"""v2 影片的技術檢查（對應父子學院 verify 的主要項目）＋人工檢視用的字幕畫格總表。

    cd $XINEW_ACADEMY && .venv/bin/python ~/QuantumComputing/academy/authoring/v2/qc_v2.py Q001

輸出 qc/verify-v2.json 與 qc/video-frames/cues_*.jpg（每條字幕中點一格，四格一張）。
"""
from pathlib import Path
import json
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_v2 import Lesson, dur, run  # noqa: E402


def probe(p):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', p]))


def main(lid):
    L = Lesson(lid)
    E = L.E
    t = json.loads((E / 'production/timing.json').read_text(encoding='utf-8'))
    expected = t['opening'] + sum(s['duration'] for s in t['scenes'])
    checks = []
    def ok(name, cond, detail):
        checks.append({'check': name, 'status': 'PASS' if cond else 'FAIL', 'detail': detail})
    master = E / 'output' / f'{L.name}-master.mp4'; zh = E / 'output' / f'{L.name}-zh-TW.mp4'
    for name, p in (('master', master), ('zh', zh)):
        d = dur(p); ok(f'{name}_duration', abs(d - expected) < 0.25, f'{d:.2f}s vs expected {expected:.2f}s')
        err = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-f', 'null', '-'], capture_output=True, text=True).stderr
        ok(f'{name}_full_decode', not err.strip(), f'{len(err)} error bytes')
        pr = probe(p)
        v = next(s for s in pr['streams'] if s['codec_type'] == 'video'); a = next(s for s in pr['streams'] if s['codec_type'] == 'audio')
        ok(f'{name}_video_format', (v['codec_name'], v['width'], v['height'], v['r_frame_rate']) == ('h264', 1920, 1080, '30/1'),
           f"{v['codec_name']} {v['width']}x{v['height']} @{v['r_frame_rate']}")
        ok(f'{name}_audio_format', (a['codec_name'], a['sample_rate'], a['channels']) == ('aac', '48000', 2), f"{a['codec_name']} {a['sample_rate']}Hz x{a['channels']}")
    lo = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(zh), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', lo)[-1])
    ok('loudness', -18 <= I <= -14, f'integrated {I} LUFS')
    srt = (E / 'subtitles/zh-TW.srt').read_text(encoding='utf-8').strip().split('\n\n')
    n_sent = sum(len(s['sentences']) for s in t['scenes'])
    ok('subtitle_count', len(srt) == n_sent, f'{len(srt)} cues / {n_sent} sentences')
    def ts(x):
        h, m, r = x.split(':'); s, ms = r.split(','); return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    times = [tuple(map(ts, b.splitlines()[1].split(' --> '))) for b in srt]
    ok('subtitle_monotonic', all(a < b for a, b in times) and all(times[i][1] <= times[i + 1][0] for i in range(len(times) - 1)),
       f'first {times[0][0]:.2f}s, last end {times[-1][1]:.2f}s')
    texts = [x['text'] for s in t['scenes'] for x in s['sentences']]
    ok('subtitle_text', [b.split('\n', 2)[2] for b in srt] == texts, 'delivered SRT text equals narration')
    ok('demo_pages', sum(s['kind'] == 'demo' for s in t['scenes']) == len(L.demos), f"{len(L.demos)} demo segments")
    # 字幕中點畫格
    fd = E / 'qc/video-frames'; fd.mkdir(parents=True, exist_ok=True)
    for f in fd.glob('*'):
        f.unlink()
    from PIL import Image
    shots = []
    for i, (a, b) in enumerate(times, 1):
        p = fd / f'cue_{i:02d}.png'
        run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{(a + b) / 2:.3f}', '-i', zh, '-frames:v', '1', p]); shots.append(p)
    for k in range(0, len(shots), 4):
        sheet = Image.new('RGB', (1920, 1080))
        for j, p in enumerate(shots[k:k + 4]):
            sheet.paste(Image.open(p).resize((960, 540)), ((j % 2) * 960, (j // 2) * 540))
        sheet.save(fd / f'cues_{k + 1:02d}-{min(k + 4, len(shots)):02d}.jpg', quality=85)
    for p in shots:
        p.unlink()
    passed = sum(c['status'] == 'PASS' for c in checks)
    json.dump({'checks': checks, 'passed': passed, 'total': len(checks), 'integratedLufs': I, 'duration': dur(zh)},
              open(E / 'qc/verify-v2.json', 'w'), ensure_ascii=False, indent=2)
    for c in checks:
        print(f"[{c['status']}] {c['check']}: {c['detail']}")
    print(f'{passed}/{len(checks)} checks passed')


if __name__ == '__main__':
    main(sys.argv[1])

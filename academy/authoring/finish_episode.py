"""量子電腦學程每集的收尾：verify → package → report → 分段 ZIP → 預覽版 → 複製回本 repo → delivery.json → 狀態表。

先寫好 $EP/qc/manual-review.md 與 slide-visual-review.md（人工檢視紀錄不自動產生），再執行：

    python3 ~/QuantumComputing/academy/authoring/finish_episode.py Q002 q002-coin-and-arrow 開學任務 2026-11-09 \
        --note "…" --not-done "…" --out /path/to/handover-folder

需要 XINEW_ACADEMY（預設 /home/user/xinewvideogpt/academy）。不會 commit，也不會上傳。
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess

X = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
Q = Path(__file__).resolve().parents[2]


def run(*cmd, **kw):
    print('$', ' '.join(map(str, cmd)))
    return subprocess.run([str(c) for c in cmd], check=True, cwd=X, **kw)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lesson'); ap.add_argument('slug'); ap.add_argument('short'); ap.add_argument('date')
    ap.add_argument('--note', default=''); ap.add_argument('--not-done', default='')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    ep = f'specials/{a.slug}'
    E = X / ep
    for f in ('qc/manual-review.md', 'qc/slide-visual-review.md'):
        assert (E / f).is_file(), f'write {f} first'
    rt = X / 'portable-runtime.sh'
    out = run(rt, 'python', 'pipeline/academy.py', 'run', 'verify', '--episode', ep, capture_output=True, text=True).stdout
    print(out.strip().splitlines()[-1])
    assert '25/25 checks passed' in out, out
    pkg = f'delivery/{a.lesson}-v1'
    if (X / pkg).exists():
        shutil.rmtree(X / pkg)
    run(rt, 'python', 'pipeline/academy.py', 'package', '--episode', ep, '--output', pkg)
    run(rt, 'python', 'pipeline/qa/write_report.py', '--episode', ep, '--date', a.date, '--note', a.note, '--not-done', a.not_done)
    name = f'{a.lesson}-v1_量子電腦學程_{a.short}_{a.date}'
    for old in (X / 'delivery/parts').glob(f'{a.lesson}-v1*'):
        old.unlink()
    run(rt, 'python', 'pipeline/split_delivery.py', '--package', pkg, '--name', name, capture_output=True)
    O = Path(a.out); O.mkdir(parents=True, exist_ok=True)
    for p in (X / 'delivery/parts').glob(f'{a.lesson}-v1*'):
        shutil.copyfile(p, O / p.name)
    shutil.copyfile(X / pkg / f'{a.slug}.pptx', O / f'{a.lesson}_{a.short}_簡報.pptx')
    shutil.copyfile(X / pkg / 'classroom.zip', O / f'{a.lesson}_{a.short}_教材.zip')
    preview = O / f'{a.lesson}_預覽版_{a.short}.mp4'
    for crf in (31, 34, 37):
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(X / pkg / f'{a.slug}-zh-TW.mp4'), '-c:v', 'libx264', '-preset', 'slow',
                        '-crf', str(crf), '-tune', 'stillimage', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(preview)], check=True)
        if preview.stat().st_size < 29 * 1024 * 1024:
            break
    assert preview.stat().st_size < 30 * 1024 * 1024, 'preview too large'

    dest = Q / 'academy/episodes' / a.slug
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(E, dest)
    for p in list(dest.glob('output/*.mp4')) + list(dest.glob('output/narration-only.mp3')):
        p.unlink()
    for d in ('qc/clips', 'qc/frames', 'qc/subtitle-precheck'):
        shutil.rmtree(dest / d, ignore_errors=True)

    asm = json.loads((E / 'qc/assembly.json').read_text(encoding='utf-8'))
    media = json.loads((E / 'qc/media-review.json').read_text(encoding='utf-8'))
    asr = json.loads((E / 'qc/asr-review.json').read_text(encoding='utf-8')) if (E / 'qc/asr-review.json').is_file() else {}
    loud = json.loads((E / 'qc/loudness-normalization.json').read_text(encoding='utf-8'))
    zipf = X / 'delivery' / f'{name}.zip'
    parts = sorted((X / 'delivery/parts').glob(f'{name}.zip.part*'))
    d = {'schemaVersion': 1, 'lessonId': a.lesson, 'program': '父子科技學院 量子電腦學程', 'episodePath': f'academy/episodes/{a.slug}',
         'version': f'{a.lesson}-v1', 'createdAt': a.date,
         'producedBy': 'Claude (cloud Linux session) via XiNewVideoGPT academy portable-runtime.sh + ooxml-template (special_builder route)',
         'status': 'verified', 'publicationStatus': 'awaiting_user_upload', 'contentMode': 'curriculum-based-preclass (no recording)',
         'durationSeconds': asm['masterDuration'], 'openingSeconds': asm['opening']['seconds'], 'voice': 'zh-TW-YunJheNeural', 'ttsEngine': 'edge-tts 7.3.1',
         'validation': {'passed': 25, 'total': 25, 'integratedLufsPredicted': loud.get('predictedIntegratedLUFS'),
                        'sceneAudioMaxLagMs': media['maxAbsLagMs'], 'sceneAudioMinCorrelation': media['minCorrelation'],
                        **{k: asr.get(k) for k in ('minSimilarity', 'meanSimilarity', 'minSoundSimilarity', 'meanSoundSimilarity')},
                        'reviewRecords': ['qc/report.md', 'qc/manual-review.md', 'qc/slide-visual-review.md'],
                        'notDone': [x for x in a.not_done.split('；') if x]},
         'largeFiles': {f.name: {'bytes': f.stat().st_size, 'sha256': sha(f)} for f in sorted((X / pkg).iterdir()) if f.suffix in ('.mp4', '.mp3')},
         'package': {'filename': zipf.name, 'bytes': zipf.stat().st_size, 'sha256': sha(zipf),
                     'parts': [{'name': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in parts],
                     'restore': f'依序把 .part 檔接成 {zipf.name}，再比對 sha256；詳見 {a.lesson}-v1_還原說明_RESTORE.txt',
                     'handedOver': f'{a.date} 以對話附件交給使用者（分段＋還原說明），另附重新壓縮的預覽版 MP4（{preview.stat().st_size / 1048576:.1f} MiB，非上傳用）'},
         'notInGit': 'MP4 與純旁白 MP3 不進 Git；檔名、大小與 SHA-256 記於本檔'}
    (dest / 'delivery.json').write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    sp = Q / 'academy/curriculum/production-status.json'
    s = json.loads(sp.read_text(encoding='utf-8'))
    s['lessons'][a.lesson] = {'status': 'verified', 'publication': 'awaiting_user_upload', 'episodePath': f'academy/episodes/{a.slug}',
                              'evidence': f'academy/episodes/{a.slug}/delivery.json'}
    sp.write_text(json.dumps(s, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    subprocess.run(['python3', str(Q / 'academy/curriculum/build_curriculum.py')], check=True)
    print('handover folder:', O)
    for p in sorted(O.iterdir()):
        print(f'  {p.name}  {p.stat().st_size}')


if __name__ == '__main__':
    main()

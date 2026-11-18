"""v2 交付：教材、說明檔、交付資料夾、分段 ZIP、預覽版、複製回本 repo、delivery.json、狀態表。

先寫好 $EP/qc/manual-review.md（人工檢視紀錄），再執行：
    cd $XINEW_ACADEMY && .venv/bin/python ~/QuantumComputing/academy/authoring/v2/deliver_v2.py Q001 開學任務 2026-11-18 /path/to/handover
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_v2 import HERE, Q, X, Lesson, dump, dur, run  # noqa: E402
from demos import PAGES  # noqa: E402


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def stamp(s):
    s = int(s); m, sec = divmod(s, 60)
    return f'{m:02d}:{sec:02d}'


def main(lid, short, date, outdir):
    L = Lesson(lid); E = L.E
    ver = json.loads((E / 'qc/verify-v2.json').read_text(encoding='utf-8'))
    assert ver['passed'] == ver['total'], 'run qc_v2.py until all checks pass'
    assert (E / 'qc/manual-review.md').is_file(), 'write qc/manual-review.md first'
    t = json.loads((E / 'production/timing.json').read_text(encoding='utf-8'))
    title = L.v1man['title']
    P = E / 'production'
    # 文件
    chapters, cur = [(0, '陳犀牛系列片頭')], t['opening']
    for s in t['scenes']:
        chapters.append((cur, s['title'])); cur += s['duration']
    (P / 'chapters.txt').write_text(''.join(f'{stamp(a)} {b}\n' for a, b in chapters), encoding='utf-8')
    (P / 'narration-script.md').write_text('\n\n'.join(
        f"## {s['page']:02d} {s['title']}" + ('（動畫展示）' if s['kind'] == 'demo' else '') + '\n\n' + '\n\n'.join(x['text'] for x in s['sentences'])
        for s in t['scenes']) + '\n', encoding='utf-8')
    demos_txt = '\n'.join(f"・{d['title'].replace('動畫展示：', '')}（{PAGES[d['page']][1]}#{d['hash']}）" for d in L.demos)
    summary = (f"這是依課綱製作的課前教學版，不是實際上課錄音。\n\n父子科技學院量子電腦學程 {lid}「{title}」新版（v2）："
               f"在原本的教學投影片之間，插入本學程 3D 互動動畫的實際操作示範。\n\n這一版新增的動畫展示\n{demos_txt}\n\n"
               "動畫都可以在瀏覽器直接開啟，自己動手操作。\n")
    desc = (f"父子科技學院 量子電腦學程 {lid}｜{title}（v2・含 3D 動畫展示）\n\n{summary}\n章節\n"
            + ''.join(f'{stamp(a)} {b}\n' for a, b in chapters)
            + '\n旁白：Edge-TTS zh-TW-YunJheNeural 合成語音。字幕已燒入影片，開啟 CC 可能重疊。\n')
    (P / 'youtube-description.txt').write_text(desc, encoding='utf-8')
    dump(P / 'youtube-metadata.json', {'title': f'父子科技學院 {lid}｜{title}（動畫展示版）', 'description': desc, 'privacyStatus': 'private',
                                       'madeForKids': None, 'reviewStatus': 'needs-parent-review', 'publicationMode': 'manual-user-upload'})
    shutil.copyfile(HERE / 'fact_check_v2.md', P / 'fact-check-v2.md')
    shutil.copyfile(L.v1 / 'production/fact-check.md', P / 'fact-check-v1.md')
    # 教材：v1 教材＋動畫展示導覽
    cz = E / 'output/classroom.zip'
    if (L.v1 / 'output/classroom.zip').is_file():
        shutil.copyfile(L.v1 / 'output/classroom.zip', cz)
    else:  # Q004 起沒有單獨交付 v1，直接打包 v1 的 classroom 資料夾
        with zipfile.ZipFile(cz, 'w', zipfile.ZIP_DEFLATED) as z:
            for f in sorted((L.v1 / 'classroom').rglob('*')):
                if f.is_file():
                    z.write(f, f.relative_to(L.v1 / 'classroom'))
    guide = [f'# {lid} 動畫展示導覽（v2）\n', '影片裡的動畫展示都可以自己操作。線上版不用下載；也可以下載 pcpcchen-coder/QuantumComputing 後，用瀏覽器開啟 `animations/` 裡的檔案。\n']
    for d in L.demos:
        guide.append(f"## {d['title']}\n\n- 開啟：{PAGES[d['page']][1]}#{d['hash']}（{d['scene']}）\n- 影片中的旁白：\n"
                     + ''.join(f'  - {s}\n' for s in d['sentences'])
                     + '- 觀察重點：' + '；'.join(f'{h}——{b}' for h, b in d['points']) + '\n')
    with zipfile.ZipFile(cz, 'a') as z:
        root = sorted({n.split('/')[0] for n in z.namelist()})[0]
        z.writestr(f'{root}/06_動畫展示導覽.md', '\n'.join(guide))
    # 純旁白
    mp3 = E / 'output/narration-only.mp3'
    run(['ffmpeg', '-y', '-v', 'error', '-i', E / 'output' / f'{L.name}-master.mp4', '-vn', '-c:a', 'libmp3lame', '-b:a', '192k', mp3])
    # 交付資料夾
    pkg = X / 'delivery' / f'{lid}-v2'
    if pkg.exists():
        shutil.rmtree(pkg)
    pkg.mkdir(parents=True)
    files = {E / 'output' / f'{L.name}-zh-TW.mp4': None, E / 'output' / f'{L.name}-master.mp4': None,
             E / 'production/presentation' / f'{L.name}.pptx': None, E / 'subtitles/zh-TW.srt': None, cz: None, mp3: None,
             P / 'chapters.txt': None, P / 'narration-script.md': None, P / 'youtube-description.txt': None, P / 'youtube-metadata.json': None,
             P / 'fact-check-v1.md': None, P / 'fact-check-v2.md': None, E / 'qc/manual-review.md': None, E / 'qc/verify-v2.json': None,
             E / 'output/thumbnail.png': None}
    for f in files:
        shutil.copyfile(f, pkg / f.name)
    (pkg / 'START_HERE.md').write_text(f"# {lid} {title}（v2・含 3D 動畫展示）\n\n{summary}\n播放 {L.name}-zh-TW.mp4（字幕已燒入），實測 {dur(E / 'output' / f'{L.name}-zh-TW.mp4'):.2f} 秒；"
                                       f"{L.name}-master.mp4 為無字幕母帶，zh-TW.srt 為字幕檔。\n簡報 {L.name}.pptx 共 {L.total} 頁，動畫展示頁有開啟線上動畫的連結。\n"
                                       "classroom.zip 是 v1 教材加上 06_動畫展示導覽。本包未上傳 YouTube。\n", encoding='utf-8')
    dump(pkg / 'checksums.json', {f.name: sha(f) for f in sorted(pkg.iterdir()) if f.name != 'checksums.json'})
    name = f'{lid}-v2_量子電腦學程_{short}_動畫展示版_{date}'
    run([X / 'portable-runtime.sh', 'python', 'pipeline/split_delivery.py', '--package', f'delivery/{lid}-v2', '--name', name], cwd=str(X))
    O = Path(outdir); O.mkdir(parents=True, exist_ok=True)
    parts = sorted((X / 'delivery/parts').glob(f'{name}.zip.part*'))
    for p in parts + list((X / 'delivery/parts').glob(f'{lid}-v2_還原說明*')):
        shutil.copyfile(p, O / p.name)
    shutil.copyfile(E / 'production/presentation' / f'{L.name}.pptx', O / f'{lid}_{short}_v2_簡報.pptx')
    shutil.copyfile(cz, O / f'{lid}_{short}_v2_教材.zip')
    preview = O / f'{lid}_v2預覽版_{short}.mp4'
    for crf in (31, 34, 37, 40):
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(E / 'output' / f'{L.name}-zh-TW.mp4'), '-c:v', 'libx264', '-preset', 'slow',
                        '-crf', str(crf), '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(preview)], check=True)
        if preview.stat().st_size < 29 * 1024 * 1024:
            break
    assert preview.stat().st_size < 30 * 1024 * 1024
    # 複製回本 repo（不含大型影片與錄影原檔）
    dest = Q / 'academy/episodes' / L.name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(E, dest, ignore=shutil.ignore_patterns('work', '*.mp4', '*.webm', 'narration-only.mp3'))
    zipf = X / 'delivery' / f'{name}.zip'
    big = [E / 'output' / f'{L.name}-zh-TW.mp4', E / 'output' / f'{L.name}-master.mp4', mp3]
    dump(dest / 'delivery.json', {
        'schemaVersion': 1, 'lessonId': lid, 'version': f'{lid}-v2', 'edition': '動畫展示版', 'createdAt': date,
        'episodePath': f'academy/episodes/{L.name}', 'basedOn': f'academy/episodes/{L.slug}（v1 的 12 頁旁白與音訊沿用）',
        'producedBy': 'Claude (cloud Linux session): academy/authoring/v2/build_v2.py on the XiNewVideoGPT portable runtime',
        'status': 'verified', 'publicationStatus': 'awaiting_user_upload', 'durationSeconds': ver['duration'], 'pages': L.total,
        'demos': [{'key': d['key'], 'title': d['title'], 'animation': f"{PAGES[d['page']][1]}#{d['hash']}"} for d in L.demos],
        'validation': {**{k: ver[k] for k in ('passed', 'total', 'integratedLufs')},
                       'records': ['qc/verify-v2.json', 'qc/manual-review.md', 'qc/asr-review.json']},
        'largeFiles': {f.name: {'bytes': f.stat().st_size, 'sha256': sha(f)} for f in big},
        'package': {'filename': zipf.name, 'bytes': zipf.stat().st_size, 'sha256': sha(zipf),
                    'parts': [{'name': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in parts],
                    'handedOver': f'{date} 以對話附件交給使用者（分段＋還原說明），另附重新壓縮的預覽版 MP4（非上傳用）'},
        'notInGit': 'MP4、錄影原檔（webm）與純旁白 MP3 不進 Git；檔名、大小與 SHA-256 記於本檔'})
    sp = Q / 'academy/curriculum/production-status.json'
    s = json.loads(sp.read_text(encoding='utf-8'))
    s['lessons'][lid]['v2'] = {'status': 'verified', 'publication': 'awaiting_user_upload', 'episodePath': f'academy/episodes/{L.name}',
                               'evidence': f'academy/episodes/{L.name}/delivery.json'}
    sp.write_text(json.dumps(s, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('handover:', O)
    for p in sorted(O.iterdir()):
        print(f'  {p.name}  {p.stat().st_size}')


if __name__ == '__main__':
    main(*sys.argv[1:5])

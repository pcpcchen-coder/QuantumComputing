"""一次補齊某一課的 TTS 快取：12 頁旁白（specials/<slug>/production/narration.json）＋ v2 動畫展示段旁白。
用的是父子學院管線同一個 synthesize()（同樣的完整性檢查與快取），失敗就等 90 秒再試。

    cd $XINEW_ACADEMY && .venv/bin/python ~/QuantumComputing/academy/authoring/v2/fill_lesson_tts.py Q004
"""
import json, os, sys, tempfile, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
X = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy'))
lid = sys.argv[1]
sys.path.insert(0, str(HERE))
from build_v2 import LESSONS  # noqa: E402
from demos import DEMOS  # noqa: E402
slug = LESSONS[lid]
sys.argv = [sys.argv[0], '--episode', f'specials/{slug}']
sys.path.insert(0, str(X / 'pipeline/scripts'))
import synthesize_narration as sn  # noqa: E402
base = [x.get('tts') or x['text'] for s in json.loads((X / 'specials' / slug / 'production/narration.json').read_text()) for x in s['sentences']]
todo = base + [s for d in DEMOS.get(lid, []) for s in d['sentences']]
for i, t in enumerate(todo, 1):
    for r in range(1, 31):
        try:
            with tempfile.TemporaryDirectory() as d:
                sn.synthesize(t, Path(d) / 'x.mp3')
            print(f'OK {i}/{len(todo)} (round {r})', flush=True); break
        except RuntimeError:
            print(f'wait {i}/{len(todo)} round {r}', flush=True); time.sleep(90)
    else:
        print('GIVEUP', i, t, flush=True); sys.exit(1)
print('ALLDONE', len(todo), flush=True)

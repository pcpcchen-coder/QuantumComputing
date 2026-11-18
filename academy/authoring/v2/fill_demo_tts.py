"""Fill the XiNewVideoGPT TTS cache for every v2 demo sentence (same synthesize() and completeness checks as the pipeline).

    cd $XINEW_ACADEMY && .venv/bin/python ~/QuantumComputing/academy/authoring/v2/fill_demo_tts.py [Q001 Q002 ...]
"""
import os, sys, tempfile, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
X = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy'))
sys.argv = [sys.argv[0], '--episode', 'specials/q001-not-faster'] + sys.argv[1:]
lessons = sys.argv[3:] or ['Q001', 'Q002', 'Q003']
sys.argv = sys.argv[:3]
sys.path.insert(0, str(X / 'pipeline/scripts')); sys.path.insert(0, str(HERE))
import synthesize_narration as sn  # noqa: E402
from demos import DEMOS  # noqa: E402
todo = [s for l in lessons for d in DEMOS[l] for s in d['sentences']]
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
print('ALLDONE', flush=True)

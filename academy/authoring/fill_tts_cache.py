"""Patiently fill XiNewVideoGPT .build-tts-cache for one episode using the pipeline's own synthesize() (same completeness checks).

    cd $XINEW_ACADEMY && .venv/bin/python ~/QuantumComputing/academy/authoring/fill_tts_cache.py specials/qxxx-<slug>
"""
import json, sys, time, tempfile
from pathlib import Path
ep = Path(sys.argv[1])
sys.argv = [sys.argv[0], '--episode', str(ep)]
import os
sys.path.insert(0, os.path.join(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy'), 'pipeline/scripts'))
import synthesize_narration as sn
sents = [x['tts'] for s in json.loads((ep/'production/narration.json').read_text()) for x in s['sentences']]
for i, t in enumerate(sents, 1):
    for round_ in range(1, 16):
        try:
            with tempfile.TemporaryDirectory() as d:
                sn.synthesize(t, Path(d)/'x.mp3')
            print(f'OK {i}/36 (round {round_})', flush=True); break
        except RuntimeError as e:
            print(f'wait {i}/36 round {round_}', flush=True); time.sleep(90)
    else:
        print(f'GIVEUP {i}', flush=True); sys.exit(1)
print('ALLDONE', flush=True)

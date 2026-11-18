#!/bin/bash
# 單課製作：Azure 補 TTS 快取 → v1 tts（timing）→ v2 audio/record/deck/assemble → qc_v2 → ASR
# 用法：produce.sh Q011    （先跑過 prepare_content.py 建好 v1 special，demos_extra/q011.py 已寫好）
set -eo pipefail
L=$1; V2=$(cd "$(dirname "$0")/.." && pwd); XA=${XINEW_ACADEMY:-/home/user/xinewvideogpt/academy}; W=${QWORK:-/home/user/qwork}
SLUG=$(cd "$XA" && .venv/bin/python -c "import sys; sys.path.insert(0,'$V2'); from build_v2 import LESSONS; print(LESSONS['$L'])")
cd "$XA"
echo "== $L $SLUG azure tts"; .venv/bin/python $V2/fill_tts_azure.py $L 2>&1 | tail -2
echo "== $L $SLUG v1 tts"; ./portable-runtime.sh python pipeline/academy.py run tts --episode specials/$SLUG 2>&1 | tail -3
for st in audio record deck assemble; do echo "== $L $st"; .venv/bin/python $V2/build_v2.py $L $st 2>&1 | tail -4; done
echo "== $L qc"; .venv/bin/python $V2/qc_v2.py $L 2>&1 | tail -3
echo "== $L asr"; "$W/asr/bin/python" $V2/tools/asr_review_v2.py --episode specials/$SLUG-v2 --model "$W/fw-small" > "$W/asr-$L.log" 2>&1; tail -1 "$W/asr-$L.log"
echo "PRODUCED $L"

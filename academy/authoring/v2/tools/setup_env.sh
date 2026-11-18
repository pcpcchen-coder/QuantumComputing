#!/bin/bash
# 新雲端容器一次性準備：XiNewVideoGPT 可攜環境 + 本機語音辨識（faster-whisper small）
# 需要：/home/user/xinewvideogpt 已 clone（add_repo pcpcchen-coder/xinewvideogpt 後 git clone）
set -eo pipefail
XA=${XINEW_ACADEMY:-/home/user/xinewvideogpt/academy}
W=${QWORK:-/home/user/qwork}; mkdir -p "$W"
(cd "$XA" && ./setup-portable.sh)
[ -x "$W/asr/bin/python" ] || { python3 -m venv "$W/asr"; "$W/asr/bin/pip" install -q faster-whisper zhconv pypinyin huggingface_hub; }
[ -f "$W/fw-small/model.bin" ] || (cd "$W" && asr/bin/python -c "from huggingface_hub import snapshot_download; print(snapshot_download('Systran/faster-whisper-small', local_dir='fw-small'))")
for b in soffice ffmpeg node; do command -v $b >/dev/null || { echo "missing $b"; exit 1; }; done
node -e "require('playwright')" || { echo "playwright missing"; exit 1; }
echo SETUP_OK

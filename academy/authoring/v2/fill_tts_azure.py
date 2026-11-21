"""用 Azure 語音服務（同一聲音 zh-TW-YunJheNeural、同一格式 24 kHz 48 kbps mono MP3）補 TTS 快取。
Edge 免費端點限流時使用；快取鍵與父子學院 synthesize() 相同，之後管線直接取用。
金鑰由環境的網路代理注入（主機 AZURE_TTS_HOST，預設 eastasia.tts.speech.microsoft.com），程式不讀金鑰。

    cd $XINEW_ACADEMY && .venv/bin/python ~/QuantumComputing/academy/authoring/v2/fill_tts_azure.py Q004 Q005 ...
"""
import hashlib, json, os, subprocess, sys, time, urllib.request
from pathlib import Path
from xml.sax.saxutils import escape
HERE = Path(__file__).resolve().parent
X = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy'))
sys.path.insert(0, str(HERE))
from build_v2 import LESSONS  # noqa: E402
from demos import DEMOS  # noqa: E402
VOICE = 'zh-TW-YunJheNeural'
HOST = os.environ.get('AZURE_TTS_HOST', 'eastasia.tts.speech.microsoft.com')
CACHE = X / '.build-tts-cache'


def fetch(text):
    ssml = f"<speak version='1.0' xml:lang='zh-TW'><voice name='{VOICE}'>{escape(text)}</voice></speak>".encode()
    req = urllib.request.Request(f'https://{HOST}/cognitiveservices/v1', data=ssml, method='POST', headers={
        'Content-Type': 'application/ssml+xml', 'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
        'User-Agent': 'qc-academy-tts'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(p)],
                                capture_output=True, text=True, check=True).stdout)


for lid in sys.argv[1:]:
    slug = LESSONS[lid]
    base = [x.get('tts') or x['text'] for s in json.loads((X / 'specials' / slug / 'production/narration.json').read_text()) for x in s['sentences']]
    todo = base + [s for d in DEMOS.get(lid, []) for s in d['sentences']]
    new = 0
    for t in todo:
        out = CACHE / (hashlib.sha256(f'{VOICE}|+0%|+0Hz|{t}'.encode('utf-8')).hexdigest() + '.mp3')
        if out.is_file():
            continue
        for attempt in range(6):
            try:
                a = fetch(t); break
            except Exception as e:  # noqa: BLE001
                print('retry', attempt, e, flush=True); time.sleep(5 * (attempt + 1))
        else:
            sys.exit(f'FAILED {lid}: {t}')
        tmp = out.with_suffix('.tmp'); tmp.write_bytes(a)
        d = dur(tmp); n = sum(ch.isalnum() for ch in t)
        assert len(a) > 2000 and 1.5 < n / d < 9, (t, len(a), d)
        tmp.rename(out); new += 1
    print(f'{lid}: {len(todo)} sentences, {new} new from Azure', flush=True)
print('ALLDONE')

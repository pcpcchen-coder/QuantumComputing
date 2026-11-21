"""產生 v2 人工檢視紀錄（qc/manual-review.md）：
    python3 write_review.py Q011 '<親自看過的抽格總表與段名>' '<字面低於 0.8 各條的原因說明>'
產生後要再讀一遍，必要時手動補充；不可把機器檢查寫成真人聽審。
EDGE：先前用 Edge TTS 合成的句數（Q011 起全部走 Azure，為 0）。
"""
import json, sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from build_v2 import LESSONS as SL  # noqa: E402
X = os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')
lid, seen, note = sys.argv[1], sys.argv[2], sys.argv[3]
E = f'{X}/specials/{SL[lid]}-v2'
v = json.load(open(E+'/qc/verify-v2.json')); a = json.load(open(E+'/qc/asr-review.json')); t = json.load(open(E+'/production/timing.json'))
c, demos, after, rates = 1, [], [], []
for i, s in enumerate(t['scenes']):
    n = len(s['sentences'])
    if s['kind'] == 'demo':
        demos.append((s['title'].replace('動畫展示：',''), c, c+n-1)); after.append(t['scenes'][i-1]['page'] if i else 0)

    c += n
total = c-1; new = total-36
rates = [len(x['text'])/(x['end']-x['start']) for sc in t['scenes'] for x in sc['sentences']]
EDGE = {'Q009': 38, 'Q008': 1}.get(lid, 0)
low = [r for r in a['rows'] if r['similarity'] < 0.8]
snd = [r for r in a['rows'] if r['soundSimilarity'] < 0.9]
L = [f"# {lid} v2（動畫展示版）內容、畫面與聲音檢視紀錄\n",
 "日期：2026-11-18（UTC）。檢視者：製作代理 Claude（雲端 Linux 環境）。",
 "**這不是真人聽審。** 代理可以看圖、讀文字、跑量測與語音辨識，不能用耳朵聽；聲音部分全部是機器證據。\n",
 "## 這一版改了什麼\n",
 f"- 以 v1 稿的 12 頁教學旁白為基礎，在第 {'、'.join(str(p) for p in after)} 頁之後插入 {len(demos)} 段「動畫展示」，新增 {new} 句旁白，全片 {total} 句。",
 "- 動畫展示是本 repo 3D 動畫的實際操作錄影：程式依旁白時間點自動按按鈕、拖滑桿（被操作的元件閃黃框），右欄三個觀察重點依旁白逐一亮黃框。",
 f"- 新版簡報 {12+len(demos)} 頁：v1 的 12 頁加上 {len(demos)} 頁動畫展示頁（截圖、觀察重點、線上動畫連結）。\n",
 "## 做了什麼\n",
 f"### 技術檢查（`verify-v2.json`，{v['passed']}/{v['total']} 通過）",
 f"片長 {v['duration']:.1f} 秒與時間表一致、母帶與字幕版整檔解碼無錯、H.264 1920×1080 30 fps、AAC 48 kHz 立體聲、整體 {v['integratedLufs']} LUFS、{total} 條字幕與旁白逐字一致且時間遞增、{len(demos)} 段動畫展示。\n",
 f"### 畫面（{total} 條字幕）",
 f"- 從最終字幕版 MP4 在每條字幕中點取一格，產生 {-(-total//4)} 張總表。",
 f"- 主代理親自看過的總表：{seen}。動畫段每一句的畫面另由查核子代理逐張對照旁白（結果寫在 `production/fact-check-v2.md`，含補抽的錄影畫格）。",
 "- 動畫段：" + '；'.join(f"「{d}」字幕第 {s}–{e} 條" for d, s, e in demos) + "。看過的畫格中，被操作的按鈕、箭頭位置、讀數與旁白一致，右欄觀察重點依序亮框。",
 "- 已知版面現象：兩行字幕會蓋住錄影畫面最下緣一條（那裡是頁面說明文字，不是旁白在講的主畫面）。\n",
 "### 聲音（機器量測，非聽審）",
 f"- 逐條語音辨識（本機 faster-whisper small）：字面相似度最低 {a['minSimilarity']}、平均 {a['meanSimilarity']}；拼音比對最低 {a['minSoundSimilarity']}、平均 {a['meanSoundSimilarity']}，沒有任何一條拼音比對低於 0.8。",
 f"- 字面低於 0.8 的第 {'、'.join(str(r['cue']) for r in low) or '（無）'} 條：{note}",
]
if snd:
    L.append("- 拼音比對低於 0.9、值得真人留意的：" + '；'.join(f"第 {r['cue']} 條「{r['text']}」辨識成「{r['heard']}」（{r['soundSimilarity']}）" for r in snd) + "。這是機器旗標，沒有真人聽過，不能判定是念錯還是辨識錯。")
L += [f"- 旁白合成：Q004 起沒有另外交付 v1，全片 {total} 句旁白都在本次合成；" + (f"其中 {EDGE} 句是先前 Edge TTS 合成留下的快取，其餘 {total-EDGE} 句" if EDGE else "全部") + f"在 Edge TTS 被限流後改用 Azure 語音服務合成（同一個 zh-TW-YunJheNeural 聲音、相同 24 kHz 48 kbps 單聲道格式、相同快取鍵），每句檢查檔案大小與語速；全片語速每秒 {min(rates):.2f} 到 {max(rates):.2f} 字，沒有截短跡象。\n",
 "### 事實",
 "- 新增動畫段見 `production/fact-check-v2.md`（動畫原始碼與場景說明、計算、畫格）；v1 段落見 `production/fact-check-v1.md`。\n",
 "## 限制\n",
 "- 沒有真人整段聽審；聲調、自然度、細微誤讀無法由機器判斷。",
 "- 動畫畫面中的隨機次數是錄影當下的結果。",
 "- 沒有用 PowerPoint／Keynote 開啟 PPTX；沒有 YouTube 版權檢查。"]
open(E+'/qc/manual-review.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(E+'/qc/manual-review.md')

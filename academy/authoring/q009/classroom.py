"""Q009 課堂教材：臨摹三條線路、箭頭追蹤表、三步線路作曲卡、27 種三步線路解答表（不需帳號、不需安裝）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q009/classroom.py
"""
from pathlib import Path
import itertools
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent
R2 = 1 / math.sqrt(2)
GATES = {'X': ((0, 1), (1, 0)), 'H': ((R2, R2), (R2, -R2)), 'Z': ((1, 0), (0, -1))}
NAME = {'X': '翻轉閘 X', 'H': '哈達瑪閘 H', 'Z': '相位翻轉閘 Z'}


def apply(g, s):
    m = GATES[g]
    return (m[0][0] * s[0] + m[0][1] * s[1], m[1][0] * s[0] + m[1][1] * s[1])


def where(s):
    """箭頭位置（只用 X、H、Z 從狀態零出發，只會到四個點）。"""
    z = s[0] ** 2 - s[1] ** 2
    x = 2 * s[0] * s[1]
    if z > 0.99:
        return '北極'
    if z < -0.99:
        return '南極'
    return '赤道（前）' if x > 0 else '赤道（後）'


def result(s):
    p1 = s[1] ** 2
    return '一定是 0' if p1 < 1e-9 else '一定是 1' if p1 > 1 - 1e-9 else '一半一半'


def trace(seq):
    s, out = (1.0, 0.0), []
    for g in seq:
        s = apply(g, s)
        out.append(where(s))
    return out, result(s)


COPY = [('X',), ('H',), ('H', 'Z', 'H')]
assert trace(('H', 'Z', 'H')) == (['赤道（前）', '赤道（後）', '南極'], '一定是 1')
assert trace(('Z', 'H', 'H'))[1] == '一定是 0'
assert trace(('X',))[1] == '一定是 1' and trace(('H',))[1] == '一半一半'
ALL3 = list(itertools.product('XHZ', repeat=3))


def circuit_svg(seq, blank=False, w=100):
    """一條線路：|0⟩、導線、閘方塊、右端儀表。blank=True 畫空方塊讓孩子填。"""
    n = 3 if blank else len(seq)
    W = 70 + n * 52 + 60
    parts = [f'<svg viewBox="0 0 {W} 60" style="width:{w * W / 230:.0f}mm;height:auto" xmlns="http://www.w3.org/2000/svg">',
             '<text x="4" y="35" font-size="15" fill="#0b2540">|0⟩</text>',
             f'<line x1="40" y1="30" x2="{W - 48}" y2="30" stroke="#0b2540" stroke-width="2"/>']
    for i in range(n):
        x = 66 + i * 52
        if blank:
            parts.append(f'<rect x="{x}" y="12" width="36" height="36" rx="5" fill="#fff" stroke="#4a6a88" stroke-width="1.5" stroke-dasharray="4 3"/>')
        else:
            parts.append(f'<rect x="{x}" y="12" width="36" height="36" rx="5" fill="#e3f1f6" stroke="#0b2540" stroke-width="2"/>'
                         f'<text x="{x + 18}" y="37" font-size="18" text-anchor="middle" fill="#0b2540" font-weight="700">{seq[i]}</text>')
    mx = W - 48
    parts.append(f'<rect x="{mx}" y="14" width="34" height="32" rx="4" fill="#fff" stroke="#0b2540" stroke-width="2"/>'
                 f'<path d="M{mx + 6} 38 A11 11 0 0 1 {mx + 28} 38 M{mx + 17} 39 L{mx + 25} 22" fill="none" stroke="#0b2540" stroke-width="2"/>')
    parts.append('</svg>')
    return ''.join(parts)


ANSWER_ROWS = ''.join(
    f'| {i} | {" → ".join(seq)} | {" → ".join(trace(seq)[0])} | {trace(seq)[1]} |\n' for i, seq in enumerate(ALL3, 1))

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q009：量子線路像樂譜（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五分鐘，帶出今天的問題：科學家畫給量子電腦的「線路圖」要怎麼讀？

## 這份教材在做什麼

好玩機制是「臨摹挑戰」：孩子當畫圖員，照著場景把 3 條線路畫在方格紙上，並說出每一步箭頭轉到哪裡；爸爸當核對員。
下半場孩子自己畫一條 3 個閘的線路，爸爸預測結果，兩人再用 Q002 做的紙布洛赫球一步一步驗證。
不需要帳號；3D 場景見 `05_三維動畫導覽.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 線＝量子位元、方塊＝閘、儀表＝測量、由左往右；順序不能亂換 | 影片第 2–6 段、列印包第 4 頁符號表 |
| 25–65 | 臨摹 3 條線路（每條約 12 分鐘），說出箭頭怎麼變 | `01_臨摹步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 自己畫 3 步線路，爸爸預測，紙球驗證（可做 3 回） | 列印包第 3 頁、`03_作曲紀錄.csv` |
| 105–115 | 孩子教爸爸讀線路圖 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替三條線路取名字 | |

## 課前準備（約 5 分鐘）

- 方格紙、鉛筆、橡皮擦、尺；列印 `02_列印包_量子線路像樂譜.pdf`（A4，共 4 頁）。
- 找出 Q002 做的紙布洛赫球（沒有的話，用一枝筆當箭頭也可以）。
- 讀一遍 `04_解答表.md`：只用 X、H、Z 從狀態零出發，箭頭只會停在四個位置：北極、南極、赤道（前）、赤道（後）。

## 核對員的原則

- 先看三樣東西有沒有畫：線（還有左端的 |0⟩）、方塊（裡面的字母）、右端的儀表。
- 再看順序：同一條線上的閘順序不能交換。例如 H→Z→H 一定得到 1，Z→H→H 一定得到 0。
- 孩子說錯箭頭位置時，不急著糾正，請他拿紙球轉一次。

## 誠實說明

- 「樂譜」是幫忙記憶的比喻：閘不會發出聲音，它們是在改變量子位元的狀態。
- 「一定得到 1」指理想、沒有雜訊的情況；真實的量子電腦會有少量錯誤。
- 本課只用一條線的線路；兩條線之間的連線（例如 CNOT）留到下一堂的 Bell 態。
''',

'01_臨摹步驟.md': '''# 臨摹步驟

## 三條要臨摹的線路（場景：animations/basic-circuits.html 與 operation.html#circuit）

| 線路 | 閘的順序 | 測量結果 |
|---|---|---|
| 第一條 | X → 測量 | 一定是 1 |
| 第二條 | H → 測量 | 一半一半 |
| 第三條 | H → Z → H → 測量 | 一定是 1 |

## 每一條都這樣做

1. 看場景（或列印包第 1 頁的範例），數一數：有幾條線？幾個方塊？最後有沒有儀表？
2. 在方格紙上畫：左邊寫 |0⟩，畫一條橫線，方塊一格一個，最右邊畫儀表。
3. 用手指從左往右走，每碰到一個方塊，就說出箭頭轉到哪裡，寫進列印包第 2 頁。
4. 爸爸核對；有漏掉的就擦掉重畫。
5. 打開場景驗證：
   - 第二條：`basic-circuits.html#superposition`，按「下一步 ▶」，再按「量測 1,000 次」。
   - 第三條：`operation.html#circuit`，按「干涉：H–Z–H」，再按「單步 ▶」四次，看最後的 1000 次結果。

## 下半場：換你作曲（約 30 分鐘）

1. 在列印包第 3 頁的三個空方塊裡，從 X、H、Z 選字母填進去（可以重複）。
2. 爸爸看圖預測：0、1，還是一半一半？寫下來。
3. 兩個人拿紙球，從北極出發，一格一格轉箭頭，看誰對。對照 `04_解答表.md`。
''',

'04_解答表.md': '# 解答表（爸爸用）：27 種三步線路\n\n'
  '從狀態零（北極）出發，只用 X、H、Z。赤道（前）是 H 把北極轉過去的那一點（+x 方向），赤道（後）是它的對面（−x 方向）。\n'
  'X：北極和南極對調；赤道上的點不動。H：北極 ↔ 赤道（前）、南極 ↔ 赤道（後）。Z：赤道（前）↔ 赤道（後）；北極、南極不動。\n\n'
  '| # | 線路 | 每一步後箭頭在哪 | 測量結果 |\n|---|---|---|---|\n' + ANSWER_ROWS
  + '\n## 臨摹的三條線路\n\n'
  + ''.join(f'- {" → ".join(s)}：{" → ".join(trace(s)[0])}；{trace(s)[1]}\n' for s in COPY)
  + '\n## 常見問題\n\n'
  '- 「赤道（後）測量也是一半一半嗎？」是。赤道上的兩點測量結果一樣，差別只在相位（Q005）；要再經過一個 H 才看得出來。\n'
  '- 「Z 對北極沒有作用？」對。Z 只改變狀態一那部分的正負號；箭頭在北極時看起來不動。\n',

'05_三維動畫導覽.md': '''# 三維動畫導覽

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## `animations/basic-circuits.html#superposition`（量子電路入門：疊加）

- 上方是線路圖：左端標 |0⟩，中間的方塊是 H，最右邊是量測錶。
- 「下一步 ▶」「◀ 上一步」：一步一步走；直線游標代表現在走到哪裡。
- 右邊「量測 1,000 次」：看 0 和 1 各幾次；「清除」重來。
- 上方「起始態」可以切成 |1⟩，線路會多一個 X。

## `animations/operation.html#circuit`（場景 6：量子線路）

- 上排按鈕選線路；今天用「干涉：H–Z–H」。
- 「單步 ▶」：執行下一欄，正在執行的方塊會發光；下方柱子是當下的狀態（高度＝機率，顏色＝相位）。
- 走到最後的量測欄會跑 1000 次，右下角顯示直方圖。
- 「⏮ 重設」回到起點；「播放」自動一步一步走。

## 操作

滑鼠拖曳旋轉、滾輪縮放；`H` 隱藏面板；`R` 重設視角。
''',
}

SHEET_HEADER = ['回合', '我畫的線路（例：H→Z→H）', '爸爸預測', '紙球第一步', '紙球第二步', '紙球第三步', '測量結果', '誰猜對']
SHEET_ROWS = ([[f'臨摹{i}', ' → '.join(s), '', *(trace(s)[0] + ['', ''])[:3], trace(s)[1]] for i, s in enumerate(COPY, 1)]
              + [[f'作曲{i}'] for i in range(1, 4)])

EXTRA_CSS = '''.grid{height:34mm;border:1pt solid #9fb7cf;margin:2mm 0 4mm;
background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt),linear-gradient(90deg,#cfdde8 .6pt,transparent .6pt);background-size:5mm 5mm}
.ex{display:flex;align-items:center;gap:6mm}.ex b{min-width:16mm}
table.trk td{height:12mm}table.cmp td{height:10mm}
.sym td{font-size:12pt}.chk li{margin:3mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    copy_blocks = ''.join(
        f'<div class="ex"><b>第{"一二三"[i]}條</b>{circuit_svg(s)}</div><div class="grid"></div>' for i, s in enumerate(COPY))
    trk_rows = ''.join(
        f'<tr><td>第{"一二三"[i]}條<br>{" → ".join(s)}</td><td>北極</td>'
        + '<td></td>' * 3 + '<td></td></tr>' for i, s in enumerate(COPY))
    compose = ''.join(
        f'<div class="box" style="margin-top:3mm"><h3>第 {i} 首</h3>{circuit_svg((), blank=True, w=90)}'
        '<p>爸爸預測：□ 一定是 0　□ 一定是 1　□ 一半一半</p>'
        '<p>紙球：一＿＿＿＿　二＿＿＿＿　三＿＿＿＿　結果＿＿＿　誰猜對？＿＿</p></div>'
        for i in range(1, 4))
    pages = [
        '<h2>臨摹挑戰：三條線路</h2><p class="lead">照著範例，畫在下面的方格裡：左邊寫 |0⟩、一條線、方塊一格一個、最右邊畫儀表。</p>'
        + copy_blocks,
        '<h2>箭頭追蹤表</h2><p class="lead">用手指沿著線往右走，每過一個方塊，寫下箭頭在哪：北極、南極、赤道（前）、赤道（後）。沒有那一步就畫斜線。</p>'
        '<table class="trk"><tr><th>線路</th><th>起點</th><th>第一步後</th><th>第二步後</th><th>第三步後</th><th>測量結果</th></tr>'
        + trk_rows + '</table>'
        '<div class="box" style="margin-top:6mm"><h3>順序實驗</h3><p>把第三條的順序改成 Z → H → H，箭頭怎麼走？結果一樣嗎？</p>'
        '<p>北極 →＿＿＿＿ →＿＿＿＿ →＿＿＿＿　結果：＿＿＿＿</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>核對員的問題</h3><p>為什麼同一條線上的閘不能隨便交換？</p>'
        '<div class="line"></div><div class="line"></div></div>',
        '<h2>換你作曲：三步線路</h2><p class="lead">在空方塊裡填 X、H 或 Z（可以重複），交給爸爸預測，再用紙球驗證。</p>'
        + compose,
        '<h2>最後一關：教爸爸讀線路圖</h2>'
        '<table class="sym"><tr><th>符號</th><th>意思</th></tr>'
        '<tr><td>一條橫線</td><td>一個量子位元；橫的方向是時間，由左往右</td></tr>'
        '<tr><td>左端的 |0⟩</td><td>起點：狀態零，箭頭在北極</td></tr>'
        '<tr><td>方塊（X、H、Z）</td><td>量子閘：轉動箭頭</td></tr>'
        '<tr><td>右端的儀表</td><td>測量：得到 0 或 1</td></tr>'
        '<tr><td>上下同一欄</td><td>不同線上的閘可以同時執行</td></tr></table>'
        '<div class="box" style="margin-top:6mm"><ul class="chk">'
        '<li>說出線、方塊、儀表各代表什麼</li><li>說出線路要從左邊開始讀</li>'
        '<li>挑一條線路，說出每一步箭頭在哪</li><li>指出一個限制：同一條線上的閘順序不能亂換</li>'
        '<li>說出「一定得到 1」是理想情況，真實機器會有少量錯誤</li><li>替三條線路取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q009 量子線路像樂譜 列印包', '父子科技學院 量子電腦學程 Q009｜量子線路像樂譜', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q009-circuit-score', folder='Q009_量子線路像樂譜', files=FILES,
        sheet=('03_作曲紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子線路像樂譜.pdf', pack_pages=4,
        pack_needles=('臨摹挑戰', '箭頭追蹤表', '順序實驗', '換你作曲', '最後一關'),
        authoring_dir=XINEW / 'authoring/q009', episode_dir='specials/q009-circuit-score',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'answerTable': {''.join(s): trace(s)[1] for s in ALL3}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q009/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

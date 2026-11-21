"""Q082 課堂教材：錯誤緩解 — 本機模擬器（只用 Python 標準函式庫）、零雜訊外插圖、誤差棒比較、說明卡與解答。

免帳號：本機模擬器 06_雜訊放大模擬.py 只需要 Python 3（不用安裝套件）；動畫用學程的 animations/operation.html（#circuit、#readout）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q082/classroom.py
"""
from pathlib import Path
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 玩具模型＝動畫 06_circuit.js 的雜訊模型：兩位元 Grover（12 個閘，理想一定量到 11）。
# 每閘錯誤率 p = 1% × 倍數；整條線路以 1 − (1 − p)^12 的機率變成四種結果之一（均勻隨機）；讀取翻轉預設關（動畫是 3%）。
GATES, SHOTS = 12, 1000


def p11(scale, readout=0.0):
    pg = 1 - (1 - 0.01 * scale) ** GATES
    return (1 - pg) * (1 - readout) ** 2 + pg / 4


XS = [1, 2, 3]
YS = [p11(x) for x in XS]                                  # 約 0.915、0.839、0.770
SIG = [math.sqrt(y * (1 - y) / SHOTS) for y in YS]         # 約 0.009、0.012、0.013
_mx, _my = sum(XS) / 3, sum(YS) / 3
SLOPE = sum((x - _mx) * (y - _my) for x, y in zip(XS, YS)) / sum((x - _mx) ** 2 for x in XS)
LIN0 = _my - SLOPE * _mx                                   # 直線外插 約 0.986
QUAD0 = 3 * YS[0] - 3 * YS[1] + YS[2]                      # 穿過三點的彎曲線（二次）外插 約 0.999
LIN_SIG = math.sqrt(sum(((14 - 6 * x) / 6) ** 2 * s ** 2 for x, s in zip(XS, SIG)))   # 約 0.015
QUAD_SIG = math.sqrt(9 * SIG[0] ** 2 + 9 * SIG[1] ** 2 + SIG[2] ** 2)                  # 約 0.046
RO = [p11(x, 0.03) for x in XS]
RO_QUAD0 = 3 * RO[0] - 3 * RO[1] + RO[2]                   # 約 0.940：外插只修閘的雜訊，讀取錯誤還在
assert abs(LIN0 - 0.986) < 0.002 and abs(QUAD0 - 0.999) < 0.002 and abs(RO_QUAD0 - 0.940) < 0.002
f3 = lambda v: f'{v:.3f}'  # noqa: E731

SIM = '''"""零雜訊外插的本機模擬器（父子科技學院 Q082）。只用 Python 標準函式庫：python3 06_雜訊放大模擬.py

模型和學程動畫 operation.html#circuit 的「加入雜訊」相同：
兩位元 Grover 線路共 12 個閘，理想上一定量到 11。每個閘的錯誤率 = 1% × 倍數；
只要有任何一個閘出錯（機率 1 − (1 − p)^12），這一次就變成 00、01、10、11 隨機一個。
"""
import math
import random

GATES = 12
SHOTS = 1000          # 改大一點，誤差棒就變小
READOUT = 0.0         # 進階：改成 0.03，看看外插的答案會停在哪裡
SEED = None           # 想讓每次結果一樣，就填一個整數


def run(scale, rng):
    p = 0.01 * scale
    hit = 0
    for _ in range(SHOTS):
        k = 3                                            # 理想答案 11
        if rng.random() < 1 - (1 - p) ** GATES:
            k = rng.randrange(4)
        for bit in (1, 2):
            if rng.random() < READOUT:
                k ^= bit
        hit += k == 3
    y = hit / SHOTS
    return y, math.sqrt(y * (1 - y) / SHOTS)


rng = random.Random(SEED)
xs = [1, 2, 3]
pts = [run(x, rng) for x in xs]
for x, (y, s) in zip(xs, pts):
    print(f'雜訊 {x} 倍：量到 11 的比例 = {y:.3f} ± {s:.3f}')
ys = [y for y, _ in pts]
mx, my = 2, sum(ys) / 3
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / 2
lin = my - slope * mx
quad = 3 * ys[0] - 3 * ys[1] + ys[2]
sl = math.sqrt(sum(((14 - 6 * x) / 6) ** 2 * s ** 2 for x, (_, s) in zip(xs, pts)))
sq = math.sqrt(9 * pts[0][1] ** 2 + 9 * pts[1][1] ** 2 + pts[2][1] ** 2)
print(f'直線外插到 0 倍：{lin:.3f} ± {sl:.3f}')
print(f'彎曲線（穿過三點）外插到 0 倍：{quad:.3f} ± {sq:.3f}')
y0, s0 = run(0, rng)
print(f'揭曉：把雜訊關掉（0 倍）跑出來 = {y0:.3f}')
'''

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q082：錯誤緩解（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：錯誤更正還做不到的時候，能不能從帶雜訊的結果估出比較準的答案？

需要：一台有 Python 3 的電腦（本機模擬器 `06_雜訊放大模擬.py` 不用安裝任何套件），和學程的 `animations/operation.html`（瀏覽器開啟，不需網路或帳號）。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三種錯誤緩解：讀取緩解、零雜訊外插、機率性錯誤消除 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 用模擬器把雜訊放大 1、2、3 倍，畫零雜訊外插圖 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 比較外插前後的期望值與誤差棒 | 列印包第 3 頁、`03_外插紀錄.csv` |
| 105–115 | 孩子教爸爸：錯誤緩解在解決什麼、代價在哪 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 在終端機跑一次 `python3 06_雜訊放大模擬.py`，看它印出 1、2、3 倍的結果、兩種外插和「揭曉」。
- 在 `operation.html#circuit` 選「Grover 搜尋」，按「播放」，再打開「加入雜訊」開關，看右下插圖的柱子掉到青線下面。
- 列印 `02_列印包_錯誤緩解.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 資料偵探怎麼玩

爸爸跑模擬器，只念出 1、2、3 倍的三個數字（先不要念外插和揭曉）。孩子把三個點畫在列印包第 1 頁的圖上，畫線延伸到 0 倍，寫下自己的估計。最後爸爸念「揭曉」那一行。

## 誠實說明

- 模擬器是學程動畫的簡化雜訊模型（任何閘出錯，這一次就變成隨機結果），不是真機。
- 用期望值的說法：「量到 11 的比例」就是這個線路的期望值（理想值是 1）。
- 錯誤緩解要用更多次數來換，而且不能取代錯誤更正——這是本課最重要的注意事項。
''',

'01_操作步驟.md': f'''# 操作步驟

## A. 先看雜訊（`operation.html#circuit`，約 5 分鐘）

1. 選「Grover 搜尋（2 位元，找 |11⟩）」，按「播放」，等走到最後的量測欄：右下插圖只有 11 一根柱子，頂到青色理想線。
2. 打開「加入雜訊（每閘 1%、讀取 3%）」：11 掉到青線下面，其他三個結果出現矮柱子。

## B. 放大雜訊、外插回零（本機模擬器，約 25 分鐘）

1. `python3 06_雜訊放大模擬.py`。爸爸只念三行「雜訊 N 倍」的數字。
2. 孩子在列印包第 1 頁畫三個點（橫軸＝雜訊倍數 0–3，縱軸＝量到 11 的比例 0.6–1.0）。
3. 用尺畫一條直線穿過三個點附近，延伸到 0 倍，讀出估計值；寫在「零雜訊外插圖」上。
4. 爸爸念「揭曉」那一行，比較：沒外插（1 倍）差多少？外插後差多少？
5. 再跑兩三次（每次結果會有一點不同），把每次的點都記在 `03_外插紀錄.csv`。

## C. 看讀錯怎麼發生（`operation.html#readout`，約 10 分鐘）

1. 拖「兩團雲的間距」到 0.4：IQ 點擠成一團，插圖兩座山合成一座。
2. 拉回 1.6：兩座山分開。讀取緩解就是先量出「0 讀成 1」「1 讀成 0」的比例，再反推。

## D. 下半場：誤差棒（約 30 分鐘）

1. 每個點畫上下誤差棒（模擬器印出的 ± 值，1000 次約 ±0.01）。
2. 比較模擬器印出的兩種外插：直線、穿過三點的彎曲線，哪個接近揭曉值？誰的誤差棒大？
3. 進階：把 `SHOTS` 改成 4000，誤差棒變成多少？把 `READOUT` 改成 0.03，外插答案停在哪裡？
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 期望的數字（模型的理論值；每次模擬會在誤差棒範圍內上下跳動）\n\n'
  '| 雜訊倍數 | 每閘錯誤率 | 量到 11 的比例 | 1000 次的誤差棒 |\n|---|---|---|---|\n'
  + ''.join(f'| {x} 倍 | {x}% | {f3(y)} | ±{f3(s)} |\n' for x, y, s in zip(XS, YS, SIG))
  + f'| 0 倍（理想） | 0% | 1.000 | — |\n\n'
  f'- 不做緩解（直接用 1 倍）：{f3(YS[0])}，差理想值 {f3(1 - YS[0])}。\n'
  f'- 直線外插到 0 倍：約 {f3(LIN0)} ± {f3(LIN_SIG)}（直線有偏差：真正的曲線是彎的）。\n'
  f'- 穿過三點的彎曲線外插：約 {f3(QUAD0)} ± {f3(QUAD_SIG)}（平均起來更準，但誤差棒是單點的四倍多，單跑一次常常比直線還偏）。\n'
  f'- 要把 ±{f3(QUAD_SIG)} 縮回 ±0.01，次數要多約 ({f3(QUAD_SIG)} ÷ 0.01)² ≈ {round((QUAD_SIG / 0.01) ** 2)} 倍：這就是「錯誤緩解要用更多次數換」。\n\n'
  '## 進階：讀取錯誤 3%\n\n'
  f'把 `READOUT = 0.03`：三個點約 {", ".join(f3(y) for y in RO)}，彎曲線外插約 {f3(RO_QUAD0)}，停在 0.97² ≈ 0.941，回不到 1。'
  '因為放大的只是閘的雜訊，讀取錯誤要另外用讀取緩解處理。\n\n'
  '## 常見問題\n\n'
  '- 錯誤緩解和錯誤更正差在哪？緩解是事後用統計估計期望值，不保護量子資訊；更正是用很多實體位元編碼，計算途中持續偵測並修正。\n'
  '- 為什麼不能一直用緩解？成本隨規模指數上升（機率性錯誤消除的次數隨線路大小指數增加），所以它是過渡工具。\n'
  '- 閘折疊為什麼不改變答案？接上反向閘等於什麼都沒做，再做一次原本的閘，理想結果不變，只是多了出錯的機會。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `operation.html#circuit`（3D 場景 6：量子線路）

- 上排選範例（Bell 態、GHZ 態、Grover 搜尋…）；「單步 ▶」一次一欄、「播放」自動走完、「⏮ 重設」。
- 開關「加入雜訊（每閘 1%、讀取 3%）」：任何閘出錯的機率是 1 − 0.99^閘數，出錯就變成隨機結果；每個位元再有 3% 讀錯。
- 右下插圖：量測 1000 次的直方圖，青線是理想機率。

## `operation.html#readout`（3D 場景 7：讀取與統計）

- 每個點是一次讀取在 IQ 平面上的訊號；粉紅線是閾值，右邊判 1（紅）、左邊判 0（藍）。
- 滑桿「兩團雲的間距」「積分時間 τ」「判別閾值位置」；開關「讀取期間 T₁ 衰減」「讀取誤差緩解」（緩解結果寫在左側讀數）。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',

'06_雜訊放大模擬.py': SIM,
}

SHEET_HEADER = ['回合', '1 倍', '2 倍', '3 倍', '我畫的直線估計', '直線外插（程式）', '彎曲線外插（程式）', '揭曉（0 倍）', '備註']
SHEET_ROWS = [[f'第 {i} 次', '', '', '', '', '', '', '', ''] for i in range(1, 6)] + [['SHOTS = 4000', '', '', '', '', '', '', '', ''], ['READOUT = 0.03', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}
.plot{position:relative;height:80mm;border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;margin:4mm 0 8mm 12mm;
background-image:linear-gradient(#ccd6e4 .4pt,transparent .4pt),linear-gradient(90deg,#ccd6e4 .4pt,transparent .4pt);background-size:100% 10mm,25% 100%}
.plot span{position:absolute;font-size:9pt}'''

PLOT = ('<div class="plot">' + ''.join(f'<span style="left:{25 * k}%;bottom:-6mm">{k}</span>' for k in range(4))
        + ''.join(f'<span style="left:-10mm;bottom:{10 * k - 2}mm">{0.6 + 0.05 * k:.2f}</span>' for k in range(9))
        + '</div><p class="note">橫軸：雜訊倍數（0、1、2、3）　縱軸：量到 11 的比例（期望值）</p>')


def html():
    pages = [
        '<h2>零雜訊外插圖（今天的作品）</h2><p class="lead">爸爸念出 1、2、3 倍的數字，你把三個點畫上去，畫線延伸到 0 倍。</p>'
        + PLOT +
        '<div class="card"><h3>我的推理</h3><p>1 倍＝＿＿＿　2 倍＝＿＿＿　3 倍＝＿＿＿</p>'
        '<p>外插到 0 倍，我估計＝＿＿＿　揭曉＝＿＿＿</p><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>資料偵探：找回零雜訊</h2><p class="lead">爸爸是操作員，你是資料偵探。每次模擬結果會有一點不同，多玩幾次。</p>'
        '<table class="rec"><tr><th>回合</th><th>1 倍</th><th>2 倍</th><th>3 倍</th><th>我的估計</th><th>揭曉</th><th>差多少</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 6)) + '</table>'
        '<p class="note">不做緩解（直接用 1 倍）差理想值多少？＿＿＿　外插之後差多少？＿＿＿</p>'
        '<p class="note">讀錯怎麼發生：operation.html#readout 把「兩團雲的間距」拉小，畫下你看到的兩座山：</p><div class="line"></div><div class="line"></div>',
        '<h2>換你改造：比一比誤差棒</h2><p class="lead">把模擬器印出的 ± 值畫成誤差棒，比較兩種外插。</p>'
        '<table class="rec"><tr><th></th><th>數值</th><th>誤差棒（±）</th><th>離揭曉值多遠</th></tr>'
        '<tr><td>不緩解（1 倍）</td><td></td><td></td><td></td></tr><tr><td>直線外插</td><td></td><td></td><td></td></tr>'
        '<tr><td>彎曲線外插</td><td></td><td></td><td></td></tr><tr><td>SHOTS = 4000 的彎曲線</td><td></td><td></td><td></td></tr></table>'
        '<p>彎曲線的誤差棒是單點的＿＿＿倍；要縮回 ±0.01，大約要多跑＿＿＿倍。</p>'
        '<p class="note">生活技能：用推估補足量測的不足。你還想到哪裡會「量幾個點、畫線推估」？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 錯誤緩解在解決什麼？</p><div class="line"></div>'
        '<p>2. 零雜訊外插怎麼做？</p><div class="line"></div><p>3. 讀取緩解怎麼做？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：緩解是估準期望值，不保護量子資訊</li><li>說出零雜訊外插：放大雜訊、量期望值、畫線回零</li>'
        '<li>說出閘折疊為什麼答案不變</li><li>指出一個限制：要用更多次數換，不能取代錯誤更正</li>'
        '<li>替零雜訊外插圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q082 錯誤緩解 列印包', '父子科技學院 量子電腦學程 Q082｜錯誤緩解', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q082-error-mitigation', folder='Q082_錯誤緩解', files=FILES,
        sheet=('03_外插紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_錯誤緩解.pdf', pack_pages=4,
        pack_needles=('零雜訊外插圖', '資料偵探', '誤差棒', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q082', episode_dir='specials/q082-error-mitigation',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#circuit', 'animations/operation.html#readout'],
               'toyModel': {'gates': GATES, 'shots': SHOTS, 'p11': [round(y, 4) for y in YS],
                            'linear0': round(LIN0, 4), 'quad0': round(QUAD0, 4),
                            'linearSigma': round(LIN_SIG, 4), 'quadSigma': round(QUAD_SIG, 4)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q082/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

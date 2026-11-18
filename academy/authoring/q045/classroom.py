"""Q045 課堂教材：熱負載預算表、線數計算卡、線材比較表、可執行的 heat_budget.py（照佈線場景的估算模型）、說明卡與解答。

不需要帳號、不需要安裝套件（heat_budget.py 只用 Python 標準函式庫；也可以只用計算機）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q045/classroom.py
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

# 與 animations/js/peripherals/common.js 的 PD.wiring、05_wiring.js 的 counts()/heat() 相同
STAGES = ['50 K', '4 K', 'Still（蒸餾器）', 'Cold plate（冷板）', 'MXC（混合腔）']
PASSIVE = [45e-3, 1e-3, 3e-6, 0.4e-6, 0.015e-6]   # W／每條不鏽鋼同軸
ATT = [0, 2e-6, 0, 2e-8, 2e-9]                    # W／每條輸入線（XY＋讀取輸入＋泵浦）的衰減器吸收
HEMT = 5e-3                                       # W／每條讀取輸出（4 K）
COOL = [30, 1.5, 40e-3, 200e-6, 19e-6]            # W（45 K／4.2 K／1.2 K／140 mK／20 mK）


def counts(n):
    g = math.ceil(n / 6)
    return {'xy': n, 'z': n, 'rin': g, 'rout': g, 'pump': g}


def heat(n):
    c = counts(n)
    coax = sum(c.values())
    loads = [coax * PASSIVE[i] + (c['xy'] + c['rin'] + c['pump']) * ATT[i] + (c['rout'] * HEMT if i == 1 else 0) for i in range(5)]
    return coax, loads


def fmt(w):
    return f'{w:.2f} W' if w >= 1 else f'{w * 1e3:.1f} mW' if w >= 1e-3 else f'{w * 1e6:.1f} μW'


TABLE = {n: heat(n) for n in (50, 100, 1000)}
# 與影片、fact-check.md 一致
assert TABLE[50][0] == 127 and TABLE[100][0] == 251 and TABLE[1000][0] == 2501
assert round(TABLE[50][1][3] / COOL[3] * 100) == 26 and round(TABLE[100][1][3] / COOL[3] * 100) == 52
assert round(TABLE[100][1][0] / COOL[0] * 100) == 38 and round(TABLE[1000][1][3] / COOL[3], 2) == 5.14
assert round(TABLE[1000][1][0], 2) == 112.55 and heat(200)[0] == 502 and round(heat(200)[1][3] / COOL[3] * 100) == 103
MAX_CP_SS = round(COOL[3] / PASSIVE[3])            # 500 條
MAX_CP_THIN = int(COOL[3] / (PASSIVE[3] * 0.27))   # 1851 條
assert MAX_CP_SS == 500 and MAX_CP_THIN == 1851
# power1000.html#heat（每個稀釋單元 MXC 30 μW）：每條磁通線在 MXC 的熱 = 被動＋直流
FLUX_SS = 0.025e-6 + 0.050e-6     # 不鏽鋼：0.075 μW
FLUX_NBTI = 0.020e-6              # 超導 NbTi：直流熱為 0，被動熱取輸出線值
MAX_MXC_SS, MAX_MXC_NBTI = round(30e-6 / FLUX_SS), round(30e-6 / FLUX_NBTI)
assert (MAX_MXC_SS, MAX_MXC_NBTI) == (400, 1500)

PROGRAM = '''"""父子科技學院 量子電腦學程 Q045：熱負載預算計算器（照 peripherals.html#wiring 的估算模型）

執行：python heat_budget.py          （不需要安裝任何套件）
改造：改下面的 QUBITS，或把 PASSIVE 乘上 0.27 試試「細同軸」
"""
import math

QUBITS = [50, 100, 1000]

STAGES = ['50 K', '4 K', 'Still', 'Cold plate', 'MXC']
PASSIVE = [45e-3, 1e-3, 3e-6, 0.4e-6, 0.015e-6]   # 每條不鏽鋼同軸帶下的熱（瓦）
ATT = [0, 2e-6, 0, 2e-8, 2e-9]                    # 每條輸入線的衰減器發熱（瓦）
HEMT = 5e-3                                       # 每條讀取輸出線的低溫放大器（4 K，瓦）
COOL = [30, 1.5, 40e-3, 200e-6, 19e-6]            # 每一層的冷卻能力（瓦）


def fmt(w):
    return f'{w:.2f} W' if w >= 1 else f'{w * 1e3:.1f} mW' if w >= 1e-3 else f'{w * 1e6:.1f} uW'


for n in QUBITS:
    g = math.ceil(n / 6)                 # 讀取輸入、讀取輸出、泵浦：每 6 顆一條
    xy, z, rin, rout, pump = n, n, g, g, g
    coax = xy + z + rin + rout + pump
    print(f'\\n{n} 顆量子位元 -> 同軸線 {coax} 條')
    for i, s in enumerate(STAGES):
        load = coax * PASSIVE[i] + (xy + rin + pump) * ATT[i] + (rout * HEMT if i == 1 else 0)
        pct = load / COOL[i] * 100
        flag = '  <-- 超過！' if pct > 100 else ''
        print(f'  {s:<10} {fmt(load):>10} / {fmt(COOL[i]):>9}  {pct:6.0f}%{flag}')
'''

ROWS_MD = ''.join(
    f'| {n} | {coax} | ' + ' | '.join(f'{fmt(l)}（{l / COOL[i] * 100:.0f}%）' for i, l in enumerate(loads)) + ' |\n'
    for n, (coax, loads) in TABLE.items())

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q045：低溫佈線與熱負載（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：每條從室溫進到稀釋冷凍機的線都會把熱帶下去，用「基準測試」算出 50、100、1000 顆量子位元的熱負載，看哪一層最先撐不住。

## 需要什麼

- 一台電腦和瀏覽器：打開學程 `animations/peripherals.html#wiring`（周邊系統 3D 場景 5「低溫佈線」）和 `animations/power1000.html#heat`（1,000 位元供電設計：低溫熱預算）。不需要帳號。
- 計算機；或用 Python 執行 `heat_budget.py`（不需要安裝套件）。
- 列印 `02_列印包_低溫佈線與熱負載.pdf`（A4，共 4 頁）；紅色筆（超過 100% 的格子塗紅）。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 冷凍機各層、每顆量子位元的線、輸入線與輸出線、熱的三個來源 | 影片第 3–6 段、列印包第 1 頁 |
| 25–65 | 基準測試：佈線場景讀 50、100 顆；自己算 1000 顆；填預算表 | `01_操作步驟.md`、列印包第 2 頁、`03_熱負載預算表.csv` |
| 65–75 | 休息 | |
| 75–105 | 比較線材：冷板能接幾條線；細同軸與超導磁通線 | 列印包第 3 頁、`power1000.html#heat` |
| 105–115 | 孩子教爸爸：為什麼每條線都帶熱、哪一層先吃緊、常見誤解 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 基準測試的規則

- 同一張表、同一套假設，只改量子位元數；每次都要寫出「哪一層最先超過」。
- 先預測再算：先猜哪一層會先爆，再看結果。
- 超過 100% 的格子塗紅；50% 以上塗橘（和場景插圖的顏色一樣）。

## 誠實說明

- 數字是動畫場景的「示意估算」：每條線熱負載取自 Krinner 等人 2019 年的論文，冷卻能力取自一台 Bluefors XLD 的量測值（場景程式碼註解）。真實系統依機型、線材、熱錨定而不同。
- 佈線場景把讀取線估成每 6 顆一組；簡報寫 4–8 顆。所以場景的 50 顆是 127 條，簡報的實例是 124 條，兩者都合理。
- 場景滑桿只到 200 顆；1000 顆是照同一個公式外推。
- 熱預算場景（power1000.html#heat）用的是另一套「推論」模型（加了可調耦合器、3 組稀釋單元），數字不能和佈線場景直接混著比。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：基準測試（約 40 分鐘）

1. 打開 `animations/peripherals.html#wiring`。右下角的插圖是「各級熱負載 / 可用冷卻功率」，超過 100% 會變紅。
2. 先在列印包第 2 頁寫預測：量子位元變多時，哪一層會最先超過？
3. 把滑桿「量子位元數（線束示意）」拉到 50。左邊面板會寫「同軸共 127 條」，下面列出每一層「熱負載 / 冷卻功率」。抄進預算表，算百分比。
4. 拉到 100，再抄一次。
5. 1000 顆：滑桿只到 200，用乘法自己算：
   - 同軸線條數 = 1000（驅動）＋1000（磁通）＋3 × 167（讀取輸入、輸出、泵浦，每 6 顆一條，無條件進位）＝ 2501
   - 每一層的熱 ≈ 條數 × 每條的熱（50 K 45 mW、4 K 1 mW、冷板 0.4 μW、混合腔 0.015 μW）；4 K 還要加上每條讀取輸出 5 mW 的低溫放大器
6. 想核對，就執行 `python heat_budget.py`，它照場景同一套公式印出三種規模。

## 下半場：換線材，多接幾條線（約 30 分鐘）

1. 冷板能抽走 200 μW；每條不鏽鋼同軸帶下 0.4 μW。最多能接幾條？
2. 換成細同軸（被動熱 × 0.27）：每條變多少？能接幾條？多接了幾條？
3. 打開 `animations/power1000.html#heat`（預設 1000 顆、3 組稀釋單元），看哪幾行是紅色、面板最下面「熱帳」寫什麼。
4. 勾選「改用 0.047" 細同軸」：哪些行變綠？哪一行反而更糟？
5. 再勾選「磁通線改用超導 NbTi」：「MXC 磁通直流」變多少？熱帳過關了嗎？
6. 把結果寫在列印包第 3 頁。
''',

'heat_budget.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 熱負載預算表（佈線場景模型）\n\n'
  '| 量子位元 | 同軸 | 50 K（30 W） | 4 K（1.5 W） | Still（40 mW） | 冷板（200 μW） | 混合腔（19 μW） |\n|---|---|---|---|---|---|---|\n'
  + ROWS_MD +
  '\n- 50 顆：全部在 30% 以下，冷板 26% 最高。\n- 100 顆：冷板 52%（變橘）、50 K 38%。\n'
  '- 200 顆（滑桿最右邊）：502 條，冷板 103%（變紅）、50 K 75%。\n'
  '- 1000 顆：冷板約 5 倍、50 K 約 3.75 倍、4 K 約 2.2 倍、混合腔約 2.1 倍都超過；只有 Still 還夠。\n\n'
  '## 換線材，多接幾條線\n\n'
  f'- 冷板只算被動熱：200 ÷ 0.4 = {MAX_CP_SS} 條不鏽鋼同軸。\n'
  f'- 細同軸：0.4 × 0.27 = 0.108 μW／條 → 200 ÷ 0.108 ≈ {MAX_CP_THIN} 條，多接約 {MAX_CP_THIN - MAX_CP_SS} 條。\n'
  f'- 混合腔的磁通線（熱預算場景，每組稀釋單元 30 μW）：不鏽鋼每條 0.025 μW 被動＋0.050 μW 直流 = 0.075 μW → {MAX_MXC_SS} 條；'
  f'超導 NbTi 每條 0.020 μW、直流 0 → {MAX_MXC_NBTI} 條，多接 {MAX_MXC_NBTI - MAX_MXC_SS} 條。\n\n'
  '## 熱預算場景（power1000.html#heat，1000 顆、3 組）\n\n'
  '| 設定 | 50 K | 4 K | CP | MXC 磁通直流 | MXC 合計 | 熱帳 |\n|---|---|---|---|---|---|---|\n'
  '| 預設 | 128% | 79% | 215% | 139% | 229% | 不過關 |\n'
  '| ＋細同軸 | 35% | 23% | 62% | 556% | 580% | 不過關 |\n'
  '| ＋細同軸＋超導磁通線 | 35% | 23% | 62% | 0% | 21% | 過關 |\n\n'
  '## 常見問題\n\n'
  '- 為什麼不全部用銅線？一般金屬導電好通常導熱也好，銅線會把很多熱帶下去，只用在同一層裡面。\n'
  '- 超導線為什麼是例外？鈮鈦在約 10 K 以下超導，訊號幾乎不損耗，導熱又極低；所以讀取輸出線從混合腔到 4 K 用鈮鈦同軸。\n'
  '- 衰減器不是也會發熱嗎？會，所以要熱錨定在每一層，而且放在冷卻能力夠的地方（Still 通常只做熱錨定、不放衰減器）。\n'
  '- 為什麼細的不鏽鋼線磁通直流熱反而變多？細線電阻較大，磁通線上的直流電流產生的熱跟著變大（熱預算場景用 ×4 估算）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要伺服器或帳號。

## `animations/peripherals.html#wiring`（周邊系統 3D 場景 5：低溫佈線）

- 六種線並排：XY 驅動、Z 磁通、讀取輸入、TWPA 泵浦、讀取輸出、直流線束。
- 面板按鈕「全部」「XY 驅動」…「直流線束」：只看一種線，畫面拉近，各層元件（衰減器、濾波、隔離器、TWPA、HEMT）亮起並標出數值。
- 滑桿「量子位元數（線束示意）」1–200：線束變密，面板列出各類線數與每一層「熱負載 / 冷卻功率」。
- 右下插圖：各級熱負載佔冷卻功率的百分比；> 50% 橘、> 100% 紅。

## `animations/power1000.html#heat`（1,000 位元供電設計：低溫熱預算）

- 滑桿「量子位元數 N」「稀釋單元／脈衝管數」；開關「改用 0.047" 細同軸」「磁通線改用超導 NbTi」等。
- 每一行是「負載 / 可用冷卻」，虛線是上限；面板最下面「熱帳：過關／不過關」。這一頁是推論模型，不是廠商數據。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放（peripherals.html）；左右方向鍵換場景。
''',
}

SHEET_HEADER = ['量子位元數', '同軸線條數', '50 K 熱', '50 K %', '4 K 熱', '4 K %', 'Still 熱', 'Still %', '冷板熱', '冷板 %',
                '混合腔熱', '混合腔 %', '最先超過的是哪一層', '我的預測對嗎']
SHEET_ROWS = [['50'], ['100'], ['1000'], ['（自選）']]

EXTRA_CSS = '''table.rec td{height:10mm}table.bud td{height:13mm;font-size:10pt}table.bud th{font-size:10pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.fridge td:first-child{font-weight:700;width:30mm}.small{font-size:10pt;color:#4a6a88}'''


def html():
    stg = ''.join(f'<tr><td>{s}</td><td>{fmt(c)}</td><td></td></tr>' for s, c in zip(STAGES, COOL))
    bud_head = '<tr><th>量子位元</th><th>同軸條數</th>' + ''.join(f'<th>{s.split("（")[0]}<br>熱／%</th>' for s in STAGES) + '</tr>'
    bud = ''.join(f'<tr><td>{n}</td>' + '<td></td>' * 6 + '</tr>' for n in ('50', '100', '1000', '＿＿'))
    pages = [
        '<h2>線數計算卡：每顆量子位元要幾條線</h2><p class="lead">先數線，再算熱。讀取線用「每 6 顆一條」（和佈線場景一樣）。</p>'
        '<table class="rec"><tr><th>線</th><th>數量規則</th><th>50 顆</th><th>100 顆</th><th>1000 顆</th></tr>'
        '<tr><td>XY 驅動線</td><td>每顆 1 條</td><td></td><td></td><td></td></tr>'
        '<tr><td>Z 磁通線</td><td>每顆 1 條</td><td></td><td></td><td></td></tr>'
        '<tr><td>讀取輸入線</td><td>每 6 顆 1 條（進位）</td><td></td><td></td><td></td></tr>'
        '<tr><td>讀取輸出線</td><td>每 6 顆 1 條（進位）</td><td></td><td></td><td></td></tr>'
        '<tr><td>泵浦線</td><td>每條輸出 1 條</td><td></td><td></td><td></td></tr>'
        '<tr><th colspan="2">同軸線合計</th><td></td><td></td><td></td></tr></table>'
        '<h3 style="margin-top:5mm">冷凍機各層能抽走多少熱（佈線場景的數字）</h3>'
        f'<table class="rec fridge"><tr><th>層</th><th>冷卻能力</th><th>每條不鏽鋼同軸帶下</th></tr>{stg}</table>'
        '<p class="note">右欄自己填：50 K 45 mW、4 K 1 mW、Still 3 μW、冷板 0.4 μW、混合腔 0.015 μW。</p>',
        '<h2>熱負載預算表（基準測試）</h2><p class="lead">先預測：量子位元變多時，哪一層最先超過？＿＿＿＿＿＿＿＿</p>'
        f'<table class="rec bud">{bud_head}{bud}</table>'
        '<p class="note">熱＝條數 × 每條的熱（4 K 再加每條讀取輸出 5 mW）；％＝熱 ÷ 冷卻能力 × 100。50% 以上塗橘，超過 100% 塗紅。</p>'
        '<p>最先超過的是：＿＿＿＿＿＿　　我的預測對嗎？＿＿＿＿</p><p>線數多一倍時，熱多了幾倍？＿＿＿＿</p>'
        '<p class="small">單位：1 W = 1000 mW；1 mW = 1000 μW。</p>',
        '<h2>換你改造：換線材，多接幾條線</h2><p class="lead">導電好的金屬通常導熱也好；超導線是例外。</p>'
        '<table class="rec"><tr><th>線材</th><th>每條帶到冷板的熱</th><th>冷板 200 μW 能接幾條</th><th>比不鏽鋼多幾條</th></tr>'
        '<tr><td>不鏽鋼同軸</td><td>0.4 μW</td><td></td><td>—</td></tr>'
        '<tr><td>細同軸（× 0.27）</td><td></td><td></td><td></td></tr></table>'
        '<h3 style="margin-top:5mm">混合腔的磁通線（熱預算場景：每組 30 μW）</h3>'
        '<table class="rec"><tr><th>磁通線</th><th>被動熱</th><th>直流發熱</th><th>每條合計</th><th>能接幾條</th></tr>'
        '<tr><td>不鏽鋼</td><td>0.025 μW</td><td>0.050 μW</td><td></td><td></td></tr>'
        '<tr><td>超導鈮鈦</td><td>0.020 μW</td><td>0</td><td></td><td></td></tr></table>'
        '<h3 style="margin-top:5mm">在 power1000.html#heat 驗證（1000 顆、3 組）</h3>'
        '<table class="rec"><tr><th>設定</th><th>哪幾行是紅色</th><th>熱帳</th></tr>'
        '<tr><td>預設</td><td></td><td></td></tr><tr><td>＋細同軸</td><td></td><td></td></tr>'
        '<tr><td>＋細同軸＋超導磁通線</td><td></td><td></td></tr></table>',
        '<h2>說明卡：我的熱負載預算表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 低溫佈線與熱負載在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：為什麼每多一條線，冷凍機就多一份負擔</li><li>讀出預算表：量子位元越多，哪一層最先吃緊</li>'
        '<li>說出衰減器為什麼要熱錨定</li><li>指出一個誤解：導電好通常導熱也好，佈線要在損耗和熱之間取捨</li>'
        '<li>替預算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q045 低溫佈線與熱負載 列印包', '父子科技學院 量子電腦學程 Q045｜低溫佈線與熱負載', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q045-cryo-wiring', folder='Q045_低溫佈線與熱負載', files=FILES,
        sheet=('03_熱負載預算表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_低溫佈線與熱負載.pdf', pack_pages=4,
        pack_needles=('線數計算卡', '冷凍機各層', '熱負載預算表', '換線材', '超導', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q045', episode_dir='specials/q045-cryo-wiring',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'heat_budget.py', 'model': 'animations/js/peripherals/common.js PD.wiring',
               'budget': {str(n): {'coax': c, 'coldPlatePct': round(l[3] / COOL[3] * 100)} for n, (c, l) in TABLE.items()},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q045/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

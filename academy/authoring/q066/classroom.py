"""Q066 課堂教材：旋轉鞍面滾球實驗步驟與紀錄表、q 參數探索表（atoms.html#paul）、只用 Python 內建功能的穩定界線程式 paul_trap_q.py、
保羅阱原理圖卡、影片解說卡與解答。

不需要帳號，也不需要安裝任何套件（paul_trap_q.py 只用 Python 標準函式庫；動畫用瀏覽器開啟）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q066/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理以 python 3 實跑 paul_trap_q.py（RK4，每週期 2000 步）的結果：單週期轉移矩陣的跡
TRACE = {0.10: 1.951, 0.15: 1.889, 0.20: 1.803, 0.25: 1.692, 0.30: 1.557, 0.35: 1.397, 0.40: 1.213, 0.45: 1.005,
         0.50: 0.773, 0.55: 0.517, 0.60: 0.237, 0.65: -0.067, 0.70: -0.394, 0.75: -0.744, 0.80: -1.117,
         0.85: -1.512, 0.90: -1.931, 0.95: -2.371, 1.00: -2.833}
BOUNDARY = 0.908
assert all((abs(t) < 2) == (q < BOUNDARY) for q, t in TRACE.items())
SECULAR = {(0.4, 30): 4.24, (0.4, 50): 7.07, (0.7, 30): 7.42}  # qΩ/(2√2)，MHz

PROGRAM = '''"""父子科技學院 量子電腦學程 Q066：保羅阱的穩定界線（只用 Python 內建功能，不需要安裝任何套件）

執行：python paul_trap_q.py
方程（a = 0，τ = Ωt/2）：x'' = 2q·cos(2τ)·x
做法：把方程積分一個翻轉週期（τ 從 0 到 π），算出「一週期後放大多少」；
      |跡| < 2 代表每個週期不會越推越遠（穩定），> 2 代表越來越遠（不穩定）。
"""
import math


def one_period(q, x, v, n=2000):
    """用四階 Runge-Kutta 把 (x, v) 積分一個週期 τ = 0 → π。"""
    h, t = math.pi / n, 0.0
    acc = lambda xx, tt: 2 * q * math.cos(2 * tt) * xx
    for _ in range(n):
        k1x, k1v = v, acc(x, t)
        k2x, k2v = v + h / 2 * k1v, acc(x + h / 2 * k1x, t + h / 2)
        k3x, k3v = v + h / 2 * k2v, acc(x + h / 2 * k2x, t + h / 2)
        k4x, k4v = v + h * k3v, acc(x + h * k3x, t + h)
        x += h / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        v += h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += h
    return x, v


def trace(q):
    x1, _ = one_period(q, 1.0, 0.0)
    _, v2 = one_period(q, 0.0, 1.0)
    return x1 + v2


# 改造區：想看更細的界線，把 0.05 改成 0.01（STEP = 0.01、範圍 range(85, 96)）
STEP = 0.05
print('  q     跡      結果')
for k in range(2, 21):
    q = k * STEP
    tr = trace(q)
    print(f'{q:5.2f}  {tr:+6.3f}  {"穩定" if abs(tr) < 2 else "不穩定"}')

# 二分法找界線
lo, hi = 0.5, 1.0
for _ in range(40):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if abs(trace(mid)) < 2 else (lo, mid)
print(f'穩定界線 q ≈ {lo:.3f}')

# 慢擺動頻率的近似公式（q 小時才準）
for q, f_rf in ((0.4, 30), (0.4, 50), (0.7, 30)):
    print(f'q = {q}、射頻 {f_rf} MHz → 慢擺動 ≈ qΩ/(2√2) = {q * f_rf / (2 * math.sqrt(2)):.2f} MHz')
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q066：Paul 阱——旋轉鞍形電場（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的問題：離子帶電，為什麼只靠固定電場抓不住它？
Wolfgang Paul 的答案是讓鞍形電場快速翻面（或旋轉），平均起來就像一個碗。今天用轉盤和鞍形紙板做「旋轉鞍面滾球」實驗，再到動畫裡改 q 參數找界線。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 恩紹定理（固定電場只有鞍點）、保羅的解法、q < 0.908 | 影片第 3–7 段、列印包第 3 頁 |
| 25–65 | 旋轉鞍面滾球：不轉、慢轉、快轉各三次，先預測再錄影 | `01_操作步驟.md`、列印包第 1 頁、`03_實驗紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 開 `animations/atoms.html#paul`，從 q = 0.10 起每次加 0.05，找出界線 | 列印包第 2 頁、`05_動畫導覽.md`、（選用）`paul_trap_q.py` |
| 105–115 | 孩子教爸爸：為什麼抓不住、翻面怎麼變成碗、轉速為什麼要合適 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替鞍面實驗影片命名、存檔 | |

## 課前準備（約 20 分鐘）

- 轉盤：旋轉托盤（餐桌轉盤）、舊唱盤或可手轉的蛋糕轉台都可以；轉速要能由慢到快。
- 鞍形：厚紙板或薄塑膠板，做法見 `01_操作步驟.md`；也可以用洋芋片形狀的塑膠蓋先試。
- 小球：彈珠、小鋼珠或乒乓球。家中有幼兒時，小球用完立刻收好，避免誤吞。
- 手機與腳架（或一個人專門拿手機），錄每一次實驗。
- 列印 `02_列印包_保羅阱.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。

## 誠實說明

- 保羅在 1989 年諾貝爾演講裡展示的是精密加工的鞍形圓盤加小鋼珠，每秒轉幾圈就能留住鋼珠。家用紙板的形狀、摩擦和轉盤晃動都不理想，
  **不保證一定留得住**；留不住也是一個好的觀察結果，請孩子記錄「撐了幾秒」和「從哪個方向滾走」。
- 電場的保羅阱是鞍形「翻面」（每半個週期上下顛倒），紙板實驗是鞍形「旋轉」；兩者都讓每個方向輪流變成谷和坡，原理相同。
- 動畫的 q 在大約 0.75–0.90 時，標籤寫「穩定」，但左邊小球的擺幅會超出鞍面而重新開始；這是動畫畫面範圍的限制。判斷穩定與否以**下方標籤和右下軌跡圖**為準。
- 動畫的「RF 頻率」滑桿只改讀數裡的頻率數字（q 固定），不會改變小球的運動。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：旋轉鞍面滾球（約 40 分鐘）

### 做鞍形（約 10 分鐘）

1. 剪一塊約 25 公分見方的厚紙板（或薄塑膠板）。
2. 把一組對角往上彎、另一組對角往下彎，做成像馬鞍或洋芋片的形狀；用膠帶在背面貼兩根竹筷固定彎度。
3. 把鞍形中心用雙面膠或黏土固定在轉盤正中央。放一顆球在中心，不轉時它應該會往下彎的那兩個角滾走。

### 實驗（約 30 分鐘）

1. 分工：爸爸是轉盤師（控制轉速、錄影），孩子是記錄員（放球、數秒數、填表）。
2. 每一次先在列印包第 1 頁寫預測：會留住還是滾掉？
3. 依序做「不轉」「慢轉」「快轉」，各三次。球輕輕放在正中心，數它撐了幾秒、從哪個方向滾走。
4. 每次都錄影，檔名寫進紀錄表（例如 `鞍面_慢轉_2.mp4`）。
5. 挑出最好的一段（留得最久的），配上孩子的解說，就是今天的作品「鞍面實驗影片」。

安全：轉速由慢到快；先清空轉盤旁邊的桌面，球可能會飛出去；眼睛不要貼近轉盤。

## 下半場：在動畫裡找界線（約 30 分鐘）

1. 用瀏覽器開 `animations/atoms.html#paul`（場景 2「Paul 阱原理」）。
2. 左邊面板「q 參數」滑桿，從 0.10 開始，每次加 0.05（可以用鍵盤方向鍵微調）。
3. 每一格記錄：鞍面下方的青色標籤（「穩定：被困住」或「不穩定：逃逸」）、右下軌跡圖的樣子、面板讀數裡的 secular 頻率。
4. 找到從穩定變成不穩定的那一格，和理論的 0.908 比一比。
5. 加碼：按「RF 開 / 關」把射頻關掉，看鞍面和標籤怎麼變；再打開。
6. （選用）在電腦上執行 `python paul_trap_q.py`，比較程式算出的界線和你找到的界線。
''',

'paul_trap_q.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## paul_trap_q.py 的輸出（製作代理實跑）\n\n| q | 跡 | 結果 |\n|---|---|---|\n'
  + ''.join(f'| {q:.2f} | {t:+.3f} | {"穩定" if abs(t) < 2 else "不穩定"} |\n' for q, t in TRACE.items())
  + f'\n穩定界線 q ≈ {BOUNDARY}。動畫裡 0.90 是「穩定」、0.95 是「不穩定」。\n\n'
  + '## 慢擺動頻率 qΩ/(2√2)\n\n| q | 射頻 | 慢擺動 |\n|---|---|---|\n'
  + ''.join(f'| {q} | {f} MHz | ≈ {v} MHz |\n' for (q, f), v in SECULAR.items())
  + '\n## 常見問題\n\n'
  '- 為什麼固定電場抓不住？恩紹定理（Earnshaw，1842）：自由空間裡的靜電位勢沒有極小值，只有鞍點；總有一個方向是下坡。\n'
  '- 翻面為什麼能抓住？離子剛要從下坡滑出去，那個方向就翻成谷把它推回；時間平均是一個指向中心的擬位勢（碗）。\n'
  '- q 跟什麼有關？q ∝ V／(mΩ²)：射頻電壓越大 q 越大；離子越重、頻率越高 q 越小（頻率是平方）。\n'
  '- 紙板實驗為什麼轉太慢會滾走？轉速越慢相當於 q 越大，超過界線就不穩定；轉速要落在合適範圍。\n'
  '- 動畫 q = 0.80 標籤寫穩定，小球卻好像跑掉？擺幅超出動畫的鞍面範圍會重新開始；以標籤和軌跡圖為準（0.80 的曲線擺得很大，尖端會超出圖框，但一直來回擺，不會像 0.95 那樣越擺越大）。\n'
  '- 常見誤解：「多放幾片電極、配好固定電壓就能抓住」——只用靜電場一定做不到。\n',

'05_動畫導覽.md': '''# 動畫導覽：atoms.html#paul（離子阱與中性原子 場景 2「Paul 阱原理」）

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

- 左邊：「旋轉鞍形位勢 φ ∝ (x² − y²) cos Ωt」——藍色鞍面不停翻面，黃色小球拖著軌跡；下方青色標籤顯示「穩定：被困住」或「不穩定：逃逸」。
- 右邊：「線性 Paul 阱」——四根桿（標籤「RF 桿（對角一組）」「接地桿」）、兩端藍色圓環「端蓋 DC（軸向囚禁）」、中間五顆「離子鏈」。
- 右下小圖「x(τ)：secular 大振盪 + micromotion 小抖動」：穩定時標「慢：secular」「快：micromotion」；不穩定時曲線衝出圖框。
- 左邊面板：「q 參數」滑桿（0.1–1.0）、「RF 開 / 關」、「RF 頻率 Ω/2π (MHz)」滑桿（10–60，只改讀數）、「重設離子位置」；讀數框顯示 q、穩定與否、secular 與 micromotion 頻率。
- 操作：`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；空白鍵暫停；左右方向鍵換場景（下一堂會用場景 1「離子阱系統全景」）。
''',
}

SHEET_HEADER = ['實驗', '轉速', '第幾次', '預測（留住／滾掉）', '撐了幾秒', '從哪個方向滾走', '影片檔名', '和預測一樣嗎']
SHEET_ROWS = ([[f'鞍面滾球', s, str(i)] for s in ('不轉', '慢轉', '快轉') for i in (1, 2, 3)]
              + [['動畫 q 參數', f'q = {q:.2f}', ''] for q in TRACE]
              + [['動畫 RF 關', 'q = 0.40', '']])

EXTRA_CSS = '''table.rec td{height:9.5mm}table.qt td{height:7.6mm;padding:.6mm 2.5mm}table.qt{font-size:11pt}
.chk li{margin:2.4mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}.cards .box{min-height:44mm}
.draw{border:1pt dashed #7f9bb3;border-radius:3mm;height:52mm;margin-top:3mm;position:relative}
.draw span{position:absolute;left:3mm;top:2mm;font-size:10pt;color:#4a6a88}'''


def html():
    rows1 = ''.join(f'<tr><td>{s}</td><td>{i}</td><td>留住／滾掉</td><td></td><td></td><td></td></tr>'
                    for s in ('不轉', '慢轉', '快轉') for i in (1, 2, 3))
    rows2 = ''.join(f'<tr><td>{q:.2f}</td><td>穩定／逃逸</td><td></td><td></td></tr>' for q in TRACE)
    pages = [
        '<h2>鞍面實驗紀錄：旋轉鞍面滾球</h2><p class="lead">爸爸是轉盤師（控制轉速、錄影），你是記錄員（放球、數秒數、填表）。每一次都先預測，再錄影。</p>'
        '<table class="rec"><tr><th>轉速</th><th>第幾次</th><th>預測</th><th>撐了幾秒</th><th>從哪個方向滾走</th><th>影片檔名</th></tr>'
        + rows1 + '</table>'
        '<div class="box" style="margin-top:4mm"><p>我發現：不轉的時候，球往＿＿＿＿＿＿滾；轉起來以後，＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>撐最久的是＿＿＿＿＿＿，我猜原因是＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<p class="note">安全：轉速由慢到快；清空轉盤旁邊的桌面；眼睛不要貼近轉盤。家用紙板不保證留得住，留不住也要記錄。</p>',
        '<h2>換你改造：q 參數探索表</h2><p class="lead">開 animations/atoms.html#paul，「q 參數」從 0.10 起每次加 0.05。看鞍面下方的標籤和右下軌跡圖。</p>'
        '<table class="rec qt"><tr><th>q</th><th>標籤</th><th>軌跡圖的樣子</th><th>secular 頻率（MHz）</th></tr>' + rows2 + '</table>'
        '<p style="margin-top:3mm">界線在 q＝＿＿＿＿ 和 ＿＿＿＿ 之間；理論值 0.908。關掉射頻時：＿＿＿＿＿＿＿＿</p>',
        '<h2>保羅阱原理圖卡</h2><p class="lead">把影片學到的寫成四張小卡，再畫一張圖。</p>'
        '<div class="cards"><div class="box"><h3>1. 恩紹定理</h3><p>只靠固定電場，空間裡沒有＿＿＿＿＿＿；最好的情況是＿＿＿＿＿＿。</p></div>'
        '<div class="box"><h3>2. 保羅的解法</h3><p>電極加＿＿＿＿電壓，鞍形每＿＿＿＿＿翻一次；離子來不及滑走，平均起來像一個＿＿＿＿。</p></div>'
        '<div class="box"><h3>3. 翻轉參數 q</h3><p>q ∝ V／(mΩ²)。電壓變大，q＿＿＿；離子變重，q＿＿＿；頻率變快，q＿＿＿。a = 0 時 q &lt; ＿＿＿＿ 才穩定。</p></div>'
        '<div class="box"><h3>4. 兩種運動</h3><p>大而慢的＿＿＿＿＿，加上跟著射頻的小而快的＿＿＿＿＿。q = 0.4、射頻 30 MHz：慢擺動 ≈ ＿＿＿＿ MHz。</p></div></div>'
        '<div class="draw"><span>畫畫看：一個鞍形（標出谷和坡），以及翻面以後的樣子</span></div>',
        '<h2>影片解說卡：我的鞍面實驗</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 這個實驗在模仿什麼？</p><div class="line"></div><p>2. 為什麼不轉時球會滾走？轉起來為什麼可能留住？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：為什麼固定電場抓不住離子（恩紹定理）</li><li>說出保羅阱怎麼讓鞍形變成一個碗</li>'
        '<li>解釋實驗：轉速要合適，小球才留得住</li><li>指出一個誤解：多放電極、配好固定電壓也抓不住，只用靜電場一定做不到</li>'
        '<li>替鞍面實驗影片取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q066 保羅阱 列印包', '父子科技學院 量子電腦學程 Q066｜Paul 阱：旋轉鞍形電場', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q066-paul-trap', folder='Q066_Paul阱_旋轉鞍形電場', files=FILES,
        sheet=('03_實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_保羅阱.pdf', pack_pages=4,
        pack_needles=('鞍面實驗紀錄', 'q 參數探索表', '保羅阱原理圖卡', '影片解說卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q066', episode_dir='specials/q066-paul-trap',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（paul_trap_q.py 只用 Python 標準函式庫）',
               'program': 'paul_trap_q.py', 'animation': 'animations/atoms.html#paul',
               'stabilityBoundary': BOUNDARY, 'traceTable': {f'{q:.2f}': t for q, t in TRACE.items()},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q066/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

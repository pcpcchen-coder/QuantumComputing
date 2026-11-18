"""Q051 課堂教材：虛構後端「犀牛六號」資料表（早上、下午兩份快照）、耦合圖、偵探線索卡、貝爾態搭檔計算表、
後端體檢報告、說明卡、解答，以及可執行的 backend_detective.py。

不需要帳號、不需要安裝套件（backend_detective.py 只用 Python 標準函式庫；也可以只用計算機）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q051/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# ---- 虛構後端「犀牛六號」（教學用，數字落在 slides/QC_Operation_Talk.pptx 第 15 頁的典型範圍附近；不代表任何真實機器）----
# 六顆排成兩排：Q0 Q1 Q2 / Q3 Q4 Q5，上下左右相鄰才相連
BACKEND = {  # 位元: (T1 μs, T2 μs, 單位元閘錯誤 %, 讀取錯誤 %)
    0: (95, 120, 0.04, 1.2),
    1: (130, 170, 0.03, 0.9),
    2: (210, 160, 0.03, 4.8),   # 壽命最好，讀取最差
    3: (40, 35, 0.12, 2.1),     # 壽命最短、單位元閘最差
    4: (115, 150, 0.03, 0.8),
    5: (80, 190, 0.05, 1.5),    # 怪數字：T2 > 2 T1
}
EDGES = {(0, 1): 0.62, (1, 2): 0.48, (3, 4): 1.40, (4, 5): 0.75, (0, 3): 0.90, (1, 4): 0.41, (2, 5): 0.55}  # 雙位元閘錯誤 %
AFTERNOON = {4: (115, 150, 0.03, 3.6)}  # 下午重新校準：四號讀取變差（漂移）


def bell_score(q, e, a, b):
    """控制位元 a 做哈達瑪閘、受控反閘、兩顆一起讀取：每一步做對的機率相乘（粗估）。"""
    return (1 - q[a][2] / 100) * (1 - e / 100) * (1 - q[a][3] / 100) * (1 - q[b][3] / 100)


def ranking(q):
    return sorted(((max(bell_score(q, e, a, b), bell_score(q, e, b, a)), a, b) for (a, b), e in EDGES.items()), reverse=True)


AM = ranking(BACKEND)
PM = ranking({**BACKEND, **AFTERNOON})
assert (AM[0][1], AM[0][2]) == (1, 4) and round(AM[0][0], 3) == 0.979
assert round(bell_score(BACKEND, EDGES[(1, 2)], 1, 2), 3) == 0.939
assert (PM[0][1], PM[0][2]) == (0, 1)
assert [k for k, v in BACKEND.items() if v[1] > 2 * v[0]] == [5]

PROGRAM = '''"""父子科技學院 量子電腦學程 Q051：看懂後端校準資料——資料偵探（只用 Python 標準函式庫）

執行：python backend_detective.py
犀牛六號是虛構的教學資料（標示虛構），數字落在真實超導量子電腦的典型範圍附近，不代表任何真實機器。
"""
# 位元: (能量弛豫時間 T1 μs, 相干時間 T2 μs, 單位元閘錯誤 %, 讀取錯誤 %)
MORNING = {
    0: (95, 120, 0.04, 1.2),
    1: (130, 170, 0.03, 0.9),
    2: (210, 160, 0.03, 4.8),
    3: (40, 35, 0.12, 2.1),
    4: (115, 150, 0.03, 0.8),
    5: (80, 190, 0.05, 1.5),
}
AFTERNOON = dict(MORNING)
AFTERNOON[4] = (115, 150, 0.03, 3.6)     # 下午重新校準後的四號

# 耦合圖：六顆排成兩排 Q0 Q1 Q2 / Q3 Q4 Q5；只有這些連線能直接做雙位元閘（數字是雙位元閘錯誤 %）
EDGES = {(0, 1): 0.62, (1, 2): 0.48, (3, 4): 1.40, (4, 5): 0.75, (0, 3): 0.90, (1, 4): 0.41, (2, 5): 0.55}


def bell(q, e, a, b):
    """控制位元 a：哈達瑪閘、受控反閘、兩顆一起讀取，每一步做對的機率相乘（粗估，忽略其他雜訊）。"""
    return (1 - q[a][2] / 100) * (1 - e / 100) * (1 - q[a][3] / 100) * (1 - q[b][3] / 100)


def report(name, q):
    print(f'=== {name} ===')
    for k, (t1, t2, g1, ro) in q.items():
        flag = '  ← 怪數字：T2 > 2 T1' if t2 > 2 * t1 else ''
        print(f'Q{k}: T1 {t1:>3} μs  T2 {t2:>3} μs  單位元閘 {g1:.2f}%  讀取 {ro:.1f}%{flag}')
    rank = sorted(((max(bell(q, e, a, b), bell(q, e, b, a)), a, b, e) for (a, b), e in EDGES.items()), reverse=True)
    print('跑貝爾態的搭檔排名（粗估成功率）：')
    for p, a, b, e in rank:
        print(f'  Q{a}–Q{b}  雙位元閘 {e:.2f}%  → {p:.1%}')
    print()


report('早上的快照', MORNING)
report('下午的快照', AFTERNOON)
# 改造區：把某顆的讀取錯誤改大或改小，看看最佳搭檔會不會換人
'''

ROWS_AM = ''.join(f'<tr><td>Q{k}</td><td>{t1}</td><td>{t2}</td><td>{g1:.2f}</td><td>{ro:.1f}</td></tr>'
                  for k, (t1, t2, g1, ro) in BACKEND.items())
ROWS_EDGE = ''.join(f'<tr><td>Q{a}–Q{b}</td><td>{e:.2f}</td><td></td></tr>' for (a, b), e in EDGES.items())
TABLE_MD = ('| 位元 | T₁ 能量弛豫時間（μs） | T₂ 相干時間（μs） | 單位元閘錯誤（%） | 讀取錯誤（%） |\n|---|---|---|---|---|\n'
            + ''.join(f'| Q{k} | {t1} | {t2} | {g1:.2f} | {ro:.1f} |\n' for k, (t1, t2, g1, ro) in BACKEND.items())
            + '\n| 連線 | 雙位元閘錯誤（%） |\n|---|---|\n' + ''.join(f'| Q{a}–Q{b} | {e:.2f} |\n' for (a, b), e in EDGES.items()))

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q051：看懂後端校準資料（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶孩子從「校準工程師」換到「使用者」：送程式到量子電腦之前，先讀懂後端的校準資料表。今天的好玩機制是資料偵探：孩子當偵探圈線索，爸爸當證人兼法官，每個結論都追問「證據在哪一格」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 認識兩種壽命、三種錯誤率、耦合圖；偵探三招 | 列印包第 1 頁、`05_動畫導覽.md` |
| 25–65 | 在犀牛六號資料表上圈線索，挑出跑貝爾態的兩顆，填搭檔計算表 | 列印包第 1、2 頁、計算機或 `backend_detective.py` |
| 65–75 | 休息 | |
| 75–105 | 寫後端體檢報告：最弱三處、比較早上與下午兩份快照、建議 | 列印包第 3 頁、`02_下午快照.md` |
| 105–115 | 孩子教爸爸：怎麼讀表、為什麼挑那兩顆 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_看懂後端校準資料.pdf`（A4，共 4 頁）；準備三種顏色的筆（好數字、弱點、怪數字）。
- 先不要給孩子看 `02_下午快照.md`，下半場再拿出來。
- 讀一遍 `04_解答.md`。

## 證人兼法官的原則

- 孩子每說一個結論（「Q2 不好」「Q1–Q4 最好」），就問：證據在表上哪一格？說得出格子和數字才算數。
- 不直接給答案；挑錯了，就請孩子把乘法算一次，讓數字自己說話。
- 最後一定要問：「這張表是什麼時候量的？等你的程式真的跑起來，數字還一樣嗎？」

## 誠實說明

- 犀牛六號是虛構的教學資料，教材每一頁都標示虛構；數字參考學程簡報（如何操作量子電腦 第 15 頁）的典型範圍，Q2 的讀取錯誤 4.8% 刻意設得比典型上限高，當成線索。
- 「每一步做對的機率相乘」是粗估，忽略閒置時的衰減、串擾等，只用來比較誰比較好。
- 真實雲端平台的欄位名稱、更新頻率各不相同。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：資料偵探（約 40 分鐘）

1. 看列印包第 1 頁的犀牛六號資料表和耦合圖。用三種顏色圈：好數字（綠）、弱點（紅）、怪數字（打問號）。
2. 偵探三招：
   - 看單顆：壽命夠不夠、單位元閘準不準、讀取清不清楚。
   - 看連線：只有耦合圖上相連的兩顆能直接做受控反閘；看那條連線的雙位元閘錯誤。
   - 抓怪數字：T₂ 不會超過 2 × T₁。哪一顆違反了？
3. 在列印包第 2 頁的搭檔計算表，把七條連線逐一算：
   成功率 ≈ (1 − 控制位元單位元閘錯誤) × (1 − 雙位元閘錯誤) × (1 − 兩顆的讀取錯誤各一次)
   例如 0.41% 要寫成 0.0041。
4. 排出前三名，說出第一名勝在哪裡。可以用 `python backend_detective.py` 對答案。

## 下半場：後端體檢報告（約 30 分鐘）

1. 在列印包第 3 頁寫下最弱的三個地方，每一個都附上「哪一格、什麼數字」。
2. 爸爸拿出 `02_下午快照.md`：同一台機器下午重新校準的結果。比一比哪個數字變了，重新算一次，最佳搭檔有沒有換人？
3. 寫下建議：跑重要的程式時，挑哪幾顆、避開哪幾顆，為什麼。

## 想多看一點（選做）

用瀏覽器開學程動畫（見 `05_動畫導覽.md`）：校準的數字從哪裡來、讀取錯誤怎麼產生、編譯器怎麼依校準資料挑位元。
''',

'02_下午快照.md': '# 犀牛六號 下午的快照（虛構）\n\n同一台機器下午重新校準。只有一顆的一個數字變了，其他都和早上一樣：\n\n'
  '| 位元 | T₁（μs） | T₂（μs） | 單位元閘錯誤（%） | 讀取錯誤（%） |\n|---|---|---|---|---|\n'
  '| Q4 | 115 | 150 | 0.03 | **3.6**（早上 0.8） |\n\n'
  '問題：最佳搭檔還是 Q1–Q4 嗎？重新算一次再回答。\n',

'03_犀牛六號資料表.md': '# 犀牛六號 早上的快照（虛構，教學用）\n\n六顆量子位元排成兩排：Q0 Q1 Q2（上排）／Q3 Q4 Q5（下排），上下左右相鄰才相連。\n\n' + TABLE_MD,

'backend_detective.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 線索\n\n'
  '- 好數字：Q1、Q4 壽命長、單位元閘 0.03%、讀取都不到 1%；連線 Q1–Q4 雙位元閘 0.41% 全場最低。\n'
  '- 陷阱：Q2 的 T₁ 210 μs 全場最好，但讀取錯誤 4.8% 全場最差。\n'
  '- 怪數字：Q5 的 T₂ 190 μs > 2 × T₁（160 μs），物理上說不通（T₂ ≤ 2T₁），可能量錯或抄錯，要標出來。\n\n'
  '## 早上：跑貝爾態的搭檔排名（每一步做對的機率相乘）\n\n| 名次 | 搭檔 | 粗估成功率 |\n|---|---|---|\n'
  + ''.join(f'| {i} | Q{a}–Q{b} | {p:.1%} |\n' for i, (p, a, b) in enumerate(AM, 1))
  + '\n算法例：Q1–Q4 = (1 − 0.0003) × (1 − 0.0041) × (1 − 0.009) × (1 − 0.008) ≈ 0.979。\n'
  'Q1–Q2 = (1 − 0.0003) × (1 − 0.0048) × (1 − 0.009) × (1 − 0.048) ≈ 0.939：讀取拖後腿。\n\n'
  '## 最弱的三個地方（參考）\n\n'
  '1. Q3：T₁ 40 μs、T₂ 35 μs 全場最短，單位元閘 0.12% 全場最高。\n'
  '2. 連線 Q3–Q4：雙位元閘錯誤 1.40%，全場最高（超出典型上限 1%）。\n'
  '3. Q2 的讀取錯誤 4.8%（超出典型上限 3%）。\n'
  '也可以接受：Q5 的資料不可信（T₂ > 2T₁），要請平台重量。\n\n'
  '## 下午快照（Q4 讀取 0.8% → 3.6%）\n\n| 名次 | 搭檔 | 粗估成功率 |\n|---|---|---|\n'
  + ''.join(f'| {i} | Q{a}–Q{b} | {p:.1%} |\n' for i, (p, a, b) in enumerate(PM[:3], 1))
  + '\n最佳搭檔換成 Q0–Q1。教訓：校準資料是某個時間點的快照，參數會漂移；送出工作前要看最新的一份。\n\n'
  '## 常見誤解\n\n'
  '- 「只看 T₁ 最大的那顆」：短線路（例如貝爾態）裡，雙位元閘和讀取錯誤影響更大。\n'
  '- 「隨便挑兩顆好位元」：不相連的兩顆不能直接做受控反閘。\n'
  '- 「表上的數字永遠準」：那是上一次校準的快照，跑的時候可能已經變了。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/peripherals.html#bringup`（周邊系統場景 10：啟動與校準）

- 「◀ 上一步」「下一步 ▶」：第 7 步 T₁ 量測、第 8 步讀取最佳化、第 10 步隨機基準測試、第 11 步上線——表上的數字就是這些步驟量出來、寫進資料庫的。

## `animations/index.html#iq`（JJ 與微波讀取 場景 10：IQ 判別）

- 「量子極限放大器（JPA/TWPA）開啟」開關：關掉後兩團點散開、讀取保真度下降。
- 「T1」滑桿拉小：準備成 1 的紅點在讀取途中掉回 0，落到藍點那一側。

## `animations/transmon-3d.html#stack`（Transmon 3D 第 12 章：編譯與控制軟體堆疊）

- 取消「自動接續」，點步驟 3「映射」：晶片標籤是今天的單位元錯誤率，編譯器挑相鄰、錯誤率低的兩顆（變金色）。
- 步驟 9 自由實驗：換電路（Bell、GHZ、BV）與晶片（直線、方格）比較。

## 操作

滑鼠拖曳旋轉、滾輪縮放；peripherals 與 index 頁可用左右方向鍵切換場景、`H` 隱藏面板。
''',
}

SHEET_HEADER = ['搭檔', '連線雙位元閘錯誤（%）', '控制位元單位元閘錯誤（%）', '讀取錯誤 A（%）', '讀取錯誤 B（%）', '粗估成功率（我算的）', '名次']
SHEET_ROWS = [[f'Q{a}–Q{b}', f'{e:.2f}', f'{BACKEND[a][2]:.2f}', f'{BACKEND[a][3]:.1f}', f'{BACKEND[b][3]:.1f}', '', '']
              for (a, b), e in EDGES.items()]

EXTRA_CSS = '''.tag{display:inline-block;background:#fde9a8;border:1pt solid #c9a227;border-radius:2mm;padding:.5mm 2.5mm;font-size:10pt;font-weight:700}
table.dt td,table.dt th{text-align:center;font-size:11.5pt}table.calc td{height:11mm}
.map{display:grid;grid-template-columns:repeat(5,auto);justify-content:center;align-items:center;gap:1mm 2mm;margin:3mm 0;font-weight:700}
.q{border:1.4pt solid #0b2540;border-radius:50%;width:15mm;height:15mm;display:flex;align-items:center;justify-content:center;font-size:12pt}
.h{width:20mm;white-space:nowrap;text-align:center;font-size:9.5pt;color:#35506b}.v{height:9mm;text-align:center;font-size:9.5pt;color:#35506b}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def coupling_map():
    e = EDGES
    q = lambda k: f'<div class="q">Q{k}</div>'  # noqa: E731
    h = lambda a, b: f'<div class="h">—{e[(a, b)]:.2f}%—</div>'  # noqa: E731
    v = lambda a, b: f'<div class="v">｜{e[(a, b)]:.2f}%</div>'  # noqa: E731
    blank = '<div></div>'
    return ('<div class="map">' + q(0) + h(0, 1) + q(1) + h(1, 2) + q(2)
            + v(0, 3) + blank + v(1, 4) + blank + v(2, 5)
            + q(3) + h(3, 4) + q(4) + h(4, 5) + q(5) + '</div>')


def html():
    calc = ''.join(f'<tr><td>Q{a}–Q{b}</td><td>{e:.2f}</td><td></td><td></td></tr>' for (a, b), e in EDGES.items())
    pages = [
        '<h2>犀牛六號 校準資料表 <span class="tag">虛構・教學用</span></h2>'
        '<p class="lead">早上的快照。用三種顏色圈：好數字、弱點、怪數字（打問號）。</p>'
        '<table class="dt"><tr><th>位元</th><th>T₁ 能量弛豫時間<br>（μs）</th><th>T₂ 相干時間<br>（μs）</th><th>單位元閘錯誤<br>（%）</th><th>讀取錯誤<br>（%）</th></tr>'
        f'{ROWS_AM}</table>'
        '<h3 style="margin-top:5mm">耦合圖（連線上的數字＝雙位元閘錯誤）</h3>' + coupling_map()
        + '<div class="box"><p><b>偵探三招</b>　① 看單顆：壽命、閘、讀取　② 看連線：相連＋雙位元閘錯誤　③ 抓怪數字：T₂ 不會超過 2 × T₁</p>'
        '<p class="note">典型範圍（學程簡報）：T₁、T₂ 數十～數百 μs；單位元閘 0.02%～0.1%；雙位元閘 0.1%～1%；讀取 0.5%～3%。</p></div>',
        '<h2>貝爾態搭檔計算表</h2><p class="lead">貝爾態＝控制位元做哈達瑪閘 → 受控反閘 → 兩顆一起讀取。把每一步做對的機率乘起來。</p>'
        '<div class="box"><p>成功率 ≈ (1 − 控制位元單位元閘錯誤) × (1 − 雙位元閘錯誤) × (1 − 讀取錯誤 A) × (1 − 讀取錯誤 B)</p>'
        '<p class="note">例：0.41% 寫成 0.0041。只有耦合圖上相連的兩顆才能配對。</p></div>'
        '<table class="calc" style="margin-top:4mm"><tr><th>搭檔</th><th>雙位元閘錯誤（%）</th><th>我的算式與結果</th><th>名次</th></tr>'
        f'{calc}</table>'
        '<p style="margin-top:4mm">我選的搭檔：＿＿＿＿＿＿　證據（哪幾格）：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>後端體檢報告</h2><p class="lead">機器：犀牛六號（虛構）　體檢醫師：＿＿＿＿＿　日期：＿＿＿＿＿</p><div class="box">'
        '<p><b>強項</b>（附證據）</p><div class="line"></div>'
        '<p><b>最弱的三個地方</b>（每一處寫出哪一格、什麼數字）</p>'
        '<p>1.</p><div class="line"></div><p>2.</p><div class="line"></div><p>3.</p><div class="line"></div>'
        '<p><b>怪數字</b>：哪一顆？為什麼說不通？</p><div class="line"></div>'
        '<p><b>下午的快照</b>：哪個數字變了？最佳搭檔有沒有換人？</p><div class="line"></div>'
        '<p><b>建議</b>：跑重要的程式時挑哪幾顆、避開哪幾顆</p><div class="line"></div></div>',
        '<h2>說明卡：我是資料偵探</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 看懂後端校準資料在解決什麼？</p><div class="line"></div><p>2. 我怎麼挑出跑貝爾態的兩顆？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中哪件事也要「用數據做選擇」？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出兩種壽命、三種錯誤率各代表什麼</li><li>說出挑搭檔的三個條件：相連、雙位元閘準、讀取清楚</li>'
        '<li>指出一個怪數字，說出為什麼說不通</li><li>指出限制：校準資料是某個時間點的快照，跑的時候可能已經變了</li>'
        '<li>替體檢報告取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q051 看懂後端校準資料 列印包', '父子科技學院 量子電腦學程 Q051｜看懂後端校準資料', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q051-backend-calibration', folder='Q051_看懂後端校準資料', files=FILES,
        sheet=('03_貝爾態搭檔計算表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_看懂後端校準資料.pdf', pack_pages=4,
        pack_needles=('犀牛六號', '貝爾態搭檔計算表', '後端體檢報告', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q051', episode_dir='specials/q051-backend-calibration',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'backend_detective.py', 'fictionalBackend': '犀牛六號（虛構，標示清楚）',
               'bestPairMorning': f'Q{AM[0][1]}–Q{AM[0][2]} {AM[0][0]:.3f}', 'bestPairAfternoon': f'Q{PM[0][1]}–Q{PM[0][2]} {PM[0][0]:.3f}',
               'rangesFrom': 'slides/QC_Operation_Talk.pptx p15', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q051/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

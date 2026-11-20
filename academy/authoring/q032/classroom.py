"""Q032 課堂教材：transmon 參數卡、三個數字的取捨單、讀取腔改造單、說明卡（列印）、解答、transmon_card.py（參數設計器）、動畫導覽。

不需要帳號，也不需要安裝套件（transmon_card.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#potential 與 transmon-3d.html#capacitor。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q032/classroom.py
"""
from pathlib import Path
import contextlib
import io
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = '''"""父子科技學院 量子電腦學程 Q032：transmon 參數設計器（只要 Python 3，不用安裝套件）。

執行：  python transmon_card.py
用電荷基底哈密頓量 H = 4E_C(n − n_g)² − (E_J/2)(|n⟩⟨n+1| + h.c.) 求能階（和動畫 index.html#potential、
transmon-3d.html 第 1 章電容分頁同一條公式）。能量都用「除以 h 之後的頻率」，單位 GHz。
想設計自己的卡：改最下面 MY_EJ、MY_EC、MY_FR 三個數字再執行。
"""
import math

EC_PER_FF = 19.37     # E_C/h [GHz] = e²/(2hC) = 19.37 / C[fF]（transmon-3d.html 第 359 行）
EJ_PER_NA = 0.4966    # E_J/h [GHz] = Φ₀I_c/(2πh) ≈ 0.4966 × I_c[nA]


def levels(ej, ec, ng=0.0, k=4, n=25):
    """最低 k 個能階（Sturm 序列二分法，三對角矩陣）。"""
    d = [4 * ec * (m - ng) ** 2 for m in range(-n, n + 1)]
    e2 = (ej / 2) ** 2

    def count(x):
        q = d[0] - x
        c = 1 if q < 0 else 0
        for di in d[1:]:
            q = di - x - e2 / (q if q != 0 else 1e-300)
            if q < 0:
                c += 1
        return c
    out = []
    for j in range(k):
        lo, hi = -ej - 1, 4 * ec * (n + 1) ** 2 + ej + 1
        for _ in range(90):
            mid = (lo + hi) / 2
            if count(mid) > j:
                hi = mid
            else:
                lo = mid
        out.append((lo + hi) / 2)
    return out


def card(ej, ec, fr=None, g=0.1):
    e = levels(ej, ec)
    f01, f12 = e[1] - e[0], e[2] - e[1]
    h = levels(ej, ec, 0.5)
    c = {'E_J/h (GHz)': ej, 'E_C/h (GHz)': ec, 'E_J/E_C': ej / ec, 'f01 (GHz)': f01, 'f12 (GHz)': f12,
         'alpha (MHz)': (f12 - f01) * 1000, '近似 f01 (GHz)': math.sqrt(8 * ej * ec) - ec,
         '電荷色散 (kHz)': abs(f01 - (h[1] - h[0])) * 1e6, 'C_sigma (fF)': EC_PER_FF / ec, 'I_c (nA)': ej / EJ_PER_NA}
    if fr is not None:
        delta, a = f01 - fr, (f12 - f01)
        chi = g * g * a / (delta * (delta + a))          # 簡報 p37：χ = g²α / [Δ(Δ+α)]
        kappa = 2 * abs(chi)                             # 令 κ ≈ 2|χ|
        c.update({'讀取腔 (GHz)': fr, '失諧 Δ (GHz)': delta, '|Δ|/g': abs(delta) / g, 'chi (MHz)': chi * 1000,
                  'kappa (MHz)': kappa * 1000, 'Purcell T1 上限 (us)': 1 / (2 * math.pi * kappa * 1e9 * (g / delta) ** 2) * 1e6})
    return c


def show(name, c):
    print(name)
    for k, v in c.items():
        print(f'  {k:>18}: {v:,.4g}')


def ej_for(target, ec):
    """E_C 固定時，找出讓 f01 = target 的 E_J（二分法）。"""
    lo, hi = ec, 400 * ec
    for _ in range(60):
        mid = (lo + hi) / 2
        e = levels(mid, ec, k=2)
        if e[1] - e[0] < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


print('一、範例卡（transmon 簡報 p12：E_J/h = 15 GHz、E_C/h = 250 MHz）＋讀取腔 7 GHz')
EXAMPLE = card(15, 0.25, fr=7.0)
show('  範例', EXAMPLE)

print()
print('二、製程誤差：E_J 多 2%（15 → 15.3 GHz）')
SHIFT = card(15.3, 0.25)['f01 (GHz)'] - EXAMPLE['f01 (GHz)']
print(f'  f01 偏移 {SHIFT * 1000:+.0f} MHz（{SHIFT / EXAMPLE["f01 (GHz)"] * 100:+.2f}%）')

print()
print('三、目標 5 GHz、E_C/h = 250 MHz：需要的 E_J')
EJ5 = ej_for(5.0, 0.25)
show(f'  E_J/h = {EJ5:.2f} GHz', card(EJ5, 0.25, fr=7.0))

print()
print('四、簡報 p37 的讀取範例（f01 5.0 GHz、α −250 MHz、讀取腔 7.0 GHz、g 100 MHz）')
d, a, g = -2.0, -0.25, 0.1
chi = g * g * a / (d * (d + a))
P37 = 1 / (2 * math.pi * 2 * abs(chi) * 1e9 * (g / d) ** 2) * 1e6
print(f'  χ = {chi * 1000:.2f} MHz，κ = 2|χ| = {2 * abs(chi) * 1000:.2f} MHz，Purcell T1 上限 ≈ {P37:.0f} μs，臨界光子數 Δ²/4g² = {d * d / (4 * g * g):.0f}')
for dd in (-1.0, -2.0, -3.0):
    t = 1 / (2 * math.pi * 2 * abs(chi) * 1e9 * (g / dd) ** 2) * 1e6
    print(f'  同樣 κ，失諧 {dd:+.1f} GHz → Purcell T1 上限 ≈ {t:.0f} μs')

print()
print('五、動畫 index.html#potential（E_C/h 固定 250 MHz）的讀數')
SCENE = {}
for r in (10, 50, 100):
    c = card(r * 0.25, 0.25)
    SCENE[r] = c
    print(f'  E_J/E_C = {r:3d}：f01 = {c["f01 (GHz)"]:.3f} GHz、f12 = {c["f12 (GHz)"]:.3f} GHz、α = {c["alpha (MHz)"]:.0f} MHz、近似 {c["近似 f01 (GHz)"]:.3f} GHz')

# 想設計自己的卡：改這三個數字
MY_EJ, MY_EC, MY_FR = 15.0, 0.25, 7.0
print()
show('六、我的卡', card(MY_EJ, MY_EC, fr=MY_FR))
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'transmon_card.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、投影片、動畫段讀數相同
_EX = R['EXAMPLE']
assert round(_EX['f01 (GHz)'], 2) == 5.21 and round(_EX['alpha (MHz)']) == -283 and round(_EX['近似 f01 (GHz)'], 2) == 5.23
assert round(_EX['C_sigma (fF)'], 1) == 77.5 and round(R['SHIFT'] * 1000) == 55
assert round(R['P37']) == 57
assert [round(R['SCENE'][r]['f01 (GHz)'], 3) for r in (50, 100)] == [4.735, 6.811]
assert [round(R['SCENE'][r]['alpha (MHz)']) for r in (50, 100)] == [-287, -274]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q032：模組發表：設計我的 transmon（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂是 QM02 模組的發表會，好玩機制是「工程答辯」：
孩子要做一張 transmon 參數卡，寫下三個數字——頻率 f₀₁、非諧性 α、E_J／E_C——並替每個數字說出取捨。下半場再加上讀取腔頻率，說明失諧為什麼要這麼大。
上一堂 Q031 是退相干偵探；下一堂 Q033 進入新模組：讀取要快、準、不破壞。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三個數字：頻率、非諧性、E_J／E_C；範例卡；常見誤解；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 用參數設計器做參數卡，再到 index.html#potential 驗證能階 | 列印包第 1、2 頁、`transmon_card.py`、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：加讀取腔頻率，說明失諧為什麼要這麼大 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與原理（工程答辯） | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替參數卡取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_參數卡.pdf`（A4，共 4 頁）。
- 讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#potential` 和 `transmon-3d.html#capacitor`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `transmon_card.py`（參數設計器，不需要安裝套件）。

## 驗收重點

1. 完成「transmon 參數卡」：f₀₁、α、E_J／E_C 三個數字，每個旁邊有一句取捨；下半場加上讀取腔頻率與失諧。
2. 不看稿說出核心原理：f₀₁ ≈ √(8E_JE_C) − E_C；α ≈ −E_C，太小脈衝要放慢；比值加大，電荷色散指數下降、非諧性只慢慢變小。
3. 指出至少一個注意事項：參數卡是設計目標；製程誤差（例如氧化層厚度改變臨界電流）會讓實際頻率偏移。

## 誠實說明

- 典型範圍取自學程簡報（JJ_Microwave_Readout_Talk p20），範例卡取自 transmon 簡報 p12；不是某一家公司的真實晶片規格。
- 「參數設計器」在課綱標為需新增的工具；本課用 `transmon_card.py` 和 transmon-3d 第 1 章的電容分頁代替。
- 參數卡是設計，家裡沒有晶片可以量；不要編造量測數據。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：做參數卡（約 40 分鐘）

1. 先訂目標：例如「f₀₁ = 5 GHz」。把典型範圍抄在列印包第 1 頁每一格旁邊（f₀₁ 4–6 GHz、α −200～−300 MHz、E_J／E_C 50–100）。
2. 用參數設計器試數字，二選一：
   - `transmon_card.py`：改最下面的 `MY_EJ`、`MY_EC`（單位 GHz）再執行，抄下 f₀₁、α、E_J／E_C、C_Σ、電荷色散。
   - `transmon-3d.html#capacitor`：E_J/h 固定 15 GHz，拉 C_Σ 滑桿，讀數會給 E_C、比值、f₀₁、α、電荷色散與判斷。
3. 三個數字都落在典型範圍裡，就抄到參數卡上；每個數字旁邊寫一句取捨（列印包第 2 頁有提示）。
4. 到 `index.html#potential` 驗證：把「E_J / E_C」滑桿調到卡上的比值（這個場景的 E_C 固定 250 MHz），看右邊金色標籤的頻率是不是一格比一格小，讀數的 α 是不是負兩三百 MHz。

## 下半場：孩子改造——加上讀取腔（約 30 分鐘）

1. 在列印包第 3 頁寫下讀取腔頻率（例如 7 GHz）。
2. 算失諧 Δ = f₀₁ − f_r，和耦合 g（約 100 MHz）比一比：|Δ| 要遠大於 g。
3. 用一句話說明失諧為什麼要這麼大：不交換能量，只互相推頻率；讀取腔的頻率才會變成狀態的指示器。
4. 加分：把 `MY_FR` 改成 6 或 8，看 transmon_card.py 算出的 Purcell T₁ 上限怎麼變。
''',

'transmon_card.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## transmon_card.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 範例卡（transmon 簡報 p12）\n\n'
  '| 項目 | 數值 | 一句取捨 |\n|---|---|---|\n'
  '| E_J/h | 15 GHz（I_c ≈ 30 nA） | 接面越大（I_c 越大），頻率越高 |\n'
  '| E_C/h | 250 MHz（C_Σ ≈ 77.5 fF） | 電容越大，越不怕背景電荷，但 α 越小 |\n'
  '| E_J／E_C | 60 | 50–100：電荷色散已經很小，α 還有兩百多 MHz |\n'
  '| f₀₁ | 5.21 GHz | 5 GHz ≈ 0.24 K ≫ 10–20 mK；和讀取腔、鄰居錯開 |\n'
  '| α | −283 MHz | 夠大，微波才能只挑 0 和 1；太小脈衝要放慢 |\n\n'
  '## 暫停題：E_J 從 15 變成 15.3 GHz（多 2%），頻率偏多少？\n\n'
  '- 約 +55 MHz（約 1%）。f₀₁ 大約跟著 √E_J 走，所以 E_J 多 2%，f₀₁ 約多 1%。這就是為什麼參數卡只是設計目標。\n\n'
  '## 讀取腔改造範例\n\n'
  '> 我的量子位元 5.21 GHz，讀取腔選 7 GHz，失諧約 −1.8 GHz，是耦合 100 MHz 的十幾倍。失諧這麼大，量子位元和讀取腔不交換能量，'
  '只互相推頻率，讀取腔的頻率會因為量子位元在 0 或 1 而偏一點點，量讀取腔就知道狀態；失諧太小，量子位元的能量也比較容易經由讀取腔漏掉。\n\n'
  '（簡報 p28、p37；Purcell 上限依 κ 而定，transmon_card.py 以 κ = 2|χ| 計算。）\n\n'
  '## 常見問題\n\n'
  '- 為什麼不把比值拉到一千？電荷色散早就小到不用擔心，α 卻繼續變小，閘要更慢。\n'
  '- 為什麼頻率不選 1 GHz？1 GHz 換算約 0.05 K，和 10–20 mK 比沒有大很多，熱擾動比較容易把它激發。\n'
  '- 動畫 index.html#potential 的 E_C 固定 250 MHz，所以拉比值滑桿等於只改 E_J：頻率跟著變，α 幾乎不變。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。

## `index.html#potential`（JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon）

- E_C/h 固定 250 MHz；載入時 E_J/E_C = 50、JJ / Transmon 模式。左邊面板往下捲有按鈕、滑桿和讀數。
- 「LC 諧振子（線性）」：位能是拋物線，右邊金色標籤三格都是 5.00 GHz，讀數 α = 0（等間距 → 無法單獨定址）。
- 「JJ / Transmon（非線性）」：餘弦位能，金色標籤 4.74、4.45、4.13 GHz，一格比一格小；讀數 α = −287 MHz。
- 「E_J / E_C（對數刻度）」滑桿拉到 100：讀數 f₀₁ 6.811 GHz、α −274 MHz——頻率跟著 E_J 走，α 幾乎不變。
- 右下小圖是電荷色散：比值越大，三條線越平。

## `transmon-3d.html#capacitor`（Transmon 3D 第 1 章：大十字電容的作用）

- E_J/h 固定 15 GHz；載入時 C_Σ = 77.5 fF：E_C 250 MHz、比值 60.0、f₀₁ 5.21 GHz、α −283 MHz、電荷色散 1.9 kHz，就是範例卡。
- 拉到 85 fF：f₀₁ 4.99 GHz、α −256 MHz、比值 65.8、電荷色散約 685 Hz——一組接近 5 GHz 的設計。
- 「回到 77.5 fF」按鈕回到範例卡。

## 之後的課

Q033「讀取要快、準、不破壞」會說出讀取量子位元的三個條件。
''',
}

SHEET_HEADER = ['項目', '我的數字', '典型範圍', '一句取捨']
SHEET_ROWS = [['頻率 f₀₁', '', '4–6 GHz'], ['非諧性 α', '', '−200～−300 MHz'], ['E_J／E_C', '', '50–100'],
              ['E_J/h', '', ''], ['E_C/h（C_Σ）', '', ''], ['讀取腔頻率 f_r', '', '例如 7 GHz'], ['失諧 Δ', '', '遠大於 g ≈ 100 MHz']]

EXTRA_CSS = '''table.rec td{height:13mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:3px solid #0b2540;border-radius:4mm;padding:4mm 6mm}.card h3{margin:0 0 2mm;font-size:15pt}
.card table{width:100%;border-collapse:collapse}.card td{border-bottom:1px solid #9fb0c8;padding:3mm 2mm;font-size:12pt}
.tip{font-size:10.5pt;color:#35506b}'''


def html():
    rows = [('頻率 f₀₁', 'GHz', '4–6 GHz'), ('非諧性 α', 'MHz', '−200～−300 MHz'), ('E_J／E_C', '', '50–100'),
            ('E_J/h', 'GHz', ''), ('E_C/h', 'MHz', ''), ('總電容 C_Σ', 'fF', '60–100 fF')]
    card = ''.join(f'<tr><td style="width:30%"><b>{a}</b></td><td>＿＿＿＿＿ {u}</td><td class="tip">{r}</td></tr>' for a, u, r in rows)
    pages = [
        '<h2>transmon 參數卡</h2><p class="lead">先訂目標，再用參數設計器試數字；三個主要數字都要落在典型範圍裡。</p>'
        '<div class="card"><h3>作品名稱：＿＿＿＿＿＿＿＿＿＿　設計者：＿＿＿＿＿＿</h3>'
        '<p>我的目標：f₀₁ ＝ ＿＿＿＿ GHz</p><table>' + card + '</table>'
        '<p style="margin-top:4mm">在 index.html#potential 驗證：比值調到 ＿＿＿，金色標籤 ＿＿＿／＿＿＿／＿＿＿ GHz　□ 一格比一格小</p></div>'
        '<p class="tip">提示：f₀₁ ≈ √(8E_J E_C) − E_C；α ≈ −E_C；C_Σ ≈ 19.37 ÷ (E_C/h，GHz) fF。</p>',
        '<h2>三個數字的取捨單</h2><p class="lead">每個數字寫一句：為什麼選這個值？放棄了什麼？</p>'
        '<table class="rec"><tr><th>數字</th><th>選太小會怎樣</th><th>選太大會怎樣</th><th>我的取捨（一句話）</th></tr>'
        '<tr><td>頻率 f₀₁</td><td></td><td></td><td></td></tr><tr><td>非諧性 α</td><td></td><td></td><td></td></tr>'
        '<tr><td>E_J／E_C</td><td></td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:4mm"><p>線索：5 GHz 換算約 0.24 K，冷凍機 10–20 mK；等間距會一起共振；比值加大，電荷色散指數下降、α 冪次下降。</p>'
        '<p>暫停題：E_J 從 15 變成 15.3 GHz（多 2%），f₀₁ 大約偏多少？</p><div class="line"></div>'
        '<p>所以參數卡上的數字是：□ 保證　□ 設計目標</p></div>',
        '<h2>讀取腔改造單</h2><p class="lead">替參數卡加一個讀取腔頻率，說明失諧為什麼要這麼大。</p>'
        '<div class="box"><p>讀取腔頻率 f_r ＝ ＿＿＿＿ GHz　　量子位元 f₀₁ ＝ ＿＿＿＿ GHz</p>'
        '<p>失諧 Δ ＝ f₀₁ − f_r ＝ ＿＿＿＿ GHz　　耦合 g ≈ 0.1 GHz　　|Δ| ÷ g ＝ ＿＿＿＿</p></div>'
        '<div class="box" style="margin-top:4mm"><p>失諧為什麼要這麼大？（提示：交換能量、推頻率、狀態的指示器）</p><div class="line"></div>'
        '<p>失諧太小會怎樣？（提示：能量經由讀取腔漏掉）</p><div class="line"></div>'
        '<p>失諧太大又會怎樣？（提示：推頻率的效果變弱）</p><div class="line"></div></div>',
        '<h2>說明卡：我的 transmon 參數卡</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 模組發表：設計我的 transmon在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：工程答辯</h3><ul class="chk">'
        '<li>不看稿說出卡上的三個數字</li><li>替每個數字說一句取捨</li>'
        '<li>說出讀取腔頻率與失諧的理由</li><li>說出參數卡是設計目標，製程誤差會讓頻率偏移</li>'
        '<li>在 index.html#potential 示範驗證能階</li><li>替參數卡取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q032 transmon 參數卡 列印包', '父子科技學院 量子電腦學程 Q032｜模組發表：設計我的 transmon', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q032-design-my-transmon', folder='Q032_設計我的transmon', files=FILES,
        sheet=('03_參數卡紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_參數卡.pdf', pack_pages=4,
        pack_needles=('transmon 參數卡', '三個數字的取捨單', '讀取腔改造單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q032', episode_dir='specials/q032-design-my-transmon',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（transmon_card.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'transmon_card.py',
               'recordedRun': {'example_f01_GHz': round(_EX['f01 (GHz)'], 3), 'example_alpha_MHz': round(_EX['alpha (MHz)'], 1),
                               'ej_plus_2pct_shift_MHz': round(R['SHIFT'] * 1000, 1), 'p37_purcell_us': round(R['P37'], 1),
                               'scene_f01_GHz': {r: round(R['SCENE'][r]['f01 (GHz)'], 3) for r in (10, 50, 100)}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q032/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

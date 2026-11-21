"""Q022 課堂教材：間距紀錄表、能階梯子圖（列印）、不等距梯子改造卡、說明卡、解答、ladder_table.py、動畫導覽。

不需要帳號，也不需要安裝套件（ladder_table.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#potential、lc-vs-jj.html#s3、#s4。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q022/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q022：能階梯子表——等距（LC）與不等距（約瑟夫森接面）。

不用安裝任何套件，只要 Python 3。執行：  python ladder_table.py
一、LC 電路：f = 1/(2π√(LC))（維基百科 LC circuit），量子化後 E_n = hf(n + ½)，每一階的間距都是 hf。
二、約瑟夫森接面做的量子位元（transmon）：H = 4E_C n² − E_J cos φ 在電荷基底上算出前幾個能階
    （和學程動畫 lc-vs-jj.html 第 3 步同一種算法：三對角矩陣 + 二分法數特徵值），E_C/h = 0.25 GHz。
能量都用「除以普朗克常數 h」之後的頻率（GHz）表示。
"""
from math import pi, sqrt

EC = 0.25  # GHz


def lc_frequency(L, C):
    return 1 / (2 * pi * sqrt(L * C))


def lc_levels(f, k=5):
    return [f * (n + 0.5) for n in range(k)]


def transmon_levels(EJ, k=5, N=25):
    """H = 4E_C n² − (E_J/2)(|n⟩⟨n+1| + h.c.)，n = −N…N；回傳最低 k 個能量（加 E_J，讓谷底為 0）。"""
    d = [4 * EC * (i - N) ** 2 for i in range(2 * N + 1)]
    e2 = (EJ / 2) ** 2

    def count(x):  # 小於 x 的特徵值個數（Sturm 序列）
        c, q = 0, d[0] - x
        if q < 0:
            c += 1
        for i in range(1, len(d)):
            q = d[i] - x - e2 / (q if q != 0 else 1e-300)
            if q < 0:
                c += 1
        return c

    out = []
    for j in range(k):
        lo, hi = -EJ - 1, 4 * EC * N * N + EJ + 1
        for _ in range(70):
            m = (lo + hi) / 2
            if count(m) > j:
                hi = m
            else:
                lo = m
        out.append((lo + hi) / 2 + EJ)
    return out


def gaps(levels):
    return [b - a for a, b in zip(levels, levels[1:])]


def z(x):
    """浮點誤差造成的 −0.000 顯示成 0"""
    return 0.0 if abs(x) < 1e-9 else x


print('一、LC 電路：每一階的間距（GHz）')
LC = {}
for L, C, name in ((1e-9, 1e-12, '1 nH、1 pF'), (4e-9, 1e-12, '4 nH、1 pF（電感換大）'), (0.25e-9, 1e-12, '0.25 nH、1 pF（電感換小）')):
    f = lc_frequency(L, C) / 1e9
    g = gaps(lc_levels(f))
    LC[name] = g
    print(f'  {name:<22} 0→1 {g[0]:.3f}　1→2 {g[1]:.3f}　2→3 {g[2]:.3f}　3→4 {g[3]:.3f}　差 {z(1000 * (g[1] - g[0])):.0f} MHz')

print()
print('二、約瑟夫森接面做的量子位元（E_C/h = 0.25 GHz）')
TR = {}
for ratio in (50, 80):
    g = gaps(transmon_levels(ratio * EC))
    TR[ratio] = g
    print(f'  E_J/E_C = {ratio:<3}  0→1 {g[0]:.3f}　1→2 {g[1]:.3f}　2→3 {g[2]:.3f}　3→4 {g[3]:.3f}　非諧性 {z(1000 * (g[1] - g[0])):.0f} MHz')

print()
print('三、微波對準 0→1 時，其他跳躍差多遠（GHz）')
for name, g in (('LC 1 nH、1 pF', LC['1 nH、1 pF']), ('transmon E_J/E_C = 50', TR[50])):
    print(f'  {name:<22} ' + '　'.join(f'{k}→{k + 1} 差 {z(g[k] - g[0]):.3f}' for k in range(1, 4)))
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'ladder_table.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白（約五吉赫、每階一樣、換大變小、4.74／4.45／4.13、約負兩百九十兆赫）及動畫段（−287、80 → −277）相同
_g1 = R['LC']['1 nH、1 pF']
assert round(_g1[0], 2) == 5.03 and max(_g1) - min(_g1) < 1e-9
assert round(R['LC']['4 nH、1 pF（電感換大）'][0], 2) == 2.52
assert [round(x, 2) for x in R['TR'][50][:3]] == [4.74, 4.45, 4.13]
assert round(1000 * (R['TR'][50][1] - R['TR'][50][0])) == -287 and round(1000 * (R['TR'][80][1] - R['TR'][80][0])) == -277

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q022：量子諧振子：等距的梯子（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。上一堂把彈簧和 LC 電路對起來；這一堂把 LC 電路當成「量子諧振子」：
能量只能一階一階，而且每一階的間距都一樣（等距的梯子）。量子位元只要最低的兩階，但等距的梯子讓對準 0→1 的微波也對準 1→2、2→3，
狀態會「一路往上爬」，挑不出兩個能階。下一堂的約瑟夫森接面，就是讓梯子變得不等距的元件。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 能階、零點能、等距的梯子、一路往上爬、常見誤會 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 在能階場景切到 LC 模式，抄下每一階的間距；畫出等距梯子圖，用箭頭畫「一路往上爬」 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：畫出不等距梯子，寫出為什麼能只在 0 與 1 之間跳 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：怎麼操作場景、為什麼等距不能用 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替梯子圖取名字、存檔 | |

## 課前準備（約 15 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開啟 `index.html#potential`（課綱指定），先按一次「LC 諧振子（線性）」和「JJ / Transmon（非線性）」；再開 `lc-vs-jj.html#s3`、`#s4`（見 `05_動畫導覽.md`）。
- 列印 `02_列印包_能階梯子圖.pdf`（A4，共 4 頁）；準備直尺、彩色筆。讀一遍 `04_解答.md`。
- 有電腦可以跑 Python 3 的話，執行一次 `ladder_table.py`（不需要安裝套件）。

## 驗收重點

1. 完成能階梯子圖：等距梯子（每階標間距）＋一支一支往上爬的箭頭；不等距梯子（間距一階比一階小）。
2. 不看稿說出核心原理：LC 電路的能階等距，對準 0→1 的微波也對準上面每一階，所以挑不出只有兩階的量子位元。
3. 指出至少一個注意事項：「等距」才是問題所在，不是能量太高或太低——換電感或電容只會讓整把梯子一起變寬或變窄。

## 誠實說明

- 本集不推導薛丁格方程式，只用 E_n = hf(n + ½) 的結果。
- 4.74、4.45、4.13 GHz 和 −287 MHz 是動畫的例子（E_J/E_C = 50、E_C/h = 250 MHz），不是某一顆晶片的量測值；transmon 筆記簡報 p14 的例子是 5.21、4.93 GHz、−283 MHz，算法一樣、參數不同。
- 「碰不到一到二」是簡化：脈衝太短時頻譜變寬，還是會漏到 |2⟩，之後的課會談。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：切到 LC 模式、抄間距、畫梯子（約 40 分鐘）

1. 打開 `index.html#potential`。一開始是 transmon（餘弦山谷），先讓孩子記下右邊三個金色數字（4.74、4.45、4.13 GHz）。
2. 爸爸按左側面板的「LC 諧振子（線性）」：山谷變成拋物線。孩子把右邊金色的三個數字抄到列印包第 1 頁（都是 5.00 GHz），再看面板讀數「非諧性 α/2π = 0 MHz（等間距 → 無法單獨定址）」。
3. 闖關一：按「10」，數字變成多少？（2.24 GHz，只看得到三階）再按「Transmon：50」回到 5.00。問孩子：間距變大變小了，可是有沒有哪一階不一樣？
4. 在列印包第 2 頁畫等距梯子：每一階一樣高，旁邊寫 5 GHz。從 |0⟩ 畫一支向上的箭頭到 |1⟩，寫「微波 5 GHz」；再用同樣長的箭頭從 |1⟩ 畫到 |2⟩、|2⟩ 畫到 |3⟩——這就是「一路往上爬」。
5. 一起看 `lc-vs-jj.html#s4`：上面 LC 那一行只有一條綠線，旁邊寫「0→1 = 1→2 = 2→3 = 3→4 全部重疊」「驅動一路往上爬」。

## 下半場：孩子改造——畫不等距梯子（約 30 分鐘）

1. 用列印包第 3 頁。畫一把越往上越窄的梯子，旁邊寫 4.74、4.45、4.13 GHz（或自己設計的數字，但要一階比一階小）。
2. 用綠筆畫一支對準 0→1 的箭頭（4.74 GHz）；在 1→2 旁邊寫「差多少？」（約 0.29 GHz，也就是 −287 MHz 的非諧性）。
3. 一起看 `lc-vs-jj.html#s3`：左邊四個 5.00、右邊一路變小；把滑桿拉到 80，左邊一起變 6.32，右邊還是不等距。
4. 寫一句說明：「為什麼微波對準 0→1 時，不會把狀態推到 2？」
''',

'ladder_table.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## ladder_table.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 闖關的答案\n\n'
  '- 第一關：量子諧振子的能量只能是 hf(n + ½)，n = 0, 1, 2, …；最低的 ½hf 叫零點能，所以不會完全靜止。\n'
  '- 第二關：LC 電路的間距全部是 hf（例子：1 nH、1 pF 約 5.03 GHz；動畫 LC 模式 5.00 GHz）。對準 0→1 的微波也對準 1→2、2→3，狀態一路往上爬。\n'
  '- 第三關：不等距梯子的例子 4.74、4.45、4.13 GHz；1→2 比 0→1 低約 0.29 GHz，對準 0→1 的微波打不到 1→2。\n\n'
  '## 暫停題：每一階間距都不一樣時，微波要選哪個頻率？\n\n'
  '- 選 0→1 的間距（例子 4.74 GHz）。這個頻率只和 0→1 共振；1→2 的間距不同，所以不會被推上去。\n\n'
  '## 常見問題\n\n'
  '- 是不是能量太低、太容易被熱擾動，所以 LC 不能用？不是本題的重點。電感或電容換大換小，只是整把梯子一起變窄或變寬（實跑：4 nH 時 2.52 GHz、0.25 nH 時 10.07 GHz），間距之間的差永遠是 0。課綱的常見誤會就是這一條：「等距」才是問題所在。\n'
  '- 為什麼是「一路往上爬」，不是在 0 和 1 之間來回？因為 1→2 的頻率和 0→1 一樣，微波推完 0→1，馬上也能推 1→2，再推 2→3……\n'
  '- 動畫的數字為什麼和簡報 p14 不一樣？參數不同（動畫 E_J/E_C = 50、E_C = 250 MHz）；算法一樣，非諧性都約 −E_C。\n'
  '- 不等距就完全不會漏嗎？不是。脈衝太短時頻譜變寬，還是會漏到 |2⟩；lc-vs-jj.html 第 6 步（DRAG）談這件事，之後的課會講。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#` 名稱可以直接跳到那一段。

## `index.html#potential`（3D 場景 4：非線性——從 LC 諧振子到 Transmon）

- 一打開是 transmon（餘弦山谷），右邊金色標籤 ω01、ω12、ω23 是 4.74、4.45、4.13 GHz，面板讀數非諧性 −287 MHz。
- 按「LC 諧振子（線性）」：拋物線山谷，金色標籤三個都是 5.00 GHz，讀數「非諧性 α/2π = 0 MHz（等間距 → 無法單獨定址）」。
- 在 LC 模式按「10」：金色標籤變成 2.24 GHz（只看得到三階），非諧性仍是 0；按「Transmon：50」回到 5.00 GHz。左側面板內容很長，按鈕在下方，要往下捲。

## `lc-vs-jj.html#s4`（第 4 步：用微波去驅動）

- 每條直線代表一個躍遷的頻率，陰影帶是對準 ω₀₁ 的驅動微波。
- LC 那一行：一條綠線，寫著「0→1 = 1→2 = 2→3 = 3→4 全部重疊」「驅動一路往上爬」。
- Transmon 那一行：四條線分開，只有 0→1 是綠色（打到），其他是灰色（沒打到）。

## `lc-vs-jj.html#s3`（第 3 步：位能與量子能階）

- 左圖 LC 拋物線（藍），右圖 transmon 餘弦（橘）；右側數字是相鄰能階的間距（GHz）。
- 滑桿 E_J/E_C 預設 50：左邊四個 5.00；右邊 4.74、4.45、4.13、3.70、3.50；讀數非諧性 −287 MHz。
- 拉到 80：左邊一起變 6.32；右邊 6.06、5.79、5.48……仍然一階比一階小；非諧性 −277 MHz。
''',
}

SHEET_HEADER = ['場景與設定', '0→1（GHz）', '1→2（GHz）', '2→3（GHz）', '非諧性讀數（MHz）', '每一階一樣嗎', '備註']
SHEET_ROWS = [['index.html#potential 一打開（JJ / Transmon）'], ['index.html#potential 按 LC 諧振子'], ['LC 模式 按 10'],
              ['LC 模式 按 Transmon：50'], ['lc-vs-jj.html#s3 滑桿 50（右圖）'], ['lc-vs-jj.html#s3 滑桿 80（右圖）']]

EXTRA_CSS = '''table.rec td{height:14mm;font-size:10.5pt}table.rec th:first-child{width:52mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.grid2{display:flex;gap:6mm;margin-top:3mm}.grid2>div{flex:1;border:1.3pt solid #0b2540;border-radius:3mm;height:150mm;padding:3mm 4mm;
background-image:repeating-linear-gradient(to top,#dbe6f0 0,#dbe6f0 .5pt,transparent .5pt,transparent 10mm)}
.grid1{border:1.3pt solid #0b2540;border-radius:3mm;height:120mm;padding:3mm 4mm;margin-top:3mm;
background-image:repeating-linear-gradient(to top,#dbe6f0 0,#dbe6f0 .5pt,transparent .5pt,transparent 10mm)}'''


def html():
    rows = [r[0] for r in SHEET_ROWS]
    pages = [
        '<h2>間距紀錄表</h2><p class="lead">把場景右邊金色的數字（相鄰兩階的間距）抄下來，再看讀數的非諧性。</p>'
        '<p>日期：＿＿＿＿＿＿　操作的人：＿＿＿＿＿＿　記錄的人：＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>場景與設定</th><th>0→1</th><th>1→2</th><th>2→3</th><th>非諧性</th><th>一樣嗎</th></tr>'
        + ''.join(f'<tr><td>{r}</td><td></td><td></td><td></td><td></td><td></td></tr>' for r in rows) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>按「10」之後，間距變大還是變小？每一階還一樣嗎？</p><div class="line"></div></div>',
        '<h2>能階梯子圖：等距的梯子</h2><p class="lead">左邊畫 LC 電路的梯子，每一階一樣高、旁邊寫間距；右邊用箭頭畫出微波怎麼一路往上爬。</p>'
        '<p>梯子圖名稱：＿＿＿＿＿＿＿＿＿＿＿＿　畫的人：＿＿＿＿＿＿</p>'
        '<div class="grid2"><div><b>LC 電路的梯子</b>（標 |0⟩、|1⟩、|2⟩、|3⟩ 和間距）</div>'
        '<div><b>微波 5 GHz 打進去</b>（每推一階畫一支箭頭）</div></div>',
        '<h2>改造：不等距梯子</h2><p class="lead">畫一把越往上越窄的梯子，標出每一階的間距，再畫出只對準 0→1 的微波。</p>'
        '<div class="grid1"><b>我的不等距梯子</b>（例子：4.74、4.45、4.13 GHz）</div>'
        '<div class="box" style="margin-top:4mm"><p>為什麼微波對準 0→1 時，不會把狀態推到 2？</p><div class="line"></div><div class="line"></div></div>',
        '<h2>說明卡：我的能階梯子圖</h2><div class="box"><p>梯子圖名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 量子諧振子：等距的梯子在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（怎麼操作場景、怎麼畫）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：LC 電路的能階梯子是什麼形狀</li><li>說出為什麼它不能直接當量子位元</li>'
        '<li>示範在場景切到 LC 模式、讀出間距</li><li>指出注意事項：等距才是問題，不是能量太高或太低</li>'
        '<li>說出不等距梯子怎麼解決</li><li>替梯子圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q022 能階梯子圖 列印包', '父子科技學院 量子電腦學程 Q022｜量子諧振子：等距的梯子', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q022-equal-ladder', folder='Q022_量子諧振子等距的梯子', files=FILES,
        sheet=('03_間距紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_能階梯子圖.pdf', pack_pages=4,
        pack_needles=('間距紀錄表', '能階梯子圖', '不等距梯子', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q022', episode_dir='specials/q022-equal-ladder',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（ladder_table.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'ladder_table.py',
               'recordedRun': {'lc_1nH_1pF_gap_GHz': round(R['LC']['1 nH、1 pF'][0], 3),
                               'lc_4nH_1pF_gap_GHz': round(R['LC']['4 nH、1 pF（電感換大）'][0], 3),
                               'lc_025nH_1pF_gap_GHz': round(R['LC']['0.25 nH、1 pF（電感換小）'][0], 3),
                               'transmon_50_gaps_GHz': [round(x, 3) for x in R['TR'][50]],
                               'transmon_50_alpha_MHz': round(1000 * (R['TR'][50][1] - R['TR'][50][0])),
                               'transmon_80_alpha_MHz': round(1000 * (R['TR'][80][1] - R['TR'][80][0]))},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q022/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

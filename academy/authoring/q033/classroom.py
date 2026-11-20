"""Q033 課堂教材：讀取需求表、三種讀取比較表、冒險關卡計算單、說明卡（列印）、解答、readout_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（readout_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#iq、#dispersive 與 animations/atoms.html#imaging。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q033/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q033：讀取需求表小工具。

不用安裝任何套件，只要 Python 3。執行：  python readout_check.py
- 一、快：讀取途中掉回 |0⟩ 的機會 ≈ 1 − e^(−t/T1)（只算 T1 衰減）。
- 二、準：讀取保真度 F = 1 − [P(1|0) + P(0|1)] / 2（學程簡報 JJ_Microwave_Readout_Talk p31）。
- 三、檢查一張讀取需求表有沒有過關（目標數字是本課設計的練習數字）。
- 四、動畫 atoms.html#imaging 的判別保真度（animations/js/atoms/12_imaging.js 第 48、55–58 行：
  亮平均 3 × 曝光毫秒數、暗平均 0.12 × 曝光毫秒數 + 0.6，Poisson 分佈，選最好的閾值）。
"""
import math


def decay_chance(t_read_us, t1_us):
    """讀取 t_read 微秒、能量弛豫時間 T1 微秒：讀取途中掉回 |0⟩ 的機會。"""
    return 1 - math.exp(-t_read_us / t1_us)


def fidelity(p1_given0, p0_given1):
    """兩種誤判機率（0–1）→ 讀取保真度。"""
    return 1 - (p1_given0 + p0_given1) / 2


def passes(t_read_us, t1_us, f, repeat_same):
    """本課的練習目標：讀取時間 ÷ T1 ≤ 1/200、保真度 ≥ 99 %、連量兩次相同 ≥ 99 %。"""
    return {'快': t_read_us / t1_us <= 1 / 200, '準': f >= 0.99, '不破壞': repeat_same >= 0.99}


def _pois(lam, k):
    return math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1))


def _cdf(lam, k):
    return sum(_pois(lam, i) for i in range(k))


def imaging_fidelity(expo_ms):
    bright, dark = 3.0 * expo_ms, 0.12 * expo_ms + 0.6
    best, bf = 1, 0.0
    th = 1
    while th < bright + 3:
        f = 1 - ((1 - _cdf(dark, th)) + _cdf(bright, th)) / 2
        if f > bf:
            bf, best = f, th
        th += 1
    return best, bf


print('一、快：讀取途中掉回 |0⟩ 的機會（只算 T1 衰減）')
DECAY = {}
for t_read, t1 in ((0.1, 100), (0.5, 100), (0.5, 1000), (5, 100), (50, 100)):
    p = decay_chance(t_read, t1)
    DECAY[(t_read, t1)] = p
    print(f'  讀取 {t_read:5.1f} μs、T1 = {t1:5d} μs：讀取時間 ÷ T1 = {t_read / t1:.4f} → 約 {100 * p:.2f} %')

print()
print('二、準：讀取保真度')
FID = {}
for a, b in ((0.004, 0.012), (0.005, 0.015), (0.01, 0.03)):
    f = fidelity(a, b)
    FID[(a, b)] = f
    print(f'  P(1|0) = {100 * a:.1f} %、P(0|1) = {100 * b:.1f} % → F = {100 * f:.1f} %，平均誤判 {100 * (a + b) / 2:.1f} %')

print()
print('三、範例需求表檢查（讀取 0.5 μs、T1 = 100 μs、F = 99.2 %、連量兩次相同 99.5 %）')
CHECK = passes(0.5, 100, FID[(0.004, 0.012)], 0.995)
for k, v in CHECK.items():
    print(f'  {k}：' + ('過關' if v else '沒過'))

print()
print('四、動畫 atoms.html#imaging 的判別保真度')
IMG = {}
for e in (1, 2, 5, 10, 20):
    th, f = imaging_fidelity(e)
    IMG[e] = (th, f)
    print(f'  曝光 {e:2d} ms：亮平均 {3 * e:.0f} 光子、暗平均 {0.12 * e + 0.6:.1f} → 閾值 {th}，判別保真度 {100 * f:.2f} %')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'readout_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、動畫段、12_imaging.js 公式相同
assert round(R['DECAY'][(0.5, 100)] * 1000, 1) == 5.0
assert abs(R['FID'][(0.004, 0.012)] - 0.992) < 1e-9
assert all(R['CHECK'].values())
assert R['IMG'][10][0] == 11 and f"{100 * R['IMG'][10][1]:.2f}" == '100.00'
assert R['IMG'][1][0] == 2 and f"{100 * R['IMG'][1][1]:.2f}" == '81.90'

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q033：讀取要快、準、不破壞（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂用「冒險任務」闖三道關卡，說出讀取量子位元的三個條件：
快（讀取時間 ≪ T₁）、準（高保真度：只量一次就判對）、不破壞（量子非破壞量測，QND：量完停在量到的結果）。
接著看為什麼不直接量電壓、超導的色散讀取、原子平台的螢光讀取。作品是一張「讀取需求表」：把三個條件各寫成可量的指標和目標數字。
下一堂 Q034 是電路 QED：量子位元＋諧振腔。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三道關卡、直接量電壓的問題、色散與螢光讀取、常見誤解；看 3D 動畫 | 影片第 2–8 段、`05_動畫導覽.md` |
| 25–65 | 寫讀取需求表：每一關寫指標、目標數字、怎麼驗收 | 列印包第 1、3 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：比較直接、色散、螢光三種讀取各過幾關 | 列印包第 2 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替需求表取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_讀取需求表.pdf`（A4，共 4 頁）。另備計算機或手機計算機、彩色筆。
- 讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#iq`、`index.html#dispersive`、`atoms.html#imaging`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `readout_check.py`（不需要安裝套件）。

## 驗收重點

1. 完成「讀取需求表」：快、準、不破壞各有一個指標、一個目標數字、一個驗收方法。
2. 不看稿說出核心原理：讀取要比 T₁ 快很多，否則讀到一半就掉回 |0⟩；只量一次就要判對；量完要停在量到的結果，才能再量、接著算。
3. 指出至少一個注意事項：「不破壞」是指不改變被量到的狀態，不是不改變疊加態。

## 誠實說明

- 讀取時間 100–500 ns、最佳 T₁ 約 0.1–1 ms、誤判率 < 1 % 取自學程簡報 p6、p26 的代表值；離子、中性原子的數字取自離子阱與中性原子簡報。
- 需求表的目標數字（1/200、99 %）是本課設計的練習數字，不是某台機器的規格。家裡沒有量子位元可以量，作品寫的是規格與驗收方法，不要編造量測數據。
- 動畫的時間、保真度是示意；保真度讀數會因為隨機抽樣每次差一點。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：讀取需求表（約 40 分鐘）

1. 用列印包第 3 頁「冒險關卡計算單」先算兩題：讀取途中掉下來的機會（讀取時間 ÷ T₁）、兩種誤判的保真度。
2. 拿列印包第 1 頁的讀取需求表，一關一列：
   - 快：指標（例如讀取時間 ÷ T₁）、目標數字、怎麼驗收（例如量讀取時間、查 T₁）。
   - 準：指標（例如單發讀取保真度）、目標數字、怎麼驗收（準備 |0⟩、|1⟩ 各量很多次，數誤判）。
   - 不破壞：指標（例如連量兩次結果一樣的比例）、目標數字、怎麼驗收。
3. 每一格都要能回答「怎麼知道過關了沒」；寫不出驗收方法的，就是規格還太模糊。
4. 用動畫對照：`index.html#iq` 拉「積分時間」和「T1」滑桿，看快和準怎麼互相牽制。

## 下半場：孩子改造——比較三種讀取（約 30 分鐘）

1. 用列印包第 2 頁的比較表：直接量電壓、色散讀取、螢光讀取。
2. 每一格打 ✓、✗ 或 ？，再寫一句理由。
3. 比速度時，要和那個平台自己的相干時間比（離子 T₂ 秒～小時、中性原子約 1 秒、超導約 0.1–1 ms）。
4. 用動畫對照：`index.html#dispersive` 看色散讀取；`atoms.html#imaging` 看中性原子的推出和成像。
''',

'readout_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## readout_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 讀取需求表參考答案\n\n'
  '| 關卡 | 指標 | 目標數字（練習用） | 怎麼驗收 |\n|---|---|---|---|\n'
  '| 快 | 讀取時間 ÷ T₁ | 不超過 1/200（例：500 ns 對 100 μs） | 量讀取脈衝的時間；查同一顆量子位元的 T₁ |\n'
  '| 準 | 單發讀取保真度 F = 1 − 兩種誤判機率的平均 | 至少 99 %（誤判率 < 1 %） | 準備 |0⟩、|1⟩ 各量幾千次，數判錯的次數 |\n'
  '| 不破壞 | 連續量兩次，結果一樣的比例 | 至少 99 % | 量完馬上再量一次，數兩次一樣的比例 |\n\n'
  '（數字依據：簡報 JJ_Microwave_Readout_Talk p6、p26、p31；目標數字是本課設計的練習數字。）\n\n'
  '## 三種讀取比較參考答案\n\n'
  '| 讀取方式 | 快 | 準 | 不破壞 |\n|---|---|---|---|\n'
  '| 直接量電壓 | ？（簡報沒有給速度） | ✗ 能量只有約 20 μeV，訊號極弱 | ✗ 直接接設備會引入耗散、破壞相干性 |\n'
  '| 色散讀取（超導） | ✓ 100–500 ns ≪ T₁ 0.1–1 ms | ✓ 單發 > 99 % | ✓ 只碰諧振腔、不翻轉量子位元（光子數不能太多） |\n'
  '| 螢光讀取（原子） | 離子約 200 μs、中性原子 1–20 ms，比超導慢很多；但要和各自的相干時間（秒級）比 | ✓ 離子 > 99.9 %、中性原子 > 99 % | 看做法：中性原子常見的推出法會把 |1⟩ 原子推走，是破壞性的；也有非破壞讀取的做法 |\n\n'
  '（簡報 JJ_Microwave_Readout_Talk p26、p28；Ion_NeutralAtom_Talk p4、p19、p35、p39。）\n\n'
  '## 暫停題：一半一半的量子位元量到 1，馬上再用不破壞的讀取量一次？\n\n'
  '- 會得到 1。疊加不在了：量第一次時就已經變成 |1⟩，這不是讀取「破壞」了什麼，而是量測本來就會讓疊加變成其中一個結果。'
  '不破壞的意思是：量到 1 之後，它就停在 |1⟩，不會被讀取弄亂。\n\n'
  '## 冒險關卡計算單答案\n\n'
  '- 讀取 0.5 μs、T₁ = 100 μs：讀取時間 ÷ T₁ = 0.005，途中掉下來約 0.5 %（千分之五）。\n'
  '- 讀取 5 μs、T₁ = 100 μs：0.05，約 4.9 %——太慢，光是這一項誤判就超過 1 %。\n'
  '- 誤判 0.4 % 與 1.2 %：平均 0.8 %，F = 99.2 %，過關；誤判 1 % 與 3 %：平均 2 %，F = 98 %，沒過。\n\n'
  '## 常見問題\n\n'
  '- 讀久一點不是比較準嗎？動畫 `index.html#iq` 裡，積分時間加長，兩團點縮小、比較分得開；但 |1⟩ 在讀取途中掉回 |0⟩ 的拖尾也變多。'
  '把 T1 滑桿拉大（讀取時間 ≪ T₁），拖尾才會少（簡報 p31 備註：這就是讀取的根本權衡）。\n'
  '- 為什麼色散讀取不翻動量子位元？量子位元和諧振腔頻率差很遠，不交換能量，只讓諧振腔頻率依 |0⟩、|1⟩ 往下或往上偏；我們只探測諧振腔（簡報 p28）。\n'
  '- 為什麼光子不能太多？腔內光子會讓量子位元失相，超過臨界光子數，色散近似就失效（簡報 p28）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。
左邊面板很長，按鈕和滑桿在下方，要往下捲。

## `index.html#iq`（JJ 與微波讀取 3D 場景 10：單發讀取：IQ 叢集與狀態判別）＝快與準

- 每條細線是一次讀取，從上方落到平面變成一個點；藍點是準備 |0⟩、紅點是準備 |1⟩，金色的線是判別線。
- 「積分時間」拉到最短：兩團變寬、混在一起，讀取保真度掉到約八成。拉到最大：兩團變小，但有些紅點拖到中間（|1⟩ 在讀取途中掉回 |0⟩）。
- 「T1」滑桿拉大：拖尾變少，保真度回升。讀數有兩種誤判機率和讀取保真度 F。每次改滑桿，點會清空重新累積。

## `index.html#dispersive`（場景 9：色散讀取）＝不破壞

- 藍、紅兩個峰是諧振腔在量子位元 |0⟩、|1⟩ 時的反應，峰的位置錯開。上方小球預設每 3 秒自動切換狀態。
- 按「量子位元 |1⟩」或「量子位元 |0⟩」會停止自動切換；讀數顯示兩個狀態的相位差（預設 90°）。

## `atoms.html#imaging`（離子阱與中性原子 3D 場景 12：螢光成像讀取）＝螢光讀取

- 依序按「準備隨機態」（紅 = |1⟩、藍 = |0⟩）、「① 推出 |1⟩」（紅色原子飛走）、「② 成像」（留下的原子發光，相機影像出現亮點）。
- 「曝光時間」從 10 ms 拉到 1 ms，判別保真度從 100.00 % 掉到 81.90 %。這是破壞性的做法；「非破壞讀取（另一種做法）」可以切換比較。

## 之後的課

Q034「電路 QED：量子位元＋諧振腔」會看讀取怎麼透過諧振腔「間接」看量子位元。
''',
}

SHEET_HEADER = ['關卡', '指標', '目標數字', '怎麼驗收', '過關了嗎']
SHEET_ROWS = [['快'], ['準'], ['不破壞']]

EXTRA_CSS = '''table.rec td{height:22mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
table.cmp td{height:30mm;font-size:11pt;text-align:left;vertical-align:top}table.cmp th{font-size:11pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.calc p{margin:2.5mm 0;font-size:12pt}'''


def html():
    pages = [
        '<h2>讀取需求表</h2><p class="lead">把「快、準、不破壞」各寫成一個可以量的指標、一個目標數字，再寫怎麼驗收。</p>'
        '<table class="rec"><tr><th style="width:14%">關卡</th><th>指標（量什麼）</th><th>目標數字</th><th>怎麼驗收</th><th style="width:12%">過關？</th></tr>'
        '<tr><td>快</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>準</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>不破壞</td><td></td><td></td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:4mm"><p>提示：快 → 讀取時間 ÷ T₁；準 → 單發讀取保真度；不破壞 → 連量兩次結果一樣的比例。</p>'
        '<p>檢查：每一格都能回答「怎麼知道過關了沒」嗎？</p></div>',
        '<h2>三種讀取比較表</h2><p class="lead">每格打 ✓、✗ 或 ？，再寫一句理由。比速度要和那個平台自己的相干時間比。</p>'
        '<table class="cmp"><tr><th style="width:18%">讀取方式</th><th>快</th><th>準</th><th>不破壞</th></tr>'
        '<tr><td>直接量電壓</td><td></td><td></td><td></td></tr>'
        '<tr><td>色散讀取（超導）</td><td></td><td></td><td></td></tr>'
        '<tr><td>螢光讀取（原子）</td><td></td><td></td><td></td></tr></table>'
        '<p style="font-size:10.5pt;color:#35506b">線索：超導讀取 100–500 ns、T₁ 0.1–1 ms；離子螢光約 200 μs、T₂ 秒～小時；中性原子曝光 1–20 ms、T₂ 約 1 秒；量子位元能量約 20 μeV。</p>',
        '<h2>冒險關卡計算單</h2><p class="lead">先算一算，再把數字寫進需求表。</p>'
        '<div class="box calc"><h3>第一關：快</h3><p>讀取途中掉下來的機會 ≈ 讀取時間 ÷ T₁（很小的時候）</p>'
        '<p>① 讀取 0.5 μs、T₁ = 100 μs：＿＿＿＿＿　② 讀取 5 μs、T₁ = 100 μs：＿＿＿＿＿</p><p>哪一個能過「誤判率 < 1 %」？＿＿＿＿＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>第二關：準</h3><p>保真度 F = 1 − （本來是 0 判成 1 ＋ 本來是 1 判成 0）÷ 2</p>'
        '<p>① 0.4 % 與 1.2 %：F = ＿＿＿＿＿　② 1 % 與 3 %：F = ＿＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>第三關：不破壞</h3><p>一顆一半一半的量子位元量到 1，馬上再量一次，會得到＿＿＿＿；疊加還在嗎？＿＿＿＿</p>'
        '<p>「不破壞」不改變的是：＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>說明卡：我的讀取需求表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 讀取要快、準、不破壞在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出讀取的三個條件</li><li>每個條件說出一個目標數字</li>'
        '<li>說出為什麼不直接量電壓</li><li>說出「不破壞」不是保住疊加</li>'
        '<li>講解三種讀取的比較表</li><li>替需求表取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q033 讀取需求表 列印包', '父子科技學院 量子電腦學程 Q033｜讀取要快、準、不破壞', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q033-readout-requirements', folder='Q033_讀取要快準不破壞', files=FILES,
        sheet=('03_讀取需求表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_讀取需求表.pdf', pack_pages=4,
        pack_needles=('讀取需求表', '三種讀取比較表', '冒險關卡計算單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q033', episode_dir='specials/q033-readout-requirements',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（readout_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'readout_check.py',
               'recordedRun': {'decay_0.5us_T1_100us': round(R['DECAY'][(0.5, 100)], 4),
                               'fidelity_0.4_1.2': round(R['FID'][(0.004, 0.012)], 3),
                               'imaging_fidelity': {f'{e}ms': round(R['IMG'][e][1], 4) for e in R['IMG']}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q033/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

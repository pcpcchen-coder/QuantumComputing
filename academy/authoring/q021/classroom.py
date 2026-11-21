"""Q021 課堂教材：週期紀錄表、類比對照表（列印）、改造預測卡、說明卡、解答、oscillation_table.py、動畫導覽。

不需要帳號，也不需要安裝套件（oscillation_table.py 只要 Python 3）；動畫用瀏覽器開啟 animations/lc-vs-jj.html#s1、#s2。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q021/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q021：彈簧、單擺、LC 電路的週期對照。

不用安裝任何套件，只要 Python 3。執行：  python oscillation_table.py
公式（維基百科 Simple harmonic motion、Pendulum (mechanics)、LC circuit）：
  彈簧    T = 2π√(m/k)
  單擺    T0 = 2π√(ℓ/g)（小角度）；任意振幅 T = T0 / AGM(1, cos(θ0/2))（算術幾何平均）
  LC 電路 T = 2π√(LC)，f = 1/T
把下面的數字換成你家量到的值，再跑一次。
"""
from math import pi, sqrt, cos, radians

G = 9.81  # 重力加速度（m/s²）


def spring_period(m, k):
    return 2 * pi * sqrt(m / k)


def pendulum_small(length):
    return 2 * pi * sqrt(length / G)


def agm(a, b):
    while abs(a - b) > 1e-15:
        a, b = (a + b) / 2, sqrt(a * b)
    return a


def pendulum_ratio(theta_deg):
    """大振幅週期 ÷ 小角度週期"""
    return 1 / agm(1.0, cos(radians(theta_deg) / 2))


def lc_period(L, C):
    return 2 * pi * sqrt(L * C)


print('一、彈簧（彈簧常數 k = 20 N/m）')
SPRING = []
for m in (0.1, 0.2, 0.4, 0.8):
    SPRING.append((m, spring_period(m, 20)))
    print(f'  重物 {m * 1000:4.0f} g  →  週期 {spring_period(m, 20):.3f} 秒')
print('  質量變成 4 倍（0.1 → 0.4 kg），週期變成', round(spring_period(0.4, 20) / spring_period(0.1, 20), 3), '倍')

print()
print('二、單擺（小角度）')
PEND = []
for length in (0.25, 0.5, 1.0):
    PEND.append((length, pendulum_small(length)))
    print(f'  擺長 {length:4.2f} m  →  週期 {pendulum_small(length):.3f} 秒（和重物多重無關）')
print('  擺長變成 1/4（1 → 0.25 m），週期變成', round(pendulum_small(0.25) / pendulum_small(1.0), 3), '倍')

print()
print('三、單擺拉到大角度：週期是小角度時的幾倍')
RATIO = {}
for th in (5, 10, 20, 30, 45, 60, 90):
    RATIO[th] = pendulum_ratio(th)
    print(f'  從 {th:2d} 度放手  →  {RATIO[th]:.4f} 倍')

print()
print('四、LC 電路')
LC = []
for L, C, name in ((1e-3, 1e-6, '1 mH、1 μF'), (1e-9, 1e-12, '1 nH、1 pF')):
    T = lc_period(L, C)
    LC.append((name, 1 / T))
    print(f'  {name}  →  週期 {T:.3e} 秒，每秒振盪 {1 / T:.3e} 次')
print('  電感變成 4 倍（1 nH → 4 nH），週期變成', round(lc_period(4e-9, 1e-12) / lc_period(1e-9, 1e-12), 3), '倍')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'oscillation_table.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白（四倍→兩倍、一公尺約兩秒、九十度多約百分之十八、約五吉赫）相同
assert abs(R['spring_period'](0.4, 20) / R['spring_period'](0.1, 20) - 2) < 1e-12
assert round(R['pendulum_small'](1.0), 1) == 2.0 and round(R['RATIO'][90], 2) == 1.18
assert round(R['LC'][1][1] / 1e9, 2) == 5.03 and round(R['LC'][0][1] / 1e3, 2) == 5.03

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q021：彈簧、單擺與 LC 電路（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂先離開超導，回到彈簧和單擺：
把力學的振盪和 LC 電路（電感＋電容）的振盪一格一格對起來——質量↔電感、彈簧↔電容。下一堂的「量子諧振子」就從這個 LC 電路出發。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 彈簧、單擺、LC 電路、類比對照表、週期公式；看動畫的直線與正弦 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 量彈簧和單擺的週期（數十次再除以十），填出力學與 LC 的對照表 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：改變質量或擺長，先預測週期，再量、再比 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：怎麼量、為什麼這樣對應 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替對照表取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 彈簧（玩具彈簧、彈簧秤或文具店的拉力彈簧都可以）、幾個一樣重的重物（例如同款的鉤碼、裝水的小瓶子、一串鑰匙）、細繩、膠帶、捲尺、碼錶（手機也可以）。
- 找一個能掛東西的地方（門框、桌邊、晾衣架），單擺的繩子要能調到 1 公尺和 25 公分。
- 列印 `02_列印包_類比對照表.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `lc-vs-jj.html#s1` 和 `#s2`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `oscillation_table.py`（不需要安裝套件），先看預測值。

## 驗收重點

1. 完成類比對照表：位置↔電荷、速度↔電流、質量↔電感、彈簧↔電容（彈簧常數 k 對應 1/C）、位能⇄動能 對應 電容能⇄電感能。
2. 不看稿說出核心原理：質量和電感都「抗拒速度（電流）的改變」；彈簧把位移變成力、電容把電荷變成電壓；週期跟著 √(m/k) 與 √(LC) 變。
3. 指出至少一個注意事項：類比只在小振幅時成立；大振幅的單擺週期會變久，不再是簡諧運動。

## 誠實說明

- 類比不只一種。課綱的「質量↔電感、彈簧↔電容」是阻抗類比（力 ↔ 電壓、位移 ↔ 電荷）；學程簡報 ep049 p8 把磁通 Φ 對到位置 x，那是對偶的配法（電容 ↔ 質量）。兩種都對，選哪一種看你把哪個量當「位置」。
- 家裡量到的週期會和公式差一點：彈簧本身有質量、擺錘不是一個點、碼錶有反應時間。差個幾個百分比是正常的。
- 1 nH、1 pF 是為了好算而選的整數例子，不是某一顆量子位元的實際元件值。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：量週期、填對照表（約 40 分鐘）

1. 掛彈簧：彈簧上端固定，下端掛一個重物，等它靜止。爸爸把重物往下拉 2～3 公分，輕輕放手（不要拉到彈簧變形）。
2. 量週期：孩子在重物通過最低點時按下碼錶並數「零」，之後每回到最低點數一下，數到「十」按停。總時間 ÷ 10 = 一次的週期。量三次取平均，填進列印包第 1 頁。
3. 掛單擺：細繩一端綁重物、一端固定，從固定點量到重物中心是 1 公尺。拉開一個小角度（重物離開中間不超過 15 公分，約 9 度以內），輕輕放手。
4. 同樣數十次來回、量三次取平均。和公式的 2.0 秒比一比。
5. 填列印包第 2 頁的類比對照表：力學那一欄寫你剛剛看到的（位置、速度、質量、彈簧、位能、動能），電路那一欄寫對應的東西，最後一欄寫「為什麼」。
6. 一起看 `lc-vs-jj.html#s1`：把相位滑桿拉小，直線和正弦幾乎疊在一起；拉大就分開——這就是「小角度才像簡諧運動」。

## 下半場：孩子改造——先預測再驗證（約 30 分鐘）

1. 用列印包第 3 頁。一次只改一件事，改之前先寫預測。
2. 彈簧：重物換成 4 個（4 倍重），預測週期變成幾倍？量完填實測值。（預測：2 倍）
3. 單擺：繩子調成 25 公分（1/4），預測週期？（預測：一半，約 1.0 秒）
4. 單擺：重物換成更重的，擺長不變，預測週期？（預測：幾乎不變）
5. 加分題：單擺從很大的角度（約 60～90 度）放手，量週期和小角度比一比。用 `oscillation_table.py` 查預測（60 度約 1.07 倍、90 度約 1.18 倍）。
6. 在對照表下面寫一句：「這個類比什麼時候不成立？」
''',

'oscillation_table.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 類比對照表參考答案（阻抗類比）\n\n'
  '| 彈簧–質量 | LC 電路 | 為什麼 |\n|---|---|---|\n'
  '| 位置 x | 電容上的電荷 Q | 兩者都是「被推離平衡多遠」 |\n'
  '| 速度 v | 電流 I | 位置變化的快慢 ↔ 電荷流動的快慢 |\n'
  '| 質量 m | 電感 L | 質量抗拒速度改變，電感抗拒電流改變 |\n'
  '| 彈簧常數 k | 1/C | 彈簧把位移變成力，電容把電荷變成電壓；彈簧越硬 ↔ 電容越小 |\n'
  '| 推力 F | 電壓 V | 讓東西動起來的「推」 |\n'
  '| 位能 ½kx² | 電容能 Q²/2C | 被「拉開」時存的能量 |\n'
  '| 動能 ½mv² | 電感能 ½LI² | 「在動」時存的能量 |\n'
  '| 週期 2π√(m/k) | 週期 2π√(LC) | 把上面的對應代進去就一樣 |\n\n'
  '另一種配法：把磁通 Φ 當位置（學程簡報 ep049 p8 的哈密頓量那一列），這時電容 ↔ 質量、1/L ↔ k。兩種都成立（維基百科 Harmonic oscillator 的類比表兩欄都列出）。\n\n'
  '## oscillation_table.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 改造的預測\n\n'
  '- 彈簧重物變 4 倍 → 週期變 √4 = 2 倍。\n'
  '- 單擺擺長變 1/4 → 週期變 1/2（1 公尺約 2.0 秒 → 25 公分約 1.0 秒）。\n'
  '- 單擺換更重的重物 → 週期幾乎不變（單擺週期和質量無關）。\n'
  '- LC：電感或電容變 4 倍 → 週期變 2 倍。\n\n'
  '## 暫停題：彈簧被拉過頭、變形回不去了，對照表還成立嗎？\n\n'
  '- 不成立。對照表靠的是「力和伸開的距離成正比」（虎克定律），彈簧被拉過頭就不再成正比，也就不再是簡諧運動；'
  '這和大角度的單擺一樣：類比只在小振幅、線性的範圍裡成立。\n\n'
  '## 常見問題\n\n'
  '- 彈簧對應電容，那彈簧越硬電容越大嗎？相反。彈簧常數 k 對應的是 1/C，彈簧越硬，對應的電容越小。\n'
  '- 單擺換重一點會擺得比較慢嗎？不會。重一點的擺錘受的重力大，但也更難加速，兩者抵消，週期幾乎不變。\n'
  '- 量到的週期和公式差了一點？正常。彈簧本身有質量、擺錘不是點、碼錶有反應時間；數十次再除以十可以減少碼錶誤差。\n'
  '- 真實的 LC 電路會一直振下去嗎？有電阻就會慢慢停下來；超導電路的電阻是零，這也是超導量子位元要用超導體的原因之一。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號（字型會從網路載入，離線時改用系統字型）。網址後面的 `#` 名稱可以直接跳到那一步。
這一頁是平面的互動圖解（不是 3D 場景）；藍色是電感（直線），橘色是約瑟夫森接面（正弦，之後的課會細談）。

## `lc-vs-jj.html#s1`（第 1 步：電流與磁通——直線 vs 正弦）

- 藍色直線：電感 I = φ（電流和磁通成正比）；橘色曲線：JJ I = sin φ。
- 「相位 φ」滑桿拉到 0.2：兩個圓點幾乎疊在一起，讀數 0.200 和 0.199；下面的說明寫「φ 很小：sin φ ≈ φ……這時它看起來是線性的」。
- 拉到 1.0：讀數 1.000 和 0.841，兩個圓點分開了。對照單擺：回復力跟著 sin θ，擺角小時 sin θ ≈ θ，就像彈簧；擺角大了就不像了。

## `lc-vs-jj.html#s2`（第 2 步：用正弦波去推，輸出長什麼樣？）

- 「驅動振幅 A」滑桿調到 0.3：藍色和橘色的波形幾乎重疊，頻譜幾乎只剩基頻；讀數「輸入加倍，輸出峰值變成（電感）」永遠是 2.00 倍。
- 調到 2.5：藍色跟著變高，橘色最高只到 +I_c 虛線、波峰中間凹下去；頻譜冒出 3ω 柱子（約基頻的 44 %）；JJ 的「輸入加倍」讀數只剩 1.00 倍。
- 重點：線性系統（像遵守虎克定律的彈簧、LC 電路）不會產生新的頻率；推得太大，非線性就出現了。

## 之後的課

第 3 步（`#s3`）是位能與量子能階，下一堂 Q022「量子諧振子：等距的梯子」會用到。
''',
}

SHEET_HEADER = ['項目', '條件（質量／擺長／角度）', '第 1 次 十次總秒數', '第 2 次', '第 3 次', '平均一次的週期（秒）', '預測（秒）', '差多少']
SHEET_ROWS = [['彈簧 1 個重物'], ['彈簧 4 個重物'], ['單擺 1 公尺'], ['單擺 25 公分'], ['單擺 1 公尺 換重物'], ['單擺 1 公尺 大角度']]

EXTRA_CSS = '''table.rec td{height:15mm;font-size:10.5pt}table.rec th:first-child{width:34mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.demo td{font-size:10.5pt;height:14mm}table.demo th:first-child{width:30mm}'''


def html():
    rows = ['彈簧 1 個重物', '彈簧 4 個重物', '單擺 1 公尺', '單擺 25 公分', '單擺 1 公尺 換重物', '單擺 1 公尺 大角度']
    analog = [('位置', ''), ('速度', ''), ('質量', ''), ('彈簧（彈簧常數 k）', ''), ('位能', ''), ('動能', ''), ('週期公式', '')]
    pages = [
        '<h2>週期紀錄表</h2><p class="lead">數十次來回再按停，總秒數 ÷ 10 就是一次的週期；每一項量三次取平均。</p>'
        '<p>日期：＿＿＿＿＿＿　放手的人：＿＿＿＿＿＿　計時的人：＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>項目</th><th>十次總秒數（三次）</th><th>平均一次的週期</th><th>預測</th></tr>'
        + ''.join(f'<tr><td>{r}</td><td></td><td></td><td></td></tr>' for r in rows) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>為什麼數十次比只量一次準？</p><div class="line"></div></div>',
        '<h2>類比對照表</h2><p class="lead">左邊寫力學，中間寫對應的電路，右邊寫為什麼。</p>'
        '<p>對照表名稱：＿＿＿＿＿＿＿＿＿＿＿＿　做的人：＿＿＿＿＿＿</p>'
        '<table class="demo"><tr><th>彈簧–質量</th><th>LC 電路</th><th>為什麼這樣對應</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td></tr>' for a, b in analog) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>這個類比什麼時候不成立？</p><div class="line"></div></div>',
        '<h2>改造預測卡</h2><p class="lead">一次只改一件事：先寫預測，再量，再比一比。</p>'
        '<table class="demo"><tr><th>改了什麼</th><th>預測：週期變幾倍</th><th>實測</th><th>猜對了嗎</th></tr>'
        '<tr><td>彈簧重物 ×4</td><td></td><td></td><td></td></tr>'
        '<tr><td>單擺擺長 ÷4</td><td></td><td></td><td></td></tr>'
        '<tr><td>單擺換更重的重物</td><td></td><td></td><td></td></tr>'
        '<tr><td>單擺從大角度放手</td><td></td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:4mm"><h3>週期公式</h3>'
        '<p>彈簧 T = 2π√(m/k)　　單擺 T ≈ 2π√(ℓ/g)（小角度）　　LC 電路 T = 2π√(LC)</p>'
        '<p>1 公尺的單擺約 2 秒；1 nH、1 pF 的 LC 電路約 5 GHz（每秒五十億次）。</p></div>',
        '<h2>說明卡：我的類比對照表</h2><div class="box"><p>對照表名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 彈簧、單擺與 LC 電路在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（怎麼量、怎麼對應）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：為什麼質量對應電感、彈簧對應電容</li><li>說出週期跟著什麼改變</li>'
        '<li>示範怎麼用碼錶量週期</li><li>說出彈簧越硬，對應的電容越小</li>'
        '<li>指出一個注意事項：類比只在小振幅時成立</li><li>替對照表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q021 類比對照表 列印包', '父子科技學院 量子電腦學程 Q021｜彈簧、單擺與 LC 電路', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q021-spring-pendulum-lc', folder='Q021_彈簧單擺與LC電路', files=FILES,
        sheet=('03_週期紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_類比對照表.pdf', pack_pages=4,
        pack_needles=('週期紀錄表', '類比對照表', '改造預測卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q021', episode_dir='specials/q021-spring-pendulum-lc',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（oscillation_table.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'oscillation_table.py',
               'recordedRun': {'spring_mass_x4_period_ratio': round(R['spring_period'](0.4, 20) / R['spring_period'](0.1, 20), 3),
                               'pendulum_1m_s': round(R['pendulum_small'](1.0), 3),
                               'pendulum_quarter_length_ratio': round(R['pendulum_small'](0.25) / R['pendulum_small'](1.0), 3),
                               'large_angle_ratio': {str(k): round(v, 4) for k, v in R['RATIO'].items()},
                               'lc_1nH_1pF_GHz': round(R['LC'][1][1] / 1e9, 3), 'lc_1mH_1uF_kHz': round(R['LC'][0][1] / 1e3, 3)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q021/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

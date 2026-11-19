"""Q059 課堂教材：誤差速查卡、偵探案件卡、誤差緩解前後比較表、可執行的 error_lab.py（＋選用 qiskit_readout.py）、說明卡與解答。

不需要帳號；error_lab.py 只用 Python 標準函式庫。qiskit_readout.py 是選用版本（需要 qiskit 與 qiskit-aer）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q059/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q059：shots、統計誤差與讀取誤差緩解 的小模擬器（只用 Python 標準函式庫）

執行：python error_lab.py               → 加態跑 100、1000、10000 shots，印出原始值、誤差與緩解後的值
      python error_lab.py 次數 0.5 0.01  → 算出機率 0.5 時要達到 ±0.01 需要幾個 shots
      python error_lab.py 偵探            → 電腦偷偷決定有沒有讀取錯誤，你用 shots 與校準找出真相
公式：
  統計誤差 σ = √(P(1−P)/N)            （shots 加 4 倍，誤差才減半）
  需要的 shots N = P(1−P) ÷ 誤差²
  讀取誤差緩解（單一位元）：P_修正(1) = (P_量到(1) − P(1|0)) ÷ (P(1|1) − P(1|0))
改造區：改 P1_GIVEN_0、P0_GIVEN_1（讀取錯誤率）或 P_TRUE（理想的 P(1)）。
"""
import math
import random
import sys

P_TRUE = 0.5        # 理想的 P(1)：加態 |+⟩ 是 0.5
P1_GIVEN_0 = 0.02   # 準備 0 卻讀成 1 的機率
P0_GIVEN_1 = 0.08   # 準備 1 卻讀成 0 的機率（讀取途中 T₁ 衰減，通常比較大）


def read(bit, e10, e01, rng):
    """讀取：真正的位元是 bit，儀器偶爾讀錯。"""
    if bit == 0:
        return 1 if rng.random() < e10 else 0
    return 0 if rng.random() < e01 else 1


def run(p_true, shots, e10, e01, rng):
    """跑 shots 次：每次先依 p_true 決定位元（量子的隨機），再經過會讀錯的儀器。回傳讀到 1 的比例。"""
    ones = sum(read(1 if rng.random() < p_true else 0, e10, e01, rng) for _ in range(shots))
    return ones / shots


def sigma(p, n):
    return math.sqrt(p * (1 - p) / n)


def shots_needed(p, err):
    return math.ceil(round(p * (1 - p) / err ** 2, 9))


def calibrate(shots, e10, e01, rng):
    """校準線路：準備 0 量 shots 次、準備 1（先做 X）量 shots 次。回傳 P(1|0)、P(1|1)。"""
    return run(0.0, shots, e10, e01, rng), run(1.0, shots, e10, e01, rng)


def mitigate(p_meas, p10, p11):
    return min(1.0, max(0.0, (p_meas - p10) / (p11 - p10)))


def table(seed=59):
    rng = random.Random(seed)
    print(f'理想 P(1) = {P_TRUE}；讀取錯誤：P(1|0) = {P1_GIVEN_0}，P(0|1) = {P0_GIVEN_1}')
    p10, p11 = calibrate(10000, P1_GIVEN_0, P0_GIVEN_1, rng)
    print(f'校準（各 10000 shots）：P(1|0) = {p10:.4f}，P(1|1) = {p11:.4f}')
    print('shots｜原始 P(1) ± σ｜偏離理想幾個 σ｜緩解後 P(1)｜緩解後 σ')
    for n in (100, 1000, 10000):
        p = run(P_TRUE, n, P1_GIVEN_0, P0_GIVEN_1, rng)
        s = sigma(p, n)
        m = mitigate(p, p10, p11)
        print(f'{n:>6}｜{p:.4f} ± {s:.4f}｜{abs(p - P_TRUE) / s:4.1f}｜{m:.4f}｜{s / (p11 - p10):.4f}')
    print('\n看最後兩欄：shots 越多誤差越小，但原始值的偏差不會消失；緩解把它修回來，誤差稍微變大。')


def detective():
    rng = random.Random()
    cases = [('沒有讀取錯誤', 0.0, 0.0), ('讀取錯誤 2%／8%', 0.02, 0.08), ('讀取錯誤 5%／15%', 0.05, 0.15)]
    name, e10, e01 = rng.choice(cases)
    print('電腦準備了加態（理想 P(1) = 0.5），也偷偷決定了讀取錯誤（' + '、'.join(c[0] for c in cases) + ' 其中之一）。')
    print('輸入 shots 數字跑實驗；輸入 校準 跑校準線路；輸入 猜 結束。')
    while True:
        cmd = input('shots／校準／猜：').strip()
        if cmd.isdigit() and int(cmd) > 0:
            n = int(cmd); p = run(0.5, n, e10, e01, rng); s = sigma(p, n)
            print(f'  {n} shots：P(1) = {p:.4f} ± {s:.4f}，偏離 0.5 是 {abs(p - 0.5) / s:.1f} 個 σ')
        elif cmd == '校準':
            p10, p11 = calibrate(5000, e10, e01, rng)
            print(f'  校準（各 5000 shots）：P(1|0) = {p10:.4f}，P(0|1) = {1 - p11:.4f}')
        elif cmd in ('猜', 'g'):
            g = input('你猜是哪一個（0＝沒有、1＝2%／8%、2＝5%／15%）：').strip()
            print('答對了！' if g.isdigit() and int(g) < 3 and cases[int(g)][0] == name else '答錯了，', '答案是', name)
            return


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] in ('偵探', 'detective'):
        detective()
    elif a and a[0] in ('次數', 'shots'):
        p, err = float(a[1]), float(a[2])
        print(f'P = {p}、誤差 ±{err}：需要約 {shots_needed(p, err)} shots')
    else:
        table()
'''

QISKIT = r'''"""Q059 選用：用 Qiskit + Aer 跑 100、1000、10000 shots，並做一次混淆矩陣校正。
需要：pip install qiskit qiskit-aer（製作時用 qiskit 2.6.2、qiskit-aer 0.18.4 實跑過）。
"""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError

# 讀取錯誤：準備 0 讀成 1 的機率 2%，準備 1 讀成 0 的機率 8%（改這裡就是偵探遊戲的「偷偷加料」）
ro = ReadoutError([[0.98, 0.02], [0.08, 0.92]])
noise = NoiseModel(); noise.add_all_qubit_readout_error(ro)
sim = AerSimulator(noise_model=noise, seed_simulator=59)


def p1(qc, shots):
    c = sim.run(qc, shots=shots).result().get_counts()
    return c.get('1', 0) / shots


plus = QuantumCircuit(1); plus.h(0); plus.measure_all()
for N in (100, 1000, 10000):
    p = p1(plus, N); s = (p * (1 - p) / N) ** 0.5
    print(f'加態 {N:>5} 次：P(1) = {p:.4f} ± {s:.4f}')
# 校準線路：準備 0、準備 1
c0 = QuantumCircuit(1); c0.measure_all()
c1 = QuantumCircuit(1); c1.x(0); c1.measure_all()
e10 = p1(c0, 10000); e11 = p1(c1, 10000)
print(f'校準：P(1|0) = {e10:.4f}，P(1|1) = {e11:.4f}')
raw = p1(plus, 10000)
mit = (raw - e10) / (e11 - e10)
print(f'加態 10000 次：原始 P(1) = {raw:.4f}，緩解後 P(1) = {mit:.4f}（理想 0.5）')
'''

ns = {}
exec(compile(PROGRAM, 'error_lab.py', 'exec'), ns)  # 用同一份程式算解答，避免手抄錯
NEED = [(0.5, 0.01), (0.1, 0.01), (0.5, 0.05), (0.5, 0.005), (0.2, 0.02)]
NEED_ROWS = ''.join(f'| {p} | ±{e} | {ns["shots_needed"](p, e):,} |\n' for p, e in NEED)
SIG_ROWS = ''.join(f'| {n:,} | ±{ns["sigma"](0.5, n):.4f} |\n' for n in (100, 1000, 2500, 4000, 10000))
MIT = ns['mitigate'](0.47, 0.02, 0.92)

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q059：shots、統計誤差與讀取誤差緩解（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心兩句：**統計誤差 σ = √(P(1−P)/N)，shots 加 4 倍誤差才減半；讀取誤差不會因為多跑而消失，要先跑校準線路量出混淆矩陣，再把結果反推回去。** 好玩機制是資料偵探：爸爸偷偷設定（或不設定）讀取錯誤，孩子用「加 shots」和「校準」兩種證據找出偏差的來源。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開 operation.html#qubit 按「一次跑 1000 shots」看 ± 誤差；再看 operation.html#readout 的混淆矩陣與「讀取誤差緩解」 | 列印包第 1 頁（誤差速查卡） |
| 25–65 | 跑 `error_lab.py`（或 `qiskit_readout.py`）：100、1000、10000 shots，畫誤差變化；做一次校正，填前後比較表 | 列印包第 3 頁 |
| 65–75 | 休息 | |
| 75–105 | 改造：用 N = P(1−P) ÷ 誤差² 算 ±1% 要幾次，再用 `error_lab.py 次數 0.5 0.01` 與模擬驗證；玩資料偵探 | 列印包第 2、3 頁 |
| 105–115 | 孩子教爸爸：兩種誤差怎麼分、怎麼校準、緩解的限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_shots與讀取誤差緩解.pdf`（A4，共 4 頁）。第 2 頁偵探案件卡沿虛線剪開、對折蓋住。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#qubit`、`operation.html#readout`（場景 1、7），不需要帳號。
- 電腦有 Python 3 就能執行 `error_lab.py`（不用安裝套件）。想用 Qiskit：`pip install qiskit qiskit-aer` 後執行 `qiskit_readout.py`。
- 讀一遍 `04_解答.md`。

## 誠實說明

- σ = √(P(1−P)/N) 是近似誤差（1σ）；shots 很少或機率很接近 0、1 時不夠準。
- 混淆矩陣例子（2%、8%）是教學用的數字；真實硬體的讀取錯誤約 0.5%～3%，每天校準都會變。
- 單一位元的緩解公式就是 2×2 混淆矩陣求反；多位元時矩陣是 2ⁿ×2ⁿ，實務上常假設各位元獨立。
- 緩解只修讀取，不修閘錯誤；而且會讓誤差範圍變大一點（要多跑 shots）。
''',

'01_操作步驟.md': '''# 操作步驟

## 先看動畫（約 15 分鐘）

1. 打開 `animations/operation.html#qubit`（場景 1）。按「|+⟩」，再按「一次跑 1000 shots」。
2. 左邊面板捲到最下面：「估計 P̂(1) = … ± 0.016（1σ）」。再按三次（共 4000 次）：± 0.008。再按十二次（共 16000 次）：± 0.004。
3. 看右下小圖：灰帶就是 ±1σ，橫軸是 shots 數（對數），越往右越窄。
4. 打開 `animations/operation.html#readout`（場景 7）。「準備狀態 θ」拉到 0°，「兩團雲的間距」調到 0.60。
5. 面板最下面：混淆矩陣 P(1|0) = 13.8%、P(0|1) = 14.5%。按「讀取誤差緩解」關掉：⟨Z⟩ 約 0.72；再打開：回到接近 1。

## 用模擬器跑三種 shots（約 40 分鐘）

1. 執行 `python error_lab.py`。表格會印出 100、1000、10000 shots 的原始 P(1)、誤差 σ、偏離理想幾個 σ、緩解後的 P(1)。
2. 把三列畫成圖：橫軸 shots（100、1000、10000），縱軸 σ。每多 10 倍 shots，σ 變成大約 1/3（√10 ≈ 3.16）。
3. 填前後比較表：原始值、緩解後的值、各自的誤差。
4. 想用 Qiskit：執行 `python qiskit_readout.py`，結果應該很接近。

## 改造：±1% 要幾次（約 30 分鐘）

1. 用公式 N = P(1−P) ÷ 誤差² 先手算：P = 0.5、誤差 0.01 → ？；P = 0.1 → ？
2. 用 `python error_lab.py 次數 0.5 0.01` 核對。
3. 把 `error_lab.py` 的 shots 改成你算出的數字，跑幾次，看 σ 是否在 0.01 附近。

## 資料偵探

1. 爸爸抽一張案件卡（或執行 `python error_lab.py 偵探`，讓電腦出題）。
2. 爸爸照案件卡改 `error_lab.py` 的 P1_GIVEN_0、P0_GIVEN_1（或 `qiskit_readout.py` 的 ReadoutError），只把結果給孩子看。
3. 孩子的證據一：加 shots。偏差忽正忽負、越跑越小 → 運氣。證據二：跑校準。P(1|0)、P(0|1) 不是 0 → 儀器。
4. 猜對換人出題；每一題寫進比較表。
''',

'error_lab.py': PROGRAM,
'qiskit_readout.py': QISKIT,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 統計誤差（P = 0.5，由 `error_lab.py` 的 sigma() 算出）\n\n'
  '| shots | σ |\n|---|---|\n' + SIG_ROWS +
  '\n100 → 10000（×100）誤差 ÷10；1000 → 4000（×4）誤差 ÷2。\n\n'
  '## 需要幾個 shots（N = P(1−P) ÷ 誤差²，由 shots_needed() 算出）\n\n'
  '| P | 誤差 | shots |\n|---|---|---|\n' + NEED_ROWS +
  '\n期望值 ⟨Z⟩ = 1 − 2P(1)，誤差是 2σ：要 ⟨Z⟩ 到 ±0.01，σ 要 0.005 → P = 0.5 時約 10,000 shots。\n\n'
  '## 混淆矩陣與緩解（影片的例子）\n\n'
  '- 校準：準備 0 量 1000 次 → 0：980、1：20；準備 1 量 1000 次 → 0：80、1：920。\n'
  '- M = [[P(0|0), P(0|1)], [P(1|0), P(1|1)]] = [[0.98, 0.08], [0.02, 0.92]]。\n'
  '- 加態理想 (0.5, 0.5)，量到 M·(0.5, 0.5) = (0.53, 0.47)。\n'
  f'- 緩解：(0.47 − 0.02) ÷ (0.92 − 0.02) = 0.45 ÷ 0.90 = {MIT:.2f}，就是 M⁻¹·(0.53, 0.47)。\n'
  '- 10000 shots 時 σ ≈ 0.005，偏差 0.03 ≈ 6σ → 不是運氣；1000 shots 時 σ ≈ 0.016，偏差只有約 1.9σ，還分不出來。\n'
  '- 緩解後誤差 ≈ 0.005 ÷ 0.90 ≈ 0.0055，比原始的大一點。\n\n'
  '## 偵探案件卡判讀\n\n'
  '| 案件 | 10000 shots 的 P(1)（理想值） | 校準 P(1\\|0)／P(0\\|1) | 嫌疑犯 |\n|---|---|---|---|\n'
  '| 沒有讀取錯誤 | 0.500 ± 0.005 | 0／0 | 只有運氣 |\n'
  '| 2%／8% | 0.470 | 0.02／0.08 | 讀取 |\n'
  '| 5%／15% | 0.450 | 0.05／0.15 | 讀取 |\n'
  '| 0%／10% | 0.450 | 0／0.10 | 讀取（只有 1 讀成 0） |\n\n'
  '## 常見誤解\n\n'
  '- 「shots 加倍，誤差減半」：要加 4 倍才減半（誤差 ∝ 1/√N）。\n'
  '- 「緩解什麼都能修」：只修讀取；閘錯誤、退相干都管不到。\n'
  '- 「緩解後一定更準」：中心值修回來了，但誤差範圍會變大，shots 要更多。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要帳號。

## `animations/operation.html#qubit`（場景 1：量子位元的狀態與測量）

- 「|+⟩」把箭頭放到赤道；「一次跑 1000 shots」一次累積 1000 次；「清除統計」歸零。
- 面板最下面的讀數「估計 P̂(1) = … ± …（1σ）」要捲動才看得到。
- 右下小圖：估計值隨 shots 收斂，灰帶 = ±1σ。

## `animations/operation.html#readout`（場景 7：讀取與統計，課綱指定）

- 滑桿「準備狀態 θ」「積分時間 τ」「兩團雲的間距」「判別閾值位置」；開關「讀取期間 T₁ 衰減」「讀取誤差緩解」。
- 面板最下面：混淆矩陣 P(1|0)、P(0|1)、讀取保真度，以及「未緩解／緩解後 P̂(1) → ⟨Z⟩（理想 …）」。
- 點的顏色是「判出」的結果；θ = 0° 時閾值右邊的紅點就是讀錯的。

## `animations/index.html#iq`（場景 10：IQ 判別）

- 每次隨機準備 0 或 1：藍＝準備 0、紅＝準備 1，就像校準線路。
- 左下讀數 P(判 1 | 備 0)、P(判 0 | 備 1) 就是混淆矩陣讀錯的兩格；關掉「包含讀取期間的 T1 衰減」，1 判成 0 會大幅下降。

## 操作

滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換場景。
''',
}

SHEET_HEADER = ['題號', '情境（出題者寫）', 'shots', '原始 P(1)', '誤差 σ', '偏離理想幾個 σ', '校準 P(1|0)', '校準 P(0|1)', '緩解後 P(1)', '嫌疑犯（運氣／儀器）']
SHEET_ROWS = [[str(k)] for k in range(1, 11)]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:4mm 5mm;height:56mm;text-align:center}
.cards h3{font-size:14pt;margin:0 0 2mm}.cards .big{font-size:22pt;font-weight:700;color:#0b2540;margin:2mm 0}.cards p{margin:1mm 0;font-size:11pt}
table.rc td{height:9.5mm;text-align:center}table.rc th{text-align:center;font-size:9.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.bt td,table.bt th{text-align:center;font-size:12pt}'''

CARDS = [('沒有讀取錯誤', 'P1_GIVEN_0 = 0、P0_GIVEN_1 = 0'), ('2%／8%', 'P1_GIVEN_0 = 0.02、P0_GIVEN_1 = 0.08'),
         ('5%／15%', 'P1_GIVEN_0 = 0.05、P0_GIVEN_1 = 0.15'), ('0%／10%', 'P1_GIVEN_0 = 0、P0_GIVEN_1 = 0.10'),
         ('沒有讀取錯誤 ②', 'P1_GIVEN_0 = 0、P0_GIVEN_1 = 0'), ('2%／8% ②', 'P1_GIVEN_0 = 0.02、P0_GIVEN_1 = 0.08')]


def html():
    cards = ''.join(f'<div class="cut"><h3>偵探案件卡</h3><p class="big">{k}</p><p>error_lab.py 改成：</p><p>{how}</p>'
                    '<p>對折蓋住，不給偵探看</p></div>' for k, how in CARDS)
    rows = ''.join(f'<tr><td>{k}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>□運氣 □儀器</td></tr>' for k in range(1, 11))
    pages = [
        '<h2>誤差速查卡</h2><p class="lead">量子結果要重複很多次（shots）再統計。偏差有兩種嫌疑犯：運氣（統計誤差）與儀器（讀取誤差）。</p>'
        '<table class="bt"><tr><th>shots N</th><th>σ（P = 0.5）</th><th>說明</th></tr>'
        '<tr><td>100</td><td>±0.050</td><td>約 ±5%</td></tr>'
        '<tr><td>1,000</td><td>±0.016</td><td>約 ±1.6%</td></tr>'
        '<tr><td>2,500</td><td>±0.010</td><td>±1% 要這麼多</td></tr>'
        '<tr><td>10,000</td><td>±0.005</td><td>約 ±0.5%</td></tr></table>'
        '<div class="box" style="margin-top:5mm"><h3>兩條公式</h3>'
        '<p style="font-size:15pt;font-weight:700">σ ＝ √(P(1−P)/N)　　N ＝ P(1−P) ÷ 誤差²</p>'
        '<p>shots ×4，誤差 ÷2；精度 ×10，shots ×100。期望值 ⟨Z⟩ 的誤差 ≈ 2σ。</p>'
        '<p style="font-size:14pt;font-weight:700">緩解：P_修正(1) ＝（P_量到(1) − P(1|0)）÷（P(1|1) − P(1|0)）</p>'
        '<p>例：（0.47 − 0.02）÷（0.92 − 0.02）＝ 0.45 ÷ 0.90 ＝ 0.50，等於乘上混淆矩陣的反矩陣 M⁻¹。</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>資料偵探規則</h3>'
        '<p>1. 出題者抽一張案件卡，照卡片偷偷改 error_lab.py 的讀取錯誤率。</p>'
        '<p>2. 偵探只能用兩種證據：加 shots 看偏差會不會變小；跑校準線路看 P(1|0)、P(0|1)。</p>'
        '<p>3. 判斷嫌疑犯是運氣還是儀器，再用緩解修回來；猜對換人出題。</p>'
        '<p class="note">提醒：shots 加 4 倍誤差才減半；緩解只修讀取，而且誤差會變大一點。</p></div>',
        '<h2>偵探案件卡</h2><p class="lead">沿虛線剪開，對折後蓋住。出題者照卡片改 error_lab.py（或 qiskit_readout.py 的 ReadoutError）。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>誤差緩解前後比較表</h2><p class="lead">每一題記下 shots、原始值、誤差、校準結果與緩解後的值。σ ＝ √(P(1−P)/N)。</p>'
        '<table class="rc"><tr><th>題</th><th>shots</th><th>原始<br>P(1)</th><th>誤差 σ</th><th>偏離<br>幾個 σ</th>'
        '<th>校準<br>P(1|0)</th><th>校準<br>P(0|1)</th><th>緩解後<br>P(1)</th><th>嫌疑犯</th></tr>'
        f'{rows}</table>'
        '<div class="box" style="margin-top:4mm"><p>改造：±1% 要幾次（先手算，再用程式核對）</p>'
        '<table class="bt"><tr><th>P</th><th>誤差</th><th>我算的 shots</th><th>程式算的 shots</th></tr>'
        '<tr><td>0.5</td><td>±0.01</td><td></td><td></td></tr><tr><td>0.1</td><td>±0.01</td><td></td><td></td></tr>'
        '<tr><td>⟨Z⟩</td><td>±0.01</td><td></td><td></td></tr></table></div>',
        '<h2>說明卡：我的誤差緩解前後比較</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. shots、統計誤差與讀取誤差緩解在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：統計誤差怎麼估？σ ＝ √(P(1−P)/N)</li>'
        '<li>說出為什麼 shots 加 4 倍，誤差才減半</li>'
        '<li>示範：跑校準線路量出混淆矩陣，再把結果修回來</li>'
        '<li>指出一個限制：緩解只修讀取，誤差範圍會變大</li>'
        '<li>替比較表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q059 shots、統計誤差與讀取誤差緩解 列印包', '父子科技學院 量子電腦學程 Q059｜shots、統計誤差與讀取誤差緩解', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q059-shots-readout-mitigation', folder='Q059_shots統計誤差與讀取誤差緩解', files=FILES,
        sheet=('03_誤差緩解前後比較表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_shots與讀取誤差緩解.pdf', pack_pages=4,
        pack_needles=('誤差速查卡', '偵探案件卡', '誤差緩解前後比較表', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q059', episode_dir='specials/q059-shots-readout-mitigation',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'error_lab.py', 'optionalProgram': 'qiskit_readout.py (qiskit 2.6.2, qiskit-aer 0.18.4)',
               'caseCards': [c[0] for c in CARDS], 'shotsTable': [100, 1000, 10000],
               'formulasFrom': 'slides/QC_Operation_Talk.pptx p32–33', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q059/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

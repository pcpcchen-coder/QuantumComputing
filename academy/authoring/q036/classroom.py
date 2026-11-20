"""Q036 課堂教材：手電筒紀錄、手繪 IQ 圖、改造單、說明卡（列印）、解答、iq_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（iq_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#iq。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q036/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q036：IQ 解調小工具。

不用安裝任何套件，只要 Python 3。執行：  python iq_check.py
- 一、解調：做一段 100 MHz 的中頻訊號 s(t) = A·cos(2π·f·t + φ)，每 1 ns 取樣一次（每秒十億次），取 200 ns；
  乘上 cos 加總得到 I、乘上 sin 加總得到 Q（學程簡報 JJ_Microwave_Readout_Talk p30 的公式，這裡權重 w(t) 取 1）。
  I = (2/N)·Σ s·cos(2πft)、Q = (2/N)·Σ s·sin(2πft)，算出來 I = A·cos φ、Q = −A·sin φ，所以 √(I² + Q²) = A。
- 二、混頻：7 GHz 的讀取訊號乘上 6.9 GHz 的本地振盪源，看乘積裡 0.1、6.9、7、13.9 GHz 各有多少。
- 三、正中間探測（上一堂 Q035，2χ = κ）：兩個狀態的穿透係數 S21 振幅一樣，但在 IQ 平面上的兩點距離是 1。
- 四、雲團：兩團中心距離 ÷（2 × 團寬 σ）＝ 訊雜比 SNR（簡報 p31；動畫 index.html#iq 的讀數同式），
  並印出手繪練習用的點（固定亂數種子，可重現）。
"""
import cmath
import math
import random


def demod(A, phi_deg, f=0.1, n=200):
    """f 以 GHz 為單位、每 1 ns 取一點，回傳 (I, Q)。"""
    phi = math.radians(phi_deg)
    s = [A * math.cos(2 * math.pi * f * t + phi) for t in range(n)]
    I = 2 / n * sum(v * math.cos(2 * math.pi * f * t) for t, v in enumerate(s))
    Q = 2 / n * sum(v * math.sin(2 * math.pi * f * t) for t, v in enumerate(s))
    return I, Q


print('一、解調：訊號的振幅 A、相位 φ → 算出的 I、Q → 從 I、Q 算回振幅與相位')
DEMOD = {}
for A, ph in ((1.0, 0), (1.0, 90), (1.0, 135), (0.5, 0), (0.5, 45), (0.8, -60)):
    I, Q = demod(A, ph)
    DEMOD[(A, ph)] = (I, Q)
    back = round(math.degrees(math.atan2(-Q, I)), 6) + 0.0
    print(f'  A = {A:.1f}、φ = {ph:+4d}° → I = {I:+.3f}、Q = {Q:+.3f} → 振幅 √(I²+Q²) = {math.hypot(I, Q):.3f}、相位 {back:+.1f}°')

print()
print('二、混頻：cos(2π·7t) × cos(2π·6.9t)，t 以 ns 為單位、每 0.005 ns 取一點、取 100 ns')
N2, DT = 20000, 0.005
prod = [math.cos(2 * math.pi * 7 * k * DT) * math.cos(2 * math.pi * 6.9 * k * DT) for k in range(N2)]
MIX = {}
for f in (0.1, 6.9, 7.0, 13.9):
    c = sum(v * cmath.exp(-2j * math.pi * f * k * DT) for k, v in enumerate(prod))
    MIX[f] = 2 * abs(c) / N2
    print(f'  {f:>5} GHz 的成分振幅：{MIX[f]:.3f}')
print('  → 剩下 0.1 GHz（差頻）和 13.9 GHz（和頻）各 0.5；和頻再用濾波器濾掉，就只剩 100 MHz 的中頻')

print()
print('三、正中間探測（χ/κ = 0.5，探測頻率在兩個諧振腔頻率正中間）')


def s21(probe, shift):
    return 1 / (1 + 2j * (probe - shift))


S0, S1 = s21(0, -0.5), s21(0, 0.5)
MID = (abs(S0), abs(S1), abs(S1 - S0), math.degrees(cmath.phase(S0)), math.degrees(cmath.phase(S1)))
print(f'  |0⟩：I = {S0.real:+.3f}、Q = {S0.imag:+.3f}，振幅 {abs(S0):.3f}、相位 {MID[3]:+.1f}°')
print(f'  |1⟩：I = {S1.real:+.3f}、Q = {S1.imag:+.3f}，振幅 {abs(S1):.3f}、相位 {MID[4]:+.1f}°')
print(f'  → 振幅一樣，只看振幅分不出來；兩點距離 {abs(S1 - S0):.3f}，在平面上分得很開')

print()
print('四、雲團：|0⟩ 中心 (−1.4, −0.7)、|1⟩ 中心 (+1.4, +0.7)，判別線是兩個中心的垂直平分線')
C0, C1 = (-1.4, -0.7), (1.4, 0.7)
D = math.dist(C0, C1)
SNR = {}
WRONG = {}
rng = random.Random(36)
for sig in (0.33, 1.25):
    SNR[sig] = D / (2 * sig)
    wrong = 0
    for k in range(2000):
        c = C0 if k % 2 == 0 else C1
        x, y = c[0] + rng.gauss(0, sig), c[1] + rng.gauss(0, sig)
        side = x * (C1[0] - C0[0]) + y * (C1[1] - C0[1])  # 投影到兩中心連線（中點在原點）
        wrong += (side > 0) if c is C0 else (side < 0)
    WRONG[sig] = wrong / 2000
    print(f'  團寬 σ = {sig}：訊雜比 = {D:.2f} ÷ (2 × {sig}) = {SNR[sig]:.1f}；2000 個點裡落錯邊的比例 {WRONG[sig] * 100:.1f} %')

print()
print('五、手繪練習的點（團寬 0.33，四捨五入到 0.1；每格 0.5）')
rng = random.Random(2036)
DRAW = []
for k in range(12):
    st = k % 2
    c = C1 if st else C0
    x, y = round(c[0] + rng.gauss(0, 0.33), 1), round(c[1] + rng.gauss(0, 0.33), 1)
    DRAW.append((st, x, y))
    print(f'  第 {k + 1:2d} 點：準備 |{st}⟩ → (I, Q) = ({x:+.1f}, {y:+.1f})')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'iq_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、動畫段、10_iq.js／09_dispersive.js 讀數相同
assert [f'{v:.3f}' for v in R['DEMOD'][(0.5, 45)]] == ['0.354', '-0.354']
assert [f'{v:.3f}' for v in R['DEMOD'][(0.8, -60)]] == ['0.400', '0.693']
assert f"{R['MIX'][0.1]:.3f}" == f"{R['MIX'][13.9]:.3f}" == '0.500' and f"{R['MIX'][7.0]:.3f}" == '0.000'
assert f"{R['MID'][0]:.3f}" == f"{R['MID'][1]:.3f}" == '0.707' and f"{R['MID'][2]:.3f}" == '1.000'
assert f"{R['SNR'][0.33]:.1f}" == '4.7' and f"{R['SNR'][1.25]:.1f}" == '1.3'
assert R['WRONG'][0.33] < 0.005 and 0.08 < R['WRONG'][1.25] < 0.13
assert all((x * 2.8 + y * 1.4 > 0) == bool(st) for st, x, y in R['DRAW'])  # 12 個練習點都沒有落錯邊

DRAW_ROWS = ''.join(f'<tr><td>{k}</td><td>|{st}⟩</td><td>{x:+.1f}</td><td>{y:+.1f}</td></tr>'
                    for k, (st, x, y) in enumerate(R['DRAW'], 1))


def grid_svg():
    """−3 到 +3、每格 0.5 的方格（12 × 12 格），中間粗線是 I 軸、Q 軸。"""
    s, n, o = 11.0, 12, 8.0  # 每格 11 mm
    lines = []
    for i in range(n + 1):
        w = 0.6 if i == n // 2 else 0.2
        c = '#333' if i == n // 2 else '#aaa'
        lines.append(f'<line x1="{o + i * s}" y1="{o}" x2="{o + i * s}" y2="{o + n * s}" stroke="{c}" stroke-width="{w}"/>')
        lines.append(f'<line x1="{o}" y1="{o + i * s}" x2="{o + n * s}" y2="{o + i * s}" stroke="{c}" stroke-width="{w}"/>')
    lab = []
    for i, v in ((0, '−3'), (2, '−2'), (4, '−1'), (8, '+1'), (10, '+2'), (12, '+3')):
        lab.append(f'<text x="{o + i * s}" y="{o + n * s + 5.5}" font-size="4" text-anchor="middle">{v}</text>')
        lab.append(f'<text x="{o - 2}" y="{o + (n - i) * s + 1.4}" font-size="4" text-anchor="end">{v}</text>')
    lab.append(f'<text x="{o + n * s + 1.5}" y="{o + 6 * s + 1.5}" font-size="5">I</text>')
    lab.append(f'<text x="{o + 6 * s + 1.5}" y="{o - 2}" font-size="5">Q</text>')
    W = o * 2 + n * s + 4
    return (f'<svg viewBox="0 0 {W} {W}" style="width:{W * 0.82:.0f}mm;height:{W * 0.82:.0f}mm;display:block;margin:0 auto">'
            + ''.join(lines) + ''.join(lab) + '</svg>')


FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q036：IQ 平面：把微波變成一個點（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。上一堂 Q035 看到：量子位元是 |0⟩ 或 |1⟩，穿過讀取諧振腔的探測微波，振幅和相位就不一樣。
這一堂要把那道微波變成「平面上的一個點」：讀取訊號先用外差的方法降到中頻、數位化，再乘上 cos 和 sin 加總（解調），得到 I（同相分量）和 Q（正交分量）兩個數字，
畫在 IQ 平面上就是一個點。好玩機制是「臨摹挑戰」：照著動畫場景親手畫出 IQ 圖。作品是「手繪 IQ 圖」。下一堂 Q037 是「單發判別與保真度」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 讀取鏈、外差降頻、手電筒類比、解調、一個點＝振幅＋相位；看 3D 動畫 | 影片第 2–8 段、`05_動畫導覽.md` |
| 25–65 | 手電筒畫圓、喊停量光點（列印包第 1 頁）；開場景臨摹，手繪 IQ 圖（列印包第 2 頁） | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子解釋：為什麼兩團點的距離比單看振幅更有用 | 列印包第 3 頁（改造單） |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替手繪圖取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_手繪IQ圖.pdf`（A4，共 4 頁）。另備手電筒、便利貼、捲尺或直尺、彩色筆（藍、紅、金或橘）。
- 讀一遍 `04_解答.md`；想多了解可以讀學程筆記 `notes/dispersive-readout.md` 的 §2.5 與 §4。
- 下載學程的 `animations/` 資料夾，用瀏覽器先開一次 `index.html#iq`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `iq_check.py`（不需要安裝套件）。

## 驗收重點

1. 完成「手繪 IQ 圖」：畫出 I、Q 兩條軸、藍點和紅點兩團、兩團中心和中間的判別線。
2. 不看稿說出核心原理：讀取微波先用外差降到中頻、數位化，再乘上 cos 和 sin 加總，得到 I、Q 兩個數字；畫成平面上一個點，離原點的距離是振幅、方向是相位。
3. 指出至少一個注意事項：I 與 Q 是同一個訊號的兩個分量，不是兩條不同的線。

## 誠實說明

- 約 7 GHz、約 100 MHz、約每秒十億次取樣是學程簡報 p30 的代表值，不同儀器規格不同。
- 手電筒畫圓是類比：光點的左右與上下位置錯開四分之一圈，用來說明「兩個分量合起來才是一個點」；真正的 I、Q 是解調後相對於參考波的兩個分量。
- 動畫裡的點雲是模擬，不是實驗數據；家裡沒有諧振腔和混頻器可以量，不要編造量測數據。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場一：手電筒畫圓（約 15 分鐘）

1. 房間調暗，爸爸站在牆前約 1.5 公尺，手電筒對著牆，手臂伸直、慢慢畫圓（大約 3 秒一圈），光點在牆上繞圈。
2. 先在牆上貼一張便利貼當「圓心」。孩子喊「停」，爸爸停住，孩子在光點位置貼一張便利貼。
3. 量這張便利貼離圓心「往右幾公分」（往左寫負數）和「往上幾公分」（往下寫負數），寫在列印包第 1 頁。喊停 6 次。
4. 討論：只看左右的數字，光點是不是來回擺動？只看上下呢？兩個數字合起來，才說得出光點在圓上的哪裡——這就是 I 和 Q 的意思。

## 上半場二：臨摹挑戰，手繪 IQ 圖（約 25 分鐘）

1. 用瀏覽器開 `animations/index.html#iq`，左邊面板往下捲到底，看到「量子極限放大器」「包含讀取期間的 T1 衰減」兩個開關、三個滑桿、「清除」按鈕和讀數。
2. 把「每秒量測次數」拉到 3 左右，看一條條細線從上方落下、越往下越收斂，落到平面上變成一個點（藍＝準備 |0⟩、紅＝準備 |1⟩）。
3. 按「清除」，把「每秒量測次數」拉到 30，等點累積成兩團。平面上的方格每格 0.5；橫的那條軸標著 I，往遠處延伸的那條軸標著 Q。
4. 在列印包第 2 頁的方格上臨摹：先數兩團中心各在第幾格，畫出 I、Q 軸、藍團、紅團和中間的金色判別線。也可以先畫第 2 頁表格裡的 12 個點練習。
5. 父子各畫一張，和畫面對照，看誰畫得最像（中心位置、團的大小、判別線方向）。

## 下半場：孩子改造——為什麼兩團點的距離比單看振幅更有用？（約 30 分鐘）

1. 用列印包第 3 頁的改造單。先回想 Q035：探測微波在兩個諧振腔頻率正中間時，兩種狀態的振幅一樣（0.707），只看振幅分不出來。
2. 看 `iq_check.py` 第三部分：同樣的振幅，在 IQ 平面上兩點的方向不同，距離是 1。
3. 回到 `index.html#iq`，按「量子極限放大器」把它關掉，看兩團變寬、混在一起，讀數裡的 SNR 從 4.7 變成 1.3；再打開。
4. 寫一段解釋：距離為什麼比振幅有用？距離又要跟什麼比（兩團的寬度）？
''',

'iq_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## iq_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 手電筒紀錄怎麼看\n\n'
  '- 每次喊停都會得到兩個數字（往右幾公分、往上幾公分）；兩個數字合起來才說得出光點在圓上的哪裡。\n'
  '- 光點離圓心的距離大約固定（手臂畫的圓），方向一直在轉：距離像振幅、方向像相位。\n'
  '- 只看左右（或只看上下）時，數字在正負之間來回，像一道波；兩道波錯開四分之一圈。\n\n'
  '## 手繪 IQ 圖參考\n\n'
  '- 動畫 `index.html#iq` 的點雲中心在程式裡是 (−1.4, 0.7) 和 (1.4, −0.7)（第二個數是平面縱深方向的座標，往觀眾這邊為正）；'
  '從畫面看：藍團在左、比較靠近觀眾，紅團在右、比較遠。把「遠方」當成方格紙的上方，藍團約在左下、紅團約在右上。\n'
  '- 判別線是兩團中心連線的垂直平分線，通過平面中心（金色線）。\n'
  '- 列印包第 2 頁的 12 個點：單數點（|0⟩）都在左下、雙數點（|1⟩）都在右上，沒有落錯邊。\n\n'
  '## 改造單參考答案\n\n'
  '- 正中間探測時兩態振幅都是 0.707，只看振幅分不出來；但 IQ 點一個在 (0.5, −0.5)、一個在 (0.5, +0.5)，相位差 90°，距離 1。'
  '平面上的點同時記住振幅和相位，所以比只看振幅多一份資訊。\n'
  '- 訊雜比＝兩團中心距離 ÷（2 × 團寬）：中心距離 √(2.8² + 1.4²) ≈ 3.13；團寬 0.33 → 3.13 ÷ 0.66 ≈ 4.7；團寬 1.25 → 3.13 ÷ 2.5 ≈ 1.3。\n'
  '- 距離一樣，團變寬時訊雜比變小，點容易落錯邊（iq_check.py 第四部分：團寬 1.25 時約一成落錯邊）。所以要看「距離比上寬度」。\n'
  '- 解調練習：A = 0.5、φ = 45° → I ≈ 0.354、Q ≈ −0.354（照本程式的參考波取法，Q 的正負號會跟著參考波的取法改變）；√(0.354² + 0.354²) ≈ 0.5。\n\n'
  '## 常見問題\n\n'
  '- 為什麼要先降頻？7 GHz 每秒振盪七十億次，直接取樣要非常快；降到約 100 MHz，每秒約十億次的取樣就夠（簡報 p30）。\n'
  '- 本地振盪源的頻率怎麼選？比諧振腔低一個中頻：ω_LO = ω_r − ω_IF（簡報 p30）。相乘後得到差頻和和頻，和頻用濾波器濾掉（iq_check.py 第二部分）。\n'
  '- 為什麼上變頻和下變頻要用同一個本地振盪源？相位才會一致（筆記 §4.1）。\n'
  '- 一定要用混頻器嗎？不一定。新一代儀器可以用高速 DAC 直接合成 GHz 訊號，省掉類比混頻器和 IQ 校正（周邊系統簡報 p21）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。
左邊面板很長，按鈕和滑桿在下方，要往下捲。

## `index.html#iq`（JJ 與微波讀取 3D 場景 10：單發讀取：IQ 叢集與狀態判別）＝本課主角

- 每一條細線是一次讀取的積分軌跡：從上方（時間 0）開始被雜訊淹沒到處亂跑，越往下越收斂，落到 IQ 平面上變成一個點。
- 點的顏色：藍＝準備 |0⟩、紅＝準備 |1⟩。點累積成兩團（「|0⟩ 叢集」「|1⟩ 叢集」），中間金色直線是判別閾值（兩團中心的垂直平分線）。
- 控制項：「量子極限放大器（JPA/TWPA）開啟」開關（關掉時兩團變寬）、「積分時間 τ_int」滑桿、「包含讀取期間的 T1 衰減」開關、「T1」滑桿、
  「每秒量測次數（動畫）」滑桿（2–60）、「清除」按鈕。改開關或前兩個滑桿都會把點清空、重新累積。
- 讀數：累積量測次數、兩種誤判比例、讀取保真度 F、SNR（兩團中心距離 ÷ 2σ）。右下角小圖是沿判別軸投影的直方圖。
- 保真度、判別閾值、T1 衰減是下一堂 Q037 的主角，本課先臨摹點和兩團。

## `index.html#dispersive`（JJ 與微波讀取 3D 場景 9：色散讀取）

- 右下角小圖是 IQ 平面：掃頻時穿透係數在平面上畫出一圈；藍點、紅點是兩個狀態在目前探測頻率下的位置。
- 拖動「探測頻率」滑桿，兩個點沿著這一圈移動；探測頻率離諧振腔很遠時，兩點都擠到這圈的左端（訊號很弱）。

## 之後的課

Q037「單發判別與保真度」會用閾值判別每一次讀取，算出讀取保真度，並認識 T₁ 造成的錯誤。
''',
}

SHEET_HEADER = ['喊停', '往右幾公分（左為負）', '往上幾公分（下為負）', '像時鐘的幾點鐘方向', '離圓心多遠']
SHEET_ROWS = [[str(k)] for k in range(1, 7)]

EXTRA_CSS = '''table.rec td{height:13mm;font-size:11pt;text-align:center}table.rec th{font-size:10pt}
table.pts td{height:6.2mm;font-size:10pt;text-align:center;padding:0 2mm}table.pts th{font-size:9.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.calc p{margin:2.2mm 0;font-size:12pt}.two{display:flex;gap:5mm;align-items:flex-start}'''


def html():
    rows = ''.join(f'<tr><td>{k}</td><td></td><td></td><td></td><td></td></tr>' for k in range(1, 7))
    pages = [
        '<h2>手電筒紀錄</h2><p class="lead">爸爸對著牆慢慢畫圓，孩子喊停，用便利貼標出光點，量它離圓心往右、往上各幾公分。</p>'
        '<table class="rec"><tr><th style="width:9%">喊停</th><th>往右幾公分<br>（左為負）</th><th>往上幾公分<br>（下為負）</th>'
        '<th>像時鐘的<br>幾點鐘方向</th><th>離圓心多遠</th></tr>' + rows + '</table>'
        '<div class="box calc" style="margin-top:4mm"><p>只看「往右」那一欄，數字是不是在正負之間來回？＿＿＿＿</p><p>只看「往上」那一欄呢？＿＿＿＿</p>'
        '<p>離圓心多遠，每次都差不多嗎？＿＿＿＿</p><p>離圓心多遠像訊號的＿＿＿＿；幾點鐘方向像訊號的＿＿＿＿。</p>'
        '<p>一句話：為什麼要兩個數字才說得出光點在哪裡？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>手繪 IQ 圖（臨摹挑戰）</h2><p class="lead">照著 index.html#iq 的畫面臨摹：每格 0.5，畫出藍團（|0⟩）、紅團（|1⟩）、兩團中心和判別線。</p>'
        '<div class="two"><div>' + grid_svg() + '</div>'
        '<div><table class="pts"><tr><th>點</th><th>準備</th><th>I</th><th>Q</th></tr>' + DRAW_ROWS + '</table>'
        '<p style="font-size:10pt;margin-top:2mm">先畫這 12 個練習點<br>（iq_check.py 第五部分），<br>再臨摹畫面上的兩團。</p></div></div>'
        '<p style="font-size:11pt;margin-top:2mm">藍團中心約在（＿＿，＿＿）；紅團中心約在（＿＿，＿＿）；作品名稱：＿＿＿＿＿＿＿＿</p>',
        '<h2>改造單：為什麼距離比振幅有用？</h2><p class="lead">用數字說明：兩團點的距離，為什麼比只看振幅更有用？</p>'
        '<div class="box calc"><h3>一、正中間的陷阱（上一堂 Q035）</h3>'
        '<p>探測在正中間：|0⟩ 的點 (0.5, −0.5)、|1⟩ 的點 (0.5, +0.5)。</p>'
        '<p>兩個點離原點的距離（振幅）各是＿＿＿＿、＿＿＿＿；一樣嗎？＿＿＿＿</p>'
        '<p>兩點之間的距離是＿＿＿＿；只看振幅分得出來嗎？＿＿＿＿　看平面上的點呢？＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>二、距離要比上團寬：訊雜比 ＝ 中心距離 ÷（2 × 團寬）</h3>'
        '<p>兩團中心距離約 3.13。放大器開著，團寬 0.33：訊雜比 ≈ ＿＿＿＿</p>'
        '<p>放大器關掉，團寬 1.25：訊雜比 ≈ ＿＿＿＿；哪一種比較容易落錯邊？＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>三、我的解釋</h3><p>＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>說明卡：我的手繪 IQ 圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. IQ 平面：把微波變成一個點在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出外差怎麼把微波降到中頻</li><li>說出解調怎麼得到 I、Q 兩個數字</li>'
        '<li>說出點的距離是振幅、方向是相位</li><li>說出 I、Q 不是兩條線</li>'
        '<li>示範一次手電筒畫圓</li><li>替手繪 IQ 圖取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q036 手繪 IQ 圖 列印包', '父子科技學院 量子電腦學程 Q036｜IQ 平面：把微波變成一個點', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q036-iq-plane', folder='Q036_IQ平面', files=FILES,
        sheet=('03_手電筒紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_手繪IQ圖.pdf', pack_pages=4,
        pack_needles=('手電筒紀錄', '手繪 IQ 圖', '改造單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q036', episode_dir='specials/q036-iq-plane',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（iq_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'iq_check.py',
               'recordedRun': {'demod_0.5_45': [round(v, 3) for v in R['DEMOD'][(0.5, 45)]],
                               'mix': {str(f): round(v, 3) for f, v in R['MIX'].items()},
                               'midpoint': [round(v, 3) for v in R['MID']],
                               'snr': {str(s): round(v, 2) for s, v in R['SNR'].items()},
                               'wrong_side': {str(s): v for s, v in R['WRONG'].items()},
                               'draw_points': R['DRAW']},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q036/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

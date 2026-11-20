"""Q037 課堂教材：保真度計算表、四種組合比較表、計算練習單、說明卡（列印）、解答、fidelity_calc.py、動畫導覽。

不需要帳號，也不需要安裝套件（fidelity_calc.py 只要 Python 3）；動畫用瀏覽器開啟 animations/operation.html#readout 與 animations/index.html#iq。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q037/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q037：保真度計算小工具。

不用安裝任何套件，只要 Python 3。執行：  python fidelity_calc.py
- 讀取保真度 F = 1 − [P(1|0) + P(0|1)] / 2（學程簡報 JJ_Microwave_Readout_Talk p31）。
  P(1|0)：準備 0 卻判成 1；P(0|1)：準備 1 卻判成 0。
- 二、三部分的模型和動畫 animations/operation.html#readout（js/operation/07_readout.js 第 51–62 行）相同：
  兩團雲中心在 ±0.65、寬度 σ = 0.715 / √(4τ)（τ 是積分時間，單位 μs）；閾值滑桿值 × 1.3 是閾值位置；
  T₁ = 50 μs，讀取途中衰減的 |1⟩ 會落在兩團之間。erf 用的是動畫裡同一個近似式，所以數字和讀數一樣。
- 一、手算保真度。二、移動閾值。三、改積分時間、開關 T₁ 衰減。四、盲測練習（固定亂數種子，可重現）。
"""
import math
import random


def erf(x):
    """與 07_readout.js 第 55 行相同的近似式。"""
    s = 1 if x >= 0 else -1
    x = abs(x)
    t = 1 / (1 + 0.3275911 * x)
    y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496735) * t + 0.254829592) * t * math.exp(-x * x)
    return s * y


def phi(x):
    return 0.5 * (1 + erf(x / math.sqrt(2)))


def fidelity(p10, p01):
    """兩種錯誤率（0～1）→ 讀取保真度。"""
    return 1 - (p10 + p01) / 2


def confusion(thr=0.0, tau=1.0, t1on=True, sep=1.0):
    """回傳 (P(1|0), P(0|1), F)，都是 0～1。"""
    scale, T1 = 1.3, 50
    c0, c1 = -sep * scale / 2, sep * scale / 2
    s = 0.55 * scale / math.sqrt(tau * 4)
    x = thr * scale
    p10 = 1 - phi((x - c0) / s)
    pd = 1 - math.exp(-tau / T1) if t1on else 0
    frac = min(1, max(0, (c1 - x) / (c1 - c0)))
    p11 = (1 - pd) * (1 - phi((x - c1) / s)) + pd * frac
    p01 = 1 - p11
    return p10, p01, fidelity(p10, p01)


def pct(v):
    return f'{v * 100:5.1f} %'


print('一、手算保真度')
EX = fidelity(0.02, 0.06)
print(f'  P(1|0) = 2 %、P(0|1) = 6 % → 平均錯誤 4 % → F = {EX * 100:.1f} %')

print()
print('二、移動閾值（積分時間 1 μs、T₁ 衰減開）')
THR = {}
for t in (-0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4):
    THR[t] = confusion(thr=t)
    p10, p01, f = THR[t]
    print(f'  閾值 {t:+.1f}：P(1|0) {pct(p10)}　P(0|1) {pct(p01)}　F {pct(f)}')

print()
print('三、積分時間與 T₁ 衰減（閾值 0）')
TAU = {}
for tau in (0.3, 0.5, 1.0, 2.0, 3.0, 4.0):
    TAU[tau] = (confusion(tau=tau), confusion(tau=tau, t1on=False))
    (a10, a01, af), (b10, b01, bf) = TAU[tau]
    print(f'  τ = {tau:.1f} μs：T₁ 開 P(1|0) {pct(a10)} P(0|1) {pct(a01)} F {pct(af)}｜T₁ 關 F {pct(bf)}')

print()
print('四、盲測練習（先自己猜閾值往哪邊偏，最後一行才是答案）')
rng = random.Random(37)
QUIZ = []
for k in range(1, 6):
    t = rng.choice((-0.3, -0.2, -0.1, 0.1, 0.2, 0.3))
    p10, p01, f = confusion(thr=t)
    QUIZ.append(t)
    print(f'  第 {k} 題：P(1|0) {pct(p10)}　P(0|1) {pct(p01)}　→ 閾值往哪邊偏？保真度多少？')
print('  答案：' + '、'.join(f'第 {k} 題 閾值 {t:+.1f}（{"往 |1⟩ 那團" if t > 0 else "往 |0⟩ 那團"}，F {confusion(thr=t)[2] * 100:.1f} %）'
                         for k, t in enumerate(QUIZ, 1)))
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'fidelity_calc.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()


def _p(v):
    return f'{v * 100:.1f}'


# 製作代理實跑（Python 3）：與旁白、動畫段、07_readout.js 讀數相同
assert f"{R['EX'] * 100:.0f}" == '96'
assert [_p(v) for v in R['THR'][0.0]] == ['3.5', '4.4', '96.1']
assert [_p(v) for v in R['THR'][0.3]] == ['0.2', '24.5', '87.7']
assert [_p(v) for v in R['THR'][-0.3]] == ['23.4', '0.6', '88.0']
assert [_p(v) for v in R['TAU'][1.0][1]] == ['3.5', '3.5', '96.5']
assert _p(R['TAU'][0.3][0][2]) == '83.9' and _p(R['TAU'][2.0][0][2]) == '98.5' and _p(R['TAU'][4.0][0][2]) == '98.1'
assert _p(R['TAU'][2.0][0][1]) == '2.4' and _p(R['TAU'][4.0][0][1]) == '3.9'

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q037：單發判別與保真度（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。上一堂我們知道每次讀取會變成 IQ 平面上的一個點；這一堂要決定這個點算 0 還是 1：
在兩團點中間畫一條「判別閾值」，落在哪一邊就判成哪個狀態。判錯有兩種：P(1|0)（準備 0 卻判成 1）和 P(0|1)（準備 1 卻判成 0），
讀取保真度 F = 1 − [P(1|0) + P(0|1)] / 2。好玩機制是「盲測」：爸爸偷偷移動閾值、遮住畫面，孩子只看兩種錯誤率猜閾值往哪邊偏。
作品是「保真度計算表」。下一堂 Q038 是「讀取鏈：衰減、環行器、放大器」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 單發讀取、判別閾值、兩種判錯、保真度公式、T₁ 造成的錯誤；看 3D 動畫 | 影片第 2–8 段、`05_動畫導覽.md` |
| 25–65 | 盲測：爸爸移動閾值並遮住畫面，孩子只看錯誤率猜偏向、算保真度（十回合） | 列印包第 1、3 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：index.html#iq 的放大器與 T1 衰減開關，四種組合比較 | 列印包第 2 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替保真度計算表取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_保真度計算表.pdf`（A4，共 4 頁）。另備一張紙（遮畫面用）、計算機或手機。
- 讀一遍 `04_解答.md`；想多了解可以讀學程筆記 `notes/dispersive-readout.md` 的 §2.5、§3。
- 下載學程的 `animations/` 資料夾，用瀏覽器先開一次 `operation.html#readout` 和 `index.html#iq`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `fidelity_calc.py`（不需要安裝套件）。

## 驗收重點

1. 完成「保真度計算表」：十回合都有兩種錯誤率、猜測、自己算的保真度，並和讀數對過答案。
2. 不看稿說出核心原理：每次讀取得到一個點，用兩團中心的垂直平分線當閾值判成 0 或 1；保真度是 1 減去兩種錯誤率的平均。
3. 指出至少一個注意事項：讀取時間拉久一點，兩團分得更開，但 T₁ 衰減也會增加，要找折衷。

## 誠實說明

- 動畫是示意模型：operation.html#readout 的 T₁ 固定 50 μs、積分時間 0.1–4 μs；index.html#iq 用相對單位。數字是模型算出來的，不是某台機器的量測值。
- index.html#iq 的錯誤率是隨機模擬的統計值，點少的時候會跳動；operation.html#readout 的錯誤率是公式值，不會跳動。
- 業界約 100–300 ns 做到 99 % 以上保真度，是學程筆記的代表值。家裡沒有量子電腦可以量，不要編造量測數據。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：盲測，填保真度計算表（約 40 分鐘）

1. 用瀏覽器開 `animations/operation.html#readout`，左邊面板往下捲到底，看到「判別閾值位置」滑桿、「讀取期間 T₁ 衰減」開關和讀數。
2. 先一起認識畫面：下方平面每個點是一次讀取；中間粉紅色的薄板是判別閾值，右邊的點塗紅色（判 1）、左邊塗藍色（判 0）。
   讀數第 3 行「混淆矩陣」寫著 P(1|0)、P(0|1) 和讀取保真度 F。
3. 盲測一回合：
   - 孩子轉過身。爸爸把「判別閾值位置」滑桿移到 −0.4～+0.4 之間的某個位置，在自己的紙上記下數值。
   - 爸爸用紙遮住滑桿數值、畫面中間的平面和右下角小圖，只露出讀數。
   - 孩子轉回來，只看 P(1|0) 和 P(0|1)：哪一種比較多？閾值往 |0⟩ 那團（負）還是 |1⟩ 那團（正）偏？寫下猜測。
   - 孩子自己算 F = 1 − [P(1|0) + P(0|1)] / 2，再和讀數的 F 對答案；爸爸掀開紙公布閾值。
4. 玩十回合。最後把閾值放回 0，看看保真度是不是比偏向任何一邊都高。
5. 沒有電腦時，可以用 `fidelity_calc.py` 第四部分的盲測題，或列印包第 3 頁的計算練習單。

## 下半場：孩子改造——放大器與 T1 衰減（約 30 分鐘）

1. 開 `animations/index.html#iq`，左邊面板往下捲，找到「量子極限放大器（JPA/TWPA）開啟」和「包含讀取期間的 T1 衰減」兩個開關（一開始都開著）。
2. 用列印包第 2 頁的比較表：四種組合（放大器開／關 × T1 衰減開／關）各跑至少 20 秒，讓點累積到 300 次以上，再記下兩種錯誤率、保真度和 SNR。
3. 比一比：關掉放大器時兩團雲有多寬？打開 T1 衰減時哪一種錯誤變多？
4. 加分題：回到 `operation.html#readout`，把「積分時間 τ」從 0.3 調到 4 μs，記下保真度，找出最好的讀取時間。
5. 寫一句結論：保真度最低的組合，是被哪一種錯誤拖低的？
''',

'fidelity_calc.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## fidelity_calc.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 盲測判讀規則（operation.html#readout，積分時間 1 μs、T₁ 衰減開）\n\n'
  '| 讀數看到 | 閾值往哪邊偏 |\n|---|---|\n'
  '| P(1\\|0) 比 P(0\\|1) 大很多 | 往 \\|0⟩ 那團（滑桿負值） |\n'
  '| P(0\\|1) 比 P(1\\|0) 大很多 | 往 \\|1⟩ 那團（滑桿正值） |\n'
  '| 兩個都很小（3.5 %、4.4 %） | 在中間附近（0），保真度最高 96.1 % |\n\n'
  '（數字與動畫 operation.html#readout 的公式相同，見 fidelity_calc.py。）\n\n'
  '## 四種組合參考答案（index.html#iq，積分時間 1、T1 = 8；統計值，點少時會跳動）\n\n'
  '| 放大器 | T1 衰減 | P(判 1｜備 0) | P(判 0｜備 1) | 保真度 | SNR |\n|---|---|---|---|---|---|\n'
  '| 開 | 開（預設） | 約 0 % | 約 7 % | 約 96–97 % | 4.7 |\n'
  '| 開 | 關 | 約 0 % | 約 0 % | 約 100 % | 4.7 |\n'
  '| 關 | 關 | 約 15 % | 約 15 % | 約 85 % | 1.3 |\n'
  '| 關 | 開 | 約 15 % | 約 18 % | 約 83 % | 1.3 |\n\n'
  '（製作代理以 10_iq.js 的公式在 Python 各模擬 3000 次估計；SNR 是公式值，不會跳動。）\n\n'
  '- 放大器關掉：雲的寬度從 0.33 變成 1.25（10_iq.js 第 55 行），兩團重疊，兩種錯誤都變多。\n'
  '- T1 衰減打開：只有準備 |1⟩ 的點會在途中掉回 |0⟩，所以 P(判 0｜備 1) 變多，P(判 1｜備 0) 幾乎不變。\n\n'
  '## 計算練習單答案\n\n'
  '- ① 2 % 與 6 % → F = 1 − 0.04 = 96 %。② 1 % 與 1 % → 99 %。③ 0.2 % 與 24.5 % → 平均 12.35 % → 約 87.7 %。\n'
  '- 閾值往 |1⟩ 那團移：P(1|0) 變少、P(0|1) 變多；往 |0⟩ 那團移：反過來。\n'
  '- 為什麼 P(0|1) 比較大：|1⟩ 會在讀取途中衰減回 |0⟩（T₁），|0⟩ 不會自己跳到 |1⟩（在這個模型裡）。\n'
  '- 讀取時間：積分久一點，雲變窄；但讀得太久，T₁ 衰減變多。fidelity_calc.py：τ 2 μs 98.5 %、4 μs 98.1 %。\n\n'
  '## 常見問題\n\n'
  '- 閾值為什麼畫在垂直平分線？兩團雲一樣寬、各佔一半時，垂直平分線讓兩種錯誤加起來最少（簡報 p31）。'
  '有 T₁ 衰減時，最好的位置會稍微往 |0⟩ 那團偏一點點（operation.html#readout 約在 −0.02～0）。\n'
  '- 為什麼讀數的 F 和我手算的差 0.1？讀數四捨五入到 0.1 %，用四捨五入後的錯誤率手算可能差一點點。\n'
  '- 真實機器還有哪些錯誤？一開始就沒準備好的熱激發、讀取微波太強造成的躍遷（簡報 p31）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。
左邊面板很長，按鈕和滑桿在下方，要往下捲。

## `operation.html#readout`（如何操作量子電腦 3D 場景 7：讀取）＝上半場主角

- 上排：準備的狀態（Bloch 球）→ 基底旋轉 → 讀取腔 → 放大器 → ADC + 積分；下方是 IQ 平面，每個點是一次讀取。
- 粉紅色薄板是判別閾值；點依「判別結果」上色：右邊紅（判 1）、左邊藍（判 0）。
- 滑桿：「判別閾值位置」（−1～1）、「積分時間 τ」（0.1～4 μs）、「兩團雲的間距」、「準備狀態 θ」；開關：「讀取期間 T₁ 衰減（T₁ = 50 μs）」「連續 shots」「讀取誤差緩解」。
- 讀數第 3 行：混淆矩陣 P(1|0)、P(0|1) 與讀取保真度 F（公式值，改設定立刻更新）。

## `index.html#iq`（JJ 與微波讀取 3D 場景 10：IQ 判別）＝下半場主角

- 每條細線是一次讀取，從上方（t = 0）落到 IQ 平面；點依「準備的狀態」上色：藍 = 準備 |0⟩、紅 = 準備 |1⟩；金色線是判別閾值。
- 開關：「量子極限放大器（JPA/TWPA）開啟」「包含讀取期間的 T1 衰減」；滑桿：積分時間、T1、每秒量測次數；「清除」按鈕。
- 讀數：累積量測次數、P(判 1｜備 0)、P(判 0｜備 1)、讀取保真度（統計值）、SNR。
- 右下角小圖：沿判別軸投影的直方圖（藍：製備 |0⟩，紅：製備 |1⟩）。

## 之後的課

Q038「讀取鏈：衰減、環行器、放大器」會沿著冷凍機看輸入線怎麼層層衰減、輸出線怎麼先用量子極限放大器再用 HEMT 放大。
''',
}

SHEET_HEADER = ['回合', '閾值（爸爸記）', 'P(1|0)', 'P(0|1)', '我猜偏向', '我算的 F', '讀數 F', '對嗎']
SHEET_ROWS = [[str(k)] for k in range(1, 11)]

EXTRA_CSS = '''table.rec td{height:12.5mm;font-size:11pt;text-align:center}table.rec th{font-size:10pt}
table.mod td{height:15mm;font-size:11pt;text-align:center}table.mod th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.calc p{margin:2.2mm 0;font-size:12pt}'''


def html():
    rows = ''.join(f'<tr><td>{k}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for k in range(1, 11))
    mod_rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td><td></td><td></td><td></td></tr>'
                       for a, b in (('開', '開（預設）'), ('開', '關'), ('關', '關'), ('關', '開')))
    pages = [
        '<h2>保真度計算表</h2><p class="lead">爸爸偷偷移動判別閾值並遮住畫面；孩子只看兩種錯誤率，猜閾值往哪邊偏，再算保真度。</p>'
        '<table class="rec"><tr><th style="width:7%">回合</th><th style="width:13%">閾值（爸爸記）</th><th style="width:11%">P(1|0)</th><th style="width:11%">P(0|1)</th>'
        '<th>我猜偏向（|0⟩／|1⟩）</th><th style="width:12%">我算的 F</th><th style="width:11%">讀數 F</th><th style="width:7%">對嗎</th></tr>' + rows + '</table>'
        '<p style="font-size:11pt;margin-top:3mm">F = 1 − [P(1|0) + P(0|1)] / 2。猜對＿＿＿／10 次。保真度最高的閾值是：＿＿＿＿</p>',
        '<h2>四種組合比較表</h2><p class="lead">開 index.html#iq，切換兩個開關；每種組合跑至少 20 秒（300 次以上）再記錄。</p>'
        '<table class="mod"><tr><th>量子極限放大器</th><th>T1 衰減</th><th>P(判 1｜備 0)</th><th>P(判 0｜備 1)</th><th>保真度</th><th>SNR</th></tr>' + mod_rows + '</table>'
        '<div class="box" style="margin-top:4mm"><p>保真度最高的是＿＿＿＿＿＿，最低的是＿＿＿＿＿＿。</p>'
        '<p>關掉放大器時兩團雲＿＿＿＿＿＿；打開 T1 衰減時，變多的是＿＿＿＿＿＿這一種錯誤。</p>'
        '<p>加分題：operation.html#readout 的積分時間 0.3／1／2／4 μs，保真度分別是＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>計算練習單</h2><p class="lead">沒有電腦也能練：用 F = 1 − [P(1|0) + P(0|1)] / 2 算保真度。</p>'
        '<div class="box calc"><h3>一、算保真度</h3>'
        '<p>① P(1|0) = 2 %、P(0|1) = 6 %：F = ＿＿＿＿</p>'
        '<p>② P(1|0) = 1 %、P(0|1) = 1 %：F = ＿＿＿＿</p>'
        '<p>③ P(1|0) = 0.2 %、P(0|1) = 24.5 %：F ≈ ＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>二、閾值往哪邊移</h3><p>把閾值往 |1⟩ 那團移，P(1|0) 會＿＿＿＿，P(0|1) 會＿＿＿＿。</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>三、T₁ 的錯誤</h3><p>為什麼 P(0|1) 常常比 P(1|0) 大？＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>讀取時間越久越好嗎？＿＿＿＿　理由：＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>說明卡：我的保真度計算表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 單發判別與保真度在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出閾值怎麼把一個點判成 0 或 1</li><li>說出保真度怎麼從兩種錯誤率算出來</li>'
        '<li>說出為什麼 P(0|1) 常常比較大</li><li>說出讀取時間拉久的好處和壞處</li>'
        '<li>示範一次盲測</li><li>替保真度計算表取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q037 保真度計算表 列印包', '父子科技學院 量子電腦學程 Q037｜單發判別與保真度', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q037-single-shot-fidelity', folder='Q037_單發判別與保真度', files=FILES,
        sheet=('03_保真度計算表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_保真度計算表.pdf', pack_pages=4,
        pack_needles=('保真度計算表', '四種組合比較表', '計算練習單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q037', episode_dir='specials/q037-single-shot-fidelity',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（fidelity_calc.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'fidelity_calc.py',
               'recordedRun': {'example_F': round(R['EX'], 4),
                               'threshold': {f'{t:+.1f}': [round(v * 100, 1) for v in R['THR'][t]] for t in R['THR']},
                               'tau_T1on': {str(t): [round(v * 100, 1) for v in R['TAU'][t][0]] for t in R['TAU']},
                               'tau_T1off_F': {str(t): round(R['TAU'][t][1][2] * 100, 1) for t in R['TAU']},
                               'quiz': R['QUIZ']},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q037/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

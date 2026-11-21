"""Q125 課堂教材：量測比較表、誤差範圍與次數估算單、改造紀錄、可執行的 shots_lab.py（純 Python）與選用的 qiskit_shots.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html（八個範例）與 operation.html#readout；shots_lab.py 只要 Python 3；
qiskit_shots.py 選用（pip install qiskit）。建置時會真的執行一次 shots_lab.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q125/classroom.py
"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，random.Random(1125)（固定種子，結果固定）
RUN_OUTPUT = '''一、八個範例：量 1 次與 1000 次（看第一個結果的比例）
  1 疊加｜理論 0：50%｜量 1 次 → 0｜量 1000 次 → 0 527 次（52.7%）｜差 2.7 點｜誤差範圍 ±1.6 點
  2 干涉｜理論 1：100%｜量 1 次 → 1｜量 1000 次 → 1 1000 次（100.0%）｜差 0.0 點｜誤差範圍 ±0.0 點
  3 Bell｜理論 00：50%｜量 1 次 → 11｜量 1000 次 → 00 494 次（49.4%）｜差 0.6 點｜誤差範圍 ±1.6 點
  4 GHZ｜理論 000：50%｜量 1 次 → 000｜量 1000 次 → 000 495 次（49.5%）｜差 0.5 點｜誤差範圍 ±1.6 點
  5 隱形傳態｜理論 0：75%｜量 1 次 → 0｜量 1000 次 → 0 728 次（72.8%）｜差 2.2 點｜誤差範圍 ±1.4 點
  6 Deutsch｜理論 1：100%｜量 1 次 → 1｜量 1000 次 → 1 1000 次（100.0%）｜差 0.0 點｜誤差範圍 ±0.0 點
  7 BV｜理論 101：100%｜量 1 次 → 101｜量 1000 次 → 101 1000 次（100.0%）｜差 0.0 點｜誤差範圍 ±0.0 點
  8 Grover｜理論 11：100%｜量 1 次 → 11｜量 1000 次 → 11 1000 次（100.0%）｜差 0.0 點｜誤差範圍 ±0.0 點
二、隱形傳態一路累加（q2 = 0 的比例，理論 75%）
  共     1 次  0 →    1 次（100.0%）  誤差範圍 ±43.3 點
  共    10 次  0 →    8 次（80.0%）  誤差範圍 ±13.7 點
  共   100 次  0 →   82 次（82.0%）  誤差範圍 ±4.3 點
  共  1000 次  0 →  756 次（75.6%）  誤差範圍 ±1.4 點
  共 10000 次  0 → 7526 次（75.3%）  誤差範圍 ±0.4 點
三、要幾次才能估到 ±2%？
  理論 50%：N = 0.5 × 0.5 ÷ 0.02² = 625 次
  理論 75%：N = 0.75 × 0.25 ÷ 0.02² = 469 次
  改造區：理論 50% 量 625 次，重複 200 輪：落在 ±2% 以內的有 137 輪（68%）
四、連續三次 0 之後，下一次是 1 的比例（一半一半）
  連續三次 0 出現 12628 回，下一次是 1 的有 6197 回（49.1%）
'''

# 製作代理實跑紀錄：qiskit 2.6.2（Python 3.13.18），StatevectorSampler(seed=1125)
QISKIT_OUTPUT = '''shots =     1  {'11': 1}  00 的比例 0.0%  誤差範圍 ±50.0%
shots =    10  {'00': 6, '11': 4}  00 的比例 60.0%  誤差範圍 ±15.8%
shots =   100  {'00': 54, '11': 46}  00 的比例 54.0%  誤差範圍 ±5.0%
shots =  1000  {'00': 512, '11': 488}  00 的比例 51.2%  誤差範圍 ±1.6%
shots = 10000  {'00': 4948, '11': 5052}  00 的比例 49.5%  誤差範圍 ±0.5%
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q125：量測 1 次與 1000 次（純 Python，不需要安裝任何套件）

執行：  python shots_lab.py
八個範例的理論機率抄自 basic-circuits.html（預設選項、最後一步）。程式只做「照理論機率抽樣」，印出：
  一、八個範例各量 1 次與 1000 次，和理論機率差多少、誤差範圍 σ = √(P(1−P)/N) 多大
  二、隱形傳態一路累加：1、10、100、1000、10000 次時的比例
  三、要幾次才能估到 ±2%：先用公式算，再把同樣的次數重複做 200 輪，數有幾輪落在 ±2% 以內（改造區可以改）
  四、連續三次 0 之後，下一次是 1 的比例（會不會「該輪到 1」？）
用固定的亂數種子，所以每次執行結果相同；改成 random.Random() 就每次不同（頁面的按鈕也是每次不同）。
"""
import random
from math import sqrt, ceil

# 範例名稱、量的位元、理論機率（頁面預設選項、最後一步）
EXAMPLES = [
    ('1 疊加', 'q0', {'0': 0.5, '1': 0.5}),
    ('2 干涉', 'q0', {'1': 1.0}),
    ('3 Bell', 'q1 q0', {'00': 0.5, '11': 0.5}),
    ('4 GHZ', 'q2 q1 q0', {'000': 0.5, '111': 0.5}),
    ('5 隱形傳態', 'q2', {'0': 0.75, '1': 0.25}),
    ('6 Deutsch', 'q0', {'1': 1.0}),
    ('7 BV', 'q2 q1 q0', {'101': 1.0}),
    ('8 Grover', 'q1 q0', {'11': 1.0}),
]


# 改造區：想估到多準（MY_ERR）、機率大約多少（MY_P）、重複幾輪（MY_ROUNDS）
MY_P, MY_ERR, MY_ROUNDS = 0.5, 0.02, 200


def shot(theory, rng):
    """照理論機率抽一個結果（和頁面的 sample() 同一種做法）"""
    r = rng.random()
    for key, p in theory.items():
        r -= p
        if r < 0:
            return key
    return key


def sigma(p, n):
    """n 次量測時，比例的誤差範圍（一個標準差）"""
    return sqrt(p * (1 - p) / n)


def need(p, err):
    """要估到 ±err（一個標準差），至少要量幾次"""
    return ceil(p * (1 - p) / err ** 2 - 1e-9)


if __name__ == '__main__':
    rng = random.Random(1125)   # 固定種子：教材的輸出才對得起來
    print('一、八個範例：量 1 次與 1000 次（看第一個結果的比例）')
    for name, bits, th in EXAMPLES:
        key = next(iter(th))
        one = shot(th, rng)
        n = sum(shot(th, rng) == key for _ in range(1000))
        f, p = n / 1000, th[key]
        print(f'  {name}｜理論 {key}：{p:.0%}｜量 1 次 → {one}｜量 1000 次 → {key} {n} 次（{f:.1%}）'
              f'｜差 {abs(f - p) * 100:.1f} 點｜誤差範圍 ±{sigma(p, 1000) * 100:.1f} 點')
    print('二、隱形傳態一路累加（q2 = 0 的比例，理論 75%）')
    zeros = total = 0
    for target in (1, 10, 100, 1000, 10000):
        while total < target:
            zeros += shot({'0': 0.75, '1': 0.25}, rng) == '0'
            total += 1
        print(f'  共 {total:>5} 次  0 → {zeros:>4} 次（{zeros / total:.1%}）  誤差範圍 ±{sigma(0.75, total) * 100:.1f} 點')
    print('三、要幾次才能估到 ±2%？')
    for p in (0.5, 0.75):
        print(f'  理論 {p:.0%}：N = {p:g} × {1 - p:g} ÷ 0.02² = {need(p, 0.02)} 次')
    N = need(MY_P, MY_ERR)
    inside = 0
    for _ in range(MY_ROUNDS):
        k = sum(rng.random() < MY_P for _ in range(N))
        inside += abs(k / N - MY_P) <= MY_ERR
    print(f'  改造區：理論 {MY_P:.0%} 量 {N} 次，重複 {MY_ROUNDS} 輪：落在 ±{MY_ERR:.0%} 以內的有 {inside} 輪（{inside / MY_ROUNDS:.0%}）')
    print('四、連續三次 0 之後，下一次是 1 的比例（一半一半）')
    seq = [rng.random() < 0.5 for _ in range(100000)]   # True 代表 1
    after = [seq[i] for i in range(3, len(seq)) if not (seq[i - 1] or seq[i - 2] or seq[i - 3])]
    print(f'  連續三次 0 出現 {len(after)} 回，下一次是 1 的有 {sum(after)} 回（{sum(after) / len(after):.1%}）')
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q125：用本機 Qiskit 量 Bell 態 1、10、100、1000、10000 次（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_shots.py
"""
from math import sqrt
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2, 2)
qc.h(0)                 # 哈達瑪閘
qc.cx(0, 1)             # 受控反閘：做出貝爾態
qc.measure([0, 1], [0, 1])

for shots in (1, 10, 100, 1000, 10000):
    counts = StatevectorSampler(seed=1125).run([qc], shots=shots).result()[0].data.c.get_counts()
    f = counts.get('00', 0) / shots
    print(f'shots = {shots:>5}  {dict(sorted(counts.items()))}  00 的比例 {f:.1%}  誤差範圍 ±{sqrt(0.25 / shots):.1%}')
'''

TABLE = [  # (範例, 量的位元, 理論機率, 類型, 1000 次誤差範圍 ±σ)
    ('1 疊加', 'q0', '0：50%、1：50%', '機率型', '±1.6 點'),
    ('2 干涉', 'q0', '1：100%', '確定型', '0'),
    ('3 Bell', 'q1 q0', '00：50%、11：50%', '機率型', '±1.6 點'),
    ('4 GHZ', 'q2 q1 q0', '000：50%、111：50%', '機率型', '±1.6 點'),
    ('5 隱形傳態', 'q2', '0：75%、1：25%', '機率型', '±1.4 點'),
    ('6 Deutsch', 'q0', '1：100%（預設 f(x) = x）', '確定型', '0'),
    ('7 BV', 'q2 q1 q0', '101：100%（預設密碼）', '確定型', '0'),
    ('8 Grover', 'q1 q0', '11：100%（2 顆、答案 11、1 輪）', '確定型', '0'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q125：量測 1 次與 1000 次（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的第十三課。
上一課（Q124）把八個範例搬到本機的 Qiskit；今天回到 basic-circuits.html，只研究量測卡的三個按鈕「量測 1 次」「量測 1,000 次」「清除」。
核心一句話：**量一次只告訴你這一次發生了什麼，量一千次才告訴你通常會發生什麼。** 好玩機制是「科學實驗」：先寫假設，再量，再拿數據和假設比。

## 八個範例的理論機率（量測比較表的答案欄）

| 範例 | 量的位元 | 理論機率（預設選項、最後一步） | 類型 | 1000 次的誤差範圍 |
|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in TABLE) + '''
- 確定型：理論機率 100% 集中在一個答案，量一次讀到的就是答案。
- 機率型：量一次只知道「這個結果會出現」，要量很多次才估得出機率。

## 統計誤差（QC_Operation_Talk.pptx 第 32 頁）

- 誤差範圍 σ = √(P(1−P)/N)。一半一半量 1000 次約 ±1.6 個百分點；75% 約 ±1.4；100% 是 0。
- σ 是「一個標準差」：大約三次裡有兩次落在 ±σ 內（常態近似）。所以偶爾超出一點是正常的。
- 倒過來算：N = P(1−P) ÷ 誤差²。一半一半估到 ±2% 要 625 次；75% 約 469 次；估到 ±1% 約 2,500 次（簡報的經驗法則）。
- 誤差減半，次數要四倍。

## 影片的念法

Bell 念「貝爾態」、Deutsch「德意志」、Grover「格羅弗」、BV「密碼範例」；q0、q2 念「編號零」「編號二」。旁白不念隨機出來的次數。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；孩子寫下假設 | 影片、列印包第 1 頁 |
| 10–25 | 對照簡報：basic-circuits.pptx 第 28 頁（量測 1 次或 1,000 次）、QC_Operation_Talk.pptx 第 32 頁（shots 與統計誤差） | 簡報 |
| 25–65 | 八個範例各量 1 次與 1000 次，填量測比較表、算差距、和誤差範圍比 | `01_操作步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子估算 ±2% 要幾次，跑 `shots_lab.py` 驗證 | 列印包第 3 頁、`03_量測比較表.csv` |
| 105–115 | 孩子教爸爸：量一次和量一千次各能告訴我們什麼、什麼時候量一次就夠、哪裡容易錯 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html`（任一範例），找到右下的量測卡。
- 選用：開 `operation.html#readout`（場景 7 讀取與統計），看 IQ 平面上一個點就是一次量測。
- 打開簡報 `slides/QC_Operation_Talk.pptx` 第 32 頁（課綱寫 p32，頁碼無誤），以及 `slides/output/basic-circuits.pptx` 第 28 頁。
- 列印 `02_列印包_量測比較表.pdf`（A4，共 4 頁），準備計算機。
- 有 Python 的電腦先跑一次 `python shots_lab.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_shots.py`（選用，不需帳號）。

## 誠實說明

- 頁面的「量測」是照理論機率抽樣的模擬，沒有雜訊；真實硬體還會有閘與讀取的錯誤（下一課 Q126 加入雜訊）。
- 「誤差範圍」一律指一個標準差；要 95% 把握（兩個標準差），±2% 需要約 2,500 次，本課不展開。
- 「三次裡約兩次」是常態近似；625 次一半一半落在 ±2% 內的精確機率是 66.3%。
- shots_lab.py 用固定亂數種子 1125，所以教材印出來的次數固定；頁面上的按鈕每次都不同。
- operation.html#readout 的雲、衰減與閾值是教學模擬，不代表特定硬體的數值。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：八個範例各量 1 次與 1000 次（約 40 分鐘）

1. 打開 `animations/basic-circuits.html`，從「範例 1 疊加」開始。換範例時頁面回到起點：點電路下方小圓點的**最後一個**（或按「下一步 ▶」走到底），停在最後一步。
2. 按一次「量測 1 次」：綠框「最近一次」只顯示一個結果（量一顆時寫成 `q2 = 0`，量多顆時是整串位元）。抄進量測比較表的「量 1 次」欄。
3. 按「清除」，再按「量測 1,000 次」：每個結果一列，灰色底是理論機率，綠色條是實際比例，右邊寫次數（百分比）；最下面一行「共 1,000 次；理論：…」。
4. 把第一個結果的百分比抄下來，和理論機率相減，寫進「差距」欄。
5. 把差距和誤差範圍比：一半一半 ±1.6、75% ±1.4、100% 是 0。在範圍內打勾；超出的話，按清除再量一回 1000 次，看看是不是運氣差（大約三次有一次會超出）。
6. 八個範例都做完，數一數：哪些量一次就夠（確定型）？哪些要量很多次（機率型）？

## 小提醒

- 量測會一直累加；換範例、換選項、移動步驟就歸零，「清除」也會歸零。
- 「量測 1,000 次」約 0.75 秒跑完，跑的時候再按不會多算。
- 想看比例怎麼慢慢穩下來：在隱形傳態連按 8 次「量測 1 次」，再按三次「量測 1,000 次」，記下每次的百分比（共 1,008、2,008、3,008 次）。

## 下半場：估算要量幾次（約 30 分鐘）

1. 在列印包第 3 頁用 N = P(1−P) ÷ 0.02² 算：一半一半、75% 各要幾次才能估到 ±2%？
2. 執行 `python shots_lab.py`，看第三段：公式的答案和程式一樣嗎？625 次重複 200 輪，有幾輪落在 ±2% 內？
3. 改 `shots_lab.py` 上面的改造區 `MY_P, MY_ERR, MY_ROUNDS`，例如 `0.75, 0.02, 200` 或 `0.5, 0.01, 200`，先預測再執行。
4. 有裝 Qiskit 的話，跑 `qiskit_shots.py`，看貝爾態 1、10、100、1000、10000 次的比例。

## 選用：讀取與統計（operation.html#readout）

- 每個點是一次量測，依粉紅色閾值判成 0（藍）或 1（紅）。把「積分時間 τ」拉到 0.10 μs，兩團雲變胖重疊，讀取保真度 F 從 96.1% 掉到 71.7%。
- 關掉「讀取誤差緩解」，看「未緩解 P̂(1)」和「理想 P(1) = 0.329」差多少；讓它多跑一會兒，差距會不會消失？
''',

'shots_lab.py': PROGRAM,
'qiskit_shots.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## shots_lab.py 實跑輸出（Python 3.13.18，random.Random(1125)，結果固定）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_shots.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=1125）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- 量一次能告訴我們什麼？只有「這個結果會出現」。比例不是 0% 就是 100%，不能代表機率。\n'
  '- 什麼時候量一次就夠？理論機率 100% 集中在一個答案時：干涉、Deutsch、BV、兩顆位元的 Grover。\n'
  '- 為什麼疊加量 1000 次差了 2.7 點，超過 ±1.6？±1.6 是一個標準差，大約三次有一次會超出；再量一回通常就回到範圍內。\n'
  '- 估到 ±2% 要幾次？一半一半 0.25 ÷ 0.0004 = 625；75% 是 0.1875 ÷ 0.0004 ≈ 469。625 次重複 200 輪，137 輪（68%）落在 ±2% 內，理論約 66%。\n'
  '- 連續三次 0 之後，下一次比較容易出 1 嗎？不會。程式裡 12,628 回連續三次 0 之後，下一次是 1 的比例 49.1%，仍然大約一半。\n'
  '- 為什麼讀取場景多量也去不掉偏差？那是讀取判錯造成的系統偏差，不是隨機誤差；要靠校準（混淆矩陣）來緩解，而緩解又會讓需要的次數變多（簡報第 32、33 頁）。\n'
  '- 下一課：在本機模擬器加入雜訊，八個範例的結果會怎樣變差？先預測，Q126 揭曉。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html`（八個範例）

- 上方分頁切換八個範例（網址後面的 `#superposition`、`#interference`、`#bell`、`#ghz`、`#teleport`、`#deutsch`、`#bv`、`#grover`）。換範例時回到起點。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」；電路下方的小圓點，一個點一步，最後一個點就是最後一步。
- 量測卡：「量測 1 次」「量測 1,000 次」「清除」；「最近一次：」綠框；每列灰色底是理論機率、綠色是實際比例，右邊「次數（百分比）」；最下面「共 N 次；理論：…」。
- 量測會累加；換步驟、換選項、換範例都會歸零。

## `animations/operation.html#readout`（場景 7：讀取與統計）

- IQ 平面「每個點 = 一個 shot」；粉紅色平面是閾值，判成 0 藍、判成 1 紅；右下小圖是 IQ 點投影到 I 軸的分佈。
- 滑桿「準備狀態 θ」（預設 70°，理想 P(1) = 0.329）「積分時間 τ」「兩團雲的間距」「判別閾值位置」；開關「連續 shots」「讀取期間 T₁ 衰減」「讀取誤差緩解」。
- 左側面板要捲到底，才看得到 shots N、混淆矩陣、讀取保真度 F 與估計值。

## `animations/operation.html#qubit`（場景 1：狀態與測量）

- 說明寫著「誤差約 √(p(1−p)/N)，要精度提高 10 倍就要 100 倍的 shots」；面板「估計 P̂(1) = … ± …（1σ）」。
''',
}

SHEET_HEADER = ['範例', '理論機率（第一個結果）', '量 1 次的結果', '量 1000 次的比例', '差距（點）', '誤差範圍 ±σ', '在範圍內嗎', '類型（確定／機率）', '備註']
SHEET_ROWS = [['範例：shots_lab.py 1 疊加', '0：50%', '0', '52.7%', '2.7', '±1.6', '超出', '機率型', '再量一回看看'],
              ['範例：shots_lab.py 7 BV', '101：100%', '101', '100.0%', '0.0', '0', '是', '確定型', '量一次就夠'],
              ['1 疊加', '', '', '', '', '', '', '', ''], ['2 干涉', '', '', '', '', '', '', '', ''],
              ['3 Bell', '', '', '', '', '', '', '', ''], ['4 GHZ', '', '', '', '', '', '', '', ''],
              ['5 隱形傳態', '', '', '', '', '', '', '', ''], ['6 Deutsch', '', '', '', '', '', '', '', ''],
              ['7 BV', '', '', '', '', '', '', '', ''], ['8 Grover', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:9.5mm;font-size:10.5pt}table.judge td.k{font-weight:bold;color:#0b2540;width:16%}
table.judge th{font-size:10pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 shots_lab.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'shots_lab.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    assert 'N = 0.5 × 0.5 ÷ 0.02² = 625 次' in out and '469 次' in out
    return out


def html():
    names = ['1 疊加', '2 干涉', '3 Bell', '4 GHZ', '5 隱形傳態', '6 Deutsch', '7 BV', '8 Grover']
    rows = ''.join(f'<tr><td class="k">{n}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for n in names)
    pages = [
        '<h2>量測比較表</h2><p class="lead">假設：量一次靠運氣；量一千次會靠近理論機率，但不會剛好相等。每個範例都走到最後一步再量。</p>'
        '<table class="judge"><tr><th>範例</th><th>理論機率（第一個結果）</th><th>量 1 次</th><th>量 1000 次的比例</th><th>差距</th><th>±σ</th><th>在範圍內？</th></tr>'
        + rows + '</table>'
        '<p class="note">±σ：一半一半 1.6、75% 1.4、100% 是 0（單位：百分點）。超出的話按清除再量一回。</p>'
        '<p>結論：確定型的範例有＿＿＿＿＿＿＿＿＿＿；機率型的範例有＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>誤差範圍與累加紀錄</h2><p class="lead">σ = √(P(1−P)/N)：機率乘上（1 − 機率），除以次數，再開根號。</p>'
        '<table class="judge"><tr><th style="width:22%">理論機率 P</th><th>N = 100</th><th>N = 1000</th><th>N = 10000</th></tr>'
        '<tr><td class="k">50%（一半一半）</td><td></td><td>±1.6</td><td></td></tr>'
        '<tr><td class="k">75%（隱形傳態）</td><td></td><td>±1.4</td><td></td></tr>'
        '<tr><td class="k">100%（確定型）</td><td></td><td></td><td></td></tr></table>'
        '<p>隱形傳態累加紀錄（連按 8 次量測 1 次，再按三次量測 1,000 次）：</p>'
        '<table class="judge"><tr><th style="width:22%">共幾次</th><th>q2 = 0 的比例</th><th>和 75% 差幾點</th></tr>'
        '<tr><td class="k">8</td><td></td><td></td></tr><tr><td class="k">1,008</td><td></td><td></td></tr>'
        '<tr><td class="k">2,008</td><td></td><td></td></tr><tr><td class="k">3,008</td><td></td><td></td></tr></table>'
        '<p>比例什麼時候開始不再大跳？</p><div class="line"></div>',
        '<h2>換你改造：估算要量幾次</h2><p class="lead">先用公式算，再跑 shots_lab.py 驗證。N = P(1−P) ÷ 誤差²</p>'
        '<table class="judge"><tr><th style="width:24%">情況</th><th>我算的 N</th><th>程式算的 N</th><th>落在範圍內的輪數</th></tr>'
        '<tr><td class="k">50%，±2%</td><td></td><td></td><td>＿＿／200</td></tr>'
        '<tr><td class="k">75%，±2%</td><td></td><td></td><td>＿＿／200</td></tr>'
        '<tr><td class="k">50%，±1%</td><td></td><td></td><td>＿＿／200</td></tr>'
        '<tr><td class="k">我的設定：</td><td></td><td></td><td>＿＿／＿＿</td></tr></table>'
        '<pre class="code"># shots_lab.py 上面的改造區\n'
        'MY_P, MY_ERR, MY_ROUNDS = 0.5, 0.02, 200   # 改成你的設定，例如 0.75, 0.02, 200\n'
        '# MY_P 機率、MY_ERR 想估到多準、MY_ROUNDS 重複幾輪</pre>'
        '<p>誤差從 ±2% 變成 ±1%，次數變成幾倍？落在範圍內的比例有沒有變？</p><div class="line"></div><div class="line"></div>',
        '<h2>最後一關：科學實驗報告</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 量一次和量一千次，各能告訴我們什麼（不看稿）：</p><div class="line"></div>'
        '<p>2. 什麼樣的範例量一次就夠：</p><div class="line"></div>'
        '<p>3. 一個注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：量一次只拿到一個結果，比例不是 0% 就是 100%</li><li>說出：理論 100% 集中在一個答案時，量一次就夠</li>'
        '<li>指出：1000 次的比例仍有約 ±1.6% 的統計誤差</li><li>完成量測比較表，八個範例都有差距和 ±σ</li>'
        '<li>用公式算出 ±2% 要 625 次，並用 shots_lab.py 驗證</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q125 量測比較表 列印包', '父子科技學院 量子電腦學程 Q125｜量測 1 次與 1000 次', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q125-one-vs-thousand', folder='Q125_量測1次與1000次', files=FILES,
        sheet=('03_量測比較表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量測比較表.pdf', pack_pages=4,
        pack_needles=('量測比較表', '誤差範圍與累加紀錄', '估算要量幾次', 'MY_ROUNDS', '最後一關'),
        authoring_dir=XINEW / 'authoring/q125', episode_dir='specials/q125-one-vs-thousand',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；shots_lab.py 只需 Python 3；qiskit_shots.py 選用：pip install qiskit）',
               'program': 'shots_lab.py', 'optionalProgram': 'qiskit_shots.py',
               'testedWith': 'Python 3.13.18 (standard library only, random seed 1125); qiskit 2.6.2 (StatevectorSampler seed=1125)',
               'recordedRun': {'sigma1000': {'p50': '±1.6', 'p75': '±1.4', 'p100': '0'},
                               'needFor2pct': {'p50': 625, 'p75': 469},
                               'rounds625': {'inside': 137, 'of': 200, 'exactBinomial': 0.663},
                               'afterThreeZeros': {'cases': 12628, 'nextIsOne': 6197, 'fraction': 0.491},
                               'qiskitBell': {'1': {'11': 1}, '10': {'00': 6, '11': 4}, '100': {'00': 54, '11': 46},
                                              '1000': {'00': 512, '11': 488}, '10000': {'00': 4948, '11': 5052}}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q125/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

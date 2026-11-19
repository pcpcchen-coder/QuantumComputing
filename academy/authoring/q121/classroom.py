"""Q121 課堂教材：Grover 逐步圖（四根柱子＋平均值虛線）、換答案預測表、離平均多遠對照單、可執行的 grover_mean.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#grover、transmon-3d.html#grover 與 operation.html#grover；grover_mean.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 grover_mean.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \\
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q121/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，沒有亂數
RUN_OUTPUT = '''一、兩顆位元、答案 01（振幅順序 00 01 10 11）
  ①哈達瑪閘：+0.50 +0.50 +0.50 +0.50   平均 +0.50   答案的機率 25.0%
  ②標記    ：+0.50 −0.50 +0.50 +0.50   平均 +0.25   答案的機率 25.0%
  ③擴散    ：+0.00 +1.00 +0.00 +0.00   平均 +0.25   答案的機率 100.0%
  標記後離平均：其他三根 +0.25（在平均上面），答案 −0.75（在平均下面）
  擴散後離平均：其他三根 −0.25，答案 +0.75：離多遠，就翻到另一邊多遠
二、沒有標記就擴散
  擴散前：+0.50 +0.50 +0.50 +0.50   平均 +0.50
  擴散後：+0.50 +0.50 +0.50 +0.50   每根都站在平均線上，一動也不動
三、四種答案都試一次
  答案 00：標記後平均 +0.25；一輪後 +1.00 +0.00 +0.00 +0.00   答案的機率 100%
  答案 01：標記後平均 +0.25；一輪後 +0.00 +1.00 +0.00 +0.00   答案的機率 100%
  答案 10：標記後平均 +0.25；一輪後 +0.00 +0.00 +1.00 +0.00   答案的機率 100%
  答案 11：標記後平均 +0.25；一輪後 +0.00 +0.00 +0.00 +1.00   答案的機率 100%
四、用真正的閘接出擴散（H、X、CZ、X、H）
  答案 00：閘電路 −1.00 +0.00 +0.00 +0.00   理想 +1.00 +0.00 +0.00 +0.00   整體差一個負號：是；機率相同
  答案 01：閘電路 +0.00 −1.00 +0.00 +0.00   理想 +0.00 +1.00 +0.00 +0.00   整體差一個負號：是；機率相同
  答案 10：閘電路 +0.00 +0.00 −1.00 +0.00   理想 +0.00 +0.00 +1.00 +0.00   整體差一個負號：是；機率相同
  答案 11：閘電路 +0.00 +0.00 +0.00 −1.00   理想 +0.00 +0.00 +0.00 +1.00   整體差一個負號：是；機率相同
五、選項變多：4 顆位元、16 個選項、答案是編號 6
  一開始：每根 +0.25，答案的機率 6.25%
  第 1 輪：標記後平均 +0.219，答案在平均下面 0.47；擴散後答案 +0.688（機率 47.3%），其他每根 +0.188
  第 2 輪：標記後平均 +0.133，答案在平均下面 0.82；擴散後答案 +0.953（機率 90.8%），其他每根 +0.078
六、改造區
  我的答案 11：標記後 +0.50 +0.50 +0.50 −0.50，平均 +0.25
  一輪後 +0.00 +0.00 +0.00 +1.00；量到 11 的機率 100%
'''

# 製作代理實跑紀錄：qiskit 2.6.2，Statevector（振幅）與 StatevectorSampler(seed=2026)，shots=1000（理想模擬，每個答案都是 100%，次數不隨種子改變）
QISKIT_OUTPUT = '''答案 00：振幅 -1.00 +0.00 +0.00 +0.00　量 1000 次 {'00': 1000}
答案 01：振幅 +0.00 -1.00 +0.00 +0.00　量 1000 次 {'01': 1000}
答案 10：振幅 +0.00 +0.00 -1.00 +0.00　量 1000 次 {'10': 1000}
答案 11：振幅 +0.00 +0.00 +0.00 -1.00　量 1000 次 {'11': 1000}
        ┌───┐        ┌───┐┌───┐        ┌───┐┌───┐ ░ ┌─┐   
   q_0: ┤ H ├──────■─┤ H ├┤ X ├──────■─┤ X ├┤ H ├─░─┤M├───
        ├───┤┌───┐ │ ├───┤├───┤┌───┐ │ ├───┤├───┤ ░ └╥┘┌─┐
   q_1: ┤ H ├┤ X ├─■─┤ X ├┤ H ├┤ X ├─■─┤ X ├┤ H ├─░──╫─┤M├
        └───┘└───┘   └───┘└───┘└───┘   └───┘└───┘ ░  ║ └╥┘
meas: 2/═════════════════════════════════════════════╩══╩═
                                                     0  1 
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q121：範例 8 Grover——對平均值翻轉（純 Python，不需安裝任何套件）

執行：  python grover_mean.py
它印出：
  一、兩顆位元、答案 01：每一步的四個振幅、平均值、每根柱子離平均多遠
  二、沒有標記就擴散：每根柱子都站在平均線上，翻完一動也不動
  三、四種答案都試一次：標記後的平均、一輪後的柱子
  四、用真正的閘（哈達瑪閘、翻轉閘、受控相位翻轉閘）接出擴散：多一個整體負號，機率不變
  五、選項變多（4 顆位元、16 個選項）：一輪拉不滿，第二輪答案離平均更遠
  六、改造區：換成自己的答案，先預測，再執行
位元字串寫成 q1 q0（最右邊是 q0），和 basic-circuits.html#grover、Qiskit 一樣。
"""
from math import sqrt

ANSWER = '01'      # 影片和教材用的答案


def show(v):
    return ' '.join(f'{a + 0.0:+.2f}'.replace('-', '−') for a in v)


def sg(a):
    return f'{a + 0.0:+.2f}'.replace('-', '−')


def mean(v):
    return sum(v) / len(v)


def uniform(n):
    """每顆位元都做哈達瑪閘之後：每個振幅都是 1/√N"""
    N = 2 ** n
    return [1 / sqrt(N)] * N


def mark(v, t):
    """標記：只把答案的振幅變號，其他不動"""
    w = v[:]
    w[int(t, 2)] = -w[int(t, 2)]
    return w


def diffuse(v):
    """擴散：每個振幅對平均值翻轉，新振幅 = 2 × 平均 − 原振幅"""
    m = mean(v)
    return [2 * m - a for a in v]


# ---- 第四段用：一顆一顆閘作用在兩顆位元上（索引 = q1 q0） ----
def h(v, q):
    m, w = 1 << q, v[:]
    for i in range(4):
        if not i & m:
            a, b = v[i], v[i | m]
            w[i], w[i | m] = (a + b) / sqrt(2), (a - b) / sqrt(2)
    return w


def x(v, q):
    m, w = 1 << q, v[:]
    for i in range(4):
        if not i & m:
            w[i], w[i | m] = v[i | m], v[i]
    return w


def cz(v):
    w = v[:]
    w[3] = -w[3]
    return w


def gate_round(t):
    """真正的閘：H、H；標記 = 對 0 的那一位做 X → CZ → X；擴散 = H、X、CZ、X、H"""
    v = [1.0, 0.0, 0.0, 0.0]
    v = h(h(v, 0), 1)
    zeros = [q for q in (0, 1) if t[1 - q] == '0']
    for q in zeros:
        v = x(v, q)
    v = cz(v)
    for q in zeros:
        v = x(v, q)
    for g in (h, x):
        v = g(g(v, 0), 1)
    v = cz(v)
    for g in (x, h):
        v = g(g(v, 0), 1)
    return v


def clean(v):
    return [0.0 if abs(a) < 1e-12 else a for a in v]


if __name__ == '__main__':
    print(f'一、兩顆位元、答案 {ANSWER}（振幅順序 00 01 10 11）')
    i = int(ANSWER, 2)
    v1 = uniform(2)
    v2 = mark(v1, ANSWER)
    v3 = diffuse(v2)
    for name, v in (('①哈達瑪閘', v1), ('②標記    ', v2), ('③擴散    ', v3)):
        print(f'  {name}：{show(v)}   平均 {mean(v):+.2f}   答案的機率 {v[i] ** 2:.1%}')
    m = mean(v2)
    print(f'  標記後離平均：其他三根 {sg(v2[(i + 1) % 4] - m)}（在平均上面），答案 {sg(v2[i] - m)}（在平均下面）')
    print(f'  擴散後離平均：其他三根 {sg(v3[(i + 1) % 4] - m)}，答案 {sg(v3[i] - m)}：離多遠，就翻到另一邊多遠')

    print('二、沒有標記就擴散')
    print(f'  擴散前：{show(v1)}   平均 {mean(v1):+.2f}')
    print(f'  擴散後：{show(diffuse(v1))}   每根都站在平均線上，一動也不動')

    print('三、四種答案都試一次')
    for t in ('00', '01', '10', '11'):
        a = mark(uniform(2), t)
        b = clean(diffuse(a))
        print(f'  答案 {t}：標記後平均 {mean(a):+.2f}；一輪後 {show(b)}   答案的機率 {b[int(t, 2)] ** 2:.0%}')

    print('四、用真正的閘接出擴散（H、X、CZ、X、H）')
    for t in ('00', '01', '10', '11'):
        g = clean(gate_round(t))
        ideal = clean(diffuse(mark(uniform(2), t)))
        same = all(abs(p * p - q * q) < 1e-12 for p, q in zip(g, ideal))
        print(f'  答案 {t}：閘電路 {show(g)}   理想 {show(ideal)}   '
              f'整體差一個負號：{"是" if all(abs(p + q) < 1e-12 for p, q in zip(g, ideal)) else "否"}；機率{"相同" if same else "不同"}')

    print('五、選項變多：4 顆位元、16 個選項、答案是編號 6')
    v = uniform(4)
    print(f'  一開始：每根 {v[0]:+.2f}，答案的機率 {v[6] ** 2:.2%}')
    for r in (1, 2):
        a = mark(v, format(6, '04b'))
        m = mean(a)
        v = diffuse(a)
        print(f'  第 {r} 輪：標記後平均 {m:+.3f}，答案在平均下面 {m - a[6]:.2f}；'
              f'擴散後答案 {v[6]:+.3f}（機率 {v[6] ** 2:.1%}），其他每根 {v[0]:+.3f}')

    # 六、改造區：換成自己的答案（兩位，只寫 0 和 1），先預測，再執行
    MY_ANSWER = '11'
    a = mark(uniform(2), MY_ANSWER)
    b = clean(diffuse(a))
    print('六、改造區')
    print(f'  我的答案 {MY_ANSWER}：標記後 {show(a)}，平均 {mean(a):+.2f}')
    print(f'  一輪後 {show(b)}；量到 {MY_ANSWER} 的機率 {b[int(MY_ANSWER, 2)] ** 2:.0%}')
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q121：用本機 Qiskit 重現兩位元 Grover 一輪（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
線路和 basic-circuits.html#grover 頁面下方的程式碼同一種接法：標記 = X、CZ、X；擴散 = H、X、CZ、X、H。
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


def grover(t, measure=True):
    """t 寫成 q1 q0；只做一輪（兩顆位元的最佳輪數）"""
    qc = QuantumCircuit(2)
    qc.h([0, 1])
    zeros = [q for q in (0, 1) if t[1 - q] == '0']
    if zeros:
        qc.x(zeros)                          # 標記：先把答案變成 11
    qc.cz(0, 1)
    if zeros:
        qc.x(zeros)                          # 再還原
    qc.h([0, 1])                             # 擴散：H、X、CZ、X、H
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    if measure:
        qc.measure_all()
    return qc


sampler = StatevectorSampler(seed=2026)
for t in ('00', '01', '10', '11'):
    amp = ' '.join(f'{round(a, 9) + 0.0:+.2f}' for a in Statevector(grover(t, measure=False)).data.real)   # 順序 00 01 10 11
    counts = sampler.run([grover(t)], shots=1000).result()[0].data.meas.get_counts()
    print(f'答案 {t}：振幅 {amp}　量 1000 次 {counts}')
print(grover('01').draw())
'''

STEPS = [  # (答案, 標記後四根, 標記後平均, 一輪後四根)
    ('00', '−½ +½ +½ +½', '¼', '1 0 0 0'),
    ('01', '+½ −½ +½ +½', '¼', '0 1 0 0'),
    ('10', '+½ +½ −½ +½', '¼', '0 0 1 0'),
    ('11', '+½ +½ +½ −½', '¼', '0 0 0 1'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q121：範例 8 Grover——對平均值翻轉（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的範例 8。
上一課（Q120）的 BV 密碼藏在正負號的排列裡；今天的 Grover 搜尋也先用一個負號標記答案，再多一個「擴散」，把答案的振幅拉高。
核心一句話：**擴散是讓每個振幅以平均值為鏡子翻過去（新振幅 = 2 × 平均 − 原振幅）；標記把答案變成負的、把平均拉低，答案離平均最遠，所以翻得最高。**
（Q106 已用答案 10 一步一步走過標記與擴散、講過硬體上的 X–CZ–X；這一課改用答案 01，從「平均值虛線在哪裡」切入，並說明整體負號。）

## 題目：四個寶箱，檢查員只說是或不是

- 四個寶箱 00、01、10、11，只有一箱有寶物。檢查員（Oracle）只回答「是／不是」。
- 古典一箱一箱問：最壞 3 次、平均 2.25 次（transmon-3d.html 第 7 章第 2 步）；N 個選項平均要 N/2 次。
- 「檢查員是不是作弊？」不是：認出答案比找出答案容易，像數獨，檢查很快、自己填很難（師生對話第 8 課）。
- 兩顆位元的 Grover 只問檢查員 1 次，就 100% 找到。

## 三步看平均值虛線（basic-circuits.pptx 第 23–24 頁、basic-circuits.html#grover，答案 01）

| 步驟 | 00 | 01（寶物） | 10 | 11 | 平均 | 寶物機率 |
|---|---|---|---|---|---|---|
| ① 兩顆都做 H | +½ | +½ | +½ | +½ | ½（虛線貼柱頂） | 25% |
| ② 標記 | +½ | −½ | +½ | +½ | ¼ | 25%（沒變） |
| ③ 擴散 | 0 | 1 | 0 | 0 | ¼ | 100% |

- ①之後每根都在平均線上：這時擴散，每根翻過去還在原地（2 × ½ − ½ = ½）。**沒有標記，擴散什麼都不做。**
- ②之後：其他三根比平均高 ¼，寶物比平均低 ¾。
- ③「離平均多遠，就翻到另一邊多遠」：其他三根從上方 ¼ 翻到下方 ¼（= 0）；寶物從下方 ¾ 翻到上方 ¾（= 1）。

## 整體負號（驗收要說得出）

- 簡報第 23 頁的擴散閘是 H、X、CZ、X、H。實際這樣接出來，每個振幅都多一個負號：寶物變成 −1，其他 0（grover_mean.py 第四段、qiskit_check.py）。
- 整體負號量不到：機率是振幅的平方，(−1)² = 1，一樣 100%。basic-circuits.html 照理想的「對平均值翻轉」畫，所以畫面上是 +1。
- 在 Qiskit 看到整排振幅一起變號，不用緊張。

## 換答案預測（孩子獨立改造的範例答案）

| 答案 | 標記後 | 標記後平均 | 一輪後 |
|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in STEPS) + '''
訣竅：寶物換到哪一箱，負號和翻轉就跟著搬到哪一箱，平均線的高度完全一樣。

## 容易錯的地方與限制（驗收要孩子說出至少一個）

1. 擴散是對平均值翻轉，不是對 0 翻轉，也不是「只替答案加分」；沒有先標記，擴散什麼都不做。
2. 標記之後機率完全沒變（各 25%），這時候量只是隨便猜。
3. 用 H、X、CZ、X、H 接出的擴散多一個整體負號，量不到、不影響結果。
4. 四個選項剛好一輪 100%；選項變多時一輪不夠：16 個選項一輪 47.3%、兩輪 90.8%（grover_mean.py 第五段、operation.html#grover）。做太多輪會怎樣，留到下一課 Q122。

## 影片的念法

Grover 念「格羅弗」；H「哈達瑪閘」、X「翻轉閘」、CZ「受控相位翻轉閘」；q0、q1 念「編號零」「編號一」；Oracle 說「標記」「檢查員」；Qiskit 說「量子程式套件」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；說明尋寶規則 | 影片、列印包第 1 頁 |
| 10–25 | 對照 basic-circuits.pptx 第 23–24 頁：三步、平均值、整體負號 | 簡報 |
| 25–65 | 爸爸在 basic-circuits.html#grover 設答案，孩子從起點逐步畫柱子與綠色虛線；transmon-3d.html#grover 第 8 步試「先擴散不動」 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子換答案，先預測再驗證；跑 grover_mean.py；（選用）qiskit_check.py | 列印包第 2、3 頁、`03_換答案預測.csv` |
| 105–115 | 孩子教爸爸：標記做什麼、擴散做什麼、一個注意事項 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#grover`（上方「位元數」「答案（q1 q0，點一下切換）」「重複輪數」）、`transmon-3d.html#grover`（第 7 章，步驟按鈕 8 是自由實驗）與 `operation.html#grover`（場景 9）。
- 打開 `slides/output/basic-circuits.pptx` 第 23–24 頁（課綱頁碼正確）。
- 列印 `02_列印包_Grover逐步圖.pdf`（A4，共 4 頁）。
- 有 Python 的電腦先跑一次 `python grover_mean.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 動畫與程式都是理想模擬；真實的量子電腦只給量測結果，看不到振幅柱子，也有閘與讀取誤差。
- 「最壞 3 次、平均 2.25 次」假設答案在四箱裡機會相等、問到第三箱還不是就不用再問第四箱。
- 數獨是教學比喻：重點是「檢查條件的電路」不需要事先知道答案。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：爸爸藏寶，孩子逐步畫（約 40 分鐘）

1. 打開 `animations/basic-circuits.html#grover`（範例 8）。「位元數」選「2 顆（N = 4）」、「重複輪數」選「1 輪」（或「最佳」，兩顆位元的最佳就是 1 輪）。
2. 爸爸點「答案（q1 q0，點一下切換）」的 q1、q0 兩格設答案（預設 11；點 q1 那格變 01）。換答案時頁面會停在最後一步；按「⏮ 起點」回到開頭。
3. 孩子每按一次「下一步 ▶」之前，先在列印包第 1 頁畫出四根柱子和綠色虛線（平均值）的位置，再看畫面：
   - 第 1 步：四根 +.500，綠色虛線貼著柱頂（平均 ½）。
   - 第 2 步：答案那根翻到下面（橘色 −.500），綠色虛線滑到 ¼；說明文字寫「看綠色虛線，平均值被拉低到 +.250」。
   - 第 3 步：擴散，答案 +1.000、其他 0。按「量測 1,000 次」，寫著「→ 找到答案 ✓」。
4. 想看「沒有標記，擴散不動」：打開 `transmon-3d.html#grover`，按步驟 8（自由實驗），答案選 00，依序按 H₁、H₂、擴散（四根不動、金色平均線「平均 +0.50」）、Oracle（平均降到 +0.25）、擴散（00 到 +1.00）、量測 50 次。
5. 想看選項變多：打開 `operation.html#grover`（16 個選項），把「答案（標記的項目）」滑桿拉到任一個，分開按「② Oracle」「③ 擴散」：做 Oracle 時出現粉紅色的平均面；一輪後答案的機率 P = 0.473，兩輪 0.908。

## 下半場：換答案，預測一輪（約 30 分鐘）

1. 孩子選另一個答案（00、10 或 11），先在列印包第 2 頁寫下：標記後四根、標記後平均、一輪後四根。
2. 在 basic-circuits.html#grover 設成那個答案，從起點逐步驗證。
3. 打開 `grover_mean.py` 最下面的改造區，把 `MY_ANSWER` 改成同一個答案（兩位，只寫 0 和 1），執行看第六段。
4. 第三段一次列出四種答案：標記後平均都是 +0.25，一輪後都 100%。
5. 有裝 Qiskit 的話，跑 `python qiskit_check.py`：四種答案的振幅都是 −1.00（整體負號），各量 1000 次全部是答案。
''',

'grover_mean.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## grover_mean.py 實跑輸出（Python 3.13.18，沒有亂數）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，Statevector；StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- 標記做了什麼？只把答案的振幅變號，機率不變；但平均從 ½ 降到 ¼，答案變成離平均最遠的一根（低 ¾）。\n'
  '- 擴散做了什麼？每個振幅以平均值為鏡子翻過去：新振幅 = 2 × 平均 − 原振幅；離平均多遠，就翻到另一邊多遠。\n'
  '- 為什麼不標記就擴散沒用？四根都等於平均，2 × ½ − ½ = ½，每根都在原地。\n'
  '- 為什麼 Qiskit 的答案振幅是 −1？H、X、CZ、X、H 接出來的擴散是理想擴散再乘一個 −1（整體負號），(−1)² = 1，量不到。\n'
  '- 換答案會怎樣？負號和翻轉跟著搬家，平均線高度一樣（¼），一輪後答案都是 1。\n'
  '- 改造區預設 MY_ANSWER = \'11\'：標記後 +½ +½ +½ −½、平均 ¼，一輪後 0 0 0 1（100%）。\n'
  '- 選項變多呢？16 個選項：第 1 輪答案只到 +0.688（47.3%），第 2 輪答案離平均更遠，到 +0.953（90.8%）。\n'
  '- 下一課 Q122：Grover 三位元——轉太多會轉過頭。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號（transmon-3d.html、operation.html 需要能載入 three.js）。

## `animations/basic-circuits.html#grover`（範例 8 Grover）

- 上方「位元數」（2 顆／3 顆）、「答案（q1 q0，點一下切換）」（預設 11）、「重複輪數」（最佳／1 輪／2 輪／3 輪）；換選項時停在最後一步。
- 電路：兩條 H、紫色「標記」方塊、「擴散」方塊、量測。「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」。
- 「振幅與機率」：四根柱子，藍色正、橘色負；**綠色虛線是平均值**（圖例「平均值」）；換步時柱子和虛線一起動。
- 「量測 1 次」「量測 1,000 次」「清除」；量到答案時寫「→ 找到答案 ✓」。
- 頁尾說明：擴散照理想的「對平均值翻轉」計算；用 H、X、多控制 Z 組成的實際電路會多一個整體負號，機率完全相同。

## `animations/transmon-3d.html#grover`（第 7 章 振幅長條）

- 步驟 2–5 是答案 10 的導覽（第 2 步寫著古典最壞 3 次、平均 2.25 次）；步驟 8「自由實驗」：答案 00～11、H₁、H₂、X₁、X₂、CZ、Oracle、擴散、一鍵 Grover、量測 50 次、重設。
- 四根柱子：金色正、紅色負；按「擴散」後出現金色平均線與「平均 +0.50」這樣的標籤。

## `animations/operation.html#grover`（場景 9 Grover 搜尋）

- 滑桿「量子位元數 n」（預設 4，N = 16）、「答案（標記的項目）」；按鈕「② Oracle」「③ 擴散」「完整一輪」「自動跑到最佳次數」「測量」「重設」。
- 柱子金色正、藍色負；做完 Oracle 時出現粉紅色的平均面；左下讀數寫答案的機率 P。
''',
}

SHEET_HEADER = ['答案', '我預測標記後四根（00 01 10 11）', '我預測標記後平均', '我預測一輪後四根', '動畫看到的一輪後', '量 1,000 次', 'grover_mean.py 第六段', '我的發現']
SHEET_ROWS = [['範例：01', '+½ −½ +½ +½', '¼', '0 1 0 0', '0 +1.000 0 0', '01（1000 次）', '同', '寶物離平均最遠，翻得最高'],
              ['00', '', '', '', '', '', '', ''], ['10', '', '', '', '', '', '', ''], ['11', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.rec td{height:10mm;font-size:11pt}table.rec td.k{font-weight:bold;color:#0b2540;width:15%}
table.rec th{font-size:10pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.plot{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:2mm 0}
.plot div{height:38mm;border:1pt solid #4a6a85;position:relative}
.plot div:before{content:"";position:absolute;left:0;right:0;top:50%;border-top:1.2pt solid #4a6a85}
.plot div span{position:absolute;bottom:-5mm;width:100%;text-align:center;font-size:10pt}
.row{margin:1mm 0 7mm}.row b{font-size:11pt}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 grover_mean.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'grover_mean.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    plot = lambda t: (f'<div class="row"><b>{t}</b>　平均 = ＿＿＿<div class="plot">'  # noqa: E731
                      + ''.join(f'<div><span>|{k}⟩</span></div>' for k in ('00', '01', '10', '11')) + '</div></div>')
    rec = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    pages = [
        '<h2>Grover 逐步圖</h2><p class="lead">basic-circuits.html#grover：2 顆、1 輪。答案：＿＿＿。每按「下一步 ▶」前，先畫四根柱子（中線是 0，往上正、往下負），再用綠筆畫平均值虛線。</p>'
        + plot('① 兩顆都做 H') + plot('② 標記') + plot('③ 擴散')
        + '<p>標記之後，寶物比平均低多少？＿＿＿；擴散之後，寶物比平均高多少？＿＿＿</p>',
        '<h2>換答案，預測一輪</h2><p class="lead">先寫預測，再用動畫從起點逐步驗證；最後跑 grover_mean.py 第三、六段。</p>'
        '<table class="rec"><tr><th style="width:15%">答案</th><th>標記後四根<br>（00 01 10 11）</th><th>標記後平均</th><th>一輪後四根</th><th>量 1,000 次</th></tr>'
        + rec('01（範例）').replace('<td></td><td></td><td></td><td></td>', '<td>+½ −½ +½ +½</td><td>¼</td><td>0 1 0 0</td><td>01：1000 次</td>', 1)
        + rec('00') + rec('10') + rec('11') + '</table>'
        '<p>寶物換位置時，什麼跟著搬家？什麼完全不變？</p><div class="line"></div>'
        '<pre class="code"># grover_mean.py 最下面的改造區：兩位，只寫 0 和 1\n'
        "MY_ANSWER = '11'\n"
        '# 改完先預測，再執行 python grover_mean.py，看第六段</pre>',
        '<h2>離平均多遠，就翻到另一邊多遠</h2><p class="lead">擴散的規則：新振幅 = 2 × 平均 − 原振幅。先自己填，再對 grover_mean.py 第一、二、五段。</p>'
        '<table class="rec"><tr><th style="width:24%">情況</th><th>平均</th><th>這一根離平均</th><th>翻過去之後</th></tr>'
        '<tr><td class="k">還沒標記，每根 +½</td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">標記後，普通的一根 +½</td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">標記後，寶物 −½</td><td></td><td></td><td></td></tr></table>'
        '<p>為什麼沒有標記，擴散什麼都不做？</p><div class="line"></div>'
        '<p>閘電路（H、X、CZ、X、H）接出來，寶物的振幅是＿＿＿；量到寶物的機率是＿＿＿。為什麼一樣？</p><div class="line"></div>'
        '<p>16 個選項時，一輪後寶物的機率約＿＿＿；兩輪約＿＿＿（operation.html#grover 讀數 P）。</p>',
        '<h2>最後一關：教爸爸對平均翻轉</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 標記做了什麼（不看稿）：</p><div class="line"></div>'
        '<p>2. 擴散為什麼讓寶物翻得最高：</p><div class="line"></div>'
        '<p>3. 一個注意事項或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：標記只把寶物變號，機率不變，平均從 ½ 降到 ¼</li><li>說出：擴散 = 對平均值翻轉，離多遠就翻到另一邊多遠</li>'
        '<li>說出：沒有標記，擴散什麼都不做</li><li>指出：閘電路多一個整體負號，量不到、不影響結果</li>'
        '<li>完成 Grover 逐步圖與換答案預測，和動畫、grover_mean.py 一致</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q121 Grover 逐步圖 列印包', '父子科技學院 量子電腦學程 Q121｜範例 8：Grover——對平均值翻轉', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q121-grover-mean-flip', folder='Q121_範例8_Grover_對平均值翻轉', files=FILES,
        sheet=('03_換答案預測.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_Grover逐步圖.pdf', pack_pages=4,
        pack_needles=('Grover 逐步圖', '換答案', '離平均多遠', 'MY_ANSWER', '最後一關'),
        authoring_dir=XINEW / 'authoring/q121', episode_dir='specials/q121-grover-mean-flip',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；grover_mean.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'grover_mean.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, no randomness); qiskit 2.6.2',
               'recordedRun': {'answer': '01', 'means': {'afterH': 0.5, 'afterMark': 0.25, 'afterDiffuse': 0.25},
                               'distanceAfterMark': {'others': 0.25, 'answer': -0.75}, 'diffuseWithoutMark': 'unchanged',
                               'allAnswersOneRound': 1.0, 'gateCircuitGlobalSign': -1,
                               'sixteenOptions': {'round1': 0.473, 'round2': 0.908},
                               'qiskitAllCorrect': ['00', '01', '10', '11']},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q121/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

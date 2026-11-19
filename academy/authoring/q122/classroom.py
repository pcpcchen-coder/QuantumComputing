"""Q122 課堂教材：輪數與成功率圖（預測與實測）、逐輪紀錄表、N 變大的輪數計算單、可執行的 grover_rounds.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#grover、operation.html#grover 與 transmon-3d.html#grover；grover_rounds.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 grover_rounds.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \\
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q122/classroom.py
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
RUN_OUTPUT = '''一、三顆位元、8 個選項、答案 101
  0 輪：（還沒做）         答案 +0.35   其他每根 +0.35   答案的機率 12.5%
  1 輪：標記後平均 +0.27   答案 +0.88   其他每根 +0.18   答案的機率 78.1%
  2 輪：標記後平均 +0.04   答案 +0.97   其他每根 −0.09   答案的機率 94.5%
  3 輪：標記後平均 −0.20   答案 +0.57   其他每根 −0.31   答案的機率 33.0%
二、繼續多做幾輪
  0 輪 12.50%  1 輪 78.12%  2 輪 94.53%  3 輪 33.01%  4 輪 1.22%  5 輪 54.80%  6 輪 99.98%
三、指針的角度（答案在 90°）
  一開始 20.7°，每一輪多轉 41.4°
  0 輪 21°→12.5%  1 輪 62°→78.1%  2 輪 104°→94.5%  3 輪 145°→33.0%
四、選項變多：最佳輪數 vs 古典平均
   2 顆（N =         4）：(π/4)√N =    1.57，最佳   1 輪，成功率 100.00000%；古典平均 2.5 次
   3 顆（N =         8）：(π/4)√N =    2.22，最佳   2 輪，成功率 94.53125%；古典平均 4.5 次
   4 顆（N =        16）：(π/4)√N =    3.14，最佳   3 輪，成功率 96.13190%；古典平均 8.5 次
  10 顆（N =     1,024）：(π/4)√N =   25.13，最佳  25 輪，成功率 99.94612%；古典平均 512.5 次
  20 顆（N = 1,048,576）：(π/4)√N =  804.25，最佳 804 輪，成功率 99.99998%；古典平均 524,288.5 次
五、8 個選項裡有 2 個答案（101 和 011）
  0 輪 25.0%  1 輪 100.0%  2 輪 25.0%  3 輪 25.0%   最佳 1 輪
六、改造區
  N = 1,024：√N = 32，(π/4)√N ≈ 25.13，最佳 25 輪
  24 輪 99.85%  25 輪 99.95%  26 輪 99.27%
  古典平均要試 512.5 次
'''

# 製作代理實跑紀錄：qiskit 2.6.2，Statevector（理論機率）與 StatevectorSampler(seed=2026)，shots=1000（次數會隨種子不同）
QISKIT_OUTPUT = '''1 輪：答案 101 的理論機率 78.1%　量 1000 次，101 出現 800 次
2 輪：答案 101 的理論機率 94.5%　量 1000 次，101 出現 950 次
3 輪：答案 101 的理論機率 33.0%　量 1000 次，101 出現 358 次
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q122：Grover 三位元——轉太多會轉過頭（純 Python，不需安裝任何套件）

執行：  python grover_rounds.py
它印出：
  一、三顆位元、答案 101：0～3 輪，每輪標記後的平均、答案和其他的振幅、答案的機率
  二、繼續多做幾輪：機率先降、再爬回來（一圈一圈起伏）
  三、指針的角度：每一輪多轉同樣的角度，答案在 90°
  四、選項變多：最佳輪數 ≈ (π/4)√N，和古典平均要試幾次比一比
  五、如果有兩個答案：最佳輪數變少，做太多一樣轉過頭
  六、改造區：換成自己的 N，先算，再執行
位元字串寫成 q2 q1 q0（最右邊是 q0），和 basic-circuits.html#grover、Qiskit 一樣。
"""
from math import asin, degrees, pi, sin, sqrt

ANSWER = '101'      # 簡報第 25 頁用的答案


def sg(a):
    return f'{a + 0.0:+.2f}'.replace('-', '−')


def grover(n, answers, rounds):
    """回傳每一輪的紀錄：(輪數, 標記後平均, 擴散後的振幅)"""
    N = 2 ** n
    idx = [int(t, 2) for t in answers]
    v = [1 / sqrt(N)] * N
    out = [(0, None, v[:])]
    for r in range(1, rounds + 1):
        for i in idx:
            v[i] = -v[i]                   # 標記：答案變號
        m = sum(v) / N
        v = [2 * m - a for a in v]          # 擴散：對平均值翻轉
        out.append((r, m, v[:]))
    return out


def p_answer(v, answers):
    return sum(v[int(t, 2)] ** 2 for t in answers)


def best_rounds(N, k=1):
    """最佳輪數：讓 (2r + 1)θ 最接近 90° 的整數 r，sin θ = √(k/N)"""
    th = asin(sqrt(k / N))
    return max(1, round(pi / (4 * th) - 0.5)), th


if __name__ == '__main__':
    print(f'一、三顆位元、8 個選項、答案 {ANSWER}')
    i = int(ANSWER, 2)
    rec = grover(3, [ANSWER], 6)
    for r, m, v in rec[:4]:
        other = v[(i + 1) % 8]
        mark = '（還沒做）      ' if m is None else f'標記後平均 {sg(m)}'
        print(f'  {r} 輪：{mark}   答案 {sg(v[i])}   其他每根 {sg(other)}   答案的機率 {v[i] ** 2:.1%}')

    print('二、繼續多做幾輪')
    print('  ' + '  '.join(f'{r} 輪 {v[i] ** 2:.2%}' for r, m, v in rec))

    print('三、指針的角度（答案在 90°）')
    th = asin(1 / sqrt(8))
    print(f'  一開始 {degrees(th):.1f}°，每一輪多轉 {degrees(2 * th):.1f}°')
    print('  ' + '  '.join(f'{r} 輪 {degrees((2 * r + 1) * th):.0f}°→{sin((2 * r + 1) * th) ** 2:.1%}' for r in range(4)))

    print('四、選項變多：最佳輪數 vs 古典平均')
    for n in (2, 3, 4, 10, 20):
        N = 2 ** n
        r, t = best_rounds(N)
        print(f'  {n:>2} 顆（N = {N:>9,}）：(π/4)√N = {pi / 4 * sqrt(N):7.2f}，最佳 {r:>3} 輪，'
              f'成功率 {sin((2 * r + 1) * t) ** 2:.5%}；古典平均 {(N + 1) / 2:,.1f} 次')

    print('五、8 個選項裡有 2 個答案（101 和 011）')
    two = ['101', '011']
    r2, _ = best_rounds(8, 2)
    print('  ' + '  '.join(f'{r} 輪 {p_answer(v, two):.1%}' for r, m, v in grover(3, two, 3)) + f'   最佳 {r2} 輪')

    # 六、改造區：換成自己的 N（2 的次方），先算，再執行
    MY_N = 1024
    r, t = best_rounds(MY_N)
    print('六、改造區')
    print(f'  N = {MY_N:,}：√N = {sqrt(MY_N):g}，(π/4)√N ≈ {pi / 4 * sqrt(MY_N):.2f}，最佳 {r} 輪')
    print('  ' + '  '.join(f'{k} 輪 {sin((2 * k + 1) * t) ** 2:.2%}' for k in (r - 1, r, r + 1)))
    print(f'  古典平均要試 {(MY_N + 1) / 2:,.1f} 次')
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q122：用本機 Qiskit 重現三位元 Grover 的 1、2、3 輪（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
線路和 basic-circuits.html#grover 的接法相同：標記 = X、多控制 Z、X；擴散 = H、X、多控制 Z、X、H。
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector

ANSWER = '101'      # 寫成 q2 q1 q0


def ccz(qc):
    qc.h(2)
    qc.ccx(0, 1, 2)                          # 多控制 Z = H、Toffoli、H
    qc.h(2)


def grover(rounds, measure=True):
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])
    zeros = [q for q in range(3) if ANSWER[2 - q] == '0']
    for _ in range(rounds):
        if zeros:
            qc.x(zeros)                      # 標記：先把答案變成 111
        ccz(qc)
        if zeros:
            qc.x(zeros)
        qc.h([0, 1, 2])                      # 擴散：H、X、多控制 Z、X、H
        qc.x([0, 1, 2])
        ccz(qc)
        qc.x([0, 1, 2])
        qc.h([0, 1, 2])
    if measure:
        qc.measure_all()
    return qc


sampler = StatevectorSampler(seed=2026)
for r in (1, 2, 3):
    p = Statevector(grover(r, measure=False)).probabilities_dict()[ANSWER]
    counts = sampler.run([grover(r)], shots=1000).result()[0].data.meas.get_counts()
    print(f'{r} 輪：答案 {ANSWER} 的理論機率 {p:.1%}　量 1000 次，{ANSWER} 出現 {counts.get(ANSWER, 0)} 次')
'''

ROUNDS = [  # (輪數, 標記後平均, 答案, 其他每根, 答案的機率)
    ('0', '—', '+0.35', '+0.35', '12.5%'),
    ('1', '+0.27', '+0.88', '+0.18', '78.1%'),
    ('2', '+0.04', '+0.97', '−0.09', '94.5%'),
    ('3', '−0.20', '+0.57', '−0.31', '33.0%'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q122：Grover 三位元——轉太多會轉過頭（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的第十課。
上一課（Q121）兩顆位元、四個寶箱，一輪就 100%；今天換成三顆位元、八個抽屜，一輪不夠、兩輪最好、三輪反而變差。
核心一句話：**Grover 每一輪都把狀態朝答案轉同樣的角度；轉到最接近答案就要停，再轉就轉過頭。最佳輪數約 (π/4)√N。**
（Q106 已用一句話帶過「八個選項 78.1%、94.5%、33%」；這一課逐輪看平均值、用指針角度解釋，並算 N = 1024。）

## 三顆位元逐輪看（basic-circuits.pptx 第 25 頁，答案 101）

| 輪數 | 標記後平均 | 答案 101 | 其他每根 | 答案的機率 |
|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in ROUNDS) + '''
- 第 1、2 輪：標記把平均拉低，答案在平均下方很遠，翻過去就變高。
- 第 3 輪：答案已經 +0.97，標記後是 −0.97，**平均變成負的**（約 −0.20）。對一條在 0 下面的線翻轉，答案只翻到 +0.57，其他掉到 −0.31：機率 94.5% → 33%。
- 繼續做：4 輪 1.2%、5 輪 54.8%、6 輪 99.98%——機率會一起一落（grover_rounds.py 第二段、operation.html#grover 右下曲線）。

## 為什麼會轉過頭：指針角度

- 把狀態想成一根指針：一個方向是答案（90°），另一個方向是其他所有選項（0°）。sin θ = 1/√N；N = 8 時 θ ≈ 20.7°。
- 一開始在 θ ≈ 21°，每輪多轉 2θ ≈ 41°：0 輪 21°、1 輪 62°、2 輪 104°、3 輪 145°。答案的機率 = sin²(角度)。
- 2 輪 104° 最接近 90°（94.5%，不是 100%）；3 輪 145° 已經轉過頭。
- 最佳輪數約 (π/4)√N（Wikipedia：r ≈ π√N/4；簡報第 26 頁）。

## N 變大：√N 的威力（簡報第 26 頁、grover_rounds.py 第四段）

| N | 古典平均要試 | Grover 最佳輪數 | 成功率 |
|---|---|---|---|
| 4（2 顆） | 2.5 次 | 1 輪 | 100% |
| 8（3 顆） | 4.5 次 | 2 輪 | 94.5% |
| 16（4 顆） | 8.5 次 | 3 輪 | 96.1% |
| 1,024（10 顆） | 512.5 次 | 25 輪 | 99.9% |
| 1,048,576（20 顆） | 約 52 萬次 | 804 輪 | > 99.99% |

孩子獨立改造的範例答案：√1024 = 32，32 × π/4 ≈ 25.1 → 25 輪（24 輪 99.85%、25 輪 99.95%、26 輪 99.27%）。

## 容易錯的地方與限制（驗收要孩子說出至少一個）

1. 輪數不是越多越好；最佳約 (π/4)√N，再多做會轉過頭。
2. 要先知道大約有幾個答案：k 個答案時最佳輪數變成 (π/4)√(N/k)。8 個選項裡有 2 個答案時，1 輪就 100%，2 輪又掉回 25%（grover_rounds.py 第五段）。
3. 是平方根加速，不是指數加速；已經證明黑盒搜尋不可能比 √N 等級更快（簡報第 26 頁、Wikipedia 引 Bennett 等人 1997）。
4. 三顆位元的最佳 2 輪也只有 94.5%，量 1,000 次仍會出現少數別的結果。

## 影片的念法

Grover 念「格羅弗」；H「哈達瑪閘」；π 念「圓周率」（四分之圓周率 = π/4）；Oracle 說「標記」；Qiskit 說「小程式」「量子程式套件」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；說明效能競賽規則，先用鉛筆畫預測 | 影片、列印包第 1 頁 |
| 10–25 | 對照 basic-circuits.pptx 第 25–26 頁：逐輪平均、指針角度、√N 表 | 簡報 |
| 25–65 | basic-circuits.html#grover 三顆位元，輪數選 1／2／3 輪，讀說明文字的機率，畫輪數與成功率圖；operation.html#grover 看右下曲線 | `01_操作步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子算 N = 1024 要幾輪；跑 grover_rounds.py；（選用）qiskit_check.py | 列印包第 3 頁、`03_輪數與成功率.csv` |
| 105–115 | 孩子教爸爸：第三輪為什麼變差、最佳輪數、一個注意事項 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#grover`（上方「位元數」「答案」「重複輪數」）、`operation.html#grover`（場景 9）與 `transmon-3d.html#grover`（第 7 章，步驟按鈕 8 是自由實驗）。
- 打開 `slides/output/basic-circuits.pptx` 第 25–27 頁（課綱頁碼正確）。
- 列印 `02_列印包_輪數與成功率圖.pdf`（A4，共 4 頁）。
- 有 Python 的電腦先跑一次 `python grover_rounds.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 動畫與程式都是理想模擬；真實的量子電腦有閘與讀取誤差，輪數越多誤差累積越多。
- 「古典平均 4.5 次」是簡報第 26 頁的 (N + 1)/2（一個一個試、答案位置機會相等）；operation.html 讀數寫 N/2 = 4 次，兩者是不同的算法約定。
- transmon-3d.html 第 7 章第 6 步的文字寫「四個振幅都變成 −½」，實際程式算出來是答案 +½、其他 −½（機率一樣各 25%）；教材以實算為準。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：記錄 1、2、3 輪，畫輪數與成功率圖（約 40 分鐘）

1. 先在列印包第 1 頁用鉛筆畫下預測：0、1、2、3 輪各是多少機率？誰猜得最接近，誰就贏這一場效能競賽。
2. 打開 `animations/basic-circuits.html#grover`（範例 8）。「位元數」選「3 顆（N = 8）」，答案預設 101（「答案（q2 q1 q0，點一下切換）」）。
3. 「重複輪數」依序選「1 輪」「2 輪」「3 輪」。每換一次，畫面停在最後一步，讀說明文字的機率：78.1%、94.5%、33%（三輪時會寫「轉過頭了」）。
4. 想一步一步看：按「⏮ 起點」再按「下一步 ▶」。每一輪是「標記」＋「擴散」兩步；看綠色虛線（平均值）：第 3 輪標記後虛線跑到 0 下面。
5. 在列印包第 1 頁用紅筆點上 0 輪 12.5%、1 輪 78.1%、2 輪 94.5%、3 輪 33%，連成線。
6. 打開 `operation.html#grover`（場景 9），「量子位元數 n」拉到 3，按「完整一輪」五次：右下插圖的白點在「P(成功) vs 輪數」曲線上走，讀數 P = 0.781、0.945、0.330、0.012、0.548。
7. 想看兩顆位元也會轉過頭：`transmon-3d.html#grover` 按步驟 8（自由實驗），選答案、按「一鍵 Grover」，再按「Oracle」「擴散」：回到各 25%。

## 下半場：N = 1024 要幾輪（約 30 分鐘）

1. 孩子在列印包第 3 頁先算：√1024 = ？　× π/4 ≈ ？　古典平均要試 (N + 1)/2 = ？
2. 跑 `python grover_rounds.py`，看第四段（N = 4 到 2²⁰ 的最佳輪數）與第六段（改造區，預設 N = 1,024）。
3. 改造：把最下面的 `MY_N` 改成別的 2 的次方（例如 4096、65536），先預測，再執行。
4. 第五段看「兩個答案」：8 個裡有 2 個答案時，1 輪 100%、2 輪 25%——要先知道大約有幾個答案。
5. 有裝 Qiskit 的話，跑 `python qiskit_check.py`：1／2／3 輪的理論機率 78.1／94.5／33.0%，再各量 1,000 次看次數（次數是隨機的）。
''',

'grover_rounds.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## grover_rounds.py 實跑輸出（Python 3.13.18，沒有亂數）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，Statevector；StatevectorSampler seed=2026，次數會隨種子不同）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- 為什麼第 3 輪會變差？標記後答案 −0.97，平均變成負的（約 −0.20）；對這條線翻轉，答案只到 +0.57，機率 33%。用指針看：2 輪 104° 已經越過 90°，3 輪 145° 轉過頭。\n'
  '- 為什麼三顆最好也只有 94.5%？每輪轉約 41°，從 21° 出發，整數輪只能停在 62° 或 104°，碰不到剛好 90°。\n'
  '- N = 1024 要幾輪？√1024 = 32，× π/4 ≈ 25.1 → 25 輪，成功率約 99.9%；古典平均 512.5 次。\n'
  '- 選項多 100 倍，輪數多幾倍？√100 = 10，約 10 倍。\n'
  '- 為什麼要先知道大約幾個答案？k 個答案時最佳輪數是 (π/4)√(N/k)；8 個裡 2 個答案，1 輪就 100%，2 輪又掉回 25%。\n'
  '- 這是指數加速嗎？不是，是平方根加速；而且已經證明黑盒搜尋不可能比這更快。\n'
  '- 下一課 Q123：古典 vs 量子——要查幾次？\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號（transmon-3d.html、operation.html 需要能載入 three.js）。

## `animations/basic-circuits.html#grover`（範例 8 Grover）

- 上方「位元數」（2 顆／3 顆）、「答案」（點一下切換；3 顆預設 101）、「重複輪數」（最佳／1 輪／2 輪／3 輪）；換選項時停在最後一步。
- 電路：H、紫色「標記」方塊、「擴散」方塊（每一輪一對）、量測。「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」。
- 「振幅與機率」：藍色正、橘色負；**綠色虛線是平均值**。說明文字寫每一步答案的機率，轉過頭時會提醒。
- 「量測 1 次」「量測 1,000 次」「清除」。

## `animations/operation.html#grover`（場景 9 Grover 搜尋）

- 滑桿「量子位元數 n」（2–6）、「答案（標記的項目）」；按鈕「② Oracle」「③ 擴散」「完整一輪」「自動跑到最佳次數」「測量」「重設」。先改 n 再改答案。
- 右下插圖：左邊「答案–非答案」平面上的金色指針（每輪轉 2θ）；右邊「P(成功) vs 輪數」曲線，白點是目前輪數。

## `animations/transmon-3d.html#grover`（第 7 章 振幅長條）

- 步驟 8「自由實驗」：答案 00～11、Oracle、擴散、「一鍵 Grover」、量測 50 次、重設。一鍵 Grover 後再按 Oracle、擴散，就會轉過頭（回到各 25%）。
- 注意：步驟 6「轉過頭」的文字寫「四個振幅都變成 −½」，實際是答案 +½、其他 −½。
''',
}

SHEET_HEADER = ['輪數', '我預測的成功率', '動畫說明文字的機率', '標記後平均（grover_rounds.py）', '答案振幅', '其他每根', '我的發現']
SHEET_ROWS = [['0', '', '12.5%', '—', '+0.35', '+0.35', ''],
              ['1', '', '', '', '', '', ''], ['2', '', '', '', '', '', ''], ['3', '', '', '', '', '', '']]

EXTRA_CSS = '''table.rec td{height:10mm;font-size:11pt}table.rec td.k{font-weight:bold;color:#0b2540;width:15%}
table.rec th{font-size:10pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.chart{position:relative;height:105mm;margin:4mm 0 10mm 14mm;border-left:1.4pt solid #0b2540;border-bottom:1.4pt solid #0b2540;
background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt),linear-gradient(90deg,#cfdde8 .6pt,transparent .6pt);background-size:100% 10%,25% 100%}
.chart .y{position:absolute;left:-13mm;font-size:9.5pt;width:11mm;text-align:right}
.chart .x{position:absolute;bottom:-6mm;font-size:10pt;width:20mm;margin-left:-10mm;text-align:center}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 grover_rounds.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'grover_rounds.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    ys = ''.join(f'<span class="y" style="bottom:{v}%;margin-bottom:-2mm">{v}%</span>' for v in range(0, 101, 20))
    xs = ''.join(f'<span class="x" style="left:{k * 25}%">{k} 輪</span>' for k in range(5))
    chart = f'<div class="chart">{ys}{xs}</div>'
    rec = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    pages = [
        '<h2>輪數與成功率圖</h2><p class="lead">效能競賽：先用鉛筆畫預測（0–3 輪），再用紅筆點上動畫說明文字的機率，連成線。basic-circuits.html#grover：3 顆位元，輪數選 1、2、3 輪。</p>'
        + chart + '<p>我預測最好的是第＿＿輪；實際最好的是第＿＿輪，成功率＿＿＿。第 4 輪你猜會怎樣？＿＿＿＿＿＿</p>',
        '<h2>逐輪紀錄：平均值與指針</h2><p class="lead">一步一步看（⏮ 起點 → 下一步 ▶），記下每一輪標記後的綠色虛線（平均值）和擴散後的柱子。</p>'
        '<table class="rec"><tr><th style="width:15%">輪數</th><th>標記後平均</th><th>擴散後答案</th><th>其他每根</th><th>答案的機率</th></tr>'
        + rec('0（起點）').replace('<td></td><td></td><td></td><td></td>', '<td>—</td><td>+0.35</td><td>+0.35</td><td>12.5%</td>', 1)
        + rec('1') + rec('2') + rec('3') + '</table>'
        '<p>第幾輪標記後，平均變成負的？＿＿＿　這時答案翻過去會怎樣？</p><div class="line"></div>'
        '<p>指針角度（sin θ = 1/√8，θ ≈ 21°，每輪多轉 2θ ≈ 41°）：0 輪 21°、1 輪＿＿°、2 輪＿＿°、3 輪＿＿°。哪一輪最接近 90°？＿＿</p>',
        '<h2>N = 1024 要幾輪？</h2><p class="lead">孩子獨立改造：先自己算，再跑 grover_rounds.py 第四、六段對答案。</p>'
        '<table class="rec"><tr><th style="width:24%">N</th><th>√N</th><th>(π/4)√N ≈ 最佳輪數</th><th>古典平均 (N + 1)/2</th></tr>'
        '<tr><td class="k">8（3 顆）</td><td>≈ 2.83</td><td>≈ 2.2 → 2 輪</td><td>4.5 次</td></tr>'
        '<tr><td class="k">1,024（10 顆）</td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">我選的 N：＿＿＿</td><td></td><td></td><td></td></tr></table>'
        '<p>選項多 100 倍，Grover 的輪數大約多幾倍？＿＿＿ 為什麼？</p><div class="line"></div>'
        '<p>8 個選項裡如果有 2 個答案，1 輪後成功率＿＿＿；2 輪後＿＿＿（grover_rounds.py 第五段）。所以要先知道什麼？</p><div class="line"></div>'
        '<pre class="code"># grover_rounds.py 最下面的改造區：寫 2 的次方\n'
        'MY_N = 1024\n'
        '# 改完先預測，再執行 python grover_rounds.py，看第六段</pre>',
        '<h2>最後一關：教爸爸轉過頭</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 第三輪為什麼機率會掉下來（不看稿）：</p><div class="line"></div>'
        '<p>2. 最佳輪數為什麼和 √N 有關：</p><div class="line"></div>'
        '<p>3. 一個注意事項或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>完成輪數與成功率圖：12.5%、78.1%、94.5%、33%，先升後降</li><li>說出：第 3 輪標記後平均變負，答案翻不上去</li>'
        '<li>說出：每輪轉固定角度，越過 90° 就轉過頭；最佳約 (π/4)√N</li><li>算出 N = 1024 約 25 輪（古典平均 512.5 次）</li>'
        '<li>指出：平方根加速，而且要先知道大約有幾個答案</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q122 輪數與成功率圖 列印包', '父子科技學院 量子電腦學程 Q122｜Grover 三位元：轉太多會轉過頭', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q122-grover-overshoot', folder='Q122_Grover三位元_轉太多會轉過頭', files=FILES,
        sheet=('03_輪數與成功率.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_輪數與成功率圖.pdf', pack_pages=4,
        pack_needles=('輪數與成功率圖', '逐輪紀錄', 'N = 1024', 'MY_N', '最後一關'),
        authoring_dir=XINEW / 'authoring/q122', episode_dir='specials/q122-grover-overshoot',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；grover_rounds.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'grover_rounds.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, no randomness); qiskit 2.6.2',
               'recordedRun': {'answer': '101', 'successByRound': {'0': 0.125, '1': 0.781, '2': 0.945, '3': 0.330},
                               'meanAfterMark': {'1': 0.27, '2': 0.04, '3': -0.20},
                               'laterRounds': {'4': 0.0122, '5': 0.548, '6': 0.9998},
                               'anglesDeg': [21, 62, 104, 145], 'stepDeg': 41.4,
                               'n1024': {'bestRounds': 25, 'success': 0.9995, 'classicalAverage': 512.5},
                               'twoAnswersOf8': {'1': 1.0, '2': 0.25}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q122/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

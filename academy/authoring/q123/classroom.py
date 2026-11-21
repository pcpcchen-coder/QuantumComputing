"""Q123 課堂教材：查詢次數比較表、三格動畫驗證單、「量子沒有優勢的問題」改造單、可執行的 query_count.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/operation.html#interference、operation.html#grover 與 transmon-3d.html#bv；query_count.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 query_count.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \\
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q123/classroom.py
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
RUN_OUTPUT = '''一、Deutsch（1 位元，四種黑盒子）
  f(x) = 0     古典問 f(0)、f(1) 共 2 次 → 常數；量子問 1 次，量到 0 的機率 100% → 常數
  f(x) = 1     古典問 f(0)、f(1) 共 2 次 → 常數；量子問 1 次，量到 0 的機率 100% → 常數
  f(x) = x     古典問 f(0)、f(1) 共 2 次 → 平衡；量子問 1 次，量到 0 的機率 0% → 平衡
  f(x) = 1 − x 古典問 f(0)、f(1) 共 2 次 → 平衡；量子問 1 次，量到 0 的機率 0% → 平衡
二、Deutsch–Jozsa（3 位元，8 個輸入）
  常數 2 台、平衡 70 台，共 72 台；量子各問 1 次，判斷正確 72 台
  古典：前 4 個都回答 0，還可能是平衡的 → 最壞要問 5 次（= 2ⁿ⁻¹ + 1）
  允許出錯：隨便抽 k 個不同的輸入問，平衡機器卻剛好全部同答案（被誤判成常數）的機率
  k = 2：42.9%  k = 3：14.3%  k = 4：2.9%
三、Bernstein–Vazirani（3 位元密碼）
  8 種密碼：古典各問 3 次全部猜中 8 種；量子各問 1 次、量到密碼的機率 100% 的有 8 種
四、Grover（找一個答案）
   2 位元（N =     4）：古典平均 2.5 次（約 N/2 = 2）；量子最佳  1 輪，成功率 100.0%，平均要跑 1.00 回
   3 位元（N =     8）：古典平均 4.5 次（約 N/2 = 4）；量子最佳  2 輪，成功率 94.5%，平均要跑 1.06 回
   4 位元（N =    16）：古典平均 8.5 次（約 N/2 = 8）；量子最佳  3 輪，成功率 96.1%，平均要跑 1.04 回
   6 位元（N =    64）：古典平均 32.5 次（約 N/2 = 32）；量子最佳  6 輪，成功率 99.7%，平均要跑 1.00 回
  10 位元（N = 1,024）：古典平均 512.5 次（約 N/2 = 512）；量子最佳 25 輪，成功率 99.9%，平均要跑 1.00 回
五、查詢次數比較表
  位元數 | Deutsch–Jozsa 古典最壞 | BV 古典 | Grover 古典平均 | 量子（DJ、BV／Grover）
       2 |                      3 |       2 |             2.5 | 1、1／1 輪
       3 |                      5 |       3 |             4.5 | 1、1／2 輪
      10 |                    513 |      10 |           512.5 | 1、1／25 輪
      20 |                524,289 |      20 |       524,288.5 | 1、1／804 輪
六、改造區
  10 位元：Deutsch–Jozsa 古典最壞 513 次 vs 量子 1 次；BV 古典 10 次 vs 量子 1 次；Grover 古典平均 512.5 次 vs 量子 25 輪
'''

# 製作代理實跑紀錄：qiskit 2.6.2，Statevector（理論機率）與 StatevectorSampler(seed=2026)，shots=1000（Grover 的次數會隨種子不同）
QISKIT_OUTPUT = '''Deutsch–Jozsa 常數：000 的理論機率 100.0%　量 1000 次，000 出現 1000 次
Deutsch–Jozsa 平衡：000 的理論機率 0.0%　量 1000 次，000 出現 0 次
BV 密碼 101：101 的理論機率 100.0%　量 1000 次，101 出現 1000 次
Grover 答案 101、2 輪：101 的理論機率 94.5%　量 1000 次，101 出現 950 次
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q123：古典 vs 量子——要查幾次？（純 Python，不需安裝任何套件）

執行：  python query_count.py
它印出：
  一、Deutsch（1 位元）：四種黑盒子，古典問 2 次，量子模擬只問 1 次
  二、Deutsch–Jozsa（3 位元）：72 台機器全部用量子模擬跑一次；古典最壞要問幾次；允許出錯時隨便抽幾個問
  三、Bernstein–Vazirani（3 位元）：8 種密碼，古典問 100、010、001 三次；量子只問 1 次
  四、Grover：古典一個一個試平均幾次 vs 量子最佳輪數與成功率
  五、查詢次數比較表（位元數變多時）
  六、改造區：換成自己的位元數，先預測，再執行
量子部分用最簡單的狀態向量模擬（沒有亂數、沒有雜訊）。位元字串最左邊是最高位。
"""
from itertools import combinations
from math import asin, comb, pi, sin, sqrt


def hadamard_all(v, n):
    """對 n 顆位元都做哈達瑪閘"""
    v = v[:]
    for q in range(n):
        bit = 1 << q
        for i in range(2 ** n):
            if not i & bit:
                a, b = v[i], v[i | bit]
                v[i], v[i | bit] = (a + b) / sqrt(2), (a - b) / sqrt(2)
    return v


def one_query(f, n):
    """量子只問一次：H → 黑盒子把 f(x) = 1 的振幅變號（相位回踢）→ H，回傳每個結果的機率"""
    v = [0.0] * 2 ** n
    v[0] = 1.0
    v = hadamard_all(v, n)
    v = [-a if f(x) else a for x, a in enumerate(v)]   # 這一行就是唯一的一次查詢
    v = hadamard_all(v, n)
    return [a * a for a in v]


def bits(x, n):
    return format(x, f'0{n}b')


if __name__ == '__main__':
    print('一、Deutsch（1 位元，四種黑盒子）')
    for name, f in (('f(x) = 0', lambda x: 0), ('f(x) = 1', lambda x: 1), ('f(x) = x', lambda x: x), ('f(x) = 1 − x', lambda x: 1 - x)):
        classical = '常數' if f(0) == f(1) else '平衡'
        p0 = one_query(f, 1)[0]
        quantum = '常數' if p0 > 0.999 else '平衡'
        print(f'  {name:<12} 古典問 f(0)、f(1) 共 2 次 → {classical}；量子問 1 次，量到 0 的機率 {p0:.0%} → {quantum}')

    n = 3
    N = 2 ** n
    print(f'二、Deutsch–Jozsa（{n} 位元，{N} 個輸入）')
    machines = [('常數', frozenset()), ('常數', frozenset(range(N)))]
    machines += [('平衡', frozenset(c)) for c in combinations(range(N), N // 2)]
    right = 0
    for kind, ones in machines:
        p0 = one_query(lambda x: x in ones, n)[0]
        right += (p0 > 0.999) == (kind == '常數')
    print(f'  常數 2 台、平衡 {len(machines) - 2} 台，共 {len(machines)} 台；量子各問 1 次，判斷正確 {right} 台')
    worst = 0
    for k in range(1, N + 1):
        # 前 k 個輸入都回答 0，還有沒有「平衡」的機器符合？有的話就還不能下結論
        if any(kind == '平衡' and not (ones & set(range(k))) for kind, ones in machines):
            worst = k
    print(f'  古典：前 {worst} 個都回答 0，還可能是平衡的 → 最壞要問 {worst + 1} 次（= 2ⁿ⁻¹ + 1）')
    print('  允許出錯：隨便抽 k 個不同的輸入問，平衡機器卻剛好全部同答案（被誤判成常數）的機率')
    print('  ' + '  '.join(f'k = {k}：{2 * comb(N // 2, k) / comb(N, k):.1%}' for k in (2, 3, 4)))

    print(f'三、Bernstein–Vazirani（{n} 位元密碼）')
    ok_c = ok_q = 0
    for s in range(N):
        f = lambda x, s=s: bin(x & s).count('1') % 2     # 黑盒子只回答 s·x 的奇偶
        guess = ''.join(str(f(1 << (n - 1 - i))) for i in range(n))   # 古典依序問 100、010、001
        ok_c += guess == bits(s, n)
        p = one_query(f, n)
        ok_q += p[s] > 0.999
    print(f'  8 種密碼：古典各問 {n} 次全部猜中 {ok_c} 種；量子各問 1 次、量到密碼的機率 100% 的有 {ok_q} 種')

    print('四、Grover（找一個答案）')
    for n2 in (2, 3, 4, 6, 10):
        N2 = 2 ** n2
        th = asin(1 / sqrt(N2))
        r = max(1, round(pi / (4 * th) - 0.5))
        p = sin((2 * r + 1) * th) ** 2
        avg = sum(range(1, N2 + 1)) / N2               # 答案在每個位置機會相同，一個一個試
        print(f'  {n2:>2} 位元（N = {N2:>5,}）：古典平均 {avg:,.1f} 次（約 N/2 = {N2 // 2:,}）；'
              f'量子最佳 {r:>2} 輪，成功率 {p:.1%}，平均要跑 {1 / p:.2f} 回')

    print('五、查詢次數比較表')
    print('  位元數 | Deutsch–Jozsa 古典最壞 | BV 古典 | Grover 古典平均 | 量子（DJ、BV／Grover）')
    for n3 in (2, 3, 10, 20):
        N3 = 2 ** n3
        r = max(1, round(pi / (4 * asin(1 / sqrt(N3))) - 0.5))
        print(f'  {n3:>6} | {2 ** (n3 - 1) + 1:>22,} | {n3:>7} | {(N3 + 1) / 2:>15,.1f} | 1、1／{r:,} 輪')

    # 六、改造區：換成自己的位元數，先預測，再執行
    MY_BITS = 10
    N4 = 2 ** MY_BITS
    r4 = max(1, round(pi / (4 * asin(1 / sqrt(N4))) - 0.5))
    print('六、改造區')
    print(f'  {MY_BITS} 位元：Deutsch–Jozsa 古典最壞 {2 ** (MY_BITS - 1) + 1:,} 次 vs 量子 1 次；'
          f'BV 古典 {MY_BITS} 次 vs 量子 1 次；Grover 古典平均 {(N4 + 1) / 2:,.1f} 次 vs 量子 {r4:,} 輪')
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q123：用本機 Qiskit 驗證三格「量子只問 1 次（或 2 輪）」（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
三個線路都是 3 顆輸入位元；黑盒子用相位翻轉閘寫成「把答案變號」的版本（和 query_count.py 一樣）。
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


def dj(balanced):
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])
    if balanced:
        qc.z([0, 1, 2])          # 平衡：f(x) = 三個位元的奇偶（只問 1 次）
    qc.h([0, 1, 2])
    return qc


def bv(secret='101'):
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])
    for q in range(3):
        if secret[2 - q] == '1':
            qc.z(q)              # 黑盒子：s·x 是奇數的項變號（只問 1 次）
    qc.h([0, 1, 2])
    return qc


def ccz(qc):
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)


def grover(answer='101', rounds=2):
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])
    zeros = [q for q in range(3) if answer[2 - q] == '0']
    for _ in range(rounds):
        if zeros:
            qc.x(zeros)
        ccz(qc)                  # 標記：每一輪問 1 次
        if zeros:
            qc.x(zeros)
        qc.h([0, 1, 2])
        qc.x([0, 1, 2])
        ccz(qc)
        qc.x([0, 1, 2])
        qc.h([0, 1, 2])
    return qc


sampler = StatevectorSampler(seed=2026)
for name, qc, key in (('Deutsch–Jozsa 常數', dj(False), '000'), ('Deutsch–Jozsa 平衡', dj(True), '000'),
                      ('BV 密碼 101', bv(), '101'), ('Grover 答案 101、2 輪', grover(), '101')):
    p = Statevector(qc).probabilities_dict().get(key, 0)
    m = qc.copy()
    m.measure_all()
    counts = sampler.run([m], shots=1000).result()[0].data.meas.get_counts()
    print(f'{name}：{key} 的理論機率 {p:.1%}　量 1000 次，{key} 出現 {counts.get(key, 0)} 次')
'''

TABLE = [  # (問題, 黑盒回答什麼, 古典, 量子, 加速, 動畫驗證)
    ('Deutsch（1 位元）', 'f(x)，x 是 1 個位元', '2 次', '1 次', '2 → 1', '—'),
    ('Deutsch–Jozsa（n 位元）', 'f(x)，保證常數或平衡', '最壞 2ⁿ⁻¹ + 1 次（3 位元 5 次）', '1 次', '指數級（不允許出錯時）', 'operation.html#interference'),
    ('Bernstein–Vazirani', 's·x（mod 2）的奇偶', 'n 次（100、010、001）', '1 次', 'n → 1', 'transmon-3d.html#bv 步驟 1、5'),
    ('Grover 搜尋', 'x 是不是答案', '平均 (N + 1)/2 次（約 N/2）', '約 (π/4)√N 輪', '平方級', 'operation.html#grover'),
    ('Shor 分解質因數', '（不是黑盒查詢題）', '次指數時間（一般數域篩法）', '多項式時間', '指數級（超多項式）', '—'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q123：古典 vs 量子——要查幾次？（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的第十一課。
前面幾課分別做過 Deutsch（Q107、Q119）、BV（Q105、Q120）、Grover（Q106、Q121、Q122）；今天不學新線路，而是把它們排進同一張表比「要查幾次」，再補上 Shor。
核心一句話：**量子快多少要看問題的結構：Deutsch、BV 只問 1 次；Grover 只快一個平方根；排序、資料載入這類問題沒有已知的量子加速。**

## 查詢次數比較表（basic-circuits.pptx 第 30 頁；Shor 與加速等級見 QC_Operation_Talk.pptx 第 42 頁）

| 問題 | 黑盒回答什麼 | 古典 | 量子 | 加速 | 動畫驗證 |
|---|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in TABLE) + '''
- 「一次查詢」＝把一個輸入丟進黑盒子、拿回一個答案。比的是查詢次數，不是閘數或秒數。量子特別的地方，是把所有輸入的疊加一起丟進去，答案寫進每一項的正負號，再用 H 干涉讀出。
- Deutsch–Jozsa 為什麼是 2ⁿ⁻¹ + 1：平衡機器有一半回答 1；如果先問到的一半剛好都是 0，還不能排除「剩下一半全是 1」。3 位元 5 次、10 位元 513 次（query_count.py 第二、五段）。
- BV：古典每次只讓一位是 1（100、010、001），一次拿回一位，n 位元要 n 次；這已經是最少（Wikipedia：at least n queries）。
- Grover：古典一個一個試，平均 (N + 1)/2 次（簡報第 26 頁；Wikipedia 與 operation.html 讀數寫約 N/2）；量子約 (π/4)√N 輪，每輪查一次黑盒。N = 8：4.5 次 vs 2 輪；N = 1,024：512.5 次 vs 25 輪。
- Shor：古典最好的一般數域篩法是次指數時間，Shor 是多項式時間（Wikipedia；QC_Operation_Talk 第 42 頁）。

## 容易錯的地方與限制（驗收要孩子說出至少一個）

1. **查詢次數少不等於總時間少**：量子閘比古典運算慢，錯誤更正有額外開銷；平方加速要問題非常大才划算（QC_Operation_Talk 第 42 頁；Wikipedia：the quadratic speedup … too modest to overcome the large overhead of near-term quantum computers）。
2. **還要算量測與重複次數**：Grover 的成功率不一定 100%（N = 8 是 94.5%），真實機器還有雜訊，要跑很多 shots。
3. **允許出錯時古典也很快**：3 位元 Deutsch–Jozsa 隨便抽 4 個不同輸入問，平衡機器被誤判成常數的機率只有 2.9%（query_count.py 第二段）；所以 Deutsch–Jozsa 的「指數」優勢只在「完全不准出錯」時成立。
4. 這些是教學用的黑盒問題，本身不實用（basic-circuits.pptx 第 30 頁備註、Wikipedia：of little practical use）。

## 孩子獨立改造：量子沒有優勢的問題（QC_Operation_Talk.pptx 第 45 頁）

- 資料輸入：載入 N 筆資料要約 N 步（例：把一整本相簿讀進電腦）。
- 資料輸出：n 個量子位元只能讀出 n 位元。
- 沒有結構的一般計算：加減乘除、排序、資料庫查詢、渲染、文書——沒有已知的量子加速（例：把一萬個數字排序）。
- 小規模問題：量子閘約 100 ns、錯誤更正開銷大，問題不夠大時古典更快。
- 對照：最適合量子的是「輸入小、計算難、輸出小」，例如分解質因數。

## 影片的念法

Deutsch 念「德意志」；BV 說「密碼問題」；Deutsch–Jozsa 說「三位元的德意志問題」；Grover 念「格羅弗」；Shor 念「秀爾」；π 說「圓周率」；Qiskit 說「量子程式套件」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；說明工程答辯規則：每填一格都要說出依據 | 影片、列印包第 1 頁 |
| 10–25 | 對照 basic-circuits.pptx 第 30 頁與 QC_Operation_Talk.pptx 第 42 頁，把四列的古典、量子次數讀一遍 | 簡報 |
| 25–65 | 畫比較表；三個動畫各驗證一格並打勾；跑 query_count.py 對答案 | `01_操作步驟.md`、列印包第 1、2 頁、`03_查詢次數比較表.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子找一個量子沒有優勢的問題，說明原因；（選用）qiskit_check.py | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼只問一次、Grover 為什麼要 √N 輪、一個注意事項 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#interference`（場景 8）、`operation.html#grover`（場景 9）與 `transmon-3d.html#bv`（第 9 章）。
- 打開 `slides/output/basic-circuits.pptx` 第 30 頁與 `slides/QC_Operation_Talk.pptx` 第 42、45 頁（課綱頁碼正確）。
- 列印 `02_列印包_查詢次數比較表.pdf`（A4，共 4 頁）。
- 有 Python 的電腦先跑一次 `python query_count.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 動畫與程式都是理想模擬；真實的量子電腦有閘與讀取誤差。
- operation.html#grover 的讀數「古典平均要查 N/2 次」和簡報第 26 頁的 (N + 1)/2 差 0.5，是不同的算法約定；兩者都是「大約一半」。
- transmon-3d.html 第 9 章導覽步驟的面板「查詢次數」一直寫「量子 0 次」（只有第 8 步自由實驗才累加），以看板文字為準。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：畫比較表，動畫驗證三格（約 40 分鐘）

1. 在列印包第 1 頁畫好比較表：問題、黑盒回答什麼、古典幾次、量子幾次、加速等級、驗證。先不看簡報，自己填一次；再對照 basic-circuits.pptx 第 30 頁。
2. **第一格：Deutsch–Jozsa 古典最壞 5 次**。開 `operation.html#interference`，按「3 位元：8 條路徑（Deutsch–Jozsa）」，把左邊面板捲到最下面。
   依序按「平衡 f = x₀」「常數 f = 0」「常數 f = 1」「平衡 f = 奇偶」，記下讀數「f(x) = 1 的有幾個」（4、0、8、4）和 P(000)（0、1、1、0）；最後一行寫著「古典最壞要查 2ⁿ⁻¹+1 = 5 次」。打勾。
3. **第二格：BV 古典 3 次、量子 1 次**。開 `transmon-3d.html#bv`（第 9 章），取消「自動接續」，按步驟「1」看古典依序問 100、010、001，看板寫「古典問了 3 次才知道 s = 101」；
   再按步驟「5」：量 50 次都是 101，看板寫「量子：查詢 1 次 → s = 101」「古典：查詢 3 次（n 位元要 n 次）」。打勾。
4. **第三格：Grover 古典平均 vs 最佳輪數**。開 `operation.html#grover`（場景 9），把「量子位元數 n」拉到 2、3、4、5、6，記下讀數「最佳輪數 ≈ …　古典平均要查 … 次」；
   n = 6 時按「自動跑到最佳次數」，看讀數停在 P = 0.997。打勾。
5. 跑 `python query_count.py`，對照第一到五段，看程式印出的次數和表上寫的一不一樣。

## 下半場：量子沒有優勢的問題（約 30 分鐘）

1. 孩子在列印包第 3 頁寫一個量子沒有優勢的問題（例：排序、把整本相簿讀進電腦、算家裡的帳），用 QC_Operation_Talk.pptx 第 45 頁的五個理由說明原因。
2. 再寫一個「輸入小、計算難、輸出小」的例子（例：分解很大的數），說明為什麼它適合量子。
3. 改造：把 query_count.py 最下面的 `MY_BITS` 改成別的位元數（例如 4、16、20），先預測三種問題的古典次數，再執行看第六段。
4. 有裝 Qiskit 的話，跑 `python qiskit_check.py`：Deutsch–Jozsa 常數／平衡、BV 101、Grover 101 兩輪的理論機率是 100%／0%／100%／94.5%，再各量 1000 次（Grover 的次數是隨機的）。
''',

'query_count.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## query_count.py 實跑輸出（Python 3.13.18，沒有亂數）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，Statevector；StatevectorSampler seed=2026，Grover 的次數會隨種子不同）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 動畫驗證三格的讀數\n\n'
  '- operation.html#interference（3 位元）：平衡 f = x₀ 有 4 個、P(000) = 0.000；常數 f = 0 有 0 個、1.000；常數 f = 1 有 8 個、1.000；平衡 f = 奇偶 有 4 個、0.000；「古典最壞要查 2ⁿ⁻¹+1 = 5 次」。\n'
  '- transmon-3d.html#bv：步驟 1 看板「古典第 1 次：x = 100 → 回答 1 … 古典問了 3 次才知道 s = 101」；步驟 5「量子：查詢 1 次 → s = 101」「古典：查詢 3 次（n 位元要 n 次）」。\n'
  '- operation.html#grover：n = 2／3／4／5／6 → 最佳 1／2／3／4／6 輪，古典平均要查 2／4／8／16／32 次；n = 6 自動跑到最佳次數 P = 0.997。\n\n'
  '## 常見問題\n\n'
  '- 為什麼 Deutsch–Jozsa 古典最壞要 2ⁿ⁻¹ + 1 次？平衡機器有一半回答 1；先問到的一半都回答 0 時，還可能是「另一半全是 1」的平衡機器，要再問一個。\n'
  '- 為什麼 BV 古典要 n 次？每次查詢只回答 1 個位元（0 或 1），密碼有 n 個位元，至少要 n 次。\n'
  '- 為什麼 Grover 量子要約 √N 輪、不是 1 次？黑盒一次只能把答案標記一點點，每輪把答案的振幅推高一點，要重複約 (π/4)√N 輪（簡報第 30 頁備註）。\n'
  '- Shor 也是查詢次數嗎？不是黑盒查詢題；比的是總計算時間：古典次指數、量子多項式。\n'
  '- 量子沒有優勢的例子：排序、加減乘除、把大量資料讀進來、只需要很小規模的問題（QC_Operation_Talk 第 45 頁）。\n'
  '- 下一課 Q124：用 Qiskit 重現八個範例。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號（operation.html、transmon-3d.html 需要能載入 three.js）。

## `animations/operation.html#interference`（場景 8 干涉）

- 上方兩個模式：「單一量子位元：兩條路徑」「3 位元：8 條路徑（Deutsch–Jozsa）」。3 位元模式的函數按鈕：常數 f = 0、常數 f = 1、平衡 f = x₀、平衡 f = 奇偶、隨機（非保證）。
- 面板讀數：「f(x) = 1 的有幾個」、|000⟩ 的振幅與 P(000)、「常數函數：完全相長／平衡函數：完全相消　（古典最壞要查 2ⁿ⁻¹+1 = 5 次）」。面板很長，捲到最下面才看得到讀數。
- 「隨機（非保證）」每按一次重抽，結果不一定是常數或平衡，不適合用來驗證表格。

## `animations/transmon-3d.html#bv`（第 9 章 BV 密碼）

- 步驟 1「題目與古典做法」：古典依序問 100、010、001，看板一行一行寫出回答。步驟 5「量測」：量 50 次都是 101，看板寫量子 1 次、古典 3 次。
- 「自動接續」打勾時會自己播下一步；要停在某一步就取消勾選。步驟 8 是自由實驗（可以換密碼、按「古典查詢一次」）。

## `animations/operation.html#grover`（場景 9 Grover 搜尋）

- 滑桿「量子位元數 n」（2–6）；讀數第三行「最佳輪數 ≈ (π/4)√N ≈ …　古典平均要查 N/2 次」。
- 「自動跑到最佳次數」：自動交替標記與擴散，做到最佳輪數就停；標記時出現粉紅色平均面；右下插圖白點沿「P(成功) vs 輪數」曲線移動。
''',
}

SHEET_HEADER = ['問題', '黑盒回答什麼', '古典要問幾次', '量子要問幾次', '加速等級', '動畫驗證（打勾）', '依據（簡報頁、動畫、程式）']
SHEET_ROWS = [['Deutsch（1 位元）', 'f(x)', '2 次', '1 次', '', '—', 'basic-circuits p30'],
              ['Deutsch–Jozsa（3 位元）', '', '', '', '', '', ''],
              ['Bernstein–Vazirani（3 位元）', '', '', '', '', '', ''],
              ['Grover（N = 8、64）', '', '', '', '', '', ''],
              ['Shor', '', '', '', '', '—', '']]

EXTRA_CSS = '''table.rec td{height:11mm;font-size:10.5pt}table.rec td.k{font-weight:bold;color:#0b2540;width:20%}
table.rec th{font-size:9.5pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 query_count.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'query_count.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    row = lambda k, a='', b='', c='', d='', e='': f'<tr><td class="k">{k}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>'  # noqa: E731
    pages = [
        '<h2>查詢次數比較表</h2><p class="lead">工程答辯：每填一格，都要說出依據（簡報頁、動畫、程式）。先自己填，再對照 basic-circuits.pptx 第 30 頁與 QC_Operation_Talk.pptx 第 42 頁。</p>'
        '<table class="rec"><tr><th style="width:20%">問題</th><th>黑盒回答什麼</th><th>古典要問幾次</th><th>量子要問幾次</th><th>加速等級</th><th style="width:10%">驗證 ✓</th></tr>'
        + row('Deutsch（1 位元）', 'f(x)', '2 次', '1 次', '', '—')
        + row('Deutsch–Jozsa（3 位元）') + row('BV 密碼（3 位元）') + row('Grover（N = 8）') + row('Grover（N = 1,024）')
        + row('Shor', '（不是黑盒題）', '', '', '', '—') + '</table>'
        '<p>哪一列的量子優勢最大？＿＿＿＿＿＿　哪一列只有平方根加速？＿＿＿＿＿＿</p>',
        '<h2>動畫驗證三格</h2><p class="lead">每驗證一格，在比較表的「驗證」欄打勾。</p>'
        '<table class="rec"><tr><th style="width:20%">動畫</th><th>我按了什麼</th><th>畫面讀數（照抄）</th><th>驗證了哪一格</th></tr>'
        '<tr><td class="k">operation.html<br>#interference</td><td>3 位元模式；f = x₀、常數 0、常數 1、奇偶</td><td>回答一的有＿、＿、＿、＿個；古典最壞＿次</td><td></td></tr>'
        '<tr><td class="k">transmon-3d.html<br>#bv</td><td>取消自動接續；步驟 1、步驟 5</td><td>古典問了＿次；量子查詢＿次</td><td></td></tr>'
        '<tr><td class="k">operation.html<br>#grover</td><td>n = 2、3、4、5、6；自動跑到最佳次數</td><td>古典平均＿、＿、＿、＿、＿次；最佳＿、＿、＿、＿、＿輪；P = ＿＿</td><td></td></tr></table>'
        '<p>n 每加 1，古典平均變成幾倍？＿＿　最佳輪數大約變成幾倍？＿＿</p><div class="line"></div>'
        '<p>query_count.py 印出的次數和表上一樣嗎？哪裡不一樣（提示：N/2 和 (N + 1)/2）？</p><div class="line"></div>',
        '<h2>量子沒有優勢的問題</h2><p class="lead">孩子獨立改造：找一個量子沒有優勢的問題，用 QC_Operation_Talk.pptx 第 45 頁說明原因。</p>'
        '<div class="box"><p>我的問題：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>原因（圈一個以上）：資料輸入要約 N 步　／　只能讀出 n 位元　／　一般計算沒有已知加速　／　問題太小　／　要很多 shots</p>'
        '<p>我的說明：</p><div class="line"></div><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><p>相反的例子（輸入小、計算難、輸出小）：＿＿＿＿＿＿＿＿＿＿＿＿</p><div class="line"></div></div>'
        '<pre class="code"># query_count.py 最下面的改造區：換成自己的位元數\n'
        'MY_BITS = 10\n'
        '# 先預測三種問題的古典次數，再執行 python query_count.py，看第六段</pre>'
        '<p>MY_BITS = ＿＿：Deutsch–Jozsa 古典最壞＿＿＿次；BV＿＿＿次；Grover 古典平均＿＿＿次 vs 量子＿＿＿輪</p>',
        '<h2>最後一關：答辯查詢次數</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 為什麼 Deutsch 和 BV 量子只要問一次（不看稿）：</p><div class="line"></div>'
        '<p>2. 為什麼 Grover 要問大約 √N 輪：</p><div class="line"></div>'
        '<p>3. 一個注意事項或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>完成查詢次數比較表：Deutsch、Deutsch–Jozsa、BV、Grover、Shor</li><li>三個動畫各驗證一格並打勾</li>'
        '<li>說出：Deutsch–Jozsa 古典最壞 2ⁿ⁻¹ + 1 次，3 位元 5 次</li><li>說出：Grover 是平方根加速，Shor 是指數級</li>'
        '<li>指出：查詢少不等於總時間少；還要算量測、重複與錯誤更正</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q123 查詢次數比較表 列印包', '父子科技學院 量子電腦學程 Q123｜古典 vs 量子：要查幾次？', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q123-query-count', folder='Q123_古典vs量子_要查幾次', files=FILES,
        sheet=('03_查詢次數比較表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_查詢次數比較表.pdf', pack_pages=4,
        pack_needles=('查詢次數比較表', '動畫驗證三格', '量子沒有優勢', 'MY_BITS', '最後一關'),
        authoring_dir=XINEW / 'authoring/q123', episode_dir='specials/q123-query-count',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；query_count.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'query_count.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, no randomness); qiskit 2.6.2',
               'recordedRun': {'deutsch': {'classical': 2, 'quantum': 1},
                               'deutschJozsa3': {'machines': 72, 'quantumCorrect': 72, 'classicalWorst': 5,
                                                 'randomMisjudge': {'2': 0.429, '3': 0.143, '4': 0.029}},
                               'bv3': {'classical': 3, 'quantum': 1, 'secretsCorrect': 8},
                               'grover': {'N': [4, 8, 16, 64, 1024], 'classicalAverage': [2.5, 4.5, 8.5, 32.5, 512.5],
                                          'bestRounds': [1, 2, 3, 6, 25], 'success': [1.0, 0.945, 0.961, 0.997, 0.999]},
                               'tenBits': {'deutschJozsaWorst': 513, 'bv': 10, 'groverClassicalAverage': 512.5, 'groverRounds': 25}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q123/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

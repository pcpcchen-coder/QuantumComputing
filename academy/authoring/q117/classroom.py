"""Q117 課堂教材：GHZ 逐步圖、量測紀錄表、少接一條的改造單、可執行的 ghz_lab.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#ghz 與 operation.html#register；ghz_lab.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 ghz_lab.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q117/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，random.Random(1117)（固定種子；換種子或換電腦的 Python 版本，次數可能不同）
RUN_OUTPUT = '''一、三顆逐步看：每一步多綁一顆（只列出不是 0 的柱子；最後是「單看每一顆」的 Bloch 向量大小）
  起點            |000⟩ +1.000                      單看 q0 1.0  q1 1.0  q2 1.0
  H(q0)         |000⟩ +0.707  |001⟩ +0.707        單看 q0 1.0  q1 1.0  q2 1.0
  CNOT(q0→q1)   |000⟩ +0.707  |011⟩ +0.707        單看 q0 0.0  q1 0.0  q2 1.0
  CNOT(q1→q2)   |000⟩ +0.707  |111⟩ +0.707        單看 q0 0.0  q1 0.0  q2 0.0
二、四顆逐步看：多一個 CNOT(q2→q3)
  起點            |0000⟩ +1.000                     單看 q0 1.0  q1 1.0  q2 1.0  q3 1.0
  H(q0)         |0000⟩ +0.707  |0001⟩ +0.707      單看 q0 1.0  q1 1.0  q2 1.0  q3 1.0
  CNOT(q0→q1)   |0000⟩ +0.707  |0011⟩ +0.707      單看 q0 0.0  q1 0.0  q2 1.0  q3 1.0
  CNOT(q1→q2)   |0000⟩ +0.707  |0111⟩ +0.707      單看 q0 0.0  q1 0.0  q2 0.0  q3 1.0
  CNOT(q2→q3)   |0000⟩ +0.707  |1111⟩ +0.707      單看 q0 0.0  q1 0.0  q2 0.0  q3 0.0
三、各量測 1000 次（random 種子 1117）
  3 顆： 000 → 495 次  111 → 505 次
  4 顆： 0000 → 470 次  1111 → 530 次
四、故意少接一條 CNOT
  3 顆少接 CNOT(q0→q1) 只量到 000、001     沒綁上（向量還是 1）：q0、q1、q2
  3 顆少接 CNOT(q1→q2) 只量到 000、011     沒綁上（向量還是 1）：q2
  4 顆少接 CNOT(q0→q1) 只量到 0000、0001   沒綁上（向量還是 1）：q0、q1、q2、q3
  4 顆少接 CNOT(q1→q2) 只量到 0000、0011   沒綁上（向量還是 1）：q2、q3
  4 顆少接 CNOT(q2→q3) 只量到 0000、0111   沒綁上（向量還是 1）：q3
五、另一種接法：全部由 q0 控制
  3 顆 H(q0) → CNOT(q0→q1) → CNOT(q0→q2)   和串下去一樣嗎？ True
  4 顆 H(q0) → CNOT(q0→q1) → CNOT(q0→q2) → CNOT(q0→q3)   和串下去一樣嗎？ True
六、玩具雜訊模型：每個 CNOT 之後，目標位元有 2% 機率被翻錯（精確計算）
  2 顆（1 個 CNOT）：量到全 0、全 1 以外的機率 2.0%
  3 顆（2 個 CNOT）：量到全 0、全 1 以外的機率 4.0%
  4 顆（3 個 CNOT）：量到全 0、全 1 以外的機率 5.9%
  5 顆（4 個 CNOT）：量到全 0、全 1 以外的機率 7.8%
  6 顆（5 個 CNOT）：量到全 0、全 1 以外的機率 9.6%
  7 顆（6 個 CNOT）：量到全 0、全 1 以外的機率 11.4%
  8 顆（7 個 CNOT）：量到全 0、全 1 以外的機率 13.2%
七、改造區
  H(q0) → CNOT(q0→q1) → CNOT(q2→q3)
    只量到 0000、0011   單看 q0 0.0  q1 0.0  q2 1.0  q3 1.0
'''

# 製作代理實跑紀錄：qiskit 2.6.2，StatevectorSampler(seed=2026)，shots=1000（四個線路用同一個種子，所以次數的數字相同、對應的結果不同）
QISKIT_OUTPUT = '''3 顆 理論機率 {'000': 0.5, '111': 0.5} 量測 1000 次 {'000': 464, '111': 536}
4 顆 理論機率 {'0000': 0.5, '1111': 0.5} 量測 1000 次 {'0000': 464, '1111': 536}
3 顆，少接 CNOT(q1→q2) 理論機率 {'000': 0.5, '011': 0.5} 量測 1000 次 {'000': 464, '011': 536}
4 顆，少接 CNOT(q1→q2) 理論機率 {'0000': 0.5, '0011': 0.5} 量測 1000 次 {'0000': 464, '0011': 536}
     ┌───┐               
q_0: ┤ H ├──■────────────
     └───┘┌─┴─┐          
q_1: ─────┤ X ├──■───────
          └───┘┌─┴─┐     
q_2: ──────────┤ X ├──■──
               └───┘┌─┴─┐
q_3: ───────────────┤ X ├
                    └───┘
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q117：範例 4 GHZ——CNOT 一路串下去（純 Python，不需安裝任何套件）

執行：  python ghz_lab.py
它用一個很小的多位元模擬器（只認得 H、X、CNOT），印出：
  一、三顆逐步看振幅：H（q0）→ CNOT（q0 → q1）→ CNOT（q1 → q2），每一步「單看每一顆」的 Bloch 向量大小
  二、四顆逐步看：多一個 CNOT（q2 → q3）
  三、三顆、四顆各量測 1000 次（固定的亂數種子；換種子次數會不一樣）
  四、故意少接一條 CNOT：結果變成什麼、哪幾顆沒綁上
  五、另一種接法：全部由 q0 控制，結果一樣嗎？
  六、玩具雜訊模型：每個 CNOT 之後，目標位元有 2% 機率被翻錯；位元越多，全 0、全 1 以外的比例越高
  七、改造區：自己排一條線路，先預測，再執行
位元字串寫成 |… q2 q1 q0⟩：最右邊那位是 q0（和 Qiskit、basic-circuits.html 一樣）。
"""
import random
from math import sqrt

R2 = 1 / sqrt(2)


def run(n, gates):
    """n 顆位元從 |0…0⟩ 出發，依序做 gates，回傳 2ⁿ 個振幅（第 i 根柱子 = i 的二進位字串）
    閘的寫法：('h', q)、('x', q)、('cx', 控制, 目標)"""
    s = [0.0] * (1 << n)
    s[0] = 1.0
    for g in gates:
        if g[0] == 'cx':
            c, t = 1 << g[1], 1 << g[2]
            s = [s[i ^ t] if i & c else s[i] for i in range(len(s))]
            continue
        name, m = g[0], 1 << g[1]
        new = s[:]
        for i in range(len(s)):
            if i & m:
                continue
            a, b = s[i], s[i | m]                       # 這一顆是 0、是 1 的兩個振幅
            if name == 'h':
                new[i], new[i | m] = (a + b) * R2, (a - b) * R2
            elif name == 'x':
                new[i], new[i | m] = b, a
            else:
                raise ValueError('只認得 h、x、cx：' + name)
        s = new
    return s


def bits(i, n):
    return format(i, f'0{n}b')


def size(s, q):
    """單看第 q 顆的 Bloch 向量大小（振幅都是實數，所以只有 x、z 兩個分量）"""
    m = 1 << q
    x = sum(2 * s[i] * s[i | m] for i in range(len(s)) if not i & m)
    z = sum((-1 if i & m else 1) * a * a for i, a in enumerate(s))
    return sqrt(x * x + z * z)


def bars(s, n):
    """只列出不是 0 的柱子"""
    return '  '.join(f'|{bits(i, n)}⟩ {a:+.3f}' for i, a in enumerate(s) if abs(a) > 1e-9)


def sizes(s, n):
    return '  '.join(f'q{q} {size(s, q):.1f}' for q in range(n))


def gname(g):
    return f'CNOT(q{g[1]}→q{g[2]})' if g[0] == 'cx' else f'{g[0].upper()}(q{g[1]})'


def ghz(n):
    """範例 4 的接法：H(q0)，再 CNOT 一路串下去 q0→q1、q1→q2、…"""
    return [('h', 0)] + [('cx', i, i + 1) for i in range(n - 1)]


def outcomes(s, n):
    return [bits(i, n) for i, a in enumerate(s) if a * a > 1e-9]


def shots(s, n, k, rng):
    """全部一起量 k 次：每次以機率 振幅² 得到其中一個位元字串；只列出有出現的"""
    counts = {}
    for _ in range(k):
        r, i = rng.random(), 0
        while i < len(s) - 1 and r >= s[i] ** 2:
            r -= s[i] ** 2
            i += 1
        counts[bits(i, n)] = counts.get(bits(i, n), 0) + 1
    return dict(sorted(counts.items()))


def show_steps(n):
    gates = ghz(n)
    print(f'  {"起點":<14}{bars(run(n, []), n):<34}單看 {sizes(run(n, []), n)}')
    for k in range(1, len(gates) + 1):
        s = run(n, gates[:k])
        print(f'  {gname(gates[k - 1]):<14}{bars(s, n):<34}單看 {sizes(s, n)}')


def noisy_outside(n, p):
    """玩具雜訊模型（精確計算，不抽樣）：每個 CNOT 之後，目標位元以機率 p 被多翻一次。
    把所有「哪幾個 CNOT 出錯」的情形都算一遍，加總量到全 0、全 1 以外的機率。"""
    gates, total = ghz(n), 0.0
    cxs = [i for i, g in enumerate(gates) if g[0] == 'cx']
    for pattern in range(1 << len(cxs)):
        seq, w = [], 1.0
        for j, g in enumerate(gates):
            seq.append(g)
            if g[0] == 'cx':
                err = (pattern >> cxs.index(j)) & 1
                w *= p if err else 1 - p
                if err:
                    seq.append(('x', g[2]))
        s = run(n, seq)
        total += w * sum(a * a for i, a in enumerate(s) if i not in (0, (1 << n) - 1))
    return total


if __name__ == '__main__':
    rng = random.Random(1117)
    print('一、三顆逐步看：每一步多綁一顆（只列出不是 0 的柱子；最後是「單看每一顆」的 Bloch 向量大小）')
    show_steps(3)
    print('二、四顆逐步看：多一個 CNOT(q2→q3)')
    show_steps(4)
    print('三、各量測 1000 次（random 種子 1117）')
    for n in (3, 4):
        print(f'  {n} 顆：', '  '.join(f'{k} → {v} 次' for k, v in shots(run(n, ghz(n)), n, 1000, rng).items()))
    print('四、故意少接一條 CNOT')
    for n in (3, 4):
        full = ghz(n)
        for j in range(1, len(full)):
            g = full[:j] + full[j + 1:]
            s = run(n, g)
            loose = [f'q{q}' for q in range(n) if size(s, q) > 0.5]
            print(f'  {n} 顆少接 {gname(full[j]):<12}只量到 {"、".join(outcomes(s, n)):<12}沒綁上（向量還是 1）：{"、".join(loose)}')
    print('五、另一種接法：全部由 q0 控制')
    for n in (3, 4):
        star = [('h', 0)] + [('cx', 0, i) for i in range(1, n)]
        print(f'  {n} 顆 ' + ' → '.join(gname(x) for x in star) + f'   和串下去一樣嗎？ {run(n, star) == run(n, ghz(n))}')
    print('六、玩具雜訊模型：每個 CNOT 之後，目標位元有 2% 機率被翻錯（精確計算）')
    for n in range(2, 9):
        print(f'  {n} 顆（{n - 1} 個 CNOT）：量到全 0、全 1 以外的機率 {noisy_outside(n, 0.02) * 100:.1f}%')

    # 七、改造區：先預測，再執行。閘寫成 ('h', 0)、('x', 1)、('cx', 0, 1)，由左往右排
    N, MY_CIRCUIT = 4, [('h', 0), ('cx', 0, 1), ('cx', 2, 3)]
    print('七、改造區')
    s = run(N, MY_CIRCUIT)
    print('  ' + ' → '.join(gname(x) for x in MY_CIRCUIT))
    print(f'    只量到 {"、".join(outcomes(s, N))}   單看 {sizes(s, N)}')
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q117：用本機 Qiskit 重現 3 顆、4 顆 GHZ 態（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


def ghz(n, skip=None):
    """H(q0)，再 CNOT 一路串下去；skip = 故意少接的那一條（例如 1 代表少接 CNOT(q1→q2)）"""
    qc = QuantumCircuit(n)
    qc.h(0)                          # 哈達瑪閘：q0 進入疊加
    for i in range(n - 1):
        if i != skip:
            qc.cx(i, i + 1)          # 受控反閘：q(i) 控制 q(i+1)，一路串下去
    return qc


for n, skip in ((3, None), (4, None), (3, 1), (4, 1)):
    qc = ghz(n, skip)
    probs = Statevector.from_instruction(qc).probabilities_dict()
    m = qc.copy()
    m.measure_all()
    counts = StatevectorSampler(seed=2026).run([m], shots=1000).result()[0].data.meas.get_counts()
    tag = f'{n} 顆' + ('' if skip is None else f'，少接 CNOT(q{skip}→q{skip + 1})')
    print(tag, '理論機率', {str(k): round(float(v), 3) for k, v in sorted(probs.items())}, '量測 1000 次', dict(sorted(counts.items())))
print(ghz(4).draw())
'''

STEPS3 = [  # (步驟, 閘, 不是 0 的柱子 |q2 q1 q0⟩, 綁住幾顆)
    ('起點', '—', '|000⟩', '0（還沒有糾纏）'),
    ('第 1 步', 'H（q0）', '|000⟩、|001⟩ 各 +0.707', '0（q0 只是疊加）'),
    ('第 2 步', 'CNOT（q0 → q1）', '|000⟩、|011⟩ 各 +0.707', '2 顆（q0、q1）'),
    ('第 3 步', 'CNOT（q1 → q2）', '|000⟩、|111⟩ 各 +0.707', '3 顆（全部）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q117：範例 4 GHZ——CNOT 一路串下去（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的範例 4。
上一課（Q116）用 H 加一個 CNOT 綁住兩顆位元（Bell 態）；今天工具不換，只把 CNOT 一個接一個串下去：H(q0) → CNOT(q0 → q1) → CNOT(q1 → q2) → …
核心一句話：**每多接一個 CNOT，就多綁一顆位元；綁 N 顆需要 N − 1 個 CNOT，量起來不是全 0 就是全 1。**

## GHZ 逐步圖（作品的答案，3 顆）

位元字串寫成 |q2 q1 q0⟩，最右邊那位是 q0（和 Qiskit、basic-circuits.html 一樣）。

| 步驟 | 閘 | 不是 0 的柱子 | 綁住幾顆 |
|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in STEPS3) + '''
4 顆多一步：CNOT（q2 → q3），柱子 |0111⟩ 搬到 |1111⟩，最後只剩 |0000⟩、|1111⟩。

「綁住幾顆」的判斷：單看那一顆的 Bloch 向量大小，1 代表還沒綁上，0 代表已經和別人糾纏（ghz_lab.py 會印出來；operation.html#register 左下也有讀數）。

## 故意少接一條（改造的答案）

- 3 顆少接最後一條 CNOT(q1→q2)：q2 一直是 0，只量到 000、011（q0、q1 是一對 Bell 態，q2 沒綁上）。
- 3 顆少接第一條 CNOT(q0→q1)：q1 一直是 0，所以 CNOT(q1→q2) 從來不會翻；只量到 000、001，只剩 q0 自己在擲硬幣。
- 4 顆少接中間 CNOT(q1→q2)：q2、q3 都綁不上，只量到 0000、0011。這就是「一環扣一環」：中間斷一環，後面全部鬆開。
- 另一種接法：全部由 q0 控制（CNOT(q0→q1)、CNOT(q0→q2)…）結果一樣是 GHZ 態（ghz_lab.py 第五段印出 True）；transmon-3d.html#stack 的自由實驗就是用這種接法。

## 常見誤解

- CNOT 的「複製」只是讓 0 對 0、1 對 1（計算基底上的對應），不是把一個未知的量子態複製一份——那是不可能的（不可複製定理）。
- 動畫是理想模擬，只會量到全 0、全 1。真機有雜訊，會出現其他組合；位元越多、CNOT 越多，出錯的機會越多。硬體常用 GHZ 態測試多位元糾纏的品質。
- ghz_lab.py 第六段的雜訊是**玩具模型**（每個 CNOT 之後目標位元有 2% 機率被翻錯），只用來看「越多顆越糟」的趨勢，不是任何真實硬體的數字。

## 影片的念法

H 念「哈達瑪閘」、CNOT「受控反閘」；GHZ 不念字母，說「範例四」「全零、全一」；q0、q1、q2、q3 念「編號零」到「編號三」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 對照簡報第 13–14 頁：範例 4 線路、振幅逐步看（001 → 011 → 111） | 簡報 basic-circuits.pptx p13–14 |
| 25–65 | 在 basic-circuits.html#ghz 位元數選 3 顆、4 顆，各從起點逐步播放、量測 1,000 次；畫逐步圖、填量測紀錄 | `01_操作步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子在 ghz_lab.py 故意少接一條 CNOT，先預測再執行；看玩具雜訊模型；選用 operation.html#register 三顆一節一節接 | 列印包第 3 頁、`03_逐步圖與改造紀錄.csv` |
| 105–115 | 孩子教爸爸：線路、規則、容易錯的地方 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#ghz`：上方「位元數」切換 3 顆／4 顆，按「⏮ 起點」「下一步 ▶」與「量測 1,000 次」。
- 選用：開 `operation.html#register`（場景 4），滑桿「量子位元數 n」拉到 3，用「目標 q2」「H」「目標 q1」「CNOT（控制 = 目標+1 → 目標）」「目標 q0」「CNOT」一節一節串，看左下的「各量子位元 Bloch 長度」。
- 打開簡報 `slides/output/basic-circuits.pptx` 第 13–14 頁（課綱寫 p13–14，頁碼無誤）。
- 列印 `02_列印包_GHZ逐步圖.pdf`（A4，共 4 頁），準備色筆。
- 有 Python 的電腦先跑一次 `python ghz_lab.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 本課的振幅都是實數（+0.707）；GHZ 態的非定域性實驗（X、Y 基底量測）不在本課範圍。
- 量 1,000 次的次數是隨機的，每次都會差一點；理論上只會出現全 0、全 1，各 50%。
- basic-circuits.html 的 GHZ 範例沒有畫 Bloch 球；要看「綁住幾顆」，用 ghz_lab.py 或 operation.html#register 的讀數。
- 振幅柱子和 Bloch 球是模擬器才看得到的；真實的量子電腦只給量測結果。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：3 顆與 4 顆（約 40 分鐘）

1. 先在列印包第 1 頁寫預測：3 顆量 1,000 次會出現哪些結果？
2. 打開 `animations/basic-circuits.html#ghz`（範例 4 GHZ 態）。上方「位元數」預設是 3 顆。
3. 按「下一步 ▶」：做完 H，|000⟩、|001⟩ 兩根藍色柱子 +.707。
4. 再按「下一步 ▶」：CNOT q0 → q1，|001⟩ 那根搬到 |011⟩；說明寫「現在有 2 顆位元綁在一起」。
5. 再按「下一步 ▶」：CNOT q1 → q2，搬到 |111⟩；|ψ⟩ = (|000⟩ + |111⟩) / √2。
6. 按「量測 1,000 次」：量測卡只列 000、111 兩列，各約一半。寫進列印包第 2 頁。
7. 「位元數」改選 4 顆：頁面會直接跳到最後一步、量測清除。先按「⏮ 起點」，再逐步按四次「下一步 ▶」：0001 → 0011 → 0111 → 1111。16 根柱子很細，數字只寫百分比。最後量 1,000 次。
8. 兩次的次數並排：全 0 和全 1 是不是都大約一半？有沒有出現其他組合？

## 下半場：故意少接一條（約 30 分鐘）

1. 在列印包第 3 頁寫預測：3 顆少接最後一條、3 顆少接第一條、4 顆少接中間一條，各會量到什麼？哪幾顆沒綁上？
2. 執行 `python ghz_lab.py`，對照第四段。
3. 打開 `ghz_lab.py` 最下面的改造區，改 `N` 和 `MY_CIRCUIT`，例如 4 顆少接最後一條、或換成全部由 q0 控制，先預測，再執行。
4. 看第六段的玩具雜訊模型：每多一顆位元（多一個 CNOT），全 0、全 1 以外的機率怎麼變？
5. 選用：開 `animations/operation.html#register`，滑桿「量子位元數 n」拉到 3。按「目標 q2」「H」：讀數 1.00、1.00、1.00「無糾纏」。按「目標 q1」「CNOT（控制 = 目標+1 → 目標）」：q1、q2 變 0.00，q0 還是 1.00（只接了一節）。再按「目標 q0」「CNOT」：三個都 0.00（這裡的鏈子是從 q2 往下串）。
6. 有裝 Qiskit 的話，跑 `qiskit_check.py`：3 顆、4 顆只有全 0、全 1；少接 CNOT(q1→q2) 時只有 000、011（4 顆是 0000、0011）。
''',

'ghz_lab.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## ghz_lab.py 實跑輸出（Python 3.13.18，random.Random(1117)）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- 每個 CNOT 做了什麼？控制位元是 1 的那一半，目標也翻成 1。柱子高度不變，只是 q0 = 1 那一根往右搬：001 → 011 → 111。\n'
  '- 要綁幾顆需要幾個閘？1 個 H，加上比位元數少一個的 CNOT：3 顆 2 個、4 顆 3 個。\n'
  '- 為什麼只量到全 0、全 1？最後只剩兩根柱子 |0…0⟩、|1…1⟩，各 +0.707，機率各 50%；其他柱子都是 0。\n'
  '- 少接一條為什麼後面全部鬆開？斷點後面那顆一直是 0，它當控制的 CNOT 就從來不會翻，下一顆也一直是 0，一路傳下去。\n'
  '- 全部由 q0 控制也可以嗎？可以，結果一樣（第五段 True）。一路串下去的好處是每個 CNOT 只連相鄰的兩顆。\n'
  '- CNOT 是在「複製」嗎？只是讓 0 對 0、1 對 1；不能把未知的量子態複製一份（不可複製定理）。\n'
  '- 雜訊模型的百分比是真機的數字嗎？不是。那是玩具模型（每個 CNOT 之後 2% 翻錯），只用來看位元越多、CNOT 越多，越容易出錯的趨勢。\n'
  '- 挑戰 MY_CIRCUIT 的預設線路 H(q0) → CNOT(q0→q1) → CNOT(q2→q3)：少了 CNOT(q1→q2)，只量到 0000、0011，q2、q3 的向量大小還是 1。\n'
  '- 下一課 Q118：範例 5 隱形傳態——四種 ψ。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html#ghz`（範例 4 GHZ 態）

- 上方「位元數」：3 顆（預設，三步：H、CNOT q0 → q1、CNOT q1 → q2）、4 顆（四步，多 CNOT q2 → q3）。換選項時頁面停在最後一步並清除量測；按目前已選的選項不會有反應。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」，右邊的小圓點可以直接跳到某一步：橘色虛線標出目前做到哪一格，還沒做的閘是淡色。
- 「振幅與機率」：3 顆 8 根柱子，下面寫振幅與百分比；4 顆 16 根細柱，只寫百分比；最下面 |ψ⟩。這個範例沒有 Bloch 球。
- 「量測 1 次」「量測 1,000 次」「清除」：只列出理論上會出現的結果；灰色底是理論機率，綠色是實際次數。
- 下方「重點」：GHZ 電路的深度隨位元數增加，硬體常用它測試多位元糾纏的品質。

## `animations/operation.html#register`（場景 4：多量子位元：2ⁿ 個振幅與糾纏）

- 滑桿「量子位元數 n」1–4（改了會回到 |0…0⟩）。上排是每顆位元自己的 Bloch 球（3 顆時左 q2、中 q1、右 q0），下排柱子是 2ⁿ 種結果。
- 「目標 q0」…「目標 q3」選要作用的位元；「H」「X」「Z」「S」「T」；「CNOT（控制 = 目標+1 → 目標）」：目標選 q1 時，控制是 q2。
- 「GHZ 態」是現成按鈕（從最高位往下串）；「測量全部」「只測 q0」「重設 |0…0⟩」。
- 左下讀數：|ψ⟩、「各量子位元 Bloch 長度」、「有糾纏」或「無糾纏（可分離態）」。

## 操作

basic-circuits.html：左右方向鍵 上一步／下一步；空白鍵 播放；點電路上的閘可以直接跳到那一步。
''',
}

SHEET_HEADER = ['位元數', '線路（閘由左往右）', '少接哪一條', '我的預測', '量到的結果', '沒綁上的位元', '一樣嗎', '備註']
SHEET_ROWS = [['範例：3 顆', 'H(q0)、CNOT(q0→q1)、CNOT(q1→q2)', '不少接', '', '000、111', '無', '', '綁 3 顆需要 2 個 CNOT'],
              ['範例：3 顆', 'H(q0)、CNOT(q0→q1)', 'CNOT(q1→q2)', '', '000、011', 'q2', '', 'q2 一直是 0'],
              ['4 顆', '', '', '', '', '', '', ''], ['4 顆', '', 'CNOT(q1→q2)', '', '', '', '', ''],
              ['我的改造線路', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:10mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:16%}
table.judge th{font-size:10.5pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 ghz_lab.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'ghz_lab.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    step = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td></tr>'  # noqa: E731
    meas = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    cut = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    pages = [
        '<h2>GHZ 逐步圖：一關多綁一顆</h2><p class="lead">H（q0）→ CNOT（q0 → q1）→ CNOT（q1 → q2）→ …　字串寫成 |q2 q1 q0⟩，最右邊是 q0。4 顆才有第 4 步。</p>'
        '<table class="judge"><tr><th style="width:16%">步驟</th><th>做了哪個閘</th><th>不是 0 的柱子</th><th>現在綁住幾顆</th></tr>'
        + step('起點') + step('第 1 步') + step('第 2 步') + step('第 3 步') + step('第 4 步') + '</table>'
        '<p>我的預測：3 顆量 1,000 次會出現＿＿＿＿＿＿＿＿＿＿；4 顆會出現＿＿＿＿＿＿＿＿＿＿</p>'
        '<div class="box" style="margin-top:4mm"><ul class="chk"><li>第一關：兩顆（上一課的 Bell 態）</li>'
        '<li>第二關：三顆，量 1,000 次只有 000、111</li><li>第三關：四顆，量 1,000 次只有 0000、1111</li><li>隱藏關：少接一條，找出斷在哪裡</li></ul></div>',
        '<h2>量測紀錄表</h2><p class="lead">在 basic-circuits.html#ghz 選位元數，按「⏮ 起點」逐步走完，再按「量測 1,000 次」。</p>'
        '<table class="judge"><tr><th style="width:16%">位元數</th><th>CNOT 有幾個</th><th>全 0 的次數</th><th>全 1 的次數</th><th>其他組合</th></tr>'
        + meas('3 顆') + meas('4 顆') + '</table>'
        '<p>綁 N 顆需要幾個 CNOT？＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>每按一次「下一步」，那根不是 0 的柱子怎麼移動？</p><div class="line"></div>'
        '<p>3 顆和 4 顆的次數放在一起比，你發現什麼？</p><div class="line"></div>',
        '<h2>換你改造：故意少接一條</h2><p class="lead">先預測，再用 ghz_lab.py 驗證。斷在哪裡？後面哪幾顆綁不上？</p>'
        '<table class="judge"><tr><th style="width:22%">少接哪一條</th><th>我的預測</th><th>ghz_lab.py 的結果</th><th>沒綁上的位元</th><th>一樣嗎</th></tr>'
        + cut('3 顆：CNOT(q1→q2)') + cut('3 顆：CNOT(q0→q1)') + cut('4 顆：CNOT(q1→q2)') + cut('4 顆：CNOT(q2→q3)') + '</table>'
        '<p>用一句話說明：為什麼少接中間一條，後面全部都綁不上？</p><div class="line"></div>'
        '<p>玩具雜訊模型：位元越多，全 0、全 1 以外的機率怎麼變？</p><div class="line"></div>'
        '<pre class="code"># ghz_lab.py 最下面的改造區（閘由左往右排）\n'
        'N, MY_CIRCUIT = 4, [(&#39;h&#39;, 0), (&#39;cx&#39;, 0, 1), (&#39;cx&#39;, 2, 3)]   # 改成你的線路\n'
        '# 閘的寫法：(&#39;h&#39;, 0) 哈達瑪閘、(&#39;x&#39;, 1) 翻轉閘、(&#39;cx&#39;, 0, 1) 受控反閘（q0 控制 q1）</pre>',
        '<h2>最後一關：教爸爸串糾纏</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 讓四顆位元一起糾纏，需要哪些閘、怎麼接（不看稿）：</p><div class="line"></div>'
        '<p>2. 為什麼量起來不是全 0 就是全 1：</p><div class="line"></div>'
        '<p>3. 一個容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：H 讓 q0 疊加；每個 CNOT 把柱子往右搬，多綁一顆</li><li>說出：綁 N 顆需要 N − 1 個 CNOT</li>'
        '<li>指出：少接一條，後面的位元就綁不上</li><li>指出：位元越多，真機上越容易被雜訊破壞</li>'
        '<li>完成 GHZ 逐步圖，和 ghz_lab.py 的結果一致</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q117 GHZ 逐步圖 列印包', '父子科技學院 量子電腦學程 Q117｜範例 4：GHZ——CNOT 一路串下去', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q117-ghz-chain', folder='Q117_範例4_GHZ_CNOT一路串下去', files=FILES,
        sheet=('03_逐步圖與改造紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_GHZ逐步圖.pdf', pack_pages=4,
        pack_needles=('GHZ 逐步圖', '量測紀錄表', '故意少接一條', 'MY_CIRCUIT', '最後一關'),
        authoring_dir=XINEW / 'authoring/q117', episode_dir='specials/q117-ghz-chain',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；ghz_lab.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'ghz_lab.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, random seed 1117); qiskit 2.6.2',
               'recordedRun': {'ghz3Steps': ['|000⟩,|001⟩', '|000⟩,|011⟩', '|000⟩,|111⟩'],
                               'blochSize3': {'afterH': [1.0, 1.0, 1.0], 'afterCNOT01': [0.0, 0.0, 1.0], 'afterCNOT12': [0.0, 0.0, 0.0]},
                               'counts1117': {'3': {'000': 495, '111': 505}, '4': {'0000': 470, '1111': 530}},
                               'missingCNOT': {'3:q1→q2': ['000', '011'], '3:q0→q1': ['000', '001'], '4:q1→q2': ['0000', '0011'], '4:q2→q3': ['0000', '0111']},
                               'starEqualsChain': True,
                               'toyNoise2pctOutside': {'3': '4.0%', '4': '5.9%', '8': '13.2%'}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q117/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

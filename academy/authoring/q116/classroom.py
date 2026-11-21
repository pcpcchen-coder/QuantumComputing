"""Q116 課堂教材：Bell 態圖鑑、逐步紀錄表、單看一顆的 Bloch 球改造單、可執行的 bell_lab.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#bell 與 operation.html#register；bell_lab.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 bell_lab.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q116/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，random.Random(1116)（固定種子；換種子或換電腦的 Python 版本，次數可能不同）
RUN_OUTPUT = '''一、逐步看振幅（Φ⁺）  每列最後是「單看那一顆」的 Bloch 向量大小
  起點              |00⟩ +1.000  |01⟩ 0  |10⟩ 0  |11⟩ 0   單看 q0 1.000  單看 q1 1.000
  H(q0)           |00⟩ +0.707  |01⟩ +0.707  |10⟩ 0  |11⟩ 0   單看 q0 1.000  單看 q1 1.000
  H(q0) → CNOT    |00⟩ +0.707  |01⟩ 0  |10⟩ 0  |11⟩ +0.707   單看 q0 0.000  單看 q1 0.000
二、四個 Bell 態：同一條線路，只差開頭加的 X
  Φ⁺  開頭：不加           狀態 (|00⟩ + |11⟩)/√2    單看 q0 0.000  單看 q1 0.000
  Φ⁻  開頭：X(q0)        狀態 (|00⟩ − |11⟩)/√2    單看 q0 0.000  單看 q1 0.000
  Ψ⁺  開頭：X(q1)        狀態 (|01⟩ + |10⟩)/√2    單看 q0 0.000  單看 q1 0.000
  Ψ⁻  開頭：X(q0)、X(q1)  狀態 (−|01⟩ + |10⟩)/√2   單看 q0 0.000  單看 q1 0.000
三、各量測 1000 次（兩顆一起量；random 種子 1116）
  Φ⁺  00 → 465 次  01 → 0 次  10 → 0 次  11 → 535 次
  Φ⁻  00 → 516 次  01 → 0 次  10 → 0 次  11 → 484 次
  Ψ⁺  00 → 0 次  01 → 497 次  10 → 503 次  11 → 0 次
  Ψ⁻  00 → 0 次  01 → 475 次  10 → 525 次  11 → 0 次
四、對照組：只做 H(q0)，不做 CNOT；以及量完一顆之後
  單看 q0：量到 0 的機率 50%，Bloch 向量大小 1.000（一半一半，卻沒有變短）
  Φ⁺ 只量 q0 一次之後：單看 q0 1.000  單看 q1 1.000（量測把糾纏拆開，兩顆都回到 1）
五、開頭的 X 等於後面補一個 Z
  X(q0) → H(q0)：(|00⟩ − |01⟩)/√2   H(q0) → Z(q0)：(|00⟩ − |01⟩)/√2   一樣嗎？ True
  Φ⁻ = 先 X(q0)：(|00⟩ − |11⟩)/√2   Φ⁺ 之後補 Z(q0)：(|00⟩ − |11⟩)/√2   一樣嗎？ True
六、改造區
  X(q1) → H(q0) → CNOT(q0→q1) → Z(q0)
    狀態 (−|01⟩ + |10⟩)/√2   單看 q0 0.000  單看 q1 0.000
'''

# 製作代理實跑紀錄：qiskit 2.6.2，StatevectorSampler(seed=2026)，shots=1000（四個線路用同一個種子，所以次數的數字相同、對應的結果不同）
QISKIT_OUTPUT = '''Φ⁺ 振幅 [0.707, 0.0, 0.0, 0.707] 單看 q0 0.0 單看 q1 0.0 量測 1000 次 {'00': 464, '11': 536}
Φ⁻ 振幅 [0.707, 0.0, 0.0, -0.707] 單看 q0 0.0 單看 q1 0.0 量測 1000 次 {'00': 464, '11': 536}
Ψ⁺ 振幅 [0.0, 0.707, 0.707, 0.0] 單看 q0 0.0 單看 q1 0.0 量測 1000 次 {'01': 464, '10': 536}
Ψ⁻ 振幅 [0.0, -0.707, 0.707, 0.0] 單看 q0 0.0 單看 q1 0.0 量測 1000 次 {'01': 464, '10': 536}
先 X 再 H，和先 H 再 Z，是同一個運算嗎？ True
     ┌───┐┌───┐     
q_0: ┤ X ├┤ H ├──■──
     ├───┤└───┘┌─┴─┐
q_1: ┤ X ├─────┤ X ├
     └───┘     └───┘
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q116：範例 3 Bell 態——四種糾纏（純 Python，不需安裝任何套件）

執行：  python bell_lab.py
它用一個很小的兩顆位元模擬器（只認得 H、X、Z、CNOT），印出：
  一、逐步看振幅：H（q0）→ CNOT（q0 → q1），CNOT 把 |01⟩ 那根搬到 |11⟩
  二、四個 Bell 態：開頭加什麼、狀態、單看每一顆的 Bloch 向量大小
  三、各量測 1000 次（固定的亂數種子；換種子次數會不一樣）
  四、對照組：只做 H 的那一顆，量起來也是一半一半，向量大小卻還是 1；只量 q0 一次之後又如何
  五、X 再 H 等於 H 再 Z：所以「開頭的 X」也可以說成「後面補一個 Z」
  六、改造區：自己排一條線路，先預測，再執行
位元字串寫成 |q1 q0⟩：右邊那位是 q0（和 Qiskit、basic-circuits.html 一樣）。
"""
import random
from math import sqrt

R2 = 1 / sqrt(2)
KETS = ['00', '01', '10', '11']          # 第 i 根柱子 = |q1 q0⟩，i = 2·q1 + q0


def run(gates):
    """兩顆位元從 |00⟩ 出發，依序做 gates，回傳四個振幅 [|00⟩, |01⟩, |10⟩, |11⟩]
    閘的寫法：('h', q)、('x', q)、('z', q)、('cx', 控制, 目標)"""
    s = [1.0, 0.0, 0.0, 0.0]
    for g in gates:
        if g[0] == 'cx':
            c, t = 1 << g[1], 1 << g[2]
            s = [s[i ^ t] if i & c else s[i] for i in range(4)]
            continue
        name, m = g[0], 1 << g[1]
        new = s[:]
        for i in range(4):
            if i & m:
                continue
            a, b = s[i], s[i | m]                       # 這一顆是 0、是 1 的兩個振幅
            if name == 'h':
                new[i], new[i | m] = (a + b) * R2, (a - b) * R2
            elif name == 'x':
                new[i], new[i | m] = b, a
            elif name == 'z':
                new[i], new[i | m] = a, -b
            else:
                raise ValueError('只認得 h、x、z、cx：' + name)
        s = new
    return s


def bloch(s, q):
    """單看第 q 顆的 Bloch 向量（振幅都是實數，所以只有 x、z 兩個分量）"""
    m = 1 << q
    x = sum(2 * s[i] * s[i | m] for i in range(4) if not i & m)
    z = sum((-1 if i & m else 1) * s[i] ** 2 for i in range(4))
    return x, z


def size(s, q):
    x, z = bloch(s, q)
    return sqrt(x * x + z * z)


def num(v):
    return '0' if abs(v) < 1e-9 else ('+' if v > 0 else '−') + f'{abs(v):.3f}'


def ket(s):
    """把振幅寫成 (+|00⟩ +|11⟩)/√2 這種式子（只處理本課用到的情形）"""
    nz = [(i, a) for i, a in enumerate(s) if abs(a) > 1e-9]
    body = ''.join(('−' if a < 0 else '') + f'|{KETS[i]}⟩' if k == 0 else (' − ' if a < 0 else ' + ') + f'|{KETS[i]}⟩'
                   for k, (i, a) in enumerate(nz))
    return body if len(nz) == 1 else f'({body})/√2'


def same(a, b):
    return all(abs(x - y) < 1e-9 for x, y in zip(a, b))


def gname(g):
    return f'CNOT(q{g[1]}→q{g[2]})' if g[0] == 'cx' else f'{g[0].upper()}(q{g[1]})'


def show(label, s):
    print(f'  {label:<16}' + '  '.join(f'|{KETS[i]}⟩ {num(a)}' for i, a in enumerate(s))
          + f'   單看 q0 {size(s, 0):.3f}  單看 q1 {size(s, 1):.3f}')


def measure_q0(s, rng):
    """只量 q0 一次：回傳結果和量完之後的狀態（另一半的振幅歸零，再重新調整大小）"""
    p1 = sum(s[i] ** 2 for i in range(4) if i & 1)
    bit = 1 if rng.random() < p1 else 0
    kept = [a if (i & 1) == bit else 0.0 for i, a in enumerate(s)]
    norm = sqrt(sum(a * a for a in kept))
    return bit, [a / norm for a in kept]


def shots(s, n, rng):
    """兩顆一起量 n 次：每次以機率 振幅² 得到 00、01、10、11 其中一個"""
    counts = {k: 0 for k in KETS}
    for _ in range(n):
        r, i = rng.random(), 0
        while i < 3 and r >= s[i] ** 2:
            r -= s[i] ** 2
            i += 1
        counts[KETS[i]] += 1
    return counts


H0, CX = ('h', 0), ('cx', 0, 1)
BELL = [H0, CX]
FOUR = [('Φ⁺', []), ('Φ⁻', [('x', 0)]), ('Ψ⁺', [('x', 1)]), ('Ψ⁻', [('x', 0), ('x', 1)])]

if __name__ == '__main__':
    rng = random.Random(1116)
    print('一、逐步看振幅（Φ⁺）  每列最後是「單看那一顆」的 Bloch 向量大小')
    show('起點', run([]))
    show('H(q0)', run([H0]))
    show('H(q0) → CNOT', run(BELL))
    print('二、四個 Bell 態：同一條線路，只差開頭加的 X')
    for name, prep in FOUR:
        s = run(prep + BELL)
        lead = '、'.join(gname(g) for g in prep) or '不加'
        print(f'  {name}  開頭：{lead:<13}狀態 {ket(s):<20}單看 q0 {size(s, 0):.3f}  單看 q1 {size(s, 1):.3f}')
    print('三、各量測 1000 次（兩顆一起量；random 種子 1116）')
    for name, prep in FOUR:
        c = shots(run(prep + BELL), 1000, rng)
        print(f'  {name}  ' + '  '.join(f'{k} → {v} 次' for k, v in c.items()))
    print('四、對照組：只做 H(q0)，不做 CNOT；以及量完一顆之後')
    s = run([H0])
    p0 = sum(s[i] ** 2 for i in range(4) if not i & 1)
    print(f'  單看 q0：量到 0 的機率 {p0 * 100:.0f}%，Bloch 向量大小 {size(s, 0):.3f}（一半一半，卻沒有變短）')
    bit, after = measure_q0(run(BELL), rng)
    print(f'  Φ⁺ 只量 q0 一次之後：單看 q0 {size(after, 0):.3f}  單看 q1 {size(after, 1):.3f}（量測把糾纏拆開，兩顆都回到 1）')
    print('五、開頭的 X 等於後面補一個 Z')
    a, b = run([('x', 0), H0]), run([H0, ('z', 0)])
    print(f'  X(q0) → H(q0)：{ket(a)}   H(q0) → Z(q0)：{ket(b)}   一樣嗎？ {same(a, b)}')
    a, b = run([('x', 0), H0, CX]), run([H0, CX, ('z', 0)])
    print(f'  Φ⁻ = 先 X(q0)：{ket(a)}   Φ⁺ 之後補 Z(q0)：{ket(b)}   一樣嗎？ {same(a, b)}')

    # 六、改造區：先預測，再執行。閘寫成 ('h', 0)、('x', 1)、('z', 0)、('cx', 0, 1)，由左往右排
    MY_CIRCUITS = [[('x', 1), ('h', 0), ('cx', 0, 1), ('z', 0)]]
    print('六、改造區')
    for g in MY_CIRCUITS:
        s = run(g)
        print('  ' + ' → '.join(gname(x) for x in g))
        print(f'    狀態 {ket(s)}   單看 q0 {size(s, 0):.3f}  單看 q1 {size(s, 1):.3f}')
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q116：用本機 Qiskit 重現四個 Bell 態（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import DensityMatrix, Operator, Pauli, Statevector, partial_trace


def bell(name):
    qc = QuantumCircuit(2)
    if name in ('Φ⁻', 'Ψ⁻'):
        qc.x(0)              # 開頭先翻 q0：H 之後帶進負號
    if name in ('Ψ⁺', 'Ψ⁻'):
        qc.x(1)              # 開頭先翻 q1：CNOT 之後兩顆相反
    qc.h(0)                  # 哈達瑪閘：q0 進入疊加
    qc.cx(0, 1)              # 受控反閘：q0 控制、q1 目標
    return qc


def size(sv, keep):
    """單看第 keep 顆：把另一顆 trace 掉，算 Bloch 向量的大小"""
    rho = partial_trace(DensityMatrix(sv), [1 - keep])
    v = [rho.expectation_value(Pauli(p)).real for p in 'XYZ']
    return round(sum(c * c for c in v) ** 0.5, 3) + 0.0


for name in ('Φ⁺', 'Φ⁻', 'Ψ⁺', 'Ψ⁻'):
    qc = bell(name)
    sv = Statevector.from_instruction(qc)
    m = qc.copy()
    m.measure_all()
    counts = StatevectorSampler(seed=2026).run([m], shots=1000).result()[0].data.meas.get_counts()
    print(name, '振幅', [round(float(a.real), 3) + 0.0 for a in sv.data],
          '單看 q0', size(sv, 0), '單看 q1', size(sv, 1), '量測 1000 次', dict(sorted(counts.items())))

xh, hz = QuantumCircuit(1), QuantumCircuit(1)
xh.x(0)
xh.h(0)
hz.h(0)
hz.z(0)
print('先 X 再 H，和先 H 再 Z，是同一個運算嗎？', Operator(xh).equiv(Operator(hz)))
print(bell('Ψ⁻').draw())
'''

ATLAS = [  # (名字, 開頭加什麼, 狀態 |q1 q0⟩, 量測結果, 負號在哪, 單看一顆)
    ('Φ⁺（第一種）', '不加', '(|00⟩ + |11⟩)/√2', '00 或 11（永遠相同）', '沒有', '兩顆都在球心'),
    ('Φ⁻（第二種）', 'X(q0)', '(|00⟩ − |11⟩)/√2', '00 或 11（永遠相同）', '|11⟩', '兩顆都在球心'),
    ('Ψ⁺（第三種）', 'X(q1)', '(|01⟩ + |10⟩)/√2', '01 或 10（永遠相反）', '沒有', '兩顆都在球心'),
    ('Ψ⁻（第四種）', 'X(q0)、X(q1)', '(−|01⟩ + |10⟩)/√2', '01 或 10（永遠相反）', '|01⟩', '兩顆都在球心'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q116：範例 3 Bell 態——四種糾纏（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的範例 3。
上一課（Q115）用 H‑Z‑H 把一個量不到的負號變成看得到的結果；今天換成兩顆位元：H 讓 q0 疊加，CNOT 讓 q1 跟著 q0 翻，兩顆就糾纏在一起。
核心一句話：**四個 Bell 態用同一條線路，只差開頭有沒有先加 X。** 先翻 q0 帶進負號（等於 H 之後補一個 Z），先翻 q1 讓兩顆相反。

## Bell 態圖鑑（作品的答案）

位元字串寫成 |q1 q0⟩，右邊那位是 q0（和 Qiskit、basic-circuits.html 一樣）。

| 名字 | 開頭加什麼 | 狀態 | 量測結果 | 負號在哪 | 單看一顆 |
|---|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in ATLAS) + '''
簡報第 12 頁把 Ψ⁻ 寫成 (|10⟩ − |01⟩)/√2，動畫寫成 (−|01⟩ + |10⟩)/√2，是同一個式子換順序。

## 為什麼向量變短（改造的答案）

- 動畫裡多顆位元時，Bloch 球畫的是「單看這一顆」的狀態。向量在球面上（大小 1）代表單看它也是一個完整的狀態；在球的內部代表單看它只剩一部分資訊；縮到球心代表單看它完全隨機。
- 做完 CNOT，整對位元的狀態是完全確定的，但資訊都在「兩顆的關聯」裡，單看哪一顆都拿不到，所以向量縮到球心。這是糾纏，不是位元壞掉。
- 對照：只做 H 的 q0 量起來也是 50/50，向量卻在赤道上、大小還是 1。所以「隨機」不等於「糾纏」，「變短」才是糾纏的記號。
- 量測其中一顆之後，兩顆都變成確定的 0 或 1，向量回到大小 1：量測把糾纏拆開了。

## 影片的念法

H 念「哈達瑪閘」、X「翻轉閘」、Z「相位翻轉閘」、CNOT「受控反閘」；Φ⁺、Φ⁻、Ψ⁺、Ψ⁻ 念成「第一種」到「第四種」（簡報第 12 頁表格的順序）；q0、q1 念「編號零」「編號一」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 對照簡報第 10–12 頁：範例 3 線路、振幅逐步看、四個 Bell 態 | 簡報 basic-circuits.pptx p10–12 |
| 25–65 | 在 basic-circuits.html#bell 把「目標 Bell 態」依序換成 Φ⁺、Φ⁻、Ψ⁺、Ψ⁻，每種從起點逐步播放、量測 1,000 次；填逐步紀錄表與圖鑑 | `01_操作步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子看「單看某一顆」的 Bloch 球，說明為什麼向量變短；跑 `bell_lab.py` 核對；用 operation.html#register 自己組 Bell 態、讀向量大小 | 列印包第 3 頁、`03_圖鑑與改造紀錄.csv` |
| 105–115 | 孩子教爸爸：線路、四種、容易錯的地方 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#bell`：上方「目標 Bell 態」切換 Φ⁺／Φ⁻／Ψ⁺／Ψ⁻，按「⏮ 起點」「下一步 ▶」與「量測 1,000 次」。
- 選用：開 `operation.html#register`（場景 4），用「目標 q1」「H」「目標 q0」「CNOT（控制 = 目標+1 → 目標）」自己組 Bell 態，看左下的「各量子位元 Bloch 長度」。
- 打開簡報 `slides/output/basic-circuits.pptx` 第 10–12 頁（課綱寫 p10–12，頁碼無誤）。
- 列印 `02_列印包_Bell態圖鑑.pdf`（A4，共 4 頁），準備兩種顏色的筆（一正一負）。
- 有 Python 的電腦先跑一次 `python bell_lab.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 本課的振幅都是實數，Bloch 向量只有 x、z 兩個分量；一般的複數相位不展開。
- 量 1,000 次的次數是隨機的，每次都會差一點；理論上 Φ 只會出現 00、11，Ψ 只會出現 01、10，各 50%。
- 「負號要再做 CNOT、H 干涉才分得出來（Bell 量測）」來自簡報第 12 頁與動畫說明；本課教材沒有另寫 Bell 量測程式。
- 真的量子電腦有雜訊，雜訊也會讓單一位元的向量變短；本課講的是理想模擬，向量變短都來自糾纏。
- Bloch 球和振幅柱子是模擬器才看得到的；真實的量子電腦只給量測結果。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：四種各做一次（約 40 分鐘）

1. 先在列印包第 1 頁的圖鑑寫預測：四種各會量到哪兩種結果？哪一種有負號？
2. 打開 `animations/basic-circuits.html#bell`（範例 3 Bell 態）。上方「目標 Bell 態」預設是 Φ⁺。
3. Φ⁺：按「下一步 ▶」：做完 H，|00⟩、|01⟩ 兩根藍色柱子 +.707；「單看 q0」的向量倒到赤道，「單看 q1」還在北極。
4. 再按「下一步 ▶」：做完 CNOT，|01⟩ 那根搬到 |11⟩；|ψ⟩ = (|00⟩ + |11⟩) / √2；兩顆 Bloch 向量都縮到球心。
5. 按「量測 1,000 次」：只有 00、11 兩列，各約一半。寫進逐步紀錄表與圖鑑。
6. 「目標 Bell 態」改選 Φ⁻：頁面會直接跳到最後一步、量測清除。先按「⏮ 起點」，再逐步按三次「下一步 ▶」（準備 X、H、CNOT），最後量 1,000 次。Φ⁻ 的 |11⟩ 柱子是橘色負的。
7. 同樣做 Ψ⁺（X 在 q1：最後是 |01⟩、|10⟩）和 Ψ⁻（兩條線都有 X：最後 |01⟩ 是橘色負的）。
8. 四種並排比較：哪兩種量起來一樣？差在哪一根柱子的顏色？

## 下半場：單看一顆的 Bloch 球（約 30 分鐘）

1. 選 Ψ⁻、按起點，一步一步看「單看 q0」「單看 q1」：準備 X 之後兩支都到南極；H 之後 q0 倒到赤道、q1 留在南極；CNOT 之後兩支都縮到球心。
2. 在列印包第 3 頁寫下：每一步兩支向量的大小（1 或 0），以及為什麼 CNOT 之後會變成 0。
3. 執行 `python bell_lab.py`，對照第一、二、四段的「單看 q0」「單看 q1」。
4. 選用：開 `animations/operation.html#register`，按「目標 q1」「H」：左下讀數「各量子位元 Bloch 長度：q0 1.00，q1 1.00」「無糾纏」。再按「目標 q0」「CNOT（控制 = 目標+1 → 目標）」：讀數變成 0.00、0.00，「有糾纏」。最後按「只測 q0」：讀數回到 1.00、1.00。
5. 挑戰：把 `MY_CIRCUITS` 換成你的線路，例如只做 `('h', 0)`，或做完 Bell 態再加 `('h', 0)`，先預測兩顆的向量大小，再執行。
6. 有裝 Qiskit 的話，跑 `qiskit_check.py`：四種的「單看 q0」「單看 q1」都是 0.0，「先 X 再 H，和先 H 再 Z」印出 True。
''',

'bell_lab.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## bell_lab.py 實跑輸出（Python 3.13.18，random.Random(1116)）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- CNOT 做了什麼？q0 是 1 的那一半，q1 也翻過來。柱子高度不變，只是 |01⟩ 那根整根搬到 |11⟩。\n'
  '- 四種只差在哪？開頭的 X：不加 Φ⁺、X(q0) Φ⁻、X(q1) Ψ⁺、兩個都加 Ψ⁻。先翻 q1，CNOT 之後兩顆相反；先翻 q0，H 會帶進負號。\n'
  '- 為什麼課綱說「X 與 Z」？X(q0) 再 H，等於 H 再 Z(q0)（bell_lab.py 第五段、Qiskit 都印出 True），所以 Φ⁻ 也可以看成 Φ⁺ 之後補一個 Z。\n'
  '- Φ⁺ 和 Φ⁻ 量 1,000 次分得出來嗎？分不出來，都是 00、11 各約一半；差別只在 |11⟩ 振幅的正負號，要再做 CNOT、H 干涉才看得到（Bell 量測）。\n'
  '- 向量縮到球心，是位元壞掉了嗎？不是。整對位元的狀態完全確定，資訊在兩顆的關聯裡；單看一顆才完全隨機。\n'
  '- 只做 H 的 q0 也是 50/50，為什麼向量沒有變短？它還是一個完整的狀態（|+⟩，在赤道上），沒有和別人糾纏。隨機不等於糾纏。\n'
  '- 只量 q0 一次之後呢？兩顆都變成確定的 0 或 1，向量大小回到 1，糾纏被量測拆開了。\n'
  '- 挑戰 MY_CIRCUITS 的預設線路 X(q1) → H(q0) → CNOT → Z(q0)：得到 (−|01⟩ + |10⟩)/√2，就是 Ψ⁻（開頭的 X(q0) 換成最後補 Z(q0)）。\n'
  '- 下一課 Q117：範例 4 GHZ——CNOT 一路串下去。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html#bell`（範例 3 Bell 態）

- 上方「目標 Bell 態」：Φ⁺（預設，兩步：H、CNOT）、Φ⁻、Ψ⁺、Ψ⁻（三步：準備 X、H、CNOT）。換選項時頁面停在最後一步並清除量測；按目前已選的選項不會有反應。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」，右邊的小圓點可以直接跳到某一步：橘色虛線標出目前做到哪一格，還沒做的閘是淡色。
- 「振幅與機率」：圖例「正振幅」藍、「負振幅」橘；四根柱子 |00⟩、|01⟩、|10⟩、|11⟩，下面寫振幅和百分比；柱子下方兩顆 Bloch 球「單看 q0」「單看 q1」（橘色向量）；最下面 |ψ⟩。
- 「量測 1 次」「量測 1,000 次」「清除」：灰色底是理論機率，綠色是實際次數；量測會累加，按「清除」才歸零。

## `animations/operation.html#register`（場景 4：多量子位元：2ⁿ 個振幅與糾纏）

- 上排是每顆位元自己的 Bloch 球（左 q1、右 q0），下排柱子是四種結果（高度 = 機率，顏色 = 相位：金 = +、藍 = −）。
- 「目標 q0」…「目標 q3」選要作用的位元；「H」「X」「Z」「S」「T」；「CNOT（控制 = 目標+1 → 目標）」：目標選 q0 時，控制是 q1。
- 「均勻疊加 H⊗ⁿ」「Bell 態」「GHZ 態」是現成按鈕；「測量全部」「只測 q0」「重設 |0…0⟩」。
- 左下讀數：|ψ⟩、「各量子位元 Bloch 長度」、「有糾纏」或「無糾纏（可分離態）」。

## 操作

basic-circuits.html：左右方向鍵 上一步／下一步；空白鍵 播放；點電路上的閘可以直接跳到那一步。
''',
}

SHEET_HEADER = ['名字', '開頭加什麼', '狀態', '量測 1000 次', '負號在哪', '單看 q0 向量大小', '單看 q1 向量大小', '我的預測', '一樣嗎', '備註']
SHEET_ROWS = [['範例：Φ⁺', '不加', '(|00⟩ + |11⟩)/√2', '00、11 各約一半', '沒有', '0', '0', '', '', 'CNOT 把 |01⟩ 搬到 |11⟩'],
              ['範例：只做 H(q0)', '—', '(|00⟩ + |01⟩)/√2', '00、01 各約一半', '沒有', '1', '1', '', '', '隨機，但沒有糾纏'],
              ['Φ⁻', '', '', '', '', '', '', '', '', ''], ['Ψ⁺', '', '', '', '', '', '', '', '', ''],
              ['Ψ⁻', '', '', '', '', '', '', '', '', ''], ['我的改造線路', '', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:10mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:16%}
table.judge th{font-size:10.5pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 bell_lab.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'bell_lab.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    blank = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    step = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    size = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    pages = [
        '<h2>Bell 態圖鑑：解鎖四個成就</h2><p class="lead">同一條線路 H（q0）→ CNOT（q0 → q1），只差開頭加的 X。字串寫成 |q1 q0⟩，右邊是 q0。</p>'
        '<table class="judge"><tr><th style="width:16%">名字</th><th>開頭加什麼</th><th>狀態</th><th>量 1,000 次</th><th>負號在哪</th><th>我的一句說明</th></tr>'
        + blank('Φ⁺') + blank('Φ⁻') + blank('Ψ⁺') + blank('Ψ⁻') + '</table>'
        '<p>永遠相同的是：＿＿＿＿＿＿　永遠相反的是：＿＿＿＿＿＿　量起來分不出來的兩對：＿＿＿＿＿＿</p>'
        '<div class="box" style="margin-top:4mm"><ul class="chk"><li>成就一：做出 Φ⁺，量 1,000 次只有 00、11</li>'
        '<li>成就二：做出 Φ⁻，找到橘色的負柱子</li><li>成就三：做出 Ψ⁺，量到兩顆相反</li><li>成就四：做出 Ψ⁻，相反又帶負號</li></ul></div>',
        '<h2>逐步紀錄表</h2><p class="lead">在 basic-circuits.html#bell 選一種 Bell 態，按「⏮ 起點」再一步一步按「下一步 ▶」。</p>'
        '<p>我選的是：＿＿＿＿＿＿　開頭加的是：＿＿＿＿＿＿</p>'
        '<table class="judge"><tr><th style="width:16%">步驟</th><th>|00⟩</th><th>|01⟩</th><th>|10⟩</th><th>|11⟩</th><th>單看 q0 箭頭</th><th>單看 q1 箭頭</th></tr>'
        + step('起點') + step('準備 X') + step('H（q0）') + step('CNOT') + '</table>'
        '<p class="note">柱子寫振幅（例如 +.707、−.707、0）；箭頭寫「北極、南極、赤道、球心」。Φ⁺ 沒有「準備 X」那一步。</p>'
        '<p>CNOT 把哪一根柱子搬到哪裡？</p><div class="line"></div>'
        '<p>量 1,000 次的結果：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：單看一顆的 Bloch 球</h2><p class="lead">向量在球面上＝大小 1；縮到球心＝大小 0。為什麼做完 CNOT 會變短？</p>'
        '<table class="judge"><tr><th style="width:22%">情況</th><th>單看 q0 大小</th><th>單看 q1 大小</th><th>單看 q0 量到 0 的機率</th><th>有糾纏嗎</th></tr>'
        + size('起點 |00⟩') + size('只做 H（q0）') + size('做完 CNOT（Φ⁺）') + size('Φ⁺ 只量 q0 之後') + '</table>'
        '<p>用一句話說明：為什麼「只做 H」也是 50/50，向量卻沒有變短？</p><div class="line"></div>'
        '<p>用一句話說明：向量縮到球心，是位元壞掉了嗎？</p><div class="line"></div>'
        '<pre class="code"># bell_lab.py 最下面的改造區（閘由左往右排）\n'
        'MY_CIRCUITS = [[(&#39;x&#39;, 1), (&#39;h&#39;, 0), (&#39;cx&#39;, 0, 1), (&#39;z&#39;, 0)]]   # 改成你的線路\n'
        '# 閘的寫法：(&#39;h&#39;, 0) 哈達瑪閘、(&#39;x&#39;, 1) 翻轉閘、(&#39;z&#39;, 0) 相位翻轉閘、(&#39;cx&#39;, 0, 1) 受控反閘（q0 控制 q1）</pre>',
        '<h2>最後一關：教爸爸四種糾纏</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 線路的兩個閘各做什麼（不看稿）：</p><div class="line"></div>'
        '<p>2. 四種 Bell 態，開頭各加了什麼：</p><div class="line"></div>'
        '<p>3. 一個容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：H 讓 q0 疊加；CNOT 在 q0 是 1 時翻 q1，把 |01⟩ 搬到 |11⟩</li><li>說出：不加 Φ⁺、X(q0) Φ⁻、X(q1) Ψ⁺、兩個都加 Ψ⁻</li>'
        '<li>指出：向量縮到球心是和另一顆糾纏，不是位元壞掉</li><li>指出：Φ⁺ 和 Φ⁻ 量起來一樣，差別只在負號</li>'
        '<li>完成 Bell 態圖鑑，和 bell_lab.py 的結果一致</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q116 Bell 態圖鑑 列印包', '父子科技學院 量子電腦學程 Q116｜範例 3：Bell 態——四種糾纏', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q116-four-bell-states', folder='Q116_範例3_Bell態_四種糾纏', files=FILES,
        sheet=('03_圖鑑與改造紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_Bell態圖鑑.pdf', pack_pages=4,
        pack_needles=('Bell 態圖鑑', '逐步紀錄表', '單看一顆', 'MY_CIRCUITS', '最後一關'),
        authoring_dir=XINEW / 'authoring/q116', episode_dir='specials/q116-four-bell-states',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；bell_lab.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'bell_lab.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, random seed 1116); qiskit 2.6.2',
               'recordedRun': {'phiPlus': {'00': '+0.707', '11': '+0.707'}, 'psiMinus': {'01': '−0.707', '10': '+0.707'},
                               'blochSize': {'afterH': [1.0, 1.0], 'afterCNOTallFour': [0.0, 0.0], 'afterMeasureQ0': [1.0, 1.0]},
                               'counts1116': {'Φ⁺': {'00': 465, '11': 535}, 'Φ⁻': {'00': 516, '11': 484},
                                              'Ψ⁺': {'01': 497, '10': 503}, 'Ψ⁻': {'01': 475, '10': 525}},
                               'xThenHequalsHthenZ': True, 'qiskitReducedBlochAllFour': 0.0},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q116/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q118 課堂教材：傳送流程表、三人傳送角色卡、拿掉修正的改造單、可執行的 teleport_lab.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#teleport（選用 operation.html#circuit）；teleport_lab.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 teleport_lab.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q118/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，random.Random(1118)（固定種子；換種子或換電腦的 Python 版本，次數可能不同）
RUN_OUTPUT = '''一、四種 ψ 各傳一次（延遲量測版）：每一步單看 q0、單看 q2
  ψ = √¾|0⟩+½|1⟩   ψ 的 Bloch 向量 (x +0.87, z +0.50) 大小 1.00
    起點：單看 q0 (x +0.00, z +1.00) 大小 1.00   單看 q2 (x +0.00, z +1.00) 大小 1.00
    ①準備ψ：單看 q0 (x +0.87, z +0.50) 大小 1.00   單看 q2 (x +0.00, z +1.00) 大小 1.00
    ②糾纏對：單看 q0 (x +0.87, z +0.50) 大小 1.00   單看 q2 (x +0.00, z +0.00) 大小 0.00
    ③Alice：單看 q0 (x +0.50, z +0.00) 大小 0.50   單看 q2 (x +0.00, z +0.00) 大小 0.00
    ④Bob修正：單看 q0 (x +1.00, z +0.00) 大小 1.00   單看 q2 (x +0.87, z +0.50) 大小 1.00
    傳完：q2 和 ψ 一樣嗎？ True   Bob 量到 1 的機率 0.25（ψ 本身 0.25）
  ψ = |1⟩   ψ 的 Bloch 向量 (x +0.00, z -1.00) 大小 1.00
    起點：單看 q0 (x +0.00, z +1.00) 大小 1.00   單看 q2 (x +0.00, z +1.00) 大小 1.00
    ①準備ψ：單看 q0 (x +0.00, z -1.00) 大小 1.00   單看 q2 (x +0.00, z +1.00) 大小 1.00
    ②糾纏對：單看 q0 (x +0.00, z -1.00) 大小 1.00   單看 q2 (x +0.00, z +0.00) 大小 0.00
    ③Alice：單看 q0 (x -1.00, z +0.00) 大小 1.00   單看 q2 (x +0.00, z +0.00) 大小 0.00
    ④Bob修正：單看 q0 (x +1.00, z +0.00) 大小 1.00   單看 q2 (x +0.00, z -1.00) 大小 1.00
    傳完：q2 和 ψ 一樣嗎？ True   Bob 量到 1 的機率 1.00（ψ 本身 1.00）
  ψ = |+⟩   ψ 的 Bloch 向量 (x +1.00, z +0.00) 大小 1.00
    起點：單看 q0 (x +0.00, z +1.00) 大小 1.00   單看 q2 (x +0.00, z +1.00) 大小 1.00
    ①準備ψ：單看 q0 (x +1.00, z +0.00) 大小 1.00   單看 q2 (x +0.00, z +1.00) 大小 1.00
    ②糾纏對：單看 q0 (x +1.00, z +0.00) 大小 1.00   單看 q2 (x +0.00, z +0.00) 大小 0.00
    ③Alice：單看 q0 (x +0.00, z +0.00) 大小 0.00   單看 q2 (x +0.00, z +0.00) 大小 0.00
    ④Bob修正：單看 q0 (x +1.00, z +0.00) 大小 1.00   單看 q2 (x +1.00, z +0.00) 大小 1.00
    傳完：q2 和 ψ 一樣嗎？ True   Bob 量到 1 的機率 0.50（ψ 本身 0.50）
  ψ = |−⟩   ψ 的 Bloch 向量 (x -1.00, z +0.00) 大小 1.00
    起點：單看 q0 (x +0.00, z +1.00) 大小 1.00   單看 q2 (x +0.00, z +1.00) 大小 1.00
    ①準備ψ：單看 q0 (x -1.00, z +0.00) 大小 1.00   單看 q2 (x +0.00, z +1.00) 大小 1.00
    ②糾纏對：單看 q0 (x -1.00, z +0.00) 大小 1.00   單看 q2 (x +0.00, z +0.00) 大小 0.00
    ③Alice：單看 q0 (x +0.00, z +0.00) 大小 0.00   單看 q2 (x +0.00, z +0.00) 大小 0.00
    ④Bob修正：單看 q0 (x +1.00, z +0.00) 大小 1.00   單看 q2 (x -1.00, z +0.00) 大小 1.00
    傳完：q2 和 ψ 一樣嗎？ True   Bob 量到 1 的機率 0.50（ψ 本身 0.50）
  四種傳完，單看 q0 都一樣嗎？ True
二、Alice 量到什麼、Bob 手上是什麼（ψ = √¾|0⟩+½|1⟩，第 ③ 步之後）
  q1 q0 = 00  機率 0.25  Bob 手上 (+0.866, +0.500) = ψ   修正：不用修 → (+0.866, +0.500) = ψ
  q1 q0 = 01  機率 0.25  Bob 手上 (+0.866, -0.500) = Zψ  修正：Z → (+0.866, +0.500) = ψ
  q1 q0 = 10  機率 0.25  Bob 手上 (+0.500, +0.866) = Xψ  修正：X → (+0.866, +0.500) = ψ
  q1 q0 = 11  機率 0.25  Bob 手上 (-0.500, +0.866) = XZψ 修正：先 X、再 Z → (+0.866, +0.500) = ψ
三、真的先量再修（古典通訊版），各傳 1000 次（random 種子 1118）
  ψ = √¾|0⟩+½|1⟩  Alice 的結果 00:226  01:275  10:243  11:256   Bob 量到 1：245 次（理論 250 次）
  ψ = |1⟩         Alice 的結果 00:247  01:246  10:241  11:266   Bob 量到 1：1000 次（理論 1000 次）
  ψ = |+⟩         Alice 的結果 00:263  01:237  10:258  11:242   Bob 量到 1：524 次（理論 500 次）
  ψ = |−⟩         Alice 的結果 00:253  01:242  10:274  11:231   Bob 量到 1：517 次（理論 500 次）
四、拿掉修正、只修一半：Bob 的 q2（延遲量測版；每格是「對或錯  量到 1 的機率  向量大小」）
  ψ              不修            只修 X          只修 Z          兩個都修
  √¾|0⟩+½|1⟩     錯 0.50 0.00     錯 0.25 0.50     錯 0.50 0.87     對 0.25 1.00
  |1⟩            錯 0.50 0.00     對 1.00 1.00     錯 0.50 0.00     對 1.00 1.00
  |+⟩            錯 0.50 0.00     錯 0.50 0.00     對 0.50 1.00     對 0.50 1.00
  |−⟩            錯 0.50 0.00     錯 0.50 0.00     對 0.50 1.00     對 0.50 1.00
五、改造區
  ψ = Ry(2.094)|0⟩  修 X：True  修 Z：False
    ψ 本身 (x +0.87, z -0.50) 大小 1.00   Bob 的 q2 (x +0.00, z -0.50) 大小 0.50   一樣嗎？ False
    Bob 量到 1 的機率 0.75，ψ 本身 0.75
'''

# 製作代理實跑紀錄：qiskit 2.6.2，StatevectorSampler(seed=2026)，shots=1000（四個線路用同一個種子；|+⟩、|−⟩ 的次數因此相同）
QISKIT_OUTPUT = '''ψ = √¾|0⟩+½|1⟩   Bob 的 q2 和 ψ 的相似度（1 = 完全相同）：兩個都修 1.000，不修 0.500，只修 X 0.625；量 1000 次 Bob 得到 1：269 次
ψ = |1⟩          Bob 的 q2 和 ψ 的相似度（1 = 完全相同）：兩個都修 1.000，不修 0.500，只修 X 1.000；量 1000 次 Bob 得到 1：1000 次
ψ = |+⟩          Bob 的 q2 和 ψ 的相似度（1 = 完全相同）：兩個都修 1.000，不修 0.500，只修 X 0.500；量 1000 次 Bob 得到 1：536 次
ψ = |−⟩          Bob 的 q2 和 ψ 的相似度（1 = 完全相同）：兩個都修 1.000，不修 0.500，只修 X 0.500；量 1000 次 Bob 得到 1：536 次
     ┌─────────┐          ┌───┐   
q_0: ┤ Ry(π/3) ├───────■──┤ H ├─■─
     └──┬───┬──┘     ┌─┴─┐└───┘ │ 
q_1: ───┤ H ├─────■──┤ X ├──■───┼─
        └───┘   ┌─┴─┐└───┘┌─┴─┐ │ 
q_2: ───────────┤ X ├─────┤ X ├─■─
                └───┘     └───┘   
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q118：範例 5 隱形傳態——四種 ψ（純 Python，不需安裝任何套件）

執行：  python teleport_lab.py
它用一個很小的三位元模擬器（只認得 H、X、Z、Ry、CNOT、CZ；振幅都是實數），印出：
  一、四種 ψ 各傳一次（延遲量測版，和 basic-circuits.html#teleport 相同）：每一步「單看 q0」「單看 q2」的 Bloch 向量
  二、Alice 量到什麼、Bob 手上是什麼、要怎麼修（ψ = √¾|0⟩ + ½|1⟩）
  三、真的「先量再修」：Alice 量測、把 2 個位元交給信差、Bob 照紙條修正，各傳 1000 次
  四、拿掉修正、只修一半：Bob 的 q2 變成什麼
  五、改造區：自己選 ψ 的角度、要不要修 X、要不要修 Z，先預測，再執行
q0、q1 在 Alice 那裡，q2 在 Bob 那裡。位元字串寫成 |q2 q1 q0⟩：最右邊那位是 q0（和 Qiskit、basic-circuits.html 一樣）。
Bloch 向量只寫 x、z 兩個分量（振幅都是實數，所以 y = 0）；大小 1 是「單看它是確定的狀態」，0 是縮在球心、完全隨機。
"""
import random
from math import cos, pi, sin, sqrt

R2 = 1 / sqrt(2)

# 四種要傳的狀態 ψ（和 basic-circuits.html#teleport 上方的選項相同），以及在 q0 準備它的閘
PSI = {
    '√¾|0⟩+½|1⟩': [('ry', 0, pi / 3)],
    '|1⟩': [('x', 0)],
    '|+⟩': [('h', 0)],
    '|−⟩': [('x', 0), ('h', 0)],
}
ENTANGLE = [('h', 1), ('cx', 1, 2)]          # 第 2 步：q1、q2 成為 Bell 態，q2 交給 Bob
ALICE = [('cx', 0, 1), ('h', 0)]              # 第 3 步：Bell 量測的前半
FIX = [('cx', 1, 2), ('cz', 0, 2)]            # 第 4 步：延遲量測版的修正（q1 控制 X、q0 控制 Z）


def run(gates, s=None):
    """三顆位元（第 i 根柱子 = i 的二進位字串 q2 q1 q0），依序做 gates，回傳 8 個振幅"""
    if s is None:
        s = [1.0] + [0.0] * 7
    s = s[:]
    for g in gates:
        name = g[0]
        if name in ('cx', 'cz'):
            c, t = 1 << g[1], 1 << g[2]
            if name == 'cx':
                s = [s[i ^ t] if i & c else s[i] for i in range(8)]
            else:
                s = [-s[i] if (i & c and i & t) else s[i] for i in range(8)]
            continue
        m, new = 1 << g[1], s[:]
        for i in range(8):
            if i & m:
                continue
            a, b = s[i], s[i | m]                    # 這一顆是 0、是 1 的兩個振幅
            if name == 'h':
                new[i], new[i | m] = (a + b) * R2, (a - b) * R2
            elif name == 'x':
                new[i], new[i | m] = b, a
            elif name == 'z':
                new[i], new[i | m] = a, -b
            elif name == 'ry':
                c, sn = cos(g[2] / 2), sin(g[2] / 2)
                new[i], new[i | m] = c * a - sn * b, sn * a + c * b
            else:
                raise ValueError('只認得 h、x、z、ry、cx、cz：' + name)
        s = new
    return s


def bloch(s, q):
    """單看第 q 顆的 Bloch 向量 (x, z)"""
    m = 1 << q
    x = sum(2 * s[i] * s[i | m] for i in range(8) if not i & m)
    z = sum((-1 if i & m else 1) * a * a for i, a in enumerate(s))
    return x, z


def fmt(v):
    x, z = v
    return f'(x {x:+.2f}, z {z:+.2f}) 大小 {sqrt(x * x + z * z):.2f}'


def target(prep):
    """ψ 本身的 Bloch 向量（只在 q0 準備，其他位元不動）"""
    return bloch(run(prep), 0)


def same(u, v):
    return abs(u[0] - v[0]) < 1e-9 and abs(u[1] - v[1]) < 1e-9


def p1(s, q):
    """量第 q 顆得到 1 的機率"""
    return sum(a * a for i, a in enumerate(s) if i & (1 << q))


def q2_state(s, q1, q0):
    """Alice 量到 q1 q0 之後，Bob 的 q2 的兩個振幅（已經除以總大小）與這個結果的機率"""
    a = [s[(b << 2) | (q1 << 1) | q0] for b in (0, 1)]
    p = a[0] ** 2 + a[1] ** 2
    return [x / sqrt(p) for x in a], p


def name_of(a, psi):
    """Bob 手上的 a 是 ψ、Zψ、Xψ 還是 XZψ（整體正負號不算）"""
    z = [psi[0], -psi[1]]
    for nm, v in (('ψ', psi), ('Zψ', z), ('Xψ', [psi[1], psi[0]]), ('XZψ', [z[1], z[0]])):
        if abs(abs(a[0] * v[0] + a[1] * v[1]) - 1) < 1e-9:
            return nm
    return '?'


def correct(a, q1, q0):
    """Bob 照紙條修正：q1 = 1 做 X，q0 = 1 做 Z（先 X、再 Z）"""
    if q1:
        a = [a[1], a[0]]
    if q0:
        a = [a[0], -a[1]]
    return a


def classical(prep, k, rng):
    """先量再修：Alice 量 q0、q1，把 2 個位元交給信差，Bob 修正後量 q2。回傳 Alice 各結果次數與 Bob 量到 1 的次數"""
    s = run(prep + ENTANGLE + ALICE)
    alice, bob1 = {'00': 0, '01': 0, '10': 0, '11': 0}, 0
    want = run(prep)
    want = [want[0], want[1]]                       # ψ 的兩個振幅
    for _ in range(k):
        r, pick = rng.random(), None
        for q1 in (0, 1):
            for q0 in (0, 1):
                a, p = q2_state(s, q1, q0)
                if pick is None and r < p:
                    pick = (q1, q0, a)
                r -= p
        q1, q0, a = pick or (1, 1, q2_state(s, 1, 1)[0])
        alice[f'{q1}{q0}'] += 1
        a = correct(a, q1, q0)
        assert abs(abs(a[0] * want[0] + a[1] * want[1]) - 1) < 1e-9   # 修完一定是 ψ
        bob1 += rng.random() < a[1] ** 2
    return alice, bob1


STEPS = [('起點', []), ('①準備ψ', None), ('②糾纏對', ENTANGLE), ('③Alice', ALICE), ('④Bob修正', FIX)]

if __name__ == '__main__':
    rng = random.Random(1118)
    print('一、四種 ψ 各傳一次（延遲量測版）：每一步單看 q0、單看 q2')
    for nm, prep in PSI.items():
        print(f'  ψ = {nm}   ψ 的 Bloch 向量 {fmt(target(prep))}')
        done = []
        for tag, gates in STEPS:
            done += prep if gates is None else gates
            s = run(done)
            print(f'    {tag}：單看 q0 {fmt(bloch(s, 0))}   單看 q2 {fmt(bloch(s, 2))}')
        print(f'    傳完：q2 和 ψ 一樣嗎？ {same(bloch(s, 2), target(prep))}   Bob 量到 1 的機率 {p1(s, 2):.2f}（ψ 本身 {p1(run(prep), 0):.2f}）')
    print('  四種傳完，單看 q0 都一樣嗎？', len({tuple(round(c, 9) for c in bloch(run(p + ENTANGLE + ALICE + FIX), 0)) for p in PSI.values()}) == 1)

    print('二、Alice 量到什麼、Bob 手上是什麼（ψ = √¾|0⟩+½|1⟩，第 ③ 步之後）')
    prep = PSI['√¾|0⟩+½|1⟩']
    psi = run(prep)[:2]
    s = run(prep + ENTANGLE + ALICE)
    for q1 in (0, 1):
        for q0 in (0, 1):
            a, p = q2_state(s, q1, q0)
            fix = {(0, 0): '不用修', (0, 1): 'Z', (1, 0): 'X', (1, 1): '先 X、再 Z'}[(q1, q0)]
            b = correct(a, q1, q0)
            print(f'  q1 q0 = {q1}{q0}  機率 {p:.2f}  Bob 手上 ({a[0]:+.3f}, {a[1]:+.3f}) = {name_of(a, psi):<4}'
                  f'修正：{fix} → ({b[0]:+.3f}, {b[1]:+.3f}) = {name_of(b, psi)}')

    print('三、真的先量再修（古典通訊版），各傳 1000 次（random 種子 1118）')
    for nm, prep in PSI.items():
        alice, bob1 = classical(prep, 1000, rng)
        print(f'  ψ = {nm:<12}Alice 的結果 ' + '  '.join(f'{k}:{v}' for k, v in alice.items())
              + f'   Bob 量到 1：{bob1} 次（理論 {p1(run(prep), 0) * 1000:.0f} 次）')

    print('四、拿掉修正、只修一半：Bob 的 q2（延遲量測版；每格是「對或錯  量到 1 的機率  向量大小」）')
    FIXES = (('不修', []), ('只修 X', FIX[:1]), ('只修 Z', FIX[1:]), ('兩個都修', FIX))
    print(('  ψ              ' + ''.join(f'{tag:<14}' for tag, _ in FIXES)).rstrip())
    for nm, prep in PSI.items():
        cells = []
        for tag, fix in FIXES:
            s = run(prep + ENTANGLE + ALICE + fix)
            ok = '對' if same(bloch(s, 2), target(prep)) else '錯'
            cells.append(f'{ok} {p1(s, 2):.2f} {sqrt(sum(c * c for c in bloch(s, 2))):.2f}')
        print((f'  {nm:<15}' + ''.join(f'{c:<16}' for c in cells)).rstrip())

    # 五、改造區：先預測，再執行。THETA 是 Ry 的角度（0 = |0⟩、pi = |1⟩、pi / 2 = |+⟩），FIX_X、FIX_Z 決定 Bob 修不修
    THETA, FIX_X, FIX_Z = 2 * pi / 3, True, False
    prep = [('ry', 0, THETA)]
    s = run(prep + ENTANGLE + ALICE + (FIX[:1] if FIX_X else []) + (FIX[1:] if FIX_Z else []))
    print('五、改造區')
    print(f'  ψ = Ry({THETA:.3f})|0⟩  修 X：{FIX_X}  修 Z：{FIX_Z}')
    print(f'    ψ 本身 {fmt(target(prep))}   Bob 的 q2 {fmt(bloch(s, 2))}   一樣嗎？ {same(bloch(s, 2), target(prep))}')
    print(f'    Bob 量到 1 的機率 {p1(s, 2):.2f}，ψ 本身 {p1(run(prep), 0):.2f}')
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q118：用本機 Qiskit 重現隱形傳態——四種 ψ（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
延遲量測版：Bob 的修正寫成受控閘（q1 控制 X、q0 控制 Z），和 basic-circuits.html#teleport 相同。
"""
from math import pi

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import DensityMatrix, Statevector, partial_trace, state_fidelity

PREP = {'√¾|0⟩+½|1⟩': lambda qc: qc.ry(pi / 3, 0), '|1⟩': lambda qc: qc.x(0),
        '|+⟩': lambda qc: qc.h(0), '|−⟩': lambda qc: (qc.x(0), qc.h(0))}


def teleport(prep, fix_x=True, fix_z=True):
    qc = QuantumCircuit(3)
    prep(qc)            # ① 在 q0 準備 ψ
    qc.h(1)             # ② q1、q2 成為 Bell 態
    qc.cx(1, 2)
    qc.cx(0, 1)         # ③ Alice：CNOT、H
    qc.h(0)
    if fix_x:
        qc.cx(1, 2)     # ④ Bob：q1 = 1 就做 X（延遲量測：改成受控閘）
    if fix_z:
        qc.cz(0, 2)     #    q0 = 1 就做 Z
    return qc


for name, prep in PREP.items():
    one = QuantumCircuit(1)
    prep(one)
    psi = DensityMatrix(Statevector.from_instruction(one))
    row = []
    for tag, fx, fz in (('兩個都修', True, True), ('不修', False, False), ('只修 X', True, False)):
        qc = teleport(prep, fx, fz)
        bob = partial_trace(Statevector.from_instruction(qc), [0, 1])    # 只留下 q2
        row.append(f'{tag} {state_fidelity(bob, psi):.3f}')
    m = teleport(prep).copy()
    m.measure_all()
    counts = StatevectorSampler(seed=2026).run([m], shots=1000).result()[0].data.meas.get_counts()
    bob1 = sum(v for k, v in counts.items() if k[0] == '1')                # 字串最左邊是 q2
    print(f'ψ = {name:<12} Bob 的 q2 和 ψ 的相似度（1 = 完全相同）：' + '，'.join(row) + f'；量 1000 次 Bob 得到 1：{bob1} 次')
print(teleport(PREP['√¾|0⟩+½|1⟩']).draw())
'''

ALICE_TABLE = [  # (Alice 量到 q1 q0, 機率, 此時 Bob 的 q2, Bob 的修正, 修正後)
    ('00', '¼', 'ψ', '不用修', 'ψ'),
    ('01', '¼', 'Zψ', 'Z', 'ψ'),
    ('10', '¼', 'Xψ', 'X', 'ψ'),
    ('11', '¼', 'XZψ', '先 X、再 Z', 'ψ'),
]

FOUR = [  # (ψ, 在 q0 怎麼準備, 傳完 Bob 的 Bloch 箭頭, Bob 量到 1 的機率)
    ('√¾|0⟩ + ½|1⟩', 'Ry(π/3)', '往 +x 傾斜 60°（和一開始的 q0 同方向）', '25%'),
    ('|1⟩', 'X', '南極', '100%'),
    ('|+⟩', 'H', '赤道 +x', '50%'),
    ('|−⟩', 'X、H', '赤道 −x（和 |+⟩ 相反）', '50%'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q118：範例 5 隱形傳態——四種 ψ（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的範例 5。
上一課（Q117）把 CNOT 串成一條鏈，讓三、四顆位元一起糾纏；今天拿一對糾纏位元當通道，把 q0 的狀態 ψ 搬到遠方 Bob 的 q2。
核心一句話：**1 對糾纏位元 ＋ 2 個古典位元，送出 1 個量子位元的狀態；搬的是狀態不是粒子，原本的 q0 不再保有 ψ，而且沒有古典通訊就完成不了，所以不能超光速。**

## 線路（簡報第 15 頁、basic-circuits.html#teleport）

q0、q1 在 Alice 那裡，q2 在 Bob 那裡；三條線都從 |0⟩ 出發。

1. 準備 ψ（q0）：√¾|0⟩ + ½|1⟩ 用 Ry(π/3)；|1⟩ 用 X；|+⟩ 用 H；|−⟩ 用 X 再 H。
2. 建立糾纏對：H（q1）、CNOT（q1 → q2），q1、q2 成為 Bell 態 (|00⟩ + |11⟩)/√2。
3. Alice：CNOT（q0 → q1）、H（q0），然後量 q0、q1，得到 2 個古典位元。
4. Bob：照那 2 個位元修正：q1 = 1 做 X，q0 = 1 做 Z。修完 q2 就是 ψ。

## Alice 量到什麼、Bob 怎麼修（簡報第 16 頁；作品「傳送流程表」的答案）

| Alice 量到 q1 q0 | 機率 | 此時 Bob 的 q2 | Bob 的修正 | 修正後 |
|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in ALICE_TABLE) + '''
口訣：q1 管 X，q0 管 Z。收到 2 個位元之前，Bob 不知道是哪一種，四種等量混在一起，單看 q2 是完全隨機（Bloch 向量縮在球心）。

## 四種 ψ 傳完的樣子

| ψ | 準備 | Bob 的 Bloch 箭頭 | Bob 量到 1 的機率 |
|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in FOUR) + '''
|+⟩ 和 |−⟩ 量起來都是 50/50，量測分不出來，要看 Bloch 球（方向相反）。這也是為什麼「四種都要傳一次」：只用 |1⟩ 檢查，漏掉 Z 修正也看不出來。

## 延遲量測版（動畫用的寫法）

動畫和 teleport_lab.py 第一段不在中間真的量測，而是把 Bob 的修正改成受控閘：CNOT（q1 → q2）代替「q1 = 1 做 X」，CZ（q0、q2）代替「q0 = 1 做 Z」。
這叫延遲量測原理：把量測移到最後，結果的機率分布不變，q2 的結果和先量再修相同。代價是受控閘要求位元彼此靠近、能做兩位元閘；真的要傳到遠方，還是得先量、再用古典通訊送 2 個位元（teleport_lab.py 第三段就是這個版本）。
延遲量測版傳完後，q0 不管 ψ 是哪一種都停在同一個方向（+x），和 ψ 無關：原來的資訊已經不在 q0 身上。

## 拿掉修正（改造的答案）

- 不修：四種 ψ，Bob 的 q2 都縮在球心，量到 0、1 各一半。
- 只修 X：|1⟩ 照樣傳對；|+⟩、|−⟩ 縮到球心，但量起來仍是一半一半，**光看量測看不出傳錯**；√¾|0⟩ + ½|1⟩ 的量測機率也還是 25%，但向量只剩一半大小。
- 只修 Z：|+⟩、|−⟩ 傳對，|1⟩ 錯（量到 0、1 各一半）。
- 結論：兩個修正都要；檢查時四種 ψ 都要傳，而且要看 Bloch 球，不能只看量測次數。

## 常見誤解

- 不是複製：傳完以後 q0 不再保有 ψ（不可複製定理）。
- 不是瞬移：沒有粒子移動，Bob 的 q2 本來就在他手上，被改變的是它的狀態。
- 不能超光速：沒有那 2 個古典位元，Bob 什麼都做不了；收到之前，他的 q2 完全隨機。

## 影片的念法

Alice、Bob 念「愛麗絲」「鮑伯」；ψ 念「要傳的狀態」；H「哈達瑪閘」、X「翻轉閘」、Z「相位翻轉閘」、CNOT「受控反閘」、CZ「受控相位翻轉閘」、Ry「旋轉閘」；
|+⟩「正號疊加態」、|−⟩「負號疊加態」；Bell「貝爾態」；q0、q1、q2 念「編號零」到「編號二」；Bloch 球念「布洛赫球」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；分配角色：Alice、Bob、信差（兩個人時信差由小紙條扮演） | 影片、列印包第 2 頁 |
| 10–25 | 對照簡報第 15–17 頁：四步驟、Alice 的四種結果與修正、Bloch 球看搬家 | 簡報 basic-circuits.pptx p15–17 |
| 25–65 | 在 basic-circuits.html#teleport 四種 ψ 各傳一次：逐步看兩顆 Bloch 球，最後量 1,000 次；填傳送流程表 | `01_操作步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子在 teleport_lab.py 拿掉修正、只修一半，先預測再執行；在動畫停在第 3 步量測對照 | 列印包第 3 頁、`03_傳送流程表.csv` |
| 105–115 | 孩子教爸爸：步驟、修正口訣、限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#teleport`：上方「要傳的狀態 ψ」四個選項；按「⏮ 起點」「下一步 ▶」「量測 1,000 次」。
- 選用：開 `operation.html#circuit`（場景 6），按「量子隱形傳態」，再按「單步 ▶」8 次，看三維版的同一條線路（那裡的 ψ 是 Ry(2π/3)，量到 1 的機率 75%，和 basic-circuits 的預設相反，別搞混）。
- 打開簡報 `slides/output/basic-circuits.pptx` 第 15–17 頁（課綱寫 p15–17，頁碼無誤）。
- 列印 `02_列印包_傳送流程表.pdf`（A4，共 4 頁），把第 2 頁的三張角色卡剪下來。
- 有 Python 的電腦先跑一次 `python teleport_lab.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 本課四種 ψ 的振幅都是實數，Bloch 向量只在 x–z 平面；複數振幅的 ψ 不在本課範圍。
- 量 1,000 次的次數是隨機的，每次都會差一點；理論值見上表。
- 振幅柱子和 Bloch 球是模擬器才看得到的；真實的量子電腦只給量測結果。
- 延遲量測版傳完 q0 停在 |+⟩ 是這種寫法的結果；真的先量再修時，q0 會被量成 0 或 1。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：四種 ψ 各傳一次（約 40 分鐘）

1. 先分配角色：Alice（管 q0、q1）、Bob（管 q2）、信差（拿紙條送 2 個位元）。在列印包第 1 頁寫預測：傳完 Bob 的箭頭會指向哪裡？
2. 打開 `animations/basic-circuits.html#teleport`（範例 5 隱形傳態）。上方「要傳的狀態 ψ」預設是 √¾|0⟩+½|1⟩。
3. 按「下一步 ▶」（① 準備 ψ）：左邊「單看 q0」的箭頭往 +x 傾斜；右邊「單看 q2」還在北極。
4. 再按（② 糾纏對）：右邊 q2 的箭頭縮進球心——糾纏中的 q2，單看完全隨機。
5. 再按（③ Alice）：左邊 q0 的箭頭也變短；q2 仍在球心。說明寫著 q1 q0 = 00、01、10、11 各 ¼，Bob 分別是 ψ、Zψ、Xψ、XZψ。
6. 再按（④ Bob 修正，虛線框「修正（2 個古典位元）」）：q2 的箭頭伸出來，指向第 1 步時 q0 傾斜的方向；左邊 q0 則倒到赤道 +x。
7. 按「量測 1,000 次」：只量 q2，灰色底是理論（0 75%、1 25%），下方出現綠字「對照 ψ：q2 的量測機率和 ψ 相同」。寫進列印包第 1 頁。
8. 換 |1⟩、|+⟩、|−⟩：頁面會直接跳到最後一步；想逐步看就先按「⏮ 起點」。每一種都記下 Bob 的箭頭方向與量測結果。|+⟩、|−⟩ 量起來一樣，箭頭方向相反。

## 下半場：拿掉修正（約 30 分鐘）

1. 在列印包第 3 頁寫預測：不修、只修 X、只修 Z，四種 ψ 各會怎樣？
2. 在動畫選 |1⟩，點電路下方右邊的第 4 個小圓點（停在第 3 步，修正還沒做），量 1,000 次：0、1 各約一半。再按「下一步 ▶」修正，量 1,000 次：全部是 1。
3. 執行 `python teleport_lab.py`，對照第四段的表。注意「只修 X」時 |+⟩：量到 1 的機率仍是 0.50，向量大小卻是 0——量測看不出傳錯。
4. 看第三段「先量再修」：Alice 真的量測、信差送紙條、Bob 照紙條修，四種結果各約四分之一，每次修完都等於 ψ。
5. 打開 `teleport_lab.py` 最下面的改造區，改 `THETA`、`FIX_X`、`FIX_Z`，先預測，再執行。
6. 有裝 Qiskit 的話，跑 `qiskit_check.py`：兩個都修相似度 1.000；不修 0.500；只修 X 時 |1⟩ 是 1.000，|+⟩、|−⟩ 是 0.500。
7. 選用：開 `animations/operation.html#circuit`，按「量子隱形傳態」，再按「單步 ▶」8 次，看三維版的線路、每條線最左邊的小 Bloch 球與最後的直方圖。
''',

'teleport_lab.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## teleport_lab.py 實跑輸出（Python 3.13.18，random.Random(1118)）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- Alice 做了什麼？CNOT（q0 → q1）再 H（q0），然後量 q0、q1。這兩個閘加上量測，就是 Bell 量測。\n'
  '- Bob 怎麼修？q1 = 1 做 X，q0 = 1 做 Z（兩個都是 1 就先 X 再 Z）。修完一定是 ψ（第二段、第三段）。\n'
  '- 紙條送到之前，Bob 自己量會怎樣？四種情況等量混在一起，q2 單看在球心，0、1 各一半，和 ψ 無關，所以得不到任何消息。\n'
  '- 為什麼不能超光速？Bob 一定要等到 2 個古典位元，而古典訊號不會比光快。\n'
  '- 為什麼不算複製？傳完以後 q0 的狀態和 ψ 無關（第一段：四種傳完 q0 都一樣，True）；ψ 只剩在 q2 上。\n'
  '- 延遲量測版和先量再修一樣嗎？Bob 的 q2 一樣（第一段 True、第三段每次修完都等於 ψ）。差別在受控閘要求位元靠近，真的傳遠要先量。\n'
  '- 只修 X 為什麼量不出錯？Z 只改 |1⟩ 的正負號，量 0、1 的機率不變；要看 Bloch 球（向量大小變小）才知道。所以檢查要傳 |+⟩、|−⟩，還要看箭頭。\n'
  '- 改造區的預設 THETA = 2π/3、只修 X：ψ 量到 1 的機率 0.75，Bob 也是 0.75，但 Bob 的向量大小只有 0.50，一樣嗎？False。\n'
  '- 下一課 Q119：範例 6 Deutsch——紅綠球搖獎機。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html#teleport`（範例 5 隱形傳態）

- 上方「要傳的狀態 ψ」：√¾|0⟩+½|1⟩（預設）、|1⟩、|+⟩、|−⟩。換選項時頁面停在最後一步並清除量測；按目前已選的選項不會有反應。
- 電路：q0、q1 在 Alice，q2 在 Bob；四步依序是準備 ψ、建立糾纏對、Alice 的 CNOT 與 H、虛線框「修正（2 個古典位元）」裡的 CNOT 與 CZ；只量 q2。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」，右邊 5 個小圓點可以直接跳到起點或某一步。
- 「振幅與機率」：8 根柱子，字串是 |q2 q1 q0⟩；藍色正振幅、橘色負振幅。下面兩顆 Bloch 球：左「單看 q0」、右「單看 q2」；向量變短代表和別的位元糾纏，縮到球心就是單看它完全隨機。
- 「量測 1 次」「量測 1,000 次」「清除」：只量 q2；最後一步量測時出現綠字「→ 對照 ψ：q2 的量測機率和 ψ 相同」。
- 頁面最下面的「Qiskit 程式碼」會隨 ψ 改變，並註明真實硬體要先量測 q0、q1 再依結果做 X、Z。

## `animations/operation.html#circuit`（場景 6：量子線路：一步一步執行，選用）

- 上排按鈕選線路，按「量子隱形傳態」；「⏮ 重設」「單步 ▶」「播放」；開關「加入雜訊（每閘 1%、讀取 3%）」。
- 8 欄：Ry 準備 q0（cos60°|0⟩ + sin60°|1⟩，量到 1 的機率 0.75）、H、CNOT、Alice 的 CNOT、H、Bob 的受控 X、受控 Z（延遲量測）、量測 q2。
- 每條線最左邊的小球是那顆位元的約化 Bloch 向量；最後的量測欄跑 1000 shots，插圖顯示直方圖（青線 = 理想機率）。

## 操作

basic-circuits.html：左右方向鍵 上一步／下一步；空白鍵 播放；點電路上的閘可以直接跳到那一步。
''',
}

SHEET_HEADER = ['ψ', '準備的閘', '② 之後 q2 的箭頭', 'Alice 量到 q1 q0', 'Bob 的修正', '修正後 q2 的箭頭', 'Bob 量 1000 次', '和 ψ 一樣嗎', '備註']
SHEET_ROWS = [['範例：√¾|0⟩+½|1⟩', 'Ry(π/3)', '球心', '（延遲量測版不用量）', 'CNOT(q1→q2)、CZ(q0,q2)', '往 +x 傾斜，同 q0 一開始', '0 約 750、1 約 250', '一樣', '理論 0 75%、1 25%'],
              ['|1⟩', 'X', '', '', '', '', '', '', ''], ['|+⟩', 'H', '', '', '', '', '', '', ''], ['|−⟩', 'X、H', '', '', '', '', '', '', ''],
              ['改造：拿掉修正', '', '', '', '不修', '', '', '', ''], ['我的改造', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:10mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:16%}
table.judge th{font-size:10.5pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.roles{display:flex;gap:4mm;margin:3mm 0}.role{flex:1;border:1.5pt dashed #4a6a85;border-radius:3mm;padding:3mm;font-size:11pt}
.role b{display:block;font-size:14pt;color:#0b2540;margin-bottom:1mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 teleport_lab.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'teleport_lab.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    row = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    alice = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td></tr>'  # noqa: E731
    cut = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    pages = [
        '<h2>傳送流程表：四種 ψ 各傳一次</h2><p class="lead">basic-circuits.html#teleport：選 ψ → ⏮ 起點 → 下一步 ×4 → 量測 1,000 次。左球「單看 q0」，右球「單看 q2」。</p>'
        '<table class="judge"><tr><th style="width:16%">ψ</th><th>① 之後 q0 的箭頭</th><th>② 之後 q2 的箭頭</th><th>④ 之後 q2 的箭頭</th><th>Bob 量 1,000 次</th></tr>'
        + row('√¾|0⟩+½|1⟩') + row('|1⟩') + row('|+⟩') + row('|−⟩') + '</table>'
        '<p>我的預測：傳完以後，Bob 的箭頭會指向＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>四種傳完，左邊 q0 的箭頭在哪裡？＿＿＿＿＿＿＿＿＿＿　和 ψ 有關嗎？＿＿＿＿</p>'
        '<p>|+⟩ 和 |−⟩ 的量測結果一樣嗎？要看什麼才分得出來？</p><div class="line"></div>',
        '<h2>三人傳送：角色卡與修正表</h2><p class="lead">剪下角色卡。兩個人上課時，信差由一張小紙條扮演；紙條送到之前，Bob 不能動。</p>'
        '<div class="roles"><div class="role"><b>Alice</b>管 q0、q1。準備 ψ，做 CNOT（q0 → q1）、H（q0），量出 2 個位元，寫在紙條上。</div>'
        '<div class="role"><b>信差</b>把紙條上的 2 個位元送到 Bob 手上。沒有信差，傳送就完成不了；信差再快也快不過光。</div>'
        '<div class="role"><b>Bob</b>管 q2。收到紙條才修正：q1 = 1 做 X，q0 = 1 做 Z。修完 q2 就是 ψ。</div></div>'
        '<table class="judge"><tr><th style="width:16%">Alice 量到 q1 q0</th><th>機率</th><th>此時 Bob 的 q2</th><th>Bob 要做的修正</th></tr>'
        + alice('00') + alice('01') + alice('10') + alice('11') + '</table>'
        '<p>修正口訣：q1 管＿＿＿，q0 管＿＿＿。</p>'
        '<p>紙條送到之前，Bob 自己量會得到什麼？為什麼這代表不能超光速？</p><div class="line"></div>',
        '<h2>換你改造：拿掉修正</h2><p class="lead">先預測，再用 teleport_lab.py 驗證。每格寫：傳對或傳錯、Bob 量到 1 的機率、向量大小。</p>'
        '<table class="judge"><tr><th style="width:22%">ψ</th><th>不修</th><th>只修 X</th><th>只修 Z</th><th>兩個都修</th></tr>'
        + cut('√¾|0⟩+½|1⟩') + cut('|1⟩') + cut('|+⟩') + cut('|−⟩') + '</table>'
        '<p>只修 X 時，|+⟩ 量起來還是一半一半，算傳對嗎？你怎麼看出來的？</p><div class="line"></div>'
        '<p>動畫停在第 3 步量 1,000 次，和修正後量 1,000 次，差在哪裡？</p><div class="line"></div>'
        '<pre class="code"># teleport_lab.py 最下面的改造區\n'
        'THETA, FIX_X, FIX_Z = 2 * pi / 3, True, False   # ψ = Ry(THETA)|0⟩；Bob 修不修 X、修不修 Z\n'
        '# THETA：0 是 |0⟩、pi 是 |1⟩、pi / 2 是 |+⟩；改完先預測，再執行</pre>',
        '<h2>最後一關：教爸爸傳送</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. Alice 要做哪些步驟（不看稿）：</p><div class="line"></div>'
        '<p>2. Bob 怎麼依照 2 個位元修正：</p><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：糾纏對 → Alice 做 CNOT、H → 量出 2 個位元</li><li>說出：q1 = 1 做 X，q0 = 1 做 Z</li>'
        '<li>指出：沒有古典通訊就完成不了，所以不能超光速</li><li>指出：傳完 q0 不再保有 ψ，是搬家不是複製</li>'
        '<li>完成傳送流程表，四種 ψ 都和 teleport_lab.py 一致</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q118 傳送流程表 列印包', '父子科技學院 量子電腦學程 Q118｜範例 5：隱形傳態——四種 ψ', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q118-teleport-four-psi', folder='Q118_範例5_隱形傳態_四種ψ', files=FILES,
        sheet=('03_傳送流程表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_傳送流程表.pdf', pack_pages=4,
        pack_needles=('傳送流程表', '三人傳送', '拿掉修正', 'FIX_X', '最後一關'),
        authoring_dir=XINEW / 'authoring/q118', episode_dir='specials/q118-teleport-four-psi',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；teleport_lab.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'teleport_lab.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, random seed 1118); qiskit 2.6.2',
               'recordedRun': {'q2AfterFix': {'√¾|0⟩+½|1⟩': [0.87, 0.5], '|1⟩': [0.0, -1.0], '|+⟩': [1.0, 0.0], '|−⟩': [-1.0, 0.0]},
                               'q2AfterEntangle': [0.0, 0.0], 'q0AfterFixAllPsi': [1.0, 0.0],
                               'aliceTable': {'00': 'ψ', '01': 'Zψ', '10': 'Xψ', '11': 'XZψ'},
                               'classical1118': {'√¾|0⟩+½|1⟩': 245, '|1⟩': 1000, '|+⟩': 524, '|−⟩': 517},
                               'noFixP1': 0.5, 'onlyXCorrect': ['|1⟩'], 'onlyZCorrect': ['|+⟩', '|−⟩'],
                               'qiskitFidelity': {'fixBoth': 1.0, 'noFix': 0.5}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q118/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q126 課堂教材：理想 vs 雜訊比較圖、三個旋鈕與錯誤預算、雜訊加倍紀錄表、最後一關檢核表；雜訊模型 notebook（雜訊模型.ipynb 與同內容的 noise_lab.py）、
純 Python 的頁面雜訊規則 page_noise.py、解答與動畫導覽。

noise_lab.py 需要 Python 3 與 pip install qiskit qiskit-aer（不需要帳號）；page_noise.py 只要 Python 3（沒有亂數，算出頁面規則的期望值）。
建置時會真的執行一次 page_noise.py，確認輸出和影片、教材寫的結果一致；Qiskit 部分（portable-runtime 沒有 Qiskit）比對製作代理已記錄的實跑輸出，
並檢查雜訊模型.ipynb 是合法的 notebook JSON、程式格內容與 noise_lab.py 相同。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \\
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q126/classroom.py
"""
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import tempfile

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，沒有亂數
RUN_OUTPUT = '''一、加入雜訊（每閘 1%、讀取 3%）：每次變成隨機的機會，和答案還剩多少
  1 疊加：1 個閘 → 變成隨機 1.0%；0 50.0%、1 50.0%；跑掉 0.0%
  2 干涉：3 個閘 → 變成隨機 3.0%；1 95.6%；跑掉 4.4%
  3 Bell 態：2 個閘 → 變成隨機 2.0%；00 46.7%、11 46.7%；跑掉 6.7%
  4 GHZ 態：3 個閘 → 變成隨機 3.0%；000 44.7%、111 44.7%；跑掉 10.7%
  5 隱形傳態：7 個閘 → 變成隨機 6.8%；0 71.9%、1 28.1%；跑掉 3.1%
  6 Deutsch：5 個閘 → 變成隨機 4.9%；1 94.7%；跑掉 5.3%
  7 BV：10 個閘 → 變成隨機 9.6%；101 83.7%；跑掉 16.3%
  8 Grover：12 個閘 → 變成隨機 11.4%；11 86.2%；跑掉 13.8%
二、雜訊一直加倍：跑掉的比例
  範例           ×1      ×2      ×4      ×8
  1 疊加          0.0%    0.0%    0.0%    0.0%
  2 干涉          4.4%    8.6%   16.4%   29.8%
  3 Bell 態      6.7%   12.8%   23.4%   38.6%
  4 GHZ 態      10.7%   20.3%   36.7%   59.2%
  5 隱形傳態        3.1%    5.9%   10.7%   17.7%
  6 Deutsch     5.3%   10.2%   19.0%   32.9%
  7 BV         16.3%   29.8%   50.5%   73.9%
  8 Grover     13.8%   25.3%   42.9%   63.0%
三、改造區：雜訊 ×2（每閘 2%、讀取 6%）
  3 Bell 態：00 43.6%、01 6.4%、10 6.4%、11 43.6%
  4 GHZ 態：000 39.8%、001 3.4%、010 3.4%、011 3.4%、100 3.4%、101 3.4%、110 3.4%、111 39.8%
  8 Grover：00 5.7%、01 9.8%、10 9.8%、11 74.7%
'''

# 製作代理實跑紀錄：qiskit 2.6.2、qiskit-aer 0.18.4（Python 3.13.18），AerSimulator seed_simulator=126
QISKIT_OUTPUT = '''雜訊模型（假設）：單位元閘 1%、雙位元閘 2%、讀取 3%；每種跑 1000 次
一、理想 vs 雜訊比較圖（雜訊 ×1）
  3 Bell 態（單位元閘 1 個、雙位元閘 1 個；雜訊 ×1）
    00  理想 ████████████████████                      50.0%
        雜訊 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                       46.4%
    01  理想                                            0.0%
        雜訊 ▒                                          2.7%
    10  理想                                            0.0%
        雜訊 ▒                                          3.4%
    11  理想 ████████████████████                      50.0%
        雜訊 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                       47.5%
    跑掉的比例 6.1%
  4 GHZ 態（單位元閘 1 個、雙位元閘 2 個；雜訊 ×1）
    000  理想 ████████████████████                      50.0%
         雜訊 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                         43.3%
    001  理想                                            0.0%
         雜訊 ▒                                          2.7%
    010  理想                                            0.0%
         雜訊 ▒                                          1.8%
    011  理想                                            0.0%
         雜訊 ▒                                          1.4%
    100  理想                                            0.0%
         雜訊                                            1.2%
    101  理想                                            0.0%
         雜訊 ▒                                          1.4%
    110  理想                                            0.0%
         雜訊 ▒                                          1.7%
    111  理想 ████████████████████                      50.0%
         雜訊 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                       46.5%
    跑掉的比例 10.2%
  8 Grover（單位元閘 10 個、雙位元閘 2 個；雜訊 ×1）
    00  理想                                            0.0%
        雜訊 ▒                                          1.8%
    01  理想                                            0.0%
        雜訊 ▒▒                                         5.5%
    10  理想                                            0.0%
        雜訊 ▒▒                                         5.4%
    11  理想 ████████████████████████████████████████ 100.0%
        雜訊 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒       87.3%
    跑掉的比例 12.7%
二、把雜訊一直加倍：八個範例跑掉的比例（每格 10000 次）
  範例          閘數(單/雙)   ×1      ×2      ×4      ×8   ×8 時最高的結果
  1 疊加          1 / 0     0.5%    0.6%    0.8%    0.5%   1（仍是答案）
  2 干涉          3 / 0     3.9%    7.7%   15.6%   29.2%   1（仍是答案）
  3 Bell 態      1 / 1     6.9%   12.9%   23.6%   38.3%   11（仍是答案）
  4 GHZ 態       1 / 2    10.9%   20.3%   37.1%   59.6%   111（仍是答案）
  5 隱形傳態        3 / 4     4.2%    7.8%   13.2%   19.5%   0（仍是答案）
  6 Deutsch     4 / 1     5.2%    9.9%   19.4%   33.6%   1（仍是答案）
  7 BV          8 / 2    13.8%   25.8%   45.1%   68.8%   101（仍是答案）
  8 Grover     10 / 2    13.7%   24.4%   41.6%   61.8%   11（仍是答案）
三、沒有單一答案的兩個範例（雜訊 ×1 與 ×8，各 10000 次）
  1 疊加：理想 0 是 50.0%；雜訊 ×1 是 49.5%；×8 是 49.5%
  5 隱形傳態：理想 0 是 75.0%；雜訊 ×1 是 70.8%；×8 是 55.5%
四、改造區：雜訊 ×2
  8 Grover（單位元閘 10 個、雙位元閘 2 個；雜訊 ×2）
    00  理想                                            0.0%
        雜訊 ▒▒                                         4.1%
    01  理想                                            0.0%
        雜訊 ▒▒▒▒                                      10.5%
    10  理想                                            0.0%
        雜訊 ▒▒▒▒▒                                     11.9%
    11  理想 ████████████████████████████████████████ 100.0%
        雜訊 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒             73.5%
    跑掉的比例 26.5%
五、延伸：故意把雜訊加倍，再往回推到「沒有雜訊」
  Grover 答案 11 的比例：雜訊 ×1 是 86.3%，×2 是 75.6%
  直線往回推到 ×0：2 × 0.863 − 0.756 = 97.0%（理想是 100%）
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q126：加入雜訊——八個範例在真實世界會怎樣（雜訊模型 notebook 的程式版）

安裝（只要一次）：  pip install qiskit qiskit-aer
執行：              python noise_lab.py
八個範例的線路和 Q124 的 eight_examples.py 一樣（照 basic-circuits.html 預設選項抄寫）。
雜訊模型是「假設」，不代表任何一台真實的量子電腦；三個參數寫在下面，要改就改這裡：
  P1：單位元閘（h、x、z、ry）做完後，有 P1 的機會被「去極化」（狀態被隨機打亂）
  P2：雙位元閘（cx、cz）做完後，兩顆位元一起有 P2 的機會被去極化
  PR：讀取時，每顆位元有 PR 的機會讀錯（0 讀成 1，或 1 讀成 0）
位元字串的最右邊是 q0。固定亂數種子，所以每次執行結果相同；拿掉 seed_simulator 就每次不同。
"""
# %% 匯入
from math import pi

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error

# %% 雜訊模型的三個參數（假設值）與改造區
P1, P2, PR = 0.01, 0.02, 0.03
MY_SCALE = 2        # 改造區：把三個參數一起乘上幾倍（1 = 原本、2 = 加倍）
SHOTS = 1000


def noise_model(scale=1):
    """照 P1、P2、PR 乘上 scale，建立一個雜訊模型"""
    nm = NoiseModel(basis_gates=['h', 'x', 'z', 'ry', 'cx', 'cz'])
    nm.add_all_qubit_quantum_error(depolarizing_error(P1 * scale, 1), ['h', 'x', 'z', 'ry'])
    nm.add_all_qubit_quantum_error(depolarizing_error(P2 * scale, 2), ['cx', 'cz'])
    r = PR * scale
    nm.add_all_qubit_readout_error(ReadoutError([[1 - r, r], [r, 1 - r]]))
    return nm


# %% 八個範例（同 Q124）
def superposition():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def interference():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.z(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def ghz():
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc


def teleport(angle=pi / 3):
    qc = QuantumCircuit(3, 1)
    qc.ry(angle, 0)
    qc.h(1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.h(0)
    qc.cx(1, 2)
    qc.cz(0, 2)
    qc.measure(2, 0)
    return qc


def deutsch():
    qc = QuantumCircuit(2, 1)
    qc.x(1)
    qc.h([0, 1])
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def bv(secret='101'):
    qc = QuantumCircuit(4, 3)
    qc.x(3)
    qc.h([0, 1, 2, 3])
    for q in range(3):
        if secret[2 - q] == '1':
            qc.cx(q, 3)
    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc


def grover():
    qc = QuantumCircuit(2, 2)
    qc.h([0, 1])
    qc.cz(0, 1)
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    qc.measure([0, 1], [0, 1])
    return qc


CIRCUITS = {'1 疊加': superposition, '2 干涉': interference, '3 Bell 態': bell, '4 GHZ 態': ghz,
            '5 隱形傳態': teleport, '6 Deutsch': deutsch, '7 BV': bv, '8 Grover': grover}


def ideal(qc):
    """理想機率（Statevector，不含雜訊）"""
    measured = sorted(qc.find_bit(i.qubits[0]).index for i in qc.data if i.operation.name == 'measure')
    sv = Statevector(qc.remove_final_measurements(inplace=False))
    return {k: v for k, v in sv.probabilities_dict(qargs=measured).items() if v > 1e-12}


def noisy(qc, scale=1, shots=SHOTS, seed=126):
    """有雜訊的模擬：回傳每個結果的比例"""
    sim = AerSimulator(noise_model=noise_model(scale), seed_simulator=seed)
    counts = sim.run(qc, shots=shots).result().get_counts()
    return {k: v / shots for k, v in counts.items()}


def gates(qc):
    one = sum(1 for i in qc.data if i.operation.name in ('h', 'x', 'z', 'ry'))
    two = sum(1 for i in qc.data if i.operation.name in ('cx', 'cz'))
    return one, two


def off(p, q):
    """跑掉的比例：把有雜訊的直方圖搬回理想的樣子，最少要搬走幾成（兩邊差的一半）"""
    return sum(abs(p.get(k, 0) - q.get(k, 0)) for k in set(p) | set(q)) / 2


def compare(name, scale=1):
    """理想 vs 雜訊比較圖（文字版）：每個結果兩條，上面理想、下面有雜訊"""
    qc = CIRCUITS[name]()
    p, q = ideal(qc), noisy(qc, scale)
    n = qc.num_clbits
    one, two = gates(qc)
    print(f'  {name}（單位元閘 {one} 個、雙位元閘 {two} 個；雜訊 ×{scale}）')
    for i in range(2 ** n):
        k = format(i, f'0{n}b')
        a, b = p.get(k, 0), q.get(k, 0)
        print(f'    {k}  理想 {"█" * round(a * 40):<40} {a:6.1%}')
        print(f'    {" " * n}  雜訊 {"▒" * round(b * 40):<40} {b:6.1%}')
    print(f'    跑掉的比例 {off(p, q):.1%}')


# %% 一、理想 vs 雜訊比較圖：Bell、GHZ、Grover
print(f'雜訊模型（假設）：單位元閘 {P1:.0%}、雙位元閘 {P2:.0%}、讀取 {PR:.0%}；每種跑 {SHOTS} 次')
print('一、理想 vs 雜訊比較圖（雜訊 ×1）')
for name in ('3 Bell 態', '4 GHZ 態', '8 Grover'):
    compare(name)

# %% 二、把雜訊加倍：八個範例跑掉的比例
print('二、把雜訊一直加倍：八個範例跑掉的比例（每格 10000 次）')
print('  範例          閘數(單/雙)   ×1      ×2      ×4      ×8   ×8 時最高的結果')
for name, make in CIRCUITS.items():
    qc = make()
    p = ideal(qc)
    row = []
    for s in (1, 2, 4, 8):
        q = noisy(qc, s, shots=10000)
        row.append(off(p, q))
    top = max(q, key=q.get)
    one, two = gates(qc)
    right = '仍是答案' if p.get(top, 0) == max(p.values()) else '已經不是答案'
    print(f'  {name:<10}  {one:>3} / {two}   ' + '  '.join(f'{x:6.1%}' for x in row) + f'   {top}（{right}）')

# %% 三、沒有單一答案的兩個範例：疊加與隱形傳態
print('三、沒有單一答案的兩個範例（雜訊 ×1 與 ×8，各 10000 次）')
for name in ('1 疊加', '5 隱形傳態'):
    qc = CIRCUITS[name]()
    p = ideal(qc)
    q1, q8 = noisy(qc, 1, shots=10000), noisy(qc, 8, shots=10000)
    print(f'  {name}：理想 0 是 {p.get("0", 0):.1%}；雜訊 ×1 是 {q1.get("0", 0):.1%}；×8 是 {q8.get("0", 0):.1%}')


# %% 四、改造區：MY_SCALE
print(f'四、改造區：雜訊 ×{MY_SCALE}')
compare('8 Grover', MY_SCALE)

# %% 五、延伸：零雜訊外插（簡報第 48 頁 ZNE 的最簡單版本）
print('五、延伸：故意把雜訊加倍，再往回推到「沒有雜訊」')
qc = grover()
a = noisy(qc, 1, shots=10000).get('11', 0)
b = noisy(qc, 2, shots=10000).get('11', 0)
print(f'  Grover 答案 11 的比例：雜訊 ×1 是 {a:.1%}，×2 是 {b:.1%}')
print(f'  直線往回推到 ×0：2 × {a:.3f} − {b:.3f} = {2 * a - b:.1%}（理想是 100%）')
'''

PURE_PROGRAM = '''"""父子科技學院 量子電腦學程 Q126：頁面的雜訊規則，算出期望值（純 Python，不需要安裝任何套件，也沒有亂數）

執行：  python page_noise.py
animations/operation.html 的「量子線路」場景有一個開關「加入雜訊（每閘 1%、讀取 3%）」，它的規則是：
  1. 線路有 G 個閘，每個閘有 1% 的機會出錯；只要有一個出錯，這一次的結果就變成「完全隨機」
     → 每次變成隨機的機會 = 1 − 0.99 的 G 次方
  2. 讀取時，每顆位元再各有 3% 的機會讀錯（0、1 對調）
這個程式不抽樣，直接把「跑很多很多次」會得到的比例算出來。SCALE 把 1% 和 3% 一起放大：2 = 雜訊加倍。
八個範例的閘數照 Q124 eight_examples.py 的線路數（不含量測）；理想機率照 basic-circuits.html 預設選項。
"""

# 範例名稱、閘數 G、理想機率（位元字串最右邊是 q0）
EXAMPLES = [
    ('1 疊加', 1, {'0': 0.5, '1': 0.5}),
    ('2 干涉', 3, {'1': 1.0}),
    ('3 Bell 態', 2, {'00': 0.5, '11': 0.5}),
    ('4 GHZ 態', 3, {'000': 0.5, '111': 0.5}),
    ('5 隱形傳態', 7, {'0': 0.75, '1': 0.25}),
    ('6 Deutsch', 5, {'1': 1.0}),
    ('7 BV', 10, {'101': 1.0}),
    ('8 Grover', 12, {'11': 1.0}),
]

GATE, READ = 0.01, 0.03   # 頁面的參數：每閘 1%、每顆位元讀取 3%
MY_SCALE = 2              # 改造區：雜訊放大幾倍


def expected(G, theory, scale=1):
    """照頁面的規則，算出每個結果的期望比例"""
    n = len(next(iter(theory)))
    keys = [format(i, f'0{n}b') for i in range(2 ** n)]
    pg = 1 - (1 - GATE * scale) ** G           # 這一次變成完全隨機的機會
    pr = READ * scale                          # 每顆位元讀錯的機會
    before = {k: (1 - pg) * theory.get(k, 0) + pg / 2 ** n for k in keys}
    after = {}
    for k in keys:
        total = 0
        for j, p in before.items():
            d = sum(a != b for a, b in zip(j, k))      # 要讀錯幾顆位元，j 才會變成 k
            total += p * pr ** d * (1 - pr) ** (n - d)
        after[k] = total
    return pg, after


def off(theory, p):
    """跑掉的比例：把有雜訊的直方圖搬回理想的樣子，最少要搬走幾成"""
    return sum(abs(theory.get(k, 0) - v) for k, v in p.items()) / 2


if __name__ == '__main__':
    print('一、加入雜訊（每閘 1%、讀取 3%）：每次變成隨機的機會，和答案還剩多少')
    for name, G, th in EXAMPLES:
        pg, p = expected(G, th)
        ans = '、'.join(f'{k} {p[k]:.1%}' for k in sorted(th))
        print(f'  {name}：{G} 個閘 → 變成隨機 {pg:.1%}；{ans}；跑掉 {off(th, p):.1%}')
    print('二、雜訊一直加倍：跑掉的比例')
    print('  範例           ×1      ×2      ×4      ×8')
    for name, G, th in EXAMPLES:
        print(f'  {name:<10}' + ''.join(f'{off(th, expected(G, th, s)[1]):8.1%}' for s in (1, 2, 4, 8)))
    print(f'三、改造區：雜訊 ×{MY_SCALE}（每閘 {GATE * MY_SCALE:.0%}、讀取 {READ * MY_SCALE:.0%}）')
    for name, G, th in EXAMPLES:
        if name in ('3 Bell 態', '4 GHZ 態', '8 Grover'):
            pg, p = expected(G, th, MY_SCALE)
            print(f'  {name}：' + '、'.join(f'{k} {v:.1%}' for k, v in p.items()))
'''


def notebook(src):
    """把 noise_lab.py 依「# %%」切成格：開頭說明變成文字格，每一段前面加一格標題文字（同 Q124）。"""
    _, doc, body = src.split('"""', 2)
    body = body.lstrip('\n')
    cells = [{'cell_type': 'markdown', 'metadata': {}, 'source': ['# 雜訊模型 notebook（Q126）\n', '\n'] + [ln + '\n' for ln in doc.splitlines()]}]
    for chunk in re.split(r'(?m)^# %% ', body)[1:]:
        title, _, code = chunk.partition('\n')
        code = code.strip('\n')
        cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': ['## ' + title]})
        lines = code.split('\n')
        cells.append({'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [],
                      'source': [ln + '\n' for ln in lines[:-1]] + [lines[-1]]})
    for i, c in enumerate(cells):
        c['id'] = f'cell-{i:02d}'
    return json.dumps({'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                                                    'language_info': {'name': 'python'}},
                       'nbformat': 4, 'nbformat_minor': 5}, ensure_ascii=False, indent=1) + '\n'


NOTEBOOK = notebook(PROGRAM)

TABLE = [  # (範例, 閘數（頁面規則）, 理想, 頁面規則 ×1 跑掉, 頁面規則 ×4 跑掉)
    ('1 疊加', '1', '0、1 各 50%', '0.0%', '0.0%'),
    ('2 干涉', '3', '1：100%', '4.4%', '16.4%'),
    ('3 Bell 態', '2', '00、11 各 50%', '6.7%', '23.4%'),
    ('4 GHZ 態', '3', '000、111 各 50%', '10.7%', '36.7%'),
    ('5 隱形傳態', '7', '0：75%、1：25%', '3.1%', '10.7%'),
    ('6 Deutsch', '5', '1：100%', '5.3%', '19.0%'),
    ('7 BV', '10', '101：100%', '16.3%', '50.5%'),
    ('8 Grover', '12', '11：100%', '13.8%', '42.9%'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q126：加入雜訊——八個範例在真實世界會怎樣（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的第十四課。
到 Q125 為止，八個範例都跑在完美的模擬器上；今天故意把錯誤放進去（好玩機制「故障注入」），看答案還認不認得出來、哪個範例最先撐不住。
作品是「理想 vs 雜訊比較圖」：同一條線路，理想與有雜訊的直方圖並排。

## 雜訊模型的三個旋鈕（noise_lab.py 的假設值）

| 旋鈕 | 程式裡的名字 | 假設值 | 意思 |
|---|---|---|---|
| 單位元閘錯誤 | `P1` | 1% | h、x、z、ry 做完後，有 1% 的機會狀態被整個打亂（去極化） |
| 雙位元閘錯誤 | `P2` | 2% | cx、cz 做完後，兩顆位元一起有 2% 的機會被打亂 |
| 讀取錯誤 | `PR` | 3% | 每顆位元有 3% 的機會讀錯（0、1 對調） |

- **這些數字是假設，不代表任何一台真實的機器**。比較圖上一定要寫清楚參數和量了幾次（課綱的常見誤解）。
- 雙位元閘設得比單位元閘大，是因為真實硬體通常如此（維基百科 NISQ：單位元閘保真度約 99–99.5%、雙位元閘約 95–99%）。
- `MY_SCALE` 把三個數字一起乘上去：2 就是雜訊加倍。

## 頁面的雜訊規則（operation.html#circuit 的「加入雜訊（每閘 1%、讀取 3%）」）

頁面用更簡單的規則：線路有 G 個閘，每次有 1 − 0.99^G 的機會整個結果變成完全隨機；再每顆位元 3% 讀錯。page_noise.py 把這個規則的期望值算出來（沒有亂數）：

| 範例 | 閘數 | 理想 | 跑掉的比例（×1） | 跑掉的比例（×4） |
|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in TABLE) + '''
「跑掉的比例」＝把有雜訊的直方圖搬回理想的樣子，最少要搬走幾成（兩份分布差的一半）。

## 今天的重點

- 錯誤預算（QC_Operation_Talk.pptx 第 47 頁）：整條線路做對 ≈ 每個閘都沒錯的機會連乘 × 每顆都讀對的機會；雙位元閘 0.3% → 約 230 個閘後剩一半（0.997^230 ≈ 0.50）。
- 閘越多越吃虧：Grover（12 個閘）、BV 跑掉最多；Bell（2 個閘）最少。
- 錯誤的樣子是「指紋」：讀錯一顆最常見，所以 Grover 的錯誤結果裡 01、10 比 00 多；頁面的閘錯誤則把整個結果打亂。
- 有些雜訊看不出來：疊加本來就一半一半，被打亂還是一半一半；隱形傳態的 75% 會往 50% 靠攏。
- 雜訊加倍有用處：零雜訊外插（第 48 頁）故意放大雜訊，再往回推到「沒有雜訊」。

## 影片的念法

Bell 念「貝爾態」、GHZ 念「範例四」或「三顆位元糾纏」、Grover「格羅弗」、BV「密碼範例」；q0、q1 念「編號零」「編號一」。旁白不念隨機出來的次數。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；孩子預測「哪個範例最先撐不住」 | 影片、列印包第 2 頁 |
| 10–25 | 對照簡報 QC_Operation_Talk.pptx 第 47 頁（錯誤預算）、第 48 頁（錯誤緩解）；三個旋鈕 | 簡報、列印包第 2 頁 |
| 25–65 | operation.html#circuit 的範例四、格羅弗各開關雜訊一次；執行 noise_lab.py，畫理想 vs 雜訊比較圖 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子把 MY_SCALE 改成 2、4、8，填雜訊加倍紀錄表，找出最先跑掉一半的範例 | 列印包第 3 頁、`03_雜訊加倍紀錄.csv` |
| 105–115 | 孩子教爸爸：三個旋鈕、為什麼閘越多越吃虧、哪裡容易錯 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 安裝：`pip install qiskit qiskit-aer`（不需要帳號），先跑一次 `python noise_lab.py`（約數秒）；或用 Jupyter／VS Code 開 `雜訊模型.ipynb` 一格一格跑。
- 沒辦法裝 Qiskit：用 `python page_noise.py`（只要 Python 3）和瀏覽器開 `animations/operation.html#circuit` 一樣能完成比較與加倍。
- 下載學程的 `animations/` 資料夾；選用：`transmon-3d.html#bv` 第 8 步「自由實驗」的「讀取雜訊」勾選框。
- 打開簡報 `slides/QC_Operation_Talk.pptx` 第 47、48 頁（課綱寫 p47–48，頁碼無誤）。
- 列印 `02_列印包_比較圖.pdf`（A4，共 4 頁），準備灰色和一支彩色筆。

## 誠實說明

- 雜訊模型是教學用的假設；真實硬體還有相干誤差、串擾、洩漏、讀取期間 T₁ 衰減等，本課沒有模擬。
- 頁面規則（出錯就整個變隨機）和 qiskit-aer 的逐閘去極化不同，數字接近但不相等。
- noise_lab.py 用固定亂數種子 126，教材印出的比例固定；拿掉種子，每次都會差一點（一萬次約 ±0.5 個百分點）。疊加的「跑掉 0.5%」只是抽樣起伏。
- 零雜訊外插只示範最簡單的直線版；外插有偏差、需要的次數也更多（第 48 頁）。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場一：在動畫裡開關雜訊（約 10 分鐘）

1. 用瀏覽器開 `animations/operation.html#circuit`（場景 6「量子線路：一步一步執行」）。
2. 按「GHZ 態（3 位元糾纏）」，連按 4 次「單步 ▶」走到量測欄。右下插圖「量測 1000 shots 的結果（青線 = 理想機率）」只有 000、111。
3. 按「加入雜訊（每閘 1%、讀取 3%）」：頁面立刻重抽 1000 次。記下：兩根主柱子和青線差多少？哪些結果冒出來？
4. 換「Grover 搜尋（2 位元，找 |11⟩）」（雜訊開關會保持打開），連按 8 次單步，看 11 和青線差多少；再關掉、打開開關重抽一次。
5. 選用：`transmon-3d.html#bv` 第 8 步「自由實驗」，選密碼 101、勾「讀取雜訊」、按「一鍵執行」，再按「④ 量測 50 次」。錯誤結果和 101 差幾個位元？

## 上半場二：理想 vs 雜訊比較圖（約 30 分鐘）

1. 執行 `python noise_lab.py`（或在 Jupyter 開 `雜訊模型.ipynb`）。第一段印出貝爾態、範例四（GHZ）、格羅弗的「理想」與「雜訊」兩排柱子。
2. 在列印包第 1 頁，每個結果畫兩根柱子：理想塗灰色、雜訊塗彩色。
3. 圖的角落寫上：單位元閘 1%、雙位元閘 2%、讀取 3%、每種 1000 次、種子 126。
4. 抄下每張圖最後一行「跑掉的比例」，排出三個範例誰受傷最多。

## 下半場：把雜訊加倍（約 30 分鐘）

1. 先在列印包第 3 頁預測：雜訊 ×1、×2、×4、×8 時，哪個範例最先「跑掉一半」？提示：數一數閘。
2. 看 `noise_lab.py` 第二段的表（每格 10000 次），把八個範例的跑掉比例抄進紀錄表。
3. 改上面的改造區 `MY_SCALE = 2` 成 4、8，看第四段 Grover 的比較圖怎麼變。
4. 沒有 Qiskit：改 `page_noise.py` 的 `MY_SCALE`，看頁面規則的期望值。
5. 延伸：第五段把 ×1、×2 的結果直線往回推到 ×0（零雜訊外插，簡報第 48 頁），和理想的 100% 差多少？

## 小提醒

- 位元字串最右邊是 q0（和頁面、Qiskit 相同）。
- 一千次本來就有約 ±1.6 個百分點的統計起伏（第 32 頁）；雜訊造成的差距要比這大，而且總是偏向同一邊。
''',

'noise_lab.py': PROGRAM,
'雜訊模型.ipynb': NOTEBOOK,
'page_noise.py': PURE_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## page_noise.py 實跑輸出（Python 3.13.18，沒有亂數）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## noise_lab.py 實跑輸出（qiskit 2.6.2、qiskit-aer 0.18.4；AerSimulator seed_simulator=126；換種子比例會差一點）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- 三個旋鈕？單位元閘錯誤（P1）、雙位元閘錯誤（P2）、讀取錯誤（PR）。今天的值 1%、2%、3% 是假設。\n'
  '- 為什麼閘越多答案掉得越多？每個閘都要做對，做對的機會連乘起來（第 47 頁錯誤預算）。Grover 12 個閘，頁面規則下每次約 11.4% 整個變隨機；GHZ 只有 3 個閘，約 3.0%。\n'
  '- 為什麼 Grover 的錯誤結果 01、10 比 00 多？讀錯一顆最常見：11 錯一顆變 01 或 10，要兩顆都錯才變 00。\n'
  '- 哪個範例最先跑掉一半？Qiskit 模型 ×8 時 BV（68.8%）、Grover（61.8%）、GHZ（59.6%）都超過一半，×4 時 BV 最多（45.1%）；頁面規則 ×4 時 BV 就到 50.5%。閘最多的 BV、Grover 最先撐不住。\n'
  '- 為什麼疊加看不出雜訊？被打亂的狀態量起來是一半一半，本來就一半一半，所以看不出差別（表上的 0.5% 是抽樣起伏）。\n'
  '- 隱形傳態呢？0 的比例從 75% 往 50% 靠（×1 約 70.8%、×8 約 55.5%）：雜訊也會把機率往平均推。\n'
  '- 零雜訊外插：2 × 0.863 − 0.756 = 0.970，比 ×1 的 86.3% 更接近 100%，但仍有偏差。\n'
  '- 下一課 Q127「專題：設計自己的線路」：用學過的閘設計一條能說明一個概念的線路；可以順便加雜訊，看它在真實世界撐不撐得住。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#circuit`（場景 6：量子線路：一步一步執行）

- 範例按鈕：Bell 態、GHZ 態（3 位元糾纏）、干涉、Deutsch–Jozsa、Bernstein–Vazirani（秘密字串 101）、Grover 搜尋（2 位元，找 |11⟩）、量子隱形傳態、QFT。
- 「⏮ 重設」「單步 ▶」「播放」；走到最後的量測欄會抽 1000 次，右下插圖是直方圖，青線是理想機率。
- 開關「加入雜訊（每閘 1%、讀取 3%）」：每次有 1 − 0.99^閘數 的機會整個結果變隨機，再每顆位元 3% 讀錯；切換時立刻重抽。

## `animations/transmon-3d.html#bv`（第 9 章：BV 密碼）

- 第 8 步「自由實驗」：密碼按鈕、①–④、「一鍵執行」（量 50 次）、「④ 量測 50 次」（再累加）、勾選框「讀取雜訊」（每顆位元 3% 讀錯，閘不出錯）。
- 右側「量測結果（N 次）」列出 000～111 的次數。

## `animations/basic-circuits.html#ghz`（範例 4）

- 重點卡：「硬體廠常用它來測試多位元糾纏的品質：雜訊越大，量到全 0、全 1 以外結果的比例就越高（這裡是理想模擬，所以不會出現）。」
''',
}

SHEET_HEADER = ['範例', '閘數（單／雙）', '我的預測', '×1 跑掉', '×2 跑掉', '×4 跑掉', '×8 跑掉', '×8 時最高的結果', '備註']
SHEET_ROWS = [['範例：noise_lab.py 8 Grover', '10 / 2', '最先撐不住', '13.7%', '24.4%', '41.6%', '61.8%', '11（仍是答案）', '種子 126、每格 10000 次'],
              ['1 疊加', '1 / 0', '', '', '', '', '', '', ''], ['2 干涉', '3 / 0', '', '', '', '', '', '', ''],
              ['3 Bell 態', '1 / 1', '', '', '', '', '', '', ''], ['4 GHZ 態', '1 / 2', '', '', '', '', '', '', ''],
              ['5 隱形傳態', '3 / 4', '', '', '', '', '', '', ''], ['6 Deutsch', '4 / 1', '', '', '', '', '', '', ''],
              ['7 BV', '8 / 2', '', '', '', '', '', '', ''], ['8 Grover', '10 / 2', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:9mm;font-size:10.5pt}table.judge td.k{font-weight:bold;color:#0b2540;width:16%}
table.judge th{font-size:10pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}
.chart{border:1pt solid #9fb3c8;height:46mm;margin:1.5mm 0 8mm;position:relative;background:repeating-linear-gradient(to top,#fff 0,#fff 4.4mm,#e6edf4 4.4mm,#e6edf4 4.6mm)}
.chart span{position:absolute;bottom:-5mm;font-size:9pt;color:#0b2540}.ch{font-weight:bold;color:#0b2540;margin:2mm 0 0}'''


def check_program():
    """真的跑一次 page_noise.py（隔離模式），確認輸出和影片、教材寫的結果一致；再檢查 Qiskit 實跑紀錄與 notebook。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'page_noise.py'
        p.write_text(PURE_PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    assert '4 GHZ 態：3 個閘 → 變成隨機 3.0%；000 44.7%、111 44.7%；跑掉 10.7%' in out
    assert '8 Grover：12 個閘 → 變成隨機 11.4%；11 86.2%；跑掉 13.8%' in out
    assert '1 疊加：1 個閘 → 變成隨機 1.0%；0 50.0%、1 50.0%；跑掉 0.0%' in out
    rows = dict(re.findall(r'^  (\d .+?)\s{2,}(\d.+)$', out.split('二、')[1].split('三、')[0], re.M))
    assert [r[0] for r in TABLE] == list(rows) and all(rows[r[0]].split()[0] == r[3] and rows[r[0]].split()[2] == r[4] for r in TABLE), rows
    for needle in ('跑掉的比例 6.1%', '跑掉的比例 10.2%', '跑掉的比例 12.7%', '5 隱形傳態：理想 0 是 75.0%；雜訊 ×1 是 70.8%；×8 是 55.5%',
                   '直線往回推到 ×0：2 × 0.863 − 0.756 = 97.0%', '1 疊加：理想 0 是 50.0%'):
        assert needle in QISKIT_OUTPUT, needle
    nb = json.loads(NOTEBOOK)
    code = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
    assert nb['nbformat'] == 4 and code.count('def ') == PROGRAM.count('def ') and 'MY_SCALE' in code
    compile(code, '雜訊模型.ipynb', 'exec')
    compile(PROGRAM, 'noise_lab.py', 'exec')
    return out


def _chart(title, labels):
    w = 100 / len(labels)
    spans = ''.join(f'<span style="left:{i * w + w / 2 - 3:.1f}%">{k}</span>' for i, k in enumerate(labels))
    return f'<p class="ch">{title}</p><div class="chart">{spans}</div>'


def html():
    names = [r[0] for r in TABLE]
    rows = ''.join(f'<tr><td class="k">{n}</td><td></td><td></td><td></td><td></td><td></td></tr>' for n in names)
    pages = [
        '<h2>理想 vs 雜訊比較圖</h2><p class="lead">每個結果畫兩根柱子：理想塗灰色、雜訊塗彩色（一格 10%）。資料：noise_lab.py 第一段。</p>'
        + _chart('貝爾態（Bell）', ['00', '01', '10', '11'])
        + _chart('範例四（GHZ）', ['000', '001', '010', '011', '100', '101', '110', '111'])
        + _chart('格羅弗（Grover）', ['00', '01', '10', '11'])
        + '<p style="margin-top:6mm">參數：單位元閘＿＿％、雙位元閘＿＿％、讀取＿＿％；每種＿＿＿次；種子＿＿＿</p>'
        '<p>跑掉的比例：貝爾態＿＿＿　範例四＿＿＿　格羅弗＿＿＿</p>',
        '<h2>三個旋鈕與錯誤預算</h2><p class="lead">整條線路做對 ≈ 每個閘都沒錯的機會連乘 × 每顆都讀對的機會（簡報第 47 頁）</p>'
        '<table class="judge"><tr><th style="width:22%">旋鈕</th><th>程式名字</th><th>假設值</th><th>白話意思</th></tr>'
        '<tr><td class="k">單位元閘</td><td>P1</td><td>1%</td><td></td></tr>'
        '<tr><td class="k">雙位元閘</td><td>P2</td><td>2%</td><td></td></tr>'
        '<tr><td class="k">讀取</td><td>PR</td><td>3%</td><td></td></tr></table>'
        '<p>頁面規則：G 個閘，每次整個變隨機的機會 = 1 − 0.99<sup>G</sup>。用計算機算：</p>'
        '<table class="judge"><tr><th style="width:22%">範例</th><th>閘數 G</th><th>0.99<sup>G</sup></th><th>1 − 0.99<sup>G</sup></th></tr>'
        '<tr><td class="k">貝爾態</td><td>2</td><td></td><td></td></tr><tr><td class="k">範例四</td><td>3</td><td></td><td></td></tr>'
        '<tr><td class="k">格羅弗</td><td>12</td><td></td><td></td></tr></table>'
        '<p>簡報的例子：0.997<sup>230</sup> ≈ ＿＿＿（雙位元閘錯誤 0.3%，約 230 個閘後剩一半）</p>'
        '<p>我的預測：哪個範例最先撐不住？為什麼？</p><div class="line"></div>',
        '<h2>換你改造：把雜訊加倍</h2><p class="lead">跑掉的比例：把有雜訊的直方圖搬回理想，最少要搬走幾成。超過 50% 就圈起來。</p>'
        '<table class="judge"><tr><th>範例</th><th>×1</th><th>×2</th><th>×4</th><th>×8</th><th>最高的還是答案嗎</th></tr>'
        + rows + '</table>'
        '<pre class="code"># noise_lab.py 上面的改造區\n'
        'MY_SCALE = 2        # 改成 4、8：三個旋鈕一起乘上去\n'
        '# 延伸：2 × (×1 的答案比例) − (×2 的答案比例) ≈ 沒有雜訊時的答案比例（零雜訊外插）</pre>'
        '<p>最先跑掉一半的是＿＿＿＿；怎麼加都看不出來的是＿＿＿＿，因為＿＿＿＿＿＿＿＿</p>',
        '<h2>最後一關：故障報告</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 雜訊模型的三個旋鈕（不看稿）：</p><div class="line"></div>'
        '<p>2. 為什麼閘越多的範例，答案掉得越多：</p><div class="line"></div>'
        '<p>3. 一個注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出三個旋鈕：單位元閘、雙位元閘、讀取</li><li>完成比較圖，角落寫上參數和次數</li>'
        '<li>說出：閘越多，每個都做對的機會連乘起來越小</li><li>雜訊加倍紀錄表八個範例都填完，圈出最先跑掉一半的</li>'
        '<li>指出：雜訊模型是假設，參數要寫清楚</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q126 理想 vs 雜訊比較圖 列印包', '父子科技學院 量子電腦學程 Q126｜加入雜訊：八個範例在真實世界會怎樣', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q126-noisy-examples', folder='Q126_加入雜訊', files=FILES,
        sheet=('03_雜訊加倍紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_比較圖.pdf', pack_pages=4,
        pack_needles=('理想 vs 雜訊比較圖', '三個旋鈕與錯誤預算', '把雜訊加倍', 'MY_SCALE', '最後一關'),
        authoring_dir=XINEW / 'authoring/q126', episode_dir='specials/q126-noisy-examples',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'yes（Python 3 與 pip install qiskit qiskit-aer；page_noise.py 只需 Python 3；動畫只需瀏覽器）',
               'program': 'noise_lab.py', 'notebook': '雜訊模型.ipynb', 'pureProgram': 'page_noise.py',
               'testedWith': 'qiskit 2.6.2, qiskit-aer 0.18.4, Python 3.13.18 (AerSimulator seed_simulator=126); page_noise.py standard library only, no randomness',
               'noiseModel': {'P1_singleQubitDepolarizing': 0.01, 'P2_twoQubitDepolarizing': 0.02, 'PR_readoutFlip': 0.03, 'assumption': True},
               'recordedRun': {'pageRule': {'ghz': {'gates': 3, 'randomized': 0.030, 'off': 0.107}, 'grover': {'gates': 12, 'randomized': 0.114, 'p11': 0.862, 'off': 0.138},
                                            'offAtX4': {r[0]: r[4] for r in TABLE}},
                               'qiskitOffX1': {'bell': 0.061, 'ghz': 0.102, 'grover': 0.127},
                               'teleportP0': {'ideal': 0.75, 'x1': 0.708, 'x8': 0.555},
                               'zne': {'x1': 0.863, 'x2': 0.756, 'extrapolated': 0.970}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q126/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

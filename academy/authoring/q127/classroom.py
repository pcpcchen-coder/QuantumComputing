"""Q127 課堂教材：專題模板（目標、線路、預測、驗證）、工具箱與兩個範例、故意出錯紀錄、最後一關檢核表；專題模板 notebook（專題模板.ipynb 與同內容的 my_circuit.py）、
純 Python 的迷你模擬器 tiny_sim.py、解答與動畫導覽。

my_circuit.py 需要 Python 3 與 pip install qiskit qiskit-aer（不需要帳號）；tiny_sim.py 只要 Python 3（沒有亂數，逐步算出狀態向量）。
建置時會真的執行一次 tiny_sim.py，確認輸出和影片、教材寫的結果一致；Qiskit 部分（portable-runtime 沒有 Qiskit）比對製作代理已記錄的實跑輸出，
並檢查專題模板.ipynb 是合法的 notebook JSON、程式格內容與 my_circuit.py 相同。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \\
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q127/classroom.py
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
RUN_OUTPUT = '''【範例甲：H、四個 T、H】
  h 0      → 0.71|0⟩ + 0.71|1⟩
  t 0      → 0.71|0⟩ + 0.50+0.50i|1⟩
  t 0      → 0.71|0⟩ + 0.71i|1⟩
  t 0      → 0.71|0⟩ + −0.50+0.50i|1⟩
  t 0      → 0.71|0⟩ + −0.71|1⟩
  h 0      → 1.00|1⟩
  理想機率：1 100.0%
  判定：預測正確
【範例乙：H H、CZ、H】
  h 0      → 0.71|00⟩ + 0.71|01⟩
  h 1      → 0.50|00⟩ + 0.50|01⟩ + 0.50|10⟩ + 0.50|11⟩
  cz 1 0   → 0.50|00⟩ + 0.50|01⟩ + 0.50|10⟩ + −0.50|11⟩
  h 0      → 0.71|00⟩ + 0.71|11⟩
  理想機率：00 50.0%、11 50.0%
  判定：預測正確
【故意出錯甲：只放三個 T】
  h 0      → 0.71|0⟩ + 0.71|1⟩
  t 0      → 0.71|0⟩ + 0.50+0.50i|1⟩
  t 0      → 0.71|0⟩ + 0.71i|1⟩
  t 0      → 0.71|0⟩ + −0.50+0.50i|1⟩
  h 0      → 0.15+0.35i|0⟩ + 0.85−0.35i|1⟩
  理想機率：0 14.6%、1 85.4%
  判定：預測不對（最多差 14.6%）
【故意出錯乙：忘了最後的 H】
  h 0      → 0.71|00⟩ + 0.71|01⟩
  h 1      → 0.50|00⟩ + 0.50|01⟩ + 0.50|10⟩ + 0.50|11⟩
  cz 1 0   → 0.50|00⟩ + 0.50|01⟩ + 0.50|10⟩ + −0.50|11⟩
  理想機率：00 25.0%、01 25.0%、10 25.0%、11 25.0%
  判定：預測不對（最多差 25.0%）
【我的專題】
  h 0      → 0.71|0⟩ + 0.71|1⟩
  s 0      → 0.71|0⟩ + 0.71i|1⟩
  s 0      → 0.71|0⟩ + −0.71|1⟩
  h 0      → 1.00|1⟩
  理想機率：1 100.0%
  判定：預測正確
'''

# 製作代理實跑紀錄：qiskit 2.6.2、qiskit-aer 0.18.4（Python 3.13.18），AerSimulator seed_simulator=127（每行行尾空白已去掉）
QISKIT_OUTPUT = '''【範例甲：四個 T ＝ 一個 Z】目標：四個八分之一圈相位閘等於一個相位翻轉閘
     ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌─┐
  q: ┤ H ├┤ T ├┤ T ├┤ T ├┤ T ├┤ H ├┤M├
     └───┘└───┘└───┘└───┘└───┘└───┘└╥┘
c: 1/═══════════════════════════════╩═
                                    0
    結果    預測     理想   抽樣 1000 次
        1  100.0%   100.0%    100.0%
    判定：預測正確

【範例乙：用 CZ 做 Bell 態】目標：不用 CNOT 也能做出 Bell 態
     ┌───┐   ┌───┐┌─┐
q_0: ┤ H ├─■─┤ H ├┤M├
     ├───┤ │ └┬─┬┘└╥┘
q_1: ┤ H ├─■──┤M├──╫─
     └───┘    └╥┘  ║
c: 2/══════════╩═══╩═
               1   0
    結果    預測     理想   抽樣 1000 次
       00   50.0%    50.0%     48.3%
       11   50.0%    50.0%     51.7%
    判定：預測正確

【故意出錯甲：只放三個 T】目標：（同範例甲，預測照抄）
     ┌───┐┌───┐┌───┐┌───┐┌───┐┌─┐
  q: ┤ H ├┤ T ├┤ T ├┤ T ├┤ H ├┤M├
     └───┘└───┘└───┘└───┘└───┘└╥┘
c: 1/══════════════════════════╩═
                               0
    結果    預測     理想   抽樣 1000 次
        0    0.0%    14.6%     11.5%
        1  100.0%    85.4%     88.5%
    判定：預測不對（最多差 14.6%）

【故意出錯乙：忘了最後的 H】目標：（同範例乙，預測照抄）
     ┌───┐   ┌─┐
q_0: ┤ H ├─■─┤M├───
     ├───┤ │ └╥┘┌─┐
q_1: ┤ H ├─■──╫─┤M├
     └───┘    ║ └╥┘
c: 2/═════════╩══╩═
              0  1
    結果    預測     理想   抽樣 1000 次
       00   50.0%    25.0%     21.9%
       01    0.0%    25.0%     24.4%
       10    0.0%    25.0%     26.4%
       11   50.0%    25.0%     27.3%
    判定：預測不對（最多差 25.0%）

【我的專題】目標：三顆位元都做 H，八種結果機率一樣
     ┌───┐┌─┐
q_0: ┤ H ├┤M├──────
     ├───┤└╥┘┌─┐
q_1: ┤ H ├─╫─┤M├───
     ├───┤ ║ └╥┘┌─┐
q_2: ┤ H ├─╫──╫─┤M├
     └───┘ ║  ║ └╥┘
c: 3/══════╩══╩══╩═
           0  1  2
    結果    預測     理想   抽樣 1000 次
      000   12.5%    12.5%     10.1%
      001   12.5%    12.5%     12.0%
      010   12.5%    12.5%     12.8%
      011   12.5%    12.5%     12.9%
      100   12.5%    12.5%     11.3%
      101   12.5%    12.5%     14.7%
      110   12.5%    12.5%     12.3%
      111   12.5%    12.5%     13.9%
    判定：預測正確

'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q127：專題模板——設計自己的線路（專題模板 notebook 的程式版）

安裝（只要一次）：  pip install qiskit qiskit-aer
執行：              python my_circuit.py
專題四步：一、寫目標　二、畫線路　三、寫預測（先寫再跑，寫好就不改）　四、用模擬器驗證
每個專題印出一份驗證報告：線路圖、預測、理想機率（Statevector）、抽樣 1000 次（AerSimulator），最後判定預測對不對。
位元字串的最右邊是 q0。固定亂數種子，所以每次執行結果相同；拿掉 seed_simulator 就每次不同。
"""
# %% 匯入
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

SHOTS = 1000
SEED = 127
TOLERANCE = 0.01   # 預測和理想機率最多差 1 個百分點，就算「預測正確」


# %% 範例甲：四個 T（八分之一圈）＝ 一個 Z（相位翻轉）
def example_a(n_t=4):
    """H、n_t 個 T、H。目標：四個 T 等於一個 Z，所以這條線路等於 H-Z-H，一定得到 1。"""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    for _ in range(n_t):
        qc.t(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


# %% 範例乙：不用 CNOT，用 CZ 做出 Bell 態
def example_b(last_h=True):
    """兩顆都 H、CZ、q0 再一個 H。目標：H-CZ-H 等於 CNOT（簡報第 22 頁），所以得到 Bell 態。"""
    qc = QuantumCircuit(2, 2)
    qc.h([0, 1])
    qc.cz(1, 0)
    if last_h:
        qc.h(0)
    qc.measure([0, 1], [0, 1])
    return qc


# %% 我的專題：改這一格（目標、線路、預測都換成自己的）
MY_GOAL = '三顆位元都做 H，八種結果機率一樣'


def my_circuit():
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc


MY_PREDICT = {format(k, '03b'): 1 / 8 for k in range(8)}   # 先寫預測，再執行！

PROJECTS = [
    ('範例甲：四個 T ＝ 一個 Z', '四個八分之一圈相位閘等於一個相位翻轉閘', example_a, {'1': 1.0}),
    ('範例乙：用 CZ 做 Bell 態', '不用 CNOT 也能做出 Bell 態', example_b, {'00': 0.5, '11': 0.5}),
    ('故意出錯甲：只放三個 T', '（同範例甲，預測照抄）', lambda: example_a(3), {'1': 1.0}),
    ('故意出錯乙：忘了最後的 H', '（同範例乙，預測照抄）', lambda: example_b(False), {'00': 0.5, '11': 0.5}),
    ('我的專題', MY_GOAL, my_circuit, MY_PREDICT),
]


# %% 驗證報告
def ideal(qc):
    """理想機率（Statevector，不抽樣）"""
    sv = Statevector(qc.remove_final_measurements(inplace=False))
    return {k: v for k, v in sv.probabilities_dict().items() if v > 1e-9}


def sample(qc):
    """模擬器抽樣 SHOTS 次，回傳每個結果的比例"""
    counts = AerSimulator(seed_simulator=SEED).run(qc, shots=SHOTS).result().get_counts()
    return {k: v / SHOTS for k, v in counts.items()}


def report(name, goal, make, predict):
    qc = make()
    p, s = ideal(qc), sample(qc)
    keys = sorted(set(p) | set(s) | set(predict))
    print(f'【{name}】目標：{goal}')
    print(qc.draw(output='text', idle_wires=False))
    print('    結果    預測     理想   抽樣 1000 次')
    for k in keys:
        print(f'    {k:>5} {predict.get(k, 0):7.1%} {p.get(k, 0):8.1%} {s.get(k, 0):9.1%}')
    worst = max(abs(predict.get(k, 0) - p.get(k, 0)) for k in keys)
    print('    判定：' + ('預測正確' if worst <= TOLERANCE else f'預測不對（最多差 {worst:.1%}）'))
    print()


for project in PROJECTS:
    report(*project)
'''

PURE_PROGRAM = '''"""父子科技學院 量子電腦學程 Q127：迷你模擬器（純 Python，不需要安裝任何套件，也沒有亂數）

執行：  python tiny_sim.py
沒辦法裝 Qiskit 時用這個：它把狀態向量（2ⁿ 個振幅）一步一步算出來，印出每一步的振幅和最後的理想機率。
會的閘：h、x、z、s、t（單位元閘），cx、cz（雙位元閘）。位元字串最右邊是 q0（和 Qiskit、動畫相同）。
改最下面 MY_STEPS 和 MY_PREDICT，就能驗證自己的線路。
"""
import cmath
import math

R = 1 / math.sqrt(2)
ONE = {'h': ((R, R), (R, -R)), 'x': ((0, 1), (1, 0)), 'z': ((1, 0), (0, -1)),
       's': ((1, 0), (0, 1j)), 't': ((1, 0), (0, cmath.exp(1j * math.pi / 4)))}


def run(n, steps):
    """steps：[('h', 0), ('t', 0), ('cz', 1, 0), ...]；回傳每一步之後的狀態向量"""
    amp = [0j] * 2 ** n
    amp[0] = 1
    history = []
    for gate, *qs in steps:
        new = amp[:]
        if gate in ONE:
            (a, b), (c, d) = ONE[gate]
            q = qs[0]
            for i in range(2 ** n):
                if not i >> q & 1:
                    j = i | 1 << q
                    new[i] = a * amp[i] + b * amp[j]
                    new[j] = c * amp[i] + d * amp[j]
        elif gate == 'cx':
            c, t = qs
            for i in range(2 ** n):
                if i >> c & 1:
                    new[i] = amp[i ^ 1 << t]
        elif gate == 'cz':
            c, t = qs
            for i in range(2 ** n):
                if i >> c & 1 and i >> t & 1:
                    new[i] = -amp[i]
        amp = new
        history.append(((gate, *qs), amp))
    return history


def fmt(z):
    """振幅寫成 0.71、−0.50+0.50i 這種樣子（同動畫的讀數）"""
    re, im = round(z.real, 2) + 0.0, round(z.imag, 2) + 0.0
    if im == 0:
        return f'{re:.2f}'.replace('-', '−')
    if re == 0:
        return f'{im:.2f}i'.replace('-', '−')
    return f'{re:.2f}{im:+.2f}i'.replace('-', '−')


def report(name, n, steps, predict):
    print(f'【{name}】')
    for (op, amp) in run(n, steps):
        terms = [f'{fmt(a)}|{k:0{n}b}⟩' for k, a in enumerate(amp) if abs(a) > 1e-9]
        print(f'  {" ".join(map(str, op)):<8} → ' + ' + '.join(terms))
    prob = {f'{k:0{n}b}': abs(a) ** 2 for k, a in enumerate(amp) if abs(a) ** 2 > 1e-9}
    keys = sorted(set(prob) | set(predict))
    print('  理想機率：' + '、'.join(f'{k} {prob.get(k, 0):.1%}' for k in keys))
    worst = max(abs(predict.get(k, 0) - prob.get(k, 0)) for k in keys)
    print('  判定：' + ('預測正確' if worst <= 0.01 else f'預測不對（最多差 {worst:.1%}）'))


A = [('h', 0), ('t', 0), ('t', 0), ('t', 0), ('t', 0), ('h', 0)]
B = [('h', 0), ('h', 1), ('cz', 1, 0), ('h', 0)]
MY_STEPS = [('h', 0), ('s', 0), ('s', 0), ('h', 0)]      # 改這裡：自己的線路（例：兩個 S 是不是等於 Z？）
MY_PREDICT = {'1': 1.0}                                  # 先寫預測，再執行！

if __name__ == '__main__':
    report('範例甲：H、四個 T、H', 1, A, {'1': 1.0})
    report('範例乙：H H、CZ、H', 2, B, {'00': 0.5, '11': 0.5})
    report('故意出錯甲：只放三個 T', 1, A[:3] + A[4:], {'1': 1.0})
    report('故意出錯乙：忘了最後的 H', 2, B[:3], {'00': 0.5, '11': 0.5})
    report('我的專題', 1, MY_STEPS, MY_PREDICT)
'''


def notebook(src):
    """把 my_circuit.py 依「# %%」切成格：開頭說明變成文字格，每一段前面加一格標題文字（同 Q124、Q126）。"""
    _, doc, body = src.split('"""', 2)
    body = body.lstrip('\n')
    cells = [{'cell_type': 'markdown', 'metadata': {}, 'source': ['# 專題模板 notebook（Q127）\n', '\n'] + [ln + '\n' for ln in doc.splitlines()]}]
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

TABLE = [  # (專題, 線路, 預測, 理想, 判定)
    ('範例甲', 'H、T、T、T、T、H', '1：100%', '1：100%', '預測正確'),
    ('範例乙', 'H H、CZ、q0 再 H', '00、11 各 50%', '00、11 各 50%', '預測正確'),
    ('故意出錯甲', 'H、T、T、T、H（少一個 T）', '1：100%（照抄）', '0：14.6%、1：85.4%', '預測不對（差 14.6%）'),
    ('故意出錯乙', 'H H、CZ（忘了最後的 H）', '00、11 各 50%（照抄）', '四種各 25%', '預測不對（差 25.0%）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q127：專題——設計自己的線路（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的第十五課。
Q113–Q126 跑過八個範例、量過次數、加過雜訊；今天換孩子當設計師（好玩機制「Maker 挑戰」）：用學過的閘設計一條能說明一個概念的線路，並在模擬器驗證。
作品是「自己的線路與驗證報告」：線路圖、預測表、模擬結果，再加一個故意出錯的版本與差別說明。

## 專題四步（課綱的動手任務）

| 步驟 | 要做什麼 | 寫在哪裡 |
|---|---|---|
| 一、目標 | 一句話寫出「我要說明什麼概念」 | 列印包第 1 頁、`MY_GOAL` |
| 二、線路 | 挑閘、畫線路圖（由左到右，q0 在最上面） | 列印包第 1 頁、`my_circuit()` |
| 三、預測 | 每個結果的機率，**先寫再跑，寫好不改**，寫上日期 | 列印包第 1 頁、`MY_PREDICT` |
| 四、驗證 | 執行模擬器：理想機率＋抽樣 1000 次；判定預測對不對 | `my_circuit.py` 印出的驗證報告 |

生活技能「從目標反推設計」：先決定要說明什麼，再決定什麼結果能當證據，最後才挑閘（維基百科 Backward design 的三階段：先定目標、再定證據、最後設計活動）。

## 工具箱（QC_Operation_Talk.pptx 第 18、22 頁）

| 閘 | 影片的念法 | 作用 |
|---|---|---|
| H | 哈達瑪閘 | 產生疊加：0 變成 0、1 各一半 |
| X | 翻轉閘 | 0 ↔ 1 |
| Z | 相位翻轉閘 | 狀態 1 的振幅變號 |
| S | 四分之一圈相位閘 | 繞 z 軸 90°；S² = Z |
| T | 八分之一圈相位閘 | 繞 z 軸 45°；T² = S（所以 T⁴ = Z） |
| CNOT | 受控反閘 | 控制是 1 時翻轉目標 |
| CZ | 受控相位翻轉閘 | 兩個都是 1 時加負號；對稱，不分控制與目標 |

相位閘（Z、S、T）不改變量到 0 或 1 的機率，只改相位（維基百科 Quantum logic gate）；要讓相位「看得見」，前後要夾 H 做干涉。

## 兩個示範專題（影片與 my_circuit.py）

| 專題 | 線路 | 預測 | 理想 | 判定 |
|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in TABLE) + '''
- 範例甲的道理：T⁴ = Z，所以 H、T、T、T、T、H = H、Z、H = X，一定得到 1。
- 範例乙的道理：第 22 頁「CNOT = (I⊗H) · CZ · (I⊗H)」——在目標位元前後各夾一個 H 的 CZ 就是 CNOT（Q111 學過）。先對 q1 做 H，再對 q0「H、CZ、H」，就等於 H＋CNOT 的貝爾態。
- 故意出錯乙：CZ 之後兩顆其實已經糾纏（動畫讀數「有糾纏」），但少了最後的 H，直接量只看到四種各 25%：糾纏還在，只是這樣量不出來。

## 影片的念法

H「哈達瑪閘」、X「翻轉閘」、Z「相位翻轉閘」、S「四分之一圈相位閘」、T「八分之一圈相位閘」、CNOT「受控反閘」、CZ「受控相位翻轉閘」、Bell「貝爾態」；q0、q1 念「編號零」「編號一」。旁白不念隨機抽樣的次數。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；孩子說出今天的作品是什麼 | 影片、列印包第 2 頁 |
| 10–25 | 概念示範：工具箱、範例甲與範例乙（QC_Operation_Talk.pptx 第 18、22 頁） | 簡報、列印包第 2 頁 |
| 25–65 | operation.html#register 用按鈕組範例甲、乙；執行 my_circuit.py；父子一起寫第一個自己的專題（目標、線路、預測、驗證） | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立做「故意出錯」版：先預測、再跑、寫差別說明 | 列印包第 3 頁、`03_驗證報告.csv` |
| 105–115 | 孩子教爸爸：我的概念、我的證據、哪裡容易錯 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔（檔名加版本與日期） | |

## 課前準備（約 15 分鐘，課綱：本機模擬器）

- 安裝：`pip install qiskit qiskit-aer`（不需要帳號），先跑一次 `python my_circuit.py`（約數秒）；或用 Jupyter／VS Code 開 `專題模板.ipynb` 一格一格跑。
- 沒辦法裝 Qiskit：`python tiny_sim.py`（只要 Python 3）會一步一步印出振幅和理想機率，一樣能驗證預測（只是沒有抽樣）。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#register`（場景 4）與 `operation.html#circuit`（場景 6）。
- 打開簡報 `slides/QC_Operation_Talk.pptx` 第 18 頁（單位元閘一覽）、第 22 頁（兩位元閘與 CNOT = H·CZ·H）、第 52 頁（操作檢查表：設計線路、先用模擬器驗證）。課綱沒有指定簡報頁，以上頁碼由製作代理讀出。
- 列印 `02_列印包_驗證報告.pdf`（A4，共 4 頁）。

## 誠實說明

- 兩個範例只在理想模擬器上驗證；真實硬體會有雜訊（Q126），結果會差一點。
- 抽樣 1000 次的比例會在理想值附近起伏（一半一半約 ±1.6 個百分點）；`my_circuit.py` 用固定種子 127，教材印出的數字固定。
- 「判定」只比對預測和理想機率（容許差 1 個百分點），不是統計檢定。
- 常見誤解（課綱）：先寫預測再跑，避免看結果才找理由。看到結果才編出假設、再假裝一開始就這麼想，科學界叫 HARKing（事後假設）。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場一：用動畫的按鈕組線路（約 10 分鐘）

1. 用瀏覽器開 `animations/operation.html#register`（場景 4「多量子位元：2ⁿ 個振幅與糾纏」），位元數維持 2。
2. 範例甲：確認「目標 q0」亮著 → 按「H」→ 連按四次「T」（看 |01⟩ 柱子的顏色一次換一個，高度不變）→ 再按「H」：只剩 |01⟩。
3. 出錯版：按「重設 |0…0⟩」→「H」→ 只按三次「T」→「H」：|00⟩ 還剩一小截。左下讀數寫的振幅和 `tiny_sim.py` 印的一樣。
4. 範例乙：按「均勻疊加 H⊗ⁿ」→「CZ」（|11⟩ 變藍、高度不變；讀數變成「有糾纏」）→「H」（目標 q0）：只剩 |00⟩、|11⟩。按「測量全部」幾次（每次要重做一遍）。
5. 選用：開 `operation.html#circuit`，按「量子隱形傳態」，一路「單步 ▶」：七個閘，最後只量 q2。這是「先定目標（把狀態送到 q2）→ 只量需要的那顆」的設計。

## 上半場二：第一份驗證報告（約 30 分鐘）

1. 執行 `python my_circuit.py`（或在 Jupyter 開 `專題模板.ipynb`）：前四份報告是範例甲、乙與兩個故意出錯版，看懂「預測、理想、抽樣 1000 次、判定」四欄。
2. 父子一起想一個目標（例：「兩個 S 等於一個 Z」「X 夾在兩個 H 中間會變成什麼」「三顆的貝爾態」），在列印包第 1 頁寫目標、畫線路、寫預測與日期。
3. 改 `my_circuit.py` 的「我的專題」那一格：`MY_GOAL`、`my_circuit()`、`MY_PREDICT`，**預測寫好就不改**，再執行。
4. 把印出的驗證報告抄到列印包第 1 頁下半，或填進 `03_驗證報告.csv`。

## 下半場：故意出錯（約 30 分鐘）

1. 在列印包第 3 頁寫：要怎麼出錯（拿掉一個閘、換一個閘、放錯目標位元），以及「出錯版會變成什麼」的預測。
2. 複製一份 `my_circuit()` 改成出錯版，加進 `PROJECTS`，執行並比對兩份報告。
3. 寫一句差別說明：哪一步不一樣、結果怎麼變、為什麼。
4. 沒有 Qiskit：改 `tiny_sim.py` 最下面的 `MY_STEPS`、`MY_PREDICT`。

## 小提醒

- 位元字串最右邊是 q0（和動畫、Qiskit 相同）；動畫的 CZ 與 CNOT 用「目標 + 1」當控制。
- 抽樣一千次本來就會差一兩個百分點；判定看的是理想機率。
''',

'my_circuit.py': PROGRAM,
'專題模板.ipynb': NOTEBOOK,
'tiny_sim.py': PURE_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## tiny_sim.py 實跑輸出（Python 3.13.18，沒有亂數）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## my_circuit.py 實跑輸出（qiskit 2.6.2、qiskit-aer 0.18.4；AerSimulator seed_simulator=127；換種子抽樣比例會差一點）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- 為什麼四個 T 等於 Z？T 是繞 z 軸 45°，四次就是 180°，正好是 Z（T = ⁴√Z）。所以 H、T×4、H = H、Z、H = X，一定得到 1。\n'
  '- 只放三個 T 呢？繞了 135°，|1⟩ 的相位是 e^{i·3π/4}；最後的 H 讓兩條路相加，量到 0 的機率 = (1 + cos 135°) / 2 ≈ 14.6%，1 ≈ 85.4%。\n'
  '- 範例乙為什麼是貝爾態？對 q0 做「H、CZ、H」就是以 q1 為控制、q0 為目標的 CNOT（第 22 頁 CNOT = (I⊗H)·CZ·(I⊗H)）；前面 q1 的 H 讓控制位元在疊加，所以得到 (|00⟩+|11⟩)/√2。q0 一開始的 H 是那個「前面的 H」。\n'
  '- 忘了最後的 H 為什麼是四種各 25%？CZ 只改相位（|11⟩ 變號），不改機率；均勻疊加的四種機率本來就各 25%。但兩顆已經糾纏（動畫讀數 Bloch 長度 0.00、有糾纏），只是直接量看不出來。\n'
  '- 判定「預測不對」是失敗嗎？不是。故意出錯版本來就該被抓出來；重點是預測先寫好，差別說明寫得出原因。\n'
  '- 抽樣 1000 次和理想不一樣？範例乙 00 是 48.3%、11 是 51.7%（種子 127），這是抽樣起伏；換種子會不同。\n'
  '- 下一課 Q128「模組發表：量子電路展」：把今天的線路與驗證報告拿出來，向家人展示並回答三個問題。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#register`（場景 4：多量子位元：2ⁿ 個振幅與糾纏）——自己組線路的「積木台」

- 滑桿「量子位元數 n」（1–4）；「目標 q0」…「目標 q3」選要作用的位元。
- 單位元閘：「H」「X」「Z」「S」「T」；雙位元閘：「CNOT（控制 = 目標+1 → 目標）」「CZ」（同樣用目標+1 當另一顆）。
- 現成按鈕：「均勻疊加 H⊗ⁿ」「Bell 態」「GHZ 態」；量測：「測量全部」「只測 q0」；「重設 |0…0⟩」。
- 柱子高度 = 機率，顏色 = 相位（金 = +，藍 = −，其他顏色是複數相位）；左下讀數有 |ψ⟩、各位元 Bloch 長度、有沒有糾纏。

## `animations/operation.html#circuit`（場景 6：量子線路：一步一步執行）

- 範例按鈕：Bell 態、GHZ 態、干涉、Deutsch–Jozsa、Bernstein–Vazirani、Grover、量子隱形傳態、量子傅立葉轉換。
- 「量子隱形傳態」：Ry、H、CX、CX、H、CX、CZ 七個閘，只量 q2；最後兩個受控閘取代「量完再修正」（延遲量測，簡報第 28 頁）。直方圖只有 0、1，青線 0.25、0.75。
- 「⏮ 重設」「單步 ▶」「播放」；開關「加入雜訊（每閘 1%、讀取 3%）」可看自己的設計在雜訊下撐不撐得住（Q126）。
''',
}

SHEET_HEADER = ['專題', '目標（一句話）', '線路（由左到右）', '預測（先寫）', '預測日期', '理想機率', '抽樣 1000 次', '判定', '差別說明']
SHEET_ROWS = [['範例：範例甲', '四個 T 等於一個 Z', 'H、T、T、T、T、H', '1：100%', '上課前', '1：100%', '1：100%', '預測正確', ''],
              ['範例：故意出錯甲', '（同範例甲）', 'H、T、T、T、H', '1：100%', '上課前', '0：14.6%、1：85.4%', '0：11.5%、1：88.5%（種子 127）', '預測不對',
               '少一個 T 只轉 135°，干涉沒有完全抵消'],
              ['我的專題', '', '', '', '', '', '', '', ''], ['我的故意出錯版', '', '', '', '', '', '', '', ''],
              ['我的第二個專題（選做）', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:9mm;font-size:10.5pt}table.judge td.k{font-weight:bold;color:#0b2540;width:18%}
table.judge th{font-size:10pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}
.grid{border:1pt solid #9fb3c8;height:70mm;margin:1.5mm 0 3mm;background:repeating-linear-gradient(to bottom,#fff 0,#fff 9.6mm,#9fb3c8 9.6mm,#9fb3c8 10mm)}
.ch{font-weight:bold;color:#0b2540;margin:2mm 0 0}'''


def check_program():
    """真的跑一次 tiny_sim.py（隔離模式），確認輸出和影片、教材寫的結果一致；再檢查 Qiskit 實跑紀錄與 notebook。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'tiny_sim.py'
        p.write_text(PURE_PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    for needle in ('h 0      → 1.00|1⟩', 't 0      → 0.71|0⟩ + 0.50+0.50i|1⟩', 'cz 1 0   → 0.50|00⟩ + 0.50|01⟩ + 0.50|10⟩ + −0.50|11⟩',
                   'h 0      → 0.71|00⟩ + 0.71|11⟩', 'h 0      → 0.15+0.35i|0⟩ + 0.85−0.35i|1⟩', '理想機率：0 14.6%、1 85.4%',
                   '理想機率：00 25.0%、01 25.0%、10 25.0%、11 25.0%'):
        assert needle in out, needle
    assert out.count('判定：預測正確') == 3 and out.count('判定：預測不對') == 2, out
    for needle in ('【範例甲：四個 T ＝ 一個 Z】', '        1  100.0%   100.0%    100.0%', '       00   50.0%    50.0%     48.3%',
                   '       11   50.0%    50.0%     51.7%', '        0    0.0%    14.6%     11.5%', '判定：預測不對（最多差 14.6%）',
                   '判定：預測不對（最多差 25.0%）'):
        assert needle in QISKIT_OUTPUT, needle
    assert QISKIT_OUTPUT.count('判定：預測正確') == 3
    nb = json.loads(NOTEBOOK)
    code = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
    assert nb['nbformat'] == 4 and code.count('def ') == PROGRAM.count('def ') and 'MY_PREDICT' in code
    compile(code, '專題模板.ipynb', 'exec')
    compile(PROGRAM, 'my_circuit.py', 'exec')
    return out


def html():
    pages = [
        '<h2>專題模板：我的線路</h2><p class="lead">四步：目標 → 線路 → 預測（先寫，寫好不改）→ 驗證。</p>'
        '<p class="ch">一、目標（我要說明什麼概念）</p><div class="line"></div>'
        '<p class="ch">二、線路圖（由左到右；q0 在最上面）</p><div class="grid"></div>'
        '<p class="ch">三、預測（先寫再跑）　日期：＿＿＿＿＿＿</p>'
        '<table class="judge"><tr><th style="width:22%">結果</th><th></th><th></th><th></th><th></th></tr>'
        '<tr><td class="k">預測機率</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">理想機率</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">抽樣 1000 次</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p class="ch">四、判定：□ 預測正確　□ 預測不對，原因：</p><div class="line"></div>',
        '<h2>工具箱與兩個範例</h2><p class="lead">簡報第 18、22 頁。相位閘不改機率，要前後夾 H 才看得見。</p>'
        '<table class="judge"><tr><th style="width:18%">閘</th><th>影片的念法</th><th>作用</th></tr>'
        '<tr><td class="k">H</td><td>哈達瑪閘</td><td>做出疊加</td></tr><tr><td class="k">X</td><td>翻轉閘</td><td>0 ↔ 1</td></tr>'
        '<tr><td class="k">Z</td><td>相位翻轉閘</td><td>|1⟩ 變號</td></tr><tr><td class="k">S</td><td>四分之一圈相位閘</td><td>S × 2 = Z</td></tr>'
        '<tr><td class="k">T</td><td>八分之一圈相位閘</td><td>T × 2 = S</td></tr><tr><td class="k">CNOT</td><td>受控反閘</td><td>控制是 1 就翻轉目標</td></tr>'
        '<tr><td class="k">CZ</td><td>受控相位翻轉閘</td><td>兩個都是 1 才變號；不分誰控制</td></tr></table>'
        '<pre class="code">範例甲  q0: H → T → T → T → T → H → 量      預測 1：100%\n'
        '範例乙  q0: H ─■─ H → 量\n        q1: H ─■────→ 量                  預測 00、11 各 50%</pre>'
        '<p>為什麼範例乙是貝爾態？（提示：CNOT = 目標前後夾 H 的 CZ）</p><div class="line"></div>',
        '<h2>換你改造：故意出錯</h2><p class="lead">出錯之前也要先預測。拿掉一個閘、換一個閘，或放錯目標位元。</p>'
        '<table class="judge"><tr><th style="width:22%"></th><th>原本的版本</th><th>故意出錯版</th></tr>'
        '<tr><td class="k">線路</td><td></td><td></td></tr><tr><td class="k">改了哪一步</td><td>—</td><td></td></tr>'
        '<tr><td class="k">我的預測</td><td></td><td></td></tr><tr><td class="k">理想機率</td><td></td><td></td></tr>'
        '<tr><td class="k">判定</td><td></td><td></td></tr></table>'
        '<pre class="code"># my_circuit.py：複製 my_circuit() 改成出錯版，再加進 PROJECTS\n'
        "PROJECTS.append(('我的故意出錯版', '（同我的專題）', my_wrong_circuit, MY_PREDICT))</pre>"
        '<p class="ch">差別說明（哪一步不一樣、結果怎麼變、為什麼）：</p><div class="line"></div><div class="line"></div>',
        '<h2>最後一關：驗證報告</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 我的線路要說明什麼概念（不看稿）：</p><div class="line"></div>'
        '<p>2. 哪一個結果是我的證據：</p><div class="line"></div>'
        '<p>3. 一個注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>寫出目標、畫出線路圖</li><li>預測在執行前寫好，寫上日期，沒有改過</li>'
        '<li>模擬器驗證：理想機率、抽樣 1000 次、判定</li><li>做出故意出錯版，寫出差別說明</li>'
        '<li>指出：先寫預測再跑，不看結果找理由</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q127 自己的線路與驗證報告 列印包', '父子科技學院 量子電腦學程 Q127｜專題：設計自己的線路', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q127-design-circuit', folder='Q127_設計自己的線路', files=FILES,
        sheet=('03_驗證報告.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_驗證報告.pdf', pack_pages=4,
        pack_needles=('專題模板：我的線路', '工具箱與兩個範例', '故意出錯', 'PROJECTS', '最後一關'),
        authoring_dir=XINEW / 'authoring/q127', episode_dir='specials/q127-design-circuit',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'yes（Python 3 與 pip install qiskit qiskit-aer；tiny_sim.py 只需 Python 3；動畫只需瀏覽器）',
               'program': 'my_circuit.py', 'notebook': '專題模板.ipynb', 'pureProgram': 'tiny_sim.py',
               'testedWith': 'qiskit 2.6.2, qiskit-aer 0.18.4, Python 3.13.18 (AerSimulator seed_simulator=127); tiny_sim.py standard library only, no randomness',
               'recordedRun': {'exampleA': {'circuit': 'H T T T T H', 'ideal': {'1': 1.0}, 'shots1000': {'1': 1.0}},
                               'exampleB': {'circuit': 'H H, CZ, H(q0)', 'ideal': {'00': 0.5, '11': 0.5}, 'shots1000': {'00': 0.483, '11': 0.517}},
                               'wrongA': {'circuit': 'H T T T H', 'ideal': {'0': 0.146, '1': 0.854}, 'shots1000': {'0': 0.115, '1': 0.885}},
                               'wrongB': {'circuit': 'H H, CZ', 'ideal': {'00': 0.25, '01': 0.25, '10': 0.25, '11': 0.25}}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q127/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

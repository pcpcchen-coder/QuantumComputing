"""Q124 課堂教材：八格檢查表、兩種跑法紀錄單、改造單、最後一關檢核表；八範例 notebook（八範例.ipynb 與同內容的 eight_examples.py）、
純 Python 答案卷 check_eight.py、解答與動畫導覽。

需要 Python 3 與 pip install qiskit qiskit-aer（不需要帳號）；沒有 Qiskit 時可先用 check_eight.py（只要 Python 3）對答案。
建置時會真的執行一次 check_eight.py，確認輸出和影片、教材寫的結果一致；Qiskit 部分（portable-runtime 沒有 Qiskit）比對製作代理已記錄的實跑輸出，
並檢查八範例.ipynb 是合法的 notebook JSON、程式格內容與 eight_examples.py 相同。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \\
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q124/classroom.py
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
RUN_OUTPUT = '''八個範例的理論機率（純 Python）
  1 疊加：0: 50%、1: 50%
  2 干涉：1: 100%
  3 Bell 態：00: 50%、11: 50%
  4 GHZ 態：000: 50%、111: 50%
  5 隱形傳態：0: 75%、1: 25%
  6 Deutsch：1: 100%
  7 BV：101: 100%
  8 Grover：11: 100%
改造區
  BV 密碼 011：011: 100%
  隱形傳態 角度 1.5708：0: 50%、1: 50%
'''

# 製作代理實跑紀錄：qiskit 2.6.2、qiskit-aer 0.18.4、Python 3.13.18；StatevectorSampler(seed=2026)、AerSimulator(seed_simulator=2026)，shots=1000
# （次數會隨種子與版本不同；理論機率不會變）
QISKIT_OUTPUT = '''一、Statevector 理論機率 vs 頁面；shots = 1000
  1 疊加：理論 0: 50%、1: 50%　和頁面一樣　量 1000 次 0: 464、1: 536
  2 干涉：理論 1: 100%　和頁面一樣　量 1000 次 1: 1000
  3 Bell 態：理論 00: 50%、11: 50%　和頁面一樣　量 1000 次 00: 464、11: 536
  4 GHZ 態：理論 000: 50%、111: 50%　和頁面一樣　量 1000 次 000: 464、111: 536
  5 隱形傳態：理論 0: 75%、1: 25%　和頁面一樣　量 1000 次 0: 731、1: 269
  6 Deutsch：理論 1: 100%　和頁面一樣　量 1000 次 1: 1000
  7 BV：理論 101: 100%　和頁面一樣　量 1000 次 101: 1000
  8 Grover：理論 11: 100%　和頁面一樣　量 1000 次 11: 1000
  八個範例裡，理論機率和頁面一樣的有 8 個
二、換成本機高效能模擬器 qiskit-aer（同樣量 1000 次）
  1 疊加：0: 510、1: 490
  2 干涉：1: 1000
  3 Bell 態：00: 504、11: 496
  4 GHZ 態：000: 496、111: 504
  5 隱形傳態：0: 752、1: 248
  6 Deutsch：1: 1000
  7 BV：101: 1000
  8 Grover：11: 1000
三、改造區：換成自己的參數，先預測，再執行
  BV 密碼 011：理論 011: 100%　讀出的正是密碼
  隱形傳態 角度 1.5708：理論 0: 50%、1: 50%　公式 sin² 算出 1 的機率 50%
'''

# 製作代理另外做的全面比對（Node 執行 basic-circuits.html 的引擎，列出 74 種選項組合與 qiskitCode() 產生的程式，逐一用 Qiskit 2.6.2 Statevector 執行）
CHECK74 = '''74 種選項組合：疊加 2、干涉 2、Bell 4、GHZ 2、隱形傳態 4、Deutsch 4、BV 8、Grover 48（2 顆：答案 4 種 × 輪數 4 種；3 顆：答案 8 種 × 輪數 4 種）
機率比對：74／74 一致（最大差 3e-15）
振幅比對：46 種完全相同；28 種差一個整體負號（−1 倍），全部是 Grover 奇數輪（1 輪 16 種、3 輪 12 種）；Grover 偶數輪 20 種完全相同
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q124：用 Qiskit 重現八個範例（八範例 notebook 的程式版）

安裝（只要一次）：  pip install qiskit qiskit-aer
執行：              python eight_examples.py
每個範例的線路都照 animations/basic-circuits.html 頁面最下方「Qiskit 程式碼」區塊（預設選項）抄寫。
每個範例跑兩次：
  1. Statevector：不量測，直接算出理論機率，和頁面灰色底的理論機率比對（數字要一樣）
  2. shots：量 1000 次，數每種結果出現幾次（像頁面的「量測 1,000 次」，每次跑都會差一點）
位元字串的最右邊是 q0（和頁面、Qiskit 的讀法相同）。
用 VS Code 或 Jupyter 開啟時，每個「# %%」是一格，可以一格一格執行；八範例.ipynb 是同樣內容的筆記本版。
"""
# %% 匯入
from math import pi, sin

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


# %% 範例 1　疊加：量子硬幣（起始態 = |0⟩）
def superposition():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc


# %% 範例 2　干涉：H-Z-H = X（中間的閘 = 有 Z）
def interference():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.z(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


# %% 範例 3　Bell 態（Φ⁺）
def bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


# %% 範例 4　GHZ 態（3 顆）
def ghz():
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc


# %% 範例 5　隱形傳態（ψ = √¾|0⟩ + ½|1⟩，只量 q2）
def teleport(angle=pi / 3):
    qc = QuantumCircuit(3, 1)
    qc.ry(angle, 0)          # 準備要傳的狀態 ψ（q0）
    qc.h(1)
    qc.cx(1, 2)              # 糾纏對（q1、q2）
    qc.cx(0, 1)
    qc.h(0)                  # Alice：Bell 量測的前半
    qc.cx(1, 2)
    qc.cz(0, 2)              # Bob：用受控閘代替「量完再修正」，結果相同
    qc.measure(2, 0)
    return qc


# %% 範例 6　Deutsch（黑盒裡的函數 f(x) = x）
def deutsch():
    qc = QuantumCircuit(2, 1)
    qc.x(1)
    qc.h([0, 1])
    qc.cx(0, 1)              # 黑盒 U_f（只查詢這一次）
    qc.h(0)
    qc.measure(0, 0)
    return qc


# %% 範例 7　Bernstein–Vazirani（密碼 s = 101，寫法 s2 s1 s0）
def bv(secret='101'):
    qc = QuantumCircuit(4, 3)
    qc.x(3)
    qc.h([0, 1, 2, 3])
    for q in range(3):       # 黑盒：計算 s·x（只查詢這一次）
        if secret[2 - q] == '1':
            qc.cx(q, 3)
    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc


# %% 範例 8　Grover（2 顆、答案 11、最佳 1 輪）
def grover():
    qc = QuantumCircuit(2, 2)
    qc.h([0, 1])
    qc.cz(0, 1)              # 標記：答案 11 變號
    qc.h([0, 1])             # 擴散：H、X、CZ、X、H（會多一個整體負號，不影響機率）
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    qc.measure([0, 1], [0, 1])
    return qc


# %% 頁面灰色底的理論機率（basic-circuits.html，預設選項）
PAGE = {
    '1 疊加': {'0': 0.5, '1': 0.5},
    '2 干涉': {'1': 1.0},
    '3 Bell 態': {'00': 0.5, '11': 0.5},
    '4 GHZ 態': {'000': 0.5, '111': 0.5},
    '5 隱形傳態': {'0': 0.75, '1': 0.25},
    '6 Deutsch': {'1': 1.0},
    '7 BV': {'101': 1.0},
    '8 Grover': {'11': 1.0},
}
CIRCUITS = dict(zip(PAGE, (superposition, interference, bell, ghz, teleport, deutsch, bv, grover)))


def theory(qc):
    """Statevector：拿掉最後的量測，算出被量測那幾顆位元的理論機率"""
    measured = sorted(qc.find_bit(i.qubits[0]).index for i in qc.data if i.operation.name == 'measure')
    sv = Statevector(qc.remove_final_measurements(inplace=False))
    return {k: v for k, v in sorted(sv.probabilities_dict(qargs=measured).items()) if v > 1e-12}


def same(p, q):
    return all(abs(p.get(k, 0) - q.get(k, 0)) < 1e-9 for k in set(p) | set(q))


def fmt(d, pct=True):
    return '、'.join(f'{k}: {v:.0%}' if pct else f'{k}: {v}' for k, v in sorted(d.items()))


# %% 一、兩種跑法：Statevector 理論機率和頁面比；shots = 1000
sampler = StatevectorSampler(seed=2026)   # 固定種子，全班印出來的次數才會一樣；拿掉就每次不同
print('一、Statevector 理論機率 vs 頁面；shots = 1000')
matched = 0
for name, make in CIRCUITS.items():
    qc = make()
    p = theory(qc)
    ok = same(p, PAGE[name])
    matched += ok
    counts = sampler.run([qc], shots=1000).result()[0].data.c.get_counts()
    print(f'  {name}：理論 {fmt(p)}　和頁面{"一樣" if ok else "不一樣！"}　量 1000 次 {fmt(counts, False)}')
print(f'  八個範例裡，理論機率和頁面一樣的有 {matched} 個')

# %% 二、換成本機高效能模擬器 qiskit-aer
print('二、換成本機高效能模擬器 qiskit-aer（同樣量 1000 次）')
try:
    from qiskit import transpile
    from qiskit_aer import AerSimulator
    sim = AerSimulator(seed_simulator=2026)
    for name, make in CIRCUITS.items():
        counts = sim.run(transpile(make(), sim), shots=1000).result().get_counts()
        print(f'  {name}：{fmt(counts, False)}')
except ImportError:
    print('  沒有安裝 qiskit-aer，跳過（pip install qiskit-aer）')

# %% 三、改造區
print('三、改造區：換成自己的參數，先預測，再執行')
MY_SECRET = '011'  # BV 的密碼（s2 s1 s0），到頁面 #bv 點成同一組密碼再比對
MY_ANGLE = pi / 2  # 隱形傳態 ψ 的角度：量到 1 的機率應該是 sin²(角度 / 2)
p = theory(bv(MY_SECRET))
print(f'  BV 密碼 {MY_SECRET}：理論 {fmt(p)}　{"讀出的正是密碼" if p.get(MY_SECRET, 0) > 0.999 else "和密碼不一樣！"}')
p = theory(teleport(MY_ANGLE))
print(f'  隱形傳態 角度 {MY_ANGLE:.4f}：理論 {fmt(p)}　公式 sin² 算出 1 的機率 {sin(MY_ANGLE / 2) ** 2:.0%}')
'''

PURE_PROGRAM = '''"""父子科技學院 量子電腦學程 Q124：八個範例的「答案卷」（純 Python，不需安裝任何套件）

執行：  python check_eight.py
沒有 Qiskit 也能先對答案：用最簡單的狀態向量模擬（只有實數振幅，沒有亂數、沒有雜訊），
照 basic-circuits.html 的八個線路一步一步算，印出被量測位元的理論機率。
位元字串的最右邊是 q0。
"""
from math import cos, pi, sin, sqrt


def run(n, gates):
    """從全零開始，依序做 gates，回傳 2ⁿ 個振幅"""
    v = [0.0] * 2 ** n
    v[0] = 1.0
    for g, *q in gates:
        for i in range(2 ** n):
            if g in ('h', 'x', 'ry'):
                m = 1 << q[0]
                if i & m:
                    continue
                a, b = v[i], v[i | m]
                if g == 'h':
                    v[i], v[i | m] = (a + b) / sqrt(2), (a - b) / sqrt(2)
                elif g == 'x':
                    v[i], v[i | m] = b, a
                else:   # ry(角度)
                    c, s = cos(q[1] / 2), sin(q[1] / 2)
                    v[i], v[i | m] = c * a - s * b, s * a + c * b
            elif g == 'z' and i >> q[0] & 1:
                v[i] = -v[i]
            elif g == 'cz' and i >> q[0] & 1 and i >> q[1] & 1:
                v[i] = -v[i]
            elif g == 'cx' and i >> q[0] & 1 and not i >> q[1] & 1:
                j = i | 1 << q[1]
                v[i], v[j] = v[j], v[i]
    return v


def probs(n, gates, measured):
    out = {}
    for i, a in enumerate(run(n, gates)):
        if a * a > 1e-12:
            k = ''.join(str(i >> q & 1) for q in sorted(measured, reverse=True))
            out[k] = out.get(k, 0) + a * a
    return '、'.join(f'{k}: {p:.0%}' for k, p in sorted(out.items()))


def H(*qs):
    return [('h', q) for q in qs]


def X(*qs):
    return [('x', q) for q in qs]


def bv(secret):
    return X(3) + H(0, 1, 2, 3) + [('cx', q, 3) for q in range(3) if secret[2 - q] == '1'] + H(0, 1, 2)


def teleport(angle):
    return [('ry', 0, angle)] + H(1) + [('cx', 1, 2), ('cx', 0, 1)] + H(0) + [('cx', 1, 2), ('cz', 0, 2)]


EIGHT = [
    ('1 疊加', 1, H(0), [0]),
    ('2 干涉', 1, H(0) + [('z', 0)] + H(0), [0]),
    ('3 Bell 態', 2, H(0) + [('cx', 0, 1)], [0, 1]),
    ('4 GHZ 態', 3, H(0) + [('cx', 0, 1), ('cx', 1, 2)], [0, 1, 2]),
    ('5 隱形傳態', 3, teleport(pi / 3), [2]),
    ('6 Deutsch', 2, X(1) + H(0, 1) + [('cx', 0, 1)] + H(0), [0]),
    ('7 BV', 4, bv('101'), [0, 1, 2]),
    ('8 Grover', 2, H(0, 1) + [('cz', 0, 1)] + H(0, 1) + X(0, 1) + [('cz', 0, 1)] + X(0, 1) + H(0, 1), [0, 1]),
]

if __name__ == '__main__':
    print('八個範例的理論機率（純 Python）')
    for name, n, gates, measured in EIGHT:
        print(f'  {name}：{probs(n, gates, measured)}')
    MY_SECRET = '011'
    MY_ANGLE = pi / 2
    print('改造區')
    print(f'  BV 密碼 {MY_SECRET}：{probs(4, bv(MY_SECRET), [0, 1, 2])}')
    print(f'  隱形傳態 角度 {MY_ANGLE:.4f}：{probs(3, teleport(MY_ANGLE), [2])}')
'''


def notebook(src):
    """把 eight_examples.py 依「# %%」切成格：開頭說明變成文字格，每一段前面加一格標題文字。"""
    _, doc, body = src.split('"""', 2)
    body = body.lstrip('\n')
    cells = [{'cell_type': 'markdown', 'metadata': {}, 'source': ['# 八範例 notebook（Q124）\n', '\n'] + [ln + '\n' for ln in doc.splitlines()]}]
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

EXAMPLES = [  # (範例, 頁面 hash, 線路重點, 頁面理論機率)
    ('1 疊加', '#superposition', 'h(0)', '0: 50%、1: 50%'),
    ('2 干涉', '#interference', 'h、z、h', '1: 100%'),
    ('3 Bell 態', '#bell', 'h(0)、cx(0, 1)', '00: 50%、11: 50%'),
    ('4 GHZ 態', '#ghz', 'h(0)、cx(0, 1)、cx(1, 2)', '000: 50%、111: 50%'),
    ('5 隱形傳態', '#teleport', 'ry(pi / 3, 0)…cz(0, 2)；只量 q2', '0: 75%、1: 25%'),
    ('6 Deutsch', '#deutsch', 'f(x) = x：cx(0, 1)', '1: 100%'),
    ('7 BV', '#bv', '密碼 101：cx(0, 3)、cx(2, 3)', '101: 100%'),
    ('8 Grover', '#grover', '2 顆、答案 11、1 輪', '11: 100%'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q124：用 Qiskit 重現八個範例（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的第十二課。
Q113–Q122 在瀏覽器裡逐一看過 basic-circuits.html 的八個範例；今天把每一頁底部的「Qiskit 程式碼」搬到自己的電腦，用本機模擬器各跑兩次，和頁面比對。
核心一句話：**圖看起來對不算數；Statevector 算出的理論機率和頁面灰色底一模一樣，才算重現。**

## 今天的好玩機制：Release 任務

就像軟體推出新版本前要過檢查：八個範例是八格檢查表，每格都要「Statevector 一致 ＋ shots 接近」才打勾，八格全勾才「發布」八範例 notebook v1.0。

## 兩種跑法（eight_examples.py 第一段）

| 跑法 | 做什麼 | 和頁面哪裡比 | 比對標準 |
|---|---|---|---|
| Statevector | 拿掉量測，直接算出理論機率（`qiskit.quantum_info.Statevector`） | 量測卡的灰色底（理論機率） | 一模一樣 |
| shots = 1000 | 真的抽樣 1000 次，數每種結果幾次（`StatevectorSampler`） | 按「量測 1,000 次」後的綠色柱 | 只會接近，每次不同 |

## 八個範例的預設選項與理論機率（頁面＝Qiskit Statevector，製作代理實跑 8／8 一致）

| 範例 | 頁面 | 線路重點 | 理論機率（最右邊是 q0） |
|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in EXAMPLES) + '''
頁面另外宣稱 74 種選項組合都和 Statevector 一致（README.md、頁尾小字）。製作代理把 74 種的程式碼逐一跑過：**機率 74／74 一致**；
但若比振幅，Grover 奇數輪的 28 種會差一個整體負號（頁面的擴散照理想「對平均值翻轉」計算，H、X、多控制 Z 組成的電路多一個 −1；量不到，所以機率相同）。

## 容易錯的地方與限制（驗收要孩子說出至少一個）

1. **自己的版本也要比對，不要只看圖**：頁面替 74 種組合對過答案，但孩子改過的參數頁面沒檢查過；shots 的直方圖每次會跳，要用 Statevector 的數字比。
2. **紀錄的名字**：頁面程式用 `QuantumCircuit(n, m)` 建紀錄、取次數寫 `.data.c`；改用 `measure_all()`（如 QC_Operation_Talk.pptx 第 27 頁）時名字變成 `meas`，要寫 `.data.meas`。
3. **固定種子**：`StatevectorSampler(seed=2026)` 每次 run 都從同一串亂數開始，所以疊加、Bell、GHZ 三個各半的範例會印出一模一樣的次數；拿掉 seed 就每次不同。
4. **只比機率、不比振幅**：Grover 的振幅可能整體差一個負號（見上）。
5. **隱形傳態只量 q2**：紀錄只有 1 格；而且用受控閘代替「中途量測再修正」，真實硬體要用動態電路（QC_Operation_Talk.pptx 第 28 頁 if_test）。
6. 本機模擬器是理想的、沒有雜訊；真實量子電腦會多出不該出現的結果（QC_Operation_Talk.pptx 第 27 頁的 01、10）。

## 影片的念法

Qiskit 說「量子程式套件」；Statevector 說「狀態向量」；shots 說「量一千次」；notebook 說「筆記本」；qiskit-aer 說「高效能模擬器」；
Deutsch 念「德意志」；BV 說「密碼範例」；Grover 念「格羅弗」；Bell 念「貝爾態」；GHZ 說「範例四」「全零、全一」；
H「哈達瑪閘」、X「翻轉閘」、Z「相位翻轉閘」、CNOT「受控反閘」、CZ「受控相位翻轉閘」、Ry「旋轉閘」；|+⟩「正號疊加態」；q0、q1、q2 念「編號零」到「編號二」；π 說「圓周率」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；說明 Release 任務：八格全勾才發布 | 影片、列印包第 1 頁 |
| 10–25 | 打開 basic-circuits.html，示範一個範例的程式碼區塊、灰色底與量測 1,000 次；說明兩種跑法 | 動畫、`05_動畫導覽.md` |
| 25–65 | 八段程式貼進 notebook；每格 Statevector 與 shots 各跑一次，填八格檢查表；再用 qiskit-aer 重跑 | `八範例.ipynb`、`01_操作步驟.md`、列印包第 1、2 頁、`03_八格檢查表.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子把一個範例改成自己的參數，先預測、再比對（頁面或公式） | 列印包第 3 頁、notebook 的「三、改造區」 |
| 105–115 | 孩子教爸爸：兩種跑法差在哪、以誰為準、一個注意事項 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替 notebook 命名、存成 v1.0 | |

## 課前準備（約 15 分鐘）

- 安裝 Python 3（3.10 以上），在終端機執行 `pip install qiskit qiskit-aer`（製作代理用 qiskit 2.6.2、qiskit-aer 0.18.4 實跑；頁面寫 Qiskit 1.x 或 2.x）。
- 想用 notebook 介面：VS Code 加 Jupyter 擴充，或 `pip install notebook` 後執行 `jupyter notebook`，開啟 `八範例.ipynb`。沒有 notebook 介面也可以直接 `python eight_examples.py`。
- 先跑一次 `python check_eight.py`（只要 Python 3），確認八個理論機率；再跑 `python eight_examples.py`，第一段最後一行應該是「理論機率和頁面一樣的有 8 個」。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html`；打開 `slides/output/basic-circuits.pptx` 第 28–29 頁、`slides/QC_Operation_Talk.pptx` 第 27 頁（課綱頁碼正確）。
- 列印 `02_列印包_八格檢查表.pdf`（A4，共 4 頁）。

## 誠實說明

- 模擬器是理想模擬，沒有雜訊；shots 的次數是隨機的，影片不念隨機次數。
- 只用 Qiskit 2.6.2、qiskit-aer 0.18.4 實測；其他版本的介面可能不同（QC_Operation_Talk 第 27 頁備註：以官方文件為準）。
- `八範例.ipynb` 是由 eight_examples.py 依「# %%」切格產生，沒有預先存輸出；製作代理把各程式格依序執行過，輸出和 eight_examples.py 相同。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：八格檢查表（約 40 分鐘）

1. 爸爸在終端機執行 `pip install qiskit qiskit-aer`，再開啟 `八範例.ipynb`（或 `eight_examples.py`）。
2. 用瀏覽器開 `basic-circuits.html`，點「範例 1 疊加」，捲到最底下展開「Qiskit 程式碼（會隨上面的選項改變）」。
   對照 notebook 的「範例 1」那一格：閘是不是一樣？（notebook 為了兩種跑法，把頁面的 print 與 StatevectorSampler 那兩行搬到最後一段。）
3. 八個範例都對照完，依序執行每一格；執行「一、兩種跑法」那一格，印出八行。
4. 在列印包第 1 頁逐格填：頁面灰色底的理論機率（在頁面按「量測 1,000 次」也看得到）、Statevector 理論機率、shots 次數、是否一致。兩個理論機率一模一樣、shots 接近，才打勾。
5. 八格全勾後，執行「二、換成本機高效能模擬器 qiskit-aer」那一格，在列印包第 2 頁比較兩次的次數：數字不同，但分布一樣嗎？
6. 想更多：把 `StatevectorSampler(seed=2026)` 的 seed 拿掉再跑兩次，次數會變；理論機率不會變。

## 下半場：換成自己的參數（約 30 分鐘）

1. 在「三、改造區」把 `MY_SECRET` 改成別的密碼（三位，例如 110），先在列印包第 3 頁寫預測，再執行。
2. 到頁面 `basic-circuits.html#bv` 點密碼按鈕（s2 s1 s0）成同一組，按「量測 1,000 次」，兩邊比對；再展開程式碼區塊，看黑盒子的 cx 那幾行是不是和 notebook 的 bv() 產生的一樣（`print(bv(MY_SECRET).draw())`）。
3. 把 `MY_ANGLE` 改成別的角度（例如 pi / 4、pi），頁面沒有這個選項，就用公式 sin²(角度 / 2) 算量到 1 的機率來比。
4. 進階：把 Grover 改成 3 顆（照頁面 3 顆的程式碼抄），或 GHZ 改成 4 顆；一樣要用 Statevector 比，不要只看直方圖。
''',

'eight_examples.py': PROGRAM,
'八範例.ipynb': NOTEBOOK,
'check_eight.py': PURE_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## check_eight.py 實跑輸出（Python 3.13.18，沒有亂數）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## eight_examples.py 實跑輸出（qiskit 2.6.2、qiskit-aer 0.18.4；StatevectorSampler seed=2026、AerSimulator seed_simulator=2026；次數會隨種子不同）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 74 種組合的全面比對（製作代理另外做）\n\n```\n' + CHECK74 + '```\n\n'
  '## 常見問題\n\n'
  '- 為什麼疊加、Bell、GHZ 三個範例的 shots 次數一模一樣？`StatevectorSampler(seed=2026)` 每次 run 都從同一串亂數開始抽，三個都是兩種結果各半，所以抽出來的分法一樣。拿掉 seed 就不同。\n'
  '- 為什麼干涉、Deutsch、BV、Grover 的 1000 次全部同一個結果？它們的理論機率是 100%，不是隨機的。\n'
  '- Statevector 和頁面不一樣怎麼辦？先檢查位元順序（最右邊是 q0）、選項是不是預設、有沒有少抄一個閘。\n'
  '- 取次數時出現 AttributeError？頁面的程式紀錄叫 c（`.data.c`）；用 `measure_all()` 的程式要改成 `.data.meas`。\n'
  '- 比振幅時 Grover 差一個負號？那是整體負號，量不到；Release 檢查以機率為準。\n'
  '- 改造 MY_ANGLE = pi / 2：量到 1 的機率是 sin²(π/4) = 50%；pi 是 100%；pi / 3 回到預設的 25%。\n'
  '- 下一課 Q125：量測 1 次與 1000 次。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。

## `animations/basic-circuits.html`（量子電路入門：八個基礎量子電路）

- 上方分頁「範例 1」到「範例 8」；網址加 `#superposition`、`#interference`、`#bell`、`#ghz`、`#teleport`、`#deutsch`、`#bv`、`#grover` 直接開啟。
- 範例標題下面是選項（例如 Bell 的四種、BV 的密碼按鈕 s2 s1 s0、Grover 的位元數與答案與輪數）；全部選項組合共 74 種。
- 右下「量測」卡：量測 1 次、量測 1,000 次、清除；灰色底是理論機率，綠色是實際次數。
- 頁面最底下「重點」卡裡有「Qiskit 程式碼（會隨上面的選項改變）」，點一下展開；右下「複製程式碼」。程式用 StatevectorSampler 量 1000 次，最後一行註解「位元字串的最右邊是 q0」。
- 頁尾小字：頁面振幅由內建的狀態向量模擬器即時計算，和 Qiskit 的 Statevector 結果一致（Grover 的擴散照理想計算，實際電路多一個整體負號，機率相同）。

## 影片裡的三段動畫

- 隱形傳態（#teleport）的程式碼：QuantumCircuit(3, 1)、ry(pi / 3, 0)、受控閘代替中途量測的註解；ψ 換成 |+⟩ 時 ry 換成 h(0)。
- Grover（#grover）的程式碼：2 顆時標記只有 cz(0, 1)、擴散五行；換成 3 顆後變成兩輪、ccz；頁尾的 Statevector 說明。
- BV（#bv）改成密碼 110：量測 1,000 次只有 110；程式碼的黑盒子變成 cx(1, 3)、cx(2, 3)。
''',
}

SHEET_HEADER = ['範例', '頁面 hash', '頁面灰色底理論機率', 'Statevector 理論機率', '一致？', 'shots 1000 次數', 'qiskit-aer 次數', '打勾']
SHEET_ROWS = [[e[0], e[1], e[3], '', '', '', '', ''] for e in EXAMPLES]

EXTRA_CSS = '''table.rec td{height:10mm;font-size:10pt}table.rec td.k{font-weight:bold;color:#0b2540;width:15%}
table.rec th{font-size:9.5pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 check_eight.py（隔離模式），確認輸出和影片、教材寫的結果一致；再和已記錄的 Qiskit 實跑輸出交叉比對理論機率。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'check_eight.py'
        p.write_text(PURE_PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    pure = re.findall(r'^  (\d .+?)：(.+)$', out, re.M)[:8]
    qk = re.findall(r'^  (\d .+?)：理論 (.+?)　和頁面一樣　', QISKIT_OUTPUT, re.M)
    assert pure == qk and len(qk) == 8, (pure, qk)
    assert [(e[0], e[3]) for e in EXAMPLES] == qk
    assert '理論機率和頁面一樣的有 8 個' in QISKIT_OUTPUT
    nb = json.loads(NOTEBOOK)
    code = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
    assert nb['nbformat'] == 4 and code.count('def ') == PROGRAM.count('def ') and 'MY_SECRET' in code
    compile(code, '八範例.ipynb', 'exec')
    compile(PROGRAM, 'eight_examples.py', 'exec')
    return out


def html():
    row = lambda e: (f'<tr><td class="k">{e[0]}</td><td>{e[1]}</td><td>{e[3]}</td><td></td><td></td><td></td></tr>')  # noqa: E731
    pages = [
        '<h2>八格檢查表</h2><p class="lead">Release 任務：每格都要「Statevector 和頁面一模一樣 ＋ shots 接近」才打勾，八格全勾才發布 v1.0。位元字串最右邊是 q0。</p>'
        '<table class="rec"><tr><th style="width:15%">範例</th><th style="width:13%">頁面</th><th>頁面灰色底</th><th>Statevector 理論機率</th><th>shots 1000 次</th><th style="width:8%">✓</th></tr>'
        + ''.join(row(e) for e in EXAMPLES) + '</table>'
        '<p>八格裡，Statevector 和頁面一模一樣的有＿＿格；shots 剛好等於理論的有＿＿格（為什麼？）</p>',
        '<h2>兩種跑法紀錄</h2><p class="lead">同一條線路跑兩次：Statevector 算理論機率，shots 真的量 1000 次；最後換 qiskit-aer 再量一次。</p>'
        '<table class="rec"><tr><th style="width:18%">範例</th><th>StatevectorSampler 次數</th><th>qiskit-aer 次數</th><th>分布一樣嗎？</th></tr>'
        '<tr><td class="k">1 疊加</td><td></td><td></td><td></td></tr><tr><td class="k">3 Bell 態</td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">4 GHZ 態</td><td></td><td></td><td></td></tr><tr><td class="k">5 隱形傳態</td><td></td><td></td><td></td></tr></table>'
        '<p>固定 seed=2026 時，1、3、4 三格的次數有什麼特別？＿＿＿＿＿＿＿＿＿＿＿＿＿</p><div class="line"></div>'
        '<p>拿掉 seed 再跑兩次：次數變了嗎？理論機率變了嗎？</p><div class="line"></div>'
        '<pre class="code">sampler = StatevectorSampler(seed=2026)   # 固定種子\n'
        'counts = sampler.run([qc], shots=1000).result()[0].data.c.get_counts()\n'
        '# measure_all() 的紀錄叫 meas：.data.meas.get_counts()</pre>',
        '<h2>換成自己的參數</h2><p class="lead">孩子獨立改造：先預測，再執行，最後比對（頁面有的選項到頁面比；頁面沒有的用公式比）。</p>'
        '<pre class="code"># eight_examples.py／八範例.ipynb 的「三、改造區」\n'
        "MY_SECRET = '011'  # BV 的密碼（s2 s1 s0）\n"
        'MY_ANGLE = pi / 2  # 隱形傳態 ψ 的角度：量到 1 的機率 = sin²(角度 / 2)</pre>'
        '<div class="box"><p>我改的參數：＿＿＿＿＿＿＿＿＿＿　改成：＿＿＿＿＿＿＿＿</p>'
        '<p>我的預測（理論機率）：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>Statevector 結果：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>比對對象（圈一個）：頁面灰色底　／　公式 sin²(角度 / 2)　／　自己手算</p>'
        '<p>一樣嗎？如果不一樣，原因：</p><div class="line"></div><div class="line"></div></div>'
        '<p>提醒：頁面替 74 種組合對過答案，但你改過的版本沒人檢查過，自己也要比對，不能只看圖。</p>',
        '<h2>最後一關：發布前的答辯</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：v1.0　日期：＿＿＿＿＿＿</p>'
        '<p>1. Statevector 和 shots 差在哪裡（不看稿）：</p><div class="line"></div>'
        '<p>2. 為什麼比對要以 Statevector 為準：</p><div class="line"></div>'
        '<p>3. 一個注意事項或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>八範例 notebook：八格都有 Statevector 與 shots 的輸出</li><li>八格檢查表全部打勾（理論機率和頁面一模一樣）</li>'
        '<li>用 qiskit-aer 重跑一次，說出次數不同但分布一樣</li><li>改一個參數，先預測再比對</li>'
        '<li>指出：自己的版本也要比對；比機率、不直接比振幅</li><li>錄音總結、替 notebook 命名、存成 v1.0</li></ul></div>',
    ]
    return printpack.document('Q124 八格檢查表 列印包', '父子科技學院 量子電腦學程 Q124｜用 Qiskit 重現八個範例', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q124-qiskit-eight', folder='Q124_用Qiskit重現八個範例', files=FILES,
        sheet=('03_八格檢查表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_八格檢查表.pdf', pack_pages=4,
        pack_needles=('八格檢查表', '兩種跑法紀錄', '換成自己的參數', 'MY_SECRET', '最後一關'),
        authoring_dir=XINEW / 'authoring/q124', episode_dir='specials/q124-qiskit-eight',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'yes（Python 3 與 pip install qiskit qiskit-aer；check_eight.py 只需 Python 3）',
               'program': 'eight_examples.py', 'notebook': '八範例.ipynb', 'answerKey': 'check_eight.py',
               'testedWith': 'qiskit 2.6.2, qiskit-aer 0.18.4, Python 3.13.18 (StatevectorSampler seed=2026, AerSimulator seed_simulator=2026); '
                             'check_eight.py standard library only, no randomness',
               'recordedRun': {'defaultsMatchPage': 8, 'combinationsChecked': 74, 'combinationsProbabilityMatch': 74,
                               'amplitudeIdentical': 46, 'amplitudeGlobalMinus': 28, 'globalMinusCases': 'Grover odd rounds (1 round 16, 3 rounds 12)',
                               'theory': {e[0]: e[3] for e in EXAMPLES},
                               'remix': {'bvSecret011': '011: 100%', 'teleportAnglePiOver2': '0: 50%, 1: 50%'}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q124/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

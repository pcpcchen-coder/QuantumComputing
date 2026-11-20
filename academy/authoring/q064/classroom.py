"""Q064 課堂教材：可執行的筆記本 my_circuit_release.ipynb（與同內容的 .py，會自動寫出實驗報告）、操作檢查表、實驗報告單、
最佳化等級比較表、重現測試與說明卡、解答。

只用本機模擬器，不需要帳號；需要在自己的電腦安裝開源套件（pip install qiskit qiskit-aer）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q064/classroom.py
"""
from pathlib import Path
import json
import os
import re
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18、qiskit 2.6.2、qiskit-aer 0.18.4、shots=1024、seed_simulator=2026、seed_transpiler=2026
# 假想晶片：直線 5 顆，原生閘 rz、sx、x、cx；雜訊：sx、x 去極化 1%、cx 去極化 1%、讀取 3%
TESTED = 'Python 3.13.18, qiskit 2.6.2, qiskit-aer 0.18.4'
RUNS = {  # 題目: (答案, {等級: (深度, sx+x, cx, 理想答案次數, 有雜訊答案次數)})
    'grover2': ('11', {0: (26, 14, 2, 1024, 866), 3: (12, 6, 2, 1024, 915)}),
    'grover3': ('101', {0: (156, 47, 51, 969, 458), 3: (95, 27, 39, 970, 550)}),
    'deutsch': ('1', {0: (9, 4, 1, 1024, 953), 3: (7, 3, 1, 1024, 958)}),
    'bell': ('00', {0: (5, 1, 1, 516, 478), 3: (5, 1, 1, 516, 478)}),
    'ghz3': ('000', {0: (6, 1, 2, 514, 471), 3: (6, 1, 2, 514, 471)}),
}
GROVER2_NOISY = {0: {'00': 25, '01': 67, '10': 66, '11': 866}, 3: {'00': 18, '01': 46, '10': 45, '11': 915}}
SEEDS_G2 = {0: [879, 866, 890, 865, 862], 3: [920, 908, 929, 912, 909]}  # 種子 1–5，有雜訊時 11 的次數
for lv, c in GROVER2_NOISY.items():
    assert sum(c.values()) == 1024 and c['11'] == RUNS['grover2'][1][lv][4]
assert [b - a for a, b in zip(SEEDS_G2[0], SEEDS_G2[3])] == [41, 42, 39, 47, 47]

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q064：模組專題——在模擬器跑我的線路（Release 任務，本機模擬器，不需要帳號）

安裝（只要一次）：  pip install qiskit qiskit-aer
執行：              python my_circuit_release.py
同一份程式也做成筆記本：my_circuit_release.ipynb（Jupyter 或 VS Code 開啟，按「全部重新執行」）
操作檢查表：① 定義問題 → ② 線路 → ③ 轉譯 → ④ 執行 → ⑤ 解讀（寫報告）
"""
# ── 第 0 格：記錄版本（報告第一段要抄）──────────────────────────────────
import sys
import qiskit
import qiskit_aer
VERSIONS = f'Python {sys.version.split()[0]} | qiskit {qiskit.__version__} | qiskit-aer {qiskit_aer.__version__}'
print(VERSIONS)
# 影片與解答用的版本：Python 3.13.18、qiskit 2.6.2、qiskit-aer 0.18.4

# ── 第 1 格：① 定義問題（改造區：換一個學過的演算法）──────────────────────
CHOICE = 'grover2'   # 可以改成 'bell'、'ghz3'、'deutsch'、'grover2'、'grover3'
PROBLEMS = {
    'bell':    ('貝爾態：兩顆位元糾纏', '00 和 11 各一半'),
    'ghz3':    ('格林伯格態：三顆一起糾纏', '000 和 111 各一半'),
    'deutsch': ('多伊奇演算法：f(x) = x 是常數還是平衡？', '1（平衡）'),
    'grover2': ('格羅弗搜尋：4 個抽屜找 11', '11'),
    'grover3': ('格羅弗搜尋：8 個抽屜找 101（2 輪）', '101'),
}
QUESTION, EXPECT = PROBLEMS[CHOICE]
print('問題：', QUESTION, '｜預期答案：', EXPECT)

# ── 第 2 格：② 線路 ───────────────────────────────────────────────────────
from qiskit import QuantumCircuit


def grover(n, target, rounds):
    """n 顆位元的格羅弗搜尋；target 的最右邊是 q0。"""
    qc = QuantumCircuit(n, n)
    qc.h(range(n))                            # 均勻疊加：每個抽屜一樣大
    zeros = [i for i, b in enumerate(reversed(target)) if b == '0']
    for _ in range(rounds):
        if zeros:
            qc.x(zeros)                       # 標記：把答案變成全 1 ……
        qc.h(n - 1); qc.mcx(list(range(n - 1)), n - 1); qc.h(n - 1)   # …… 多控制相位翻轉 ……
        if zeros:
            qc.x(zeros)                       # …… 再還原
        qc.h(range(n)); qc.x(range(n))        # 擴散：對平均值翻轉
        qc.h(n - 1); qc.mcx(list(range(n - 1)), n - 1); qc.h(n - 1)
        qc.x(range(n)); qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


def build(choice):
    if choice == 'bell':
        qc = QuantumCircuit(2, 2); qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1])
    elif choice == 'ghz3':
        qc = QuantumCircuit(3, 3); qc.h(0); qc.cx(0, 1); qc.cx(1, 2); qc.measure(range(3), range(3))
    elif choice == 'deutsch':                 # 黑盒 f(x) = x：一個受控反閘
        qc = QuantumCircuit(2, 1); qc.x(1); qc.h([0, 1]); qc.cx(0, 1); qc.h(0); qc.measure(0, 0)
    elif choice == 'grover2':
        qc = grover(2, '11', 1)
    elif choice == 'grover3':
        qc = grover(3, '101', 2)
    return qc


qc = build(CHOICE)
print(qc.draw())

# ── 第 3 格：③ 轉譯到一顆假想的晶片，比較兩種最佳化等級 ─────────────────
from qiskit import transpile
from qiskit.transpiler import CouplingMap

BASIS = ['rz', 'sx', 'x', 'cx']             # 假想晶片的原生閘
CHIP = CouplingMap.from_line(5)              # 直線排列的 5 顆位元，只有相鄰的能做兩位元閘
LEVELS = (0, 3)                              # 0 = 不最佳化；3 = 最用力最佳化
SEED_T = 2026                                # 轉譯也有亂數，固定下來才能重現
compiled = {lv: transpile(qc, basis_gates=BASIS, coupling_map=CHIP, optimization_level=lv, seed_transpiler=SEED_T)
            for lv in LEVELS}


def summary(t):
    ops = t.count_ops()
    return {'深度': t.depth(), 'sx+x': ops.get('sx', 0) + ops.get('x', 0), 'cx': ops.get('cx', 0), 'rz': ops.get('rz', 0)}


for lv, t in compiled.items():
    print(f'最佳化等級 {lv}：', summary(t))

# ── 第 4 格：④ 執行：理想模擬器 vs 加上雜訊模型 ──────────────────────────
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

P1, P2, PR = 0.01, 0.01, 0.03                # 假設值：單位元閘 1%、受控反閘 1%、讀取 3%（rz 是虛擬 Z，不加雜訊）
noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(P1, 1), ['sx', 'x'])
noise.add_all_qubit_quantum_error(depolarizing_error(P2, 2), ['cx'])
noise.add_all_qubit_readout_error(ReadoutError([[1 - PR, PR], [PR, 1 - PR]]))
ideal_sim = AerSimulator()
noisy_sim = AerSimulator(noise_model=noise)
SHOTS, SEED = 1024, 2026


def run(sim, t, seed=SEED):
    counts = sim.run(t, shots=SHOTS, seed_simulator=seed).result().get_counts()
    return dict(sorted(counts.items()))


results = {lv: (run(ideal_sim, t), run(noisy_sim, t)) for lv, t in compiled.items()}
for lv, (ideal, noisy) in results.items():
    print(f'等級 {lv} 理想  ', ideal)
    print(f'等級 {lv} 有雜訊', noisy)

# ── 第 5 格：⑤ 解讀：自動檢查，寫出實驗報告 ─────────────────────────────
top = {lv: max(r[0], key=r[0].get) for lv, r in results.items()}
for lv, (ideal, noisy) in results.items():
    assert sum(ideal.values()) == SHOTS and sum(noisy.values()) == SHOTS
    assert run(noisy_sim, compiled[lv]) == noisy, '同一個種子重跑，數字應該一模一樣'
    assert top[lv] in EXPECT, f'理想模擬最多的結果 {top[lv]} 和預期答案 {EXPECT} 不一樣：先檢查線路'
print('自動檢查全部通過')

VERSION = 'v1.0'
rows = ''.join(f"| {lv} | {summary(compiled[lv])['深度']} | {summary(compiled[lv])['sx+x']} | {summary(compiled[lv])['cx']} "
               f"| {results[lv][0].get(top[lv], 0)} | {results[lv][1].get(top[lv], 0)} |\n" for lv in LEVELS)
report = f"""# 模擬器實驗報告 {VERSION}：{QUESTION}

1. 問題與預期答案：{QUESTION}；預期 {EXPECT}
2. 環境：{VERSIONS}
3. 晶片假設：直線 5 顆，原生閘 {', '.join(BASIS)}；轉譯種子 {SEED_T}
4. 雜訊模型（假設值）：單位元閘 {P1:.0%}、受控反閘 {P2:.0%}、讀取 {PR:.0%}；rz 不加雜訊
5. 執行：shots = {SHOTS}，模擬種子 = {SEED}

| 最佳化等級 | 深度 | sx＋x 個數 | cx 個數 | 理想：{top[LEVELS[0]]} 次數 | 有雜訊：{top[LEVELS[0]]} 次數 |
|---|---|---|---|---|---|
{rows}
6. 我的解讀（自己寫）：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
7. 限制：雜訊模型是假設，不代表任何一台真機；換種子、換版本，數字會變。
"""
name = f'report_{CHOICE}_{VERSION}.md'
open(name, 'w', encoding='utf-8').write(report)
print(report)
print('報告存成', name)

# 影片中的結果（CHOICE = 'grover2'，種子 2026）：
#   等級 0：深度 26、sx＋x 14 個、cx 2 個；有雜訊 {'00': 25, '01': 67, '10': 66, '11': 866}
#   等級 3：深度 12、sx＋x 6 個、cx 2 個；有雜訊 {'00': 18, '01': 46, '10': 45, '11': 915}
#   改成 'grover3'：等級 0 cx 51 個、101 有 458 次；等級 3 cx 39 個、101 有 550 次
'''


def notebook(program):
    """把程式依「# ── 第 k 格」切成筆記本的程式格，前面各加一格說明。"""
    head, *parts = re.split(r'\n(?=# ── 第 )', program)
    title = ('# Q064 模組專題：在模擬器跑我的線路（Release 任務）\n\n'
             '父子科技學院 量子電腦學程。只用本機模擬器，不需要帳號。\n\n'
             '**操作檢查表**：① 定義問題 → ② 線路 → ③ 轉譯 → ④ 執行 → ⑤ 解讀（寫報告）\n\n'
             '**重現測試**：審查員只拿著 `report_…_v1.0.md`，在自己的電腦重跑；數字一模一樣才發布。\n\n'
             '| 版本 | 日期 | 改了什麼 |\n|---|---|---|\n| v1.0 | | 範例：兩顆 Grover |\n| v1.1 | | 我挑的題目＋比較等級 0、3 |')
    cells = [{'cell_type': 'markdown', 'metadata': {}, 'source': title.splitlines(True)}]
    for p in parts:
        first, _, body = p.partition('\n')
        note = first.strip('# ─').strip()
        cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': [f'## {note}']})
        cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [],
                      'source': body.strip('\n').splitlines(True)})
    nb = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                                       'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 5}
    return json.dumps(nb, ensure_ascii=False, indent=1) + '\n'


NOTEBOOK = notebook(PROGRAM)

STAGES = [('① 定義問題', '寫下要問什麼、預期答案是什麼'), ('② 線路', '畫出線路，印出 qc.draw()'),
          ('③ 轉譯', '等級 0 和等級 3：深度、sx＋x、cx 各幾個'), ('④ 執行', 'shots 1024、種子 2026、理想與有雜訊各跑一次'),
          ('⑤ 解讀', '和預期比較，自動檢查通過，寫進報告')]


def table_md(key):
    ans, rows = RUNS[key]
    return ('| 最佳化等級 | 深度 | sx＋x | cx | 理想：' + ans + ' 次數 | 有雜訊：' + ans + ' 次數 |\n|---|---|---|---|---|---|\n'
            + ''.join(f'| {lv} | {d} | {s} | {c} | {i} | {n} |\n' for lv, (d, s, c, i, n) in rows.items()))


FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q064：模組專題——在模擬器跑我的線路（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂是 QM04 的模組專題：孩子自己挑一個學過的演算法，
照操作檢查表「定義問題 → 線路 → 轉譯 → 執行 → 解讀」在本機模擬器跑完整流程，加上雜訊模型、比較兩種轉譯最佳化等級，
最後寫成一份別人也能重現的實驗報告，通過「重現測試」才算發布 v1.0。

## 課前準備（約 20 分鐘，不需要帳號）

1. 安裝 Python 3.10 以上，接著在終端機輸入：`pip install qiskit qiskit-aer`（想用筆記本再加 `jupyter`）。
2. 先自己跑一次：`python my_circuit_release.py`。應該看到版本號、線路圖、等級 0 和等級 3 的閘數、四行結果、「自動檢查全部通過」，
   資料夾裡多出 `report_grover2_v1.0.md`。
   - 本程式在 {TESTED} 測試過。版本不同時，轉譯後的閘數和有雜訊的數字可能不一樣；這正是報告要寫版本號的原因。
3. 列印 `02_列印包_Release任務.pdf`（A4，共 4 頁）；準備一個印章當「v1.0 發布章」。讀一遍 `04_解答.md`。
4. 在另一台電腦（或另一個資料夾）也裝好同版本，等一下做重現測試用。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 照五關走一次範例：兩顆 Grover 找 11 | 影片第 4–8 段、列印包第 1 頁 |
| 25–65 | 孩子挑題目（CHOICE），加雜訊跑完整流程，寫報告 v1.0；爸爸做重現測試 | 筆記本、`01_操作步驟.md`、列印包第 2、4 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：比較等級 0 與等級 3（建議三顆 Grover），說明差異，更新成 v1.1 | 列印包第 3 頁、`03_實驗紀錄.csv` |
| 105–115 | 孩子教爸爸：五關、為什麼閘少錯就少、雜訊模型是假設 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 重現審查員（爸爸）的原則

- 只拿報告，不看孩子的螢幕：照報告上的版本、題目、晶片、雜訊參數、shots、兩個種子重跑。
- 數字一模一樣才蓋章；不一樣就一起找原因（版本不同？種子沒寫？改了參數沒記？），修好報告再送一次。
- 有雜訊的數字每換一個種子就會變（兩顆 Grover 等級 0 換 5 個種子：862～890 次），不要求和影片一樣；固定種子 2026 時才會一樣。

## 誠實說明

- 雜訊模型（單位元閘與 cx 各 1%、讀取 3%）和直線 5 顆的晶片都是教學用的假設，不代表任何一台真機。
- 等級 3 不保證每條線路都最好：兩顆 Grover 的等級 1 在這個版本實跑 922 次，比等級 3 的 915 次還多一點。說明差異時可以拿來討論。
- 只用本機模擬器；不連雲端、不需要帳號。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：照五關走範例，再挑自己的題目（約 40 分鐘）

1. 開啟 `my_circuit_release.ipynb`，選「全部重新執行」（或執行 `python my_circuit_release.py`）。
2. 第 0 格：把版本號抄到列印包第 2 頁。
3. 第 1 格 ① 定義問題：先用預設的 `CHOICE = 'grover2'` 跑一次，對照影片；接著改成自己挑的題目：
   `'bell'`、`'ghz3'`、`'deutsch'`、`'grover2'`、`'grover3'`，在列印包第 1 頁寫下問題和預期答案。
4. 第 2 格 ② 線路：看印出來的線路圖，說出每一段在做什麼。
5. 第 3 格 ③ 轉譯：抄下等級 0、等級 3 的深度、sx＋x、cx 個數。
6. 第 4 格 ④ 執行：看理想與有雜訊四行結果。
7. 第 5 格 ⑤ 解讀：自動檢查通過後，資料夾多出 `report_<題目>_v1.0.md`；打開它，把第 6 項「我的解讀」寫完。
8. 重現測試：把報告交給爸爸，爸爸只看報告在自己的電腦重跑；數字一樣就蓋 v1.0 發布章。

## 下半場：比較兩種最佳化等級（約 30 分鐘）

1. 把 `CHOICE` 改成 `'grover3'`（三顆、八個抽屜找 101、兩輪），再跑一次。
2. 在列印包第 3 頁填等級 0、等級 3 的深度、cx 個數、有雜訊時 101 的次數。
3. 說明差異：哪一個等級的閘比較少？為什麼閘少，答案出現的次數就多？
4. 想多看一點：把第 3 格的 `LEVELS = (0, 3)` 改成 `(0, 1, 2, 3)`；或把 `SEED = 2026` 換成別的數字（記得改回來才能和影片比對）。
5. 在第一格的更新紀錄寫上 v1.1 改了什麼，報告檔名改成 v1.1，再請爸爸重現一次。

## 沒有電腦的備案

打開 `animations/operation.html#circuit`（選「Grover 搜尋（2 位元，找 |11⟩）」、按「單步 ▶」八次、打開「加入雜訊」）與
`animations/basic-circuits.html#grover`（位元數改成 3 顆，看「101 94.5%」）。動畫的雜訊算法和筆記本不同，數字不會一樣。
''',

'my_circuit_release.py': PROGRAM,
'my_circuit_release.ipynb': NOTEBOOK,

'04_解答.md': '# 解答（爸爸用）\n\n'
  f'## 影片中的實跑（{TESTED}、shots=1024、seed_simulator=2026、seed_transpiler=2026）\n\n'
  '假想晶片：直線 5 顆，原生閘 rz、sx、x、cx；雜訊：sx、x、cx 各 1%、讀取 3%；rz 不加雜訊。\n\n'
  + ''.join(f'### {k}\n\n' + table_md(k) + '\n' for k in RUNS)
  + "兩顆 Grover 有雜訊的完整結果：等級 0 {'00': 25, '01': 67, '10': 66, '11': 866}；等級 3 {'00': 18, '01': 46, '10': 45, '11': 915}。\n\n"
  '換種子 1–5（兩顆 Grover 有雜訊時 11 的次數）：等級 0 ' + '、'.join(map(str, SEEDS_G2[0])) + '；等級 3 ' + '、'.join(map(str, SEEDS_G2[3]))
  + '；等級 3 每次多 39～47 次。\n\n'
  '用 20 萬次密度矩陣模擬估計的成功率：兩顆 Grover 等級 0 約 85.5%、等級 3 約 89.6%；三顆 Grover 約 46.3%、54.9%；'
  '三顆在理想時本來就只有 94.5%（sin²(5θ)，θ = asin(1/√8)）。\n\n'
  '## 常見問題\n\n'
  '- 為什麼 Bell、GHZ 兩種等級一模一樣？線路太短，沒有可以合併的閘；最佳化不是每次都有效果。\n'
  '- 為什麼等級 3 的 rz 也變少？相鄰的單位元閘被合併成更少的旋轉；rz 是虛擬 Z（第五十三堂），這裡不加雜訊，所以真正影響結果的是 sx、x、cx 的個數。\n'
  '- 等級越高一定越好嗎？不一定。兩顆 Grover 的等級 1 實跑 922 次，比等級 3 的 915 次多；三顆時等級 1 也有 564 次。報告要寫清楚比了哪兩個等級。\n'
  '- 重現測試數字不一樣？先對照報告第 2 項的版本號，再檢查兩個種子和 CHOICE；套件改版時轉譯結果可能不同。\n'
  '- 位元字串怎麼讀？最右邊是 q0（第一顆）。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#circuit`（場景 6：量子線路）

- 範例選「Grover 搜尋（2 位元，找 |11⟩）」，按「單步 ▶」八次走到量測欄：右下直方圖只有 11 一根，頂到青色的理想線。
- 「加入雜訊（每閘 1%、讀取 3%）」：打開後 11 變矮、00、01、10 冒出矮柱。算法和筆記本的雜訊模型不同，只看趨勢。

## `animations/basic-circuits.html#deutsch`（範例 6：Deutsch 演算法）

- 「下一步 ▶」按四次、「量測 1,000 次」：f(x)=x 時 q0 全是 1，右邊寫「→ 平衡函數」；黑盒改成 f(x)=1 再量，全是 0、「→ 常數函數」。

## `animations/basic-circuits.html#grover`（範例 8：Grover 搜尋）

- 位元數改成「3 顆（N = 8）」：畫面停在第 2 輪擴散，說明寫「答案的機率升到 94.5%」。
- 「重複輪數」改成 3 輪：轉過頭，答案的機率反而下降。最下面「Qiskit 程式碼」可以和筆記本的 grover() 對照。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放（operation.html）；左右方向鍵換步（basic-circuits.html）。
''',
}

SHEET_HEADER = ['版本', '題目（CHOICE）', '最佳化等級', '雜訊', '模擬種子', '轉譯種子', '深度', 'sx＋x', 'cx', '答案次數', '我的觀察']
SHEET_ROWS = ([['v1.0', 'grover2', str(lv), z, '2026', '2026'] for lv in (0, 3) for z in ('無', '有')]
              + [['v1.0', '（自己挑）', str(lv), '有', '2026', '2026'] for lv in (0, 3)]
              + [['v1.1', 'grover3', str(lv), '有', '2026', '2026'] for lv in (0, 3)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.stamp{border:1.6pt dashed #0b2540;border-radius:50%;width:36mm;height:36mm;display:flex;align-items:center;justify-content:center;text-align:center;
font-size:12pt;color:#4a6a88;margin:3mm auto 0}.two{display:grid;grid-template-columns:1fr 1fr;gap:6mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}
table.stg td{height:11mm;font-size:11.5pt}'''


def html():
    stg = ''.join(f'<tr><td>□ {a}</td><td>{b}</td><td></td></tr>' for a, b in STAGES)
    pages = [
        '<h2>操作檢查表：五關</h2><p class="lead">一關一關往下走，每一關都在右欄留一句紀錄。先用範例（兩顆 Grover 找 11）走一次，再換自己的題目。</p>'
        '<div class="box"><p>我挑的題目（CHOICE）：＿＿＿＿＿＿＿＿　它是第幾堂學的？＿＿＿＿</p>'
        '<p>我要問的問題：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>預期答案（理想模擬應該得到）：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>'
        f'<table class="rec stg" style="margin-top:4mm"><tr><th>關卡</th><th>要做的事</th><th>我的紀錄</th></tr>{stg}</table>'
        '<p class="note" style="margin-top:3mm">可以選的題目：bell（第十堂）、ghz3（第五十七堂）、deutsch（第十二堂）、grover2、grover3（第十三堂）。</p>',
        '<h2>模擬器實驗報告單 v1.0</h2><p class="lead">程式會自動寫出 report_…_v1.0.md；這張紙是給審查員看的紙本版。</p>'
        '<div class="box"><p>1. 問題與預期答案：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>2. 環境：Python＿＿＿＿　qiskit＿＿＿＿　qiskit-aer＿＿＿＿</p>'
        '<p>3. 晶片假設：直線＿＿顆，原生閘＿＿＿＿＿＿＿＿；轉譯種子＿＿＿＿</p>'
        '<p>4. 雜訊模型（假設值）：單位元閘＿＿%、cx＿＿%、讀取＿＿%</p>'
        '<p>5. 執行：shots＿＿＿＿　模擬種子＿＿＿＿</p></div>'
        '<table class="rec" style="margin-top:4mm"><tr><th>最佳化等級</th><th>深度</th><th>sx＋x</th><th>cx</th><th>理想：答案次數</th><th>有雜訊：答案次數</th></tr>'
        '<tr><td>0</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>3</td><td></td><td></td><td></td><td></td><td></td></tr></table>'
        '<p style="margin-top:4mm">6. 我的解讀：理想結果代表＿＿＿＿＿＿＿＿＿＿；少掉的次數代表＿＿＿＿＿＿＿＿＿＿</p><div class="line"></div>'
        '<p>7. 限制：雜訊模型是假設，不代表任何一台真機；＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：比較兩種最佳化等級（v1.1）</h2><p class="lead">把 CHOICE 改成 grover3（三顆、八個抽屜找 101、兩輪），比較等級 0 和等級 3。</p>'
        '<table class="rec"><tr><th>題目</th><th>等級</th><th>深度</th><th>cx 個數</th><th>sx＋x 個數</th><th>有雜訊：答案次數</th></tr>'
        + ''.join(f'<tr><td>{k}</td><td>{lv}</td><td></td><td></td><td></td><td></td></tr>' for k in ('grover2', 'grover3') for lv in (0, 3)) + '</table>'
        '<pre class="code">CHOICE = \'grover3\'      # 改造區\nLEVELS = (0, 3)          # 想多看：(0, 1, 2, 3)\nSEED_T = 2026            # 轉譯種子</pre>'
        '<p>哪一個等級的閘比較少？＿＿＿＿＿＿　答案出現的次數差多少？＿＿＿＿＿＿</p>'
        '<p class="note">說明差異（為什麼閘少，答案就多？兩顆和三顆，哪一個差得多？）：</p><div class="line"></div><div class="line"></div>',
        '<h2>重現測試與說明卡</h2><div class="two"><div class="box"><h3>重現審查員（爸爸）</h3>'
        '<ul class="chk"><li>只看報告，照版本、題目、參數、兩個種子重跑</li><li>理想結果一模一樣</li><li>有雜訊結果一模一樣</li>'
        '<li>報告寫了雜訊參數和「這是假設」</li></ul><p>重跑的數字：＿＿＿＿＿＿＿＿</p></div>'
        '<div><div class="stamp">v1.0<br>發布章</div><p class="note" style="text-align:center">四項都打勾才蓋章</p></div></div>'
        '<div class="box" style="margin-top:4mm"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　最新版本：v＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>更新紀錄　v1.0：＿＿＿＿＿＿＿＿＿＿　v1.1：＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出五關：定義問題、線路、轉譯、執行、解讀</li><li>解釋為什麼等級 3 的結果比較好（閘少，出錯機會少）</li>'
        '<li>指出一個限制：雜訊模型是假設，要寫清楚用了哪些參數</li><li>替報告取名字、寫上版本號存檔</li></ul></div>',
    ]
    return printpack.document('Q064 Release 任務 列印包', '父子科技學院 量子電腦學程 Q064｜模組專題：在模擬器跑我的線路', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q064-simulator-project', folder='Q064_模組專題_在模擬器跑我的線路', files=FILES,
        sheet=('03_實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_Release任務.pdf', pack_pages=4,
        pack_needles=('操作檢查表', '實驗報告單', '最佳化等級', '重現測試', '最後一關'),
        authoring_dir=XINEW / 'authoring/q064', episode_dir='specials/q064-simulator-project',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'pip install qiskit qiskit-aer（jupyter 選用）',
               'program': 'my_circuit_release.py', 'notebook': 'my_circuit_release.ipynb', 'testedWith': TESTED,
               'recordedRun': {'seed': 2026, 'seedTranspiler': 2026, 'shots': 1024,
                               'grover2Noisy': {str(k): v for k, v in GROVER2_NOISY.items()},
                               'successCounts': {k: {str(lv): r[4] for lv, r in v[1].items()} for k, v in RUNS.items()}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q064/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

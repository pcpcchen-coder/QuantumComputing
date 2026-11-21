"""Q115 課堂教材：實驗紀錄表（有 Z／沒有 Z）、路徑加總表、錯誤示範與挑戰、可執行的 paths.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#interference 與 operation.html#interference；paths.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 paths.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q115/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，random.Random(1115)（固定種子；這兩條線路的機率是 100%／0%，次數本來就不會變）
RUN_OUTPUT = '''一、逐步看振幅（有 Z）
  起點          |0⟩ +1.000（100%）  |1⟩ 0（0%）
  H           |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  H → Z       |0⟩ +0.707（50%）  |1⟩ −0.707（50%）
  H → Z → H   |0⟩ 0（0%）  |1⟩ +1.000（100%）
二、對照組（拿掉 Z）
  起點          |0⟩ +1.000（100%）  |1⟩ 0（0%）
  H           |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  H → H       |0⟩ +1.000（100%）  |1⟩ 0（0%）
三、路徑加總表（同一個結果的兩條路徑先相加，再平方）
  H → Z → H（最後一個 H 之前：|0⟩ +0.707、|1⟩ −0.707）
    到 |0⟩  經由 0：+0.500  經由 1：−0.500  總和 0  機率 0%
    到 |1⟩  經由 0：+0.500  經由 1：+0.500  總和 +1.000  機率 100%
  H → H（最後一個 H 之前：|0⟩ +0.707、|1⟩ +0.707）
    到 |0⟩  經由 0：+0.500  經由 1：+0.500  總和 +1.000  機率 100%
    到 |1⟩  經由 0：+0.500  經由 1：−0.500  總和 0  機率 0%
四、錯誤示範：把機率相加
  每條路徑的機率 0.25，兩條相加 0.50：到 |0⟩、到 |1⟩ 都是 50%，算不出抵消
五、各量測 1000 次
  H → Z → H   0 → 0 次  1 → 1000 次
  H → H       0 → 1000 次  1 → 0 次
六、改造區
  H → X → H   |0⟩ +1.000（100%）  |1⟩ 0（0%）
  H → X → H（最後一個 H 之前：|0⟩ +0.707、|1⟩ +0.707）
    到 |0⟩  經由 0：+0.500  經由 1：+0.500  總和 +1.000  機率 100%
    到 |1⟩  經由 0：+0.500  經由 1：−0.500  總和 0  機率 0%
'''

# 製作代理實跑紀錄：qiskit 2.6.2，StatevectorSampler(seed=2026)，shots=1000
QISKIT_OUTPUT = '''H‑Z‑H 振幅 [0.0, 1.0] 機率 {'1': 1.0} 量測 1000 次 {'1': 1000}
H‑H   振幅 [1.0, 0.0] 機率 {'0': 1.0} 量測 1000 次 {'0': 1000}
H‑Z‑H 和 X 是同一個運算嗎？ True
H‑H 和「什麼都不做」是同一個運算嗎？ True
   ┌───┐┌───┐┌───┐
q: ┤ H ├┤ Z ├┤ H ├
   └───┘└───┘└───┘
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q115：範例 2 干涉——H‑Z‑H = X（純 Python，不需安裝任何套件）

執行：  python paths.py
它用一個很小的一顆位元模擬器（只認得 H、X、Z 三種閘），印出：
  一、逐步看振幅：H → Z → H，每一步 |0⟩、|1⟩ 的振幅與機率
  二、對照組：拿掉 Z，只剩 H → H
  三、路徑加總表：最後一個 H 把「經由 0」和「經由 1」兩條路徑的振幅加起來
  四、錯誤示範：如果把機率相加，會得到什麼
  五、各量測 1000 次（固定的亂數種子；這兩條線路的機率是 100%／0%，所以次數不會變）
  六、改造區：自己排一條線路，先預測，再執行
"""
import random
from math import sqrt

R2 = 1 / sqrt(2)


def run(gates):
    """一顆位元從 |0⟩ 出發，由左往右依序做 gates（'h'、'x'、'z'），回傳 [|0⟩ 的振幅, |1⟩ 的振幅]"""
    a, b = 1.0, 0.0
    for g in gates:
        if g == 'h':
            a, b = (a + b) * R2, (a - b) * R2
        elif g == 'x':
            a, b = b, a
        elif g == 'z':
            b = -b
        else:
            raise ValueError('只認得 h、x、z：' + g)
    return [a, b]


def num(v):
    return '0' if abs(v) < 1e-9 else ('+' if v > 0 else '−') + f'{abs(v):.3f}'


def name(gates):
    return ' → '.join(g.upper() for g in gates) or '起點'


def show(gates):
    s = run(gates)
    print(f'  {name(gates):<12}' + '  '.join(f'|{i}⟩ {num(v)}（{v * v * 100:.0f}%）' for i, v in enumerate(s)))


def steps(gates):
    for k in range(len(gates) + 1):
        show(gates[:k])


# H 的係數：從 |j⟩ 到 |i⟩ 乘上 HC[i][j]（只有 |1⟩ → |1⟩ 是負的）
HC = [[R2, R2], [R2, -R2]]


def path_table(gates):
    """最後一個閘必須是 H：把它之前的振幅，沿兩條路徑乘上 H 的係數，再加總"""
    assert gates[-1] == 'h'
    before = run(gates[:-1])
    print(f'  {name(gates)}（最後一個 H 之前：|0⟩ {num(before[0])}、|1⟩ {num(before[1])}）')
    for i in (0, 1):
        via = [before[j] * HC[i][j] for j in (0, 1)]
        total = via[0] + via[1]
        print(f'    到 |{i}⟩  經由 0：{num(via[0])}  經由 1：{num(via[1])}  總和 {num(total)}  機率 {total * total * 100:.0f}%')


def shots(gates, n, rng):
    """量測 n 次：每次以機率 振幅² 得到 0 或 1，回傳 [0 的次數, 1 的次數]"""
    p0 = run(gates)[0] ** 2
    c0 = sum(rng.random() < p0 for _ in range(n))
    return [c0, n - c0]


HZH, HH = ['h', 'z', 'h'], ['h', 'h']

if __name__ == '__main__':
    rng = random.Random(1115)
    print('一、逐步看振幅（有 Z）')
    steps(HZH)
    print('二、對照組（拿掉 Z）')
    steps(HH)
    print('三、路徑加總表（同一個結果的兩條路徑先相加，再平方）')
    path_table(HZH)
    path_table(HH)
    print('四、錯誤示範：把機率相加')
    p = (R2 * R2) ** 2
    print(f'  每條路徑的機率 {p:.2f}，兩條相加 {p + p:.2f}：到 |0⟩、到 |1⟩ 都是 50%，算不出抵消')
    print('五、各量測 1000 次')
    for g in (HZH, HH):
        c = shots(g, 1000, rng)
        print(f'  {name(g):<12}0 → {c[0]} 次  1 → {c[1]} 次')

    # 六、改造區：先預測，再執行。閘寫成 'h'、'x'、'z'，由左往右排
    MY_CIRCUITS = [['h', 'x', 'h']]
    print('六、改造區')
    for g in MY_CIRCUITS:
        show(g)
        if g and g[-1] == 'h':
            path_table(g)
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q115：用本機 Qiskit 重現 H‑Z‑H = X（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Operator, Statevector


def report(name, qc):
    sv = Statevector.from_instruction(qc)
    m = qc.copy()
    m.measure_all()
    counts = StatevectorSampler(seed=2026).run([m], shots=1000).result()[0].data.meas.get_counts()
    print(name, '振幅', [round(float(a.real), 3) + 0.0 for a in sv.data],
          '機率', {str(k): round(float(v), 3) for k, v in sv.probabilities_dict().items() if v > 1e-9},
          '量測 1000 次', dict(sorted(counts.items())))


hzh = QuantumCircuit(1)
hzh.h(0)                     # 第一個哈達瑪閘：做出疊加
hzh.z(0)                     # 相位翻轉閘：只給 |1⟩ 加負號
hzh.h(0)                     # 第二個哈達瑪閘：干涉
hh = QuantumCircuit(1)
hh.h(0)
hh.h(0)                      # 對照組：拿掉 Z
report('H‑Z‑H', hzh)
report('H‑H  ', hh)

x = QuantumCircuit(1)
x.x(0)
print('H‑Z‑H 和 X 是同一個運算嗎？', Operator(hzh).equiv(Operator(x)))
print('H‑H 和「什麼都不做」是同一個運算嗎？', Operator(hh).equiv(Operator(QuantumCircuit(1))))
print(hzh.draw())
'''

TABLE = [  # (線路, 結果, 經由 0, 經由 1, 總和, 機率, 干涉)
    ('H → Z → H', '|0⟩', '+½', '−½', '0', '0%', '破壞性（抵消）'),
    ('H → Z → H', '|1⟩', '+½', '+½', '1', '100%', '建設性（加強）'),
    ('H → H', '|0⟩', '+½', '+½', '1', '100%', '建設性（加強）'),
    ('H → H', '|1⟩', '+½', '−½', '0', '0%', '破壞性（抵消）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q115：範例 2 干涉——H‑Z‑H = X（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的範例 2。
上一課（Q114）發現 |+⟩ 和 |−⟩ 量起來一樣，只差 |1⟩ 振幅的正負號；今天在兩個 H 中間夾一個 Z，讓這個正負號變成看得到的結果。
核心一句話：**干涉發生在振幅，不是機率。** H‑Z‑H 100% 量到 1；拿掉 Z，H‑H 100% 量到 0。

## 路徑加總表（作品的答案）

最後一個 H 把「經由 0」和「經由 1」兩條路徑的振幅加起來（H 的係數只有 |1⟩ → |1⟩ 是負的）：

| 線路 | 結果 | 經由 0 | 經由 1 | 總和 | 機率 | 干涉 |
|---|---|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in TABLE) + '''
最下面再留一列「量測 1,000 次」：H‑Z‑H 全部是 1、H‑H 全部是 0（機率是 100%／0%，所以每次都一樣）。

## 影片的念法

H 念「哈達瑪閘」、X「翻轉閘」、Z「相位翻轉閘」；|+⟩「正號疊加態」、|−⟩「負號疊加態」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 對照簡報第 7–9 頁：範例 2 線路、振幅逐步看、路徑加總 | 簡報 basic-circuits.pptx p7–9 |
| 25–65 | 在 basic-circuits.html#interference 先選「有 Z」逐步播放三步、量測 1,000 次；再選「沒有 Z」從起點走兩步、量測 1,000 次；填實驗紀錄表 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子用路徑加總表解釋為什麼會抵消，跑 `paths.py` 核對；挑戰 H‑X‑H | 列印包第 2、3 頁、`03_實驗與改造紀錄.csv` |
| 105–115 | 孩子教爸爸：結果、原因、容易錯的地方 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#interference`：上方「中間的閘」切換「有 Z／沒有 Z」，按「⏮ 起點」「下一步 ▶」與「量測 1,000 次」。
- 選用：開 `operation.html#interference`（場景 8），按「單一量子位元：兩條路徑」，把「A：相位 φ」滑桿放在 0° 和 180° 比較；0° 等於沒有 Z、180° 等於有 Z。
- 打開簡報 `slides/output/basic-circuits.pptx` 第 7–9 頁（課綱寫 p7–9，頁碼無誤）。
- 列印 `02_列印包_路徑加總表.pdf`（A4，共 4 頁），準備兩種顏色的筆（一正一負）。
- 有 Python 的電腦先跑一次 `python paths.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 本課的振幅都是實數，正負號就是 0° 或 180° 的相位差；一般的複數相位不展開。
- 「每條路徑的振幅」是把最後一個 H 之前的振幅乘上 H 的係數（±1/√2），所以是 ±½；這是簡報第 9 頁的算法。
- 「中途偷看走哪一條路，干涉消失、變回 50/50」來自 operation.html#interference 的說明與維基百科 Probability amplitude 的雙狹縫敘述；paths.py 沒有模擬中途量測。
- Bloch 球和振幅柱子是模擬器才看得到的；真實的量子電腦只給量測結果。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：有 Z、沒有 Z 各做一次（約 40 分鐘）

1. 先在列印包第 1 頁寫預測：H‑Z‑H 量 1,000 次會得到什麼？拿掉 Z 呢？
2. 打開 `animations/basic-circuits.html#interference`（範例 2 干涉）。上方「中間的閘」選「有 Z」（預設）。
3. 按「下一步 ▶」：做完第一個 H，兩根柱子都是朝上的藍色 +0.707、各 50%；右邊 Bloch 球的橘色箭頭從北極倒到赤道。
4. 再按「下一步 ▶」：做完 Z，|1⟩ 柱子翻到下面變橘色 −0.707，下面仍是 50%；箭頭沿著赤道轉到另一邊。|ψ⟩ = (|0⟩ − |1⟩) / √2。
5. 再按「下一步 ▶」：做完第二個 H，|0⟩ 柱子變成 0，|1⟩ 柱子 +1.000、100%；箭頭到南極；|ψ⟩ = |1⟩。
6. 按「量測 1,000 次」：只有「1」一列，1000 次（100.0%）。把每一步寫進實驗紀錄表。
7. 「中間的閘」改選「沒有 Z」：頁面會直接跳到最後一步。先按「⏮ 起點」，再按兩次「下一步 ▶」：第二個 H 之後 |0⟩ 柱子 +1.000，箭頭回到北極。
8. 按「量測 1,000 次」：只有「0」一列，1000 次。兩組並排比較：只改了哪一個變因？結果差多少？

## 選用：三維動畫的兩條路徑

1. 開 `animations/operation.html#interference`，按「單一量子位元：兩條路徑」。
2. 「A：相位 φ」放 0°（等於沒有 Z）：右下「結果 |1⟩」的藍、橙箭頭一正一反，P(1) = 0.00。
3. 推到 180°（等於有 Z）：右上「結果 |0⟩」的兩支箭頭抵消，P(0) = 0.00；右下接成一支白箭頭，P(1) = 1.00。
4. 按「A：中途偵測路徑（破壞干涉）」：兩個結果都變成 0.50，這就是「把機率相加」的答案。

## 下半場：用路徑加總表解釋抵消（約 30 分鐘）

1. 不看動畫，在列印包第 2 頁填兩組的路徑加總表：最後一個 H 之前的兩個振幅各乘 ±1/√2，同一個結果的兩條路徑相加，再平方。
2. 執行 `python paths.py`，對照第三段「路徑加總表」。
3. 第 3 頁的錯誤示範：只把機率相加（¼ + ¼），為什麼算不出 0？
4. 挑戰：把 `MY_CIRCUITS` 換成你的線路，例如 `['h', 'x', 'h']`（中間換成翻轉閘），先預測再執行。
5. 有裝 Qiskit 的話，跑 `qiskit_check.py`，看「H‑Z‑H 和 X 是同一個運算嗎？」印出 True。
''',

'paths.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## paths.py 實跑輸出（Python 3.13.18，random.Random(1115)）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- Z 做完之後量測，看得出差別嗎？看不出來：|1⟩ 的振幅變成 −0.707，平方後還是 50%。\n'
  '- 為什麼 H‑Z‑H 會 100% 是 1？最後一個 H 把兩條路徑混合：到 |0⟩ 是 (+½) + (−½) = 0，到 |1⟩ 是 (+½) + (+½) = 1。\n'
  '- 為什麼「經由 1 到 |1⟩」是 +½？Z 之後 |1⟩ 的振幅是 −0.707，H 從 |1⟩ 到 |1⟩ 的係數也是負的（−0.707），負負得正。\n'
  '- 拿掉 Z 呢？H‑H 等於什麼都沒做：到 |0⟩ 是 ½ + ½ = 1，到 |1⟩ 是 ½ − ½ = 0，100% 是 0。\n'
  '- 為什麼不能把機率相加？每條路徑的機率是 ¼，兩條相加永遠是 ½，算不出 0；會互相抵消的是有正負號的振幅。\n'
  '- 挑戰 H‑X‑H：X 把 |+⟩ 的兩個振幅對調，還是 +0.707、+0.707，所以最後回到 |0⟩，100% 是 0（H·X·H = Z，作用在 |0⟩ 上不改變它）。\n'
  '- 下一課 Q116：範例 3 Bell 態——四種糾纏。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html#interference`（範例 2 干涉）

- 上方「中間的閘」：有 Z（預設，三步：第一個 H、Z 閘、第二個 H）或沒有 Z（兩步）。換選項時頁面停在最後一步並清除量測。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」：橘色虛線標出目前做到哪一格，還沒做的閘是淡色。
- 「振幅與機率」：圖例「正振幅」藍、「負振幅」橘；柱子下面寫振幅和百分比；右邊 Bloch 球（軸標 |0⟩、|1⟩、+x、−x、+y），橘色箭頭；下方 |ψ⟩。
- 「量測 1 次」「量測 1,000 次」「清除」：灰色底是理論機率，綠色是實際次數；量測會累加，按「清除」才歸零。

## `animations/operation.html#interference`（場景 8：加速的關鍵——振幅會互相抵消）

- 「單一量子位元：兩條路徑」：起點 |0⟩ 經 H 分成上（|0⟩）下（|1⟩）兩條路，下面那條路上的紫色方塊是「相位 φ」，第二個 H 再合到「結果 |0⟩」「結果 |1⟩」。
- 藍 = 經由 |0⟩ 的貢獻、橙 = 經由 |1⟩ 的貢獻、白 = 總和；金色標籤 P(0)、P(1)；右下小圖是 P(0) 對 φ 的曲線。
- 滑桿「A：相位 φ」0°–360°；「A：自動掃描 φ」；「A：中途偵測路徑（破壞干涉）」。
- 「3 位元：8 條路徑（Deutsch–Jozsa）」是後面課程的內容。

## 操作

basic-circuits.html：左右方向鍵 上一步／下一步；空白鍵 播放；點電路上的閘可以直接跳到那一步。
''',
}

SHEET_HEADER = ['線路', '步驟', '|0⟩ 振幅', '|1⟩ 振幅', '機率', '量測 1000 次', '我的預測', '一樣嗎', '備註']
SHEET_ROWS = [['範例：H → Z → H', '第 2 步（Z 之後）', '+0.707', '−0.707', '50%／50%', '—', '', '', '這一步量不出差別'],
              ['範例：H → Z → H', '第 3 步（第二個 H）', '0', '+1.000', '0%／100%', '1 → 1000 次', '', '', '到 |0⟩：+½ −½ = 0'],
              ['範例：H → H', '第 2 步（第二個 H）', '+1.000', '0', '100%／0%', '0 → 1000 次', '', '', '到 |1⟩：+½ −½ = 0'],
              ['有 Z', '', '', '', '', '', '', '', ''], ['沒有 Z', '', '', '', '', '', '', '', ''],
              ['我的改造線路', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:10mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:20%}
table.judge th{font-size:10.5pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 paths.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'paths.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    step = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td></tr>'  # noqa: E731
    pages = [
        '<h2>科學實驗紀錄表：有 Z、沒有 Z</h2><p class="lead">只改一個變因：中間的閘。先寫預測，再在 basic-circuits.html#interference 逐步播放。</p>'
        '<p>我的預測：有 Z 量 1,000 次 → ＿＿＿＿＿＿　沒有 Z → ＿＿＿＿＿＿</p>'
        '<table class="judge"><tr><th style="width:20%">有 Z</th><th>|0⟩ 振幅</th><th>|1⟩ 振幅</th><th>Bloch 箭頭在哪</th></tr>'
        + step('起點') + step('第一個 H') + step('Z') + step('第二個 H') +
        '<tr><td class="k">量測 1,000 次</td><td colspan="3">0：＿＿次　1：＿＿次</td></tr></table>'
        '<table class="judge" style="margin-top:4mm"><tr><th style="width:20%">沒有 Z</th><th>|0⟩ 振幅</th><th>|1⟩ 振幅</th><th>Bloch 箭頭在哪</th></tr>'
        + step('起點') + step('第一個 H') + step('第二個 H') +
        '<tr><td class="k">量測 1,000 次</td><td colspan="3">0：＿＿次　1：＿＿次</td></tr></table>'
        '<p>只改了一個閘，結果差在哪裡：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>作品：路徑加總表</h2><p class="lead">最後一個 H 之前的振幅 × H 的係數（±1/√2）＝每條路徑的振幅；同一個結果的兩條路徑先相加，再平方。</p>'
        '<table class="judge"><tr><th style="width:16%">線路</th><th style="width:10%">結果</th><th>經由 0</th><th>經由 1</th><th>總和</th><th>機率</th><th style="width:16%">抵消／加強</th></tr>'
        '<tr><td class="k">H → Z → H</td><td>|0⟩</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">H → Z → H</td><td>|1⟩</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">H → H</td><td>|0⟩</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">H → H</td><td>|1⟩</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">量測 1,000 次</td><td colspan="6">H‑Z‑H：＿＿＿＿＿＿　H‑H：＿＿＿＿＿＿</td></tr></table>'
        '<p class="note">提示：H 從 |0⟩ 出發到 |0⟩、|1⟩ 都乘 +1/√2；從 |1⟩ 出發到 |0⟩ 乘 +1/√2、到 |1⟩ 乘 −1/√2。</p>'
        '<p>用一句話說明：為什麼 H‑Z‑H 到 |0⟩ 會抵消？</p><div class="line"></div><div class="line"></div>',
        '<h2>錯誤示範與挑戰</h2><p class="lead">干涉發生在振幅，不是機率。</p>'
        '<table class="judge"><tr><th style="width:20%">算法</th><th>到 |0⟩</th><th>到 |1⟩</th><th style="width:22%">算得出抵消嗎</th></tr>'
        '<tr><td class="k">把機率相加</td><td>¼ + ¼ = ＿＿</td><td>¼ + ¼ = ＿＿</td><td></td></tr>'
        '<tr><td class="k">振幅先加再平方</td><td>(＿＿ + ＿＿)² = ＿＿</td><td>(＿＿ + ＿＿)² = ＿＿</td><td></td></tr></table>'
        '<p>挑戰：中間的 Z 換成 X（H → X → H），先用路徑加總表預測，再跑程式驗證。</p>'
        '<table class="judge"><tr><th style="width:20%">線路</th><th>我的預測</th><th>paths.py 結果</th><th style="width:12%">一樣嗎</th></tr>'
        '<tr><td class="k">H → X → H</td><td></td><td></td><td></td></tr><tr><td class="k">我的線路：</td><td></td><td></td><td></td></tr></table>'
        '<pre class="code"># paths.py 最下面的改造區（閘由左往右排）\n'
        'MY_CIRCUITS = [[&#39;h&#39;, &#39;x&#39;, &#39;h&#39;]]   # 改成你的線路\n'
        '# 閘的寫法：&#39;h&#39; 哈達瑪閘、&#39;x&#39; 翻轉閘、&#39;z&#39; 相位翻轉閘</pre>',
        '<h2>最後一關：教爸爸干涉</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. H‑Z‑H 和 H‑H 的結果各是什麼（不看稿）：</p><div class="line"></div>'
        '<p>2. 為什麼會抵消（用路徑加總說）：</p><div class="line"></div>'
        '<p>3. 一個容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：H‑Z‑H 100% 量到 1，所以 H·Z·H = X；拿掉 Z，100% 量到 0</li><li>說出：到 |0⟩ 的兩條路徑 +½、−½ 抵消，到 |1⟩ 的 +½、+½ 加強</li>'
        '<li>指出：干涉發生在振幅，不是機率（機率相加算不出 0）</li><li>完成路徑加總表，和 paths.py 的結果一致</li>'
        '<li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q115 路徑加總表 列印包', '父子科技學院 量子電腦學程 Q115｜範例 2：干涉——H‑Z‑H = X', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q115-hzh-interference', folder='Q115_範例2_干涉_HZH', files=FILES,
        sheet=('03_實驗與改造紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_路徑加總表.pdf', pack_pages=4,
        pack_needles=('科學實驗紀錄表', '路徑加總表', '錯誤示範', 'MY_CIRCUITS', '最後一關'),
        authoring_dir=XINEW / 'authoring/q115', episode_dir='specials/q115-hzh-interference',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；paths.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'paths.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, random seed 1115); qiskit 2.6.2',
               'recordedRun': {'hzh': {'0': '0 (0%)', '1': '+1.000 (100%)'}, 'hh': {'0': '+1.000 (100%)', '1': '0 (0%)'},
                               'pathSum': {'hzhTo0': '+0.5 + (−0.5) = 0', 'hzhTo1': '+0.5 + 0.5 = 1'},
                               'hxh': {'0': '+1.000 (100%)'},
                               'qiskitCounts': {'hzh': {'1': 1000}, 'hh': {'0': 1000}}, 'qiskitHZHequalsX': True},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q115/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q113 課堂教材：讀圖約定卡、臨摹挑戰卡、可執行的 read_order.py（純 Python）與選用的 qiskit_check.py、兩閘線路改造表、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html（#superposition、#interference、#bell）；read_order.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 read_order.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q113/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，結果固定（無亂數）
RUN_OUTPUT = '''一、約定二：位元字串裡 q0 寫在最右邊（兩顆位元，字串是 q1 q0）
  X(q0)            |01⟩ +1.000（100%）
  X(q1)            |10⟩ +1.000（100%）
二、約定三：振幅有正有負，機率 = 振幅²，負號量不到
  H                |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  H → Z            |0⟩ +0.707（50%）  |1⟩ −0.707（50%）
三、四種閘（由左往右：先準備起點，再做這個閘）
  H：|0⟩ 起點         |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  H：|1⟩ 起點         |0⟩ +0.707（50%）  |1⟩ −0.707（50%）
  X：|0⟩ 起點         |1⟩ +1.000（100%）
  X：|1⟩ 起點         |0⟩ +1.000（100%）
  Z：|0⟩ 起點         |0⟩ +1.000（100%）
  Z：|1⟩ 起點         |1⟩ −1.000（100%）
  CX：控制 q0 = 0     |00⟩ +1.000（100%）
  CX：控制 q0 = 1     |11⟩ +1.000（100%）
四、改造區：2 顆位元，X(q1) → H(q0)
  我的線路             |10⟩ +0.707（50%）  |11⟩ +0.707（50%）
'''

# 製作代理實跑紀錄：qiskit 2.6.2，StatevectorSampler(seed=2026)，shots=1000
QISKIT_OUTPUT = '''只翻 q0 機率 {'01': 1.0} 量測 1000 次 {'01': 1000}
只翻 q1 機率 {'10': 1.0} 量測 1000 次 {'10': 1000}
H → Z 振幅 [0.707, -0.707] 機率 {'0': 0.5, '1': 0.5}
   ┌───┐┌───┐
q: ┤ H ├┤ Z ├
   └───┘└───┘
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q113：讀圖之前——三個約定與今天用到的閘（純 Python，不需安裝任何套件）

執行：  python read_order.py
它用一個很小的狀態向量模擬器（只認得 H、X、Z、CX 四種閘），印出：
  一、約定二：位元字串裡 q0 寫在最右邊
  二、約定三：振幅有正有負，機率 = 振幅²
  三、四種閘把 |0⟩、|1⟩ 變成什麼
  四、改造區：你自己畫的兩閘線路
"""
from math import sqrt

R2 = 1 / sqrt(2)


def run(n, gates):
    """n 顆位元都從 |0⟩ 出發，由左往右依序做 gates，回傳 2ⁿ 個振幅（第 i 個對應位元字串 bits(i)）"""
    s = [0.0] * (1 << n)
    s[0] = 1.0
    for g in gates:
        name, q = g[0], g[1]
        m = 1 << q
        if name == 'h':
            for i in range(len(s)):
                if not i & m:
                    a, b = s[i], s[i | m]
                    s[i], s[i | m] = (a + b) * R2, (a - b) * R2
        elif name == 'x':
            for i in range(len(s)):
                if not i & m:
                    s[i], s[i | m] = s[i | m], s[i]
        elif name == 'z':
            for i in range(len(s)):
                if i & m:
                    s[i] = -s[i]
        elif name == 'cx':  # ('cx', 控制, 目標)
            mt = 1 << g[2]
            for i in range(len(s)):
                if i & m and not i & mt:
                    s[i], s[i | mt] = s[i | mt], s[i]
        else:
            raise ValueError('只認得 h、x、z、cx：' + name)
    return s


def bits(i, n):
    """位元字串：最左邊是編號最大的位元，最右邊是 q0（和 Qiskit 相同）"""
    return ''.join(str((i >> q) & 1) for q in range(n - 1, -1, -1))


def amp(a):
    return '0' if abs(a) < 1e-9 else ('+' if a > 0 else '−') + f'{abs(a):.3f}'


def show(title, n, gates):
    s = run(n, gates)
    line = '  '.join(f'|{bits(i, n)}⟩ {amp(a)}（{a * a * 100:.0f}%）' for i, a in enumerate(s) if abs(a) > 1e-9)
    print(f'  {title:<16} {line}')


def label(gates):
    return ' → '.join(f'{g[0].upper()}(q{g[1]})' if g[0] != 'cx' else f'CX(q{g[1]}→q{g[2]})' for g in gates) or '（沒有閘）'


if __name__ == '__main__':
    print('一、約定二：位元字串裡 q0 寫在最右邊（兩顆位元，字串是 q1 q0）')
    show('X(q0)', 2, [('x', 0)])
    show('X(q1)', 2, [('x', 1)])
    print('二、約定三：振幅有正有負，機率 = 振幅²，負號量不到')
    show('H', 1, [('h', 0)])
    show('H → Z', 1, [('h', 0), ('z', 0)])
    print('三、四種閘（由左往右：先準備起點，再做這個閘）')
    show('H：|0⟩ 起點', 1, [('h', 0)])
    show('H：|1⟩ 起點', 1, [('x', 0), ('h', 0)])
    show('X：|0⟩ 起點', 1, [('x', 0)])
    show('X：|1⟩ 起點', 1, [('x', 0), ('x', 0)])
    show('Z：|0⟩ 起點', 1, [('z', 0)])
    show('Z：|1⟩ 起點', 1, [('x', 0), ('z', 0)])
    show('CX：控制 q0 = 0', 2, [('cx', 0, 1)])
    show('CX：控制 q0 = 1', 2, [('x', 0), ('cx', 0, 1)])

    # 四、改造區：自己畫一條兩閘線路。每個閘寫成 ('h', 位元)、('x', 位元)、('z', 位元) 或 ('cx', 控制, 目標)
    MY_N = 2
    MY_CIRCUIT = [('x', 1), ('h', 0)]
    print(f'四、改造區：{MY_N} 顆位元，{label(MY_CIRCUIT)}')
    show('我的線路', MY_N, MY_CIRCUIT)
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q113：用本機 Qiskit 確認位元順序（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector

for name, q in (('只翻 q0', 0), ('只翻 q1', 1)):
    qc = QuantumCircuit(2, 2)
    qc.x(q)                       # 翻轉閘：只作用在一顆位元
    sv = Statevector.from_instruction(qc)
    qc.measure([0, 1], [0, 1])
    counts = StatevectorSampler(seed=2026).run([qc], shots=1000).result()[0].data.c.get_counts()
    print(name, '機率', {str(k): round(float(v), 3) for k, v in sv.probabilities_dict().items()}, '量測 1000 次', counts)   # 位元字串最右邊是 q0

qc = QuantumCircuit(1)
qc.h(0)
qc.z(0)                           # 哈達瑪閘之後再做相位翻轉閘
sv = Statevector.from_instruction(qc)
print('H → Z 振幅', [round(float(a.real), 3) for a in sv.data], '機率', {str(k): round(float(v), 3) for k, v in sv.probabilities_dict().items()})
print(qc.draw())
'''

GATES = [  # (符號, 名稱, 旁白念法, 作用, 動畫方塊顏色)
    ('H', 'Hadamard', '哈達瑪閘', '|0⟩ → 一半 |0⟩、一半 |1⟩；|1⟩ → 一半一半但 |1⟩ 帶負號', '藍'),
    ('X', 'NOT', '翻轉閘', '|0⟩ ↔ |1⟩ 對調', '酒紅'),
    ('Z', '相位翻轉', '相位翻轉閘', '|0⟩ 不變，|1⟩ 多一個負號', '紫'),
    ('CNOT', '控制 NOT', '受控反閘', '實心點 = 控制，圈加號 = 目標；控制是 1 才翻轉目標', '酒紅色的點和圈'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q113：讀圖之前——三個約定與今天用到的閘（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是新模組「動手寫量子電路：從八個範例到自己的線路」的第一課：
先講好讀線路圖的三個約定，再認識四種閘的符號。八個範例本身留給接下來八堂課（Q114–Q121），今天不必把任何一個範例講完。

## 三個約定（讀圖約定卡的內容）

| 約定 | 內容 | 容易錯的地方 |
|---|---|---|
| 一 由左往右 | 橫軸是時間；一條橫線 = 一顆量子位元；最左邊是起點 |0⟩，方塊是閘，最右邊是量測；同一欄的閘同一拍做 | 橫線不是電線 |
| 二 q0 在哪裡 | 線路圖：q0 畫在最上面；位元字串：q0 寫在最右邊（|01⟩ = q1 是 0、q0 是 1） | 不同工具順序可能相反（Qiskit 和學程動畫都是 q0 在最右邊），讀結果前先確認 |
| 三 振幅有正負 | 每個結果一個振幅；柱子往上正、往下負；機率 = 振幅²，負號量不到 | 顏色看圖例：動畫藍正橘負，八個範例簡報金正紅負 |

## 四種閘

| 符號 | 名稱 | 影片念法 | 作用 | 動畫裡的顏色 |
|---|---|---|---|---|
''' + ''.join(f'| {a} | {b} | {c} | {d} | {e} |\n' for a, b, c, d, e in GATES) + '''
簡報第 4 頁的閘表還列了 CZ／CCZ（受控相位翻轉閘）和 Ry（可轉任意角度的旋轉閘），範例 4 以後才會用到。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 對照簡報第 2–4 頁：八個範例地圖、三個約定、閘表 | 簡報 basic-circuits.pptx p2–4、列印包第 1 頁 |
| 25–65 | 臨摹挑戰：在 basic-circuits.html#superposition 逐步播放疊加範例並讀出每一步；爸爸出題、孩子照畫 | `01_操作步驟.md`、列印包第 2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子自己畫一條兩閘線路，標出位元順序，寫預測，跑 `read_order.py` 對答案 | 列印包第 3 頁、`03_兩閘線路紀錄.csv` |
| 105–115 | 孩子教爸爸：怎麼操作、三個約定和四種閘 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#superposition`，按一次「下一步 ▶」和「量測 1,000 次」。
- 打開簡報 `slides/output/basic-circuits.pptx` 第 2–4 頁（課綱素材寫 p2–4，家長準備寫 p3–4：第 2 頁是地圖，第 3 頁是約定，第 4 頁是閘表）。
- 列印 `02_列印包_讀圖約定卡.pdf`（A4，共 4 頁），準備格子紙和兩種顏色的筆（一正一負）。
- 有 Python 的電腦先跑一次 `python read_order.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 本課的振幅都是實數（正或負）；更一般的情形振幅可以是複數，機率是「振幅乘自己的共軛」，本課不展開。
- 「換工具順序可能相反」是課綱提醒的一般情形；本課只實測了 Qiskit 與學程動畫。
- 量測 1,000 次的結果每次不同；只有「只翻 q0 → 01」這種確定的狀態，才會每次都一樣。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：逐步播放疊加範例（約 40 分鐘）

1. 打開 `animations/basic-circuits.html#superposition`（範例 1 疊加）。上方「起始態」先選 |0⟩。
2. 照約定一讀圖：左邊 `q0`、起點 `|0⟩`，藍色 `H` 方塊，最右邊量測錶。讀出來寫在列印包第 2 頁。
3. 按「下一步 ▶」：橘色虛線從 H 左邊走到右邊；看「振幅與機率」卡，柱子從一根變兩根，讀出每根下面的振幅和百分比。
4. 按「量測 1,000 次」：灰色是理論，綠色是實際次數。記下次數（每次不同）。
5. 想看負號：到 `#interference`（範例 2）按兩次「下一步 ▶」，做完 Z 後 |1⟩ 的柱子翻到下面變橘色，百分比仍是 50%。第三步留到範例 2 那堂。
6. 想看位元順序：到 `#bell`（範例 3），選上方第二個選項（Φ⁻），按「⏮ 起點」再按一次「下一步 ▶」，只做 q0 上的 X：柱子升在 |01⟩。

## 臨摹挑戰（穿插在上半場）

1. 出題官（爸爸）在動畫或簡報挑一張線路圖，只給看圖。
2. 臨摹員（孩子）在格子紙上照畫：橫線、起點、方塊、符號、量測，寫上 q0、q1。
3. 一起在動畫按「下一步 ▶」，一格一格對答案；畫錯或順序寫反的地方記在約定卡背面。

## 下半場：自己畫兩閘線路（約 30 分鐘）

1. 在列印包第 3 頁畫一條只有兩個閘的線路（一顆或兩顆位元），q0 畫在最上面。
2. 寫預測：每種結果的振幅與機率，位元字串 q0 寫在最右邊。
3. 打開 `read_order.py`，把最下面改造區的 `MY_N`、`MY_CIRCUIT` 改成你的線路，執行 `python read_order.py`，對照第四段的輸出。
4. 有裝 Qiskit 的話，用 `qiskit_check.py` 的寫法再跑一次，看位元字串的順序是否一樣。
''',

'read_order.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## read_order.py 實跑輸出（Python 3.13.18，結果固定）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- |01⟩ 是哪一顆是 1？最右邊是 q0，所以 q0 = 1、q1 = 0。線路圖上 q0 在最上面。\n'
  '- 為什麼 H → Z 之後機率還是 50%？Z 只給 |1⟩ 加負號，(−0.707)² = 0.5，負號平方後不見了。\n'
  '- 動畫和簡報的顏色為什麼不同？動畫（basic-circuits.html）藍色正、橘色負；八個範例簡報金色正、紅色負。換一份圖先看圖例。\n'
  '- 受控反閘哪一邊是控制？實心點是控制，圓圈加號是目標。read_order.py 寫成 (\'cx\', 控制, 目標)。\n'
  '- 改造區範例 X(q1) → H(q0)：q1 先翻成 1，q0 再進疊加，所以只會有 10、11，各 50%（字串左邊那位是 q1）。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html`（八個基礎量子電路）

- 頁首說明：「電路圖 q0 在最上面，但寫成位元字串時 q0 在最右邊」。
- 上方分頁：範例 1 疊加 … 範例 8 Grover；網址後面的 `#superposition`、`#interference`、`#bell` 直接開到該範例。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」：橘色虛線標出目前做到哪一格；還沒做的閘是淡色。
- 「振幅與機率」：圖例「正振幅」藍、「負振幅」橘；柱子下面寫振幅和百分比；下方 |ψ⟩ 是目前的狀態。
- 「量測 1 次」「量測 1,000 次」「清除」：灰色底是理論機率，綠色是實際次數；標題列寫「量測 q1 q0」。
- 最下面「Qiskit 程式碼」可以展開，最後一行註解「位元字串的最右邊是 q0」。

## 操作

左右方向鍵：上一步／下一步；空白鍵：播放。點電路上的閘可以直接跳到那一步。
''',
}

SHEET_HEADER = ['線路', '位元數', '第 1 個閘', '第 2 個閘', '我的預測（字串：q0 在最右邊）', 'read_order.py 結果', '一樣嗎', '哪裡容易錯']
SHEET_ROWS = [['範例：只翻 q0', '2', 'X(q0)', '—', '01', '|01⟩ +1.000（100%）', '是', 'q0 寫在最右邊'],
              ['範例：H 再 Z', '1', 'H(q0)', 'Z(q0)', '0 和 1 各 50%', '|1⟩ −0.707（50%）', '是', '負號量不到'],
              ['我的線路 1', '', '', '', '', '', '', ''], ['我的線路 2', '', '', '', '', '', '', ''], ['爸爸的線路', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:11mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:22%}
.wire{border-bottom:1.4pt solid #0b2540;height:14mm;position:relative;margin:0 0 4mm 14mm}.wire span{position:absolute;left:-14mm;bottom:-3mm;font-size:11pt}
.grid{height:52mm;border:1pt solid #cfdde8;background-image:linear-gradient(#cfdde8 .5pt,transparent .5pt),linear-gradient(90deg,#cfdde8 .5pt,transparent .5pt);
background-size:6mm 6mm;margin:2mm 0}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 read_order.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'read_order.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    gate_rows = ''.join(f'<tr><td class="k">{a}</td><td>{c}</td><td>{d}</td><td></td></tr>' for a, b, c, d, e in GATES)
    pages = [
        '<h2>讀圖約定卡</h2><p class="lead">把三個約定和四種閘整理在同一張卡上；之後八個範例都用得到。</p>'
        '<table class="judge"><tr><th style="width:22%">約定</th><th>用自己的話寫</th></tr>'
        '<tr><td class="k">一、由左往右</td><td></td></tr><tr><td class="k">二、q0 在哪裡</td><td>線路圖：＿＿＿＿　位元字串：＿＿＿＿</td></tr>'
        '<tr><td class="k">三、振幅有正負</td><td>機率 = ＿＿＿＿；動畫：＿色正、＿色負</td></tr></table>'
        '<table class="judge" style="margin-top:4mm"><tr><th style="width:12%">符號</th><th style="width:20%">名稱</th><th style="width:40%">作用</th><th>畫出符號</th></tr>'
        + gate_rows + '</table>',
        '<h2>臨摹挑戰卡</h2><p class="lead">出題官（爸爸）挑一張線路圖，只給看圖；臨摹員（你）照畫一遍，再標上約定。</p>'
        '<div class="grid"></div><p>這張圖有＿＿顆位元；最上面那條是 q＿；第一格的閘是＿＿＿；量測在＿＿＿＿。</p>'
        '<h3>逐步播放疊加範例（basic-circuits.html#superposition）</h3>'
        '<table class="judge"><tr><th style="width:18%">步驟</th><th>虛線在哪裡</th><th>|0⟩ 的振幅／機率</th><th>|1⟩ 的振幅／機率</th></tr>'
        '<tr><td class="k">起點</td><td></td><td></td><td></td></tr><tr><td class="k">第 1 步 H</td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">量測 1,000 次</td><td colspan="3">0：＿＿次　1：＿＿次</td></tr></table>'
        '<p class="note">畫錯或順序寫反的地方，記在約定卡背面。</p>',
        '<h2>換你改造：自己畫兩閘線路</h2><p class="lead">只用兩個閘，一顆或兩顆位元都可以；q0 畫在最上面。</p>'
        '<div class="wire"><span>q0 |0⟩</span></div><div class="wire"><span>q1 |0⟩</span></div>'
        '<p>我的預測（位元字串 q0 寫在最右邊）：</p><div class="line"></div>'
        '<pre class="code"># read_order.py 最下面的改造區\nMY_N = 2\nMY_CIRCUIT = [(&#39;x&#39;, 1), (&#39;h&#39;, 0)]   # 改成你的兩個閘\n'
        '# 閘的寫法：(&#39;h&#39;, 位元)、(&#39;x&#39;, 位元)、(&#39;z&#39;, 位元)、(&#39;cx&#39;, 控制, 目標)</pre>'
        '<p>程式印出：</p><div class="line"></div><p>和預測一樣嗎？如果不一樣，是哪一個約定讀反了？</p><div class="line"></div>',
        '<h2>最後一關：教爸爸讀圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 三個約定（不看稿）：</p><div class="line"></div><div class="line"></div>'
        '<p>2. 四種閘的符號和作用：</p><div class="line"></div>'
        '<p>3. 一個容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出三個約定：由左往右、q0 位置、振幅正負</li><li>認出 H、X、Z、CNOT 的符號</li>'
        '<li>指出：不同工具的位元順序可能相反，讀結果前先確認</li><li>完成讀圖約定卡，兩閘線路的預測和程式結果一致</li>'
        '<li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q113 讀圖約定卡 列印包', '父子科技學院 量子電腦學程 Q113｜讀圖之前：三個約定與今天用到的閘', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q113-reading-conventions', folder='Q113_讀圖之前_三個約定與閘', files=FILES,
        sheet=('03_兩閘線路紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_讀圖約定卡.pdf', pack_pages=4,
        pack_needles=('讀圖約定卡', '臨摹挑戰卡', '逐步播放', '換你改造', 'MY_CIRCUIT', '最後一關'),
        authoring_dir=XINEW / 'authoring/q113', episode_dir='specials/q113-reading-conventions',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；read_order.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'read_order.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only); qiskit 2.6.2',
               'recordedRun': {'xq0': '01', 'xq1': '10', 'hz': {'0': '+0.707 (50%)', '1': '−0.707 (50%)'},
                               'qiskitCounts': {'xq0': {'01': 1000}, 'xq1': {'10': 1000}}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q113/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

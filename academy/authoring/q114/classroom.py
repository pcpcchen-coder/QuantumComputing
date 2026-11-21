"""Q114 課堂教材：|+⟩／|−⟩ 對照表、盲測紀錄卡、再加一個 H 預測表、可執行的 coin.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#superposition 與 operation.html#qubit；coin.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 coin.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q114/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，random.Random(1114)（固定種子，結果固定）
RUN_OUTPUT = '''一、兩種疊加態（機率 = 振幅²）
  |+⟩ = H|0⟩    |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  |−⟩ = H|1⟩    |0⟩ +0.707（50%）  |1⟩ −0.707（50%）
二、各量測 1000 次
  |+⟩   0 → 491 次  1 → 509 次
  |−⟩   0 → 485 次  1 → 515 次
三、盲測 5 回合（先看次數猜，再看答案）
  第 1 回  0 → 486 次  1 → 514 次    答案：|+⟩
  第 2 回  0 → 518 次  1 → 482 次    答案：|+⟩
  第 3 回  0 → 494 次  1 → 506 次    答案：|−⟩
  第 4 回  0 → 508 次  1 → 492 次    答案：|−⟩
  第 5 回  0 → 483 次  1 → 517 次    答案：|−⟩
四、改造區：再加一個 H
  H → H         |0⟩ +1.000（100%）  |1⟩ 0（0%）
  X → H → H     |0⟩ 0（0%）  |1⟩ +1.000（100%）
'''

# 製作代理實跑紀錄：qiskit 2.6.2，StatevectorSampler(seed=2026)，shots=1000
QISKIT_OUTPUT = '''|+⟩ 振幅 [0.707, 0.707] 機率 {'0': 0.5, '1': 0.5} 量測 1000 次 {'0': 464, '1': 536}
|−⟩ 振幅 [0.707, -0.707] 機率 {'0': 0.5, '1': 0.5} 量測 1000 次 {'0': 464, '1': 536}
|+⟩ 再加 H 振幅 [1.0, 0.0] 機率 {'0': 1.0} 量測 1000 次 {'0': 1000}
|−⟩ 再加 H 振幅 [0.0, 1.0] 機率 {'1': 1.0} 量測 1000 次 {'1': 1000}
   ┌───┐┌───┐
q: ┤ X ├┤ H ├
   └───┘└───┘
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q114：範例 1 疊加——量子硬幣與 |+⟩、|−⟩（純 Python，不需安裝任何套件）

執行：  python coin.py
它用一個很小的一顆位元模擬器（只認得 H、X、Z 三種閘），印出：
  一、兩種疊加態的振幅與機率：|0⟩ → H 得 |+⟩；|1⟩（先 X）→ H 得 |−⟩
  二、各量測 1000 次的次數（用固定的亂數種子，所以每次執行結果相同；真實量測每次都不同）
  三、盲測：電腦偷偷選 |+⟩ 或 |−⟩，只給你看次數
  四、改造區：再加一個 H 會怎樣？
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


def amp(v):
    return '0' if abs(v) < 1e-9 else ('+' if v > 0 else '−') + f'{abs(v):.3f}'


def show(title, gates):
    s = run(gates)
    print(f'  {title:<14}' + '  '.join(f'|{i}⟩ {amp(v)}（{v * v * 100:.0f}%）' for i, v in enumerate(s)))


def shots(gates, n, rng):
    """量測 n 次：每次以機率 振幅² 得到 0 或 1，回傳 [0 的次數, 1 的次數]"""
    p0 = run(gates)[0] ** 2
    c0 = sum(rng.random() < p0 for _ in range(n))
    return [c0, n - c0]


def name(gates):
    return ' → '.join(g.upper() for g in gates) or '（沒有閘）'


PLUS, MINUS = ['h'], ['x', 'h']

if __name__ == '__main__':
    rng = random.Random(1114)   # 固定種子：教材的輸出才對得起來；改成 random.Random() 就每次不同
    print('一、兩種疊加態（機率 = 振幅²）')
    show('|+⟩ = H|0⟩', PLUS)
    show('|−⟩ = H|1⟩', MINUS)
    print('二、各量測 1000 次')
    for title, g in (('|+⟩', PLUS), ('|−⟩', MINUS)):
        c = shots(g, 1000, rng)
        print(f'  {title:<6}0 → {c[0]} 次  1 → {c[1]} 次')
    print('三、盲測 5 回合（先看次數猜，再看答案）')
    for r in range(1, 6):
        secret = rng.choice(['|+⟩', '|−⟩'])
        c = shots(PLUS if secret == '|+⟩' else MINUS, 1000, rng)
        print(f'  第 {r} 回  0 → {c[0]} 次  1 → {c[1]} 次    答案：{secret}')

    # 四、改造區：先預測，再執行。閘寫成 'h'、'x'、'z'，由左往右排
    MY_CIRCUITS = [['h', 'h'], ['x', 'h', 'h']]
    print('四、改造區：再加一個 H')
    for g in MY_CIRCUITS:
        show(name(g), g)
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q114：用本機 Qiskit 重現 |+⟩、|−⟩（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


def report(name, qc):
    sv = Statevector.from_instruction(qc)
    m = qc.copy()
    m.measure_all()
    counts = StatevectorSampler(seed=2026).run([m], shots=1000).result()[0].data.meas.get_counts()
    print(name, '振幅', [round(float(a.real), 3) for a in sv.data],
          '機率', {str(k): round(float(v), 3) for k, v in sv.probabilities_dict().items()}, '量測 1000 次', dict(sorted(counts.items())))


plus = QuantumCircuit(1)
plus.h(0)                    # |0⟩ → 哈達瑪閘 → |+⟩
minus = QuantumCircuit(1)
minus.x(0)                   # 先用翻轉閘準備 |1⟩
minus.h(0)                   # |1⟩ → 哈達瑪閘 → |−⟩
report('|+⟩', plus)
report('|−⟩', minus)

for name, qc in (('|+⟩ 再加 H', plus), ('|−⟩ 再加 H', minus)):
    qc2 = qc.copy()
    qc2.h(0)                 # 改造：再加一個哈達瑪閘
    report(name, qc2)
print(minus.draw())
'''

TABLE = [  # (態, 起點, 閘, |0⟩ 振幅, |1⟩ 振幅, 機率, Bloch 箭頭, 動畫柱子顏色)
    ('|+⟩', '|0⟩', 'H', '+0.707', '+0.707', '0：50%、1：50%', '赤道 +x', '藍、藍'),
    ('|−⟩', '|1⟩', 'X → H', '+0.707', '−0.707', '0：50%、1：50%', '赤道 −x（正對面）', '藍、橘'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q114：範例 1 疊加——量子硬幣與 |+⟩、|−⟩（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的範例 1。
上一課（Q113）講了讀圖的三個約定；今天只用一顆位元：|0⟩ 做 H 得到 |+⟩，|1⟩（先加 X）做 H 得到 |−⟩。
核心一句話：**|+⟩ 和 |−⟩ 機率一樣，只差 |1⟩ 振幅的正負號。** 干涉（H‑Z‑H）留給下一課 Q115。

## |+⟩／|−⟩ 對照表（作品的答案）

| 態 | 起點 | 閘 | |0⟩ 振幅 | |1⟩ 振幅 | 機率 | Bloch 箭頭 | 動畫柱子 |
|---|---|---|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in TABLE) + '''
最下面再留一列「量測 1,000 次的次數」：兩列都大約各 500 次，但每次不同；次數的差異來自隨機，不是正負號造成的。

## 影片的念法

|+⟩ 念「正號疊加態」、|−⟩ 念「負號疊加態」；H 念「哈達瑪閘」、X「翻轉閘」、Z「相位翻轉閘」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 對照簡報第 5–6 頁：範例 1 的線路、|+⟩ 和 |−⟩ 的四格對照 | 簡報 basic-circuits.pptx p5–6 |
| 25–65 | 在 basic-circuits.html#superposition 從 |0⟩、|1⟩ 起始各做一次，比較柱子顏色、Bloch 箭頭、量測 1,000 次；填對照表；玩盲測 | `01_操作步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子預測「再加一個 H」會怎樣，跑 `coin.py` 驗證 | 列印包第 3 頁、`03_盲測與改造紀錄.csv` |
| 105–115 | 孩子教爸爸：怎麼做出兩種疊加態、差在哪、哪裡容易錯 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#superposition`：上方「起始態」切換 |0⟩／|1⟩，按「下一步 ▶」與「量測 1,000 次」。
- 選用：開 `operation.html#qubit`，按 |+⟩，把「φ（相位）」滑桿拖到 180°，看箭頭轉到赤道對面、理論機率不變。
- 打開簡報 `slides/output/basic-circuits.pptx` 第 5–6 頁（課綱寫 p5–6，頁碼無誤）。
- 列印 `02_列印包_正負疊加態對照表.pdf`（A4，共 4 頁），準備兩種顏色的筆（一正一負）。
- 有 Python 的電腦先跑一次 `python coin.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 本課的振幅都是實數；「量不到的正負號叫做相位」嚴格說是兩個振幅的相對相位，本課不展開複數。
- 量測 1,000 次的實際次數每次不同；coin.py 用固定亂數種子 1114，所以教材印出來的次數固定。
- 「只看次數猜對約一半」是推論：兩種疊加態的量測機率完全相同，次數裡沒有可以分辨的資訊。coin.py 只示範 5 回合。
- Bloch 球和振幅柱子是模擬器才看得到的；真實的量子電腦只給量測結果。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：從 |0⟩ 與 |1⟩ 起始各做一次（約 40 分鐘）

1. 打開 `animations/basic-circuits.html#superposition`（範例 1 疊加）。上方「起始態」先選 |0⟩。
2. 按「下一步 ▶」：做完 H，兩根柱子都是朝上的藍色 +0.707，下面寫 50%；右邊 Bloch 球的橘色箭頭轉到赤道上（+x）。下方 |ψ⟩ = (|0⟩ + |1⟩) / √2。
3. 按「量測 1,000 次」：灰色是理論，綠色是實際次數。把次數寫進對照表最下面一列。
4. 起始態改選 |1⟩：線路前面多一個酒紅色 X，頁面會直接跳到最後一步。先按「⏮ 起點」，再按「下一步 ▶」：X 讓箭頭轉到南極、|1⟩ 柱子 +1。
5. 再按「下一步 ▶」：|1⟩ 柱子翻到下面變橘色 −0.707，下面仍是 50%；箭頭在赤道的另一邊（−x）。|ψ⟩ = (|0⟩ − |1⟩) / √2。
6. 再按「量測 1,000 次」，次數寫進對照表。比較兩列：哪些欄一樣、哪些不一樣？

## 盲測（穿插在上半場）

1. 孩子轉過身。爸爸在動畫選 |0⟩ 或 |1⟩，做到最後一步，按「量測 1,000 次」。
2. 用手或紙遮住振幅卡（柱子、Bloch 球、|ψ⟩）和上方選項，只給孩子看量測卡的次數。
3. 孩子猜 |+⟩ 或 |−⟩，記在列印包第 2 頁；連續玩 5 回合以上，數猜對幾次。
4. 也可以讓電腦當出題官：`python coin.py` 第三段是 5 回合盲測（先遮住答案欄）。

## 下半場：再加一個 H（約 30 分鐘）

1. 在列印包第 3 頁寫預測：|+⟩ 再加一個 H 會變成什麼？|−⟩ 呢？量測 1,000 次會得到什麼？
2. 執行 `python coin.py`，看第四段「改造區」的輸出，對照預測。
3. 改 `MY_CIRCUITS` 自己試別的組合，例如 `['h', 'h', 'h']`、`['x', 'h', 'z', 'h']`（後者是下一課的主角，先預測就好）。
4. 有裝 Qiskit 的話，跑 `qiskit_check.py`，看「再加 H」的 1000 次是不是全部 0、全部 1。
''',

'coin.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## coin.py 實跑輸出（Python 3.13.18，random.Random(1114)，結果固定）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- |+⟩ 和 |−⟩ 哪裡一樣？兩個結果的機率都是 50%（0.707² ≈ 0.5、(−0.707)² ≈ 0.5）。\n'
  '- 哪裡不一樣？|1⟩ 的振幅：|+⟩ 是 +0.707、|−⟩ 是 −0.707；Bloch 箭頭在赤道上正對面（+x 與 −x）。\n'
  '- 為什麼量測 1,000 次看不出差別？量測只給 0 或 1，機率又完全一樣，次數裡沒有正負號的資訊；盲測猜對的機會約一半。\n'
  '- 為什麼兩次 1,000 次的次數不一樣？量測是隨機的。Qiskit 用同一個種子時，|+⟩ 和 |−⟩ 的次數甚至一模一樣（464／536），可見差異來自亂數，不是正負號。\n'
  '- 再加一個 H 呢？H 做兩次等於沒做：|+⟩ → |0⟩、|−⟩ → |1⟩，都是 100%。這時候一量就分得出來，正負號「現身」了。\n'
  '- 下一課：在兩個 H 中間夾一個 Z（相位翻轉閘），結果會變成什麼？先預測，Q115 揭曉。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html#superposition`（範例 1 疊加）

- 上方「起始態」：|0⟩（預設）或 |1⟩；選 |1⟩ 時線路前面多一個 X 步驟「X 閘：準備 |1⟩」。換選項時頁面停在最後一步並清除量測。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」：橘色虛線標出目前做到哪一格。
- 「振幅與機率」：圖例「正振幅」藍、「負振幅」橘；柱子下面寫振幅和百分比；右邊 Bloch 球（軸標 |0⟩、|1⟩、+x、−x、+y），橘色箭頭；下方 |ψ⟩。
- 「量測 1 次」「量測 1,000 次」「清除」：綠框顯示最近一次的結果；灰色底是理論機率，綠色是實際次數；量測會累加，按「清除」才歸零。

## `animations/operation.html#qubit`（量子位元的狀態與測量）

- 預設按鈕 |0⟩、|1⟩、|+⟩、|+i⟩、θ=60°；滑桿「θ（極角）」「φ（相位）」。
- |+⟩ 是 θ = 90°、φ = 0°；把 φ 拖到 180° 就是 |−⟩（箭頭在赤道正對面）。改 φ 不會改變理論機率（青線不動）。
- 「測量一次」「連續 shots」「清除統計」「一次跑 1000 shots」。

## 操作

basic-circuits.html：左右方向鍵 上一步／下一步；空白鍵 播放；點電路上的閘可以直接跳到那一步。
''',
}

SHEET_HEADER = ['回合／線路', '起點', '閘', '量測 1000 次：0 的次數', '1 的次數', '我猜（|+⟩／|−⟩）', '答案', '猜對嗎', '備註']
SHEET_ROWS = [['範例：coin.py 盲測第 1 回', '（遮住）', 'H', '486', '514', '', '|+⟩', '', '次數看不出正負號'],
              ['範例：再加一個 H（|−⟩）', '|1⟩', 'X → H → H', '0', '1000', '—', '|1⟩ 100%', '—', '正負號現身'],
              ['盲測第 1 回', '', '', '', '', '', '', '', ''], ['盲測第 2 回', '', '', '', '', '', '', '', ''],
              ['盲測第 3 回', '', '', '', '', '', '', '', ''], ['我的改造線路', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:11mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:20%}
table.judge th{font-size:10.5pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 coin.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'coin.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    blind_rows = ''.join(f'<tr><td class="k">第 {i} 回</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 7))
    pages = [
        '<h2>|+⟩／|−⟩ 對照表</h2><p class="lead">在 basic-circuits.html#superposition 從 |0⟩、|1⟩ 起始各做一次，把看到的填進去。</p>'
        '<table class="judge"><tr><th style="width:20%">欄位</th><th>|+⟩（起始態 |0⟩）</th><th>|−⟩（起始態 |1⟩）</th></tr>'
        '<tr><td class="k">做了哪些閘</td><td></td><td></td></tr>'
        '<tr><td class="k">|0⟩ 的振幅</td><td></td><td></td></tr><tr><td class="k">|1⟩ 的振幅</td><td></td><td></td></tr>'
        '<tr><td class="k">柱子顏色／方向</td><td></td><td></td></tr><tr><td class="k">機率</td><td></td><td></td></tr>'
        '<tr><td class="k">Bloch 箭頭在哪</td><td></td><td></td></tr>'
        '<tr><td class="k">量測 1,000 次</td><td>0：＿＿次　1：＿＿次</td><td>0：＿＿次　1：＿＿次</td></tr></table>'
        '<p>一樣的欄位：＿＿＿＿＿＿＿＿＿＿　不一樣的欄位：＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>盲測紀錄卡</h2><p class="lead">爸爸背著你準備 |+⟩ 或 |−⟩，量測 1,000 次，只給你看次數。你來猜！</p>'
        '<table class="judge"><tr><th style="width:20%">回合</th><th>0 的次數</th><th>1 的次數</th><th>我猜</th><th>答案</th></tr>'
        + blind_rows + '</table>'
        '<p>猜對＿＿回／共＿＿回。和亂猜比起來怎麼樣？</p><div class="line"></div>'
        '<p>為什麼只看次數分不出來？</p><div class="line"></div>'
        '<p class="note">也可以讓電腦出題：coin.py 第三段是 5 回合盲測（先遮住答案欄）。</p>',
        '<h2>換你改造：再加一個 H</h2><p class="lead">先寫預測，再跑 coin.py 驗證。</p>'
        '<table class="judge"><tr><th style="width:20%">線路</th><th>我的預測（振幅／機率）</th><th>coin.py 結果</th><th style="width:12%">一樣嗎</th></tr>'
        '<tr><td class="k">|0⟩ → H → H</td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">|1⟩ → H → H</td><td></td><td></td><td></td></tr>'
        '<tr><td class="k">我的線路：</td><td></td><td></td><td></td></tr></table>'
        '<pre class="code"># coin.py 最下面的改造區（閘由左往右排；從 |1⟩ 出發就先放一個 &#39;x&#39;）\n'
        'MY_CIRCUITS = [[&#39;h&#39;, &#39;h&#39;], [&#39;x&#39;, &#39;h&#39;, &#39;h&#39;]]   # 改成你的線路\n'
        '# 閘的寫法：&#39;h&#39; 哈達瑪閘、&#39;x&#39; 翻轉閘、&#39;z&#39; 相位翻轉閘</pre>'
        '<p>再加一個 H 之後，|+⟩ 和 |−⟩ 量起來還一樣嗎？正負號跑到哪裡去了？</p><div class="line"></div><div class="line"></div>',
        '<h2>最後一關：教爸爸兩種疊加態</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. |+⟩ 和 |−⟩ 各是怎麼做出來的（不看稿）：</p><div class="line"></div>'
        '<p>2. 機率一樣在哪裡，振幅差在哪裡：</p><div class="line"></div>'
        '<p>3. 一個容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：|0⟩ → H 得 |+⟩；|1⟩（先 X）→ H 得 |−⟩</li><li>說出：機率都是 50%，只差 |1⟩ 振幅的正負號</li>'
        '<li>指出：量測 1,000 次看不出 |+⟩ 和 |−⟩ 的差別</li><li>完成 |+⟩／|−⟩ 對照表，再加一個 H 的預測和程式結果一致</li>'
        '<li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q114 |+⟩／|−⟩ 對照表 列印包', '父子科技學院 量子電腦學程 Q114｜範例 1：疊加——量子硬幣與 |+⟩、|−⟩', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q114-plus-minus-coin', folder='Q114_範例1_疊加_量子硬幣', files=FILES,
        sheet=('03_盲測與改造紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_正負疊加態對照表.pdf', pack_pages=4,
        pack_needles=('對照表', '盲測紀錄卡', '換你改造', 'MY_CIRCUITS', '最後一關'),
        authoring_dir=XINEW / 'authoring/q114', episode_dir='specials/q114-plus-minus-coin',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；coin.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'coin.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, random seed 1114); qiskit 2.6.2',
               'recordedRun': {'plus': {'0': '+0.707 (50%)', '1': '+0.707 (50%)'}, 'minus': {'0': '+0.707 (50%)', '1': '−0.707 (50%)'},
                               'hh': {'fromZero': '|0⟩ 100%', 'fromOne': '|1⟩ 100%'},
                               'qiskitCounts': {'plus': {'0': 464, '1': 536}, 'minus': {'0': 464, '1': 536},
                                                'plusH': {'0': 1000}, 'minusH': {'1': 1000}}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q114/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

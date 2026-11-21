"""Q106 課堂教材：振幅長條逐步圖（Bell 態與兩位元 Grover）、可執行的 grover_bars.py、換答案預測表、容易錯的地方、教爸爸檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#grover；程式只要 Python 3。
建置時會真的執行一次 grover_bars.py，確認輸出和影片、教材寫的數字一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q106/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，結果固定（無亂數）
RUN_OUTPUT = '''== Bell 態：兩顆哈達瑪閘 → 受控相位翻轉 → Q2 再一個哈達瑪閘 ==
起點      00:+1.00 ▇▇▇▇▇▇▇▇  01:+0.00           10:+0.00           11:+0.00         
H⊗H       00:+0.50 ▇▇▇▇      01:+0.50 ▇▇▇▇      10:+0.50 ▇▇▇▇      11:+0.50 ▇▇▇▇    
    a00·a11 = +0.25，a01·a10 = +0.25 → 乘積態
CZ        00:+0.50 ▇▇▇▇      01:+0.50 ▇▇▇▇      10:+0.50 ▇▇▇▇      11:−0.50 ▇▇▇▇    
    a00·a11 = −0.25，a01·a10 = +0.25 → 糾纏
H(Q2)     00:+0.71 ▇▇▇▇▇▇    01:+0.00           10:+0.00           11:+0.71 ▇▇▇▇▇▇  
    a00·a11 = +0.50，a01·a10 = +0.00 → 糾纏

== 兩位元 Grover，答案 = 10 ==
H⊗H       00:+0.50 ▇▇▇▇      01:+0.50 ▇▇▇▇      10:+0.50 ▇▇▇▇      11:+0.50 ▇▇▇▇    
標記      00:+0.50 ▇▇▇▇      01:+0.50 ▇▇▇▇      10:−0.50 ▇▇▇▇      11:+0.50 ▇▇▇▇    
    平均 = +0.25
擴散      00:+0.00           01:+0.00           10:+1.00 ▇▇▇▇▇▇▇▇  11:+0.00         
    一輪後：量到 10 的機率 100.0 %
第二輪    00:−0.50 ▇▇▇▇      01:−0.50 ▇▇▇▇      10:+0.50 ▇▇▇▇      11:−0.50 ▇▇▇▇    
    兩輪後：量到 10 的機率 25.0 %（轉過頭）

== 位元多了：答案的機率（%）==
位元  選項   1 輪    2 輪    3 輪    4 輪
  2     4   100.0    25.0    25.0   100.0
  3     8    78.1    94.5    33.0     1.2
  4    16    47.3    90.8    96.1    58.2
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q106：振幅長條逐步圖——Bell 態與兩位元 Grover（純 Python，不需要安裝任何套件）

執行：  python grover_bars.py
位元順序和學程動畫 transmon-3d.html 第 7 章相同：|Q1 Q2⟩，左邊那位是 Q1。
"""
import math

ANSWER = '10'       # 改造區：把答案換成 00、01、10 或 11，先預測一輪後的長條，再執行
R2 = 1 / math.sqrt(2)


def h(a, q):
    """哈達瑪閘：q = 0 是 Q1（左邊那位），q = 1 是 Q2"""
    bit = 2 if q == 0 else 1
    b = a[:]
    for i in range(4):
        if not i & bit:
            b[i], b[i | bit] = R2 * (a[i] + a[i | bit]), R2 * (a[i] - a[i | bit])
    return b


def cz(a):
    """受控相位翻轉：只把 |11⟩ 的振幅變號"""
    return a[:3] + [-a[3]]


def oracle(a, ans):
    """標記答案：答案那一格變號（硬體上是在受控相位翻轉前後，對答案是 0 的位元夾翻轉閘）"""
    b = a[:]
    b[int(ans, 2)] *= -1
    return b


def diffuse(a):
    """擴散：每個振幅對平均值翻轉，新振幅 = 2 × 平均 − 原振幅"""
    m = sum(a) / len(a)
    return [2 * m - v for v in a]


def sg(v):
    return ('−' if v < -1e-9 else '+') + f'{abs(v):.2f}'


def bar(v):
    n = round(abs(v) * 8)
    return sg(v) + ' ' + ('▇' * n).ljust(8)


def show(name, a):
    pad = 10 - sum(2 if ord(c) > 0x2E80 else 1 for c in name)
    print(name + ' ' * pad + '  '.join(f'{k}:{bar(v)}' for k, v in zip(('00', '01', '10', '11'), a)))


def check(a):
    p1, p2 = a[0] * a[3], a[1] * a[2]
    kind = '乘積態' if abs(p1 - p2) < 1e-9 else '糾纏'
    return f'    a00·a11 = {sg(p1)}，a01·a10 = {sg(p2)} → {kind}'


def grover_prob(n, rounds):
    """n 個位元（N = 2ⁿ 個選項）做 rounds 輪之後，答案的機率"""
    N = 2 ** n
    a = [1 / math.sqrt(N)] * N
    for _ in range(rounds):
        a[0] = -a[0]
        a = diffuse(a)
    return a[0] ** 2


if __name__ == '__main__':
    print('== Bell 態：兩顆哈達瑪閘 → 受控相位翻轉 → Q2 再一個哈達瑪閘 ==')
    a = [1.0, 0.0, 0.0, 0.0]
    show('起點', a)
    a = h(h(a, 0), 1); show('H⊗H', a); print(check(a))
    a = cz(a); show('CZ', a); print(check(a))
    a = h(a, 1); show('H(Q2)', a); print(check(a))
    print()
    print(f'== 兩位元 Grover，答案 = {ANSWER} ==')
    a = h(h([1.0, 0.0, 0.0, 0.0], 0), 1); show('H⊗H', a)
    a = oracle(a, ANSWER); show('標記', a); print(f'    平均 = {sg(sum(a) / 4)}')
    a = diffuse(a); show('擴散', a)
    print(f'    一輪後：量到 {ANSWER} 的機率 {a[int(ANSWER, 2)] ** 2 * 100:.1f} %')
    a = oracle(a, ANSWER); a = diffuse(a); show('第二輪', a)
    print(f'    兩輪後：量到 {ANSWER} 的機率 {a[int(ANSWER, 2)] ** 2 * 100:.1f} %（轉過頭）')
    print()
    print('== 位元多了：答案的機率（%）==')
    print('位元  選項   1 輪    2 輪    3 輪    4 輪')
    for n in (2, 3, 4):
        print(f'{n:>3}  {2 ** n:>4}' + ''.join(f'{grover_prob(n, r) * 100:8.1f}' for r in (1, 2, 3, 4)))
'''

# 逐步圖的八列：(列名, 這一步做什麼, 參考振幅 00/01/10/11, 判定)
ROWS = [
    ('起點', '兩顆都在 |00⟩', '+1、0、0、0', '乘積態'),
    ('H⊗H', '兩顆都做 H', '+½、+½、+½、+½', '乘積態（¼ = ¼）'),
    ('CZ', '|11⟩ 翻負號', '+½、+½、+½、−½', '糾纏（−¼ ≠ ¼）'),
    ('H(Q2)', 'Bell 態', '+0.71、0、0、+0.71', '糾纏'),
    ('H⊗H', 'Grover 第一步', '+½、+½、+½、+½', '乘積態'),
    ('標記 10', 'X(Q2)→CZ→X(Q2)', '+½、+½、−½、+½', '糾纏'),
    ('擴散', '2 × 平均 − 原振幅', '0、0、+1、0', '乘積態'),
    ('量測', '量 50 次', '每次都是 10', '—'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q106：第 8 課 糾纏與兩位元 Grover（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的兩件事：兩顆位元怎麼糾纏在一起、四個選項怎麼只查一次就找到答案；課堂用「尋寶」的方式，跟著 3D 動畫第 7 章一步一步畫振幅長條。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#grover`（第 7 章）；加映 `basic-circuits.html#grover`。免安裝、不需帳號 |
| 程式 | `grover_bars.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_糾纏與兩位元Grover.pdf`（A4，共 4 頁）；一張小紙片給藏寶人寫答案 |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「四個箱子，最少要開幾次才一定找到？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：乘積態等式、CZ 做出糾纏、Bell 態、標記與擴散 | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 第 7 章步驟 1–6 逐步看，每一步先預測再畫一排長條 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 換答案位置：爸爸藏寶，孩子預測一輪後的長條，再用自由實驗與程式驗證 | `grover_bars.py`、列印包第 2 頁、`03_換答案紀錄.csv` |
| 105–115 | 孩子教爸爸：操作與原理，指出一個限制 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結、替逐步圖命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `transmon-3d.html#grover`，取消「自動接續」，按步驟按鈕 1–6、8 各看一次；左上方字幕會跟著動畫說明。
- 跑一次 `python grover_bars.py`，確認「一輪後：量到 10 的機率 100.0 %」。
- 讀一遍 `04_解答.md`。

## 帶的原則

- 每一步先讓孩子預測、畫下來，再看動畫；畫錯不扣分，對照後用另一支筆修正。
- 長條高度是振幅、可正可負；機率是振幅的平方。負號量不出來，但會在干涉時起作用。
- 最重要的一句：兩位元 Grover 剛好一輪 100%，是因為選項只有 4 個；位元多了就不一定剛好，做太多輪還會轉過頭。

## 誠實說明

- 動畫與程式都是理想模擬；實機上 CZ 和讀取都有誤差，10 不會剛好 100%，但會明顯突出。
- 動畫的量測是隨機抽樣，Bell 態量 40 次時 00 和 11 的次數每次不同。
- 位元順序：transmon-3d 第 7 章寫成 |Q1 Q2⟩（左邊是 Q1）；basic-circuits 寫成 q1 q0（右邊是 q0）。兩者都是「左邊高位」，名字不同而已。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：逐步畫振幅長條（約 40 分鐘）

1. 用瀏覽器開 `animations/transmon-3d.html#grover`（第 7 章：振幅長條）。
2. 先取消「自動接續」，這樣每一步播完會停下來。
3. 按步驟按鈕「1」（糾纏）。每次左上方字幕說要送一個閘時，先按「暫停」，在列印包第 1 頁畫出你預測的四根長條，再按「播放」對答案。
4. 看長條右邊的兩個乘積 a₀₀·a₁₁、a₀₁·a₁₀，把判定（乘積態／糾纏）寫在最右欄。
5. 按「2」到「5」做 Grover（答案 10），同樣先預測再看；第 4 步注意金色平均線。
6. 按「6」看「再多做一次」：答案的長條掉回多少？其他三根變成正的還是負的？
7. 卡住時按「重播」或「◀ 上一步」，同一步從頭再播一次。

## 下半場：換答案位置（約 30 分鐘）

1. 爸爸當藏寶人：在紙片上寫一個答案（00、01、10、11），蓋起來。
2. 孩子在列印包第 2 頁寫預測：標記之後四根長條、平均、一輪之後四根長條。
3. 打開動畫第 8 步（自由實驗），按答案按鈕選同一個答案，按「一鍵 Grover」；或自己依序按 H₁、H₂、Oracle、擴散，最後「量測 50 次」。
4. 打開 `grover_bars.py`，把最上面的 `ANSWER = '10'` 改成同一個答案，執行 `python grover_bars.py` 對照。
5. 加碼：開 `animations/basic-circuits.html#grover`，位元數選「3 顆（N = 8）」，重複輪數依序選「1 輪」「2 輪」「3 輪」，記下答案的機率；再對照程式最後的表格。
''',

'grover_bars.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 逐步圖參考答案（振幅依序是 00、01、10、11）\n\n| 列 | 做什麼 | 振幅 | 判定 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in ROWS)
  + '\n## grover_bars.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- 乘積態判斷：(a|0⟩ + b|1⟩)⊗(c|0⟩ + d|1⟩) 的四個振幅是 ac、ad、bc、bd，所以 a₀₀·a₁₁ = a₀₁·a₁₀ = abcd；不相等就拆不開。\n'
  '- 換答案位置：不論答案是哪一格，標記後都是三個 +½、一個 −½，平均都是 ¼，一輪後答案 = 1、其他 = 0。把 ANSWER 改成 01 實跑，一輪後量到 01 的機率也是 100.0 %。\n'
  '- 標記 00 的硬體做法：兩顆都先做 X → CZ → 兩顆再做 X（只把該位元是 0 的位元夾 X）。\n'
  '- 兩輪：答案 +½、其他 −½，四個機率又是各 25%（轉過頭）。四輪又回到 100%：N = 4 時起點角度 30°，每一輪轉 60°，四輪後到 270°，sin² 又是 1。\n'
  '- 位元多了：8 個選項 1 輪 78.1 %、2 輪 94.5 %、3 輪 33.0 %；16 個選項 3 輪 96.1 %、4 輪 58.2 %。最佳輪數約 (π/4)√N。\n'
  '- 動畫第 6 步的字幕寫「四個振幅都變成 −½」，但長條實際是答案 +½（金色）、其他 −½（紅色）；機率仍是各 25%，結論不變。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `transmon-3d.html#grover`（第 7 章：振幅長條，八步驟）

- 四根長條是 |00⟩、|01⟩、|10⟩、|11⟩ 的振幅（左邊那位是 Q1）；高度可正可負，負的是紅色；長條上方標著振幅與機率。
- 長條右邊即時顯示 a₀₀·a₁₁、a₀₁·a₁₀ 與判定（乘積態／糾纏，C = 2|a₀₀a₁₁ − a₀₁a₁₀|）；上方電路圖高亮正在送的閘。
- 步驟：1 糾纏（H⊗H → CZ → H(Q2)，量 40 次）→ 2 Grover 題目 → 3 Oracle（X(Q2) → CZ → X(Q2)）→ 4 擴散（金色平均線）→ 5 量測 50 次 → 6 轉過頭 → 7 Deutsch → 8 自由實驗。
- 第 8 步按鈕：答案 00／01／10／11；H₁、H₂、X₁、X₂、CZ、Oracle、擴散；「一鍵 Grover」「量測 50 次」「重設 |00⟩」。

## `basic-circuits.html#grover`（範例：Grover 搜尋）

- 上方選項：位元數「2 顆（N = 4）」「3 顆（N = 8）」；答案的每一位可以點一下切換；重複輪數「最佳」「1 輪」「2 輪」「3 輪」。
- 改選項後畫面停在最後一步，方便比較；「量測 1,000 次」看實際次數，灰色底是理論機率。

## `basic-circuits.html#bell`（範例：Bell 態）

- H 做出疊加，CNOT 把兩顆綁在一起；右邊兩顆的 Bloch 向量縮到球心，代表單看一顆完全隨機。
''',
}

SHEET_HEADER = ['藏寶人的答案', '預測：標記後四根（00/01/10/11）', '預測：平均', '預測：一輪後四根', '動畫結果', '程式結果', '和預測一樣嗎']
SHEET_ROWS = [['00'], ['01'], ['10'], ['11'], ['（加碼）3 位元 1 輪'], ['（加碼）3 位元 2 輪'], ['（加碼）3 位元 3 輪']]

EXTRA_CSS = '''table.steps td{height:22mm;padding:0 1mm}table.steps td.c{width:21mm;vertical-align:top}table.steps .z{height:11mm;border-bottom:1pt dashed #4a6a88}
table.steps th{font-size:9.5pt}table.steps td.n{font-size:9.5pt;width:26mm}table.steps td.j{width:24mm;font-size:9pt;color:#4a6a88}
table.rec td{height:10mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 grover_bars.py（隔離模式），確認輸出和影片、教材寫的數字一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'grover_bars.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
        assert out == RUN_OUTPUT, out
        p.write_text(PROGRAM.replace("ANSWER = '10'", "ANSWER = '01'"), encoding='utf-8')
        out01 = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                               env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
        assert '一輪後：量到 01 的機率 100.0 %' in out01, out01
    return out


def html():
    rows = ''.join(f'<tr><td class="n"><b>{a}</b><br>{b}</td><td class="c"><div class="z"></div></td><td class="c"><div class="z"></div></td><td class="c"><div class="z"></div></td><td class="c"><div class="z"></div></td><td class="j"></td></tr>'
                   for a, b, c, d in ROWS)
    pages = [
        '<h2>振幅長條逐步圖</h2><p class="lead">跟著 transmon-3d.html#grover 第 7 章：每一步先預測、畫長條（中線是 0，往上正、往下負），再看動畫對答案。</p>'
        '<p>開場先猜：四個箱子，古典做法最壞要開幾次？＿＿　Grover 要查幾次？＿＿</p>'
        '<table class="steps"><tr><th>步驟</th><th>|00⟩</th><th>|01⟩</th><th>|10⟩</th><th>|11⟩</th><th>乘積態／糾纏</th></tr>' + rows + '</table>',
        '<h2>換你改造：換答案位置</h2><p class="lead">藏寶人（爸爸）寫下答案；尋寶者（你）先預測，再用動畫第 8 步與 grover_bars.py 驗證。</p>'
        '<table class="rec"><tr><th>答案</th><th>標記後四根</th><th>平均</th><th>一輪後四根</th><th>動畫</th><th>程式</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS[:4]) + '</table>'
        '<pre class="code">ANSWER = \'10\'   # 改造區：換成 00、01、10 或 11\n\n執行：python grover_bars.py</pre>'
        '<h3>加碼：位元多了（basic-circuits.html#grover，3 顆位元）</h3>'
        '<table class="rec"><tr><th>輪數</th><th>我的預測</th><th>答案的機率</th></tr>'
        '<tr><td>1 輪</td><td></td><td></td></tr><tr><td>2 輪</td><td></td><td></td></tr><tr><td>3 輪</td><td></td><td></td></tr></table>',
        '<h2>三個容易錯的地方</h2><div class="box"><ul class="chk">'
        '<li>兩位元 Grover 剛好一輪 100%，是因為只有 4 個選項；多做一輪會轉過頭</li>'
        '<li>位元多了不一定剛好：8 個選項最好的是 2 輪（約 94.5%），不是 100%</li>'
        '<li>CZ 不改變任何機率，卻能把乘積態變成糾纏</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>Bell 態</h3>'
        '<p>量 1000 次，大約 00 有＿＿次、11 有＿＿次，01 和 10 有＿＿次。</p>'
        '<p>單看一顆：□ 完全隨機　□ 一定是 0　　兩顆一起看：□ 永遠相同　□ 隨機</p>'
        '<p>可以用糾纏超光速傳訊息嗎？□ 可以　□ 不行，因為＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>最後一關：教爸爸尋寶</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. CZ 只翻一個負號，為什麼兩顆位元就拆不開了？</p><div class="line"></div>'
        '<p>2. 標記和擴散各做了什麼，答案怎麼從 25% 變成 100%？</p><div class="line"></div>'
        '<p>3. 位元多了，為什麼不一定剛好？做太多輪會怎樣？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>不看稿說出乘積態的等式 a₀₀·a₁₁ = a₀₁·a₁₀</li><li>示範動畫第 7 章任一步，並解釋長條怎麼變</li>'
        '<li>說出擴散的規則：新振幅 = 2 × 平均 − 原振幅</li><li>指出一個限制：位元多了不一定剛好；多做會轉過頭</li>'
        '<li>替振幅長條逐步圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q106 糾纏與兩位元 Grover 列印包', '父子科技學院 量子電腦學程 Q106｜第 8 課：糾纏與兩位元 Grover', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q106-entanglement-grover', folder='Q106_糾纏與兩位元Grover', files=FILES,
        sheet=('03_換答案紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_糾纏與兩位元Grover.pdf', pack_pages=4,
        pack_needles=('振幅長條逐步圖', 'H(Q2)', '換答案位置', '容易錯', 'Bell 態', '最後一關'),
        authoring_dir=XINEW / 'authoring/q106', episode_dir='specials/q106-entanglement-grover',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；grover_bars.py 只需 Python 3）',
               'program': 'grover_bars.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'answer': '10', 'oneRound': 1.0, 'twoRounds': 0.25, 'n8': [0.781, 0.945, 0.330], 'n16Round3': 0.961},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q106/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q105 課堂教材：BV 比賽紀錄（程式對決）、可執行的 bv_duel.py、八振幅追蹤表、換密碼改造表、容易錯的地方、教爸爸檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#bv 與 basic-circuits.html#bv；程式只要 Python 3。
建置時會真的執行一次 bv_duel.py（原始設定，以及 SECRET = '110'、'011010' 與 NOISE = 0 三種改造），確認輸出和影片、教材寫的數字一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q105/classroom.py
"""
from pathlib import Path
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

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，固定亂數種子（SEED = 7），結果可重現
RUN_OUTPUT = '''密碼 s = 101（3 位元）
古典第 1 次：問 x = 100 → 回答 1
古典第 2 次：問 x = 010 → 回答 0
古典第 3 次：問 x = 001 → 回答 1
古典查詢 3 次 → 拼出 s = 101
① H 之後：   000:+0.354  001:+0.354  010:+0.354  011:+0.354  100:+0.354  101:+0.354  110:+0.354  111:+0.354
② 查詢 1 次： 000:+0.354  001:-0.354  010:+0.354  011:-0.354  100:-0.354  101:+0.354  110:-0.354  111:+0.354
③ 再 H 之後： 000:+0.000  001:+0.000  010:+0.000  011:+0.000  100:+0.000  101:+1.000  110:+0.000  111:+0.000
量測 1000 次（每顆位元讀錯 3%）：101 914 次、111 29 次、001 29 次、100 26 次
最多的是 101（91.4%）→ 猜中
查詢次數：古典 3 次，量子 1 次
'''
# 改造試跑：(要改的那一行, 輸出裡必須出現的字串)
VARIANTS = [
    ("SECRET = '110'", ('古典查詢 3 次 → 拼出 s = 110', '② 查詢 1 次： 000:+0.354  001:+0.354  010:-0.354  011:-0.354  100:-0.354  101:-0.354',
                        '110 914 次', '最多的是 110（91.4%）→ 猜中')),
    ("SECRET = '011010'", ('古典查詢 6 次 → 拼出 s = 011010', '011010 831 次', '最多的是 011010（83.1%）→ 猜中', '查詢次數：古典 6 次，量子 1 次')),
    ('NOISE = 0.0', ('101 1000 次', '最多的是 101（100.0%）→ 猜中')),
]

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q105：BV 密碼對決——古典逐位查詢 vs 量子只查詢一次（純 Python，不需要安裝任何套件）

執行：  python bv_duel.py
做法和學程動畫 transmon-3d.html 第 9 章相同：H⊗n → 黑盒子（只查詢一次）→ H⊗n → 量測。
"""
import math
import random

SECRET = '101'      # 改造區：換成你自己的密碼（只能用 0 和 1，幾位都可以，建議 3–6 位）
SHOTS = 1000        # 量子電路重跑幾次（每個 shot：重設 → 跑電路 → 讀一次）
NOISE = 0.03        # 每顆位元讀錯的機率（3% 是動畫裡的示意值；改成 0 就是理想機器）
SEED = 7            # 亂數種子：固定它，每次跑出來的結果都一樣


def oracle(x):
    """黑盒子：只回答 s·x 的奇偶（對應位元相乘、加總、取 mod 2）"""
    return sum(int(a) * int(b) for a, b in zip(SECRET, x)) % 2


def hadamard_all(amp, n):
    """每顆位元各做一次 H（哈達瑪閘）"""
    a = amp[:]
    for q in range(n):
        bit = 1 << q
        for i in range(len(a)):
            if not i & bit:
                x, y = a[i], a[i | bit]
                a[i], a[i | bit] = (x + y) / math.sqrt(2), (x - y) / math.sqrt(2)
    return a


def show(amp, n):
    """列出振幅；位元多於 3 顆時只列前 8 個"""
    t = '  '.join(f'{i:0{n}b}:{v:+.3f}' for i, v in enumerate(amp[:8]))
    return t + ('  …' if len(amp) > 8 else '')


if __name__ == '__main__':
    n = len(SECRET)
    print(f'密碼 s = {SECRET}（{n} 位元）')
    # 古典：一次問一位
    got = ''
    for k in range(n):
        x = ''.join('1' if j == k else '0' for j in range(n))
        r = oracle(x)
        got += str(r)
        print(f'古典第 {k + 1} 次：問 x = {x} → 回答 {r}')
    print(f'古典查詢 {n} 次 → 拼出 s = {got}')
    # 量子：振幅向量（2ⁿ 個數字）
    amp = [1.0] + [0.0] * (2 ** n - 1)
    amp = hadamard_all(amp, n)
    print('① H 之後：  ', show(amp, n))
    amp = [(-1) ** oracle(f'{i:0{n}b}') * v for i, v in enumerate(amp)]
    print('② 查詢 1 次：', show(amp, n))
    amp = hadamard_all(amp, n)
    amp = [0.0 if abs(v) < 1e-12 else v for v in amp]
    print('③ 再 H 之後：', show(amp, n))
    # 量測：依振幅² 抽樣，再加上讀取誤判
    rng = random.Random(SEED)
    prob = [v * v for v in amp]
    count = {}
    for _ in range(SHOTS):
        r, k = rng.random(), 0
        while k < len(prob) - 1 and r >= prob[k]:
            r -= prob[k]
            k += 1
        for q in range(n):
            if rng.random() < NOISE:
                k ^= 1 << q
        key = f'{k:0{n}b}'
        count[key] = count.get(key, 0) + 1
    top = sorted(count.items(), key=lambda kv: -kv[1])
    print(f'量測 {SHOTS} 次（每顆位元讀錯 {NOISE:.0%}）：' + '、'.join(f'{k} {c} 次' for k, c in top[:4]))
    best, c = top[0]
    print(f'最多的是 {best}（{c / SHOTS:.1%}）→ {"猜中" if best == SECRET else "沒猜中"}')
    print(f'查詢次數：古典 {n} 次，量子 1 次')
'''

# 八振幅追蹤（s = 101，由 bv_duel.py 實跑）：(步驟, 000…111 的正負號／值)
TRACE = [('① 三顆都做 H', ['+0.35'] * 8),
         ('② 查詢黑盒子一次', ['+0.35', '−0.35', '+0.35', '−0.35', '−0.35', '+0.35', '−0.35', '+0.35']),
         ('③ 再做一次 H', ['0', '0', '0', '0', '0', '1', '0', '0'])]
LABELS = ['000', '001', '010', '011', '100', '101', '110', '111']

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q105：第 7 課 BV 密碼——一次猜中三位元（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：黑盒子藏著一個 3 位元密碼 s，只回答 s·x 的奇偶；古典要一位一位問（3 次），Bernstein–Vazirani（BV）演算法只查詢 1 次。課堂用「程式對決」的方式：孩子是量子方、爸爸是古典方，比誰問得少。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#bv`（第 9 章）；加映 `basic-circuits.html#bv`（範例 7，教科書版）。免安裝、不需帳號 |
| 程式 | `bv_duel.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_BV密碼.pdf`（A4，共 4 頁） |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「3 位元密碼，最少要問幾次？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：s·x 的奇偶、古典逐位查詢、疊加／相位／干涉、八振幅追蹤 | 影片第 4–7 段、列印包第 2 頁 |
| 25–65 | 對決：第 9 章第 8 步，按「隨機（隱藏）」後，爸爸按「古典查詢一次」、孩子按「一鍵執行」，填比賽紀錄 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：換自己的密碼，讓爸爸用古典方法猜；改 `bv_duel.py` 的 SECRET、NOISE | `bv_duel.py`、列印包第 3 頁、`03_BV比賽紀錄.csv` |
| 105–115 | 孩子教爸爸：操作與原理，指出一個限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替比賽紀錄命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `transmon-3d.html#bv`，取消「自動接續」，按步驟按鈕 1–7 各看一次；左上方字幕會跟著動畫說明。第 8 步是自由實驗。
- 跑一次 `python bv_duel.py`，確認最後兩行是「最多的是 101（91.4%）→ 猜中」「查詢次數：古典 3 次，量子 1 次」。
- 讀一遍 `04_解答.md`。

## 對決規則

- 每一場先按「隨機（隱藏）」，誰都不知道密碼。古典方每按一次「古典查詢一次」算 1 次；量子方按「一鍵執行」算 1 次（或手動按 ①②③④，② 黑盒子才算查詢）。
- 先拼出完整密碼、而且答對的一方，記在比賽紀錄；查詢次數少的贏。
- 下半場換孩子出題：孩子自己設定密碼（例如 110），爸爸只能用「一次問一個 x、只聽奇偶」的方式猜。可以先口頭玩，再用程式驗證。

## 誠實說明

- BV 的優勢是**查詢次數**（n 次 → 1 次），不是什麼題目都變快；它全程沒有糾纏，古典電腦也能輕鬆模擬，是展示「疊加 → 相位 → 干涉」套路的示範題，不代表實際應用。
- 「6 個 H 約 100 ns、讀取約 1 μs」是學程文件的常見量級；3% 讀取誤判是動畫與程式的示意值。
- 程式的量測用固定亂數種子（SEED = 7），所以每次結果都一樣；改 SEED 會得到稍微不同的次數。動畫的量測每次隨機。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：程式對決（約 40 分鐘）

1. 用瀏覽器開 `animations/transmon-3d.html#bv`（第 9 章：BV 密碼）。
2. 先取消「自動接續」，按步驟按鈕「1」到「7」看一遍：題目與古典做法 → 均勻疊加 → 查詢黑盒子 → 干涉 → 量測 → 真實硬體 → 標準版與重點。
3. 按步驟按鈕「8」（自由實驗）。先選密碼「101」，依序按「① H⊗3」「② 黑盒子」「③ H⊗3」「④ 量測 50 次」，把每一步的八根長條抄進列印包第 2 頁。
4. 對決：按「隨機（隱藏）」→ 爸爸按「古典查詢一次」，直到拼出密碼（看上方看板）→ 孩子按「一鍵執行」→ 看左上角字幕揭曉。
5. 把面板「查詢次數」（量子 N 次 ／ 古典 M 次）和雙方的答案記進比賽紀錄。至少比 3 場。
6. 加碼：勾選「讀取雜訊」（每顆 3% 讀錯）再比一次，看量測統計是不是還有一根最突出。

## 加映：教科書版（約 10 分鐘，可選）

- `animations/basic-circuits.html#bv`：按「下一步 ▶」四次：X 閘 → 全部 H → 黑盒（CNOT）→ H；按「量測 1,000 次」。
- 點上方「s2=1」「s1=0」「s0=1」按鈕換密碼（例如改成 110），按「清除」再量一次，看 CNOT 換到哪幾條線。

## 下半場：換你設密碼（約 30 分鐘）

1. 孩子在紙上寫一個 3 位元密碼，藏起來。爸爸每次說一個 x（例如 100），孩子只回答 s·x 的奇偶（0 或 1），看爸爸要問幾次。
2. 打開 `bv_duel.py`，把最上面的 `SECRET = '101'` 改成自己的密碼，先在列印包第 3 頁寫預測，再執行 `python bv_duel.py`。
3. 改造：密碼改成 6 位元（例如 011010）；把 `NOISE` 改成 0 或 0.1；每次都先預測。
4. 想一想：密碼位數越多，古典要問幾次？量子呢？讀錯機率變大時，最多的那一個還會是密碼嗎？
''',

'bv_duel.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## s·x 的奇偶\n\n'
  '- s = 101、x = 111：1·1 + 0·1 + 1·1 = 2 → 偶數 → 回答 0。\n'
  '- 古典依序問 100、010、001：回答剛好是 s 的第 1、2、3 位（101）。n 位元密碼要問 n 次。\n\n'
  '## 八振幅追蹤（s = 101，由左到右 000～111）\n\n| 步驟 | ' + ' | '.join(LABELS) + ' |\n|---|' + '---|' * 8 + '\n'
  + ''.join(f'| {name} | ' + ' | '.join(v) + ' |\n' for name, v in TRACE)
  + '\n- 查詢後直接量：8 個結果仍各 12.5%，答案藏在正負號裡。\n'
  '- s = 110 時，查詢後變負號的是 010、011、100、101；s = 011 時是 001、010、101、110（x 和 s 對應位相乘加總為奇數者）。\n\n'
  '## bv_duel.py 實跑（Python 3.13.18，SEED = 7）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- 改造參考：SECRET = \'110\' → 110 出現 914 次；SECRET = \'011010\' → 古典 6 次、量子 1 次，011010 出現 831 次（83.1%）；NOISE = 0.0 → 101 出現 1000 次。\n'
  '- 位元越多，每顆 3% 讀錯累積起來，正確答案的比例會下降（3 位元約 91%、6 位元約 83%），但通常仍是最突出的那一個。\n'
  '- 常見誤解：BV 的優勢是查詢次數，不是什麼都快；全程沒有糾纏，古典電腦也能模擬，是示範題，不代表實際應用。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `transmon-3d.html#bv`（第 9 章：BV 密碼，八步驟）

- 步驟按鈕 1–8；「◀ 上一步」「暫停」「重播」「下一步 ▶」；「自動接續」核取方塊。
- 畫面：8 根長條是 |q1 q2 q3⟩ 的振幅（|000⟩～|111⟩），正的金色、負的紅色，標籤寫振幅和機率；上方看板左邊是電路、右邊是推導；左上方字幕跟著說明。
- 第 8 步（自由實驗）：密碼按鈕 000～111、「隨機（隱藏）」；「① H⊗3」「② 黑盒子」「③ H⊗3」「④ 量測 50 次」；「一鍵執行」「古典查詢一次」「重設」；「讀取雜訊」（每顆 3%）。面板有「密碼 s」「查詢次數」「量測最多」與量測統計。

## `basic-circuits.html#bv`（範例 7：教科書版）

- q0–q2 是輸入、q3 是輔助位元：X 閘 → 全部 H（q3 變成 |−⟩）→ 黑盒（密碼為 1 的位元各接一條 CNOT 到 q3）→ 再對 q0–q2 做 H。
- 振幅柱：往上是正（藍）、往下是負（橘）；最後只剩兩根，因為 q3 一直停在 |−⟩。
- 「密碼 s（s2 s1 s0，點一下切換）」可換密碼；「量測 1 次」「量測 1,000 次」「清除」。

## 操作

滑鼠拖曳旋轉、滾輪縮放；transmon-3d 按 ←→ 切換章節。
''',
}

SHEET_HEADER = ['場次', '密碼誰設的', '古典方查詢次數', '古典拼出的密碼', '量子方查詢次數', '量子量到最多的', '揭曉的密碼', '誰贏', '備註（雜訊？位數？）']
SHEET_ROWS = [['1', '電腦（隨機隱藏）'], ['2', '電腦（隨機隱藏）'], ['3', '電腦（讀取雜訊）'], ['4', '孩子'], ['5', '孩子（6 位元）'], ['6', '']]

EXTRA_CSS = '''table.rec td{height:10mm}table.rec th{white-space:nowrap;font-size:9.5pt}table.amp td,table.amp th{text-align:center;font-size:10.5pt;height:9mm}
.chk li{margin:2.5mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def run_program(text):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'bv_duel.py'
        p.write_text(text, encoding='utf-8')
        return subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                              env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout


def check_program():
    """真的跑 bv_duel.py（隔離模式）：原始設定的輸出要逐字相同，三種改造要出現教材寫的數字。"""
    out = run_program(PROGRAM)
    assert out == RUN_OUTPUT, out
    for line, needles in VARIANTS:
        key = line.split(' =')[0]
        text, n = re.subn(rf'^{key} = \S+', line, PROGRAM, count=1, flags=re.M)
        assert n == 1, line
        o = run_program(text)
        for s in needles:
            assert s in o, (line, s, o)
    return out


def html():
    th = ''.join(f'<th>{x}</th>' for x in LABELS)
    trace = ''.join(f'<tr><th>{name}</th>' + ''.join(f'<td>{v}</td>' for v in vals) + '</tr>' for name, vals in TRACE[:1]) + \
        ''.join(f'<tr><th>{name}</th>' + '<td></td>' * 8 + '</tr>' for name, _ in TRACE[1:])
    blank = ''.join(f'<tr><th>{name}</th>' + '<td></td>' * 8 + '</tr>' for name, _ in TRACE)
    pages = [
        '<h2>BV 比賽紀錄（程式對決）</h2><p class="lead">transmon-3d.html#bv 第 8 步：先按「隨機（隱藏）」，爸爸按「古典查詢一次」，孩子按「一鍵執行」。</p>'
        '<p>開場先猜：3 位元密碼，古典最少要問＿＿次？量子要問＿＿次？　10 位元呢？古典＿＿次，量子＿＿次</p>'
        '<table class="rec"><tr><th>場次</th><th>密碼誰設的</th><th>古典問幾次</th><th>古典拼出</th><th>量子問幾次</th><th>量子量到最多</th><th>揭曉密碼</th><th>誰贏</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<p class="note">規則：古典方每按一次「古典查詢一次」算 1 次；量子方按「② 黑盒子」或「一鍵執行」算 1 次。</p>',
        '<h2>八振幅追蹤表</h2><p class="lead">密碼 s = 101。先預測，再按 ①②③ 對照動畫的八根長條（正的金色、負的紅色）。</p>'
        '<h3>黑盒子只回答奇偶：s = 101、x = 111</h3><p>1·1 ＋ 0·1 ＋ 1·1 ＝ ＿＿　→ 奇數還是偶數？＿＿　→ 黑盒子回答＿＿</p>'
        f'<table class="amp"><tr><th>步驟</th>{th}</tr>{trace}</table>'
        '<p>查詢後直接量，每個結果的機率是＿＿%。答案藏在哪裡？＿＿＿＿＿＿＿＿</p>'
        '<h3>換你：密碼 s = ＿＿＿（自己設定）</h3>'
        f'<table class="amp"><tr><th>步驟</th>{th}</tr>{blank}</table>'
        '<p class="note">提示：查詢後，x 和 s 對應位相乘加總是奇數的，翻成負號。</p>',
        '<h2>換你設密碼：改 bv_duel.py</h2><p class="lead">先預測，再執行 python bv_duel.py，把輸出抄進表格。</p>'
        '<pre class="code">SECRET = \'101\'   # 改造區：換成你自己的密碼（只能用 0 和 1）\nSHOTS = 1000     # 重跑幾次\nNOISE = 0.03     # 每顆位元讀錯的機率\nSEED = 7         # 亂數種子</pre>'
        '<table class="rec"><tr><th>SECRET</th><th>NOISE</th><th>我的預測</th><th>古典問幾次</th><th>量子問幾次</th><th>最多的是（%）</th><th>猜中？</th></tr>'
        '<tr><td>101</td><td>0.03</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>（自己的）</td><td>0.03</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>（6 位元）</td><td>0.03</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>101</td><td>0</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>101</td><td>0.1</td><td></td><td></td><td></td><td></td><td></td></tr></table>'
        '<p class="note">位數越多，古典要問幾次？量子呢？讀錯機率變大時，最多的那一個還是密碼嗎？＿＿＿＿＿＿＿＿</p>',
        '<h2>容易錯的地方 ＋ 教爸爸</h2><div class="box"><ul class="chk">'
        '<li>查詢後直接量看不出答案：8 個結果仍各 12.5%，要再做一次 H 干涉</li>'
        '<li>優勢是查詢次數（n 次 → 1 次），不是什麼題目都變快</li>'
        '<li>全程沒有糾纏，古典電腦也能模擬：是示範題，不代表實際應用</li>'
        '<li>真實晶片有雜訊：101 不會剛好 100%，重複很多次是為了確認哪個最突出</li></ul>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 黑盒子回答的是什麼？古典為什麼要問 3 次？</p><div class="line"></div>'
        '<p>2. 疊加、相位、干涉，各在哪一步出場？</p><div class="line"></div>'
        '<ul class="chk"><li>示範動畫第 9 章第 8 步一場對決，並解釋畫面</li><li>指出一個限制</li><li>替比賽紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q105 BV 密碼 列印包', '父子科技學院 量子電腦學程 Q105｜第 7 課：BV 密碼——一次猜中三位元', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q105-bv-secret', folder='Q105_BV密碼', files=FILES,
        sheet=('03_BV比賽紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_BV密碼.pdf', pack_pages=4,
        pack_needles=('BV 比賽紀錄', '八振幅追蹤表', 'bv_duel.py', '容易錯', '教爸爸'),
        authoring_dir=XINEW / 'authoring/q105', episode_dir='specials/q105-bv-secret',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；bv_duel.py 只需 Python 3）',
               'program': 'bv_duel.py', 'testedWith': 'Python 3.13.18 (standard library only, SEED = 7)',
               'recordedRun': {'secret': '101', 'classicalQueries': 3, 'quantumQueries': 1, 'shots': 1000, 'noise': 0.03,
                               'correctCount': 914, 'sixBitCorrectCount': 831},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q105/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

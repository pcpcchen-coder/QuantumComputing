"""Q061 課堂教材：精度實驗表、解鎖成就卡、分布記錄表、可執行的 qpe_lab.py、說明卡與解答。

不需要帳號；qpe_lab.py 只用 Python 標準函式庫就能跑（有裝 qiskit 與 qiskit-aer 時，加參數 qiskit 會改用真正的相位估計線路）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q061/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q061：QFT 與相位估計 的小模擬器

執行：python qpe_lab.py              → 精度實驗：θ = 3/8 與 1/3，用 3、4、5 個計數位元各跑 1000 次
      python qpe_lab.py 分布 0.3      → 改造：自己選一個相位（單位：圈），印出三種位元數的直方圖
      python qpe_lab.py 成就          → 解鎖成就：電腦偷偷選相位，你從量測結果猜答案
      python qpe_lab.py qiskit 0.3    → 有裝 qiskit 與 qiskit-aer 時，用真正的相位估計線路跑
相位 θ 的單位是「圈」：θ = 1 代表轉一整圈。估計值 = 量到的整數 y ÷ 2ⁿ。
只用 Python 標準函式庫（qiskit 模式除外）。
"""
import cmath
import math
import random
import sys


def probs(theta, n):
    """理想相位估計（n 個計數位元）量到 y 的機率：|(1/2ⁿ) Σ_k e^{2πik(θ − y/2ⁿ)}|²。"""
    N = 2 ** n
    out = []
    for y in range(N):
        s = sum(cmath.exp(2j * math.pi * k * (theta - y / N)) for k in range(N)) / N
        out.append(abs(s) ** 2)
    return out


def run(theta, n, shots=1000, rng=random):
    p = probs(theta, n)
    counts = [0] * len(p)
    for y in rng.choices(range(len(p)), weights=p, k=shots):
        counts[y] += 1
    return counts


def report(theta, n, counts):
    N = 2 ** n
    y = max(range(N), key=lambda k: counts[k])
    est = y / N
    err = min(abs(est - theta), 1 - abs(est - theta))   # 相位是一圈一圈的，0 和 1 是同一點
    return y, est, err


def table(seed=61):
    rng = random.Random(seed)
    for theta, name in ((3 / 8, '3/8'), (1 / 3, '1/3')):
        print(f'相位 θ = {name} ≈ {theta:.4f} 圈')
        print('位元數｜格子｜最多次的 y（次數）｜估計 y ÷ 2ⁿ｜誤差｜最多次那格的理論機率')
        for n in (3, 4, 5):
            c = run(theta, n, 1000, rng)
            y, est, err = report(theta, n, c)
            print(f'{n}｜1/{2 ** n}｜{y}（{c[y]}）｜{est:.4f}｜{err:.4f}｜{probs(theta, n)[y]:.3f}')
        print()
    print('能整除（3/8）時每次都讀對；除不盡（1/3）時會散開，但每多一個位元，誤差大約減半。')


def histogram(theta, seed=61):
    rng = random.Random(seed)
    for n in (3, 4, 5):
        c = run(theta, n, 1000, rng)
        y, est, err = report(theta, n, c)
        print(f'--- {n} 個計數位元（格子 1/{2 ** n} 圈）：最多次 y = {y}，估計 {est:.4f}，誤差 {err:.4f}')
        for k, v in enumerate(c):
            if v:
                print(f'y = {k:2d}（{k}/{2 ** n} = {k / 2 ** n:.4f}）{v:4d} ' + '█' * (v // 20))
    print('看一看：哪一種位元數最集中？θ 離最近的格子有多遠（θ × 2ⁿ 和整數差多少）？')


def achievement():
    n = random.choice((3, 4, 5))
    theta = random.choice((random.randrange(2 ** n) / 2 ** n, random.random()))
    c = run(theta, n, 1000)
    print(f'電腦偷偷選了一個相位，用 {n} 個計數位元跑了 1000 次：')
    for k, v in enumerate(c):
        if v >= 10:
            print(f'  y = {k}：{v} 次')
    guess = input(f'你猜 θ 是幾圈？（可以寫成分數，例如 3/{2 ** n}）：').strip()
    try:
        a, _, b = guess.partition('/')
        g = float(a) / float(b) if b else float(a)
    except ValueError:
        print('看不懂這個答案。'); return
    ok = abs(g - theta) <= 1 / 2 ** n
    print(f'真正的 θ = {theta:.4f} 圈；你猜 {g:.4f}。', '解鎖成就！蓋一個章。' if ok else '差了超過一格，再試一次。')


def with_qiskit(theta):
    from qiskit import QuantumCircuit, transpile
    from qiskit.circuit.library import QFTGate
    from qiskit_aer import AerSimulator
    sim = AerSimulator(seed_simulator=61)
    for n in (3, 4, 5):
        qc = QuantumCircuit(n + 1, n)
        qc.x(n)                                   # 目標位元放在 |1⟩：受控相位閘的「本徵態」
        qc.h(range(n))                            # ① 疊加
        for j in range(n):                        # ② 相位回踢：第 j 顆控制 U 的 2^j 次方
            qc.cp(2 * math.pi * theta * 2 ** j, j, n)
        qc.append(QFTGate(n).inverse(), range(n))  # ③ 反向 QFT
        qc.measure(range(n), range(n))            # ④ 量測
        counts = sim.run(transpile(qc, sim), shots=1000).result().get_counts()
        top = sorted(((int(k, 2), v) for k, v in counts.items()), key=lambda kv: -kv[1])[:4]
        print(f'{n} 個計數位元：前幾名 (y, 次數) = {top}；估計 {top[0][0] / 2 ** n:.4f}')


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else ''
    val = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
    if arg in ('分布', 'hist'):
        histogram(val)
    elif arg in ('成就', 'game'):
        achievement()
    elif arg == 'qiskit':
        with_qiskit(val)
    else:
        table()
'''

ns = {}
exec(compile(PROGRAM, 'qpe_lab.py', 'exec'), ns)  # 用同一份程式算解答，避免手抄錯


def _rows(theta):
    out = ''
    for n in (3, 4, 5):
        p = ns['probs'](theta, n)
        y = max(range(2 ** n), key=lambda k: p[k])
        est = y / 2 ** n
        out += f'| {n} | 1/{2 ** n} | {y} | {est:.4f} | {abs(est - theta):.4f} | {p[y]:.3f} |\n'
    return out


ANS = {name: _rows(t) for name, t in (('3/8', 3 / 8), ('1/3', 1 / 3), ('0.3', 0.3))}

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q061：QFT 與相位估計（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心一句：**量子傅立葉轉換讓相位互相干涉；相位估計靠它把藏在相位裡的數字 θ 變成量得到的整數 y，估計值是 y ÷ 2ⁿ。計數位元每多一顆，格子就細一半。** 但 QFT 本身不是加速來源，它要搭配有結構的問題（藏著一個相位或一個週期）才有用。好玩機制是解鎖成就：每過一關就在成就卡上蓋章。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開 operation.html#circuit，選「量子傅立葉轉換」一步一步執行；operation.html#interference 把相位轉到 120° | 列印包第 1 頁（精度實驗表） |
| 25–65 | 用 `qpe_lab.py`（或 Qiskit）做 θ = 3/8 與 1/3 的 3、4、5 位元相位估計，填精度實驗表；玩解鎖成就 | 列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 改造：選一個不能整除的相位（例如 0.3），畫三種位元數的直方圖 | 列印包第 3 頁、`qpe_lab.py 分布 0.3` |
| 105–115 | 孩子教爸爸：原理、精度和位元數的關係、一個限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_QFT與相位估計.pdf`（A4，共 4 頁）。第 2 頁成就卡沿虛線剪開。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#circuit`、`operation.html#interference`、`operation.html#shor`，不需要帳號。
- 電腦有 Python 3 就能執行 `qpe_lab.py`（不用安裝套件）。有 qiskit 與 qiskit-aer 的話，`python qpe_lab.py qiskit 0.3` 會用真正的相位估計線路。
- 讀一遍 `04_解答.md`。

## 誠實說明

- `qpe_lab.py` 的標準模式用相位估計的精確機率公式抽樣，等於理想無雜訊的線路；真實硬體還有閘與讀取錯誤。
- 「最接近那格的機率至少約 40%」是理論下界 4/π² ≈ 0.405；實際機率看相位離格子多遠。
- 受控操作次數 1 + 2 + 4 + … = 2ⁿ − 1 是「重複套用 U」的算法；有些 U 的高次方可以直接做得更便宜。
''',

'01_操作步驟.md': '''# 操作步驟

## 先看動畫（約 15 分鐘）

1. `animations/operation.html#circuit`：按「量子傅立葉轉換（QFT，輸入 |110⟩）」，一直按「單步 ▶」。第 1 步只剩 |110⟩ 一根柱子；第 8 步（SWAP）後八根柱子一樣矮、顏色（相位）輪流變；第 9 步量測，右下小圖八個結果差不多一樣多——光做 QFT 讀不出 6。
2. `animations/operation.html#interference`：滑桿「A：相位 φ」拉到 0°、180°、120°。這就是一個位元的相位估計：120°（1/3 圈）時 P(0) = 0.25、P(1) = 0.75。
3. `animations/operation.html#shor`：按三次「下一步 ▶」看到間隔 4 的梳子，再按一次看 QFT 把它變成 0、16、32、48 四根尖峰（第五步留到下一堂）。

## 精度實驗（約 40 分鐘）

1. 執行 `python qpe_lab.py`，把 θ = 3/8 與 θ = 1/3 的結果填進精度實驗表。
2. 用 Qiskit 寫（`python qpe_lab.py qiskit 0.3333` 也可以）：
   ```python
   qc = QuantumCircuit(n + 1, n)
   qc.x(n)
   qc.h(range(n))
   for j in range(n):
       qc.cp(2 * math.pi * theta * 2 ** j, j, n)
   qc.append(QFTGate(n).inverse(), range(n))
   qc.measure(range(n), range(n))
   ```
3. 解鎖成就：爸爸從成就卡選一關，偷偷設定相位（或執行 `python qpe_lab.py 成就` 讓電腦選），只說要用幾個計數位元；孩子從最多次的 y 推回 θ，差不到一格就蓋章。

## 改造：除不盡的相位（約 30 分鐘）

1. 執行 `python qpe_lab.py 分布 0.3`（或換成自己選的相位）。
2. 在分布記錄表畫出三種位元數的直方圖，寫下最多次的 y、估計值和誤差。
3. 算一算 θ × 2ⁿ 離最近的整數多遠，解釋為什麼某一種位元數特別集中。
''',

'qpe_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用，理想機率由 `qpe_lab.py` 的公式算出）\n\n'
  '表頭：位元數｜格子｜最可能的 y｜估計 y ÷ 2ⁿ｜誤差｜那一格的機率\n\n'
  '## θ = 3/8\n\n| n | 格子 | y | 估計 | 誤差 | 機率 |\n|---|---|---|---|---|---|\n' + ANS['3/8'] +
  '\n## θ = 1/3\n\n| n | 格子 | y | 估計 | 誤差 | 機率 |\n|---|---|---|---|---|---|\n' + ANS['1/3'] +
  '\n（qiskit-aer 固定種子 61 實跑 1000 次：3 位元 y = 3 有 680 次、4 位元 y = 5 有 687 次、5 位元 y = 11 有 677 次。）\n\n'
  '## 改造 θ = 0.3\n\n| n | 格子 | y | 估計 | 誤差 | 機率 |\n|---|---|---|---|---|---|\n' + ANS['0.3'] +
  '\n0.3 × 16 = 4.8，離整數 5 只差 0.2 格；0.3 × 8 = 2.4、0.3 × 32 = 9.6 都差 0.4 格，所以 4 位元最集中。'
  '注意 5 位元的誤差沒有比 4 位元小：剛好 4 位元的格子更貼近 0.3，但 5 位元保證的誤差上限（半格 = 1/64 圈）比較小。\n\n'
  '## 重點\n\n'
  '- QFT：把數字寫進相位（|x⟩ → 每格轉 x/2ⁿ 圈），只用 H、受控相位閘與 SWAP，n 位元約 n(n+1)/2 個閘（n = 3 時 6 個）。\n'
  '- 相位估計：疊加 → 受控 U 的 1、2、4…次方（相位回踢）→ 反向 QFT（干涉）→ 量測 y，θ ≈ y ÷ 2ⁿ。\n'
  '- θ 能寫成 y/2ⁿ 時一定讀對；否則最接近那格的機率至少 4/π² ≈ 40.5%。\n\n'
  '## 常見誤解\n\n'
  '- 「QFT 本身就是加速」：量測只拿到一個結果，轉換後的 2ⁿ 個數值讀不出來；要搭配有結構的問題（相位估計的相位、Shor 的週期）。\n'
  '- 「位元越多越好，不用代價」：5 位元的受控 U 要套用 1 + 2 + 4 + 8 + 16 = 31 次，線路變深、錯誤也變多。\n'
  '- 「量一次就知道相位」：除不盡時結果會散開，要跑很多次看分布。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要帳號。

## `animations/operation.html#circuit`（場景 6：量子線路，課綱指定）

- 範例按鈕「量子傅立葉轉換（QFT，輸入 |110⟩）」；「⏮ 重設」「單步 ▶」「播放」；開關「加入雜訊」。
- 下方柱子：高度 = 機率、顏色 = 相位；最後的量測欄跑 1000 shots，右下小圖是直方圖（青線 = 理想機率）。

## `animations/operation.html#interference`（場景 8：干涉）

- 「單一量子位元：兩條路徑」模式：H → 相位 φ（紫色方塊）→ H。滑桿「A：相位 φ」；右上 P(0)、下方 P(1)；右下小圖是 P(0) 對 φ 的干涉條紋。

## `animations/operation.html#shor`（場景 10：Shor 週期尋找）

- 「下一步 ▶」逐步執行：① 疊加 ② 計算 f(x) ③ 量測第二暫存器（梳子）④ QFT（尖峰）⑤ 量測與連分數。本課只看到第 ④ 步；完整流程是下一堂的主題。

## 操作

滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換場景。
''',
}

SHEET_HEADER = ['相位 θ（圈）', '計數位元數', '格子（圈）', '最多次的 y', '次數', '估計 y ÷ 2ⁿ', '誤差', '解鎖了哪個成就']
SHEET_ROWS = [[t, str(n)] for t in ('3/8', '1/3', '0.3', '自選') for n in (3, 4, 5)]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:4mm 5mm;height:64mm;text-align:center}
.cards h3{font-size:14pt;margin:0 0 2mm}.cards .big{font-size:22pt;font-weight:700;color:#0b2540;margin:2mm 0}.cards p{margin:1mm 0;font-size:11pt}
.cards .stamp{display:inline-block;width:15mm;height:15mm;border:1.5px dashed #888;border-radius:50%;margin-top:2mm}
table.rc td{height:9mm;text-align:center}table.rc th{text-align:center;font-size:9.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.bt td,table.bt th{text-align:center;font-size:11.5pt}
.hist{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}.hist .h{border:1px solid #999;height:62mm;padding:2mm;font-size:10pt}'''

CARDS = [('讀出精準相位', '能整除的相位，一次讀對', '例：3 位元、θ = 3/8'),
         ('格子變細', '同一個相位，多加一顆位元', '說出誤差變成多少'),
         ('除不盡也不怕', '相位夾在兩格中間', '說出最可能的兩個答案'),
         ('看穿分布', '畫出 3、4、5 位元的直方圖', '說出哪一種最集中、為什麼'),
         ('資源算帳', '算出受控 U 要套用幾次', '例：5 位元是 31 次'),
         ('小老師', '不看稿教爸爸 QFT 與相位估計', '再指出一個限制')]


def html():
    cards = ''.join(f'<div class="cut"><h3>成就卡</h3><p class="big">{t}</p><p>{a}</p><p>{b}</p>'
                    '<span class="stamp"></span></div>' for t, a, b in CARDS)
    rows = ''.join(f'<tr><td>{t}</td><td>{n}</td><td>1/{2 ** n}</td><td></td><td></td><td></td><td></td></tr>'
                   for t in ('3/8', '1/3') for n in (3, 4, 5))
    pages = [
        '<h2>精度實驗表</h2><p class="lead">相位估計：量到整數 y，估計 θ ≈ y ÷ 2ⁿ（單位：圈）。計數位元每多一顆，格子細一半。</p>'
        '<table class="rc"><tr><th>相位 θ</th><th>計數位元</th><th>格子</th><th>最多次的 y</th><th>次數<br>（/1000）</th>'
        '<th>估計<br>y ÷ 2ⁿ</th><th>誤差</th></tr>'
        f'{rows}</table>'
        '<div class="box" style="margin-top:5mm"><h3>相位估計四步</h3>'
        '<p>① 疊加：計數位元全做 H　② 相位回踢：受控 U、U²、U⁴…　③ 反向 QFT：讓相位互相干涉　④ 量測：θ ≈ y ÷ 2ⁿ</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>記住兩件事</h3>'
        '<p>1. 能整除的相位一定讀對；除不盡時結果會散開，最接近那格的機率至少約 40%。</p>'
        '<p>2. 精度要用資源換：5 位元的受控 U 要套用 1 + 2 + 4 + 8 + 16 = 31 次。</p>'
        '<p class="note">QFT 本身不是加速來源；它要搭配有結構的問題（藏著一個相位或週期）才有用。</p></div>',
        '<h2>解鎖成就卡</h2><p class="lead">沿虛線剪開。每完成一關，就在圓圈裡蓋章或簽名。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>分布記錄表：除不盡的相位</h2><p class="lead">我選的相位 θ = ＿＿＿＿ 圈。用 3、4、5 個計數位元各跑 1000 次，畫出直方圖。</p>'
        '<div class="hist"><div class="h">3 位元（格子 1/8）</div><div class="h">4 位元（格子 1/16）</div><div class="h">5 位元（格子 1/32）</div></div>'
        '<table class="bt" style="margin-top:4mm"><tr><th>位元數</th><th>θ × 2ⁿ</th><th>離最近整數</th><th>最多次的 y</th><th>那格次數</th><th>誤差</th></tr>'
        '<tr><td>3</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>4</td><td></td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>5</td><td></td><td></td><td></td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:4mm"><p>哪一種位元數最集中？為什麼？</p><div class="line"></div></div>',
        '<h2>說明卡：我的相位估計精度實驗</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. QFT 與相位估計在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：QFT 怎麼用干涉把相位變成數字？</li>'
        '<li>說出相位估計的四步，以及 θ ≈ y ÷ 2ⁿ</li>'
        '<li>示範精度實驗：位元越多，格子越細、誤差約減半</li>'
        '<li>指出一個限制：QFT 本身不是加速來源，要搭配有結構的問題</li>'
        '<li>替精度實驗取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q061 QFT 與相位估計 列印包', '父子科技學院 量子電腦學程 Q061｜QFT 與相位估計', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q061-qft-phase-estimation', folder='Q061_QFT與相位估計', files=FILES,
        sheet=('03_精度實驗記錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_QFT與相位估計.pdf', pack_pages=4,
        pack_needles=('精度實驗表', '成就卡', '分布記錄表', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q061', episode_dir='specials/q061-qft-phase-estimation',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'qpe_lab.py', 'achievementCards': [c[0] for c in CARDS],
               'qftFrom': 'animations/js/operation/06_circuit.js', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q061/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

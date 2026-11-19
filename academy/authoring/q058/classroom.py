"""Q058 課堂教材：基底對照卡、盲測題卡、基底判讀表、可執行的 basis_lab.py、說明卡與解答。

不需要帳號、不需要安裝套件（basis_lab.py 只用 Python 標準函式庫；也可以只用動畫場景與紙卡）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q058/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q058：量測基底與期望值 的小模擬器（只用 Python 標準函式庫）

執行：python basis_lab.py            → 印出每個狀態在 Z、X、Y 基底的理論期望值與一次模擬（1000 shots）
      python basis_lab.py 盲測        → 電腦偷偷出題，你選基底、看統計、猜答案
規則和硬體一樣：最後一定「量 Z」。
  - 量 Z：直接量
  - 量 X：先做 H 再量 Z
  - 量 Y：先做 S†，再做 H，再量 Z
期望值 = P(0) − P(1) = (0 的次數 − 1 的次數) / shots
改造區：在 STATES 加你自己的狀態（θ 是從北極倒下的角度，φ 是繞赤道轉的相位，單位都是度）。
"""
import cmath
import math
import random
import sys

STATES = {   # 名稱: (θ, φ)
    '|0⟩ 零態': (0, 0),
    '|1⟩ 一態': (180, 0),
    '|+⟩ 加態': (90, 0),
    '|−⟩ 減態': (90, 180),
    '|+i⟩ 虛數方向': (90, 90),
    '倒下 60°': (60, 0),
    '動畫場景 7 的 θ=90°': (90, math.degrees(0.4)),   # operation.html#readout 的準備狀態相位固定 0.4 rad
}

R2 = 1 / math.sqrt(2)
H = ((R2, R2), (R2, -R2))
SDG = ((1, 0), (0, -1j))


def prepare(theta, phi):
    t, p = math.radians(theta), math.radians(phi)
    return [complex(math.cos(t / 2)), cmath.exp(1j * p) * math.sin(t / 2)]


def apply(g, v):
    return [g[0][0] * v[0] + g[0][1] * v[1], g[1][0] * v[0] + g[1][1] * v[1]]


def rotate_for(basis, v):
    """量測前的基底旋轉：Z 不動、X 先 H、Y 先 S† 再 H。"""
    if basis == 'X':
        v = apply(H, v)
    elif basis == 'Y':
        v = apply(H, apply(SDG, v))
    return v


def p0(basis, v):
    return abs(rotate_for(basis, v)[0]) ** 2


def run(basis, v, shots=1000, rng=random):
    n0 = sum(rng.random() < p0(basis, v) for _ in range(shots))
    return n0, shots - n0


def expectation(n0, n1):
    return (n0 - n1) / (n0 + n1)


def table(seed=58):
    rng = random.Random(seed)
    print('狀態｜基底｜理論 P(0)｜理論期望值｜模擬 1000 shots（0 / 1）｜模擬期望值')
    for name, (th, ph) in STATES.items():
        v = prepare(th, ph)
        for b in 'ZXY':
            q = p0(b, v)
            n0, n1 = run(b, v, 1000, rng)
            print(f'{name}｜{b}｜{q:.3f}｜{round(2 * q - 1, 6) + 0.0:+.3f}｜{n0} / {n1}｜{expectation(n0, n1):+.3f}')
    print('\n提醒：模擬期望值每次會差一點點；shots 越多越接近理論值（下一堂會算要多少 shots）。')


def blind():
    names = ['|0⟩ 零態', '|1⟩ 一態', '|+⟩ 加態', '|−⟩ 減態']
    secret = random.choice(names)
    v = prepare(*STATES[secret])
    print('電腦偷偷從 ' + '、'.join(names) + ' 選了一個。每次輸入 Z 或 X（可以重複），輸入 猜 結束。')
    while True:
        b = input('基底（Z／X／猜）：').strip().upper()
        if b in ('Z', 'X'):
            n0, n1 = run(b, v, 100)
            print(f'  量 {b}（{"直接量" if b == "Z" else "先 H 再量 Z"}）100 次：0 → {n0}，1 → {n1}，期望值 {expectation(n0, n1):+.2f}')
        elif b in ('猜', 'G'):
            g = input('你猜是哪一個（0／1／+／−）：').strip().replace('-', '−')
            ok = {'0': names[0], '1': names[1], '+': names[2], '−': names[3]}.get(g) == secret
            print('答對了！' if ok else '答錯了，', '答案是', secret)
            return


if __name__ == '__main__':
    blind() if len(sys.argv) > 1 and sys.argv[1] in ('盲測', 'blind') else table()
'''

ns = {}
exec(compile(PROGRAM, 'basis_lab.py', 'exec'), ns)  # 用同一份程式算解答，避免手抄錯


def ideal(name, b):
    v = ns['prepare'](*ns['STATES'][name])
    return round(2 * ns['p0'](b, v) - 1, 6) + 0.0


ANS_ROWS = ''.join(f'| {n.replace("|", chr(92) + "|")} | ' + ' | '.join(f'{ideal(n, b):+.3f}' for b in 'ZXY') + ' |\n' for n in ns['STATES'])

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q058：量測基底與期望值（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心一句：**硬體只會量 Z（是 0 還是 1）；想量 X，量之前先做 H；想量 Y，先做 S† 再做 H。量完的計數可以算成期望值：⟨Z⟩ = P(0) − P(1)。** 好玩機制是盲測：爸爸偷偷選 |0⟩、|1⟩、|+⟩、|−⟩ 其中一個，孩子只能選基底、看統計，猜出答案。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開 operation.html#readout，θ 設 90°，切換「量 Z」「量 X」「量 Y」 | 列印包第 1 頁（基底對照卡） |
| 25–65 | 在場景比較 Z、X 基底；玩盲測（場景 2 或 `basis_lab.py 盲測`），填基底判讀表 | 列印包第 2、3 頁 |
| 65–75 | 休息 | |
| 75–105 | 改造：用 `basis_lab.py` 算 \\|0⟩、\\|+⟩、倒下 60° 的 ⟨Z⟩、⟨X⟩，和場景讀數對照 | 列印包第 3 頁、`basis_lab.py` |
| 105–115 | 孩子教爸爸：為什麼要先轉、怎麼算、哪裡容易錯 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_量測基底與期望值.pdf`（A4，共 4 頁）。第 2 頁盲測題卡沿虛線剪開、對折蓋住。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#readout`（場景 7）與 `operation.html#gates`（場景 2），不需要帳號。
- 電腦有 Python 3 就能執行 `basis_lab.py`（不用安裝套件）。也可以用任何本機量子模擬器，記得量 X 前加 H。
- 讀一遍 `04_解答.md`。

## 誠實說明

- 場景 7 的準備狀態相位固定 0.4 弧度（約 23°），所以 θ = 90° 不是正好 |+⟩：量 X 的理想期望值是 0.921，不是 1。`basis_lab.py` 裡有這個狀態可以對照。
- 場景 7 預設打開「讀取期間 T₁ 衰減」與「讀取誤差緩解」，讀數會和理想值差一點；讀取誤差是下一堂的主題。
- 理想情況下「先 H 再量 |+⟩，1000 次全是 0」；真實硬體約有 0.5%～3% 的讀取錯誤。
''',

'01_操作步驟.md': '''# 操作步驟

## 先看動畫（約 15 分鐘）

1. 打開 `animations/operation.html#readout`（場景 7：讀取與統計）。
2. 把「準備狀態 θ」拉到 90°。按「量 Z（直接量）」：IQ 平面上藍、紅兩團點差不多一樣多。
3. 按「量 X（先 H）」：讀取鏈最前面的「基底旋轉」方塊寫著 H，新的點幾乎都在藍色（0）那一團。
4. 把左邊面板捲到最下面，看「⟨X⟩ = …（理想 0.921）」。再按「量 Y（先 S†H）」，理想值變成多少？
5. 把 θ 改成 0°、60°、180°，每次三個基底都量一遍，記在基底判讀表。

## 盲測（約 40 分鐘）

1. 爸爸抽一張題卡（|0⟩、|1⟩、|+⟩、|−⟩），不給孩子看。
2. 爸爸在 `operation.html#gates`（場景 2）照題卡做出狀態：|0⟩＝「重設 |0⟩」、|1⟩＝「重設 |1⟩」、|+⟩＝「重設 |0⟩」＋H、|−⟩＝「重設 |1⟩」＋H。孩子先轉過頭去。
3. 孩子只能說「量 Z」或「量 X」：量 Z 就直接看面板的測量機率；量 X 就先按一次 H 再看。
4. 也可以讓電腦出題：執行 `python basis_lab.py 盲測`。
5. 猜對換人出題；每一題都寫進基底判讀表。

## 改造：用模擬器算（約 30 分鐘）

1. 執行 `python basis_lab.py`，找出 |0⟩、|+⟩、倒下 60° 的 Z、X 期望值。
2. 用公式自己算一次：期望值 = (0 的次數 − 1 的次數) ÷ shots。
3. 和場景 7 的讀數對照：θ = 60° 時場景的 ⟨X⟩ 理想值為什麼是 0.798 而不是 0.866？（提示：場景的相位固定 0.4 弧度）
''',

'basis_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 理論期望值（由 `basis_lab.py` 算出）\n\n'
  '| 狀態 | ⟨Z⟩ | ⟨X⟩ | ⟨Y⟩ |\n|---|---|---|---|\n' + ANS_ROWS +
  '\n## 盲測判讀（P(0)，理想情況）\n\n'
  '| 狀態 | 量 Z | 量 X（先 H） | 判讀 |\n|---|---|---|---|\n'
  '| \\|0⟩ | 全是 0 | 各一半 | Z 全 0 |\n'
  '| \\|1⟩ | 全是 1 | 各一半 | Z 全 1 |\n'
  '| \\|+⟩ | 各一半 | 全是 0 | Z 各半、X 全 0 |\n'
  '| \\|−⟩ | 各一半 | 全是 1 | Z 各半、X 全 1 |\n\n'
  '## 重點\n\n'
  '- 硬體只量 Z。量 X 前先做 H（H 把 |+⟩ 變 |0⟩、|−⟩ 變 |1⟩）；量 Y 前先做 S† 再做 H。\n'
  '- 期望值 ⟨Z⟩ = P(0) − P(1)，一定在 −1 到 +1；它就是 Bloch 球上箭頭的高度。\n'
  '- 範例：1000 shots，0 有 250 次、1 有 750 次 → ⟨Z⟩ = 0.25 − 0.75 = −0.5（場景 1 的 θ = 120°）。\n'
  '- 場景 7 的 θ = 90°：⟨Z⟩ 理想 0.000、⟨X⟩ 理想 0.921、⟨Y⟩ 理想 0.389（相位固定 0.4 弧度）。\n\n'
  '## 常見誤解\n\n'
  '- 「量 X 就是直接量」：忘了先做 H，量到的還是 Z，就是在量錯的東西。\n'
  '- 「期望值是某一次會量到的結果」：每次只會得到 0 或 1；−0.5 是很多次的平均。\n'
  '- 「跑幾次就夠」：次數太少誤差很大（100 shots 時 ⟨Z⟩ 的誤差約 ±0.1），下一堂會算。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要帳號。

## `animations/operation.html#readout`（場景 7：讀取與統計，課綱指定）

- 左邊面板：「準備狀態 θ」、三個基底按鈕「量 Z（直接量）」「量 X（先 H）」「量 Y（先 S†H）」、積分時間、雲間距、閾值、「連續 shots」「讀取期間 T₁ 衰減」「讀取誤差緩解」。
- 中間上排是讀取鏈：基底旋轉（寫著 —、H 或 S†H）→ 讀取腔 → 放大器 → ADC＋積分；下面是 IQ 平面（藍＝判成 0、紅＝判成 1，粉紅色是閾值）。
- 面板最下面的讀數要捲動才看得到：「⟨X⟩ = …（理想 …）」。

## `animations/operation.html#qubit`（場景 1）與 `#gates`（場景 2）

- 場景 1：θ 滑桿、「一次跑 1000 shots」，柱子上的數字就是次數，可以算期望值。
- 場景 2：「重設 |0⟩」「重設 |1⟩」「H」，面板最下面有測量機率；盲測用它出題。

## 操作

滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換場景。
''',
}

SHEET_HEADER = ['題號', '準備的狀態（出題者寫）', '量測基底', '量測前先做', 'shots', '0 的次數', '1 的次數', '期望值 P(0)−P(1)', '我猜的狀態', '對／錯']
SHEET_ROWS = [[str(k)] for k in range(1, 11)]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:4mm 5mm;height:56mm;text-align:center}
.cards h3{font-size:14pt;margin:0 0 2mm}.cards .big{font-size:30pt;font-weight:700;color:#0b2540;margin:2mm 0}.cards p{margin:1mm 0;font-size:11pt}
table.rc td{height:9.5mm;text-align:center}table.rc th{text-align:center;font-size:9.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.bt td,table.bt th{text-align:center;font-size:12pt}'''

CARDS = [('|0⟩', '零態', '重設 |0⟩'), ('|1⟩', '一態', '重設 |1⟩'), ('|+⟩', '加態', '重設 |0⟩ → H'), ('|−⟩', '減態', '重設 |1⟩ → H'),
         ('|0⟩', '零態（第二張）', '重設 |0⟩'), ('|−⟩', '減態（第二張）', '重設 |1⟩ → H')]


def html():
    cards = ''.join(f'<div class="cut"><h3>盲測題卡</h3><p class="big">{k}</p><p>{n}</p><p>場景 2 做法：{how}</p>'
                    '<p>對折蓋住，不給偵探看</p></div>' for k, n, how in CARDS)
    rows = ''.join(f'<tr><td>{k}</td><td></td><td>□Z □X</td><td></td><td></td><td></td><td></td><td></td></tr>' for k in range(1, 11))
    pages = [
        '<h2>基底對照卡</h2><p class="lead">硬體只會量 Z（是 0 還是 1）。想量別的方向，量測前先旋轉，把想問的方向轉到 Z。</p>'
        '<table class="bt"><tr><th>想量的方向</th><th>量測前先做</th><th>為什麼</th></tr>'
        '<tr><td>Z（零一）</td><td>直接量</td><td>|0⟩、|1⟩ 本來就在上下軸</td></tr>'
        '<tr><td>X（正負）</td><td>H</td><td>H：|+⟩ → |0⟩，|−⟩ → |1⟩</td></tr>'
        '<tr><td>Y（虛數方向）</td><td>S† 再 H</td><td>|+i⟩ → |+⟩ → |0⟩</td></tr>'
        '<tr><td>Z⊗Z（兩位元奇偶）</td><td>各自量 Z</td><td>結果相乘</td></tr></table>'
        '<div class="box" style="margin-top:5mm"><h3>期望值怎麼算</h3>'
        '<p style="font-size:15pt;font-weight:700">⟨Z⟩ ＝ P(0) − P(1) ＝（0 的次數 − 1 的次數）÷ shots</p>'
        '<p>例：1000 shots，0 有 250 次、1 有 750 次 → 0.25 − 0.75 ＝ −0.5。期望值一定在 −1 到 +1，就是 Bloch 球上箭頭的高度。</p>'
        '<p>量 X 時一樣用這個公式，只是量之前先做了 H，算出來的是 ⟨X⟩。</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>盲測規則</h3>'
        '<p>1. 出題者從 |0⟩、|1⟩、|+⟩、|−⟩ 抽一張題卡，偷偷做出狀態。</p>'
        '<p>2. 偵探只能說「量 Z」或「量 X」，每次看一組統計（例如 100 shots）。</p>'
        '<p>3. 用最少組統計猜出答案；猜對換人出題。</p>'
        '<p class="note">提醒：量 X 前一定要先做 H；忘了旋轉，就是在量錯的東西。</p></div>',
        '<h2>盲測題卡</h2><p class="lead">沿虛線剪開，對折後蓋住。出題者照「場景 2 做法」在 operation.html#gates 做出狀態。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>基底判讀表</h2><p class="lead">每一題記下基底、次數與期望值。期望值 ＝（0 的次數 − 1 的次數）÷ shots。</p>'
        '<table class="rc"><tr><th>題</th><th>準備的狀態<br>（出題者寫）</th><th>基底</th><th>shots</th><th>0 的<br>次數</th>'
        '<th>1 的<br>次數</th><th>期望值</th><th>我猜的<br>狀態</th></tr>'
        f'{rows}</table>'
        '<div class="box" style="margin-top:4mm"><p>改造：模擬器算出來的期望值</p>'
        '<table class="bt"><tr><th>狀態</th><th>⟨Z⟩</th><th>⟨X⟩</th><th>場景 7 讀數</th></tr>'
        '<tr><td>|0⟩</td><td></td><td></td><td></td></tr><tr><td>|+⟩</td><td></td><td></td><td></td></tr>'
        '<tr><td>倒下 60°</td><td></td><td></td><td></td></tr></table></div>',
        '<h2>說明卡：我的基底判讀表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 量測基底與期望值在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：為什麼硬體只能量 Z？</li>'
        '<li>示範：量 X 前先做 H，|+⟩ 變成全部是 0</li>'
        '<li>用計數算一次期望值：P(0) − P(1)</li>'
        '<li>指出一個錯誤：量 X 前要先做 H；忘了旋轉就是在量錯的東西</li>'
        '<li>替基底判讀表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q058 量測基底與期望值 列印包', '父子科技學院 量子電腦學程 Q058｜量測基底與期望值', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q058-basis-expectation', folder='Q058_量測基底與期望值', files=FILES,
        sheet=('03_基底判讀表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量測基底與期望值.pdf', pack_pages=4,
        pack_needles=('基底對照卡', '盲測題卡', '基底判讀表', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q058', episode_dir='specials/q058-basis-expectation',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'basis_lab.py', 'blindCards': [c[0] for c in CARDS], 'bases': ['Z', 'X', 'Y'],
               'basisTableFrom': 'slides/QC_Operation_Talk.pptx p31', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q058/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q060 課堂教材：主動重置任務卡、冒險任務關卡卡、症狀判讀表、可執行的 dynamic_lab.py、說明卡與解答。

不需要帳號；dynamic_lab.py 只用 Python 標準函式庫就能跑（有裝 qiskit 與 qiskit-aer 時，加參數 qiskit 會改用真正的動態線路 if_test）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q060/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q060：動態線路 的小模擬器

執行：python dynamic_lab.py            → 主動重置：零態、一態、加態、倒下 60° 各跑 1000 次，比較「有回饋」和「沒有回饋」
      python dynamic_lab.py 冒險        → 冒險任務：電腦偷偷選起點，你寫條件，最後 1000 次全是 0 就過關
      python dynamic_lab.py 症狀        → 三位元重複碼：故意翻錯一顆，看兩顆輔助位元的症狀
      python dynamic_lab.py qiskit      → 有裝 qiskit 與 qiskit-aer 時，用真正的中途量測＋if_test 跑主動重置與症狀量測
主動重置的線路：準備狀態 → 中途量測 → 量到 1 就做 X（翻轉閘）→ 再量一次。
只用 Python 標準函式庫（qiskit 模式除外）。
"""
import math
import random
import sys

STARTS = {   # 名稱: 從北極倒下的角度 θ（度）；量到 1 的機率 = sin²(θ/2)
    '|0⟩ 零態': 0,
    '|1⟩ 一態': 180,
    '|+⟩ 加態': 90,
    '倒下 60°': 60,
}


def p1(theta):
    return math.sin(math.radians(theta) / 2) ** 2


def active_reset(theta, shots=1000, feedback=True, rng=random):
    """回傳 (第一次量到 0 的次數, 第一次量到 1 的次數, 第二次量到 0 的次數, 第二次量到 1 的次數)。"""
    a0 = a1 = b0 = b1 = 0
    for _ in range(shots):
        first = 1 if rng.random() < p1(theta) else 0   # 中途量測：狀態塌縮成 0 或 1
        a1 += first
        a0 += 1 - first
        bit = first
        if feedback and first == 1:                    # 前饋：量到 1 就做 X
            bit = 0
        b1 += bit
        b0 += 1 - bit
    return a0, a1, b0, b1


def table(seed=60):
    rng = random.Random(seed)
    print('起點｜回饋｜第一次量測（0 / 1）｜第二次量測（0 / 1）')
    for name, th in STARTS.items():
        for fb in (True, False):
            a0, a1, b0, b1 = active_reset(th, 1000, fb, rng)
            print(f'{name}｜{"有" if fb else "沒有"}｜{a0} / {a1}｜{b0} / {b1}')
    print('\n有回饋時第二次量測全部是 0；沒有回饋時，第二次量測和第一次一樣（量過就塌縮了）。')


def adventure():
    name = random.choice(list(STARTS))
    th = STARTS[name]
    print('關主（電腦）偷偷選了一個起點。你只能中途量一次，再決定量到 0、量到 1 各要做什麼。')
    r0 = input('量到 0 時要做什麼？（輸入 X 或 不做）：').strip().upper()
    r1 = input('量到 1 時要做什麼？（輸入 X 或 不做）：').strip().upper()
    ok = 0
    for _ in range(1000):
        bit = 1 if random.random() < p1(th) else 0
        if (bit == 0 and r0 == 'X') or (bit == 1 and r1 == 'X'):
            bit ^= 1
        ok += bit == 0
    print(f'最後量 1000 次：0 有 {ok} 次、1 有 {1000 - ok} 次。', '過關！' if ok == 1000 else '還沒過關，再想想條件。')
    print('關主選的起點是', name)


def syndrome(data):
    """三顆資料位元 data = [q1, q2, q3]；輔助一比 1、2 號，輔助二比 2、3 號（相同得 0，不同得 1）。"""
    return data[0] ^ data[1], data[1] ^ data[2]


FIX = {(0, 0): None, (1, 0): 0, (1, 1): 1, (0, 1): 2}   # 症狀 → 要修第幾顆（0 起算）


def syndrome_demo():
    print('資料位元一開始都是 000（重複碼的邏輯 0）。')
    for wrong in (None, 0, 1, 2):
        data = [0, 0, 0]
        if wrong is not None:
            data[wrong] ^= 1
        s = syndrome(data)
        fix = FIX[s]
        after = data[:]
        if fix is not None:
            after[fix] ^= 1
        tag = '沒有翻錯' if wrong is None else f'故意翻錯 {wrong + 1} 號'
        print(f'{tag}：資料 {data} → 症狀（輔助一, 輔助二）= {s} → ' + ('不用修' if fix is None else f'修 {fix + 1} 號') + f' → {after}')
    print('改造：同時翻錯兩顆（例如 1、2 號），症狀會指到哪裡？修完變成什麼？')


def with_qiskit():
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    sim = AerSimulator()
    qc = QuantumCircuit(1, 2)
    qc.h(0)
    qc.measure(0, 0)
    with qc.if_test((qc.clbits[0], 1)):
        qc.x(0)
    qc.measure(0, 1)
    print(qc.draw())
    print('主動重置（位元字串左邊是第二次量測）：', sim.run(qc, shots=1000).result().get_counts())
    q = QuantumCircuit(5, 5)   # 0、1、2 是資料位元，3、4 是輔助位元
    q.x(1)                      # 故意把 2 號翻錯
    q.cx(0, 3); q.cx(1, 3); q.cx(1, 4); q.cx(2, 4)
    q.measure(3, 3); q.measure(4, 4)
    with q.if_test((q.clbits[3], 1)):
        with q.if_test((q.clbits[4], 1)):
            q.x(1)
    q.measure([0, 1, 2], [0, 1, 2])
    print('症狀量測＋修正（左兩位是輔助二、輔助一，右三位是資料 3、2、1 號）：', sim.run(q, shots=200).result().get_counts())


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else ''
    {'冒險': adventure, 'adventure': adventure, '症狀': syndrome_demo, 'syndrome': syndrome_demo,
     'qiskit': with_qiskit}.get(arg, table)()
'''

ns = {}
exec(compile(PROGRAM, 'dynamic_lab.py', 'exec'), ns)  # 用同一份程式算解答，避免手抄錯
SYN_ROWS = ''
for wrong in (None, 0, 1, 2):
    data = [0, 0, 0]
    if wrong is not None:
        data[wrong] ^= 1
    s = ns['syndrome'](data)
    fix = ns['FIX'][s]
    SYN_ROWS += f'| {"沒有" if wrong is None else str(wrong + 1) + " 號"} | {"".join(map(str, data))} | {s[0]} | {s[1]} | {"不用修" if fix is None else str(fix + 1) + " 號"} |\n'
P1_ROWS = ''.join(f'| {n.replace("|", chr(92) + "|")} | {ns["p1"](t):.2f} | 約 {round(1000 * ns["p1"](t))} 次做 X | 全是 0 | 約 {round(1000 * ns["p1"](t))} 次是 1 |\n'
                  for n, t in ns['STARTS'].items())

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q060：動態線路（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心一句：**動態線路在中途量一部分位元，再依結果（古典位元）馬上決定後面的閘；最簡單的例子是主動重置：量到 1 就做 X 翻回 0。** 回饋一定要在相干時間內完成，延遲本身就會造成錯誤。好玩機制是冒險任務：關主藏起點，勇者只能中途量一次、寫好條件，最後 1000 次全是 0 就過關。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開 atoms.html#zoned 按「中途量測」；basic-circuits.html#teleport 看第 4 步的修正 | 列印包第 1 頁（任務卡） |
| 25–65 | 在模擬器做主動重置線路（`dynamic_lab.py` 或 Qiskit），比較有、沒有回饋；玩冒險任務 | 列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 改造：三位元重複碼＋兩顆輔助位元的症狀量測，故意翻錯一顆、填症狀判讀表 | 列印包第 3 頁、`dynamic_lab.py 症狀` |
| 105–115 | 孩子教爸爸：原理、主動重置三步、為什麼要快 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_動態線路.pdf`（A4，共 4 頁）。第 2 頁關卡卡沿虛線剪開。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `atoms.html#zoned`、`basic-circuits.html#teleport`、`operation.html#qec`，不需要帳號。
- 電腦有 Python 3 就能執行 `dynamic_lab.py`（不用安裝套件）。有 qiskit 與 qiskit-aer 的話，`python dynamic_lab.py qiskit` 會用真正的 `if_test`。
- 讀一遍 `04_解答.md`。

## 誠實說明

- `dynamic_lab.py` 的標準模式是把「中途量測後塌縮成 0 或 1」直接用亂數模擬，適合單顆位元的主動重置與只有翻轉錯誤的重複碼；一般的動態線路請用 qiskit 模式或其他模擬器。
- 理想模擬裡「第二次量測全是 0」；真實硬體有讀取錯誤（約 0.5%～3%），讀錯就會補錯閘。
- 「判別與決策約數百奈秒、主動重置約 1–5 μs、被動等待數百 μs」是簡報的代表值，各機型不同。
''',

'01_操作步驟.md': '''# 操作步驟

## 先看動畫（約 15 分鐘）

1. `animations/atoms.html#zoned`：按「中途量測」，最前面一排原子被搬到讀取區、拍螢光、再補新原子。看右下角小圖：中途讀取 1 ms，並行 CZ 只要 0.3 μs。
2. `animations/basic-circuits.html#teleport`：按「下一步」走到第 4 步，讀說明：真實做法是先量 q0、q1，再依結果對 q2 做 X、Z；動畫用受控閘代替（延遲量測原理）。按「量測 1,000 次」，q2 約 75% 是 0。
3. `animations/operation.html#qec`：關掉「自動循環」，按「下一步」四次：錯誤 → 症狀 → 解碼 → 修正。

## 主動重置（約 40 分鐘）

1. 執行 `python dynamic_lab.py`，看四個起點「有回饋」「沒有回饋」的兩次量測次數。
2. 用 Qiskit 寫（簡報第 28 頁的寫法）：
   ```python
   qc = QuantumCircuit(1, 2)
   qc.h(0)
   qc.measure(0, 0)
   with qc.if_test((qc.clbits[0], 1)):
       qc.x(0)
   qc.measure(0, 1)
   ```
3. 冒險任務：爸爸當關主，從 |0⟩、|1⟩、|+⟩ 選一個起點（或執行 `python dynamic_lab.py 冒險` 讓電腦選）；孩子當勇者，只能中途量一次，寫好「量到 0／量到 1 各做什麼」。最後 1000 次全是 0 就過關。

## 改造：重複碼症狀量測（約 30 分鐘）

1. 三顆資料位元（1、2、3 號）都從 0 開始，兩顆輔助位元也從 0 開始。
2. 受控反閘：1 號→輔助一、2 號→輔助一（輔助一記下 1、2 號是否相同）；2 號→輔助二、3 號→輔助二。
3. 只量兩顆輔助位元，填症狀判讀表；再故意翻錯一顆試一次（`python dynamic_lab.py 症狀`）。
''',

'dynamic_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 主動重置（理想情況，1000 次）\n\n'
  '| 起點 | 第一次量到 1 的機率 | 有回饋 | 有回饋：第二次量測 | 沒有回饋：第二次量測 |\n|---|---|---|---|---|\n' + P1_ROWS +
  '\n（加態實跑例：qiskit-aer 固定種子 7，第一次 499 次 0、501 次 1，第二次 1000 次全是 0。）\n\n'
  '## 症狀判讀表（由 `dynamic_lab.py` 算出）\n\n'
  '| 翻錯的位元 | 資料（1、2、3 號） | 輔助一 | 輔助二 | 要修 |\n|---|---|---|---|---|\n' + SYN_ROWS +
  '\n同時翻錯兩顆時症狀會指錯：例如 1、2 號都錯 → 症狀 (0, 1) → 修 3 號 → 變成 111，三顆都錯（維基百科 Bit-flip code 也舉這個例子）。\n\n'
  '## 重點\n\n'
  '- 動態線路：中途量測一部分位元，依結果（古典位元）決定後面的閘（前饋）。\n'
  '- 用途：主動重置、隱形傳態的 X／Z 修正、錯誤更正每輪量症狀、重複直到成功。\n'
  '- 延遲量測原理：可以把「量完再補閘」改成受控閘、量測挪到最後，機率分佈相同；代價是位元要留到最後。\n\n'
  '## 常見誤解\n\n'
  '- 「回饋可以慢慢來」：等待時位元還在衰減；T₁ ≈ 90 μs 時多等 1 μs，衰減機率約 1 − e^(−1/90) ≈ 1.1%。\n'
  '- 「中途量測不影響被量的位元」：被量的那顆會塌縮，疊加就沒了。\n'
  '- 「讀取一定對」：讀錯就會補錯閘。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要帳號。

## `animations/atoms.html#zoned`（原子場景 11：分區架構與並行閘，課綱指定）

- 上方儲存區、中間糾纏區、下方讀取區；按鈕「▶ 執行一層」「中途量測」「重置」、滑桿「並行對數」。
- 「中途量測」：抓起第 4 列 → 搬到讀取區 → 螢光成像 → 補充新原子。右下小圖：一層的時間組成（搬運 250 μs、CZ 0.3 μs、中途讀取 1 ms）。

## `animations/basic-circuits.html#teleport`（範例 5：量子隱形傳態）

- 「下一步」逐步執行；第 4 步方框「修正（2 個古典位元）」用受控閘代替「量測後再修正」。下方兩顆 Bloch 球是「單看 q0」「單看 q2」；右邊可以量測 q2。

## `animations/operation.html#qec`（場景 11：錯誤更正）

- 「d = 3／5／7」、實體錯誤率滑桿、「自動循環」、「下一步」、「跑 2000 輪（只統計）」。每一輪：錯誤（紅球）→ 症狀（橘色柱子）→ 解碼（綠線）→ 修正。

## 操作

滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換場景。
''',
}

SHEET_HEADER = ['題號', '翻錯的位元（出題者寫）', '輔助一（比 1、2 號）', '輔助二（比 2、3 號）', '我判斷要修', '修完的資料', '對／錯']
SHEET_ROWS = [[str(k)] for k in range(1, 11)]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:4mm 5mm;height:56mm;text-align:center}
.cards h3{font-size:14pt;margin:0 0 2mm}.cards .big{font-size:30pt;font-weight:700;color:#0b2540;margin:2mm 0}.cards p{margin:1mm 0;font-size:11pt}
table.rc td{height:9.5mm;text-align:center}table.rc th{text-align:center;font-size:9.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.bt td,table.bt th{text-align:center;font-size:12pt}'''

CARDS = [('|0⟩', '零態', '什麼都不做'), ('|1⟩', '一態', 'qc.x(0)'), ('|+⟩', '加態', 'qc.h(0)'),
         ('|0⟩', '零態（第二張）', '什麼都不做'), ('|1⟩', '一態（第二張）', 'qc.x(0)'), ('|+⟩', '加態（第二張）', 'qc.h(0)')]


def html():
    cards = ''.join(f'<div class="cut"><h3>關卡卡</h3><p class="big">{k}</p><p>{n}</p><p>準備方法：{how}</p>'
                    '<p>關主收好，不給勇者看</p></div>' for k, n, how in CARDS)
    rows = ''.join(f'<tr><td>{k}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for k in range(1, 11))
    pages = [
        '<h2>主動重置任務卡</h2><p class="lead">動態線路：在中途量一部分位元，依結果（古典位元）馬上決定後面的閘。</p>'
        '<table class="bt"><tr><th>步驟</th><th>做什麼</th><th>Qiskit</th></tr>'
        '<tr><td>① 量測</td><td>先量一次</td><td>qc.measure(0, 0)</td></tr>'
        '<tr><td>② 判斷</td><td>結果是 1 嗎？</td><td>with qc.if_test((qc.clbits[0], 1)):</td></tr>'
        '<tr><td>③ 回饋</td><td>是 1 就做 X（翻轉閘）</td><td>　　qc.x(0)</td></tr>'
        '<tr><td>④ 驗收</td><td>再量一次</td><td>qc.measure(0, 1)</td></tr></table>'
        '<div class="box" style="margin-top:5mm"><h3>為什麼要快</h3>'
        '<p>判別與決策約數百 ns；主動重置約 1–5 μs，被動等待要數百 μs。</p>'
        '<p>等待時位元還在衰減：T₁ ≈ 90 μs 時，多等 1 μs 約 1% 機會衰減。延遲本身就會造成錯誤。</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>冒險任務規則</h3>'
        '<p>1. 關主抽一張關卡卡，偷偷在模擬器準備起點。</p>'
        '<p>2. 勇者不看準備的程式，只能中途量一次，寫好「量到 0、量到 1 各做什麼」。</p>'
        '<p>3. 最後量 1000 次全是 0 就過關；再挑戰拿掉回饋，看會失敗幾次。</p>'
        '<p class="note">提醒：讀錯就會補錯閘；被量過的位元疊加就沒了。</p></div>',
        '<h2>冒險任務關卡卡</h2><p class="lead">沿虛線剪開，對折後蓋住。關主照「準備方法」在線路最前面準備起點。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>症狀判讀表</h2><p class="lead">三顆資料位元（1、2、3 號）＋兩顆輔助位元。輔助一比 1、2 號，輔助二比 2、3 號；相同得 0，不同得 1。</p>'
        '<table class="rc"><tr><th>題</th><th>翻錯的位元<br>（出題者寫）</th><th>輔助一</th><th>輔助二</th>'
        '<th>我判斷<br>要修</th><th>修完的<br>資料</th><th>對／錯</th></tr>'
        f'{rows}</table>'
        '<div class="box" style="margin-top:4mm"><p>挑戰：同時翻錯兩顆，症狀指到哪裡？修完變成什麼？</p>'
        '<table class="bt"><tr><th>翻錯</th><th>輔助一</th><th>輔助二</th><th>修完</th></tr>'
        '<tr><td>1、2 號</td><td></td><td></td><td></td></tr><tr><td>2、3 號</td><td></td><td></td><td></td></tr></table></div>',
        '<h2>說明卡：我的主動重置線路</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 動態線路在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：動態線路和一般線路差在哪裡？</li>'
        '<li>示範主動重置：量到 1 就做 X，第二次量測全是 0</li>'
        '<li>用症狀找出翻錯的那一顆</li>'
        '<li>指出一個限制：回饋要在相干時間內完成，延遲本身就會造成錯誤</li>'
        '<li>替主動重置線路取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q060 動態線路 列印包', '父子科技學院 量子電腦學程 Q060｜動態線路', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q060-dynamic-circuits', folder='Q060_動態線路', files=FILES,
        sheet=('03_症狀判讀表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_動態線路.pdf', pack_pages=4,
        pack_needles=('主動重置任務卡', '關卡卡', '症狀判讀表', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q060', episode_dir='specials/q060-dynamic-circuits',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'dynamic_lab.py', 'adventureCards': [c[0] for c in CARDS],
               'dynamicCircuitFrom': 'slides/QC_Operation_Talk.pptx p13, p28', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q060/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q055 課堂教材：兩種實現對照表、角色扮演卡、原生閘對照表、可執行的 twoqubit_lab.py、說明卡與解答。

不需要帳號、不需要安裝套件（twoqubit_lab.py 只用 Python 標準函式庫；也可以只用動畫）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q055/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 兩種實現對照表（列印包第 1 頁；解答見 04_解答.md）
COMPARE = [  # (比較項目, 磁通調頻 CZ, 交叉共振 CR)
    ('代表架構', '可調頻率（Google 等）', '固定頻率（IBM 早期）'),
    ('調整或驅動什麼', '用磁通脈衝把 A 的頻率往下拉', '用 B 的頻率去驅動 A（只送微波）'),
    ('物理機制', '|11⟩ 靠近 |20⟩，迴避交叉把 |11⟩ 推低，只有 |11⟩ 多累積相位', '因耦合，B 繞 ±x 旋轉，方向由 A 決定（ZX）'),
    ('直接得到的閘', 'CZ：|11⟩ → −|11⟩', 'ZX(π/2)，加單位元修正 = CNOT'),
    ('典型時間（簡報 p23）', '約 40–70 ns', '約 200–500 ns'),
    ('要另外修正的', '其他態的單位元相位（虛擬 Z）', '單位元旋轉（修正成 CNOT）'),
    ('容易出錯的地方', '太靠近交叉點或太快 → 洩漏到 |20⟩', '頻率配置要合適；閘比較慢'),
]

# 原生兩位元閘（學程簡報 p24；各平台依世代而異，以官方文件為準）
NATIVE = [  # (平台, 原生兩位元閘, 架構特點)
    ('IBM Eagle', 'ECR（由交叉共振構成）', '固定頻率、重六角耦合'),
    ('IBM Heron', 'CZ（另有分數角 RZZ）', '可調耦合器'),
    ('Google Sycamore／Willow', 'CZ（或 √iSWAP 類）', '可調頻率＋可調耦合器、方格'),
    ('Rigetti', 'CZ／iSWAP', '可調耦合器'),
    ('離子阱（參考）', 'MS／ZZ', '全連接、閘較慢'),
]

ROLES = [  # (情境, 爸爸（控制 A）, 你（目標 B）, 正確動作)
    ('交叉共振①', '舉 0，喊「送出微波」', '手臂從頭頂往下倒 90°', '往左倒（動畫左邊的球）'),
    ('交叉共振②', '舉 1，喊「送出微波」', '手臂從頭頂往下倒 90°', '往右倒（動畫右邊的球）'),
    ('CZ①', '舉 1', '舉 0', '都不動（|10⟩ 不變）'),
    ('CZ②', '舉 1', '舉 1', '兩人一起喊「負號！」（|11⟩ → −|11⟩）'),
]

PROGRAM = '''"""父子科技學院 量子電腦學程 Q055：兩位元閘小實驗室（只用 Python 標準函式庫）

執行：python twoqubit_lab.py
一、CZ 和 CNOT 作用在四個基底態上；CNOT = (I⊗H)·CZ·(I⊗H)。
二、交叉共振：目標 B 的旋轉方向由控制 A 決定。
三、照 operation.html#twoqubit（05_twoqubit.js）的模型，改「脈衝深度」，看條件相位、閘時間與能階間距。
模型是教學用的簡化，只用來比較趨勢。
"""
import math

S = 1 / math.sqrt(2)
KETS = ['00', '01', '10', '11']   # 左邊是 A，右邊是 B


def mat_vec(m, v):
    return [sum(m[i][j] * v[j] for j in range(4)) for i in range(4)]


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def kron(a, b):
    return [[a[i // 2][j // 2] * b[i % 2][j % 2] for j in range(4)] for i in range(4)]


I2 = [[1, 0], [0, 1]]
H2 = [[S, S], [S, -S]]
CZ = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]
CNOT = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]

print('一、CZ 只讓 |11⟩ 多一個負號')
for k, name in enumerate(KETS):
    v = [0, 0, 0, 0]
    v[k] = 1
    out = mat_vec(CZ, v)
    print(f'  CZ |{name}⟩ = {"−" if out[k] < 0 else "+"}|{name}⟩')
IH = kron(I2, H2)
built = mat_mul(mat_mul(IH, CZ), IH)
same = all(abs(built[i][j] - CNOT[i][j]) < 1e-12 for i in range(4) for j in range(4))
print(f'  (I⊗H)·CZ·(I⊗H) 等於 CNOT 嗎？ {same}')

print('\\n二、交叉共振：B 從北極出發，轉 90°')
for a in (0, 1):
    ang = math.pi / 2 * (1 if a == 0 else -1)      # A=0 繞 +x、A=1 繞 −x（同動畫）
    y, z = -math.sin(ang), math.cos(ang)           # 北極 (0,0,1) 繞 x 轉 ang
    side = '−y（動畫畫面往左）' if y < 0 else '+y（動畫畫面往右）'
    print(f'  A = {a}：B 的布洛赫向量 (x, y, z) = (0.00, {y:+.2f}, {z:+.2f}) → 指向 {side}')

print('\\n三、磁通調頻 CZ：改脈衝深度（05_twoqubit.js 的模型）')
FB, AL, G, FA0 = 5.0, -0.25, 0.015, 6.0   # GHz：B 的頻率、非諧性、耦合、A 的起點


def lower(fa):
    e11, e20 = fa + FB, 2 * fa + AL
    m, d = (e11 + e20) / 2, (e11 - e20) / 2
    return m - math.sqrt(d * d + 2 * G * G)


def phase(depth, tp):
    fmin = FA0 - depth * (FA0 - 5.25 + 0.02)
    def fa(t):
        r = min(1, t / (tp * 0.25), (tp - t) / (tp * 0.25))
        return FA0 - (FA0 - fmin) * math.sin(math.pi / 2 * max(0, r)) ** 2
    n, s = 400, 0.0
    for i in range(n):
        f = fa((i + 0.5) / n * tp)
        s += (lower(f) - (f + FB)) * tp / n
    return abs(2 * math.pi * s), fmin


print('  深度   A 最低頻率   找到 π 的時間   間距（|20⟩−|11⟩）')
for depth in (0.85, 0.90, 0.95):             # 改造區：試試 0.80、0.93
    best = min(range(20, 121), key=lambda t: abs(phase(depth, t)[0] - math.pi))
    ph, fmin = phase(depth, best)
    gap = (2 * fmin + AL - (fmin + FB)) * 1000
    note = '（120 ns 內湊不到 π）' if abs(ph - math.pi) > 0.1 else ''
    print(f'  {depth:.2f}   {fmin:.3f} GHz    {best:3d} ns {note}  {gap:4.0f} MHz')
print('  越靠近交叉點：閘越快，但間距越小、越容易洩漏到 |20⟩。')
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q055：兩位元閘——CZ 與交叉共振（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心有兩句：**磁通調頻把 A 的頻率拉低，讓 |11⟩ 靠近 |20⟩，迴避交叉讓只有 |11⟩ 多累積相位，累積到 π 就是 CZ；交叉共振用 B 的頻率去驅動 A，B 的旋轉方向由 A 決定，加上單位元修正就是 CNOT。** 好玩機制是角色扮演：爸爸當控制 A、孩子當目標 B，用牌子和手臂演出兩種閘。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開動畫，認識能階圖、四個相位轉盤與交叉共振的兩顆布洛赫球 | `operation.html#twoqubit` |
| 25–65 | 觀察迴避交叉與條件相位、調深度看取捨；在 `transmon-3d.html#case` 做一次 CZ；角色扮演 | 列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 整理各家原生兩位元閘對照表；完成兩種實現對照表；執行 `twoqubit_lab.py` | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：兩種做法的原理、一個限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#twoqubit`（課綱指定）與 `transmon-3d.html#case`（不需要網路、伺服器或帳號）。
- 列印 `02_列印包_兩位元閘.pdf`（A4，共 4 頁），第 2 頁的角色卡沿虛線剪開；準備兩張寫著 0 和 1 的牌子。
- 讀一遍 `04_解答.md`。

## 角色扮演的原則

- 影片旁白把 A、B 念成「甲、乙」：甲＝控制 A（爸爸），乙＝目標 B（孩子）。
- 演完一定到動畫對照：交叉共振看兩顆布洛赫球的方向；CZ 看四個轉盤裡哪一個轉了。
- 演錯了就交換角色，讓孩子當出題的控制位元。

## 誠實說明

- 閘時間「約 40–70 ns」「約 200–500 ns」與「兩位元閘誤差約高十倍」是學程簡報的概括數字，實際依機器而異。
- operation 動畫的「洩漏風險（示意）」是教學用的判斷，不是洩漏機率；動畫的頻率與耦合是教學數值。
- 各家原生閘依世代而異，表格取自學程簡報 p24，以官方文件為準。
- 「往左倒／往右倒」只是代表兩個相反方向的約定；轉動 3D 視角後左右會改變。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：磁通調頻 CZ（約 15 分鐘）

1. 打開 `animations/operation.html#twoqubit`，預設是「CZ（磁通調頻）」。
2. 看右邊能階圖：金色線是 |11⟩、紫色線標著 |20⟩，左下角標著「迴避交叉」。
3. 按「▶ 執行」：看白點滑到交叉旁再回來、量子位元 A 發藍光；再按一次，只看上方四個轉盤，哪一個轉了？轉了幾度？
4. 抄下左邊讀數：條件相位、最接近時間距、洩漏風險（示意）、「CZ：脈衝長度」。
5. 把「CZ：脈衝深度」調成 0.90、0.85，各按一次「自動找 π（調長度）」，再抄一次（填列印包第 1 頁下方）。

## 上半場：交叉共振與實際晶片（約 15 分鐘）

1. 點「交叉共振 CR」，按「▶ 執行」：左右兩顆球的箭頭往哪裡倒？讀數旋轉角幾度？
2. 打開 `animations/transmon-3d.html#case`，取消勾選「自動接續」，按「下一步 ▶」到第 6 步「換你操作」。
3. 按「π → Q2」、等兩秒再按「π → Q3」，再按「CZ（Q2–Q3）」：看 Q3 的頻率移到幾 GHz、右邊「|11⟩ 累積相位」最後寫什麼。

## 角色扮演（約 10 分鐘）

1. 照列印包第 2 頁的卡片，爸爸舉牌、孩子用手臂演出。
2. 每演完一張，到 operation 動畫對照。

## 下半場：原生閘對照表（約 30 分鐘）

1. 列印包第 3 頁：照影片與簡報 p24 填各家原生兩位元閘，標出是哪一種實現（CZ 類或交叉共振類）。
2. 完成第 1 頁的兩種實現對照表，替它取名字。
3. 執行 `python twoqubit_lab.py`，對答案；改「改造區」的深度再跑一次。
''',

'twoqubit_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 兩種實現對照表\n\n| 比較項目 | 磁通調頻 CZ | 交叉共振 CR |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in COMPARE)
  + '\n## operation.html#twoqubit 讀數\n\n'
  '| 脈衝深度 | f_A 最低 | 自動找 π 後的時間 | 條件相位 | 最接近間距 | 洩漏風險（示意） |\n|---|---|---|---|---|---|\n'
  '| 0.95（預設） | 5.269 GHz | 59 ns | 180° | 19 MHz | 高 |\n'
  '| 0.90 | 5.307 GHz | 110 ns | 180° | 57 MHz | 低 |\n'
  '| 0.85 | 5.346 GHz | 120 ns（湊不到 π） | 約 133° | 95 MHz | 低 |\n\n'
  '- 深度 0.90 時、還沒按自動找 π（仍是 59 ns）：條件相位只有 97°。\n'
  '- 四個轉盤只有 |11⟩ 的金色箭頭從右轉到左（180°）。\n'
  '- 交叉共振：左邊（A = |0⟩）箭頭往左倒、右邊（A = |1⟩）往右倒，停在赤道，「ZX 旋轉角 = 90°」。\n\n'
  '## transmon-3d.html#case 第 6 步\n\n'
  '- Q1 4.900、Q2 5.100、Q3 5.300 GHz；CZ 時 Q3 移到 5.383 GHz（= 5.100 + 0.283），出現紅色碰撞帶（刻意共振），最後「180°（= −1，CZ 完成）」，Q3 回到 5.300。\n\n'
  '## 角色扮演\n\n| 情境 | 爸爸 | 孩子 | 正確動作 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in ROLES)
  + '\n## 原生兩位元閘（學程簡報 p24，以官方文件為準）\n\n| 平台 | 原生兩位元閘 | 架構特點 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in NATIVE)
  + '\n## 常見誤解\n\n'
  '- 「兩位元閘和單位元閘一樣準」：兩位元閘誤差通常高約十倍，是主要錯誤來源。\n'
  '- 「脈衝越快越好」：太靠近交叉點或太快，會洩漏到 |20⟩。\n'
  '- 「CZ 有分控制和目標」：CZ 是對稱的；CNOT 才有控制與目標之分。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#twoqubit`（如何操作量子電腦 場景 5：兩位元閘，課綱指定）

- 選項：「CZ（磁通調頻）」「交叉共振 CR」；滑桿：「CZ：脈衝深度（接近交叉點）」「CZ：脈衝長度」；按鈕：「▶ 執行」「自動找 π（調長度）」。
- CZ 模式：左邊晶片（量子位元 A、B、耦合器、Z 線），右邊能階圖（金色 |11⟩、紫色 |20⟩、迴避交叉），上方四個條件相位轉盤；右下插圖上半是 f_A 的磁通脈衝，下半是累積的條件相位與 π 虛線。
- CR 模式：兩顆目標 B 的布洛赫球（左：A = |0⟩；右：A = |1⟩）；右下插圖是驅動包絡與兩條相反方向的旋轉角。

## `animations/transmon-3d.html#case`（Transmon 3D 第 6 章：三顆可調 transmon 的頻率配置）

- 第 5 步「CZ 閘」會自動演示；第 6 步「換你操作」有三條 Φ 滑桿、π → Q1／Q2／Q3、CZ（Q2–Q3）、回到配置等按鈕。
- 頻率尺上實線是 0→1、細線是 1→2（低 283 MHz）、◆ 是雙光子；紅色帶是碰撞。

## 操作

滑鼠拖曳旋轉、滾輪縮放；operation 頁可用左右方向鍵切換場景、`H` 隱藏面板。
''',
}

SHEET_HEADER = ['比較項目', '磁通調頻 CZ', '交叉共振 CR', '我的補充']
SHEET_ROWS = [[a] for a, *_ in COMPARE]

EXTRA_CSS = '''table.cmp td{height:11mm;font-size:11pt}table.cmp th{font-size:11pt}table.cmp td:first-child{width:34mm}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:3.5mm 4.5mm;height:52mm}
.cards h3{font-size:14pt;margin:0 0 1.5mm}.cards p{margin:1mm 0;font-size:11pt}
table.nt td{height:11mm}table.dp td{height:9mm;text-align:center}table.dp th{text-align:center}'''


def html():
    cmp_rows = ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, *_ in COMPARE)
    cards = ''.join(f'<div class="cut"><h3>角色卡 {i}：{a}</h3><p><b>爸爸（控制 A）：</b>{b}</p><p><b>你（目標 B）：</b>{c}</p>'
                    f'<p><b>你的動作：</b>＿＿＿＿＿＿＿＿＿＿＿＿</p><p class="note">演完到動畫對照，對了打勾 □</p></div>'
                    for i, (a, b, c, d) in enumerate(ROLES, 1))
    nt_rows = ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, *_ in NATIVE)
    pages = [
        '<h2>兩種實現對照表</h2><p class="lead">看完影片和動畫，把兩種做法並排寫清楚。</p>'
        '<table class="cmp"><tr><th>比較項目</th><th>磁通調頻 CZ</th><th>交叉共振 CR</th></tr>'
        f'{cmp_rows}</table>'
        '<div class="box" style="margin-top:3mm"><p>operation.html#twoqubit：改「CZ：脈衝深度」，按「自動找 π（調長度）」後抄下讀數</p>'
        '<table class="dp"><tr><th>深度</th><th>脈衝長度</th><th>條件相位</th><th>最接近間距</th><th>洩漏風險</th></tr>'
        '<tr><td>0.95</td><td></td><td></td><td></td><td></td></tr><tr><td>0.90</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>0.85</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p class="note">作品名稱：＿＿＿＿＿＿＿＿＿＿　我發現：越靠近交叉點，閘越＿＿＿，洩漏風險越＿＿＿。</p></div>',
        '<h2>角色扮演卡</h2><p class="lead">沿虛線剪開。爸爸當控制 A、你當目標 B；手臂舉高代表箭頭指向北極（|0⟩）。演完到動畫對照。</p>'
        f'<div class="cards">{cards}</div>'
        '<div class="box" style="margin-top:4mm"><p>1. 交叉共振：送出的微波打在誰身上？頻率對準誰？</p><div class="line"></div>'
        '<p>2. CZ：四種狀態裡，只有哪一種會喊「負號」？為什麼兩人可以交換角色？</p><div class="line"></div></div>',
        '<h2>原生兩位元閘對照表</h2><p class="lead">原生閘＝硬體直接會做的閘。依世代而異，以官方文件為準。</p>'
        '<table class="nt"><tr><th>平台</th><th>原生兩位元閘</th><th>屬於哪一種實現？（CZ 類／交叉共振類／其他）</th></tr>'
        f'{nt_rows}</table>'
        '<div class="box" style="margin-top:4mm"><p>1. 為什麼同一個目標（糾纏兩顆量子位元），各家做法不同？</p><div class="line"></div>'
        '<p>2. 執行 twoqubit_lab.py：(I⊗H)·CZ·(I⊗H) 等於 CNOT 嗎？＿＿＿　深度 0.85 時，＿＿＿＿＿＿＿＿</p><div class="line"></div>'
        '<p>3. 一段線路有 10 個兩位元閘、20 個單位元閘，哪一種比較可能出錯？為什麼？</p><div class="line"></div></div>',
        '<h2>說明卡：我的兩種實現對照表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 兩位元閘：CZ 與交叉共振在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：磁通調頻讓 |11⟩ 靠近 |20⟩，只有 |11⟩ 多一個負號</li><li>不看稿說出：交叉共振用 B 的頻率驅動 A，B 的轉向看 A</li>'
        '<li>示範：在動畫裡切換兩種模式，各執行一次</li><li>指出限制：兩位元閘誤差通常比單位元閘高約十倍，是主要錯誤來源</li>'
        '<li>替兩種實現對照表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q055 兩位元閘列印包', '父子科技學院 量子電腦學程 Q055｜兩位元閘：CZ 與交叉共振', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q055-cz-cross-resonance', folder='Q055_兩位元閘', files=FILES,
        sheet=('03_兩種實現對照表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_兩位元閘.pdf', pack_pages=4,
        pack_needles=('兩種實現對照表', '角色扮演卡', '原生兩位元閘對照表', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q055', episode_dir='specials/q055-cz-cross-resonance',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'twoqubit_lab.py', 'roleCards': [a for a, *_ in ROLES],
               'nativeGatesFrom': 'slides/QC_Operation_Talk.pptx p24', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q055/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

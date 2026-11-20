"""Q015 課堂教材：關卡設計表、示範關卡書（五關）、魔王關設計與好關卡檢查、說明卡、解答、escape_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（escape_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/operation.html 的五個場景。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q015/classroom.py
"""
from pathlib import Path
import contextlib
import io
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = '''"""父子科技學院 量子電腦學程 Q015：量子逃脫室——五關答案的驗算。

不用安裝任何套件，只要 Python 3。執行：  python escape_check.py
每一關都用和學程動畫 operation.html 相同的規則計算（只算理想狀況，沒有雜訊）。
自己設計新關卡時，可以照同樣的方法先算一次，確定答案只有一個。
"""
import cmath
import itertools
import math

S = 1 / math.sqrt(2)
H = [[S, S], [S, -S]]          # 哈達瑪閘
Z = [[1, 0], [0, -1]]          # 相位翻轉閘
GATES = {'H': H, 'Z': Z}


def apply(m, v):
    return [m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1]]


def p1(v):
    return abs(v[1]) ** 2


# 第一關：箭頭從北極往下傾斜 theta 度，得到 0 的機率 = cos²(theta/2)（01_qubit.js）
theta = 60
P0_LEVEL1 = math.cos(math.radians(theta) / 2) ** 2
print(f'第一關：傾斜 {theta} 度，得到 0 的機率 {P0_LEVEL1:.3f}；量 1000 次，平均約 {1000 * P0_LEVEL1:.0f} 次是 0'
      f'（一個標準差約 {math.sqrt(1000 * P0_LEVEL1 * (1 - P0_LEVEL1)):.0f} 次）')

# 第二關：哈達瑪閘 → 在 |1> 路徑加相位 phi → 哈達瑪閘（08_interference.js）
LEVEL2 = {}
for phi in (0, 90, 180, 270):
    v = apply(H, [1, 0])
    v = [v[0], v[1] * cmath.exp(1j * math.radians(phi))]
    v = apply(H, v)
    LEVEL2[phi] = p1(v)
    print(f'第二關：相位 {phi:3d} 度，得到 1 的機率 {LEVEL2[phi]:.3f}')

# 第三關：兩顆量子位元，哈達瑪閘 + 受控反閘 → 貝爾態（04_register.js 的「Bell 態」按鈕）
amp = {'00': 1.0, '01': 0.0, '10': 0.0, '11': 0.0}            # 兩顆都從 0 開始；左邊那一位是控制位元
new = dict.fromkeys(amp, 0.0)
for k, x in amp.items():                                          # 對控制位元做哈達瑪閘
    for b, sign in (('0', 1), ('1', 1 if k[0] == '0' else -1)):
        new[b + k[1]] += S * sign * x
amp = {(k if k[0] == '0' else k[0] + str(1 - int(k[1]))): x for k, x in new.items()}   # 受控反閘
BELL = {k: round(abs(a) ** 2, 3) for k, a in amp.items()}
print('第三關：貝爾態的四種結果機率', BELL)

# 第四關：16 個抽屜的格羅弗搜尋（09_grover.js：標記＝寶藏變號；擴散＝a → 2×平均 − a）
N, TREASURE = 16, 11
a = [1 / math.sqrt(N)] * N
GROVER = [a[TREASURE] ** 2]
for r in range(1, 6):
    a[TREASURE] = -a[TREASURE]
    mean = sum(a) / N
    a = [2 * mean - x for x in a]
    GROVER.append(a[TREASURE] ** 2)
print('第四關：第 0–5 輪寶藏的機率', [round(p, 3) for p in GROVER])

# 魔王關：只用 H 和 Z，從 |0> 出發，最少幾個閘能「一定得到 1」？列出所有答案
BOSS = {}
for k in range(1, 5):
    BOSS[k] = []
    for seq in itertools.product('HZ', repeat=k):
        v = [1, 0]
        for g in seq:
            v = apply(GATES[g], v)
        if p1(v) > 0.999:
            BOSS[k].append('→'.join(seq))
    print(f'魔王關：{k} 個閘時，一定得到 1 的排法：{BOSS[k] or "沒有"}')
v = apply(H, apply(H, [1, 0]))
HH_P1 = p1(v)
print(f'魔王關對照：只按 H→H，得到 1 的機率 {HH_P1:.3f}（回到 0）')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'escape_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與 source-notes.md 的紀錄相同
assert round(R['P0_LEVEL1'], 3) == 0.75
assert round(R['LEVEL2'][0], 3) == 0.0 and round(R['LEVEL2'][180], 3) == 1.0 and round(R['LEVEL2'][90], 3) == 0.5
assert R['BELL'] == {'00': 0.5, '01': 0.0, '10': 0.0, '11': 0.5}
assert round(R['GROVER'][3], 3) == 0.961 and max(range(6), key=lambda i: R['GROVER'][i]) == 3
assert R['BOSS'][1] == [] and R['BOSS'][2] == [] and R['BOSS'][3] == ['H→Z→H']
assert round(R['HH_P1'], 3) == 0.0

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q015：迷你專案——量子逃脫室（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片示範一本五關的逃脫室關卡書：疊加和測量、干涉、糾纏、格羅弗搜尋，最後是要用兩個概念才能破的魔王關（課綱的「Boss 關」）。課堂上父子各設計兩關、交換破關，孩子再設計自己的魔王關，合成一本五關關卡書。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 複習五個概念、看示範關卡書、讀「好關卡的三條規則」 | 影片第 3–8 段、列印包第 2 頁 |
| 25–65 | 魔王戰：父子各填兩關關卡設計表，交換破關；出題的人當關主 | 列印包第 1 頁、`03_關卡設計表.csv`、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子設計魔王關（兩個概念才能破），自己先在動畫裡破一次，再給爸爸破 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：每一關用了哪個概念、怎麼操作動畫驗證 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替關卡書取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html`，先把五個場景各點一次：`#qubit`、`#gates`、`#interference`、`#register`、`#grover`。
- 翻出 Q002–Q014 的作品（說明卡、結果表、截圖），出題時可以拿來找靈感。
- 列印 `02_列印包_量子逃脫室.pdf`（A4，共 4 頁）；第 1 頁「關卡設計表」可以多印幾張。讀一遍 `04_解答.md`。
- 有電腦可以跑 Python 3 的話，先執行一次 `escape_check.py`（不需要安裝套件），看看怎麼「先算一次」確認答案。

## 出題的三條規則（驗收重點）

1. 唯一正解：題目只能有一個說得通的答案。「把箭頭弄到赤道」有無限多種做法，要改成「只能用哪些閘、最少幾個」。
2. 要有提示：提示幫忙想，不直接說出答案。
3. 不靠運氣：「量一次得到 1 就過關」只是在丟硬幣；改成問「一千次裡大約幾次」或「會不會出現」。

## 誠實說明

- 動畫和程式算的是理想的量子狀態，沒有雜訊；真的量子電腦還會有誤差（上一堂 Q014 的主題）。
- 第一關「大約 750 次」是平均值，實際跑一千次每次會差十幾次，答案要寫成「大約」或給一個範圍。
- 示範關卡書是影片舉的例子；孩子自己設計的關卡更重要，題目不必和示範一樣。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：魔王戰——父子出題對戰（約 40 分鐘）

1. 父子各拿一張「關卡設計表」（列印包第 1 頁），各設計兩關。每一關填五格：概念、場景、題目、唯一正解、提示。
2. 每一關都要用到一個學過的概念，並指定一個動畫場景：
   - 疊加和測量：`operation.html#qubit`（θ 滑桿、「測量一次」「一次跑 1000 shots」）
   - 量子閘：`operation.html#gates`（X、Y、Z、H 按鈕、「重設 |0⟩」）
   - 干涉：`operation.html#interference`（「A：相位 φ」滑桿、「A：中途偵測路徑」開關）
   - 糾纏：`operation.html#register`（「Bell 態」「測量全部」）
   - 格羅弗搜尋：`operation.html#grover`（「完整一輪」「自動跑到最佳次數」「測量」）
3. 出題的人先自己在動畫裡破一次，確認答案成立、而且只有一個。
4. 交換設計表破關：破關的人先自己想，卡住才看提示，最後用動畫驗證。
5. 出題的人當關主：答案對了就在關卡書蓋章；答案不唯一或要靠運氣的題目，一起改到合格。

## 下半場：孩子設計魔王關（約 30 分鐘）

1. 從疊加、測量、干涉、糾纏、格羅弗搜尋挑兩個概念（列印包第 3 頁）。
2. 寫題目：只懂一個概念的人要卡住。影片的例子：只能用 H 和 Z，最少幾個閘把 0 變成 1？
3. 自己先在動畫裡破一次；有電腦的話，照 `escape_check.py` 的寫法算一次。
4. 給爸爸破關，記下爸爸卡在哪裡、看了幾次提示。
5. 把四關加魔王關排成五關關卡書，取一個名字。
''',

'escape_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## escape_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 示範關卡書\n\n'
  '| 關 | 概念 | 場景 | 題目 | 正解 | 提示 |\n|---|---|---|---|---|---|\n'
  '| 1 斜斜的箭頭 | 疊加和測量 | #qubit | 箭頭從北極往下傾斜 60 度，量 1000 次，大約幾次得到 0？ | 大約 750 次（機率 3/4） | 傾斜越多，越容易得到 1 |\n'
  '| 2 兩條路 | 干涉 | #interference | 相位調到幾度，結果一定是 1？ | 180 度 | 0 度時一定是 0 |\n'
  '| 3 雙胞胎 | 糾纏 | #register | 做出貝爾態再量兩顆，會不會量到 01？ | 不會，只有 00 和 11，各一半 | 兩顆對照，永遠一樣 |\n'
  '| 4 十六個抽屜 | 格羅弗搜尋 | #grover | 做幾輪再打開抽屜最好？ | 3 輪，約 96% | √16 × 0.785，去掉小數 |\n'
  '| 魔王關 | 疊加＋干涉 | #gates | 只用 H 和 Z，最少幾個閘把 0 變成 1？ | H → Z → H，3 個閘（唯一） | H 做兩次會回到原點 |\n\n'
  '## 暫停題：第三關改成「量一次得到 00 就過關」哪裡不好？\n\n'
  '貝爾態量一次，00 和 11 各一半：這樣過關只看運氣，而且量到 11 的人明明懂也過不了。'
  '改法：問「會不會量到 01 或 10」，或「量十次，00 和 11 會不會同時出現、01 會不會出現」。\n\n'
  '## 常見問題\n\n'
  '- 為什麼第一關不能問「量一次會得到什麼」？量一次只會得到 0 或 1，看運氣；問一千次的比例，答案才固定在 3/4 附近。\n'
  '- 魔王關為什麼要兩個概念？H 做出疊加（兩條路），Z 改變其中一條路的相位，第二個 H 讓兩條路干涉；少了任何一個都到不了 1。'
  '只按 H→H 會回到 0（第二關相位 0 度的情況），H→Z→H 就是第二關相位 180 度的情況。\n'
  '- 怎麼判斷答案唯一？像 escape_check.py 那樣把所有可能列出來算一次：只用 H 和 Z 時，1 個、2 個閘都做不到，3 個閘只有 H→Z→H。\n'
  '- 第一關的「750」為什麼每次不一樣？那是平均值；一千次的實際次數會上下差十幾次（一個標準差約 14 次）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟 `operation.html`，不需要網路、伺服器或帳號。網址後面的 `#` 名稱可以直接跳到場景。

## `#qubit`（場景 1：量子位元的狀態與測量）

- 「θ（極角）」滑桿決定箭頭往下傾斜多少；得到 0 的機率 = cos²(θ/2)。預設按鈕「θ=60°」直接傾斜 60 度。
- 「測量一次」「一次跑 1000 shots」；右邊藍柱＝得到 0、紅柱＝得到 1，青色細線是理論機率。

## `#gates`（場景 2：單位元量子閘）

- 按 X、Y、Z、H，箭頭繞粉紅色的旋轉軸轉；「重設 |0⟩」回到北極。讀數顯示 P(0)、P(1)。
- 右下插圖記下依序按過的閘；「示範：H → Z → H = X」一次做完魔王關的例子。

## `#interference`（場景 8：干涉）

- 「A：相位 φ」滑桿：0 度一定得到 0、180 度一定得到 1；「A：中途偵測路徑」打開後變成一半一半。

## `#register`（場景 4：多量子位元與糾纏）

- 「Bell 態」：下排只剩 |00⟩、|11⟩ 兩根柱子，上排箭頭縮成一點，讀數顯示「有糾纏」。「測量全部」：結果是 00 或 11。

## `#grover`（場景 9：Grover 搜尋）

- 16 根柱子＝16 個抽屜；「完整一輪」「自動跑到最佳次數」「測量」；N = 16 時最佳是 3 輪。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；← → 切換場景。
''',
}

SHEET_HEADER = ['關卡', '出題的人', '概念', '動畫場景', '題目', '唯一正解', '提示', '破關的人', '看了幾次提示', '過關了嗎', '備註']
SHEET_ROWS = ([[f'第 {i} 關', '爸爸' if i % 2 else '孩子'] for i in range(1, 5)] + [['魔王關', '孩子', '（兩個概念）']])

EXTRA_CSS = '''table.rec td{height:27mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.demo td{font-size:10.5pt;height:auto}table.demo th:last-child{width:24mm;white-space:nowrap}table.demo th:first-child{width:22mm}
table.rec th:nth-child(4){width:30%}'''


def html():
    rows = ''.join(f'<tr><td>{n}</td><td></td><td></td><td></td><td></td><td></td></tr>' for n in ('第 1 關', '第 2 關', '第 3 關', '第 4 關'))
    pages = [
        '<h2>關卡設計表</h2><p class="lead">每一關填五格：概念、場景、題目、唯一正解、提示。出題的人要先自己在動畫裡破一次。</p>'
        '<p>出題的人：□ 爸爸　□ 孩子　　概念可選：疊加、測量、干涉、糾纏、格羅弗搜尋</p>'
        '<table class="rec"><tr><th>關卡</th><th>概念</th><th>動畫場景</th><th>題目</th><th>唯一正解</th><th>提示</th></tr>'
        + rows + '</table>'
        '<div class="box" style="margin-top:5mm"><h3>關主檢查（每關都要打勾才合格）</h3><ul class="chk">'
        '<li>答案只有一個，沒有第二種說得通的答案</li><li>提示幫忙想，但沒有直接說出答案</li>'
        '<li>不靠運氣：不是「量一次得到某個結果就過關」</li><li>出題的人自己在動畫裡破過一次</li></ul></div>',
        '<h2>示範關卡書：五關</h2><p class="lead">影片裡的例子。正解在 04_解答.md，先自己破關再看。</p>'
        '<table class="demo"><tr><th>關</th><th>概念＋場景</th><th>題目</th><th>提示</th><th>我的答案</th></tr>'
        '<tr><td>1 斜斜的箭頭</td><td>疊加和測量<br>#qubit</td><td>箭頭從北極往下傾斜 60 度，量 1000 次，大約幾次得到 0？</td><td>傾斜越多，越容易得到 1</td><td></td></tr>'
        '<tr><td>2 兩條路</td><td>干涉<br>#interference</td><td>相位調到幾度，結果一定是 1？</td><td>0 度時一定是 0</td><td></td></tr>'
        '<tr><td>3 雙胞胎</td><td>糾纏<br>#register</td><td>做出貝爾態再量兩顆，會不會量到 01？</td><td>兩顆對照，永遠一樣</td><td></td></tr>'
        '<tr><td>4 十六個抽屜</td><td>格羅弗搜尋<br>#grover</td><td>做幾輪再打開抽屜，找到寶藏的機會最大？</td><td>√16 × 0.785，去掉小數</td><td></td></tr>'
        '<tr><td>魔王關</td><td>疊加＋干涉<br>#gates</td><td>只用 H 和 Z，最少幾個閘把 0 變成 1？</td><td>H 做兩次會回到原點</td><td></td></tr></table>'
        '<div class="box" style="margin-top:5mm"><h3>暫停題</h3><p>如果第 3 關改成「量一次得到 00 就過關」，哪裡不好？要怎麼改？</p>'
        '<div class="line"></div><div class="line"></div></div>',
        '<h2>換你改造：魔王關</h2><p class="lead">要用兩個概念才能破；只懂一個概念的人會卡住。</p>'
        '<div class="box"><h3>設計</h3><p>我挑的兩個概念：＿＿＿＿＿＿＋＿＿＿＿＿＿　場景：＿＿＿＿＿＿＿＿</p>'
        '<p>題目：</p><div class="line"></div><div class="line"></div>'
        '<p>唯一正解：</p><div class="line"></div><p>提示：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>試玩紀錄</h3><p>我自己先破了嗎？□ 破了　□ 還沒　　答案真的只有一個嗎？□ 是　□ 要改</p>'
        '<p>爸爸看了＿＿次提示，花了＿＿分鐘破關；爸爸卡在：</p><div class="line"></div>'
        '<p>下次想加的關：</p><div class="line"></div></div>',
        '<h2>說明卡：我的量子逃脫室</h2><div class="box"><p>關卡書名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 這本關卡書在解決什麼（考了哪些概念）？</p><div class="line"></div><p>2. 我怎麼做（怎麼出題、怎麼確認答案）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 真實的量子電腦哪裡會用到這些概念？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出五關各用了哪個概念</li><li>說出最難的一關是哪一關、為什麼</li>'
        '<li>在動畫裡示範破一關給爸爸看</li><li>指出一個注意事項：唯一正解、要有提示、不靠運氣</li>'
        '<li>替關卡書取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q015 量子逃脫室 列印包', '父子科技學院 量子電腦學程 Q015｜迷你專案：量子逃脫室', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q015-quantum-escape-room', folder='Q015_量子逃脫室', files=FILES,
        sheet=('03_關卡設計表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子逃脫室.pdf', pack_pages=4,
        pack_needles=('關卡設計表', '示範關卡書', '魔王關', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q015', episode_dir='specials/q015-quantum-escape-room',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（escape_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'escape_check.py',
               'recordedRun': {'level1_P0': round(R['P0_LEVEL1'], 3), 'level2_P1_at_180': round(R['LEVEL2'][180], 3),
                               'level3_bell': R['BELL'], 'level4_round3': round(R['GROVER'][3], 3), 'boss_shortest': R['BOSS'][3]},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q015/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

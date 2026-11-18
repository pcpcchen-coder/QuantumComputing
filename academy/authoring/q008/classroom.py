"""Q008 課堂教材：合作遊戲（CHSH 遊戲）卡片、對戰紀錄、策略列舉、勝率表與解答（不需帳號、不需安裝）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q008/classroom.py
"""
from pathlib import Path
import itertools
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent
CARDS = ('紅', '藍')  # 紅 = 0、藍 = 1（CHSH 遊戲的 x、y）
CASES = [(x, y) for x in (0, 1) for y in (0, 1)]


def wins(sa, sb):
    """sa、sb = (拿到紅卡的答案, 拿到藍卡的答案)。贏的條件：兩張藍卡答案不同，其他答案相同（a⊕b = x∧y）。"""
    return sum((sa[x] ^ sb[y]) == (x & y) for x, y in CASES)


STRATS = list(itertools.product((0, 1), repeat=2))
TABLE = {(sa, sb): wins(sa, sb) for sa in STRATS for sb in STRATS}
assert max(TABLE.values()) == 3 and len(TABLE) == 16
QUANTUM = math.cos(math.pi / 8) ** 2
assert round(QUANTUM, 3) == 0.854


def sname(s):
    return f'紅答{s[0]}、藍答{s[1]}'


FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q008：糾纏，一對神祕骰子（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五分鐘，帶出今天的重點：糾纏是兩個結果之間的關聯，不能用來比光還快地傳訊息。

## 這份教材在做什麼

父子玩一個合作遊戲（物理學家叫它 CHSH 遊戲）：兩人各自隨機拿到紅卡或藍卡，不能互看、不能說話，各自寫下 0 或 1。
兩張都是藍卡時答案要「不同」才贏，其他情況答案「相同」就贏。開始前可以商量策略。
孩子會發現：不管怎麼約定，不用量子最多只能贏四種情況中的三種（75%）；兩人如果各拿一顆糾纏的量子位元，理論上可以贏約 {QUANTUM * 100:.0f}%。
不需要帳號；3D 場景見 `05_三維動畫導覽.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 神祕骰子、貝爾態、為什麼不能傳訊息 | 影片第 3–6 段、3D 場景 |
| 25–65 | 合作遊戲：剪卡片、約定策略、玩 20 回合，每 10 回合交換角色 | `01_遊戲步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子自己想古典策略，列出四種情況算勝率 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼糾纏不能傳訊息 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替勝率表取名字 | `03_勝率表.csv` |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_神祕骰子.pdf`（A4，共 4 頁），剪下第 1 頁的八張卡片：每人兩紅兩藍。
- 剪刀、鉛筆、兩個不透明的杯子或信封（抽卡用）。
- 讀一遍 `04_解答.md`。

## 角色交換的原則

- 策略設計師：開局前說清楚約定（例如「紅卡答 0、藍卡答 1」）；記分員：翻牌後判定輸贏、寫進紀錄表。每 10 回合交換。
- 抽卡前兩人一起洗牌，抽完要放回，這樣每回合紅藍的機會才各一半。
- 20 回合太少，勝率上下跳動很正常；看的是「最多能到多少」，不是一次的運氣。

## 誠實說明

- 「神祕骰子」是比喻。只會「永遠一樣」的骰子，用事先約好也做得到；真正分得出糾纏的是今天的合作遊戲。
- 量子策略的約 {QUANTUM * 100:.1f}% 是理論值，在家沒辦法用紙筆真的做到；勝率表裡這一格填理論值即可。
- 量子策略也不是傳訊息：每個人自己的答案仍然是隨機的，要對答案才看得出勝率。
''',

'01_遊戲步驟.md': '''# 遊戲步驟

## 準備

1. 剪下列印包第 1 頁的卡片：我拿兩紅兩藍，爸爸也拿兩紅兩藍。
2. 各自把四張卡蓋著放進杯子（或信封）。

## 每一回合

1. 兩人各自從自己的杯子抽一張，只能自己看。
2. 依照事先約好的策略，在紀錄表寫下 0 或 1（寫好不能改）。
3. 一起翻開卡片和答案。
4. 記分員判定：兩張都是藍卡 → 答案不同才贏；其他情況 → 答案相同才贏。
5. 卡片放回杯子，搖一搖，下一回合。

## 角色交換

- 第 1–10 回合：我當策略設計師（決定約定），爸爸當記分員。
- 第 11–20 回合：交換，爸爸想新的約定，我當記分員。
- 每 10 回合算一次勝率（贏的次數 ÷ 10），寫進列印包第 4 頁的勝率表。

## 下半場：自己想策略（約 30 分鐘）

1. 每個策略都寫成「紅卡答什麼、藍卡答什麼」，兩人各一個。
2. 在列印包第 3 頁列出四種發卡情況：紅紅、紅藍、藍紅、藍藍。
3. 一格一格判定輸贏，算出四種情況贏幾種。
4. 至少試四組策略。找得到贏四種的嗎？
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 全部 16 組古典策略\n\n'
  '每個人的策略是「拿到紅卡答幾、拿到藍卡答幾」，共 4 種；兩人合起來 16 組。表內是四種發卡情況中贏幾種。\n\n'
  + '| 我 ＼ 爸爸 | ' + ' | '.join(sname(s) for s in STRATS) + ' |\n|---' * (len(STRATS) + 1) + '|\n'
  + ''.join(f'| {sname(sa)} | ' + ' | '.join(f'{TABLE[(sa, sb)]}/4' for sb in STRATS) + ' |\n' for sa in STRATS)
  + f'\n最多 3/4 = 75%，沒有一組能贏 4 種：前三種情況要求「答案相同」，第四種要求「答案不同」，四個要求不可能同時成立。\n\n'
  f'## 量子策略\n\n兩人事先各拿一顆糾纏的量子位元（貝爾態），依照拿到的卡片選不同角度測量，把測量結果當答案；理論勝率 cos²(π/8) ≈ {QUANTUM * 100:.1f}%。\n'
  '每個人自己的測量結果仍是一半一半的隨機，所以不能傳訊息。\n\n'
  '## 常見問題\n\n'
  '- 20 回合贏了 17 次（85%）？古典策略也可能靠運氣暫時超過 75%，回合越多越接近理論值。\n'
  '- 孩子說「量了一顆，另一顆就變了，所以能傳訊息」：請他想想，遠方的人只看自己的結果，能分辨出你量了沒有嗎？（不能，永遠一半一半。）\n',

'05_三維動畫導覽.md': '''# 三維動畫導覽

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## 場景一：`animations/operation.html#register`（場景 4：多位元與糾纏）

- 按「Bell 態」：下排柱子只剩 |00⟩ 和 |11⟩，上排兩顆小球的箭頭都縮成一點（單看一顆完全隨機）。
- 按「測量全部」：得到 00 或 11。再按一次「Bell 態」重新準備，多試幾次。
- 按「只測 q0」：q0 隨機得到 0 或 1，另一顆跟著確定；但遠方的人沒有對答案前看不出來。
- 對照「均勻疊加 H⊗ⁿ」：四根柱子一樣高，箭頭不會縮短，沒有糾纏。

## 場景二：`animations/basic-circuits.html#bell`

- 按「下一步」兩次：H 讓 q0 疊加，CNOT 讓 q1 跟著走。
- 按「量測 1,000 次」：只出現 00 和 11，各約一半。

## 操作

滑鼠拖曳旋轉、滾輪縮放；`H` 隱藏面板；`R` 重設視角。
''',
}

SHEET_HEADER = ['回合段', '策略設計師', '約定（我：紅答／藍答）', '約定（爸爸：紅答／藍答）', '回合數', '贏的次數', '勝率', '理論最高']
SHEET_ROWS = ([['第 1–10 回合', '我', '', '', '10', '', '', '75%'], ['第 11–20 回合', '爸爸', '', '', '10', '', '', '75%']]
              + [['下半場策略', '我', '', '', '4 種情況', '', '', '75%'] for _ in range(4)]
              + [['量子策略（理論）', '', '糾纏＋換角度測量', '糾纏＋換角度測量', '', '', f'{QUANTUM * 100:.1f}%', f'{QUANTUM * 100:.1f}%']])

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:4mm}
.card{height:38mm;border:1.2pt dashed #0b2540;border-radius:3mm;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:26pt;font-weight:700;color:#fff}
.red{background:#d64545}.blue{background:#2f6fd6}
table.rec td{height:7.2mm;text-align:center}table.st td{height:9mm;text-align:center}
.chk li{margin:3mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''

ROUNDS = 20


def html():
    card = lambda c, who: f'<div class="card {"red" if c == "紅" else "blue"}">{c}卡<span style="font-size:11pt;font-weight:400">{who}</span></div>'
    pages = [
        '<h2>合作遊戲：紅卡和藍卡（CHSH 遊戲）</h2><p class="lead">兩人各自抽卡，不能互看、不能說話，各寫 0 或 1。</p>'
        '<div class="box"><h3>贏的條件</h3><p>有紅卡（紅紅、紅藍、藍紅）：兩人答案<b>相同</b>才贏。</p>'
        '<p>兩張藍卡（藍藍）：兩人答案<b>不同</b>才贏。</p><p class="note">開始前可以商量策略；拿到卡之後就不能說話、不能改答案。</p></div>'
        '<h3 style="margin-top:5mm">剪下卡片：每人兩紅兩藍</h3><div class="cards">'
        + ''.join(card(c, '我') for c in '紅紅藍藍') + ''.join(card(c, '爸爸') for c in '紅紅藍藍') + '</div>'
        '<p class="note">每回合抽完要放回、搖一搖，紅和藍的機會才各一半。</p>',
        '<h2>對戰紀錄表</h2><p class="lead">每 10 回合交換角色：策略設計師 ↔ 記分員。</p>'
        '<p>第 1–10 回合約定：我 紅答＿ 藍答＿；爸爸 紅答＿ 藍答＿<br>第 11–20 回合約定：我 紅答＿ 藍答＿；爸爸 紅答＿ 藍答＿</p>'
        '<table class="rec"><tr><th>回合</th><th>我的卡</th><th>我的答案</th><th>爸爸的卡</th><th>爸爸的答案</th><th>贏／輸</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, ROUNDS + 1)) + '</table>'
        '<p class="note">第 1–10 回合贏＿＿次；第 11–20 回合贏＿＿次。</p>',
        '<h2>下半場：自己想古典策略</h2><p class="lead">每個策略寫成「紅卡答什麼、藍卡答什麼」，列出四種情況算贏幾種。</p>'
        '<p class="note">紅紅、紅藍、藍紅：答案要相同；藍藍：答案要不同。每格寫「贏」或「輸」。</p>'
        '<table class="st"><tr><th style="width:22mm">策略</th><th>我<br>紅／藍</th><th>爸爸<br>紅／藍</th><th>紅紅</th><th>紅藍</th>'
        '<th>藍紅</th><th>藍藍</th><th>贏幾種</th></tr>'
        '<tr><td>例：都答 0</td><td>0／0</td><td>0／0</td><td>贏</td><td>贏</td><td>贏</td><td>輸</td><td>3／4</td></tr>'
        + ''.join(f'<tr><td>策略 {i}</td><td></td><td></td><td></td><td></td><td></td><td></td><td>＿／4</td></tr>' for i in range(1, 6))
        + '</table><div class="box" style="margin-top:6mm"><h3>想一想</h3><p>有沒有一組策略四種情況全贏？為什麼？</p>'
        '<div class="line"></div><div class="line"></div></div>',
        '<h2>CHSH 遊戲勝率表</h2><table><tr><th>策略</th><th>回合或情況</th><th>贏幾次</th><th>勝率</th></tr>'
        '<tr><td>第 1–10 回合（我設計）</td><td>10 回合</td><td></td><td></td></tr>'
        '<tr><td>第 11–20 回合（爸爸設計）</td><td>10 回合</td><td></td><td></td></tr>'
        '<tr><td>我想到最好的古典策略</td><td>4 種情況</td><td></td><td></td></tr>'
        '<tr><td>古典策略理論最高</td><td>4 種情況</td><td>3</td><td>75%</td></tr>'
        f'<tr><td>量子策略（糾纏，理論值）</td><td>—</td><td>—</td><td>約 {QUANTUM * 100:.0f}%</td></tr></table>'
        '<p>勝率表的名字：＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<h2 style="margin-top:6mm">最後一關：教爸爸神祕骰子</h2><div class="box"><ul class="chk">'
        '<li>說出糾纏是兩個結果之間的關聯</li><li>說出為什麼單看一邊永遠是隨機的</li>'
        '<li>說出糾纏不能比光還快地傳訊息</li><li>說出古典策略最高四分之三，量子約八成五</li>'
        '<li>說出合作遊戲為什麼要先約定策略</li><li>替勝率表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q008 神祕骰子 列印包', '父子科技學院 量子電腦學程 Q008｜糾纏：一對神祕骰子', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q008-entangled-dice', folder='Q008_神祕骰子', files=FILES,
        sheet=('03_勝率表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_神祕骰子.pdf', pack_pages=4,
        pack_needles=('合作遊戲', '剪下卡片', '對戰紀錄表', '自己想古典策略', 'CHSH 遊戲勝率表', '最後一關'),
        authoring_dir=XINEW / 'authoring/q008', episode_dir='specials/q008-entangled-dice',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'classicalMaxWins': 3, 'classicalStrategies': len(TABLE), 'quantumWinProbability': round(QUANTUM, 4),
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q008/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

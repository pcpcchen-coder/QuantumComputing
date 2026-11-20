"""Q012 課堂教材：黑盒子函數卡（八張）、出題單、判案紀錄、平衡函數設計單、說明卡、解答、判案小程式與動畫導覽。

不需要帳號，也不需要安裝套件；動畫路線只要瀏覽器打開 animations/operation.html#interference；
判案小程式 dj_check.py 只用 Python 內建功能。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q012/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent
INPUTS = [format(x, '03b') for x in range(8)]  # 卡片正面：000 … 111（最右邊是 x₀）

# 出題單：卡片背面依序寫 000、001、…、111 的答案。前四組和 operation.html#interference 三位元模式的四個選項相同
# （js/operation/08_interference.js 第 61–64 行），E 是場景沒有的平衡函數。
# 最後兩欄是 dj_check.py 實跑結果（Python 3.13，只用標準函式庫）。
CASES = [  # (代號, 名稱, 背面答案, 類型, 場景選項, 量到 000 的機率, 量子實際會量到)
    ('A', '全部是 0', '00000000', '常數', '常數 f = 0', 1, '000'),
    ('B', '全部是 1', '11111111', '常數', '常數 f = 1', 1, '000'),
    ('C', '看最後一位', '01010101', '平衡', '平衡 f = x₀', 0, '001'),
    ('D', '1 的個數是奇數', '01101001', '平衡', '平衡 f = 奇偶', 0, '111'),
    ('E', '看第一位', '00001111', '平衡', '（場景沒有，用 dj_check.py）', 0, '100'),
]
for _c, _n, card, kind, *_ in CASES:
    assert len(card) == 8 and card.count('1') in ((0, 8) if kind == '常數' else (4,))
# 另一個實跑例子：00010111 是平衡（四個 1），但量子結果分散在 001、010、100、111 各 0.25，仍然不會是 000。

PROGRAM = '''"""父子科技學院 量子電腦學程 Q012：多伊奇–喬薩 判案小程式（只用 Python 內建功能，不用安裝套件）

用法：  python dj_check.py 01101001
        依序填 000、001、010、011、100、101、110、111 這八種輸入的答案（0 或 1）。
不填：  python dj_check.py        → 把場景 8 的四個內建函數各跑一次
"""
import sys

INPUTS = [format(x, '03b') for x in range(8)]          # 000 … 111；最右邊是 x₀
BUILTIN = {                                             # 和 operation.html#interference 三位元模式相同
    '常數 f = 0': '00000000',
    '常數 f = 1': '11111111',
    '平衡 f = x₀（最後一位）': '01010101',
    '平衡 f = 奇偶': '01101001',
}


def judge(name, card):
    f = [int(c) for c in card]
    signs = [-1 if v else 1 for v in f]                 # 黑盒子：答案是 1 的路蓋上負號
    arrows = ''.join('←' if s < 0 else '→' for s in signs)
    # 再做一次哈達瑪閘之後，量到 k 的振幅 = (1/8)·Σ(−1)^f(x)·(−1)^(x·k)
    amp = [sum(s * (-1) ** bin(x & k).count('1') for x, s in enumerate(signs)) / 8 for k in range(8)]
    prob = [round(a * a, 3) for a in amp]
    ones = sum(f)
    kind = '常數' if ones in (0, 8) else '平衡' if ones == 4 else '不是常數也不是平衡（違反保證）'
    print(f'【{name}】卡片 {card}（1 有 {ones} 個 → {kind}）')
    print(f'  八支箭頭：{arrows}　頭尾相接走到 {sum(signs):+d} 格')
    print(f'  量到 000 的機率：{prob[0]}')
    print('  所有結果：' + '、'.join(f'{INPUTS[k]} {p}' for k, p in enumerate(prob) if p > 0))
    verdict = '常數' if prob[0] > 0.999 else '平衡' if prob[0] < 0.001 else '違反保證：量一次不能保證判對'
    print(f'  量子判案：{verdict}\\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        card = sys.argv[1].strip()
        assert len(card) == 8 and set(card) <= {'0', '1'}, '請填 8 個 0 或 1，例如 01101001'
        judge('我的函數', card)
    else:
        for n, c in BUILTIN.items():
            judge(n, c)
'''

CASE_TABLE = ('| 代號 | 規則 | 背面（000→111） | 類型 | 場景選項 | 量到 000 的機率 | 量子會量到 |\n|---|---|---|---|---|---|---|\n'
              + ''.join(f'| {c} | {n} | `{k}` | {t} | {s} | {p} | {r} |\n' for c, n, k, t, s, p, r in CASES))

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q012：多伊奇–喬薩——一次看穿（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的案子：黑盒子函數保證只有「常數」或「平衡」兩種，古典偵探一張一張翻卡，量子方法只問一次，靠的是干涉。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 黑盒子、常數與平衡、八支箭頭的干涉 | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 爸爸出題、孩子翻牌判案；每一案再用干涉場景看量子判定 | 列印包第 1、2 頁、`03_判案紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子設計一個三位元平衡函數，畫箭頭並驗證 | 列印包第 3 頁、`dj_check.py` |
| 105–115 | 孩子教爸爸：問題是什麼、為什麼一次就夠 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_一次看穿.pdf`（A4，共 4 頁），剪下第 1 頁的八張函數卡。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#interference`，按「3 位元：8 條路徑（Deutsch–Jozsa）」確認看得到八個小圓盤。
- 讀一遍 `04_解答.md`。有 Python 的話，先跑一次 `python dj_check.py`。

## 出題單（卡片背面依 000、001、…、111 的順序寫）

{CASE_TABLE}
出題時把卡片洗亂、正面（000…111）朝上排好，背面的答案朝下。前四組和場景的四個選項一樣，翻完可以直接到場景看量子判定。

## 出題人的原則

- 只出常數或平衡：這是題目的保證。出了「三個 1」這種卡，量子方法就不能保證判對（`dj_check.py` 會顯示「違反保證」）。
- 想讓偵探翻滿五張，就把平衡函數的四個 0 擺在偵探最可能先翻的位置；這正是「最壞情況」。
- 孩子說「量子把八張都看過了」時，提醒他：量子只告訴你常數或平衡，不會告訴你每一張寫什麼。

## 誠實說明

- 這是教學用的玩具問題，它示範干涉，本身幾乎沒有實際用途。
- 「最壞要翻五張」是要百分之百確定的情況；如果允許一點點出錯，隨機翻幾張就很有把握，量子的優勢在於只問一次而且一定正確。
- 場景不能輸入自訂的函數；孩子自己設計的平衡函數，用紙上的箭頭和 `dj_check.py` 驗證。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：翻牌判案（約 40 分鐘）

1. 爸爸依出題單挑一組（先不要說是哪一組），把八張函數卡正面朝上排好、答案朝下。
2. 孩子一次翻一張，每翻一張就說出推理：「還不能確定」或「可以判案了」。
3. 能確定就停，在列印包第 2 頁寫下翻了幾張、判斷是常數還是平衡。
4. 打開 `operation.html#interference`，按「3 位元：8 條路徑（Deutsch–Jozsa）」，選和這一案相同的函數：
   - 看中間八個小圓盤：答案是 1 的箭頭朝左，答案是 0 的朝右。
   - 看右邊大圓：八支箭頭頭尾相接；金色字 `P(000)` 是量到 000 的機率。
   - 看右下小圖：最後量測的八種結果；常數只有 000，平衡一定不是 000。
5. 換一組卡，多辦幾案。至少辦一次常數、一次平衡，再辦一次「爸爸故意讓你翻滿五張」的案子。

## 下半場：設計自己的平衡函數（約 30 分鐘）

1. 在列印包第 3 頁的八格裡填上剛好四個 1。
2. 在每格下面畫箭頭：0 朝右、1 朝左，再把八支箭頭頭尾相接畫在格子紙上，看是不是回到起點。
3. 到場景切換「平衡 f = x₀」和「平衡 f = 奇偶」，比較朝左的箭頭在哪裡，你的設計和哪一個比較像。
4. 有 Python 的話，執行 `python dj_check.py 你的八個數字`（例如 `python dj_check.py 00001111`），看量到 000 的機率是不是 0。
5. 挑戰：故意寫一張「三個 1」的卡跑跑看，說說為什麼這時候量子方法不能保證判對。
''',

'dj_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 出題單與量子判定（dj_check.py 實跑，Python 3.13，只用標準函式庫）\n\n' + CASE_TABLE + '''
## 古典翻牌

- 八張卡（三個位元）最壞要翻 2³⁻¹＋1 = 5 張：平衡函數的四個 0 可能剛好都先被翻到，第五張才分得出來。
- 最好的情況是 2 張：前兩張就不一樣，一定是平衡。
- 十個位元（1,024 張卡）最壞要翻 513 張；量子方法不管幾個位元，都只問黑盒子一次。

## 量子判定

- 量到 000 的機率 = （八支箭頭頭尾相接的總和 ÷ 8）²。常數：八支同向，機率 1；平衡：四正四負，總和 0，機率 0。
- 平衡函數不一定只量到一種結果：例如 `00010111` 會分散在 001、010、100、111 各 0.25，但一定不會是 000。
- 三位元的平衡函數一共有 70 種（八格挑四格放 1）；全部都是量到 000 的機率 0。

## 常見問題

- 量子是不是把八張都看過了？不是。它只回答「常數或平衡」，不會告訴你每一張寫什麼。
- 為什麼只靠疊加不夠？疊加之後直接量，只會隨機得到一種輸入，和翻一張卡差不多；要再做一次哈達瑪閘讓八條路干涉，答案才會出現。
- 輔助位元做什麼？它先做翻轉閘、再做哈達瑪閘，讓黑盒子把「答案是 1」變成那一條路上的負號。
- 這有什麼用？這是教學用的玩具問題，示範干涉；本身幾乎沒有實際用途。
''',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#interference`（場景 8：干涉）

- 上方按「3 位元：8 條路徑（Deutsch–Jozsa）」。
- 函數選項：「常數 f = 0」「常數 f = 1」「平衡 f = x₀」「平衡 f = 奇偶」「隨機（非保證）」。
- 中間八個小圓盤是八種輸入；箭頭朝右是正、朝左是負。右邊大圓把八支箭頭頭尾相接，白色箭頭是總和，金色字是 P(000)。
- 右下小圖：最後量測八種結果的機率，000 是金色。
- 「隨機（非保證）」每按一次重新亂選，多半不是常數也不是平衡，用來看「違反保證」時會部分抵消。

## `animations/operation.html#circuit`（場景 6：量子線路）

- 範例選「Deutsch–Jozsa（平衡函數）」：兩個輸入位元加一個輔助位元，黑盒子是 f = x₀ ⊕ x₁。
- 按「單步 ▶」六次，最後一步跑 1000 次，只會出現 11：不是 00，所以是平衡。

## `animations/basic-circuits.html#deutsch`（量子電路入門：Deutsch）

- 最小的案子：黑盒子只有 0、1 兩種輸入。上方「黑盒裡的函數」四選一。
- 換選項會直接跳到最後一步；按「量測 1,000 次」，量的是 q0：0 是常數、1 是平衡，下方出現綠色判定字。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放（operation.html）；左右方向鍵換步（basic-circuits.html）。
''',
}

SHEET_HEADER = ['案號', '出題組（判完再填）', '翻開順序', '翻了幾張', '偵探判斷', '正確嗎', '場景選的函數', 'P(000)', '量子判斷']
SHEET_ROWS = [[f'第 {i} 案'] for i in range(1, 7)] + [['我的平衡函數', '自己設計']]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:3mm}
.card{border:1.6pt dashed #0b2540;border-radius:3mm;height:36mm;display:flex;flex-direction:column;align-items:center;justify-content:center}
.card b{font-size:30pt;letter-spacing:2mm}.card small{margin:0}
table.rec td{height:11mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.eight{display:grid;grid-template-columns:repeat(8,1fr);gap:2mm;margin-top:3mm;text-align:center}
.eight div{border:1.2pt solid #0b2540;border-radius:2mm;padding:1.5mm 0;font-size:12pt}
.eight .ans{height:13mm}.eight .arr{height:13mm;border-style:dashed}
.paper{height:46mm;margin-top:3mm;border:1.2pt solid #7f9bb3;background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt),
linear-gradient(90deg,#cfdde8 .6pt,transparent .6pt);background-size:6mm 6mm}'''


def html():
    cards = ''.join(f'<div class="card"><small>函數卡</small><b>{x}</b><small>背面寫 0 或 1</small></div>' for x in INPUTS)
    cases = ''.join(f'<tr><td>{c}</td><td>{n}</td><td>{k}</td><td>{t}</td></tr>' for c, n, k, t, *_ in CASES)
    rows = ''.join(f'<tr><td>第 {i} 案</td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 6))
    heads = ''.join(f'<div>{x}</div>' for x in INPUTS)
    pages = [
        '<h2>黑盒子函數卡</h2><p class="lead">沿虛線剪下八張卡。正面是輸入，背面由出題人（爸爸）寫答案 0 或 1。</p>'
        f'<div class="cards">{cards}</div>'
        '<h3 style="margin-top:5mm">出題單（爸爸用，不給偵探看）</h3>'
        f'<table><tr><th>代號</th><th>規則</th><th>背面（000→111）</th><th>類型</th></tr>{cases}</table>'
        '<p class="note">保證：只出常數（全部一樣）或平衡（剛好四個 0、四個 1）。A–D 和干涉場景的四個選項相同。</p>',
        '<h2>黑盒子判案紀錄</h2><p class="lead">古典偵探：一次翻一張，能確定就停。量子判定：到干涉場景選同一種函數。</p>'
        '<table class="rec"><tr><th>案號</th><th>翻開順序</th><th>翻了幾張</th><th>我的判斷</th><th>場景的 P(000)</th><th>量子判斷</th></tr>'
        f'{rows}</table>'
        '<div class="box" style="margin-top:5mm"><h3>偵探推理</h3>'
        '<p>1. 翻到第幾張時，一定能判案？為什麼？</p><div class="line"></div>'
        '<p>2. 哪一案讓我翻最多張？出題人是怎麼擺的？</p><div class="line"></div>'
        '<p>3. 量子方法只問一次，它有沒有告訴我每一張卡寫什麼？</p><div class="line"></div></div>',
        '<h2>換你出題：設計三位元平衡函數</h2><p class="lead">八格裡填剛好四個 1。0 的箭頭朝右，1 的箭頭朝左。</p>'
        f'<div class="eight">{heads}</div><div class="eight">' + '<div class="ans"></div>' * 8 + '</div>'
        '<div class="eight">' + '<div class="arr"></div>' * 8 + '</div>'
        '<h3 style="margin-top:4mm">把八支箭頭頭尾相接（一格一步）</h3><div class="paper"></div>'
        '<table style="margin-top:4mm"><tr><th>檢查</th><th>我的結果</th></tr>'
        '<tr><td>1 的個數剛好是 4 嗎？</td><td></td></tr><tr><td>箭頭接完回到起點了嗎？</td><td></td></tr>'
        '<tr><td>和場景的哪一種平衡比較像？</td><td></td></tr><tr><td>dj_check.py：量到 000 的機率</td><td></td></tr></table>',
        '<h2>說明卡：我的判案紀錄</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 黑盒子的問題是什麼？</p><div class="line"></div><p>2. 量子方法為什麼只問一次就能判案？</p><div class="line"></div>'
        '<div class="line"></div><p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：常數和平衡是什麼，題目保證了什麼</li><li>說出古典八張卡最壞要翻幾張</li>'
        '<li>用八支箭頭解釋：常數相長、平衡相消</li><li>指出一個限制：這是玩具問題，它示範干涉，不代表實際應用</li>'
        '<li>替判案紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q012 一次看穿 列印包', '父子科技學院 量子電腦學程 Q012｜多伊奇–喬薩：一次看穿', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q012-deutsch-jozsa', folder='Q012_一次看穿', files=FILES,
        sheet=('03_判案紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_一次看穿.pdf', pack_pages=4,
        pack_needles=('函數卡', '出題單', '判案紀錄', '偵探推理', '平衡函數', '箭頭', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q012', episode_dir='specials/q012-deutsch-jozsa',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'game': '偵探翻牌（八張函數卡）＋干涉場景量子判定',
               'program': 'dj_check.py（只用 Python 標準函式庫）', 'cases': [c[:4] for c in CASES],
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q012/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

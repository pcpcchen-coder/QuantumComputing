"""Q073 課堂教材：裝載與重排 — 動畫操作步驟、棋盤競速規則與紀錄、重排演算法紀錄、填滿機率表、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/atoms.html（#tweezer），用瀏覽器開啟；另備西洋棋盤（8×8）、棋子或圍棋子、硬幣、骰子。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q073/classroom.py
"""
from math import comb, log10
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent


def tail(m, n, q):
    """(T+4)² 支光鑷裡至少 N 顆原子的機率（同 08_tweezer.js 插圖的綠線）。"""
    return sum(comb(m, k) * q ** k * (1 - q) ** (m - k) for k in range(n, m + 1))


# 動畫的三種陣列大小（目標 T×T，光鑷 (T+4)×(T+4)），裝載機率 p = 0.5
ODDS = []
for T in (4, 6, 8):
    N, M = T * T, (T + 4) * (T + 4)
    ODDS.append((T, M, N, N // 2, round(N * log10(0.5), 1), tail(M, N, 0.5)))
assert ODDS[0][1] == 64 and ODDS[0][3] == 8          # 8×8 光鑷＝西洋棋盤；平均 8 個空位
assert abs(100 * log10(0.5) + 30.1) < 0.05           # 0.5¹⁰⁰ ≈ 10⁻³⁰
assert ODDS[2][5] > 0.9                               # 8×8 目標、重排後仍 > 90 %

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q073：裝載與重排（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：光鑷陣列裝載完，為什麼總有大約一半是空的？空位要怎麼補滿？

需要：瀏覽器開 `animations/atoms.html#tweezer`；一張西洋棋盤（8×8）、約 40 顆棋子（棋子不夠可用圍棋子或硬幣代替）、一枚硬幣、一顆骰子。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 碰撞阻斷、裝載→成像→重排→再成像、不重排的機率 | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 棋盤競速（最少步數）＋在動畫裡看重排 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子寫自己的重排規則，在棋盤上試、和動畫對照 | 列印包第 3 頁、`03_競速與規則紀錄.csv` |
| 105–115 | 孩子教爸爸：為什麼有空位、怎麼補滿、哪裡有風險 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#tweezer` 走一次：把「陣列大小」拉到 4（光鑷 8×8，和棋盤一樣）→ ① 裝載 → ② 成像 → ③ 重排，看讀數「搬運 x / n」。
- 列印 `02_列印包_裝載與重排.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 棋盤競速怎麼玩

1. 中間 4×4（第 3–6 行、第 3–6 列）是目標區，外圍兩圈是儲備區。
2. 隨機裝載：每一格擲一次硬幣，正面就放一顆棋子。擺好後拍照或畫在列印包上，兩人用同一盤。
3. 搬運：每次拿起一顆棋子，只能直走或橫走，一格算一步；棋子沿格線之間的通道走，不會被別的棋子擋住（就像動畫裡移動光鑷走光鑷之間的通道）。
4. 目標區 16 格全部有棋子就完成。總步數少的人贏；平手比搬運次數。
5. 加碼（示意）：每搬一顆就擲一次骰子，擲到 1，那顆棋子算掉了，要再補一次。

## 誠實說明

- 課綱寫的「動畫玩家重排模式」目前還沒有：動畫只會跑它自己的規則。孩子的規則在棋盤上驗證，再和動畫的搬運次數對照。
- 「擲到 1 就掉」只是遊戲規則，用來體會「步數越多，掉的機會越大」，不是真實機器的掉落率；動畫本身也不模擬掉原子。
- 每格約一半：簡報寫約 50 %，動畫說明寫約 50–60 %。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 隨機裝載與成像（`atoms.html#tweezer`，約 10 分鐘）

1. 按「① 裝載」：紅色原子雲罩住光鑷，淡去後留下青色原子。
2. 按「② 成像」：原子亮起，目標區的空位變成紅圈。讀面板上的「原子 N 顆（裝載率 %）」，記在列印包第 1 頁。
3. 再重複 4 次，看每次的裝載率和紅圈位置。

## B. 填滿機率（約 5 分鐘）

看右下角插圖「目標區全部填滿的機率」：紅線＝不重排（p^N），綠線＝重排。拉「陣列大小」和「裝載機率 p」，看兩個圓點怎麼移動。

## C. 棋盤競速（約 20 分鐘）

照「00_爸爸先讀」的規則玩至少兩盤，記在列印包第 2 頁。

## D. 看動畫重排（約 5 分鐘）

1. 「陣列大小」拉到 4 → ① 裝載 → ② 成像，數紅圈有幾個。
2. 按「③ 重排」：洋紅色的移動光鑷一次搬一顆，先補離中心近的空位，每次找金框外最近的原子。
3. 搬完看讀數「搬運 n / n」：n 是不是等於剛才數到的紅圈數？

## E. 下半場：寫自己的重排規則（約 30 分鐘）

用列印包第 3 頁寫 3–5 行規則，在棋盤上用同一盤擺法照做，記下搬運次數和總步數，和上半場及動畫對照。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 動畫三種大小（裝載機率 p = 0.5，以動畫插圖的公式重算）\n\n'
  '| 目標 T×T | 光鑷支數 | 目標原子數 N | 平均空位（搬運次數） | 不重排全滿：0.5^N | 重排後全滿（原子夠用的機率） |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {T}×{T} | {M} | {N} | 約 {e} | 約 10^{lg} | 約 {100 * q:.3f}% |\n' for T, M, N, e, lg, q in ODDS)
  + '\n100 顆時不重排：0.5¹⁰⁰ ≈ 10⁻³⁰（簡報第 26 頁）。\n\n'
  '## 棋盤競速\n\n'
  '- 搬運次數最少＝目標區的空位數（每搬一次只補一格）。所以真正能比的是**總步數**。\n'
  '- 每顆棋子的步數至少是它到空位的「橫向格數＋直向格數」。好規則：先把最難補的空位（離儲備區遠的，例如靠中心的）配給最近的棋子。\n'
  '- 動畫的規則：空位依離中心距離排序，近的先補；每個空位配金框外「橫＋直格數」最近的原子。它是簡單的貪婪法，不一定是總步數最少。\n'
  '- 加碼規則下，步數和搬運次數越多，擲到 1 的次數越多——這就是課綱的注意事項：搬運有機率掉原子，步數越多，掉的機會越大。\n\n'
  '## 常見問題\n\n'
  '- 為什麼每格只有 0 或 1 顆？光鑷很小，兩顆原子在光照下碰撞，一起被踢出（碰撞阻斷）。\n'
  '- SLM 和 AOD 差在哪？SLM 畫出整片靜態光鑷（停車格），換圖約 10 ms；AOD 用 RF 頻率改偏折角，μs 級，負責搬運（搬運車）。\n'
  '- 為什麼搬完要再拍照？搬運可能掉原子，再成像確認目標區真的排滿才開始計算。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `atoms.html#tweezer`（中性原子場景 8：光鑷裝載與重排）

- 按鈕：① 裝載、② 成像、③ 重排、全部重來。
- 滑桿「陣列大小（目標 T×T）」：4–8，光鑷是 (T+4)×(T+4) 支；改動後陣列重建。
- 滑桿「裝載機率 p」：40–70 %。
- 顏色：紅色雲＝磁光阱原子雲、青色球＝原子、金框＝目標區、紅圈＝目標區空位、洋紅色錐＝AOD 移動光鑷。
- 讀數：光鑷支數、原子數與裝載率、目標區填滿數、搬運次數。
- 右下插圖：目標區全部填滿的機率（log₁₀）；紅線不重排、綠線重排。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '誰', '裝載率或空位數', '規則（簡述）', '搬運次數', '總步數', '擲到 1 掉了幾顆', '備註']
SHEET_ROWS = ([[f'動畫裝載第 {i} 次', '', '', '', '', '', '', ''] for i in range(1, 6)]
              + [[f'棋盤競速第 {i} 盤', w, '', '', '', '', '', ''] for i in (1, 2) for w in ('孩子', '爸爸')]
              + [['自己的規則', '孩子', '', '', '', '', '', ''], ['動畫的規則（4×4）', '動畫', '', '先補中心、配最近', '', '', '', '']])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}
table.board{border-collapse:collapse;margin:3mm 0}table.board td{width:8mm;height:8mm;border:1pt solid #888;padding:0}
table.board td.t{background:#f6e3b8}'''


def board():
    cells = ''.join('<tr>' + ''.join(f'<td class="{"t" if 2 <= i < 6 and 2 <= j < 6 else ""}"></td>' for j in range(8)) + '</tr>'
                    for i in range(8))
    return f'<table class="board">{cells}</table>'


def html():
    pages = [
        '<h2>實驗一：隨機裝載</h2><p class="lead">在 atoms.html#tweezer：按 ① 裝載 → ② 成像，記下面板讀數。重複五次。</p>'
        '<table class="rec"><tr><th>第幾次</th><th>原子幾顆</th><th>裝載率</th><th>目標區紅圈幾個</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td></tr>' for i in range(1, 6)) + '</table>'
        '<p>五次的裝載率大約都在多少？＿＿＿＿　為什麼不會是 100%？</p><div class="line"></div>'
        '<p class="note">右下插圖：不重排時，100 顆全部到位的機率約 10⁻³⁰。</p>',
        '<h2>棋盤競速：最少步數排整齊</h2><p class="lead">中間淺色 4×4 是目標區。每格擲硬幣，正面放棋子；把擺法畫在下面，兩人用同一盤。</p>'
        + board() +
        '<table class="rec"><tr><th>盤</th><th>誰</th><th>空位數</th><th>搬運次數</th><th>總步數</th><th>擲到 1 掉了幾顆</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td>{w}</td><td></td><td></td><td></td><td></td></tr>' for i in (1, 2) for w in ('孩子', '爸爸')) + '</table>'
        '<p class="note">發現了嗎？搬運次數最少就是＿＿＿＿的數目。</p>',
        '<h2>換你改造：重排演算法紀錄（今天的作品）</h2><p class="lead">寫 3–5 行，讓別人照著做也能排滿。</p>'
        '<div class="card"><h3>我的重排規則</h3><p>1.</p><div class="line"></div><p>2.</p><div class="line"></div>'
        '<p>3.</p><div class="line"></div><p>4.</p><div class="line"></div><p>5.</p><div class="line"></div></div>'
        '<p>用同一盤試：搬運次數＿＿＿　總步數＿＿＿　上半場最好成績＿＿＿</p>'
        '<p>動畫（4×4）：紅圈＿＿＿個　搬運次數＿＿＿　一樣嗎？＿＿＿</p>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p class="note">生活技能：設計演算法——把一件事拆成清楚的步驟，別人照做也能成功。</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 為什麼裝載完總有大約一半是空的？</p><div class="line"></div>'
        '<p>2. 重排怎麼把空位補滿？（拍照、規劃、移動光鑷）</p><div class="line"></div>'
        '<p>3. SLM 和 AOD 各負責什麼？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出碰撞阻斷：每格 0 或 1 顆、約一半</li><li>說出一輪準備四步：裝載、成像、重排、再成像</li>'
        '<li>說出不重排為什麼不行：0.5 連乘很多次</li><li>指出一個限制：搬運可能掉原子，步數越多越容易掉</li>'
        '<li>替重排演算法紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q073 裝載與重排 列印包', '父子科技學院 量子電腦學程 Q073｜裝載與重排', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q073-loading-rearrangement', folder='Q073_裝載與重排', files=FILES,
        sheet=('03_競速與規則紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_裝載與重排.pdf', pack_pages=4,
        pack_needles=('隨機裝載', '棋盤競速', '重排演算法紀錄', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q073', episode_dir='specials/q073-loading-rearrangement',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#tweezer'],
               'materials': ['西洋棋盤 8×8', '棋子或圍棋子約 40 顆', '硬幣', '骰子'],
               'fillOdds': [{'T': T, 'tweezers': M, 'N': N, 'log10NoRearrange': lg, 'pRearranged': round(q, 4)}
                            for T, M, N, _, lg, q in ODDS],
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q073/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

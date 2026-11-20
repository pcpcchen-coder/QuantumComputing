"""Q086 課堂教材：邏輯閘與魔術態 — 動畫操作步驟、價目表、資源估算表（今天的作品）、工程答辯紀錄、一輪與兩輪比較、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/transmon-3d.html#surgery（第 11 章），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q086/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent


def sup(p):
    """10⁻ⁿ 形式的科學記號（給表格用）。"""
    m, e = f'{p:.1e}'.split('e')
    return f'{m}×10' + ''.join('⁻⁰¹²³⁴⁵⁶⁷⁸⁹'[0 if c == '-' else int(c) + 1] for c in str(int(e)))


OUT1 = lambda p: 35 * p ** 3          # 動畫 out1()：15-to-1 一輪的輸出錯誤率近似
ACC = lambda p: (1 - p) ** 15          # 動畫看板：接受率 ≈ (1 − p)¹⁵

# 動畫看板「邏輯閘從哪裡來？」（drawBoard11 intro）
PRICE = [('X、Z（Pauli）', '只記在軟體裡（Pauli frame）', '幾乎免費'),
         ('多位元 Pauli 量測', 'lattice surgery：合併 → 量 d 輪 → 拆開', '約 d μs'),
         ('H、S、CNOT（Clifford）', '由 lattice surgery 組合、補丁變形', '數倍 d μs'),
         ('T（非 Clifford）', '魔術態 + 閘傳送；魔術態要蒸餾或培育', '最貴')]

# 蒸餾：注入錯誤率 p 下的一輪輸出與接受率（動畫自由實驗滑桿 10⁻⁴～10⁻¹·³ ≈ 5%）
PS = [1e-4, 1e-3, 1e-2, 0.04, 0.05]
DIST = [(p, OUT1(p), round(100 * ACC(p), 1)) for p in PS]
P2 = OUT1(OUT1(1e-3))                  # 兩輪：約 1.5×10⁻²¹

# ---- 練習用的假設數字（教學用，不是任何真實演算法的估算）----
T_COUNT = 1_000_000                    # 假設演算法需要的 T 閘數
CLIFF_COUNT = 10_000_000               # 假設的 Clifford 閘數（不消耗魔術態）
RUN_S = 10                             # 假設希望 10 秒內把 T 閘做完
RATE1 = 10_000                         # 假設：一座「一輪」工廠每秒產出 1 萬顆
RATE2 = 1_000                          # 假設：一座「兩輪」工廠每秒產出 1 千顆
INJ1 = T_COUNT * 15
INJ2 = T_COUNT * 225
NEED_RATE = T_COUNT // RUN_S           # 每秒要用掉幾顆魔術態
FAC1 = -(-NEED_RATE // RATE1)          # 10 座
FAC2 = -(-NEED_RATE // RATE2)          # 100 座
assert (INJ1, INJ2, NEED_RATE, FAC1, FAC2) == (15_000_000, 225_000_000, 100_000, 10, 100)

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q086：邏輯閘與魔術態（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出兩個問題：表面碼把資料存好之後，要怎麼在邏輯位元上計算？哪一種閘最花錢？

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `transmon-3d.html#surgery`（第 11 章：Lattice surgery 與魔術態蒸餾）。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 兩類閘、價目表、晶格手術、閘傳送、蒸餾 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 在動畫裡看手術與工廠、填資源估算表、玩工程答辯 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 比較一輪與兩輪蒸餾的資源估算，找出主要成本 | 列印包第 3 頁、`03_估算與答辯紀錄.csv` |
| 105–115 | 孩子教爸爸：為什麼 T 閘最貴 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在第 11 章把步驟 ①–⑦ 播一次（約 3 分鐘），再按步驟 8 試「準備接縫 → 合併 → 拆開」。
- 列印 `02_列印包_邏輯閘與魔術態.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 工程答辯怎麼玩

爸爸當評審，給一個演算法的 T 閘數和 Clifford 閘數（可用列印包的假設數字，也可以自己出）。孩子當工程師，算出要幾顆魔術態、要消耗幾顆注入態、要幾座工廠，最後回答：「成本主要花在哪裡？」評審至少追問一題，例如「一輪不夠乾淨怎麼辦？」「Clifford 閘那麼多，為什麼不算它？」

## 誠實說明

- 價目表的「約 d μs」「數倍 d μs」、注入錯誤率約 10⁻³、Shor 需要 10⁻¹⁰ 以下，都是動畫與教學紀錄的代表值。
- 35p³ 是一階近似；動畫的抽樣模型是簡化的。
- 列印包的 T 數（{T_COUNT:,}）、Clifford 數、工廠每秒產量是**練習用的假設數字**，不是任何真實演算法的估算。
- 本課最重要的注意事項：容錯時代的成本主要在 T 閘與魔術態工廠，不在 Clifford 閘。
''',

'01_操作步驟.md': '''# 操作步驟（`transmon-3d.html#surgery`）

## A. 價目表與閘傳送（約 10 分鐘）

1. 開啟後是步驟 ①。看後方看板「邏輯閘從哪裡來？」：四列由便宜到貴，最後一列 T 是橘色的「最貴」。抄到列印包第 1 頁。
2. 按步驟 5（T 閘傳送）：看板上是「資料位元 ψ」和「魔術態 |T⟩」兩個方塊，下面四行輪流變金色。第 ④ 行會隨機告訴你這次要不要補一個 S。

## B. 晶格手術（約 10 分鐘）

1. 按步驟 8（自由實驗）。中間那一行淡淡的圓球是接縫位元。
2. 按「準備接縫」→「合併（量 X_A·X_B）」：數一數新出現的穩定子方塊，看看板一輪一輪列出結果與乘積（共 3 輪）。
3. 按「拆開」：接縫位元閃白光被量掉，回到兩塊補丁。多做幾次，記下每次的 X_A·X_B——個別結果隨機，乘積才有意義。

## C. 魔術態工廠（約 10 分鐘）

1. 按步驟 6、7 看一輪和兩輪蒸餾；看板的柱子越矮越乾淨，灰色是 Shor 需要的程度。
2. 回到步驟 8，按「看魔術態工廠」，拉「注入錯誤率 p」滑桿，按「跑 2000 次統計」：試 10⁻³、1%、4%、5%，把接受率記在列印包第 3 頁。

## D. 下半場：比較兩種資源估算（約 30 分鐘）

用列印包第 3 頁，同一個演算法分別用一輪和兩輪蒸餾估算注入態數與工廠數，找出主要成本。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 邏輯閘的價目表（動畫看板）\n\n| 邏輯運算 | 做法 | 代價 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in PRICE)
  + '\n## 15-to-1 蒸餾（一輪；輸出 ≈ 35p³，接受率 ≈ (1 − p)¹⁵）\n\n| 注入錯誤率 p | 一輪輸出 | 接受率 |\n|---|---|---|\n'
  + ''.join(f'| {sup(p)} | {sup(o)} | 約 {a}% |\n' for p, o, a in DIST)
  + f'\n兩輪（p = 10⁻³）：約 {sup(P2)}，每顆消耗 225 顆注入態。p = 5% 時一輪輸出 {sup(OUT1(0.05))}，仍比輸入乾淨，但接受率不到一半，每顆實際要花更多注入態（15 ÷ 接受率）。動畫的 2000 次統計會和表格差一點點。\n\n'
  '## 資源估算（練習用假設數字）\n\n'
  f'- 假設 T 閘 {T_COUNT:,} 個、Clifford 閘 {CLIFF_COUNT:,} 個、希望 {RUN_S} 秒內做完。\n'
  f'- 魔術態：一個 T 閘一顆 → {T_COUNT:,} 顆；Clifford 閘不消耗魔術態。\n'
  f'- 注入態：一輪 ×15 = {INJ1:,} 顆；兩輪 ×225 = {INJ2:,} 顆（差 15 倍）。\n'
  f'- 每秒要用掉 {NEED_RATE:,} 顆魔術態：一輪工廠（假設每秒 {RATE1:,} 顆）要 {FAC1} 座；兩輪工廠（假設每秒 {RATE2:,} 顆）要 {FAC2} 座。\n'
  '- 主要成本：T 閘 → 魔術態 → 注入態與工廠面積；Clifford 閘雖然多，不需要魔術態。\n\n'
  '## 常見問題\n\n'
  '- 為什麼 Clifford 閘「好做」？表面碼上可以用 lattice surgery（合併、量 d 輪、拆開）與補丁變形組出來，全程受保護；X、Z 只要記在軟體裡。\n'
  '- 為什麼不能全部用橫向閘？Eastin–Knill 定理：沒有碼能把一組通用閘全部做成橫向。\n'
  '- 只有 Clifford 不夠嗎？Gottesman–Knill 定理：只用 Clifford 閘與 Pauli 量測的電路，古典電腦能有效率地模擬。\n'
  '- 合併時為什麼要量 d 輪？量測本身也會出錯，要多輪資料讓解碼器在時間方向上抓錯。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `transmon-3d.html#surgery`（第 11 章：Lattice surgery 與魔術態蒸餾）

- 步驟按鈕 1–8：① 為什麼、② 合併、③ 拆開、④ CNOT、⑤ T 閘傳送、⑥ 蒸餾、⑦ 第二輪與工廠、⑧ 自由實驗。
- 「◀ 上一步／暫停／重播／下一步 ▶」與「自動接續」核取方塊（取消勾選就停在目前步驟）。
- 圖例：圓球＝資料位元（中間一行是接縫）；青色格子＝Z 穩定子、琥珀色格子＝X 穩定子；亮框是合併時新打開的穩定子，亮起＝量到 −1。
- 工廠：橘色球＝注入的髒魔術態、金色球＝蒸餾後的乾淨魔術態、紅色＝有錯；頂上的燈是檢查值。
- 自由實驗：準備接縫、合併（量 X_A·X_B）、拆開、重設；看 lattice surgery／看魔術態工廠；注入錯誤率 p 滑桿；1 輪／2 輪；跑一輪；跑 2000 次統計。

## 操作

滑鼠拖曳旋轉、滾輪縮放；鍵盤左右鍵換章。
''',
}

SHEET_HEADER = ['項目', '注入錯誤率 p', '輪數', '接受率（%）', '輸出錯誤率', 'T 閘數', '魔術態數', '注入態數', '工廠數', '備註']
SHEET_ROWS = ([['蒸餾統計', sup(p), '1', '', '', '', '', '', '', ''] for p in PS[1:]]
              + [['資源估算（一輪）', '10⁻³', '1', '', '', str(T_COUNT), '', '', '', '假設數字'],
                 ['資源估算（兩輪）', '10⁻³', '2', '', '', str(T_COUNT), '', '', '', '假設數字']]
              + [[f'工程答辯第 {i} 題', '', '', '', '', '', '', '', '', ''] for i in range(1, 6)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>邏輯閘的價目表</h2><p class="lead">在 transmon-3d.html#surgery 步驟 ①，把後方看板抄下來（由便宜到貴）。</p>'
        '<table class="rec"><tr><th>邏輯運算</th><th>怎麼做</th><th>代價</th><th>要魔術態嗎</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td><td></td></tr>' for a, _, _ in PRICE) + '</table>'
        '<div class="card"><h3>資源估算表（今天的作品）</h3>'
        f'<p>演算法：＿＿＿＿＿＿　T 閘數：＿＿＿＿＿　Clifford 閘數：＿＿＿＿＿</p>'
        '<p>魔術態：＿＿＿＿ 顆　注入態（一輪 ×15）：＿＿＿＿ 顆　工廠：＿＿＿ 座</p>'
        '<p>主要成本在：＿＿＿＿＿＿＿＿＿＿　理由：</p><div class="line"></div>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>工程答辯：成本花在哪裡</h2><p class="lead">評審（爸爸）出題、追問；工程師（你）用數字回答。</p>'
        '<table class="rec"><tr><th>題</th><th>T 閘數</th><th>Clifford 閘數</th><th>魔術態</th><th>注入態</th><th>評審追問</th><th>我的回答</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 6)) + '</table>'
        '<p class="note">答不出來？回頭查價目表：哪一列要消耗魔術態？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：一輪 vs 兩輪</h2>'
        f'<p class="lead">練習用假設：T 閘 {T_COUNT:,} 個、希望 {RUN_S} 秒內做完；一輪工廠每秒產 {RATE1:,} 顆、兩輪工廠每秒產 {RATE2:,} 顆。</p>'
        '<table class="rec"><tr><th></th><th>每顆魔術態用掉的注入態</th><th>注入態總數</th><th>每秒要幾顆</th><th>工廠數</th><th>輸出錯誤率</th></tr>'
        '<tr><td>一輪</td><td>15</td><td></td><td></td><td></td><td></td></tr><tr><td>兩輪</td><td>225</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p>動畫統計（步驟 8、跑 2000 次）：p = 10⁻³ 接受率＿＿%　p = 1% ＿＿%　p = 4% ＿＿%　p = 5% ＿＿%</p>'
        '<p class="note">生活技能：估算成本——先找出最貴的那一項，才知道該從哪裡省。你想到哪個例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 哪些閘是 Clifford 閘？為什麼「好做」？</p><div class="line"></div>'
        '<p>2. T 閘怎麼用魔術態做出來？</p><div class="line"></div><p>3. 15-to-1 蒸餾怎麼把魔術態變乾淨？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出兩類閘：Clifford 好做、T 難做</li><li>說出魔術態怎麼用：蒸餾乾淨，再消耗一顆</li>'
        '<li>說出一輪和兩輪各消耗幾顆注入態</li><li>指出一個限制：成本主要在 T 閘，不在 Clifford 閘</li>'
        '<li>替資源估算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q086 邏輯閘與魔術態 列印包', '父子科技學院 量子電腦學程 Q086｜邏輯閘與魔術態', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q086-logical-gates-magic-states', folder='Q086_邏輯閘與魔術態', files=FILES,
        sheet=('03_估算與答辯紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_邏輯閘與魔術態.pdf', pack_pages=4,
        pack_needles=('價目表', '資源估算表', '工程答辯', '一輪 vs 兩輪', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q086', episode_dir='specials/q086-logical-gates-magic-states',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/transmon-3d.html#surgery'],
               'practiceAssumptions': {'tCount': T_COUNT, 'cliffordCount': CLIFF_COUNT, 'runSeconds': RUN_S,
                                       'factoryRatePerSecond1': RATE1, 'factoryRatePerSecond2': RATE2},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q086/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

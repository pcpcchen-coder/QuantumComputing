"""Q042 課堂教材：安全須知、打氣筒與除塵罐實驗步驟、實驗紀錄表、脈衝管循環對照圖、電費帳計算、解說卡與解答。

不需要帳號、不需要安裝；器材是打氣筒與空氣除塵罐（除塵罐由家長操作）。動畫用瀏覽器開 animations/peripherals.html#pulsetube。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q042/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 規格（學程簡報「量子電腦的周邊系統」第 8 頁：PT415／CPA1110）
SPEC = {'compressor_kW': 10.7, 'water_L_min': 11.5, 'stage2_W_at_4K2': 1.5, 'stage1_W_at_45K': 40, 'valve_Hz': 1.4}
RATIO = SPEC['compressor_kW'] * 1000 / SPEC['stage2_W_at_4K2']   # 7133
PERIOD = 1 / SPEC['valve_Hz']                                     # 0.714 s
CARNOT = 4.2 / (300 - 4.2)                                        # 0.0142
ACTUAL = SPEC['stage2_W_at_4K2'] / (SPEC['compressor_kW'] * 1000)  # 0.00014
assert round(RATIO) == 7133 and round(PERIOD, 2) == 0.71 and round(CARNOT * 100, 2) == 1.42

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q042：脈衝管與壓縮機（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：用打氣筒和除塵罐體驗「壓縮變熱、膨脹變冷」，再對照動畫，說出脈衝管怎麼靠壓力一高一低和蓄冷器，把冷端降到約 3 K。

## 器材

- 打氣筒（腳踏車用即可）、一顆可打氣的球或輪胎（讓打氣筒有東西可壓）
- 空氣除塵罐一罐（**由家長操作**）
- 計時器（手機即可）；可選：廚房用或額溫用的溫度計
- 列印 `02_列印包_脈衝管與壓縮機.pdf`（A4，共 4 頁）
- 瀏覽器打開學程的 `animations/peripherals.html#pulsetube`（下載 `animations/` 資料夾即可離線使用）

## 安全須知（實驗前先一起讀）

- 除塵罐**只能正放**使用。倒過來會噴出極冷的液體，液體沸點很低，可能造成凍傷。
- 除塵罐由家長操作；**不對人、不對動物噴**；不要吸入；遠離火源；不要加熱或刺穿罐子。
- 每次只短按幾秒；罐身變冰時先放下，等回溫再用。
- 打氣時不要打到超過輪胎或球標示的壓力。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三步：壓、放、存；四個零件；一個循環 | 影片第 2–7 段、列印包第 3 頁 |
| 25–65 | 安全須知 → 寫預測 → 打氣筒實驗 → 除塵罐實驗（家長）→ 對照動畫 | `01_實驗步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子寫出：為什麼冷端沒有會動的零件是一個優點 | 列印包第 4 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（最後一關） |
| 115–120 | 錄音總結、替實驗紀錄取名、存檔 | |

## 誠實說明

- 打氣筒變溫，一部分來自氣體被壓縮，一部分來自活塞摩擦；本課不區分各佔多少。
- 除塵罐裡裝的是可液化的氣體，變冰主要來自液體汽化、氣體膨脹時吸熱；和脈衝管裡的氦氣原理相近但不完全相同。
- 規格數字（10.7 kW、1.5 W、40 W、11.5 公升／分鐘）是一款常見機型的規格，不同機型不同。
''',

'01_實驗步驟.md': '''# 實驗步驟

## 實驗一：打氣筒（壓縮變熱，約 10 分鐘）

1. 在列印包第 1 頁寫預測：打氣幾十下之後，打氣筒底部會變熱、變冷，還是不變？
2. 打氣前，孩子先摸打氣筒底部（靠近出氣口那一段），記下感覺（冷／普通／溫／熱）。
3. 接上球或輪胎，快速打氣 30 下；記下用了幾秒。
4. 馬上再摸同一個位置，記下感覺。有溫度計的話，貼著量一次。
5. 休息一分鐘，再摸一次，看看熱量是不是慢慢散掉了。

## 實驗二：除塵罐（膨脹變冷，約 10 分鐘，家長操作）

1. 先讀列印包第 1 頁的安全須知。
2. 孩子寫預測；摸罐身（還沒噴之前）記下感覺。
3. 家長**正放**拿著罐子，朝空的方向（不是人）連續短噴 3 次，每次約 2 秒。
4. 孩子摸罐身，記下感覺；有溫度計的話量一次。
5. 放著兩分鐘，罐身慢慢回溫，再摸一次。

## 實驗三：對照動畫（約 15 分鐘）

1. 打開 `animations/peripherals.html#pulsetube`。
2. 把「顯示速度」拉到最慢，看「冷頭內壓力」小圖：一下高、一下低。
3. 看控制面板的讀數：高壓相寫「氣體壓縮」、低壓相寫「氣體膨脹 → 冷端吸熱」。
4. 對照列印包第 3 頁：哪一步像打氣筒？哪一步像除塵罐？
5. 看粒子顏色：上面紅（室溫），一級冷端附近橘黃（約 45 K），二級冷端附近綠（約 3 K）。

## 下半場：冷端不動的好處（約 30 分鐘）

在列印包第 4 頁寫出至少三個理由，並寫一個「還是有的限制」。
''',

'04_解答.md': f'''# 解答（爸爸用）

## 實驗結果的方向

- 打氣筒：打氣後底部變溫或變熱（壓縮＋摩擦），放一會兒又回到室溫。
- 除塵罐：噴完罐身變冰（液體汽化、氣體膨脹吸熱），放一會兒回溫。
- 和脈衝管的對照：打氣筒像「高壓進來」那一步（壓縮的熱在室溫端丟掉）；除塵罐像「切到低壓」那一步（冷端膨脹、吸熱）。

## 電費帳

- 壓縮機用電 {SPEC['compressor_kW']} kW ＝ {SPEC['compressor_kW'] * 1000:.0f} W；二級冷端在 4.2 K 時 {SPEC['stage2_W_at_4K2']} W。
- {SPEC['compressor_kW'] * 1000:.0f} ÷ {SPEC['stage2_W_at_4K2']} ≈ {RATIO:.0f}，大約七千倍。
- 冷卻水每分鐘 {SPEC['water_L_min']} 公升，一小時 {SPEC['water_L_min'] * 60:.0f} 公升。
- 旋轉閥每秒約 {SPEC['valve_Hz']} 次 → 一輪約 {PERIOD:.2f} 秒。
- 為什麼越冷越難搬熱？把熱從低溫搬到室溫，理論上最好的效率是 低溫 ÷（室溫 − 低溫）。4.2 K 對 300 K：4.2 ÷ 295.8 ≈ {CARNOT * 100:.2f} %。實際只有 {ACTUAL * 100:.3f} %，大約是理論上限的百分之一。溫度越低，這個上限就越小。

## 冷端不動的好處（參考答案）

1. 振動小：晶片和測量線路怕晃動，振動會在線路上變成雜訊。
2. 少磨損、更可靠：冷端藏在真空罩裡，要修得整台回溫，之後再花約 1–2 天重新降溫。
3. 構造簡單：沒有低溫的活塞（排氣器），零件少、比較便宜。

限制：旋轉閥和氣流仍會帶來一點振動；有些系統把馬達移遠（遠端馬達），振動更小，但約損失 20 % 冷卻功率（例如 1.5 W → 約 1.2 W）。
''',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/peripherals.html#pulsetube`（周邊系統場景 2：脈衝管冷卻）

- 左邊：氦壓縮機（電力約 10 kW、水冷）；橘紅色管子是高壓氦（約 2 MPa），藍色是低壓氦（約 0.8 MPa）。
- 冷頭：旋轉閥、蓄冷器、一級脈衝管、二級蓄冷器、二級脈衝管、緩衝槽＋孔口。
- 粒子顏色代表溫度：上面紅（室溫）、一級冷端附近橘黃（約 45 K）、二級冷端附近綠（約 3 K）。
- 「顯示速度」滑桿：只改動畫快慢；真實的旋轉閥約每秒 1.4 次。
- 「冷頭內壓力」小圖與讀數：高壓相＝氣體壓縮；低壓相＝氣體膨脹、冷端吸熱。

## `animations/peripherals.html#overview`（周邊系統場景 1：系統全景）

- 按「只看冷卻相關」：只留下脈衝管氦氣（綠）、冷卻水（藍）、混合氣循環（紫）、真空（灰）。
- 按「視角：冷凍機頂部」：看綠色軟管接進冷凍機頂部的冷頭。
- 「典型用電分配」：脈衝管壓縮機約 10.7 kW，是機房裡最耗電的單一設備。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['實驗', '操作者', '預測（變熱／變冷／不變）', '動作', '時間（秒）', '之前的感覺', '之後的感覺', '溫度計讀數（可不填）', '和預測一樣嗎']
SHEET_ROWS = [
    ['打氣筒 第 1 次', '孩子', '', '快速打氣 30 下'],
    ['打氣筒 第 2 次', '孩子', '', '快速打氣 30 下'],
    ['打氣筒 休息一分鐘後', '孩子', '', '不動'],
    ['除塵罐 第 1 次', '家長', '', '正放、短噴 3 次'],
    ['除塵罐 第 2 次', '家長', '', '正放、短噴 3 次'],
    ['除塵罐 放兩分鐘後', '家長', '', '不動'],
]

EXTRA_CSS = '''table.rec td{height:11mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.warn{border:2pt solid #c0392b;border-radius:3mm;padding:3mm 4.5mm;background:#fdf1ef}.warn h3{color:#c0392b}
.cyc{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin:3mm 0}.cyc div{border:1.3pt solid #0b2540;border-radius:3mm;padding:3mm;min-height:40mm}
.cyc b{display:block;font-size:13pt;margin-bottom:1mm}.ladder td{text-align:center}'''


def html():
    pages = [
        '<h2>實驗前：安全須知與預測</h2><p class="lead">今天的科學實驗：壓縮變熱、膨脹變冷。</p>'
        '<div class="warn"><h3>安全須知（一起讀，讀完打勾）</h3><ul class="chk">'
        '<li>除塵罐只能正放；倒過來會噴出極冷液體，可能凍傷</li><li>除塵罐由家長操作，不對人、不對動物噴</li>'
        '<li>不吸入、遠離火源、不加熱、不刺穿罐子</li><li>每次只短噴幾秒，罐身變冰就先放下</li>'
        '<li>打氣不超過球或輪胎標示的壓力</li></ul></div>'
        '<div class="box" style="margin-top:6mm"><h3>我的預測</h3>'
        '<p>1. 快速打氣 30 下後，打氣筒底部會：□ 變熱　□ 變冷　□ 不變</p><p>我為什麼這樣猜：</p><div class="line"></div>'
        '<p>2. 除塵罐短噴 3 次後，罐身會：□ 變熱　□ 變冷　□ 不變</p><p>我為什麼這樣猜：</p><div class="line"></div></div>',
        '<h2>實驗紀錄</h2><p class="lead">記錄員（你）負責摸溫度、計時；操作員（爸爸）負責打氣和除塵罐。</p>'
        '<table class="rec"><tr><th>實驗</th><th>操作者</th><th>動作</th><th>秒數</th><th>之前</th><th>之後</th><th>和預測一樣？</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[3]}</td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS)
        + '</table><p class="note">感覺可以寫：冷／普通／溫／熱。有溫度計就把數字寫在旁邊。</p>'
        '<div class="box" style="margin-top:4mm"><h3>我發現</h3><p>壓縮的時候，溫度＿＿＿＿；膨脹的時候，溫度＿＿＿＿。</p>'
        '<p>放一會兒之後，溫度都會＿＿＿＿，因為＿＿＿＿＿＿＿＿＿＿＿＿。</p></div>',
        '<h2>對照動畫：一個循環的三步</h2><p class="lead">打開 peripherals.html#pulsetube，把顯示速度拉到最慢。</p>'
        '<div class="cyc"><div><b>01 高壓進來</b>壓縮的熱在室溫端帶走<br><br>像哪個實驗？＿＿＿</div>'
        '<div><b>02 穿過蓄冷器</b>熱留在金屬網<br><br>蓄冷器像什麼？＿＿＿</div>'
        '<div><b>03 切到低壓</b>冷端膨脹、吸熱<br><br>像哪個實驗？＿＿＿</div></div>'
        '<table class="ladder"><tr><th>位置</th><th>室溫端</th><th>一級冷端</th><th>二級冷端</th></tr>'
        '<tr><td>溫度</td><td>約 300 K</td><td>約 45 K</td><td>約 3 K</td></tr>'
        '<tr><td>動畫粒子顏色</td><td></td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:5mm"><h3>電費帳（用計算機）</h3>'
        '<p>壓縮機用電 10.7 kW ＝ ＿＿＿＿ W；二級冷端在 4.2 K 時只有 1.5 W。</p>'
        '<p>＿＿＿＿ ÷ 1.5 ≈ ＿＿＿＿ 倍</p><p>旋轉閥每秒約 1.4 次，一輪約 ＿＿＿＿ 秒（1 ÷ 1.4）。</p>'
        '<p>為什麼越冷的地方越難把熱搬出去？</p><div class="line"></div></div>',
        '<h2>解說卡：冷端不動的好處</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>脈衝管在冷端沒有會動的零件，這是優點，因為：</p>'
        '<p>1.</p><div class="line"></div><p>2.</p><div class="line"></div><p>3.</p><div class="line"></div>'
        '<p>可是還是有一個限制：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：壓力一高一低＋蓄冷器，怎麼讓冷端變冷</li><li>說出兩級溫度：約 45 K 和約 3 K</li>'
        '<li>說出打氣筒和除塵罐各像循環的哪一步</li><li>指出一個注意事項：除塵罐倒置會噴出極冷液體，只能正放、家長操作</li>'
        '<li>替實驗紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q042 脈衝管與壓縮機 列印包', '父子科技學院 量子電腦學程 Q042｜脈衝管與壓縮機', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q042-pulse-tube', folder='Q042_脈衝管與壓縮機', files=FILES,
        sheet=('03_實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_脈衝管與壓縮機.pdf', pack_pages=4,
        pack_needles=('安全須知', '我的預測', '實驗紀錄', '一個循環的三步', '電費帳', '解說卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q042', episode_dir='specials/q042-pulse-tube',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'materials': '打氣筒、空氣除塵罐（家長操作）、計時器；可選溫度計',
               'safety': '除塵罐只能正放、由家長操作、不對人噴', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q042/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

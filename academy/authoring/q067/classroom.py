"""Q067 課堂教材：尋寶寶物卡（atoms.html#ionsys）、尋寶紀錄表、系統方塊圖底稿、離子阱與超導的設施比較表、最後一關與解答。

不需要帳號，也不需要安裝任何套件（動畫用瀏覽器開啟）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q067/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 寶物：(名稱, 動畫裡的標籤, 位置提示, 用哪個按鈕看得到它的連線, 子系統, 它的工作)；標籤逐字取自 animations/js/atoms/01_ionsys.js
TREASURES = [
    ('超高真空腔', '超高真空腔（表面電極阱 + 離子鏈）', '光學桌右半邊，銅色線圈中間', '全部', '真空與阱', '< 10⁻¹¹ mbar；晶片上方 50–100 μm 懸浮一串離子'),
    ('369 nm 雷射', '369 nm 冷卻 / 偵測', '桌面左邊第一台', '只看雷射', '雷射', '冷卻、初始化、偵測'),
    ('935 nm 雷射', '935 nm 回泵', '桌面左邊第二台', '只看雷射', '雷射', '把掉到旁邊能階的離子拉回來'),
    ('355 nm 脈衝雷射', '355 nm 脈衝雷射（Raman 閘）', '桌面左邊第四台', '只看雷射', '雷射', '兩道光交叉，做量子閘（頻差 12.6 GHz）'),
    ('聲光調變器 AOM', 'AOM（開關 · 調頻）→ 光纖', '雷射右邊的小方塊', '只看雷射', '光學', '微秒內開關、調頻，再接光纖'),
    ('成像物鏡與相機', '成像物鏡 → PMT / 相機', '真空腔正上方', '全部', '成像', '收集離子的螢光、數光子'),
    ('磁場線圈', '磁場線圈（3 對，定量子化軸）', '圍住真空腔的銅色圓環', '全部', '磁場', '定出量子化軸'),
    ('螺旋共振器', '螺旋共振器（RF 升壓）', '真空腔右邊的銅色圓柱', '只看電子訊號', '射頻', '把射頻升壓到數百伏，送進阱'),
    ('多通道 DAC', '多通道 DAC（阱電極 DC）', '後排機櫃', '只看電子訊號', '直流', '控制數十～數百片電極：位置、搬運'),
    ('微波號角', '微波號角 12.6 GHz', '真空腔後方', '只看電子訊號', '微波', '直接驅動量子位元（單位元閘）'),
    ('FPGA 時序控制', 'FPGA 時序控制（ARTIQ 類）', '後排左邊的機櫃', '只看電子訊號', '控制', '以奈秒精度指揮所有脈衝、讀光子計數'),
    ('冷卻水機', '冷卻水機（雷射散熱）', '畫面右邊', '只看設施', '設施', '帶走雷射與電子的熱'),
]
BONUS = [('399 nm 雷射', '光游離：裝載離子'), ('離子泵 + NEG', '持續抽氣，維持超高真空'), ('銣鐘 10 MHz', '所有頻率的共同時脈'),
         ('恆溫空調（±0.1 °C）', '光路與頻率不漂移'), ('UPS / 配電盤', '短暫停電時雷射不失鎖')]
COMPARE = [  # (項目, 超導, 離子阱)；依 docs/離子阱與中性原子系統指南.md 第 4 節與兩個動畫插圖
    ('機房中間的主角', '稀釋冷凍機（晶片 10 mK）', '光學桌＋超高真空腔'),
    ('最吃電的負載', '脈衝管壓縮機 10.7 kW、冷卻水 10 kW', '空調／冷卻水、雷射、控制電子'),
    ('單套用電（量級）', '約 25–26 kW（示意）', '商用機台官方 < 40 kW'),
    ('環境要求', '冷卻水、防振、³He 供應', '恆溫 ±0.1 °C、防振、潔淨'),
    ('停電後恢復', '重新降溫 2–5 天，再完整校準', '重新鎖雷射、重裝離子：數十分鐘～數小時'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q067：離子阱系統全景（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶孩子把一台離子阱量子電腦拆成子系統：真空腔與原子源、四道雷射、電子系統（射頻、直流、微波）、
成像讀取、時序控制與設施。今天的好玩機制是「尋寶」：你當藏寶人，孩子當尋寶員，在互動動畫裡找出每件設備、追出它的連線，最後畫成系統方塊圖。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 概念示範：五大子系統與一輪流程（冷卻 → 初始化 → 閘 → 偵測） | 影片第 3–8 段 |
| 25–65 | 尋寶：抽寶物卡、在 `animations/atoms.html#ionsys` 找到設備、用分類按鈕追連線，畫方塊圖 | 列印包第 1–3 頁、`03_寶物清單.csv` |
| 65–75 | 休息 | |
| 75–105 | 比較離子阱與超導的設施需求，可對照 `animations/peripherals.html#overview` | 列印包第 4 頁 |
| 105–115 | 孩子教爸爸：每個子系統在做什麼、一輪流程 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替方塊圖命名、存檔 | |

## 課前準備（約 15 分鐘）

- 電腦或平板，用瀏覽器開 `animations/atoms.html#ionsys`（不需要網路、伺服器或帳號）。
- 列印 `02_列印包_離子阱全景.pdf`（A4，共 4 頁），把第 1 頁的 12 張寶物卡剪開、洗牌。
- 色筆至少四色：紫（光）、紅或橘（射頻／直流）、青（資料）、藍（冷卻水）。
- 讀一遍 `04_解答.md`。

## 誠實說明

- 動畫的設備數量、位置與用電數字是**代表值或示意**，實際依系統而異；動畫插圖寫明「示意」。
- 離子阱「不需要稀釋冷凍機」不等於「完全不需要低溫」：部分系統把阱放進 4–20 K 的低溫恆溫器，讓真空更好、電極雜訊更低。
- 動畫沒有視角按鈕；可用滑鼠拖曳旋轉、滾輪縮放，按 `R` 回到原本的視角。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：尋寶（約 40 分鐘）

1. 開 `animations/atoms.html#ionsys`（場景 1「離子阱量子電腦：系統全景」）。左邊面板下方有四個按鈕：「全部」「只看雷射」「只看電子訊號」「只看設施」。
2. 爸爸（藏寶人）抽一張寶物卡唸出名稱；孩子（尋寶員）在畫面上找到它的標籤，用手指出來。
3. 說出它的工作（卡片背面或列印包第 2 頁可以對答案），再按卡片上寫的分類按鈕，追出它的連線接到哪裡。
4. 在尋寶紀錄表（列印包第 2 頁）填：在哪裡找到、屬於哪個子系統、連到哪裡。
5. 每找到一件，就在方塊圖底稿（列印包第 3 頁）畫一個方塊；光用紫色箭頭、電訊號用紅／橘／青、冷卻水用藍色。
6. 12 張找齊後，挑戰加分寶物（399 nm 雷射、離子泵、銣鐘、恆溫空調、UPS）。

## 下半場：比較兩種機房（約 30 分鐘）

1. 再開 `animations/peripherals.html#overview`（超導量子電腦機房全景），按「只看冷卻相關」，看右下的用電圖。
2. 回到 `atoms.html#ionsys` 按「只看設施」，看右下的用電示意圖。
3. 填列印包第 4 頁的比較表：機房中間的主角、最吃電的負載、停電後要多久恢復。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 寶物卡\n\n| # | 寶物 | 動畫標籤 | 位置提示 | 看連線的按鈕 | 子系統 | 工作 |\n|---|---|---|---|---|---|---|\n'
  + ''.join(f'| {i} | {n} | {lb} | {pos} | {btn} | {sub} | {job} |\n' for i, (n, lb, pos, btn, sub, job) in enumerate(TREASURES, 1))
  + '\n加分寶物：' + '；'.join(f'{n}（{j}）' for n, j in BONUS) + '\n\n'
  + '## 設施比較表\n\n| 項目 | 超導 | 離子阱 |\n|---|---|---|\n' + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in COMPARE)
  + '\n## 常見問題\n\n'
  '- 一輪流程是什麼？冷卻 → 初始化 → 量子閘（雷射或微波）→ 偵測螢光。\n'
  '- 怎麼讀出 0 或 1？偵測光只讓其中一種狀態的離子一直發光；物鏡收光送到 PMT 或相機，光子多判 1、幾乎沒有判 0（細節見 Q068）。\n'
  '- 為什麼要恆溫 ±0.1 °C？溫度漂移會讓光路和雷射頻率漂移，閘和讀取都會變差。\n'
  '- 常見誤解：「量子電腦都要稀釋冷凍機」——離子阱不需要，但需要超高真空與多道穩頻雷射。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## atoms.html#ionsys（離子阱與中性原子 場景 1「離子阱量子電腦：系統全景」）

- 光學桌：左邊四台雷射（369／935／399／355 nm）→ AOM → 光纖；右半邊是超高真空腔，被三對銅色磁場線圈圍住，上方是成像物鏡，後方是微波號角，右邊是螺旋共振器。
- 後排機櫃：控制電腦、FPGA 時序控制、銣鐘 10 MHz、AOM 驅動 DDS、多通道 DAC、RF 源 + 放大器、微波合成器。
- 右邊設施：UPS / 配電盤、冷卻水機（雷射散熱）、恆溫空調（±0.1 °C）。
- 左邊面板：「全部」「只看雷射」「只看電子訊號」「只看設施」；說明框跟著換。右下小圖：典型用電（示意）。
- 操作：滑鼠拖曳旋轉、滾輪縮放、`R` 重設視角、`H` 隱藏面板、空白鍵暫停；左右方向鍵換場景（下一堂用場景 3「離子量子位元」）。

## peripherals.html#overview（超導量子電腦周邊 場景 1「量子電腦機房全景」）

- 中央是稀釋冷凍機（量子晶片在 10 mK）；按「只看冷卻相關」只留脈衝管氦氣、冷卻水、混合氣循環、真空；右下用電圖合計約 26 kW（示意）。
''',
}

SHEET_HEADER = ['編號', '寶物', '動畫標籤', '位置提示', '看連線的按鈕', '子系統', '它的工作', '找到了嗎', '連到哪裡（自己填）']
SHEET_ROWS = ([[str(i), n, lb, pos, btn, sub, job, '', ''] for i, (n, lb, pos, btn, sub, job) in enumerate(TREASURES, 1)]
              + [[f'加分{i}', n, '', '', '', '', j, '', ''] for i, (n, j) in enumerate(BONUS, 1)])

EXTRA_CSS = '''.tcards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin-top:3mm}
.tcard{border:1.2pt dashed #7f9bb3;border-radius:3mm;height:40mm;padding:3mm;display:flex;flex-direction:column;justify-content:space-between}
.tcard b{font-size:14pt}.tcard .n{font-size:10pt;color:#4a6a88}.tcard .h{font-size:10pt;color:#4a6a88}
table.rec td{height:12mm;font-size:10.5pt}table.rec{font-size:10.5pt}
table.cmp td{height:17mm;font-size:11pt}
.chk li{margin:2mm 0;font-size:12pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.draw{border:1pt dashed #7f9bb3;border-radius:3mm;height:178mm;margin-top:3mm;position:relative}
.draw span{position:absolute;left:3mm;top:2mm;font-size:10pt;color:#4a6a88}
.legend{font-size:10.5pt;margin-top:2mm}'''


def html():
    cards = ''.join(f'<div class="tcard"><span class="n">寶物 {i}</span><b>{n}</b><span class="h">提示：{pos}</span></div>'
                    for i, (n, lb, pos, btn, sub, job) in enumerate(TREASURES, 1))
    rows = ''.join(f'<tr><td>{i}</td><td>{n}</td><td>□</td><td></td><td></td></tr>' for i, (n, *_r) in enumerate(TREASURES, 1))
    cmp_rows = ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, _b, _c in COMPARE[:3] + COMPARE[4:])
    pages = [
        '<h2>寶物卡：離子阱尋寶</h2><p class="lead">爸爸是藏寶人：剪開、洗牌，一次抽一張。你是尋寶員：在 atoms.html#ionsys 找到它、說出它的工作。</p>'
        '<div class="tcards">' + cards + '</div>',
        '<h2>尋寶紀錄表</h2><p class="lead">找到一件就打勾，寫下它屬於哪個子系統、用分類按鈕追出它連到哪裡。</p>'
        '<table class="rec"><tr><th>#</th><th>寶物</th><th>找到</th><th>子系統（真空／雷射／電子／成像／設施）</th><th>連到哪裡</th></tr>' + rows + '</table>'
        '<p class="note">加分寶物：399 nm 雷射、離子泵 + NEG、銣鐘 10 MHz、恆溫空調、UPS。</p>',
        '<h2>系統方塊圖底稿</h2><p class="lead">真空腔畫在中間，其他設備畫成方塊，用箭頭連起來。</p>'
        '<p class="legend">箭頭顏色：紫＝光（雷射）　紅＝射頻　橘＝直流　青＝資料／光子計數　藍＝冷卻水　黃＝電力</p>'
        '<div class="draw"><span>作品名稱：＿＿＿＿＿＿＿＿＿＿　（先畫真空腔，再一件一件加上去）</span></div>',
        '<h2>設施比較表與最後一關</h2><p class="lead">比較離子阱和超導量子電腦的機房（可對照 peripherals.html#overview）。</p>'
        '<table class="rec cmp"><tr><th>項目</th><th>超導</th><th>離子阱</th></tr>' + cmp_rows + '</table>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出離子阱的子系統：真空與阱、雷射、成像、電子、控制、設施</li>'
        '<li>說出一輪流程：冷卻 → 初始化 → 量子閘 → 偵測螢光</li>'
        '<li>說出怎麼讀出 0 或 1：看離子亮不亮、數光子</li>'
        '<li>指出一個誤解：離子阱不需要稀釋冷凍，但需要超高真空與多道穩頻雷射</li>'
        '<li>替系統方塊圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q067 離子阱全景 列印包', '父子科技學院 量子電腦學程 Q067｜離子阱系統全景', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q067-ion-trap-system', folder='Q067_離子阱系統全景', files=FILES,
        sheet=('03_寶物清單.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_離子阱全景.pdf', pack_pages=4,
        pack_needles=('寶物卡', '尋寶紀錄表', '系統方塊圖底稿', '設施比較表', '最後一關'),
        authoring_dir=XINEW / 'authoring/q067', episode_dir='specials/q067-ion-trap-system',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（瀏覽器開啟動畫）',
               'animation': 'animations/atoms.html#ionsys', 'compareAnimation': 'animations/peripherals.html#overview',
               'treasures': len(TREASURES), 'bonusTreasures': len(BONUS),
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q067/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

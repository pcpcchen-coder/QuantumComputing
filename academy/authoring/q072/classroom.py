"""Q072 課堂教材：磁光阱與光鑷 — 動畫操作步驟、吹風機乒乓球實驗紀錄、光鑷原理圖、SLM／AOD 對照、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/atoms.html（#atomsys、#tweezer），用瀏覽器開啟；實驗另備吹風機、乒乓球、吸管。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q072/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 簡報第 24 頁的代表值
V_ROOM, V_MOT = 300, 0.1               # m/s
SLOWDOWN = round(V_ROOM / V_MOT)       # 3000
assert SLOWDOWN == 3000
STAGES = [('原子源', '室溫 Rb 蒸氣'), ('2D MOT', '冷原子束'), ('3D MOT', '~100 μK 原子雲'),
          ('偏振梯度冷卻', '~10 μK'), ('裝進光鑷', '單顆原子')]
# 簡報第 25 頁 SLM／AOD 對照
SLM_AOD = [('作用', '在相位上「畫」出整個光鑷圖案', 'RF 頻率 → 光的偏折角度'),
           ('陣列', '任意 2D 圖案，上千～上萬點', '多音 RF → 一列／一欄光鑷'),
           ('速度', '慢（~10 ms 換圖）', '快（μs 級），可平滑移動'),
           ('用途', '靜態陣列（儲存）', '搬運原子、重排、分區架構')]
# 08_tweezer.js 預設：目標 6×6、光鑷 10×10、裝載機率 0.5
TRIALS = 5

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q072：磁光阱與光鑷（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：室溫下亂飛的原子，怎麼先冷下來，再一顆一顆抓住？

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `atoms.html#atomsys` 和 `atoms.html#tweezer`。不需要網路、帳號或安裝。
實驗器材：吹風機（要有冷風檔）、乒乓球、吸管。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 系統全景、磁光阱四步、光鑷原理、碰撞阻斷 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 吹風機乒乓球實驗；在動畫裡對照光路、裝載光鑷 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 解釋 SLM 與 AOD，畫光鑷原理圖 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：磁光阱和光鑷怎麼抓原子 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#atomsys` 按「只看雷射」、「視角：真空腔特寫」，找到 MOT 線圈、冷卻光和光鑷光路。
- 在 `#tweezer` 按「① 裝載」→「② 成像」，看讀數的裝載率。
- 先試一次吹風機：開**冷風**、朝上，把乒乓球放進氣流。列印 `02_列印包_磁光阱與光鑷.pdf`（A4，共 4 頁），讀一遍 `04_解答.md`。

## 安全

- 吹風機只用冷風，不要對著臉或眼睛吹；插座和電線遠離水。
- 真實實驗室的雷射功率很高（光鑷雷射常需數十瓦），絕不可用雷射筆照眼睛模仿。

## 誠實說明

- 吹風機和乒乓球只是類比：抓住球的是氣流，抓住原子的是光學偶極力；兩者的物理原理不同。
- 溫度、速度、光鑷深度都是簡報的代表值，依系統而異。
- 動畫的裝載是隨機的，每次結果不同。
- 本課最重要的誤解：光鑷不是把原子「夾住」，而是用光學偶極力把原子吸到光最強處。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 吹風機抓乒乓球（約 15 分鐘）

1. 爸爸拿吹風機，開冷風、朝上吹；把乒乓球輕輕放進氣流，看它浮在半空中。
2. 孩子用吸管對著球的側邊輕輕吹，或用手指輕推，觀察球偏出去後會不會回到氣流中間。
3. 改變吹風機的風量檔位，記下球的高度怎麼變，寫在列印包第 1 頁。
4. 討論：氣流扮演什麼？在光鑷裡，扮演「氣流」的是哪一道光？

## B. 對照光路（`atoms.html#atomsys`，約 10 分鐘）

1. 按「只看雷射」：找出光鑷雷射 → SLM → 2D AOD → 二向色鏡 → 高 NA 物鏡 → 玻璃真空腔。
2. 按「視角：真空腔特寫」：找到 MOT 線圈與穿過中央的冷卻光。
3. 再按「只看電子訊號」：看多音 RF AWG 驅動 AOD 的橘色流線。把看到的元件寫在列印包第 1 頁。

## C. 裝載光鑷（`atoms.html#tweezer`，約 15 分鐘）

1. 按「全部重來」→「① 裝載」→「② 成像」，記下讀數的原子數與裝載率。重複五次，記在列印包第 2 頁。
2. 把「裝載機率 p」拉到 70%，再做兩次，比一比。
3. （預告下一堂）按「③ 重排」，看洋紅色的移動光鑷怎麼搬原子。

## D. 下半場：SLM 與 AOD、畫原理圖（約 30 分鐘）

用列印包第 3 頁，先填 SLM／AOD 對照表，再畫光鑷原理圖：雷射從哪裡出發、經過哪些元件、原子為什麼被抓住。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 從原子氣體到單顆原子（簡報第 24 頁）\n\n'
  + ''.join(f'{i}. {a}：{b}\n' for i, (a, b) in enumerate(STAGES, 1))
  + f'\n- 室溫原子約 {V_ROOM} m/s，MOT 中約 {V_MOT} m/s：慢了約 {SLOWDOWN} 倍。\n'
  '- 溫度 ~100 μK（MOT）→ ~10 μK（偏振梯度冷卻）；光鑷深度 ~1 mK，比原子的能量深很多，所以抓得住。\n'
  '- 冷卻只在每輪開始做一次，之後原子留在光鑷裡做計算。\n\n'
  '## 磁光阱怎麼運作\n\n- 6 道紅失諧 780 nm 雷射從三軸對打：迎面而來的原子較容易吸光而被減速（Doppler 冷卻，「光學糖漿」）。\n'
  '- 反亥姆霍茲線圈：中心磁場為零、往外線性增加；配合圓偏振，離中心越遠被推回的力越大。\n- 數秒內收集 10⁶–10⁸ 顆原子。\n\n'
  '## 光鑷\n\n- 紅失諧雷射 → 原子被拉向光最強處（光學偶極力）；高 NA 物鏡聚焦到 ~1 μm → 三維位井，深度 ~1 mK；遠失諧 → 幾乎不散射光子。\n'
  '- 碰撞阻斷：兩顆原子在同一支光鑷會在光照下碰撞、一起被踢出 → 每格 0 或 1 顆，約 50 %。\n\n'
  '## SLM 與 AOD（簡報第 25 頁）\n\n| | SLM（空間光調變器） | AOD（聲光偏轉器） |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in SLM_AOD)
  + '\n一台光鑷系統 = SLM 做「停車格」＋ AOD 做「搬運車」；光鑷雷射常需數十瓦。\n\n'
  '## 動畫裝載（#tweezer 預設）\n\n10×10 = 100 支光鑷、裝載機率 50 %：每次大約 50 顆上下，每次都不同。p 拉到 70 % 時大約 70 顆上下。\n\n'
  '## 常見問題\n\n- 光鑷是「夾住」原子嗎？不是，是光學偶極力把原子吸到光最強處。\n'
  '- 為什麼不能每格都裝一顆？光鑷太小，兩顆會碰撞一起被踢出，所以只能隨機約一半。\n'
  '- 吹風機實驗和光鑷一樣嗎？只是類比：都是「偏離中心會被拉回」，但一個靠氣流、一個靠光。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `atoms.html#atomsys`（原子場景 7：中性原子系統全景）

- 單選：全部、只看雷射、只看電子訊號、只看設施。
- 視角：全景、真空腔特寫、機櫃側。
- 光學桌：Rb 原子源＋2D MOT → 玻璃真空腔；MOT 線圈與 780 nm 冷卻光；光鑷雷射 852/1064 nm → SLM → 2D AOD → 二向色鏡 → 高 NA 物鏡；芮德堡雷射、相機、FPGA、AWG。

## `atoms.html#tweezer`（原子場景 8：光鑷裝載與重排）

- 按鈕：① 裝載、② 成像、③ 重排、全部重來。
- 滑桿：陣列大小（目標 T×T，預設 6×6，光鑷 10×10）、裝載機率 p（40–70 %，預設 50 %）。
- 紅色雲＝MOT 原子雲；青色小球＝原子；金框＝目標區；紅圈＝成像後的空位；洋紅色＝AOD 移動光鑷。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '設定', '觀察 1', '觀察 2', '備註']
SHEET_ROWS = ([['吹風機實驗', f'風量第 {i} 檔', '', '', ''] for i in (1, 2)]
              + [['吸管側吹', '', '', '', '']]
              + [[f'裝載第 {i} 次', 'p = 50 %', '', '', ''] for i in range(1, TRIALS + 1)]
              + [[f'裝載第 {i} 次', 'p = 70 %', '', '', ''] for i in (1, 2)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}.draw{height:70mm;border:1pt dashed #888;border-radius:3mm}'''


def html():
    pages = [
        '<h2>實驗：吹風機抓乒乓球</h2><p class="lead">冷風、朝上吹，把乒乓球放進氣流。用吸管從側邊輕輕吹，看球會不會回到中間。</p>'
        '<table class="rec"><tr><th>做了什麼</th><th>球怎麼動</th><th>有沒有回到中間</th></tr>'
        '<tr><td>風量第 1 檔</td><td></td><td></td></tr><tr><td>風量第 2 檔</td><td></td><td></td></tr>'
        '<tr><td>吸管側吹</td><td></td><td></td></tr><tr><td>手指輕推</td><td></td><td></td></tr></table>'
        '<div class="card"><h3>對照光路（atoms.html#atomsys「只看雷射」）</h3><p>光鑷雷射 → ＿＿＿＿ → ＿＿＿＿ → 二向色鏡 → ＿＿＿＿ → 原子</p>'
        '<p>在光鑷裡，扮演「吹風機氣流」的是：＿＿＿＿＿＿＿＿</p><p>不一樣的地方：＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>裝載光鑷：每格零或一顆</h2><p class="lead">atoms.html#tweezer：全部重來 → ① 裝載 → ② 成像，記下讀數。</p>'
        '<table class="rec"><tr><th>次數</th><th>裝載機率 p</th><th>原子數（共 100 支）</th><th>裝載率</th><th>目標區已填滿</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td>50 %</td><td></td><td></td><td>／ 36</td></tr>' for i in range(1, TRIALS + 1))
        + ''.join(f'<tr><td>{i}</td><td>70 %</td><td></td><td></td><td>／ 36</td></tr>' for i in (6, 7)) + '</table>'
        '<p class="note">為什麼每格只有零或一顆？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：SLM 與 AOD</h2><table class="rec"><tr><th></th><th>SLM 空間光調變器</th><th>AOD 聲光偏轉器</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, *_ in SLM_AOD) + '</table>'
        '<div class="card"><h3>光鑷原理圖（今天的作品）</h3><div class="draw"></div>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>'
        '<p class="note">生活技能：用類比實驗理解力場——你還想到哪個「偏了會被拉回來」的例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 磁光阱怎麼把原子冷下來？</p><div class="line"></div>'
        '<p>2. 光鑷怎麼抓住單顆原子？</p><div class="line"></div><p>3. SLM 和 AOD 各負責什麼？</p><div class="line"></div>'
        '<p>4. 一個誤解或限制：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：磁光阱先冷卻，光鑷再聚焦抓住</li><li>說出光學偶極力：原子被拉向光最強處</li>'
        '<li>說出碰撞阻斷：每格零或一顆、約一半</li><li>指出誤解：光鑷不是夾子，是光的力</li>'
        '<li>替光鑷原理圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q072 磁光阱與光鑷 列印包', '父子科技學院 量子電腦學程 Q072｜磁光阱與光鑷', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q072-mot-optical-tweezers', folder='Q072_磁光阱與光鑷', files=FILES,
        sheet=('03_實驗與裝載紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_磁光阱與光鑷.pdf', pack_pages=4,
        pack_needles=('吹風機', '對照光路', '裝載光鑷', 'SLM 與 AOD', '光鑷原理圖', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q072', episode_dir='specials/q072-mot-optical-tweezers',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#atomsys', 'animations/atoms.html#tweezer'],
               'materials': ['吹風機（冷風）', '乒乓球', '吸管'], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q072/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

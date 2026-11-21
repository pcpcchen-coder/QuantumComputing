"""Q040 課堂教材：機房設備清單、七類連線清單、「斷掉會怎樣」卡、說明卡（列印）、解答、power_budget.py、動畫導覽。

不需要帳號，也不需要安裝套件（power_budget.py 只要 Python 3）；動畫用瀏覽器開啟 animations/peripherals.html#overview。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q040/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q040：機房用電小工具。

不用安裝任何套件，只要 Python 3。執行：  python power_budget.py
- 一、典型用電分配：數字和動畫 peripherals.html#overview 右下小圖一樣（js/peripherals/common.js 的 PD.power，「示意，依機型與規模而異」）。
- 二、每一項占幾成，壓縮機加冷卻水占幾成。
- 三、對照：冷凍機最底層（混合腔）的冷卻功率約 19 微瓦（學程簡報 QC_Peripheral_Systems_Talk p7，Krinner et al. 2019 的量測）。
  這是「最底層能帶走多少熱」，不是晶片本身的耗電。
"""

POWER = [  # (設備, kW)
    ('脈衝管壓縮機', 10.7),
    ('冷卻水系統', 10.0),
    ('控制電子機櫃', 3.0),
    ('氣體處理系統（泵）', 1.5),
    ('電腦 / 監控 / 網路', 1.0),
]
MXC_COOLING_W = 19e-6  # 混合腔在 20 mK 的冷卻功率（瓦）

TOTAL = sum(kw for _, kw in POWER)
print('一、典型用電分配（kW，示意）')
for name, kw in POWER:
    print(f'  {name:10s} {kw:5.1f} kW')
print(f'  合計 {TOTAL:.1f} kW（動畫小圖寫「約 {TOTAL:.0f} kW」）')

print()
print('二、每一項占幾成')
SHARE = {name: kw / TOTAL for name, kw in POWER}
for name, s in SHARE.items():
    print(f'  {name:10s} {s * 100:5.1f} %')
COOLING_PAIR = SHARE['脈衝管壓縮機'] + SHARE['冷卻水系統']
print(f'  壓縮機 + 冷卻水：{COOLING_PAIR * 100:.1f} %')

print()
print('三、對照最底層的冷卻功率')
RATIO = TOTAL * 1000 / MXC_COOLING_W
print(f'  機房用電 {TOTAL:.1f} kW ÷ 最底層冷卻功率 {MXC_COOLING_W * 1e6:.0f} 微瓦 ≈ {RATIO:.1e} 倍')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'power_budget.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()

# 製作代理實跑（Python 3）：與旁白、動畫小圖一致
assert f"{R['TOTAL']:.1f}" == '26.2' and f"{R['TOTAL']:.0f}" == '26'
assert f"{R['COOLING_PAIR'] * 100:.0f}" == '79'
assert f"{R['RATIO']:.1e}" == '1.4e+09'

DEVICES = [
    ('稀釋冷凍機（晶片在最底部 10 mK）', '正中間', '低溫系統'),
    ('控制電子機櫃', '冷凍機左邊', '控制電子'),
    ('控制電腦', '左後方', '控制電子／軟體'),
    ('UPS 不斷電', '左前方', '機房設施'),
    ('配電盤', '最左邊', '機房設施'),
    ('溫控器 / 壓力監控', '冷凍機後方', '低溫系統（監控）'),
    ('氣體處理系統 GHS', '冷凍機右後方', '低溫系統'),
    ('混合氣儲存槽', '右後方', '低溫系統'),
    ('液氮冷阱（選配）', '冷凍機後方偏右', '低溫系統'),
    ('脈衝管壓縮機', '冷凍機右前方', '低溫系統'),
    ('冷卻水機', '最右前方', '機房設施'),
    ('使用者 / 雲端', '左上方的雲', '軟體'),
]
LINKS = [
    ('脈衝管氦氣', '綠', '脈衝管壓縮機', '冷凍機頂上的冷頭（高壓、低壓兩條）'),
    ('冷卻水', '藍', '冷卻水機', '脈衝管壓縮機（帶走約 10 kW 熱）'),
    ('混合氣循環', '紫', '氣體處理系統', '冷凍機（抽氣、回流）；也接儲存槽、冷阱'),
    ('真空', '灰', '氣體處理系統的泵', '外真空罩'),
    ('微波 / 直流線', '橘', '控制電子機櫃', '冷凍機頂板的密封接頭'),
    ('資料 / 時脈', '青', '控制電腦', '機櫃、氣體處理系統、溫控器、雲端'),
    ('電力', '黃', '配電盤（經 UPS 或直接）', 'UPS → 機櫃、電腦、GHS；直接 → 壓縮機、冷卻水機'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q040：量子電腦 ≠ 量子晶片（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。上一堂 Q039 我們替讀取電路做取捨；這一堂把鏡頭拉遠到整間機房：
量子晶片鎖在稀釋冷凍機最底部（約 10 mK），只是一小塊；要讓它運作，還需要低溫系統、低溫佈線、控制電子、軟體、機房設施五大子系統，
設備之間用七類連接串起來：脈衝管氦氣、冷卻水、混合氣、真空、微波（與直流線）、資料（與時脈）、電力。
好玩機制是「尋寶」：在 3D 場景裡找出每一台設備、每一類連線。作品是「機房設備清單」。下一堂 Q041 是「為什麼要 10 mK」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 機房全景、冷卻側四類、訊號側與電力、用電、方塊圖；看 3D 動畫 | 影片第 2–8 段、`05_動畫導覽.md` |
| 25–65 | 尋寶：在 peripherals.html#overview 找設備、一類一類切換連接，列出設備與連線清單 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：挑一條連接，說明它斷掉會發生什麼事 | 列印包第 3 頁、`power_budget.py` |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替機房設備清單取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_機房設備清單.pdf`（A4，共 4 頁）。另備彩色筆（七種顏色最好：綠、藍、紫、灰、橘、青、黃）。
- 讀一遍 `04_解答.md`；想多了解可以讀學程文件 `docs/周邊系統連接與啟動指南.md` 的 §1、§3、§6。
- 下載學程的 `animations/` 資料夾，用瀏覽器先開一次 `peripherals.html#overview`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `power_budget.py`（不需要安裝套件）。

## 驗收重點

1. 完成「機房設備清單」：至少十樣設備（名字、在畫面哪裡、屬於哪個子系統），以及七類連線各從哪裡接到哪裡。
2. 不看稿說出核心原理：量子電腦不等於量子晶片；晶片要靠低溫、佈線、控制電子、軟體和機房設施才能運作。
3. 指出至少一個注意事項：晶片只占整台機器很小一部分；周邊系統才是體積與耗電的大宗（動畫小圖：壓縮機加冷卻水約占八成）。

## 誠實說明

- 動畫裡設備的位置、大小、管線走向和用電數字都是示意（小圖寫「依機型與規模而異」）；學程指南的合計寫約 25 kW，動畫小圖約 26 kW。
- 「斷掉會怎樣」照學程指南 §6 的描述，實際反應依機型與控制軟體而異。家裡沒有機房可以試，不要編造實驗結果。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：機房尋寶（約 40 分鐘）

1. 用瀏覽器開 `animations/peripherals.html#overview`，左邊面板往下捲到底，看到三列按鈕：七顆連接按鈕、「全部顯示」「只看冷卻相關」「只看訊號相關」、三個視角按鈕。
2. 尋設備：用列印包第 1 頁，一台一台找出設備，寫下名字、它在畫面的哪裡（中間、左邊、右後方……）、屬於五大子系統的哪一個；找到就打勾。
   找不到時，按「視角：冷凍機頂部」「視角：機櫃側」換角度，或用滑鼠拖曳旋轉、滾輪縮放。
3. 尋連線：用列印包第 2 頁。先按「只看冷卻相關」，再按「只看訊號相關」，看兩大類各有哪幾種顏色；
   再一顆一顆按連接按鈕（按一次關掉、再按一次打開），每一類寫下顏色、從哪一台接到哪一台。
4. 最後按「全部顯示」，把七類連線用彩色筆畫在設備清單旁邊的空白處（或另一張紙上的機房平面圖）。

## 下半場：孩子改造——如果斷掉了（約 30 分鐘）

1. 用列印包第 3 頁：挑一條連接（例如電力、冷卻水、真空），在動畫裡只留下那一類，看它從哪裡接到哪裡。
2. 往下追：它斷掉以後，哪一台設備先停？接著會影響誰？最後晶片會怎樣？
3. 對照 `04_解答.md` 裡學程指南的描述，寫下恢復時要先做什麼。
4. 加分題：執行 `power_budget.py`，看看壓縮機加冷卻水占全部用電的幾成，再和冷凍機最底層的冷卻功率比一比。
''',

'power_budget.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## power_budget.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 機房設備清單參考答案（照 peripherals.html#overview 的標籤；位置以載入時的全景視角描述）\n\n'
  '| 設備 | 在畫面哪裡 | 子系統 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in DEVICES) +
  '\n## 七類連線參考答案（動畫的顏色）\n\n'
  '| 連接 | 顏色 | 從 | 到 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in LINKS) +
  '\n「只看冷卻相關」留下脈衝管氦氣、冷卻水、混合氣循環、真空；「只看訊號相關」留下微波 / DC、資料 / 時脈；電力兩組都不包括。\n\n'
  '## 「斷掉會怎樣」參考答案（學程指南 docs/周邊系統連接與啟動指南.md §6）\n\n'
  '- 停電：壓縮機與冷卻水停止，UPS 維持控制系統；約 10 分鐘後混合液開始沸騰，除必要閥門外全部關閉，混合氣經背壓閥回收至儲存槽。'
  '復電後依序重啟：冷卻水 → 壓縮機 → 氣體處理系統，重新降溫需數小時到 1 天。\n'
  '- 冷卻水中斷／過溫：壓縮機聯鎖停機。恢復水路、檢查冷卻水機後重啟壓縮機。\n'
  '- 真空洩漏：外真空罩（OVC）壓力上升、各級升溫，系統停止循環。用氦質譜檢漏、更換密封，重新抽真空。\n'
  '- 讀取訊號變差（和微波線有關）：依序檢查放大器偏壓、泵浦、室溫連接、衰減值。\n'
  '- 原則：任何異常都要優先確保混合氣（³He）不外洩。\n\n'
  '## 常見問題\n\n'
  '- 晶片那麼小，為什麼機器這麼大？晶片要在約 10 mK 工作，冷凍機、壓縮機、冷卻水、氣體處理系統負責把它降溫並維持；控制電子、軟體負責產生和解讀每一個微波脈衝。\n'
  '- 最耗電的是哪一台？動畫小圖：脈衝管壓縮機 10.7 kW、冷卻水系統 10.0 kW，兩項約占 79 %。\n'
  '- 20 微瓦是晶片的耗電嗎？不是。那是冷凍機最底層（混合腔）在 20 mK 能帶走的熱（簡報 p7），說明低溫端的熱預算非常小。\n'
  '- 為什麼有些設備接 UPS、有些直接接配電盤？UPS 供應控制電子、電腦、氣體處理系統的控制器與閥門、溫控器、網路這些關鍵負載；'
  '壓縮機、冷卻水機這類大功率設備直接由配電盤供電（動畫說明與學程指南 §2）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。
左邊面板很長，按鈕在下方，要往下捲。

## `peripherals.html#overview`（周邊系統 3D 場景 1：量子電腦機房全景：設備與連接）

- 中間：稀釋冷凍機（金色標籤「量子晶片在 10 mK」）。左邊：控制電子機櫃、控制電腦、UPS 不斷電、配電盤，左上方的雲是使用者 / 雲端 API。
  右邊：氣體處理系統 GHS、混合氣儲存槽、液氮冷阱（選配）、脈衝管壓縮機、冷卻水機；冷凍機後方是溫控器 / 壓力監控。
- 七類連接：細管裡的彩色小點一直在流動。綠＝脈衝管氦氣、藍＝冷卻水、紫＝混合氣循環、灰＝真空、橘＝微波 / DC、青＝資料 / 時脈、黃＝電力。
- 控制：七顆連接按鈕（按一次關掉、再按一次打開）；「全部顯示」「只看冷卻相關」「只看訊號相關」；「視角：全景」「視角：冷凍機頂部」「視角：機櫃側」。
  滑鼠可以拖曳旋轉、滾輪縮放；空白鍵暫停。
- 右下角小圖：典型用電分配（kW，示意），由上到下是脈衝管壓縮機 10.7、冷卻水系統 10.0、控制電子機櫃 3.0、氣體處理系統（泵）1.5、電腦 / 監控 / 網路 1.0，合計約 26 kW。
- 同一頁上方還有其他 9 個場景（脈衝管、稀釋原理、降溫、佈線、電子學、軟體、機房設施、監控、上線），之後的課會用到。

## 之後的課

Q041「為什麼要 10 mK」會用量子位元的能量和溫度比一比，說明晶片為什麼要那麼冷。
''',
}

SHEET_HEADER = ['設備', '在畫面哪裡', '屬於哪個子系統', '找到了']
SHEET_ROWS = [[] for _ in range(12)]

EXTRA_CSS = '''table.dev td{height:12.2mm;font-size:11pt}table.dev th{font-size:10.5pt;white-space:nowrap}
table.lnk td{height:19mm;font-size:11pt;vertical-align:top}table.lnk th{font-size:10.5pt;white-space:nowrap}table.lnk td:first-child{white-space:nowrap}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.calc p{margin:2.4mm 0;font-size:12pt}'''


def html():
    dev_rows = ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 13))
    lnk_rows = ''.join(f'<tr><td>{name}</td><td></td><td></td><td></td></tr>' for name, *_ in LINKS)
    pages = [
        '<h2>機房設備清單（尋寶卡）</h2><p class="lead">打開 peripherals.html#overview，一台一台找出設備，寫下名字、位置和子系統。</p>'
        '<table class="dev"><tr><th style="width:6%">#</th><th style="width:32%">設備名字</th><th style="width:22%">在畫面哪裡</th>'
        '<th>屬於哪個子系統</th><th style="width:9%">找到了</th></tr>' + dev_rows + '</table>'
        '<p style="font-size:10.5pt;margin-top:2.5mm">五大子系統：低溫系統、低溫佈線、控制電子、軟體、機房設施。找不到就換視角或旋轉、縮放。</p>',
        '<h2>七類連線清單</h2><p class="lead">一顆一顆按連接按鈕，看哪一類不見了；寫下顏色、從哪一台接到哪一台。</p>'
        '<table class="lnk"><tr><th style="width:20%">連接</th><th style="width:12%">顏色</th><th style="width:30%">從哪一台</th><th>接到哪一台</th></tr>'
        + lnk_rows + '</table>'
        '<p style="font-size:10.5pt;margin-top:2.5mm">按「只看冷卻相關」留下哪幾類？＿＿＿＿＿＿＿＿　按「只看訊號相關」留下哪幾類？＿＿＿＿＿＿＿＿</p>',
        '<h2>「斷掉會怎樣」卡</h2><p class="lead">挑一條連接，在動畫裡只留下它，再往下追：誰先停？接著影響誰？晶片會怎樣？</p>'
        '<div class="box calc"><h3>一、我挑的連接</h3><p>連接：＿＿＿＿＿＿　顏色：＿＿＿＿　從＿＿＿＿＿＿接到＿＿＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>二、往下追</h3><p>① 先停下來的是：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>② 接著會影響：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p><p>③ 最後晶片會：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>三、恢復的順序</h3><p>第一步：＿＿＿＿＿＿　第二步：＿＿＿＿＿＿　第三步：＿＿＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>四、加分題：用電</h3><p>動畫小圖的合計約＿＿＿＿ kW；壓縮機加冷卻水約占＿＿＿＿成。</p>'
        '<p>冷凍機最底層的冷卻功率約＿＿＿＿微瓦；它是晶片的耗電嗎？＿＿＿＿</p></div>',
        '<h2>說明卡：我的機房設備清單</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 量子電腦 ≠ 量子晶片在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出為什麼量子電腦不等於量子晶片</li><li>說出七類連接，各從哪裡接到哪裡</li>'
        '<li>說出晶片只占很小一部分，周邊才是體積與耗電大宗</li><li>說出一條連接斷掉會怎樣</li>'
        '<li>示範一次：在動畫裡只看冷卻相關、只看訊號相關</li><li>替機房設備清單取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q040 機房設備清單 列印包', '父子科技學院 量子電腦學程 Q040｜量子電腦 ≠ 量子晶片', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q040-whole-machine', folder='Q040_量子電腦不等於量子晶片', files=FILES,
        sheet=('03_機房設備清單.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_機房設備清單.pdf', pack_pages=4,
        pack_needles=('機房設備清單', '七類連線清單', '斷掉會怎樣', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q040', episode_dir='specials/q040-whole-machine',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（power_budget.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'power_budget.py',
               'recordedRun': {'total_kW': round(R['TOTAL'], 1),
                               'shares_percent': {k: round(v * 100, 1) for k, v in R['SHARE'].items()},
                               'compressor_plus_cooling_water_percent': round(R['COOLING_PAIR'] * 100, 1),
                               'total_over_mxc_cooling': float(f"{R['RATIO']:.2g}")},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q040/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q047 課堂教材：故障注入紀錄表、異常處置卡（量子電腦版與家用版）、軟體堆疊連連看、可執行的 fault_sim.py
（照監控場景的故障模型逐秒印出數值與聯鎖判斷）、說明卡與解答。

不需要帳號、不需要安裝套件（fault_sim.py 只用 Python 標準函式庫）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q047/classroom.py
"""
from pathlib import Path
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = '''"""父子科技學院 量子電腦學程 Q047：故障注入模擬器（照 peripherals.html#monitor 的示意模型）

執行：python fault_sim.py water     冷卻水中斷
      python fault_sim.py leak      真空洩漏
      python fault_sim.py block     流阻堵塞
不需要安裝任何套件。時間是「動畫秒數」（場景標示時間加速），不是真實冷凍機的時間。
改造：改 ALARM_WATER、STOP_WATER 這些門檻，看看警報和聯鎖提早或延後多少。
"""
import math
import sys

ALARM_WATER = 27.0    # 冷卻水入水溫度超過這個值：警報（°C）
STOP_WATER = 32.0     # 到這個值：聯鎖停壓縮機（°C）
ALARM_OVC = 1e-3      # 外真空（OVC）壓力超過這個值：警報（mbar）
ALARM_FLOW = 0.2      # ³He 流量低於這個值：警報（mmol/s）


def step(fault, t):
    water, ovc, flow, cond, comp_on = 18.0, 1e-5, 0.5, 500.0, True
    status, action = 'OK', '—'
    if fault == 'water':
        water = 18 + min(30, t * 2.2)
        comp_on = water < STOP_WATER
        status = '警報' if water > ALARM_WATER else '警告'
        action = '冷卻水溫上升' if comp_on else '聯鎖停止壓縮機；準備回收混合氣'
    elif fault == 'leak':
        ovc = 1e-5 * math.exp(min(t, 20) * 0.6)
        status = '警報' if ovc > ALARM_OVC else '警告'
        action = '停止循環、檢漏' if ovc > ALARM_OVC else 'OVC 壓力上升'
    elif fault == 'block':
        flow = 0.5 * math.exp(-t / 3)
        cond = 500 + min(600, t * 60)
        status = '警報' if flow < ALARM_FLOW else '警告'
        action = '多為雜質凍結；回收混合氣、清理冷阱' if flow < ALARM_FLOW else '流量下降'
    return water, ovc, flow, cond, comp_on, status, action


fault = sys.argv[1] if len(sys.argv) > 1 else 'water'
print(f'故障情境：{fault}')
print(' 秒  水溫°C   OVC(mbar)  流量  凝結壓力  壓縮機  狀態  動作')
for t in range(0, 13):
    w, o, f, c, on, s, a = step(fault, t)
    print(f'{t:3d}  {w:5.1f}  {o:9.1e}  {f:4.2f}  {c:6.0f}    {"運轉" if on else "停止"}   {s}  {a}')
'''

# 與影片、fact-check.md 一致（09_monitor.js 的模型）
T_WATER_ALARM = (27 - 18) / 2.2
T_WATER_STOP = (32 - 18) / 2.2
T_LEAK_ALARM = math.log(100) / 0.6
T_BLOCK_ALARM = -3 * math.log(0.4)
assert (round(T_WATER_ALARM, 2), round(T_WATER_STOP, 2), round(T_LEAK_ALARM, 2), round(T_BLOCK_ALARM, 2)) == (4.09, 6.36, 7.68, 2.75)
_ns = {}
exec(compile(PROGRAM.split("fault = sys.argv")[0], 'fault_sim', 'exec'), _ns)
assert _ns['step']('water', 4)[5] == '警告' and _ns['step']('water', 5)[5] == '警報'
assert _ns['step']('water', 6)[4] is True and _ns['step']('water', 7)[4] is False
assert _ns['step']('leak', 7)[5] == '警告' and _ns['step']('leak', 8)[5] == '警報'
assert _ns['step']('block', 2)[5] == '警告' and _ns['step']('block', 3)[5] == '警報'

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q047：軟體、監控與聯鎖（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：認識軟體堆疊與校準資料庫，分清「告警」和「聯鎖」，再用「故障注入」在監控場景製造三種故障，寫出異常處置卡。

## 需要什麼

- 一台電腦和瀏覽器：打開學程 `animations/peripherals.html#software`（周邊系統 3D 場景 7「軟體堆疊」）和 `animations/peripherals.html#monitor`（場景 9「監控與聯鎖」）。不需要帳號。
- 可選：用 Python 執行 `fault_sim.py`（不需要安裝套件），逐秒印出故障數值。
- 列印 `02_列印包_軟體監控與聯鎖.pdf`（A4，共 4 頁）；紅筆、綠筆。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 軟體堆疊、校準資料庫、告警與聯鎖、監控的三大類數字 | 影片、列印包第 1 頁 |
| 25–65 | 故障注入：冷卻水中斷、真空洩漏、流阻堵塞，各記錄徵兆、自動動作、人工處置 | `01_操作步驟.md`、列印包第 2 頁、`03_故障注入紀錄表.csv` |
| 65–75 | 休息 | |
| 75–105 | 替家裡的冰箱或熱水器寫異常處置卡 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：軟體堆疊、告警與聯鎖、人先安全 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 故障注入的規則

- 一次只注入一種故障；按下前先預測「會先看到什麼徵兆」。
- 每種故障都分三欄寫：徵兆（看到什麼數字變化）、自動動作（系統自己做了什麼）、人工處置（人要接著做什麼）。
- 做完一種先按「正常運轉」回到原狀，再試下一種。

## 安全提醒（今天的重點）

- 聯鎖會自動保護設備，但它只會「停下來」，不會找原因、不會修。
- 處置卡第一行永遠是「人先安全」：先確認人員安全，再處理機器。
- 家用設備有怪味、冒煙、漏水或漏電疑慮時：孩子一律先離遠、找大人，不要自己拆、不要碰電源線。

## 誠實說明

- 監控場景的升溫、壓力、流量曲線是教學示意模型（插圖標「時間加速」），27 °C 警報、32 °C 停壓縮機是場景程式的門檻；實際門檻與反應以設備手冊為準。
- 簡報第 28 頁註明：停電的反應依 Bluefors LD 使用手冊，其餘是典型經驗。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場暖身：軟體堆疊（約 5 分鐘）

1. 打開 `animations/peripherals.html#software`。中間五層由上往下：使用者程式／雲端 API、編譯器、脈衝層、控制韌體／序列器、硬體。
2. 把滑桿「播放速度」調到 0.5，看白色方塊往下時標籤怎麼變，綠色球往上時又怎麼變；寫在列印包第 1 頁。
3. 找到右邊金色圓柱「校準資料庫」和「自動校準服務」；左邊讀數寫著哪些參數會漂移？

## 故障注入（約 35 分鐘）

1. 打開 `animations/peripherals.html#monitor`。左邊面板有四個按鈕：正常運轉、冷卻水中斷、真空洩漏、流阻堵塞。右下角是監控曲線（最近 60 秒，時間加速）。
2. 按「冷卻水中斷」。看讀數「冷卻水入水」幾度時狀態從 WARN 變 ALARM？幾度時壓縮機變「停止」？紫色的點把混合氣送到哪裡？
3. 按「正常運轉」回原狀；再按「真空洩漏」。看「OVC」壓力怎麼變、哪一層的溫度計小球先變色、面板動作寫什麼。
4. 按「正常運轉」；再按「流阻堵塞」。看「³He 流量」和「凝結壓力」往哪個方向變、面板動作寫什麼。
5. 三種都寫進列印包第 2 頁（或 `03_故障注入紀錄表.csv`）。
6. 想看逐秒數字：`python fault_sim.py water`（或 `leak`、`block`）。

## 下半場：家用異常處置卡（約 30 分鐘）

1. 挑一台家裡的設備：冰箱或熱水器。
2. 列出兩個可能的異常和徵兆（看到、聽到、聞到什麼）。
3. 照三行格式寫處置：第一行人先安全；第二行看設備自己有沒有保護動作；第三行人要做什麼（例如：找大人、看說明書、打電話給維修）。
4. 寫在列印包第 3 頁下半，貼在設備旁邊。
''',

'fault_sim.py': PROGRAM,

'04_解答.md': f'''# 解答（爸爸用）

## 軟體堆疊連連看

| 層 | 往下時的樣子 | 往上時的樣子 |
|---|---|---|
| 使用者程式／雲端 API | 量子電路（H、CNOT…） | 結果回到使用者 |
| 編譯器 | 原生閘＋實體量子位元 | 直方圖／期望值 |
| 脈衝層 | 脈衝序列（含時間表） | 位元串 |
| 控制韌體／序列器 | 波形＋指令 | 0／1 位元串 |
| 硬體 | 微波脈衝 | IQ 原始資料 |

（場景 `07_software.js` 的標籤；方塊在兩層之間時標籤會提早或延後一點換，順序才是重點。）

校準資料庫存：頻率、脈衝振幅、DRAG 修正係數、讀取參數（閾值等）。參數會漂移，所以每日或每週自動重校；單顆量子位元幾十分鐘、整顆處理器數小時（簡報第 26 頁）。

## 告警和聯鎖

- 告警：通知人（亮燈、簡訊、郵件）。聯鎖：條件超過門檻，自動讓設備進入安全狀態（例如冷卻水過溫 → 壓縮機停機）。
- 生活例子：微波爐門一打開就切斷產生微波的電源。

## 故障注入紀錄（監控場景模型；時間是動畫秒數）

| 故障 | 徵兆 | 自動動作 | 人工處置 |
|---|---|---|---|
| 冷卻水中斷 | 入水溫度從 18 °C 每秒升 2.2 °C；約 {T_WATER_ALARM:.1f} 秒超過 27 °C 變 ALARM | 約 {T_WATER_STOP:.1f} 秒到 32 °C，聯鎖停壓縮機；混合氣送回儲存槽；之後各層升溫 | 恢復水路、檢查冷卻水機，再重啟壓縮機 |
| 真空洩漏 | OVC 壓力從 1.0e-5 mbar 指數上升；混合腔、冷板的小球最先變色；約 {T_LEAK_ALARM:.1f} 秒超過 1e-3 mbar 變 ALARM | 告警、停止循環 | 用氦質譜檢漏儀找漏點、換密封、重新抽真空 |
| 流阻堵塞 | ³He 流量從 0.50 往下掉、凝結壓力從 500 mbar 往上升；約 {T_BLOCK_ALARM:.1f} 秒流量低於 0.2 變 ALARM | 告警 | 回收混合氣、清理冷阱；必要時升溫到約 4 K 以上 |

注意：網頁實際播放時，動畫秒數可能比真實秒數慢（電腦越忙越慢），所以用碼錶量到的秒數會比表上大。

## 常見問題

- 有聯鎖為什麼還要人？聯鎖只會停機保護設備，不會找原因、不會修；而且人員安全要先確認。
- 為什麼一出事就先回收混合氣？氦三很貴，冷凍機把它放在封閉系統裡；指南的原則是任何異常都優先確保混合氣不外洩。
- 三種故障怎麼分？看哪個數字先動：水溫（冷卻水）、外真空壓力（真空洩漏）、³He 流量與凝結壓力（流阻堵塞）。
''',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要伺服器或帳號。

## `animations/peripherals.html#software`（周邊系統 3D 場景 7：軟體堆疊）

- 五層板子：使用者程式／雲端 API、編譯器、脈衝層、控制韌體／序列器、硬體；右邊有工作佇列、校準資料庫、自動校準服務，左下有監控／日誌。
- 白色方塊往下（編譯與下傳），綠色球往上（量測結果回傳），旁邊標籤顯示每一層的樣子。
- 滑桿「播放速度」0.3–2 倍。右下插圖「同一個程式在不同層的樣子」：電路與脈衝時間軸並排。

## `animations/peripherals.html#monitor`（周邊系統 3D 場景 9：監控與聯鎖）

- 按鈕「正常運轉」「冷卻水中斷」「真空洩漏」「流阻堵塞」：注入故障，觀察讀數、告警燈、溫度計小球顏色（> 1.3 倍橘、> 3 倍紅）與自動處置。
- 右下插圖「監控曲線（最近 60 秒，時間加速）」：混合腔、冷板、蒸餾器、4 K 的溫度。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；左右方向鍵換場景。
''',
}

SHEET_HEADER = ['故障', '我的預測（會先看到什麼）', '徵兆：哪個數字先變', '狀態何時變 ALARM', '自動動作', '人工處置', '人員安全要注意什麼', '預測對嗎']
SHEET_ROWS = [['冷卻水中斷'], ['真空洩漏'], ['流阻堵塞'], ['（家用）冰箱或熱水器']]

EXTRA_CSS = '''table.rec td{height:11mm}table.big td{height:24mm;font-size:10pt;vertical-align:top}table.big th{font-size:10pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card td:first-child{font-weight:700;width:40mm}.card td{height:12mm}.small{font-size:10pt;color:#4a6a88}'''


def html():
    layers = ['使用者程式／雲端 API', '編譯器', '脈衝層', '控制韌體／序列器', '硬體']
    stack = ''.join(f'<tr><td>{n}</td><td></td><td></td></tr>' for n in layers)
    faults = ''.join(f'<tr><td>{f}</td><td></td><td></td><td></td><td></td></tr>' for f in ('冷卻水中斷', '真空洩漏', '流阻堵塞'))
    pages = [
        '<h2>軟體堆疊連連看</h2><p class="lead">打開 peripherals.html#software，把播放速度調到 0.5，寫下每一層的標籤。</p>'
        f'<table class="rec"><tr><th>層</th><th>白色方塊往下時</th><th>綠色球往上時</th></tr>{stack}</table>'
        '<p>校準資料庫存了哪些參數？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>為什麼要每天或每週重新校準？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<h3 style="margin-top:5mm">告警和聯鎖</h3>'
        '<table class="rec"><tr><th></th><th>做什麼</th><th>舉一個例子</th></tr>'
        '<tr><td>告警</td><td></td><td></td></tr><tr><td>聯鎖</td><td></td><td></td></tr></table>',
        '<h2>故障注入紀錄表</h2><p class="lead">打開 peripherals.html#monitor。一次只注入一種故障，按下前先預測。</p>'
        '<table class="rec big"><tr><th>故障</th><th>徵兆<br>哪個數字先變</th><th>何時變<br>ALARM</th><th>自動動作</th><th>人工處置</th></tr>'
        f'{faults}</table>'
        '<p class="note">冷卻水看「冷卻水入水」；真空洩漏看「OVC」；流阻堵塞看「³He 流量」和「凝結壓力」。右下角監控曲線也要看。</p>'
        '<p>哪一種故障最快變 ALARM？＿＿＿＿＿＿　哪一種會讓壓縮機停機？＿＿＿＿＿＿</p>',
        '<h2>異常處置卡</h2><p class="lead">三行格式：人先安全 → 看機器自己做了什麼 → 人要接著做什麼。</p>'
        '<h3>量子電腦版：冷卻水中斷</h3><table class="rec card">'
        '<tr><td>徵兆</td><td></td></tr><tr><td>① 人先安全</td><td></td></tr>'
        '<tr><td>② 機器自動做了</td><td></td></tr><tr><td>③ 人接著做</td><td></td></tr></table>'
        '<h3 style="margin-top:5mm">家用版：＿＿＿＿＿＿（冰箱或熱水器）</h3><table class="rec card">'
        '<tr><td>可能的異常</td><td></td></tr><tr><td>徵兆</td><td></td></tr><tr><td>① 人先安全</td><td></td></tr>'
        '<tr><td>② 設備的保護</td><td></td></tr><tr><td>③ 人接著做</td><td></td></tr></table>'
        '<p class="small">有怪味、冒煙、漏水：先離遠、找大人，不要自己拆。</p>',
        '<h2>說明卡：我的異常處置卡</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 軟體、監控與聯鎖在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：量子程式經過哪幾層變成微波</li><li>分清告警和聯鎖，各舉一個例子</li>'
        '<li>說出三種故障各看哪個數字</li><li>指出注意事項：聯鎖保護設備但不會修；人先安全，再處理機器</li>'
        '<li>替處置卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q047 軟體、監控與聯鎖 列印包', '父子科技學院 量子電腦學程 Q047｜軟體、監控與聯鎖', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q047-software-monitor', folder='Q047_軟體監控與聯鎖', files=FILES,
        sheet=('03_故障注入紀錄表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_軟體監控與聯鎖.pdf', pack_pages=4,
        pack_needles=('軟體堆疊連連看', '告警和聯鎖', '故障注入紀錄表', '異常處置卡', '人先安全', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q047', episode_dir='specials/q047-software-monitor',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'fault_sim.py', 'model': 'animations/js/peripherals/09_monitor.js',
               'faultAlarmSeconds': {'water': round(T_WATER_ALARM, 2), 'waterCompressorStop': round(T_WATER_STOP, 2),
                                     'leak': round(T_LEAK_ALARM, 2), 'block': round(T_BLOCK_ALARM, 2)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q047/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

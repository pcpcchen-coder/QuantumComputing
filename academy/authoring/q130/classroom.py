"""Q130 課堂教材：斷電時間軸、可執行的備援方案計算 outage_timeline.py、實驗室斷電處置卡、容易錯的地方、教爸爸檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/power1000.html#outage 與 animations/peripherals.html#cooldown、#monitor；程式只要 Python 3。
建置時會真的執行一次 outage_timeline.py，確認輸出和影片、教材寫的數字一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q130/classroom.py
"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，結果固定（無亂數）
RUN_OUTPUT = '''容忍時間 2 分鐘；發電機接手 30 秒
A 只有控制電子接 UPS，市電停 1 分鐘：冷卻鏈停 1 分鐘 → 保住：1 K 以下
A 只有控制電子接 UPS，市電停 5 分鐘：冷卻鏈停 5 分鐘 → 超過 1 K：停機 2–5 天＋完整校準
B 冷卻鏈接 UPS＋發電機，市電停 3 小時：冷卻鏈停 0 分鐘 → 保住：1 K 以下
C 冷卻鏈接 UPS、發電機沒起來，市電停 10 分鐘：冷卻鏈停 0 分鐘 → 保住：1 K 以下
C 冷卻鏈接 UPS、發電機沒起來，市電停 16 分鐘：冷卻鏈停 1 分鐘 → 保住：1 K 以下
C 冷卻鏈接 UPS、發電機沒起來，市電停 60 分鐘：冷卻鏈停 45 分鐘 → 超過 1 K：停機 2–5 天＋完整校準
6 個案例，保住 4 個
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q130：斷電時間軸——不同備援方案，冷卻鏈會停多久？（純 Python，不需要安裝任何套件）

執行：  python outage_timeline.py
時間數字：冷卻中斷約 2 分鐘晶片超過 1 K、重新降溫 2–5 天，取自 LRZ 公開論文（arXiv:2509.12949）；
發電機啟動＋自動切換約 10–30 秒，取自學程文件「量子電腦供電設計文獻回顧」§2 的推論（這裡取保守的 30 秒）。
"""

TOLERANCE_MIN = 2.0     # 冷卻鏈最多能停幾分鐘（約 2 分鐘就超過 1 K）
GEN_START_MIN = 0.5     # 發電機啟動＋自動切換開關（約 10–30 秒，取 30 秒）
RECOOL = '2–5 天'        # 超過 1 K 之後：重新降溫，再完整校準

# 改造區：(案例名稱, 市電停幾分鐘, 冷卻鏈有沒有接 UPS, UPS 撐幾分鐘, 發電機有沒有起來)
CASES = [
    ('A 只有控制電子接 UPS，市電停 1 分鐘', 1, False, 0, False),
    ('A 只有控制電子接 UPS，市電停 5 分鐘', 5, False, 0, False),
    ('B 冷卻鏈接 UPS＋發電機，市電停 3 小時', 180, True, 15, True),
    ('C 冷卻鏈接 UPS、發電機沒起來，市電停 10 分鐘', 10, True, 15, False),
    ('C 冷卻鏈接 UPS、發電機沒起來，市電停 16 分鐘', 16, True, 15, False),
    ('C 冷卻鏈接 UPS、發電機沒起來，市電停 60 分鐘', 60, True, 15, False),
]


def cooling_gap(outage, cool_on_ups, ups, gen_ok):
    """冷卻鏈真正斷電幾分鐘"""
    if not cool_on_ups:
        return outage                      # 冷卻鏈沒有備援：市電停多久，它就停多久
    if gen_ok and ups >= GEN_START_MIN:
        return 0.0                         # UPS 撐到發電機接手：冷卻鏈不停
    return max(0.0, outage - ups)          # 發電機沒起來：UPS 用完後，停到市電回來


if __name__ == '__main__':
    print(f'容忍時間 {TOLERANCE_MIN:g} 分鐘；發電機接手 {GEN_START_MIN * 60:g} 秒')
    kept = 0
    for name, outage, cool, ups, gen in CASES:
        gap = cooling_gap(outage, cool, ups, gen)
        ok = gap <= TOLERANCE_MIN
        kept += ok
        result = '保住：1 K 以下' if ok else f'超過 1 K：停機 {RECOOL}＋完整校準'
        print(f'{name}：冷卻鏈停 {gap:g} 分鐘 → {result}')
    print(f'{len(CASES)} 個案例，保住 {kept} 個')
'''

# 時間軸上要標的點：(時間, 事件, 依據)
TIMELINE = [
    ('0 秒', '市電中斷；UPS 用電池幾乎立刻接手', '維基 Uninterruptible power supply；簡報 p8'),
    ('約 10–30 秒', '備用發電機起動＋自動切換開關（ATS）完成', '學程文件 §2 推論'),
    ('約 2 分鐘', '冷卻鏈若沒有備援：混合腔超過 1 K，校準狀態保不住', 'LRZ arXiv:2509.12949；簡報 p7'),
    ('UPS 用完時', '方案 C（發電機沒起來）：冷卻鏈從這一刻開始停', 'power1000.html#outage 方案 C'),
    ('2–5 天（最壞約 10 天）', '重新降溫；降到 100 mK 以下才開始重新校準', 'LRZ；簡報 p7'),
    ('數週', '真空通常還撐得住（不是硬體損壞）', 'LRZ；簡報 p7'),
]

# 故障注入題目（爸爸出題、孩子判斷）：(題目, 參考答案)
QUIZ = [
    ('pw#outage 方案 A，播放到 2 分鐘：白點在紅線的哪一邊？', '剛好衝過 1 K 紅線；之後要好幾天才降回來，停機約 3–5 天（含重新降溫與完整校準）。'),
    ('切到方案 B：曲線長什麼樣？停機時間？', '整條平貼在 10 mK；停機時間 0（不受影響）。'),
    ('方案 C，UPS 撐 15 分鐘 vs 60 分鐘：曲線哪裡不一樣？', '平的那段一直走到 UPS 用完（15 分或 60 分）才往上衝；只要發電機沒起來、市電沒回來，停機時間都同 A。'),
    ('pe#monitor 按「冷卻水中斷」：電還在，為什麼冷凍機也回溫？', '水溫超限 → 聯鎖停掉壓縮機；壓縮機一停，冷卻鏈就斷了。所以冰水機也是關鍵負載。'),
    ('pe#cooldown：重新降溫最花時間的是哪一段？', '② 脈衝管預冷（動畫示意約一天）；之後還要凝結混合氣、稀釋循環，到基溫才能重新校準。'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q130：斷電的代價——2 分鐘換 2–5 天（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：冷卻鏈一斷電，晶片約 2 分鐘就超過 1 K，接下來要 2–5 天重新降溫與校準；備援要保護的是「冷卻鏈的連續運轉」。課堂用「故障注入」的方式：爸爸在動畫裡製造故障，孩子當值班工程師判斷後果。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `power1000.html#outage`（斷電時間軸）；加映 `peripherals.html#cooldown`（降溫流程）、`peripherals.html#monitor`（監控與聯鎖）。免安裝、不需帳號 |
| 程式 | `outage_timeline.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_斷電的代價.pdf`（A4，共 4 頁）；彩色筆兩枝（畫時間軸） |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「停電兩分鐘會怎樣？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：冷卻鏈三環、LRZ 四個數字、1 K 分水嶺、時間賽跑 | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 故障注入：在斷電時間軸上模擬 A／B／C 三種方案，把時間點畫進時間軸 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：替一間實驗室寫斷電處置卡；跑程式、改案例 | `outage_timeline.py`、列印包第 2 頁、`03_備援案例紀錄.csv` |
| 105–115 | 孩子教爸爸：操作與原理，指出一個限制 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結、替時間軸與處置卡命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `power1000.html#outage`，在「備援方案」下拉選單切換 A、B、C，再拖「UPS 撐住冷卻鏈的時間（方案 C）」滑桿，看曲線怎麼變。
- 跑一次 `python outage_timeline.py`，確認最後一行是「6 個案例，保住 4 個」。
- 讀一遍 `04_解答.md`（故障注入題目的參考答案）。

## 出題者的原則

- 一次只注入一種故障；先讓孩子預測，再按播放／按鈕看結果。
- 每一題都請孩子在時間軸上做記號：停電、UPS 用完、超過 1 K 的時間點。
- 最重要的一句：要保護的是冷卻鏈的連續運轉，不是每台儀器都要長時間備援。

## 誠實說明

- 「約 2 分鐘超過 1 K」「重新降溫 2–5 天、最壞約 10 天」「真空撐數週」出自 LRZ 與 IQM 的公開論文（arXiv:2509.12949），是一台 20 位元系統的經驗，不同機器會不同。
- 「發電機＋ATS 約 10–30 秒」「UPS 撐到發電機接手」「蓄冷桶」「軟啟動／變頻讓 UPS 小一個級距」是學程文件依文獻所做的推論。
- 動畫的溫度曲線是教學示意，不是實測；程式假設市電一回來冷卻鏈就立刻恢復，實際上壓縮機停機後再啟動常要等一段時間（需向原廠確認），真實情況只會更糟。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：故障注入（約 40 分鐘）

1. 用瀏覽器開 `animations/power1000.html#outage`（場景 5：斷電時間軸）。
2. 看懂畫面：橫軸是對數時間（1 秒到 10 天），金色曲線是混合腔溫度，紅色虛線是 1 K，白點沿著曲線自動播放，上方顯示時間 t 和溫度。
3. 「備援方案」選「A：只有控制電子接 UPS」，看白點何時衝過紅線、何時降回來；左下讀數看「停機時間（示意）」。
4. 換「B：冷卻鏈 UPS＋發電機接手」：曲線平貼在底下，停機時間 0。
5. 換「C：冷卻鏈 UPS，但發電機沒起來」，把「UPS 撐住冷卻鏈的時間（方案 C）」拖到 5、15、30、60 分鐘，各看一次。
6. 每一題都把時間點畫在列印包第 1 頁的時間軸上。

## 加映：周邊系統動畫（約 10 分鐘，可選）

- `animations/peripherals.html#cooldown`：按「⏸ 暫停」，再拖「時間 (小時)」滑桿，看四個階段：① 抽真空 → ② 脈衝管預冷 → ③ 凝結混合氣 → ④ 稀釋循環 → 基溫。
- `animations/peripherals.html#monitor`：先按「正常運轉」，再按「冷卻水中斷」，看狀態從 WARN 變 ALARM、壓縮機停止、混合氣回收到儲存槽、右下監控曲線往上翹。

## 下半場：斷電處置卡（約 30 分鐘）

1. 選一間實驗室（可以是想像的），在列印包第 2 頁寫：誰負責、偵測到什麼、先做什麼、多久之內要決定。
2. 打開 `outage_timeline.py`，找到最上面的 `TOLERANCE_MIN`、`GEN_START_MIN` 和 `CASES`。
3. 先在 `03_備援案例紀錄.csv` 寫預測，再執行 `python outage_timeline.py`，把結果抄進去。
4. 改造：在 `CASES` 加一個自己的案例（例如 UPS 只撐 1 分鐘、發電機沒起來、市電停 3 分鐘），先預測，再跑。
5. 想一想：UPS 要撐多久才夠？是撐好幾個小時，還是撐到發電機接手？
''',

'outage_timeline.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 時間軸上的點\n\n| 時間 | 事件 | 依據 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in TIMELINE)
  + '\n## 故障注入題目\n\n| 題目 | 參考答案 |\n|---|---|\n'
  + ''.join(f'| {a} | {b} |\n' for a, b in QUIZ)
  + '\n## outage_timeline.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- 冷卻鏈沒有備援（A）時，市電停多久，冷卻鏈就停多久：停 1 分鐘還在 2 分鐘以內，停 5 分鐘就超過。\n'
  '- 冷卻鏈接 UPS 且發電機起來（B）：UPS 只要撐過發電機接手的 30 秒，冷卻鏈不停；市電停 3 小時也一樣。\n'
  '- 發電機沒起來（C）：UPS 用完之後，冷卻鏈停到市電回來；市電 16 分鐘回來時只多停 1 分鐘，60 分鐘就停 45 分鐘。\n'
  '- 限制：程式假設市電一回來冷卻鏈就立刻恢復，實際上壓縮機再啟動常要等待；容忍時間 2 分鐘是 LRZ 一台機器的經驗值。\n'
  '- 常見誤解：要保護的是冷卻鏈的連續運轉（壓縮機、氣體處理系統、冰水機與泵浦），不是每台儀器都要長時間備援；UPS 的任務是撐到發電機接手。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `power1000.html#outage`（場景 5：斷電時間軸：2 分鐘換 2–5 天）

- 橫軸是對數時間（刻度 1 秒、1 分、2 分、1 小時、1 天、5 天，播到 10 天）；縱軸是混合腔溫度（10 mK 到 300 K）；紅色虛線是 1 K，旁邊寫著「超過 1 K → 需要完整校準」。
- 「備援方案」下拉選單：A 只有控制電子接 UPS；B 冷卻鏈 UPS＋發電機接手；C 冷卻鏈 UPS，但發電機沒起來。
- 「UPS 撐住冷卻鏈的時間（方案 C）」滑桿：5–60 分鐘。換方案或拖滑桿時，白點從 1 秒重新播放。
- 讀數：方案、冷卻鏈負載（55–110 kW）、停機時間（示意）。曲線是依 LRZ 公開數據繪製的教學示意，不是實測。

## `peripherals.html#cooldown`（場景 4：降溫流程）

- 「時間 (小時)」滑桿 0–36、「⏸ 暫停」「⟲ 重新開始」、「播放速度（小時/秒）」滑桿；右下是各級溫度隨時間的對數圖。
- 副標題：乾式稀釋冷凍機一次完整降溫約 1–2 天；升溫回室溫也需約 1 天。

## `peripherals.html#monitor`（場景 9：監控、聯鎖與故障處置）

- 按鈕：正常運轉、冷卻水中斷、真空洩漏、流阻堵塞。
- 冷卻水中斷：入水溫度上升 → WARN → ALARM → 聯鎖停止壓縮機、GHS 回收混合氣到儲存槽 → 各級溫度計變紅、右下監控曲線往上翹。

## 操作

滑鼠拖曳旋轉、滾輪縮放；左右方向鍵換場景、空白鍵暫停、H 隱藏面板。
''',
}

SHEET_HEADER = ['案例', '市電停幾分鐘', '冷卻鏈接 UPS？', 'UPS 撐幾分鐘', '發電機起來？', '我的預測', '冷卻鏈停幾分鐘', '結果', '和預測一樣嗎']
SHEET_ROWS = ([['A', '1', '否', '0', '否'], ['A', '5', '否', '0', '否'], ['B', '180', '是', '15', '是'],
               ['C', '10', '是', '15', '否'], ['C', '16', '是', '15', '否'], ['C', '60', '是', '15', '否'], ['自己設計', '', '', '', '']])

EXTRA_CSS = '''.axis{position:relative;height:42mm;border-left:1.5pt solid #0b2540;border-bottom:1.5pt solid #0b2540;margin:4mm 0 10mm 8mm}
.axis .red{position:absolute;left:0;right:0;top:45%;border-top:1.2pt dashed #c0392b}
.axis .red span{position:absolute;right:0;top:-5mm;color:#c0392b;font-size:9pt}
.axis .tick{position:absolute;bottom:-6mm;font-size:9pt;color:#4a6a88;transform:translateX(-50%)}
.axis .yl{position:absolute;left:-8mm;font-size:8.5pt;color:#4a6a88}
table.rec td{height:8mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:1.4pt solid #0b2540;border-radius:3mm;padding:3mm 4mm;margin-top:3mm}.card .row{border-bottom:1pt dashed #4a6a88;height:8.5mm;margin-top:1mm}
pre.code{font-size:8.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:2.5mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 outage_timeline.py（隔離模式），確認輸出和影片、教材寫的數字一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'outage_timeline.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    ticks = ''.join(f'<span class="tick" style="left:{x}%">{s}</span>' for x, s in
                    [(0, '1 秒'), (30, '1 分'), (35, '2 分'), (60, '1 小時'), (83, '1 天'), (95, '5 天')])
    pages = [
        '<h2>斷電時間軸</h2><p class="lead">跟著 power1000.html#outage 故障注入：每一題都在下面的時間軸做記號。</p>'
        '<p>開場先猜：冷卻停兩分鐘，要多久才能恢復？ □ 幾分鐘　□ 幾小時　□ 幾天　因為＿＿＿＿＿＿＿＿＿＿</p>'
        '<div class="axis"><span class="yl" style="top:0">300 K</span><span class="yl" style="top:40%">1 K</span><span class="yl" style="bottom:0">10 mK</span>'
        f'<div class="red"><span>1 K 紅線：超過要完整校準</span></div>{ticks}</div>'
        '<table class="rec"><tr><th>題目（爸爸注入的故障）</th><th>我的預測</th><th>超過 1 K 的時間點</th><th>停機多久</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td><td></td></tr>' for a in
                  ['方案 A：只有控制電子接 UPS', '方案 B：冷卻鏈 UPS＋發電機', '方案 C：UPS 撐 15 分鐘', '方案 C：UPS 撐 60 分鐘', '冷卻水中斷（pe#monitor）'])
        + '</table><p class="note">用兩種顏色：藍色畫「停電、UPS 接手、發電機接手」，紅色畫「超過 1 K」。</p>',
        '<h2>換你改造：實驗室斷電處置卡</h2><p class="lead">替一間實驗室寫：停電的時候，誰、看什麼、先做什麼、多久之內要決定。</p>'
        '<div class="card"><b>實驗室名稱：＿＿＿＿＿＿＿＿　值班人：＿＿＿＿＿＿　聯絡電話：＿＿＿＿＿＿</b>'
        '<p>1. 偵測：看到什麼就算停電／冷卻異常？（告警、讀數）</p><div class="row"></div>'
        '<p>2. 處置：前 30 秒、前 2 分鐘各要確認什麼？（UPS、發電機、冷卻水）</p><div class="row"></div><div class="row"></div>'
        '<p>3. 通報與恢復：要通知誰？超過 1 K 之後要排幾天停機？</p><div class="row"></div></div>'
        '<table class="rec"><tr><th>案例</th><th>市電停</th><th>冷卻鏈 UPS</th><th>UPS 撐</th><th>發電機</th><th>我的預測</th><th>程式結果</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<pre class="code">TOLERANCE_MIN = 2.0   # 冷卻鏈最多能停幾分鐘\nGEN_START_MIN = 0.5   # 發電機＋自動切換（30 秒）\nCASES = [ (名稱, 市電停幾分鐘, 冷卻鏈接 UPS?, UPS 撐幾分鐘, 發電機起來?) ... ]</pre>',
        '<h2>三個容易錯的地方</h2><div class="box"><ul class="chk">'
        '<li>要保護的是冷卻鏈的連續運轉，不是每台儀器都要長時間備援</li>'
        '<li>冰水機也是關鍵負載：冷卻水太熱，低溫泵浦一樣會跳機；可加蓄冷桶讓泵浦繼續循環</li>'
        '<li>壓縮機啟動電流要和 UPS 一起算：軟啟動或變頻驅動能讓 UPS 小一個級距</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>時間賽跑</h3>'
        '<p>UPS 接手：幾乎立刻　發電機＋ATS：約＿＿＿秒　冷卻能停：約＿＿＿分鐘</p>'
        '<p>所以 UPS 要撐到：□ 好幾個小時　□ 發電機接手為止</p>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>最後一關：教爸爸斷電的代價</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 為什麼冷卻停兩分鐘，要賠上兩到五天？</p><div class="line"></div>'
        '<p>2. 三種備援方案，哪幾種會超過 1 K？為什麼？</p><div class="line"></div>'
        '<p>3. UPS 要撐到什麼時候為止？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>不看稿說出核心原理：約 2 分鐘超過 1 K、重新降溫 2–5 天、損失的是時間</li><li>示範 power1000.html#outage 切換 A／B／C，並解釋曲線</li>'
        '<li>說出備援邏輯：UPS 撐到發電機接手，保護整條冷卻鏈</li><li>指出一個限制：曲線是示意、程式假設電一回來冷卻就恢復</li>'
        '<li>替斷電時間軸與處置卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q130 斷電的代價 列印包', '父子科技學院 量子電腦學程 Q130｜斷電的代價：2 分鐘換 2–5 天', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q130-outage-cost', folder='Q130_斷電的代價', files=FILES,
        sheet=('03_備援案例紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_斷電的代價.pdf', pack_pages=4,
        pack_needles=('斷電時間軸', '1 K 紅線', '處置卡', '容易錯', '時間賽跑', '最後一關'),
        authoring_dir=XINEW / 'authoring/q130', episode_dir='specials/q130-outage-cost',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；outage_timeline.py 只需 Python 3）',
               'program': 'outage_timeline.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'cases': 6, 'kept': 4, 'lost': ['A 市電停 5 分鐘', 'C 發電機沒起來、市電停 60 分鐘']},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q130/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

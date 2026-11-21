"""Q131 課堂教材：冷卻鏈供電架構圖底稿、設備清單、停電考題卡、壓縮機接法比較表、說明卡與解答。

不需要帳號或安裝；只要紙筆（或瀏覽器打開 animations/power1000.html#outage 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q131/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 設備清單：(設備, 屬於哪一層, 為什麼)
DEVICES = [
    ('中壓雙迴路進線', '進線', '一路斷了還有另一路'),
    ('發電機＋自動切換開關（ATS）', '進線', '長時間停電的電源；啟動加切換約 10–30 秒（推論）'),
    ('N+1 UPS（冷卻鏈用）', '機電匯流排', '撐到發電機接手'),
    ('氦壓縮機（每支脈衝管一台，約 10–15 kW）', '機電匯流排', '最大的單一負載；停了就沒有冷卻'),
    ('氣體處理系統（GHS）泵浦與閥門', '機電匯流排', '讓混合氣循環；不能斷電'),
    ('冰水機與冷卻水泵浦', '機電匯流排', '帶走壓縮機的熱；水溫超限會讓泵浦跳機'),
    ('冷卻水蓄冷桶', '機電匯流排（水路）', '冰水機停了，泵浦繼續轉，水溫守住幾分鐘'),
    ('精密空調', '依負載分層', '控制電子區要穩定室溫；冷凍機房也要恆溫'),
    ('隔離、低雜散磁場變壓器', '乾淨匯流排', '和機電匯流排分開'),
    ('雙轉換 UPS（乾淨用）', '乾淨匯流排', '零切換時間，給控制電子'),
    ('控制電子、精密直流電源', '乾淨匯流排', '單點接地，遠離馬達雜訊'),
]
QUIZ = [  # (業主的考題, 參考答案)
    ('市電斷了 30 秒就回來，冷凍機會怎樣？', '冷卻鏈接在 UPS 上：壓縮機、GHS、冷卻水泵都不停，溫度不動。'),
    ('市電斷了 1 小時，發電機正常啟動。', 'UPS 先撐 10–30 秒，發電機接手後由發電機帶整條冷卻鏈。'),
    ('發電機沒起來，UPS 撐得了多久就多久，然後呢？', 'UPS 耗盡後冷卻停止，約 2 分鐘超過 1 K（依機型），之後要 2–5 天恢復。所以發電機要定期帶載測試。'),
    ('冰水機故障，但市電正常。', '蓄冷桶＋泵浦繼續循環，水溫在幾分鐘內守住；要在這段時間內切到備用冰水機。'),
    ('3 台壓縮機同時啟動，UPS 跳脫。', '啟動電流太大：先錯開啟動，再考慮軟啟動或變頻驅動。'),
    ('只有控制電子接 UPS，停電時會怎樣？', '電腦還醒著，冷卻卻停了：約 2 分鐘晶片超過 1 K（LRZ 數據點）。'),
]
COMPARE = [  # (接法, 啟動電流, UPS 容量, 好處, 代價)
    ('直接接市電（定頻）', '大（啟動瞬間）', '要放大才撐得住', '簡單、OEM 原廠方案', 'UPS 成本被啟動電流放大；不能錯開或降頻'),
    ('加軟啟動', '降低', '可小一個級距（設計目標）', '不改壓縮機運轉點', '只管啟動，不管穩態'),
    ('加變頻驅動', '降低', '可小一個級距（設計目標）', '可群控錯開啟動；主動前端 THD < 5%；穩態降頻可能省電（需實測）', '變頻器可能變雜訊源：要濾波、屏蔽；改轉速可能影響冷卻，第一版只做軟啟動＋額定頻率'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q131：冷卻鏈不斷電與壓縮機驅動（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「真實任務」：孩子當設計師，替一台超導量子電腦畫冷卻鏈的供電架構圖；你當業主，出停電考題。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 為什麼先保護冷卻鏈、冷卻鏈四棒、架構三層 | 影片第 3–6 段、列印包第 1 頁 |
| 25–65 | 畫冷卻鏈供電架構圖；業主出停電考題 | 列印包第 1、2 頁、`03_停電考題紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 比較壓縮機直接接市電、加軟啟動、加變頻驅動 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：冷卻鏈為什麼要整條保護 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_冷卻鏈不斷電.pdf`（A4，共 4 頁），準備色筆三支（建議：橘＝機電、藍＝乾淨、綠＝進線與 UPS）。
- 讀一遍 `04_解答.md`。想看動畫的話，用瀏覽器開 `animations/power1000.html#outage` 與 `#overview`。

## 業主的原則

- 考題要具體：「斷多久」「哪一台壞」「發電機有沒有起來」。
- 答不出來不扣分：答不出來的地方就是架構圖要補強的地方，請孩子在圖上加一個元件或一行註解。
- 孩子若只把電腦接 UPS，先別糾正，用考題「停電 3 分鐘，冷凍機溫度呢？」讓他自己發現。

## 誠實說明

- 「約 2 分鐘超過 1 K、恢復 2–5 天」來自德國 LRZ 超算中心的公開紀錄（一台 20 位元機），不同機型會不同。
- 「發電機＋自動切換約 10–30 秒」「軟啟動讓 UPS 小一個級距」「THD < 5%」是學程供電文件的推論與設計目標，不是實測。
- 本課的架構是學程文件提出的參考架構，不是某家廠商的現成產品。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：冷卻鏈供電架構圖（約 40 分鐘）

1. 在列印包第 1 頁的底稿上，先畫出三層：最上面「進線」、左邊「機電匯流排」、右邊「乾淨匯流排」。
2. 依設備清單（列印包第 1 頁下方）把每台設備畫進對應的那一層，用線連起來。
3. 一定要標出三個位置：**UPS**（兩台：冷卻鏈用、乾淨用）、**精密空調**、**冷卻水蓄冷桶**。
4. 冷凍機畫在最右邊，用箭頭標出「冷卻」從壓縮機一路接到冷凍機。
5. 業主出考題（列印包第 2 頁），孩子在圖上指出答案；答不出來就補強，記在 `03_停電考題紀錄.csv`。

## 下半場：壓縮機的三種接法（約 30 分鐘）

1. 在列印包第 3 頁的表格填寫：直接接市電、加軟啟動、加變頻驅動，各自的啟動電流、UPS 容量、好處、代價。
2. 想一想：三台壓縮機同時啟動和錯開啟動，UPS 看到的電流有什麼不同？畫兩條示意曲線。
3. 寫下變頻驅動的一個代價（提示：雜訊、冷卻工作點）。

## 動畫對照（選做）

- `animations/power1000.html#outage`：「備援方案」選 A、B、C，看混合腔溫度曲線。
- `animations/power1000.html#overview`：勾「模擬斷電」，再取消「冷卻鏈接 UPS＋發電機」，看 MXC 溫度。
- `animations/peripherals.html#pulsetube`：氦壓縮機、旋轉閥與冷卻水。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 設備放在哪一層\n\n| 設備 | 層 | 為什麼 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in DEVICES)
  + '\n精密空調：課綱要求標出位置。控制電子區（乾淨側）需要穩定室溫（LRZ 案例要求控制電子 ΔT < 1 °C／24 h）；機電區也要散熱。畫在哪一側都可以，重點是寫出它要不要接 UPS、為什麼。\n\n'
  + '## 停電考題參考答案\n\n' + ''.join(f'- **{q}** {a}\n' for q, a in QUIZ)
  + '\n## 壓縮機三種接法\n\n| 接法 | 啟動電流 | UPS 容量 | 好處 | 代價 |\n|---|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in COMPARE)
  + '\n## 常見誤解\n\n'
  '- 「UPS 要撐好幾個小時」：冷卻鏈 UPS 的主要任務是撐到發電機接手（約 10–30 秒，推論）；長時間靠發電機。\n'
  '- 「壓縮機停一下再開就好」：一般冷凍壓縮機停機後要等壓力平衡才能再啟動；氦壓縮機條件要問廠商。所以目標是不讓它停。\n'
  '- 「2 分鐘是固定值」：只是一個公開數據點（LRZ），設計時把容忍時間當輸入，依實際回溫曲線決定。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/power1000.html#outage`（斷電時間軸）

- 「備援方案」：A 只有控制電子接 UPS、B 冷卻鏈 UPS＋發電機接手、C 冷卻鏈 UPS 但發電機沒起來。
- 「UPS 撐住冷卻鏈的時間（方案 C）」：5–60 分鐘。
- 時間軸是對數座標（1 秒到 10 天），曲線是教學示意，依 LRZ 公開數據繪製。

## `animations/power1000.html#overview`（全景）

- 勾「模擬斷電（市電中斷）」，再取消「冷卻鏈接 UPS＋發電機」，看右邊 MXC 溫度變色。
- 紅色編號是痛點，點一下看說明（1 號：UPS 要為馬達群設計）。

## `animations/peripherals.html#pulsetube`（脈衝管冷卻器＋氦壓縮機）

- 壓縮機、旋轉閥、高壓與低壓氦氣管、冷卻水進出；右下小圖是冷頭內壓力。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['考題', '業主的情境', '孩子的答案（指出圖上哪裡）', '答得出來嗎', '補強了什麼']
SHEET_ROWS = [[f'考題 {i}', q] for i, (q, _) in enumerate(QUIZ, 1)] + [['自訂考題 1', ''], ['自訂考題 2', '']]

EXTRA_CSS = '''.arch{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:30mm 70mm;gap:4mm;margin-top:3mm}
.lane{border:1.3pt dashed #0b2540;border-radius:3mm;padding:2mm 3mm;font-size:11pt;color:#4a6a88}
.lane.top{grid-column:1/3}.lane b{color:#0b2540}
.dev{columns:2;font-size:10.5pt;margin:3mm 0 0;padding-left:5mm}.dev li{margin:.6mm 0}
.quiz{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}
.qc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:3mm 4mm;min-height:52mm;font-size:12pt}.qc b{color:#35a9d6}
table.rec td{height:15mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    dev = ''.join(f'<li>{a}</li>' for a, *_ in DEVICES)
    quiz = ''.join(f'<div class="qc"><b>考題 {i}</b><br>{q}<br><br>答案在圖上哪裡？<div class="line"></div><div class="line"></div></div>'
                   for i, (q, _) in enumerate(QUIZ, 1))
    pages = [
        '<h2>冷卻鏈供電架構圖（底稿）</h2><p class="lead">把設備畫進對應的層，連起線。一定要標出：UPS、精密空調、冷卻水蓄冷桶。</p>'
        '<div class="arch"><div class="lane top"><b>進線</b>（中壓雙迴路、發電機、自動切換開關）</div>'
        '<div class="lane"><b>機電匯流排</b>（變壓器 A）</div><div class="lane"><b>乾淨匯流排</b>（變壓器 B）　→　冷凍機</div></div>'
        f'<h3 style="margin-top:4mm">設備清單</h3><ul class="dev">{dev}</ul>'
        '<p class="note">提示：冷卻要從壓縮機一路接到冷凍機；任何一棒停下，晶片就回溫。</p>',
        f'<h2>停電考題卡</h2><p class="lead">業主（爸爸）讀考題，設計師（你）在架構圖上指出答案。答不出來就補強。</p><div class="quiz">{quiz}</div>',
        '<h2>換你改造：壓縮機的三種接法</h2><p class="lead">比較直接接市電、加軟啟動、加變頻驅動。</p>'
        '<table class="rec"><tr><th>接法</th><th>啟動電流</th><th>UPS 容量</th><th>好處</th><th>代價</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td></tr>' for r in COMPARE) + '</table>'
        '<h3 style="margin-top:5mm">三台壓縮機：同時啟動 vs 錯開啟動</h3>'
        '<div class="box" style="height:60mm"><p class="note">畫兩條示意曲線：橫軸時間、縱軸 UPS 看到的電流。</p></div>'
        '<p class="note">變頻驅動的一個代價：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡：我的冷卻鏈供電架構圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 冷卻鏈有哪幾棒？</p><div class="line"></div><p>2. 為什麼 UPS 要涵蓋壓縮機，而不是只保護電腦？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出冷卻鏈四棒：壓縮機、冷卻水、氣體處理、稀釋冷凍機</li><li>解釋分層保護：UPS 撐到發電機接手</li>'
        '<li>說出蓄冷桶的用途</li><li>指出一個限制：停太久會回溫，備援時間依回溫曲線決定</li>'
        '<li>替架構圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q131 冷卻鏈不斷電 列印包', '父子科技學院 量子電腦學程 Q131｜冷卻鏈不斷電與壓縮機驅動', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q131-cooling-chain-ups', folder='Q131_冷卻鏈不斷電', files=FILES,
        sheet=('03_停電考題紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_冷卻鏈不斷電.pdf', pack_pages=4,
        pack_needles=('架構圖', '設備清單', '停電考題卡', '三種接法', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q131', episode_dir='specials/q131-cooling-chain-ups',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'devices': len(DEVICES), 'quizCards': len(QUIZ), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q131/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

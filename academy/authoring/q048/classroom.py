"""Q048 課堂教材：機房配置方格紙、設備卡與用電表、從零到上線檢查表（五階段×四項）、停電演練卡、可執行的 power_budget.py、說明卡與解答。

不需要帳號、不需要安裝套件（power_budget.py 只用 Python 標準函式庫；也可以只用計算機）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q048/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 典型用電（kW）：學程「周邊系統連接與啟動指南」§1.2、animations/js/peripherals/common.js PD.power
LOADS = [  # (設備, kW, 一般接法, 建議位置)
    ('脈衝管壓縮機', 10.7, '三相市電（通常不接 UPS）', '隔壁或室外'),
    ('冷卻水系統（冷卻水機、泵）', 10.0, '三相市電', '隔壁或室外'),
    ('控制電子機櫃', 3.0, 'UPS（前面加隔離變壓器）', '靠近冷凍機頂板'),
    ('氣體處理系統（泵）', 1.5, '市電；控制器與閥門接 UPS', '靠近冷凍機'),
    ('電腦／監控／網路', 1.0, 'UPS', '機櫃旁或控制室'),
]
TOTAL = round(sum(k for _, k, *_ in LOADS), 1)
assert TOTAL == 26.2

# 從零到上線整合檢查表：slides/QC_Peripheral_Systems_Talk.pptx 第 37 頁
CHECKLIST = [
    ('1. 設施就緒', ['三相電、UPS、接地', '冷卻水機與水路', '壓縮空氣、空調', '網路與時間同步']),
    ('2. 冷卻系統', ['壓縮機 ↔ 冷頭軟管', '冷卻水試運轉', 'GHS 泵、閥、儲存槽', '控制軟體連線']),
    ('3. 低溫佈線', ['裝線、熱錨定', '室溫／低溫各量一次穿透', '屏蔽、樣品盒、打線', '關罐、抽真空、檢漏']),
    ('4. 降溫', ['脈衝管預冷', '凝結混合氣', '循環到基溫', '確認各級溫度']),
    ('5. 電子與校準', ['儀器鎖相、觸發', 'HEMT／TWPA 偏壓', '自動校準流程', '基準測試 → 上線']),
]
assert all(len(items) == 4 for _, items in CHECKLIST)

PROGRAM = '''"""父子科技學院 量子電腦學程 Q048：從零到上線——機房用電與 UPS 估算（只用 Python 標準函式庫）

執行：python power_budget.py
數字是學程簡報與文件整理的代表值（依機型與規模而異），只用來練習「先算清楚再配置」。
"""
LOADS = {                      # kW；學程《周邊系統連接與啟動指南》§1.2
    '脈衝管壓縮機': 10.7,
    '冷卻水系統': 10.0,
    '控制電子機櫃': 3.0,
    '氣體處理系統（泵）': 1.5,
    '電腦／監控／網路': 1.0,
}

total = sum(LOADS.values())
print(f'合計約 {total:.1f} kW（簡報取整為「約 25 kW」）')
for name, kw in LOADS.items():
    print(f'  {name:<12} {kw:>5.1f} kW  佔 {kw / total:5.1%}')

# 改造區：決定哪些負載接 UPS、要撐多久（小時），UPS 需要的能量 = 功率 × 時間
on_ups = ['控制電子機櫃', '電腦／監控／網路']    # 一般作法：控制系統接 UPS，壓縮機不接
hours = 2                                           # 簡報建議至少 1–2 小時
kw = sum(LOADS[n] for n in on_ups)
print(f'\\n方案 A：UPS 供 {kw:.1f} kW × {hours} 小時 = {kw * hours:.1f} kWh')

# 方案 B（學程文件的推論）：冷卻鏈也接 UPS，只要撐到發電機接手（例如 15 分鐘）
cool = LOADS['脈衝管壓縮機'] + LOADS['冷卻水系統']
bridge_h = 15 / 60
print(f'方案 B：另加冷卻鏈 {cool:.1f} kW × {bridge_h:.2f} 小時 = {cool * bridge_h:.1f} kWh，'
      f'但 UPS 的瞬間輸出要從 {kw:.1f} kW 提高到 {kw + cool:.1f} kW 以上')
'''

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q048：從零到上線（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的真實任務：把整套超導量子電腦搬進一間空房間，畫出機房配置圖，再照「從零到上線」檢查表逐項打勾。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開機房場景，算總用電（約 25 kW）、認識四大需求 | `animations/peripherals.html#infra`、列印包第 2 頁、`power_budget.py` |
| 25–65 | 孩子當工程師畫配置圖，爸爸當驗收員拿檢查表逐項問 | 列印包第 1、3 頁、方格紙 |
| 65–75 | 休息 | |
| 75–105 | 在場景按「⚡ 模擬停電」，修改配置讓系統安全撐過，再演練一次 | 列印包第 4 頁、`animations/power1000.html#outage` |
| 105–115 | 孩子教爸爸：四大需求、每台設備為什麼放那裡 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `peripherals.html#infra` 和 `#bringup`（不需要網路、伺服器或帳號）。
- 列印 `02_列印包_從零到上線.pdf`（A4，共 4 頁）；另準備一張方格紙、四種顏色的筆（電：黃、水：藍、接地：綠、訊號：橘）。
- 讀一遍 `04_解答.md`。

## 驗收員的原則

- 每個位置都要說得出理由：「壓縮機為什麼放隔壁？」答得出噪音、振動、廢熱才打勾。
- 漏一項就退回重畫，這就是檢查表的用處：彌補記憶和注意力的限制。
- 停電演練時，先問「混合氣怎麼辦？」——任何異常都要優先確保混合氣（³He）不外洩。

## 誠實說明

- 用電、冷卻水、UPS 時數都是學程簡報整理的代表值，依機型與規模而異。
- 「冷卻鏈也接 UPS、由發電機接手」是學程供電文件標示的推論，不是業界標準作法；簡報的一般作法是壓縮機不接 UPS，停電時依程序回收混合氣。
- 機房場景的停電溫度曲線是示意；超算中心公開案例（約 2 分鐘超過 1 K、重新降溫 2–5 天）是學程文件轉述的數字。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：算需求、畫配置（約 40 分鐘）

1. 打開 `animations/peripherals.html#infra`（場景 8：機房基礎設施）。拖曳旋轉、滾輪縮放，找出每台設備：市電變壓器、配電盤、UPS＋電池、隔離變壓器、控制電子＋電腦、GHS、壓縮機、冷卻水機、恆溫空調／壓縮空氣、單點接地、避震座。
2. 看左邊面板：正常運轉的典型用電，合計約 25 kW。執行 `python power_budget.py`（或用計算機）把列印包第 2 頁的用電表填完。
3. 在方格紙上畫機房（一格＝0.5 公尺，自己決定房間大小）：先擺冷凍機，再依四原則擺其他設備。用列印包第 2 頁的設備卡剪下來排排看，再畫上去。
4. 用四種顏色畫線：電（黃）、冷卻水（藍）、接地（綠，全部匯到一個點）、訊號（橘，走頂部線槽，和電力線分開）。
5. 爸爸拿列印包第 3 頁的檢查表，從「1. 設施就緒」開始逐項問、逐項打勾。
6. 打開 `peripherals.html#bringup`（場景 10），按「下一步 ▶」走完 11 個校準步驟，對照檢查表第 5 階段。

## 下半場：模擬停電、改配置（約 30 分鐘）

1. 回到 `#infra`，按「⚡ 模擬停電」：記下哪些設備停了、哪些還在運轉（淡黃色的 UPS 線路）。讀左邊面板的停電說明。
2. 在列印包第 4 頁的停電演練卡寫下：停電後第一件事、混合氣怎麼辦、復電後的重啟順序。
3. 打開 `animations/power1000.html#outage`（斷電時間軸），在「備援方案」選 A、B、C，比較混合腔溫度曲線。
4. 修改你的配置圖（例如加發電機、冷卻鏈接 UPS），用 `power_budget.py` 的改造區算 UPS 需要多少能量，再演練一次。
''',

'power_budget.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 用電表（學程指南 §1.2）\n\n| 設備 | 約 kW | 一般接法 | 建議位置 |\n|---|---|---|---|\n'
  + ''.join(f'| {n} | {k} | {w} | {p} |\n' for n, k, w, p in LOADS)
  + f'| 合計 | {TOTAL}（簡報與指南取整為約 25 kW） | | |\n\n'
  '壓縮機＋冷卻水約佔 79%。`power_budget.py` 輸出：方案 A（控制電子＋電腦 4.0 kW × 2 小時）= 8.0 kWh；'
  '方案 B 另加冷卻鏈 20.7 kW × 0.25 小時 ≈ 5.2 kWh，但 UPS 瞬間輸出要提高到 24.7 kW 以上。\n\n'
  '## 配置四原則（簡報第 33 頁）\n\n'
  '1. 冷凍機置中，四周留維護與開罐空間，上方要有挑高與吊裝設備。\n'
  '2. 電子機櫃靠近冷凍機頂板 → 室溫纜線短（損耗與相位漂移小）。\n'
  '3. GHS 與儲存槽靠近冷凍機 → 抽氣管短。\n'
  '4. 壓縮機、冷卻水機放隔壁或室外 → 噪音、振動、廢熱隔離；頂部線槽分開微波／直流與電力；單點接地、UPS 與配電盤集中。\n\n'
  '## 停電演練\n\n'
  '- 自動反應：壓縮機與冷卻水停止，UPS 維持控制系統；GHS 關閉閥門，混合氣經背壓閥回收至儲存槽（指南 §6）。\n'
  '- 復電重啟順序：冷卻水 → 壓縮機 → GHS，再重新降溫、重新校準。\n'
  '- 冷卻水中斷：壓縮機聯鎖停機（避免過溫）。\n'
  '- 改造方向：冷卻鏈接 UPS 撐到發電機接手（學程文件的推論）；冷卻水加緩衝水槽；UPS 容量要和壓縮機啟動電流一起設計。\n\n'
  '## 常見誤解\n\n'
  '- 「只要控制電腦接 UPS 就安全」：電腦還在，但冷卻一停，超算中心案例約 2 分鐘晶片就超過 1 K，重新降溫 2–5 天並需完整校準。\n'
  '- 「量子電腦很省電」：一套單機系統約 25 kW，大半花在冷卻（壓縮機與冷卻水）。\n'
  '- 「接地越多點越好」：多點接地會形成接地迴路，要單點（星形）接地。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/peripherals.html#infra`（場景 8：機房基礎設施）

- 左邊面板：「⚡ 模擬停電」「脈衝管遠端馬達 + 纜線固定（降振）」兩個開關，下面是正常／停電時的說明文字。
- 顏色：黃＝電力、淡黃＝UPS 供電、藍＝冷水、橘＝回水、黃綠＝接地線、冷頭上的橘紅波浪＝冷頭振動、底下綠色波浪＝樣品處振動。
- 右下角小圖：停電後混合腔溫度的示意曲線（停電後紅點會沿曲線移動）。

## `animations/peripherals.html#bringup`（場景 10：啟動與校準）

- 「◀ 上一步」「下一步 ▶」「自動播放」：走過 11 個步驟（系統檢查 → … → 隨機基準測試 → 上線）。右下角是每一步的典型量測圖。

## `animations/power1000.html#outage`（斷電時間軸）

- 「備援方案」A／B／C 與「UPS 撐住冷卻鏈的時間（方案 C）」滑桿；曲線為教學示意，時間點引用 LRZ 公開數據。

## 也可以看

- `peripherals.html#overview`（場景 1：系統全景）：所有管線與用電分配小圖。
- `power1000.html#ground`、`#field`：接地電流與母線磁場（進階）。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換場景。
''',
}

SHEET_HEADER = ['階段', '項目', '負責人', '完成（✓）', '日期', '備註']
SHEET_ROWS = [[stage, item, '', '', '', ''] for stage, items in CHECKLIST for item in items]

EXTRA_CSS = '''.sq{height:150mm;border:1.2pt solid #0b2540;background-image:linear-gradient(#cfdde8 .5pt,transparent .5pt),
linear-gradient(90deg,#cfdde8 .5pt,transparent .5pt);background-size:6mm 6mm;margin-top:3mm;position:relative}
.sq span{position:absolute;font-size:9pt;color:#4a6a88;background:#fff;padding:0 1mm}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:3mm}
.card{border:1.2pt dashed #0b2540;border-radius:2mm;padding:2mm;font-size:10pt;text-align:center;height:15mm;display:flex;align-items:center;justify-content:center}
table.ck td{font-size:10.5pt;padding:1.1mm 2mm}table.ck td.box{width:9mm;text-align:center}table.ck th{font-size:10.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.ld td{height:9mm}'''

DEVICES = ['稀釋冷凍機', '控制電子機櫃', '電腦', 'GHS', '混合氣儲存槽', '脈衝管壓縮機', '冷卻水機', '配電盤',
           'UPS＋電池', '隔離變壓器', '恆溫空調', '壓縮空氣', '單點接地', '頂部線槽', '發電機（改造用）', '緩衝水槽（改造用）']


def html():
    cards = ''.join(f'<div class="card">{d}</div>' for d in DEVICES)
    ld = ''.join(f'<tr><td>{n}</td><td>{k}</td><td></td><td></td><td></td></tr>' for n, k, *_ in LOADS)
    ck = ''.join(f'<tr><th colspan="3">{stage}</th></tr>' + ''.join(
        f'<tr><td class="box">□</td><td>{it}</td><td style="width:38mm"></td></tr>' for it in items) for stage, items in CHECKLIST)
    pages = [
        '<h2>機房配置圖</h2><p class="lead">一格＝0.5 公尺。先擺冷凍機，再依四原則擺其他設備；用四種顏色畫線：電（黃）、水（藍）、接地（綠）、訊號（橘）。</p>'
        '<div class="sq"><span style="left:2mm;top:2mm">北</span><span style="right:2mm;bottom:2mm">比例：一格 0.5 m</span></div>'
        '<div class="box" style="margin-top:4mm"><p>配置圖名稱：＿＿＿＿＿＿＿＿＿＿　工程師：＿＿＿＿＿　驗收員：＿＿＿＿＿</p>'
        '<p class="note">四原則：① 冷凍機置中、留開罐空間與吊裝挑高　② 電子機櫃靠近頂板　③ GHS 靠近冷凍機　④ 壓縮機、冷卻水機放隔壁或室外；電力線和訊號線分開走</p></div>',
        '<h2>設備卡與用電表</h2><p class="lead">剪下設備卡，在方格紙上排排看；再把用電表填完（可用 power_budget.py 驗算）。</p>'
        f'<div class="cards">{cards}</div>'
        '<h3 style="margin-top:5mm">用電表（典型值，依機型而異）</h3>'
        '<table class="ld"><tr><th>設備</th><th>約 kW</th><th>接市電或 UPS？</th><th>放在哪裡？</th><th>理由</th></tr>' + ld
        + '<tr><td><b>合計</b></td><td></td><td colspan="3">簡報說「約 25 kW」，你算出來是＿＿＿＿ kW</td></tr></table>'
        '<p class="note">最大的兩項是哪兩台？它們加起來佔總用電的百分之幾？＿＿＿＿＿＿＿＿</p>',
        '<h2>從零到上線檢查表</h2><p class="lead">五個階段、每階段四項。驗收員逐項問，答得出理由才打勾。</p>'
        f'<table class="ck"><tr><th style="width:9mm">✓</th><th>項目</th><th>負責人／日期</th></tr>{ck}</table>'
        '<p class="note">檢查表的用處：彌補記憶和注意力的限制，避免漏掉步驟。（第 5 階段可對照 peripherals.html#bringup 的 11 個校準步驟）</p>',
        '<h2>停電演練卡</h2><div class="box"><p>1. 按「⚡ 模擬停電」後，停下來的設備：＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>　還在運轉（接 UPS）的設備：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>2. 混合氣怎麼辦？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>3. 復電後重啟順序：（　）→（　）→（　）</p>'
        '<p>4. 我的改法（例如發電機、冷卻鏈接 UPS、緩衝水槽）：</p><div class="line"></div>'
        '<p>5. UPS 要供幾 kW、撐多久？需要多少 kWh？＿＿＿＿＿＿＿＿＿</p></div>'
        '<h2 style="margin-top:5mm">說明卡：我的機房</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 機房要準備哪四樣東西？</p><div class="line"></div><p>2. 壓縮機為什麼放隔壁或室外？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出四大需求：電力、冷卻水、防振、接地</li><li>指著配置圖說出每台設備為什麼放那裡</li>'
        '<li>說出哪些設備接 UPS、為什麼壓縮機通常不接</li><li>指出注意事項：一套約 25 kW；停電先保護壓縮機與混合氣</li>'
        '<li>替配置圖和檢查表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q048 從零到上線 列印包', '父子科技學院 量子電腦學程 Q048｜從零到上線', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q048-zero-to-online', folder='Q048_從零到上線', files=FILES,
        sheet=('03_上線檢查表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_從零到上線.pdf', pack_pages=4,
        pack_needles=('機房配置圖', '設備卡', '用電表', '從零到上線檢查表', '停電演練卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q048', episode_dir='specials/q048-zero-to-online',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'power_budget.py', 'loadsKW': {n: k for n, k, *_ in LOADS}, 'totalKW': TOTAL,
               'checklistFrom': 'slides/QC_Peripheral_Systems_Talk.pptx p37', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q048/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

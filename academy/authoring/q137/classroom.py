"""Q137 課堂教材：中性原子供電需求表底稿、離子阱比較表、擴大瓶頸推論單、說明卡與解答。

不需要帳號或安裝；只要紙筆（或瀏覽器打開 animations/atoms.html#atomsys 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q137/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 需求表：(設備, 類別, 用電, 怕什麼, 可容忍中斷, 建議供電, 依據)
NEEDS = [
    ('光鑷雷射（光纖放大器）', '雷射', '50 W 型 < 300 W、100 W 型 < 500 W；130 W 光功率約 0.4–0.65 kW 電力（推論）',
     '泵浦驅動電流雜訊 → 強度雜訊 → 參量加熱（推論）', 'T1 秒級：失原子可接受，熱狀態被打亂代價高', '雙轉換 UPS；需要冷卻', '簡報 p38–40；文獻回顧 §12.1、§13.1、§14.2'),
    ('芮德堡雷射＋超穩參考腔', '雷射', '小', '相位雜訊（servo bump）；參考腔溫度', 'T1 秒級（參考腔溫控）', '雙轉換 UPS；低雜訊雷射電流源', '簡報 p38、p40；§13.2'),
    ('冷卻／成像雷射（780 nm）', '雷射', '小', '驅動電流雜訊', 'T1 秒級（鎖頻）', '雙轉換 UPS', '§12.1；§14.1'),
    ('AOD／AOM 的 RF 驅動（多音 AWG＋放大器）', '射頻驅動', '中', '電源漣波 → 繞射效率 → 強度雜訊（推論）', '依附在 T1（與雷射一起）', '低漣波電源', '簡報 p38、p43；§13.4'),
    ('MOT 與補償線圈電源', '線圈', '裝載時大電流，計算時關閉、只留量化軸', '要快速關斷（IGBT 需 TVS 保護）又要 ppm 級穩場', '可中斷：重新裝載即可', '可不接 UPS，省容量（推論）', '簡報 p40–41；§13.3、§14.2'),
    ('FPGA（即時重排）、GPU／控制電腦', '控制與環境', '中；容錯階段會變大（解碼）', '不能斷', 'T1 秒級', '雙轉換 UPS', '§12.1；§14.2'),
    ('精密空調（恆溫）', '控制與環境', '可能是最大項', '停了 → 光路漂移、陣列位置偏、雷射失鎖', 'T2 分鐘級', 'UPS 撐到發電機', '§12.1；§14.1–14.2'),
    ('雷射冷卻水機', '控制與環境', '可能是最大項之一', '水溫（Pasqal 20–23 °C）', 'T2 分鐘級', 'UPS 撐到發電機；加緩衝', '簡報 p38；§12.2、§14.2'),
    ('離子泵控制器（真空）', '控制與環境', '小', '壓力緩慢上升', 'T3 小時級（NEG 緩衝）', '發電機', '§14.1–14.2'),
]
COMPARE = [  # (比較項, 離子阱, 中性原子)
    ('單套功率', 'Helios 官方 < 40 kW；Oracle 合作資料約 60 kW', '約 3–10 kW（峰值、典型、模型推估混合）'),
    ('最敏感的電源點', '阱 RF 振幅 ppm、DC 電極 nV/√Hz、線圈電流 ppm、雷射電流 nA', '光鑷強度雜訊、芮德堡相位雜訊、線圈快速開關'),
    ('斷電時掉了什麼', 'RF 一斷，離子立刻逃逸', '光鑷一斷，原子立刻掉出，但每輪本來就重裝'),
    ('有沒有 T0 零中斷層', '有：阱 RF 鏈、DC 電極 DAC、時序 FPGA、銣鐘（推論）', '沒有：失去原子不是災難（推論）'),
    ('要保護的是什麼', '離子本身（RF、DAC）', '雷射與光學的熱穩態'),
    ('斷電後恢復', '數十分鐘到數小時（系統指南）', '數十分鐘到數小時（系統指南）'),
    ('可以不接 UPS 的大負載', '（找找看）', 'MOT 線圈電源（推論）'),
]
SCALE = [  # (瓶頸, 依據, 推論出的供電需求)
    ('可用雷射功率', '約 15 W 囚禁 3,000 多顆原子；30–40 W 光源逐漸可得；商用放大器已超過 100 W', '更多、更大功率的光纖放大器；泵浦驅動電源'),
    ('物鏡受熱', '高功率下像差惡化；SLM 繞射效率約 65% → 45%', '散熱、精密空調、光學區局部溫控'),
    ('即時解碼', '已與 2,000 多張 H100 並置運轉', 'GPU 叢集可能 MW 級（推論）→ AI 機房供電規格'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q137：中性原子的供電：保護熱穩態（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「資料偵探」：孩子把簡報和文件裡的線索整理成一張中性原子供電需求表；你當檔案員，拿上一堂離子阱的資料逐列追問。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 整套最省電、四類用電、離子阱 vs 中性原子、分層備援 | 影片第 3–8 段 |
| 25–65 | 填中性原子供電需求表；逐列和離子阱比較 | 列印包第 1、2 頁、`03_需求表紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 推論中性原子擴大後卡在哪 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼要保護的是熱穩態 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_中性原子供電.pdf`（A4，共 4 頁），準備兩色筆（建議：黑＝文獻數字、紅＝推論）。
- 讀一遍 `04_解答.md`。準備供電簡報第 38–43 頁；想看動畫的話，用瀏覽器開 `animations/atoms.html#atomsys` 與 `#tweezer`。

## 檔案員的原則

- 每填一列就問：「這一格的出處是哪一頁？是量到的，還是推論？」
- 拿離子阱對照：「同一種設備在離子阱那邊屬於哪一層？為什麼不一樣？」
- 孩子若把光鑷雷射當成用電大宗，先別糾正，請他把 0.4–0.65 kW 和整套 3–10 kW 放在一起比。

## 誠實說明

- 0.4–0.65 kW、T1／T2／T3 分層、MOT 線圈可不接 UPS、解碼 GPU 可能 MW 級，都是學程供電文件的【推論】，不是廠商規範或實測。
- 整套 3–10 kW 是不同廠商、不同定義（峰值、典型、模型推估）的數字合在一起看的範圍。
- 外部論文的數字（130 W、4.04 → 6.34 s、−20／−30 dBc、每秒 30 萬顆原子）依學程文獻回顧的摘錄。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：中性原子供電需求表（約 40 分鐘）

1. 在列印包第 1 頁的表格裡，先寫下四類設備：雷射、射頻驅動、線圈、控制與環境。
2. 每一列填：用多少電、怕什麼、斷電能撐多久（T1 秒級／T2 分鐘級／T3 小時級／可中斷）、建議怎麼供電。
3. 每一格寫出處（簡報頁碼或文件章節）；只有推論的格子用紅筆標「推論」。
4. 填完一列，檔案員（爸爸）用列印包第 2 頁追問：離子阱那邊是哪一層？記在 `03_需求表紀錄.csv`。

## 下半場：擴大後卡在哪（約 30 分鐘）

1. 讀列印包第 3 頁的三個瓶頸：可用雷射功率、物鏡受熱、即時解碼。
2. 推論：原子數變成 10 倍時，哪一列的用電會變大？（提示：光鑷約 1.3 kW 光功率、4–6 kW 電力，推論）
3. 寫一句「真正的限制」：電不夠，還是熱散不掉，還是運算跟不上？

## 動畫對照（選做）

- `animations/atoms.html#atomsys`：按「只看設施」，看右下角「典型用電分配」（示意）；按「只看電子訊號」＋「視角：機櫃側」，找出線圈電源。
- `animations/atoms.html#tweezer`：按「① 裝載」「② 成像」「③ 重排」，看原子掉了怎麼一輪補回來。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 中性原子供電需求表\n\n| 設備 | 類別 | 用電 | 怕什麼 | 可容忍中斷 | 建議供電 | 依據 |\n|---|---|---|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in NEEDS)
  + '\n## 和離子阱比較\n\n| 比較項 | 離子阱 | 中性原子 |\n|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in COMPARE)
  + '\n## 擴大後卡在哪\n\n| 瓶頸 | 依據 | 推論出的供電需求 |\n|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in SCALE)
  + '\n## 常見誤解\n\n'
  '- 「整套省電，電源隨便就好」：光鑷強度雜訊會在兩倍阱頻附近造成參量加熱，縮短原子壽命；泵浦驅動與 RF 電源的雜訊不能放過。\n'
  '- 「原子掉了就是災難」：中性原子每輪本來就重新裝載；真正花時間的是雷射重新鎖頻、熱平衡與 SLM／AOD 重新校準。\n'
  '- 「大電流負載一定要接 UPS」：MOT 線圈斷了只要重新裝載，文件推論可以不接 UPS，省下容量。\n'
  '- 「光鑷雷射是用電大宗」：約 0.4–0.65 kW（推論），大宗是環境控制、其他雷射與控制電子。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/atoms.html#atomsys`（場景 7：中性原子系統全景）

- 「全部／只看雷射／只看電子訊號／只看設施」：分類顯示光路、RF 與資料線、電力與冷卻水。
- 「視角：全景」「視角：真空腔特寫」「視角：機櫃側」。
- 右下角「典型用電分配（kW，示意，非官方數字）」：雷射 3.0、雷射冷卻水機 2.5、控制電子 2.5、真空線圈微波 0.6、恆溫空調 2.0。

## `animations/atoms.html#tweezer`（場景 8：光鑷裝載與重排）

- 「① 裝載」「② 成像」「③ 重排」；滑桿「陣列大小（目標 T×T）」「裝載機率 p」。

## 操作

拖曳旋轉、滾輪縮放；`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['設備', '類別', '用電', '怕什麼', '可容忍中斷（層）', '建議供電', '出處（頁碼／章節）', '推論？', '離子阱那邊是哪一層']
SHEET_ROWS = [[a, b] for a, b, *_ in NEEDS] + [['自訂設備 1', ''], ['自訂設備 2', '']]

EXTRA_CSS = '''table.rec td{height:13mm;font-size:10.5pt}table.rec th{font-size:10.5pt}
table.cmp td{height:16mm;font-size:11pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td><td></td><td></td><td></td></tr>' for a, b, *_ in NEEDS)
    cmp_rows = ''.join(f'<tr><td><b>{a}</b></td><td></td><td></td></tr>' for a, *_ in COMPARE)
    scale = ''.join(f'<tr><td><b>{a}</b><br><span class="note">{b}</span></td><td></td></tr>' for a, b, _ in SCALE)
    pages = [
        '<h2>中性原子供電需求表（底稿）</h2><p class="lead">每一列填用電、怕什麼、斷電能撐多久、建議供電。出處寫在格子角落；推論用紅筆標出。</p>'
        '<table class="rec"><tr><th>設備</th><th>類別</th><th>用電</th><th>怕什麼</th><th>可容忍中斷</th><th>建議供電</th></tr>'
        + rows + '</table><p class="note">層級：T1 秒級／T2 分鐘級／T3 小時級／可中斷（文件推論的分層）。</p>',
        '<h2>和離子阱比一比</h2><p class="lead">檔案員（爸爸）拿出上一堂的離子阱資料，逐列追問；你填中性原子那一欄。</p>'
        '<table class="cmp"><tr><th>比較項</th><th>離子阱</th><th>中性原子</th></tr>' + cmp_rows + '</table>',
        '<h2>換你改造：擴大後卡在哪</h2><p class="lead">原子數變成 10 倍，哪裡先撐不住？寫出你推論的供電需求。</p>'
        '<table class="cmp"><tr><th>瓶頸與依據</th><th>我推論的供電需求</th></tr>' + scale + '</table>'
        '<div class="box" style="margin-top:5mm"><p>真正的限制是：□ 電不夠　□ 熱散不掉　□ 運算跟不上</p><p>為什麼：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>說明卡：我的中性原子供電需求表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 用電大宗是什麼？最敏感的又是什麼？</p><div class="line"></div><p>2. 為什麼中性原子不需要零中斷層，卻還是要保護雷射？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出四類用電：雷射、射頻驅動、線圈、控制與環境</li><li>解釋熱穩態：停機時間花在熱平衡與校準</li>'
        '<li>說出哪個大負載可以不接 UPS（MOT 線圈）</li><li>指出一個限制：光鑷強度雜訊造成參量加熱</li>'
        '<li>替需求表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q137 中性原子供電 列印包', '父子科技學院 量子電腦學程 Q137｜中性原子的供電：保護熱穩態', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q137-neutral-atom-power', folder='Q137_中性原子供電', files=FILES,
        sheet=('03_需求表紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_中性原子供電.pdf', pack_pages=4,
        pack_needles=('需求表', '和離子阱比一比', '擴大後卡在哪', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q137', episode_dir='specials/q137-neutral-atom-power',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'needsRows': len(NEEDS), 'compareRows': len(COMPARE), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q137/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q138 課堂教材：三平台供電比較表底稿、評審記分卡、UPS 設計說明單、說明卡與解答。

不需要帳號或安裝；只要紙筆（或瀏覽器打開 animations/atoms.html#compare、power1000.html#outage 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q138/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 比較表：(列, 超導, 離子阱, 中性原子, 是否推論／出處)
TABLE = [
    ('用電大宗', '壓縮機（每台 10–15 kW）＋冷卻水', '精密空調與雷射冷卻水、雷射、控制電子', '精密空調與冷卻水、雷射（光纖放大器）、控制電子／GPU', '文獻回顧 §17；簡報 p44'),
    ('單套功率', '約 20–30 kW（LRZ 降溫峰值約 30 kW）', 'Helios 官方 < 40 kW；Oracle 合作約 60 kW（不含外部空調）', '約 3–10 kW', '§17；定義不同（峰值、最壞、上限）見簡報 p45'),
    ('最敏感電源', '磁通偏壓 µV 級', '阱 RF 振幅 ppm、DC 電極 nV、線圈 ppm', '光鑷強度雜訊、芮德堡相位雜訊', '§17；簡報 p44'),
    ('可容忍中斷', '冷卻中斷約 2 分鐘內仍 < 1 K', 'RF／DAC 0 ms【推論】', '失去原子可接受（每輪本來就重新裝載）', '§17；離子阱一格是推論'),
    ('斷電後恢復', '重新降溫 2–5 天（最壞約 10 天）＋全校準', '數十分鐘～數小時', '數十分鐘～數小時', '§17；系統指南 §4'),
    ('UPS 設計邏輯', '保冷卻鏈：分鐘級、大容量、吃得下啟動電流、撐到發電機', '保離子：毫秒級、容量小、零切換＋設備端直流保持', '保熱穩態：秒到分鐘、中等容量、MOT 線圈可不接', '§17【推論】；簡報 p46'),
]
PITCHES = [  # (業務的賣點, 評審可以追問的地方, 參考判斷)
    ('「我們這台是離線式，切換只要 10 毫秒，很快！」', '離子阱 RF／DAC 能停 10 毫秒嗎？', '不行：離子阱 T0 層要零切換時間（推論），要雙轉換＋設備端直流保持。'),
    ('「容量剛好 30 kW，跟一套超導機一樣大。」', '壓縮機啟動電流算進去了嗎？', '超導 UPS 要吃得下壓縮機啟動電流；30 kW 是整套降溫峰值，啟動電流要另外向廠商確認。'),
    ('「電池可以撐 2 小時，停電都不怕。」', '發電機呢？電池撐完之後？', '超導 UPS 的任務是撐到發電機接手；電池加大只是把升溫往後推（動畫 outage 方案 C）。'),
    ('「所有設備都接上，最安全。」', 'MOT 線圈也要接嗎？', '中性原子的 MOT 線圈斷了只要重新裝載，可以不接，省下大電流容量（推論）。'),
    ('「一種規格通吃三個平台。」', '三平台的時間尺度一樣嗎？', '分鐘、毫秒、秒到分鐘不同，所以要做成依平台分層的參考設計（推論）。'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q138：三平台比較——三種 UPS 設計邏輯（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「產品評審」：孩子拿三平台供電比較表當評審，你當 UPS 業務，推銷一台「三平台通吃」的機器。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 單套功率、比較表四列、分鐘 vs 毫秒、三種設計邏輯 | 影片第 3–7 段、列印包第 1 頁 |
| 25–65 | 填三平台供電比較表；爸爸推銷、孩子評審 | 列印包第 1、2 頁、`03_評審記分.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子替一個平台寫 UPS 設計說明 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼量子機房 UPS 不能只有一種規格 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_三平台供電比較.pdf`（A4，共 4 頁），準備兩色筆（建議：黑＝有出處、紅＝推論，推論格另畫星號）。
- 讀一遍 `04_解答.md`，和供電簡報第 44–46 頁。想看動畫的話，用瀏覽器開 `animations/atoms.html#compare` 與 `animations/power1000.html#outage`。

## 業務的原則

- 賣點要具體：切換幾毫秒、容量幾 kW、電池撐多久。
- 孩子問「出處呢？」時，老實回答哪些是推論；這正是今天的驗收重點。
- 孩子若給「一種規格通吃」高分，先別糾正，用「離子阱能停 10 毫秒嗎？」讓他自己發現。

## 誠實說明

- 公開數字很少：Helios 有 < 40 kW 與約 60 kW 兩個說法，文件找不到官方說明；中性原子各家只有總數。
- 單套功率的定義不同：LRZ 是降溫峰值、Google 是最壞情況、Helios 是官方上限、Oracle 資料不含外部空調。
- 「三種 UPS 設計邏輯」「離子阱 0 ms」「MOT 線圈可不接」都是學程供電文件的推論，不是廠商規範。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：三平台供電比較表＋產品評審（約 40 分鐘）

1. 在列印包第 1 頁的表格，依影片與簡報第 44 頁填六列：用電大宗、單套功率、最敏感電源、可容忍中斷、斷電後恢復、UPS 設計邏輯。
2. 每一格寫出處；只有推論的格子用紅筆寫，並畫一個星號。
3. 爸爸當業務，從列印包第 2 頁挑賣點推銷；孩子對照比較表追問，在記分卡寫「適合哪個平台、不適合哪個平台、理由」。
4. 把每一回合記在 `03_評審記分.csv`。

## 下半場：替一個平台寫 UPS 設計說明（約 30 分鐘）

1. 挑一個平台（超導、離子阱或中性原子）。
2. 在列印包第 3 頁回答：要保護什麼？時間尺度？容量大或小？切換時間？哪些負載可以不接？
3. 最後寫一個限制（例如：只有一個公開數據點、沒有公開規格）。

## 動畫對照（選做）

- `animations/atoms.html#compare`：三平台並排；按「規模」看已展示的位元數。
- `animations/power1000.html#outage`：「備援方案」選 C，再把「UPS 撐住冷卻鏈的時間（方案 C）」拉到 60 分鐘。
- `animations/power1000.html#roadmap`：三階段路線圖，點「分層 UPS＋精密空調參考設計」。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 三平台供電比較表\n\n| 列 | 超導 | 離子阱 | 中性原子 | 出處／推論 |\n|---|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in TABLE)
  + '\n## 業務賣點與評審判斷\n\n' + ''.join(f'- **{p}** 追問：{q} 判斷：{a}\n' for p, q, a in PITCHES)
  + '\n## 常見誤解\n\n'
  '- 「功率最大的平台最難做 UPS」：難度主要看時間尺度與切換時間；離子阱 UPS 容量小，T0 層卻最嚴格（推論）。\n'
  '- 「單套功率可以直接比大小」：降溫峰值、最壞情況、官方上限、不含外部空調，定義不同（簡報 p45）。\n'
  '- 「三種設計邏輯是業界標準」：是學程供電文件 §17 的推論；目前沒有量子電腦專用的電力品質規格（§19.1）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/atoms.html#compare`（三平台比較）

- 左超導（旁邊有 10 mK 稀釋冷凍機）、中離子阱（四根桿子間的離子鏈）、右中性原子（6×6 陣列與移動的光鑷）。
- 按鈕「連接性」「閘速度」「相干時間」「規模」切換比較項目；數值是 2024–2026 年的代表值。

## `animations/power1000.html#outage`（斷電時間軸）

- 「備援方案」C：冷卻鏈接 UPS，但發電機沒起來；滑桿「UPS 撐住冷卻鏈的時間（方案 C）」5–60 分鐘。
- 曲線是教學示意，依 LRZ 公開數據繪製。

## `animations/power1000.html#roadmap`（三階段路線圖）

- 學程文件的規劃建議（非既有產品）；點卡片跳到對應的痛點場景。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['回合', '業務的賣點', '評審追問', '適合哪個平台', '不適合哪個平台', '理由（出處或推論）']
SHEET_ROWS = [[f'回合 {i}', p] for i, (p, _, _) in enumerate(PITCHES, 1)] + [['自訂賣點 1', ''], ['自訂賣點 2', '']]

EXTRA_CSS = '''table.cmp td{height:17mm;font-size:10.5pt}table.cmp td:first-child{width:24mm;font-weight:700;color:#0b2540}
.pitch{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}
.pc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:3mm 4mm;min-height:40mm;font-size:11.5pt}.pc b{color:#35a9d6}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    rows = ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td></tr>' for r in TABLE)
    pitch = ''.join(f'<div class="pc"><b>賣點 {i}</b><br>{p}<br><br>適合／不適合哪個平台？理由：<div class="line"></div><div class="line"></div></div>'
                    for i, (p, _, _) in enumerate(PITCHES, 1))
    pages = [
        '<h2>三平台供電比較表（底稿）</h2><p class="lead">每一格寫出處；只有推論的格子用紅筆寫，並畫星號 ★。</p>'
        f'<table class="cmp"><tr><th>列</th><th>超導</th><th>離子阱</th><th>中性原子</th></tr>{rows}</table>'
        '<p class="note">提示：單套功率的數字定義不同（降溫峰值、最壞情況、官方上限、不含外部空調），不能直接比大小。</p>',
        f'<h2>評審記分卡：業務的賣點</h2><p class="lead">業務（爸爸）念賣點，評審（你）對照比較表追問，寫下判斷和理由。</p><div class="pitch">{pitch}</div>',
        '<h2>換你改造：一個平台的 UPS 設計說明</h2><p class="lead">挑一個平台：□ 超導　□ 離子阱　□ 中性原子</p>'
        '<div class="box"><p>1. 要保護的是什麼？</p><div class="line"></div>'
        '<p>2. 時間尺度：□ 毫秒　□ 秒到分鐘　□ 分鐘；容量：□ 小　□ 中　□ 大</p>'
        '<p>3. 切換時間的要求：</p><div class="line"></div>'
        '<p>4. 哪些負載可以不接 UPS？省下什麼？</p><div class="line"></div><div class="line"></div>'
        '<p>5. 一個限制（哪一格是推論、缺什麼公開數字）：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>說明卡：我的三平台供電比較表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 三個平台各自要保護什麼？</p><div class="line"></div><p>2. 為什麼量子機房 UPS 不能只有一種規格？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三種保護對象：冷卻鏈、離子、熱穩態</li><li>說出時間尺度：分鐘、毫秒、秒到分鐘</li>'
        '<li>說出單套功率的大小順序，以及為什麼不能直接比</li><li>指出一個限制：公開數字有限，部分是推論</li>'
        '<li>替比較表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q138 三平台供電比較 列印包', '父子科技學院 量子電腦學程 Q138｜三平台比較：三種 UPS 設計邏輯', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q138-three-platform-ups', folder='Q138_三平台供電比較', files=FILES,
        sheet=('03_評審記分.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_三平台供電比較.pdf', pack_pages=4,
        pack_needles=('比較表', '評審記分卡', '設計說明', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q138', episode_dir='specials/q138-three-platform-ups',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'tableRows': len(TABLE), 'pitchCards': len(PITCHES), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q138/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

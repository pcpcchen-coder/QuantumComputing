"""Q135 課堂教材：磁場紀錄表、估算練習卡、配電佈局草圖底稿、說明卡與解答。

不需要帳號或安裝；只要紙筆與瀏覽器（打開 animations/power1000.html#field 移動母線、記錄冷凍機處的磁場）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q135/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 紀錄表的參考讀數：(配線方式, 電流 A, 成對間距 cm, 距離 m, 冷凍機處磁場, 交流判斷) — 由 power1000.html#field 畫面讀出（2026-11-18）
READINGS = [
    ('去回線成對', 360, 10, 3.0, '0.800 µT', '超過'),
    ('去回線成對', 360, 10, 6.0, '0.200 µT', '超過'),
    ('去回線成對', 360, 10, 8.5, '0.100 µT', '符合（剛好過線）'),
    ('去回線成對', 360, 10, 9.0, '0.089 µT', '符合'),
    ('去回線成對', 360, 10, 1.0, '7.2 µT', '超過'),
    ('單根（淨電流不為零）', 360, '—', 3.0, '24.0 µT', '超過'),
    ('單根（淨電流不為零）', 360, '—', 6.0, '12.0 µT', '超過'),
    ('變壓器（近似偶極）', 360, '—', 3.0, '0.533 µT', '超過'),
    ('變壓器（近似偶極）', 360, '—', 6.0, '0.067 µT', '符合'),
    ('去回線成對', 1000, 10, 3.0, '2.2 µT', '超過'),
    ('去回線成對', 1000, 2, 3.0, '0.444 µT', '超過'),
    ('去回線成對', 1000, 2, 7.0, '0.082 µT', '符合'),
]
# 估算練習：(題目, 參考答案)
QUIZ = [
    ('單根導體 1,000 A，距離 1 m，磁場大約多少？過直流門檻嗎？', '約 200 µT（文件估算）；超過直流 < 100 µT。'),
    ('同上，改成 2 m？', '1/r：剩一半，約 100 µT，剛好在直流門檻邊緣。'),
    ('去回線成對、間距 10 cm、1,000 A、1 m？', '200 µT × (0.1 ÷ 1) = 約 20 µT；直流過關，交流遠超 ≪ 1 µT。'),
    ('同上，拉到 3 m？', '200 ÷ 3 × (0.1 ÷ 3) ≈ 2.2 µT（文件寫約 2 µT）；仍超過交流要求。'),
    ('成對母線的距離加倍，磁場剩多少？變壓器（偶極）呢？', '成對 1/r²：剩 1/4；偶極 1/r³：剩 1/8。'),
    ('換成 800 VDC 直流母線，就不用管磁場了嗎？', '不是：直流母線產生靜磁場，改用直流 < 100 µT 判斷；配電路徑仍要重新規劃。'),
]
# 草圖要標的東西：(項目, 參考做法, 依據)
LAYOUT = [
    ('冷凍機', '放中間，四周留維護與開罐空間', '周邊簡報 p33'),
    ('壓縮機、冷卻水機', '放隔壁或室外（噪音、振動、廢熱）', '周邊簡報 p33'),
    ('變壓器', '盡量遠（偶極 1/r³ 衰減快，但近處很強）', '文獻回顧 §3.2 推論、§3.4.3'),
    ('母線', '去回線成對、緊密並行；配電走廊與量子機台保持距離', '開發計畫 §10.2'),
    ('UPS 與配電盤', '集中放置', '周邊簡報 p33'),
    ('線槽', '頂部線槽分開：微波／直流 vs 電力', '周邊簡報 p33'),
    ('鋼構、電梯', '標出位置；它們會扭曲或改變直流磁場', '文獻回顧 §3.4.3'),
    ('每段距離旁', '寫上估算的磁場與是否過關', '本課估算三步'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q135：磁場與配電佈局：母線離冷凍機多遠（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「設計改造」：孩子當配電設計師，在磁場動畫裡移動母線、切換配線方式；你當量測員，讀出冷凍機處的磁場、填紀錄表、出追問。下半場孩子替一間機房畫配電佈局草圖。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 為什麼磁場要管、三種衰減、估算三步 | 影片第 3–6 段、列印包第 2 頁（估算練習卡） |
| 25–65 | 在 `power1000.html#field` 移動母線、記錄冷凍機處的磁場 | 列印包第 1 頁、`03_磁場紀錄表.csv` |
| 65–75 | 休息 | |
| 75–105 | 畫配電佈局草圖 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：距離加倍時三種配線各剩多少、成對為什麼好 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_配電佈局草圖.pdf`（A4，共 4 頁），準備尺與三色筆（建議：紅＝超過、綠＝符合、藍＝距離與尺寸）。
- 用瀏覽器開 `animations/power1000.html#field`，先自己拉一次「與冷凍機距離」滑桿。讀一遍 `04_解答.md`。

## 量測員的原則

- 每次只讓孩子改一個旋鈕（距離、配線方式、電流、成對間距其中一個），其他先固定。
- 追問要具體：「電流加到 1,000 A，這個位置還過關嗎？」「換成單根呢？」
- 孩子若說「晶片有磁屏蔽，所以不用管」，先別糾正，請他看紀錄表上單根 360 A 在 6 m 仍有 12 µT，再談殘留磁場。

## 誠實說明

- 磁場要求（直流每軸 < 100 µT、交流 ≪ 1 µT）來自德國 LRZ 超算中心論文列出的 IQM 現場要求（依學程文件摘錄），不同廠商與機型會不同。
- 「1,000 A 單根 1 m 約 200 µT」「成對 3 m 約 2 µT」是學程供電文件的推論估算，未計鋼構與實際佈線。
- 動畫用簡化公式；交流以 0.1 µT 判斷是動畫的判斷線，變壓器偶極的係數是教學設定，不是某台變壓器的實測。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：移動母線，記錄冷凍機處的磁場（約 40 分鐘）

1. 用瀏覽器開 `animations/power1000.html#field`。預設：電流 360 A、與冷凍機距離 3.0 m、配線方式「去回線成對」、成對間距 10 cm、勾選「交流（50/60 Hz）」。
2. 讀右上角「冷凍機位置磁場 ≈ …」，紅字＝超過、綠字＝符合，填進列印包第 1 頁的紀錄表（或 `03_磁場紀錄表.csv`）。
3. 只動「與冷凍機距離」：3、6、9、1 m 各記一次。找出距離加倍時磁場剩多少。
4. 「配線方式」改「單根（淨電流不為零）」和「變壓器（近似偶極）」，同樣記 3 m 和 6 m。
5. 回到成對，把「電流」拉到 1000 A，再把「成對間距」縮到 2 cm，最後找出要拉到多遠才變綠。
6. 找出「成對、360 A」交流過關的最小距離——這是草圖的第一條規則。

## 下半場：配電佈局草圖（約 30 分鐘）

1. 在列印包第 3 頁的方格上，先畫機房外框，冷凍機放中間（每格 1 m）。
2. 決定壓縮機、冷卻水機、變壓器、UPS 與配電盤、母線走廊的位置。
3. 每段母線或變壓器到冷凍機，量出距離，用上半場的紀錄或估算三步寫下磁場，標紅或綠。
4. 寫一個改善方案和它的代價（例如：提高配電電壓降低電流、補償線圈、屏蔽）。

## 動畫對照（選做）

- `animations/power1000.html#field`：取消「交流（50/60 Hz）」，看同一個讀數改用直流 < 100 µT 判斷。
- `animations/peripherals.html#infra`：看「市電變壓器（三相）」在牆外的室外區、「配電盤」與「UPS + 電池」在另一側（3D 示意，尺寸不是公尺）。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 紀錄表參考讀數（power1000.html#field）\n\n| 配線方式 | 電流 (A) | 成對間距 (cm) | 距離 (m) | 冷凍機處磁場 | 交流判斷（0.1 µT） |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d:.1f} | {e} | {f} |\n' for a, b, c, d, e, f in READINGS)
  + '\n成對、360 A 時，大約 8.5 m 由紅轉綠（8.4 m 為 0.102 µT）。\n\n'
  + '## 估算練習參考答案\n\n' + ''.join(f'- **{q}** {a}\n' for q, a in QUIZ)
  + '\n## 配電佈局草圖要標的東西\n\n| 項目 | 參考做法 | 依據 |\n|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in LAYOUT)
  + '\n## 常見誤解\n\n'
  '- 「晶片有磁屏蔽，母線放哪都可以」：殘留磁場的要求很嚴（降溫時磁通會被困在晶片），距離仍然重要。\n'
  '- 「改成直流母線就沒有磁場問題」：直流母線產生靜磁場，要對照直流 < 100 µT；配電路徑仍要規劃。\n'
  '- 「成對配線一定抵消」：只有去回電流相等時才抵消；不平衡或地線電流會變回 1/r。\n'
  '- 「估算過關就好」：估算未計鋼構與實際佈線，要用三軸磁通門磁力計量直流與交流磁場。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/power1000.html#field`（磁場與配電佈局）

- 俯視圖：左邊是母線（或變壓器），右邊圓圈是冷凍機；色塊是磁場強度（對數，藍＝弱、紅＝強）。
- 滑桿「電流」50–2000 A；「與冷凍機距離」0.5–10 m；「成對間距」2–50 cm。
- 選單「配線方式」：單根（淨電流不為零）、去回線成對、變壓器（近似偶極）。
- 勾選「交流（50/60 Hz）」：交流以 0.1 µT 判斷；取消後用直流 < 100 µT 判斷。
- 依 B = µ₀I／2πr 等公式估算，非量測。

## `animations/peripherals.html#infra`（周邊系統 3D 場景 8：機房基礎設施，選看）

- 「市電變壓器（三相）」在牆外的室外區；「配電盤」「UPS + 電池」「隔離變壓器」在機房另一側；黃色流動的線是電力。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['次數', '配線方式', '電流 (A)', '成對間距 (cm)', '與冷凍機距離 (m)', '冷凍機處磁場 (µT)', '交流判斷（符合／超過）']
SHEET_ROWS = [[str(i)] for i in range(1, 13)]

EXTRA_CSS = '''table.rec2 td{height:10.5mm;font-size:11pt}table.rec2 th{font-size:10.5pt}
.quiz{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}
.qc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:3mm 4mm;min-height:50mm;font-size:12pt}.qc b{color:#35a9d6}
.gridmap{display:block;width:100%;height:150mm;margin-top:3mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def _grid(cols=18, rows=15):  # 方格紙（每格 1 m）；用 SVG 畫線，列印時不依賴背景圖
    lines = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{rows}" />' for x in range(1, cols)) + \
        ''.join(f'<line x1="0" y1="{y}" x2="{cols}" y2="{y}" />' for y in range(1, rows))
    return (f'<svg class="gridmap" viewBox="0 0 {cols} {rows}" preserveAspectRatio="none">'
            f'<g stroke="#c9d6e3" stroke-width="0.03">{lines}</g>'
            f'<rect x="0" y="0" width="{cols}" height="{rows}" fill="none" stroke="#0b2540" stroke-width="0.08" /></svg>')


def html():
    rows = ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 13))
    quiz = ''.join(f'<div class="qc"><b>練習 {i}</b><br>{q}<br><br>我的估算：<div class="line"></div><div class="line"></div></div>'
                   for i, (q, _) in enumerate(QUIZ, 1))
    pages = [
        '<h2>磁場紀錄表</h2><p class="lead">每次只改一個旋鈕；讀右上角「冷凍機位置磁場」，紅＝超過、綠＝符合。</p>'
        '<table class="rec2"><tr><th>#</th><th>配線方式</th><th>電流 (A)</th><th>間距 (cm)</th><th>距離 (m)</th><th>磁場 (µT)</th><th>符合？</th></tr>'
        + rows + '</table>'
        '<p class="note">規律：距離加倍，單根剩 ＿＿、成對剩 ＿＿、偶極剩 ＿＿。成對、360 A 交流過關至少要 ＿＿ m。</p>',
        f'<h2>估算練習卡</h2><p class="lead">單根：每 1,000 A、1 m 約 200 µT；成對：再乘「間距 ÷ 距離」；直流 &lt; 100 µT、交流 ≪ 1 µT（動畫以 0.1 µT 判斷）。</p><div class="quiz">{quiz}</div>',
        '<h2>換你改造：配電佈局草圖</h2><p class="lead">每格 1 m。冷凍機放中間，標出壓縮機、冷卻水機、變壓器、UPS 與配電盤、母線走廊；每段距離旁寫上估算磁場。</p>'
        + _grid() +
        '<p class="note">改善方案與代價：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡：我的配電佈局草圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 三種配線方式，距離加倍時各剩多少？</p><div class="line"></div><p>2. 為什麼成對配線比單根好？什麼時候會失效？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三種衰減：單根 1/r、成對 1/r²、偶極 1/r³</li><li>說出 LRZ 的兩個磁場門檻</li>'
        '<li>用估算三步算一次母線磁場</li><li>指出一個限制：有磁屏蔽，距離仍然重要</li>'
        '<li>替草圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q135 配電佈局草圖 列印包', '父子科技學院 量子電腦學程 Q135｜磁場與配電佈局：母線離冷凍機多遠', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q135-busbar-field-layout', folder='Q135_配電佈局草圖', files=FILES,
        sheet=('03_磁場紀錄表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_配電佈局草圖.pdf', pack_pages=4,
        pack_needles=('磁場紀錄表', '估算練習卡', '配電佈局草圖', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q135', episode_dir='specials/q135-busbar-field-layout',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'referenceReadings': len(READINGS), 'quizCards': len(QUIZ), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q135/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

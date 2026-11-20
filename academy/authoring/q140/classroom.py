"""Q140 課堂教材：逐層熱預算表、基準測試紀錄表、每瓦代價表、說明卡與解答。

不需要帳號或安裝；只要紙筆與計算機（或瀏覽器打開 animations/power1000.html#heat 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q140/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 逐層熱預算（1,000 位元、不改架構；文件 §3.1【推論】）：(層, 約溫度, 估算負載, 可用冷卻（3 單元）, 判斷)
LAYERS = [
    ('50 K', '約 35–45 K', '約 200 W', '約 150–165 W', '超過'),
    ('4 K', '約 3–4 K', '約 4.4 W＋HEMT', '約 5.4–6 W', '逼近上限'),
    ('Still（蒸餾室）', '約 0.9 K', '約 10 mW', '約 120 mW', '可'),
    ('CP（冷板）', '約 100 mK', '約 1.3 mW', '0.6–1.2 mW', '緊'),
    ('MXC 被動（混合腔）', '約 10–20 mK', '約 81 µW', '約 90 µW', '幾乎吃光'),
    ('MXC 磁通直流', '約 10–20 mK', '約 125 µW', '同上', '超過'),
]
# 每條線被動熱負載（Krinner 2019 Table 2，文件 §3.1）
PER_LINE = [
    ('驅動線（SS）', '45 mW', '1.0 mW', '4 µW', '0.4 µW', '0.013 µW'),
    ('磁通線（SS）', '56 mW', '1.2 mW', '2 µW', '0.29 µW', '0.025 µW'),
    ('輸出線（NbTi，CP 以下）', '—', '—', '—', '0.29 µW', '0.020 µW'),
]
# 基準測試方案（power1000.html#heat，1,000 位元；數值由動畫公式算出）：(方案, 最少幾組過關, 壓縮機電力, 加冷卻水, 備註)
BENCH = [
    ('不改架構（3 組）', '7 組', '87.5 kW', '52.5 kW', '3 組時 50 K、CP、MXC 磁通直流、MXC 合計超過'),
    ('只勾細同軸', '8 組也不過關', '—', '—', 'MXC 磁通直流 500 µW，被動熱降、直流熱 ×4'),
    ('只勾超導 NbTi 磁通線', '7 組', '87.5 kW', '52.5 kW', '磁通直流歸零，但 CP 仍是瓶頸'),
    ('細同軸＋NbTi', '2 組', '25.0 kW', '15.0 kW', 'CP 92%（橘黃）'),
    ('只勾低溫 CMOS＋多工', '2 組', '25.0 kW', '15.0 kW', '線 3,875 → 595 條；4 K 每位元 +1.5 mW（動畫假設）；1 組時 CP 超過'),
]
# 每瓦代價（文件 §1；粗算）
COST = [
    ('45 K（50 K 層）', '一支 PT420 約 55 W', '壓縮機 12.5 kW（與 4 K 共用）'),
    ('4 K', '同一支 PT420 約 2.0 W', '同上'),
    ('20 mK（混合腔）', '一個低溫模組 32 µW', '模組輸入約 30 kW → 每 µW 將近 1 W（粗算）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q140：低溫熱預算：熱帳怎麼變成電（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「基準測試」：固定同一台 1,000 位元的機器，一次只改一個條件，比較哪個佈線方案熱帳過關、又用最少的壓縮機電力。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 五層冷盤、逐層估算方法、熱帳怎麼變成電 | 影片第 3–7 段、列印包第 1 頁 |
| 25–65 | 在熱預算動畫逐層加總，填逐層熱預算表 | 列印包第 1 頁、`03_基準測試紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 基準測試：細同軸、超導 NbTi 磁通線、低溫 CMOS＋多工 | 列印包第 2、3 頁 |
| 105–115 | 孩子教爸爸：熱帳怎麼變成電 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_逐層熱預算.pdf`（A4，共 4 頁），準備計算機。
- 讀一遍 `04_解答.md`。用瀏覽器開 `animations/power1000.html#heat`，預設 1,000 位元、3 組稀釋單元。

## 記錄員的原則

- 一次只改一個條件，改完要把其他條件還原（或重新整理頁面）。
- 每個方案都記：熱帳過不過關、最少要幾組稀釋單元、壓縮機電力幾 kW。
- 孩子若說「多加稀釋單元就好」，先別糾正，請他把壓縮機電力念出來，再和換線材的方案比。

## 誠實說明

- 逐層負載是把 Krinner 2019（蘇黎世聯邦理工學院）每條線實測熱負載乘上參考架構線數的線性外推，學程文件標為推論，不是實機量測。
- 動畫裡低溫 CMOS「4 K 每位元 1.5 mW」、加冷卻水「約 0.6 倍」是動畫的假設值。
- 「混合腔每微瓦將近 1 瓦室溫電力」是用一個低溫模組的公開規格粗算（輸入功率包含所有層），只用來說明量級。
- peripherals.html#wiring 用的是另一個單台冷凍機的示意模型，百分比不要和 power1000 混著比。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：逐層加總熱負載（約 40 分鐘）

1. 在列印包第 1 頁的逐層熱預算表，先寫上五層：50 K、4 K、Still、CP、MXC。
2. 用每條線熱負載表（列印包第 1 頁下方）挑兩層手算：例如 50 K 層，驅動線 1,000 條 × 45 mW、磁通線 2,500 條 × 56 mW，再加讀取與泵浦。
3. 打開 `animations/power1000.html#heat`，對照七列橫條，把每一層的負載、可用冷卻、使用百分比填進表格。
4. 標出超過（紅）和逼近（橘黃）的層，寫下「要不要加脈衝管」。
5. 把「稀釋單元／脈衝管數」往上加，直到面板顯示「熱帳 過關」，記下組數和壓縮機電力。

## 下半場：基準測試（約 30 分鐘）

1. 重新整理頁面，只勾「改用 0.047" 細同軸」，記下哪一列變紅；再調稀釋單元，看能不能過關。
2. 重新整理，只勾「磁通線改用超導 NbTi」，同樣記錄。
3. 兩個一起勾，把稀釋單元往下減，找出最少幾組還能過關。
4. 重新整理，只勾「低溫 CMOS＋多工」，記下線數和 4 K 那一列。
5. 在列印包第 2 頁的紀錄表選出冠軍：熱帳過關、壓縮機電力最少。
6. 在列印包第 3 頁填每瓦代價表，寫出「越低溫，每瓦冷卻越貴」的理由。

## 動畫對照（選做）

- `animations/peripherals.html#wiring`：把「量子位元數（線束示意）」拉到 200，看右下角小圖哪一級先變紅；按「讀取輸出」看 HEMT 的位置。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 逐層熱預算（1,000 位元、不改架構；推論）\n\n| 層 | 約溫度 | 估算負載 | 可用冷卻（3 單元） | 判斷 |\n|---|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in LAYERS)
  + '\n動畫（power1000.html#heat 預設）顯示：50 K 202 W / 158 W 超過 28%；4 K 4.5 W / 5.7 W 79%；Still 10.5 mW / 120 mW 9%；CP 1.3 mW / 600 µW 超過 115%；'
  'MXC 被動 81.3 µW / 90.0 µW 90%；MXC 磁通直流 125 µW / 90.0 µW 超過 39%；MXC 合計 206 µW / 90.0 µW 超過 129%；熱帳不過關；壓縮機電力 37.5 kW。\n\n'
  + '## 每條線被動熱負載（Krinner 2019）\n\n| 線 | 50 K | 4 K | Still | CP | MXC |\n|---|---|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in PER_LINE)
  + '\n手算範例：50 K 層＝驅動類（XY 1,000＋讀取輸入 125＋泵浦 125）× 45 mW ＋ 磁通 2,500 × 56 mW ＋ 讀取輸出 125 × 45 mW ≈ 56.25＋140＋5.6 ≈ 202 W。\n\n'
  + '## 基準測試參考結果（1,000 位元）\n\n| 方案 | 最少幾組過關 | 壓縮機電力 | 加冷卻水 | 備註 |\n|---|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in BENCH)
  + '\n並列冠軍：細同軸＋NbTi 磁通線、低溫 CMOS＋多工，都是 2 組過關、壓縮機 25 kW，比硬撐的 7 組（87.5 kW）少 62.5 kW；兩者瓶頸不同（前者 CP 92%，後者 CP 59%），可以再加碼比 N 往上調時誰先不過關。\n\n'
  + '## 每瓦代價\n\n| 層 | 冷卻 | 室溫電力 |\n|---|---|---|\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in COST)
  + '\n## 常見誤解與注意事項\n\n'
  '- 「冷卻不夠就多加稀釋單元」：可以過關，但每組多一台約 12.5 kW 壓縮機，還要加冷卻水；換線材常常更省。\n'
  '- 「細線一定比較好」：被動熱降近 4 倍，但不鏽鋼磁通線的直流熱反而變 4 倍，磁通線要改走超導線。\n'
  '- 「每一層的 1 瓦都一樣」：越低溫，每瓦冷卻要付出的室溫電力越多；混合腔只有幾十 µW 可用。\n'
  '- 「這些是量測值」：是每條線實測值乘上線數的線性外推，屬推論。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/power1000.html#heat`（低溫熱預算）

- 左邊：冷凍機示意，五層冷盤（50 K、4 K、Still、CP、MXC）與量子晶片。
- 右邊：七列橫條（50 K、4 K、Still、CP、MXC 被動、MXC 磁通直流、MXC 合計），白色虛線＝可用冷卻上限；紅＝超過、橘黃＝超過 75%。
- 控制項：「量子位元數 N」（100–3,000）、「稀釋單元／脈衝管數」（1–8 組）、「改用 0.047" 細同軸」、「磁通線改用超導 NbTi」、「容忍 CP 200 mK、MXC 30 mK」、「低溫 CMOS＋多工（4 K 每位元 1.5 mW）」。
- 面板：進冷凍機的線、壓縮機電力（每組 12.5 kW）、加冷卻水（約 0.6×）、熱帳過關／不過關。

## `animations/peripherals.html#wiring`（低溫佈線 3D）

- 六條線：XY 驅動、Z 磁通、讀取輸入、TWPA 泵浦、讀取輸出、直流線束；按名稱可聚焦單一條線，看各級元件。
- 「量子位元數（線束示意）」1–200；右下角小圖是各級熱負載 / 可用冷卻（示意估算）。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['方案', '勾了哪些', '稀釋單元幾組', '哪一列最紅', '熱帳過關嗎', '壓縮機電力 kW', '加冷卻水 kW']
SHEET_ROWS = [[r[0], '', '', '', '', '', ''] for r in BENCH] + [['自訂方案 1', '', '', '', '', '', ''], ['自訂方案 2', '', '', '', '', '', '']]

EXTRA_CSS = '''table.rec td{height:11mm}table.small td,table.small th{font-size:10pt;padding:1mm 2mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    layer_rows = ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td></tr>' for r in LAYERS[:5])
    per_line = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in PER_LINE)
    bench_rows = ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td></tr>' for r in BENCH)
    cost_rows = ''.join(f'<tr><td>{r[0]}</td><td></td><td></td></tr>' for r in COST)
    pages = [
        '<h2>逐層熱預算表</h2><p class="lead">1,000 位元、3 組稀釋單元。每一層填負載、可用冷卻、使用百分比，再判斷要不要加脈衝管。</p>'
        '<table class="rec"><tr><th>層</th><th>負載</th><th>可用冷卻</th><th>使用 %</th><th>要加脈衝管嗎？</th></tr>' + layer_rows
        + '<tr><td>MXC 磁通直流</td><td></td><td></td><td></td><td></td></tr></table>'
        '<h3 style="margin-top:4mm">每條線被動熱負載（Krinner 2019 實測）</h3>'
        '<table class="small"><tr><th>線</th><th>50 K</th><th>4 K</th><th>Still</th><th>CP</th><th>MXC</th></tr>' + per_line + '</table>'
        '<p class="note">線數：XY 驅動 1,000、磁通 2,500、讀取輸入／輸出／泵浦各 125（參考架構，推論）。</p>',
        '<h2>基準測試紀錄表</h2><p class="lead">位元數固定 1,000。一次只改一個條件；記下最少幾組稀釋單元過關、壓縮機電力。</p>'
        '<table class="rec"><tr><th>方案</th><th>最少幾組過關</th><th>壓縮機 kW</th><th>冷卻水 kW</th><th>哪一列最難</th></tr>' + bench_rows
        + '<tr><td>自訂方案</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p class="note">冠軍：熱帳過關、壓縮機電力最少的方案是＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>越低溫，每瓦越貴</h2><p class="lead">同樣的室溫電，往下層換到的冷卻越來越少。</p>'
        '<table class="rec"><tr><th>層</th><th>能帶走多少熱</th><th>要付多少室溫電</th></tr>' + cost_rows + '</table>'
        '<div class="box" style="height:55mm;margin-top:5mm"><p class="note">用自己的話寫：為什麼混合腔省下幾 µW 也不能小看？</p></div>',
        '<h2>說明卡：我的逐層熱預算表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 熱預算為什麼要一層一層算？</p><div class="line"></div><p>2. 熱帳不過關，怎麼變成室溫用電？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個注意事項或限制：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出五層冷盤與逐層估算方法（線數 × 每條熱）</li><li>指出 1,000 位元不改架構時超過的兩層：50 K 與 MXC</li>'
        '<li>解釋加脈衝管＝加壓縮機＋冷卻水</li><li>說出注意事項：越低溫，每瓦冷卻越貴；數字是推論</li>'
        '<li>替熱預算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q140 逐層熱預算 列印包', '父子科技學院 量子電腦學程 Q140｜低溫熱預算：熱帳怎麼變成電', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q140-cryo-heat-budget', folder='Q140_低溫熱預算', files=FILES,
        sheet=('03_基準測試紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_逐層熱預算.pdf', pack_pages=4,
        pack_needles=('逐層熱預算表', '每條線被動熱負載', '基準測試紀錄表', '每瓦越貴', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q140', episode_dir='specials/q140-cryo-heat-budget',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'layers': len(LAYERS), 'benchmarks': len(BENCH), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q140/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

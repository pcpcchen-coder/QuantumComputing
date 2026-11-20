"""Q134 課堂教材：接地拓樸比較圖底稿、證人線索卡、儀器數記錄表、改造方案、說明卡與解答。

不需要帳號或安裝；只要紙筆，加上瀏覽器打開 animations/power1000.html#ground 做記錄（離線即可）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q134/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 接地拓樸：(拓樸, 怎麼接, 好處, 代價／限制)
TOPOLOGIES = [
    ('單點（星形）接地', '每台設備各拉一條線回到同一個接地點', '低頻沒有迴路', '設備分散數公尺時，高頻失效（長地線像電感與天線）；10–20 個機櫃很難做到（推論）'),
    ('網狀接地', '多點互相導通，形成一張接地網（資料中心常見）', '高頻阻抗低', '刻意製造大量迴路；和量子機台需要的單點接地衝突'),
    ('混合接地', '低頻照星形、高頻照網狀；例如屏蔽一端直接接地、另一端經電容接地', '兼顧低頻與高頻', '要依頻段設計；施工與驗證複雜'),
    ('量子區（技術接地）', '量子區有獨立的技術接地，只在一點接回建築接地', '把量子機台和資料中心接地網隔開', '冷卻水管、氦氣管要加絕緣段；比較像工程服務加參考設計'),
]
# 儀器數記錄表的參考值（power1000.html#ground，每台 0.75 mA、接地阻抗 5 mΩ）：(台數, 地線電流, 地電位差)
COUNTS = [(10, '0.007 A', '38 µV'), (50, '0.037 A', '188 µV'), (100, '0.075 A', '375 µV'),
          (250, '0.188 A', '938 µV'), (400, '0.300 A', '1.50 mV')]
CLUES = [  # (證人的線索, 參考推理)
    ('同一台儀器有時正常、有時出錯；動一下同軸接頭，好像就好了。', '接頭鬆脫或接觸電阻變大，屏蔽層上的接地迴路電流轉成訊號雜訊，而且時有時無。'),
    ('上個月多裝了一整櫃儀器，之後偏壓雜訊變大。', '交流入口變多，每台合規的漏電流加總，地線電流與地電位差跟著變大。'),
    ('機櫃前已經加了隔離變壓器，問題還在。', '繞組間電容讓高頻共模漏過去；同軸線一接到冷凍機，迴路又被接回來。'),
    ('換了一批新的隔離 DC-DC 模組，共模尖峰變大。', '隔離電容較大：I = C·dV/dt，電容越大尖峰越大，走地線與屏蔽、繞過差模濾波器。'),
    ('冷凍機的冷卻水管和氦氣軟管都是金屬的。', '管路也是接地路徑，把冷凍機接回建築；要做單點接地，管路要加絕緣段。'),
    ('機房是資料中心的網狀接地網。', '網狀接地刻意製造迴路，和量子機台的單點接地衝突；可考慮量子區，只在一點接回。'),
    ('乾脆把儀器的地線拔掉吧？', '不行：安規要求外殼接保護地線，只能用隔離、絕緣段、混合接地處理。'),
]
IMPROVE = [  # (改善方案, 好處, 代價)
    ('機櫃集中供電（一櫃 1–2 個交流入口）', '交流入口從數百個降到十幾個，漏電流路徑大幅減少', '儀器廠要改機箱與電源入口；共用母線可能造成模組間串擾'),
    ('壓低每台漏電流（少放 Y 電容、醫療級電源）', '每個入口漏得少', '少 Y 電容，EMC 傳導干擾測試變難'),
    ('低隔離電容的隔離 DC-DC', '共模尖峰變小', '低隔離電容與效率、體積衝突'),
    ('量子區＋混合接地', '把量子機台和建築接地網隔開；兼顧高低頻', '管路加絕緣段；施工與驗證要另外做'),
    ('接地電流監測 PDU', '每個插座的接地電流看得見，可和校準異常做時間對照', '只量不減；要量 mA 以下的剩餘電流，精度是挑戰'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q134：接地與共模——上百台儀器一起漏電（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天玩「偵探辦案」：孩子當偵探，在接地動畫裡把儀器一台一台加上去，追出地線裡的雜訊；你當證人，提供線索。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三條電流路徑、共模電流的四站、100 vs 1,000 位元、三種接地拓樸 | 影片第 3–8 段、列印包第 1 頁 |
| 25–65 | 在 `power1000.html#ground` 增加儀器數、記錄；證人出線索 | 列印包第 2、3 頁、`03_儀器數記錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 提出一種接地拓樸改善方案，畫進比較圖並寫出取捨 | 列印包第 1、3 頁 |
| 105–115 | 孩子教爸爸：為什麼儀器越多，地電位差越大 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_接地與共模.pdf`（A4，共 4 頁），準備紅、橘、綠三色筆（建議：紅＝保護地線電流、橘＝同軸屏蔽、綠＝建築接地）。
- 用瀏覽器開 `animations/power1000.html#ground` 試拉一次「交流入口（儀器台數）」滑桿；讀一遍 `04_解答.md`。

## 證人的原則

- 一次只給一條線索（列印包第 2 頁），讓孩子先說「電流走哪一條路」，再說「怎麼改」。
- 答不出來不扣分：請孩子回到動畫拉一拉滑桿，或在比較圖上補一條路徑。
- 孩子若說「拔掉地線就好」，用第 7 張線索卡提醒安規。

## 誠實說明

- 250–350 個交流入口、0.1–0.35 A、0.1–3.5 mV、10–20 個機櫃，是學程設計文件的推論估算，不是量測。
- 動畫的地電位差 = 台數 × 每台漏電流 × 接地阻抗，是教學用的簡化模型；真實機房的電流分配在地線與屏蔽之間，也和頻率有關。
- 常見誤解：單點接地在大系統不一定可行，要依頻段設計。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：增加儀器數，觀察共模電流（約 40 分鐘）

1. 開 `animations/power1000.html#ground`，先不要動「每台漏電流」與兩個勾選框。
2. 把「交流入口（儀器台數）」依序拉到 10、50、100、250、400 台，每次在列印包第 3 頁（或 `03_儀器數記錄.csv`）記下「地線電流」「地電位差」。
3. 算一算：台數變成 10 倍時，地電位差變成幾倍？
4. 把台數固定在 400，「接地阻抗」從 5 拉到 1 mΩ，再記一次。地電位差有沒有低於 µV 級？
5. 把「隔離 DC-DC 的隔離電容」從 100 拉到 1000、再拉到 2 pF，記下「共模尖峰」；地電位差有沒有跟著變？
6. 證人（爸爸）讀線索卡（列印包第 2 頁），偵探在比較圖上指出電流走哪一條路。

## 下半場：接地拓樸改善方案（約 30 分鐘）

1. 在列印包第 1 頁的三欄，畫出單點、網狀、混合接地的示意圖，各寫一個好處與一個代價。
2. 從列印包第 3 頁下方挑一種改善方案，寫進比較圖：它減少了哪一條路的電流？代價是什麼？
3. 寫一句限制：為什麼單點接地在 10–20 個機櫃的大系統不一定可行？

## 動畫對照（選做）

- `animations/power1000.html#scale`：拉「量子位元數 N」到 100、1,000、10,000，看「交流入口（儀器）」與「地線電流總和」。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 儀器數記錄表參考值（每台 0.75 mA、接地阻抗 5 mΩ）\n\n| 台數 | 地線電流 | 地電位差 |\n|---|---|---|\n'
  + ''.join(f'| {n} | {a} | {b} |\n' for n, a, b in COUNTS)
  + '\n台數 10 → 100 倍數為 10；地電位差與台數成正比。400 台、接地阻抗 1 mΩ：約 300 µV，仍遠大於 µV 級。\n'
  '隔離電容 100 pF → 共模尖峰 0.24 A；1000 pF → 2.40 A；2 pF → 4.8 mA（I = C × 48 V／20 ns）。地電位差不跟著變，因為動畫裡它只由台數、漏電流與接地阻抗決定。\n\n'
  + '## 三種接地拓樸\n\n| 拓樸 | 怎麼接 | 好處 | 代價／限制 |\n|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in TOPOLOGIES)
  + '\n## 證人線索參考推理\n\n' + ''.join(f'- **{q}** {a}\n' for q, a in CLUES)
  + '\n## 改善方案的取捨\n\n| 方案 | 好處 | 代價 |\n|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in IMPROVE)
  + '\n## 常見誤解\n\n'
  '- 「單點接地一定最好」：設備分散數公尺時，星形接地只在低頻有效；MHz 以上要網狀或平面接地，所以要依頻段設計（混合接地）。\n'
  '- 「加隔離變壓器就斷開迴路了」：繞組電容讓高頻漏過，同軸線又把迴路接回來。\n'
  '- 「每台都合規就沒事」：合規的漏電流乘上數百台，就是 mV 等級的地電位差（文件推論）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/power1000.html#ground`（接地與共模）

- 滑桿：「交流入口（儀器台數）」10–400、「每台漏電流」0.1–3.5 mA、「接地阻抗」1–20 mΩ、「隔離 DC-DC 的隔離電容」2–1000 pF。
- 勾選：「機櫃集中供電（每櫃一個交流入口）」「量子等級隔離 DC-DC（隔離電容 ≤ 10 pF）」（上半場先不勾，下半場改造時可以試）。
- 紅點＝保護地線上的接地電流；橘色路徑＝同軸屏蔽層（迴路的另一半）。
- 黑框：交流入口 × 漏電流、地線電流、地電位差（偏壓要求 µV 級）、每顆 DC-DC 共模尖峰。

## `animations/power1000.html#scale`（規模計算器）

- 拉「量子位元數 N」，看「交流入口（儀器）」與「地線電流總和」怎麼跟著變；白色虛線是 1,000 位元參考門檻。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['設定', '交流入口（台）', '接地阻抗（mΩ）', '隔離電容（pF）', '地線電流', '地電位差', '共模尖峰', '我的觀察']
SHEET_ROWS = ([[f'加儀器 {i}', str(n), '5', '100'] for i, (n, _, _) in enumerate(COUNTS, 1)]
              + [['降接地阻抗', '400', '1', '100'], ['隔離電容大', '250', '5', '1000'], ['隔離電容小', '250', '5', '2'],
                 ['我的改造', '', '', '']])

EXTRA_CSS = '''.topo{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:3mm}
.tc{border:1.3pt dashed #0b2540;border-radius:3mm;padding:2mm 3mm;min-height:120mm;font-size:11pt;color:#4a6a88}
.tc b{color:#0b2540;font-size:12pt}.tc .draw{height:62mm;border-bottom:.9pt dotted #7f9bb3;margin-bottom:2mm}
.quiz{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm;margin-top:3mm}
.qc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:2.5mm 4mm;min-height:44mm;font-size:11.5pt}.qc b{color:#35a9d6}
table.rec td{height:9mm}.imp{font-size:10.5pt;margin:2mm 0 0;padding-left:5mm}.imp li{margin:.8mm 0}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    topo = ''.join(f'<div class="tc"><b>{t}</b><div class="draw"></div>好處：<div class="line"></div>代價：<div class="line"></div></div>'
                   for t in ('單點（星形）接地', '網狀接地', '混合接地'))
    clues = ''.join(f'<div class="qc"><b>線索 {i}</b><br>{q}<br><br>電流走哪一條路？<div class="line"></div></div>'
                    for i, (q, _) in enumerate(CLUES, 1))
    rows = ''.join(f'<tr><td>{n} 台</td><td>5</td><td></td><td></td></tr>' for n, _, _ in COUNTS) \
        + '<tr><td>400 台</td><td>1</td><td></td><td></td></tr>'
    imp = ''.join(f'<li>{a}</li>' for a, *_ in IMPROVE)
    pages = [
        '<h2>接地拓樸比較圖（底稿）</h2><p class="lead">畫出三種接地拓樸，各寫一個好處和一個代價。紅＝保護地線電流、橘＝同軸屏蔽、綠＝建築接地。</p>'
        f'<div class="topo">{topo}</div>'
        '<p class="note">提示：單點接地在大系統不一定可行，要依頻段設計。</p>',
        f'<h2>證人線索卡</h2><p class="lead">證人（爸爸）一次讀一張，偵探（你）說出電流走哪一條路、可以怎麼改。</p><div class="quiz">{clues}</div>',
        '<h2>儀器數記錄表</h2><p class="lead">在 power1000.html#ground 拉「交流入口（儀器台數）」，每台漏電流保持 0.75 mA。</p>'
        '<table class="rec"><tr><th>交流入口</th><th>接地阻抗（mΩ）</th><th>地線電流</th><th>地電位差</th></tr>' + rows + '</table>'
        '<p class="note">台數變 10 倍，地電位差變幾倍？＿＿＿＿　隔離電容 1000 pF 的共模尖峰：＿＿＿＿　2 pF：＿＿＿＿</p>'
        f'<h3 style="margin-top:4mm">換你改造：挑一種接地改善方案</h3><ul class="imp">{imp}</ul>'
        '<p>我選：＿＿＿＿＿＿＿＿＿＿　它減少了哪一條路的電流？＿＿＿＿＿＿＿＿＿＿</p><p>代價：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡：我的接地拓樸比較圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 共模電流從哪裡漏出來？走哪兩條路到冷凍機？</p><div class="line"></div><p>2. 為什麼儀器越多，地電位差越大？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三條電流路徑：Y 電容、同軸屏蔽、隔離電容</li><li>解釋放大：地電位差 ≈ 台數 × 漏電流 × 接地阻抗</li>'
        '<li>分辨單點、網狀、混合接地</li><li>指出一個限制：單點接地在大系統不一定可行，要依頻段設計</li>'
        '<li>替比較圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q134 接地與共模 列印包', '父子科技學院 量子電腦學程 Q134｜接地與共模：上百台儀器一起漏電', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q134-grounding-common-mode', folder='Q134_接地與共模', files=FILES,
        sheet=('03_儀器數記錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_接地與共模.pdf', pack_pages=4,
        pack_needles=('接地拓樸比較圖', '證人線索卡', '儀器數記錄表', '換你改造', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q134', episode_dir='specials/q134-grounding-common-mode',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'topologies': len(TOPOLOGIES), 'clueCards': len(CLUES), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q134/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q136 課堂教材：離子阱供電需求表底稿、偵探線索卡、毫秒級備援說明單、說明卡與解答。

不需要帳號或安裝；只要紙筆（或瀏覽器打開 animations/atoms.html#ionsys 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q136/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 需求表：(子系統, 用電特性, 精密要求, 可容忍中斷／層級, 出處)
SUBSYSTEMS = [
    ('阱 RF 驅動（RF 源、放大器、螺旋共振器）', '模型取約 10 W（Góis 2024）', '振幅 ppm 級（文獻 200 s 內優於 5 ppm）', 'T0：0 ms', '簡報 p30、p32；文件 §8.1'),
    ('DC 電極 DAC（多通道）', '每電極約 30 mW（架構模型）', '< 100 nV/√Hz，再濾波壓 10⁵ 倍；µs 級更新', 'T0：0 ms', '簡報 p30、p33；文件 §8.2'),
    ('時序 FPGA、銣鐘（10 MHz）', '中', '10 MHz 參考與時序不能斷', 'T0：0 ms', '簡報 p30、p35'),
    ('雷射驅動與鎖頻電子（5–10 台）', '單台不大但數量多', '1 MHz 線寬需積分電流雜訊 ≤ 300 nA', 'T1：毫秒～秒', '簡報 p33；文件 §8.4'),
    ('磁場線圈電流源', '小', '電流 ppm 級；怕 50/60 Hz 與 150／250 Hz 諧波', 'T0 或 T1（文件未分層；請孩子自己判斷）', '簡報 p30、p34；文件 §8.3'),
    ('精密空調、雷射冷卻水', '小型系統可能是最大用電項（約 78%，待核對）', '光學桌 ±0.1 °C', 'T2：數分鐘', '簡報 p31、p35；文件 §7.1'),
    ('離子泵控制器、真空計', '小', 'NEG 可撐住', 'T3：數小時', '簡報 p35；文件 §9.1'),
]
CLUES = [  # (線索卡問題, 參考答案與出處)
    ('Helios 官方基本機組用電多少？', '< 40 kW（官方）；Oracle 合作資料約 60 kW，差異沒有官方說明（簡報 p31）。'),
    ('小型離子阱用電的大宗是什麼？這個數字可靠嗎？', '環境控制（雷射用空調）約 78%；二手摘要，原文未能核對，只當量級參考（簡報 p31）。'),
    ('RF 振幅漂 1 ppm，會發生什麼事？', '徑向模態頻率也漂約 1 ppm，MS 雙位元閘失諧（簡報 p32；文件 §8.1）。'),
    ('DC 電極為什麼不能只靠重濾波？', 'QCCD 要 µs 級更新電壓，濾波越重搬運越慢；DAC 與電源本身要安靜（簡報 p33；文件 §8.2）。'),
    ('雷射要 1 MHz 線寬，電流雜訊要多小？', '積分電流雜訊 ≤ 300 nA（二極體約 3 MHz/µA）（簡報 p33；文件 §8.4）。'),
    ('150 Hz、250 Hz 的磁場雜訊從哪裡來？', '電腦、螢幕電源的二極體整流（非線性負載）產生的奇次諧波（簡報 p34；文件 §8.3）。'),
]
COMPARE = [  # (比較項目, 超導, 離子阱)
    ('最怕斷電的設備', '冷卻鏈（壓縮機、冷卻水、GHS）', '阱 RF、DC 電極 DAC、時序、銣鐘'),
    ('可容忍的中斷', '約 2 分鐘（LRZ 數據點）', '0 ms（推論：連一個週期都不能斷）'),
    ('斷了之後', '約 2 分鐘超過 1 K，重新降溫 2–5 天', '離子立刻逃逸，重新裝載與校準約數十分鐘～數小時'),
    ('UPS 的任務', '撐到發電機接手', '零切換時間；加設備端直流保持'),
    ('UPS 總容量', '大（壓縮機是最大負載）', '較小，但對切換時間與電源品質更嚴'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q136：離子阱的供電：ppm 與 nV（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「資料偵探」：孩子當偵探，從簡報與文件找出離子阱每一路電源的數字，填進供電需求表；你當證人兼審查員，追問每個數字的出處。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 用電大宗、四路精密電源、三個精密數字、市電諧波、備援四層 | 影片第 3–8 段、列印包第 1 頁 |
| 25–65 | 整理離子阱供電需求表；爸爸用線索卡追問出處 | 列印包第 1、2 頁、`03_線索紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 寫出「為什麼離子阱要毫秒級備援」 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：三個數字各屬哪一路、為什麼 RF 不能斷 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_離子阱供電.pdf`（A4，共 4 頁），準備紅、藍兩色筆（紅＝零中斷那一層，藍＝其他層）。
- 讀一遍 `04_解答.md`。想看動畫的話，用瀏覽器開 `animations/atoms.html#ionsys`（系統全景）、`#paul`（Paul 阱）、`#qccd`（搬運架構）。
- 素材：供電簡報（`slides/output/qc-power-supply.pptx`）第 30–37 頁；離子阱簡報（`slides/Ion_NeutralAtom_Talk.pptx`）第 11 頁。

## 證人的原則

- 每填一格就問兩件事：「哪一頁寫的？」「是量測，還是推論？」
- 找不到出處不扣分，先在格子旁打問號；第 2 張線索卡的 78% 本來就標著「待核對」。
- 孩子若把離子阱的備援說成「撐兩分鐘」，先別糾正，請他到動畫 `#paul` 按「RF 開 / 關」，看離子怎麼跑掉。

## 誠實說明

- 「T0–T3 四層」「RF 與 DC 連一個週期都不能斷」「恢復約數十分鐘到數小時」是學程文件的推論與估計，不是量測。
- 外部論文的數字（5 ppm、100 nV/√Hz、300 nA、約 25 倍、150／250 Hz）依學程文獻回顧的摘錄，原文未重新開啟。
- 動畫裡的典型用電長條（10／6／5／7／0.2 kW）是示意值。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：離子阱供電需求表（約 40 分鐘）

1. 在列印包第 1 頁的表格，第一欄已列出七個子系統。
2. 偵探（孩子）翻供電簡報第 30–37 頁與離子阱簡報第 11 頁，為每一列填：用電特性、精密要求、可容忍中斷（T0／T1／T2／T3）、出處頁碼。
3. 證人（爸爸）每填一格就追問出處；量測值寫「測」，推論寫「推」，找不到寫「？」。
4. 用紅筆圈出 T0 零中斷那一層的所有子系統。
5. 用列印包第 2 頁的六張線索卡互考；答案與出處記在 `03_線索紀錄.csv`。

## 下半場：為什麼是毫秒級備援（約 30 分鐘）

1. 在列印包第 3 頁的比較表，填超導和離子阱的五個比較項目。
2. 用三句話寫出「為什麼離子阱要毫秒級備援」：誰不能斷、斷了會怎樣、該怎麼供電。
3. 加分題：電壓驟降比完全停電更常見，T0 和 T1 的設備要怎麼設計？

## 動畫對照（選做）

- `animations/atoms.html#ionsys`：右下角典型用電示意；按「只看設施」「只看電子訊號」。
- `animations/atoms.html#paul`：拖「q 參數」看 secular 頻率；按「RF 開 / 關」看離子逃逸。
- `animations/atoms.html#qccd`：按「▶ 執行一段線路」，看 DC 電極亮起與搬運時間。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 離子阱供電需求表\n\n| 子系統 | 用電特性 | 精密要求 | 可容忍中斷 | 出處 |\n|---|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in SUBSYSTEMS)
  + '\n磁場線圈：文件把它列在「電流 ppm 級、怕諧波」，但 §9.2 的四層表沒有列入。孩子若放在 T0 或 T1，只要說得出理由（線圈電流一跳，量子位元頻率就變）都算對。\n\n'
  + '## 線索卡參考答案\n\n' + ''.join(f'- **{q}** {a}\n' for q, a in CLUES)
  + '\n## 超導 vs 離子阱的備援\n\n| 比較項目 | 超導 | 離子阱 |\n|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in COMPARE)
  + '\n## 常見誤解\n\n'
  '- 「離子阱沒有冷凍機，所以供電不重要」：要精密控制的電源反而更多（RF、數十到上千路 DC、5–10 台雷射、線圈）。\n'
  '- 「UPS 撐得住就好」：T0 層要的是零切換時間；雙轉換 UPS 之外，設備端還要直流保持，連 UPS 故障旁路都不掉電（推論）。\n'
  '- 「市電沒停電就沒事」：電腦、螢幕的整流諧波（150／250 Hz）會變成背景磁場雜訊；市電諧波是離子阱的頭號敵人。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/atoms.html#ionsys`（離子阱系統全景）

- 右下角「典型用電（示意；Quantinuum Helios 官方 < 40 kW）」：空調 / 冷卻水 ~10 kW 最大。
- 按鈕「全部」「只看雷射」「只看電子訊號」「只看設施」：設施模式看 UPS / 配電盤、冷卻水機、恆溫空調的連線；電子訊號模式看 RF（紅）、DC（橘）。

## `animations/atoms.html#qccd`（QCCD 搬運架構）

- 「▶ 執行一段線路」：離子經過的分段 DC 電極會亮起橘色；右下角小圖是一層線路的時間組成。

## `animations/atoms.html#paul`（Paul 阱原理）

- 「q 參數」滑桿：secular 頻率 ≈ qΩ/(2√2)，和 q 成正比。
- 「RF 開 / 關」：關掉 RF，鞍形位勢消失，離子逃逸。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['線索卡', '問題', '偵探的答案', '出處（簡報頁或文件章節）', '量測／推論／待核對']
SHEET_ROWS = [[f'線索 {i}', q] for i, (q, _) in enumerate(CLUES, 1)] + [['自訂線索 1', ''], ['自訂線索 2', '']]

EXTRA_CSS = '''table.req td{height:15mm;font-size:10.5pt}table.req td:first-child{width:46mm}
.quiz{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}
.qc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:3mm 4mm;min-height:52mm;font-size:12pt}.qc b{color:#35a9d6}
table.rec td{height:14mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    req = ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td></tr>' for r in SUBSYSTEMS)
    clue = ''.join(f'<div class="qc"><b>線索 {i}</b><br>{q}<br><br>答案與出處：<div class="line"></div><div class="line"></div></div>'
                   for i, (q, _) in enumerate(CLUES, 1))
    pages = [
        '<h2>離子阱供電需求表（底稿）</h2><p class="lead">每一列填用電、精密要求、可容忍中斷（T0／T1／T2／T3）與出處。用紅筆圈出 T0 零中斷那一層。</p>'
        '<table class="req"><tr><th>子系統</th><th>用電特性</th><th>精密要求</th><th>可容忍中斷</th><th>出處</th></tr>'
        f'{req}</table>'
        '<p class="note">提示：三個單位——ppm（RF 振幅）、nV/√Hz（DC 電極）、nA（雷射電流）。量測寫「測」，推論寫「推」，找不到寫「？」。</p>',
        f'<h2>偵探線索卡</h2><p class="lead">證人（爸爸）讀線索，偵探（你）找答案，並說出是哪一頁寫的。</p><div class="quiz">{clue}</div>',
        '<h2>換你改造：為什麼是毫秒級備援</h2><p class="lead">比較超導和離子阱，再用三句話寫出理由。</p>'
        '<table class="rec"><tr><th>比較項目</th><th>超導</th><th>離子阱</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td></td><td></td></tr>' for r in COMPARE) + '</table>'
        '<h3 style="margin-top:5mm">我的三句話</h3>'
        '<div class="box"><p>1. 誰不能斷：</p><div class="line"></div><p>2. 斷了會怎樣：</p><div class="line"></div><p>3. 該怎麼供電：</p><div class="line"></div></div>'
        '<p class="note">加分題：電壓驟降比完全停電更常見，T0 和 T1 的設備要怎麼設計？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡：我的離子阱供電需求表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. ppm、nV、nA 各是哪一路電源的要求？</p><div class="line"></div><p>2. 為什麼 RF 那一路一刻都不能斷？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出四路精密電源：阱 RF、DC 電極、雷射電流、線圈電流</li><li>說出三個數字：ppm、nV/√Hz、nA 各屬哪一路</li>'
        '<li>解釋為什麼 T0 要零切換時間</li><li>指出一個陷阱：市電諧波（150／250 Hz）是頭號敵人</li>'
        '<li>替需求表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q136 離子阱的供電 列印包', '父子科技學院 量子電腦學程 Q136｜離子阱的供電：ppm 與 nV', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q136-ion-trap-power', folder='Q136_離子阱供電', files=FILES,
        sheet=('03_線索紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_離子阱供電.pdf', pack_pages=4,
        pack_needles=('需求表', '子系統', '偵探線索卡', '毫秒級備援', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q136', episode_dir='specials/q136-ion-trap-power',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'subsystems': len(SUBSYSTEMS), 'clueCards': len(CLUES), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q136/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q141 課堂教材：擴展用電比較表、答辯追問卡、低溫電源轉換困難卡、說明卡與解答。

不需要帳號或安裝；只要紙筆（或瀏覽器打開 animations/power1000.html#scale、#devplan 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q141/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 擴展用電比較表：(負載, 1,000 位元（文件 §4.1，推論）, 10,000 位元參考（推論）, 依據)
COMPARE = [
    ('脈衝管壓縮機', '37.5–62.5 kW', '30–60 台等級（每台約 12.5 kW → 約 375–750 kW）', '§4.1 3–5 支 × 12.5 kW；§7 壓縮機群 30–60 台'),
    ('氣體處理系統與泵', '3–5 kW', '隨冷凍機台數增加（文件未給數字）', '§4.1'),
    ('壓縮機冷卻水', '15–40 kW', '隨壓縮機增加（文件未給數字）', '§4.1；Google：冷卻水另需 10 kW 以上'),
    ('低溫系統合計（模組化）', '—', '12 × 30 kW ≈ 360 kW（僅低溫）', '§7；IBM Starling 約 12 個模組（報導）'),
    ('室溫控制電子', '10–100 kW', '每位元 10–100 W × 10,000 → 100–1,000 kW（線性外推）', '§4.1 每位元 10–100 W'),
    ('低溫 CMOS（4 K 熱負載）', '—', '10–20 W 在 4 K（每位元 1–2 mW）', '§7；簡報 p55'),
    ('精密直流源', '3–7 kW', '隨通道數增加（文件未給數字）', '§4.1 105–125 台 × 30–60 W；§5'),
    ('即時解碼（FPGA／GPU）', '5–50 kW', '依錯誤更正規模（文件未給數字）', '§4.1；§7 必須緊鄰機台'),
    ('電子區空調', '5–50 kW', '約電子熱負載的 30–50%', '§4.1'),
    ('設施合計', '約 80–320 kW（中點約 200 kW）', 'MW 級量子資料中心', '§4.1；§7；文獻回顧 §4（推論）'),
]
QUIZ = [  # (評審的追問, 參考答案)
    ('200 kW 是量出來的嗎？', '不是。是文件把八類負載各估低值和高值，再取中點相加的推論。'),
    ('一萬位元為什麼是 MW 級？', '模組化冷凍機約 12 × 30 kW ≈ 360 kW 只是低溫系統；壓縮機 30–60 台等級，再加控制電子、解碼、空調。'),
    ('每位元控制電子省到 10 W，一萬位元還是 MW 級嗎？', '規模計算器（推論模型）算出約 1,388 kW，仍是 MW 級；壓縮機 487.5 kW 不變。'),
    ('模組數多一倍，總功率會怎樣？', '低溫系統約跟著模組數線性增加（每模組約 30 kW）；其他項目要另外估。'),
    ('為什麼要高電壓、低電流送進冷凍機？', '線材帶進去的熱負載和電流有關；低電流送入，到低溫端再降壓。'),
    ('91.6% 這個數字可靠嗎？', '是廠商（EPC）文章的數字，正式論文待確認；答辯時要說出來。'),
]
DIFFICULTIES = [  # (困難, 卡住什麼, 可能的解法, 代價或注意)
    ('損耗吃掉 4 K 冷卻預算', '效率 90% 供 10 W 要多散 1.1 W；4 K 每支脈衝管只有約 2 W', '效率目標高於室溫產品；或放在 50 K 層', '50 K 層再送到 4 K，要權衡線損與熱導'),
    ('磁性元件低溫特性改變', '多數鐵氧體的磁導率在低溫大幅下降', '空心電感、低溫適用磁性材料、開關電容拓撲', '要重新驗證；材料選擇變少'),
    ('電容低溫容值下降', '高介電常數陶瓷特別明顯', '選低溫特性穩定的介質', '接受較大的體積'),
    ('切換雜訊離晶片很近', '雜訊可能干擾量子位元與讀取', '屏蔽、遠離晶片擺放、避開量子位元與讀取頻段、鎖定時脈', '屏蔽與擺放增加體積與設計難度'),
    ('封裝與可靠度', '熱循環造成應力、焊點問題', '借鏡太空與低溫儀器封裝；熱循環測試', '測試要時間'),
    ('測試成本高', '每次降溫都要時間', '小型 4 K 恆溫器（不需要稀釋冷凍機）', '要自建或找合作'),
    ('市場時程不確定', '低溫 CMOS 何時成為主流沒有定論', '小團隊＋學研合作；設檢查點', '投入要分段決策'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q141：從 1,000 到 10,000：MW 級與低溫電源轉換（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「工程答辯」：孩子當答辯人，拿著擴展用電比較表說明 1,000 與 10,000 位元的用電；你當評審，追問每個數字的依據。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 1,000 位元用電預算、四大塊、1,000 vs 10,000、低溫電源轉換的設計理念 | 影片第 3–7 段 |
| 25–65 | 整理擴展用電比較表；評審追問 | 列印包第 1、2 頁、`03_擴展用電比較表.csv` |
| 65–75 | 休息 | |
| 75–105 | 列出低溫電源轉換的兩個關鍵困難，各寫一個解法與代價 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼萬位元會變成 MW 級 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_擴展用電比較.pdf`（A4，共 4 頁），讀一遍 `04_解答.md` 與供電簡報第 51–57 頁。
- 想看動畫的話，用瀏覽器開 `animations/power1000.html#scale`（規模計算器）與 `#devplan`（開發計畫第 ⑧⑨⑩ 項）。

## 評審的原則

- 每一格都問一次「這個數字從哪裡來？量測、廠商文章，還是推論？」
- 被問倒不扣分：在那一格畫一個問號，寫下「要查什麼」。
- 10,000 位元那一欄很多格文件沒有給數字，寫「推論」或「待查」就是正確答案。

## 誠實說明

- 1,000 位元的 80–320 kW、中點約 200 kW 是學程文件的推論；10,000 位元的 MW 級、壓縮機 30–60 台也是推論，誤差可能很大。
- IBM Starling「約 12 個模組、每模組約 30 kW」來自文件引用的報導。
- 4 K GaN 轉換 91.6% 是廠商文章，正式論文待確認。
- 開發計畫的 ⑧⑨⑩ 是規劃建議，不是既有產品。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：擴展用電比較表（約 40 分鐘）

1. 在列印包第 1 頁，先填 1,000 位元那一欄：從影片或簡報第 51 頁找八類負載的低值與高值。
2. 再填 10,000 位元那一欄：只寫文件有依據的數字（模組化冷凍機 12 × 30 kW、低溫 CMOS 10–20 W @ 4 K），其他格寫「推論」或「待查」。
3. 每一格旁邊標來源：量測、廠商文章、推論。
4. 評審拿列印包第 2 頁的追問卡逐張追問；答不出來就在格子畫問號。

## 下半場：低溫電源轉換的兩個關鍵困難（約 30 分鐘）

1. 在列印包第 3 頁，從困難清單挑出兩個你認為最關鍵的。
2. 每個困難寫：它卡住了什麼、一個可能的解法、這個解法的代價。
3. 想一想：為什麼要「高電壓、低電流」送進冷凍機？

## 動畫對照（選做）

- `animations/power1000.html#scale`：把「量子位元數 N」拉到 10,000，看設施總功率與小字「MW 級量子資料中心」；再把「每位元室溫控制電子功耗」調成 10 W。
- `animations/power1000.html#devplan`：點 ⑧ 4 K 低溫電源轉換，讀困難與解法；再點 ⑨、⑩；把「時間」拉到第 36 個月看檢查點。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 擴展用電比較表（參考）\n\n| 負載 | 1,000 位元 | 10,000 位元（參考） | 依據 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in COMPARE)
  + '\n全部是學程文件的推論；10,000 位元一欄的「線性外推」由比較表自行換算，誤差可能很大。\n\n'
  + '規模計算器（power1000.html#scale，推論模型）在 N = 10,000、每位元 50 W 時算出設施約 1,948 kW（壓縮機 487.5 kW、控制電子 500 kW）；每位元 10 W 時約 1,388 kW。\n\n'
  + '## 評審追問參考答案\n\n' + ''.join(f'- **{q}** {a}\n' for q, a in QUIZ)
  + '\n## 低溫電源轉換的困難（開發計畫 §8.3）\n\n| 困難 | 卡住什麼 | 可能的解法 | 代價或注意 |\n|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in DIFFICULTIES)
  + '\n孩子挑哪兩個都可以；最常被選的是「損耗吃掉 4 K 冷卻預算」與「磁性元件與電容的低溫特性」。重點是說清楚卡住什麼，並寫出解法的代價。\n\n'
  '## 常見誤解\n\n'
  '- 「萬位元就是千位元乘十」：有些項目（模組化冷凍機）接近線性，有些（解碼、空調）文件沒有給數字；萬位元的數字是推論，誤差可能很大。\n'
  '- 「控制電子省電就能解決」：規模計算器裡每位元降到 10 W，萬位元仍約 1,388 kW；壓縮機一格不變。\n'
  '- 「91.6% 已經是成熟產品」：那是廠商文章的展示，正式論文待確認；開發計畫把 4 K 低溫電源轉換放在 3–7 年的共同研發。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/power1000.html#scale`（規模計算器）

- 「量子位元數 N」：100–約 20,000（對數滑桿）；「每位元室溫控制電子功耗」：1–150 W；「架構」：今日室溫控制／未來低溫 CMOS＋多工。
- 七列橫條；最下列是設施總功率，超過 1,000 kW 時小字寫「MW 級量子資料中心」。右邊面板有壓縮機、控制電子、設施總功率。

## `animations/power1000.html#devplan`（開發計畫，規劃建議）

- 點項目卡看「要做出什麼、第一步、困難與解法、完成判準」；綠框＝需要先有，金框＝成果提供給。
- 第三階段（3–7 年）：⑧ 4 K 低溫電源轉換、⑨ 高通道數直流供電、⑩ 模組化量子資料中心配電、⑪ 解碼機櫃供電與液冷。
- 「時間」滑桿：第 12、36 個月啟動第二、三階段；第 6、12、18、36 個月有檢查點。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['負載', '1,000 位元', '來源（量測／廠商／推論）', '10,000 位元', '來源（量測／廠商／推論）', '評審追問後的問號']
SHEET_ROWS = [[a] for a, *_ in COMPARE]

EXTRA_CSS = '''table.cmp td{height:11mm;font-size:10.5pt}table.cmp td:first-child{width:38mm}
.quiz{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}
.qc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:3mm 4mm;min-height:52mm;font-size:12pt}.qc b{color:#35a9d6}
.dif{columns:2;font-size:10.5pt;margin:2mm 0 0;padding-left:5mm}.dif li{margin:.6mm 0}
table.rec td{height:24mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    rows = ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, *_ in COMPARE)
    quiz = ''.join(f'<div class="qc"><b>追問 {i}</b><br>{q}<br><br>我的回答與依據：<div class="line"></div><div class="line"></div></div>'
                   for i, (q, _) in enumerate(QUIZ, 1))
    dif = ''.join(f'<li>{a}</li>' for a, *_ in DIFFICULTIES)
    pages = [
        '<h2>擴展用電比較表</h2><p class="lead">左欄 1,000 位元、右欄 10,000 位元。每一格標來源：量測、廠商文章、推論。</p>'
        f'<table class="cmp"><tr><th>負載</th><th>1,000 位元</th><th>10,000 位元</th></tr>{rows}</table>'
        '<p class="note">萬位元系統的數字是推論，誤差可能很大；文件沒給的格子寫「推論」或「待查」。</p>',
        f'<h2>答辯追問卡</h2><p class="lead">評審（爸爸）讀追問，答辯人（你）指著比較表說出依據。被問倒就畫問號。</p><div class="quiz">{quiz}</div>',
        '<h2>換你改造：低溫電源轉換的兩個關鍵困難</h2><p class="lead">從清單挑兩個最關鍵的，寫出卡住什麼、解法與代價。</p>'
        f'<h3>困難清單</h3><ul class="dif">{dif}</ul>'
        '<table class="rec"><tr><th>我挑的困難</th><th>卡住什麼</th><th>可能的解法</th><th>代價</th></tr>'
        '<tr><td>1.</td><td></td><td></td><td></td></tr><tr><td>2.</td><td></td><td></td><td></td></tr></table>'
        '<p class="note">想一想：為什麼要用高電壓、低電流把電送進冷凍機？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡：我的擴展用電比較表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 1,000 位元大約用多少電？哪一塊最大、哪一塊變動最大？</p><div class="line"></div><p>2. 10,000 位元為什麼會變成 MW 級？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：1,000 位元約 80–320 kW（中點約 200 kW）</li><li>解釋萬位元為什麼是 MW 級：模組化冷凍機、壓縮機群、控制電子</li>'
        '<li>說出低溫電源轉換的設計理念：高壓低電流送入、低溫端降壓</li><li>指出一個限制：萬位元數字是推論，誤差可能很大</li>'
        '<li>替比較表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q141 擴展用電比較 列印包', '父子科技學院 量子電腦學程 Q141｜從 1,000 到 10,000：MW 級與低溫電源轉換', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q141-mw-cryo-conversion', folder='Q141_擴展用電與低溫轉換', files=FILES,
        sheet=('03_擴展用電比較表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_擴展用電比較.pdf', pack_pages=4,
        pack_needles=('擴展用電比較表', '答辯追問卡', '兩個關鍵困難', '困難清單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q141', episode_dir='specials/q141-mw-cryo-conversion',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'compareRows': len(COMPARE), 'quizCards': len(QUIZ), 'difficulties': len(DIFFICULTIES),
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q141/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

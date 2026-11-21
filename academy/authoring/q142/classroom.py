"""Q142 課堂教材：空白產品 × 平台矩陣、產品提案卡、評審表、新產品構想卡、說明卡與解答。

不需要帳號或安裝；只要紙筆（或瀏覽器打開 animations/power1000.html#devplan、#roadmap 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q142/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 產品 × 平台矩陣（簡報 p73；文獻回顧 §18）：(代號, 產品, 超導, 離子阱, 中性原子, 時程, 格子小字／依據)
MATRIX = [
    ('A', '機房 UPS／配電／PDU（依平台分層）', '●', '●', '●', '現在', '超導保冷卻鏈；離子阱 T0 零中斷；中性原子保雷射熱穩態'),
    ('B', '精密空調與冷卻水（含蓄冷）', '●', '●', '●', '現在', '冷卻水 15–25 °C；±0.1 °C；20–23 °C、物鏡熱'),
    ('C', '雷射與光纖放大器電源', '○', '●', '●', '1–3 年', '離子阱 5–10 台雷射；中性原子 50–100 W 級放大器'),
    ('D', '機櫃級低雜訊乾淨電源', '●', '●', '◐', '1–3 年', '控制電子櫃；RF、DAC 電源；AOD 驅動；以 ODM 與控制電子廠合作'),
    ('E', '解碼 GPU／FPGA 機櫃供電', '●', '●', '●', '現在起', '規格就是 AI 機房；旁邊的 GPU 叢集可能是 MW 級（推論）'),
    ('F', '壓縮機與泵變頻驅動', '●', '◐', '○', '1–3 年', '超導主力；離子阱只有選配低溫；賣給冷凍機 OEM'),
    ('G', '精密電流源（線圈）', '◐', '●', '●', '1–3 年', 'ppm 線圈（離子阱）；快速開關＋量化場（中性原子）'),
    ('H', '諧波與磁場治理、量子區接地', '●', '●', '◐', '現在', '主動諧波濾波、母線與變壓器磁場設計、現場勘查'),
    ('I', '高通道 DAC 供電、低溫轉換', '●', '●', '○', '3–7 年', '低溫 GaN、cryo-CMOS；與學研合作'),
]
PRIORITY = [  # 簡報 p74、文獻回顧 §18.1
    ('1', 'A＋B＋H', '量子機房關鍵電力與精密環境（現在）', '三平台通用；差異化在依平台分層的 UPS 與實測交付'),
    ('2', 'E', '解碼 GPU／FPGA 機櫃（現在起）', '規格就是 AI 機房；電力量體在旁邊的經典運算'),
    ('3', 'F＋C／G', 'OEM 零組件（1–3 年）', '超導壓縮機變頻；原子平台雷射驅動、泵浦電源、線圈電流源'),
    ('4', 'D', '機櫃級乾淨電源（1–3 年）', '以 ODM 方式與控制電子廠合作'),
    ('5', 'I', '研發（3–7 年）', '低溫 GaN、高通道數 DAC 供電，與學研合作'),
]
MATURITY = [  # 教學用分級（依時程與合作方式對應，非文件原有分類）
    ('現在就有', '用現有產品就能組成（A、B、H、E）'),
    ('要和夥伴開發', '1–3 年，OEM／ODM 零組件（C、D、F、G）'),
    ('還在研究', '3–7 年，與學研合作（I）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q142：我們的切入點：產品 × 平台矩陣（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「產品評審」：你當提案人，一次拿一張產品卡，說服孩子先做它；孩子當評審，手上只有一張產品 × 平台矩陣。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 做電源不做儀器、矩陣怎麼讀、通用 vs 專用、整合優先序 | 影片第 3–8 段、列印包第 1 頁 |
| 25–65 | 在空白矩陣上標平台與成熟度；爸爸提案、孩子評審 | 列印包第 1、2 頁、`03_產品評審紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子提出一個矩陣上還沒有的產品構想，加一列 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：矩陣怎麼讀、優先序怎麼排 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_產品平台矩陣.pdf`（A4，共 4 頁），剪下第 2 頁的產品卡。準備三色筆（建議：綠＝現在就有、橙＝要和夥伴開發、紫＝還在研究）。
- 讀一遍 `04_解答.md`（簡報 p73 的完整矩陣與 p74 的優先序）。想看動畫的話，用瀏覽器開 `animations/power1000.html#devplan` 與 `#roadmap`。

## 提案人的原則

- 每張卡都要說出：它服務哪幾個平台、時程多久、為什麼現在該做。
- 故意誇大一次，例如「壓縮機變頻驅動三個平台都很需要」，看孩子能不能用矩陣（超導 ●、離子阱 ◐、中性原子 ○）抓出來。
- 孩子說不出依據的格子，請他先畫問號，不要直接給答案。

## 誠實說明

- 矩陣、整合優先序和「只能選一件就先做 A＋B＋H」都是學程供電文件的規劃建議與推論，不是既有產品線，也不是客戶確認的需求。
- 文件寫明：規格目標是開發起點的假設值，要用客戶的場地規劃文件與實測修正；所以矩陣要隨客戶回饋更新。
- 「成熟度」三級（現在就有／要和夥伴開發／還在研究）是本課為了教學，依時程與合作方式整理的分法。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：標出平台與成熟度（約 40 分鐘）

1. 在列印包第 1 頁的空白矩陣上，先讀產品名稱（A–I），每一列依你的理解畫 ●（主要）、◐（部分）、○（少或不需要）。
2. 最右欄填時程：現在、1–3 年、3–7 年。
3. 用三色筆替每一列塗成熟度：綠＝現在就有、橙＝要和夥伴開發、紫＝還在研究。
4. 爸爸拿第 2 頁的產品卡一張一張提案；你依評審三問打分：服務幾個平台？時程？符號有沒有依據？結果記在 `03_產品評審紀錄.csv`。
5. 最後排出你的優先序 1–5，和文件的整合優先序比一比，寫下一個不同的地方和理由。

## 下半場：矩陣上還沒有的產品（約 30 分鐘）

1. 從文獻缺口找靈感（列印包第 3 頁有提示）。
2. 在新產品構想卡寫：產品名稱、三個平台各一個符號、時程、一句依據、誰會買。
3. 把它加在矩陣最下面一列，標上「構想」，日後有客戶回饋再改。

## 動畫對照（選做）

- `animations/power1000.html#devplan`：點 ⑦ 精密線圈電流源、④ 壓縮機變頻驅動，看右側第一行的「矩陣」代號。
- `animations/power1000.html#roadmap`：看每張卡左上角的代號；點「解碼機櫃供電與液冷」會跳到全景，再點紅點 7。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 產品 × 平台矩陣（簡報 p73；文獻回顧 §18）\n\n'
  '| 代號 | 產品 | 超導 | 離子阱 | 中性原子 | 時程 | 格子小字／依據 |\n|---|---|---|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in MATRIX)
  + '\n● 主要　◐ 部分　○ 少或不需要\n\n## 整合優先序（簡報 p74；文獻回顧 §18.1）\n\n| 序 | 代號 | 內容 | 理由 |\n|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in PRIORITY)
  + '\n## 成熟度（本課教學用分級）\n\n' + ''.join(f'- **{a}**：{b}\n' for a, b in MATURITY)
  + '\n## 常見誤解\n\n'
  '- 「矩陣是定案」：矩陣是規劃工具，符號與時程依公開文獻判斷；客戶的場地規劃文件、實測與回饋進來就要更新。\n'
  '- 「三格都是 ● 就代表同一個產品」：A 列三格都是 ●，但超導保冷卻鏈、離子阱保零中斷、中性原子保雷射熱穩態，規格不同。\n'
  '- 「切入點就是自己做精密儀器」：簡報 p12 的原則是做儀器背後的電源，不做儀器；精密 DAC 儀器是儀器公司的本業。\n'
  '- 「這些已經是上市產品」：文獻回顧 §6 寫明沒有找到已推出量子專用方案的公開資訊；開發計畫是規劃建議。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/power1000.html#devplan`（開發計畫，規劃建議）

- 11 張項目卡分成 0–1 年、1–3 年、3–7 年；每張卡下方寫「矩陣 X」。
- 點卡片看右側：第一行是階段與矩陣代號，再來是要做出什麼、第一步、困難與解法、完成判準。
- 綠框是它需要先有的項目，金框是靠它提供成果的項目。

## `animations/power1000.html#roadmap`（三階段路線圖）

- 每張卡左上角是矩陣代號（QGP、OCP 不是矩陣代號，是先建立的能力與產業組織）。
- 點卡片會跳到對應的痛點場景；「解碼機櫃供電與液冷」跳到全景，紅點 7 是「解碼要緊鄰機台」。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['代號', '產品', '服務幾個平台（● 數）', '時程', '成熟度', '依據（簡報頁或文件章節）', '評審結論與理由']
SHEET_ROWS = [[c, n] for c, n, *_ in MATRIX] + [['構想 1', ''], ['構想 2', '']]

EXTRA_CSS = '''table.mx td,table.mx th{font-size:11pt;padding:1.6mm 2mm}table.mx td.c{width:17mm;text-align:center}table.mx td{height:10mm}
.cards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin-top:3mm}
.pc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:2.5mm 3mm;min-height:30mm;font-size:11pt}.pc b{color:#35a9d6;font-size:14pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    rows = ''.join(f'<tr><td><b>{c}</b> {n}</td><td class="c"></td><td class="c"></td><td class="c"></td><td class="c"></td><td class="c"></td></tr>'
                   for c, n, *_ in MATRIX)
    cards = ''.join(f'<div class="pc"><b>{c}</b><br>{n}<br><span class="note">平台：＿＿＿　時程：＿＿＿</span></div>' for c, n, *_ in MATRIX)
    pages = [
        '<h2>產品 × 平台矩陣（空白）</h2><p class="lead">每格畫 ●（主要）、◐（部分）、○（少）；最右兩欄填時程與成熟度。</p>'
        '<table class="mx"><tr><th>代號與產品</th><th>超導</th><th>離子阱</th><th>中性原子</th><th>時程</th><th>成熟度</th></tr>'
        f'{rows}<tr><td><b>＋</b> 我的構想：</td><td class="c"></td><td class="c"></td><td class="c"></td><td class="c"></td><td class="c"></td></tr></table>'
        '<p class="note">成熟度三色：綠＝現在就有、橙＝要和夥伴開發、紫＝還在研究。原則：做儀器背後的電源，不做儀器。</p>',
        '<h2>產品評審：提案卡與評審三問</h2><p class="lead">提案人（爸爸）一次拿一張卡；評審（你）只看矩陣，問三件事。</p>'
        '<div class="box"><b>評審三問</b>：1. 服務幾個平台？　2. 時程是現在還是三年以後？　3. 格子裡的符號有沒有文件依據？</div>'
        f'<div class="cards">{cards}</div>'
        '<p class="note">剪下九張卡。說不出依據的格子，先畫問號。</p>',
        '<h2>換你改造：矩陣上還沒有的產品</h2><p class="lead">從文獻缺口找靈感，替矩陣加一列。</p>'
        '<div class="box"><p class="note">靈感提示（文獻回顧 §19）：離子阱 RF 與電極需要多快的電源保持？量子機房的接地與低頻磁場沒有設計規範；'
        '線圈電流源沒有商用標準品的比較研究。</p></div>'
        '<div class="box" style="margin-top:4mm"><p>產品名稱：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>超導：＿＿　離子阱：＿＿　中性原子：＿＿　時程：＿＿＿＿</p>'
        '<p>一句依據：</p><div class="line"></div><p>誰會買：</p><div class="line"></div>'
        '<p>客戶回饋後要改什麼：</p><div class="line"></div></div>',
        '<h2>說明卡：我的產品 × 平台矩陣</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 矩陣的列、欄和符號各代表什麼？</p><div class="line"></div><p>2. 為什麼第一步選三平台通用的 A＋B＋H？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：列是產品、欄是平台、● ◐ ○ 是需求程度</li><li>說出整合優先序：A＋B＋H → E → F＋C／G → D → I</li>'
        '<li>舉一個通用、一個專用的產品</li><li>指出一個限制：矩陣是規劃工具，要隨客戶回饋更新</li>'
        '<li>替矩陣取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q142 產品 × 平台矩陣 列印包', '父子科技學院 量子電腦學程 Q142｜我們的切入點：產品 × 平台矩陣', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q142-product-platform-matrix', folder='Q142_產品平台矩陣', files=FILES,
        sheet=('03_產品評審紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_產品平台矩陣.pdf', pack_pages=4,
        pack_needles=('產品 × 平台矩陣', '評審三問', '提案卡', '換你改造', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q142', episode_dir='specials/q142-product-platform-matrix',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'matrixRows': len(MATRIX), 'productCards': len(MATRIX), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q142/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

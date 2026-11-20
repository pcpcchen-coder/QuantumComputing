"""Q094 課堂教材：畢業專題提案 — 一頁提案模板、範例提案、產品評審表、兩週縮小範圍計畫、說明卡與解答。

免安裝、不需帳號：模板用紙筆即可；範例專題只用學程的 animations/operation.html#grover，用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q094/classroom.py
"""
from pathlib import Path
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 一頁提案的五個格子（課綱學習目標）
FIELDS = [('問題', '用一句話寫出想回答什麼'), ('方法', '動畫、程式、簡報或短片，打算怎麼做'),
          ('資源', '時間、工具、資料、需要誰幫忙'), ('風險', '哪裡可能卡住＋每個風險的備案'),
          ('成功標準', '看得到、量得到、對得到，附上證據')]

# 範例專題：09_grover.js 預設 N = 16；P(k) = sin²((2k+1)θ)，θ = asin(1/√N)；kOpt = round(π/(4θ) − 0.5)
N = 16
TH = math.asin(1 / math.sqrt(N))
K_OPT = max(1, round(math.pi / (4 * TH) - 0.5))
assert K_OPT == 3
P = [(k, round(100 * math.sin((2 * k + 1) * TH) ** 2, 1)) for k in range(6)]   # 0:6.2 1:47.3 2:90.8 3:96.1 4:58.2 5:12.5

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q094：畢業專題提案（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天孩子當提案人：挑一個量子主題，寫成一頁提案，向爸爸做五分鐘簡報；爸爸當產品評審。

只需要紙筆。若孩子想參考範例專題，下載學程的 `animations/` 資料夾，開 `operation.html#grover`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 一頁提案的五個格子、成功標準三特點 | 影片第 3–8 段、`01_提案步驟.md` |
| 25–65 | 寫一頁提案、五分鐘簡報、產品評審 | 列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 依回饋修改，縮小範圍到兩週做得完 | 列印包第 3 頁、`03_評審與兩週計畫.csv` |
| 105–115 | 孩子教爸爸：提案怎麼寫、成功標準怎麼訂 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_畢業專題提案.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md` 的範例提案。
- 想一想孩子這學程最有興趣的兩三堂課，簡報時可以從那裡提問。

## 產品評審怎麼玩

孩子用五分鐘依序講完五格。爸爸在評審表上每格打 1–3 分（1＝還看不懂、2＝看得懂但不夠具體、3＝清楚又做得到），最後問一個最難回答的問題，例如「兩週真的做得完嗎？」。回饋要具體，說哪一格、改什麼。

## 誠實說明

- 五個格子取自課綱的學習目標；課綱的「提案模板」標為需新增，本教材的模板是示範版。
- 評審每格 1–3 分是本教材自訂的簡化規則。
- 最重要的注意事項：範圍要小到做得完；寧可做小而完整。
''',

'01_提案步驟.md': '''# 提案步驟

## A. 選題（約 10 分鐘）

1. 列出三個你在學程裡最好奇的主題。
2. 每個主題判斷是哪一型：驗證型（用動畫重現一個結果）、講解型（做短片或簡報教會別人）、比較型（整理資料做成表）。
3. 挑一個兩週內做得完的。

## B. 寫一頁提案（約 20 分鐘）

照列印包第 1 頁，五格都要寫：問題、方法、資源、風險（含備案）、成功標準（含證據）。

## C. 五分鐘簡報與產品評審（約 10 分鐘）

依序講五格，爸爸在列印包第 2 頁打分並提問。把問題一字不漏記下來。

## D. 下半場：縮到兩週做得完（約 30 分鐘）

1. 圈出分數最低的那一格，先改它。
2. 刪掉範圍，只留下最核心的一件事；成功標準最好寫出一個數字。
3. 用列印包第 3 頁把兩週排成時間表，每隔幾天要有一個可以展示的成果。

## 參考：範例專題（`operation.html#grover`）

按「重設」，再一次一次按「完整一輪」，看右下插圖「P(成功) vs 輪數」上的白點；左側讀數會寫出答案的機率與最佳輪數。
''',

'04_解答.md': '# 解答與範例（爸爸用）\n\n## 範例一頁提案：格羅弗搜尋做幾輪最好\n\n'
  '| 格子 | 範例內容 |\n|---|---|\n'
  '| 問題 | 在 16 個抽屜裡，格羅弗搜尋做幾輪最容易找到答案？ |\n'
  '| 方法 | 用 operation.html#grover，每按一次「完整一輪」記下答案的機率，畫成折線圖 |\n'
  '| 資源 | 瀏覽器、學程動畫、方格紙；第 1 週量測，第 2 週畫圖做簡報；請爸爸幫忙檢查表格 |\n'
  '| 風險 | 讀數看不懂 → 先重看第一堂的格羅弗動畫展示；時間不夠 → 只做 16 個抽屜，不做其他大小 |\n'
  f'| 成功標準 | 表格列出第 0–5 輪的機率；最高點落在第 {K_OPT} 輪，和 (π/4)√N ≈ 3 相符；附截圖 |\n\n'
  '## 範例的參考數字（依 09_grover.js 的公式重算，沒有隨機成分）\n\n| 輪數 | 答案的機率 |\n|---|---|\n'
  + ''.join(f'| {k} | 約 {p}% |\n' for k, p in P)
  + '\n第 2 輪已超過九成，第 3 輪最高，第 4 輪轉過頭下降。\n\n'
  '## 常見問題\n\n'
  '- 題目太大怎麼辦？只回答一個問題、只用一種主要工具、先做最小可展示版本。\n'
  '- 成功標準怎樣才算好？看得到（能展示）、量得到（有數字）、對得到（能和理論、論文或別人的結果比）。\n'
  '- 被評審問倒怎麼辦？把問題記下來，下半場修改時優先處理。\n',

'05_動畫導覽.md': '''# 動畫導覽（範例專題用）

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `operation.html#grover`（3D 場景 9：Grover 搜尋）

- 滑桿：「量子位元數 n」（2–6）、「答案（標記的項目）」。預設 n = 4（16 個抽屜）、答案 11。
- 按鈕：② Oracle、③ 擴散、完整一輪、自動跑到最佳次數、測量、重設。
- 柱子是振幅：金色為正、藍色為負；綠框是答案。
- 右下插圖：左半是「答案–非答案」平面的幾何圖，右半是「P(成功) vs 輪數」，白點是目前輪數。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '格子／日期', '內容', '評審分數（1–3）', '評審的問題', '修改後', '可展示的成果', '完成了嗎', '備註']
SHEET_ROWS = ([['產品評審', f, '', '', '', '', '', '', ''] for f, _ in FIELDS]
              + [[f'兩週計畫第 {i} 天', '', '', '', '', '', '', '', ''] for i in range(1, 15)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}table.tpl td{height:24mm;vertical-align:top}'''


def html():
    pages = [
        '<h2>一頁提案模板（今天的作品：專題提案書）</h2><p class="lead">五格都寫滿，才算一頁提案。範圍要小到兩週做得完。</p>'
        '<p>專題名稱：＿＿＿＿＿＿＿＿＿＿＿＿　類型：驗證型／講解型／比較型　提案人：＿＿＿＿　日期：＿＿＿＿</p>'
        '<table class="rec tpl"><tr><th style="width:22%">格子</th><th>我的內容</th></tr>'
        + ''.join(f'<tr><td><b>{f}</b><br><small>{d}</small></td><td></td></tr>' for f, d in FIELDS) + '</table>',
        '<h2>產品評審：你簡報、爸爸評分</h2><p class="lead">五分鐘依序講完五格。評審每格打 1–3 分：1 還看不懂、2 看得懂但不夠具體、3 清楚又做得到。</p>'
        '<table class="rec"><tr><th>格子</th><th>分數（1–3）</th><th>評審的一句回饋</th></tr>'
        + ''.join(f'<tr><td>{f}</td><td></td><td></td></tr>' for f, _ in FIELDS) + '<tr><td>總分</td><td>／15</td><td></td></tr></table>'
        '<div class="card"><h3>評審最難的一個問題</h3><div class="line"></div><div class="line"></div>'
        '<p>我的回答：</p><div class="line"></div></div>',
        '<h2>換你改造：縮到兩週做得完</h2><p class="lead">先改最低分那一格，再刪範圍，最後排兩週。</p>'
        '<p>最低分的格子：＿＿＿＿　我要改成：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>刪掉的部分：＿＿＿＿＿＿＿＿＿＿＿＿　只留下的核心：＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>新的成功標準（寫出一個數字）：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>天</th><th>要做什麼</th><th>可以展示的成果</th><th>完成</th></tr>'
        + ''.join(f'<tr><td>第 {d} 天</td><td></td><td></td><td></td></tr>' for d in (1, 3, 5, 7, 9, 11, 14)) + '</table>'
        '<p class="note">生活技能：提案與接受回饋——說得清楚，也要虛心接受回饋。</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 一頁提案有哪五個格子？</p><div class="line"></div>'
        '<p>2. 好的成功標準要符合哪三個特點？</p><div class="line"></div><p>3. 你的專題怎麼證明成功了？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出五個格子：問題、方法、資源、風險、成功標準</li><li>說出成功標準三特點：看得到、量得到、對得到</li>'
        '<li>說出被評審問倒時怎麼辦</li><li>指出一個限制：範圍要小到做得完，寧可做小而完整</li>'
        '<li>替專題提案書取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q094 畢業專題提案 列印包', '父子科技學院 量子電腦學程 Q094｜畢業專題提案', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q094-capstone-proposal', folder='Q094_畢業專題提案', files=FILES,
        sheet=('03_評審與兩週計畫.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_畢業專題提案.pdf', pack_pages=4,
        pack_needles=('一頁提案模板', '產品評審', '縮到兩週做得完', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q094', episode_dir='specials/q094-capstone-proposal',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#grover'],
               'proposalFields': [f for f, _ in FIELDS], 'exampleGroverPercent': dict(P), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q094/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

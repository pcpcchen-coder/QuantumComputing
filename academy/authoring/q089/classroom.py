"""Q089 課堂教材：最佳化與機器學習：炒作與現實 — 六張改寫標題卡、新聞查核表、改寫練習、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/operation.html#grover（平方加速的直覺），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q089/classroom.py
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


def k_opt(N):
    """09_grover.js：kOpt = max(1, round(π/(4θ) − 0.5))，sin θ = 1/√N（JS Math.round 為四捨五入）。"""
    th = math.asin(1 / math.sqrt(N))
    return max(1, math.floor(math.pi / (4 * th) - 0.5 + 0.5)), th


GROVER = []
for n in range(2, 7):
    N = 1 << n
    k, th = k_opt(N)
    GROVER.append((n, N, N // 2, k, round(100 * math.sin((2 * k + 1) * th) ** 2, 1)))
assert [g[3] for g in GROVER] == [1, 2, 3, 4, 6]
assert k_opt(10 ** 6)[0] == 785

# 六張標題卡：全部為改寫／虛構的練習題，不是真實新聞引文。依據欄只引用學程簡報（QC_Operation_Talk.pptx）。
CARDS = [
    ('量子電腦讓人工智慧訓練快一萬倍', '誇大',
     '第 44 頁：機器學習加速類型「未定」；第 45 頁：資料載入約 N 步、沒有實用 QRAM',
     '和哪個古典方法比？資料怎麼載入？訓練資料多大？'),
    ('量子演算法解決物流最佳化，全面超越超級電腦', '誇大',
     '第 44 頁：最佳化（QAOA、量子退火）是啟發式，實用優勢尚未確立',
     '是哪個問題、多大？比的是最好的古典求解法嗎？'),
    ('量子搜尋：一百萬個候選只要約 785 次', '部分正確',
     '動畫場景 9：古典平均 50 萬次、Grover 約 785 次；第 42 頁：平方加速易被閘慢與錯誤更正開銷吃掉',
     '只算了查詢次數，沒算每次多慢；第 45 頁：一般資料庫查詢沒有已知量子加速'),
    ('未來的容錯量子電腦可破解 RSA-2048', '合理（附條件）',
     '第 44 頁：Shor 指數級；需容錯；2025 估計 < 100 萬實體位元、< 1 週',
     '「未來」「容錯」是關鍵條件，不是現在的機器'),
    ('量子模擬自旋系統，做出超越古典的實驗', '大致合理',
     '第 44 頁：物理模擬最可能最早實用、已有超越古典的實驗；第 43 頁：優勢邊界持續被古典演算法挑戰',
     '之後古典方法可能追上，要看後續研究'),
    ('買一台量子電腦，文書和試算表都會變快', '錯誤',
     '第 45 頁：加減乘除、排序、資料庫查詢、渲染、文書沒有已知的量子加速',
     '一般計算不是量子電腦擅於處理的問題'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q089：最佳化與機器學習：炒作與現實（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：新聞說量子電腦會讓最佳化和人工智慧大躍進，哪些說法有根據？

只需要列印包和瀏覽器（選用）：下載學程的 `animations/` 資料夾，開 `operation.html#grover` 看平方加速。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 應用地圖、加速的等級、哪些事不會變快 | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 六張標題卡逐一查核：證據、比較基準、限制 | 列印包第 1–2 頁、`03_新聞查核表.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子挑一則誇大標題，改寫成正確版本 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：怎麼分辨合理宣稱和誇大宣傳 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_最佳化與機器學習.pdf`（A4，共 4 頁），第 1 頁的六張標題卡剪開。
- 讀一遍 `04_解答.md`。六張卡都是**改寫／虛構的練習題**，不是真實新聞引文，卡上已標示。

## 誠實說明

- 本集對最佳化與機器學習的說法，只採用學程簡報第 44–45 頁的保守結論：最佳化「實用優勢尚未確立」、機器學習「加速未定、資料載入是瓶頸、仍在研究」。
- 這些結論會隨研究進展改變（簡報自註）。目的是學會問問題，不是把量子說得一無是處。
- 「比古典快」一定要問：和哪個古典演算法比？問題規模多大？有沒有算總時間（重複次數、錯誤更正、資料載入）？
''',

'01_操作步驟.md': '''# 操作步驟

## A. 看平方加速（`operation.html#grover`，約 10 分鐘，選用）

1. 確認「量子位元數 n」是 4（N = 16），按「自動跑到最佳次數」，看答案柱子被拉高；記下輪數。
2. 把「量子位元數 n」拉到 5、6，各按一次「自動跑到最佳次數」，記下輪數，填在列印包第 2 頁下方。
3. 看右下插圖的曲線：轉過最佳輪數，成功機率反而下降。

## B. 查核六則標題（約 30 分鐘）

每張卡回答三件事，寫進列印包第 2 頁的新聞查核表：證據在哪裡？和什麼比較？有什麼限制？最後判定：合理／部分正確／誇大／錯誤。

## C. 圖表抓鬼（穿插進行）

遇到圖表就檢查：縱軸是不是對數刻度？有沒有寫問題規模？比較對象是不是最好的古典方法？有沒有寫「示意」？

## D. 下半場：改寫一則誇大標題（約 30 分鐘）

用列印包第 3 頁：保留真的部分，補上比較對象、問題規模和限制，不要把「可能」寫成「已經」。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 六張標題卡（改寫／虛構練習題）\n\n'
  '| # | 標題卡 | 判定 | 依據 | 要追問的地方 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {i} | {t} | {v} | {e} | {q} |\n' for i, (t, v, e, q) in enumerate(CARDS, 1))
  + '\n判定是參考答案；孩子只要說得出依據和限制，判定略有不同也可以。\n\n'
  '## Grover 平方加速（以動畫 09_grover.js 的公式重算）\n\n'
  '| 量子位元數 n | 候選數 N | 古典平均查 N/2 次 | 最佳輪數 | 最佳時答案機率 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {n} | {N} | {c} | {k} | 約 {p}% |\n' for n, N, c, k, p in GROVER)
  + '\nN = 100 萬時：古典平均 50 萬次，Grover 約 785 次。候選數變 4 倍，輪數只變約 2 倍——這是平方加速，不是指數加速。'
  '而且動畫是沒有雜訊的理想情況；簡報第 42 頁提醒，量子閘比古典運算慢很多、錯誤更正有開銷，平方加速要在問題非常大時才划算。\n\n'
  '## 常見問題\n\n'
  '- 最佳化有量子加速嗎？QAOA、量子退火是啟發式方法；Grover 類有證明但只是平方。簡報結論：實用優勢尚未確立。\n'
  '- 量子機器學習呢？量子核方法、HHL 類加速類型未定；資料載入約 N 步、沒有實用 QRAM，是主要瓶頸。\n'
  '- 什麼問題最適合量子電腦？輸入小、計算難、輸出小，而且有可利用的數學或物理結構（例如分解質因數）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `operation.html#grover`（3D 場景 9：Grover 搜尋）

- 滑桿「量子位元數 n」：2–6（N = 4–64）；「答案（標記的項目）」：選哪一根是答案。
- 按鈕：② Oracle、③ 擴散、完整一輪、自動跑到最佳次數、測量、重設。
- 柱子高度是振幅（金色正、藍色負）；綠框是答案。做 Oracle 時出現粉紅色的平均振幅面。
- 右下插圖：左邊是「答案–非答案」平面的轉角，右邊是成功機率 vs 輪數，轉過頭會下降。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['標題卡', '證據在哪裡', '和什麼比較', '問題規模', '算了總時間嗎', '限制', '判定', '我的改寫']
SHEET_ROWS = [[f'第 {i} 張：{t}', '', '', '', '', '', '', ''] for i, (t, *_) in enumerate(CARDS, 1)]

EXTRA_CSS = '''table.rec td{height:11mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.hl{border:1.5pt dashed #0b2540;border-radius:3mm;padding:4mm;font-size:13pt;min-height:28mm}
.hl small{display:block;color:#666;font-size:9pt;margin-top:2mm}'''


def html():
    pages = [
        '<h2>六張新聞標題卡</h2><p class="lead">沿虛線剪開。每張都是改寫過的練習標題，不是真實新聞引文。</p><div class="cards">'
        + ''.join(f'<div class="hl"><b>第 {i} 張</b><br>「{t}」<small>標示：改寫／練習用</small></div>' for i, (t, *_) in enumerate(CARDS, 1))
        + '</div><p class="note">圖表抓鬼：縱軸是對數嗎？規模多大？和最好的古典方法比了嗎？有沒有寫「示意」？</p>',
        '<h2>新聞查核表（今天的作品）</h2><p class="lead">每張卡寫下：證據、比較基準、限制，再判定。</p>'
        '<table class="rec"><tr><th>卡</th><th>證據在哪裡</th><th>和什麼比較</th><th>限制</th><th>判定</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 7)) + '</table>'
        '<p>判定選一個：合理／部分正確／誇大／錯誤</p>'
        '<p>Grover 平方加速（operation.html#grover）：n = 4 要＿＿輪；n = 5 要＿＿輪；n = 6 要＿＿輪</p>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>',
        '<h2>換你改造：把標題改正確</h2><p class="lead">挑一則最誇大的標題，保留真的部分，補上條件。</p>'
        '<div class="card"><h3>原本的標題</h3><div class="line"></div></div>'
        '<div class="card"><h3>補上三個條件</h3><p>和哪個古典方法比：＿＿＿＿＿＿＿＿＿＿</p><p>問題規模多大：＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>還有哪些限制：＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<div class="card"><h3>我的改寫版</h3><div class="line"></div><div class="line"></div></div>'
        '<p class="note">生活技能：媒體識讀——看到驚人的數字，先問比較條件。不要把「可能」寫成「已經」。</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 最佳化的量子加速現在到哪裡了？</p><div class="line"></div>'
        '<p>2. 量子機器學習為什麼卡在資料進出？</p><div class="line"></div><p>3. 什麼樣的問題最適合量子電腦？</p><div class="line"></div>'
        '<p>4. 一個注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>說出最佳化現況：啟發式為主，實用優勢尚未確立</li><li>說出機器學習瓶頸：資料載入約 N 步、輸出只有 n 位元</li>'
        '<li>說出平方加速和指數加速的差別</li><li>指出一個注意事項：比古典快要問和誰比、問題多大</li>'
        '<li>替新聞查核表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q089 最佳化與機器學習：炒作與現實 列印包', '父子科技學院 量子電腦學程 Q089｜最佳化與機器學習：炒作與現實', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q089-optimization-ml-hype', folder='Q089_最佳化與機器學習', files=FILES,
        sheet=('03_新聞查核表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_最佳化與機器學習.pdf', pack_pages=4,
        pack_needles=('新聞標題卡', '新聞查核表', '把標題改正確', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q089', episode_dir='specials/q089-optimization-ml-hype',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#grover'],
               'headlineCardsAreRewritten': True, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q089/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

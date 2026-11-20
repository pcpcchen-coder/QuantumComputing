"""Q063 課堂教材：加速等級表、12 張問題卡、工程答辯審查單、新聞判斷單、可執行的 speedup_lab.py、說明卡與解答。

不需要帳號；speedup_lab.py 只用 Python 標準函式庫，把「比較快」換成數字：格羅弗輪數、秀爾 vs 一般數域篩法的量級、
精確模擬的記憶體、資料載入瓶頸、平方加速的交叉點（明確標成假設）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q063/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q063：快在哪？加速的等級 —— 把「比較快」換成數字

執行：python speedup_lab.py                  → 四個實驗全部跑一次
      python speedup_lab.py 格羅弗 1000000   → N 個抽屜：古典平均次數 vs 格羅弗輪數
      python speedup_lab.py 分解 2048        → n 位元：一般數域篩法 vs 秀爾 n³ 的量級（示意，常數略去）
      python speedup_lab.py 記憶體 50        → 精確模擬 n 顆量子位元要多少記憶體
      python speedup_lab.py 交叉 1e-9 1e-3   → 假設古典每查一次 1e-9 秒、量子每輪 1e-3 秒，N 多大格羅弗才划算
只用 Python 標準函式庫。所有「每一步幾秒」都是你自己填的假設，不是哪一台機器的真實數字。
"""
import math
import sys


def grover(N):
    """N 個抽屜、一個答案：古典平均要查 N/2 次；格羅弗約 (π/4)√N 輪。"""
    theta = math.asin(1 / math.sqrt(N))
    k = max(1, round(math.pi / (4 * theta) - 0.5))
    p = math.sin((2 * k + 1) * theta) ** 2
    return N / 2, k, p


def shor_vs_gnfs(bits):
    """n 位元整數：一般數域篩法 exp((64/9)^(1/3) (ln N)^(1/3) (ln ln N)^(2/3)) 與 n³ 的以 10 為底的量級。"""
    ln_n = bits * math.log(2)
    gnfs = (64 / 9) ** (1 / 3) * ln_n ** (1 / 3) * math.log(ln_n) ** (2 / 3) / math.log(10)
    return gnfs, 3 * math.log10(bits)


def memory(n):
    """精確存下 n 顆量子位元的狀態：2ⁿ 個複數，每個 16 bytes。"""
    return 2 ** n * 16


def human(b):
    for unit, s in (('EB', 1e18), ('PB', 1e15), ('TB', 1e12), ('GB', 1e9), ('MB', 1e6), ('KB', 1e3)):
        if b >= s:
            return f'{b / s:.3g} {unit}'
    return f'{b} bytes'


def crossover(t_classical, t_round):
    """古典平均 (N/2)·t_classical = 格羅弗 (π/4)√N·t_round 的 N。"""
    s = (math.pi / 4) * t_round * 2 / t_classical
    return s * s


def show_grover(N):
    c, k, p = grover(N)
    print(f'格羅弗：N = {N:,} 個抽屜 → 古典平均查 {c:,.0f} 次；格羅弗最佳 {k:,} 輪（成功機率 {p:.3f}）；差 {c / k:,.1f} 倍')


def show_shor(bits):
    g, s = shor_vs_gnfs(bits)
    print(f'分解 {bits} 位元：古典（一般數域篩法）約 10^{g:.1f}；秀爾約 n³ = 10^{s:.1f}（示意量級，常數都略去）')


def show_memory(n):
    print(f'精確模擬 {n} 顆：2^{n} × 16 bytes = {human(memory(n))}')


def show_cross(tc, tq):
    N = crossover(tc, tq)
    print(f'假設古典每查一次 {tc:g} 秒、格羅弗每輪 {tq:g} 秒：N 要超過約 {N:.3g}，格羅弗才比較快')
    for x in (1e6, 1e9, 1e12, 1e15):
        print(f'  N = {x:.0e}：古典 {x / 2 * tc:.3g} 秒，格羅弗 {math.pi / 4 * math.sqrt(x) * tq:.3g} 秒')


def show_loading(N):
    c, k, _ = grover(N)
    print(f'載入瓶頸：先把 {N:,} 筆資料一筆一筆載入（約 {N:,} 步），再跑 {k:,} 輪格羅弗 → 合計 {N + k:,} 步，'
          f'比古典直接找的平均 {c:,.0f} 次還多')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['格羅弗']:
        show_grover(int(float(a[1])) if len(a) > 1 else 10 ** 6)
    elif a[:1] == ['分解']:
        show_shor(int(a[1]) if len(a) > 1 else 2048)
    elif a[:1] == ['記憶體']:
        show_memory(int(a[1]) if len(a) > 1 else 50)
    elif a[:1] == ['交叉']:
        show_cross(float(a[1]) if len(a) > 1 else 1e-9, float(a[2]) if len(a) > 2 else 1e-3)
    else:
        print('== 平方級：格羅弗 ==')
        for N in (4, 16, 64, 10 ** 6, 10 ** 12):
            show_grover(N)
        print('\n== 指數級：秀爾 vs 一般數域篩法 ==')
        for bits in (512, 1024, 2048):
            show_shor(bits)
        print('\n== 古典模擬的極限 ==')
        for n in (30, 40, 50):
            show_memory(n)
        print('\n== 瓶頸 ==')
        show_loading(10 ** 6)
        show_cross(1e-9, 1e-3)
'''

ns = {}
exec(compile(PROGRAM, 'speedup_lab.py', 'exec'), ns)  # 用同一份程式算解答，避免手抄錯

_c6, _k6, _p6 = ns['grover'](10 ** 6)
_g2048, _s2048 = ns['shor_vs_gnfs'](2048)
_cross = ns['crossover'](1e-9, 1e-3)

PROBLEMS = [
    ('分解一個 2048 位元的整數', '指數級', '秀爾演算法：古典次指數（約 10³⁵ 量級）、量子約 n³（約 10¹⁰）；要大規模容錯量子電腦'),
    ('算離散對數（另一種公開金鑰加密的難題）', '指數級', '秀爾演算法同樣適用（簡報第 42 頁表格）'),
    ('算出一個分子的基態能量（化學、藥物）', '指數級', '量子系統模擬，多數情況指數級；工業級分子需數百萬實體位元等級'),
    ('模擬一塊磁性材料裡的自旋', '指數級', '物理模擬；簡報第 44 頁：最可能最早實用'),
    ('一百萬個沒有規律的號碼裡找出唯一一個', '平方級', '格羅弗：古典平均 50 萬次 → 約 785 輪'),
    ('用蒙地卡羅估計投資風險（精度 ε）', '平方級', '振幅估計：約 1/ε² 次 → 約 1/ε 次；需容錯、常數開銷大'),
    ('暴力試出 128 位元的對稱金鑰', '平方級', '格羅弗約 2⁶⁴ 次（維基百科）；金鑰加倍就抵消'),
    ('數獨、旅行推銷員這類 NP 完全問題的暴力搜尋', '平方級（最多）', '普遍認為量子電腦不能有效解 NP 完全問題，格羅弗只給平方加速'),
    ('把一百萬筆資料排序', '沒有加速', '沒有已知的量子加速（簡報第 45 頁）'),
    ('文書處理、影像渲染、兩個數相加', '沒有加速', '沒有已知的量子加速；量子閘約 100 ns，反而更慢'),
    ('用量子電腦分析大數據、做機器學習', '未定', '資料載入是瓶頸，沒有實用的 QRAM；仍在研究'),
    ('物流路線最佳化（量子退火、QAOA）', '未定', '啟發式方法，實用優勢尚未確立'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q063：快在哪？加速的等級（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心一句：**量子電腦不是什麼都比較快。有可利用的結構、靠干涉集中機率的問題才有加速，而且分等級：分解質因數與量子系統模擬是指數級；無結構搜尋與蒙地卡羅估計是平方級；加減乘除、排序、文書沒有已知加速；機器學習與最佳化仍未定。資料輸入、資料輸出與小問題的額外開銷，都可能把加速吃掉。** 好玩機制是工程答辯：孩子提案，爸爸當審查委員追問三問——哪一級？規模變大時差多少？資料進出會不會卡住？

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開 operation.html#grover 調量子位元數，看「最佳輪數 vs 古典次數」；看 transmon-3d.html#shor 第 3、5、6 步 | 列印包第 4 頁（說明卡） |
| 25–65 | 把 12 張問題卡排進加速等級表、寫理由；玩工程答辯 | 列印包第 1–3 頁、`speedup_lab.py` |
| 65–75 | 休息 | |
| 75–105 | 改造：找一則宣稱量子加速的新聞，用新聞判斷單判斷屬於哪一級 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：三級、結構＋干涉、一個限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_加速等級表.pdf`（A4，共 4 頁）。第 2 頁問題卡沿虛線剪開。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#grover` 與 `transmon-3d.html#shor`，不需要帳號。
- 電腦有 Python 3 就能執行 `speedup_lab.py`（不用安裝套件）。
- 準備一兩則「量子電腦比超級電腦快 X 倍」的新聞（或讓孩子自己找）。
- 讀一遍 `04_解答.md`。

## 誠實說明

- 「古典約 10³⁵、秀爾約 10¹⁰」是略去常數的示意量級（簡報第 42 頁），不是真實執行時間。
- 等級表裡的「未定」與各應用的現況，是目前文獻的常見結論（簡報第 44 頁），會隨研究改變。
- `speedup_lab.py 交叉` 的每步秒數是你自己填的假設；真實的交叉點取決於硬體與錯誤更正的開銷。
- 2019 年「200 秒 vs 一萬年」的宣稱，IBM 估計最佳化後 Summit 約 2.5 天（維基百科 Quantum supremacy）；優勢邊界一直被古典演算法挑戰。
''',

'01_操作步驟.md': '''# 操作步驟

## 先看動畫（約 15 分鐘）

1. 打開 `animations/operation.html#grover`。拉「量子位元數 n」滑桿到 2、4、6，抄下左邊面板最下方讀數的「最佳輪數」與「古典平均要查幾次」：
   N = 4 → 1 輪／2 次；N = 16 → 3 輪／8 次；N = 64 → 6 輪／32 次。
2. N = 64 時交替按「② Oracle」「③ 擴散」六次，看答案的機率 P 到 0.997；再按「測量」——六十四個振幅，只讀出一個號碼。
3. 打開 `animations/transmon-3d.html#shor`（第 8 章），先取消勾選「自動接續」，按步驟按鈕 3、5、6，讀右邊說明：
   模指數最花資源（閘數約 n³）；QFT 只要約 n² 個閘，古典 FFT 要約 n·2ⁿ 步。

## 父子實作：加速等級表（約 40 分鐘）

1. 每人輪流抽一張問題卡，放進等級表的四格之一：指數級、平方級、沒有加速、未定。
2. 每張卡寫一句理由：有沒有可利用的結構？規模變大時差多少？資料進出會不會卡住？
3. 用 `python speedup_lab.py` 算數字：例如 `python speedup_lab.py 格羅弗 1000000`、`python speedup_lab.py 分解 2048`、`python speedup_lab.py 記憶體 50`。
4. 工程答辯：孩子提案（等級＋數字），爸爸用審查單追問三問；答不出來就退回重寫。

## 改造：判斷一則新聞（約 30 分鐘）

1. 找一則宣稱量子加速的新聞。
2. 在新聞判斷單寫下：解什麼問題？比的是總時間還是單一步驟？資料怎麼進出？
3. 判斷它屬於哪一級，再用 `speedup_lab.py 交叉` 試試：如果量子每輪比古典慢一百萬倍，平方加速要 N 多大才划算？
''',

'speedup_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 12 張問題卡的參考分級\n\n| # | 問題 | 等級 | 理由 |\n|---|---|---|---|\n'
  + ''.join(f'| {i} | {q} | {lv} | {why} |\n' for i, (q, lv, why) in enumerate(PROBLEMS, 1)) +
  '\n分級是「規模變大時差距怎麼變」，不是某一題快幾秒。孩子的理由合理即可，例如把機器學習放「平方級」並說明「某些子程序可用振幅放大」也可以討論，但要指出資料載入的瓶頸。\n\n'
  '## 數字（由 `speedup_lab.py` 算出）\n\n'
  f'- 一百萬個抽屜：古典平均 {_c6:,.0f} 次；格羅弗最佳 {_k6} 輪（(π/4)√10⁶ ≈ 785.4），成功機率 {_p6:.4f}。\n'
  '- N = 4、16、64：最佳 1、3、6 輪；古典平均 2、8、32 次（與 operation.html#grover 讀數相同）。\n'
  f'- 分解 2048 位元：一般數域篩法約 10^{_g2048:.1f}；n³ = 2048³ ≈ 8.6 × 10⁹（10^{_s2048:.1f}）。\n'
  '- 精確模擬：30 顆 2³⁰ × 16 bytes ≈ 17.2 GB（16 GiB）；40 顆 ≈ 17.6 TB；50 顆 ≈ 18 PB。每多 10 顆 × 1024。\n'
  f'- 載入瓶頸：一百萬筆一筆一筆載入約 10⁶ 步，再加 {_k6} 輪，已經比古典直接找的平均 {_c6:,.0f} 次還多。\n'
  f'- 交叉點（假設古典每次 1 ns、格羅弗每輪 1 ms）：N 約 {_cross:.2g}；N = 10¹² 時古典 500 秒、格羅弗約 785 秒，量子還比較慢。\n\n'
  '## 常見誤解\n\n'
  '- 「n 個量子位元同時試 2ⁿ 個答案，所以快 2ⁿ 倍」：量測只得到一個隨機結果；沒有干涉就等於亂猜。\n'
  '- 「量子電腦什麼都比較快」：只有特定結構的問題有加速，幅度從平方級到指數級不等。\n'
  '- 「量子電腦能有效解 NP 完全問題」：普遍認為不能；格羅弗只給平方加速。\n'
  '- 「量子位元越多越強」：錯誤率、連接與相干時間同樣重要。\n'
  '- 「量子電腦能加速大數據分析」：沒有實用的 QRAM，大量資料載入本身就會吃掉加速。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要帳號。

## `animations/operation.html#grover`（場景 9：Grover 搜尋）

- 滑桿「量子位元數 n」（2～6，N = 4～64）、「答案（標記的項目）」；按鈕「② Oracle」「③ 擴散」「完整一輪」「自動跑到最佳次數」「測量」「重設」。
- 左邊面板最下方讀數：第幾輪、答案的機率、最佳輪數 ≈ (π/4)√N、古典平均要查幾次、測量結果。
- 右下小圖：每輪在「答案–非答案」平面轉 2θ，以及成功機率 vs 輪數。

## `animations/transmon-3d.html#shor`（第 8 章：Shor 演算法，分解 15）

- 右邊有步驟按鈕 1～8 與「自動接續」勾選框；要自己一步一步看時先取消勾選。
- 第 3 步模指數（最花資源，閘數約 n³）、第 5 步 QFT（約 n² 個閘 vs 古典 FFT 約 n·2ⁿ 步）、第 6 步量測（只落在 0、4、8、12）。

## 操作

滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換場景（operation.html）或章節（transmon-3d.html）。
''',
}

SHEET_HEADER = ['題號', '問題', '等級（指數／平方／沒有／未定）', '古典要多少', '量子要多少', '理由（結構、差距）', '瓶頸（輸入、輸出、小問題）']
SHEET_ROWS = [[str(i), q] for i, (q, _, _) in enumerate(PROBLEMS, 1)]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}.cards .cut{padding:3mm 4mm;height:50mm;text-align:center}
.cards h3{font-size:12pt;margin:0 0 2mm}.cards .big{font-size:13pt;font-weight:700;color:#0b2540;margin:3mm 0;line-height:1.35}.cards p{margin:1mm 0;font-size:10pt}
table.lv td{height:120mm;vertical-align:top}table.lv th{font-size:12pt;text-align:center}
table.dv td{height:12mm}table.dv th{text-align:left;font-size:10.5pt}table.dv td:first-child{width:36mm;font-weight:700}
.chk li{margin:2mm 0;font-size:12pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    cards = ''.join(f'<div class="cut"><h3>問題卡・{i}</h3><p class="big">{q}</p><p>哪一級？差多少？卡在哪？</p></div>'
                    for i, (q, _, _) in enumerate(PROBLEMS, 1))
    lv = ('<table class="lv"><tr><th>指數級</th><th>平方級</th><th>沒有加速</th><th>未定</th></tr>'
          '<tr>' + '<td></td>' * 4 + '</tr></table>')
    rows = ''.join(f'<tr><td>{k}</td><td></td></tr>' for k in ('提案題目', '我說的等級', '古典要多少', '量子要多少',
                                                               '審查一：哪一級？', '審查二：差多少？', '審查三：卡在哪？', '審查結果'))
    news = ''.join(f'<tr><td>{k}</td><td></td></tr>' for k in ('新聞標題／日期', '解什麼問題', '有沒有可利用的結構',
                                                               '比的是什麼（總時間？）', '資料怎麼進出', '我判斷的等級'))
    pages = [
        '<h2>加速等級表</h2><p class="lead">把 12 張問題卡排進四格，每張寫一句理由。分級看「規模變大時差距怎麼變」。</p>'
        + lv +
        '<div class="box" style="margin-top:4mm"><p>平方級：N 個抽屜，古典平均 N/2 次，格羅弗約 (π/4)√N 輪。一百萬 → 50 萬次 vs 約 785 輪。</p>'
        '<p>指數級：分解 2048 位元，古典約 10³⁵、秀爾約 10¹⁰（示意量級，常數略去）。</p>'
        '<p>瓶頸：輸入（載入 N 筆約 N 步）、輸出（n 顆只讀出 n 位元）、小問題（閘約 100 ns）。</p></div>',
        '<h2>問題卡（12 張）</h2><p class="lead">沿虛線剪開。抽一張、說出等級，再用數字說明差多少、卡在哪。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>工程答辯審查單</h2><p class="lead">孩子提案，爸爸是審查委員。三問都答得出來才通過。</p>'
        f'<table class="dv"><tr><th>項目</th><th>寫下來</th></tr>{rows}</table>'
        '<h2 style="margin-top:5mm">新聞判斷單</h2>'
        f'<table class="dv"><tr><th>項目</th><th>寫下來</th></tr>{news}</table>',
        '<h2>說明卡：快在哪？</h2><div class="box">'
        '<p>1. 量測只拿到一個結果：沒有安排好相位、沒有干涉，就等於亂猜。</p>'
        '<p>2. 配方：疊加 → 用問題的結構安排相位 → 干涉讓錯的答案抵消 → 量測。</p>'
        '<p>3. 最適合量子電腦的問題：輸入小、計算難、輸出小，而且有可利用的結構。</p>'
        '<p>4. 比較要算總時間：重複量測次數、錯誤更正開銷、資料載入。</p></div>'
        '<div class="box" style="margin-top:3mm"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 快在哪？加速的等級在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:3mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三級，各舉一個例子</li>'
        '<li>解釋為什麼要有結構和干涉才有加速</li>'
        '<li>指出一個限制：沒有實用的 QRAM，大量資料載入本身就會吃掉加速</li>'
        '<li>替加速等級表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q063 快在哪？加速的等級 列印包', '父子科技學院 量子電腦學程 Q063｜快在哪？加速的等級', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q063-speedup-levels', folder='Q063_快在哪加速的等級', files=FILES,
        sheet=('03_加速等級表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_加速等級表.pdf', pack_pages=4,
        pack_needles=('加速等級表', '問題卡', '工程答辯審查單', '新聞判斷單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q063', episode_dir='specials/q063-speedup-levels',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'speedup_lab.py', 'problemCards': len(PROBLEMS),
               'levelsFrom': 'slides/QC_Operation_Talk.pptx p36–37, p42–45; animations/operation.html#grover; transmon-3d.html#shor',
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q063/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q109 課堂教材：表面碼解碼練習單、可執行的 surface_d3.py、兩個錯誤的騙局紀錄表、容易錯的地方、教爸爸檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#surface（第 10 章）；程式只要 Python 3。
建置時會真的執行一次 surface_d3.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q109/classroom.py
"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，結果固定（無亂數）
RUN_OUTPUT = '''一、單一錯誤（9 種）
  錯誤 D1 → 亮：左上（內部） → 修正 D1 → 成功 ✓
  錯誤 D2 → 亮：左上（內部） → 修正 D1 → 成功 ✓
  錯誤 D3 → 亮：右邊界半圓 → 修正 D3 → 成功 ✓
  錯誤 D4 → 亮：左上（內部）、左邊界半圓 → 修正 D4 → 成功 ✓
  錯誤 D5 → 亮：左上（內部）、右下（內部） → 修正 D5 → 成功 ✓
  錯誤 D6 → 亮：右下（內部）、右邊界半圓 → 修正 D6 → 成功 ✓
  錯誤 D7 → 亮：左邊界半圓 → 修正 D7 → 成功 ✓
  錯誤 D8 → 亮：右下（內部） → 修正 D8 → 成功 ✓
  錯誤 D9 → 亮：右下（內部） → 修正 D8 → 成功 ✓
二、兩個錯誤（36 種）中，騙過解碼器的：
  錯誤 D1、D4 → 亮：左邊界半圓 → 修正 D7 → 邏輯錯誤 ✗（剩下 D1、D4、D7）
  錯誤 D1、D5 → 亮：右下（內部） → 修正 D8 → 邏輯錯誤 ✗（剩下 D1、D5、D8）
  錯誤 D1、D7 → 亮：左上（內部）、左邊界半圓 → 修正 D4 → 邏輯錯誤 ✗（剩下 D1、D4、D7）
  錯誤 D1、D8 → 亮：左上（內部）、右下（內部） → 修正 D5 → 邏輯錯誤 ✗（剩下 D1、D5、D8）
  錯誤 D1、D9 → 亮：左上（內部）、右下（內部） → 修正 D5 → 邏輯錯誤 ✗（剩下 D1、D5、D9）
  錯誤 D2、D4 → 亮：左邊界半圓 → 修正 D7 → 邏輯錯誤 ✗（剩下 D2、D4、D7）
  錯誤 D2、D5 → 亮：右下（內部） → 修正 D8 → 邏輯錯誤 ✗（剩下 D2、D5、D8）
  錯誤 D2、D7 → 亮：左上（內部）、左邊界半圓 → 修正 D4 → 邏輯錯誤 ✗（剩下 D2、D4、D7）
  錯誤 D2、D8 → 亮：左上（內部）、右下（內部） → 修正 D5 → 邏輯錯誤 ✗（剩下 D2、D5、D8）
  錯誤 D2、D9 → 亮：左上（內部）、右下（內部） → 修正 D5 → 邏輯錯誤 ✗（剩下 D2、D5、D9）
  錯誤 D3、D6 → 亮：右下（內部） → 修正 D8 → 邏輯錯誤 ✗（剩下 D3、D6、D8）
  錯誤 D3、D8 → 亮：右下（內部）、右邊界半圓 → 修正 D6 → 邏輯錯誤 ✗（剩下 D3、D6、D8）
  錯誤 D3、D9 → 亮：右下（內部）、右邊界半圓 → 修正 D6 → 邏輯錯誤 ✗（剩下 D3、D6、D9）
  錯誤 D4、D7 → 亮：左上（內部） → 修正 D1 → 邏輯錯誤 ✗（剩下 D1、D4、D7）
  錯誤 D5、D8 → 亮：左上（內部） → 修正 D1 → 邏輯錯誤 ✗（剩下 D1、D5、D8）
  錯誤 D5、D9 → 亮：左上（內部） → 修正 D1 → 邏輯錯誤 ✗（剩下 D1、D5、D9）
  錯誤 D6、D8 → 亮：右邊界半圓 → 修正 D3 → 邏輯錯誤 ✗（剩下 D3、D6、D8）
  錯誤 D6、D9 → 亮：右邊界半圓 → 修正 D3 → 邏輯錯誤 ✗（剩下 D3、D6、D9）
  共 18 種會造成邏輯錯誤，18 種修得好
三、每顆資料位元以機率 p 翻轉時，邏輯錯誤率（512 種情況全部加總，不用亂數）
  p =    1%  →  邏輯錯誤率   0.17%  （比不編碼好）
  p =    5%  →  邏輯錯誤率   3.69%  （比不編碼好）
  p =   10%  →  邏輯錯誤率  11.97%  （比不編碼還糟）
  p =   20%  →  邏輯錯誤率  30.84%  （比不編碼還糟）
  p =   30%  →  邏輯錯誤率  43.85%  （比不編碼還糟）
四、我的實驗：
  錯誤 D1、D4 → 亮：左邊界半圓 → 修正 D7 → 邏輯錯誤 ✗（剩下 D1、D4、D7）
'''

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q109：表面碼——穩定子與匹配解碼（純 Python，不需要安裝任何套件）

執行：  python surface_d3.py
d = 3 的表面碼（和 transmon-3d.html 第 10 章同一個排法）：資料位元 D1～D9 排成 3×3，
  D1 D2 D3
  D4 D5 D6
  D7 D8 D9
這裡只看 X 錯誤（位元翻轉），所以只用 4 個 Z 穩定子（青色格子）；Z 錯誤由另外 4 個 X 穩定子用同樣的方法處理。
"""
from itertools import combinations

# 改造區 1：自己注入錯誤（寫資料位元的編號），看哪些穩定子亮、解碼器怎麼修
MY_ERRORS = [1, 4]

# 4 個 Z 穩定子：名字 → 它量奇偶的資料位元
Z_STABS = {
    '左上（內部）': (1, 2, 4, 5),
    '右下（內部）': (5, 6, 8, 9),
    '左邊界半圓': (4, 7),
    '右邊界半圓': (3, 6),
}
TOP_ROW = (1, 2, 3)   # 邏輯 Z 是第一列的 Z：殘餘的 X 錯誤在這一列有奇數個 → 邏輯位元被翻轉


def syndrome(errs):
    """哪些穩定子亮（量到 −1）：它管的資料位元裡，錯誤的個數是奇數"""
    return tuple(name for name, qs in Z_STABS.items() if sum(q in errs for q in qs) % 2 == 1)


# 解碼器：對每一種亮法，找「最少顆」就能造成同樣亮法的修正（最小權重）。
# d = 3 只有 2⁹ = 512 種，可以全部試一遍；大碼距時改用最小權重完美匹配，答案相同、但快得多。
TABLE = {}
for k in range(10):
    for fix in combinations(range(1, 10), k):
        TABLE.setdefault(syndrome(set(fix)), set(fix))


def decode(errs):
    errs = set(errs)
    fix = TABLE[syndrome(errs)]
    left = errs ^ fix                     # 錯誤和修正抵消後剩下的
    logical = sum(q in left for q in TOP_ROW) % 2 == 1
    return fix, left, logical


def show(errs):
    fix, left, logical = decode(errs)
    lit = syndrome(set(errs)) or ('沒有',)
    print(f'  錯誤 {fmt(errs)} → 亮：{"、".join(lit)} → 修正 {fmt(fix)} → '
          + ('邏輯錯誤 ✗（剩下 ' + fmt(left) + '）' if logical else '成功 ✓'))


def fmt(qs):
    return '、'.join(f'D{q}' for q in sorted(qs)) or '無'


if __name__ == '__main__':
    print('一、單一錯誤（9 種）')
    for q in range(1, 10):
        show([q])
    print('二、兩個錯誤（36 種）中，騙過解碼器的：')
    bad = [pair for pair in combinations(range(1, 10), 2) if decode(pair)[2]]
    for pair in bad:
        show(pair)
    print(f'  共 {len(bad)} 種會造成邏輯錯誤，{36 - len(bad)} 種修得好')
    print('三、每顆資料位元以機率 p 翻轉時，邏輯錯誤率（512 種情況全部加總，不用亂數）')
    for p in (0.01, 0.05, 0.10, 0.20, 0.30):
        pl = sum(p ** k * (1 - p) ** (9 - k)
                 for k in range(10) for errs in combinations(range(1, 10), k) if decode(errs)[2])
        print(f'  p = {p * 100:4.0f}%  →  邏輯錯誤率 {pl * 100:6.2f}%  '
              + ('（比不編碼好）' if pl < p else '（比不編碼還糟）'))
    print('四、我的實驗：')
    show(MY_ERRORS)
'''

# 單一錯誤練習：(錯誤, 亮的青色格子, 解碼器修哪一顆, 結果)
SINGLE = [
    ('D5 的 X', '左上、右下', 'D5', '成功'),
    ('D1 的 X', '左上', 'D1', '成功'),
    ('D7 的 X', '左邊界半圓', 'D7', '成功'),
    ('D6 的 X', '右下、右邊界半圓', 'D6', '成功'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q109：第 11 課 表面碼——穩定子與匹配解碼（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：表面碼只量相鄰位元的奇偶（穩定子），不量資料本身；錯誤會讓附近的格子「亮」，解碼器把亮點配對，推回錯誤的位置。課堂用「Bug 獵人」的方式：一個人偷偷放錯誤，另一個人只看亮點來抓。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#surface`（第 10 章表面碼，按步驟「8」進自由實驗）；加映 `operation.html#qec`（場景 11）。免安裝、不需帳號 |
| 程式 | `surface_d3.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_表面碼解碼練習單.pdf`（A4，共 4 頁）；一張紙蓋住螢幕上的圓球（解碼的人只准看格子） |
| 參考 | slides/transmon.pptx 第 24 頁、slides/QC_Operation_Talk.pptx 第 49–50 頁 |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「不量資料，怎麼知道哪裡錯了？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：三位元重複碼、d = 3 表面碼、一個週期、配對與邊界 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 在第 10 章自由實驗點位元注入錯誤，看症狀與解碼器配對，填單一錯誤練習 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：找出兩個錯誤造成邏輯錯誤的例子；用程式對答案、改 MY_ERRORS | `surface_d3.py`、列印包第 2 頁、`03_騙局紀錄.csv` |
| 105–115 | 孩子教爸爸：操作與原理，指出一個限制 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結、替表面碼解碼練習單命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `transmon-3d.html#surface`，從步驟 1 看到步驟 7（自動接續，約 3 分鐘，左上方字幕逐句說明），再按步驟「8」進自由實驗。
- 在自由實驗點 D5 一下、按「解碼並修正」；再點 D1、D4 各一下、按「解碼並修正」，看到「邏輯錯誤！（邏輯 X）」。
- 跑一次 `python surface_d3.py`，確認「共 18 種會造成邏輯錯誤，18 種修得好」。
- 讀一遍 `04_解答.md`。

## 解碼的人（爸爸）的原則

- 只准看格子（亮的穩定子），不看圓球的顏色；先說出「錯在哪、要修哪一顆」，再按「解碼並修正」對答案。
- 最重要的一句：解碼器只看得到症狀，看不到錯誤本身；它選「最少錯誤就能解釋這些亮點」的答案，所以 d = 3 只保證修好 1 個錯誤。

## 誠實說明

- 自由實驗的「跑 300 次統計」和 operation.html 的插圖都用簡化模型（只有資料位元出錯、量測完美），門檻約 10–15%；真實電路（閘與量測也會錯）的門檻約 1%。
- `surface_d3.py` 只看 X 錯誤（Z 錯誤由另一組穩定子用同樣方法處理），解碼器用「全部試一遍找最少顆」的方法；d = 3 只有 512 種情況，結果和最小權重完美匹配相同，碼距大時就要改用匹配演算法。
- 程式裡錯誤 D2 會被「修」在 D1、錯誤 D9 被修在 D8：D1、D2 一起翻剛好是上邊界的琥珀色穩定子，不影響邏輯資訊，所以仍然是成功。
- 一個週期約 1 μs、Google 2024 年 Willow 晶片 d = 3 → 5 → 7 每次邏輯錯誤率約減半（Λ ≈ 2.1），依學程文件與維基百科 Surface code。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：單一錯誤與配對（約 40 分鐘）

1. 用瀏覽器開 `animations/transmon-3d.html#surface`（第 10 章）。看完步驟 1～7，再按步驟「8」（自由實驗）。
2. 點中間的資料位元 D5 一下（變紅 = X 錯誤）。看哪些格子亮：青色格子（Z 穩定子）亮了幾個？在哪裡？填進列印包第 1 頁。
3. 按「解碼並修正」：白線把亮點配成一對，D5 標上「修正」，右邊面板「最近一次解碼」寫「成功：錯誤已修正 ✓」。
4. 再點 D5 兩下（Z，藍色）、三下（Y，紫色）：亮的變成琥珀色格子、兩色都亮。
5. 換邊上的 D1、D7、D6 各試一次：只亮一個格子時，解碼器把亮點配到邊界。
6. 換手：一個人偷偷點，另一個人蓋住圓球、只看格子猜錯在哪，再按「解碼並修正」對答案。

## 加映：另一個動畫（約 10 分鐘，可選）

- `animations/operation.html#qec`：碼距 5 的表面碼自動一輪一輪跑（紅球 → 橘色柱子 → 綠線 → 修正）。右下插圖是 d = 3、5、7 的邏輯錯誤率；拖「實體錯誤率 p」滑桿，看白色直線移到哪裡、三條線誰高誰低。

## 下半場：找兩個錯誤的騙局（約 30 分鐘）

1. 回到第 10 章自由實驗，先按「清除錯誤」。點 D1、D4 各一下，按「解碼並修正」，看到「邏輯錯誤！（邏輯 X）」。
2. 自己再找兩個錯誤的組合：先猜會不會騙過解碼器，再按「解碼並修正」，填進列印包第 2 頁。
3. 執行 `python surface_d3.py`，對照「二、兩個錯誤」的 18 種騙局。你找到的有在裡面嗎？
4. 改造：把 `MY_ERRORS = [1, 4]` 改成你想試的位元（例如 `[3, 6]`、`[2, 5, 8]`），再跑一次，看最後一行。
5. 想一想：為什麼有一半的兩個錯誤組合修得好？騙局裡的錯誤和修正合起來，是不是都連成一條從上到下的線？
'''
}

FILES.update({
'surface_d3.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 單一錯誤練習\n\n| 錯誤 | 亮的青色格子 | 解碼器修哪一顆 | 結果 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in SINGLE)
  + '\n- Z 錯誤（點兩下）亮的是琥珀色格子；Y（點三下）兩色都亮，解碼器 X、Z 分開配對、分開修正。\n'
  '- 只亮一個格子（邊上出錯）時，落單的亮點配到最近的邊界。\n'
  '\n## surface_d3.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- D1、D4：共用的左上格子翻兩次互相抵消不亮，只亮左邊界半圓；最省的解釋是 D7 一顆錯，補上後 D1、D4、D7 整排都翻了 = 邏輯 X。\n'
  '- 騙局的共同點：真正的錯誤加上解碼器的修正，剛好連成一條從上邊連到下邊的線（每一列各一顆），所有格子都不亮，邏輯位元卻被翻轉。\n'
  '- 36 種兩個錯誤中 18 種修得好：兩顆錯誤加上修正沒有連成貫穿的線，剩下的只是穩定子本身（不影響邏輯資訊）。\n'
  '- 錯誤率掃描：p = 1%、5% 時邏輯錯誤率比 p 低（編碼有幫助）；p = 10% 以上反而比 p 高。這是 d = 3、只看 X、量測完美的簡化情況，真實電路的門檻約 1%。\n'
  '- d = 5 需要 2×25 − 1 = 49 顆，最多修 2 個錯誤；d = 7 需要 97 顆，最多修 3 個。\n'
  '- 數一數：d = 3 是 9 顆資料 + 8 顆量測 = 17 顆；一個週期是重設 → 4 層 CZ → 量測；青色格子的順序是左上 → 左下 → 右上 → 右下（琥珀色是左上 → 右上 → 左下 → 右下）；解碼器選總路徑最短（最少錯誤）的解釋。\n'
  '- 量奇偶為什麼不破壞疊加：|000⟩ 和 |111⟩ 的 Z₁Z₂ 都是 +1，量到的結果和 α、β 無關。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `transmon-3d.html#surface`（第 10 章：量子錯誤更正——表面碼）

- 圓球 = 資料位元 D1～D9（紅 X 錯誤、藍 Z 錯誤、紫 Y 錯誤）；小方塊 = 量測位元；青色格子 = Z 穩定子（抓 X 錯誤）、琥珀色格子 = X 穩定子（抓 Z 錯誤）；格子亮起 = 量到 −1；白線 = 解碼器的配對。
- 步驟 1～8：結構、一個週期（重設 → 4 層 CZ → 量測）、單一 X 錯誤（D5）、Z 與 Y 錯誤、邊界（D1）、邏輯錯誤（D1、D4）、碼距與閾值（d = 5）、自由實驗。「◀ 上一步」「暫停」「重播」「下一步 ▶」與「自動接續」。
- 自由實驗：點資料位元依序 X → Z → Y → 清除；碼距「3（17 顆）」「5（49 顆）」「7（97 顆）」；「錯誤率 p」滑桿；「解碼並修正」「隨機錯誤」「清除錯誤」「跑 300 次統計」「清除統計」。面板「亮起的穩定子」「最近一次解碼」。

## `operation.html#qec`（場景 11：雜訊與量子錯誤更正）

- 白球 = 資料量子位元、青色方塊 = Z 型穩定子、紫色 = X 型；亮橘色柱子 = 症狀；綠線 = 解碼器推測的錯誤鏈。本場景只示範 X 錯誤。
- 「d = 3」「d = 5」「d = 7」；「實體錯誤率 p（每個資料量子位元）」滑桿；「自動循環」「下一步」「跑 2000 輪（只統計）」。
- 右下插圖：即時蒙地卡羅的邏輯錯誤率 vs 實體錯誤率（藍 d = 3、橙 d = 5、紅 d = 7；虛線「未編碼 = p」；白色直線 = 目前的 p）。

## 操作

滑鼠拖曳旋轉、滾輪縮放；transmon-3d 下方可切換十二章，左右方向鍵也能換章。
''',
})

SHEET_HEADER = ['回合', '放錯的人', '錯誤（翻開前不看）', '亮的格子', '解碼的人猜：修哪一顆', '按解碼並修正的結果', '騙過了嗎']
SHEET_ROWS = [['1', '孩子', '', '', '', '', ''], ['2', '孩子', '', '', '', '', ''], ['3', '孩子', '', '', '', '', ''],
              ['4', '爸爸', '', '', '', '', ''], ['5', '爸爸', '', '', '', '', ''], ['6（兩個錯誤）', '孩子', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:17mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540}
table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}
pre.grid{font-size:13pt;line-height:1.5;margin:1mm 0 2mm;background:none;border:none}
.balls{font-size:11pt;color:#4a6a88;margin:1mm 0 3mm}'''


def check_program():
    """真的跑一次 surface_d3.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'surface_d3.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    single = ''.join(f'<tr><td class="k">{a}</td><td></td><td></td><td></td><td></td></tr>' for a, b, c, d in SINGLE)
    pages = [
        '<h2>表面碼解碼練習單</h2><p class="lead">在 transmon-3d.html#surface 按步驟「8」自由實驗：點資料位元注入錯誤，看哪些格子亮，再按「解碼並修正」。</p>'
        '<p>開場先猜：不量資料本身，怎麼知道哪一顆錯了？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<pre class="code grid">D1  D2  D3\nD4  D5  D6\nD7  D8  D9</pre>'
        '<p class="balls">青色格子 = Z 穩定子（抓 X 錯誤，點一下）；琥珀色格子 = X 穩定子（抓 Z 錯誤，點兩下）；Y = 點三下，兩色都亮。</p>'
        '<table class="judge"><tr><th style="width:16%">錯誤</th><th style="width:24%">亮的格子（位置、顏色）</th><th style="width:20%">我猜修哪一顆</th>'
        '<th style="width:20%">解碼器修哪一顆</th><th style="width:20%">最近一次解碼</th></tr>'
        + single + '</table>'
        '<p class="note">只亮一個格子時，落單的亮點配到哪裡？＿＿＿＿＿＿　解碼器看得到錯誤本身嗎？ □ 看得到　□ 只看得到亮點</p>',
        '<h2>Bug 獵人：兩個錯誤的騙局</h2><p class="lead">放錯的人偷偷點位元；解碼的人蓋住圓球、只看格子。找出兩個錯誤造成「邏輯錯誤」的例子。</p>'
        '<table class="rec"><tr><th>回合</th><th>放錯的人</th><th>錯誤</th><th>亮的格子</th><th>猜修哪一顆</th><th>解碼結果</th><th>騙過了？</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td></td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<pre class="code">MY_ERRORS = [1, 4]   # 改造區：自己注入錯誤（寫資料位元的編號），看哪些穩定子亮、解碼器怎麼修</pre>'
        '<p class="note">我找到的騙局：＿＿＿＿＿＿＿＿　程式說 36 種兩個錯誤裡有＿＿＿種騙局。騙局的錯誤加修正連成什麼形狀？＿＿＿＿＿＿</p>',
        '<h2>三個容易錯的地方</h2><div class="box"><ul class="chk">'
        '<li>以為表面碼會量資料位元：其實只量相鄰位元的奇偶，疊加不被破壞</li>'
        '<li>以為碼距越大一定越好：前提是實體錯誤率低於門檻（真實電路約 1%）</li>'
        '<li>以為 d = 3 能修所有錯誤：只保證修 1 個，兩個錯誤就可能騙過解碼器</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>數一數</h3>'
        '<p>d = 3：＿＿ 顆資料 + ＿＿ 顆量測 = ＿＿ 顆　　d = 5：2d² − 1 = ＿＿ 顆，最多修 ＿＿ 個錯誤</p>'
        '<p>一個週期：重設 → ＿＿ 層 CZ → 量測；青色格子的順序：左上 → ＿＿ → ＿＿ → 右下</p>'
        '<p>解碼器的原則：□ 錯誤最多的解釋　□ 總路徑最短（最少錯誤）的解釋</p>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>最後一關：教爸爸表面碼</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 為什麼量奇偶不會破壞疊加？</p><div class="line"></div>'
        '<p>2. 解碼器怎麼從亮點推回錯誤？落單的亮點怎麼辦？</p><div class="line"></div>'
        '<p>3. 碼距越大越好嗎？前提是什麼？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>不看稿說出：只量奇偶、亮點配對、修正</li><li>在自由實驗示範 D5 單一錯誤與 D1、D4 的騙局，並解釋格子為什麼亮</li>'
        '<li>說出極限：d = 3 只保證修 1 個錯誤</li><li>指出一個限制：低於門檻，碼距越大才越好</li>'
        '<li>替表面碼解碼練習單取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q109 表面碼解碼練習單 列印包', '父子科技學院 量子電腦學程 Q109｜第 11 課：表面碼——穩定子與匹配解碼', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q109-surface-code', folder='Q109_表面碼穩定子與匹配解碼', files=FILES,
        sheet=('03_騙局紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_表面碼解碼練習單.pdf', pack_pages=4,
        pack_needles=('表面碼解碼練習單', '解碼並修正', '騙局', 'MY_ERRORS', '容易錯', '門檻', '最後一關'),
        authoring_dir=XINEW / 'authoring/q109', episode_dir='specials/q109-surface-code',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；surface_d3.py 只需 Python 3）',
               'program': 'surface_d3.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'singleErrorsCorrected': 9, 'twoErrorLogicalFailures': 18, 'twoErrorCombos': 36,
                               'logicalRatePercent': {'1': 0.17, '5': 3.69, '10': 11.97, '20': 30.84, '30': 43.85},
                               'myErrors_D1_D4': '邏輯錯誤'},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q109/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

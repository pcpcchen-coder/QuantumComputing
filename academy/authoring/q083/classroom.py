"""Q083 課堂教材：重複碼：最簡單的錯誤更正 — 硬幣偵探遊戲、症狀解碼表、翻兩枚實驗、邏輯錯誤率計算、說明卡與解答。

免安裝、不需帳號：三枚硬幣；選用學程的 animations/transmon-3d.html#surface（第 10 章步驟 ③、⑥）當延伸觀看。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q083/classroom.py
"""
from itertools import product
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 症狀：s1 = 第一、二枚是否不同；s2 = 第二、三枚是否不同（1 = 不同）。解碼表：症狀 → 要翻哪一枚（0 = 不翻）
DECODE = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}
SYN_TXT = {0: '同', 1: '異'}


def syndrome(f):
    return (f[0] ^ f[1], f[1] ^ f[2])


# 八種翻法（從 000 出發，1 = 被翻）→ 症狀 → 解碼器翻哪一枚 → 修完的結果
PATTERNS = []
for f in product((0, 1), repeat=3):
    s = syndrome(f)
    k = DECODE[s]
    out = list(f)
    if k:
        out[k - 1] ^= 1
    PATTERNS.append((''.join(map(str, f)), sum(f), s, k, ''.join(map(str, out))))
for pat, n, s, k, out in PATTERNS:
    assert (out == '000') == (n <= 1), (pat, out)   # 翻 0、1 枚修得回來；翻 2、3 枚變成 111（邏輯錯誤）


def p_logical(p):
    return 3 * p * p * (1 - p) + p ** 3     # = 3p² − 2p³（維基百科 Quantum error correction：成功機率 1 − 3p² + 2p³）


PS = [0.01, 0.05, 0.10, 0.20, 0.50, 0.60]
RATES = [(p, p_logical(p)) for p in PS]
assert abs(p_logical(0.10) - 0.028) < 1e-12
assert abs(p_logical(0.50) - 0.50) < 1e-12 and p_logical(0.60) > 0.60


def pct(x):
    return f'{100 * x:.3g}%'


TABLE_MD = ''.join(f'| {pat} | {n} | {SYN_TXT[s[0]]}、{SYN_TXT[s[1]]} | {"不翻" if k == 0 else f"第 {k} 枚"} | {out} | {"✓" if out == "000" else "✗ 邏輯錯誤"} |\n'
                   for pat, n, s, k, out in PATTERNS)

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q083：重複碼：最簡單的錯誤更正（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：量子資料不能抄、也不能偷看，那怎麼抓錯、修錯？答案是重複碼加上「只比較、不讀出」的症狀量測。

只需要三枚硬幣、列印包和筆。想看動畫的話，用瀏覽器開學程的 `animations/transmon-3d.html#surface`，按步驟 3 和 6（不需要網路、帳號或安裝）。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 古典重複碼、不可複製、症狀量測、解碼表 | 影片第 3–7 段 |
| 25–65 | 硬幣偵探辦案十回合，完成症狀解碼表 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 同時翻兩枚：八種翻法全部試一次，算邏輯錯誤率 | 列印包第 3 頁、`03_偵探與錯誤率紀錄.csv` |
| 105–115 | 孩子教爸爸：怎麼編碼、症狀怎麼量、哪裡會錯 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 準備三枚一樣的硬幣，正面朝上代表 0、反面代表 1。
- 列印 `02_列印包_重複碼.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 偵探辦案怎麼玩

孩子轉身。爸爸把三枚硬幣排成「正正正」，偷偷翻其中一枚（也可以都不翻），然後只說兩句：「第一和第二枚：同／不同」「第二和第三枚：同／不同」。孩子用解碼表指出嫌犯，最後轉身看硬幣對答案。

## 誠實說明

- 硬幣是古典的：真的量子位元不能複製，也不能直接看；硬幣遊戲只模擬「只聽症狀」這個規則。
- 量子的三位元重複碼只防位元翻轉，防不了相位翻轉；同時翻兩枚以上就會修錯。
- 邏輯錯誤率的公式假設每枚獨立、被翻機率相同，而且症狀量測本身不出錯。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 先建立症狀解碼表（約 10 分鐘）

1. 三枚硬幣排成「正正正」（000）。
2. 依序只翻第一枚、只翻第二枚、只翻第三枚、都不翻。每次寫下兩個答案：第一和第二枚同不同？第二和第三枚同不同？
3. 把四種答案填進列印包第 1 頁的症狀解碼表：症狀 → 嫌犯 → 要翻回哪一枚。

## B. 偵探辦案（約 25 分鐘，十回合）

爸爸照「00_爸爸先讀」出題，孩子只聽兩個答案判斷，記在列印包第 2 頁。

## C. 延伸：看動畫裡的偵探（選用，約 5 分鐘）

開 `transmon-3d.html#surface`，先取消「自動接續」，按步驟 3：正中間一顆被翻成紅色，旁邊兩塊格子亮起；解碼器用白線配對，修回來。這是下一堂的表面碼，但「只看哪裡不一樣」的想法和今天一樣。

## D. 下半場：同時翻兩枚（約 30 分鐘）

1. 用列印包第 3 頁，把八種翻法（000 到 111）一一擺出來，照解碼表修，看修完是不是回到 000。
2. 數一數：翻兩枚有幾種？翻三枚有幾種？
3. 用公式 3p²(1−p) + p³ 算 p = 1%、5%、10%、20%、50% 的邏輯錯誤率，和不編碼的 p 比較。
4. 動畫延伸：步驟 6 看兩個錯誤怎麼騙過解碼器。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 症狀解碼表\n\n| 第一、二枚 | 第二、三枚 | 嫌犯 | 修正 |\n|---|---|---|---|\n'
  '| 同 | 同 | 沒有 | 不翻 |\n| 異 | 同 | 第 1 枚 | 翻回第 1 枚 |\n| 異 | 異 | 第 2 枚 | 翻回第 2 枚 |\n| 同 | 異 | 第 3 枚 | 翻回第 3 枚 |\n\n'
  '## 八種翻法（從 000 出發）\n\n| 被翻的位置 | 翻幾枚 | 症狀 | 解碼器翻 | 修完 | 結果 |\n|---|---|---|---|---|---|\n'
  + TABLE_MD
  + '\n翻 0 或 1 枚都修得回來；翻 2 枚時症狀指向剩下那一枚，修完變成 111；翻 3 枚時症狀全是「同」，根本不修，也是 111。\n\n'
  '## 邏輯錯誤率\n\n修錯 = 翻兩枚（3 種挑法）或翻三枚（1 種）：P = 3p²(1−p) + p³ = 3p² − 2p³。\n\n| 每枚被翻的機率 p | 不編碼 | 三位元重複碼 |\n|---|---|---|\n'
  + ''.join(f'| {pct(p)} | {pct(p)} | {pct(r)} |\n' for p, r in RATES)
  + '\np 小於一半時編碼比較好；p = 50% 時打平；p 大於一半時編碼反而更糟。\n\n'
  '## 常見問題\n\n'
  '- 為什麼不能把量子位元抄三份？不可複製定理：未知的量子態不能複製。重複碼是用兩個受控反閘把 α|0⟩ + β|1⟩ 編成 α|000⟩ + β|111⟩，這是糾纏，不是三份副本。\n'
  '- 為什麼症狀量測不會破壞疊加？000 和 111 兩兩比較的答案完全一樣，量到的只有「哪裡不同」，和 α、β 無關。\n'
  '- 為什麼還需要表面碼？三位元重複碼只防位元翻轉；相位翻轉是量子才有的錯誤，要另外處理（下一堂）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。本課沒有重複碼專用場景，借用表面碼章節的兩個步驟來看「症狀」與「被騙」。

## `transmon-3d.html#surface`（第 10 章：表面碼）

- 上方步驟按鈕 1–8；「播放／暫停」「重播」「下一步」；「自動接續」勾選時會自動跳到下一步。
- 步驟 3「單一 X 錯誤」：正中間的資料位元變紅（位元翻轉），旁邊兩塊青色格子亮起；解碼器用白線配對，在中間補一次翻轉。
- 步驟 6「邏輯錯誤」：相鄰兩顆同時被翻，只亮一塊邊上的半圓格子；解碼器去翻第三顆，結果三顆連成一條紅線，出現「邏輯錯誤」。
- 步驟 8「自由實驗」：自己點資料位元注入錯誤，再按「解碼並修正」。

## 操作

滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '爸爸翻了哪一枚', '第一、二枚同不同', '第二、三枚同不同', '我的判斷', '對嗎', 'p', '邏輯錯誤率', '備註']
SHEET_ROWS = ([[f'偵探第 {i} 回合', '', '', '', '', '', '', '', ''] for i in range(1, 11)]
              + [[f'翻法 {pat}', pat, '', '', '', '', '', '', ''] for pat, *_ in PATTERNS]
              + [['錯誤率計算', '', '', '', '', '', f'{pct(p)}', '', ''] for p in PS])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>症狀解碼表（今天的作品）</h2><p class="lead">三枚硬幣正面朝上＝000。只翻一枚（或都不翻），寫下兩個答案：同或異。</p>'
        '<table class="rec"><tr><th>爸爸翻了</th><th>第一、二枚</th><th>第二、三枚</th><th>嫌犯</th><th>要怎麼修</th></tr>'
        + ''.join(f'<tr><td>{w}</td><td></td><td></td><td></td><td></td></tr>' for w in ('都不翻', '第 1 枚', '第 2 枚', '第 3 枚')) + '</table>'
        '<div class="card"><h3>症狀解碼表</h3><p>同、同 → ＿＿＿＿　異、同 → ＿＿＿＿</p><p>異、異 → ＿＿＿＿　同、異 → ＿＿＿＿</p>'
        '<p>為什麼只問「同不同」？</p><div class="line"></div><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>偵探辦案：誰被翻了</h2><p class="lead">你轉身，只聽爸爸說兩個答案。用解碼表指出嫌犯，再轉身看硬幣。</p>'
        '<table class="rec"><tr><th>回合</th><th>第一、二枚</th><th>第二、三枚</th><th>我說嫌犯是</th><th>真正翻的</th><th>對嗎</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 11)) + '</table>'
        '<p class="note">猜對幾次？＿＿　有沒有哪一回爸爸其實翻了兩枚？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：同時翻兩枚會怎樣</h2><p class="lead">從 000 出發，八種翻法都擺一次，照解碼表修，看修完是不是 000。</p>'
        '<table class="rec"><tr><th>翻法</th><th>症狀</th><th>解碼器翻</th><th>修完</th><th>修好了嗎</th></tr>'
        + ''.join(f'<tr><td>{pat}</td><td></td><td></td><td></td><td></td></tr>' for pat, *_ in PATTERNS) + '</table>'
        '<p>修錯的翻法有幾種？翻兩枚＿＿種、翻三枚＿＿種　邏輯錯誤率 = 3p²(1−p) + p³</p>'
        '<p>p = 10%：＿＿＿%　p = 20%：＿＿＿%　p = 60%：＿＿＿%（比 60% 好還是壞？）</p>'
        '<p class="note">生活技能：用冗餘保護重要資訊——你最重要的檔案存了幾份？放在幾個地方？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 量子的重複碼怎麼編碼？為什麼不是抄三份？</p><div class="line"></div>'
        '<p>2. 症狀怎麼量？為什麼不會破壞疊加？</p><div class="line"></div><p>3. 同時翻兩枚會怎樣？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出編碼：0 → 000、1 → 111，靠受控反閘，不是複製</li><li>說出症狀：兩兩比較，只說哪裡不同</li>'
        '<li>用解碼表抓出一個嫌犯</li><li>指出一個限制：只防翻轉，錯兩顆就修錯</li>'
        '<li>替症狀解碼表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q083 重複碼列印包', '父子科技學院 量子電腦學程 Q083｜重複碼：最簡單的錯誤更正', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q083-repetition-code', folder='Q083_重複碼', files=FILES,
        sheet=('03_偵探與錯誤率紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_重複碼.pdf', pack_pages=4,
        pack_needles=('症狀解碼表', '偵探辦案', '同時翻兩枚', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q083', episode_dir='specials/q083-repetition-code',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/transmon-3d.html#surface'],
               'logicalErrorRate': {pct(p): round(r, 6) for p, r in RATES}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q083/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

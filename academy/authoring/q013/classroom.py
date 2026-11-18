"""Q013 課堂教材：尋寶比賽規則與預測、尋寶比賽結果表、64 個抽屜改造表、說明卡、解答、grover_rounds.py、動畫導覽。

不需要帳號，也不需要安裝套件（grover_rounds.py 只要 Python 3）；動畫用瀏覽器開啟 animations/operation.html#grover。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q013/classroom.py
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


def rounds(n_drawers, treasure, k):
    """和 animations/js/operation/09_grover.js 相同：標記＝寶藏變號；擴散＝a → 2×平均 − a。回傳第 0..k 輪寶藏的機率。"""
    amp = [1 / math.sqrt(n_drawers)] * n_drawers
    out = [amp[treasure] ** 2]
    for _ in range(k):
        amp[treasure] = -amp[treasure]
        m = sum(amp) / n_drawers
        amp = [2 * m - a for a in amp]
        out.append(amp[treasure] ** 2)
    return out


P16, P64, P4 = rounds(16, 11, 8), rounds(64, 11, 8), rounds(4, 3, 3)
# 製作代理實跑（Python 3）：與 source-notes.md 的紀錄相同
assert [round(p, 3) for p in P16[1:6]] == [0.473, 0.908, 0.961, 0.582, 0.125]
assert round(P64[6], 3) == 0.997 and round(P4[1], 3) == 1.0 and round(P4[2], 3) == 0.25
EST = {n: math.floor(0.785 * math.sqrt(n)) for n in (4, 16, 64)}
assert EST == {4: 1, 16: 3, 64: 6}

PROGRAM = '''"""父子科技學院 量子電腦學程 Q013：格羅弗搜尋——每一輪之後，寶藏的機率是多少？

不用安裝任何套件，只要 Python 3。執行：  python grover_rounds.py
想改抽屜數，就改下面的 N（16、64、4……）；寶藏的號碼改 TREASURE（要在 0 到 N-1 之間）。
算法和學程動畫 operation.html#grover 相同：標記＝寶藏的振幅變號；擴散＝每個振幅 a 變成 2×平均−a。
"""
import math

N = 16          # 抽屜數
TREASURE = 11   # 寶藏在幾號抽屜（0 到 N-1）
ROUNDS = 8      # 要算到第幾輪

assert 0 <= TREASURE < N, '寶藏的號碼要在 0 到 N-1 之間'
amp = [1 / math.sqrt(N)] * N        # 一開始每根柱子一樣高
print(f'N = {N}，估算：√N × 0.785 ≈ {0.785 * math.sqrt(N):.2f}，去掉小數 → {math.floor(0.785 * math.sqrt(N))} 輪；古典平均約要翻 {N / 2:.0f} 次')
print(f'第 0 輪：寶藏的機率 {amp[TREASURE] ** 2:.3f}')
for r in range(1, ROUNDS + 1):
    amp[TREASURE] = -amp[TREASURE]                   # 標記：寶藏翻到下面
    mean = sum(amp) / N
    amp = [2 * mean - a for a in amp]                # 擴散：對平均值翻過去
    print(f'第 {r} 輪：寶藏的機率 {amp[TREASURE] ** 2:.3f}')
'''


def pct(p):
    return f'{p * 100:.1f}%'


FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q013：格羅弗搜尋——16 個抽屜找寶藏（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：用 16 個信封玩尋寶比賽，比較「一個一個翻」和「照動畫做格羅弗搜尋」各要幾次，再把抽屜改成 64 個，預測最好的輪數並驗證。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 振幅柱子、一輪兩步（標記＋擴散）、為什麼約 √N、轉太多反而變差；寫下預測 | 影片第 3–8 段、列印包第 1 頁 |
| 25–65 | 尋寶比賽：隨機隊翻信封、量子隊用動畫做三輪再測量；量子隊再試四輪、五輪 | `01_操作步驟.md`、列印包第 2 頁、`03_尋寶比賽結果表.csv` |
| 65–75 | 休息 | |
| 75–105 | 改成 64 個抽屜：先用口訣預測，再用動畫（或 `grover_rounds.py`）驗證 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：一輪兩步、為什麼三輪最好、限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 16 個信封（或紙杯、撲克牌背面朝上），寫上編號 0–15；一張小貼紙或硬幣當寶藏。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#grover`（場景 9：Grover 搜尋），先自己按一次「自動跑到最佳次數」。
- 列印 `02_列印包_格羅弗尋寶.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 有電腦可以跑 Python 3 的話，先執行一次 `grover_rounds.py`（不需要安裝套件）。

## 比賽的原則

- 量子隊「看一次」是真的隨機：做三輪後約 96% 會中，五次裡偶爾會有一次沒中，這很正常。
- 隨機隊的次數每次都不一樣，玩五次才看得出平均；16 個信封的平均約 8.5 次。
- 讓孩子自己決定量子隊要做幾輪，做太多輪時讓他親眼看到機率掉下來，比直接告訴他更有效。

## 誠實說明

- 動畫和程式算的是理想的振幅，沒有雜訊；真的量子電腦還會有誤差。
- 信封遊戲裡沒有真正的量子：量子隊的「中不中」是動畫依機率抽出來的。
- 格羅弗搜尋要先有能「認得寶藏」的檢查器（Oracle）；遊戲裡由動畫的「答案」滑桿代替，真實問題中做出這個檢查器往往是最難的部分。
- 「乘 0.785 再去掉小數」是估算口訣，在 4、16、64 個抽屜都和動畫算出的最佳輪數相同，但不保證每個數字都相同。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：16 個信封尋寶比賽（約 40 分鐘）

1. 先在列印包第 1 頁寫預測：隨機隊平均要翻幾次？量子隊做幾輪最好？
2. 爸爸背著孩子，把寶藏放進其中一個信封，記下號碼（例如 11 號）。
3. 隨機隊：孩子一個一個翻信封，數翻到第幾個才找到。記在列印包第 2 頁。
4. 量子隊：打開 `animations/operation.html#grover`，把「答案（標記的項目）」滑桿調到同一個號碼。
   按「完整一輪」三次（看讀數的「第 3 輪」），再按「測量」一次：讀數最後一行出現「✓ 找到了」或「✗」。
5. 每一隊玩五次（每次重新藏寶藏；量子隊每次先按「重設」）。
6. 量子隊加碼：故意做四輪、五輪再測量，記下讀數上的「答案的機率 P」。

## 下半場：64 個抽屜（約 30 分鐘）

1. 先預測：√64 = 8，乘 0.785，去掉小數 → 第幾輪最好？寫在列印包第 3 頁。
2. 把「量子位元數 n」滑桿調到 6（N = 64）。
3. 按「完整一輪」一次一次做，把每一輪的「答案的機率 P」抄進表格，找出最高的那一輪。
4. 也可以按「自動跑到最佳次數」，看它停在第幾輪；或執行 `grover_rounds.py`，把 N 改成 64。
5. 和古典方法比一比：64 個抽屜平均要翻幾次？
''',

'grover_rounds.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 16 個抽屜（寶藏 11 號；grover_rounds.py 實跑）\n\n| 輪數 | 寶藏的機率 |\n|---|---|\n'
  + ''.join(f'| 第 {i} 輪 | {p:.3f}（{pct(p)}） |\n' for i, p in enumerate(P16[:7]))
  + f'\n最好是第 3 輪（約 96%）；第 4 輪掉到 {pct(P16[4])}、第 5 輪只剩 {pct(P16[5])}。' + '估算：√16 = 4，×0.785 = 3.14，去掉小數 → 3 輪。\n'
  '隨機隊：16 個信封平均約 8.5 次（最少 1 次、最多 16 次；翻到第 15 個還沒中，其實就知道是最後一個了）。\n\n'
  '## 64 個抽屜\n\n| 輪數 | 寶藏的機率 |\n|---|---|\n'
  + ''.join(f'| 第 {i} 輪 | {p:.3f}（{pct(p)}） |\n' for i, p in enumerate(P64[:9]))
  + '\n最好是第 6 輪（約 99.7%）。估算：√64 = 8，×0.785 = 6.28，去掉小數 → 6 輪。古典平均約 32 次。抽屜 4 倍（16 → 64），輪數 2 倍（3 → 6）。\n\n'
  '## 暫停題：4 個抽屜\n\n'
  f'做 1 輪就是 {pct(P4[1])}；做 2 輪掉回 {pct(P4[2])}，和一開始一樣，轉過頭了。估算：√4 = 2，×0.785 = 1.57，去掉小數 → 1 輪。\n\n'
  '## 常見問題\n\n'
  '- 標記之後為什麼機率沒變？機率是振幅的平方，寶藏從 +0.25 變成 −0.25，平方還是 1/16。\n'
  '- 擴散在做什麼？先算所有柱子的平均，再把每根柱子以平均當鏡子翻過去：新高度 = 2 × 平均 − 原高度。寶藏在平均下面最遠，翻上來就最高。\n'
  '- 為什麼會轉過頭？每一輪都把狀態往寶藏轉一個固定角度；轉過了寶藏的方向，再轉就越離越遠。\n'
  '- 是指數加速嗎？不是。古典約 N/2 次，格羅弗約 0.785×√N 輪，是平方根加速；而且已經證明黑盒搜尋不可能更快。\n'
  '- 檢查器（Oracle）從哪來？要先能把「是不是寶藏」寫成量子線路。遊戲裡是動畫的「答案」滑桿；真實問題中，做出檢查器往往是最難的部分。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#grover`（場景 9：Grover 搜尋——振幅放大）

- 柱子高度是振幅（可以是負的）：正的是橘色、負的是藍色。綠框和「答案」標籤是寶藏。
- 「量子位元數 n」滑桿：2–6（N = 4、8、16、32、64）；「答案（標記的項目）」滑桿：寶藏的號碼。
- 「② Oracle」：寶藏翻到下面；粉紅色平面是平均振幅。「③ 擴散」：每根柱子對平均翻過去。「完整一輪」＝兩步一起做。
- 「自動跑到最佳次數」：從頭開始，一輪一輪做到最佳輪數就停。「測量」：依機率抽一個結果。「重設」：回到一開始。
- 左邊面板的讀數：第幾輪、答案的機率 P、最佳輪數、古典平均要查幾次、測量結果。
- 右下插圖：左邊是每輪轉 2θ 的幾何圖，右邊是「P(成功) vs 輪數」曲線，白點是目前的輪數。

## `animations/basic-circuits.html#grover`（八個基礎量子電路：Grover）

- 可選 2 顆（4 個）或 3 顆（8 個）位元、點選答案、重複 1–3 輪；綠色虛線是平均值。
- 選 3 顆、3 輪，說明文字會提醒「轉過頭了」。

## `animations/transmon-3d.html#grover`（第 7 章：振幅長條）

- 步驟 ②–⑥ 是 4 個選項的格羅弗搜尋：一輪就 100%，再多做一輪又回到各 25%。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放（operation.html）。
''',
}

SHEET_HEADER = ['隊伍', '第幾次', '寶藏號碼', '做了幾輪（量子隊）', '翻了幾次／看了幾次', '找到了嗎', '答案的機率 P（量子隊）', '備註']
SHEET_ROWS = ([['隨機隊', str(i)] for i in range(1, 6)] + [['量子隊', str(i), '', '3'] for i in range(1, 6)]
              + [['量子隊加碼', '1', '', '4'], ['量子隊加碼', '2', '', '5']])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.env{display:grid;grid-template-columns:repeat(8,1fr);gap:2.5mm;margin:3mm 0}.env div{border:1.2pt solid #0b2540;border-radius:2mm;height:13mm;
display:flex;align-items:center;justify-content:center;font-size:13pt}'''


def html():
    env = ''.join(f'<div>{i}</div>' for i in range(16))
    pages = [
        '<h2>尋寶比賽：規則和預測</h2><p class="lead">16 個信封，只有一個藏著寶藏。隨機隊一個一個翻；量子隊用動畫做格羅弗搜尋。</p>'
        f'<div class="env">{env}</div>'
        '<div class="box"><h3>規則</h3><p>1. 爸爸偷偷把寶藏放進一個信封，記下號碼。</p>'
        '<p>2. 隨機隊：一個一個翻，數翻到第幾個才找到。</p>'
        '<p>3. 量子隊：動畫的「答案」調成同一個號碼，按「完整一輪」三次，再按「測量」一次，看中不中。</p>'
        '<p>4. 每隊玩五次，記在第 2 頁。</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>先預測</h3><p>隨機隊平均要翻大約＿＿次。</p>'
        '<p>量子隊做＿＿輪最好，那時寶藏的機率大約＿＿％。</p><p>如果做到第 5 輪，我猜機率會：□ 更高　□ 一樣　□ 變低</p>'
        '<p>我為什麼這樣猜：</p><div class="line"></div></div>',
        '<h2>尋寶比賽結果表</h2><p class="lead">每隊玩五次。量子隊記下讀數上的「答案的機率 P」。</p>'
        '<table class="rec"><tr><th>次</th><th>隨機隊：翻了幾次</th><th>量子隊：做幾輪</th><th>量子隊：中了嗎</th><th>答案的機率 P</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td>3</td><td></td><td></td></tr>' for i in range(1, 6))
        + '<tr><td>平均</td><td></td><td></td><td>中了＿次</td><td></td></tr></table>'
        '<h3 style="margin-top:5mm">量子隊加碼：故意多做幾輪</h3>'
        '<table class="rec"><tr><th>做幾輪</th><th>答案的機率 P</th><th>中了嗎</th></tr>'
        + ''.join(f'<tr><td>{k} 輪</td><td></td><td></td></tr>' for k in (1, 2, 3, 4, 5)) + '</table>'
        '<p class="note">第幾輪的機率最高？多做之後發生什麼事？＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：64 個抽屜</h2><p class="lead">先預測，再把動畫的「量子位元數 n」調到 6 驗證。</p>'
        '<div class="box"><h3>先預測</h3><p>√64 ＝＿＿；×0.785 ＝＿＿；去掉小數 → 第＿＿輪最好。</p>'
        '<p>古典方法平均要翻大約＿＿次。</p></div>'
        '<table class="rec" style="margin-top:4mm"><tr><th>輪數</th>' + ''.join(f'<th>{k}</th>' for k in range(9)) + '</tr>'
        '<tr><td>答案的機率 P</td>' + '<td></td>' * 9 + '</tr></table>'
        '<p class="note">16 個抽屜最好是第＿＿輪；64 個是第＿＿輪。抽屜變成＿＿倍，輪數變成＿＿倍。</p>'
        '<div class="box" style="margin-top:4mm"><h3>挑戰</h3><p>4 個抽屜做 1 輪、2 輪，機率各是多少？（試著把量子位元數調到 2）</p>'
        '<div class="line"></div><p>32 個抽屜（量子位元數 5）：我預測第＿＿輪最好，實際是第＿＿輪。</p></div>',
        '<h2>說明卡：我的尋寶比賽</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 格羅弗搜尋每一輪做哪兩步？</p><div class="line"></div><p>2. 為什麼 16 個抽屜做 3 輪最好？</p><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出一輪兩步：標記、擴散</li><li>用手比出「對平均值翻過去」</li>'
        '<li>說出 16 個抽屜約 3 輪、64 個約 6 輪</li><li>說出為什麼做太多輪反而變差</li>'
        '<li>指出一個限制：平方根加速，不是指數；要先做得出檢查器</li><li>替結果表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q013 格羅弗尋寶 列印包', '父子科技學院 量子電腦學程 Q013｜格羅弗搜尋：16 個抽屜找寶藏', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q013-grover-treasure', folder='Q013_格羅弗尋寶', files=FILES,
        sheet=('03_尋寶比賽結果表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_格羅弗尋寶.pdf', pack_pages=4,
        pack_needles=('尋寶比賽', '先預測', '結果表', '64 個抽屜', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q013', episode_dir='specials/q013-grover-treasure',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（grover_rounds.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'grover_rounds.py', 'recordedRun': {'N16': [round(p, 3) for p in P16[:6]], 'N64_round6': round(P64[6], 3)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q013/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

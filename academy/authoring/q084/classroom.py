"""Q084 課堂教材：表面碼 — 動畫操作步驟、解碼練習單、抓蟲遊戲紀錄、會騙人的錯誤組合、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/transmon-3d.html（#surface）與 animations/operation.html（#qec），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q084/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 碼距 d：實體位元 2d² − 1、可修正 ⌊(d−1)/2⌋ 個、最少幾個錯誤可能騙過解碼器（⌊(d−1)/2⌋ + 1）
DIST = [(d, d * d, d * d - 1, 2 * d * d - 1, (d - 1) // 2, (d - 1) // 2 + 1) for d in (3, 5, 7)]
assert [r[3] for r in DIST] == [17, 49, 97]
# 以 transmon-3d.html 第 10 章自己的解碼器（decodeType）窮舉只有 X 錯誤的情況（製作代理以 node 重跑）
FOOL_D3_PAIRS = [(1, 4), (1, 5), (1, 7), (1, 8), (1, 9), (2, 4), (2, 5), (2, 7), (2, 8), (2, 9),
                 (3, 6), (3, 8), (3, 9), (4, 7), (5, 8), (5, 9), (6, 8), (6, 9)]
assert len(FOOL_D3_PAIRS) == 18           # 36 組雙錯誤中有 18 組騙過碼距 3
FOOL_D5_TRIPLES = 292                     # 碼距 5：沒有任何雙錯誤騙得過；2300 組三錯誤中 292 組會

GRID = ('<table class="grid"><tr><td>D1</td><td>D2</td><td>D3</td></tr><tr><td>D4</td><td>D5</td><td>D6</td></tr>'
        '<tr><td>D7</td><td>D8</td><td>D9</td></tr></table>')

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q084：表面碼（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出三件事：資料位元和量測位元、錯誤留下的症狀、解碼器怎麼把症狀配對。

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `transmon-3d.html#surface` 和 `operation.html#qec`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 資料位元、量測位元、一輪檢查、症狀、最小權重配對 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 看第 10 章步驟 ①–⑥，再玩抓蟲遊戲：爸爸藏錯、孩子配對、和解碼器比 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子當出題者：找出會騙過解碼器的錯誤組合 | 列印包第 3 頁、`03_抓蟲與改造紀錄.csv` |
| 105–115 | 孩子教爸爸：為什麼只量奇偶、解碼怎麼做 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `transmon-3d.html#surface` 看一次步驟 ①、③、⑥，再到 ⑧ 自由實驗點幾顆資料位元、按「解碼並修正」。
- 列印 `02_列印包_表面碼.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 抓蟲遊戲怎麼玩

孩子背對螢幕。爸爸在 ⑧ 自由實驗（碼距 3）點一兩顆資料位元：點一次是 X（翻轉，紅）、兩次 Z（相位，藍）、三次 Y（紫）、四次清除。
建議先只用 X。爸爸把亮起來的格子畫在練習單的方格上，孩子只看亮點，自己配對、圈出猜的錯誤位置；最後爸爸按「解碼並修正」，三方對照。

## 誠實說明

- 動畫只讓資料位元出錯、量測完美；真實電路的閘與量測也會錯。
- 「一輪約 1 微秒」「一顆可靠的邏輯位元要數百到上千顆實體位元」是學程簡報與文件的代表值和估計。
- 錯誤率與門檻（碼距越大是否越好）留到下一堂 Q085。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 看表面碼的結構與一個錯誤（`transmon-3d.html#surface`，約 15 分鐘）

1. 開啟後會自動播放步驟 ①「結構」：9 顆資料位元（圓球）、8 顆量測位元（小方塊）；青色格子抓 X（翻轉）錯誤、琥珀色格子抓 Z（相位）錯誤。
2. 按步驟 ②：看量測位元重設、4 層兩位元閘、量測。
3. 按步驟 ③：D5 變紅，兩塊青色格子亮；白線配對後 D5 被修正。把亮點畫在列印包第 1 頁。
4. 按步驟 ④、⑤：Z 與 Y 錯誤、邊上的錯誤配到邊界。
5. 按步驟 ⑥：D1、D4 兩個錯誤騙過解碼器，變成邏輯錯誤。

## B. 抓蟲遊戲（約 20 分鐘，至少八回合）

按步驟 ⑧ 自由實驗，照「00_爸爸先讀」玩；每回合記在列印包第 2 頁。

## C. 碼距 7 的一輪（`operation.html#qec`，約 5 分鐘）

1. 關掉「自動循環」，按「d = 7」，把「實體錯誤率」調到 10% 左右。
2. 按「下一步」四次：紅球（錯誤）→ 橘柱（症狀）→ 綠線（配對）→ 修正。紫色方塊只管相位錯誤，這個場景不會亮。

## D. 下半場：找會騙人的組合（約 30 分鐘）

1. 在 ⑧ 自由實驗（碼距 3），只用 X 錯誤，試各種兩顆的組合，按「解碼並修正」；畫面出現「邏輯錯誤」就記下來。
2. 按「5（49 顆）」換碼距 5，兩顆還騙得過嗎？至少要幾顆？
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 碼距與資源\n\n'
  '| 碼距 | 資料位元 | 量測位元 | 實體位元合計 | 最多可修正 | 最少幾個錯誤可能騙過 |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {d} | {a} | {b} | {n} | {c} 個 | {f} 個 |\n' for d, a, b, n, c, f in DIST)
  + '\n## 碼距 3：哪些兩顆 X 錯誤會騙過解碼器？\n\n'
  '以動畫第 10 章自己的解碼器窮舉（只放 X 錯誤），36 組兩顆組合中有 18 組會變成邏輯錯誤：\n\n'
  + '、'.join(f'D{a}+D{b}' for a, b in FOOL_D3_PAIRS) + '\n\n'
  '動畫步驟 ⑥ 示範的是 D1+D4：解碼器只看到左側一個亮點，修了 D7，結果 D1、D4、D7 整條都翻了。\n'
  f'碼距 5：沒有任何兩顆組合騙得過；2300 組三顆組合中有 {FOOL_D5_TRIPLES} 組會。\n\n'
  '## 常見問題\n\n'
  '- 為什麼只量奇偶？直接量資料會讓疊加塌縮；量奇偶得到的結果和資料本身無關，所以不破壞量子資訊。\n'
  '- 為什麼不把資料複製三份？量子態不能複製；表面碼是把資訊分散在很多位元的糾纏態裡。\n'
  '- 為什麼選總路徑最短的配對？錯誤率低的時候，錯得少的情況最常見；這也是它會被「排得剛好」的錯誤騙過的原因。\n'
  '- 一個邏輯位元要多少實體位元？碼距 3 是 17 顆；真正可靠的邏輯位元估計要數百到上千顆（例如對話紀錄：p = 0.1%、目標 10⁻¹² 約 880 顆）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `transmon-3d.html#surface`（transmon 3D 第 10 章：量子錯誤更正：表面碼）

- 步驟按鈕 1–8：① 結構 ② 一個週期 ③ 單一 X 錯誤 ④ Z 與 Y 錯誤 ⑤ 邊界 ⑥ 邏輯錯誤 ⑦ 碼距與閾值 ⑧ 自由實驗。
- 圖例：圓球＝資料位元（紅 X、藍 Z、紫 Y 錯誤）；小方塊＝量測位元；青色格子＝Z 穩定子（抓 X 錯誤）、琥珀色＝X 穩定子（抓 Z 錯誤）；格子亮起＝量到 −1；白線＝解碼器的配對。
- 自由實驗：點資料位元注入錯誤（X → Z → Y → 清除）、「解碼並修正」、碼距 3／5／7、「隨機錯誤」、「跑 300 次統計」。
- 勾選「自動接續」時，每一步播完會自動進下一步。

## `operation.html#qec`（操作場景 11：雜訊與量子錯誤更正）

- 單選 d = 3／5／7；滑桿「實體錯誤率 p」；開關「自動循環」；「下一步」；「跑 2000 輪（只統計）」。
- 白球＝資料量子位元、青色方塊＝Z 型、紫色＝X 型；紅球＝錯誤、橘色柱＝症狀、綠線＝解碼器推測的錯誤鏈。
- 右下插圖是邏輯錯誤率與實體錯誤率的即時模擬（下一堂 Q085 再用）。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '碼距', '爸爸放的錯誤', '亮起的格子', '我的配對與猜測', '解碼器的修正', '誰對', '是否邏輯錯誤', '備註']
SHEET_ROWS = ([[f'抓蟲第 {i} 回合', '3', '', '', '', '', '', '', ''] for i in range(1, 9)]
              + [[f'改造第 {i} 組', '', '', '', '', '', '', '', ''] for i in range(1, 7)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}
table.grid{border-collapse:collapse;display:inline-table;margin:2mm 4mm}table.grid td{width:9mm;height:9mm;border:1pt solid #0b2540;text-align:center;font-size:8pt;color:#888}'''


def html():
    pages = [
        '<h2>看懂表面碼：碼距 3</h2><p class="lead">在 transmon-3d.html#surface 看步驟 ①、③、⑥。把亮起的格子畫在方格旁邊。</p>'
        '<table class="rec"><tr><th>步驟</th><th>放了哪些錯誤</th><th>亮了幾塊、哪一色</th><th>解碼器修了哪顆</th><th>結果</th></tr>'
        + ''.join(f'<tr><td>{s}</td><td></td><td></td><td></td><td></td></tr>' for s in ('③ 單一 X', '④ Z', '④ Y', '⑤ 邊界', '⑥ 兩個 X'))
        + '</table>'
        '<div class="card"><h3>解碼練習單（今天的作品）</h3><p>每一格是一顆資料位元。把亮點畫在格線上，用線配對，圈出你猜的錯誤。</p>'
        + GRID * 3 + '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>抓蟲遊戲：爸爸藏蟲、你來抓</h2><p class="lead">你背對螢幕，只看爸爸畫的亮點。自己配對、圈出錯誤，再看解碼器怎麼配。</p>'
        '<table class="rec"><tr><th>回合</th><th>亮點（畫或寫）</th><th>我猜的錯誤</th><th>解碼器修了</th><th>真正的錯誤</th><th>誰對</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 9)) + '</table>'
        '<p class="note">我和解碼器不一樣的那幾回合，是哪一條配對不同？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：找出會騙人的組合</h2><p class="lead">在自由實驗只放 X 錯誤，按「解碼並修正」。出現「邏輯錯誤」就記下來。</p>'
        '<table class="rec"><tr><th>碼距</th><th>我放的錯誤</th><th>解碼器修了</th><th>邏輯錯誤嗎</th></tr>'
        + ''.join(f'<tr><td>{d}</td><td></td><td></td><td></td></tr>' for d in (3, 3, 3, 3, 5, 5, 5)) + '</table>'
        '<p>碼距 3：最少＿＿個錯誤就可能騙過它。碼距 5：最少＿＿個。</p>'
        '<p class="note">生活技能：從線索推回原因——醫生看症狀推病因、修車師傅聽聲音找故障。你想到哪個例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 資料位元和量測位元各做什麼？</p><div class="line"></div>'
        '<p>2. 為什麼表面碼只量奇偶？</p><div class="line"></div><p>3. 解碼器怎麼從亮點推回錯誤？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：只量奇偶，不碰資料、不破壞疊加</li><li>說出症狀是什麼：奇偶改變、格子亮起</li>'
        '<li>說出解碼：亮點兩兩配、總路徑最短，落單的配到邊界</li><li>指出一個限制：一顆可靠的邏輯位元要數百到上千顆實體位元</li>'
        '<li>替解碼練習單取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q084 表面碼列印包', '父子科技學院 量子電腦學程 Q084｜表面碼', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q084-surface-code', folder='Q084_表面碼', files=FILES,
        sheet=('03_抓蟲與改造紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_表面碼.pdf', pack_pages=4,
        pack_needles=('看懂表面碼', '解碼練習單', '抓蟲遊戲', '會騙人的組合', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q084', episode_dir='specials/q084-surface-code',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/transmon-3d.html#surface', 'animations/operation.html#qec'],
               'physicalQubits': {str(d): n for d, _, _, n, _, _ in DIST}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q084/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

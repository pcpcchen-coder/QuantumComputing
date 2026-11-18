"""Q016 課堂教材：發表模板（十張詞卡）、示範詞卡與建議十詞、兩分鐘導覽稿、首映會回饋單與說明卡、示範答案、動畫導覽。

不需要帳號，也不需要安裝套件；動畫用瀏覽器開啟 animations/operation.html（與 index.html）的場景。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q016/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 建議十詞：(名詞, 第幾堂, 一句話, 比喻, 哪裡不像, 場景畫面)。比喻都是教學比喻，出處見 fact-check.md。
WORDS = [
    ('量子位元', 'Q002', '量子電腦存資訊的最小單位，可以畫成一支指向球面的箭頭', '地球儀上插的一支箭頭',
     '真的量子位元裡沒有看得到的箭頭；量的時候只會得到 0 或 1', 'operation.html#qubit：左邊的球和箭頭，按 |0⟩、|1⟩'),
    ('疊加', 'Q002', '箭頭不在北極也不在南極，指向球面上另一個方向', '指向東北方的風向標',
     '風向標看一眼就知道方向；量子位元一量只得到 0 或 1', '#qubit：按 |+⟩，箭頭躺在赤道上'),
    ('測量', 'Q003', '問量子位元是 0 還是 1，只得到一個答案，問完狀態就變了', '擲一枚偏心的硬幣',
     '硬幣擲完還是原來那枚；量子位元量完會塌縮成 0 或 1', '#qubit：按「測量一次」，箭頭跳到北極或南極'),
    ('量子閘', 'Q004', '把箭頭繞著某一根軸轉一個角度', '翻煎餅（翻轉閘）',
     '煎餅只能整面翻；哈達瑪閘可以把箭頭停在赤道上', '#gates：按 X、H，看粉紅色的旋轉軸'),
    ('相位', 'Q005', '箭頭繞著赤道轉的角度；直接量看不見，卻會改變後面的結果', '操場跑道上站的位置',
     '跑道上的位置用眼睛就看得到；相位要先用哈達瑪閘轉一下再量', '#qubit：拖「φ（相位）」滑桿，青線不動'),
    ('干涉', 'Q006', '振幅先相加，方向相同變強，方向相反抵消', '兩道水波相遇',
     '電子一顆一顆送也有條紋；偷看走哪條路，干涉就消失', '#interference：相位調到 180 度'),
    ('糾纏', 'Q008', '兩顆量子位元的結果互相關聯，單看一顆是隨機的', '一對神祕骰子',
     '不能用來比光還快地傳訊息', '#register：按「Bell 態」，只剩 00 和 11'),
    ('量子線路', 'Q009', '量子程式的圖：線是量子位元、方塊是閘、儀表是測量，由左往右', '樂譜',
     '閘不會發出聲音，它們是在轉動量子位元的狀態', '#circuit：一步一步執行的線路'),
    ('格羅弗搜尋', 'Q013', '每做一輪，把寶藏的振幅拉高一點；16 個抽屜大約 3 輪', '在 16 個抽屜裡找寶藏',
     '不是一個一個打開抽屜；做太多輪反而會轉過頭', '#grover：按「完整一輪」，寶藏那根柱子變高'),
    ('退相干', 'Q014', '量子位元和環境接觸，資訊漏掉，疊加慢慢變得像猜硬幣', '被環境偷看了一眼',
     '環境沒有眼睛；真正的原因是熱、電磁雜訊和材料缺陷', 'index.html#bloch：按「T1 能量弛豫」或「Ramsey 進動」'),
]
assert len(WORDS) == 10 and len({w[0] for w in WORDS}) == 10

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q016：成果發表——我的量子小百科（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂是第一階段「量子直覺」的最後一堂：孩子挑十個學過的量子名詞，每個詞寫一張卡（一句話、一個比喻、哪裡不像、一個場景畫面），辦一場「首映會」發表給家人聽，下半場再錄一段兩分鐘的動畫導覽。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 看示範詞卡（疊加、干涉、糾纏），練習說「哪裡不像」 | 影片第 3–8 段、列印包第 2 頁 |
| 25–65 | 父子一起寫十張詞卡，然後辦首映會：孩子發表，家人當觀眾，每個詞給一個讚＋一個問題 | 列印包第 1、4 頁、`03_小百科詞卡.csv`、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子挑最喜歡的動畫場景，寫三段導覽稿，錄兩分鐘；自己聽一次，改好再錄第二版 | 列印包第 3 頁、`05_動畫導覽.md` |
| 105–115 | 孩子教爸爸：三個名詞、一個比喻和哪裡不像、在動畫裡指出畫面 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替小百科取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html`，把 `#qubit`、`#gates`、`#interference`、`#register`、`#circuit`、`#grover` 各點一次；`index.html#bloch` 是第十四堂退相干的場景。
- 列印 `02_列印包_量子小百科.pdf`（A4，共 4 頁）。第 1 頁發表模板是十張詞卡的表格；也可以把每個詞抄到一張小卡上。
- 找家人當觀眾（課綱的「家人觀眾」）：首映會大約 10–15 分鐘，觀眾只要做一件事——每個詞給一個讚和一個問題。
- 準備一支能錄音或錄影的手機，給下半場的兩分鐘導覽。讀一遍 `04_示範答案.md`。

## 驗收重點

1. 十張卡都填滿四格：一句話、比喻、哪裡不像、場景畫面。
2. 不看稿說出核心原理：至少三個名詞，各用一句話說清楚。
3. 能指出比喻的限制：每個比喻都要說出一個「哪裡不像」。最常見的壞例子是「疊加＝同時是 0 又是 1」，它會讓人以為量子電腦能同時試所有答案（第一、二堂學過）。

## 誠實說明

- 風向標、水波、神祕骰子、樂譜……都是教學比喻，不是正式定義；`04_示範答案.md` 是影片的例子，孩子自己的說法更重要，不必照抄。
- 動畫算的是理想的量子狀態，沒有雜訊；真的量子電腦還有誤差（第十四堂）。
- 首映會的回饋是練習「接受回饋」：觀眾的問題不是扣分，是下一版要改的地方。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：寫十張詞卡＋首映會（約 40 分鐘）

1. 從列印包第 2 頁的建議十詞開始，也可以換成自己更喜歡的詞（例如隱形傳態、2ⁿ）。
2. 每個詞填四格（列印包第 1 頁或 `03_小百科詞卡.csv`）：
   - 一句話：用自己的話，最好二十個字以內，不抄課本。
   - 比喻：用生活裡看得到、摸得到的東西。
   - 哪裡不像：這個比喻在哪一點會把人帶錯？一定要寫。
   - 場景畫面：哪個動畫場景、按哪個按鈕，讓別人照著做就看得到。
3. 每寫完一張，打開動畫確認畫面真的會出現。
4. 首映會：孩子站到前面，一個詞大約 30 秒，不看稿說出一句話、比喻、哪裡不像，再在動畫裡指出畫面。
5. 觀眾（家人）每個詞給「一個讚＋一個問題」，寫在列印包第 4 頁的回饋單；孩子記下問題，修改卡片。

## 下半場：兩分鐘導覽（約 30 分鐘）

1. 挑一個最喜歡的動畫場景（列印包第 3 頁）。
2. 寫三段：畫面上看到什麼 → 按哪個按鈕、怎麼變 → 這個變化代表哪個量子名詞。
3. 用手機錄兩分鐘：一邊操作動畫，一邊說。
4. 自己從頭聽一次，找出一個說不清楚的地方，改好再錄第二版，兩個版本都存起來。
''',

'04_示範答案.md': '# 示範答案（爸爸用）\n\n影片的建議十詞。比喻都是教學比喻；孩子自己的說法更重要，只要四格都說得通就算完成。\n\n'
  '| 名詞 | 第幾堂 | 一句話 | 比喻 | 哪裡不像 | 場景畫面 |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {w[0]} | {w[1]} | {w[2]} | {w[3]} | {w[4]} | {w[5]} |\n' for w in WORDS) +
  '\n## 暫停題：把量子位元比喻成一枚硬幣，哪裡像、哪裡不像？\n\n'
  '像：量的時候只有兩種結果（0 或 1），量很多次可以算比例。\n'
  '不像：硬幣只有正反兩面；量子位元的箭頭可以指向球面上任何方向，還有看不見的相位。'
  '量子位元的箭頭方向決定得到 0 和 1 的機率，量完會塌縮成 0 或 1；硬幣看完還是原來那枚硬幣。\n\n'
  '## 壞比喻：「疊加＝同時是 0 又是 1」\n\n'
  '這樣說會讓人以為量子電腦能同時試所有答案（第一堂破除的迷思）。'
  '而且赤道上「前面」和「後面」兩支箭頭，測量時都是 0、1 各一半，用這個說法分不出來；'
  '再按一次哈達瑪閘，一支回到北極、一支到南極（第五堂；`operation.html#gates`）。'
  '比較好的說法：疊加是箭頭指向的一個新方向（第二堂）。\n\n'
  '## 常見問題\n\n'
  '- 比喻找不到「哪裡不像」怎麼辦？問自己：這個東西用眼睛看得到嗎？量完會不會變？能不能用來傳訊息？通常其中一題就會露出差別。\n'
  '- 一句話太長怎麼辦？先刪掉例子和形容詞，只留「它是什麼」；例子放到比喻那一格。\n'
  '- 首映會冷場怎麼辦？觀眾的問題可以從「為什麼」「如果……會怎樣」開始，例如「如果偷看會怎樣？」。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。網址後面的 `#` 名稱可以直接跳到場景。

## 給詞卡「場景畫面」用的場景

- `operation.html#qubit`（量子位元、疊加、測量、相位）：按 |0⟩、|1⟩、|+⟩ 移動箭頭；「測量一次」「一次跑 1000 shots」；拖「φ（相位）」滑桿時，青色理論線不動。
- `operation.html#gates`（量子閘、相位）：按 X、Y、Z、H，箭頭繞粉紅色的旋轉軸轉；「重設 |0⟩」回到北極；讀數顯示 P(0)、P(1)。
- `operation.html#interference`（干涉）：「A：相位 φ」滑桿，0 度一定得到 0、180 度一定得到 1；「A：中途偵測路徑」打開後變成一半一半。
- `operation.html#register`（糾纏）：「Bell 態」之後只剩 |00⟩、|11⟩ 兩根柱子；「測量全部」結果是 00 或 11。
- `operation.html#circuit`（量子線路）：由左到右一步一步執行的線路。
- `operation.html#grover`（格羅弗搜尋）：16 根柱子＝16 個抽屜；「完整一輪」「自動跑到最佳次數」「測量」。
- `index.html#bloch`（退相干）：「T1 能量弛豫」「Ramsey 進動」。

## 兩分鐘導覽怎麼錄

1. 開場一句：「這是＿＿場景，它在講＿＿。」
2. 中間示範：按一個按鈕，說「你看，＿＿變成了＿＿」。
3. 結尾一句：「這代表＿＿；不過要注意，＿＿。」

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；← → 切換場景。
''',
}

SHEET_HEADER = ['編號', '名詞', '第幾堂學的', '一句話', '比喻', '哪裡不像', '場景畫面（場景＋按鈕）', '首映會的讚', '首映會的問題', '改好了嗎']
SHEET_ROWS = [[str(i), w[0], w[1]] for i, w in enumerate(WORDS, 1)]

EXTRA_CSS = '''table.rec td{height:17mm}table.rec td:first-child{width:25mm;font-size:11pt;white-space:nowrap}table.rec th:nth-child(n+2){width:22%}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.demo td{font-size:10.5pt;height:auto}table.demo th:first-child{width:16mm}
table.fb td{height:8.5mm;font-size:10.5pt}table.fb th:first-child{width:25mm}table.fb th:nth-child(n+2){width:30%}'''


def html():
    rows = ''.join(f'<tr><td>{w[0]}</td><td></td><td></td><td></td><td></td></tr>' for w in WORDS)
    demo = ''.join(f'<tr><td>{w[0]}</td><td>{w[2]}</td><td>{w[3]}</td><td>{w[4]}</td><td>{w[5]}</td></tr>'
                   for w in WORDS if w[0] in ('疊加', '干涉', '糾纏'))
    words = '、'.join(f'{w[0]}（{w[1]}）' for w in WORDS)
    fb = ''.join('<tr><td></td><td></td><td></td><td></td></tr>' for _ in range(10))
    pages = [
        '<h2>發表模板：十張詞卡</h2><p class="lead">每個名詞填四格：一句話（二十字內）、比喻、哪裡不像、場景畫面。可以換成自己喜歡的詞。</p>'
        '<table class="rec"><tr><th>名詞</th><th>一句話</th><th>比喻</th><th>哪裡不像</th><th>場景畫面</th></tr>'
        + rows + '</table>',
        '<h2>示範詞卡與建議十詞</h2><p class="lead">影片的三張示範卡。先用自己的話寫，再對照。</p>'
        '<table class="demo"><tr><th>名詞</th><th>一句話</th><th>比喻</th><th>哪裡不像</th><th>場景畫面</th></tr>' + demo + '</table>'
        f'<div class="box" style="margin-top:4mm"><h3>建議十詞（括號是第幾堂學的）</h3><p>{words}</p>'
        '<p>也可以換成：隱形傳態（Q011）、2ⁿ 個振幅（Q007）……</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>暫停題</h3><p>把量子位元比喻成一枚硬幣，哪裡像？哪裡不像？</p>'
        '<p>像：</p><div class="line"></div><p>不像：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>壞比喻改一改</h3><p>「疊加＝同時是 0 又是 1」會讓人以為什麼？我會改成：</p>'
        '<div class="line"></div></div>',
        '<h2>換你改造：兩分鐘導覽</h2><p class="lead">挑一個最喜歡的動畫場景，介紹給沒看過的人。</p>'
        '<div class="box"><p>我挑的場景：＿＿＿＿＿＿＿＿＿＿　網址 #：＿＿＿＿＿＿＿＿</p>'
        '<p>1. 畫面上看到什麼？</p><div class="line"></div><div class="line"></div>'
        '<p>2. 按哪個按鈕？畫面怎麼變？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 這個變化代表哪個量子名詞？要注意什麼？</p><div class="line"></div><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>錄音紀錄</h3>'
        '<p>第一版：＿＿分＿＿秒　　自己聽完，說不清楚的地方：</p><div class="line"></div>'
        '<p>我怎麼改：</p><div class="line"></div>'
        '<p>第二版：＿＿分＿＿秒　　檔名：＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>首映會回饋單與說明卡</h2><p class="lead">觀眾每個詞給一個讚、一個問題；發表的人記下來，改好卡片。</p>'
        '<table class="fb"><tr><th>名詞</th><th>讚（說得好的地方）</th><th>問題</th><th>我怎麼改</th></tr>' + fb + '</table>'
        '<div class="box" style="margin-top:4mm"><h3>說明卡：我的量子小百科</h3><p>小百科名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 在解決什麼？　2. 我怎麼做？　3. 哪裡容易錯？　4. 真實的量子電腦哪裡會用到？（錄音回答）</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三個名詞，各用一句話</li><li>說一個比喻，接著說它哪裡不像</li>'
        '<li>在動畫裡指出一個畫面給爸爸看</li><li>替小百科取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q016 量子小百科 列印包', '父子科技學院 量子電腦學程 Q016｜成果發表：我的量子小百科', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q016-quantum-glossary', folder='Q016_量子小百科', files=FILES,
        sheet=('03_小百科詞卡.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子小百科.pdf', pack_pages=4,
        pack_needles=('發表模板', '示範詞卡', '兩分鐘導覽', '首映會', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q016', episode_dir='specials/q016-quantum-glossary',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（動畫用瀏覽器）',
               'words': [w[0] for w in WORDS], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q016/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

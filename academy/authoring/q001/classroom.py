"""Q001 課堂教材：宣稱卡、分類板、量子問題清單、學程地圖與解答（不需帳號、不需安裝）。

    XINEW_ACADEMY=/path/to/XiNewVideoGPT/academy XINEW_CHROME=/path/to/chrome \
      $XINEW_ACADEMY/portable-runtime.sh python academy/authoring/q001/classroom.py

改完教材後：重跑 XiNewVideoGPT 的 pipeline/delivery.py，再跑 verify。
"""
from pathlib import Path
import json
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent
QREPO = HERE.parents[2]
CATALOG = json.loads((QREPO / 'academy/curriculum/catalog.json').read_text(encoding='utf-8'))

FAST, SAME, WRONG = '有機會變快', '不會變快', '說錯了'
# (宣稱, 正確的堆, 理由, 守門人可以追問)
CARDS = [
 ('量子電腦會同時試所有答案，所以什麼都快 2ⁿ 倍。', WRONG,
  '測量只會得到一個隨機結果；只是同時試，等於亂猜。加速要靠干涉讓錯的答案抵消。', '測量之後，你拿到幾個答案？'),
 ('夠大的量子電腦，可以很快把非常大的數字分解成質數。', FAST,
  '秀爾演算法：步數是輸入長度的多項式；古典上一般認為很難。但需要大型、能更正錯誤的量子電腦。', '現在的量子電腦做得到嗎？'),
 ('用量子電腦開網頁、看影片會更順。', SAME,
  '這些工作沒有讓干涉發揮的結構，瓶頸在網路和顯示，不在計算。', '開網頁慢，慢在哪裡？'),
 ('量子電腦很快就會取代手機和筆電。', WRONG,
  '量子電腦是專門工具，還要極低溫和很多周邊設備；平常的工作仍由普通電腦做。', '量子電腦要放在多冷的地方？'),
 ('在一百萬筆沒有排序的資料裡找一筆，量子方法大約不到一千次。', FAST,
  '格羅弗搜尋約 √N 次；一筆一筆翻平均約 N/2 次。這是平方根加速，不是指數加速。', '這是幾倍的加速？會不會更快？'),
 ('用量子電腦打報告、寫作業會比較快。', SAME,
  '打字和排版不是難算的問題，普通電腦早就夠快。', '寫作業最花時間的是哪一步？'),
 ('量子位元同時是 0 和 1，所以一次就能讀出所有答案。', WRONG,
  '疊加是很多可能各帶一個振幅；一次測量只得到一個結果。', '量子位元被測量後會怎樣？'),
 ('模擬新藥分子或新材料，是量子電腦有機會發揮的地方。', FAST,
  '費曼 1981 年就提出用量子系統模擬量子世界；大型強關聯的分子和材料是候選題目。', '為什麼普通電腦算分子會很吃力？'),
 ('玩電腦遊戲時，量子電腦能讓畫面更順。', SAME,
  '畫面靠顯示卡大量平行處理像素，沒有讓干涉加速的結構。', '遊戲畫面是誰在算？'),
 ('只要量子位元夠多，任何問題都能一秒解決。', WRONG,
  '大多數問題只會小幅變快，有些完全不會；位元多也要演算法對題。', '有沒有一個例子是位元再多也不會快？'),
 ('把一大堆資料讀進量子電腦做統計，一定會變快。', SAME,
  '資料要先載入量子電腦，這一步本身就慢，常常把加速吃掉。', '資料要怎麼放進量子電腦？'),
 ('有些量子系統（例如磁性材料）的行為，用量子電腦模擬會比普通電腦有效率。', FAST,
  '用量子系統模擬量子系統，是量子電腦最早被提出的用途之一。', '為什麼量子系統比較適合模擬量子系統？'),
]
assert len(CARDS) == 12 and {c[1] for c in CARDS} == {FAST, SAME, WRONG}
assert all(sum(c[1] == k for c in CARDS) == 4 for k in (FAST, SAME, WRONG))

MODULES = CATALOG['modules']
FIRST = {m['id']: [l['sourceRow']['課程主題'] for l in CATALOG['lessons'] if l['sourceRow']['模組'].startswith(m['id'])][:3] for m in MODULES}

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q001：開學任務（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五到六分鐘，帶出今天的問題：量子電腦真的「什麼都更快」嗎？

## 這份教材在做什麼

用 12 張宣稱卡玩分類，讓孩子自己找出「同時試所有答案」這種說法哪裡不對，並說出量子電腦擅長與不擅長的事。
不需要任何帳號，也不需要安裝；第 75–105 分鐘想看三維動畫的話，要有這個學程的 repo（見 `05_三維動畫導覽.md`）。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片、說說聽過的量子電腦說法 | 影片 |
| 10–25 | 量子工具箱：疊加、干涉、糾纏、測量 | 影片第 4–7 段 |
| 25–65 | 宣稱卡分類＋冒險任務（孩子是探險家，爸爸是守門人） | 列印包第 1、2 頁、`01_宣稱卡解答.md`、`03_宣稱分類紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 寫量子問題清單、查一句新聞說法、看三維動畫 | 列印包第 3 頁、`05_三維動畫導覽.md` |
| 105–115 | 孩子教爸爸：量子電腦快在哪 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名存檔 | |

## 課前準備（約 10 分鐘）

1. 列印 `02_列印包_開學任務.pdf`（A4，共 4 頁）。第 1 頁沿虛線剪成 12 張卡。
2. 讀一遍 `01_宣稱卡解答.md`，守門人的追問題都在裡面。
3. 準備便利貼；如果要錄音總結，準備手機錄音（只留在家裡）。

## 守門人的原則

- 不急著說答案，先問「你的證據是什麼？」
- 孩子放錯也沒關係，說得出理由就值得稱讚；說不出來的卡，寫進問題清單，之後的課會回來。
- 有幾張卡本來就有灰色地帶（例如「分解大數」要等很大的量子電腦），重點是說出條件。

## 誠實說明

- 本課的說法依 Aaronson（Scientific American 2008、Nature Physics 2015）、Shor、Grover 與 Preskill 的文章，詳見影片的 `fact-check.md`。
- 「一百萬筆不到一千次」是用格羅弗搜尋約 (π/4)√N 次推算的；原論文寫的是 O(√N)。
- 宣稱卡上的句子是本課為了練習改寫的常見說法，不是引用某一則新聞。
''',

'01_宣稱卡解答.md': '# 宣稱卡解答與守門人追問\n\n三堆各 4 張。孩子的分法和這份不同時，先聽理由；條件說得清楚的話，可以算對。\n\n'
  + '| 卡號 | 宣稱 | 正確的堆 | 理由 | 守門人追問 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {i} | {c[0]} | {c[1]} | {c[2]} | {c[3]} |\n' for i, c in enumerate(CARDS, 1))
  + '\n## 三堆的共同點\n\n'
  f'- **{FAST}**：問題有特殊的數學或物理結構，演算法能用干涉讓錯的答案互相抵消；加速大小不一樣（分解大數快非常多，搜尋只有平方根）。\n'
  f'- **{SAME}**：日常工作沒有這種結構，或卡在資料輸入、網路、顯示，不在計算。\n'
  f'- **{WRONG}**：把疊加說成「一次讀出所有答案」，或說量子電腦會取代所有電腦。\n',

'04_學程地圖.md': '# 量子電腦學程地圖\n\n共 96 堂，6 個模組，每模組 16 堂。每堂 120 分鐘。\n\n'
  + ''.join(f'## {m["id"]} {m["name"]}（{m["lessons"]}）\n\n{m["stage"]}；{m["audience"]}。\n\n前三堂：'
            + '、'.join(FIRST[m['id']]) + '。\n\n' for m in MODULES)
  + '完整課表見 repo 的 `academy/CURRICULUM_INDEX.md`。\n',

'05_三維動畫導覽.md': '''# 三維動畫導覽（75–105 分鐘使用）

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## 今天要看的場景

打開 `animations/operation.html#workflow`（場景 12：完整流程）。

1. 按播放，看一個量子程式怎麼一路變成結果：程式 → 轉譯 → 脈衝 → 控制電子 → 重複很多次 → 統計結果。
2. 找一找：哪一步花最多時間？量子計算本身占了多少？
3. 回答：為什麼要重複跑很多次？（提示：每次測量只得到一個結果）

## 操作

- 滑鼠拖曳旋轉、滾輪縮放；`←` `→` 切換場景、空白鍵暫停、`H` 隱藏面板。
- 想先偷看下一堂：`animations/operation.html#qubit`（量子位元與測量）。
''',
}

SHEET_HEADER = ['卡號', '宣稱', '我放的堆', '我的理由', '正確的堆', '守門人追問', '過關（是／否）']
SHEET_ROWS = [[str(i), c[0], '', '', c[1], c[3]] for i, c in enumerate(CARDS, 1)]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:2mm}
.cc{height:56mm;padding:4mm 4.5mm;position:relative;display:flex;align-items:center}
.cc b{position:absolute;top:2.2mm;left:4mm;font-size:12pt;color:#35a9d6}.cc p{margin:3mm 0 0;font-size:12.5pt;line-height:1.55}
.zones{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:4mm}
.zone{height:200mm;border:2pt solid #0b2540;border-radius:4mm;padding:4mm 4mm}.zone h3{font-size:16pt;margin:0}
.zone p{font-size:10.5pt;color:#35506b;margin:1mm 0 0}.zone.fast{border-color:#35a9d6}.zone.wrong{border-color:#f0a020}
ol.q{margin:2mm 0 0;padding-left:8mm}ol.q li{height:12.5mm;border-bottom:.9pt solid #7f9bb3;font-size:11pt;color:#7f9bb3}
.map{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:3mm}.map div{padding:2.5mm 3.5mm;font-size:10.5pt}
.map b{display:block;font-size:12pt;margin-bottom:.5mm}.chk li{margin:3mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}
.chk{padding-left:2mm}'''


def html():
    pages = []
    pages.append('<h2>宣稱卡 12 張</h2><p class="lead">沿虛線剪下。每放一張卡，先說理由，守門人再追問：你的證據是什麼？</p>'
                 '<div class="cards">' + ''.join(f'<div class="cut cc"><b>{i}</b><p>{c[0]}</p></div>' for i, c in enumerate(CARDS, 1))
                 + '</div>')
    pages.append('<h2>分類板：三堆</h2><p class="lead">把卡片放進三個框。每框旁邊寫一句：這一堆的卡有什麼共同點？</p>'
                 f'<div class="zones"><div class="zone fast"><h3>{FAST}</h3><p>要有特殊結構</p></div>'
                 f'<div class="zone"><h3>{SAME}</h3><p>普通電腦就很好</p></div>'
                 f'<div class="zone wrong"><h3>{WRONG}</h3><p>哪裡說錯了？</p></div></div>'
                 '<p class="note" style="margin-top:3mm">提示：測量只會得到一個結果。</p>')
    pages.append('<h2>我的量子問題清單</h2><p class="lead">寫下十個你最想知道的量子問題，越奇怪越好。之後的課回答了哪一題，就打個勾。</p>'
                 '<ol class="q">' + '<li></li>' * 10 + '</ol>'
                 '<div class="box" style="margin-top:5mm"><h3>新聞查核：找一句講量子電腦的話</h3>'
                 '<p>出處（哪個網站或影片、日期）：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
                 '<p>那句話：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
                 f'<p>我判斷它屬於：□ {FAST}　□ {SAME}　□ {WRONG}</p>'
                 '<p>我的理由：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>')
    pages.append('<h2>學程地圖與最後一關</h2><p class="lead">96 堂、6 個模組。今天是第一堂。</p>'
                 '<div class="map">' + ''.join(f'<div class="box"><b>{m["id"]} {m["name"]}</b>{m["lessons"]}｜{m["stage"]}</div>' for m in MODULES)
                 + '</div><div class="box" style="margin-top:6mm"><h3>最後一關：教爸爸量子快在哪（不看稿）</h3><ul class="chk">'
                 '<li>說出「同時試所有答案」錯在哪</li><li>舉一件有機會變快的事</li><li>舉一件不會變快的事</li>'
                 '<li>說出一個限制（例如：格羅弗搜尋只快平方根）</li><li>替兩件作品取名字並存檔</li></ul></div>')
    return printpack.document('Q001 開學任務 列印包', '父子科技學院 量子電腦學程 Q001｜開學任務', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q001-not-faster', folder='Q001_開學任務', files=FILES,
        sheet=('03_宣稱分類紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_開學任務.pdf', pack_pages=4,
        pack_needles=('宣稱卡 12 張', '分類板', FAST, SAME, WRONG, '我的量子問題清單', '新聞查核', '學程地圖', '最後一關'),
        authoring_dir=XINEW / 'authoring/q001', episode_dir='specials/q001-not-faster',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False, 'claimCards': len(CARDS),
               'cardsPerPile': {k: sum(c[1] == k for c in CARDS) for k in (FAST, SAME, WRONG)},
               'factsFrom': 'production/fact-check.md (Aaronson 2008/2015, Shor, Grover, Preskill)'})
    # classroom_pack 要求列印原稿放在 XiNewVideoGPT/academy 底下；複製一份回本 repo 保存
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q001/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q018 課堂教材：超導觀察筆記（觀察／推論兩欄）、動畫溫度紀錄表、臨界溫度排行榜、說明卡、示範答案、動畫導覽。

不需要帳號，也不需要安裝套件；動畫用瀏覽器開啟 animations/index.html#cooper。懸浮實驗只看影片，不在家操作。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q018/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 臨界溫度（K）與出處；出處見 fact-check.md。
MATERIALS = [
    ('鋁 Al', 1.2, '簡報 JJ 與微波讀取 p7；動畫 index.html#cooper'),
    ('汞 Hg', 4.2, '維基百科 Superconductivity（1911 年昂內斯）'),
    ('鉭 Ta', 4.5, '簡報 JJ 與微波讀取 p7'),
    ('鈮 Nb', 9.2, '簡報 JJ 與微波讀取 p7'),
    ('氮化鈮鈦 NbTiN', 14, '簡報 JJ 與微波讀取 p7'),
    ('釔鋇銅氧 YBCO', 93, '維基百科 Superconductivity（約 93 K）'),
]
assert [m[1] for m in MATERIALS] == sorted(m[1] for m in MATERIALS)

# 動畫溫度紀錄：(溫度 K, 配對比例讀數, 連在一起的電子對, 下方的字, 右下小圖的點)。依 02_cooper.js 第 49、59–62 行計算。
TEMPS = [
    (0.3, '100 %', '10 對', '超導態（青色）', '電阻 0'),
    (0.9, '68 %', '7 對', '超導態（青色）', '電阻 0'),
    (1.1, '29 %', '3 對', '超導態（青色）', '電阻 0'),
    (1.3, '0 %', '0 對', '正常態（粉紅色）', '跳到上面那條線'),
    (2.5, '0 %', '0 對', '正常態（粉紅色）', '上面那條線'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q018：超導——電阻消失、磁鐵懸浮（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂認識超導的兩個特徵：零電阻與排斥磁場（邁斯納效應）。孩子看一段安全的懸浮影片，把現象寫進「超導觀察筆記」，而且要把「觀察」（真的看到的）和「推論」（想出來的原因）分兩欄寫；再用動畫的溫度滑桿對照正常態與超導態。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 臨界溫度、零電阻、邁斯納效應、磁鐵為什麼浮起來 | 影片第 3–7 段 |
| 25–65 | 看懸浮影片寫觀察筆記（孩子當紀錄員、爸爸當提問官）；再用動畫溫度滑桿填紀錄表 | 列印包第 1、2 頁、`01_操作步驟.md`、`05_動畫導覽.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子查三種超導材料的臨界溫度，寫出處，從低排到高 | 列印包第 3 頁、`03_臨界溫度排行榜.csv` |
| 105–115 | 孩子教爸爸：兩個特徵、臨界溫度、一個注意事項 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替觀察筆記取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 找一段安全的超導懸浮影片（課綱的家長課前準備），先自己看一遍：確認是正規教學或實驗室的示範，片長 1–3 分鐘即可。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `index.html#cooper`，試拉「溫度 T (K)」滑桿、按「超導態 0.3 K」「正常態 2.5 K」。
- 列印 `02_列印包_超導觀察筆記.pdf`（A4，共 4 頁）。讀一遍 `04_示範答案.md`。

## 安全（一定要先講）

- **液態氮會凍傷。本課只看影片，不在家操作。** 不要嘗試自己買液態氮或乾冰來做懸浮實驗。
- 強力磁鐵會夾手、會吸壞手機與信用卡；本課也不需要拿磁鐵實驗。

## 驗收重點

1. 完成超導觀察筆記：至少五條觀察，每條都有對應的推論（或寫「還不知道」）。
2. 不看稿說出核心原理：超導的兩個特徵（零電阻、排斥磁場），以及要冷到臨界溫度以下。
3. 能指出一個注意事項：液態氮會凍傷，只看影片；或「磁鐵浮起來」本身還不能證明邁斯納效應。

## 誠實說明

- 動畫裡電子成對、晶格扭曲是示意畫面，不是真的照片；詳細機制在下一堂（庫柏對與能隙）。動畫沒有磁鐵，懸浮要看影片。
- 臨界溫度在不同資料裡會差一點點（例如汞 4.15 或 4.2 K），寫清楚出處就好。
- 有些影片裡磁鐵倒過來也不掉下來，那是另一個現象（磁通釘扎），本集沒有講，也沒有查核；可以當作「還不知道」的推論欄。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：超導觀察筆記（約 40 分鐘）

1. 孩子當「紀錄員」，爸爸當「提問官」。先播一次影片，只看不寫。
2. 第二次播放，邊看邊寫（列印包第 1 頁）：每看到一個現象，寫進「觀察」欄。例如：磁鐵浮在黑色圓片上方、圓片旁邊冒白霧、過一陣子磁鐵掉下來。
3. 提問官每一條都追問：「這是你看到的，還是你猜的？」猜的移到「推論」欄。
4. 替每條觀察寫一個推論，想不出來就寫「還不知道」。
5. 打開 `animations/index.html#cooper`，照列印包第 2 頁的溫度順序拉滑桿（0.3 → 0.9 → 1.1 → 1.3 → 2.5 K），每一格記下讀數、連線、下方的字、右下小圖的點。
6. 回答：電阻在哪個溫度突然出現？（約 1.2 K，鋁的臨界溫度）

## 下半場：臨界溫度排行榜（約 30 分鐘）

1. 挑三種超導材料（可從示範答案的清單挑，也可以自己找）。
2. 查臨界溫度，寫下數字和出處（書名或網頁名稱）。
3. 從低排到高，畫在列印包第 3 頁的溫度尺上，再畫一條液態氮 77 K 的線。
4. 說說看：哪些材料只用液態氮就能變成超導？量子晶片在 10 mK 工作，你挑的材料都夠冷嗎？
''',

'04_示範答案.md': '# 示範答案（爸爸用）\n\n孩子自己的觀察更重要；只要觀察和推論分得清楚，就算完成。\n\n'
  '## 觀察和推論（影片的例子）\n\n'
  '| 觀察（看到的） | 推論（想出來的原因） |\n|---|---|\n'
  '| 磁鐵浮在黑色圓片上方 | 圓片變成超導體，表面電流像電磁鐵把磁鐵推開 |\n'
  '| 圓片旁邊冒出白霧 | 圓片非常冷，空氣裡的水氣遇冷凝結（一般常識） |\n'
  '| 過一陣子磁鐵掉下來 | 圓片回溫到臨界溫度以上，不再超導 |\n'
  '| 圓片泡在冒泡的液體裡 | 液體可能是液態氮，正在沸騰（要問影片說明才能確定） |\n\n'
  '暫停題「冒白霧是觀察還是推論？」：冒白霧是觀察；「很冷」「是液態氮」是推論。\n\n'
  '提醒：維基百科 Meissner effect 指出，磁鐵浮在已經超導的材料上方，嚴格說不能證明邁斯納效應；'
  '要看材料冷下來那一刻，磁場有沒有被推出去。\n\n'
  '## 動畫溫度紀錄表（index.html#cooper）\n\n'
  '| 溫度 | 配對比例讀數 | 連在一起的電子對 | 下方的字 | 右下小圖的點 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {t[0]} K | {t[1]} | {t[2]} | {t[3]} | {t[4]} |\n' for t in TEMPS) +
  '\n連線數依程式計算（配對比例 = 1 − (T/1.2)⁴，共 10 對，四捨五入）。\n\n'
  '## 臨界溫度（從低到高）\n\n| 材料 | 臨界溫度 | 出處 |\n|---|---|---|\n'
  + ''.join(f'| {m[0]} | 約 {m[1]} K | {m[2]} |\n' for m in MATERIALS) +
  '\n液態氮沸點 77 K：表上只有釔鋇銅氧高於它。量子晶片在約 10 mK 工作，比表上所有材料都冷。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## index.html#cooper（超導體：Cooper pair 與零電阻）

- 金色小球：鋁的正離子晶格；藍色、紫色小球：電子；青色連線：成對的電子（庫柏對）。
- 「溫度 T (K)」滑桿：0.05–3 K。按鈕「超導態 0.3 K」「正常態 2.5 K」一鍵切換。
- 左邊讀數：「T / Tc」和「配對比例」。溫度越接近 1.2 K，連在一起的電子對越少。
- 下方大字：青色「超導態……無散射」或粉紅色「正常態……有電阻」。
- 右下小圖：電阻對溫度，在 1.2 K（鋁的臨界溫度）突然從 0 跳上去；青色點是目前溫度。
- 限制：場景沒有磁鐵，看不到懸浮或邁斯納效應；電子成對是示意，詳細機制在下一堂。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；空白鍵暫停；← → 切換場景。
''',
}

SHEET_HEADER = ['編號', '材料', '臨界溫度（K）', '出處（書名或網頁）', '排名（低→高）', '比 77 K 高嗎']
SHEET_ROWS = [['1', '', '', '', '', ''], ['2', '', '', '', '', ''], ['3', '', '', '', '', '']]

EXTRA_CSS = '''table.rec td{height:13mm}table.rec th:first-child{width:12mm}table.rec th:nth-child(n+2){width:44%}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.tmp td{height:11mm;font-size:10.5pt}table.tmp th:first-child{width:18mm}
table.mat td{height:13mm}table.mat th:first-child{width:12mm}
.scale{display:flex;justify-content:space-between;border-top:2px solid #333;margin:8mm 2mm 2mm;padding-top:1mm;font-size:10pt}'''


def html():
    obs = ''.join(f'<tr><td>{i}</td><td></td><td></td></tr>' for i in range(1, 9))
    tmp = ''.join(f'<tr><td>{t[0]} K</td><td></td><td></td><td></td><td></td></tr>' for t in TEMPS)
    mat = ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td></tr>' for i in range(1, 4))
    pages = [
        '<h2>超導觀察筆記：看懸浮影片</h2><p class="lead">紀錄員（孩子）寫，提問官（爸爸）每一條都問：「這是看到的，還是猜的？」</p>'
        '<div class="box"><p><b>安全：液態氮會凍傷。本課只看影片，不在家操作。</b></p>'
        '<p>影片名稱：＿＿＿＿＿＿＿＿＿＿＿＿＿＿　出處：＿＿＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<table class="rec" style="margin-top:4mm"><tr><th>#</th><th>觀察（眼睛真的看到的）</th><th>推論（想出來的原因，不知道就寫「還不知道」）</th></tr>'
        + obs + '</table>',
        '<h2>動畫溫度紀錄表</h2><p class="lead">打開 index.html#cooper，照順序拉「溫度 T (K)」滑桿，每一格記下來。</p>'
        '<table class="tmp"><tr><th>溫度</th><th>配對比例讀數</th><th>連在一起的電子對</th><th>下方的字（顏色）</th><th>右下小圖的點</th></tr>'
        + tmp + '</table>'
        '<div class="box" style="margin-top:4mm"><h3>想一想</h3><p>電阻在哪個溫度突然出現？＿＿＿＿ K，這叫做＿＿＿＿＿＿。</p>'
        '<p>超導態和正常態，電子走路的樣子差在哪裡？</p><div class="line"></div><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>暫停題</h3><p>影片裡圓片旁邊冒出白霧：這是觀察還是推論？它可能代表什麼？</p>'
        '<div class="line"></div><div class="line"></div></div>',
        '<h2>換你改造：臨界溫度排行榜</h2><p class="lead">挑三種超導材料，查臨界溫度，寫出處，從低排到高。</p>'
        '<table class="mat"><tr><th>#</th><th>材料</th><th>臨界溫度（K）</th><th>出處（書名或網頁）</th></tr>' + mat + '</table>'
        '<div class="box" style="margin-top:4mm"><h3>畫在溫度尺上（再畫一條液態氮 77 K 的線）</h3>'
        '<div class="scale"><span>0 K</span><span>20</span><span>40</span><span>60</span><span>80</span><span>100 K</span></div>'
        '<p>排名（低 → 高）：＿＿＿＿＿＿　→　＿＿＿＿＿＿　→　＿＿＿＿＿＿</p>'
        '<p>只用液態氮就能變成超導的是：＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>量子晶片在約 10 mK 工作，我挑的材料都夠冷嗎？</p><div class="line"></div></div>',
        '<h2>說明卡與最後一關</h2><p class="lead">把今天的觀察筆記整理成一張說明卡，再教爸爸。</p>'
        '<div class="box"><h3>說明卡：我的超導觀察筆記</h3><p>筆記名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>超導的兩個特徵：</p><div class="line"></div><div class="line"></div>'
        '<p>1. 在解決什麼？　2. 我怎麼做？　3. 哪裡容易錯？　4. 真實的量子電腦哪裡會用到？（錄音回答）</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出兩個特徵：零電阻、排斥磁場</li><li>說出為什麼要冷到臨界溫度以下</li>'
        '<li>在動畫裡把溫度拉過 1.2 K，指出變化</li><li>指出一個注意事項：液態氮會凍傷，只看影片</li>'
        '<li>替觀察筆記取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q018 超導觀察筆記 列印包', '父子科技學院 量子電腦學程 Q018｜超導：電阻消失、磁鐵懸浮', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q018-superconductivity', folder='Q018_超導觀察筆記', files=FILES,
        sheet=('03_臨界溫度排行榜.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_超導觀察筆記.pdf', pack_pages=4,
        pack_needles=('超導觀察筆記', '動畫溫度紀錄表', '臨界溫度排行榜', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q018', episode_dir='specials/q018-superconductivity',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（動畫用瀏覽器）',
               'materials': [m[0] for m in MATERIALS], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q018/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q101 課堂教材：案件卡、證據紀錄表、30 秒迷思修正講稿、迷思修正卡與解答；附一支可執行的頻率碰撞小程式。

不需要帳號，也不需要安裝套件：動畫用瀏覽器打開 animations/transmon-3d.html#case；
freq_case.py 只用 Python 標準函式庫（python freq_case.py）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q101/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent
PROGRAM = (HERE / 'freq_case.py').read_text(encoding='utf-8')

# 製作代理實跑 python freq_case.py（Python 3.13，標準函式庫）的輸出，與動畫第 6 章的數值一致
RUN_OUTPUT = '''製程原貌（三顆都在 Φ = 0）：Q1 5.120 GHz  Q2 5.100 GHz  Q3 5.390 GHz
    Q1–Q2 同頻（差 20 MHz）；Q2 0→1 ≈ Q3 1→2；旁觀者：Q1 0→1 ≈ Q3 1→2
迷思：全部調成 5.100：Q1 5.100 GHz  Q2 5.100 GHz  Q3 5.100 GHz
    Q1–Q2 同頻（差 0 MHz）；Q2–Q3 同頻（差 0 MHz）；旁觀者：Q1 ≈ Q3
棋盤格（Q1 = Q3 = 4.90）：Q1 4.900 GHz  Q2 5.100 GHz  Q3 4.900 GHz
    旁觀者：Q1 ≈ Q3
頻率配置（4.90／5.10／5.30）：Q1 4.900 GHz  Q2 5.100 GHz  Q3 5.300 GHz
    無碰撞
Q2 想往上調到 5.20 GHz： None （None = 做不到，只能往下調）
調近再調開：Q2、Q3 固定在配置，Q1 從 4.90 慢慢往上
    Q1 = 4.90 GHz（Φ = 0.128 Φ₀）：無碰撞
    Q1 = 4.95 GHz（Φ = 0.113 Φ₀）：Q1 驅動 ≈ Q2 雙光子 0→2
    Q1 = 5.00 GHz（Φ = 0.095 Φ₀）：旁觀者：Q1 0→1 ≈ Q3 1→2
    Q1 = 5.05 GHz（Φ = 0.073 Φ₀）：無碰撞
    Q1 = 5.08 GHz（Φ = 0.055 Φ₀）：Q1–Q2 同頻（差 20 MHz）
    Q1 = 5.10 GHz（Φ = 0.039 Φ₀）：Q1–Q2 同頻（差 0 MHz）
'''

CLAIMS = [  # (學生原話的一部分, 判斷, 修正)
    ('用 XY 寫入想要的狀態', '對', '從 |0⟩ 出發；脈衝面積定角度、相位定旋轉軸'),
    ('XY 讓電路來回振盪，「變成」量子位元', '因果顛倒', '十字電容＋JJ 本來就是量子位元，XY 只改變它的狀態'),
    ('SQUID 用來修正製程差異', '只對一半', '還能閃開材料缺陷、做 CZ；而且只能往下調'),
    ('控制好 Z 就能得到特性一樣的位元', '方向相反', 'Z 只調得動頻率；而且頻率要刻意錯開'),
]
KNOBS = [  # (特性, 由什麼決定, Z 調得動嗎)
    ('頻率 f₀₁', 'E_J（SQUID）＋E_C', '可以（只能往下）'),
    ('非諧性（約 −E_C）', '十字電容幾何', '不行'),
    ('T₁、T₂（壽命）', '材料、介面缺陷、雜訊', '不行'),
    ('耦合強度 g', '電容幾何', '不行'),
    ('讀取腔頻率、χ', '共振腔設計', '不行'),
]
EVIDENCE = [  # (動畫位置, 操作, 要看什麼)
    ('步驟 1 製程誤差', '按「重播」，看頻率尺與右側面板', '幾處碰撞？哪兩顆幾乎同頻？'),
    ('步驟 2 SQUID 調頻', '看左邊 |cos| 小圖與 Q1 的線', '頻率往哪個方向走？最高點在哪？'),
    ('步驟 3 頻率配置', '看棋盤格（Q1 = Q3）為什麼失敗', '「旁觀者碰撞」是什麼？'),
    ('步驟 6 自由實驗', '「回到製程原貌」→「π → Q1」', '只打 Q1，Q2 有沒有被激發？'),
    ('步驟 6 自由實驗', '拖 Q1 Φ 滑桿，讓 Q1 靠近再離開 Q2', '紅色帶子何時出現、何時消失？'),
    ('步驟 6 自由實驗', '「回到配置」→「CZ（Q2–Q3）」', '耦合電容何時亮？相位累積到幾度？'),
]

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q101：迷思修正——Z 線不是把位元調成一樣（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天玩「偵探辦案」：抓出一句聽起來很合理的錯誤想法——
「只要控制好 Z 線，就能把很多顆位元調成特性一樣」——再用 3D 動畫找證據修正它。

## 需要準備

- 瀏覽器打開 `animations/transmon-3d.html#case`（第 6 章：案例）。需要連網載入 three.js；不需要帳號。
- 選用：`freq_case.py`（只用 Python 標準函式庫，`python freq_case.py`），用和動畫相同的公式算頻率與碰撞。
- 列印 `02_列印包_迷思修正.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片，讀案子 | 影片、列印包第 1 頁 |
| 10–25 | 三條線索：XY 寫入、Z 的用途與限制、Z 只調得動頻率 | 影片第 3–8 段、列印包第 1 頁下半 |
| 25–65 | 案例章：把頻率調近再調開，觀察碰撞與耦合何時打開；寫證據欄 | `01_操作步驟.md`、列印包第 2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子寫 30 秒迷思修正說明，計時念 | 列印包第 3 頁 |
| 105–115 | 角色互換：孩子教爸爸操作與原理 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | 列印包第 4 頁（迷思修正卡） |

## 爸爸扮嫌疑人的台詞（故意說錯，等孩子反駁）

1. 「XY 線一打，電路才變成量子位元。」
2. 「SQUID 想往上調、往下調都可以。」
3. 「Z 線調好，每顆的 T₁ 就會一樣。」
4. 「把三顆頻率調成一樣，最整齊、最好控制。」

## 誠實說明

- 動畫的頻率（5.12／5.10／5.39 GHz、配置 4.90／5.10／5.30 GHz）、碰撞判定窗與串擾比例都是示意值，不是某顆真實晶片的規格。
- 動畫步驟 1–5 會自動播放；看不清楚就按「暫停」或「重播」，取消「自動接續」可以停在同一步。
- 產業有兩條路線：可調頻率（彈性大、CZ 快）與固定頻率＋可調耦合器或微波閘（穩定、線少）。影片沒點名公司，詳見師生對話紀錄第 3 課。
''',

'01_操作步驟.md': '''# 操作步驟（案例章，約 40 分鐘）

打開 `animations/transmon-3d.html#case`。右側面板上方的 1–6 是步驟；取消「自動接續」可以停在同一步。

## 一、看案發現場（步驟 1、2）

1. 按「1」，再按「重播」。看上方頻率尺：Q1、Q2 的實線幾乎疊在一起，紅色帶子代表碰撞；右側面板列出「碰撞 3 處」。
2. 等字幕「這時對 Q1 送一個 π 脈衝」：Q2 也被激發（右側面板 Q2 的 P₁ 不再是 0）。記進列印包第 2 頁。
3. 按「2」：看 Q1 的 Z 線送電流、左邊 |cos| 小圖的點往下滑、頻率尺上 Q1 的線往左移，再回來。

## 二、調近再調開（步驟 6 自由實驗）

1. 按「6」，再按「回到製程原貌」：三顆都在 Φ = 0，紅色帶子出現。
2. 按「π → Q1」：Q1 亮起，Q2 也微微發亮（串擾）。
3. 按「回到配置」：Q1 4.90、Q2 5.10、Q3 5.30 GHz，相隔約 200 MHz，顯示「無碰撞」。
4. 拖「Q1 Φ」滑桿往左（磁通變小 → Q1 頻率往上、靠近 Q2）。記下紅色帶子第一次出現時 Q1 的頻率；再拖回去，記下它消失的位置。
5. 再按「π → Q1」：這次只有 Q1 亮。
6. 按「CZ（Q2–Q3）」：Q3 短暫被推上去，Q2–Q3 之間的耦合電容亮起青光；面板「|11⟩ 累積相位」到 180°（= −1）就完成。

## 三、選用：用程式驗算

`python freq_case.py` 會印出四種排法的碰撞（製程原貌、全部調成一樣、棋盤格、頻率配置），以及 Q1 從 4.90 慢慢往上的變化。
可以改 `show(...)` 那幾行的頻率，試著排一組自己的頻率。
''',

'freq_case.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 學生原話逐句判斷\n\n| 說法 | 判斷 | 修正 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in CLAIMS)
  + '\n## Z 調得動什麼\n\n| 特性 | 由什麼決定 | Z 調得動？ |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in KNOBS)
  + '\n## freq_case.py 實跑輸出（Python 3.13，標準函式庫）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '重點：全部調成一樣反而有 3 處碰撞；棋盤格（Q1 = Q3）還剩 1 處旁觀者碰撞；錯開成 4.90／5.10／5.30 才無碰撞。\n'
  'Q1 從 4.90 往上靠近 Q2 的途中，會先撞到幾種不同的碰撞（雙光子、旁觀者），最後在 5.08 附近和 Q2 同頻。\n\n'
  '## 動畫裡的證據（參考）\n\n'
  '- 步驟 1：製程原貌 Q1 5.12、Q2 5.10、Q3 5.39 GHz，碰撞 3 處；對 Q1 送 π 脈衝，Q2 的 P₁ 約 0.35（示意的洩漏比例）。\n'
  '- 步驟 2：E_J(Φ) = E_J,max|cos(πΦ/Φ₀)|，最高點在 Φ = 0（sweet spot），只能往下調；離開 sweet spot，頻率尺上的線會抖動（磁通雜訊）。\n'
  '- 步驟 6：「回到配置」後無碰撞，π → Q1 只激發 Q1；CZ 時 Q3 推到 5.383 GHz（= f_Q2 − α），耦合電容發亮，|11⟩ 相位累積到 180°。\n\n'
  '## 課後練習（出自師生對話紀錄第 3 課）\n\n'
  '1. 判斷對錯：「只要每顆位元的 Z 線校準好，所有位元的 T₁ 就會一樣。」——錯。Z 只能調頻率；T₁ 由材料與缺陷決定。\n'
  '2. 為什麼可調 transmon 的 E_J 設計值要刻意做大？——SQUID 只能把頻率往下調，E_J 做大才有往下調的空間。\n'
  '3. 列出 Z 線的三個代價。——磁通串擾（需補償）、配線與熱負載、離開 sweet spot 的磁通雜訊。\n',

'05_動畫導覽.md': '''# 動畫導覽：transmon-3d.html 第 6 章（案例）

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，用瀏覽器開啟 `transmon-3d.html#case`（需要連網載入 three.js，不需要帳號）。

- 上方看板：左邊是 SQUID 干涉小圖 E_J(Φ)/E_J,max = |cos(πΦ/Φ₀)|，三個點是三顆位元目前的磁通；右邊是頻率尺（4.55–5.45 GHz），實線 0→1、細線 1→2、◆ 雙光子 0→2。
- 紅色帶子＝碰撞；位元外圈的紅圈＝這顆捲入碰撞。
- 右側面板：步驟 1–6、「◀ 上一步」「暫停」「重播」「下一步 ▶」「自動接續」。
- 步驟 6 自由實驗：Q1／Q2／Q3 Φ 滑桿、「π → Q1」「π → Q2」「π → Q3」「CZ（Q2–Q3）」「回到配置」「回到製程原貌」「顯示 Q2 鄰居的禁區」。
- 滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換章節。
''',
}

SHEET_HEADER = ['證據編號', '動畫位置', '操作', '看到什麼', '證明哪一句是錯的', 'Q1 頻率（GHz）', '有沒有紅色帶子']
SHEET_ROWS = [[str(i), a, b] for i, (a, b, _) in enumerate(EVIDENCE, 1)]

EXTRA_CSS = '''table.rec td{height:11mm;font-size:11pt}table.rec th{font-size:11pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}
.chk li:before{content:"□ "}.chk{padding-left:2mm}.quote{font-size:15pt;border-left:4pt solid #0b2540;padding:2mm 4mm;margin:3mm 0;background:#f2f6fa}
.two{display:grid;grid-template-columns:1fr 1fr;gap:5mm}.two .box{min-height:52mm}.small{font-size:10.5pt}table.ev td{height:19mm}'''


def html():
    pages = [
        '<h2>案件卡：今天的案子</h2><p class="lead">偵探（你）要把對的留下，把錯的圈出來。</p>'
        '<div class="quote">「我用 XY 驅動線寫入我要的量子狀態，讓十字電容跟 JJ 來回振盪（變成量子位元），'
        'SQUID 是用來修正製程差異用的！只要控制好 Z，我就可以得到數個特性接近的量子位元？」</div>'
        '<table class="rec"><colgroup><col style="width:40%"><col style="width:18%"><col style="width:42%"></colgroup><tr><th>說法</th><th>對／錯／一半</th><th>為什麼</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, *_ in CLAIMS) + '</table>'
        '<h3 style="margin-top:4mm">三條線索（看影片時填）</h3>'
        '<p>線索一：電路是不是因為 XY 才變成量子位元？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>線索二：Z 線的頻率可以往＿＿＿調，最高點在 Φ ＝＿＿＿</p>'
        '<p>線索三：Z 只調得動＿＿＿＿；頻率一樣會發生＿＿＿＿和＿＿＿＿</p>',
        '<h2>證據紀錄：案例章調近再調開</h2><p class="lead">animations/transmon-3d.html#case。每找到一個證據，寫下看到什麼、證明哪一句是錯的。</p>'
        '<table class="rec ev"><colgroup><col style="width:6%"><col style="width:17%"><col style="width:25%"><col style="width:26%"><col style="width:26%"></colgroup><tr><th>#</th><th>動畫位置</th><th>操作</th><th>看到什麼</th><th>證明哪一句錯</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td class="small">{a}</td><td class="small">{b}</td><td></td><td></td></tr>'
                  for i, (a, b, _) in enumerate(EVIDENCE, 1)) + '</table>'
        '<p class="note">調近：拖 Q1 Φ 滑桿讓 Q1 靠近 Q2。紅色帶子第一次出現時，Q1 ＝＿＿＿＿ GHz；調開後消失時，Q1 ＝＿＿＿＿ GHz。</p>'
        '<p class="note">CZ（Q2–Q3）時，哪裡亮起青光？＿＿＿＿＿＿　相位累積到＿＿＿度。</p>',
        '<h2>換你改造：30 秒迷思修正說明</h2><p class="lead">三句結構：大家常以為什麼 → 其實是什麼 → 證據在哪裡。</p>'
        '<div class="box"><p>1. 大家常以為：</p><div class="line"></div><div class="line"></div>'
        '<p>2. 其實是：</p><div class="line"></div><div class="line"></div>'
        '<p>3. 證據在：</p><div class="line"></div><div class="line"></div></div>'
        '<p>計時念一次：第 1 次＿＿＿秒　第 2 次＿＿＿秒　第 3 次＿＿＿秒（目標 30 秒以內、不念太快）</p>'
        '<h3>Z 調得動什麼？（打勾）</h3><table class="rec"><tr><th>特性</th><th>由什麼決定</th><th>Z 調得動？</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>□ 可以　□ 不行</td></tr>' for a, b, _ in KNOBS) + '</table>',
        '<h2>迷思修正卡</h2><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<div class="two"><div class="box"><h3>錯的說法</h3><div class="line"></div><div class="line"></div><div class="line"></div></div>'
        '<div class="box"><h3>正確的說法</h3><div class="line"></div><div class="line"></div><div class="line"></div></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>證據（動畫哪一步、看到什麼）</h3><div class="line"></div><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：Z 線能調什麼、不能調什麼</li><li>解釋為什麼頻率要錯開，不是調成一樣</li>'
        '<li>說出耦合什麼時候打開：做閘時才短暫對上</li><li>指出一個注意事項：頻率太近會碰撞與串擾，配置時要刻意錯開</li>'
        '<li>替迷思修正卡取名字、錄音、存檔</li></ul></div>',
    ]
    return printpack.document('Q101 迷思修正 列印包', '父子科技學院 量子電腦學程 Q101｜迷思修正：Z 線不是把位元調成一樣', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q101-z-line-myth', folder='Q101_迷思修正', files=FILES,
        sheet=('03_證據紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_迷思修正.pdf', pack_pages=4,
        pack_needles=('案件卡', '三條線索', '證據紀錄', '調近', '30 秒迷思修正說明', '迷思修正卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q101', episode_dir='specials/q101-z-line-myth',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（瀏覽器開動畫；freq_case.py 只用 Python 標準函式庫）',
               'program': 'freq_case.py', 'testedWith': 'Python 3.13 standard library',
               'scene': 'animations/transmon-3d.html#case', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q101/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q065 課堂教材：五條件卡三張（超導、離子阱、中性原子）、平台對照卡、交換挑錯紀錄單、說明卡與最後一關、解答、動畫導覽。

不需要安裝程式；動畫用瀏覽器開啟 animations/ 資料夾即可。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q065/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

CONDS = [('①', '可擴充、定義清楚的兩個能階'), ('②', '能初始化到 |0⟩'), ('③', '相干時間 ≫ 閘時間'),
         ('④', '通用量子閘（單位元＋兩位元）'), ('⑤', '能讀取單一量子位元')]
PLATFORMS = ['超導（人造原子）', '離子阱（帶電原子）', '中性原子（不帶電原子）']
# 解答：簡報 Ion_NeutralAtom_Talk.pptx 第 3、4、39、40 頁；JJ_Microwave_Readout_Talk.pptx 第 3、10 頁；QC_Operation_Talk.pptx 第 13 頁（代表值）
ANSWERS = {
    '超導（人造原子）': ['鋁＋約瑟夫森接面電路；非諧性讓間距不相等，只用最低兩個能階（約 5 GHz）',
                    '10 mK 下熱平衡幾乎全在 |0⟩（被動重置），或量測後補 π 脈衝（主動重置）',
                    'T₂ 約 0.1–1 ms；閘 ~25 ns／~60 ns；T₂／閘 約 10³',
                    '微波脈衝；兩位元閘 CZ／交叉共振；只連最近鄰，遠距要 SWAP',
                    '色散微波讀取，約 0.5 μs（三平台最快）'],
    '離子阱（帶電原子）': ['¹⁷¹Yb⁺ 的兩個超精細能階，相差 12.6 GHz',
                     '雷射冷卻＋光泵浦（> 99.9 %）',
                     'T₂ 秒～小時；兩位元閘 10–200 μs；T₂／閘 約 10⁴',
                     '單位元：微波／Raman；兩位元：共享振動（MS 閘），同鏈全連接',
                     '狀態相依螢光 → PMT／相機（> 99.9 %），約 200 μs'],
    '中性原子（不帶電原子）': ['⁸⁷Rb 的兩個超精細能階，相差 6.8 GHz',
                       '雷射冷卻＋光泵浦；先成像，再重排出完整陣列',
                       'T₂ 約 1 s（回波），Caltech 2025 紀錄 12.6 s；兩位元閘約 0.3 μs',
                       '單位元：全域＋局部定址；兩位元：芮德堡阻斷（CZ）；搬運 → 任意配對',
                       '推走一個態＋螢光成像 → 相機（> 99 %），約 ms'],
}
RULER = [('抓住量子位元', '晶片上固定', 'RF 電場（Paul 阱）＋超高真空', '光鑷＋超高真空'),
         ('環境', '10 mK 稀釋冷凍機', '超高真空，室溫或 4–20 K', '超高真空，原子冷到 μK'),
         ('強項', '速度', '品質', '數量與並行'),
         ('規模（2025 代表值）', '~100–1000+', '~100（Helios 98）', '數百～6100 顆原子'),
         ('主要挑戰', '佈線、低溫、元件缺陷', '速度、雷射與電極規模化', '原子損失、讀取與循環速度')]
for k, v in ANSWERS.items():
    assert len(v) == len(CONDS), k

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q065：人造原子 vs 真的原子（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂是 QM05「各種量子電腦平台」的第一堂：用 DiVincenzo 五條件當「同一把尺」，
比較超導量子位元（人造原子）和離子阱、中性原子（真的原子）。父子各填一套五條件卡，再交換卡片互相挑錯，完成「平台對照卡」。

## 課前準備（約 15 分鐘，不需要帳號或安裝）

1. 拿出第十七堂的五條件檢核卡（沒有也沒關係，列印包第 1、2 頁就是空白卡）。
2. 列印 `02_列印包_交換作品.pdf`（A4，共 4 頁）兩份：你一份、孩子一份；準備兩支紅筆。
3. 讀一遍 `04_解答.md`。在自己那一份卡片裡「故意藏一個錯」，例如寫「超導不需要冷凍機」或「中性原子靠電場抓住」。
4. 在電腦上打開動畫（下載 `animations/` 整個資料夾）：`index.html#potential`、`atoms.html#atomsys`、`atoms.html#compare`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 對照簡報第 3、4 頁和三個動畫，認識三個平台 | `05_動畫導覽.md` |
| 25–65 | 父子各自替三個平台填五條件卡，每格寫一個證據 | 列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 交換卡片，用紅筆圈錯、寫理由、查證改正；完成平台對照卡 | 列印包第 2、3 頁、`03_平台對照表.csv` |
| 105–115 | 孩子教爸爸：差別、抓法與讀法、一個常見誤解 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 挑錯的原則

- 圈錯要寫理由；被圈的人要拿簡報、動畫或解答去查，對了就保留，錯了就改正，兩人都在紀錄單簽名。
- 數字是「代表值」：簡報寫明依原子種類、系統與年份差異很大。數量級對、來源寫清楚就算對，不必和解答一字不差。
- 爸爸藏的錯被找到，孩子得一分；孩子找到解答以外的合理問題，也得一分。

## 誠實說明

- 本課只比較三個平台；光子、矽自旋等其他平台不在本集範圍。
- 中性原子的 6100 顆是原子陣列的規模，不等於 6100 個能做運算的量子位元。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：填三張五條件卡（約 40 分鐘）

1. 先在每張卡的最上面寫：平台名字、量子位元是什麼做的、用什麼抓住它。
2. 五條件一條一格，每格寫「做法＋一個證據」（數字、簡報頁碼或動畫畫面），例如「③ T₂ 約 0.1–1 ms（簡報第 39 頁）」。
3. 最右欄打勾：這一條是這個平台的強項（★）、普通（○），還是弱點（△）。
4. 三張都填完，把強項和弱點抄到第 2 頁下方的「平台對照卡」。

## 下半場：交換作品，互相挑錯（約 30 分鐘）

1. 和爸爸交換整套卡片。
2. 用紅筆圈出你覺得錯或漏掉的格子，在第 3 頁的紀錄單寫下：哪一張、哪一條、為什麼。
3. 換回卡片，被圈的人去查證：打開簡報、動畫或 `04_解答.md`，寫下查證結果（保留／改正）。
4. 最後一起完成平台對照卡，替它取名字，寫上版本（例如 v1.0）。

## 沒有電腦的備案

只用 `04_解答.md` 的對照表；把解答蓋住，一人念一格，另一人判斷是哪個平台。
''',

'04_解答.md': '# 解答（爸爸用）\n\n數值為簡報標明的代表值（離子阱與中性原子量子電腦簡報第 3、4、39、40 頁；JJ 元件與微波讀取第 3、10 頁；如何操作量子電腦第 13 頁）。\n\n'
  + '| 條件 | ' + ' | '.join(PLATFORMS) + ' |\n|---|---|---|---|\n'
  + ''.join(f'| {n} {c} | ' + ' | '.join(ANSWERS[p][i] for p in PLATFORMS) + ' |\n' for i, (n, c) in enumerate(CONDS))
  + '\n## 平台對照卡（同一把尺）\n\n| 項目 | ' + ' | '.join(PLATFORMS) + ' |\n|---|---|---|---|\n'
  + ''.join(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} |\n' for r in RULER)
  + '\n## 常見的錯（挑錯時可以拿來用）\n\n'
  '- 「超導不需要冷凍機」：錯，要 10 mK 稀釋冷凍機。\n'
  '- 「真原子天生一模一樣，所以比較簡單」：錯，要用雷射與真空系統抓住、冷卻、操控它們。\n'
  '- 「中性原子靠電場抓住」：錯，中性原子不帶電，用聚焦雷射（光鑷）；用 RF 電場抓的是離子。\n'
  '- 「閘越快的平台一定越好」：不一定；要看相干時間除以閘時間，還要算讀取、搬運、冷卻（簡報第 40 頁）。\n'
  '- 「有兩個能階就是量子位元」：不夠，五條件都要過關（第十七堂）。\n'
  '- 「超導每一顆頻率都一樣」：錯，製程變異讓頻率散佈，要逐顆校準。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/index.html#potential`（場景 4：能階與非諧性）

- 預設是 JJ／Transmon：餘弦位能井，右側間距 4.74、4.45、4.13 GHz，越往上越窄（非諧性約 −287 MHz）。
- 按「LC 諧振子（線性）」：拋物線，三個間距都是 5.00 GHz，說明寫「等間距 → 無法單獨定址」。
- 切回 JJ，拖動「E_J / E_C」滑桿：頻率跟著變。接面做得不同，人造原子的頻率就不同。

## `animations/atoms.html#atomsys`（場景 7：中性原子系統全景）

- 「只看雷射」：同一顆原子要被 5–7 種雷射照射；「視角：真空腔特寫」：玻璃腔裡 6×6 的原子陣列；
  「只看設施」：沒有稀釋冷凍機，主要負載是雷射、冷卻水、恆溫空調（右下示意圖約 10 kW 等級）。

## `animations/atoms.html#compare`（場景 13：三平台比較）

- 「連接性」「閘速度」「相干時間」「規模」四個按鈕，長條上的標籤就是對照卡的證據；右下插圖是時間尺度（log 座標）。

## 延伸

- `atoms.html#ionsys`（場景 1：離子阱系統全景）會在第六十七堂細看；下一堂看 `atoms.html#paul`（Paul 阱）。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；左右方向鍵換場景。
''',
}

SHEET_HEADER = ['條件', '超導（人造原子）', '離子阱', '中性原子', '證據來源（頁碼／動畫）', '挑錯紀錄']
SHEET_ROWS = [[f'{n} {c}'] for n, c in CONDS] + [[r[0]] for r in RULER]

EXTRA_CSS = '''table.card td{height:15mm;font-size:11pt}table.card td.c{width:46mm;font-weight:700}table.card td.s{width:16mm;text-align:center;color:#4a6a88}
.cut h3{margin:0 0 1.5mm}.cut .meta{font-size:10.5pt;margin:0 0 2mm;color:#35506b}.cut{margin-bottom:5mm}
table.rul td{height:12mm;font-size:11pt}table.rec td{height:13mm}
.chk li{margin:2.2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def card(title):
    rows = ''.join(f'<tr><td class="c">{n} {c}</td><td></td><td class="s">★ ○ △</td></tr>' for n, c in CONDS)
    return (f'<div class="cut"><h3>五條件卡：{title}</h3><p class="meta">量子位元是什麼做的：＿＿＿＿＿＿＿＿　用什麼抓住：＿＿＿＿＿＿＿＿　填卡人：＿＿＿＿</p>'
            f'<table class="card"><tr><th>條件</th><th>做法＋一個證據（數字、頁碼或動畫）</th><th>評等</th></tr>{rows}</table></div>')


def html():
    ruler = ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td></tr>' for r in RULER)
    pages = [
        '<h2>五條件卡（一）</h2><p class="lead">同一把尺：DiVincenzo 五條件。每格寫做法＋一個證據；評等：★ 強項、○ 普通、△ 弱點。</p>'
        + card(PLATFORMS[0]) + card(PLATFORMS[1]),
        '<h2>五條件卡（二）＋平台對照卡</h2>' + card(PLATFORMS[2])
        + '<h3>平台對照卡</h3><p class="note">作品名稱：＿＿＿＿＿＿＿＿　版本：v＿＿＿　日期：＿＿＿＿</p>'
        '<table class="rul"><tr><th>項目</th><th>超導</th><th>離子阱</th><th>中性原子</th></tr>' + ruler + '</table>',
        '<h2>交換挑錯紀錄單</h2><p class="lead">交換卡片，用紅筆圈錯；在這裡寫理由。被圈的人查證後填「結果」。</p>'
        '<table class="rec"><tr><th>誰的卡</th><th>哪個平台</th><th>第幾條</th><th>我覺得錯在哪、為什麼</th><th>查證來源</th><th>結果（保留／改正）</th></tr>'
        + '<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>' * 9 + '</table>'
        '<div class="box" style="margin-top:4mm"><p>爸爸藏的錯：找到了嗎？□ 找到　□ 沒找到　　是哪一格：＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>比分：孩子＿＿分　爸爸＿＿分　　兩人簽名：＿＿＿＿＿＿　＿＿＿＿＿＿</p></div>',
        '<h2>說明卡與最後一關</h2><div class="box"><h3>三句話說清楚</h3>'
        '<p>1. 人造原子是＿＿＿＿＿＿＿＿做的，好處是＿＿＿＿＿＿，缺點是＿＿＿＿＿＿。</p>'
        '<p>2. 真的原子天生＿＿＿＿＿＿，但要用＿＿＿＿＿＿和＿＿＿＿＿＿抓住它們。</p>'
        '<p>3. 用同一把尺比：超導贏在＿＿＿＿，離子阱贏在＿＿＿＿，中性原子贏在＿＿＿＿。</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出人造原子和真的原子差在哪裡</li><li>說出三個平台各用什麼抓住量子位元、怎麼讀取</li>'
        '<li>指出一個常見誤解：真原子一模一樣，但要用雷射與真空系統抓住它們</li><li>替平台對照卡取名字、寫上版本號存檔</li></ul></div>'
        '<div class="box" style="margin-top:4mm"><h3>錄音提問</h3><p>1. 人造原子 vs 真的原子在解決什麼？　2. 我怎麼做？　3. 哪裡容易錯？　4. 生活中或真實的量子電腦哪裡會用到？</p>'
        '<div class="line"></div><div class="line"></div></div>',
    ]
    return printpack.document('Q065 交換作品 列印包', '父子科技學院 量子電腦學程 Q065｜人造原子 vs 真的原子', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q065-artificial-vs-real-atoms', folder='Q065_人造原子vs真的原子', files=FILES,
        sheet=('03_平台對照表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_交換作品.pdf', pack_pages=4,
        pack_needles=('五條件卡', '平台對照卡', '交換挑錯', '最後一關'),
        authoring_dir=XINEW / 'authoring/q065', episode_dir='specials/q065-artificial-vs-real-atoms',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（動畫用瀏覽器開啟）',
               'platforms': PLATFORMS, 'conditions': [c for _, c in CONDS], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q065/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

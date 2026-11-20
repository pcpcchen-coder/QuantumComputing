"""Q097 課堂教材：導覽：一顆 transmon 的十二章旅程 — 動畫操作步驟、十二章闖關紀錄、心智圖、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/transmon-3d.html（十二章），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q097/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# transmon-3d.html 的十二章（CH 定義的 id、short、title）與參考答案（「這章在回答什麼問題」，依簡報第 18 頁副標與動畫說明整理）
CH12 = [
    (1, 'chip', '晶片', '一顆 transmon 的俯視圖', '一顆超導量子位元在晶片上長什麼樣子？十字電容、SQUID、XY／Z 線、讀取共振腔各做什麼？'),
    (2, 'junction', '約瑟夫森結', '約瑟夫森結：非線性電感的本體', '為什麼約瑟夫森結能當一個無耗散、非線性的電感？'),
    (3, 'potential', '位能井', 'cos 位能井：能階不再等距', '為什麼能階不等距，才挑得出 |0⟩ 和 |1⟩？'),
    (4, 'control', '操控', '用微波轉動布洛赫球', '怎麼用微波把狀態寫進位元（π、π/2 脈衝、Rabi 振盪）？'),
    (5, 'readout', '讀取', '色散讀取：從頻移讀出狀態', '怎麼知道位元是 0 還是 1？讀完怎麼回到 |0⟩？'),
    (6, 'case', '案例', '案例：三顆可調 transmon 的頻率配置', '多顆位元放在一起，頻率要怎麼排才不會碰撞、串擾？'),
    (7, 'grover', '振幅長條', '振幅長條：糾纏、Grover 與 Deutsch', '兩顆位元的振幅怎麼變化？糾纏、Grover 搜尋、Deutsch 在做什麼？'),
    (8, 'shor', 'Shor', 'Shor 演算法：用 QFT 找週期，分解 15', '量子電腦為什麼能幫忙分解大數（找週期）？'),
    (9, 'bv', 'BV 密碼', '基本操作案例：3 顆位元一次猜中密碼（BV）', '只查詢黑盒子一次，怎麼猜中 3 位元密碼？'),
    (10, 'surface', '表面碼', '量子錯誤更正：表面碼', '量子錯誤怎麼抓、怎麼修，又不破壞疊加？'),
    (11, 'surgery', '邏輯閘', 'Lattice surgery 與魔術態蒸餾', '受保護的邏輯位元怎麼做運算？'),
    (12, 'stack', '軟體堆疊', '編譯與控制軟體堆疊', '一行程式怎麼變成送進晶片的微波脈衝？'),
]
assert len(CH12) == 12

# 師生對話紀錄的課程地圖：課 → 主題 → 對應動畫章節（學程 Q099–Q111）
MAP13 = [(1, 'SQUID 干涉', '1'), (2, '寫入與 SQUID', '1、4'), (3, '迷思修正', '6'), (4, '頻率配置', '6'),
         (5, '能階與 Rabi', '3、4'), (6, '讀取與重設', '5'), (7, '疊加與 BV', '9'), (8, '糾纏與 Grover', '7'),
         (9, 'Deutsch', '7（#deutsch）'), (10, 'Shor', '8'), (11, '表面碼', '10'), (12, '邏輯閘', '11'), (13, '軟體堆疊', '12')]
assert len(MAP13) == 13
PARTS = [('第一篇 硬體', '第 1–6 課'), ('第二篇 演算法', '第 7–10 課'), ('第三篇 容錯與系統', '第 11–13 課')]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q097：導覽：一顆 transmon 的十二章旅程（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂是「超導量子電腦深入」模組的第一課：先看全貌，把 transmon 3D 動畫的十二章走一遍，再畫成一張心智圖；之後 Q098–Q111 才逐課鑽細節。

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `transmon-3d.html`（需連網載入 three.js；資料夾裡也附了 `lib/three-r128.min.js`）。不需要帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 十二章一覽、師生對話紀錄的課程地圖 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 冒險任務：逐章闖關，每章寫一句「這章在回答什麼問題」 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 把十二章畫成心智圖，圈出最想深入的三章 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與每章在講什麼 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 先自己開 `transmon-3d.html#chip`，在第 1 章按「送出 π 脈衝」，看十字板發金光再慢慢變暗；再點畫面下方章節列的 01–12，各看一眼。
- 讀一遍 `docs/超導量子電腦師生對話教學紀錄.md` 開頭的「課程地圖」（3 篇 13 課）。
- 列印 `02_列印包_十二章旅程.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 冒險任務怎麼玩

爸爸是嚮導：點開一章，問「這章在回答什麼問題？」孩子是冒險者：自己按那一章的按鈕（第 5 章以後多半有「下一步 ▶」的分步導覽，左上方會跳字幕），看完用一句話回答，寫在列印包上。卡住就打問號，不必當場弄懂——之後的課會回來。

## 誠實說明

- 3D 模型未按比例：真正的晶片只有數百 μm，畫面的粗細與距離都是示意。
- 動畫與師生對話紀錄裡的數字（f₀₁ = 5.21 GHz、讀取共振腔約 7 GHz、E_J／E_C = 15 GHz／250 MHz 等）是本系列貫穿全課的範例參數，不是某一顆實際晶片。
- 這一堂只做導覽；每章的原理會在之後各課查核與展開。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 第 1 章：晶片（`transmon-3d.html#chip`，約 10 分鐘）

1. 「晶片總覽」分頁：找出十字電容板、SQUID（兩個約瑟夫森結）、XY 驅動線、Z 磁通線、讀取共振腔、饋線（可勾「顯示標籤」）。
2. 按「送出 π 脈衝」：青綠色小點沿 XY 線跑向十字板，十字板發金光（激發到 |1⟩），再慢慢變暗（T₁ 衰減回 |0⟩）。
3. 切到「大十字電容的作用」分頁：看四隻手臂各接什麼、電場線和 JJ 輪流發亮；拖「C_Σ」滑桿看十字板變粗變細，再按「回到 77.5 fF」。

## B. 冒險任務：逐章闖關（約 30 分鐘）

用畫面下方的章節列（01 晶片 … 12 軟體堆疊）依序點開。每章：
1. 讀左側面板的標題與第一段說明。
2. 按一兩個按鈕（有分步導覽的章節按「下一步 ▶」，或直接點步驟編號）。
3. 在列印包第 1–2 頁寫一句：「這章在回答＿＿＿＿？」不懂的打問號。

## C. 下半場：十二章心智圖（約 30 分鐘）

1. 列印包第 3 頁中間寫「一顆 transmon」，外圈分三區：硬體（第 1–6 章）、演算法（第 7–9 章）、容錯與系統（第 10–12 章）。
2. 用箭頭連出「要先懂哪一章才看得懂哪一章」，可以參考師生對話紀錄的課程地圖。
3. 圈出最想深入的三章，各寫一句理由。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 每章在回答什麼問題（參考答案，孩子用自己的話說即可）\n\n'
  '| 章 | 名稱 | 動畫網址 | 這章在回答什麼問題 |\n|---|---|---|---|\n'
  + ''.join(f'| {n} | {s} | `transmon-3d.html#{h}` | {q} |\n' for n, h, s, _, q in CH12)
  + '\n## 師生對話紀錄的課程地圖（3 篇 13 課）\n\n'
  + ''.join(f'- {p}：{r}\n' for p, r in PARTS)
  + '\n| 課 | 主題 | 對應動畫章節 |\n|---|---|---|\n'
  + ''.join(f'| {n} | {t} | 第 {c} 章 |\n' for n, t, c in MAP13)
  + '\n地圖上的箭頭：1→2，2→3→4，2→5，2→6；6→7（讀取接到演算法篇）；7→8→9→10；4→11、10→11；11→12→13。\n\n'
  '## 常見問題\n\n'
  '- 為什麼十二章、十三課對不齊？有些課共用一章（第 3、4 課都用第 6 章；第 8、9 課都用第 7 章），有些課用兩章（第 2 課用第 1、4 章）。\n'
  '- 為什麼十字板做那麼大？大電容讓 E_C 變小，背景電荷雜訊造成的頻率漂移被壓低（簡報第 2 頁：壓到 kHz 等級）。\n'
  '- 動畫裡的晶片是真的嗎？是示意：實際尺寸數百 μm、未按比例；數字是本系列的範例參數。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要帳號。

## `transmon-3d.html`（十二章）

- 畫面下方的章節列：01 晶片、02 約瑟夫森結、03 位能井、04 操控、05 讀取、06 案例、07 振幅長條、08 Shor、09 BV 密碼、10 表面碼、11 邏輯閘、12 軟體堆疊。
- 網址可以直接帶章節：`#chip`、`#junction`、`#potential`、`#control`、`#readout`、`#case`、`#grover`、`#shor`、`#bv`、`#surface`、`#surgery`、`#stack`；另有 `#capacitor`（第 1 章電容分頁）。
- 第 5 章以後多數章節是分步導覽：「◀ 上一步／暫停／重播／下一步 ▶」與「自動接續」，左上方字幕跟著說明。

## 第 1 章按鈕

- 分頁：「晶片總覽」、「大十字電容的作用」。
- 「送出 π 脈衝」、核取「顯示標籤」；電容分頁有「C_Σ」滑桿（5–200 fF）、「回到 77.5 fF」、核取「電場線」「手臂用途」。

## 操作

滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['章', '名稱', '網址', '我按了哪些按鈕', '這章在回答什麼問題', '懂了／打問號', '想深入（圈三章）']
SHEET_ROWS = [[str(n), s, f'transmon-3d.html#{h}', '', '', '', ''] for n, h, s, _, _ in CH12]

EXTRA_CSS = '''table.rec td{height:11mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}
.mind{border:2pt dashed #0b2540;border-radius:4mm;height:120mm;margin-top:4mm;position:relative}
.mind span{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border:2pt solid #0b2540;border-radius:50%;padding:6mm 8mm;font-weight:700}'''


def _rows(chs):
    return ''.join(f'<tr><td>{n}</td><td>{s}</td><td></td><td></td></tr>' for n, _, s, _, _ in chs)


def html():
    head = '<table class="rec"><tr><th>章</th><th>名稱</th><th>這章在回答什麼問題？</th><th>懂了／？</th></tr>'
    pages = [
        '<h2>冒險任務（上）：第 1–6 章</h2><p class="lead">在 transmon-3d.html 用畫面下方的章節列點開每一章，按一兩個按鈕，用一句話寫下它在回答什麼問題。</p>'
        + head + _rows(CH12[:6]) + '</table>'
        '<p class="note">第 1 章小任務：按「送出 π 脈衝」，十字板發金光後怎麼了？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>冒險任務（下）：第 7–12 章</h2><p class="lead">卡住的章節先打問號，之後的課還會回來。</p>'
        + head + _rows(CH12[6:]) + '</table>'
        '<p class="note">闖過幾關？＿＿／12　打問號的是第＿＿＿＿＿章</p>',
        '<h2>換你改造：十二章路線心智圖（今天的作品）</h2><p class="lead">中間是一顆 transmon；外圈分成硬體、演算法、容錯與系統三區，用箭頭連出先後順序。</p>'
        '<div class="mind"><span>一顆 transmon</span></div>'
        '<p>最想深入的三章：第＿＿章，因為＿＿＿＿＿＿＿＿；第＿＿章，因為＿＿＿＿＿＿＿＿；第＿＿章，因為＿＿＿＿＿＿＿＿</p>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p class="note">生活技能：先看全貌再鑽細節——你還能用在哪裡？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 一顆 transmon 從晶片走到軟體，要經過哪幾段？</p><div class="line"></div>'
        '<p>2. 挑一章，說出它在回答什麼問題：</p><div class="line"></div><p>3. 師生對話紀錄分成哪三篇？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出旅程分段：硬體、演算法、容錯與系統</li><li>示範操作第 1 章：送出 π 脈衝，說出金光代表什麼</li>'
        '<li>挑一章說出它在回答什麼問題</li><li>指出一個注意事項：3D 模型未按比例，數字是範例參數</li>'
        '<li>替心智圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q097 十二章旅程列印包', '父子科技學院 量子電腦學程 Q097｜導覽：一顆 transmon 的十二章旅程', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q097-transmon-twelve-chapters', folder='Q097_十二章旅程', files=FILES,
        sheet=('03_闖關紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_十二章旅程.pdf', pack_pages=4,
        pack_needles=('冒險任務（上）', '冒險任務（下）', '心智圖', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q097', episode_dir='specials/q097-transmon-twelve-chapters',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': [f'animations/transmon-3d.html#{h}' for _, h, *_ in CH12],
               'courseMap': {str(n): {'topic': t, 'chapters': c} for n, t, c in MAP13}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q097/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

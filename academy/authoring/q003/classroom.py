"""Q003 課堂教材：擲硬幣與 3D 場景兩個實驗、三角度實驗、誤差表與解答（不需帳號、不需安裝）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q003/classroom.py
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


def p0(deg):
    return math.cos(math.radians(deg) / 2) ** 2


def err(p, n):
    return math.sqrt(p * (1 - p) / n)


NS = [10, 100, 1000, 10000]
ANGLES = [30, 60, 90, 120, 150]
assert round(err(0.5, 1000) * 100, 2) == 1.58

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q003：一看就變（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五分鐘，帶出今天的問題：測量量子位元時，會發生什麼事？

## 這份教材在做什麼

兩個實驗：擲硬幣 100 次、3D 場景跑 1000 次。孩子當實驗員，爸爸當檢查員，最後孩子自己設計三個角度的實驗，畫出「角度 vs 得到零的比例」。
不需要帳號；3D 場景見 `05_三維動畫導覽.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 只得到零或一、塌縮、重複次數與誤差 | 影片第 3–6 段 |
| 25–65 | 實驗一擲硬幣（約 20 分鐘）＋實驗二 3D 場景（約 20 分鐘） | `01_實驗步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 三個角度的實驗、畫折線圖 | 列印包第 3 頁、`03_實驗紀錄.csv` |
| 105–115 | 孩子教爸爸：為什麼要重複很多次 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名 | |

## 課前準備（約 5 分鐘）

- 硬幣兩枚（一人一枚）、鉛筆、尺；列印 `02_列印包_一看就變.pdf`（A4，共 4 頁）。
- 讀一遍 `04_解答與誤差表.md`。

## 檢查員的原則

- 孩子的硬幣是 54 次正面、46 次反面？很正常。一百次的比例上下差五個百分點左右都常見。
- 追問「為什麼和理論值不一樣」時，好答案是「次數有限，比例本來就會跳」，不是「動畫壞了」。
- 擲硬幣只是用來練習統計；量子測量的隨機，依量子力學是規則本身，不是手不穩。

## 誠實說明

- 「塌縮」是教科書的標準說法；物理學家對它背後怎麼解釋還有不同看法，本課不討論。
- 誤差表用的是 √(p(1−p)/N)，代表「大約多少」，不是保證不會超過。
''',

'01_實驗步驟.md': '''# 實驗步驟

## 實驗一：擲硬幣 100 次（約 20 分鐘）

1. 先預測：100 次裡，正面大約幾次？寫在列印包第 1 頁。
2. 擲 100 次，每次在「正面」或「反面」欄畫一筆，五筆一個正字。
3. 算出正面的比例（正面次數 ÷ 100）。
4. 在長條圖格子畫兩根長條：正面、反面。
5. 爸爸也擲 100 次，兩個人比一比，差多少？

## 實驗二：3D 場景（約 20 分鐘）

1. 打開 `animations/operation.html#qubit`。
2. 按「|+⟩」或把 θ 調成 90 度。先猜：1000 次裡會有幾次 0？
3. 按「清除統計」，再按「一次跑 1000 shots」，記下 0 和 1 的次數。
4. 把 θ 調成 60 度，重複第 2、3 步。理論上大約 750 次是 0。
5. 按「測量一次」幾次，看箭頭怎麼跳到北極或南極（塌縮）。

## 下半場：三個角度（約 30 分鐘）

1. 自己選三個角度（例如 30、90、150 度）。
2. 每個角度先清除統計、跑 1000 次，記下得到 0 的比例。
3. 在列印包第 3 頁的圖上，橫軸是角度、縱軸是比例，點三個點連起來。
''',

'04_解答與誤差表.md': '# 解答與誤差表（爸爸用）\n\n## 理論上得到零的比例\n\n'
  + '| 角度 | 得到零 | 一千次大約幾次零 |\n|---|---|---|\n'
  + ''.join(f'| {a} 度 | {p0(a) * 100:.1f}% | {round(p0(a) * 1000)} |\n' for a in ANGLES)
  + '\n## 重複次數與誤差（一半一半的狀態，或擲硬幣）\n\n誤差 ≈ √(p(1−p)/N)，p = 0.5。實際結果大約三分之二的時候落在這個範圍內。\n\n'
  + '| 重複次數 N | 比例大約上下差 | 次數大約上下差 |\n|---|---|---|\n'
  + ''.join(f'| {n} | {err(0.5, n) * 100:.2f} 個百分點 | {err(0.5, n) * n:.1f} 次 |\n' for n in NS)
  + '\n次數變成四倍，比例的誤差減半；精準十倍，要一百倍的次數。\n\n'
  '## 常見問題\n\n'
  '- 孩子的 90 度跑出 0 是 470 次：在一千次上下差 16 次左右的範圍外一點點，仍然可能發生，再跑一次看看。\n'
  '- 塌縮之後「馬上再測一次結果一樣」：3D 場景按「測量一次」後箭頭停在極點，這時再測不會變。\n',

'05_三維動畫導覽.md': '''# 三維動畫導覽

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## 今天要看的場景：`animations/operation.html#qubit`（場景 1：狀態與測量）

- 「測量一次」：箭頭塌縮到北極或南極，下面的燈號亮起。
- 「連續 shots」：一直測量，右邊的長條慢慢接近青色的理論線。
- 「一次跑 1000 shots」：馬上跑一千次。
- 「清除統計」：換角度之前先按。
- 右下小圖：估計的比例隨次數慢慢穩定，灰色帶是大約的誤差範圍。

## 操作

滑鼠拖曳旋轉、滾輪縮放；`H` 隱藏面板；`R` 重設視角。
''',
}

SHEET_HEADER = ['實驗', '角度或硬幣', '預測', '重複次數', '得到零（或正面）次數', '比例', '理論比例', '差多少']
SHEET_ROWS = ([['擲硬幣（我）', '硬幣', '', '100', '', '', '50%'], ['擲硬幣（爸爸）', '硬幣', '', '100', '', '', '50%']]
              + [['3D 場景', f'{a} 度', '', '1000', '', '', f'{p0(a) * 100:.1f}%'] for a in (90, 60)]
              + [['三角度實驗', '我選：', '', '1000'] for _ in range(3)])

EXTRA_CSS = '''table.tally td{height:30mm;vertical-align:top}table.rec td{height:11mm}
.bars{display:grid;grid-template-columns:repeat(10,1fr);border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;height:70mm;margin-top:3mm;
background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt);background-size:100% 7mm}
.plot{height:95mm;border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;margin:3mm 0 0 10mm;position:relative;
background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt),linear-gradient(90deg,#cfdde8 .6pt,transparent .6pt);background-size:100% 9.5mm,10% 100%}
.ylab{position:absolute;left:-10mm;font-size:9pt;color:#4a6a88}.xlab{display:flex;justify-content:space-between;margin-left:10mm;font-size:9pt;color:#4a6a88}
.chk li{margin:3mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    pages = [
        '<h2>實驗一：擲硬幣 100 次</h2><p class="lead">先預測，再擲。每次畫一筆，五筆一個正字。</p>'
        '<p>我預測正面大約：＿＿＿次　　爸爸預測：＿＿＿次</p>'
        '<table class="tally"><tr><th></th><th>正面（正字）</th><th>反面（正字）</th><th>正面比例</th></tr>'
        '<tr><td>我</td><td></td><td></td><td></td></tr><tr><td>爸爸</td><td></td><td></td><td></td></tr></table>'
        '<h3 style="margin-top:5mm">長條圖（每格 10 次）</h3><div class="bars"></div>'
        '<p class="note">下面寫：我的正面、我的反面、爸爸的正面、爸爸的反面。兩個人差了幾次？</p>',
        '<h2>實驗二：3D 場景跑一千次</h2><p class="lead">打開 animations/operation.html#qubit。每次換角度前先按「清除統計」。</p>'
        '<table class="rec"><tr><th>角度</th><th>我猜幾次零</th><th>零的次數</th><th>一的次數</th><th>零的比例</th><th>理論比例</th></tr>'
        f'<tr><td>90 度</td><td></td><td></td><td></td><td></td><td>{p0(90) * 100:.0f}%</td></tr>'
        f'<tr><td>60 度</td><td></td><td></td><td></td><td></td><td>{p0(60) * 100:.0f}%</td></tr>'
        '<tr><td>再跑一次 90 度</td><td></td><td></td><td></td><td></td><td>50%</td></tr></table>'
        '<div class="box" style="margin-top:6mm"><h3>觀察塌縮</h3><p>按「測量一次」五次，每次箭頭跳到哪裡？</p>'
        '<p>1.＿＿＿　2.＿＿＿　3.＿＿＿　4.＿＿＿　5.＿＿＿</p><p>箭頭跳到極點後，再按一次「測量一次」，結果會變嗎？＿＿＿＿</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>檢查員的問題</h3><p>為什麼兩次 90 度的結果不完全一樣？</p><div class="line"></div><div class="line"></div></div>',
        '<h2>下半場：三個角度的實驗</h2><p class="lead">自己選三個角度，每個跑一千次，把點畫在圖上連起來。</p>'
        '<table class="rec"><tr><th>角度</th><th>零的次數</th><th>零的比例</th></tr>'
        + '<tr><td>＿＿度</td><td></td><td></td></tr>' * 3 + '</table>'
        '<div class="plot"><span class="ylab" style="top:-2mm">100%</span><span class="ylab" style="top:45mm">50%</span>'
        '<span class="ylab" style="bottom:-2mm">0%</span></div>'
        '<div class="xlab"><span>0 度</span><span>45</span><span>90</span><span>135</span><span>180 度</span></div>'
        '<p class="note">角度越大，得到零的比例怎麼變？用一句話寫下來：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>最後一關：教爸爸為什麼要重複</h2><div class="box"><ul class="chk">'
        '<li>說出測量的結果只有兩種</li><li>說出測量之後狀態會改變（塌縮）</li>'
        '<li>說出為什麼一次看不出機率</li><li>說出為什麼兩次實驗的次數不一樣</li>'
        '<li>說出一個限制：次數有限，比例就有誤差</li><li>替統計表和長條圖取名字、存檔</li></ul></div>'
        '<div class="box" style="margin-top:6mm"><h3>重複次數與誤差（一半一半）</h3>'
        '<table><tr><th>重複次數</th><th>比例大約上下差</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td>{err(0.5, n) * 100:.1f} 個百分點</td></tr>' for n in (100, 1000, 10000))
        + '</table><p class="note">次數四倍，誤差才減半。</p></div>',
    ]
    return printpack.document('Q003 一看就變 列印包', '父子科技學院 量子電腦學程 Q003｜一看就變', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q003-measure-and-shots', folder='Q003_一看就變', files=FILES,
        sheet=('03_實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_一看就變.pdf', pack_pages=4,
        pack_needles=('擲硬幣 100 次', '長條圖', '3D 場景跑一千次', '觀察塌縮', '三個角度', '最後一關'),
        authoring_dir=XINEW / 'authoring/q003', episode_dir='specials/q003-measure-and-shots',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'errorTable': {n: round(err(0.5, n), 4) for n in NS}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q003/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

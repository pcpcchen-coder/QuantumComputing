"""Q092 課堂教材：量子感測與原子鐘 — 動畫操作步驟、Ramsey 實驗紀錄、猜頻率差、量子感測應用圖、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/index.html（#bloch）與 animations/peripherals.html（#electronics、#bringup），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q092/classroom.py
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

# 01_bloch.js Ramsey 模式：角度 a = 1.5·Δ·t，t > 12 重新開始 → 每輪圈數 = 1.5·Δ·12 / 2π
DETUNE = [0.5, 0.8, 1.0, 1.5, 2.0]
TURNS = {d: round(1.5 * d * 12 / (2 * math.pi), 1) for d in DETUNE}
assert TURNS[2.0] == 5.7 and TURNS[0.8] == 2.3
# 光速約 30 公分／奈秒
GPS = [('1 ns', 0.3), ('10 ns', 3), ('100 ns', 30), ('1 μs', 300)]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q092：量子感測與原子鐘（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：量子電腦還要等，有哪種量子技術早就天天在用？答案是原子鐘與量子感測。

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `index.html#bloch`、`peripherals.html#electronics`、`peripherals.html#bringup`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 原子鐘為什麼準、怎麼鎖定、Ramsey 干涉、量子感測三對象 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 在 #bloch 做 Ramsey 進動實驗、玩猜頻率差 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 找家裡間接用到原子鐘的設備，畫量子感測應用圖 | 列印包第 3 頁、`03_實驗與調查紀錄.csv` |
| 105–115 | 孩子教爸爸：原子鐘與 Ramsey 原理 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#bloch` 按「Ramsey 進動 + T2」，把「失諧 Δ（Ramsey）」拉到 0、1、2，看箭頭轉得多快。
- 列印 `02_列印包_量子感測與原子鐘.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 猜頻率差怎麼玩

孩子背對螢幕。爸爸把失諧滑桿拉到 0.5～2 之間某個位置，再按一次「Ramsey 進動 + T2」讓動畫從頭開始。孩子轉回來，只數箭頭在動畫重來之前（約 12 秒）繞了幾圈，用「圈數 ÷ 3 ≈ 失諧」說出猜測，爸爸公布滑桿數字。

## 誠實說明

- 動畫是相對單位的示意：「圈數 ÷ 3」只適用於這個動畫，不是物理公式。
- #bloch 的 Ramsey 模式只畫赤道上的繞圈與縮短，沒有第二個 π/2 脈衝；「角度變成機率」請搭配 `#bringup` 第 6 步的條紋圖說明。
- 本課最重要的注意事項：量子感測和原子鐘早就有商用產品，比量子計算更早落地。
''',

'01_操作步驟.md': '''# 操作步驟

## A. Ramsey 進動實驗（`index.html#bloch`，約 15 分鐘）

1. 按「Ramsey 進動 + T2」：金色箭頭躺到赤道上繞圈、一邊縮短，約 12 秒後重來。
2. 把「失諧 Δ（Ramsey）」拉到 0.5，再按一次「Ramsey 進動 + T2」從頭開始，數一輪繞幾圈。
3. 依序試 0.8、1.0、1.5、2.0，每次都重按一次再數，記在列印包第 1 頁。
4. 看箭頭旁的 P(1)：為什麼一直是 0.50？

## B. 猜頻率差（約 15 分鐘，至少六回合）

爸爸照「00_爸爸先讀」出題，孩子只數圈數，記在列印包第 2 頁。

## C. 看真機怎麼用 Ramsey（`peripherals.html#bringup`，約 5 分鐘）

1. 按「◀ 上一步」回到第 1 步，再按「下一步 ▶」走到第 6 步 Ramsey。
2. 看插圖的青色條紋：十微秒擺了幾次？擺幅怎麼變？

## D. 看量子電腦裡的原子鐘（`peripherals.html#electronics`，約 5 分鐘）

機櫃最上面的黃色模組是「銣原子鐘 / 10 MHz 分配」，看它閃的時候，側邊的小黃球一起變大。

## E. 下半場：家裡的原子鐘（約 30 分鐘）

在家裡走一圈，找會自動對時、會定位的設備，填在列印包第 3 頁，畫成量子感測應用圖。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## Ramsey 進動：每輪圈數（依 01_bloch.js 計算）\n\n'
  '| 失諧 Δ | 每輪圈數 | 圈數 ÷ 3 |\n|---|---|---|\n'
  + ''.join(f'| {d} | 約 {TURNS[d]} | {round(TURNS[d] / 3, 2)} |\n' for d in DETUNE)
  + '\n圈數 = 1.5 × Δ × 12 ÷ 2π ≈ 2.86 × Δ。畫面上數到的圈數會差零點幾圈，猜到大、中、小就算成功。\n\n'
  '## 時間差與定位誤差（光速約每奈秒 30 公分）\n\n| 時間差 | 位置差 |\n|---|---|\n'
  + ''.join(f'| {t} | 約 {m} 公尺 |\n' for t, m in GPS)
  + '\n## 常見問題\n\n'
  '- 為什麼原子鐘準？同一種原子的超精細躍遷頻率每顆都一樣；一秒定義為銫-133 振盪 9,192,631,770 次。\n'
  '- 原子鐘怎麼運作？電子振盪器的微波照原子，數翻轉的原子數，翻得最多代表對準，偏了就修正。\n'
  '- 為什麼 #bloch 的 P(1) 一直是 0.5？箭頭在赤道上，量 0 或 1 的機會各半；要第二個 π/2 脈衝才能把角度讀成機率。\n'
  '- 為什麼等越久越靈敏？角度 = 頻率差 × 等待時間，等越久角度越大；但等太久相位會亂掉（T₂），所以有上限。\n'
  '- 量子電腦為什麼需要原子鐘？所有儀器鎖在同一個 10 MHz 參考，量子閘的相位就是微波的相位。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `index.html#bloch`（超導場景 1：量子位元與 Bloch 球）

- 單選：Rabi 振盪、Ramsey 進動 + T2、T1 能量弛豫、手動 θ / φ。
- 滑桿「失諧 Δ（Ramsey）」：0–2，預設 0.8。改滑桿不會讓動畫重來，重按單選才會。
- 按鈕「π/2 脈衝 → 疊加態」：把箭頭放到赤道。

## `peripherals.html#bringup`（周邊場景 10：啟動與校準流程）

- 「◀ 上一步」「下一步 ▶」與「自動播放」開關；第 6 步 Ramsey 的插圖是條紋：擺動快慢＝頻率差，包絡給 T₂*。

## `peripherals.html#electronics`（周邊場景 6：室溫控制電子學）

- 機櫃最上層「銣原子鐘 / 10 MHz 分配」；時脈閃爍是示意，真實參考每秒振盪一千萬次。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '失諧（爸爸設定）', '我數到的圈數', '我猜的失諧', '對嗎', '設備名稱', '對時或定位', '源頭', '備註']
SHEET_ROWS = ([['Ramsey 實驗', str(d), '', '', '', '', '', '', ''] for d in DETUNE]
              + [[f'猜頻率差第 {i} 回合', '', '', '', '', '', '', '', ''] for i in range(1, 7)]
              + [[f'家裡設備 {i}', '', '', '', '', '', '', '', ''] for i in range(1, 7)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}.map{height:70mm}'''


def html():
    pages = [
        '<h2>實驗一：Ramsey 進動</h2><p class="lead">在 index.html#bloch：按「Ramsey 進動 + T2」，改失諧後再重按一次，數一輪（約 12 秒）繞幾圈。</p>'
        '<table class="rec"><tr><th>失諧 Δ</th><th>一輪繞幾圈</th><th>圈數 ÷ 3</th><th>箭頭旁的 P(1)</th></tr>'
        + ''.join(f'<tr><td>{d}</td><td></td><td></td><td></td></tr>' for d in DETUNE) + '</table>'
        '<div class="card"><h3>想一想</h3><p>失諧是 0 時，箭頭怎麼動？＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>為什麼 P(1) 一直是 0.5？</p><div class="line"></div><p>等得越久，為什麼越容易分辨很接近的頻率差？</p><div class="line"></div></div>',
        '<h2>科學實驗：猜出頻率差</h2><p class="lead">你背對螢幕，爸爸偷偷拉失諧滑桿。轉回來只數圈數，用「圈數 ÷ 3 ≈ 失諧」猜。</p>'
        '<table class="rec"><tr><th>回合</th><th>我數到的圈數</th><th>我猜的失諧</th><th>真正的失諧</th><th>差多少</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 7)) + '</table>'
        '<p class="note">哪一回合最難猜？＿＿　為什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：量子感測應用圖（今天的作品）</h2><p class="lead">在家裡找會自動對時、會定位的設備，畫線連到原子鐘。</p>'
        '<table class="rec"><tr><th>設備</th><th>自動對時／定位</th><th>源頭（衛星或網路時間）</th></tr>'
        + ''.join('<tr><td></td><td></td><td></td></tr>' for _ in range(5)) + '</table>'
        '<div class="card map"><h3>應用圖：中間畫原子鐘，連到每樣設備；旁邊加上量磁場、量重力的例子</h3></div>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p class="note">算一算：時間差 1 微秒，位置差約＿＿＿公尺（光每奈秒約走 30 公分）。</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 原子鐘為什麼準？</p><div class="line"></div>'
        '<p>2. Ramsey 干涉怎麼把很小的頻率差量出來？</p><div class="line"></div><p>3. 量子感測還能量什麼？</p><div class="line"></div>'
        '<p>4. 一個常見誤解或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出原子鐘為什麼準：每顆原子頻率都一樣</li><li>說出 Ramsey：兩個 π/2 夾一段等待</li>'
        '<li>說出量子電腦為什麼也需要原子鐘</li><li>指出一個誤解：量子感測比量子計算更早落地</li>'
        '<li>替量子感測應用圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q092 量子感測與原子鐘 列印包', '父子科技學院 量子電腦學程 Q092｜量子感測與原子鐘', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q092-quantum-sensing-atomic-clock', folder='Q092_量子感測與原子鐘', files=FILES,
        sheet=('03_實驗與調查紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子感測與原子鐘.pdf', pack_pages=4,
        pack_needles=('Ramsey 進動', '猜出頻率差', '量子感測應用圖', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q092', episode_dir='specials/q092-quantum-sensing-atomic-clock',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/index.html#bloch', 'animations/peripherals.html#bringup', 'animations/peripherals.html#electronics'],
               'ramseyTurnsPerCycle': {str(k): v for k, v in TURNS.items()}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q092/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

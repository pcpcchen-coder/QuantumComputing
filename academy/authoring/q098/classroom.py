"""Q098 課堂教材：LC 與 JJ：線性和非線性的差別 — 圖解操作步驟、預測與實驗紀錄、線性 vs 非線性對照表、第 4 步說明、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/lc-vs-jj.html（#s1–#s5），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q098/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 以 lc-vs-jj.html 同一個電荷基底哈密頓量 H = 4E_C n² − E_J cos φ 重算（E_C/h = 0.25 GHz，n = −25…25）
# (E_J/E_C, LC 每階間距 GHz, transmon ω01, ω12, ω23 GHz, α MHz)
LEVELS = [
    (20, 3.16, 2.89, 2.53, 2.42, -364),
    (30, 3.87, 3.60, 3.29, 2.99, -309),
    (50, 5.00, 4.73, 4.45, 4.13, -287),
    (60, 5.48, 5.21, 4.93, 4.62, -283),
    (80, 6.32, 6.06, 5.79, 5.48, -277),
    (120, 7.75, 7.49, 7.22, 6.93, -271),
]
# 第 2 步：sin(A·sin ωt) 的 3ω 諧波 / 基頻（頁面同一個貝索函數數值積分）
HARM = [(0.3, 0.4), (1.4, 9.3), (3.0, 91.2)]

TABLE = [('電流–磁通', 'I = Φ/L，直線', 'I = I_c sin φ，正弦'),
         ('電感', '常數 L', 'L_J0 / cos φ，隨相位改變'),
         ('位能', '拋物線', '餘弦'),
         ('正弦驅動', '同頻率，振幅成正比', '波峰壓平，冒出 3ω、5ω'),
         ('量子能階', '等間距', '越上越擠（非諧性 α）'),
         ('能不能當量子位元', '不能，驅動一路往上爬', '可以，0→1 能單獨打到'),
         ('耗散', '超導時無耗散', '超導時也無耗散')]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q098：LC 與 JJ：線性和非線性的差別（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片要回答一個問題：LC 電路和約瑟夫森接面（JJ）看起來那麼像，為什麼只有 JJ 能做成量子位元？

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `lc-vs-jj.html`。它是一份二維圖解，往下捲有第 1–6 步和一張總結表。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 兩個電路的差別：直線 vs 正弦 | 影片第 3–5 段、`05_圖解導覽.md` |
| 25–65 | 圖解第 1–5 步，每步先預測再拖滑桿驗證 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 用第 4 步寫：為什麼線性 LC 停不在 |1⟩ | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸操作與原理 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 自己把 `lc-vs-jj.html` 從頭捲到尾一次，試拖第 1 步的「相位 φ」、第 2 步的「驅動振幅 A」、第 3 步的「E_J / E_C」。
- 列印 `02_列印包_LC與JJ.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 科學實驗怎麼玩

爸爸先說「我要把某個滑桿拖到哪裡」，孩子在列印包第 1 頁寫下預測，爸爸再拖，兩人一起看圖。猜錯就把原因寫進對照表。

## 誠實說明

- 圖解裡的能階數字是本學程範例參數（E_C/h = 250 MHz）的數值解，不是某一顆實際晶片。
- 「非線性」指的是電流和磁通的關係不是直線，不是電路會亂跳——這是本課最常見的誤解。
''',

'01_操作步驟.md': '''# 操作步驟（`animations/lc-vs-jj.html`）

## 第 1 步：電流與磁通（`#s1`，約 8 分鐘）

1. 藍色直線是電感 I = φ，橘色曲線是 JJ I = sin φ。
2. 把「相位 φ」從 0 慢慢往右拖：兩個圓點先重疊，再分開；灰色切線越來越平。
3. 拖到 π/2（約 1.57）：切線水平；再往右，JJ 的電流反而變小（負的等效電感）。

## 第 2 步：用正弦波去推（`#s2`，約 8 分鐘）

1. 把「驅動振幅 A」拖到 3：橘色波形波峰被壓平，下方頻譜的 3ω、5ω 長條變高。
2. 拖到 0.3：橘色幾乎變回純正弦，3ω 長條幾乎看不到。

## 第 3 步：位能與能階（`#s3`，約 10 分鐘）

1. 「E_J / E_C」預設 50：左邊拋物線的間距數字全部一樣，右邊餘弦的間距一格比一格小。
2. 拖到 20：右邊出現井頂虛線，最上面的能階冒出井口變成虛線。
3. 拖到 60：右邊間距 5.21、4.93、4.62，和簡報第 14 頁相同。

## 第 4 步：用微波去推（`#s4`，約 8 分鐘）

看「LC」那一列（全部重疊）和「Transmon」那一列（只有 0→1 是綠色）。滑桿和第 3 步共用。

## 第 5 步：非線性藏在哪裡（`#s5`，約 6 分鐘）

橘色實線是 1 − cos φ，藍色虛線是只留二次項的拋物線，陰影是四次項造成的差距。

## 下半場：換你改造（約 30 分鐘）

用列印包第 3 頁，根據第 4 步的圖寫出：為什麼線性 LC 停不在 |1⟩。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 第 3 步的能階（以圖解同一個哈密頓量重算，E_C/h = 250 MHz）\n\n'
  '| E_J/E_C | LC 每階間距 | Transmon 0→1 | 1→2 | 2→3 | 非諧性 α |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {r} | {lc:.2f} GHz | {a:.2f} | {b:.2f} | {c:.2f} | {al} MHz |\n' for r, lc, a, b, c, al in LEVELS)
  + '\nE_J/E_C = 60 就是簡報第 14 頁的範例（E_J/h = 15 GHz）。E_J/E_C 越大，α 只稍微變小，但頻率越高。\n\n'
  '## 第 2 步的諧波（3ω ÷ 基頻）\n\n| 驅動振幅 A | 3ω／基頻 |\n|---|---|\n'
  + ''.join(f'| {a} rad | 約 {h}% |\n' for a, h in HARM)
  + '\n## 線性 vs 非線性對照表（參考答案）\n\n| 項目 | LC 電路 | 約瑟夫森接面 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in TABLE)
  + '\n## 第 4 步參考說明\n\nLC 的能階等間距，所以 0→1、1→2、2→3 的頻率完全一樣。對準 0→1 的微波同時也對準所有更高的躍遷，'
  '狀態會一路往上爬（變成同調態），沒辦法只用 |0⟩ 和 |1⟩。Transmon 的 1→2 比 0→1 低約 283 MHz，微波只打得到 0→1。\n\n'
  '## 常見問題\n\n'
  '- 非線性是不是電路會亂跳？不是，是電流和磁通的關係不是一條直線。\n'
  '- 為什麼不用二極體或電晶體當非線性元件？它們會耗能，破壞量子狀態；JJ 在超導時沒有電阻。\n'
  '- 有了非諧性就萬無一失嗎？不是。脈衝太短、頻寬太寬，還是會漏到 |2⟩（圖解第 6 步 DRAG）。\n',

'05_圖解導覽.md': '''# 圖解導覽

學程的互動圖解在 pcpcchen-coder/QuantumComputing 的 `animations/lc-vs-jj.html`，下載後用瀏覽器開啟，不需要網路或帳號。

- 藍色是線性的 LC（電感），橘色是約瑟夫森接面（JJ）。
- `#s1` 第 1 步：電流與磁通，滑桿「相位 φ」（−4.71～4.71）。
- `#s2` 第 2 步：正弦驅動，滑桿「驅動振幅 A（rad）」（0.1～3）。
- `#s3` 第 3 步：位能與量子能階，滑桿「E_J / E_C」（10～120，預設 50）；E_C/h 固定 250 MHz。
- `#s4` 第 4 步：躍遷頻率圖，和第 3 步共用滑桿。綠色是被驅動打到，灰色是沒打到。
- `#s5` 第 5 步：泰勒展開，靜態圖。
- `#s6drag` 第 6 步：DRAG（延伸，本課不要求）；`#s6`：總結表。
''',
}

SHEET_HEADER = ['步驟', '操作', '我的預測', '實際看到', '猜對嗎', '寫進對照表的一句話']
SHEET_ROWS = [['第 1 步', '相位 φ 從 0 拖到 π/2', '', '', '', ''],
              ['第 1 步', '相位 φ 超過 π/2', '', '', '', ''],
              ['第 2 步', '驅動振幅 A 拖到 3', '', '', '', ''],
              ['第 2 步', '驅動振幅 A 拖到 0.3', '', '', '', ''],
              ['第 3 步', 'E_J/E_C 拖到 20', '', '', '', ''],
              ['第 3 步', 'E_J/E_C 拖到 120', '', '', '', ''],
              ['第 4 步', '看 LC 與 Transmon 兩列', '', '', '', ''],
              ['第 5 步', '看陰影區', '', '', '', '']]

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>科學實驗：先預測再驗證</h2><p class="lead">在 lc-vs-jj.html：爸爸說要拖哪個滑桿，你先寫預測，再一起看圖。</p>'
        '<table class="rec"><tr><th>步驟</th><th>操作</th><th>我的預測</th><th>實際看到</th><th>猜對嗎</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td><td></td><td></td></tr>' for a, b, *_ in SHEET_ROWS) + '</table>',
        '<h2>線性 vs 非線性對照表（今天的作品）</h2><p class="lead">左欄寫 LC 電路，右欄寫約瑟夫森接面。</p>'
        '<table class="rec"><tr><th>項目</th><th>LC 電路</th><th>約瑟夫森接面</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, *_ in TABLE) + '</table>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>',
        '<h2>換你改造：LC 為什麼停不在 |1⟩</h2><p class="lead">看圖解第 4 步的躍遷頻率圖。</p>'
        '<div class="box"><p>1. LC 那一列：0→1、1→2、2→3 的頻率是＿＿＿＿＿（一樣／不一樣）</p>'
        '<p>2. Transmon 那一列：被綠色打到的是＿＿＿＿＿，其他是＿＿＿＿＿色</p>'
        '<p>3. 用自己的話說明：</p><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>'
        '<p class="note">生活技能：用對照表整理差異——你還能把哪兩樣東西排成對照表？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 電感和 JJ 的電流–磁通曲線差在哪裡？</p><div class="line"></div>'
        '<p>2. 為什麼 LC 能階等間距，JJ 越上越擠？</p><div class="line"></div><p>3. 非諧性有什麼用？</p><div class="line"></div>'
        '<p>4. 一個誤解或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：直線 vs 正弦</li><li>說出：拋物線等間距、餘弦越上越擠</li>'
        '<li>說出：微波為什麼只打到 0→1</li><li>指出：非線性不是電路亂跳；脈衝太快會漏到 |2⟩</li>'
        '<li>替對照表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q098 LC 與 JJ 列印包', '父子科技學院 量子電腦學程 Q098｜LC 與 JJ：線性和非線性的差別', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q098-lc-vs-jj-nonlinearity', folder='Q098_LC與JJ線性和非線性', files=FILES,
        sheet=('03_預測與實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_LC與JJ.pdf', pack_pages=4,
        pack_needles=('科學實驗', '對照表', 'LC 為什麼停不在', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q098', episode_dir='specials/q098-lc-vs-jj-nonlinearity',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/lc-vs-jj.html#s1', 'animations/lc-vs-jj.html#s3', 'animations/lc-vs-jj.html#s4',
                          'animations/lc-vs-jj.html#s5'],
               'levelsGHz': {str(r): [lc, a, b, c] for r, lc, a, b, c, _ in LEVELS}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q098/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

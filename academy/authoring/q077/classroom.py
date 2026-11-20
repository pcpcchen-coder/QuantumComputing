"""Q077 課堂教材：光子量子電腦 — 光路元件卡、兩路干涉儀預測、闖關紀錄、加一顆光子（HOM）、說明卡與解答。

免安裝、不需帳號：可用學程的 animations/operation.html#interference 當兩路干涉儀的數學對照，用瀏覽器開啟。
實體部分只用鏡子、透明壓克力片與安全光源示意光路；家用光源不是單光子，看到的是示意，不是量子實驗。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q077/classroom.py
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

# 理想兩路干涉儀（兩臂距離相同、50:50 分光鏡）：出口 0 的機率 = cos²(φ/2)，與 08_interference.js 的 P(0) 相同
PHASES = [0, 90, 180, 270, 360]
P0 = [(f, round(math.cos(math.radians(f) / 2) ** 2, 2)) for f in PHASES]
assert P0[0][1] == 1.0 and P0[2][1] == 0.0 and P0[1][1] == 0.5

# 闖關：五關光路（爸爸出題用）
LEVELS = [
    ('第 1 關', '一片分光鏡，一顆光子', '兩個偵測器各一半（每次只響一個）'),
    ('第 2 關', '兩片分光鏡排成干涉儀，相位 0°', '永遠同一個出口（出口 0）'),
    ('第 3 關', '同一台干涉儀，相位 180°', '永遠另一個出口（出口 1）'),
    ('第 4 關', '同一台干涉儀，擋住一條路', '干涉消失，通過的光子兩出口各一半'),
    ('第 5 關', '兩顆一樣的光子同時從分光鏡兩邊進', '總是一起從同一個出口出來（HOM）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q077：光子量子電腦（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出光子平台的三個元件（分光鏡、相位器、單光子偵測器）、兩路干涉儀、Hong–Ou–Mandel 效應、玻色取樣與測量式量子計算。

學程目前沒有光子平台的專屬簡報或 3D 場景（課綱標為「需新增」）。數學對照可用 `animations/operation.html#interference`：兩個 H 對應兩片分光鏡、「相位 φ」對應相位器。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 光路四元件、兩條路 vs 一條路 | 影片第 3–6 段、`05_動畫導覽.md` |
| 25–65 | 畫兩路干涉儀、預測輸出、闖關五關 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 加一顆光子：預測 HOM 結果、錯開抵達時間 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：光路怎麼走 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 鏡子兩面、透明壓克力片兩片（當分光片）、手電筒或安全光源；**不要用雷射筆對著眼睛，也不要讓光反射到別人臉上**。
- 先自己在 `#interference` 拖一次「A：相位 φ」，再開「A：中途偵測路徑」。
- 列印 `02_列印包_光子量子電腦.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 誠實說明

- 家用光源發出的是大量光子，鏡子與壓克力片只能示意光路，看不到單光子干涉或 HOM 效應；預測要用紙上的光路圖和動畫來對答案。
- 「兩條路都開時永遠同一個出口」假設兩臂距離相同、分光鏡是理想 50:50。
- 光子很難直接互相作用，路上丟失光子（損耗）是光子平台的主要挑戰。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 認識元件（約 10 分鐘）

在列印包第 1 頁畫出四種元件的符號：鏡子（斜線）、分光鏡（虛線斜線）、相位器（小方塊）、單光子偵測器（半圓）。

## B. 動畫對照：兩路干涉儀（`operation.html#interference`，約 10 分鐘）

1. 確認選的是「單一量子位元：兩條路徑」。
2. 拖「A：相位 φ」到 0°、90°、180°、270°，把右上（出口 0）與右下（出口 1）的 P(0)、P(1) 記在列印包第 1 頁。
3. 打開「A：中途偵測路徑（破壞干涉）」，看兩個出口變成多少。

## C. 闖關（約 20 分鐘，五關）

爸爸照 `04_解答.md` 的關卡在紙上畫光路（或用鏡子與壓克力片擺出來示意），孩子先預測哪個偵測器會響、說出理由，再對答案，記在列印包第 2 頁。

## D. 下半場：加一顆光子（約 30 分鐘）

在光路設計圖上讓兩顆一樣的光子同時從分光鏡兩邊進入，預測兩個偵測器會不會同時響；再讓其中一顆晚一點到，預測結果。寫在列印包第 3 頁。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 兩路干涉儀（理想、兩臂距離相同；與動畫 P(0) = cos²(φ/2) 相同）\n\n'
  '| 相位 φ | 出口 0 機率 | 出口 1 機率 |\n|---|---|---|\n'
  + ''.join(f'| {f}° | {p:.2f} | {1 - p:.2f} |\n' for f, p in P0)
  + '\n擋住一條路（或偵測走哪條路）：干涉消失，兩出口各一半。\n\n## 闖關五關\n\n| 關卡 | 光路 | 答案 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in LEVELS)
  + '\n## 加一顆光子（Hong–Ou–Mandel，1987）\n\n'
  '- 兩顆一模一樣、同時抵達的光子從 50:50 分光鏡兩邊進入：總是一起從同一個（隨機）出口出來，兩個偵測器不會同時各響一次。\n'
  '- 讓其中一顆晚到（或兩顆可分辨）：效應消失，常常一邊一顆。\n\n'
  '## 常見問題\n\n'
  '- 光子會被分光鏡切成兩半嗎？不會。一顆光子在兩個出口形成疊加，偵測時只在一個偵測器出現。\n'
  '- 為什麼兩位元閘難做？光子幾乎不互相作用；線性光學方案（KLM）靠額外光子與測量造出等效互動，成功率不是百分之百。\n'
  '- 玻色取樣是萬用量子電腦嗎？不是，它是受限的計算任務；九章（2020）最多偵測到 76 顆光子。\n'
  '- 測量式量子計算：先準備糾纏的資源態（叢集態），再逐一測量來推進計算，主要考慮用光子實作。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。學程尚無光子平台專屬場景。

## `operation.html#interference`（操作場景 8：干涉）

- 選項：「單一量子位元：兩條路徑」、「3 位元：8 條路徑（Deutsch–Jozsa）」。本課只用第一個。
- 滑桿「A：相位 φ」：0–360°。開關「A：自動掃描 φ」、「A：中途偵測路徑（破壞干涉）」。
- 右上大圓盤是結果 |0⟩、右下是結果 |1⟩；藍、橙箭頭是兩條路的貢獻，白色是總和。右下小圖是 P(0) 對 φ 的干涉條紋。
- 對照光路：第一個 H ＝ 第一片分光鏡、相位 φ ＝ 相位器、第二個 H ＝ 第二片分光鏡、兩個出口 ＝ 兩個單光子偵測器。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '光路／相位', '我的預測', '實際結果', '對嗎', '備註']
SHEET_ROWS = ([['干涉儀相位', f'{f}°', '', '', '', ''] for f in PHASES]
              + [[a, b, '', '', '', ''] for a, b, _ in LEVELS]
              + [['加一顆光子', '同時抵達', '', '', '', ''], ['加一顆光子', '一顆晚到', '', '', '', '']])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}.draw{border:1pt dashed #6b7c93;height:62mm;margin-top:3mm}'''


def html():
    pages = [
        '<h2>第一關：元件與兩路干涉儀</h2><p class="lead">在 operation.html#interference 拖「A：相位 φ」，把兩個出口的機率記下來。</p>'
        '<table class="rec"><tr><th>相位 φ</th><th>我先預測：哪個出口</th><th>出口 0 機率</th><th>出口 1 機率</th></tr>'
        + ''.join(f'<tr><td>{f}°</td><td></td><td></td><td></td></tr>' for f in PHASES) + '</table>'
        '<p>打開「中途偵測路徑」後：出口 0 ＝＿＿＿　出口 1 ＝＿＿＿</p>'
        '<div class="card"><h3>光路設計圖（今天的作品）</h3><p>畫出光源、鏡子、分光鏡、相位器、偵測器。</p><div class="draw"></div>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>闖關：爸爸擺光路、你預測</h2><p class="lead">先說出預測和理由，再對答案。答錯就重畫光路，再闖一次。</p>'
        '<table class="rec"><tr><th>關卡</th><th>光路</th><th>我的預測</th><th>答案</th><th>對嗎</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td><td></td><td></td></tr>' for a, b, _ in LEVELS) + '</table>'
        '<p class="note">安全：光源不可直視，不要讓光反射到別人眼睛。</p>',
        '<h2>換你改造：加一顆光子</h2><p class="lead">兩顆一模一樣的光子，同時從分光鏡的兩邊進來。</p>'
        '<div class="box"><p>1. 我預測：兩個偵測器會同時各響一次嗎？＿＿＿　理由：</p><div class="line"></div>'
        '<p>2. 對照 Hong–Ou–Mandel 效應，實際會怎樣？</p><div class="line"></div>'
        '<p>3. 讓其中一顆光子晚一點到，結果會變成怎樣？</p><div class="line"></div></div>'
        '<p class="note">生活技能：用光傳遞資訊——光纖網路每天都用光在送資料。你想到哪個例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 分光鏡、相位器、單光子偵測器各做什麼？</p><div class="line"></div>'
        '<p>2. 兩路干涉儀的輸出怎麼預測？</p><div class="line"></div><p>3. 玻色取樣和測量式量子計算是什麼？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三種元件</li><li>說出相位怎麼決定出口</li>'
        '<li>說出擋住一條路時干涉為什麼消失</li><li>指出一個限制：光子難直接互動、損耗是主要挑戰</li>'
        '<li>替光路設計圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q077 光子量子電腦 列印包', '父子科技學院 量子電腦學程 Q077｜光子量子電腦', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q077-photonic-quantum-computer', folder='Q077_光子量子電腦', files=FILES,
        sheet=('03_闖關與預測紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_光子量子電腦.pdf', pack_pages=4,
        pack_needles=('兩路干涉儀', '光路設計圖', '闖關', '加一顆光子', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q077', episode_dir='specials/q077-photonic-quantum-computer',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#interference'],
               'interferometerP0': dict(P0), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q077/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

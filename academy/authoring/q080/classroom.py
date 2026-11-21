"""Q080 課堂教材：平台大比較與供電分析 — 動畫操作步驟、平台評分表、產品評審紀錄、換權重計算、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/atoms.html#compare 與 animations/power1000.html#outage，用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q080/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

CRIT = ['時間尺度', '連接性', '錯誤率', '設施', '供電']
PLATFORMS = ['超導', '離子阱', '中性原子', '光子', '半導體自旋', '拓樸']

# 簡報 Ion_NeutralAtom_Talk.pptx p39–43、qc-power-supply.pptx p44 與 13_compare.js 的代表值（2024–2026）
FACTS = [
    ('兩位元閘時間', '~50–60 ns', '10–200 μs', '~0.3 μs'),
    ('1000 個兩位元閘', '50 μs', '0.1 s', '0.3 ms（不含搬運）'),
    ('讀取', '~0.5 μs（色散微波）', '~200 μs（螢光）', '~ms（成像）'),
    ('T₂ ÷ 閘時間', '≈ 2×10³', '≈ 10⁴ 以上', '≈ 3×10⁶（計入搬運約 10³–10⁴）'),
    ('連接性', '最近鄰（固定），遠距靠 SWAP', '同鏈全連接；QCCD 搬運', '搬運重排 → 任意配對'),
    ('最佳兩位元閘保真度', '~99.7–99.9%', '99.9–99.99%', '~99.5–99.7%'),
    ('規模（2025）', '~100–1000+', '~100（Helios 98）', '數百～6000+ 顆原子'),
    ('核心設施', '10 mK 稀釋冷凍機＋壓縮機', '超高真空、5–10 種雷射', '超高真空玻璃腔、光鑷雷射'),
    ('單套功率', '約 20–30 kW', '< 40 kW（官方）～60 kW', '約 3–10 kW（無官方數字）'),
    ('斷電後恢復', '重新降溫 2–5 天＋全校準', '數十分鐘～數小時', '數十分鐘～數小時'),
]

# 示範分數（1–5，製作代理自訂，只為示範權重效果；不是客觀評比）
EXAMPLE = {'超導': [3, 2, 4, 2, 3], '離子阱': [5, 5, 5, 4, 2], '中性原子': [4, 4, 3, 4, 5]}
W_EQUAL = [1, 1, 1, 1, 1]
W_POWER = [1, 1, 1, 1, 3]


def total(scores, w):
    return sum(s * x for s, x in zip(scores, w))


T_EQ = {k: total(v, W_EQUAL) for k, v in EXAMPLE.items()}
T_PW = {k: total(v, W_POWER) for k, v in EXAMPLE.items()}
assert T_EQ == {'超導': 14, '離子阱': 21, '中性原子': 20}
assert T_PW == {'超導': 20, '離子阱': 25, '中性原子': 30}
assert max(T_EQ, key=T_EQ.get) == '離子阱' and max(T_PW, key=T_PW.get) == '中性原子'

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q080：平台大比較與供電分析（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片用五把尺比較超導、離子阱、中性原子：時間尺度、連接性、錯誤率、設施、供電。

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `atoms.html#compare`（三平台比較）和 `power1000.html#outage`（斷電時間軸）。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 五把尺：速度、比值、連接、錯誤率、設施與用電 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 替六個平台打分數、玩產品評審 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 換一組權重（供電 ×3），看排名怎麼變 | 列印包第 3 頁、`03_評分與權重紀錄.csv` |
| 105–115 | 孩子教爸爸：怎麼比平台、為什麼快不一定贏 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `atoms.html#compare` 依序按「連接性」「閘速度」「相干時間」「規模」，看柱子和標籤怎麼變。
- 列印 `02_列印包_平台大比較.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md` 的代表值表。

## 產品評審怎麼玩

爸爸抽一個平台當廠商，用一分鐘只講優點。孩子當評審：先說出五把尺，再打 1–5 分，並追問一個弱點（例如離子阱閘慢、超導要稀釋冷凍機、中性原子讀取慢、原子會丟失）。

## 誠實說明

- 所有數字是學程簡報與動畫標示的 2024–2026 代表值，各家、各年差異很大。
- 光子、半導體自旋、拓樸三欄學程還沒有共同的比較表，請用 Q077–Q079 的筆記填；查不到就畫問號，不要猜。
- 離子阱「0 ms 不能中斷」與三種 UPS 設計邏輯，是供電文件標示的推論。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 三平台比較（`atoms.html#compare`，約 15 分鐘）

1. 按「連接性」：看超導晶片相鄰的耦合線、離子之間的弧線、被光鑷拉著走的原子。
2. 按「閘速度」：柱子比連續做 1000 個兩位元閘要多久（動畫 1 秒 = 真實 20 ms）；按「↻ 重播」再看一次。
3. 按「相干時間」：柱子變成 log₁₀(T₂ ÷ 閘時間)，看排名怎麼換；讀中性原子的標籤「計入搬運」。
4. 按「規模」：已展示的量子位元或原子數（對數）。
5. 看右下角小圖：兩位元閘、讀取、T₂ 三列的時間尺度。

## B. 斷電時間軸（`power1000.html#outage`，約 5 分鐘，只有超導）

1. 備援方案選 A：曲線約 2 分鐘超過 1 K，之後要好幾天才降回。
2. 改選 B：冷卻鏈接 UPS＋發電機接手，曲線是平的。

## C. 替六個平台打分數（約 20 分鐘）

用列印包第 1 頁，每把尺 1–5 分。超導、離子阱、中性原子用代表值表；光子、半導體自旋、拓樸用前幾堂筆記，查不到畫問號。

## D. 下半場：換權重（約 30 分鐘）

列印包第 3 頁：先五項權重都是 1 算總分排名；再把供電權重改成 3 重算，比較兩次排名，寫下排名為什麼變。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 代表值表（簡報 p39–43、供電簡報 p44、動畫 13_compare.js）\n\n'
  '| 項目 | 超導 | 離子阱 | 中性原子 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in FACTS)
  + '\n## 示範分數（只為示範權重效果，不是標準答案）\n\n| 平台 | ' + ' | '.join(CRIT) + ' | 等權總分 | 供電 ×3 總分 |\n|---|' + '---|' * (len(CRIT) + 2) + '\n'
  + ''.join(f'| {k} | ' + ' | '.join(map(str, v)) + f' | {T_EQ[k]} | {T_PW[k]} |\n' for k, v in EXAMPLE.items())
  + '\n- 等權：離子阱第一（21）、中性原子第二（20）、超導第三（14）。\n- 供電 ×3：中性原子第一（30）、離子阱第二（25）、超導第三（20）。\n\n'
  '孩子的分數不同沒關係；驗收看的是能不能說清楚每個分數的依據，以及排名為什麼變。\n\n'
  '## 常見問題\n\n'
  '- 為什麼快不一定贏？要看相干時間 ÷ 閘時間：失去相干前能做幾個閘；真正的循環還包含讀取、搬運、冷卻。\n'
  '- 離子阱沒有稀釋冷凍機，為什麼不一定比較省電？要 5–10 種雷射和精密空調；Helios 官方 < 40 kW，Oracle 合作資料約 60 kW（不含外部空調）。\n'
  '- 為什麼量子機房 UPS 不能只有一種？超導保冷卻鏈（分鐘）、離子阱保離子（毫秒，推論）、中性原子保熱穩態（秒～分鐘）。\n'
  '- 99.99% 是整台機器嗎？不是，是兩顆離子的展示（簡報 p42）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `atoms.html#compare`（離子阱與中性原子場景 13：三平台比較）

- 左：超導晶片（藍）＋ 10 mK 稀釋冷凍機；中：離子鏈（金）；右：原子陣列（青），粉紅色光鑷拉著幾顆原子移動。
- 按鈕：連接性、閘速度、相干時間、規模、↻ 重播。
- 右下小圖：時間尺度比較（秒，log 座標，代表值）。

## `power1000.html#outage`（1000 位元供電場景 5：斷電時間軸）

- 只畫超導。下拉選單「備援方案」A／B／C；滑桿「UPS 撐住冷卻鏈的時間（方案 C）」。
- 曲線是教學示意，依 LRZ 公開數據（約 2 分鐘超過 1 K、恢復 2–5 天）繪製。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放（atoms.html）。
''',
}

SHEET_HEADER = ['平台'] + [f'{c}（1–5）' for c in CRIT] + ['等權總分', '供電 ×3 總分', '依據／備註']
SHEET_ROWS = [[p] + [''] * (len(CRIT) + 3) for p in PLATFORMS]

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def _grid(cols):
    return ('<table class="rec"><tr><th>平台</th>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr>'
            + ''.join('<tr><td>' + p + '</td>' + '<td></td>' * len(cols) + '</tr>' for p in PLATFORMS) + '</table>')


def html():
    pages = [
        '<h2>平台評分表（今天的作品）</h2><p class="lead">每把尺 1–5 分。光子、半導體自旋、拓樸查不到就畫「？」。</p>'
        + _grid(CRIT + ['依據'])
        + '<div class="card"><h3>我的標準</h3><p>我最在乎的一把尺：＿＿＿＿＿＿　因為：＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>產品評審：爸爸推銷、你評分</h2><p class="lead">爸爸抽一個平台，用一分鐘只講優點；你用五把尺打分，並追問一個弱點。</p>'
        '<table class="rec"><tr><th>回合</th><th>平台</th><th>廠商說的優點</th><th>我追問的弱點</th><th>依據（數字）</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 7)) + '</table>'
        '<p class="note">生活技能：決策時先說清楚標準。你今天用了哪五把尺？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：換一組權重</h2><p class="lead">總分 = 每把尺的分數 × 權重，再加起來。</p>'
        + _grid(['等權總分', '名次', '供電 ×3 總分', '名次'])
        + '<p>排名變了嗎？誰上升、誰下降？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p><p>為什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p class="note">再試一組你自己的權重：＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 比較平台的五把尺是什麼？</p><div class="line"></div>'
        '<p>2. 為什麼「快」不一定贏？</p><div class="line"></div><p>3. 三個平台斷電時各要保護什麼？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出五把尺：時間尺度、連接性、錯誤率、設施、供電</li><li>說出為什麼要看相干時間 ÷ 閘時間</li>'
        '<li>說出換權重之後排名為什麼變</li><li>指出一個限制：數字是代表值，各家各年差很多</li>'
        '<li>替平台評分表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q080 平台大比較與供電分析 列印包', '父子科技學院 量子電腦學程 Q080｜平台大比較與供電分析', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q080-platform-comparison-power', folder='Q080_平台大比較與供電分析', files=FILES,
        sheet=('03_評分與權重紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_平台大比較.pdf', pack_pages=4,
        pack_needles=('平台評分表', '產品評審', '換一組權重', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q080', episode_dir='specials/q080-platform-comparison-power',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#compare', 'animations/power1000.html#outage'],
               'exampleScores': EXAMPLE, 'criteria': CRIT, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q080/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

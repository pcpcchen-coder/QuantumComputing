"""Q076 課堂教材：類比量子模擬 — 紙上阻斷實驗、相圖觀察紀錄、動畫操作步驟、類比 vs 數位比較表、說明卡與解答。

免安裝、不需帳號：紙、尺、硬幣，加上學程的 animations/atoms.html（#rydberg、#tweezer），用瀏覽器開啟。
課綱列的「★ 芮德堡陣列有序相場景」尚未存在，失諧與有序相用紙上阻斷規則代替。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q076/classroom.py
"""
from itertools import combinations
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 動畫 10_rydberg.js 的代表值：C₆/2π = 858 GHz·μm⁶ = 858000 MHz·μm⁶、Ω/2π = 2 MHz
C6, OMEGA = 858000.0, 2.0
RB = (C6 / OMEGA) ** (1 / 6)                     # ≈ 8.68 μm
assert abs(RB - 8.68) < 0.01
V = lambda r: C6 / r ** 6                         # MHz  # noqa: E731
N_SITES = 13
SPACINGS = [2.5, 3, 4, 5, 7, 10]                  # μm（紙上 1 公分 = 1 微米，紙條 8.7 公分 = 阻斷半徑）


def pattern(a, n=N_SITES, rb=8.7):
    """硬阻斷規則（失諧為正）：距離 < rb 的兩顆不能同時激發，激發數越多越好。從左邊開始貪婪放置（一維時就是最多）。"""
    out, last = [], None
    for i in range(n):
        if last is None or (i - last) * a >= rb:
            out.append(i); last = i
    return out


def brute_max(a, n=N_SITES, rb=8.7):
    for k in range(n, 0, -1):
        for c in combinations(range(n), k):
            if all((c[j + 1] - c[j]) * a >= rb for j in range(k - 1)):
                return k
    return 0


ROWS = []
for a in SPACINGS:
    p = pattern(a)
    assert len(p) == brute_max(a)
    ROWS.append((a, ''.join('●' if i in p else '○' for i in range(N_SITES)), len(p), len(p) and (p[1] - p[0] if len(p) > 1 else 1)))
# 2.5 μm：每 4 顆一顆；3、4 μm：每 3 顆一顆；5、7 μm：隔一顆；10 μm：全部
assert [r[3] for r in ROWS] == [4, 3, 3, 2, 2, 1]

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q076：類比量子模擬（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片的問題是：能不能不把問題拆成量子閘，直接讓原子陣列扮演想研究的材料？

需要：A4 紙或白紙、尺、十幾枚硬幣、一段 8.7 公分的紙條（代表阻斷半徑），以及瀏覽器開 `animations/atoms.html#rydberg`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 方程式的三個旋鈕、類比模擬的一輪、有序相怎麼出現 | 影片第 3–6 段 |
| 25–65 | 紙上阻斷實驗、動畫裡拉間距、畫相圖 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 比較類比模擬與數位線路的優缺點 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：怎麼調出有序的圖案 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 在桌上（或長條紙上）用尺畫 13 個點，間距先用 5 公分；紙上 1 公分代表 1 微米。
- 自己在 `#rydberg` 拖一次「原子間距 r (μm)」滑桿，看綠色阻斷球在約 8.7 μm 變灰。
- 列印 `02_列印包_類比量子模擬.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 紙上阻斷實驗怎麼玩

爸爸說出「間距 X 微米、失諧為正／負」。孩子先在紀錄表寫預測，再放硬幣（硬幣＝被激發到芮德堡態的原子）：
失諧為負，一枚都不放；失諧為正，硬幣越多越好，但任兩枚硬幣的距離都不能小於紙條（{RB:.1f} 公分）。

## 誠實說明

- 課綱想要的「芮德堡陣列有序相場景」還沒做好；學程動畫只有兩顆原子的阻斷場景，沒有可調失諧的多原子場景。
- 紙上規則是簡化的「硬阻斷」：阻斷半徑內最多一顆激發、失諧為正就盡量多激發。真實實驗是量子演化，邊界附近和長程尾巴會讓圖案不完美。
- 交互作用數值與阻斷半徑 8.7 μm 是動畫的代表值（銣原子 70S 量級）。
- 最重要的注意事項：類比模擬只能模擬和硬體相像的模型，不是通用計算。
''',

'01_操作步驟.md': f'''# 操作步驟

## A. 動畫：間距和交互作用（`atoms.html#rydberg`，約 10 分鐘）

1. 看右邊能階圖上方的金色字「V/h = C₆/r⁶ ≈ … MHz」。
2. 把「原子間距 r (μm)」拉到 3、4、5、7、9、10、12，每次記下 V 的數字、阻斷球是綠色（阻斷）還是灰色（不阻斷），寫在列印包第 1 頁。
3. 找出從「阻斷」變成「不阻斷」的間距（約 {RB:.1f} μm）。這就是紙條的長度。

## B. 紙上阻斷實驗（約 20 分鐘）

1. 13 個點排成一列，間距依序用 2.5、3、4、5、7、10 公分（1 公分 = 1 微米）。
2. 每一種間距先寫預測，再放硬幣；失諧為負時一枚都不放。
3. 把結果畫成 ●（激發）○（基態），數一數激發幾顆，記在列印包第 2 頁的相圖觀察紀錄。

## C. 畫相圖（約 10 分鐘）

橫軸是間距、縱軸是失諧（負／正），每一格寫上你看到的圖案名稱：「全暗」、「隔一顆」、「隔兩顆」、「隔三顆」、「全亮」。

## D. 可選：先把原子排整齊（`atoms.html#tweezer`）

按「全部重來」、把「陣列大小」調成 4，依序按「① 裝載」「② 成像」「③ 重排」，看光鑷把原子補成沒有缺口的方格——類比模擬開始前，陣列要先排好。

## E. 下半場：類比 vs 數位（約 30 分鐘）

用列印包第 3 頁的表，各寫兩個優點、一個缺點，再寫一句「什麼問題適合用類比、什麼問題要用數位」。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 動畫裡的交互作用（以動畫常數 C₆/2π = 858 GHz·μm⁶ 計算）\n\n'
  '| 間距 | V（MHz） | 阻斷？（R_b ≈ 8.7 μm） |\n|---|---|---|\n'
  + ''.join(f'| {r} μm | {V(r):.0f} | {"阻斷" if r < RB else "不阻斷"} |\n' if V(r) >= 100 else f'| {r} μm | {V(r):.2f} | {"阻斷" if r < RB else "不阻斷"} |\n'
            for r in [3, 4, 5, 7, 9, 10, 12])
  + '\n動畫畫面在 V ≥ 100 時顯示整數，否則顯示兩位小數。距離加倍，V 變成 1/64。\n\n'
  '## 紙上阻斷實驗（13 個點，失諧為正；失諧為負一律全暗 ○○○…）\n\n| 間距 | 圖案 | 激發數 | 每幾顆一顆 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} μm | {s} | {k} | {p} |\n' for a, s, k, p in ROWS)
  + '\n規律：阻斷半徑 ÷ 間距越大，激發的原子就隔得越開；間距大於阻斷半徑時，全部都能激發。間距 5、7 μm 的「隔一顆」就是影片說的棋盤式有序相（像反鐵磁的一上一下）。\n\n'
  '（製作代理另以「雷射強度趨近零」的古典能量 E = −Δ Σn + Σ V nn 窮舉 12 顆原子檢查：失諧為負時全暗；失諧為正、間距 5–6 μm 時出現隔一顆的排法，4 μm 附近出現隔兩顆的片段，10 μm 時全亮，與紙上規則的趨勢一致。）\n\n'
  '## 類比 vs 數位（參考答案）\n\n'
  '- 類比優點：不用拆成大量的閘，整個陣列一起演化；很適合研究和硬體相像的材料（量子相變、自旋液體）與圖最佳化（最大獨立集）。\n'
  '- 類比缺點：只能模擬和硬體相像的模型，不是通用計算；旋鈕只有雷射強度、失諧和排列。\n'
  '- 數位優點：什麼演算法都能寫；走向可錯誤更正的通用計算。\n'
  '- 數位缺點：需要很多層閘，每層都帶進誤差；中性原子的搬運與讀取也花時間。\n'
  '- 同一套中性原子硬體可以兩種模式都用（簡報第 37 頁）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `atoms.html#rydberg`（中性原子場景 10：芮德堡阻斷與 CZ 閘）

- 滑桿「原子間距 r (μm)」：2–15。綠色球＝阻斷範圍（R_b ≈ 8.7 μm）；間距大於 R_b 時變灰。
- 右邊雙原子能階圖：最上面 |rr⟩（兩顆都激發）會隨 V 往上推；上方金字是 V 的數值。
- 「▶ 雷射脈衝」：右下插圖畫出 P(gg)、P(單激發)、P(rr) 隨時間變化。

## `atoms.html#tweezer`（中性原子場景 8：光鑷裝載與重排）

- 按鈕：① 裝載、② 成像、③ 重排、全部重來；滑桿：陣列大小、裝載機率 p。

## 還沒有的場景

課綱列的「芮德堡陣列有序相場景」（可調失諧、看到多顆原子排出有序圖案）尚未製作；本課用紙上阻斷實驗代替。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '間距（μm）', '失諧（正／負）', 'V（MHz）', '阻斷？', '我的預測', '實際圖案', '激發數', '備註']
SHEET_ROWS = ([['動畫：間距與 V', str(r), '', '', '', '', '', '', ''] for r in [3, 4, 5, 7, 9, 10, 12]]
              + [['紙上實驗', str(a), d, '', '', '', '', '', ''] for a in SPACINGS for d in ('負', '正')])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}.dots{letter-spacing:2mm;font-size:13pt}'''


def html():
    dots = '○' * N_SITES
    pages = [
        '<h2>實驗一：間距和交互作用</h2><p class="lead">在 atoms.html#rydberg 拖「原子間距 r (μm)」，記下能階圖上方金字的 V，以及阻斷球的顏色。</p>'
        '<table class="rec"><tr><th>間距</th><th>V（MHz）</th><th>阻斷球顏色</th><th>阻斷／不阻斷</th></tr>'
        + ''.join(f'<tr><td>{r} μm</td><td></td><td></td><td></td></tr>' for r in [3, 4, 5, 7, 9, 10, 12]) + '</table>'
        '<p>從阻斷變成不阻斷的間距約：＿＿＿ μm　→　紙條剪成＿＿＿公分</p>'
        '<p class="note">距離加倍，V 變成幾分之一？＿＿＿</p>',
        '<h2>相圖觀察紀錄（今天的作品）</h2><p class="lead">13 個點，1 公分＝1 微米。先寫預測，再放硬幣：紙條內只能有一枚，越多越好；失諧為負就不放。</p>'
        '<table class="rec"><tr><th>間距</th><th>失諧</th><th>我的預測</th><th>實際圖案（●／○）</th><th>激發數</th></tr>'
        + ''.join(f'<tr><td>{a} μm</td><td>{d}</td><td></td><td class="dots">{dots}</td><td></td></tr>' for a in SPACINGS for d in ('負', '正')) + '</table>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>',
        '<h2>換你改造：類比和數位比一比</h2><p class="lead">各寫兩個優點、一個缺點。</p>'
        '<table class="rec"><tr><th></th><th>類比模擬</th><th>數位線路</th></tr>'
        '<tr><td>優點 1</td><td></td><td></td></tr><tr><td>優點 2</td><td></td><td></td></tr><tr><td>缺點</td><td></td><td></td></tr></table>'
        '<p>什麼問題適合用類比？＿＿＿＿＿＿＿＿＿＿＿＿＿</p><p>什麼問題一定要用數位？＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<div class="card"><h3>相圖</h3><p>橫軸：間距（2.5、3、4、5、7、10 μm）；縱軸：失諧（負／正）。每格寫圖案名稱。</p>'
        '<div class="line"></div><div class="line"></div><div class="line"></div></div>'
        '<p class="note">生活技能：用模型研究難以直接觀察的系統。你還想到哪個「用模型研究」的例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 類比量子模擬和數位線路差在哪裡？</p><div class="line"></div>'
        '<p>2. 方程式的三個旋鈕是什麼？</p><div class="line"></div><p>3. 有序的圖案是怎麼出現的？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：不拆成閘，讓陣列直接演化</li><li>說出三個旋鈕：雷射強度、失諧、交互作用</li>'
        '<li>說出有序相：失諧調正＋阻斷 → 隔一顆激發一顆</li><li>指出一個限制：只能模擬和硬體相像的模型，不是通用計算</li>'
        '<li>替相圖觀察紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q076 類比量子模擬 列印包', '父子科技學院 量子電腦學程 Q076｜類比量子模擬', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q076-analog-quantum-simulation', folder='Q076_類比量子模擬', files=FILES,
        sheet=('03_相圖觀察紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_類比量子模擬.pdf', pack_pages=4,
        pack_needles=('間距和交互作用', '相圖觀察紀錄', '類比和數位比一比', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q076', episode_dir='specials/q076-analog-quantum-simulation',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#rydberg', 'animations/atoms.html#tweezer'],
               'missingScene': '★ 芮德堡陣列有序相場景（課綱需新增，尚未存在）',
               'blockadeRadiusUm': round(RB, 2), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q076/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

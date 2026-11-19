"""Q068 課堂教材：闖關步驟（atoms.html#ionqubit 依序冷卻、光泵浦、微波閘、偵測）、闖關紀錄表、能階圖底稿、偵測直方圖觀察表、
只用 Python 內建功能的亮暗讀取模擬 ion_readout.py、解說卡與解答。

不需要帳號，也不需要安裝任何套件（ion_readout.py 只用 Python 標準函式庫；動畫用瀏覽器開啟）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q068/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理以 python 3 實跑 ion_readout.py（random.seed(68)，各 20000 次）的結果：偵測時間 → (亮態平均, 閾值, 判別保真度 %)
READOUT = {50: (5, 0, 98.44), 100: (10, 1, 99.76), 200: (20, 2, 99.73), 300: (30, 2, 99.67), 500: (50, 3, 99.61)}
assert all(abs(m - 0.1 * t) < 1e-9 for t, (m, _, _) in READOUT.items())
GAP = round(12.6 + 2.1, 1)  # |0⟩ 往上可吸收的線與偵測光的差（GHz）
assert GAP == 14.7

PROGRAM = '''"""父子科技學院 量子電腦學程 Q068：離子亮暗讀取模擬（只用 Python 內建功能，不需要安裝任何套件）

執行：python ion_readout.py
模型（和動畫 atoms.html#ionqubit 相同的代表值）：
  亮態 |1⟩：物鏡每微秒收到 0.1 個光子；背景每微秒 0.0005 個
  亮態偶爾經偏共振激發漏到暗態（平均 10000 μs 一次），暗態漏到亮態（平均 100000 μs 一次）
做法：各模擬 20000 次亮態與暗態，找出錯誤最少的閾值（光子數 > 閾值 判為 1）。
"""
import math
import random

random.seed(68)
R, BG, TAU1, TAU0 = 0.1, 0.0005, 10000, 100000


def poisson(lam):
    """數光子：平均 lam 的卜瓦松亂數。"""
    L, k, p = math.exp(-lam), 0, 1.0
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            return k - 1


def shot(bright, t):
    """偵測 t 微秒，回傳收到幾個光子。"""
    tp = random.expovariate(1 / (TAU1 if bright else TAU0))
    te = min(t, tp) if bright else max(0.0, t - tp)
    return poisson(R * te + BG * t)


def best_threshold(t, n=20000):
    c0 = [shot(False, t) for _ in range(n)]
    c1 = [shot(True, t) for _ in range(n)]
    best = None
    for thr in range(12):
        err = (sum(c > thr for c in c0) + sum(c <= thr for c in c1)) / (2 * n)
        if best is None or err < best[1]:
            best = (thr, err)
    return best


# 改造區：換別的偵測時間試試看（微秒）
for t in (50, 100, 200, 300, 500):
    thr, err = best_threshold(t)
    print(f'偵測 {t:3d} μs：亮態平均 {R * t:4.0f} 個光子，閾值 > {thr}，判別保真度 ≈ {100 * (1 - err):.2f}%')

print('暗態 |0⟩ 為什麼暗：偵測光對準 F=1 → F′=0；|0⟩ 往上能吸收的線差了 12.6 + 2.1 =', round(12.6 + 2.1, 1), 'GHz')
'''

STAGES = [
    ('第一關', '① Doppler 冷卻', '369 nm（＋935 nm 回泵）', '金色標籤變成「已冷卻：尚未初始化」', '為什麼雷射頻率要略低於共振？'),
    ('第二關', '② 光泵浦初始化 |0⟩', '369 nm ＋ 2.1 GHz 邊帶', '布洛赫球箭頭指向 |0⟩，P(|1⟩) = 0%', '為什麼最後一定停在 |0⟩？'),
    ('第三關', '④ 微波 π', '12.6 GHz 微波', 'P(|1⟩) = 100%', 'π 脈衝的效果像哪一個量子閘？'),
    ('第四關', '③ 微波 π/2', '12.6 GHz 微波（時間減半）', 'P(|1⟩) = 50%', '為什麼時間減半，轉的角度也減半？'),
    ('第五關', '⑤ 偵測（螢光）', '369 nm（只和 |1⟩ 共振）', '直方圖多一根柱子（藍或紅）', '亮代表 0 還是 1？'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q068：¹⁷¹Yb⁺ 量子位元與雷射冷卻（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的問題：一顆鐿一七一離子怎麼變成量子位元？又怎麼冷卻、歸零、轉動、讀出來？
今天的好玩機制是「闖關」：爸爸當關主，孩子在互動動畫 `animations/atoms.html#ionqubit` 依序過五關，每關先說出「用哪道光、為什麼」才能按下一步，最後畫出自己的能階圖。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 超精細量子位元、Doppler 冷卻、光泵浦 | 影片第 3–6 段、列印包第 2 頁 |
| 25–65 | 闖關：冷卻 → 光泵浦 → 微波 π → 微波 π/2 → 偵測；每關填紀錄、畫箭頭 | `01_闖關步驟.md`、列印包第 1–2 頁、`03_闖關紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子解釋：為什麼 \\|0⟩ 不會被偵測光激發（差 14.7 GHz）；在動畫各偵測 \\|0⟩、\\|1⟩ 一次；跑一千次看直方圖 | 列印包第 3 頁、（選用）`ion_readout.py` |
| 105–115 | 孩子教爸爸：能階、流程、亮暗判讀 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替能階圖命名、存檔 | |

## 課前準備（約 15 分鐘）

- 電腦或平板的瀏覽器能開 `animations/atoms.html#ionqubit`（下載學程 repo 後直接開檔即可，不需要網路或帳號）。先自己按一次 ① → ② → ③ → ⑤。
- 列印 `02_列印包_離子量子位元.pdf`（A4，共 4 頁）；準備彩色筆（藍、紅、紫、粉紅、青）畫能階圖。
- 讀一遍 `04_解答.md`，關主檢查題的答案都在裡面。

## 誠實說明

- 動畫的數字是代表值（例如亮態每微秒收到 0.1 個光子、Doppler 極限約 0.5 mK），不是某一台機器的實測。
- 動畫的步驟會「排隊」：連按幾顆按鈕，會一個做完才做下一個；等金色標籤回到「待命」或「已冷卻」再按下一關比較清楚。
- 1600×900 以下的螢幕，左邊面板只看得到 ①② 兩顆按鈕，往下捲動面板才看得到 ③④⑤、「一次跑 1000 shots」、「偵測時間」滑桿和讀數。也可以按 `H` 隱藏面板看全畫面。
- 判別保真度和閾值是動畫每次載入時用亂數重新校準的，數字會有一點點不同（200 μs 時大約 99.6%–99.9%）。
- 動畫的 π/2 是「繞 x 軸轉 90°」，結果是一半一半，但它**不是**哈達瑪閘；不要混在一起。
''',

'01_闖關步驟.md': '# 闖關步驟（關主：爸爸；闖關者：孩子）\n\n'
  '開 `animations/atoms.html#ionqubit`（場景 3「離子量子位元」）。先按「重置」。每一關：\n'
  '1. 闖關者先說出：這一關按哪顆按鈕、用哪一道光、為什麼要做。\n'
  '2. 關主點頭後才按；看畫面變化，填進列印包第 1 頁。\n'
  '3. 在能階圖底稿（列印包第 2 頁）畫上這一關的箭頭，用和動畫一樣的顏色。\n'
  '4. 順序錯了（例如沒歸零就偵測），回第一關重來。\n\n'
  '| 關卡 | 按鈕 | 用到的光 | 過關時畫面上看到 | 關主檢查題 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} |\n' for a, b, c, d, e in STAGES).replace('|0⟩', '\\|0⟩').replace('|1⟩', '\\|1⟩')
  + '\n## 下半場：為什麼 |0⟩ 是暗的（約 30 分鐘）\n\n'
  '1. 看能階圖：|0⟩ 比 |1⟩ 低多少？偵測光（紫色 369 nm 箭頭）是從哪一層往上？\n'
  '2. 從 |0⟩ 往上能吸收的那條線（到 F′=1），和偵測光差多少？（提示：12.6 GHz ＋ 2.1 GHz）\n'
  '3. 驗證：② 歸零 → ⑤ 偵測，看直方圖柱子落在哪；② → ④ → ⑤，再看一次。\n'
  '4. 加碼：② → ③ → 「一次跑 1000 shots」，看藍紅兩堆；把「偵測時間」改成 50 μs、500 μs 再跑，記錄保真度。\n'
  '5. （選用）在電腦上執行 `python ion_readout.py`，比較程式和動畫的閾值與保真度。\n',

'ion_readout.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 關主檢查題\n\n'
  '- 第一關：雷射頻率略低於共振，只有迎著光跑的離子因都卜勒效應「看到」頻率變高、剛好共振而吸收，被往回推；放光方向隨機，平均下來越跑越慢。\n'
  '- 第二關：369 nm 加 2.1 GHz 邊帶只會激發 |1⟩；掉回 |1⟩ 會再被激發，掉到 |0⟩ 就沒有共振的光，不再吸光，所以最後一定停在 |0⟩。\n'
  '- 第三關：π 脈衝把 |0⟩ 翻成 |1⟩，效果像翻轉閘。\n'
  '- 第四關：微波讓量子位元以固定速度在布洛赫球上轉，轉的角度和脈衝時間成正比；時間減半，角度從 180° 變 90°。\n'
  '- 第五關：亮代表 1（369 nm 只和 |1⟩ 共振，循環躍遷一直放光），暗代表 0。\n\n'
  f'## 為什麼 |0⟩ 是暗的\n\n偵測光對準 F=1 → F′=0。|0⟩（F=0）往上能吸收的線是到 F′=1，需要的頻率比偵測光高 12.6 ＋ 2.1 ≈ {GAP} GHz，差太多，幾乎不吸收，所以暗。\n\n'
  '## ion_readout.py 的輸出（製作代理實跑）\n\n| 偵測時間 | 亮態平均 | 閾值 | 判別保真度 |\n|---|---|---|---|\n'
  + ''.join(f'| {t} μs | {m} 個 | > {th} | {f:.2f}% |\n' for t, (m, th, f) in READOUT.items())
  + '\n偵測太短，亮暗兩堆靠在一起；偵測太久，亮態有機會漏成暗態，保真度反而略降。動畫裡 200 μs 時約 99.6%–99.9%、50 μs 時約 98%–98.8%（每次載入略有不同）。\n\n'
  '## 常見誤解\n\n- 「雷射冷卻是讓雷射變冷」——錯。雷射沒有變冷，是原子被一次次推慢；溫度量的是原子亂跑的程度。\n'
  '- 「π/2 脈衝就是哈達瑪閘」——不是；兩者都會從 |0⟩ 做出一半一半，但轉的軸不同。\n'
  '- 「偵測一次就知道疊加的比例」——每次偵測只得到亮或暗；要重複很多次（一千次）才看得出比例。\n',

'05_動畫導覽.md': '''# 動畫導覽：atoms.html#ionqubit（離子阱與中性原子 場景 3「離子量子位元」）

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

- 左半：能階圖。藍色「|0⟩ ²S₁/₂ F=0」、紅色「|1⟩ ²S₁/₂ F=1」（Δ = 12.6 GHz）；上方「²P₁/₂ F′=0」「²P₁/₂ F′=1」（Δ = 2.1 GHz）；右邊「²D₃/₂」「³D[3/2]₁/₂」。
- 中間：金色離子、369／935 nm 雷射、上方「高 NA 物鏡 → PMT（光子計數）」、下方「微波號角」；離子下方的金色標籤顯示目前狀態。
- 右邊：布洛赫球（上 |0⟩、下 |1⟩），標籤顯示 P(|1⟩)；右下：「偵測光子數直方圖（藍：真值 |0⟩，紅：真值 |1⟩）」，黃色虛線是閾值。
- 左邊面板：「① Doppler 冷卻」「② 光泵浦初始化 |0⟩」「③ 微波 π/2」「④ 微波 π」「⑤ 偵測（螢光）」「一次跑 1000 shots」「重置」、「偵測時間 (μs)」滑桿（50–500）。
- 操作：`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；左右方向鍵換場景（下一堂會用場景 4「離子鏈集體振動」）。
''',
}

SHEET_HEADER = ['關卡', '按鈕', '先說出：用哪道光', '先說出：為什麼', '關主點頭（✓）', '畫面上看到', '能階圖畫了箭頭（✓）']
SHEET_ROWS = ([[a, b] for a, b, *_ in STAGES]
              + [['改造', f'偵測 {s}'] for s in ('|0⟩', '|1⟩')]
              + [['改造', f'一次跑 1000 shots（{t} μs）'] for t in (50, 200, 500)])

EXTRA_CSS = '''table.rec td{height:12mm}table.rec{font-size:11pt}table.qt td{height:10mm}
.chk li{margin:2.4mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.draw{border:1pt dashed #7f9bb3;border-radius:3mm;height:150mm;margin-top:3mm;position:relative}
.draw span{position:absolute;font-size:10pt;color:#4a6a88}'''


def html():
    rows1 = ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td><td></td><td></td></tr>' for a, b, *_ in STAGES)
    rows3 = ''.join(f'<tr><td>{t} μs</td><td></td><td></td><td></td><td></td></tr>' for t in (50, 200, 500))
    pages = [
        '<h2>闖關紀錄：五關</h2><p class="lead">爸爸是關主，你是闖關者。每一關先說出「用哪道光、為什麼」，關主點頭才能按。</p>'
        '<table class="rec"><tr><th>關卡</th><th>按鈕</th><th>用哪道光</th><th>為什麼要做</th><th>畫面上看到什麼</th></tr>'
        + rows1 + '</table>'
        '<div class="box" style="margin-top:4mm"><p>我覺得最難的一關是＿＿＿＿＿＿，因為＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>順序如果弄錯（例如沒歸零就偵測），會發生＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<p class="note">動畫的步驟會排隊依序執行；等金色標籤寫「待命」再按下一關比較清楚。</p>',
        '<h2>能階圖底稿：今天的作品</h2><p class="lead">照動畫畫出能階，再用彩色筆畫上每一關的箭頭（紫 369 nm、粉紅 935 nm、淡紫 369 nm + 2.1 GHz、青 12.6 GHz 微波）。</p>'
        '<div class="draw"><span style="left:3mm;top:2mm">上方：²P₁/₂ F′=0、F′=1（相差＿＿＿ GHz）</span>'
        '<span style="right:3mm;top:40mm">右邊：²D₃/₂、³D[3/2]₁/₂</span>'
        '<span style="left:3mm;bottom:16mm">|1⟩ = F=1（紅）</span><span style="left:3mm;bottom:3mm">|0⟩ = F=0（藍）　相差＿＿＿ GHz</span></div>'
        '<p style="margin-top:3mm">作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>',
        '<h2>換你改造：偵測直方圖觀察表</h2><p class="lead">為什麼 |0⟩ 不會被偵測光激發？先看能階圖，再用動畫驗證。</p>'
        '<div class="box"><p>偵測光（369 nm）從＿＿＿往上，對準 F=1 → F′=＿＿。|0⟩ 往上能吸收的線到 F′=1，和偵測光差 12.6 ＋ ＿＿＿ ＝ ＿＿＿ GHz。</p>'
        '<p>② 歸零 → ⑤ 偵測：柱子是＿＿色，落在＿＿＿個光子附近。② → ④ → ⑤：柱子是＿＿色，落在＿＿＿個光子附近。</p></div>'
        '<p style="margin-top:3mm">② → ③ → 「一次跑 1000 shots」，再改「偵測時間」：</p>'
        '<table class="rec qt"><tr><th>偵測時間</th><th>亮態平均</th><th>閾值</th><th>判別保真度</th><th>藍紅兩堆分得開嗎</th></tr>' + rows3 + '</table>'
        '<p style="margin-top:3mm">我發現：偵測時間太短會＿＿＿＿＿＿＿＿；太長會＿＿＿＿＿＿＿＿。</p>',
        '<h2>解說卡：我的能階圖</h2><div class="box"><p>1. 量子位元的 0 和 1 是哪兩個能階？</p><div class="line"></div>'
        '<p>2. 冷卻、光泵浦、偵測，各自用光做了什麼？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：0 和 1 是 ¹⁷¹Yb⁺ 基態的兩個超精細能階（F=0、F=1，差 12.6 GHz）</li>'
        '<li>說出流程：冷卻 → 光泵浦歸零 → 微波閘 → 螢光偵測</li>'
        '<li>解釋為什麼 |0⟩ 是暗的（差 14.7 GHz）</li>'
        '<li>指出一個誤解：雷射冷卻是讓原子變慢，不是讓雷射變冷</li>'
        '<li>替能階圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q068 離子量子位元 列印包', '父子科技學院 量子電腦學程 Q068｜¹⁷¹Yb⁺ 量子位元與雷射冷卻', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q068-yb-qubit-cooling', folder='Q068_鐿離子量子位元與雷射冷卻', files=FILES,
        sheet=('03_闖關紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_離子量子位元.pdf', pack_pages=4,
        pack_needles=('闖關紀錄', '能階圖底稿', '偵測直方圖觀察表', '解說卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q068', episode_dir='specials/q068-yb-qubit-cooling',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（ion_readout.py 只用 Python 標準函式庫）',
               'program': 'ion_readout.py', 'animation': 'animations/atoms.html#ionqubit',
               'darkStateDetuningGHz': GAP, 'readoutTable': {f'{t}us': {'brightMean': m, 'threshold': th, 'fidelityPct': f} for t, (m, th, f) in READOUT.items()},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q068/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

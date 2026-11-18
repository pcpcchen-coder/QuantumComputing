"""Q041 課堂教材：溫度換算表、競速計時卡、3 GHz／8 GHz 改造表、說明卡、解答與可執行的驗算程式。

不需要帳號、不需要安裝；只要一台有指數鍵（eˣ 或 exp）的計算機。驗算程式只用 Python 標準函式庫。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q041/classroom.py
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

H, KB, EV = 6.62607015e-34, 1.380649e-23, 1.602176634e-19   # SI 定義值
TEMPS = [('室溫', 300.0), ('液氮', 77.0), ('液氦', 4.2), ('稀釋冷凍機', 0.01)]


def t_star(f_ghz):
    """量子位元能量換成溫度（K）：hf / k_B。"""
    return H * f_ghz * 1e9 / KB


def boltz(f_ghz, T):
    """波茲曼因子 exp(−hf/kT)。"""
    return math.exp(-t_star(f_ghz) / T)


# 和 fact-check.md 的數字互相核對
assert round(H * 5e9 / EV * 1e6, 2) == 20.68 and round(t_star(5), 3) == 0.240
assert round(boltz(5, 77), 4) == 0.9969 and round(boltz(5, 4.2), 4) == 0.9445 and abs(boltz(5, 0.01) - 3.79e-11) < 1e-13
assert round(t_star(3), 3) == 0.144 and round(t_star(8), 3) == 0.384
assert round(t_star(3) / math.log(100) * 1e3, 1) == 31.3 and round(t_star(8) / math.log(100) * 1e3, 1) == 83.4


SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')


def fmt(x):
    if x > 0.001:
        return f'{x:.4f}'
    m, e = f'{x:.1e}'.split('e')
    return f'{m}×10' + str(int(e)).translate(SUP)


assert fmt(3.789e-11) == '3.8×10⁻¹¹'


PROGRAM = '''"""父子科技學院 量子電腦學程 Q041：為什麼要 10 mK——溫度換算驗算程式（只用標準函式庫）

執行：python temperature_table.py
先自己用計算機算完，再用這個程式對答案。
"""
import math

h = 6.62607015e-34      # 普朗克常數 J·s（定義值）
k = 1.380649e-23        # 波茲曼常數 J/K（定義值）
eV = 1.602176634e-19    # 1 電子伏特是多少焦耳

TEMPS = [("室溫", 300), ("液氮", 77), ("液氦", 4.2), ("稀釋冷凍機", 0.01)]

for f_ghz in (3, 5, 8):                       # 想試別的頻率，改這一行
    E = h * f_ghz * 1e9                       # 量子位元的一份能量（焦耳）
    T_star = E / k                            # 換成溫度（克耳文）
    print(f"{f_ghz} GHz：hf = {E / eV * 1e6:.2f} μeV ≈ {T_star:.3f} K")
    for name, T in TEMPS:
        x = E / (k * T)                       # 比值 hf / kT
        print(f"   {name:>5} {T:>7} K   hf/kT = {x:10.4g}   exp(-hf/kT) = {math.exp(-x):.4g}")
    print(f"   熱激發 < 1% 要低於 {T_star / math.log(100) * 1000:.0f} mK\\n")
'''

ANSWER_ROWS = ''.join(
    f'| {n} | {T:g} K | {t_star(5) / T:.4g} | {fmt(boltz(5, T))} |\n' for n, T in TEMPS)

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q041：為什麼要 10 mK（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的問題：量子晶片為什麼要放在 10 mK？答案是拿量子位元的一份能量 hf 和熱能 k_BT 比一比。

## 你只需要

- 一台有指數鍵（eˣ、exp 或 SHIFT + ln）的計算機；手機的科學計算機也可以。
- 列印 `02_列印包_溫度換算.pdf`（A4，共 4 頁）、一支有秒表的手機當計時器。
- 先讀一遍 `04_解答.md`。想用電腦對答案，可以跑 `temperature_table.py`（只要 Python，不需安裝套件）。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | hf 與 k_BT 是什麼、5 GHz 換算成 0.24 K、波茲曼因子三步 | 影片第 3–6 段、列印包第 1 頁上半 |
| 25–65 | 溫度換算競速：孩子當計算員、爸爸當裁判，填完 5 GHz 換算表 | 列印包第 1、2 頁、`03_溫度換算表.csv` |
| 65–75 | 休息 | |
| 75–105 | 改造：3 GHz 與 8 GHz 各需要多冷 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：原理與一個常見誤解 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 裁判的原則

- 先估數量級再按計算機：5 GHz ≈ 0.24 K，頻率加倍、溫度也加倍。估對數量級，再算精確值。
- 計時只算到「寫下答案」為止；答案錯就不算這一題的時間，改對再計。
- 遇到 exp(−0.0008) 這種很接近 1 的數，答案寫「≈ 0.999」就算對；要看的是「接近 1」還是「幾乎是 0」。

## 計算機小提醒

- 科學記號：5 GHz = 5 × 10⁹ Hz；普朗克常數 6.626 × 10⁻³⁴；波茲曼常數 1.381 × 10⁻²³。
- 很多計算機的指數鍵是 SHIFT + ln（標成 eˣ）；先算出比值，再按「−」和 eˣ。
- exp(−24) 太小，有些計算機會顯示 3.775…E−11，意思是 3.775 × 10⁻¹¹。

## 誠實說明

- 波茲曼因子 exp(−hf/kT) 其實是「激發態對基態的機率比」。低溫時幾乎等於熱激發機率；高溫時兩能階的激發機率會接近一半（0.5），不是 1。
- 簡報講者備註說「100 mK 熱激發到百分之一量級」，我們驗算 5 GHz 約 9%，所以不採用那句話。
- 真實晶片的「等效溫度」常比冷凍機底板高（動畫寫 40–60 mK），本課不深入。
- 10 mK 不是為了讓電腦變快，而是為了讓熱雜訊幾乎不存在。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：5 GHz 溫度換算競速（約 40 分鐘）

1. 先一起算一次（不計時）：E = 6.626×10⁻³⁴ × 5×10⁹ ≈ 3.3×10⁻²⁴ J；再除以 1.381×10⁻²³ → 約 0.24 K。寫在列印包第 1 頁最上面。
2. 換算表一列一題：比值 x = 0.24 ÷ 溫度 → 加負號 → 按 eˣ。
3. 爸爸按秒表喊「開始」，孩子寫完答案喊「好」；記在第 2 頁的計時卡。
4. 四題都算完後，把「熱激發」那一欄由大到小排一排：哪一個溫度才夠冷？
5. 加碼題：100 mK、50 mK、1.2 K（鋁的超導溫度）。

## 下半場：3 GHz 與 8 GHz（約 30 分鐘）

1. 先估：3 GHz 大約是 5 GHz 的幾倍？溫度也就是 0.24 K 的幾倍？
2. 再算：hf ÷ k_B 得到 T*；熱激發 < 1% 的上限 = T* ÷ 4.6（因為 ln 100 ≈ 4.6）。
3. 在 10 mK 時，3 GHz 和 8 GHz 的熱激發各是多少？哪一個比較怕熱？
4. 用 `temperature_table.py` 對答案（可選）。
''',

'temperature_table.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  f'## 5 GHz：hf = 3.313×10⁻²⁴ J ≈ 20.68 μeV；hf/k_B = {t_star(5):.4f} K\n\n'
  '| 地方 | 溫度 | 比值 hf/kT | 波茲曼因子 exp(−hf/kT) |\n|---|---|---|---|\n' + ANSWER_ROWS +
  '\n加碼題：100 mK → x = 2.4、exp(−2.4) ≈ 0.091（約 9%，還是太多）；50 mK → x = 4.8、≈ 0.0082；1.2 K → x = 0.2、≈ 0.82。\n\n'
  '## 改造：3 GHz 與 8 GHz\n\n| 頻率 | hf/k_B | 熱激發 < 1% 要低於 | 10 mK 時的波茲曼因子 |\n|---|---|---|---|\n'
  + ''.join(f'| {f} GHz | {t_star(f):.3f} K | {t_star(f) / math.log(100) * 1e3:.0f} mK | {fmt(boltz(f, 0.01))} |\n' for f in (3, 5, 8))
  + '\n頻率越低，一份能量越小，就越怕熱：3 GHz 要比 8 GHz 冷得多才夠。\n\n'
  '## 常見問題\n\n'
  '- 室溫的 0.9992 是「熱激發機率 99.9%」嗎？不是。它是激發態和基態的機率比，接近 1 代表兩邊幾乎一樣多（各約一半）。\n'
  '- 為什麼不是 0 K？做不到；而且 10 mK 時熱激發已經約 4×10⁻¹¹，其他誤差來源遠比它大。\n'
  '- 10 mK 讓電腦變快嗎？不會。它只是讓熱雜訊幾乎不存在，量子位元才能好好待在零。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `animations/transmon-3d.html#readout`（第 5 章 讀取）

- 步驟 1：面板寫「h × 5.21 GHz ≈ 22 μeV（約相當於 0.25 K 的熱能）」——和今天的換算一樣。
- 步驟 7：「稀釋冷凍機全程維持 ~10 mK」；位元等效溫度常為 40–60 mK，靜置時仍有約 0.1–1% 在 |1⟩。

## `animations/peripherals.html#cooldown`（場景 4 降溫流程）

- 按「⏸ 暫停」，拖動「時間 (小時)」滑桿：0 h 每層 300 K；約 24 h 上面幾層降下來；36 h 混合腔約 10.2 mK。
- 右下插圖是對數座標的各級溫度曲線。

## `animations/index.html#fridge`（場景 11 低溫讀取鏈）

- 控制面板寫著 7 GHz 的熱光子數：300 K ≈ 890、10 mK ≈ 10⁻¹⁵。
- 「放大混合腔」可以近看樣品盒。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；左右方向鍵換場景（周邊系統、JJ 頁）或換章（transmon 3D）。
''',
}

SHEET_HEADER = ['頻率 (GHz)', '地方', '溫度 (K)', 'hf/k_B (K)', '比值 hf/kT', '波茲曼因子 exp(−hf/kT)', '夠冷嗎', '計時 (秒)']
SHEET_ROWS = ([['5', n, f'{T:g}'] for n, T in TEMPS]
              + [['5', '加碼', '0.1'], ['5', '加碼', '0.05']]
              + [[str(f), n, f'{T:g}'] for f in (3, 8) for n, T in TEMPS])

EXTRA_CSS = '''table.rec td{height:11mm}.big td{height:13mm;font-size:13pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}
.chk li:before{content:"□ "}.chk{padding-left:2mm}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin:3mm 0}
.steps div{border:1.2pt solid #0b2540;border-radius:2.5mm;padding:2.5mm 3mm;font-size:11.5pt}.steps b{display:block;color:#4a6a88}'''


def html():
    rows = ''.join(f'<tr><td>{n}</td><td>{T:g} K</td><td></td><td></td><td></td></tr>' for n, T in TEMPS)
    timer = ''.join(f'<tr><td>第 {i} 題</td><td>{q}</td><td></td><td></td><td></td></tr>'
                    for i, q in enumerate(['5 GHz → 克耳文', '室溫 300 K', '液氮 77 K', '液氦 4.2 K', '10 mK', '加碼：100 mK'], 1))
    pages = [
        '<h2>溫度換算表：5 GHz 量子位元</h2><p class="lead">先把量子位元的一份能量換成溫度，再和四個地方比一比。</p>'
        '<div class="box"><p>hf ＝ 6.626×10⁻³⁴ × 5×10⁹ ≈ ＿＿＿＿ J　　hf ÷ k_B ＝ ＿＿＿＿ ÷ 1.381×10⁻²³ ≈ ＿＿＿＿ K</p></div>'
        '<div class="steps"><div><b>01 算比值</b>x ＝ hf/kT ＝ 0.24 K ÷ 溫度</div><div><b>02 加負號</b>−x</div><div><b>03 按指數鍵</b>exp(−x)</div></div>'
        '<table class="rec big"><tr><th>地方</th><th>溫度</th><th>比值 x</th><th>exp(−x)</th><th>夠冷嗎？</th></tr>' + rows + '</table>'
        '<p class="note">exp(−x) 接近 1：激發態和基態幾乎一樣多（熱雜訊很多）；接近 0：熱激發幾乎不存在。</p>',
        '<h2>溫度換算競速：計時卡</h2><p class="lead">計算員（孩子）按計算機，裁判（爸爸）計時、核對答案。先估數量級，再按計算機。</p>'
        '<table class="rec"><tr><th>題號</th><th>題目</th><th>先估（數量級）</th><th>答案</th><th>秒數</th></tr>' + timer + '</table>'
        '<div class="box" style="margin-top:5mm"><p>最快的一題：＿＿＿＿　秒　　估錯數量級的一題：＿＿＿＿</p>'
        '<p>我發現的訣竅：</p><div class="line"></div></div>',
        '<h2>換你改造：3 GHz 和 8 GHz 各需要多冷？</h2><p class="lead">頻率不同，一份能量不同，需要的溫度也不同。</p>'
        '<table class="rec big"><tr><th>頻率</th><th>先估 hf/k_B</th><th>算出 hf/k_B</th><th>熱激發 &lt; 1%：÷ 4.6</th><th>10 mK 時 exp(−x)</th></tr>'
        '<tr><td>3 GHz</td><td></td><td></td><td></td><td></td></tr><tr><td>5 GHz</td><td></td><td>0.24 K</td><td></td><td></td></tr>'
        '<tr><td>8 GHz</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p class="note">為什麼除以 4.6？因為 exp(−x) ＜ 0.01 需要 x ＞ ln 100 ≈ 4.6。</p>'
        '<div class="box" style="margin-top:4mm"><p>哪一個頻率最怕熱？為什麼？</p><div class="line"></div><div class="line"></div></div>',
        '<h2>說明卡：為什麼要 10 mK</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 要拿來比的是哪兩種能量？</p><div class="line"></div><p>2. 為什麼室溫、液氮、液氦都不夠冷？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個常見誤解或限制：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出原理：hf 和 k_BT 比一比</li><li>把 5 GHz 換成約 0.24 K</li>'
        '<li>說出 10 mK 時熱激發約 4×10⁻¹¹</li><li>指出誤解：10 mK 不是為了變快，是為了讓熱雜訊幾乎不存在</li>'
        '<li>替換算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q041 為什麼要 10 mK 列印包', '父子科技學院 量子電腦學程 Q041｜為什麼要 10 mK', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q041-why-10mk', folder='Q041_為什麼要10mK', files=FILES,
        sheet=('03_溫度換算表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_溫度換算.pdf', pack_pages=4,
        pack_needles=('溫度換算表', '計時卡', '3 GHz', '8 GHz', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q041', episode_dir='specials/q041-why-10mk',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（計算機；temperature_table.py 只用 Python 標準函式庫，可選）',
               'program': 'temperature_table.py', 'factsFrom': 'production/fact-check.md',
               'keyNumbers': {'5GHz_K': round(t_star(5), 4), 'exp_minus_24': f'{boltz(5, 0.01):.3g}'}})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q041/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

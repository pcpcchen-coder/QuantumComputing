"""Q024 課堂教材：單擺週期紀錄表、角度與計時卡（列印）、能階間距紀錄、說明卡、解答、pendulum_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（pendulum_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/transmon-3d.html#junction、#potential 與 lc-vs-jj.html#s5。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q024/classroom.py
"""
from pathlib import Path
import contextlib
import io
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = '''"""父子科技學院 量子電腦學程 Q024：單擺與約瑟夫森接面的「近似失效」小實驗。

不用安裝任何套件，只要 Python 3。執行：  python pendulum_check.py
一、單擺：大角度的週期比小角度長（維基百科 Pendulum (mechanics)，AGM 公式 T = T0 / M(1, cos(θ0/2))）
二、接面電感：L_J = L_J0 / cos φ = L_J0 / √(1 − (I/Ic)²)（學程簡報 JJ_Microwave_Readout_Talk p14、transmon p4–5）
三、小電流電感 L_J0 = Φ0 / (2π Ic)，Ic = 30 nA 的例子（同上）
"""
from math import sqrt, pi, cos, radians

G = 9.81              # 重力加速度（m/s²）
ROPE = 1.0            # 擺繩（m）
H = 6.62607015e-34    # 普朗克常數（SI 定義值）
E = 1.602176634e-19   # 基本電荷（SI 定義值）


def agm(a, b):
    for _ in range(40):
        a, b = (a + b) / 2, sqrt(a * b)
    return a


T0 = 2 * pi * sqrt(ROPE / G)
print(f'一、單擺（擺繩 {ROPE} m）：小角度週期 T0 = {T0:.3f} 秒')
PEND = {}
for deg in (5, 10, 20, 30, 45, 60, 90):
    PEND[deg] = T0 / agm(1, cos(radians(deg) / 2))
    print(f'  放手角度 {deg:3d} 度  →  週期 {PEND[deg]:.3f} 秒（比小角度多 {(PEND[deg] / T0 - 1) * 100:5.2f} %），十次來回 {10 * PEND[deg]:6.2f} 秒')

print()
print('二、接面電感隨電流變大：L_J / L_J0 = 1 / √(1 − (I/Ic)²)')
LJ = {}
for r in (0.1, 0.3, 0.5, 0.7, 0.87, 0.95, 0.98, 0.99):
    LJ[r] = 1 / sqrt(1 - r * r)
    print(f'  電流 = {r:4.2f} Ic  →  電感 = {LJ[r]:6.2f} 倍')
print('  電流到 Ic：電感變成無限大；超過 Ic，接面跳到有電壓、會耗能的狀態。')

print()
IC = 30e-9
LJ0_NH = H / (2 * E) / (2 * pi * IC) * 1e9
print(f'三、Ic = 30 nA 時，小電流電感 L_J0 = Φ0 / (2π Ic) = {LJ0_NH:.1f} nH')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'pendulum_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白（十度約二十點一秒、六十度約二十一點五秒；一半多一成五、九成八約五倍；約十一奈亨）相同
assert round(10 * R['PEND'][10], 1) == 20.1 and round(10 * R['PEND'][60], 1) == 21.5
assert round(R['PEND'][90] / R['T0'], 2) == 1.18
assert round(R['LJ'][0.5], 2) == 1.15 and round(R['LJ'][0.98]) == 5
assert round(R['LJ0_NH']) == 11

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q024：JJ 是非線性電感（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂看約瑟夫森接面（JJ）在電路裡的角色：它像一個電感，而且電感會隨電流改變（非線性），又沒有電阻損耗（無耗散）。
用單擺的小角度和大角度比一比，體會「近似什麼時候會失效」。上一堂 Q023 是接面的結構與兩個效應；下一堂 Q025 看 E_J 與 E_C 兩個能量尺度。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 接面為什麼像電感、電感隨電流變大、非線性與無耗散；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 做一公尺的單擺，十度和六十度各數十次來回，記下秒數 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：在 transmon-3d 位能井那一章，找出能階間距開始變小的地方 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替紀錄取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 細繩（約 1.2 公尺，綁好後從支點到重物中心量 1 公尺）、重物（螺帽、鎖頭或裝水的小瓶，越小越重越好）、量角器、膠帶、碼錶（手機也可以）、一個穩固的支點（門框、桌邊夾住的尺）。
- 列印 `02_列印包_單擺週期.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `transmon-3d.html#junction` 和 `#potential`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `pendulum_check.py`（不需要安裝套件）。

## 驗收重點

1. 完成單擺週期紀錄：十度、六十度各量兩次以上，算出一次週期，並寫一句比較。
2. 不看稿說出核心原理：接面的電壓和電流變化的快慢成正比，所以像電感；電感 = 小電流電感 ÷ cos φ，電流越接近 Ic 越大。
3. 指出至少一個注意事項：JJ 沒有電阻損耗，是「無耗散」的非線性元件；但電流超過 Ic 就跳到有電壓的狀態、會耗能。

## 誠實說明

- 單擺的計算值（十次來回：10° 約 20.10 秒、60° 約 21.53 秒）是理想單擺；細繩有質量、重物不是一個點、大角度時擺幅會慢慢變小，量到的時間會差一些，重點是「大角度比較慢」。
- 單擺和接面是「近似失效、振盪變軟」的類比，不是一格一格對應：單擺的回復力和 sin θ 成正比，接面的電流和 sin φ 成正比，形狀相同。
- 11 nH、5.21／4.93 GHz、−283 MHz 都是學程簡報和動畫的範例參數，不是某一顆晶片的量測。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：量單擺的週期（約 40 分鐘）

1. 把細繩一端固定在支點，另一端綁重物；從支點量到重物中心剛好 1 公尺。
2. 把量角器貼在支點旁（或用列印包第 2 頁的角度卡），先標出 10 度和 60 度的位置。
3. 爸爸把重物拉到 10 度，繩子拉直、輕輕放手（不要推）。孩子在重物第一次回到最外側時按下碼錶，數十次來回再按停。
4. 換成 60 度，同樣數十次來回。兩個角度都各量兩次，填進列印包第 1 頁。
5. 算一次的週期：十次的時間 ÷ 10。比一比：60 度比 10 度多了幾秒？多了百分之幾？
6. 一起看 `transmon-3d.html#junction`：把相位差滑桿從 0 度拉到 80 度，看「電感 L_J / L_J0」從 1.00 變成 5.76。在紀錄表下面寫一句：「單擺是＿＿變大時變慢，接面是＿＿變大時電感變大。」
7. 拍照記錄。

## 下半場：孩子改造——找出能階間距開始變小的地方（約 30 分鐘）

1. 打開 `transmon-3d.html#potential`（第 3 章位能井）。面板上方第一個按鈕「有 JJ（transmon）」是預設。
2. 把每兩階之間標的間距（GHz）從下往上抄進列印包第 3 頁的表。
3. 按第二個按鈕「沒有 JJ（線性 LC）」，再抄一次；比較兩欄。
4. 回答：間距從哪一格開始變小？線性電路有沒有變小？面板的非諧性讀數各是多少？
5. 最後寫一句「近似在哪裡失效」：單擺、接面、能階各一個。
6. 加分題：跑 `pendulum_check.py`，看 30 度、45 度、90 度的週期，畫一張「角度—週期」的小圖。
''',

'pendulum_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## pendulum_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 單擺週期紀錄參考\n\n'
  '| 放手角度 | 十次來回（計算值） | 一次週期 | 比小角度多 |\n|---|---|---|---|\n'
  f'| 10 度 | 約 {10 * R["PEND"][10]:.2f} 秒 | 約 {R["PEND"][10]:.2f} 秒 | 約 {(R["PEND"][10] / R["T0"] - 1) * 100:.1f} % |\n'
  f'| 60 度 | 約 {10 * R["PEND"][60]:.2f} 秒 | 約 {R["PEND"][60]:.2f} 秒 | 約 {(R["PEND"][60] / R["T0"] - 1) * 100:.1f} % |\n\n'
  '實際量到的會差一些（反應時間、空氣阻力讓大角度的擺幅慢慢變小、繩子有質量），只要看得出「六十度比十度慢約一秒半（十次）」就對了。\n\n'
  '## 能階間距參考（transmon-3d.html#potential）\n\n'
  '| 間距 | 有 JJ（transmon） | 沒有 JJ（線性 LC） |\n|---|---|---|\n'
  '| 0→1 | 5.21 GHz | 5.48 GHz |\n| 1→2 | 4.93 GHz | 5.48 GHz |\n| 2→3 | 4.62 GHz | 5.48 GHz |\n| 3→4 | 4.25 GHz | 5.48 GHz |\n| 4→5 | 3.91 GHz | 5.48 GHz |\n\n'
  '- 從第一格往上就開始變小（5.21 → 4.93），越往上縮得越多；線性電路每一格都一樣。\n'
  '- 面板讀數：有 JJ 時非諧性 α = −283 MHz（4.93 − 5.21 ≈ −0.28 GHz）；沒有 JJ 時「0（等距）」。\n\n'
  '## 暫停題：電流推到超過臨界電流，它還是無耗散的電感嗎？\n\n'
  '- 不是。電流到 Ic 時電感已經變成無限大；超過 Ic，相位差鎖不住，接面兩端出現電壓（上一堂的交流效應），'
  '同時有電阻性的電流，開始耗能（學程簡報 transmon p5「超過後跳到有電壓的耗散態」）。量子位元工作時電流遠小於 Ic，所以是無耗散的。\n\n'
  '## 常見問題\n\n'
  '- 為什麼說它像電感？把 I = Ic sin φ 對時間微分，相位轉動的速度又和電壓成正比，整理後得到 V = L_J · dI/dt，形式和電感一樣，只是 L_J = L_J0 / cos φ。\n'
  '- 它的能量存在哪裡？不是線圈的磁場；維基百科 Josephson effect 說它來自庫柏對的動能，叫動感電感；學程簡報說「能量存在相位耦合裡」。\n'
  '- 二極體也是非線性，為什麼不用？二極體、電晶體會耗能發熱，會破壞量子相干；接面在超導狀態下沒有電阻。\n'
  '- 單擺和接面是同一回事嗎？形狀相同的類比：單擺的位能 −mgl cos θ、接面的位能 −E_J cos φ；小角度（小電流）時都很像直線，大了就「變軟」、變慢。\n'
  '- 電感變大為什麼會變慢？上上堂 Q021：電路的週期跟著電感乘電容的根號變，電感大，振得慢。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#junction`、`#potential`、`#s5` 會直接跳到該處。

## `transmon-3d.html#junction`（第 2 章：約瑟夫森結——非線性電感的本體）

- 下層 Al、中間淡紫色的 AlOx 絕緣層、上層 Al；青色和金色的小球兩顆一組（庫柏對）從下層穿過絕緣層走到上層，電流越大走得越快。
- 右側面板讀數：「相位差 φ」「電流 I / I_c」「電感 L_J / L_J0」。一開始是 35°、0.574、1.22。
- 拖動「φ」滑桿：0° → 0.000、1.00（小球停在原地打轉）；80° → 0.985、5.76；90° 附近顯示「→ ∞」；超過 90° 顯示負電感（本課不展開）。
- 勾選「施加電壓 V ≠ 0」：相位差一直轉，電流變成交流（上一堂的交流效應）。

## `lc-vs-jj.html#s5`（圖解第 5 步：泰勒展開——多出來的四次項）

- 橘色實線 1 − cos φ（真正的接面）、藍色虛線 φ²/2（只留二次項）、灰色點線 φ²/2 − φ⁴/24。
- 中間兩條幾乎重疊；往兩邊橘色變平、比拋物線低，淺橘色陰影標「四次項造成的差距」。

## `transmon-3d.html#potential`（第 3 章：cos 位能井——能階不再等距）

- 銅色餘弦山谷、灰色拋物線、六條能階（最下面兩條金色）、右邊間距標籤；旁邊有一個同形的單擺在擺動。
- 面板上方兩個按鈕：「有 JJ（transmon）」「沒有 JJ（線性 LC）」；讀數有 E₁ − E₀、E₂ − E₁、E₃ − E₂ 與非諧性 α。
- 下方還有「送 π 脈衝」「持續驅動 40 ns」等按鈕，是之後的課（只停在 |0⟩、|1⟩）會用到的。
- 拖曳可以旋轉、滾輪縮放。

## 之後的課

Q025「E_J 與 E_C：兩個能量尺度」會用 `index.html#potential` 與 `transmon-3d.html#potential` 掃描 E_J／E_C。
''',
}

SHEET_HEADER = ['放手角度', '第 1 次十次來回（秒）', '第 2 次十次來回（秒）', '一次週期（秒）', '比十度多（秒）']
SHEET_ROWS = [['10 度'], ['60 度'], ['（加分）30 度'], ['（加分）90 度']]

EXTRA_CSS = '''table.rec td{height:15mm;font-size:10.5pt}table.rec th:first-child{width:30mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:3mm}.cards .cut{font-size:12pt;padding:4mm 3mm;text-align:center}
.cards .cut b{display:block;font-size:15pt;margin-bottom:1mm}
.lv td{height:11mm}'''


def _protractor():
    """一張「角度卡」：從支點往下的 0 度線，左右各標 10 度與 60 度。"""
    import math
    lines = []
    for d, lab in ((0, '0°'), (10, '10°'), (-10, '10°'), (60, '60°'), (-60, '60°')):
        x2 = 100 + 90 * math.sin(math.radians(d))
        y2 = 8 + 90 * math.cos(math.radians(d))
        dash = '' if d == 0 else ' stroke-dasharray="4 3"'
        lines.append(f'<line x1="100" y1="8" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#0b2540" stroke-width="{2 if d == 0 else 1.4}"{dash}/>')
        lines.append(f'<text x="{100 + 98 * math.sin(math.radians(d)):.1f}" y="{8 + 98 * math.cos(math.radians(d)) + 4:.1f}" '
                     f'font-size="9" text-anchor="middle" fill="#0b2540">{lab}</text>')
    return ('<svg width="120mm" height="64mm" viewBox="0 0 200 112"><circle cx="100" cy="8" r="3" fill="#0b2540"/>'
            + ''.join(lines) + '</svg>')


def html():
    pages = [
        '<h2>單擺週期紀錄表</h2><p class="lead">擺繩 1 公尺。每個角度數十次來回，量兩次；一次週期 = 十次的時間 ÷ 10。</p>'
        '<p>紀錄名稱：＿＿＿＿＿＿＿＿＿＿＿＿　量的人：＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>放手角度</th><th>第 1 次（10 次來回）</th><th>第 2 次（10 次來回）</th><th>一次週期</th><th>比十度多</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td><td></td><td></td></tr>' for a in ('10 度', '60 度', '（加分）30 度', '（加分）90 度'))
        + '</table>'
        '<div class="box" style="margin-top:3mm"><p>我發現：角度變大，週期變＿＿＿；就像接面的電流變大，電感變＿＿＿。</p><div class="line"></div>'
        '<p>動畫 #junction：相位差 0 度時電感是＿＿＿倍，80 度時是＿＿＿倍。</p><div class="line"></div></div>',
        '<h2>角度卡與計時卡</h2><p class="lead">角度卡的圓點對準支點、0° 線對準靜止的繩子；把重物拉到虛線再放手。計時卡剪下來輪流用。</p>'
        '<div style="text-align:center">' + _protractor() + '</div>'
        '<div class="cards">'
        '<div class="cut"><b>放手的人</b>繩子拉直、對準虛線<br>輕輕放手，不要推</div>'
        '<div class="cut"><b>計時的人</b>重物到最外側時按下<br>數「零、一、二……十」再按停</div>'
        '<div class="cut"><b>小心</b>重物不要對著人<br>六十度擺得很快，站遠一點</div>'
        '<div class="cut"><b>記錄</b>每個角度量兩次<br>差太多（超過半秒）就再量一次</div></div>',
        '<h2>能階間距紀錄</h2><p class="lead">transmon-3d.html#potential：把每兩階之間的間距從下往上抄下來，再按第二個按鈕比一比。</p>'
        '<table class="lv"><tr><th>間距</th><th>有 JJ（transmon）GHz</th><th>沒有 JJ（線性 LC）GHz</th><th>有沒有變小？</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td><td></td></tr>' for a in ('0→1', '1→2', '2→3', '3→4', '4→5')) + '</table>'
        '<div class="box" style="margin-top:4mm"><p>間距從哪一格開始變小？＿＿＿＿＿＿　面板的非諧性：有 JJ ＿＿＿＿，沒有 JJ ＿＿＿＿</p>'
        '<h3>近似在哪裡失效？</h3><p>單擺：</p><div class="line"></div><p>接面：</p><div class="line"></div><p>能階：</p><div class="line"></div></div>',
        '<h2>說明卡：我的單擺週期紀錄</h2><div class="box"><p>紀錄名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. JJ 是非線性電感在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（單擺怎麼量、動畫怎麼找）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出為什麼接面像電感</li><li>說出電感怎麼隨電流變：越接近 Ic 越大</li>'
        '<li>說出非線性的意思：反應會隨大小改變</li><li>說出能階間距從哪裡開始變小</li>'
        '<li>指出一個注意事項：無耗散，但超過 Ic 會耗能</li><li>替紀錄取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q024 單擺週期 列印包', '父子科技學院 量子電腦學程 Q024｜JJ 是非線性電感', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q024-jj-nonlinear-inductor', folder='Q024_JJ是非線性電感', files=FILES,
        sheet=('03_單擺週期紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_單擺週期.pdf', pack_pages=4,
        pack_needles=('單擺週期紀錄表', '角度卡', '能階間距紀錄', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q024', episode_dir='specials/q024-jj-nonlinear-inductor',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（pendulum_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'pendulum_check.py',
               'recordedRun': {'T0_s_1m': round(R['T0'], 3),
                               'ten_swings_s': {d: round(10 * R['PEND'][d], 2) for d in (10, 60, 90)},
                               'LJ_ratio': {str(r): round(R['LJ'][r], 2) for r in (0.5, 0.87, 0.98)},
                               'LJ0_nH_at_30nA': round(R['LJ0_NH'], 2)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q024/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

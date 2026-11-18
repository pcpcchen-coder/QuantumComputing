"""Q020 課堂教材：繩圈與相位時鐘貼紙紀錄、環形相位圖（列印）、Φ₀ 計算卡、說明卡、解答、flux_scale.py、動畫導覽。

不需要帳號，也不需要安裝套件（flux_scale.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#squid 與 #jj。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q020/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q020：磁通量子 Φ₀ = h/2e 有多小？——算數值、換算地磁場的面積、檢查相位時鐘貼紙。

不用安裝任何套件，只要 Python 3。執行：  python flux_scale.py
普朗克常數 h 與基本電荷 e 是國際單位制從 2019 年起的定義值；Φ₀ = h/(2e)（維基百科 Magnetic flux quantum、學程簡報 p9）。
地磁場約 30–60 μT（維基百科 Earth's magnetic field），本程式以 50 μT 為代表值。
"""
H = 6.62607015e-34    # 普朗克常數（J·s）
E = 1.602176634e-19   # 基本電荷（C）

PHI0 = H / (2 * E)    # 超導的磁通量子（Wb）
PHI_E = H / E         # 如果載流子是單顆電子，一格會是這麼大（Wb）
print(f'磁通量子 Φ₀ = h / 2e ≈ {PHI0:.4e} Wb')
print(f'如果是單顆電子 h / e ≈ {PHI_E:.4e} Wb（是 Φ₀ 的 {PHI_E / PHI0:.0f} 倍）')

print()
print('地磁場垂直穿過一個圈，要剛好裝進一格 Φ₀，圈要多大？（面積 = Φ₀ ÷ 磁場）')
AREAS = {}
for b_ut in (30, 50, 60):
    area = PHI0 / (b_ut * 1e-6)          # 平方公尺
    um2 = area * 1e12                    # 平方微米
    side = area ** 0.5 * 1e6             # 正方形每一邊（微米）
    AREAS[b_ut] = (um2, side)
    print(f'  {b_ut} μT：面積 ≈ {um2:5.1f} μm²，正方形每一邊 ≈ {side:4.2f} μm')
PER_MM = 1000 / AREAS[50][1]
print(f'一毫米（1000 μm）裡排得下約 {PER_MM:.0f} 個每邊 {AREAS[50][1]:.1f} μm 的小正方形')

print()
print('繩圈上 8 張相位時鐘貼紙：每張多轉幾度，回到起點時一共轉了幾圈？')
TURNS = {}
for step in (45, 22.5, 90, 30):
    total = 8 * step
    TURNS[step] = total / 360
    ok = '可以（整數圈）' if total % 360 == 0 else '不行（接不起來）'
    print(f'  每張 {step:5.1f}°：一共 {total:5.1f}° = {total / 360:.2f} 圈 → {ok}')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'flux_scale.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與簡報 p9（2.068 × 10⁻¹⁵ Wb）、旁白（約 41 μm²、每邊 6.4 μm、一毫米約 150 多個、45° 一整圈、22.5° 半圈）相同
assert round(R['PHI0'] * 1e18) == 2068 and round(R['PHI_E'] / R['PHI0']) == 2
assert round(R['AREAS'][50][0]) == 41 and round(R['AREAS'][50][1], 1) == 6.4 and 150 <= R['PER_MM'] < 160
assert R['TURNS'][45] == 1 and R['TURNS'][22.5] == 0.5

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q020：磁通量子化 Φ₀ = h/2e（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。上一堂說到超導體裡的電子兩兩成對，所有電子對進入同一個量子狀態，整塊超導體只要一個相位描述。
這一堂把超導體彎成環：沿著環繞一圈，相位必須回到原點，所以環裡的磁通只能是磁通量子 Φ₀ 的整數倍；而 Φ₀ = h/2e 的那個「2e」，就是電子成對的證據。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 磁通、相位像時鐘指針、磁通一格一格、Φ₀ = h/2e、為什麼是 2e；看動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 父子共同實作：用繩圈與相位時鐘貼紙，示範繞一圈相位必須回到原點 | 列印包第 1 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：用計算機算出 Φ₀，換算地磁場穿過多大的面積；畫環形相位圖 | 列印包第 2、3 頁 |
| 105–115 | 孩子教爸爸：相位為什麼要回到原點、磁通為什麼一格一格、分母為什麼是 2e | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替環形相位圖取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 一條約 2 公尺的繩子（毛線、跳繩都可以）、時鐘貼紙 8 張以上（沒有的話用圓形貼紙自己畫指針）、計算機（手機的也可以）。
- 列印 `02_列印包_環形相位圖.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#squid` 和 `index.html#jj`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `flux_scale.py`（不需要安裝套件），對照孩子用計算機算的答案。

## 解鎖成就（好玩機制）

每完成一項，在說明卡上蓋章或打勾：① 相位回到原點（繩圈接得起來）② 找到接不起來的角度 ③ 算出 Φ₀ ④ 算出地磁場的面積 ⑤ 畫完環形相位圖 ⑥ 教會爸爸分母為什麼是 2e。

## 驗收重點

1. 說得出：整塊超導體共用一個相位，沿著環繞一圈回到同一點，相位必須對上，只能轉整數圈。
2. 說得出：所以環裡的磁通只能是 Φ₀ 的整數倍（0、1、2、3……格）。
3. 指出容易錯的地方：分母是 2e 而不是 e——如果載流子是單顆電子，一格會是 h/e，大一倍；實驗量到 h/2e，證明載流子是帶 2e 的 Cooper pair。

## 誠實說明

- 「相位像時鐘指針」「磁通像樓梯」都是簡化圖像。嚴格說量子化的是磁通加上環流造成的修正（fluxoid）；環夠粗、繞行路徑上沒有電流時，它才剛好等於環內的磁通。
- 「磁場不剛好，環會流出電流補成整數格」也是簡化說法：環變成超導時把磁通凍結成整數格，之後外面的磁場再變，環流會讓環內的磁通維持不變。
- 地磁場依地點約 30–60 μT，本課用 50 μT 當代表值；面積答案會依地點在約 34–69 μm² 之間。
- 動畫 `index.html#squid` 的環夾了兩個約瑟夫森接面，外加磁通可以連續調；畫面呈現的是「每隔一個 Φ₀ 就重複」的反應，不是一格一格跳動的磁通。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：繩圈與相位時鐘貼紙（約 40 分鐘）

1. 做超導環：繩子在桌上或地上圍成一個圓圈，頭尾接起來。在接頭處做記號，當作「起點」。
2. 貼 8 張時鐘貼紙：沿著繩圈等距離貼（大約每 1/8 圈一張），第 1 張就貼在起點。每張貼紙只畫一根指針，代表那個位置的相位。
3. 第一次：每張比前一張多轉 45°（第 1 張指 12 點，第 2 張指 1 點半，第 3 張指 3 點……）。走完 8 張再回到起點，指針剛好轉了 360°，和第 1 張對得上——相位回到原點，這是允許的狀態（解鎖成就①）。
4. 第二次：每張只多轉 22.5°。走回起點時只轉了 180°，指針指 6 點，和第 1 張的 12 點接不起來——同一個地方不能有兩個相位，這是超導環不允許的狀態（解鎖成就②）。
5. 再試 90°、30°：8 × 90° = 720°（兩圈，可以）；8 × 30° = 240°（不行）。在列印包第 1 頁記錄每次的角度、總共轉幾圈、接不接得起來。
6. 連到磁通：指針繞一圈多轉一整圈，就代表環裡多了一格磁通 Φ₀。所以 0 圈 ↔ 0 格、1 圈 ↔ 1 格、2 圈 ↔ 2 格；半圈不行，所以半格也不行。
7. 最後一起說一次注意事項：一格的大小是 h/2e，分母是 2e 而不是 e。

## 下半場：孩子改造——算出 Φ₀ 與面積（約 30 分鐘）

1. 用列印包第 3 頁的計算卡：Φ₀ = h ÷ (2 × e)，h = 6.626 × 10⁻³⁴ J·s、e = 1.602 × 10⁻¹⁹ C。計算機上的「×10 的次方」鍵通常寫成 EXP 或 EE（解鎖成就③）。
2. 再算一次 h ÷ e（如果載流子是單顆電子），比一比是 Φ₀ 的幾倍。
3. 面積 = Φ₀ ÷ 地磁場。地磁場用 50 μT = 50 × 10⁻⁶ T。算出的單位是平方公尺，乘上 10¹² 換成平方微米（解鎖成就④）。
4. 開根號得到正方形每一邊幾微米；一毫米（1000 μm）裡排得下幾個？
5. 用列印包第 2 頁畫環形相位圖：畫一個圓、8 個位置、每個位置的指針；旁邊寫上「繞一圈轉了幾圈 = 磁通幾格」（解鎖成就⑤）。替它取名字，拿去考爸爸。
''',

'flux_scale.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 相位為什麼要回到原點\n\n'
  '- 整塊超導體的電子對共用一個量子狀態，只要一個相位描述；同一個位置只能有一個相位。\n'
  '- 沿著環走一圈回到同一點，相位必須對上，所以一圈下來的相位變化只能是 0、360°、720°……（2π 的整數倍）。\n'
  '- 穿過環的磁通每多一個 Φ₀，相位繞一圈就多轉一整圈；所以環裡的磁通只能是 Φ₀ 的整數倍。\n\n'
  '## 貼紙角度參考答案（8 張）\n\n'
  '| 每張多轉 | 一共 | 幾圈 | 接得起來嗎 |\n|---|---|---|---|\n'
  '| 45° | 360° | 1 | 可以（1 格磁通） |\n| 22.5° | 180° | 0.5 | 不行 |\n'
  '| 90° | 720° | 2 | 可以（2 格磁通） |\n| 30° | 240° | 0.67 | 不行 |\n\n'
  '## flux_scale.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 暫停題：一毫米裡排得下幾個每邊 6.4 μm 的小正方形？\n\n'
  '- 1000 ÷ 6.43 ≈ 155，大約一百五十多個。\n\n'
  '## 常見問題\n\n'
  '- 普通銅線圈的磁通也一格一格嗎？不會。銅線裡的電子沒有共用一個相位，磁通可以是任何大小。\n'
  '- 為什麼分母是 2e？在環裡繞圈、帶著那個共同相位的是 Cooper pair，每對帶 2e。如果是單顆電子，一格會是 h/e，大一倍；1961 年的實驗量到 h/2e。\n'
  '- Φ₀ 跟材料有關嗎？無關。h 和 e 都是基本常數，任何超導體的 Φ₀ 都一樣。\n'
  '- 動畫裡的磁通滑桿為什麼可以停在 0.25？那個環夾了兩個約瑟夫森接面，外加磁通可以連續調；環的反應（右下小圖、環流光點）每隔一個 Φ₀ 重複一次。\n'
  '- 真實的量子電腦哪裡會用到？超導量子干涉元件（SQUID）用磁通調整量子位元頻率，調頻的週期就是一個 Φ₀（學程簡報 p9）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。網址後面的 `#` 名稱可以直接跳到場景。

## `index.html#jj`（JJ 與微波讀取 場景 3：約瑟夫森接面）——只看相位鐘

- 上方兩個圓圈是「相位鐘」：左邊藍色代表左邊那塊鋁的相位、右邊紅色代表右邊那塊鋁的相位，兩根指針一直一起轉。
- 上方中間金色的字寫著兩個相位的差（一開始 30°）。把「偏壓電流」滑桿拉到 0，相位差很快變成 0°，中間的電子對不再往右流。
- 約瑟夫森接面是之後幾堂的主角，今天只借用「相位鐘」的畫法。

## `index.html#squid`（JJ 與微波讀取 場景 6：DC SQUID）

- 銀色大圓環是超導鋁環，左右兩個橘色小方塊是約瑟夫森接面。青色箭頭代表穿過環的磁通，環中央的字顯示「Φ = … Φ₀」。
- 「外加磁通 Φ / Φ₀」滑桿：拉到 0，箭頭消失、沿著環轉的小光點（環流）也消失；拉到 0.25，箭頭和光點出現。
- 右下小圖的橫軸是 Φ / Φ₀，青色點標目前位置：0 在最高、0.5 掉到最低、1 又回到最高——每隔一個 Φ₀ 重複一次。
- 這個環夾了接面，所以外加磁通可以連續調，不是一格一格跳；畫面上看到的是「以 Φ₀ 為週期」的反應。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；← → 切換場景。
''',
}

SHEET_HEADER = ['回合', '每張多轉幾度', '8 張一共幾度', '一共幾圈', '和起點接得起來嗎', '對應磁通幾格', '誰轉的指針', '看到什麼']
SHEET_ROWS = [['第 1 回（45°）'], ['第 2 回（22.5°）'], ['第 3 回（90°）'], ['第 4 回（30°）'], ['第 5 回（自己選）']]

EXTRA_CSS = '''table.rec td{height:20mm;font-size:10.5pt}table.rec th:first-child{width:30mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.demo td{font-size:10.5pt;height:auto}table.demo th:first-child{width:40mm}
.ring{height:150mm;display:flex;align-items:center;justify-content:center}
.ring div{width:120mm;height:120mm;border:2px dashed #888;border-radius:50%}'''


def html():
    rounds = ['第 1 回（45°）', '第 2 回（22.5°）', '第 3 回（90°）', '第 4 回（30°）', '第 5 回（自己選）']
    pages = [
        '<h2>繩圈與相位時鐘貼紙：觀察紀錄</h2><p class="lead">繩子圍成圈，等距離貼 8 張貼紙；每張比前一張多轉同樣的角度，走回起點看接不接得起來。</p>'
        '<p>日期：＿＿＿＿＿＿　參加的人：＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>回合</th><th>8 張一共幾度？幾圈？</th><th>和起點接得起來嗎？</th><th>對應磁通幾格</th></tr>'
        + ''.join(f'<tr><td>{r}</td><td></td><td></td><td></td></tr>' for r in rounds) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>為什麼同一個地方不能有兩個相位？</p><div class="line"></div>'
        '<p>注意事項：一格的大小是 h/2e，分母是 2e 而不是 e。</p></div>',
        '<h2>環形相位圖</h2><p class="lead">在圓上畫 8 個位置和每個位置的指針；旁邊寫「繞一圈轉了幾圈＝磁通幾格」。</p>'
        '<p>相位圖名稱：＿＿＿＿＿＿＿＿＿＿＿＿　畫的人：＿＿＿＿＿＿</p>'
        '<div class="ring"><div></div></div>'
        '<div class="box"><p>繞一圈轉了＿＿＿圈　→　環裡的磁通是＿＿＿格 Φ₀</p></div>',
        '<h2>Φ₀ 計算卡</h2><p class="lead">拿出計算機：一格磁通量子有多小？地磁場要穿過多大的圈才裝得下一格？</p>'
        '<table class="demo"><tr><th>要算的</th><th>算式</th><th>我的答案</th></tr>'
        '<tr><td>磁通量子 Φ₀</td><td>6.626 × 10⁻³⁴ ÷ (2 × 1.602 × 10⁻¹⁹)</td><td>＿＿＿＿ Wb</td></tr>'
        '<tr><td>如果是單顆電子</td><td>6.626 × 10⁻³⁴ ÷ 1.602 × 10⁻¹⁹</td><td>＿＿＿＿ Wb（是 Φ₀ 的＿倍）</td></tr>'
        '<tr><td>面積（地磁場 50 μT）</td><td>Φ₀ ÷ (50 × 10⁻⁶)</td><td>＿＿＿＿ m² ＝ ＿＿＿＿ μm²</td></tr>'
        '<tr><td>正方形每一邊</td><td>面積開根號</td><td>＿＿＿＿ μm</td></tr>'
        '<tr><td>一毫米排得下幾個</td><td>1000 ÷ 每一邊</td><td>＿＿＿＿ 個</td></tr></table>'
        '<div class="box" style="margin-top:4mm"><h3>單位換算小抄</h3>'
        '<p>1 Wb = 1 T 垂直穿過 1 m²　　1 μT = 10⁻⁶ T　　1 m² = 10¹² μm²　　1 mm = 1000 μm</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>相位回到原點的三步</h3>'
        '<p>① 整塊超導體共用一個相位　② 繞環一圈回到起點，指針必須對上　③ 只能轉整數圈 → 磁通只能是 Φ₀ 的整數倍</p></div>',
        '<h2>說明卡：我的環形相位圖</h2><div class="box"><p>相位圖名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 磁通量子化在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（繩圈、貼紙、計算）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：解鎖成就</h3><ul class="chk">'
        '<li>繩圈接得起來：相位回到原點</li><li>找到接不起來的角度</li>'
        '<li>算出 Φ₀ ≈ 2.07 × 10⁻¹⁵ Wb</li><li>算出地磁場要穿過多大的面積</li>'
        '<li>指出容易錯的地方：分母是 2e，不是 e</li><li>替環形相位圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q020 環形相位圖 列印包', '父子科技學院 量子電腦學程 Q020｜磁通量子化 Φ₀ = h/2e', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q020-flux-quantization', folder='Q020_磁通量子化', files=FILES,
        sheet=('03_相位時鐘貼紙紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_環形相位圖.pdf', pack_pages=4,
        pack_needles=('繩圈與相位時鐘貼紙', '環形相位圖', 'Φ₀ 計算卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q020', episode_dir='specials/q020-flux-quantization',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（flux_scale.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'flux_scale.py',
               'recordedRun': {'phi0_Wb': float(f"{R['PHI0']:.6e}"), 'h_over_e_ratio': round(R['PHI_E'] / R['PHI0']),
                               'area_um2': {str(b): round(a, 1) for b, (a, _) in R['AREAS'].items()},
                               'side_um_50uT': round(R['AREAS'][50][1], 2), 'per_mm': round(R['PER_MM']),
                               'sticker_turns': {str(k): round(v, 3) for k, v in R['TURNS'].items()}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q020/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

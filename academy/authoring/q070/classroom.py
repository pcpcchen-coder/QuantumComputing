"""Q070 課堂教材：成就清單（atoms.html#ms 執行閘、改失諧、停在半圈）、成就紀錄表、莫索閘說明圖底稿、隱藏成就觀察表、
只用 Python 內建功能的相空間迴圈計算 ms_gate.py、解說卡與解答。

不需要帳號，也不需要安裝任何套件（ms_gate.py 只用 Python 標準函式庫；動畫用瀏覽器開啟）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q070/classroom.py
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

# 製作代理以 python 3 實跑 ms_gate.py（K = 1、失諧 10 kHz）的結果：停止比例 → (時間 μs, |α|, P(11))
HALF_P11 = round(math.sin(math.pi / 8) ** 2, 3)
assert HALF_P11 == 0.146
STOPS = {0.25: (25, 0.354, 0.005), 0.5: (50, 0.500, 0.146), 0.75: (75, 0.354, 0.429), 1.0: (100, 0.000, 0.500)}
GATE_US = {5: 200, 10: 100, 20: 50, 50: 20}
assert all(abs(1000 / k - v) < 1e-9 for k, v in GATE_US.items())

PROGRAM = '''"""父子科技學院 量子電腦學程 Q070：莫爾默與索倫森閘的相空間迴圈（只用 Python 內建功能，不需要安裝任何套件）

執行：python ms_gate.py
模型（和動畫 atoms.html#ms 相同）：
  振動在相空間的位置 α(t) = A·(e^{iδt} − 1)，畫一個半徑 A 的圓，t = 2πK/δ 時回到原點
  幾何相位 Φ(t) = A²·(δt − sin δt)；A = 1/(4√K)，讓繞完 K 圈時 2Φ = π/4
  從 |00⟩ 出發：P(00) = cos²(2Φ)，P(11) = sin²(2Φ)
"""
import cmath
import math

K = 1                       # 改造區：繞幾圈（1 或 2）
FK = 10                     # 改造區：失諧 δ/2π，單位 kHz
A = 1 / (4 * math.sqrt(K))


def state(frac):
    """閘進行到 frac（0～1）時的位移、相位和機率。"""
    s = 2 * math.pi * K * frac
    alpha = A * (cmath.exp(1j * s) - 1)
    phi = A * A * (s - math.sin(s))
    return abs(alpha), 2 * phi / math.pi, math.cos(2 * phi) ** 2, math.sin(2 * phi) ** 2


print(f'失諧 {FK} kHz，繞 {K} 圈 → 閘時間 = {1000 * K / FK:.0f} μs')
for frac in (0, 0.25, 0.5, 0.75, 1.0):
    a, ph, p00, p11 = state(frac)
    note = '迴圈閉合' if a < 1e-9 and frac > 0 else ('還沒開始' if frac == 0 else '迴圈未閉合：自旋和振動仍糾纏')
    print(f'停在 {frac:4.0%}（{1000 * K * frac / FK:5.1f} μs）：|α| = {a:.3f}，2Φ = {ph:.3f}π，'
          f'P(00) = {p00:.3f}，P(11) = {p11:.3f}　{note}')
for fk in (5, 10, 20, 50):
    print(f'失諧 {fk:2d} kHz → 閘時間 {1000 * K / fk:.0f} μs')
'''

ACHIEVEMENTS = [
    ('第一枚', '看見推力', '按「▶ 執行閘」，看左邊離子上下出現紅影、藍影', '紅影、藍影各代表什麼？為什麼往相反方向？'),
    ('第二枚', '畫出一圈', '看右邊相空間：紅、藍兩條軌跡各畫一個圓再回到原點', '為什麼紅、藍兩圈方向相反？「S_x = 0 不動」是哪些分量？'),
    ('第三枚', '拿到糾纏', '閘完成時讀數：時間 100 μs，P(00) = P(11) = 0.5', '閘在幾微秒完成？那時 P(11) 是多少？'),
    ('第四枚', '調快調慢', '把「失諧」拉到 20 kHz、5 kHz，看閘時間', '失諧加倍，閘時間變幾倍？'),
    ('隱藏成就', '迴圈沒閉合', '「停止時刻」拉到 50% 再按執行閘', 'P(11) 是多少？紅影藍影還在嗎？這代表什麼錯誤？'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q070：Mølmer–Sørensen 閘（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的問題：兩顆離子的自旋幾乎不直接互相影響，要怎麼讓它們糾纏？
答案是「莫爾默與索倫森閘」（簡稱莫索閘、MS 閘）：雙色雷射產生自旋相依力，推著兩顆離子共享的振動在相空間繞一圈；圈閉合時振動回到原狀，只留下糾纏。
今天的好玩機制是「解鎖成就」：孩子在互動動畫 `animations/atoms.html#ms` 一枚一枚解鎖成就，爸爸當成就官，說得出為什麼才畫上徽章，最後完成「MS 閘說明圖」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 雙色雷射、自旋相依力、相空間迴圈、幾何相位 | 影片第 3–8 段、列印包第 2 頁 |
| 25–65 | 解鎖第一～四枚成就：執行閘、記下閘完成時間與 P(11)、改失諧；畫說明圖 | `01_成就清單.md`、列印包第 1–2 頁、`03_成就紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 隱藏成就：停止時刻 50%，觀察迴圈沒閉合；（選用）執行 `ms_gate.py` 比較 25%、50%、75% | 列印包第 3 頁、`ms_gate.py` |
| 105–115 | 孩子教爸爸：原理、結果、錯誤 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替說明圖命名、存檔 | |

## 課前準備（約 15 分鐘）

- 電腦或平板的瀏覽器能開 `animations/atoms.html#ms`（下載學程 repo 後直接開檔即可，不需要網路或帳號）。先自己按一次「▶ 執行閘」。
- 列印 `02_列印包_莫索閘.pdf`（A4，共 4 頁）；準備紅、藍、黃三色筆畫說明圖。
- 讀一遍 `04_解答.md`，成就官檢查題的答案都在裡面。

## 誠實說明

- 動畫的數字是代表值：失諧預設 10 kHz、閘時間 = 1 ÷ 失諧；圈的大小已調成「繞完剛好得到最大糾纏」，不是某一台機器的實測。
- 動畫裡的「失諧」滑桿只改閘時間，迴圈總會在閘時間閉合；「迴圈沒閉合」要用「停止時刻」滑桿模擬。真實機器上，失諧和脈衝時間沒配好就會這樣。
- 1600×900 以下的螢幕，左邊面板要往下捲動才看得到讀數、按鈕和滑桿；也可以按 `H` 隱藏面板看全畫面。
- 「停止時刻」滑桿只能讓已經跑完的閘往回停；要停在更晚的位置，先把滑桿拉好，再按一次「▶ 執行閘」。
- 「自旋是正的／負的分量」指沿雷射選定方向（σx）的狀態，不是 |0⟩、|1⟩；從 |00⟩ 出發，四種組合各占一份。
- 對溫度不敏感只在離子振動夠小（Lamb–Dicke 區）時成立，實務上多半仍先把離子冷到很低。
''',

'01_成就清單.md': '# 成就清單（成就官：爸爸；操作員：孩子）\n\n'
  '開 `animations/atoms.html#ms`（場景 5「Mølmer–Sørensen 閘」）。每一枚成就：\n'
  '1. 操作員照「怎麼解鎖」操作，看畫面變化，填進列印包第 1 頁。\n'
  '2. 操作員回答成就官的檢查題；說得出為什麼，成就官才畫上徽章。\n'
  '3. 把這一步畫進說明圖（列印包第 2 頁）。\n\n'
  '| 成就 | 名稱 | 怎麼解鎖 | 成就官檢查題 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in ACHIEVEMENTS)
  + '\n## 下半場：隱藏成就（約 30 分鐘）\n\n'
  '1. 把「停止時刻」依序設成 25%、50%、75%，每次都按一次「▶ 執行閘」，記下時間、P(00)、P(11)。\n'
  '2. 看相空間：點停在哪裡？離原點多遠？左邊的紅影、藍影還在嗎？\n'
  '3. 把「停止時刻」拉回 100% 再執行，比較閉合與沒閉合的讀數。\n'
  '4. 加碼：打開「顯示 2 個迴圈（K=2）」，停在 50% 時迴圈有閉合嗎？P(11) 是多少？為什麼還不是 0.5？\n'
  '5. （選用）在電腦上執行 `python ms_gate.py`，把 K 改成 2 再跑一次，和動畫比較。\n',

'ms_gate.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 成就官檢查題\n\n'
  '- 第一枚：紅影是沿雷射選定方向自旋為 +1 的分量，藍影是 −1 的分量；雙色雷射產生自旋相依力，力的方向由自旋決定，所以往相反方向推。\n'
  '- 第二枚：兩顆自旋都是 +1（S_x = +2）和都是 −1（S_x = −2）的分量，推力方向相反，所以繞的方向相反；一顆 +1、一顆 −1（S_x = 0）的推力抵消，不動。\n'
  '- 第三枚：失諧 10 kHz 時閘在 100 μs 完成；P(00) = P(11) = 0.5，得到最大糾纏的貝爾態 (|00⟩ − i|11⟩)/√2。\n'
  '- 第四枚：閘時間 = 1 ÷ 失諧。' + '、'.join(f'{k} kHz → {v} μs' for k, v in GATE_US.items()) + '；失諧加倍，閘時間減半。\n'
  f'- 隱藏成就：停在 50% 時 P(11) = sin²(π/8) ≈ {HALF_P11}，振動停在離原點最遠的地方，紅影藍影還在：自旋和振動仍糾纏，閘出錯。\n\n'
  '## ms_gate.py 的輸出（製作代理實跑，K = 1、10 kHz）\n\n| 停止時刻 | 時間 | 離原點 \\|α\\| | P(11) |\n|---|---|---|---|\n'
  + ''.join(f'| {int(f * 100)}% | {t} μs | {a:.3f} | {p:.3f} |\n' for f, (t, a, p) in STOPS.items())
  + '\nK = 2（兩個小圈）時，停在 50% 剛好繞完第一圈，迴圈閉合但 P(11) 只有 0.146；要繞完兩圈（100%）才到 0.5。閉合是必要條件，相位也要累積夠。\n\n'
  '## 常見錯誤與誤解\n\n- 「迴圈沒閉合也沒關係，P(11) 有數字就好」——錯。沒閉合時自旋和振動仍糾纏，兩顆離子得不到乾淨的貝爾態，閘出錯。\n'
  '- 「離子一定要冷到完全不動才能做莫索閘」——不必；幾何相位只看圓的面積，和一開始的振動無關（限振動夠小的 Lamb–Dicke 區）。\n'
  '- 「失諧越大越好，閘越快」——失諧加大閘變快，但要讓相位剛好，雷射強度也得跟著加大。\n',

'05_動畫導覽.md': '''# 動畫導覽：atoms.html#ms（離子阱與中性原子 場景 5「Mølmer–Sørensen 閘」）

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

- 左半：兩顆金色離子（「離子 1　離子 2」）與兩道雷射「ω₀ + (ω_m + δ)」「ω₀ − (ω_m + δ)」；執行時離子上下出現紅影、藍影。
- 右半：「振動模態的相空間」，橫軸「位置 x」、縱軸「動量 p」；紅色軌跡「S_x = +2」、藍色「S_x = −2」，原點旁「S_x = 0 不動」。
- 右下：「布居數與運動位移 vs 時間」：藍 P(00)、紅 P(11)、虛線 |α|（運動位移）、黃色直線是目前時間。
- 左邊面板：讀數（時間、閘時間、P(00)、P(11)、幾何相位、迴圈是否閉合）、「▶ 執行閘」、「失諧 δ/2π (kHz)」滑桿（5–50）、「停止時刻（迴圈比例）」滑桿、「顯示 2 個迴圈（K=2）」開關。
- 操作：`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；左右方向鍵換場景（上一堂用場景 4「離子鏈集體振動」）。
''',
}

SHEET_HEADER = ['成就', '名稱', '操作', '畫面上看到', '時間 (μs)', 'P(11)', '說得出為什麼（✓）', '徽章（✓）']
SHEET_ROWS = ([[a, b, c] for a, b, c, _ in ACHIEVEMENTS]
              + [['改造', f'停止時刻 {s}%', '停止時刻滑桿＋執行閘'] for s in (25, 50, 75)])

EXTRA_CSS = '''table.rec td{height:13mm}table.rec{font-size:11pt}table.qt td{height:10mm}
.chk li{margin:2.4mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.draw{border:1pt dashed #7f9bb3;border-radius:3mm;height:150mm;margin-top:3mm;position:relative}
.draw span{position:absolute;font-size:10pt;color:#4a6a88}'''


def html():
    rows1 = ''.join(f'<tr><td>{a}<br>{b}</td><td></td><td></td><td></td></tr>' for a, b, *_ in ACHIEVEMENTS[:4])
    rows3 = ''.join(f'<tr><td>{s}%</td><td></td><td></td><td></td><td></td></tr>' for s in (25, 50, 75, 100))
    pages = [
        '<h2>成就紀錄：四枚成就</h2><p class="lead">你是操作員，爸爸是成就官。每一枚都要說得出為什麼，成就官才畫上徽章。</p>'
        '<table class="rec"><tr><th>成就</th><th>畫面上看到什麼</th><th>讀數（時間、P(11)）</th><th>徽章</th></tr>'
        + rows1 + '</table>'
        '<div class="box" style="margin-top:4mm"><p>閘在＿＿＿＿ μs 完成，那時 P(00) ＝＿＿＿＿，P(11) ＝＿＿＿＿。</p>'
        '<p>失諧 20 kHz 時閘時間＿＿＿＿ μs；5 kHz 時＿＿＿＿ μs。我發現：閘時間 ＝ 1 ÷ ＿＿＿＿＿＿</p></div>'
        '<p class="note">讀數在左邊面板下方，往下捲動或按 H 切換面板。</p>',
        '<h2>莫索閘說明圖底稿：今天的作品</h2><p class="lead">左邊畫兩顆離子和兩道雷射，右邊畫相空間的紅藍兩圈，最下面寫出最後的糾纏態。</p>'
        '<div class="draw"><span style="left:3mm;top:2mm">兩道雷射：ω₀ ＋ (ω_m ＋ δ)、ω₀ − (ω_m ＋ δ)；δ 叫做＿＿＿＿</span>'
        '<span style="right:3mm;top:12mm">相空間：橫軸＿＿＿＿、縱軸＿＿＿＿</span>'
        '<span style="right:3mm;top:60mm">紅圈 S_x = +2、藍圈 S_x = −2、S_x = 0 ＿＿＿＿</span>'
        '<span style="left:3mm;bottom:3mm">閉合後：|00⟩ → ＿＿＿＿＿＿＿＿＿＿＿＿</span></div>'
        '<p style="margin-top:3mm">作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>',
        '<h2>隱藏成就觀察表：迴圈沒閉合</h2><p class="lead">把「停止時刻」設好，再按「▶ 執行閘」。點停在哪裡？還糾纏嗎？</p>'
        '<table class="rec qt"><tr><th>停止時刻</th><th>時間 (μs)</th><th>P(11)</th><th>點離原點遠嗎</th><th>紅影藍影還在嗎</th></tr>' + rows3 + '</table>'
        '<div class="box" style="margin-top:4mm"><p>停在 50% 時，P(11) ＝＿＿＿＿，比 0.5 少，因為＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>迴圈沒閉合時，自旋和＿＿＿＿還糾纏在一起，所以＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>加碼：打開兩個迴圈（K=2）、停在 50%，迴圈閉合了嗎？P(11) ＝＿＿＿＿</p></div>',
        '<h2>解說卡：我的莫索閘說明圖</h2><div class="box"><p>1. 雙色雷射怎麼產生自旋相依力？</p><div class="line"></div>'
        '<p>2. 振動繞完一圈之後，留下了什麼？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個錯誤或限制：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一枚成就：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：兩道頻率 ω₀ ± (ω_m + δ) 的雷射產生自旋相依力</li>'
        '<li>說出相空間迴圈：自旋相同的分量繞圈，自旋相反的不動</li>'
        '<li>說出結果：閉合後振動回原狀，只留下糾纏 (|00⟩ − i|11⟩)/√2</li>'
        '<li>指出一個錯誤：迴圈沒閉合，運動和自旋仍糾纏，閘會出錯</li>'
        '<li>替說明圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q070 莫索閘 列印包', '父子科技學院 量子電腦學程 Q070｜Mølmer–Sørensen 閘', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q070-molmer-sorensen-gate', folder='Q070_莫索閘', files=FILES,
        sheet=('03_成就紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_莫索閘.pdf', pack_pages=4,
        pack_needles=('成就紀錄', '說明圖底稿', '隱藏成就觀察表', '解說卡', '最後一枚成就'),
        authoring_dir=XINEW / 'authoring/q070', episode_dir='specials/q070-molmer-sorensen-gate',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（ms_gate.py 只用 Python 標準函式庫）',
               'program': 'ms_gate.py', 'animation': 'animations/atoms.html#ms',
               'halfLoopP11': HALF_P11, 'gateTimeUs': {f'{k}kHz': v for k, v in GATE_US.items()},
               'stops': {f'{int(f * 100)}%': {'timeUs': t, 'alpha': a, 'P11': p} for f, (t, a, p) in STOPS.items()},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q070/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

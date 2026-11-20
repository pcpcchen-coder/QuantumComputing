"""Q043 課堂教材：冷卻功率計算程式、動畫驗算路線、闖關卡、計算表與曲線格、溫度減半挑戰、說明卡與解答。

不需要帳號；計算機或任何 Python 3 都能做，動畫路線只要瀏覽器。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q043/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

N_MMOL = 0.5  # 典型 ³He 循環率（mmol/s），簡報 p9 與動畫預設值


def q_uw(t_mk, n_mmol=N_MMOL):
    """Q̇ = 84 ṅ T²，回傳 μW。"""
    return 84 * (n_mmol * 1e-3) * (t_mk * 1e-3) ** 2 * 1e6


def t_bal_mk(load_uw, n_mmol=N_MMOL):
    return (load_uw * 1e-6 / (84 * n_mmol * 1e-3)) ** 0.5 * 1e3


TEMPS = [100, 50, 40, 30, 20, 10, 5]
TABLE = {t: round(q_uw(t), 2) for t in TEMPS}
assert TABLE[100] == 420 and TABLE[20] == 16.8 and TABLE[10] == 4.2 and TABLE[5] == 1.05
HALVES = [(40, 20), (20, 10), (10, 5)]
assert all(abs(q_uw(b) / q_uw(a) - 0.25) < 1e-12 for a, b in HALVES)
assert round(t_bal_mk(10), 1) == 15.4 and round(t_bal_mk(40), 1) == 30.9

PROGRAM = '''"""父子科技學院 量子電腦學程 Q043：稀釋冷凍原理——冷卻功率計算（任何 Python 3 都能跑，不需安裝套件）

公式：Q = 84 × n × T²     Q：瓦特（W）  n：氦三循環率（mol/s）  T：混合腔溫度（K）
執行：python cooling_power.py
"""

N_MMOL = 0.5            # 氦三循環率，單位 mmol/s（典型值；動畫預設也是 0.5）


def cooling_power_uw(t_mk, n_mmol=N_MMOL):
    n = n_mmol / 1000   # mmol/s → mol/s
    t = t_mk / 1000     # mK → K
    q = 84 * n * t ** 2  # 瓦特
    return q * 1e6      # W → μW


def balance_temp_mk(load_uw, n_mmol=N_MMOL):
    """冷卻功率剛好等於熱負載時的溫度：T = √(Q ÷ 84n)"""
    q = load_uw / 1e6
    n = n_mmol / 1000
    return (q / (84 * n)) ** 0.5 * 1000


print('溫度 (mK)   冷卻功率 (μW)')
for t in [100, 50, 40, 30, 20, 10, 5]:
    print(f'{t:>8}   {cooling_power_uw(t):>10.2f}')

print()
print('溫度減半大魔王：')
for a, b in [(40, 20), (20, 10), (10, 5)]:
    print(f'{a} mK → {b} mK：{cooling_power_uw(a):.2f} → {cooling_power_uw(b):.2f} μW，'
          f'剩 {cooling_power_uw(b) / cooling_power_uw(a):.2f} 倍')

print()
for load in [10, 40]:
    print(f'熱負載 {load} μW → 平衡溫度約 {balance_temp_mk(load):.1f} mK')

# 改造區：把 N_MMOL 改成 1.0 或 1.5，看冷卻功率和平衡溫度怎麼變
'''

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q043：稀釋冷凍原理（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：知道氦三溶入氦四時會吸熱，並用 Q̇ = 84ṅT² 算出不同溫度的冷卻功率。

## 兩條路線，可以一起用

| 路線 | 需要 | 用途 |
|---|---|---|
| A 計算機（或 `cooling_power.py`） | 計算機；或任何 Python 3，不需要裝套件 | 孩子親手算 |
| B 瀏覽器動畫 | 下載學程 `animations/`，用瀏覽器開 `peripherals.html#dilution`；免安裝、不需帳號 | 爸爸用滑桿驗算 |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 混合液分兩層、氦三循環四站、溶解吸熱 | 影片第 3–5 段、列印包第 1 頁 |
| 25–65 | 用公式算七個溫度的冷卻功率，畫曲線；爸爸用動畫驗算 | 列印包第 2 頁、`03_冷卻功率計算表.csv`、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 溫度減半大魔王：熱負載剩多少 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：稀釋冷凍原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 打開 `animations/peripherals.html#dilution`，找到左邊面板下方兩個滑桿（循環率、熱負載）和「平衡溫度」讀數，右下角是冷卻功率曲線。
- 列印 `02_列印包_稀釋冷凍原理.pdf`（A4，共 4 頁）；準備印章或貼紙當闖關章、計算機。讀一遍 `04_解答.md`。

## 關主的原則

- 單位最容易錯：mK ÷ 1000 → K、mmol/s ÷ 1000 → mol/s，算出的瓦特 × 1,000,000 → μW。
- 先猜再算：大魔王關一定要先寫下猜測（很多人會猜「剩一半」）。
- 動畫讀數只顯示 20 mK 和 100 mK 的冷卻功率與平衡溫度；其他溫度用「熱負載滑桿調到你算出的數字，看平衡溫度是不是你代入的溫度」來驗算。

## 誠實說明

- Q̇ = 84ṅT² 是理想值；實際機台因熱交換器效率等因素會低於它（動畫讀數也這樣註明）。本課只用它看趨勢。
- 「流汗蒸發」是幫助理解吸熱的類比，不是同一種物理過程。
- 典型循環率 0.5 mmol/s 取自學程簡報與動畫預設值，不是某一台機器的規格。
''',

'01_操作步驟.md': '''# 操作步驟

## 一、手算（約 25 分鐘）

1. 公式：冷卻功率 Q = 84 × n × T²（Q 單位 W；n 單位 mol/s；T 單位 K）。
2. 先換單位：n = 0.5 mmol/s = 0.0005 mol/s；例如 20 mK = 0.02 K。
3. 算：84 × 0.0005 × 0.02 × 0.02 = 0.0000168 W = 16.8 μW。
4. 照列印包第 2 頁，把 100、50、40、30、20、10、5 mK 都算一遍，填進表格，再把點畫在曲線格上連起來。

## 二、程式（選做，約 5 分鐘）

1. 執行 `python cooling_power.py`，對照你手算的表格。
2. 改造區：把 `N_MMOL` 改成 1.0，再跑一次，看每個數字變成幾倍。

## 三、動畫驗算（關主做，約 10 分鐘）

1. 打開 `animations/peripherals.html#dilution`，左邊面板捲到最下面。
2. 讀數第二行直接寫出「20 mK 時冷卻功率」和「100 mK 時」的數字，對照孩子的答案（預設 16.8 μW、420 μW）。
3. 其他溫度：把「MXC 上的熱負載」滑桿拉到孩子算出的功率（例如 30 mK 的 37.8 μW，滑桿每格 0.5，拉到 38 附近），讀「平衡溫度」是否約等於 30 mK。滑桿最大 60 μW，所以 40 mK 以上（67.2 μW 起）無法用滑桿驗，只驗 30 mK 以下。
4. 右下角小圖：青色曲線是冷卻功率，橘紅虛線是熱負載，黃點是平衡溫度。

## 四、溫度減半大魔王（約 30 分鐘）

1. 在列印包第 3 頁先寫猜測。
2. 算三組：40→20、20→10、10→5 mK，每組算「後 ÷ 前」。
3. 寫下規律，並說明為什麼（提示：T 乘了兩次）。
'''
,
'cooling_power.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 冷卻功率表（n = 0.5 mmol/s）\n\n| 溫度 (mK) | 溫度 (K) | 冷卻功率 (μW) |\n|---|---|---|\n'
  + ''.join(f'| {t} | {t / 1000:g} | {TABLE[t]:g} |\n' for t in TEMPS)
  + '\n## 溫度減半\n\n| 前 → 後 (mK) | 冷卻功率 (μW) | 後 ÷ 前 |\n|---|---|---|\n'
  + ''.join(f'| {a} → {b} | {TABLE[a]:g} → {TABLE[b]:g} | 1/4 |\n' for a, b in HALVES)
  + '\n規律：溫度減半，T² 變成 (1/2)² = 1/4，所以可承受的熱負載只剩四分之一。\n\n'
  '## 平衡溫度\n\n- 熱負載 10 μW → 約 15.4 mK（動畫預設）\n- 熱負載 40 μW（四倍）→ 約 30.9 mK（兩倍）\n'
  '- 循環率改成 1.2 mmol/s、熱負載 10 μW → 約 10.0 mK\n\n'
  '## 影片中的暫停題\n\n- 20 mK → 10 mK：約 17 μW（精確 16.8）→ 4.2 μW。\n\n'
  '## 常見問題\n\n'
  '- 為什麼溶解會吸熱？氦三從濃相越過界面進入稀相是吸熱過程，就像液體蒸發要吸熱；吸走的熱就是冷卻功率。\n'
  '- 為什麼混合腔最冷？吸熱發生在那裡；晶片的熱經樣品盒、支架、混合腔板傳到混合液被帶走。\n'
  '- 為什麼不能一直冷下去？越冷，冷卻功率按溫度平方掉得越快；任何一點熱負載都會讓溫度停在 T = √(Q ÷ 84n)。\n'
  '- 想冷一點怎麼辦？加大循環率（受泵和熱交換器限制），或更有效：把熱擋在上面幾層，別讓它到混合腔。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/peripherals.html#dilution`（周邊系統 場景 3：稀釋冷凍原理）

- 小圓點是 ³He，顏色代表溫度（紅色室溫 → 藍色極冷）；越過混合腔金色界面時會閃一下，代表吸熱。
- 加熱環在 Still（蒸餾室），³He 在那裡蒸發後從頂端被抽走。
- 滑桿「³He 循環率 ṅ (mmol/s)」0.1–1.5、「MXC 上的熱負載 (μW)」0.5–60；讀數顯示平衡溫度、20 mK 與 100 mK 的冷卻功率。
- 「視角：樣品區（晶片位置）」：看晶片的熱怎麼一路傳到混合液；「顯示熱傳導路徑」可開關。

## `animations/peripherals.html#overview`（場景 1：系統全景）

- 按「只看冷卻相關」，再關掉「脈衝管氦氣」「冷卻水」「真空」，只留紫色的混合氣循環：Still 抽氣 → 氣體處理系統 → 凝結回流；旁邊連著混合氣儲存槽。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；`R` 重設視角；左右方向鍵換場景。
''',
}

SHEET_HEADER = ['溫度 (mK)', '溫度 (K)', 'n (mol/s)', 'T²', '84 × n × T² (W)', '冷卻功率 (μW)', '動畫驗算（平衡溫度）', '對嗎？']
SHEET_ROWS = [[str(t), '', '0.0005'] for t in TEMPS]

STAMPS = ['第一關：說出濃相和稀相', '第二關：說出四站和吸熱的站', '第三關：算出 20 mK 的冷卻功率']

EXTRA_CSS = '''.stamps{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:4mm}
.stamp{border:1.4pt solid #0b2540;border-radius:50%;aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
text-align:center;font-size:12pt;padding:5mm}.stamp b{font-size:10pt;color:#4a6a88}.stamp.boss{border-style:dashed;border-width:2pt}
.plot{position:relative;height:72mm;border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;margin:3mm 0 0 14mm;
background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt),linear-gradient(90deg,#cfdde8 .6pt,transparent .6pt);background-size:100% 9mm,10% 100%}
.ylab{position:absolute;left:-13mm;font-size:9pt;color:#4a6a88}.xlab{display:flex;justify-content:space-between;margin:1mm 0 0 14mm;font-size:9.5pt;color:#4a6a88}
table.rec td{height:8.5mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.formula{font-size:16pt;text-align:center;margin:2mm 0;font-weight:700}'''


def html():
    stamp = ''.join(f'<div class="stamp"><b>第 {i} 關</b>{t.split("：")[1]}<br>□</div>' for i, t in enumerate(STAMPS, 1))
    xl = ''.join(f'<span>{x}</span>' for x in range(0, 101, 10))
    pages = [
        '<h2>闖關卡：稀釋冷凍原理</h2><p class="lead">每過一關，關主（爸爸）蓋一個章；三關全過才能挑戰大魔王。</p>'
        f'<div class="stamps">{stamp}</div>'
        '<div class="box" style="margin-top:6mm"><h3>第一關：兩種氦</h3><p>混合液冷到約＿＿＿K 以下會分成兩層：上層幾乎全是＿＿＿（濃相），'
        '下層是＿＿＿裡溶著一點＿＿＿（稀相），稀相裡至少還有＿＿＿%。</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>第二關：氦三的四站</h3>'
        '<p>① ＿＿＿＿（4 K 板）→ ② ＿＿＿＿（熱交換器）→ ③ ＿＿＿＿（混合腔）→ ④ ＿＿＿＿（蒸餾室）</p>'
        '<p>哪一站會吸熱？＿＿＿＿　為什麼？</p><div class="line"></div></div>',
        '<h2>第三關：冷卻功率計算表</h2><p class="formula">Q = 84 × n × T²　（n = 0.5 mmol/s = 0.0005 mol/s）</p>'
        '<table class="rec"><tr><th>溫度 (mK)</th><th>溫度 (K)</th><th>T²</th><th>冷卻功率 (W)</th><th>冷卻功率 (μW)</th></tr>'
        + ''.join(f'<tr><td>{t}</td><td></td><td></td><td></td><td></td></tr>' for t in TEMPS) + '</table>'
        '<h3 style="margin-top:4mm">把點畫上去連成曲線（橫軸 mK，縱軸 μW，每格 60 μW）</h3>'
        '<div class="plot"><span class="ylab" style="top:-2mm">480</span><span class="ylab" style="top:34mm">240</span>'
        f'<span class="ylab" style="bottom:-2mm">0</span></div><div class="xlab">{xl}</div>',
        '<h2>大魔王：溫度減半</h2><p class="lead">如果溫度減半，可以承受的熱負載剩下多少？先猜，再算三組。</p>'
        '<div class="box"><p>我的猜測：剩＿＿＿＿　理由：</p><div class="line"></div></div>'
        '<table class="rec" style="margin-top:4mm"><tr><th>前 → 後 (mK)</th><th>前的冷卻功率 (μW)</th><th>後的冷卻功率 (μW)</th><th>後 ÷ 前</th></tr>'
        + ''.join(f'<tr><td>{a} → {b}</td><td></td><td></td><td></td></tr>' for a, b in HALVES) + '</table>'
        '<div class="box" style="margin-top:4mm"><h3>找規律</h3><p>每次都剩＿＿＿＿，因為溫度在公式裡乘了＿＿次。</p>'
        '<p>反過來：熱負載變成 4 倍，平衡溫度變成＿＿倍。（動畫：熱負載 10 → 40 μW，平衡溫度＿＿＿ → ＿＿＿ mK）</p></div>'
        '<p class="note">挑戰題：循環率加倍（0.5 → 1.0 mmol/s），20 mK 的冷卻功率變成＿＿＿ μW。</p>',
        '<h2>說明卡：我的冷卻功率計算</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 稀釋冷凍機靠什麼變冷？</p><div class="line"></div><p>2. 為什麼混合腔是最冷的地方？</p><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：氦三從濃相溶入稀相會吸熱</li><li>說出氦三循環的四站</li>'
        '<li>用公式算一個溫度的冷卻功率，記得換單位</li><li>指出一個限制：越冷越難冷，溫度減半功率剩 1/4</li>'
        '<li>替計算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q043 稀釋冷凍原理 列印包', '父子科技學院 量子電腦學程 Q043｜稀釋冷凍原理', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q043-dilution-refrigerator', folder='Q043_稀釋冷凍原理', files=FILES,
        sheet=('03_冷卻功率計算表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_稀釋冷凍原理.pdf', pack_pages=4,
        pack_needles=('闖關卡', '第一關', '冷卻功率計算表', '大魔王', '溫度減半', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q043', episode_dir='specials/q043-dilution-refrigerator',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（計算機；選做 Python 3 標準函式庫；動畫用瀏覽器）',
               'program': 'cooling_power.py', 'coolingPowerTableUW': {str(k): v for k, v in TABLE.items()},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q043/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q102 課堂教材：可執行的頻率碰撞檢查器、動畫自由實驗操作步驟、禁區計算卡、三顆配置表、五顆挑戰表、說明卡與解答。

不需要帳號、不需要安裝套件：檢查器只用 Python 標準函式庫；動畫用瀏覽器開啟 animations/transmon-3d.html#case。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q102/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = '''"""父子科技學院 量子電腦學程 Q102：頻率碰撞檢查器（只用 Python 標準函式庫，不需安裝、不需帳號）

規則與數值照學程 3D 動畫 transmon-3d.html#case（第 6 章）的設定：
  非諧性 α = −283 MHz（1→2 比 0→1 低 283 MHz）
  判定窗（示意值）：同頻 ±30 MHz、0→1 撞 1→2 ±25 MHz、雙光子 ±12 MHz
位元排成一列：Q1 – Q2 – Q3 – …，相鄰的兩顆互為鄰居；
同一顆位元的兩個鄰居（隔一顆）也要檢查「旁觀者碰撞」。

執行：python collision_checker.py
改造：把 PLANS 裡的頻率換成你自己排的數字（單位 GHz），再執行一次。
"""
ALPHA = -0.283                                  # GHz
WIN = {'same': 0.030, 'x12': 0.025, 'tp': 0.012}  # GHz


def check(freqs, tops=None):
    """回傳碰撞清單；空清單代表依動畫的判定窗沒有碰撞。
    tops：每顆位元的最高頻率（磁通為零的 sweet spot）；SQUID 只能往下調，超過就算錯。"""
    out = []
    n = len(freqs)
    for k, (f, top) in enumerate(zip(freqs, tops or [9.9] * n)):
        if f > top + 1e-9:
            out.append(f'Q{k + 1} 排 {f:.2f} 高於最高 {top:.2f}（只能往下調）')

    def pair(i, j, spectator):
        fi, fj = freqs[i], freqs[j]
        a, b = f'Q{i + 1}', f'Q{j + 1}'
        pre = '旁觀者：' if spectator else ''
        if abs(fi - fj) < WIN['same']:
            out.append(f'{pre}{a} ≈ {b}（同頻，差 {abs(fi - fj) * 1000:.0f} MHz）')
        if abs(fi - (fj + ALPHA)) < WIN['x12']:
            out.append(f'{pre}{a} 0→1 ≈ {b} 1→2')
        if abs(fj - (fi + ALPHA)) < WIN['x12']:
            out.append(f'{pre}{b} 0→1 ≈ {a} 1→2')
        if not spectator:
            if abs(fi - (fj + ALPHA / 2)) < WIN['tp']:
                out.append(f'{a} 驅動 ≈ {b} 雙光子 0→2')
            if abs(fj - (fi + ALPHA / 2)) < WIN['tp']:
                out.append(f'{b} 驅動 ≈ {a} 雙光子 0→2')

    for i in range(n - 1):
        pair(i, i + 1, False)      # 相鄰
    for i in range(n - 2):
        pair(i, i + 2, True)       # 同一顆位元的兩個鄰居
    return out


def zones(f):
    """某顆位元頻率為 f 時，鄰居不能去的五個頻率（GHz）。"""
    return {'0→1 撞 1→2（下）': f + ALPHA, '雙光子（下）': f + ALPHA / 2, '同頻': f,
            '雙光子（上）': f - ALPHA / 2, '0→1 撞 1→2（上）': f - ALPHA}


# 五顆練習用的「最高頻率」（自訂的練習數字，不是哪一台真機的資料）
TOPS5 = [5.12, 5.10, 5.39, 5.05, 5.25]

PLANS = {
    '剛做好（製程原貌）': [5.12, 5.10, 5.39],
    '棋盤格': [4.90, 5.10, 4.90],
    '動畫的配置': [4.90, 5.10, 5.30],
    '第二個空位': [4.90, 5.10, 5.00],
    '五顆（第一次嘗試）': [4.90, 5.10, 5.30, 5.00, 4.80],
    '五顆（範例解）': [4.90, 5.10, 5.30, 4.90, 5.10],
}

if __name__ == '__main__':
    print('Q2 在 5.10 GHz 時，鄰居的禁區：')
    for k, v in zones(5.10).items():
        print(f'  {k:<14}{v:.3f} GHz')
    print()
    for name, fs in PLANS.items():
        res = check(fs, TOPS5 if len(fs) == 5 else None)
        print(f'{name}：' + '、'.join(f'{f:.2f}' for f in fs) + ' GHz')
        print('  ' + ('無碰撞 ✓' if not res else f'碰撞 {len(res)} 處：' + '；'.join(res)))
'''

# 建置時真的執行一次檢查器，結果必須和影片、解答一致（製作代理實跑：Python 3.13.18）
_NS = {}
exec(compile(PROGRAM, 'collision_checker.py', 'exec'), _NS)
CHECK, ZONES, TOPS5, PLANS = _NS['check'], _NS['zones'], _NS['TOPS5'], _NS['PLANS']
RESULTS = {name: CHECK(fs, TOPS5 if len(fs) == 5 else None) for name, fs in PLANS.items()}
assert len(RESULTS['剛做好（製程原貌）']) == 3
assert RESULTS['棋盤格'] == ['旁觀者：Q1 ≈ Q3（同頻，差 0 MHz）']
assert RESULTS['動畫的配置'] == [] and RESULTS['第二個空位'] == [] and RESULTS['五顆（範例解）'] == []
assert RESULTS['五顆（第一次嘗試）'] == ['Q4 0→1 ≈ Q3 1→2']
Z = {k: round(v, 3) for k, v in ZONES(5.10).items()}
assert list(Z.values()) == [4.817, 4.958, 5.1, 5.241, 5.383], Z


def _res(name):
    r = RESULTS[name]
    return '無碰撞 ✓' if not r else f'碰撞 {len(r)} 處：' + '；'.join(r)


ANSWER_ROWS = ''.join(f'| {n} | ' + '、'.join(f'{f:.2f}' for f in fs) + f' | {_res(n)} |\n' for n, fs in PLANS.items())

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q102：頻率配置與頻率碰撞（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的頭目戰：替多顆可調 transmon 排頻率，避開鄰居的禁區。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三個原因、五個禁區、棋盤格為什麼不夠 | 影片第 3–5 段、列印包第 1 頁（禁區計算卡） |
| 25–65 | 替三顆位元排頻率，在動畫自由實驗檢查（孩子是排頻師、爸爸是頭目） | `01_操作步驟.md`、列印包第 2 頁 |
| 65–75 | 休息 | |
| 75–105 | 紙上挑戰五顆位元，用 `collision_checker.py` 驗收 | 列印包第 3 頁、`03_頻率配置表.csv` |
| 105–115 | 孩子教爸爸：怎麼排、為什麼會撞 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#case`，按步驟按鈕「6」進入自由實驗，試拖一次 Q3 Φ 滑桿。
- 有 Python 3 的電腦執行一次 `python collision_checker.py`（不用裝任何套件），確定會印出四種排法的結果。
- 列印 `02_列印包_頻率配置.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 頭目（爸爸）的原則

- 先算禁區再放位元：孩子沒在頻率尺上畫禁區就放，先不算過關。
- 喊「碰撞！」時要說出種類：同頻、0→1 撞 1→2、雙光子、旁觀者。
- 撞車很正常：影片裡我們第一次排五顆，也在 Q4 撞上 Q3 的 1→2。

## 誠實說明

- 判定窗（同頻 ±30、0→1 撞 1→2 ±25、雙光子 ±12 MHz）和動畫一樣是**示意值**；真機依耦合、脈衝與校準而定。
- 五顆練習的「最高頻率」是自訂的練習數字，不是哪一台真機的資料。
- 頻率配置還受製程誤差影響：設計值和實測值會不同，排好之後還要量、還要調；材料缺陷也會隨時間飄移。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：三顆位元（約 40 分鐘）

1. 在列印包第 1 頁算出 Q2（5.10 GHz）的五個禁區：5.10 ± 0.283、5.10 ± 0.1415、5.10。
2. 在列印包第 2 頁的頻率尺畫出禁區，替 Q1、Q3 各選一個頻率（不能超過最高頻率：Q1 5.12、Q3 5.39）。
3. 打開 `animations/transmon-3d.html#case`，按步驟按鈕「6」進入「⑥ 自由實驗」。
4. 先按「回到製程原貌」：看紅色帶和面板的碰撞清單（碰撞 3 處）。按「π → Q1」，看 Q2 的 P₁ 也被激發。
5. 勾選「顯示 Q2 鄰居的禁區」，拖動「Q1 Φ」「Q3 Φ」滑桿，把頻率調到你排的數字（面板 Q1、Q3 那一列會顯示 GHz）。
6. 碰撞清單出現「無碰撞 ✓」才算打倒頭目；再按「π → Q1」「π → Q3」，確認只有目標亮起來。
7. 填到列印包第 2 頁的配置表；也可以改 `collision_checker.py` 的 PLANS 再跑一次對照。

## 下半場：五顆位元（約 30 分鐘，紙上）

1. 列印包第 3 頁有五顆位元的最高頻率：5.12、5.10、5.39、5.05、5.25 GHz（練習數字）。
2. 從中間開始排，每放一顆就查：和左右鄰居（同頻、0→1 撞 1→2、雙光子），以及隔一顆的位元（旁觀者：同頻、0→1 撞 1→2）。
3. 排完把五個數字填進 `collision_checker.py` 的 PLANS，執行驗收；撞車就改一個數字再跑。
''',

'collision_checker.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## Q2 = 5.10 GHz 時鄰居的禁區\n\n| 禁區 | 頻率（GHz） |\n|---|---|\n'
  + ''.join(f'| {k} | {v:.3f} |\n' for k, v in ZONES(5.10).items())
  + '\n## 碰撞檢查程式實跑（Python 3.13.18）\n\n| 排法 | 頻率（GHz） | 結果 |\n|---|---|---|\n' + ANSWER_ROWS
  + '\n三顆的答案不只一組：Q3 放 5.30 或 5.00 都可以（動畫和程式都顯示無碰撞）；Q1 也可以試 4.70（避開 4.817 與 4.958）。\n'
  + '五顆的答案也不只一組；只要程式印出「無碰撞 ✓」、而且每顆都沒超過最高頻率就過關。\n\n'
  + '## 常見問題\n\n'
  '- 為什麼不能全部調成一樣？相鄰同頻會交換激發，π 脈衝也分不出要打哪一顆（動畫製程原貌：打 Q1，Q2 的 P₁ 約 0.3）。\n'
  '- 為什麼 1→2 比 0→1 低？transmon 的能階越往上越密，非諧性 α ≈ −283 MHz（動畫第 3 章）。\n'
  '- 雙光子是什麼？兩個光子一起把位元從 0 推到 2，每個光子的頻率是 0→2 總能量的一半，約在 0→1 下方 141 MHz。\n'
  '- 為什麼棋盤格不夠？中間位元的兩個鄰居同頻，對中間位元做閘時，兩邊一起被拖下水（旁觀者碰撞）。\n'
  '- 那受控相位翻轉閘（CZ）呢？做閘時才刻意把 Q3 推到 5.383 GHz（Q2 0→1 = Q3 1→2），只停留幾十奈秒；動畫自由實驗的「CZ（Q2–Q3）」按鈕可以看。\n'
  '- 為什麼要排得比最高頻率低？SQUID 只能把頻率往下調，最高點在磁通 0（sweet spot）。\n',

'05_動畫導覽.md': '''# 動畫導覽：transmon-3d.html 第 6 章「案例」

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

- 開 `transmon-3d.html#case`；上方步驟按鈕 1–6：① 製程誤差、② SQUID 調頻、③ 頻率配置、④ XY 寫入、⑤ CZ 閘、⑥ 自由實驗。前五步會自動播放並在左上方跳出說明。
- 頻率尺（4.55–5.45 GHz）：每顆位元有實線 0→1、細線 1→2、◆ 雙光子；紅色帶＝碰撞。
- ⑥ 自由實驗：「Q1 Φ／Q2 Φ／Q3 Φ」滑桿、「π → Q1／Q2／Q3」、「CZ（Q2–Q3）」、「回到配置」、「回到製程原貌」、「顯示 Q2 鄰居的禁區」。
- 面板下方：每顆位元的 f₀₁、Φ、P(|1⟩)，以及碰撞清單（「碰撞 n 處」或「無碰撞 ✓」）。面板比較高時往下捲。
- 操作：滑鼠拖曳旋轉、滾輪縮放、左右方向鍵換章節。
''',
}

SHEET_HEADER = ['排法', '位元數', 'Q1 (GHz)', 'Q2 (GHz)', 'Q3 (GHz)', 'Q4 (GHz)', 'Q5 (GHz)', '我預測的碰撞', '動畫／程式的結果', '改了什麼']
SHEET_ROWS = [['製程原貌', '3', '5.12', '5.10', '5.39'], ['棋盤格', '3', '4.90', '5.10', '4.90'],
              ['我的三顆第 1 次', '3'], ['我的三顆第 2 次', '3'], ['我的五顆第 1 次', '5'], ['我的五顆第 2 次', '5'],
              ['我的五顆第 3 次', '5']]

EXTRA_CSS = '''table.rec td{height:10mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.ruler{position:relative;height:30mm;margin:4mm 4mm 2mm;border-bottom:1.4pt solid #0b2540}
.ruler span{position:absolute;bottom:-6mm;font-size:9pt;transform:translateX(-50%);color:#4a6a88}
.ruler i{position:absolute;bottom:0;width:0;height:4mm;border-left:1pt solid #0b2540}
.zone td{font-size:12pt;height:9mm}pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def ruler():
    ticks = ''.join(f'<i style="left:{(f - 4.6) / 0.8 * 100:.1f}%"></i><span style="left:{(f - 4.6) / 0.8 * 100:.1f}%">{f:.1f}</span>'
                    for f in [4.6 + 0.1 * k for k in range(9)])
    return f'<div class="ruler">{ticks}</div><p class="note" style="margin-top:8mm">頻率尺 4.6–5.4 GHz：用鉛筆畫禁區（斜線），再用彩色筆畫位元的實線。</p>'


def html():
    pages = [
        '<h2>關卡一：禁區計算卡</h2><p class="lead">規則：自己的任何一條線，撞上鄰居的任何一條線，就是碰撞。α = −0.283 GHz。</p>'
        '<table class="rec zone"><tr><th>碰撞種類</th><th>怎麼算（鄰居 B 不能去）</th><th>A = 5.21 GHz</th><th>Q2 = 5.10 GHz</th></tr>'
        '<tr><td>同頻</td><td>f_B ≈ f_A</td><td>5.21</td><td></td></tr>'
        '<tr><td>B 的 0→1 撞 A 的 1→2</td><td>f_B ≈ f_A − 0.283</td><td>4.93</td><td></td></tr>'
        '<tr><td>A 的 0→1 撞 B 的 1→2</td><td>f_B ≈ f_A + 0.283</td><td>5.49</td><td></td></tr>'
        '<tr><td>雙光子（兩條）</td><td>f_B ≈ f_A ± 0.1415</td><td>5.07、5.35</td><td></td></tr>'
        '<tr><td>旁觀者</td><td>A 的兩個鄰居之間：同頻、0→1 撞 1→2</td><td colspan="2">鄰居的鄰居也要查</td></tr></table>'
        '<div class="box" style="margin-top:5mm"><h3>先想一想</h3><p>為什麼 1→2 比 0→1 低？</p><div class="line"></div>'
        '<p>棋盤格（Q1 = Q3 = 4.90、Q2 = 5.10）哪裡出事？</p><div class="line"></div></div>'
        '<p class="note">禁區寬度（同頻 ±30、1→2 ±25、雙光子 ±12 MHz）是動畫的示意值。</p>',
        '<h2>關卡二：三顆位元的頻率配置表</h2><p class="lead">Q2 留在 5.10（sweet spot）。Q1 最高 5.12、Q3 最高 5.39 GHz，只能往下調。</p>'
        + ruler() +
        '<table class="rec"><tr><th>位元</th><th>最高頻率</th><th>我排的頻率</th><th>為什麼不會撞</th></tr>'
        '<tr><td>Q1</td><td>5.12</td><td></td><td></td></tr><tr><td>Q2</td><td>5.10</td><td>5.10</td><td>留在 sweet spot</td></tr>'
        '<tr><td>Q3</td><td>5.39</td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:4mm"><h3>動畫驗收（transmon-3d.html#case → 步驟 6 自由實驗）</h3><ul class="chk">'
        '<li>回到製程原貌：看到碰撞 3 處</li><li>拖滑桿到我排的頻率：出現「無碰撞 ✓」</li>'
        '<li>π → Q1：只有 Q1 亮</li><li>π → Q3：只有 Q3 亮</li></ul></div>',
        '<h2>關卡三：五顆位元（紙上挑戰）</h2><p class="lead">Q1–Q5 排成一列。每顆的最高頻率是練習數字，排的時候不能超過。</p>'
        '<table class="rec"><tr><th>位元</th><th>最高頻率</th><th>第 1 次</th><th>第 2 次</th><th>第 3 次</th></tr>'
        + ''.join(f'<tr><td>Q{i}</td><td>{t:.2f}</td><td></td><td></td><td></td></tr>' for i, t in enumerate(TOPS5, 1))
        + '<tr><td>碰撞？</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p style="margin-top:3mm">逐對檢查：相鄰（Q1–Q2、Q2–Q3、Q3–Q4、Q4–Q5）查同頻、1→2、雙光子；隔一顆（Q1–Q3、Q2–Q4、Q3–Q5）查旁觀者。</p>'
        '<pre class="code"># collision_checker.py 的 PLANS 加一行，再執行\n\'我的五顆\': [___, ___, ___, ___, ___],</pre>'
        '<p class="note">撞車很正常：影片裡我們第一次排五顆，也在 Q4 撞上 Q3 的 1→2。</p>',
        '<h2>說明卡：我的頻率配置表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 為什麼頻率要錯開？（三個原因）</p><div class="line"></div><div class="line"></div>'
        '<p>2. 碰撞有哪幾種？</p><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出頻率要錯開的三個原因：寫入、耦合、隱藏頻率</li><li>說出四種碰撞：同頻、0→1 撞 1→2、雙光子、旁觀者</li>'
        '<li>解釋棋盤格為什麼不夠</li><li>指出一個限制：製程誤差讓設計值和實測值不同；只能往下調；缺陷會飄移</li>'
        '<li>替配置表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q102 頻率配置 列印包', '父子科技學院 量子電腦學程 Q102｜頻率配置與頻率碰撞', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q102-frequency-collisions', folder='Q102_頻率配置與頻率碰撞', files=FILES,
        sheet=('03_頻率配置表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_頻率配置.pdf', pack_pages=4,
        pack_needles=('禁區計算卡', '三顆位元的頻率配置表', '五顆位元', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q102', episode_dir='specials/q102-frequency-collisions',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（Python 3 標準函式庫；動畫用瀏覽器開啟）',
               'program': 'collision_checker.py', 'testedWith': 'Python 3.13.18',
               'recordedRun': {k: (v or '無碰撞') for k, v in RESULTS.items()}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q102/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

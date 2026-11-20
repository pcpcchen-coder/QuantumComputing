"""Q053 課堂教材：洩漏對照圖、故障卡、虛擬 Z 省時間練習、可執行的 leak_lab.py、說明卡與解答。

不需要帳號、不需要安裝套件（leak_lab.py 只用 Python 標準函式庫；也可以只用動畫）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q053/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# operation.html#pulse 右下插圖「f₁₂ 處 … dB」（面積 180°；圖的下限 −60）；括號內是 Python 重現 03_pulse.js 的未截斷值
LEAK = [  # (閘長度, 方波, 高斯, 高斯 + DRAG)
    ('40 ns', '−34', '−59', '−60（約 −85）'),
    ('20 ns', '−23', '−50', '−60（約 −74）'),
    ('10 ns', '−21', '−34', '−60（約 −72）'),
]

# 改造練習：一段單一量子位元線路（練習假設：每個閘若用真脈衝都是 40 ns）
CIRCUIT = ['H', 'S', 'H', 'T', 'X', 'Z', 'H', 'S']
PHASE_ONLY = {'Z': '繞 z 轉 180°', 'S': '繞 z 轉 90°', 'T': '繞 z 轉 45°'}

CARDS = [  # (卡名, 故障描述, 處方, 驗證)
    ('方波漏電', '用 40 ns 的方波做翻轉閘，量完發現有些狀態跑到 |2⟩。',
     '換成高斯，再加上 DRAG 修正分量。', '動畫切換形狀：f₁₂ 處 −34 → −59 → −60 dB'),
    ('趕時間', '為了快，把高斯脈衝縮成 10 ns，洩漏變多。',
     '加上 DRAG，或把閘時間放回 20–40 ns。', '10 ns 高斯 −34 dB；加 DRAG 壓到 −60'),
    ('係數歸零', '有人把 DRAG 係數 β 設成 0，洩漏又回來了。',
     'β 要校準：掃描 β，找誤差最小的那一點。', 'lc-vs-jj 第 6 步：β=0 時「1.0 倍」'),
    ('刪掉虛擬 Z', '工程師說「虛擬 Z 沒送脈衝，刪掉也沒差」，結果答案全錯。',
     '不能刪：它改了後面所有脈衝的相位，要在軟體裡記帳。', '90°、虛擬 Z、90° 停在赤道；刪掉後 90°、90° 跑到南極'),
    ('只有兩層樓', '設計師說「量子位元只有 0 和 1，頻譜寬一點沒關係」。',
     'transmon 不是完美二能階：f₁₂ 只比 f₀₁ 低約 200–300 MHz。', '看動畫紅色虛線離 f₀₁ 多近'),
    ('多花的 40 ns', '線路裡的 Z、S、T 都用真的脈衝做，整段線路變慢。',
     '改成虛擬 Z：只改後面脈衝的相位，0 ns。', '列印包第 3 頁練習：算出省多少'),
]

PROGRAM = '''"""父子科技學院 量子電腦學程 Q053：DRAG 與虛擬 Z 的小實驗室（只用 Python 標準函式庫）

執行：python leak_lab.py
一、照 operation.html#pulse（03_pulse.js）的算法，算方波、高斯、高斯 + DRAG 在 f₁₂ 處的頻譜高度（dB，以 f₀₁ 為 0 dB）。
二、在布洛赫球上比較「90°、虛擬 Z、90°」和「90°、90°」。
三、把線路裡只改相位的閘改成虛擬 Z，算省下多少時間（練習假設：每個真脈衝 40 ns）。
模型忽略退相干與線路失真，只用來比較趨勢。
"""
import math

ALPHA = -0.22  # f12 − f01（GHz），和動畫相同


def wave(shape, area_deg=180, tg=40.0):
    """回傳 [(t, I, Q)]，I、Q 單位 rad/ns；面積只由 I 決定。"""
    def env(t):
        if shape == 'square':
            return 1.0
        s, x = tg / 4, t - tg / 2
        return math.exp(-x * x / (2 * s * s)) - math.exp(-tg * tg / (8 * s * s))
    beta = 1 / (2 * math.pi * ALPHA)           # 讓頻譜在 f12 處為零
    n, dt, total, raw = 400, tg / 400, 0.0, []
    for i in range(n + 1):
        t = i * dt
        d_env = (env(t + 0.01) - env(t - 0.01)) / 0.02
        raw.append((t, env(t), beta * d_env if shape == 'drag' else 0.0))
        total += env(t) * dt
    k = math.radians(area_deg) / total
    return [(t, i * k, q * k) for t, i, q in raw]


def spectrum(w, f, tg):
    re = im = 0.0
    dt = tg / (len(w) - 1)
    for t, i, q in w:
        a = -2 * math.pi * f * t
        re += (i * math.cos(a) - q * math.sin(a)) * dt
        im += (i * math.sin(a) + q * math.cos(a)) * dt
    return math.hypot(re, im)


print('一、f12 處的頻譜高度（dB；動畫的圖最低只畫到 -60）')
print('  閘長度   方波    高斯    高斯+DRAG')
for tg in (40, 20, 10):          # 改造區：加 30、16 試試
    row = []
    for shape in ('square', 'gauss', 'drag'):
        w = wave(shape, 180, tg)
        row.append(20 * math.log10(spectrum(w, ALPHA, tg) / spectrum(w, 0, tg)))
    print(f'  {tg:>3} ns  {row[0]:6.1f}  {row[1]:6.1f}  {row[2]:8.1f}')


def rot(v, axis, ang):
    """布洛赫向量 v 繞單位軸 axis 轉 ang（弧度），羅德里格斯公式。"""
    a, b, c = axis
    x, y, z = v
    co, si = math.cos(ang), math.sin(ang)
    d = a * x + b * y + c * z
    return (x * co + (b * z - c * y) * si + a * d * (1 - co),
            y * co + (c * x - a * z) * si + b * d * (1 - co),
            z * co + (a * y - b * x) * si + c * d * (1 - co))


X90 = lambda v: rot(v, (1, 0, 0), math.pi / 2)   # 相位 0° 的 90° 脈衝
VZ90 = lambda v: rot(v, (0, 0, 1), math.pi / 2)  # 虛擬 Z（90°）：動畫把箭頭繞 z 轉 90°


def show(name, v):
    print(f'  {name:<26} (x, y, z) = ({v[0]:+.2f}, {v[1]:+.2f}, {v[2]:+.2f})  P(1) = {(1 - v[2]) / 2:.3f}')


print('\\n二、虛擬 Z 會改變後面的脈衝')
N = (0.0, 0.0, 1.0)
show('90°、90°', X90(X90(N)))
show('90°、虛擬Z、90°', X90(VZ90(X90(N))))
show('90°、虛擬Z、90°、虛擬Z、90°', X90(VZ90(X90(VZ90(X90(N))))))

print('\\n三、改成虛擬 Z 省多少時間（練習假設：每個真脈衝 40 ns）')
circuit = ['H', 'S', 'H', 'T', 'X', 'Z', 'H', 'S']   # 改造區：換成你自己的線路
phase_only = {'Z', 'S', 'T'}
before = 40 * len(circuit)
after = 40 * sum(g not in phase_only for g in circuit)
print(f'  線路 {" ".join(circuit)}')
print(f'  原本 {before} ns，改成虛擬 Z 後 {after} ns，省下 {before - after} ns（{(before - after) / before:.0%}）')
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q053：DRAG 與虛擬 Z（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心有兩句：**DRAG 在 f₁₂ 那個頻率替脈衝的頻譜挖洞，讓快速脈衝少漏到 |2⟩；虛擬 Z 不送脈衝，只改之後所有脈衝的相位，所以不花時間。** 好玩機制是故障卡：爸爸抽卡念出故障，孩子當維修員說出原因、開處方，再到動畫驗證。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開動畫，認識三種脈衝形狀與「虛擬 Z（90°）」按鈕 | `operation.html#pulse`、`lc-vs-jj.html#s6drag` |
| 25–65 | 量三種脈衝在 f₁₂ 處的 dB，畫洩漏對照圖；輪流抽故障卡 | 列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 把線路裡的 Z、S、T 改成虛擬 Z，算省下多少時間；動畫驗證虛擬 Z 會改變後面的脈衝 | 列印包第 3 頁、`leak_lab.py` |
| 105–115 | 孩子教爸爸：DRAG 與虛擬 Z 的作用、一個限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#pulse`（課綱指定）與 `lc-vs-jj.html#s6drag`（不需要網路、伺服器或帳號）。
- 列印 `02_列印包_DRAG與虛擬Z.pdf`（A4，共 4 頁），第 2 頁的故障卡沿虛線剪開。
- 讀一遍 `04_解答.md`。

## 出題者的原則

- 念卡時只說「故障現象」，不要先說處方。
- 孩子開完處方，一定要到動畫驗證：分貝數降了、或箭頭停對地方，才算修好。
- 答錯了請孩子說：是哪一個觀念想錯（頻譜？能階？相位記帳？）。

## 誠實說明

- operation 動畫的 dB 是「頻譜相對 f₀₁ 的高度」，不是洩漏機率；圖最低只畫到 −60 dB，DRAG 實際更低。
- lc-vs-jj 動畫的洩漏機率（6 ns：純高斯約 4.7%、DRAG 約 0.04%）是三能階模型（α = −250 MHz）的數值，不是特定硬體量測。
- 改造練習「每個閘 40 ns」是教學假設；真實硬體的閘時間因機器而異。
- 方向說明：operation 動畫中 x 軸（橘）朝向觀眾、y 軸（綠）朝右；轉動視角後左右會跟著改變。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：洩漏對照圖（約 20 分鐘）

1. 打開 `animations/operation.html#pulse`。「脈衝面積」保持 180°。
2. 依序點「方波」「高斯」「高斯 + DRAG」，讀右下插圖紅色虛線旁的「f₁₂ 處 … dB」，抄到列印包第 1 頁。
3. 把「閘長度（ns）」改成 20、10，再各量一次三種形狀。
4. 在第 1 頁的長條圖畫出九個數字（越往下越好），替這張洩漏對照圖取名字。
5. 加碼：打開 `animations/lc-vs-jj.html#s6drag`，看最下面三格讀數；把「DRAG 係數 β」從 1 拉到 0，看「洩漏降低倍數」變成幾倍。

## 上半場：故障卡（約 20 分鐘）

1. 爸爸洗牌、抽一張卡，只念「故障」那一行。
2. 孩子說出原因、開處方，再照卡上的「驗證」到動畫裡確認。
3. 修好的卡放一邊，換人抽卡（也可以讓孩子自己出一張新故障卡）。

## 下半場：改成虛擬 Z（約 30 分鐘）

1. 在列印包第 3 頁的線路表，圈出只改相位的閘（Z、S、T），填上原本與改虛擬 Z 後的時間。
2. 執行 `python leak_lab.py`，對答案。
3. 動畫驗證：operation.html#pulse，面板捲到最下面，面積 90°：送出脈衝 → 按「虛擬 Z（90°）」→ 再送出脈衝，記下箭頭位置與 P(1)。按「重設 |0⟩」，改成只送兩次脈衝，比較結果。
''',

'leak_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 洩漏對照圖（operation.html#pulse，面積 180°，f₁₂ 處 dB）\n\n| 閘長度 | 方波 | 高斯 | 高斯 + DRAG |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in LEAK)
  + '\n動畫的圖最低只畫到 −60 dB；括號是程式算出的未截斷值。規律：越短越寬（數字越大＝越漏），方波最漏，DRAG 在 f₁₂ 挖洞。10 ns 的高斯（−34）和 40 ns 的方波一樣糟。\n\n'
  '## lc-vs-jj.html#s6drag（三能階模型，α = −250 MHz）\n\n'
  '- 預設 6 ns、β = 1：純高斯結束後留在 |2⟩ 4.7 × 10⁻²，DRAG 4.0 × 10⁻⁴，降低 118.0 倍。\n'
  '- β = 0：兩條線重合，「1.0 倍」。\n- β = 1、20 ns：2.7 × 10⁻⁵ 對 4.9 × 10⁻¹⁰，約 5.5 × 10⁴ 倍。\n\n'
  '## 故障卡\n\n| 卡 | 原因與處方 | 驗證 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {c} | {d} |\n' for a, b, c, d in CARDS)
  + '\n## 改成虛擬 Z\n\n'
  f'- 線路 {" ".join(CIRCUIT)}：只改相位的有 S、T、Z、S 共 4 個（Z = 繞 z 180°、S = 90°、T = 45°）。\n'
  '- 原本 8 × 40 = 320 ns；改虛擬 Z 後 4 × 40 = 160 ns，省 160 ns（50%）。\n'
  '- 動畫：90°、虛擬 Z、90° → 箭頭朝向觀眾（+x），P(1) = 0.500，「虛擬 Z 累積的座標相位 = 90°」；只送 90°、90° → 南極，P(1) = 1.000。\n'
  '- 再加一次虛擬 Z、再一個 90° → 回到北極，P(1) = 0.000。\n\n'
  '## 常見誤解\n\n'
  '- 「transmon 只有 0 和 1」：還有 |2⟩、|3⟩…，f₁₂ 只比 f₀₁ 低約 200–300 MHz。\n'
  '- 「虛擬 Z 什麼都沒做，可以刪」：它改了後面所有脈衝的相位，刪掉結果就變。\n'
  '- 「DRAG 讓脈衝變慢」：脈衝一樣快，只是在 f₁₂ 的頻譜挖了洞。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#pulse`（如何操作量子電腦 場景 3：微波脈衝，課綱指定）

- 選項：「方波」「高斯」「高斯 + DRAG」；滑桿：「脈衝面積 → 旋轉角」「脈衝相位 φ → 旋轉軸方向」「頻率失諧 Δ（MHz）」「閘長度（ns）」。
- 按鈕：「▶ 送出脈衝」「虛擬 Z（90°）」「重設 |0⟩」；面板最下面有「虛擬 Z 累積的座標相位」與「目前 P(1)」讀數。
- 右下插圖：上半是 I（金）與 Q×3（青）包絡，下半是頻譜，紅色虛線是 f₁₂（f₀₁ − 220 MHz），旁邊寫「f₁₂ 處 … dB」。

## `animations/lc-vs-jj.html#s6drag`（LC 與約瑟夫森接面 第 6 步：DRAG 讓脈衝在 ω₁₂ 上挖一個洞）

- 四張小圖：脈衝包絡、頻譜、脈衝期間 |2⟩ 的佔有率、閘結束後的洩漏 vs 閘長度；橘褐色是純高斯、紫色是 DRAG。
- 滑桿「π 脈衝長度」「非諧性 α」「DRAG 係數 β」；最下面三格讀數：純高斯與 DRAG 結束後留在 |2⟩ 的機率、洩漏降低倍數。

## 操作

滑鼠拖曳旋轉、滾輪縮放；operation 頁可用左右方向鍵切換場景、`H` 隱藏面板。
''',
}

SHEET_HEADER = ['閘長度', '方波 dB', '高斯 dB', '高斯 + DRAG dB', '我的觀察']
SHEET_ROWS = [[a] for a, *_ in LEAK]

EXTRA_CSS = '''table.lk td{height:12mm;font-size:12pt}table.lk th{font-size:11pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:3.5mm 4.5mm;height:76mm}
.cards h3{font-size:14pt;margin:0 0 1.5mm}.cards p{margin:1mm 0;font-size:11pt}.cards .rx{border-top:.8pt dotted #7f9bb3;padding-top:1.5mm;margin-top:2mm;color:#35506b}
table.ct td{height:10mm;text-align:center}table.ct th{text-align:center}
.bars{height:58mm;border-left:1pt solid #0b2540;border-bottom:1pt solid #0b2540;margin:3mm 0 0 10mm;position:relative}'''


def html():
    rows = ''.join(f'<tr><td style="width:24mm">{a}</td><td></td><td></td><td></td></tr>' for a, *_ in LEAK)
    cards = ''.join(f'<div class="cut"><h3>故障卡 {i}：{a}</h3><p><b>故障：</b>{b}</p>'
                    f'<div class="rx"><p><b>我的診斷：</b>＿＿＿＿＿＿＿＿＿＿＿＿</p><p><b>我的處方：</b>＿＿＿＿＿＿＿＿＿＿＿＿</p>'
                    f'<p class="note">驗證方法：{d}</p></div></div>' for i, (a, b, c, d) in enumerate(CARDS, 1))
    ct = ''.join(f'<tr><td>{k}</td><td>{g}</td><td></td><td></td><td></td></tr>' for k, g in enumerate(CIRCUIT, 1))
    pages = [
        '<h2>洩漏對照圖</h2><p class="lead">operation.html#pulse，面積 180°。讀右下插圖紅色虛線旁的「f₁₂ 處 … dB」：數字越接近 0 越漏，越往下越好。</p>'
        '<table class="lk"><tr><th>閘長度</th><th>方波</th><th>高斯</th><th>高斯 + DRAG</th></tr>'
        f'{rows}</table>'
        '<div class="box" style="margin-top:4mm"><p>把九個數字畫成長條圖（橫軸：形狀與閘長度，縱軸：0 到 −60 dB，往下畫）</p>'
        '<div class="bars"></div>'
        '<p class="note">作品名稱：＿＿＿＿＿＿＿＿＿＿　我發現：脈衝越＿＿＿越漏；最漏的形狀是＿＿＿＿；DRAG 在 f₁₂ ＿＿＿＿＿＿。</p></div>',
        '<h2>故障卡</h2><p class="lead">沿虛線剪開。爸爸抽卡、只念「故障」；維修員寫下診斷與處方，再照驗證方法到動畫確認。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>虛擬 Z 省時間練習</h2><p class="lead">練習假設：每個閘若用真的脈衝做，都要 40 ns；改成虛擬 Z 就是 0 ns。</p>'
        '<table class="ct"><tr><th>順序</th><th>閘</th><th>只改相位嗎？</th><th>原本（ns）</th><th>改虛擬 Z 後（ns）</th></tr>'
        f'{ct}<tr><td colspan="3"><b>合計</b></td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:4mm"><p>1. 省下＿＿＿＿ ns，是原本的＿＿＿＿%。</p><div class="line"></div>'
        '<p>2. 動畫驗證（面積 90°）：送脈衝 → 虛擬 Z → 送脈衝，箭頭停在＿＿＿＿，P(1)＝＿＿＿；只送兩次脈衝呢？＿＿＿＿</p><div class="line"></div>'
        '<p>3. 為什麼虛擬 Z 不能刪？</p><div class="line"></div></div>',
        '<h2>說明卡：我的洩漏對照圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. DRAG 與虛擬 Z 在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：DRAG 在 f₁₂ 挖洞，快速脈衝也少漏</li><li>不看稿說出：虛擬 Z 只改後面脈衝的相位，0 ns</li>'
        '<li>示範：90°、虛擬 Z、90° 和 90°、90° 結果不同</li><li>指出限制：transmon 不是完美二能階，f₁₂ 只低約 200–300 MHz</li>'
        '<li>替洩漏對照圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q053 DRAG 與虛擬 Z 列印包', '父子科技學院 量子電腦學程 Q053｜DRAG 與虛擬 Z', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q053-drag-virtual-z', folder='Q053_DRAG與虛擬Z', files=FILES,
        sheet=('03_洩漏對照表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_DRAG與虛擬Z.pdf', pack_pages=4,
        pack_needles=('洩漏對照圖', '故障卡', '虛擬 Z 省時間練習', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q053', episode_dir='specials/q053-drag-virtual-z',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'leak_lab.py', 'faultCards': [a for a, *_ in CARDS],
               'leakageFrom': 'slides/QC_Operation_Talk.pptx p21', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q053/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

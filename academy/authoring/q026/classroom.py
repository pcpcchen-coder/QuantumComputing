"""Q026 課堂教材：洗衣板觀察紀錄（往上推）、往回調紀錄與彈珠實驗、遲滯解釋工作單、說明卡（列印）、解答、washboard_sim.py、動畫導覽。

不需要帳號，也不需要安裝套件（washboard_sim.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#washboard。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q026/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q026：傾斜洗衣板（電阻電容分路接面模型，和動畫 index.html#washboard 同一條方程式）。

不用安裝任何套件，只要 Python 3。執行：  python washboard_sim.py
- 方程式（無因次）：相位粒子的加速度 = I − sin φ − (速度)/Q
  I 是偏壓電流（以臨界電流 Ic 為單位）；Q 是品質因子，摩擦越小 Q 越大；動畫預設 Q = 8。
- 平均電壓（以 Ic·R 為單位）= 平均速度 ÷ Q；和動畫右下角小圖的橫軸相同。
- 先把電流一格一格往上加（0 → 1.3），再一格一格往回調（1.3 → 0）；
  每一格都從上一格結束時的狀態接著跑，所以會記得「之前發生過什麼」。
- 和動畫不同的地方：這裡沒有加隨機雜訊，每一格跑得夠久才取平均，結果每次都一樣。
- 參考：學程簡報 JJ_Microwave_Readout_Talk p16；animations/js/scenes/05_washboard.js；維基百科 Phase qubit、Josephson effect。
"""
import math

Q = 8.0          # 品質因子（動畫預設值）
DT = 0.01        # 每一步的時間（無因次）
SETTLE = 300.0   # 每一格先跑這麼久，讓小球安定下來
AVG = 200.0      # 再跑這麼久，取平均速度


def run_step(i_bias, phi, v, q=Q):
    """在固定電流下跑一段時間，回傳 (平均電壓, 結束時的 φ, 結束時的速度)。"""
    for _ in range(int(SETTLE / DT)):
        v += (i_bias - math.sin(phi) - v / q) * DT
        phi += v * DT
    start, n = phi, int(AVG / DT)
    for _ in range(n):
        v += (i_bias - math.sin(phi) - v / q) * DT
        phi += v * DT
    return (phi - start) / AVG / q, phi, v


def sweep(q=Q, top=1.3, step=0.01):
    ups = [round(k * step, 2) for k in range(int(round(top / step)) + 1)]
    downs = ups[::-1][1:]
    phi, v, rows = 0.0, 0.0, []
    for direction, currents in (('上升', ups), ('下降', downs)):
        for i_bias in currents:
            volt, phi, v = run_step(i_bias, phi, v, q)
            rows.append((direction, i_bias, volt))
    return rows


def thresholds(rows):
    up = [i for d, i, volt in rows if d == '上升' and volt > 0.02]
    down = [i for d, i, volt in rows if d == '下降' and volt > 0.02]
    return min(up), min(down)


ROWS = sweep()
ESCAPE, RETRAP = thresholds(ROWS)
SHOW = {0.0, 0.3, 0.5, 0.9, 0.99, 1.0, 1.01, 1.1, 1.3, 0.2, 0.17, 0.16, 0.15, 0.1}
print(f'品質因子 Q = {Q:g}（摩擦越小 Q 越大）')
print('方向   電流 I/Ic   平均電壓 ⟨V⟩/IcR   狀態')
for d, i_bias, volt in ROWS:
    if round(i_bias, 2) in SHOW:
        print(f'{d}   {i_bias:8.2f}   {volt:14.3f}      {"電壓態" if volt > 0.02 else "零電壓態"}')
print()
print(f'往上加：電流到 {ESCAPE:.2f} 才滑出山谷（臨界電流是 1）')
print(f'往回調：電流降到 {RETRAP:.2f} 還在滑，再低一格才停下（回捕電流）')
print(f'動畫小圖寫的估計值 4/(πQ) = {4 / (math.pi * Q):.2f}')
print()
print('摩擦變大（Q 變小）時，停下來的電流：')
for q in (2.0, 4.0, 8.0, 16.0):
    e, r = thresholds(sweep(q, step=0.01))
    print(f'  Q = {q:4.1f}：滑出 {e:.2f}、往回調時最後還在滑的電流 {r:.2f}（估計值 4/(πQ) = {min(1.0, 4 / (math.pi * q)):.2f}）')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'washboard_sim.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
_V = {(d, round(i, 2)): v for d, i, v in R['ROWS']}
# 製作代理實跑（Python 3）：往上加到 1.00 才滑出；往回調時 0.16 還在滑、0.15 停下（和動畫小圖的估計值 4/(πQ) = 0.16 一致）
assert R['ESCAPE'] == 1.0 and R['RETRAP'] == 0.16
assert _V[('上升', 0.5)] < 0.02 and _V[('下降', 0.5)] > 0.4      # 同樣是 0.5：上去時零電壓態、下來時電壓態
assert _V[('下降', 0.15)] < 0.02

UP = ['0.30', '0.50', '0.70', '0.80', '0.85', '0.90', '0.95', '1.00', '1.10']
DOWN = ['1.10', '0.80', '0.50', '0.30', '0.20', '0.18', '0.16', '0.14', '0.10']

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q026：傾斜洗衣板（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂用「相位粒子在傾斜洗衣板上滾」來看真實的約瑟夫森接面（電阻電容分路接面模型，RCSJ）：
電容像質量、電阻的倒數像摩擦、偏壓電流決定洗衣板多斜。電流超過臨界電流 Ic，山谷消失、相位一直跑，接面出現電壓；電流往回調時，小球要降到很低的電流（回捕電流）才停下——這就是遲滯。
下一堂 Q027 看 SQUID：用磁場轉頻率。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 洗衣板模型、零電壓態與電壓態、遲滯、電流電壓曲線；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 在 index.html#washboard 一格一格推偏壓電流，記錄小球何時滑出；用彈珠與波浪紙板模擬 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：把電流推過 1 再慢慢往回調，記下停住的電流，解釋為什麼不在同一點停（遲滯） | 列印包第 2、3 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替觀察紀錄取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 一台有瀏覽器的電腦、鉛筆、兩色筆、尺。
- 波浪紙板（瓦楞紙板撕掉一面，露出波浪；或把厚紙折成連續的波浪）、一顆彈珠、幾本書（用來把紙板一端墊高）、捲尺。
- 列印 `02_列印包_洗衣板觀察.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#washboard`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `washboard_sim.py`（不需要安裝套件），看看沒有雜訊時的往上、往回兩趟數字。

## 驗收重點

1. 完成「洗衣板觀察紀錄」：往上推的每一格、往回調的每一格，都記下電流與狀態；圈出滑出的那一格和停下的那一格。
2. 不看稿說出核心原理：電容像質量、電阻的倒數像摩擦、偏壓電流像傾斜；電流超過臨界電流，山谷消失、相位一直跑、出現電壓；往回調時小球停不下來，要降到回捕電流才被接住。
3. 指出至少一個注意事項：相位粒子是數學上的類比，接面裡沒有一顆真的球在跑。

## 誠實說明

- 動畫和 `washboard_sim.py` 用的是無因次的模型（電流以 Ic 為單位、電壓以 Ic·R 為單位、品質因子預設 8），不是某一顆真實接面的量測。
- 動畫有加一點隨機雜訊，所以每次停下來的電流可能差一兩格；`washboard_sim.py` 沒有雜訊，每次結果一樣。
- 動畫的「掃描」按鈕約 14 秒跑完一趟，太快了：右下角曲線往回時，要到電流降到零之後才回到縱軸。想量回捕電流，請手動慢慢往回調（每一格停幾秒）。
- 彈珠實驗只能模擬「傾斜到某個程度會滾出凹槽」；真實接面沒有重力，彈珠的摩擦也和電阻不一樣——讓孩子自己找出差異。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：一格一格推偏壓電流（約 40 分鐘）

1. 用瀏覽器開 `index.html#washboard`，左邊面板往下捲，找到「偏壓電流 I / Ic（傾斜）」滑桿（預設 0.30）和下面的讀數。
2. 爸爸推滑桿（點滑桿後用鍵盤方向鍵微調，每按一下 0.01；不要一下子拉很多，小球會被晃出去），依序停在列印包第 1 頁的每一格，每一格停 3 秒。
3. 孩子記下：小球旁邊「位障 ΔU」的數字、讀數第一行是「零電壓態」還是「電壓態」、小球還在山谷裡還是滑走了。圈出小球滑出去的那一格。
4. 按「重設」或重新整理頁面，再做一次，看看滑出的那一格是不是一樣。
5. 也可以按「掃描：0 → 1.3 → 0（看遲滯）」，看右下角小圖畫出一整圈的曲線。
6. 彈珠實驗：把波浪紙板平放，彈珠放在一個凹槽裡；用書把紙板一端慢慢墊高，量下彈珠滾出第一個凹槽時墊了幾公分，做三次，記在列印包第 2 頁。

## 下半場：孩子改造——解釋遲滯（約 30 分鐘）

1. 先把偏壓電流推到 1.10，讓小球滑走（讀數變成電壓態）。
2. 依列印包第 2 頁的每一格慢慢往回調，每一格停 5 秒，記下讀數狀態和右下角金色圓點在斜虛線上還是縱軸上。圈出讀數變回零電壓態的那一格。
3. 比一比：滑出去的那一格和停下來的那一格差多少？同樣是 0.50，往上推和往回調時的狀態一樣嗎？
4. 用列印包第 3 頁寫一句話解釋，提示：速度、摩擦、山谷。
5. 加分題：把「品質因子 Q」滑桿改成 4 或 16（Q 越小，摩擦越大），先預測停下來的電流會變高還是變低，再做一次；也可以跑 `washboard_sim.py` 對答案。
''',

'washboard_sim.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## washboard_sim.py 實跑輸出（沒有雜訊；品質因子 8，和動畫預設相同）\n\n```\n' + RUN_LOG + '```\n\n'
  '## 往上推該看到什麼（動畫）\n\n'
  '- 電流 0.30：位障 1.15、零電壓態；0.50：0.68；0.70：0.31；0.80：0.17；0.90：0.06（電流越大，位障越矮）。讀數第二行的電漿頻率從 0.98 倍降到 0.66 倍（0.90 時）。\n'
  '- 一格一格慢慢推（每格 0.01、停 3 秒），讀數大約在 1.00 或 1.01 變成電壓態，也就是電流到臨界電流才滑出去；一下子拉太多，小球會被晃出山谷，提早滑出。\n'
  '- 超過 1 以後位障標籤消失（已經沒有山谷），讀數變成「電壓態」。\n\n'
  '## 往回調該看到什麼（動畫，每一格停 5 秒）\n\n'
  '- 1.10、0.80、0.50、0.30、0.20、0.18：都還是電壓態，金色圓點在斜虛線上；大約到 0.16 才變回零電壓態（停在哪一格可能差一兩格），圓點回到縱軸。'
  '動畫小圖右上角寫的估計值是「回捕電流 I_r ≈ 4Ic/πQ = 0.16 Ic」。\n'
  '- 同樣是 0.50：往上推時是零電壓態，往回調時是電壓態——結果要看之前發生過什麼。\n\n'
  '## 一句話解釋（範例）\n\n'
  '> 小球滑出去以後跑得很快，摩擦又小，電流降回 1 以下、山谷重新出現時，它的速度足夠衝過一個又一個山谷；'
  '要等傾斜小到推力抵不過摩擦、速度掉下來，才會被某個山谷接住，所以停下來的電流比滑出去的電流低很多。\n\n'
  '## 摩擦變大會怎樣\n\n'
  '- 品質因子 Q 越小（摩擦越大），小球越容易停下，停下來的電流越高：Q = 4 約 0.32、Q = 16 約 0.08（見上面程式輸出）；'
  'Q = 2 時往回調約 0.60 就停，遲滯小很多。\n\n'
  '## 彈珠和真的接面哪裡不一樣（參考答案）\n\n'
  '- 接面裡沒有真的球，「位置」是相位差、「速度」對應電壓；推動它的是電流，不是重力。\n'
  '- 彈珠的摩擦來自紙板和空氣，接面的「摩擦」來自並聯的電阻；彈珠會在凹槽裡滾來滾去，接面在低溫下山谷裡的能量還是一階一階的（量子化）。\n'
  '- 紙板的波浪不一定一樣高，真的洗衣板位能每一個山谷都一樣。\n\n'
  '## 常見問題\n\n'
  '- 為什麼相位一直跑就有電壓？約瑟夫森關係：電壓和相位變化的快慢成正比（V = (ħ/2e)·dφ/dt），相位停住，電壓就是零。\n'
  '- 這和量子電腦有什麼關係？早期的相位量子位元，把偏壓調到接近臨界電流，用山谷裡最低兩個能階當 0 和 1；現在主流的 transmon 不加偏壓，洗衣板是平的（學程簡報 p16）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。

## `index.html#washboard`（JJ 與微波讀取 3D 場景 5：RCSJ 模型：傾斜洗衣板位勢）

- 金色小球標著「相位粒子 φ」；洗衣板往右下傾斜，相機會跟著小球移動（可以用「相機跟隨相位粒子」開關關掉）。
- 左邊面板（往下捲）：滑桿「偏壓電流 I / Ic（傾斜）」0–1.6（預設 0.30）、「品質因子 Q（阻尼越小 Q 越大）」1–20（預設 8.0）；
  按鈕「掃描：0 → 1.3 → 0（看遲滯）」「重設」；讀數第一行「零電壓態」或「電壓態」，第二行電漿頻率 ω_p(I) 是 I = 0 時的幾倍。
- 小球右邊的標籤「位障 ΔU ≈ … E_J」是擋住小球的位障高度；電流超過 1 時消失。山谷裡的短線是量子化的能階（示意）。
- 右下角小圖「I–V 特性」：縱軸電流、橫軸平均電壓；金色虛線是兩條理論上的路（縱軸、斜線），金色圓點是現在的位置，青色曲線只在按「掃描」時畫。
- 小球滑走後跑得很快，相機追不上，小球常常跑到畫面右下方之外；這時看讀數和右下角小圖就好。
- 掃描約 14 秒跑完一趟；往回時曲線一直留在斜線右邊，要到電流降到零之後才回縱軸（平均電壓的反應比掃描慢）。量回捕電流請手動慢慢調。

## 之後的課

Q027「SQUID：用磁場轉頻率」會用 `index.html#squid`：兩個接面並聯成環，用磁通調整頻率。
''',
}

SHEET_HEADER = ['方向', '偏壓電流 I/Ic', '位障 ΔU（E_J）', '讀數狀態', '小球／圓點在哪']
SHEET_ROWS = [['往上推', c] for c in UP] + [['往回調', c] for c in DOWN]

EXTRA_CSS = '''table.rec td{height:11mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.grid{display:block;margin:2mm auto 0}.cap{font-size:10.5pt;color:#35506b;margin:1mm 0 0}'''


def _iv_grid():
    """電流電壓曲線草圖格：橫軸平均電壓 0–1.4、縱軸電流 0–1.4，畫出 1 的位置。"""
    W, H, L, B, T, Rt = 520, 300, 56, 40, 12, 16
    pw, ph = W - L - Rt, H - T - B
    s = [f'<svg class="grid" width="140mm" height="81mm" viewBox="0 0 {W} {H}" font-size="13" font-family="sans-serif">']
    for k in range(15):
        x = L + pw * k / 14
        y = T + ph - ph * k / 14
        w = 1.2 if k in (0, 10) else 0.5
        c = '#0b2540' if k in (0, 10) else '#b9c9d8'
        s.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{T + ph}" stroke="{c}" stroke-width="{w}"/>')
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L + pw}" y2="{y:.1f}" stroke="{c}" stroke-width="{w}"/>')
    for k, lab in ((0, '0'), (10, '1')):
        s.append(f'<text x="{L + pw * k / 14:.1f}" y="{T + ph + 16}" text-anchor="middle">{lab}</text>')
        s.append(f'<text x="{L - 6}" y="{T + ph - ph * k / 14 + 4:.1f}" text-anchor="end">{lab}</text>')
    s.append(f'<text x="{L + pw / 2}" y="{H - 6}" text-anchor="middle">平均電壓（×IcR）</text>')
    s.append(f'<text x="14" y="{T + ph / 2}" text-anchor="middle" transform="rotate(-90 14 {T + ph / 2})">電流（×Ic）</text></svg>')
    return ''.join(s)


def html():
    pages = [
        '<h2>洗衣板觀察紀錄：往上推</h2><p class="lead">打開 index.html#washboard，偏壓電流一格一格往上推，每一格停 3 秒再記。</p>'
        '<p>記錄的人：＿＿＿＿＿＿　推滑桿的人：＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>偏壓電流 I/Ic</th><th>位障 ΔU（E_J）</th><th>讀數狀態</th><th>小球在山谷裡？</th></tr>'
        + ''.join(f'<tr><td>{c}</td><td></td><td></td><td></td></tr>' for c in UP) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>小球在哪一格滑出去？＿＿＿＿　再做一次是同一格嗎？＿＿＿＿</p>'
        '<p>電流越大，位障怎麼變？</p><div class="line"></div></div>',
        '<h2>往回調紀錄與彈珠實驗</h2><p class="lead">先推到 1.10 讓小球滑走，再一格一格往回調，每一格停 5 秒。</p>'
        '<table class="rec"><tr><th>偏壓電流 I/Ic</th><th>讀數狀態</th><th>金色圓點：斜虛線或縱軸</th></tr>'
        + ''.join(f'<tr><td>{c}</td><td></td><td></td></tr>' for c in DOWN) + '</table>'
        '<div class="box" style="margin-top:3mm"><h3>彈珠與波浪紙板</h3>'
        '<p>彈珠滾出第一個凹槽時，紙板一端墊高：第一次＿＿＿ 公分　第二次＿＿＿ 公分　第三次＿＿＿ 公分</p>'
        '<p>彈珠滾出去以後，把紙板放低一點，它會停在下一個凹槽嗎？</p><div class="line"></div></div>',
        '<h2>遲滯解釋工作單</h2><p class="lead">為什麼電流往回調時，小球不會在滑出去的那一點停下來？</p>'
        '<div class="box"><h3>一、比一比</h3><p>滑出去的電流：＿＿＿＿　停下來的電流：＿＿＿＿　同樣 0.50，往上是＿＿＿＿態，往回是＿＿＿＿態</p>'
        '<h3>二、畫出電流電壓曲線（往上一種顏色、往回另一種顏色）</h3>' + _iv_grid() +
        '<h3>三、我的一句話解釋（用上：速度、摩擦、山谷）</h3><div class="line"></div><div class="line"></div>'
        '<h3>四、摩擦變大（品質因子 Q 變小），停下來的電流會變高還是變低？</h3><p>我的預測：＿＿＿＿　動畫實測（Q = ＿＿）：＿＿＿＿</p></div>',
        '<h2>說明卡：我的洗衣板觀察紀錄</h2><div class="box"><p>紀錄名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 傾斜洗衣板在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（怎麼推電流、怎麼記錄）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三個對照：電容、電阻、偏壓電流</li><li>說出零電壓態和電壓態差在哪裡</li>'
        '<li>說出電流超過臨界電流時會發生什麼事</li><li>用速度、摩擦、山谷解釋遲滯</li>'
        '<li>指出一個注意事項：相位粒子只是數學上的類比</li><li>替觀察紀錄取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q026 洗衣板觀察 列印包', '父子科技學院 量子電腦學程 Q026｜傾斜洗衣板', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q026-tilted-washboard', folder='Q026_傾斜洗衣板', files=FILES,
        sheet=('03_洗衣板觀察紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_洗衣板觀察.pdf', pack_pages=4,
        pack_needles=('洗衣板觀察紀錄', '往回調紀錄', '遲滯解釋工作單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q026', episode_dir='specials/q026-tilted-washboard',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（washboard_sim.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'washboard_sim.py',
               'recordedRun': {'Q': R['Q'], 'escape_Ic': R['ESCAPE'], 'lowest_running_on_way_down_Ic': R['RETRAP'],
                               'V_up_0.5': round(_V[('上升', 0.5)], 3), 'V_down_0.5': round(_V[('下降', 0.5)], 3)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q026/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

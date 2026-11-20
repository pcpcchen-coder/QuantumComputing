"""Q025 課堂教材：比值掃描記錄表、掃描圖方格紙、折衷點工作單、說明卡（列印）、解答、ejec_scan.py、動畫導覽。

不需要帳號，也不需要安裝套件（ejec_scan.py 只要 Python 3）；動畫用瀏覽器開啟 animations/transmon-3d.html#capacitor 與 animations/index.html#potential。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q025/classroom.py
"""
from pathlib import Path
import contextlib
import io
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = '''"""父子科技學院 量子電腦學程 Q025：E_J／E_C 掃描（和動畫 transmon-3d.html#capacitor 同一套算法）。

不用安裝任何套件，只要 Python 3。執行：  python ejec_scan.py
- 約瑟夫森能量 E_J/h 固定 15 GHz；充電能量 E_C/h = 19.37 GHz ÷ 電容（fF）（e²/2hC）。
- 能量公式 H = 4E_C(n − n_g)² − E_J cos φ 寫成電荷基底的三對角矩陣，用二分法求最低三個能階；
  在背景電荷 n_g = 0 與 0.5 各算一次（和動畫的 capStats 一樣）：
  非諧性 α 取兩點的平均，電荷色散 = 兩點的 f01 相差多少。
- 參考：學程簡報 JJ_Microwave_Readout_Talk p15、p19；transmon.pptx p15；維基百科 Transmon。
"""
EJ = 15.0             # GHz（約瑟夫森能量 E_J/h，動畫的設定）
EC_PER_FF = 19.37     # GHz·fF（E_C/h = 19.37 / C）


def levels(ej, ec, ng, k=3, n_max=25):
    """電荷基底 H 的最低 k 個能階（單位 GHz），Sturm 序列二分法。"""
    d = [4 * ec * (n - ng) ** 2 for n in range(-n_max, n_max + 1)]
    e2 = (ej / 2) ** 2

    def count(x):
        q = d[0] - x
        c = 1 if q < 0 else 0
        for di in d[1:]:
            q = di - x - e2 / (q if q != 0 else 1e-300)
            if q < 0:
                c += 1
        return c

    out = []
    for j in range(k):
        lo, hi = -ej - 1, 4 * ec * (n_max + 1) ** 2 + ej + 1
        for _ in range(90):
            m = (lo + hi) / 2
            if count(m) > j:
                hi = m
            else:
                lo = m
        out.append((lo + hi) / 2)
    return out


def stats(c_ff):
    ec = EC_PER_FF / c_ff
    a, b = levels(EJ, ec, 0.0), levels(EJ, ec, 0.5)
    fa, fb = a[1] - a[0], b[1] - b[0]
    alpha = ((a[2] - 2 * a[1] + a[0]) + (b[2] - 2 * b[1] + b[0])) / 2
    return {'C': c_ff, 'EC': ec, 'ratio': EJ / ec, 'f01': (fa + fb) / 2, 'alpha': alpha, 'disp': abs(fa - fb)}


def fix(x, d):
    """像 JavaScript 的 toFixed：剛好在一半時進位（Python 的 format 會取偶數）。"""
    from decimal import Decimal, ROUND_HALF_UP
    return str(Decimal(x).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def hz(g):
    """GHz → 好讀的單位（和動畫的 fmtF 寫法一樣）。"""
    v = g * 1e9
    if v >= 1e9:
        return fix(g, 2) + ' GHz'
    if v >= 1e6:
        return fix(v / 1e6, 0 if v >= 1e8 else 1) + ' MHz'
    if v >= 1e3:
        return fix(v / 1e3, 1) + ' kHz'
    return '< 0.1 Hz' if v < 0.1 else fix(v, 1) + ' Hz'


def verdict(r):
    if r < 20:
        return '電荷雜訊主導'
    return 'transmon 區間' if r <= 120 else '非諧性偏小，閘需放慢'


SCAN = [10, 20, 30, 50, 77.5, 100, 150, 200]
ROWS = [stats(c) for c in SCAN]
print('電容      E_C        E_J/E_C   f01         非諧性 α     電荷色散     判斷')
for s in ROWS:
    print(f"{s['C']:6.1f} fF  {hz(s['EC']):>9}  {s['ratio']:6.1f}   {hz(s['f01']):>9}   −{hz(abs(s['alpha'])):>9}   "
          f"{hz(s['disp']):>10}   {verdict(s['ratio'])}")

print()
print('折衷點的例子：非諧性至少 200 MHz、電荷色散低於 10 kHz')
ALL = [stats(c / 2) for c in range(10, 401)]          # 5–200 fF，每 0.5 fF（和動畫滑桿一樣）
OK = [s['C'] for s in ALL if abs(s['alpha']) >= 0.2 and s['disp'] < 1e-5]
LOW, HIGH = min(OK), max(OK)
print(f'  兩條都符合的電容：{LOW} – {HIGH} fF（比值 {stats(LOW)["ratio"]:.1f} – {stats(HIGH)["ratio"]:.1f}）')
print('  電容再小：電荷色散超過 10 kHz；電容再大：非諧性不到 200 MHz。')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'ejec_scan.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
_S = {s['C']: s for s in R['ROWS']}
# 製作代理實跑（Python 3）：與動畫 transmon-3d.html#capacitor 的讀數（Node 以頁面程式實算）及旁白、動畫段相同
assert round(_S[77.5]['ratio'], 1) == 60.0 and round(_S[77.5]['alpha'] * 1000) == -283 and round(_S[77.5]['disp'] * 1e6, 1) == 1.9
assert round(_S[200]['ratio'], 1) == 154.9 and round(_S[200]['alpha'] * 1000) == -104 and _S[200]['disp'] * 1e9 < 0.1
assert round(_S[20]['ratio'], 1) == 15.5 and round(_S[20]['alpha'], 2) == -1.33 and round(_S[20]['disp'] * 1000, 1) == 53.1
assert (R['LOW'], R['HIGH']) == (66.0, 107.0)

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q025：E_J 與 E_C：兩個能量尺度（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂認識描述超導量子位元的兩個能量：約瑟夫森能量 E_J（位能井有多深）和充電能量 E_C（多放一顆電子到電容上的靜電能）。
重點是：E_J／E_C 比值決定量子位元的性格；比值加大時，電荷色散指數下降，非諧性只慢慢變小，所以比值越大不是越好。下一堂 Q026 看傾斜洗衣板。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 兩個能量、比值、背景電荷與電荷色散；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 在 transmon-3d 拉電容滑桿掃描比值，記錄非諧性與電荷色散，畫掃描圖 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：訂兩條標準，圈出範圍，挑一個折衷點並說明理由 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替掃描圖取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 一台有瀏覽器的電腦（平板也可以，但滑桿較難拉準）、鉛筆、兩色筆、尺。
- 列印 `02_列印包_比值掃描.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `transmon-3d.html#capacitor` 和 `index.html#potential`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `ejec_scan.py`（不需要安裝套件），對照動畫的讀數。

## 驗收重點

1. 完成「E_J／E_C 掃描圖」：橫軸是比值，畫出非諧性與電荷色散兩條線（電荷色散用每格乘以十的刻度）。
2. 不看稿說出核心原理：E_J 是位能井的深度、E_C 是多放一顆電子的靜電能；比值小怕背景電荷，比值大能階幾乎不隨背景電荷變；電荷色散指數下降、非諧性只慢慢變小。
3. 指出至少一個注意事項：E_J／E_C 越大不是越好；非諧性會跟著變小，脈衝要放慢，閘也變慢。

## 誠實說明

- 動畫與 `ejec_scan.py` 把 E_J/h 固定在 15 GHz，只改電容；真實晶片的 E_J 和電容都會依設計改變。
- 「非諧性至少 200 MHz、電荷色散低於 10 kHz」只是練習用的標準，不是業界規格；孩子可以自己訂、說出理由就好。
- 「山谷和粒子」「粒子越重越不怕晃」是學程簡報的力學類比，不是嚴格的物理描述。
- 臨界電流 30 nA ≈ 15 GHz、80 fF ≈ 240 MHz 是學程簡報的典型值，不是某一顆晶片的量測。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：掃描比值、畫掃描圖（約 40 分鐘）

1. 用瀏覽器開 `transmon-3d.html#capacitor`，會直接打開第 1 章「大十字電容的作用」分頁。右邊面板往下捲，找到「C_Σ」滑桿和下面的讀數。
2. 爸爸拉滑桿（也可以點滑桿後用鍵盤方向鍵微調，每按一下 0.5 fF），依序停在 10、20、30、50、77.5、100、150、200 fF。
3. 孩子把每一格的「E_J/E_C」「非諧性 α」「電荷色散」「判斷」抄進列印包第 1 頁。
4. 在列印包第 2 頁畫掃描圖：橫軸是比值（每格乘以十），一條線畫非諧性（取絕對值，MHz）、一條線畫電荷色散（kHz，每格乘以十）。電荷色散小於 0.1 Hz 的格子，畫在最下面並標「< 0.1 Hz」。
5. 一起看 `index.html#potential`：按下排的「CPB：E_J/E_C = 1」「10」「Transmon：50」，看右下角小圖三條線從起伏到拉平。
6. 填列印包第 1 頁下面的問題：比值從 10 到 60，哪一個數字變得比較多？

## 下半場：孩子改造——找折衷點（約 30 分鐘）

1. 用列印包第 3 頁。先訂兩條標準（例如非諧性至少 200 MHz、電荷色散低於 10 kHz），各寫一句為什麼。
2. 在掃描圖上用兩色筆圈出兩條標準都符合的範圍。
3. 挑一個點（可以回到動畫把滑桿拉到那裡），寫下：放棄了什麼、換到了什麼。
4. 加分題：跑 `ejec_scan.py`，看看程式算出的範圍和你圈的一不一樣。
''',

'ejec_scan.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## ejec_scan.py 實跑輸出（和動畫 transmon-3d.html#capacitor 的讀數相同）\n\n```\n' + RUN_LOG + '```\n\n'
  '## 掃描圖該看出什麼\n\n'
  '- 電荷色散：電容從 10 fF 到 200 fF（比值 7.7 → 154.9），從 940 MHz 一路掉到小於 0.1 Hz，少了九個零以上——這是「指數下降」。\n'
  '- 非諧性：從 −2.44 GHz（10 fF）、−1.33 GHz（20 fF）慢慢變成 −104 MHz（200 fF）；比值加大，非諧性一直變小，但只少了二十幾倍，比電荷色散慢得多。\n'
  '- 學程簡報（transmon.pptx p15，E_C 固定 250 MHz、改 E_J）：比值 10 → 60，電荷色散 62.8 MHz → 1.9 kHz（約 3 萬倍），非諧性只從 −353 變成 −283 MHz（少兩成）。\n\n'
  '## 暫停題：電容一直加大到無限大，會變成什麼？\n\n'
  '- 充電能量 E_C 趨近零，非諧性（約 −E_C）也趨近零：能階又變成等距的梯子，也就是 Q022 的量子諧振子。'
  '一道對準 0→1 的微波會一路往上推，挑不出兩個能階。所以電容不是越大越好。\n\n'
  '## 折衷點範例\n\n'
  '> 我訂的標準是非諧性至少 200 MHz（脈衝才不會漏到第三階）、電荷色散低於 10 kHz（背景電荷影響很小）。'
  '兩條都符合的電容是 66–107 fF。我選 77.5 fF：比值 60，非諧性 −283 MHz，電荷色散 1.9 kHz。'
  '我放棄了一些非諧性（電容 26 fF、比值約 20 時有 −970 MHz），換到電荷色散小了好幾千倍。\n\n'
  '## 常見問題\n\n'
  '- E_J、E_C 為什麼用 GHz、MHz 當單位？能量除以普朗克常數就是頻率，量子電路習慣用頻率來說能量。\n'
  '- 背景電荷從哪裡來？晶片基板和介面裡會隨機跳動的電荷，沒辦法完全消除（學程簡報 p19）。\n'
  '- 電荷量子位元和主流設計差在哪？同一條能量公式，唯一的差別是 E_J／E_C 比值（維基百科 Transmon）；主流設計在接面旁並聯一塊大電容，把比值拉到 50–100。\n'
  '- 為什麼非諧性太小，閘就要放慢？1→2 的頻率太靠近 0→1，脈衝越短頻譜越寬，越容易碰到 1→2、漏到更高的能階（transmon-3d 第 3 章）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。

## `transmon-3d.html#capacitor`（Transmon 3D 第 1 章：大十字電容的作用）

- 中間的十字金屬板就是並聯的大電容；拉「C_Σ」滑桿（5–200 fF），十字板會跟著變粗或變細（只是示意大小，未按比例）。
- 讀數：電容 C_Σ、充電能 E_C/h、E_J/E_C、f₀₁、非諧性 α、電荷色散、判斷（E_J/h 固定 15 GHz）。
  - 77.5 fF（預設）：250 MHz、60.0、5.21 GHz、−283 MHz、1.9 kHz、transmon 區間。
  - 200 fF：96.8 MHz、154.9、3.31 GHz、−104 MHz、< 0.1 Hz、非諧性偏小，閘需放慢。
  - 20 fF：969 MHz、15.5、9.69 GHz、−1.33 GHz、53.1 MHz、電荷雜訊主導（接近 Cooper pair box）。
- 「回到 77.5 fF」按鈕回到預設值。

## `index.html#potential`（JJ 與微波讀取 3D 場景 4：能階與非諧性）

- 打開時是 JJ／Transmon 模式、E_J/E_C = 50。左邊面板下排三顆按鈕「CPB：E_J/E_C = 1」「10」「Transmon：50」。
- 右下角小圖「電荷色散：能階隨背景電荷 n_g 的變化」：藍、紅、綠三條線是最低三個能階。
  - 比值 1：藍線和紅線上下起伏（紅線超出上緣的部分被截平）。
  - 比值 10：藍線和紅線幾乎拉平，綠線還有一點彎。
  - 比值 50：三條都是平的直線。
- 面板讀數的非諧性只算背景電荷 0 的那一點（比值 10 時 −637 MHz），和 transmon-3d、學程簡報取兩點平均的數字不同，比較時要注意。

## 之後的課

Q026「傾斜洗衣板」會用 `index.html#washboard` 看相位粒子在洗衣板位勢裡怎麼滑出井。
''',
}

SHEET_HEADER = ['電容 C_Σ（fF）', 'E_J/E_C', '非諧性 α', '電荷色散', '判斷']
SHEET_ROWS = [[str(c)] for c in R['SCAN']]

EXTRA_CSS = '''table.rec td{height:13mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.grid{display:block;margin:2mm auto 0}.cap{font-size:10.5pt;color:#35506b;margin:1mm 0 0}'''


def _grid():
    """掃描圖方格紙：橫軸比值 1–1000（每格乘以十），左軸電荷色散 0.1 Hz–1 GHz（每格乘以十）。"""
    W, H, L, B, T, Rt = 640, 560, 70, 50, 16, 20
    pw, ph = W - L - Rt, H - T - B
    s = [f'<svg class="grid" width="170mm" height="149mm" viewBox="0 0 {W} {H}" font-size="13" font-family="sans-serif">']
    for k in range(4):  # 比值 1, 10, 100, 1000
        x0 = L + pw * k / 3
        s.append(f'<line x1="{x0:.1f}" y1="{T}" x2="{x0:.1f}" y2="{T + ph}" stroke="#0b2540" stroke-width="1.2"/>')
        s.append(f'<text x="{x0:.1f}" y="{T + ph + 18}" text-anchor="middle">{10 ** k}</text>')
        if k < 3:
            for m in range(2, 10):
                x = x0 + pw / 3 * math.log10(m)
                s.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{T + ph}" stroke="#b9c9d8" stroke-width="0.6"/>')
    labels = ['0.1 Hz', '1 Hz', '10 Hz', '100 Hz', '1 kHz', '10 kHz', '100 kHz', '1 MHz', '10 MHz', '100 MHz', '1 GHz']
    for k, lab in enumerate(labels):
        y = T + ph - ph * k / (len(labels) - 1)
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L + pw}" y2="{y:.1f}" stroke="#7f9bb3" stroke-width="0.8"/>')
        s.append(f'<text x="{L - 6}" y="{y + 4:.1f}" text-anchor="end">{lab}</text>')
    s.append(f'<text x="{L + pw / 2}" y="{H - 8}" text-anchor="middle">E_J／E_C（每格乘以十）</text></svg>')
    return ''.join(s)


def html():
    pages = [
        '<h2>比值掃描記錄表</h2><p class="lead">打開 transmon-3d.html#capacitor，把 C_Σ 滑桿停在每一格，抄下讀數（E_J/h 固定 15 GHz）。</p>'
        '<p>記錄的人：＿＿＿＿＿＿　拉滑桿的人：＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<table class="rec"><tr>' + ''.join(f'<th>{h}</th>' for h in SHEET_HEADER) + '</tr>'
        + ''.join(f'<tr><td>{c}</td><td></td><td></td><td></td><td></td></tr>' for c in R['SCAN']) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>比值從 10 附近到 60 附近，非諧性和電荷色散，哪一個變得比較多？</p><div class="line"></div></div>',
        '<h2>E_J／E_C 掃描圖</h2><p class="lead">橫軸是比值，縱軸每一格乘以十。用一色筆畫電荷色散，另一色筆把非諧性（MHz）寫在每個點旁邊。</p>'
        + _grid() + '<p class="cap">電荷色散小於 0.1 Hz 的點畫在最下面那條線上，標「&lt; 0.1 Hz」。</p>',
        '<h2>折衷點工作單</h2><p class="lead">非諧性要夠大、電荷色散要夠小——兩個目標互相拉扯，找一個說得出理由的點。</p>'
        '<div class="box"><h3>一、我的兩條標準</h3><p>非諧性至少：＿＿＿＿ MHz，因為</p><div class="line"></div>'
        '<p>電荷色散低於：＿＿＿＿ kHz，因為</p><div class="line"></div>'
        '<h3>二、兩條都符合的範圍</h3><p>電容：＿＿＿＿ fF 到 ＿＿＿＿ fF（比值 ＿＿＿＿ 到 ＿＿＿＿）</p>'
        '<h3>三、我選的折衷點</h3><p>電容 ＿＿＿＿ fF、比值 ＿＿＿＿、非諧性 ＿＿＿＿、電荷色散 ＿＿＿＿</p>'
        '<p>我放棄了：</p><div class="line"></div><p>我換到了：</p><div class="line"></div></div>',
        '<h2>說明卡：我的比值掃描圖</h2><div class="box"><p>掃描圖名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. E_J 與 E_C：兩個能量尺度在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（怎麼掃描、怎麼畫）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出 E_J：位能井有多深</li><li>不看稿說出 E_C：多放一顆電子的靜電能</li>'
        '<li>說出比值小和比值大的量子位元有什麼不同</li><li>說出電荷色散急速下降、非諧性慢慢變小</li>'
        '<li>指出一個注意事項：比值越大不是越好</li><li>替掃描圖取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q025 比值掃描 列印包', '父子科技學院 量子電腦學程 Q025｜E_J 與 E_C：兩個能量尺度', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q025-ej-ec-two-energy-scales', folder='Q025_EJ與EC兩個能量尺度', files=FILES,
        sheet=('03_比值掃描紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_比值掃描.pdf', pack_pages=4,
        pack_needles=('比值掃描記錄表', '掃描圖', '折衷點工作單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q025', episode_dir='specials/q025-ej-ec-two-energy-scales',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（ejec_scan.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'ejec_scan.py',
               'recordedRun': {str(c): {'ratio': round(_S[c]['ratio'], 1), 'alpha_MHz': round(_S[c]['alpha'] * 1000, 1),
                                        'dispersion_Hz': round(_S[c]['disp'] * 1e9, 3)} for c in R['SCAN']} | {
                               'compromise_fF': [R['LOW'], R['HIGH']]},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q025/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

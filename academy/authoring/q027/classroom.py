"""Q027 課堂教材：調頻闖關記錄表、調頻曲線方格紙、對稱與不對稱比較工作單、說明卡（列印）、解答、squid_tuning.py、動畫導覽。

不需要帳號，也不需要安裝套件（squid_tuning.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#squid 與 animations/transmon-3d.html#case。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q027/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q027：SQUID 調頻曲線（和動畫 index.html#squid 同一套算法）。

不用安裝任何套件，只要 Python 3。執行：  python squid_tuning.py
- 兩個接面合起來的約瑟夫森能量 E_JΣ/h = 20 GHz，充電能量 E_C/h = 0.25 GHz（動畫的設定）。
- E_J(Φ) = E_JΣ × √(cos²(πΦ/Φ₀) + d² sin²(πΦ/Φ₀))，d 是接面不對稱度（0 = 兩個接面一樣）。
- 頻率 f01 ≈ √(8 E_J E_C) − E_C；磁通敏感度 = 頻率對磁通的斜率（和動畫一樣用 ±0.001 Φ₀ 的差分）。
- 參考：學程簡報 JJ_Microwave_Readout_Talk p17；docs/超導量子電腦師生對話教學紀錄.md 第 1–3 課。
"""
import math

EJS = 20.0     # GHz
EC = 0.25      # GHz


def f01(phi, d=0.0):
    c, s = math.cos(math.pi * phi), math.sin(math.pi * phi)
    ej = EJS * math.sqrt(c * c + d * d * s * s)
    return math.sqrt(8 * ej * EC) - EC


def shown(phi, d=0.0):
    """動畫讀數顯示的頻率（負的顯示成 0）。"""
    return max(0.0, f01(phi, d))


def slope(phi, d=0.0):
    return (f01(phi + 1e-3, d) - f01(phi - 1e-3, d)) / 2e-3


print('一、調頻曲線（對稱 d = 0 與不對稱 d = 0.6）')
print('磁通 Φ/Φ₀   f01（d=0）  斜率（d=0）   f01（d=0.6）  斜率（d=0.6）')
TABLE = [round(k * 0.05, 2) for k in range(11)]
for p in TABLE:
    print(f'  {p:5.2f}     {shown(p):6.3f} GHz  {slope(p):7.2f}      {shown(p, 0.6):6.3f} GHz  {slope(p, 0.6):7.2f}')

print()
print('二、闖關：滑桿每格 0.005 Φ₀，找最接近目標的格子（誤差要在 ±0.05 GHz 以內）')
GRID = [round(k * 0.005, 3) for k in range(101)]          # 0 ~ 0.5
TARGETS = [6.0, 5.5, 5.0, 4.5, 4.0]
QUEST = {}
for t in TARGETS:
    best = min(GRID, key=lambda p: abs(shown(p) - t))
    QUEST[t] = (best, shown(best))
    ok = '過關' if abs(shown(best) - t) <= 0.05 else '差太多'
    print(f'  目標 {t:.1f} GHz → 磁通 {best:.3f} Φ₀，頻率 {shown(best):.3f} GHz（差 {abs(shown(best) - t) * 1000:.0f} MHz，{ok}）')

print()
print('三、甜蜜點與雜訊')
NOISE0 = (f01(0) - f01(0.01)) * 1000
NOISE25 = (f01(0.25) - f01(0.26)) * 1000
DROP002 = (f01(0) - f01(0.02)) * 1000
print(f'  磁通 0 的斜率 = {slope(0):.2f}（甜蜜點）；0.25 的斜率 = {slope(0.25):.2f} GHz/Φ₀')
print(f'  同樣抖 0.01 Φ₀：在 0 頻率差 {NOISE0:.1f} MHz，在 0.25 差 {NOISE25:.0f} MHz（約 {NOISE25 / NOISE0:.0f} 倍）')
print(f'  從 0 拉到 0.02 Φ₀：頻率還是降了 {DROP002:.1f} MHz（一階不敏感，不是完全不動）')

print()
print('四、調頻範圍（最高 Φ = 0，最低 Φ = 0.5）')
RANGE = {}
for d in (0.0, 0.3, 0.6, 0.8):
    hi, lo = shown(0, d), shown(0.5, d)
    RANGE[d] = (hi, lo)
    print(f'  d = {d:.1f}：{hi:.3f} → {lo:.3f} GHz，範圍 {hi - lo:.3f} GHz；Φ = 0.25 的斜率 {slope(0.25, d):.2f}')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'squid_tuning.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
_f, _s = R['shown'], R['slope']
# 製作代理實跑（Python 3）：與動畫 index.html#squid 的讀數（Node 以場景公式實算）、旁白、動畫段相同
assert f'{_f(0):.3f}' == '6.075' and f'{_f(0.25):.3f}' == '5.068' and f'{_f(0.1):.3f}' == '5.918' and f'{_f(0.19):.3f}' == '5.502'
assert f'{_f(0.02):.3f}' == '6.068' and f'{_s(0.02):.2f}' == '-0.62' and f'{_s(0.25):.2f}' == '-8.35' and f'{_s(0):.2f}' == '0.00'
assert f'{_f(0.25, 0.6):.3f}' == '5.493' and f'{_s(0.25, 0.6):.2f}' == '-4.25' and f'{_f(0.5, 0.6):.3f}' == '4.649'
assert round(R['NOISE0'], 1) == 1.6 and round(R['NOISE25']) == 86 and round(R['DROP002']) == 6
assert R['QUEST'][5.5] == (0.19, _f(0.19))
assert all(abs(f - t) <= 0.05 for t, (_, f) in R['QUEST'].items())

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q027：SQUID：用磁場轉頻率（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂認識超導量子干涉元件（SQUID）：兩個約瑟夫森接面並聯成環，穿過環的磁通會改變等效的約瑟夫森能量 E_J，
量子位元的頻率就跟著變（每隔一個磁通量子 Φ₀ 重複一次）。調頻曲線最高的地方叫甜蜜點，斜率為零，對磁通雜訊一階不敏感。下一堂 Q028 做量子位元家族圖鑑。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 兩個接面成環、兩條路的干涉、磁通 → E_J → 頻率、甜蜜點；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 調頻闖關：爸爸出題、孩子拉滑桿，記點畫調頻曲線，找甜蜜點 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：比較對稱與不對稱 SQUID 的調頻範圍 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替調頻曲線取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 一台有瀏覽器的電腦（平板也可以，但滑桿較難拉準）、鉛筆、兩色筆、尺。
- 列印 `02_列印包_調頻闖關.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#squid`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `squid_tuning.py`（不需要安裝套件），對照動畫的讀數。

## 驗收重點

1. 完成「調頻曲線」：橫軸是磁通（0 到 0.5 Φ₀），縱軸是頻率，至少五個闖關點連成一條線，標出甜蜜點。
2. 不看稿說出核心原理：兩路超導電流在環裡干涉，磁通改變臨界電流與 E_J；頻率 f₀₁ ≈ √(8E_J E_C) − E_C 跟著變；Φ = 0 頻率最高，只能往下調。
3. 指出至少一個注意事項：可調 = 多一個雜訊入口；甜蜜點是一階不敏感，不是完全不受影響（偏 0.02 Φ₀ 頻率仍降約 6 MHz）。

## 誠實說明

- 動畫與 `squid_tuning.py` 的 E_JΣ/h = 20 GHz、E_C/h = 250 MHz 是示意設定，不是某一顆晶片的量測。
- 「兩個一樣的接面在半個磁通量子臨界電流變成零」是理想對稱的情況；真實的兩個接面不可能完全一樣。
- 動畫讀數在對稱（d = 0）、Φ = 0.5 時也會顯示斜率 0.00 和甜蜜點字樣：那裡頻率已掉到零、曲線是尖點，是數值計算的假象，不是真的甜蜜點。
- 闖關的「±0.05 GHz」只是遊戲規則，不是業界規格。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：調頻闖關、畫調頻曲線（約 40 分鐘）

1. 用瀏覽器開 `index.html#squid`。左邊面板往下捲，找到「外加磁通 Φ / Φ₀」滑桿和下面的讀數；右下角小圖是頻率對磁通的曲線，青色點是現在的位置。
2. 爸爸出題：從列印包第 1 頁挑一個目標頻率（6.0、5.5、5.0、4.5、4.0 GHz），也可以自己出 4–6 GHz 之間的題目。
3. 孩子拉滑桿（也可以點滑桿後用鍵盤方向鍵微調，每按一下 0.005 Φ₀），讓讀數粗體的頻率落在目標 ±0.05 GHz 以內就過關，記下磁通、頻率和磁通敏感度。
4. 在列印包第 2 頁把每一關的點畫上去，連成調頻曲線。
5. 找甜蜜點：把磁通拉回 0，讀數最下面會寫「甜蜜點：對磁通雜訊一階免疫」；在曲線上圈出來。
6. 比一比：把磁通拉到 0.02，頻率還會不會變？（會，從 6.075 降到 6.068 GHz。）

## 下半場：孩子改造——對稱與不對稱（約 30 分鐘）

1. 用列印包第 3 頁。先在不對稱度 0（對稱）記下磁通 0、0.25、0.5 的頻率。
2. 把「接面不對稱度」滑桿拉到 0.3、0.6，再記一次；看小圖金色曲線（現在的設定）和灰色曲線（對稱時）差在哪裡。
3. 算調頻範圍（最高減最低），比較 Φ = 0.25 的磁通敏感度。
4. 寫一句話：不對稱的環放棄了什麼、換到了什麼。
5. 加分題：跑 `squid_tuning.py`，看看 d = 0.8 時範圍剩多少。
''',

'squid_tuning.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## squid_tuning.py 實跑輸出（和動畫 index.html#squid 的讀數相同）\n\n```\n' + RUN_LOG + '```\n\n'
  '## 調頻曲線該看出什麼\n\n'
  '- Φ = 0 頻率最高（6.075 GHz），斜率是 0：這就是甜蜜點。往兩邊拉，頻率都往下掉，所以只能往下調。\n'
  '- 對稱（d = 0）時，Φ = 0.5 頻率掉到 0；整條曲線每隔 1 Φ₀ 重複一次（動畫滑桿可以拉到 −1～1 看）。\n'
  '- 越靠近 0.5，曲線越陡：同樣抖一點磁通，頻率抖得越多。\n\n'
  '## 暫停題：一定要停在甜蜜點以外，怎麼讓它比較不怕磁通雜訊？\n\n'
  '- 用不對稱的 SQUID（兩個接面做得不一樣大）：調頻範圍變小，但整條曲線比較平。d = 0.6 時 Φ = 0.25 的斜率從 −8.35 變成 −4.25 GHz/Φ₀。'
  '不對稱的環在 Φ = 0.5 的谷底還有第二個斜率為零的點（動畫讀數也會寫甜蜜點）。\n\n'
  '## 改造範例\n\n'
  '> 對稱的環可以從 6.075 GHz 一路調到 0，範圍最大，但在 0.25 附近斜率 −8.35，很怕磁通雜訊。'
  '不對稱度 0.6 時最低只到 4.649 GHz，範圍剩 1.43 GHz，可是同一個位置的斜率只剩 −4.25。我放棄了調頻範圍，換到比較穩。\n\n'
  '## 常見問題\n\n'
  '- 磁通怎麼來？晶片上每顆可調位元旁邊有一條 Z 控制線，通一點電流就產生穿過小環的磁通（學程簡報 p17）。\n'
  '- 為什麼頻率要調？把兩顆位元調到共振做雙量子位元閘、避開有缺陷的頻率、給每顆位元不同的頻率地址（transmon-3d 第 6 章）。\n'
  '- 甜蜜點是不是完全不受雜訊影響？不是。斜率為零只代表「一階」不敏感；從 0 拉到 0.02 Φ₀，頻率還是降了約 6 MHz。\n'
  '- 為什麼說可調是多一個雜訊入口？固定頻率的位元沒有這條磁通線；多了能調頻的旋鈕，磁通雜訊也就能讓頻率抖動，相位慢慢亂掉。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。

## `index.html#squid`（JJ 與微波讀取 3D 場景 6：DC SQUID）

- 銀色的鋁環上夾兩個橘色接面（JJ₁、JJ₂），下方是金色的 Z 控制線；青色箭頭是穿過環的磁通，環中央寫著目前的 Φ。
- 左邊面板：「外加磁通 Φ / Φ₀」滑桿（−1～1，打開時在 0.25）、「接面不對稱度 d」滑桿（0～0.8）、「自動掃描磁通」按鈕。
- 讀數：等效 E_J/h、粗體的頻率 f₀₁、磁通敏感度 df/dΦ；斜率接近 0 時會加上「甜蜜點：對磁通雜訊一階免疫」。
  - 磁通 0：6.075 GHz、斜率 0.00（甜蜜點）。
  - 磁通 0.25：5.068 GHz、斜率 −8.35；不對稱度 0.6 時 5.493 GHz、斜率 −4.25。
- 右下小圖：灰色線是對稱時的曲線，金色線是目前不對稱度的曲線（對稱時兩條重疊），青色點是目前位置，「甜蜜點」標在最高點。

## `transmon-3d.html#case`（Transmon 3D 第 6 章：三顆可調 transmon 的頻率配置）

- 自動播放的步驟動畫，左上方會跳出字幕。步驟 ②「SQUID 調頻」說明 Z 線磁通讓頻率往下調、離開甜蜜點會抖動；步驟 ③「頻率配置」把 Q2 留在甜蜜點、Q1 和 Q3 調到不同頻率。
- 步驟 ⑥ 可以自己拖三條 Z 線的磁通，看頻率怎麼互相碰撞。

## 之後的課

Q028「量子位元家族圖鑑」會比較 transmon、fluxonium、電荷與相位量子位元的結構與優缺點。
''',
}

SHEET_HEADER = ['目標頻率（GHz）', '磁通 Φ/Φ₀', '頻率 f₀₁（GHz）', '磁通敏感度', '過關？']
SHEET_ROWS = [[f'{t:.1f}'] for t in R['TARGETS']] + [['自己出題'], ['自己出題']]

EXTRA_CSS = '''table.rec td{height:13mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.grid{display:block;margin:2mm auto 0}.cap{font-size:10.5pt;color:#35506b;margin:1mm 0 0}'''


def _grid():
    """調頻曲線方格紙：橫軸磁通 0–0.5 Φ₀（每格 0.05），縱軸頻率 0–6.5 GHz（每格 0.5）。"""
    W, H, L, B, T, Rt = 640, 560, 70, 50, 16, 20
    pw, ph = W - L - Rt, H - T - B
    s = [f'<svg class="grid" width="170mm" height="149mm" viewBox="0 0 {W} {H}" font-size="13" font-family="sans-serif">']
    for k in range(11):
        x = L + pw * k / 10
        s.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{T + ph}" stroke="{"#0b2540" if k % 2 == 0 else "#b9c9d8"}" stroke-width="{1.2 if k % 2 == 0 else 0.6}"/>')
        if k % 2 == 0:
            s.append(f'<text x="{x:.1f}" y="{T + ph + 18}" text-anchor="middle">{k * 0.05:.1f}</text>')
    for k in range(14):
        y = T + ph - ph * k / 13
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L + pw}" y2="{y:.1f}" stroke="{"#7f9bb3" if k % 2 == 0 else "#d3dde7"}" stroke-width="0.8"/>')
        if k % 2 == 0:
            s.append(f'<text x="{L - 6}" y="{y + 4:.1f}" text-anchor="end">{k * 0.5:.0f} GHz</text>')
    s.append(f'<text x="{L + pw / 2}" y="{H - 8}" text-anchor="middle">外加磁通 Φ / Φ₀</text></svg>')
    return ''.join(s)


def html():
    pages = [
        '<h2>調頻闖關記錄表</h2><p class="lead">打開 index.html#squid，拉「外加磁通」滑桿，讓頻率落在目標 ±0.05 GHz 以內就過關。</p>'
        '<p>出題的人：＿＿＿＿＿＿　拉滑桿的人：＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<table class="rec"><tr>' + ''.join(f'<th>{h}</th>' for h in SHEET_HEADER) + '</tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>磁通拉回 0 時，讀數寫了什麼？那裡的磁通敏感度是多少？</p><div class="line"></div></div>',
        '<h2>調頻曲線</h2><p class="lead">把每一關的（磁通, 頻率）畫成點，連成曲線；用另一色筆圈出甜蜜點。</p>'
        + _grid() + '<p class="cap">提示：頻率最高的地方在磁通 0；越靠近 0.5，曲線越陡。</p>',
        '<h2>對稱與不對稱比較工作單</h2><p class="lead">拉「接面不對稱度」滑桿，比較調頻範圍和磁通敏感度。</p>'
        '<table class="rec"><tr><th>不對稱度 d</th><th>Φ = 0 的頻率</th><th>Φ = 0.25 的頻率</th><th>Φ = 0.5 的頻率</th><th>範圍（最高 − 最低）</th><th>Φ = 0.25 的敏感度</th></tr>'
        + ''.join(f'<tr><td>{d}</td><td></td><td></td><td></td><td></td><td></td></tr>' for d in ('0', '0.3', '0.6')) + '</table>'
        '<div class="box" style="margin-top:4mm"><p>小圖裡金色曲線和灰色曲線差在哪裡？</p><div class="line"></div>'
        '<p>不對稱的環放棄了：</p><div class="line"></div><p>換到了：</p><div class="line"></div>'
        '<p>如果你是工程師，會選哪一種？為什麼？</p><div class="line"></div></div>',
        '<h2>說明卡：我的調頻曲線</h2><div class="box"><p>調頻曲線名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. SQUID：用磁場轉頻率在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（怎麼闖關、怎麼畫）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：兩個接面並聯成環，磁通讓兩路電流干涉</li><li>說出磁通 → E_J → 頻率，而且只能往下調</li>'
        '<li>說出甜蜜點在哪裡、斜率為什麼是零</li><li>說出不對稱的環範圍變小、比較不怕雜訊</li>'
        '<li>指出一個注意事項：可調 = 多一個雜訊入口</li><li>替調頻曲線取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q027 調頻闖關 列印包', '父子科技學院 量子電腦學程 Q027｜SQUID：用磁場轉頻率', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q027-squid-flux-tuning', folder='Q027_SQUID用磁場轉頻率', files=FILES,
        sheet=('03_調頻闖關紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_調頻闖關.pdf', pack_pages=4,
        pack_needles=('調頻闖關記錄表', '調頻曲線', '對稱與不對稱比較工作單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q027', episode_dir='specials/q027-squid-flux-tuning',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（squid_tuning.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'squid_tuning.py',
               'recordedRun': {'quest': {f'{t:.1f}': {'flux': p, 'f01_GHz': round(f, 3)} for t, (p, f) in R['QUEST'].items()},
                               'noise_MHz': {'at0': round(R['NOISE0'], 2), 'at0.25': round(R['NOISE25'], 1)},
                               'drop_0_to_0.02_MHz': round(R['DROP002'], 2),
                               'range_GHz': {f'{d:.1f}': [round(hi, 3), round(lo, 3)] for d, (hi, lo) in R['RANGE'].items()}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q027/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

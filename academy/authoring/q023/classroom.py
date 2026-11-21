"""Q023 課堂教材：模型標註清單、標註貼紙與相位時鐘（列印）、三十秒說明稿紙、說明卡、解答、tunnel_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（tunnel_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#jj。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q023/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q023：約瑟夫森接面的三個數字小實驗。

不用安裝任何套件，只要 Python 3。執行：  python tunnel_check.py
一、直流約瑟夫森效應  I = Ic sin φ（學程簡報 JJ_Microwave_Readout_Talk p13）
二、交流約瑟夫森效應  f = (2e/h) V，約 483.6 GHz/mV（同上；維基百科 Josephson voltage standard）
三、穿隧和厚度：穿過去的比例隨厚度「指數」變小（維基百科 Quantum tunnelling）
    這裡的 1 % 只是好算的例子，不是真實氧化鋁的數值。
"""
from math import sin, asin, radians, degrees

E = 1.602176634e-19   # 基本電荷（庫侖，SI 定義值）
H = 6.62607015e-34    # 普朗克常數（焦耳·秒，SI 定義值）
IC_NA = 40            # 臨界電流的例子（nA）：簡報的典型值是 20–60 nA

print('一、直流效應：I = Ic sin φ（Ic =', IC_NA, 'nA）')
DC = {}
for deg in (0, 30, 60, 78.5, 90):
    DC[deg] = IC_NA * sin(radians(deg))
    print(f'  相位差 {deg:5.1f} 度  →  電流 {DC[deg]:5.1f} nA')
PHASE = {r: degrees(asin(r)) for r in (0.5, 0.98)}
print('  反過來：電流是 0.5 Ic → 相位差', round(PHASE[0.5], 1), '度；0.98 Ic →', round(PHASE[0.98], 1), '度')
print('  電流想超過 Ic？sin φ 最大只有 1，相位差鎖不住，接面兩端就會出現電壓。')

print()
print('二、交流效應：f = (2e/h) × V')
KJ_GHZ_PER_MV = 2 * E / H / 1e9 / 1e3
print(f'  2e/h = {KJ_GHZ_PER_MV:.4f} GHz / mV')
AC = {}
for uv in (1, 10, 100, 1000):
    AC[uv] = KJ_GHZ_PER_MV * uv / 1000
    print(f'  電壓 {uv:5d} μV  →  電流振盪 {AC[uv]:9.4f} GHz')

print()
print('三、穿隧和厚度：假設 1 份厚度只讓 1 % 穿過去（好算的例子）')
P1 = 0.01
TUNNEL = {}
for n in (1, 2, 3):
    TUNNEL[n] = P1 ** n
    print(f'  厚度 {n} 份  →  穿過去 {TUNNEL[n] * 100:.4f} %')
print('  如果和厚度「成反比」，厚一倍會剩 0.5 %；實際是指數，只剩 0.01 %，小了五十倍。')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'tunnel_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、動畫段（三十度、約七十九度、四百八十三點六吉赫、厚一倍不是一半）相同
assert round(R['PHASE'][0.5], 1) == 30.0 and round(R['PHASE'][0.98]) == 79
assert round(R['KJ_GHZ_PER_MV'], 1) == 483.6 and round(R['DC'][30], 1) == 20.0
assert abs(R['TUNNEL'][2] - 1e-4) < 1e-12

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q023：約瑟夫森接面：超導三明治（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂認識約瑟夫森接面（JJ）：兩片超導體夾一層非常薄的絕緣體。
重點是三層結構、庫柏電子對整對穿隧（穿隧是波的性質，不是挖洞），以及直流與交流兩個約瑟夫森效應。下一堂 Q024 會看它為什麼像一個非線性電感。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三層結構、電子對穿隧、相位差、兩個效應；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 用兩片吐司夾一張薄紙做接面模型，貼上標註、畫相位時鐘 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：寫一段三十秒說明，解釋穿隧不是挖洞，計時修到剛好 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：結構與兩個效應 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替模型取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 兩片吐司（或兩片厚紙板、兩塊海綿）、一張影印紙或描圖紙、便利貼、膠帶、剪刀、彩色筆、碼錶（手機也可以）。用吐司的話，做完拍照記錄，吐司不要吃（貼過膠帶和便利貼）。
- 列印 `02_列印包_接面模型.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#jj`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `tunnel_check.py`（不需要安裝套件）。

## 驗收重點

1. 完成接面紙模型與標註：超導體（鋁）×2、絕緣層（氧化鋁，約 1–2 nm）、相位 φ₁、φ₂、相位差、一個模型的限制。
2. 不看稿說出核心原理：三層結構；庫柏電子對整對穿過薄絕緣層；不加電壓也有超電流（I = Ic sin φ）；加了電壓相位差一直轉、電流振盪（約 483.6 GHz/mV）。
3. 指出至少一個注意事項：絕緣層只有約 1–2 奈米（幾個原子層）；穿隧是波的性質，不是粒子在牆上打洞。

## 誠實說明

- 模型只表示三層的順序，不按比例；紙和吐司的厚度比和真實接面差很多。
- 「電子對踩同一個節拍」「相位像時鐘指針」是比喻：每一塊超導體可以用同一個相位描述。
- 接面面積（約 0.01–0.05 μm²）、臨界電流（約 20–60 nA）是學程簡報的典型值，不是某一顆晶片的量測。
- `tunnel_check.py` 第三部分的 1 % 只是好算的例子，用來說明「指數」和「成反比」的差別。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：做接面模型、貼標註（約 40 分鐘）

1. 爸爸把兩片吐司並排放好，中間夾一張薄紙，三層對齊：吐司｜紙｜吐司。這就是「超導｜絕緣｜超導」。
2. 孩子從列印包第 2 頁剪下標註：兩片吐司各貼「超導體（鋁）」，薄紙貼「絕緣層（氧化鋁，約 1–2 nm）」。
3. 在兩片吐司上各貼一個相位時鐘，用彩色筆畫指針：左邊指 12 點、右邊指 1 點（差 30 度），再貼上「相位 φ₁」「相位 φ₂」和「相位差 φ = φ₂ − φ₁」。
4. 貼一張「庫柏電子對（2e）」在左邊吐司，畫一條虛線箭頭穿過紙到右邊——提醒自己：這是波接上，紙上不會有洞。
5. 貼「模型的限制」：寫一句「紙太厚了，真正的絕緣層只有約 1–2 nm」。
6. 一起看 `index.html#jj`：按「I ≈ Ic」，金色字從 30° 變成約 79°；再按「I = 1.4 Ic（電壓態）」，右邊紅色的相位鐘一直轉。把右邊時鐘的指針改畫成 79 度差，說說看電流變大還是變小。
7. 拍照記錄，填列印包第 1 頁的檢核表。

## 下半場：孩子改造——三十秒說明（約 30 分鐘）

1. 用列印包第 3 頁。分三段寫：結構（指著模型說三層）、穿隧（用波說明）、限制（模型哪裡不像真的）。
2. 寫完用碼錶計時念一次，記下秒數。超過三十秒就刪字，不到就補一個例子，再念一次。
3. 在稿紙下面寫一句：「為什麼穿隧不是挖洞？」
4. 加分題：跑 `tunnel_check.py` 第三部分，說說看「厚一倍」為什麼不是剩一半。
''',

'tunnel_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 模型標註參考答案\n\n'
  '| 模型的部分 | 代表什麼 | 要說出的重點 |\n|---|---|---|\n'
  '| 左邊吐司 | 超導體（鋁），相位 φ₁ | 電子兩兩配成庫柏電子對，整塊共用一個相位 |\n'
  '| 中間薄紙 | 絕緣層（氧化鋁，約 1–2 nm） | 只有幾個原子層；夠薄，電子對才能穿隧 |\n'
  '| 右邊吐司 | 超導體（鋁），相位 φ₂ | 被絕緣層隔開，相位可以和左邊不同 |\n'
  '| 兩個時鐘的角度差 | 相位差 φ = φ₂ − φ₁ | 直流：I = Ic sin φ；交流：有電壓 V 時 φ 一直轉 |\n'
  '| 穿過紙的虛線箭頭 | 庫柏電子對穿隧（電荷 2e） | 是波接上，不是挖洞；紙完好如初 |\n'
  '| 模型的限制 | 不按比例 | 紙太厚了；真的絕緣層只有約 1–2 nm |\n\n'
  '## tunnel_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 暫停題：絕緣層變厚一倍，穿過去的電流會剛好變成一半嗎？\n\n'
  '- 不會，會小很多。波在絕緣層裡是「指數」變弱（維基百科 Quantum tunnelling；學程筆記 I_c ∝ e^(−2κd)）：'
  '如果 1 份厚度讓 1 % 穿過去，2 份厚度只剩 1 % 的 1 %，也就是 0.01 %；若是「成反比」會剩 0.5 %，差了五十倍。'
  '所以做接面時，氧化層厚度要控制得非常準。\n\n'
  '## 三十秒說明範例（約 120 字）\n\n'
  '> 約瑟夫森接面是一個超導三明治：兩片超導的鋁，中間夾一層只有一到兩奈米的氧化鋁。'
  '超導體裡的電子兩兩成對，電子對的波會滲進絕緣層，雖然越來越弱，但牆很薄，到另一邊還剩一點，兩邊的波就接上了，電子對就這樣過去。'
  '牆上沒有洞，也沒有被打破。我的模型用紙當絕緣層，但紙太厚了，真的絕緣層只有幾個原子層。\n\n'
  '## 常見問題\n\n'
  '- 絕緣體不是不導電嗎？厚的絕緣體幾乎不讓電流過；只有一到兩奈米時，波還沒弱到零就到了另一邊，所以有穿隧電流。\n'
  '- 不加電壓為什麼會有電流？直流約瑟夫森效應：超電流由相位差決定（I = Ic sin φ），不需要電壓去推。\n'
  '- 電壓有什麼用？交流約瑟夫森效應：有電壓時相位差一直轉，電流以 f = 2eV/h 振盪，每 1 mV 約 483.6 GHz；這個關係準到被各國當成電壓標準。\n'
  '- 動畫裡的電子對穿過去會閃一下，是真的嗎？那是動畫的示意；真正的穿隧是波函數重疊，看不到「一閃」。\n'
  '- 為什麼量子電腦需要它？下一堂 Q024：它像一個會隨電流改變的「非線性電感」，讓能階不再等距，才能只挑兩個能階當量子位元。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#jj` 會直接跳到這個場景。

## `index.html#jj`（JJ 與微波讀取 3D 場景 3：約瑟夫森接面的結構與穿隧）

- 左右兩塊銀色方塊是鋁電極（右邊畫成半透明）；中間橘紅色薄片是氧化鋁穿隧阻障，下方金色標籤「AlOx 穿隧阻障 ~1–2 nm」。
- 藍紫兩顆一組的小球是庫柏電子對，往右流，經過阻障時閃一下淡黃光（示意，不是真的看得到）。
- 上方兩個相位鐘：左藍右紅；中間金色大字是相位差與電流，例如「φ = φ₂ − φ₁ = 30°　I = Ic sin φ = 0.50 Ic」。
- 左邊面板下方：「偏壓電流 I / Ic」滑桿、三顆按鈕「I = 0.5 Ic（超電流）」「I ≈ Ic」「I = 1.4 Ic（電壓態）」和讀數框。
  - 0.5 Ic：相位差 30°，讀數「超電流態……電壓為零，能量不耗散」。
  - I ≈ Ic（0.98）：相位差約 79°（讀數 78.5°），右下小圖左半的青色點爬到正弦曲線接近頂端。
  - 1.4 Ic：右邊紅色相位鐘一直轉、金色字的角度一直變；讀數換成「電壓態……有耗散」；小圖右半的青色點落到電阻分支的斜線上。
- 拖曳可以旋轉、滾輪縮放；按 R 重設視角。

## 之後的課

Q024「JJ 是非線性電感」會用 `transmon-3d.html` 與 `lc-vs-jj.html#s5` 看電感怎麼隨電流改變。
''',
}

SHEET_HEADER = ['模型的部分', '代表什麼', '貼好了嗎（✓）', '我會怎麼解釋', '爸爸的評語']
SHEET_ROWS = [['左邊吐司'], ['中間薄紙'], ['右邊吐司'], ['兩個相位時鐘'], ['穿過紙的虛線箭頭'], ['模型的限制']]

EXTRA_CSS = '''table.rec td{height:16mm;font-size:10.5pt}table.rec th:first-child{width:36mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.stk{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.stk .cut{font-size:14pt;font-weight:700;text-align:center;padding:4mm 3mm}
.clocks{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:4mm;text-align:center}.clocks p{margin:1mm 0 0;font-size:12pt}
.script .line{height:10mm}'''


def _clock():
    ticks = ''.join(
        f'<line x1="50" y1="6" x2="50" y2="{14 if k % 3 == 0 else 10}" stroke="#0b2540" stroke-width="{2 if k % 3 == 0 else 1}" '
        f'transform="rotate({k * 30} 50 50)"/>' for k in range(12))
    return (f'<svg width="52mm" height="52mm" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="none" stroke="#0b2540" '
            f'stroke-width="2.5"/>{ticks}<circle cx="50" cy="50" r="2.5" fill="#0b2540"/></svg>')


def html():
    parts = [('左邊吐司', '超導體（鋁）・相位 φ₁'), ('中間薄紙', '絕緣層（氧化鋁，約 1–2 nm）'), ('右邊吐司', '超導體（鋁）・相位 φ₂'),
             ('兩個時鐘的角度差', '相位差 φ = φ₂ − φ₁'), ('穿過紙的虛線箭頭', '庫柏電子對穿隧（2e）'), ('模型的限制', '')]
    stickers = ['超導體（鋁）', '超導體（鋁）', '絕緣層（氧化鋁，約 1–2 nm）', '庫柏電子對（2e）',
                '相位 φ₁', '相位 φ₂', '相位差 φ = φ₂ − φ₁', '模型的限制：紙太厚了']
    pages = [
        '<h2>模型標註清單</h2><p class="lead">兩片吐司夾一張薄紙：超導｜絕緣｜超導。每一部分貼好標註，再寫你會怎麼解釋。</p>'
        '<p>模型名稱：＿＿＿＿＿＿＿＿＿＿＿＿　做的人：＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>模型的部分</th><th>代表什麼</th><th>貼好了</th><th>我會怎麼解釋</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td><td></td></tr>' for a, b in parts) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>動畫裡按「I ≈ Ic」後，相位差變成幾度？按「電壓態」後，相位鐘怎麼了？</p><div class="line"></div></div>',
        '<h2>標註貼紙與相位時鐘</h2><p class="lead">沿虛線剪下，貼在模型上；兩個時鐘自己畫指針，表示兩邊的相位。</p>'
        '<div class="stk">' + ''.join(f'<div class="cut">{s}</div>' for s in stickers) + '</div>'
        '<div class="clocks"><div>' + _clock() + '<p>相位 φ₁（左邊吐司）</p></div><div>' + _clock() + '<p>相位 φ₂（右邊吐司）</p></div></div>',
        '<h2>三十秒說明稿紙</h2><p class="lead">解釋「穿隧」不是挖洞穿過去。寫好後用碼錶計時，修到剛好三十秒。</p>'
        '<div class="box script"><h3>一、結構（指著模型說三層）</h3><div class="line"></div><div class="line"></div>'
        '<h3>二、穿隧（用波說明電子對怎麼過去）</h3><div class="line"></div><div class="line"></div><div class="line"></div>'
        '<h3>三、限制（模型哪裡不像真的）</h3><div class="line"></div><div class="line"></div></div>'
        '<table style="margin-top:4mm"><tr><th>念第幾次</th><th>秒數</th><th>改了什麼</th></tr>'
        '<tr><td>1</td><td></td><td></td></tr><tr><td>2</td><td></td><td></td></tr><tr><td>3</td><td></td><td></td></tr></table>',
        '<h2>說明卡：我的接面模型</h2><div class="box"><p>模型名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 約瑟夫森接面：超導三明治在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（模型怎麼做、怎麼標）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三層結構：超導｜絕緣｜超導</li><li>說出電子對怎麼過去（波接上，不是挖洞）</li>'
        '<li>說出直流效應：零電壓也有超電流</li><li>說出交流效應：有電壓，相位差一直轉</li>'
        '<li>指出一個注意事項：絕緣層只有約 1–2 nm</li><li>替模型取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q023 接面模型 列印包', '父子科技學院 量子電腦學程 Q023｜約瑟夫森接面：超導三明治', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q023-josephson-junction-sandwich', folder='Q023_約瑟夫森接面超導三明治', files=FILES,
        sheet=('03_模型標註檢核.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_接面模型.pdf', pack_pages=4,
        pack_needles=('模型標註清單', '標註貼紙', '三十秒說明稿紙', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q023', episode_dir='specials/q023-josephson-junction-sandwich',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（tunnel_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'tunnel_check.py',
               'recordedRun': {'phase_deg_at_0.5Ic': round(R['PHASE'][0.5], 1), 'phase_deg_at_0.98Ic': round(R['PHASE'][0.98], 1),
                               'dc_current_nA_at_30deg_Ic40': round(R['DC'][30], 2),
                               'ac_GHz_per_mV': round(R['KJ_GHZ_PER_MV'], 4),
                               'tunnel_fraction_1_2_3': [R['TUNNEL'][n] for n in (1, 2, 3)]},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q023/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

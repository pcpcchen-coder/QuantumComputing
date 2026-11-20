"""Q104 課堂教材：讀取八步驟卡（八關闖關）、可執行的重設計時程式 reset_timer.py、重設比較表、容易錯的地方、教爸爸檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#readout；程式只要 Python 3。
建置時會真的執行一次 reset_timer.py，確認輸出和影片、教材寫的數字一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q104/classroom.py
"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，結果固定（無亂數）
RUN_OUTPUT = '''T₁ = 100 μs
被動等待：等幾倍 T₁ → 每個 shot 多久、每秒幾個、還留在 |1⟩ 的比例
  等 1 T₁：   101.5 μs，每秒     9,852 個，殘留  36.79 %
  等 3 T₁：   301.5 μs，每秒     3,317 個，殘留   4.98 %
  等 5 T₁：   501.5 μs，每秒     1,994 個，殘留   0.67 %
  等 7 T₁：   701.5 μs，每秒     1,426 個，殘留   0.09 %
主動重設：2.97 μs，每秒 336,700 個
主動重設比等 5 T₁ 快 169 倍
'''
PASSIVE = [(1, '101.5', '9,852', '36.79'), (3, '301.5', '3,317', '4.98'), (5, '501.5', '1,994', '0.67'), (7, '701.5', '1,426', '0.09')]

PROGRAM = '''"""父子科技學院 量子電腦學程 Q104：讀完之後怎麼回到 |0⟩——被動等待 vs 主動重設（純 Python，不需要安裝任何套件）

執行：  python reset_timer.py
時間數值取自學程動畫 transmon-3d.html 第 5 章第 7 步的時間軸看板（示意值）。
"""
import math

T1 = 100.0          # 能量衰減時間 T₁（微秒，μs）
GATE = 0.5          # 跑一次線路的閘（μs）
READ = 1.0          # 讀取一次（μs）
DECIDE = 0.35       # FPGA 判斷（μs）
PI = 0.12           # π 脈衝：把 1 翻回 0（μs）
WAIT_T1 = 5         # 改造區：被動等待要等幾倍 T₁？（試試 1、3、5、7）


def passive(n):
    """被動等待：什麼都不做，等 n 倍 T₁。回傳 (每個 shot 的時間 μs, 還留在 |1⟩ 的比例)"""
    return GATE + READ + n * T1, math.exp(-n)


def active():
    """主動重設：讀取 → 判斷 → 是 1 就送 π 脈衝 → 再讀一次確認"""
    return GATE + READ + DECIDE + PI + READ


if __name__ == '__main__':
    print(f'T₁ = {T1:g} μs')
    print('被動等待：等幾倍 T₁ → 每個 shot 多久、每秒幾個、還留在 |1⟩ 的比例')
    for n in (1, 3, 5, 7):
        t, left = passive(n)
        print(f'  等 {n} T₁：{t:8.1f} μs，每秒 {1e6 / t:9,.0f} 個，殘留 {left * 100:6.2f} %')
    tp, _ = passive(WAIT_T1)
    ta = active()
    print(f'主動重設：{ta:.2f} μs，每秒 {1e6 / ta:,.0f} 個')
    print(f'主動重設比等 {WAIT_T1} T₁ 快 {tp / ta:.0f} 倍')
'''

# 八關（transmon-3d.html 第 5 章的八個步驟）：(關, 動畫步驟名, 參考關鍵字, 關主問題, 參考答案)
STAGES = [
    ('第 1 關', '為什麼間接讀', '敲鈴聽音高', '為什麼不直接量量子位元？',
     '一份激發只有約 22 μeV，沒有偵測器能直接數；直接取能量會把 |1⟩ 打回 |0⟩。'),
    ('第 2 關', '色散偏移', '腔頻率 ±χ', '位元在 |0⟩、|1⟩ 時，共振腔頻率往哪邊偏？',
     '|0⟩ 往下、|1⟩ 往上，各偏 χ ≈ 0.77 MHz，兩邊差約 1.5 MHz。'),
    ('第 3 關', '探測與 IQ', '中間探測、相位一正一負', '為什麼探測微波要放在兩個頻率中間？',
     '兩個狀態的振幅一樣、相位一正一負，差別最大；κ ≈ 2χ 時相位差 90°，IQ 上分得最開。'),
    ('第 4 關', '讀取鏈', '下去擋熱、上來放大', '輸入線和輸出線各要擋住什麼？',
     '輸入線分級衰減擋住室溫熱雜訊；輸出線用環行器／隔離器擋住放大器雜訊回灌，量子極限放大器只多約半個光子雜訊。'),
    ('第 5 關', '積分與判別', '兩團雲＋判別線', '積分時間為什麼不能太短，也不能太長？',
     '太短雜訊大、兩團重疊；太長 |1⟩ 可能在讀取途中衰減成 |0⟩。約 100–300 ns 可達 99% 以上。'),
    ('第 6 關', '反作用與 QND', '再量一樣、疊加塌縮', '量到 1 之後立刻再量，會得到什麼？疊加還在嗎？',
     '還是 1（QND）；但原本的疊加在第一次量的時候已經塌縮。'),
    ('第 7 關', '重設', '不降溫，回到 |0⟩', '讀完要重新降溫嗎？有哪幾種回到 |0⟩ 的方法？',
     '不用，冷凍機一直維持約 10 mK。被動等待（5 T₁ ≈ 0.5 ms）、主動重設（約 1–3 μs）、無條件重設（約 2 μs）。'),
    ('第 8 關', '自由實驗', '找最佳 τ', '拖動積分 τ，保真度怎麼變？',
     'τ 太短重疊變多、太長衰減變多，中間有一個最佳值；看面板「估計讀取保真度」。'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q104：第 6 課 色散讀取與重設（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：量子位元的狀態怎麼讀出來、讀完怎麼回到 |0⟩；課堂用「闖關（八關）」的方式，跟著 3D 動畫第 5 章的八個步驟走一遍。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#readout`（第 5 章）；加映 `index.html#dispersive`、`index.html#iq`。免安裝、不需帳號 |
| 程式 | `reset_timer.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_色散讀取與重設.pdf`（A4，共 4 頁）；印章或貼紙當過關章 |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「讀完要重新降溫嗎？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：間接讀取、色散偏移、探測與 IQ、讀取鏈、判別、QND | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 跟著第 5 章八步驟闖關，每步寫一個關鍵字（孩子是挑戰者、爸爸是關主） | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 比較被動重設和主動重設要花多久：跑程式、改等待倍數、填表 | `reset_timer.py`、列印包第 2 頁、`03_重設比較紀錄.csv` |
| 105–115 | 孩子教爸爸：操作與原理，指出一個限制 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結、替讀取八步驟卡命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `transmon-3d.html#readout`，取消「自動接續」，按步驟按鈕 1–8 各看一次；左上方字幕會跟著動畫說明。
- 跑一次 `python reset_timer.py`，確認最後一行是「主動重設比等 5 T₁ 快 169 倍」。
- 讀一遍 `04_解答.md`（八關參考關鍵字與關主問題答案）。

## 關主的原則

- 一關一個問題（列印包第 1 頁有建議題目）；答得出來才蓋章，答不出來就按「重播」再看一次，不算犯規。
- 關鍵字由孩子自己寫，可以和參考答案不一樣，只要說得出理由。
- 最重要的一句：QND（量子非破壞性）讀取不改變被量到的狀態，但會破壞疊加。

## 誠實說明

- 動畫與程式裡的 T₁ = 100 μs、各段時間（閘 0.5 μs、讀取 1 μs、判斷 0.35 μs、π 脈衝 0.12 μs）是示意值，真實機器各不相同。
- 「100–300 ns 做到 99% 以上」「量子極限放大器約多半個光子雜訊」等數字來自學程的師生對話紀錄，是常見量級，不代表特定機器。
- 動畫的 IQ 點是隨機抽樣，每次看到的點群與保真度數字會有一點不同。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：八關闖關（約 40 分鐘）

1. 用瀏覽器開 `animations/transmon-3d.html#readout`（第 5 章：色散讀取）。
2. 先取消「自動接續」，這樣每一步播完會停下來，不會自己跳到下一步。
3. 按步驟按鈕「1」開始。看完左上方字幕和右邊說明後，挑戰者在列印包第 1 頁那一關寫一個關鍵字。
4. 關主問那一關的問題（列印包上有建議題目）；答得出來就蓋章，再按「下一步 ▶」。
5. 卡住時按「重播」，同一步從頭再播一次。
6. 第 8 關（自由實驗）：準備選「|1⟩」→ 按「量測一次」→ 按「主動重設」；再選「|1⟩」→「量測一次」→「被動等待 5T₁」（慢動作）。拖動「積分 τ」滑桿，看「估計讀取保真度」怎麼變。

## 加映：另一個動畫（約 10 分鐘，可選）

- `animations/index.html#dispersive`：按「量子位元 |0⟩」「量子位元 |1⟩」看兩條曲線；把「色散位移 χ / κ」拉到 0.10 再拉回 0.50，看面板的相位差。
- `animations/index.html#iq`：關掉「量子極限放大器（JPA/TWPA）開啟」，看兩團雲變胖；再打開，把「T1」滑桿拉到 3，看紅點拖尾。

## 下半場：被動 vs 主動重設（約 30 分鐘）

1. 打開 `reset_timer.py`，找到最上面的數字（T1、GATE、READ、DECIDE、PI、WAIT_T1）。
2. 先在列印包第 2 頁寫預測：等 5 T₁ 每秒能跑幾個 shot？主動重設快幾倍？
3. 執行 `python reset_timer.py`，把輸出抄進表格。
4. 改造：把 `WAIT_T1` 改成 3 或 7、把 `T1` 改成 50 或 300，再跑一次；每次都先預測。
5. 想一想：等得越久殘留越少，但每秒能跑的次數也越少，你會選幾倍？
''',

'reset_timer.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 八關參考關鍵字與關主問題\n\n| 關 | 動畫步驟 | 參考關鍵字 | 關主問題 | 參考答案 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} |\n' for a, b, c, d, e in STAGES)
  + '\n## reset_timer.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- 被動等待：每多等 1 T₁，殘留在 |1⟩ 的比例乘上 e⁻¹ ≈ 0.37；等 5 T₁ 剩 e⁻⁵ ≈ 0.67%。\n'
  '- 主動重設的時間是固定流程：閘 0.5＋讀取 1＋判斷 0.35＋π 脈衝 0.12＋確認讀取 1 = 2.97 μs（量到 0 時其實不必送 π 脈衝，這裡一律算進去，取保守值）。\n'
  '- 主動重設的殘留誤差主要來自讀錯（判別錯誤），所以常讀兩次確認；動畫看板也列出第三種「無條件重設」（約 2 μs，不必先讀）。\n'
  '- 改造參考：T1 改成 300（WAIT_T1 = 5）→ 等 5 T₁ 要 1,501.5 μs，每秒約 666 個，主動重設快約 506 倍——位元越好（T₁ 越長），被動等待反而越慢。\n'
  '- 常見誤解：QND 讀取不改變被量到的狀態（量到 1 再量還是 1），但會破壞疊加（疊加態在量的那一刻塌縮）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `transmon-3d.html#readout`（第 5 章：色散讀取，八步驟）

- 步驟按鈕 1–8；「◀ 上一步」「暫停」「重播」「下一步 ▶」；「自動接續」核取方塊。
- 1 為什麼間接讀 → 2 色散偏移（青色 |0⟩、金色 |1⟩ 兩條曲線）→ 3 探測與 IQ → 4 讀取鏈看板 → 5 積分與判別（白色軌跡收斂、判別閾值）→ 6 反作用與 QND（連續量三次）→ 7 重設時間軸看板 → 8 自由實驗。
- 第 8 步按鈕：準備「|0⟩」「|1⟩」「疊加態」；「量測一次」「量測 20 次」「清除點」；「積分 τ」滑桿；「主動重設」「被動等待 5T₁」。

## `index.html#dispersive`（場景 9：色散讀取）

- 藍色 = 位元在 |0⟩、紅色 = |1⟩；金色直線是探測微波；右下是 IQ 平面小圖。
- 「色散位移 χ / κ」= 0.50 時（2χ = κ），面板顯示相位差 90°、「✓ 最佳」；拉到 0.10 時相位差只剩約 22.6°。

## `index.html#iq`（場景 10：IQ 判別）

- 每條細線是一次讀取，從上方 t = 0 落到平面；藍點製備 |0⟩、紅點製備 |1⟩；金色線是判別閾值；右下是沿判別軸的直方圖。
- 「量子極限放大器（JPA/TWPA）開啟」關掉：兩團變胖、保真度下降；「T1」滑桿拉小：紅點在讀取途中掉回 |0⟩，在兩團之間拖尾。

## 操作

滑鼠拖曳旋轉、滾輪縮放；index.html 按 H 隱藏面板、左右方向鍵換場景。
''',
}

SHEET_HEADER = ['實驗', 'T1（μs）', 'WAIT_T1（幾倍）', '我的預測', '每個 shot（μs）', '每秒幾個', '殘留在 |1⟩（%）', '主動重設快幾倍', '和預測一樣嗎']
SHEET_ROWS = ([['原本的程式', '100', '5'], ['改等待倍數', '100', '3'], ['改等待倍數', '100', '7'],
               ['改 T1', '50', '5'], ['改 T1', '300', '5'], ['自己選', '', '']])

EXTRA_CSS = '''.stages{display:grid;grid-template-columns:repeat(2,1fr);gap:3mm;margin-top:3mm}
.stage{border:1.2pt solid #0b2540;border-radius:3mm;padding:2.4mm 3mm;font-size:10.5pt;min-height:36mm;position:relative}
.stage b{font-size:11.5pt;color:#0b2540}.stage .q{color:#4a6a88;font-size:9.5pt;margin:1mm 0}
.stage .kw{border-bottom:1pt dashed #4a6a88;height:8mm;margin-top:1.5mm}.stage .stamp{position:absolute;right:3mm;top:2mm;font-size:10pt;color:#4a6a88}
table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 reset_timer.py（隔離模式），確認輸出和影片、教材寫的數字一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'reset_timer.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    stage = ''.join(f'<div class="stage"><span class="stamp">過關章 □</span><b>{a}｜{b}</b>'
                    f'<div class="q">關主問：{d}</div>我的關鍵字：<div class="kw"></div></div>' for a, b, c, d, e in STAGES)
    pages = [
        '<h2>讀取八步驟卡</h2><p class="lead">跟著 transmon-3d.html#readout 第 5 章，一步一關。先取消「自動接續」。</p>'
        '<p>開場先猜：讀完一次，要不要把冷凍機重新降溫？ □ 要　□ 不用　因為＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        f'<div class="stages">{stage}</div>',
        '<h2>換你改造：被動等待 vs 主動重設</h2><p class="lead">先預測，再跑 reset_timer.py，把輸出抄進表格。</p>'
        '<table class="rec"><tr><th>實驗</th><th>T1（μs）</th><th>等幾倍 T₁</th><th>我的預測</th><th>每秒幾個</th><th>殘留在 |1⟩</th><th>主動快幾倍</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<pre class="code">T1 = 100.0      # 能量衰減時間（μs）\nGATE = 0.5      # 閘\nREAD = 1.0      # 讀取一次\nDECIDE = 0.35   # FPGA 判斷\nPI = 0.12       # π 脈衝\nWAIT_T1 = 5     # 改造區：被動等待幾倍 T₁</pre>'
        '<p class="note">等得越久，殘留越少，但每秒能跑的次數也越少。你會選等幾倍？為什麼？＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>三個容易錯的地方</h2><div class="box"><ul class="chk">'
        '<li>讀完不必重新降溫：冷凍機一直維持約 10 mK，只要讓這顆位元回到 |0⟩</li>'
        '<li>兩團雲會有一點重疊：讀取本身就有錯誤率（約 100–300 ns 可達 99% 以上）</li>'
        '<li>讀取光子會讓位元頻率偏移：讀取會干擾疊加態</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>QND（量子非破壞性）量測</h3>'
        '<p>量到的狀態不會被改掉：量到 1，立刻再量還是＿＿。</p><p>但原本的疊加態：□ 還在　□ 已經塌縮</p>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>最後一關：教爸爸讀取</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 共振腔的「音高」怎麼透露位元的狀態？</p><div class="line"></div>'
        '<p>2. IQ 平面上的兩團雲，怎麼判成 0 或 1？</p><div class="line"></div>'
        '<p>3. 被動等待和主動重設，哪個快？快幾倍？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>不看稿說出讀取原理：音高偏移、探測、兩團雲、判別線</li><li>示範動畫第 5 章任一步，並解釋畫面</li>'
        '<li>說出兩種重設方式和大約的時間</li><li>指出一個限制：QND 也會讓疊加塌縮；讀取有錯誤率</li>'
        '<li>替讀取八步驟卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q104 色散讀取與重設 列印包', '父子科技學院 量子電腦學程 Q104｜第 6 課：色散讀取與重設', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q104-dispersive-readout', folder='Q104_色散讀取與重設', files=FILES,
        sheet=('03_重設比較紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_色散讀取與重設.pdf', pack_pages=4,
        pack_needles=('讀取八步驟卡', '第 8 關', '被動等待', '主動重設', '容易錯', 'QND', '最後一關'),
        authoring_dir=XINEW / 'authoring/q104', episode_dir='specials/q104-dispersive-readout',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；reset_timer.py 只需 Python 3）',
               'program': 'reset_timer.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'passive5T1_us': 501.5, 'passive5T1_perSec': 1994, 'active_us': 2.97, 'active_perSec': 336700, 'speedup': 169},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q104/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q038 課堂教材：讀取鏈接線圖（闖關卡）、熱光子計算表、分貝練習單、說明卡（列印）、解答、thermal_photons.py、動畫導覽。

不需要帳號，也不需要安裝套件（thermal_photons.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#fridge。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q038/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q038：熱光子計算小工具。

不用安裝任何套件，只要 Python 3。執行：  python thermal_photons.py
- 一、熱光子數 n_th = 1 / (e^(hf/kT) − 1)（玻色–愛因斯坦分布；學程簡報 JJ_Microwave_Readout_Talk p33 與動畫 index.html#fridge 的讀數用同一個式子）。
- 二、孩子的算法：只算從室溫灌下來的熱雜訊，每經過一個 −20 dB 衰減器就除以 100（簡報 p32：4 K、100 mK、10 mK 各 −20 dB）。
- 三、分貝換算：每 −10 dB 變成十分之一；+20 dB 是 100 倍、+40 dB 是 10000 倍。
- 四、加分題：把衰減器自己放出的熱雜訊也算進去（簡報 p33：「衰減器把訊號與上游雜訊一起壓低，但自身在冷端只貢獻該溫度的熱雜訊」）。
  這裡用常見的衰減器模型：n_out = n_in / A + (1 − 1/A) × n_th(衰減器所在溫度)，A 是衰減倍數（−20 dB → A = 100）。
"""
import math

H = 6.62607015e-34   # 普朗克常數（J·s）
KB = 1.380649e-23    # 波茲曼常數（J/K）
F = 7e9              # 讀取微波 7 GHz（簡報 p33）


def n_th(T, f=F):
    """溫度 T（K）下、頻率 f 的平均熱光子數。"""
    return 1 / math.expm1(H * f / (KB * T))


def db_to_ratio(db):
    """分貝 → 功率倍數。"""
    return 10 ** (db / 10)


print('一、7 GHz 的熱光子數')
NTH = {}
for name, T in (('300 K 室溫', 300), ('4 K', 4), ('100 mK', 0.1), ('10 mK', 0.01)):
    NTH[T] = n_th(T)
    print(f'  {name:8s}：{NTH[T]:.3g} 個')

print()
print('二、孩子的算法：從 890 個開始，每個 −20 dB 衰減器除以 100')
SIMPLE = [890.0]
for k in range(3):
    SIMPLE.append(SIMPLE[-1] / 100)
    print(f'  經過第 {k + 1} 個衰減器：{SIMPLE[-1]:g} 個')
print(f'  只放兩個衰減器：{SIMPLE[2]:g} 個，是千分之一的 {SIMPLE[2] / 0.001:.0f} 倍')

print()
print('三、分貝換算')
DB = {}
for db in (-10, -20, -40, -60, 20, 40):
    DB[db] = db_to_ratio(db)
    print(f'  {db:+d} dB → × {DB[db]:g}')
SIG = [('AWG（室溫）', -50), ('經過三個 −20 dB 衰減器', -50 - 60)]
for name, dbm in SIG:
    print(f'  {name}：{dbm} dBm')

print()
print('四、加分題：衰減器自己也會放出所在溫層的熱雜訊')
STAGES = [(4, 20), (0.1, 20), (0.01, 20)]
n = n_th(300)
FULL = [n]
for T, att in STAGES:
    A = db_to_ratio(att)
    n = n / A + (1 - 1 / A) * n_th(T)
    FULL.append(n)
    print(f'  經過 {T:g} K 的 −{att} dB 衰減器：{n:.3g} 個')
A60 = db_to_ratio(60)
ALL_ROOM = n_th(300) / A60 + (1 - 1 / A60) * n_th(300)
print(f'  對照：60 dB 全部放在 300 K：{ALL_ROOM:.4g} 個（一點都沒有變少）')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'thermal_photons.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()

# 製作代理實跑（Python 3）：與旁白、簡報 p33、動畫讀數一致
assert f"{R['NTH'][300]:.1f}" == '892.5' and f"{R['NTH'][0.01]:.1e}".endswith('e-15')
assert [f'{v:g}' for v in R['SIMPLE']] == ['890', '8.9', '0.089', '0.00089']
assert R['DB'][-60] == 1e-6 and R['DB'][40] == 1e4
assert f"{R['FULL'][1]:.3g}" == '20.2' and f"{R['FULL'][2]:.3g}" == '0.238' and f"{R['FULL'][3]:.2g}" == '0.0024'
assert abs(R['ALL_ROOM'] - R['NTH'][300]) < 1e-6

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q038：讀取鏈：衰減、環行器、放大器（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。上一堂我們學會把一個 IQ 點判成 0 或 1；這一堂沿著稀釋冷凍機走一趟讀取鏈：
輸入線往下，在 4 K、100 mK、10 mK 各放一個 −20 dB 衰減器，把室溫的熱雜訊壓下去；輸出線往上，先經過環行器／隔離器，
再用 10 mK 的量子極限放大器（JPA／TWPA）、4 K 的 HEMT（高電子遷移率電晶體放大器）、最後室溫放大器。
好玩機制是「闖關」：每個元件一關，說得出它的目的才過關。作品是「讀取鏈接線圖」。下一堂 Q039 是「讀取設計的取捨」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 溫層與兩條線、熱光子、層層衰減、分貝、環行器與放大器順序；看 3D 動畫 | 影片第 2–8 段、`05_動畫導覽.md` |
| 25–65 | 闖關：照 index.html#fridge 從室溫畫到 10 mK，再畫回來，每個元件說出目的 | 列印包第 1 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：算出 300 K 熱雜訊經過衰減後剩幾個熱光子 | 列印包第 2、3 頁、`thermal_photons.py` |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替讀取鏈接線圖取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_讀取鏈接線圖.pdf`（A4，共 4 頁）。另備彩色筆（建議藍色畫輸入線、橘色畫輸出線）、計算機或手機。
- 讀一遍 `04_解答.md`；想多了解可以讀學程筆記 `notes/dispersive-readout.md` 的 §3、§4。
- 下載學程的 `animations/` 資料夾，用瀏覽器先開一次 `index.html#fridge`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `thermal_photons.py`（不需要安裝套件）。

## 驗收重點

1. 完成「讀取鏈接線圖」：六個溫層、輸入線三個衰減器與濾波器、輸出線環行器與三級放大器，每個元件旁邊寫上目的。
2. 不看稿說出核心原理：輸入線層層衰減把熱雜訊壓下來；輸出線先用環行器擋住回來的雜訊，再先用量子極限放大器、後用 HEMT。
3. 指出至少一個注意事項：衰減不是浪費訊號，是把熱雜訊壓下來；訊號變弱，室溫端多給一點功率就好。

## 誠實說明

- 衰減器的配置照學程簡報 p32 與動畫（4 K、100 mK、10 mK 各 −20 dB）；學程筆記的例子是 4 K、Still、MXC（−20、−10、−20 dB）。實際配置依機器而異。
- 「890 個 → 0.00089 個」只算從室溫灌下來的那一份；衰減器自己也會放出所在溫層的熱雜訊，算進去會多一些（見解答的加分題）。
- 動畫的光球大小、光暈大小、右下小圖的功率數字都是示意，不是某台冷凍機的量測值。家裡沒有冷凍機可以量，不要編造量測數據。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：闖關畫讀取鏈接線圖（約 40 分鐘）

1. 用瀏覽器開 `animations/index.html#fridge`，左邊面板往下捲到底，看到讀數、「動畫速度」滑桿和「視角：整體」「放大混合腔」兩個按鈕。
2. 先一起認識畫面：左邊一排標籤是六個溫層（300 K 室溫頂板、50 K、4 K、Still ~0.8 K、Cold plate ~100 mK、Mixing chamber ~10 mK）；
   淡藍色光球是讀取脈衝，沿輸入線往下走，經過晶片後變成金色，沿輸出線往上走。把「動畫速度」調到 0.3× 比較好追。
3. 闖關規則：用列印包第 1 頁的接線圖，從最上面開始，跟著光球一個元件一個元件走。每到一個元件：
   - 孩子在接線圖的那一層畫出元件（輸入線畫在左欄、輸出線畫在右欄）；
   - 說出它的目的（例如「衰減器：把熱雜訊壓下去」「環行器：只讓訊號往上走，擋住回來的雜訊」）；
   - 爸爸覺得說對了，就在「過關」欄打勾，進下一關。
4. 按「放大混合腔」看最底下：低通／Eccosorb 濾波、樣品盒與磁屏蔽、環行器、TWPA／JPA。按「視角：整體」回來。
5. 全部過關後，在接線圖上標出每一層的溫度，以及衰減或放大了幾 dB。
6. 沒有電腦時，可以照影片和列印包第 1 頁旁邊的提示畫。

## 下半場：孩子改造——算出剩幾個熱光子（約 30 分鐘）

1. 用列印包第 2 頁的熱光子計算表：從 300 K 的 890 個開始，每經過一個 −20 dB 衰減器就除以 100，寫下每一層剩幾個。
2. 挑戰題：只放兩個衰減器會剩幾個？和千分之一（0.001）比一比，寫一句話說明為什麼要放三層。
3. 用列印包第 3 頁練習分貝換算（−10 dB = 十分之一；+20 dB = 100 倍）。
4. 加分題（給高中以上）：執行 `thermal_photons.py` 第四部分，看看把衰減器自己的熱雜訊算進去以後，剩下幾個；再看看 60 dB 全部放在室溫會怎樣。
''',

'thermal_photons.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## thermal_photons.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 讀取鏈接線圖參考答案（照學程簡報 p32 與 index.html#fridge）\n\n'
  '| 溫層 | 輸入線（往下） | 輸出線（往上） | 目的 |\n|---|---|---|---|\n'
  '| 300 K 室溫 | AWG、IQ 混頻器（約 −50 dBm） | 室溫放大器、下變頻、ADC、FPGA | 產生脈衝；最後放大、數位化、判別 0／1 |\n'
  '| 50 K | （熱錨定） | （熱錨定） | 把線的熱導走 |\n'
  '| 4 K | 衰減器 −20 dB | HEMT 約 +40 dB | 壓熱雜訊／第二級放大 |\n'
  '| Still ~0.8 K | （熱錨定，可加 −10 dB） | 超導同軸線 | |\n'
  '| Cold plate ~100 mK | 衰減器 −20 dB | — | 壓熱雜訊 |\n'
  '| Mixing chamber ~10 mK | 衰減器 −20 dB、低通／紅外濾波 | 環行器／隔離器、TWPA／JPA 約 +20 dB | 壓熱雜訊、濾高頻／擋回來的雜訊、第一級放大（約半個光子雜訊） |\n'
  '| 樣品 | 晶片：約 −120 dBm（腔內幾個光子） | 訊號約 −120 dBm 起 | |\n\n'
  '## 熱光子計算表答案\n\n'
  '- 890 → 第一個衰減器 8.9 → 第二個 0.089 → 第三個 0.00089（約千分之一以下）。\n'
  '- 只放兩個：0.089 個，是千分之一的 89 倍，太吵了；所以要放三層、總共約 −60 dB（簡報 p33：約 −60 dB 才能讓殘留熱光子 ≲ 10⁻³）。\n'
  '- 加分題：把衰減器自己的熱雜訊算進去，4 K 那層之後約 20.2 個（4 K 自己就有約 11.4 個）、100 mK 之後約 0.24 個、10 mK 之後約 0.0024 個；'
  '如果 60 dB 全部放在 300 K，出來還是約 890 個，一點都沒變少——這就是衰減器要放在越來越冷的地方的原因。\n'
  '  （加分題的算式是常見的衰減器模型，學程簡報 p33 用文字描述同一件事；簡報說的「≲ 10⁻³」是代表值。）\n\n'
  '## 分貝練習單答案\n\n'
  '- −10 dB = 十分之一；−20 dB = 百分之一；−40 dB = 萬分之一；−60 dB = 百萬分之一。+20 dB = 100 倍；+40 dB = 10000 倍。\n'
  '- −50 dBm 經過三個 −20 dB 衰減器 → −110 dBm（動畫小圖 MXC 那點是 −110，再經過濾波和線路，到晶片約 −120）。\n'
  '- 放大器順序：量子極限放大器（10 mK，約 +20 dB，約半個光子雜訊）→ HEMT（4 K，約 +40 dB，約 10–20 個光子雜訊）→ 室溫放大器。\n\n'
  '## 常見問題\n\n'
  '- 衰減不是浪費訊號嗎？衰減器把訊號和熱雜訊一起壓低；訊號變弱，室溫端多給一點功率就好（簡報 p33）。真正要擋的是會讓量子位元失相的熱光子。\n'
  '- 為什麼不全部在室溫衰減？衰減器自己會放出所在溫度的熱雜訊，放在 300 K 就會補回 300 K 的雜訊（見加分題）。\n'
  '- 為什麼量子極限放大器要放第一級？簡報 p34 的 Friis 公式：整條放大鏈的雜訊主要由第一級決定。HEMT 當第一級會加入 10–20 個光子的雜訊，把只有幾個光子的訊號淹沒。\n'
  '- 環行器在做什麼？只讓訊號往上走，擋住從上面回來的雜訊和放大器的泵浦微波，不讓它們回灌到晶片（學程筆記 §4.2）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。
左邊面板很長，讀數、滑桿和按鈕在下方，要往下捲。

## `index.html#fridge`（JJ 與微波讀取 3D 場景 11：稀釋冷凍機中的微波讀取鏈）

- 左邊標籤：六個溫層板（300 K 室溫頂板、50 K、4 K、Still ~0.8 K、Cold plate ~100 mK、Mixing chamber ~10 mK），晶片在最底下（樣品盒＋磁屏蔽）。
- 輸入線（左）：三個「衰減器 −20 dB」與「低通 / Eccosorb 濾波」。輸出線（右）：「環行器 / 隔離器」、「TWPA / JPA（~20 dB）」、「HEMT（~40 dB）」、「室溫放大器」。
- 光球：往下時淡藍色，每經過一個衰減器就變小，外圈的光暈也變小；經過晶片後變成金色，往上經過放大器時放大器會亮起來，光球一級比一級大。
- 讀數：第一行跟著光球的位置換說明；第二行是熱光子數「7 GHz 時 300 K ≈ 890，10 mK ≈ 10⁻¹⁵」。
- 控制：「動畫速度」滑桿（0.3×–2.5×）、「視角：整體」「放大混合腔」按鈕；滑鼠可以拖曳旋轉、滾輪縮放；空白鍵暫停。
- 右下角小圖：訊號功率沿讀取鏈的變化（dBm），從 AWG −50 往下到晶片 −120，再經過放大器爬回來；青色直線跟著光球的位置移動。

## 之後的課

Q039「讀取設計的取捨」會看讀取腔線寬、色散位移、Purcell 效應和讀取速度怎麼互相拉扯。
''',
}

LAYERS = ['300 K 室溫', '50 K', '4 K', 'Still ~0.8 K', 'Cold plate ~100 mK', 'Mixing chamber ~10 mK', '樣品（晶片）']
SHEET_HEADER = ['溫層', '輸入線元件（往下）', '輸出線元件（往上）', '目的', '過關']
SHEET_ROWS = [[name] for name in LAYERS]

EXTRA_CSS = '''table.map td{height:14.5mm;font-size:10.5pt;vertical-align:top}table.map th{font-size:10.5pt}table.map td:first-child{font-size:10pt;white-space:nowrap}table.map th{white-space:nowrap}
table.rec td{height:13mm;font-size:11.5pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.calc p{margin:2.2mm 0;font-size:12pt}'''


def html():
    map_rows = ''.join(f'<tr><td>{name}</td><td></td><td></td><td></td><td></td></tr>' for name in LAYERS)
    rec_rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td><td></td></tr>' for a, b in (
        ('出發', '300 K 室溫'), ('第 1 個衰減器', '4 K（−20 dB）'), ('第 2 個衰減器', '100 mK（−20 dB）'), ('第 3 個衰減器', '10 mK（−20 dB）')))
    pages = [
        '<h2>讀取鏈接線圖（闖關卡）</h2><p class="lead">照 index.html#fridge 從室溫往下走輸入線，再沿輸出線走回室溫；每個元件一關，說出目的才打勾。</p>'
        '<table class="map"><tr><th style="width:17%">溫層</th><th style="width:24%">輸入線元件（往下）</th><th style="width:24%">輸出線元件（往上）</th>'
        '<th>目的</th><th style="width:9%">過關</th></tr>' + map_rows + '</table>'
        '<p style="font-size:10.5pt;margin-top:2.5mm">提示：輸入線有 3 個衰減器和 1 個濾波器；輸出線有環行器和 3 級放大器。最後標出每一層衰減或放大了幾 dB。</p>',
        '<h2>熱光子計算表</h2><p class="lead">7 GHz 時，300 K 的線裡大約有 890 個熱光子。每經過一個 −20 dB 衰減器，就除以 100。</p>'
        '<table class="rec"><tr><th style="width:22%">走到哪裡</th><th style="width:26%">溫層（衰減）</th><th>剩幾個熱光子</th><th style="width:20%">比千分之一多還是少？</th></tr>'
        '<tr><td>出發</td><td>300 K 室溫</td><td>890</td><td>多</td></tr>' + rec_rows.split('</tr>', 1)[1] + '</table>'
        '<div class="box calc" style="margin-top:5mm"><h3>挑戰題</h3><p>只放兩個衰減器，會剩＿＿＿＿個熱光子，是千分之一的＿＿＿＿倍。</p>'
        '<p>為什麼要放三層？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>為什麼不能把 60 dB 全部放在室溫？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>分貝練習單</h2><p class="lead">每 −10 dB 就是變成十分之一；每 +10 dB 就是變成十倍。</p>'
        '<div class="box calc"><h3>一、換成倍數</h3>'
        '<p>① −20 dB = ＿＿＿＿分之一　② −40 dB = ＿＿＿＿分之一　③ −60 dB = ＿＿＿＿分之一</p>'
        '<p>④ +20 dB = ＿＿＿＿倍　⑤ +40 dB = ＿＿＿＿倍</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>二、訊號走到哪裡</h3><p>AWG 送出 −50 dBm，經過三個 −20 dB 衰減器後是＿＿＿＿ dBm。</p>'
        '<p>動畫右下小圖裡，晶片那一點大約是＿＿＿＿ dBm。</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>三、放大器排順序</h3><p>第一級：＿＿＿＿＿＿（放在＿＿＿＿）　第二級：＿＿＿＿＿＿（放在＿＿＿＿）　第三級：＿＿＿＿＿＿</p>'
        '<p>為什麼第一級要用量子極限放大器？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>說明卡：我的讀取鏈接線圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 讀取鏈：衰減、環行器、放大器在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出輸入線為什麼要層層衰減</li><li>說出環行器的目的</li>'
        '<li>說出放大器為什麼要先量子極限、再 HEMT</li><li>說出為什麼衰減不是浪費訊號</li>'
        '<li>示範一次：用動畫從室溫追蹤訊號到晶片再回來</li><li>替讀取鏈接線圖取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q038 讀取鏈接線圖 列印包', '父子科技學院 量子電腦學程 Q038｜讀取鏈：衰減、環行器、放大器', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q038-readout-chain', folder='Q038_讀取鏈：衰減、環行器、放大器', files=FILES,
        sheet=('03_讀取鏈接線圖.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_讀取鏈接線圖.pdf', pack_pages=4,
        pack_needles=('讀取鏈接線圖', '熱光子計算表', '分貝練習單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q038', episode_dir='specials/q038-readout-chain',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（thermal_photons.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'thermal_photons.py',
               'recordedRun': {'n_th_7GHz': {str(T): float(f'{v:.4g}') for T, v in R['NTH'].items()},
                               'simple_chain': R['SIMPLE'],
                               'full_model_chain': [float(f'{v:.4g}') for v in R['FULL']],
                               'all_60dB_at_300K': float(f"{R['ALL_ROOM']:.4g}")},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q038/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

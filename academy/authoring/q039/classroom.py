"""Q039 課堂教材：讀取參數卡、有／無濾波器對照表、答辯追問卡、說明卡（列印）、解答、readout_calculator.py（讀取參數計算器）、動畫導覽。

不需要帳號，也不需要安裝套件（readout_calculator.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#dispersive、#iq 與 operation.html#readout。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q039/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q039：讀取參數計算器。

不用安裝任何套件，只要 Python 3。執行：  python readout_calculator.py
想試自己的參數，改最下面 MY_DESIGN 那一行的數字再執行一次。

公式（學程簡報 JJ_Microwave_Readout_Talk p35、p37 與學程筆記 notes/dispersive-readout.md §2.5、§3；頻率都是「除以 2π」以後的數字）：
- 失諧 Δ = f_q − f_r
- 色散位移 χ = g² α / [Δ (Δ + α)]（兩個狀態的讀取腔頻率差 2χ）
- 建議線寬 κ = 2|χ|（2χ ≈ κ 時兩個狀態分得最開）
- 臨界光子數 n_crit = Δ² / (4 g²)
- 珀塞爾漏能 γ_P = κ (g/Δ)²，珀塞爾限制的 T₁ 上限 = 1 / (2π γ_P)
- 讀取腔響應時間約 1 / (2π κ)；簡報 p37 的讀取時間是它的好幾倍（約 300–600 ns 對 145 ns）
- 兩個狀態在同相正交平面上的距離（探測在正中間）= 2x / (1 + x²)，x = 2χ/κ（最大值 1 在 x = 1）
- 珀塞爾濾波器：學程簡報和筆記沒有給它能把漏能壓低幾倍；這裡的 FILTER = 100 是練習用的假設值，不是某個濾波器的規格。
"""
import math

FILTER = 100  # 假設：濾波器把珀塞爾漏能壓低 100 倍（練習用）


def design(fr, fq, g, alpha, kappa=None, filt=1):
    """fr、fq、g、alpha 單位 GHz（g = 0.1 就是 100 MHz）；kappa 不給就用 2|χ|；filt = 濾波器壓低倍數。"""
    D = fq - fr
    chi = g ** 2 * alpha / (D * (D + alpha))
    k = 2 * abs(chi) if kappa is None else kappa
    x = 2 * abs(chi) / k
    gp = k * (g / D) ** 2 / filt
    return {'chi_MHz': chi * 1e3, 'kappa_MHz': k * 1e3, 'ratio_2chi_kappa': x, 'distance': 2 * x / (1 + x * x),
            'n_crit': D ** 2 / (4 * g ** 2), 'T1_limit_us': 1 / (2 * math.pi * gp * 1e9) * 1e6,
            'one_over_kappa_ns': 1 / (2 * math.pi * k * 1e9) * 1e9}


def show(name, d):
    print(f'  {name}')
    print(f"    色散位移 χ = {d['chi_MHz']:.3f} MHz，線寬 κ = {d['kappa_MHz']:.3f} MHz，2χ/κ = {d['ratio_2chi_kappa']:.2f}，距離 = {d['distance']:.3f}")
    print(f"    臨界光子數 = {d['n_crit']:.0f}，珀塞爾限制的 T₁ 上限 = {d['T1_limit_us']:.0f} μs，1/κ = {d['one_over_kappa_ns']:.0f} ns")


print('一、簡報 p37 的範例：讀取腔 7 GHz、量子位元 5 GHz、g = 100 MHz、α = −250 MHz')
BASE = design(7.0, 5.0, 0.100, -0.250)
show('沒有濾波器、κ = 2|χ|', BASE)

print()
print('二、色散位移不變，只改線寬')
K = BASE['kappa_MHz'] / 1e3
DOUBLE = design(7.0, 5.0, 0.100, -0.250, kappa=2 * K)
HALF = design(7.0, 5.0, 0.100, -0.250, kappa=K / 2)
show('線寬加倍（讀得快）', DOUBLE)
show('線寬減半（讀得慢）', HALF)

print()
print('三、沒有濾波器：維持 κ = 2|χ|，把 g 調小，直到 T₁ 上限超過 500 μs')
NOFILTER = None
for g_mhz in range(100, 20, -1):
    d = design(7.0, 5.0, g_mhz / 1000, -0.250)
    if d['T1_limit_us'] >= 500:
        NOFILTER = (g_mhz, d)
        break
show(f'g = {NOFILTER[0]} MHz', NOFILTER[1])
print(f"    讀取腔響應時間從 {BASE['one_over_kappa_ns']:.0f} ns 變成 {NOFILTER[1]['one_over_kappa_ns']:.0f} ns，讀取變慢")

print()
print(f'四、有濾波器（假設把漏能壓低 {FILTER} 倍）：g = 100 MHz')
WITHF = design(7.0, 5.0, 0.100, -0.250, filt=FILTER)
WITHF2 = design(7.0, 5.0, 0.100, -0.250, kappa=2 * K, filt=FILTER)
show('κ = 2|χ|', WITHF)
show('κ 加倍（更快，但 2χ/κ 變 0.5）', WITHF2)

print()
print('五、我的設計（改這一行）')
MY_DESIGN = design(7.0, 5.0, 0.100, -0.250)
show('MY_DESIGN', MY_DESIGN)
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'readout_calculator.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()

# 製作代理實跑（Python 3）：與旁白、簡報 p37、筆記 §2.5、§3 一致
B = R['BASE']
assert f"{B['chi_MHz']:.2f}" == '-0.56' and f"{B['kappa_MHz']:.1f}" == '1.1' and round(B['n_crit']) == 100
assert round(B['T1_limit_us']) == 57 and round(B['one_over_kappa_ns']) == 143 and f"{B['distance']:.3f}" == '1.000'
assert f"{R['DOUBLE']['distance']:.3f}" == '0.800' and f"{R['HALF']['distance']:.3f}" == '0.800'
assert round(R['DOUBLE']['T1_limit_us']) == 29 and round(R['HALF']['T1_limit_us']) == 115
assert R['NOFILTER'][0] == 58 and round(R['NOFILTER'][1]['T1_limit_us']) == 506 and round(R['NOFILTER'][1]['one_over_kappa_ns']) == 426
assert round(R['WITHF']['T1_limit_us']) == 5730 and round(R['WITHF2']['T1_limit_us']) == 2865

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q039：讀取設計的取捨（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。上一堂我們沿著稀釋冷凍機走完讀取鏈；這一堂回到晶片上的讀取腔，練習工程師的取捨：
讀取腔線寬 κ 大，讀得快，但量子位元會經由讀取腔漏能（珀塞爾效應，γ ≈ κ(g/Δ)²），能量弛豫時間 T₁ 的上限變短；
色散位移 χ 要和 κ 搭配，2χ ≈ κ 時兩個狀態分得最開；讀取光子數多訊號強，但超過臨界光子數會引發躍遷；珀塞爾濾波器讓 κ 可以大又不漏能。
好玩機制是「工程答辯」：孩子設計一組參數，爸爸當審查委員追問，孩子用計算器的數字回答。作品是「讀取參數卡」。下一堂 Q040 是「量子電腦 ≠ 量子晶片」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三個旋鈕、線寬與珀塞爾效應、2χ ≈ κ、簡報 p37 數值範例、珀塞爾濾波器；看 3D 動畫 | 影片第 2–8 段、`05_動畫導覽.md` |
| 25–65 | 父子用讀取參數計算器設計一組參數，填讀取參數卡；爸爸用答辯追問卡追問 | 列印包第 1、3 頁、`readout_calculator.py`、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：在沒有／有珀塞爾濾波器兩種情況下重新設計 | 列印包第 2 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替讀取參數卡取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_讀取參數卡.pdf`（A4，共 4 頁）。另備計算機或手機。
- 執行一次 `readout_calculator.py`（只要 Python 3，不需要安裝套件），對照 `04_解答.md` 裡的實跑輸出。沒有電腦時，可以直接用解答裡的數字。
- 想多了解可以讀學程筆記 `notes/dispersive-readout.md` 的 §2.5、§3。
- 下載學程的 `animations/` 資料夾，用瀏覽器先開一次 `index.html#dispersive`（見 `05_動畫導覽.md`）。

## 驗收重點

1. 完成「讀取參數卡」：五個輸入數字、算出的 χ、κ、臨界光子數、珀塞爾 T₁ 上限、讀取時間，以及每個選擇的好處和代價。
2. 不看稿說出核心原理：κ 大讀得快但漏能；2χ ≈ κ 分得最開；濾波器讓讀取頻率通過、擋住量子位元頻率。
3. 指出至少一個注意事項：κ 大讀得快，但 Purcell 效應會讓 T₁ 變短；每個旋鈕都有甜蜜點，不是越大越好。

## 誠實說明

- 數值範例（7 GHz、5 GHz、g 100 MHz、α −250 MHz → χ ≈ −0.56 MHz、κ ≈ 1.1 MHz、T₁ 上限 ≈ 57 μs）照學程簡報 p37 與筆記，是教學範例，不是某台機器的量測值。
- 「濾波器把漏能壓低 100 倍」是計算器裡練習用的假設值；學程簡報和筆記沒有給濾波器的倍數。答辯時請說「假設」。
- 珀塞爾公式是近似式；真實晶片的 T₁ 由所有損耗一起決定，珀塞爾只給一個上限。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：設計一組參數並答辯（約 40 分鐘）

1. 執行 `python readout_calculator.py`，先看第一部分：簡報 p37 的範例（讀取腔 7 GHz、量子位元 5 GHz、g = 100 MHz、α = −250 MHz）。
   把算出的 χ、κ、臨界光子數、珀塞爾 T₁ 上限、1/κ 抄到列印包第 1 頁的「範例」那一欄。
2. 看第二部分：色散位移不變、線寬加倍或減半，距離都變成 0.800；線寬加倍時 T₁ 上限減半。
3. 父子一起改 `MY_DESIGN` 那一行（例如把讀取腔改成 7.2 GHz、g 改成 80 MHz），重新執行，把結果抄到「我的設計」那一欄，並在每一格寫下好處和代價。
4. 工程答辯：爸爸拿列印包第 3 頁的追問卡，一次問一題；孩子必須用計算器的數字回答，答得出來就打勾。
5. 可以在動畫裡看「線寬加倍或減半」：開 `index.html#dispersive`，把「色散位移 χ / κ」滑桿拉到 0.25、1.0、0.5，看讀數的分離距離（見 `05_動畫導覽.md`）。

## 下半場：孩子改造——有／無珀塞爾濾波器（約 30 分鐘）

1. 用列印包第 2 頁的對照表。
2. 沒有濾波器：目標是珀塞爾 T₁ 上限超過 500 μs。維持 κ = 2|χ|，把 g 一點一點調小（計算器第三部分自動找），記下 g、κ、1/κ，說明讀取變慢多少。
3. 有濾波器：計算器第四部分假設濾波器把漏能壓低 100 倍，g 維持 100 MHz、κ 維持大。記下 T₁ 上限。
4. 兩組並排，寫一句話答辯：你會選哪一組？為什麼？（提示：快、準、不傷位元，三件事各怎麼樣？）
''',

'readout_calculator.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## readout_calculator.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 讀取參數卡參考答案（簡報 p37 範例）\n\n'
  '| 項目 | 數字 | 好處 | 代價 |\n|---|---|---|---|\n'
  '| 讀取腔 f_r | 7.0 GHz | | |\n'
  '| 量子位元 f_q | 5.0 GHz（Δ = −2 GHz） | 失諧大，在色散區 | 失諧越大，χ 越小 |\n'
  '| 耦合 g | 100 MHz | χ 夠大 | 珀塞爾漏能 ∝ g² |\n'
  '| 色散位移 χ | ≈ −0.56 MHz | 兩狀態差 2χ ≈ 1.1 MHz | 太大會增加熱光子失相 |\n'
  '| 線寬 κ | ≈ 1.1 MHz（= 2|χ|） | 分得最開；1/κ ≈ 143 ns | 珀塞爾 T₁ 上限只有約 57 μs |\n'
  '| 臨界光子數 | 100 | | 讀取光子數要控制在它以下 |\n'
  '| 讀取時間 | 約 300–600 ns（簡報 p37） | | |\n\n'
  '## 有／無濾波器對照表答案\n\n'
  '- 沒有濾波器：g 降到 58 MHz 時，χ ≈ −0.19 MHz、κ ≈ 0.37 MHz，T₁ 上限約 506 μs；1/κ 從 143 ns 變成約 426 ns，讀取變慢約三倍。'
  '原因：維持 κ = 2|χ| 時，χ ∝ g²、珀塞爾漏能 κ(g/Δ)² ∝ g⁴，所以 g 小一點，T₁ 上限就大很多。\n'
  '- 有濾波器（假設壓低 100 倍）：g 100 MHz、κ ≈ 1.1 MHz 時 T₁ 上限約 5730 μs；κ 加倍時約 2865 μs，但 2χ/κ 變成 0.5、距離 0.8。\n'
  '- 答辯可以這樣說：「沒有濾波器時，我只能用小的 g 和 κ 換 T₁，讀取變慢；有濾波器時，可以保留 g = 100 MHz、κ = 1.1 MHz，讀得快又不漏能，所以選有濾波器。」\n\n'
  '## 答辯追問卡參考答案\n\n'
  '- 為什麼不把線寬再調大？κ 加倍，珀塞爾 T₁ 上限從 57 μs 減半到約 29 μs；而且 2χ/κ 變成 0.5，距離掉到 0.8。\n'
  '- 為什麼 2χ 要約等於 κ？探測在正中間時，x = 2χ/κ = 1 的距離 2x/(1+x²) 最大（= 1）；x = 0.5 或 2 都是 0.8（筆記 §2.5 表）。\n'
  '- T₁ 上限夠不夠？57 μs 對現在幾百微秒的量子位元不夠（簡報 p37 備註），要加珀塞爾濾波器。\n'
  '- 讀取光子數可以多送嗎？臨界光子數 100（Δ²/4g²）；超過會引發不想要的躍遷，量子位元甚至被激發到 |2⟩ 以上（簡報 p35 備註）。\n'
  '- 讀取要多久？約 300–600 ns，是 1/κ（約 143 ns）的好幾倍（簡報 p37）。\n\n'
  '## 常見問題\n\n'
  '- 線寬越大越好嗎？不是。κ 大讀得快，但沒有濾波器時珀塞爾效應讓 T₁ 變短；κ 太大 χ 跟不上，兩個狀態反而分不開。\n'
  '- 珀塞爾濾波器是什麼？讀取腔與饋線之間的帶通濾波器，讓讀取頻率（7 GHz）通過、擋住量子位元頻率（5 GHz），所以 κ 可以大而量子位元不經饋線衰減（簡報 p35）。\n'
  '- 計算器的「100 倍」哪裡來？是練習用的假設值；簡報和筆記沒有給濾波器的倍數。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。
左邊面板很長，讀數、滑桿和按鈕在下方，要往下捲。

## `index.html#dispersive`（JJ 與微波讀取 3D 場景 9：色散讀取）

- 「色散位移 χ / κ」滑桿：預設 0.50（2χ/κ = 1，讀數打勾「最佳」，分離距離 1.000）。拉到 0.25 或 1.00，分離距離都是 0.800；
  可以想成色散位移不變、線寬加倍或減半。
- 一開始「自動切換 |0⟩ ↔ |1⟩」是開的，每 3 秒換一次狀態；按「量子位元 |0⟩」或「量子位元 |1⟩」就會停下來。

## `operation.html#readout`（如何操作量子電腦 3D 場景 7：讀取）

- 「積分時間 τ」從 1.00 μs 拉到 0.40 μs：讀取保真度從 96.1 % 掉到 87.3 %；再把「兩團雲的間距（色散位移/放大器）」拉到 1.60：升到 96.5 %。
  讀數的混淆矩陣與保真度是用公式算的，改滑桿立刻更新。

## `index.html#iq`（JJ 與微波讀取 3D 場景 10：單發讀取）

- 「T1（與 τ_int 同單位，越大衰減越少）」滑桿：預設 8。拉到 2，讀取途中掉回 |0⟩ 的紅點變多，落在兩團中間或藍色那一側；拉到 40，紅點幾乎都留在紅色那一團。
  這個場景沒有珀塞爾效應的模型，我們只是用 T1 滑桿「模擬」漏能變多（沒有濾波器）或變少（像加了濾波器）。保真度是統計值，每次會有一點不同。

## 之後的課

Q040「量子電腦 ≠ 量子晶片」會走出晶片，看機房全景與 7 類連接（氦氣、冷卻水、混合氣、真空、微波、資料、電力）。
''',
}

SHEET_HEADER = ['項目', '範例（簡報 p37）', '我的設計', '好處', '代價']
SHEET_ROWS = [[x] for x in ('讀取腔 f_r', '量子位元 f_q', '耦合 g', '非諧性 α', '色散位移 χ', '線寬 κ', '臨界光子數', '珀塞爾 T₁ 上限', '1/κ（讀取時間）')]

EXTRA_CSS = '''table.card td{height:12.5mm;font-size:10.5pt;vertical-align:middle}table.card th{font-size:10.5pt;white-space:nowrap}table.card td:first-child{font-size:10pt;white-space:nowrap}
table.cmp td{height:13mm;font-size:11pt;text-align:center}table.cmp th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.calc p{margin:2.2mm 0;font-size:12pt}'''


def html():
    card_rows = ''.join(f'<tr><td>{r[0]}</td><td>{ex}</td><td></td><td></td><td></td></tr>' for r, ex in zip(
        SHEET_ROWS, ('7.0 GHz', '5.0 GHz', '100 MHz', '−250 MHz', '', '', '', '', '')))
    cmp_rows = ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a in ('耦合 g', '線寬 κ', '色散位移 χ', '珀塞爾 T₁ 上限', '1/κ（讀取快慢）', '兩狀態距離'))
    pages = [
        '<h2>讀取參數卡</h2><p class="lead">用 readout_calculator.py 算出每一格；「我的設計」改 MY_DESIGN 那一行。每個選擇都寫好處和代價。</p>'
        '<table class="card"><tr><th style="width:20%">項目</th><th style="width:18%">範例（簡報 p37）</th><th style="width:18%">我的設計</th>'
        '<th>好處</th><th>代價</th></tr>' + card_rows + '</table>'
        '<p style="font-size:10.5pt;margin-top:2.5mm">提示：建議線寬 κ = 2|χ|；珀塞爾漏能 = κ(g/Δ)²；臨界光子數 = Δ²/4g²。</p>',
        '<h2>有／無濾波器對照表</h2><p class="lead">同一顆量子位元設計兩次：目標是珀塞爾 T₁ 上限超過 500 μs，又盡量讀得快。</p>'
        '<table class="cmp"><tr><th style="width:30%">項目</th><th>沒有濾波器</th><th>有濾波器（假設壓低 100 倍）</th></tr>' + cmp_rows + '</table>'
        '<div class="box calc" style="margin-top:5mm"><h3>答辯</h3><p>我選＿＿＿＿＿＿＿＿，因為＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>沒有濾波器時，讀取變慢了大約＿＿＿＿倍。</p>'
        '<p>這組設計的代價是＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>答辯追問卡（爸爸用）</h2><p class="lead">一次問一題；孩子用計算器的數字回答，答得出來就打勾。</p>'
        '<div class="box"><ul class="chk">'
        '<li>為什麼不把線寬再調大？調大以後 T₁ 上限變多少？</li>'
        '<li>為什麼 2χ 要約等於 κ？比值變成一半或兩倍會怎樣？</li>'
        '<li>珀塞爾 T₁ 上限夠不夠？不夠怎麼辦？</li>'
        '<li>讀取光子數可以多送嗎？臨界光子數是多少？</li>'
        '<li>讀取大概要多久？和 1/κ 有什麼關係？</li>'
        '<li>濾波器擋住的是哪個頻率？讓哪個頻率通過？</li></ul></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>審查紀錄</h3><p>答對＿＿＿題／6 題　最難回答的一題：＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>委員的建議：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>說明卡：我的讀取參數卡</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 讀取設計的取捨在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三個旋鈕各自的好處和代價</li><li>說出為什麼 2χ 要約等於 κ</li>'
        '<li>說出珀塞爾效應為什麼讓 T₁ 變短</li><li>說出珀塞爾濾波器怎麼解決</li>'
        '<li>示範一次：用計算器改一個數字並解釋結果</li><li>替讀取參數卡取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q039 讀取參數卡 列印包', '父子科技學院 量子電腦學程 Q039｜讀取設計的取捨', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q039-readout-tradeoffs', folder='Q039_讀取設計的取捨', files=FILES,
        sheet=('03_讀取參數卡.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_讀取參數卡.pdf', pack_pages=4,
        pack_needles=('讀取參數卡', '有／無濾波器對照表', '答辯追問卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q039', episode_dir='specials/q039-readout-tradeoffs',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（readout_calculator.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'readout_calculator.py',
               'recordedRun': {'base': {k: float(f'{v:.4g}') for k, v in R['BASE'].items()},
                               'kappa_double_T1_us': float(f"{R['DOUBLE']['T1_limit_us']:.4g}"),
                               'kappa_half_T1_us': float(f"{R['HALF']['T1_limit_us']:.4g}"),
                               'no_filter_g_MHz': R['NOFILTER'][0],
                               'no_filter': {k: float(f'{v:.4g}') for k, v in R['NOFILTER'][1].items()},
                               'with_filter_assumed_100x_T1_us': float(f"{R['WITHF']['T1_limit_us']:.4g}")},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q039/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

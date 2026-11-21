"""Q035 課堂教材：S21 判讀紀錄、χ/κ 改造表、判讀練習單、說明卡（列印）、解答、s21_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（s21_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#dispersive。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q035/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q035：S21 判讀小工具。

不用安裝任何套件，只要 Python 3。執行：  python s21_check.py
公式和動畫 animations/index.html#dispersive（js/scenes/09_dispersive.js 第 20–21、74、106–108 行）相同，
頻率都以諧振腔線寬 κ 為單位：
- 量子位元在 |0⟩：諧振腔頻率 ω_r − χ；在 |1⟩：ω_r + χ（學程簡報 JJ_Microwave_Readout_Talk p28）。
- 穿透係數 S21 = 1 / (1 + 2i(ω − ω_s)/κ)（筆記 notes/dispersive-readout.md §2.5）：
  振幅 |S21| = 1/√(1 + 4d²)、相位 = −arctan(2d)，d = (ω − ω_s)/κ。
- 一、探測在正中間：不同 2χ/κ 的相位差與 IQ 分離距離。
- 二、χ/κ = 0.5 時，探測頻率移動，兩種狀態的振幅、相位差與分離距離。
- 三、盲測練習：電腦偷偷選 |0⟩ 或 |1⟩，只印出 S21 的振幅與相位，你來猜（固定亂數種子，可重現）。
"""
import cmath
import math
import random


def s21(probe, shift):
    """探測頻率 probe、諧振腔頻率 shift（都以 κ 為單位）的穿透係數。"""
    return 1 / (1 + 2j * (probe - shift))


def compare(chi, probe=0.0):
    """回傳 (|0⟩ 振幅, |1⟩ 振幅, 相位差（度）, IQ 分離距離)。"""
    s0, s1 = s21(probe, -chi), s21(probe, chi)
    dphi = abs(math.degrees(cmath.phase(s1) - cmath.phase(s0)))
    return abs(s0), abs(s1), dphi, abs(s1 - s0)


print('一、探測在正中間（ω = ω_r）：2χ/κ 與相位差、分離距離')
MID = {}
for x in (0.1, 0.2, 0.25, 0.5, 1, 2, 3, 4):
    a0, a1, dphi, sep = compare(x / 2)
    MID[x] = (a0, dphi, sep)
    print(f'  2χ/κ = {x:<4}：兩種狀態振幅都是 {a0:.3f}、相位差 {dphi:5.1f}°、分離距離 {sep:.3f}')

print()
print('二、χ/κ = 0.5（2χ = κ），移動探測頻率')
PROBE = {}
for p in (-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0):
    a0, a1, dphi, sep = compare(0.5, p)
    PROBE[p] = (a0, a1, dphi, sep)
    print(f'  探測 {p:+.2f} κ：|0⟩ 振幅 {a0:.3f}、|1⟩ 振幅 {a1:.3f}、相位差 {dphi:5.1f}°、分離距離 {sep:.3f}')

print()
print('三、盲測練習（χ/κ = 0.5；先自己猜，最後一行才是答案）')
rng = random.Random(39)
QUIZ = []
for k in range(1, 6):
    state = rng.randint(0, 1)
    probe = rng.choice((-0.5, 0.0, 0.5))
    s = s21(probe, 0.5 if state else -0.5)
    QUIZ.append((probe, state))
    print(f'  第 {k} 題：探測 {probe:+.1f} κ → 振幅 {abs(s):.3f}、相位 {math.degrees(cmath.phase(s)):+6.1f}°')
print('  答案：' + '、'.join(f'第 {k} 題 |{st}⟩' for k, (_, st) in enumerate(QUIZ, 1)))
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 's21_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、動畫段、09_dispersive.js 讀數相同
assert f"{R['MID'][1][1]:.1f}" == '90.0' and f"{R['MID'][1][2]:.3f}" == '1.000'
assert f"{R['MID'][0.25][1]:.0f}" == '28' and f"{R['MID'][0.25][2]:.2f}" == '0.47'
assert f"{R['MID'][4][1]:.0f}" == '152' and f"{R['MID'][4][2]:.2f}" == '0.47'
assert f"{R['MID'][0.2][1]:.1f}" == '22.6' and f"{R['MID'][0.2][2]:.3f}" == '0.385'
assert f"{R['MID'][3][1]:.1f}" == '143.1' and f"{R['MID'][3][2]:.3f}" == '0.600'
assert f"{R['PROBE'][-0.5][2]:.1f}" == '63.4' and f"{R['PROBE'][-0.5][1]:.3f}" == '0.447' and f"{R['PROBE'][-0.5][0]:.3f}" == '1.000'
assert f"{R['PROBE'][0.0][0]:.3f}" == f"{R['PROBE'][0.0][1]:.3f}" == '0.707'

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q035：色散位移 ±χ（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂的主角是「色散位移」：量子位元在 |0⟩ 時，讀取諧振腔的頻率往下偏 χ；在 |1⟩ 時往上偏 χ。
我們送一道探測微波穿過諧振腔，看穿透訊號 S21 的振幅和相位，就能判斷狀態。好玩機制是「盲測」：爸爸偷偷設定狀態，孩子只看曲線猜 0 或 1。
作品是「S21 判讀紀錄」。下一堂 Q036 是「IQ 平面：把微波變成一個點」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 色散區、色散位移有多小、S21 的振幅與相位、怎麼判讀、κ 和 χ 的搭配；看 3D 動畫 | 影片第 2–8 段、`05_動畫導覽.md` |
| 25–65 | 盲測：爸爸設定狀態並遮住答案，孩子只看曲線，寫 S21 判讀紀錄（十回合） | 列印包第 1、3 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：調「色散位移 χ / κ」與「探測頻率」滑桿，找最好分辨的組合 | 列印包第 2 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替判讀紀錄取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_S21判讀紀錄.pdf`（A4，共 4 頁）。另備便利貼（遮小球和按鈕用）、彩色筆。
- 讀一遍 `04_解答.md`；想多了解可以讀學程筆記 `notes/dispersive-readout.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先開一次 `index.html#dispersive`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `s21_check.py`（不需要安裝套件）。

## 驗收重點

1. 完成「S21 判讀紀錄」：十回合都有探測頻率、看到的線索、猜測和答案，並算出猜對幾次。
2. 不看稿說出核心原理：量子位元的狀態讓諧振腔頻率偏移 ±χ；探測微波穿過諧振腔，振幅和相位跟著改變；探測在正中間時振幅一樣、要看相位。
3. 指出至少一個注意事項：2χ ≈ κ 時兩個狀態分得最開（相位差 90°），但這只是最佳化條件之一，不是唯一的設計選擇。

## 誠實說明

- χ ≈ 0.77 MHz、兩狀態差約 1.5 MHz 是學程 transmon 簡報與師生對話紀錄的範例數字，不是某台機器的量測值；不同文獻對 χ 的定義可能差兩倍，正負號也不一定相同。
- 動畫裡的頻率以線寬 κ 為單位，是示意；盲測用的是動畫畫出的理論曲線，不是實驗數據。家裡沒有諧振腔可以量，不要編造量測數據。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：盲測，寫 S21 判讀紀錄（約 40 分鐘）

1. 用瀏覽器開 `animations/index.html#dispersive`，左邊面板往下捲到底，看到「量子位元 |0⟩」「量子位元 |1⟩」兩顆按鈕、兩個滑桿和讀數。
2. 先一起認識畫面：前面兩座小山是振幅（藍 = |0⟩、紅 = |1⟩），後面是相位曲線，金色直線是探測微波，右下角小圖是兩個狀態的點。
3. 盲測一回合：
   - 孩子轉過身。爸爸按「量子位元 |0⟩」或「量子位元 |1⟩」（按了就會停止自動切換），可以順便把「探測頻率」滑桿拉到 −0.5、0 或 +0.5。
   - 爸爸用便利貼遮住上方的小球、它的標籤，以及面板上那一排狀態按鈕。
   - 孩子轉回來，只看曲線：亮起來的是偏左（藍）還是偏右（紅）的那座山？金色探測線碰到亮曲線的地方是高還是低？寫下猜測和理由。
   - 爸爸掀開便利貼，寫下答案。
4. 玩十回合，算猜對幾次。換探測頻率時，振幅線索會改變：探測在正中間時兩條振幅一樣高，要靠其他線索。
5. 沒有電腦時，可以用 `s21_check.py` 第三部分的盲測題，或用列印包第 3 頁的判讀練習單。

## 下半場：孩子改造——找最好分的組合（約 30 分鐘）

1. 用列印包第 2 頁的改造表。「色散位移 χ / κ」滑桿從 0.05 調到 2，每一格記下讀數的「兩狀態相位差 Δθ」與「IQ 分離距離」。
2. 找出分離距離最大的那一格（讀數會打勾、寫「最佳」）。
3. 再把「探測頻率」移離 0，看分離距離會不會變小。
4. 寫一句結論：哪一個組合最好分辨？為什麼這不是唯一的設計選擇（例如線寬大一點讀得比較快，但量子位元會經由諧振腔漏能量）？
''',

's21_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## s21_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 判讀規則（χ/κ = 0.5）\n\n'
  '| 探測頻率 | \\|0⟩ 的線索 | \\|1⟩ 的線索 | 怎麼判讀 |\n|---|---|---|---|\n'
  '| 0（正中間） | 振幅 0.707 | 振幅 0.707 | 振幅分不出來；看亮的是哪座山，或看相位（相位差 90°） |\n'
  '| −0.5（藍色山頂） | 振幅 1.000（山頂） | 振幅 0.447 | 亮曲線在金線上高 → \\|0⟩；低 → \\|1⟩ |\n'
  '| +0.5（紅色山頂） | 振幅 0.447 | 振幅 1.000（山頂） | 亮曲線在金線上高 → \\|1⟩；低 → \\|0⟩ |\n\n'
  '（數字與動畫 index.html#dispersive 的公式相同，見 s21_check.py。）\n\n'
  '## 改造表參考答案（探測在正中間）\n\n'
  '| χ/κ | 2χ/κ | 相位差 | 分離距離 |\n|---|---|---|---|\n'
  '| 0.05 | 0.1 | 11.4° | 0.198 |\n| 0.1 | 0.2 | 22.6° | 0.385 |\n| 0.25 | 0.5 | 53.1° | 0.800 |\n'
  '| 0.5 | 1 | 90.0° | 1.000（最大，讀數打勾「最佳」） |\n| 1 | 2 | 126.9° | 0.800 |\n| 1.5 | 3 | 143.1° | 0.600 |\n| 2 | 4 | 151.9° | 0.471 |\n\n'
  '- 相位差一直隨 χ 變大，但分離距離在 2χ = κ 時最大：χ 太大時，探測微波落在兩座山的低處，穿過來的訊號變弱，兩點反而靠近。\n'
  '- 為什麼不是唯一的設計選擇：簡報 p29 說這是讀取的「最佳化條件之一」；筆記 §3 提到線寬大一點，光子漏出諧振腔比較快，讀取可以快一些，'
  '但量子位元也比較容易經由諧振腔漏掉能量（Purcell 效應），所以晶片會加濾波器；探測微波也不能太強（光子太多會擾亂量子位元）。\n\n'
  '## 判讀練習單答案\n\n'
  '- ① 探測 −0.5、亮的是紅色、在金線上很低 → |1⟩。② 探測 +0.5、亮曲線碰到山頂 → 亮的是紅山 → |1⟩。③ 探測 0、亮的是偏左的山 → |0⟩。\n'
  '- 探測在正中間時，兩條振幅一樣高（0.707），只看振幅分不出來。\n'
  '- 0.77 MHz × 2 ≈ 1.5 MHz；1.5 MHz ÷ 7 GHz = 1.5 ÷ 7000 ≈ 0.0002，約萬分之二。\n\n'
  '## 常見問題\n\n'
  '- 為什麼諧振腔頻率會跟著量子位元變？量子位元約 5 GHz、諧振腔約 7 GHz，差很遠（色散區），兩者不交換能量，只互相「推」頻率：'
  '|0⟩ 時腔頻率 ω_r − χ、|1⟩ 時 ω_r + χ（簡報 p28）。\n'
  '- 動畫裡為什麼小球的狀態一換，亮的曲線就換？亮的那一條代表「現在這個狀態」下諧振腔的反應；另一條是另一個狀態的參考線。\n'
  '- χ 的定義：本學程用「腔頻率 = ω_r ± χ」，兩狀態相差 2χ；有些文獻把總差距叫 χ，看資料時要先確認（筆記 §2.2）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。
左邊面板很長，按鈕和滑桿在下方，要往下捲。

## `index.html#dispersive`（JJ 與微波讀取 3D 場景 9：色散讀取）＝本課主角

- 前面兩座小山是穿透訊號的振幅：藍色峰在 ω_r − χ（|0⟩），紅色峰在 ω_r + χ（|1⟩）；後面是相位曲線；金色直線是探測微波。
- 上方小球是量子位元，預設每 3 秒自動切換 |0⟩、|1⟩；目前狀態的那條曲線比較亮。按「量子位元 |0⟩」或「量子位元 |1⟩」會停止自動切換。
- 「色散位移 χ / κ」滑桿（0.05–2）：兩座山的距離跟著變。「探測頻率 (ω − ω_r) / κ」滑桿（−3–3）：金線左右移動。
- 讀數：兩狀態相位差 Δθ、IQ 分離距離（最大值 1 出現在 2χ = κ、探測於中點）、目前 2χ/κ（接近 1 時打勾「最佳」）。
- 右下角小圖是 IQ 平面（下一堂 Q036 的主角）：兩個點是兩種狀態在探測頻率下的位置。

## 課後延伸：`transmon-3d.html#readout`（transmon 3D 第 5 章：讀取）

- 8 個步驟的自動導覽，第 2 步「色散偏移」看兩條共振曲線（青 = |0⟩、金 = |1⟩，相差約 1.5 MHz），第 3 步「探測與 IQ」看兩個狀態變成 IQ 平面上的兩個點。
- 每一步播完會自動接下一步；想停在某一步，取消「自動接續」的勾選。

## 之後的課

Q036「IQ 平面：把微波變成一個點」會看外差解調怎麼把微波訊號變成 I、Q 兩個數字。
''',
}

SHEET_HEADER = ['回合', '探測頻率', '看到的線索（亮的山、金線上高低）', '我的猜測', '正確答案', '對嗎']
SHEET_ROWS = [[str(k)] for k in range(1, 11)]

EXTRA_CSS = '''table.rec td{height:12.5mm;font-size:11pt;text-align:center}table.rec th{font-size:10pt}
table.mod td{height:13mm;font-size:11pt;text-align:center}table.mod th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.calc p{margin:2.2mm 0;font-size:12pt}'''


def html():
    rows = ''.join(f'<tr><td>{k}</td><td></td><td></td><td></td><td></td><td></td></tr>' for k in range(1, 11))
    mod_rows = ''.join(f'<tr><td>{v}</td><td>{x}</td><td></td><td></td><td></td></tr>'
                       for v, x in (('0.05', '0.1'), ('0.1', '0.2'), ('0.25', '0.5'), ('0.5', '1'), ('1', '2'), ('1.5', '3'), ('2', '4')))
    pages = [
        '<h2>S21 判讀紀錄</h2><p class="lead">爸爸偷偷設定 |0⟩ 或 |1⟩ 並遮住小球和按鈕；孩子只看曲線，寫下線索和猜測。</p>'
        '<table class="rec"><tr><th style="width:8%">回合</th><th style="width:14%">探測頻率</th><th>看到的線索（亮的山在左或右、金線上高或低）</th>'
        '<th style="width:12%">我的猜測</th><th style="width:12%">正確答案</th><th style="width:8%">對嗎</th></tr>' + rows + '</table>'
        '<p style="font-size:11pt;margin-top:3mm">猜對＿＿＿／10 次。最有用的線索是：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>改造表：找最好分的組合</h2><p class="lead">「色散位移 χ / κ」滑桿每調一格，記下讀數的相位差和分離距離（探測頻率先放在 0）。</p>'
        '<table class="mod"><tr><th>χ / κ</th><th>2χ / κ</th><th>相位差 Δθ</th><th>IQ 分離距離</th><th>兩座山看起來</th></tr>' + mod_rows + '</table>'
        '<div class="box" style="margin-top:4mm"><p>分離距離最大的是 χ / κ = ＿＿＿＿；把探測頻率移到 −0.5，分離距離變成＿＿＿＿。</p>'
        '<p>這個組合為什麼不是唯一的設計選擇？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>判讀練習單</h2><p class="lead">沒有電腦也能練：照描述判斷是 |0⟩ 還是 |1⟩（χ / κ = 0.5，藍山在左、紅山在右）。</p>'
        '<div class="box calc"><h3>一、看曲線猜狀態</h3>'
        '<p>① 探測在 −0.5（藍色山頂），亮的是紅色曲線，在金線上很低：＿＿＿＿</p>'
        '<p>② 探測在 +0.5（紅色山頂），亮的曲線在金線上碰到山頂：＿＿＿＿</p>'
        '<p>③ 探測在 0（正中間），亮的是偏左的那座山：＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>二、正中間的陷阱</h3><p>探測在正中間時，兩種狀態的振幅一樣嗎？＿＿＿＿　那要看什麼？＿＿＿＿＿＿</p></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>三、色散位移有多小</h3><p>χ ≈ 0.77 MHz，兩狀態相差 2χ ≈ ＿＿＿＿ MHz。</p>'
        '<p>放在 7 GHz（= 7000 MHz）的諧振腔裡，相對大約是＿＿＿＿＿＿。</p></div>',
        '<h2>說明卡：我的 S21 判讀紀錄</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 色散位移 ±χ 在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出狀態怎麼讓腔頻率偏 ±χ</li><li>說出怎麼從 S21 的振幅和相位判讀</li>'
        '<li>說出探測在正中間時為什麼要看相位</li><li>說出 2χ ≈ κ 不是唯一的設計選擇</li>'
        '<li>示範一次盲測</li><li>替判讀紀錄取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q035 S21 判讀紀錄 列印包', '父子科技學院 量子電腦學程 Q035｜色散位移 ±χ', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q035-dispersive-shift', folder='Q035_色散位移', files=FILES,
        sheet=('03_S21判讀紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_S21判讀紀錄.pdf', pack_pages=4,
        pack_needles=('S21 判讀紀錄', '改造表', '判讀練習單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q035', episode_dir='specials/q035-dispersive-shift',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（s21_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 's21_check.py',
               'recordedRun': {'mid_phase_deg': {str(x): round(R['MID'][x][1], 1) for x in R['MID']},
                               'mid_separation': {str(x): round(R['MID'][x][2], 3) for x in R['MID']},
                               'probe_-0.5': [round(v, 3) for v in R['PROBE'][-0.5]],
                               'quiz': R['QUIZ']},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q035/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

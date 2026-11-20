"""Q030 課堂教材：晶片尋寶圖、元件用途表、頻率表工作單、說明卡（列印）、解答、freq_plan.py、動畫導覽。

不需要帳號，也不需要安裝套件（freq_plan.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#chip 與 transmon-3d.html#chip。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q030/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q030：一條饋線串四個讀取腔的頻率表檢查器。

不用安裝任何套件，只要 Python 3。執行：  python freq_plan.py
- 把你設計的四個讀取腔頻率（GHz）寫進 PLAN，執行後會檢查：
  1. 都在 6–8 GHz 之間（簡報 JJ_Microwave_Readout_Talk p27：λ/4 諧振腔 fr ≈ 6–8 GHz）
  2. 相鄰兩個至少隔 MIN_GAP（本課自訂 50 MHz；動畫讀數寫典型凹陷寬度、狀態偏移約 1–5 MHz）
- 也估算每個讀取腔蛇形線的總路程：λ/4 共振腔的頻率和路程成反比，
  以簡報「約 4 mm ↔ 約 7 GHz」為基準：L ≈ 4 mm × 7 GHz ÷ f（只是數量級，沒有考慮材料與實際佈局）。
- 參考：animations/js/scenes/08_chip.js（四個讀取腔 6.82、6.97、7.11、7.26 GHz）。
"""

PLAN = [6.40, 6.60, 6.80, 7.00]   # ← 改成你的四個頻率（GHz）
MIN_GAP = 0.050                     # 本課自訂的安全距離：50 MHz
SCENE = [6.82, 6.97, 7.11, 7.26]    # 動畫 index.html#chip 的四個讀取腔


def path_mm(f):
    """以「約 4 mm ↔ 約 7 GHz」換算的蛇形線總路程（mm）。"""
    return 4.0 * 7.0 / f


def check(plan, min_gap=MIN_GAP):
    """回傳 (是否通過, 相鄰間隔 MHz 清單, 問題清單)。"""
    fs = sorted(plan)
    gaps = [round((b - a) * 1000) for a, b in zip(fs, fs[1:])]
    problems = []
    for f in fs:
        if not 6.0 <= f <= 8.0:
            problems.append(f'{f:.2f} GHz 不在 6–8 GHz 之間')
    for (a, b), g in zip(zip(fs, fs[1:]), gaps):
        if g < min_gap * 1000:
            problems.append(f'{a:.2f} 和 {b:.2f} GHz 只差 {g} MHz，太接近')
    return (not problems), gaps, problems


def report(name, plan):
    ok, gaps, problems = check(plan)
    print(f'{name}：' + '、'.join(f'{f:.2f}' for f in sorted(plan)) + ' GHz')
    print('  相鄰間隔：' + '、'.join(f'{g} MHz' for g in gaps))
    print('  蛇形線路程：' + '、'.join(f'{path_mm(f):.2f} mm' for f in sorted(plan)))
    print('  結果：' + ('通過' if ok else '不通過 → ' + '；'.join(problems)))
    return ok


print('一、動畫 index.html#chip 的頻率表')
SCENE_OK = report('動畫', SCENE)
print()
print('二、你的頻率表')
PLAN_OK = report('我的設計', PLAN)
print()
print('三、太接近的例子：兩個讀取腔只差 1 MHz')
CLOSE_OK = report('太接近', [6.80, 6.801, 7.00, 7.20])
print()
D1 = path_mm(6.82) - path_mm(6.97)
D2 = path_mm(7.11) - path_mm(7.26)
print(f'四、頻率差 150 MHz，路程差多少？6.82→6.97 GHz：{D1:.3f} mm；7.11→7.26 GHz：{D2:.3f} mm（都不到 0.1 mm）')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'freq_plan.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、動畫段、08_chip.js 相同
assert R['SCENE_OK'] and R['PLAN_OK'] and not R['CLOSE_OK']
assert R['check'](R['SCENE'])[1] == [150, 140, 150]
assert round(R['path_mm'](6.82), 2) == 4.11 and round(R['path_mm'](7.26), 2) == 3.86
assert round(R['D1'], 3) == 0.088 and round(R['D2'], 3) == 0.081

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q030：晶片長什麼樣子（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂在 Xmon 晶片上找出量子位元、讀取腔、饋線與控制線，理解頻率多工：
一顆量子位元是十字電容板加上 SQUID（兩個約瑟夫森接面）接地；XY 驅動線送約 5 GHz 微波轉動狀態，Z 磁通線改變 SQUID 的磁通調整頻率；
每顆量子位元配一個蜿蜒的 λ/4 讀取腔（約 4 mm、約 7 GHz），好幾個讀取腔共用一條饋線，靠不同頻率分開（頻率多工）。
下一堂 Q031 追查退相干的敵人。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 十字電容板與 SQUID、兩條控制線、讀取腔與饋線、頻率多工；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 晶片尋寶：爸爸念元件名字，孩子在列印的晶片圖上找到、用五種顏色圈起來、寫用途；再用 3D 動畫對照 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：設計一條饋線串四個讀取腔的頻率表，用 `freq_plan.py` 檢查 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替晶片圖取名字、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_晶片尋寶.pdf`（A4，共 4 頁）；準備紅、藍、綠、黃、紫五色筆；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#chip` 和 `transmon-3d.html#chip`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `freq_plan.py`（不需要安裝套件）。

## 驗收重點

1. 完成「標註好的晶片圖」：五種元件都圈出來、寫上用途，並有圖例和標題。
2. 不看稿說出核心原理：十字電容板＋SQUID 是量子位元；XY 轉狀態、Z 調頻率；讀取腔一端靠量子位元、一端靠饋線；頻率不同，一條饋線同時讀好幾顆。
3. 指出至少一個注意事項：晶片圖是示意、不按比例，實際佈局尺寸與元件數依廠商而不同；相鄰讀取腔頻率太接近，凹陷會疊在一起。

## 誠實說明

- 列印包的晶片圖是本課自己畫的示意圖，比照 3D 動畫的佈局，沒有按比例，也不是任何一家廠商的真實晶片。
- 「相鄰至少 50 MHz」是本課自訂的練習規則，不是業界標準；動畫的四個讀取腔相隔 140–150 MHz，場景說明寫「頻率差數十 MHz」。
- `freq_plan.py` 的路程用「約 4 mm ↔ 約 7 GHz」按比例換算，只是數量級。
- 動畫 index.html#chip 裡蛇形線繞的圈數只是示意：第四號繞最多圈，頻率卻最高，和「路程越遠頻率越低」相反（08_chip.js 第 37 行註解「此處僅示意」），可以拿來當「找錯」題。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：晶片尋寶（約 40 分鐘）

1. 拿出列印包第 1 頁的晶片尋寶圖，圖上有 8 個編號圓圈，每個指著一種元件（有的元件出現好幾次，只標一次）。
2. 爸爸念一個元件名字（量子位元的十字電容板、SQUID、讀取腔、饋線、XY 驅動線、Z 磁通線、接地面、放大器方向），孩子找出是哪個編號。
3. 用顏色圈起來：量子位元紅、讀取腔藍、饋線綠、XY 驅動線黃、Z 磁通線紫；把答案和用途填進第 2 頁的元件用途表。
4. 打開 `index.html#chip`：對照畫面上的 Q1–Q4、讀取腔、饋線；按「放大 Xmon」看十字下方的橘紅小環（SQUID）。
5. 打開 `transmon-3d.html#chip`：看一顆量子位元的標籤（XY 驅動線、Z 磁通線、讀取共振腔、饋線），按「送出 π 脈衝」看十字板亮起金光。
6. 替晶片圖加上圖例和標題，拍照存檔。

## 下半場：孩子改造——頻率表（約 30 分鐘）

1. 用列印包第 3 頁。一條饋線要串四個讀取腔，寫出四個頻率，放在 6–8 GHz 之間，相鄰至少差 50 MHz。
2. 把四個頻率寫進 `freq_plan.py` 的 PLAN，執行，看「通過／不通過」和每個讀取腔的蛇形線路程。
3. 試一個故意太接近的表（例如只差 1 MHz），說說讀取時會發生什麼事。
4. 加分題：打開 `index.html#chip`，按 Q1–Q4 按鈕，觀察右下頻譜小圖哪個凹陷移動。
''',

'freq_plan.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## freq_plan.py 實跑輸出（PLAN 為預設的範例頻率表）\n\n```\n' + RUN_LOG + '```\n\n'
  '## 晶片尋寶圖編號\n\n'
  '1 十字電容板（量子位元，提供大電容）　2 SQUID（兩個約瑟夫森接面，接到地）　3 讀取腔（λ/4 蜿蜒共平面波導，約 4 mm、約 7 GHz）　'
  '4 饋線（一條線串好幾個讀取腔）　5 XY 驅動線（送約 5 GHz 微波，轉動狀態）　6 Z 磁通線（改變 SQUID 磁通，調整頻率）　'
  '7 接地面（灰色的超導金屬）　8 OUT → 放大器（讀取訊號出去的方向）\n\n'
  '## 暫停題：兩個讀取腔只差 1 MHz 會怎樣？\n\n'
  '- 典型的凹陷寬度和量子位元狀態造成的偏移都有幾 MHz（動畫讀數：κ/2π、2χ/2π ≈ 1–5 MHz），兩個凹陷會疊在一起，'
  '看到頻譜變化時分不出是哪一顆量子位元換了狀態，讀一顆也可能干擾隔壁（簡報 p26「低串擾」）。\n\n'
  '## 說明範例\n\n'
  '> 我在晶片圖上找到四顆十字形的量子位元，每顆下面有 SQUID，左右有驅動線和磁通線，上面有一條蜿蜒的讀取腔，四個讀取腔都靠到同一條饋線。'
  '我設計的頻率是 6.40、6.60、6.80、7.00 GHz，相鄰差 200 MHz，比 50 MHz 大很多，凹陷不會疊在一起。這張圖是示意，真的晶片尺寸和數量依廠商不同。\n\n'
  '（範例只是示意，請寫你們自己的設計。）\n\n'
  '## 常見問題\n\n'
  '- 為什麼讀取腔要彎來彎去？約 4 mm 的線要塞進小小的晶片裡，彎成蛇形比較省空間。（本課推論；簡報寫的是「蜿蜒共面波導」）\n'
  '- 為什麼讀取腔頻率和量子位元不一樣？簡報 p28 的例子是量子位元約 5 GHz、讀取腔約 7 GHz，差很遠才不會直接交換能量；這部分在 Q035 詳談。\n'
  '- 十字為什麼要四隻手臂？分別靠近讀取腔、XY 驅動線、經 SQUID 接地、鄰近量子位元或耦合器，用距離調整耦合強度（transmon-3d 第 1 章）。\n'
  '- 有沒有不是十字的？transmon 簡報 p11 備註：IBM 等常用兩塊方形電容板的版本，原理相同。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。

## `transmon-3d.html#chip`（Transmon 3D 第 1 章：一顆 transmon 的俯視圖）

- 灰色接地面中間是十字電容板；標籤標出 SQUID（兩個約瑟夫森結）、Z 磁通線、XY 驅動線、讀取共振腔（~7 GHz）、饋線、接地面、基板。
- 按「送出 π 脈衝」：十字板亮起金光（激發到 |1⟩），再慢慢變暗（衰減回 |0⟩）。取消「顯示標籤」可以先自己猜，再打開對答案。
- 「大十字電容的作用」分頁說明四隻手臂各接什麼。

## `index.html#chip`（JJ 與微波讀取 3D 場景 8：晶片與多工讀取）

- 四顆 Xmon（Q1–Q4），每顆上方一條蜿蜒的讀取腔，都靠到最上面同一條饋線（左端 IN、右端 OUT → 放大器）。
- 饋線上的彩色光點是讀取脈衝，每 4.5 秒自動送一次；經過哪個讀取腔，那個讀取腔就閃青光。
- 左邊面板往下捲：按 Q1–Q4 切換 |0⟩／|1⟩，右下頻譜小圖對應的凹陷會從虛線左邊移到右邊；「放大 Xmon」「放大饋線耦合」可以拉近看細節，「視角：全晶片」回到全景。
- 讀數列出四個讀取腔的頻率 6.82、6.97、7.11、7.26 GHz。注意：動畫裡凹陷的寬度和移動距離是示意放大，蛇形線的圈數也只是示意。

## 之後的課

Q031「退相干：敵人在哪裡」會追查讓量子位元失去量子特性的雜訊來源。
''',
}

SHEET_HEADER = ['讀取腔', '頻率（GHz）', '和前一個差（MHz）', '蛇形線路程（mm）', '通過？']
SHEET_ROWS = [['1'], ['2'], ['3'], ['4']]

EXTRA_CSS = '''table.rec td{height:12mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.fig{display:block;margin:2mm auto 0}.cap{font-size:10.5pt;color:#35506b;margin:1mm 0 0}'''


def _chip_fig():
    """示意晶片圖（比照 index.html#chip 佈局，不按比例）：四個十字、蛇形讀取腔、饋線、控制線，8 個編號圓圈。"""
    s = ['<svg class="fig" width="175mm" height="128mm" viewBox="0 0 700 512" font-size="15" font-family="sans-serif">']
    s.append('<rect x="10" y="10" width="680" height="492" rx="8" fill="#d9dee6" stroke="#0b2540" stroke-width="2"/>')
    # 饋線
    s.append('<line x1="30" y1="70" x2="670" y2="70" stroke="#0b2540" stroke-width="7"/>')
    s.append('<rect x="14" y="58" width="22" height="24" fill="#c9a24a"/><rect x="664" y="58" width="22" height="24" fill="#c9a24a"/>')
    for i, x in enumerate((110, 270, 430, 590)):
        legs = 6
        top, bot = 100, 250
        dz = (bot - top) / legs
        pts = [(x - 50, 84), (x + 28, 84), (x + 28, top)]
        for k in range(legs):
            xx = x + (-28 if k % 2 == 0 else 28)
            pts += [(xx, top + dz * k), (xx, top + dz * (k + 1))]
        pts += [(x, bot), (x, 268)]
        s.append('<polyline fill="none" stroke="#0b2540" stroke-width="3" points="' + ' '.join(f'{a:.0f},{b:.0f}' for a, b in pts) + '"/>')
        s.append(f'<line x1="{x - 18}" y1="268" x2="{x + 18}" y2="268" stroke="#0b2540" stroke-width="4"/>')
        cy = 340
        s.append(f'<rect x="{x - 52}" y="{cy - 9}" width="104" height="18" fill="#fff" stroke="#0b2540" stroke-width="2"/>')
        s.append(f'<rect x="{x - 9}" y="{cy - 52}" width="18" height="104" fill="#fff" stroke="#0b2540" stroke-width="2"/>')
        s.append(f'<circle cx="{x}" cy="{cy + 66}" r="8" fill="none" stroke="#0b2540" stroke-width="3"/>')
        s.append(f'<polyline fill="none" stroke="#0b2540" stroke-width="2.5" points="{x + 78},490 {x + 78},{cy} {x + 60},{cy}"/>')
        s.append(f'<polyline fill="none" stroke="#0b2540" stroke-width="2.5" stroke-dasharray="7 3" points="{x - 34},490 {x - 34},{cy + 80} {x - 4},{cy + 80}"/>')
        s.append(f'<text x="{x - 46}" y="{cy - 22}" font-weight="bold">Q{i + 1}</text>')
    marks = [(1, 110 + 70, 300), (2, 270 + 36, 430), (3, 430 + 62, 170), (4, 90, 46), (5, 645, 440),
             (6, 110 - 56, 460), (7, 640, 250), (8, 640, 46)]
    for n, x, y in marks:
        s.append(f'<circle cx="{x}" cy="{y}" r="14" fill="#f5c242" stroke="#0b2540" stroke-width="2"/>'
                 f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-weight="bold">{n}</text>')
    s.append('<text x="130" y="42" fill="#35506b">讀取訊號：左邊進 → 右邊出　　（示意圖，不按比例）</text></svg>')
    return ''.join(s)


def html():
    pages = [
        '<h2>晶片尋寶圖</h2><p class="lead">找出 8 個編號各指著什麼元件，用五種顏色圈出來：量子位元紅、讀取腔藍、饋線綠、XY 驅動線黃、Z 磁通線紫。</p>'
        + _chip_fig() + '<p class="cap">提示：實線的控制線和虛線的控制線是兩種不同的線；圈數只是示意，不能拿來推算頻率。</p>',
        '<h2>元件用途表</h2><p class="lead">把尋寶的答案和用途填進來，再用 3D 動畫對照。</p>'
        '<table class="rec"><tr><th>編號</th><th>元件名稱</th><th>顏色</th><th>用途（一句話）</th><th>動畫對到了嗎？</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td></td><td></td><td></td><td></td></tr>' for n in range(1, 9)) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>圖例和標題：</p><div class="line"></div></div>',
        '<h2>頻率表工作單</h2><p class="lead">一條饋線串四個讀取腔：放在 6–8 GHz 之間，相鄰至少差 50 MHz（本課自訂的安全距離）。</p>'
        '<table class="rec"><tr>' + ''.join(f'<th>{h}</th>' for h in SHEET_HEADER) + '</tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<p class="cap">蛇形線路程 ≈ 4 mm × 7 ÷ 頻率（GHz）；可以用 freq_plan.py 檢查。</p>'
        '<div class="box" style="margin-top:4mm"><p>如果兩個讀取腔只差 1 MHz，會發生什麼事？</p><div class="line"></div>'
        '<p>頻率越高，蛇形線要變遠還是變近？</p><div class="line"></div>'
        '<p>動畫的四個頻率相隔多少？我的設計呢？</p><div class="line"></div></div>',
        '<h2>說明卡：我的晶片圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 晶片長什麼樣子在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿指出量子位元、讀取腔、饋線、XY 驅動線、Z 磁通線</li><li>說出 XY 和 Z 兩條線各管什麼</li>'
        '<li>說出頻率多工：一條饋線怎麼同時讀好幾顆</li><li>說出相鄰讀取腔的頻率為什麼要隔得夠遠</li>'
        '<li>指出一個注意事項：晶片圖是示意，尺寸與元件數依廠商而不同</li><li>替作品取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q030 晶片尋寶 列印包', '父子科技學院 量子電腦學程 Q030｜晶片長什麼樣子', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q030-chip-layout', folder='Q030_晶片長什麼樣子', files=FILES,
        sheet=('03_頻率表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_晶片尋寶.pdf', pack_pages=4,
        pack_needles=('晶片尋寶圖', '元件用途表', '頻率表工作單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q030', episode_dir='specials/q030-chip-layout',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（freq_plan.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'freq_plan.py',
               'recordedRun': {'scene_gaps_mhz': R['check'](R['SCENE'])[1],
                               'scene_path_mm': [round(R['path_mm'](f), 2) for f in R['SCENE']],
                               'example_plan': R['PLAN'], 'example_plan_ok': R['PLAN_OK'],
                               'path_diff_150mhz_mm': [round(R['D1'], 3), round(R['D2'], 3)]},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q030/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

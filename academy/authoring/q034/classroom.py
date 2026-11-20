"""Q034 課堂教材：電路 QED 示意圖、音叉／橡皮筋耦合紀錄、場景尋寶單、說明卡（列印）、解答、cqed_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（cqed_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#chip。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q034/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q034：電路 QED 小工具。

不用安裝任何套件，只要 Python 3。執行：  python cqed_check.py
- 一、頻率分得夠開嗎？失諧 Δ = f_q − f_r 和耦合強度 g 比一比（學程簡報 JJ_Microwave_Readout_Talk p28：|Δ| ≫ g 才是色散區域）。
- 二、動畫 index.html#chip 的四個讀取腔頻率與間隔（animations/js/scenes/08_chip.js 第 33 行）。
- 三、動畫右下角 |S21| 頻譜：每個凹陷在虛線左邊或右邊幾個像素（08_chip.js 第 97、100–101 行；core.js Plot.frame 邊界 46／12 px，插圖寬 380 px）。
"""

# 一、頻率分得夠開嗎？（GHz）
def detuning_ratio(f_q, f_r, g):
    """回傳 |Δ| / g；越大越像「只互推頻率、不交換能量」。"""
    return abs(f_q - f_r) / g


print('一、頻率分得夠開嗎？（|Δ| / g）')
RATIO = {}
for f_q, f_r, g in ((5.0, 7.0, 0.1), (6.5, 7.0, 0.1), (6.95, 7.0, 0.1), (7.0, 7.0, 0.1)):
    r = detuning_ratio(f_q, f_r, g)
    RATIO[(f_q, f_r)] = r
    tag = '分得很開（色散區域）' if r >= 10 else ('太接近：會直接交換能量' if r <= 1 else '介於中間')
    print(f'  量子位元 {f_q:.2f} GHz、讀取腔 {f_r:.2f} GHz、g = {1000 * g:.0f} MHz → |Δ|/g = {r:5.1f}　{tag}')

# 二、動畫的四個讀取腔
FR = [6.82, 6.97, 7.11, 7.26]
GAPS = [round(1000 * (b - a)) for a, b in zip(FR, FR[1:])]
print()
print('二、動畫 #chip 的四個讀取腔頻率（GHz）：' + '、'.join(f'{f:.2f}' for f in FR))
print('  相鄰間隔（MHz）：' + '、'.join(str(x) for x in GAPS))

# 三、右下角頻譜：凹陷偏離虛線幾個像素
CHI, KAP = 0.004, 0.006          # 08_chip.js 第 97 行（示意放大）
SHIFT = 6 * CHI                   # 第 101 行：|1⟩ → f_r + 6χ，|0⟩ → f_r − 6χ
W, L, R = 380, 46, 12
PX_PER_GHZ = (W - L - R) / (7.38 - 6.7)
DIP_PX = SHIFT * PX_PER_GHZ
FWHM_PX = (2 * KAP) * PX_PER_GHZ  # 1 − 0.85 / (1 + 4d²)，d = Δf / (2κ)：半深度在 |Δf| = κ
print()
print('三、動畫右下角 |S21| 頻譜')
print(f'  每 GHz 約 {PX_PER_GHZ:.0f} px；凹陷偏離虛線 {1000 * SHIFT:.0f} MHz ≈ {DIP_PX:.1f} px（|0⟩ 在左、|1⟩ 在右）')
print(f'  切換一顆量子位元，凹陷移動 {2 * DIP_PX:.1f} px；凹陷半深度寬約 {FWHM_PX:.1f} px')
print('  動畫的偏移是示意放大；場景讀數寫的典型值是 2χ/2π ≈ 1–5 MHz')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'cqed_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、動畫段、08_chip.js 數值相同
assert R['RATIO'][(5.0, 7.0)] == 20.0
assert R['GAPS'] == [150, 140, 150]
assert round(R['PX_PER_GHZ']) == 474 and round(R['DIP_PX']) == 11 and round(R['FWHM_PX']) == 6

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q034：電路 QED：量子位元＋諧振腔（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂用「角色扮演」認識電路量子電動力學（電路 QED）的三個零件：
量子位元（人造原子）、讀取諧振腔（讀取腔）、饋線。重點是：讀取不直接碰量子位元，而是看讀取腔——讀取腔的頻率隨量子位元的狀態偏一點，
我們從饋線送出來的訊號間接知道答案。作品是一張「電路 QED 示意圖」。下一堂 Q035 是色散位移 ±χ。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 借自原子物理、晶片上的三個零件、頻率要分開、讀取的路線、頻率多工；看 3D 動畫 | 影片第 2–8 段、`05_動畫導覽.md` |
| 25–65 | 敲音叉或撥橡皮筋看耦合；在 3D 場景指出量子位元、讀取腔、饋線；角色扮演 | 列印包第 2、3 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：畫量子位元、讀取腔、饋線三者的連接圖 | 列印包第 1 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替示意圖取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_電路QED示意圖.pdf`（A4，共 4 頁）。另備彩色筆。
- 兩支音高一樣的音叉（最好附共鳴箱），再一支音高不同的；沒有音叉就準備兩條橡皮筋和一個空紙盒或鞋盒。
- 讀一遍 `04_解答.md` 和學程筆記 `notes/dispersive-readout.md` 的第 0、1 節。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#chip`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `cqed_check.py`（不需要安裝套件）。

## 驗收重點

1. 完成「電路 QED 示意圖」：量子位元、讀取腔、饋線三者的連接，標出頻率（約 5 GHz、約 7 GHz）、耦合強度 g、漏出速度 κ、微波進出方向。
2. 不看稿說出核心原理：讀取不直接碰量子位元；讀取腔的頻率隨量子位元的狀態往下或往上偏一點，我們只看饋線送出來的訊號。
3. 指出至少一個注意事項：讀取腔與量子位元頻率要分得夠開，才不會直接交換能量。

## 誠實說明

- 耦合強度（電路約 50–200 MHz、原子 kHz–MHz）、讀取腔約 4 mm 與 6–8 GHz、量子位元約 5 GHz 取自學程簡報 p27、p28 與學程筆記的代表值。
- 音叉共鳴是課堂比喻：它說明「音高一樣才容易互相交換振動」，不是量子位元的物理模型。橡皮筋的效果可能很弱，照實記錄就好，不要編造結果。
- 動畫的頻率與頻譜偏移是示意，偏移有刻意放大。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：耦合與場景（約 40 分鐘）

1. 音叉：敲響一支，靠近另一支音高一樣的音叉（不要碰到），幾秒後按住敲過的那支讓它停，聽聽沒敲的那支有沒有在響。
   再換一支音高不同的音叉做一次。把結果寫在列印包第 2 頁。
2. 沒有音叉：兩條橡皮筋套在同一個空紙盒上，先拉成一樣緊，撥一條，看另一條有沒有跟著抖；再把其中一條拉得更緊（音高變高）做一次。
3. 想一想：哪一組像「量子位元和讀取腔頻率太接近」？哪一組像「分得夠開」？
4. 打開 `index.html#chip`，用列印包第 3 頁尋寶：在畫面上指出十字形的量子位元、彎來彎去的讀取腔、上方的饋線、十字下端的橘紅小環。
5. 角色扮演：一人當量子位元（手上拿一張寫著 0 或 1 的卡，不給別人看），一人當讀取腔（看了卡以後只用「高音」或「低音」哼一聲），
   一人當讀取的人（站在饋線另一頭，只能聽讀取腔的聲音）。輪流換角色。

## 下半場：孩子改造——畫連接圖（約 30 分鐘）

1. 用列印包第 1 頁畫電路 QED 示意圖：量子位元在一邊、饋線在另一邊、讀取腔夾在中間。
2. 標出：量子位元約 5 GHz、讀取腔約 7 GHz；量子位元和讀取腔靠近的地方寫 g，讀取腔和饋線靠近的地方寫 κ；微波從饋線左邊進、右邊出去放大器。
3. 挑戰：畫四顆量子位元共用一條饋線，替每個讀取腔標上不同的頻率（可以用動畫裡的 6.82、6.97、7.11、7.26 GHz）。
''',

'cqed_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## cqed_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 電路 QED 示意圖參考答案\n\n'
  '- 三個零件由左到右（或由下到上）：量子位元 → 讀取腔 → 饋線；讀取腔一頭靠近量子位元（耦合強度 g，電路約 50–200 MHz），'
  '另一頭靠近饋線（κ：讀取腔的光子漏到饋線的速率）。\n'
  '- 頻率：量子位元約 5 GHz、讀取腔約 7 GHz，相差約 2 GHz，遠大於 g（約 100 MHz）→ 色散區域：不交換能量、只互推頻率。\n'
  '- 微波：從饋線輸入端送入讀取腔附近頻率的脈衝，穿透出去後送往放大器；量子位元是 |0⟩ 或 |1⟩，讀取腔頻率往下或往上偏，訊號的相位、振幅跟著不同。\n'
  '- 挑戰：四個讀取腔頻率各不同（真實晶片相差數十 MHz；動畫用 6.82、6.97、7.11、7.26 GHz），共用一條饋線＝頻率多工。\n\n'
  '（簡報 JJ_Microwave_Readout_Talk p26、p27、p28、p29；學程筆記 notes/dispersive-readout.md §2.1、§2.2；場景 08_chip.js 說明第 6–8 行。）\n\n'
  '## 暫停題：哪一組音叉像讀取時的量子位元和讀取腔？\n\n'
  '- 音高一樣的兩支：敲一支，另一支也會響（共鳴，能量從一支傳到另一支）——像頻率太接近，兩者直接交換能量，這是讀取要避免的。\n'
  '- 音高不同的兩支：共鳴弱很多——像讀取時的量子位元和讀取腔：頻率分得夠開，不直接交換能量，讀取腔只當指示器。\n'
  '- 注意：音高剛好差八度時也容易共鳴（維基百科 Sympathetic resonance），挑音叉時避開。\n\n'
  '## 場景尋寶單答案（index.html#chip，全晶片視角）\n\n'
  '- 量子位元：四個十字形（標著 Q1–Q4）。讀取腔：十字上方彎來彎去的線（標籤「λ/4 讀取諧振腔」）。饋線：畫面最上方橫過整片晶片的線（「讀取饋線 IN」「OUT → 放大器」）。\n'
  '- 十字下端的橘紅小環：SQUID／約瑟夫森結（按「放大 Xmon」看得更清楚）。\n'
  '- 按 Q2 的按鈕切到 |1⟩：右下角第二個凹陷從虛線左邊移到右邊；讀數「腔頻 +χ」。\n\n'
  '## 常見問題\n\n'
  '- 為什麼不把量子位元直接接到饋線？直接接上量測設備會帶進耗散、破壞相干性；讓量子位元間接影響讀取腔，再用微波探測讀取腔（簡報 p26）。\n'
  '- 頻率太接近會怎樣？能量會在量子位元和讀取腔之間來回交換（色散區域外，筆記 §2.2），讀取腔不再只是指示器。\n'
  '- 為什麼叫「電路」量子電動力學？借自原子物理的共振腔 QED：原子換成超導人造原子，光學腔換成晶片上的微波諧振腔（簡報 p27；維基百科 Circuit quantum electrodynamics）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。
左邊面板很長，按鈕在下方，要往下捲。

## `index.html#chip`（JJ 與微波讀取 3D 場景 8：電路 QED 晶片：量子位元 + 讀取諧振腔）

- 四個十字形是量子位元（Xmon），十字上方彎來彎去的線是讀取諧振腔，最上方橫線是共用饋線；十字下端的橘紅小環是 SQUID／約瑟夫森結。
- 「自動重複讀取」預設開著：每 4.5 秒從饋線左端送出一串發光小球（讀取脈衝），經過時讀取腔會閃青光。
- 「Q1: |0⟩」…「Q4: |0⟩」按鈕切換各量子位元的狀態；右下角 |S21| 頻譜的凹陷會在虛線左邊（|0⟩）或右邊（|1⟩）。
- 「▶ 多工讀取（4 個頻率同時）」送四串、「只讀 Q2」只送第二串；「視角：全晶片」「放大 Xmon」「放大饋線耦合」換鏡頭。
- 讀數列出四個讀取腔的頻率 6.82、6.97、7.11、7.26 GHz；動畫裡的偏移有示意放大。

## 之後的課

Q035「色散位移 ±χ」會看讀取腔頻率怎麼隨量子位元狀態偏移 ±χ，並只看穿透訊號判讀狀態。
''',
}

SHEET_HEADER = ['零件', '在場景哪裡', '頻率', '靠近誰', '扮演什麼角色']
SHEET_ROWS = [['量子位元'], ['讀取腔'], ['饋線']]

EXTRA_CSS = '''.draw{height:120mm;border:1.3pt dashed #7f9bb3;border-radius:3mm;margin:3mm 0}
table.rec td{height:20mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.calc p{margin:2.5mm 0;font-size:12pt}'''


def html():
    pages = [
        '<h2>電路 QED 示意圖</h2><p class="lead">畫出量子位元、讀取腔、饋線三者的連接：讀取腔夾在中間。</p>'
        '<div class="draw"></div>'
        '<div class="box"><p>要標的東西：□ 量子位元約 5 GHz　□ 讀取腔約 7 GHz　□ 耦合強度 g　□ 漏出速度 κ　□ 微波從哪裡進、往哪裡出去（放大器）</p>'
        '<p>挑戰：四顆量子位元共用一條饋線，每個讀取腔標不同頻率。</p></div>',
        '<h2>耦合紀錄表：音叉或橡皮筋</h2><p class="lead">敲一支（撥一條），看另一支（另一條）有沒有跟著振動。照實記錄。</p>'
        '<table class="rec"><tr><th style="width:22%">組合</th><th>敲／撥哪一個</th><th>另一個有沒有響或抖？</th><th>多明顯（0–3）</th></tr>'
        '<tr><td>音高一樣</td><td></td><td></td><td></td></tr>'
        '<tr><td>音高不同</td><td></td><td></td><td></td></tr>'
        '<tr><td>橡皮筋一樣緊</td><td></td><td></td><td></td></tr>'
        '<tr><td>橡皮筋不一樣緊</td><td></td><td></td><td></td></tr></table>'
        '<div class="box calc" style="margin-top:4mm"><p>哪一組像「頻率太接近、直接交換能量」？＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>哪一組像「分得夠開，讀取腔只當指示器」？＿＿＿＿＿＿＿＿＿＿</p></div>',
        '<h2>場景尋寶單：index.html#chip</h2><p class="lead">在畫面上指出來，打勾，再寫一句它的工作。</p>'
        '<div class="box"><ul class="chk">'
        '<li>十字形的量子位元（有幾顆？＿＿）</li><li>彎來彎去的讀取腔</li><li>畫面上方的饋線（哪一頭進、哪一頭出？）</li>'
        '<li>十字下端的橘紅小環</li><li>每隔幾秒跑過饋線的光點</li><li>右下角頻譜的凹陷（有幾個？＿＿）</li></ul></div>'
        '<div class="box calc" style="margin-top:4mm"><h3>角色扮演</h3><p>量子位元：＿＿＿＿　讀取腔：＿＿＿＿　讀取的人：＿＿＿＿</p>'
        '<p>讀取的人猜對幾次？＿＿／＿＿　讀取的人有沒有直接看到卡片？＿＿</p></div>',
        '<h2>說明卡：我的電路 QED 示意圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 電路 QED：量子位元＋諧振腔在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>說出為什麼讀取要透過讀取腔</li><li>說出量子位元、讀取腔、饋線的角色</li>'
        '<li>說出頻率要分得夠開</li><li>在場景指出三個零件</li>'
        '<li>講解自己的示意圖</li><li>替示意圖取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q034 電路 QED 示意圖 列印包', '父子科技學院 量子電腦學程 Q034｜電路 QED：量子位元＋諧振腔', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q034-circuit-qed', folder='Q034_電路QED量子位元與諧振腔', files=FILES,
        sheet=('03_零件對照表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_電路QED示意圖.pdf', pack_pages=4,
        pack_needles=('電路 QED 示意圖', '耦合紀錄表', '場景尋寶單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q034', episode_dir='specials/q034-circuit-qed',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（cqed_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'cqed_check.py',
               'recordedRun': {'detuning_ratio_5_7GHz_g100MHz': R['RATIO'][(5.0, 7.0)],
                               'chip_resonator_gaps_MHz': R['GAPS'],
                               'inset_dip_offset_px': round(R['DIP_PX'], 1)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q034/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

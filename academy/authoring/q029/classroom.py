"""Q029 課堂教材：影子蒸鍍記錄表、紙橋製作與預測單、角度改造工作單、說明卡（列印）、解答、shadow_overlap.py、動畫導覽。

不需要帳號，也不需要安裝套件（shadow_overlap.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#fab。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q029/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q029：影子蒸鍍的重合寬度（和動畫 index.html#fab 同一套幾何）。

不用安裝任何套件，只要 Python 3。執行：  python shadow_overlap.py
- 紙橋（或光阻橋）離桌面（基板）的高度 h，照射角度 θ 從垂直方向量起。
- 每一邊的影子平移 s = h × tanθ（動畫讀數「影子平移 s = h·tanθ」）。
- 第一次從左邊照，亮區往右平移 s；第二次從右邊照，亮區往左平移 s。
  橋正下方兩次都照到的寬度 = 2s − 橋寬；小於 0 代表兩邊碰不到（沒有接面）。
- 這是理想的平行光；手電筒是點光源，實際影子會放大、邊緣模糊。
- 參考：學程簡報 JJ_Microwave_Readout_Talk p21–22；animations/js/scenes/07_fab.js。
"""
import math

H = 5.0       # 紙離桌面的高度（公分）
W = 2.0       # 紙橋寬度（公分）


def shift(h, deg):
    return h * math.tan(math.radians(deg))


def overlap(h, w, deg):
    """橋正下方兩次都照到的寬度（公分）；負數表示中間還差多少才碰得到。"""
    return 2 * shift(h, deg) - w


print(f'一、紙高 {H:.0f} 公分、橋寬 {W:.0f} 公分：照射角度與橋下重合寬度（理想平行光）')
print('角度   每邊平移     橋下重合')
TABLE = {}
for deg in range(5, 45, 5):
    o = overlap(H, W, deg)
    TABLE[deg] = o
    note = f'{o:5.2f} 公分' if o > 0 else f'碰不到（還差 {-o:.2f} 公分）'
    print(f' {deg:2d}°   {shift(H, deg):5.2f} 公分   {note}')

MIN_DEG = math.degrees(math.atan(W / (2 * H)))
print()
print(f'二、最小角度：tanθ = 橋寬 ÷（2 × 高度）→ θ = {MIN_DEG:.1f}°，比這個角度小，橋下就沒有重合')

print()
print('三、換一個高度（角度 20°）：紙架得越高，平移越多')
HEIGHTS = {}
for h in (3.0, 5.0, 8.0):
    HEIGHTS[h] = overlap(h, W, 20)
    print(f'  高 {h:.0f} 公分：每邊平移 {shift(h, 20):.2f} 公分，橋下重合 {overlap(h, W, 20):5.2f} 公分')

print()
print('四、動畫 index.html#fab 的幾何（場景單位）')
HB, HT, XB, S = 0.8, 0.25, 0.25, 0.55        # 07_fab.js 第 16、40 行
HEFF = HB + HT * 0.5                          # 第 77 行
THETA = math.degrees(math.atan(S / HEFF))
JJW = 2 * S - 2 * XB
print(f'  有效高度 h = {HEFF:.3f}、平移 s = {S}、蒸鍍角 θ = {THETA:.1f}°（讀數寫 31°）')
print(f'  橋寬 {2 * XB}，橋下重合寬 2s − 橋寬 = {JJW:.2f}（和金色重疊區的寬度一樣）')

print()
print('五、製程控制（簡報 p22）：f01 正比於 1/√R_n')
RATIO = 1.02 ** -0.5
print(f'  R_n 大 2 %：頻率變成 {RATIO:.4f} 倍，少 {(1 - RATIO) * 100:.2f} %；以 5 GHz 為例約少 {(1 - RATIO) * 5000:.1f} MHz')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'shadow_overlap.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、動畫段、07_fab.js 幾何相同
assert round(R['overlap'](5, 2, 20), 2) == 1.64 and round(R['overlap'](5, 2, 10), 2) == -0.24
assert round(R['MIN_DEG'], 1) == 11.3 and round(R['THETA']) == 31 and round(R['JJW'], 2) == 0.6
assert round((1 - R['RATIO']) * 100, 2) == 0.99 and round((1 - R['RATIO']) * 5000) == 49

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q029：晶片怎麼做：雙角度蒸鍍（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂認識約瑟夫森接面（JJ）怎麼做：雙層光阻做出一座懸空的光阻橋（Dolan bridge），
鋁從 +θ、−θ 兩個角度各蒸鍍一次，中間不破真空做原位氧化；影子讓兩層往相反方向平移，在橋的正下方重合，剝離（lift-off）後留下 Al / AlOx / Al 接面。
下一堂 Q030 看晶片長什麼樣子。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 接面的大小、雙層光阻與懸空橋、兩次斜角蒸鍍、氧化與剝離、氧化參數影響頻率；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 影子蒸鍍：做紙橋，手電筒左右各照一次，用兩色筆描出亮區，找橋下的重合區並拍照 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：改變照射角度，先預測再量出橋下重合寬度 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替影子蒸鍍作品取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 手電筒（光點越小越好，手機的手電筒也可以）、A4 厚紙或紙板、剪刀（由爸爸操作或在旁協助）、尺、量角器、鉛筆和兩種顏色的筆、幾本書（把紙架高用）、白紙一張墊在桌上。
- 列印 `02_列印包_影子蒸鍍.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#fab`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `shadow_overlap.py`（不需要安裝套件），對照預測。

## 安全

- 真實的接面製程在無塵室進行，要用顯影化學藥品、真空蒸鍍設備，家中絕對不要模仿，只做影子模擬。
- 手電筒不要直視、不要照別人的眼睛；剪刀由爸爸操作或在旁協助。

## 驗收重點

1. 完成「影子蒸鍍照片＋說明」：照片看得到兩色描線與紙橋下方的重合區，說明寫出照射角度、紙的高度、橋寬和量到的重合寬度。
2. 不看稿說出核心原理：懸空橋 → 第一次斜角蒸鍍（往一邊平移）→ 原位氧化 → 第二次反方向蒸鍍（往另一邊平移）→ 兩層在橋下重合 → 剝離。
3. 指出至少一個注意事項：真實製程使用化學藥品與真空設備，家中只做影子模擬；角度太小、兩邊碰不到就沒有接面；手電筒不是平行光，量到的寬度會和公式有差。

## 誠實說明

- 影子模擬只示範幾何上的平移與重合，不代表真實的尺寸：真實的接面只有約 100 × 200 nm²，光阻厚度與蒸鍍角也不同。
- 手電筒是點光源，影子會比紙大、邊緣模糊；手電筒拿遠一點（例如 50 公分以上）、光點小一點，結果會比較接近公式。
- 開口裡面也會有兩色都照到的地方（動畫裡第二層鋁在開口裡也有一段疊在第一層上）；本課只把紙橋正下方那一段當作「接面」，和簡報、動畫的金色標示一致。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：做紙橋、影子蒸鍍（約 40 分鐘）

1. 在厚紙中間畫兩個並排的方形開口（例如各 4 × 3 公分），兩個開口之間留一條 2 公分寬的紙條當「橋」；由爸爸剪下開口（列印包第 2 頁有尺寸圖）。
2. 桌上墊一張白紙，用兩疊一樣高的書把厚紙架高，讓紙離白紙約 5 公分，紙橋要平、不要下垂。量好高度寫在列印包第 1 頁。
3. 爸爸拿手電筒，從左邊斜斜照下來：用量角器或「高度與水平距離」對好角度（例如和垂直方向夾 20°）。手電筒盡量拿遠一點，光點小一點。
4. 孩子用鉛筆描出白紙上亮的區域。
5. 從右邊用同樣的角度再照一次，換另一色筆描。
6. 找紙橋正下方：兩種顏色都描到的那一小段，就是「接面」。量出它的寬度，拍照存檔。

## 下半場：孩子改造——改變照射角度（約 30 分鐘）

1. 用列印包第 3 頁。先寫預測：角度變大，橋下重合的寬度會變大還是變小？
2. 至少照三種角度（例如 10°、20°、30°），每種都左右各照一次、量重合寬度；10° 時兩邊可能碰不到。
3. 把量到的寬度和公式 2h·tanθ − 橋寬 比一比，寫下差在哪裡、為什麼（提示：手電筒不是平行光）。
4. 加分題：改變紙的高度或橋寬，再預測一次；跑 `shadow_overlap.py` 對照。
''',

'shadow_overlap.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## shadow_overlap.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 影子蒸鍍該看出什麼\n\n'
  '- 從左邊照，亮區往右平移；從右邊照，亮區往左平移。左開口的亮區會伸進紙橋下方的右邊一點，右開口的亮區會伸進紙橋下方的左邊一點，兩者在橋的正下方交會。\n'
  '- 角度越大、紙架得越高，平移越多，橋下重合越寬：寬度 ≈ 2h·tanθ − 橋寬。\n'
  '- 動畫 index.html#fab 也是同一套幾何：蒸鍍角約 31°、平移 0.55、橋寬 0.5，金色重疊區寬 0.6（場景單位）。\n\n'
  '## 暫停題：角度太小，橋下還會重合嗎？\n\n'
  '- 不會。兩邊的平移加起來（2h·tanθ）比橋寬還小時，兩層在橋下碰不到，中間留一條縫，就沒有接面。紙高 5 公分、橋寬 2 公分時，角度要大於約 11.3°。\n\n'
  '## 說明範例\n\n'
  '> 我們把紙架高 5 公分，紙橋寬 2 公分。手電筒從左右各斜照 20°，兩色在紙橋下面重合了大約 1.5 公分，比公式的 1.64 公分小一點，'
  '因為手電筒不是平行光、邊緣有點糊。照 10° 時兩邊碰不到，就沒有接面。真的晶片是在真空裡用鋁原子做，接面只有 100 × 200 奈米。\n\n'
  '（範例中的 1.5 公分只是示意，請寫你們實際量到的數字。）\n\n'
  '## 常見問題\n\n'
  '- 為什麼要兩層光阻？下層顯影比較快，會挖出底切，上層才會留下懸空的橋，橋下才有空間讓斜飛的鋁鑽進去（簡報 p21）。\n'
  '- 為什麼中間要氧化、而且不破真空？氧化鋁就是接面中間的絕緣層；不破真空直接通氧氣，氧化的壓力 × 時間決定厚度、也就決定電阻和臨界電流（簡報 p21）。\n'
  '- 剝離拿掉了什麼？光阻和光阻上面多餘的鋁；只留下直接落在基板上的兩層鋁線。\n'
  '- 為什麼頻率很難做準？f01 ∝ 1/√R_n，R_n 差 2 % 頻率就差約 1 %（約 50 MHz）；工程師在室溫先量 R_n 預測頻率，必要時用雷射或熱退火微調（簡報 p22）。\n'
  '- 還有別的做法嗎？簡報 p21 備註提到 Manhattan 法：兩條互相垂直的線各蒸鍍一次，不需要懸空橋。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。

## `index.html#fab`（JJ 與微波讀取 3D 場景 7：JJ 製程：Dolan bridge 雙角度蒸鍍）

- 打開時會自動依序播放五個步驟；左邊面板往下捲，按「1」～「5」可以直接跳到某一步（按了之後自動播放會關掉，想再自動播放就按「自動播放」）。
- 畫面上方的青色大字寫目前是第幾步：
  1. 電子束微影 + 顯影：紫色的上層光阻、淡藍色的下層光阻，開口中間有一座金色標籤的「懸空光阻橋」，下層標著「底切」。
  2. 第一次斜角蒸鍍：白色的鋁原子斜斜飛下來，光阻上面蓋上一層多餘的鋁。
  3. 原位氧化：橘紅色的氧氣分子幾乎垂直落下。
  4. 第二次斜角蒸鍍：鋁原子從相反的方向飛下來。
  5. 剝離：光阻往上飄走、淡掉，鏡頭拉近，金色閃爍的一小條就是接面（標籤「JJ：Al / AlOx / Al 重疊區」）。
- 面板讀數：蒸鍍角約 31°（影子平移 s = h·tanθ）、接面面積約 0.02 μm²、R_n 約 5–15 kΩ 等。
- 拖曳可以旋轉視角，按 R 重設視角；第二到四步時光阻上蓋著一層多餘的鋁，底部的鋁條不容易看清楚，到第五步剝離後最清楚。

## 之後的課

Q030「晶片長什麼樣子」會在 Xmon 晶片上找出量子位元、讀取腔、饋線與控制線。
''',
}

SHEET_HEADER = ['照射角度（度）', '紙高 h（公分）', '橋寬（公分）', '預測重合寬度（公分）', '量到的重合寬度（公分）']
SHEET_ROWS = [['10'], ['20'], ['30'], ['自己選'], ['自己選']]

EXTRA_CSS = '''table.rec td{height:13mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.fig{display:block;margin:2mm auto 0}.cap{font-size:10.5pt;color:#35506b;margin:1mm 0 0}'''


def _bridge_fig():
    """紙橋尺寸圖與照射示意（側視）。"""
    s = ['<svg class="fig" width="170mm" height="120mm" viewBox="0 0 680 480" font-size="15" font-family="sans-serif">']
    # 上視圖：厚紙與兩個開口
    s.append('<text x="20" y="24" font-weight="bold">上視圖（厚紙）</text>')
    s.append('<rect x="60" y="40" width="560" height="170" fill="#eef3f8" stroke="#0b2540" stroke-width="2"/>')
    s.append('<rect x="150" y="80" width="160" height="90" fill="#fff" stroke="#0b2540" stroke-width="2" stroke-dasharray="6 4"/>')
    s.append('<rect x="390" y="80" width="160" height="90" fill="#fff" stroke="#0b2540" stroke-width="2" stroke-dasharray="6 4"/>')
    s.append('<text x="230" y="130" text-anchor="middle">開口 4 × 3 公分</text><text x="470" y="130" text-anchor="middle">開口 4 × 3 公分</text>')
    s.append('<text x="350" y="125" text-anchor="middle" font-weight="bold">紙橋</text><text x="350" y="145" text-anchor="middle">2 公分</text>')
    s.append('<text x="340" y="200" text-anchor="middle" fill="#35506b">虛線剪開（爸爸操作）</text>')
    # 側視圖
    s.append('<text x="20" y="250" font-weight="bold">側視圖（照射示意）</text>')
    s.append('<line x1="40" y1="440" x2="640" y2="440" stroke="#0b2540" stroke-width="3"/><text x="600" y="465">桌面</text>')
    s.append('<line x1="150" y1="360" x2="310" y2="360" stroke="#0b2540" stroke-width="2" stroke-dasharray="6 4"/>')
    s.append('<line x1="60" y1="360" x2="150" y2="360" stroke="#0b2540" stroke-width="6"/>')
    s.append('<line x1="310" y1="360" x2="390" y2="360" stroke="#7a3fb0" stroke-width="6"/>')
    s.append('<line x1="550" y1="360" x2="620" y2="360" stroke="#0b2540" stroke-width="6"/>')
    s.append('<line x1="390" y1="360" x2="550" y2="360" stroke="#0b2540" stroke-width="2" stroke-dasharray="6 4"/>')
    s.append('<text x="350" y="350" text-anchor="middle" fill="#7a3fb0">紙橋</text>')
    s.append('<line x1="630" y1="360" x2="630" y2="440" stroke="#35506b"/><text x="636" y="405" fill="#35506b">h</text>')
    s.append('<line x1="200" y1="270" x2="350" y2="440" stroke="#e0a54a" stroke-width="2"/><text x="70" y="285" fill="#b07a20">第一次（左）</text>')
    s.append('<line x1="500" y1="270" x2="350" y2="440" stroke="#2a8fb0" stroke-width="2"/><text x="505" y="285" fill="#1f6f8a">第二次（右）</text>')
    s.append('<line x1="200" y1="270" x2="200" y2="330" stroke="#35506b" stroke-dasharray="3 3"/><text x="208" y="320" fill="#35506b">θ</text>')
    s.append('<rect x="325" y="432" width="50" height="10" fill="#f5c242"/><text x="350" y="425" text-anchor="middle" font-size="13">重合區</text></svg>')
    return ''.join(s)


def html():
    pages = [
        '<h2>影子蒸鍍記錄表</h2><p class="lead">手電筒從左、右兩邊用同樣角度各照一次，兩色描出亮區，量紙橋正下方的重合寬度。</p>'
        '<p>拿燈的人：＿＿＿＿＿＿　描影子的人：＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>紙高 h：＿＿＿ 公分　紙橋寬：＿＿＿ 公分　手電筒離紙約：＿＿＿ 公分</p>'
        '<table class="rec"><tr>' + ''.join(f'<th>{h}</th>' for h in SHEET_HEADER) + '</tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>照片編號：＿＿＿＿　橋下有沒有兩色重合？寬度是多少？</p><div class="line"></div></div>',
        '<h2>紙橋製作與照射示意</h2><p class="lead">照尺寸剪出兩個開口、留下 2 公分的紙橋；架高後從左右各照一次。</p>'
        + _bridge_fig() + '<p class="cap">安全：剪刀由爸爸操作或在旁協助；手電筒不要直視。真實製程使用化學藥品與真空設備，家中只做影子模擬。</p>',
        '<h2>角度改造工作單</h2><p class="lead">先預測，再照照看：角度改變，橋下的重合寬度怎麼變？</p>'
        '<div class="box"><p>我的預測：角度變大，重合寬度會（變大／變小／不變），因為：</p><div class="line"></div></div>'
        '<table class="rec" style="margin-top:3mm"><tr><th>角度</th><th>公式 2h·tanθ − 橋寬</th><th>量到的寬度</th><th>差多少？</th></tr>'
        + ''.join(f'<tr><td>{d}</td><td></td><td></td><td></td></tr>' for d in ('10°', '20°', '30°')) + '</table>'
        '<div class="box" style="margin-top:4mm"><p>角度太小時發生什麼事？</p><div class="line"></div>'
        '<p>量到的和公式差在哪裡？為什麼？</p><div class="line"></div>'
        '<p>如果要讓接面變寬，可以改什麼？</p><div class="line"></div></div>',
        '<h2>說明卡：我的影子蒸鍍</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 晶片怎麼做：雙角度蒸鍍在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出五個步驟：光阻橋、蒸鍍、氧化、蒸鍍、剝離</li><li>說出為什麼接面在橋的正下方</li>'
        '<li>說出角度、高度和重合寬度的關係</li><li>說出氧化參數會影響量子位元的頻率</li>'
        '<li>指出一個注意事項：真實製程有化學藥品與真空設備</li><li>替作品取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q029 影子蒸鍍 列印包', '父子科技學院 量子電腦學程 Q029｜晶片怎麼做：雙角度蒸鍍', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q029-double-angle-evaporation', folder='Q029_晶片怎麼做雙角度蒸鍍', files=FILES,
        sheet=('03_影子蒸鍍紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_影子蒸鍍.pdf', pack_pages=4,
        pack_needles=('影子蒸鍍記錄表', '紙橋製作與照射示意', '角度改造工作單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q029', episode_dir='specials/q029-double-angle-evaporation',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（shadow_overlap.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'shadow_overlap.py',
               'recordedRun': {'overlap_cm_h5_w2': {f'{d}': round(o, 2) for d, o in R['TABLE'].items()},
                               'min_angle_deg': round(R['MIN_DEG'], 1),
                               'scene': {'theta_deg': round(R['THETA'], 1), 'jj_width': round(R['JJW'], 2)},
                               'rn_2pct_freq_drop_pct': round((1 - R['RATIO']) * 100, 2)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q029/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

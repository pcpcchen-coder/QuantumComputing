"""Q006 課堂教材：水盆干涉實驗、光源安全卡、3D 場景相位預測、亮暗曲線與解答（不需帳號、不需安裝）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q006/classroom.py
"""
from pathlib import Path
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent


def p0(deg):
    """3D 場景 8 模式 A：出口零的機率 cos²(φ/2)。"""
    return math.cos(math.radians(deg) / 2) ** 2


PHASES = [0, 45, 90, 135, 180, 270, 360]
assert round(p0(45), 3) == 0.854 and round(p0(135), 3) == 0.146 and abs(p0(180)) < 1e-12


def bright(deg):
    p = p0(deg)
    return '最亮' if p > 0.99 else '全暗' if p < 0.01 else '一半一半' if abs(p - 0.5) < 0.01 else '比較亮' if p > 0.5 else '比較暗'


FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q006：干涉（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五分鐘，帶出今天的問題：波為什麼可以互相抵消？上一堂看不見的相位，怎麼變成看得見的亮和暗？

## 這份教材在做什麼

兩個實驗：水盆裡用兩支筆點水看干涉圖案、3D 場景裡拖相位看兩條路徑合起來的亮暗。孩子當實驗員，爸爸當安全官（光源只由爸爸操作），最後孩子自己挑相位、先預測再驗證。
當堂作品：一張干涉實驗照片，加上一句孩子自己寫的說明。不需要帳號；3D 場景見 `05_三維動畫導覽.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 水波相加、雙狹縫、振幅相加而不是機率相加 | 影片第 3–6 段 |
| 25–65 | 實驗一水盆（約 25 分鐘，拍照）＋實驗二 3D 場景（約 15 分鐘） | `01_實驗步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 改變路徑相位：先預測出口零變亮或變暗，再驗證、畫點 | 列印包第 3 頁、`03_實驗紀錄.csv` |
| 105–115 | 孩子教爸爸：為什麼波可以互相抵消 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替照片取名、寫一句說明、存檔 | |

## 課前準備（約 10 分鐘）

- 淺水盆（烤盤或洗菜盆，水深 1–2 公分）、兩支筆、一條橡皮筋、手電筒或手機燈、手機拍照。
- 選配：低功率雷射筆（第 2 級、標示 1 mW 以下的紅光），只由爸爸操作。
- 列印 `02_列印包_干涉.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。

## 安全官的原則

- 雷射筆只由爸爸拿；只往白牆或白紙照；絕對不直視、不照人、不照鏡子或亮面（反光也會進眼睛）。
- 第 2 級雷射筆靠「眨眼反射」保護眼睛，刻意盯著看一樣會受傷；不要買來路不明、標示不清的「強力」雷射筆。
- 水盆放在地上或穩固的桌面，旁邊不要有插座和電器；做完把水倒掉、擦乾地板。

## 檢查員的原則

- 孩子看不到平靜的線？多半是兩支筆不同步。用橡皮筋把兩支筆綁在一起，一起點，最穩。
- 手電筒從斜上方照水面，盆底會出現亮暗的花紋，比直接看水面清楚，也比較好拍。
- 孩子問「抵消的地方能量去哪了？」好問題：它沒有消失，而是分到旁邊加強的地方。
- 誤會要糾正：量子電腦不是「把所有答案同時試一遍」；它靠安排相位，讓錯的答案互相抵消、對的答案互相加強。

## 誠實說明

- 課綱提到「手機光源＋梳子」：梳齒間距大約一毫米，用手機白光照到牆上，主要看到的是梳齒的影子，不是乾淨的干涉條紋。可以把它當成討論題：「影子條紋」和「干涉條紋」有什麼不同？（影子：擋住的地方暗；干涉：光到得了的地方也可能變暗。）
- 真正的光干涉條紋需要很窄、很靠近的兩條縫和顏色單一的光（例如雷射）；本課以水盆為主，光的部分不強求。
- 3D 場景的「兩條路徑」在數學上等同物理實驗室的「Mach–Zehnder 干涉儀」；本課沒有實際的光學干涉儀。
''',

'01_實驗步驟.md': '''# 實驗步驟

## 實驗一：水盆裡的波（約 25 分鐘）

1. 在淺盆裡裝 1–2 公分的水，等水面完全靜下來。
2. 先用一支筆輕點水面一下，看一圈圈的波紋怎麼散開。寫在列印包第 1 頁。
3. 用橡皮筋把兩支筆並排綁好，筆尖相距約 3 公分，一起穩穩地、一下一下輕點水面。
4. 找兩組波紋交會處那些「幾乎不動的線」——那裡是波峰碰到波谷、互相抵消的地方。
5. 手電筒從斜上方照，看盆底的亮暗花紋；用手機拍照（可以拍影片再截圖）。
6. 改造：把筆尖分開到約 6 公分，或點快一點，平靜的線變多還是變少？記下來。
7. 選一張最清楚的照片，寫一句說明，例如：「兩組波在這些線上互相抵消，所以水面不動。」

## 選做：光的實驗（爸爸操作）

1. 關燈，爸爸把手機燈或手電筒照過梳子，投到白牆上，看到的是什麼？是影子，還是干涉條紋？
2. 有低功率雷射筆的話，由爸爸往白牆照，孩子站在雷射筆後面看牆上的點，不看雷射筆的出口。

## 實驗二：3D 場景（約 15 分鐘）

1. 打開 `animations/operation.html#interference`（場景 8：干涉），確認上面選的是「單一量子位元：兩條路徑」。
2. 把「A：相位 φ」拖到 0 度：最右上的大圓盤「結果 |0⟩」白色箭頭最長，P(0) = 1。
3. 慢慢拖到 180 度：上面白色箭頭縮短到不見，下面「結果 |1⟩」的白色箭頭變大。
4. 先猜，再按「A：中途偵測路徑（破壞干涉）」：兩個出口的機率變成多少？

## 下半場：改變路徑相位（約 30 分鐘）

1. 在列印包第 3 頁的表上，每個相位先寫預測：出口零會「最亮、比較亮、一半一半、比較暗、全暗」哪一種？
2. 把滑桿拖到那個相位，讀出 P(0)，寫在表上。
3. 在亮暗曲線格上畫點：橫軸是相位，縱軸是 P(0)。最後再打開「A：自動掃描 φ」，和右下角的曲線比一比。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 3D 場景 8：出口零的機率 P(0) = cos²(φ/2)\n\n'
  + '| 相位 | P(0) | 亮暗 |\n|---|---|---|\n'
  + ''.join(f'| {a} 度 | {p0(a):.3f} | {bright(a)} |\n' for a in PHASES)
  + '\n打開「中途偵測路徑」後：不管相位是多少，P(0) = P(1) = 0.5（干涉消失，只剩機率相加）。\n\n'
  '## 振幅相加（量子電路範例 2：H‑Z‑H）\n\n'
  '- 沒有 Z：到 0 的兩條路 ½ + ½ = 1，到 1 的兩條路 ½ − ½ = 0 → 一定得到 0。\n'
  '- 有 Z（相位 180 度）：到 0 的兩條路 ½ − ½ = 0，到 1 的兩條路 ½ + ½ = 1 → 一定得到 1。\n'
  '- 如果只把機率相加：每條路各 ¼，兩條路合起來是 ½，永遠是一半一半，不會出現 0 或 1。\n\n'
  '## 水盆\n\n'
  '- 平靜的線：兩組波的波峰碰到波谷的地方。\n'
  '- 兩支筆分開一點，或點快一點（波峰之間的距離變小），平靜的線通常會變多、變密。實際水盆會受手的節奏、盆邊反射影響，看不清楚很正常。\n\n'
  '## 常見問題\n\n'
  '- 「量子電腦是不是同時試所有答案？」不是。最後只量得到一個結果；量子演算法靠干涉，讓錯的答案抵消、對的答案加強。\n'
  '- 「梳子照出來的條紋是干涉嗎？」多半是影子。影子是被擋住才暗；干涉是光到得了的地方也會因為抵消而變暗。\n',

'05_三維動畫導覽.md': '''# 三維動畫導覽

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## 今天要看的場景 1：`animations/operation.html#interference`（場景 8：干涉）

- 「單一量子位元：兩條路徑」：左邊起點分成上下兩條路，下面那條經過紫色的「相位 φ」方塊，最後在右邊兩個大圓盤合起來。
- 大圓盤裡：藍箭頭是經由上面那條路的貢獻、橙箭頭是經由下面那條路的貢獻，白箭頭是兩者頭尾相接的總和。
- 「A：相位 φ」滑桿：改變下面那條路多轉的相位。
- 「A：自動掃描 φ」：相位自己一圈一圈轉；右下角小圖的白點沿著亮暗曲線（干涉條紋）跑。
- 「A：中途偵測路徑（破壞干涉）」：偷看走哪條路，白箭頭消失，機率變成一半一半。
- 「3 位元：8 條路徑」：進階，八支箭頭頭尾相接，可以完全加強或完全抵消。

## 今天要看的場景 2：`animations/basic-circuits.html#interference`（範例 2：干涉）

- 按「下一步 ▶」逐步看：疊加 → 只改正負號 → 再混合；藍色柱子是正振幅、銅色是負振幅。
- 上方「中間的閘」切換「有 Z／沒有 Z」，結果從一定是 1 變成一定是 0。

## 操作

滑鼠拖曳旋轉、滾輪縮放；`H` 隱藏面板；`R` 重設視角。
''',
}

SHEET_HEADER = ['實驗', '條件', '預測', '觀察或 P(0)', '亮暗', '一句說明']
SHEET_ROWS = ([['水盆', '一支筆'], ['水盆', '兩支筆（相距約 3 公分）'], ['水盆', '兩支筆（相距約 6 公分）'], ['水盆', '點快一點']]
              + [['3D 場景', f'相位 {a} 度'] for a in (0, 45, 90, 135, 180)]
              + [['3D 場景', '偵測路徑（任一相位）']]
              + [['我選的相位', '＿＿度'] for _ in range(2)])

EXTRA_CSS = '''table.rec td{height:11mm}table.obs td{height:17mm}
.photo{border:1.2pt dashed #7f9bb3;border-radius:3mm;height:62mm;display:flex;align-items:center;justify-content:center;color:#7f9bb3;font-size:12pt}
.plot{height:80mm;border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;margin:3mm 0 0 10mm;position:relative;
background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt),linear-gradient(90deg,#cfdde8 .6pt,transparent .6pt);background-size:100% 10mm,12.5% 100%}
.ylab{position:absolute;left:-10mm;font-size:9pt;color:#4a6a88}.xlab{display:flex;justify-content:space-between;margin-left:10mm;font-size:9pt;color:#4a6a88}
.chk li{margin:2.6mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.warn{border:2pt solid #c0392b;border-radius:3mm;padding:3mm 4.5mm}.warn h3{color:#c0392b}'''


def html():
    pages = [
        '<h2>實驗一：水盆裡的波</h2><p class="lead">淺盆裝 1–2 公分的水。兩支筆用橡皮筋綁在一起，同時輕點水面。</p>'
        '<table class="obs"><tr><th>怎麼點</th><th>我先猜會看到</th><th>我真的看到</th></tr>'
        '<tr><td>一支筆</td><td></td><td></td></tr><tr><td>兩支筆（相距約 3 公分）</td><td></td><td></td></tr>'
        '<tr><td>兩支筆分開（約 6 公分）</td><td></td><td></td></tr><tr><td>點快一點</td><td></td><td></td></tr></table>'
        '<h3 style="margin-top:5mm">我的干涉照片（貼上或印出來）</h3><div class="photo">照片貼這裡</div>'
        '<p style="margin-top:3mm">照片名稱：＿＿＿＿＿＿＿＿＿＿＿＿　一句說明：</p><div class="line"></div>',
        '<h2>光的實驗：安全官（爸爸）操作</h2>'
        '<div class="warn"><h3>雷射安全卡</h3><ul class="chk">'
        '<li>雷射筆只由爸爸拿</li><li>只往白牆或白紙照</li><li>絕對不直視、不照人、不照動物</li>'
        '<li>不照鏡子、玻璃或亮亮的表面</li><li>用完馬上關掉、收好</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>影子還是干涉？</h3>'
        '<p>爸爸用手機燈照過梳子，投到牆上。牆上的條紋是：□ 影子　□ 干涉條紋　□ 不確定</p>'
        '<p>我的理由：</p><div class="line"></div>'
        '<p class="note">提示：影子是被擋住才暗；干涉是光到得了的地方，也可能因為抵消而變暗。</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>雙狹縫：連連看</h3>'
        '<table><tr><th>做法</th><th>牆上看到</th></tr><tr><td>光穿過一條縫</td><td></td></tr>'
        '<tr><td>光穿過兩條縫</td><td></td></tr><tr><td>電子一次只送一顆，送很多顆</td><td></td></tr>'
        '<tr><td>查每一顆走哪條縫</td><td></td></tr></table>'
        '<p class="note">選項：一片亮光／亮暗條紋／也排出條紋／條紋不見</p></div>',
        '<h2>下半場：改變相位，預測亮或暗</h2><p class="lead">打開 animations/operation.html#interference。先寫預測，再拖「A：相位 φ」讀出 P(0)。</p>'
        '<table class="rec"><tr><th>相位</th><th>我預測出口零</th><th>P(0)</th><th>猜中了嗎</th></tr>'
        + ''.join(f'<tr><td>{a} 度</td><td></td><td></td><td></td></tr>' for a in (0, 45, 90, 135, 180))
        + '<tr><td>我選：＿＿度</td><td></td><td></td><td></td></tr><tr><td>我選：＿＿度</td><td></td><td></td><td></td></tr></table>'
        '<p class="note">預測用這五個詞：最亮、比較亮、一半一半、比較暗、全暗。</p>'
        '<div class="plot"><span class="ylab" style="top:-2mm">1</span><span class="ylab" style="top:38mm">0.5</span>'
        '<span class="ylab" style="bottom:-2mm">0</span></div>'
        '<div class="xlab"><span>0 度</span><span>90</span><span>180</span><span>270</span><span>360 度</span></div>',
        '<h2>最後一關：教爸爸什麼是干涉</h2><div class="box"><ul class="chk">'
        '<li>說出兩道波什麼時候變大、什麼時候抵消</li><li>說出雙狹縫查走哪條縫，條紋會怎樣</li>'
        '<li>說出為什麼機率不能直接相加</li><li>說出相位怎麼決定出口零的亮或暗</li>'
        '<li>指出一個誤會：量子電腦不是同時試所有答案</li><li>說出一條雷射安全規則</li>'
        '<li>替干涉照片取名字、寫一句說明、存檔</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>振幅相加（兩條路到同一個出口）</h3>'
        '<table><tr><th></th><th>到出口零</th><th>到出口一</th></tr>'
        '<tr><td>相位 0 度</td><td>½ + ½ = ＿＿</td><td>½ − ½ = ＿＿</td></tr>'
        '<tr><td>相位 180 度</td><td>½ − ½ = ＿＿</td><td>½ + ½ = ＿＿</td></tr></table>'
        '<p class="note">振幅像箭頭，方向相反就抵消。先加振幅，再算機率。</p></div>',
    ]
    return printpack.document('Q006 干涉 列印包', '父子科技學院 量子電腦學程 Q006｜干涉', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q006-interference-waves', folder='Q006_干涉', files=FILES,
        sheet=('03_實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_干涉.pdf', pack_pages=4,
        pack_needles=('水盆裡的波', '干涉照片', '雷射安全卡', '影子還是干涉', '預測亮或暗', '最後一關'),
        authoring_dir=XINEW / 'authoring/q006', episode_dir='specials/q006-interference-waves',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'p0ByPhase': {a: round(p0(a), 4) for a in PHASES}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q006/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

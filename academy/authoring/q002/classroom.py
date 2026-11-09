"""Q002 課堂教材：紙的布洛赫球做法與圖樣、人肉布洛赫球指令卡、角度預測紀錄、解答（不需帳號、不需安裝）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q002/classroom.py
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
ANGLES = [0, 30, 45, 60, 90, 120, 135, 150, 180]


def p0(deg):
    return math.cos(math.radians(deg) / 2) ** 2


assert abs(p0(60) - 0.75) < 1e-9 and abs(p0(90) - 0.5) < 1e-9

# 人肉布洛赫球指令卡：(卡片文字, 手臂該指向)
CARDS = [
 ('狀態零', '正上方（北極）'), ('狀態一', '正下方（南極）'), ('一半一半', '水平指向前方（赤道）'),
 ('一半一半，相位轉四分之一圈', '水平指向側邊（赤道上另一點）'), ('角度六十度', '從頭頂往前傾六十度'),
 ('角度一百二十度', '比水平再往下三十度'), ('角度三十度', '從頭頂往前傾一點點'), ('角度一百五十度', '接近正下方'),
 ('得到零的機會四分之三', '六十度'), ('得到一的機會四分之三', '一百二十度'), ('一定得到一', '一百八十度，正下方'),
 ('你自己出一題', '請爸爸指'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q002：硬幣與箭頭（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五分鐘，帶出今天的問題：量子位元和一般的位元差在哪裡？

## 這份教材在做什麼

用紙盤和竹籤做一顆布洛赫球，把「量子位元是一支箭頭」變成拿在手上的東西；再用身體當箭頭玩指令卡，最後自己選角度、預測、用 3D 場景驗證。
不需要帳號；第 75–105 分鐘要開 3D 場景（見 `05_三維動畫導覽.md`）。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 硬幣 vs 箭頭、角度決定機率、相位 | 影片第 3–7 段 |
| 25–65 | 做紙球（約 25 分鐘）＋人肉布洛赫球（約 15 分鐘） | `01_紙球做法.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 自己選角度、寫預測、3D 場景跑一千次驗證 | 列印包第 3 頁、`03_角度預測紀錄.csv` |
| 105–115 | 孩子教爸爸：量子位元是什麼 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替紙球取名字 | |

## 課前準備（約 10 分鐘）

- 紙盤兩個（直徑 18–23 公分）、竹籤一支（剪到比紙盤直徑短一點）、一小塊黏土或保麗龍球、膠帶、彩色筆、剪刀（爸爸操作）。
- 列印 `02_列印包_硬幣與箭頭.pdf`（A4，共 4 頁），第 2 頁剪成 12 張指令卡。
- 讀一遍 `04_角度與機率解答.md`。

## 守門人的原則

- 孩子說「疊加就是同時是零又是一」時，不要說錯，請他用紙球指出「那個方向在哪裡」。
- 相位這堂只要知道「轉了看不出來」就好，之後干涉的課才會用到。

## 誠實說明

- 布洛赫球是畫圖的方法。對超導量子位元來說，晶片裡沒有一支真的箭頭；對電子自旋，箭頭方向才對應空間中的方向。
- 角度與機率的對應用的是 P(0) = cos²(θ/2)，解答表的百分比四捨五入到小數一位。
''',

'01_紙球做法.md': '''# 紙的布洛赫球：做法（約 25 分鐘）

## 材料

紙盤 2 個、竹籤 1 支、黏土或保麗龍球 1 小塊、膠帶、彩色筆、剪刀（爸爸操作）。

## 步驟

1. **剪縫**：兩個紙盤各從邊緣剪一條直線到圓心（沿著列印包第 1 頁圖樣的虛線）。
2. **十字交叉**：把兩個紙盤從剪縫互相插進去，變成一個立體的十字球。用膠帶固定。
3. **畫赤道**：在其中一個紙盤上，畫一條穿過圓心、和另一個紙盤垂直的線，這是赤道。
4. **標極點**：最上面寫「0」（北極、狀態零），最下面寫「1」（南極、狀態一）。
5. **裝箭頭**：在圓心黏一小塊黏土，竹籤插進去當箭頭，尖端可以轉向任何方向。
6. **畫角度**：從北極往南極，每 30 度畫一個小刻度：0、30、60、90（赤道）、120、150、180。

## 檢查

- 箭頭指北極：這是狀態零。
- 箭頭指南極：這是狀態一。
- 箭頭指赤道：這是一半一半的疊加。
- 箭頭繞著赤道轉：這是相位在變；測量得到零和一的機會不會改變。
''',

'04_角度與機率解答.md': '# 角度與機率解答（爸爸用）\n\n角度是箭頭離北極的角度；得到零的機會 = cos²(角度 ÷ 2)。\n\n'
  + '| 角度 | 得到零 | 得到一 | 一千次大約幾次零 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} 度 | {p0(a) * 100:.1f}% | {(1 - p0(a)) * 100:.1f}% | {round(p0(a) * 1000)} |\n' for a in ANGLES)
  + '\n實際跑一千次，次數會在附近上下跳，例如一半一半的狀態大約差 16 次左右；下一堂會仔細講。\n\n'
  + '## 人肉布洛赫球指令卡答案\n\n| 卡片 | 手臂指向 |\n|---|---|\n'
  + ''.join(f'| {c} | {a} |\n' for c, a in CARDS),

'05_三維動畫導覽.md': '''# 三維動畫導覽

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## 今天要看的場景：`animations/operation.html#qubit`（場景 1：狀態與測量）

1. 按「|0⟩」「|1⟩」「|+⟩」按鈕，看箭頭跳到北極、南極、赤道。
2. 拉「θ（極角）」滑桿：箭頭上下移動，右邊的理論機率（青線）跟著變。
3. 拉「φ」滑桿：箭頭繞著赤道轉，理論機率完全不變——這就是相位看不出來。
4. 選好角度後，按「一次跑 1000 shots」，記下得到 0 和得到 1 的次數。

## 操作

滑鼠拖曳旋轉、滾輪縮放；`H` 隱藏面板；`R` 重設視角。
''',
}

SHEET_HEADER = ['角度', '我的預測（零比一半多／少／一半）', '理論得到零（%）', '一千次實測零的次數', '實測比例（%）', '差多少']
SHEET_ROWS = [[f'{a}', '', f'{p0(a) * 100:.1f}'] for a in ANGLES] + [['我自己選：', ''] for _ in range(3)]

EXTRA_CSS = '''.svgbox{display:flex;justify-content:center;margin-top:4mm}
.cards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:3mm}.cc{height:52mm;padding:4mm;position:relative;display:flex;align-items:center;justify-content:center;text-align:center}
.cc b{position:absolute;top:2.2mm;left:4mm;font-size:11pt;color:#35a9d6}.cc p{font-size:16pt;font-weight:700;margin:0}
table.rec td{height:12mm}.chk li{margin:3mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def plate_svg():
    ticks = ''.join(
        f'<line x1="{100 + 92 * math.sin(math.radians(a)):.1f}" y1="{100 - 92 * math.cos(math.radians(a)):.1f}" '
        f'x2="{100 + 84 * math.sin(math.radians(a)):.1f}" y2="{100 - 84 * math.cos(math.radians(a)):.1f}" stroke="#0b2540" stroke-width="1.2"/>'
        f'<text x="{100 + 72 * math.sin(math.radians(a)):.1f}" y="{104 - 72 * math.cos(math.radians(a)):.1f}" font-size="7" text-anchor="middle">{a}°</text>'
        for a in (30, 60, 120, 150))
    return ('<svg width="150mm" height="170mm" viewBox="0 -14 200 228" font-family="Noto Sans CJK TC">'
            '<circle cx="100" cy="100" r="92" fill="none" stroke="#0b2540" stroke-width="1.6"/>'
            '<line x1="8" y1="100" x2="192" y2="100" stroke="#35a9d6" stroke-width="1.4"/>'
            '<line x1="100" y1="100" x2="100" y2="192" stroke="#0b2540" stroke-width="1.2" stroke-dasharray="4 3"/>'
            '<text x="100" y="2" font-size="11" text-anchor="middle" font-weight="700">0（北極）</text>'
            '<text x="100" y="208" font-size="11" text-anchor="middle" font-weight="700">1（南極）</text>'
            '<text x="165" y="95" font-size="8" text-anchor="middle" fill="#35a9d6">赤道（90°）</text>'
            '<text x="112" y="150" font-size="7" fill="#4a6a88">剪縫（剪到圓心）</text>'
            '<circle cx="100" cy="100" r="2.5" fill="#f0a020"/>' + ticks + '</svg>')


def html():
    pages = [
        '<h2>紙盤圖樣</h2><p class="lead">把圖樣疊在紙盤上描下來：虛線是剪縫，藍線是赤道，刻度是離北極的角度。兩個紙盤都要剪縫。</p>'
        f'<div class="svgbox">{plate_svg()}</div><p class="note">另一個紙盤只要剪縫，不用畫赤道。黏土放在圓心（黃點），竹籤插進去當箭頭。</p>',
        '<h2>人肉布洛赫球指令卡</h2><p class="lead">沿虛線剪下。爸爸抽一張唸出來，你用手臂當箭頭指出來，再用紙球擺一次。</p>'
        '<div class="cards">' + ''.join(f'<div class="cut cc"><b>{i}</b><p>{c}</p></div>' for i, (c, _) in enumerate(CARDS, 1)) + '</div>',
        '<h2>角度預測紀錄表</h2><p class="lead">先寫預測，再到 3D 場景把角度調好，按「一次跑 1000 shots」，記下得到零的次數。</p>'
        '<table class="rec"><tr><th>角度</th><th>預測：零比一半多／少／一半</th><th>一千次裡零的次數</th><th>比例</th><th>和預測一樣嗎？</th></tr>'
        + ''.join(f'<tr><td>{a} 度</td><td></td><td></td><td></td><td></td></tr>' for a in (30, 60, 120, 150))
        + '<tr><td>我選：＿＿度</td><td></td><td></td><td></td><td></td></tr><tr><td>我選：＿＿度</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p class="note" style="margin-top:4mm">想一想：轉動相位（φ）之後，零的次數會變嗎？</p>',
        '<h2>最後一關：用紙球教爸爸</h2><div class="box"><ul class="chk">'
        '<li>說出位元和量子位元差在哪裡（硬幣和箭頭）</li><li>用紙球擺出狀態零</li><li>用紙球擺出狀態一</li>'
        '<li>用紙球擺出一半一半</li><li>說出相位轉了，測量機率會不會變</li>'
        '<li>說出一個限制：超導量子位元的晶片裡沒有真的箭頭</li><li>替紙球取名字、拍照存檔</li></ul></div>'
        '<div class="box" style="margin-top:6mm"><h3>我的紙球名字</h3><div class="line"></div>'
        '<h3 style="margin-top:4mm">今天我學到的一句話</h3><div class="line"></div><div class="line"></div></div>',
    ]
    return printpack.document('Q002 硬幣與箭頭 列印包', '父子科技學院 量子電腦學程 Q002｜硬幣與箭頭', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q002-coin-and-arrow', folder='Q002_硬幣與箭頭', files=FILES,
        sheet=('03_角度預測紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_硬幣與箭頭.pdf', pack_pages=4,
        pack_needles=('紙盤圖樣', '北極', '南極', '人肉布洛赫球指令卡', '角度預測紀錄表', '最後一關'),
        authoring_dir=XINEW / 'authoring/q002', episode_dir='specials/q002-coin-and-arrow',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False, 'commandCards': len(CARDS),
               'angleTable': {a: round(p0(a), 4) for a in ANGLES}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q002/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

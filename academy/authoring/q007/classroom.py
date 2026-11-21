"""Q007 課堂教材：米粒杯子、2ⁿ 記憶體競速對照表、自家電腦計算單、解答（不需帳號、不需安裝）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q007/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent
BYTES = 16  # 一個複數振幅＝兩個雙精度數（8 位元組）


def amps(n):
    return 2 ** n


def mem(n):
    return amps(n) * BYTES


def human(b):
    """以 1024 進位表示（電腦標示的記憶體容量即為此慣例）。"""
    for unit in ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB'):
        if b < 1024:
            return f'{b:g} {unit}'
        b /= 1024
    return f'{b:g} ZB'


def max_qubits(ram_gb):
    """記憶體（GB，1024 進位）÷ 16 後能除以二幾次。"""
    x, n = ram_gb * 1024 ** 3 // BYTES, 0
    while x >= 2:
        x //= 2
        n += 1
    return n


def laptops(n):
    r = mem(n) / LAPTOP
    return '不到一台' if r < 1 else f'{round(r):,}'


TABLE_N = [1, 2, 3, 4, 5, 10, 20, 30, 40, 50]
RAMS = [4, 8, 16, 32, 64]
LAPTOP = 16 * 1024 ** 3
assert human(mem(30)) == '16 GB' and human(mem(40)) == '16 TB' and human(mem(50)) == '16 PB'
assert mem(40) // LAPTOP == 1024 and mem(50) // LAPTOP == 1048576
assert max_qubits(16) == 30 and max_qubits(8) == 29 and amps(50) == 1125899906842624

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q007：兩顆、三顆、五十顆（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五分鐘，帶出今天的問題：量子位元越來越多，要記住的振幅會變成多少？

## 這份教材在做什麼

兩個活動：用米粒和杯子數出 1 到 5 個量子位元有幾種組合；再和孩子用計算機比賽，算出 1 到 50 個量子位元需要多少記憶體，完成「2ⁿ 記憶體對照表」。
下半場孩子查自家電腦的記憶體，算出最多能精確模擬幾個量子位元。不需要帳號；3D 場景見 `05_三維動畫導覽.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 組合翻倍、每種組合一個振幅、每個振幅 16 位元組 | 影片第 3–6 段、3D 場景 4 |
| 25–65 | 活動一米粒杯子（約 15 分鐘）＋活動二記憶體競速（約 25 分鐘） | `01_活動步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 查自家電腦記憶體，算出最多幾個量子位元 | 列印包第 3 頁、`03_記憶體對照表.csv` |
| 105–115 | 孩子教爸爸：為什麼普通電腦模擬不了太多量子位元 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名 | |

## 課前準備（約 5 分鐘）

- 米粒一小碗、杯子（至少 8 個，紙杯或小碟都可以）、計算機兩台（手機計算機也可以）、鉛筆；列印 `02_列印包_兩顆三顆五十顆.pdf`（A4，共 4 頁）。
- 讀一遍 `04_解答與對照表.md`。

## 裁判的原則

- 計算機到二十幾顆就會出現很長的數字或科學記號，這正是「爆炸」的感覺，可以一起讀出來。
- 檢查法：2¹⁰ = 1024 ≈ 1000，所以每多 10 顆，答案大約多三個零（KB → MB → GB → TB → PB）。
- 孩子說「五十顆量子位元可以一次算出一千兆個答案」時，請追問：測量一次能讀到幾個零或一？（答案：五十個。）

## 誠實說明

- 這裡算的是「把全部振幅存下來」的精確模擬（每個振幅用兩個雙精度數，16 位元組）。科學家還有張量網路等捷徑，可以處理糾纏不多的線路；本課不細談。
- 電腦標示的「16 GB」記憶體是 16 × 1024³ 位元組，剛好裝得下 30 個量子位元；實際上作業系統和程式也要用記憶體，所以通常再少一顆。
- 「超過最大超級電腦的記憶體」依學程簡報第 43 頁的說法（頂級超級電腦總記憶體約 10 PB 等級）。
''',

'01_活動步驟.md': '''# 活動步驟

## 活動一：米粒和杯子（約 15 分鐘）

1. 一個杯子代表一種組合（例如「零一」），在杯子前放一張小紙條寫上組合。
2. 每個杯子放一粒米，代表「這個組合要記一個振幅」。
3. 一顆量子位元：兩個杯子（零、一）。兩顆：四個（零零、零一、一零、一一）。三顆：八個。
4. 四顆、五顆的杯子不夠，就在列印包第 1 頁畫格子代替。
5. 填好「顆數 → 杯子數」，再猜猜五十顆要幾個杯子。

## 活動二：記憶體競速（約 25 分鐘）

1. 你和爸爸各拿一台計算機和列印包第 2 頁。
2. 從一顆開始：振幅數 = 上一列 × 2；記憶體 = 振幅數 × 16 位元組。
3. 一人當計算手、一人當裁判，算到 10 顆換手。裁判用「每多 10 顆大約多三個零」檢查。
4. 算錯了就從上一列重算，誰先正確填完 50 顆誰贏。
5. 換算單位：1024 位元組 = 1 KB，1024 KB = 1 MB，再往上是 GB、TB、PB。

## 下半場：查自家電腦（約 30 分鐘）

1. 在電腦的「設定 → 系統 → 關於」（Windows）或「關於這台 Mac」找到記憶體（RAM）大小。
2. 把 GB 換成位元組（× 1024 × 1024 × 1024），先除以 16，再一直除以 2，數除了幾次。
3. 次數就是最多能精確模擬的量子位元數；再減一顆，留給作業系統。
''',

'04_解答與對照表.md': '# 解答與對照表（爸爸用）\n\n## 2ⁿ 記憶體對照表（每個振幅 16 位元組，1024 進位）\n\n'
  + '| 量子位元數 | 振幅數 2ⁿ | 記憶體 | 大約幾台 16 GB 筆電 |\n|---|---|---|---|\n'
  + ''.join(f'| {n} | {amps(n):,} | {human(mem(n))} | {laptops(n)} |\n' for n in TABLE_N)
  + '\n五十顆：約 1126 兆個振幅，16 PB（十進位約 18 PB），約一百萬台 16 GB 筆電。\n\n'
  '## 自家電腦最多能精確模擬幾顆\n\n| 記憶體 | 理論上最多 | 留給作業系統後 |\n|---|---|---|\n'
  + ''.join(f'| {r} GB | {max_qubits(r)} 顆 | {max_qubits(r) - 1} 顆 |\n' for r in RAMS)
  + '\n記憶體每多一倍，只多一顆量子位元。\n\n'
  '## 常見問題\n\n'
  '- 「五十顆可以讀出一千兆個答案？」不行：測量一次只得到五十個零或一（課綱常見誤解）。\n'
  '- 「用單精度存可以多一顆嗎？」可以：每個振幅 8 位元組，同樣記憶體多一顆，但精度變差。\n'
  '- 計算機出現「1.1259e15」：就是 1.1259 × 10¹⁵，約一千一百兆。\n',

'05_三維動畫導覽.md': '''# 三維動畫導覽

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## 今天要看的場景：`animations/operation.html#register`（場景 4：多位元與糾纏）

- 「量子位元數 n」滑桿：1 到 4 顆，下方柱子從 2 根變成 16 根，每根是一種組合的振幅。
- 「均勻疊加 H⊗ⁿ」：所有柱子一樣高，每種組合的機率相同。
- 「測量全部」：只剩一根柱子，只讀到 n 個零或一。
- 右下小圖：精確模擬所需記憶體（2ⁿ × 16 位元組），30、40、50 顆各有一個點。

## 操作

滑鼠拖曳旋轉、滾輪縮放；`H` 隱藏面板；`R` 重設視角。
''',
}

SHEET_HEADER = ['量子位元數', '我算的振幅數', '我算的記憶體', '裁判檢查', '正確振幅數', '正確記憶體']
SHEET_ROWS = [[str(n), '', '', '', str(amps(n)), human(mem(n))] for n in TABLE_N] + [['我家電腦：＿＿GB', '', '', '', '', '']]

EXTRA_CSS = '''table.cups td{height:12mm}table.race td{height:10.5mm}table.race td:first-child{text-align:center;font-weight:700}
.grid32{display:grid;grid-template-columns:repeat(8,1fr);gap:2mm;margin-top:3mm}.grid32 div{border:1pt solid #7f9bb3;height:12mm;border-radius:1.5mm;font-size:8pt;color:#9ab;padding:.5mm 1mm}
.chk li{margin:3mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.big{font-size:15pt;line-height:2.1}'''

RACE_N = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50]


def html():
    pages = [
        '<h2>活動一：米粒和杯子</h2><p class="lead">一個杯子＝一種組合，一粒米＝要記的一個振幅。</p>'
        '<table class="cups"><tr><th>量子位元數</th><th>寫出所有組合</th><th>杯子數</th></tr>'
        '<tr><td>1 顆</td><td>零、一</td><td></td></tr><tr><td>2 顆</td><td></td><td></td></tr>'
        '<tr><td>3 顆</td><td></td><td></td></tr><tr><td>4 顆</td><td>（太多了？用下面的格子）</td><td></td></tr>'
        '<tr><td>5 顆</td><td>（用下面的格子）</td><td></td></tr></table>'
        '<h3 style="margin-top:5mm">杯子不夠？在格子裡畫米粒（5 顆量子位元）</h3><div class="grid32">'
        + ''.join(f'<div>{i:05b}</div>' for i in range(32)) + '</div>'
        '<p class="big">每多一顆，杯子變成＿＿倍。猜猜五十顆要幾個杯子：＿＿＿＿＿＿＿＿</p>',
        '<h2>活動二：2ⁿ 記憶體競速對照表</h2><p class="lead">振幅數＝上一列 × 2；記憶體＝振幅數 × 16 位元組。裁判檢查：每多 10 顆，大約多三個零。</p>'
        '<table class="race"><tr><th>量子位元數</th><th>振幅數</th><th>記憶體（位元組）</th><th>換成 KB／MB／GB…</th><th>裁判 ✓</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td>{"2" if n == 1 else ""}</td><td>{"32" if n == 1 else ""}</td><td></td><td></td></tr>' for n in RACE_N)
        + '</table><p class="note">1024 位元組＝1 KB；1024 KB＝1 MB；1024 MB＝1 GB；再往上是 TB、PB。</p>',
        '<h2>下半場：我家電腦能模擬幾顆？</h2><p class="lead">在電腦的設定裡找到記憶體（RAM）大小。</p>'
        '<div class="box big">我家電腦的記憶體：＿＿＿＿ GB<br>'
        '換成位元組：＿＿＿＿ × 1024 × 1024 × 1024<br>＝ ＿＿＿＿＿＿＿＿＿＿＿＿＿＿ 位元組<br>'
        '先除以 16：＿＿＿＿＿＿＿＿＿＿＿＿<br>再一直除以 2，除了＿＿＿＿次<br>'
        '最多能精確模擬：＿＿＿＿顆量子位元（留給作業系統：再減一顆）</div>'
        '<div class="box" style="margin-top:6mm"><h3>估算挑戰</h3>'
        '<p>如果記憶體多一倍，可以多模擬幾顆？＿＿＿＿</p>'
        '<p>要模擬五十顆，大約要幾台 16 GB 的電腦？＿＿＿＿＿＿＿＿</p>'
        '<p>這件事做得到嗎？為什麼？</p><div class="line"></div><div class="line"></div></div>',
        '<h2>最後一關：教爸爸翻倍的威力</h2><div class="box"><ul class="chk">'
        '<li>說出每多一顆量子位元，振幅的數量會怎樣</li><li>說出每個振幅要幾個位元組</li>'
        '<li>說出三十、四十、五十顆大約要多少記憶體</li><li>說出我家電腦最多能精確模擬幾顆</li>'
        '<li>指出一個限制：振幅很多，測量一次只讀到 n 個零或一</li><li>替 2ⁿ 記憶體對照表取名字、存檔</li></ul></div>'
        '<div class="box" style="margin-top:6mm"><h3>記憶體爆炸（每個振幅 16 位元組）</h3>'
        '<table><tr><th>量子位元數</th><th>記憶體</th><th>大約等於</th></tr>'
        f'<tr><td>30</td><td>{human(mem(30))}</td><td>一台筆電</td></tr>'
        f'<tr><td>40</td><td>{human(mem(40))}</td><td>約一千台筆電</td></tr>'
        f'<tr><td>50</td><td>{human(mem(50))}（約 18 PB）</td><td>約一百萬台筆電</td></tr>'
        '</table><p class="note">每多十顆，大約一千倍。</p></div>',
    ]
    return printpack.document('Q007 兩顆三顆五十顆 列印包', '父子科技學院 量子電腦學程 Q007｜兩顆、三顆、五十顆', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q007-two-to-the-n', folder='Q007_兩顆三顆五十顆', files=FILES,
        sheet=('03_記憶體對照表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_兩顆三顆五十顆.pdf', pack_pages=4,
        pack_needles=('米粒和杯子', '記憶體競速對照表', '我家電腦能模擬幾顆', '最後一關'),
        authoring_dir=XINEW / 'authoring/q007', episode_dir='specials/q007-two-to-the-n',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'bytesPerAmplitude': BYTES, 'memoryTable': {n: mem(n) for n in TABLE_N},
               'maxQubitsByRamGB': {r: max_qubits(r) for r in RAMS}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q007/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

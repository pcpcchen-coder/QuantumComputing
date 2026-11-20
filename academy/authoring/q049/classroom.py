"""Q049 課堂教材：時間預算表、時間機器換算尺與滑桿實驗表、瓶頸改造卡、說明卡與最後一關、可執行的 time_budget.py、解答。

不需要帳號、不需要安裝套件（time_budget.py 只用 Python 標準函式庫；也可以只用計算機）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q049/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 典型值：animations/js/operation/12_workflow.js times()（第 79 行）與插圖文字；slides/QC_Operation_Talk.pptx p13、p15、p30
RESET_PASSIVE_US, RESET_ACTIVE_US, GATE_LAYER_US, MEAS_US = 250.0, 2.0, 0.1, 1.0
DEPTH, SHOTS, SLOW = 20, 1000, 1_000_000
SHOT_US = RESET_PASSIVE_US + DEPTH * GATE_LAYER_US + MEAS_US
assert SHOT_US == 253.0
JOB_S = SHOT_US * SHOTS / 1e6
assert abs(JOB_S - 0.253) < 1e-12

STATIONS = [  # (站, 做什麼, 在哪裡, 典型耗時)
    ('① 寫程式、送出', '寫線路、指定 shots，送進雲端', '你的電腦 → 雲端 API', '送出：網路往返（秒）'),
    ('　排隊（佇列）', '等前面的工作跑完', '雲端排程器', '秒～分鐘（看當天多忙）'),
    ('② 轉譯', '換原生閘、挑實體量子位元、插 SWAP、最佳化', '古典電腦', '秒級（最佳化越多越久）'),
    ('③ 脈衝排程', '每個閘查校準資料庫，排上奈秒時間軸', '古典電腦', '和轉譯合計：秒級'),
    ('④ 控制電子', '波形載入 AWG／FPGA，鎖 10 MHz 時脈、觸發', '控制電子機櫃', '載入：秒級'),
    ('⑤ 晶片執行', '每個 shot：重置 → 閘 → 讀取，重複 1000 次', '冷凍機裡的晶片', '253 μs × 1000 ≈ 0.25 秒'),
    ('⑥ 判別與結果', '判成 0／1、累積計數、回傳', 'FPGA → 網路 → 你的電腦', '判別即時；回傳：秒'),
]

PROGRAM = '''"""父子科技學院 量子電腦學程 Q049：一次量子計算的生命週期——時間預算與時間機器（只用 Python 標準函式庫）

執行：python time_budget.py
數字是學程動畫 operation.html#workflow 與簡報整理的典型量級（依機型、後端與當天負載而異）。
"""
SLOW = 1_000_000                      # 時間機器：放慢一百萬倍（1 微秒 → 1 秒）


def shot_us(depth=20, active_reset=False):
    reset = 2.0 if active_reset else 250.0   # 主動重置約 2 μs；被動等待約 250 μs
    gates = depth * 0.1                      # 每一層閘約 0.1 μs
    meas = 1.0                               # 讀取約 1 μs
    return reset, gates, meas, reset + gates + meas


def pretty(sec):
    for unit, s in (('年', 365.25 * 86400), ('天', 86400), ('小時', 3600), ('分鐘', 60), ('秒', 1),
                    ('毫秒', 1e-3), ('微秒', 1e-6), ('奈秒', 1e-9)):
        if sec >= s:
            return f'{sec / s:.3g} {unit}'
    return f'{sec:.3g} 秒'


for label, depth, active, shots in [('預設（被動重置）', 20, False, 1000),
                                    ('shots 改成十萬', 20, False, 100_000),
                                    ('主動重置＋十萬 shots', 20, True, 100_000),
                                    ('主動重置＋十萬 shots＋深度 1000 層', 1000, True, 100_000)]:
    r, g, m, s = shot_us(depth, active)
    job = s * shots / 1e6
    print(f'{label}：每 shot {s:.1f} μs（重置 {r / s:.1%}、閘 {g / s:.1%}、讀取 {m / s:.1%}）× {shots:,} = {pretty(job)}；'
          f'放慢後 {pretty(job * SLOW)}')

# 改造區：量子線路以外的等待（自己填，單位：秒）
waits = {'排隊': 60, '轉譯與脈衝排程': 5, '載入波形': 2, '網路往返': 1}
quantum = shot_us()[3] * 1000 / 1e6
total = sum(waits.values()) + quantum
print(f'\\n全部合計 {pretty(total)}，晶片上只佔 {quantum / total:.2%}')
for k, v in waits.items():
    print(f'  {k}：{pretty(v)}，放慢一百萬倍後 {pretty(v * SLOW)}')
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q049：一次量子計算的生命週期（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶孩子從「按下送出」開始，跟著一個量子工作走過六站：寫程式、轉譯、脈衝排程、控制電子、晶片重複執行（shots）、判別與結果；再用「時間機器」（放慢一百萬倍，1 μs → 1 秒）看清楚每一站花多少時間。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開完整流程場景，認識六站與右下角的時間插圖 | `animations/operation.html#workflow` |
| 25–65 | 孩子當駕駛員按「下一站 ▶」，爸爸當計時員填時間預算表、換算放慢後的時間 | 列印包第 1、2 頁、`time_budget.py` |
| 65–75 | 休息 | |
| 75–105 | 圈出最慢的一站，提出縮短方法，在場景用滑桿驗證，算省下多少 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：六站順序、哪一站最久、常見誤解 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#workflow` 和 `#pulse`（不需要網路、伺服器或帳號）。
- 列印 `02_列印包_一次量子計算的生命週期.pdf`（A4，共 4 頁），準備計算機或執行 `python time_budget.py`。
- 讀一遍 `04_解答.md`。

## 計時員的原則

- 每一站都要寫單位：奈秒（ns）、微秒（μs）、毫秒（ms）、秒，每一級差一千倍。
- 「典型耗時」是量級，不是精確值；真實後端依機型與當天負載而異，排隊時間尤其不固定。
- 驗收時問：「晶片上的時間大多花在哪裡？」「從送出到拿回結果，最久的通常是哪一段？」

## 誠實說明

- 各站耗時取自學程動畫插圖與簡報的典型量級（被動重置 250 μs、主動重置約 2 μs、每層閘 0.1 μs、讀取 1 μs；佇列、轉譯、波形載入、網路傳輸「秒～分鐘」）。
- 時間機器是教學比喻；換算見 `04_解答.md`。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：跟著工作走、填預算表（約 40 分鐘）

1. 打開 `animations/operation.html#workflow`（場景 12：完整流程）。先關掉「自動播放」，改按「下一站 ▶」。
2. 每到一站，讀左邊面板最下面的說明，在列印包第 1 頁的時間預算表寫下：做什麼、在哪裡、典型耗時。
   - ① 寫程式：螢幕上是貝爾態程式（`qc.h(0)`、`qc.cx(0, 1)`、`measure_all()`），最後一行指定 shots。
   - ② 轉譯：標籤 `q0→Q3`、`q1→Q1`：邏輯量子位元被放到哪一顆實體量子位元。
   - ③ 脈衝排程：時間軸上的方塊一個接一個亮起（D＝驅動、Z＝磁通、M＝讀取）。
   - ④ 控制電子：機櫃上的綠燈閃爍。
   - ⑤ 晶片執行：上方計數跳到 1,000；⑥ 判別與結果：直方圖 00、11 最高，01、10 只有一點點（雜訊造成的錯誤）。
3. 看右下角插圖：一個 shot 的時間組成與總執行時間；把數字抄進預算表「⑤ 晶片執行」那一列。
4. 用列印包第 2 頁的時間機器換算尺，把每一站換算成「放慢一百萬倍後」的時間（或執行 `python time_budget.py`）。
5. 打開 `operation.html#pulse`（場景 3：微波脈衝）：預設 40 ns 就是一個翻轉閘；按「虛擬 Z（90°）」看看不送脈衝也能轉相位（零時間）。

## 下半場：找瓶頸、提方法（約 30 分鐘）

1. 在預算表上圈出最慢的一站（分「晶片上」和「從送出到拿回結果」兩種看法）。
2. 回到 `#workflow`，照列印包第 2 頁的滑桿實驗表操作：「shots N」拉到 100,000、按「主動重置」、把「線路深度」拉到 1000 層，記下插圖的數字。
3. 在列印包第 3 頁的瓶頸改造卡寫下你的方法、改前／改後時間、代價（例如 shots 變少，統計誤差變大）。
4. 用 `time_budget.py` 的改造區填入你假設的排隊、轉譯時間，看看晶片上的時間只佔多少。
''',

'time_budget.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 時間預算表（典型量級）\n\n| 站 | 做什麼 | 在哪裡 | 典型耗時 |\n|---|---|---|---|\n'
  + ''.join(f'| {a.strip()} | {b} | {c} | {d} |\n' for a, b, c, d in STATIONS)
  + '\n## 一個 shot（動畫預設：深度 20 層、被動重置）\n\n'
  '- 重置 250 μs（98.8%）＋閘 2.0 μs（0.8%）＋讀取 1.0 μs（0.4%）＝ 253 μs；× 1,000 shots ＝ 0.253 秒。\n'
  '- shots 十萬：25.3 秒。主動重置：每 shot 5 μs（重置 40%），十萬 shots ＝ 0.5 秒。主動重置＋深度 1000 層：每 shot 103 μs（閘 97.1%），十萬 shots ＝ 10.3 秒。\n\n'
  '## 時間機器（放慢一百萬倍）\n\n'
  '| 真實 | 放慢後 |\n|---|---|\n'
  '| 40 ns（一個翻轉閘） | 0.04 秒 |\n| 1 μs（一次讀取） | 1 秒 |\n| 253 μs（一個 shot） | 253 秒 ≈ 4.2 分鐘 |\n'
  '| 0.253 秒（一千個 shot） | 253,000 秒 ≈ 70 小時 ≈ 2.9 天 |\n| 5 ms（主動重置一千個 shot） | 5,000 秒 ≈ 1.4 小時 |\n'
  '| 1 分鐘（假設排隊） | 6,000 萬秒 ≈ 694 天 ≈ 1.9 年 |\n\n'
  '## 瓶頸與縮短方法\n\n'
  '- 晶片上：瓶頸是被動重置 → 改主動重置（量測＋條件翻轉，約 1–5 μs，簡報第 13 頁）。線路很深時瓶頸換成閘。\n'
  '- 從送出到拿回結果：通常是排隊、轉譯、載入與傳輸 → 把很多條線路打包成一個工作、只排一次隊；挑不忙的時段或後端；最佳化等級不要開過頭。\n'
  '- 減少 shots 會變快，但統計誤差約與 1/√N 成正比：1,000 shots 約 ±1.6%，100 shots 約 ±5%（簡報第 32 頁）。\n\n'
  '## 常見誤解\n\n'
  '- 「量子電腦一按就算完」：排隊與編譯常比量子線路本身花更多時間。\n'
  '- 「晶片上的時間都在計算」：預設情況下 98.8% 在等重置。\n'
  '- 「虛擬 Z 也要送脈衝」：虛擬 Z 只改之後脈衝的相位，零時間。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#workflow`（場景 12：一次量子計算的完整流程）

- 六個彩色平台：① 寫程式（綠）、② 轉譯（青）、③ 脈衝排程（紫）、④ 控制電子（橘）、⑤ 晶片執行 shots（藍）、⑥ 判別與結果（紅）。
- 控制項：「自動播放」「下一站 ▶」「shots N」（100–100,000）、「線路深度（層）」（1–1000）、「主動重置（量測 + 條件 π 脈衝）」。
- 右下角插圖：一個 shot 的時間組成（紫＝重置、金＝閘、紅＝讀取）與總執行時間；下方灰字「另加：佇列、轉譯、波形載入、網路傳輸（秒～分鐘）」。

## `animations/operation.html#pulse`（場景 3：微波脈衝）

- 「閘長度（ns）」預設 40 ns、「脈衝面積 → 旋轉角」180° 就是翻轉閘；面板讀數「峰值 Rabi 頻率」。
- 「虛擬 Z（90°）」：不送脈衝，只改之後脈衝的相位——零時間。

## 也可以看

- `peripherals.html#software`（周邊場景 7：軟體堆疊）：同一個程式在各層的樣子、校準資料庫。
- `operation.html#readout`（場景 7：讀取與統計）：「積分時間 τ」滑桿，讀取要花多少微秒。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換場景。
''',
}

SHEET_HEADER = ['站', '做什麼', '在哪裡', '典型耗時', '放慢一百萬倍後', '我猜的排名', '備註']
SHEET_ROWS = [[a.strip(), b, c, '', '', '', ''] for a, b, c, _ in STATIONS]

EXTRA_CSS = '''table.bt td{font-size:10.5pt;padding:1.6mm 2mm;height:12mm}table.bt th{font-size:10.5pt}
table.lad td{font-size:11pt;padding:1.4mm 2mm;text-align:center}table.lad th{font-size:10.5pt}
table.ex td{font-size:10.5pt;height:9mm}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    bt = ''.join(f'<tr><td>{a}</td><td style="font-size:9.5pt">{b}</td><td></td><td></td><td></td></tr>' for a, b, *_ in STATIONS)
    ladder = [('奈秒 ns', '10⁻⁹ 秒', '一個閘：數十 ns'), ('微秒 μs', '10⁻⁶ 秒', '一個 shot：約 253 μs'),
              ('毫秒 ms', '10⁻³ 秒', '一千個 shot：約 253 ms'), ('秒 s', '1 秒', '送出、轉譯、載入'),
              ('分鐘', '60 秒', '排隊（看當天多忙）')]
    lad = ''.join(f'<tr><td>{u}</td><td>{v}</td><td>{e}</td><td></td></tr>' for u, v, e in ladder)
    exps = [('預設', '1,000', '20', '關'), ('實驗一', '100,000', '20', '關'), ('實驗二', '100,000', '20', '開'), ('實驗三', '100,000', '1000', '開')]
    ex = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td></td><td></td><td></td></tr>' for a, b, c, d in exps)
    pages = [
        '<h2>時間預算表</h2><p class="lead">跟著工作一站一站走。每一站寫下在哪裡、典型耗時，再用時間機器換算（放慢一百萬倍：1 μs → 1 秒）。</p>'
        '<p>我猜最花時間的一站是：＿＿＿＿＿＿＿＿＿＿　（走完再對答案）</p>'
        '<table class="bt"><tr><th style="width:30mm">站</th><th>做什麼</th><th style="width:30mm">在哪裡</th><th style="width:28mm">典型耗時</th><th style="width:30mm">放慢一百萬倍後</th></tr>'
        + bt + '</table>'
        '<div class="box" style="margin-top:4mm"><p>⑤ 拆開看：一個 shot ＝ 重置＿＿＿ μs ＋ 閘＿＿＿ μs ＋ 讀取＿＿＿ μs ＝＿＿＿ μs；× 1,000 ＝＿＿＿ 秒</p>'
        '<p class="note">駕駛員：＿＿＿＿＿　計時員：＿＿＿＿＿　作品名稱：＿＿＿＿＿＿＿＿</p></div>',
        '<h2>時間機器換算尺</h2><p class="lead">每往上一級差一千倍。放慢一百萬倍＝把「微秒」念成「秒」。</p>'
        '<table class="lad"><tr><th>單位</th><th>等於</th><th>例子</th><th>放慢一百萬倍後</th></tr>' + lad + '</table>'
        '<div class="box" style="margin-top:4mm"><p>練習：40 ns 的翻轉閘 →＿＿＿秒；一千個 shot（0.253 秒）→＿＿＿天；排隊 1 分鐘 →＿＿＿年</p></div>'
        '<h3 style="margin-top:5mm">滑桿實驗表（operation.html#workflow 右下角插圖）</h3>'
        '<table class="ex"><tr><th>實驗</th><th>shots N</th><th>深度（層）</th><th>主動重置</th><th>每 shot（μs）</th><th>最大的是？佔幾 %</th><th>總時間</th></tr>'
        + ex + '</table><p class="note">每改一次滑桿，就把插圖下方黃字抄下來。瓶頸換人了嗎？</p>',
        '<h2>瓶頸改造卡</h2><div class="box"><p>1. 晶片上最慢的是：＿＿＿＿＿＿＿　佔一個 shot 的＿＿＿ %</p>'
        '<p>2. 從送出到拿回結果，最慢的是：＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>3. 我的縮短方法（例如主動重置、打包工作、少一點 shots、挑不忙的時段）：</p><div class="line"></div><div class="line"></div>'
        '<p>4. 改前＿＿＿＿＿＿　→　改後＿＿＿＿＿＿　省下＿＿＿＿＿＿</p>'
        '<p>5. 代價是什麼？（例如 shots 變少，統計誤差變大：1,000 次約 ±1.6%，100 次約 ±5%）</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>生活技能：找出流程瓶頸</h3>'
        '<p>整條流程的速度卡在最慢的那一步。想一個生活裡的例子（排隊買早餐、全家出門……），它的瓶頸在哪裡？</p><div class="line"></div></div>',
        '<h2>說明卡：一次量子計算的生命週期</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 六站的順序：</p><div class="line"></div><p>2. 一個 shot 裡發生哪三件事？哪一件最久？</p><div class="line"></div>'
        '<p>3. 為什麼每個 shot 都要重來？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出六站：程式、轉譯、脈衝、控制電子、shots、結果</li><li>讀出時間預算表：哪一站最花時間</li>'
        '<li>說出一個縮短方法和它的代價</li><li>指出常見誤解：排隊與編譯常比量子線路本身花更多時間</li>'
        '<li>替時間預算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q049 一次量子計算的生命週期 列印包', '父子科技學院 量子電腦學程 Q049｜一次量子計算的生命週期', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q049-job-lifecycle', folder='Q049_一次量子計算的生命週期', files=FILES,
        sheet=('03_時間預算表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_一次量子計算的生命週期.pdf', pack_pages=4,
        pack_needles=('時間預算表', '時間機器換算尺', '滑桿實驗表', '瓶頸改造卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q049', episode_dir='specials/q049-job-lifecycle',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'time_budget.py', 'shotMicroseconds': SHOT_US, 'jobSeconds1000Shots': JOB_S,
               'timeMachineFactor': SLOW, 'stationsFrom': 'slides/QC_Operation_Talk.pptx p3; animations/js/operation/12_workflow.js',
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q049/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

"""Q046 課堂教材：控制鏈角色卡、拍手排練紀錄表、控制鏈流程圖底稿、相位計算卡、可執行的 phase_drift.py、說明卡與解答。

不需要帳號、不需要安裝套件（phase_drift.py 只用 Python 標準函式庫；也可以只用計算機）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q046/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent


def phase_deg(f_hz, dt_s):
    """時間差 dt 造成的相位差（度），頻率 f。"""
    return 360.0 * f_hz * dt_s


F = 5e9   # 5 GHz（場景與簡報：驅動在 4–8 GHz；operation.html#pulse 的 f01 約 5 GHz）
REF = 10e6  # 10 MHz 參考時脈
# 與影片、fact-check.md 一致
assert abs(1 / F - 0.2e-9) < 1e-18                      # 5 GHz 一圈 0.2 ns
assert round(phase_deg(F, 0.1e-9), 6) == 180.0          # 晚 0.1 ns → 180°
assert round(phase_deg(F, 10e-12), 6) == 18.0           # 晚 10 ps → 18°
assert round(phase_deg(F, 1e-12), 6) == 1.8             # 晚 1 ps → 1.8°
assert round(1 / REF * 1e9) == 100 and REF == 1e7       # 10 MHz：每秒一千萬拍、一拍 100 ns
assert round(F / REF) == 500                            # 5 GHz 是 10 MHz 的 500 倍
assert round(phase_deg(1.0, 1.0)) == 360                # 頻率差 1 Hz，一秒累積一整圈
# 拍手版：兩個節拍器 60 與 63 拍／分，頻率差 0.05 Hz，10 秒差半拍、20 秒差一拍
assert abs((63 - 60) / 60 * 10 - 0.5) < 1e-12 and abs((63 - 60) / 60 * 20 - 1.0) < 1e-12

DELAYS = [(1e-12, '1 ps'), (10e-12, '10 ps'), (50e-12, '50 ps'), (0.1e-9, '0.1 ns'), (0.2e-9, '0.2 ns'), (1e-9, '1 ns')]

PROGRAM = '''"""父子科技學院 量子電腦學程 Q046：時間差 → 相位差 計算器

執行：python phase_drift.py          （不需要安裝任何套件）
改造：改下面的 FREQ（例如 4e9、8e9），或改 DF 看兩台沒鎖在一起的儀器怎麼慢慢飄走
"""

FREQ = 5e9          # 驅動微波的頻率（赫），5 GHz
REF = 10e6          # 參考時脈 10 MHz
DF = 1.0            # 兩台儀器各自走時，頻率差多少（赫）

print(f'參考時脈 {REF / 1e6:.0f} MHz：每秒 {REF:,.0f} 拍，一拍 {1 / REF * 1e9:.0f} ns')
print(f'{FREQ / 1e9:g} GHz 是參考時脈的 {FREQ / REF:,.0f} 倍；轉一圈要 {1 / FREQ * 1e9:.3f} ns')

print('\\n一、時間差 → 相位差（相位差 = 360° × 頻率 × 時間差）')
for dt, name in [(1e-12, '1 ps'), (10e-12, '10 ps'), (50e-12, '50 ps'), (0.1e-9, '0.1 ns'), (0.2e-9, '0.2 ns'), (1e-9, '1 ns')]:
    deg = 360 * FREQ * dt
    print(f'  晚 {name:>6}：{deg:8.1f}°   （除掉整圈後 {deg % 360:5.1f}°）')

print(f'\\n二、兩台儀器沒鎖在一起，頻率差 {DF} Hz：相位一秒一秒累積')
for t in [0.1, 0.25, 0.5, 1.0, 2.0]:
    deg = 360 * DF * t
    print(f'  {t:4} 秒後：差 {deg:6.1f}°（{deg / 360:.2f} 圈）')

print('\\n三、拍手版：兩個節拍器各打各的（60 與 63 拍／分）')
for t in [5, 10, 20, 40]:
    beats = (63 - 60) / 60 * t
    print(f'  {t:2} 秒後：差 {beats:.2f} 拍')
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q046：控制電子與時脈（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：量子晶片在冷凍機最底層，指揮它的是室溫那一整櫃控制儀器；一次測量要依序經過「上傳 → 觸發 → 驅動 → 讀取 → 判別 → 回饋」六個站，而且所有儀器都鎖在同一個 10 MHz 參考時脈上。今天全家扮演這條控制鏈，用拍手當時脈。

## 需要什麼

- 一台電腦和瀏覽器：打開學程 `animations/peripherals.html#electronics`（周邊系統 3D 場景 6「控制電子學」），想多看可以再開 `animations/operation.html#pulse`（微波脈衝）。不需要帳號。
- 一枚硬幣（當量子位元：正面＝0、反面＝1）、六張便條紙（寫上六個站名）、一張白紙（記結果）。
- 手機節拍器 App 或計時器（沒有也行，由一個人拍手）。
- 列印 `02_列印包_控制電子與時脈.pdf`（A4，共 4 頁）；計算機，或用 Python 執行 `phase_drift.py`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 看控制電子場景；認識六個站、10 MHz 參考時脈 | 影片第 4–7 段、列印包第 1 頁 |
| 25–65 | 人肉控制鏈：分配角色、拍手排練，傳遞一次測量 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 故意讓一站慢半拍；兩個節拍器各打各的；算相位差 | 列印包第 2–3 頁、`phase_drift.py` |
| 105–115 | 孩子教爸爸：六個站、為什麼要同一個時脈、常見誤解 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、流程圖命名、存檔 | |

## 角色扮演的規則

- 「時脈」只有一個人（或一個節拍器）：每拍一下，就是一個時鐘週期。其他人只能在「輪到自己的那一拍」動作。
- 人不夠就一人兼兩、三站，但每站還是只能在自己那一拍動作。
- 先照規則跑三次「正常版」，結果都對了，再開始搗蛋。

## 誠實說明

- 拍手、硬幣是比喻：真實的一拍（10 MHz）只有 100 奈秒，回饋在幾百奈秒內完成；家裡的一拍約一秒。
- 回饋延遲（約 350 ns、跨機櫃 < 550 ns）、取樣率等數字取自學程簡報整理的廠商公開資料，僅供比較。
- 「時間差→相位差」的換算是單一頻率的理想情形，用來感受量級；真實系統會在軟體裡校正固定延遲，難處理的是沒校正到的漂移與抖動。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：人肉控制鏈（約 40 分鐘）

1. 打開 `animations/peripherals.html#electronics`，跟著發光的小球看一次循環；上方大字依序是 ① 上傳 → ② 觸發、驅動 → ③ 讀取、判別 → ④ 回饋 → ⑤ 回傳。
2. 把六張便條紙寫上：上傳（控制電腦）、觸發（同步器）、驅動（波形產生器）、讀取（讀取模組）、判別（可程式邏輯晶片）、回饋。分配角色；另外指定一個人當「時脈」（銣原子鐘）。
3. 硬幣正面朝上放在桌子中間，它是量子位元，一開始是 0。
4. 「時脈」穩定地拍手，一秒一下。依序：
   - 第 1 拍：上傳站把寫著「翻一次」的紙條交給觸發站。
   - 第 2 拍：觸發站喊「開始！」，指向驅動站和讀取站。
   - 第 3 拍：驅動站照紙條把硬幣翻面（現在是 1）。
   - 第 4 拍：讀取站看硬幣，把看到的面告訴判別站。
   - 第 5 拍：判別站在白紙寫下 0 或 1。
   - 第 6 拍：回饋站：如果寫的是 1，就把硬幣翻回 0（主動重置），再把結果交回上傳站。
5. 跑三次，都要得到「判別＝1、最後硬幣＝0」。把每次結果填進列印包第 2 頁。
6. 一起畫控制鏈流程圖（列印包第 3 頁）：六個方塊、箭頭，再畫一條從「時脈」連到每一站的線。

## 下半場：一站慢半拍（約 30 分鐘）

1. 讓「驅動站」在兩拍中間才翻硬幣（慢半拍）。讀取站還是在第 4 拍看：看到的是什麼？判別對嗎？
2. 改讓「讀取站」慢半拍、其他人照常：判別站第 5 拍要寫字時，拿到答案了嗎？
3. 讓「回饋站」慢兩拍：下一輪的上傳站要等多久才能開始？
4. 兩個節拍器（或兩個人）各打各的：一個每分鐘 60 下、一個 63 下，驅動站跟第一個、讀取站跟第二個。數一數：幾秒後兩邊差半拍？
5. 執行 `python phase_drift.py`，或用計算機：相位差 = 360° × 頻率 × 時間差。5 GHz 時，晚 1 ps、10 ps、0.1 ns 各差幾度？
6. 把觀察寫在列印包第 2、3 頁。
''',

'phase_drift.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 正常版\n\n'
  '- 第 3 拍硬幣翻成 1，第 4 拍讀到 1，第 5 拍判別寫 1，第 6 拍回饋把硬幣翻回 0：判別＝1、最後硬幣＝0。\n\n'
  '## 一站慢半拍\n\n'
  '- 驅動站慢半拍：第 4 拍時硬幣可能還沒翻（或剛好在翻），讀取站讀到 0 → 判別寫 0，錯了；而且回饋站以為是 0 沒有重置，硬幣最後變成 1。真實系統：脈衝和讀取窗口對不齊，雙量子位元閘需要兩個通道奈秒等級對齊。\n'
  '- 讀取站慢半拍：判別站第 5 拍拿不到答案，只好猜，或整條鏈卡住。\n'
  '- 回饋站慢兩拍：下一輪要多等兩拍；真實儀器把回饋壓在幾百奈秒（單機約 350 ns、跨機櫃 < 550 ns）。\n'
  '- 兩個節拍器 60 與 63 拍／分：頻率差 3 拍／分 = 0.05 拍／秒，10 秒差半拍、20 秒差一整拍，而且越差越多。這就是「沒有鎖在同一個參考時脈，相位會飄」。\n\n'
  '## 相位計算（5 GHz，相位差 = 360° × 頻率 × 時間差）\n\n'
  '| 時間差 | 相位差 |\n|---|---|\n'
  + ''.join(f'| {name} | {phase_deg(F, dt):g}° |\n' for dt, name in DELAYS) +
  '\n- 5 GHz 轉一圈 0.2 ns，所以晚 0.2 ns 剛好一整圈（360°），晚 1 ns 是五整圈（1800°）。\n'
  '- 10 MHz：每秒 10,000,000 拍，一拍 100 ns；5 GHz ÷ 10 MHz = 500 倍。\n'
  '- 兩台 5 GHz 儀器差 1 Hz：0.25 秒差 90°、0.5 秒差 180°、1 秒差 360°。\n\n'
  '## 常見問題\n\n'
  '- 每台儀器的時鐘都很準，為什麼還要接在一起？兩個各自走的時鐘頻率總有一點差，相位會一直累積；所有 LO、DAC、ADC 都從同一個 10 MHz 參考倍頻出來，相位才會彼此鎖定。\n'
  '- 時脈和觸發有什麼不同？10 MHz 參考讓大家的「頻率和相位」一致；觸發／同步匯流排讓大家在「同一個時鐘週期開始播放」。兩個都要。\n'
  '- 為什麼回饋要這麼快？主動重置、中途量測與量子糾錯都要在量子位元還沒失去資訊前做完；糾錯解碼要在約微秒內完成。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要伺服器或帳號。

## `animations/peripherals.html#electronics`（周邊系統 3D 場景 6：控制電子學）

- 中間的機櫃由上往下：銣原子鐘／10 MHz 分配、同步器／觸發分配、AWG／DAC（XY 驅動）、LO 合成器、IQ 混頻器、讀取模組、FPGA 即時處理／回饋、DC 電流源、HEMT 偏壓與 TWPA 泵浦源。左邊是控制電腦，右邊是冷凍機頂板。
- 發光的小球依序走一次「量測—回饋」循環，上方大字寫出目前步驟。
- 面板按鈕「外差 IQ 混頻架構」「直接射頻合成（RFSoC 等）」：切換兩種產生微波的方法；滑桿「播放速度」0.3–2 倍。
- 右下插圖：XY 驅動波形（約 40 ns；I 是高斯包絡、Q 是 DRAG 修正、藍色是上變頻後的微波）。

## `animations/operation.html#pulse`（如何操作量子電腦 3D 場景 3：微波脈衝）

- 滑桿「脈衝面積 → 旋轉角」「脈衝相位 φ → 旋轉軸方向」；按「▶ 送出脈衝」看布洛赫球上的箭頭轉動，「重設 |0⟩」回到北極。
- 試試：面積 90°、相位 0° 送兩次 → 箭頭到南極；重設後先送一次 0°，再把相位改成 90° 送第二次 → 箭頭停在赤道。相位差 90°，結果就不一樣。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['回合', '改了什麼（誰慢半拍）', '第 4 拍讀到', '判別寫下', '最後硬幣', '判別對嗎', '觀察']
SHEET_ROWS = [['正常 1'], ['正常 2'], ['正常 3'], ['驅動站慢半拍'], ['讀取站慢半拍'], ['回饋站慢兩拍'], ['兩個節拍器各打各的']]

EXTRA_CSS = '''table.rec td{height:10mm}table.role td{height:15mm;font-size:11pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.flow{display:flex;flex-wrap:wrap;gap:4mm;margin-top:4mm}.flow div{border:1.5px dashed #4a6a88;border-radius:3mm;width:52mm;height:34mm;
padding:2mm;font-size:10pt;color:#4a6a88}.clockline{border:1.5px dashed #c9a227;border-radius:3mm;height:14mm;margin-top:4mm;padding:2mm;
font-size:10pt;color:#8a6d00}.small{font-size:10pt;color:#4a6a88}'''


def html():
    roles = [('1 上傳', '控制電腦', '第 1 拍：把「翻一次」紙條交給觸發站'),
             ('2 觸發', '同步器', '第 2 拍：喊「開始！」'),
             ('3 驅動', '任意波形產生器（＋混頻器）', '第 3 拍：把硬幣翻面'),
             ('4 讀取', '讀取模組（降頻＋數位化）', '第 4 拍：看硬幣，告訴判別站'),
             ('5 判別', '可程式邏輯晶片', '第 5 拍：寫下 0 或 1'),
             ('6 回饋', '可程式邏輯晶片→波形產生器', '第 6 拍：是 1 就翻回 0，結果交回電腦')]
    role_rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td></td></tr>' for a, b, c in roles)
    rec_rows = ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS)
    pages = [
        '<h2>控制鏈角色卡：六個站</h2><p class="lead">一個人當「時脈」（銣原子鐘）穩定拍手；其他人只能在輪到自己的那一拍動作。硬幣是量子位元：正面＝0、反面＝1。</p>'
        '<table class="rec role"><tr><th>站</th><th>真實儀器</th><th>遊戲裡做什麼</th><th>誰扮演</th></tr>'
        f'{role_rows}</table>'
        '<p class="note">時脈：＿＿＿＿＿＿（一秒拍一下）。真實的 10 MHz 參考，一拍只有 100 ns。</p>',
        '<h2>排練紀錄表：正常版與慢半拍</h2><p class="lead">先跑三次正常版，再一次只讓一站出錯。</p>'
        '<table class="rec"><tr><th>回合</th><th>第 4 拍讀到</th><th>判別寫下</th><th>最後硬幣</th><th>判別對嗎</th><th>觀察</th></tr>'
        f'{rec_rows}</table>'
        '<p>兩個節拍器 60 與 63 拍／分：＿＿＿ 秒後差半拍；＿＿＿ 秒後差一拍。</p>'
        '<p>哪一站慢半拍，最容易讓結果出錯？為什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>我的控制鏈流程圖</h2><p class="lead">在方塊裡寫站名和真實儀器，用箭頭連起來；最後畫一條時脈線連到每一站。</p>'
        '<div class="flow">' + ''.join(f'<div>第 {i} 站：</div>' for i in range(1, 7)) + '</div>'
        '<div class="clockline">時脈線：銣原子鐘 10 MHz →（連到哪幾站？）</div>'
        '<h3 style="margin-top:5mm">相位計算卡（相位差＝360° × 頻率 × 時間差）</h3>'
        '<table class="rec"><tr><th>頻率</th><th>時間差</th><th>相位差</th></tr>'
        '<tr><td>5 GHz</td><td>1 ps</td><td></td></tr><tr><td>5 GHz</td><td>10 ps</td><td></td></tr>'
        '<tr><td>5 GHz</td><td>0.1 ns</td><td></td></tr><tr><td>差 1 Hz</td><td>1 秒</td><td></td></tr></table>'
        '<p class="small">1 ns = 1000 ps；5 GHz = 每秒 50 億圈。</p>',
        '<h2>說明卡：我的控制鏈流程圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 控制電子與時脈在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出一次測量的六個站：上傳、觸發、驅動、讀取、判別、回饋</li><li>說出 10 MHz 參考時脈的用處：大家的頻率都從它倍頻，相位彼此鎖定</li>'
        '<li>說出慢半拍會讓哪裡出錯</li><li>指出一個誤解：每台各自很準還不夠，所有儀器要鎖同一個參考時脈，否則相位會飄</li>'
        '<li>替流程圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q046 控制電子與時脈 列印包', '父子科技學院 量子電腦學程 Q046｜控制電子與時脈', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q046-control-clock', folder='Q046_控制電子與時脈', files=FILES,
        sheet=('03_排練紀錄表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_控制電子與時脈.pdf', pack_pages=4,
        pack_needles=('角色卡', '六個站', '排練紀錄表', '慢半拍', '流程圖', '相位計算卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q046', episode_dir='specials/q046-control-clock',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'phase_drift.py', 'scene': 'animations/peripherals.html#electronics',
               'phase': {'5GHz_period_ns': 0.2, '0.1ns_deg': 180, '10ps_deg': 18, '1ps_deg': 1.8, '1Hz_per_s_deg': 360},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q046/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

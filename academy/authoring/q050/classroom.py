"""Q050 課堂教材：九張校準卡（剪貼）、校準流程卡、重置比較表、少一步預測卡、可執行的 reset_budget.py、說明卡與解答。

不需要帳號、不需要安裝套件（reset_budget.py 只用 Python 標準函式庫；也可以只用計算機）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q050/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 九步校準：slides/QC_Operation_Talk.pptx 第 14 頁（順序、名稱、要調好什麼）；「依賴」與「跳過會怎樣」是本課的教學整理
STEPS = [  # (關, 步驟, 要調好什麼, 依賴前面哪一步, 跳過會怎樣)
    ('第一關 找頻率', '讀取腔頻譜', '讀取頻率與色散位移', '—（降到基溫、線路檢查完成）', '不知道用什麼頻率讀取，後面每一步都讀不出結果'),
    ('第一關 找頻率', '量子位元頻譜', 'f₀₁、f₁₂（非諧性）', '1 讀取頻率', '不知道要用什麼頻率驅動量子位元'),
    ('第二關 調脈衝', 'Rabi 實驗', 'π 脈衝振幅（剛好轉半圈）', '2 f₀₁', '翻轉閘轉太多或太少'),
    ('第二關 調脈衝', 'Ramsey 實驗', '精確頻率（~kHz）', '3 π/2 脈衝', '頻率差一點，π 脈衝轉不到南極、相位慢慢跑掉'),
    ('第三關 量壽命、修閘', 'T₁／T₂ 量測', '能量弛豫、相位相干時間', '3、4 準確的 π、π/2 脈衝', '不知道線路能跑多久、該挑哪顆量子位元'),
    ('第三關 量壽命、修閘', 'DRAG／精修', '減少洩漏到 |2⟩、相位誤差；精修振幅', '2 f₁₂、3 振幅', '閘錯誤率偏高，偶爾漏到 |2⟩'),
    ('第四關 讀取與驗收', '讀取最佳化', '讀取頻率、功率、積分權重、閾值', '1 讀取腔、3 π 脈衝（準備 |1⟩）', '0 和 1 分不清，讀取錯誤變多'),
    ('第四關 讀取與驗收', '兩位元閘', 'CZ 振幅／時間、相位修正', '單位元閘都校好', '糾纏做不好，貝爾態出現 01、10'),
    ('第四關 讀取與驗收', '基準測試', 'RB、XEB 得到每閘錯誤率', '前面全部', '不知道校準好不好，使用者看不到錯誤率'),
]
assert len(STEPS) == 9

PROGRAM = '''"""父子科技學院 量子電腦學程 Q050：初始化與校準——重置時間預算（只用 Python 標準函式庫）

執行：python reset_budget.py
數字是學程簡報（如何操作量子電腦 第 13 頁）整理的代表值，依晶片與平台而異，只用來練習估算。
"""
import math

H = 6.62607015e-34      # 普朗克常數 J·s
KB = 1.380649e-23       # 波茲曼常數 J/K


def thermal_p1(f_ghz, t_mk):
    """兩能階在溫度 T 下停在 |1⟩ 的機率（約等於 exp(−hf/kBT)）。"""
    x = H * f_ghz * 1e9 / (KB * t_mk * 1e-3)
    return 1 / (1 + math.exp(x))


print('一、殘留熱激發（5 GHz 量子位元）')
for t in (10, 40, 50, 60):
    print(f'  等效溫度 {t:>2} mK → 約 {thermal_p1(5, t):.2e}（{thermal_p1(5, t):.2%}）停在 |1⟩')

# 一輪（shot）＝ 線路 + 讀取 + 重置；單位 μs
CIRCUIT, READOUT = 1.0, 1.0
T1 = 50.0                       # 能量弛豫時間 μs（改造區：改成 100 試試）
passive = 5 * T1                # 被動：等 5 T₁
active = READOUT + 0.3 + 0.04 + READOUT   # 主動：讀取、FPGA 判斷、π 脈衝、確認讀取

print('\\n二、被動重置 vs 主動重置')
for name, reset in (('被動等待 5 T₁', passive), ('主動重置', active)):
    shot = CIRCUIT + READOUT + reset
    print(f'  {name:<10} 重置 {reset:7.2f} μs，一輪 {shot:7.2f} μs，重置佔 {reset / shot:5.1%}，'
          f'每秒約 {1e6 / shot:,.0f} 輪')
print(f'  被動等待後殘留在 |1⟩：e^-5 ≈ {math.exp(-5):.2%}')
print(f'  主動重置快約 {passive / active:.0f} 倍')
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q050：初始化與校準（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出兩個藏在幕後的問題：每一輪（shot）開始前，量子位元怎麼回到 |0⟩？量子閘要怎麼調，才能剛好轉對角度？今天的好玩機制是闖關：孩子當校準工程師排九張校準卡，爸爸當關主抽問。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開動畫，認識被動與主動重置、九步校準 | `transmon-3d.html#readout`、`operation.html#pulse`、`peripherals.html#bringup`、`reset_budget.py` |
| 25–65 | 孩子把九張校準卡排成正確順序，寫下每一步調好什麼；爸爸逐關抽問 | 列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 拿掉一張卡，預測哪個結果會出錯，再用動畫驗證 | 列印包第 3 頁、`operation.html#pulse` |
| 105–115 | 孩子教爸爸：兩種重置、九步順序 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `peripherals.html#bringup`（課綱指定）、`operation.html#pulse`、`transmon-3d.html#readout`（不需要網路、伺服器或帳號）。
- 列印 `02_列印包_初始化與校準.pdf`（A4，共 4 頁），剪下第 1 頁的九張校準卡並洗亂。
- 讀一遍 `04_解答.md`。

## 關主的原則

- 每張卡都要說得出「這一步調好了什麼」「它要用到前面哪一步的數字」，答得出才蓋章。
- 排錯了不直接給答案，請孩子說說看會卡在哪一步（例如：還不知道頻率，拉比要用什麼頻率驅動？）。
- 最後一定要問：「今天校準好，明天還準嗎？」——答案是不一定，參數會漂移，每天甚至每幾小時要重做一部分。

## 誠實說明

- 九步順序依學程簡報第 14 頁；周邊系統動畫把它展開成 11 步（多了系統檢查、Punch-out、上線，兩位元閘另計）。不同實驗室的順序會微調，例如讀取最佳化有時放在更前面。
- 分成四關是本課的教學分組，不是業界標準名稱。
- 重置時間、等效溫度、校準頻率都是學程簡報整理的代表值，依晶片與平台而異。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：重置與九步校準（約 40 分鐘）

1. 打開 `animations/transmon-3d.html#readout`（第 5 章讀取），取消「自動接續」，點步驟按鈕 7：看板上三列時間軸比較被動等待、主動重設、無條件重設。
2. 點步驟 8（自由實驗）：按 |1⟩ → 量測一次 → 主動重設，讀左上角字幕；再按 |1⟩ → 被動等待 5T₁，看面板的 P(|1⟩) 慢慢掉下來。
3. 執行 `python reset_budget.py`，把列印包第 3 頁的重置比較表填完。
4. 打開 `animations/peripherals.html#bringup`（場景 10），按「◀ 上一步」「下一步 ▶」逐步看右下角的量測圖。
5. 把九張校準卡洗亂，孩子排順序、在卡背寫「要調好什麼」「用到哪一步的數字」；爸爸逐關抽問，答對蓋章，最後抄到列印包第 2 頁的校準流程卡。

## 下半場：少做一步會怎樣（約 30 分鐘）

1. 爸爸抽走一張卡，孩子在列印包第 3 頁的預測卡寫下：哪個結果會出錯、為什麼。
2. 用 `animations/operation.html#pulse` 驗證「跳過 Ramsey」：把「脈衝面積」調到 180°，按「▶ 送出脈衝」看箭頭到南極；按「重設 |0⟩」，把「頻率失諧 Δ」調到 10 MHz 再送一次，箭頭轉不到南極。
3. 再試「跳過 Rabi」：失諧調回 0，面積改成 150° 或 210°，看翻轉閘轉太少或太多。
4. 討論：今天校準好，明天還準嗎？為什麼雲端系統每天甚至每幾小時重新校準？
''',

'reset_budget.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 九步校準（簡報第 14 頁）\n\n| # | 關 | 步驟 | 要調好什麼 | 用到哪一步 | 跳過會怎樣 |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {i} | {g} | {n} | {w} | {d} | {s} |\n' for i, (g, n, w, d, s) in enumerate(STEPS, 1))
  + '\n校準結果存進校準資料庫，轉譯與產生脈衝時自動取用；參數會因溫度、TLS（材料）缺陷、磁通雜訊漂移，雲端系統通常每天或每數小時自動重新校準。\n\n'
  '## 重置比較（簡報第 13 頁；reset_budget.py 輸出）\n\n'
  '| | 被動重置 | 主動重置 |\n|---|---|---|\n'
  '| 做法 | 什麼都不做，等約 5 T₁ | 先量測，是 1 就送 π 脈衝翻回 0 |\n'
  '| 時間 | 數百 μs（T₁ = 50 μs → 250 μs） | 約 1–5 μs（程式估約 2.3 μs） |\n'
  '| 殘留 | e⁻⁵ ≈ 0.67% | 主要來自讀取誤判，可量兩次確認 |\n'
  '| 需要 | 不需回饋 | FPGA 數百 ns 內即時判別 |\n'
  '| 每秒輪數（線路＋讀取各 1 μs） | 約 3,968 輪，重置佔 99.2% | 約 230,000 輪 |\n\n'
  '殘留熱激發：5 GHz、等效溫度 50 mK → exp(−hf/kBT) ≈ 0.82%；40 mK ≈ 0.25%；60 mK ≈ 1.8%；10 mK ≈ 4×10⁻¹¹。\n\n'
  '## 常見誤解\n\n'
  '- 「校準一次就好」：參數會漂移，每天甚至每幾小時就要重做一部分。\n'
  '- 「量完要重新降溫才能歸零」：冷凍機全程維持約 10 mK，只要讓位元回到 |0⟩。\n'
  '- 「冷凍機 10 mK，所以量子位元一定在 |0⟩」：等效溫度常較高，仍有少量停在 |1⟩，主動重置也順便清掉。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/peripherals.html#bringup`（周邊系統場景 10：啟動與校準，課綱指定）

- 「◀ 上一步」「下一步 ▶」「自動播放」：走過 11 個步驟（系統檢查 → 讀取腔頻譜 → Punch-out → 量子位元頻譜 → Rabi → Ramsey → T₁ → 讀取最佳化 → DRAG／閘微調 → 隨機基準測試 → 上線）。右下角是每一步的典型量測圖。

## `animations/operation.html#pulse`（如何操作量子電腦 場景 3：微波脈衝）

- 「脈衝面積 → 旋轉角」「脈衝相位 φ」「頻率失諧 Δ（MHz）」「閘長度（ns）」滑桿；「▶ 送出脈衝」「虛擬 Z（90°）」「重設 |0⟩」按鈕；方波／高斯／高斯 + DRAG 選項。

## `animations/transmon-3d.html#readout`（Transmon 3D 第 5 章：色散讀取）

- 步驟 7「重設」：三種歸零方法的時間軸。步驟 8「自由實驗」：準備 |0⟩／|1⟩／疊加態、量測一次、主動重設、被動等待 5T₁。

## 操作

滑鼠拖曳旋轉、滾輪縮放；peripherals 與 operation 頁可用左右方向鍵切換場景、`H` 隱藏面板。
''',
}

SHEET_HEADER = ['順序', '關', '步驟', '要調好什麼', '用到哪一步', '跳過會怎樣（我的預測）', '蓋章']
SHEET_ROWS = [[str(i), g, n, '', '', '', ''] for i, (g, n, *_) in enumerate(STEPS, 1)]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:4mm}
.card{border:1.4pt dashed #0b2540;border-radius:2mm;padding:3mm;height:48mm;display:flex;flex-direction:column;justify-content:space-between}
.card b{font-size:15pt}.card .q{font-size:10pt;color:#4a6a88}.card .ln{border-bottom:.8pt solid #9fb3c8;height:6mm}
table.fl td{height:10.5mm;font-size:10.5pt}table.fl th{font-size:10.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.cmp td{height:9mm}'''

# 卡片洗亂的固定順序（讓孩子自己排）
SHUFFLE = [4, 7, 1, 9, 3, 6, 2, 8, 5]
assert sorted(SHUFFLE) == list(range(1, 10))


def html():
    cards = ''.join(f'<div class="card"><b>{STEPS[k - 1][1]}</b><span class="q">這一步調好了什麼？</span>'
                    '<div class="ln"></div><span class="q">要用到哪一步的數字？</span><div class="ln"></div></div>'
                    for k in SHUFFLE)
    fl = ''.join(f'<tr><td style="width:10mm">{i}</td><td style="width:30mm"></td><td></td><td></td><td style="width:14mm"></td></tr>'
                 for i in range(1, 10))
    pages = [
        '<h2>九張校準卡</h2><p class="lead">沿虛線剪下、洗亂。排出正確順序，在空白處寫下這一步調好了什麼、要用到哪一步的數字。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>校準流程卡</h2><p class="lead">把排好的九張卡抄下來；關主（爸爸）抽問，答得出理由才蓋章。</p>'
        f'<table class="fl"><tr><th>#</th><th>步驟</th><th>要調好什麼</th><th>用到哪一步</th><th>章</th></tr>{fl}</table>'
        '<div class="box" style="margin-top:4mm"><p>流程卡名稱：＿＿＿＿＿＿＿＿＿＿　校準工程師：＿＿＿＿＿　關主：＿＿＿＿＿</p>'
        '<p class="note">提示：分成四關——找頻率、調脈衝、量壽命修閘、讀取與驗收。結果存進校準資料庫；參數會漂移，要定期重做。</p></div>',
        '<h2>重置比較表</h2><p class="lead">用 reset_budget.py 或計算機填完。</p>'
        '<table class="cmp"><tr><th></th><th>被動重置</th><th>主動重置</th></tr>'
        '<tr><td>怎麼做</td><td></td><td></td></tr><tr><td>要多久</td><td></td><td></td></tr>'
        '<tr><td>殘留在 |1⟩</td><td></td><td></td></tr><tr><td>每秒約幾輪</td><td></td><td></td></tr></table>'
        '<h2 style="margin-top:5mm">少一步預測卡</h2><div class="box">'
        '<p>1. 拿掉的卡：＿＿＿＿＿＿＿＿　我預測出錯的結果：＿＿＿＿＿＿＿＿＿＿＿＿</p><div class="line"></div>'
        '<p>2. 拿掉的卡：＿＿＿＿＿＿＿＿　我預測出錯的結果：＿＿＿＿＿＿＿＿＿＿＿＿</p><div class="line"></div>'
        '<p>3. 很久都不重新校準，會怎樣？</p><div class="line"></div>'
        '<p>4. 用 operation.html#pulse 驗證：失諧 10 MHz 時，箭頭停在哪裡？＿＿＿＿＿＿</p></div>',
        '<h2>說明卡：我的校準流程</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 初始化在解決什麼？</p><div class="line"></div><p>2. 為什麼校準的順序不能亂排？</p><div class="line"></div>'
        '<p>3. 生活中哪件事也要「先做 A 才能做 B」？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出被動重置和主動重置差在哪裡</li><li>排出九步校準，說出每一步調好什麼</li>'
        '<li>說出一步沒做會錯在哪裡</li><li>指出限制：校準會漂移，每天甚至每幾小時要重做一部分</li>'
        '<li>替校準流程卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q050 初始化與校準 列印包', '父子科技學院 量子電腦學程 Q050｜初始化與校準', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q050-init-calibration', folder='Q050_初始化與校準', files=FILES,
        sheet=('03_校準流程卡.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_初始化與校準.pdf', pack_pages=4,
        pack_needles=('九張校準卡', '校準流程卡', '重置比較表', '少一步預測卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q050', episode_dir='specials/q050-init-calibration',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'reset_budget.py', 'calibrationSteps': [n for _, n, *_ in STEPS],
               'stepsFrom': 'slides/QC_Operation_Talk.pptx p14', 'resetFrom': 'slides/QC_Operation_Talk.pptx p13',
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q050/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

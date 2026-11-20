"""Q052 課堂教材：脈衝設計紀錄（闖關表）、失諧實驗表、面積加法練習、可執行的 pulse_lab.py、說明卡與解答。

不需要帳號、不需要安裝套件（pulse_lab.py 只用 Python 標準函式庫；也可以只用動畫）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q052/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 闖關：operation.html#pulse（高斯、40 ns、失諧 0）；落點以 Bloch 座標與 1600×900 畫面方向表示（Python 重現 03_pulse.js 確認）
LEVELS = [  # (關, 目標, 面積, 相位, 落點, P(1))
    ('第一關 翻轉', '從 |0⟩ 到 |1⟩', '180°', '0°', '南極（|1⟩）', '1.000'),
    ('第二關 疊加', '停在赤道、一半一半', '90°', '0°', '赤道 −y（畫面左邊）', '0.500'),
    ('第三關 繞 y 軸', '繞 y 軸轉到赤道', '90°', '90°', '赤道 +x（朝向觀眾）', '0.500'),
    ('第四關 分段', '用四個小脈衝到 |1⟩', '45° × 4', '0°', '南極（|1⟩）', '1.000'),
    ('第五關 倒帶', '轉出去再轉回 |0⟩', '90° 再 90°', '0° 再 180°', '回到北極（|0⟩）', '0.000'),
]
DETUNE = [  # (失諧 MHz, 軸翹起角度, 面積 180° 的 P(1))
    ('0', '0°', '1.000'), ('5', '約 22°', '0.933'), ('10', '約 39°', '0.753'), ('20', '約 58°', '0.300'),
]

PROGRAM = '''"""父子科技學院 量子電腦學程 Q052：微波脈衝——面積與相位的小實驗室（只用 Python 標準函式庫）

執行：python pulse_lab.py
模型：旋轉座標中的方波脈衝，旋轉軸 = (cos φ, sin φ, Δ/Ω)。和動畫一樣忽略退相干，只用來練習「面積轉幾度、相位繞哪軸」。
"""
import math


def rotate(v, axis, angle):
    """把布洛赫向量 v 繞 axis 轉 angle（弧度），羅德里格斯公式。"""
    n = math.sqrt(sum(a * a for a in axis))
    a, b, c = (x / n for x in axis)
    x, y, z = v
    co, si = math.cos(angle), math.sin(angle)
    d = a * x + b * y + c * z
    return (x * co + (b * z - c * y) * si + a * d * (1 - co),
            y * co + (c * x - a * z) * si + b * d * (1 - co),
            z * co + (a * y - b * x) * si + c * d * (1 - co))


def pulse(v, area_deg, phase_deg=0, detune_mhz=0, t_ns=40):
    """送一個方波脈衝：面積 area_deg（度）、相位 phase_deg（度）、失諧 detune_mhz、時間 t_ns。"""
    omega = math.radians(area_deg) / t_ns            # 拉比角頻率 rad/ns
    delta = 2 * math.pi * detune_mhz * 1e-3          # 失諧角頻率 rad/ns
    ph = math.radians(phase_deg)
    axis = (omega * math.cos(ph), omega * math.sin(ph), delta)
    return rotate(v, axis, math.sqrt(omega ** 2 + delta ** 2) * t_ns)


def show(name, v):
    p1 = (1 - v[2]) / 2
    print(f'  {name:<22} 箭頭 (x, y, z) = ({v[0]:+.2f}, {v[1]:+.2f}, {v[2]:+.2f})  量到 1 的機率 {p1:.3f}')


NORTH = (0.0, 0.0, 1.0)
print('一、面積決定轉幾度（相位 0°）')
for a in (45, 90, 180, 270, 360):
    show(f'面積 {a}°', pulse(NORTH, a))

print('\\n二、相位決定繞哪條軸（面積 90°）')
for ph in (0, 90, 180, 270):
    show(f'相位 {ph}°', pulse(NORTH, 90, ph))

print('\\n三、闖關檢查')
v = NORTH
for _ in range(4):
    v = pulse(v, 45)
show('45° 送四次', v)
show('90°@0° 再 90°@180°', pulse(pulse(NORTH, 90, 0), 90, 180))

print('\\n四、控制變因：面積 180°、相位 0°，只改失諧（方波 40 ns，平均拉比頻率 12.5 MHz）')
for d in (0, 5, 10, 20):   # 改造區：自己加 2.5、15 試試
    tilt = math.degrees(math.atan2(d, 12.5))
    v = pulse(NORTH, 180, 0, d)
    print(f'  失諧 {d:>4} MHz  軸翹起 {tilt:4.1f}°  量到 1 的機率 {(1 - v[2]) / 2:.3f}')
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q052：微波脈衝——面積與相位（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心只有兩句：**脈衝面積決定轉幾度，脈衝相位決定繞哪一條軸。** 好玩機制是闖關：孩子當脈衝設計師，先在紀錄上寫下面積和相位的預測，再到動畫裡送出脈衝；爸爸當關主出題、蓋章。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開動畫，認識面積、相位兩個旋鈕 | `operation.html#pulse`、`transmon-3d.html#control` |
| 25–65 | 闖五關：翻轉、疊加、繞 y 軸、分段、倒帶 | 列印包第 1 頁（脈衝設計紀錄） |
| 65–75 | 休息 | |
| 75–105 | 控制變因：只改失諧，記錄軸翹起多少、P(1) 剩多少 | 列印包第 2 頁、`pulse_lab.py` |
| 105–115 | 孩子教爸爸：面積與相位的作用、一個限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#pulse`（課綱指定）與 `transmon-3d.html#control`（不需要網路、伺服器或帳號）。
- 列印 `02_列印包_微波脈衝面積與相位.pdf`（A4，共 4 頁）。
- 讀一遍 `04_解答.md`。

## 關主的原則

- 每一關先寫預測，再送脈衝；箭頭停對地方才蓋章。
- 預測錯了不直接給答案，請孩子說：是面積想錯，還是相位想錯？
- 下半場一定要守住「一次只改一個條件」：面積、相位固定，只動失諧。

## 誠實說明

- 動畫與 `pulse_lab.py` 都忽略退相干，只示範旋轉；真實量子位元還有 T₁、T₂ 與洩漏。
- 動畫用高斯脈衝，`pulse_lab.py` 用方波，失諧時的 P(1) 不一樣（10 MHz：動畫的高斯 0.753、方波模型 0.499；20 MHz：0.300 對 0.009）；趨勢相同，都是失諧越大越轉不到南極。
- 方向說明：動畫中 x 軸（橘）朝向觀眾、y 軸（綠）朝右；你轉動視角後，左右會跟著改變。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：五關（約 40 分鐘）

打開 `animations/operation.html#pulse`。每一關前先按「重設 |0⟩」，把「頻率失諧 Δ」留在 0。

1. 第一關 翻轉：「脈衝面積」180°、「脈衝相位 φ」0°，按「▶ 送出脈衝」，箭頭到南極。
2. 第二關 疊加：面積 90°、相位 0°，箭頭停在赤道（畫面左邊）。粉紅色直線是這次的旋轉軸。
3. 第三關 繞 y 軸：面積 90°、相位 90°，粉紅軸和綠色 y 軸重疊，箭頭朝你倒下。
4. 第四關 分段：面積 45°，連按四次送出（每次等箭頭停下），看能不能到南極。
5. 第五關 倒帶：面積 90°、相位 0° 送一次；不按重設，把相位改成 180° 再送一次，箭頭回到北極。
6. 加碼：打開 `transmon-3d.html#control`（第 4 章），面板往下捲，分別按「X 軸 π/2」「Y 軸 π/2」，比較「此刻的狀態」的式子。

## 下半場：控制變因（約 30 分鐘）

1. 面積 180°、相位 0°，失諧依序設成 0、5、10、20 MHz；每次先按「重設 |0⟩」再送出。
2. 看粉紅色旋轉軸翹起多少、箭頭停在哪裡；把面板「目前 P(1)」抄到列印包第 2 頁。
3. 執行 `python pulse_lab.py`，比較方波模型的數字。
4. 討論：為什麼校準時要先把頻率對準（拉姆齊實驗）？
''',

'pulse_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 五關（operation.html#pulse，高斯 40 ns、失諧 0）\n\n| 關 | 目標 | 面積 | 相位 | 落點 | P(1) |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} | {f} |\n' for a, b, c, d, e, f in LEVELS)
  + '\n## 失諧實驗（面積 180°、相位 0°；動畫的高斯 40 ns 模型）\n\n| 失諧 | 軸翹起 | P(1) |\n|---|---|---|\n'
  + ''.join(f'| {d} MHz | {t} | {p} |\n' for d, t, p in DETUNE)
  + '\n軸翹起角度 = atan(失諧 ÷ 平均拉比頻率)，40 ns 的 180° 脈衝平均拉比頻率是 12.5 MHz。\n\n'
  '## 面積加法練習\n\n- 45° × 4 = 180°（翻轉閘）；90° × 2 = 180°；30° × 6 = 180°；360° 轉一圈回到 |0⟩。\n'
  '- 40 ns 的高斯 180° 脈衝峰值拉比頻率約 23 MHz；時間縮成 20 ns 要約 47 MHz。\n\n'
  '## 常見誤解\n\n'
  '- 「面積一樣，脈衝就一樣」：轉的角度一樣，但形狀不同頻譜不同；動畫頻譜圖中 f₁₂ 處方波約 −34 dB、高斯約 −59 dB，方波較容易洩漏到 |2⟩。\n'
  '- 「相位不同，量起來不同」：90° 脈衝不管相位多少，P(1) 都是 0.5；相位差別要靠之後的脈衝或干涉才看得出來。\n'
  '- 「頻率差一點沒關係」：失諧讓旋轉軸翹起，翻轉閘轉不到南極。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#pulse`（如何操作量子電腦 場景 3：微波脈衝，課綱指定）

- 滑桿：「脈衝面積 → 旋轉角」「脈衝相位 φ → 旋轉軸方向」「頻率失諧 Δ（MHz）」「閘長度（ns）」。
- 按鈕：「▶ 送出脈衝」「虛擬 Z（90°）」「重設 |0⟩」；選項：方波／高斯／高斯 + DRAG。
- 畫面：中間是 3D 波形（金色 I、青色 Q、白色實際微波）；右上是布洛赫球，送脈衝時粉紅色直線是旋轉軸；右下插圖是包絡與頻譜（紅色虛線是 f₁₂）。

## `animations/transmon-3d.html#control`（Transmon 3D 第 4 章：用微波轉動布洛赫球）

- 按鈕「X 軸 π」「X 軸 π/2」「Y 軸 π/2」「持續驅動（Rabi 振盪）」「重設 |0⟩」；面板顯示「此刻的狀態」與量測機率。

## 操作

滑鼠拖曳旋轉、滾輪縮放；operation 頁可用左右方向鍵切換場景、`H` 隱藏面板。
''',
}

SHEET_HEADER = ['關', '目標', '我的面積', '我的相位', '預測落點', '實際落點', '蓋章']
SHEET_ROWS = [[a, b, '', '', '', '', ''] for a, b, *_ in LEVELS]

EXTRA_CSS = '''table.fl td{height:14mm;font-size:11pt}table.fl th{font-size:10.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.cmp td{height:11mm}'''


def html():
    fl = ''.join(f'<tr><td style="width:28mm">{a}</td><td style="width:34mm">{b}</td><td></td><td></td><td></td><td></td><td style="width:12mm"></td></tr>'
                 for a, b, *_ in LEVELS)
    det = ''.join(f'<tr><td>{d} MHz</td><td></td><td></td><td></td></tr>' for d, *_ in DETUNE)
    pages = [
        '<h2>脈衝設計紀錄</h2><p class="lead">每一關先寫下面積和相位的預測，再到 operation.html#pulse 送出脈衝；箭頭停對地方，關主蓋章。</p>'
        '<table class="fl"><tr><th>關</th><th>目標</th><th>面積</th><th>相位</th><th>預測落點</th><th>實際落點</th><th>章</th></tr>'
        f'{fl}</table>'
        '<div class="box" style="margin-top:4mm"><p>紀錄名稱：＿＿＿＿＿＿＿＿＿＿　脈衝設計師：＿＿＿＿＿　關主：＿＿＿＿＿</p>'
        '<p class="note">提示：面積決定轉幾度，相位決定繞哪條軸。每關先按「重設 |0⟩」（倒帶關除外），失諧保持 0。</p></div>',
        '<h2>失諧實驗表</h2><p class="lead">控制變因：面積固定 180°、相位固定 0°，只改失諧。每次先按「重設 |0⟩」。</p>'
        '<table class="cmp"><tr><th>失諧</th><th>粉紅軸翹起多少（畫圖或描述）</th><th>箭頭停在哪裡</th><th>P(1)</th></tr>'
        f'{det}</table>'
        '<div class="box" style="margin-top:5mm"><p>把 P(1) 畫成曲線（橫軸：失諧 MHz，縱軸：P(1)）</p>'
        '<div style="height:60mm;border-left:1pt solid #0b2540;border-bottom:1pt solid #0b2540;margin:3mm 0 0 8mm"></div>'
        '<p class="note">我固定了：＿＿＿＿＿＿＿＿　我只改了：＿＿＿＿＿＿＿＿</p></div>',
        '<h2>面積加法練習</h2><p class="lead">面積＝振幅×時間，可以一段一段累加。</p><div class="box">'
        '<p>1. 45° 送幾次會到南極？＿＿＿　30° 呢？＿＿＿</p><div class="line"></div>'
        '<p>2. 360° 送一次，箭頭停在哪裡？＿＿＿＿＿＿　為什麼？</p><div class="line"></div>'
        '<p>3. 40 ns 的 180° 脈衝峰值約 23 MHz；時間縮成 20 ns，振幅要變成幾倍？＿＿＿</p><div class="line"></div>'
        '<p>4. 90°（相位 0°）和 90°（相位 90°）量到 1 的機率各是多少？它們是同一個狀態嗎？</p><div class="line"></div>'
        '<p>5. 面積一樣是 180°，方波和高斯脈衝有什麼不同？（看右下插圖的 f₁₂）</p><div class="line"></div></div>',
        '<h2>說明卡：我的脈衝設計</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 脈衝面積在解決什麼？</p><div class="line"></div><p>2. 我怎麼用相位做出繞 y 軸的旋轉？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：面積決定轉幾度</li><li>不看稿說出：相位決定繞哪條軸</li>'
        '<li>示範倒帶關：90°@0° 再 90°@180° 回到 |0⟩</li><li>指出限制：面積相同、形狀不同，頻譜和洩漏不同</li>'
        '<li>替脈衝設計紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q052 微波脈衝：面積與相位 列印包', '父子科技學院 量子電腦學程 Q052｜微波脈衝：面積與相位', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q052-pulse-area-phase', folder='Q052_微波脈衝面積與相位', files=FILES,
        sheet=('03_脈衝設計紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_微波脈衝面積與相位.pdf', pack_pages=4,
        pack_needles=('脈衝設計紀錄', '失諧實驗表', '面積加法練習', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q052', episode_dir='specials/q052-pulse-area-phase',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'pulse_lab.py', 'levels': [a for a, *_ in LEVELS],
               'pulseFrom': 'slides/QC_Operation_Talk.pptx p20', 'leakageFrom': 'slides/QC_Operation_Talk.pptx p21',
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q052/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

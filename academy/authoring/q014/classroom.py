"""Q014 課堂教材：雜訊卡、故障卡遊戲紀錄、防雜訊方法卡、說明卡、解答、noise_numbers.py、動畫導覽。

不需要帳號，也不需要安裝套件（noise_numbers.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#bloch。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q014/classroom.py
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

H, KB = 6.62607015e-34, 1.380649e-23
T_QUBIT_MK = H * 5e9 / KB * 1000          # 5 GHz 量子位元的能量換算成溫度（mK）
RATIO = T_QUBIT_MK / 10                    # 冷到 10 mK 時，量子位元能量是熱的幾倍
GATES = 100e-6 / 25e-9                     # 相位相干時間 100 微秒 ÷ 閘時間 25 奈秒
# 動畫 js/scenes/01_bloch.js 的示意：T1 = 5、T2 = 6（相對時間，秒）
T1_ANIM = [round(math.exp(-t / 5), 2) for t in (0, 3, 6, 9, 12)]
T2_ANIM = [round(math.exp(-t / 6), 2) for t in (0, 3, 6, 9, 12)]
assert round(T_QUBIT_MK) == 240 and round(RATIO) == 24 and round(GATES) == 4000
assert T1_ANIM == [1.0, 0.55, 0.3, 0.17, 0.09] and T2_ANIM == [1.0, 0.61, 0.37, 0.22, 0.14]

PROGRAM = '''"""父子科技學院 量子電腦學程 Q014：量子態很怕吵——用數字看雜訊。

不用安裝任何套件，只要 Python 3。執行：  python noise_numbers.py
可以改下面的 FREQ_GHZ（量子位元頻率）、FRIDGE_MK（冰箱溫度）、T2_US、GATE_NS 看看數字怎麼變。
"""
import math

FREQ_GHZ = 5       # 量子位元頻率（吉赫）
FRIDGE_MK = 10     # 冰箱最底層的溫度（毫克耳文）
T2_US = 100        # 相位相干時間（微秒）
GATE_NS = 25       # 一個閘要多久（奈秒）

h, kB = 6.62607015e-34, 1.380649e-23
qubit_mK = h * FREQ_GHZ * 1e9 / kB * 1000
ratio = qubit_mK / FRIDGE_MK
print(f'{FREQ_GHZ} GHz 量子位元的能量，約等於 {qubit_mK:.0f} mK 的熱')
print(f'冰箱 {FRIDGE_MK} mK：量子位元能量是熱的 {ratio:.1f} 倍，被熱踢上去的機會約 e^-{ratio:.1f} ≈ {math.exp(-ratio):.1e}')
print(f'相位相干時間 {T2_US} 微秒 ÷ 閘時間 {GATE_NS} 奈秒 ≈ {T2_US * 1000 / GATE_NS:.0f} 個閘')
print()
print('動畫 index.html#bloch 的示意（相對時間）：')
for t in (0, 3, 6, 9, 12):
    print(f'  t = {t:2d}：能量弛豫模式 P(1) = {math.exp(-t / 5):.2f}；拉姆齊模式 箭頭大小 = {math.exp(-t / 6):.2f}')
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q014：量子態很怕吵——雜訊與退相干（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：一起做一副「雜訊卡」，每張寫一種干擾和它讓布洛赫球上的箭頭怎麼變，再用三維動畫對照；下半場孩子自己設計「防雜訊方法卡」。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 資訊漏到環境、箭頭變短、能量弛豫（T1）和失相（T2）、為什麼要冷到 10 mK | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 一起做雜訊卡（至少 4 張），玩故障卡：抽卡後用動畫演出來 | `01_操作步驟.md`、列印包第 1–2 頁、`03_故障卡紀錄表.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子設計防雜訊方法卡：選一種雜訊、想擋法、寫清楚擋住哪一種 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：兩種壞法、為什麼要冷、一個限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 空白卡片（或把列印包第 1 頁剪開）、彩色筆。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `index.html#bloch`（場景 1：量子位元與 Bloch 球），先自己按一次「T1 能量弛豫」和「Ramsey 進動 + T2」。
- 列印 `02_列印包_雜訊卡.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 有電腦可以跑 Python 3 的話，先執行一次 `noise_numbers.py`（不需要安裝套件）。

## 帶的原則

- 先讓孩子說「箭頭會怎麼變」，再打開動畫驗證；猜錯沒關係，對照時改卡片就好。
- 兩種壞法分清楚：能量弛豫是箭頭往北極（零態）回去；失相是赤道上的箭頭一邊轉一邊縮、得到一的機率一直一半。
- 最常見的誤解：「冷」是為了讓熱雜訊遠小於量子位元的能量，不是為了讓電腦跑得更快。

## 誠實說明

- 動畫的衰減時間是放慢很多的示意（約 5、6 秒）；真實晶片的能量弛豫時間，簡報寫最好的約 0.1–1 毫秒。
- 雜訊卡上的「干擾」是幫助理解的分類，真實晶片裡同一種干擾常常同時影響兩種壞法。
- 防雜訊的方法沒有萬靈丹：每一種方法只擋住某些雜訊，這正是今天要孩子練習說清楚的地方。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：一起做雜訊卡、玩故障卡（約 40 分鐘）

1. 打開 `animations/index.html#bloch`，按「π/2 脈衝 → 疊加態」：箭頭在赤道上、碰著球面，讀數寫「純態」。這是沒有雜訊的對照組。
2. 按「T1 能量弛豫」：箭頭從南極（一態）出發，沿縱軸往上縮、穿過球心、指向北極（零態）那一側；右下小圖的曲線往下滑。
3. 按「Ramsey 進動 + T2」：箭頭在赤道上一邊轉一邊縮，留下往內捲的軌跡；右下小圖一直停在 0.5，讀數出現「混態：失去相干性」。
4. 把「失諧 Δ（Ramsey）」滑桿拉到 0，再按一次「Ramsey 進動 + T2」：箭頭不轉，但照樣縮短。
5. 用列印包第 1 頁做雜訊卡，至少 4 張：寫干擾的名字、它從哪裡來、畫出箭頭怎麼變、屬於哪一種壞法、動畫按哪一顆對照。
   參考干擾：多餘的熱、線路帶進來的電磁雜訊、材料裡的缺陷、讀取太慢、讀取腔裡的熱光子。
6. 玩故障卡：卡片洗牌、背面朝上。爸爸抽一張念出來，孩子在動畫裡按對應的模式，說出箭頭會怎麼變。記在列印包第 2 頁。

## 下半場：防雜訊方法卡（約 30 分鐘）

1. 選一張雜訊卡，想一個擋住它的方法（參考：冷卻、金屬屏蔽、濾波、更乾淨的材料、讀快一點、算快一點）。
2. 在列印包第 3 頁寫清楚：它擋住哪一種雜訊？擋不住哪一種？
3. 有電腦的話，執行 `noise_numbers.py`，把 FRIDGE_MK 改成 100、1000，看看「被熱踢上去的機會」怎麼變。
''',

'noise_numbers.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 兩種壞法\n\n'
  '| | 能量弛豫（T1） | 失相（T2） |\n|---|---|---|\n'
  '| 發生什麼事 | 一態把能量交給環境，掉回零態 | 能量沒變少，相位被雜訊攪亂 |\n'
  '| 箭頭怎麼變 | 從南極沿縱軸往北極回去 | 赤道上一邊轉一邊縮短 |\n'
  '| 得到一的機率 | 從 1 往下掉 | 一直是 0.5 |\n'
  '| 動畫按鈕 | 「T1 能量弛豫」 | 「Ramsey 進動 + T2」 |\n\n'
  '動畫的示意數字（noise_numbers.py 實跑，相對時間 0、3、6、9、12）：能量弛豫 P(1) = '
  + '、'.join(f'{p:.2f}' for p in T1_ANIM) + '；拉姆齊箭頭大小 = ' + '、'.join(f'{p:.2f}' for p in T2_ANIM) + '。\n\n'
  '## 為什麼要冷到 10 mK\n\n'
  f'5 GHz 量子位元的能量約等於 {T_QUBIT_MK:.0f} mK 的熱；冷到 10 mK，量子位元能量是熱的 {RATIO:.0f} 倍（熱只剩 1/24），'
  f'被熱踢上去的機會約 e⁻²⁴ ≈ {math.exp(-RATIO):.0e}。冷是為了讓熱雜訊遠小於量子位元的能量，不是為了跑得更快。\n\n'
  f'## 經驗法則\n\n相位相干時間 100 微秒 ÷ 閘時間 25 奈秒 ≈ {GATES:.0f} 個閘。\n\n'
  '## 暫停題：讀取比能量弛豫時間還久，會怎樣？\n\n讀到一半，一態可能已經掉回零態，讀到錯的結果。所以讀取時間必須遠小於能量弛豫時間。\n\n'
  '## 防雜訊方法參考\n\n'
  '| 方法 | 主要擋住 | 擋不住的例子 |\n|---|---|---|\n'
  '| 冷到 10 mK | 熱激發、熱光子 | 外面來的電磁波、材料缺陷 |\n'
  '| 金屬屏蔽 | 外面的電磁場 | 熱、材料缺陷 |\n'
  '| 更乾淨的材料 | 材料裡的缺陷 | 外面的電磁波 |\n'
  '| 讀快一點、算快一點 | 不擋雜訊，而是在壞掉前做完 | 任何雜訊本身 |\n\n'
  '「擋不住的例子」是課堂討論用的簡化說法；真實晶片裡各種雜訊會互相影響。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/index.html#bloch`（場景 1：量子位元與 Bloch 球）

- 金色箭頭是量子態：北極 |0⟩、南極 |1⟩、赤道是一半一半的疊加。箭頭尖端的小標籤是 P(1)。
- 模式按鈕：「Rabi 振盪」（微波讓箭頭繞圈）、「Ramsey 進動 + T2」（失相）、「T1 能量弛豫」、「手動 θ / φ」。每按一次都從頭開始；每 12 秒自動重來。
- 「π/2 脈衝 → 疊加態」：把箭頭放到赤道上，沒有雜訊、不會縮短（讀數寫「純態」）。
- 「失諧 Δ（Ramsey）」滑桿：拉姆齊模式下箭頭轉圈的快慢；拉到 0 就不轉，但照樣縮短。
- 左邊讀數：Bloch 向量和箭頭大小 |r|；|r| 小於 0.98 會寫「混態：失去相干性」。
- 右下小圖：P(|1⟩) 隨時間變化。能量弛豫模式往下滑；拉姆齊模式是停在 0.5 的平線。

## 操作

`H` 隱藏面板；空白鍵暫停；滑鼠拖曳旋轉、滾輪縮放；`R` 重設視角。
''',
}

SHEET_HEADER = ['第幾輪', '抽到的雜訊卡', '它從哪裡來', '屬於哪一種壞法', '動畫按哪一顆', '箭頭怎麼變（孩子說）', '對照動畫後對了嗎', '可以用什麼方法擋']
SHEET_ROWS = [[str(i)] for i in range(1, 9)]

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}.card{border:1.4pt dashed #0b2540;border-radius:3mm;padding:3mm 4mm;
font-size:11.5pt;line-height:1.55}.card b{display:block;font-size:12.5pt;margin-bottom:1mm}.card .ball{display:inline-block;width:16mm;height:16mm;
border:1.2pt solid #0b2540;border-radius:50%;float:right;margin-left:2mm}'''


def card(n):
    return (f'<div class="card"><span class="ball"></span><b>雜訊卡 {n}</b>干擾名稱：＿＿＿＿＿＿<br>從哪裡來：＿＿＿＿＿＿<br>'
            '箭頭怎麼變（畫在右邊的球上）：<br>＿＿＿＿＿＿＿＿＿＿＿＿<br>壞法：□ 能量弛豫　□ 失相<br>動畫按：＿＿＿＿＿＿</div>')


def html():
    pages = [
        '<h2>雜訊卡（剪下來）</h2><p class="lead">每張卡寫一種干擾，畫出布洛赫球上的箭頭會怎麼變，再用動畫對照。</p>'
        f'<div class="cards">{"".join(card(i) for i in range(1, 7))}</div>'
        '<p class="note">參考：多餘的熱、電磁雜訊、材料缺陷、讀取太慢、讀取腔裡的熱光子。</p>',
        '<h2>故障卡遊戲紀錄</h2><p class="lead">爸爸抽一張雜訊卡，孩子先說箭頭會怎麼變，再在動畫裡按對應的模式驗證。</p>'
        '<table class="rec"><tr><th>輪</th><th>抽到的卡</th><th>壞法</th><th>動畫按哪一顆</th><th>先說：箭頭怎麼變</th><th>對了嗎</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 9)) + '</table>'
        '<div class="box" style="margin-top:5mm"><h3>對照組</h3><p>按「π/2 脈衝 → 疊加態」：箭頭在＿＿＿＿上，讀數寫＿＿＿＿。</p>'
        '<p>按「Ramsey 進動 + T2」：右下小圖一直停在＿＿＿＿。</p></div>',
        '<h2>換你改造：防雜訊方法卡</h2><p class="lead">選一種雜訊，想一個擋法，寫清楚它擋住哪一種、擋不住哪一種。</p>'
        '<div class="box"><h3>我的防雜訊方法卡</h3><p>方法名稱：＿＿＿＿＿＿＿＿＿＿</p><p>它擋住的雜訊：＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>保護的是：□ 能量弛豫　□ 失相　□ 兩種都有</p><p>它是怎麼擋的：</p><div class="line"></div><div class="line"></div>'
        '<p>它擋不住的雜訊（至少一種）：＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>挑戰</h3><p>冰箱從 10 mK 變成 100 mK，量子位元能量是熱的幾倍？（240 ÷ 100 ＝＿＿）</p>'
        '<p>相位相干時間 100 微秒，閘要 25 奈秒，大約能做＿＿＿＿個閘？</p></div>',
        '<h2>說明卡：我的雜訊卡牌組</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 量子態為什麼會壞？</p><div class="line"></div><p>2. 能量弛豫和失相，箭頭各怎麼變？</p><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出兩種壞法，並在動畫裡各按一次</li><li>說出箭頭變短代表什麼</li>'
        '<li>說出為什麼要冷到 10 mK（熱和量子位元能量比一比）</li><li>說出冷不是為了跑得更快</li>'
        '<li>介紹一張自己設計的防雜訊方法卡</li><li>替卡牌組取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q014 雜訊卡 列印包', '父子科技學院 量子電腦學程 Q014｜量子態很怕吵：雜訊與退相干', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q014-noise-decoherence', folder='Q014_雜訊卡', files=FILES,
        sheet=('03_故障卡紀錄表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_雜訊卡.pdf', pack_pages=4,
        pack_needles=('雜訊卡', '故障卡遊戲紀錄', '防雜訊方法卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q014', episode_dir='specials/q014-noise-decoherence',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（noise_numbers.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'noise_numbers.py', 'recordedRun': {'qubit_mK_5GHz': round(T_QUBIT_MK), 'ratio_at_10mK': round(RATIO, 1),
                                                              'gates_100us_25ns': round(GATES)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q014/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')

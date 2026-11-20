"""Q032 模組發表：設計我的 transmon — v2 動畫展示段（格式見 ../demos.py 的說明）。

第 1、2 段用課綱「家長課前準備」指定的 index.html#potential（demos.PAGES['jj']；js/scenes/04_potential.js，App.register id 'potential'，第 3 行；
index.html 第 43 行載入；#controls 在 #panel 內，index.html 第 26–31 行）。第 3 段用 transmon-3d.html#capacitor（demos.PAGES['tr']，第 1 章「大十字電容的作用」分頁），
當作本課第 9 頁說的「參數設計器」（課綱的設計器工具尚未新增；這個分頁有 C_Σ 滑桿和 E_C、比值、f₀₁、α、電荷色散、判斷六個讀數）。
每段都是新開頁面（record_demo.js 第 14–19 行），從頁面預設狀態開始；三段開頭都先把 #panel 捲到底（同 Q025、Q028 的 _PANEL），讓按鈕、滑桿和讀數入鏡；旁白不提捲動。

index.html#potential（04_potential.js）：
- 載入時的初始狀態：EC = 0.25 GHz 固定（第 12 行）；ratio = 50、mode = 'transmon'（第 13 行）；第一排「JJ / Transmon（非線性）」與下排「Transmon：50」為 on（第 114、116 行；core.js 第 345–352 行）。
- #controls 依序（core.js 第 339–370 行）：第一排 radio「LC 諧振子（線性）」「JJ / Transmon（非線性）」（第 114 行）、滑桿「E_J / E_C（對數刻度）」min 0、max 2、step 0.01、值 = log10 比值、
  顯示 10^v 取一位小數（第 115 行）、下排 radio「CPB：E_J/E_C = 1」「10」「Transmon：50」（第 116 行）、讀數（第 22、109–112 行）。
  record_demo.js 'click' 以 '#controls button' 的 textContent.trim().startsWith 比對（第 26 行）：'LC' 只對到「LC 諧振子（線性）」、'JJ' 只對到「JJ / Transmon（非線性）」。
  'slider' 以 '#controls .slider' 的 textContent.includes 找（第 27–28 行），本場景只有一根滑桿；值直接寫 log10（1.75…2.00），按下後 oninput → ratio = 10^v → rebuild。
  不用 'sweep'（record_demo.js 第 65 行每格 Math.round，0–2 的滑桿只會跳整數）。
- 讀數四行（第 109–112 行）：「E_J/E_C = 50.0　（E_C/h = 250 MHz, E_J/h = 12.50 GHz）」「ω₀₁/2π = 4.735 GHz　ω₁₂/2π = 4.448 GHz」「非諧性 α/2π = -287 MHz （≈ −E_C = −250 MHz）」
  「近似公式 √(8E_JE_C) − E_C = 4.750 GHz」；LC 模式第三行括號改為「（等間距 → 無法單獨定址）」（第 111 行）。
- 金色躍遷頻率標籤（第 18、96–105 行，class 'gold small'）放在 x = 5.9、兩能階中點高度，文字「ω01/2π = x.xx GHz」（toFixed(2)）。
- 以頁面同一條電荷基底哈密頓量（core.js 第 205–213 行 U.transmon，N = 14；第 59–61 行 E = 本徵值 + E_J）用 numpy 實算（transmon_card.py 的 Sturm 二分法結果相同）：
  比值 50：f₀₁ 4.735480、f₁₂ 4.448174、f₂₃ 4.127164 GHz → 讀數 4.735／4.448、α −287（−287.31）、近似 4.750、E_J/h 12.50；標籤 4.74、4.45、4.13。
  比值 100（滑桿值 2）：f₀₁ 6.811284、f₁₂ 6.537410 → 讀數 6.811／6.537、α −274（−273.87）、近似 6.821、E_J/h 25.00、「E_J/E_C = 100.0」。
  LC 模式比值 50（第 51–57 行）：ω = √(8·12.5·0.25) = 5 → 能階 2.5、7.5、12.5…（浮點數剛好整除），三個標籤都是「5.00 GHz」，α = 0 → 讀數「0 MHz」。
- 標籤投影（相機 pos [0, 2.8, 12.5]、target [0, 2.6, 0]、fov 45、面板右移 180 px，1600×900；第 9 行、core.js 第 233–236 行）：
  比值 50 金色標籤中心 (1492, 582)、(1492, 493)、(1493, 410)，由下往上依序是 ω01、ω12、ω23；LC 模式 (1492, 578)、(1492, 481)、(1493, 384)。
  右下小圖 #inset-wrap 約佔 x 1184–1584、y 620–884（css/style.css 第 56–59 行），比值 50／LC 的標籤都在它上方；比值 100 時 ω01 標籤中心降到 y 609，
  下緣會被小圖蓋住，所以第 1 段在比值 100 時只念面板讀數，不念金色標籤。
- 主畫面縱軸比例 ys = 5.6 / max(2E_J, 6E_C)（第 30–31 行）隨比值改變：比值 50 → 100 時能階在畫面上反而往下移、擠在一起，所以第 1 段不描述能階線怎麼移動。

transmon-3d.html#capacitor（第 4381–4384 行：#capacitor → 第 1 章且 capView = true；go() → bindChapter(0)，第 1033–1046 行 → setCapView(true)、fillCap()）：
- 載入時的初始狀態：capC = 77.5（第 1015 行）；E_J/h 固定 15 GHz（capStats 第 360–364 行）；讀數（第 888 行）電容 #r1C、充電能 #r1EC、E_J/E_C #r1ratio、f₀₁ #r1f、非諧性 α #r1a、電荷色散 #r1d、判斷 #r1v。
- 滑桿 #c1C min 5、max 200、step 0.5（第 887 行）；cs1.oninput → capC → fillCap（第 1040 行），所以用 ('js', …) 設值並觸發 input（同 q025.py／q028.py 的 _cap）。
- fillCap（第 1197–1208 行）、fmtF（第 365–371 行），以同一段程式（transmonLevels N = 25，n_g = 0 與 0.5 平均）用 numpy 實算：
  77.5 fF → 「77.5 fF」「250 MHz」「60.0」「5.21 GHz」「−283 MHz」「1.9 kHz」「transmon 區間」（Q025 查核畫格已逐項核對）；
  85 fF → 「85.0 fF」「228 MHz」「65.8」「4.99 GHz」（4.990157）「−256 MHz」（−256.12）「684.6 Hz」「transmon 區間」（比值 ≤ 120，第 1206 行，判斷文字不變）。
- 十字板粗細 sGoal = clamp(C/77.5, 0.3, 1.8)（第 4168 行）：85 fF 只粗 1.10 倍，變化很小，旁白不提。

1. tune（after=4，第 4 頁「數字一：頻率」之後）：#potential 比值 50 讀數（E_C 250 MHz、f₀₁ 4.735）→ 滑桿 1.75…2.00 拉到 100 → 讀數 E_J 25、f₀₁ 6.811（高了 2.08 GHz）→ α −287 → −274 幾乎不變 → 解讀（不描述畫面）。
2. ladder（after=5，第 5 頁「數字二：非諧性」之後）：#potential 按「LC」→ 拋物線、三個金色標籤都是 5.00 GHz → 讀數 α 0、等間距（讀數括號原文「無法單獨定址」，本課沒用過「定址」，旁白改說本課第 5 頁的「沒辦法只挑出其中兩階」「每一格一起共振」） → 按「JJ」→ 4.74、4.45、4.13 → α −287、約等於負的充電能量。
3. designer（after=7，第 7 頁「範例卡」之後）：#capacitor 77.5 fF（5.21 GHz，和範例卡一樣）→ 滑桿拉到 85 fF（4.99 GHz、比值 65.8）→ α −256、色散 684.6 Hz（說「不到一千赫茲」）、判斷不變 → 解讀。
- 用詞與本課 36 句一致：「能階場景」「比值」「約瑟夫森能量」「充電能量」「非諧性」「電荷色散」「參數設計器」「大十字電容的分頁」「範例卡」「典型範圍」。
  按鈕字面是英文開頭：「LC 諧振子（線性）」旁白說「第一排最左邊、寫著諧振子的按鈕」；「JJ / Transmon（非線性）」說「諧振子旁邊的按鈕」。
- 動作時間依實測語速（約每秒 5.2 字＋每句 0.5 秒停頓）以「該詞前的字數 ÷ 5.2」再提前約 0.5 秒排定：
  tune 第 2 句「一路拉到」約 1.2 秒、「現在讀數」約 3.3 秒 → 滑桿 0.7–1.95 秒走完；ladder 第 1 句「寫著諧振子」約 3.6 秒、「按鈕」約 4.2 秒 → 3.6 秒按 LC；第 3 句「按鈕」約 1.5 秒 → 0.9 秒按 JJ；
  designer 第 2 句「把電容」約 1.7 秒、「拉到八十五」約 3.3 秒 → 1.4–2.6 秒拉完。所有描述數字的句子都用「現在／是」而不用「變成」，因為說到時變化已經結束。
"""

LESSON = 'Q032'

_PANEL = "document.getElementById('panel').scrollTop=1e5;"
_POT = 'JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon'
_CAP = 'Transmon 3D 第 1 章：大十字電容的作用（C_Σ 滑桿與讀數）'
_R = 'E_J / E_C'


def _cap(v):
    """把 transmon-3d 第 1 章的 C_Σ 滑桿設成 v，觸發 input 讓讀數更新，並對滑桿那一列加黃框。"""
    return (f"(function(){{var r=document.getElementById('c1C');r.value={v};r.dispatchEvent(new Event('input'));"
            f"if(window.__flash)window.__flash(r.closest('label'));}})();")


_LIST = [
 dict(key='tune', after=4, page='jj', hash='potential', scene=_POT + '（E_J / E_C 滑桿與讀數）',
      title='動畫展示：拉比值，看頻率怎麼走', sub='三維動畫：能階場景——充電能量固定，只改約瑟夫森能量',
      sentences=[
       '打開約瑟夫森接面動畫的能階場景，現在停在比值五十；左邊面板的讀數寫著，充電能量是兩百五十兆赫，零到一的頻率是四點七三五吉赫。',
       '把比值的滑桿一路拉到最右邊的一百：現在讀數裡的約瑟夫森能量是二十五吉赫，零到一的頻率是六點八一一吉赫，比開頭高了兩吉赫多。',
       '再看非諧性：開頭是負兩百八十七兆赫，現在讀數是負兩百七十四兆赫，幾乎沒動。',
       '這個場景的充電能量固定不動，所以拉比值就是只改約瑟夫森能量：頻率跟著它走，非諧性主要看充電能量。'],
      actions=[(0, 0.1, ('js', _PANEL)),
               (1, 0.7, ('slider', _R, 1.75)), (1, 0.95, ('slider', _R, 1.8)), (1, 1.2, ('slider', _R, 1.85)),
               (1, 1.45, ('slider', _R, 1.9)), (1, 1.7, ('slider', _R, 1.95)), (1, 1.95, ('slider', _R, 2))],
      points=[('比值五十', 'f₀₁ = 4.735 GHz'), ('拉到一百', 'f₀₁ = 6.811 GHz'), ('非諧性', '−287 → −274 MHz')],
      pmap=[0, 1, 2, 2], shot=(1, 6.0)),
 dict(key='ladder', after=5, page='jj', hash='potential', scene=_POT + '（LC 與 JJ 對照）',
      title='動畫展示：等間距和不等距', sub='三維動畫：能階場景——諧振子與約瑟夫森接面',
      sentences=[
       '重新打開能階場景，按下第一排最左邊、寫著諧振子的按鈕：位能換成拋物線，右邊三個金色標籤都寫著五點零零吉赫。',
       '面板讀數的非諧性是零，括號寫著等間距；也就是說，沒辦法只挑出其中兩階，微波一打，每一格都會一起共振。',
       '再按諧振子旁邊的按鈕，換回約瑟夫森接面的餘弦形位能：金色標籤從下往上是四點七四、四點四五、四點一三，一格比一格小。',
       '讀數的非諧性現在是負兩百八十七兆赫，括號寫著約等於負的充電能量；正是這兩百多兆赫的差距，讓微波能只挑零和一。'],
      actions=[(0, 0.1, ('js', _PANEL)), (0, 3.6, ('click', 'LC')), (2, 0.9, ('click', 'JJ'))],
      points=[('諧振子', '三格都是 5.00 GHz'), ('讀數 α = 0', '等間距，每一格一起共振'), ('換回接面', '4.74、4.45、4.13 GHz')],
      pmap=[0, 1, 2, 2], shot=(2, 6.5)),
 dict(key='designer', after=7, page='tr', hash='capacitor', scene=_CAP,
      title='動畫展示：用參數設計器對準五吉赫', sub='三維動畫：Transmon 第 1 章——大十字電容的分頁',
      sentences=[
       '換到超導量子位元的另一個三維動畫，打開大十字電容的分頁，它就像一個參數設計器：面板寫著七十七點五飛法拉，頻率五點二一吉赫，和剛才的範例卡一樣。',
       '假設目標是五吉赫：把電容的滑桿往右拉到八十五飛法拉，現在頻率是四點九九吉赫，比值是六十五點八。',
       '非諧性是負兩百五十六兆赫，電荷色散不到一千赫茲，判斷那一行沒有變，還是同一個區間。',
       '三個數字都還在典型範圍裡，這就是一組可以寫上卡的設計；代價是非諧性比範例卡小了一些。'],
      actions=[(0, 0.1, ('js', _PANEL))] + [(1, round(1.4 + 0.2 * k, 2), ('js', _cap(v))) for k, v in enumerate([79, 80, 81, 82, 83, 84, 85])],
      points=[('77.5 fF', '5.21 GHz，同範例卡'), ('拉到 85 fF', 'f₀₁ = 4.99 GHz'), ('α = −256 MHz', '電荷色散不到 1 kHz')],
      pmap=[0, 1, 2, 2], shot=(2, 3.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q032'] 取用。"""

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)

    def get(self, k, default=None):
        return list(self) if k == LESSON else default

    def keys(self):
        return [LESSON]

    def values(self):
        return [list(self)]

    def items(self):
        return [(LESSON, list(self))]


DEMOS = _Demos(_LIST)

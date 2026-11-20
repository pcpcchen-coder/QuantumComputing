"""Q028 量子位元家族圖鑑 — v2 動畫展示段（格式見 ../demos.py 的說明）。

課綱沒有指定 3D 場景（「沿用 3D 場景」為空，只有簡報 JJ_Microwave_Readout_Talk p18–20）；本課挑三個和四種量子位元直接相關、而且前幾課已用過的控制項：
電荷型與大電容型用 index.html#potential（簡報 p19 備註「切換到 3D 場景 4」）、相位型用 index.html#washboard（簡報 p16 備註「早期的相位量子位元」）、
「沒有全能冠軍」用 transmon-3d.html#capacitor（電容拉小時判斷文字「電荷雜訊主導（接近 Cooper pair box）」）。超電感型沒有對應的動畫，只在投影片介紹。
每段都是新開頁面（record_demo.js 第 14–19 行），從頁面預設狀態開始；三段開頭都把 #panel 捲到底，旁白不提捲動。用詞和本課 36 句一致：
電荷型、大電容型、相位型（第 3 頁的小名）、背景電荷、電荷色散（第 4 頁）、偏壓電流、相位粒子、山谷、位障（第 7 頁）、山谷裡的振動頻率（第 7 頁）。

1. charge（after=5）index.html#potential：js/scenes/04_potential.js（App.register id 'potential'，第 3 行；index.html 第 43 行載入；#controls 在 #panel 內，index.html 第 26–31 行）。
   載入時的初始狀態：ratio = 50、mode = 'transmon'（第 13 行）；滑桿「E_J / E_C（對數刻度）」顯示 50.0（第 115 行）；下排 radio「CPB：E_J/E_C = 1」「10」「Transmon：50」，
   initial 50 → 「Transmon：50」為 on（第 116 行；core.js 第 345–352 行）。按下 → rs.set(log10 v) → ratio = v → rebuild（第 115–116 行），右下小圖每畫格重畫，按下後下一畫格就換。
   record_demo.js 'click' 以 '#controls button' 的 textContent.trim().startsWith 比對（第 26 行）：'CPB'、'Transmon' 各只對到一顆（第一排是「JJ / Transmon（非線性）」，開頭是 'JJ'）。
   右下小圖（第 118–129 行；index.html 第 35 行 #inset-wrap）：標題「電荷色散：能階隨背景電荷 n_g 的變化」，橫軸「背景電荷 n_g」−1～1，縱軸 (E − E₀)/E₀₁ 範圍 −0.2～2.6（超出截在邊上，第 122、126 行），
   三條線藍 #4f8cff、紅 #ff5a5f、綠 #2ecc71（第 124 行）= rebuild 時以 U.transmon 算的最低三個能階（第 69–74 行）。
   以頁面同一段程式在 Node 實算（與 q025.py 第 1 段、fact_check_v2_q011_q040.md Q025 節的畫格一致）：比值 50 三條都是平線；比值 1 藍 0～0.595 波浪、紅 1.595～4.117（頂端截在上緣）、綠整條貼上緣。
   所以旁白只說藍線和紅線起伏，不說綠線；不念面板讀數（非諧性讀數只取 n_g = 0，比值 1 時 ω₁₂ 只有 0.03 GHz，容易誤導）。
   CPB 在第 2 句 2.4 秒按（「按鈕」約在 2.3–3.1 秒），Transmon 在第 4 句 0.7 秒按（「五十的按鈕」約在 1.0–1.9 秒）。按 Transmon 後滑桿顯示 50.1（step 0.01），旁白不念。
2. phase（after=7）index.html#washboard：js/scenes/05_washboard.js（id 'washboard'，第 3 行；index.html 第 44 行）。
   載入時的初始狀態：iB = 0.3、Q = 8、phi = 0、follow = true（第 15 行）；小球在 asin 0.3 附近振盪，阻尼 v/Q（第 95–99 行），jj 頁 settle 4 秒後振幅很小、看起來停在谷底（q026.py 說明同）。
   滑桿「偏壓電流 I / Ic（傾斜）」0–1.6、step 0.01、toFixed(2)（第 64 行，oninput → iB、buildSurface）；'slider' 用 __sl（textContent.includes，record_demo.js 第 27 行）→ '偏壓電流' 只對到這一根。
   不用 'sweep'（record_demo.js 第 64 行每格 Math.round，0–1.6 的滑桿只會跳整數）。
   位障標籤（teal small，第 22、56–60 行）：每 0.25 秒（第 114 行）放在小球所在井右側位障頂（pmax）上方，文字「位障 ΔU ≈ x.xx E_J」；
   Node 以第 17、45–47 行實算：0.30 → 1.15、0.50 → 0.68、0.70 → 0.31、0.85 → 0.11、0.90 → 0.06。
   讀數第一行（第 115–116 行）：|vAvg| ≤ 0.08 時「零電壓態：相位被困在井中做電漿振盪」；第二行（第 117 行）「ω_p(I) = ω_p0 (1 − (I/Ic)²)^{1/4} = x.xx ω_p0」：0.30 → 0.98、0.90 → 0.66。
   第 2 句從 0.6 秒起每 0.68 秒加 0.05（0.35 → 0.90，第 8.08 秒到 0.90，標籤最晚 8.33 秒顯示 0.06；「最後停在零點零六」約在 8.1–9.4 秒）。
   每格平衡點最多移 0.104 rad（0.85 → 0.90），換算多出的能量約 0.002 E_J，遠小於 0.06 的位障；q026.py 以同樣每格 0.05、間隔 0.74 秒模擬 300 次都沒有滑出，本段間隔 0.68 秒相近。
   第 3 句說「已經從一開始的零點九八倍降到零點六六倍」：數字在第 2 句就變完，用「已經」。「山谷裡的振動頻率」= 讀數第二行的 ω_p（場景說明稱電漿頻率），本課第 7 頁第 2 句用同一說法。
3. tradeoff（after=8）transmon-3d.html#capacitor：第 4381–4384 行 #capacitor → 第 1 章且 capView = true；go() → bindChapter(0)（第 1033–1046 行）→ setCapView(true)、fillCap()。
   載入時的初始狀態：capC = 77.5（第 1015 行）；分頁內容第 879–890 行：滑桿 #c1C「C_Σ」5–200、step 0.5、value 77.5（第 887 行）；讀數（第 888 行）電容、充電能、E_J/E_C、f₀₁、非諧性 α、電荷色散、判斷；
   按鈕 #c1reset「回到 77.5 fF」（第 889 行，第 1041 行 onclick → capC = 77.5、fillCap）。cs1.oninput → fillCap（第 1040 行），所以 ('js', …) 設值後觸發 input（同 q025.py）。
   fillCap 第 1197–1208 行、capStats 第 360–364 行；Node 實算（與 q025.py、fact_check_v2_q011_q040.md Q025 節畫格一致）：
   77.5 fF → 250 MHz、60.0、5.21 GHz、−283 MHz、1.9 kHz、transmon 區間；20 fF → 969 MHz、15.5、9.69 GHz、−1.33 GHz、53.1 MHz、「電荷雜訊主導（接近 Cooper pair box）」（銅色）。
   −1.33 GHz ÷ −283 MHz ≈ 4.7 倍 →「大了好幾倍」。十字板粗細 sGoal = clamp(capC / 77.5, 0.3, 1.8)（第 4166–4174 行），約 0.3 秒趨近；C ≤ 23.25 fF 到下限 0.3。
   第 2 句從 0.4 秒起每 0.3 秒一格拉到 20（2.5 秒到位；q025 實測同類拉法約早 0.6 秒），「十字板變細」約在 2.3–3.3 秒。第 4 句 0.2 秒按「回到 77.5 fF」（「回到七十七點五的按鈕」約在 0.4–2.2 秒）。
"""

LESSON = 'Q028'

_PANEL = "document.getElementById('panel').scrollTop=1e5;"
_POT = 'JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon（電荷色散小圖）'
_WB = 'JJ 與微波讀取 3D 場景 5：RCSJ 模型——傾斜洗衣板位勢'
_CAP = 'Transmon 3D 第 1 章：大十字電容的作用（C_Σ 滑桿與讀數）'
_I = '偏壓電流'


def _ramp(si, t0, dt, values):
    return [(si, round(t0 + k * dt, 2), ('slider', _I, v)) for k, v in enumerate(values)]


def _cap(v):
    """把 transmon-3d 第 1 章的 C_Σ 滑桿設成 v，觸發 input 讓讀數更新，並對滑桿那一列加黃框。"""
    return (f"(function(){{var r=document.getElementById('c1C');r.value={v};r.dispatchEvent(new Event('input'));"
            f"if(window.__flash)window.__flash(r.closest('label'));}})();")


def _sweep(si, t0, dt, values):
    return [(si, round(t0 + k * dt, 2), ('js', _cap(v))) for k, v in enumerate(values)]


_LIST = [
 dict(key='charge', after=5, page='jj', hash='potential', scene=_POT,
      title='動畫展示：電荷型和大電容型差在哪', sub='三維動畫：能階與非諧性——右下角的電荷色散小圖',
      sentences=[
       '打開約瑟夫森接面動畫的能階場景，左邊面板現在停在比值五十，也就是大電容型；右下角小圖的藍、紅、綠三條線，是最低的三個能階，現在都是平的。',
       '按下下排最左邊、寫著等於一的按鈕，換成電荷型的比值：小圖裡的藍線和紅線變成了上下起伏的波浪。',
       '小圖的橫軸是背景電荷，基板裡的電荷一跳，能階就跟著上下動；這就是電荷型怕背景電荷、電荷色散很大的原因。',
       '最後按寫著五十的按鈕，回到大電容型的比值，三條線又都是平的；同一條能量公式，只差一個比值，怕不怕背景電荷就差這麼多。'],
      actions=[(0, 0.1, ('js', _PANEL)), (1, 1.9, ('click', 'CPB')), (3, 0.7, ('click', 'Transmon'))],
      points=[('比值五十，大電容型', '三條線都是平的'), ('比值一，電荷型', '藍線紅線上下起伏'), ('回到比值五十', '三條線又拉平了')],
      pmap=[0, 1, 1, 2], shot=(1, 6.0)),
 dict(key='phase', after=7, page='jj', hash='washboard', scene=_WB,
      title='動畫展示：相位型用的山谷', sub='三維動畫：洗衣板位勢——把偏壓電流加到接近臨界電流',
      sentences=[
       '打開約瑟夫森接面動畫的洗衣板場景：金色小球是相位粒子，停在一個山谷的底部；左邊面板的偏壓電流是零點三零，小球右邊的位障標著一點一五。',
       '把偏壓電流一格一格加到零點九零：洗衣板越來越斜，山谷越來越淺，位障的數字一路往下掉，最後停在零點零六。',
       '小球還是留在山谷裡，讀數仍寫著零電壓態；讀數下面那行算的山谷振動頻率，已經從一開始的零點九八倍降到零點六六倍。',
       '這就是相位型的兩面：轉一下電流就能調頻率，可是電流只要一抖，頻率也跟著抖。'],
      actions=[(0, 0.1, ('js', _PANEL))] + _ramp(1, 0.1, 0.66, [0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]),
      points=[('偏壓電流零點三零', '位障一點一五'), ('加到零點九零', '位障降到零點零六'), ('振動頻率跟著變', '可調，也怕電流抖')],
      pmap=[0, 1, 2, 2], shot=(1, 9.5)),
 dict(key='tradeoff', after=8, page='tr', hash='capacitor', scene=_CAP,
      title='動畫展示：顧了這頭，顧不了那頭', sub='三維動畫：Transmon 第 1 章——把大電容拉小',
      sentences=[
       '換到超導量子位元的另一個三維動畫，打開大十字電容的分頁：中間的十字金屬板就是並聯的大電容，面板寫著七十七點五飛法拉，比值六十，非諧性負兩百八十三兆赫。',
       '把滑桿往左拉到二十飛法拉：十字板變細，比值掉到十五點五，非諧性變成負一點三三吉赫，大了好幾倍。',
       '可是電荷色散已經是五十三點一兆赫，原本只有一點九千赫；判斷那一行寫著電荷雜訊主導，比值太小，就往電荷型靠過去了。',
       '按下回到七十七點五的按鈕，數字回到原來的樣子；非諧性和電荷色散互相拉扯，就算是同一種設計，也要在兩者之間取捨。'],
      actions=[(0, 0.1, ('js', _PANEL))] + _sweep(1, 0.4, 0.3, [70, 60, 50, 40, 35, 30, 25, 20]) + [(3, 0.2, ('id', 'c1reset'))],
      points=[('七十七點五飛法拉', '比值六十'), ('拉到二十飛法拉', '非諧性大了好幾倍'), ('電荷色散變大', '往電荷型靠過去')],
      pmap=[0, 1, 2, 2], shot=(1, 3.5)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q028'] 取用。"""

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

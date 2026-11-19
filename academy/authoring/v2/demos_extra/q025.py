"""Q025 E_J 與 E_C：兩個能量尺度 — v2 動畫展示段（格式見 ../demos.py 的說明）。

第 1 段用課綱「家長課前準備」指定的 index.html#potential（demos.PAGES['jj']），第 2、3 段用 transmon-3d.html#capacitor（demos.PAGES['tr']，
第 1 章「大十字電容的作用」分頁；課綱素材列的是 tr:potential，但第 3 章只比較有／沒有 JJ，沒有比值的滑桿；#capacitor 分頁才有 E_J/E_C、非諧性、電荷色散三個讀數）。
每段都是新開頁面，從頁面預設狀態開始。

1. dispersion（after=6）index.html#potential：js/scenes/04_potential.js（App.register id 'potential'，第 3 行；index.html 第 43 行載入；#controls 在 #panel 內）。
   載入時的初始狀態：mode = 'transmon'、ratio = 50（第 13 行），「Transmon：50」按鈕為 on（第 116 行 initial 50）。
   #controls 依序（core.js 第 339–370 行 ui.row／radio／slider／readout）：第一排 radio「LC 諧振子（線性）」「JJ / Transmon（非線性）」（第 114 行）、
   滑桿「E_J / E_C（對數刻度）」（第 115 行）、第二排（下排）radio「CPB：E_J/E_C = 1」「10」「Transmon：50」（第 116 行，按下 rs.set(log10 v) → ratio = v → rebuild）、讀數（第 109–112 行）。
   record_demo.js 'click' 以 textContent.trim().startsWith 比對（第 26 行）：'CPB'、'10'、'Transmon' 各只對到一顆（第一排是「JJ / Transmon」，開頭不同）。
   右下小圖（第 118–129 行，ctx.inset → #inset-wrap，core.js 第 372–375 行；css/style.css 第 56–59 行固定在右下、z-index 4）：標題「電荷色散：能階隨背景電荷 n_g 的變化」，
   橫軸「背景電荷 n_g」−1～1、縱軸 (E − E₀)/E₀₁、範圍 −0.2～2.6（超出就截在邊上，第 122、126 行），三條線依序藍 #4f8cff、紅 #ff5a5f、綠 #2ecc71（第 124 行）；
   bands 在 rebuild 時以 U.transmon(EJ, EC, ng, 10) 重算（第 69–74 行），每一畫格重畫（core.js 第 278 行），所以按下後下一畫格就換。
   以頁面同一段程式（core.js U.transmon + 第 69–74、120–126 行）在 Node 實算，各線在 n_g = −1～1 的最小～最大值（以 E₀₁ 為單位）：
   - 比值 50：藍 0.000～0.000、紅 1.000～1.000、綠 1.939～1.939 → 三條平的直線。
   - 比值 1：藍 0.000～0.595（波浪，高點在 n_g = ±0.5）、紅 1.595～4.117（超過 2.6 的部分截在上緣）、綠 4.239～9.171（整條截在上緣，看起來是貼著上緣的平線）→ 旁白只說藍線和紅線起伏。
   - 比值 10：藍 0.000～0.001、紅 1.001～1.033（在 190 px 高的圖上約 2 px）、綠 1.732～1.966（約 16 px 的起伏）→ 藍紅幾乎平、綠還有一點彎。
   讀數的非諧性只取 n_g = 0（第 97、108 行），比值 10 時顯示 −637 MHz，和投影片第 7 頁引用的 −353 MHz（transmon 簡報 p15 取兩點平均）定義不同，所以本段旁白不念讀數。
2. bigC（after=8）transmon-3d.html#capacitor：第 4381–4384 行 #capacitor → 第 1 章（id 'chip'）且 capView = true；go() → bindChapter(0)（第 1033–1046 行）→ setCapView(true) 與 fillCap()。
   分頁內容第 879–890 行：滑桿 #c1C「C_Σ」min 5、max 200、step 0.5、value 77.5（第 887 行），讀數 dl（第 888 行）依序 電容 C_Σ #r1C、充電能 E_C/h #r1EC、E_J/E_C #r1ratio、f₀₁ #r1f、
   非諧性 α #r1a、電荷色散 #r1d、判斷 #r1v；按鈕 #c1reset「回到 77.5 fF」（第 889 行）。cs1.oninput → capC → fillCap（第 1040 行），所以 ('js', …) 設值後要觸發 input。
   fillCap 第 1197–1208 行；capStats 第 360–364 行（E_J/h 固定 15 GHz、E_C/h = 19.37 / C[fF]、transmonLevels 第 347–358 行在 n_g = 0 與 0.5 求能階，α 取兩點平均、電荷色散 = |f₀₁(0) − f₀₁(0.5)|）；
   fmtF 第 365–371 行；判斷：比值 < 20「電荷雜訊主導（接近 Cooper pair box）」（copper）、≤ 120「transmon 區間」（teal）、其餘「非諧性偏小，閘需放慢」（gold）。
   以同一段程式在 Node 實算的讀數：77.5 fF → 250 MHz、60.0、5.21 GHz、−283 MHz、1.9 kHz、transmon 區間；
   200 fF → 96.8 MHz、154.9、3.31 GHz、−104 MHz、< 0.1 Hz、非諧性偏小，閘需放慢（155 fF 時比值 120.03，已越過 120）。
   十字板粗細：第 4166–4174 行 sGoal = clamp(capC / 77.5, 0.3, 1.8)，以每秒 8 的指數速率趨近（約 0.3 秒到位）；200 fF → 1.8 倍（C ≥ 139.5 fF 就到上限）。
   滑桿從 1.0 秒起每 0.2 秒一格拉到 200（3.2 秒到位），旁白說「十字板變粗」時已到上限。
3. compromise（after=10）同一分頁，新開頁面（capC 又是 77.5，第 1015 行）。往左拉到 20 fF：969 MHz、15.5、9.69 GHz、−1.33 GHz、53.1 MHz、電荷雜訊主導（接近 Cooper pair box）；
   十字板 20 / 77.5 = 0.26 → 下限 0.3 倍。再用 ('id', 'c1reset') 按「回到 77.5 fF」（第 1041 行）回到 77.5 fF 的讀數。
- 第 1 段開頭先把 #panel 捲到底（index.html 的面板可捲動，css/style.css 第 32 行），讓下排按鈕入鏡；transmon-3d.html 的 .panel（第 45–53 行，max-height 100% − 160px、overflow-y auto）
  也用同一句捲到底，讓滑桿、讀數與「回到 77.5 fF」按鈕同時入鏡；旁白不提捲動。
- 第 2、3 段的滑桿用 ('js', …) 設定 #c1C 並觸發 input（record_demo.js 的 'slider'／'sweep' 只找 #controls .slider，transmon-3d 沒有這種元素）。
"""

LESSON = 'Q025'

_PANEL = "document.getElementById('panel').scrollTop=1e5;"
_POT = 'JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon（電荷色散小圖）'
_CAP = 'Transmon 3D 第 1 章：大十字電容的作用（C_Σ 滑桿與讀數）'


def _cap(v):
    """把 transmon-3d 第 1 章的 C_Σ 滑桿設成 v，觸發 input 讓讀數更新，並對滑桿那一列加黃框。"""
    return (f"(function(){{var r=document.getElementById('c1C');r.value={v};r.dispatchEvent(new Event('input'));"
            f"if(window.__flash)window.__flash(r.closest('label'));}})();")


def _sweep(si, t0, dt, values):
    return [(si, round(t0 + k * dt, 2), ('js', _cap(v))) for k, v in enumerate(values)]


_LIST = [
 dict(key='dispersion', after=6, page='jj', hash='potential', scene=_POT,
      title='動畫展示：背景電荷一變，能階跟著動', sub='三維動畫：能階與非諧性——右下角的電荷色散小圖',
      sentences=[
       '打開約瑟夫森接面動畫的能階場景，現在停在比值五十；右下角小圖畫的是能階隨背景電荷的變化，藍、紅、綠三條線都是平的。',
       '按下下排最左邊、寫著等於一的按鈕，把比值調成一：小圖裡的藍線和紅線變成上下起伏的波浪，背景電荷一變，能階就跟著動。',
       '再按旁邊寫著十的按鈕：藍線和紅線幾乎拉平了，最上面的綠線還看得出一點彎；比值才加到十，起伏就小了一大截。',
       '最後按寫著五十的按鈕回到開頭，三條線又都是平的；比值越大，背景電荷怎麼跳，能階都幾乎不動，這就是電荷色散被壓下來。'],
      actions=[(0, 0.1, ('js', _PANEL)), (1, 2.8, ('click', 'CPB')), (2, 1.5, ('click', '10')), (3, 1.4, ('click', 'Transmon'))],
      points=[('比值五十', '三條線都是平的'), ('比值一', '藍線紅線上下起伏'), ('比值十', '起伏小了一大截')],
      pmap=[0, 1, 2, 0], shot=(1, 6.5)),
 dict(key='bigC', after=8, page='tr', hash='capacitor', scene=_CAP,
      title='動畫展示：電容加大，非諧性變小', sub='三維動畫：Transmon 第 1 章——大十字電容的作用',
      sentences=[
       '換到超導量子位元的另一個三維動畫，打開大十字電容的分頁：中間的十字金屬板就是並聯的大電容，面板寫著電容七十七點五飛法拉，比值六十。',
       '把電容的滑桿往右拉到兩百，十字板變粗，充電能量變小，比值變成一百五十四點九。',
       '電荷色散那一行變成小於零點一赫茲，幾乎不受背景電荷影響；可是非諧性也從負兩百八十三，縮小到負一百零四兆赫。',
       '判斷那一行寫著：非諧性偏小，閘需放慢；因為一到二的頻率太靠近零到一，脈衝一快，就會漏到更高的能階。'],
      actions=[(0, 0.1, ('js', _PANEL))] + _sweep(1, 1.0, 0.2, [90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]),
      points=[('電容七十七點五飛法拉', '比值六十'), ('拉到兩百飛法拉', '比值約一百五十五'), ('色散很小，非諧性也小', '閘需放慢')],
      pmap=[0, 1, 2, 2], shot=(2, 3.0)),
 dict(key='compromise', after=10, page='tr', hash='capacitor', scene=_CAP,
      title='動畫展示：找一個折衷點', sub='三維動畫：Transmon 第 1 章——電容太小與剛剛好',
      sentences=[
       '重新打開大十字電容的分頁，這次把滑桿往左拉到二十飛法拉，十字板變細，比值掉到十五點五。',
       '非諧性變成負一點三三吉赫，非常大；電荷色散卻有五十三點一兆赫，判斷那一行寫著電荷雜訊主導。',
       '最後按下回到七十七點五的按鈕：比值回到六十，非諧性負兩百八十三兆赫，電荷色散只有一點九千赫。',
       '兩百多兆赫的非諧性，足夠讓微波只挑零和一；不到兩千赫的電荷色散，影響已經很小，這就是兩個目標之間的折衷點。'],
      actions=[(0, 0.1, ('js', _PANEL))] + _sweep(0, 3.2, 0.3, [70, 60, 50, 40, 35, 30, 25, 20]) + [(2, 2.2, ('id', 'c1reset'))],
      points=[('拉到二十飛法拉', '比值十五點五'), ('非諧性很大', '電荷色散五十三兆赫'), ('回到七十七點五', '兩個目標的折衷點')],
      pmap=[0, 1, 2, 2], shot=(1, 3.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q025'] 取用。"""

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

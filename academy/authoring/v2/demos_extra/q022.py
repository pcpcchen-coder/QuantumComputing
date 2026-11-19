"""Q022 量子諧振子：等距的梯子 — v2 動畫展示段（格式見 ../demos.py 的說明）。

第 1 段用課綱「家長課前準備」指定的 index.html#potential（demos.PAGES['jj']），第 2、3 段用課綱素材 lc-vs-jj.html（demos.PAGES['lc'] 的 #s4、#s3）。
transmon.pptx p14 講者備註把 #s3 稱為「圖解：能階間距」、#s4 稱為「圖解：只停在 |0⟩|1⟩」。

1. ladder（after=4）index.html#potential：js/scenes/04_potential.js（App.register id 'potential'，第 3 行；index.html 第 43 行載入；#controls 在 #panel 內）。
   載入時的初始狀態：mode = 'transmon'、ratio = 50（第 13 行），畫面是餘弦山谷；所以先按 LC 才看得到拋物線。
   #controls 依序：radio「LC 諧振子（線性）」「JJ / Transmon（非線性）」（第 114 行，第一個按鈕即 LC）、滑桿「E_J / E_C（對數刻度）」（第 115 行）、
   radio「CPB：E_J/E_C = 1」「10」「Transmon：50」（第 116 行，按下呼叫 rs.set → 滑桿 upd → ratio = 10^v → rebuild，core.js 第 359–368 行）、讀數（第 109–112 行）。
   LC：U = E_J φ²/2（第 32 行）、E_n = √(8E_JE_C)(n + ½)（第 52–55 行）；E_C = 0.25、ratio 50 → E_J = 12.5 → 間距 5.000 GHz。
   能階線畫 min(5, shown) 條（第 77–91 行），左邊標籤 |0⟩–|3⟩ 只有 4 個（第 17、92–95 行，x = −5.6）；右邊金色標籤（'gold small'，x = 5.9，第 18、98–105 行）
   「ω01/2π = 5.00 GHz」三個；讀數「非諧性 α/2π = 0 MHz （等間距 → 無法單獨定址）」（第 108–111 行）。這兩個標籤在 transmon 模式也一直在（只是數字不同），旁白用「標著」不說「出現」。
   按「10」（LC 模式下）：E_J = 2.5 → 間距 2.236 GHz；Etop = 5、ys = 1.12，能階高度 1.25、3.76、6.26（< 6.3）→ shown = 3：三條能階、標籤 |0⟩|1⟩|2⟩、
   金色標籤兩個「2.24 GHz」，非諧性讀數「0 MHz」（以同一段程式在 Node 實算，不是 −0；按 CPB = 1 會顯示「−0」，所以不用）。
   E_J 在 LC 模式等於電感能量 (Φ₀/2π)²/L，E_J 變小 = 電感變大，所以旁白說「等於把電感換大」。
2. climb（after=6）lc-vs-jj.html#s4：第 246–260 行 section #s4「第 4 步 · 用微波去驅動／能不能只停在 |0⟩ 和 |1⟩？」，說明文字「每條直線代表一個躍遷 |n⟩→|n+1⟩ 的頻率，
   陰影帶是頻率對準 ω₀₁ 的驅動微波」。draw4（第 498–529 行，滑桿預設 50）：LC 列只有一條 class 'hit'（綠 --hit #2C8A55，第 98 行）的線與藍色陰影帶，
   陰影帶第 514 行、綠線第 515 行，文字「0→1 = 1→2 = 2→3 = 3→4 全部重疊」（綠字 t-hit，第 516 行）與下一行「驅動一路往上爬」（第 517 行）；Transmon 列有陰影帶「驅動 @ ω₀₁」（第 519–521 行）與四條線
   4.74、4.45、4.13、3.70 GHz，只有 |f − drive| < 0.02 的 0→1 是 'hit' 綠色，其他三條 'miss' 灰（--miss #A3B0AC，第 99 行；第 522–528 行，判斷在第 523 行）。
   本段沒有控制項要操作，只在開頭 scrollIntoView。
3. uneven（after=8）lc-vs-jj.html#s3：第 214–243 行 section #s3「第 3 步 · 位能與量子能階／拋物線的能階等間距，餘弦的不是」；左圖 #fig3a「LC：U = E_J φ²/2」藍（--lc #1D6A8B）、
   右圖 #fig3b「Transmon：U = E_J(1 − cos φ)」橘（--jj #B65C12），.twin 兩欄並排（第 69 行；寬度 ≤ 760px 才改單欄）。
   draw3（第 484–497 行）、drawWell 右側間距標籤（第 475–482 行，只標到不超過 ymax = 4.9·wp 的能階）。滑桿 #ratio（第 233 行，10–120、預設 50），input 事件重畫（第 530 行）。
   以頁面同一段程式在 Node 實算：50 → 左 5.00 ×4、右 4.74、4.45、4.13、3.70、3.50，r3c「−287 MHz」；80 → 左 6.32 ×4、右 6.06、5.79、5.48、5.15、4.78，r3c「−277 MHz」；
   50 時井頂虛線（2E_J = 25 > ymax 24.5）不畫，旁白不提。
- 第 1 段開頭先把 #panel 捲到底（面板可捲動，css/style.css 第 32 行），讓按鈕與讀數入鏡；lc-vs-jj.html 沒有 #controls，第 3 段用 ('js', …) 設定原生滑桿並觸發 input（同 q021.py）。
- 版面估計（1600×900）：#s3、#s4 各自的標題、圖與讀數都在一個畫面內（main 最寬 1040px）；待試錄確認。
"""

LESSON = 'Q022'

_PANEL = "document.getElementById('panel').scrollTop=1e5;"


def _set(el, v):
    """把 lc-vs-jj.html 的原生滑桿設成 v，觸發 input 讓圖重畫，並對滑桿那一列加黃框。"""
    return (f"(function(){{var r=document.getElementById('{el}');r.value={v};r.dispatchEvent(new Event('input'));"
            f"if(window.__flash)window.__flash(r.closest('.control'));}})();")


def _top(sec):
    return f"document.getElementById('{sec}').scrollIntoView({{block:'start'}});"


_LIST = [
 dict(key='ladder', after=4, page='jj', hash='potential', scene='JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon',
      title='動畫展示：梯子每一階一樣高', sub='三維動畫：能階與非諧性——線性諧振子的等距能階',
      sentences=[
       '打開約瑟夫森接面動畫的能階場景，先按第一個、寫著線性諧振子的按鈕，畫面換成一條拋物線形的山谷，裡面架著一階一階的能階。',
       '左邊從下往上標著零、一、二、三，右邊金色的數字是相鄰兩階的間距：五點零零、五點零零、五點零零，三個完全一樣。',
       '面板下方的讀數寫著：非諧性是零兆赫，意思是間距之間沒有差別，括號裡還寫著等間距、無法單獨定址。',
       '再按寫著十的按鈕，等於把電感換大：金色數字一起變成二點二四吉赫，梯子只看得到三階，兩個間距還是一樣，非諧性仍然是零。'],
      actions=[(0, 0.1, ('js', _PANEL)), (0, 5.6, ('click', 'LC 諧振子')), (3, 0.5, ('click', '10'))],
      points=[('線性諧振子', '拋物線山谷'), ('三個間距', '都是五點零零吉赫'), ('換大電感', '間距變小，仍然等距')],
      pmap=[0, 1, 1, 2], shot=(1, 7.0)),
 dict(key='climb', after=6, page='lc', hash='s4', scene='LC 與約瑟夫森接面 圖解第 4 步：用微波去驅動——能不能只停在 |0⟩ 和 |1⟩？',
      title='動畫展示：微波一路往上推', sub='互動圖解：LC 與約瑟夫森接面第 4 步（平面互動圖）',
      sentences=[
       '換到電感電容與約瑟夫森接面圖解的第四步：每一條直線代表往上跳一階需要的頻率，陰影帶是對準零到一的驅動微波。',
       '上面那一行是電感電容電路，只有一條綠色的線，旁邊寫著零到一、一到二、二到三、三到四，全部疊在一起。',
       '綠色字的下一行寫著：驅動一路往上爬；微波推完零到一，也正好推得動上面每一階。',
       '再看下面那一行，約瑟夫森接面做的量子位元：四條線分開了，只有零到一那條是綠色，其他三條是灰色，微波打不到。'],
      actions=[(0, 0.1, ('js', _top('s4')))],
      points=[('每一條直線', '往上跳一階的頻率'), ('電感電容', '四個跳躍同一個頻率'), ('約瑟夫森接面', '只打得到零到一')],
      shot=(1, 5.0)),
 dict(key='uneven', after=8, page='lc', hash='s3', scene='LC 與約瑟夫森接面 圖解第 3 步：拋物線的能階等間距，餘弦的不是',
      title='動畫展示：不等距的梯子', sub='互動圖解：LC 與約瑟夫森接面第 3 步（平面互動圖）',
      sentences=[
       '回到圖解的第三步，左右兩張圖並排：左邊藍色是電感電容的拋物線，右邊橘色是約瑟夫森接面的餘弦山谷。',
       '左邊梯子旁的四個數字都是五點零零；右邊的數字從四點七四、四點四五、四點一三，一路變小。',
       '下面的讀數寫著，非諧性是負兩百八十七兆赫：一到二比零到一少了這麼多，所以微波可以只挑零和一。',
       '把圖下面的滑桿從五十拉到八十，左邊四個數字一起變成六點三二，右邊還是一階比一階小，讀數變成負兩百七十七兆赫。'],
      actions=[(0, 0.1, ('js', _top('s3'))),
               (3, 1.0, ('js', _set('ratio', 55))), (3, 1.25, ('js', _set('ratio', 60))), (3, 1.5, ('js', _set('ratio', 65))),
               (3, 1.75, ('js', _set('ratio', 70))), (3, 2.0, ('js', _set('ratio', 75))), (3, 2.25, ('js', _set('ratio', 80)))],
      points=[('左右並排', '拋物線對上餘弦'), ('右邊梯子', '越往上越擠'), ('滑桿拉到八十', '左邊仍然等距')],
      pmap=[0, 1, 1, 2], shot=(1, 5.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q022'] 取用。"""

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

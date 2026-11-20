"""Q021 彈簧、單擺與 LC 電路 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都用課綱指定的 animations/lc-vs-jj.html（demos.PAGES['lc']），第 1 段 #s1、第 2、3 段 #s2。
這一頁不是 3D 場景，而是平面 SVG 互動圖解；沒有 #controls 也沒有 label.slider，所以 record_demo.js 的
('click'／'slider'／'sweep') 都找不到控制項，三段一律用 ('js', …) 直接設定原生 <input type=range> 的值並觸發 input 事件
（lc-vs-jj.html 第 398 行 phiIn、第 439 行 ampIn 都是 addEventListener('input', …)，所以畫面會立刻重畫）。
每次設定都對 .control（滑桿那一列）呼叫 record_demo.js 提供的 window.__flash 加黃框。

lc-vs-jj.html 對照（行號）：
- 第 154 行 <section class="step" id="s1">「第 1 步 · 本構關係／電流與磁通：直線 vs 正弦」；第 184 行 id="s2"「第 2 步 · 疊加原理測試／用正弦波去推，輸出長什麼樣？」。
  網址 hash 會讓瀏覽器捲到該 section；每段第一個動作再 scrollIntoView 一次，避免字型載入後位置跑掉。
- 顏色（第 13–15 行，淺色主題）：--lc #1D6A8B（藍）、--jj #B65C12（橘）；圖例第 167、197 行。
- 第 1 步：滑桿 #phi（第 170–171 行）min −4.71、max 4.71、預設 0.6；圖第 378–385 行：藍色直線 I = φ、橘色 sin φ、
  切線、藍圓點 (φ, φ)、橘圓點 (φ, sin φ)；讀數第 386–390 行 r1a = φ、r1b = sin φ（三位小數）；
  說明 #r1note 第 391–396 行：|φ| < 0.35 →「φ 很小：sin φ ≈ φ，JJ 跟普通電感幾乎一模一樣，這時它看起來是線性的。」
  φ = 0.2 → 0.200／0.199；φ = 1.0 → 1.000／0.841、說明換成「直線和正弦分開了……等效電感變大了 1.85 倍」。
- 第 2 步：滑桿 #amp（第 201–202 行）0.1–3、預設 1.4；上圖（第 406–414 行）兩個週期，藍 A·sin t、橘 sin(A·sin t)，±I_c 虛線（第 411 行）；
  下圖頻譜（第 416–431 行）1ω、3ω、5ω、7ω 各一對柱子，藍色只有 1ω = 100、其他為 0（第 425 行 lv = k===1 ? 100 : 0），
  橘色 = |J_k(A)| / |J_1(A)| × 100；讀數第 435–437 行：r2a 固定「2.00 倍」、r2b = sin(min(2A, π/2)) / sin(min(A, π/2))、r2c = 3ω/基頻。
  以頁面同一段程式在 Node 實算：A = 0.3 → 3ω 0.4 %、r2b 1.91 倍；A = 2.5 → 3ω 43.6 %（柱上標 44）、5ω 3.9、r2b 1.00 倍；
  A = 2.5 時橘色波形在 A·sin t = π/2 處碰到 +I_c，波峰正中間 sin(2.5) = 0.60，凹下去。
- 版面：main 最寬 1040px、.pair 5fr／7fr，1600×900 視窗下圖寬約 590px；第 1、2 步的圖、滑桿、讀數估計都在一個畫面內（待試錄確認）。
"""

LESSON = 'Q021'


def _set(el, v):
    """把 lc-vs-jj.html 的原生滑桿設成 v，觸發 input 讓圖重畫，並對滑桿那一列加黃框。"""
    return (f"(function(){{var r=document.getElementById('{el}');r.value={v};r.dispatchEvent(new Event('input'));"
            f"if(window.__flash)window.__flash(r.closest('.control'));}})();")


def _top(sec):
    return f"document.getElementById('{sec}').scrollIntoView({{block:'start'}});"


_LIST = [
 dict(key='smallangle', after=4, page='lc', hash='s1', scene='LC 與約瑟夫森接面 圖解第 1 步：電流與磁通——直線 vs 正弦',
      title='動畫展示：小角度時，正弦像直線', sub='互動圖解：LC 與約瑟夫森接面第 1 步（平面互動圖）',
      sentences=[
       '打開電感電容與約瑟夫森接面圖解的第一步：藍色直線是普通電感，電流和磁通成正比；橘色曲線是正弦，就像單擺的回復力。',
       '把相位滑桿往回拉到零點二，兩個圓點幾乎疊在一起，讀數是零點二和零點一九九。',
       '下面的說明也寫著：相位很小時，正弦幾乎等於直線，看起來是線性的。',
       '再拉到一點零，兩個圓點分開了，直線是一點零，正弦只有零點八四；擺角一大，單擺也像這樣不再跟著直線走。'],
      actions=[(0, 0.1, ('js', _top('s1'))),
               (1, 0.9, ('js', _set('phi', 0.5))), (1, 1.3, ('js', _set('phi', 0.4))), (1, 1.7, ('js', _set('phi', 0.3))),
               (1, 2.1, ('js', _set('phi', 0.25))), (1, 2.5, ('js', _set('phi', 0.2))),
               (3, 0.4, ('js', _set('phi', 0.4))), (3, 0.8, ('js', _set('phi', 0.6))), (3, 1.2, ('js', _set('phi', 0.8))),
               (3, 1.6, ('js', _set('phi', 1.0)))],
      points=[('藍色直線', '電流和磁通成正比'), ('相位零點二', '正弦幾乎等於直線'), ('拉到一點零', '兩個圓點分開')],
      shot=(2, 2.0)),
 dict(key='linear', after=6, page='lc', hash='s2', scene='LC 與約瑟夫森接面 圖解第 2 步：用正弦波去推，輸出長什麼樣？',
      title='動畫展示：線性就是加倍得加倍', sub='互動圖解：LC 與約瑟夫森接面第 2 步（平面互動圖）',
      sentences=[
       '換到圖解的第二步：用同一個正弦波去推電感和約瑟夫森接面，上面畫兩個週期的電流，下面是各個頻率的柱子。',
       '把驅動振幅調小到零點三，藍色和橘色的波形幾乎疊在一起，下面的柱子幾乎只剩最左邊那一對，也就是原本的頻率，叫做基頻。',
       '讀數欄寫著：藍色電感的輸入加倍，輸出峰值就變成兩倍，輸入和輸出成正比，這就叫做線性。',
       '而且藍色的頻譜永遠只有基頻一根，線性系統不會自己產生新的頻率。'],
      actions=[(0, 0.1, ('js', _top('s2'))),
               (1, 0.8, ('js', _set('amp', 1.1))), (1, 1.2, ('js', _set('amp', 0.8))), (1, 1.6, ('js', _set('amp', 0.5))),
               (1, 2.0, ('js', _set('amp', 0.3)))],
      points=[('同一個正弦波', '推電感和接面'), ('振幅零點三', '兩條波形幾乎重疊'), ('線性系統', '輸入加倍、輸出加倍')],
      pmap=[0, 1, 2, 2], shot=(1, 5.0)),
 dict(key='overdrive', after=8, page='lc', hash='s2', scene='LC 與約瑟夫森接面 圖解第 2 步：用正弦波去推，輸出長什麼樣？',
      title='動畫展示：推太大力就走樣', sub='互動圖解：LC 與約瑟夫森接面第 2 步（平面互動圖）',
      sentences=[
       '回到第二步，這次把驅動振幅慢慢加大到二點五。',
       '藍色電感的波形頂端標著二點五，橘色的電流卻最高只到上面那條虛線，那是接面能通過的最大電流，波峰中間還凹了下去。',
       '下面第二對柱子代表三倍的頻率，橘色那根已經長到大約基頻的四成多；推得越用力，新產生的頻率就越強。',
       '讀數也寫著：橘色的輸入加倍，輸出峰值只變成一點零零倍；振幅一大，線性的類比就不管用了。'],
      actions=[(0, 0.1, ('js', _top('s2'))),
               (0, 1.6, ('js', _set('amp', 1.6))), (0, 2.0, ('js', _set('amp', 1.8))), (0, 2.4, ('js', _set('amp', 2.0))),
               (0, 2.8, ('js', _set('amp', 2.2))), (0, 3.2, ('js', _set('amp', 2.35))), (0, 3.6, ('js', _set('amp', 2.5)))],
      points=[('振幅加大', '橘色被壓在虛線下'), ('三倍頻', '約基頻的四成多'), ('大振幅', '線性類比不管用')],
      pmap=[0, 0, 1, 2], shot=(2, 4.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q021'] 取用。"""

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

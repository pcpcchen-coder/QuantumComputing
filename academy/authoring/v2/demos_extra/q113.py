"""Q113 讀圖之前：三個約定與今天用到的閘 — v2 動畫展示段（格式見 ../demos.py 的說明）。

全部用 bc = animations/basic-circuits.html（淺色主題：正振幅 --pos #1D6A8B 藍、負振幅 --neg #B65C12 橘；
閘方塊 H 藍 --h、X 酒紅 --x #A23B5C、Z 紫 --z #7348A3；起點 |0⟩、最右邊量測錶、橘色虛線游標 .head）。
按鈕 id：#bFirst「⏮ 起點」、#bNext「下一步 ▶」、#m1000「量測 1,000 次」；選項 #opts .seg button:nth-child(n)。
- read（#superposition）：讀一張一顆位元的線路：q0、|0⟩、H、量測錶；下一步讓虛線走過 H，柱子從一根變兩根一樣高；量測 1,000 次約各半。
- order（#bell）：選 Φ⁻（準備步驟 X(q0)）或 Ψ⁺（X(q1)），按起點再下一步一次，只做準備的翻轉閘：|01⟩、|10⟩ 的柱子升到 +1；
  選項按下後頁面停在最後一步（rebuild(false)），所以同一段 js 裡立刻按「起點」。後面的 H、CNOT 是淡色（.future），本段不播。
- zgate（#interference，選項「有 Z」）：只走前兩步 H、Z：|1⟩ 柱子由藍翻成橘色 −0.707，兩根下方的機率仍是 50%；第三步留給 Q115。
已用 Playwright（1600×900，zoom 0.8）實拍確認畫面：|ψ⟩ = |01⟩、|10⟩、(|0⟩ − |1⟩) / √2。
"""

LESSON = 'Q113'

# basic-circuits.html 是一般網頁：縮小並捲到選項列，讓選項、電路、振幅與量測卡同時入鏡
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")


def _pick(n):
    """點第 n 個選項（頁面會跳到最後一步），再立刻按「起點」回到第 0 步"""
    return ('js', f"(function(){{var b=document.querySelector('#opts .seg button:nth-child({n})');window.__flash&&window.__flash(b);"
                  "b.click();document.getElementById('bFirst').click();})()")


_LIST = [
 dict(key='read', after=4, page='bc', hash='superposition', scene='量子電路入門互動動畫：疊加（讀一張線路圖）',
      title='動畫展示：照約定一讀線路', sub='三維動畫：量子電路入門——疊加範例的線路圖',
      sentences=[
       '打開線路入門動畫的疊加範例，照約定一來讀：左邊寫著編號零的位元，從零態出發，線上有一個藍色的哈達瑪閘，最右邊是量測。',
       '一開始橘色虛線停在閘的左邊；按下一步，虛線走到閘的右邊，下面的柱子從一根變成一樣高的兩根。',
       '最後走到量測，按量測一千次，綠色的次數條，零和一大約各占一半。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (1, 4.2, ('sel', '#bNext')), (2, 2.4, ('sel', '#m1000'))],
      points=[('最左邊', '編號零，從零態出發'), ('按下一步', '虛線往右走一格'), ('量測一千次', '零和一約各一半')], shot=(2, 4.5)),
 dict(key='order', after=5, page='bc', hash='bell', scene='量子電路入門互動動畫：Bell 態（只播準備的翻轉閘）',
      title='動畫展示：編號零寫在最右邊', sub='三維動畫：量子電路入門——兩顆位元的位元順序',
      sentences=[
       '換到有兩條橫線的範例：上面是編號零，下面是編號一；先選上方第二個選項，翻轉閘出現在編號零那條線上。',
       '按下一步，只做這個翻轉閘：升起來的柱子是零一，量測一千次也全部是零一，編號零的一寫在最右邊。',
       '換成第三個選項，翻轉閘移到編號一的線上，一樣只走一步，升起來的變成一零。',
       '後面淡淡的那些閘，是範例三才要用到的步驟，今天先不按。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 7.6, _pick(2)),
               (1, 0.6, ('sel', '#bNext')), (1, 4.4, ('sel', '#m1000')),
               (2, 0.6, _pick(3)), (2, 5.0, ('sel', '#bNext'))],
      points=[('上下兩條線', '編號零在上面'), ('翻編號零', '讀出零一'), ('翻編號一', '讀出一零')], shot=(1, 8.5)),
 dict(key='zgate', after=8, page='bc', hash='interference', scene='量子電路入門互動動畫：干涉（只播前兩步 H、Z）',
      title='動畫展示：相位翻轉閘與負振幅', sub='三維動畫：量子電路入門——柱子的正負顏色',
      sentences=[
       '再看干涉範例的前兩步，這裡有藍色的哈達瑪閘和紫色的相位翻轉閘，第三個閘留到範例二再講。',
       '按下一步，做完哈達瑪閘，零和一兩根藍色柱子一樣高，機率各一半。',
       '再按一次，做完相位翻轉閘，一那根柱子翻到下面，變成橘色的負振幅，零還是藍色的正振幅。',
       '看柱子下面的數字，兩個機率仍然都是百分之五十，負號在機率裡看不出來。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (1, 0.5, ('sel', '#bNext')), (2, 0.5, ('sel', '#bNext'))],
      points=[('哈達瑪閘之後', '兩根藍柱一樣高'), ('相位翻轉閘之後', '一變成橘色負振幅'), ('機率', '仍然各百分之五十')], shot=(3, 2.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q113'] 取用。"""

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

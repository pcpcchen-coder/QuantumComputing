"""Q114 範例 1：疊加——量子硬幣與 |+⟩、|−⟩ — v2 動畫展示段（格式見 ../demos.py 的說明）。

bc = animations/basic-circuits.html#superposition（淺色主題：正振幅 --pos #1D6A8B 藍、負振幅 --neg #B65C12 橘；
Bloch 向量 .vec 用 --neg 橘色；軸標 |0⟩、|1⟩、+x、−x、+y；閘方塊 H 藍、X 酒紅 --x #A23B5C）。
選項「起始態」#opts .seg button:nth-child(1) = |0⟩（預設）、(2) = |1⟩；按選項會 rebuild(false)：頁面直接停在最後一步，並清除量測。
按鈕 id：#bFirst「⏮ 起點」、#bNext「下一步 ▶」、#m1「量測 1 次」、#m1000「量測 1,000 次」（量測會累加，不自動清除）。
- plusminus：|0⟩ 下一步 → |+⟩（兩根藍柱 +.707、箭頭到 +x）；改選 |1⟩、起點、下一步（X：箭頭到南極、|1⟩ 柱 +1）、
  下一步（H：|1⟩ 柱翻下變橘 −.707、箭頭到 −x）。上一課 Q113 只用了 |0⟩ 起點的「下一步、量一千次」。
- blind：選 |1⟩（直接是 |−⟩），量測 1 次 × 3、再量測 1,000 次（累加到 1,003 次）；改選 |0⟩（|+⟩，量測清除）再量 1,000 次。
op = animations/operation.html#qubit（js/operation/01_qubit.js）：
- equator：按 |+⟩（θ=90°、φ=0°，清除統計）→ 一次跑 1000 shots → 拖「φ（相位）」0→180（只改 ph，不清除統計，
  青色理論線位置由 θ 決定，不動）→ 清除統計 → 再跑 1000 shots。θ=90°、φ=180° 即 (|0⟩ − |1⟩)/√2。
"""

LESSON = 'Q114'

# basic-circuits.html 是一般網頁：縮小並捲到選項列，讓選項、電路、振幅與量測卡同時入鏡（同 Q113）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")


def _opt(n, first=False):
    """點起始態第 n 個選項（頁面會跳到最後一步）；first=True 時立刻再按「起點」回到第 0 步"""
    tail = "document.getElementById('bFirst').click();" if first else ''
    return ('js', f"(function(){{var b=document.querySelector('#opts .seg button:nth-child({n})');window.__flash&&window.__flash(b);"
                  f"b.click();{tail}}})()")


_LIST = [
 dict(key='plusminus', after=5, page='bc', hash='superposition', scene='量子電路入門互動動畫：疊加（起始態 |0⟩ 與 |1⟩ 對照）',
      title='動畫展示：正號和負號兩種疊加態', sub='三維動畫：量子電路入門——起始態零與一的對照',
      sentences=[
       '打開線路入門動畫的疊加範例，起始態是零；按下一步做哈達瑪閘，兩根柱子都是朝上的藍色，橘色箭頭倒向赤道。',
       '現在把起始態換成一，線路前面多了一個酒紅色的翻轉閘；從起點按下一步，箭頭轉到南極，一的柱子升到頂。',
       '再按一次下一步做哈達瑪閘，一的柱子翻到下面，變成橘色的負零點七零七，箭頭停在赤道的另一邊。',
       '兩次柱子下面都寫著百分之五十，不同的只有一那根柱子的方向，和箭頭指的位置。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 5.4, ('sel', '#bNext')),
               (1, 1.4, _opt(2, first=True)), (1, 7.6, ('sel', '#bNext')),
               (2, 0.6, ('sel', '#bNext'))],
      points=[('起始態零', '兩根藍柱，箭頭在一邊'), ('起始態一', '一的柱子翻成橘色'), ('機率', '都是百分之五十')], shot=(3, 2.0)),
 dict(key='equator', after=6, page='op', hash='qubit', scene='3D 場景 1：量子位元的狀態與測量',
      title='動畫展示：赤道上的兩個對面', sub='三維動畫：量子位元的狀態與測量',
      sentences=[
       '換到三維動畫的量子位元場景，按加號那一顆，箭頭躺到赤道上；一次跑一千次，右邊兩根柱子差不多一樣高。',
       '現在把相位滑桿推到一百八十度，箭頭沿著赤道轉到正對面，這個位置就是負號那一種疊加態。',
       '青色的理論線一動也不動，左邊面板的理論機率仍然是零點五和零點五。',
       '清除統計後再跑一千次，兩根柱子還是差不多一樣高；箭頭的方向，量測看不出來。'],
      actions=[(0, 4.4, ('click', '|+⟩')), (0, 7.8, ('click', '一次跑 1000 shots')),
               (1, 0.6, ('sweep', 'φ（相位）', 0, 180, 4.0)),
               (3, 0.4, ('click', '清除統計')), (3, 2.2, ('click', '一次跑 1000 shots'))],
      points=[('加號那一顆', '箭頭在赤道上'), ('相位一百八十度', '轉到正對面'), ('理論機率', '仍然各一半')], shot=(2, 2.0)),
 dict(key='blind', after=8, page='bc', hash='superposition', scene='量子電路入門互動動畫：疊加（盲測：只看量測次數）',
      title='動畫展示：只看次數的盲測', sub='三維動畫：量子電路入門——量測一次與一千次',
      sentences=[
       '接著在動畫裡試一回盲測：起始態選一，頁面直接停在最後一步，也就是負號那一種疊加態。',
       '先按三次量測一次，綠框裡的結果每次都可能不同，才三次，還看不出比例。',
       '再按量測一千次，綠色的次數條一路往右拉，最後零和一都停在灰色理論底色的一半附近。',
       '把起始態換回零，變成正號那一種，再量一千次，一樣是大約各半；只看次數，分不出是哪一種。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 3.8, _opt(2)),
               (1, 0.6, ('sel', '#m1')), (1, 2.0, ('sel', '#m1')), (1, 3.4, ('sel', '#m1')),
               (2, 1.0, ('sel', '#m1000')),
               (3, 1.4, _opt(1)), (3, 5.2, ('sel', '#m1000'))],
      points=[('量測一次', '每次結果可能不同'), ('量測一千次', '零和一約各一半'), ('換成正號', '次數看起來一樣')], shot=(2, 3.5)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q114'] 取用。"""

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

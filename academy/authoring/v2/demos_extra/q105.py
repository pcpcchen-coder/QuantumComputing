"""Q105 第 7 課：BV 密碼——一次猜中三位元 — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html#bv（第 9 章）。步驟按鈕在 #g9steps（第 8 個是「自由實驗」，dur 0、不會自動接續）；
自由實驗的控制項在 #g9extra：密碼按鈕 [data-s9="0"…"7"]、[data-s9="hide"]「隨機（隱藏）」；①–④ 是 [data-op9="H3"|"O"|"H3b"|"M"]；
#g9run「一鍵執行」、#g9cq「古典查詢一次」。面板要先把 #g9extra 捲到頂端，按鈕、密碼／查詢次數欄和量測統計才會一起入鏡（1600×900 實測）。
動畫時間：H⊗3 1.6 秒、黑盒子 1.4 秒、量測 50 次約 2.8 秒；一鍵執行全程約 7.4 秒，結束才在左上角字幕揭曉密碼。
長條：正振幅金色、負振幅紅色，標籤「+0.35 ・ 12.5%」。
bc = animations/basic-circuits.html#bv（範例 7，教科書版：q0–q2 輸入、q3 輔助）。密碼按鈕在 #opts 內（依序 s2、s1、s0；
改選項會停在最後一步）；#bNext、#m1000、#mClear。頁面先捲到 #opts。最後一步振幅只剩 0101（藍、朝上）和 1101（橘、朝下）。
"""

LESSON = 'Q105'

_STEP8 = '#g9steps button:nth-child(8)'
_FIT = "document.getElementById('g9extra').scrollIntoView({block:'start'});"
_BC_FIT = "document.getElementById('opts').scrollIntoView({behavior:'smooth', block:'start'})"

_LIST = [
 dict(key='amps', after=6, page='tr', hash='bv', scene='Transmon 3D 第 9 章：BV 密碼——自由實驗',
      title='動畫展示：八根柱子的正負號', sub='三維動畫：BV 密碼——一步一步看振幅',
      sentences=[
       '打開超導三維動畫的第九章，直接按第八步自由實驗，再把密碼選成一零一；中間八根柱子代表零零零到一一一八個結果，一開始只有零零零那一根。',
       '按一號按鈕，三顆一起做哈達瑪閘，八根柱子都變成正零點三五，每一根上面都標著百分之十二點五，這時候量，只能亂猜。',
       '再按二號黑盒子，只查詢這一次，看板上第一和第三條線出現相位翻轉閘，零零一、零一一、一零零、一一零四根翻成紅色朝下，機率卻還是各百分之十二點五。',
       '按三號按鈕再做一次哈達瑪閘，七根柱子縮成零，只剩一零一升到一；再按四號量測五十次，右邊的統計五十次全部落在一零一。'],
      actions=[(0, 3.8, ('sel', _STEP8)), (0, 5.0, ('js', _FIT)), (0, 7.2, ('sel', '[data-s9="5"]')),
               (1, 0.8, ('sel', '[data-op9="H3"]')),
               (2, 0.8, ('sel', '[data-op9="O"]')),
               (3, 0.6, ('sel', '[data-op9="H3b"]')), (3, 7.4, ('sel', '[data-op9="M"]'))],
      points=[('一號哈達瑪閘', '八根都是正零點三五'), ('二號黑盒子', '四根翻成紅色'), ('三號哈達瑪閘', '只剩一零一')], shot=(2, 6.0)),
 dict(key='duel', after=9, page='tr', hash='bv', scene='Transmon 3D 第 9 章：BV 密碼——自由實驗',
      title='動畫展示：古典三次對量子一次', sub='三維動畫：BV 密碼——隱藏密碼對決',
      sentences=[
       '來一場真正的對決：同樣進到第八步，按隨機隱藏，電腦偷偷藏好一個密碼，面板上的密碼欄只剩問號。',
       '古典方先上場，連按三次古典查詢一次，看板每問一次只多拼出一位，問到第三次，左上角才寫出完整的密碼。',
       '換量子方，按一鍵執行：三顆先做哈達瑪閘，查詢黑盒子一次，再做哈達瑪閘，最後量五十次。',
       '五十次全部落在同一根柱子上，左上角揭曉密碼並打勾，面板的查詢次數寫著量子一次、古典三次。'],
      actions=[(0, 1.0, ('sel', _STEP8)), (0, 2.2, ('js', _FIT)), (0, 4.0, ('sel', '[data-s9="hide"]')),
               (1, 2.0, ('id', 'g9cq')), (1, 4.6, ('id', 'g9cq')), (1, 7.0, ('id', 'g9cq')),
               (2, 1.2, ('id', 'g9run'))],
      points=[('隨機隱藏', '誰都不知道密碼'), ('古典方', '問三次才拼出'), ('量子方', '只查詢一次')], shot=(3, 3.0)),
 dict(key='textbook', after=10, page='bc', hash='bv', scene='基礎量子電路 範例 7：Bernstein–Vazirani',
      title='動畫展示：換成自己的密碼', sub='三維動畫：教科書版電路——輔助位元與受控反閘',
      sentences=[
       '換到量子電路入門的密碼範例，這是教科書的版本：上面三條線是輸入，最下面多一顆輔助位元，黑盒子裡放的是受控反閘。',
       '連按四次下一步：輔助位元先被翻轉閘翻成一，全部做哈達瑪閘，經過黑盒子，再做一次哈達瑪閘，最後只剩一根藍色朝上、一根橘色朝下。',
       '朝下那根是因為輔助位元一直停在相減的疊加態；按量測一千次，最近一次顯示一零一，下面寫著密碼等於一零一。',
       '把密碼的後兩位各點一下，改成一一零，黑盒子裡的受控反閘跟著換位置；清除後再量一千次，答案變成一一零。'],
      actions=[(0, 0.3, ('js', _BC_FIT)),
               (1, 3.2, ('sel', '#bNext')), (1, 4.9, ('sel', '#bNext')), (1, 6.6, ('sel', '#bNext')), (1, 8.0, ('sel', '#bNext')),
               (2, 5.0, ('sel', '#m1000')),
               (3, 1.2, ('sel', '#opts .seg button:nth-child(2)')), (3, 2.0, ('sel', '#opts .seg button:nth-child(3)')),
               (3, 7.4, ('sel', '#mClear')), (3, 8.2, ('sel', '#m1000'))],
      points=[('輔助位元', '翻轉閘加哈達瑪閘'), ('黑盒子', '密碼為一的位接受控反閘'), ('換成一一零', '答案跟著變')], shot=(2, 8.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q105'] 取用。"""

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

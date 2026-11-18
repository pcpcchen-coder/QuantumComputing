"""Q009 量子線路像樂譜：v2 動畫展示段（格式見 ../demos.py 的說明）。"""

LESSON = 'Q009'

# basic-circuits.html 是一般網頁：先縮小並捲到「電路」卡，讓線路圖和量測卡同時入鏡
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#circ').closest('.card').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-12);")

_LIST = [
 dict(key='read', after=3, page='bc', hash='superposition', scene='量子電路入門互動動畫：疊加',
      title='動畫展示：讀一張最簡單的線路圖', sub='三維動畫：量子電路入門——疊加',
      sentences=[
       '打開線路入門動畫的疊加範例，上面這張圖只有一條橫線，代表一個量子位元，最左邊寫著它從狀態零出發。',
       '線上有一個方塊，最右邊是一個像儀表的符號；按下一步，游標往右走過方塊，箭頭被轉到赤道。',
       '走到儀表就是測量，按量測一千次，零和一大約各一半。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (1, 5.8, ('sel', '#bNext')), (2, 2.0, ('sel', '#m1000'))],
      points=[('一條橫線', '一個量子位元'), ('方塊', '把箭頭轉到赤道'), ('儀表', '零和一各約一半')], shot=(2, 4.6)),
 dict(key='step', after=4, page='op', hash='circuit', scene='3D 場景 6：量子線路——一步一步執行',
      title='動畫展示：一欄一欄往右走', sub='三維動畫：量子線路一步一步執行',
      sentences=[
       '換到三維動畫的量子線路場景，選干涉這一條：一條線上有三個方塊，最後是測量。',
       '按一次單步，第一個方塊發光，下方兩根柱子變成一樣高，代表零和一的機率各一半。',
       '再按一次，相位翻轉只讓柱子換了顏色；第三步之後，只剩下狀態一的柱子。',
       '最後走到測量欄，跑一千次的結果全部都是一。'],
      actions=[(0, 1.4, ('click', '干涉')), (1, 0.6, ('click', '單步')), (2, 0.4, ('click', '單步')),
               (2, 3.9, ('click', '單步')), (3, 1.4, ('click', '單步'))],
      points=[('第一步', '柱子一樣高'), ('相位翻轉', '只換顏色'), ('走到測量', '一千次都是一')], shot=(3, 4.4)),
 dict(key='column', after=5, page='op', hash='circuit', scene='3D 場景 6：量子線路——一步一步執行',
      title='動畫展示：同一欄同時執行', sub='三維動畫：量子線路一步一步執行',
      sentences=[
       '再選一條比較寬的線路，這裡有三條橫線，所以是三個量子位元。',
       '按單步，第一欄只有最下面那條線上有一個方塊，其他兩條線這一拍休息。',
       '再按一次，三條線上的方塊排在同一欄，一起發光，就像總譜上同一拍的三個音符同時演奏。'],
      actions=[(0, 0.8, ('click', 'Deutsch')), (1, 1.0, ('click', '單步')), (2, 1.2, ('click', '單步'))],
      points=[('三條橫線', '三個量子位元'), ('第一欄', '只有一個方塊'), ('同一欄', '三個閘一起執行')], shot=(2, 4.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q009'] 取用。"""

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

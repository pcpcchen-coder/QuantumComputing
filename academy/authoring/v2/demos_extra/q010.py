"""Q010 第一個量子程式：貝爾態 — v2 動畫展示段（格式見 ../demos.py 的說明）。"""

LESSON = 'Q010'

# basic-circuits.html 是一般網頁：縮小並捲到範例標題，讓選項、電路和量測卡同時入鏡
_BC_FIT = ("document.body.style.zoom='0.62';"
           "document.querySelector('#sceneTitle').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-8);")
# 展開頁面最下方的程式碼區塊並捲過去
_BC_CODE = ("document.body.style.zoom='0.9';"
            "document.querySelector('.card.take details').open=true;"
            "document.querySelector('.card.take').scrollIntoView({block:'start'});"
            "window.__flash(document.querySelector('#code').closest('pre'));")

_LIST = [
 dict(key='code', after=6, page='bc', hash='bell', scene='量子電路入門互動動畫：Bell 態',
      title='動畫展示：線路變成程式', sub='三維動畫：量子電路入門——貝爾態的程式碼',
      sentences=[
       '打開線路入門動畫的貝爾態，上面這條線路，就是我們要寫成程式的那四格。',
       '往下捲到最底，展開程式碼區塊：先建立兩顆量子位元、兩格紀錄，接著一行哈達瑪閘、一行受控反閘、一行測量。',
       '倒數第二行請套件內建的取樣器跑一千次，最後一行把結果印出來；教材裡的版本換成高效能模擬器、跑一千零二十四次，線路的部分完全一樣。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (1, 1.2, ('js', _BC_CODE))],
      points=[('上方線路', '貝爾態的四格'), ('程式碼', '一格對應一行'), ('取樣器那一行', '重複跑很多次')], shot=(1, 9.0)),
 dict(key='noise', after=8, page='op', hash='circuit', scene='3D 場景 6：量子線路——一步一步執行',
      title='動畫展示：理想結果和雜訊', sub='三維動畫：量子線路一步一步執行',
      sentences=[
       '換到三維動畫的量子線路場景，選貝爾態，按三次單步，走過哈達瑪閘、受控反閘，最後到測量欄。',
       '右下角的小圖跑了一千次，只有零零和一一兩根柱子，青色的線是理想的機率。',
       '打開加入雜訊的開關，模擬每個閘和每次讀取都有一點出錯的機會，零一和一零就冒出矮矮的小柱子。',
       '真的量子電腦也會這樣，所以看到少量的零一和一零，不代表程式寫錯。'],
      actions=[(0, 1.4, ('click', 'Bell 態')), (0, 4.0, ('click', '單步')), (0, 6.0, ('click', '單步')),
               (0, 8.0, ('click', '單步')), (2, 1.6, ('toggle', '加入雜訊', True))],
      points=[('三次單步', '走到測量欄'), ('理想模擬', '只有零零和一一'), ('加入雜訊', '冒出零一和一零')], shot=(3, 1.5)),
 dict(key='variants', after=10, page='bc', hash='bell', scene='量子電路入門互動動畫：Bell 態',
      title='動畫展示：另外兩種貝爾態', sub='三維動畫：量子電路入門——四種貝爾態',
      sentences=[
       '回到線路入門動畫，上方可以切換四種貝爾態；選第三個，線路最前面就多了一個翻轉閘，放在第二顆上。',
       '按量測一千次，柱子變成零一和一零，兩顆永遠相反。',
       '再選第二個，翻轉閘移到第一顆，量一千次又回到零零和一一，和原本看起來一模一樣。',
       '仔細看左下的振幅柱子，一一那根往下翻成負的，這就是藏起來的正負號。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 6.0, ('sel', '#opts .seg button:nth-child(3)')),
               (1, 1.0, ('sel', '#mClear')), (1, 1.4, ('sel', '#m1000')),
               (2, 1.6, ('sel', '#opts .seg button:nth-child(2)')), (2, 2.4, ('sel', '#mClear')),
               (2, 5.4, ('sel', '#m1000'))],
      points=[('第三種', '零一和一零'), ('第二種', '又是零零和一一'), ('振幅柱子', '一一變成負的')], shot=(3, 2.5)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q010'] 取用。"""

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

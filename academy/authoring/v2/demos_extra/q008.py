"""Q008 糾纏：一對神祕骰子 — v2 動畫展示段（格式見 ../demos.py 的說明）。"""

LESSON = 'Q008'

_LIST = [
 dict(key='shrink', after=3, page='op', hash='register', scene='3D 場景 4：多量子位元：2ⁿ 個振幅與糾纏',
      title='動畫展示：箭頭縮成一點', sub='三維動畫：多量子位元與糾纏',
      sentences=[
       '打開三維動畫的多位元場景，上排是兩顆量子位元各自的小球，下排柱子是四種結果的機率。',
       '按下貝爾態這顆按鈕，做出一對糾纏的量子位元，柱子只剩零零和一一兩根。',
       '再看上排，兩支箭頭都縮成中間一個點：單看任何一顆都猜不出結果，資訊藏在兩顆的關聯裡。'],
      actions=[(0, 0.3, ('click', '重設')), (1, 1.2, ('click', 'Bell 態'))],
      points=[('下排柱子', '四種結果的機率'), ('按貝爾態', '只剩零零和一一'), ('上排箭頭', '縮成一點')], shot=(2, 3.0)),
 dict(key='circuit', after=4, page='bc', hash='bell', scene='基礎量子電路動畫：Bell 態',
      title='動畫展示：兩步做出貝爾態', sub='三維動畫：量子電路入門的貝爾態',
      sentences=[
       '換到量子電路動畫的貝爾態，一開始兩顆量子位元都是零。',
       '按一次下一步，第一顆進入疊加；再按一次，兩位元閘讓第二顆跟著第一顆走。',
       '最後按量測一千次，直方圖只出現零零和一一，各大約一半，零一和一零一次都沒有。'],
      actions=[(0, 0.3, ('js', "window.scrollTo({top: 560, behavior: 'instant'})")), (1, 0.6, ('sel', '#bNext')), (1, 4.6, ('sel', '#bNext')), (2, 1.0, ('sel', '#m1000'))],
      points=[('第一步', '第一顆疊加'), ('第二步', '第二顆跟著走'), ('量一千次', '只有零零和一一')], shot=(2, 5.5)),
 dict(key='measure', after=6, page='op', hash='register', scene='3D 場景 4：多量子位元：2ⁿ 個振幅與糾纏',
      title='動畫展示：一起量和只量一顆', sub='三維動畫：多量子位元與糾纏',
      sentences=[
       '回到多位元場景，每次測量之前，都重新做一次貝爾態，再按測量全部。',
       '結果一下是零零、一下是一一，誰也預測不了，但兩顆永遠相同。',
       '換成只量第一顆，它自己隨機得到零或一，另一顆也跟著確定；可是遠方的人沒有對答案，什麼也看不出來。'],
      actions=[(0, 0.4, ('click', 'Bell 態')), (0, 5.0, ('click', '測量全部')),
               (1, 0.2, ('click', 'Bell 態')), (1, 0.8, ('click', '測量全部')),
               (1, 2.4, ('click', 'Bell 態')), (1, 3.0, ('click', '測量全部')),
               (1, 4.6, ('click', 'Bell 態')), (1, 5.2, ('click', '測量全部')),
               (2, 0.3, ('click', 'Bell 態')), (2, 1.6, ('click', '只測 q0'))],
      points=[('每次重做貝爾態', '再測量全部'), ('零零或一一', '兩顆永遠相同'), ('只量一顆', '單看仍是隨機')], shot=(1, 6.3)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q008'] 取用。"""

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

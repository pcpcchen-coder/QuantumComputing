"""Q007 兩顆、三顆、五十顆：2ⁿ 有多大 — v2 動畫展示段（3D 場景 4：多位元與糾纏，operation.html#register）。

格式同 demos.py。場景程式：animations/js/operation/04_register.js
（滑桿「量子位元數 n」1–4；按鈕「均勻疊加 H⊗ⁿ」「測量全部」「重設 |0…0⟩」；右下插圖：2ⁿ × 16 bytes 記憶體曲線）。
"""

LESSON = 'Q007'

_LIST = [
 dict(key='bars', after=3, page='op', hash='register', scene='3D 場景 4：多位元與糾纏',
      title='動畫展示：每多一顆，位置翻倍', sub='三維動畫：多量子位元與二的次方個振幅',
      sentences=[
       '打開三維動畫的多位元場景，下方底座上的每一個位置代表一種組合，也就是一個振幅。',
       '把量子位元從一顆調到四顆，位置從兩個變成四個、八個，最後變成十六個。',
       '按均勻疊加，十六個位置都立起一樣高的柱子，每一種組合的機率都是十六分之一。'],
      actions=[(1, 1.2, ('slider', '量子位元數 n', 1)), (1, 4.7, ('slider', '量子位元數 n', 2)),
               (1, 5.5, ('slider', '量子位元數 n', 3)), (1, 6.9, ('slider', '量子位元數 n', 4)),
               (2, 0.4, ('click', '均勻疊加'))],
      points=[('一個位置', '一種組合的振幅'), ('一顆到四顆', '兩個變十六個'), ('均勻疊加', '柱子一樣高')], shot=(2, 4.0)),
 dict(key='readout', after=5, page='op', hash='register', scene='3D 場景 4：多位元與糾纏',
      title='動畫展示：振幅很多，讀出來很少', sub='三維動畫：測量全部只得到一種組合',
      sentences=[
       '把量子位元調成四顆，按均勻疊加，十六種組合的柱子一樣高。',
       '現在按測量全部，十六根柱子只剩下一根，我們只讀到四個零或一。',
       '重新疊加再測一次，通常會讀到另一種組合，但每次都只有四個位元的答案。'],
      actions=[(0, 0.3, ('slider', '量子位元數 n', 4)), (0, 2.6, ('click', '均勻疊加')),
               (1, 1.0, ('click', '測量全部')), (2, 0.3, ('click', '均勻疊加')), (2, 1.7, ('click', '測量全部'))],
      points=[('均勻疊加', '十六根一樣高'), ('測量全部', '只剩一根'), ('每次讀出', '只有四個位元')], shot=(1, 4.5)),
 dict(key='memory', after=6, page='op', hash='register', scene='3D 場景 4：多位元與糾纏',
      title='動畫展示：記憶體曲線', sub='三維動畫：精確模擬需要的記憶體',
      sentences=[
       '同一個場景的右下角有一張小圖，畫的是在普通電腦上精確模擬，需要多少記憶體。',
       '橫軸是量子位元的數量；縱軸越往上，代表的數字大得越快，所以一路翻倍的記憶體，畫出來像一條斜直線。',
       '三十顆的點在筆電的位置，五十顆的點，已經和紅色虛線標示的頂級超級電腦總記憶體差不多高。'],
      actions=[(0, 0.3, ('slider', '量子位元數 n', 4)), (0, 1.5, ('click', '均勻疊加'))],
      points=[('右下小圖', '精確模擬的記憶體'), ('斜直線', '一路翻倍'), ('五十顆', '超級電腦等級')], shot=(2, 3.0)),
]


class _Demos(list):
    """清單（目前 demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q007'] 取用。"""

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

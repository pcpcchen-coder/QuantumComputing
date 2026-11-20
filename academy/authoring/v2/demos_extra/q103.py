"""Q103 能階、共振與拉比振盪 — v2 動畫展示段（格式見 ../demos.py 的說明）。

transmon-3d.html 的面板可以捲動：第 3 章把「有 JJ／沒有 JJ」按鈕捲到面板頂端，這時兩排按鈕、
「送 π 脈衝」與即時讀數 #r3p 會同時入鏡（1600×900 實測）。第 3 章驅動模擬 1 秒動畫 = 8 ns：
π 脈衝（20 ns）約 2.5 秒、持續驅動 40 ns 約 5 秒。第 4 章有 JJ 的持續驅動每 2.2 秒轉一圈；
沒有 JJ 時 1 秒動畫 = 16 ns，40 ns 後自動停下。
"""

LESSON = 'Q103'

# 第 3 章：把「有 JJ／沒有 JJ」捲到面板頂端（按鈕、送脈衝、讀數一起入鏡）
_P3_FIT = "document.getElementById('c3tr').scrollIntoView({block:'start'});"
# 第 4 章（有 JJ）：把讀數表捲到面板頂端，讓「類型」、P(|1⟩) 曲線與按鈕同框
_P4_FIT = "document.getElementById('r4psi').closest('dl').scrollIntoView({block:'start'});"
# 第 4 章切到沒有 JJ 前先捲回頂端，讓觀眾看到切換按鈕（沒有 JJ 的說明較短，整個面板放得下）
_P4_TOP = "document.getElementById('panel').scrollTop=0;"

_LIST = [
 dict(key='pi', after=5, page='tr', hash='potential', scene='Transmon 3D 第 3 章：cos 位能井',
      title='動畫展示：同一個派脈衝', sub='三維動畫：位能井——有和沒有約瑟夫森接面',
      sentences=[
       '打開超導三維動畫的第三章位能井，銅色曲線是約瑟夫森接面的位能，梯子的間距越往上越小，旁邊標著每一對的頻率。',
       '按下送派脈衝，青色色塊從最底下的零，整塊搬到上一階的一，面板上一的機率是零點九九四。',
       '切到沒有約瑟夫森接面，梯子變成等距，每一對都是五十四點八億赫茲；再送同一個派脈衝。',
       '這次青色色塊散到好幾階，一只剩兩成左右，平均能階在二點五附近，根本停不住。'],
      actions=[(0, 0.2, ('js', _P3_FIT)), (1, 0.6, ('id', 'c3pi')),
               (2, 0.5, ('id', 'c3lc')), (2, 5.6, ('id', 'c3pi'))],
      points=[('有約瑟夫森接面', '一的機率零點九九四'), ('沒有約瑟夫森接面', '梯子等距'), ('同一個派脈衝', '散到好幾階')], shot=(3, 3.0)),
 dict(key='drive40', after=7, page='tr', hash='potential', scene='Transmon 3D 第 3 章：cos 位能井',
      title='動畫展示：持續驅動四十奈秒', sub='三維動畫：位能井——轉一圈，還是一路往上爬',
      sentences=[
       '同一個畫面，先確認選的是有約瑟夫森接面的電路，這次改按持續驅動四十奈秒。',
       '看青色色塊：先從零整塊搬到一，再從一搬回零，最後面板上零的機率回到一點零零零。',
       '切到沒有約瑟夫森接面，再按一次持續驅動，色塊一路往上爬，擠到最上面那一格。',
       '面板的平均能階停在九點五二，零的機率是零點零零零，就像被越推越大的古典電流振盪。'],
      actions=[(0, 0.2, ('js', _P3_FIT)), (0, 1.2, ('id', 'c3tr')), (1, 0.3, ('id', 'c3long')),
               (2, 0.4, ('id', 'c3lc')), (2, 1.6, ('id', 'c3long'))],
      points=[('有約瑟夫森接面', '轉一圈回到零'), ('沒有約瑟夫森接面', '一路往上爬'), ('平均能階', '九點五二')], shot=(3, 2.0)),
 dict(key='rabi', after=8, page='tr', hash='control', scene='Transmon 3D 第 4 章：用微波轉動布洛赫球',
      title='動畫展示：拉比振盪', sub='三維動畫：用微波轉動布洛赫球',
      sentences=[
       '換到第四章操控，按持續驅動，布洛赫球上的箭頭開始連續轉圈，右邊面板的金色曲線跟著上下起伏。',
       '注意面板的類型欄，大部分時間寫的是疊加態，只有轉到最上面或最下面的瞬間，才變成純的零或純的一。',
       '現在切到沒有約瑟夫森接面，左邊梯子的上面幾階標著紅色的也共振；再按持續驅動，箭頭越縮越短，掉向球心。',
       '四十奈秒後驅動自動停下，類型欄變成紅字：已漏出零和一，不是量子位元的狀態。'],
      actions=[(0, 0.2, ('js', _P4_FIT)), (0, 1.4, ('id', 'c4rabi')),
               (2, 0.3, ('js', _P4_TOP)), (2, 0.5, ('id', 'c4mlc')), (2, 6.4, ('id', 'c4rabi'))],
      points=[('持續驅動', '箭頭連續轉圈'), ('類型欄', '大多是疊加態'), ('沒有約瑟夫森接面', '箭頭縮到球心')], shot=(3, 2.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q103'] 取用。"""

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

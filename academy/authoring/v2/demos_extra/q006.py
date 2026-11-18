"""Q006 干涉：波可以互相抵消 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：
- animations/basic-circuits.html#interference（範例 2：H‑Z‑H）。按鈕 id：bFirst、bNext、m1000、mClear；
  選項「中間的閘」在 #opts 內，第二顆按鈕是「沒有 Z」（改選項後停在最後一步）。頁面要先捲到 #opts 才看得到電路、振幅柱與量測。
- animations/operation.html#interference（js/operation/08_interference.js）。按鈕：「單一量子位元：兩條路徑」「3 位元：8 條路徑（Deutsch–Jozsa）」
  「A：自動掃描 φ」「A：中途偵測路徑（破壞干涉）」「常數 f = 0」「平衡 f = x₀」；滑桿「A：相位 φ」。
Q001 已用過 interference 場景的「0→180 度＋偵測路徑」；本課改看九十度一半一半、自動掃描的干涉條紋、八條路徑模式，不重複偵測路徑。
"""
LESSON = 'Q006'

_SCROLL = "document.getElementById('opts').scrollIntoView({behavior:'smooth', block:'start'})"
_OPT_NO_Z = '#opts .seg button:nth-child(2)'
_SCENE8 = '3D 場景 8：干涉'

_LIST = [
 dict(key='hzh', after=5, page='bc', hash='interference', scene='基礎量子電路 範例 2：干涉',
      title='動畫展示：一個負號決定結果', sub='三維動畫：量子電路的干涉範例',
      sentences=[
       '換到量子電路的干涉範例：一個量子位元先做疊加，再只改一個正負號，最後再混合一次。',
       '第一步做出疊加，兩根藍色柱子一樣高；第二步替一那根加上負號，它翻成銅色朝下，量一千次還是各一半。',
       '第三步再混合一次，通往零的兩條路一正一負互相抵消，量一千次，全部都是一。',
       '把中間改正負號的那一步拿掉，結果整個反過來，量一千次全部是零。'],
      actions=[(0, 0.2, ('js', _SCROLL)),
               (1, 0.3, ('sel', '#bNext')), (1, 4.6, ('sel', '#bNext')), (1, 8.4, ('sel', '#m1000')),
               (2, 0.4, ('sel', '#mClear')), (2, 0.8, ('sel', '#bNext')), (2, 5.6, ('sel', '#m1000')),
               (3, 2.4, ('sel', _OPT_NO_Z)), (3, 2.8, ('sel', '#mClear')), (3, 4.9, ('sel', '#m1000'))],
      points=[('只改正負號', '機率還是各一半'), ('再混合一次', '通往零的路抵消'), ('拿掉負號', '結果反過來')], shot=(2, 7.4)),
 dict(key='halfway', after=6, page='op', hash='interference', scene=_SCENE8,
      title='動畫展示：轉到九十度，再轉到底', sub='三維動畫：加速的關鍵——振幅會互相抵消',
      sentences=[
       '回到三維動畫的干涉場景，右上的大圓盤是出口零，右下是出口一，藍色和橙色箭頭各代表一條路的貢獻。',
       '把相位從零度轉到九十度，橙色箭頭跟著轉向，上下兩支白色的總和箭頭變得一樣大，各占一半。',
       '繼續轉到一百八十度，上面的橙色箭頭轉到藍色箭頭的正對面，兩者抵消，出口零的機率變成零。',
       '打開自動掃描，右下角小圖的白點沿著曲線上上下下，亮、暗、亮、暗，這就是兩條路的干涉條紋。'],
      actions=[(0, 0.2, ('click', '單一量子位元')), (0, 0.4, ('slider', 'A：相位 φ', 0)),
               (1, 0.6, ('sweep', 'A：相位 φ', 0, 90, 3.6)),
               (2, 0.6, ('sweep', 'A：相位 φ', 90, 180, 4.6)),
               (3, 0.6, ('toggle', 'A：自動掃描 φ', True))],
      points=[('九十度', '兩個出口各一半'), ('一百八十度', '出口零抵消為零'), ('自動掃描', '畫出干涉條紋')], shot=(2, 8.5)),
 dict(key='eightpaths', after=10, page='op', hash='interference', scene=_SCENE8,
      title='動畫展示：八條路一起干涉', sub='三維動畫：八條路徑匯到同一個出口',
      sentences=[
       '挑戰題：如果路不只兩條呢？在干涉場景切換到三個位元，現在有八條路，最後全部匯到同一個出口。',
       '選常數函數，八支箭頭全都朝同一個方向，頭尾接起來最強，這個出口的機率是百分之百。',
       '換成平衡函數，四支朝右、四支朝左，頭尾接起來剛好回到原點，這個出口的機率變成零。',
       '量子演算法做的事，就是安排這些箭頭的方向，讓不要的答案自己抵消掉。'],
      actions=[(0, 4.4, ('click', '3 位元')), (1, 0.3, ('click', '常數 f = 0')), (2, 0.3, ('click', '平衡 f = x'))],
      points=[('八條路', '匯到同一個出口'), ('箭頭同向', '機率百分之百'), ('正負各半', '完全抵消')], shot=(2, 6.0)),
]


class _Demos(list):
    """demos.py 的載入器用 DEMOS[LESSON] = DEMOS（清單）；也接受 {'Q006': [...]} 形式的存取。"""
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

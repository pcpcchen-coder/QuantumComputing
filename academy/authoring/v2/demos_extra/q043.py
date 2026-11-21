"""Q043 稀釋冷凍原理 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/peripherals.html#overview（js/peripherals/01_overview.js）、#dilution（js/peripherals/03_dilution.js）。
控制項（ui.button／ui.toggle／ui.slider 建在 #controls）：
  01_overview.js：按鈕「脈衝管氦氣」「冷卻水」「混合氣循環」「真空」…（預設 on，點一下切換）、「只看冷卻相關」
  03_dilution.js：滑桿「³He 循環率 ṅ (mmol/s)」（0.1–1.5，預設 0.5）、「MXC 上的熱負載 (μW)」（0.5–60，預設 10）；讀數「平衡溫度 …」
兩頁的說明文字很多，控制項在面板下方；每段開頭把面板捲到底，讓按鈕、滑桿和讀數入鏡。
"""
LESSON = 'Q043'

_PANEL_BOTTOM = ('js', "document.getElementById('panel').scrollTop=1e5;")

_LIST = [
 dict(key='ghs', after=3, page='pe', hash='overview', scene='周邊系統 3D 場景 1：系統全景',
      title='動畫展示：混合氣從哪裡來', sub='三維動畫：機房全景——混合氣循環',
      sentences=[
       '先打開周邊系統的機房全景，按只看冷卻相關，再把脈衝管氦氣、冷卻水和真空三條線關掉，只留下紫色的混合氣循環。',
       '紫色的粗管從冷凍機頂部把氣抽到旁邊的氣體處理系統，細一點的管子再把淨化過的氣送回冷凍機。',
       '氣體處理系統旁邊連著一個儲存槽，停機的時候，昂貴的混合氣就收回這個槽裡，一點都不能漏掉。'],
      actions=[(0, 0.2, _PANEL_BOTTOM), (0, 3.4, ('click', '只看冷卻相關')),
               (0, 5.6, ('toggle', '脈衝管氦氣', False)), (0, 6.8, ('toggle', '冷卻水', False)),
               (0, 7.8, ('toggle', '真空', False))],
      points=[('只看冷卻相關', '再關掉三條線'), ('紫色粗管', '把氣抽出來、再送回去'), ('儲存槽', '停機時收回混合氣')], shot=(1, 3.0)),
 dict(key='cycle', after=4, page='pe', hash='dilution', scene='周邊系統 3D 場景 3：稀釋冷凍原理',
      title='動畫展示：跟著氦三繞一圈', sub='三維動畫：稀釋冷凍機裡的氦三循環',
      sentences=[
       '換到稀釋冷凍機的場景，這些小圓點就是氦三，從最上面的室溫一路往下，顏色從紅慢慢變成藍，代表越來越冷。',
       '它們沿著螺旋狀的熱交換器往下，進入混合腔上層的濃相，每次越過金色的界面，就閃出一個小光點，代表在這裡吸熱。',
       '接著氦三混在稀相裡往上走，回到發著橘光的加熱環旁邊，也就是蒸餾室，在那裡蒸發，再從頂端被抽走。',
       '把循環率的滑桿往右拉，圓點跑得更快，代表每秒有更多氦三越過界面；面板上的平衡溫度也跟著往下降。'],
      actions=[(0, 0.2, _PANEL_BOTTOM), (3, 1.8, ('slider', '循環率', 1.2))],
      points=[('顏色', '紅色室溫到藍色極冷'), ('金色界面', '越過就吸熱'), ('循環率', '越大跑得越快')], shot=(1, 6.0)),
 dict(key='balance', after=8, page='pe', hash='dilution', scene='周邊系統 3D 場景 3：稀釋冷凍原理',
      title='動畫展示：熱負載和平衡溫度', sub='三維動畫：冷卻功率曲線與熱負載',
      sentences=[
       '再看右下角的小圖：青色曲線是冷卻功率，橘紅色虛線是熱負載，兩條線交叉的黃點，就是冷凍機會停下來的溫度。',
       '一開始循環率是零點五、熱負載是十微瓦，面板上寫著平衡溫度大約十五點四毫克耳文。',
       '把熱負載慢慢拉到四十微瓦，虛線往上移，黃點往右滑，平衡溫度變成大約三十點九，差不多是兩倍。',
       '面板還寫著，二十毫克耳文時冷卻功率大約十六點八微瓦；熱負載只要比它大，就停不在二十毫克耳文。'],
      actions=[(0, 0.2, _PANEL_BOTTOM), (2, 1.4, ('sweep', '熱負載', 10, 40, 4.0))],
      points=[('黃點', '冷卻功率等於熱負載'), ('熱負載十微瓦', '約十五點四毫克耳文'), ('熱負載四倍', '溫度約兩倍')], shot=(2, 7.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q043'] 取用。"""

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

"""Q042 脈衝管與壓縮機 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/peripherals.html#pulsetube（js/peripherals/02_pulsetube.js）
  滑桿「顯示速度（實際約 1.4 Hz）」（第 67 行，0.2–2×）；小圖「冷頭內壓力」0.8–2.0 MPa（第 70–80 行）；
  讀數「高壓相：氣體壓縮／低壓相：氣體膨脹 → 冷端吸熱」（第 93 行）；粒子顏色依高度代表溫度（第 54、89 行，
  App.tempColor 對數色階：300 K 紅、45 K 橘黃、3 K 綠）。
場景：animations/peripherals.html#overview（js/peripherals/01_overview.js）
  按鈕「只看冷卻相關」（第 85 行）、「視角：冷凍機頂部」（第 89 行）；小圖「典型用電分配」（第 92–95 行，common.js PD.power）。
"""

LESSON = 'Q042'

PT_SCENE = '周邊系統 3D 場景 2：脈衝管冷卻'
PT_SUB = '三維動畫：脈衝管冷卻器與氦壓縮機'

_LIST = [
 dict(key='valve', after=6, page='pe', hash='pulsetube', scene=PT_SCENE,
      title='動畫展示：旋轉閥切換高低壓', sub=PT_SUB,
      sentences=[
       '打開周邊系統動畫的脈衝管場景，左邊深綠色的箱子是氦壓縮機，橘紅色的管子把高壓氦氣送上冷頭，藍色的管子把低壓氦氣帶回來。',
       '我們把顯示速度調慢，看冷頭壓力的小圖，曲線在高低兩個值之間來回切換，一下高、一下低，很像方波。',
       '控制面板的讀數也跟著換：高壓相寫著氣體壓縮，低壓相寫著氣體膨脹、冷端吸熱。',
       '動畫為了讓你看清楚放慢了，真實的旋轉閥快得多，大約每秒切換一點四次。'],
      actions=[(1, 0.6, ('slider', '顯示速度', 0.3))],
      points=[('氦壓縮機', '送出高壓、收回低壓'), ('壓力小圖', '高低來回切換'), ('低壓相', '膨脹、冷端吸熱')], shot=(2, 4.0)),
 dict(key='stages', after=7, page='pe', hash='pulsetube', scene=PT_SCENE,
      title='動畫展示：蓄冷器和兩級冷端', sub=PT_SUB,
      sentences=[
       '再看冷頭裡面：透明管子中有許多小粒子，粒子的顏色代表溫度，最上端是紅色的室溫。',
       '往下到第一級冷端，顏色變成橘黃，標籤寫著大約四十五克耳文；再往下到第二級冷端，粒子變成綠色，大約三克耳文。',
       '粗的蓄冷器裡，粒子只小幅上下擺動；細的脈衝管裡擺得比較大，而且起落比蓄冷器晚一點，這個節奏差就是緩衝槽和小孔調出來的。'],
      actions=[(0, 0.4, ('slider', '顯示速度', 0.5))],
      points=[('粒子顏色', '代表溫度'), ('兩級冷端', '約 45 K、約 3 K'), ('脈衝管', '擺得大、晚一點')], shot=(1, 6.0)),
 dict(key='room', after=8, page='pe', hash='overview', scene='周邊系統 3D 場景 1：系統全景',
      title='動畫展示：機房裡的脈衝管', sub='三維動畫：量子電腦機房全景',
      sentences=[
       '換到周邊系統的機房全景，按下只看冷卻相關，訊號線和電力線都藏起來，只留下冷卻用的管路。',
       '綠色的兩條是脈衝管的氦氣軟管，從脈衝管壓縮機一路接到冷凍機頂部；藍色的是冷卻水，從冷卻水機流到壓縮機。',
       '按視角冷凍機頂部，靠近一點看，綠色軟管接進頂板上方那根銀色的冷頭。',
       '畫面上的用電分配圖裡，數字最大的一條就是脈衝管壓縮機，大約十點七千瓦，比冷卻水系統還多。'],
      actions=[(0, 3.2, ('click', '只看冷卻相關')), (2, 0.4, ('click', '視角：冷凍機頂部'))],
      points=[('只看冷卻相關', '留下冷卻管路'), ('綠色軟管', '壓縮機接到冷頭'), ('用電', '壓縮機約 10.7 kW')], shot=(2, 3.5)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q042'] 取用。"""

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

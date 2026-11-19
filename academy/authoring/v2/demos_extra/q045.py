"""Q045 低溫佈線與熱負載 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（已讀原始碼確認）：
- peripherals.html#wiring（animations/js/peripherals/05_wiring.js）：
  滑桿「量子位元數（線束示意）」1–200、預設 20（ui.slider）；
  選項按鈕「全部」「XY 驅動」「Z 磁通」「讀取輸入」「TWPA 泵浦」「讀取輸出」「直流線束」（ui.radio）。
  插圖顏色：比例 > 100% 紅、> 50% 橘；冷板 97 顆變橘、195 顆變紅，50 K 133 顆變橘（模型見 js/peripherals/common.js PD.wiring）。
- power1000.html#heat：自訂控制項（不是 core.js 的 ui），開關是 #controls 底下的 <label class="tog"><input type=checkbox>，
  依序為「改用 0.047" 細同軸」「磁通線改用超導 NbTi」「容忍 CP 200 mK、MXC 30 mK」「低溫 CMOS＋多工」，所以用 ('js', …) 點 checkbox（第 0、1 個 label.tog）。
"""
LESSON = 'Q045'

# 點 checkbox 並讓整個開關（含文字）閃黃框，觀眾看得出按了哪一個
_TOG = ("(()=>{const l=document.querySelectorAll('#controls > label.tog')[%d];"
        "window.__flash(l);l.querySelector('input').click();})()")
_THIN = ('js', _TOG % 0)   # 改用 0.047" 細同軸
_NBTI = ('js', _TOG % 1)   # 磁通線改用超導 NbTi

_WIRING = '周邊系統 3D 場景 5：低溫佈線'

_LIST = [
 dict(key='lines', after=5, page='pe', hash='wiring', scene=_WIRING,
      title='動畫展示：輸入線和輸出線', sub='三維動畫：低溫佈線——每一層放了什麼元件',
      sentences=[
       '打開周邊系統動畫的低溫佈線場景，六種顏色的線從室溫頂板一路穿到混合腔，每一層旁邊都標著溫度。',
       '在面板上點驅動線，其他線變淡，畫面拉近，四克耳文、冷板和混合腔三層的衰減器閃著光，旁邊標著負二十分貝。',
       '改點讀取輸出線，橘黃色的點反過來往上走，依序經過混合腔的隔離器和行波參量放大器、四克耳文大約四十分貝的低溫放大器，最後是室溫放大。',
       '面板下方的說明也寫著，這條線從混合腔到四克耳文，用的是超導的鈮鈦同軸線。'],
      actions=[(1, 1.6, ('click', 'XY 驅動')), (2, 1.3, ('click', '讀取輸出'))],
      points=[('驅動線', '三層各負二十分貝'), ('讀取輸出線', '往上經過兩級放大'), ('超導鈮鈦線', '混合腔到四克耳文')], shot=(2, 8.0)),
 dict(key='budget', after=7, page='pe', hash='wiring', scene=_WIRING,
      title='動畫展示：線越多，冷板越紅', sub='三維動畫：低溫佈線——各層熱負載預算',
      sentences=[
       '回到全部線路，先把量子位元數設成五十顆，右下角的小圖是每一層熱負載佔冷卻能力的百分比，現在全部是綠色。',
       '接著把滑桿分三次推到兩百，中間的線束越來越密，冷板那一條先變成橘色，到了兩百顆就翻成紅色。',
       '這時面板寫著同軸線一共五百零二條，冷板用掉百分之一百零三，五十克耳文那層也到了百分之七十五。',
       '量子位元到了幾百顆，冷板和五十克耳文就率先吃緊，這是超導量子電腦變大時的瓶頸之一。'],
      actions=[(0, 0.4, ('click', '全部')), (0, 3.0, ('slider', '量子位元數', 50)),
               (1, 0.6, ('slider', '量子位元數', 100)), (1, 3.4, ('slider', '量子位元數', 150)), (1, 5.8, ('slider', '量子位元數', 200))],
      points=[('五十顆', '全部是綠色'), ('推到兩百', '冷板先變紅'), ('瓶頸', '冷板和五十克耳文')], shot=(2, 4.0)),
 dict(key='material', after=10, page='pw', hash='heat', scene='1,000 位元供電設計 場景 3：低溫熱預算',
      title='動畫展示：換線材，熱帳過關', sub='三維動畫：一千位元供電設計——低溫熱預算',
      sentences=[
       '換到一千位元供電設計動畫的熱預算頁，預設是一千顆量子位元、三組稀釋單元，五十克耳文、冷板和混合腔合計都是紅色，面板最下面寫著熱帳不過關。',
       '打開細同軸的開關，五十克耳文、四克耳文和冷板一下子都變成綠色，可是混合腔磁通直流那一行反而衝到底，寫著超過百分之四百五十六。',
       '再打開磁通線改用超導鈮鈦的開關，直流發熱變成零，混合腔合計降到百分之二十一，熱帳終於過關。',
       '在這個估算裡，細線少帶熱、超導線不發熱，兩個辦法搭配起來，三組稀釋單元才撐得住一千顆量子位元的線。'],
      actions=[(1, 1.4, _THIN), (2, 2.0, _NBTI)],
      points=[('預設', '熱帳不過關'), ('細同軸', '被動熱少，直流熱變多'), ('超導磁通線', '熱帳過關')], shot=(2, 7.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q045'] 取用。"""

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

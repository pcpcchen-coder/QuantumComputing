"""Q012 多伊奇–喬薩：一次看穿 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（皆讀原始碼確認）：
- animations/basic-circuits.html#deutsch：SCENES 的 id "deutsch"（第 419 行）；選項「黑盒裡的函數」四顆按鈕依序為
  f(x)=0、f(x)=1、f(x)=x（預設）、f(x)=1−x（第 421 行），畫在 #opts .seg 裡（renderOpts，第 599 行）；
  換選項會 rebuild(false)，直接跳到最後一步並清空量測（rebuild 第 625–638 行、go → clearShots 第 818 行）；
  #m1000（第 222 行）每 30 毫秒 40 次，約 0.75 秒跑完 1,000 次；只量 q0（meas: [0]）；
  最後一步量測後 #verdict 出現綠色（--hit）的「→ 常數函數」或「→ 平衡函數」（第 440、890 行；CSS 第 154 行）。
  直方圖只列理論機率不為 0 的結果（marginal，第 285–289 行），所以常數只有「0」一列、平衡只有「1」一列。
- animations/operation.html#circuit：js/operation/06_circuit.js 的 dj 範例（第 27–34 行），按鈕「Deutsch–Jozsa（平衡函數）」
  （第 169 行，以按鈕文字開頭比對）、「單步 ▶」（第 172 行）；六欄：X(q2)、H×3、CX(0,2)、CX(1,2)、H×3、M(q0,q1)；
  q0 在最上面、q2 在最下面（wy，第 85 行）；下方八根柱子高度 = 機率（common.js AmpBars）；
  最後量測欄跑 1000 shots（第 144 行），右下插圖只有「11」一根（青線 = 理想機率）。
- animations/operation.html#interference：js/operation/08_interference.js；模式按鈕「3 位元：8 條路徑（Deutsch–Jozsa）」（第 70 行）；
  函數按鈕「常數 f = 0」「常數 f = 1」「平衡 f = x₀」（預設）「平衡 f = 奇偶」「隨機（非保證）」（第 61–65、74 行）；
  中間八個小圓盤（第 51–56 行）的金色箭頭 f(x)=1 朝左、否則朝右（第 122–123 行）；右邊大圓「結果 |000⟩」把八支箭頭頭尾相接，
  白色總和箭頭長度 ∝ Σ(−1)^f(x)/8（第 128 行），總和為 0 時 fatArrow 隱藏（core.js 第 161 行）；金色字 P(000)（第 130 行）；
  右下插圖是八種結果的機率直方圖，000 金色、其他藍色（第 88–90 行）。

以 Python 實算（與頁面公式相同）：三位元 平衡 f = x₀ 只量到 001、奇偶只量到 111；常數兩種 P(000) = 1；
兩位元 f = x₀ ⊕ x₁ 只量到 11。
"""

LESSON = 'Q012'

# basic-circuits.html 是一般網頁：縮小並捲到選項列，讓選項、電路、振幅與 Bloch 球、量測卡同時入鏡（同 Q011）
_BC_FIT = ("document.body.style.zoom='0.68';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-8);")

_LIST = [
 dict(key='onebit', after=5, page='bc', hash='deutsch', scene='量子電路入門互動動畫：Deutsch 演算法',
      title='動畫展示：最小的案子只有兩張卡', sub='三維動畫：量子電路入門——多伊奇演算法',
      sentences=[
       '先看最小的案子：打開線路入門動畫的多伊奇演算法，黑盒子只有零和一兩種輸入，古典偵探要問兩次。',
       '上方把黑盒子選成永遠輸出一，畫面直接跳到最後一步；按量測一千次，量的是輸入那一顆，一千次全部是零，下面出現綠字：常數函數。',
       '再換成一減掉輸入，這是平衡的黑盒子；再量一千次，這次全部是一，綠字變成平衡函數。',
       '黑盒子只被問了一次，四種黑盒子都能百分之百判對；接下來的三位元版本，用的是同一招。'],
      actions=[(0, 0.2, ('js', _BC_FIT)),
               (1, 2.6, ('sel', '#opts .seg button:nth-child(2)')), (1, 6.4, ('sel', '#m1000')),
               (2, 1.6, ('sel', '#opts .seg button:nth-child(4)')), (2, 4.4, ('sel', '#m1000'))],
      points=[('永遠輸出一', '一千次都是零：常數'), ('一減掉輸入', '一千次都是一：平衡'), ('只問一次', '四種黑盒子都判對')],
      shot=(2, 7.5)),
 dict(key='circuit', after=6, page='op', hash='circuit', scene='3D 場景 6：量子線路——一步一步執行',
      title='動畫展示：三步判案的線路', sub='三維動畫：量子線路一步一步執行——多伊奇–喬薩',
      sentences=[
       '換到三維動畫的量子線路場景，選多伊奇喬薩那一個範例：上面兩條是輸入位元，最下面一條是輔助位元。',
       '按單步，先把輔助位元翻成一，再讓三條線都做哈達瑪閘；接著兩格是黑盒子，下面八根柱子的高度完全沒變。',
       '再按一次，三條線又做一次哈達瑪閘，柱子只剩一根；最後一格是測量，右下角的小圖跑了一千次，全部落在一一。',
       '兩個輸入位元不是零零，所以這個黑盒子是平衡的；量子方法只問了一次，古典最壞要問三次。'],
      actions=[(0, 3.2, ('click', 'Deutsch')),
               (1, 0.6, ('click', '單步')), (1, 3.8, ('click', '單步')),
               (1, 6.0, ('click', '單步')), (1, 7.2, ('click', '單步')),
               (2, 0.6, ('click', '單步')), (2, 5.6, ('click', '單步'))],
      points=[('前兩格', '輔助位元翻成一，全部疊加'), ('黑盒子兩格', '柱子高度不變'), ('最後測量', '一千次都是一一')],
      shot=(3, 1.5)),
 dict(key='arrows', after=7, page='op', hash='interference', scene='3D 場景 8：干涉——3 位元模式（Deutsch–Jozsa）',
      title='動畫展示：八支箭頭的相長與相消', sub='三維動畫：干涉——三位元、八條路徑',
      sentences=[
       '打開三維動畫的干涉場景，切到三位元模式：起點分成八條路，中間八個小圓盤，各代表一種輸入。',
       '先選常數，永遠輸出零：八支金色箭頭全部朝右，在右邊的大圓裡頭尾相接，白色的總和箭頭最遠，量到零零零的機率是一。',
       '換成平衡的函數，最後一位是一的四支箭頭翻成朝左，頭尾相接走回起點，白色箭頭不見了，機率變成零。',
       '再換另一種平衡，朝左的位置不一樣，可是一樣四正四負、完全抵消；右下角的小圖也看得到，結果一定不是零零零。'],
      actions=[(0, 3.6, ('click', '3 位元')),
               (1, 1.0, ('click', '常數 f = 0')),
               (2, 1.2, ('click', '平衡 f = x')),
               (3, 1.0, ('click', '平衡 f = 奇'))],
      points=[('常數', '八支同向，機率一'), ('平衡', '四正四負，機率零'), ('換一種平衡', '一樣完全抵消')],
      shot=(3, 6.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q012'] 取用。"""

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

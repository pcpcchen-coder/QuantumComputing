"""Q125 量測 1 次與 1000 次 — v2 動畫展示段（格式見 ../demos.py 的說明）。

bc = animations/basic-circuits.html。量測卡按鈕 #m1「量測 1 次」、#m1000「量測 1,000 次」（setInterval 每 30 ms 加 40 次，約 0.75 秒跑完；
跑的時候再按會被 shotTimer 擋掉）、#mClear「清除」。量測會累加；go()（換步驟、換選項、換範例）會 clearShots()。
換範例（hashchange → selectScene → rebuild(true)）停在起點；#dots 的最後一個點（button:last-child）直接跳到最後一步。
「最近一次」綠框 #chip：只量一顆時寫成「q2 = 0」，量多顆時是整串位元；#verdict 只在最後一步出現。#hist 每列「次數（百分比）」，最下面「共 N 次；理論：…」。
- once：#ghz（預設 3 顆）最後一步：量測卡只有 000、111 兩列（理論各 50%）；連按量測 1 次，綠框是 000 或 111（隨機，旁白不說是哪個）。
  再換 #bv（預設密碼 101）最後一步：量測 1 次 → 綠框 101、verdict「→ 密碼 s = 101」、101「1（100.0%）」；再按一次仍是 101、100%。
  Q010、Q113–Q124 沒有在 #ghz、#bv 按過「量測 1 次」（Q114 只在 #superposition 按過）。
- pile：#teleport（預設 ψ = √¾|0⟩+½|1⟩）最後一步，只量 q2，理論「0 75%、1 25%」；量測 1 次 × 8（比例隨機大跳），再量測 1,000 次 × 3，
  「共 1,008 次」→「共 2,008 次」→「共 3,008 次」（總數是確定的；百分比隨機，旁白不念）。Q118、Q124 用過 #teleport，但沒有按過量測 1 次，也沒有累加。
op = animations/operation.html#readout（js/operation/07_readout.js「讀取與統計」，Q001–Q124 沒有用過）：
- readout：預設 θ = 70°、量 Z、「連續 shots」開（每秒 60 個）、積分時間 τ = 1.00 μs、「讀取誤差緩解」開。每個 shot 在 IQ 平面多一個點，依閾值（粉紅色平面）
  判成 0（藍）或 1（紅）。面板（#panel 捲到底才看得到 readout）：「理想 P(1) = 0.329」、「讀取保真度 F = 96.1%」；滑桿「積分時間 τ」設 0.1 → 兩團雲變胖重疊、
  F = 71.7%（改滑桿會清除統計）。關掉「讀取誤差緩解」→ 第四行「未緩解 P̂(1)」，期望值約 0.426（Node 以同一 shot() 程式蒙地卡羅 2000 輪 × 300 次：
  第 1 百分位 0.360，仍高於 0.329）；再打開 → 「緩解後 P̂(1)」用混淆矩陣反推（旁白不念數值）。
已用 Playwright 單張截圖確認以上畫面（scratchpad q125/shot1.js、shot2.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q125'

# 縮小並捲到範例標題，讓選項、電路和量測卡同時入鏡（同 Q124 bvparam）
_BC_FIT = ("document.body.style.zoom='0.62';"
           "document.querySelector('#sceneTitle').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-8);")
# 跳到最後一步
_LAST = ('sel', '#dots button:last-child')
# 換到密碼範例（hashchange 後重新捲到標題）
_TO_BV = ('js', "location.hash='bv';setTimeout(function(){" + _BC_FIT + "},200);")
# operation.html 左側面板捲到底並保持（readout 才會入鏡；行數變動時也不會被切掉，同 Q102）
_PIN = ('js', "(()=>{const pn=document.getElementById('panel');const f=()=>{pn.scrollTop=pn.scrollHeight;};f();"
              "clearInterval(window.__pin);window.__pin=setInterval(f,500);})()")

_LIST = [
 dict(key='once', after=4, page='bc', hash='ghz', scene='量子電路入門互動動畫：GHZ 態與 BV（量測 1 次）',
      title='動畫展示：只按一次量測', sub='三維動畫：量子電路入門——全零全一與密碼範例',
      sentences=[
       '打開線路入門動畫的範例四，三顆位元串成一條鏈；點最右邊的小圓點跳到最後一步，量測卡只剩全零和全一兩列。',
       '連按幾次量測一次，綠框裡的三個位元總是一起出現，不是全零就是全一，可是下一次是哪一個，誰也說不準。',
       '換到範例七的密碼範例，一樣跳到最後一步，按一次量測，綠框是一零一，下面寫著密碼就是一零一。',
       '再按一次還是一零一，比例一直是百分之百；答案集中在一個結果的線路，量一次就讀得出來。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 6.9, _LAST),
               (1, 1.6, ('sel', '#m1')), (1, 3.4, ('sel', '#m1')), (1, 5.2, ('sel', '#m1')), (1, 7.0, ('sel', '#m1')),
               (2, 0.3, _TO_BV), (2, 3.4, _LAST), (2, 5.4, ('sel', '#m1')),
               (3, 0.5, ('sel', '#m1'))],
      points=[('範例四', '不是全零就是全一'), ('量一次', '下一次是哪個說不準'), ('密碼範例', '量一次就讀出答案')], shot=(1, 8.0)),
 dict(key='pile', after=6, page='bc', hash='teleport', scene='量子電路入門互動動畫：隱形傳態（量測 1 次八下，再累加三次 1,000 次）',
      title='動畫展示：次數一路累加', sub='三維動畫：量子電路入門——隱形傳態的量測卡',
      sentences=[
       '打開隱形傳態範例，跳到最後一步；這裡只量編號二，灰色底寫著零占四分之三、一占四分之一。',
       '先連按八次量測一次，下面的百分比每按一次就大跳一下；才八次，就算剛好碰到四分之三，也只是碰巧，還說不準。',
       '再按量測一千次，次數一口氣累加上去，最下面的小字變成一千零八次，綠色條停到灰色底附近。',
       '再按兩次，總數到了三千零八次；這時再多量一千次，百分比只會小小移動，不再像一開始那樣大跳。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 2.6, _LAST),
               (1, 0.8, ('sel', '#m1')), (1, 1.4, ('sel', '#m1')), (1, 2.0, ('sel', '#m1')), (1, 2.6, ('sel', '#m1')),
               (1, 3.2, ('sel', '#m1')), (1, 3.8, ('sel', '#m1')), (1, 4.4, ('sel', '#m1')), (1, 5.0, ('sel', '#m1')),
               (2, 0.6, ('sel', '#m1000')),
               (3, 0.3, ('sel', '#m1000')), (3, 1.6, ('sel', '#m1000'))],
      points=[('量八次', '百分比大跳'), ('累加一千次', '停到灰色底附近'), ('三千多次', '只小小移動')], shot=(3, 6.0)),
 dict(key='readout', after=8, page='op', hash='readout', scene='3D 場景 7：讀取與統計（積分時間縮到最短、開關讀取誤差緩解）',
      title='動畫展示：多量也去不掉的偏差', sub='三維動畫：讀取與統計',
      sentences=[
       '換到三維動畫的讀取場景：每量一次，平台上就多一個點，閾值左邊判成零、塗成藍色，右邊判成一、塗成紅色。',
       '把積分時間拉到最短，兩團雲一下子變胖、疊在一起，左邊面板的讀取保真度從九成六掉到大約七成二。',
       '關掉讀取誤差緩解，面板改成未緩解的估計值，它比上面的理想機率高出一截；多量幾次，只會讓它穩穩偏在那裡。',
       '再打開緩解，面板用事先量好的混淆矩陣把結果反推回去；不過簡報提醒，做了緩解，需要的次數還會更多。'],
      actions=[(0, 0.2, _PIN),
               (1, 1.8, ('slider', '積分時間 τ', 0.1)),
               (2, 0.6, ('toggle', '讀取誤差緩解', False)),
               (3, 0.6, ('toggle', '讀取誤差緩解', True))],
      points=[('每個點', '一次量測'), ('積分時間太短', '兩團雲重疊'), ('讀取偏差', '多量也不會消失')], shot=(2, 6.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q125'] 取用。"""

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

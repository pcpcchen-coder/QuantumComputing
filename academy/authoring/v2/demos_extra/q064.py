"""Q064 模組專題：在模擬器跑我的線路 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（已讀原始碼，並以 1600×900 Chromium（swiftshader）截圖確認畫面位置，截圖在 /home/user/qwork/q064shots/）：
- op#circuit：animations/js/operation/06_circuit.js。範例按鈕「Grover 搜尋（2 位元，找 |11⟩）」（CIRCUITS.grover，第 42–51 行，
  8 欄：H、H｜CZ｜H、H｜X、X｜CZ｜X、X｜H、H｜量測），所以 ('click', 'Grover 搜尋') 以開頭比對；「單步 ▶」（第 172 行）；
  「加入雜訊（每閘 1%、讀取 3%）」是 ui.toggle 建的按鈕（core.js 第 354–355 行，class on），切換時若已有結果立即重抽（第 174 行 sample()）。
  量測欄跑 1000 次，右下插圖「量測 1000 shots 的結果（青線 = 理想機率）」（第 178–182 行），柱子橘色、理想線青色（op8.png）。
  理想時 11 為 1000 次、其他三個位置是平的；中間的三維振幅柱只剩 |11⟩ 一根（op8.png）。
  加入雜訊：12 個閘 → 1 − 0.99¹² = 11.4% 換成均勻隨機，再每顆 3% 翻轉；期望 00 ≈ 29、01 ≈ 54、10 ≈ 54、11 ≈ 862（1000 次中），
  截圖一次為 11: 863、10: 54、01: 48，三個矮柱都看得到、11 低於青線（op8n.png）。數字是頁面亂數，旁白不念。
- bc#deutsch：animations/basic-circuits.html 範例 6（SCENES id "deutsch"，第 419–445 行），4 步（X 輔助位元、兩顆 H、黑盒、q0 做 H）；
  選項「黑盒裡的函數」f(x)=0／f(x)=1／f(x)=x（預設）／f(x)=1−x，renderOpts() 建在 #opts .seg，第 2 個按鈕是 f(x)=1；
  換選項 → rebuild(false) 直接停在最後一步並清除量測。#bNext「下一步 ▶」、#m1000「量測 1,000 次」（第 194–224 行 markup）。
  f(x)=x：量測卡「1 1000（100.0%）」與「→ 平衡函數」；f(x)=1：「0 1000（100.0%）」與「→ 常數函數」（dj4m.png、djcm.png；機率 100%，結果固定）。
- bc#grover：同檔範例 8（第 471–513 行），選項「位元數」第 2 個按鈕「3 顆（N = 8）」，答案預設 101、輪數「最佳」= 2；
  換成 3 顆後停在「第 5 步 第 2 輪・擴散」，說明「答案的機率升到 94.5%」；振幅卡只有 |101⟩ 一根高柱（+.972），其他 −.088；
  量測卡列出 8 種結果，「101 94.5%」其餘「0.8%」（g3m.png）。量測次數與「最近一次」是亂數，旁白不念次數、不念「找到答案」標示。
  縮放 0.62 並捲到 #sceneTitle 時，選項在上、電路在中、振幅卡在左下、量測卡在右下（同 Q057 的 _BC_FIT）。
Q010、Q057、Q061 用過 op#circuit 的 Bell、GHZ、QFT；本課用 Grover 範例。bc 只用過 bell、ghz、teleport、interference、superposition；本課用 deutsch、grover。
"""
LESSON = 'Q064'

# basic-circuits.html 是一般網頁：縮小並捲到範例標題，讓選項、電路、振幅卡和量測卡同時入鏡
_BC_FIT = ("document.body.style.zoom='0.62';"
           "document.querySelector('#sceneTitle').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-8);")
_STEP = ('click', '單步')
_OPT2 = ('sel', '#opts .seg button:nth-child(2)')

_LIST = [
 dict(key='grover', after=6, page='op', hash='circuit', scene='3D 場景 6：量子線路——格羅弗搜尋（兩顆找 11）',
      title='動畫展示：兩顆格羅弗加上雜訊', sub='三維動畫：量子線路一步一步執行——格羅弗搜尋',
      sentences=[
       '換到三維動畫的量子線路場景，按格羅弗搜尋的範例，上方換成兩條線、八欄的線路，這是兩顆位元找一一的版本。',
       '連按八次單步，走到最右邊的量測欄；中間的柱子只剩一一那一根，其他三個位置都是平的。',
       '右下的小圖跑了一千次，只有一一一根橘色柱子，頂到青色的理想線，一次就找到答案。',
       '打開加入雜訊的開關，一一的柱子掉到青線下方，零零、零一、一零都冒出矮矮的小柱子，和程式裡的雜訊是同一個道理。'],
      actions=[(0, 4.4, ('click', 'Grover 搜尋')),
               (1, 0.2, _STEP), (1, 0.5, _STEP), (1, 0.8, _STEP), (1, 1.1, _STEP),
               (1, 1.4, _STEP), (1, 1.7, _STEP), (1, 2.0, _STEP), (1, 2.3, _STEP),
               (3, 0.8, ('toggle', '加入雜訊', True))],
      points=[('八次單步', '走到量測欄'), ('理想模擬', '只有 11 一根'), ('加入雜訊', '11 變矮、旁邊冒矮柱')], shot=(3, 7.0)),
 dict(key='deutsch', after=9, page='bc', hash='deutsch', scene='量子電路入門互動動畫：Deutsch 演算法',
      title='動畫展示：換一個題目', sub='三維動畫：量子電路入門——多伊奇問題',
      sentences=[
       '題目不一定要用格羅弗搜尋，也可以挑第十二堂的多伊奇問題；打開線路入門動畫的這個範例，黑盒裡預設是平衡函數。',
       '連按四次下一步：輔助位元先翻成一，兩顆都做哈達瑪閘，接著查一次黑盒，最後零號再做一次哈達瑪閘。',
       '按量測一千次，零號位元一千次都是一，右邊寫著平衡函數。',
       '把上方的黑盒換成永遠輸出一的常數函數，再量一千次，結果全部變成零，右邊改寫常數函數。'],
      actions=[(0, 0.2, ('js', _BC_FIT)),
               (1, 0.4, ('sel', '#bNext')), (1, 1.4, ('sel', '#bNext')), (1, 2.4, ('sel', '#bNext')), (1, 3.4, ('sel', '#bNext')),
               (2, 0.5, ('sel', '#m1000')),
               (3, 1.6, _OPT2), (3, 5.0, ('sel', '#m1000'))],
      points=[('四次下一步', '黑盒只查一次'), ('平衡函數', 'q0 全是 1'), ('常數函數', 'q0 全是 0')], shot=(3, 8.5)),
 dict(key='grover3', after=10, page='bc', hash='grover', scene='量子電路入門互動動畫：Grover 搜尋（三顆）',
      title='動畫展示：三顆的理想值', sub='三維動畫：量子電路入門——三顆格羅弗搜尋',
      sentences=[
       '回到線路入門動畫的格羅弗搜尋，把位元數改成三顆：八個抽屜，答案預設是一零一，畫面直接停在第二輪擴散。',
       '電路上是兩組標記和擴散；說明寫著答案的機率升到百分之九十四點五，左邊的振幅柱子只有一零一高高站著。',
       '按量測一千次，右邊列出八種結果，一零一的綠色條幾乎填滿整格，其他七種只有零星幾次。',
       '所以三顆就算沒有雜訊，也不是百分之百；程式裡理想模擬的一零一，大約九百七十次，報告要先寫下這個理想值。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 3.4, _OPT2),
               (2, 0.5, ('sel', '#m1000'))],
      points=[('改成三顆', '停在第二輪擴散'), ('理論機率', '101 是 94.5%'), ('沒有雜訊', '也不是 100%')], shot=(2, 6.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q064'] 取用。"""

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

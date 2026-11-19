"""Q120 範例 7：BV——查一次讀出整串密碼 — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html#bv（第 9 章）。第 8 步「自由實驗」#g9steps button:nth-child(8)（dur 0、不會自動接續）；控制項在 #g9extra：
密碼按鈕 [data-s9="0"…"7"]（000…111）；①–④ 是 [data-op9="H3"|"O"|"H3b"|"M"]；#g9reset「重設」（清空看板與柱子，密碼不變）。
選密碼只改 S.s，不會重設柱子；面板要先把 #g9extra 捲到頂端，按鈕與量測統計才會一起入鏡（同 Q105）。
動畫時間：H⊗3 1.6 秒、黑盒子 1.4 秒、量測 50 次約 2.8 秒。柱子：正振幅金色、負振幅紅色，標籤「+0.35 ・ 12.5%」。
看板（上方畫布）：黑盒子畫成虛線框「黑盒子 s = …」，密碼為 1 的那條線放一個 Z；s = 000 時框內空的。
Playwright 實拍（1600×900）：s = 000 → ① 八根 +0.35 → ② 虛線框內沒有 Z、柱子不變 → ③ 只剩 |000⟩ +1.00 → ④ 50/50 都是 000、左上角「量測最多的是 000（50/50 次），猜中 ✓」；
s = 111、重設後 ①② → 看板三條線都是 Z，001、010、100、111 四根變紅（奇數個 1）。
面板說明文字本身就寫著「值得試試：s = 000 時黑盒子什麼都不做，H⊗3 做兩次等於沒做，結果回到 000；s = 111 時三顆都被 Z，結果 111」。
Q105 用過第 8 步的 s = 101 ①②③④ 與「隨機（隱藏）」古典對決；本課改看 s = 000（H 做兩次＝沒做）與 s = 111 的紅色排法。

bc = animations/basic-circuits.html#bv（範例 7，教科書版：q0–q2 輸入、q3 輔助）。密碼按鈕在 #opts .seg，依序 s2、s1、s0（預設 101）；
改選項會停在最後一步（rebuild(false)）；#bFirst「⏮ 起點」、#bNext「下一步 ▶」、#m1000「量測 1,000 次」。
Playwright 實拍 s = 011（點第 1、2 個按鈕：101 → 001 → 011）：第 1 步只有 1000 一根 +1；第 2 步 16 根 ±.250、右邊 8 根（q3 = 1）整排朝下；
第 3 步黑盒子兩條 CNOT（q0→q3、q1→q3），左邊 8 根 + − − + + − − +（右邊 8 根相反），每根 6.3%；第 4 步只剩 0011 +.707（藍、朝上）與 1011 −.707（橘、朝下）；
量 1,000 次：011 1000 次、判定「→ 密碼 s = 011」。Q105 用過 bc#bv 的 101 逐步與改成 110；本課改用 011 從起點逐步看 16 根柱子。

op = animations/operation.html#circuit（js/operation/06_circuit.js）範例按鈕「Bernstein–Vazirani（秘密字串 101）」：五欄 X(q3)、全部 H、CX(0,3)+CX(2,3)、全部 H、量測；
「單步 ▶」一次一欄，到量測欄時抽 1000 shots，右下插圖「量測 1000 shots 的結果（青線 = 理想機率）」；理想時只有 101 一根、頂端碰到青線。
開關「加入雜訊（每閘 1%、讀取 3%）」切換時立刻重新抽樣：每個 shot 有 1 − 0.99^11 ≈ 10% 機會變成隨機結果，再每位 3% 讀錯；
實拍：101 降到八成多、其他結果都冒出矮柱子（次數隨機，旁白不念）。其他課（Q009、Q010）用過這個場景的干涉、Deutsch、貝爾態，沒有用過 BV。
已用 Playwright 單張截圖確認以上畫面與數值（scratchpad q120/shot_bc.js、shot_tr.js、shot_op.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q120'

_STEP8 = '#g9steps button:nth-child(8)'
_FIT = "document.getElementById('g9extra').scrollIntoView({block:'start'});"
# basic-circuits.html：縮小並捲到選項列，讓選項、電路、振幅與量測卡同時入鏡（同 Q113–Q119）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")


def _bit(n):
    """點密碼的第 n 個切換鈕（1 = s2、2 = s1、3 = s0）；頁面會停在最後一步"""
    return ('js', f"(function(){{var b=document.querySelector('#opts .seg button:nth-child({n})');window.__flash&&window.__flash(b);b.click();}})()")


_LIST = [
 dict(key='zero', after=7, page='tr', hash='bv', scene='Transmon 3D 第 9 章：BV 密碼——自由實驗（密碼 000 與 111）',
      title='動畫展示：哈達瑪閘做兩次', sub='三維動畫：BV 密碼——全零與全一的密碼',
      sentences=[
       '回到超導三維動畫的第九章，按第八步自由實驗，把密碼選成零零零，再按一號，八根金色柱子都升到正零點三五。',
       '按二號黑盒子，看板上的虛線框裡空空的，一個相位翻轉閘都沒有，八根柱子一根也沒有翻紅。',
       '接著按三號，第二次哈達瑪閘把第一次整個抵銷，柱子縮回最左邊那一根；按四號量五十次，五十次都是零零零。',
       '換成一一一，按重設，再按一號和二號：三條線都放上相位翻轉閘，有奇數個一的四根翻成紅色，連一一一自己也在裡面。'],
      actions=[(0, 2.4, ('sel', _STEP8)), (0, 3.4, ('js', _FIT)), (0, 6.6, ('sel', '[data-s9="0"]')),
               (0, 8.6, ('sel', '[data-op9="H3"]')),
               (1, 0.8, ('sel', '[data-op9="O"]')),
               (2, 0.6, ('sel', '[data-op9="H3b"]')), (2, 7.2, ('sel', '[data-op9="M"]')),
               (3, 0.6, ('sel', '[data-s9="7"]')), (3, 1.8, ('id', 'g9reset')),
               (3, 3.2, ('sel', '[data-op9="H3"]')), (3, 5.2, ('sel', '[data-op9="O"]'))],
      points=[('密碼零零零', '黑盒子裡空空的'), ('兩次哈達瑪閘', '回到零零零'), ('密碼一一一', '奇數個一的翻紅')], shot=(3, 10.5)),
 dict(key='noise', after=8, page='op', hash='circuit', scene='3D 場景 6：量子線路——一步一步執行（Bernstein–Vazirani）',
      title='動畫展示：加上雜訊的密碼', sub='三維動畫：量子線路——理想結果和雜訊',
      sentences=[
       '換到三維動畫的量子線路場景，選秘密字串一零一那一組，按五次單步：翻轉閘、一排哈達瑪閘、黑盒子、再一排哈達瑪閘，最後到量測欄。',
       '右下角的小圖是跑一千次的結果，只有一零一一根柱子，高度剛好碰到青色的理想線。',
       '打開加入雜訊的開關，每個閘有百分之一、每次讀取有百分之三的機會出錯，一零一的柱子矮了一截，其他結果都冒出小柱子。',
       '答案還是最高的那一根；真實的量子電腦就是這樣，要跑很多次，挑出最突出的結果，不能只看一次就下結論。'],
      actions=[(0, 4.4, ('click', 'Bernstein')),
               (0, 7.4, ('click', '單步')), (0, 8.8, ('click', '單步')), (0, 10.4, ('click', '單步')),
               (0, 11.8, ('click', '單步')), (0, 13.6, ('click', '單步')),
               (2, 1.6, ('toggle', '加入雜訊', True))],
      points=[('理想模擬', '只有一零一一根'), ('加入雜訊', '其他結果冒出來'), ('跑很多次', '挑最突出的')], shot=(3, 2.0)),
 dict(key='mykey', after=9, page='bc', hash='bv', scene='量子電路入門互動動畫：BV（自訂密碼 011，從起點逐步播放）',
      title='動畫展示：自訂密碼零一一', sub='三維動畫：量子電路入門——十六根柱子逐步看',
      sentences=[
       '打開線路入門動畫的範例七，密碼預設是一零一；點最左邊那格改成零、中間那格改成一，上方就變成零一一。',
       '按起點，再按兩次下一步：輔助位元先翻成一，接著四顆一起做哈達瑪閘，十六根柱子一樣大小，右邊八根整排朝下。',
       '第三步，黑盒子裡兩條受控反閘從編號零和編號一連到輔助位元，左邊八根排成上下下上、上下下上，正是零一一的指紋。',
       '最後一步只剩兩根柱子，按量測一千次，一千次都是零一一，下面寫著密碼等於零一一。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 7.2, _bit(1)), (0, 9.4, _bit(2)),
               (1, 0.6, ('sel', '#bFirst')), (1, 3.2, ('sel', '#bNext')), (1, 6.4, ('sel', '#bNext')),
               (2, 0.4, ('sel', '#bNext')),
               (3, 0.4, ('sel', '#bNext')), (3, 4.2, ('sel', '#m1000'))],
      points=[('自訂密碼', '一零一改成零一一'), ('第三步', '左邊八根是指紋'), ('量測一千次', '全部是零一一')], shot=(2, 9.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q120'] 取用。"""

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

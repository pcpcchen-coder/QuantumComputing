"""Q122 Grover 三位元：轉太多會轉過頭 — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html#grover（第 7 章）。第 8 步「自由實驗」#g7steps button:nth-child(8)（dur 0、不會自動接續）；控制項在 #g7extra：
答案 [data-ans="3"]（11）、#g7run「一鍵 Grover」（g7Reset 後 H、H、CZ、擴散、量測 50 次；答案 11 不需要 X；約 8.2 秒）、[data-op="O"]「Oracle」、[data-op="D"]「擴散」。
一鍵 Grover 的擴散帶 mean: true，金色平均線之後一直顯示。柱子正振幅金色、負振幅紅色，標籤「+0.50 ・ 25%」。動畫時間：Oracle 1.0 秒、擴散 2.4 秒。
第 8 步的說明文字寫著「一鍵 Grover 後再按 Oracle、擴散：轉過頭」。第 6 步「轉過頭」的時間軸字幕與面板寫「四個振幅都變成 −½」，和程式不符（實際答案 +½、其他 −½），所以本課不用第 6 步。
Playwright 實拍（1600×900）：答案 11 → 一鍵 Grover：|11⟩ +1.00 ・ 100%、「平均 +0.25」、量測 50 次 11 有 50 次 → Oracle：|11⟩ −1.00、「平均 −0.25」
→ 擴散：|11⟩ +0.50（金）、其他 −0.50（紅）、各 25%、平均 −0.25 → Oracle：四根都是 −0.50、平均 −0.50 → 擴散：四根不動 → Oracle：|11⟩ +0.50、平均 −0.25 → 擴散：|11⟩ −1.00 ・ 100%。
Q106 用過第 7 章步驟 1、3、4、5；Q121 用過第 8 步手動送閘、答案 00、「沒有標記的擴散」；本課改成一鍵 Grover 之後再多做三輪。

op = animations/operation.html#grover（js/operation/09_grover.js）。滑桿「量子位元數 n」拉到 3（N = 8）、「答案（標記的項目）」拉到 5（改值都會 setup() 重設；先改 n 再改答案，否則答案滑桿顯示 11、實際 mark = 7）；
「完整一輪」= Oracle，0.7 秒後擴散。右下插圖：左邊金色指針每輪轉 2θ（舊的變淡），右邊「P(成功) vs 輪數」金色曲線 sin²((2x + 1)θ)，橫軸 0 到 km = max(2 × 最佳 + 1, 3) = 5，
白點是目前輪數。Playwright 實拍 n = 3：讀數 P = 0.125 → 0.781 → 0.945 → 0.330 → 0.012（八根全是藍色、答案那根最矮，白點在谷底）→ 0.548（白點在右端往上）。
Q001 用過本場景 n = 4 按「完整一輪」四次；Q121 用過答案 6 分開按標記與擴散兩輪；本課改成 n = 3、五輪，看右下曲線起伏。

bc = animations/basic-circuits.html#grover（範例 8）。#opts 依序三組 .seg：位元數、答案、重複輪數。位元數按第 2 鈕「3 顆（N = 8）」後，第 2 組換成「答案（q2 q1 q0）」三鈕（預設 101），
點第 1 鈕 q2 → 001；第 3 組第 4 鈕「3 輪」；改選項會停在最後一步，按 #bFirst「⏮ 起點」回開頭，#bNext「下一步 ▶」；長條換步 0.65 秒內插，綠色虛線（.mean）跟著內插；正振幅藍、負振幅橘。
Playwright 實拍答案 001、3 輪：第 1 步八根 +.354 → 第 3 步 001 +.884、其他 +.177、說明「答案的機率升到 78.1%」→ 第 5 步 +.972、其他 −.088、94.5%
→ 第 6 步 001 −.972、八根全是負的、平均 −.199 → 第 7 步 +.575、其他 −.309、說明「平均值變成負的，翻過去反而變小：答案的機率降到 33%。轉過頭了」。
Q106 用過 bc#grover 換答案 10、三顆兩輪、直接切三輪；Q121 用過兩顆答案 01 逐步看虛線；本課改成三顆、答案 001、三輪從起點逐步看。
已用 Playwright 單張截圖確認以上畫面與數值（scratchpad q122/shot_tr.js、shot_op.js、shot_bc.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q122'

_STEP8 = '#g7steps button:nth-child(8)'
_FIT = "document.getElementById('g7extra').scrollIntoView({block:'start'});"
# basic-circuits.html：縮小並捲到選項列，讓選項、電路、振幅與量測卡同時入鏡（同 Q113–Q121）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")

_LIST = [
 dict(key='twobit', after=6, page='tr', hash='grover', scene='Transmon 3D 第 7 章：振幅長條——自由實驗（答案 11，一鍵 Grover 後再多做三輪）',
      title='動畫展示：兩顆位元也會轉過頭', sub='三維動畫：振幅長條——多做一輪',
      sentences=[
       '這次到超導三維動畫第七章的自由實驗：按第八步，答案選一一，再按一鍵格羅弗，讓兩顆位元先做完一輪。',
       '一一那根衝到正一，右邊量五十次全是一一；接著自己多做一輪，先按標記，一一翻成紅色的負一。',
       '再按擴散，一一掉回正零點五，其他三根變成紅色的負零點五，四個結果又是各四分之一，平均線停在負零點二五。',
       '再做一輪，四根全是負零點五，擴散翻不動；再做一輪，一一又回到百分之百，只是柱子朝下，變成負一。'],
      actions=[(0, 4.0, ('sel', _STEP8)), (0, 4.4, ('js', _FIT)), (0, 5.6, ('sel', '[data-ans="3"]')),
               (0, 6.6, ('id', 'g7run')),
               (1, 7.6, ('sel', '[data-op="O"]')),
               (2, 0.6, ('sel', '[data-op="D"]')),
               (3, 0.4, ('sel', '[data-op="O"]')), (3, 1.8, ('sel', '[data-op="D"]')),
               (3, 5.0, ('sel', '[data-op="O"]')), (3, 6.4, ('sel', '[data-op="D"]'))],
      points=[('一鍵 Grover', '一輪就 100%'), ('多做一輪', '回到各 25%'), ('再兩輪', '回到 100%，振幅 −1')], shot=(2, 8.0)),
 dict(key='curve', after=7, page='op', hash='grover', scene='3D 場景 9：Grover 搜尋——三顆位元連做五輪（右下成功機率曲線）',
      title='動畫展示：成功機率一起一落', sub='三維動畫：Grover 搜尋——P(成功) vs 輪數',
      sentences=[
       '換到三維動畫的格羅弗場景，把量子位元數拉到三，下面剩八根柱子，再把答案滑桿拉到五，青綠框移到五號。',
       '看右下角的插圖：左邊是金色指針，右邊是成功機率對輪數的曲線；按完整一輪兩次，白點爬到頂端附近，讀數零點九四五。',
       '再按一次，白點滑下坡，只剩零點三三；第四次，八根柱子全翻到下面，答案那根縮得最矮，機率零點零一二。',
       '按第五次，白點又往上爬到零點五四八：指針每輪往同一個方向轉同樣的角度，轉過答案以後繼續轉，靠近答案的反方向時機率又升高，就這樣一起一落。'],
      actions=[(0, 4.6, ('slider', '量子位元數 n', 3)), (0, 8.0, ('slider', '答案（標記的項目）', 5)),
               (1, 6.6, ('click', '完整一輪')), (1, 9.0, ('click', '完整一輪')),
               (2, 0.4, ('click', '完整一輪')), (2, 4.0, ('click', '完整一輪')),
               (3, 0.5, ('click', '完整一輪'))],
      points=[('兩輪', '白點在頂端，0.945'), ('四輪', '掉到 0.012'), ('五輪', '又爬回 0.548')], shot=(2, 9.5)),
 dict(key='rounds3', after=9, page='bc', hash='grover', scene='量子電路入門互動動畫：Grover（3 顆位元、答案 001、3 輪，從起點逐步看）',
      title='動畫展示：三輪一步一步看', sub='三維動畫：量子電路入門——三顆位元的平均值虛線',
      sentences=[
       '回到線路入門動畫的範例八：位元數選三顆，點一下編號二那一格，答案換成零零一，輪數選三輪，再按起點。',
       '按下一步，八根藍色柱子一樣高；再按兩次，第一輪的標記和擴散做完，零零一冒出來，說明寫著百分之七十八點一。',
       '再按兩次做完第二輪，答案升到百分之九十四點五，其他七根變成小小的橘色，掉到零的下面。',
       '第三輪一標記，八根全是橘色，綠色虛線也沉到零下；再按擴散，答案只剩百分之三十三，說明寫著轉過頭了。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 3.2, ('sel', '#opts div.seg:nth-of-type(1) button:nth-child(2)')),
               (0, 5.6, ('sel', '#opts div.seg:nth-of-type(2) button:nth-child(1)')),
               (0, 7.4, ('sel', '#opts div.seg:nth-of-type(3) button:nth-child(4)')), (0, 8.8, ('sel', '#bFirst')),
               (1, 0.4, ('sel', '#bNext')), (1, 3.2, ('sel', '#bNext')), (1, 5.0, ('sel', '#bNext')),
               (2, 0.4, ('sel', '#bNext')), (2, 2.0, ('sel', '#bNext')),
               (3, 0.4, ('sel', '#bNext')), (3, 5.6, ('sel', '#bNext'))],
      points=[('第 1 輪', '78.1%'), ('第 2 輪', '94.5%，其他掉到零下'), ('第 3 輪', '虛線沉到零下，掉到 33%')], shot=(3, 9.5)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q122'] 取用。"""

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

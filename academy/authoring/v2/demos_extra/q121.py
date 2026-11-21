"""Q121 範例 8：Grover——對平均值翻轉 — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html#grover（第 7 章）。第 8 步「自由實驗」#g7steps button:nth-child(8)（dur 0、不會自動接續）；控制項在 #g7extra：
答案 [data-ans="0"…"3"]（00…11）；[data-op="H0"]「H₁」、[data-op="H1"]「H₂」、[data-op="O"]「Oracle」、[data-op="D"]「擴散」；#g7meas「量測 50 次」。
按「擴散」時 S.showMean = true，金色平均線與標籤「平均 +0.50」淡入，之後一直顯示（只有重設才關）；平均線跟著目前振幅移動。
動畫時間：H 1.0 秒、Oracle 1.0 秒、擴散 2.4 秒（先 0.7 秒讓平均線出現）、量測 50 次約 2.8 秒。柱子：正振幅金色、負振幅紅色，標籤「+0.50 ・ 25%」。
Playwright 實拍（1600×900）：答案 00 → H₁、H₂ 四根 +0.50 → 先按擴散：平均線「平均 +0.50」貼著柱頂、四根不動 → Oracle：|00⟩ 紅色 −0.50、「平均 +0.25」
→ 擴散：|00⟩ +1.00 ・ 100%、其他 +0.00 → 量測 50 次：00 有 50 次。
Q106 用過第 7 章步驟 1、3、4、5（答案 10 的導覽）；本課改用第 8 步自由實驗、答案 00，並先做「沒有標記的擴散」。

op = animations/operation.html#grover（js/operation/09_grover.js）。滑桿「量子位元數 n」預設 4（N = 16）、「答案（標記的項目）」（改值會 setup() 重設）；
按鈕「② Oracle」「③ 擴散」分開按；粉紅色半透明平均面只在 phase === 'oracle' 時顯示；正振幅金色 0xe0a54a、負振幅藍色 0x4f8cff；答案柱底下青綠框、上方標籤「答案」。
Playwright 實拍答案 6：Oracle → 讀數「已做 Oracle，粉紅面 = 平均振幅」P = 0.063；擴散 → P = 0.473（答案 +0.6875、其他 +0.1875）；
第二次 Oracle → 答案 −0.6875，平均面 +0.133；擴散 → P = 0.908（答案 +0.953）。右下插圖有「P(成功) vs 輪數」曲線（之後會下降），旁白不提，留給 Q122。
Q001 用過本場景十六根柱子按「完整一輪」四次；本課改成標記和擴散分開按、看粉紅平均面、只做兩輪。

bc = animations/basic-circuits.html#grover（範例 8）。#opts 依序三組 .seg：位元數、答案（q1 q0）、重複輪數；答案按鈕文字「q1=1」「q0=1」（預設 11），
點 q1 那格 → 01，改選項會停在最後一步（rebuild(false)）；#bFirst「⏮ 起點」、#bNext「下一步 ▶」、#m1000「量測 1,000 次」；長條換步 0.65 秒內插，綠色虛線（.mean）跟著內插。
Playwright 實拍答案 01：起點 +1.000 0 0 0（平均 +.250）→ 第 1 步四根 +.500（平均 +.500）→ 第 2 步 01 −.500（橘、朝下），平均 +.250 →
第 3 步 0 +1.000 0 0 → 量 1,000 次：01 1000 次、「→ 找到答案 ✓」。Q106 用過 bc#grover 的換答案 10（直接跳最後一步）、三顆兩輪、三輪；本課改成答案 01 從起點逐步看綠色虛線。
已用 Playwright 單張截圖確認以上畫面與數值（scratchpad q121/shot_tr.js、shot_op.js、shot_bc.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q121'

_STEP8 = '#g7steps button:nth-child(8)'
_FIT = "document.getElementById('g7extra').scrollIntoView({block:'start'});"
# basic-circuits.html：縮小並捲到選項列，讓選項、電路、振幅與量測卡同時入鏡（同 Q113–Q120）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")

_LIST = [
 dict(key='flat', after=4, page='tr', hash='grover', scene='Transmon 3D 第 7 章：振幅長條——自由實驗（答案 00，先擴散、再標記）',
      title='動畫展示：沒有標記，擴散不動', sub='三維動畫：振幅長條——金色平均線',
      sentences=[
       '這次到超導三維動畫第七章的自由實驗裡操作：按第八步，答案選零零，接著按哈達瑪閘一號和二號，四根金色柱子都到正零點五。',
       '先不標記，直接按擴散：金色的平均線出現在正零點五，剛好貼著柱子頂端，翻完四根一動也不動。',
       '接著按標記，零零那根翻成紅色的負零點五，平均線跟著降到正零點二五。',
       '再按一次擴散，三根掉到零，零零衝到正一；最後按量測五十次，五十次都是零零。'],
      actions=[(0, 4.8, ('sel', _STEP8)), (0, 5.3, ('js', _FIT)), (0, 6.4, ('sel', '[data-ans="0"]')),
               (0, 8.2, ('sel', '[data-op="H0"]')), (0, 9.4, ('sel', '[data-op="H1"]')),
               (1, 2.0, ('sel', '[data-op="D"]')),
               (2, 0.9, ('sel', '[data-op="O"]')),
               (3, 0.6, ('sel', '[data-op="D"]')), (3, 4.6, ('id', 'g7meas'))],
      points=[('先按擴散', '四根都在平均線上，不動'), ('按標記', '平均降到 +0.25'), ('再按擴散', '00 衝到 +1，50 次都是 00')], shot=(3, 7.8)),
 dict(key='sixteen', after=8, page='op', hash='grover', scene='3D 場景 9：Grover 搜尋——標記與擴散分開按（16 個選項）',
      title='動畫展示：十六個選項的平均面', sub='三維動畫：Grover 搜尋——粉紅色平均面',
      sentences=[
       '換到三維動畫的格羅弗場景，十六根柱子代表十六個選項；把答案滑桿拉到六，青綠色的框就移到編號六那一根。',
       '這次把標記和擴散分開按：先按標記，答案那根翻到下面變成藍色，粉紅色的平均面只比其他柱子低一點點。',
       '再按擴散，答案只翻到正零點六九，機率大約四成七，其他十五根都矮了一點；離平均不夠遠，一輪拉不滿。',
       '第二輪再按標記，答案翻到負零點六九，離平均面比上一輪遠得多；再按擴散，答案升到零點九五，讀數的機率變成零點九零八。'],
      actions=[(0, 6.2, ('slider', '答案（標記的項目）', 6)),
               (1, 3.4, ('click', '② Oracle')),
               (2, 0.6, ('click', '③ 擴散')),
               (3, 0.6, ('click', '② Oracle')), (3, 6.8, ('click', '③ 擴散'))],
      points=[('第一次標記', '平均面只低一點點'), ('一輪之後', '答案約 47%'), ('第二輪', '離平均更遠，升到 90.8%')], shot=(3, 11.5)),
 dict(key='dashed', after=9, page='bc', hash='grover', scene='量子電路入門互動動畫：Grover（答案 01，從起點逐步看平均值虛線）',
      title='動畫展示：綠色虛線一步一步看', sub='三維動畫：量子電路入門——平均值虛線',
      sentences=[
       '打開線路入門動畫的範例八，答案預設是一一，點一下編號一那一格，答案就換成零一，再按起點。',
       '按下一步，四根藍色柱子一樣高，綠色虛線從四分之一升上來，剛好貼著柱子頂端。',
       '再按下一步，零一那根翻到下面變成橘色，綠色虛線跟著往下滑，停在四分之一的高度。',
       '最後一步擴散，三根藍色柱子縮成零，零一翻上來頂到最高；按量測一千次，一千次都是零一，旁邊寫著找到答案。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 5.0, ('sel', '#opts div.seg:nth-of-type(2) button:nth-child(1)')),
               (0, 8.8, ('sel', '#bFirst')),
               (1, 0.5, ('sel', '#bNext')),
               (2, 0.5, ('sel', '#bNext')),
               (3, 0.5, ('sel', '#bNext')), (3, 5.8, ('sel', '#m1000'))],
      points=[('第一步', '虛線貼著四根柱頂'), ('標記', '虛線滑到 ¼'), ('擴散', '01 頂到最高，1000 次都是 01')], shot=(3, 9.5)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q121'] 取用。"""

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

"""Q119 範例 6：Deutsch——紅綠球搖獎機 — v2 動畫展示段（格式見 ../demos.py 的說明）。

bc = animations/basic-circuits.html#deutsch（淺色主題：正振幅 --pos 藍、負振幅 --neg 橘；4 根柱子 |00⟩ |01⟩ |10⟩ |11⟩，字串 |q1 q0⟩；只量 q0；
最後一步量測時出現綠字判定「→ 常數函數」或「→ 平衡函數」；第 1–3 步量測不出現判定）。
選項「黑盒裡的函數」#opts .seg button:nth-child(n)：1 = f(x)=0、2 = f(x)=1、3 = f(x)=x（預設）、4 = f(x)=1−x。
按「不同的」選項會 rebuild(false)：停在最後一步（步驟 4 / 4）、量測清除；#dots 有 5 個圓點（起點＋4 步），nth-child(4) = 第 3 步（問完黑盒子、最後的 H 之前）。
按鈕 id：#bNext「下一步 ▶」、#m1000「量測 1,000 次」（約 0.8 秒跑完）。
Playwright 實拍（1600×900，zoom 0.8）第 4 步振幅：f=0 |00⟩ +.707 藍（朝上）、|10⟩ −.707 橘（朝下）；f=1 |00⟩ −.707 橘、|10⟩ +.707 藍（上下顛倒）；
f=x |01⟩ +.707 藍、|11⟩ −.707 橘；f=1−x |01⟩ −.707 橘、|11⟩ +.707 藍。量 1,000 次：f=0、f=1 全部 0「→ 常數函數」；f=x、f=1−x 全部 1「→ 平衡函數」。
第 3 步：f=0 (|00⟩ + |01⟩ − |10⟩ − |11⟩)/2、f=x (|00⟩ − |01⟩ − |10⟩ + |11⟩)/2，理論 q0 0、1 各 50%（實拍 531／469、505／495，隨機，旁白不念）；
f=x 第 3 步按下一步再量 1,000 次：1000 次都是 1、「→ 平衡函數」。
Q107 用過 bc#deutsch 只選 f(x)=1−x 逐步看 Bloch 球；本課改看四種函數最後一步的柱子位置與量測（four），以及最後的 H 之前量測（skip）。
op = animations/operation.html#interference（js/operation/08_interference.js）模式 B「3 位元：8 條路徑（Deutsch–Jozsa）」：
  中間 8 個圓圈的金色箭頭朝右 = +、朝左 = −；右上金字 P(000)；右下插圖「最後量測的機率分佈（8 種結果）」（000 金色、其他藍色）；
  面板 readout「常數函數：完全相長／平衡函數：完全相消　（古典最壞要查 2ⁿ⁻¹+1 = 5 次）」。切到模式 B 時預設是「平衡 f = x₀」。
  實拍：常數 f = 1 → 8 支箭頭全部朝左、P(000) = 1.00、插圖只有 000 一根；平衡 f = x₀ → 箭頭一右一左交錯、P(000) = 0.00、插圖只有 001；
  平衡 f = 奇偶 → 箭頭另一種排法（000 右、001 左、010 左、011 右…）、P(000) = 0.00、插圖只有 111。
  面板比視窗高，切到模式 B 後把 #panel 捲到底，函數按鈕與 readout 才同時入鏡。
  Q006 用過模式 B 的「常數 f = 0」「平衡 f = x」並描述箭頭頭尾相接；本課改看「常數 f = 1」（全部反向仍百分之百）與插圖落點、「平衡 f = 奇偶」。
已用 Playwright 單張截圖確認以上畫面與數值（scratchpad q119/shot119.js、shot119b.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q119'

# basic-circuits.html：縮小並捲到選項列，讓選項、電路、振幅與量測卡同時入鏡（同 Q113–Q118）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")
# operation.html：面板捲到底
_OP_FIT = "(()=>{const p=document.getElementById('panel');if(p)p.scrollTop=p.scrollHeight;})();"


def _opt(n):
    """點「黑盒裡的函數」第 n 個選項（頁面會跳到最後一步、清除量測）"""
    return ('js', f"(function(){{var b=document.querySelector('#opts .seg button:nth-child({n})');window.__flash&&window.__flash(b);b.click();}})()")


_DOT3 = ('sel', '#dots button:nth-child(4)')   # 第 3 步：問完黑盒子、最後的 H 之前

_LIST = [
 dict(key='skip', after=5, page='bc', hash='deutsch', scene='量子電路入門互動動畫：Deutsch（最後的哈達瑪閘之前先量）',
      title='動畫展示：少了最後一步會怎樣', sub='三維動畫：量子電路入門——問完黑盒子就量',
      sentences=[
       '打開線路入門動畫的範例六，選最左邊兩顆都紅的函數，再點右邊第四個小圓點，停在問完黑盒子的那一步。',
       '這時按量測一千次，零和一的綠色條差不多一樣多，看不出這是常數機器。',
       '換成先紅後綠的平衡函數，同樣停在這一步量一千次，還是一半一半，兩台機器看起來一模一樣。',
       '按下一步，對編號零做最後的哈達瑪閘，再量一千次，一千次全部是一，下面出現綠字寫著平衡函數。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 4.0, _opt(1)), (0, 7.6, _DOT3),
               (1, 1.0, ('sel', '#m1000')),
               (2, 0.4, _opt(3)), (2, 3.0, _DOT3), (2, 4.8, ('sel', '#m1000')),
               (3, 0.4, ('sel', '#bNext')), (3, 5.6, ('sel', '#m1000'))],
      points=[('問完黑盒子就量', '零和一各約一半'), ('常數、平衡', '這時看起來一樣'), ('最後的哈達瑪閘', '一千次都是一')], shot=(3, 9.5)),
 dict(key='four', after=6, page='bc', hash='deutsch', scene='量子電路入門互動動畫：Deutsch（四種函數輪流比較最後一步）',
      title='動畫展示：四台機器的判讀表', sub='三維動畫：量子電路入門——四種黑盒子跑完的柱子',
      sentences=[
       '回到範例六，直接比較四台機器跑完的樣子；選兩顆都紅，頁面跳到最後一步，零零那根朝上，一零那根朝下。',
       '按量測一千次，全部是零，綠字寫著常數函數；換成兩顆都綠，還是同樣兩根柱子，只是上下顛倒。',
       '再量一千次，仍然全部是零；換成先紅後綠，柱子搬到零一和一一，量一千次全部是一，綠字改成平衡函數。',
       '最後選先綠後紅，柱子位置不變、上下又顛倒，量起來還是全部是一：判讀只看柱子站在哪兩格，不看朝上朝下。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 5.2, _opt(1)),
               (1, 0.3, ('sel', '#m1000')), (1, 5.4, _opt(2)),
               (2, 0.3, ('sel', '#m1000')), (2, 2.8, _opt(3)), (2, 7.0, ('sel', '#m1000')),
               (3, 0.4, _opt(4)), (3, 5.0, ('sel', '#m1000'))],
      points=[('常數兩台', '柱子在零零、一零，量到零'), ('平衡兩台', '柱子在零一、一一，量到一'), ('上下顛倒', '整體負號，不影響判讀')], shot=(3, 9.0)),
 dict(key='eight', after=7, page='op', hash='interference', scene='3D 場景 8：干涉（3 位元：8 條路徑）',
      title='動畫展示：八顆球的落點', sub='三維動畫：加速的關鍵——八條路匯到全零',
      sentences=[
       '換到三維動畫的干涉場景，切到三個位元、八條路的模式；左邊面板最下面寫著，古典最壞要查五次。',
       '選常數函數等於一，也就是八顆都綠：八個圓圈裡的箭頭全部朝左，右下角的小圖只剩全零那一根柱子，頂到最高。',
       '換成第一種平衡函數，箭頭一右一左交錯，上方全零的機率變成零，右下角的柱子跳到零零一。',
       '再換成按奇偶分的平衡函數，箭頭換了一種排法，柱子跳到一一一；平衡機器的落點會變，但永遠不在全零。'],
      actions=[(0, 2.8, ('click', '3 位元')), (0, 3.4, ('js', _OP_FIT)),
               (1, 0.4, ('click', '常數 f = 1')),
               (2, 0.4, ('click', '平衡 f = x')),
               (3, 0.4, ('click', '平衡 f = 奇偶'))],
      points=[('八顆都綠', '箭頭同向，全零百分之百'), ('第一種平衡', '落在零零一'), ('奇偶平衡', '落在一一一，仍不是全零')], shot=(3, 6.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q119'] 取用。"""

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

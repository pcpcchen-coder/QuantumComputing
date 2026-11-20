"""Q117 範例 4：GHZ——CNOT 一路串下去 — v2 動畫展示段（格式見 ../demos.py 的說明）。

bc = animations/basic-circuits.html#ghz（淺色主題：正振幅 --pos 藍；GHZ 範例沒有 Bloch 球（build 沒給 bloch），量測卡只列理論機率不為 0 的結果）。
選項「位元數」#opts .seg button:nth-child(n)：1 = 3 顆（預設，3 步：H、CNOT q0→q1、CNOT q1→q2）、2 = 4 顆（4 步，多 CNOT q2→q3）。
按「不同的」選項會 rebuild(false)：頁面停在最後一步、量測清除。3 顆時 8 根柱子 |000⟩…|111⟩（下面寫振幅 +.707 與 50%）；
4 顆時 16 根細柱（.bars.dense：標籤 0000…1111 不加 ket、振幅數字隱藏，只寫百分比）。按鈕 id：#bFirst「⏮ 起點」、#bNext「下一步 ▶」、#m1000「量測 1,000 次」。
- chain3：3 顆從起點走三步：H → |000⟩、|001⟩ 兩根藍柱 +.707；CNOT q0→q1 → |001⟩ 那根移到 |011⟩（650 ms 內插）；CNOT q1→q2 → 移到最右邊 |111⟩；
  |ψ⟩ = (|000⟩ + |111⟩) / √2；量測 1,000 次只列 000、111 兩列（灰底理論 50%、綠色實際次數；次數隨機，旁白不念）。
- four：選 4 顆 → 跳到最後一步：電路多一條 q3 線與 CNOT q2→q3；16 根細柱只剩最左 0000、最右 1111，各寫 50%；
  再按起點逐步：H → 0000、0001；CNOT → 0011；CNOT → 0111；CNOT → 1111（第二根柱子一路往右跳）。不量測。
  Q008 只在 bc#bell 量過兩顆，Q116 用 bc#bell 四種；GHZ 範例在先前各課的動畫段都沒用過。
op = animations/operation.html#register（js/operation/04_register.js）：滑桿「量子位元數 n」拉到 3 會重建場景（重設成 |000⟩）；
上排 Bloch 球由左到右是 q2、q1、q0；左下讀數「各量子位元 Bloch 長度：q0 …，q1 …，q2 …」與「無糾纏（可分離態）…」／粉紅色「有糾纏：…」。
按鈕文字（record_demo.js 用 startsWith 比對）：「目標 q0」「目標 q1」「目標 q2」「H」「CNOT（控制 = 目標+1 → 目標）」。
- bind：目標 q2 → H：0.71 |000⟩ + 0.71 |100⟩，長度 1.00、1.00、1.00，無糾纏（q2 的向量倒到 +x）；
  目標 q1 → CNOT（控制 q2 → 目標 q1）：0.71 |000⟩ + 0.71 |110⟩，長度 q0 1.00、q1 0.00、q2 0.00，有糾纏（左邊兩支縮成一點，右邊 q0 仍指向 |0⟩）；
  目標 q0 → CNOT（控制 q1 → 目標 q0）：0.71 |000⟩ + 0.71 |111⟩，三個都是 0.00。Q116 用同一場景做兩顆；本段是三顆，看鏈子一節一節接上。
已用 Playwright（1600×900；bc zoom 0.8）實拍確認以上畫面與數值（scratchpad q117/shot117.js）。
"""

LESSON = 'Q117'

# basic-circuits.html 是一般網頁：縮小並捲到選項列，讓選項、電路、振幅與量測卡同時入鏡（同 Q113–Q116）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")


def _opt(n, first=False):
    """點「位元數」第 n 個選項（頁面會跳到最後一步）；first=True 時立刻再按「起點」回到第 0 步"""
    tail = "document.getElementById('bFirst').click();" if first else ''
    return ('js', f"(function(){{var b=document.querySelector('#opts .seg button:nth-child({n})');window.__flash&&window.__flash(b);"
                  f"b.click();{tail}}})()")


_LIST = [
 dict(key='chain3', after=4, page='bc', hash='ghz', scene='量子電路入門互動動畫：GHZ 態（3 顆，逐步播放）',
      title='動畫展示：三顆位元一步一步綁', sub='三維動畫：量子電路入門——範例四的八根柱子',
      sentences=[
       '打開線路入門動畫的範例四，位元數是三顆：三條線上排著一個哈達瑪閘和兩個受控反閘，下面是八根柱子。',
       '第一步做哈達瑪閘，零零零和零零一兩根藍色柱子一樣高；第二步，零零一那根整根移到零一一。',
       '第三步，那根柱子再移到最右邊的一一一，八根只剩頭尾兩根，各寫著百分之五十。',
       '按量測一千次，右邊的量測卡只列出零零零和一一一兩列，綠色的次數條各自停在一半附近。'],
      actions=[(0, 0.2, ('js', _BC_FIT)),
               (1, 0.5, ('sel', '#bNext')), (1, 5.6, ('sel', '#bNext')),
               (2, 0.5, ('sel', '#bNext')),
               (3, 0.4, ('sel', '#m1000'))],
      points=[('哈達瑪閘之後', '零零零、零零一各一半'), ('兩個受控反閘', '零零一 → 零一一 → 一一一'), ('量測一千次', '只有零零零和一一一')], shot=(3, 4.0)),
 dict(key='four', after=5, page='bc', hash='ghz', scene='量子電路入門互動動畫：GHZ 態（4 顆）',
      title='動畫展示：換成四顆位元', sub='三維動畫：量子電路入門——十六根柱子的範例四',
      sentences=[
       '把上方的位元數換成四顆，頁面直接跳到最後一步：線路多了第四條線，也多了一個受控反閘。',
       '下面變成十六根細細的柱子，只有最左邊的全零和最右邊的全一兩根站著，各寫著百分之五十。',
       '回到起點再走一次，按下一步做哈達瑪閘，第二根柱子站起來，和全零那根一樣高。',
       '接著連按三次，那根柱子依序跳到零零一一、零一一一，最後跳到最右邊的一一一一；每跳一次，就多綁一顆。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 1.8, _opt(2)),
               (2, 0.4, ('sel', '#bFirst')), (2, 3.6, ('sel', '#bNext')),
               (3, 2.9, ('sel', '#bNext')), (3, 4.0, ('sel', '#bNext')), (3, 6.8, ('sel', '#bNext'))],
      points=[('四顆位元', '多一條線、多一個受控反閘'), ('十六根柱子', '只剩全零和全一'), ('每按一步', '那根柱子往右跳，多綁一顆')], shot=(1, 6.0)),
 dict(key='bind', after=6, page='op', hash='register', scene='3D 場景 4：多量子位元：2ⁿ 個振幅與糾纏（三顆，自己用閘串鏈子）',
      title='動畫展示：鏈子一節一節接上', sub='三維動畫：多量子位元與糾纏——三顆位元的向量大小',
      sentences=[
       '換到三維動畫的多位元場景，把位元數滑桿拉到三，上排出現三顆小球，左邊是編號二，右邊是編號零。',
       '先選目標二號，按哈達瑪閘：二號的箭頭倒向正前方、朝著我們，看起來變短，但左下三個向量大小都還是一，寫著無糾纏。',
       '再選目標一號，按受控反閘，由二號控制一號：左邊兩支箭頭縮成一點，右邊的編號零還指著上方，大小仍是一。',
       '最後選目標零號，再按一次受控反閘：第三支箭頭也縮進去，三個數字都是零，鏈子接到底，三顆全部綁住。'],
      actions=[(0, 3.6, ('slider', '量子位元數 n', 3)),
               (1, 0.4, ('click', '目標 q2')), (1, 2.0, ('click', 'H')),
               (2, 0.4, ('click', '目標 q1')), (2, 2.4, ('click', 'CNOT')),
               (3, 0.4, ('click', '目標 q0')), (3, 2.8, ('click', 'CNOT'))],
      points=[('只做哈達瑪閘', '三顆都是一，無糾纏'), ('接上第一節', '二號、一號變零，零號還是一'), ('接上第二節', '三顆都是零，全部綁住')], shot=(2, 9.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q117'] 取用。"""

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

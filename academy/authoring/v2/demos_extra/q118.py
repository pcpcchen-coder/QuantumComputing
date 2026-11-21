"""Q118 範例 5：隱形傳態——四種 ψ — v2 動畫展示段（格式見 ../demos.py 的說明）。

bc = animations/basic-circuits.html#teleport（淺色主題：正振幅 --pos 藍、負振幅 --neg 橘；Bloch 向量 .vec 橘色；
閘方塊 H 藍、X 酒紅、Ry 綠；8 根柱子 |000⟩…|111⟩（字串 |q2 q1 q0⟩），柱子下面兩顆 Bloch 球，左「單看 q0」、右「單看 q2」，畫的是 reducedBloch()；
只量 q2；最後一步量測時出現綠字「→ 對照 ψ：q2 的量測機率和 ψ 相同」）。
選項「要傳的狀態 ψ」#opts .seg button:nth-child(n)：1 = √¾|0⟩+½|1⟩（預設，Ry(π/3)）、2 = |1⟩（X）、3 = |+⟩（H）、4 = |−⟩（X、H）。
四步：① 準備 ψ（q0）② 建立糾纏對（H q1、CNOT q1→q2）③ Alice：CNOT q0→q1、H q0 ④ Bob：虛線框「修正（2 個古典位元）」CNOT q1→q2、CZ q0–q2。
按「不同的」選項會 rebuild(false)：停在最後一步、量測清除；#dots 有 5 個圓點（起點＋4 步），nth-child(4) = 第 3 步。
按鈕 id：#bFirst「⏮ 起點」、#bNext「下一步 ▶」、#m1000「量測 1,000 次」。兩步之間振幅 650 ms 線性內插，Bloch 向量跟著內插後的振幅移動。
Bloch 球的投影：北極 |0⟩ 在上、南極 |1⟩ 在下；+x 在左前方（畫面左下）、−x 在右後方（畫面右上）。
- move：預設 ψ 從起點四步走完再量測（Playwright 實拍數值，reducedBloch (x, z)）：
  起點兩支都在北極；① q0 (0.87, 0.50) 往 +x 傾斜，q2 仍在北極；② q2 (0, 0) 縮進球心，q0 不變；③ q0 (0.50, 0) 變短、倒到赤道，q2 仍在球心；
  ④ q2 (0.87, 0.50) 和 ① 的 q0 同方向，q0 (1, 0)；量測 1,000 次只列 0、1 兩列，理論 0 75%、1 25%（灰色底），實拍一次 766／234（隨機，旁白不念）。
- four：換選項比較最後一步：|1⟩ → |ψ⟩ = (|100⟩ + |101⟩ + |110⟩ + |111⟩) / 2，右邊四根 +.500 藍、左邊四根 0，q2 指向南極；
  |+⟩ → 8 根一樣高 +.354 藍，q2 (1, 0) 在赤道（畫面左下）；|−⟩ → |100⟩…|111⟩ 四根 −.354 橘、在下面，q2 (−1, 0) 在赤道另一頭（畫面右上）；
  四種的「單看 q0」都在 (1, 0)（尖端 61.2, 124.0）。Q116 用 bc#bell 比四種貝爾態；本頁 #teleport 先前各課的動畫段都沒用過。
- nofix：選 |1⟩ → 跳到第 3 步（#dots 第 4 個）：q2 在球心；量測 1,000 次 0、1 兩列，理論各 50%（實拍 520／480）；
  下一步（修正）→ q2 指向南極，量測卡只剩「1」一列，理論 100%，量 1,000 次後出現綠字判定（實拍 1000 次都是 1）。
op = animations/operation.html#circuit 的「量子隱形傳態」線路（Ry(2π/3)，8 欄）與本課相關，但它的 ψ 和 bc 預設不同（P(1) = 0.75），
為避免「四種 ψ」之外再多一種，本課動畫段不用，只列在教材導覽。
已用 Playwright（1600×900；bc zoom 0.8）實拍確認以上畫面與數值（scratchpad q118/shot118.js）。
"""

LESSON = 'Q118'

# basic-circuits.html 是一般網頁：縮小並捲到選項列，讓選項、電路、振幅、Bloch 球與量測卡同時入鏡（同 Q113–Q117）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")


def _opt(n, first=False):
    """點「要傳的狀態 ψ」第 n 個選項（頁面會跳到最後一步）；first=True 時立刻再按「起點」回到第 0 步"""
    tail = "document.getElementById('bFirst').click();" if first else ''
    return ('js', f"(function(){{var b=document.querySelector('#opts .seg button:nth-child({n})');window.__flash&&window.__flash(b);"
                  f"b.click();{tail}}})()")


_LIST = [
 dict(key='move', after=3, page='bc', hash='teleport', scene='量子電路入門互動動畫：隱形傳態（預設 ψ，逐步播放）',
      title='動畫展示：看狀態怎麼搬家', sub='三維動畫：量子電路入門——範例五的兩顆布洛赫球',
      sentences=[
       '打開線路入門動畫的範例五，柱子下面有兩顆布洛赫球：左邊單看編號零，右邊單看編號二，兩支箭頭都指向北極。',
       '第一步用旋轉閘準備要傳的狀態，左邊的箭頭往旁邊傾斜；第二步做出糾纏對，右邊那支箭頭立刻縮進球心。',
       '第三步愛麗絲做受控反閘和哈達瑪閘，左邊的箭頭也變短，倒到赤道上，右邊還是縮在球心。',
       '第四步鮑伯修正，右邊的箭頭伸出來，指向左邊一開始傾斜的方向；按量測一千次，綠色的條大多落在零。'],
      actions=[(0, 0.2, ('js', _BC_FIT)),
               (1, 0.5, ('sel', '#bNext')), (1, 6.0, ('sel', '#bNext')),
               (2, 0.5, ('sel', '#bNext')),
               (3, 0.5, ('sel', '#bNext')), (3, 6.8, ('sel', '#m1000'))],
      points=[('糾纏對做好', '鮑伯的箭頭縮進球心'), ('愛麗絲做完', '鮑伯仍在球心'), ('鮑伯修正後', '箭頭和原本的狀態同方向')], shot=(3, 9.5)),
 dict(key='four', after=7, page='bc', hash='teleport', scene='量子電路入門互動動畫：隱形傳態（換四種 ψ 比較最後一步）',
      title='動畫展示：四種狀態傳完的樣子', sub='三維動畫：量子電路入門——鮑伯的箭頭指向哪裡',
      sentences=[
       '回到範例五，直接比較四種狀態傳完的樣子；先選一態，頁面跳到最後一步，右邊鮑伯的箭頭指向南極。',
       '看振幅柱子：左邊四根都是零，右邊四根一樣高，它們最左邊那一位都是一，也就是鮑伯那一顆一定是一。',
       '換成正號疊加態，八根柱子一樣高，鮑伯的箭頭倒到赤道上；再換負號疊加態，右邊四根翻到下面變成橘色，箭頭轉到赤道另一頭。',
       '四種換來換去，左邊編號零的箭頭一直停在同一個位置：原本的狀態已經搬到鮑伯那邊，沒有留下一份。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 4.6, _opt(2)),
               (2, 0.4, _opt(3)), (2, 6.2, _opt(4))],
      points=[('一態', '鮑伯的箭頭指向南極'), ('正號、負號疊加態', '箭頭在赤道兩頭'), ('編號零', '四種都停在同一處')], shot=(2, 12.0)),
 dict(key='nofix', after=10, page='bc', hash='teleport', scene='量子電路入門互動動畫：隱形傳態（|1⟩，修正前後各量一千次）',
      title='動畫展示：少了修正會怎樣', sub='三維動畫：量子電路入門——修正前後的量測卡',
      sentences=[
       '在動畫裡也能看拿掉修正的樣子：選一態，再點電路下方右邊的第四個小圓點，停在第三步，修正還沒做。',
       '這時右邊鮑伯的箭頭縮在球心；按量測一千次，零和一的綠色條差不多一樣多，傳一態也只得到一半一半。',
       '按下一步做修正，箭頭伸到南極；再量一千次，量測卡只剩一這一列，上面還出現一行綠字，說和要傳的狀態相同。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 3.4, _opt(2)), (0, 7.4, ('sel', '#dots button:nth-child(4)')),
               (1, 3.4, ('sel', '#m1000')),
               (2, 0.4, ('sel', '#bNext')), (2, 3.8, ('sel', '#m1000'))],
      points=[('停在第三步', '鮑伯的箭頭在球心'), ('沒修就量', '零和一各約一半'), ('修正之後', '一千次都是一')], shot=(2, 10.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q118'] 取用。"""

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

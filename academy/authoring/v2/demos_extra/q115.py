"""Q115 範例 2：干涉——H‑Z‑H = X — v2 動畫展示段（格式見 ../demos.py 的說明）。

bc = animations/basic-circuits.html#interference（淺色主題：正振幅 --pos #1D6A8B 藍、負振幅 --neg #B65C12 橘；
Bloch 向量 .vec 用 --neg 橘色；閘方塊 H 藍 --h、Z 紫 --z #7348A3；尚未做的閘淡色 .future）。
選項「中間的閘」#opts .seg button:nth-child(1) = 有 Z（預設，三步）、(2) = 沒有 Z（兩步）；按選項會 rebuild(false)：
頁面停在最後一步並清除量測，所以 _opt(2, first=True) 在同一段 js 裡立刻按「⏮ 起點」。
按鈕 id：#bFirst「⏮ 起點」、#bNext「下一步 ▶」、#m1000「量測 1,000 次」。
- hzh：有 Z，三步走完（Q113 的 zgate 只走了前兩步 H、Z）：H → |+⟩（兩根藍柱 +.707，箭頭北極→赤道）、
  Z → |−⟩（|1⟩ 柱翻成橘色 −.707，箭頭沿赤道繞 z 軸轉到另一邊，機率仍 50%）、H → |1⟩（|0⟩ 柱 0、|1⟩ 柱 +1.000、箭頭到南極、
  |ψ⟩ = |1⟩）；量測 1,000 次只有「1」一列，1000（100.0%）。
- noz：改選沒有 Z、起點，兩步：H → |+⟩、H → |0⟩（|0⟩ +1.000、|1⟩ 0、箭頭回北極）；量測 1,000 次只有「0」一列，1000（100.0%）。
op = animations/operation.html#interference（js/operation/08_interference.js，模式 A「單一量子位元：兩條路徑」）：
- paths：φ = 0 等於沒有 Z、φ = 180° 等於有 Z（Z 給 |1⟩ 路徑加 180° 相位）。紫色方塊「相位 φ」在下方 |1⟩ 那條路上；
  結果圓盤「結果 |0⟩」右上、「結果 |1⟩」右下；藍 = 經由 |0⟩ 的貢獻、橙 = 經由 |1⟩ 的貢獻、白 = 總和；金色標籤 P(0)／P(1)。
  φ = 0：右下藍、橙一正一反，白色總和為零，P(1) = 0.00；φ = 180：右上抵消 P(0) = 0.00，右下同向接成白箭頭 P(1) = 1.00，
  中間 |1⟩ 節點的橙色箭頭轉向左。Q001 已用過 0→180＋偵測路徑、Q006 用過 90 度與自動掃描；本段只看 0 與 180 兩端對應有無 Z。
已用 Playwright（1600×900；bc zoom 0.8）實拍確認以上畫面與數值。
"""

LESSON = 'Q115'

# basic-circuits.html 是一般網頁：縮小並捲到選項列，讓選項、電路、振幅與量測卡同時入鏡（同 Q113、Q114）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")


def _opt(n, first=False):
    """點「中間的閘」第 n 個選項（頁面會跳到最後一步）；first=True 時立刻再按「起點」回到第 0 步"""
    tail = "document.getElementById('bFirst').click();" if first else ''
    return ('js', f"(function(){{var b=document.querySelector('#opts .seg button:nth-child({n})');window.__flash&&window.__flash(b);"
                  f"b.click();{tail}}})()")


_LIST = [
 dict(key='hzh', after=4, page='bc', hash='interference', scene='量子電路入門互動動畫：干涉（有 Z，三步走完）',
      title='動畫展示：三步走完，負號變成結果', sub='三維動畫：量子電路入門——干涉範例逐步播放',
      sentences=[
       '打開線路入門動畫的干涉範例，中間的閘選有相位翻轉；這次三步全部走完，同時盯著右邊布洛赫球的橘色箭頭。',
       '第一步做完哈達瑪閘，箭頭從北極倒到赤道；第二步做完相位翻轉閘，箭頭沿著赤道轉到另一邊，柱子下面仍是兩個百分之五十。',
       '第三步做完第二個哈達瑪閘，零那根柱子縮到不見，一那根翻上來升到頂，箭頭停在南極。',
       '按量測一千次，綠色的次數條只有一這一列，一千次全部是一。'],
      actions=[(0, 0.2, ('js', _BC_FIT)),
               (1, 0.6, ('sel', '#bNext')), (1, 4.8, ('sel', '#bNext')),
               (2, 0.6, ('sel', '#bNext')),
               (3, 0.4, ('sel', '#m1000'))],
      points=[('相位翻轉閘之後', '機率仍各一半'), ('第二個哈達瑪閘', '零抵消、一加強'), ('量測一千次', '全部是一')], shot=(3, 2.4)),
 dict(key='noz', after=5, page='bc', hash='interference', scene='量子電路入門互動動畫：干涉（沒有 Z 的對照組）',
      title='動畫展示：拿掉中間的閘', sub='三維動畫：量子電路入門——干涉範例的對照組',
      sentences=[
       '現在做對照組：把中間的閘換成沒有相位翻轉，線路上只剩兩個藍色的哈達瑪閘，再回到起點。',
       '第一步和剛才一模一樣，兩根藍色柱子一樣高，箭頭倒到赤道。',
       '第二步直接做第二個哈達瑪閘，一那根柱子縮到不見，零那根升到頂，箭頭回到北極。',
       '量測一千次，這回一千次全部是零；只拿掉一個閘，結果整個翻了過來。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 3.4, _opt(2, first=True)),
               (1, 0.5, ('sel', '#bNext')),
               (2, 0.6, ('sel', '#bNext')),
               (3, 0.4, ('sel', '#m1000'))],
      points=[('拿掉相位翻轉閘', '只剩兩個哈達瑪閘'), ('第二個哈達瑪閘', '回到零態'), ('量測一千次', '全部是零')], shot=(3, 2.4)),
 dict(key='paths', after=6, page='op', hash='interference', scene='3D 場景 8：加速的關鍵——振幅會互相抵消（單一量子位元：兩條路徑）',
      title='動畫展示：兩條路的箭頭相加', sub='三維動畫：加速的關鍵——振幅會互相抵消',
      sentences=[
       '換到三維動畫的干涉場景：起點分成上下兩條路，下面那條路上的紫色方塊，負責替經過一的路加上相位。',
       '相位放在零度，等於沒有相位翻轉閘；右下的結果一裡，藍色和橙色箭頭一正一反抵消，金色數字寫著機率零。',
       '把相位推到一百八十度，等於加上相位翻轉閘，下面那條路的橙色箭頭跟著轉向反方向。',
       '這下換右上的結果零抵消成零，右下的兩支箭頭同向，接成一支白色箭頭，機率變成一。'],
      actions=[(0, 0.2, ('click', '單一量子位元')), (0, 0.4, ('slider', 'A：相位 φ', 0)),
               (2, 0.4, ('sweep', 'A：相位 φ', 0, 180, 4.0))],
      points=[('相位零度', '沒有相位翻轉：結果一抵消'), ('一百八十度', '有相位翻轉：結果零抵消'), ('白色箭頭', '振幅的總和')], shot=(3, 3.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q115'] 取用。"""

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

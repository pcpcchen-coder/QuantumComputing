"""Q116 範例 3：Bell 態——四種糾纏 — v2 動畫展示段（格式見 ../demos.py 的說明）。
bc = animations/basic-circuits.html#bell（淺色主題：正振幅 --pos 藍、負振幅 --neg 橘；Bloch 向量 .vec 橘色；
閘方塊 H 藍、X 酒紅；兩顆 Bloch 球在柱子下面，標「單看 q0」「單看 q1」，畫的是 reducedBloch()；最下面一行 |ψ⟩）。
選項「目標 Bell 態」#opts .seg button:nth-child(n)：1 = Φ⁺（預設，兩步 H、CNOT）、2 = Φ⁻（X(q0)）、3 = Ψ⁺（X(q1)）、4 = Ψ⁻（X(q0)、X(q1)），
後三種是三步（準備 X、H、CNOT）。按「不同的」選項會 rebuild(false)：頁面停在最後一步、量測清除；按目前已選的選項不會有反應，
所以 gallery 一開始用 #dots 的最後一個點直接跳到 Φ⁺ 的最後一步。按鈕 id：#bFirst「⏮ 起點」、#bNext「下一步 ▶」、#m1000「量測 1,000 次」。
- gallery：四種依序比較（最後一步）：Φ⁺ |00⟩、|11⟩ +.707 藍；Φ⁻ 線路多 X(q0)、|11⟩ −.707 橘；Ψ⁺ X 換到 q1、|01⟩、|10⟩ +.707 藍；
  Ψ⁻ 兩條線都有 X、|01⟩ −.707 橘、|10⟩ +.707 藍，|ψ⟩ = (−|01⟩ + |10⟩) / √2；四種的兩顆 Bloch 向量都在球心（reducedBloch = 0）。
  Q010 用過 Ψ⁺、Φ⁻ 的量測與程式碼區塊，Q113 用過 Φ⁻／Ψ⁺ 只走準備的第一步；本段不量測，只把四種的柱子顏色與球心並排比較。
- psim：Ψ⁻ 從起點三步走完再量測：起點兩支向量都在北極；X、X → |11⟩ +1，兩支到南極；H(q0) → |10⟩ +.707、|11⟩ −.707 橘，
  單看 q0 倒到赤道（−x）、單看 q1 仍在南極（大小都是 1）；CNOT → 橘色負振幅由 |11⟩ 移到 |01⟩（兩步間線性內插），兩支向量同時縮到球心；
  量測 1,000 次只有 01、10 兩列。
op = animations/operation.html#register（js/operation/04_register.js）：上排 Bloch 球左邊是 q1、右邊是 q0；左下讀數
「各量子位元 Bloch 長度：q0 …，q1 …」與「無糾纏（可分離態）…」／粉紅色「有糾纏：單一量子位元的向量變短（約化態是混態）」。
按鈕文字（record_demo.js 用 startsWith 比對）：「目標 q0」「目標 q1」「H」「CNOT（控制 = 目標+1 → 目標）」「只測 q0」。
- length：目標 q1 → H：|ψ⟩ = 0.71 |00⟩ + 0.71 |10⟩，長度 q0 1.00、q1 1.00，無糾纏（q1 的向量指向 +x，朝向鏡頭）；
  目標 q0 → CNOT（控制 q1 → 目標 q0）：0.71 |00⟩ + 0.71 |11⟩，長度 0.00、0.00，有糾纏，右邊 q0 原本朝上的箭頭縮成一點；
  只測 q0：狀態塌縮成 |00⟩ 或 |11⟩（隨機，旁白不念），長度回到 1.00、1.00，無糾纏。Q008 只按過「Bell 態」與「測量全部／只測 q0」看隨機性，
  本段改用閘按鈕自己組，並讀向量大小的數字。
已用 Playwright（1600×900；bc zoom 0.8）實拍確認以上畫面與數值。
"""

LESSON = 'Q116'

# basic-circuits.html 是一般網頁：縮小並捲到選項列，讓選項、電路、振幅、Bloch 球與量測卡同時入鏡（同 Q113–Q115）
_BC_FIT = ("document.body.style.zoom='0.8';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-10);")


def _opt(n, first=False):
    """點「目標 Bell 態」第 n 個選項（頁面會跳到最後一步）；first=True 時立刻再按「起點」回到第 0 步"""
    tail = "document.getElementById('bFirst').click();" if first else ''
    return ('js', f"(function(){{var b=document.querySelector('#opts .seg button:nth-child({n})');window.__flash&&window.__flash(b);"
                  f"b.click();{tail}}})()")


_LIST = [
 dict(key='gallery', after=6, page='bc', hash='bell', scene='量子電路入門互動動畫：Bell 態（四種並排比較）',
      title='動畫展示：四種貝爾態一次看', sub='三維動畫：量子電路入門——四個貝爾態的柱子',
      sentences=[
       '打開線路入門動畫的貝爾態範例，先跳到最後一步：第一種只有零零和一一兩根藍色柱子，都朝上。',
       '選第二種，線路最前面在編號零多出一個翻轉閘，一一那根翻到下面，變成橘色。',
       '選第三種，翻轉閘換到編號一，柱子搬到零一和一零；選第四種，兩條線都有翻轉閘，零一那根變成橘色。',
       '四種換來換去，柱子下面兩顆布洛赫球的箭頭一直待在球心：不管哪一種，單看一顆都完全隨機。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 4.4, ('sel', '#dots button:last-child')),
               (1, 0.4, _opt(2)),
               (2, 0.4, _opt(3)), (2, 5.5, _opt(4))],
      points=[('第一、二種', '零零和一一，第二種帶負號'), ('第三、四種', '零一和一零，第四種帶負號'), ('兩顆小球', '四種都縮在球心')], shot=(3, 3.0)),
 dict(key='psim', after=8, page='bc', hash='bell', scene='量子電路入門互動動畫：Bell 態（Ψ⁻ 逐步播放）',
      title='動畫展示：第四種，箭頭怎麼縮進球心', sub='三維動畫：量子電路入門——單看一顆的布洛赫球',
      sentences=[
       '換到第四種，回到起點，這次一步一步走，盯著柱子下面那兩顆布洛赫球：一開始兩支箭頭都指向北極。',
       '第一步做兩個翻轉閘，一一那根升到頂，兩支箭頭從北極直直落到南極；途中一閃而過的變短只是動畫過場，不是糾纏。',
       '第二步做哈達瑪閘，編號零的箭頭倒到赤道，編號一還留在南極，兩支箭頭都還是滿的。',
       '第三步做受控反閘，橘色的負柱子從一一搬到零一，兩支箭頭同時縮進球心；量一千次，只出現零一和一零。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 1.0, _opt(4, first=True)),
               (1, 0.5, ('sel', '#bNext')),
               (2, 0.5, ('sel', '#bNext')),
               (3, 0.5, ('sel', '#bNext')), (3, 7.6, ('sel', '#m1000'))],
      points=[('翻轉閘之後', '兩支箭頭在南極'), ('哈達瑪閘之後', '編號零倒到赤道'), ('受控反閘之後', '兩支都縮進球心')], shot=(3, 10.0)),
 dict(key='length', after=10, page='op', hash='register', scene='3D 場景 4：多量子位元：2ⁿ 個振幅與糾纏（自己用閘組貝爾態）',
      title='動畫展示：向量大小的讀數', sub='三維動畫：多量子位元與糾纏——單一位元的向量大小',
      sentences=[
       '換到三維動畫的多位元場景，這次不按現成的貝爾態按鈕，自己組：先選目標一號，再按哈達瑪閘。',
       '左下的讀數寫著，兩顆的向量大小都是一，下一行是無糾纏；一號自己量雖然一半一半，向量卻沒有變短。',
       '再選目標零號，按受控反閘，由一號控制零號：右邊那支朝上的箭頭縮成一點，兩個數字都變成零，讀數換成粉紅色的有糾纏。',
       '最後按只量零號，兩個數字立刻回到一，讀數又變回無糾纏：量測把這一對的糾纏拆開了。'],
      actions=[(0, 7.2, ('click', '目標 q1')), (0, 8.8, ('click', 'H')),
               (2, 0.6, ('click', '目標 q0')), (2, 2.4, ('click', 'CNOT')),
               (3, 0.8, ('click', '只測 q0'))],
      points=[('只做哈達瑪閘', '大小都是一，無糾纏'), ('受控反閘之後', '大小都是零，有糾纏'), ('只量零號', '回到一，糾纏拆開')], shot=(2, 11.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q116'] 取用。"""

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

"""Q128 模組發表：量子電路展 — v2 動畫展示段（格式見 ../demos.py 的說明）。

與先前各課的區隔：Q113–Q127 的 bc 段都是用 hash 直接開某個範例，沒有點過頁面上方的八個分頁（#tab-…），也沒有讀過重點卡的「延伸：」連結；
op#workflow 只有 Q001（自動播放走一遍）與 Q111（右下插圖的時間組成、主動重置、shots N）用過，沒有用「下一站 ▶」逐站停下來看
程式螢幕、映射標籤與結果直方圖；op#circuit 的「量子傅立葉轉換（QFT，輸入 |110⟩）」預設線路沒有任何一課用過。

tour = basic-circuits.html（預設 #superposition）。標題「八個基礎量子電路」；#tabs 八個按鈕 #tab-superposition … #tab-grover，
  文字「範例 1 疊加」…「範例 8 Grover」。點分頁 → selectScene()：#sceneNo「範例 3 / 8」、#sceneTitle「Bell 態：兩顆位元糾纏」，電路兩條線；
  #tab-teleport 三條線；#tab-grover 的 #links 兩行：「延伸：如何操作量子電腦 · Grover 搜尋：振幅放大」「延伸：Transmon 3D · 第 7 章 振幅長條：糾纏、Grover 與 Deutsch」。
  record_demo.js 的 ('sel', …) 是 el.click()，不會捲動；開頭把頁面縮到 0.8（三條線電路才完整入鏡），最後用 ('js', …) 把 .card.take 捲到畫面中央（Playwright 截圖 bc_tele.png、bc_links08.png）。
pipeline = operation.html#workflow（12_workflow.js）。載入後自動播放（每站約 2.2 秒，第 ⑤ 站 3.5 秒），開始時停在哪一站不固定，
  所以用 ('js', _WF0) 關掉「自動播放」並依 .readout 第一個字（①–⑥）補按「下一站 ▶」回到 ①（按到 ⑥→① 會把計數歸零）。
  ① 程式螢幕固定寫著 qc = QuantumCircuit(2)、qc.h(0)、qc.cx(0, 1)、qc.measure_all()（＝範例 3 Bell 態）；
  ② 轉譯：5 顆實體位元排成 T 形（邊 0–1、1–2、1–3、3–4），i = 1、3 兩顆發光，標籤「q0→Q3」「q1→Q1」；
  ⑤ 晶片閃爍，標籤「shot n / 1,000」（3.5 秒內跑完 1,000 次；每次 50% 得 00 或 11，再有 4% 機會換成 01 或 10）；
  ⑥ 直方圖：00、11 金色、01、10 灰色（約 2% 各，幾乎貼地）。計數是亂數，旁白不念（截圖 wf0.png、wf5.png）。
presets = operation.html#circuit（06_circuit.js）。#controls 預設線路按鈕：Bell 態、GHZ 態（3 位元糾纏）、干涉：H–Z–H、Deutsch–Jozsa（平衡函數）、
  Bernstein–Vazirani（秘密字串 101）（4 條線）、Grover 搜尋（2 位元，找 |11⟩）（2 條線）、量子隱形傳態、量子傅立葉轉換（QFT，輸入 |110⟩）。
  QFT 九步：X X → H q2（2 根）→ P(π/2) → P(π/4) → H q1（4 根）→ P(π/2) → H q0（8 根，顏色兩兩一組）→ SWAP（8 根一樣高、四種顏色輪流）→ M；
  讀數「步驟 9 / 9：量測：8 個結果機率相同 —— 資訊都在相位裡…」；插圖 1000 shots 八根都在青線 0.125 附近（亂數，旁白不念次數）（截圖 op_qft7.png、op_qft9.png）。
已用 Playwright 單張截圖確認以上畫面（scratchpad q128/shot1–3.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q128'

# 縮小到 0.8，讓三條線的隱形傳態電路也完整入鏡（截圖 bc_tele.png）
_BC_ZOOM = "document.body.style.zoom='0.8';window.scrollTo(0,0);"
# 把重點卡捲到畫面中央，閃一下延伸連結
_BC_LINKS = ("document.querySelector('.card.take').scrollIntoView({block:'center'});"
             "window.__flash(document.querySelector('#links'));")
# 關掉自動播放，再補按「下一站」回到 ① 寫程式（開始時停在哪一站不固定）
_WF0 = ("(function(){var bs=[...document.querySelectorAll('#controls button')];"
        "var a=bs.find(function(x){return x.textContent.trim().indexOf('自動播放')===0;});"
        "if(a){window.__flash(a);if(a.classList.contains('on'))a.click();}"
        "var nx=bs.find(function(x){return x.textContent.trim().indexOf('下一站')===0;});"
        "var b=document.querySelector('#controls .readout b');"
        "var m='①②③④⑤⑥'.indexOf(((b&&b.textContent)||'①').charAt(0));"
        "var n=(6-Math.max(0,m))%6;for(var i=0;i<n;i++)nx.click();})()")

_LIST = [
 dict(key='tour', after=3, page='bc', hash='superposition', scene='量子電路入門互動動畫：上方八個分頁（範例 3、5、8）與重點卡的延伸連結',
      title='動畫展示：一排分頁就是展品目錄', sub='三維動畫：量子電路入門——八個分頁與延伸連結',
      sentences=[
       '打開線路入門動畫，大標題寫著八個基礎量子電路，下面一排八個分頁，從範例一疊加排到範例八格羅弗，就是今天的展品目錄。',
       '點範例三，標題上方的小字寫著八個裡的第三個，題目換成貝爾態：兩顆位元糾纏，電路也換成兩條線。',
       '再點範例五隱形傳態，電路變成三條線；最後點範例八格羅弗，往下捲到最底下的重點卡。',
       '重點卡下面有兩行延伸連結，寫著另一個動畫的名稱和場景，還有超導晶片動畫的第七章；海報上的出處，就照這個格式寫。'],
      actions=[(0, 0.2, ('js', _BC_ZOOM)), (1, 0.3, ('sel', '#tab-bell')),
               (2, 0.4, ('sel', '#tab-teleport')), (2, 4.2, ('sel', '#tab-grover')), (2, 6.4, ('js', _BC_LINKS))],
      points=[('八個分頁', '今天的展品目錄'), ('點一個分頁', '八個裡的第幾個'), ('延伸連結', '出處照這樣寫')], shot=(1, 4.0)),
 dict(key='pipeline', after=6, page='op', hash='workflow', scene='3D 場景 12：完整流程——關掉自動播放，用「下一站」逐站看貝爾態程式跑過真實機器',
      title='動畫展示：貝爾態送進真實機器', sub='三維動畫：一次量子計算的完整流程，逐站停下來看',
      sentences=[
       '觀眾問：真的量子電腦也一樣嗎？打開操作量子電腦動畫的完整流程場景，先關掉自動播放，螢幕上的程式正是範例三的貝爾態。',
       '按下一站，進入轉譯：五顆實體位元排成丁字形，其中兩顆亮起，標籤寫著編號零對到實體三號、編號一對到實體一號。',
       '再按三次，經過脈衝排程和控制電子，來到冷凍機裡的晶片，晶片一閃一閃，上方的計數一路跑到一千。',
       '最後一站判別與結果，零零和一一兩根金色柱子差不多高，零一和一零幾乎貼在地上；真實機器會有少量錯誤，所以要看比例。'],
      actions=[(0, 7.4, ('js', _WF0)),
               (1, 0.3, ('click', '下一站')),
               (2, 0.3, ('click', '下一站')), (2, 1.6, ('click', '下一站')), (2, 2.9, ('click', '下一站')),
               (3, 0.3, ('click', '下一站'))],
      points=[('程式螢幕', '就是範例三貝爾態'), ('轉譯', '對到實體位元'), ('結果', '少量錯誤，要看比例')], shot=(3, 3.5)),
 dict(key='presets', after=10, page='op', hash='circuit', scene='3D 場景 6：量子線路——八個預設線路（BV、Grover），再單步走完量子傅立葉轉換',
      title='動畫展示：下一次展覽的新展品', sub='三維動畫：量子線路的八個預設線路與量子傅立葉轉換',
      sentences=[
       '想替下一次展覽找新展品？打開量子線路場景，左邊有八個預設線路按鈕，大多是我們展覽裡的老朋友。',
       '點猜密碼，線路變成四條線；點格羅弗，又變回兩條線，閘排得滿滿的。',
       '最後一顆是展覽裡沒有的量子傅立葉轉換：連按七次單步，每做一個哈達瑪閘，柱子就從一根變成兩根、四根、八根。',
       '再按兩次，走過交換閘和量測：八根柱子一樣矮、四種顏色輪流；面板寫著資訊都藏在相位裡，量一千次，八個結果幾乎一樣多。'],
      actions=[(1, 0.3, ('click', 'Bernstein')), (1, 3.4, ('click', 'Grover')),
               (2, 0.4, ('click', '量子傅立葉')),
               (2, 4.6, ('click', '單步')), (2, 5.4, ('click', '單步')), (2, 6.2, ('click', '單步')), (2, 7.0, ('click', '單步')),
               (2, 7.8, ('click', '單步')), (2, 8.6, ('click', '單步')), (2, 9.4, ('click', '單步')),
               (3, 0.3, ('click', '單步')), (3, 1.5, ('click', '單步'))],
      points=[('八個預設線路', '大多是老朋友'), ('量子傅立葉轉換', '一根變成八根'), ('量測', '資訊藏在相位裡')], shot=(3, 5.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q128'] 取用。"""

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

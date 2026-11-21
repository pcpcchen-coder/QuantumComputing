"""Q011 隱形傳態：傳狀態不傳東西 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（皆讀原始碼確認）：
- animations/basic-circuits.html#teleport：SCENES 的 id "teleport"（約第 397 行）；
  選項「要傳的狀態 ψ」四顆按鈕依序為 √¾|0⟩+½|1⟩（預設）、|1⟩、|+⟩、|−⟩，畫在 #opts .seg 裡（renderOpts，約第 600 行）；
  換選項會 rebuild(false)，直接跳到最後一步（約第 616 行）；用 hash 載入則從起點開始；
  #bFirst、#bNext（約第 194–197 行），每一步振幅與 Bloch 球內插 650 毫秒；按「下一步」會清空量測紀錄（go → clearShots）；
  #m1000（約第 222 行）約 0.75 秒跑完 1,000 次；只量 q2；最後一步量測後出現綠色的 verdict 字。
  兩顆 Bloch 球依序是「單看 q0」「單看 q2」（bloch: [0, 2]）。
- animations/operation.html#circuit：js/operation/06_circuit.js 的 tele 範例，按鈕「量子隱形傳態」、「單步 ▶」；
  八欄：Ry、H、CX、CX、H、CX、CZ、M；最後量測欄跑 1000 shots，右下插圖畫直方圖（青線 = 理想機率），q2 量到 1 的機率 0.75。

以頁面引擎（simulate、marginal、reducedBloch）在 Node 實算：
- ψ = |1⟩：第 1 步 q0 指向南極、q2 指向北極；第 2、3 步 q2 在球心；第 4 步 q2 指向南極、q0 指向 +x（不再朝下）。
- ψ = 預設：第 3 步量 q2 理論 0、1 各 50%；第 4 步 0 為 75%、1 為 25%。
"""

LESSON = 'Q011'

# basic-circuits.html 是一般網頁：縮小並捲到選項列，讓選項、電路、振幅與 Bloch 球、量測卡同時入鏡
_BC_FIT = ("document.body.style.zoom='0.68';"
           "document.querySelector('#opts').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-8);")

_LIST = [
 dict(key='bloch', after=4, page='bc', hash='teleport', scene='量子電路入門互動動畫：隱形傳態',
      title='動畫展示：狀態搬家的四步', sub='三維動畫：量子電路入門——隱形傳態的布洛赫球',
      sentences=[
       '打開線路入門動畫的隱形傳態，上方把要傳的狀態選成一，再按起點，從頭開始走。',
       '按下一步，振幅柱子下面有兩顆球：左邊是愛麗絲那顆，箭頭翻到正下方，代表一；右邊是鮑伯那顆，還指著正上方。',
       '再按一次，做出糾纏對，鮑伯那顆的箭頭一下子縮到球心，單看它完全隨機。',
       '第三步愛麗絲做完受控反閘和哈達瑪閘，鮑伯那顆還縮在球心；第四步照兩個位元修正，它就指向正下方，愛麗絲那顆卻已經不朝下了。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 4.4, ('sel', '#opts .seg button:nth-child(2)')), (0, 6.4, ('sel', '#bFirst')),
               (1, 0.4, ('sel', '#bNext')), (2, 0.4, ('sel', '#bNext')),
               (3, 0.4, ('sel', '#bNext')), (3, 6.4, ('sel', '#bNext'))],
      points=[('選成一', '愛麗絲那顆朝下'), ('做出糾纏對', '鮑伯那顆縮到球心'), ('第四步修正後', '鮑伯朝下，愛麗絲不再朝下')],
      shot=(3, 11.0)),
 dict(key='call', after=6, page='bc', hash='teleport', scene='量子電路入門互動動畫：隱形傳態',
      title='動畫展示：打電話前後', sub='三維動畫：量子電路入門——修正前後各量一千次',
      sentences=[
       '回到隱形傳態，這次用預設的狀態，量到零的機率是四分之三；連按三次下一步，停在還沒打電話的時候。',
       '按量測一千次，量的是鮑伯那一條線：零和一大約各一半，灰色的理論也是一半一半。',
       '再按下一步，鮑伯照兩個位元修正，紀錄會清空；再量一千次，零大約變成四分之三，統計條上方還多了一行綠字，說鮑伯量到的機率和要傳的狀態相同。',
       '差別只在那兩個位元：沒有電話，鮑伯量到的就只是一半一半的隨機結果。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 6.8, ('sel', '#bNext')), (0, 7.6, ('sel', '#bNext')), (0, 8.4, ('sel', '#bNext')),
               (1, 0.6, ('sel', '#m1000')),
               (2, 0.6, ('sel', '#bNext')), (2, 5.2, ('sel', '#m1000'))],
      points=[('還沒打電話', '零和一各一半'), ('照兩個位元修正', '零約占四分之三'), ('差別', '只在那兩個位元')],
      shot=(3, 2.0)),
 dict(key='repeat', after=8, page='op', hash='circuit', scene='3D 場景 6：量子線路——一步一步執行',
      title='動畫展示：重複一千次來確認', sub='三維動畫：量子線路一步一步執行——量子隱形傳態',
      sentences=[
       '換到三維動畫的量子線路場景，選量子隱形傳態，三條線上排了八格，最後一格是測量。',
       '連按單步，每按一次，那一格的閘就會亮起來：先準備狀態，再做糾纏對，接著是愛麗絲的兩步，和鮑伯的兩步修正。',
       '最後一格是測量，右下角的小圖跑了一千次：量到一的柱子大約佔四分之三，和青色的理想線差不多高。',
       '這次準備的狀態，量到一的機率正好是四分之三，鮑伯量到的也是四分之三，和他收到原本的狀態相符；只量一次看不出來，重複很多次才比得出來。'],
      actions=[(0, 3.4, ('click', '量子隱形傳態')),
               (1, 0.6, ('click', '單步')), (1, 6.0, ('click', '單步')), (1, 6.8, ('click', '單步')),
               (1, 7.4, ('click', '單步')), (1, 8.2, ('click', '單步')), (1, 9.6, ('click', '單步')), (1, 10.4, ('click', '單步')),
               (2, 0.3, ('click', '單步'))],
      points=[('八格線路', '一格一格亮起來'), ('最後的測量', '跑一千次'), ('量到一', '約四分之三')],
      shot=(3, 2.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q011'] 取用。"""

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

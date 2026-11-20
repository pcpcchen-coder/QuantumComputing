"""Q057 Qiskit 實作：Bell 與 GHZ — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（已讀原始碼，並以 1600×900 Chromium（swiftshader）截圖確認畫面位置，截圖在 /home/user/qwork/q057shots/）：
- bc#ghz：animations/basic-circuits.html 範例 4「GHZ 態：多顆位元一起糾纏」（SCENES id "ghz"，第 377–395 行）。
  選項「位元數」3 顆／4 顆（opts 第 380 行；renderOpts() 建在 #opts .seg，第 2 個按鈕是「4 顆」）；
  換選項 → rebuild(false) 直接停在最後一步並清除量測（第 642–655 行、clearShots）。
  #bNext「下一步 ▶」、#m1000「量測 1,000 次」、#mClear「清除」（第 194–224 行 markup）。
  量測列只列出理論機率不為零的結果（histRender()），所以最後一步只會列出 000、111（4 顆：0000、1111）。
  縮放 0.62 並捲到 #sceneTitle 時，電路在上、振幅與機率卡在左下、量測卡在右下（bc3m.png、bc4m.png）。
  程式碼區塊 .card.take details 展開後（縮放 0.9）整段入鏡：4 顆時有 qc.cx(0, 1)、qc.cx(1, 2)、qc.cx(2, 3)（bccode.png；qiskitCode()）。
- op#circuit：animations/js/operation/06_circuit.js。範例按鈕「GHZ 態（3 位元糾纏）」（CIRCUITS.ghz，4 欄：H、CNOT q0→q1、CNOT q1→q2、量測）；
  「單步 ▶」；toggle「加入雜訊（每閘 1%、讀取 3%）」切換時若已有結果立即重抽（sample()）。
  量測欄跑 1000 次，右下插圖「量測 1000 shots 的結果（青線 = 理想機率）」，8 個位置都畫（op4.png、op4n.png）。
  雜訊算法：1−0.99³ ≈ 3% 的機率換成均勻隨機結果，再對每顆位元 3% 翻轉；單一錯誤組合期望約 18 次（1000 次中），
  六個中間位置在截圖中都出現矮柱，000、111 期望約 447 次，低於青線 500。
Q010 已用過 bc#bell 的程式碼段與 op#circuit 的貝爾態雜訊段；本課改用 GHZ 範例，句子新寫。
"""
LESSON = 'Q057'

# basic-circuits.html 是一般網頁：縮小並捲到範例標題，讓選項、電路、振幅卡和量測卡同時入鏡
_BC_FIT = ("document.body.style.zoom='0.62';"
           "document.querySelector('#sceneTitle').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-8);")
# 展開頁面最下方的程式碼區塊並捲過去
_BC_CODE = ("document.body.style.zoom='0.9';"
            "document.querySelector('.card.take details').open=true;"
            "document.querySelector('.card.take').scrollIntoView({block:'start'});"
            "window.__flash(document.querySelector('#code').closest('pre'));")

_LIST = [
 dict(key='ghz', after=4, page='bc', hash='ghz', scene='量子電路入門互動動畫：GHZ 態',
      title='動畫展示：三顆一起糾纏', sub='三維動畫：量子電路入門——格林伯格態',
      sentences=[
       '打開線路入門動畫的第四個範例，也就是格林伯格態；一開始停在起點，三條線都還是零。',
       '連按三次下一步，先是哈達瑪閘，再是兩個受控反閘，一個接一個往下傳。',
       '這時左下的振幅柱子，只剩頭尾的零零零和一一一兩根，各占百分之五十。',
       '按量測一千次，右邊只列出零零零和一一一兩種結果，兩條綠色都在一半左右。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (1, 0.8, ('sel', '#bNext')), (1, 2.6, ('sel', '#bNext')),
               (1, 4.4, ('sel', '#bNext')), (3, 0.8, ('sel', '#m1000'))],
      points=[('三次下一步', '受控反閘往下傳'), ('振幅柱子', '只剩頭尾兩根'), ('量一千次', '只有 000、111')], shot=(3, 5.0)),
 dict(key='code', after=6, page='bc', hash='ghz', scene='量子電路入門互動動畫：GHZ 態',
      title='動畫展示：多一顆，多一行', sub='三維動畫：量子電路入門——四顆的格林伯格態與程式碼',
      sentences=[
       '回到同一個動畫，把上方的位元數改成四顆，線路自動多出第三個受控反閘，畫面直接停在最後一步。',
       '量一千次，結果只有四個零和四個一兩種，三顆和四顆的差別，只是多綁了一顆。',
       '往下展開程式碼，四顆的版本只比三顆多一行受控反閘，從第三顆接到第四顆。',
       '我們的筆記本用迴圈幫你接，只要改一個數字，就能變成五顆。'],
      actions=[(0, 0.2, ('js', _BC_FIT)), (0, 4.0, ('sel', '#opts .seg button:nth-child(2)')),
               (1, 0.6, ('sel', '#m1000')), (2, 0.5, ('js', _BC_CODE))],
      points=[('改成四顆', '多一個受控反閘'), ('量一千次', '只有 0000、1111'), ('程式碼', '多一行 cx(2, 3)')], shot=(2, 5.0)),
 dict(key='noise', after=8, page='op', hash='circuit', scene='3D 場景 6：量子線路——一步一步執行',
      title='動畫展示：三顆加上雜訊', sub='三維動畫：量子線路一步一步執行——格林伯格態',
      sentences=[
       '換到三維動畫的量子線路場景，按三顆糾纏的範例，再按四次單步，走到最右邊的量測欄。',
       '右下的小圖跑了一千次，只有零零零和一一一兩根柱子，差不多碰到青色的理想線。',
       '打開加入雜訊的開關，中間六個位置都冒出很矮的小柱子。',
       '頭尾兩根大柱子也比青線矮了一截；這和筆記本裡有雜訊的直方圖，是同一個道理。'],
      actions=[(0, 3.6, ('click', 'GHZ 態')), (0, 5.4, ('click', '單步')), (0, 6.2, ('click', '單步')),
               (0, 7.0, ('click', '單步')), (0, 7.8, ('click', '單步')), (2, 1.0, ('toggle', '加入雜訊', True))],
      points=[('四次單步', '走到量測欄'), ('理想模擬', '只有 000、111'), ('加入雜訊', '中間冒出矮柱')], shot=(3, 2.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q057'] 取用。"""

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

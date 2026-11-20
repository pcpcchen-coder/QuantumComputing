"""Q124 用 Qiskit 重現八個範例 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都用 basic-circuits.html（bc）各範例頁底部的「Qiskit 程式碼（會隨上面的選項改變）」區塊（<details> 在 .card.take 裡，程式碼在 #code，由 qiskitCode() 產生）。
Q010 只用過 #bell 的程式碼區塊；Q113–Q123 沒有展開過程式碼區塊。record_demo.js 的 ('sel', …) 是在頁面裡 el.click()，不會捲動畫面，
所以可以停在程式碼區塊、同時點上面的選項按鈕，程式碼會立刻重產（rebuild() 只改 #code 的文字，<details> 保持展開）。

tp = #teleport（範例 5）。預設 ψ = √¾|0⟩+½|1⟩：程式碼第三行 from math import pi；qc = QuantumCircuit(3, 1)；qc.ry(pi / 3, 0)；
  Bob 段註解「真實硬體會先量測 q0、q1，再依結果做 X、Z（動態電路）；這裡用受控閘代替，結果相同」、qc.cx(1, 2)、qc.cz(0, 2)；qc.measure(2, 0)。
  選項 #opts .seg 第 3 顆是「|+⟩」：程式變成 qc.h(0)，from math import pi 消失（Node 實跑 qiskitCode 與 Playwright 截圖確認）。
  Q118 用過 #teleport 的線路、四種 ψ 的最後一步與修正前後量測，沒有展開過程式碼。
gr = #grover（範例 8）。預設 2 顆、答案 11、最佳 1 輪：標記段只有 qc.cz(0, 1)；擴散段註解「擴散：H、X、多控制 Z、X、H（這樣接會多一個整體負號，不影響機率）」，
  下面五行 h、x、cz、x、h。按 #opts 第一組第 2 顆「3 顆（N = 8）」→ 答案預設 101、最佳 2 輪：標記段 qc.x(1)、qc.ccz(0, 1, 2)、qc.x(1)，「第 2 輪・標記」再出現一次。
  頁尾 footer：「所有振幅都由頁面內建的狀態向量模擬器即時計算，和 Qiskit 的 Statevector 結果一致（Grover 的擴散步驟照理想的『對平均值翻轉』計算；
  用 H、X、多控制 Z 組成的實際電路會多一個整體負號，機率完全相同）」。捲到 footer 底部時，第 2 輪程式碼與 footer 同時入鏡（Playwright 截圖）。
  Q121、Q122 用過 #grover 的線路逐步與平均值虛線，沒有展開過程式碼。
bv = #bv（範例 7）。預設密碼 101（按鈕 s2=1、s1=0、s0=1）；點第 2 顆（s1）→ 111，再點第 3 顆（s0）→ 110；選項改變後停在最後一步。
  黑盒受控反閘由 q0、q2 → q1、q2；量測 1,000 次：綠色柱只有 110「1000（100.0%）」，verdict「→ 密碼 s = 110」（理論 100%，不是隨機數值）。
  程式碼：「# Bernstein–Vazirani：查一次就猜中密碼（密碼 s = 110）」、qc.cx(1, 3)、qc.cx(2, 3)。Q120 用過 #bv 自訂密碼 011 從起點逐步播放；本課改用 110 並讀程式碼。
已用 Playwright 單張截圖確認以上畫面（scratchpad q124/shot1.js、shot2.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q124'

# 展開頁面最下方的程式碼區塊並捲過去（同 Q010 的作法）
_BC_CODE = ("document.body.style.zoom='0.9';"
            "document.querySelector('.card.take details').open=true;"
            "document.querySelector('.card.take').scrollIntoView({block:'start'});"
            "window.__flash(document.querySelector('#code').closest('pre'));")
# 捲到頁尾那句「和 Qiskit 的 Statevector 結果一致」
_BC_FOOT = ("document.querySelector('footer').scrollIntoView({block:'end'});"
            "window.__flash(document.querySelector('footer span'));")
# 縮小並捲到範例標題，讓選項、電路和量測卡同時入鏡（同 Q010）
_BC_FIT = ("document.body.style.zoom='0.62';"
           "document.querySelector('#sceneTitle').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-8);")

_LIST = [
 dict(key='tpcode', after=6, page='bc', hash='teleport', scene='量子電路入門互動動畫：隱形傳態（頁面底部的程式碼區塊）',
      title='動畫展示：隱形傳態的程式碼', sub='三維動畫：量子電路入門——隱形傳態的程式碼區塊',
      sentences=[
       '打開線路入門動畫的隱形傳態，展開最底下的程式碼區塊；建線路那一行寫著三顆量子位元，紀錄卻只有一格。',
       '因為最後只量編號二；上面多匯入了圓周率，是因為要傳的狀態，是用旋轉閘轉三分之圓周率做出來的。',
       '鮑伯修正那一段有一行註解：真實硬體會先量編號零和編號一，再照結果修正；這裡改用受控閘代替，結果相同。',
       '把要傳的狀態換成正號疊加態，旋轉閘那一行馬上換成一個哈達瑪閘，匯入圓周率那一行也不見了。'],
      actions=[(0, 0.2, ('js', _BC_CODE)),
               (3, 2.2, ('sel', '#opts .seg button:nth-child(3)'))],
      points=[('三顆位元、一格紀錄', '最後只量編號二'), ('受控閘', '代替中途量測再修正'), ('換成正號疊加態', '旋轉閘換成哈達瑪閘')], shot=(2, 3.0)),
 dict(key='grcode', after=7, page='bc', hash='grover', scene='量子電路入門互動動畫：Grover（程式碼區塊與頁尾的比對說明）',
      title='動畫展示：多出來的整體負號', sub='三維動畫：量子電路入門——格羅弗的程式碼與頁尾說明',
      sentences=[
       '到線路入門動畫的格羅弗範例，展開程式碼區塊；兩顆位元、答案一一的時候，標記那一段只有一行受控相位翻轉閘。',
       '擴散那一段是哈達瑪、翻轉、受控相位翻轉、翻轉、哈達瑪五行，註解寫著這樣接會多一個整體負號，不影響機率。',
       '在上面把位元數換成三顆，程式立刻變多：答案換成一零一、做兩輪，標記用翻轉閘夾住一個多控制的相位翻轉。',
       '捲到頁面最下面，小字寫著頁面的振幅由內建模擬器即時計算，和量子程式套件的狀態向量結果一致。'],
      actions=[(0, 0.2, ('js', _BC_CODE)),
               (2, 1.8, ('sel', '#opts .seg button:nth-child(2)')),
               (3, 0.3, ('js', _BC_FOOT))],
      points=[('兩顆位元', '標記只有一行'), ('擴散五行', '多一個整體負號'), ('頁尾', '和狀態向量結果一致')], shot=(2, 6.0)),
 dict(key='bvparam', after=10, page='bc', hash='bv', scene='量子電路入門互動動畫：BV（密碼改成 110，量測後讀程式碼）',
      title='動畫展示：改一個參數，兩邊一起比', sub='三維動畫：量子電路入門——密碼範例改成一一零',
      sentences=[
       '打開線路入門動畫的密碼範例，把上面的密碼按鈕點成一一零，線路裡黑盒子的受控反閘馬上換了位置。',
       '先按清除，再按量測一千次，綠色的柱子只剩一一零一根，旁邊寫著密碼就是一一零。',
       '往下捲到程式碼區塊，黑盒子那兩行變成編號一和編號二各接一個受控反閘，註解裡的密碼也改成一一零。',
       '改造時就照這樣做：頁面點成同一組參數，筆記本跑出的理論機率要和頁面一模一樣，才算比對完成。'],
      actions=[(0, 0.2, ('js', _BC_FIT)),
               (0, 4.0, ('sel', '#opts .seg button:nth-child(2)')), (0, 5.0, ('sel', '#opts .seg button:nth-child(3)')),
               (1, 0.6, ('sel', '#mClear')), (1, 1.6, ('sel', '#m1000')),
               (2, 0.3, ('js', _BC_CODE))],
      points=[('密碼一一零', '受控反閘換位置'), ('量測一千次', '只有一一零'), ('程式碼', '跟著選項改變')], shot=(1, 6.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q124'] 取用。"""

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

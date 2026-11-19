"""Q081 錯誤預算：線路能跑多深 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/operation.html#circuit（js/operation/06_circuit.js）
  範例按鈕：Bell 態、GHZ 態（3 位元糾纏）、干涉：H–Z–H、Deutsch–Jozsa（平衡函數）、Bernstein–Vazirani（秘密字串 101）、
            Grover 搜尋（2 位元，找 |11⟩）、量子隱形傳態、量子傅立葉轉換（QFT，輸入 |110⟩）
  控制：⏮ 重設、單步 ▶、播放（每 1.3 s 走一欄）；開關：加入雜訊（每閘 1%、讀取 3%）
  雜訊模型 sample()：以 pg = 1 − 0.99^閘數 輸出均勻隨機結果，否則照理想機率；再對每個量測位元以 3% 翻轉。
    干涉 H–Z–H：3 個閘、4 欄（播放約 5.2 s）；理想 100% 為 1；含雜訊時 0 的期望約 4.4%
    Grover：12 個閘、8 欄（播放約 10.4 s）；理想 100% 為 11；含雜訊時 11 的期望約 86%，其他三個各約 4–5%
  切換範例會清空直方圖，但雜訊開關的狀態保留；打開開關時若已有直方圖，立刻用雜訊重抽 1000 次。
  旁白只說柱子變矮、冒出小柱子、離青線多遠，不宣稱任何特定的隨機計數。
"""
LESSON = 'Q081'


class _Demos(list):
    def keys(self):
        return [LESSON]

    def items(self):
        return [(LESSON, list(self))]

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


# 幀率補償（同 q004.py）：core.js 把每幀 dt 限在 0.05 秒，負載高時動畫會落後旁白。
FPS_FIX = ('js', "(()=>{if(window.__qfps)return;window.__qfps=1;let n=0,t0=performance.now();"
                 "const f=(now)=>{n++;if(now-t0>=1000){App.speed=Math.min(8,Math.max(1,20*(now-t0)/1000/n));n=0;t0=now;}"
                 "requestAnimationFrame(f);};requestAnimationFrame(f);})()")

S_CIR = '3D 場景 6：量子線路——一步一步執行'

DEMOS = _Demos([
 dict(key='compound', after=4, page='op', hash='circuit', scene=S_CIR,
      title='動畫展示：雜訊就是連乘', sub='三維動畫：量子線路一步一步執行，加入雜訊',
      sentences=[
       '打開量子線路場景，選格羅弗搜尋按播放，亮起的閘一欄一欄往右移，這條線路有八欄、一共十二個閘，大約要走十秒。',
       '走到測量欄後，右下小圖只有一一這根柱子，剛好頂到青色的理想線；現在打開加入雜訊的開關，每個閘有百分之一、讀取有百分之三的機會出錯。',
       '一一那根柱子立刻變矮，另外三個結果冒出小柱子；這個開關的算法正是連乘，零點九九自乘十二次，大約百分之八十九。',
       '做錯的那一成多會隨機落在四個結果之一，再加上讀取出錯，所以一一的柱子比青線矮了一截。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.6, ('click', 'Grover 搜尋')), (0, 1.4, ('click', '播放')),
               (1, 7.2, ('toggle', '加入雜訊', True))],
      points=[('理想模擬', '只有 11 一根柱子'), ('打開雜訊', '11 變矮、冒出小柱'), ('連乘', '0.99¹² ≈ 89%')], shot=(2, 3.0)),
 dict(key='deeper', after=7, page='op', hash='circuit', scene=S_CIR,
      title='動畫展示：閘越多，越模糊', sub='三維動畫：三個閘和十二個閘的線路，同樣的雜訊',
      sentences=[
       '再開一次量子線路場景，先打開雜訊，選只有三個閘的干涉線路按播放，走到測量欄時，小圖裡一的柱子幾乎頂到青線，零只冒出一點。',
       '換成十二個閘的格羅弗搜尋同樣按播放，這次要走八欄，亮起的閘一欄一欄往右移，大約十秒才會走到測量欄。',
       '走到測量欄後，一一的柱子離青線明顯遠了一截，其他三個結果也冒出小柱子。',
       '閘從三個變成十二個，連乘起來的成功率就從大約九成七掉到不到九成，線路越深，正確答案就越被雜訊淹沒。'],
      actions=[(0, 0.1, FPS_FIX), (0, 1.5, ('toggle', '加入雜訊', True)), (0, 3.5, ('click', '干涉')),
               (0, 4.8, ('click', '播放')),
               (1, 0.2, ('click', 'Grover 搜尋')), (1, 0.8, ('click', '播放'))],
      points=[('三個閘', '1 幾乎頂到青線'), ('十二個閘', '11 離青線一截'), ('越深越模糊', '0.99³ ≈ 97%、0.99¹² ≈ 89%')], shot=(2, 4.0)),
])

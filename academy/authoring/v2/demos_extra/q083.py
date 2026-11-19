"""Q083 重複碼：最簡單的錯誤更正 — v2 動畫展示段（格式見 ../demos.py 的說明）。

本學程沒有重複碼專用場景（課綱標為需新增），改用最接近的現成場景：
場景：animations/transmon-3d.html#surface（第 10 章：表面碼，G10STEPS）
  步驟按鈕在 #g10steps 裡（文字 1–8，沒有 id），用 ('sel', '#g10steps button:nth-child(k)') 點選；點下即 g10Step(k−1) 並開始播放。
  「自動接續」核取方塊 id = g10auto（預設勾選）：步驟播完會自動跳下一步，所以每段一開始先點一次把它取消。
  步驟 ③「單一 X 錯誤」（dur 22 s）：0.3 s 在正中間 D5 注入 X（紅球），含 D5 的兩個 Z 穩定子（青色）立刻亮；
     11 s decode10()：白色配對線 0–2.0 s，1.3 s 套用修正（球閃白、標「修正」約 1.25 s 淡出），格子熄滅。
  步驟 ⑥「邏輯錯誤」（dur 31 s）：0.3 s 在 D1、D4 注入 X（同一行相鄰兩顆）；兩者共用的青色格子不亮，只有含 D4、D7 的邊界半圓亮；
     11 s 解碼：白線、1.3 s 在 D7 補 X、2.0 s 判定邏輯錯誤 → D1、D4、D7 全紅並以紅線串起，紅色標籤「邏輯錯誤！（邏輯 X）」；
     25 s 才顯示導引線（本段在那之前結束）。
  以上時間都是相對於點下步驟按鈕的時刻；結果是固定腳本，不是隨機。
  注意：transmon-3d.html 的每幀 dt 限在 0.05 s，且沒有 App.speed 可補償；錄影幀率低於 20 fps 時步驟會比旁白慢。
"""
LESSON = 'Q083'


class _Demos(list):
    def keys(self):
        return [LESSON]

    def items(self):
        return [(LESSON, list(self))]

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


# 幀率補償（同 q004.py）：只適用 operation.html（App.speed）。本課兩段都在 transmon-3d.html，該頁沒有 App，故不使用。
FPS_FIX = ('js', "(()=>{if(window.__qfps)return;window.__qfps=1;let n=0,t0=performance.now();"
                 "const f=(now)=>{n++;if(now-t0>=1000){App.speed=Math.min(8,Math.max(1,20*(now-t0)/1000/n));n=0;t0=now;}"
                 "requestAnimationFrame(f);};requestAnimationFrame(f);})()")

S_SURF = 'transmon 3D 第 10 章：表面碼'
NO_AUTO = ('id', 'g10auto')

DEMOS = _Demos([
 dict(key='syndrome', after=7, page='tr', hash='surface', scene=S_SURF,
      title='動畫展示：一顆被翻，兩格亮起', sub='三維動畫：表面碼的症狀與解碼',
      sentences=[
       '打開超導晶片動畫的表面碼章節，選第三步：正中間的資料球被翻轉成紅色，旁邊兩塊格子立刻亮起青綠色。',
       '解碼器看不到紅球，只看得到亮起的格子；它用白線把兩塊亮格連成一對，最短的路正好經過中間那顆球，於是在那裡補一次翻轉。',
       '紅球變回原色，兩塊格子也熄了；這和三枚硬幣的症狀一樣，只說哪裡不一樣，從頭到尾沒有讀出任何一顆資料球。'],
      actions=[(0, 0.2, NO_AUTO), (0, 3.3, ('sel', '#g10steps button:nth-child(3)'))],
      points=[('一顆翻轉', '兩塊格子亮起'), ('白線配對', '最短路經過中間'), ('補一次翻轉', '沒讀出任何資料')], shot=(1, 4.6)),
 dict(key='fooled', after=8, page='tr', hash='surface', scene=S_SURF,
      title='動畫展示：錯兩顆，解碼器被騙', sub='三維動畫：表面碼的邏輯錯誤',
      sentences=[
       '回到表面碼章節，選第六步：相鄰的兩顆球一起被翻轉成紅色，它們共用的格子反而沒亮，只有邊上一塊半圓形格子亮起來。',
       '解碼器只看到一個亮點，白線一閃，它猜是同一排的第三顆出錯，就去翻了它。',
       '結果三顆全變紅，連成一條紅線，格子全都不亮，跳出邏輯錯誤的紅字。'],
      actions=[(0, 0.2, NO_AUTO), (0, 2.4, ('sel', '#g10steps button:nth-child(6)'))],
      points=[('相鄰兩顆翻轉', '只亮一塊邊格'), ('解碼器猜錯', '去翻第三顆'), ('三顆全翻', '邏輯錯誤')], shot=(2, 2.0)),
])

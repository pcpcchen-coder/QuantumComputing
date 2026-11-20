"""Q097 導覽：一顆 transmon 的十二章旅程 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/transmon-3d.html#chip（第 1 章：晶片，CH[0]）
  載入 #chip 時預設在「晶片總覽」分頁（c1A），「顯示標籤」預設勾選；章節列（#rail，01 晶片 … 12 軟體堆疊）在畫面下方。
  按鈕 id = c1pulse「送出 π 脈衝」：xyT = 0，六顆青綠色小球（xyPulses，COL.teal）沿 XY 驅動線從晶片邊緣跑向十字板，
     xyT·1.4 > 1（約 0.7 s）時 excite = 1，十字板發金光（mat.pad emissive 金色＋padLight），約 1.1 s 時小球消失；
     之後每幀 excite *= exp(−dt/6)：金光以約 6 秒的時間常數慢慢變暗（示意 T₁ 衰減回 |0⟩）。
  按鈕 id = c1tabB「大十字電容的作用」：setCapView(true)；鏡頭目標移到 CAPVIEW（平滑移動），隱藏總覽標籤，
     顯示四隻手臂標籤（上臂→讀取共振腔、左臂→XY 驅動線、右臂→鄰近位元／耦合器（示意）、下臂→SQUID→接地）、
     右臂旁多一條耦合器線，青綠色電場線出現在十字板與接地面的間隙；fieldMat.opacity = 0.3 + 0.7·cos²(1.6T)，
     JJ 發光 = 0.3 + 2.2·(1 − cos²(1.6T))：電場線與 JJ 約每 2 秒輪流發亮（連續效果，與時間點無關）。
  注意：transmon-3d.html 的每幀 dt 限在 0.05 s，且沒有 App.speed 可補償；錄影時本頁會落後 3–9 秒。
     因此旁白只描述「按下之後會出現、且會持續一段時間」的畫面（金光慢慢變暗、電場線持續輪流發亮），不描述逐步變化的時間點。
"""
LESSON = 'Q097'


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

S_CHIP = 'transmon 3D 第 1 章：晶片'

DEMOS = _Demos([
 dict(key='chip', after=3, page='tr', hash='chip', scene=S_CHIP,
      title='動畫展示：一顆位元的俯視圖', sub='三維動畫：晶片總覽與微波脈衝',
      sentences=[
       '打開超導晶片的三維動畫，停在第一章，從斜上方俯看一顆位元：灰色的接地面中央有一塊十字形的金屬板，後方是一條蜿蜒的共振腔，畫面下方是一整排十二個章節。',
       '按下送出脈衝的按鈕，一串青綠色的小點沿著驅動線跑向十字板，十字板接著亮起金色的光，代表位元被激發到一。',
       '這道金光不會一直亮著，它會慢慢變暗，表示位元自己衰減回零，這段時間就是之後會學到的能量鬆弛時間。'],
      actions=[(1, 2.0, ('id', 'c1pulse'))],
      points=[('十字金屬板', '就是大電容'), ('送出脈衝', '十字板亮起金光'), ('金光變暗', '衰減回零')], shot=(2, 0.5)),
 dict(key='arms', after=6, page='tr', hash='chip', scene=S_CHIP,
      title='動畫展示：十字板的四隻手臂', sub='三維動畫：大十字電容的作用',
      sentences=[
       '回到第一章，切到大十字電容的作用這一頁，鏡頭移近十字板，四隻手臂旁邊各出現一個說明標籤。',
       '上臂接讀取共振腔，左臂接驅動線，下臂經過兩個約瑟夫森接面接地，右臂接到鄰近的位元或耦合器，多顆位元就是這樣連在一起。',
       '十字板和接地面之間的細縫裡出現青綠色的電場線，它和中間的接面輪流發亮，代表能量在電場和接面之間來回流動。'],
      actions=[(0, 0.5, ('id', 'c1tabB'))],
      points=[('四隻手臂', '各接一樣東西'), ('右臂', '連到鄰近位元'), ('電場線', '和接面輪流發亮')], shot=(2, 3.0)),
])

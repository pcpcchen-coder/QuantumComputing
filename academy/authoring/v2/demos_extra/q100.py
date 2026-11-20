"""Q100 第 2 課：transmon 怎麼寫入狀態 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/transmon-3d.html#chip（第 1 章：晶片總覽）
  按鈕 #c1pulse「送出 π 脈衝」：6 顆青綠色小球沿左邊 XY 驅動線（x −6 → −3.95）跑向十字板（xyT·1.4 > 1，約 0.7 s 模擬時間），
  到達後 excite = 1，十字板發金光（padLight 金色），之後 excite *= exp(−dt/6) 慢慢衰減。Z 磁通線從畫面下方接到 SQUID，第 1 章沒有任何動畫。
  標籤（3D 跟隨）：十字電容板 C_Σ、SQUID：兩個約瑟夫森結、讀取共振腔 ~7 GHz、饋線、XY 驅動線、Z 磁通線、接地面、基板。面板在畫面右側。
場景：animations/transmon-3d.html#control（第 4 章：用微波轉動布洛赫球）
  按鈕 id：c4xpi「X 軸 π」、c4xh「X 軸 π/2」、c4yh「Y 軸 π/2」、c4rabi「持續驅動（Rabi 振盪）」、c4r「重設 |0⟩」。
  每個脈衝動畫時長 1.1·角度/π + 0.25 s（π：1.35 s；π/2：0.8 s，模擬時間）；驅動中左側能階梯 |0⟩–|1⟩ 之間出現青色波；
  梯子長條粗細 ∝ 佔據機率（1 + 4p），|0⟩、|1⟩ 金色、|2⟩ 灰色；球上金色箭頭與金色軌跡（重設會清除軌跡）。
  X 軸 π/2：箭頭轉到世界 +z（朝鏡頭）；Y 軸 π/2：轉到世界 +x（朝右邊的 X 標籤）。
場景：animations/transmon-3d.html#case（第 6 章：三顆可調 transmon）
  先按 #c6auto 取消自動接續，再用 ('sel', '#c6steps button:nth-child(6)') 進入步驟 ⑥ 自由實驗：setPhi(ALLOC)，
  Q1 → 4.90 GHz（Φ ≈ 0.129）、Q2 留 5.10 GHz（Φ = 0）、Q3 → 5.30 GHz（Φ ≈ 0.080）；Φ ≥ 0.06 的位元 Z 線發銅光、SQUID 冒銅色箭頭。
  十字板本身是灰色，只有被激發時才發出該位元的顏色（Q1 青綠 #35b8ac）；頻率尺 4.55–5.45 GHz，Q1 是青綠色實線。
  Φ 滑桿 #c6phi0（0–0.3）沒有 #controls .slider 標籤，record_demo.js 的 'slider' 用不到，改用 'js' 以 requestAnimationFrame 拖動並觸發 input。
  以頁面模型重算 Q1（E_J,max 14.49、E_C 0.25、d 0.013 GHz）：Φ 0.129 → 4.90、0.144 → 4.84、0.156 → 4.79、0.2 → 4.58 GHz；
  途中經過 Q2 的 1→2（4.817 GHz，判定窗 ±25 MHz）時頻率尺閃紅色帶、Q1 與 Q2 周圍閃紅圈（6 秒拖動中約 1 秒）。
  'π → Q1'（[data-pi="0"]）：Q1 色小球沿後方 XY 線跑到 Q1，applyPi 以 Q1 當下頻率驅動 → Q1 激發；Q2 失諧約 520 MHz，P < 1%。
  激發依 exp(−dt/14) 衰減（放慢以便觀察）。
  transmon 頁面沒有 App.speed（FPS_FIX 不適用）；dt 上限 0.05 s，負載高時落後約 3–9 s，旁白避免精確對時，也不念左上方字幕與面板讀數。
"""
LESSON = 'Q100'


class _Demos(list):
    def keys(self):
        return [LESSON]

    def items(self):
        return [(LESSON, list(self))]

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


# 幀率補償（同 q004.py）：core.js 把每幀 dt 限在 0.05 秒，負載高時動畫會落後旁白。
# transmon-3d.html 沒有 App.speed，本課三段都在 transmon 頁面，所以不使用。
FPS_FIX = ('js', "(()=>{if(window.__qfps)return;window.__qfps=1;let n=0,t0=performance.now();"
                 "const f=(now)=>{n++;if(now-t0>=1000){App.speed=Math.min(8,Math.max(1,20*(now-t0)/1000/n));n=0;t0=now;}"
                 "requestAnimationFrame(f);};requestAnimationFrame(f);})()")

# 第 6 章自由實驗：把 Q1 的 Φ 滑桿從配置值 0.129 用 6 秒拖到 0.2（牆鐘時間）
Q1_SWEEP = ('js', "(()=>{const s=document.getElementById('c6phi0');if(!s)return;const l=s.closest('label')||s;"
                  "const a=0.129,b=0.2,t0=performance.now(),D=6000;l.classList.add('qflash');"
                  "const f=(n)=>{const u=Math.min(1,(n-t0)/D);s.value=a+(b-a)*u;s.dispatchEvent(new Event('input'));"
                  "if(u<1)requestAnimationFrame(f);else l.classList.remove('qflash');};requestAnimationFrame(f);})()")

S_CHIP = 'transmon 3D 第 1 章：一顆 transmon 的俯視圖'
S_CTRL = 'transmon 3D 第 4 章：用微波轉動布洛赫球'
S_CASE = 'transmon 3D 第 6 章：三顆可調 transmon 的頻率配置'

DEMOS = _Demos([
 dict(key='chip', after=3, page='tr', hash='chip', scene=S_CHIP,
      title='動畫展示：寫入走的是哪一條線', sub='三維動畫：晶片總覽與 XY 微波脈衝',
      sentences=[
       '打開傳輸子三維動畫的第一章，畫面上的標籤指出每個零件：中央是十字電容板，左邊伸進來的是微波驅動線，從下方接到兩個接面旁邊的，是調頻磁通線。',
       '按下送出脈衝，一串青綠色的小點沿著左邊的驅動線跑到十字板旁邊，十字板接著亮起金色的光，代表位元被寫成了一。',
       '整個過程裡，下方的磁通線都沒有動靜；之後金光會慢慢變暗，那是位元自己衰減回零，也不是磁通線做的事。'],
      actions=[(1, 1.0, ('id', 'c1pulse'))],
      points=[('左邊驅動線', '送出微波脈衝'), ('十字板發金光', '被寫成一'), ('下方磁通線', '沒有參與寫入')], shot=(2, 1.0)),
 dict(key='rotate', after=5, page='tr', hash='control', scene=S_CTRL,
      title='動畫展示：轉幾度、繞哪一軸', sub='三維動畫：π、π/2 脈衝與微波相位',
      sentences=[
       '換到第四章，畫面中間是布洛赫球，金色箭頭指向上方的零；左邊是一道能階梯，下面兩階是零和一，最上面灰色的那階是二。',
       '送一個轉一百八十度的脈衝，零和一之間出現一道青綠色的波，箭頭從上方一路轉到下方的一，梯子上代表一的那階變粗、代表零的那階變細，灰色的二沒有變化。',
       '按重設回到零，再送一個只轉九十度的脈衝，箭頭停在赤道上、朝向我們這一側，零和一兩階一樣粗。',
       '再重設一次，換成相位差九十度的脈衝，箭頭一樣停在赤道，卻改成指向右邊；轉的角度相同，相位不同，停下的方向就不同。'],
      actions=[(0, 0.3, ('id', 'c4r')),
               (1, 0.3, ('id', 'c4xpi')),
               (2, 0.3, ('id', 'c4r')), (2, 3.0, ('id', 'c4xh')),
               (3, 0.3, ('id', 'c4r')), (3, 3.4, ('id', 'c4yh'))],
      points=[('一百八十度', '零整個翻成一'), ('九十度', '停在赤道、一半一半'), ('相位不同', '停的方向不同')], pmap=[0, 0, 1, 2], shot=(1, 7.0)),
 dict(key='xyz', after=8, page='tr', hash='case', scene=S_CASE,
      title='動畫展示：調磁通和送脈衝的差別', sub='三維動畫：三顆可調 transmon 的自由實驗',
      sentences=[
       '最後到第六章的自由實驗，晶片上排著三顆十字形的位元，每顆後方接一條微波驅動線，前方接一條調頻磁通線；最左邊那顆已經被往下調了頻率，它的磁通線發著銅色的光。',
       '先拖最左邊那顆的磁通滑桿，把磁通加大，看板右邊頻率尺上青綠色的線一路往左移，頻率變低，途中碰到鄰居的頻率時閃過一下紅色；可是那顆十字板始終是暗的。',
       '接著送一個一百八十度脈衝給最左邊那顆，青綠色的小點沿著後方的驅動線跑過去，十字板亮起青綠色的光，中間那顆仍然是暗的。',
       '兩種操作的差別一目了然：調磁通只是把位元搬到另一個頻率，送脈衝才真正改變了它的狀態。'],
      actions=[(0, 0.3, ('id', 'c6auto')), (0, 1.5, ('sel', '#c6steps button:nth-child(6)')),
               (1, 1.0, Q1_SWEEP),
               (2, 0.3, ('sel', '[data-pi="0"]'))],
      points=[('拖磁通滑桿', '頻率線左移、十字板不亮'), ('送一百八十度脈衝', '十字板亮起'), ('分工', '磁通管頻率、脈衝管狀態')], pmap=[0, 0, 1, 2], shot=(2, 6.0)),
])

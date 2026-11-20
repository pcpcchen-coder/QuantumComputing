"""Q077 光子量子電腦 — v2 動畫展示段（格式見 ../demos.py 的說明）。

學程沒有光子平台的簡報或場景（課綱標為需新增），只選一段真正相關的現有場景：
場景：animations/operation.html#interference（js/operation/08_interference.js）
  模式 A「單一量子位元：兩條路徑」：|0⟩ 起點經 H 分成上下兩條路，|1⟩ 路上有紫色方塊「相位 φ」，第二個 H 合併到兩個大圓盤
  「結果 |0⟩」（右上）、「結果 |1⟩」（右下）；藍、橙箭頭是兩條路的貢獻，白色是總和；兩出口上方顯示 P(0)、P(1)。
  控制：radio「單一量子位元：兩條路徑」／「3 位元：8 條路徑（Deutsch–Jozsa）」；滑桿「A：相位 φ」0–360；
        toggle「A：自動掃描 φ」、「A：中途偵測路徑（破壞干涉）」。
  偵測路徑開啟：中間出現白色小球（紅色自發光）與標籤「偵測路徑中」，白色總和箭頭隱藏，P(0)=P(1)=0.50。
  右下小圖：P(0)=cos²(φ/2) 曲線，白點標示目前 φ。
  這張圖的數學和兩路（馬赫–曾德）干涉儀相同：兩個 H 對應兩片分光鏡，相位 φ 對應相位器。
"""
LESSON = 'Q077'


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

S_INT = '3D 場景 8：干涉'

DEMOS = _Demos([
 dict(key='mzi', after=6, page='op', hash='interference', scene=S_INT,
      title='動畫展示：把干涉圖當成光路', sub='三維動畫：兩條路徑、相位與偵測路徑',
      sentences=[
       '打開操作動畫的干涉場景，左邊的起點分成上下兩條路，下面那條路上的紫色方塊是相位，右邊兩個大圓盤是兩個出口；把兩個哈達瑪閘想成兩片分光鏡，它就是一台兩路干涉儀。',
       '相位是零的時候，右上出口的白色總和箭頭最大，右下出口的機率是零，就像光子一定從同一個出口出來。',
       '把相位器從零度轉到一百八十度，白色箭頭換到右下出口，光子改從另一個出口出來，右下角小圖的白點沿著曲線滑下去。',
       '最後打開中途偵測路徑，兩條路中間出現一顆標著偵測路徑中的小球，白色總和箭頭不見了，兩個出口變回各一半。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.3, ('click', '單一量子位元')), (0, 0.5, ('slider', 'A：相位 φ', 0)),
               (2, 0.5, ('sweep', 'A：相位 φ', 0, 180, 6.0)),
               (3, 2.0, ('toggle', 'A：中途偵測路徑', True))],
      points=[('相位零度', '光子走同一個出口'), ('轉到一百八十度', '換另一個出口'), ('偵測路徑', '兩個出口各一半')], shot=(2, 7.5)),
])

"""Q080 平台大比較與供電分析 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/atoms.html#compare（js/atoms/13_compare.js）
  單選按鈕：連接性、閘速度、相干時間、規模（預設連接性）；按鈕：↻ 重播
  色彩：超導 藍 0x4f8cff（左，晶片＋稀釋冷凍機）、離子阱 金 0xffc04a（中，八顆離子鏈）、中性原子 青 0x38d6e9（右，6×6 陣列，四顆被粉紅光鑷來回拉動）
  連接性：超導相鄰耦合線閃爍；離子之間 28 條弧線（全連接）；原子搬運
  閘速度：1000 個兩位元閘，動畫 1 秒 = 真實 20 ms → 超導（50 μs）與中性原子（0.3 ms）幾乎瞬間到頂，離子阱（0.1 s）約 5 秒才到頂（速度 1×）
  相干時間：log₁₀(T₂／閘時間)：超導 3.3、離子阱 4、中性原子 6.5（標籤：計入搬運約 10³–10⁴）；柱子約 0.7 秒升到位
  規模：log₁₀：超導 1121 → 3.05、離子阱 98 → 1.99、中性原子 6100 → 3.79；標籤 Willow 105、Condor 1121、Helios 98、Caltech 6100
  右下角小圖（#inset-wrap，畫面上）：時間尺度比較：兩位元閘、讀取、T₂ 三列，三色點，log 座標
場景：animations/power1000.html#outage（場景 5：斷電時間軸；只畫超導）
  下拉選單「備援方案」：none（A：只有控制電子接 UPS，預設）、full（B：冷卻鏈 UPS＋發電機接手）、gen（C）
  曲線：混合腔溫度，對數時間 1 秒～10 天；A：約 120 秒超過 1 K 紅色虛線，1 小時後恢復供電、約 3.5 天降回；B：維持 10 mK 平線
  白點約每 12.6 秒循環一次；下拉選單沒有按鈕，用 ('js', …) 改值並觸發 change
"""
LESSON = 'Q080'


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

# power1000.html 的下拉選單沒有按鈕可按：改值後觸發 change（等同使用者選取）
OUTAGE_FULL = ('js', "(()=>{const s=document.querySelector('#controls select');s.value='full';s.dispatchEvent(new Event('change'));})()")

S_CMP = '離子阱與中性原子場景 13：三平台比較'
S_OUT = '1000 位元供電場景 5：斷電時間軸'

DEMOS = _Demos([
 dict(key='speed', after=4, page='at', hash='compare', scene=S_CMP,
      title='動畫展示：比速度，也比比值', sub='三維動畫：三平台比較（閘速度與相干時間）',
      sentences=[
       '打開離子阱與中性原子動畫的三平台比較場景，左邊藍色是超導晶片和冷凍機，中間金色是一串離子，右邊青色是原子陣列。',
       '按閘速度，三根柱子開始比賽連續做一千個兩位元閘：超導和中性原子的柱子一下子就到頂，離子阱的柱子要慢慢爬上去。',
       '再按相干時間，柱子改成比失去相干前能做幾個閘，這次離子阱超過了超導，中性原子最高，但標籤提醒，算進搬運就只剩一千到一萬。',
       '右下角的小圖把閘、讀取和相干時間畫在同一把對數尺上，三種顏色的點，彼此相差好幾個數量級。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.3, ('click', '連接性')),
               (1, 0.4, ('click', '閘速度')),
               (2, 0.4, ('click', '相干時間'))],
      points=[('閘速度', '超導最快，離子阱最慢'), ('相干時間 ÷ 閘時間', '排名換了'), ('對數小圖', '差好幾個數量級')], shot=(2, 6.0)),
 dict(key='connect', after=5, page='at', hash='compare', scene=S_CMP,
      title='動畫展示：誰連得到誰', sub='三維動畫：三平台比較（連接性與規模）',
      sentences=[
       '回到三平台比較場景，按連接性：超導晶片上只有相鄰量子位元之間的耦合線在閃，代表只能和鄰居做閘。',
       '中間的離子之間，每一對都有一條弧線相連，代表同一條鏈裡任兩顆都能直接做閘；右邊幾顆原子正被粉紅色的光鑷拉著來回移動。',
       '再按規模，比的是已經展示過的量子位元或原子數，用對數畫柱子：中性原子最高，標籤寫著加州理工學院的六千一百顆陣列，離子阱大約一百顆。'],
      actions=[(0, 0.1, FPS_FIX), (0, 2.6, ('click', '連接性')),
               (2, 0.4, ('click', '規模'))],
      points=[('超導', '只連最近鄰'), ('離子阱', '任兩顆都有弧線'), ('中性原子', '光鑷搬運、數量最多')], shot=(1, 6.0)),
 dict(key='outage', after=8, page='pw', hash='outage', scene=S_OUT,
      title='動畫展示：超導斷電的代價', sub='互動動畫：斷電時間軸（教學示意曲線）',
      sentences=[
       '換到一千位元供電動畫的斷電時間軸，這一頁只畫超導：橫軸是從一秒到十天的對數時間，曲線是稀釋冷凍機混合腔的溫度。',
       '預設方案只有控制電子接不斷電系統，曲線在兩分鐘附近衝過一克耳文的紅色虛線，要過好幾天才降回原來的溫度。',
       '把備援方案換成冷卻鏈接不斷電系統、再由發電機接手，整條曲線變成平的，溫度一直停在十毫克耳文。'],
      actions=[(2, 4.5, OUTAGE_FULL)],
      points=[('只保控制電子', '兩分鐘就超過一克耳文'), ('恢復', '要好幾天'), ('保住冷卻鏈', '溫度不動')], shot=(1, 5.0)),
])

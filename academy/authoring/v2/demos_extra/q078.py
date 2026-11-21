"""Q078 半導體自旋量子位元 — v2 動畫展示段（格式見 ../demos.py 的說明）。

學程目前沒有半導體自旋／量子點場景（課綱標為 需新增），所以只用一段真正相關的既有場景：
場景：animations/atoms.html#compare（js/atoms/13_compare.js）三平台比較：超導 · 離子阱 · 中性原子
  單選按鈕：連接性（預設）、閘速度、相干時間、規模；另有「↻ 重播」
  最左邊（藍）是超導，旁邊標「10 mK 稀釋冷凍機」；這正是孩子下半場要拿來和自旋量子位元比較的對象
  閘速度：柱子依真實時間爬升（動畫 1 秒 = 20 ms）；超導 50 μs、中性原子 0.3 ms 幾乎瞬間到頂，離子阱 0.1 s 約需 5 秒（速度 1×）
  相干時間：柱高 = log₁₀(T₂ / 兩位元閘時間)，超導 ≈ 2×10³ 最矮，離子阱 ≈ 10⁴、中性原子 ≈ 3×10⁶；柱高約 0.7 秒內長到位
  場景裡沒有自旋量子位元那一欄；旁白只說「還沒有這一欄」，不描述不存在的畫面
"""
LESSON = 'Q078'


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

S_CMP = '原子場景 13：三平台比較'

DEMOS = _Demos([
 dict(key='compare', after=10, page='at', hash='compare', scene=S_CMP,
      title='動畫展示：先認識比較的對手', sub='三維動畫：超導、離子阱、中性原子的閘速度與相干時間',
      sentences=[
       '打開離子阱與中性原子動畫的三平台比較場景，最左邊藍色的是超導，中間金色的是離子阱，右邊青色的是中性原子。',
       '按閘速度，比的是連做一千個兩位元閘要多久：超導和中性原子的柱子一瞬間就衝到頂，離子阱的柱子要好幾秒才慢慢爬滿。',
       '再按相干時間，比的是量子資訊消失之前能做幾個閘，超導的柱子最矮，大約只有兩千個。',
       '這張比較圖還沒有半導體自旋這一欄，下半場就由你替它補上尺寸和工作溫度。'],
      actions=[(0, 0.1, FPS_FIX), (1, 0.4, ('click', '閘速度')), (2, 0.4, ('click', '相干時間'))],
      points=[('三個平台', '藍、金、青三種顏色'), ('閘速度', '超導一瞬間做完'), ('相干時間', '超導的柱子最矮')], shot=(1, 7.0)),
])

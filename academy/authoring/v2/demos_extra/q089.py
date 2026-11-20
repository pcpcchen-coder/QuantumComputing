"""Q089 最佳化與機器學習：炒作與現實 — v2 動畫展示段（格式見 ../demos.py 的說明）。

只選一段真正相關的場景：平方加速的極限（Grover 類方法是最佳化地圖上唯一有證明的加速，而且只是平方）。
場景：animations/operation.html#grover（js/operation/09_grover.js）
  滑桿：量子位元數 n（2–6，預設 4；改動時呼叫 setup() 重設柱子與輪數）、答案（標記的項目）（預設 11）
  按鈕：② Oracle、③ 擴散、完整一輪、自動跑到最佳次數、測量、重設
  「自動跑到最佳次數」：先 setup()，之後每 0.8 秒（速度 1×）交替做 Oracle／擴散，做滿 kOpt 輪就停
  kOpt = max(1, round(π/(4θ) − 0.5))，sin θ = 1/√N：
    n = 4（N = 16）→ 3 輪（6 步 ≈ 4.8 s），答案機率 sin²(7θ) ≈ 0.961，其他振幅 ≈ −0.05
    n = 6（N = 64）→ 6 輪（12 步 ≈ 9.6 s），答案機率 sin²(13θ) ≈ 0.997
  柱子＝振幅：正值金色 0xe0a54a、負值藍色 0x4f8cff；答案柱底下有綠青色框（0x66ffcc）與「答案」標籤
  右下插圖（固定在畫面右下角，380×230）：左半是「答案–非答案」平面的轉角，右半是 P(成功) vs 輪數曲線
  （橫軸 0 到 2·kOpt+1，曲線先升後降，白點標出目前輪數）
  古典平均查 N/2 次：16 → 8、64 → 32（場景副標「古典平均 N/2 次，量子約 (π/4)√N 次」）
"""
LESSON = 'Q089'


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

S_GROVER = '3D 場景 9：Grover 搜尋'

DEMOS = _Demos([
 dict(key='sqrtlimit', after=4, page='op', hash='grover', scene=S_GROVER,
      title='動畫展示：平方加速有多少', sub='三維動畫：格羅弗搜尋的輪數和候選數',
      sentences=[
       '打開三維動畫的格羅弗搜尋場景，十六根柱子代表十六個候選，綠框圍住的是答案；按下自動跑到最佳次數，答案那根柱子一輪一輪被拉高，大約三輪之後，其他柱子幾乎縮到零。',
       '再把量子位元數拉到六，柱子變成六十四根，再按一次自動跑，這次答案柱子要一輪一輪爬升，經過大約六輪，才被拉到最高。',
       '候選多了四倍，輪數只多了一倍；古典方法平均要翻一半的候選，從八次變成三十二次，這就是平方加速，不是指數加速。',
       '右下插圖畫著成功機率和輪數的關係，曲線升到最高之後又往下掉，而且這還是完全沒有雜訊的理想情況。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.3, ('slider', '量子位元數', 4)), (0, 0.8, ('click', '重設')),
               (0, 9.0, ('click', '自動跑到最佳次數')),
               (1, 0.8, ('slider', '量子位元數', 6)), (1, 2.6, ('click', '自動跑到最佳次數'))],
      points=[('十六個候選', '大約三輪找到答案'), ('六十四個候選', '大約六輪，不是十二輪'), ('平方加速', '轉過頭反而變差')], shot=(3, 3.0)),
])

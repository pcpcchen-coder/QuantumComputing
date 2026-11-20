"""Q088 量子化學與材料 — v2 動畫展示段（格式見 ../demos.py 的說明）。

學程沒有化學／分子專用場景；只選一個真正相關的場景：
場景：animations/operation.html#register（js/operation/04_register.js）
  滑桿：量子位元數 n（1–4，步進 1，預設 2）；改動時重建布洛赫球與 2ⁿ 根振幅柱
  按鈕：目標 q0–q3、H、X、Z、S、T、CNOT（控制 = 目標+1 → 目標）、CZ、均勻疊加 H⊗ⁿ、Bell 態、GHZ 態、測量全部、只測 q0、重設 |0…0⟩
  右下插圖（畫在畫布上）：「精確模擬 n 個量子位元所需記憶體（2ⁿ × 16 bytes）」，金色曲線 0–60 位元；
    青色點標 30 位元「16 GB（筆電）」、40 位元「16 TB（大型伺服器）」、50 位元「18 PB」；紅色虛線「頂級超級電腦總記憶體 ≈ 10 PB」
  均勻疊加：每個量子位元做 H，2ⁿ 根柱子等高（金色 = 正相位）
"""
LESSON = 'Q088'


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

S_REG = '3D 場景 4：多位元與糾纏'

DEMOS = _Demos([
 dict(key='wall', after=3, page='op', hash='register', scene=S_REG,
      title='動畫展示：一般電腦撞上的那道牆', sub='三維動畫：二的幾次方個振幅與模擬所需記憶體',
      sentences=[
       '打開操作動畫的多位元場景，把量子位元數從一拉到四，下面的柱子從兩根、四根、八根，一路變成十六根。',
       '按下均勻疊加，十六根柱子變得一樣高；每多一個量子位元，要記住的數字就多一倍。',
       '右下插圖畫出用一般電腦精確記住這些數字要多少記憶體：三十個量子位元大約十六吉位元組，筆電還放得下。',
       '到了五十個量子位元要十八拍位元組，橘色斜線已經越過紅色虛線，也就是頂級超級電腦的總記憶體；分子裡的電子一多，也會撞上同一道牆。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.3, ('slider', '量子位元數 n', 1)), (0, 3.5, ('sweep', '量子位元數 n', 1, 4, 6.0)),
               (1, 0.8, ('click', '均勻疊加'))],
      points=[('多一個位元', '柱子多一倍'), ('三十個位元', '約 16 GB，筆電放得下'), ('五十個位元', '超過超級電腦記憶體')],
      shot=(2, 3.0)),
])

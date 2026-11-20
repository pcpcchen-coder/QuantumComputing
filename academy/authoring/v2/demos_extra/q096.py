"""Q096 畢業 Teach-back：換孩子教爸爸 — v2 動畫展示段（格式見 ../demos.py 的說明）。

本課沒有專屬場景（課綱素材欄：沒有可直接沿用的頁面；「發表模板」需新增、未實作）。
只放一段「示範怎麼用場景教人」：先讓爸爸預測，再操作，再請孩子用一句話解釋。

場景：animations/operation.html#interference（js/operation/08_interference.js）
  單選：單一量子位元：兩條路徑（預設 A）、3 位元：8 條路徑（Deutsch–Jozsa）
  滑桿：A：相位 φ（0–360，預設 0）；開關：A：自動掃描 φ、A：中途偵測路徑（破壞干涉）（預設關）
  右側兩個結果圓：結果 |0⟩（上，x=3.5,y=1.6）、結果 |1⟩（下，y=-1.6），各有藍、橙貢獻箭頭與白色總和箭頭，金色標籤 P(0)／P(1)
    φ=0：上方白箭頭最長、下方為零；φ=180：反過來
  插圖「結果 P(0) 與 φ 的關係（干涉條紋）」：金色曲線 cos²(φ/2)、紅色虛線 0.5、白點標目前 φ
  中途偵測路徑開啟：中間 (-1,0) 出現發紅光的白色小球，白色總和箭頭隱藏，白點落到 0.5 紅虛線上
"""
LESSON = 'Q096'


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

S_INT = '操作場景 8：干涉'
PHI = 'A：相位 φ'

DEMOS = _Demos([
 dict(key='teachdemo', after=6, page='op', hash='interference', scene=S_INT,
      title='動畫展示：先預測，再操作', sub='三維動畫：用干涉場景示範一段教學',
      sentences=[
       '示範一段換孩子教爸爸的教學：孩子打開干涉場景，先不動任何東西，問爸爸右邊兩個結果各會出現多少。',
       '爸爸猜完，孩子再把相位從零慢慢轉到一百八十度，上面結果零的白色總和箭頭越縮越短，下面結果一的白色箭頭越變越大，插圖上的白點沿著曲線滑到最低。',
       '接著打開中途偵測路徑，中間冒出一顆發紅光的小球，兩個白色總和箭頭都不見了，插圖的白點跳到一半高的紅色虛線上。',
       '最後請孩子用一句話解釋剛才看到的變化，說得出為什麼，才算真的教會了。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.5, ('slider', PHI, 0)),
               (1, 3.5, ('sweep', PHI, 0, 180, 8.0)),
               (2, 2.0, ('toggle', 'A：中途偵測路徑', True))],
      points=[('先問', '讓爸爸預測結果'), ('再轉相位', '白箭頭換到另一邊'), ('偷看路徑', '干涉消失，一半一半')], pmap=[0, 1, 2, 2], shot=(1, 14.0)),
])

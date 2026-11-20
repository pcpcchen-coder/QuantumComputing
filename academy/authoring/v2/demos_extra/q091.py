"""Q091 Shor 之後：後量子密碼 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/operation.html#shor（js/operation/10_shor.js）
  按鈕：N = 15、N = 21（ui.radio）；a = 2、a = 4、a = 7、a = 8 …（依 N 動態產生，N = 15 預設 a = 7）；下一步 ▶、自動播放、重設
  柱子：64 根代表 x 暫存器 0–63；每次狀態改變後以 1 − exp(−6·dt) 平滑，約 0.5–1 秒到位
  步驟（手動按「下一步」，沒有排隊時間）：
    0 初始：只有 x = 0 一根柱子（金色）
    1 H⊗⁶：64 根同高（高度縮為 0.35）
    2 計算 f(x)：柱子依 f(x) 上色（N = 15、a = 7 → 1、7、4、13 四色，每 4 根一循環）
    3 量測第二暫存器：隨機選一個 f 值，只留下間隔 4 的 16 根（哪一種顏色是隨機的，間隔固定）
    4 QFT：青色峰值，N = 15、a = 7 時恰在 0、16、32、48（各 1/4，其他位置為 0），峰上有青色數字標籤
    5 量測：隨機一根峰值變白色（可能是 0；連分數結果只在左側讀數，不在畫面上）
  右下插圖：f(x) = aˣ mod N（週期函數），標題下寫「a = 7，週期 r = 4」；步驟 ≥ 3 時被選中的 f 值點變白
  畫面上方金色字：目前步驟名稱
"""
LESSON = 'Q091'


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

S_SHOR = '3D 場景 10：Shor 週期尋找'

DEMOS = _Demos([
 dict(key='period', after=4, page='op', hash='shor', scene=S_SHOR,
      title='動畫展示：用干涉找出週期', sub='三維動畫：秀爾演算法分解十五',
      sentences=[
       '打開三維動畫的秀爾週期尋找場景，選十五當作要分解的數，一開始只有最左邊一根柱子；右下的小圖畫出七的次方除以十五的餘數，每四個一循環。',
       '按下一步，六十四根柱子變得一樣高，代表零到六十三同時存在；再按一次，柱子染上四種顏色，每四根一個循環，顏色就是算出來的餘數。',
       '再按下一步，量一下第二個暫存器，畫面只剩同一種顏色的柱子，彼此間隔四格，像一把梳子。',
       '接著按下一步做量子傅立葉轉換，梳子變成四根青色的高峰，停在零、十六、三十二和四十八，其他位置都被干涉抵消；最後再按一次量測，其中一根高峰變成白色，交給古典電腦去推算週期。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.3, ('click', 'N = 15')), (0, 0.8, ('click', '重設')),
               (1, 0.3, ('click', '下一步')), (1, 6.8, ('click', '下一步')),
               (2, 0.3, ('click', '下一步')),
               (3, 0.3, ('click', '下一步')), (3, 12.9, ('click', '下一步'))],
      points=[('疊加與上色', '餘數每四根一循環'), ('量測第二暫存器', '間隔四格的梳子'), ('量子傅立葉轉換', '高峰在零、十六、三十二、四十八')],
      shot=(3, 8.0)),
])

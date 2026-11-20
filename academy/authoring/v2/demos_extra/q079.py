"""Q079 拓樸量子位元與 NV 色心 — v2 動畫展示段（格式見 ../demos.py 的說明）。

學程沒有拓樸量子位元、編織或 NV 色心的場景（課綱標為「需新增」），本課只放一段真正相關的展示：
表面碼本身是一種拓樸量子錯誤更正碼（Wikipedia: Toric code），只有貫穿上下邊界的錯誤鏈才會變成邏輯錯誤。

場景：animations/operation.html#qec（js/operation/11_qec.js）
  單選按鈕：d = 3、d = 5、d = 7（按下會呼叫 setup()：清空錯誤、phase 歸零、統計歸零）
  滑桿：實體錯誤率 p（每個資料量子位元）（0.005–0.2，預設 0.05）
  開關：自動循環（預設開，每 0.9 s 走一步）；按鈕：下一步、跑 2000 輪（只統計）
  下一步的順序：① 隨機錯誤（紅球）→ ② 量測穩定子（症狀方塊亮橘、豎起橘柱）→ ③ 解碼（綠線）→ ④ 修正並判定 → 清空
  d = 7、p = 8%：49 顆資料量子位元，一顆錯誤都沒有的機率約 0.92⁴⁹ ≈ 1.7%；旁白不宣稱任何特定的隨機結果
"""
LESSON = 'Q079'


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

S_QEC = '3D 場景 11：雜訊與量子錯誤更正（表面碼）'

DEMOS = _Demos([
 dict(key='surface', after=3, page='op', hash='qec', scene=S_QEC,
      title='動畫展示：只怕貫穿整片的錯誤', sub='三維動畫：表面碼——一種拓樸錯誤更正碼',
      sentences=[
       '打開操作動畫的錯誤更正場景，白球是資料量子位元，下面的方塊負責檢查附近的奇偶，這套排法叫做表面碼。',
       '先關掉自動循環，把碼距換成七，實體錯誤率調到百分之八，再按下一步，畫面上冒出紅球，代表隨機發生的錯誤。',
       '再按一次，錯誤附近的方塊亮成橘色、豎起柱子，這是症狀；再按一次，綠線把症狀兩兩配對或連到邊界，這是解碼器的猜測。',
       '最後按下一步完成修正，橘柱全部消失；畫面上可能還留著紅球，但只要它們沒有連成一條從上邊界貫穿到下邊界的鏈，資訊就沒有壞，這種只看整體連法的保護，就是拓樸的想法。'],
      actions=[(0, 0.1, FPS_FIX),
               (1, 0.3, ('toggle', '自動循環', False)), (1, 2.2, ('click', 'd = 7')),
               (1, 4.6, ('slider', '實體錯誤率', 0.08)), (1, 8.4, ('click', '下一步')),
               (2, 0.3, ('click', '下一步')), (2, 7.0, ('click', '下一步')),
               (3, 0.3, ('click', '下一步'))],
      points=[('紅球', '隨機發生的錯誤'), ('橘柱與綠線', '症狀與配對'), ('貫穿上下', '才會壞掉資訊')], shot=(2, 10.0)),
])

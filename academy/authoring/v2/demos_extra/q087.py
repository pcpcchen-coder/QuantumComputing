"""Q087 變分演算法：VQE 與 QAOA — v2 動畫展示段（格式見 ../demos.py 的說明）。

課綱的「★ 變分能量地形場景」尚未製作（需新增），本集只用現有、真正相關的兩個操作場景：
場景：animations/operation.html#gates（js/operation/02_gates.js）
  按鈕：X Y Z H／S S† T T† √X；Rx(θ)、Ry(θ)、Rz(θ)；重設 |0⟩、重設 |1⟩、清除軌跡；兩個示範
  滑桿：旋轉角 θ（給 Rx / Ry / Rz）−180–180，步進 5，預設 90；動畫速度 0.3–3（預設 1×）
  每個閘排隊執行，時間 (0.5 + |角度|/π × 0.8) / 速度 秒：45° → 0.7 s；粉紅線為旋轉軸（附標籤「旋轉軸 · Ry(45°)」），
  球上留軌跡（trailN 900）；右下插圖「最後一個閘的矩陣與線路紀錄」：線路方塊顯示標籤前兩字（Ry），重設會清空
  Ry 從 |0⟩ 出發：每次 45°，四次 = 180° → 南極（|1⟩）
場景：animations/operation.html#qubit（js/operation/01_qubit.js）
  滑桿：θ（極角）0–180（改動會清空統計）；按鈕：測量一次、連續 shots、清除統計、一次跑 1000 shots、|0⟩ |1⟩ |+⟩ |+i⟩ θ=60°
  右側統計柱：藍 = 得到 0、紅 = 得到 1；青色橫線 = 理論機率 P(0) = cos²(θ/2)；柱高以指數平滑（約 0.3 s）追上
  θ = 60° → P(0) = 0.75；120° → 0.25；180° → 0（cos(π/2)² ≈ 4e−33，實際不會出現 0）
  每批 1000 次的實際比例有約 ±1.4% 的隨機誤差，旁白只說「大約」
"""
LESSON = 'Q087'


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

S_GATES = '操作場景 2：單位元量子閘'
S_QUBIT = '操作場景 1：量子位元的狀態與測量'

DEMOS = _Demos([
 dict(key='knob', after=4, page='op', hash='gates', scene=S_GATES,
      title='動畫展示：線路上的旋鈕', sub='三維動畫：可調角度的旋轉閘',
      sentences=[
       '打開操作動畫的單位元閘場景，先按重設回到零態，箭頭指向北極。',
       '把旋轉角設成四十五度，按一下有角度的旋轉閘，箭頭繞著粉紅色的旋轉軸，往下轉了四十五度。',
       '再連按三次，箭頭一格一格往下轉，最後停在南極，球面上留下一道弧形的軌跡，右下角的線路紀錄也排出四個方塊。',
       '在變分演算法裡，這個角度就是一顆旋鈕；一條線路可以有很多顆，古典電腦的工作就是決定每一顆該轉多少。'],
      actions=[(0, 0.1, FPS_FIX), (0, 3.0, ('click', '重設 |0⟩')),
               (1, 0.3, ('slider', '旋轉角 θ', 45)), (1, 2.6, ('click', 'Ry(θ)')),
               (2, 0.3, ('click', 'Ry(θ)')), (2, 0.6, ('click', 'Ry(θ)')), (2, 0.9, ('click', 'Ry(θ)'))],
      points=[('旋轉角', '一顆可以調的旋鈕'), ('每按一次', '再轉四十五度'), ('四次之後', '箭頭停在南極')], shot=(2, 6.0)),
 dict(key='loop', after=6, page='op', hash='qubit', scene=S_QUBIT,
      title='動畫展示：手動跑一圈變分迴圈', sub='三維動畫：調角度、量一千次、再調角度',
      sentences=[
       '回到量子位元場景，假裝能量就是結果零出現的比例，我們的旋鈕只有一顆，就是箭頭的極角。',
       '先把極角放在六十度，跑一千次，藍色柱子大約占四分之三，和青色的理論線差不多高。',
       '古典電腦決定把極角加到一百二十度，箭頭往南轉，再跑一千次，藍色柱子掉到大約四分之一。',
       '再調到一百八十度跑一次，藍色柱子完全消失，能量降到最低；量子負責量，古典負責調，這就是變分迴圈。'],
      actions=[(0, 0.1, FPS_FIX),
               (1, 0.3, ('click', 'θ=60°')), (1, 2.6, ('click', '一次跑 1000 shots')),
               (2, 1.8, ('slider', 'θ（極角）', 120)), (2, 4.8, ('click', '一次跑 1000 shots')),
               (3, 0.3, ('slider', 'θ（極角）', 180)), (3, 2.4, ('click', '一次跑 1000 shots'))],
      points=[('六十度', '藍柱約四分之三'), ('一百二十度', '藍柱約四分之一'), ('一百八十度', '藍柱消失')], shot=(3, 5.0)),
])

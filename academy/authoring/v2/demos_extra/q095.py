"""Q095 畢業專題製作 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/operation.html#workflow（js/operation/12_workflow.js）
  控制項：開關「自動播放」（預設開）、按鈕「下一站 ▶」（按下即關閉自動前進、stage+1；從第六站再按會回到第一站並清空計數）、
          滑桿「shots N」（預設 1000）、「線路深度（層）」、開關「主動重置（量測 + 條件 π 脈衝）」
  六站：① 寫程式、② 轉譯（藍綠）、③ 脈衝排程（紫）、④ 控制電子（橘）、⑤ 晶片執行 shots（藍）、⑥ 判別與結果（紅）
  程式螢幕：qc.h(0)、qc.cx(0, 1)、measure_all、shots=N（位於畫面左側，被控制面板擋住，旁白不描述它）
  第五站：計數在 3.5 秒內跑到 N（預設 1000），每次 50% 為 00、50% 為 11，約 4% 改記成 01 或 10；
          直方圖 00、11 為金色柱，01、10 為灰色柱，柱高 = 比例 × 2.2；在第一到第四站柱子縮回 0
  自動播放時每站 2.2 秒（第五站 3.5 秒），錄影開始時站別不確定，所以第一句用 js 重建場景（回到第一站），再關掉自動播放。
"""
LESSON = 'Q095'


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
# 重建目前場景：stage、計數歸零，封包回到第一站
RESTART = ('js', "(()=>{App.active=null;App.show(App.cur);})()")

S_FLOW = '3D 場景 12：完整流程'

DEMOS = _Demos([
 dict(key='verify', after=6, page='op', hash='workflow', scene=S_FLOW,
      title='動畫展示：跑一千次來對答案', sub='三維動畫：一次量子計算的完整流程',
      sentences=[
       '打開操作動畫的完整流程場景，先關掉自動播放，這次要送出的，正是先做哈達瑪閘、再做受控反閘的兩位元線路。',
       '每按一次下一站，發光的工作封包就往前走一站，依序經過轉譯、脈衝排程和控制電子，藍綠、紫、橘三個平台輪流亮起來。',
       '再按一次，封包進到冷凍機裡的晶片，晶片快速閃爍，上方的計數一路跑到一千次，右邊的金色柱子同時冒了出來。',
       '按到最後一站，結果送回來：零零和一一兩根金色柱子差不多一樣高，零一和一零的灰色柱子幾乎貼在地面，和事先寫下的預測對得上。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.3, RESTART), (0, 1.2, ('toggle', '自動播放', False)),
               (1, 1.5, ('click', '下一站')), (1, 4.5, ('click', '下一站')), (1, 7.5, ('click', '下一站')),
               (2, 0.4, ('click', '下一站')),
               (3, 0.3, ('click', '下一站'))],
      points=[('先寫預測', '零零、一一各一半'), ('跑一千次', '計數跑完，柱子冒出'), ('對答案', '兩根金柱差不多高')], shot=(3, 6.0)),
])

"""Q094 畢業專題提案 — v2 動畫展示段（格式見 ../demos.py 的說明）。

本課是提案課，只放一段：用範例專題（格羅弗搜尋幾輪最好）示範「看得到、量得到、對得到」的成功標準。
場景：animations/operation.html#grover（js/operation/09_grover.js）
  預設：量子位元數 n = 4（N = 16）、答案 11；柱子 = 振幅，正為金色（0xe0a54a）、負為藍色（0x4f8cff）；答案有綠框與「答案」標籤
  按鈕：② Oracle、③ 擴散、完整一輪（先 Oracle，700 ms 後擴散）、自動跑到最佳次數、測量、重設
  右下插圖：左半幾何圖，右半「P(成功) vs 輪數」曲線，目前輪數是白點（橫軸 0–7）
  決定性結果（無隨機）：第 1 輪 P ≈ 0.473、第 2 輪 ≈ 0.908、第 3 輪 ≈ 0.961（最佳 kOpt = 3）、第 4 輪 ≈ 0.582
  第 3 輪後其他振幅 ≈ −0.051（很小的藍色）；兩次「完整一輪」至少相隔 0.8 s，避免在 Oracle 階段重複排入擴散
"""
LESSON = 'Q094'


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
 dict(key='example', after=6, page='op', hash='grover', scene=S_GROVER,
      title='動畫展示：範例專題怎麼驗收', sub='三維動畫：格羅弗搜尋做幾輪最好',
      sentences=[
       '來看範例專題怎麼驗收：打開三維動畫的格羅弗搜尋場景，十六根金色柱子代表十六個抽屜，綠框那一根就是要找的答案。',
       '按一次完整一輪，答案的柱子一下子被高高拉起，比其他柱子高出許多，右下插圖的白點也沿著曲線往右上移了一格。',
       '再按兩次，做到第三輪，答案的柱子幾乎頂到最高，其他柱子都縮得很小，白點也爬到曲線的頂端附近。',
       '多按一輪變成第四輪，答案的柱子反而變矮，白點沿著曲線往下掉；做太多輪會轉過頭，正好驗證大約三輪最好。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.3, ('click', '重設')),
               (1, 1.8, ('click', '完整一輪')),
               (2, 0.3, ('click', '完整一輪')), (2, 2.4, ('click', '完整一輪')),
               (3, 1.5, ('click', '完整一輪'))],
      points=[('第一輪', '答案被拉高'), ('第三輪', '白點接近頂端'), ('第四輪', '轉過頭變矮')], pmap=[0, 0, 1, 2], shot=(2, 7.0)),
])

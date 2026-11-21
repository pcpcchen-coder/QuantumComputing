"""Q110 第 12 課：lattice surgery 與魔術態蒸餾 — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html#surgery（第 11 章）。步驟按鈕在 #g11steps（程式動態產生、沒有 id；第 8 個是「自由實驗」，
  dur 0、不會自動接續）。三段都在自由實驗裡用按鍵操作，不靠步驟 1–7 的 cue 時間軸（機器忙、幀率低時步驟腳本會比牆鐘慢）。
  自由實驗控制項（g11BindFree）：#g11vs「看 lattice surgery」、#g11vf「看魔術態工廠」、#g11prep「準備接縫」、#g11mrg「合併（量 X_A·X_B）」、
  #g11spl「拆開」、#g11rst「重設」、#g11p 滑桿（label「注入錯誤率 p」，數值是 log10 p，min -4、max -1.3、step 0.05，預設 -3）、
  [data-lv11="1"]「1 輪」、[data-lv11="2"]「2 輪」、#g11run「跑一輪」、#g11mc「跑 2000 次統計」。
  record_demo.js 的 slider 只找 #controls .slider（operation.html 用），所以本頁滑桿用 js 設值並送 input 事件。
  動畫時間依畫面幀推進（dt 上限 0.05 s）：合併每 2.4 秒量一輪、共 3 輪；拆開時接縫位元白光 1.2 秒、2.2 秒後恢復兩塊；
  蒸餾 0–1.6 秒飛入、1.6–2.8 秒四盞燈依序亮、2.8 秒起「通過！輸出錯誤率 ≈ …」與金色球、4.4 秒結束。錄影幀率低時會比牆鐘慢。
  控制項全在面板可見範圍內（1600×900 試拍），不必捲動。
"""

LESSON = 'Q110'

_STEP8 = ('sel', '#g11steps button:nth-child(8)')


def _p(v):
    """把「注入錯誤率 p」滑桿設成 log10 p = v（與手動拖動相同，觸發 input）"""
    return ('js', f"(()=>{{const s=document.getElementById('g11p');s.value={v};"
                  f"s.dispatchEvent(new Event('input'));window.__flash(s.closest('label'));}})()")


_LIST = [
 dict(key='merge', after=6, page='tr', hash='surgery', scene='transmon 3D 第 11 章：lattice surgery——自由實驗（準備接縫、合併、拆開）',
      title='動畫展示：縫起來，再拆開', sub='三維動畫：兩塊補丁合併量出聯合奇偶',
      sentences=[
       '打開超導晶片動畫第十一章，按第八步自由實驗，畫面上是左右兩塊邏輯位元補丁，中間那一行接縫位元顏色很淡，還沒有用到。',
       '按準備接縫，接縫的三顆位元亮成淡青色，旁邊標上零態；接著按合併，接縫一帶多出幾個新格子，一明一暗地閃著。',
       '上方看板一輪一輪寫出新琥珀色格子的結果，正一、負一是隨機的，但每一輪都一樣，最後的乘積就是聯合奇偶，金色標籤也寫著它。',
       '量滿三輪以後按拆開，接縫位元閃著白光被量掉，新格子跟著消失，兩塊補丁恢復獨立，看板寫著已拆開。'],
      actions=[(0, 0.5, _STEP8),
               (1, 0.3, ('id', 'g11prep')), (1, 6.0, ('id', 'g11mrg')),
               (3, 0.8, ('id', 'g11spl'))],
      points=[('準備接縫', '接縫位元重設到零態'), ('合併', '個別隨機、乘積固定'), ('拆開', '兩塊恢復獨立')], shot=(2, 9.0)),
 dict(key='distill', after=9, page='tr', hash='surgery', scene='transmon 3D 第 11 章：魔術態工廠——自由實驗（跑一輪蒸餾）',
      title='動畫展示：十五顆進，一顆出', sub='三維動畫：魔術態工廠跑一輪蒸餾',
      sentences=[
       '回到第十一章的自由實驗，按看魔術態工廠，鏡頭往右移：左邊排著十五顆橘色球，中間是蒸餾工廠，頂上有四盞還沒亮的燈。',
       '上方看板寫著，注入錯誤率千分之一，輸出約三點五乘十的負八次方，接受率百分之九十八點五；下面的柱子越矮代表越乾淨。',
       '把注入錯誤率的滑桿拉到最左邊的萬分之一，看板馬上改成輸出約三點五乘十的負十一次方，接受率超過百分之九十九點八。',
       '按跑一輪，十五顆球依序飛進工廠，頂上的燈一盞接一盞亮成青色，工廠上方寫著通過，一顆金色球滾到右邊。'],
      actions=[(0, 0.4, _STEP8), (0, 2.6, ('id', 'g11vf')),
               (2, 2.5, _p(-4)),
               (3, 0.3, ('id', 'g11run'))],
      points=[('十五顆橘色球', '注入的髒魔術態'), ('四盞燈全亮青色', '檢查全部通過'), ('一顆金色球', '乾淨的魔術態')], shot=(3, 4.2)),
 dict(key='stress', after=10, page='tr', hash='surgery', scene='transmon 3D 第 11 章：魔術態工廠——自由實驗（調高注入錯誤率、統計、兩輪）',
      title='動畫展示：原料越髒，丟得越多', sub='三維動畫：調高注入錯誤率看接受率',
      sentences=[
       '接著模仿孩子的改造：進自由實驗、切到工廠，把注入錯誤率一路拉到最右邊，大約百分之五，看板上的接受率掉到百分之四十六點二。',
       '按跑兩千次統計，左上角和看板都寫出這兩千批裡接受了幾批，比例不到一半，另一半的原料檢查不過、整批丟掉。',
       '再按兩輪的按鈕，看板改算兩輪：第一輪的輸出變成第二輪的輸入，最後錯誤率約三乘十的負六次方，可是一顆要耗掉兩百二十五顆注入態。',
       '注入越髒，丟掉的越多、要蒸的輪數也越多；所以工程師拚命壓低注入錯誤率，工廠才不會變成整台電腦的瓶頸。'],
      actions=[(0, 0.3, _STEP8), (0, 1.6, ('id', 'g11vf')), (0, 5.8, _p(-1.3)),
               (1, 0.4, ('id', 'g11mc')),
               (2, 0.3, ('sel', '[data-lv11="2"]'))],
      points=[('注入約百分之五', '接受率掉到四成多'), ('跑兩千次統計', '不到一半被接受'), ('改成兩輪', '耗掉兩百二十五顆')], shot=(2, 8.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q110'] 取用。"""

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)

    def get(self, k, default=None):
        return list(self) if k == LESSON else default

    def keys(self):
        return [LESSON]

    def values(self):
        return [list(self)]

    def items(self):
        return [(LESSON, list(self))]


DEMOS = _Demos(_LIST)

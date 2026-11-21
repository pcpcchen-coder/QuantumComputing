"""Q112 模組發表：換你當老師 — v2 動畫展示段（格式見 ../demos.py 的說明）。

全部用 tr = animations/transmon-3d.html，只用按下當下就生效的操作（章節按鈕、第 1 章按鈕／勾選框、滑桿 input 事件），不靠章節步驟腳本的時間軸。
- map：從 #chip 出發，點底部章節列 #chap-readout（第 5 章「色散讀取：從頻移讀出狀態」，鏡頭移到讀取共振腔，上方浮出 S21 與 IQ 兩塊看板，
  左上角字幕從步驟 1 開始）、#chap-bv（第 9 章，上方電路看板，下方 8 根振幅長條 |000⟩…|111⟩）、#chap-surface（第 10 章，9 顆白色資料位元圓球排成 3×3），
  最後 #chap-chip 回到第 1 章（第 1–4 章不顯示左上字幕）。
- write：#chip 第 1 章晶片總覽。標籤：十字電容板 C_Σ、SQUID：兩個約瑟夫森結、讀取共振腔 ~7 GHz、饋線、XY 驅動線、Z 磁通線、接地面（Al）、基板。
  #c1pulse「送出 π 脈衝」：6 個青色（COL.teal）光點沿 XY 線跑向十字（約 0.7 秒），之後十字板發光（excite = 1），
  每幀乘 exp(−dt/6)：時間常數 6 秒的示意衰減（真實 T₁ 約 100 μs）。#c1tags「顯示標籤」勾選框：click 會取消勾選並觸發 change → 標籤全部隱藏。
- whatif：#capacitor（第 1 章「大十字電容的作用」分頁，C_Σ = 77.5 fF）。滑桿 #c1C（5–200，step 0.5）oninput → fillCap()；
  面板（已用 node 讀頁面確認）：20 fF → E_C 969 MHz、E_J/E_C 15.5、f₀₁ 9.69 GHz、α −1.33 GHz、判斷「電荷雜訊主導（接近 Cooper pair box）」（銅色）；
  200 fF → 96.8 MHz、154.9、3.31 GHz、−104 MHz、「非諧性偏小，閘需放慢」（金色）。十字板粗細 = clamp(C/77.5, 0.3, 1.8)；青色電場線與「電場集中在間隙」標籤。
  滑桿用 ('js', …) 在頁面內依實際經過時間約 2 秒拖到目標值（每步觸發 input；機器忙時步數變少，但終點一定是目標值）。
"""

LESSON = 'Q112'


def _drag(target, secs=2.0):
    """依實際經過時間把 #c1C 拖到 target（機器忙、計時器變慢時也一定停在 target）"""
    ms = int(secs * 1000)
    return ('js', "(function(){var s=document.getElementById('c1C');if(!s)return;window.__flash&&window.__flash(s.closest('label')||s);"
                  f"var a=+s.value,b={target},T={ms},t0=performance.now();var h=setInterval(function(){{"
                  "var u=Math.min(1,(performance.now()-t0)/T);s.value=a+(b-a)*u;s.dispatchEvent(new Event('input'));"
                  "if(u>=1)clearInterval(h);},60);})()")


_LIST = [
 dict(key='map', after=3, page='tr', hash='chip', scene='transmon 3D 章節列：第 5 章讀取、第 9 章 BV 密碼、第 10 章表面碼，再回第 1 章',
      title='動畫展示：先找到你的那一章', sub='三維動畫：十二章章節列，一課對一章',
      sentences=[
       '打開超導晶片動畫，畫面最下方是十二章的章節列；挑好要教的那一課，先在這裡找到它對應的章。',
       '點第五章讀取，鏡頭移到蜿蜒的讀取共振腔，上方浮出兩塊看板，左上角的字幕開始逐步說明。',
       '點第九章猜密碼，上方是電路看板，下方八根柱子代表三顆位元八種結果的振幅。',
       '再點第十章表面碼，九顆白色圓球排成三乘三的方格；最後點回第一章，回到我們要示範的晶片。'],
      actions=[(1, 0.4, ('id', 'chap-readout')),
               (2, 0.4, ('id', 'chap-bv')),
               (3, 0.4, ('id', 'chap-surface')), (3, 6.0, ('id', 'chap-chip'))],
      points=[('第五章', '讀取共振腔與看板'), ('第九章', '電路與八根振幅'), ('第十章', '三乘三的表面碼')], shot=(2, 4.0)),
 dict(key='write', after=5, page='tr', hash='chip', scene='transmon 3D 第 1 章：晶片總覽——送出 π 脈衝、關掉標籤',
      title='動畫展示：寫入靠的是驅動線', sub='三維動畫：晶片總覽與派脈衝',
      sentences=[
       '這是第一章的晶片總覽，標籤標出十字電容板、兩個約瑟夫森接面、驅動線、磁通線和讀取共振腔。',
       '按送出派脈衝，一串青色光點沿著驅動線跑向十字板，十字板亮起金光，代表位元被激發到一。',
       '接下來什麼都不按，金光在幾秒內慢慢變暗，代表位元自己掉回零態；真實晶片大約一百微秒，動畫把它放慢了。',
       '當老師時可以把標籤關掉，考考爸爸：哪一條線負責寫入？哪一條線負責調頻率？'],
      actions=[(1, 0.6, ('id', 'c1pulse')),
               (3, 1.5, ('id', 'c1tags'))],
      points=[('青色光點', '沿驅動線送進來'), ('十字板發光', '位元到了一'), ('關掉標籤', '考考爸爸')], shot=(1, 4.0)),
 dict(key='whatif', after=7, page='tr', hash='capacitor', scene='transmon 3D 第 1 章：大十字電容的作用——拖動 C_Σ 滑桿到 20 與 200 fF',
      title='動畫展示：如果電容改掉會怎樣？', sub='三維動畫：大十字電容的作用',
      sentences=[
       '換到第一章的第二個分頁，大十字電容的作用，青色的電場線集中在十字板和接地面之間的間隙。',
       '把電容從七十七點五飛法拉拉小到二十，十字板變細，位元頻率升到大約九十七億赫茲，判斷變成電荷雜訊主導。',
       '再拉大到兩百，十字板變粗，非諧性縮小到大約一億零四百萬赫茲，判斷變成非諧性偏小、閘需放慢。',
       '這就是一題好的為什麼題：電容太小怕雜訊，太大又怕脈衝漏到更高的能階，所以要選在中間。'],
      actions=[(1, 2.0, _drag(20)),
               (2, 0.5, _drag(200))],
      points=[('二十飛法拉', '電荷雜訊主導'), ('兩百飛法拉', '非諧性偏小'), ('出題', '為什麼要選中間')], shot=(2, 5.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q112'] 取用。"""

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

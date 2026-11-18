"""Q109 第 11 課：表面碼——穩定子與匹配解碼 — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html#surface（第 10 章）。步驟按鈕在 #g10steps（第 8 個是「自由實驗」，dur 0、不會自動接續，
  setup 會 clear10() 清掉所有錯誤；d = 3 與步驟 1 相同，不重建方格）。自由實驗控制項：[data-d10]「3（17 顆）」…、#g10p 錯誤率、
  #g10dec「解碼並修正」、#g10rnd「隨機錯誤」、#g10clr「清除錯誤」、#g10mc「跑 300 次統計」；面板 #g10lit「亮起的穩定子」、#g10res「最近一次解碼」。
  注入錯誤只能點 3D 畫面上的資料位元（stage 的 pointerdown／pointerup + Raycaster，只在自由實驗、沒有解碼動畫時有效），
  所以用 js 在 #stage 上送一對同座標的 PointerEvent。座標是 1600×900 視窗、第 10 章鏡頭（CH 固定 target／pos，無自動旋轉）下
  資料位元的畫面位置，由製作代理單張截圖量得：D1 (583, 543)、D4 (578, 613)、D5 (720, 615)、D7 (572, 700)。
  解碼動畫（g10 dec）：配對白線 0–2.0 秒、1.3 秒套用修正（「Dn 修正」金色標籤約 1.2 秒）、2.0 秒寫入「最近一次解碼」；
  時間依畫面幀推進（dt 上限 0.05 s），錄影幀率低時比牆鐘慢，所以旁白在按鈕後約 1.5 秒才說白線。
  #g10dec 用 element.click() 不會捲動面板，先把按鈕捲到面板中間，讓按鈕與面板讀數同時入鏡。
op = animations/operation.html#qec（場景 11，js/operation/11_qec.js）：預設 d = 5、p = 5%、「自動循環」開著（每 0.9 秒一個階段）；
  右下插圖「邏輯錯誤率 vs 實體錯誤率（即時蒙地卡羅）」載入後逐幀算 3 × 15 點、每點 1000 次（d = 3 藍 #4f8cff、d = 5 橙 #e0a54a、
  d = 7 紅 #ff5a5f；灰白虛線「未編碼 = p」；白色直線在目前的 p）。滑桿標籤「實體錯誤率 p（每個資料量子位元）」，數值是小數（0.15 = 15%）。
"""

LESSON = 'Q109'

_STEP8 = ('sel', '#g10steps button:nth-child(8)')
_SHOW_DEC = ('js', "document.getElementById('g10dec').scrollIntoView({block:'center'});")


def _tap(x, y):
    """在 3D 畫面 (x, y) 點一下（第 10 章自由實驗：點資料位元依序注入 X → Z → Y → 清除）"""
    return ('js', "(()=>{const s=document.getElementById('stage');"
                  f"const o={{clientX:{x},clientY:{y},bubbles:true,pointerId:1}};"
                  "s.dispatchEvent(new PointerEvent('pointerdown',o));s.dispatchEvent(new PointerEvent('pointerup',o));})()")


_D1, _D4, _D5 = _tap(583, 543), _tap(578, 613), _tap(720, 615)

_LIST = [
 dict(key='match', after=7, page='tr', hash='surface', scene='transmon 3D 第 10 章：表面碼——自由實驗（D5 的 X 錯誤）',
      title='動畫展示：兩個亮點配成一對', sub='三維動畫：在中間放一個位元翻轉，看解碼器配對',
      sentences=[
       '打開超導晶片動畫第十章表面碼，按第八步自由實驗，這裡可以自己點資料位元，把錯誤放進去。',
       '點一下中間的第五號，它變成紅色的位元翻轉，左上和右下兩個青色格子同時亮起來，琥珀色格子沒有反應。',
       '按下解碼並修正，白線把兩個亮點連成一對，最短的路徑正好經過第五號，那顆圓球標上修正，格子全部熄滅。',
       '面板最下面的最近一次解碼寫著成功，錯誤已修正；從頭到尾，解碼器沒有量過任何一顆資料位元。'],
      actions=[(0, 0.5, _STEP8), (0, 2.0, _SHOW_DEC),
               (1, 0.8, _D5),
               (2, 0.2, ('id', 'g10dec'))],
      points=[('點一下第五號', '兩個青色格子亮'), ('解碼並修正', '白線配成一對'), ('最近一次解碼', '成功，錯誤已修正')], shot=(3, 2.0)),
 dict(key='fool', after=8, page='tr', hash='surface', scene='transmon 3D 第 10 章：表面碼——自由實驗（D1、D4 兩個 X 錯誤）',
      title='動畫展示：兩個錯誤騙過解碼器', sub='三維動畫：第一號加第四號，修完卻是邏輯錯誤',
      sentences=[
       '回到自由實驗，這次在第一號和第四號各點一下，兩顆都變成紅色的位元翻轉。',
       '它們共用的左上青色格子翻了兩次，互相抵消沒有亮，只剩左邊界的半圓亮起來，右邊面板寫著青色一個。',
       '按下解碼並修正，解碼器只看到一個亮點，就在第七號補上翻轉，左邊從上到下三顆全變成紅色。',
       '所有格子都熄滅了，晶片上方卻跳出紅字，寫著邏輯錯誤，邏輯位元被翻轉，解碼器完全沒有發現。'],
      actions=[(0, 0.3, _STEP8), (0, 1.2, _SHOW_DEC),
               (0, 3.2, _D1), (0, 4.4, _D4),
               (2, 0.2, ('id', 'g10dec'))],
      points=[('第一號加第四號', '只亮左邊界'), ('在第七號補翻轉', '整排都翻了'), ('格子全熄滅', '卻是邏輯錯誤')], shot=(3, 2.0)),
 dict(key='threshold', after=10, page='op', hash='qec', scene='3D 場景 11：錯誤更正（d = 5，自動循環與即時蒙地卡羅）',
      title='動畫展示：低於門檻才有用', sub='三維動畫：碼距三、五、七的邏輯錯誤率',
      sentences=[
       '換到操作動畫的錯誤更正場景，這片表面碼的碼距是五，上方寫著二十五顆資料加二十四顆量測，一共四十九顆實體位元。',
       '動畫一輪一輪自動跑：先隨機出現紅球，再量穩定子，立起橘色柱子的方塊就是症狀，接著綠線把症狀配對或連到上下邊界，然後修正。',
       '右下角的小圖是即時模擬，藍、橙、紅三條線是碼距三、五、七；在錯誤率低的左邊，碼距七的紅線壓在最下面。',
       '把錯誤率滑桿拉到百分之十五，白色直線移到右邊，這裡三條線擠在一起，都在不編碼的虛線上方，越過門檻，加大碼距就沒有好處了。'],
      actions=[(3, 0.6, ('slider', '實體錯誤率', 0.15))],
      points=[('碼距五', '四十九顆實體位元'), ('錯誤率低', '碼距越大越好'), ('越過門檻', '加大碼距沒好處')], shot=(3, 4.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q109'] 取用。"""

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

"""Q060 動態線路 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都是本學程動畫段第一次使用的場景（Q046 用過 pe#electronics 的回饋、Q050 用過 tr 第 5 章步驟 8 的主動重設，本課不重複）。
皆已讀原始碼確認，並以 1600×900 Chromium（swiftshader）截圖確認畫面位置。

- bc#teleport：animations/basic-circuits.html（SCENES 的 id "teleport"，第 396–413 行）。預設 ψ = √¾|0⟩ + ½|1⟩。
  控制項 #bNext（第 197 行）、#m1000「量測 1,000 次」（第 222 行），用 ('sel', '#…') 以 el.click() 觸發（不會自動捲動），
  所以用 ('js', scrollTo) 決定視野：捲到 520 時電路圖（q0、q1、q2 三條線、右側方框「修正（2 個古典位元）」）和
  「下一步」按鈕都在畫面中；捲到 1000 時最上面是步驟說明，左下是兩顆 Bloch 球（左「單看 q0」、右「單看 q2」），右邊是量測卡。
  第 3 步後 q2 向量縮在球心（說明「q2 的向量還在球心」）；第 4 步說明「真實做法是 Alice 量測 q0、q1，把 2 個位元傳給 Bob：
  q1 = 1 就對 q2 做 X，q0 = 1 就做 Z。這裡用受控閘代替「量測後再修正」（延遲量測原理）…修正後 q2 的向量回到 ψ」。
  量測 1,000 次截圖：754（75.4%）／246（24.6%），註「理論：0 75%、1 25%」，並出現「→ 對照 ψ：q2 的量測機率和 ψ 相同」。
  go() 的過場是 650 ms 的 requestAnimationFrame（實際時間），每次點擊間隔 ≥ 1 秒。
- at#zoned：animations/js/atoms/11_zoned.js。ui.button「中途量測」（第 116 行），序列 seqMeasure（第 99–108 行）：
  抓起第 4 列前 npairs = 6 顆（0.6 秒）→ 搬到讀取區（1.8 秒）→ 螢光成像（3.0 秒，讀取區青色光片＋往上飛的光點，第 141–145 行）
  → 補充新原子（1.2 秒，縮小後回到原位，第 146–149 行），全部是場景秒數。錄影速度不固定，所以第一個動作暫停 App 迴圈
  （App.paused = true，core.js 第 272 行讓迴圈以 d = 0 呼叫 update），改由 setInterval 依實際時間 × __rate 餵 update，
  停在 __tgt（Q046 的作法，但不重建場景）；之後用 _go 改目標。速度 0.6：抓起＋搬運約 4 秒、成像約 5 秒、補充約 2 秒（實際時間）；成像從第 2 句開始前約 1 秒啟動，讓青光在第 2 句開頭變亮。
  截圖位置：上面藍框標「儲存區」（區域標籤只有這個在畫面內）、四色原子與「邏輯位元 A–D」標籤；中間粉紅色帶成對圓環（糾纏區）；
  最下面青色帶（讀取區）；被抓的是最靠近鏡頭那一排（4 綠 2 紫）、上方有粉紅色光錐；右下小圖「一層的時間組成（代表值）」：
  抓取 + 搬運 250 μs、芮德堡 CZ（並行）0.3 μs、搬回 250 μs、中途讀取（選用）1 ms，頁尾「閘本身只佔極小比例；整體速度由搬運與讀取決定」
  （第 121–123 行）。面板讀數在 1600×900 下位於畫面外（y ≈ 912），旁白不提。
- op#qec：animations/js/operation/11_qec.js。ui.radio「d = 3／d = 5／d = 7」（第 133 行，點了會 setup() 清空、phase = 0）、
  ui.toggle「自動循環」預設開（第 136 行）、ui.button「下一步」（第 137 行，會關 auto 並 stepCycle()）。
  stepCycle（第 121–131 行）第一下用 Math.random 產生錯誤，所以第一下用 ('js', …) 暫時把 Math.random 換成固定種子
  （mulberry32，種子 258；只在同步的 click 期間生效，之後還原），確定只有正中間 (2,2) 一顆資料位元出錯。
  截圖：第一下中間一顆紅球；第二下紅球斜對角兩塊方塊變色並豎起橘色柱子（第 116 行）；第三下面板「③ 解碼：配對 2 個症狀」、
  綠線連起兩個症狀；第四下紅球變回白色、柱子消失、綠線留著，面板第一行「④ 修正完成 → 邏輯資訊保住了 ✓」
  （讀數框在左邊面板最下面，第一行在 1600×900 可見）。頂端金色標籤「邏輯量子位元：d = 5，25 資料 + 24 量測 = 49 實體量子位元」。
"""
LESSON = 'Q060'


class _Demos(list):
    """清單（demos.py 的載入方式），同時也能用 DEMOS['Q060'] 取用。"""

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


def _scroll(y):
    return ('js', "window.scrollTo({top: %d, behavior: 'instant'})" % y)


# 分區架構：暫停原本的迴圈，改用實際時間 × __rate 餵場景，停在 __tgt（場景秒數）
_DRV = ("(()=>{App.paused=true;clearInterval(window.__wi);window.__acc=0;window.__tgt=0;window.__rate=0.6;"
        "window.__wt=performance.now();window.__wi=setInterval(()=>{const n=performance.now();"
        "let d=(n-window.__wt)/1000*window.__rate;window.__wt=n;d=Math.max(0,Math.min(d,window.__tgt-window.__acc));"
        "if(d<=0)return;window.__acc+=d;App.time+=d;App.active.update(App.time,d);},30);})()")
_MEASURE = ('js', "(()=>{const b=window.__btn('中途量測');window.__flash(b);b.click();window.__tgt=2.4;})()")


def _go(tgt):
    return ('js', 'window.__tgt=%s;' % tgt)


# 錯誤更正：第一下「下一步」用固定種子產生錯誤（只有正中間一顆）
_SEEDED_STEP = ('js', "(()=>{const R=Math.random;let a=258;Math.random=function(){a|=0;a=a+0x6D2B79F5|0;"
                      "let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};"
                      "try{const b=window.__btn('下一步');window.__flash(b);b.click();}finally{Math.random=R;}})()")

DEMOS = _Demos([
 dict(key='teleport', after=5, page='bc', hash='teleport', scene='基礎量子電路 範例 5：量子隱形傳態',
      title='動畫展示：隱形傳態的修正', sub='三維動畫：量子電路入門——用受控閘代替量完再補閘',
      sentences=[
       '換到基礎量子電路網頁的隱形傳態範例，三條線由上往下，是要送出的狀態、愛麗絲的糾纏位元，和鮑伯手上的位元。',
       '連按三次下一步，做完準備、糾纏和愛麗絲那一邊的閘；往下看，右邊那顆鮑伯的布洛赫球，箭頭縮在球心，單看完全隨機。',
       '再按一次下一步，第四步是鮑伯依兩個位元修正；說明寫著，真實做法是先量愛麗絲的兩顆位元，結果是一，就對鮑伯補翻轉閘或相位翻轉閘。',
       '動畫用受控閘代替量完再補閘，鮑伯的箭頭回到要送的狀態；按量測一千次，零大約七成五、一大約兩成五，和原本一樣。'],
      actions=[(0, 0.2, _scroll(520)),
               (1, 0.5, ('sel', '#bNext')), (1, 1.6, ('sel', '#bNext')), (1, 2.7, ('sel', '#bNext')), (1, 5.4, _scroll(1000)),
               (2, 0.5, ('sel', '#bNext')),
               (3, 6.0, ('sel', '#m1000'))],
      points=[('鮑伯的箭頭', '修正前縮在球心'), ('真實做法', '量兩顆、依結果補閘'), ('量一千次', '約七成五比兩成五')], shot=(3, 11.0)),
 dict(key='zoned', after=8, page='at', hash='zoned', scene='原子 3D 場景 11：分區架構與並行閘',
      title='動畫展示：中途量測要搬家', sub='三維動畫：中性原子的分區架構——中途量測',
      sentences=[
       '打開原子平台動畫的分區架構場景，上面藍框是儲存區，四種顏色代表四個邏輯位元；中間粉紅色是糾纏區，下面青色是讀取區。',
       '按下中途量測，粉紅色的光鑷抓起最靠近我們那一排的六顆原子，整排搬到最下面的讀取區，遠離其他原子。',
       '讀取區亮起青光，往上飛的小光點代表螢光，靠拍照判讀零或一；量完的原子已經被加熱，所以換上新原子補回原位。',
       '右下角的小圖寫著，並行的糾纏閘只要零點三微秒，中途讀取卻要一毫秒，慢了三千多倍，整體速度常常卡在讀取。'],
      actions=[(0, 0.2, ('js', _DRV)),
               (1, 0.3, _MEASURE), (1, 9.8, _go(5.4)),
               (2, 6.5, _go('1e9'))],
      points=[('搬到讀取區', '遠離其他原子'), ('螢光成像', '量完換新原子'), ('讀取一毫秒', '比閘慢三千多倍')], shot=(1, 9.0)),
 dict(key='syndrome', after=10, page='op', hash='qec', scene='3D 場景 11：錯誤更正（表面碼）',
      title='動畫展示：量症狀、再修正', sub='三維動畫：量子錯誤更正——每一輪的症狀量測',
      sentences=[
       '換到操作動畫的錯誤更正場景，先關掉自動循環，再選碼距五：白球是二十五顆資料位元，青色和紫色方塊是量奇偶的量測位元。',
       '按下一步，正中間有一顆資料位元出錯，變成紅球；再按一次，紅球斜對角的兩塊方塊變色，豎起橘色柱子，這就是症狀。',
       '量測位元只量周圍的奇偶，不碰資料本身；第三下，解碼器把這兩個症狀配成一對，用綠線連起來，推測錯在中間。',
       '第四下照著推測修正，紅球變回白色，左邊面板最下面寫著修正完成、邏輯資訊保住了；真實機器每一輪都要這樣量、這樣修。'],
      actions=[(0, 3.0, ('toggle', '自動循環', False)), (0, 5.0, ('click', 'd = 5')),
               (1, 0.4, _SEEDED_STEP), (1, 5.6, ('click', '下一步')),
               (2, 4.6, ('click', '下一步')),
               (3, 0.4, ('click', '下一步'))],
      points=[('一顆出錯', '中間變成紅球'), ('量奇偶', '兩根橘色柱子'), ('解碼修正', '紅球變回白色')], shot=(2, 9.0)),
])

"""Q019 Cooper pair 與能隙 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都用課綱指定的場景 index.html#cooper：js/scenes/02_cooper.js（App.register id 'cooper'，第 3 行；index.html 第 41 行載入；#controls 第 31 行）。
按鈕由 core.js ui.button 放進 #controls（core.js 第 339–343 行），ui.radio 同一列（第 345–352 行），所以 ('click', 文字開頭) 可用；
滑桿由 ui.slider 放進 #controls 的 label.slider（第 359–369 行），record_demo.js 用 textContent.includes 找標籤。

控制項（02_cooper.js）：
- 滑桿「溫度 T (K)」0.05–3、step 0.05、預設 0.3（第 43–44 行）。注意 record_demo.js 的 'sweep' 會把值 Math.round 成整數，
  這個滑桿是小數，所以第三段改用一連串 ('slider', '溫度', 值)，不用 sweep。
- 互斥按鈕「超導態 0.3 K」「正常態 2.5 K」（第 45 行），按下即把滑桿設成 0.3 或 2.5。
- 讀數（第 46、106 行）：「T / Tc = …　配對比例 ≈ …%」＋ 超導時「能隙 Δ 打開：小擾動無法散射 Cooper pair」、
  正常時「無能隙：電子與聲子碰撞 → 焦耳熱」。Tc = 1.2（第 43 行）。
畫面（02_cooper.js）：
- 晶格 11×3×4 顆金色（0xe0a54a）離子（第 12–20 行）；標籤「正離子晶格（Al）」（第 40 行）。
- 10 對電子（第 27 行）：一顆 0x6fb4ff 藍、一顆 0x9d7bff 紫（第 29 行），青色連線 0x8ef0ff（第 34 行）；標籤「Cooper pair（↑↓ 電子對）」（第 39 行）。
- 超導時配對比例 frac = 1 − (T/Tc)⁴、配對數 round(frac × 10)（第 59–60 行）；配對的電子繞中心轉、整體以 +x（往右）速度 1.4 前進、連線顯示（第 66–74 行）；
  未配對的電子連線隱藏、以每秒 2 + 3T 次的機率隨機改變方向（第 75–88 行）。
- 晶格下方大字（第 41、61–62 行）：超導「超導態：Cooper pair 同步流動，無散射」青色 #8ef0ff；正常「正常態：電子被晶格振動散射 → 有電阻」粉紅 #ffb0b2。
- 右下小圖「電阻 R 對溫度 T（鋁，Tc ≈ 1.2 K）」：T < Tc 時 R = 0，否則 R = 1 + 0.08(T − Tc)，青色點 #38c6d9 標目前溫度（第 48–53 行；#inset-wrap 在右下，css/style.css 第 56 行）。
- 晶格扭曲（第 98–104 行）位移最大約 0.05 格，幅度很小，旁白不說「看得到離子靠過來」。
配對比例（四捨五入）：T = 1.2 → 0%（不小於 Tc 為正常態）；1.1 → 29%；1.0 → 52%；0.8 → 80%；0.6 → 94%；0.3 → 100%。
- 三段開頭都先把 #panel 捲到底（面板 max-height 100vh − 96px、可捲動，css/style.css 第 32 行），讓按鈕與讀數入鏡（待試錄確認）。
"""

LESSON = 'Q019'

_PANEL = "document.getElementById('panel').scrollTop=1e5;"
_SCENE = 'JJ 與微波讀取 3D 場景 2：超導體——Cooper pair 與零電阻'

_LIST = [
 dict(key='pairs', after=5, page='jj', hash='cooper', scene=_SCENE,
      title='動畫展示：一對一對往前走', sub='三維動畫：超導體裡的庫柏對與晶格',
      sentences=[
       '打開約瑟夫森接面與微波讀取動畫的庫柏對場景，金色的小球是鋁的正離子，排成一個整齊的晶格。',
       '溫度一開始就設在零點三度，比臨界溫度低；藍色和紫色的小球是電子，每兩顆用一條青色的線連成一對。',
       '每一對一邊繞著轉，一邊和其他電子對一起往右邊前進，晶格下面的大字寫著：同步流動，沒有散射。',
       '左邊面板上的配對比例是百分之百，代表每一顆電子都找到了伴。'],
      actions=[(0, 0.1, ('js', _PANEL))],
      points=[('金色小球', '鋁的正離子晶格'), ('青色連線', '兩顆電子一對'), ('一起往右走', '沒有被撞偏')],
      pmap=[0, 1, 2, 2], shot=(2, 4.0)),
 dict(key='nogap', after=6, page='jj', hash='cooper', scene=_SCENE,
      title='動畫展示：沒有能隙會怎樣', sub='三維動畫：超導態和正常態對照',
      sentences=[
       '現在按正常態二點五度，溫度升到臨界溫度以上，電子之間的青色連線一下子全部消失。',
       '電子變成一顆一顆亂跑，常常突然轉向，那就是被晶格振動撞到；晶格下面的字也已經換成粉紅色的正常態，有電阻。',
       '左邊面板寫著：沒有能隙，電子和聲子，也就是晶格的振動碰撞，產生熱。',
       '再按回超導態，電子馬上重新成對，面板換成：能隙打開，小擾動散射不了電子對。'],
      actions=[(0, 0.1, ('js', _PANEL)), (0, 1.3, ('click', '正常態')), (3, 0.8, ('click', '超導態'))],
      points=[('正常態', '連線消失、亂跑'), ('沒有能隙', '碰撞變成熱'), ('回到超導態', '能隙保護電子對')],
      pmap=[0, 0, 1, 2], shot=(1, 3.0)),
 dict(key='cooling', after=8, page='jj', hash='cooper', scene=_SCENE,
      title='動畫展示：慢慢降溫，慢慢成對', sub='三維動畫：溫度滑桿與電阻曲線',
      sentences=[
       '最後拖動溫度滑桿，從二點五度慢慢往下降，眼睛盯著右下角電阻對溫度的小圖。',
       '高於一點二度時，青色的點停在上面那段線上，電阻不是零；一跨過臨界溫度，點就掉到零。',
       '同時面板的配對比例也開始往上爬，到一點零度大約一半，越冷越多。',
       '降到零點三度，配對比例回到百分之百；動畫裡的比例曲線是示意，量子晶片則在比這裡再冷三十倍的地方工作。'],
      actions=[(0, 0.1, ('js', _PANEL)), (0, 0.2, ('slider', '溫度', 2.5)), (0, 3.4, ('slider', '溫度', 2.3)),
               (0, 5.2, ('slider', '溫度', 2.1)),
               (1, 0.6, ('slider', '溫度', 1.9)), (1, 2.2, ('slider', '溫度', 1.6)), (1, 3.8, ('slider', '溫度', 1.3)),
               (1, 5.6, ('slider', '溫度', 1.1)),
               (2, 2.6, ('slider', '溫度', 1.0)), (2, 4.6, ('slider', '溫度', 0.8)), (2, 5.6, ('slider', '溫度', 0.6)),
               (3, 0.5, ('slider', '溫度', 0.45)), (3, 1.2, ('slider', '溫度', 0.3))],
      points=[('高於臨界溫度', '電阻不是零'), ('跨過一點二度', '電阻掉到零'), ('越冷', '配對比例越高')],
      pmap=[0, 1, 2, 2], shot=(2, 4.5)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q019'] 取用。"""

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

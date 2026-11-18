"""Q053 DRAG 與虛擬 Z — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（已讀原始碼確認，並以 1600×900 Chromium（swiftshader）截圖確認畫面位置與讀數）：
- op#pulse：animations/js/operation/03_pulse.js。
  ui.radio「方波」「高斯」「高斯 + DRAG」（第 70 行；core.js 第 345–352 行，radio 是 #controls 裡的 button，
  ('click', '高斯') 以開頭比對會先找到「高斯」那一顆，不會點到「高斯 + DRAG」）；預設高斯、180°、40 ns（第 39 行）。
  右下插圖（第 81–96 行）：上半 I（金 #e0a54a）與 Q×3（青 #38c6d9）包絡，下半頻譜（相對 f₀₁，−0.4～+0.2 GHz，下限 −60 dB），
  紅色虛線 #ff5a5f 在 f₁₂ = f₀₁ − 220 MHz，旁邊文字「f₁₂ 處 … dB」。截圖讀數：方波 −34、高斯 −59、高斯 + DRAG −60（真值約 −85，被 max(−60) 截在圖底）。
  方波時包絡是平頂（env = 1，第 42 行），頻譜一整排旁瓣；DRAG 時 Q = β·dI/dt，β = 1/(2π·(−0.22)) < 0，青色曲線先在零線下、後在零線上。
  ui.slider「脈衝面積 → 旋轉角」（第 71 行）；ui.button「▶ 送出脈衝」「虛擬 Z（90°）」「重設 |0⟩」（第 76–78 行）。
  「虛擬 Z（90°）」：frame += 90°、狀態向量直接繞 z 轉 90°，不呼叫 startPulse（沒有發光小球、沒有粉紅軸更新）；讀數「虛擬 Z 累積的座標相位 = …」（第 127 行）。
  面板捲到最下面（#panel scrollTop）後，按鈕與讀數（「目前 P(1) = …」）都在畫面左下。
  實測（截圖＋DOM 讀數）：90° 脈衝 → 箭頭在左（−y）；虛擬 Z → 朝觀眾（+x），累積 90°；再 90° 脈衝（粉紅軸沿橘色 x 軸穿過箭頭）→ 不動，P(1)=0.500；
  再虛擬 Z → 右（+y），累積 180°；再 90° 脈衝 → 回北極，P(1)=0.000。
- lc#s6drag：animations/lc-vs-jj.html 第 6 步（section id="s6drag"，第 283–325 行；繪圖程式第 553–646 行）。2D 頁面，控制項不在 #controls，
  用 ('js', …) 設定 <input type=range> #dT（π 脈衝長度 2–30 ns，預設 6）、#dB（DRAG 係數 β 0–1.6，預設 1）並送出 input 事件（第 645 行監聽）。
  1600×900、淺色主題下整個第 6 步在畫面內：左側說明文字；右側四張小圖（左上包絡、右上頻譜含「ω₁₂（Δ = α）」虛線、左下「脈衝期間 |2⟩ 的佔有率」、
  右下「閘結束後的洩漏 vs 閘長度」含目前閘長的圓點），橘褐色（--jj）＝純高斯、紫色（--q）＝DRAG；最下方三格讀數 #rDa、#rDb、#rDc。
  實測讀數：預設「4.7 × 10⁻²」「4.0 × 10⁻⁴」「118.0 倍」；左下峰值 17.8%／8.9%（Node 執行頁面的 simDrag 重算）；
  β→0：紫色與橘褐色重合、「1.0 倍」，頻譜深谷位置 Δ = α/β 往左移，β < 0.53 時移出圖外；β=1、20 ns：「2.7 × 10⁻⁵」「4.9 × 10⁻¹⁰」。

時間控制：vz 段第一個動作用 ('js', …) 重建場景、暫停原本迴圈，改由 setInterval 依實際經過時間餵 update（同 Q049／Q052），
一個脈衝實際約 1.6 秒；連送之間至少隔 2.2 秒。shape 段只看插圖（由 build() 直接重畫），lc 段是 2D 頁面，都不需要對時。
Q046（相位差 90° 的兩個脈衝）、Q049（閘長度與連按兩次虛擬 Z）、Q050（90°／180° 與失諧）、Q052（面積累加、旋轉軸）已用過 op#pulse；
本課改看：脈衝形狀切換與 f₁₂ 處的分貝數、虛擬 Z 之後同一個脈衝的效果改變。lc#s6drag 本學程第一次使用。
"""
LESSON = 'Q053'

_DRV = ("(()=>{App.cur=-1;App.showByHash();App.paused=true;clearInterval(window.__wi);"
        "window.__wt=performance.now();window.__wi=setInterval(()=>{const n=performance.now();"
        "const d=Math.min(0.2,(n-window.__wt)/1000);window.__wt=n;App.time+=d;App.active.update(App.time,d);},30);"
        "document.getElementById('panel').scrollTop=1e5;})()")
_SEND = ('click', '▶ 送出脈衝')
_VZ = ('click', '虛擬 Z')
_SCENE = '3D 場景 3：微波脈衝'

# lc-vs-jj.html：設定滑桿並觸發重畫；__lsw 依實際時間逐步拖動
_LC_INIT = ("window.__ls=(id,v)=>{const e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input'));"
            "if(window.__flash)window.__flash(e.closest('.control'));};"
            "window.__lsw=(id,a,b,ms)=>{clearInterval(window.__swi);const n=Math.max(2,Math.round(ms/120));let k=0;"
            "window.__swi=setInterval(()=>{k++;window.__ls(id,a+(b-a)*k/n);if(k>=n)clearInterval(window.__swi);},120);};"
            "document.getElementById('s6drag').scrollIntoView({block:'start'});")


class _Demos(list):
    """清單（demos.py 的載入方式），同時也能用 DEMOS['Q053'] 取用。"""

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


DEMOS = _Demos([
 dict(key='shape', after=4, page='op', hash='pulse', scene=_SCENE,
      title='動畫展示：三種脈衝的頻譜', sub='三維動畫：微波脈衝——方波、高斯、加上修正',
      sentences=[
       '打開操作量子電腦動畫的微波脈衝場景，先看右下角的小圖：上半部是脈衝的包絡，下半部是頻譜，紅色虛線標的就是從一跳到二的頻率。',
       '在左邊面板點方波，金色的包絡變成平平的一塊，頻譜冒出一整排高高低低的旁瓣，紅線旁的讀數變成負三十四分貝。',
       '換回高斯，包絡變成圓滑的小山丘，紅線附近的旁瓣矮了下去，讀數變成負五十九分貝。',
       '最後點高斯加修正，包絡下面多出一條先往下、再往上的青色曲線，這就是正交那一路的修正；紅線旁的讀數掉到圖的最底，負六十分貝。'],
      actions=[(1, 1.2, ('click', '方波')), (2, 0.6, ('click', '高斯')), (3, 0.9, ('click', '高斯 + DRAG'))],
      points=[('方波', '旁瓣高，負三十四分貝'), ('高斯', '圓滑，負五十九分貝'), ('加上修正', '紅線處壓到圖底')], shot=(3, 10.0)),
 dict(key='leak', after=5, page='lc', hash='s6drag', scene='LC 與約瑟夫森接面 第 6 步：快速脈衝的洩漏',
      title='動畫展示：漏到第三能階有多少', sub='三維動畫：三能階模擬——純高斯和加上修正',
      sentences=[
       '換到線性電路與約瑟夫森接面比較動畫的第六步，右邊的小圖裡，橘褐色是純高斯脈衝，紫色是加了修正的脈衝；右上的頻譜圖中，紫色曲線在一跳到二的虛線那裡挖出一個深谷。',
       '左下是六奈秒脈衝期間第三能階的佔有率，橘褐色中途衝到將近百分之十八，紫色只到大約百分之九；最下面的讀數是結束時剩下的，大約百分之四點七對上萬分之四。',
       '把修正係數從一慢慢拉到零，紫色的深谷往左滑出圖外，兩組曲線越靠越近，最後疊在一起，降低倍數只剩一倍。',
       '再把係數拉回一，並把脈衝加到二十奈秒，右下角的圓點往右移，純高斯剩大約十萬分之三，修正後只剩大約百億分之五；慢一點的脈衝本來就漏得少，修正讓它再少好幾個數量級。'],
      actions=[(0, 0.1, ('js', _LC_INIT)),
               (2, 0.3, ('js', "window.__lsw('dB',1,0,4200)")),
               (3, 0.3, ('js', "window.__ls('dB',1)")), (3, 2.6, ('js', "window.__lsw('dT',6,20,2400)"))],
      points=[('頻譜深谷', '在一跳到二的頻率'), ('六奈秒', '百分之四點七對萬分之四'), ('係數拉到零', '兩條線疊在一起')], shot=(1, 9.0)),
 dict(key='vz', after=7, page='op', hash='pulse', scene=_SCENE,
      title='動畫展示：不花時間，卻改變後面', sub='三維動畫：微波脈衝——虛擬旋轉之後的同一個脈衝',
      sentences=[
       '回到微波脈衝場景，把左邊面板捲到最下面，面積設成九十度後送出脈衝，發光的小球跑進晶片，箭頭從北極倒到赤道的左邊。',
       '現在按一下虛擬旋轉的按鈕：沒有小球跑出去，箭頭卻立刻繞著垂直軸轉了四分之一圈，停在朝向我們的位置，面板寫著累積的座標相位九十度。',
       '再送一個一模一樣的九十度脈衝，粉紅色的旋轉軸剛好穿過箭頭，箭頭留在原地不動，量到一的機會還是一半；要是少了剛才那一下，兩個這樣的脈衝會把箭頭送到南極。',
       '再按一次虛擬旋轉，箭頭轉到赤道右邊，累積相位變成一百八十度；第三個同樣的脈衝送出去，箭頭竟然爬回北極的零：三個脈衝完全相同，結果由兩次不花時間的虛擬旋轉決定。'],
      actions=[(0, 0.2, ('js', _DRV)), (0, 4.6, ('slider', '脈衝面積', 90)), (0, 6.8, _SEND),
               (1, 2.0, _VZ),
               (2, 0.8, _SEND),
               (3, 0.5, _VZ), (3, 6.0, _SEND)],
      points=[('虛擬旋轉', '沒有脈衝，箭頭立刻轉'), ('同一個脈衝', '箭頭不動'), ('再轉一次', '箭頭回到北極')], shot=(2, 6.0)),
])

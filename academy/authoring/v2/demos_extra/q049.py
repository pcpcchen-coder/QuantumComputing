"""Q049 一次量子計算的生命週期 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（已讀原始碼確認，並以 1600×900 Chromium（swiftshader）實際截圖確認畫面位置：
說明面板與控制項在左、右下角是插圖、六站平台由左往右排成弧形）：
- operation.html#workflow（animations/js/operation/12_workflow.js）：
  六站平台（第 18–23 行）：① 寫程式 綠 0x2e9e5b、② 轉譯 青 0x1c9db0、③ 脈衝排程 紫 0x8a5cd0、④ 控制電子 橘 0xc8862a、
  ⑤ 晶片執行 shots 藍 0x3b6fd8、⑥ 判別與結果 紅 0xd9534f。第一站螢幕是貝爾態程式，最後一行 `sampler.run([qc], shots=N)`（第 36 行）；
  轉譯站映射標籤「q0→Q3」「q1→Q1」（第 41 行，stage ≥ 1 才顯示）；脈衝排程時間軸方塊在 stage 2 依序變亮（第 107 行），
  標籤「D=驅動 Z=磁通 M=讀取」（第 48 行）；控制電子機櫃綠燈在 stage 3 閃爍（第 108 行）；stage 4 晶片站上方「shot n / 1,000」計數，
  3.5 秒場景時間數完（第 97、110–112 行）；直方圖 00、11 金色 0xe0a54a，01、10 灰藍 0x4a5468（約 4% 機率出錯，第 60、110 行）。
  控制項（第 73–77 行）：ui.toggle「自動播放」（預設開）、ui.button「下一站 ▶」（按下會關自動播放、stage+1）、
  ui.slider「shots N」（log10，2–5，預設 3＝1,000）、ui.slider「線路深度（層）」1–1000 預設 20、ui.toggle「主動重置（量測 + 條件 π 脈衝）」預設關。
  右下插圖（第 81–93 行）實測：預設「重置：250 μs（98.8%）／閘：2.0 μs（0.8%）／讀取：1.0 μs（0.4%）」「每 shot 253.0 μs × 1,000 shots = 253.0 ms」；
  shots 十萬「= 25.30 s」；再開主動重置「重置：2.0 μs（40.0%）」「每 shot 5.0 μs × 100,000 shots = 500.0 ms」；
  再把深度拉到 1000「閘：100 μs（97.1%）」「= 10.30 s」。
- operation.html#pulse（animations/js/operation/03_pulse.js）：預設面積 180°、閘長 40 ns（第 39 行）；ui.slider「脈衝面積 → 旋轉角」「閘長度（ns）」
  （第 71、74 行）；ui.button「▶ 送出脈衝」「虛擬 Z（90°）」「重設 |0⟩」（第 76–78 行）；一個脈衝播放 1.6 秒場景時間（第 103 行）。
  讀數（第 126–129 行）：40 ns「峰值 Rabi 頻率 ≈ 23 MHz」、20 ns「≈ 47 MHz」、送出 180° 後「目前 P(1) = 1.000」。
  面積 90° 送出後箭頭停在赤道左側（−y），按兩次虛擬 Z 後轉到赤道右側（+y），讀數「虛擬 Z 累積的座標相位 = 180°」（截圖確認）。
  面板要捲到最下面，按鈕和讀數才在畫面內。

時間控制：錄影時 swiftshader 畫格慢，core.js 的 dt 上限 0.05 秒會讓場景時間變慢，計數和脈衝就對不上旁白。
所以 stations 與 gate 兩段第一個動作用 ('js', …) 重建場景（App.cur=-1; App.showByHash()），暫停原本迴圈（App.paused=true，
迴圈仍以 dt=0 呼叫 update 並繪圖），改由 setInterval 依實際經過時間餵 update（同 Q046 的做法）。
timemachine 段只看插圖（由滑桿值直接算出），不需要對時。
Q001 已用過 workflow 場景（一句話帶過六站）；本課旁白改講各站畫面細節與插圖數字，不重複。
"""
LESSON = 'Q049'

_WF = '3D 場景 12：一次量子計算的完整流程'
_DRV = ("(()=>{App.cur=-1;App.showByHash();App.paused=true;clearInterval(window.__wi);"
        "window.__wt=performance.now();window.__wi=setInterval(()=>{const n=performance.now();"
        "const d=Math.min(0.2,(n-window.__wt)/1000);window.__wt=n;App.time+=d;App.active.update(App.time,d);},30);})()")
_PANEL_BOTTOM = "document.getElementById('panel').scrollTop=1e5;"
_NEXT = ('click', '下一站')

_LIST = [
 dict(key='stations', after=4, page='op', hash='workflow', scene=_WF,
      title='動畫展示：一站一站走', sub='三維動畫：一次量子計算的完整流程——六站的畫面',
      sentences=[
       '打開操作量子電腦動畫的完整流程場景，先把自動播放關掉，改成自己按下一站；最左邊綠色的第一站，螢幕上是一段貝爾態的程式，最後一行把工作送出，並指定重複次數。',
       '按下一站，工作封包移到青色的轉譯站，五顆實體量子位元旁邊出現兩個標籤：程式裡的零號量子位元放到實體的三號，一號放到實體的一號。',
       '再按一下，到紫色的脈衝排程站，時間軸上的小方塊一個接一個亮起來，分成驅動、磁通和讀取三種通道；再下一站是控制電子，機櫃上的綠燈開始閃爍。',
       '來到藍色的晶片站，上方的計數一路跳到一千；最後一站是紅色的判別站，直方圖上零零和一一兩根金色柱子升起來，零一和一零只冒出一點點，那是少數出錯的結果。'],
      actions=[(0, 0.2, ('js', _DRV)), (0, 0.6, ('toggle', '自動播放', False)),
               (1, 0.4, _NEXT), (2, 0.4, _NEXT), (2, 10.6, _NEXT),
               (3, 0.4, _NEXT), (3, 5.2, _NEXT)],
      points=[('轉譯', '邏輯位元放到實體位元'), ('脈衝排程', '方塊依序亮起'), ('晶片與判別', '計數到一千、直方圖')], shot=(3, 9.0)),
 dict(key='timemachine', after=5, page='op', hash='workflow', scene=_WF,
      title='動畫展示：一個 shot 的時間帳', sub='三維動畫：一次量子計算的完整流程——右下角的時間插圖',
      sentences=[
       '回到完整流程場景，這次看右下角的小圖：一次重複的時間畫成一條彩色橫條，紫色的重置佔了百分之九十八點八，金色的閘和紅色的讀取細得幾乎看不見。',
       '小圖下面寫著，每次二百五十三微秒乘上一千次，等於二百五十三毫秒；把重複次數拉到十萬次，總時間就跳到二十五點三秒。',
       '現在打開主動重置，紫色的橫條一下子縮短，一次重複只要五微秒，十萬次也只要五百毫秒，重置只剩百分之四十。',
       '最後把線路深度從二十層拉到一千層，金色的閘變成主角，佔了百分之九十七點一；瓶頸換了位置，下一步要縮短的，變成閘的時間。'],
      actions=[(1, 8.4, ('slider', 'shots N', 5)), (2, 1.0, ('toggle', '主動重置', True)),
               (3, 0.8, ('sweep', '線路深度', 20, 1000, 3.0))],
      points=[('被動重置', '佔九成八以上'), ('主動重置', '十萬次只要半秒'), ('線路變深', '瓶頸換成閘')], shot=(3, 6.0)),
 dict(key='gate', after=6, page='op', hash='pulse', scene='3D 場景 3：微波脈衝',
      title='動畫展示：四十奈秒和零秒', sub='三維動畫：微波脈衝——一個閘要多久',
      sentences=[
       '換到操作量子電腦動畫的微波脈衝場景，左邊面板上，脈衝面積是一百八十度，代表一個翻轉閘，閘的持續時間設成四十奈秒。',
       '按下送出脈衝，一顆發光的小球沿著驅動線跑進晶片，右邊布洛赫球上的箭頭，從北極的零一路轉到南極的一。',
       '把時間縮短成二十奈秒，面板最下面的峰值拉比頻率，從大約二十三兆赫跳到四十七兆赫：時間少一半，脈衝就得加倍用力，才能轉出同樣的角度。',
       '最後按重設，把面積改成九十度再送一次，箭頭停在赤道左邊；連按兩下虛擬相位轉動，箭頭立刻轉到赤道右邊，因為它只改之後脈衝的相位，不必送出脈衝，花的時間是零。'],
      actions=[(0, 0.2, ('js', _DRV)), (0, 0.6, ('js', _PANEL_BOTTOM)),
               (1, 0.5, ('click', '▶ 送出脈衝')),
               (2, 1.6, ('slider', '閘長度', 20)),
               (3, 0.8, ('click', '重設')), (3, 2.0, ('slider', '脈衝面積', 90)), (3, 3.4, ('click', '▶ 送出脈衝')),
               (3, 7.4, ('click', '虛擬 Z')), (3, 8.4, ('click', '虛擬 Z'))],
      points=[('翻轉閘', '約四十奈秒的脈衝'), ('縮短一半', '脈衝加倍用力'), ('虛擬相位轉動', '零時間')], shot=(1, 4.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q049'] 取用。"""

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

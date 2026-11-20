"""Q046 控制電子與時脈 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（已讀原始碼確認）：
- peripherals.html#electronics（animations/js/peripherals/06_electronics.js）：
  選項按鈕「外差 IQ 混頻架構」「直接射頻合成（RFSoC 等）」（ui.radio，第 76 行）；滑桿「播放速度」0.3–2（第 78 行）。
  循環步驟（cyc 秒，速度 1×，外差模式，seq() 第 82–98 行、cyc 第 112 行）：① 上傳 0–0.7、② 同步觸發 0.7–1.3、② 中頻→混頻器 1.3–1.9、
  ② 上變頻→冷凍機 1.9–2.9、③ 讀取脈衝 2.9–3.9、③ 訊號返回 3.9–4.9、③ 判別 4.9–5.4、④ 即時回饋 5.4–6.0、
  ④ 條件式 π 脈衝 6.0–7.0、⑤ 回傳 7.0–7.8、等待 7.8–8.4。直接合成模式：② 直接合成 1.3–2.4。
  直接合成時 LO 合成器與 IQ 混頻器亮度 0.12 → 0.02（第 116 行）；面板說明換成「直接合成：高速 DAC（數 GSa/s）…省去類比混頻器與校正」（第 129–132 行）。
  右下插圖「XY 驅動波形」（第 99–108 行）：I 高斯包絡 #e0a54a（橘黃）、Q DRAG 修正 #38c6d9（青）、上變頻後的 RF 藍色、橫軸「時間（~40 ns 脈衝）」。
- operation.html#pulse（animations/js/operation/03_pulse.js）：滑桿「脈衝面積 → 旋轉角」「脈衝相位 φ → 旋轉軸方向」（第 71–72 行）；
  按鈕「▶ 送出脈衝」「重設 |0⟩」（第 76、78 行）；一個脈衝播放 1.6 秒場景時間（第 103 行）。
  面積 90°、相位 0° 兩次 → 箭頭到南極；重設後 0° 一次、再 90° 一次 → 箭頭在 −y 軸上，繞 y 軸轉動不動，停在赤道（1600×900 實測截圖確認）。

時間控制：swiftshader 錄影時畫格很慢，core.js 的 dt 上限 0.05 秒會讓場景時間只剩實際時間的約三分之一，
控制電子場景的循環就無法和旁白對齊。所以第一個動作用 ('js', …) 重建場景（App.cur=-1; App.showByHash()，cyc 歸零）、
暫停原本的迴圈（App.paused=true，迴圈仍以 dt=0 呼叫 update 並繪圖），改由 setInterval 依「實際經過時間 × __rate」餵 update，
並在 __tgt（累積場景秒數）停住，讓每一步在旁白說到時出現。之後用 _go 改目標與速度。
微波脈衝場景同樣用這個方式（速度 0.5，一個脈衝約 3.2 秒）；送下一個脈衝或按重設前，上一個脈衝一定已經播完
（「重設」不會停止播放中的脈衝，兩者重疊會讓箭頭偏掉）。
1600×900 截圖確認位置：機櫃在畫面中央、銣原子鐘（金黃）在最上面、控制電腦在機櫃左邊、冷凍機在右邊；
步驟大字在機櫃上方；插圖在右下角（蓋住「量子晶片 10 mK」標籤，所以旁白不提晶片標籤）；面板說明在左下。
"""
LESSON = 'Q046'

_DRV = ("(()=>{App.cur=-1;App.showByHash();App.paused=true;clearInterval(window.__wi);"
        "window.__acc=0;window.__tgt=%s;window.__rate=%s;window.__wt=performance.now();"
        "window.__wi=setInterval(()=>{const n=performance.now();let d=(n-window.__wt)/1000*window.__rate;window.__wt=n;"
        "d=Math.max(0,Math.min(d,window.__tgt-window.__acc));if(d<=0)return;"
        "window.__acc+=d;App.time+=d;App.active.update(App.time,d);},30);%s})()")


def _drv(tgt, rate, then=''):
    return ('js', _DRV % (tgt, rate, then))


def _go(tgt, rate):
    return ('js', 'window.__tgt=%s;window.__rate=%s;' % (tgt, rate))


# 重建後點「直接射頻合成」並閃黃框
_DIRECT = "const b=window.__btn('直接射頻');window.__flash(b);b.click();"

_ELEC = '周邊系統 3D 場景 6：控制電子學'

_LIST = [
 dict(key='rack', after=5, page='pe', hash='electronics', scene=_ELEC,
      title='動畫展示：機櫃與驅動波形', sub='三維動畫：控制電子學——外差混頻和直接合成',
      sentences=[
       '打開周邊系統動畫的控制電子場景，中間直立的機櫃疊著九台儀器，最上面金黃色的是銣原子鐘，左邊是控制電腦，右邊透明的圓筒是冷凍機。',
       '右下角的小圖是驅動波形，橫軸大約四十奈秒：橘黃色的是高斯形狀的包絡，青色的是修正項，藍色的細波才是搬到四到八吉赫之後真正送出的微波。',
       '在左邊面板點直接射頻合成，本地振盪器和混頻器那兩台暗了下來，驅動脈衝不經過混頻器，直接從波形產生器送進冷凍機。',
       '左邊面板下方的說明也跟著改了：用每秒取樣數十億次的高速數位轉類比轉換器，直接輸出吉赫訊號，省去類比混頻器和校正。'],
      actions=[(0, 0.2, _drv('1e9', 1)), (2, 1.2, _drv(2.2, 1, _DIRECT)), (3, 0.3, _go('1e9', 1))],
      points=[('九台儀器', '最上面是銣原子鐘'), ('驅動波形', '包絡乘上吉赫載波'), ('直接合成', '不用混頻器')], shot=(2, 7.0)),
 dict(key='chain', after=6, page='pe', hash='electronics', scene=_ELEC,
      title='動畫展示：走一次控制鏈', sub='三維動畫：控制電子學——一次量測與回饋的循環',
      sentences=[
       '回到控制電子場景，這次放慢腳步，跟著發光的小球走完一次循環，機櫃上方的大字會寫出現在是第幾步。',
       '控制電腦先把脈衝序列上傳到同步器，同步器觸發波形產生器和讀取模組，驅動脈衝經過混頻器往上搬頻，送進冷凍機。',
       '接著讀取脈衝送到晶片，帶著狀態的訊號從另一條線回來，降頻、數位化之後，交給可程式邏輯晶片判別是零還是一。',
       '畫面示範讀到一的情況：結果在零點三五到零點五五微秒內回饋給波形產生器，送出把一翻回零的脈衝，這就是主動重置，最後才回傳電腦。'],
      actions=[(0, 0.2, _drv(0.05, 1)), (1, 0.3, _go(2.85, 0.33)), (2, 0.2, _go(5.3, 0.3)), (3, 1.5, _go(7.75, 0.24))],
      points=[('上傳、觸發', '電腦→同步器→各儀器'), ('驅動、讀取', '脈衝進去、訊號回來'), ('判別、回饋', '幾百奈秒內主動重置')],
      shot=(3, 6.0)),
 dict(key='phase', after=8, page='op', hash='pulse', scene='3D 場景 3：微波脈衝',
      title='動畫展示：相位差九十度', sub='三維動畫：微波脈衝——相位決定旋轉軸',
      sentences=[
       '換到操作量子電腦動畫的微波脈衝場景，畫面中間是驅動脈衝的波形，右邊的布洛赫球上，箭頭一開始指向北極的零。',
       '把脈衝面積設成九十度，連續送出兩個相位都是零度的脈衝，箭頭先倒到赤道，再一路轉到南極的一。',
       '按重設，先送一個同樣的脈衝讓箭頭倒到赤道，再把第二個脈衝的相位轉到九十度，就像時脈沒鎖好、相位飄走了，然後送出去。',
       '這一次箭頭動也不動，還停在赤道上，量到零和一的機會各一半；同樣兩個脈衝，只因為相位差了九十度，結果就從一變成一半一半。'],
      actions=[(0, 0.2, _drv('1e9', 0.5)), (1, 0.3, ('slider', '脈衝面積', 90)), (1, 0.6, ('click', '▶ 送出脈衝')),
               (1, 5.0, ('click', '▶ 送出脈衝')), (2, 1.0, ('click', '重設')), (2, 1.6, ('click', '▶ 送出脈衝')),
               (2, 5.3, ('slider', '脈衝相位', 90)), (2, 9.0, ('click', '▶ 送出脈衝'))],
      points=[('相位都是零度', '箭頭轉到南極'), ('第二個差九十度', '箭頭停在赤道'), ('相位飄走', '結果就變了')], shot=(3, 2.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q046'] 取用。"""

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

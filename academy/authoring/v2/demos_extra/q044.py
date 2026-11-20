"""Q044 降溫一次要幾天 — v2 動畫展示段（格式見 ../demos.py 的說明）。

控制項出處：
- animations/js/peripherals/04_cooldown.js：ui.slider('時間 (小時)', 0, 36, ...)（第 41 行）、ui.button('⏸ 暫停', ...)（第 43 行）；
  階段標籤 phase()（第 39 行）、凝結液滴 25<t<28 才出現（第 65 行）、溫度曲線小圖（第 52 行）、readout 小字（第 68 行）。
- animations/power1000.html 場景 outage：select('備援方案', ...)（第 409 行，選項值 none／full／gen）、
  metrics「停機時間（示意）」（第 440–441 行）。此頁的控制項不是 core.js 的 ui，所以用 ('js', ...) 改選單。
"""

LESSON = 'Q044'

_SEL = "document.querySelector('#controls select')"
_PICK_FULL = ("(function(){const s=" + _SEL + ";s.value='full';s.dispatchEvent(new Event('change'));window.__flash(s);})()")
_FLASH_SEL = "window.__flash(" + _SEL + ")"

_LIST = [
 dict(key='precool', after=4, page='pe', hash='cooldown', scene='周邊系統 3D 場景 4：降溫流程',
      title='動畫展示：抽真空和預冷', sub='三維動畫：降溫流程——從室溫出發',
      sentences=[
       '打開周邊系統動畫的降溫流程場景，先按暫停，再把時間滑桿拉回零小時，冷凍機上方寫著第一步，抽真空和檢漏。',
       '慢慢把時間往後撥，過了第二小時就進入脈衝管預冷，五十克耳文和四克耳文那兩層先開始變冷，下面三層隨後跟上，顏色從紅色漸漸轉成黃色。',
       '右下角的小圖畫著各層的溫度曲線，白色直線標出現在的時間；從第二小時到第二十五小時這一大段都還在預冷，是整趟降溫最花時間的部分。'],
      actions=[(0, 4.2, ('click', '⏸ 暫停')), (0, 7.0, ('slider', '時間 (小時)', 0)),
               (1, 1.0, ('sweep', '時間 (小時)', 0, 24, 9.0))],
      points=[('第一步', '抽真空與檢漏'), ('脈衝管預冷', '各層由紅轉黃'), ('第二到第二十五小時', '最花時間的一段')],
      shot=(1, 8.5)),
 dict(key='condense', after=6, page='pe', hash='cooldown', scene='周邊系統 3D 場景 4：降溫流程',
      title='動畫展示：凝結和稀釋循環', sub='三維動畫：降溫流程——一路冷到基溫',
      sentences=[
       '同一個場景，按暫停之後把時間撥到第二十六小時，上方換成第三步，凝結混合氣，冷凍機中間冒出一顆顆往下落的淡藍色小亮點。',
       '繼續往後撥，進入第四步稀釋循環，面板上混合腔的讀數在幾個小時內，從幾百毫克耳文一路掉到四十毫克耳文左右。',
       '撥到第三十六小時，上方寫著基溫穩定、可以開始量測，混合腔大約十毫克耳文。',
       '面板最下面還有一行小字：時間尺度只是典型示意，實際要看機型和負載。'],
      actions=[(0, 1.8, ('click', '⏸ 暫停')), (0, 4.0, ('slider', '時間 (小時)', 26)),
               (1, 1.0, ('sweep', '時間 (小時)', 28, 31, 4.5)),
               (2, 0.3, ('sweep', '時間 (小時)', 31, 36, 2.0))],
      points=[('第三步', '凝結的小亮點'), ('第四步', '混合腔一路往下掉'), ('第三十六小時', '約 10 mK')],
      shot=(2, 4.0)),
 dict(key='outage', after=8, page='pw', hash='outage', scene='1,000 位元供電設計 場景 5：斷電時間軸',
      title='動畫展示：停電兩分鐘換好幾天', sub='三維動畫：斷電時間軸——冷得慢，熱得快',
      sentences=[
       '換到千位元供電動畫的斷電時間軸，橫軸是對數時間，從一秒一路排到十天，金色曲線是混合腔的溫度。',
       '預設的方案只有控制電子接不斷電系統，冷卻一停，曲線大約兩分鐘就衝過一克耳文的紅色虛線，接下來要好幾天才降得回來。',
       '面板上的停機時間寫著大約三到五天，包含重新降溫和完整校準。',
       '改選冷卻鏈接上不斷電系統、再由發電機接手，整條曲線就平平貼在十毫克耳文，停機時間變成零。'],
      actions=[(1, 1.0, ('js', _FLASH_SEL)), (3, 1.0, ('js', _PICK_FULL))],
      points=[('方案 A', '約兩分鐘超過 1 K'), ('停機時間', '約三到五天'), ('方案 B', '曲線平貼 10 mK')],
      shot=(1, 6.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q044'] 取用。"""

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

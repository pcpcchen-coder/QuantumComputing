"""Q111 第 13 課：編譯與控制軟體堆疊 — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html#stack（第 12 章）。步驟按鈕在 #g12steps（程式動態產生、沒有 id；第 9 個是「自由實驗」，
  dur 0、不會自動接續，setup 是 BV @ 直線 5 顆、階段 0「原始電路」）。前兩段都在自由實驗裡用按鍵操作，不靠步驟 1–8 的 cue 時間軸
  （機器忙、幀率低時步驟腳本會比牆鐘慢）。自由實驗控制項（g12BindFree）：[data-ck12="bell"|"ghz"|"bv"]、
  [data-tp12="line"]「直線 5 顆」、[data-tp12="grid"]「方格 3×3」（換晶片保留目前階段、重新編譯）、#g12prevS「◀ 上一階段」、
  #g12nextS「下一階段 ▶」（並在左上角字幕寫 stageNote12）、#g12play「播放脈衝」（跳到階段 5、白色游標掃 6 秒的畫面時間）、
  #g12run「執行 2000 shots」（直方圖、每位元 2% 讀取誤判，隨機）。換晶片不會更新左上角字幕，所以 route 段換方格後再按一次
  「◀ 上一階段」「下一階段 ▶」，讓字幕寫出新的路由結果（插入 0 個 SWAP）。
  compile12 實際結果（與 classroom.py 的 stack_race.py 相同）：BV @ 直線 映射 q0→Q0、q1→Q1、q2→Q3、q3→Q2，1 個 CZ 兩端不相鄰，
  2 個 SWAP、CZ 3 → 9、抵消 4 對 H·H、總時間 1320 ns（閘做到 720 ns）；BV @ 方格 映射 q0→Q0、q1→Q2、q2→Q4、q3→Q1（Q1 有 3 個鄰居），
  0 個 SWAP、CZ 3、總時間 840 ns（閘做到 240 ns）。
op = animations/operation.html#workflow（場景 12）。工作封包每站約 2.2 秒自動前進（第 ⑤ 站 3.5 秒）；
  插圖「一個 shot 的時間組成（μs）與總執行時間」：重置 250 μs（主動重置 2.0 μs）、閘 = 深度 20 × 0.1 = 2.0 μs、讀取 1.0 μs；
  「每 shot … μs × … shots = …」，job < 1 s 時以 ms 顯示（toFixed(1)；被動 1000 shots = 253.0 ms、主動 1000 shots = 5.0 ms、主動 100,000 shots = 500.0 ms）；最後一行「另加：佇列、轉譯、波形載入、網路傳輸（秒～分鐘）」。
  控制項：toggle「主動重置（量測 + 條件 π 脈衝）」、slider「shots N」（log10，2–5，預設 3）。
"""

LESSON = 'Q111'

_STEP9 = ('sel', '#g12steps button:nth-child(9)')

_LIST = [
 dict(key='route', after=5, page='tr', hash='stack', scene='transmon 3D 第 12 章：軟體堆疊——自由實驗（BV 一階段一階段編譯，直線換方格）',
      title='動畫展示：直線晶片要搬家', sub='三維動畫：一步步看編譯器插入交換閘',
      sentences=[
       '打開超導晶片動畫第十二章，按第九步自由實驗，預設是猜密碼的電路放在直線五顆的晶片上，上方看板畫著原始電路。',
       '連按兩次下一階段，先分解成原生閘，再映射到實體位元；看板上有一個受控相位翻轉閘畫成紅色，代表它的兩端不相鄰。',
       '再按一次下一階段，路由插進兩個交換閘，看板上多了一大串紫色的閘，下方寫著受控相位翻轉閘從三個變成九個。',
       '接著把晶片換成方格，退一階段再前進，重新路由：輔助位元被放在有三個鄰居的位置，交換閘變成零個，受控相位翻轉閘只剩三個。'],
      actions=[(0, 0.5, _STEP9),
               (1, 0.4, ('id', 'g12nextS')), (1, 3.4, ('id', 'g12nextS')),
               (2, 0.4, ('id', 'g12nextS')),
               (3, 1.5, ('sel', '[data-tp12="grid"]')), (3, 3.0, ('id', 'g12prevS')), (3, 3.6, ('id', 'g12nextS'))],
      points=[('映射以後', '紅色＝兩端不相鄰'), ('直線晶片', '兩個交換閘，九個 CZ'), ('方格晶片', '零個交換閘，三個 CZ')], shot=(2, 5.0)),
 dict(key='pulse', after=7, page='tr', hash='stack', scene='transmon 3D 第 12 章：軟體堆疊——自由實驗（播放脈衝、換方格、執行 2000 shots）',
      title='動畫展示：奈秒時間軸賽跑', sub='三維動畫：同一個電路，兩種晶片的脈衝時間軸',
      sentences=[
       '回到第十二章的自由實驗，猜密碼電路還在直線晶片上，按播放脈衝，下方看板變成每顆位元的脈衝時間軸，總共一千三百二十奈秒。',
       '白色游標從左掃到右，掃到哪個閘，晶片上對應的位元就亮起來，做受控相位翻轉閘的那條連線會變成橘色。',
       '把晶片換成方格，再按一次播放脈衝，總時間縮短成八百四十奈秒；這一次，右邊藍色的讀取比前面所有的閘加起來還久。',
       '最後按執行兩千次，看板換成直方圖，最高的那一根就是密碼一一一；旁邊幾根矮的，是動畫故意加進去的讀取誤判。'],
      actions=[(0, 0.4, _STEP9), (0, 6.5, ('id', 'g12play')),
               (1, 0.2, ('id', 'g12play')),
               (2, 0.3, ('sel', '[data-tp12="grid"]')), (2, 3.0, ('id', 'g12play')),
               (3, 1.2, ('id', 'g12run'))],
      points=[('直線晶片', '一千三百二十奈秒'), ('方格晶片', '八百四十奈秒'), ('執行兩千次', '密碼一一一最高')], shot=(2, 6.5)),
 dict(key='workflow', after=8, page='op', hash='workflow', scene='3D 場景 12：完整流程——一個 shot 的時間組成（主動重置、shots N）',
      title='動畫展示：一次執行花多久？', sub='三維動畫：完整流程與一次執行的時間組成',
      sentences=[
       '換到操作量子電腦動畫的完整流程場景，發光的工作封包從寫程式出發，經過轉譯、脈衝排程和控制電子，送進冷凍機裡的晶片。',
       '右下角的插圖算一次執行要多久：沒有主動重置時，每次都要等兩百五十微秒，讓位元自己回到零態，跑一千次大約兩百五十三毫秒。',
       '打開主動重置，量到一就馬上補一個派脈衝，重置只要兩微秒，每次執行剩五微秒，一千次只要五毫秒。',
       '把重複次數拉到最大的十萬次，也才五百毫秒；插圖下方提醒，排隊、轉譯和網路傳輸，常常還要再花上幾秒到幾分鐘。'],
      actions=[(2, 0.4, ('toggle', '主動重置', True)),
               (3, 0.4, ('slider', 'shots N', 5))],
      points=[('被動等待', '重置佔了九成以上'), ('主動重置', '每次只剩五微秒'), ('十萬次', '還要加上排隊與傳輸')], shot=(3, 3.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q111'] 取用。"""

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

"""Q130 斷電的代價：2 分鐘換 2–5 天 — v2 動畫展示段（格式見 ../demos.py 的說明）。

本課前沒有任何一課用過 pe（peripherals.html）與 pw（power1000.html）；Q129 用 pw#overview、pe#infra 等全景，本課只用斷電、回溫、監控三個場景。

cooldown = peripherals.html#cooldown（js/peripherals/04_cooldown.js）。#controls：滑桿「時間 (小時)」0–36、按鈕「⏸ 暫停」「⟲ 重新開始」、滑桿「播放速度（小時/秒）」。
  載入後自動播放（1 小時/秒），且 core.js 每格 dt 上限 0.05 秒，WebGL 慢時時間會變慢；所以先按「⏸ 暫停」，再用 slider／sweep 直接拖「時間 (小時)」，時間點固定。
  phase()：t<2「① 抽真空 / 檢漏」、<25「② 脈衝管預冷」、<27.5「③ 凝結混合氣」（淺藍液滴 0x8ef0ff 落下，只在 25<t<28 出現）、<33「④ 稀釋循環 → 基溫」、之後「✓ 基溫穩定，可開始量測」。
  副標題「乾式稀釋冷凍機一次完整降溫約 1–2 天；升溫回室溫也需約 1 天」；右側各級溫度標籤；右下小圖「各級溫度隨時間（對數座標）」0–36 h，白色直線標目前時間。
outage = power1000.html#outage（SVG，不是 #controls button／.slider 結構，所以用 ('js', …)）。#controls 裡一個 <select>（備援方案：none／full／gen）與一個 range（UPS 撐住冷卻鏈的時間（方案 C），5–60，預設 15）。
  select 的 change 與 range 的 input 都會把 st.play 歸零（白點從 1 秒重新播）。白點 12 秒走完對數軸 1 秒→10 天（2 分約 4.2 秒、1 小時約 7.2 秒、1 天約 10 秒），停 0.6 秒再循環。
  方案 A：t0=0，約 119 秒到 1 K，1 小時升到 30 K，之後約 3.5 天降回 10 mK；讀數「停機時間（示意）約 3–5 天（含重新降溫與完整校準）」。
  方案 B：整條 10 mK，「0（不受影響）」綠色。方案 C：平到 UPS 分鐘數才上升，「約 3–5 天（UPS 耗盡後同 A）」。上方標籤「t = … MXC ≈ …」依溫度變綠／金／紅。
monitor = peripherals.html#monitor（js/peripherals/09_monitor.js）。#controls 按鈕「正常運轉」「冷卻水中斷」「真空洩漏」「流阻堵塞」，下方 readout。
  冷卻水中斷：入水 18 °C 起每秒 +2.2（時間加速），狀態立刻 WARN（黃字）、入水 >27 °C ALARM（紅字，儀表櫃上的圓燈變紅跳動）；≥32 °C 聯鎖停壓縮機（「壓縮機 停止」），紫色氣流改走混合氣儲存槽；
  之後各級溫度上升、溫度計小球變紅、右下「監控曲線（最近 60 秒，時間加速）」四條線往上翹。WebGL 慢時情境時間也會變慢，旁白只描述先後順序，不念秒數。
已用 Playwright 單張截圖確認以上畫面（scratchpad q130/shot1.js、shot2.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q130'

# power1000.html 的控制項不是按鈕，用 js 設值並送 change／input 事件
_SC = ("(function(){var s=document.querySelector('#controls select');window.__flash(s);"
       "s.value='%s';s.dispatchEvent(new Event('change'));})()")
_UPS = ("(function(){var i=document.querySelector('#controls input[type=range]');window.__flash(i.closest('.ctl'));"
        "i.value=%d;i.dispatchEvent(new Event('input'));})()")

_LIST = [
 dict(key='cooldown', after=4, page='pe', hash='cooldown', scene='周邊系統 3D 場景 4：降溫流程——從室溫到 10 mK',
      title='動畫展示：重新降溫為什麼要好幾天', sub='三維動畫：稀釋冷凍機的降溫流程',
      sentences=[
       '打開周邊系統動畫的降溫流程場景，左上角的副標題寫著，乾式稀釋冷凍機完整降溫一次大約要一到兩天；先按暫停，把時間拉回零。',
       '把時間往後拖，最上面的大字先是抽真空，接著換成最花時間的脈衝管預冷，右邊各層的溫度數字一路往下掉。',
       '大約一天之後，混合氣凝結成淺藍色的小液滴往下掉，接著稀釋循環啟動，最下面的混合腔幾個小時內就降到最低溫。',
       '大字換成基溫穩定、可以開始量測，右下角曲線圖上的白線一路移到三十六小時；這還只是降溫，接著還要把每顆位元重新校準。'],
      actions=[(0, 10.8, ('click', '⏸ 暫停')), (0, 12.2, ('slider', '時間 (小時)', 0)),
               (1, 0.3, ('sweep', '時間 (小時)', 0, 2, 2.5)), (1, 2.9, ('sweep', '時間 (小時)', 2, 24, 7.5)),
               (2, 0.3, ('sweep', '時間 (小時)', 24, 27, 4.0)), (2, 6.0, ('sweep', '時間 (小時)', 27, 34, 4.5)),
               (3, 0.3, ('sweep', '時間 (小時)', 34, 36, 1.5))],
      points=[('脈衝管預冷', '最花時間的一段'), ('凝結與循環', '幾小時降到最低溫'), ('降溫之後', '還要重新校準')], shot=(3, 4.0)),
 dict(key='outage', after=7, page='pw', hash='outage', scene='1,000 位元供電動畫 場景 5：斷電時間軸——方案 A、B、C',
      title='動畫展示：三種方案的斷電時間軸', sub='互動動畫：斷電時間軸——2 分鐘換 2–5 天',
      sentences=[
       '換到一千位元供電動畫的斷電時間軸，橫軸是對數時間，從一秒排到十天；金色曲線是混合腔的溫度，紅色虛線是一克耳文。',
       '第一種方案只有控制電子接不斷電系統：白點一出發，大約兩分鐘就衝過紅線，一小時後升到大約三十克耳文，好幾天後才降回來。',
       '換成第二種方案，冷卻鏈接上不斷電系統，再由發電機接手：整條曲線平平貼在最底下，左邊的停機時間變成零。',
       '第三種是發電機沒起來，把不斷電系統撐住的時間拉到三十分鐘：曲線平平走到三十分鐘才往上衝，停機時間又變回三到五天。'],
      actions=[(1, 0.2, ('js', _SC % 'none')),
               (2, 0.3, ('js', _SC % 'full')),
               (3, 0.3, ('js', _SC % 'gen')), (3, 4.2, ('js', _UPS % 30))],
      points=[('第一種方案', '兩分鐘衝過一克耳文'), ('第二種方案', '曲線平貼，停機為零'), ('第三種方案', '撐完才往上衝')], shot=(1, 9.5)),
 dict(key='monitor', after=8, page='pe', hash='monitor', scene='周邊系統 3D 場景 9：監控、聯鎖與故障處置——冷卻水中斷',
      title='動畫展示：電還在，冷卻水斷了', sub='三維動畫：監控、聯鎖與故障處置',
      sentences=[
       '最後打開周邊系統動畫的監控與聯鎖場景，左邊先選正常運轉：狀態是綠色的，冷卻水入水十八度，壓縮機在運轉。',
       '按下冷卻水中斷，入水溫度一路往上爬，狀態先變成黃色的警告，接著轉成紅色的告警，儀表櫃上的圓燈也變紅跳動。',
       '水溫一超過上限，聯鎖就自動停掉壓縮機，紫色的氣流改走儲存槽，把混合氣收回去，保護昂貴的氦三。',
       '少了壓縮機，各層溫度計的小球大多變成紅色，右下角的監控曲線全部往上翹；電明明還在，冷卻水一斷，冷凍機照樣回溫。'],
      actions=[(0, 4.6, ('click', '正常運轉')), (1, 0.3, ('click', '冷卻水中斷'))],
      points=[('冷卻水中斷', '警告轉成告警'), ('聯鎖', '停壓縮機、回收混合氣'), ('冰水機', '也是關鍵負載')], shot=(3, 5.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q130'] 取用。"""

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

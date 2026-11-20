"""Q129 電從哪裡來、到哪裡去 — v2 動畫展示段（格式見 ../demos.py 的說明）。

pe 與 pw 兩頁在 Q129 之前都沒有任何一課的展示段用過。本課刻意避開斷電相關的畫面與操作（Q130 會用 pw#outage、pe#monitor）：
不勾 pw#overview 的「模擬斷電（市電中斷）」、不點痛點 1（UPS 與冷卻中斷）；不用 pe#infra（右下插圖是停電後的溫度曲線，Q133 也會用到）。

circuits = peripherals.html#overview（js/peripherals/01_overview.js）。#controls 的按鈕：「脈衝管氦氣」「冷卻水」「混合氣循環」「真空」「微波 / DC」
  「資料 / 時脈」「電力」（各自開關，預設全開）、「全部顯示」「只看冷卻相關」（pt、water、mix、vac）「只看訊號相關」（rf、data）、三個視角按鈕。
  按「只看訊號相關」→「微波」→「資料」→「電力」之後只剩黃色電力線：配電盤 → UPS 不斷電 → 控制電子機櫃、控制電腦；配電盤 → 冷卻水機、壓縮機；UPS → GHS。
  再按「只看冷卻相關」：綠色脈衝管氦氣、藍色冷卻水、紫色混合氣、灰色真空。右下插圖「典型用電分配（kW，示意）」：脈衝管壓縮機 10.7（綠）、
  冷卻水系統 10.0（藍）、控制電子機櫃 3.0（紫）、氣體處理系統（泵）1.5（青）、電腦 / 監控 / 網路 1.0（灰），底下「合計約 26 kW（依機型與規模而異）」。
coldhead = peripherals.html#pulsetube（02_pulsetube.js）。氦壓縮機標籤「氦壓縮機 電力 ~10 kW · 水冷」；高壓氦（~2 MPa，紅橘色粒子）、低壓氦（~0.8 MPa，藍色）
  兩條軟管；冷卻水 進（藍）/ 出（橘）；金色標籤「一級冷端 ~45 K（~40 W）」「二級冷端 ~3 K（~1.5 W @ 4.2 K）」。右下插圖（冷頭內壓力）會蓋住二級冷端標籤，
  所以開頭用 ('js', …) 把 #inset-wrap 隱藏（截圖 pt1.png）。旋轉閥是對稱圓柱，看不出在轉，旁白不提。
facility = power1000.html#overview（SVG 場景，不是 three.js）。左到右：中壓進線（雙迴路＋發電機）→ 分層 UPS（80–270 kW）→ 機電（約 80 kW）／乾淨（約 70 kW）／
  運算（約 30 kW）三條匯流排 → 八個負載方塊 → 稀釋冷凍機；粒子顏色：機電橘、乾淨青、運算紫，粒子密度代表功率。紅色痛點是 SVG 的 g.pp（依序 1–7），
  沒有 HTMLElement.click，所以用 ('js', …) 送 MouseEvent('click')。點痛點 2、4、7：面板「痛點 2 壓縮機：最大的單一負載」「每支脈衝管 ≈ 12.5 kW 壓縮機…」、
  「痛點 4 2,500–3,000 路精密直流」「約 110 台 24 通道儀器…」、「痛點 7 解碼要緊鄰機台」；面板第一列一直是「設施總功率（中點）約 200 kW」（截圖 pw2.png）。
已用 Playwright 單張截圖確認以上畫面（scratchpad q129shot/shot.js；nice -n 19，未做錄影或 QV2_DRY）。
"""

LESSON = 'Q129'

# 右下插圖會蓋住「二級冷端」標籤，先隱藏
_HIDE_INSET = "document.getElementById('inset-wrap').style.display='none';"


def _pp(n):
    """點 power1000.html#overview 的第 n 個紅色痛點（SVG 元素，用 MouseEvent）。"""
    return ("(function(){var g=document.querySelectorAll('#svg g.pp')[%d];window.__flash(g);"
            "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));})()" % (n - 1))


_LIST = [
 dict(key='circuits', after=4, page='pe', hash='overview', scene='周邊系統 3D 場景 1：機房全景——只看電力線，再只看冷卻相關，對照右下的典型用電分配',
      title='動畫展示：機房裡的電力線', sub='三維動畫：量子電腦機房全景——設備與連接',
      sentences=[
       '打開周邊系統動畫的第一個場景，機房中央是稀釋冷凍機，四周擺著配電盤、不斷電系統、電子機櫃、壓縮機和冷卻水機。',
       '先按只看訊號相關，再把微波和資料兩條關掉、把電力打開，畫面上只剩一條條黃色的電力線。',
       '黃線從配電盤出發，接到不斷電系統、電子機櫃和控制電腦，也接到壓縮機、冷卻水機和氣體處理系統。',
       '最後按只看冷卻相關，綠色氦氣、藍色冷卻水、紫色混合氣流個不停；右下角的用電分配圖裡，壓縮機和冷卻水就佔了大半。'],
      actions=[(1, 0.6, ('click', '只看訊號相關')), (1, 2.6, ('click', '微波')), (1, 3.4, ('click', '資料')),
               (1, 5.0, ('click', '電力')),
               (3, 0.6, ('click', '只看冷卻相關'))],
      points=[('黃色電力線', '從配電盤接到每台設備'), ('只看冷卻相關', '氦氣、冷卻水、混合氣'), ('用電分配圖', '壓縮機＋冷卻水佔大半')], shot=(3, 8.0)),
 dict(key='coldhead', after=6, page='pe', hash='pulsetube', scene='周邊系統 3D 場景 2：脈衝管冷卻器＋氦壓縮機——電力約 10 kW 換來 4 K 約 1.5 W',
      title='動畫展示：一萬瓦換一點五瓦', sub='三維動畫：脈衝管冷卻器與氦壓縮機',
      sentences=[
       '換到同一個動畫的脈衝管場景：左邊的氦壓縮機標著電力約一萬瓦、水冷，右邊高高的冷頭就是它要餵飽的對象。',
       '紅色粒子是高壓氦氣、藍色是低壓氦氣，沿著兩條軟管在壓縮機和冷頭之間流動。',
       '看冷頭旁的兩塊金色標籤：一級冷端約絕對溫度四十五度、冷卻能力約四十瓦；二級冷端約三度，只有約一點五瓦。',
       '壓縮機腳邊還有冷卻水一進一出：一萬瓦的電換來不到兩瓦的低溫冷卻，其餘幾乎都變成熱，由冷卻水帶走。'],
      actions=[(0, 0.2, ('js', _HIDE_INSET))],
      points=[('氦壓縮機', '電力約 10 kW、水冷'), ('二級冷端', '約 1.5 W @ 4.2 K'), ('冷卻水', '把熱帶走')], shot=(2, 6.0)),
 dict(key='facility', after=9, page='pw', hash='overview', scene='1,000 位元供電動畫場景 1：全景——三條匯流排、八個負載，點痛點 2、4、7',
      title='動畫展示：千位元設施的用電全景', sub='互動動畫：全景——電從哪裡來、到哪裡去',
      sentences=[
       '最後打開一千位元供電動畫的全景場景：左邊是中壓進線，接著是分層不斷電系統，再分成機電、乾淨、運算三條匯流排。',
       '粒子越密代表功率越大：橘色流向壓縮機和冰水機，青色流向控制電子和精密直流，紫色流向即時解碼和電子區空調。',
       '點紅色二號，面板寫著壓縮機是最大的單一負載，每支脈衝管約一萬兩千五百瓦；再點四號，精密直流要兩千五百到三千路。',
       '最後點七號，即時解碼要緊鄰機台；面板最上面也寫著，整座設施中點合計約兩百千瓦。'],
      actions=[(2, 0.6, ('js', _pp(2))), (2, 8.6, ('js', _pp(4))),
               (3, 0.5, ('js', _pp(7)))],
      points=[('三條匯流排', '機電、乾淨、運算'), ('粒子密度', '代表功率大小'), ('紅色編號', '點開看痛點說明')], shot=(3, 6.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q129'] 取用。"""

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

"""Q135 磁場與配電佈局：母線離冷凍機多遠 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都在 power1000.html#field（本課是磁場的主場；Q133 只示範過取消「交流（50/60 Hz）」勾選，本課不再碰那個勾選）：
  wiring   after=4（「磁場的四個來源」之後）  「配線方式」選單：成對 → 單根 → 拉距離 → 變壓器（近似偶極）
  current  after=5（「比一比：單根 vs 成對」之後）「電流」360→1000 A、「成對間距」10→2 cm、再拉「與冷凍機距離」到 7 m
  distance after=7（「移動母線的紀錄」之後）  「與冷凍機距離」3 → 6 → 9 → 1 m（課綱動手任務：移動母線、記錄冷凍機處磁場）

畫面依據（animations/power1000.html，S({ id: 'field' …})，約第 454–495 行；秒數以「字數 ÷ 4.5」估）：
  build()：預設 st.I=360、st.d=3、st.mode='pair'、st.s=0.1、st.ac=true。控制項文字：滑桿「電流」(50–2000, step 10, 顯示「360 A」)、
    「與冷凍機距離」(0.5–10, step 0.1, 顯示「3.0 m」)、選單「配線方式」(single「單根（淨電流不為零）」／pair「去回線成對」／
    dipole「變壓器（近似偶極）」)、滑桿「成對間距」(0.02–0.5, step 0.01, 顯示「10 cm」)、勾選「交流（50/60 Hz）」（本課不動）。
  B(st,r)：mu=2e-7；single → mu·I/r；pair → mu·I·s/r²；dipole → mu·I·0.2/r³。
  render()：母線為 x=130 的直條 fill #e0a54a（橘黃），文字「母線（成對）」或「母線（單根）」；dipole 時改畫方塊與文字「變壓器」；
    冷凍機圓圈在 fx = 130 + d×95，下方距離文字 d.toFixed(1)+' m'；右上框「冷凍機位置磁場 ≈ X µT」（X≥1 用 1 位小數，否則 3 位）；
    交流時 ok = B < 0.1 µT，綠 #3ccf8e「符合」，否則紅 #ff5a5f「超過：拉開距離、成對配線、補償線圈或屏蔽」。
    熱圖色相 (1−v)×200，v = (log10 B[µT] + 1)/4；熱圖只依母線位置而定，拉距離時只有冷凍機圓圈移動。
  以下數字皆已用 headless Chromium 開頁、執行同樣的 js 後讀出畫面文字核對（2026-11-18）。

wiring
  句 0（60 字，約 13.3 秒）：預設 pair、3 m → 2e-7×360×0.1／9 = 0.800 µT，紅色；截圖可見母線旁黃紅條紋→綠→右側藍。
  句 1（48 字，約 10.7 秒）：1.5 秒時「配線方式」選 single → 2e-7×360／3 = 24.0 µT；文字變「母線（單根）」；熱圖整片轉黃綠、右側不再有藍色。
  句 2（45 字，約 10.0 秒）：1.0 秒起 3 秒內把「與冷凍機距離」由 3 拖到 6 → 12.0 µT（一半）；圓圈右移，距離字「6.0 m」。
  句 3（55 字，約 12.2 秒）：1.0 秒時選 dipole → 2e-7×360×0.2／216 = 0.067 µT，綠色「符合」；母線直條換成「變壓器」方塊，色塊只在方塊附近一小團。
current
  句 0（58 字，約 12.9 秒）：2.5 秒起 4 秒內把「電流」由 360 拖到 1000 → 2e-7×1000×0.1／9 = 2.2 µT（紅）。
  句 1（45 字，約 10.0 秒）：「2.2 µT」對照文獻回顧 §3.4.3 表「同上，距離 3 m 約 2 µT」；4.0 秒起 2 秒內「成對間距」10→2 cm →
       2e-7×1000×0.02／9 = 0.444 µT（紅）。
  句 2（47 字，約 10.4 秒）：2.2 → 0.444 為五分之一（少了五分之四）；仍是紅色「超過」；交流判斷線「此處以 0.1 µT 判斷」。
  句 3（46 字，約 10.2 秒）：1.0 秒起 3 秒內「與冷凍機距離」3→7 → 4e-6／49 = 0.082 µT，綠色「符合」（6.4 m 附近轉綠）。
distance
  句 0（44 字，約 9.8 秒）：預設畫面，0.800 µT 紅色「超過」。
  句 1（48 字，約 10.7 秒）：1.5 秒起 4 秒內「與冷凍機距離」3→6；圓圈 fx 由 415 移到 700；6 m → 7.2e-6／36 = 0.200 µT（紅），為 0.8 的四分之一。
  句 2（44 字，約 9.8 秒）：1.0 秒起 5 秒內 6→9；8.4 m 為 0.102（紅）、8.5 m 為 0.100（綠「符合」，因 B<0.1 用未四捨五入值）；跨線約在句內 5.2 秒，「變成綠色的符合」約在 5–6.4 秒說到；9 m → 0.089 µT 綠。
  句 3（56 字，約 12.4 秒）：1.0 秒起 2.5 秒內 9→1 → 7.2 µT 紅；圓圈退到母線旁的綠色帶（熱圖不變，只有圓圈移動）。

試拍需確認：自寫的逐步拖動（setInterval 每 1/12 秒送一次 'input'）在錄影中是否順暢；黃色外框（.qflash）是否出現在被拖的滑桿上；
current 句 0 的拖動在 6.5 秒結束，「二點二」約在第 11 秒說到，確認數字已停住。
"""
import json

LESSON = 'Q135'


def _pw_sel(label, value):
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const s=d.querySelector('select');window.__flash(d);s.value=%s;s.dispatchEvent(new Event('change'));})()"
            % (json.dumps(label), json.dumps(value)))


def _pw_sl(label, value):  # power1000 的 .ctl 滑桿：設 input.value 後送出 'input' 事件
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const i=d.querySelector('input');window.__flash(d);i.value=%s;i.dispatchEvent(new Event('input'));})()"
            % (json.dumps(label), json.dumps(str(value))))


def _pw_sweep(label, a, b, secs):  # 在頁面內用 setInterval 逐步改滑桿值（每秒 12 步），每步送出 'input'；拖動期間滑桿加黃框
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const i=d.querySelector('input');const a=%r,b=%r,n=Math.max(2,Math.round(%r*12));let k=0;d.classList.add('qflash');"
                  "const h=setInterval(()=>{k++;i.value=String(a+(b-a)*k/n);i.dispatchEvent(new Event('input'));"
                  "if(k>=n){clearInterval(h);i.value=String(b);i.dispatchEvent(new Event('input'));setTimeout(()=>d.classList.remove('qflash'),300);}},%d);})()"
            % (json.dumps(label), a, b, secs, round(secs * 1000 / max(2, round(secs * 12)))))


_LIST = [
 dict(key='wiring', pmap=[0, None, 1, 2], after=4, page='pw', hash='field', scene='1,000 位元供電互動動畫 場景 6：磁場與配電佈局',
      title='動畫展示：三種配線，三種衰減', sub='互動動畫：磁場與配電佈局',
      sentences=[
       '打開磁場場景，先看預設的去回線成對：冷凍機在三公尺外，右上角讀數零點八微特斯拉，色塊從母線旁的紅黃條紋，經過綠色，慢慢褪成右邊的藍色。',
       '把配線方式換成單根，淨電流不為零，同樣三公尺，讀數一下跳到二十四微特斯拉，大部分色塊都變成黃綠色。',
       '再把與冷凍機距離從三公尺拉到六公尺，單根的讀數只降到十二微特斯拉，距離加倍，磁場才少一半。',
       '最後換成變壓器的近似偶極，同樣六公尺，讀數只剩零點零六七微特斯拉，變成綠色的符合，色塊縮成變壓器旁邊的一小團。'],
      actions=[(1, 1.5, _pw_sel('配線方式', 'single')), (2, 1.0, _pw_sweep('與冷凍機距離', 3, 6, 3.0)),
               (3, 1.0, _pw_sel('配線方式', 'dipole'))],
      points=[('成對三公尺', '零點八微特斯拉'), ('單根', '距離加倍只少一半'), ('變壓器偶極', '六公尺就符合')], shot=(3, 6.0)),
 dict(key='current', after=5, page='pw', hash='field', scene='1,000 位元供電互動動畫 場景 6：磁場與配電佈局',
      title='動畫展示：電流加大，配線並緊', sub='互動動畫：磁場與配電佈局',
      sentences=[
       '回到磁場場景，這次只動電流：把滑桿從預設的三百六十安培一路拉到一千安培，成對母線、三公尺外的讀數升到二點二微特斯拉。',
       '這和文件估算的大約兩微特斯拉對得上；接著把成對間距從十公分縮到兩公分，讀數降到零點四四四。',
       '兩條線並得更緊，磁場少了五分之四，可是右上角還是紅色的超過，因為交流的判斷線是零點一微特斯拉。',
       '最後把距離拉到七公尺，等滑桿停下來，讀數掉到零點零八二，才變成綠色的符合；並緊配線有幫助，距離仍然少不了。'],
      actions=[(0, 2.5, _pw_sweep('電流', 360, 1000, 4.0)), (1, 4.0, _pw_sweep('成對間距', 0.1, 0.02, 2.0)),
               (3, 0.5, _pw_sweep('與冷凍機距離', 3, 7, 2.5))],
      points=[('一千安培', '三公尺外約二點二微特斯拉'), ('間距縮到兩公分', '仍然超過'), ('拉到七公尺', '才符合')], shot=(3, 8.0)),
 dict(key='distance', pmap=[0, 1, 2, None], after=7, page='pw', hash='field', scene='1,000 位元供電互動動畫 場景 6：磁場與配電佈局',
      title='動畫展示：移動母線，記錄磁場', sub='互動動畫：磁場與配電佈局',
      sentences=[
       '照紀錄表的方法再做一次：成對母線、三百六十安培，從三公尺開始，讀數零點八，是紅色的超過。',
       '把與冷凍機距離的滑桿慢慢往右拖，冷凍機的圓圈跟著往右走，到六公尺時讀數是零點二，正好是四分之一。',
       '繼續慢慢拖到九公尺，留意右上角的文字：大約八點五公尺時，紅色的超過變成綠色的符合，最後停在零點零八九。',
       '反過來把冷凍機推近到一公尺，讀數衝到七點二微特斯拉，圓圈退回母線旁邊的綠色帶，這就是母線不能貼著冷凍機走的原因。'],
      actions=[(1, 1.5, _pw_sweep('與冷凍機距離', 3, 6, 4.0)), (2, 0.5, _pw_sweep('與冷凍機距離', 6, 9, 5.0)),
               (3, 1.0, _pw_sweep('與冷凍機距離', 9, 1, 2.5))],
      points=[('三公尺', '零點八，超過'), ('六公尺', '剩四分之一'), ('九公尺', '低於判斷線，符合')], shot=(2, 8.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

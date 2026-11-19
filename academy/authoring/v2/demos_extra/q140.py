"""Q140 低溫熱預算：熱帳怎麼變成電 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段（Q131–Q139 都沒用過 pw#heat 與 pe#wiring）：
  wiring  after=4（「逐層估算的方法」之後）   pe#wiring：「量子位元數（線束示意）」20 → 200，再按「讀取輸出」
  ledger  after=6（「熱帳怎麼變成電」之後）   pw#heat：讀預設七列，再把「稀釋單元／脈衝管數」3 → 7（硬撐到過關）
  wires   after=10（「換你改造：線材與多工」之後）pw#heat：勾「改用 0.047" 細同軸」→ 勾「磁通線改用超導 NbTi」→「稀釋單元」設 2

畫面依據
(A) animations/power1000.html，S({ id: 'heat' …}) 約第 299–347 行；共用 PER_LINE／CAP／lines()／heat()／fmtW 約第 75–100 行。
  build()：st.N=1000、st.du=3、thin／nbti／hot／cryo 皆 false。控制項（一字不差）：
    滑桿「量子位元數 N」(100–3000, step 50, 預設 1000)、滑桿「稀釋單元／脈衝管數」(1–8, step 1, 預設 3，顯示「3 組」)、
    勾選框「改用 0.047" 細同軸」「磁通線改用超導 NbTi」「容忍 CP 200 mK、MXC 30 mK」「低溫 CMOS＋多工（4 K 每位元 1.5 mW）」。
    _pw_sl('稀釋單元', …) 只對到第二根滑桿；_pw_tog('細同軸'／'超導 NbTi') 各只對到一個勾選框。
  render()：左邊冷凍機示意五層冷盤，標「50 K」「4 K」「Still」「CP」「MXC」，底下「量子晶片」；右邊七列：
    「50 K」「4 K」「Still」「CP」「MXC 被動」「MXC 磁通直流」「MXC 合計」，每列文字「負載 / 容量」與「超過 x%」或「使用 x%」；
    橫條顏色 frac > 1 紅 #ff5a5f、> 0.75 橘黃 #e0a54a、其餘綠 #3ccf8e；白色虛線在 frac = 1（x = 470 + 460/1.6），底下小字「虛線＝可用冷卻上限」。
    面板 metrics：「進冷凍機的線」「稀釋單元／脈衝管」「壓縮機電力」= du × 12.5 kW、「加冷卻水（約 0.6×）」= du × 7.5 kW、「熱帳」過關／不過關（七列皆 ≤ 1）。
  以下數字是把上述公式照抄成 node 腳本算出（2026-11-18；依指示錄影進行中不開瀏覽器，未開頁核對）：
    預設（du 3）：50 K 202 W / 158 W 超過 28% 紅；4 K 4.5 W / 5.7 W 使用 79% 橘黃；Still 10.5 mW / 120 mW 9% 綠；CP 1.3 mW / 600 µW 超過 115% 紅；
      MXC 被動 81.3 µW / 90.0 µW 90% 橘黃；MXC 磁通直流 125 µW / 90.0 µW 超過 39% 紅；MXC 合計 206 µW / 90.0 µW 超過 129% 紅；
      進冷凍機的線 3,875 條；壓縮機電力 37.5 kW；加冷卻水 22.5 kW；熱帳 不過關。
    du 4：50 K 96%（橘黃）；MXC 磁通直流 104%、CP 161%、合計 172% 仍紅。du 5：磁通直流 83%；CP 129%、合計 137% 紅。du 6：CP 107%、合計 115% 紅。
    du 7：50 K 55%、4 K 34%、CP 92% 橘黃、MXC 被動 39%、磁通直流 60%、MXC 合計 206 µW / 210 µW 使用 98% 橘黃 → 熱帳 過關；壓縮機電力 87.5 kW、加冷卻水 52.5 kW。
    細同軸（du 3）：50 K 54.5 W / 158 W 使用 35% 綠；4 K 1.3 W 23%；CP 369 µW 62%；MXC 被動 21.9 µW 24%；
      MXC 磁通直流 500 µW / 90.0 µW 超過 456% 紅；MXC 合計 522 µW 超過 480% 紅；熱帳 不過關（heat() 的 k = 0.27、fluxDC ×4）。
    細同軸＋NbTi（du 3）：MXC 被動 18.6 µW 21%；MXC 磁通直流「0.0 µW / 90.0 µW」使用 0%；MXC 合計 18.6 µW / 90.0 µW 使用 21%；七列皆綠 → 熱帳 過關，37.5 kW。
    細同軸＋NbTi（du 2）：50 K 54.5 W / 105 W 52%；4 K 1.3 W / 3.8 W 34%；CP 369 µW / 400 µW 92% 橘黃；MXC 合計 18.6 µW / 60.0 µW 31%；
      熱帳 過關；壓縮機電力 25.0 kW、加冷卻水 15.0 kW（87.5 − 25 = 62.5 kW）。
(B) animations/js/peripherals/05_wiring.js（App.register id 'wiring', num 5）＋ common.js PD.wiring：
  六條線（顏色不同）：「XY 驅動」「Z 磁通」「讀取輸入」「TWPA 泵浦」「讀取輸出」「直流線束」；讀取輸出的粒子往上走，其餘往下。
  滑桿「量子位元數（線束示意）」1–200, step 1, 預設 20；按鈕列「全部」＋六條線的名稱（radio）；readout；
  inset 標題「各級熱負載 / 可用冷卻功率（示意估算）」，五列「50 K」「4 K」「Still」「Cold plate」「MXC」，百分比 > 100 紅、> 50 橘黃、其餘綠，
  底下小字「100 % = 該級冷卻功率用盡（紅色）」；desc 寫著熱負載在「（右下角）」。
  counts(n)：XY n、Z n、讀取輸入／輸出／泵浦各 ceil(n/6)；同軸 = 2n + 3·ceil(n/6)；每級熱 = 同軸 × passive + (XY+輸入+泵浦) × attDiss（4 K 再加 輸出 × 5 mW HEMT）。
  node 算出：n = 20 → 同軸共 52 條，Cold plate 11%、50 K 8%（全綠）。n = 97 Cold plate 轉橘黃、n = 133 50 K 轉橘黃、n = 195 Cold plate 轉紅。
    n = 200 → 同軸共 502 條；50 K 22.59 W / 30.00 W 75% 橘黃；4 K 45%；Still 4%；Cold plate 206.2 μW / 200.0 μW 103% 紅；MXC 42%。
  按「讀取輸出」：其他線淡出（opacity 0.06），相機飛近；讀取輸出各級元件標籤出現：「室溫放大」「HEMT ~40 dB」「隔離器 + TWPA」；
    readout 加上 INFO.rout：「…→ 4 K HEMT（~40 dB，耗電 5–10 mW）→ 室溫放大 …」與「目前 200 顆量子位元 → 此類線 34 條」。

逐句（秒數以「字數 ÷ 4.5」估）
wiring
  句 0（56 字，約 12.4 秒）：不操作。六色線、inset（右下角，依 desc）。
  句 1（59 字，約 13.1 秒）：5.0 秒起 5 秒內滑桿 20 → 200（record_demo 的 sweep 會四捨五入成整數）；Cold plate 約 6.9 秒橘黃、50 K 約 8.1 秒橘黃
       （「冷板那條先變橘黃，接著是五十克耳文」約 9.8–13 秒說到）；Cold plate 約 9.8 秒轉紅（句 2 才說）。readout「同軸共 52 條」在 0 秒已顯示。
  句 2（49 字，約 10.9 秒）：停在 200：同軸共 502 條；Cold plate 103% 紅；50 K 75%。
  句 3（53 字，約 11.8 秒）：0.5 秒按「讀取輸出」：HEMT 標籤在 4 K 那層出現；readout 說明「耗電 5–10 mW」。
ledger
  句 0（47 字，約 10.4 秒）：不操作。五層冷盤、七列、白色虛線。
  句 1（49 字，約 10.9 秒）：不操作。50 K「202 W / 158 W」紅、「超過 28%」。
  句 2（45 字，約 10.0 秒）：不操作。MXC 合計「206 µW / 90.0 µW」「超過 129%」；metrics「熱帳 不過關」。
  句 3（54 字，約 12.0 秒）：1.0 秒起 3 秒內「稀釋單元」3 → 7（每秒 12 步；step 1 由瀏覽器取整）；4.0 秒到 7 組 → 熱帳 過關（「熱帳過關」約 5.8 秒說到）；
       壓縮機電力 37.5 → 87.5 kW。
wires
  句 0（52 字，約 11.6 秒）：3.6 秒勾「改用 0.047" 細同軸」（「勾選改用細同軸」約 3.6–5.3 秒）；50 K → 54.5 W、使用 35%。
  句 1（37 字，約 8.2 秒）：不操作。MXC 磁通直流 500 µW、超過 456%；熱帳 不過關。
  句 2（39 字，約 8.7 秒）：0.6 秒勾「磁通線改用超導 NbTi」：磁通直流「0.0 µW」；MXC 合計 18.6 µW；熱帳 過關（du 仍 3）。
  句 3（48 字，約 10.7 秒）：1.8 秒「稀釋單元」設 2（「減到兩組」約 2.7 秒說完）：熱帳 過關；壓縮機電力 25.0 kW；「比硬撐的七組」指 ledger 段 87.5 kW。

試拍需確認：(1) pe#wiring 預設相機下，inset 是否真的在右下角、五列標籤（Cold plate）是否可讀；(2) 拉到 200 時「線束越來越密」在畫面上看得出來
（線束 group 在原點附近、六條主線在 z = 0.25，可能被冷盤擋住）；(3) 按「讀取輸出」後相機 flyTo 完成時，「HEMT ~40 dB」金色標籤是否在 4 K 那層旁、
沒有被面板蓋住；readout 的「耗電 5–10 mW」是否在面板可見範圍內（INFO 文字很長，面板可能要捲動）；(4) pw#heat 的 _pw_sweep 拖 step 1 滑桿時
du 是否逐格變化、七列是否跟著重畫；(5) 黃色外框是否落在被動的滑桿／勾選框；(6) metrics「熱帳」「壓縮機電力」兩格在 1600×900 畫面內可見。
"""
import json

LESSON = 'Q140'


def _pw_tog(label, on):
    return ('js', "(()=>{const l=[...document.querySelectorAll('#controls label.tog')].find(x=>x.textContent.includes(%s));"
                  "const i=l.querySelector('input');window.__flash(l);if(i.checked!==%s){i.checked=%s;i.dispatchEvent(new Event('change'));}})()"
            % (json.dumps(label), 'true' if on else 'false', 'true' if on else 'false'))


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


_DU = '稀釋單元'

_LIST = [
 dict(key='wiring', pmap=[None, 0, 1, 2], after=4, page='pe', hash='wiring', scene='周邊系統 3D 場景 5：低溫佈線',
      title='動畫展示：線一多，冷板先喊緊', sub='三維動畫：低溫佈線與各級熱負載',
      sentences=[
       '先打開周邊系統動畫的低溫佈線場景，六種顏色的線從頂板往下穿過每一層，右下角的小圖是各級熱負載對可用冷卻的百分比。',
       '預設是二十顆量子位元、同軸線共五十二條；把滑桿往右拉到兩百顆，細線束越來越密，冷板那條先變橘黃，接著是五十克耳文。',
       '停在兩百顆，同軸線變成五百零二條，冷板那條超過百分之一百、變成紅色，五十克耳文也用掉百分之七十五。',
       '再按讀取輸出，其他線淡掉，四克耳文那層的元件標著高電子遷移率放大器，說明寫著它耗電五到十毫瓦，這是主動熱。'],
      actions=[(1, 5.0, ('sweep', '量子位元數', 20, 200, 5.0)), (3, 0.5, ('click', '讀取輸出'))],
      points=[('二十顆', '各級都很寬鬆'), ('兩百顆', '冷板先超過'), ('低溫放大器', '耗電也是熱')], shot=(2, 3.0)),
 dict(key='ledger', pmap=[None, 0, 1, 2], after=6, page='pw', hash='heat', scene='1,000 位元供電互動動畫 場景 3：低溫熱預算',
      title='動畫展示：用冷卻硬撐', sub='互動動畫：低溫熱預算',
      sentences=[
       '換到供電互動動畫的低溫熱預算，左邊是冷凍機的五層冷盤，右邊七列橫條，白色虛線是可用冷卻的上限。',
       '預設一千位元、三組稀釋單元：五十克耳文那列是兩百零二瓦對一百五十八瓦，紅色，寫著超過百分之二十八。',
       '最底下的混合腔合計，兩百零六微瓦對九十微瓦，超過百分之一百二十九，面板上的熱帳寫著不過關。',
       '把稀釋單元慢慢加到七組，紅條一條條退到虛線左邊，熱帳過關，可是壓縮機電力從三十七點五千瓦變成八十七點五千瓦。'],
      actions=[(3, 1.0, _pw_sweep(_DU, 3, 7, 3.0))],
      points=[('三組', '五十克耳文超標'), ('混合腔', '超過一倍多，不過關'), ('加到七組', '過關，壓縮機八十七點五千瓦')], shot=(3, 7.0)),
 dict(key='wires', pmap=[0, 0, 1, 2], after=10, page='pw', hash='heat', scene='1,000 位元供電互動動畫 場景 3：低溫熱預算',
      title='動畫展示：換線，比加冷卻省', sub='互動動畫：低溫熱預算',
      sentences=[
       '回到熱預算動畫，一樣一千位元、三組，勾選改用細同軸，五十克耳文那列掉到五十四點五瓦，只用了百分之三十五。',
       '可是混合腔磁通直流那列跳到五百微瓦，超過百分之四百五十六，熱帳還是不過關。',
       '再勾選磁通線改用超導，磁通直流歸零，混合腔合計只剩十八點六微瓦，三組就過關了。',
       '最後把稀釋單元減到兩組，熱帳仍然過關，壓縮機電力只要二十五千瓦，比硬撐的七組少了六十二點五千瓦。'],
      actions=[(0, 3.6, _pw_tog('細同軸', True)), (2, 0.6, _pw_tog('超導 NbTi', True)), (3, 1.8, _pw_sl(_DU, 2))],
      points=[('細同軸', '上層變輕、直流熱翻四倍'), ('超導磁通線', '混合腔過關'), ('兩組就夠', '壓縮機二十五千瓦')], shot=(3, 4.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

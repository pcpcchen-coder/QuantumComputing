"""Q141 從 1,000 到 10,000：MW 級與低溫電源轉換 — v2 動畫展示段（格式見 ../demos.py 的說明）。

power1000.html（pw）是 SVG 頁面，控制項是 .ctl 滑桿與 label.tog 勾選框，所以用 ('js', ...) 操作；
_pw_sl／_pw_sweep 照抄 q139.py，_pw_card 照抄 q138.py（點 #svg 裡含指定文字的 g.pp；devplan 的項目卡也是 g.pp，
click 事件設 st.sel = p.n，見 power1000.html 開發計畫 build()）。

與 q131–q139 不重複的操作：
  - scale：Q134 只把 N 設 100／10,000 看「交流入口」「地線電流」；Q139 拖 N、在 N = 1,000 動「每位元室溫控制電子功耗」、切「架構」。
    本課直接把 N 設成 10,000（不拖），改看設施總功率與面板的壓縮機／控制電子，並在 10,000 位元下把每位元功耗 50 → 10 W。
  - devplan：q131–q139 都沒用過。本課點 ⑧ ⑨ ⑩，最後把「時間」滑桿拉到第 36 個月。
  - heat 場景的「低溫 CMOS＋多工」勾選不用（Q140 是熱預算主場，避免重疊）。

三段，依插入位置排列：
  mw      after=5（「從千瓦到百萬瓦」之後）      pw#scale    N 設 4（10,000）→ 每位元功耗 50 → 10 W
  conv8   after=7（「低溫電源轉換的設計理念」之後） pw#devplan  點 ⑧ 4 K 低溫電源轉換
  stage3  after=10（「換你改造」之後）           pw#devplan  點 ⑨ → 點 ⑩ → 「時間」0 → 36

畫面依據（animations/power1000.html，2026-11-18 版本；依指示錄影進行中不開瀏覽器，數字是把 render() 公式照抄成 node 腳本算出）：

mw（S({ id: 'scale' …})，約第 251–297 行；預設 N = 1,000、W = 50、架構 rt）
  N = 10,000：L = lines(10000)：C = 15,000、fl = 1,250、total = 38,750、dc = 28,750 → dcUnits = 1,198；fridges = 10；pts = 39；
    comp = 487.5；elec = 500；dec = 250；hv = 0.4(500 + 53.91 + 250) = 321.56；kw = 487.5 + 292.5 + 40 + 500 + 53.91 + 3 + 250 + 321.56 = 1948.47。
  句 0（58 字，約 12.9 秒）：6.0 秒（「直接把位元數設成一萬」約第 22–31 字，4.9–6.9 秒）設「量子位元數」= 4 →
       頂端大字「N = 10,000 位元　·　耦合器 15,000　·　讀取饋線 1,250」。
  句 1（41 字，約 9.1 秒）：最下列「設施總功率」1948 kW（紅 #ff5a5f，frac 6.1 > 1），小字 note（kw > 1000）「MW 級量子資料中心」。
  句 2（51 字，約 11.3 秒）：面板 metrics「壓縮機 487.5 kW」「控制電子 500.0 kW」；8.5 秒起 2.0 秒內「每位元室溫控制電子功耗」50 → 10 W
       （「拉到文件的下限十瓦」約第 42–50 字，9.3–11.1 秒）。文件 §4.1：每位元 10–100 W。
  句 3（48 字，約 10.7 秒）：W = 10：elec = 100 →「控制電子 100.0 kW」；hv = 161.56；kw = 1388.47 → 設施「1388 kW」仍紅、note 仍「MW 級量子資料中心」；
       「壓縮機 487.5 kW」與「39 支／487.5 kW 壓縮機」不變（comp 只由 pts 決定，與 W 無關）。
conv8（S({ id: 'devplan' …})，約第 565–632 行；預設 st.sel = 2、month = 0、auto 關）
  句 0（54 字，約 12.0 秒）：左側三個階段標題「0–1 年／1–3 年／3–7 年」，11 張卡（①–⑪）。month = 0 時 start = [0, 12, 36]，
       第二、三階段卡片 opacity 0.4；第三階段（y0 = 500，左下，紫 #9d8cff）為 ⑧⑨⑩⑪。
  句 1（56 字，約 12.4 秒）：1.0 秒點 ⑧（_pw_card('4 K 低溫電源轉換')）→ 右側 detail「⑧ 4 K 低溫電源轉換」，
       「要做出什麼：在冷凍機 4 K 層工作的 DC-DC：高壓低電流送入、低溫端降壓，供電給低溫控制晶片」。
  句 2（47 字，約 10.4 秒）：detail「第一步：和學研合作量元件的低溫特性」「完成判準：小功率原型在 4 K 恆溫器中展示」。
  句 3（51 字，約 11.3 秒）：FEEDS[8] = [9, 10] → ⑨、⑩ 外框 #e0a54a、寬 3.5（金色）；needs = []（沒有任何 FEEDS 值含 8）→
       detail「■ 需要先有：（無）」「■ 成果提供給：⑨ 高通道數直流供電、⑩ 模組化量子資料中心配電」。
stage3（同場景，重新載入，month = 0）
  句 0（54 字，約 12.0 秒）：1.0 秒點 ⑨ → 「要做出什麼：數千到上萬路精密直流背後的電源分配：多軌、低雜訊、彼此隔離、高密度」。
  句 1（57 字，約 12.7 秒）：⑨ 的 needs = FEEDS 中含 9 的鍵 = ③⑤⑥⑧ → 綠框 #3ccf8e；困難表第 4 列「架構可能被低溫化取代 ｜ 保留送進冷凍機的介面，與 ⑧ 共用技術」。
  句 2（53 字，約 11.8 秒）：1.0 秒點 ⑩ → 「要做出什麼：把 ① 做成可複製的「量子單元」模組，並排擴充到 MW 等級」。needs = ①②④⑧（綠框）。
  句 3（54 字，約 12.0 秒）：1.5 秒起 2.5 秒內「時間」0 → 36：month ≥ 12 第二階段亮（opacity 1），= 36 第三階段亮；metrics「目前 第三階段」
       「已啟動項目 11 / 11」「下一個檢查點 —」，下方「第 36 個月檢查點：OEM 有設計導入嗎？低溫 CMOS 與模組化冷凍機進度如何？」
       （旁白只念後半句）。拖動途中依序閃過第 6、12、18 個月檢查點文字。

試拍需確認：(1) mw 句 0 設 N = 4 後橫條與頂端文字是否立即更新（tick 依 st.dirty 重畫）；(2) mw 面板 metrics「壓縮機」「控制電子」
在 1600×900 畫面內是否可見；(3) conv8 month = 0 時第三階段卡片 opacity 0.4，⑧ 的白框與 ⑨⑩ 的金框是否看得清楚；
(4) devplan 卡片 click（MouseEvent bubbles）是否觸發 g 上的 click listener、detail 是否更新；(5) stage3 _pw_sweep 對 step = 1 的「時間」滑桿
（小數值會被瀏覽器取整）是否順暢、metrics 最後停在第 36 個月檢查點；(6) detail 的 foreignObject 文字在錄影解析度下是否可讀。
"""
import json

LESSON = 'Q141'


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


def _pw_card(text):  # 點 #svg 裡含指定文字的 g.pp（devplan 的項目卡；click 會設 st.sel）
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.includes(%s));"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));})()" % json.dumps(text))


_N = '量子位元數'
_W = '每位元室溫控制電子功耗'

_LIST = [
 dict(key='mw', pmap=[0, 0, 1, 2], after=5, page='pw', hash='scale', scene='1,000 位元供電互動動畫 場景 2：規模計算器',
      title='動畫展示：一萬位元的電費單', sub='互動動畫：規模計算器',
      sentences=[
       '打開供電互動動畫的規模計算器，這次不慢慢拖，直接把位元數設成一萬，最上面寫著耦合器一萬五千、讀取饋線一千兩百五十。',
       '最下面那列設施總功率是一千九百四十八千瓦，紅色，旁邊小字寫著百萬瓦級量子資料中心。',
       '右邊面板上，壓縮機四百八十七點五千瓦，控制電子五百千瓦；接著把每位元控制電子功耗，拉到文件的下限十瓦。',
       '控制電子降成一百千瓦，設施總功率還有一千三百八十八千瓦，依然是百萬瓦級；壓縮機那一格一點都沒變。'],
      actions=[(0, 6.0, _pw_sl(_N, 4)), (2, 8.5, _pw_sweep(_W, 50, 10, 2.0))],
      points=[('一萬位元', '設施約 1,948 kW'), ('每位元 50 → 10 W', '仍約 1,388 kW'), ('壓縮機', '487.5 kW 不動')], shot=(1, 4.0)),
 dict(key='conv8', after=7, page='pw', hash='devplan', scene='1,000 位元供電互動動畫 場景 8：開發計畫',
      title='動畫展示：第八項，四克耳文電源', sub='互動動畫：開發計畫（規劃建議）',
      sentences=[
       '換到供電互動動畫的開發計畫，十一個項目分成三個階段；時間滑桿停在啟動，所以左下第三階段的紫色卡片還是暗的。',
       '點下第八項四克耳文低溫電源轉換，右邊寫著要做出什麼：在冷凍機四克耳文層工作的直流轉換器，供電給低溫控制晶片。',
       '下面的第一步寫著和學研合作，量元件的低溫特性；完成判準是小功率原型，在四克耳文恆溫器中展示。',
       '左邊第九和第十項亮起金色外框，代表它們靠第八項提供成果；說明裡需要先有那一欄寫著無，第八項不必先等別的項目。'],
      actions=[(1, 1.0, _pw_card('4 K 低溫電源轉換'))],
      points=[('第三階段', '三到七年，下一代架構'), ('第八項', '四克耳文直流轉換'), ('金色外框', '第九、第十項靠它')], shot=(3, 3.0)),
 dict(key='stage3', pmap=[0, 0, 1, 2], after=10, page='pw', hash='devplan', scene='1,000 位元供電互動動畫 場景 8：開發計畫',
      title='動畫展示：從第八項到百萬瓦', sub='互動動畫：開發計畫（規劃建議）',
      sentences=[
       '再點第九項高通道數直流供電，要做的是數千到上萬路精密直流背後的電源分配：多軌、低雜訊、彼此隔離、高密度。',
       '綠色外框是它需要先有的項目，第八項也在裡面；困難表最後一列寫著，這套架構可能被低溫化取代，所以和第八項共用技術。',
       '接著點第十項模組化量子資料中心配電，目標是把第一項的參考設計做成可複製的量子單元，並排擴充到百萬瓦等級。',
       '最後把時間拉到第三十六個月，三個階段全部亮起，面板下方的檢查點問：低溫控制晶片與模組化冷凍機的進度如何？'],
      actions=[(0, 1.0, _pw_card('高通道數直流供電')), (2, 1.0, _pw_card('模組化量子資料中心配電')),
               (3, 1.5, _pw_sweep('時間', 0, 36, 2.5))],
      points=[('第九項', '和第八項共用技術'), ('第十項', '並排擴充到 MW 級'), ('第三十六個月', '檢查低溫 CMOS 進度')], shot=(3, 8.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

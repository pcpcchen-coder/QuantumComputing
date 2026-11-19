"""Q144 畢業專題：替一台量子電腦寫供電規格書 — v2 動畫展示段（格式見 ../demos.py 的說明）。

power1000.html（pw）是 SVG 頁面，控制項是 label.tog 勾選框，紅色痛點與開發計畫卡片都是 #svg 裡的 g.pp，所以用 ('js', ...) 操作；
_pw_tog、_pw_pp 照抄 q131.py，_pw_card 照抄 q143.py。

本課是畢業綜整：用課綱指定的全景（overview）把規格書五章各對到一個痛點，最後在開發計畫看「缺口變機會」的寫法。
與 q131–q143 不重複的操作：
  - overview：q131 勾「模擬斷電」、取消「冷卻鏈接 UPS＋發電機」、點痛點 1；q132 點痛點 4、勾「模擬斷電」、取消「控制與量測接 UPS」；
    q142 點痛點 7。本課點痛點 2、3、5、6（前面沒點過），並取消「運算接 UPS」（前面沒用過）。
    唯一重複的是「模擬斷電」勾選本身——不勾它，取消「運算接 UPS」在畫面上沒有任何效果（tick：comp = !out || st.ups.comp）。
  - devplan：q141 點 ⑧⑨⑩；q142 點 ④⑦；q143 預設 ②、自動導覽到 ③、點 ③、點 ⑥。本課只點 ①（前面沒點過）。
    （q138 在 roadmap 點的是「A＋B 分層 UPS＋精密空調參考設計」卡，會跳到 #outage，和 devplan 的 ① 卡是不同場景、不同行為。）
  - 面板最下面的三行全景數字（設施總功率、冷卻鏈、UPS 容量）前面各課旁白沒有念過。

三段，依插入位置排列：
  power   after=6（「第一、二章：用電與備援」之後）  pw#overview  讀三行數字 → 點痛點 2 → 模擬斷電＋取消運算接 UPS
  risks   after=8（「第五章：熱預算」之後）          pw#overview  點痛點 3（接地）→ 痛點 6（磁場）→ 痛點 5（熱預算）
  gaps    after=10（「換你改造：第六章 文獻缺口」之後）pw#devplan   點 ① → 困難表第一、二列 → 綠框 ②④

畫面依據（animations/power1000.html，2026-11-19 讀到的版本；依指示錄影進行中不開瀏覽器、不試錄，全部逐行讀原始碼；
秒數以每秒 4.5 字估（PLAYBOOK），已製作各課實測約每秒 4.7–5.5 字，所以「說到時」的字位也用 5.4 字每秒檢查下限）：

record_demo 每段重新 goto 並等 settle，所以每段開始時都是場景預設值：
overview build()：st.outage = false；ups = {cool, ctrl, comp} 全 true；st.sel = null → renderPP() 只有三列 metrics：
「設施總功率（中點）｜約 200 kW」「冷卻鏈（要撐過斷電）｜約 80 kW」「UPS 容量｜80–270 kW」（#metrics 在左側 #panel 內，
desc 三段與四個勾選框之下）。點痛點 n → st.sel = n → 三列之後加「痛點 n｜標題」（紅字 bad）與一整列說明文字。
devplan build()：st.sel = 2、month = 0、auto = false。

power（pw#overview）
  句 0（61 字，約 13.6 秒）：無動作。念 metrics 三列（「面板下方」：#metrics 在勾選框之下、.hint 之上）：約 200 kW、約 80 kW、80–270 kW。
  句 1（54 字，約 12.0 秒）：0.3 秒 _pw_pp(2)（「點二號紅點」第 1–5 字）→ PP[1] = [550, 110, 2, '壓縮機：最大的單一負載',
       '每支脈衝管 ≈ 12.5 kW 壓縮機。熱預算不夠 → 多加脈衝管 → 多加電與冷卻水；還要 N+1。']；紅點在「機電匯流排」框
       （450,120,200×90）上緣。metrics 多兩列「痛點 2｜壓縮機：最大的單一負載」與說明。
  句 2（50 字，約 11.1 秒）：0.3 秒 _pw_tog('模擬斷電', True)（「勾選模擬斷電」第 1–6 字）→ st.outage = true；
       1.8 秒 _pw_tog('運算接 UPS', False)（「再取消運算接不斷電系統」第 7–17 字 ≈ 1.3–3.8 秒）→ st.ups.comp = false →
       tick：f.comp、f.dec、f.hvac 的 Flow.on = false，不再產生新粒子，已在路上的跑完消失（路徑 stroke-opacity .25 仍在）。
       運算匯流排框在 (450,540)，標「運算匯流排／約 30 kW」；負載「即時解碼 5–50 kW」(730,540)、「電子區空調 5–50 kW」(730,620)；
       這三條 Flow 的顏色都是 '#9d8cff'（紫）。f.grid 也停（進線）。旁白只說紫色那條停了、解碼和空調不再有粒子。
  句 3（61 字，約 13.6 秒）：無動作。cool、ctrl 仍 true → f.mech/comp1/chill/ghs/tofr1（橘 '#ff8a5c'）與
       f.clean/elec/dc/clk/tofr2（青 '#38c6d9'）繼續產生粒子；out && !cool 為假 → st.temp 維持 0.01 → 「MXC 10 mK」綠字。
       機電（y 120）、乾淨（y 330）兩框都在運算（y 540）之上 →「上面兩條」。
       後半句「解碼只能容忍秒級中斷、要接雙轉換式不斷電系統」是設計文件 §4.2 表格「運算｜秒級｜雙轉換 UPS」，明說是文件，不是畫面。
risks（pw#overview，重新載入：三列 metrics、無選取）
  句 0（56 字，約 12.4 秒）：1.4 秒 _pw_pp(3)（「點」在第 8 字 ≈ 1.5–1.8 秒）→ PP[2] = [550, 320, 3, '數百個交流入口的接地',
       '約 250–350 台設備，每台 0.5–1 mA 漏電流 → 地線 0.1–0.35 A → 數百 µV 到 mV 的地電位，偏壓要求是 µV。']；
       紅點在「乾淨匯流排」框（450,330）上緣。說明裡有三個「→」，旁白說「用箭頭串起來」。
  句 1（62 字，約 13.8 秒）：0.3 秒 _pw_pp(6)（句首「再點六號紅點」）→ PP[5] = [410, 470, 6, '配電磁場',
       '250 kW、400 V 約 360 A；母線與變壓器要遠離冷凍機並成對配線（LRZ 要求交流 ≪ 1 µT）。']；
       (410,470) 在 F('M370,380 C410,380 410,585 450,585')（UPS → 運算匯流排的紫色配電線）的轉彎處。
  句 2（50 字，約 11.1 秒）：0.3 秒 _pw_pp(5)（「最後點冷凍機身上的五號紅點」第 1–12 字）→ PP[4] = [1080, 330, 5, '低溫熱預算',
       '不改架構時 50 K 約 200 W、4 K 約 4.4 W、MXC 被動＋直流約 200 µW，都超過或逼近 3 個單元的容量。']；
       (1080,330) 在冷凍機框（1000,90,160×520）內 4 K（y 300）與 Still（y 380）兩條線之間。
gaps（pw#devplan，重新載入：sel = 2）
  句 0（53 字，約 11.8 秒）：1.4 秒 _pw_card('分層 UPS＋空調參考設計')（「點第一項」第 7–10 字 ≈ 1.3–2.2 秒）→ st.sel = 1、
       st.auto = false → render()：右側 detail「0–1 年 · 矩陣 A＋B」「① 分層 UPS＋空調參考設計」，下方困難表兩欄標題
       「困難｜可能的解法」，四列（PLAN[0].d 共 4 組）。① 卡（30,62）白框。
  句 1（52 字，約 11.6 秒）：無動作。困難表第一列「拿不到真實負載數據（規格書在 NDA 後）｜用免費的電力品質與啟動暫態量測換數據」。
  句 2（49 字，約 10.9 秒）：無動作。第二列「冷卻容忍時間只有一個公開數據點｜設計方法把容忍時間當輸入參數，示範場域實測」。
  句 3（43 字，約 9.6 秒）：無動作。needs(1) = FEEDS 值含 1 的鍵 = ②（[1,10,11]）、④（[1,10]）→ ② ④ 綠框 #3ccf8e 寬 3.5；
       detail 底部「■ 需要先有：② 現場勘查服務、④ 壓縮機變頻驅動」。feeds(1) = ⑩ 金框（旁白不提）。

觀察重點卡（pmap）：
  power [0, 1, 2, 2]     句 0 三個數字（場景載入即有）／句 1 痛點 2（0.3 秒點擊）／句 2–3 運算不接 UPS（句 2 的 1.8 秒取消）
  risks [0, 1, 2]        三句各點一個痛點，點擊都在句首 0.3–1.4 秒，旁白說到內容前畫面已出現
  gaps  [None, 0, 1, 2]  句 0 只點開 ①、介紹困難表，不亮卡；句 1、2 各對一列；句 3 綠框

試拍需確認：(1) power／risks：點痛點後 #metrics 多兩列加一段說明，在 1600×900 下左側 #panel 是否不必捲動就看得到
（desc 三段＋四個勾選框之下）；(2) power 句 2：勾「模擬斷電」與取消「運算接 UPS」相隔 1.5 秒，__flash 兩次是否清楚，
紫色粒子在句 2 內是否已跑完消失（Flow 速度 140 px／秒，最長的 comp 路徑約 260 px，約 2 秒）；(3) risks 句 0：
1.4 秒點擊若實測語速較快（每秒 5.5 字），「點」在 1.3 秒，點擊略晚 0.1 秒，可接受；(4) gaps：devplan 右側 foreignObject
困難表在錄影解析度下第一、二列是否可讀；_pw_card 的 includes('分層 UPS＋空調參考設計') 只會對到 ① 卡（devplan 裡只有卡片是 g.pp）；
(5) 三段的 shot 截圖是否落在效果出現之後。
"""
import json

LESSON = 'Q144'


def _pw_tog(label, on):
    return ('js', "(()=>{const l=[...document.querySelectorAll('#controls label.tog')].find(x=>x.textContent.includes(%s));"
                  "const i=l.querySelector('input');window.__flash(l);if(i.checked!==%s){i.checked=%s;i.dispatchEvent(new Event('change'));}})()"
            % (json.dumps(label), 'true' if on else 'false', 'true' if on else 'false'))


def _pw_pp(n):  # 點全景場景的紅色痛點 n
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.trim()===%s);"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));window.__flash(document.getElementById('metrics'));})()" % json.dumps(str(n)))


def _pw_card(text):  # 點 #svg 裡含指定文字的 g.pp（devplan 卡片會設 st.sel）
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.includes(%s));"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));})()" % json.dumps(text))


_LIST = [
 dict(key='power', pmap=[0, 1, 2, 2], after=6, page='pw', hash='overview', scene='1,000 位元供電互動動畫 場景 1：全景',
      title='動畫展示：用電與備援章的數字', sub='互動動畫：電從哪裡來、到哪裡去',
      sentences=[
       '打開供電互動動畫的全景，左邊面板下方有三行數字：設施總功率中點約兩百千瓦，冷卻鏈約八十千瓦，不斷電系統八十到兩百七十千瓦。',
       '點二號紅點，面板寫著壓縮機是最大的單一負載，每支脈衝管約十二點五千瓦，熱預算不夠就多加脈衝管，還要多備一台。',
       '勾選模擬斷電，再取消運算接不斷電系統，下方紫色的運算匯流排停了，即時解碼和電子區空調不再有粒子流過。',
       '上面兩條匯流排照樣在流，混合腔還是十毫克耳文；可是文件寫著解碼只能容忍秒級中斷，所以備援章要讓運算也接雙轉換式不斷電系統。'],
      actions=[(1, 0.3, _pw_pp(2)), (2, 0.3, _pw_tog('模擬斷電', True)), (2, 1.8, _pw_tog('運算接 UPS', False))],
      points=[('三個數字', '200 kW・80 kW・80–270 kW'), ('痛點 2', '壓縮機 12.5 kW，還要 N+1'), ('運算不接 UPS', '紫色匯流排停下')],
      shot=(3, 3.0)),
 dict(key='risks', pmap=[0, 1, 2], after=8, page='pw', hash='overview', scene='1,000 位元供電互動動畫 場景 1：全景',
      title='動畫展示：三章各對一個痛點', sub='互動動畫：電從哪裡來、到哪裡去',
      sentences=[
       '再開一次全景，點乾淨匯流排上的三號紅點，說明用箭頭把接地章串起來：設備台數、每台漏電流、地線電流，最後是地電位。',
       '再點六號紅點，它在通往運算匯流排的配電線上，說明寫著母線和變壓器要遠離冷凍機、成對配線，括號裡是交流磁場要遠小於一微特斯拉。',
       '最後點冷凍機身上的五號紅點看熱預算章：五十克耳文、四克耳文和混合腔，三層都超過或逼近三個單元的容量。'],
      actions=[(0, 1.4, _pw_pp(3)), (1, 0.3, _pw_pp(6)), (2, 0.3, _pw_pp(5))],
      points=[('痛點 3 接地', '地線 0.1–0.35 A'), ('痛點 6 配電磁場', '遠離冷凍機、成對配線'), ('痛點 5 熱預算', '三層都超過或逼近')],
      shot=(2, 3.0)),
 dict(key='gaps', pmap=[None, 0, 1, 2], after=10, page='pw', hash='devplan', scene='1,000 位元供電互動動畫 場景 8：開發計畫',
      title='動畫展示：把缺口寫成機會', sub='互動動畫：開發計畫（規劃建議）',
      sentences=[
       '最後換到開發計畫，點第一項分層不斷電加空調參考設計，右邊的困難表列出四個困難，每一個旁邊都配了可能的解法。',
       '第一列寫著拿不到真實負載數據，因為規格書在保密協定後面；解法是用免費的電力品質和啟動暫態量測，去換數據。',
       '第二列就是第六章的缺口：冷卻容忍時間只有一個公開數據點，解法是把它當成輸入參數，再到示範場域實測。',
       '左邊第二和第四項亮起綠框，代表要先有它們：現場勘查的實測數據，和壓縮機變頻驅動的群控。'],
      actions=[(0, 1.4, _pw_card('分層 UPS＋空調參考設計'))],
      points=[('困難一', '拿不到真實負載數據'), ('困難二', '容忍時間只有一個數據點'), ('綠框 ②④', '先有勘查與群控')],
      shot=(2, 3.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

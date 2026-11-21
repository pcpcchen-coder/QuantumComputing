"""Q143 三階段路線圖與 11 個開發項目 — v2 動畫展示段（格式見 ../demos.py 的說明）。

power1000.html（pw）是 SVG 頁面，控制項是 .ctl 滑桿與 label.tog 勾選框，所以用 ('js', ...) 操作；
_pw_tog 照抄 q131.py，_pw_sweep 照抄 q141.py（原出 q139.py），_pw_card 照抄 q141.py（點 #svg 裡含指定文字的 g.pp；
roadmap 卡片 click → App.go(對應痛點場景)；devplan 卡片 click → st.sel = p.n、st.auto = false、取消勾選）。

與 q131–q141 不重複的操作：
  - roadmap：Q138 讀三欄、點「A＋B 分層 UPS＋精密空調參考設計」跳 #outage。本課改讀面板的「先建立的能力 1–3」、卡片底下的
    「→ 看痛點：…」小字，點第一欄第二張「H 現場勘查」跳 #field。
  - devplan：Q141 點 ⑧ ⑨ ⑩、「時間」0 → 36；Q142 用 ④ ⑦（矩陣標籤、綠框／金框）。本課只用 ② ③ ⑥（預設 ②、自動導覽 ② → ③、
    點 ③、點 ⑥），「時間」只拉 0 → 6 → 12 → 18；不點 ④ ⑦（③ 的金框會亮在 ⑤⑥⑦⑨ 上，旁白只說「四個金框」）。
  - roadmap：Q142 點「解碼機櫃供電與液冷」跳全景再點痛點 7；本課點「現場勘查」跳磁場場景，不重複。
  - 「自動導覽（依建議啟動順序）」勾選框：q131–q141 都沒用過。

三段，依插入位置排列：
  roadmap   after=3（「三階段路線圖」之後）       pw#roadmap  面板三個能力 → 卡片小字 → 點「現場勘查」跳 #field
  autotour  after=6（「建議的啟動順序」之後）     pw#devplan  預設 ② → 勾自動導覽（6 秒後 ③）→ 點 ③ 停下
  checks    after=10（「換你改造：寫完成判準」之後） pw#devplan  點 ⑥ → 完成判準 → 「時間」0→6 → 6→12 → 12→18

畫面依據（animations/power1000.html，2026-11-19 版本；依指示錄影進行中不開瀏覽器、不試錄，全部逐行讀原始碼；
秒數：已製作的 q131–q134 實測約每秒 4.7–5.5 字（句首到下一句首，含 0.48 秒墊音），下面「字@秒」用 5.4／4.6 字每秒算區間）：

record_demo.js 先 goto、等 settle 4000 ms（pw 預設）才從 t = 0 開始，所以 roadmap 卡片淡入（delay = 欄×1.2＋列×0.25，
最後一張 3.15 秒起 0.5 秒內到 1）在句 0 前已全部出現；devplan 每段重新 goto，所以 st.sel = 2、month = 0、auto 關。

roadmap（S({ id: 'roadmap' …})，第 497–520 行）
  句 0（62 字）：metrics 三列「先建立的能力 1 ｜ QGP 規格與量測」「先建立的能力 2 ｜ 驗證平台」「先建立的能力 3 ｜ 夥伴生態」
       （#metrics 在左側 #panel 內、desc 與 controls 之下；roadmap 沒有控制項）。無動作。
  句 1（51 字）：每張卡第三行 txt「→ 看痛點：」＋ SCENES.find(go).title.split('：')[0]；第一欄（0–1 年）第二張 tag「H」、
       「現場勘查：磁場、接地電流、電力品質」、go = 'field' → 「→ 看痛點：磁場與配電佈局」。無動作。
  句 2（59 字）：0.8 秒 _pw_card('現場勘查')（「點下現場勘查那張卡」0.1–1.9 秒）→ App.go(field)：panel 標題
       「磁場與配電佈局：母線離冷凍機多遠？」。field build() 預設 I = 360 A、d = 3 m、mode = 'pair'、s = 0.1 m、ac = true：
       B = 2e-7 × 360 × 0.1 ／ 3² = 8.0e-7 T = 0.8 µT → 顯示「冷凍機位置磁場 ≈ 0.800 µT」；ac 時 ok = B < 0.1 → false → 紅字
       #ff5a5f，下一行「交流要求 ≪ 1 µT（此處以 0.1 µT 判斷）」，再下一行紅字「超過：拉開距離、成對配線、補償線圈或屏蔽」；
       母線標「母線（成對）」，距離標「3.0 m」。
autotour（S({ id: 'devplan' …})，第 565–632 行；PLAN、FEEDS、CHECKS 第 529–563 行）
  FEEDS = {2: [1,10,11], 3: [5,6,7,9], 1: [10], 4: [1,10], 5: [6,9], 6: [9], 8: [9,10]}；
  render()：選中卡白框 #ffffff 寬 4；needs（FEEDS 值含 p.n 的鍵）綠框 #3ccf8e；feeds（FEEDS[p.n]）金框 #e0a54a 寬 3.5。
  句 0（61 字）：st.sel = 2 → 右側 detail「0–1 年 · 矩陣 H」「② 現場勘查服務」「要做出什麼：標準化的量子機房勘查：磁場、接地電流、
       電力品質、振動、溫濕度、5–7 GHz 射頻；2–3 天完成」；左側 ② 卡白框。無動作。
  句 1（56 字）：feeds(2) = ①⑩⑪ 金框；needs(2) = []（沒有任何 FEEDS 值含 2）→ detail 最下「■ 需要先有：（無）」
       「■ 成果提供給：① 分層 UPS＋空調參考設計、⑩ 模組化量子資料中心配電、⑪ 解碼機櫃供電與液冷」。無動作。
  句 2（52 字）：0.1 秒 _pw_tog('自動導覽', True) → change → st.auto = true、st.t = 0；tick 累加 dt，st.t > 6 時
       st.sel = order[(order.indexOf(2) + 1)] = 3 → 約 6.1 秒白框跳到 ③。「看，白框跳到第三項」的「看」在第 34 字
       ≈ 6.4–7.5 秒，在跳之後。order = [2,3,1,6,5,4,7,11,8,9,10]。
  句 3（51 字）：0.2 秒 _pw_card('量子等級電源規格')（「點一下第三項的卡片」）→ st.sel = 3、st.auto = false、勾選框取消；
       ③ 白框、feeds(3) = ⑤⑥⑦⑨ 四個金框、needs(3) = [] →「需要先有：（無）」。
       時間餘裕：下一次自動換項（→ ①）在句 2 開始後 12.1 秒；句 2 長約 9.6–11.1 秒，所以點擊落在換項前 ≥ 0.8 秒。
       就算錄影掉幀使 6 秒計時變慢，點 ③ 也保證停在 ③（只可能讓句 2 的「看」早於跳動，見試拍清單）。
checks（同場景，重新載入：sel = 2、month = 0）
  句 0（53 字）：2.0 秒 _pw_card('集中供電＋監測')（「點第二」第 9 字 ≈ 1.8–2.1 秒）→ detail「1–3 年 · 矩陣 A／D」
       「⑥ 集中供電＋監測 PDU」「第一步：PDU 先做（不需儀器廠配合）」；month = 0 < 12，所以 ⑥ 卡 opacity 0.4（偏暗，仍可點）。
  句 1（49 字）：detail「完成判準：抓到一次「接地電流變化 ↔ 量測異常」的時間對應」；needs(6) = FEEDS 值含 6 的鍵 = ③⑤ → 綠框；
       feeds(6) = ⑨ 金框（旁白不提）。無動作。
  句 2（46 字）：2.2 秒起 0.6 秒 _pw_sweep('時間', 0, 6)（「拉到第六」第 12 字 ≈ 2.4–2.8 秒）→ 滑桿值「第 6 個月」；metrics
       「目前 第一階段」「已啟動項目 3 / 11」（只有 st = 0 的 ①②③）「下一個檢查點 第 12 個月」，下方
       「第 6 個月檢查點：取得場地規劃文件了嗎？QGP 量測台量得出產品差異嗎？」。卡片亮度不變（第二階段 12 個月才啟動）。
  句 3（66 字）：0.3 秒起 0.8 秒 _pw_sweep('時間', 6, 12) → month = 12：start[1] = 12，④⑤⑥⑦ opacity 1（⑥ 仍是白框）；
       「目前 第二階段」「已啟動項目 7 / 11」；4.3 秒起 0.8 秒 _pw_sweep('時間', 12, 18)（「再拉到」第 22 字 ≈ 4.2–4.9 秒）→
       「第 18 個月檢查點：有儀器廠或冷凍機廠願意共同開發嗎？」「下一個檢查點 第 36 個月」（旁白不念 36）。
       ⑥ 的第一步「PDU 先做（不需儀器廠配合）」仍在 detail 上 →「第六項的第一步不必等他們」。

觀察重點卡（pmap）：
  roadmap  [0, 1, 2]       句 0 能力（面板已在）／句 1 卡片小字（已在）／句 2 點卡（0.8 秒跳頁）
  autotour [0, 1, None, 2] 句 2 開頭 ③ 還沒出現，不亮卡；句 3 點 ③、四個金框才亮「第三項」卡
  checks   [0, 1, 2, 2]    句 0 第六項第一步（2.0 秒點擊，旁白念到第一步時已出現）／句 1 判準／句 2–3 時間機器

試拍需確認：(1) autotour 句 2：錄影（swiftshader、1600×900）下 rAF 是否 ≥ 20 fps——dt 上限 0.05 秒，掉幀會讓 6 秒計時變慢，
③ 可能晚於「看」才跳；(2) autotour 句 3 點擊時是否還沒自動跳到 ①（句 2 實際長度若超過約 11.9 秒就會先跳）；
(3) roadmap 句 0：#metrics 的三列在 #panel 內是否不必捲動就看得到；(4) roadmap 句 2：App.go(field) 後 hash 以 replaceState 改成
#field，磁場熱圖、紅字是否完整畫出；(5) checks 句 0：⑥ 卡在 opacity 0.4 時白框、③⑤ 綠框是否夠明顯；(6) checks 句 2–3：_pw_sweep 對 step = 1
的「時間」滑桿取整是否順暢、metrics 與檢查點文字是否即時更新；(7) devplan 右側 foreignObject（x 560–1180）說明文字與困難表在錄影
解析度下是否可讀，以及 detail 底部「需要先有／成果提供給」兩行是否在 720 高的框內不必捲動。
"""
import json

LESSON = 'Q143'


def _pw_tog(label, on):
    return ('js', "(()=>{const l=[...document.querySelectorAll('#controls label.tog')].find(x=>x.textContent.includes(%s));"
                  "const i=l.querySelector('input');window.__flash(l);if(i.checked!==%s){i.checked=%s;i.dispatchEvent(new Event('change'));}})()"
            % (json.dumps(label), 'true' if on else 'false', 'true' if on else 'false'))


def _pw_sweep(label, a, b, secs):  # 在頁面內用 setInterval 逐步改滑桿值（每秒 12 步），每步送出 'input'；拖動期間滑桿加黃框
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const i=d.querySelector('input');const a=%r,b=%r,n=Math.max(2,Math.round(%r*12));let k=0;d.classList.add('qflash');"
                  "const h=setInterval(()=>{k++;i.value=String(a+(b-a)*k/n);i.dispatchEvent(new Event('input'));"
                  "if(k>=n){clearInterval(h);i.value=String(b);i.dispatchEvent(new Event('input'));setTimeout(()=>d.classList.remove('qflash'),300);}},%d);})()"
            % (json.dumps(label), a, b, secs, round(secs * 1000 / max(2, round(secs * 12)))))


def _pw_card(text):  # 點 #svg 裡含指定文字的 g.pp（roadmap 卡片會換場景；devplan 卡片會設 st.sel）
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.includes(%s));"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));})()" % json.dumps(text))


_LIST = [
 dict(key='roadmap', pmap=[0, 1, 2], after=3, page='pw', hash='roadmap', scene='1,000 位元供電互動動畫 場景 7：三階段路線圖',
      title='動畫展示：卡片背後的痛點', sub='互動動畫：三階段路線圖（規劃建議）',
      sentences=[
       '打開供電互動動畫的路線圖場景，這次先看左邊面板下方，列著三個要先建立的能力：量子等級電源規格與量測、驗證平台，還有夥伴生態。',
       '每張卡片底下都有一行小字，指向它要解決的痛點，例如第一欄第二張的現場勘查，寫著看痛點：磁場與配電佈局。',
       '點下現場勘查那張卡，畫面直接跳到磁場場景：預設成對母線離冷凍機三公尺，冷凍機位置的磁場約零點八微特斯拉，紅字寫著超過。'],
      actions=[(2, 0.8, _pw_card('現場勘查'))],
      points=[('三個先建立的能力', 'QGP・驗證平台・夥伴生態'), ('卡片小字', '→ 看痛點：磁場與配電佈局'), ('點現場勘查', '冷凍機處 0.8 µT，超過')],
      shot=(1, 3.0)),
 dict(key='autotour', pmap=[0, 1, None, 2], after=6, page='pw', hash='devplan', scene='1,000 位元供電互動動畫 場景 8：開發計畫',
      title='動畫展示：誰先開工？', sub='互動動畫：開發計畫（規劃建議）',
      sentences=[
       '換到開發計畫場景，右邊說明預設打開第二項現場勘查服務：一套標準化的量子機房勘查，量磁場、接地電流和電力品質，兩到三天完成。',
       '左邊第一、第十、第十一項亮起金框，代表勘查的成果要提供給它們；說明最下面的需要先有寫著無，所以它可以第一個開工。',
       '勾選自動導覽，畫面就會照著建議的啟動順序，每隔六秒自動換到下一個項目；看，白框跳到第三項量子等級電源規格。',
       '點一下第三項的卡片，導覽就停在這裡；它一口氣亮了四個金框，因為之後的電源產品，都要拿它的量測台來驗證。'],
      actions=[(2, 0.1, _pw_tog('自動導覽', True)), (3, 0.2, _pw_card('量子等級電源規格'))],
      points=[('第二項 現場勘查', '需要先有：無'), ('金框', '成果提供給 ①⑩⑪'), ('第三項 QGP', '四個金框靠它驗證')],
      shot=(3, 3.0)),
 dict(key='checks', pmap=[0, 1, 2, 2], after=10, page='pw', hash='devplan', scene='1,000 位元供電互動動畫 場景 8：開發計畫',
      title='動畫展示：判準與時間機器', sub='互動動畫：開發計畫（規劃建議）',
      sentences=[
       '再開一次開發計畫，點第二階段的第六項集中供電加監測配電單元，第一步寫著先做配電單元，因為不需要儀器廠配合。',
       '它的完成判準很具體：抓到一次接地電流變化和量測異常的時間對應；綠框是第三和第五項，代表要先有它們。',
       '打開時間機器，把時間滑桿拉到第六個月，面板寫著已啟動三項，檢查點問的是場地規劃文件和量測台。',
       '拉到第十二個月，第二階段連同第六項一起亮起；再拉到第十八個月，檢查點問：有儀器廠或冷凍機廠願意共同開發嗎？第六項的第一步不必等他們。'],
      actions=[(0, 2.0, _pw_card('集中供電＋監測')), (2, 2.2, _pw_sweep('時間', 0, 6, 0.6)),
               (3, 0.3, _pw_sweep('時間', 6, 12, 0.8)), (3, 4.3, _pw_sweep('時間', 12, 18, 0.8))],
      points=[('第六項 PDU 先做', '不需儀器廠配合'), ('完成判準', '接地電流 ↔ 量測異常'), ('時間機器', '6 → 12 → 18 個月')],
      shot=(3, 9.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

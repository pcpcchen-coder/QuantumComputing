"""Q142 我們的切入點：產品 × 平台矩陣 — v2 動畫展示段（格式見 ../demos.py 的說明）。

power1000.html（pw）是 SVG 頁面，所以用 ('js', ...) 操作；_pw_card 照抄 q138.py／q141.py（點 #svg 裡含指定文字的 g.pp：
devplan 的項目卡 click 會設 st.sel = p.n；roadmap 的卡片 click 會 App.go 到對應的痛點場景），_pw_pp 照抄 q131.py（點全景的紅色痛點）。

與 q131–q141 不重複的操作：
  - devplan：Q141 點 ⑧ ⑨ ⑩ 並拖「時間」滑桿。本課只點 ⑦ 精密線圈電流源與 ④ 壓縮機變頻驅動，看右側第一行的「矩陣」代號與它服務的平台，不動時間滑桿。
  - roadmap：Q138 看三欄、念第一欄 A＋B 與第二欄 F、G，點 A＋B 卡跳到斷電時間軸。本課看「同一代號在不同階段再出現」（A、I），
    點第三欄 E「解碼機櫃供電與液冷」卡跳到全景，再點痛點 7（q131 點過痛點 1、q132 點過痛點 4，痛點 7 沒人點過）。

兩段，依插入位置排列（寧缺勿濫，只做兩段）：
  platform  after=5（「比一比：三平台通用 vs 單一平台」之後）  pw#devplan   點 ⑦ → 點 ④
  codes     after=7（「整合優先序」之後）                    pw#roadmap   點 E 卡（跳到 #overview）→ 點痛點 7

畫面依據（animations/power1000.html，2026-11-19 讀原始碼；依指示錄影進行中不開瀏覽器）：

platform（S({ id: 'devplan' …})，約第 565–632 行；build() 預設 st.sel = 2、month = 0、auto 關）
  句 0（55 字，約 12.2 秒，pmap None）：右側 detail 為 PLAN[1]：第一行小字「0–1 年 · 矩陣 H」，大字「② 現場勘查服務」。
  句 1（56 字，約 12.4 秒，卡 0）：0.8 秒點 ⑦（_pw_card('精密線圈電流源')；「第七項」約第 6–8 字，1.3 秒）→ render()：
       detail 第一行「1–3 年 · 矩陣 G」，「⑦ 精密線圈電流源」，「要做出什麼：離子阱與中性原子用：ppm 級穩定型（內建 50/60 Hz 前饋）與毫秒級快切型」。
       ⑦ 在第二階段（st = 1），month = 0 < 12，卡片 opacity 0.4，但外框變白、寬 4。
  句 2（45 字，約 10.0 秒，卡 1）：needs = FEEDS 中值含 7 的鍵 = [3] → ③ 外框 #3ccf8e（綠）、寬 3.5；FEEDS[7] 不存在 → 沒有金框；
       detail「第一步：做 20 A 原型交給原子物理實驗室」「■ 需要先有：③ 量子等級電源規格 QGP」「■ 成果提供給：（無）」。
  句 3（52 字，約 11.6 秒，卡 2）：0.6 秒點 ④（_pw_card('壓縮機變頻驅動')；「第四項」約第 2–4 字）→ detail「1–3 年 · 矩陣 F」，
       「要做出什麼：脈衝管氦氣壓縮機（約 12.5 kW）的變頻驅動：軟啟動、群控、低諧波、低共模、驟降穿越」；
       needs = []（沒有任何 FEEDS 值含 4）→ 無綠框；FEEDS[4] = [1, 10] → ①、⑩ 外框 #e0a54a（金）。
       「對到矩陣裡超導當主力的那一列」對照簡報 p73／文獻回顧 §18：F 壓縮機與泵變頻驅動｜超導 ●（主力）離子阱 ◐ 中性原子 ○。
codes（S({ id: 'roadmap' …})，約第 497–525 行；卡片 g.pp 依 delay = 欄 × 1.2 + 列 × 0.25 秒淡入，約 3.7 秒全部出現）
  句 0（50 字，約 11.1 秒，pmap None）：三欄 12 張卡，每張左上角圓角色塊是代號（A＋B、H、QGP、OCP｜F、D、A／D、G｜I、I、A、E）；
       場景副標「代號對應簡報「產品 × 平台矩陣」A–I；點卡片可跳到對應的痛點場景」。
  句 1（51 字，約 11.3 秒，卡 0）：第三欄卡片「800 VDC 模組化量子資料中心」標 A（矩陣 A＝機房 UPS／配電／PDU，第一欄是「A＋B」）；
       「4 K GaN 低溫電源轉換」與「高通道數直流供電」都標 I。
  句 2（49 字，約 10.9 秒，卡 1）：2.0 秒點第三欄最下面的「解碼機櫃供電與液冷」卡（_pw_card；go = 'overview'；卡上小字「→ 看痛點：全景」；
       「解碼機櫃」約第 8–11 字，1.8 秒）→ App.go(0) 全景：最下方「運算匯流排 約 30 kW」，紫色 #9d8cff 粒子流 comp
       （M370,380 → 450,585）流進它，再分到「即時解碼 5–50 kW」「電子區空調 5–50 kW」。
  句 3（56 字，約 12.4 秒，卡 2）：0.4 秒點痛點 7（_pw_pp(7)；位置 728,542，在即時解碼旁）→ metrics「痛點 7｜解碼要緊鄰機台」，
       下方說明「超導回饋預算只有個位數到數十 µs；解碼機櫃沿用 AI 機房供電與液冷。」

試拍需確認：(1) devplan 卡片 click（MouseEvent bubbles）是否觸發 g 的 click listener、detail 是否立刻改成 ⑦／④（st.dirty → tick 重畫）；
(2) month = 0 時第二階段卡片 opacity 0.4，⑦／④ 的白框與 ③ 的綠框、①⑩ 的金框在錄影解析度下是否看得清楚；(3) detail 第一行
「1–3 年 · 矩陣 G／F」字級 13 px 是否可讀；(4) roadmap 句 2 點卡片時第三欄是否已淡入（句 0+1 約 22 秒，應已完全出現）；
(5) 跳到全景後 _pw_pp(7) 是否找得到 g.pp（App.go 會清空 svg 再 build，句 3 開始時應已完成）、面板文字是否在畫面內；
(6) 全景下方紫色粒子流是否明顯（comp 流率 2）。
"""
import json

LESSON = 'Q142'


def _pw_card(text):  # 點 #svg 裡含指定文字的 g.pp（devplan 項目卡設 st.sel；roadmap 卡片 App.go 到痛點場景）
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.includes(%s));"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));})()" % json.dumps(text))


def _pw_pp(n):  # 點全景場景的紅色痛點 n
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.trim()===%s);"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));window.__flash(document.getElementById('metrics'));})()" % json.dumps(str(n)))


_LIST = [
 dict(key='platform', pmap=[None, 0, 1, 2], after=5, page='pw', hash='devplan', scene='1,000 位元供電互動動畫 場景 8：開發計畫',
      title='動畫展示：代號背後是哪個平台', sub='互動動畫：開發計畫（規劃建議）',
      sentences=[
       '換到供電互動動畫的開發計畫，右邊預設打開第二項現場勘查服務，最上面那行小字寫著零到一年，後面跟著它的矩陣代號。',
       '點第二階段的第七項精密線圈電流源，小字換成一到三年和另一個代號，下面寫著離子阱與中性原子用，分成穩定型和快切型。',
       '這一項只有第三項量子等級電源規格亮起綠框；第一步寫著做二十安培的原型，交給原子物理實驗室。',
       '再點第四項壓縮機變頻驅動，寫的是脈衝管氦氣壓縮機，對到矩陣裡超導當主力的那一列；金框亮在第一項和第十項。'],
      actions=[(1, 0.8, _pw_card('精密線圈電流源')), (3, 0.6, _pw_card('壓縮機變頻驅動'))],
      points=[('⑦ 矩陣 G', '離子阱與中性原子用'), ('綠框 ③', '先要有 QGP 規格'), ('④ 矩陣 F', '超導壓縮機，成果給 ①⑩')], shot=(3, 6.0)),
 dict(key='codes', pmap=[None, 0, 1, 2], after=7, page='pw', hash='roadmap', scene='1,000 位元供電互動動畫 場景 7：三階段路線圖',
      title='動畫展示：同一個代號，不同階段', sub='互動動畫：三階段路線圖（規劃建議）',
      sentences=[
       '換到同一個動畫的路線圖，三欄共十二張卡片；這次只看每張卡左上角的圓角小標籤，它就是矩陣的代號。',
       '第三欄的模組化量子資料中心，又帶著機房配電那一列的代號；低溫電源轉換和高通道數直流，也共用同一個代號。',
       '點第三欄最下面的解碼機櫃供電與液冷，畫面直接跳到全景，最下面那條紫色粒子流過去的，就是運算匯流排。',
       '再點七號紅點，面板寫著解碼要緊鄰機台：超導的回饋預算只有個位數到數十微秒，解碼機櫃沿用人工智慧機房的供電與液冷。'],
      actions=[(2, 2.0, _pw_card('解碼機櫃供電與液冷')), (3, 0.4, _pw_pp(7))],
      points=[('同一個代號', 'A 跨階段、I 兩張共用'), ('E 解碼機櫃卡', '跳到全景的運算匯流排'), ('七號痛點', '解碼要緊鄰機台')], shot=(1, 6.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

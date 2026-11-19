"""Q138 三平台比較：三種 UPS 設計邏輯 — v2 動畫展示段（格式見 ../demos.py 的說明）。

compare 用 atoms.html（at，core.js 架構）：#controls 的 ui.radio 是 <button>，用 demos.py 的 ('click', 按鈕文字開頭)。
outage／roadmap 用 power1000.html（pw，SVG 頁面）：控制項是 .ctl 的 select／range，用 ('js', ...)；_pw_sel 照抄 q131.py，
_pw_sl 照抄 q133.py，_pw_card 為本課新寫（點路線圖卡片）。
與 q131–q137 不重複的操作：compare 場景（q131–q137 都沒用過）；outage 的「UPS 撐住冷卻鏈的時間（方案 C）」滑桿（q131 只切過
「備援方案」，本課為了讓滑桿生效，必須先切到方案 C，這一步和 q131 段 2 句 3 相同）；roadmap 場景（q131–q137 都沒用過）。

  compare  after=3（「三平台的單套功率」之後）       at#compare：預設「連接性」→ 句 3 按「規模」
  outage   after=6（「三種 UPS 設計邏輯」之後）      pw#outage：方案 C → 滑桿 60 分鐘
  roadmap  after=9（「產品評審：評審與業務」之後）    pw#roadmap：三欄卡片 → 點「分層 UPS＋精密空調參考設計」跳到 #outage

畫面依據（逐行讀 animations/js/atoms/13_compare.js、js/core.js、js/peripherals/common.js、animations/power1000.html；
本次沒有開瀏覽器試拍，秒數以「字數 ÷ 4.5」估）：
compare（13_compare.js）
  App.register id 'compare'、num 13、title「三平台比較：超導 · 離子阱 · 中性原子」；camera pos [0, 6.2, 11.2] → target [0, 0.5, −0.6]。
  三個底座 X = sc −5／ion 0／atom 5，各有發光圓環 COL sc 0x4f8cff（藍）、ion 0xffc04a（金）、atom 0x38d6e9（青）；
  底座標籤「超導（Google、IBM…）」「離子阱（Quantinuum、IonQ…）」「中性原子（QuEra、Atom Computing…）」。
  超導：4×4 金色十字量子位元＋藍色耦合器；App.buildFridge（peripherals/common.js，atoms.html 第 40 行有載入）放在 x = −6.75，
    標籤「10 mK 稀釋冷凍機」。離子阱與中性原子底座沒有冷凍機。
  離子阱：4 根銅色桿（0xc98a4b）沿 x 軸；8 顆金色離子（App.particle COL.ion）排成一串；離子之間金色弧線（conn 模式閃動）。
  中性原子：6×6 青色發光球；movers = 第 0、7、14、21 顆來回移動，上方各一支洋紅色（0xff4fd8）半透明錐 = 光鑷。
  ui.radio 按鈕「連接性」「閘速度」「相干時間」「規模」（預設 conn），另有「↻ 重播」。
  規模模式：caption（金色）「規模：已展示的量子位元 / 原子數（log₁₀，2024–2026 代表值）」；柱高 = log₁₀ 值 /7×2.8，
    約 0.67 秒長到定值；柱上標籤 sc「約 100–1000+（Willow 105、Condor 1121）」、ion「約 100（Helios 98）」、
    atom「數百到數千（Caltech 陣列 6100）」。readout 同 caption。
  句 0（47 字，約 10.4 秒）：預設畫面，三座底座與標籤。無動作。
  句 1（48 字，約 10.7 秒）：冷凍機與「10 mK 稀釋冷凍機」標籤；離子阱、中性原子底座沒有冷凍機。無動作。
  句 2（51 字，約 11.3 秒）：銅色桿、金色離子串、青色 6×6 陣列、洋紅色光鑷錐帶著四顆原子來回移動。無動作。
  句 3（50 字，約 11.1 秒）：0.3 秒按「規模」→ 柱子重長、標籤換成 1121／98／6100。
  「位元多，不等於用電多」只放在 points（對照第 3 頁單套功率），旁白句 3 只念畫面上的數字。
outage（power1000.html 第 403–452 行）
  select「備援方案」選項 none「A：只有控制電子接 UPS」／full「B：…」／gen「C：冷卻鏈 UPS，但發電機沒起來」（預設 none）；
  slider「UPS 撐住冷卻鏈的時間（方案 C）」5–60、step 5、預設 15，顯示「15 分鐘」。換方案或拉滑桿都會 st.play = 0（白點重跑）、重畫曲線。
  curve：方案 C 的冷卻停止時刻 t0 = ups×60 秒；之後約 120 秒到 1 K；再 1 小時開始降溫 3.5 天。紅色虛線在 1 K，
    文字「超過 1 K → 需要完整校準」。白點每約 12.6 秒從 1 秒走到 10 天（對數），上方文字「t = …　MXC ≈ …」。
  metrics：「方案」A／C、「冷卻鏈負載」55–110 kW、「停機時間（示意）」A＝約 3–5 天（含重新降溫與完整校準）、
    C＝約 3–5 天（UPS 耗盡後同 A）。
  句 0（50 字，約 11.1 秒）：預設方案 A，面板「冷卻鏈負載 55–110 kW」。無動作。
  句 1（53 字，約 11.8 秒）：0.3 秒選 C → 曲線轉折點移到 15 分鐘；白點約 6.3 秒後走到 15 分鐘（log 900／log 864000 ≈ 0.50）。
  句 2（41 字，約 9.1 秒）：0.4 秒滑桿設 60 → 標籤「60 分鐘」，曲線立刻重畫，轉折點在 1 小時，曲線仍衝過紅色虛線。
  句 3（47 字，約 10.4 秒）：metrics「停機時間（示意）約 3–5 天（UPS 耗盡後同 A）」。無動作。
roadmap（power1000.html 第 497–520 行）
  title「我們要怎麼做：三階段路線圖」；三欄標題「0–1 年：建立案例與規格」「1–3 年：進入供應鏈」「3–7 年：下一代架構」；
  卡片 opacity 依 delay = 欄×1.2＋列×0.25 秒淡入（約 3 秒內全部出現）。第一欄第一張 tag「A＋B」、文字「分層 UPS＋精密空調參考設計」、
  下方「→ 看痛點：斷電時間軸」（go = outage）；第二欄第一張「F」「壓縮機變頻驅動（軟啟動、N+1）」，第四張「G」「精密線圈電流源（原子平台）」。
  卡片 <g class="pp"> 有 click → App.go(outage)，hash 換成 #outage。
  句 0（53 字，約 11.8 秒）：三欄標題。無動作。
  句 1（42 字，約 9.3 秒）：第一欄第一張卡。無動作。
  句 2（58 字，約 12.9 秒）：第二欄的 F 卡與 G 卡。無動作。
  句 3（39 字，約 8.7 秒）：0.4 秒點 A＋B 卡 → 畫面換成斷電時間軸（方案 A 預設）。

試拍需確認：compare 預設視角下最左邊的冷凍機與「10 mK 稀釋冷凍機」標籤是否在畫面內（x = −6.75）、右側「中性原子（QuEra、Atom
Computing…）」標籤是否被切；規模模式的三個柱上標籤是否可讀；outage 句 1 白點走到 15 分鐘的時間點（約句內 6.6 秒）；roadmap
卡片在句 0 開始前是否已全部淡入（若錄影從場景載入就開始，句 0 開頭可能還在淡入）；roadmap 點卡片後 App.go 換頁是否正常。
"""
import json

LESSON = 'Q138'


def _pw_sel(label, value):
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const s=d.querySelector('select');window.__flash(d);s.value=%s;s.dispatchEvent(new Event('change'));})()"
            % (json.dumps(label), json.dumps(value)))


def _pw_sl(label, value):  # power1000 的 .ctl 滑桿：設 input.value 後送出 'input' 事件
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const i=d.querySelector('input');window.__flash(d);i.value=%s;i.dispatchEvent(new Event('input'));})()"
            % (json.dumps(label), json.dumps(str(value))))


def _pw_card(text):  # 點路線圖（roadmap）裡含指定文字的卡片；卡片的 click 會 App.go 到對應的痛點場景
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.includes(%s));"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));})()" % json.dumps(text))


_LIST = [
 dict(key='compare', pmap=[None, 0, 1, 2], after=3, page='at', hash='compare', scene='離子阱與中性原子 3D 場景 13：三平台比較',
      title='動畫展示：三個平台站一排', sub='三維動畫：超導、離子阱、中性原子並排比較',
      sentences=[
       '打開離子阱與中性原子動畫的第十三個場景，三平台比較：左邊是超導，中間是離子阱，右邊是中性原子。',
       '左邊面板寫著，超導需要十毫克耳文的稀釋冷凍機和大量佈線；離子阱和中性原子都不用它，用電大宗就從這裡分岔。',
       '離子阱是一串懸在四根銅色桿子之間的金色離子；中性原子是一片青色陣列，幾支洋紅色的光鑷正搬著原子來回走。',
       '按下規模，柱子換成已展示的位元數：超導標著一千一百二十一，離子阱九十八，中性原子的陣列有六千一百顆。'],
      actions=[(3, 0.3, ('click', '規模'))],
      points=[('超導', '需要 10 mK 稀釋冷凍機'), ('離子阱、中性原子', '不需要稀釋冷凍機'), ('規模', '位元多，不等於用電多')], shot=(3, 4.0)),
 dict(key='outage', pmap=[None, 0, 1, 2], after=6, page='pw', hash='outage', scene='1,000 位元供電互動動畫 場景 5：斷電時間軸',
      title='動畫展示：電池加大，只是延後', sub='互動動畫：斷電時間軸（方案 C）',
      sentences=[
       '回到供電互動動畫的斷電時間軸，先看面板：冷卻鏈負載寫著五十五到一百一十千瓦，這是一千位元設施的估算。',
       '改選方案丙，冷卻鏈有不斷電系統，可是發電機沒起來；預設撐十五分鐘，白點走到十五分鐘左右，就沿著曲線往上爬。',
       '把撐住的時間拉到六十分鐘，轉折點只往右挪到一小時，曲線一樣衝過一克耳文的紅色虛線。',
       '面板的停機時間仍寫著約三到五天；所以超導的不斷電系統是撐到發電機接手，不是靠電池撐完整場停電。'],
      actions=[(1, 0.3, _pw_sel('備援方案', 'gen')), (2, 0.4, _pw_sl('UPS 撐住冷卻鏈的時間', 60))],
      points=[('方案 C', '有 UPS，發電機沒起來'), ('UPS 撐 15 → 60 分鐘', '升溫只往後推'), ('停機時間', '仍約 3–5 天')], shot=(2, 5.0)),
 dict(key='roadmap', pmap=[None, 0, 1, 2], after=9, page='pw', hash='roadmap', scene='1,000 位元供電互動動畫 場景 7：三階段路線圖',
      title='動畫展示：一個想法，三種零件', sub='互動動畫：三階段路線圖（規劃建議）',
      sentences=[
       '換到供電互動動畫的路線圖，卡片分成三欄：零到一年建立案例與規格，一到三年進入供應鏈，三到七年做下一代架構。',
       '第一欄最上面那張，寫著分層不斷電系統加精密空調的參考設計，文件認為三個平台都需要它。',
       '第二欄裡，超導用得上的是壓縮機變頻驅動，原子平台用得上的是精密線圈電流源，同一個分層想法，落到不同平台變成不同零件。',
       '點一下分層不斷電系統那張卡，畫面直接跳到斷電時間軸，也就是這張卡要回答的痛點。'],
      actions=[(3, 0.4, _pw_card('分層 UPS＋精密空調參考設計'))],
      points=[('0–1 年第一張', '分層 UPS＋精密空調'), ('1–3 年', '壓縮機變頻・線圈電流源'), ('點卡片', '跳到對應的痛點')], shot=(2, 6.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

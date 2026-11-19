"""Q139 規模計算器：位元數一變，什麼先爆？ — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都在 power1000.html#scale（本課是規模計算器的主場；Q134 的 scale 段只把 N 設成 100、10,000 看「交流入口」「地線電流」兩列，
本課改看同軸線／KIDE 級冷凍機台數／脈衝管／4 K 熱負載／設施總功率，並動 Q134 沒碰的「每位元室溫控制電子功耗」與「架構」）：
  climb  after=4（「規模計算器的算法」之後）  「量子位元數 N」3 → 2（100）→ 慢拉回 3（1,000）→ 3.02（1,047）→ 4（10,000）
  power  after=7（「控制電子這一項」之後）    「每位元室溫控制電子功耗」50 → 150 → 1 W，再把 N 推到 3.02（1,047）
  cryo   after=10（「換你改造」之後）         「架構」選 cryo（未來：低溫 CMOS＋多工），再把 N 由 3 慢拉到 4

畫面依據（animations/power1000.html，S({ id: 'scale' …})，約第 251–297 行；共用模型 lines()／heat()／CAP 在約第 75–100 行）：
  build()：預設 st.N=1000、st.W=50、st.cryo=false。控制項：滑桿「量子位元數 N」(2–4.3, step 0.01, 預設 3, 顯示 fmtN(round(10^v)))、
    滑桿「每位元室溫控制電子功耗」(1–150, step 1, 預設 50, 顯示「50 W」)、選單「架構」(rt「今日：室溫控制、每位元獨立線」／cryo「未來：低溫 CMOS＋多工」)。
    _pw_sl／_pw_sweep 用 label.includes 找控制項：「量子位元數」只對到第一根滑桿（第二根的文字是「每位元…」，不含「量子位元數」）。
  render()：L = lines(N, cryo)：C = round(1.5N)、fl = ceil(N/8)、xy = cryo ? ceil(N/16) : N、flux = cryo ? ceil((N+C)/16) : N+C、
    total = xy+flux+3fl、dc = (cryo ? 0 : N+C)+3fl。fridges = max(1, ceil(total/4000))；
    pts = max(3·fridges, ceil(s50/52.5), ceil(s4/1.9))；dcUnits = ceil(dc/24)；inst = ceil(N/7)+dcUnits+10；
    elec = N·(cryo ? min(W,5) : W)/1000；comp = 12.5·pts；dec = 25N/1000；hv = 0.4(elec+0.045dcUnits+dec)；
    kw = 1.6comp + 4fridges + elec + 0.045dcUnits + 3 + dec + hv；pe = 0.75e-3·inst。
    七列門檻：同軸 4000、精密直流 3000、交流入口 350、地線 0.1 A、脈衝管 5、4 K 熱負載＝容量 1.9·pts（此列 val > ref 才紅、不畫虛線）、設施 320 kW。
    顏色：超過門檻 紅 #ff5a5f；frac > 0.75 橘黃 #e0a54a；其餘 青 #38c6d9。白色虛線在 x = 260 + 640/log10(37) ≈ 668。
  以下數字都是把上述公式照抄成 node 腳本算出（2026-11-18；依指示錄影進行中不開瀏覽器，未開頁核對）。

climb（秒數以「字數 ÷ 4.5」估）
  句 0（50 字，約 11.1 秒）：3.5 秒起 1.5 秒內 N 由 3 拖到 2 →「N = 100 位元 · 耦合器 150 · 讀取饋線 13」；七列：389 條、289 路、38 個、0.03 A、
       3 支（37.5 kW 壓縮機）、452 mW（容量 5.7 W）、78 kW，全部青色；最長的脈衝管列寬 329 px < 虛線 408 px →「沒有一條碰到白色虛線」。
  句 1（44 字，約 9.8 秒）：0.3 秒起 4.5 秒內 N 由 2 拖回 3。地線列 v≈2.67（N≈468）變紅 → 約 3.3 秒（「最先變紅」約 3.8 秒說到）；
       同軸 v≈2.89、精密直流／脈衝管 v≈2.90、交流入口 v≈2.99 轉橘黃，4.8 秒停在 1,000：3,875 條、2,875 路、273 個、4 支（皆橘黃），
       0.20 A（紅），4.5 W／容量 7.6 W、200 kW（青）。
  句 2（48 字，約 10.7 秒）：1.5 秒設 3.02 → N = 1,047：同軸 4,058 條，紅，小字「需 2 台 KIDE 級」；列寬 410 px，剛越過虛線（408 px）。
       同一格精密直流 3,011 路也變紅（旁白不提）。
  句 3（45 字，約 10.0 秒）：脈衝管 4 → 6 支（3×2 台冷凍機；75.0 kW 壓縮機）已在句 2 出現；4.0 秒起 1.5 秒內 N 由 3.02 拖到 4 →
       N = 10,000：38,750 條（需 10 台 KIDE 級）、28,750 路、2,637 個、1.98 A、39 支、1948 kW 全紅；4 K 45.0 W／容量 74.1 W（frac 0.61）青色。
power
  句 0（50 字，約 11.1 秒）：預設 N = 1,000、W = 50：設施總功率「200 kW」青色；面板 metrics「控制電子 50.0 kW」。3.0 秒對第二根滑桿設 50（不改值，只亮黃框）。
  句 1（51 字，約 11.3 秒）：1.0 秒起 3 秒內 W 50 → 150：kw = 200 + 1.4·(W−50) → 340 kW，紅（W≈136 時跨 320，約 3.6 秒）；metrics「控制電子 150.0 kW」。
  句 2（51 字，約 11.3 秒）：1.0 秒起 2.5 秒內 W 150 → 1：kw = 131 kW（青）；同軸 3,875 條（橘黃）不變——lines() 不含 W。
  句 3（46 字，約 10.2 秒）：1.5 秒設 N = 3.02（1,047），W 仍 1：同軸 4,058 條紅；設施 177 kW（frac 0.55，青）。
cryo
  句 0（56 字，約 12.4 秒）：3.0 秒「架構」選 cryo → N = 1,000：同軸 595 條（63+157+375）、精密直流 375 路、脈衝管 3 支，皆青；4 K 2.3 W；
       地線 0.13 A 仍紅（旁白不提）。
  句 1（53 字，約 11.8 秒）：1.5 秒起 6 秒內 N 由 3 拖到 4（cryo）：交流入口 v≈3.34（N≈2,188）紅 → 約 3.5 秒；脈衝管 v≈3.63（4,266）、
       設施 v≈3.66（4,571）約 5.3–5.5 秒紅；同軸 v≈3.83（6,761，4,018 條）約 6.5 秒紅（「六千七百多」約 9.3 秒說到）；4 K 在 v≈3.28 轉橘黃。
  句 2（49 字，約 10.9 秒）：N = 10,000：同軸 5,938 條「需 2 台 KIDE 級」；脈衝管 12 支（150.0 kW）。「第一段的十台、三十九支」指 climb 句 3 畫面。
  句 3（54 字，約 12.0 秒）：4 K 22.5 W（含 10,000×1.5 mW = 15 W）／容量 22.8 W（12×1.9），frac 0.99 → 橘黃（此列 val > ref 才紅，
       而 pts 由 ceil(22.5/1.9) = 12 決定，所以 cryo 下 4 K 列最多到橘黃）。設施 681 kW、精密直流 3,750 路（紅），旁白不提。

試拍需確認：(1) _pw_sweep 拖對數滑桿時 N 文字與橫條是否順暢更新（step 0.01，每秒 12 步）；(2) climb 句 2 同軸列寬 410 px 只比虛線多 2 px，
截圖是否看得出「越過虛線」；(3) 黃色外框（.qflash／__flash）是否落在被動的那根滑桿；(4) cryo 句 1 的紅燈順序（交流入口 → 脈衝管、設施 → 同軸）
在錄影中是否和旁白對得上；(5) 面板 metrics「控制電子」一格是否在 1600×900 畫面內可見。
"""
import json

LESSON = 'Q139'


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


_N = '量子位元數'
_W = '每位元室溫控制電子功耗'

_LIST = [
 dict(key='climb', pmap=[0, None, 1, 2], after=4, page='pw', hash='scale', scene='1,000 位元供電互動動畫 場景 2：規模計算器',
      title='動畫展示：一級一級往上調', sub='互動動畫：規模計算器',
      sentences=[
       '打開供電互動動畫的規模計算器，先把量子位元數拉到最左邊的一百，七列橫條全是青色，沒有一條碰到白色虛線。',
       '接著慢慢拉回一千：地線電流那列最先變紅，同軸線、精密直流、交流入口和脈衝管則變成橘黃色。',
       '再往右推一小格到一千零四十七位元，同軸線變成四千零五十八條，剛好越過白色虛線變紅，小字寫著需要兩台。',
       '同一格裡，脈衝管從四支跳到六支；最後拉到一萬位元，七列裡只剩四克耳文熱負載那一列還是青色。'],
      actions=[(0, 3.5, _pw_sweep(_N, 3, 2, 1.5)), (1, 0.3, _pw_sweep(_N, 2, 3, 4.5)),
               (2, 1.5, _pw_sl(_N, 3.02)), (3, 4.0, _pw_sweep(_N, 3.02, 4, 1.5))],
      points=[('一百位元', '七列全是青色'), ('一千零四十七位元', '同軸線先撞牆'), ('一萬位元', '只剩四克耳文沒變紅')], shot=(3, 7.0)),
 dict(key='power', pmap=[None, 0, 1, 2], after=7, page='pw', hash='scale', scene='1,000 位元供電互動動畫 場景 2：規模計算器',
      title='動畫展示：省電救得了線嗎？', sub='互動動畫：規模計算器',
      sentences=[
       '回到規模計算器，位元數停在一千，第二根滑桿是每位元室溫控制電子功耗，預設五十瓦，設施總功率兩百千瓦。',
       '把功耗拉到一百五十瓦，面板上的控制電子從五十千瓦變成一百五十千瓦，設施總功率跳到三百四十千瓦，變紅了。',
       '反過來拉到最左邊的一瓦，設施總功率降到一百三十一千瓦，可是同軸線那列還是三千八百七十五條，一條都沒少。',
       '這時再把位元數推到一千零四十七，設施總功率只有一百七十七千瓦，同軸線照樣變紅：省電救不了線。'],
      actions=[(0, 3.0, _pw_sl(_W, 50)), (1, 1.0, _pw_sweep(_W, 50, 150, 3.0)), (2, 1.0, _pw_sweep(_W, 150, 1, 2.5)),
               (3, 1.5, _pw_sl(_N, 3.02))],
      points=[('一百五十瓦', '設施總功率變紅'), ('一瓦', '同軸線一條沒少'), ('一千零四十七位元', '省電擋不住線')], shot=(1, 6.0)),
 dict(key='cryo', pmap=[0, 1, 2, 2], after=10, page='pw', hash='scale', scene='1,000 位元供電互動動畫 場景 2：規模計算器',
      title='動畫展示：低溫控制加多工', sub='互動動畫：規模計算器',
      sentences=[
       '最後試孩子改造的方向：架構選單切到未來的低溫控制晶片加多工，一千位元的同軸線從三千八百七十五條降到五百九十五條。',
       '接著把位元數往上拉，這次接著變紅的換成交流入口，然後是脈衝管和設施總功率，同軸線拖到六千七百多位元才變紅。',
       '停在一萬位元：同軸線五千九百三十八條，冷凍機從第一段的十台變成兩台，脈衝管也從三十九支降到十二支。',
       '可是四克耳文熱負載二十二點五瓦，容量二十二點八瓦，變成橘黃色；每位元多出的一點五毫瓦，把瓶頸搬到了四克耳文。'],
      actions=[(0, 3.0, _pw_sel('架構', 'cryo')), (1, 1.5, _pw_sweep(_N, 3, 4, 6.0))],
      points=[('低溫控制＋多工', '同軸線大減'), ('紅燈順序', '交流入口先，同軸線最後'), ('一萬位元', '瓶頸搬到四克耳文')], shot=(2, 4.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

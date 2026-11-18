"""Q133 機房要求：防振、接地與電磁干擾 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段，依插入位置排列：
  field  after=3（勘查規格頁之後）  pw#field   只看規格上的直流／交流兩個磁場門檻（距離、電流、配線留給 Q135）
  infra  after=6（防振頁之後）      pe#infra   避震座、降振開關、單點接地（課綱指定的 3D 場景）
  ground after=7（接地頁之後）      pw#ground  只看預設值與「每台漏電流」降到醫療級（加儀器數、拓樸留給 Q134）

畫面依據（逐句；秒數以「字數 ÷ 4.5」估）：

field（animations/power1000.html，S({ id: 'field' …})，約第 454–495 行）
  句 0（56 字，約 12.4 秒）：render() 非偶極模式時在 x=ox=130 畫母線長條，文字 st.mode==='pair' → 「母線（成對）」；
       冷凍機圓圈在 fx = ox + d×95 = 130+285 = 415（母線右邊），圓內文字「冷凍機」，下方距離文字「3.0 m」；
       熱圖色相 (1-v)×200（v 大＝紅），右上框文字「色塊：藍＝弱、紅＝強（對數）」。
  句 1（48 字，約 10.7 秒）：build() 預設 I=360、d=3、mode='pair'、s=0.1、ac=true。
       B = 2e-7×360×0.1／3² = 8e-7 T = 0.8 µT → 顯示「冷凍機位置磁場 ≈ 0.800 µT」；
       ac 為真時門檻 B < 0.1 µT → ok=false → 紅色 #ff5a5f，文字「交流要求 ≪ 1 µT（此處以 0.1 µT 判斷）」
       與「超過：拉開距離、成對配線、補償線圈或屏蔽」。
  句 2（56 字，約 12.4 秒）：0.4 秒時取消勾選 label.tog「交流（50/60 Hz）」→ st.ac=false → 門檻 B < 100 µT →
       綠色 #3ccf8e「符合」、文字「直流要求 < 100 µT」；B 值不變（0.800 µT）。
ground（animations/power1000.html，S({ id: 'ground' …})，約第 350–400 行）
  句 0（54 字，約 12.0 秒）：上方 12 個方框文字「儀器」，各畫一個電容符號並標「Y」（旁白不唸字母，只說「小電容」）；
       下方文字「保護地線（PE）」；Flow 粒子顏色 #ff5a5f（紅點），desc「紅點代表接地電流」。
  句 1（51 字，約 11.3 秒）：預設 n=250、leak=0.75 mA、R=5 mΩ、shelf=false → 「交流入口 250 個 × 0.75 mA」；
       pe = 250×0.75e-3 = 0.1875 A → 「地線電流 ≈ 0.188 A」（> 0.1 A 為紅色）；
       gp = 0.1875×5e-3 ≈ 0.94 mV → 以 µV 顯示約「938 µV」（> 5 µV 為紅色）→ 旁白「將近一毫伏」。
  句 2（61 字，約 13.6 秒）：1.4 秒時把 .ctl「每台漏電流」（0.1–3.5，step 0.05）設為 0.1 →
       pe = 0.025 A，gp = 1.25e-4 V →「地電位差 ≈ 125 µV（偏壓要求 µV 級）」，仍 > 5 µV → 紅色。
       0.1 mA＝100 µA，對應供電簡報 p22／文獻回顧 §3.4.2 的醫療級觸碰電流 100 µA（「大約是醫療級的等級」）。
infra（animations/js/peripherals/08_infra.js）
  句 0（50 字，約 11.1 秒）：ctx.label('避震座 + 剛性框架', [1.9, 0.2, 2.2])；四個避震座方塊在 (±1.6, ±1.6)；common.js buildFridge 框架四支腳也在 (±W, ±W)，W=1.6。
  句 1（77 字，約 17.1 秒）：兩條 dynLine：冷頭處 vib（0xff7a59，y≈4.35）與樣品處 vib2（0x2ecc71 綠，y≈0.55，位置較低）；
       標籤 vL.set(`冷頭振動 → 樣品處振動（${remoteMotor ? '已隔離' : '未隔離'}）`)。
       8.6 秒（旁白說到「關掉」後）把 ui.toggle「脈衝管遠端馬達 + 纜線固定（降振）」（預設 on）關掉 →
       damp 由 0.12 變 0.6 → 綠色波振幅 A×damp 由 0.03 變 0.15（五倍），括號變「未隔離」。
  句 2（61 字，約 13.6 秒）：0.3 秒時再打開 → damp 回 0.12；ctx.label('單點接地', [-1.6, 0.35, 4.3])；
       四條 0x9ad11a 細管由 [-3.4,..,2.25]（控制電子 + 電腦）、[0,..,1.6]（冷凍機）、[3.8,..,2.6]（壓縮機）、
       [-6.5,..,2.7]（隔離變壓器）連到接地點 [-1.6, 0.05, 3.8]。

試拍需確認：pe#infra 兩條波與「避震座 + 剛性框架」「單點接地」標籤在 1600×900 畫面中是否可見、綠色波是否被壓縮機方塊遮住；
接地細管（半徑 0.02）可能很細，旁白只說「各有一條線連到這一點」。
"""
import json

LESSON = 'Q133'


def _pw_tog(label, on):
    return ('js', "(()=>{const l=[...document.querySelectorAll('#controls label.tog')].find(x=>x.textContent.includes(%s));"
                  "const i=l.querySelector('input');window.__flash(l);if(i.checked!==%s){i.checked=%s;i.dispatchEvent(new Event('change'));}})()"
            % (json.dumps(label), 'true' if on else 'false', 'true' if on else 'false'))


def _pw_sel(label, value):
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const s=d.querySelector('select');window.__flash(d);s.value=%s;s.dispatchEvent(new Event('change'));})()"
            % (json.dumps(label), json.dumps(value)))


def _pw_sl(label, value):  # power1000 的 .ctl 滑桿：設 input.value 後送出 'input' 事件
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const i=d.querySelector('input');window.__flash(d);i.value=%s;i.dispatchEvent(new Event('input'));})()"
            % (json.dumps(label), json.dumps(str(value))))


_LIST = [
 dict(key='field', after=3, page='pw', hash='field', scene='1,000 位元供電互動動畫 場景 6：磁場與配電佈局',
      title='動畫展示：規格上的兩個磁場數字', sub='互動動畫：磁場與配電佈局',
      sentences=[
       '再看供電動畫的磁場場景，這是一張俯視圖：左邊那條是成對的母線，右邊三公尺外的圓圈是冷凍機，色塊越紅代表磁場越強。',
       '預設是三百六十安培、距離三公尺，冷凍機位置大約零點八微特斯拉，用交流的要求來看，顯示紅色的超過。',
       '取消交流這個勾選，改用直流的要求，同樣的零點八微特斯拉就變成綠色的符合，因為直流的門檻是一百微特斯拉，寬鬆得多。'],
      actions=[(2, 0.4, _pw_tog('交流', False))],
      points=[('俯視圖', '母線到冷凍機三公尺'), ('交流要求', '零點八微特斯拉就超過'), ('直流要求', '一百微特斯拉以下符合')], shot=(1, 6.0)),
 dict(key='infra', after=6, page='pe', hash='infra', scene='周邊系統 3D 場景 8：機房基礎設施',
      title='動畫展示：機房裡的防振與接地', sub='三維動畫：機房基礎設施',
      sentences=[
       '打開周邊系統動畫的機房基礎設施場景，畫面上有一個標籤寫著避震座加剛性框架，冷凍機框架的四隻腳就站在避震座上。',
       '畫面上還有兩條波，標籤寫著冷頭振動傳到樣品處振動，現在括號裡是已隔離；關掉脈衝管遠端馬達加纜線固定這個開關，位置較低的那條綠色波馬上變大，括號改成未隔離。',
       '再把開關打開，綠色的波又變小；地上還有一個標籤寫著單點接地，控制電子、冷凍機、壓縮機和隔離變壓器，都各有一條線連到這一點。'],
      actions=[(1, 8.6, ('toggle', '脈衝管遠端馬達', False)), (2, 0.3, ('toggle', '脈衝管遠端馬達', True))],
      points=[('避震座', '加剛性框架'), ('降振開關', '關掉後樣品處振動變大'), ('單點接地', '各設備一條線回到同一點')], shot=(1, 14.0)),
 dict(key='ground', after=7, page='pw', hash='ground', scene='1,000 位元供電互動動畫 場景 4：接地與共模',
      title='動畫展示：合規的漏電流加起來', sub='互動動畫：接地與共模',
      sentences=[
       '換到供電互動動畫的接地場景：上面一排是儀器，每台都有一個小電容，把電流漏到下面的保護地線，紅點就是接地電流。',
       '預設是兩百五十個交流入口、每個零點七五毫安培，地線電流大約零點一九安培，地電位差將近一毫伏，都是紅色。',
       '把每台漏電流拉到零點一毫安培，大約是醫療級電源的等級，地電位差降到一百二十五微伏，可是還是紅色，因為偏壓要求的是微伏等級。'],
      actions=[(2, 1.4, _pw_sl('每台漏電流', 0.1))],
      points=[('每台小電容', '電流漏到保護地線'), ('兩百五十台', '地電位差將近一毫伏'), ('降到醫療級', '仍超過微伏要求')], shot=(2, 6.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

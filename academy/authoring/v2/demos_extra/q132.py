"""Q132 精密 DC 源與雜訊預算 — v2 動畫展示段（格式見 ../demos.py 的說明）。

power1000.html（pw）是 SVG 頁面，控制項是 .ctl 滑桿／select 與 label.tog 勾選框，不是 operation.html 的按鈕，
所以用 ('js', ...) 操作；下面的小函式產生那段程式碼（照抄 q131.py）。

每段每句的畫面依據（行號為 2026-11-18 讀到的版本）：

electronics（pe#electronics，animations/js/peripherals/06_electronics.js；不操作控制項）
  句 0：mods 陣列共 9 個模組，由上而下（y = 3.95 − i·0.43）；第 8 個 ['dc', 'DC 電流源（磁通偏壓）'] ＝倒數第二。
  句 1：pk2 = U.sphere(0.08, U.glow(0x9ad1a0))（淡綠）；update 裡 pk2 沿 P.dcFr 以 (time*0.25)%1 不停循環（約 4 秒一圈）；
        dcFr 名稱含 'Fr' → 纜線色 0xff9f43（橘）；dcFr 終點 [3.6, 0.5, −0.2]，晶片在 [3.4, 0.4, 0]。
  句 2：pk 依 seq() 各步變色（0x38c6d9、0x4f8cff、0xe0a54a…），stepLbl（'big teal'，位置 [0.8, 4.9, 0]）顯示「① 上傳脈衝序列…⑤ 結果回傳電腦」。
  句 3：第 1 個模組「銣原子鐘 / 10 MHz 分配」；clkT % 1 < 0.15 時 emissive 0.9、時脈小球放大（一閃一閃）；
        最後一個模組「HEMT 偏壓 · TWPA 泵浦源」。
overview（pw#overview，animations/power1000.html 第 167–249 行）
  句 0：節點 '乾淨匯流排'（450,330）位於三條匯流排中間；負載 '控制電子'、'精密直流 ×110 台'、'時脈與網路' 標 'clean'。
  句 1：_pw_pp(4) 點痛點 4 → metrics 顯示「痛點 4｜2,500–3,000 路精密直流」與說明
        「約 110 台 24 通道儀器；單台合格不等於接起來合格；前一級電源的共模、熱漂移是關鍵。」（metrics 在左側面板）
  句 2：勾「模擬斷電（市電中斷）」→ f.grid.on = false；ups.ctrl 預設 true → clean、elec、dc、clk、tofr2 繼續產生粒子。
  句 3：取消「控制與量測接 UPS」→ ctrl = false → 上述五條 Flow.on = false，不再產生新粒子，已在路上的跑完消失。
        後半句「真實的機器裡偏壓一跳要重新校準」是文獻回顧 §3.1.2「中斷與驟降」，明說是真實機器，不是畫面。
ground（pw#ground，animations/power1000.html 第 350–400 行）
  句 0：12 個 '儀器' 方框，每個畫電容符號（標 'Y'）；desc「紅點代表接地電流」；'保護地線（PE）'。
  句 1：預設 C = 100 → 黑框（box 330,290 fill rgba(8,14,26,.85)）最後一行
        「每顆 DC-DC 共模尖峰 ≈ 0.24 A（100 pF × 48 V／20 ns）」；node 算得 100e-12*48/20e-9 = 0.24。
  句 2：勾「量子等級隔離 DC-DC（隔離電容 ≤ 10 pF）」→ C = min(100,10) = 10 → 黑框「0.02 A（10 pF …）」，
        左側 metrics「共模尖峰」由 240.0 mA 變 24.0 mA。
  句 3：勾「機櫃集中供電」→ n = ceil(250/12) = 21、leak = min(0.75,0.5) = 0.5 → 黑框「交流入口 21 個 × 0.50 mA」，
        地電位差由 938 µV 變 53 µV（gp > 5e-6 仍為紅色 #ff5a5f），文字「（偏壓要求 µV 級）」。
"""
import json

LESSON = 'Q132'


def _pw_tog(label, on):
    return ('js', "(()=>{const l=[...document.querySelectorAll('#controls label.tog')].find(x=>x.textContent.includes(%s));"
                  "const i=l.querySelector('input');window.__flash(l);if(i.checked!==%s){i.checked=%s;i.dispatchEvent(new Event('change'));}})()"
            % (json.dumps(label), 'true' if on else 'false', 'true' if on else 'false'))


def _pw_sel(label, value):
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const s=d.querySelector('select');window.__flash(d);s.value=%s;s.dispatchEvent(new Event('change'));})()"
            % (json.dumps(label), json.dumps(value)))


def _pw_sl(label, value):  # 設定 pw 頁的 .ctl 滑桿（本課未用，留給改稿時用）
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const i=d.querySelector('input[type=range]');window.__flash(d);i.value=%s;i.dispatchEvent(new Event('input'));})()"
            % (json.dumps(label), json.dumps(str(value))))


def _pw_pp(n):  # 點全景場景的紅色痛點 n
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.trim()===%s);"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));window.__flash(document.getElementById('metrics'));})()" % json.dumps(str(n)))


_LIST = [
 dict(key='electronics', after=3, page='pe', hash='electronics', scene='周邊系統 3D 場景 6：室溫控制電子學',
      title='動畫展示：精密直流在哪裡', sub='三維動畫：控制電子機櫃裡的直流電流源',
      sentences=[
       '打開周邊系統動畫的控制電子學場景，中間這座機櫃從上到下排著九個模組，倒數第二個就是直流電流源，負責磁通偏壓。',
       '盯著一顆淡綠色的小球看：它從直流電流源出發，沿著橘色的線一路走進冷凍機，到了晶片旁邊又從頭開始，從來不停。',
       '另一顆會換顏色的封包，則是一輪一輪地送出脈衝、讀回結果，上方的大字會寫出現在走到第幾步。',
       '最上面的銣原子鐘一閃一閃，代表所有儀器都對齊同一個十兆赫的參考時脈；最下面那個模組，負責放大器的偏壓和泵浦。'],
      actions=[],
      points=[('直流電流源', '磁通偏壓，從來不停'), ('脈衝封包', '一輪一輪送與讀'), ('銣原子鐘', '十兆赫參考時脈')], shot=(1, 4.0)),
 dict(key='overview', after=5, page='pw', hash='overview', scene='1,000 位元供電互動動畫 場景 1：全景',
      title='動畫展示：一百一十台精密直流', sub='互動動畫：乾淨匯流排與精密直流',
      sentences=[
       '回到供電互動動畫的全景，中間那條是乾淨匯流排，後面接著控制電子、時脈與網路，還有一百一十台精密直流。',
       '點四號紅點，左邊面板寫著：兩千五百到三千路精密直流，單台合格不等於接起來合格，前一級電源的共模和熱漂移是關鍵。',
       '勾選模擬斷電，進線的粒子停了，但乾淨匯流排靠不斷電系統繼續流，流向精密直流的粒子也沒有斷。',
       '再取消控制與量測接不斷電系統，乾淨那一條的粒子流完就停了；在真實的機器裡，偏壓一跳，量子位元就得重新校準。'],
      actions=[(1, 0.3, _pw_pp(4)), (2, 0.3, _pw_tog('模擬斷電', True)), (3, 1.0, _pw_tog('控制與量測接 UPS', False))],
      points=[('乾淨匯流排', '接一百一十台精密直流'), ('四號痛點', '單台合格不等於整體'), ('取消保護', '乾淨那條停下來')], shot=(1, 6.0)),
 dict(key='ground', after=10, page='pw', hash='ground', scene='1,000 位元供電互動動畫 場景 4：接地與共模',
      title='動畫展示：繞過濾波器的電流', sub='互動動畫：接地與共模',
      sentences=[
       '打開供電互動動畫的接地與共模場景，上面一排是儀器，每台都畫了一個電容符號，紅點就是漏進保護地線的電流。',
       '中間黑框的最後一行寫著，每顆隔離直流轉換器的共模尖峰大約零點二四安培，就是一百皮法乘上四十八伏特、再除以二十奈秒。',
       '勾選量子等級隔離直流轉換器，隔離電容壓到十皮法，左邊面板的共模尖峰，從二百四十毫安培變成二十四毫安培。',
       '再勾機櫃集中供電，交流入口從兩百五十個變成二十一個，地電位差從九百多微伏降到五十多微伏，但還是紅色，因為偏壓要求是微伏等級。'],
      actions=[(2, 0.4, _pw_tog('量子等級隔離 DC-DC', True)), (3, 0.4, _pw_tog('機櫃集中供電', True))],
      points=[('共模尖峰', '電容乘電壓變化率'), ('隔離電容十皮法', '尖峰變十分之一'), ('集中供電', '地電位差降，仍超標')], shot=(3, 9.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)

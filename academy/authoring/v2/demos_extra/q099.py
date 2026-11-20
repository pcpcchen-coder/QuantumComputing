"""Q099 第 1 課：SQUID 干涉之後能做什麼 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景：animations/index.html#squid（js/scenes/06_squid.js）
  滑桿：「外加磁通 Φ / Φ₀」（-1–1，步進 0.005，預設 0.25）、「接面不對稱度 d = (E_J1 − E_J2)/(E_J1 + E_J2)」（0–0.8，預設 0）；
  開關：自動掃描磁通（flux = sin(0.35·time)，起點取決於場景時間，不用）。
  畫面：銀色超導環，左右兩側橘紅色 JJ（亮度 ∝ 等效 E_J）；環下方金色 Z 控制線；環內淺藍色箭頭（0x7fdcff）長度 ∝ Φ、
  透明度 min(1, 2|Φ| + 0.05)，Φ = 0 時看不見；環上 28 顆淡金色光點繞圈，速度 ∝ sin(πΦ)，|sin(πΦ)| < 0.03 時隱藏。
  右下插圖：灰色 = d = 0 曲線、金色（#e0a54a）= 目前 d 的曲線、青色圓點（#38c6d9）= 目前 Φ；曲線頂端標「甜蜜點」。
  以場景模型重算（E_JΣ = 20、E_C = 0.25 GHz）：f₀₁(0) = 6.075；f₀₁(±0.08) = 5.974；f₀₁(0.17) = 5.619、f₀₁(0.33) = 4.262；
  d = 0 時 f₀₁(0.5) = 0（max(0, …)）；d = 0.5 時 f₀₁(0.5) = 4.222 GHz。
  record_demo.js 的 'sweep' 會把值 Math.round 成整數，不能掃 -1–1 的磁通，所以用 SWEEP()（'js' 動作，以 requestAnimationFrame 依關鍵幀改滑桿並觸發 input）。
場景：animations/transmon-3d.html#case（第 6 章：三顆可調 transmon 的頻率配置）
  步驟按鈕在 #c6steps（沒有 id），用 ('sel', '#c6steps button:nth-child(2)') 進入步驟 ② SQUID 調頻；「自動接續」核取方塊 #c6auto（預設勾選），先取消。
  步驟 ②（dur 20 s）：4 s 時 Q1 開始掃描：0–3 s 平滑升到 Φ = 0.2、3–8 s 停住、8–11 s 降回 0（Q1 頻率 5.12 → 約 4.58 GHz）；
  Q1（青綠 #35b8ac，最左邊）SQUID 冒銅色小箭頭、Z 線發銅色光；看板左邊 |cos| 小圖上青綠色圓點下滑；右邊頻率尺（4.55–5.45 GHz，往右變高）
  青綠色實線左移，並以 |df/dΦ| × 0.0025 的幅度抖動（離開 Φ = 0 才明顯）。
  transmon 頁面沒有 App.speed（FPS_FIX 不適用）；dt 上限 0.05 s，負載高時落後約 3–9 s，旁白避免精確對時，也不念左上方字幕。
"""
import json

LESSON = 'Q099'


class _Demos(list):
    def keys(self):
        return [LESSON]

    def items(self):
        return [(LESSON, list(self))]

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


# 幀率補償（同 q004.py）：core.js 把每幀 dt 限在 0.05 秒，負載高時動畫會落後旁白。
FPS_FIX = ('js', "(()=>{if(window.__qfps)return;window.__qfps=1;let n=0,t0=performance.now();"
                 "const f=(now)=>{n++;if(now-t0>=1000){App.speed=Math.min(8,Math.max(1,20*(now-t0)/1000/n));n=0;t0=now;}"
                 "requestAnimationFrame(f);};requestAnimationFrame(f);})()")


def SWEEP(label, keys):
    """依關鍵幀 [(秒, 值), ...] 平滑拖動滑桿（小數值；牆鐘時間）。"""
    return ('js', "(()=>{const l=[...document.querySelectorAll('#controls .slider')].find(x=>x.textContent.includes(%s));"
                  "if(!l)return;const r=l.querySelector('input');const K=%s;const t0=performance.now();"
                  "l.classList.add('qflash');"
                  "const f=(n)=>{const t=(n-t0)/1000;let v=K[K.length-1][1];"
                  "for(let i=1;i<K.length;i++){if(t<=K[i][0]){const a=K[i-1],b=K[i];v=a[1]+(b[1]-a[1])*(t-a[0])/(b[0]-a[0]);break;}}"
                  "r.value=v;r.dispatchEvent(new Event('input'));"
                  "if(t<K[K.length-1][0])requestAnimationFrame(f);else l.classList.remove('qflash');};"
                  "requestAnimationFrame(f);})()" % (json.dumps(label, ensure_ascii=False), json.dumps(keys)))


FLUX = '外加磁通'
ASYM = '接面不對稱度'
S_SQUID = '超導場景 6：DC SQUID'
S_CASE = 'transmon 3D 第 6 章：三顆可調 transmon 的頻率配置'

DEMOS = _Demos([
 dict(key='flux', after=4, page='jj', hash='squid', scene=S_SQUID,
      title='動畫展示：磁通一加，頻率就變', sub='三維動畫：兩個 JJ 並聯成環的 DC SQUID',
      sentences=[
       '打開約瑟夫森接面動畫的第六個場景，中間是一個銀色的超導環，左右兩側各有一塊橘紅色的接面，下面那條金色細線就是磁通控制線；現在磁通是零，環裡什麼也沒有穿過。',
       '我們把磁通從零慢慢加到半個磁通量子，一片淺藍色箭頭從環中間穿過去，越來越明顯，兩側接面旁的缺口也開始閃出金色小光點。',
       '看右下角的小圖：青色圓點已經沿著金色曲線滑到最低點，頻率一路掉到底。',
       '再把磁通繼續加到一個磁通量子，圓點又爬回最高點，接面旁的小光點也消失；每隔一個磁通量子，頻率的變化就重複一次。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.3, ('slider', ASYM, 0)), (0, 0.4, ('slider', FLUX, 0)),
               (1, 2.0, SWEEP(FLUX, [(0, 0), (7, 0.5)])),
               (3, 0.3, SWEEP(FLUX, [(0, 0.5), (4, 1.0)]))],
      points=[('零磁通', '圓點在最高點'), ('半個磁通量子', '頻率掉到底'), ('一個磁通量子', '又回到最高點')], shot=(1, 8.0)),
 dict(key='sweetspot', after=6, page='jj', hash='squid', scene=S_SQUID,
      title='動畫展示：甜蜜點和不對稱接面', sub='三維動畫：f₀₁ 與外加磁通的關係',
      sentences=[
       '回到同一個場景，把磁通放回零，青色圓點停在小圖曲線的最高點，旁邊寫著甜蜜點，這一段曲線是平的。',
       '在零附近來回小小地調一下，圓點只是左右滑，高度幾乎不變；移到四分之一個磁通量子，再同樣小小地調，圓點就明顯地上下移動。',
       '接著把接面不對稱度拉到零點五，金色曲線馬上變得平緩，在半個磁通量子的地方不再掉到底；灰色那條，是原本兩個接面一樣大時的曲線。',
       '把磁通加到半個磁通量子，圓點只往下滑一段就停住；能調的範圍變小了，換來整條曲線比較不陡，對磁通雜訊也比較不敏感。'],
      actions=[(0, 0.1, FPS_FIX), (0, 0.2, ('slider', ASYM, 0)), (0, 0.3, ('slider', FLUX, 0)),
               (1, 0.3, SWEEP(FLUX, [(0, 0), (1, -0.08), (2.5, 0.08), (3.5, 0)])),
               (1, 5.0, SWEEP(FLUX, [(0, 0.25), (1, 0.17), (2.5, 0.33), (4, 0.17), (5.5, 0.25)])),
               (2, 2.8, ('slider', ASYM, 0.5)),
               (3, 0.5, SWEEP(FLUX, [(0, 0.25), (4, 0.5)]))],
      points=[('甜蜜點', '曲線是平的'), ('離開甜蜜點', '圓點上下移動'), ('不對稱接面', '範圍小、較不怕雜訊')], pmap=[0, 1, 2, 2], shot=(2, 8.0)),
 dict(key='chip', after=8, page='tr', hash='case', scene=S_CASE,
      title='動畫展示：用磁通把頻率往下調', sub='三維動畫：三顆可調 transmon 的晶片與頻率尺',
      sentences=[
       '換到傳輸子的三維動畫第六章，晶片上排著三顆十字形的位元，每顆下方都有兩個橘色小塊圍成的小迴路，旁邊經過一條控制線；上方看板左邊是干涉小圖，右邊是頻率尺。',
       '控制線送進電流，最左邊那顆位元的小迴路冒出銅色小箭頭，看板小圖上的青綠色圓點沿著曲線往下滑，頻率尺上同色的實線也往左移，代表頻率變低。',
       '剛才離開最高點的時候，那條實線一直微微抖動，這就是磁通雜訊造成的頻率抖動；控制線的電流關掉之後，圓點回到最高點，抖動也就消失了。'],
      actions=[(0, 0.3, ('id', 'c6auto')), (0, 10.0, ('sel', '#c6steps button:nth-child(2)'))],
      points=[('控制線送電流', '磁通穿過小迴路'), ('干涉小圖', '圓點往下滑'), ('頻率尺', '實線往左移、會抖動')], shot=(1, 6.0)),
])

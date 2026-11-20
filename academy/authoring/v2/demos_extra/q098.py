"""Q098 LC 與 JJ：線性和非線性的差別 — v2 動畫展示段（格式見 ../demos.py 的說明）。

頁面：animations/lc-vs-jj.html（PAGES 的 'lc'；二維 SVG 圖解，單欄捲動頁，沒有左側 #controls 面板）
  因為沒有 #controls，('click')／('slider')／('sweep') 都找不到控制項；本檔一律用 ('js', …)：
  直接改 <input type="range"> 的 value 並送出 input 事件（頁面以 addEventListener('input', drawN) 重畫）。
  每段第一個動作先 scrollIntoView 該 section，避免字型載入後版面位移。
  頁面沒有 App／requestAnimationFrame 動畫迴圈（只在滑桿 input 時重畫 SVG），所以不需要也不使用 FPS_FIX（App 不存在）。
  預設 colorScheme 為淺色：電感 --lc #1D6A8B（藍）、JJ --jj #B65C12（橘）、被打到 --hit #2C8A55（綠）、沒打到 --miss（灰）。
#s1（第 1 步）：滑桿 id=phi（−4.71～4.71，預設 0.6）。藍直線 I=φ、橘正弦 I=sin φ；藍點 (φ, φ)、橘點 (φ, sin φ)；灰色切線斜率 cos φ。
  縱軸只畫到 ±1.7，φ > 1.7 時藍點被裁掉（旁白不提藍點的末狀態）。
#s3（第 3 步）：滑桿 id=ratio（E_J/E_C，10～120，預設 50；E_C = 0.25 GHz 固定）。
  左圖拋物線六條能階、右側間距標籤全部相同（50 時 5.00）；右圖餘弦，間距 4.73、4.45、4.13、3.71、3.50（製作代理以同一哈密頓量重算）。
  井頂虛線在 2E_J，只有 2E_J < ymax = 4.9·√(8E_J E_C) 時才畫：50 時不畫；20 時井頂 10 GHz，第 5、6 條能階（10.28、14.35）在井頂以上，畫成虛線。
#s4（第 4 步）：fig4。LC 列一條綠線＋「0→1 = 1→2 = 2→3 = 3→4 全部重疊」「驅動一路往上爬」；Transmon 列四條線，只有 0→1 為綠色（|f−ω₀₁| < 0.02），其他灰色。
#s5（第 5 步）：fig5。橘實線 1−cos φ、藍虛線 φ²/2、灰點線 φ²/2−φ⁴/24、兩者之間陰影＋「四次項造成的差距」。靜態圖。
"""
LESSON = 'Q098'


class _Demos(list):
    def keys(self):
        return [LESSON]

    def items(self):
        return [(LESSON, list(self))]

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


def SCROLL(sec, smooth=False):
    beh = 'smooth' if smooth else 'instant'
    return ('js', f"document.getElementById('{sec}').scrollIntoView({{block:'start',behavior:'{beh}'}})")


def SET(rid, v):
    return ('js', f"(()=>{{const el=document.getElementById('{rid}');el.value={v};el.dispatchEvent(new Event('input'));}})()")


def SWEEP(rid, a, b, secs):
    """在頁面裡用 requestAnimationFrame 把滑桿從 a 拖到 b（秒數 secs），拖動中加黃色外框。"""
    return ('js', f"(()=>{{const el=document.getElementById('{rid}');const t0=performance.now();el.classList.add('qflash');"
                  f"const f=(now)=>{{const k=Math.min(1,(now-t0)/{int(secs * 1000)});el.value=({a}+({b}-({a}))*k).toFixed(2);"
                  f"el.dispatchEvent(new Event('input'));if(k<1)requestAnimationFrame(f);else el.classList.remove('qflash');}};"
                  f"requestAnimationFrame(f);}})()")


S_S1 = 'LC 與 JJ 圖解第 1 步：電流與磁通'
S_S3 = 'LC 與 JJ 圖解第 3 步：位能與量子能階'
S_S4 = 'LC 與 JJ 圖解第 4–5 步：微波驅動與泰勒展開'

DEMOS = _Demos([
 dict(key='tangent', after=4, page='lc', hash='s1', scene=S_S1,
      title='動畫展示：沿著正弦曲線走', sub='二維圖解：電流與磁通，直線和正弦',
      sentences=[
       '打開電感和約瑟夫森接面的圖解第一步，藍色直線是電感，橘色曲線是約瑟夫森接面，兩個圓點標出同一個相位上的電流。',
       '把相位從零慢慢往右拉，一開始兩個圓點幾乎疊在一起，接著橘色圓點落到藍色下方，灰色切線越來越平。',
       '拉到九十度，切線變成水平；再往右拉，橘色曲線往下彎，電流反而變小，這是普通電感絕對不會出現的事。'],
      actions=[(0, 0.1, SCROLL('s1')), (0, 0.3, SET('phi', 0.05)),
               (1, 0.5, SWEEP('phi', 0.05, 1.57, 8.0)),
               (2, 0.3, SET('phi', 1.57)), (2, 2.6, SWEEP('phi', 1.57, 2.6, 4.0))],
      points=[('相位很小', '兩點幾乎重疊'), ('九十度', '切線變水平'), ('超過九十度', '電流反而變小')], shot=(1, 8.0)),
 dict(key='levels', after=6, page='lc', hash='s3', scene=S_S3,
      title='動畫展示：拋物線和餘弦的能階', sub='二維圖解：位能井與數值算出的能階',
      sentences=[
       '翻到圖解第三步，左邊藍色拋物線裡的能階一格一格等距排好，旁邊標出的間距數字全部相同。',
       '右邊橘色的餘弦位能井越往上開口越寬，能階越擠，旁邊的間距數字一格比一格小。',
       '把下方的能量比值滑桿往左拉，橘色井口出現一條水平虛線，最上面的兩條能階冒出井口，也變成虛線。',
       '再拉回原來的位置，能階又全部回到井裡；左邊的拋物線不管怎麼拉，間距永遠相同。'],
      actions=[(0, 0.1, SCROLL('s3')), (0, 0.3, SET('ratio', 50)),
               (2, 1.0, SWEEP('ratio', 50, 20, 4.5)),
               (3, 0.4, SWEEP('ratio', 20, 50, 3.5))],
      points=[('拋物線', '能階等間距'), ('餘弦', '越往上越擠'), ('能量比值變小', '能階冒出井口')], pmap=[0, 1, 2, 2], shot=(2, 7.0)),
 dict(key='drive', after=7, page='lc', hash='s4', scene=S_S4,
      title='動畫展示：微波只打到零和一', sub='二維圖解：躍遷頻率與四次項',
      sentences=[
       '再往下到第四步，上面一列是電感電容電路，所有躍遷的綠線疊成同一條，旁邊寫著全部重疊、驅動一路往上爬。',
       '下面一列是傳輸子，四條躍遷線彼此錯開，只有對準零到一的那一條是綠色，其他都是灰色。',
       '接著看第五步，橘色實線是真正的餘弦，藍色虛線是只留二次項的拋物線，兩者之間的陰影，就是四次項造成的差距。'],
      actions=[(0, 0.1, SCROLL('s4')), (2, 0.2, SCROLL('s5', smooth=True))],
      points=[('電感電容電路', '躍遷全部重疊'), ('傳輸子', '只打到零到一'), ('四次項', '位能比拋物線低')], shot=(1, 4.0)),
])

"""Q063 快在哪？加速的等級 — v2 動畫展示段（格式見 ../demos.py 的說明）。

皆已讀原始碼確認，並以 1600×900 Chromium（swiftshader）截圖確認畫面位置（/home/user/qwork/q063shots/）。
三段都只用按鈕或滑桿（立即生效、同步計算），旁白描述動作後停住的讀數與柱子，不描述過渡。

- op#grover：animations/js/operation/09_grover.js。
  ui.slider「量子位元數 n」2–6（第 44 行，改值會 setup() 重建，N = 64 時 64 根柱子，場景不重，用 slider 不用 sweep）。
  ui.button「② Oracle」「③ 擴散」（第 48–49 行，同步；Oracle 只在 phase ≠ oracle 時做，擴散只在 phase = oracle 時做，所以交替按不會重複）、
  「測量」「重設」（第 53–54 行）。左邊面板最下方 readout（第 89–90 行）：
  截圖 n2.png「N = 4，第 0 輪／答案的機率 P = 0.250／最佳輪數 ≈ (π/4)√N ≈ 1　古典平均要查 2 次」；
  n4.png「N = 16…≈ 3　古典平均要查 8 次」；n6.png「N = 64…≈ 6　古典平均要查 32 次」；
  k6.png（交替按六次）「N = 64，第 6 輪／答案的機率 P = 0.997　其他每個 = 0.0001」，答案柱高高立起、其他振幅為負，貼平成藍色（第 38 行）；
  meas.png「測量結果：… ✓ 找到了」。注意 setup 會把 mark 夾成 min(mark, N−1)：第一段調到 n = 2 後答案變成 3，所以旁白不說第一段的答案號碼；
  第三段是新頁面，直接設 n = 6，答案維持預設 11。「測量」用 Math.random，第三段把它在同步 click 期間固定為 0.5 → 量到 11
  （/home/user/qwork/q063calc/checks.py 照抄第 41、53 行重算：累積機率到 11 才超過 0.5）。
  Q001 的 grover 段看的是 N = 16、三輪超過九成、多一輪轉過頭；本課改看滑桿 n 與「最佳輪數 vs 古典次數」讀數（平方級），以及 N = 64 六輪後只讀出一個號碼（輸出瓶頸），不重複。
- tr#shor：animations/transmon-3d.html 第 8 章（第 958–966 行）。「自動接續」#g8auto 預設勾選（第 963 行），第一個動作先關掉；
  步驟按鈕在 #g8steps，由 G8STEPS 產生（第 1118–1119 行，按鈕文字 1–8，沒有 id），所以用 ('sel', '#g8steps button:nth-child(k)')；
  g8Step（第 2009 行）同步換掉右側 #g8title／#g8body。截圖 tr3a.png：右側「③ 模指數：一次算出所有 f(x)，產生糾纏」，
  說明最後一段「這一步是整個演算法最花資源的部分…閘數約 n³」；tr5a.png：「⑤ 量子傅立葉轉換：梳子 → 尖峰」，
  最後一段「只要約 n² 個閘；古典 FFT 處理 2ⁿ 個點要約 n·2ⁿ 步。指數級加速就來自這裡。」（第 1966 行）；
  tr6a.png：步驟 6 的 setup 直接把長條設成 QFT 後的狀態（g8Set("qft")），0、4、8、12 四根 ±0.50（金、紅），其他貼平。
  左上角字幕（capEl）依場景時間跳出、會變動，旁白不描述它。Q061、Q062 只用 op#shor，沒有用過 transmon 第 8 章。
"""
LESSON = 'Q063'


class _Demos(list):
    """清單（demos.py 的載入方式），同時也能用 DEMOS['Q063'] 取用。"""

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)

    def get(self, k, default=None):
        return list(self) if k == LESSON else default

    def keys(self):
        return [LESSON]

    def values(self):
        return [list(self)]

    def items(self):
        return [(LESSON, list(self))]


_N = '量子位元數 n'
_OR, _DF = ('click', '②'), ('click', '③')
_MEASURE = ('js', "(()=>{const R=Math.random;Math.random=()=>0.5;try{const b=window.__btn('測量');window.__flash(b);b.click();}"
                  "finally{Math.random=R;}})()")


def _step(k):
    return ('sel', f'#g8steps button:nth-child({k})')


def _rounds(start, n=6, gap=0.5):
    """從句內 start 秒起，交替按 Oracle、擴散 n 輪。"""
    out = []
    for i in range(n):
        out.append((start + 2 * i * gap, _OR))
        out.append((start + (2 * i + 1) * gap, _DF))
    return out


DEMOS = _Demos([
 dict(key='scale', after=5, page='op', hash='grover', scene='3D 場景 9：Grover 搜尋（量子位元數 2、4、6）',
      title='動畫展示：抽屜變多，輪數只多一點', sub='三維動畫：格羅弗搜尋——最佳輪數和古典次數',
      sentences=[
       '打開操作動畫的格羅弗搜尋場景，左邊面板最下方的讀數，會同時寫出量子的最佳輪數，和古典平均要查幾次。',
       '把量子位元數調成二，只有四個抽屜：讀數寫著最佳一輪，古典平均查兩次，幾乎沒有差別。',
       '調成四，十六個抽屜，最佳三輪對八次；再調成六，六十四個抽屜，最佳六輪對三十二次。',
       '抽屜多了十六倍，古典次數也多十六倍，量子輪數卻只從一輪變成六輪，大約跟著抽屜數的平方根增加。'],
      actions=[(1, 1.6, ('slider', _N, 2)), (2, 0.4, ('slider', _N, 4)), (2, 4.6, ('slider', _N, 6))],
      points=[('四個抽屜', '一輪對兩次'), ('六十四個抽屜', '六輪對三十二次'), ('平方級', '跟著平方根增加')], shot=(3, 3.0)),
 dict(key='exp', after=6, page='tr', hash='shor', scene='transmon 3D 第 8 章：Shor 演算法（模指數、QFT、量測）',
      title='動畫展示：指數級從哪裡來', sub='三維動畫：秀爾演算法——量子傅立葉轉換的閘數',
      sentences=[
       '換到超導量子位元三維動畫的第八章秀爾演算法，先把右邊的自動接續關掉，改用步驟按鈕一步一步看。',
       '按第三步模指數，右邊說明寫著：這是整個演算法最花資源的一步，閘數大約是位元數的三次方。',
       '按第五步量子傅立葉轉換，右邊最後一段寫著：量子只要大約位元數平方個閘，古典處理同樣多的點，步數跟著二的次方暴增。',
       '再按第六步，四根高柱子立在零、四、八、十二，其他都貼平了；有週期這種結構，干涉才換得到指數級加速。'],
      actions=[(0, 0.3, ('id', 'g8auto')), (1, 0.5, _step(3)), (2, 0.5, _step(5)), (3, 0.4, _step(6))],
      points=[('模指數', '閘數約位元數三次方'), ('量子傅立葉轉換', '約位元數平方個閘'), ('有週期結構', '才有指數級加速')], shot=(2, 8.0)),
 dict(key='output', after=8, page='op', hash='grover', scene='3D 場景 9：Grover 搜尋（六十四個抽屜，量測一次）',
      title='動畫展示：算完了，只讀到一個號碼', sub='三維動畫：格羅弗搜尋——輸出只有幾個位元',
      sentences=[
       '回到格羅弗搜尋場景，把量子位元數調成六，六十四個抽屜，讀數寫著最佳六輪。',
       '接著連做六輪標記加擴散：答案那根柱子高高立起，其他都貼平了，讀數寫著答案的機率是零點九九七。',
       '按測量，讀數最後一行寫著測量結果十一，找到了；我們拿到的，也就只是一個六位元的號碼。',
       '六十四個振幅的細節都讀不出來；所以好的量子演算法，答案本身就要很短，像這裡只要一個號碼。'],
      actions=[(0, 1.0, ('slider', _N, 6))] + [(1, t, a) for t, a in _rounds(0.6, gap=0.4)] + [(2, 0.3, _MEASURE)],
      points=[('六十四個抽屜', '最佳六輪'), ('六輪之後', '機率零點九九七'), ('量一次', '只讀到一個號碼')], shot=(2, 6.0)),
])

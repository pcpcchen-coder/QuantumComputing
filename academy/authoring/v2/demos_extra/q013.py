"""Q013 格羅弗搜尋：16 個抽屜找寶藏 — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（皆讀原始碼確認）：
- animations/operation.html#grover：js/operation/09_grover.js（App.register id 'grover'，第 3 行）。
  預設 n = 4（N = 16）、答案 mark = 11（第 15 行）；答案柱底有綠色發光框 0x66ffcc、柱頂標籤「答案」（第 26、31 行）；
  柱子下方編號 0–15（labelFn String(i)，第 23 行）；N > 16 時每列 8 根（cols，第 22 行），N = 64 即 8×8。
  柱高 = 振幅；正振幅 0xe0a54a（橘）、負振幅 0x4f8cff（藍）（第 38 行）；
  粉紅色平均面 0xff6bd5 只在做完 Oracle、還沒擴散時顯示（第 29、85 行）。
  滑桿「量子位元數 n」2–6（第 44 行）；按鈕「② Oracle」「③ 擴散」「完整一輪」（第 48–50 行，完整一輪 = Oracle 後 700 毫秒擴散）、
  「自動跑到最佳次數」（第 52 行：先 setup() 重設，之後每 0.8 秒做半步，k ≥ kOpt 停）、「測量」「重設」（第 53–54 行）。
  kOpt = max(1, round(π/(4θ) − 0.5))：N = 16 為 3、N = 64 為 6（第 43 行）。
  讀數在左側面板 #controls 內（ui.readout，第 55 行；operation.html 的 #panel 在左邊，css/style.css 第 32 行）：
  「N = …，第 k 輪」「答案的機率 P = …」「最佳輪數 ≈ (π/4)√N ≈ …　古典平均要查 N/2 次」（第 89–90 行）。
  右下插圖（#inset-wrap，css/style.css 第 56 行）：左邊幾何圖、右邊「P(成功) vs 輪數」曲線，目前輪數畫白點（第 58–79 行）。
- 面板內容較多，max-height 為 100vh − 96px 且可捲動；每段開頭先把 #panel 捲到底，讓按鈕與讀數入鏡（待試錄確認）。

以與 09_grover.js 相同的算法實算（grover_rounds.py）：
- N = 16：第 1 輪寶藏 0.6875（P 0.473）、其他 0.1875；第 3 輪 P 0.961；第 4 輪寶藏 0.763（P 0.582）、其他 −0.167（藍色、朝下）；第 5 輪 P 0.125。
- N = 64：第 6 輪 P 0.997。
"""

LESSON = 'Q013'

_PANEL = "document.getElementById('panel').scrollTop=1e5;"

_LIST = [
 dict(key='round', after=5, page='op', hash='grover', scene='3D 場景 9：Grover 搜尋——振幅放大',
      title='動畫展示：一輪兩步', sub='三維動畫：格羅弗搜尋——標記和擴散',
      sentences=[
       '打開三維動畫的格羅弗搜尋場景，十六根柱子代表十六個抽屜，頭上標著答案的第十一號，就是藏寶藏的抽屜。',
       '先按神諭，也就是做標記，寶藏那根柱子翻到下面，變成藍色，同時出現一片粉紅色的平面，那就是所有柱子的平均高度。',
       '再按擴散，每根柱子都以剛才那片粉紅色平面當鏡子翻過去：寶藏那根一下子被拉到最高，其他柱子都矮了一點。',
       '看左邊面板的讀數，寶藏的機率從十六分之一升到零點四七左右，這樣就完成了一輪。'],
      actions=[(0, 0.1, ('js', _PANEL)), (0, 0.3, ('click', '重設')),
               (1, 1.0, ('click', '② Oracle')), (2, 1.0, ('click', '③ 擴散'))],
      points=[('按標記', '寶藏翻到下面'), ('粉紅色平面', '所有柱子的平均'), ('按擴散', '寶藏被拉到最高')],
      shot=(2, 5.0)),
 dict(key='overshoot', after=8, page='op', hash='grover', scene='3D 場景 9：Grover 搜尋——振幅放大',
      title='動畫展示：轉過頭了', sub='三維動畫：格羅弗搜尋——多做幾輪會怎樣',
      sentences=[
       '回到格羅弗搜尋，按自動跑到最佳次數，動畫會從頭開始，一輪接一輪地做，到第三輪就自己停下來。',
       '這時讀數上寶藏的機率大約零點九六；右下角小圖的白點，也停在曲線的最高點附近。',
       '如果不停手，再按一次完整一輪：寶藏那根反而變矮，機率掉到不到六成，其他柱子的藍色部分也往下伸得更長。',
       '再做一輪，機率只剩一成多，白點又沿著曲線往下掉了一大截，這就是轉過頭。'],
      actions=[(0, 0.1, ('js', _PANEL)), (0, 1.8, ('click', '自動跑到最佳次數')),
               (2, 2.2, ('click', '完整一輪')), (3, 0.6, ('click', '完整一輪'))],
      points=[('第三輪', '機率約九成六'), ('第四輪', '掉到不到六成'), ('第五輪', '只剩一成多')],
      shot=(2, 6.5)),
 dict(key='sixtyfour', after=10, page='op', hash='grover', scene='3D 場景 9：Grover 搜尋——振幅放大',
      title='動畫展示：六十四個抽屜', sub='三維動畫：格羅弗搜尋——量子位元數調到六',
      sentences=[
       '改造題也能在三維動畫裡驗證：把量子位元數的滑桿調到六，抽屜就變成六十四個，排成八乘八的方陣。',
       '先在紙上寫下預測，再按自動跑到最佳次數，看動畫一輪一輪把寶藏拉高。',
       '左邊的讀數寫著，最佳輪數大約是六，古典方法平均要查三十二次。',
       '跑完第六輪，寶藏的機率接近百分之百；把動畫的結果和你的預測比一比，猜對了就在結果表上打個勾。'],
      actions=[(0, 0.1, ('js', _PANEL)), (0, 4.3, ('slider', '量子位元數 n', 6)),
               (1, 2.4, ('click', '自動跑到最佳次數'))],
      points=[('調到六', '六十四個抽屜'), ('最佳輪數', '大約六輪'), ('第六輪', '接近百分之百')],
      shot=(3, 2.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q013'] 取用。"""

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


DEMOS = _Demos(_LIST)

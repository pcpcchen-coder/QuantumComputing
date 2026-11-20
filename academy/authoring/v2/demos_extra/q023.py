"""Q023 約瑟夫森接面：超導三明治 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都用課綱指定的 index.html#jj（demos.PAGES['jj']；js/scenes/03_jj.js，App.register id 'jj'，第 3 行；index.html 第 42 行載入）。
控制項由 core.js ui.slider／ui.radio 放進 #controls（core.js 第 339–370 行）；record_demo.js 的 'click' 用
#controls button 的 textContent.trim().startsWith 找按鈕（record_demo.js 第 26 行）。每段都是新開頁面，從預設 I = 0.5 Ic 開始。

03_jj.js 對照（行號）：
- 第 17–25 行：左右兩塊鋁電極 W = 4.6（銀灰 0xb9c4d4 金屬），右側半透明 opacity 0.3＋淺色邊線（第 21–23 行）；
  中間阻障厚 0.16、顏色 0xff7a59（橘紅）、opacity 0.85（第 24 行）。
- 第 26–28 行標籤：「超導體 Al（電極 1）· 相位 φ₁」「超導體 Al（電極 2）· 相位 φ₂」、金色「AlOx 穿隧阻障 ~1–2 nm」（位置 [0, −1.25, 1.5]，在阻障下方前側）。
- 第 30–38 行相位鐘：左 x = −2.3 藍 0x4f8cff、右 x = +2.3 紅 0xff5a5f；第 102–103 行左指針轉 −phi1（每秒 0.8 弧度），右指針轉 −(phi1 + phi)。
- 第 39、105 行：金色大字（class 'big gold'，[0, 3.2, 0]）「φ = φ₂ − φ₁ = 30°　I = Ic sin φ = 0.50 Ic」，角度 toFixed(0)。
- 第 42–52 行：26 對 Cooper pair，每對一顆 0x6fb4ff（藍）一顆 0x9d7bff（紫）；第 108–113 行以 1.6·flow 往 +x 移動、到右端繞回左端。
  （相機在 [7.5, 5.5, 11.5]，+x 在畫面右方；左電極不透明，電子對只在右側半透明電極裡看得到。）
- 第 54–58、115–121 行：電子對中心 |x| < 0.05 且速度 > 0.05 時，在阻障處亮一顆 0xffe08a（淡黃）閃光，約 0.4 秒淡出、同時變大。
- 第 66–69 行：iBias 預設 0.5；滑桿「偏壓電流 I / Ic」0–1.6；互斥按鈕三顆（同一列，依序）「I = 0.5 Ic（超電流）」「I ≈ Ic」（0.98）「I = 1.4 Ic（電壓態）」，
  按下即 sl.set(v)（core.js 第 345–352 行）。
- 第 92–96 行：I ≤ Ic 時相位差以 min(1, dt·4) 的比例趨向 asin(I/Ic)：0.5 → 30°；0.98 → 78.5°（金字顯示 79°），約 1 秒內收斂。
- 第 97–100 行：I > Ic（電壓態）時 phi 每秒增加 6·√(I² − 1)：1.4 → 每秒 5.88 弧度（約每秒 0.94 圈；dt 上限 0.05，畫格率低時會變慢），
  flow = 0.6 + 0.4 sin φ；右指針相對左指針一直轉、金字角度一直變。
- 第 123–125 行讀數框（#controls 最後一個元素，下方還有面板的操作提示 .hint）：
  I ≤ Ic「超電流態：φ = arcsin(I/Ic) = 30.0°／電壓為零，能量不耗散」；I > Ic「電壓態：相位差持續旋轉 → 電流以 2eV/h 振盪／同時出現準粒子（電阻性）電流 → 有耗散」。
- 第 73–87 行右下小圖「電流–相位關係 I = Ic sin φ 與 I–V 特性」：左半金色正弦 sin φ（0–2π）、青色點 #38c6d9 在 (φ, sin φ)；
  右半金色直線 V = 0、I 0→1（超電流分支），灰色曲線 v < 1 時 0.03v、之後斜率 0.78（電阻分支）；青色點：I ≤ Ic 在 (0, I)，I = 1.4 時在 V = 1 + 1.37/0.78 ≈ 2.76、I = 1.4（右上的斜線上）。
- 第 64、106 行的青色電壓標籤（[6.5, −1.4, 0]）以 1600×900 視窗估算投影約在 (1474, 709)，落在右下小圖（#inset-wrap，z-index 4）範圍內、可能被蓋住，旁白不提它（待試錄確認）。
- 每段開頭把 #panel 捲到底（css/style.css 第 32 行面板 max-height 100vh − 96px、可捲動），讓按鈕與讀數框入鏡；旁白不提捲動。
"""

LESSON = 'Q023'

# 錄影時把閃光球改成不寫深度、最後繪製，避免它淡出後擋住半透明的阻障（動畫原始碼未修改）
_PANEL = ("document.getElementById('panel').scrollTop=1e5;"
          "App.scene.traverse(function(o){if(o.isMesh&&o.material&&o.material.color&&o.material.color.getHex()===0xffe08a)"
          "{o.material.depthWrite=false;o.material.depthTest=false;o.renderOrder=10;}});")
_SCENE = 'JJ 與微波讀取 3D 場景 3：約瑟夫森接面（JJ）的結構與穿隧'

_LIST = [
 dict(key='sandwich', after=4, page='jj', hash='jj', scene=_SCENE,
      title='動畫展示：超導三明治的三層', sub='三維動畫：兩塊鋁、一層氧化鋁、穿過去的電子對',
      sentences=[
       '打開約瑟夫森接面的三維動畫場景：左右兩塊銀色的方塊是兩片超導的鋁，右邊那塊畫成半透明，讓我們看得到裡面。',
       '中間夾著一層橘紅色的薄片，下方的金色標籤寫著穿隧阻障，大約一到兩奈米，也就是今天說的絕緣層。',
       '藍色和紫色的小球兩兩一組，代表庫柏電子對，它們一路往右流，經過中間那層時會亮起一個小小的黃色光點。',
       '要記得，這一閃只是動畫的示意：真正的穿隧沒有在牆上打洞，而是電子對的波滲過薄薄的絕緣層，和另一邊的波接上。'],
      actions=[(0, 0.1, ('js', _PANEL))],
      points=[('兩塊銀色方塊', '兩片超導的鋁'), ('橘紅色薄片', '絕緣層約一到兩奈米'), ('黃色光點', '只是示意，不是挖洞')],
      pmap=[0, 1, 2, 2], shot=(2, 4.0)),
 dict(key='dc', after=6, page='jj', hash='jj', scene=_SCENE,
      title='動畫展示：零電壓也有電流', sub='三維動畫：偏壓電流與相位差（直流約瑟夫森效應）',
      sentences=[
       '回到同一個場景，偏壓電流現在停在臨界電流的一半，上方金色的字寫著相位差三十度。',
       '按下第二顆按鈕，把電流加到接近臨界電流，金色的字已經變成七十九度左右，兩根指針也差得更開了。',
       '面板下方的讀數框寫著超電流態，電壓為零，能量不耗散；沒有加電壓，電流照樣穿過接面。',
       '右下角小圖的左半邊是正弦曲線，青色的點停在接近頂端的地方；頂端就是臨界電流，電流再大，相位差就鎖不住了。'],
      actions=[(0, 0.1, ('js', _PANEL)), (1, 1.2, ('click', 'I ≈ Ic'))],
      points=[('電流一半', '相位差三十度'), ('接近臨界電流', '約七十九度，電壓仍是零'), ('小圖的點', '停在正弦頂端附近')],
      pmap=[0, 1, 1, 2], shot=(2, 3.0)),
 dict(key='ac', after=7, page='jj', hash='jj', scene=_SCENE,
      title='動畫展示：有了電壓，相位一直轉', sub='三維動畫：電壓態與相位鐘（交流約瑟夫森效應）',
      sentences=[
       '這次直接按下寫著電壓態的按鈕，把電流加到臨界電流的一點四倍，超過了臨界電流。',
       '右邊紅色相位鐘的指針轉得比左邊藍色的快，一圈一圈把它甩開，金色字裡的相位差數字也一直在變。',
       '面板下方的讀數框也已經是電壓態：相位差持續旋轉，電流跟著振盪，同時出現電阻性的電流，有了耗散。',
       '右下角小圖的右半邊，青色的點已經不在電壓為零的那條直線上，而是落在右邊的斜線上；有了電壓，相位就一直轉，這就是交流約瑟夫森效應。'],
      actions=[(0, 0.1, ('js', _PANEL)), (0, 2.2, ('click', 'I = 1.4'))],
      points=[('按電壓態', '電流是一點四倍'), ('相位差', '一直轉下去'), ('小圖的點', '落在右邊斜線上')],
      pmap=[0, 1, 1, 2], shot=(1, 4.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q023'] 取用。"""

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

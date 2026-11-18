# Q109 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw），revision id 取自 MediaWiki API（prop=revisions）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Surface code（Wikipedia，oldid=1380986407）

- 「The '''surface code''' is a topological quantum error correcting code, and an example of a stabilizer code, defined on a two-dimensional spin lattice. The first type of surface code introduced by Alexei Kitaev in 1997 was the '''toric code''', which gets its name from its periodic boundary conditions」（連結標記已去除）
- 「When p is low, this will create sparsely distributed pairs of anyons which have not moved far from their point of creation. Correction can be achieved by identifying the pairs that the anyons were created in (up to an equivalence class), and then re-annihilating them to remove the errors.」
- 「This gives a threshold probability, under which the error correction will almost certainly succeed. Through a mapping to the random-bond Ising model, this critical probability has been found to be around 11%.」（獨立位元／相位翻轉、量測完美的模型；與動畫簡化模型門檻約 10–15% 同一量級）
- 「These thresholds are upper limits and are useless unless efficient algorithms are found to achieve them. The most well-used algorithm is minimum weight perfect matching.」
- 「The most important characteristic of such an open boundary is that a Pauli X error no longer necessarily flips two plaquette stabilizers. An edge on the boundary only has one adjacent plaquette, and thus an X error on the corresponding qubit will only flip a single B_p」（邊界上的錯誤只亮一個）
- 「A distance-d rotated planar code has d² physical qubits」「the d² qubits are located on the ''vertices'' of a d × d square lattice, and both Z and X stabilizers are located on the plaquettes of this rotated lattice, with the two types in a checkerboard pattern. Furthermore, some weight-2 Z (resp. X) stabilizers exist on the left and right (resp. top and bottom) boundaries of the lattice」（d² 顆資料位元；穩定子各需一顆量測位元，合計 2d² − 1）
- 「As of 2025, Google Quantum AI has implemented the rotated planar code for up to code distance 7 on their newest generation of superconducting quantum processors, Willow, demonstrating a logical error suppression factor Λ slightly larger than 2 when the code distance is increased by 2, indicating below-threshold behavior.」

## Quantum error correction（Wikipedia，oldid=1384638817）

- 「In quantum channels, however, the no-cloning theorem prevents copying an unknown qubit, seemingly posing an obstacle to quantum error correction. This challenge is overcome by encoding the logical information of a single qubit into a highly entangled state of multiple physical qubits.」
- 「the '''three-qubit bit-flip code''', first proposed by Asher Peres in 1985, uses entanglement and syndrome measurements to correct errors」
- 「while this procedure perfectly corrects the output when zero or one flips are introduced by the channel, if more than one qubit is flipped then the output is not properly corrected. For example, if the first and second qubits are flipped, then the syndrome measurement gives the outcome P_3, and the third qubit is flipped, instead of the first two.」（兩個錯誤騙過解碼器的最小例子）

## Threshold theorem（Wikipedia，oldid=1360742213）

- 「the '''threshold theorem''' (or '''quantum fault-tolerance theorem''') states that a quantum computer with a physical error rate below a certain threshold can, through application of quantum error correction schemes, suppress the logical error rate to arbitrarily low levels.」
- 「Current estimates put the threshold for the surface code on the order of 1%」

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 11 課

- 「最好的雙位元閘錯誤率約 10⁻³；破解 RSA-2048 要上億到數十億個閘，等於每個閘要 10⁻¹² 左右。差九個數量級，只能**用很多實體位元組成一顆邏輯位元**，一邊算一邊抓錯修錯。」
- 障礙表：「不可複製定理｜未知量子態不能複製三份｜用**糾纏**分散資訊」「一量就塌縮｜直接量資料會毀掉疊加｜只量位元之間的**奇偶**」「錯誤是連續的｜可能只偏 0.01 弧度｜量奇偶把小偏差**離散化**成「有錯／沒錯」」；「兩種錯誤都要抓：**X（位元翻轉）**與 **Z（相位翻轉，古典沒有）**」。
- 重複碼表：「同｜同｜沒錯」「異｜同｜第 1 顆翻」「異｜異｜第 2 顆翻」「同｜異｜第 3 顆翻」；「|000⟩ 和 |111⟩ 的奇偶一樣，所以量到的資訊**和 α、β 無關**，疊加完整保留。量奇偶就是把資料位元用 CNOT「加總 mod 2」到輔助位元」。
- 「9 顆資料位元 3×3，格子中間與邊上放 8 顆量測位元，共 **17 顆**（一般 2d² − 1）。[Z] 方塊量 4 顆的 Z 奇偶抓 X 錯誤；[X] 方塊抓 Z 錯誤；邊界只量 2 顆。**每個量測位元只和上下左右鄰居互動**，正好對應超導 2D 方格。」
- 「D5 的 X 錯誤 → 兩個 [Z] 方塊亮」「D1 的 X 錯誤 → 只亮一個 → 錯誤串另一端在邊界」「Y = X 和 Z 同時，兩組都亮」「**邏輯錯誤**：錯誤排成一整條連通鏈、橫跨晶片」「可修 ⌊(d−1)/2⌋ 個錯誤」。
- 「**一個週期（約 1 μs）**：重設量測位元 → 4 層 CZ（N／Z 字形順序，避免一個錯誤擴散成兩個）→ 中途 QND 量測 → 和上一輪比較得到**偵測事件** → 重複；看「時間 × 空間」的 3D 圖。」
- 「**解碼器**：最小權重完美匹配（MWPM）把偵測事件兩兩配對或配到邊界；必須**即時**（FPGA／ASIC／GPU）；修正多半只記在軟體（**Pauli frame**）」。
- 「**ε_L ≈ A·(p/p_th)^((d+1)/2)**，p_th 約 1%。p < p_th 時 d 每加 2，邏輯錯誤率除以固定倍數 Λ；p > p_th 時碼越大越糟。」「2024（2025 刊於 Nature）｜Google Willow：d = 3/5/7，**Λ ≈ 2.1**」。

## 學程內部簡報

- slides/transmon.pptx 第 24 頁（課綱寫 p25；p25 實為「Lattice surgery 與魔術態蒸餾」，故改引 p24）：「量子錯誤更正：表面碼」「① 結構　17 顆實體位元存 1 顆邏輯位元：資訊分散在糾纏態裡，不是複製。」「② 一個週期　約 1 μs：量測位元與鄰居做 CZ，再讀出穩定子的奇偶。」「⑤ 邊界　落單的亮點配到邊界上。」「⑥ 邏輯錯誤　d = 3 只能修 1 個錯；兩個錯誤可能騙過解碼器。」「⑦ 碼距與閾值　d = 5、7 需 49、97 顆（2d² − 1）；實體錯誤率低於約 1% 時，碼距越大越可靠。」
- slides/QC_Operation_Talk.pptx 第 49 頁：「難題　不能複製量子態，也不能直接量資料（會塌縮）」「奇偶改變 = 症狀；量子資訊本身不被讀取」「解碼器（古典電腦，需即時）把症狀配對 → 推測錯誤鏈 → 修正」「碼距 d：可修正 ⌊(d−1)/2⌋ 個錯誤；錯誤鏈貫穿整片才會造成邏輯錯誤」；備註「紅球；再量測穩定子，亮起橘色柱子的就是症狀；再解碼，綠線是解碼器推測的錯誤鏈」。
- 第 50 頁：「實體錯誤率 p 低於門檻 pth（表面碼 ~1%）時，碼距每加 2，邏輯錯誤率乘上 1/Λ」「高於門檻：越大的碼反而越差」「d = 3 → 5 → 7，Λ ≈ 2.14」；備註「右下插圖是即時蒙地卡羅模擬的結果：三條線是 d = 3、5、7，在實體錯誤率低時，d 越大越好；在大約 10% 左右三條線交叉——這是本場景簡化模型（只有資料錯誤、沒有量測錯誤）的門檻，真實電路層級的雜訊下門檻約 1%。」「d = 3、5、7 的邏輯錯誤率每次大約減半」。

## 互動動畫程式

- animations/transmon-3d.html 第 10 章（CH id: "surface"）：圖例「圓球＝資料位元（紅 X 錯誤、藍 Z 錯誤、紫 Y 錯誤）；小方塊＝量測位元；青色格子＝Z 穩定子（抓 X 錯誤）、琥珀色格子＝X 穩定子（抓 Z 錯誤）；格子亮起＝該穩定子量到 −1；白線＝解碼器的配對」。
- codeStruct(3)：Z 穩定子 = 內部 {D1,D2,D4,D5}、{D5,D6,D8,D9}、左邊界 {D4,D7}、右邊界 {D3,D6}；X 穩定子 = 內部 {D2,D3,D5,D6}、{D4,D5,D7,D8}、上邊界 {D1,D2}、下邊界 {D8,D9}。註解「互動順序：Z 穩定子走 N 字形（左上→左下→右上→右下），X 穩定子走 Z 字形（左上→右上→左下→右下）」。
- 步驟 ⑥ cue：「D1、D4 在同一個青色格子裡，兩個翻轉互相抵消，它沒亮；只有左邊界的半圓（含 D4、D7）亮了。」「解碼器只看到一個亮點，最省的解釋是「D7 錯了一個」，於是在 D7 補 X。」「結果 D1、D4、D7 整行都是 X：所有穩定子都不亮，但這正好是邏輯 X」。
- 自由實驗：「點畫面上的資料位元（圓球）注入錯誤：每點一次依序是 X → Z → Y → 清除」；按鈕 `#g10dec`「解碼並修正」、`#g10rnd`「隨機錯誤」、`#g10clr`「清除錯誤」、`#g10mc`「跑 300 次統計」、`data-d10`「3（17 顆）」「5（49 顆）」「7（97 顆）」；面板 `#g10lit`「青色 n 個、琥珀色 n 個」、`#g10res`「成功：錯誤已修正 ✓」或「邏輯錯誤！（邏輯 X）」；邏輯錯誤時 `logTag10` 紅字掛在方格上方。注入只能經 stage 的 pointerdown／pointerup＋Raycaster（`cur === 9 && g10S.free && !g10S.dec`）。
- 解碼器說明：「最小權重完美匹配（亮點 ≤ 14 個時以動態規劃精確求解，更多時改用貪婪法），X、Z 兩類錯誤分開解碼。自由實驗的統計用簡化雜訊模型（只有資料位元以機率 p 發生 X/Y/Z 錯誤、量測完美），閾值約 10–15%；真實電路（閘與量測也會錯）的閾值約 1%。」
- animations/js/operation/11_qec.js：`let d = 5, p = 0.05 … auto = true`；標籤「邏輯量子位元：d = 5，25 資料 + 24 量測 = 49 實體量子位元」、「上邊界」「下邊界」；stepCycle：「① 發生隨機錯誤（紅球）」「② 量測穩定子：亮起的方塊 = 症狀」「③ 解碼：配對 n 個症狀（綠線 = 推測的錯誤鏈）」「④ 修正…」；自動循環每 0.9 秒一階段；滑桿「實體錯誤率 p（每個資料量子位元）」0.005–0.2；插圖「邏輯錯誤率 vs 實體錯誤率（即時蒙地卡羅）」，DS = [3, 5, 7]、每點 1000 次、顏色 '#4f8cff'、'#e0a54a'、'#ff5a5f'，虛線「未編碼 = p」，白色直線畫在目前的 p；desc「本場景只示範 X 錯誤、不含量測錯誤，解碼器為最小權重配對」。

## 製作代理試拍（2026-11-18，單張截圖，非正式錄影、非 QV2_DRY，nice -n 19）

- #surface 步驟 8：用 js 在 #stage 送 PointerEvent（720, 615）→ D5 變紅、左上與右下青色格子亮，面板「青色 2 個、琥珀色 0 個」；按 #g10dec 後約 1.6 秒畫面有白色配對線，之後「最近一次解碼」為「成功：錯誤已修正 ✓」。
- 同上點 (583, 543)、(578, 613)（D1、D4）：面板「青色 1 個、琥珀色 0 個」，只亮左邊界半圓；解碼後 D1、D4、D7 皆紅，方格上方紅字「邏輯錯誤！（邏輯 X）」，面板「青色 0 個、琥珀色 0 個」。
- operation.html#qec：載入後插圖三條線完成；低錯誤率處紅線（d = 7）在最下、藍線（d = 3）最高；滑桿設 0.15 後顯示「15.0%」，白色直線移到 15%，三條線在右側擠在一起、與「未編碼 = p」虛線差不多高。蒙地卡羅有隨機性，旁白不念數值。
- 機器負載高時第 10 章動畫的步驟時間比牆鐘慢（試拍時約 0.4–0.7 倍），因此展示段改用自由實驗（注入與解碼都由按鍵觸發），不依賴步驟腳本的 cue 時間。

## 實跑紀錄（surface_d3.py，Python 3.13.18，無外部套件，無亂數）

```
一、單一錯誤（9 種）
  錯誤 D1 → 亮：左上（內部） → 修正 D1 → 成功 ✓
  錯誤 D2 → 亮：左上（內部） → 修正 D1 → 成功 ✓
  錯誤 D3 → 亮：右邊界半圓 → 修正 D3 → 成功 ✓
  錯誤 D4 → 亮：左上（內部）、左邊界半圓 → 修正 D4 → 成功 ✓
  錯誤 D5 → 亮：左上（內部）、右下（內部） → 修正 D5 → 成功 ✓
  錯誤 D6 → 亮：右下（內部）、右邊界半圓 → 修正 D6 → 成功 ✓
  錯誤 D7 → 亮：左邊界半圓 → 修正 D7 → 成功 ✓
  錯誤 D8 → 亮：右下（內部） → 修正 D8 → 成功 ✓
  錯誤 D9 → 亮：右下（內部） → 修正 D8 → 成功 ✓
二、兩個錯誤（36 種）中，騙過解碼器的：
  錯誤 D1、D4 → 亮：左邊界半圓 → 修正 D7 → 邏輯錯誤 ✗（剩下 D1、D4、D7）
  錯誤 D1、D5 → 亮：右下（內部） → 修正 D8 → 邏輯錯誤 ✗（剩下 D1、D5、D8）
  錯誤 D1、D7 → 亮：左上（內部）、左邊界半圓 → 修正 D4 → 邏輯錯誤 ✗（剩下 D1、D4、D7）
  錯誤 D1、D8 → 亮：左上（內部）、右下（內部） → 修正 D5 → 邏輯錯誤 ✗（剩下 D1、D5、D8）
  錯誤 D1、D9 → 亮：左上（內部）、右下（內部） → 修正 D5 → 邏輯錯誤 ✗（剩下 D1、D5、D9）
  錯誤 D2、D4 → 亮：左邊界半圓 → 修正 D7 → 邏輯錯誤 ✗（剩下 D2、D4、D7）
  錯誤 D2、D5 → 亮：右下（內部） → 修正 D8 → 邏輯錯誤 ✗（剩下 D2、D5、D8）
  錯誤 D2、D7 → 亮：左上（內部）、左邊界半圓 → 修正 D4 → 邏輯錯誤 ✗（剩下 D2、D4、D7）
  錯誤 D2、D8 → 亮：左上（內部）、右下（內部） → 修正 D5 → 邏輯錯誤 ✗（剩下 D2、D5、D8）
  錯誤 D2、D9 → 亮：左上（內部）、右下（內部） → 修正 D5 → 邏輯錯誤 ✗（剩下 D2、D5、D9）
  錯誤 D3、D6 → 亮：右下（內部） → 修正 D8 → 邏輯錯誤 ✗（剩下 D3、D6、D8）
  錯誤 D3、D8 → 亮：右下（內部）、右邊界半圓 → 修正 D6 → 邏輯錯誤 ✗（剩下 D3、D6、D8）
  錯誤 D3、D9 → 亮：右下（內部）、右邊界半圓 → 修正 D6 → 邏輯錯誤 ✗（剩下 D3、D6、D9）
  錯誤 D4、D7 → 亮：左上（內部） → 修正 D1 → 邏輯錯誤 ✗（剩下 D1、D4、D7）
  錯誤 D5、D8 → 亮：左上（內部） → 修正 D1 → 邏輯錯誤 ✗（剩下 D1、D5、D8）
  錯誤 D5、D9 → 亮：左上（內部） → 修正 D1 → 邏輯錯誤 ✗（剩下 D1、D5、D9）
  錯誤 D6、D8 → 亮：右邊界半圓 → 修正 D3 → 邏輯錯誤 ✗（剩下 D3、D6、D8）
  錯誤 D6、D9 → 亮：右邊界半圓 → 修正 D3 → 邏輯錯誤 ✗（剩下 D3、D6、D9）
  共 18 種會造成邏輯錯誤，18 種修得好
三、每顆資料位元以機率 p 翻轉時，邏輯錯誤率（512 種情況全部加總，不用亂數）
  p =    1%  →  邏輯錯誤率   0.17%  （比不編碼好）
  p =    5%  →  邏輯錯誤率   3.69%  （比不編碼好）
  p =   10%  →  邏輯錯誤率  11.97%  （比不編碼還糟）
  p =   20%  →  邏輯錯誤率  30.84%  （比不編碼還糟）
  p =   30%  →  邏輯錯誤率  43.85%  （比不編碼還糟）
四、我的實驗：
  錯誤 D1、D4 → 亮：左邊界半圓 → 修正 D7 → 邏輯錯誤 ✗（剩下 D1、D4、D7）
```

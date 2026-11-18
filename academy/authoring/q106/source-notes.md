# Q106 來源筆記（逐字引文）

查核日：2026-11-18。Bell state 頁由製作代理用 MediaWiki API 直接讀取原始 wikitext（含 revision id）；Quantum entanglement 與 Grover's algorithm 兩頁因 API 限流，改用網頁讀取（WebFetch），revision id 取自頁面的永久連結。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Bell state（Wikipedia，oldid=1365950086，原始 wikitext）

- 「the '''Bell's states''' or '''EPR pairs''' are specific [[quantum states]] of two [[qubits]] that represent the simplest examples of [[quantum entanglement]].」
- 「These mechanisms cannot transmit [[information]] faster than the speed of light, a result known as the [[no-communication theorem]].」
- 「If Alice measured her qubit in the standard basis, the outcome would be either 0 or 1, each with probability 1/2; if Bob (subscript "B") also measured his qubit, the outcome would be the same as for Alice. Thus, Alice and Bob would each seemingly have random outcome. Through communication they would discover that, although their outcomes separately seemed random, these were perfectly correlated.」
- 「Thus, quantum theory violates the Bell inequality and the idea of local "hidden variables".」

## Quantum entanglement（Wikipedia，oldid=1383454028，網頁讀取）

- 定義：糾纏是「the quantum state of each particle in a group cannot be described independently of the state of the others」（句子後續未摘）。
- 2022 諾貝爾物理獎頒給 Aspect、Clauser、Zeilinger，「for experiments with entangled photons, establishing the violation of Bell inequalities」（句子後續未摘）。
- 糾纏「cannot be used for faster-than-light communication」（部分句）。

## Grover's algorithm（Wikipedia，oldid=1385418712，網頁讀取）

- 「It was devised by Indian-American computer scientist Lov Grover in 1996.」
- 演算法「finds with high probability the unique input to a black box function that produces a particular output value」，並稱為相對古典做法的平方加速（網頁轉文字時 √ 符號遺失，讀到的是「O(N)」，以原頁數學式 O(√N) 為準）。
- 「The earliest time that we get a near-optimal measurement is therefore r≈πN/4.」（同上，轉文字時 √ 遺失；即 r ≈ (π/4)√N）
- 「subsequent iterations rotate the state vector away from |ω⟩, reducing the probability of obtaining the correct answer.」
- 維基頁沒有直接寫「N = 4 一輪剛好 100%」；本集這一點依學程師生對話紀錄、兩個動畫與 grover_bars.py 實跑。

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 8 課

- 「兩顆各自疊加時，(a|0⟩+b|1⟩)⊗(c|0⟩+d|1⟩) = ac|00⟩+ad|01⟩+bc|10⟩+bd|11⟩，所以乘積態一定滿足 **a₀₀ × a₁₁ = a₀₁ × a₁₀**；不成立就拆不開，這就是**糾纏**。」
- 步驟表：「1｜H⊗H｜+½ +½ +½ +½｜¼ = ¼ 乘積態」「2｜**CZ**｜+½ +½ +½ **−½**｜−¼ ≠ ¼ **糾纏**」「3｜Q2 再 H｜1/√2 0 0 1/√2｜Bell 態」。
- 「CZ 只翻 |11⟩ 的號，機率都沒變，但已經拆不開。」
- 「Bell 態量 1000 次：00 約 500、11 約 500。單看一顆完全隨機，一起看永遠相同。**和古典相關性的差別**：換成任何角度的基底量都仍相關，相關程度隨角度變化的方式違反 **Bell 不等式**（2022 諾貝爾獎）。糾纏**不能超光速傳訊**：單看一邊永遠 50/50。」
- Grover：「步驟 2 oracle：00 +½ 01 +½ 10 −½ 11 +½ ← 答案被挖成洞，機率仍各 25%（此刻糾纏）」「步驟 3 擴散：平均 = ¼；新振幅 = 2×平均 − 原振幅　00 0 01 0 10 1 11 0」。
- 「Oracle（標記 10）｜X(Q2) → **CZ** → X(Q2)｜先翻 Q2，CZ 的負號就落在 |10⟩」。
- 「重點是**認出答案比找出答案容易**」；「約 (π/4)√N 次…是**平方加速**。每次迭代朝答案轉 2θ（sin θ = 1/√N）；N = 4 剛好一次到 90°，N 更大時**轉過頭機率反而下降**。」
- 課後練習 3 答案：「轉過頭，四個結果回到各 25%。」

## 學程內部簡報

- slides/transmon.pptx 第 22 頁：「振幅長條：糾纏、Grover 與 Deutsch」「① 糾纏　CZ 只把 |11⟩ 翻成負號，a₀₀·a₁₁ ≠ a₀₁·a₁₀，就拆不回兩顆各自的狀態。」「②–⑤ Grover　Oracle 把答案的振幅翻負，擴散「對平均值翻轉」，四選一只查詢一次就找到 10。」「⑥ 轉過頭　多做一次 Oracle＋擴散，振幅又回到各 25%。」
- slides/output/basic-circuits.pptx 第 10–11 頁：Bell 態「各自隨機、彼此一致，而且無法拆成兩顆位元各自的狀態：這就是 糾纏」；振幅逐步 +1 → +1/√2、+1/√2 → |00⟩、|11⟩ 各 +1/√2。
- 第 23–24 頁：「① H：均勻疊加　4 個答案各 25%」「② 標記（Oracle）　Oracle 認得答案 |11⟩，只把它的振幅變成負的；機率不變」「③ 擴散　新振幅 = 2 × 平均 − a」「2 × ¼ − ½ = 0；2 × ¼ − (−½) = 1 → 100%」「比平均高的翻下來、比平均低的翻上去：被標記成負的答案離平均最遠，翻得最高」。

## 互動動畫程式

- animations/transmon-3d.html 第 7 章（id: grover）：html「長條高度是振幅（可正可負，負的是紅色），機率是振幅的平方。上方電路圖高亮的是正在送的閘…步驟 1 講糾纏、2–6 講 Grover 搜尋、7 講 Deutsch，8 是自由實驗。」；按鈕 `#g7prev`、`#g7play`（暫停／播放／再看一次）、`#g7re`「重播」、`#g7next`、`#g7auto`「自動接續」、步驟按鈕 `#g7steps` 1–8；面板 `#g7p1`、`#g7p2`、`#g7ent`、`#g7hist`（量測結果）。
- 3D 標籤：長條上方「±0.50 ・ 25%」（負的標紅）；右邊「a₀₀·a₁₁ = …」「a₀₁·a₁₀ = …」「→ 乘積態」或「→ 糾纏（C = …）」；「平均 ±0.25」金色；「★ 答案」金色標在答案長條下方（step > 0 且有答案時）。
- 步驟 1 cues（dur 36）：0.3 說明；4.5「兩顆都做 H…四個振幅都變成 +½」；9.5 乘積態；13.5「送 CZ…只有 |11⟩ 翻成負號」；18「a₀₀·a₁₁ = −¼ ≠ a₀₁·a₁₀ = ¼…（C = 1）」；23「Q2 再做一次 H：得到 Bell 態」；27.5「量測 40 次…只會出現 00 或 11」。
- 步驟 3（Oracle，answer = 2 即 10）cues：0.3 X(Q2)；5 CZ；9.5 X(Q2)「負號從 |11⟩ 移到 |10⟩」；14.5「此刻兩顆位元是糾纏的」。步驟 4：0.3 平均線「(½ + ½ − ½ + ½)/4 = ¼」；5 擴散 Dg（g7Apply：a → 2m − a）。步驟 5：0.3「量測 50 次…結果都是 10」。
- 步驟 6「轉過頭」：從 [0, 0, 1, 0] 做 Og(2) 再 Dg，g7Apply 的結果是 [−½, −½, +½, −½]；字幕寫「四個振幅都變成 −½」與實際長條不同（答案那根是 +½、金色），機率各 25% 的結論不變。本集旁白與展示都沒有用這句字幕。
- 步驟 8 自由實驗：答案按鈕 00／01／10／11；H₁、H₂、X₁、X₂、CZ、Oracle、擴散；「一鍵 Grover」「量測 50 次」「重設 |00⟩」。
- animations/basic-circuits.html 範例 grover：選項「位元數」（2 顆（N = 4）／3 顆（N = 8））、「答案（q1 q0，點一下切換）」預設 11、「答案（q2 q1 q0…）」預設 101、「重複輪數」（最佳／1 輪／2 輪／3 輪）；best = 2 位元 1 輪、3 位元 2 輪；擴散 BLK kind diff 照理想 2m − a 計算；改選項 rebuild(false) 停在最後一步、go() 會清除量測；「量測 1,000 次」每 30 ms 40 次。

## 實跑紀錄（grover_bars.py，Python 3.13.18，無外部套件）

```
== Bell 態：兩顆哈達瑪閘 → 受控相位翻轉 → Q2 再一個哈達瑪閘 ==
起點      00:+1.00 ▇▇▇▇▇▇▇▇  01:+0.00           10:+0.00           11:+0.00         
H⊗H       00:+0.50 ▇▇▇▇      01:+0.50 ▇▇▇▇      10:+0.50 ▇▇▇▇      11:+0.50 ▇▇▇▇    
    a00·a11 = +0.25，a01·a10 = +0.25 → 乘積態
CZ        00:+0.50 ▇▇▇▇      01:+0.50 ▇▇▇▇      10:+0.50 ▇▇▇▇      11:−0.50 ▇▇▇▇    
    a00·a11 = −0.25，a01·a10 = +0.25 → 糾纏
H(Q2)     00:+0.71 ▇▇▇▇▇▇    01:+0.00           10:+0.00           11:+0.71 ▇▇▇▇▇▇  
    a00·a11 = +0.50，a01·a10 = +0.00 → 糾纏

== 兩位元 Grover，答案 = 10 ==
H⊗H       00:+0.50 ▇▇▇▇      01:+0.50 ▇▇▇▇      10:+0.50 ▇▇▇▇      11:+0.50 ▇▇▇▇    
標記      00:+0.50 ▇▇▇▇      01:+0.50 ▇▇▇▇      10:−0.50 ▇▇▇▇      11:+0.50 ▇▇▇▇    
    平均 = +0.25
擴散      00:+0.00           01:+0.00           10:+1.00 ▇▇▇▇▇▇▇▇  11:+0.00         
    一輪後：量到 10 的機率 100.0 %
第二輪    00:−0.50 ▇▇▇▇      01:−0.50 ▇▇▇▇      10:+0.50 ▇▇▇▇      11:−0.50 ▇▇▇▇    
    兩輪後：量到 10 的機率 25.0 %（轉過頭）

== 位元多了：答案的機率（%）==
位元  選項   1 輪    2 輪    3 輪    4 輪
  2     4   100.0    25.0    25.0   100.0
  3     8    78.1    94.5    33.0     1.2
  4    16    47.3    90.8    96.1    58.2
```

- 把 `ANSWER` 改成 `'01'` 再跑：標記後 01 為 −0.50、平均 +0.25；一輪後 01 = +1.00，「一輪後：量到 01 的機率 100.0 %」；兩輪後 25.0 %。（classroom.py 建置時兩種答案都會實跑並比對。）

## 製作代理試拍（2026-11-18，單張截圖，非正式錄影）

- transmon-3d.html#grover（1600×900）：取消自動接續、按步驟 1、按暫停、1.5 秒後按播放；CZ 之後長條 |11⟩ 變紅「−0.50 · 25%」，右邊「a₀₀·a₁₁ = −0.250」「a₀₁·a₁₀ = +0.250」「→ 糾纏（C = 1.00）」；H(Q2) 與量 40 次後長條 00、11 為「+0.71 · 50%」，面板量測結果 00 = 21、11 = 19、01 = 10 = 0（隨機）。面板捲動後步驟按鈕仍在畫面內。
- 同頁按步驟 4：金色平均線與「平均 +0.25」，擴散後 |10⟩「+1.00 · 100%」、其他「+0.00 · 0%」，|10⟩ 下方「★ 答案」，判定回到乘積態。
- basic-circuits.html#grover（zoom 0.62）：切 q0 → 答案 10，最後一步 |10⟩ +1.000、100%，量 1,000 次全部 10、「→ 找到答案 ✓」；切 3 顆（N = 8）：答案 101、最佳 2 輪 +.972、94.5%，量 1,000 次 101 有 948 次、其他各 3–12 次；選 3 輪：101 掉到 +.575、33%，其他 −.309、9.6%，說明寫「轉過頭了」。

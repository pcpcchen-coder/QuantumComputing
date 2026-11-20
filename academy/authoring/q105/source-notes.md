# Q105 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理透過 MediaWiki API 直接讀取原始 wikitext（revision id 取自 API 回應）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Bernstein–Vazirani algorithm（Wikipedia，oldid=1371471620）

- 「The '''Bernstein–Vazirani algorithm''', which solves the '''Bernstein–Vazirani problem''', is a [[quantum algorithm]] invented by Ethan Bernstein and [[Umesh Vazirani]] in 1997.」
- 「Given an oracle that implements a function f: {0,1}ⁿ → {0,1} in which f(x) is promised to be the dot product between x and a secret string s ∈ {0,1}ⁿ modulo 2, f(x) = x·s = x₁s₁ ⊕ x₂s₂ ⊕ ⋯ ⊕ xₙsₙ, find s.」（數學式由 <math> 轉寫）
- 「Classically, the most efficient method to find the secret string is by evaluating the function n times with the input values x = 2ⁱ for all i ∈ {0, 1, …, n−1}」
- 「In contrast to the classical solution which needs at least n queries of the function to find s, only one query is needed using quantum computing.」
- 「Apply a Hadamard transform to the n qubit state |0⟩^⊗n … Next, apply the oracle U_f which transforms |x⟩ → (−1)^f(x)|x⟩. This can be simulated through the standard oracle that transforms |b⟩|x⟩ → |b ⊕ f(x)⟩|x⟩ by applying this oracle to (|0⟩ − |1⟩)/√2 |x⟩.」
- 「Another Hadamard transform is applied to each qubit which makes it so that for qubits where sᵢ = 1, its state is converted from |−⟩ to |1⟩ and for qubits where sᵢ = 0, its state is converted from |+⟩ to |0⟩.」
- 「Since s ⊕ y = 0 is only true when s = y, this means that the only non-zero amplitude is on |s⟩.」

## Gottesman–Knill theorem（Wikipedia，oldid=1354309521）

- 「stabilizer circuits—circuits that only consist of gates from the normalizer of the qubit Pauli group, also called Clifford group—can be perfectly simulated in polynomial time on a probabilistic classical computer. The Clifford group can be generated solely by using the controlled NOT, Hadamard, and phase gates (CNOT, H and S)」
- （BV 電路只用 H、Z（= S²）與 CNOT，屬於 Clifford 電路；transmon-3d.html 第 11 章原文亦寫「第 7 章的 Bell、Grover、Deutsch 和第 9 章的 BV 全都是 Clifford 電路，這就是它們能被古典模擬的原因」。）

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 7 課

- 學生提問：「當量子位元被設定好之後，他會穩定一段時間叫做 T₁……例如有三個量子位元，經過我的設定是 010，那我讀取也是 010……那疊加態要做啥？」
- 「**① T₁ 不是「穩定期」，而是「衰減的時間常數」。** |1⟩ 的機率從一開始就照 e^(−t/T₁) 往下掉；T₁ ≈ 100 μs 表示 100 μs 後只剩約 37%。」
- 「**② 不是「在 T₁ 內讀很多次」，而是「整個流程重跑很多次」。** 量測會塌縮，讀一次就結束。每個 **shot** = 重設到 |000⟩ → 跑完電路 → 讀一次；重複 1000–10000 個 shot 才得到分布。」
- 「「設定 010、讀出 010」只是古典位元。量子電腦的能力來自三件事一起作用」：疊加（n 顆位元同時帶著 2ⁿ 個振幅）、相位（每個振幅有正負）、干涉（再做一次閘，讓錯的答案抵消、對的答案加強）。
- 「**光有疊加沒用**：直接量均勻疊加態只會隨機得到一個答案。演算法的工作是**設計干涉**。」
- 「黑盒子藏著 s = 101，輸入 x 回答 s·x 的奇偶。古典要問 3 次（100、010、001），量子**只問 1 次**。」
- 八振幅表：「1 H⊗3｜+ + + + + + + +｜每個 1/√8；量測各 12.5%」「2 查詢一次｜+ − + − − + − +｜x₁+x₃ 為奇數的翻負號；**機率仍各 12.5%**」「3 再 H⊗3｜0 0 0 0 0 1 0 0｜只有 101 的 8 項全同號」。
- 「y = 101 時全部同號 → 1；其他 y 都是 4 正 4 負 → 0。」
- 「實機：6 個 H（約 100 ns）＋讀取約 1 μs；1000 shot 中 101 約 95% 以上，其他零星出現。」
- 「注意：BV 只用到疊加和干涉，**沒有用到糾纏**，古典電腦其實也能有效模擬」。

## 學程內部簡報

- slides/transmon.pptx 第 23 頁「BV：3 顆位元一次猜中密碼」：「① 題目　黑盒子藏 3 位元密碼 s，只回答 s·x 的奇偶；古典要問 3 次（n 位元問 n 次）。」「③ 查詢一次　|x⟩ → (−1)^(s·x)|x⟩，答案寫進正負號。」「④ 干涉　再做一次 H，除了 |s⟩ 以外全部抵消。」「⑥ 真實硬體　6 個 H（20–50 ns）＋虛擬 Z，約 100 ns，遠短於 T₁；讀取約 1 μs 後主動重設。」
- 第 18 頁十二章一覽：「▶ 3D 第 9 章：BV 密碼 | p23 | BV：3 顆位元一次猜中密碼」。（課綱寫 p24；p24 實為「量子錯誤更正：表面碼」，故改引 p23。）
- slides/output/basic-circuits.pptx 第 21 頁「範例 7｜BV：查一次讀出整串密碼」：「① 輔助 q3 翻成 1」「② 全部 H　q0–q2 同時代表 8 種輸入；q3 變成 |−⟩」「③ 黑盒：密碼 s = 101　q0、q2 各接一條 CNOT 到 q3；每個輸入帶上 (−1)s·x」「④ 再做 H、量測　q2 q1 q0 = 101：正好就是密碼」。
- 第 22 頁「振幅逐步看」：「8 種輸入振幅都是 1/(2√2) ≈ 0.35」「s·x 為奇數的輸入多一個負號：機率仍各 12.5%」「只剩 101：機率 100%」。

## 互動動畫程式

- animations/transmon-3d.html 第 9 章（id: bv，「BV 密碼」）：G9STEPS 八步「題目與古典做法、均勻疊加、查詢黑盒子、干涉、量測、真實硬體、標準版與重點、自由實驗」；步驟按鈕 `#g9steps`、`#g9auto`「自動接續」。
- 第 8 步自由實驗 extra：密碼按鈕 `data-s9="0"…"7"`（000…111）與「隨機（隱藏）」（`data-s9="hide"`，capShow「已隨機藏好一個 3 位元密碼…」）；「① H⊗3」「② 黑盒子」「③ H⊗3」「④ 量測 50 次」（`data-op9`）；`#g9run`「一鍵執行」、`#g9cq`「古典查詢一次」、`#g9reset`「重設」、`#g9noise`「讀取雜訊」（每顆 3%）。
- classicalQuery()：依序問 100、010、001，看板加一行「古典第 k 次：x = … → 回答 …（所以 s 的第 k 位是 …）」；字幕「古典已查詢 N 次，還沒拼出完整密碼。」／「古典問了 3 次才拼出 s = …；量子只要 1 次。」
- 量測揭曉字幕：「量測最多的是 …（50/50 次）；密碼揭曉：s = …，猜中 ✓。量子只查詢了 1 次。」面板 `#g9q`「量子 N 次 ／ 古典 M 次」、`#g9s` 隱藏時顯示「？？？（隱藏）」。
- 長條顏色：負振幅 RED、正振幅 COL.gold；標籤「+0.35 ・ 12.5%」。動畫時間 D9 = { H3: 1.6, Z: 0.9, O: 1.4 } 秒；量測每秒 20 次。
- animations/basic-circuits.html 範例 7（id: bv）：「Bernstein–Vazirani：查一次就猜中密碼」；選項「密碼 s（s2 s1 s0，點一下切換）」預設 101；步驟「X 閘：輔助位元準備成 |1⟩」「H 閘：全部疊加」「黑盒：計算 s·x（只查詢這一次）」「H 閘：干涉讀出密碼」；verdict「→ 密碼 s = …」；按鈕 `#bNext`「下一步 ▶」、`#m1000`「量測 1,000 次」、`#mClear`「清除」；正振幅 --pos（藍）、負振幅 --neg（橘）。

## 製作代理試拍（2026-11-18，單張截圖，非正式錄影）

- tr#bv 第 8 步、密碼 101：①後八根皆「+0.35 ・ 12.5%」；②後 001、011、100、110 為紅色「−0.35 ・ 12.5%」，看板 q1、q3 出現 Z；③④後只剩 101「+1.00 ・ 100%」，統計 101 = 50/50，字幕「量測最多的是 101（50/50 次），猜中 ✓。量子只查詢了 1 次。」
- tr#bv 隱藏對決：三次古典查詢後字幕「古典問了 3 次才拼出 s = 110；量子只要 1 次。」；一鍵執行後「…密碼揭曉：s = 110，猜中 ✓…」，面板「量子 1 次 ／ 古典 3 次」（密碼為隨機，每次不同）。
- bc#bv：四步後只剩 0101（藍、朝上）與 1101（橘、朝下）；量測 1,000 次「最近一次：101」「→ 密碼 s = 101」；改成 110 後 CNOT 移到 q1、q2，結果 110。

## 實跑紀錄（bv_duel.py，Python 3.13.18，無外部套件，SEED = 7）

```
密碼 s = 101（3 位元）
古典第 1 次：問 x = 100 → 回答 1
古典第 2 次：問 x = 010 → 回答 0
古典第 3 次：問 x = 001 → 回答 1
古典查詢 3 次 → 拼出 s = 101
① H 之後：   000:+0.354  001:+0.354  010:+0.354  011:+0.354  100:+0.354  101:+0.354  110:+0.354  111:+0.354
② 查詢 1 次： 000:+0.354  001:-0.354  010:+0.354  011:-0.354  100:-0.354  101:+0.354  110:-0.354  111:+0.354
③ 再 H 之後： 000:+0.000  001:+0.000  010:+0.000  011:+0.000  100:+0.000  101:+1.000  110:+0.000  111:+0.000
量測 1000 次（每顆位元讀錯 3%）：101 914 次、111 29 次、001 29 次、100 26 次
最多的是 101（91.4%）→ 猜中
查詢次數：古典 3 次，量子 1 次
```

改造試跑：SECRET = '110' → 110 出現 914 次；SECRET = '011010' → 古典 6 次、量子 1 次，011010 出現 831 次（83.1%）；NOISE = 0.0 → 101 出現 1000 次。

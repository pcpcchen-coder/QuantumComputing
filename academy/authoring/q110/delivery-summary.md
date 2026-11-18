這是依課綱製作的課前教學版，不是實際上課錄音。

父子科技學院量子電腦學程第一百一十堂（超導量子電腦師生對話第 12 課）：表面碼把邏輯位元存好了，要怎麼對它做運算？Clifford 運算靠 lattice surgery 縫合與拆開補丁，真正帶來量子優勢的 T 閘，則要消耗事先蒸餾好的魔術態。

這一集會學到
・為什麼不能直接送脈衝：橫向閘的限制（Eastin–Knill）、Clifford 電路可被古典模擬（Gottesman–Knill）
・邏輯閘價目表：Pauli 幾乎免費、聯合量測約 d μs、Clifford 數倍、T 閘最貴
・lattice surgery：準備接縫 → 合併量 d 輪 → 拆開；個別結果隨機，乘積是 X_A ⊗ X_B
・三次聯合量測做出邏輯 CNOT；T 閘傳送：一顆魔術態，一半機率補一個 S
・15-to-1 蒸餾：15 顆進、1 顆出，錯誤率約 35p³（程式實算：3 顆出錯的 455 種排列中 35 種騙過檢查）
・限制：容錯時代的成本主要在 T 閘與魔術態工廠

主要來源：本學程「超導量子電腦師生對話教學紀錄」第 12 課、Transmon 筆記簡報第 25 頁、transmon-3d.html 第 11 章；維基百科 Lattice surgery、Magic state distillation、Gottesman–Knill theorem、Eastin–Knill theorem、Clifford gate；本機 magic_budget.py 實跑紀錄。

教材用法（classroom.zip）
先讀「00_爸爸先讀」，照「01_操作步驟」打開 transmon-3d.html#surgery，依序看合併、拆開、CNOT，再到自由實驗跑蒸餾統計；列印包有邏輯閘資源估算表、蒸餾實驗紀錄表、容易錯的地方與工程答辯檢核表。課堂 120 分鐘另計。

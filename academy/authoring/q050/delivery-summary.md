這是依課綱製作的課前教學版，不是實際上課錄音。

父子科技學院量子電腦學程第五十堂：初始化與校準。每一輪計算開始前，量子位元要怎麼回到零？量子閘要怎麼調，才能剛好轉對角度？

這一集會學到
・初始化：每個 shot 都要回到 |0⟩；等效溫度約 50 mK 時，5 GHz 的量子位元約 0.8% 停在 |1⟩
・被動重置（等約 5 T₁，數百 μs）和主動重置（量測＋回饋，約 1–5 μs）的差別
・九步校準：讀取腔頻譜、量子位元頻譜、Rabi、Ramsey、T₁／T₂、DRAG 精修、讀取最佳化、兩位元閘、基準測試
・校準結果存進校準資料庫；參數會漂移，雲端系統每天甚至每幾小時重新校準
・依賴關係決定先後順序：少做一步，哪個結果會出錯

主要來源：本學程「如何操作量子電腦」簡報第 13–15 頁；互動動畫 peripherals.html#bringup、operation.html#pulse、transmon-3d.html 第 5 章；維基百科 Rabi cycle、Ramsey interferometry、Randomized benchmarking、Calibration、Topological sorting。

教材用法（classroom.zip）
先讀「00_爸爸先讀」，照「01_操作步驟」用動畫認識重置與校準；列印包有九張校準卡、校準流程卡、重置比較表與少一步預測卡。課堂 120 分鐘另計。

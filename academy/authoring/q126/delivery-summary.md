這是依課綱製作的課前教學版，不是實際上課錄音。

父子科技學院量子電腦學程第一百二十六堂：加入雜訊——八個範例在真實世界會怎樣。同一條線路跑兩次，一次理想、一次加上雜訊模型，把兩份直方圖並排成「理想 vs 雜訊比較圖」，看貝爾態、GHZ 態、Grover 的答案怎麼變差，再把雜訊一路加倍，找出最先撐不住的範例。

這一集會學到
・雜訊模型的三個旋鈕：單位元閘、雙位元閘、讀取（今天的 1%、2%、3% 是假設值）
・錯誤預算：做對的機會連乘起來，閘越多越吃虧
・Bell → GHZ → Grover：閘越多，跑掉的比例越大；讀錯一顆最常見
・看不出來的雜訊：量子硬幣被打亂還是一半一半；隱形傳態往一半靠攏
・容易錯：雜訊模型是假設，參數要寫清楚；統計誤差不是雜訊
・把雜訊加倍：最先跑掉一半的範例，以及零雜訊外插

主要來源：維基百科 Fault injection、Quantum depolarizing channel、Noisy intermediate-scale quantum computing；本學程「如何操作量子電腦」簡報第 47、48、32 頁，以及 operation.html 場景 6「量子線路」、transmon-3d.html 第 9 章、basic-circuits.html 範例 4 互動動畫；本機 Python 與 Qiskit 2.6.2、qiskit-aer 0.18.4 實跑紀錄。

教材用法（classroom.zip）
先讀「00_爸爸先讀」，照「01_操作步驟」在 operation.html#circuit 開關雜訊，再執行 noise_lab.py（或開 雜訊模型.ipynb，需 pip install qiskit qiskit-aer）畫比較圖；下半場改 MY_SCALE 把雜訊加倍，填雜訊加倍紀錄表。沒有 Qiskit 時用 page_noise.py（只要 Python 3）。課堂 120 分鐘另計。

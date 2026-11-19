這是依課綱製作的課前教學版，不是實際上課錄音。

父子科技學院量子電腦學程第一百二十四堂：用 Qiskit 重現八個範例。把「量子電路入門」互動動畫八個範例頁底部的 Qiskit 程式碼搬到自己的電腦，每個範例用 Statevector 與 shots 各跑一次，和頁面的理論機率逐格比對，八格全勾才發布八範例 notebook v1.0。

這一集會學到
・程式從哪裡來：每個範例頁底部的程式碼區塊，會跟著選項改變
・兩種跑法：Statevector 算理論機率（要和頁面一模一樣），shots 量 1000 次（只會接近）
・八個範例的預設理論機率：疊加、干涉、Bell、GHZ、隱形傳態、Deutsch、BV、Grover
・實跑結果：預設 8／8 一致；74 種選項組合機率 74／74 一致；Grover 奇數輪振幅差一個整體負號
・容易錯：measure_all 的紀錄叫 meas、固定種子讓次數重複、shots 會跳動別只看圖
・動手：八範例 notebook、qiskit-aer 重跑、改成自己的參數再比對

主要來源：維基百科 Qiskit、Project Jupyter；本學程「量子電路入門：八個範例」簡報第 28–29 頁、「如何操作量子電腦」簡報第 27–28 頁，以及 basic-circuits.html 互動動畫與其程式碼產生器；本機 Qiskit 2.6.2、qiskit-aer 0.18.4 實跑紀錄。

教材用法（classroom.zip）
先讀「00_爸爸先讀」，安裝 qiskit 與 qiskit-aer，開啟「八範例.ipynb」（或執行 eight_examples.py），照「01_操作步驟」逐格跑並填八格檢查表；沒有 Qiskit 時先用 check_eight.py 對答案。下半場用列印包第 3 頁把一個範例改成自己的參數再比對。課堂 120 分鐘另計。

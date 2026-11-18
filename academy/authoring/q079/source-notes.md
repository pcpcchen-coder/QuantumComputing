# Q079 來源筆記（逐字引文）

查核日：2026-11-18。學程沒有拓樸量子位元與 NV 色心的簡報或場景；以下維基百科引文由製作代理以 WebFetch 讀取（經摘要工具回傳的逐字片段）。

## Wikipedia: Topological quantum computer

- 「The unitary operation corresponding to exchanging anyons depends only on the topology of the braid.」
- 「such perturbations do not alter the topological properties of the braids」；資訊「is impervious to small errors in the trajectories」
- 「It was proposed by Russian-American physicist Alexei Kitaev in 1997.」
- 非阿貝爾任意子「a species required for topological quantum computers, have yet to be experimentally confirmed」
- 2018 年孤立馬約拉納粒子的宣稱「was retracted in 2021」；2021 年的後續指出「the data in the 2018 paper was incomplete and misrepresented the results」
- 2025 年微軟發表 Majorana 1，「claiming partial evidence of topological behaviour」

## Wikipedia: Majorana 1

- 2025 年 2 月（引用日期 2025-02-19）發表；「The device can fit eight qubits.」；topoconductor 為 indium arsenide 與 aluminum
- 論文作者：measurements「do not, by themselves, determine whether the low-energy states detected by interferometry are topological」

## Wikipedia: Toric code

- 表面碼是「a topological quantum error correcting code」；第一個表面碼是 Kitaev 1997 年提出的 toric code
- 平面碼：非平凡路徑連接相對的邊界，最短長度為 d（碼距）

## Wikipedia: Topology

- 「a topologist cannot distinguish a coffee mug from a doughnut」

## Wikipedia: Nitrogen-vacancy center

- 「It consists of a nearest-neighbor pair of a nitrogen atom, which substitutes for a carbon atom, and a lattice vacancy.」
- spin-dependent photoluminescence「enables measurement of the electronic spin state」；「enables optical spin-polarization, which initializes the quantum state of a qubit」
- 「relatively long spin coherence at room temperature, lasting up to milliseconds」
- 「NV centers emit bright red light … if excited off-resonantly by visible green light」
- 「NV centers enable nanoscale measurements of magnetic and electric fields」；「enable the implementation of quantum algorithms and networks」；「explored for applications in quantum computing」

## animations/js/operation/11_qec.js

- subtitle：「用很多實體量子位元編碼 1 個邏輯量子位元；只量『奇偶』不量資料」
- desc：「如果剩下的錯誤剛好形成一條『由上貫穿到下』的鏈，就是邏輯錯誤。」
- 控制項：`ui.radio([[3, 'd = 3'], [5, 'd = 5'], [7, 'd = 7']] …)`、`ui.slider('實體錯誤率 p（每個資料量子位元）', 0.005, 0.2, 0.005, p …)`、`ui.toggle('自動循環', auto …)`、`ui.button('下一步' …)`
- stepCycle：① 發生隨機錯誤（紅球）→ ② 量測穩定子（亮起的方塊 = 症狀）→ ③ 解碼（綠線）→ ④ 修正

## 學程內部

- academy/lessons/Q078/brief.md：半導體自旋量子位元，「認識量子點、電子自旋與 CMOS 製程的關係」
- academy/lessons/Q080/brief.md：平台大比較與供電分析，「從時間尺度、連接性、錯誤率、設施、供電比較各平台」
- docs/量子電腦學院_課程擴充規劃.md：Q079 列為「◆ 新簡報；★ 編織（braiding）示意場景」，平台原本缺拓樸與 NV 色心

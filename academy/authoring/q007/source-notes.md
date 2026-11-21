# Q007 來源筆記（逐字引文）

查核日：2026-11-18。維基百科三頁由製作代理開啟並取得逐字引文。學程內部簡報與 3D 場景程式由製作代理讀取；數字由製作代理用 2ⁿ × 16 位元組重算。

## Quantum computing（Wikipedia，oldid=1385829008）

- 「this makes it challenging for a classical computer to simulate a quantum one」
- 「representing a 100-qubit system requires storing 2^100 classical values.」
- 「When a qubit is measured in the standard basis, the result is a classical bit.」
- 「because the measurement at the end of the computation gives only one value.」

## Holevo's theorem（Wikipedia，oldid=1379872262）

- 「the amount of classical information that can be retrieved」…「can be only up to n classical (non-quantum encoded) bits」

## Double-precision floating-point format（Wikipedia，oldid=1386295200）

- 「usually occupying 64 bits in computer memory.」→ 一個複數振幅＝實部＋虛部兩個雙精度數＝16 位元組。

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 9 頁：「多個量子位元：2ⁿ 個振幅」；「每多 1 個量子位元，狀態空間加倍：50 個 ≈ 10¹⁵ 個振幅」；備註「n 個量子位元就有 2 的 n 次方個振幅」「這個平行性沒辦法直接讀出來」。
- 第 43 頁：「精確狀態向量：2ⁿ 個複數 × 16 bytes」「~50 個量子位元就超過最大超級電腦的記憶體」；備註「30 個量子位元要 16 GB，筆電還可以；40 個要 16 TB；50 個要 18 PB，超過目前最大超級電腦的總記憶體」「張量網路可以處理糾纏不多的線路」。

## 3D 場景 4：animations/js/operation/04_register.js

- 滑桿「量子位元數 n」1–4，顯示「（2ⁿ 個振幅）」；按鈕「均勻疊加 H⊗ⁿ」「測量全部」「重設 |0…0⟩」。
- 插圖「精確模擬 n 個量子位元所需記憶體（2ⁿ × 16 bytes）」：30 → 16 GB（筆電）、40 → 16 TB（大型伺服器）、50 → 18 PB；紅虛線「頂級超級電腦總記憶體 ≈ 10 PB」（畫在 10^16.5）。

## 重算

| n | 振幅數 2ⁿ | 記憶體 2ⁿ × 16 B |
|---|---|---|
| 1–5 | 2、4、8、16、32 | 32、64、128、256、512 B |
| 10 | 1,024 | 16 KiB |
| 20 | 1,048,576 | 16 MiB |
| 30 | 1,073,741,824 | 16 GiB（≈ 17.2 GB） |
| 40 | ≈ 1.10 × 10¹² | 16 TiB（≈ 17.6 TB） |
| 50 | 1,125,899,906,842,624 | 16 PiB（≈ 18.0 PB） |

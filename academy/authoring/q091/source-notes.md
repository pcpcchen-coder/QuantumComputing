# Q091 來源筆記（逐字引文）

查核日：2026-11-18。學程內部簡報、講稿、對話紀錄與動畫程式由製作代理讀取；維基百科條目作交叉比對。

## 如何操作量子電腦（slides/QC_Operation_Talk.pptx）與講稿 speech/量子電腦操作演講稿.md

第 40 頁（Grover）
- 「應用：振幅放大與振幅估計（蒙地卡羅平方加速）、對稱加密強度減半」
- 講稿：「對密碼學來說，等於把對稱加密的有效金鑰長度減半，所以只要把金鑰加長一倍即可。」

第 41 頁「Shor 演算法：用干涉找週期」
- 「② 模指數 / 計算 f(x) = 7ˣ mod 15 = 1, 7, 4, 13, 1, …（週期 4）」
- 「④ QFT 後：峰值在 64k/r = 0、16、32、48」
- 「gcd(4 − 1, 15) = 3，gcd(4 + 1, 15) = 5 → 15 = 3 × 5」

第 42 頁：「RSA-2048 古典不可行，量子可行」

第 44 頁「量子電腦能算什麼：應用地圖」
- 「密碼分析（RSA、ECC）/ Shor / 指數級 / 需容錯；RSA-2048 估計 < 100 萬實體位元、< 1 週（2025）」
- 講稿：「2025 年 Google 的 Gidney 估計，破解 RSA-2048 需要不到一百萬個錯誤率 0.1% 的實體量子位元、運轉不到一週，比 2019 年估計的兩千萬個少了二十倍。這也是各國加速導入後量子密碼的原因。」

講稿 Q4「Shor 演算法現在能破解 RSA 嗎？」
- 「還不能。…目前最大的系統約一千個量子位元，且尚未達到所需的錯誤更正規模。但『先收集、後解密』的風險促使各界導入後量子密碼（NIST FIPS 203/204/205，2024）。」

## docs/超導量子電腦師生對話教學紀錄.md（Shor 一節）

- 「Shor（1994）在多項式時間內分解大整數，直接威脅 RSA。」
- 表：「Gidney & Ekerå（2019）約 2000 萬 / 約 8 小時」「Gidney（2025）不到 100 萬 / 不到一週」；「前提：實體錯誤率約 0.1% 加表面碼。」
- 「RSA 與 ECC（離散對數，甚至更早被破）受威脅；AES 只受 Grover 平方加速影響，AES-256 仍安全。NIST 2024 年 8 月公布 ML-KEM（FIPS 203）、ML-DSA（FIPS 204）、SLH-DSA（FIPS 205）。最急迫的風險是『現在先收集，以後再解密』。」

## animations/js/operation/10_shor.js

- desc：「古典最好的演算法需要『次指數』時間；Shor 只需多項式時間 —— 這就是 RSA 會被威脅的原因。」
- 按鈕：`ui.radio([[15, 'N = 15'], [21, 'N = 21']], …)`；`b.textContent = \`a = ${x}\``；`ui.button('下一步 ▶'…)`、`ui.button('自動播放'…)`、`ui.button('重設'…)`
- STEPS：「① H⊗⁶：x 暫存器均勻疊加」「② 計算 f(x) = aˣ mod N（顏色 = f(x)）」「③ 量測第二暫存器 → 只留下 f(x) 相同的 x（間隔 = r）」「④ QFT：週期 r 轉成峰值，位置 ≈ 64·k / r」「⑤ 量測 x 暫存器得到 y（白色），交給古典電腦」
- 插圖：`ctx.inset('f(x) = aˣ mod N（週期函數）', …)`，文字「a = ${a}，週期 r = ${order(a, N)}」

## 維基百科（交叉比對）

- RSA (cryptosystem)：名稱取自 Rivest、Shamir、Adleman；安全性依賴分解兩個大質數乘積的困難。
- Shor's algorithm：1994 年；多項式時間解整數分解與離散對數，足夠大的量子電腦可破解 RSA、Diffie–Hellman、橢圓曲線密碼。
- Post-quantum cryptography：在古典電腦上執行、可抵抗量子電腦攻擊的密碼演算法；與量子金鑰分發不同；對稱加密以加倍金鑰長度因應 Grover。
- NIST Post-Quantum Cryptography Standardization：2024 年 8 月發布 FIPS 203（ML-KEM，源自 CRYSTALS-Kyber）、FIPS 204（ML-DSA，源自 CRYSTALS-Dilithium）、FIPS 205（SLH-DSA，源自 SPHINCS+）。
- Harvest now, decrypt later：蒐集目前讀不了的加密資料，期待日後解密技術（含量子電腦）成熟再解開。

這是依課綱製作的課前教學版，不是實際上課錄音。

父子科技學院量子電腦學程第九十一堂：Shor 演算法為什麼會破解 RSA，以及後量子密碼怎麼接手。

這一集會學到
・公開金鑰密碼：RSA 靠分解大數很難，ECC 靠離散對數
・Shor 四步：分解變找週期、疊加一次算全部、QFT 變出高峰、古典算 gcd（15 = 3 × 5）
・破解 RSA-2048 的資源估計：2019 約 2000 萬實體位元，2025 不到 100 萬
・哪些會受影響：公開金鑰要換，對稱加密把鑰匙加倍就好
・NIST 2024 年公布的 ML-KEM、ML-DSA、SLH-DSA；「先存下來、以後再解密」是現在就存在的風險

主要來源：本學程「如何操作量子電腦」簡報第 40–42、44 頁與講稿；師生對話教學紀錄；互動動畫 operation.html#shor 的原始碼；維基百科 RSA、Shor's algorithm、Post-quantum cryptography、NIST Post-Quantum Cryptography Standardization、Harvest now, decrypt later。

教材用法（classroom.zip）
先讀「00_爸爸先讀」，照「01_操作步驟」在瀏覽器動畫裡看 Shor 找週期，再用列印包的盤點表和問題卡做安全審查、查 NIST 標準。課堂 120 分鐘另計。

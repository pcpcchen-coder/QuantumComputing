# Q001 事實查核

查核日：2026-11-07。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：arXiv 三頁（Shor、Grover、Preskill）由研究子代理開啟並回報逐字引文，主代理沒有逐頁重讀；Aaronson 兩篇由主代理下載 PDF、以 pdftotext 讀原文。學程內部簡報 `slides/QC_Operation_Talk.pptx` 由主代理逐頁讀取標題與內文。
限制：本集是給孩子的入門課，用了「快非常多」「平方根」這類口語說法，沒有給具體倍數；課綱的 YouTube 搜尋入口沒有挑選或觀看。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 測量只得到一個結果，而且是隨機的（3） | Aaronson 2008：measurement will pick out just one of the possibilities at random | 相符 |
| 2 | 只是同時試再隨便抽一個，跟亂猜差不多（3） | Aaronson 2008：no better off than … tried out one randomly chosen | 相符 |
| 3 | 讓錯的答案抵消、對的加強（4） | Aaronson 2008：paths leading to a wrong answer would cancel out … constructive interference | 相符 |
| 4 | 只對有特殊結構的問題才有機會大幅加速（5、6） | Aaronson 2008：exceptionally fast at a few specific tasks…；have to exploit the problems' structure | 相符 |
| 5 | 秀爾演算法可在夠大的量子電腦上比已知古典方法快非常多（6） | Shor：steps polynomial in the input size；generally thought to be hard on a classical computer | 相符（「快非常多」是對多項式與已知古典方法差距的口語說法） |
| 6 | 一百萬筆一筆一筆翻平均五十萬次，格羅弗不到一千次（6） | Grover：classical minimum of N/2（50% 機率）；O(√N) steps。(π/4)√10⁶ ≈ 785 為標準結果推算 | 相符（「平均五十萬次」以 N/2 表述） |
| 7 | 費曼 1981 年演講提出用量子系統模擬量子世界（6） | Preskill：In May 1981, Feynman spoke…proposed … quantum computers to simulate quantum systems | 相符 |
| 8 | 大量資料讀進量子電腦本身很花時間，可能吃掉加速（7） | Aaronson 2015：load a large amount of classical data … efficient enough to preserve the quantum speedup | 相符 |
| 9 | 上網、打字、看影片、玩遊戲不會因量子電腦變快（7） | Aaronson 2008（多數問題只會小幅勝出）；學程簡報 C p45「哪些事不會變快」 | 相符（本集的教學判斷，依上述來源） |
| 10 | 量子位元怕熱、怕雜訊（7） | 學程簡報 A p6（品質指標 T₁/T₂）、B p6（為什麼要 10 mK） | 相符 |
| 11 | 學程 96 堂、三階段（2、11） | `academy/curriculum/catalog.json` | 相符 |

## 課程

- 主題、學習目標、動手任務（宣稱卡分類）、好玩機制（冒險任務）、作品、生活技能與 120 分鐘流程依 `academy/lessons/Q001/lesson.json` 核對。
- 片名把課綱的「更快的電腦」去掉引號，避免標題與字幕出現全形引號斷行問題，意思相同。
- 沒有課堂錄音；本集是依課綱製作的課前教學版，未虛構孩子作品或對話。

# Q004 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科 Quantum logic gate 由製作代理以網頁擷取工具開啟並取得逐字引文；學程簡報第 18 頁與 3D 場景程式（`animations/js/operation/02_gates.js`、`common.js` 的 ROT 表）由製作代理讀取；六關答案由製作代理依旋轉表逐步推算。
用語：「正前方／赤道前方」= 布洛赫球 +x（|+⟩），「正後方」= −x（|−⟩）；三維動畫預設視角下 x 軸朝向觀眾。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 量子閘只讓箭頭繞一條軸轉動，不會變短（3） | QLG：gates are unitary；C p18：單位元閘就是 Bloch 球上的旋轉 | 相符（單位元閘） |
| 2 | 在旋轉軸上的箭頭轉完還在原地（3、4） | 旋轉的基本性質；X|+⟩=|+⟩ | 相符 |
| 3 | X、H、Z 都是轉一百八十度（3） | QLG：Pauli X, Y, Z…by π radians；H…rotation of π；02_gates.js ROT | 相符 |
| 4 | 翻轉閘（X）的軸是前後軸，北極↔南極，像古典的非（4） | QLG：rotation around the x axis；quantum equivalent of the NOT gate；bit-flip maps |0⟩→|1⟩ and |1⟩→|0⟩；C p18 | 相符 |
| 5 | 哈達瑪閘（H）的軸在北極和赤道前方正中間，兩者互換（5） | QLG：rotation of π about the axis (x̂+ẑ)/√2；C p18：|0⟩ 變成 |+⟩ | 相符 |
| 6 | 北極按一次 H，測量一半一半（5） | QLG：equal superposition state；場景讀數 P(0)=0.500 | 相符 |
| 7 | 相位翻轉閘（Z）軸是直立軸，兩極不動，赤道前方轉到後方，機率不變（5） | QLG：Z rotation around z axis，phase-flip；C p18：只改相位、單獨量測看不出差別 | 相符 |
| 8 | 同一個閘連做兩次回原狀；H 做兩次回北極（6） | QLG：Hadamard is involutory；X²=Z²=I | 相符 |
| 9 | 一串 X/H/Z 從最後一顆倒著再做一次就回到起點（6） | 三者皆自逆，(ABC)⁻¹=C⁻¹B⁻¹A⁻¹=CBA | 相符（限這三種閘；S、T 等需用反向閘） |
| 10 | 量子閘可倒回去，測量不行（6、12） | QLG：quantum logic gates are reversible；Measurement…is irreversible | 相符 |
| 11 | 第一、二關各一顆，第三關至少兩顆（7） | X|0⟩=|1⟩；H|0⟩=|+⟩；|−⟩ 需 XH 或 HZ（單顆 X/H/Z 都到不了） | 相符 |
| 12 | 第四關：不用 X 到南極（8） | HZH=X（C p18 場景示範「H → Z → H = X」） | 相符（三顆） |
| 13 | 第五關：X、H、Z、H 之後（8） | |0⟩→|1⟩→|−⟩→|+⟩→|0⟩，回到北極 | 相符 |
| 14 | 第六關只用 X、Z 到不了赤道（8） | X、Z 只把兩極互換或不動 | 相符（陷阱關無解） |
| 15 | 場景粉紅線是旋轉軸（8） | 02_gates.js desc：粉紅線是旋轉軸 | 相符 |

## 課程

- 主題、學習目標、動手任務（六關）、孩子獨立改造（出兩關並寫參考解）、好玩機制（闖關）、作品（闖關紀錄表）、120 分鐘流程與驗收依 `academy/lessons/Q004/lesson.json` 核對。
- 驗收的兩個注意事項（H 做兩次回原狀；量子閘可以倒回去，測量不行）都在第 6 幕與第 12 幕出現。
- 「翻轉閘」「相位翻轉閘」是 bit-flip、phase-flip 的意譯，旁白避免英文字母；投影片同時標 X、H、Z，對應三維動畫的按鈕。
- 沒有課堂錄音；未虛構孩子作品或對話。

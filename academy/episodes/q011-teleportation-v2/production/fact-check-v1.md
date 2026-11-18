# Q011 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科 Quantum teleportation 頁由製作代理直接開啟並摘錄（oldid=1384656230）；學程簡報「量子電路入門：八個範例」第 15–17 頁的文字與講者備註、`animations/basic-circuits.html` 隱形傳態範例與 `animations/js/operation/06_circuit.js` 的 tele 範例由製作代理讀取；隱形傳態範例各步的 Bloch 向量與 q2 量測機率，由製作代理在 Node 執行頁面引擎（simulate、marginal、reducedBloch）實算。
限制：本集沒有實作程式，也沒有真機數據；角色扮演的硬幣、信封、時鐘箭頭是教學模型。動畫段尚未試錄。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 隱形傳態用糾纏把一顆量子位元的狀態送到遠方，送過去的不是粒子本身（1、5） | Quantum teleportation：only transfers quantum information；Alice's particle has not been physically moved to Bob; only its state has been transferred | 相符 |
| 2 | 需要一對事先分好的糾纏位元，兩人一人一顆（2、3） | 維基：a means of generating an entangled Bell state of qubits and distributing to two different locations；簡報 p15「q2 交給遠方的 Bob」 | 相符 |
| 3 | 一定要用普通通訊送出兩個位元（2、3、6） | 維基：a communication channel capable of transmitting two classical bits；For every qubit teleported, Alice needs to send Bob two classical bits | 相符 |
| 4 | 狀態搬過去之後，原本那一顆的狀態被破壞；沒有多出一份，叫不可複製（2、7） | 維基：initial quantum information is "destroyed"…no-cloning theorem is maintained；Teleportation does not result in the copying of qubits；簡報 p17「q0 卻不再是 ψ：狀態是搬過去，不是複製」；引擎實算第 4 步 q0 不再是 ψ | 相符 |
| 5 | 寄件人不用知道要傳的是什麼狀態（3） | 維基：The sender does not have to know the particular quantum state；簡報 p15「Alice 不必知道 ψ 是什麼」 | 相符 |
| 6 | 線路三條線：上兩條在愛麗絲、最下面在鮑伯（4） | 簡報 p15「q0、q1（Alice）、q2（Bob）」；basic-circuits.html init 文字 | 相符 |
| 7 | 四步：準備狀態；哈達瑪閘加受控反閘做糾纏對；愛麗絲受控反閘、哈達瑪閘再測量得兩個位元；打電話後鮑伯修正（4） | 簡報 p15 ①–④；basic-circuits.html teleport steps；維基 Protocol | 相符 |
| 8 | 科幻傳送是搬人或東西；隱形傳態沒有粒子或物質被搬過去（5） | 維基：commonly portrayed in science fiction as a means to transfer physical objects…only transfers quantum information；There is no transfer of matter or energy involved | 相符 |
| 9 | 測量得到四種結果之一，各四分之一（6） | 簡報 p16 機率欄皆 ¼；維基：two classical bits (00, 01, 10 or 11)…with equal probability of 1/4 | 相符 |
| 10 | 四種結果對應不同修正：不用修、翻轉閘、相位翻轉閘、兩個都要（6） | 簡報 p16 修正表（不用修、Z、X、先 X 再 Z）；維基：identity、σ3、σ1、σ3σ1 | 相符 |
| 11 | 不知道結果，鮑伯那顆只是隨機狀態；電話前他拿不到任何訊息（6、7、12） | 簡報 p16「收到 2 個位元之前，Bob 不知道是哪一種，q2 對他來說完全隨機」；引擎實算第 2、3 步 q2 的 Bloch 向量長度為 0、量測 0／1 各 50% | 相符 |
| 12 | 電話不會比光快，所以隱形傳態不能比光快（7、12） | 維基：Because classical information needs to be sent, quantum teleportation cannot occur faster than the speed of light | 相符 |
| 13 | 一顆量子位元量一次只得到零或一；要重複很多次比機率（8） | 動畫量測卡說明「要重複很多次，才看得出機率分布」；引擎：預設 ψ 修正後 q2 量到 0 為 75% | 相符 |
| 14 | 量到零的機會四分之三、傳一千次約七百五十次（8，暫停題，答案在教材） | 期望值 1000 × ¾ = 750；有限次數會上下跳 | 相符 |
| 15 | 未來量子網路與多晶片量子電腦靠它搬運量子狀態（10） | basic-circuits.html teleport take：「量子網路與模組化量子電腦都靠它在不同晶片之間搬運量子態」 | 相符（僅本學程動畫文字，未另查外部文獻；見 not_verified） |
| 16 | 角色扮演：擲兩枚硬幣代表測量結果（9） | 四種結果各 ¼，兩枚公平硬幣同為各 ¼ | 教學模型（教材已註明硬幣不是量子測量） |
| 17 | 下一堂：只問一次看穿黑盒子函數是常數還是平衡（12） | academy/lessons/Q012/brief.md | 相符 |

## 動畫段（demos_extra/q011.py）

| 段 | 說法 | 依據 | 結論 |
|---|---|---|---|
| 狀態搬家的四步 | 選成一；第 1 步愛麗絲那顆朝正下方、鮑伯那顆朝正上方；第 2 步鮑伯那顆縮到球心；第 3 步仍在球心；第 4 步鮑伯朝正下方、愛麗絲不再朝下 | 引擎實算 ψ=\|1⟩：q0 (0,0,−1)→(−1,0,0)→(1,0,0)；q2 (0,0,1)→0→0→(0,0,−1)；Bloch 球依序為單看 q0、單看 q2 | 相符（左右位置待試錄確認） |
| 打電話前後 | 第 3 步量 1,000 次 0／1 各約一半、灰色理論一半；下一步會清空紀錄；修正後 0 約四分之三，出現綠字 | marginal：第 3 步 {0: .5, 1: .5}、第 4 步 {0: .75, 1: .25}；go() 呼叫 clearShots；verdict 只在最後一步出現，CSS color var(--hit)（綠） | 相符 |
| 重複一千次來確認 | 八格、單步時該格閘發光、最後量測跑一千次、量到 1 約四分之三、青色理想線 | 06_circuit.js：tele 八欄；emissiveIntensity 0.8；sample() 1000 次；Ry(2π/3) → P(1)=0.75；inset 理想線 #8ef0ff | 相符 |

## 課程

- 主題、學習目標、動手任務（三人扮演 Alice、Bob、信差）、孩子獨立改造（6 格漫畫標出打電話）、好玩機制（角色扮演）、作品（傳送流程漫畫）、120 分鐘流程、驗收（沒有兩個古典位元只拿到隨機狀態；不能超光速）、生活技能（分清楚什麼要靠通訊）依 `academy/lessons/Q011/lesson.json` 核對。
- 旁白不念英文：Alice、Bob 稱「愛麗絲」「鮑伯」；CNOT 稱「受控反閘」、H 稱「哈達瑪閘」、X 稱「翻轉閘」、Z 稱「相位翻轉閘」。
- 沒有課堂錄音；未虛構孩子作品或對話。

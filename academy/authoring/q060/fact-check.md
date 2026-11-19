# Q060 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科三頁（Deferred measurement principle、Quantum error correction 的 Bit-flip code 一節、Quantum teleportation）由製作代理取得 wikitext 並摘錄；學程簡報 `QC_Operation_Talk.pptx` 第 13、28 頁（含講者備註）以 python-pptx 讀取；互動動畫 basic-circuits.html（teleport）、atoms.html（zoned）、operation.html（qec）、peripherals.html（bringup）原始碼由製作代理讀取，並以 1600×900 Chromium（swiftshader）截圖確認；主動重置、無回饋對照組與三位元重複碼症狀表以 qiskit 2.6.2＋qiskit-aer 0.18.4 實跑（`/home/user/qwork/q060calc/checks.py`，固定亂數種子 7，輸出附在文末）。
限制：本集只談理想的動態線路邏輯；各平台實際的回饋延遲與錯誤率只引用簡報的代表值。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：估算要跑幾次、修正讀取誤差；量測都放在最後（1） | academy/lessons/Q059/brief.md（shots、統計誤差與讀取誤差緩解）；Q057–Q059 的線路都只在最後量測 | 相符 |
| 2 | 動態線路：中途量測一部分位元，依結果決定下一步（1、3） | op_talk p28「線路中途量測部分量子位元／依結果（古典位元）決定後面的閘」 | 相符 |
| 3 | 沒被量的位元繼續留在疊加和糾纏裡（3） | 只量部分位元；op_talk p28；Deferred measurement「measuring qubits as early as possible…」（量部分、其他繼續運算） | 相符（被量的那顆會塌縮，見第 13 列） |
| 4 | 結果存成古典位元，控制電子依零或一決定要不要加閘，叫前饋（3） | op_talk p28；p28 程式 `with qc.if_test((qc.clbits[0], 1)): qc.x(1)` | 相符（「前饋」為 feed-forward 的中文稱呼） |
| 5 | 要在相干時間內完成，判別與決策約數百奈秒（3、8、12） | op_talk p28「需要控制電子在相干時間內完成判別與決策（~數百 ns）」；課綱常見誤解 | 相符（代表值，見 not_verified） |
| 6 | 四種用途：主動重置；隱形傳態依兩個結果補翻轉閘或相位翻轉閘；錯誤更正每輪量症狀即時解碼；重複直到成功（4） | op_talk p28「用途」四行；Quantum teleportation「two classical bits… modified in one of three ways, or not at all」 | 相符（重複直到成功只列名，見 not_verified） |
| 7 | 延遲量測原理：依結果補的閘換成受控閘、量測挪到最後，機率分佈一樣（5、動畫 teleport） | Deferred measurement「delaying measurements until the end … doesn't affect the probability distribution of outcomes」「measuring commutes with conditioning」；op_talk p28 備註 | 相符 |
| 8 | 延遲的代價：位元要留到最後；早點量完，同時要保存的位元較少（5） | Deferred measurement「measuring qubits as early as possible can reduce the maximum number of simultaneously stored qubits」 | 相符 |
| 9 | 主動重置三步：量測、判斷、是一就送翻轉閘、是零不做事（6） | op_talk p13「先量測：若結果是 1 → 立刻送 π 脈衝翻回 0」；π 脈衝即翻轉閘（X） | 相符 |
| 10 | 被動等待數百微秒，主動重置約一到五微秒，快上百倍（6） | op_talk p13「數百 μs（如 250 μs）」「~1–5 μs」，備註「比被動重置快上百倍」；250/2.5 = 100 | 相符 |
| 11 | 例題：H → 中途量測 → 若 1 則 X → 再量，一千次；第一次約各半（499／501），第二次全是零（7） | checks.py `active reset (c1 c0): {'00': 499, '01': 501}`（c1 = 第二次量測全為 0）；Ry(60°) 起點也全回 0（`ry60 reset`） | 相符（固定種子的一次模擬、理想無雜訊） |
| 12 | 多等一微秒、能量弛豫時間約九十微秒 → 約百分之一機會衰減（8） | bringup 場景「T₁ ≈ 90 μs」；1 − e^(−1/90) = 0.01105 | 相符（估算） |
| 13 | 讀取出錯就會補錯閘；被量過的位元疊加就沒了（8） | 讀取錯誤（op_talk p33 備註 0.5–3%）→ 依錯誤結果補閘；量測塌縮（op 場景 1） | 相符 |
| 14 | 冒險任務：關主選零態、一態、加態，勇者中途量一次、量到一走翻轉閘，最後一千次全是零過關；拿掉回饋會失敗（9） | checks.py：有回饋第二次量測全 0；無回饋 `{'11': 486, '00': 514}`（加態約一半失敗）；一態無回饋全為 1 | 相符 |
| 15 | 重複碼：三顆資料、兩顆輔助；輔助一比一號二號、輔助二比二號三號；相同得零不同得一；只量輔助（10） | Quantum error correction bit-flip code「asking whether one of the qubits differs from the others… without also querying for the values」；checks.py 症狀表 | 相符 |
| 16 | 二號錯兩顆輔助都是一；只有第一顆是一 → 一號錯；只有第二顆是一 → 三號錯（10） | checks.py：[0,1,0] s1=1 s2=1；[1,0,0] s1=1 s2=0；[0,0,1] s1=0 s2=1；Aer 實跑 err 1 → 輔助 11、修正後資料 000 | 相符 |
| 17 | 120 分鐘安排（11） | 課綱 2 小時流程 | 相符 |
| 18 | 下一堂：量子傅立葉轉換與相位估計（12） | academy/lessons/Q061/brief.md | 相符 |

## 投影片上的數字與符號

- 第 3、4 頁「約數百 ns」見第 5 列；第 6 頁「被動數百 μs → 主動約 1–5 μs」見第 10 列；第 7 頁 1000 次全是 0 見第 11 列；第 8 頁「T₁ ≈ 90 μs，多等 1 μs」「約 1%」見第 12 列；第 10 頁「1,1 → 2 號錯」見第 16 列。

## 課程

- 主題、學習目標、動手任務、孩子獨立改造、好玩機制（冒險任務）、作品（主動重置線路）、生活技能（根據回饋即時調整）、家長準備、120 分鐘流程、驗收與常見誤解依 `academy/lessons/Q060/lesson.json` 核對。
- 家長準備的 atoms.html#zoned（中途量測）用在動畫段 zoned。
- 旁白不念英文：X 念翻轉閘、Z 念相位翻轉閘、H 念哈達瑪閘、CNOT 念受控反閘、T₁ 念能量弛豫時間、Alice／Bob 念愛麗絲／鮑伯；投影片保留符號。
- 沒有課堂錄音；未虛構孩子作品或對話。

## 動畫展示段（demos_extra/q060.py）

- teleport（bc#teleport）：捲到 520 截圖可見 q0、q1、q2 三條線與方框「修正（2 個古典位元）」；三次「下一步」後捲到 1000，說明「q2 的向量還在球心」、右邊「單看 q2」球的向量縮成球心一點；第 4 步說明「真實做法是 Alice 量測 q0、q1…q1 = 1 就對 q2 做 X，q0 = 1 就做 Z。這裡用受控閘代替…（延遲量測原理）…q2 的向量回到 ψ」；第 4 步後 |ψ⟩ 中 q2 = 0 的四項各 0.433（P = 4 × 0.1875 = 0.75）；量測 1,000 次截圖 754／246、「理論：0 75%、1 25%」。
- zoned（at#zoned）：截圖確認儲存區藍框與標籤、4 色原子＋「邏輯位元 A–D」、中間粉紅成對圓環帶、下方青色帶；「中途量測」後最前一排 6 顆（4 綠 2 紫）帶粉紅光錐移到青色帶；成像時青色光片與往上飛的光點；補充後原子回原位；小圖 0.3 μs 與 1 ms（1 ms ÷ 0.3 μs = 3333，「三千多倍」）、頁尾「整體速度由搬運與讀取決定」。以實際時間驅動場景（不受錄影速度影響）。
- syndrome（op#qec）：關「自動循環」、點「d = 5」（setup 清空）；第一下以固定種子 258 產生錯誤，截圖只有正中間 1 顆紅球；第二下斜對角兩塊方塊變色並豎起橘色柱子；第三下面板「③ 解碼：配對 2 個症狀」、綠線連兩個症狀；第四下紅球變白、面板「④ 修正完成 → 邏輯資訊保住了 ✓」（面板最下方可見）。程式碼：兩個症狀距離 1、到邊界各 2，最小權重配對必配成一對，翻轉的正是 (2,2)。
- 三段都只用按鈕或以實際時間驅動的動作，旁白描述的都是動作後會維持的狀態。

## Python 輸出

```
active reset (c1 c0): {'00': 499, '01': 501}
no feedback: {'11': 486, '00': 514}
ry60 reset: {'00': 758, '01': 242}
reset instr: {'0': 1000}
err None {'00000': 200}
err 0 {'01001': 200}
err 1 {'11000': 200}
err 2 {'10100': 200}
[0, 0, 0] s1= 0 s2= 0
[1, 0, 0] s1= 1 s2= 0
[0, 1, 0] s1= 1 s2= 1
[1, 1, 0] s1= 0 s2= 1
[0, 0, 1] s1= 0 s2= 1
[1, 0, 1] s1= 1 s2= 1
[0, 1, 1] s1= 1 s2= 0
[1, 1, 1] s1= 0 s2= 0
readout/gate ratio 1ms/0.3us = 3333.3333333333335
T1 100us, feedback 1us decay prob 0.009950166250831893  0.5us 0.00498752080731768
passive 5T1  0.006737946999085467
1 - exp(-1/90) = 0.01105
```

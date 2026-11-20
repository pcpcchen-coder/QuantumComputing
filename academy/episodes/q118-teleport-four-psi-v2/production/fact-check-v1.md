# Q118 事實查核

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科四頁（Quantum teleportation、Deferred measurement principle、No-cloning theorem、No-communication theorem）由製作代理取得原始 wikitext 並摘錄；學程簡報 basic-circuits.pptx 第 15–17 頁（用 python-pptx 讀出實際頁碼與文字與備註）、互動動畫 basic-circuits.html #teleport、operation.html#circuit（js/operation/06_circuit.js）的程式由製作代理讀取，動畫畫面以 Playwright 實拍確認；程式結果由製作代理在本機實際執行。
執行環境：Python 3.13.18（teleport_lab.py，只用標準函式庫，random 種子 1118）；Qiskit 2.6.2（qiskit_check.py，StatevectorSampler seed=2026）。
限制：本課四種 ψ 的振幅皆為實數；量測一千次的次數是隨機的，旁白不念數字；「受控閘要三顆位元靠在一起、傳遠要先量」依 Deferred measurement principle 條目的圖說，未另查特定實驗。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂把受控反閘串成一條鏈，讓三顆位元一起糾纏（1） | Q117 課名與簡報第 13 頁 | 相符 |
| 2 | 拿一對糾纏的位元當通道，把一顆位元的狀態送到遠方（1） | 簡報第 15 頁標題「用糾纏把狀態送過去」；Quantum teleportation「transferring quantum information from a sender at one location to a receiver some distance away」 | 相符 |
| 3 | 搬的是狀態，不是粒子；一定要再打一通普通的電話，所以快不過光（1） | 簡報第 15 頁備註「用電話告訴 Bob」「沒有搬動任何粒子」；Quantum teleportation「only transfers quantum information」「classical information needs to be sent … cannot occur faster than the speed of light」 | 相符 |
| 4 | 三人傳送：愛麗絲、鮑伯、信差送兩個位元（2） | 課綱好玩機制「角色扮演（三人傳送）」；第 15 頁「量 q0、q1 得到 2 個位元」 | 相符（信差一角為本課設計，代表古典通道） |
| 5 | 紙條送到之前鮑伯什麼都不能做；作品傳送流程表，四種狀態各傳一次（2） | 簡報第 16 頁「收到 2 個位元之前，Bob 不知道是哪一種」；課綱作品「傳送流程表」、動手任務「四種 ψ 各傳一次」 | 相符 |
| 6 | 三條線從零態出發，編號零、一在愛麗絲，編號二在遠方的鮑伯（3） | 簡報第 15 頁「q0 |0⟩（Alice）」「q1 |0⟩（Alice）」「q2 |0⟩（Bob）」「q2 交給遠方的 Bob」 | 相符 |
| 7 | 第一步在編號零準備狀態；第二步哈達瑪閘加受控反閘，讓編號一、二變成貝爾態（3） | 簡報第 15 頁 ①②；動畫 build [H(1)], [CX(1, 2)] | 相符 |
| 8 | 第三步愛麗絲做受控反閘和哈達瑪閘，量出兩個位元；第四步鮑伯照兩個位元修正，編號二變成要傳的狀態（3） | 簡報第 15 頁 ③④；Quantum teleportation protocol；teleport_lab.py 第一段四種都 True | 相符 |
| 9 | 愛麗絲的結果：編號一、編號零的兩個位元，四種各占四分之一（4） | 簡報第 16 頁表格「Alice 量到 q1 q0」各 ¼；teleport_lab.py 第二段機率 0.25 | 相符 |
| 10 | 零零不用修；零一補相位翻轉閘；一零補翻轉閘；一一兩個都補（4） | 簡報第 16 頁表格；teleport_lab.py 第二段修正後都是 ψ | 相符 |
| 11 | 口訣：編號一是一做翻轉閘，編號零是一做相位翻轉閘；修完都一樣（4） | 簡報第 15 頁「q1 = 1 做 X、q0 = 1 做 Z」 | 相符 |
| 12 | 紙條送到之前四種混在一起，鮑伯的位元完全隨機（5） | 簡報第 16 頁與備註「四種等量混在一起，q2 對他來說完全隨機」；teleport_lab.py 第一段 ③ 之後 q2 大小 0.00 | 相符 |
| 13 | 這時鮑伯自己量，不管傳哪一種都是一半零一半一（5） | teleport_lab.py 第四段「不修」四種 P(1) 0.50；動畫實拍 |1⟩ 第 3 步理論 0、1 各 50% | 相符 |
| 14 | 不能超光速：消息要靠信差，信差快不過光（5、8、12） | Quantum teleportation「cannot occur faster than the speed of light」；No-communication theorem | 相符 |
| 15 | 動畫用延遲量測版：把鮑伯的兩個修正改成由編號一、編號零控制的受控閘（6） | 簡報第 17 頁「動畫用受控閘代替『量測後再修正』（延遲量測原理）」；動畫 [CX(1, 2)], [CZ(0, 2)] | 相符 |
| 16 | 修翻轉的是受控反閘、修相位的是受控相位翻轉閘；結果和先量再修完全一樣（6） | Deferred measurement principle「delaying measurements … doesn't affect the probability distribution」與圖說；teleport_lab.py 第三段每次修完都等於 ψ（assert） | 相符 |
| 17 | 好處是可一步一步看振幅；受控閘要三顆靠在一起，真的傳遠還是得先量再打電話（6） | Deferred measurement principle 圖說「requires both qubits to be near … limits the distance of the teleportation」 | 相符（條目圖說；未另查實驗） |
| 18 | 動畫可換四種狀態：零態占四分之三那種、一態、正號、負號疊加態（7） | 動畫選項 √¾|0⟩+½|1⟩、|1⟩、|+⟩、|−⟩ | 相符 |
| 19 | 第一種傳完鮑伯量到零的機率四分之三；一態傳完箭頭指向南極，每次都量到一（7） | 動畫理論 0 75%；teleport_lab.py P(1) 0.25、1.00；實拍 |1⟩ q2 在南極 | 相符 |
| 20 | 正號、負號疊加態量起來都一半一半，要看布洛赫球，箭頭停在赤道兩個相反方向（7） | 簡報第 17 頁「|+⟩ 和 |−⟩ 量起來都是 50/50，要看 Bloch 球才分得出來」；teleport_lab.py q2 (+1, 0)／(−1, 0) | 相符 |
| 21 | 不是複製：傳完後編號零不管傳哪一種都停在同一方向，原來的資訊不在它身上（8） | 簡報第 17 頁「q0 卻不再是 ψ：狀態是搬過去，不是複製」；teleport_lab.py「四種傳完，單看 q0 都一樣嗎？ True」；No-cloning theorem；Quantum teleportation「not copied during teleportation」 | 相符（「停在同一方向」是延遲量測版的結果，見 not_verified） |
| 22 | 沒有粒子移動，鮑伯的位元本來就在他手上，改變的只是它的狀態（8） | 簡報第 15 頁備註「沒有搬動任何粒子」；Quantum teleportation「moving the information between carriers and not movement of the actual carriers」 | 相符 |
| 23 | 沒有那兩個位元鮑伯什麼都做不了；驗收要說出的限制（8、12） | 課綱驗收「沒有古典通訊就無法完成，所以不能超光速」 | 相符 |
| 24 | 實作：範例五選狀態、回到起點、四步；左邊編號零、右邊編號二；走完量一千次對照（9） | basic-circuits.html 選項、#bFirst、#bNext、#m1000；Bloch 球 bloch: [0, 2]（左 q0、右 q2）；實拍 | 相符 |
| 25 | 拿掉修正後四種的箭頭全縮在球心、量起來一半一半（10） | teleport_lab.py 第四段「不修」四種「錯 0.50 0.00」；Qiskit 相似度 0.500 | 相符 |
| 26 | 只補翻轉閘：一態照樣傳對；正號疊加態量起來仍一半一半，但箭頭縮進球心，其實傳錯（10） | teleport_lab.py 第四段「只修 X」|1⟩ 對 1.00 1.00、|+⟩ 錯 0.50 0.00；Qiskit 只修 X：|1⟩ 1.000、|+⟩ 0.500 | 相符 |
| 27 | 120 分鐘流程、生活技能「通訊不可少」（11） | 課綱「生活技能支線：通訊是不可少的一環」 | 相符 |
| 28 | 原本那顆不再保有那個狀態（12） | 第 21 條 | 相符 |
| 29 | 下一堂是範例六，德意志演算法，用紅綠球搖獎機來猜黑盒子（12） | academy/lessons/Q119/brief.md「範例 6：Deutsch——紅綠球搖獎機」「四種黑盒」 | 相符 |

## 動畫展示段（demos_extra/q118.py）

| 段 | 說法 | 依據（原始碼與實拍） | 結論 |
|---|---|---|---|
| move | 柱子下面兩顆布洛赫球，左單看編號零、右單看編號二，兩支都指向北極 | bloch: [0, 2]，標籤「單看 q0」「單看 q2」；起點尖端 (100, 29.5)；實拍 | 相符 |
| move | 第一步旋轉閘準備，左邊箭頭往旁邊傾斜；第二步做出糾纏對，右邊箭頭縮進球心 | Ry(π/3)：q0 (0.87, 0.50)，尖端 (66.4, 84.1)；② q2 (0, 0) 尖端 (100, 104)；向量隨 650 ms 內插移動 | 相符 |
| move | 第三步愛麗絲做受控反閘、哈達瑪閘，左邊箭頭變短、倒到赤道，右邊仍在球心 | ③ q0 (0.50, 0.00)，尖端 (80.6, 114.0)；q2 (0, 0) | 相符 |
| move | 第四步鮑伯修正，右邊箭頭指向左邊一開始傾斜的方向；量一千次綠色條大多落在零 | ④ q2 尖端 (66.4, 84.1)＝① 的 q0；理論 0 75%（灰色底），實拍 766 | 相符（次數隨機，旁白不念） |
| four | 選一態跳到最後一步，鮑伯的箭頭指向南極 | 選項 (2) → rebuild(false)，「步驟 4 / 4」；q2 尖端 (100, 178.5) | 相符 |
| four | 左邊四根都是零，右邊四根一樣高，最左那一位都是一，鮑伯那顆一定是一 | (|100⟩ + |101⟩ + |110⟩ + |111⟩) / 2；字串 |q2 q1 q0⟩，最左是 q2 | 相符 |
| four | 正號疊加態八根一樣高，箭頭倒到赤道；負號疊加態右邊四根翻到下面變橘色，箭頭到赤道另一頭 | |+⟩：8 根 +.354；q2 (1, 0)；|−⟩：|100⟩…|111⟩ −.354（.fill.n 橘）；q2 (−1, 0)，尖端 (138.8, 84.0) | 相符 |
| four | 四種換來換去，左邊編號零的箭頭一直停在同一位置 | 四種 q0 尖端都是 (61.2, 124.0)；teleport_lab.py True | 相符 |
| nofix | 選一態再點第四個小圓點，停在第三步 | #dots 5 個圓點，nth-child(4) → go(3)；實拍「步驟 3 / 4」 | 相符 |
| nofix | 鮑伯的箭頭縮在球心；量一千次零和一差不多一樣多 | 第 3 步 q2 (0, 0)；理論各 50%，實拍 520／480 | 相符 |
| nofix | 下一步做修正，箭頭伸到南極；再量一千次只剩一這一列，上面出現綠字說和要傳的狀態相同 | 第 4 步 q2 (0, −1)；histRender 只列理論不為 0 的「1」；verdict「→ 對照 ψ：q2 的量測機率和 ψ 相同」在 .last 下、hist 上；實拍 1000 次 | 相符 |

## 課程

- 主題、學習目標、動手任務、孩子獨立改造（拿掉修正步驟）、好玩機制（角色扮演：三人傳送）、作品（傳送流程表）、生活技能（通訊是不可少的一環）、120 分鐘流程、驗收（沒有古典通訊就無法完成，所以不能超光速）依 `academy/lessons/Q118/lesson.json` 核對。
- 課綱素材寫簡報 p15–17：用 python-pptx 讀 basic-circuits.pptx，第 15 頁「範例 5｜隱形傳態：用糾纏把狀態送過去」、第 16 頁「Alice 量到什麼、Bob 怎麼修」、第 17 頁「動畫：用 Bloch 球看狀態搬家」，頁碼無誤。
- 課綱「對象與上課方式」寫「逐步播放振幅長條、量測 1000 次，再用本機 Qiskit 模擬器重現」：教材提供免安裝的 teleport_lab.py 與選用的 qiskit_check.py（pip install qiskit）。
- 課綱素材另列 `o:circuit`（operation.html#circuit），其中「量子隱形傳態」線路用 Ry(2π/3)（量到 1 的機率 0.75），和 basic-circuits 預設 ψ（量到 0 的機率 0.75）方向相反；為免在「四種 ψ」之外多出第五種造成混淆，動畫展示段未選用，只寫進教材導覽（選用）。
- 先前各課：Q010 結尾只預告隱形傳態；Q113 只在八個範例總覽提到範例五；demos_extra 沒有 q011.py，也沒有任何一課用過 bc#teleport 或 op#circuit 的隱形傳態線路，旁白與觀察沒有重複。
- 旁白不念英文：Alice、Bob 念「愛麗絲」「鮑伯」；ψ 念「要傳的狀態」；H「哈達瑪閘」、X「翻轉閘」、Z「相位翻轉閘」、CNOT「受控反閘」、CZ「受控相位翻轉閘」、Ry「旋轉閘」；|+⟩、|−⟩ 念「正號疊加態」「負號疊加態」；Bell「貝爾態」；q0–q2「編號零」到「編號二」；Deutsch「德意志」。投影片保留 ψ、CNOT 等符號。旁白避開「長」字。所有句子（含動畫段 11 句）以 caption_wrap.wrap_caption 檢查可排成兩行字幕。
- 沒有課堂錄音；未虛構孩子作品或對話。

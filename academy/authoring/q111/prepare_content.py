"""Q111 第 13 課：編譯與控制軟體堆疊 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q111/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q111', 'q111-software-stack', '2026-11-18'
TITLE = '編譯與控制軟體堆疊'
TOPIC = '第 13 課：編譯與控制軟體堆疊'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q111/lesson.json',
    'dialog': f'{REPO} docs/超導量子電腦師生對話教學紀錄.md（第 13 課）',
    'tr_slides': f'{REPO} slides/transmon.pptx（第 26 頁：3D 第 12 章軟體堆疊）',
    'op_slides': f'{REPO} slides/QC_Operation_Talk.pptx（第 26 頁：轉譯）',
    'scene_tr': f'{REPO} animations/transmon-3d.html#stack（第 12 章步驟 1–9）',
    'scene_op': f'{REPO} animations/operation.html#workflow（場景 12 完整流程）',
    'openqasm': 'https://en.wikipedia.org/wiki/OpenQASM',
    'fpga': 'https://en.wikipedia.org/wiki/Field-programmable_gate_array',
    'qiskit': 'https://en.wikipedia.org/wiki/Qiskit',
    'qlg': 'https://en.wikipedia.org/wiki/Quantum_logic_gate',
    'run': f'{REPO} academy/authoring/q111/classroom.py（stack_race.py 實跑紀錄）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q111 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（跟著一條電路走完七層：分解、映射、SWAP 路由、最佳化、排程、脈衝、FPGA 回饋）、動手任務（在軟體堆疊章比較直線與方格晶片的 SWAP 數與總時間）、'
                '孩子獨立改造（選 Bell、GHZ、BV 其中一個，寫出每一層做了什麼）、好玩機制（效能競賽）、作品（七層堆疊說明卡）、生活技能（系統的每一層都有責任）、'
                '120 分鐘流程、驗收與常見誤解（晶片連接方式會大幅改變 SWAP 數與錯誤）'},
    {'id': 'dialog', 'title': '超導量子電腦師生對話教學紀錄 第 13 課', 'publisher': REPO, 'url': SRC['dialog'],
     'usedFor': '七層與兩根支柱；原生閘 Rz、√X、CZ 與分解式；校準感知映射；SWAP = 3 個 CNOT、找最少 SWAP 是 NP-hard；Rz 是虛擬 Z、0 ns；'
                '相鄰 CZ 不能同時（頻率碰撞）；脈衝表（√X 20–40 ns、CZ 40–60 ns、讀取 0.3–1 μs）；10 MHz 參考時鐘、條件分支幾百 ns；'
                '重跑數千 shot、讀取混淆矩陣；編譯上傳排隊常比跑還久；校準依賴圖；NISQ 錯誤緩解與 FTQC 錯誤更正；動畫實際編譯結果表'},
    {'id': 'tr_slides', 'title': 'Transmon 筆記簡報 第 26 頁', 'publisher': REPO, 'url': SRC['tr_slides'],
     'usedFor': '3D 第 12 章九步驟摘要：七層、分解成 Rz、√X、CZ、依校準資料映射、不相鄰插 SWAP（每個 = 3 個 CZ）、H·H 抵消與虛擬 Z、ASAP 但相鄰 CZ 不同時、FPGA 回饋與校準依賴圖'},
    {'id': 'op_slides', 'title': '如何操作量子電腦 第 26 頁「轉譯（transpile）」', 'publisher': REPO, 'url': SRC['op_slides'],
     'usedFor': '轉譯五步（分解、配置、路由、最佳化、排程）；H = RZ(π/2)·SX·RZ(π/2)、CNOT = (I⊗H)·CZ·(I⊗H)、SWAP = 3 × CNOT；配置要考慮當天校準的錯誤率；轉譯好壞可差數倍閘數'},
    {'id': 'scene_tr', 'title': '互動動畫 transmon-3d.html 第 12 章「編譯與控制軟體堆疊」', 'publisher': REPO, 'url': SRC['scene_tr'],
     'usedFor': 'compile12（分解、窮舉映射、前瞻路由、H·H 抵消、Rz 合併、ASAP 排程且相鄰 CZ 錯開）；DUR12（√X 32 ns、Rz 0、CZ 48 ns、讀取 600 ns）；'
                '兩種晶片（直線 5 顆、方格 3×3）與固定校準資料；看板 A 電路、看板 B 統計／脈衝時間軸／直方圖；自由實驗按鈕「Bell」「GHZ」「BV」「直線 5 顆」「方格 3×3」'
                '「◀ 上一階段」「下一階段 ▶」「播放脈衝」「執行 2000 shots」；回饋步驟（讀取 600 ns → FPGA 約 300 ns → 條件 π 脈衝）；校準依賴圖 11 節點'},
    {'id': 'scene_op', 'title': '互動動畫 operation.html 場景 12「一次量子計算的完整流程」', 'publisher': REPO, 'url': SRC['scene_op'],
     'usedFor': '六站（寫程式、轉譯、脈衝排程、控制電子、晶片執行 shots、判別與結果）與工作封包；插圖「一個 shot 的時間組成」：被動重置 250 μs、主動重置 2 μs、閘 = 深度 × 0.1 μs、讀取 1 μs；'
                '控制項「自動播放」「下一站 ▶」「shots N」「線路深度（層）」「主動重置（量測 + 條件 π 脈衝）」；「另加：佇列、轉譯、波形載入、網路傳輸（秒～分鐘）」'},
    {'id': 'openqasm', 'title': 'OpenQASM', 'publisher': 'Wikipedia（oldid=1305446199）', 'url': SRC['openqasm'],
     'usedFor': 'OpenQASM 是描述量子電路的語言，設計成中間表示，讓高階編譯器與量子硬體溝通；可描述依量測結果的古典前饋流程控制、指令的明確時序、附加校準用的低階定義'},
    {'id': 'fpga', 'title': 'Field-programmable gate array', 'publisher': 'Wikipedia（oldid=1385952866）', 'url': SRC['fpga'],
     'usedFor': 'FPGA 是製造後可重複程式化的可配置積體電路'},
    {'id': 'qiskit', 'title': 'Qiskit', 'publisher': 'Wikipedia（oldid=1382602577）', 'url': SRC['qiskit'],
     'usedFor': 'Qiskit 的 transpiler 把電路依特定裝置的拓撲與限制改寫並最佳化（減少閘數或深度）'},
    {'id': 'qlg', 'title': 'Quantum logic gate', 'publisher': 'Wikipedia（oldid=1376542851）', 'url': SRC['qlg'],
     'usedFor': 'SWAP 閘交換兩顆位元；電路模型中由古典電腦產生閘的組合，量子電腦像協同處理器接收「對哪些位元做哪些基本閘」的指令'},
    {'id': 'run', 'title': 'stack_race.py 在 Python 3 的實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': 'H、X、CNOT 的原生閘分解與 SWAP = 3 個 CNOT 的矩陣驗算；Bell、GHZ、BV × 直線、方格的 SWAP、CZ、總時間（與動畫 compile12 相同）且實體電路模擬結果與原始電路相同；'
                'BV 在直線晶片上換 CNOT 順序：最少 1 個 SWAP、6 個 CZ、1080 ns'},
]

SCENES = [
 ('編譯與控制軟體堆疊', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百一十一堂，編譯與控制軟體堆疊，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '這是師生對話的最後一課：前面十二課從晶片、脈衝、讀取講到演算法和錯誤更正，今天要把它們串成一條生產線。',
  '你在電腦上寫的一行程式，要經過七層軟體，才會變成某條同軸線上、某個奈秒送出的微波；讀回來的訊號，再一路翻成零和一的統計。'], ['curriculum', 'dialog']),
 ('效能競賽：誰的電路跑得快？', [
  '今天的玩法叫效能競賽：同一個電路放到兩種晶片上，比一比要插幾個交換閘、用幾個受控相位翻轉閘、總共要跑多少奈秒。',
  '晶片有兩種，五顆排成一直線，或九顆排成三乘三的方格；電路有三個，貝爾態、三顆位元的糾纏態，以及猜密碼的電路。',
  '每比完一場，就把每一層做了什麼寫下來，最後做成今天的作品：七層堆疊說明卡。'], ['curriculum', 'scene_tr']),
 ('七層軟體堆疊', [
  '最上面兩層是應用層和電路的中間表示：你用程式套件寫電路，再轉成一種跟硬體無關的量子組合語言。',
  '第三層是編譯器，負責分解、映射、路由、最佳化和排程；第四層是脈衝層，把每個閘換成校準好的波形。',
  '第五層是可程式化邏輯晶片負責的即時控制，第六層是類比硬體，第七層整理結果；旁邊還有自動校準和錯誤處理兩根支柱。'], ['dialog', 'tr_slides', 'scene_tr', 'openqasm', 'fpga']),
 ('分解：換成硬體懂的原生閘', [
  '硬體只懂三種原生閘：只改相位的旋轉、轉九十度的半個翻轉閘，以及兩顆位元之間的受控相位翻轉閘。',
  '受控反閘拆成三步：目標位元先做哈達瑪閘，接著做受控相位翻轉閘，再做一次哈達瑪閘；翻轉閘就是兩個半個翻轉閘。',
  '哈達瑪閘最後會展開成改相位、半個翻轉閘、再改相位；先留著不拆，是為了讓最佳化看得出哪些可以互相抵消。'], ['dialog', 'op_slides', 'scene_tr', 'run']),
 ('映射與路由：不相鄰就插 SWAP', [
  '映射是決定每顆邏輯位元要放在哪一顆實體位元上：編譯器查今天的校準資料，挑彼此相鄰、錯誤率最低的組合。',
  '猜密碼的電路裡，輔助位元要和另外三顆各做一次受控反閘，可是直線晶片上每顆最多只有兩個鄰居，總有一對不相鄰。',
  '這時路由就插入交換閘，把狀態搬過去，每個交換閘等於三個受控反閘；大電路要找最少的交換閘非常困難，實務上用近似的方法。'], ['dialog', 'op_slides', 'scene_tr', 'qiskit', 'qlg']),
 ('最佳化：抵消、合併、虛擬 Z', [
  '最佳化第一招是抵消：兩個哈達瑪閘中間沒有別的閘，就整對刪掉；猜密碼的電路放在直線晶片上，一共抵消了四對。',
  '第二招是合併：相鄰的相位旋轉加成一個，角度剛好是零的就直接刪掉。',
  '關鍵是相位旋轉不花時間，它只在軟體裡改後面脈衝的相位參考；真正的成本，是半個翻轉閘和受控相位翻轉閘的數量與層數。'], ['dialog', 'tr_slides', 'scene_tr', 'run']),
 ('排程與脈衝：奈秒時間軸', [
  '排程決定每個閘在第幾奈秒開始：能同時做的盡量一起做，但相鄰位元的受控相位翻轉閘不能同時做，否則會頻率碰撞。',
  '動畫裡，半個翻轉閘換成三十二奈秒的微波脈衝，受控相位翻轉閘換成四十八奈秒的磁通脈衝，讀取脈衝大約六百奈秒。',
  '每顆位元有三條線：驅動線、磁通線和讀取線；同一個猜密碼電路，在直線晶片上要一千三百二十奈秒，在方格晶片上只要八百四十奈秒。'], ['dialog', 'scene_tr', 'run']),
 ('即時控制：FPGA 幾百奈秒內回饋', [
  '第五層的即時控制，由可程式化邏輯晶片負責：所有儀器鎖在同一個一千萬赫茲的參考時鐘上，以奈秒的精度同步播放。',
  '動態電路要在中途量測，再決定下一步，例如量到一就送一個派脈衝，把位元主動重設回零態。',
  '讀取大約六百奈秒，判斷大約三百奈秒，再送出條件脈衝，整段要在一微秒左右完成；錯誤更正的即時回饋，也是同一套機制。'], ['dialog', 'scene_tr', 'scene_op', 'openqasm']),
 ('結果處理與兩根支柱', [
  '第七層整理結果：同一個電路重跑幾千次，把每次的讀取訊號判別成零或一，再用讀取誤判的統計表修正，最後回傳直方圖。',
  '第一根支柱是自動校準：從找讀取腔、找位元頻率、校派脈衝的振幅一路往下，一步失敗就退回去重做，每天甚至每小時跑一次。',
  '第二根支柱是錯誤處理：現在的機器靠錯誤緩解，多跑很多次來抵消雜訊；到了容錯時代，就靠表面碼和即時解碼器。'], ['dialog', 'scene_tr', 'scene_op']),
 ('跑程式：效能競賽計分板', [
  '教材的小程式先驗算原生閘：哈達瑪閘、翻轉閘、受控反閘換成原生閘以後，矩陣都和原本一樣，交換閘也真的等於三個受控反閘。',
  '再把三個電路放到兩種晶片上比賽，數字和動畫面板一模一樣；把編譯好的實體電路模擬一遍，結果也和原始電路相同。',
  '最後試著把三個受控反閘換個順序，直線晶片上只要一個交換閘，總時間從一千三百二十降到一千零八十奈秒。'], ['run', 'scene_tr', 'dialog']),
 ('兩小時的效能競賽', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘在軟體堆疊章比較直線和方格晶片的交換閘數與總時間，然後休息十分鐘。',
  '下半場三十分鐘，你從貝爾態、三顆位元的糾纏態、猜密碼電路裡挑一個，寫出每一層做了什麼；接著十分鐘換你教爸爸。',
  '最後五分鐘錄音總結，替七層堆疊說明卡取名字、存一個版本；今天的生活技能是：系統的每一層都有自己的責任。'], ['curriculum']),
 ('最後一關：說出七層', [
  '最後請不看稿說出：一行程式怎麼經過分解、映射、路由、最佳化、排程和脈衝，再由即時控制送到晶片上？',
  '再指出一個限制：晶片的連接方式會大幅改變交換閘的數量，交換閘越多，受控相位翻轉閘就越多，錯誤也越多。',
  '今天的作品是七層堆疊說明卡，下一課是模組發表，換你當老師；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'dialog', 'scene_tr']),
]

VISIBLE = [
 ['量子電腦學程 第一百一十一堂', '第 13 課：\n編譯與控制軟體堆疊', '從一行程式到奈秒級微波，再翻回統計', '量子第一百一十一堂  ·  依課綱製作的課前教學版'],
 ['效能競賽：誰的電路跑得快？', '同一個電路、兩種晶片，比 SWAP、CZ 與總時間',
  '01 直線 5 顆', '每顆最多\n兩個鄰居', '→', '02 方格 3×3', '位元最多\n四個鄰居', '→', '03 計分', 'SWAP、CZ 個數\n總時間（ns）',
  '今天的作品：七層堆疊說明卡'],
 ['七層軟體堆疊', '從演算法到微波，再從訊號回到統計',
  '01', '①–② 應用與電路 IR', 'Qiskit 寫電路 → OpenQASM 3（與硬體無關）',
  '02', '③–④ 編譯器與脈衝層', '分解、映射、路由、最佳化、排程 → 波形',
  '03', '⑤–⑦ 控制、硬體、結果', 'FPGA 即時控制；兩根支柱：校準與錯誤處理'],
 ['分解：換成硬體懂的原生閘', '原生閘只有 Rz、√X、CZ', '先保留 H，最佳化時才展開',
  'Rz(θ)', '只改相位，0 ns', '√X', 'X 軸轉 90°', 'CZ', '磁通脈衝', 'CNOT', 'H · CZ · H',
  'H = Rz(π/2) · √X · Rz(π/2)；X = √X · √X'],
 ['映射與路由：不相鄰就插 SWAP', 'BV（s = 111）：輔助位元要和 3 顆各做一次 CNOT',
  '映射：挑今天最好的', '相鄰、錯誤率最低的實體位元', '→', '路由：不相鄰就搬', '插入 SWAP（= 3 個 CNOT）',
  '直線晶片：2 個 SWAP，CZ 從 3 個變 9 個',
  '找最少 SWAP 很難（NP-hard），實務上用啟發式'],
 ['最佳化：抵消、合併、虛擬 Z', 'BV @ 直線：路由後 → 最佳化後',
  '01 抵消', 'H·H 相鄰就刪（4 對）', '02 合併', '相鄰 Rz 合成一個', '03 虛擬 Z', 'Rz 只改相位參考，0 ns',
  '真正的成本：√X 與 CZ 的個數和深度'],
 ['排程與脈衝：奈秒時間軸', '每顆位元三條線：XY、Z、讀取',
  'ASAP 並行  →  相鄰 CZ 錯開  →  換成波形',
  '01 √X', 'DRAG 脈衝 32 ns', '02 CZ', '磁通脈衝 48 ns', '03 讀取', '約 600 ns',
  'BV：直線 1320 ns、方格 840 ns（動畫示意值）'],
 ['即時控制：FPGA 幾百 ns 內回饋', '所有通道鎖在同一個 10 MHz 參考時鐘',
  '① 讀取 約 600 ns\n② FPGA 判斷 約 300 ns\n③ 送出條件 π 脈衝',
  '動態電路', '量到 1 就送 π 脈衝（主動重設）', 'OpenQASM 3 用 if／while 描述\n錯誤更正的回饋也是同一套',
  '整段要在約 1 μs 內完成'],
 ['結果處理與兩根支柱', '重跑數千 shot → 判別 0/1 → 修正讀取誤差 → 直方圖',
  '自動校準', '讀取腔 → 位元頻譜 → Rabi → Ramsey …\n失敗就退回上一步重做',
  '錯誤處理', '現在：錯誤緩解（多跑很多次）\n容錯時代：表面碼 + 即時解碼',
  '編譯、上傳、排隊常比在晶片上跑還久'],
 ['跑程式：效能競賽計分板', 'stack_race.py 實跑結果（純 Python）',
  '01', '原生閘驗算', 'H、X、CNOT、SWAP 全部相同 ✓',
  '02', 'BV：直線 vs 方格', 'SWAP 2 vs 0；1320 vs 840 ns',
  '03', 'CNOT 換順序', '直線只要 1 個 SWAP，1080 ns'],
 ['兩小時的效能競賽', '影片先引路，接下來編譯、比賽、寫說明卡',
  '00–25', '開場＋七層示範', '25–65', '直線 vs 方格比賽', '65–75', '休息十分鐘',
  '75–105', '挑一個電路寫七層', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：每一層都有責任'],
 ['最後一關：說出七層', '暫停影片：不看稿說一次，再指出一個限制',
  '01', '說出原理', '分解→映射→路由→最佳化→排程→脈衝',
  '02', '說出數字', 'BV：直線 2 個 SWAP、方格 0 個',
  '03', '指出一個限制', '連接方式大幅改變 SWAP 數與錯誤',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、師生對話最後一課、七層把程式翻成微波', '封面版型＋陳犀牛', '說出今天要串起來的東西'),
 ('效能競賽：兩種晶片、三個電路、比 SWAP／CZ／總時間', '三步流程卡＋黃字', '認識今天的作品'),
 ('七層與兩根支柱', '三點條列＋陳犀牛', '說卡第一欄：七層的名字'),
 ('原生閘 Rz、√X、CZ；CNOT = H·CZ·H；H 的展開', '面板四張卡＋黃字', '說卡：分解層'),
 ('映射（校準感知）、路由（SWAP = 3 CNOT）', '雙框對照＋白字＋黃字', '說卡：映射與路由'),
 ('最佳化：H·H 抵消、Rz 合併、虛擬 Z 0 ns', '三張步驟卡＋黃字', '說卡：最佳化層'),
 ('排程（相鄰 CZ 錯開）與脈衝時間軸；直線 1320 ns、方格 840 ns', '路徑一行＋三張卡＋黃字', '說卡：排程與脈衝'),
 ('即時控制：10 MHz 時鐘、動態電路、回饋約 1 μs', '左三行＋右欄＋黃字', '說卡：即時控制'),
 ('結果處理、自動校準、錯誤處理', '左右比較卡＋黃字', '說卡：結果處理與兩根支柱'),
 ('跑程式：原生閘驗算、六場比賽、換順序只要 1 個 SWAP', '三點條列＋陳犀牛', '跑程式、改 MY_CIRCUIT 與 MY_CHIP'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：原理、數字、限制；預告 Q112', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='OpenQASM, Field-programmable gate array, Qiskit and Quantum logic gate claims from Wikipedia raw wikitext fetched by the producing agent '
                      'on 2026-11-18 (verbatim quotes in production/source-notes.md); repo teaching dialogue (lesson 13), transmon and QC_Operation_Talk slide decks '
                      'and animation source (transmon-3d.html chapter 12, operation.html scene 12) read by the producing agent; native-gate identities, '
                      'SWAP/CZ/time numbers and the CNOT-reordering result from actually running stack_race.py (pure Python 3), which reimplements the '
                      'animation compile12 pipeline and matches its numbers.',
        not_verified=['√X 32 ns、CZ 48 ns、讀取 600 ns、FPGA 判斷約 300 ns 是動畫示意值；師生對話紀錄的範圍是 √X 20–40 ns、CZ 40–60 ns、讀取 0.3–1 μs，未另查特定硬體規格',
                      '10 MHz 參考時鐘、條件分支幾百 ns、校準每天甚至每小時一次、編譯上傳排隊常比跑還久，依學程師生對話紀錄與動畫，未另查廠商文件',
                      '「找最少 SWAP 是 NP-hard」「實務上用 SABRE 等啟發式」依學程師生對話紀錄，未另讀論文',
                      '課綱列的 transmon.pptx p27 實際是「一句話總結」頁；軟體堆疊內容在 p26，本集改引 p26',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

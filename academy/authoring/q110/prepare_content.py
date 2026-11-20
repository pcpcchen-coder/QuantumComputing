"""Q110 第 12 課：lattice surgery 與魔術態蒸餾 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q110/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q110', 'q110-lattice-surgery', '2026-11-18'
TITLE = 'Lattice surgery 與魔術態蒸餾'
TOPIC = '第 12 課：lattice surgery 與魔術態蒸餾'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q110/lesson.json',
    'dialog': f'{REPO} docs/超導量子電腦師生對話教學紀錄.md（第 12 課）',
    'tr_slides': f'{REPO} slides/transmon.pptx（第 25 頁：3D 第 11 章邏輯閘）',
    'scene_tr': f'{REPO} animations/transmon-3d.html#surgery（第 11 章步驟 1–8）',
    'lattice': 'https://en.wikipedia.org/wiki/Lattice_surgery',
    'magic': 'https://en.wikipedia.org/wiki/Magic_state_distillation',
    'gk': 'https://en.wikipedia.org/wiki/Gottesman%E2%80%93Knill_theorem',
    'ek': 'https://en.wikipedia.org/wiki/Eastin%E2%80%93Knill_theorem',
    'clifford': 'https://en.wikipedia.org/wiki/Clifford_gate',
    'run': f'{REPO} academy/authoring/q110/classroom.py（magic_budget.py 實跑紀錄）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q110 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（兩塊補丁合併量 X_A·X_B、三步 CNOT、T 閘傳送、15-to-1 魔術態工廠）、動手任務（在邏輯閘章依序播放合併、拆開、CNOT，再跑蒸餾統計）、'
                '孩子獨立改造（調高注入錯誤率，觀察蒸餾成功率）、好玩機制（工程答辯）、作品（邏輯閘資源估算表）、生活技能（估算成本）、'
                '120 分鐘流程、驗收與常見誤解（容錯時代的成本主要在 T 閘與魔術態工廠）'},
    {'id': 'dialog', 'title': '超導量子電腦師生對話教學紀錄 第 12 課', 'publisher': REPO, 'url': SRC['dialog'],
     'usedFor': '表面碼負責存、Clifford 用 lattice surgery、T 靠魔術態；橫向閘與 Eastin–Knill；Gottesman–Knill 與 Bell、Grover、Deutsch、BV；'
                'T = diag(1, e^{iπ/4})、Shor 需要 T；合併 → 聯合奇偶 → 量 d 輪 → 拆開、Pauli frame、拉鍊比喻、硬體動作仍是表面碼週期；'
                'CNOT 三次聯合量測、約 2～3d 輪；閘傳送一半補 S；注入 p ≈ 10⁻³；15-to-1 輸出約 35p³、兩輪約 10⁻²¹ 耗 225 顆；工廠產能決定時間；成本表'},
    {'id': 'tr_slides', 'title': 'Transmon 筆記簡報 第 25 頁', 'publisher': REPO, 'url': SRC['tr_slides'],
     'usedFor': '3D 第 11 章八個步驟摘要：不移動位元只改量哪些穩定子；邏輯 CNOT = 一塊輔助補丁 + 三次聯合量測；T 閘消耗一顆魔術態；35p³、10⁻³ 兩輪後約 10⁻²¹'},
    {'id': 'scene_tr', 'title': '互動動畫 transmon-3d.html 第 11 章「Lattice surgery 與魔術態蒸餾」', 'publisher': REPO, 'url': SRC['scene_tr'],
     'usedFor': '兩塊 d = 3 補丁 A、B 與中間一行接縫；合併時新 X 穩定子個別隨機、乘積 = X_A ⊗ X_B、量 3 輪（約 3 μs）；拆開時接縫在 Z 基底量掉；'
                'CNOT 看板四步；T 閘傳送看板；工廠 15 顆橘色球、頂上 4 盞燈、金色輸出球；看板錯誤率長條（注入、1 輪、2 輪、Shor 需要 10⁻¹⁰）；'
                '自由實驗按鈕「準備接縫」「合併（量 X_A·X_B）」「拆開」「看魔術態工廠」「跑一輪」「跑 2000 次統計」「1 輪」「2 輪」、滑桿「注入錯誤率 p」'},
    {'id': 'lattice', 'title': 'Lattice surgery', 'publisher': 'Wikipedia（oldid=1386404961）', 'url': SRC['lattice'],
     'usedFor': 'lattice surgery 是在兩顆錯誤更正過的邏輯位元之間執行邏輯閘的方法；合併與拆開；可組出邏輯 CNOT；原本為表面碼定義；已在超導位元等平台實驗展示'},
    {'id': 'magic', 'title': 'Magic state distillation', 'publisher': 'Wikipedia（oldid=1374675256）', 'url': SRC['magic'],
     'usedFor': 'Clifford 運算可在古典電腦上多項式時間模擬；Clifford 閘由 H、S、CNOT 生成；加上一個非 Clifford 運算才通用；魔術態加 Clifford 閘可做出非 Clifford 閘；'
                '蒸餾 = 從多個有雜訊的態做出更準確的態；Knill 2004 提出、Bravyi 與 Kitaev 分析；檢查不過就丟掉重來'},
    {'id': 'gk', 'title': 'Gottesman–Knill theorem', 'publisher': 'Wikipedia（oldid=1354309521）', 'url': SRC['gk'],
     'usedFor': '只由 Clifford 群的閘組成的穩定子電路，可在機率型古典電腦上以多項式時間完美模擬；Clifford 群由 CNOT、H、S 生成'},
    {'id': 'ek', 'title': 'Eastin–Knill theorem', 'publisher': 'Wikipedia（oldid=1353641779）', 'url': SRC['ek'],
     'usedFor': '沒有任何量子錯誤更正碼能橫向實作一組通用閘；橫向閘保證錯誤不會不受控制地擴散；繞過的方法包括閘傳送與魔術態蒸餾；2009 年發表'},
    {'id': 'clifford', 'title': 'Clifford gate', 'publisher': 'Wikipedia（oldid=1309382074）', 'url': SRC['clifford'],
     'usedFor': '只含 Clifford 閘的電路可被古典電腦有效率模擬；Clifford 群由 H、S、CNOT 生成；所有 Pauli 閘都是 Clifford 閘；S = diag(1, i)'},
    {'id': 'run', 'title': 'magic_budget.py 在 Python 3 的實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': 'T 閘傳送四種結果機率各 0.25、補正後全部得到 T|ψ⟩；4 個檢查下 1、2 顆出錯 0 種漏網，3 顆出錯 455 種中 35 種漏網；'
                'p = 10⁻³ 接受率 98.5%、輸出 3.5×10⁻⁸；p = 5% 接受率 46.6%；十億個 T 閘：一輪後仍預計出錯 35 次，兩輪每顆約耗 228 顆注入態'},
]

SCENES = [
 ('Lattice surgery 與魔術態蒸餾', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百一十堂，晶格手術與魔術態蒸餾，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一課的表面碼負責把一顆邏輯位元存好；可是光存不夠，要計算，還得在這些受保護的邏輯位元上做量子閘。',
  '今天看兩招：用晶格手術把兩塊表面碼縫起來再拆開，以及用蒸餾好的魔術態，做出最關鍵的四十五度相位閘。'], ['curriculum', 'dialog']),
 ('工程答辯：每個閘要多少成本？', [
  '今天的玩法叫工程答辯：你是設計容錯量子電腦的工程師，爸爸是評審，會追問每一種邏輯閘要花多少時間、多少位元。',
  '流程分三步：先看晶格手術怎麼縫合與拆開，再看四十五度相位閘怎麼靠魔術態傳送，最後跑魔術態工廠的蒸餾統計。',
  '每答出一題，就填一格邏輯閘資源估算表，這是今天的作品；答辯時還要說出每個數字是從哪裡來的。'], ['curriculum', 'scene_tr']),
 ('為什麼不能直接送脈衝？', [
  '最安全的做法叫橫向閘：每顆實體位元各做一次同樣的閘，就等於邏輯閘，錯誤不會擴散；可是有定理證明，沒有任何碼能把一整組通用閘全做成橫向。',
  '量子閘分兩類：翻轉閘、相位翻轉閘、哈達瑪閘、受控反閘這些叫克利福德閘；只用它們加上量測的電路，古典電腦都能有效率地模擬。',
  '動畫第七章的貝爾態、德意志和兩位元格羅弗電路，全都只用克利福德閘；要有量子優勢，還需要四十五度相位閘，秀爾演算法就少不了它。'], ['dialog', 'ek', 'gk', 'clifford', 'magic']),
 ('邏輯閘的價目表', [
  '把容錯時代的邏輯運算按成本排一排：翻轉閘和相位翻轉閘最便宜，只要在軟體裡記帳，幾乎不花時間。',
  '兩顆以上邏輯位元的聯合奇偶量測，用晶格手術來做，大約花碼距那麼多微秒；哈達瑪閘、受控反閘由好幾次手術組合，要花好幾倍。',
  '最貴的是四十五度相位閘，每做一次就要消耗一顆事先做好的魔術態；所以容錯時代的成本，主要花在這種閘和生產魔術態的工廠上。'], ['dialog', 'scene_tr', 'curriculum']),
 ('合併：打開接縫', [
  '動畫第十一章擺了兩塊碼距三的表面碼補丁，左邊是邏輯位元甲，右邊是邏輯位元乙，中間留著一行接縫位元。',
  '晶格手術不移動任何位元，只改變這一輪要量哪些穩定子：打開接縫上的新格子，兩塊碼就暫時變成一大塊。',
  '新出現的琥珀色格子，每一個的結果都是隨機的正一或負一，但全部乘起來，剛好等於甲和乙兩顆邏輯位元的聯合奇偶。'], ['dialog', 'tr_slides', 'scene_tr', 'lattice']),
 ('一次手術：準備、合併、拆開', [
  '一次完整的手術分三步：先把接縫位元重設到零態，再合併、連量碼距那麼多輪，最後把接縫位元量掉，拆回兩塊。',
  '合併要量好幾輪，是因為量測本身也會出錯；動畫裡量三輪，每一輪的乘積都一樣，交給解碼器確認，前後大約三微秒。',
  '拆開以後，量到的聯合奇偶留在兩顆邏輯位元上，那些隨機的個別結果只要在軟體裡記帳補正；硬體動作仍然是上一課的表面碼週期。'], ['dialog', 'scene_tr']),
 ('三次量測做出受控反閘', [
  '有了聯合奇偶量測，就能拼出受控反閘：除了控制和目標兩塊補丁，再加一塊輔助補丁，先準備在加號態。',
  '第一步縫合控制和輔助、量一種奇偶；第二步換縫合輔助和目標、量另一種奇偶，就是剛才那種合併；第三步單獨量輔助，把它拆掉。',
  '最後依三次結果在軟體裡補正，就等於對控制和目標做了受控反閘，前後大約兩到三倍碼距的週期，也就是十幾到幾十微秒。'], ['dialog', 'tr_slides', 'scene_tr', 'lattice']),
 ('T 閘：消耗一顆魔術態', [
  '四十五度相位閘沒辦法用晶格手術直接做，但可以先準備一顆魔術態，也就是加號態再轉四十五度，然後把它消耗掉。',
  '用手術量資料和魔術態的聯合奇偶，再量魔術態本身，它就被用掉了；一半機率直接得到這個閘，另一半要再補一個九十度相位閘。',
  '九十度相位閘是克利福德閘，用手術就能補；所以一個四十五度相位閘，等於一顆魔術態加上一些便宜的運算，問題變成魔術態夠不夠乾淨。'], ['dialog', 'scene_tr', 'magic', 'run']),
 ('注入與 15-to-1 蒸餾', [
  '魔術態的來源叫注入：把一顆實體位元轉到魔術態，再擴大成一整塊補丁；注入時還沒受保護，錯誤率大約千分之一，跑秀爾演算法遠遠不夠。',
  '解法是蒸餾：十五顆髒的魔術態送進工廠，跑一段只用克利福德閘的電路，量四個檢查值，全部通過才保留，有一個不對就整批丟掉。',
  '輸出只有一顆，錯誤率大約是三十五乘以輸入錯誤率的三次方：千分之一送進去，出來大約是三點五乘十的負八次方。'], ['dialog', 'tr_slides', 'scene_tr', 'magic']),
 ('跑程式：邏輯閘資源估算表', [
  '教材裡的小程式先驗算魔術態傳送：四種量測結果的機率各是四分之一，補上該補的閘以後，每一種都得到正確的結果。',
  '再把十五顆輸入的錯誤排列全部試一遍：一顆或兩顆出錯一定被抓到；三顆出錯的四百五十五種排列裡，有三十五種騙得過檢查。',
  '最後估算十億個四十五度相位閘：蒸一輪還會錯幾十次，要蒸兩輪才夠，每顆魔術態平均耗掉兩百多顆注入態。'], ['run', 'scene_tr', 'dialog']),
 ('兩小時的工程答辯', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘在第十一章依序播放合併、拆開、受控反閘，再跑蒸餾統計，然後休息十分鐘。',
  '下半場三十分鐘，你要自己把注入錯誤率調高，看接受率怎麼往下掉；接著十分鐘換你教爸爸，晶格手術和蒸餾各怎麼運作。',
  '最後五分鐘錄音總結，替邏輯閘資源估算表取名字、存一個版本；今天的生活技能是估算成本，先把帳算清楚再動工。'], ['curriculum']),
 ('最後一關：答辯邏輯閘成本', [
  '最後請不看稿說出：晶格手術怎麼量出兩顆邏輯位元的聯合奇偶？為什麼四十五度相位閘要靠魔術態？',
  '再指出一個限制：容錯時代的成本主要在四十五度相位閘和魔術態工廠，工廠的產能，常常決定整個演算法要跑多久。',
  '今天的作品是邏輯閘資源估算表，下一課是師生對話的最後一課，跟著一條電路走完編譯與控制軟體堆疊；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'dialog', 'scene_tr']),
]

VISIBLE = [
 ['量子電腦學程 第一百一十堂', '第 12 課：\nlattice surgery 與魔術態蒸餾', '縫合補丁量聯合奇偶，消耗魔術態做 T 閘', '量子第一百一十堂  ·  依課綱製作的課前教學版'],
 ['工程答辯：每個閘要多少成本？', '你是工程師，爸爸是評審，數字要說出來源',
  '01 縫合', '合併、量 d 輪\n再拆開', '→', '02 傳送', '消耗一顆魔術態\n做出 T 閘', '→', '03 蒸餾', '15 顆髒的進\n1 顆乾淨的出',
  '今天的作品：邏輯閘資源估算表'],
 ['為什麼不能直接送脈衝？', '容錯量子電腦的兩招從這裡來',
  '01', '橫向閘不夠用', 'Eastin–Knill：沒有碼能全做成橫向',
  '02', 'Clifford 閘可模擬', 'Gottesman–Knill：古典電腦能有效率模擬',
  '03', '還需要 T 閘', 'T = Z 軸轉 45°，秀爾演算法少不了'],
 ['邏輯閘的價目表', '容錯時代：每種邏輯運算的做法與代價', '成本主要花在 T 閘與魔術態工廠',
  'X、Z', '記帳，幾乎免費', '聯合量測', '手術，約 d μs', 'H、S、CNOT', '手術組合，數倍', 'T 閘', '魔術態，最貴',
  '一個 T 閘 = 消耗 1 顆魔術態 + 閘傳送'],
 ['合併：打開接縫', '兩塊 d = 3 補丁 A、B，中間一行接縫位元',
  '合併前：兩塊獨立', '各量各的穩定子', '→', '合併：暫時一大塊', '打開接縫上的新穩定子',
  '新 X 穩定子個別隨機 ±1，乘積 = X_A ⊗ X_B',
  '不移動位元，只改變「這一輪量哪些穩定子」'],
 ['一次手術：準備、合併、拆開', '準備接縫 → 合併量 d 輪 → 拆開',
  '01 準備', '接縫位元重設到 |0⟩', '02 合併', '連量 d 輪（動畫 3 輪）', '03 拆開', '接縫在 Z 基底量掉',
  '個別結果的修正只記在軟體裡（Pauli frame）'],
 ['三次量測做出受控反閘', '控制 C、輔助 A（準備在 |+⟩）、目標 T',
  '① 縫 C、A  →  ② 縫 A、T  →  ③ 量掉 A  →  補 Pauli',
  '01 量 Z_C ⊗ Z_A', '縫合控制與輔助', '02 量 X_A ⊗ X_T', '縫合輔助與目標', '03 量 A 的 Z', '拆掉輔助補丁',
  '約 2～3d 輪週期：十幾到幾十 μs'],
 ['T 閘：消耗一顆魔術態', '閘傳送：|T⟩ = T|+⟩ = (|0⟩ + e^(iπ/4)|1⟩)/√2',
  '① 準備魔術態 |T⟩\n② 量 Z_資料 ⊗ Z_魔術態\n③ 量魔術態的 X',
  '④ 看結果', '一半直接得到 T，一半補一個 S', 'S 是 Clifford，用手術就能補\nT 閘 = 1 顆魔術態 + Clifford',
  '問題變成：魔術態夠乾淨嗎？'],
 ['注入與 15-to-1 蒸餾', '輸出錯誤率約 35p³（Bravyi–Kitaev，2005）',
  '注入（髒）', '實體位元轉到 |T⟩ 再擴大\n錯誤率約 p ≈ 10⁻³',
  '15-to-1 蒸餾', '15 顆進、4 個檢查全過才留\n10⁻³ → 約 3.5×10⁻⁸',
  '不夠就再蒸一輪：約 10⁻²¹，耗 225 顆'],
 ['跑程式：邏輯閘資源估算表', 'magic_budget.py 實跑結果（純 Python）',
  '01', 'T 閘傳送 4 種結果', '補正後全部得到 T ✓',
  '02', '3 顆出錯 455 種', '35 種騙過 4 個檢查',
  '03', '10 億個 T 閘', '蒸 2 輪，每顆約耗 228 顆'],
 ['兩小時的工程答辯', '影片先引路，接下來縫、拆、蒸、算',
  '00–25', '開場＋手術與蒸餾示範', '25–65', '合併、拆開、CNOT', '65–75', '休息十分鐘',
  '75–105', '調高注入錯誤率', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：估算成本'],
 ['最後一關：答辯邏輯閘成本', '暫停影片：不看稿說一次，再指出一個限制',
  '01', '說出原理', '合併量聯合奇偶、魔術態做 T',
  '02', '說出數字', '15 顆換 1 顆，錯誤率約 35p³',
  '03', '指出一個限制', '成本主要在 T 閘與魔術態工廠',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、表面碼負責存，要算還得做邏輯閘', '封面版型＋陳犀牛', '說出今天的兩招'),
 ('工程答辯：縫合、傳送、蒸餾三步', '三步流程卡＋黃字', '認識今天的作品'),
 ('橫向閘與 Eastin–Knill、Clifford 與 Gottesman–Knill、T 閘', '三點條列＋陳犀牛', '說出為什麼需要 T 閘'),
 ('邏輯閘價目表：Pauli、聯合量測、Clifford、T', '面板四張卡＋黃字', '估算表第一欄'),
 ('合併：接縫、新 X 穩定子個別隨機、乘積 = X_A ⊗ X_B', '雙框對照＋白字＋黃字', '說出聯合奇偶'),
 ('一次手術：準備、合併量 d 輪、拆開、Pauli frame', '三張步驟卡＋黃字', '說出為什麼量 d 輪'),
 ('邏輯 CNOT：Z_C ⊗ Z_A、X_A ⊗ X_T、量 A', '路徑一行＋三張卡＋黃字', '估算表：CNOT 的時間'),
 ('T 閘傳送：魔術態、聯合量測、一半補 S', '左三行＋右欄＋黃字', '估算表：T 閘的做法'),
 ('注入 p ≈ 10⁻³、15-to-1 蒸餾 35p³、第二輪 10⁻²¹', '左右比較卡＋黃字', '估算表：魔術態的錯誤率'),
 ('跑程式：T 閘傳送驗算、35／455、十億個 T 閘的資源', '三點條列＋陳犀牛', '跑程式、改 MY_P 與 MY_T_COUNT'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：原理、數字、限制；預告 Q111', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Lattice surgery, Magic state distillation, Gottesman–Knill theorem, Eastin–Knill theorem and Clifford gate claims from Wikipedia '
                      'raw wikitext fetched by the producing agent on 2026-11-18 (verbatim quotes in production/source-notes.md); repo teaching dialogue '
                      '(lesson 12), transmon slide deck and animation source read by the producing agent; T-gate teleportation, 15-to-1 check counts, '
                      'acceptance and resource numbers from actually running magic_budget.py (pure Python 3).',
        not_verified=['35p³、兩輪約 10⁻²¹、注入約 10⁻³ 依學程師生對話紀錄與動畫，未另讀 Bravyi–Kitaev 2005 原文',
                      '合併約 d μs、CNOT 約 2～3d 輪（十幾到幾十 μs）依學程文件與動畫，未另查硬體實驗的實際時間',
                      'magic_budget.py 的 4 個檢查是 15-to-1 偵測 Z 錯誤的計數模型；騙過檢查的排列一律算成輸出有錯（保守估計），不是完整的量子電路模擬',
                      '課綱列的 transmon.pptx p26 實際是第 12 章軟體堆疊頁；lattice surgery 與魔術態內容在 p25，本集改引 p25',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

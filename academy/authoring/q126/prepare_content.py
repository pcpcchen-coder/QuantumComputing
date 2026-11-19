"""Q126 加入雜訊：八個範例在真實世界會怎樣 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q126/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q126', 'q126-noisy-examples', '2026-11-18'
TITLE = '加入雜訊：八個範例在真實世界會怎樣'
TOPIC = '加入雜訊：八個範例在真實世界會怎樣'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q126/lesson.json',
    'op_talk': f'{REPO} slides/QC_Operation_Talk.pptx（第 47 頁「錯誤預算：能跑多深的線路？」；第 48 頁「錯誤緩解：現在就能用的方法」；第 32 頁「shots 與統計誤差」）',
    'op_scene': f'{REPO} animations/operation.html#circuit（js/operation/06_circuit.js「量子線路：一步一步執行」，開關「加入雜訊（每閘 1%、讀取 3%）」與 sample()）',
    'bc_page': f'{REPO} animations/basic-circuits.html#ghz（範例 4 的重點卡：「硬體廠常用它來測試多位元糾纏的品質」）',
    'tr_bv': f'{REPO} animations/transmon-3d.html#bv（第 9 章 BV 密碼，第 8 步自由實驗的「讀取雜訊」勾選框：每顆位元 3% 的獨立誤判）',
    'fault': 'https://en.wikipedia.org/wiki/Fault_injection',
    'depol': 'https://en.wikipedia.org/wiki/Quantum_depolarizing_channel',
    'nisq': 'https://en.wikipedia.org/wiki/Noisy_intermediate-scale_quantum_computing',
    'run': f'{REPO} academy/authoring/q126/classroom.py（page_noise.py、noise_lab.py 實跑紀錄）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q126 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（在本機模擬器加入雜訊模型，觀察 Bell、GHZ、Grover 的結果如何變差）、動手任務（同一條線路跑理想與有雜訊兩種模擬，比較直方圖）、'
                '孩子獨立改造（把雜訊加倍，找出哪個範例最先看不出答案）、好玩機制（故障注入）、作品（理想 vs 雜訊比較圖）、生活技能（理論和現實的差距）、'
                '家長課前準備（qiskit-aer 雜訊模型）、120 分鐘流程、驗收與常見誤解（模擬器的雜訊模型是假設，參數要寫清楚）、下一課 Q127「專題：設計自己的線路」'},
    {'id': 'op_talk', 'title': '如何操作量子電腦（簡報）第 47、48、32 頁', 'publisher': REPO, 'url': SRC['op_talk'],
     'usedFor': '第 47 頁「錯誤預算：能跑多深的線路？」：F線路 ≈ (1 − ε1Q)^G₁ (1 − ε2Q)^G₂ (1 − εM)^n；「兩位元閘錯誤 0.3% → 約 230 個兩位元閘後成功率剩 50%」。'
                '第 48 頁「錯誤緩解」表：零雜訊外插（ZNE）「故意放大雜訊（閘折疊、拉長脈衝），外插回雜訊 0」、代價「shots 數倍；外插有偏差」；讀取誤差緩解「只修讀取」。'
                '第 32 頁：σ(P̂) = √(P(1−P)/N)（一千次一半一半約 ±1.6 個百分點）。課綱寫 p47–48，內容確實在第 47、48 頁'},
    {'id': 'op_scene', 'title': '如何操作量子電腦 3D 場景 6「量子線路：一步一步執行」', 'publisher': REPO, 'url': SRC['op_scene'],
     'usedFor': '06_circuit.js sample()：開關打開時 pg = 1 − 0.99^G（G = 線路的閘數，不含量測），每個 shot 以 pg 的機會換成均勻隨機結果，'
                '再每顆位元以 3% 翻轉；量測欄抽 1000 shots，右下插圖「量測 1000 shots 的結果（青線 = 理想機率）」；切換開關會立刻重新抽樣。'
                'GHZ 態（3 位元糾纏）：H、CX、CX 三個閘；Grover 搜尋（2 位元，找 |11⟩）：H H、CZ、H H、X X、CZ、X X、H H 共 12 個閘'},
    {'id': 'bc_page', 'title': '互動動畫：量子電路入門 範例 4 GHZ 態的重點卡', 'publisher': REPO, 'url': SRC['bc_page'],
     'usedFor': '「GHZ 電路的深度隨位元數增加，每多一顆就多一個 CNOT。硬體廠常用它來測試多位元糾纏的品質：雜訊越大，量到全 0、全 1 以外結果的比例就越高（這裡是理想模擬，所以不會出現）。」'},
    {'id': 'tr_bv', 'title': 'Transmon 3D 第 9 章 BV 密碼：自由實驗的「讀取雜訊」', 'publisher': REPO, 'url': SRC['tr_bv'],
     'usedFor': '說明「振幅由 8 維實數態向量逐閘計算（H、Z、黑盒子）；量測依 振幅² 隨機取樣。「讀取雜訊」為每顆位元 3% 的獨立誤判（示意值）。」；'
                '程式 `if (S.noisy) for (const bit of BIT9) if (Math.random() < 0.03) k ^= bit;`（只翻讀出的位元，閘不出錯）；「一鍵執行」量 50 次，「④ 量測 50 次」再累加 50 次'},
    {'id': 'fault', 'title': 'Fault injection', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['fault'],
     'usedFor': '「fault injection is a testing technique for understanding how computing systems behave when stressed in unusual ways」；'
                '軟體測試中「introducing faults to test code paths」、「widely considered to be an important part of developing robust software」'},
    {'id': 'depol', 'title': 'Quantum depolarizing channel', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['depol'],
     'usedFor': '去極化通道「a model for quantum noise」：Δλ(ρ) = (1 − λ)ρ + (λ/d)I，把狀態和最大混合態線性組合；λ = 1 時任何輸入都變成最大混合態'},
    {'id': 'nisq', 'title': 'Noisy intermediate-scale quantum computing', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['nisq'],
     'usedFor': '「they suffer from decoherence, gate errors, and measurement errors that accumulate during computation」；'
                '「Gate fidelities hover around 99-99.5% for single-qubit operations and 95–99% for two-qubit gates」（雙位元閘比單位元閘容易錯）'},
    {'id': 'run', 'title': 'page_noise.py（純 Python，沒有亂數）與 noise_lab.py（Qiskit 2.6.2 + qiskit-aer 0.18.4，seed_simulator=126）實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': '頁面規則期望值：GHZ 3 個閘 → 變成隨機 3.0%，000、111 各 44.7%，跑掉 10.7%；Grover 12 個閘 → 變成隨機 11.4%，11 為 86.2%，跑掉 13.8%；疊加跑掉 0.0%。'
                '雜訊模型（單位元閘 1%、雙位元閘 2%、讀取 3% 的假設值）：Bell、GHZ、Grover 跑掉的比例依序變大；Grover 錯誤結果 01、10 比 00 多；'
                '雜訊 ×1、×2、×4、×8 時密碼範例與 Grover 跑掉最多、疊加只有統計起伏；隱形傳態 0 的比例從 75% 往 50% 靠攏；零雜訊外插把 Grover 的 11 從 86.3% 推回 97.0%'},
]

SCENES = [
 ('加入雜訊：八個範例在真實世界會怎樣', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百二十六堂，加入雜訊：八個範例在真實世界會怎樣，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '到目前為止，八個範例都跑在完美的模擬器上，每個閘都照算、每次讀取都讀對，真實的量子電腦可沒有這麼乖。',
  '今天要問的是：如果每一步都可能出一點錯，八個範例的答案還認得出來嗎？哪一個範例最先撐不住？'], ['curriculum', 'nisq']),
 ('故障注入：故意放進錯誤', [
  '今天的好玩機制是故障注入：故意把錯誤放進系統，看它在不尋常的壓力下怎麼表現，是工程師測試系統夠不夠穩的方法。',
  '做法很簡單：同一條線路跑兩次，一次用沒有錯誤的理想模擬，一次加上雜訊模型，再把兩份直方圖並排比較。',
  '作品是一張理想和雜訊的比較圖：每個結果畫兩根柱子，一根理想、一根有雜訊，差多少一眼就看得出來。'], ['curriculum', 'fault']),
 ('雜訊模型的三個旋鈕', [
  '模擬器的雜訊模型可以想成三個旋鈕：單位元閘出錯的機會、雙位元閘出錯的機會，還有讀取時讀錯的機會。',
  '閘出錯用去極化來模擬，意思是位元的狀態有一點機會被整個打亂；讀錯就是把零看成一，或把一看成零。',
  '教材把三個旋鈕設成百分之一、百分之二和百分之三；雙位元閘比較容易錯，但這只是假設的數字，不代表任何一台真實的機器。'], ['depol', 'nisq', 'run']),
 ('錯誤預算：閘越多越吃虧', [
  '簡報第四十七頁的錯誤預算說：整條線路做對的機會，大約是每個閘都沒出錯的機會連乘起來，再乘上每次讀取都讀對的機會。',
  '它舉的例子是：雙位元閘的錯誤率千分之三，大約做兩百三十個雙位元閘之後，成功率就只剩一半。',
  '所以閘越多、位元越多，答案越容易被雜訊淹沒；八個範例的閘數不一樣，加了雜訊以後受傷的程度也不一樣。'], ['op_talk']),
 ('貝爾態與範例四：錯誤從哪裡冒出來', [
  '教材程式先跑貝爾態：理想的直方圖只有零零和一一兩根；有雜訊的那一份，兩根各少了一截，少掉的次數散到零一和一零。',
  '範例四多一顆位元、多一個受控反閘，能跑錯的結果從兩個變成六個，跑掉的比例也比貝爾態多。',
  '程式最後一行會印出跑掉的比例：把有雜訊的直方圖搬回理想的樣子，最少要搬走幾成，就是雜訊造成的傷害。'], ['run', 'bc_page']),
 ('格羅弗：十二個閘的代價', [
  '兩顆位元的格羅弗只有一個答案一一，卻要做十二個閘：一排哈達瑪閘、一次標記，再加上五步擴散。',
  '加了雜訊，格羅弗跑掉的比例比貝爾態和範例四都多；多出來的錯誤結果裡，零一和一零又比零零常見。',
  '原因是讀錯常常只錯一顆：一一錯一顆就變成零一或一零，要兩顆一起讀錯，才會變成零零。'], ['run', 'op_scene']),
 ('看不出來的雜訊', [
  '有一個範例很特別：量子硬幣本來就一半一半，被打亂以後還是一半一半，只看直方圖，完全看不出雜訊。',
  '隱形傳態量到零本來是四分之三，雜訊越大，越往一半靠攏；雜訊不只會冒出新柱子，也會把機率往平均推。',
  '所以要測雜訊，得挑答案集中、結果確定的線路；量子硬幣這種本來就隨機的線路，再壞也看不出來。'], ['run', 'depol']),
 ('容易錯的地方', [
  '第一個容易錯：模擬器的雜訊模型只是假設，比較圖上一定要寫清楚三個參數，別人才知道你的雜訊有多大。',
  '第二，別把統計誤差當成雜訊：量一千次本來就會差一兩個百分點，雜訊造成的差距比這更大，而且總是偏向同一邊。',
  '第三，答案的柱子還是最高，不代表雜訊不重要；線路一變深，錯誤會一路累積，很快就分不清答案。'], ['curriculum', 'op_talk', 'nisq']),
 ('父子共同實作：理想 vs 雜訊比較圖', [
  '上半場四十分鐘，先在三維動畫的量子線路場景，把範例四和格羅弗各跑一次理想、一次加雜訊，記下哪些柱子冒出來。',
  '接著在電腦上執行教材的雜訊程式，它會並排印出貝爾態、範例四和格羅弗的理想與雜訊兩排柱子，以及跑掉的比例。',
  '最後把三組結果畫成比較圖：理想塗灰色、雜訊塗彩色，圖的旁邊寫上三個參數和量了幾次。'], ['curriculum', 'op_scene', 'run']),
 ('換你改造：把雜訊加倍', [
  '下半場換你當故障工程師：把程式裡的放大倍數改成二、四、八，每次加倍，記下八個範例跑掉的比例。',
  '先預測哪個範例最先有一半的結果跑掉，再執行驗證；提示是數一數每個範例有幾個閘。',
  '簡報第四十八頁的零雜訊外插，就是反過來利用加倍：故意把雜訊放大，再把結果往回推到沒有雜訊的地方。'], ['curriculum', 'op_talk', 'run']),
 ('兩小時的故障注入', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘跑理想和雜訊兩種模擬、畫比較圖，然後休息十分鐘。',
  '下半場三十分鐘把雜訊一路加倍，找出最先撐不住的範例；接著十分鐘角色互換，由你教爸爸雜訊模型和比較圖。',
  '最後五分鐘錄音總結、替比較圖命名、存一個版本；今天的生活技能是理論和現實的差距：紙上的滿分，到現場常要打折。'], ['curriculum']),
 ('最後一關：故障報告', [
  '最後一關請不看稿說出：雜訊模型有哪三個旋鈕？為什麼閘越多的範例，答案掉得越多？',
  '再指出一個注意事項：模擬器的雜訊模型只是假設，參數要寫清楚，換一組參數，比較圖就會不一樣。',
  '今天的作品是理想和雜訊的比較圖，下一堂是專題：設計自己的線路；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum']),
]

VISIBLE = [
 ['量子電腦學程 第一百二十六堂', '加入雜訊\n八個範例在真實世界', '理想模擬 vs. 真實硬體', '量子第一百二十六堂  ·  依課綱製作的課前教學版'],
 ['故障注入：故意放進錯誤', '同一條線路，跑兩次',
  '01 理想', '沒有錯誤的\n模擬器', '→', '02 雜訊', '加上\n雜訊模型', '→', '03 比較', '兩份直方圖\n並排看',
  '今天的作品：理想 vs 雜訊比較圖'],
 ['雜訊模型的三個旋鈕', '教材的假設值（不代表真實機器）',
  '01', '單位元閘 1%', '去極化：狀態有機會被整個打亂',
  '02', '雙位元閘 2%', '兩顆一起被打亂，比較容易錯',
  '03', '讀取 3%', '0 看成 1，或 1 看成 0'],
 ['錯誤預算：閘越多越吃虧', '簡報 p47：做對的機會一路連乘', '每一步都要做對（教材的假設值）',
  '單位元閘', '0.99 的 G₁ 次方', '雙位元閘', '0.98 的 G₂ 次方', '讀取', '0.97 的 n 次方', '全部相乘', '≈ 整條做對的機會',
  '2Q 錯誤 0.3% → 約 230 個閘後剩一半'],
 ['貝爾態與範例四', '錯誤從哪裡冒出來',
  '貝爾態', '00、11 各少一截', '→', '範例四', '多一顆位元、多一個受控反閘',
  '可能跑錯的結果：2 個 → 6 個',
  '跑掉的比例＝搬回理想最少要搬幾成'],
 ['格羅弗：十二個閘的代價', '一個答案 11，卻要做 12 個閘',
  '貝爾態', '2 個閘', '範例四', '3 個閘', '格羅弗', '12 個閘',
  '錯誤結果：01、10 比 00 常見'],
 ['看不出來的雜訊', '雜訊會把機率往平均推',
  '量子硬幣 50%  →  打亂後還是 50%  →  看不出來',
  '疊加', '50% → 50%', '隱形傳態', '75% → 往 50% 靠', '格羅弗', '100% → 掉下來',
  '要測雜訊，挑答案確定的線路'],
 ['容易錯的地方', '雜訊、運氣和線路深度',
  '一、雜訊模型是假設，參數要寫清楚\n二、統計誤差不是雜訊\n三、答案最高不代表雜訊不重要',
  '比較圖寫上三個參數', '一千次約差 ±1.6%', '線路越深\n錯誤越累積',
  '暫停影片：寫下你最容易搞錯的一點'],
 ['父子共同實作：比較圖', 'operation.html#circuit ＋ noise_lab.py',
  '動畫', '範例四、格羅弗\n開關雜訊各跑一次',
  '程式', '貝爾態、範例四、格羅弗\n理想與雜訊並排',
  '比較圖：理想灰色、雜訊彩色、寫上參數'],
 ['換你改造：把雜訊加倍', '孩子獨立改造：當故障工程師',
  '01', '先預測', '哪個範例最先跑掉一半',
  '02', '再加倍', 'MY_SCALE = 2、4、8',
  '03', '往回推', '零雜訊外插（簡報 p48）'],
 ['兩小時的故障注入', '影片先引路，接下來跑、比、加倍',
  '00–25', '開場＋三個旋鈕', '25–65', '理想與雜訊比較圖', '65–75', '休息十分鐘',
  '75–105', '把雜訊加倍', '105–115', '換你教爸爸', '115–120', '錄音總結＋存版本',
  '今日生活技能：理論和現實的差距'],
 ['最後一關：故障報告', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '三個旋鈕', '單位元閘、雙位元閘、讀取',
  '02', '閘越多越吃虧', '每個閘都要做對',
  '03', '一個注意事項', '雜訊模型是假設，參數要寫清楚',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、八個範例都跑在完美模擬器、今天的問題', '封面版型＋陳犀牛', '說出今天要做的作品'),
 ('故障注入：理想、雜訊、比較；理想 vs 雜訊比較圖', '三步流程卡＋黃字', '寫下自己的預測'),
 ('雜訊模型三個旋鈕：單位元閘 1%、雙位元閘 2%、讀取 3%（假設值）；去極化', '三點條列＋陳犀牛', '把三個參數抄在比較圖角落'),
 ('錯誤預算（QC_Operation_Talk 第 47 頁）：連乘；0.3% → 約 230 個雙位元閘剩一半', '面板四張卡＋黃字', '數一數每個範例幾個閘'),
 ('Bell 與 GHZ：錯誤結果 2 個 → 6 個；跑掉的比例', '雙框對照＋白字＋黃字', '讀出程式印的跑掉比例'),
 ('Grover 12 個閘；01、10 比 00 常見（讀錯一顆）', '三張步驟卡＋黃字', '找出最常見的錯誤結果'),
 ('疊加看不出雜訊；隱形傳態往 50% 靠；要測雜訊挑答案確定的線路', '路徑一行＋三張卡＋黃字', '比較疊加和 Grover'),
 ('容易錯：參數要寫清楚、統計誤差不是雜訊、線路越深錯誤越累積', '左三行＋右欄＋黃字', '寫在比較圖背面'),
 ('父子共同實作：operation.html#circuit 開關雜訊；noise_lab.py 比較圖', '左右比較卡＋黃字', '完成理想 vs 雜訊比較圖'),
 ('獨立改造：MY_SCALE = 2、4、8；零雜訊外插（第 48 頁）', '三點條列＋陳犀牛', '找出最先跑掉一半的範例'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：三個旋鈕、閘越多越吃虧、雜訊模型是假設；預告 Q127', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Fault injection, Quantum depolarizing channel and Noisy intermediate-scale quantum computing claims from Wikipedia raw wikitext fetched by the '
                      'producing agent on 2026-11-19 (verbatim quotes in production/source-notes.md); repo slides (QC_Operation_Talk.pptx pages 47, 48, 32) '
                      'and animation source (operation.html scene 6 circuit: 06_circuit.js sample() noise rule; basic-circuits.html GHZ takeaway card; '
                      'transmon-3d.html chapter 9 free-experiment readout-noise checkbox) read by the producing agent and checked with Playwright screenshots; '
                      'page_noise.py run with Python 3.13 (no randomness, exact expectation of the page rule); noise_lab.py run with Qiskit 2.6.2 and '
                      'qiskit-aer 0.18.4 (seed_simulator=126); the noise model parameters (1%, 2%, 3%) are stated as assumptions, not hardware data.',
        not_verified=['雜訊模型的參數（單位元閘 1%、雙位元閘 2%、讀取 3%）是教學用的假設，不代表任何一台真實的量子電腦；真實硬體還有相干誤差、串擾、洩漏等本課沒有模擬的雜訊',
                      '頁面（operation.html#circuit）的雜訊規則是「出錯就整個變成均勻隨機」的簡化版，和 qiskit-aer 的逐閘去極化不同，兩者的數字接近但不相等',
                      '「跑掉的比例」是兩份分布差的一半（總變異距離），含統計起伏；疊加範例的 0.5% 是一萬次的抽樣起伏，期望值是 0',
                      '零雜訊外插只示範最簡單的直線外插；簡報第 48 頁提醒外插有偏差、shots 要數倍',
                      'Qiskit 只用 2.6.2、qiskit-aer 只用 0.18.4 實跑；課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

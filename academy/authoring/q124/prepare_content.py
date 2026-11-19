"""Q124 用 Qiskit 重現八個範例 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q124/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q124', 'q124-qiskit-eight', '2026-11-18'
TITLE = '用 Qiskit 重現八個範例'
TOPIC = '用 Qiskit 重現八個範例'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q124/lesson.json',
    'bc_page': f'{REPO} animations/basic-circuits.html（八個範例；每頁底部「Qiskit 程式碼（會隨上面的選項改變）」區塊由 qiskitCode() 產生；頁尾「和 Qiskit 的 Statevector 結果一致」；README.md「74 種選項組合都已和 Qiskit Statevector 比對過」）',
    'bc_talk': f'{REPO} slides/output/basic-circuits.pptx（第 28 頁「互動動畫：逐步播放、自己量測」；第 29 頁「頁面底部附會隨選項改變的 Qiskit 程式碼，可以複製到自己的電腦執行」；原始稿 slides/reports/basic-circuits.js）',
    'op_talk': f'{REPO} slides/QC_Operation_Talk.pptx（第 27 頁「實際操作：用 Qiskit 跑一個 Bell 態」與備註；第 28 頁動態線路 if_test）',
    'qiskit': 'https://en.wikipedia.org/wiki/Qiskit',
    'jupyter': 'https://en.wikipedia.org/wiki/Project_Jupyter',
    'run': f'{REPO} academy/authoring/q124/classroom.py（eight_examples.py、check_eight.py 實跑紀錄；74 種組合比對）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q124 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（在本機模擬器重現八個範例，與頁內結果比對）、動手任務（照頁面附的 Qiskit 程式碼建立線路，用 Statevector 與 shots 各跑一次）、'
                '孩子獨立改造（把其中一個範例改成自己的參數再比對）、好玩機制（Release 任務）、作品（八範例 notebook）、生活技能（用工具驗證結果）、'
                '家長課前準備（安裝 Python、qiskit、qiskit-aer）、120 分鐘流程、驗收與常見誤解（頁面已用 Statevector 比對 74 種組合；自己的版本也要比對，不要只看圖）'},
    {'id': 'bc_page', 'title': '互動動畫：量子電路入門 八個基礎量子電路（basic-circuits.html）', 'publisher': REPO, 'url': SRC['bc_page'],
     'usedFor': '八個範例的預設選項與理論機率（頁面引擎 simulate／marginal 用 Node 實算）；程式碼區塊 summary「Qiskit 程式碼（會隨上面的選項改變）」、「複製程式碼」按鈕、'
                '「需要 pip install qiskit（Qiskit 1.x 或 2.x）」；程式碼用 QuantumCircuit(n, m)、StatevectorSampler().run([qc], shots=1000)、.data.c.get_counts()、'
                '「位元字串的最右邊是 q0」；隱形傳態註解「真實硬體會先量測 q0、q1，再依結果做 X、Z（動態電路）；這裡用受控閘代替，結果相同」；'
                'Grover 擴散註解「這樣接會多一個整體負號，不影響機率」；頁尾「所有振幅都由頁面內建的狀態向量模擬器即時計算，和 Qiskit 的 Statevector 結果一致」；'
                '量測卡「灰色底是理論機率，綠色是實際次數」、按鈕「量測 1,000 次」「清除」；選項組合數 2+2+4+2+4+4+8+48 = 74'},
    {'id': 'bc_talk', 'title': '量子電路入門：八個範例（簡報）第 28–29 頁', 'publisher': REPO, 'url': SRC['bc_talk'],
     'usedFor': '第 28 頁：右下可以量測 1 次或 1,000 次，灰底是理論機率、綠色是實際次數。第 29 頁：Deutsch 四種函數、BV 共 8 種密碼可切換；'
                '「頁面底部附會隨選項改變的 Qiskit 程式碼，可以複製到自己的電腦執行」（課綱頁碼 p28–29 正確）'},
    {'id': 'op_talk', 'title': '如何操作量子電腦（簡報）第 27、28 頁', 'publisher': REPO, 'url': SRC['op_talk'],
     'usedFor': '第 27 頁：用 Qiskit 跑 Bell 態三段（寫線路、選後端轉譯、執行 1000 shots 取回計數），程式用 qc.measure_all() 與 .data.meas.get_counts()；'
                '「理想：00、11 各 50%；01、10 出現 = 雜訊」；備註「程式介面依版本會調整，實際使用時以官方文件為準」。第 28 頁：動態線路「量測 q0，若為 1 則對 q1 做 X」（if_test）'},
    {'id': 'qiskit', 'title': 'Qiskit', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['qiskit'],
     'usedFor': '「open-source, Python-based … software stack for quantum computing」；可在量子電腦或 classical simulators 上執行；primitives（samplers、estimators）可用本機模擬器；'
                'quantum information module；Qiskit Aer（qiskit-aer）「A high-performance simulator for quantum circuits」「frequently used to validate algorithms before running on actual quantum processors」'},
    {'id': 'jupyter', 'title': 'Project Jupyter（Jupyter Notebook 一節）', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['jupyter'],
     'usedFor': 'notebook 是「an ordered list of input/output cells which can contain code, text … mathematics, plots」；Visual Studio Code 支援在本機編輯 Jupyter notebooks'},
    {'id': 'run', 'title': 'eight_examples.py（Qiskit 2.6.2、qiskit-aer 0.18.4）、check_eight.py（純 Python）與 74 種組合比對實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': '八個預設範例 Statevector 理論機率 8／8 和頁面一致：疊加 0、1 各 50%；干涉 1 為 100%；Bell 00、11 各 50%；GHZ 000、111 各 50%；隱形傳態 q2 的 0 為 75%、1 為 25%；'
                'Deutsch（f(x) = x）1 為 100%；BV 101 為 100%；Grover（2 顆、答案 11、1 輪）11 為 100%。StatevectorSampler(seed=2026) 1000 shots：三個各半的範例次數完全相同（同一串亂數）；'
                '頁面 74 種選項組合的程式碼逐一在 Qiskit 執行，機率 74／74 一致（最大差 3e-15）；比振幅時 46 種相同、28 種差一個整體負號，28 種全是 Grover 奇數輪（1 輪 16 種、3 輪 12 種），偶數輪 20 種相同；'
                '改造：BV 密碼 011 → 011 為 100%；隱形傳態角度 π/2 → 0、1 各 50%（= sin²(π/4)）'},
]

SCENES = [
 ('用 Qiskit 重現八個範例', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百二十四堂，用程式套件重現八個範例，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '從第一百一十三堂開始，我們在瀏覽器裡把八個範例一個一個看完；今天要把它們全部搬進自己的電腦，用程式再跑一遍。',
  '今天記住一句話：圖看起來對還不算數，算出來的數字和頁面對得上，才算真的重現。'], ['curriculum', 'bc_page']),
 ('Release 任務：八格全勾才發布', [
  '今天的好玩機制是發布任務：就像軟體公司推出新版本以前，每一項都要過檢查，才能貼上版本一點零的標籤。',
  '我們的檢查表有八格，每個範例都用兩種方式跑，結果和頁面一致才打勾，八格全部打勾才算發布成功。',
  '作品叫八範例筆記本，每個範例一格程式、一格說明，最後存成第一個正式版本。'], ['curriculum']),
 ('從頁面到筆記本', [
  '程式從哪裡來？線路入門動畫的每個範例頁，最底下都有一個可以展開的程式碼區塊，旁邊還有複製按鈕。',
  '這段程式會跟著上面的選項一起改變，換了密碼或換了位元數，程式裡的閘也會跟著換。',
  '筆記本是一種可以一格一格執行的檔案，把八段程式各貼進一格，按一格就跑一格，輸出直接留在那一格下面。'], ['bc_page', 'bc_talk', 'jupyter']),
 ('同一條線路，跑兩次', [
  '每個範例都跑兩次：第一次用狀態向量，不做量測，直接算出每種結果的理論機率。',
  '第二次真的量一千次，數每種結果出現幾次，就像在頁面上按量測一千次那個按鈕。',
  '比對的標準不一樣：狀態向量要和頁面灰色底的理論機率一模一樣，量一千次的次數只要接近就好。'], ['curriculum', 'bc_page', 'bc_talk', 'qiskit']),
 ('範例 1–4：機率對得上嗎', [
  '先看前四個：量子硬幣是零和一各一半；干涉範例中間有相位翻轉閘，量到一的機率是百分之百。',
  '貝爾態只有零零和一一各一半；範例四把三顆串在一起，只有全零和全一各一半。',
  '量一千次的時候，一半一半的結果不會剛好各五百次，這很正常；要看的是狀態向量那一欄有沒有完全對上。'], ['bc_page', 'run']),
 ('範例 5–8：預設選項', [
  '隱形傳態只量編號二，量到零的機率是四分之三、量到一是四分之一，正好是要傳過去的那個狀態。',
  '德意志範例預設的黑盒子是平衡的，所以一定量到一；密碼範例預設的密碼是一零一，理論機率也全部落在一零一。',
  '格羅弗範例是兩顆位元、答案一一，只做一輪，就把答案的機率推到百分之百。'], ['bc_page', 'run']),
 ('我們真的跑了：8 個與 74 種', [
  '我們真的在電腦上跑了一次：八個預設範例的理論機率，八個全部和頁面一模一樣。',
  '再把頁面所有選項的組合都試一遍，一共七十四種，機率也是七十四種全部一致。',
  '如果改成比振幅，有二十八種差了一個整體負號，全部是格羅弗跑奇數輪的情況；負號量不到，所以機率還是一樣。'], ['bc_page', 'run']),
 ('容易錯的地方', [
  '第一個容易錯的地方：頁面的程式先建好紀錄格再量測；如果改成一次量全部的寫法，存結果的名字會換掉，取次數那一行也要跟著改。',
  '第二，固定亂數種子以後，三個一半一半的範例會印出一模一樣的次數，這不是巧合，是同一串亂數被重複使用。',
  '第三，量一千次的次數每次都會跳動，只看直方圖的高低很容易被騙，一定要拿狀態向量算出的數字來比。'], ['op_talk', 'bc_page', 'run']),
 ('父子共同實作：八格檢查表', [
  '上半場四十分鐘，爸爸先在終端機裝好兩個套件，你負責從頁面複製程式碼，一個範例貼進一格。',
  '每一格都用狀態向量和量一千次各跑一次，再把理論機率抄進檢查表，和頁面灰色底一格一格對。',
  '八格都打勾以後，再換成本機的高效能模擬器重跑一次，看看次數雖然不同，分布是不是一樣。'], ['curriculum', 'qiskit', 'run']),
 ('換你改造：換成自己的參數', [
  '下半場換你改造：挑一個範例換成自己的參數，例如把密碼改成零一一，或把隱形傳態的角度改成二分之圓周率。',
  '改之前先寫下預測；密碼範例可以到頁面點成同一組密碼再比，角度頁面沒有，就拿公式算出的機率來對。',
  '這就是今天的注意事項：頁面已經替七十四種組合對過答案，但你改過的版本沒人檢查過，自己也要比對，不能只看圖。'], ['curriculum', 'bc_page', 'run']),
 ('兩小時的發布任務', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘父子一起把八個範例貼進筆記本、兩種跑法各跑一次，然後休息十分鐘。',
  '下半場三十分鐘換你改參數再比對；接著十分鐘角色互換，由你教爸爸怎麼操作、為什麼結果是這樣。',
  '最後五分鐘錄音總結、替筆記本命名、存成第一版；今天的生活技能是用工具驗證結果。'], ['curriculum']),
 ('最後一關：發布前的答辯', [
  '最後一關請不看稿說出：狀態向量和量一千次差在哪裡？為什麼比對的時候要以狀態向量為準？',
  '再指出一個注意事項：格羅弗的振幅可能整體差一個負號，這量不到，所以比對時要比機率，不要直接比振幅。',
  '今天的作品是八範例筆記本，下一堂要用頁面上的量測按鈕，比一比量一次和量一千次有什麼不同；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'run']),
]

VISIBLE = [
 ['量子電腦學程 第一百二十四堂', '用 Qiskit\n重現八個範例', '本機模擬器跑一遍，和頁內結果比對', '量子第一百二十四堂  ·  依課綱製作的課前教學版'],
 ['Release 任務：八格全勾才發布', '每個範例都要過檢查',
  '01 重現', '八個範例\n各跑兩種方式', '→', '02 比對', '和頁面的\n理論機率比', '→', '03 發布', '八格全勾\n存成 v1.0',
  '今天的作品：八範例 notebook'],
 ['從頁面到筆記本', 'basic-circuits.html 每頁底部都有程式碼',
  '01', '程式碼區塊', '展開就看得到，可以一鍵複製',
  '02', '跟著選項改變', '換密碼、換位元數，閘也跟著換',
  '03', 'notebook', '一格程式、一格說明，逐格執行'],
 ['同一條線路，跑兩次', 'eight_examples.py 的做法', 'Statevector 與 shots',
  'Statevector', '不量測，直接算', '對照', '頁面灰色底', 'shots = 1000', '真的抽樣一千次', '對照', '頁面綠色柱',
  '理論要一模一樣；次數只會接近'],
 ['範例 1–4：機率對得上嗎', '預設選項，Statevector 理論機率',
  '範例 1、2', '疊加 0／1 各 50%；干涉 1：100%', '→', '範例 3、4', 'Bell 00／11、GHZ 000／111 各 50%',
  '和頁面灰色底一字不差',
  '量一千次：接近一半，不會剛好'],
 ['範例 5–8：預設選項', '位元字串最右邊是 q0',
  '05 隱形傳態', '只量 q2：0 75%、1 25%', '06–07 Deutsch、BV', 'f(x)=x → 1；密碼 101', '08 Grover', '2 顆、答案 11：100%',
  '八個範例都要在 notebook 留下輸出'],
 ['我們真的跑了：8 個與 74 種', 'Qiskit 2.6.2 · qiskit-aer 0.18.4',
  '頁面程式碼  →  Statevector  →  和頁面比  →  打勾',
  '8／8', '預設範例全部對上', '74／74', '所有選項組合機率一致', '28 種', 'Grover 奇數輪差整體負號',
  '機率一樣，振幅可能差一個負號'],
 ['容易錯的地方', '發布前再檢查一次',
  '一、measure_all 的紀錄叫 meas\n二、固定種子，次數會重複\n三、shots 會跳動，別只看圖',
  '頁面程式用 data.c', '隱形傳態只量 q2', 'Grover 振幅\n可能整體變號',
  '暫停影片：寫下你最容易搞錯的一點'],
 ['父子共同實作：八格檢查表', 'pip install qiskit qiskit-aer',
  '複製', '八個程式碼區塊\n貼進 notebook 八格',
  '比對', 'Statevector、shots\n各跑一次再打勾',
  '再用 qiskit-aer 重跑一遍'],
 ['換你改造：換成自己的參數', '孩子獨立改造：先預測，再比對',
  '01', '換密碼', 'BV 改成 011，頁面也點成 011',
  '02', '換角度', '隱形傳態 ry 改成 π/2',
  '03', '自己比對', '用 Statevector 對數字，不只看圖'],
 ['兩小時的發布任務', '影片先引路，接下來重現、比對、改造',
  '00–25', '開場＋兩種跑法', '25–65', '八個範例貼進 notebook', '65–75', '休息十分鐘',
  '75–105', '改成自己的參數再比對', '105–115', '換你教爸爸', '115–120', '錄音總結＋存成 v1.0',
  '今日生活技能：用工具驗證結果'],
 ['最後一關：發布前的答辯', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '兩種跑法', 'Statevector 和 shots 差在哪',
  '02', '以誰為準', '理論機率要一模一樣',
  '03', '一個注意事項', '比機率，不直接比振幅',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從瀏覽器搬到自己的電腦、今天的一句話', '封面版型＋陳犀牛', '說出今天要做的作品'),
 ('Release 任務：重現、比對、發布；八格檢查表', '三步流程卡＋黃字', '畫出八格檢查表'),
 ('頁面程式碼區塊（basic-circuits.pptx 第 29 頁）、會隨選項改變、notebook 逐格執行', '三點條列＋陳犀牛', '找到第一個範例的程式碼區塊'),
 ('兩種跑法：Statevector 對灰色底、shots 對綠色柱', '面板四張卡＋黃字', '說出兩種跑法的差別'),
 ('範例 1–4 的理論機率', '雙框對照＋白字＋黃字', '勾前四格'),
 ('範例 5–8 的理論機率', '三張步驟卡＋黃字', '勾後四格'),
 ('實跑：8／8、74／74、28 種整體負號', '路徑一行＋三張卡＋黃字', '對照自己的輸出'),
 ('容易錯：measure_all 的 meas、固定種子、shots 跳動；隱形傳態只量 q2；Grover 整體負號', '左三行＋右欄＋黃字', '寫在檢查表背面'),
 ('父子共同實作：複製八段程式、兩種跑法、qiskit-aer 重跑', '左右比較卡＋黃字', '八格全勾'),
 ('獨立改造：BV 密碼 011、隱形傳態角度 π/2、自己比對', '三點條列＋陳犀牛', '改一個參數並比對'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：兩種跑法、以理論機率為準、比機率不比振幅；預告 Q125', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Qiskit and Project Jupyter claims from Wikipedia raw wikitext fetched by the producing agent on 2026-11-19 '
                      '(verbatim quotes in production/source-notes.md); repo slides (basic-circuits.pptx pages 28-29, QC_Operation_Talk.pptx pages 27-28, '
                      'with notes) and animation source (basic-circuits.html engine: SCENES, simulate, marginal, qiskitCode; page footer; README) read by the '
                      'producing agent and checked with Playwright screenshots; the page engine was run in Node to list all 74 option combinations with their '
                      'probabilities and generated Qiskit code, each generated program was executed with Qiskit 2.6.2 Statevector and compared '
                      '(74/74 probabilities equal, 28 Grover odd-round cases differ by a global sign in amplitude); eight_examples.py run with Qiskit 2.6.2 '
                      '(StatevectorSampler seed=2026) and qiskit-aer 0.18.4 (seed_simulator=2026); check_eight.py (pure Python 3.13.18, no randomness).',
        not_verified=['Qiskit 1.x 與更舊版本未實測；只用 Qiskit 2.6.2 與 qiskit-aer 0.18.4 跑過（頁面寫「Qiskit 1.x 或 2.x」）',
                      '「軟體公司推出新版本以前每一項都要過檢查」是一般比喻，未引文獻',
                      '未在 Jupyter／VS Code 介面中實際開啟 八範例.ipynb；只確認它是合法的 nbformat 4 JSON，且各程式格串起來用 Qiskit 2.6.2 執行結果與 eight_examples.py 相同',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

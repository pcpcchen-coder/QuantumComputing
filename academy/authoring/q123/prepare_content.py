"""Q123 古典 vs 量子：要查幾次？ — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q123/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q123', 'q123-query-count', '2026-11-18'
TITLE = '古典 vs 量子：要查幾次？'
TOPIC = '古典 vs 量子：要查幾次？'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q123/lesson.json',
    'bc_talk': f'{REPO} slides/output/basic-circuits.pptx（第 30 頁「古典 vs 量子：要查幾次？」表格與備註；第 26 頁 √N 表格；原始稿 slides/reports/basic-circuits.js）',
    'op_talk': f'{REPO} slides/QC_Operation_Talk.pptx（第 42 頁「快在哪？加速的等級」與備註；第 45 頁「哪些事不會變快」；第 39、40 頁 Deutsch–Jozsa、Grover）',
    'scene_int': f'{REPO} animations/operation.html#interference（animations/js/operation/08_interference.js：模式 B「3 位元：8 條路徑（Deutsch–Jozsa）」，readout「f(x) = 1 的有 k 個」「古典最壞要查 2ⁿ⁻¹+1 = 5 次」）',
    'scene_bv': f'{REPO} animations/transmon-3d.html#bv（第 9 章：步驟 1「題目與古典做法」classicalQuery 依序問 100、010、001；步驟 5「量測」看板「量子：查詢 1 次」「古典：查詢 3 次（n 位元要 n 次）」）',
    'scene_gr': f'{REPO} animations/operation.html#grover（animations/js/operation/09_grover.js：「量子位元數 n」、readout「最佳輪數 ≈ (π/4)√N」「古典平均要查 N/2 次」、「自動跑到最佳次數」）',
    'dj': 'https://en.wikipedia.org/wiki/Deutsch%E2%80%93Jozsa_algorithm',
    'bv': 'https://en.wikipedia.org/wiki/Bernstein%E2%80%93Vazirani_algorithm',
    'grover': "https://en.wikipedia.org/wiki/Grover%27s_algorithm",
    'shor': "https://en.wikipedia.org/wiki/Shor%27s_algorithm",
    'run': f'{REPO} academy/authoring/q123/classroom.py（query_count.py、qiskit_check.py 實跑紀錄）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q123 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（整理 Deutsch、BV、Grover 的古典與量子查詢次數，分辨加速大小）、動手任務（做一張查詢次數比較表並用動畫驗證其中三格）、'
                '孩子獨立改造（找一個量子沒有優勢的問題，說明原因）、好玩機制（工程答辯）、作品（查詢次數比較表）、生活技能（用數字比較）、'
                '120 分鐘流程、驗收與常見誤解（查詢次數少不等於總時間少；還要算讀取與重複次數）'},
    {'id': 'bc_talk', 'title': '量子電路入門：八個範例（簡報）第 30、26 頁', 'publisher': REPO, 'url': SRC['bc_talk'],
     'usedFor': '第 30 頁表格：Deutsch「f(x)，x 是 1 個位元」古典 2 次、量子 1 次；Deutsch–Jozsa（n 位元）「最壞 2ⁿ⁻¹ + 1 次」、量子 1 次；'
                'Bernstein–Vazirani「s·x（mod 2）」「n 次（每次問一位）」、量子 1 次；Grover「x 是不是答案」「平均約 N/2 次」「約 (π/4)√N 輪」；'
                '「前三個是同一個套路：疊加 → 黑盒把答案寫進正負號 → H 干涉；Grover 則要重複約 √N 輪」；備註「用 001、010、100 去問，需要 n 次」「是黑盒查詢次數的比較 … 還不是實用的應用」。'
                '第 26 頁：N = 8 古典平均 4.5 次、2 輪；N = 1,024 古典平均 512.5 次、25 輪、99.9%；備註「平均要試 N 加 1 除以 2 次」'},
    {'id': 'op_talk', 'title': '如何操作量子電腦（簡報）第 39、40、42、45 頁', 'publisher': REPO, 'url': SRC['op_talk'],
     'usedFor': '第 42 頁「快在哪？加速的等級」：質因數分解古典 exp(O(n^1/3 (log n)^2/3))、量子 O(n³) 左右、超多項式（指數級）；量子系統模擬「指數級（多數情況）」；'
                '無結構搜尋 O(N) → O(√N)「平方」；蒙地卡羅「平方」；「平方加速：差距是 N 和 √N，好處要在 N 很大時才顯現，而且容易被量子閘較慢、錯誤更正的開銷吃掉」'
                '「實際比較要算總時間：shots、錯誤更正、資料載入」；備註「古典最好的一般數域篩法是次指數時間，Shor 是多項式時間」。'
                '第 45 頁「哪些事不會變快」：資料輸入約 N 步、資料輸出只讀 n 位元、「加減乘除、排序、資料庫查詢、渲染、文書：沒有已知的量子加速」、小規模問題、'
                '「最適合量子電腦的問題是『輸入小、計算難、輸出小』」，備註舉分解質因數為例。第 40 頁「N = 10⁶ 時，古典平均 50 萬次，Grover ~785 次」；第 39 頁 Deutsch–Jozsa 與 BV 古典次數'},
    {'id': 'scene_int', 'title': '互動動畫：如何操作量子電腦（operation.html）場景 8 干涉', 'publisher': REPO, 'url': SRC['scene_int'],
     'usedFor': 'Playwright 實拍模式 B：平衡 f = x₀「有 4 個」P(000) = 0.000；常數 f = 0「有 0 個」P(000) = 1.000；常數 f = 1「有 8 個」振幅 −1.000、P(000) = 1.000；'
                '平衡 f = 奇偶「有 4 個」P(000) = 0.000；readout 一直寫「（古典最壞要查 2ⁿ⁻¹+1 = 5 次）」'},
    {'id': 'scene_bv', 'title': '互動動畫 transmon-3d.html 第 9 章 BV 密碼（步驟 1、5）', 'publisher': REPO, 'url': SRC['scene_bv'],
     'usedFor': '步驟 1：字幕「它只回答 s·x 的奇偶」；看板「古典第 1 次：x = 100 → 回答 1」「x = 010 → 回答 0」「x = 001 → 回答 1」「古典問了 3 次才知道 s = 101」；'
                '字幕「古典要問 3 次；n 位元密碼就要 n 次」。步驟 5：量 50 次「101（50/50）」；看板「量子：查詢 1 次 → s = 101」「古典：查詢 3 次（n 位元要 n 次）」'},
    {'id': 'scene_gr', 'title': '互動動畫：如何操作量子電腦（operation.html）場景 9 Grover 搜尋', 'publisher': REPO, 'url': SRC['scene_gr'],
     'usedFor': 'Playwright 實拍 readout：n = 2「N = 4 … ≈ 1　古典平均要查 2 次」、n = 4「N = 16 … ≈ 3　古典平均要查 8 次」、n = 6「N = 64 … ≈ 6　古典平均要查 32 次」；'
                '自動跑到最佳次數 P = 0.135、0.344、0.591、0.816、0.964、0.997；Oracle 階段顯示粉紅色平均面；右下白點停在曲線頂端'},
    {'id': 'dj', 'title': 'Deutsch–Jozsa algorithm', 'publisher': 'Wikipedia（oldid=1381683602）', 'url': SRC['dj'],
     'usedFor': '古典決定性演算法最壞要 2^(n−1) + 1 次（「just over half the set of inputs must be evaluated」）；隨機演算法常數 k 次就高機率答對；'
                '量子一次查詢永遠答對；「of little practical use」；機率型古典電腦容易解，所以沒有和 BPP 分開'},
    {'id': 'bv', 'title': 'Bernstein–Vazirani algorithm', 'publisher': 'Wikipedia（oldid=1371471620）', 'url': SRC['bv'],
     'usedFor': 'f(x) = x·s mod 2；古典最有效率是用 x = 2^i 問 n 次；「at least n queries」；量子只要 1 次；機率型也要 Ω(n) 次'},
    {'id': 'grover', 'title': "Grover's algorithm", 'publisher': 'Wikipedia（oldid=1385418712）', 'url': SRC['grover'],
     'usedFor': '古典平均 N/2 步；O(√N) 次；只有平方加速；BBBV 證明漸近最佳；「the quadratic speedup achieved is too modest to overcome the large overhead of near-term quantum computers」'},
    {'id': 'shor', 'title': "Shor's algorithm", 'publisher': 'Wikipedia（oldid=1384103273）', 'url': SRC['shor'],
     'usedFor': 'Shor 在量子電腦上是多項式時間；最好的古典演算法一般數域篩法是次指數時間；目前沒有已知的古典多項式時間分解法'},
    {'id': 'run', 'title': 'query_count.py（純 Python）與 qiskit_check.py（Qiskit 2.6.2）實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': 'Deutsch 四種黑盒：古典 2 次、量子 1 次全對；3 位元 Deutsch–Jozsa 72 台機器（常數 2、平衡 70）量子各 1 次全部判對；古典前 4 個都回答 0 仍可能平衡 → 最壞 5 次；'
                '隨機抽 2／3／4 個不同輸入誤判平衡機器的機率 42.9%／14.3%／2.9%；BV 8 種密碼古典 3 次、量子 1 次全中；'
                'Grover N = 4／8／16／64／1,024 古典平均 2.5／4.5／8.5／32.5／512.5 次、最佳 1／2／3／6／25 輪、成功率 100／94.5／96.1／99.7／99.9%；'
                '10 位元：Deutsch–Jozsa 古典最壞 513 次、BV 10 次、Grover 512.5 次 vs 25 輪；Qiskit 理論機率 100%、0%、100%、94.5%'},
]

SCENES = [
 ('古典 vs 量子：要查幾次？', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百二十三堂，古典和量子要查幾次，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '前面幾堂分別認識了德意志、密碼猜謎和格羅弗搜尋；今天不學新線路，而是把它們排在同一張表上比一比。',
  '今天要記住一句話：量子快多少要看問題的結構，有的快到只問一次，有的只快一個平方根，有的根本沒有變快。'], ['curriculum', 'bc_talk']),
 ('工程答辯：查詢次數比較表', [
  '今天的好玩機制是工程答辯：爸爸當評審，孩子每填一格表，都要說出依據，還要用動畫或小程式證明。',
  '作品叫查詢次數比較表，每一列是一個問題，欄位寫黑盒子回答什麼、古典要問幾次、量子要問幾次、加速屬於哪一級。',
  '表的最後一欄留給動畫驗證，今天至少要打三個勾，分別對應德意志、密碼和搜尋這三列。'], ['curriculum', 'bc_talk']),
 ('什麼叫「查一次」', [
  '先講清楚什麼叫查一次：黑盒子像一台只能投幣發問的機器，看不到裡面，每問一次就算一次查詢。',
  '比較的是問了幾次，不是電路有多少閘，也不是花了幾秒；這叫查詢次數，是一把很好數、也很公平的尺。',
  '量子的特別之處，是可以把所有輸入的疊加態一起丟進去，問一次就讓答案寫進每一項的正負號。'], ['bc_talk', 'dj']),
 ('Deutsch：2 次 vs 1 次', [
  '第一列是德意志問題：一位元的黑盒子，問它是常數還是平衡；古典一定要問零和一兩次，量子只問一次。',
  '換成三位元、八個輸入的版本，古典運氣差的時候，問了四個答案都一樣，還是不能下結論。',
  '所以最壞要問到一半再多一個，寫成二的位元數減一次方再加一；量子不管有幾個位元，都只問一次。'], ['bc_talk', 'dj', 'run']),
 ('BV 密碼：n 次 vs 1 次', [
  '第二列是密碼問題：黑盒子藏著一串零和一，你丟一串數字進去，它只回答對應位相乘加總的奇偶。',
  '古典的好辦法是每次只讓一位是一：先丟一零零，再丟零一零，最後丟零零一，一次只拿回密碼的一位，三位元就得問三次。',
  '量子只要問一次，整串密碼一起出現；位元越多，古典的次數跟著一起加，量子永遠停在一次。'], ['bc_talk', 'bv', 'scene_bv', 'run']),
 ('Grover：約 N/2 vs 約 √N', [
  '第三列是格羅弗搜尋：一堆抽屜裡只有一個是答案，黑盒子只會回答，你指的這一個是不是答案。',
  '古典只能一個一個打開，八個抽屜平均要開四點五次，一千零二十四個抽屜平均要開五百一十二點五次。',
  '量子大約要做四分之圓周率乘上根號抽屜數那麼多輪，一千零二十四個只要二十五輪；這是平方根的加速。'], ['bc_talk', 'grover', 'run']),
 ('Shor 與加速等級', [
  '最後補一列秀爾演算法：它解的是分解質因數，古典最好的方法也要次指數時間，量子只要多項式時間。',
  '如何操作量子電腦簡報第四十二頁把加速分成兩級：分解質因數和多半的量子模擬是指數級，搜尋只有平方級。',
  '平方級是把古典平均五十萬次，變成格羅弗大約七百八十五輪；好處要等問題非常大，才看得出來。'], ['op_talk', 'shor', 'grover']),
 ('容易錯的地方', [
  '第一個容易錯的地方：查詢次數少，不等於總時間少；量子閘比古典運算慢，還要加上錯誤更正的開銷。',
  '第二，量子跑完還要量測，格羅弗的成功率不一定是百分之百，常常要多跑幾回、讀很多次，才能確定答案。',
  '第三，三位元的德意志問題如果允許一點點出錯，古典隨便抽四個來問，誤判的機會就不到百分之三。'], ['curriculum', 'op_talk', 'grover', 'dj', 'run']),
 ('父子共同實作：比較表＋驗證三格', [
  '上半場先在紙上畫好比較表，每填一格，就要說出是從哪一頁簡報、哪一段動畫看來的。',
  '再打開三個動畫驗證三格：干涉場景看古典最壞次數，第九章看古典一位一位問，格羅弗場景看抽屜變多時的次數。',
  '每驗證一格就打一個勾，再用小程式把同樣三格跑一次，看看程式印出的次數和表上寫的一不一樣。'], ['curriculum', 'scene_int', 'scene_bv', 'scene_gr', 'run']),
 ('換你改造：量子沒有優勢的問題', [
  '下半場換你找一個量子沒有優勢的問題，例如把一萬個數字排序，或是把一整本相簿的照片讀進電腦。',
  '原因可以從簡報第四十五頁找：資料要一筆一筆載入，量出來的位元又很少，排序和加減乘除也沒有已知的量子加速。',
  '再想一個相反的例子：輸入很小、計算很難、輸出也很小，像分解一個很大的數，才是量子電腦最適合的題目。'], ['curriculum', 'op_talk']),
 ('兩小時的工程答辯', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘父子一起做比較表、用動畫驗證三格，然後休息十分鐘。',
  '下半場三十分鐘由你找出量子沒有優勢的問題並說明原因；接著十分鐘換你當老師，把比較表和原理教給爸爸。',
  '最後五分鐘錄音總結、替作品命名、存一個版本；今天的生活技能是用數字比較，說快之前先說快多少。'], ['curriculum']),
 ('最後一關：答辯查詢次數', [
  '最後一關請不看稿說出：為什麼德意志和密碼問題量子只要問一次，格羅弗卻要問大約根號那麼多輪？',
  '再指出一個注意事項：查詢次數少不等於總時間少，還要算進讀取、重複和錯誤更正的成本。',
  '今天的作品是查詢次數比較表，下一堂要用量子程式套件在自己的電腦上重現八個範例；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'op_talk']),
]

VISIBLE = [
 ['量子電腦學程 第一百二十三堂', '古典 vs 量子：\n要查幾次？', '整理 Deutsch、BV、Grover、Shor 的查詢次數', '量子第一百二十三堂  ·  依課綱製作的課前教學版'],
 ['工程答辯：查詢次數比較表', '每填一格，都要說出依據',
  '01 填表', '黑盒回答什麼\n古典、量子各幾次', '→', '02 驗證', '用動畫和程式\n打三個勾', '→', '03 答辯', '說出加速等級\n和一個限制',
  '今天的作品：查詢次數比較表'],
 ['什麼叫「查一次」', '比的是查詢次數，不是閘數或秒數',
  '01', '黑盒子', '看不到裡面，只能投進輸入、拿回答案',
  '02', '一次查詢', '問一次算一次，古典量子用同一把尺',
  '03', '量子的問法', '把所有輸入的疊加一起丟進去'],
 ['Deutsch：2 次 vs 1 次', '簡報 basic-circuits 第 30 頁第一、二列', 'Deutsch 與 n 位元版（Deutsch–Jozsa）',
  '1 位元古典', '問 f(0)、f(1)：2 次', '1 位元量子', '1 次', 'n 位元古典', '最壞 2ⁿ⁻¹ + 1 次', 'n 位元量子', '還是 1 次',
  '前一半都一樣，還分不出常數或平衡'],
 ['BV 密碼：n 次 vs 1 次', '黑盒子只回答 s·x（mod 2）的奇偶',
  '古典', '一次放一個 1：100、010、001', '→', '量子', '疊加一起問：1 次讀出 101',
  '3 位元古典 3 次；10 位元古典 10 次',
  '位元越多，量子永遠 1 次'],
 ['Grover：約 N/2 vs 約 √N', '找抽屜：黑盒只回答「是不是答案」',
  '01 古典平均', 'N = 8 → 4.5 次', '02 量子', '(π/4)√N → 2 輪', '03 加速', 'N 大 100 倍，輪數約 10 倍',
  'N = 1,024：古典平均 512.5 次 vs Grover 25 輪'],
 ['Shor 與加速等級', 'QC_Operation_Talk 第 42 頁：快在哪？',
  '分解質因數：古典次指數 → 量子多項式',
  '指數級', '分解質因數、多數量子模擬', '平方級', '搜尋、蒙地卡羅估計', 'N = 100 萬', '50 萬次 vs 約 785 輪',
  '平方加速要問題很大才明顯'],
 ['容易錯的地方', '工程答辯時評審一定會問',
  '一、查詢少 ≠ 總時間少\n二、還要算量測與重複次數\n三、允許出錯時古典也很快',
  '量子閘較慢', '錯誤更正有開銷', 'Deutsch–Jozsa 抽 4 個\n誤判 2.9%',
  '暫停影片：寫下你最容易搞錯的一點'],
 ['父子共同實作：比較表＋驗證三格', 'operation.html、transmon-3d.html',
  '畫表', '問題、黑盒回答、古典、\n量子、加速等級、驗證',
  '驗證', '干涉、第 9 章、Grover\n各打一個勾',
  '再跑 query_count.py 對一次'],
 ['換你改造：量子沒有優勢的問題', '孩子獨立改造：QC_Operation_Talk 第 45 頁',
  '01', '資料輸入', '載入 N 筆資料要約 N 步',
  '02', '一般計算', '排序、加減乘除：沒有已知加速',
  '03', '適合量子的題目', '輸入小、計算難、輸出小'],
 ['兩小時的工程答辯', '影片先引路，接下來填表、驗證、答辯',
  '00–25', '開場＋四列查詢次數', '25–65', '做比較表、動畫驗證三格', '65–75', '休息十分鐘',
  '75–105', '找量子沒有優勢的問題', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：用數字比較'],
 ['最後一關：答辯查詢次數', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '為什麼只問一次', '答案寫進正負號，再干涉',
  '02', 'Grover 為什麼要 √N 輪', '每輪只把答案推高一點',
  '03', '一個注意事項', '查詢少 ≠ 總時間少',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、把四個演算法排在同一張表、今天的一句話', '封面版型＋陳犀牛', '說出今天要做的作品'),
 ('工程答辯：填表、驗證、答辯', '三步流程卡＋黃字', '畫出比較表的欄位'),
 ('查詢的定義：黑盒子、一次查詢、量子用疊加一起問', '三點條列＋陳犀牛', '說出什麼叫查一次'),
 ('Deutsch：2 次 vs 1 次；n 位元古典最壞 2ⁿ⁻¹ + 1 次（basic-circuits 第 30 頁）', '面板四張卡＋黃字', '填表第一列'),
 ('BV：100、010、001 問 n 次 vs 1 次', '雙框對照＋白字＋黃字', '填表第二列'),
 ('Grover：N = 8 平均 4.5 次 vs 2 輪；1,024 平均 512.5 次 vs 25 輪', '三張步驟卡＋黃字', '填表第三列'),
 ('Shor 與加速等級：次指數 vs 多項式；指數級與平方級（QC_Operation_Talk 第 42 頁）', '路徑一行＋三張卡＋黃字', '在表上標加速等級'),
 ('容易錯：查詢少不等於總時間少、量測與重複、允許出錯時古典也快', '左三行＋右欄＋黃字', '寫在比較表背面'),
 ('父子共同實作：比較表＋三個動畫各驗證一格＋query_count.py', '左右比較卡＋黃字', '打三個勾'),
 ('獨立改造：量子沒有優勢的問題（QC_Operation_Talk 第 45 頁）', '三點條列＋陳犀牛', '說出一個例子和原因'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：為什麼只問一次、Grover 為什麼要 √N 輪、一個注意事項；預告 Q124', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method="Deutsch-Jozsa, Bernstein-Vazirani, Grover's and Shor's algorithm claims from Wikipedia raw wikitext fetched by the producing agent on 2026-11-19 "
                      '(verbatim quotes in production/source-notes.md); repo slides (basic-circuits.pptx pages 26 and 30, QC_Operation_Talk.pptx pages 39, 40, 42 and 45, '
                      'with notes) and animation source (js/operation/08_interference.js, 09_grover.js, transmon-3d.html chapter 9) read by the producing agent and '
                      'checked with Playwright screenshots; query counts, the 72 three-bit constant/balanced machines, the random-sampling error rates and the Grover '
                      'table from actually running query_count.py (pure Python 3.13.18, no randomness) and qiskit_check.py (Qiskit 2.6.2, Statevector and '
                      'StatevectorSampler seed=2026).',
        not_verified=['「量子閘比古典運算慢」「錯誤更正的開銷」依 QC_Operation_Talk 第 42、45 頁與 Wikipedia Grover 條目的定性說法，沒有具體時間數字',
                      '「多半的量子模擬是指數級」依 QC_Operation_Talk 第 42 頁「指數級（多數情況）」；未另查文獻',
                      '「一萬個數字排序」「一整本相簿讀進電腦」是依第 45 頁「排序」「資料輸入」舉的例子，不是簡報原句',
                      '未讀 Deutsch 1985、Deutsch–Jozsa 1992、Bernstein–Vazirani 1997、Grover 1996、Shor 1994 原始論文；課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

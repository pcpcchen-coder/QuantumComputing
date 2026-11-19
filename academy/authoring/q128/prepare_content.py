"""Q128 模組發表：量子電路展 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q128/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q128', 'q128-circuit-expo', '2026-11-18'
TITLE = '模組發表：量子電路展'
TOPIC = '模組發表：量子電路展'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q128/lesson.json',
    'module': f'{REPO} academy/lessons/Q113–Q127/brief.md（QM08 各課主題）',
    'bc': f'{REPO} animations/basic-circuits.html（量子電路入門互動動畫「八個基礎量子電路」：八個分頁、各範例的預設選項、量測 1,000 次、重點卡的延伸連結）',
    'op_circuit': f'{REPO} animations/operation.html#circuit（js/operation/06_circuit.js「量子線路：一步一步執行」：加入雜訊（每閘 1%、讀取 3%））',
    'poster': 'https://en.wikipedia.org/wiki/Poster_session',
    'curator': 'https://en.wikipedia.org/wiki/Curator',
    'plagiarism': 'https://en.wikipedia.org/wiki/Plagiarism',
    'run': f'{REPO} academy/authoring/q128/classroom.py（exhibit_helper.py、qiskit_check.py 實跑紀錄）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q128 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（向家人展示自己的線路，回答三個問題）、動手任務（每人 5 分鐘：線路、振幅逐步、量測結果）、'
                '孩子獨立改造（根據觀眾問題修改說明）、好玩機制（首映會）、作品（量子電路展海報）、生活技能（發表與回饋）、'
                '家長課前準備（發表模板）、120 分鐘流程、驗收、常見誤解（截圖與程式要註明出處）、錄音四問、下一課 Q129「電從哪裡來、到哪裡去」'},
    {'id': 'module', 'title': 'QM08 各課課綱（Q113–Q127）', 'publisher': REPO, 'url': SRC['module'],
     'usedFor': 'Q113 讀圖之前：三個約定；Q114–Q121 範例 1–8；Q125 量測 1 次與 1000 次；Q126 加入雜訊；Q127 專題：設計自己的線路'},
    {'id': 'bc', 'title': '量子電路入門互動動畫 basic-circuits.html', 'publisher': REPO, 'url': SRC['bc'],
     'usedFor': '標題「八個基礎量子電路」；八個分頁：範例 1 疊加、2 干涉、3 Bell 態、4 GHZ 態、5 隱形傳態、6 Deutsch、7 BV、8 Grover；'
                'Bell 態預設 Φ⁺：H 閘（q0）→ CNOT，兩步；H 之後 |00⟩、|01⟩ 各 +0.707，CNOT 之後 |00⟩、|11⟩ 各 +0.707；第三種 Ψ⁺ 先對 q1 做 X，量測永遠相反（01 或 10）；'
                '量測按鈕「量測 1 次」「量測 1,000 次」「清除」；每個範例重點卡下方的「延伸：」連結（動畫名＋章節）'},
    {'id': 'op_circuit', 'title': '如何操作量子電腦 3D 場景 6「量子線路：一步一步執行」', 'publisher': REPO, 'url': SRC['op_circuit'],
     'usedFor': '「加入雜訊（每閘 1%、讀取 3%）」：理想時不會出現的結果冒出少量次數（Q126 用過）'},
    {'id': 'poster', 'title': 'Poster session', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['poster'],
     'usedFor': '海報展：研究內容做成海報，「the researcher in attendance answering questions posed by passing colleagues」；海報展也被用來代替口頭報告做為評量'},
    {'id': 'curator', 'title': 'Curator', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['curator'],
     'usedFor': '展覽策展人「someone who selects and often interprets works for an exhibit」，也負責寫展品標籤（writing labels）'},
    {'id': 'plagiarism', 'title': 'Plagiarism', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['plagiarism'],
     'usedFor': '「the representation of another person\'s language, thoughts, ideas, or expressions as one\'s own original work」'},
    {'id': 'run', 'title': 'exhibit_helper.py（純 Python，沒有亂數）與 qiskit_check.py（Qiskit 2.6.2 Statevector）實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': '八個範例預設選項的理想機率 8/8 和頁面一樣；Bell 態振幅逐步 +1.000|00⟩ → +0.707|00⟩ +0.707|01⟩ → +0.707|00⟩ +0.707|11⟩；'
                'Qiskit Statevector 重算八個理想機率與純 Python 完全相同；海報檢查 8/8'},
]

SCENES = [
 ('模組發表：量子電路展', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百二十八堂，模組發表：量子電路展，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '這個模組從讀圖的三個約定開始，走過八個範例，又數過量測次數、加過雜訊，上一堂還設計了自己的線路。',
  '今天是模組發表：你當策展人，把學過的線路布置成一場展覽，向家人展示，再回答觀眾的三個問題。'], ['curriculum', 'module', 'curator']),
 ('首映會：三步完成一件展品', [
  '今天的好玩機制叫首映會：就像電影第一次上映，你的作品第一次正式面對觀眾。',
  '流程分三步：先挑一件展品，再用五分鐘發表，最後回答觀眾提出的三個問題。',
  '今天的作品是量子電路展海報，一張海報配一件展品，發表時就站在海報旁邊講。'], ['curriculum']),
 ('展品目錄：八個範例分三區', [
  '八個範例可以分成三個展區：第一區只有一顆位元，放量子硬幣和干涉。',
  '第二區是糾纏：貝爾態、三顆位元一起糾纏的範例四，還有把狀態送過去的隱形傳態。',
  '第三區是演算法：德意志、猜密碼和格羅弗，都靠干涉，用比古典更少的查詢找到答案。'], ['bc', 'module']),
 ('五分鐘發表：線路、振幅、量測', [
  '每人五分鐘，照課綱分三段：先介紹線路，再一步一步看振幅，最後公布量測結果。',
  '介紹線路時說清楚幾顆位元、幾個步驟、量哪幾顆；播放振幅時，每按一步就說一句柱子怎麼變。',
  '公布結果時，把理想機率和量一千次的比例放在一起，再說出展品來自哪個動畫、哪個範例。'], ['curriculum', 'bc']),
 ('示範：範例三貝爾態', [
  '我們用範例三貝爾態示範：兩條線、兩個步驟，先對編號零做哈達瑪閘，再做受控反閘。',
  '振幅逐步：起點只有零零一根；哈達瑪閘之後，零零和零一各零點七零七；受控反閘之後，換成零零和一一。',
  '量測結果：理想機率是零零、一一各一半，量一千次也只出現這兩種，兩顆位元永遠一樣。'], ['bc', 'run']),
 ('觀眾的三個問題', [
  '發表完，請家人至少問三個問題；常見的有三種：為什麼會這樣、改一個閘會怎樣、真的量子電腦也一樣嗎？',
  '回答「改一個閘」最好當場改給觀眾看：例如把貝爾態換成第三種，結果就變成零一和一零，兩顆永遠相反。',
  '回答「真的電腦」可以引用雜訊那一課：每個閘、每次讀取都可能出錯，所以會冒出少量別的結果。'], ['curriculum', 'bc', 'op_circuit']),
 ('海報怎麼排', [
  '海報就是五分鐘發表的地圖：研討會的海報展，作者也是站在海報旁邊，回答走過的人提出的問題。',
  '版面由上到下排：先是作品名和一句話，接著是線路圖和三格振幅，最後是量測結果的直方圖。',
  '每一格都要讓沒學過量子的家人看得懂：少寫算式，多畫圖，再配一句白話說明。'], ['poster', 'curriculum']),
 ('截圖與程式要註明出處', [
  '今天的注意事項：截圖與程式要註明出處，寫清楚是哪個動畫檔、哪個範例，程式是哪個檔案、哪個版本。',
  '把別人的文字、想法或作品當成自己的原創，叫做抄襲；註明出處，觀眾也才找得到原始畫面。',
  '還要說清楚結果的來歷：模擬器算出的是理想機率，不是真實機器的實測。'], ['curriculum', 'plagiarism']),
 ('父子共同實作：每人五分鐘', [
  '上半場四十分鐘，每人輪流發表五分鐘：打開線路入門動畫，選好範例，邊按下一步邊講。',
  '教材的展品小幫手會印出八張展品卡：位元數、步驟數、理想機率，八個範例都和頁面一樣。',
  '把它改成你的展品，就會印出每一步的振幅；另一支程式用本機的量子程式套件重算，八個理想機率也完全對得上。'], ['curriculum', 'bc', 'run']),
 ('換你改造：根據觀眾問題', [
  '下半場三十分鐘換你獨立改造：把觀眾問倒你的問題記下來，修改海報上的說明。',
  '改說明有三步：先找出觀眾卡住的那一句，再換成更白話的說法或多畫一張圖，最後重講一次給同一位觀眾聽。',
  '展品小幫手也會檢查海報：欄位齊不齊、出處有沒有寫、三個問題是不是都有回答。'], ['curriculum', 'run']),
 ('兩小時的量子電路展', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘輪流發表、互相提問，然後休息十分鐘。',
  '下半場三十分鐘，你根據觀眾的問題修改說明；接著十分鐘角色互換，由你教爸爸操作和原理。',
  '最後五分鐘錄音總結、替作品命名、存一個版本；今天的生活技能是發表與回饋：講給別人聽，再從問題裡改進。'], ['curriculum']),
 ('最後一關：首映會', [
  '最後一關請不看稿說出：你的展品在解決什麼？核心原理用一句話怎麼講？',
  '再指出一個注意事項，例如截圖與程式要註明出處，模擬結果不能當成真實機器的實測。',
  '今天的作品是量子電路展海報，下一堂是電從哪裡來、到哪裡去；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum']),
]

VISIBLE = [
 ['量子電腦學程 第一百二十八堂', '模組發表\n量子電路展', '八個範例走完，今天開一場展覽', '量子第一百二十八堂  ·  依課綱製作的課前教學版'],
 ['首映會：三步完成一件展品', '你當策展人，作品第一次面對觀眾',
  '01 挑展品', '八個範例\n任選一個', '→', '02 發表', '五分鐘：線路、\n振幅、量測', '→', '03 回答', '觀眾的\n三個問題',
  '今天的作品：量子電路展海報'],
 ['展品目錄：八個範例分三區', 'basic-circuits.html 的八個分頁',
  '01', '一顆位元區（範例 1–2）', '疊加（量子硬幣）、干涉 H‑Z‑H',
  '02', '糾纏區（範例 3–5）', 'Bell 態、GHZ 態、隱形傳態',
  '03', '演算法區（範例 6–8）', 'Deutsch、BV、Grover：查詢更少'],
 ['五分鐘發表：三段', '照課綱：線路、振幅逐步、量測結果', '線路 → 振幅逐步 → 量測 → 出處',
  '線路', '幾顆位元、幾步', '振幅', '每按一步說一句', '量測', '理想 vs 一千次', '出處', '動畫＋範例編號',
  '每人 5 分鐘，先排練一次'],
 ['示範：範例 3 Bell 態', '兩條線、兩個步驟',
  '線路', 'H(q0) → CNOT', '→', '振幅逐步', '|00⟩ → |00⟩,|01⟩ → |00⟩,|11⟩',
  '量測：00、11 各 50%',
  '兩顆位元永遠一樣 → 這就是糾纏'],
 ['觀眾的三個問題', '發表完，請家人至少問三題',
  '第一問', '為什麼會這樣？', '第二問', '改一個閘會怎樣？', '第三問', '真機器也一樣嗎？',
  '答不出來：先記下來，等一下改說明'],
 ['海報怎麼排', '研討會海報展：作者站在海報旁回答問題',
  '作品名  →  線路圖  →  振幅  →  直方圖',
  '上', '作品名＋一句話', '中', '線路圖＋三格振幅', '下', '直方圖＋出處',
  '少寫算式、多畫圖、一句白話'],
 ['截圖與程式要註明出處', '課綱的注意事項：截圖與程式要註明出處',
  '① 動畫檔名＋#範例\n② 程式檔名＋版本\n③ 理想模擬還是實測',
  '範例寫法', 'basic-circuits.html#bell 範例 3', '截圖：量子電路入門互動動畫\n程式：qiskit_check.py（Qiskit 2.6.2）',
  '沒寫出處＝把別人的作品當成自己的'],
 ['父子共同實作：每人五分鐘', 'basic-circuits.html ＋ exhibit_helper.py',
  '動畫', '選範例、按下一步\n邊按邊講',
  '程式', '八張展品卡 8/8 ✓\nQiskit 重算 8/8 ✓',
  '每人 5 分鐘：線路、振幅、量測'],
 ['換你改造：根據觀眾問題', '孩子獨立改造：修改海報上的說明',
  '01', '記下問題', '哪一題把你問倒了',
  '02', '改說明', '換白話、多畫一張圖',
  '03', '再講一次', '講給同一位觀眾聽'],
 ['兩小時的量子電路展', '影片先引路，接下來發表、提問、改進',
  '00–25', '開場＋示範發表', '25–65', '每人五分鐘發表', '65–75', '休息十分鐘',
  '75–105', '依觀眾問題改說明', '105–115', '換你教爸爸', '115–120', '錄音總結＋存版本',
  '今日生活技能：發表與回饋'],
 ['最後一關：首映會', '暫停影片：不看稿講一次，再指出一個注意事項',
  '01', '解決什麼', '我的展品一句話講完',
  '02', '核心原理', '哪一步最關鍵',
  '03', '注意事項', '截圖與程式要註明出處',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、QM08 走完、今天當策展人開展覽', '封面版型＋陳犀牛', '說出今天要交的作品'),
 ('首映會三步：挑展品、五分鐘發表、回答三個問題；作品量子電路展海報', '三步流程卡＋黃字', '挑出自己的展品'),
 ('展品目錄：一顆位元區（1–2）、糾纏區（3–5）、演算法區（6–8）', '三點條列＋陳犀牛', '在 basic-circuits.html 找到自己的範例'),
 ('五分鐘發表：線路、振幅逐步、量測結果、出處', '面板四張卡＋黃字', '照四格寫發表大綱'),
 ('示範範例 3 Bell 態：H、CNOT；振幅三格；00、11 各 50%', '雙框對照＋白字＋黃字', '照示範講一次自己的展品'),
 ('觀眾三問：為什麼、改一個閘、真機器（雜訊）', '三張步驟卡＋黃字', '請家人提三個問題'),
 ('海報版面：作品名＋一句話、線路圖＋三格振幅、直方圖＋出處（Poster session）', '路徑一行＋三張卡＋黃字', '畫海報草稿'),
 ('注意事項：截圖與程式註明出處（Plagiarism）；理想模擬不是實測', '左三行＋右欄＋黃字', '在海報右下角寫出處'),
 ('父子共同實作：basic-circuits.html 每人五分鐘；exhibit_helper.py、qiskit_check.py', '左右比較卡＋黃字', '輪流發表並請對方提問'),
 ('獨立改造：記下問題、改說明、再講一次；海報檢查', '三點條列＋陳犀牛', '修改海報說明'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：解決什麼、核心原理、注意事項；預告 Q129', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Poster session, Curator and Plagiarism claims from Wikipedia raw wikitext fetched by the producing agent on 2026-11-19 '
                      '(verbatim quotes in production/source-notes.md); QM08 lesson briefs (Q113–Q127) and animation source '
                      '(basic-circuits.html SCENES, tabs, measurement buttons and extension links; operation.html scene 6 noise toggle) '
                      'read by the producing agent and checked with Playwright screenshots; the eight default ideal distributions were '
                      'computed by running the page engine in Node, by exhibit_helper.py (Python 3.13.18, standard library, no randomness) '
                      'and by qiskit_check.py (Qiskit 2.6.2 Statevector); all three agree.',
        not_verified=['八個範例只驗證理想模擬（預設選項）；量一千次的比例每次不同，旁白不念次數',
                      '「常見的三種問題」是本課整理的發表練習建議，課綱只寫「回答三個問題」，沒有規定題目',
                      '海報版面（由上到下：作品名、線路與振幅、直方圖與出處）是本課的建議做法，不是研討會的統一規格',
                      'Qiskit 只用 2.6.2 實跑；課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

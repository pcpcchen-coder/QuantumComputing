"""Q127 專題：設計自己的線路 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q127/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q127', 'q127-design-circuit', '2026-11-18'
TITLE = '專題：設計自己的線路'
TOPIC = '專題：設計自己的線路'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q127/lesson.json',
    'op_talk': f'{REPO} slides/QC_Operation_Talk.pptx（第 18 頁「單位元量子閘一覽」；第 22 頁「兩位元閘：產生糾纏的唯一方法」；第 28 頁「動態線路」；第 52 頁「操作一台量子電腦：檢查表」）',
    'op_register': f'{REPO} animations/operation.html#register（js/operation/04_register.js「多量子位元：2ⁿ 個振幅與糾纏」：按鈕 H、X、Z、S、T、CNOT、CZ、均勻疊加、測量全部）',
    'op_circuit': f'{REPO} animations/operation.html#circuit（js/operation/06_circuit.js「量子線路：一步一步執行」的「量子隱形傳態」範例）',
    'qgate': 'https://en.wikipedia.org/wiki/Quantum_logic_gate',
    'harking': 'https://en.wikipedia.org/wiki/HARKing',
    'backward': 'https://en.wikipedia.org/wiki/Backward_design',
    'run': f'{REPO} academy/authoring/q127/classroom.py（tiny_sim.py、my_circuit.py 實跑紀錄）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q127 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（用學過的閘設計一條能說明一個概念的線路，並在模擬器驗證）、動手任務（寫出目標、畫線路、預測結果、用模擬器驗證）、'
                '孩子獨立改造（加一個「故意出錯」的版本，說明差別）、好玩機制（Maker 挑戰）、作品（自己的線路與驗證報告）、生活技能（從目標反推設計）、'
                '家長課前準備（本機模擬器）、120 分鐘流程、驗收與常見誤解（先寫預測再跑，避免看結果才找理由）、需新增素材（專題模板）、下一課 Q128「模組發表：量子電路展」'},
    {'id': 'op_talk', 'title': '如何操作量子電腦（簡報）第 18、22、28、52 頁', 'publisher': REPO, 'url': SRC['op_talk'],
     'usedFor': '第 18 頁：Z「|1⟩ 變號（相位翻轉）」、H「|0⟩ → |+⟩：產生疊加」、S「繞 z 軸 90°｜相位 i；S² = Z」、T「繞 z 軸 45°」。'
                '第 22 頁：CZ「兩個都是 1 時加負號（對稱）」「CZ 對稱：不分控制與目標」、等價關係「CNOT = (I⊗H) · CZ · (I⊗H)」。'
                '第 28 頁：「3D 場景 6 的「量子隱形傳態」範例以延遲量測原理把條件操作改成受控閘，結果相同：q2 最後得到 q0 原本的狀態（P(1) = 0.75）」。'
                '第 52 頁檢查表：「2 設計線路」「3 先用模擬器｜驗證邏輯正確」「8 後處理與驗證｜與模擬比較；答案可驗證就驗證」'},
    {'id': 'op_register', 'title': '如何操作量子電腦 3D 場景 4「多量子位元：2ⁿ 個振幅與糾纏」', 'publisher': REPO, 'url': SRC['op_register'],
     'usedFor': '按鈕「目標 q0–q3」「H」「X」「Z」「S」「T」「CNOT（控制 = 目標+1 → 目標）」「CZ」「均勻疊加 H⊗ⁿ」「測量全部」「重設 |0…0⟩」；'
                '柱子高度 = 機率、顏色 = 相位（金 = +，藍 = −）；讀數「各量子位元 Bloch 長度」與「有糾纏／無糾纏」'},
    {'id': 'op_circuit', 'title': '如何操作量子電腦 3D 場景 6「量子線路：一步一步執行」量子隱形傳態', 'publisher': REPO, 'url': SRC['op_circuit'],
     'usedFor': 'tele：Ry、H、CX、CX、H、CX、CZ 七個閘，量測欄只量 q2（meas: [2]）；步驟 6「Bob 依 q1 的結果做 X（延遲量測：改成受控閘）」、'
                '步驟 8「量測 q2：P(1) = 0.75，和一開始的 q0 相同」'},
    {'id': 'qgate', 'title': 'Quantum logic gate', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['qgate'],
     'usedFor': 'Phase shift gates：「The probability of measuring a |0⟩ or |1⟩ is unchanged after applying this gate, however it modifies the phase of the quantum state」；'
                'T gate φ = π/4、S gate φ = π/2、Pauli-Z φ = π；S = √Z、T = √S = ⁴√Z；Pauli Z「sometimes called phase-flip」'},
    {'id': 'harking', 'title': 'HARKing', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['harking'],
     'usedFor': '「hypothesizing after the results are known」：「presenting a post hoc hypothesis in the introduction of a research report as if it were an a priori hypothesis」，'
                '被稱為 questionable research practice'},
    {'id': 'backward', 'title': 'Backward design', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['backward'],
     'usedFor': '「setting goals before choosing instructional methods and forms of assessment」；三階段：Identify the results desired → Determine acceptable levels of evidence → Design activities'},
    {'id': 'run', 'title': 'tiny_sim.py（純 Python，沒有亂數）與 my_circuit.py（Qiskit 2.6.2 + qiskit-aer 0.18.4，seed_simulator=127）實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': '範例甲 H、四個 T、H：理想 1 = 100%，一千次全是 1；範例乙 H H、CZ、H：理想 00、11 各 50%，一千次只有 00、11；'
                '故意出錯甲（三個 T）：理想 0 = 14.6%、1 = 85.4%；故意出錯乙（沒有最後的 H）：四種各 25%；判定「預測正確／預測不對」'},
]

SCENES = [
 ('專題：設計自己的線路', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百二十七堂，專題：設計自己的線路，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '這個模組我們一路跑過八個範例，也數過量測次數、加過雜訊；今天換你當設計師，不再照抄現成的線路。',
  '任務是用學過的閘，設計一條能說明一個概念的線路，再用模擬器證明，它真的照你想的方式運作。'], ['curriculum']),
 ('創客挑戰：專題四步驟', [
  '今天的好玩機制是創客挑戰：像做一件作品一樣，從一個想法開始，做出能動、能測、能拿給別人看的東西。',
  '專題分四步：先寫目標，再畫線路，接著寫下預測，最後用模擬器驗證，看預測和結果對不對得上。',
  '作品是自己的線路與驗證報告：一張線路圖、一張預測表、一份模擬結果，再加上一個故意出錯的版本。'], ['curriculum', 'op_talk']),
 ('工具箱：學過的閘', [
  '先打開工具箱：哈達瑪閘做出疊加，翻轉閘把零和一對調，相位翻轉閘只讓狀態一的振幅變號。',
  '還有兩個轉得比較少的相位閘：四分之一圈相位閘做兩次，等於相位翻轉閘；八分之一圈相位閘做兩次，等於四分之一圈。',
  '兩顆位元的有受控反閘和受控相位翻轉閘；受控相位翻轉閘只在兩顆都是一的時候加負號，所以不分誰控制誰。'], ['op_talk', 'qgate']),
 ('從目標反推設計', [
  '設計線路最好倒過來想：先決定要說明什麼，再決定什麼樣的結果能當證據，最後才挑閘。',
  '例如目標是「相位看不見，但干涉看得見」，證據就是：只加相位閘，機率不變；前後夾上哈達瑪閘，結果就跟著改變。',
  '證據決定線路的樣子：要看相位，最後就得安排干涉；要看糾纏，就得量兩顆，比對它們是不是永遠一樣。'], ['backward', 'qgate']),
 ('範例甲：四個八分之一圈', [
  '範例甲的目標是：四個八分之一圈相位閘，效果等於一個相位翻轉閘；線路是哈達瑪閘、四個八分之一圈，再一個哈達瑪閘。',
  '先寫預測：如果目標是對的，這條線路就等於哈達瑪、相位翻轉、哈達瑪，量一千次應該全部是一。',
  '模擬器算出的理想機率是一，百分之百；抽樣一千次也全部是一，預測對了，目標得到證據。'], ['qgate', 'op_talk', 'run']),
 ('範例乙：另一種貝爾態配方', [
  '範例乙的目標是：不用受控反閘，也能做出貝爾態；線路是兩顆都做哈達瑪閘，接著受控相位翻轉閘，再對編號零做一次哈達瑪閘。',
  '簡報第二十二頁寫著：受控反閘，等於在目標位元前後各夾一個哈達瑪閘的受控相位翻轉閘；範例乙就是照這個關係改寫的。',
  '預測是零零和一一各一半；模擬器的理想機率正是各百分之五十，抽樣一千次也只出現這兩種。'], ['op_talk', 'run']),
 ('先寫預測，再按執行', [
  '今天最重要的習慣：預測一定要在執行之前寫下來，寫好就不改，連日期一起記在驗證報告上。',
  '科學界把「看到結果才編出假設，再假裝一開始就這麼想」叫做事後假設，這會讓實驗失去檢驗的力量。',
  '預測錯了不丟臉，反而是最有收穫的時候：寫下錯在哪裡，再想一個新的預測，去跑下一次。'], ['curriculum', 'harking']),
 ('故意出錯的版本', [
  '改造任務是做一個故意出錯的版本，例如範例甲只放三個八分之一圈，少轉了八分之一圈。',
  '結果不再全是一：理想機率大約是一佔八成五、零佔一成五；少一個閘，干涉就沒有完全抵消。',
  '範例乙如果忘了最後的哈達瑪閘，四種結果各佔四分之一：糾纏還在，只是量不出來；這就是差別說明要寫的東西。'], ['run', 'curriculum']),
 ('父子共同實作：從目標到驗證', [
  '上半場四十分鐘，先在三維動畫的多位元場景，用按鈕把範例甲和範例乙各組一次，看柱子的顏色和高度怎麼變。',
  '接著打開教材的專題模板程式，填好目標和預測再執行，它會畫出線路、算出理想機率、抽樣一千次，最後判定預測對不對。',
  '然後爸爸和孩子一起想一個自己的目標，照四步驟走一遍，把線路圖和預測表貼進驗證報告。'], ['curriculum', 'op_register', 'run']),
 ('換你改造：故意出錯', [
  '下半場換你獨立改造：替自己的線路做一個故意出錯的版本，拿掉一個閘、換一個閘，或改錯目標位元。',
  '出錯之前也要先預測：你覺得會錯成什麼樣子？寫下來再跑，比對兩個版本的結果差在哪裡。',
  '最後替兩個版本寫一句差別說明：哪一步不一樣、結果怎麼變、為什麼會這樣變。'], ['curriculum', 'run']),
 ('兩小時的創客挑戰', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘看兩個範例，接著四十分鐘寫目標、畫線路、預測和驗證，然後休息十分鐘。',
  '下半場三十分鐘做故意出錯的版本，寫差別說明；接著十分鐘角色互換，由你教爸爸操作和原理。',
  '最後五分鐘錄音總結、替作品命名、存一個版本；今天的生活技能是從目標反推設計：先想清楚要什麼，再決定怎麼做。'], ['curriculum', 'backward']),
 ('最後一關：驗證報告', [
  '最後一關請不看稿說出：你的線路要說明什麼概念？哪一個結果是你的證據？',
  '再指出一個注意事項：預測要先寫再跑，看到結果才找理由，驗證就不算數。',
  '今天的作品是自己的線路與驗證報告，下一堂是模組發表：量子電路展；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum']),
]

VISIBLE = [
 ['量子電腦學程 第一百二十七堂', '專題\n設計自己的線路', '用學過的閘，說明一個概念', '量子第一百二十七堂  ·  依課綱製作的課前教學版'],
 ['創客挑戰：專題四步驟', '從一個想法，到一份驗證報告',
  '01 目標', '我要說明\n什麼概念', '→', '02 線路', '挑閘、\n畫線路圖', '→', '03 驗證', '先寫預測\n再跑模擬器',
  '今天的作品：自己的線路與驗證報告'],
 ['工具箱：學過的閘', '簡報 p18、p22',
  '01', '單位元閘', 'H 疊加、X 對調、Z 變號',
  '02', '轉一點點的相位閘', 'S × 2 = Z；T × 2 = S',
  '03', '雙位元閘', 'CNOT；CZ 不分誰控制誰'],
 ['從目標反推設計', '先決定證據，再挑閘', '目標 → 證據 → 線路',
  '要看相位', '最後安排干涉', '要看糾纏', '兩顆一起量', '要看機率', '量很多次', '要看錯誤', '做故意出錯版',
  '證據決定線路的樣子'],
 ['範例甲：四個 T', '目標：四個八分之一圈 = 一個 Z',
  '線路', 'H → T T T T → H', '→', '等於', 'H → Z → H',
  '預測：1 佔 100%',
  '理想 100%、一千次全是 1 → 預測正確'],
 ['範例乙：用 CZ 做貝爾態', '不用 CNOT 也能糾纏',
  '第一步', 'q0、q1 都做 H', '第二步', 'CZ（不分控制）', '第三步', 'q0 再做 H',
  '預測：00、11 各 50% → 預測正確'],
 ['先寫預測，再按執行', '事後假設會讓驗證失去力量',
  '寫預測  →  按執行  →  比對  →  不改預測',
  '預測', '先寫、寫日期', '結果', '照實記錄', '錯了', '寫下錯在哪',
  '常見誤解：看結果才找理由'],
 ['故意出錯的版本', '少一個閘，差在哪裡',
  '甲：只放三個 T\n乙：忘了最後的 H\n你：拿掉、換掉或放錯位元',
  '1 佔 85%、0 佔 15%', '四種各 25%', '糾纏還在\n只是量不出來',
  '暫停影片：猜猜你的出錯版會怎樣'],
 ['父子共同實作：四步驟', 'operation.html#register ＋ my_circuit.py',
  '動畫', '範例甲、範例乙\n用按鈕各組一次',
  '程式', '專題模板：目標、預測\n理想機率、一千次、判定',
  '驗證報告：線路圖＋預測表＋結果'],
 ['換你改造：故意出錯', '孩子獨立改造：當出錯設計師',
  '01', '先預測', '出錯版會錯成什麼樣子',
  '02', '再執行', '拿掉、換掉或改目標位元',
  '03', '寫差別', '哪一步不同、結果怎麼變'],
 ['兩小時的創客挑戰', '影片先引路，接下來寫、畫、猜、驗',
  '00–25', '開場＋兩個範例', '25–65', '目標、線路、預測、驗證', '65–75', '休息十分鐘',
  '75–105', '故意出錯版', '105–115', '換你教爸爸', '115–120', '錄音總結＋存版本',
  '今日生活技能：從目標反推設計'],
 ['最後一關：驗證報告', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '我的概念', '線路要說明什麼',
  '02', '我的證據', '哪一個結果能證明',
  '03', '一個注意事項', '預測先寫再跑，不看結果找理由',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、八個範例之後換自己設計、今天的任務', '封面版型＋陳犀牛', '說出今天要做的作品'),
 ('創客挑戰：目標、線路、預測、驗證；自己的線路與驗證報告', '三步流程卡＋黃字', '寫下自己的第一個點子'),
 ('工具箱：H、X、Z；S² = Z、T² = S（QC_Operation_Talk 第 18 頁）；CNOT、CZ 對稱（第 22 頁）', '三點條列＋陳犀牛', '把工具箱抄在模板第 2 頁'),
 ('從目標反推設計：目標 → 證據 → 線路；四種證據對應的線路安排', '面板四張卡＋黃字', '替自己的目標想一個證據'),
 ('範例甲：H、T×4、H；等於 H-Z-H；預測 1 佔 100%，驗證正確', '雙框對照＋白字＋黃字', '照模板寫出範例甲的預測'),
 ('範例乙：H H、CZ、H；CNOT = (I⊗H)·CZ·(I⊗H)（第 22 頁）；00、11 各 50%', '三張步驟卡＋黃字', '比較範例乙和 Q116 的貝爾態線路'),
 ('先寫預測再跑：事後假設（HARKing）；預測錯了要寫下原因', '路徑一行＋三張卡＋黃字', '在模板上寫日期與預測'),
 ('故意出錯：三個 T → 1 佔 85.4%；沒有最後的 H → 四種各 25%', '左三行＋右欄＋黃字', '猜自己的出錯版'),
 ('父子共同實作：operation.html#register 組範例甲乙；my_circuit.py 專題模板', '左右比較卡＋黃字', '完成第一份驗證報告'),
 ('獨立改造：故意出錯版、先預測、寫差別說明', '三點條列＋陳犀牛', '完成出錯版與差別說明'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：我的概念、我的證據、預測先寫再跑；預告 Q128', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Quantum logic gate, HARKing and Backward design claims from Wikipedia raw wikitext fetched by the producing agent on 2026-11-19 '
                      '(verbatim quotes in production/source-notes.md); repo slides (QC_Operation_Talk.pptx pages 18, 22, 28, 52 read with zipfile) '
                      'and animation source (operation.html scene 4 register: 04_register.js buttons H/X/Z/S/T/CNOT/CZ/uniform superposition/measure; '
                      'scene 6 circuit: 06_circuit.js teleport preset) read by the producing agent and checked with Playwright screenshots; '
                      'tiny_sim.py run with Python 3.13 (no randomness, exact state vectors); my_circuit.py run with Qiskit 2.6.2 and '
                      'qiskit-aer 0.18.4 (seed_simulator=127).',
        not_verified=['範例甲、範例乙是教學示範用的小線路，只驗證理想模擬器上的結果；沒有在真實硬體上執行',
                      '抽樣一千次的比例隨亂數種子而變（範例乙 00、11 各約一半，故意出錯版的比例會在理想值附近起伏）；旁白不念抽樣次數',
                      '「判定」只比對預測和理想機率（容許差 1 個百分點），不做統計檢定',
                      'Qiskit 只用 2.6.2、qiskit-aer 只用 0.18.4 實跑；課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

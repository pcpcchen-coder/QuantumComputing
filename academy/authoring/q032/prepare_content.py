"""Q032 模組發表：設計我的 transmon — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q032/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q032', 'q032-design-my-transmon', '2026-11-18'
TITLE = '模組發表：設計我的 transmon'
TOPIC = '模組發表：設計我的 transmon'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q032/lesson.json',
    'neighbors': f'{REPO} academy/lessons/Q031/brief.md、academy/lessons/Q033/brief.md',
    'jj_talk_p19': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p19（Transmon 深入：EJ/EC 與電荷色散，含講者備註）',
    'jj_talk_p20': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p20（Transmon 典型參數，含講者備註）',
    'jj_talk_p21': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p21（JJ 製程，講者備註：氧化層厚度決定穿隧電阻和臨界電流）',
    'jj_talk_p28': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p28（色散區域，含講者備註）',
    'jj_talk_p37': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p37（數值範例：設計一組讀取參數，含講者備註）',
    'transmon_p12': f'{REPO} slides/transmon.pptx p12（典型參數（本系列範例））',
    'potential_scene': f'{REPO} animations/index.html#potential（animations/js/scenes/04_potential.js）',
    'tr_scene': f'{REPO} animations/transmon-3d.html（#capacitor 第 1 章電容分頁、第 3 章位能井、第 6 章頻率配置）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q032 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（選定頻率、非諧性、E_J／E_C，說明每個數字背後的取捨）、動手任務（用參數設計器做一張 transmon 參數卡，並在場景驗證能階）、'
                '孩子獨立改造（替參數卡加一個讀取腔頻率，並說明失諧為什麼要這麼大）、好玩機制（工程答辯）、作品（transmon 參數卡）、'
                '家長課前準備（參數設計器；index.html#potential）、120 分鐘流程、驗收與常見誤解（參數卡是設計目標；製程誤差會讓實際頻率偏移）、'
                '生活技能支線（用數字支持設計決定）'},
    {'id': 'neighbors', 'title': '量子電腦學程 Q031、Q033 課綱', 'publisher': REPO, 'url': SRC['neighbors'],
     'usedFor': '上一堂：退相干：敵人在哪裡（偵探辦案，找出破壞量子位元的嫌犯）；'
                '下一堂：讀取要快、準、不破壞（QM03 讀取量子位元與周邊系統的第一堂）'},
    {'id': 'jj_talk_p19', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p19：Transmon 深入：EJ/EC 與電荷色散', 'publisher': REPO, 'url': SRC['jj_talk_p19'],
     'usedFor': 'ħω01 ≈ √(8EJEC) − EC；非諧性 α ≈ −EC（只以冪次下降）；電荷色散 ∝ e^(−√(8EJ/EC))（指數下降）；'
                '備註：背景電荷是無法完全消除的雜訊；「犧牲一點點非諧性，換來對電荷雜訊幾乎免疫」；3D 場景 4 把 EJ/EC 從 1 拉到 50'},
    {'id': 'jj_talk_p20', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p20：Transmon 典型參數', 'publisher': REPO, 'url': SRC['jj_talk_p20'],
     'usedFor': 'f01 4–6 GHz；非諧性 α ≈ −EC，−200～−300 MHz；EJ/EC 50–100；JJ 臨界電流 20–50 nA；總電容 60–100 fF；T1（最佳實驗）0.1–1 ms'},
    {'id': 'jj_talk_p21', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p21：JJ 製程（講者備註）', 'publisher': REPO, 'url': SRC['jj_talk_p21'],
     'usedFor': '「氧氣壓力乘上時間，決定了氧化層厚度，也就決定了穿隧電阻和臨界電流」→ 製程差一點，臨界電流與 E_J 就跟著變'},
    {'id': 'jj_talk_p28', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p28：色散區域', 'publisher': REPO, 'url': SRC['jj_talk_p28'],
     'usedFor': '|Δ| = |ωq − ωr| ≫ g 的色散區域；「失諧很大 → 不交換能量，只互相『推』頻率」；諧振腔頻率成為量子位元狀態的指示器；量子位元 5 GHz、諧振腔 7 GHz、Δ ≈ −2 GHz'},
    {'id': 'jj_talk_p37', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p37：數值範例：設計一組讀取參數', 'publisher': REPO, 'url': SRC['jj_talk_p37'],
     'usedFor': '讀取腔 7.0 GHz、量子位元 5.0 GHz、Δ/2π = −2.0 GHz、耦合 g/2π = 100 MHz、α/2π = −250 MHz；Purcell T1 上限 ≈ 57 μs（1/[κ(g/Δ)²]）→ 需 Purcell 濾波器'},
    {'id': 'transmon_p12', 'title': 'Transmon 筆記簡報 p12：典型參數（本系列範例）', 'publisher': REPO, 'url': SRC['transmon_p12'],
     'usedFor': 'EJ/h 15 GHz、EC/h 250 MHz（CΣ ≈ 77.5 fF）、EJ/EC 60、f01 5.21 GHz（電荷基底數值對角化）、α/2π −283 MHz（近似 −EC = −250 MHz）；讀取共振腔 ~7 GHz；工作溫度 10–20 mK，5 GHz 對應 hf/kB ≈ 0.24 K'},
    {'id': 'potential_scene', 'title': 'JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon', 'publisher': REPO, 'url': SRC['potential_scene'],
     'usedFor': '實作「在場景驗證能階」與動畫段：E_C/h 固定 250 MHz（第 12 行）、初始比值 50（第 13 行）；按鈕「LC 諧振子（線性）」「JJ / Transmon（非線性）」、'
                '滑桿「E_J / E_C（對數刻度）」、按鈕「CPB：E_J/E_C = 1」「10」「Transmon：50」（第 114–116 行）；金色躍遷頻率標籤（第 97–105 行）；'
                '讀數 ω₀₁、ω₁₂、非諧性、近似公式（第 108–112 行）'},
    {'id': 'tr_scene', 'title': 'Transmon 3D（transmon-3d.html）', 'publisher': REPO, 'url': SRC['tr_scene'],
     'usedFor': '第 1 章「大十字電容的作用」分頁當參數設計器：E_J/h 固定 15 GHz、C_Σ 滑桿 5–200 fF、讀數 E_C、E_J/E_C、f₀₁、α、電荷色散、判斷（第 360–371、879–890、1197–1208 行）；'
                '第 3 章：非諧性越大，閘可以做得越快、脈衝不能無限縮短（第 912 行）；第 6 章：鄰近位元錯開約 200 MHz、20 ns π 脈衝頻寬約 50 MHz（第 1317–1321 行）'},
]

SCENES = [
 ('模組發表：設計我的 transmon', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第三十二堂，模組發表：設計我的超導量子位元，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂我們當偵探，找出破壞量子位元的嫌犯；這個模組從超導一路走到大電容型的超導量子位元，今天要把學過的東西，變成一張自己的設計卡。',
  '好玩的地方是工程答辯：卡上的每一個數字，你都要能說出為什麼這樣選，又放棄了什麼。'], ['curriculum', 'neighbors']),
 ('三個重點', [
  '今天有三個重點：第一，頻率，也就是零到一的頻率，要選在多高；第二，非諧性，要多大才夠讓微波只挑零和一。',
  '第三，約瑟夫森能量和充電能量的比值；三個數字互相牽動，改一個，另外兩個也會跟著變。',
  '今天的作品是一張超導量子位元參數卡，上面寫著三個數字，每個數字旁邊附上一句取捨。'], ['curriculum', 'jj_talk_p19']),
 ('參數卡上有什麼', [
  '先看參數卡上要填什麼：學程簡報整理了一頁典型數字，可以當作設計的參考範圍。',
  '頻率大約四到六吉赫，非諧性大約負兩百到負三百兆赫，兩個能量的比值大約五十到一百。',
  '同一頁還列了臨界電流二十到五十奈安培、總電容六十到一百飛法拉；今天先把三個主要數字定下來。'], ['jj_talk_p20']),
 ('數字一：頻率', [
  '第一個數字是頻率：把八倍的約瑟夫森能量乘上充電能量，開根號，再減掉一個充電能量，就是零到一頻率的近似值。',
  '頻率要夠高：五吉赫換算成溫度，大約是零點二四克耳文，比冷凍機的十到二十毫克耳文高得多，熱擾動就很難把它激發。',
  '它還要和讀取腔錯開大約兩吉赫，和隔壁的量子位元也要錯開，例如兩百兆赫；典型的頻率，落在四到六吉赫之間。'], ['jj_talk_p19', 'transmon_p12', 'jj_talk_p37', 'tr_scene', 'jj_talk_p20']),
 ('數字二：非諧性', [
  '第二個數字是非諧性：一到二的頻率減掉零到一的頻率；對大電容型的超導量子位元來說，大約等於負的充電能量。',
  '如果能階等間距，微波一打，零到一、一到二會一起共振；有了兩三百兆赫的差距，微波才能只挑零和一。',
  '非諧性太小，脈衝就得放慢，否則會漏到更高的能階；典型的數字，是負兩百到負三百兆赫。'], ['jj_talk_p19', 'jj_talk_p20', 'potential_scene', 'tr_scene']),
 ('數字三：兩個能量的比值', [
  '第三個數字是約瑟夫森能量和充電能量的比值；比值加大時，電荷色散呈指數下降，量子位元幾乎不怕背景電荷。',
  '可是非諧性也會跟著變小，只是變得很慢，只按冪次下降；所以比值不是越大越好。',
  '典型的設計，比值落在五十到一百；在這個範圍裡，電荷色散已經很小，非諧性還留著兩百多兆赫。'], ['jj_talk_p19', 'jj_talk_p20']),
 ('我的參數卡：範例', [
  '來看學程簡報的一張範例卡：約瑟夫森能量十五吉赫，充電能量兩百五十兆赫，比值剛好六十。',
  '算出來的頻率是五點二一吉赫，非諧性負兩百八十三兆赫；對應的總電容，大約七十七點五飛法拉。',
  '用近似公式驗算：八乘十五再乘零點二五，開根號約五點四八，減掉零點二五是五點二三，和數值解的五點二一很接近。'], ['transmon_p12', 'jj_talk_p19']),
 ('常見誤解：卡上數字不是保證', [
  '最常見的誤解是：卡上寫五點二一吉赫，做出來就一定是五點二一；其實參數卡只是設計目標。',
  '接面的氧化層只要厚一點或薄一點，臨界電流就會改變，約瑟夫森能量跟著變，實際頻率也就偏移了。',
  '暫停影片想一想：如果約瑟夫森能量從十五變成十五點三吉赫，多了百分之二，頻率大約會偏多少？'], ['curriculum', 'jj_talk_p21', 'jj_talk_p19']),
 ('實作：做一張參數卡', [
  '實作的時候用參數設計器：可以是教材裡的小程式，也可以是超導量子位元三維動畫裡、大十字電容的分頁。',
  '先訂一個目標，例如頻率五吉赫，再調整兩個能量，直到三個數字都落在典型範圍裡，抄到參數卡上。',
  '接著打開能階場景，把比值調到差不多的位置，看能階的間隔是不是一格比一格小，驗證你的卡片。'], ['curriculum', 'tr_scene', 'potential_scene']),
 ('換你改造：加上讀取腔', [
  '下半場換你：替參數卡加一個讀取腔頻率，例如七吉赫，比量子位元的五吉赫高兩吉赫，這個差距叫失諧。',
  '失諧要遠大於兩者的耦合，大約一百兆赫；這樣它們不會交換能量，只會互相推動頻率，讀取腔的頻率就能透露量子位元的狀態。',
  '失諧越小，量子位元的能量越容易經由讀取腔漏掉；簡報算過，失諧兩吉赫時，能量弛豫時間會被限制在大約五十七微秒，所以還要加濾波器。'],
  ['curriculum', 'jj_talk_p28', 'jj_talk_p37']),
 ('兩小時的設計發表會', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘一起用參數設計器做參數卡，再到能階場景驗證，然後休息十分鐘。',
  '下半場三十分鐘，你替參數卡加上讀取腔頻率，並說明失諧為什麼要這麼大；接著十分鐘交換角色，由你教爸爸操作和原理。',
  '最後五分鐘錄音總結，替你的參數卡取個名字，再存一個版本。'], ['curriculum']),
 ('最後一關：工程答辯', [
  '最後一關是工程答辯：請不看稿說出卡上的三個數字，再替每個數字說一句，為什麼選這個值、放棄了什麼。',
  '再指出一個要注意的地方：參數卡是設計目標，製程誤差會讓實際頻率偏移，做好之後還要再量一次。',
  '今天的作品是超導量子位元參數卡，也是這個模組的發表；下一堂進入新模組，讀取量子位元要做到快、準、不破壞；我是陳犀牛，保持好奇，我們下次見！'],
  ['curriculum', 'neighbors']),
]

VISIBLE = [
 ['量子電腦學程 第三十二堂', '模組發表\n設計我的 transmon', '用數字支持每一個設計決定', '量子第三十二堂  ·  依課綱製作的課前教學版'],
 ['三個重點', '三個數字，各有取捨',
  '01 頻率', 'f₀₁ 選多高\n4–6 GHz', '→', '02 非諧性', 'α ≈ −E_C\n只挑 0 和 1', '→', '03 比值', 'E_J／E_C\n50–100',
  '今天的作品：transmon 參數卡'],
 ['參數卡上有什麼', '學程簡報的典型數字',
  '01', '頻率 f₀₁', '約 4–6 GHz',
  '02', '非諧性 α', '約 −200～−300 MHz',
  '03', 'E_J／E_C', '約 50–100'],
 ['數字一：頻率', 'f₀₁ ≈ √(8E_J E_C) − E_C', '選頻率的取捨',
  '換算溫度', '5 GHz ≈ 0.24 K', '冷凍機', '只有 10–20 mK', '離讀取腔', '錯開約 2 GHz', '離鄰居', '例如錯開 200 MHz',
  '典型範圍：4–6 GHz'],
 ['數字二：非諧性', 'α = f₁₂ − f₀₁ ≈ −E_C',
  '等間距', '每一格一起共振', '→', '不等距', '微波只挑 0 和 1',
  '太小：脈衝要放慢，才不會漏到 |2⟩',
  '典型：−200～−300 MHz'],
 ['數字三：E_J／E_C', '比值加大，兩件事一起變',
  '電荷色散', '指數下降，很快變小', '非諧性', '冪次下降，慢慢變小', '取捨', '50–100 剛剛好',
  '比值不是越大越好'],
 ['我的參數卡：範例', '學程簡報的一組數字',
  'E_J/h 15 GHz ÷ E_C/h 250 MHz → 比值 60',
  'f₀₁', '5.21 GHz', 'α', '−283 MHz', 'C_Σ', '約 77.5 fF',
  '近似公式驗算：√30 − 0.25 ≈ 5.23 GHz'],
 ['常見誤解：卡上數字不是保證', '參數卡是設計目標',
  '一、卡上是設計目標\n二、氧化層一變，E_J 就變\n三、實際頻率會偏移',
  'E_J：15 → 15.3 GHz', 'f₀₁ 偏多少？', '提示：\nf₀₁ 約跟著 √E_J',
  '暫停影片：頻率大約偏多少？'],
 ['實作：做一張參數卡', '爸爸和孩子一起設計',
  '參數設計器', '訂目標、調能量\n抄下三個數字',
  '能階場景', '調到同一個比值\n看間隔變小',
  '每個數字旁邊寫一句取捨'],
 ['換你改造：加上讀取腔', '替參數卡加一個讀取腔頻率',
  '01', '讀取腔頻率', '例如 7 GHz',
  '02', '失諧', '約 2 GHz，遠大於 g ≈ 100 MHz',
  '03', '為什麼要這麼大', '不交換能量，只推頻率'],
 ['兩小時的設計發表會', '影片先引路，接下來算、驗、改、教',
  '00–25', '開場＋三個數字', '25–65', '做參數卡＋驗證', '65–75', '休息十分鐘',
  '75–105', '加上讀取腔頻率', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：用數字支持設計決定'],
 ['最後一關：工程答辯', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '說出三個數字', '頻率、非諧性、比值',
  '02', '說出每個取捨', '為什麼選、放棄什麼',
  '03', '指出一個注意事項', '製程誤差讓頻率偏移',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從上一堂偵探辦案接到模組發表；好玩機制「工程答辯」', '封面版型＋陳犀牛', '猜猜一顆超導量子位元要定哪些數字'),
 ('三個重點：頻率、非諧性、E_J／E_C；三個數字互相牽動', '三步流程卡＋黃字', '認識今天的作品：transmon 參數卡'),
 ('參數卡上有什麼：典型 f₀₁ 4–6 GHz、α −200～−300 MHz、E_J／E_C 50–100（另有 I_c、C_Σ）', '三點條列＋陳犀牛', '把三個範圍抄到參數卡空格旁'),
 ('數字一 頻率：f₀₁ ≈ √(8E_JE_C) − E_C；5 GHz ≈ 0.24 K ≫ 10–20 mK；離讀取腔約 2 GHz、鄰居例如 200 MHz', '面板四張卡＋黃字', '說出頻率不能太低的理由'),
 ('數字二 非諧性：α = f₁₂ − f₀₁ ≈ −E_C；等間距會一起共振；太小脈衝要放慢', '雙框對照＋白字＋黃字', '說出非諧性太小會怎樣'),
 ('數字三 E_J／E_C：電荷色散指數下降、非諧性冪次下降；50–100', '三張卡＋黃字', '說出比值為什麼不是越大越好'),
 ('範例卡：E_J/h 15 GHz、E_C/h 250 MHz、比值 60、f₀₁ 5.21 GHz、α −283 MHz、C_Σ ≈ 77.5 fF；近似公式 5.23 GHz', '路徑一行＋三張卡＋黃字', '用近似公式驗算一次'),
 ('常見誤解：參數卡是設計目標；氧化層厚度 → I_c → E_J → 頻率偏移', '左三行＋右欄＋黃字', '暫停想：E_J 多 2%，頻率偏多少'),
 ('實作：用參數設計器（transmon_card.py 或 transmon-3d#capacitor）做參數卡，再到 index.html#potential 驗證能階', '左右比較卡＋黃字', '父子做參數卡、驗證能階'),
 ('獨立改造：加讀取腔頻率（例如 7 GHz）、失諧約 2 GHz ≫ g ≈ 100 MHz；不交換能量、只推頻率；Purcell 上限約 57 μs', '三點條列＋陳犀牛', '寫下讀取腔頻率與失諧的理由'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：三個數字與取捨、製程誤差讓頻率偏移；預告 Q033', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Curriculum rows (Q031, Q032, Q033), the curriculum slide decks JJ_Microwave_Readout_Talk.pptx p19, p20, p21, p28, p37 and '
                      'transmon.pptx p12 (slide text, tables and speaker notes extracted with python-pptx), the animation sources '
                      'animations/js/scenes/04_potential.js (index.html#potential), animations/js/core.js, animations/css/style.css and '
                      'animations/transmon-3d.html (chapter 1 capacitor tab, chapter 3, chapter 6) read by the producing agent on 2026-11-18; '
                      'the transmon levels (f₀₁, α, the E_J 15 → 15.3 GHz shift, the scene readouts) were recomputed by diagonalising the same '
                      'charge-basis Hamiltonian in transmon_card.py (Python 3) and numpy.',
        not_verified=['典型範圍（f₀₁ 4–6 GHz、α −200～−300 MHz、E_J／E_C 50–100、I_c 20–50 nA、C_Σ 60–100 fF）取自學程簡報 p20 的整理，本集沒有另找業界最新統計',
                      '「和讀取腔錯開大約兩吉赫」取自簡報 p28、p37 的範例（5 GHz 與 7 GHz）；「和隔壁錯開，例如兩百兆赫」取自 transmon-3d 第 6 章的示意配置，都是例子，不是固定規格',
                      '「熱擾動很難把它激發」是以 hf/k_B ≈ 0.24 K 遠大於 10–20 mK 做的數量級說明，本集沒有計算熱激發機率',
                      '「非諧性太小脈衝要放慢」只講定性（transmon-3d 第 3 章、Q025），本集未計算閘時間',
                      '製程誤差只舉氧化層厚度影響臨界電流（簡報 p21 備註）；本集不估計真實製程的頻率誤差大小，暫停題的「多百分之二」是本集設計的數字',
                      '暫停題答案（約 +55 MHz、約 1%）由 transmon_card.py 以 E_C/h = 250 MHz 對角化求得，不是量測',
                      'Purcell 上限約 57 μs 是簡報 p37 在 g = 100 MHz、κ ≈ 1.1 MHz 下的範例計算，本集不推導',
                      '課綱的「★ transmon 參數設計器」尚未有獨立網頁工具；本集以教材 transmon_card.py 與 transmon-3d.html 第 1 章電容分頁代替',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看',
                      '本集未錄影試拍；動畫段（index.html#potential 的讀數與金色標籤、transmon-3d#capacitor 讀數在 1600×900 錄影下是否清楚）待 v2 試錄確認'],
        tts_date='2026-11-18')

"""Q025 E_J 與 E_C：兩個能量尺度 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q025/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q025', 'q025-ej-ec-two-energy-scales', '2026-11-18'
TITLE = 'E_J 與 E_C：兩個能量尺度'
TOPIC = 'E_J 與 E_C：兩個能量尺度'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q025/lesson.json',
    'neighbors': f'{REPO} academy/lessons/Q024/brief.md、academy/lessons/Q026/brief.md',
    'jj_talk_p14': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p14（含講者備註）',
    'jj_talk_p15': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p15（含講者備註）',
    'jj_talk_p18': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p18（含講者備註）',
    'jj_talk_p19': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p19（含講者備註）',
    'transmon_p14': f'{REPO} slides/transmon.pptx p14（含講者備註）',
    'transmon_p15': f'{REPO} slides/transmon.pptx p15（含講者備註）',
    'potential_scene': f'{REPO} animations/index.html#potential（animations/js/scenes/04_potential.js、js/core.js U.transmon）',
    'tr_capacitor': f'{REPO} animations/transmon-3d.html#capacitor（第 1 章「大十字電容的作用」分頁：capStats、fillCap）',
    'wiki_transmon': 'https://en.wikipedia.org/wiki/Transmon',
    'wiki_cpb': 'https://en.wikipedia.org/wiki/Charge_qubit',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q025 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（知道 E_J／E_C 比值決定量子位元的性格，以及電荷色散為什麼會被壓下來）、動手任務（在場景掃描 E_J／E_C，記錄非諧性與電荷色散的變化）、'
                '孩子獨立改造（找出一個「非諧性夠、電荷雜訊又小」的折衷點並說明理由）、好玩機制（設計改造）、作品（E_J／E_C 掃描圖）、家長課前準備（index.html#potential）、'
                '120 分鐘流程、驗收與常見誤解（E_J／E_C 越大不是越好；非諧性會跟著變小）、生活技能支線（在兩個互相衝突的目標中取捨）'},
    {'id': 'neighbors', 'title': '量子電腦學程 Q024、Q026 課綱', 'publisher': REPO, 'url': SRC['neighbors'],
     'usedFor': '上一堂：JJ 是非線性電感（JJ 的電感會隨電流改變，這個非線性是做出量子位元的關鍵）；'
                '下一堂：傾斜洗衣板（用相位粒子在洗衣板位勢中的運動理解 RCSJ 模型與 I–V 遲滯；在場景加大偏壓電流，記錄粒子何時從井中滑出）'},
    {'id': 'jj_talk_p14', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p14：JJ 是一個「非線性電感」', 'publisher': REPO, 'url': SRC['jj_talk_p14'],
     'usedFor': '備註：電感值隨相位（電流）改變、沒有耗散；「把它和電容並聯，就得到一個非線性振盪器，也就是 transmon 量子位元」；JJ 同時是 EJ 的來源'},
    {'id': 'jj_talk_p15', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p15：兩個能量尺度：EJ 與 EC', 'publisher': REPO, 'url': SRC['jj_talk_p15'],
     'usedFor': 'H = 4EC(n̂ − ng)² − EJ cos φ̂；EJ = Φ0 Ic / 2π：Cooper pair 穿隧的耦合能（位勢深度），由接面面積、氧化層 → Ic 決定，Ic = 30 nA → ≈ 15 GHz；'
                'EC = e² / 2CΣ：多加一顆電子的靜電能（「質量」的倒數），由總電容 CΣ（含大電容板）決定，CΣ = 80 fF → ≈ 240 MHz；'
                '類比：質量 ∝ 1/EC 的粒子在深度 ∝ EJ 的餘弦井中運動，EJ/EC 決定量子位元類型；備註：EC 越小、粒子越重、越不容易被量子漲落晃動；ng 是背景電荷造成的偏移'},
    {'id': 'jj_talk_p18', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p18：以 JJ 為核心的量子位元家族', 'publisher': REPO, 'url': SRC['jj_talk_p18'],
     'usedFor': '電荷（CPB）EJ/EC ~1、對電荷雜訊極敏感；Transmon：JJ/SQUID ∥ 大電容、EJ/EC 50–100、非諧性 −200～−300 MHz、業界主流、抗電荷雜訊；'
                '備註：電荷量子位元也叫 Cooper pair box，對背景電荷非常敏感；transmon 在旁邊並聯一個大電容把 EJ/EC 拉到 50 到 100'},
    {'id': 'jj_talk_p19', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p19：Transmon 深入：EJ/EC 與電荷色散', 'publisher': REPO, 'url': SRC['jj_talk_p19'],
     'usedFor': 'ħω01 ≈ √(8EJEC) − EC；α ≈ −EC（只以冪次下降）；εm ∝ e^−√(8EJ/EC)（指數下降）；EJ/EC 越大，能階越平直；'
                '備註：背景電荷來自基板或介面中隨機跳動的電荷、無法完全消除；EJ/EC = 1 時能階隨 ng 劇烈起伏、相干性很差；5、10 起伏迅速變小；到 50 幾乎是平的；'
                '犧牲一點點非諧性，換來對電荷雜訊幾乎免疫'},
    {'id': 'transmon_p14', 'title': 'Transmon 筆記簡報 p14：非諧性：能階不再等距', 'publisher': REPO, 'url': SRC['transmon_p14'],
     'usedFor': 'Transmon：E12 比 E01 低 283 MHz（5.21／4.93 GHz）；備註：非諧性遠大於控制脈衝的頻寬，所以可以只操作最低兩個能階'},
    {'id': 'transmon_p15', 'title': 'Transmon 筆記簡報 p15：為何 EJ/EC 要大', 'publisher': REPO, 'url': SRC['transmon_p15'],
     'usedFor': 'EJ/EC 從 10 到 60，電荷色散 62.8 MHz → 1.9 kHz（約 3 萬倍）；同一範圍內非諧性 −353 → −283 MHz（只少兩成）；'
                '備註：電荷色散是 f01 隨背景電荷 n_g 的最大漂移量，E_C 固定為 250 MHz，數值解'},
    {'id': 'potential_scene', 'title': 'JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon（能階與非諧性）', 'publisher': REPO, 'url': SRC['potential_scene'],
     'usedFor': '動畫段 1：右下小圖「電荷色散：能階隨背景電荷 n_g 的變化」三條線（藍、紅、綠）；按鈕「CPB：E_J/E_C = 1」「10」「Transmon：50」；'
                '場景說明：比值小時能階對背景電荷極敏感，約 50 時電荷色散指數級下降、非諧性只以冪次減少'},
    {'id': 'tr_capacitor', 'title': 'Transmon 3D 第 1 章：大十字電容的作用（#capacitor 分頁）', 'publisher': REPO, 'url': SRC['tr_capacitor'],
     'usedFor': '動畫段 2、3 與實作：C_Σ 滑桿 5–200 fF、E_J/h 固定 15 GHz、讀數（電容、充電能、E_J/E_C、f₀₁、非諧性、電荷色散、判斷）；'
                '說明「電容太大，α 太小，脈衝容易漏到 |2⟩」；判斷 < 20「電荷雜訊主導」、≤ 120「transmon 區間」、> 120「非諧性偏小，閘需放慢」'},
    {'id': 'wiki_transmon', 'title': 'Wikipedia: Transmon', 'publisher': 'Wikipedia', 'url': SRC['wiki_transmon'],
     'usedFor': 'transmon 與 Cooper-pair box 用同一個 Hamiltonian，唯一的差別是 EJ/EC 比值；用大並聯電容提高比值；好處是能階幾乎不受 offset charge 影響，'
                '壞處是非諧性變小；E10 隨 ng 的變化隨比值指數下降，非諧性只以 (EJ/EC)^−1/2 的代數方式下降；2007 年 Yale 提出'},
    {'id': 'wiki_cpb', 'title': 'Wikipedia: Charge qubit', 'publisher': 'Wikipedia', 'url': SRC['wiki_cpb'],
     'usedFor': 'charge qubit 也叫 Cooper-pair box，基底狀態是小島上有無多餘的 Cooper pair；ng 為 effective offset charge'},
]

SCENES = [
 ('E_J 與 E_C：兩個能量尺度', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第二十五堂，約瑟夫森能量與充電能量：兩個能量尺度，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂看到約瑟夫森接面的電感會隨電流改變；把這個非線性的電感和電容並聯，就得到能階不等距、可以當量子位元的電路。',
  '今天要認識描述這個電路的兩個能量：約瑟夫森能量和充電能量，看看它們的比值怎麼決定量子位元的性格。'], ['curriculum', 'neighbors', 'jj_talk_p14']),
 ('三個重點', [
  '今天有三個重點：第一，約瑟夫森能量來自接面，決定位能山谷有多深；充電能量來自電容，是多放一顆電子要花的能量。',
  '第二，兩者的比值決定量子位元的性格；第三，比值加大時，電荷色散急速下降，非諧性卻只是慢慢變小。',
  '今天的作品是一張掃描圖：把比值從小調到大，記下非諧性和電荷色散怎麼變。'], ['curriculum', 'jj_talk_p15', 'jj_talk_p19']),
 ('約瑟夫森能量', [
  '先看約瑟夫森能量：它代表庫柏電子對穿過接面的耦合有多強，在位能圖上，就是那個餘弦形山谷有多深。',
  '它由接面決定：接面的面積和氧化層的厚度決定臨界電流，臨界電流越大，約瑟夫森能量就越大。',
  '典型的數字是：臨界電流三十奈安培，約瑟夫森能量換算成頻率，大約是十五吉赫。'], ['jj_talk_p15']),
 ('充電能量', [
  '再看充電能量：它是多放一顆電子到電容上，要花掉的靜電能量。',
  '電容越大，多放一顆電子越不費力，充電能量就越小；所以量子位元旁邊，常會並聯一塊很大的電容板。',
  '總電容八十飛法拉的時候，充電能量大約兩百四十兆赫，比約瑟夫森能量小了六十倍左右。'], ['jj_talk_p15', 'wiki_transmon']),
 ('比值決定性格', [
  '可以把這個電路想成一顆粒子在山谷裡晃動：約瑟夫森能量是山谷的深度，充電能量越小，這顆粒子就越重。',
  '比值接近一的叫電荷量子位元，也叫庫柏電子對盒子；比值拉到五十到一百，就是現在業界主流的設計。',
  '有趣的是，這兩種量子位元用的是同一條能量公式，唯一的差別，就是這個比值。'], ['jj_talk_p15', 'jj_talk_p18', 'wiki_transmon', 'wiki_cpb']),
 ('背景電荷與電荷色散', [
  '比值為什麼重要？晶片的基板和介面裡，有一些電荷會隨機跳動，叫做背景電荷，這種雜訊沒辦法完全消除。',
  '背景電荷一跳，量子位元的頻率也可能跟著偏移；頻率隨背景電荷變化的最大幅度，叫做電荷色散。',
  '比值是一的時候，能階隨背景電荷劇烈起伏，頻率一直被打亂，量子位元的相干性很差。'], ['jj_talk_p19', 'transmon_p15', 'jj_talk_p18']),
 ('電荷色散被壓下來', [
  '比值加大時，電荷色散隨比值的平方根呈指數下降；非諧性卻只是慢慢變小，大約維持在負的充電能量附近。',
  '學程簡報算過：比值從十加到六十，電荷色散從六十二點八兆赫，降到一點九千赫，大約小了三萬倍。',
  '同一個範圍裡，非諧性只從負三百五十三兆赫變成負兩百八十三兆赫，只少兩成；用一點非諧性，換來幾乎不怕背景電荷，非常划算。'],
  ['jj_talk_p19', 'transmon_p15', 'wiki_transmon']),
 ('越大不是越好', [
  '最常見的誤解是：比值越大越好；其實比值大到某個程度，電荷色散早就小到不必擔心，非諧性卻還在繼續變小。',
  '非諧性太小，一到二的頻率就和零到一太接近，微波脈衝要放慢，才不會漏到更高的能階，邏輯閘也就跟著變慢。',
  '暫停影片想一想：如果電容一直加大，加到無限大，這個電路最後會變成哪一堂看過的東西？'], ['curriculum', 'tr_capacitor', 'transmon_p14', 'wiki_transmon']),
 ('實作：掃描比值', [
  '實作的時候，父子一起打開超導量子位元的三維動畫，找到大十字電容的分頁，裡面有一根調整電容的滑桿。',
  '爸爸拉滑桿，從十飛法拉一路拉到兩百，孩子把每一格的比值、非諧性和電荷色散記在表上。',
  '最後把比值畫在橫軸，非諧性和電荷色散各畫一條線；電荷色散的數字相差好幾個零，縱軸要用每一格乘以十的刻度。'], ['curriculum', 'tr_capacitor']),
 ('換你改造：找折衷點', [
  '下半場換你：找一個非諧性夠大、電荷色散又小的折衷點，並且說明理由。',
  '先自己訂兩條標準，例如非諧性至少兩百兆赫、電荷色散低於十千赫，再在掃描圖上，圈出兩條都符合的範圍。',
  '最後挑一個點，用一句話說明：你放棄了什麼，又換到了什麼。'], ['curriculum', 'tr_capacitor']),
 ('兩小時的比值掃描工坊', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘一起掃描比值、畫出掃描圖，然後休息十分鐘。',
  '下半場三十分鐘，你訂標準、找折衷點並寫下理由；接著十分鐘交換角色，由你教爸爸操作和原理。',
  '最後五分鐘錄音總結，替你的掃描圖取個名字，再存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸兩個能量', [
  '最後一關，請不看稿說出：兩個能量各代表什麼？比值大和比值小的量子位元，有什麼不同？',
  '再指出一個要注意的地方：比值越大不是越好，電荷色散變小的同時，非諧性也跟著變小。',
  '今天的作品是比值掃描圖，下一堂要看傾斜的洗衣板：把相位想成一顆在波浪形位能上的小球，看電流加大時它怎麼滑出山谷；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'neighbors']),
]

VISIBLE = [
 ['量子電腦學程 第二十五堂', 'E_J 與 E_C\n兩個能量尺度', '井有多深、粒子多重，比值決定性格', '量子第二十五堂  ·  依課綱製作的課前教學版'],
 ['三個重點', '兩個能量，一個比值',
  '01 兩個能量', '井的深度 E_J\n充電能 E_C', '→', '02 比值定性格', '比值小怕電荷\n比值大才穩定', '→', '03 有得有失', '色散急速下降\n非諧性慢慢變小',
  '今天的作品：E_J／E_C 掃描圖'],
 ['約瑟夫森能量 E_J', '庫柏電子對穿隧的耦合能',
  '01', '位能井的深度', '餘弦山谷有多深',
  '02', '由接面決定', '面積、氧化層 → Ic',
  '03', '典型數值', 'Ic 30 nA → 約 15 GHz'],
 ['充電能量 E_C', '多放一顆電子的靜電能', '四個觀察',
  '第一點', 'E_C = e²/2C', '第二點', '電容越大越小', '第三點', '80 fF 約 240 MHz', '第四點', '像質量的倒數',
  '大電容板讓充電能量變小'],
 ['比值決定性格', '同一條公式，只差一個比值',
  '電荷量子位元', 'E_J／E_C ≈ 1', '⇄', '主流設計', 'E_J／E_C ≈ 50–100',
  'H = 4E_C(n − n_g)² − E_J cos φ',
  '井越深、粒子越重，越不怕晃'],
 ['背景電荷與電荷色散', '基板裡亂跳的電荷',
  '背景電荷 n_g', '隨機跳動的雜訊', '電荷色散', '頻率的最大漂移', '比值 = 1', '能階劇烈起伏',
  '頻率被打亂，相干性很差'],
 ['電荷色散被壓下來', '指數下降，對上冪次下降',
  'E_J／E_C 從 10 加到 60（E_C = 250 MHz）',
  '電荷色散', '62.8 MHz → 1.9 kHz', '約 3 萬倍', '指數下降', '非諧性 α', '−353 → −283 MHz',
  '用一點非諧性，換來不怕電荷雜訊'],
 ['越大不是越好', '非諧性跟著變小',
  '一、色散早就夠小\n二、非諧性還在減\n三、閘要放慢',
  '電容無限大', '會變成什麼？', '提示：\n等距的梯子',
  '暫停影片：電容一直加大，會變成什麼？'],
 ['實作：掃描 E_J／E_C', '拉滑桿，記三個數字',
  '拉滑桿的人（爸爸）', '電容 C_Σ\n10 → 200 fF',
  '記錄的人（你）', '比值、非諧性\n電荷色散',
  '電荷色散用 ×10 刻度畫'],
 ['換你改造：找折衷點', '兩個目標，互相拉扯',
  '01', '訂兩條標準', '|α| ≥ 200 MHz、色散 < 10 kHz',
  '02', '圈出範圍', '兩條都符合的區間',
  '03', '挑一個點', '放棄什麼、換到什麼'],
 ['兩小時的比值掃描工坊', '影片先引路，接下來掃、畫、選、教',
  '00–25', '開場＋兩個能量', '25–65', '掃描比值＋畫圖', '65–75', '休息十分鐘',
  '75–105', '找折衷點＋理由', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：在衝突的目標中取捨'],
 ['最後一關：教爸爸兩個能量', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '說出兩個能量', '井的深度、充電能',
  '02', '說出比值的性格', '小的怕電荷、大的才穩',
  '03', '指出一個注意事項', '比值越大不是越好',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從上一堂非線性電感接到兩個能量尺度', '封面版型＋陳犀牛', '想一想描述電路要哪兩個能量'),
 ('三個重點：兩個能量、比值定性格、色散急降而非諧性慢減', '三步流程卡＋黃字', '認識今天的作品：掃描圖'),
 ('約瑟夫森能量：穿隧耦合能、位能井深度、由 Ic 決定、30 nA ≈ 15 GHz', '三點條列＋陳犀牛', '說出 E_J 代表什麼'),
 ('充電能量：e²/2C、電容越大越小、80 fF ≈ 240 MHz、像質量的倒數', '面板四張卡＋黃字', '說出 E_C 代表什麼'),
 ('比值決定性格：CPB ≈ 1、主流設計 50–100、同一條 Hamiltonian', '雙框對照＋白字＋黃字', '用山谷和粒子說明比值'),
 ('背景電荷與電荷色散：雜訊來源、定義、比值 1 時劇烈起伏', '三張步驟卡＋黃字', '說出電荷色散是什麼'),
 ('電荷色散被壓下來：指數對冪次、10 → 60 時 62.8 MHz → 1.9 kHz、α −353 → −283 MHz', '路徑一行＋三張卡＋黃字', '說出為什麼這筆交換划算'),
 ('越大不是越好：色散早就夠小、非諧性還在減、閘要放慢', '左三行＋右欄＋黃字', '暫停想電容無限大會怎樣'),
 ('實作：transmon-3d.html#capacitor 拉 C_Σ 10 → 200 fF，記比值、α、電荷色散', '左右比較卡＋黃字', '父子一起掃描、畫掃描圖'),
 ('獨立改造：訂標準、圈範圍、挑折衷點並說明取捨', '三點條列＋陳犀牛', '寫下放棄了什麼、換到什麼'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：兩個能量、比值性格、越大不是越好；預告 Q026', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Curriculum rows (Q024, Q025, Q026), the curriculum slide decks JJ_Microwave_Readout_Talk.pptx p14, p15, p18, p19 and '
                      'transmon.pptx p14–15 (slide text, tables and speaker notes extracted with python-pptx), and the animation sources '
                      'animations/js/scenes/04_potential.js with js/core.js (index.html#potential) and animations/transmon-3d.html (chapter 1 '
                      '#capacitor tab: capStats, fillCap) read by the producing agent on 2026-11-18; the scene readouts were recomputed in Node '
                      'with the pages\' own code and again in Python by ejec_scan.py; the E_J/E_C trade-off and naming checked against the '
                      'Wikipedia articles Transmon and Charge qubit (raw wikitext fetched 2026-11-18).',
        not_verified=['「臨界電流三十奈安培對應約十五吉赫」「八十飛法拉對應約兩百四十兆赫」取自學程簡報 JJ_Microwave_Readout_Talk p15 的典型值，不是某一顆晶片的實測值',
                      '「比值五十到一百是業界主流」取自學程簡報 p18 的典型範圍；各公司、各代晶片的實際設計會不同',
                      '「十到六十時電荷色散 62.8 MHz → 1.9 kHz、非諧性 −353 → −283 MHz」是 transmon 簡報 p15 在 E_C = 250 MHz 下的數值解'
                      '（非諧性取背景電荷 0 與 0.5 兩點的平均）；動畫 index.html#potential 的讀數只取背景電荷 0，比值十時顯示 −637 MHz，兩者定義不同，旁白不混用',
                      '「非諧性只以冪次下降」的冪次（約比值的負二分之一次方，指相對非諧性）來自維基百科 Transmon 條目；旁白只說「慢慢變小」，不念出冪次',
                      '「山谷與粒子」「粒子越重越不怕晃」是學程簡報 p15 的力學類比，不是嚴格的物理描述',
                      '「微波脈衝要放慢，邏輯閘跟著變慢」依 transmon-3d 第 1 章判斷文字「非諧性偏小，閘需放慢」與第 3 章說明（脈衝越短頻譜越寬、越容易漏到 |2⟩）；本集不估算實際閘時間',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看',
                      '本集未錄影試拍；動畫段（index.html#potential 小圖在比值一時紅線超出上緣被截平、綠線貼在上緣；transmon-3d.html#capacitor 面板捲到底後滑桿與讀數是否同時入鏡、'
                      '十字板粗細變化是否看得清楚）待 v2 試錄確認'],
        tts_date='2026-11-18')

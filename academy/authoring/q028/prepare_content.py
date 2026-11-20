"""Q028 量子位元家族圖鑑 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q028/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q028', 'q028-qubit-family-cards', '2026-11-18'
TITLE = '量子位元家族圖鑑'
TOPIC = '量子位元家族圖鑑'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q028/lesson.json',
    'neighbors': f'{REPO} academy/lessons/Q026/brief.md、academy/lessons/Q027/brief.md、academy/lessons/Q029/brief.md',
    'jj_talk_p16': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p16（含講者備註）',
    'jj_talk_p18': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p18（含講者備註）',
    'jj_talk_p19': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p19（含講者備註）',
    'jj_talk_p20': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p20（含講者備註）',
    'potential_scene': f'{REPO} animations/index.html#potential（animations/js/scenes/04_potential.js、js/core.js U.transmon）',
    'washboard_scene': f'{REPO} animations/index.html#washboard（animations/js/scenes/05_washboard.js）',
    'tr_capacitor': f'{REPO} animations/transmon-3d.html#capacitor（第 1 章「大十字電容的作用」分頁：capStats、fillCap）',
    'wiki_cpb': 'https://en.wikipedia.org/wiki/Charge_qubit',
    'wiki_transmon': 'https://en.wikipedia.org/wiki/Transmon',
    'wiki_fluxonium': 'https://en.wikipedia.org/wiki/Fluxonium',
    'wiki_phase': 'https://en.wikipedia.org/wiki/Phase_qubit',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q028 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（比較 transmon、fluxonium、電荷與相位量子位元的結構與優缺點）、動手任務（為四種量子位元各做一張圖鑑卡：結構、頻率、優點、弱點）、'
                '孩子獨立改造（自己設計一張「理想量子位元」卡，說明它要跟誰借優點）、好玩機制（解鎖成就（圖鑑卡））、作品（量子位元圖鑑卡）、家長課前準備（圖鑑卡模板）、'
                '120 分鐘流程、驗收與常見誤解（沒有在所有指標都最好的量子位元；廠商選擇各有考量）、生活技能支線（整理比較表）'},
    {'id': 'neighbors', 'title': '量子電腦學程 Q026、Q027、Q029 課綱', 'publisher': REPO, 'url': SRC['neighbors'],
     'usedFor': '前兩堂：傾斜洗衣板（相位粒子在洗衣板位勢中的運動）；上一堂：SQUID（兩個 JJ 並聯成環可以用磁通調整頻率，認識甜蜜點）；'
                '下一堂：晶片怎麼做：雙角度蒸鍍（理解 Dolan bridge 兩次斜向蒸鍍如何做出重疊的 JJ）'},
    {'id': 'jj_talk_p16', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p16：RCSJ 模型與傾斜洗衣板位勢', 'publisher': REPO, 'url': SRC['jj_talk_p16'],
     'usedFor': '備註：「早期的『相位量子位元』就是在接近 Ic 的偏壓下，利用井中最低的兩個能階。現代的 transmon 則是在不加偏壓的情況下工作」'},
    {'id': 'jj_talk_p18', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p18：以 JJ 為核心的量子位元家族', 'publisher': REPO, 'url': SRC['jj_talk_p18'],
     'usedFor': '家族表：電荷（CPB）小島 + 1 JJ、EJ/EC ~1、5–10 GHz、非諧性大、最早的超導量子位元、對電荷雜訊極敏感；'
                'Transmon JJ/SQUID ∥ 大電容、50–100、4–6 GHz、−200～−300 MHz、業界主流、抗電荷雜訊、結構簡單；'
                '磁通（Flux）超導環 + 3–4 JJ；Fluxonium 1 JJ ∥ 超電感（JJ 陣列）、~1–10、0.1–1 GHz、極大、T1 可達 ms、低頻高非諧性；'
                '相位（Phase）電流偏壓 1 JJ、≫ 1、5–10 GHz、中、洗衣板井中能階、已較少使用；共同點「都靠 JJ 提供『無耗散的非線性』；差別在 EJ/EC 比值與電路拓樸」；'
                '「數值為典型範圍，實際依設計而異」；備註：Transmon「Google、IBM 都用它的變形」、Fluxonium 的超電感「通常是由上百個大 JJ 串成的陣列」、「相位量子位元……現在比較少用了」'},
    {'id': 'jj_talk_p19', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p19：Transmon 深入：EJ/EC 與電荷色散', 'publisher': REPO, 'url': SRC['jj_talk_p19'],
     'usedFor': '備註：背景電荷 ng 來自基板或介面中隨機跳動的電荷；EJ/EC 等於 1 時能階隨 ng 劇烈起伏，背景電荷一跳頻率就跟著變；到 50 能階幾乎是平的'},
    {'id': 'jj_talk_p20', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p20：Transmon 典型參數', 'publisher': REPO, 'url': SRC['jj_talk_p20'],
     'usedFor': 'f01 4–6 GHz、非諧性 −200～−300 MHz、EJ/EC 50–100、T1（最佳實驗）0.1–1 ms'},
    {'id': 'potential_scene', 'title': 'JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon（電荷色散小圖）', 'publisher': REPO, 'url': SRC['potential_scene'],
     'usedFor': '動畫段 1：右下小圖「電荷色散：能階隨背景電荷 n_g 的變化」三條線；按鈕「CPB：E_J/E_C = 1」「Transmon：50」'},
    {'id': 'washboard_scene', 'title': 'JJ 與微波讀取 3D 場景 5：RCSJ 模型——傾斜洗衣板位勢', 'publisher': REPO, 'url': SRC['washboard_scene'],
     'usedFor': '動畫段 2：偏壓電流滑桿、位障標籤、零電壓態讀數、ω_p(I) 讀數；場景說明「早期的相位量子位元就是利用這些能階；現代 transmon 則在 I = 0（不傾斜）下工作」'},
    {'id': 'tr_capacitor', 'title': 'Transmon 3D 第 1 章：大十字電容的作用（#capacitor 分頁）', 'publisher': REPO, 'url': SRC['tr_capacitor'],
     'usedFor': '動畫段 3：C_Σ 滑桿、讀數（比值、非諧性、電荷色散、判斷）、「回到 77.5 fF」按鈕'},
    {'id': 'wiki_cpb', 'title': 'Wikipedia: Charge qubit', 'publisher': 'Wikipedia', 'url': SRC['wiki_cpb'],
     'usedFor': 'also known as Cooper-pair box；基底狀態是小島上有沒有多餘的 Cooper pair；小島經 JJ 接到超導庫；典型 T2 約 1–2 μs；1999 年 Nakamura 等人首次觀察到同調振盪'},
    {'id': 'wiki_transmon', 'title': 'Wikipedia: Transmon', 'publisher': 'Wikipedia', 'url': SRC['wiki_transmon'],
     'usedFor': '2007 年 Yale 與 Université de Sherbrooke 團隊發展；與 Cooper-pair box 同一個 Hamiltonian，唯一差別是 EJ/EC；用大並聯電容提高比值'},
    {'id': 'wiki_fluxonium', 'title': 'Wikipedia: Fluxonium', 'publisher': 'Wikipedia', 'url': SRC['wiki_fluxonium'],
     'usedFor': 'JJ、電容與 superinductor 組成迴路、對 offset charge noise 不敏感；2009 年 Yale 的 Michel Devoret 團隊提出；相干時間毫秒等級、非諧性高；'
                '最常用的工作點是半個磁通量子，對磁通雜訊一階不敏感，頻率 100 MHz–1 GHz；製作複雜、難擴充；低頻通常閘比較慢；'
                '背景段：transmon 的缺點包括 low anharmonicity；有公司（D-Wave、Atlantic Quantum、Qilimanjaro）專注發展 fluxonium'},
    {'id': 'wiki_phase', 'title': 'Wikipedia: Phase qubit', 'publisher': 'Wikipedia', 'url': SRC['wiki_phase'],
     'usedFor': '電流偏壓的 JJ、在零電壓態工作；比值約 10⁶；用井中最低兩個能階當零和一；E01 ≈ ħω_p；改變偏壓電流可調能階差（優點），電流起伏造成頻率起伏、量子態失相（限制）；'
                '1985 年 John Clarke、Michel Devoret、John M. Martinis 首次以實驗展示相位的量子化，因此獲 2025 年諾貝爾物理學獎'},
]

SCENES = [
 ('量子位元家族圖鑑', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第二十八堂，量子位元家族圖鑑，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂把兩個約瑟夫森接面並聯成環，用磁通調整頻率；其實同樣是約瑟夫森接面，配上不同的電路，就能做出好幾種不同的超導量子位元。',
  '今天我們要替這個家族做一本圖鑑，比較四位成員的結構、頻率、優點和弱點。'], ['curriculum', 'neighbors', 'jj_talk_p18']),
 ('三個重點', [
  '今天有三個重點：第一，四種量子位元都靠約瑟夫森接面提供不耗損能量的非線性，差別在旁邊接了什麼，以及兩種能量的比值。',
  '第二，每一種都有拿手的地方，也都有怕的雜訊；第三，沒有一種在所有指標都最好，廠商的選擇各有考量。',
  '今天的作品是四張量子位元圖鑑卡，最後你還要設計一張自己的理想量子位元卡。'], ['curriculum', 'jj_talk_p18']),
 ('家族總覽', [
  '學程簡報有一張家族表，列出以約瑟夫森接面為核心的幾種量子位元；今天挑四種，用小名來記：電荷型、大電容型、超電感型和相位型。',
  '比較的時候看兩件事：第一，接面旁邊接了什麼；第二，約瑟夫森能量和充電能量的比值是多少。',
  '表上還有一種用超導環加三、四個接面做成的磁通量子位元，今天先不做，課後可以自己補一張卡。'], ['jj_talk_p18']),
 ('電荷型', [
  '電荷型也叫庫柏電子對盒子，結構是一個很小的超導小島，透過一個約瑟夫森接面接到外面，用小島上有沒有多一對電子來分零和一。',
  '它是最早的超導量子位元，一九九九年就有實驗第一次看到它在兩個狀態之間來回振盪；比值大約是一，頻率約五到十吉赫，非諧性很大。',
  '它最大的弱點是怕背景電荷：頻率隨背景電荷飄動的幅度叫電荷色散，電荷型的電荷色散很大，相位相干時間大約只有一到兩微秒。'],
  ['jj_talk_p18', 'jj_talk_p19', 'wiki_cpb']),
 ('大電容型', [
  '大電容型和電荷型用的是同一條能量公式，差別在旁邊並聯一塊很大的電容，把比值拉到五十到一百；它是二零零七年由耶魯大學等團隊提出的。',
  '它的頻率約四到六吉赫，非諧性大約負兩百到負三百兆赫；幾乎不怕背景電荷，結構又簡單，是現在業界的主流，上一堂的可調環也常裝在它身上。',
  '弱點是非諧性比較小，脈衝太快就可能漏到更高的能階；簡報整理的最佳實驗，能量弛豫時間大約零點一到一毫秒。'],
  ['jj_talk_p18', 'jj_talk_p20', 'wiki_transmon']),
 ('超電感型', [
  '超電感型是一個小接面並聯一個超電感，這個超電感通常是上百個比較大的接面串在一起；它是二零零九年由耶魯大學的團隊提出的。',
  '它的頻率很低，大約零點一到一吉赫，非諧性極大，能量弛豫時間可以到毫秒等級；通常停在半個磁通量子的地方，那裡對磁通雜訊一階不敏感。',
  '它也不怕背景電荷；弱點是那一大串接面讓製作變得複雜，比較難大量擴充，而且頻率低，閘通常也比較慢。'],
  ['jj_talk_p18', 'wiki_fluxonium']),
 ('相位型', [
  '相位型是一個用電流偏壓的接面，就是第二十六堂的傾斜洗衣板：偏壓電流調到接近臨界電流，相位粒子所在的山谷變淺、位障變低，再用山谷裡最低的兩個能階當零和一。',
  '它的比值遠大於一，頻率約五到十吉赫；零到一的頻率大約等於山谷裡的振動頻率，改變電流就能調整它，但電流一抖，頻率也跟著抖，量子狀態就慢慢亂掉。',
  '一九八五年，有三位科學家在這種接面裡量到量子化的能階，二零二五年因此得到諾貝爾物理學獎；不過現在相位型已經比較少用了。'],
  ['jj_talk_p16', 'jj_talk_p18', 'wiki_phase', 'neighbors']),
 ('沒有全能冠軍', [
  '最常見的誤解是：一定有一種量子位元在所有指標都最好；其實頻率、非諧性、相干時間、怕哪種雜訊、好不好製作，常常顧了這頭就顧不了那頭。',
  '所以廠商的選擇各有考量：簡報備註提到，幾家大公司用的都是大電容型的變形，也有公司專門發展超電感型。',
  '暫停影片想一想：如果你想要量子位元不怕背景電荷，又想要很大的非諧性，四張卡裡該先看哪一張？'],
  ['curriculum', 'jj_talk_p18', 'wiki_fluxonium']),
 ('實作：四張圖鑑卡', [
  '實作的時候，父子一起為四種量子位元各做一張圖鑑卡，每張卡有四格：結構、頻率、優點、弱點。',
  '爸爸念家族表上的一列，孩子把重點填進卡片，再畫一個簡單的結構圖：小島加接面、接面並聯大電容、接面並聯一串接面，或是接面接上電流源。',
  '每完成一張卡，就在卡角蓋一個解鎖成就的章；四張都蓋滿，再把卡片照比值從小排到大。'], ['curriculum', 'jj_talk_p18']),
 ('換你改造：理想量子位元', [
  '下半場換你：自己設計一張理想量子位元卡，替它取名字，畫出你想像的結構。',
  '卡上每一個優點都要寫出跟誰借的，例如向大電容型借結構簡單，向超電感型借很大的非諧性。',
  '最後誠實寫下它的代價：借來的優點會不會互相打架？它是不是比較難做，或是怕另一種雜訊？'], ['curriculum', 'jj_talk_p18']),
 ('兩小時的圖鑑卡工坊', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘一起做四張圖鑑卡，然後休息十分鐘。',
  '下半場三十分鐘，你設計理想量子位元卡；接著十分鐘交換角色，由你教爸爸操作和原理。',
  '最後五分鐘錄音總結，替你的圖鑑取個名字，再存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸量子位元家族', [
  '最後一關，請不看稿說出：四種量子位元的共同點是什麼？它們各自的結構和拿手的地方是什麼？',
  '再指出一個要注意的地方：沒有一種量子位元在所有指標都最好，每家廠商的選擇都有自己的考量。',
  '今天的作品是量子位元圖鑑卡，下一堂要看晶片怎麼做：從兩個角度斜斜地蒸鍍鋁，讓兩層金屬重疊出約瑟夫森接面；我是陳犀牛，保持好奇，我們下次見！'],
  ['curriculum', 'neighbors']),
]

VISIBLE = [
 ['量子電腦學程 第二十八堂', '量子位元\n家族圖鑑', '同一種接面，四種性格', '量子第二十八堂  ·  依課綱製作的課前教學版'],
 ['三個重點', '一種接面，四種電路',
  '01 共同點', 'JJ 提供非線性\n差在接了什麼', '→', '02 各有所長', '拿手的地方\n怕的雜訊', '→', '03 沒有全能', '沒有一種\n全部最好',
  '今天的作品：四張量子位元圖鑑卡'],
 ['家族總覽', '電荷・大電容・超電感・相位',
  '01', '看結構', '接面旁邊接了什麼',
  '02', '看比值', 'E_J／E_C 是多少',
  '03', '課後補一張', '磁通型：環＋3–4 個 JJ'],
 ['電荷型（CPB）', '庫柏電子對盒子', '圖鑑卡',
  '結構', '小島＋1 個 JJ', '頻率', '5–10 GHz', '優點', '最早、非諧性大', '弱點', '怕背景電荷',
  '相位相干時間約 1–2 μs'],
 ['大電容型（Transmon）', '電荷型＋並聯大電容',
  '電荷型', 'E_J／E_C ≈ 1', '⇄', '大電容型', 'E_J／E_C ≈ 50–100',
  '4–6 GHz  ·  α −200～−300 MHz  ·  T1 0.1–1 ms',
  '不怕背景電荷，但非諧性小'],
 ['超電感型（Fluxonium）', '1 個 JJ ∥ 超電感（上百個 JJ）',
  '頻率', '0.1–1 GHz', '非諧性', '極大', '能量弛豫', '可到毫秒等級',
  '弱點：製作複雜、閘比較慢'],
 ['相位型（Phase）', '電流偏壓的 JJ＝傾斜洗衣板',
  '電流接近 Ic → 山谷變淺 → 用最低兩個能階',
  '比值', 'E_J／E_C ≫ 1', '可調', '改電流就改頻率', '弱點', '電流一抖頻率就抖',
  '1985 年量到能階，2025 年諾貝爾獎'],
 ['沒有全能冠軍', '顧了這頭，顧不了那頭',
  '一、頻率與非諧性\n二、相干時間與雜訊\n三、好不好製作',
  '兩個願望', '不怕電荷＋非諧性大', '提示：\n比一比優點格',
  '暫停影片：兩個願望，先看哪一張卡？'],
 ['實作：四張圖鑑卡', '結構、頻率、優點、弱點',
  '念家族表的人（爸爸）', '一次念一列\n說出重點',
  '填卡的人（你）', '填四格\n畫結構圖',
  '每完成一張，蓋一個解鎖章'],
 ['換你改造：理想量子位元', '每個優點都要說跟誰借',
  '01', '取名字、畫結構', '你想像的電路',
  '02', '寫出借來的優點', '例如向超電感型借',
  '03', '誠實寫代價', '會不會互相打架'],
 ['兩小時的圖鑑卡工坊', '影片先引路，接下來比、填、設計、教',
  '00–25', '開場＋家族總覽', '25–65', '做四張圖鑑卡', '65–75', '休息十分鐘',
  '75–105', '設計理想卡', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：整理比較表'],
 ['最後一關：教爸爸量子位元家族', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '說出共同點', '都靠 JJ 的非線性',
  '02', '說出四種的特色', '結構和拿手的地方',
  '03', '指出一個注意事項', '沒有一種全部最好',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從上一堂 SQUID 接到量子位元家族', '封面版型＋陳犀牛', '想一想同一種接面能做出幾種量子位元'),
 ('三個重點：共同點是 JJ 的非線性、各有所長、沒有全能', '三步流程卡＋黃字', '認識今天的作品：四張圖鑑卡'),
 ('家族總覽：簡報 p18 家族表；看結構、看比值；磁通型課後補卡', '三點條列＋陳犀牛', '記住四個小名'),
 ('電荷型：小島＋1 JJ、比值約 1、5–10 GHz、非諧性大、怕背景電荷（電荷色散）、T2 約 1–2 μs', '面板四張卡＋黃字', '說出電荷型的優點和弱點'),
 ('大電容型：同一條公式、並聯大電容、50–100、4–6 GHz、α −200～−300 MHz、業界主流、T1 0.1–1 ms', '雙框對照＋白字＋黃字', '說出大電容型怎麼從電荷型改過來'),
 ('超電感型：1 JJ ∥ 超電感、0.1–1 GHz、非諧性極大、T1 可到毫秒、半個磁通量子、製作複雜', '三張步驟卡＋黃字', '說出超電感型的優點和弱點'),
 ('相位型：電流偏壓的 JJ、接近 Ic、最低兩個能階、可調但怕電流雜訊、1985 實驗與 2025 諾貝爾獎', '路徑一行＋三張卡＋黃字', '說出相位型可調的原因和代價'),
 ('沒有全能冠軍：指標互相拉扯、廠商選擇各有考量；暫停題', '左三行＋右欄＋黃字', '暫停想兩個願望先看哪張卡'),
 ('實作：四張圖鑑卡（結構、頻率、優點、弱點），蓋解鎖章，照比值排序', '左右比較卡＋黃字', '父子一起填卡、畫結構圖'),
 ('獨立改造：理想量子位元卡，每個優點寫出跟誰借，寫下代價', '三點條列＋陳犀牛', '設計自己的理想卡'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：共同點、四種特色、沒有全部最好；預告 Q029', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Curriculum rows (Q026, Q027, Q028, Q029), the curriculum slide deck JJ_Microwave_Readout_Talk.pptx p18–20 plus p16 '
                      '(slide text, tables and speaker notes extracted with python-pptx), the animation sources animations/js/scenes/04_potential.js, '
                      '05_washboard.js with js/core.js (index.html#potential, #washboard) and animations/transmon-3d.html (chapter 1 #capacitor tab: '
                      'capStats, fillCap) read by the producing agent on 2026-11-20, with the scene readouts recomputed in Node using the pages\' own code; '
                      'qubit facts checked against the Wikipedia articles Charge qubit, Transmon, Fluxonium and Phase qubit (raw wikitext fetched 2026-11-20).',
        not_verified=['四種量子位元的比值、頻率、非諧性取自學程簡報 p18 家族表；表上註明「數值為典型範圍，實際依設計而異」，不是某一顆晶片的量測',
                      '「最佳實驗能量弛豫時間約零點一到一毫秒」取自學程簡報 p20；維基百科 Transmon 條目另列 30–40 μs、95 μs、0.3 ms 等不同年代的數字，旁白只引用簡報的範圍',
                      '「電荷型相位相干時間約一到兩微秒」取自維基百科 Charge qubit 條目的典型值；「超電感型能量弛豫時間可到毫秒等級」取自學程簡報 p18 與維基百科 Fluxonium 條目',
                      '「幾家大公司用的都是大電容型的變形」取自學程簡報 p18 講者備註（Google、IBM）；「也有公司專門發展超電感型」取自維基百科 Fluxonium 條目；'
                      '旁白不念公司名字，也不評論各公司的現況或優劣',
                      '「二零零七年由耶魯大學等團隊提出」「二零零九年由耶魯大學的團隊提出」「一九九九年第一次看到電荷型的振盪」「一九八五年量到量子化能階、二零二五年諾貝爾物理學獎」'
                      '取自維基百科 Transmon、Fluxonium、Charge qubit、Phase qubit 條目，未另查原始論文',
                      '「零到一的頻率大約等於山谷裡的振動頻率」依維基百科 Phase qubit（E01 ≈ ħω_p）；實際相位型的最低躍遷略低於電漿頻率',
                      '磁通量子位元（簡報 p18 第三列）本集只提名稱與結構，不做圖鑑卡',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看',
                      '本集未錄影試拍；動畫段（index.html#potential 小圖、index.html#washboard 位障標籤與讀數、transmon-3d.html#capacitor 讀數與十字板粗細）待 v2 試錄確認'],
        tts_date='2026-11-18')

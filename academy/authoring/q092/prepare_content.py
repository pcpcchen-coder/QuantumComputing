"""Q092 量子感測與原子鐘 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q092/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q092', 'q092-quantum-sensing-atomic-clock', '2026-11-18'
TITLE = '量子感測與原子鐘'
TOPIC = '量子感測與原子鐘'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q092/lesson.json',
    'periph_talk': f'{REPO} slides/QC_Peripheral_Systems_Talk.pptx（第 22 頁）',
    'atoms_speech': f'{REPO} speech/離子阱與中性原子演講稿.md（原子鐘段落）',
    'bloch': f'{REPO} animations/index.html#bloch（js/scenes/01_bloch.js）',
    'bringup': f'{REPO} animations/peripherals.html#bringup（js/peripherals/10_bringup.js）',
    'electronics': f'{REPO} animations/peripherals.html#electronics（js/peripherals/06_electronics.js）',
    'atomic_clock': 'https://en.wikipedia.org/wiki/Atomic_clock',
    'second': 'https://en.wikipedia.org/wiki/Second',
    'ramsey': 'https://en.wikipedia.org/wiki/Ramsey_interferometry',
    'sensor': 'https://en.wikipedia.org/wiki/Quantum_sensor',
    'nv': 'https://en.wikipedia.org/wiki/Nitrogen-vacancy_center',
    'atom_interf': 'https://en.wikipedia.org/wiki/Atom_interferometer',
    'gps': 'https://en.wikipedia.org/wiki/Global_Positioning_System',
    'ntp': 'https://en.wikipedia.org/wiki/Network_Time_Protocol',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q092 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標、動手任務（Ramsey 干涉量頻率差）、孩子獨立改造（家裡哪些設備間接用到原子鐘）、好玩機制（科學實驗）、作品、生活技能、120 分鐘流程、驗收與常見誤解'},
    {'id': 'periph_talk', 'title': '量子電腦的周邊系統（內部技術分享簡報）第 22 頁', 'publisher': REPO, 'url': SRC['periph_talk'],
     'usedFor': '銣原子鐘／GPS 馴服 10 MHz 參考；所有 LO、DAC、ADC 由它倍頻、相位鎖定；量子閘的相位就是微波的相位，LO 沒鎖定參考相位會漂移'},
    {'id': 'atoms_speech', 'title': '離子阱與中性原子演講稿（原子鐘段落）', 'publisher': REPO, 'url': SRC['atoms_speech'],
     'usedFor': '大自然保證同一種同位素的每一顆原子完全相同，能階頻率精確——原子鐘就是用這個特性；不需逐顆調頻'},
    {'id': 'bloch', 'title': '互動動畫：超導場景 1 量子位元與 Bloch 球', 'publisher': REPO, 'url': SRC['bloch'],
     'usedFor': 'Ramsey 進動模式：赤道上的態因失諧繞 z 軸進動、向量因 T2 縮短；失諧滑桿 0–2；π/2 脈衝把態放到赤道'},
    {'id': 'bringup', 'title': '互動動畫：周邊場景 10 啟動與校準流程', 'publisher': REPO, 'url': SRC['bringup'],
     'usedFor': '十一步校準；Ramsey：兩個 π/2 之間等待 τ，條紋頻率＝失諧量 → 修正頻率；包絡給出 T₂*'},
    {'id': 'electronics', 'title': '互動動畫：周邊場景 6 室溫控制電子學', 'publisher': REPO, 'url': SRC['electronics'],
     'usedFor': '機櫃最上層「銣原子鐘／10 MHz 分配」模組與時脈分配；所有儀器鎖在同一個 10 MHz 參考'},
    {'id': 'atomic_clock', 'title': 'Atomic clock', 'publisher': 'Wikipedia', 'url': SRC['atomic_clock'],
     'usedFor': '原子鐘以原子躍遷頻率校正電子振盪器、回饋鎖定；GPS 衛星搭載原子鐘'},
    {'id': 'second', 'title': 'Second', 'publisher': 'Wikipedia', 'url': SRC['second'],
     'usedFor': '秒的定義：銫-133 基態超精細躍遷 9,192,631,770 次'},
    {'id': 'ramsey', 'title': 'Ramsey interferometry', 'publisher': 'Wikipedia', 'url': SRC['ramsey'],
     'usedFor': '兩個 π/2 脈衝夾一段自由演化，相位差轉為躍遷機率；用於原子鐘'},
    {'id': 'sensor', 'title': 'Quantum sensor', 'publisher': 'Wikipedia', 'url': SRC['sensor'],
     'usedFor': '量子感測利用量子態對環境的敏感量測時間、磁場、重力等'},
    {'id': 'nv', 'title': 'Nitrogen-vacancy center', 'publisher': 'Wikipedia', 'url': SRC['nv'],
     'usedFor': '鑽石氮空位中心可做磁場量測（磁力計）'},
    {'id': 'atom_interf', 'title': 'Atom interferometer', 'publisher': 'Wikipedia', 'url': SRC['atom_interf'],
     'usedFor': '原子干涉儀可量測重力加速度（重力儀）'},
    {'id': 'gps', 'title': 'Global Positioning System', 'publisher': 'Wikipedia', 'url': SRC['gps'],
     'usedFor': '衛星廣播時間、接收器以訊號到達時間差定位；衛星搭載原子鐘'},
    {'id': 'ntp', 'title': 'Network Time Protocol', 'publisher': 'Wikipedia', 'url': SRC['ntp'],
     'usedFor': '電腦經網路校時，最上層時間源為原子鐘或 GPS 時鐘'},
]

SCENES = [
 ('量子感測與原子鐘', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第九十二堂，量子感測與原子鐘，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂我們看到，夠大的量子電腦能破解今天常用的公開金鑰密碼，所以全世界正在換上後量子密碼。',
  '今天要回答：量子電腦還要等好幾年才夠大，可是有一種量子技術早就天天在幫你，它是什麼？量子態又怎麼拿來量時間、磁場和重力？'], ['curriculum']),
 ('三步：鐘、干涉、應用', [
  '今天分三步：先看原子鐘為什麼準，再學一種叫拉姆齊干涉的量法，最後看量子感測還能量哪些東西。',
  '今天的好玩機制是科學實驗：在動畫裡改一個頻率差，親眼看箭頭轉得更快或更慢。',
  '今天的作品是一張量子感測應用圖，把你家裡間接用到原子鐘的東西都畫上去。'], ['curriculum']),
 ('為什麼原子適合當鐘', [
  '任何鐘都需要一個穩定的擺動，再數它擺了幾次；擺鐘靠擺錘，石英錶靠石英片的振動。',
  '原子鐘用原子兩個超精細能階之間的頻率當擺動，大自然保證同一種原子每一顆都一樣，不必逐顆校準。',
  '國際上把一秒定義成：銫一百三十三原子的這個躍遷，振盪九十一億九千二百六十三萬一千七百七十次。'], ['atoms_speech', 'second', 'atomic_clock']),
 ('原子鐘怎麼運作', [
  '原子鐘裡面其實有一個普通的電子振盪器，原子負責替它打分數。',
  '先把原子都準備到零，再照上振盪器產生的微波，最後數有多少原子翻成了一。',
  '頻率完全對準時翻得最多；一旦偏了，翻的數目就變少，電路立刻把頻率修回來，就這樣一直鎖住。'], ['atomic_clock']),
 ('比一比：各自跑、共用鐘', [
  '量子電腦本身也離不開原子鐘：控制室裡幾十台儀器，全都鎖在同一個每秒振盪一千萬次的參考時脈上，常用的就是銣原子鐘。',
  '如果各台儀器各跑各的，驅動和讀取的參考相位就會慢慢漂走，每次量測都對不上。',
  '因為量子閘的相位就是微波的相位，大家必須踩同一個節拍，有時還用全球定位衛星的訊號來馴服這顆原子鐘。'], ['periph_talk', 'electronics']),
 ('拉姆齊干涉：兩個半轉', [
  '拉姆齊干涉的做法是：先用一個半轉的脈衝，把箭頭從北極轉到赤道。',
  '接著什麼都不做，靜靜等一段時間；如果微波和原子的頻率差了一點，箭頭就會在赤道上繞圈，偏出一個角度。',
  '最後再打一個半轉的脈衝，這個角度就變成量到一的機率；等得越久，角度累積越多，越小的頻率差也看得出來。'], ['ramsey', 'bloch', 'bringup']),
 ('量子感測能量什麼', [
  '量子位元最怕環境干擾，可是反過來想，這份敏感正好可以拿來量東西，這就是量子感測。',
  '磁場會讓能階的頻率偏移，例如鑽石裡一種叫氮空位中心的缺陷，就能用來量非常微弱的磁場。',
  '重力也行：讓一團冷原子像波一樣分開再合起來，干涉的結果會跟著重力改變，這叫原子干涉儀。'], ['sensor', 'nv', 'atom_interf']),
 ('原子鐘就在你身邊', [
  '你的手機定位，靠的就是衛星上的原子鐘：每顆衛星不停廣播自己的時間，手機比較訊號到達的時間差來算位置。',
  '光一奈秒大約走三十公分，時間差一微秒，位置就差大約三百公尺，所以衛星上的鐘一定要非常準。',
  '手機和電腦上網自動對時，最上游也是接到原子鐘或衛星的時間，所以你家其實早就用著量子技術。'], ['gps', 'ntp', 'atomic_clock']),
 ('科學實驗：猜出頻率差', [
  '實作的時候做科學實驗：打開布洛赫球動畫，選拉姆齊進動，爸爸偷偷把失諧滑桿拉到某個位置。',
  '你不看數字，只數箭頭在動畫重來之前繞了幾圈；在這個動畫裡，圈數除以三，差不多就是滑桿上的失諧。',
  '玩幾回合，記下猜的和真正的數字，再想一想：要分辨兩個很接近的頻率差，為什麼等得越久越容易？'], ['curriculum', 'bloch']),
 ('換你改造：家裡的原子鐘', [
  '下半場換你改造：在家裡走一圈，找出哪些東西會自己對時，例如手機、電腦和電視盒。',
  '再找出會定位的東西，例如汽車導航和運動手錶，它們都在接收衛星上原子鐘送來的時間。',
  '最後畫成量子感測應用圖：中間是原子鐘，用線連到每一樣東西，旁邊再加上量磁場和量重力兩個例子。'], ['curriculum', 'gps', 'ntp']),
 ('兩小時的感測實驗室', [
  '兩小時的安排是：開場十分鐘，認識原子鐘和量子感測十五分鐘，接著四十分鐘在動畫裡做拉姆齊實驗、玩猜頻率差，然後休息十分鐘。',
  '下半場三十分鐘在家裡找原子鐘、畫應用圖，接著十分鐘交換角色，由你教爸爸原子鐘和拉姆齊干涉的原理。',
  '最後五分鐘錄音總結，替應用圖取名字，存一個版本；精密量測改變生活，我們每天準時、不迷路，背後都是這些看不見的鐘。'], ['curriculum']),
 ('最後一關：教爸爸量時間', [
  '最後一關，請不看稿說出：原子鐘為什麼準？拉姆齊干涉怎麼把很小的頻率差量出來？',
  '再指出一個常見誤解：很多人以為量子技術都還在實驗室，其實原子鐘和量子感測早就有商用產品，比量子計算更早落地。',
  '今天的作品是量子感測應用圖，下一堂我們來畫量子電腦的產業地圖，看各家公司走哪條路、要經過哪幾個階段；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum']),
]

VISIBLE = [
 ['量子電腦學程 第九十二堂', '量子感測\n與原子鐘', '用量子態量時間', '量子第九十二堂  ·  依課綱製作的課前教學版'],
 ['三步：鐘、干涉、應用', '今天的好玩機制：科學實驗',
  '01 原子鐘', '原子的頻率\n每顆都一樣', '→', '02 Ramsey', '兩個半轉\n量頻率差', '→', '03 感測應用', '時間、磁場\n還有重力',
  '今天的作品：量子感測應用圖'],
 ['為什麼原子適合當鐘', '大自然保證每顆原子都一樣',
  '01', '鐘＝擺動＋計數', '擺錘、石英、原子',
  '02', '兩個超精細能階', '頻率每顆都相同',
  '03', '一秒的國際定義', '¹³³Cs 振盪約 92 億次'],
 ['原子鐘怎麼運作', '原子替振盪器打分數', '一輪校正',
  '第一步', '原子都到 |0⟩', '第二步', '照振盪器的微波', '第三步', '數翻成 |1⟩', '第四步', '偏了就修頻率',
  '翻得最多＝頻率對準'],
 ['比一比：各自跑、共用鐘', '量子電腦的幾十台儀器',
  '各自的時脈', '參考相位慢慢漂走', '→', '鎖在銣原子鐘', '10 MHz 參考',
  '量子閘的相位就是微波的相位',
  '所有儀器踩同一個節拍'],
 ['Ramsey 干涉', '把頻率差變成機率',
  '01 先轉 π/2', '箭頭轉到赤道', '02 等待 τ', '頻率差讓箭頭繞圈', '03 再轉 π/2', '角度變成 P(1)',
  '等得越久，越小的差也看得出'],
 ['量子感測能量什麼', '怕干擾，所以很靈敏',
  '時間  →  磁場  →  重力',
  '時間與頻率', '原子鐘、校時', '磁場', '鑽石 NV 中心', '重力', '原子干涉儀',
  '量子位元的弱點，感測的優點'],
 ['原子鐘就在你身邊', '看不見，卻天天在用',
  '一、衛星定位：帶原子鐘\n二、網路校時：自動對時\n三、量子電腦：共用時脈',
  '要多準', '光 1 ns 走 30 cm', '差 1 μs\n位置差約 300 m',
  '定位其實是在量時間'],
 ['科學實驗：猜出頻率差', '只看箭頭繞幾圈',
  '出題者（爸爸）', '偷偷拉失諧滑桿\n不讓你看數字',
  '實驗者（你）', '數箭頭繞幾圈\n圈數÷3≈失諧',
  '繞得越快，頻率差越大'],
 ['換你改造：家裡的原子鐘', '畫一張量子感測應用圖',
  '01', '找會自動對時的', '手機、電腦、電視盒',
  '02', '找會定位的', '汽車導航、運動手錶',
  '03', '畫線連到源頭', '加上磁場、重力例子'],
 ['兩小時的感測實驗室', '影片先引路，接下來看、量、找、畫',
  '00–25', '開場＋原子鐘與量子感測', '25–65', 'Ramsey＋猜頻率差', '65–75', '休息十分鐘',
  '75–105', '找家裡的原子鐘', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：精密量測改變生活'],
 ['最後一關：教爸爸量時間', '暫停影片：不看稿說一次，再指出一個誤解',
  '01', '說出原子鐘為什麼準', '每顆原子頻率都一樣',
  '02', '說出 Ramsey 原理', '兩個半轉夾一段等待',
  '03', '指出一個常見誤解', '感測比計算更早落地',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、天天在用的量子技術', '封面版型＋陳犀牛', '回想上一堂的後量子密碼'),
 ('三步：鐘、干涉、應用', '三步流程卡＋黃字', '認識科學實驗與今天的作品'),
 ('為什麼原子適合當鐘：擺動＋計數、秒的定義', '三點條列＋陳犀牛', '說出原子鐘為什麼準'),
 ('原子鐘怎麼運作：回饋鎖定', '面板四張卡＋黃字', '照順序說出四步'),
 ('比較：各跑各的 vs 鎖在銣原子鐘', '雙框對照＋白字＋黃字', '說出量子電腦為什麼要共用時脈'),
 ('Ramsey 干涉：兩個 π/2 夾等待', '三張步驟卡＋黃字', '說出等待時為什麼會偏出角度'),
 ('量子感測：時間、磁場、重力', '路徑一行＋三張卡＋黃字', '各舉一個例子'),
 ('原子鐘在身邊：定位與校時', '左三行＋右欄＋黃字', '算一微秒差多少公尺'),
 ('實驗：猜出頻率差', '左右比較卡＋黃字', '出題者與實驗者'),
 ('獨立改造：家裡的原子鐘', '三點條列＋陳犀牛', '找、分類、畫應用圖'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：原子鐘、Ramsey、常見誤解；預告 Q093', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Repo slides (QC_Peripheral_Systems_Talk.pptx p22), speech notes and animation source (js/scenes/01_bloch.js, '
                      'js/peripherals/06_electronics.js, 10_bringup.js) read by the producing agent; general facts cross-checked against Wikipedia '
                      '(Atomic clock, Second, Ramsey interferometry, Quantum sensor, Nitrogen-vacancy center, Atom interferometer, GPS, NTP). '
                      'Turns-per-cycle in the Bloch Ramsey mode computed from the scene code (angle = 1.5·Δ·t, loop restarts at t = 12).',
        not_verified=['課綱列的「◆ 新簡報：量子感測」「★ Ramsey 干涉感測場景」尚未製作；本集用現有 #bloch 的 Ramsey 進動模式與周邊場景代替',
                      '#bloch 的 Ramsey 進動只畫赤道上的進動與縮短，不含第二個 π/2 脈衝；「角度變成機率」是用旁白與周邊場景 10 的條紋圖說明',
                      '「圈數除以三約等於失諧」只適用於本動畫的相對單位（每輪 12 單位時間、角速度 1.5Δ），不是物理公式',
                      '家用設備（電視盒、運動手錶）是否接 GPS 或網路校時依型號而定，作業時請孩子自己查證',
                      '量子感測商用產品的具體廠牌、型號本集未列出',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

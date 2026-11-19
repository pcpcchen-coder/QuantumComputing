"""Q024 JJ 是非線性電感 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q024/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q024', 'q024-jj-nonlinear-inductor', '2026-11-18'
TITLE = 'JJ 是非線性電感'
TOPIC = 'JJ 是非線性電感'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q024/lesson.json',
    'neighbors': f'{REPO} academy/lessons/Q023/brief.md、academy/lessons/Q025/brief.md',
    'jj_talk_p14': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p14（含講者備註）',
    'transmon_p4_5': f'{REPO} slides/transmon.pptx p4–5（含講者備註）',
    'transmon_p6': f'{REPO} slides/transmon.pptx p6（含講者備註）',
    'transmon_p7': f'{REPO} slides/transmon.pptx p7（含講者備註）',
    'transmon_p8': f'{REPO} slides/transmon.pptx p8（含講者備註）',
    'ep049_p11_12': f'{REPO} slides/output/ep049-superconducting-qubit.pptx p11–12（含講者備註）',
    'notes': f'{REPO} notes/transmon-josephson-inductance.md',
    'tr_junction': f'{REPO} animations/transmon-3d.html#junction',
    'tr_potential': f'{REPO} animations/transmon-3d.html#potential',
    'lc_s5': f'{REPO} animations/lc-vs-jj.html#s5',
    'wiki_je': 'https://en.wikipedia.org/wiki/Josephson_effect',
    'wiki_pendulum': 'https://en.wikipedia.org/wiki/Pendulum_(mechanics)',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q024 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（知道 JJ 的電感會隨電流改變，這個非線性是做出量子位元的關鍵）、動手任務（比較單擺小振幅與大振幅的週期，對照 JJ 電感隨電流變大）、'
                '孩子獨立改造（用 transmon-3d 場景找出能階間距開始變小的地方）、好玩機制（科學實驗：單擺大小振幅）、作品（單擺週期紀錄）、'
                '家長課前準備（細繩、重物、量角器；transmon-3d.html；notes/transmon-josephson-inductance.md）、120 分鐘流程、'
                '驗收與常見誤解（JJ 沒有電阻損耗，所以是「無耗散」的非線性元件）、生活技能支線（注意「近似」什麼時候會失效）'},
    {'id': 'neighbors', 'title': '量子電腦學程 Q023、Q025 課綱', 'publisher': REPO, 'url': SRC['neighbors'],
     'usedFor': '上一堂：約瑟夫森接面：超導三明治（SIS 結構、Cooper pair 穿隧、DC／AC Josephson 效應）；'
                '下一堂：E_J 與 E_C：兩個能量尺度（E_J／E_C 比值決定量子位元的性格）'},
    {'id': 'jj_talk_p14', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p14：JJ 是一個「非線性電感」', 'publisher': REPO, 'url': SRC['jj_talk_p14'],
     'usedFor': '由 I = Ic sin φ 與 V = (Φ0/2π) dφ/dt 得 V = LJ · dI/dt、LJ(φ) = Φ0 / (2π Ic cos φ)；小電流 LJ0 = Φ0/(2π Ic)，Ic = 30 nA → LJ0 ≈ 11 nH；'
                '電感隨電流（相位）改變 → 非線性；無耗散：不像電阻會發熱；φ → π/2 時發散；備註「JJ 是一個無耗散的非線性電感」'},
    {'id': 'transmon_p4_5', 'title': 'Transmon 筆記簡報 p4「從約瑟夫森方程式推出電感」、p5「JJ 電感隨電流變大」', 'publisher': REPO, 'url': SRC['transmon_p4_5'],
     'usedFor': 'p4：dI/dt = Ic cos φ · dφ/dt，V = LJ · dI/dt「形式與電感完全相同」，LJ0 ≈ 10.9 nH（Ic ≈ 30 nA）；'
                'p5：I ≪ Ic「LJ ≈ LJ0，行為像普通電感」、I → Ic「LJ → ∞，超過後跳到有電壓的耗散態」、π/2 < φ < π「LJ < 0」；'
                '備註 L_J = L_J0 / sqrt(1 − (I/Ic)²)、「量子位元運作時電流遠小於 Ic，所以落在曲線左邊平坦處，但仍帶有一點彎曲」'},
    {'id': 'transmon_p6', 'title': 'Transmon 筆記簡報 p6：小振幅像電感，大振幅變軟', 'publisher': REPO, 'url': SRC['transmon_p6'],
     'usedFor': 'U = EJ(1 − cos φ) ≈ EJφ²/2 − EJφ⁴/24；二次項 → 等效電感 LJ0；能量存在相位耦合裡，不是磁場（動感電感）；'
                '四次項 → 非線性，振幅越大，回復力比拋物線弱，頻率變低；備註「大振幅時位能井比拋物線平坦」'},
    {'id': 'transmon_p7', 'title': 'Transmon 筆記簡報 p7：為什麼要用 JJ 取代線性電感', 'publisher': REPO, 'url': SRC['transmon_p7'],
     'usedFor': '非線性 α ≈ −283 MHz（能階不等距）；無耗散 0 Ω（唯一同時非線性又不耗能的元件；二極體、電晶體會耗能而破壞相干）；'
                '體積極小 ≈10 nH / 0.02 μm²（同樣電感若用線圈要毫米級繞線）'},
    {'id': 'transmon_p8', 'title': 'Transmon 筆記簡報 p8：直覺圖像：量子單擺', 'publisher': REPO, 'url': SRC['transmon_p8'],
     'usedFor': 'θ ↔ φ，U = −mgl cos θ 與 −E_J cos φ 同形；「幾乎是簡諧振盪，但頻率會隨振幅略降。這一點點不簡諧，就是量子位元的關鍵。」'},
    {'id': 'ep049_p11_12', 'title': '《量子超級英雄》#049 報告簡報 p11–12：JJ 登場、泰勒展開：多出來的四次方項', 'publisher': REPO, 'url': SRC['ep049_p11_12'],
     'usedFor': 'p11：把電感 L 換成 JJ，電感能量原本是平方函數，現在變成 cos 函數；p12：−EJ cos φ ≈ −EJ + (EJ/2)φ² − (EJ/24)φ⁴，'
                '二次方項跟 LC 一樣（只留到這裡能階還是等距），四次方項是 JJ 獨有、讓能階變得不等距；備註「往上 JJ 的位能井比拋物線寬，能階就會愈來愈密」'},
    {'id': 'notes', 'title': '筆記：Transmon——約瑟夫森電感、電路結構與量子位元機制', 'publisher': REPO, 'url': SRC['notes'],
     'usedFor': 'L_J(I) = L_J0 / √(1 − (I/I_c)²)，電流越接近 I_c 電感越大；I = I_c 時 L_J → ∞，超過後跳到有電壓的耗散態；'
                'JJ 是目前已知唯一同時「非線性」又「無耗散」的電路元件（二極體、電晶體會耗能）；約 100 nm × 200 nm 的接面就有約 10 nH，線圈要毫米等級；'
                '數值範例 E_J/h = 15 GHz → I_c ≈ 30 nA、L_J0 ≈ 10.9 nH；E₁ − E₀ = 5.214 GHz、E₂ − E₁ = 4.931 GHz、α = −283 MHz，線性 LC 5.477 GHz；'
                '量子單擺：振幅越大頻率越低，這一點點不簡諧就是量子位元的關鍵'},
    {'id': 'tr_junction', 'title': 'Transmon 3D 第 2 章：約瑟夫森結：非線性電感的本體', 'publisher': REPO, 'url': SRC['tr_junction'],
     'usedFor': '動畫段：下層 Al、紫色 AlOx 絕緣層、上層 Al，青金兩色庫柏對沿路徑穿過絕緣層（速度 ∝ sin φ）；相位差滑桿 φ（0–180，預設 35）；'
                '讀數「相位差 φ」「電流 I / I_c」「電感 L_J / L_J0」（= 1/cos φ）'},
    {'id': 'tr_potential', 'title': 'Transmon 3D 第 3 章：cos 位能井：能階不再等距', 'publisher': REPO, 'url': SRC['tr_potential'],
     'usedFor': '動畫段與孩子改造：銅色 −E_J cos φ 位能井、灰色拋物線、六條能階與間距標籤 5.21／4.93／4.62／4.25／3.91 GHz、同形的單擺；'
                '「有 JJ（transmon）」「沒有 JJ（線性 LC）」切換（線性 LC 每階 5.48 GHz）；讀數非諧性 α「−283 MHz」／「0（等距）」'},
    {'id': 'lc_s5', 'title': 'LC 與約瑟夫森接面 圖解第 5 步：泰勒展開：多出來的四次項', 'publisher': REPO, 'url': SRC['lc_s5'],
     'usedFor': '動畫段：1 − cos φ（真正的 JJ，橘色）、φ²/2（只留二次項，藍色虛線）、φ²/2 − φ⁴/24（灰色點線），陰影「四次項造成的差距」'},
    {'id': 'wiki_je', 'title': 'Wikipedia: Josephson effect（Josephson inductance 一節）', 'publisher': 'Wikipedia', 'url': SRC['wiki_je'],
     'usedFor': 'V = Φ0/(2π Ic cos φ) · ∂I/∂t = L(φ) ∂I/∂t；L(φ) = L_J / cos φ；行為像電感但沒有相關的磁場，來自載子（庫柏對）的動能，也叫動感電感（kinetic inductance）'},
    {'id': 'wiki_pendulum', 'title': 'Wikipedia: Pendulum (mechanics)', 'publisher': 'Wikipedia', 'url': SRC['wiki_pendulum'],
     'usedFor': '小角度近似 sin θ ≈ θ；Arbitrary-amplitude period：大振幅週期比小角度近似長；AGM 公式 T = 2π√(ℓ/g) / M(1, cos(θ₀/2))'
                '（製作代理以此實算：一公尺擺十次來回 10° 約 20.10 秒、60° 約 21.53 秒、90° 週期約多 18%）'},
]

SCENES = [
 ('JJ 是非線性電感', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第二十四堂，約瑟夫森接面是非線性電感，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂拆開了約瑟夫森接面這個超導三明治，看到穿過去的電流由兩邊的相位差決定，最大就是臨界電流。',
  '今天換個角度看同一個接面：在電路裡它的作用像一個電感，而且這個電感會隨電流改變，這正是做出量子位元的關鍵。'], ['curriculum', 'neighbors', 'jj_talk_p14']),
 ('三個重點', [
  '今天有三個重點：第一，約瑟夫森接面在電路裡就像一個電感，這可以從上一堂的兩個效應推出來。',
  '第二，它的電感會隨電流改變，電流越接近臨界電流，電感就越大；第三，它沒有電阻，不會發熱，是無耗散的非線性元件。',
  '今天的作品是一張單擺週期紀錄，小角度和大角度各量一次，看看近似什麼時候會失效。'], ['curriculum', 'jj_talk_p14']),
 ('接面為什麼像電感', [
  '先回想電感：電感讓電流不容易變快或變慢，電流變化得越快，電感兩端的電壓就越大。',
  '約瑟夫森接面也是這樣：電流跟著相位差變，相位差又跟著電壓轉，兩件事合起來，電壓正好和電流變化的快慢成正比。',
  '這個比例就是它的電感；臨界電流是三十奈安培的接面，電流很小時，電感大約是十一奈亨。'], ['jj_talk_p14', 'transmon_p4_5', 'wiki_je', 'notes']),
 ('電感隨電流變大', [
  '關鍵在於，這個電感不是固定的：它等於小電流時的電感，再除以相位差的餘弦。',
  '電流只有臨界電流的一半時，電感大約多出一成五；電流到了臨界電流的九成八，電感變成大約五倍。',
  '電流一碰到臨界電流，電感就變成無限大；再往上推，接面就跳到有電壓的狀態，開始耗能。'], ['jj_talk_p14', 'transmon_p4_5', 'notes', 'wiki_je']),
 ('什麼叫非線性', [
  '這就是非線性的意思：普通線圈的電感是固定的，不管電流大小，它對電流變化的反應都一樣。',
  '約瑟夫森接面的電感卻跟著電流走，電流小時幾乎不變，越接近臨界電流變得越快；反應會隨大小改變的元件，就叫非線性元件。',
  '電流和相位差的關係是正弦曲線，小的時候幾乎是直線；量子位元工作時電流遠小於臨界電流，正落在這一段，只帶一點點彎曲，但這一點點就夠了。'],
  ['transmon_p4_5', 'jj_talk_p14', 'transmon_p8']),
 ('位能變軟，梯子變擠', [
  '從能量來看，接面的位能是一條餘弦形的山谷；把它展開，第一項和普通電感一樣是拋物線，接著多出一個負的四次方項。',
  '這個四次方項讓山谷往上越來越比拋物線寬鬆，振幅一大，拉回來的力就比拋物線弱，振盪就變慢。',
  '所以能階不再等距：在學程動畫的參數裡，零到一是五點二一吉赫，一到二只剩四點九三吉赫，這個差距叫做非諧性。'],
  ['transmon_p6', 'ep049_p11_12', 'tr_potential', 'notes']),
 ('無耗散，又非常小', [
  '非線性的元件其實很多，例如二極體和電晶體，但它們工作時會耗能發熱，而熱會破壞脆弱的量子狀態。',
  '約瑟夫森接面在超導狀態下沒有電阻，電流流過不會發熱，它是目前已知唯一同時非線性又不耗能的電路元件。',
  '它還非常小：零點零二平方微米的接面就有大約十奈亨，同樣的電感改用線圈來繞，得要毫米大小。'], ['transmon_p7', 'notes', 'jj_talk_p14']),
 ('不是線圈那種電感', [
  '最常見的誤解是：非線性的元件一定會耗能，或者以為接面的電感和線圈一樣是固定的。',
  '其實接面沒有電阻損耗，是無耗散的非線性元件；它也不像線圈那樣把能量存在磁場裡，所以這種電感另有一個名字，叫動感電感。',
  '暫停影片想一想：如果把接面的電流推到超過臨界電流，它還是無耗散的電感嗎？'], ['curriculum', 'transmon_p6', 'wiki_je', 'transmon_p4_5']),
 ('實作：單擺大小角度', [
  '實作的時候，父子一起做單擺：一公尺的細繩綁一個重物，用量角器量好放手的角度。',
  '先拉開十度放手，數十次來回再按停碼錶；再拉開六十度，一樣數十次，把兩個時間都記下來。',
  '用一公尺的擺來算，十度大約二十點一秒，六十度大約二十一點五秒，大角度明顯比較慢，就像電流大時接面的電感變大，電路也振得比較慢。'],
  ['curriculum', 'wiki_pendulum', 'transmon_p8']),
 ('換你改造：找出間距變小處', [
  '下半場換你：打開學程的超導量子位元三維動畫，到位能井那一章，找出能階間距從哪裡開始變小。',
  '看每兩階之間標的間距，從下往上一格一格比；再切換到沒有約瑟夫森接面的線性電路，比較每一格都一樣的情形。',
  '最後在紀錄上寫一句：近似在哪裡失效？單擺是角度變大，接面是電流變大，能階則是越往上越明顯。'], ['curriculum', 'tr_potential']),
 ('兩小時的非線性實驗室', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘一起做單擺，量小角度和大角度的週期，然後休息十分鐘。',
  '下半場三十分鐘，你在動畫裡找出能階間距開始變小的地方；接著十分鐘交換角色，由你教爸爸操作和原理。',
  '最後五分鐘錄音總結，替你的單擺週期紀錄取個名字，再存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸非線性電感', [
  '最後一關，請不看稿說出：為什麼約瑟夫森接面像一個電感？它的電感怎麼隨電流改變？',
  '再指出一個要注意的地方：接面沒有電阻損耗，是無耗散的非線性元件，但電流超過臨界電流，它就會開始耗能。',
  '今天的作品是單擺週期紀錄，下一堂要看兩個能量尺度：約瑟夫森能量和充電能量的比值，怎麼決定量子位元的性格；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'neighbors']),
]

VISIBLE = [
 ['量子電腦學程 第二十四堂', '約瑟夫森接面\n是非線性電感', '電感會隨電流改變，這就是關鍵', '量子第二十四堂  ·  依課綱製作的課前教學版'],
 ['三個重點', '從電感到非線性',
  '01 像電感', '兩個效應\n合起來推出', '→', '02 會變的電感', '電流越大\n電感越大', '→', '03 無耗散', '沒有電阻\n不會發熱',
  '今天的作品：單擺週期紀錄'],
 ['接面為什麼像電感', 'V = L_J · dI/dt',
  '01', '電感的定義', '電流變得越快，電壓越大',
  '02', '接面也一樣', 'I 跟著 φ，φ 跟著 V',
  '03', '小電流時', 'Ic = 30 nA → 約 11 nH'],
 ['電感隨電流變大', 'L_J = L_J0 / cos φ', '四個讀數',
  '第一點', '小電流 ≈ L_J0', '第二點', '0.5 Ic → 1.15 倍', '第三點', '0.98 Ic → 約 5 倍', '第四點', 'Ic → 無限大',
  '越接近 Ic，電感變大得越快'],
 ['什麼叫非線性', '反應會隨大小改變',
  '普通線圈', 'L 固定不變', '⇄', '約瑟夫森接面', 'L 跟著電流變',
  'I = Ic sin φ：小電流時幾乎是直線',
  '量子位元只用一點點彎曲'],
 ['位能變軟，梯子變擠', '−E_J cos φ ≈ φ² 項 − φ⁴ 項',
  '二次方項', '像普通電感', '四次方項', '大振幅變軟', '能階間距', '5.21 → 4.93 GHz',
  '差距叫非諧性，約 −283 MHz'],
 ['無耗散，又非常小', '同時非線性又不耗能',
  '非線性 ＋ 無耗散 ＋ 很小  →  量子位元的心臟',
  '非線性', '能階不等距', '無耗散', '0 Ω，不發熱', '很小', '約 10 nH／0.02 μm²',
  '二極體、電晶體會耗能'],
 ['不是線圈那種電感', '沒有電阻，也不靠磁場',
  '一、沒有電阻損耗\n二、電感跟著電流變\n三、超過 Ic 才耗能',
  '能量不在磁場', '叫動感電感', '和線圈的\n電感不同',
  '暫停影片：超過 Ic 還無耗散嗎？'],
 ['實作：單擺大小角度', '一公尺細繩，十度對六十度',
  '放手的人（爸爸）', '量好角度\n十度、六十度',
  '計時的人（你）', '數十次來回\n記下秒數',
  '大角度比較慢：約 20.1 秒對 21.5 秒'],
 ['換你改造：找出間距變小處', '用 transmon-3d 位能井那一章',
  '01', '打開位能井', 'transmon-3d.html#potential',
  '02', '一格一格比', '5.21、4.93、4.62 GHz…',
  '03', '寫下近似失效處', '大角度、大電流、高能階'],
 ['兩小時的非線性實驗室', '影片先引路，接下來量、比、找、教',
  '00–25', '開場＋非線性電感', '25–65', '量單擺週期', '65–75', '休息十分鐘',
  '75–105', '找能階間距', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：注意近似何時失效'],
 ['最後一關：教爸爸非線性電感', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '說出為什麼像電感', '電壓 ∝ 電流變化的快慢',
  '02', '說出怎麼隨電流變', '越接近 Ic，電感越大',
  '03', '指出一個注意事項', '無耗散，但超過 Ic 會耗能',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從上一堂超導三明治接到「接面像電感」', '封面版型＋陳犀牛', '想一想電感會不會變'),
 ('三個重點：像電感、電感隨電流變、無耗散', '三步流程卡＋黃字', '認識今天的作品'),
 ('接面為什麼像電感：V = L_J dI/dt、Ic = 30 nA → 約 11 nH', '三點條列＋陳犀牛', '說出電感的定義'),
 ('電感隨電流變大：L_J = L_J0 / cos φ、0.5 Ic → 1.15 倍、0.98 Ic → 約 5 倍、Ic → 無限大', '面板四張卡＋黃字', '說出越接近 Ic 電感越大'),
 ('什麼叫非線性：線圈 L 固定、接面 L 跟著電流變；小電流時近似直線', '雙框對照＋白字＋黃字', '說出非線性的意思'),
 ('位能變軟：二次方項與四次方項、能階 5.21 → 4.93 GHz、非諧性約 −283 MHz', '三張步驟卡＋黃字', '說出四次方項讓梯子變擠'),
 ('無耗散又很小：0 Ω、二極體電晶體會耗能、約 10 nH／0.02 μm²', '路徑一行＋三張卡＋黃字', '說出為什麼選接面'),
 ('不是線圈那種電感：沒有電阻損耗、動感電感、超過 Ic 才耗能', '左三行＋右欄＋黃字', '暫停想超過 Ic 還無耗散嗎'),
 ('實作：一公尺單擺，十度對六十度，各數十次來回', '左右比較卡＋黃字', '父子一起量週期、記秒數'),
 ('獨立改造：transmon-3d 位能井，找出能階間距開始變小處', '三點條列＋陳犀牛', '一格一格比間距、寫近似失效處'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：為什麼像電感、怎麼隨電流變、注意事項；預告 Q025', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Curriculum rows (Q023, Q024, Q025), the curriculum slide decks JJ_Microwave_Readout_Talk.pptx p14, transmon.pptx p3–8 and '
                      'ep049-superconducting-qubit.pptx p11–12 (slide text and speaker notes extracted with python-pptx), '
                      'notes/transmon-josephson-inductance.md, animations/transmon-3d.html (chapters junction and potential) and '
                      'animations/lc-vs-jj.html#s5 read by the producing agent on 2026-11-18; the Josephson inductance formula checked against the '
                      'Wikipedia article Josephson effect and the large-amplitude pendulum period against Pendulum (mechanics) (raw wikitext fetched '
                      '2026-11-18); inductance ratios, transmon levels and pendulum periods recomputed by the producing agent with pendulum_check.py '
                      'and with the level routine copied from transmon-3d.html.',
        not_verified=['「臨界電流三十奈安培時小電流電感約十一奈亨」取自學程簡報 JJ_Microwave_Readout_Talk p14 與 transmon p4 的範例參數（Φ0/2πIc = 10.97 nH），不是某一顆晶片的量測值',
                      '「五點二一、四點九三吉赫」「非諧性約負兩百八十三兆赫」是學程動畫與筆記的範例參數（E_J/h = 15 GHz、E_C/h = 250 MHz）的數值解，真實晶片依設計而不同',
                      '「零點零二平方微米約十奈亨」「線圈要毫米大小」取自 transmon p7 與筆記的概略比較，本集沒有另外計算線圈尺寸',
                      '「目前已知唯一同時非線性又不耗能的電路元件」是學程筆記與簡報 p7 的說法；本集沒有另找文獻逐一比對其他超導元件',
                      '單擺週期（十度約二十點一秒、六十度約二十一點五秒，十次來回）是理想單擺以 g = 9.81 m/s² 的計算值；家中細繩有質量、擺錘不是質點、'
                      '大角度時擺幅會因空氣阻力慢慢變小，量到的時間會和計算差一些',
                      '「大角度單擺變慢」和「接面電感變大、電路變慢」是同一種「近似失效、振盪變軟」的類比，不是一格一格對應的物理量',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看',
                      '本集未錄影試拍；動畫段（transmon-3d.html#junction 滑桿逐步設值、#potential 按鈕切換後能階移動的時間、lc-vs-jj.html#s5 版面是否一頁看完）待 v2 試錄確認'],
        tts_date='2026-11-18')

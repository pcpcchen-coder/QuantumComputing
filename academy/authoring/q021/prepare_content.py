"""Q021 彈簧、單擺與 LC 電路 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q021/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q021', 'q021-spring-pendulum-lc', '2026-11-18'
TITLE = '彈簧、單擺與 LC 電路'
TOPIC = '彈簧、單擺與 LC 電路'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q021/lesson.json',
    'neighbors': f'{REPO} academy/lessons/Q020/brief.md、academy/lessons/Q022/brief.md',
    'ep049_p6': f'{REPO} slides/output/ep049-superconducting-qubit.pptx p6（含講者備註）',
    'ep049_p8': f'{REPO} slides/output/ep049-superconducting-qubit.pptx p8（含講者備註）',
    'transmon_p8': f'{REPO} slides/transmon.pptx p8（含講者備註）',
    'jj_talk_p8': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p8',
    'wiki_shm': 'https://en.wikipedia.org/wiki/Simple_harmonic_motion',
    'wiki_pendulum': 'https://en.wikipedia.org/wiki/Pendulum_(mechanics)',
    'wiki_lc': 'https://en.wikipedia.org/wiki/LC_circuit',
    'wiki_analogy': 'https://en.wikipedia.org/wiki/Mechanical%E2%80%93electrical_analogies',
    'wiki_ho': 'https://en.wikipedia.org/wiki/Harmonic_oscillator',
    'lc_s1s2': f'{REPO} animations/lc-vs-jj.html#s1、#s2',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q021 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（把力學振盪和電磁振盪對應起來：質量↔電感、彈簧↔電容）、動手任務（量彈簧和單擺的週期，填出力學與 LC 的對照表）、'
                '孩子獨立改造（改變質量或擺長，預測週期變化並驗證）、好玩機制（科學實驗：彈簧振盪計時）、作品（類比對照表）、家長課前準備（彈簧、重物、細繩、碼錶）、'
                '120 分鐘流程、驗收與常見誤解（類比只在小振幅時成立；大振幅單擺就不再是簡諧運動）、生活技能支線（用類比把新知識接到舊知識）'},
    {'id': 'neighbors', 'title': '量子電腦學程 Q020、Q022 課綱', 'publisher': REPO, 'url': SRC['neighbors'],
     'usedFor': '上一堂：磁通量子化（超導環裡的磁通只能是 Φ₀ 的整數倍）；'
                '下一堂：量子諧振子——等距的梯子（LC 電路的能階等距，所以無法只挑出兩個能階當量子位元）'},
    {'id': 'ep049_p6', 'title': '《量子超級英雄》#049 報告簡報 p6：繞個遠路——從彈簧到哈密頓量', 'publisher': REPO, 'url': SRC['ep049_p6'],
     'usedFor': '彈簧拉著一個質量振盪就是諧振子；力學能守恆，動能＋位能為定值，一高一低互相交換'},
    {'id': 'ep049_p8', 'title': '《量子超級英雄》#049 報告簡報 p8：力學振盪 ↔ 電磁振盪——LC 電路', 'publisher': REPO, 'url': SRC['ep049_p8'],
     'usedFor': '對照表：彈簧–質量系統（動能 ⇄ 位能、質量來回運動）↔ LC 電路（電容能 ⇄ 電感能、電荷來回流動）；'
                '超導 LC 電路就能成為一個會出現量子現象的諧振子'},
    {'id': 'transmon_p8', 'title': 'Transmon 筆記簡報 p8：直覺圖像——量子單擺', 'publisher': REPO, 'url': SRC['transmon_p8'],
     'usedFor': '單擺位能 U = −mgl cos θ（回復力來自重力）；幾乎是簡諧振盪，但頻率會隨振幅略降（大振幅不再簡諧）'},
    {'id': 'jj_talk_p8', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p8', 'publisher': REPO, 'url': SRC['jj_talk_p8'],
     'usedFor': '量子位元 f01 ≈ 5 GHz（與 1 nH、1 pF 算出的 5.03 GHz 比較）'},
    {'id': 'wiki_shm', 'title': 'Wikipedia: Simple harmonic motion', 'publisher': 'Wikipedia', 'url': SRC['wiki_shm'],
     'usedFor': '彈簧週期 T = 2π√(m/k)；簡諧運動是等時的（週期與振幅無關）；單擺小振幅時週期與振幅、質量無關'},
    {'id': 'wiki_pendulum', 'title': 'Wikipedia: Pendulum (mechanics)', 'publisher': 'Wikipedia', 'url': SRC['wiki_pendulum'],
     'usedFor': '回復力來自重力、方程式含 sin θ；小角度近似 sin θ ≈ θ；T₀ = 2π√(ℓ/g)，小角度下與振幅無關（等時性）；'
                '1 公尺的擺 T₀ ≈ 2 秒（ℓ ≈ T₀²/4 的經驗式）；任意振幅的週期（算術幾何平均公式），振幅越大週期越久'},
    {'id': 'wiki_lc', 'title': 'Wikipedia: LC circuit', 'publisher': 'Wikipedia', 'url': SRC['wiki_lc'],
     'usedFor': '電容在電場、電感在磁場儲存能量；充好電的電容接上電感，電流流過電感，電感抗拒電流改變，把電容反向充電，週而復始；'
                '電荷來回流動、能量在電容與電感間來回，像單擺；ω₀ = 1/√(LC)；有電阻時振盪會漸漸停止'},
    {'id': 'wiki_analogy', 'title': 'Wikipedia: Mechanical–electrical analogies', 'publisher': 'Wikipedia', 'url': SRC['wiki_analogy'],
     'usedFor': '阻抗類比（力 ↔ 電壓）：速度 ↔ 電流、位移 ↔ 電荷、質量 ↔ 電感、柔度（compliance，1/k）↔ 電容；類比不只一種'},
    {'id': 'wiki_ho', 'title': 'Wikipedia: Harmonic oscillator（類比表）', 'publisher': 'Wikipedia', 'url': SRC['wiki_ho'],
     'usedFor': '彈簧常數 k ↔ 1/C（彈性的倒數）、質量 m ↔ 電感 L；共振頻率 (1/2π)√(k/m) ↔ (1/2π)√(1/LC)；另一欄（質量 ↔ 電容）是對偶的配法'},
    {'id': 'lc_s1s2', 'title': 'LC 與約瑟夫森接面 圖解第 1、2 步', 'publisher': REPO, 'url': SRC['lc_s1s2'],
     'usedFor': '第 1 步：電感 I = φ 是直線、JJ I = sin φ 是正弦，φ 很小時兩者幾乎一樣；第 2 步：線性系統輸入加倍輸出加倍、不產生新頻率，大振幅時 JJ 產生 3ω 諧波'},
]

SCENES = [
 ('彈簧、單擺與 LC 電路', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第二十一堂，彈簧、單擺與電感電容電路，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂看到超導環裡的磁通只能一格一格地變；今天先離開超導，回到每個人都看過的東西：彈簧和單擺。',
  '我們要把力學的振盪和電路裡的振盪對起來，因為超導量子位元的出發點，就是一個會振盪的電路。'], ['curriculum', 'neighbors', 'ep049_p8']),
 ('三個重點', [
  '今天有三個重點：第一，彈簧和單擺都在來回振盪，能量在兩種形式之間換來換去。',
  '第二，電感電容電路也會振盪，只是來回跑的是電荷；第三，把兩邊一格一格對起來：質量對應電感，彈簧對應電容。',
  '今天的作品是一張類比對照表，左邊寫力學，右邊寫電路，每一格都要說得出理由。'], ['curriculum', 'ep049_p8']),
 ('彈簧振盪：來回換能量', [
  '先看彈簧：一個重物掛在彈簧上，往下拉一點再放手，它就上下來回振盪。',
  '拉得越開，彈簧拉回來的力越大，力和伸開的距離成正比；重物衝過中間時跑得最快，到兩端時停一下再折返。',
  '能量一直在換手：在兩端，彈簧的位能最多；在中間，動能最多；兩者加起來不變。'], ['ep049_p6', 'wiki_shm']),
 ('單擺：小角度的簡諧運動', [
  '再看單擺：一條細繩綁一個重物，拉開一個小角度放手，它就左右擺動。',
  '把它拉回中間的是重力，回復力和擺角的正弦成正比；擺角很小時，正弦幾乎等於角度本身，單擺就和彈簧一樣是簡諧運動。',
  '有趣的是，單擺的週期只看擺繩有多少公尺，換一個更重的重物，週期幾乎不變；一公尺的擺，來回一次大約兩秒。'], ['wiki_pendulum', 'wiki_shm', 'transmon_p8']),
 ('LC 電路：電荷來回流動', [
  '電路也能振盪：把一個電容和一個電感接成一圈，先把電容充好電。',
  '電容放電，電流流過電感；電感抗拒電流的改變，電流會繼續流，把電容反過來充電，然後再流回來。',
  '能量就在電容的電場和電感的磁場之間換來換去，電荷在電路裡來回流動，就像重物來回擺動。'], ['wiki_lc', 'ep049_p8']),
 ('類比對照表：一格一格對', [
  '現在把兩邊對起來：重物的位置對應電容上的電荷，重物的速度對應電路裡的電流。',
  '質量讓重物不容易加速或減速，電感讓電流不容易變快或變慢，所以質量對應電感。',
  '彈簧把位移變成拉回的力，電容把電荷變成電壓，所以彈簧對應電容；不過要小心，彈簧越硬，對應的電容反而越小。'], ['wiki_analogy', 'wiki_ho', 'curriculum']),
 ('週期對照：跟著根號走', [
  '對照表最有用的地方是週期：彈簧的週期跟著質量的根號變，質量變成四倍，週期變成兩倍。',
  '電路的週期跟著電感乘電容的根號變，所以把電感或電容換大，電路都振得比較慢；彈簧換硬，重物就振得比較快。',
  '如果電感是一奈亨、電容是一皮法，算出來大約每秒振盪五十億次，也就是五吉赫，正好落在超導量子位元常用的微波頻率附近。'], ['wiki_shm', 'wiki_ho', 'wiki_lc', 'jj_talk_p8']),
 ('小振幅才成立', [
  '要注意，這張對照表有一個前提：振幅要小。',
  '單擺拉到很大的角度，正弦和角度不再差不多，週期會比小角度時更久；一公尺的擺從九十度放手，週期大約多出百分之十八，已經不是簡諧運動了。',
  '暫停影片想一想：如果彈簧被拉過頭、變形回不去了，對照表還成立嗎？'], ['wiki_pendulum', 'curriculum', 'transmon_p8']),
 ('實作：用碼錶量週期', [
  '實作的時候，父子一起量週期：一個人拉開重物再放手，另一個人按碼錶，數十次來回再按停。',
  '把總時間除以十，就是一次的週期；數十次比只量一次準，因為按碼錶的反應時間被分攤掉了。',
  '量完彈簧再量單擺，把結果填進對照表的力學那一欄，再在電路那一欄寫下對應的東西。'], ['curriculum']),
 ('換你改造：先預測再驗證', [
  '下半場換你改造：一次只改一件事，先寫預測，再動手量。',
  '彈簧那邊把重物換成四倍重，預測週期變成幾倍；單擺那邊把擺繩剪成四分之一，預測週期變成多少。',
  '量完和預測比一比；再替單擺換一個更重的重物，看看週期是不是幾乎不變，記得每次都只拉開一個小角度。'], ['curriculum', 'wiki_shm', 'wiki_pendulum']),
 ('兩小時的振盪實驗室', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘量彈簧和單擺、填對照表，然後休息十分鐘。',
  '下半場三十分鐘，你自己改質量或擺繩，先預測再驗證；接著十分鐘交換角色，由你教爸爸怎麼量、為什麼這樣對應。',
  '最後五分鐘錄音總結，替你的類比對照表取個名字，再存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸做類比', [
  '最後一關，請不看稿說出：為什麼質量對應電感、彈簧對應電容？週期又會跟著什麼改變？',
  '再指出一個要注意的地方：類比只在小振幅時成立，拉到大角度的單擺就不再是簡諧運動。',
  '今天的作品是類比對照表，下一堂要看量子諧振子：電感電容電路的能階像一把間距相等的梯子，這正是它不能直接當量子位元的原因；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'neighbors']),
]

VISIBLE = [
 ['量子電腦學程 第二十一堂', '彈簧、單擺\n與 LC 電路', '力學振盪，對上電路振盪', '量子第二十一堂  ·  依課綱製作的課前教學版'],
 ['三個重點', '從彈簧到電路',
  '01 力學振盪', '彈簧和單擺\n能量換手', '→', '02 電路振盪', 'LC 電路\n電荷來回', '→', '03 對起來', '質量↔電感\n彈簧↔電容',
  '今天的作品：類比對照表'],
 ['彈簧振盪：來回換能量', '重物掛在彈簧上',
  '01', '拉得越開', '拉回的力越大',
  '02', '中間跑最快', '兩端停一下再折返',
  '03', '能量換手', '位能 ⇄ 動能，總和不變'],
 ['單擺：小角度的簡諧運動', '細繩加重物', '四個觀察',
  '第一點', '重力拉回', '第二點', 'sin θ ≈ θ', '第三點', '週期看擺長', '第四點', '1 公尺約 2 秒',
  '換更重的重物，週期幾乎不變'],
 ['LC 電路：電荷來回流動', '電容和電感接成一圈',
  '電容', '存電場的能量', '⇄', '電感', '存磁場的能量',
  '電荷來回流動，像重物來回擺',
  '能量在兩者之間換手'],
 ['類比對照表：一格一格對', '力學 ↔ 電路',
  '質量 m ↔ 電感 L', '都抗拒速度的改變', '彈簧 k ↔ 電容 C', 'k 對應 1/C', '位置 ↔ 電荷', '速度 ↔ 電流',
  '彈簧越硬，電容越小'],
 ['週期對照：跟著根號走', '把兩個公式並排',
  'T = 2π√(m/k)  ⇄  T = 2π√(LC)',
  '彈簧', '質量 ×4 → 週期 ×2', 'LC 電路', 'L 或 C 變大就變慢', '例子', '1 nH、1 pF ≈ 5 GHz',
  '量子位元常用的微波頻率'],
 ['小振幅才成立', '大角度的單擺會走樣',
  '一、小角度：sin θ ≈ θ\n二、大角度：週期變久\n三、不再是簡諧運動',
  '1 公尺的擺', '從 90 度放手', '週期約變成\n1.18 倍',
  '暫停影片：彈簧拉壞了還成立嗎？'],
 ['實作：用碼錶量週期', '數十次，再除以十',
  '放手的人（爸爸）', '拉開一點點\n輕輕放手',
  '計時的人（你）', '數十次來回\n再按停碼錶',
  '先量彈簧，再量單擺'],
 ['換你改造：先預測再驗證', '下半場，一次只改一件事',
  '01', '重物換四倍重', '彈簧週期變幾倍',
  '02', '擺繩剪成四分之一', '單擺週期變多少',
  '03', '單擺換更重的', '週期會變嗎'],
 ['兩小時的振盪實驗室', '影片先引路，接下來量、填、改、教',
  '00–25', '開場＋類比概念', '25–65', '量週期＋填對照表', '65–75', '休息十分鐘',
  '75–105', '改質量或擺長', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：用舊知識接新知識'],
 ['最後一關：教爸爸做類比', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '說出怎麼對應', '質量↔電感、彈簧↔電容',
  '02', '週期跟著什麼變', '根號質量、根號 LC',
  '03', '指出一個注意事項', '類比只在小振幅成立',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從上一堂的磁通量子化回到彈簧和單擺', '封面版型＋陳犀牛', '想一想電路為什麼會振盪'),
 ('三個重點：力學振盪、電路振盪、對起來', '三步流程卡＋黃字', '認識今天的作品'),
 ('彈簧振盪：回復力、最快與停頓的位置、能量換手', '三點條列＋陳犀牛', '說出能量怎麼換手'),
 ('單擺：重力拉回、sin θ ≈ θ、週期看擺長、1 公尺約 2 秒', '面板四張卡＋黃字', '說出單擺什麼時候是簡諧運動'),
 ('LC 電路：電容與電感換能量、電荷來回流動', '雙框對照＋白字＋黃字', '說出電路怎麼自己振盪'),
 ('類比對照表：質量↔電感、彈簧↔電容、位置↔電荷、速度↔電流', '三張步驟卡＋黃字', '說出每一格對應的理由'),
 ('週期對照：2π√(m/k) 與 2π√(LC)；1 nH、1 pF ≈ 5 GHz', '路徑一行＋三張卡＋黃字', '預測換大換小後的週期'),
 ('小振幅才成立：大角度單擺週期變久', '左三行＋右欄＋黃字', '暫停想彈簧拉壞了還成立嗎'),
 ('實作：用碼錶量十次來回', '左右比較卡＋黃字', '父子一起量週期、填對照表'),
 ('獨立改造：改質量或擺長，先預測再驗證', '三點條列＋陳犀牛', '寫預測、量、比一比'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：怎麼對應、週期跟著什麼變、注意事項；預告 Q022', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Curriculum rows (Q020, Q021, Q022), the curriculum slide decks ep049-superconducting-qubit.pptx p6, p8 and '
                      'transmon.pptx p8, plus JJ_Microwave_Readout_Talk.pptx p8 (slide text and speaker notes extracted with python-pptx), '
                      'and animations/lc-vs-jj.html (#s1, #s2) read by the producing agent on 2026-11-18; spring, pendulum and LC facts '
                      'and the analogy table checked against the Wikipedia articles Simple harmonic motion, Pendulum (mechanics), LC circuit, '
                      'Mechanical–electrical analogies and Harmonic oscillator (raw wikitext fetched 2026-11-18); periods and the 5 GHz '
                      'example recomputed by the producing agent with oscillation_table.py.',
        not_verified=['「質量↔電感、彈簧↔電容」是阻抗類比（力 ↔ 電壓、位移 ↔ 電荷）；簡報 ep049 p8 的哈密頓量那一列把磁通 Φ 對到位置 x，'
                      '那是對偶的配法（電容 ↔ 質量、1/L ↔ k），兩種都成立，本集依課綱用前一種，教材解答另作說明',
                      '「彈簧對應電容」嚴格說是彈簧的柔度 1/k 對應 C；旁白以「彈簧越硬，電容反而越小」說明',
                      '1 nH、1 pF 是為了好算而選的整數例子，不是某一顆量子位元的實際元件值；5.03 GHz 由 1/(2π√(LC)) 算出，與簡報 p8 的 f01 ≈ 5 GHz 比較',
                      '「一公尺的擺來回一次約兩秒」由 2π√(1/9.81) = 2.006 s 算出；「九十度放手週期多約百分之十八」由算術幾何平均公式算出（1.180 倍），未考慮擺繩質量與空氣阻力',
                      '家中實驗的彈簧本身有質量、擺錘不是質點，量到的週期會和公式差一點；本集不展開修正',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看',
                      '本集未錄影試拍；動畫段（lc-vs-jj.html 的捲動位置、滑桿以程式設定的時間點、入鏡範圍）待 v2 試錄確認'],
        tts_date='2026-11-18')

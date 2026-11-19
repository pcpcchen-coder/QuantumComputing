"""Q125 量測 1 次與 1000 次 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q125/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q125', 'q125-one-vs-thousand', '2026-11-18'
TITLE = '量測 1 次與 1000 次'
TOPIC = '量測 1 次與 1000 次'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q125/lesson.json',
    'bc_page': f'{REPO} animations/basic-circuits.html（八個範例；量測卡「量測 1 次」「量測 1,000 次」「清除」、「最近一次」綠框、灰色底理論機率與綠色實際次數、「共 N 次；理論：…」；sample()、addShots()、go() 會 clearShots()）',
    'bc_talk': f'{REPO} slides/output/basic-circuits.pptx（第 28 頁「互動動畫：逐步播放、自己量測」：右下可以量測 1 次或 1,000 次，灰底是理論機率、綠色是實際次數）',
    'op_talk': f'{REPO} slides/QC_Operation_Talk.pptx（第 32 頁「shots 與統計誤差」；第 30 頁「一個 shot 的讀取流程」；第 33 頁「讀取誤差與緩解」）',
    'op_scene': f'{REPO} animations/operation.html#readout（js/operation/07_readout.js「讀取與統計」）與 #qubit（01_qubit.js 說明「誤差約 √(p(1−p)/N)」）',
    'lln': 'https://en.wikipedia.org/wiki/Law_of_large_numbers',
    'binom': 'https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval',
    'rule68': 'https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule',
    'run': f'{REPO} academy/authoring/q125/classroom.py（shots_lab.py、qiskit_shots.py 實跑紀錄）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q125 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（用頁內的量測按鈕理解單次結果與統計結果的差別）、動手任務（每個範例各量 1 次與 1000 次，比較和理論機率的差距）、'
                '孩子獨立改造（估算要幾次才能把機率估到 ±2%）、好玩機制（科學實驗）、作品（量測比較表）、生活技能（重複實驗）、'
                '家長課前準備（basic-circuits 任一範例）、120 分鐘流程、驗收與常見誤解（1000 次的比例仍有約 ±1.6% 的統計誤差）'},
    {'id': 'bc_page', 'title': '互動動畫：量子電路入門 八個基礎量子電路（basic-circuits.html）', 'publisher': REPO, 'url': SRC['bc_page'],
     'usedFor': '量測卡說明「每次量測只會得到一個結果，狀態也就此塌縮。要重複很多次，才看得出機率分布。灰色底是理論機率，綠色是實際次數。」；'
                '按鈕「量測 1 次」「量測 1,000 次」「清除」；「最近一次：」綠框（量一顆時寫成 q2 = 0，量多顆時是整串）；每列「次數（百分比）」；'
                '最下面「共 N 次；理論：…」；量測會累加，go()（換步驟、換選項、換範例）會 clearShots() 歸零；每次 sample() 都照目前步驟的理論機率重新抽；'
                '八個範例預設的理論機率（Q124 實跑：疊加 50／50、干涉 1 為 100%、Bell 00／11、GHZ 000／111 各 50%、隱形傳態 q2 0 為 75%、Deutsch 1、BV 101、Grover 11 都是 100%）'},
    {'id': 'bc_talk', 'title': '量子電路入門：八個範例（簡報）第 28 頁', 'publisher': REPO, 'url': SRC['bc_talk'],
     'usedFor': '「右下可以量測 1 次或 1,000 次：灰底是理論機率、綠色是實際次數」'},
    {'id': 'op_talk', 'title': '如何操作量子電腦（簡報）第 30、32、33 頁', 'publisher': REPO, 'url': SRC['op_talk'],
     'usedFor': '第 32 頁「shots 與統計誤差」：σ(P̂) = √(P(1−P)/N)；經驗法則「只要看哪個結果最常出現：數百～數千」「估計機率到 ±1%：~2,500」「估計期望值到 ±0.01：~10,000」'
                '「錯誤緩解會再放大所需 shots」「精度 ×10 → shots ×100」（課綱 p32 正確）。第 30 頁：每個 shot 積分後成為 IQ 平面上的一個點，用閾值判成位元。'
                '第 33 頁：兩團 IQ 雲重疊、讀取期間 T₁ 衰減；縮短積分時間 → 雲變胖、重疊增加；讀取誤差緩解用混淆矩陣反推'},
    {'id': 'op_scene', 'title': '如何操作量子電腦 3D 場景 7「讀取與統計」、場景 1「狀態與測量」', 'publisher': REPO, 'url': SRC['op_scene'],
     'usedFor': '07_readout.js：預設 θ = 70°、連續 shots 每秒 60 個、積分時間 τ = 1.00 μs；IQ 點依閾值判成 0（藍）或 1（紅）；面板「理想 P(1) = 0.329」、'
                '「讀取保真度 F」τ = 1.00 μs 時 96.1%、τ = 0.10 μs 時 71.7%；「讀取誤差緩解」開關切換「緩解後／未緩解 P̂(1)」。01_qubit.js 說明「誤差約 √(p(1−p)/N)，要精度提高 10 倍就要 100 倍的 shots」'},
    {'id': 'lln', 'title': 'Law of large numbers', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['lln'],
     'usedFor': '「the average of the results obtained from a large number of independent random samples converges to the true value」；'
                '「There is no principle that a small number of observations will coincide with the expected value or that a streak of one value will immediately be "balanced" by the others」（賭徒謬誤）'},
    {'id': 'binom', 'title': 'Binomial proportion confidence interval', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['binom'],
     'usedFor': '二項比例的標準差 σₙ = √(p(1−p)/n)；比例的標準誤 √(p̂(1−p̂)/n)'},
    {'id': 'rule68', 'title': '68–95–99.7 rule', 'publisher': 'Wikipedia（2026-11-19 擷取 raw wikitext）', 'url': SRC['rule68'],
     'usedFor': '常態分布約 68% 的值落在平均值的一個標準差內、約 95% 在兩個標準差內'},
    {'id': 'run', 'title': 'shots_lab.py（純 Python，random.Random(1125)）與 qiskit_shots.py（Qiskit 2.6.2，StatevectorSampler seed=1125）實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': '誤差範圍：一半一半 1000 次 ±1.6 點、75% 1000 次 ±1.4 點、100% 為 0；±2% 需要 625 次（一半一半）、469 次（75%）；'
                '一半一半量 625 次重複 200 輪，137 輪（68%）落在 ±2% 內（二項分布精確值 66.3%）；連續三次 0 之後下一次是 1 的比例 49.1%；'
                '隱形傳態累加 1、10、100、1000、10000 次的比例；疊加範例 1000 次差 2.7 點（超出一個標準差，屬正常起伏）'},
]

SCENES = [
 ('量測 1 次與 1000 次', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百二十五堂，量測一次與一千次，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂把八個範例搬進自己的電腦；今天回到頁面，專心研究量測卡上那三個按鈕：量測一次、量測一千次和清除。',
  '今天記住一句話：量一次只告訴你這一次發生了什麼，量一千次才告訴你通常會發生什麼。'], ['curriculum', 'bc_page']),
 ('科學實驗：先猜、再量、再比', [
  '今天的好玩機制是科學實驗：先寫下假設，再動手量，最後拿數據和假設比一比，對不上就要找原因。',
  '我們的假設是：量一次的結果靠運氣；量一千次的比例會靠近灰色底的理論機率，但不會剛好相等。',
  '作品是一張量測比較表，八個範例各占一列，記下理論機率、量一次的結果、量一千次的比例，還有兩者的差距。'], ['curriculum', 'bc_talk']),
 ('量一次：只拿到一個答案', [
  '按一下量測一次，綠框只跳出一個結果；只量一顆位元時寫成編號幾等於多少，量好幾顆時就是一整串位元。',
  '頁面每按一次，都照同一條線路的機率重新抽一次，所以連按幾次，結果可以不一樣，也可以剛好一樣。',
  '只按一次的時候，下面的比例不是百分之百就是零，這只是那一次的運氣，還不能拿來代表機率。'], ['bc_page']),
 ('什麼時候量一次就夠', [
  '有些範例量一次就夠：干涉、德意志、密碼範例和兩顆位元的格羅弗，理論機率都是百分之百，集中在一個答案。',
  '這種線路把所有機率推到同一個結果上，量一次讀到的就是答案，再量下去，也只是重複確認。',
  '可是量子硬幣、貝爾態這種一半一半的範例，量一次只能說這個結果會出現，說不出它出現的機會有多大。'], ['bc_page', 'run']),
 ('量一千次：灰色底與綠色條', [
  '量一千次的時候，每個結果占一列：灰色底是理論機率，綠色條是實際比例，右邊寫著次數和百分比。',
  '最下面一行小字寫著一共量了幾次，後面接著每個結果的理論機率，正好拿來和綠色條對照。',
  '量測會一直累加，換範例、換選項或移動步驟才會歸零；想在同一步重新開始，就按清除。'], ['bc_page', 'bc_talk']),
 ('一千次還差多少：統計誤差', [
  '一千次的比例還是會和理論差一點，簡報第三十二頁給了算法：機率乘上一減機率，除以次數，再開根號。',
  '隱形傳態量到零的機率是四分之三，量一千次的誤差範圍大約正負一點四個百分點，比一半一半的範例小一些。',
  '這個範圍不是保證：大約三次裡有兩次會落在裡面，偶爾超出一點也正常，不代表頁面壞掉。'], ['op_talk', 'binom', 'rule68', 'run']),
 ('要幾次才能估到 ±2%', [
  '反過來問：想把一半一半的機率估到正負百分之二，要量幾次？把公式倒過來，零點二五除以零點零零零四，是六百二十五次。',
  '機率是四分之三的隱形傳態，同樣的精準度只要大約四百七十次；機率越靠近一半，需要的次數越多。',
  '簡報也列了經驗法則：只想知道哪個結果最常出現，幾百到幾千次就夠；要估到正負百分之一，大約要兩千五百次。'], ['op_talk', 'binom', 'run']),
 ('容易錯的地方', [
  '第一個容易錯：連續量到好幾次零，下一次並不會比較容易出現一；每一次都是重新準備，前面的結果不會影響後面。',
  '第二，大數法則說的是次數很多時，平均會靠近理論值；它沒有說短短幾次裡，零和一會自動補回平衡。',
  '第三，次數加多只會縮小隨機的誤差；如果讀取本身就會判錯，那一份偏差不會因為多量而消失。'], ['lln', 'op_talk', 'run']),
 ('父子共同實作：量測比較表', [
  '上半場四十分鐘，打開線路入門動畫，八個範例逐一走到最後一步，先按量測一次，把綠框的結果抄進比較表。',
  '接著按清除，再按量測一千次，把綠色的百分比抄下來，和灰色底的理論機率相減，算出差距。',
  '最後把差距和誤差範圍比一比：在範圍內就打勾；超出的話，再量一回一千次，看看是不是剛好運氣差。'], ['curriculum', 'bc_page']),
 ('換你改造：估算要量幾次', [
  '下半場換你估算：挑一個範例，先用公式算出要量幾次才能估到正負百分之二，寫在比較表旁邊。',
  '頁面的按鈕一次加一千，所以改用教材的小程式，它可以指定次數，把六百二十五次重複做兩百輪。',
  '數一數有幾輪落在正負百分之二以內；理論上大約三分之二，正好呼應剛才說的三次裡有兩次。'], ['curriculum', 'rule68', 'run']),
 ('兩小時的科學實驗', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘把八個範例各量一次和一千次、填比較表，然後休息十分鐘。',
  '下半場三十分鐘換你估算次數，再用程式驗證；接著十分鐘角色互換，由你教爸爸怎麼操作、為什麼要量很多次。',
  '最後五分鐘錄音總結、替比較表命名、存一個版本；今天的生活技能是重複實驗：一次的結果不算數，重複才可靠。'], ['curriculum']),
 ('最後一關：科學實驗報告', [
  '最後一關請不看稿說出：量一次和量一千次，各能告訴我們什麼？什麼樣的範例，量一次就夠？',
  '再指出一個注意事項：一千次的比例仍有大約正負一點六個百分點的統計誤差，差一點點是正常的，不是錯誤。',
  '今天的作品是量測比較表，下一堂要在本機模擬器加入雜訊，看看八個範例到了真實世界會變成什麼樣子；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'op_talk']),
]

VISIBLE = [
 ['量子電腦學程 第一百二十五堂', '量測 1 次\n與 1000 次', '單次結果 vs. 統計結果', '量子第一百二十五堂  ·  依課綱製作的課前教學版'],
 ['科學實驗：先猜、再量、再比', '假設 → 實驗 → 結論',
  '01 假設', '一次靠運氣\n千次靠近理論', '→', '02 實驗', '八個範例\n各量兩種', '→', '03 結論', '差距在\n誤差範圍內嗎',
  '今天的作品：量測比較表'],
 ['量一次：只拿到一個答案', '量測卡「最近一次」的綠框',
  '01', '一個結果', '量一顆寫 q2 = 0，量多顆是一整串',
  '02', '每次重新抽', '連按幾次，結果可以不同',
  '03', '比例只有 0% 或 100%', '一次的運氣，不代表機率'],
 ['什麼時候量一次就夠', '理論機率集中在一個答案嗎？', '確定型 vs. 機率型',
  '確定型', '100% 的範例', '量一次', '讀到的就是答案', '機率型', '50%、75% 的範例', '量一次', '只知道「會出現」',
  '機率型的範例要量很多次'],
 ['量一千次：灰色底與綠色條', '量測卡的讀法',
  '灰色底', '理論機率', '→', '綠色條', '實際比例＋次數（百分比）',
  '最下面一行：共幾次；理論各多少',
  '換範例、換選項、移動步驟就歸零'],
 ['一千次還差多少：統計誤差', '簡報 p32：σ = √(P(1−P)/N)',
  '一半一半', '1000 次：約 ±1.6%', '隱形傳態 75%', '1000 次：約 ±1.4%', '100% 的範例', '誤差是 0',
  '約三次有兩次落在 ±σ 內'],
 ['要幾次才能估到 ±2%', 'N = P(1−P) ÷ 0.02²',
  '想要的誤差  →  倒過來算  →  需要的次數',
  '625 次', '一半一半估到 ±2%', '約 470 次', '75% 估到 ±2%', '2,500 次', '一半一半估到 ±1%',
  '誤差減半，次數變四倍'],
 ['容易錯的地方', '量很多次之前先想清楚',
  '一、連續幾個 0，不會「該輪到 1」\n二、大數法則不會自動補回平衡\n三、多量只縮小隨機誤差',
  '每次都重新準備', '比例要很多次才穩', '讀取判錯的偏差\n不會因多量而消失',
  '暫停影片：寫下你最容易搞錯的一點'],
 ['父子共同實作：量測比較表', 'basic-circuits.html 八個範例',
  '量 1 次', '走到最後一步\n抄下綠框結果',
  '量 1000 次', '清除後再量\n抄百分比、算差距',
  '差距在 ±誤差內就打勾'],
 ['換你改造：估算要量幾次', '孩子獨立改造：先算，再用程式驗證',
  '01', '先算', 'N = P(1−P) ÷ 0.02²',
  '02', '再跑', 'shots_lab.py：625 次 × 200 輪',
  '03', '數一數', '約三分之二落在 ±2% 內'],
 ['兩小時的科學實驗', '影片先引路，接下來量、比、估',
  '00–25', '開場＋讀量測卡', '25–65', '八個範例各量兩種', '65–75', '休息十分鐘',
  '75–105', '估算次數再驗證', '105–115', '換你教爸爸', '115–120', '錄音總結＋存版本',
  '今日生活技能：重複實驗'],
 ['最後一關：科學實驗報告', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '一次與千次', '各能告訴我們什麼',
  '02', '量一次就夠', '答案集中在一個結果時',
  '03', '一個注意事項', '1000 次仍有約 ±1.6% 誤差',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、量測卡三個按鈕、今天的一句話', '封面版型＋陳犀牛', '說出今天要做的作品'),
 ('科學實驗：假設、實驗、結論；量測比較表', '三步流程卡＋黃字', '寫下自己的假設'),
 ('量一次：綠框一個結果、每次重新抽、比例只有 0% 或 100%', '三點條列＋陳犀牛', '按三次量測 1 次'),
 ('確定型（干涉、Deutsch、BV、Grover 2 顆）與機率型（疊加、Bell、GHZ、隱形傳態）', '面板四張卡＋黃字', '把八個範例分成兩類'),
 ('量測卡讀法：灰色底、綠色條、共幾次與理論、何時歸零（basic-circuits.pptx 第 28 頁）', '雙框對照＋白字＋黃字', '讀出一次量測一千次的結果'),
 ('統計誤差 σ = √(P(1−P)/N)（QC_Operation_Talk 第 32 頁）；±1.6、±1.4、0；約三分之二落在 ±σ 內', '三張步驟卡＋黃字', '算一個範例的誤差範圍'),
 ('估到 ±2%：625、約 470；經驗法則 ±1% 約 2,500', '路徑一行＋三張卡＋黃字', '倒過來算次數'),
 ('容易錯：賭徒謬誤、大數法則、讀取偏差不因多量消失', '左三行＋右欄＋黃字', '寫在比較表背面'),
 ('父子共同實作：八個範例各量 1 次與 1000 次，算差距、比誤差範圍', '左右比較卡＋黃字', '完成量測比較表'),
 ('獨立改造：公式估次數、shots_lab.py 625 次 × 200 輪', '三點條列＋陳犀牛', '數幾輪落在 ±2% 內'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：一次與千次、量一次就夠的條件、±1.6% 統計誤差；預告 Q126', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Law of large numbers, Binomial proportion confidence interval and 68–95–99.7 rule claims from Wikipedia raw wikitext fetched by the '
                      'producing agent on 2026-11-19 (verbatim quotes in production/source-notes.md); repo slides (QC_Operation_Talk.pptx pages 30, 32, 33; '
                      'basic-circuits.pptx page 28) and animation source (basic-circuits.html measurement card: sample, addShots, histRender, showLast, go/clearShots; '
                      'operation.html scenes 7 readout and 1 qubit) read by the producing agent and checked with Playwright screenshots; the readout scene '
                      'confusion-matrix values (F = 96.1% at 1.00 μs, 71.7% at 0.10 μs) read from the live panel and its raw-estimate bias checked by a Node Monte Carlo of the '
                      'same shot() code; shots_lab.py run with Python 3.13.18 (random.Random(1125)); qiskit_shots.py run with Qiskit 2.6.2 (StatevectorSampler seed=1125); '
                      'exact binomial probability for 625 shots within ±2% computed (0.663).',
        not_verified=['「誤差範圍」一律指一個標準差 σ = √(P(1−P)/N)（課綱 ±1.6%、簡報第 32 頁的寫法）；用兩個標準差（約 95%）時，±2% 需要約 2,500 次，本課未展開',
                      '「三次裡約有兩次落在 ±σ 內」是常態近似；625 次的二項分布精確值為 66.3%，次數很少或機率接近 0、100% 時近似會變差',
                      '讀取場景的模型（高斯雲、T₁ 衰減、閾值）是頁面的教學模擬，不代表特定硬體的數值',
                      'Qiskit 只用 2.6.2 實跑；課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')

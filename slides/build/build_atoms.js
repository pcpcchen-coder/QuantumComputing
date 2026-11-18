/* 產生簡報：離子阱與中性原子量子電腦 —— 系統、量子位元、操作與量測
 * 用法：node build_atoms.js
 * 輸出：../Ion_NeutralAtom_Talk.pptx 與 ../../speech/離子阱與中性原子演講稿.md（由同一份講者備註生成）
 * 投影片內容分在 atoms_slides_1.js（開場、離子阱）與 atoms_slides_2.js（中性原子、比較、總結）
 * 前置步驟：python3 make_atom_figures.py（物理圖表）、node shoot_atoms.js（3D 截圖與 atoms_crops.json）
 */
const fs = require('fs');
const path = require('path');
const { applyTheme } = require('./apply_theme');
const { makeDeck } = require('./deck_lib');

const ROOT = path.resolve(__dirname, '..');
const FIG = path.join(ROOT, 'figures');
const OUT = path.join(ROOT, 'Ion_NeutralAtom_Talk.pptx');
const SPEECH = path.resolve(ROOT, '..', 'speech', '離子阱與中性原子演講稿.md');
const ANIM = 'animations/atoms.html';
const SCENES = {
  ionsys: [1, '離子阱系統全景'], paul: [2, 'Paul 阱原理'], ionqubit: [3, '離子量子位元'], modes: [4, '離子鏈集體振動'], ms: [5, 'MS 閘'], qccd: [6, 'QCCD 搬運'],
  ionflow: [7, '離子運算與讀取'], hmaser: [8, '氫邁射頻率基準'], photonic: [9, '光子互連'],
  atomsys: [10, '中性原子系統全景'], tweezer: [11, '光鑷裝載與重排'], atomqubit: [12, '原子量子位元'], rydberg: [13, '芮德堡阻斷'], zoned: [14, '分區架構'], imaging: [15, '螢光成像讀取'],
  atomflow: [16, '原子運算與讀取'], atomclock: [17, '頻率基準與原子鐘'],
  compare: [18, '三平台比較'],
};
const D = makeDeck({ title: '離子阱與中性原子量子電腦：系統、量子位元、操作與量測', subject: 'Paul 阱、光鑷、雷射冷卻、MS 閘、芮德堡阻斷、螢光讀取、氫邁射頻率基準與平台比較', footer: '離子阱與中性原子量子電腦 · 系統 · 量子位元 · 操作 · 量測', scenes: SCENES, animRel: 'https://pcpcchen-coder.github.io/QuantumComputing/animations/atoms.html' });
const { pres, C, HEX, runs } = D;
const CROP = JSON.parse(fs.readFileSync(path.join(__dirname, 'atoms_crops.json'), 'utf8'));
/* 3D 截圖（自動裁掉背景）；name 可以是場景代號或額外截圖名稱（<場景>_<說明>） */
const pic = (s, name, x, y, w, h, o = {}) => D.fitImage(s, path.join(FIG, '3d_atoms', name + '.jpg'), x, y, w, h, { crop: CROP[name], alt: `3D 場景：${(SCENES[name] || SCENES[name.split('_')[0]])[1]}`, ...o });
const fig = (s, name, x, y, w, h, o = {}) => D.fitImage(s, path.join(FIG, 'atoms', name + '.png'), x, y, w, h, { alt: o.alt || name, ...o });

const SLIDES = [];
const S = (o) => SLIDES.push(o);
const H = (s, t) => s.addText(runs(t), { placeholder: 'title' });
const sec = (num, title, body, img, col = C.accent1) => async (s) => {
  s.addText(num, { x: 0.7, y: 1.3, w: 3, h: 1.4, fontSize: 80, bold: true, color: col, margin: 0, isTextBox: true, fontFace: 'Arial' });
  s.addText(runs(title), { placeholder: 'title' }); s.addText(runs(body), { placeholder: 'body' });
  if (img) await pic(s, img, 7.9, 0.9, 5.1, 5.6);
};
const sub = (s, t, x, y, w, col = C.text1, size = 18) => s.addText(runs(t), { x, y, w, h: 0.45, fontSize: size, bold: true, color: col, margin: 0, isTextBox: true, valign: 'middle' });
/* 左側色條標題 + 內文的小卡 */
const tile = (s, x, y, w, h, head, body, col = C.accent2, o = {}) => {
  D.card(s, x, y, w, h, o.fill);
  s.addShape(pres.shapes.RECTANGLE, { x, y: y + 0.12, w: 0.07, h: h - 0.24, fill: { color: col }, line: { color: col, width: 0 }, objectName: D.oname('tile-bar') });
  s.addText(runs(head), { x: x + 0.25, y: y + 0.1, w: w - 0.4, h: 0.42, fontSize: o.hs || 16, bold: true, color: col, margin: 0, isTextBox: true, valign: 'middle' });
  D.para(s, Array.isArray(body) ? body : [body], x + 0.25, y + 0.55, w - 0.45, h - 0.65, { size: (o.size || 13) * 1.12, color: '3A4356', space: o.space ?? 5, bullet: o.bullet });
};
/* 底部重點條 */
const takeaway = (s, text, y = 6.05) => {
  D.card(s, 0.6, y, 12.15, 0.72, 'FBF4E8');
  s.addText(runs(text), { x: 0.85, y, w: 11.7, h: 0.72, fontSize: 15, color: C.text1, valign: 'middle', margin: 0, isTextBox: true, objectName: D.oname('takeaway') });
};
const ION = C.accent1, ATOM = C.accent2, SC = C.accent6;
const ctx = { D, C, HEX, pres, runs, S, H, sec, sub, pic, fig, tile, takeaway, SCENES, SLIDES, ION, ATOM, SC };
require('./atoms_slides_1')(ctx);
require('./atoms_slides_2')(ctx);

const QA = [
  ['離子阱和中性原子都用「原子」，最大的差別是什麼？', '帶不帶電。離子帶電，可以用電場（Paul 阱）牢牢抓住，彼此有很強的庫侖作用，所以靠共同的振動模態做兩位元閘；中性原子不帶電，只能用雷射光鑷抓（深度約 1 mK，淺得多），平常幾乎不互相作用，要激發到芮德堡態才會「打開」交互作用。這個差別決定了兩者的閘機制、速度、規模與主要錯誤來源。'],
  ['為什麼離子阱的保真度特別高？', '離子在超高真空中、遠離表面（數十微米以上），超精細時鐘量子位元對磁場一階不敏感，T₂ 可達秒到小時；所有離子完全相同，不需要逐顆調頻率；雷射或微波控制的雜訊可以被精確校準。缺點是閘慢（數十到數百微秒）。'],
  ['中性原子號稱可以做到上萬顆，為什麼還沒有取代其他平台？', '原子數多不等於可用的運算多：閘保真度（~99.5%）仍略低於最好的離子阱；讀取慢（毫秒級）且多半是破壞性的；原子會從光鑷中損失，需要連續補充；每一層運算還要搬運原子（數百微秒）。2023–2025 年這些問題都有顯著進展（並行邏輯閘、連續裝載、擦除轉換），是目前進展最快的路線之一。'],
  ['這兩種平台需要稀釋冷凍機嗎？', '不需要。離子與原子本身是用雷射冷卻到 mK～μK，裝置主體在超高真空中、多半在室溫運作；部分離子阱系統把阱放在 4–20 K 的小型低溫恆溫器中（改善真空、降低電極雜訊），但遠比 10 mK 稀釋冷凍機簡單。主要的設施需求變成雷射、光學穩定度（恆溫、防振）與電子設備。'],
  ['離子在搬運時不會失去量子資訊嗎？', '只要電壓波形平滑、搬運速度與阱頻率匹配，離子的內部態（量子位元）幾乎不受影響；主要代價是運動被加熱，所以閘前要再冷卻（用另一種離子做共冷，不打擾量子位元）。目前 QCCD 系統的時間預算中，搬運與冷卻常佔多數。'],
  ['芮德堡態壽命很短，閘會不會很容易出錯？', '芮德堡態（n ≈ 50–70）的壽命約 100 μs 量級，而 CZ 閘只需要約 0.2–0.5 μs，原子只在芮德堡態停留很短時間，所以衰變造成的錯誤約在 0.1% 量級。主要錯誤還包括雷射相位雜訊、原子溫度造成的多普勒失諧與位置誤差。'],
  ['離子阱「用氫原子打微波」是什麼意思？', '指用氫邁射（氫原子鐘）當頻率基準：氫原子 21 公分線（1.42 GHz）在鐵氟龍泡與銅共振腔裡自我維持振盪，再把石英振盪器鎖上去輸出 10 MHz，所有微波合成器都鎖到它，產生相位穩定的 12.6 GHz 閘微波。它不直接操作量子位元；離子的 T₂ 長達秒級，控制微波若不夠穩，相位誤差就會變成 dephasing。很多實驗室用銣鐘或 GPS 馴服振盪器就夠，需要長時間相干時才用氫邁射（3D 場景 8、16）。'],
  ['離子阱和中性原子的讀取，「亮」代表的狀態為什麼相反？', '離子阱用循環躍遷只讓 |1⟩ 發光，所以亮 = |1⟩，離子留在阱裡、可重新初始化；中性原子的標準做法是先把 |1⟩ 的原子推出光鑷，再拍照看剩下的原子，所以亮 = |0⟩，被推走的原子要重新裝載，原子意外遺失也會被讀成 |1⟩（3D 場景 7、15）。'],
  ['中性原子的 MS 閘跟芮德堡 CZ 差在哪？', '中性原子不用 MS 閘：MS 需要共享的振動匯流排，只有帶電、靠庫侖力連成一串的離子才有；中性原子各自在光鑷裡，沒有共用振動，所以改用芮德堡阻斷。MS 是振動在相空間繞一圈留下幾何相位，原生形式 exp(−iπ/4·XX)，10–200 μs、全連接、> 99.9 %；芮德堡 CZ 是兩顆不能同時被激發，原生形式 diag(1,1,1,−1)，0.2–0.5 μs、要先搬到阻斷半徑內、可大量並行、約 99.5–99.7 %。兩者只差 Hadamard 與單位元 Z 旋轉，都是最大糾纏閘。'],
  ['離子阱的光子互連怎麼做遠端糾纏？', '兩個模組的通訊離子各被超快脈衝激發，放出一顆和自己糾纏的光子（例：(|↓⟩|H⟩ + |↑⟩|V⟩)/√2）；光子經單模光纖送到中間的分光鏡，兩顆光子無法分辨時做雙光子干涉，偵測器以特定組合同時響就「宣告」兩顆離子投影成貝爾態（糾纏交換）。成功率約 ½η²（η 為單顆光子的總偵測效率，約 1–3 %），每秒數十到數百對；失敗只是重試。成功後用本地 MS 閘交給記憶離子，再用量子態 / 量子閘傳送把模組連成一台電腦（3D 場景 9）。'],
  ['兩種平台的用電大概多少？', '公開資料很少：Quantinuum Helios 官方說基本單元 < 40 kW，與 Oracle 合作的資料寫約 60 kW（不含外部空調）；中性原子沒有官方數字，研究論文的模型假設約 7 kW（256 顆，僅供參考）。主要負載是雷射與其冷卻、控制電子、精密空調，而不是低溫系統。'],
];

(async () => {
  await D.loadIcons();
  let cur = null;
  for (const sd of SLIDES) {
    if (sd.sec !== cur) { pres.addSection({ title: sd.sec }); cur = sd.sec; }
    const slide = pres.addSlide({ masterName: sd.layout || 'CONTENT', sectionTitle: sd.sec });
    await sd.render(slide);
    const cue = sd.anim ? `【3D 動畫】場景 ${SCENES[sd.anim][0]}「${SCENES[sd.anim][1]}」：${ANIM}#${sd.anim}\n` : '';
    slide.addNotes(`${cue}【建議時間】約 ${sd.min} 分鐘\n\n${sd.notes}`);
  }
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, D.THEME);
  console.log('written', OUT, SLIDES.length, 'slides');
  const total = SLIDES.reduce((a, b) => a + b.min, 0);
  let md = `# 演講稿：離子阱與中性原子量子電腦 —— 系統、量子位元、操作與量測\n\n`;
  md += `> 本稿與 \`slides/Ion_NeutralAtom_Talk.pptx\` 的講者備註同步產生（來源：\`slides/build/build_atoms.js\`、\`atoms_slides_1.js\`、\`atoms_slides_2.js\`）。\n`;
  md += `> 共 ${SLIDES.length} 張投影片，預估總時長約 ${Math.round(total)} 分鐘（含 Q&A 約 10 分鐘）。互動 3D 動畫：\`${ANIM}\`（18 個場景）；系統建置細節：\`docs/離子阱與中性原子系統指南.md\`。\n\n`;
  md += `## 使用方式\n\n- 標示【切換到 3D 場景 N】時，點投影片右上角按鈕，或開啟 \`${ANIM}#場景代號\`。\n- 3D 操作：← → 切換、空白鍵暫停、H 隱藏面板、F 全螢幕、R 重設視角。\n- 超導量子電腦的對照內容：\`animations/index.html\`（JJ 與讀取）、\`animations/peripherals.html\`（周邊系統）、\`animations/operation.html\`（操作）。\n\n## 時間規劃\n\n| 段落 | 投影片 | 時間（分） |\n|---|---|---|\n`;
  const secs = {};
  SLIDES.forEach((s, i) => { (secs[s.sec] ||= { a: i + 1, b: i + 1, t: 0 }); secs[s.sec].b = i + 1; secs[s.sec].t += s.min; });
  Object.entries(secs).forEach(([k, v]) => { md += `| ${k} | ${v.a}–${v.b} | ${Math.round(v.t * 10) / 10} |\n`; });
  const skip = SLIDES.map((s, i) => (s.optional ? i + 1 : 0)).filter(Boolean);
  md += `\n### 60 分鐘精簡版建議\n\n- 可略過或快速帶過：第 ${skip.join('、')} 頁。\n- 3D 動畫只現場示範場景 1、5、7、9、10、13、16、18，其餘請聽眾會後自行操作。\n- 也可以只講一個平台：離子阱（01–02）或中性原子（03–04），再加 05 比較。\n\n---\n`;
  cur = null;
  SLIDES.forEach((s, i) => {
    if (s.sec !== cur) { md += `\n## ${s.sec}\n`; cur = s.sec; }
    md += `\n### 第 ${i + 1} 頁：${s.title.replace(/\n/g, '').replace(/[_^]\{([^}]*)\}/g, '$1').replace(/\*\*/g, '')}\n\n- 建議時間：約 ${s.min} 分鐘\n`;
    if (s.anim) md += `- 3D 動畫：場景 ${SCENES[s.anim][0]}「${SCENES[s.anim][1]}」→ \`${ANIM}#${s.anim}\`\n`;
    md += `\n${s.notes.split('\n').map((l) => l.trim()).filter(Boolean).join('\n\n')}\n`;
  });
  md += `\n---\n\n## Q&A 準備\n\n`;
  QA.forEach(([q, a], i) => { md += `**Q${i + 1}. ${q}**\n\n${a}\n\n`; });
  fs.writeFileSync(SPEECH, md);
  console.log('written', SPEECH);
})().catch((e) => { console.error(e); process.exit(1); });

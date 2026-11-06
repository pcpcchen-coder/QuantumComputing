/* 產生簡報：如何操作量子電腦 —— 設定、計算、讀取，以及它為什麼快
 * 用法：node build_operation.js
 * 輸出：../QC_Operation_Talk.pptx 與 ../../speech/量子電腦操作演講稿.md（由同一份講者備註生成）
 * 投影片內容分在 op_slides_1.js（開場、基礎、設定、計算）與 op_slides_2.js（讀取、加速原理、實務、總結）
 */
const fs = require('fs');
const path = require('path');
const { applyTheme } = require('./apply_theme');
const { makeDeck } = require('./deck_lib');

const ROOT = path.resolve(__dirname, '..');
const FIG = path.join(ROOT, 'figures');
const OUT = path.join(ROOT, 'QC_Operation_Talk.pptx');
const SPEECH = path.resolve(ROOT, '..', 'speech', '量子電腦操作演講稿.md');
const SCENES = {
  qubit: [1, '狀態與測量'], gates: [2, '單位元閘'], pulse: [3, '微波脈衝'], register: [4, '多位元與糾纏'], twoqubit: [5, '兩位元閘'], circuit: [6, '量子線路'],
  readout: [7, '讀取與統計'], interference: [8, '干涉'], grover: [9, 'Grover 搜尋'], shor: [10, 'Shor 週期尋找'], qec: [11, '錯誤更正'], workflow: [12, '完整流程'],
};
const D = makeDeck({ title: '如何操作量子電腦：設定、計算、讀取與加速原理', subject: '量子位元、量子閘、讀取、演算法與錯誤更正', footer: '如何操作量子電腦 · 設定 · 計算 · 讀取 · 加速原理', scenes: SCENES, animRel: '../animations/operation.html' });
const { pres, C, HEX, runs } = D;
const CROP = JSON.parse(fs.readFileSync(path.join(__dirname, 'op_crops.json'), 'utf8'));
/* 3D 截圖（自動裁掉背景）；name 可以是場景代號或額外截圖名稱 */
const pic = (s, name, x, y, w, h, o = {}) => D.fitImage(s, path.join(FIG, '3d_op', name + '.jpg'), x, y, w, h, { crop: CROP[name], alt: `3D 場景：${(SCENES[name] || SCENES[name.split('_')[0]])[1]}`, ...o });
const fig = (s, name, x, y, w, h, o = {}) => D.fitImage(s, path.join(FIG, 'op', name + '.png'), x, y, w, h, { alt: o.alt || name, ...o });
const CHART_FONT = { catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', legendFontFace: '+mn-lt', titleFontFace: '+mn-lt', dataLabelFontFace: '+mn-lt', valAxisTitleFontFace: '+mn-lt', catAxisTitleFontFace: '+mn-lt' };
const CHART_BASE = () => ({ ...CHART_FONT, catAxisLabelColor: '4A5468', valAxisLabelColor: '4A5468', catAxisLabelFontSize: 11, valAxisLabelFontSize: 11, valGridLine: { color: 'E3E7EE', size: 0.75 }, catGridLine: { style: 'none' }, legendFontSize: 11, titleFontSize: 13, titleColor: '1A1F2B' });

const SLIDES = [];
const S = (o) => SLIDES.push(o);
const H = (s, t) => s.addText(runs(t), { placeholder: 'title' });
const sec = (num, title, body, img, col = C.accent1) => async (s) => {
  s.addText(num, { x: 0.7, y: 1.3, w: 3, h: 1.4, fontSize: 80, bold: true, color: col, margin: 0, isTextBox: true, fontFace: 'Arial' });
  s.addText(runs(title), { placeholder: 'title' }); s.addText(runs(body), { placeholder: 'body' });
  if (img) await pic(s, img, 7.9, 0.9, 5.1, 5.6);
};
const sub = (s, t, x, y, w, col = C.text1, size = 18) => s.addText(runs(t), { x, y, w, h: 0.45, fontSize: size, bold: true, color: col, margin: 0, isTextBox: true, valign: 'middle' });
/* 程式碼框（深色底、等寬字） */
const codeBox = (s, lines, x, y, w, h, o = {}) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: '141A26' }, line: { color: '141A26', width: 0 }, objectName: D.oname('code-bg') });
  const arr = lines.map((ln, i) => {
    const isC = /^\s*(#|\/\/)/.test(ln);
    return { text: ln || ' ', options: { color: isC ? '7FA37A' : 'D8E4F2', breakLine: i < lines.length - 1 } };
  });
  s.addText(arr, { x: x + 0.2, y: y + 0.12, w: w - 0.4, h: h - 0.24, fontFace: 'Consolas', fontSize: o.size || 12.5, valign: 'top', margin: 0, isTextBox: true, lineSpacingMultiple: 1.05, objectName: D.oname('code') });
};
/* 左側色條標題 + 內文的小卡 */
const tile = (s, x, y, w, h, head, body, col = C.accent2, o = {}) => {
  D.card(s, x, y, w, h, o.fill);
  s.addShape(pres.shapes.RECTANGLE, { x, y: y + 0.12, w: 0.07, h: h - 0.24, fill: { color: col }, line: { color: col, width: 0 }, objectName: D.oname('tile-bar') });
  s.addText(runs(head), { x: x + 0.25, y: y + 0.1, w: w - 0.4, h: 0.42, fontSize: o.hs || 16, bold: true, color: col, margin: 0, isTextBox: true, valign: 'middle' });
  D.para(s, Array.isArray(body) ? body : [body], x + 0.25, y + 0.55, w - 0.45, h - 0.65, { size: (o.size || 13) * 1.12, color: '3A4356', space: o.space ?? 5, bullet: o.bullet });
};
const ctx = { D, C, HEX, pres, runs, S, H, sec, sub, pic, fig, codeBox, tile, CHART_BASE, SCENES };
require('./op_slides_1')(ctx);
require('./op_slides_2')(ctx);

const QA = [
  ['量子電腦可以取代我的筆電或伺服器嗎？', '不會。量子電腦是「加速器」，只對特定結構的問題有優勢（週期尋找、量子系統模擬、某些搜尋與取樣），而且輸入輸出都要經過古典電腦。一般的文書、資料庫、網頁、影像處理都不會因為量子電腦而變快。'],
  ['一個 shot 為什麼要重新從 |0⟩ 開始？', '測量會讓量子態塌縮，量測後原本的疊加就不存在了；而且量子態只能維持數十到數百微秒。所以每個 shot 都是獨立的一次「準備 → 演化 → 測量」，要靠重複很多次來累積統計。'],
  ['為什麼不能直接把 2ⁿ 個振幅讀出來？', '測量只會得到 n 個位元（Holevo 界限）。要估計所有振幅需要量子態斷層掃描，需要的設定數與 shots 隨 n 指數成長，等於把量子優勢全部抵銷。演算法必須設計成「答案集中在少數幾個結果上」。'],
  ['Shor 演算法現在能破解 RSA 嗎？', '還不能。2025 年的估計是：破解 RSA-2048 需要約一百萬個錯誤率 0.1% 的實體量子位元連續運轉不到一週；目前最大的系統約一千個量子位元，且尚未達到所需的錯誤更正規模。但「先收集、後解密」的風險促使各界導入後量子密碼（NIST FIPS 203/204/205，2024）。'],
  ['量子電腦的結果每次都不一樣，可以信任嗎？', '量子計算本質上是機率性的：我們估計的是分佈或期望值，誤差可以由 shots 數控制（∝ 1/√N）。對於像 Shor、Grover 這類答案可以用古典電腦快速驗證的問題，只要驗證就能確定答案。'],
  ['錯誤緩解和錯誤更正差在哪裡？', '錯誤緩解（ZNE、PEC、讀取緩解）是在後處理中用統計方法「估計」無雜訊的期望值，代價是 shots 增加，沒有保護量子資訊本身；錯誤更正用很多實體量子位元編碼一個邏輯量子位元，在計算過程中持續偵測並修正錯誤，是長時間、大規模計算的必要條件。'],
  ['一般工程師要從哪裡開始學操作量子電腦？', '從 Qiskit 或 Cirq 的教學開始，在模擬器上寫 Bell 態、Grover、QFT；再用雲端平台（IBM Quantum、Amazon Braket、Azure Quantum 等）送到真機，比較模擬與真機結果的差異，並嘗試讀取誤差緩解與動態解耦等設定。'],
];

(async () => {
  await D.loadIcons();
  let cur = null;
  for (const sd of SLIDES) {
    if (sd.sec !== cur) { pres.addSection({ title: sd.sec }); cur = sd.sec; }
    const slide = pres.addSlide({ masterName: sd.layout || 'CONTENT', sectionTitle: sd.sec });
    await sd.render(slide);
    const cue = sd.anim ? `【3D 動畫】場景 ${SCENES[sd.anim][0]}「${SCENES[sd.anim][1]}」：animations/operation.html#${sd.anim}\n` : '';
    slide.addNotes(`${cue}【建議時間】約 ${sd.min} 分鐘\n\n${sd.notes}`);
  }
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, D.THEME);
  console.log('written', OUT, SLIDES.length, 'slides');
  const total = SLIDES.reduce((a, b) => a + b.min, 0);
  let md = `# 演講稿：如何操作量子電腦 —— 設定、計算、讀取，以及它為什麼快\n\n`;
  md += `> 本稿與 \`slides/QC_Operation_Talk.pptx\` 的講者備註同步產生（來源：\`slides/build/build_operation.js\`、\`op_slides_1.js\`、\`op_slides_2.js\`）。\n`;
  md += `> 共 ${SLIDES.length} 張投影片，預估總時長約 ${Math.round(total)} 分鐘（含 Q&A 約 10 分鐘）。互動 3D 動畫：\`animations/operation.html\`（12 個場景）。\n\n`;
  md += `## 使用方式\n\n- 標示【切換到 3D 場景 N】時，點投影片右上角按鈕，或開啟 \`animations/operation.html#場景代號\`。\n- 3D 操作：← → 切換、空白鍵暫停、H 隱藏面板、F 全螢幕、R 重設視角。\n- 前兩次分享的內容（JJ 元件與微波讀取、周邊系統）分別在 \`animations/index.html\`、\`animations/peripherals.html\`。\n\n## 時間規劃\n\n| 段落 | 投影片 | 時間（分） |\n|---|---|---|\n`;
  const secs = {};
  SLIDES.forEach((s, i) => { (secs[s.sec] ||= { a: i + 1, b: i + 1, t: 0 }); secs[s.sec].b = i + 1; secs[s.sec].t += s.min; });
  Object.entries(secs).forEach(([k, v]) => { md += `| ${k} | ${v.a}–${v.b} | ${Math.round(v.t * 10) / 10} |\n`; });
  const skip = SLIDES.map((s, i) => (s.optional ? i + 1 : 0)).filter(Boolean);
  md += `\n### 精簡版建議（約 90 分鐘）\n\n- 可略過或快速帶過：第 ${skip.join('、')} 頁。\n- 3D 動畫只現場示範場景 1、2、6、8、9、10、11，其餘請聽眾會後自行操作。\n- 每頁講解以投影片重點為主，備註中的延伸說明留給 Q&A；Q&A 縮短為 5 分鐘。\n- 也可以分兩次進行：第一次 01–03（基礎、設定、計算），第二次 04–06（讀取、加速原理、實務）。\n\n---\n`;
  cur = null;
  SLIDES.forEach((s, i) => {
    if (s.sec !== cur) { md += `\n## ${s.sec}\n`; cur = s.sec; }
    md += `\n### 第 ${i + 1} 頁：${s.title.replace(/\n/g, '').replace(/[_^]\{([^}]*)\}/g, '$1').replace(/\*\*/g, '')}\n\n- 建議時間：約 ${s.min} 分鐘\n`;
    if (s.anim) md += `- 3D 動畫：場景 ${SCENES[s.anim][0]}「${SCENES[s.anim][1]}」→ \`animations/operation.html#${s.anim}\`\n`;
    md += `\n${s.notes.split('\n').map((l) => l.trim()).filter(Boolean).join('\n\n')}\n`;
  });
  md += `\n---\n\n## Q&A 準備\n\n`;
  QA.forEach(([q, a], i) => { md += `**Q${i + 1}. ${q}**\n\n${a}\n\n`; });
  fs.writeFileSync(SPEECH, md);
  console.log('written', SPEECH);
})().catch((e) => { console.error(e); process.exit(1); });

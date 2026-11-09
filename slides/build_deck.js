#!/usr/bin/env node
/*
 * 影片 → 報告用 PPT 產生器（通用引擎）
 *
 * 用法：
 *   node build_deck.js episodes/ep049.js            # 輸出到 output/<meta.output>
 *   node build_deck.js episodes/ep049.js out.pptx   # 指定輸出檔
 *
 * 每一集只需要寫一個內容檔（episodes/epXXX.js），匯出 { meta, slides }。
 * 支援的投影片類型與欄位請見 slides/README.md。
 */
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// ───────────────────────────── 主題 ─────────────────────────────
// 超導／低溫主題：深海軍藍為主、冰藍為底、青綠強調、琥珀色代表「能量／微波」
const THEME = {
  name: "QuBear Cryo",
  headFontFace: "Microsoft JhengHei",
  bodyFontFace: "Microsoft JhengHei",
  colors: {
    dk1: "152033", // 內文
    lt1: "FFFFFF",
    dk2: "0F2B46", // 標題、深色頁背景
    lt2: "EAF3F8", // 卡片底色（冰藍）
    accent1: "1A9DB0", // 青綠：主要強調
    accent2: "E8962E", // 琥珀：能量、微波
    accent3: "6C5CE7", // 紫：量子
    accent4: "D64545", // 紅：不行 ✗
    accent5: "2E9E64", // 綠：可以 ✓
    accent6: "5E6E82", // 石板灰：說明文字
    hlink: "1A9DB0",
    folHlink: "6C5CE7",
  },
};
const HEX = THEME.colors;
const EQ_FONT = "Cambria"; // 方程式用（Office 內建，含希臘字母）

const W = 13.333;
const H = 7.5;
const MX = 0.6; // 左右邊界
const TOP = 1.55; // 內容區上緣
const BOTTOM = 6.7; // 內容區下緣
const CW = W - 2 * MX; // 內容寬

// ───────────────────────────── 小工具 ─────────────────────────────
/** 把簡單標記轉成 pptxgenjs 的 runs：**粗體**、_{下標}、^{上標} */
function runs(str, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|_\{[^}]*\}|\^\{[^}]*\})/g;
  let last = 0;
  let m;
  const push = (text, extra = {}) => {
    if (text) out.push({ text, options: { ...base, ...extra } });
  };
  while ((m = re.exec(str))) {
    push(str.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith("**")) push(tok.slice(2, -2), { bold: true, color: base.strongColor || C().accent1 });
    else if (tok.startsWith("_{")) push(tok.slice(2, -1), { subscript: true });
    else push(tok.slice(2, -1), { superscript: true });
    last = m.index + tok.length;
  }
  push(str.slice(last));
  if (!out.length) out.push({ text: "", options: { ...base } });
  out.forEach((r) => delete r.options.strongColor);
  return out;
}

/** 多段落（每段一個 item）組成一個 text 陣列 */
function paragraphs(items, paraOpts = {}, runOpts = {}) {
  const arr = [];
  items.forEach((item, i) => {
    const isLast = i === items.length - 1;
    const isSub = typeof item === "object" && item.sub;
    const text = typeof item === "string" ? item : item.text;
    const pOpts = {
      ...paraOpts,
      ...(isSub ? { indentLevel: 1, fontSize: (runOpts.fontSize || 16) - 2 } : {}),
    };
    // 段落屬性（項目符號、間距）只能放在該段第一個 run，否則 pptxgenjs 會把每個 run 拆成新段落
    const rs = runs(text, { ...runOpts, ...(isSub ? { fontSize: pOpts.fontSize } : {}) });
    Object.assign(rs[0].options, pOpts);
    rs[rs.length - 1].options.breakLine = !isLast;
    arr.push(...rs);
  });
  return arr;
}

let _pres = null;
const C = () => _pres.SchemeColor;

const iconCache = new Map();
async function iconPng(spec, hex = "FFFFFF") {
  const key = spec + hex;
  if (iconCache.has(key)) return iconCache.get(key);
  const [lib, name] = spec.split(":");
  const mod = require(`react-icons/${lib}`);
  const Comp = mod[name];
  if (!Comp) throw new Error(`找不到圖示 ${spec}`);
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + hex, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  const data = "image/png;base64," + buf.toString("base64");
  iconCache.set(key, data);
  return data;
}

/** 彩色圓形 + 白色圖示（本範本的視覺主軸） */
async function iconCircle(slide, spec, x, y, d, fill, name) {
  slide.addShape(_pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" }, objectName: `${name}-circle` });
  const pad = d * 0.22;
  slide.addImage({ data: await iconPng(spec), x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad, objectName: `${name}-icon` });
}

const TONE = () => ({
  good: C().accent5,
  bad: C().accent4,
  warn: C().accent2,
  neutral: C().accent1,
  quantum: C().accent3,
});

// ───────────────────────────── 版面（layouts） ─────────────────────────────
function defineLayouts(pres, meta) {
  const footer = meta.footer || meta.series || "";
  pres.defineSlideMaster({
    title: "TITLE_DARK",
    background: { color: C().text2 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.25, w: 8.4, h: 1.9, fontSize: 40, bold: true, color: C().background1, align: "left", valign: "top", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "subtitle", type: "body", x: 0.8, y: 4.3, w: 8.4, h: 0.9, fontSize: 20, color: C().background2, align: "left", valign: "top", margin: 0 }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "CONTENT",
    background: { color: C().background1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.4, w: 10.3, h: 0.85, fontSize: 32, bold: true, color: C().text2, align: "left", valign: "middle", margin: 0 }, text: "" } },
      { text: { text: footer, options: { x: MX, y: 6.98, w: 9, h: 0.32, fontSize: 11, color: C().accent6, margin: 0 } } },
    ],
    slideNumber: { x: 12.13, y: 6.98, w: 0.6, h: 0.32, fontSize: 11, color: C().accent6, align: "right", margin: 0 },
  });
  pres.defineSlideMaster({
    title: "DARK",
    background: { color: C().text2 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.4, w: 10.3, h: 0.85, fontSize: 32, bold: true, color: C().background1, align: "left", valign: "middle", margin: 0 }, text: "" } },
      { text: { text: footer, options: { x: MX, y: 6.98, w: 9, h: 0.32, fontSize: 11, color: C().background2, margin: 0 } } },
    ],
    slideNumber: { x: 12.13, y: 6.98, w: 0.6, h: 0.32, fontSize: 11, color: C().background2, align: "right", margin: 0 },
  });
}

/** 每張內容頁右上角的「影片時間」標籤 */
function timeChip(slide, time, dark = false) {
  if (!time) return;
  slide.addShape(_pres.shapes.ROUNDED_RECTANGLE, {
    x: 11.05, y: 0.6, w: 1.68, h: 0.44, rectRadius: 0.22,
    fill: { color: dark ? C().background1 : C().background2 }, line: { type: "none" }, objectName: "time-chip",
  });
  slide.addText(`▶ ${time}`, {
    x: 11.05, y: 0.6, w: 1.68, h: 0.44, fontSize: 12, color: C().text2, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "time-chip-text",
  });
}

function bulletBox(slide, items, x, y, w, h, opts = {}) {
  slide.addText(
    paragraphs(items, { bullet: { indent: 18 }, paraSpaceAfter: opts.space ?? 10 }, { fontSize: opts.fontSize || 16, color: opts.color || C().text1 }),
    { x, y, w, h, valign: "top", margin: [2, 4, 2, 0], isTextBox: true, objectName: opts.name || "bullets" }
  );
}

function captionText(slide, text, x, y, w, name = "caption") {
  slide.addText(runs(text, { fontSize: 11, color: C().accent6, italic: true }), { x, y, w, h: 0.3, margin: 0, isTextBox: true, objectName: name });
}

// ───────────────────────────── 投影片類型 ─────────────────────────────
const R = {};

R.title = async (pres, s, meta) => {
  const slide = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: s.section });
  slide.addText(s.kicker || meta.series, { x: 0.8, y: 1.45, w: 8.4, h: 0.5, fontSize: 16, bold: true, color: C().accent2, margin: 0, isTextBox: true, objectName: "kicker" });
  slide.addText(s.title, { placeholder: "title" });
  if (s.subtitle) slide.addText(s.subtitle, { placeholder: "subtitle" });
  if (s.meta) {
    slide.addText(paragraphs(s.meta, { paraSpaceAfter: 4 }, { fontSize: 13, color: C().background2 }), {
      x: 0.8, y: 5.55, w: 8.4, h: 1.1, margin: 0, valign: "top", isTextBox: true, objectName: "source-meta",
    });
  }
  // 視覺主軸：不等距能階（愈往上愈密），呼應「非諧振子」
  const levels = s.levels || [0, 1, 1.8, 2.45, 2.95, 3.3];
  const x0 = 9.9, x1 = 12.5, yb = 5.9, scale = 1.05;
  levels.forEach((e, i) => {
    const y = yb - e * scale;
    slide.addShape(pres.shapes.LINE, { x: x0, y, w: x1 - x0, h: 0, line: { color: i < 2 ? HEX.accent2 : HEX.accent1, width: i < 2 ? 4 : 2.5 }, objectName: `deco-level-${i}` });
    slide.addText(`|${i}⟩`, { x: x1 + 0.08, y: y - 0.2, w: 0.6, h: 0.4, fontSize: 14, fontFace: EQ_FONT, color: i < 2 ? C().accent2 : C().background2, margin: 0, isTextBox: true, objectName: `deco-ket-${i}` });
  });
  slide.addShape(pres.shapes.LINE, { x: 10.6, y: yb - levels[1] * scale + 0.06, w: 0, h: (levels[1] - levels[0]) * scale - 0.12, line: { color: HEX.lt1, width: 2.5, beginArrowType: "triangle" }, objectName: "deco-arrow" });
  if (s.notes) slide.addNotes(s.notes);
};

R.agenda = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time);
  const items = s.items;
  const cols = 3, rows = Math.ceil(items.length / cols);
  const gap = 0.3;
  const cw = (CW - gap * (cols - 1)) / cols;
  const ch = (BOTTOM - TOP - gap * (rows - 1)) / rows;
  items.forEach((it, i) => {
    const c = i % cols, r = Math.floor(i / cols);
    const x = MX + c * (cw + gap), y = TOP + r * (ch + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: ch, rectRadius: 0.12, fill: { color: C().background2 }, line: { type: "none" }, objectName: `agenda-card-${i}` });
    slide.addShape(pres.shapes.OVAL, { x: x + 0.3, y: y + 0.3, w: 0.62, h: 0.62, fill: { color: C().accent1 }, line: { type: "none" }, objectName: `agenda-num-bg-${i}` });
    slide.addText(String(i + 1), { x: x + 0.3, y: y + 0.3, w: 0.62, h: 0.62, fontSize: 20, bold: true, color: C().background1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: `agenda-num-${i}` });
    if (it.time) slide.addText(it.time, { x: x + cw - 1.9, y: y + 0.42, w: 1.6, h: 0.38, fontSize: 12, color: C().accent6, align: "right", margin: 0, isTextBox: true, objectName: `agenda-time-${i}` });
    slide.addText(it.head, { x: x + 0.3, y: y + 1.08, w: cw - 0.6, h: 0.5, fontSize: 19, bold: true, color: C().text2, margin: 0, valign: "top", isTextBox: true, objectName: `agenda-head-${i}` });
    slide.addText(runs(it.body, { fontSize: 14, color: C().text1 }), { x: x + 0.3, y: y + 1.62, w: cw - 0.6, h: ch - 1.8, margin: 0, valign: "top", isTextBox: true, objectName: `agenda-body-${i}` });
  });
  if (s.notes) slide.addNotes(s.notes);
};

R.cards = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time);
  let y0 = TOP;
  if (s.lead) {
    slide.addText(runs(s.lead, { fontSize: 18, color: C().text1 }), { x: MX, y: TOP, w: CW, h: 0.6, margin: 0, valign: "top", isTextBox: true, objectName: "lead" });
    y0 = TOP + 0.85;
  }
  const bottom = s.callout ? BOTTOM - 0.95 : BOTTOM;
  const n = s.cards.length;
  const gap = 0.3;
  const cw = (CW - gap * (n - 1)) / n;
  const ch = bottom - y0;
  for (let i = 0; i < n; i++) {
    const cd = s.cards[i];
    const x = MX + i * (cw + gap);
    const tone = TONE()[cd.tone || "neutral"];
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: y0, w: cw, h: ch, rectRadius: 0.12, fill: { color: C().background2 }, line: { type: "none" }, objectName: `card-${i}` });
    const toneHex = { good: HEX.accent5, bad: HEX.accent4, warn: HEX.accent2, neutral: HEX.accent1, quantum: HEX.accent3 }[cd.tone || "neutral"];
    await iconCircle(slide, cd.icon || "md:MdScience", x + 0.3, y0 + 0.3, 0.8, toneHex, `card-${i}`);
    if (cd.badge) {
      slide.addText(cd.badge, { x: x + 1.25, y: y0 + 0.42, w: cw - 1.5, h: 0.56, fontSize: 15, bold: true, color: tone, margin: 0, valign: "middle", isTextBox: true, objectName: `card-badge-${i}` });
    }
    slide.addText(cd.head, { x: x + 0.3, y: y0 + 1.3, w: cw - 0.6, h: 0.55, fontSize: 19, bold: true, color: C().text2, margin: 0, valign: "top", isTextBox: true, objectName: `card-head-${i}` });
    const body = Array.isArray(cd.body) ? cd.body : [cd.body];
    slide.addText(paragraphs(body, { paraSpaceAfter: 8 }, { fontSize: n <= 3 ? 16 : 14, color: C().text1 }), { x: x + 0.3, y: y0 + 1.9, w: cw - 0.6, h: ch - 2.1, margin: 0, valign: "top", isTextBox: true, objectName: `card-body-${i}` });
  }
  if (s.callout) callout(slide, s.callout, MX, BOTTOM - 0.7, CW, 0.7);
  if (s.notes) slide.addNotes(s.notes);
};

function callout(slide, text, x, y, w, h) {
  slide.addShape(_pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: C().text2 }, line: { type: "none" }, objectName: "callout-bg" });
  slide.addText(runs(text, { fontSize: 17, color: C().background1, bold: false, strongColor: C().accent2 }), { x: x + 0.3, y, w: w - 0.6, h, margin: 0, valign: "middle", isTextBox: true, objectName: "callout-text" });
}

function eqBox(slide, eq, label, x, y, w, h, i) {
  slide.addShape(_pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: C().background2 }, line: { type: "none" }, objectName: `eq-bg-${i}` });
  const eqH = label ? h * 0.6 : h;
  slide.addText(runs(eq, { fontSize: 24, fontFace: EQ_FONT, color: C().text2 }), { x: x + 0.2, y: y + 0.05, w: w - 0.4, h: eqH, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: `eq-${i}` });
  if (label) slide.addText(runs(label, { fontSize: 13, color: C().accent6 }), { x: x + 0.2, y: y + eqH - 0.05, w: w - 0.4, h: h - eqH, align: "center", valign: "top", margin: 0, isTextBox: true, objectName: `eq-label-${i}` });
}

R.equations = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time);
  const leftW = s.eqWidth || 6.1;
  const gap = 0.25;
  const n = s.eqs.length;
  const bottom = s.callout ? BOTTOM - 0.95 : BOTTOM;
  const eh = Math.min(1.45, (bottom - TOP - gap * (n - 1)) / n);
  s.eqs.forEach((e, i) => eqBox(slide, e.eq, e.label, MX, TOP + i * (eh + gap), leftW, eh, i));
  bulletBox(slide, s.bullets, MX + leftW + 0.5, TOP, CW - leftW - 0.5, bottom - TOP);
  if (s.callout) callout(slide, s.callout, MX, BOTTOM - 0.7, CW, 0.7);
  if (s.notes) slide.addNotes(s.notes);
};

function chartOpts(spec, extra = {}) {
  const T = HEX;
  return {
    showTitle: !!spec.title, title: spec.title, titleFontSize: 14, titleColor: T.dk2, titleFontFace: "+mn-lt",
    showLegend: spec.series.length > 1, legendPos: "b", legendFontSize: 12, legendFontFace: "+mn-lt", legendColor: T.dk1,
    catAxisLabelColor: T.accent6, valAxisLabelColor: T.accent6, catAxisLabelFontSize: 12, valAxisLabelFontSize: 12,
    catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    valGridLine: { color: "D9E3EA", size: 0.75 }, catGridLine: { style: "none" },
    catAxisLineColor: "B8C5D0", valAxisLineShow: false,
    showCatAxisTitle: !!spec.xTitle, catAxisTitle: spec.xTitle, catAxisTitleColor: T.accent6, catAxisTitleFontSize: 12, catAxisTitleFontFace: "+mn-lt",
    showValAxisTitle: !!spec.yTitle, valAxisTitle: spec.yTitle, valAxisTitleColor: T.accent6, valAxisTitleFontSize: 12, valAxisTitleFontFace: "+mn-lt",
    chartColors: spec.series.map((x) => x.color || T.accent1),
    ...extra,
  };
}

function addChart(slide, spec, x, y, w, h) {
  const data = spec.series.map((sr) => ({ name: sr.name, labels: spec.labels, values: sr.values }));
  if (spec.kind === "bar") {
    slide.addChart(_pres.charts.BAR, data, {
      x, y, w, h, barDir: "col", barGapWidthPct: 60,
      ...chartOpts(spec, { showValue: true, dataLabelPosition: "outEnd", dataLabelColor: HEX.dk2, dataLabelFontSize: 13, dataLabelFontFace: "+mn-lt", dataLabelFontBold: true }),
      ...(spec.options || {}), objectName: "chart",
    });
  } else {
    slide.addChart(_pres.charts.LINE, data, {
      x, y, w, h, lineSize: 3, lineDataSymbol: "none",
      ...chartOpts(spec),
      ...(spec.options || {}), objectName: "chart",
    });
  }
}

R.chart = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time);
  const chartW = s.chartWidth || 6.9;
  const bottom = s.callout ? BOTTOM - 0.95 : BOTTOM;
  addChart(slide, s.chart, MX, TOP, chartW, bottom - TOP - (s.caption ? 0.35 : 0));
  if (s.caption) captionText(slide, s.caption, MX, bottom - 0.3, chartW);
  bulletBox(slide, s.bullets, MX + chartW + 0.5, TOP + 0.1, CW - chartW - 0.5, bottom - TOP - 0.1);
  if (s.callout) callout(slide, s.callout, MX, BOTTOM - 0.7, CW, 0.7);
  if (s.notes) slide.addNotes(s.notes);
};

/** 方程式橫條 + 左圖表 + 右側「各項說明」卡 */
R.expansion = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time);
  eqBox(slide, s.eq, s.eqLabel, MX, TOP, CW, 1.15, 0);
  const y0 = TOP + 1.45;
  const chartW = 6.4;
  addChart(slide, s.chart, MX, y0, chartW, BOTTOM - y0 - 0.35);
  if (s.caption) captionText(slide, s.caption, MX, BOTTOM - 0.3, chartW);
  const x = MX + chartW + 0.4, w = CW - chartW - 0.4;
  const gap = 0.2, n = s.terms.length;
  const th = (BOTTOM - y0 - gap * (n - 1)) / n;
  s.terms.forEach((t, i) => {
    const y = y0 + i * (th + gap);
    const toneHex = { good: HEX.accent5, bad: HEX.accent4, warn: HEX.accent2, neutral: HEX.accent1, quantum: HEX.accent3 }[t.tone || "neutral"];
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: th, rectRadius: 0.1, fill: { color: C().background2 }, line: { type: "none" }, objectName: `term-bg-${i}` });
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.2, y: y + (th - 0.5) / 2, w: 1.55, h: 0.5, rectRadius: 0.25, fill: { color: toneHex }, line: { type: "none" }, objectName: `term-pill-${i}` });
    slide.addText(runs(t.term, { fontSize: 15, fontFace: EQ_FONT, color: C().background1, bold: true }), { x: x + 0.2, y: y + (th - 0.5) / 2, w: 1.55, h: 0.5, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: `term-${i}` });
    slide.addText([
      ...runs(t.head, { fontSize: 16, bold: true, color: C().text2, breakLine: true }),
      ...runs(t.body, { fontSize: 13, color: C().text1 }),
    ], { x: x + 1.95, y, w: w - 2.1, h: th, valign: "middle", margin: 0, isTextBox: true, objectName: `term-text-${i}` });
  });
  if (s.notes) slide.addNotes(s.notes);
};

/** 能階圖：一或兩組「樓梯」，可畫躍遷箭頭（ok / bad / neutral） */
R.ladder = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time);
  const n = s.ladders.length;
  const diagW = s.diagramWidth || (n === 1 ? 5.4 : 7.6);
  const bottom = s.callout ? BOTTOM - 0.95 : BOTTOM;
  const gap = 0.3;
  const pw = (diagW - gap * (n - 1)) / n;
  const toneHex = { good: HEX.accent5, bad: HEX.accent4, warn: HEX.accent2, neutral: HEX.accent1, quantum: HEX.accent3 };
  s.ladders.forEach((ld, li) => {
    const px = MX + li * (pw + gap), py = TOP, ph = bottom - TOP;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px, y: py, w: pw, h: ph, rectRadius: 0.12, fill: { color: C().background2 }, line: { type: "none" }, objectName: `ladder-bg-${li}` });
    slide.addText(ld.name, { x: px + 0.25, y: py + 0.2, w: pw - 0.5, h: 0.45, fontSize: 17, bold: true, color: C().text2, margin: 0, isTextBox: true, objectName: `ladder-name-${li}` });
    if (ld.sub) slide.addText(runs(ld.sub, { fontSize: 12, color: C().accent6 }), { x: px + 0.25, y: py + 0.65, w: pw - 0.5, h: 0.35, margin: 0, isTextBox: true, objectName: `ladder-sub-${li}` });
    const lx = px + 0.85, lw = pw * 0.48;
    const ybot = py + ph - 0.45, ytop = py + 1.35;
    const emax = Math.max(...ld.levels), emin = Math.min(...ld.levels);
    const yOf = (e) => ybot - ((e - emin) / (emax - emin)) * (ybot - ytop);
    ld.levels.forEach((e, k) => {
      const y = yOf(e);
      const hi = (ld.highlight || []).includes(k);
      slide.addShape(pres.shapes.LINE, { x: lx, y, w: lw, h: 0, line: { color: hi ? HEX.accent2 : HEX.dk2, width: hi ? 4 : 2.5 }, objectName: `level-${li}-${k}` });
      slide.addText(`|${k}⟩`, { x: px + 0.2, y: y - 0.2, w: 0.6, h: 0.4, fontSize: 15, fontFace: EQ_FONT, color: C().text2, margin: 0, align: "right", valign: "middle", isTextBox: true, objectName: `ket-${li}-${k}` });
    });
    (ld.arrows || []).forEach((a, ai) => {
      const y1 = yOf(ld.levels[a.from]), y2 = yOf(ld.levels[a.to]);
      const ax = lx + 0.3 + ai * 0.45;
      const col = toneHex[a.tone || "warn"];
      slide.addShape(pres.shapes.LINE, { x: ax, y: y2 + 0.05, w: 0, h: y1 - y2 - 0.1, line: { color: col, width: 3, beginArrowType: "triangle" }, objectName: `arrow-${li}-${ai}` });
      if (a.label) slide.addText(a.label, { x: lx + lw + 0.12, y: (y1 + y2) / 2 - 0.2, w: pw - (lx - px) - lw - 0.2, h: 0.4, fontSize: 13, bold: true, color: col, margin: 0, valign: "middle", isTextBox: true, objectName: `arrow-label-${li}-${ai}` });
    });
  });
  bulletBox(slide, s.bullets, MX + diagW + 0.45, TOP, CW - diagW - 0.45, bottom - TOP);
  if (s.caption) captionText(slide, s.caption, MX, bottom + 0.05, diagW);
  if (s.callout) callout(slide, s.callout, MX, BOTTOM - 0.7, CW, 0.7);
  if (s.notes) slide.addNotes(s.notes);
};

R.table = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time);
  const head = s.headers.map((h, i) => ({ text: h, options: { bold: true, color: HEX.lt1, fill: { color: i === 0 ? HEX.accent6 : HEX.dk2 }, fontSize: 16, align: i === 0 ? "left" : "center", valign: "middle" } }));
  const body = s.rows.map((r, ri) => r.map((cell, ci) => ({
    text: cell,
    options: { fontSize: 15, color: HEX.dk1, bold: ci === 0, fill: { color: ri % 2 ? "FFFFFF" : HEX.lt2 }, valign: "middle", align: ci === 0 ? "left" : "center", fontFace: ci === 0 ? undefined : undefined },
  })));
  const bottom = s.callout ? BOTTOM - 0.95 : BOTTOM;
  const rowH = Math.min(0.85, (bottom - TOP) / (s.rows.length + 1));
  slide.addTable([head, ...body], {
    x: MX, y: TOP, w: CW, colW: s.colW || [2.4, (CW - 2.4) / 2, (CW - 2.4) / 2], rowH,
    border: { type: "solid", pt: 1, color: "FFFFFF" }, margin: [4, 10, 4, 10], objectName: "table",
  });
  if (s.callout) callout(slide, s.callout, MX, BOTTOM - 0.7, CW, 0.7);
  if (s.notes) slide.addNotes(s.notes);
};

/** 結構圖：約瑟夫森接面（超導體｜絕緣體｜超導體） */
R.junction = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "CONTENT", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time);
  const dx = MX, dw = 6.6, dy = TOP + 1.2, dh = 2.8;
  const insW = 0.55, sW = (dw - insW) / 2;
  const blocks = [
    { x: dx, w: sW, color: HEX.accent1, label: s.left || "超導體 S" },
    { x: dx + sW, w: insW, color: HEX.accent2, label: "" },
    { x: dx + sW + insW, w: sW, color: HEX.accent1, label: s.right || "超導體 S" },
  ];
  blocks.forEach((b, i) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: b.x, y: dy, w: b.w, h: dh, fill: { color: b.color }, line: { color: "FFFFFF", width: 1 }, objectName: `jj-block-${i}` });
    if (b.label) slide.addText(b.label, { x: b.x, y: dy + dh - 0.65, w: b.w, h: 0.5, fontSize: 17, bold: true, color: C().background1, align: "center", margin: 0, isTextBox: true, objectName: `jj-label-${i}` });
  });
  slide.addText(s.middle || "絕緣體 I（約 1 nm）", { x: dx + sW - 1.2, y: dy + dh + 0.12, w: insW + 2.4, h: 0.4, fontSize: 14, bold: true, color: C().accent2, align: "center", margin: 0, isTextBox: true, objectName: "jj-ins-label" });
  // 庫柏電子對：成對的小圓
  const pair = (cx, cy, k) => {
    [0, 0.36].forEach((o, j) => slide.addShape(pres.shapes.OVAL, { x: cx + o, y: cy, w: 0.3, h: 0.3, fill: { color: HEX.lt1 }, line: { color: HEX.dk2, width: 1 }, objectName: `pair-${k}-${j}` }));
  };
  [[0.5, 0.45], [1.6, 1.05], [0.9, 1.45], [2.2, 0.35]].forEach(([ox, oy], k) => pair(dx + ox, dy + oy, `L${k}`));
  [[0.6, 0.6], [1.8, 1.25], [1.1, 0.25]].forEach(([ox, oy], k) => pair(dx + sW + insW + ox, dy + oy, `R${k}`));
  // 穿隧箭頭
  slide.addShape(pres.shapes.LINE, { x: dx + 1.8, y: dy - 0.45, w: dw - 3.6, h: 0, line: { color: HEX.dk2, width: 3, endArrowType: "triangle" }, objectName: "jj-tunnel-arrow" });
  slide.addText(s.arrowLabel || "庫柏電子對成對穿隧", { x: dx, y: dy - 1.0, w: dw, h: 0.45, fontSize: 16, bold: true, color: C().text2, align: "center", margin: 0, isTextBox: true, objectName: "jj-tunnel-label" });
  if (s.symbol) slide.addText(runs(s.symbol, { fontSize: 13, color: C().accent6 }), { x: dx, y: dy + dh + 0.65, w: dw, h: 0.6, align: "center", margin: 0, isTextBox: true, objectName: "jj-symbol" });
  bulletBox(slide, s.bullets, MX + dw + 0.5, TOP, CW - dw - 0.5, BOTTOM - TOP);
  if (s.notes) slide.addNotes(s.notes);
};

R.summary = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "DARK", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time, true);
  const n = s.points.length;
  const gap = 0.18;
  const rh = (BOTTOM - TOP - gap * (n - 1)) / n;
  s.points.forEach((p, i) => {
    const y = TOP + i * (rh + gap);
    slide.addShape(pres.shapes.OVAL, { x: MX, y: y + (rh - 0.6) / 2, w: 0.6, h: 0.6, fill: { color: C().accent2 }, line: { type: "none" }, objectName: `sum-num-bg-${i}` });
    slide.addText(String(i + 1), { x: MX, y: y + (rh - 0.6) / 2, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: C().text2, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: `sum-num-${i}` });
    slide.addText(runs(p, { fontSize: 18, color: C().background1, strongColor: C().accent2 }), { x: MX + 0.85, y, w: CW - 0.85, h: rh, valign: "middle", margin: 0, isTextBox: true, objectName: `sum-text-${i}` });
  });
  if (s.notes) slide.addNotes(s.notes);
};

R.closing = async (pres, s) => {
  const slide = pres.addSlide({ masterName: "DARK", sectionTitle: s.section });
  slide.addText(s.title, { placeholder: "title" });
  timeChip(slide, s.time, true);
  const lw = 6.3;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: TOP, w: lw, h: BOTTOM - TOP, rectRadius: 0.12, fill: { color: "1B3D5E" }, line: { type: "none" }, objectName: "question-bg" });
  slide.addText(s.questionKicker || "討論題", { x: MX + 0.35, y: TOP + 0.3, w: lw - 0.7, h: 0.45, fontSize: 16, bold: true, color: C().accent2, margin: 0, isTextBox: true, objectName: "question-kicker" });
  slide.addText(runs(s.question, { fontSize: 26, bold: true, color: C().background1 }), { x: MX + 0.35, y: TOP + 0.9, w: lw - 0.7, h: 1.5, valign: "top", margin: 0, isTextBox: true, objectName: "question" });
  if (s.prompts) slide.addText(paragraphs(s.prompts, { bullet: { indent: 16 }, paraSpaceAfter: 6 }, { fontSize: 14, color: C().background2 }), { x: MX + 0.35, y: TOP + 2.5, w: lw - 0.7, h: BOTTOM - TOP - 2.7, valign: "top", margin: 0, isTextBox: true, objectName: "question-prompts" });
  const rx = MX + lw + 0.5, rw = CW - lw - 0.5;
  slide.addText(s.refsHead || "延伸觀看與資料來源", { x: rx, y: TOP, w: rw, h: 0.45, fontSize: 16, bold: true, color: C().accent2, margin: 0, isTextBox: true, objectName: "refs-head" });
  slide.addText(paragraphs(s.refs, { bullet: { indent: 16 }, paraSpaceAfter: 8 }, { fontSize: 13, color: C().background1 }), { x: rx, y: TOP + 0.6, w: rw, h: BOTTOM - TOP - 0.6, valign: "top", margin: 0, isTextBox: true, objectName: "refs" });
  if (s.notes) slide.addNotes(s.notes);
};

// ───────────────────────────── 主題寫入（取代 Office 預設色票） ─────────────────────────────
async function applyTheme(file, theme) {
  const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file), { createFolders: false });
  // 去掉資料夾項目（雲端硬碟／共同編輯時可能無法開啟）
  Object.keys(zip.files).filter((f) => zip.files[f].dir).forEach((f) => delete zip.files[f]);
  const part = "ppt/theme/theme1.xml";
  const xml = await zip.file(part).async("string");
  const slots = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"];
  const scheme = `<a:clrScheme name="${theme.name}">` + slots.map((k) => `<a:${k}><a:srgbClr val="${theme.colors[k]}"/></a:${k}>`).join("") + "</a:clrScheme>";
  const out = xml.replace(/<a:clrScheme\b[\s\S]*?<\/a:clrScheme>/, () => scheme).replace(/(<a:(?:theme|fontScheme)\b[^>]*?\bname=")[^"]*"/g, (_, h) => `${h}${theme.name}"`);
  zip.file(part, out, { createFolders: false });
  // pptxgenjs 在同一段落的每個 run 前都寫一個 <a:pPr>（無效 XML，項目符號會消失），只保留段首那一個
  for (const f of Object.keys(zip.files).filter((f) => /^ppt\/(slides|slideLayouts)\/[^/]+\.xml$/.test(f))) {
    const x = await zip.file(f).async("string");
    const fixed = x.replace(/(<\/a:r>)<a:pPr\b[^>]*?(?:\/>|>[\s\S]*?<\/a:pPr>)/g, "$1");
    if (fixed !== x) zip.file(f, fixed, { createFolders: false });
  }
  // pptxgenjs 會在同一頁寫出重複的 shape ID（PowerPoint 開檔時會要求修復），重新依序編號
  for (const f of Object.keys(zip.files).filter((f) => /^ppt\/(slides|slideLayouts|slideMasters|notesSlides|notesMasters)\/[^/]+\.xml$/.test(f))) {
    const x = await zip.file(f).async("string");
    const ids = [...x.matchAll(/<p:cNvPr id="(\d+)"/g)].map((m) => m[1]);
    if (new Set(ids).size === ids.length) continue;
    let k = 0;
    zip.file(f, x.replace(/<p:cNvPr id="\d+"/g, () => `<p:cNvPr id="${++k}"`), { createFolders: false });
  }
  // pptxgenjs 會寫出 PowerPoint 不接受的 crossesAt="autoZero"
  for (const f of Object.keys(zip.files).filter((f) => /^ppt\/charts\/chart\d+\.xml$/.test(f))) {
    const c = await zip.file(f).async("string");
    zip.file(f, c.replace(/<c:crossesAt val="autoZero"\/>/g, '<c:crosses val="autoZero"/>'), { createFolders: false });
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

// ───────────────────────────── 主程式 ─────────────────────────────
async function build(contentPath, outPath) {
  const { meta, slides } = require(path.resolve(contentPath));
  const pres = new pptxgen();
  _pres = pres;
  pres.layout = "LAYOUT_WIDE";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = meta.title;
  pres.subject = meta.subject || meta.title;
  pres.author = meta.author || "";
  defineLayouts(pres, meta);
  let currentSection = null;
  for (const s of slides) {
    if (s.section && s.section !== currentSection) {
      pres.addSection({ title: s.section });
      currentSection = s.section;
    }
    const fn = R[s.type];
    if (!fn) throw new Error(`未知的投影片類型：${s.type}`);
    await fn(pres, s, meta);
  }
  const file = outPath || path.join(__dirname, "output", meta.output || "deck.pptx");
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await pres.writeFile({ fileName: file });
  await applyTheme(file, THEME);
  console.log(`已輸出：${file}（${slides.length} 張）`);
}

if (require.main === module) {
  const [, , content, out] = process.argv;
  if (!content) {
    console.error("用法：node build_deck.js episodes/epXXX.js [輸出.pptx]");
    process.exit(1);
  }
  build(content, out).catch((e) => {
    console.error(e);
    process.exit(1);
  });
}

module.exports = { build, THEME };

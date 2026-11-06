/* 簡報共用版型與元件（兩份簡報共用）：主題、版面、卡片、圖示、方程式框、表格、流程箭頭、3D 場景連結 */
const path = require('path');
const pptxgen = require('pptxgenjs');
const sharp = require('sharp');
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const Fa = require('react-icons/fa');

function makeDeck(opt) {
  const THEME = {
    name: 'Quantum Copper',
    headFontFace: 'Microsoft JhengHei',
    bodyFontFace: 'Microsoft JhengHei',
    colors: {
      dk1: '1A1F2B', lt1: 'FFFFFF', dk2: '0B1424', lt2: 'F1F4F8',
      accent1: 'C8862A', accent2: '1C9DB0', accent3: '3B6FD8', accent4: 'D9534F', accent5: '2E9E5B', accent6: '7A8699',
      hlink: '1C9DB0', folHlink: '8A5CD0',
    },
  };
  const HEX = THEME.colors;

  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE'; // 13.333 × 7.5 in
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = opt.title;
  pres.subject = opt.subject;
  pres.author = '技術分享';
  const C = pres.SchemeColor;

  /* ---------------- 版面（layouts） ---------------- */
  const FOOT = opt.footer;
  pres.defineSlideMaster({
    title: 'TITLE_DARK',
    background: { color: HEX.dk2 },
    objects: [
      { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 1.9, w: 6.9, h: 2.1, fontSize: 32, bold: true, color: C.background1, valign: 'bottom', align: 'left', margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 4.2, w: 6.9, h: 1.2, fontSize: 18, color: C.accent1, valign: 'top', align: 'left', margin: 0 }, text: '' } },
    ],
  });
  pres.defineSlideMaster({
    title: 'SECTION_DARK',
    background: { color: HEX.dk2 },
    objects: [
      { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 2.75, w: 7.2, h: 1.1, fontSize: 40, bold: true, color: C.background1, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.95, w: 7.2, h: 1.6, fontSize: 18, color: 'C9D3E3', valign: 'top', align: 'left', margin: 0 }, text: '' } },
      { text: { text: FOOT, options: { x: 0.7, y: 6.9, w: 6, h: 0.3, fontSize: 10, color: '8A97AB', margin: 0 } } },
    ],
    slideNumber: { x: 12.2, y: 6.9, w: 0.6, h: 0.3, fontSize: 10, color: '8A97AB', align: 'right' },
  });
  pres.defineSlideMaster({
    title: 'CONTENT',
    background: { color: HEX.lt1 },
    margin: [0.5, 0.6, 0.6, 0.6],
    objects: [
      { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.35, w: 9.3, h: 0.8, fontSize: 30, bold: true, color: C.text1, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
      { text: { text: FOOT, options: { x: 0.6, y: 7.0, w: 6, h: 0.3, fontSize: 10, color: HEX.accent6, margin: 0 } } },
    ],
    slideNumber: { x: 12.13, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: HEX.accent6, align: 'right' },
  });

  /* ---------------- 共用元件 ---------------- */
  const shadow = () => ({ type: 'outer', color: '000000', opacity: 0.12, blur: 6, offset: 2, angle: 90 });
  let objN = 0; const oname = (p) => `${p}_${++objN}`;

  async function iconPng(Icon, color = '#FFFFFF', size = 256) {
    const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Icon, { color, size }));
    const buf = await sharp(Buffer.from(svg)).resize(size, size).png().toBuffer();
    return 'image/png;base64,' + buf.toString('base64');
  }
  const ICONS = {};
  async function loadIcons() {
    const list = { atom: Fa.FaAtom, clock: Fa.FaClock, wave: Fa.FaWaveSquare, target: Fa.FaBullseye, bolt: Fa.FaBolt, snow: Fa.FaSnowflake,
      chip: Fa.FaMicrochip, signal: Fa.FaSignal, eye: Fa.FaEye, layer: Fa.FaLayerGroup, random: Fa.FaRandom, bug: Fa.FaBug, magnet: Fa.FaMagnet,
      fire: Fa.FaFire, satellite: Fa.FaSatelliteDish, link: Fa.FaLink, sliders: Fa.FaSlidersH, filter: Fa.FaFilter, redo: Fa.FaRedo, brain: Fa.FaBrain,
      stream: Fa.FaStream, shield: Fa.FaShieldAlt, tachometer: Fa.FaTachometerAlt, cubes: Fa.FaCubes, play: Fa.FaPlay, check: Fa.FaCheck, search: Fa.FaSearch,
      volume: Fa.FaVolumeUp, cogs: Fa.FaCogs, ruler: Fa.FaRulerHorizontal };
    for (const [k, I] of Object.entries(list)) ICONS[k] = await iconPng(I);
  }

  function card(slide, x, y, w, h, fill = C.background2) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: fill, width: 0 }, shadow: shadow(), objectName: oname('card') });
  }
  function iconCircle(slide, key, x, y, d = 0.62, color = C.accent1) {
    slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color, width: 0 }, objectName: oname('icon-bg') });
    const p = d * 0.25;
    slide.addImage({ data: ICONS[key], x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, altText: key, objectName: oname('icon') });
  }
  function numCircle(slide, n, x, y, d = 0.55, color = C.accent1) {
    slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color, width: 0 }, objectName: oname('num-bg') });
    slide.addText(String(n), { x, y, w: d, h: d, fontSize: 16, bold: true, color: C.background1, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: oname('num') });
  }
  /* 把簡易標記轉成 runs：_{下標}、^{上標}、**粗體** */
  function runs(str, base = {}) {
    const out = []; let i = 0; let buf = '';
    const flush = () => { if (buf) { out.push({ text: buf, options: { ...base } }); buf = ''; } };
    while (i < str.length) {
      if ((str[i] === '_' || str[i] === '^') && str[i + 1] === '{') {
        flush(); const j = str.indexOf('}', i);
        out.push({ text: str.slice(i + 2, j), options: { ...base, [str[i] === '_' ? 'subscript' : 'superscript']: true } });
        i = j + 1;
      } else if (str.startsWith('**', i)) {
        flush(); const j = str.indexOf('**', i + 2);
        out.push(...runs(str.slice(i + 2, j), { ...base, bold: true }));
        i = j + 2;
      } else { buf += str[i++]; }
    }
    flush();
    return out;
  }
  /* 多段落文字：每段可為字串或 {t, bullet, color, size, bold, space} */
  function para(slide, items, x, y, w, h, o = {}) {
    const arr = [];
    items.forEach((it, k) => {
      const d = typeof it === 'string' ? { t: it } : it;
      const base = { fontSize: d.size || o.size || 15, color: d.color || o.color || C.text1, bold: d.bold };
      const rs = runs(d.t, base);
      rs.forEach((r, j) => {
        if (d.bullet || (o.bullet && d.bullet !== false)) r.options.bullet = { indent: 14 };
        r.options.paraSpaceAfter = d.space ?? o.space ?? 6;
        if (j === rs.length - 1 && k < items.length - 1) r.options.breakLine = true;
        arr.push(r);
      });
    });
    slide.addText(arr, { x, y, w, h, valign: o.valign || 'top', margin: o.margin ?? 0, isTextBox: true, lineSpacingMultiple: o.lsm || 1.12, fit: 'none', objectName: oname(o.name || 'text'), align: o.align || 'left' });
  }
  /* 方程式框 */
  function eqBox(slide, lines, x, y, w, h, o = {}) {
    card(slide, x, y, w, h, o.fill || 'FBF4E8');
    const arr = [];
    lines.forEach((ln, k) => {
      const d = typeof ln === 'string' ? { t: ln } : ln;
      const rs = runs(d.t, { fontSize: d.size || o.size || 20, color: d.color || C.text1, fontFace: d.cjk ? undefined : 'Cambria' });
      rs.forEach((r, j) => { if (j === rs.length - 1 && k < lines.length - 1) r.options.breakLine = true; if (j === 0) r.options.paraSpaceAfter = 4; arr.push(r); });
    });
    slide.addText(arr, { x: x + 0.2, y: y + 0.1, w: w - 0.4, h: h - 0.2, align: o.align || 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: oname('equation') });
  }
  async function fitImage(slide, file, x, y, w, h, o = {}) {
    let input = file; let meta;
    if (o.crop) { input = await sharp(file).extract(o.crop).toBuffer(); }
    meta = await sharp(input).metadata();
    const ar = meta.width / meta.height; let iw = w, ih = w / ar;
    if (ih > h) { ih = h; iw = h * ar; }
    const ix = x + (o.alignX === 'left' ? 0 : o.alignX === 'right' ? w - iw : (w - iw) / 2);
    const iy = y + (o.alignY === 'top' ? 0 : (h - ih) / 2);
    const opts = { x: ix, y: iy, w: iw, h: ih, altText: o.alt || path.basename(file), objectName: oname('image') };
    if (o.crop) opts.data = 'image/' + (meta.format === 'jpeg' ? 'jpeg' : 'png') + ';base64,' + input.toString('base64'); else opts.path = file;
    slide.addImage(opts);
    return { x: ix, y: iy, w: iw, h: ih };
  }
  function caption(slide, text, x, y, w, o = {}) {
    slide.addText(runs(text), { x, y, w, h: 0.32, fontSize: 11, color: o.color || C.accent6, italic: true, margin: 0, align: o.align || 'left', isTextBox: true, objectName: oname('caption') });
  }
  const SCENES = opt.scenes;
  function animPill(slide, id, x = 10.15, y = 0.47) {
    const [n, name] = SCENES[id];
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.6, h: 0.48, rectRadius: 0.24, fill: { color: C.accent2 }, line: { color: C.accent2, width: 0 }, objectName: oname('anim-pill') });
    slide.addText([{ text: `▶ 3D 場景 ${n}：${name}`, options: { hyperlink: { url: `${opt.animRel}#${id}`, tooltip: '開啟 3D 動畫（瀏覽器）' }, color: C.background1, bold: true } }],
      { x, y, w: 2.6, h: 0.48, fontSize: 12, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: oname('anim-link') });
  }
  function table(slide, rows, x, y, w, colW, o = {}) {
    const fs_ = o.size || 13;
    const data = rows.map((r, i) => r.map((c) => {
      const isHead = i === 0;
      return { text: runs(String(c), {}), options: { bold: isHead, color: isHead ? C.background1 : C.text1, fill: { color: isHead ? (o.head || C.text2) : (i % 2 ? C.background1 : C.background2) }, fontSize: isHead ? fs_ : fs_, valign: 'middle', margin: [4, 6, 4, 6] } };
    }));
    slide.addTable(data, { x, y, w, colW, border: { type: 'solid', pt: 0.5, color: 'D5DBE5' }, rowH: o.rowH || 0.42, autoPage: false, objectName: oname('table') });
  }
  function chevrons(slide, steps, x, y, w, h, colors) {
    const n = steps.length; const gap = 0.06; const sw = (w - gap * (n - 1)) / n;
    steps.forEach((s, i) => {
      const col = colors ? colors[i % colors.length] : C.accent2;
      slide.addShape(i === 0 ? pres.shapes.PENTAGON : pres.shapes.CHEVRON, { x: x + i * (sw + gap), y, w: sw, h, fill: { color: col }, line: { color: col, width: 0 }, objectName: oname('flow-step') });
      slide.addText(runs(s, {}), { x: x + i * (sw + gap) + (i ? 0.3 : 0.08), y, w: sw - (i ? 0.45 : 0.35), h, fontSize: 12, bold: true, color: C.background1, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: oname('flow-text') });
    });
  }


  /* 箭頭線：由 (x1,y1) 指向 (x2,y2)。PowerPoint 不接受負的寬高，方向改用 flipH / flipV 表示 */
  function link(slide, x1, y1, x2, y2, o = {}) {
    const line = { color: o.color || HEX.accent6, width: o.width || 1.75, endArrowType: o.end === false ? undefined : 'triangle' };
    if (o.both) line.beginArrowType = 'triangle';
    if (o.dash) line.dashType = o.dash;
    slide.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), flipH: x2 < x1, flipV: y2 < y1, line, objectName: oname(o.name || 'link') });
  }

  return { pres, C, HEX, THEME, SCENES, link, shadow, oname, ICONS, loadIcons, card, iconCircle, numCircle, runs, para, eqBox, fitImage, caption, animPill, table, chevrons };
}
module.exports = { makeDeck };

/* 產生簡報：超導量子電腦的周邊系統與整合
 * 用法：node build_peripherals.js
 * 輸出：../QC_Peripheral_Systems_Talk.pptx 與 ../../speech/周邊系統演講稿.md（由同一份講者備註生成）
 * 數值來源見「參考資料」頁與 docs/周邊系統連接與啟動指南.md
 */
const fs = require('fs');
const path = require('path');
const { applyTheme } = require('./apply_theme');
const { makeDeck } = require('./deck_lib');

const ROOT = path.resolve(__dirname, '..');
const FIG = path.join(ROOT, 'figures');
const OUT = path.join(ROOT, 'QC_Peripheral_Systems_Talk.pptx');
const SPEECH = path.resolve(ROOT, '..', 'speech', '周邊系統演講稿.md');
const SCENES = {
  overview: [1, '系統全景'], pulsetube: [2, '脈衝管冷卻'], dilution: [3, '稀釋冷凍原理'], cooldown: [4, '降溫流程'], wiring: [5, '低溫佈線'],
  electronics: [6, '控制電子學'], software: [7, '軟體堆疊'], infra: [8, '機房基礎設施'], monitor: [9, '監控與聯鎖'], bringup: [10, '啟動與校準'],
};
const D = makeDeck({ title: '超導量子電腦：周邊系統與整合', subject: '稀釋冷凍、佈線、控制電子、軟體與機房基礎設施', footer: '超導量子電腦 · 周邊系統與整合', scenes: SCENES, animRel: '../animations/peripherals.html' });
const { pres, C, HEX, THEME, link, loadIcons, card, iconCircle, numCircle, runs, para, eqBox, fitImage, caption, animPill, table, chevrons, shadow, oname } = D;
const IMG = (n) => path.join(FIG, '3d_periph', n + '.jpg');
const CROP = {
  overview: { left: 200, top: 180, width: 2150, height: 1100 }, pulsetube: { left: 380, top: 200, width: 1750, height: 1050 },
  dilution: { left: 860, top: 90, width: 900, height: 1270 }, cooldown: { left: 760, top: 40, width: 1150, height: 1240 },
  wiring: { left: 680, top: 0, width: 1050, height: 1340 }, electronics: { left: 380, top: 220, width: 1850, height: 1050 },
  software: { left: 420, top: 200, width: 1950, height: 1050 }, infra: { left: 330, top: 260, width: 1950, height: 1150 },
  monitor: { left: 560, top: 300, width: 1500, height: 860 }, bringup: { left: 330, top: 300, width: 2000, height: 800 },
};
const pic = (s, id, x, y, w, h, o = {}) => fitImage(s, IMG(o.file || id), x, y, w, h, { crop: CROP[id], alt: `3D 場景：${SCENES[id][1]}`, ...o });
const CHART_FONT = { catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', legendFontFace: '+mn-lt', titleFontFace: '+mn-lt', dataLabelFontFace: '+mn-lt', valAxisTitleFontFace: '+mn-lt', catAxisTitleFontFace: '+mn-lt' };
const CHART_BASE = () => ({ ...CHART_FONT, catAxisLabelColor: '4A5468', valAxisLabelColor: '4A5468', catAxisLabelFontSize: 11, valAxisLabelFontSize: 11, valGridLine: { color: 'E3E7EE', size: 0.75 }, catGridLine: { style: 'none' }, legendFontSize: 11, titleFontSize: 13, titleColor: '1A1F2B' });

/* ---------- 共用計算：佈線熱負載、降溫模型（與 3D 動畫相同） ---------- */
const W = { stages: ['50 K', '4 K', 'Still', 'Cold plate', 'MXC'], passive: [45e-3, 1e-3, 3e-6, 0.4e-6, 0.015e-6], attDiss: [0, 2e-6, 0, 2e-8, 2e-9], hemt: 5e-3, cool: [30, 1.5, 40e-3, 200e-6, 19e-6] };
const lineCount = (n) => ({ xy: n, z: n, rin: Math.ceil(n / 6), rout: Math.ceil(n / 6), pump: Math.ceil(n / 6) });
const heatPct = (n) => { const c = lineCount(n); const nc = c.xy + c.z + c.rin + c.rout + c.pump; return W.stages.map((_, i) => (100 * (nc * W.passive[i] + (c.xy + c.rin + c.pump) * W.attDiss[i] + (i === 1 ? c.rout * W.hemt : 0))) / W.cool[i]); };
const TMODEL = (t) => {
  const pre = (tau, Tend, t0 = 2) => (t < t0 ? 300 : Tend + (300 - Tend) * Math.exp(-(t - t0) / tau));
  const T50 = pre(5.5, 45), T4 = pre(7.5, 3.4, 2.3); const Tl = pre(8.5, 4.2, 3); const L = [Tl, Tl, Tl];
  if (t > 25) L.fill(Math.exp(Math.log(Tl) + (Math.log(1.0) - Math.log(Tl)) * Math.min(1, (t - 25) / 2.5)));
  if (t > 27.5) { const u = t - 27.5; L[0] = 0.8 + 0.2 * Math.exp(-u / 0.6); L[1] = 0.1 + 0.9 * Math.exp(-u / 1.2); L[2] = 0.01 + 0.99 * Math.exp(-u / 1.0); }
  return [T50, T4, ...L];
};

/* ---------------- 投影片內容 ---------------- */
const SLIDES = [];
const S = (o) => SLIDES.push(o);
const H = (s, t) => s.addText(runs(t), { placeholder: 'title' });
const sec = (num, title, body, img, col = C.accent1) => async (s) => {
  s.addText(num, { x: 0.7, y: 1.3, w: 3, h: 1.4, fontSize: 80, bold: true, color: col, margin: 0, isTextBox: true, fontFace: 'Arial' });
  s.addText(runs(title), { placeholder: 'title' }); s.addText(runs(body), { placeholder: 'body' });
  if (img) await pic(s, img, 8.0, 0.9, 5.0, 5.6);
};
const sub = (s, t, x, y, w, col = C.text1, size = 18) => s.addText(runs(t), { x, y, w, h: 0.45, fontSize: size, bold: true, color: col, margin: 0, isTextBox: true, valign: 'middle' });

// ===== 開場 =====
S({ sec: '開場', layout: 'TITLE_DARK', title: '量子電腦的周邊系統：讓 10 mK 的晶片真正運轉', min: 1.5,
  async render(s) {
    s.addText('量子電腦的周邊系統：\n讓 10 mK 的晶片真正運轉', { placeholder: 'title' });
    s.addText('稀釋冷凍 · 低溫佈線 · 控制電子 · 軟體 · 機房基礎設施 · 系統整合', { placeholder: 'body' });
    await pic(s, 'dilution', 8.6, 0.6, 4.2, 6.2);
    s.addText('技術分享（續篇）· 搭配互動 3D 動畫（animations/peripherals.html）', { x: 0.7, y: 6.55, w: 7.0, h: 0.4, fontSize: 13, color: 'A8B4C6', margin: 0, isTextBox: true });
  },
  notes: `大家好，上一次我們談了量子電腦的核心：約瑟夫森接面和微波讀取。今天是續篇，要談的是「晶片以外的一切」——讓這顆在 10 mK 下工作的晶片真正能夠運轉的所有周邊系統。
很多人第一次看到量子電腦的照片，看到的是那個金色的「吊燈」，其實那只是稀釋冷凍機的內部。一台能運作的超導量子電腦，還需要壓縮機、冷卻水、氣體處理系統、上百條微波線、一整櫃控制電子、時脈同步、軟體、電力和監控。今天的目標是把這些設備一一說清楚，並且說明它們怎麼連接、怎麼啟動，最後讓量子電腦可以正常運行。
同樣搭配 3D 動畫，這次的動畫在 animations/peripherals.html，共 10 個場景。`,
});
S({ sec: '開場', title: '今日議程', min: 1.5,
  async render(s) {
    H(s, '今日議程');
    const items = [['01', '低溫系統', '稀釋冷凍機、脈衝管與壓縮機、稀釋原理、氣體處理、降溫流程', C.accent3],
      ['02', '低溫佈線與封裝', '線路種類與數量、衰減濾波、熱負載預算、纜線、屏蔽', C.accent2],
      ['03', '控制電子學', '架構、外差與直接合成、時脈同步、即時回饋、直流源', C.accent1],
      ['04', '軟體與運作', '軟體堆疊、啟動校準、監控聯鎖、故障處置', C.accent5],
      ['05', '機房基礎設施', '電力與 UPS、冷卻水與環境、防振接地、配置', C.accent4],
      ['06', '系統整合', '連接清單、從零到上線的檢查表、規模化趨勢', C.accent6]];
    items.forEach(([n, t, d, col], i) => {
      const x = 0.6 + (i % 3) * 4.1, y = 1.45 + Math.floor(i / 3) * 2.6;
      card(s, x, y, 3.9, 2.35);
      s.addText(n, { x: x + 0.25, y: y + 0.15, w: 1.2, h: 0.75, fontSize: 36, bold: true, color: col, margin: 0, isTextBox: true, fontFace: 'Arial' });
      sub(s, t, x + 1.35, y + 0.3, 2.4);
      para(s, [d], x + 0.25, y + 1.05, 3.45, 1.2, { size: 13.5, color: '4A5468' });
    });
    s.addText('全程約 90 分鐘（含 Q&A）· 搭配 10 個 3D 場景 · 另附《周邊系統連接與啟動指南》', { x: 0.6, y: 6.6, w: 12, h: 0.35, fontSize: 13, color: C.accent6, italic: true, margin: 0, isTextBox: true });
  },
  notes: `今天分成六個部分。第一部分是低溫系統，這是整個周邊最大、最貴、也最需要了解的部分；第二部分是低溫佈線與封裝，也就是訊號怎麼從室溫進到 10 mK；第三部分是室溫控制電子學；第四部分是軟體與日常運作；第五部分是機房基礎設施，包括電力、冷卻水、防振和接地；最後第六部分把所有東西串起來：一張完整的連接清單，以及一份從零到上線的檢查表。
另外我也整理了一份書面的《周邊系統連接與啟動指南》，放在 repo 的 docs 資料夾，會後可以當作實際建置時的參考。`,
});
S({ sec: '開場', title: '量子電腦 ≠ 量子晶片', anim: 'overview', min: 3,
  async render(s) {
    H(s, '量子電腦 ≠ 量子晶片'); animPill(s, 'overview');
    await pic(s, 'overview', 0.6, 1.4, 7.4, 4.9, { alignX: 'left' });
    caption(s, '3D 場景 1：機房全景，可切換各類連接（氦氣、冷卻水、混合氣、真空、微波、資料、電力）', 0.6, 6.35, 7.4);
    const sys = [['snow', '低溫系統', '稀釋冷凍機、脈衝管、壓縮機、GHS', C.accent3], ['stream', '低溫佈線', '同軸線、衰減器、濾波器、放大器', C.accent2], ['chip', '控制電子', 'AWG、LO、ADC、FPGA、DC 源、時脈', C.accent1], ['cogs', '軟體', '編譯、脈衝、校準、監控', C.accent5], ['bolt', '機房設施', '電力、UPS、冷卻水、空調、接地', C.accent4]];
    sys.forEach(([ic, t, d, col], i) => {
      const y = 1.45 + i * 1.02;
      iconCircle(s, ic, 8.3, y + 0.05, 0.6, col);
      sub(s, t, 9.05, y, 3.7, C.text1, 16);
      s.addText(d, { x: 9.05, y: y + 0.42, w: 3.7, h: 0.4, fontSize: 12.5, color: '4A5468', margin: 0, isTextBox: true });
    });
  },
  notes: `這頁的重點是一句話：量子電腦不等於量子晶片。
【切換到 3D 場景 1】這是一間典型的超導量子電腦機房。中間是稀釋冷凍機，量子晶片在它最底部；右邊是脈衝管的氦壓縮機、氣體處理系統和混合氣儲存槽，最右邊是冷卻水機；左邊是控制電子機櫃、控制電腦、UPS 和配電盤。
面板上的按鈕可以切換不同類型的連接：綠色是脈衝管的高低壓氦氣，藍色是冷卻水，紫色是稀釋循環的混合氣，灰色是真空，橘色是微波和直流線，青色是資料和時脈，黃色是電力。按「只看冷卻相關」或「只看訊號相關」可以把兩大類分開來看。
右邊把這些設備歸納成五大子系統。接下來每一部分會深入一個子系統，最後再回到這張全景圖，把連接整理成清單。`,
});
S({ sec: '開場', title: '系統方塊圖：誰連到誰', min: 3,
  async render(s) {
    H(s, '系統方塊圖：誰連到誰');
    const box = (x, y, w, h, t, col, sz = 13) => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: col }, line: { color: col, width: 0 }, shadow: shadow(), objectName: oname('block') });
      s.addText(runs(t), { x, y, w, h, fontSize: sz, bold: true, color: C.background1, align: 'center', valign: 'middle', margin: 2, isTextBox: true, objectName: oname('block-text') });
    };
    const ln = (x, y, w, h, col, o = {}) => link(s, x, y, x + w, y + h, { color: col, width: 2.25, dash: o.dash, both: o.both, name: 'link' });
    // 中央
    box(5.35, 2.55, 2.6, 2.2, '稀釋冷凍機\n（量子晶片 10 mK）', C.text2, 15);
    // 左：控制
    box(0.6, 1.5, 2.3, 0.75, '雲端 / 使用者', C.accent6);
    box(0.6, 2.75, 2.3, 0.75, '控制電腦 / 軟體', C.accent5);
    box(0.6, 4.0, 2.3, 0.95, '控制電子機櫃\nAWG · LO · ADC · FPGA', C.accent1);
    box(0.6, 5.4, 2.3, 0.75, '銣鐘 10 MHz 參考', C.accent1);
    box(3.1, 5.4, 2.0, 0.75, '溫控器 / 監控', C.accent6);
    // 右：冷卻
    box(10.4, 1.5, 2.3, 0.75, '氦壓縮機', C.accent5);
    box(10.4, 2.75, 2.3, 0.75, '冷卻水機', C.accent3);
    box(10.4, 4.0, 2.3, 0.95, '氣體處理系統 GHS\n泵 · 閥 · 冷阱', '8A5CD0');
    box(10.4, 5.4, 2.3, 0.75, '混合氣儲存槽', '8A5CD0');
    box(5.35, 0.95 + 0.4, 2.6, 0.6, 'UPS / 配電盤', C.accent4);
    // 連線
    ln(1.75, 2.25, 0, 0.5, C.accent2, { both: true });
    ln(1.75, 3.5, 0, 0.5, C.accent2, { both: true });
    ln(1.75, 5.4, 0, -0.45, C.accent1, {});
    ln(2.9, 4.45, 2.45, -0.5, 'FF9F43', {});
    ln(2.9, 3.12, 2.45, 0, C.accent2, { dash: 'dash' });
    ln(4.1, 5.4, 1.25, -0.9, C.accent6, { both: true });
    ln(10.4, 1.88, -2.45, 1.0, C.accent5, { both: true });
    ln(11.55, 2.75, 0, -0.5, C.accent3, { both: true });
    ln(10.4, 4.45, -2.45, -0.3, '8A5CD0', { both: true });
    ln(11.55, 4.95, 0, 0.45, '8A5CD0', { both: true });
    ln(6.65, 1.95, 0, 0.6, C.accent4, {});
    // 圖例
    const leg = [['微波 / DC', 'FF9F43'], ['資料 / 時脈', HEX.accent2], ['氦氣（脈衝管）', HEX.accent5], ['冷卻水', HEX.accent3], ['混合氣 / 真空', '8A5CD0'], ['電力', HEX.accent4]];
    leg.forEach(([t, c], i) => { const x = 5.3 + (i % 2) * 1.6, y = 5.05 + Math.floor(i / 2) * 0.38; s.addShape(pres.shapes.RECTANGLE, { x, y: y + 0.1, w: 0.22, h: 0.14, fill: { color: c }, line: { color: c, width: 0 }, objectName: oname('legend') }); s.addText(t, { x: x + 0.28, y, w: 1.35, h: 0.34, fontSize: 11, color: '4A5468', margin: 0, isTextBox: true }); });
    caption(s, '完整的接頭、介質與規格見第六部分「系統連接清單」', 0.6, 6.55, 12);
  },
  notes: `這張方塊圖把全景圖抽象化，方便記憶誰連到誰。
中間是稀釋冷凍機。左半邊是「訊號側」：使用者透過雲端把程式送給控制電腦，控制電腦驅動控制電子機櫃，機櫃用大量微波和直流線連到冷凍機頂板；所有儀器都鎖在同一個銣鐘的 10 MHz 參考時脈上；溫控器和監控系統讀取冷凍機內各級的溫度計。
右半邊是「冷卻側」：氦壓縮機用一對高低壓軟管連到冷凍機頂部的脈衝管冷頭，壓縮機的熱由冷卻水機帶走；氣體處理系統 GHS 透過抽氣管和回流管和冷凍機交換混合氣，不用時把混合氣存回儲存槽。
上方的 UPS 和配電盤供電給所有設備。這張圖的每一條線，在最後的連接清單裡都會對應到具體的接頭和規格。`,
});

// ===== 01 低溫系統 =====
S({ sec: '01 低溫系統', layout: 'SECTION_DARK', title: '01 低溫系統', min: 0.5, render: sec('01', '低溫系統', '稀釋冷凍機 · 脈衝管 · 壓縮機 · 稀釋原理 · 氣體處理 · 降溫', 'cooldown', C.accent3),
  notes: `第一部分：低溫系統。` });
S({ sec: '01 低溫系統', title: '為什麼要 10 mK？', min: 2,
  async render(s) {
    H(s, '為什麼要 10 mK？');
    const st = [['5 GHz', '量子位元能量 hf ≈ 20 μeV ≈ 240 mK × k_{B}', C.accent1], ['10 mK', 'k_{B}T 只有 hf 的 1/24 → 熱激發 ≈ e^{−24}', C.accent3], ['2Δ ≈ 360 μeV', '鋁超導能隙；溫度越低，準粒子越少', C.accent2]];
    st.forEach(([v, l, col], i) => {
      const x = 0.6 + i * 4.1; card(s, x, 1.5, 3.9, 2.1);
      s.addText(v, { x, y: 1.6, w: 3.9, h: 0.95, fontSize: 34, bold: true, color: col, align: 'center', valign: 'middle', margin: 0, isTextBox: true, fontFace: 'Arial' });
      s.addText(runs(l), { x: x + 0.2, y: 2.6, w: 3.5, h: 0.85, fontSize: 13.5, color: '4A5468', align: 'center', margin: 0, isTextBox: true });
    });
    sub(s, '溫度不夠低會發生什麼？', 0.6, 3.95, 6, C.accent4);
    para(s, ['量子位元有殘留熱激發 → 初始化錯誤', '讀取腔中有熱光子 → 量子位元失相（T_{2} 下降）', '準粒子增加 → 穿隧過 JJ 帶走能量（T_{1} 下降）', '超導體（Al，T_{c} ≈ 1.2 K）根本無法超導'], 0.6, 4.45, 6.0, 2.3, { size: 15, bullet: true, space: 8 });
    card(s, 7.0, 3.95, 5.75, 2.75, 'FBF4E8');
    para(s, [{ t: '溫度是「階梯」降下來的', bold: true, color: C.accent1, size: 17 }, '300 K → 50 K → 4 K：脈衝管（機械式冷凍）', '4 K → 0.9 K → 100 mK → 10 mK：稀釋循環', '每一級都是「熱錨定點」：線路、屏蔽、元件都要在每一級散熱'], 7.25, 4.1, 5.3, 2.5, { size: 14.5, space: 8 });
  },
  notes: `先回答一個基本問題：為什麼要 10 mK？
5 GHz 的量子位元，一個光子的能量約 20 微電子伏特，相當於 240 mK 的熱能。在 10 mK 下，熱能只有它的 24 分之一，熱激發機率是 e 的負 24 次方，幾乎為零。如果溫度只有 100 mK，熱激發就會到百分之一的量級，初始化就會出錯。
溫度不夠低的後果有四個：量子位元有殘留熱激發；讀取腔裡有熱光子造成失相；準粒子變多讓 T1 下降；更極端的是，鋁的臨界溫度只有 1.2 K，溫度太高根本不會超導。
右邊的重點是：溫度是一階一階降下來的。上半段 300 K 到 4 K 由脈衝管這種機械式冷凍機負責，下半段 4 K 到 10 mK 由稀釋循環負責。每一級都是熱錨定點，這個觀念在佈線部分會一再出現。`,
});
S({ sec: '01 低溫系統', title: '稀釋冷凍機：各級溫度與冷卻功率', min: 3,
  async render(s) {
    H(s, '稀釋冷凍機：各級溫度與冷卻功率');
    table(s, [['溫層', '量測溫度', '冷卻功率（量測）', '主要用途'],
      ['50 K 級', '~35 K', '30 W @ 45 K', '輻射屏蔽、纜線第一次熱錨定'],
      ['4 K 級', '~2.85 K', '1.5 W @ 4.2 K', 'HEMT 放大器、衰減器、凝結混合氣'],
      ['Still', '~0.88 K', '40 mW @ 1.2 K', '³He 蒸發、熱錨定'],
      ['Cold plate', '~82 mK', '200 μW @ 140 mK', '衰減器、環行器'],
      ['MXC', '~6–10 mK', '19 μW @ 20 mK', '量子晶片、TWPA、最後一級濾波'],
    ], 0.6, 1.45, 7.6, [1.5, 1.4, 2.0, 2.7], { size: 13, rowH: 0.52 });
    caption(s, '量測值：Krinner et al., EPJ Quantum Technol. 6, 2 (2019)（Bluefors XLD）', 0.6, 4.65, 7.6);
    table(s, [['機型', '20 mK', '100 mK', 'MXC 板'], ['Bluefors LD450', '≥ 14 μW', '≥ 450 μW', '294 mm'], ['Bluefors XLD1000sl', '> 30 μW', '> 1000 μW', '500 mm'], ['Oxford ProteoxMX', '> 12 μW', '> 450 μW', '360 mm'], ['Bluefors KIDE', '> 90 μW', '> 3000 μW', '1.6 m²']],
      0.6, 5.05, 7.6, [2.6, 1.6, 1.7, 1.7], { size: 12, rowH: 0.36, head: C.accent3 });
    card(s, 8.5, 1.45, 4.25, 5.3);
    para(s, [{ t: '觀念', bold: true, color: C.accent1, size: 17 }, '越往下，冷卻功率以**數量級**遞減：30 W → 1.5 W → 40 mW → 200 μW → 19 μW', 'MXC 只有約 20 μW —— 一顆 LED 指示燈的千分之一', '所以任何進到低溫的線、元件、輻射都必須精打細算', '基溫約 10 mK；空機降溫約 1–2 天'], 8.75, 1.6, 3.8, 5.0, { size: 14.5, space: 10 });
  },
  notes: `這頁是稀釋冷凍機最重要的一張表。上表是 ETH Zurich 的 Krinner 等人在 2019 年量測的一台 Bluefors XLD：50 K 級實際約 35 K，在 45 K 時有 30 W 的冷卻功率；4 K 級約 2.85 K，1.5 W；Still 約 0.88 K，40 mW；Cold plate 約 82 mK，200 μW；混合腔 MXC 約 6 mK，20 mK 時只有 19 μW。
下表是幾款商用機型的規格比較：入門的 LD450 在 20 mK 有 14 μW，大型的 XLD1000sl 超過 30 μW，最新的 KIDE 平台超過 90 μW，號稱可支援上千顆量子位元。
右邊的觀念最重要：越往下，冷卻功率以數量級遞減。MXC 只有約 20 微瓦，大概是一顆 LED 指示燈功率的千分之一。所以所有進到低溫的東西——線路、元件、甚至紅外輻射——都要精打細算，這就是第二部分「熱負載預算」的由來。`,
});
S({ sec: '01 低溫系統', title: '脈衝管冷卻器與氦壓縮機', anim: 'pulsetube', min: 3,
  async render(s) {
    H(s, '脈衝管冷卻器與氦壓縮機'); animPill(s, 'pulsetube');
    await pic(s, 'pulsetube', 0.6, 1.4, 6.3, 4.4, { alignX: 'left' });
    caption(s, '3D 場景 2：旋轉閥切換高低壓、蓄冷器形成溫度梯度（粒子顏色 = 溫度）', 0.6, 5.85, 6.3);
    table(s, [['規格', 'PT415', 'PT420'], ['冷卻功率 @ 4.2 K', '1.5 W', '2.0 W'], ['冷卻功率 @ 45 K', '40 W', '55 W'], ['壓縮機', 'CPA1110', 'CPA1114'], ['耗電（60 Hz）', '10.7 kW', '12.5 kW'], ['冷卻水', '11.5 L/min，≤ 27 °C', '依型號'], ['氦氣工作壓力', '15–17 bar（靜態）', '—']], 7.2, 1.45, 5.55, [2.0, 1.85, 1.7], { size: 12.5, rowH: 0.43 });
    para(s, ['旋轉閥約 **1.4 Hz** 切換高/低壓；冷端**無活動零件**', '**遠端馬達**可降低振動，但約損失 20 % 冷卻功率'], 7.2, 4.65, 5.55, 1.2, { size: 13.5, bullet: true, space: 6 });
    caption(s, '資料：Bluefors / Cryomech PT415、PT420 規格頁；遠端馬達：CUORE（arXiv:1904.05745）', 7.2, 5.95, 5.55);
  },
  notes: `稀釋冷凍機的上半段靠脈衝管冷卻器。它由兩部分組成：放在地上的氦壓縮機，和裝在冷凍機頂部的冷頭，兩者用一對高低壓軟管連接，軟管可以長達 20 公尺，所以壓縮機可以放在隔壁房間減少噪音和振動。
【切換到 3D 場景 2】壓縮機把氦氣壓縮到高壓，熱量交給冷卻水帶走。冷頭上的旋轉閥大約每秒 1.4 次切換高壓和低壓，讓冷頭裡的氦氣週期性壓縮膨脹。蓄冷器是填滿金屬網或稀土合金的管子，像海綿一樣儲存和交換熱量，形成上熱下冷的溫度梯度；脈衝管和緩衝槽調整相位，使膨脹發生在冷端，冷端就持續吸熱。粒子的顏色代表溫度。
右邊是最常用的兩款規格：PT415 在 4.2 K 有 1.5 W、45 K 有 40 W，壓縮機耗電約 10.7 kW、冷卻水每分鐘 11.5 公升、入水溫度不超過 27 度。這兩個數字——10 kW 和冷卻水——直接決定機房的電力和水路設計。
冷端沒有活動零件，所以振動比傳統 GM 冷凍機小，但旋轉閥本身還是會振動，可以選配遠端馬達，代價是大約 20% 的冷卻功率。`,
});
S({ sec: '01 低溫系統', title: '稀釋冷凍原理：³He 溶入 ⁴He 時吸熱', anim: 'dilution', min: 3,
  async render(s) {
    H(s, '稀釋冷凍原理：³He 溶入 ⁴He 時吸熱'); animPill(s, 'dilution');
    await pic(s, 'dilution', 0.6, 1.35, 3.9, 5.4, { alignX: 'left' });
    const steps = ['**凝結**：GHS 送回的 ³He 在 4 K 凝結，經流阻維持壓力（~500 mbar）', '**預冷**：在熱交換器中被回流的冷稀相冷卻', '**溶解（製冷）**：MXC 中 ³He 由濃相越過相界面進入稀相 → 吸熱', '**蒸發**：Still（~0.8 K）加熱，³He 優先蒸發（壓力 ~0.03 mbar）', '**抽回**：室溫渦輪泵抽走、經冷阱淨化後回到 ①'];
    steps.forEach((t, i) => { numCircle(s, i + 1, 4.8, 1.5 + i * 1.02, 0.48, ['8A5CD0', C.accent3, C.accent2, C.accent1, C.accent5][i]); para(s, [t], 5.45, 1.45 + i * 1.02, 3.9, 0.95, { size: 13.5 }); });
    eqBox(s, ['Q̇ ≈ 84 ṅ T²', { t: 'Q̇：W　ṅ：³He 循環率 mol/s　T：MXC 溫度 K', size: 12.5, cjk: true, color: '4A5468' }], 9.6, 1.45, 3.15, 1.6, { size: 22 });
    card(s, 9.6, 3.3, 3.15, 3.4);
    para(s, [{ t: '典型值', bold: true, color: C.accent1, size: 16 }, 'ṅ ≈ 0.5 mmol/s', '→ 20 mK 時 ~17 μW', '→ 100 mK 時 ~420 μW', '混合液：LD 約 18 L ³He + 90 L ⁴He（STP）；XLD 約 40 L ³He'], 9.8, 3.45, 2.8, 3.2, { size: 13.5, space: 7 });
  },
  notes: `下半段 4 K 到 10 mK 靠的是稀釋冷凍，這是一個非常巧妙的物理過程。
氦有兩種同位素：³He 和 ⁴He。把兩者混合，在 0.87 K 以下會自動分成兩相：上層幾乎是純 ³He 的濃相，下層是 ³He 溶在超流 ⁴He 裡的稀相，即使到絕對零度，稀相裡還是會有 6.6% 的 ³He。
【切換到 3D 場景 3】跟著顏色看 ³He 原子的旅程：第一步，從 GHS 送回來的 ³He 在 4 K 板凝結成液體，經過流阻維持凝結壓力；第二步，在熱交換器裡被回流的冷稀相預冷；第三步是關鍵，在混合腔裡，³He 從濃相越過相界面「溶入」稀相——就像液體蒸發需要吸熱一樣，這個溶解過程也要吸熱，這就是製冷的來源，畫面上相界面的閃光代表吸熱；第四步，稀相裡的 ³He 往上擴散到 Still，Still 加熱到約 0.8 K，³He 的蒸氣壓遠高於 ⁴He，所以優先蒸發；第五步，被室溫的渦輪泵抽走，經過冷阱淨化後再送回第一步，形成循環。
冷卻功率是 84 乘以循環率乘以溫度平方。以典型的 0.5 mmol/s 計算，20 mK 時約 17 μW、100 mK 時約 420 μW，和商用 LD450 的規格非常吻合。面板上可以調循環率和熱負載，看平衡溫度怎麼變。
畫面最下方是樣品區：量子晶片並不在混合腔裡，而是裝在樣品盒內，經銅支架鎖在 MXC 板下方，外面套紅外與磁屏蔽；晶片的熱經由固體傳導，依序經過樣品盒、支架、MXC 板，最後由混合液帶走。按「視角：樣品區」可以拉近看。
最後一個實務重點：混合液裡的 ³He 非常昂貴且稀缺，一台 LD 約需 18 公升、XLD 約 40 公升，價格每公升可達數千到上萬美元，可能佔冷凍機成本的四分之一，所以系統設計上一定要確保它不會外洩。`,
});
S({ sec: '01 低溫系統', title: '冷卻功率與溫度的關係', min: 2,
  async render(s) {
    H(s, '冷卻功率與溫度的關係');
    const Ts = [5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100];
    const ser = [0.25, 0.5, 1.0].map((n) => ({ name: `ṅ = ${n} mmol/s`, labels: Ts.map(String), values: Ts.map((T) => +(84 * n * 1e-3 * (T * 1e-3) ** 2 * 1e6).toFixed(2)) }));
    s.addChart(pres.charts.LINE, ser, { x: 0.6, y: 1.4, w: 7.6, h: 5.2, ...CHART_BASE(), chartColors: [HEX.accent6, HEX.accent2, HEX.accent1], lineSize: 2.5, lineDataSymbol: 'circle', lineDataSymbolSize: 6, showLegend: true, legendPos: 'b', showTitle: true, title: '理想冷卻功率 Q̇ = 84 ṅ T²（μW）', valAxisLogScaleBase: 10, valAxisMinVal: 0.01, valAxisMaxVal: 1000, catAxisTitle: 'MXC 溫度 (mK)', showCatAxisTitle: true, valAxisTitle: 'μW（對數）', showValAxisTitle: true, catAxisTitleColor: '4A5468', valAxisTitleColor: '4A5468', catAxisTitleFontSize: 11, valAxisTitleFontSize: 11, objectName: 'chart-cooling-power' });
    card(s, 8.5, 1.45, 4.25, 5.25);
    para(s, [{ t: '設計意涵', bold: true, color: C.accent1, size: 17 }, '冷卻功率 ∝ T²：溫度減半，冷卻功率只剩 1/4', '熱負載多 4 倍 → 基溫升高 2 倍', '提高 ṅ（加 Still 熱、加大泵）可增加功率，但受泵浦能力與熱交換器限制', '實務上：**把熱負載擋在上層**，比追求更大冷卻功率有效'], 8.75, 1.6, 3.8, 5.0, { size: 14.5, bullet: false, space: 10 });
  },
  notes: `把剛剛的公式畫成圖。橫軸是混合腔溫度，縱軸是冷卻功率，用對數座標；三條線是不同的 ³He 循環率。
最重要的設計意涵是：冷卻功率和溫度平方成正比。溫度減半，冷卻功率只剩四分之一；反過來說，熱負載多四倍，基溫就升高兩倍。
提高循環率可以增加功率，例如加大 Still 加熱功率、用更大的泵，但會受泵浦能力和熱交換器效率的限制。所以實務上最有效的策略是把熱負載擋在上層：在 4 K、Still、Cold plate 就把熱和雜訊吸收掉，而不是讓它們跑到混合腔。`,
});
S({ sec: '01 低溫系統', title: '氣體處理系統（GHS）', anim: 'overview', min: 2.5,
  async render(s) {
    H(s, '氣體處理系統（GHS）'); animPill(s, 'overview');
    const comps = [['tachometer', '渦輪分子泵 + 乾式前級泵', '抽 Still（~0.03 mbar），維持 ³He 循環', C.accent3],
      ['filter', '冷阱（內建或液氮）', '凍住混合氣中的空氣、水氣等雜質，避免堵塞流阻', C.accent2],
      ['sliders', '氣動閥 + 壓力計 P1–P6 + 流量計', '電腦控制凝結、循環、回收；監控流量與壓力', C.accent1],
      ['layer', '混合氣儲存槽（dump）', '停機時儲存 ³He/⁴He；背壓閥（~1.1–1.2 bar）可自動回收', '8A5CD0'],
      ['shield', '外真空罩（OVC）抽氣', '降溫前抽高真空並檢漏；運轉中監控 OVC 壓力', C.accent6]];
    comps.forEach(([ic, t, d, col], i) => {
      const y = 1.45 + i * 1.05;
      iconCircle(s, ic, 0.6, y + 0.05, 0.62, col);
      sub(s, t, 1.4, y, 6.2, C.text1, 16.5);
      s.addText(d, { x: 1.4, y: y + 0.45, w: 6.3, h: 0.45, fontSize: 13.5, color: '4A5468', margin: 0, isTextBox: true });
    });
    card(s, 8.0, 1.45, 4.75, 5.3, 'FBF4E8');
    para(s, [{ t: '³He：最昂貴的「耗材」', bold: true, color: C.accent4, size: 17 }, '每公升 ~1,000–20,000 美元，可佔冷凍機成本的 1/4', '一台 LD ~18 L、XLD ~40 L ³He', '供應有限（核武氚衰變副產品）；已有業者簽約月球開採 ³He（2028 起交貨）', '**GHS 的首要任務：任何異常都不能讓混合氣外洩**'], 8.25, 1.6, 4.3, 5.0, { size: 14, space: 10 });
  },
  notes: `氣體處理系統 GHS 是稀釋循環在室溫端的部分，通常是一個裝滿泵、閥門和儀表的櫃子。
它有五大功能：第一，渦輪分子泵加乾式前級泵抽 Still，壓力約 0.03 mbar，維持 ³He 循環；第二，冷阱把混合氣裡的空氣、水氣凍住，不然雜質會在低溫的流阻處結冰堵塞，這是實際運轉中最常見的問題之一；第三，氣動閥、壓力計和流量計由電腦控制，執行凝結、循環、回收等程序；第四，混合氣儲存槽在停機時儲存混合氣，背壓閥在壓力超過約 1.1 bar 時自動讓混合氣流回儲存槽；第五，負責外真空罩的抽氣和檢漏。
右邊強調 ³He 的價值：每公升一千到兩萬美元，可佔冷凍機成本的四分之一。目前 ³He 主要來自核武氚的衰變，供應非常有限，Bluefors 甚至和業者簽了從月球開採 ³He 的供貨協議。所以 GHS 設計的首要任務是：任何異常情況下，混合氣都不能外洩。`,
});
S({ sec: '01 低溫系統', title: '降溫與升溫流程', anim: 'cooldown', min: 2.5,
  async render(s) {
    H(s, '降溫與升溫流程'); animPill(s, 'cooldown');
    chevrons(s, ['① 抽真空 / 檢漏\n~2 h', '② 脈衝管預冷\n~20 h', '③ 凝結混合氣\n~2–3 h', '④ 循環到基溫\n~3–5 h'], 0.6, 1.45, 12.15, 0.95, [C.accent6, C.accent5, '8A5CD0', C.accent3]);
    const Ts = []; for (let t = 0; t <= 36; t += 1) Ts.push(t);
    const names = ['50 K 級', '4 K 級', 'Still', 'Cold plate', 'MXC'];
    const ser = names.map((n, i) => ({ name: n, labels: Ts.map(String), values: Ts.map((t) => +TMODEL(t)[i].toPrecision(3)) }));
    s.addChart(pres.charts.LINE, ser, { x: 0.6, y: 2.6, w: 7.4, h: 4.1, ...CHART_BASE(), chartColors: [HEX.accent1, HEX.accent5, HEX.accent2, HEX.accent3, '8A5CD0'], lineSize: 2, lineDataSymbol: 'none', showLegend: true, legendPos: 'r', showTitle: true, title: '各級溫度（K，對數）— 示意模型', valAxisLogScaleBase: 10, valAxisMinVal: 0.01, valAxisMaxVal: 1000, catAxisTitle: '時間 (h)', showCatAxisTitle: true, catAxisTitleColor: '4A5468', catAxisTitleFontSize: 11, catAxisLabelFrequency: 6, objectName: 'chart-cooldown' });
    await pic(s, 'cooldown', 8.3, 2.6, 2.1, 4.1, { file: 'cooldown_pre' });
    await pic(s, 'cooldown', 10.6, 2.6, 2.1, 4.1);
    caption(s, '預冷中（12 h）　　　　 循環中（34 h）', 8.3, 6.7, 4.4, { align: 'center' });
  },
  notes: `一次完整的降溫分四個階段。
第一，抽真空和檢漏，約兩小時：外真空罩要抽到高真空，否則殘留氣體會把熱從外面傳進來。
第二，脈衝管預冷，這是最久的階段，約二十小時：50 K 和 4 K 板由脈衝管直接冷卻，下面各級透過預冷迴路或熱開關跟著降到約 4 K。時間主要取決於各級的熱容量，也就是掛了多少銅和多少線。
第三，凝結混合氣，約兩三小時：GHS 把混合氣送進去，在 4 K 凝結成液體。
第四，啟動稀釋循環，數小時內降到 10 mK 左右。
【切換到 3D 場景 4】可以用時間滑桿或自動播放看整個過程，各級的顏色代表溫度，右下角是溫度曲線。左邊的圖是同一個模型的曲線。Bluefors 規格是空機 24 小時內到基溫，大型機台或負載多的系統通常需要一天半到兩天。
升溫也很慢，回到室溫要一到兩天。這意味著：更換晶片的週期是以「天」計算，這對研發流程規劃非常重要，也是為什麼大型系統會用多台冷凍機輪流測試。`,
});

// ===== 02 佈線 =====
S({ sec: '02 低溫佈線與封裝', layout: 'SECTION_DARK', title: '02 低溫佈線與封裝', min: 0.5, render: sec('02', '低溫佈線與封裝', '線路種類 · 衰減與濾波 · 熱負載預算 · 纜線材料 · 屏蔽與封裝', 'wiring', C.accent2), notes: `第二部分：訊號怎麼從室溫進到 10 mK。` });
S({ sec: '02 低溫佈線與封裝', title: '每顆量子位元需要哪些線？', anim: 'wiring', min: 3,
  async render(s) {
    H(s, '每顆量子位元需要哪些線？'); animPill(s, 'wiring');
    table(s, [['線路', '數量', '用途', '典型配置'],
      ['XY 驅動', '每顆 1 條', '微波脈衝做單量子位元閘', '−20 dB @4K、−20 @CP、−20 @MXC'],
      ['Z 磁通', '每顆 1 條', 'SQUID 調頻、雙量子位元閘', '−10 dB @4K、1.3 GHz 低通 + Eccosorb'],
      ['讀取輸入', '每 4–8 顆 1 條', '多工讀取脈衝', '同 XY（共 −60 dB）'],
      ['讀取輸出', '每 4–8 顆 1 條', '讀取訊號回到室溫', '隔離器 → TWPA → NbTi 線 → HEMT'],
      ['TWPA 泵浦', '每條輸出 1 條', '驅動參量放大器', '衰減 + 定向耦合器'],
      ['直流線', '數十條', '溫度計、加熱器、HEMT 偏壓', '雙絞線、RC 濾波'],
    ], 0.6, 1.45, 8.3, [1.4, 1.6, 2.4, 2.9], { size: 12.5, rowH: 0.55 });
    caption(s, '配置參考：Krinner et al. (2019)', 0.6, 5.4, 8.3);
    card(s, 9.2, 1.45, 3.55, 5.25);
    s.addText('124', { x: 9.2, y: 1.6, w: 3.55, h: 1.0, fontSize: 54, bold: true, color: C.accent2, align: 'center', margin: 0, isTextBox: true, fontFace: 'Arial' });
    s.addText('50 顆量子位元所需的 RF 線\n（50 XY + 50 Z + 8 輸入 + 8 輸出 + 8 泵浦）', { x: 9.35, y: 2.6, w: 3.25, h: 0.9, fontSize: 12.5, color: '4A5468', align: 'center', margin: 0, isTextBox: true });
    para(s, ['規模 ∝ 量子位元數：100 顆 ≈ 250 條', 'XLD1000sl 最多可裝 1008 條同軸', '高密度扁平纜線：每片 8 通道，可達 1,536 條'], 9.4, 3.7, 3.2, 2.9, { size: 13, bullet: true, space: 8 });
  },
  notes: `每顆 transmon 量子位元需要哪些線？
XY 驅動線，每顆一條，送微波脈衝做單量子位元閘；Z 磁通線，每顆一條，調整 SQUID 頻率、做雙量子位元閘；讀取的輸入和輸出線則是每四到八顆共用一組，靠頻率多工；每條讀取輸出需要一條 TWPA 泵浦線；另外還有幾十條直流線給溫度計、加熱器和 HEMT 偏壓。
右邊這個數字很有代表性：ETH 的 50 顆量子位元系統需要 124 條射頻線。也就是說，射頻線數量大約是量子位元數的兩倍半，100 顆就要約 250 條。大型冷凍機 XLD1000sl 最多可以預裝 1008 條同軸線；用高密度扁平纜線可以到 1,536 條。
【切換到 3D 場景 5】這個場景把六種線並排畫出來，每一級的元件都標在線上；滑桿可以增加量子位元數，看線束變多，以及右下角各級熱負載的變化。`,
});
S({ sec: '02 低溫佈線與封裝', title: '各級的衰減、濾波與放大', anim: 'wiring', min: 3,
  async render(s) {
    H(s, '各級的衰減、濾波與放大'); animPill(s, 'wiring');
    await pic(s, 'wiring', 0.6, 1.4, 3.6, 5.4, { alignX: 'left' });
    const cols = [['溫層', 1.2], ['輸入（XY / 讀取）', 2.2], ['Z 磁通', 1.9], ['讀取輸出', 2.6]];
    table(s, [cols.map((c) => c[0]),
      ['300 K', '密封接頭', '密封接頭 + bias-tee', '室溫放大 → 下變頻'],
      ['50 K', '熱錨定', '熱錨定', '熱錨定'],
      ['4 K', '−20 dB', '−10 dB', '**HEMT ~40 dB**（~5–10 mW）'],
      ['Still', '熱錨定（0 dB）', '熱錨定', 'NbTi 超導線'],
      ['Cold plate', '−20 dB', '—', '環行器'],
      ['MXC', '−20 dB + 濾波', '低通 + Eccosorb', '隔離器、帶通、**TWPA 20–30 dB**'],
    ], 4.5, 1.45, 7.9, cols.map((c) => c[1]), { size: 12.5, rowH: 0.5 });
    para(s, ['輸入總衰減約 **60 dB**（+ ~9 dB 線損）→ 6 GHz 殘留熱光子 ~10^{−3}', '衰減器要**熱錨定**在對應溫層，吸收的功率才不會加熱下一級', '輸出線用 NbTi 超導同軸：低損耗、低導熱'], 4.5, 5.15, 8.2, 1.6, { size: 13.5, bullet: true, space: 6 });
  },
  notes: `這頁整理每一級放什麼元件。
輸入線，也就是 XY 驅動和讀取輸入：4 K、Cold plate、MXC 各放 20 dB 衰減器，總共約 60 dB，加上纜線本身大約 9 dB 的損耗。這樣在 6 GHz 的殘留熱光子大約是千分之一。注意 Still 那一級通常只做熱錨定，不放衰減器——因為衰減器會吸收功率發熱，要放在冷卻功率夠的位置。
Z 磁通線需要比較大的電流，所以衰減比較少，只在 4 K 放 10 dB，主要靠 MXC 的低通濾波和 Eccosorb 紅外濾波。
讀取輸出線方向相反：MXC 的隔離器和 TWPA，Cold plate 的環行器，經過 NbTi 超導同軸到 4 K 的 HEMT，HEMT 本身會消耗約 5 到 10 mW，在 4 K 這是可以接受的。
關鍵觀念是熱錨定：衰減器吸收的訊號功率會變成熱，所以必須牢牢鎖在對應溫層的銅板上。`,
});
S({ sec: '02 低溫佈線與封裝', title: '熱負載預算：線越多，冷卻功率越緊', anim: 'wiring', min: 3,
  async render(s) {
    H(s, '熱負載預算：線越多，冷卻功率越緊'); animPill(s, 'wiring');
    const p50 = heatPct(50), p200 = heatPct(200);
    s.addChart(pres.charts.BAR, [{ name: '50 顆量子位元（~127 條同軸）', labels: W.stages, values: p50.map((v) => +v.toFixed(1)) }, { name: '200 顆量子位元（~500 條同軸）', labels: W.stages, values: p200.map((v) => +v.toFixed(1)) }],
      { x: 0.6, y: 1.4, w: 7.6, h: 5.3, barDir: 'col', barGrouping: 'clustered', ...CHART_BASE(), chartColors: [HEX.accent2, HEX.accent4], showLegend: true, legendPos: 'b', showTitle: true, title: '各級熱負載佔冷卻功率比例（%，示意估算）', showValue: true, dataLabelPosition: 'outEnd', dataLabelFontSize: 10, dataLabelColor: '1A1F2B', valAxisMaxVal: 120, objectName: 'chart-heat-budget' });
    card(s, 8.5, 1.45, 4.25, 5.25);
    para(s, [{ t: '估算假設', bold: true, color: C.accent1, size: 16 }, '每條不鏽鋼同軸被動熱：50 K ~45 mW、4 K ~1 mW、CP ~0.4 μW、MXC ~0.015 μW', 'HEMT 每顆 5 mW（4 K）', '冷卻功率取 XLD 量測值',
      { t: '結論', bold: true, color: C.accent4, size: 16 }, '數百顆量子位元時，**Cold plate 與 50 K** 率先吃緊', '對策：低導熱扁平纜線、多路共用、低溫電子學、更大型平台（如 KIDE）'], 8.75, 1.6, 3.8, 5.0, { size: 13, space: 7 });
  },
  notes: `把線數和熱負載連起來看。這張圖是用 Krinner 論文的每條線熱負載，和同一台 XLD 的冷卻功率，估算各級熱負載佔冷卻功率的比例。藍色是 50 顆量子位元，大約 127 條同軸線；紅色是 200 顆，大約 500 條。
50 顆的時候，各級都還很寬鬆，最多二十幾趴。200 顆的時候，50 K 級用掉約四分之三，Cold plate 已經超過一百趴——也就是冷卻功率用盡，MXC 也到了四成。
這是一個簡化的估算，實際系統會用更低導熱的扁平纜線、更好的熱錨定，但它說明了一個重要事實：佈線的熱負載是超導量子電腦規模化的主要瓶頸之一。業界的對策包括：低導熱的高密度扁平纜線、多路共用、把部分控制電子放進低溫的 cryo-CMOS，以及更大的冷凍平台。
【在 3D 場景 5 中可以把量子位元數從 1 拉到 200，右下角的長條即時變化】`,
});
S({ sec: '02 低溫佈線與封裝', title: '纜線材料與高密度佈線', min: 2,
  async render(s) {
    H(s, '纜線材料與高密度佈線');
    table(s, [['纜線', '導熱', '損耗', '典型用途'],
      ['不鏽鋼同軸（UT85-SS）', '低', '中', '輸入、磁通線（室溫 → MXC）'],
      ['CuNi 同軸', '比 SS 高 20–30 %', '中', '輸入線（常見替代）'],
      ['NbTi 超導同軸', '極低（超導段）', '極低', '輸出線 MXC → 4 K'],
      ['銅 / 銀鍍同軸', '高', '低', '只用在同一溫層內、室溫段'],
      ['高密度扁平纜線', '低（每通道 < 4 μW，3 K→0.7 K）', '中', '大量 XY/Z 線，每片 8 通道'],
      ['磷青銅 / 康銅雙絞線', '低', '—', '直流：溫度計、加熱器、偏壓'],
    ], 0.6, 1.45, 8.4, [2.6, 2.3, 1.0, 2.5], { size: 12.5, rowH: 0.55 });
    caption(s, '扁平纜線導熱數據為廠商宣稱值（Bluefors Cri/oFlex）', 0.6, 5.4, 8.4);
    card(s, 9.3, 1.45, 3.45, 5.25);
    para(s, [{ t: '選材原則', bold: true, color: C.accent1, size: 16 }, '跨溫層：選**低導熱**材料（SS、NbTi）', '同溫層：選**低損耗**材料（銅）', '輸出線的損耗直接降低 SNR → 用超導線', '每條線都要在每一級**熱錨定**', '纜線要固定、包覆 —— 振動摩擦會產生雜訊'], 9.5, 1.6, 3.1, 5.0, { size: 13.5, space: 9 });
  },
  notes: `纜線材料的選擇是導熱和損耗之間的權衡：導電好的金屬通常導熱也好。
跨越溫層的段落要選低導熱的材料：輸入和磁通線常用不鏽鋼同軸，CuNi 也可以但導熱多 20 到 30%；輸出線從 MXC 到 4 K 用 NbTi 超導同軸，因為超導狀態下既不損耗、導熱又極低，而輸出線的任何損耗都會直接降低讀取訊雜比。
同一溫層內，或室溫段，可以用損耗低的銅線。直流線用磷青銅或康銅雙絞線。
大量的 XY 和 Z 線，現在越來越多改用高密度扁平纜線，一片可以有 8 個通道，大幅提高密度。
最後一點常被忽略：纜線要固定好、做包覆。脈衝管的振動會讓纜線彼此摩擦，摩擦起電會產生千赫茲等級的雜訊，這在機房基礎設施那部分會再提到。`,
});
S({ sec: '02 低溫佈線與封裝', title: '屏蔽與樣品封裝', min: 2.5,
  async render(s) {
    H(s, '屏蔽與樣品封裝');
    const L = [['magnet', '磁屏蔽', 'Cryoperm / μ-metal（高磁導率）+ 超導鋁屏蔽；多層組合可達 > 10⁴ 倍衰減；目標殘留場約 < 1 μT', C.accent3],
      ['eye', '紅外 / 輻射屏蔽', '各級的銅輻射屏蔽；樣品區「光密封」+ 黑色吸收塗層 → 準粒子密度降低 3 個數量級', C.accent4],
      ['chip', '樣品盒', '銅或鋁盒、PCB 轉接、打線（wire bond）；抑制盒體共振模態、良好熱接觸', C.accent1],
      ['filter', '最後一級濾波', 'Eccosorb 紅外吸收濾波器、低通濾波，擋住高頻光子', C.accent2]];
    L.forEach(([ic, t, d, col], i) => {
      const x = 0.6 + (i % 2) * 6.15, y = 1.45 + Math.floor(i / 2) * 2.65;
      card(s, x, y, 5.95, 2.45);
      iconCircle(s, ic, x + 0.25, y + 0.25, 0.62, col);
      sub(s, t, x + 1.05, y + 0.3, 4.7, C.text1, 17);
      para(s, [d], x + 0.3, y + 1.05, 5.4, 1.3, { size: 13.5, color: '4A5468' });
    });
    caption(s, '紅外屏蔽效果：Barends et al., APL 99, 113507 (2011)；磁屏蔽模擬：COMSOL 論文', 0.6, 6.5, 12);
  },
  notes: `佈線之外，晶片本身還需要層層保護。
磁屏蔽：地磁場約 50 微特斯拉，會在超導體裡形成磁通渦旋，造成損耗，也會影響 SQUID。所以用高磁導率的 Cryoperm 或 μ-metal，加上超導鋁屏蔽，多層組合可以衰減一萬倍以上，目標殘留磁場約在一微特斯拉以下。
紅外和輻射屏蔽：每一級都有銅製的輻射屏蔽罩。Barends 等人 2011 年的實驗顯示，把樣品區做到完全光密封、加上黑色吸收塗層，準粒子密度可以降低三個數量級，T1 明顯改善。
樣品盒：通常是銅或鋁盒，晶片透過打線連到 PCB，再接到同軸接頭。盒子本身的電磁共振模態必須遠離量子位元頻率，並且和 MXC 板有良好的熱接觸。
最後一級濾波：Eccosorb 吸收材料做的濾波器，擋住從線路傳下來的高頻光子。`,
});

// ===== 03 控制電子學 =====
S({ sec: '03 控制電子學', layout: 'SECTION_DARK', title: '03 控制電子學', min: 0.5, render: sec('03', '室溫控制電子學', '架構 · 外差 vs 直接合成 · 時脈同步 · 即時回饋 · 直流源', 'electronics', C.accent1), notes: `第三部分：室溫的控制電子學。` });
S({ sec: '03 控制電子學', title: '控制系統架構', anim: 'electronics', min: 3,
  async render(s) {
    H(s, '控制系統架構'); animPill(s, 'electronics');
    await pic(s, 'electronics', 0.6, 1.4, 7.0, 4.2, { alignX: 'left' });
    caption(s, '3D 場景 6：上傳 → 觸發 → 驅動 → 讀取 → 判別 → 回饋 → 回傳（依序播放）', 0.6, 5.65, 7.0);
    const mods = [['AWG / DAC', '產生驅動與讀取波形（GSa/s 等級、14-bit）'], ['LO + IQ 混頻器', '上變頻到 4–8 GHz（外差架構）'], ['ADC + 下變頻', '讀取訊號數位化（數 GSa/s）'], ['FPGA', '序列播放、解調、判別、即時回饋'], ['DC 電流源', '磁通偏壓（低雜訊、高解析度）'], ['同步器 + 參考時脈', '所有儀器同相位、同觸發']];
    mods.forEach(([t, d], i) => {
      const y = 1.45 + i * 0.85;
      numCircle(s, i + 1, 7.9, y + 0.08, 0.45, C.accent1);
      sub(s, t, 8.5, y, 4.2, C.text1, 15);
      s.addText(d, { x: 8.5, y: y + 0.38, w: 4.25, h: 0.38, fontSize: 12.5, color: '4A5468', margin: 0, isTextBox: true });
    });
    para(s, ['每顆量子位元約需 2–3 個高速通道 + 1 個 DC 通道'], 0.6, 6.1, 7.0, 0.5, { size: 14, bold: true, color: C.accent1 });
  },
  notes: `控制電子機櫃的組成：
AWG 或 DAC 負責產生驅動和讀取的波形，取樣率每秒數十億次、14 位元解析度；LO 和 IQ 混頻器把中頻訊號上變頻到 4 到 8 GHz；ADC 和下變頻器把讀取訊號數位化；FPGA 負責播放序列、解調、判別和即時回饋；DC 電流源提供磁通偏壓；同步器和參考時脈讓所有儀器保持同相位、同觸發。
【切換到 3D 場景 6】動畫依序播放一個完整的循環：電腦上傳脈衝序列到同步器、同步器觸發 AWG 和讀取模組、AWG 產生的 XY 脈衝經過混頻器進入冷凍機、讀取脈衝進去再回來、FPGA 判別 0 或 1、再在幾百奈秒內回饋一個條件式的 π 脈衝做主動重置，最後把結果回傳電腦。右下角是 XY 驅動波形：I 是高斯包絡、Q 是 DRAG 修正。
大致估算：每顆量子位元需要兩到三個高速通道加一個直流通道，100 顆量子位元就是幾百個通道，這是控制電子規模化的挑戰。`,
});
S({ sec: '03 控制電子學', title: '外差 IQ 混頻 vs 直接射頻合成', anim: 'electronics', min: 2.5,
  async render(s) {
    H(s, '外差 IQ 混頻 vs 直接射頻合成'); animPill(s, 'electronics');
    const two = [['外差 IQ 混頻', C.accent3, ['AWG 產生中頻（~100 MHz）I/Q', 'LO + 類比 IQ 混頻器上變頻', '需校正 IQ 不平衡、LO 洩漏、鏡像', '元件成熟、成本較低']], ['直接射頻合成', C.accent1, ['高速 DAC 直接合成 GHz 訊號', '數位上變頻（NCO），無類比混頻器', '免 IQ 校正、通道一致性好', '近年主流（RFSoC、新一代儀器）']]];
    two.forEach(([t, col, b], i) => {
      const x = 0.6 + i * 3.6; card(s, x, 1.45, 3.4, 3.2);
      sub(s, t, x + 0.25, 1.6, 3.0, col, 17);
      para(s, b, x + 0.25, 2.15, 2.95, 2.4, { size: 13.5, bullet: true, space: 6 });
    });
    table(s, [['產品（例）', '頻率範圍', '重點規格'], ['Zurich SHFQC+', 'DC–8.5 GHz', 'DAC 14-bit 6 GSa/s；ADC 4 GSa/s'], ['Qblox QCM-RF/QRM-RF', '2–18.5 GHz', 'LINQ 回饋網路 < 400 ns'], ['Keysight M5300A', 'DC–16 GHz', '2 GHz 瞬時頻寬、14-bit'], ['QM OPX1000', 'MW-FEM', '8 輸出、2–4 GSa/s'], ['RFSoC（QICK）', '至 ~6 GHz', '開源、ADC 2.5 GS/s']],
      7.9, 1.45, 4.85, [1.75, 1.35, 1.75], { size: 11.5, rowH: 0.5 });
    caption(s, '規格取自各廠商公開資料（2026），僅供比較，不代表推薦', 7.9, 4.95, 4.85);
    para(s, ['選型考量：**頻率範圍**（含讀取與 TWPA 泵浦）、**通道數與密度**、**回饋延遲**、**相位雜訊**（如 −110 dBc/Hz @10 kHz）、軟體生態、每通道成本'], 0.6, 5.45, 12.15, 1.2, { size: 14.5, space: 6 });
  },
  notes: `產生 GHz 微波有兩種架構。
傳統的外差架構：AWG 產生大約 100 MHz 的中頻 I/Q 訊號，和 LO 在類比 IQ 混頻器裡上變頻。元件成熟，但必須定期校正 IQ 不平衡、LO 洩漏和鏡像頻率，通道一多，校正工作量很大。
直接射頻合成：用每秒數十億次的高速 DAC 直接合成 GHz 訊號，在數位端做上變頻，沒有類比混頻器，因此不需要 IQ 校正，通道之間的一致性也比較好。這是近幾年的主流，例如 RFSoC 平台和新一代的商用儀器。
右邊列出幾款代表性產品的公開規格，例如 Zurich 的 SHFQC+、Qblox、Keysight、Quantum Machines，以及 Fermilab 開源的 QICK，這只是比較，不代表推薦。
選型的考量包括頻率範圍、通道數和密度、回饋延遲、相位雜訊、軟體生態，以及每通道成本。`,
});
S({ sec: '03 控制電子學', title: '時脈與同步：所有儀器踩同一個節拍', min: 2.5,
  async render(s) {
    H(s, '時脈與同步：所有儀器踩同一個節拍');
    // 樹狀示意
    const nd = (x, y, w, t, col) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.62, rectRadius: 0.08, fill: { color: col }, line: { color: col, width: 0 }, objectName: oname('clk-node') }); s.addText(runs(t), { x, y, w, h: 0.62, fontSize: 12.5, bold: true, color: C.background1, align: 'center', valign: 'middle', margin: 2, isTextBox: true }); };
    nd(2.4, 1.5, 2.6, '銣原子鐘 / GPS 馴服\n10 MHz 參考', C.accent1);
    nd(2.4, 2.75, 2.6, '時脈 / 觸發分配器', C.accent6);
    ['AWG 1…N', 'LO 合成器', '讀取 ADC', 'FPGA 同步器'].forEach((t, i) => { nd(0.6 + i * 1.6, 4.05, 1.45, t, C.accent3); link(s, 3.7, 3.37, 0.6 + i * 1.6 + 0.72, 4.05, { color: HEX.accent6, width: 1.5, name: 'clk-line' }); });
    link(s, 3.7, 2.12, 3.7, 2.75, { color: HEX.accent1, width: 2, name: 'clk-line' });
    para(s, ['**10 MHz 參考**：所有 LO、DAC、ADC 的頻率都由它倍頻而來 → 相位彼此鎖定', '**觸發 / 同步匯流排**：讓數十台儀器在同一個時鐘週期開始播放（例：100 MHz 同步時脈）', '**相位雜訊**：直接造成量子位元失相 → 選用低相位雜訊的參考與合成器'], 0.6, 4.95, 6.5, 1.8, { size: 13.5, bullet: true, space: 6 });
    card(s, 7.4, 1.45, 5.35, 5.25, 'FBF4E8');
    para(s, [{ t: '為什麼要這麼嚴格？', bold: true, color: C.accent1, size: 17 }, '量子閘的相位就是微波的相位：驅動 LO 與讀取 LO 若沒有鎖定，每次量測的參考相位都會漂移', '雙量子位元閘需要兩個通道的脈衝**奈秒級對齊**', '多台儀器擴展時，觸發抖動（jitter）必須遠小於脈衝寬度（~數十 ns）', '實務：參考時脈用低雜訊分配放大器、等長纜線，並在軟體中校正固定延遲'], 7.65, 1.6, 4.9, 5.0, { size: 14, space: 9 });
  },
  notes: `時脈與同步是很容易被忽略、但一出問題就很難除錯的部分。
所有儀器都鎖在同一個 10 MHz 參考時脈上，常用銣原子鐘，有時再用 GPS 馴服。每一台儀器裡的 LO、DAC、ADC 的頻率都是由這個參考倍頻而來，所以彼此的相位是鎖定的。另外還有觸發和同步匯流排，讓幾十台儀器在同一個時鐘週期開始播放，例如 Zurich 的 ZSync 就傳一個 100 MHz 的同步時脈。
為什麼要這麼嚴格？因為量子閘的相位就是微波的相位：如果驅動和讀取的 LO 沒有鎖定，每次量測的參考相位都會漂移；雙量子位元閘需要兩個通道的脈衝在奈秒等級對齊；擴展到很多台儀器時，觸發抖動必須遠小於幾十奈秒的脈衝寬度。實務上會用低雜訊的分配放大器、等長纜線，再在軟體裡校正固定延遲。`,
});
S({ sec: '03 控制電子學', title: '即時回饋與直流偏壓源', min: 2.5,
  async render(s) {
    H(s, '即時回饋與直流偏壓源');
    const st = [['~350 ns', '單機內回饋延遲\n（Zurich SHFQC）', C.accent1], ['< 550 ns', '跨機櫃系統回饋\n（經 PQSC）', C.accent3], ['< 400 ns', '量測結果分配網路\n（Qblox LINQ）', C.accent2]];
    st.forEach(([v, l, col], i) => { const x = 0.6 + i * 2.6; card(s, x, 1.45, 2.4, 2.0); s.addText(v, { x, y: 1.55, w: 2.4, h: 0.9, fontSize: 30, bold: true, color: col, align: 'center', valign: 'middle', margin: 0, isTextBox: true, fontFace: 'Arial' }); s.addText(l, { x, y: 2.5, w: 2.4, h: 0.8, fontSize: 12.5, color: '4A5468', align: 'center', margin: 0, isTextBox: true }); });
    para(s, ['**主動重置**：讀到 1 就送 π 脈衝，比等待 T_{1} 衰減快百倍', '**中途量測與條件運算**：量子糾錯、量子傳送的必要條件', '**糾錯解碼器**：每輪症狀（syndrome）須在 ~μs 內解碼，FPGA/ASIC 實作'], 0.6, 3.75, 7.6, 2.4, { size: 14.5, bullet: true, space: 9 });
    card(s, 8.5, 1.45, 4.25, 5.25);
    para(s, [{ t: '直流與偏壓源', bold: true, color: C.accent1, size: 17 }, '**磁通偏壓**：低雜訊電流/電壓源（例：24 通道、25-bit、< 20 nV/√Hz）', '經 **bias-tee** 與快速 Z 脈衝合併在同一條線', '**HEMT 偏壓**：精密低雜訊電源，上電順序要正確', '**TWPA 泵浦**：低相位雜訊微波源 + DC 偏壓', '直流線要濾波、接地良好，避免低頻雜訊造成磁通漂移'], 8.75, 1.6, 3.8, 5.0, { size: 13.5, space: 8 });
  },
  notes: `即時回饋是量子糾錯的基礎。目前商用設備的回饋延遲：單一儀器內約 350 奈秒，跨機櫃約 550 奈秒以內，Qblox 的結果分配網路約 400 奈秒以內。
它的應用包括：主動重置，讀到 1 就立刻送 π 脈衝把它翻回 0，比等 T1 自然衰減快上百倍；中途量測與條件運算，這是量子糾錯和量子傳送的必要條件；糾錯解碼器，每一輪的症狀量測結果必須在微秒等級內解碼完成，否則錯誤會累積，這通常用 FPGA 或專用晶片實作。
右邊是直流和偏壓源。磁通偏壓需要非常低雜訊的電流或電壓源，例如 QDevil QDAC-II 是 24 通道、25 位元、雜訊低於每根號赫茲 20 奈伏特；它和快速 Z 脈衝透過 bias-tee 合併在同一條線上。HEMT 需要精密的偏壓電源，而且上電和斷電的順序要正確，否則可能損壞。TWPA 需要低相位雜訊的泵浦源。所有直流線都要濾波、良好接地，否則低頻雜訊會造成磁通漂移。`,
});

// ===== 04 軟體與運作 =====
S({ sec: '04 軟體與運作', layout: 'SECTION_DARK', title: '04 軟體與運作', min: 0.5, render: sec('04', '軟體與運作', '軟體堆疊 · 啟動與校準 · 監控與聯鎖 · 故障處置', 'software', C.accent5), notes: `第四部分：軟體與日常運作。` });
S({ sec: '04 軟體與運作', title: '軟體堆疊：從量子程式到微波', anim: 'software', min: 2.5,
  async render(s) {
    H(s, '軟體堆疊：從量子程式到微波'); animPill(s, 'software');
    await pic(s, 'software', 0.6, 1.4, 6.6, 4.3, { alignX: 'left' });
    caption(s, '3D 場景 7：程式逐層下傳、結果逐層回傳；校準資料庫與自動校準服務', 0.6, 5.75, 6.6);
    table(s, [['層', '工作'], ['使用者 / 雲端 API', 'Qiskit、Cirq、OpenQASM；工作佇列與權限'], ['編譯器', '原生閘分解、量子位元映射、路由（SWAP）、最佳化'], ['脈衝層', '查校準資料 → 脈衝；排出時間表'], ['控制韌體', 'FPGA 序列器、波形記憶體、即時分支'], ['校準 / 監控', '自動校準、參數漂移追蹤、日誌與告警']], 7.5, 1.45, 5.25, [1.9, 3.35], { size: 12.5, rowH: 0.62 });
    para(s, ['軟體是把「硬體」變成「可用的量子電腦」的關鍵'], 7.5, 5.4, 5.25, 0.8, { size: 14.5, bold: true, color: C.accent5 });
  },
  notes: `硬體連好之後，要靠軟體把它變成「可用的量子電腦」。
最上層是使用者介面，例如 Qiskit、Cirq 或 OpenQASM，透過雲端 API 和工作佇列送到機器。編譯器把任意的量子閘分解成這台機器支援的原生閘，依照晶片的連接關係做量子位元映射和路由，必要時插入 SWAP，並且最佳化電路深度。脈衝層把每一個原生閘查校準資料庫轉成具體的脈衝，排出時間表。控制韌體在 FPGA 上以奈秒精度播放，處理即時分支。
【切換到 3D 場景 7】白色方塊是程式往下傳，標籤會告訴你它在每一層長什麼樣子；綠色球是結果往上傳：IQ 原始資料、0/1 位元串、最後變成直方圖或期望值。右邊的校準資料庫和自動校準服務貫穿其中。`,
});
S({ sec: '04 軟體與運作', title: '從基溫到上線：啟動與校準流程', anim: 'bringup', min: 3,
  async render(s) {
    H(s, '從基溫到上線：啟動與校準流程'); animPill(s, 'bringup');
    chevrons(s, ['系統\n檢查', '讀取腔\n頻譜', 'Punch\n-out', '量子位元\n頻譜', 'Rabi', 'Ramsey'], 0.6, 1.45, 12.15, 0.95, [C.accent6, C.accent3, C.accent3, C.accent2, C.accent2, C.accent2]);
    chevrons(s, ['T₁ / T₂', '讀取\n最佳化', 'DRAG\n閘微調', '隨機基準\n測試 RB', '雙量子位元\n閘校準', '上線 ✓'], 0.6, 2.55, 12.15, 0.95, [C.accent1, C.accent1, C.accent1, C.accent5, C.accent5, C.accent5]);
    await pic(s, 'bringup', 0.6, 3.75, 6.6, 2.7, { alignX: 'left' });
    caption(s, '3D 場景 10：每一步的典型量測圖顯示在右下角', 0.6, 6.5, 6.6);
    card(s, 7.5, 3.75, 5.25, 3.0);
    para(s, [{ t: '要點', bold: true, color: C.accent1, size: 16 }, '全部由軟體自動執行，結果寫入校準資料庫', '單量子位元：數十分鐘；整個處理器：數小時', '參數會漂移（TLS、溫度、磁通）→ 每日/每週自動重校', '任何一步失敗 → 回頭檢查硬體（佈線、偏壓、溫度）'], 7.75, 3.9, 4.8, 2.8, { size: 13.5, space: 7 });
  },
  notes: `降到基溫、所有線都接好之後，量子電腦還不能直接用，還要一連串的校準。
第一步是系統檢查：各級溫度、HEMT 和 TWPA 偏壓、每條線的穿透和衰減是否符合預期。第二步，讀取腔頻譜，在饋線上掃頻找到每個讀取腔的共振凹陷。第三步 punch-out，提高讀取功率，如果共振頻率會從被量子位元推移的位置跳回裸頻，就證明量子位元存在而且耦合正常。第四步，量子位元頻譜找到 f01。接著 Rabi 找 π 脈衝振幅、Ramsey 精修頻率、量 T1 和 T2、最佳化讀取參數、微調 DRAG，最後用隨機基準測試量出每閘錯誤率；雙量子位元閘還需要額外的校準。
【切換到 3D 場景 10】右下角會依序顯示每一步的典型量測圖。
這些步驟全部由軟體自動執行。單顆量子位元大約幾十分鐘，整顆處理器要數小時。參數會漂移，所以每天或每週要自動重校。而且如果某一步失敗，例如找不到讀取腔，往往是硬體問題——佈線接錯、放大器沒偏壓、溫度不對——這也是為什麼前面的周邊系統要做對。`,
});
S({ sec: '04 軟體與運作', title: '監控與聯鎖', anim: 'monitor', min: 2.5,
  async render(s) {
    H(s, '監控與聯鎖'); animPill(s, 'monitor');
    await pic(s, 'monitor', 0.6, 1.4, 6.0, 3.6, { alignX: 'left' });
    caption(s, '3D 場景 9：冷卻水中斷 → 告警、聯鎖、回收混合氣', 0.6, 5.05, 6.0);
    table(s, [['監控項目', '感測器 / 儀表'], ['50 K 級', 'PT100 / 矽二極體'], ['4 K、Still', 'Cernox'], ['Cold plate、MXC', 'RuO₂'], ['GHS', '壓力計 P1–P6、³He 流量計'], ['真空', 'OVC 真空計'], ['壓縮機', '冷卻水溫、氦壓、馬達狀態'], ['機房', '市電、UPS、室溫、濕度']], 6.9, 1.45, 5.85, [2.3, 3.55], { size: 12.5, rowH: 0.44 });
    para(s, ['**聯鎖**：冷卻水過溫 → 壓縮機停機；停電/控制器故障 → 閥門關閉、混合氣經背壓閥回儲存槽', '**遠端監控**：24 小時趨勢紀錄、簡訊/郵件告警、遠端操作'], 0.6, 5.5, 12.15, 1.3, { size: 14, bullet: true, space: 6 });
  },
  notes: `冷凍機一旦降溫，通常會連續運轉好幾個月，所以 24 小時監控非常重要。
溫度計依溫度範圍選擇：50 K 級用 PT100 或矽二極體，4 K 和 Still 用 Cernox，Cold plate 和 MXC 用氧化釕 RuO2，它們由專用的低溫溫控器以很小的激發電流讀取，避免自己加熱。GHS 有多個壓力計和 ³He 流量計；另外監控外真空、壓縮機的冷卻水溫和氦壓、以及機房的電力、溫濕度。
聯鎖的邏輯：冷卻水過溫，壓縮機自動停機保護自己；停電或控制器故障時，閥門關閉，混合氣經背壓閥自動回到儲存槽，保護昂貴的 ³He。
【切換到 3D 場景 9】選「冷卻水中斷」，可以看到水溫上升、超過門檻後壓縮機停機、各級開始升溫、告警燈轉紅、混合氣開始回收到儲存槽。也可以試試「真空洩漏」和「流阻堵塞」。`,
});
S({ sec: '04 軟體與運作', title: '常見故障與處置', anim: 'monitor', min: 2.5,
  async render(s) {
    H(s, '常見故障與處置'); animPill(s, 'monitor');
    table(s, [['故障', '徵兆', '自動動作', '人工處置'],
      ['停電', '壓縮機、冷卻水停止', 'UPS 維持控制；~10 分鐘後混合液沸騰 → 回收儲存槽', '復電後依序重啟，重新降溫（數小時～1 天）'],
      ['冷卻水中斷 / 過溫', '水溫上升', '壓縮機聯鎖停機', '恢復水路後重啟壓縮機；檢查冷卻水機'],
      ['流阻堵塞', '³He 流量下降、凝結壓力升高、MXC 升溫', '告警', '回收混合氣、清理冷阱；必要時升溫至 ~4 K 以上'],
      ['真空洩漏', 'OVC 壓力上升、各級升溫', '告警、停止循環', '檢漏（氦質譜）、更換密封、重新抽真空'],
      ['放大器 / 線路異常', '讀取 SNR 下降、找不到共振', '—', '檢查 HEMT/TWPA 偏壓、室溫連接、衰減值'],
      ['量子位元參數漂移', '保真度下降', '自動重校', '檢查 TLS 跳動、磁通偏壓、溫度'],
    ], 0.6, 1.45, 12.15, [2.0, 3.1, 3.4, 3.65], { size: 12, rowH: 0.7 });
    caption(s, '停電反應依 Bluefors LD 使用手冊；其餘為典型經驗，實際以設備手冊為準', 0.6, 6.55, 12.15);
  },
  notes: `這張表整理常見故障和處置方式，是實際運轉時最實用的一頁。
停電：壓縮機和冷卻水機停止，UPS 維持控制系統；大約十分鐘後混合液開始沸騰，閥門除了必要的之外全部關閉，混合氣經背壓閥回收到儲存槽。復電後依序重啟，重新降溫需要數小時到一天。
冷卻水中斷或過溫：壓縮機聯鎖停機，恢復水路後重啟。
流阻堵塞：³He 流量下降、凝結壓力上升、混合腔升溫，多半是雜質在冷阱或流阻處凍結，需要回收混合氣、清理冷阱，嚴重時要升溫。
真空洩漏：外真空壓力上升，各級升溫，需要用氦質譜檢漏儀找漏點。
放大器或線路異常：表現為讀取訊雜比下降或找不到共振，檢查偏壓和連接。
量子位元參數漂移：保真度下降，自動重校，必要時檢查 TLS 或磁通偏壓。
停電的反應依據 Bluefors 的使用手冊，其他是典型經驗，實際操作請以設備手冊為準。`,
});

// ===== 05 機房 =====
S({ sec: '05 機房基礎設施', layout: 'SECTION_DARK', title: '05 機房基礎設施', min: 0.5, render: sec('05', '機房基礎設施', '電力與 UPS · 冷卻水與環境 · 防振、接地與 EMI · 配置', 'infra', C.accent4), notes: `第五部分：機房基礎設施。` });
S({ sec: '05 機房基礎設施', title: '電力：一套系統約 25 kW', anim: 'infra', min: 2.5,
  async render(s) {
    H(s, '電力：一套系統約 25 kW'); animPill(s, 'infra');
    const P = [['脈衝管壓縮機', 10.7], ['冷卻水系統', 10.0], ['控制電子機櫃', 3.0], ['氣體處理系統', 1.5], ['電腦 / 監控', 1.0]];
    s.addChart(pres.charts.BAR, [{ name: '用電 (kW)', labels: P.map((p) => p[0]), values: P.map((p) => p[1]) }], { x: 0.6, y: 1.4, w: 7.0, h: 4.6, barDir: 'bar', ...CHART_BASE(), chartColors: [HEX.accent1], showLegend: false, showTitle: true, title: '典型用電分配（kW）', showValue: true, dataLabelPosition: 'outEnd', dataLabelFontSize: 11, dataLabelColor: '1A1F2B', dataLabelFormatCode: '0.0', catAxisOrientation: 'maxMin', objectName: 'chart-power' });
    caption(s, 'Google Sycamore：冷凍 ~10 kW + 冷卻水 ≥10 kW + 電子 ~3 kW，最壞 ~26 kW（Arute et al., 2019 補充資料）', 0.6, 6.05, 7.0);
    card(s, 7.9, 1.45, 4.85, 5.25);
    para(s, [{ t: '供電規劃', bold: true, color: C.accent4, size: 17 }, '**三相市電**（壓縮機、冷卻水機）', '**UPS** 供應：控制電子、電腦、GHS 控制器與閥門、溫控器、監控網路（建議 ≥ 1–2 小時）', '壓縮機通常**不接 UPS**（功率大）；停電時依程序安全回收混合氣', '可選：發電機自動切換，縮短停機時間', '電子機櫃前加**隔離變壓器**、乾淨電源，降低雜訊'], 8.15, 1.6, 4.4, 5.0, { size: 13.5, space: 9 });
  },
  notes: `電力規劃。一套以單台稀釋冷凍機為核心的系統，用電約 25 千瓦。最大的是脈衝管壓縮機，約 10.7 千瓦；冷卻水系統也約 10 千瓦；控制電子機櫃約 3 千瓦，系統越大越多；氣體處理系統和電腦監控各一兩千瓦。這和 Google Sycamore 論文補充資料裡公開的數字一致：冷凍約 10 kW、冷卻水 10 kW 以上、電子約 3 kW，最壞情況約 26 kW。
供電規劃的原則：壓縮機和冷卻水機用三相市電；控制電子、電腦、GHS 控制器和閥門、溫控器、監控網路接 UPS，建議至少撐一到兩小時，確保停電時能執行安全程序、保留監控紀錄。壓縮機功率太大，通常不接 UPS，停電時依程序回收混合氣即可；如果要縮短停機時間，可以加裝發電機自動切換。電子機櫃前建議加隔離變壓器，提供乾淨的電源。
【切換到 3D 場景 8】按「模擬停電」，可以看到市電斷開後哪些設備還在運作、哪些停止，右下角是停電後混合腔溫度的變化。`,
});
S({ sec: '05 機房基礎設施', title: '冷卻水、環境與公用設施', anim: 'infra', min: 2,
  async render(s) {
    H(s, '冷卻水、環境與公用設施'); animPill(s, 'infra');
    const items = [['wave', '冷卻水', 'PT415 壓縮機：11.5 L/min、入水 ≤ 27 °C；帶走 ~10 kW；建議閉迴路冷卻水機 + 流量/溫度監控', C.accent3],
      ['snow', '空調', '機房 10–35 °C、濕度 ≤ 80 % RH（30 °C）；電子機櫃需穩定溫度以減少相位漂移', C.accent2],
      ['cogs', '壓縮空氣', '~5 bar，驅動 GHS 氣動閥（停氣時常閉閥維持安全狀態）', C.accent6],
      ['layer', '液氮（選配）', '外部液氮冷阱；或選用內建冷阱以省去液氮補充', C.accent5],
      ['ruler', '空間與承重', '冷凍機框架 + 吊裝空間（開罐需挑高與吊車）；壓縮機可置於隔壁降噪', C.accent1]];
    items.forEach(([ic, t, d, col], i) => {
      const y = 1.45 + i * 1.05;
      iconCircle(s, ic, 0.6, y + 0.05, 0.62, col);
      sub(s, t, 1.4, y, 10, C.text1, 16.5);
      s.addText(d, { x: 1.4, y: y + 0.45, w: 11.3, h: 0.45, fontSize: 13.5, color: '4A5468', margin: 0, isTextBox: true });
    });
    caption(s, '環境與公用設施需求依 Bluefors LD 使用手冊；冷卻水規格依 PT415 規格', 0.6, 6.55, 12);
  },
  notes: `除了電力，機房還需要幾項公用設施。
冷卻水：以 PT415 為例，每分鐘 11.5 公升、入水溫度不超過 27 度，帶走約 10 千瓦的熱。建議用閉迴路的冷卻水機，並且監控流量和溫度，因為冷卻水中斷是最常見的停機原因之一。
空調：機房溫度 10 到 35 度、濕度在 30 度時不超過 80%。對量子電腦來說更重要的是溫度穩定，電子機櫃的溫度變化會造成相位漂移。
壓縮空氣：大約 5 bar，用來驅動 GHS 的氣動閥；停氣時常閉閥會維持在安全狀態。
液氮：如果用外部液氮冷阱就需要定期補充液氮；新機型多用內建冷阱。
空間與承重：冷凍機開罐換樣品需要挑高和吊裝設備；壓縮機可以放在隔壁房間降低噪音和振動。`,
});
S({ sec: '05 機房基礎設施', title: '防振、接地與電磁干擾', anim: 'infra', min: 2.5,
  async render(s) {
    H(s, '防振、接地與電磁干擾'); animPill(s, 'infra');
    const cols = [['防振', C.accent1, ['脈衝管 ~1.4 Hz 及諧波振動', '纜線摩擦起電 → 5–10 kHz 雜訊，影響相干性', '對策：遠端馬達、軟管固定、纜線綁紮/包覆（改善 > 10×）、避震座、剛性框架']],
      ['接地', C.accent5, ['單點（星形）接地，避免接地迴路', '冷凍機、機櫃、儀器共用同一參考', '電子機櫃前加隔離變壓器', 'DC 線使用雙絞、屏蔽與濾波']],
      ['電磁干擾', C.accent3, ['遠離大型馬達、變頻器、電梯', 'Wi-Fi 6E／7（5.9–7.1 GHz）落在量子位元與讀取腔頻段，須屏蔽', '磁屏蔽 + 遠離磁性物件（鋼構、磁鐵）', '室溫纜線使用高品質同軸、良好鎖緊']]];
    cols.forEach(([t, col, b], i) => {
      const x = 0.6 + i * 4.1; card(s, x, 1.45, 3.9, 4.75);
      sub(s, t, x + 0.25, 1.6, 3.4, col, 18);
      para(s, b, x + 0.25, 2.15, 3.45, 3.9, { size: 13.5, bullet: true, space: 8 });
    });
    caption(s, '振動與摩擦起電雜訊：Kalra et al., Rev. Sci. Instrum. 87, 073905 (2016)（量測對象為電子自旋量子位元）', 0.6, 6.4, 12);
  },
  notes: `防振、接地和電磁干擾這三項，常常是實驗室裡「莫名其妙」問題的來源。
防振：脈衝管在 1.4 Hz 和它的諧波上振動，會讓纜線彼此摩擦產生摩擦起電，形成 5 到 10 kHz 的雜訊，影響量子位元相干性。研究顯示把纜線固定、包覆可以改善十倍以上；這篇研究量測的是電子自旋量子位元，但振動透過摩擦起電耦合到纜線的機制，同樣存在於超導系統的直流與控制線上；另外可以用遠端馬達、固定軟管、避震座和剛性框架。
接地：採用單點星形接地，避免接地迴路；冷凍機、機櫃和儀器共用同一個參考點；電子機櫃前加隔離變壓器；直流線用雙絞、屏蔽並且濾波。
電磁干擾：遠離大型馬達、變頻器和電梯；Wi-Fi 和手機頻段要特別注意：Wi-Fi 6E 和 Wi-Fi 7 使用 5.925 到 7.125 GHz，正好落在超導量子位元和讀取諧振腔的頻段，5G 的 3.3 到 5 GHz 也很接近，所以一定要做好屏蔽；遠離鋼構和磁鐵等磁性物件；室溫段的同軸線要用高品質的並確實鎖緊。`,
});
S({ sec: '05 機房基礎設施', title: '機房配置建議', anim: 'infra', min: 2,
  async render(s) {
    H(s, '機房配置建議'); animPill(s, 'infra');
    await pic(s, 'infra', 0.6, 1.4, 7.3, 4.8, { alignX: 'left' });
    caption(s, '3D 場景 8：電力（黃）、UPS 供電（淡黃）、冷卻水、接地、空調；可模擬停電', 0.6, 6.25, 7.3);
    card(s, 8.2, 1.45, 4.55, 5.25);
    para(s, [{ t: '配置原則', bold: true, color: C.accent1, size: 17 }, '冷凍機置中，四周留維護與開罐空間', '電子機櫃靠近冷凍機頂板 → 縮短室溫纜線', '壓縮機、冷卻水機放隔壁或室外 → 噪音、振動、廢熱隔離', 'GHS 與儲存槽靠近冷凍機 → 抽氣管短', '頂部線槽分開：微波/直流 vs 電力', '單點接地、UPS 與配電盤集中'], 8.45, 1.6, 4.1, 5.0, { size: 13.5, space: 8 });
  },
  notes: `最後整理機房配置的原則。
冷凍機放在中間，四周留維護和開罐的空間；電子機櫃靠近冷凍機頂板，縮短室溫段的纜線，減少損耗和相位漂移；壓縮機和冷卻水機放在隔壁或室外，把噪音、振動和廢熱隔離開；GHS 和儲存槽靠近冷凍機，因為 Still 抽氣管越短越好；頂部線槽要把微波直流線和電力線分開走；接地、UPS 和配電盤集中管理。
【在 3D 場景 8 中可以從不同角度看這個配置】`,
});

// ===== 06 整合 =====
S({ sec: '06 系統整合', layout: 'SECTION_DARK', title: '06 系統整合', min: 0.5, render: sec('06', '系統整合', '連接清單 · 從零到上線檢查表 · 規模化趨勢', 'overview', C.accent6), notes: `第六部分：把所有東西連起來。` });
S({ sec: '06 系統整合', title: '系統連接清單（一）：冷卻、氣體與真空', anim: 'overview', min: 2.5,
  async render(s) {
    H(s, '系統連接清單（一）：冷卻、氣體與真空'); animPill(s, 'overview');
    table(s, [['從', '到', '介質 / 接頭', '注意事項'],
      ['冷卻水機', '氦壓縮機', '冷卻水 進/回（快速接頭）', '流量 ~11.5 L/min、≤ 27 °C；裝流量與溫度監控'],
      ['氦壓縮機', '脈衝管冷頭', '高壓 / 低壓 氦軟管（自封接頭）', '充氦壓力依規格；軟管固定避免振動'],
      ['壓縮機', '旋轉閥馬達', '馬達電源線', '遠端馬達選配'],
      ['GHS', '冷凍機 Still', 'Still 抽氣管（大口徑 KF/ISO）', '越短越好；渦輪泵 + 乾式前級泵'],
      ['GHS', '冷凍機凝結管線', '凝結回流管（小口徑，經冷阱）', '冷阱定期再生；避免雜質'],
      ['GHS', '混合氣儲存槽', '儲存/回收管 + 背壓閥', '確認背壓閥（~1.1–1.2 bar）作動'],
      ['GHS 泵', '外真空罩（OVC）', '真空管（KF）', '降溫前抽真空並以氦質譜檢漏'],
      ['壓縮空氣', 'GHS 氣動閥', '~5 bar 氣管', '斷氣時常閉閥維持安全'],
    ], 0.6, 1.45, 12.15, [1.7, 2.0, 3.5, 4.95], { size: 12, rowH: 0.56 });
  },
  notes: `第六部分把前面所有內容整理成一張「系統連接清單」，這兩頁也對應到書面指南裡的連接表。
第一張是冷卻、氣體和真空：冷卻水機的進回水接到壓縮機，要裝流量和溫度監控；壓縮機的高低壓氦軟管接到冷頭，軟管要固定；遠端馬達的電源線；GHS 的 Still 抽氣管是大口徑的，越短越好；凝結回流管經過冷阱；GHS 和儲存槽之間的回收管與背壓閥；GHS 的泵連到外真空罩；以及壓縮空氣接到 GHS 的氣動閥。
每一項的「注意事項」都是實際建置時常出問題的地方。`,
});
S({ sec: '06 系統整合', title: '系統連接清單（二）：訊號、資料與電力', anim: 'overview', min: 2.5,
  async render(s) {
    H(s, '系統連接清單（二）：訊號、資料與電力'); animPill(s, 'overview');
    table(s, [['從', '到', '介質 / 接頭', '注意事項'],
      ['AWG / 讀取輸出', '冷凍機頂板', 'SMA 同軸 → 密封接頭', '依線路圖標號；量測每條穿透與衰減'],
      ['冷凍機頂板', '讀取 ADC', '輸出同軸（經室溫放大）', '確認 HEMT 偏壓後再量 SNR'],
      ['DC 源', '頂板直流接頭', 'Fischer / micro-D 線束 + 濾波', '磁通、HEMT、TWPA 偏壓；上電順序'],
      ['溫控器', '溫度計 / 加熱器', '低溫直流線束', '各級溫度計校正曲線'],
      ['銣鐘', '所有儀器', '10 MHz 參考 + 觸發/同步線', '等長纜線；確認全部鎖相'],
      ['控制電腦', '儀器 / GHS / 溫控器', '乙太網路（獨立網段）', '時間同步（NTP）、遠端存取權限'],
      ['控制電腦', '雲端 / 使用者', '網路 + 防火牆', 'API、佇列、身分驗證'],
      ['配電盤 / UPS', '所有設備', '三相 / 單相電源', '關鍵負載接 UPS；單點接地'],
    ], 0.6, 1.45, 12.15, [1.8, 2.0, 3.3, 5.05], { size: 12, rowH: 0.56 });
  },
  notes: `第二張是訊號、資料和電力：AWG 和讀取模組透過 SMA 同軸連到冷凍機頂板的密封接頭，依線路圖標號，每條線都要量穿透和衰減；輸出線經室溫放大接到讀取 ADC；DC 源透過直流線束接到頂板，提供磁通、HEMT 和 TWPA 偏壓，要注意上電順序；溫控器接溫度計和加熱器；銣鐘的 10 MHz 參考和觸發同步線接到所有儀器，要確認全部鎖相；控制電腦用獨立網段連所有儀器、GHS 和溫控器；對外透過防火牆提供雲端服務；配電盤和 UPS 供電給所有設備，關鍵負載接 UPS，並採單點接地。
這兩張表加起來，就是讓量子電腦「連起來」的完整清單。`,
});
S({ sec: '06 系統整合', title: '從零到上線：整合檢查表', anim: 'bringup', min: 3,
  async render(s) {
    H(s, '從零到上線：整合檢查表'); animPill(s, 'bringup');
    const ph = [['設施就緒', ['三相電、UPS、接地', '冷卻水機與水路', '壓縮空氣、空調', '網路與時間同步'], C.accent4],
      ['冷卻系統', ['壓縮機 ↔ 冷頭軟管', '冷卻水試運轉', 'GHS 泵、閥、儲存槽', '控制軟體連線'], C.accent3],
      ['低溫佈線', ['裝線、熱錨定', '室溫/低溫各量一次穿透', '屏蔽、樣品盒、打線', '關罐、抽真空、檢漏'], C.accent2],
      ['降溫', ['脈衝管預冷', '凝結混合氣', '循環到基溫', '確認各級溫度'], '8A5CD0'],
      ['電子與校準', ['儀器鎖相、觸發', 'HEMT/TWPA 偏壓', '自動校準流程', '基準測試 → 上線'], C.accent5]];
    ph.forEach(([t, items, col], i) => {
      const x = 0.6 + i * 2.47;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.45, w: 2.3, h: 0.7, rectRadius: 0.08, fill: { color: col }, line: { color: col, width: 0 }, objectName: oname('phase') });
      s.addText(`${i + 1}. ${t}`, { x, y: 1.45, w: 2.3, h: 0.7, fontSize: 15, bold: true, color: C.background1, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
      card(s, x, 2.3, 2.3, 3.6);
      items.forEach((it, k) => {
        s.addShape(pres.shapes.RECTANGLE, { x: x + 0.2, y: 2.55 + k * 0.82, w: 0.24, h: 0.24, fill: { color: C.background1 }, line: { color: col, width: 1.5 }, objectName: oname('checkbox') });
        s.addText(it, { x: x + 0.55, y: 2.45 + k * 0.82, w: 1.65, h: 0.7, fontSize: 12.5, color: C.text1, margin: 0, isTextBox: true, valign: 'top' });
      });
    });
    s.addText('完整步驟與數值請見 docs/周邊系統連接與啟動指南.md', { x: 0.6, y: 6.15, w: 12.15, h: 0.45, fontSize: 14, bold: true, color: C.accent1, margin: 0, isTextBox: true });
  },
  notes: `這頁是一份從零到上線的整合檢查表，分五個階段，每階段四項。
第一，設施就緒：三相電、UPS、接地；冷卻水機和水路；壓縮空氣和空調；網路與時間同步。第二，冷卻系統：壓縮機到冷頭的軟管、冷卻水試運轉、GHS 的泵閥和儲存槽、控制軟體連線。第三，低溫佈線：裝線並熱錨定、室溫和低溫各量一次穿透、屏蔽樣品盒和打線、關罐抽真空檢漏。第四，降溫：預冷、凝結、循環、確認各級溫度。第五，電子與校準：儀器鎖相和觸發、HEMT 和 TWPA 偏壓、自動校準流程、基準測試後上線。
每一項的細節和數值都寫在書面的《周邊系統連接與啟動指南》裡，建置時可以逐項勾選。`,
});
S({ sec: '06 系統整合', title: '規模化趨勢', min: 2,
  async render(s) {
    H(s, '規模化趨勢');
    const t = [['cubes', '更大的冷凍平台', 'Bluefors KIDE：> 90 μW @20 mK、> 4000 條 RF 線、9 支脈衝管，目標 1000+ 量子位元；IBM Goldeneye 概念機 1.7 m³', C.accent3],
      ['link', '模組化與互連', '多台冷凍機/多晶片以低溫微波或光學互連；IBM 已展示連結的模組化低溫腔', C.accent2],
      ['chip', '低溫控制電子', 'Cryo-CMOS（例：Intel Horse Ridge II，4 K 工作）、SFQ 邏輯 → 減少室溫到低溫的線數', C.accent1],
      ['stream', '高密度佈線', '扁平/柔性纜線、多工、整合濾波 → 降低每通道熱負載與體積', C.accent5],
      ['fire', '³He 供應', '價格與供應成為瓶頸；長期採購合約、回收、替代冷卻技術研究中', C.accent4]];
    t.forEach(([ic, h, d, col], i) => {
      const y = 1.45 + i * 1.05;
      iconCircle(s, ic, 0.6, y + 0.05, 0.62, col);
      sub(s, h, 1.4, y, 11, C.text1, 16.5);
      s.addText(d, { x: 1.4, y: y + 0.45, w: 11.3, h: 0.45, fontSize: 13.5, color: '4A5468', margin: 0, isTextBox: true });
    });
    caption(s, '來源：Bluefors KIDE 產品頁、IBM Quantum blog（Goldeneye）、Intel 新聞稿（Horse Ridge II）、Science (2026) ³He 報導', 0.6, 6.55, 12);
  },
  notes: `最後看規模化的趨勢。周邊系統是超導量子電腦擴展到上千、上百萬顆量子位元的主要瓶頸之一。
第一，更大的冷凍平台：Bluefors 的 KIDE 在 20 mK 有超過 90 μW、可裝超過 4000 條射頻線，目標支援上千顆量子位元；IBM 也展示過 1.7 立方公尺的 Goldeneye 概念機。
第二，模組化與互連：用多台冷凍機、多顆晶片，透過低溫微波或光學鏈路互連。
第三，低溫控制電子：把部分控制電路做成能在 4 K 工作的 cryo-CMOS，例如 Intel 的 Horse Ridge II，或是 SFQ 超導邏輯，減少從室溫拉下來的線。
第四，高密度佈線：扁平柔性纜線、多工和整合濾波。
第五，³He 的供應：價格和供應已經成為瓶頸，業界在簽長期合約、做回收，也在研究替代的冷卻技術。`,
});
S({ sec: '06 系統整合', title: '重點回顧', min: 2,
  async render(s) {
    H(s, '重點回顧');
    const tk = [['量子電腦是一個系統', '晶片之外：低溫、佈線、電子、軟體、機房五大子系統缺一不可'],
      ['冷卻功率逐級遞減', '50 K 30 W → 4 K 1.5 W → MXC ~20 μW；熱負載要擋在上層'],
      ['佈線決定規模', '每顆量子位元 ~2.5 條 RF 線；被動熱傳導與空間是主要瓶頸'],
      ['電子要同步、要快', '10 MHz 參考鎖相、奈秒對齊、數百奈秒即時回饋'],
      ['設施決定可用率', '~25 kW 電力、10 kW 冷卻水、UPS、聯鎖與 24 小時監控；³He 不能外洩']];
    tk.forEach(([t, d], i) => {
      const y = 1.5 + i * 1.05;
      numCircle(s, i + 1, 0.6, y + 0.12, 0.62, [C.accent3, C.accent2, C.accent1, C.accent5, C.accent4][i]);
      sub(s, t, 1.45, y, 11.2, C.text1, 19);
      s.addText(runs(d), { x: 1.45, y: y + 0.47, w: 11.2, h: 0.45, fontSize: 14.5, color: '4A5468', margin: 0, isTextBox: true });
    });
  },
  notes: `用五句話回顧：
第一，量子電腦是一個系統，晶片之外的低溫、佈線、電子、軟體、機房五大子系統缺一不可。
第二，冷卻功率逐級遞減，從 50 K 的 30 W 到混合腔的 20 μW，熱負載要擋在上層。
第三，佈線決定規模，每顆量子位元大約需要兩條半射頻線，被動熱傳導和空間是主要瓶頸。
第四，電子要同步、要快：10 MHz 參考鎖相、奈秒等級對齊、數百奈秒的即時回饋。
第五，設施決定可用率：大約 25 kW 電力、10 kW 冷卻水、UPS、聯鎖和 24 小時監控，而且 ³He 絕對不能外洩。`,
});
S({ sec: '06 系統整合', title: '3D 動畫導覽（animations/peripherals.html）', min: 1,
  async render(s) {
    H(s, '3D 動畫導覽');
    table(s, [['場景', '主題', '對應投影片'], ['1 系統全景', '機房設備與 7 類連接', '3、11、35–36'], ['2 脈衝管冷卻', '旋轉閥、蓄冷器、壓縮機', '8'], ['3 稀釋冷凍原理', '³He 循環、Q̇ = 84ṅT²', '9'], ['4 降溫流程', '各級溫度隨時間', '12'], ['5 低溫佈線', '6 類線路、熱負載預算', '14–16'], ['6 控制電子學', '量測–回饋循環、時脈', '20–21'], ['7 軟體堆疊', '下傳與回傳', '25'], ['8 機房基礎設施', '電力、冷卻水、停電模擬', '30–33'], ['9 監控與聯鎖', '故障情境', '27–28'], ['10 啟動與校準', '11 步驟與量測圖', '26、37']],
      0.6, 1.4, 7.6, [2.4, 3.4, 1.8], { size: 12.5, rowH: 0.45 });
    card(s, 8.5, 1.45, 4.25, 5.25);
    para(s, [{ t: '操作方式', bold: true, color: C.accent2, size: 18 }, '瀏覽器開啟 animations/peripherals.html（離線可用）', '網址加 #場景代號直接跳轉', '投影片右上角「▶ 3D 場景」按鈕可直接開啟', '← → 切換、空白鍵暫停、H 隱藏面板、F 全螢幕', 'JJ 與讀取原理的動畫在 index.html'], 8.75, 1.6, 3.8, 5.0, { size: 14, space: 9 });
  },
  notes: `這頁是 3D 動畫的導覽。這次的動畫在 animations/peripherals.html，共 10 個場景，和上一次 JJ 與讀取的動畫 index.html 互相連結。操作方式和上次相同。`,
});
S({ sec: '06 系統整合', title: '參考資料', min: 0.5,
  async render(s) {
    H(s, '參考資料');
    para(s, [
      'S. Krinner et al., "Engineering cryogenic setups for 100-qubit scale superconducting circuit systems," EPJ Quantum Technol. 6, 2 (2019).',
      'P. Krantz et al., "A quantum engineer\'s guide to superconducting qubits," Appl. Phys. Rev. 6, 021318 (2019).',
      'F. Arute et al., "Quantum supremacy using a programmable superconducting processor," Nature 574, 505 (2019)（補充資料：功耗）.',
      'R. Barends et al., "Minimizing quasiparticle generation from stray infrared light," Appl. Phys. Lett. 99, 113507 (2011).',
      'R. Kalra et al., "Vibration-induced electrical noise in a cryogen-free dilution refrigerator: characterization, mitigation, and impact on qubit coherence," Rev. Sci. Instrum. 87, 073905 (2016).',
      'L. Stefanazzi et al., "The QICK (Quantum Instrumentation Control Kit)," Rev. Sci. Instrum. 93, 044709 (2022).',
      'Bluefors：LD / XLD / KIDE 產品頁與 LD 使用手冊；PT415、PT420 脈衝管規格。',
      'Oxford Instruments ProteoxMX 規格；Zurich Instruments SHFQC+ 規格與主動重置說明；Qblox 產品文件；Keysight M5300A 規格；QDevil QDAC-II。',
      'Fermilab QSC Cryogenics Course（稀釋冷卻功率公式）；Science (2026) 關於 ³He 供應的報導。',
    ], 0.6, 1.45, 12.15, 5.3, { size: 13, bullet: true, space: 6 });
  },
  notes: `這頁是參考資料。最推薦的是 Krinner 等人 2019 年的論文，它完整記錄了一套 100 顆量子位元等級的低溫系統怎麼設計，今天很多數字都來自這篇；Krantz 的工程師指南也有一章談控制和讀取硬體。廠商的規格書和使用手冊則是實際建置時最直接的參考。`,
});
S({ sec: '06 系統整合', layout: 'TITLE_DARK', title: 'Q & A', min: 10,
  async render(s) {
    s.addText('Q & A', { placeholder: 'title' });
    s.addText('謝謝大家！歡迎提問與討論', { placeholder: 'body' });
    await pic(s, 'infra', 7.7, 1.0, 5.4, 5.4);
  },
  notes: `以上就是今天的分享，謝謝大家，歡迎提問。（備用問答請參考演講稿最後的「Q&A 準備」。）`,
});

const QA = [
  ['為什麼不用液氦「濕式」冷凍機？', '濕式系統需要定期補充液氦，運轉成本高且液氦供應不穩；乾式（脈衝管）系統只需電力與冷卻水即可連續運轉數月，維護簡單，是目前量子電腦的主流。代價是脈衝管的振動與較大的電力需求。'],
  ['一台稀釋冷凍機能放多少顆量子位元？', '取決於線路空間與熱負載：XLD 等級約可支援數百顆（最多 ~1000 條同軸）；KIDE 等平台以 1000+ 顆為目標。更大規模需要低溫電子、高密度佈線或多台互連。'],
  ['停電時量子位元的資料會怎樣？', '量子態本來就只維持微秒等級，不存在「資料遺失」問題；真正的影響是系統升溫後需要重新降溫與重新校準，造成數小時到一天的停機。'],
  ['控制電子可以全部放進冷凍機嗎？', '目前功耗太大：MXC 只有 ~20 μW，4 K 也只有 ~1.5 W。Cryo-CMOS 與 SFQ 正在發展，先從 4 K 級開始部分整合。'],
  ['³He 這麼貴，會不會用完？', '在封閉迴路中 ³He 不會消耗，只要系統不洩漏即可長期使用；問題在於新建系統的需求量。業界正以長期供應合約、回收與替代技術因應。'],
  ['建置一套系統大約要多久？', '設施就緒後，冷凍機安裝與佈線約數週；首次降溫約 1–2 天；完整校準到上線約數天到數週，視量子位元數與自動化程度而定。'],
];

(async () => {
  await loadIcons();
  let cur = null;
  for (const sd of SLIDES) {
    if (sd.sec !== cur) { pres.addSection({ title: sd.sec }); cur = sd.sec; }
    const slide = pres.addSlide({ masterName: sd.layout || 'CONTENT', sectionTitle: sd.sec });
    await sd.render(slide);
    const cue = sd.anim ? `【3D 動畫】場景 ${SCENES[sd.anim][0]}「${SCENES[sd.anim][1]}」：animations/peripherals.html#${sd.anim}\n` : '';
    slide.addNotes(`${cue}【建議時間】約 ${sd.min} 分鐘\n\n${sd.notes}`);
  }
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log('written', OUT, SLIDES.length, 'slides');
  const total = SLIDES.reduce((a, b) => a + b.min, 0);
  let md = `# 演講稿：量子電腦的周邊系統 —— 讓 10 mK 的晶片真正運轉\n\n`;
  md += `> 本稿與 \`slides/QC_Peripheral_Systems_Talk.pptx\` 的講者備註同步產生（來源：\`slides/build/build_peripherals.js\`）。\n`;
  md += `> 共 ${SLIDES.length} 張投影片，預估總時長約 ${Math.round(total)} 分鐘（含 Q&A 約 10 分鐘）。建置細節請見 \`docs/周邊系統連接與啟動指南.md\`。\n\n`;
  md += `## 使用方式\n\n- 標示【切換到 3D 場景 N】時，點投影片右上角按鈕，或開啟 \`animations/peripherals.html#場景代號\`。\n- 3D 操作：← → 切換、空白鍵暫停、H 隱藏面板、F 全螢幕、R 重設視角。\n\n## 時間規劃\n\n| 段落 | 投影片 | 時間（分） |\n|---|---|---|\n`;
  const secs = {};
  SLIDES.forEach((s, i) => { (secs[s.sec] ||= { a: i + 1, b: i + 1, t: 0 }); secs[s.sec].b = i + 1; secs[s.sec].t += s.min; });
  Object.entries(secs).forEach(([k, v]) => { md += `| ${k} | ${v.a}–${v.b} | ${v.t} |\n`; });
  md += `\n### 60 分鐘精簡版建議\n\n可略過或快速帶過：第 10 頁（冷卻功率曲線）、第 17 頁（纜線材料）、第 21 頁（產品比較）、第 28 頁（故障表，可會後閱讀）、第 33 頁（機房配置）、第 38 頁（規模化趨勢）；Q&A 縮短為 5 分鐘。\n\n---\n`;
  cur = null;
  SLIDES.forEach((s, i) => {
    if (s.sec !== cur) { md += `\n## ${s.sec}\n`; cur = s.sec; }
    md += `\n### 第 ${i + 1} 頁：${s.title.replace(/\n/g, '').replace(/[_^]\{([^}]*)\}/g, '$1')}\n\n- 建議時間：約 ${s.min} 分鐘\n`;
    if (s.anim) md += `- 3D 動畫：場景 ${SCENES[s.anim][0]}「${SCENES[s.anim][1]}」→ \`animations/peripherals.html#${s.anim}\`\n`;
    md += `\n${s.notes.split('\n').map((l) => l.trim()).filter(Boolean).join('\n\n')}\n`;
  });
  md += `\n---\n\n## Q&A 準備\n\n`;
  QA.forEach(([q, a], i) => { md += `**Q${i + 1}. ${q}**\n\n${a}\n\n`; });
  fs.writeFileSync(SPEECH, md);
  console.log('written', SPEECH);
})().catch((e) => { console.error(e); process.exit(1); });

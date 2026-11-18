/* 產生簡報：超導量子電腦的 JJ 元件與微波讀取
 * 用法：node build_deck.js
 * 需要：pptxgenjs、sharp、react、react-dom、react-icons（見 README）
 * 輸出：../JJ_Microwave_Readout_Talk.pptx 與 ../../speech/演講稿.md（由同一份講者備註生成）
 */
const fs = require('fs');
const path = require('path');

const { applyTheme } = require('./apply_theme');
const ROOT = path.resolve(__dirname, '..');
const FIG = path.join(ROOT, 'figures');
const OUT = path.join(ROOT, 'JJ_Microwave_Readout_Talk.pptx');
const SPEECH = path.resolve(ROOT, '..', 'speech', '演講稿.md');
const ANIM_REL = 'https://pcpcchen-coder.github.io/QuantumComputing/animations/index.html'; // GitHub Pages 網址

const SCENES = {
  bloch: [1, 'Bloch 球'], cooper: [2, 'Cooper pair'], jj: [3, 'JJ 結構'], potential: [4, '能階與非諧性'], washboard: [5, '洗衣板位勢'], squid: [6, 'SQUID'],
  fab: [7, 'JJ 製程'], chip: [8, '晶片與多工讀取'], dispersive: [9, '色散讀取'], iq: [10, 'IQ 判別'], fridge: [11, '低溫讀取鏈'],
};
const { makeDeck } = require('./deck_lib');
const D = makeDeck({ title: '超導量子電腦：JJ 元件與微波讀取', subject: '約瑟夫森接面、transmon 與色散讀取技術分享', footer: '超導量子電腦 · JJ 元件與微波讀取', scenes: SCENES, animRel: ANIM_REL });
const { pres, C, HEX, THEME, link, loadIcons, card, iconCircle, numCircle, runs, para, eqBox, fitImage, caption, animPill, table, chevrons, shadow, oname } = D;
/* ---------------- 投影片內容 ---------------- */
const SLIDES = [];
const S = (o) => SLIDES.push(o);
const IMG3 = (n) => path.join(FIG, '3d', n + '.jpg');
const IMGF = (n) => path.join(FIG, n + '.png');

// ===== 開場 =====
S({ sec: '開場', layout: 'TITLE_DARK', title: '超導量子電腦的核心：\n約瑟夫森接面（JJ）與微波讀取', min: 1.5,
  async render(s) {
    s.addText(runs('超導量子電腦的核心：\n約瑟夫森接面（JJ）與微波讀取'), { placeholder: 'title' });
    s.addText('從超導物理、JJ 元件、transmon 量子位元，到用微波讀出 |0⟩ 與 |1⟩', { placeholder: 'body' });
    await fitImage(s, IMG3('chip'), 8.0, 0.9, 5.1, 5.7, { crop: { left: 640, top: 170, width: 1580, height: 1120 }, alt: '量子晶片 3D 模型' });
    s.addText('技術分享 · 搭配互動 3D 動畫（animations/index.html）', { x: 0.7, y: 6.55, w: 7.2, h: 0.4, fontSize: 13, color: 'A8B4C6', margin: 0, isTextBox: true });
  },
  notes: `各位同仁大家好。今天想跟大家分享超導量子電腦裡最核心的兩件事：第一是「約瑟夫森接面」，也就是 Josephson Junction，簡稱 JJ；第二是我們怎麼用微波，去讀出一顆量子位元到底是 0 還是 1。
為什麼挑這兩個主題？因為 JJ 是讓超導電路變成「量子位元」的唯一關鍵元件，沒有它，電路就只是一個普通的 LC 振盪器；而讀取則是整台量子電腦和外界溝通的出口，讀不準，前面算得再好也沒用。
今天的分享會搭配一組互動 3D 動畫，每到一個主題，我會切換到對應的場景，用動畫把抽象的物理畫面化。投影片右上角有藍綠色的「3D 場景」按鈕，點下去就會打開對應的動畫。`,
});
S({ sec: '開場', title: '今日議程', min: 1.5,
  async render(s) {
    s.addText(runs('今日議程'), { placeholder: 'title' });
    const items = [
      ['01', '背景知識', '量子位元、超導、Cooper pair、磁通量子化、為什麼需要非線性', C.accent3],
      ['02', 'JJ 元件', '結構與 Josephson 關係式、E_{J} 與 E_{C}、SQUID、transmon、製程與雜訊', C.accent1],
      ['03', '微波讀取', '電路 QED、色散位移、IQ 解調、單發判別、低溫讀取鏈、量子極限放大器', C.accent2],
      ['04', '整合與總結', '從 JJ 到讀出位元的完整流程、重點回顧、3D 動畫導覽', C.accent5],
    ];
    items.forEach(([n, t, d, col], i) => {
      const x = 0.6 + i * 3.08, y = 1.55;
      card(s, x, y, 2.85, 4.6);
      s.addText(n, { x: x + 0.3, y: y + 0.3, w: 2.2, h: 0.9, fontSize: 44, bold: true, color: col, margin: 0, isTextBox: true, fontFace: 'Arial' });
      s.addText(t, { x: x + 0.3, y: y + 1.3, w: 2.3, h: 0.5, fontSize: 21, bold: true, color: C.text1, margin: 0, isTextBox: true });
      para(s, [d], x + 0.3, y + 1.95, 2.3, 2.4, { size: 14, color: '4A5468' });
    });
    s.addText('全程約 90–100 分鐘（含 Q&A）；時間有限時可改用演講稿中的 60 分鐘精簡版 · 每個主題搭配互動 3D 動畫', { x: 0.6, y: 6.35, w: 12, h: 0.4, fontSize: 14, color: C.accent6, italic: true, margin: 0, isTextBox: true });
  },
  notes: `今天的內容分成四個部分。
第一部分是背景知識：先複習量子位元是什麼、評估它好壞的指標，再介紹超導現象、Cooper pair、磁通量子化，最後回答一個關鍵問題：為什麼一定要有「非線性」元件。
第二部分是今天的主角 JJ：從它的三明治結構、兩條 Josephson 關係式，談到它為什麼是一個「非線性電感」，再延伸到 SQUID、transmon 量子位元、製程怎麼做、以及造成退相干的雜訊來源。
第三部分是微波讀取：電路量子電動力學（circuit QED）的架構、色散讀取的原理、IQ 解調與單發判別，還有整條從室溫到 10 mK 再回到室溫的讀取鏈，以及量子極限放大器。
最後第四部分把整個流程串起來，並做重點回顧。完整版大約一個半小時，最後留時間給大家提問。`,
});
S({ sec: '開場', title: '為什麼是超導量子電腦？', min: 2,
  async render(s) {
    s.addText(runs('為什麼是超導量子電腦？'), { placeholder: 'title' });
    const stats = [['10 mK', '工作溫度\n（比外太空冷 ~300 倍）', C.accent3], ['~5 GHz', '量子位元頻率\n（微波頻段）', C.accent1], ['20–50 ns', '單量子位元閘\n時間', C.accent2], ['> 99 %', '讀取保真度\n（數百 ns 內完成）', C.accent5]];
    stats.forEach(([v, l, col], i) => {
      const x = 0.6 + i * 3.08;
      card(s, x, 1.5, 2.85, 2.25);
      s.addText(v, { x, y: 1.65, w: 2.85, h: 1.0, fontSize: 40, bold: true, color: col, align: 'center', valign: 'middle', margin: 0, isTextBox: true, fontFace: 'Arial' });
      s.addText(l, { x, y: 2.7, w: 2.85, h: 0.9, fontSize: 14, color: '4A5468', align: 'center', valign: 'top', margin: 0, isTextBox: true });
    });
    iconCircle(s, 'check', 0.6, 4.25, 0.55, C.accent5);
    s.addText('優勢', { x: 1.3, y: 4.25, w: 4, h: 0.55, fontSize: 20, bold: true, color: C.text1, valign: 'middle', margin: 0, isTextBox: true });
    para(s, ['以**半導體微影製程**製作，可沿用既有晶圓技術擴展', '電路參數（頻率、耦合）可**設計**，不受自然原子限制', '閘操作快（奈秒級），已展示**低於容錯閾值**的量子糾錯'], 0.6, 4.95, 5.9, 1.8, { size: 15, bullet: true });
    iconCircle(s, 'snow', 6.85, 4.25, 0.55, C.accent4);
    s.addText('挑戰', { x: 7.55, y: 4.25, w: 4, h: 0.55, fontSize: 20, bold: true, color: C.text1, valign: 'middle', margin: 0, isTextBox: true });
    para(s, ['相干時間仍有限（T_{1}、T_{2} 約 0.1–1 ms 量級）', '需稀釋冷凍機與大量**微波佈線**，擴展受限', '製程變異造成頻率散佈，需**頻率定位**技術'], 6.85, 4.95, 5.9, 1.8, { size: 15, bullet: true });
  },
  notes: `在各種量子電腦平台中——離子阱、中性原子、光子、矽自旋——超導路線是目前產業界投入最多的一條，Google、IBM 都是這條路線。
先看幾個數字建立直覺：它工作在大約 10 mK，比外太空的 2.7 K 還冷三百倍；量子位元的頻率約 5 GHz，剛好是微波頻段，所以我們所有控制和讀取都靠微波；單量子位元閘只要二三十奈秒；讀取在幾百奈秒內就能有 99% 以上的保真度。
優勢是：它是用類似半導體的微影製程做出來的，可以沿用既有製程技術；它是「人造原子」，頻率、耦合強度都可以設計；而且速度快，近年已經展示了錯誤率低於容錯閾值的量子糾錯。
挑戰則是：相干時間還是有限；整台機器要放進稀釋冷凍機，每顆量子位元都要好幾條微波線；以及製程變異會讓每顆量子位元頻率不一樣——這點跟 JJ 的製程直接相關，等一下會詳細講。`,
});

// ===== 01 背景知識 =====
S({ sec: '01 背景知識', layout: 'SECTION_DARK', title: '01 背景知識', min: 0.5,
  async render(s) {
    s.addText('01', { x: 0.7, y: 1.3, w: 3, h: 1.4, fontSize: 80, bold: true, color: C.accent1, margin: 0, isTextBox: true, fontFace: 'Arial' });
    s.addText(runs('背景知識'), { placeholder: 'title' });
    s.addText('量子位元 · 超導 · Cooper pair · 磁通量子化 · 非線性', { placeholder: 'body' });
    await fitImage(s, IMG3('bloch'), 8.2, 1.0, 4.6, 5.4, { crop: { left: 700, top: 0, width: 1160, height: 1440 } });
  },
  notes: `我們先從背景知識開始。這部分是為了讓沒有物理背景的同仁也能跟上，如果大家已經很熟悉，我會講快一點。`,
});
S({ sec: '01 背景知識', title: '位元 vs 量子位元：疊加與 Bloch 球', anim: 'bloch', min: 2.5,
  async render(s) {
    s.addText(runs('位元 vs 量子位元：疊加與 Bloch 球'), { placeholder: 'title' }); animPill(s, 'bloch');
    card(s, 0.6, 1.5, 3.0, 2.3); card(s, 3.85, 1.5, 3.0, 2.3);
    s.addText('古典位元', { x: 0.85, y: 1.65, w: 2.6, h: 0.45, fontSize: 18, bold: true, color: C.text1, margin: 0, isTextBox: true });
    para(s, ['只能是 0 **或** 1', '讀取不改變狀態', '可任意複製'], 0.85, 2.2, 2.6, 1.5, { size: 14, bullet: true });
    s.addText('量子位元', { x: 4.1, y: 1.65, w: 2.6, h: 0.45, fontSize: 18, bold: true, color: C.accent2, margin: 0, isTextBox: true });
    para(s, ['可處於 |0⟩ 與 |1⟩ 的**疊加**', '量測會「塌縮」到 0 或 1', '不可複製（no-cloning）'], 4.1, 2.2, 2.6, 1.5, { size: 14, bullet: true });
    eqBox(s, ['|ψ⟩ = cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩', { t: 'P(1) = sin²(θ/2)', size: 16, color: C.accent6 }], 0.6, 4.05, 6.25, 1.25);
    para(s, ['**Bloch 球**：北極 |0⟩、南極 |1⟩、赤道為等權重疊加', '**微波脈衝 = 旋轉**：共振驅動繞 x/y 軸轉（Rabi），π 脈衝使 |0⟩→|1⟩'], 0.6, 5.5, 6.25, 1.3, { size: 14, bullet: true });
    await fitImage(s, IMG3('bloch'), 7.15, 1.4, 5.6, 5.05, { crop: { left: 640, top: 0, width: 1280, height: 1300 }, alt: 'Bloch 球 3D 動畫' });
    caption(s, '3D 場景 1：狀態向量隨 Rabi 驅動旋轉', 7.15, 6.55, 5.6, { align: 'center' });
  },
  notes: `古典位元非 0 即 1；量子位元則可以處在 0 和 1 的疊加。一個量子位元的純態可以用兩個角度 θ 和 φ 描述，所以可以畫在一個單位球面上，這就是 Bloch 球：北極是 |0⟩、南極是 |1⟩，赤道上則是 0 和 1 各一半的疊加，差別在相對相位 φ。
【切換到 3D 場景 1】大家看這個金色箭頭就是量子態。當我們送入一個頻率剛好等於量子位元頻率的微波——也就是共振驅動——狀態會繞著 x 軸旋轉，這叫 Rabi 振盪。右下角的曲線是激發態機率 P(1) 隨時間變化，呈現 sin² 的形狀。脈衝長度剛好讓它轉 180 度，就叫 π 脈衝，等於古典的 NOT 閘；轉 90 度就是 π/2 脈衝，產生疊加態。
請大家記住一件事：量測會讓疊加塌縮到 0 或 1，機率由 θ 決定。所以「讀取」本質上是一個統計過程，這一點到第三部分會很重要。`,
});
S({ sec: '01 背景知識', title: '量子位元的品質指標', anim: 'bloch', min: 2,
  async render(s) {
    s.addText(runs('量子位元的品質指標'), { placeholder: 'title' }); animPill(s, 'bloch');
    const rows = [
      ['clock', 'T_{1}：能量弛豫時間', '|1⟩ 自發放出能量回到 |0⟩ 的時間常數。最佳 transmon 約 0.1–1 ms。', C.accent4],
      ['wave', 'T_{2}：相位相干時間', '疊加態相位資訊保留多久；T_{2} ≤ 2T_{1}。受低頻雜訊（磁通、電荷）影響。', C.accent3],
      ['target', '閘保真度', '單量子位元閘 > 99.9 %、雙量子位元閘 > 99.5 %（最佳實驗）。', C.accent1],
      ['eye', '讀取保真度與速度', '單發讀取 > 99 %，時間 100–500 ns；需同時兼顧不破壞相鄰量子位元。', C.accent2],
    ];
    rows.forEach(([ic, t, d, col], i) => {
      const y = 1.55 + i * 1.3;
      iconCircle(s, ic, 0.6, y + 0.08, 0.68, col);
      s.addText(runs(t, {}), { x: 1.5, y, w: 5.6, h: 0.45, fontSize: 18, bold: true, color: C.text1, margin: 0, isTextBox: true });
      para(s, [d], 1.5, y + 0.48, 5.6, 0.75, { size: 14, color: '4A5468' });
    });
    card(s, 7.55, 1.55, 5.2, 4.95);
    s.addText('經驗法則', { x: 7.85, y: 1.75, w: 4.6, h: 0.45, fontSize: 18, bold: true, color: C.accent1, margin: 0, isTextBox: true });
    para(s, ['可執行的操作數 ≈ T_{2} / 閘時間', '例：T_{2} = 100 μs、閘 = 25 ns → 約 4000 個閘', '讀取時間必須 ≪ T_{1}，否則讀取途中就衰減', '所有指標都和 **JJ 品質**（缺陷、準粒子）與**讀取電路設計**（Purcell 效應）有關'], 7.85, 2.3, 4.6, 4.0, { size: 15, bullet: true, space: 10 });
  },
  notes: `評估量子位元好壞有四個常用指標。
T1 是能量弛豫時間：如果把量子位元放在 |1⟩，它會自發放出一個微波光子掉回 |0⟩，T1 就是這個過程的時間常數。最好的 transmon 現在在 0.1 到 1 毫秒的量級。
T2 是相位相干時間：疊加態的相對相位能維持多久。它受到低頻雜訊影響，例如磁通雜訊、電荷雜訊。理論上 T2 最多是 2 倍 T1。在 3D 場景 1 中可以切到「Ramsey 進動 + T2」模式，會看到向量在赤道上轉、同時越縮越短，那就是失相。
閘保真度和讀取保真度則是操作層面的指標。
右邊的經驗法則：你能做多少個操作，大約是 T2 除以閘時間。讀取時間必須遠小於 T1，否則讀到一半它就掉下來了——這是讀取設計最基本的限制。也請大家先留個印象：這些指標都會回到兩件事——JJ 的材料品質，以及讀取電路的設計。`,
});
S({ sec: '01 背景知識', title: '超導現象：零電阻與完全抗磁', anim: 'cooper', min: 2,
  async render(s) {
    s.addText(runs('超導現象：零電阻與完全抗磁'), { placeholder: 'title' }); animPill(s, 'cooper');
    const cards = [
      ['bolt', '零直流電阻', '低於臨界溫度 T_{c}，電流可在超導環中流動多年不衰減。', C.accent1],
      ['magnet', 'Meissner 效應', '磁場被完全排出超導體內部（完全抗磁），只在表面穿透深度 λ ~ 50–100 nm 內存在。', C.accent3],
      ['snow', '臨界溫度 T_{c}', 'Al ≈ 1.2 K、Ta ≈ 4.5 K、Nb ≈ 9.2 K、NbTiN ≈ 14 K。量子電路在 10 mK 工作 ≪ T_{c}。', C.accent2],
    ];
    cards.forEach(([ic, t, d, col], i) => {
      const y = 1.5 + i * 1.75;
      card(s, 0.6, y, 5.9, 1.55);
      iconCircle(s, ic, 0.85, y + 0.25, 0.62, col);
      s.addText(runs(t, {}), { x: 1.7, y: y + 0.18, w: 4.6, h: 0.42, fontSize: 18, bold: true, color: C.text1, margin: 0, isTextBox: true });
      para(s, [d], 1.7, y + 0.65, 4.6, 0.85, { size: 14, color: '4A5468' });
    });
    await fitImage(s, IMG3('cooper'), 6.8, 1.45, 5.95, 4.6, { crop: { left: 300, top: 300, width: 1960, height: 980 }, alt: 'Cooper pair 3D 動畫' });
    caption(s, '3D 場景 2：低於 T_{c} 時電子配對、整體同步流動', 6.8, 6.1, 5.95, { align: 'center' });
  },
  notes: `超導體有兩個招牌現象。第一是零直流電阻：降到臨界溫度以下，電阻突然變成零，在超導環中激發的電流可以流好幾年不衰減。第二是 Meissner 效應：磁場會被完全排出超導體內部，只在表面幾十到一百奈米的穿透深度內存在。
量子電路常用的材料：鋁，臨界溫度 1.2 K，是 JJ 最常用的材料；鉭 4.5 K，近年做電容板可以大幅提升 T1；鈮 9.2 K。我們的晶片在 10 mK 工作，遠低於這些溫度，所以電路幾乎沒有損耗。
【切換到 3D 場景 2】左邊的溫度滑桿可以拉看看：在 2.5 K 的正常態，電子被晶格振動散射、亂跑，這就是電阻的來源；降到 0.3 K，電子兩兩配對成 Cooper pair，整體同步往同一個方向流動，不再被散射。右下角是電阻對溫度的曲線，在 Tc 突然降到零。`,
});
S({ sec: '01 背景知識', title: 'BCS 理論：Cooper pair 與能隙', anim: 'cooper', min: 2.5,
  async render(s) {
    s.addText(runs('BCS 理論：Cooper pair 與能隙'), { placeholder: 'title' }); animPill(s, 'cooper');
    para(s, ['電子經過時吸引正離子 → 晶格局部扭曲（聲子）→ 吸引第二顆電子', '兩顆**自旋相反、動量相反**的電子形成 **Cooper pair**（電荷 2e，玻色子）', '所有 Cooper pair 凝聚為**同一個巨觀量子態**', '拆散一對需要能量 **2Δ**（超導能隙）→ 小擾動無法散射 → 零電阻'], 0.6, 1.5, 6.3, 2.9, { size: 15, bullet: true, space: 9 });
    eqBox(s, ['ψ(r) = √n_{s} · e^{iφ(r)}', { t: '整塊超導體只需一個「相位 φ」描述', size: 14, color: C.accent6, cjk: true }], 0.6, 4.55, 6.3, 1.35);
    s.addText('相位 φ 是本次分享的主角——JJ 正是「兩塊超導體之間的相位差」', { x: 0.6, y: 6.1, w: 6.3, h: 0.6, fontSize: 14, bold: true, color: C.accent1, margin: 0, isTextBox: true });
    // 能量尺度比較
    card(s, 7.3, 1.5, 5.45, 5.2);
    s.addText('能量尺度比較（鋁）', { x: 7.6, y: 1.65, w: 4.9, h: 0.45, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true });
    const bars = [['超導能隙 2Δ/h', 88, '≈ 88 GHz（2Δ ≈ 360 μeV）', C.accent4], ['量子位元 f_{01}', 5, '≈ 5 GHz（≈ 20 μeV）', C.accent2], ['熱能 k_{B}T/h @10 mK', 0.21, '≈ 0.2 GHz', C.accent6]];
    bars.forEach(([lab, v, txt, col], i) => {
      const y = 2.25 + i * 1.08; const W = 4.6 * Math.max(0.012, v / 88);
      s.addText(runs(lab, {}), { x: 7.6, y, w: 4.9, h: 0.35, fontSize: 13.5, color: C.text1, margin: 0, isTextBox: true });
      s.addShape(pres.shapes.RECTANGLE, { x: 7.6, y: y + 0.4, w: W, h: 0.36, fill: { color: col }, line: { color: col, width: 0 }, objectName: oname('bar') });
      s.addText(txt, { x: 7.6 + W + 0.1 > 11.2 ? 7.7 : 7.6 + W + 0.1, y: y + 0.4, w: 3.2, h: 0.36, fontSize: 12.5, color: 7.6 + W + 0.1 > 11.2 ? C.background1 : '4A5468', bold: 7.6 + W + 0.1 > 11.2, valign: 'middle', margin: 0, isTextBox: true });
    });
    para(s, ['量子位元光子能量 ≪ 2Δ → 無法拆散 Cooper pair，電路幾乎無耗散', '熱能 ≪ 量子位元能量 → 熱激發機率極低'], 7.6, 5.55, 4.95, 1.1, { size: 13.5, bullet: true });
  },
  notes: `超導的微觀解釋是 BCS 理論。直覺是這樣：一顆電子經過晶格，會把周圍帶正電的離子稍微吸過來，留下一條短暫的正電荷尾跡——這就是聲子；這條尾跡又吸引了第二顆電子。結果兩顆自旋相反、動量相反的電子形成一對，叫 Cooper pair，帶電荷 2e。
關鍵在於：Cooper pair 是玻色子，所有的 pair 會凝聚到同一個量子態，所以整塊超導體可以用一個巨觀的波函數描述：振幅是 pair 密度的平方根，乘上一個相位 e 的 iφ。請記住這個相位 φ——今天的主角 JJ，本質上就是兩塊超導體之間的「相位差」。
右邊是能量尺度的比較：要拆散一對 Cooper pair 需要 2Δ，鋁大約是 88 GHz 的光子能量；量子位元只有 5 GHz；10 mK 的熱能只有 0.2 GHz。所以量子位元的光子拆不散 Cooper pair，電路幾乎沒有耗散；熱擾動也遠小於量子位元能量，所以量子位元可以穩定待在基態。這就是為什麼超導 + 極低溫是實現量子位元的好平台。`,
});
S({ sec: '01 背景知識', title: '磁通量子化：Φ₀ = h / 2e', min: 2,
  async render(s) {
    s.addText(runs('磁通量子化：Φ₀ = h / 2e'), { placeholder: 'title' });
    // 示意圖：超導環與磁通
    s.addShape(pres.shapes.DONUT, { x: 0.9, y: 1.7, w: 3.9, h: 3.9, fill: { color: 'B9C4D4' }, line: { color: '8A97AB', width: 1 }, adjustPoint: 0.1, objectName: oname('ring') });
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
      const cx = 2.35 + i * 0.5, cy = 3.15 + j * 0.5;
      s.addShape(pres.shapes.OVAL, { x: cx, y: cy, w: 0.22, h: 0.22, fill: { color: C.background1 }, line: { color: C.accent2, width: 2 }, objectName: oname('flux-dot') });
      s.addShape(pres.shapes.OVAL, { x: cx + 0.07, y: cy + 0.07, w: 0.08, h: 0.08, fill: { color: C.accent2 }, line: { color: C.accent2, width: 0 }, objectName: oname('flux-dot-c') });
    }
    s.addText('穿出紙面的磁通 Φ', { x: 1.0, y: 5.75, w: 3.7, h: 0.35, fontSize: 13, color: C.accent2, align: 'center', margin: 0, isTextBox: true });
    eqBox(s, ['∮ ∇φ · dl = 2π n', 'Φ = n · Φ_{0}', { t: 'Φ_{0} = h / 2e ≈ 2.068 × 10^{−15} Wb', size: 18 }], 5.4, 1.5, 7.35, 2.2);
    para(s, ['波函數繞超導環一圈必須回到原值 → 相位變化只能是 2π 的整數倍', '環內磁通因此被「量子化」為 Φ_{0} 的整數倍', '分母是 **2e** 而不是 e —— 直接證明載流子是 **Cooper pair**', 'Φ_{0} 是超導電路的「自然單位」：SQUID 的調頻週期、JJ 電感、AC Josephson 頻率都由它決定'], 5.4, 3.95, 7.35, 2.8, { size: 15, bullet: true, space: 9 });
  },
  notes: `第三個背景知識是磁通量子化。既然整塊超導體共享一個波函數，那麼沿著一個超導環繞一圈，波函數必須回到自己，相位的總變化只能是 2π 的整數倍。這個條件換算過來，就是環內的磁通只能是一個基本單位 Φ0 的整數倍。
Φ0 等於 h 除以 2e，約 2.07 乘 10 的負 15 次方韋伯。這裡分母是 2e 而不是 e，正是實驗上證明「載流子是成對電子」的直接證據。
Φ0 可以說是超導電路的自然單位。等一下我們會看到：JJ 的電感、AC Josephson 效應的頻率，還有 SQUID 調頻的週期，全部都用 Φ0 來表示。`,
});
S({ sec: '01 背景知識', title: '為什麼需要非線性？', anim: 'potential', min: 2.5,
  async render(s) {
    s.addText(runs('為什麼需要非線性？'), { placeholder: 'title' }); animPill(s, 'potential');
    await fitImage(s, IMGF('lc_vs_transmon'), 0.6, 1.4, 8.2, 4.4, { alignX: 'left' });
    caption(s, 'E_{J}/h = 12.5 GHz、E_{C}/h = 250 MHz（E_{J}/E_{C} = 50）', 0.6, 5.85, 8.2);
    card(s, 9.05, 1.45, 3.7, 5.25);
    s.addText('關鍵問題', { x: 9.3, y: 1.6, w: 3.2, h: 0.42, fontSize: 18, bold: true, color: C.accent4, margin: 0, isTextBox: true });
    para(s, ['LC 振盪器能階**等間距**：頻率 ω 的微波同時激發 0→1→2→3…，無法只用兩個能階', '把電感換成 **JJ**：位勢由拋物線變成餘弦，能階間距逐漸變小', '**非諧性** α = ω_{12} − ω_{01} ≈ −E_{C}（約 −200～−300 MHz）', '於是可以只選擇 |0⟩、|1⟩ 作為量子位元'], 9.3, 2.1, 3.25, 4.5, { size: 14, bullet: true, space: 8 });
  },
  notes: `這頁是理解 JJ 為什麼重要的關鍵。
一個超導 LC 振盪器其實已經是量子的了：它的能量是量子化的。問題是，它的位勢是一個拋物線，所以能階完全等間距。這會造成什麼問題？如果我用頻率 ω 的微波想把它從 0 激發到 1，同一個頻率也剛好會把 1 激發到 2、2 激發到 3……它會一路爬上去，我們沒辦法只在兩個能階之間操作，也就不是一個量子位元。
解法是把線性電感換成 JJ。JJ 的位勢是 −EJ cos φ，在底部像拋物線，越往上越寬，所以能階越往上間距越小。左圖是我們的實際計算：0→1 是 4.74 GHz、1→2 是 4.45 GHz，差了大約 290 MHz，這就叫非諧性。只要我們的微波脈衝頻寬比這個差距小，就能只操作 0 和 1。
【切換到 3D 場景 4】可以在「LC 諧振子」和「JJ / Transmon」兩種模式間切換，看能階和波函數的差異；右邊的標籤會即時顯示每個躍遷頻率。`,
});

// ===== 02 JJ =====
S({ sec: '02 JJ 元件', layout: 'SECTION_DARK', title: '02 JJ 元件', min: 0.5,
  async render(s) {
    s.addText('02', { x: 0.7, y: 1.3, w: 3, h: 1.4, fontSize: 80, bold: true, color: C.accent1, margin: 0, isTextBox: true, fontFace: 'Arial' });
    s.addText(runs('約瑟夫森接面（JJ）'), { placeholder: 'title' });
    s.addText('結構 · Josephson 關係 · 非線性電感 · SQUID · Transmon · 製程 · 雜訊', { placeholder: 'body' });
    await fitImage(s, IMG3('jj'), 8.0, 1.0, 5.0, 5.4, { crop: { left: 1100, top: 160, width: 1300, height: 1150 } });
  },
  notes: `接下來進入今天的主角：約瑟夫森接面。`,
});
S({ sec: '02 JJ 元件', title: 'JJ 的結構：超導–絕緣–超導', anim: 'jj', min: 2.5,
  async render(s) {
    s.addText(runs('JJ 的結構：超導–絕緣–超導'), { placeholder: 'title' }); animPill(s, 'jj');
    await fitImage(s, IMG3('jj'), 0.6, 1.4, 6.9, 4.9, { crop: { left: 400, top: 120, width: 2160, height: 1240 }, alt: 'JJ 三明治結構 3D 模型', alignX: 'left' });
    caption(s, '3D 場景 3：Cooper pair 穿隧與兩側的「相位鐘」', 0.6, 6.35, 6.9);
    table(s, [['項目', '典型值'], ['材料', 'Al / AlOx / Al'], ['氧化層厚度', '1–2 nm'], ['接面面積', '~0.01–0.05 μm²'], ['正常態電阻 R_{n}', '5–15 kΩ'], ['臨界電流 I_{c}', '20–60 nA'], ['電容 C_{J}', '~1–2 fF']], 7.8, 1.5, 4.95, [2.2, 2.75], { size: 13.5, rowH: 0.47 });
    para(s, ['絕緣層夠薄 → Cooper pair 可**整對量子穿隧**', '兩側超導體各有相位 φ_{1}、φ_{2}；一切由**相位差 φ** 決定'], 7.8, 5.0, 4.95, 1.6, { size: 14, bullet: true, space: 8 });
  },
  notes: `JJ 的結構非常簡單：兩片超導體，中間夾一層非常薄的絕緣層。量子電路裡最常見的是鋁 / 氧化鋁 / 鋁，絕緣層只有一到兩奈米，也就是幾個原子層。
因為絕緣層夠薄，Cooper pair 可以整對用量子穿隧的方式通過。右邊是典型數字：面積大約零點零幾平方微米，正常態電阻幾千到一萬多歐姆，臨界電流幾十奈安培。
【切換到 3D 場景 3】大家看左右兩塊鋁，上方各有一個「相位鐘」，代表各自的巨觀相位 φ1、φ2。中間紅色那層是氧化鋁穿隧阻障。藍紫色的小球對是 Cooper pair，它們穿過阻障時會閃一下。上方的標籤顯示相位差 φ，以及對應的電流。等一下我們用這個場景來說明兩條 Josephson 關係式。`,
});
S({ sec: '02 JJ 元件', title: 'Josephson 的兩大關係式', anim: 'jj', min: 3,
  async render(s) {
    s.addText(runs('Josephson 的兩大關係式'), { placeholder: 'title' }); animPill(s, 'jj');
    const blocks = [
      ['DC Josephson 效應', 'I = I_{c} sin φ', ['**零電壓**下就能有超電流', '電流大小由相位差 φ 決定', '最大值 I_{c}：超過就進入電壓態'], C.accent3, 0.6],
      ['AC Josephson 效應', 'dφ/dt = 2eV / ħ', ['加電壓 V → 相位**持續旋轉**', '電流以 f = V/Φ_{0} 振盪', '483.6 GHz / mV：**電壓標準**的基礎'], C.accent4, 6.8],
    ];
    blocks.forEach(([t, eq, bl, col, x]) => {
      card(s, x, 1.5, 5.95, 4.15);
      s.addText(t, { x: x + 0.3, y: 1.68, w: 5.3, h: 0.45, fontSize: 20, bold: true, color: col, margin: 0, isTextBox: true });
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.3, y: 2.3, w: 5.35, h: 1.05, rectRadius: 0.1, fill: { color: C.background1 }, line: { color: col, width: 1.5 }, objectName: oname('eq-frame') });
      s.addText(runs(eq, { fontFace: 'Cambria' }), { x: x + 0.3, y: 2.3, w: 5.35, h: 1.05, fontSize: 28, color: C.text1, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: oname('equation') });
      para(s, bl, x + 0.3, 3.6, 5.35, 1.9, { size: 15, bullet: true, space: 8 });
    });
    s.addText(runs('兩式合起來 → JJ 是一個「由相位控制的非線性元件」；I_{c} = (π Δ / 2e R_{n})（Ambegaokar–Baratoff）'), { x: 0.6, y: 5.95, w: 12.15, h: 0.6, fontSize: 15, color: C.text1, bold: true, margin: 0, isTextBox: true, valign: 'middle' });
  },
  notes: `1962 年 Josephson 預測了兩個效應，後來得了諾貝爾獎。
第一個是 DC Josephson 效應：通過接面的超電流 I 等於 Ic 乘上 sin φ。注意這是在零電壓下發生的——不需要電壓就有電流，而電流大小由相位差決定。最大能通過的電流就是臨界電流 Ic。
第二個是 AC Josephson 效應：如果接面兩端有電壓 V，相位差就會隨時間持續增加，速率是 2eV/ħ。代入第一式，電流就會以頻率 V/Φ0 振盪，每毫伏特對應 483.6 GHz。這個關係精確到被拿來當作國際電壓標準。
【切換到 3D 場景 3】把偏壓電流拉到 0.5 Ic，相位差停在 30 度，電壓為零；拉到接近 Ic，相位差趨近 90 度；超過 Ic，例如 1.4 Ic，大家看相位鐘開始一直轉，這就是電壓態，右下角的 I-V 圖上工作點跳到了電阻分支。
最後一行是 Ambegaokar–Baratoff 關係：Ic 乘上正常態電阻 Rn 是一個由超導能隙決定的常數。這個關係在製程上非常實用，等一下會用到。`,
});
S({ sec: '02 JJ 元件', title: 'JJ 是一個「非線性電感」', min: 2.5,
  async render(s) {
    s.addText(runs('JJ 是一個「非線性電感」'), { placeholder: 'title' });
    eqBox(s, [{ t: '由 I = I_{c} sin φ 與 V = (Φ_{0}/2π) dφ/dt：', size: 15, cjk: true, color: '4A5468' }, 'V = L_{J} · dI/dt', 'L_{J}(φ) = Φ_{0} / (2π I_{c} cos φ)'], 0.6, 1.5, 5.3, 2.4, { size: 22 });
    para(s, ['小電流時 L_{J0} = Φ_{0}/(2π I_{c})', '例：I_{c} = 30 nA → L_{J0} ≈ **11 nH**', '電感**隨電流（相位）改變** → 非線性', '**無耗散**：不像電阻會發熱', '同時也是 E_{J}（約瑟夫森能）的來源'], 0.6, 4.15, 5.3, 2.6, { size: 15, bullet: true, space: 7 });
    await fitImage(s, IMGF('cpr_lj'), 6.2, 1.5, 6.55, 4.3);
    caption(s, '左：電流–相位關係；右：電感隨相位上升，φ → π/2 時發散', 6.2, 5.95, 6.55, { align: 'center' });
  },
  notes: `把兩條 Josephson 關係式合起來，對時間微分：dI/dt 等於 Ic cos φ 乘 dφ/dt，而 dφ/dt 又正比於電壓。整理一下會得到 V 等於某個 L 乘 dI/dt——這就是電感的定義式。所以 JJ 在電路上就像一個電感，叫約瑟夫森電感 LJ。
但它跟普通線圈電感有兩個不同：第一，它的值會隨相位、也就是隨流過的電流改變——這就是非線性；第二，它沒有耗散，不會發熱。
數字感：Ic 是 30 nA 的話，LJ 大約 11 nH。右圖看到電感隨相位增加而上升，在 π/2 發散。
所以今天最重要的一句話是：JJ 是一個「無耗散的非線性電感」。把它和電容並聯，就得到一個非線性振盪器，也就是 transmon 量子位元。`,
});
S({ sec: '02 JJ 元件', title: '兩個能量尺度：E_{J} 與 E_{C}', anim: 'potential', min: 3,
  async render(s) {
    s.addText(runs('兩個能量尺度：E_{J} 與 E_{C}'), { placeholder: 'title' }); animPill(s, 'potential');
    eqBox(s, ['H = 4E_{C}(n̂ − n_{g})² − E_{J} cos φ̂', { t: '[φ̂, n̂] = i ：相位與 Cooper pair 數為共軛變數', size: 15, cjk: true, color: '4A5468' }], 0.6, 1.5, 12.15, 1.45, { size: 26 });
    table(s, [['', '約瑟夫森能 E_{J}', '充電能 E_{C}'],
      ['定義', 'E_{J} = Φ_{0} I_{c} / 2π = ħ I_{c} / 2e', 'E_{C} = e² / 2C_{Σ}'],
      ['物理意義', 'Cooper pair 穿隧的耦合能（位勢深度）', '多加一顆電子的靜電能（「質量」的倒數）'],
      ['由什麼決定', '接面面積、氧化層 → I_{c}', '總電容 C_{Σ}（含大電容板）'],
      ['典型值（h 為單位）', 'I_{c} = 30 nA → ≈ 15 GHz', 'C_{Σ} = 80 fF → ≈ 240 MHz'],
    ], 0.6, 3.25, 12.15, [2.6, 4.775, 4.775], { size: 14, rowH: 0.5 });
    s.addText(runs('類比：一顆「質量 ∝ 1/E_{C}」的粒子在「深度 ∝ E_{J}」的餘弦井中運動；E_{J}/E_{C} 決定量子位元類型'), { x: 0.6, y: 6.05, w: 12.15, h: 0.6, fontSize: 15, bold: true, color: C.accent1, margin: 0, isTextBox: true, valign: 'middle' });
  },
  notes: `把 JJ 和一個電容並聯，整個電路的量子力學由這條 Hamiltonian 描述。它有兩個能量尺度。
EJ 是約瑟夫森能，等於 Φ0 Ic 除以 2π，代表 Cooper pair 穿隧的耦合強度，在位勢圖上就是那個餘弦井有多深。
EC 是充電能，e² / 2CΣ，代表多放一顆電子到電容上要花多少靜電能。在力學類比中它像是「質量的倒數」：EC 越小、粒子越重、越不容易被量子漲落晃動。
這裡的 n 是穿過接面的 Cooper pair 數，φ 是相位，兩者是共軛變數，就像位置和動量。ng 是環境中背景電荷造成的偏移。
典型數字：Ic 30 nA 對應 EJ 約 15 GHz；總電容 80 fF 對應 EC 約 240 MHz。兩者比值 EJ/EC 決定了量子位元的類型，這是下一頁之後的重點。`,
});
S({ sec: '02 JJ 元件', title: 'RCSJ 模型與傾斜洗衣板位勢', anim: 'washboard', min: 2.5,
  async render(s) {
    s.addText(runs('RCSJ 模型與傾斜洗衣板位勢'), { placeholder: 'title' }); animPill(s, 'washboard');
    await fitImage(s, IMG3('washboard'), 0.6, 1.4, 6.3, 4.85, { crop: { left: 380, top: 120, width: 1800, height: 1200 }, alt: '洗衣板位勢 3D 動畫', alignX: 'left' });
    caption(s, '3D 場景 5：相位粒子在井中振盪，電流超過 I_{c} 即滾下坡', 0.6, 6.3, 6.3);
    eqBox(s, ['C(ħ/2e) φ̈ + (ħ/2eR) φ̇ + I_{c} sin φ = I', 'U(φ) = −E_{J} cos φ − (ħI/2e) φ'], 7.2, 1.5, 5.55, 1.6, { size: 17 });
    table(s, [['電路量', '力學類比'], ['電容 C', '質量'], ['1/R（並聯電阻）', '摩擦'], ['偏壓電流 I', '傾斜角度'], ['井中振盪', '電漿頻率 ω_{p}'], ['滾下坡', 'dφ/dt ≠ 0 → 出現電壓']], 7.2, 3.35, 5.55, [2.5, 3.05], { size: 13.5, rowH: 0.44 });
  },
  notes: `真實的 JJ 除了理想的約瑟夫森元件，還並聯了自身的電容和一個電阻，這叫 RCSJ 模型。寫出電路方程式，會發現它和「一顆球在傾斜的洗衣板上滾動」的方程式完全一樣：電容扮演質量、電阻扮演摩擦、偏壓電流決定洗衣板傾斜多少。
【切換到 3D 場景 5】金色的球就是「相位粒子」。在小電流時它被困在某個井裡做小幅振盪，振盪頻率叫電漿頻率；這時相位不隨時間增加，所以沒有電壓。把電流拉超過 Ic，最後一個井消失，球開始一路滾下坡，dφ/dt 不為零，就出現了電壓。
按「掃描」按鈕會把電流從 0 拉到 1.3 再降回來，右下角會畫出 I-V 曲線：低阻尼時有遲滯，電流降到 Ic 以下球還是繼續滾，直到回捕電流才停下來。
另外，在井中能量是量子化的，圖上的短線就是能階。早期的「相位量子位元」就是在接近 Ic 的偏壓下，利用井中最低的兩個能階。現代的 transmon 則是在不加偏壓的情況下工作，也就是洗衣板完全水平。`,
});
S({ sec: '02 JJ 元件', title: 'SQUID：用磁通調整的 JJ', anim: 'squid', min: 2.5,
  async render(s) {
    s.addText(runs('SQUID：用磁通調整的 JJ'), { placeholder: 'title' }); animPill(s, 'squid');
    await fitImage(s, IMG3('squid'), 0.6, 1.4, 4.4, 4.6, { crop: { left: 700, top: 0, width: 1300, height: 1440 }, alt: 'SQUID 3D 模型', alignX: 'left' });
    caption(s, '3D 場景 6：兩個 JJ 並聯成環', 0.6, 6.05, 4.4);
    await fitImage(s, IMGF('squid_tuning'), 5.2, 1.4, 4.4, 3.2);
    eqBox(s, ['E_{J}(Φ) = E_{JΣ} |cos(πΦ/Φ_{0})| ·', '√(1 + d² tan²(πΦ/Φ_{0}))'], 5.2, 4.75, 4.4, 1.25, { size: 15 });
    card(s, 9.85, 1.45, 2.9, 5.25);
    para(s, [{ t: '重點', bold: true, color: C.accent1, size: 17 }, '兩個 JJ 並聯成環 = 一個**臨界電流可調**的 JJ', '用晶片上的 **Z 線**通電流產生磁通 → 即時調頻', '**甜蜜點** Φ = 0：df/dΦ = 0，對磁通雜訊一階免疫', '**不對稱 SQUID** 縮小調頻範圍、降低雜訊敏感度'], 10.05, 1.6, 2.55, 5.0, { size: 13.5, bullet: false, space: 9 });
  },
  notes: `如果把兩個 JJ 並聯成一個小環，就是 DC SQUID。由於磁通量子化，穿過環的磁通會讓兩個 JJ 的相位產生干涉，整體效果等於一個「臨界電流可以用磁通調整」的 JJ，週期剛好是一個 Φ0。
在量子晶片上，每顆量子位元旁邊會有一條 Z 控制線，通一點電流就能改變穿過 SQUID 的磁通，進而在奈秒尺度內調整量子位元頻率。這被用來做雙量子位元閘（把兩顆調到共振）、或是避開有缺陷的頻率。
中間的圖是頻率對磁通：對稱 SQUID 在半個 Φ0 處頻率會掉到零；不對稱 SQUID 的調頻範圍比較小，但曲線比較平，對磁通雜訊比較不敏感。曲線最高點的地方叫甜蜜點，斜率為零，對磁通雜訊一階免疫，通常讓量子位元停在這裡。
【切換到 3D 場景 6】拉動磁通滑桿，可以看到穿過環的磁場箭頭、環上的屏蔽電流，右下角的工作點沿著曲線移動，面板也會顯示目前的 EJ 和頻率。`,
});
S({ sec: '02 JJ 元件', title: '以 JJ 為核心的量子位元家族', min: 2.5,
  async render(s) {
    s.addText(runs('以 JJ 為核心的量子位元家族'), { placeholder: 'title' });
    table(s, [['類型', '電路結構', 'E_{J}/E_{C}', '頻率', '非諧性', '特點'],
      ['電荷（CPB）', '小島 + 1 JJ', '~1', '5–10 GHz', '大', '最早的超導量子位元；對電荷雜訊極敏感'],
      ['**Transmon**', 'JJ/SQUID ∥ 大電容', '50–100', '4–6 GHz', '−200～−300 MHz', '**業界主流**；抗電荷雜訊、結構簡單'],
      ['磁通（Flux）', '超導環 + 3–4 JJ', '~50', '1–10 GHz', '大', '以環流方向編碼；對磁通雜訊敏感'],
      ['Fluxonium', '1 JJ ∥ 超電感（JJ 陣列）', '~1–10', '0.1–1 GHz', '極大', 'T_{1} 可達 ms；低頻、高非諧性'],
      ['相位（Phase）', '電流偏壓 1 JJ', '≫ 1', '5–10 GHz', '中', '洗衣板井中能階；已較少使用'],
    ], 0.6, 1.5, 12.15, [1.75, 2.45, 1.25, 1.35, 1.75, 3.6], { size: 13.5, rowH: 0.62 });
    s.addText(runs('共同點：都靠 JJ 提供「無耗散的非線性」；差別在 E_{J}/E_{C} 比值與電路拓樸'), { x: 0.6, y: 5.6, w: 12.15, h: 0.5, fontSize: 15, bold: true, color: C.accent1, margin: 0, isTextBox: true });
    caption(s, '數值為典型範圍，實際依設計而異', 0.6, 6.15, 12.15);
  },
  notes: `JJ 加上不同的電路拓樸，就形成不同的超導量子位元。
最早的是電荷量子位元，也叫 Cooper pair box，EJ 和 EC 差不多大，它對環境中的背景電荷非常敏感，相干時間很短。
Transmon 就是在電荷量子位元旁邊並聯一個大電容，把 EJ/EC 拉到 50 到 100，對電荷雜訊幾乎免疫，結構簡單，是目前業界主流，Google、IBM 都用它的變形。
磁通量子位元用一個超導環加三四個 JJ，以環流順時針或逆時針來編碼。
Fluxonium 是一個 JJ 並聯一個「超電感」，這個超電感通常是由上百個大 JJ 串成的陣列。它頻率低、非諧性極大，T1 可以到毫秒等級，是近年很熱門的方向。
相位量子位元就是剛才洗衣板的那種，現在比較少用了。
這些量子位元的共同點是：全部靠 JJ 提供無耗散的非線性。接下來我們專注在最主流的 transmon。`,
});
S({ sec: '02 JJ 元件', title: 'Transmon 深入：E_{J}/E_{C} 與電荷色散', anim: 'potential', min: 3,
  async render(s) {
    s.addText(runs('Transmon 深入：E_{J}/E_{C} 與電荷色散'), { placeholder: 'title' }); animPill(s, 'potential');
    await fitImage(s, IMGF('charge_dispersion'), 0.6, 1.45, 12.15, 3.3);
    caption(s, '前三個能階隨背景電荷 n_{g} 的變化（以 E_{01} 正規化）。E_{J}/E_{C} 越大，能階越平直', 0.6, 4.75, 12.15, { align: 'center' });
    const f = [['頻率', 'ħω_{01} ≈ √(8E_{J}E_{C}) − E_{C}'], ['非諧性', 'α ≈ −E_{C}（只以冪次下降）'], ['電荷色散', 'ε_{m} ∝ e^{−√(8EJ/EC)}（指數下降）']];
    f.forEach(([t, e], i) => {
      const x = 0.6 + i * 4.1;
      card(s, x, 5.2, 3.9, 1.5);
      s.addText(t, { x: x + 0.25, y: 5.3, w: 3.4, h: 0.4, fontSize: 15, bold: true, color: C.accent1, margin: 0, isTextBox: true });
      s.addText(runs(e, { fontFace: 'Cambria' }), { x: x + 0.25, y: 5.75, w: 3.45, h: 0.8, fontSize: 16, color: C.text1, margin: 0, isTextBox: true, valign: 'middle' });
    });
  },
  notes: `為什麼 transmon 要把 EJ/EC 拉到 50 以上？看這張圖。橫軸是背景電荷 ng——它來自基板或介面中隨機跳動的電荷，是一種無法完全消除的雜訊。縱軸是能階。
EJ/EC 等於 1 的時候，能階隨 ng 劇烈起伏，只要背景電荷一跳，量子位元頻率就跟著變，相干性很差。比值增加到 5、10，起伏迅速變小；到 50，能階幾乎是平的。
下面三個公式說明了為什麼這個交換很划算：電荷色散隨 EJ/EC 的平方根「指數」下降，而非諧性只以「冪次」下降，大約維持在 −EC。所以我們犧牲一點點非諧性，換來對電荷雜訊幾乎免疫。這就是 transmon 名稱的由來——transmission-line shunted plasma oscillation qubit。
【切換到 3D 場景 4】把 EJ/EC 從 1 拉到 50，右下角的插圖就是這張電荷色散圖，會即時更新。`,
});
S({ sec: '02 JJ 元件', title: 'Transmon 典型參數', min: 1.5,
  async render(s) {
    s.addText(runs('Transmon 典型參數'), { placeholder: 'title' });
    const st = [['4–6 GHz', 'f_{01} 量子位元頻率'], ['−200～−300 MHz', '非諧性 α ≈ −E_{C}'], ['50–100', 'E_{J}/E_{C} 比值'], ['20–50 nA', 'JJ 臨界電流 I_{c}'], ['60–100 fF', '總電容 C_{Σ}'], ['0.1–1 ms', 'T_{1}（最佳實驗）']];
    st.forEach(([v, l], i) => {
      const col = i % 3, row = Math.floor(i / 3);
      const x = 0.6 + col * 4.1, y = 1.55 + row * 2.45;
      card(s, x, y, 3.9, 2.2);
      s.addText(v, { x, y: y + 0.3, w: 3.9, h: 1.0, fontSize: v.length > 9 ? 30 : 38, bold: true, color: [C.accent3, C.accent1, C.accent2][col], align: 'center', valign: 'middle', margin: 0, isTextBox: true, fontFace: 'Arial' });
      s.addText(runs(l, {}), { x, y: y + 1.35, w: 3.9, h: 0.5, fontSize: 15, color: '4A5468', align: 'center', margin: 0, isTextBox: true });
    });
    caption(s, '電容板材料（Al、Nb、Ta）與基板（高阻矽、藍寶石）介面品質是 T_{1} 的主要限制', 0.6, 6.5, 12.15);
  },
  notes: `這頁整理 transmon 的典型參數，方便大家建立數量級的直覺：頻率 4 到 6 GHz，非諧性負兩三百 MHz，EJ/EC 在 50 到 100 之間，JJ 的臨界電流幾十奈安培，總電容幾十到一百飛法拉。T1 方面，最好的實驗在零點一到一毫秒之間，近年用鉭當電容板、改善介面處理，T1 有明顯進步。
這裡想強調：JJ 本身其實很小，電容板才是佔面積最大的部分，而 T1 的主要限制往往來自電容板和基板之間介面上的缺陷，下一頁和雜訊那一頁會再提。`,
});
S({ sec: '02 JJ 元件', title: 'JJ 製程：Dolan bridge 雙角度蒸鍍', anim: 'fab', min: 3,
  async render(s) {
    s.addText(runs('JJ 製程：Dolan bridge 雙角度蒸鍍'), { placeholder: 'title' }); animPill(s, 'fab');
    await fitImage(s, IMG3('fab'), 6.3, 1.45, 6.45, 4.5, { crop: { left: 200, top: 260, width: 2200, height: 1000 }, alt: 'Dolan bridge 製程 3D 動畫' });
    caption(s, '3D 場景 7：Lift-off 後留下兩層鋁的重疊區 = JJ', 6.3, 6.0, 6.45, { align: 'center' });
    const steps = ['**雙層光阻 + 電子束微影**：下層 MMA 顯影較快形成底切 → 上層 PMMA 留下懸空「橋」', '**第一次斜角蒸鍍 Al（+θ）**：影子使沉積位置平移', '**原位氧化**：不破真空通入 O_{2}，長出 1–2 nm AlOx', '**第二次斜角蒸鍍 Al（−θ）**：在橋正下方與第一層重疊', '**Lift-off**：去除光阻，只留下重疊的 Al/AlOx/Al'];
    steps.forEach((t, i) => {
      const y = 1.5 + i * 1.03;
      numCircle(s, i + 1, 0.6, y + 0.05, 0.5, C.accent1);
      para(s, [t], 1.3, y, 4.75, 0.98, { size: 14 });
    });
  },
  notes: `JJ 怎麼做出來？最經典的方法是 Dolan bridge 雙角度陰影蒸鍍，這也是很多實驗室和公司在用的方法。
第一步，塗兩層電子束光阻：下層 MMA 顯影比較快，會被挖出一個底切；上層 PMMA 定義圖形，在兩條開口之間留下一座懸空的光阻橋。
第二步，在真空中從一個斜角蒸鍍鋁。因為有角度，鋁原子穿過開口後落在基板上的位置會平移，就像影子一樣。
第三步，不破真空直接通入氧氣，讓鋁表面長出一到兩奈米的氧化鋁。氧氣壓力乘上時間，決定了氧化層厚度，也就決定了穿隧電阻和臨界電流。
第四步，從相反的角度再蒸鍍一次鋁，第二層會往反方向平移，剛好在橋的正下方和第一層重疊——這個重疊區就是 JJ。
第五步，lift-off，把光阻和上面多餘的金屬一起溶掉。
【切換到 3D 場景 7】動畫會依序播放這五個步驟，也可以點 1 到 5 的按鈕直接跳到某一步。注意第二和第四步的原子飛行方向是相反的。最後一步相機會拉近，金色閃爍的就是 JJ。
除了 Dolan bridge，另一種常見的是 Manhattan 法，用兩條互相垂直的線條各蒸鍍一次，不需要懸空橋，製程穩定性更好。`,
});
S({ sec: '02 JJ 元件', title: '製程控制：從氧化參數到量子位元頻率', min: 2.5,
  async render(s) {
    s.addText(runs('製程控制：從氧化參數到量子位元頻率'), { placeholder: 'title' });
    chevrons(s, ['氧化壓力×時間\n接面面積', '室溫電阻 R_{n}', 'I_{c} = πΔ / 2eR_{n}', 'E_{J} = ħI_{c} / 2e', '量子位元\n頻率 f₀₁'], 0.6, 1.55, 12.15, 1.15, [C.accent3, C.accent2, C.accent5, C.accent1, C.accent4]);
    card(s, 0.6, 3.05, 5.9, 3.65);
    s.addText('為什麼頻率定位很難？', { x: 0.9, y: 3.2, w: 5.3, h: 0.45, fontSize: 18, bold: true, color: C.accent4, margin: 0, isTextBox: true });
    para(s, ['f_{01} ∝ √E_{J} ∝ 1/√R_{n}：R_{n} 差 2 % → 頻率差約 1 %（~50 MHz）', '氧化層厚度只有幾個原子層，面積僅 ~0.02 μm²', '固定頻率 transmon 之間若頻率太接近（**頻率碰撞**）會造成串擾與閘錯誤'], 0.9, 3.75, 5.35, 2.85, { size: 14.5, bullet: true, space: 8 });
    card(s, 6.85, 3.05, 5.9, 3.65);
    s.addText('業界常見對策', { x: 7.15, y: 3.2, w: 5.3, h: 0.45, fontSize: 18, bold: true, color: C.accent5, margin: 0, isTextBox: true });
    para(s, ['**室溫探針量測 R_{n}**：降溫前預測頻率（Ambegaokar–Baratoff）', '**雷射 / 熱退火**：製作後微調 R_{n}，把頻率修到目標值', '**可調頻設計**：SQUID + Z 線，在低溫下再調整', '**製程監控**：測試結構、晶圓級統計、改善氧化均勻性'], 7.15, 3.75, 5.35, 2.85, { size: 14.5, bullet: true, space: 8 });
  },
  notes: `這頁講製程控制，是工程上很實際的問題。
整條因果鏈是：氧化的壓力乘時間和接面面積決定了穿隧電阻 Rn；Ambegaokar–Baratoff 關係告訴我們 Ic 和 Rn 成反比；Ic 決定 EJ；EJ 再決定量子位元頻率。
困難在於：頻率正比於 EJ 的平方根，也就是 Rn 的負二分之一次方。Rn 只要差 2%，頻率就差 1%，大約 50 MHz。而氧化層只有幾個原子層厚、面積只有零點零二平方微米，要控制到百分之一非常困難。對於固定頻率的 transmon，如果相鄰量子位元頻率太接近，就會發生所謂頻率碰撞，造成串擾和雙量子位元閘錯誤。
業界的對策包括：在室溫就用探針量 Rn，降溫前就能預測頻率；用雷射或熱退火在製作後微調 Rn，把頻率修到目標值；或是乾脆用 SQUID 做成可調頻；以及在製程上做大量的統計監控。`,
});
S({ sec: '02 JJ 元件', title: 'JJ 的其他角色：不只是量子位元', min: 2.5,
  async render(s) {
    s.addText(runs('JJ 的其他角色：不只是量子位元'), { placeholder: 'title' });
    const items = [
      ['link', '可調耦合器', '以 SQUID 調整兩量子位元間的有效耦合，可開關 → 高保真雙量子位元閘'],
      ['volume', 'JPA 參量放大器', 'JJ/SQUID 共振腔 + 泵浦，增益 ~20 dB，雜訊接近量子極限（窄頻）'],
      ['stream', 'TWPA 行波放大器', '數千個 JJ 串成傳輸線，頻寬數 GHz，可同時放大多工讀取訊號'],
      ['random', 'SNAIL / 三波混頻', '非對稱多 JJ 迴路，提供 χ^{(3)} 型非線性，用於參量轉換與耦合'],
      ['layer', '超電感（JJ 陣列）', '上百個大 JJ 串聯 → 高阻抗、低損耗電感，fluxonium 的核心'],
      ['tachometer', 'SFQ 數位邏輯', '單磁通量子脈衝電路，可在低溫端產生控制訊號，減少佈線'],
    ];
    items.forEach(([ic, t, d], i) => {
      const col = i % 3, row = Math.floor(i / 3);
      const x = 0.6 + col * 4.1, y = 1.5 + row * 2.6;
      card(s, x, y, 3.9, 2.35);
      iconCircle(s, ic, x + 0.25, y + 0.25, 0.6, [C.accent2, C.accent1, C.accent3][col]);
      s.addText(t, { x: x + 1.0, y: y + 0.3, w: 2.8, h: 0.5, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true, valign: 'middle' });
      para(s, [d], x + 0.25, y + 1.0, 3.45, 1.25, { size: 13.5, color: '4A5468' });
    });
  },
  notes: `JJ 除了當量子位元之外，在整個系統裡還扮演很多角色。
可調耦合器：用 SQUID 做成的耦合元件，可以把兩顆量子位元之間的耦合打開或關掉，這是 Google Sycamore 之後很多架構的關鍵。
JPA，約瑟夫森參量放大器：把 JJ 或 SQUID 放進共振腔，用一個泵浦微波驅動它的非線性，就能放大微弱訊號，而且雜訊接近量子力學允許的極限。缺點是頻寬窄。
TWPA，行波參量放大器：把數千個 JJ 串成一條傳輸線，頻寬可以到好幾 GHz，可以同時放大多顆量子位元的讀取訊號。這兩個放大器在讀取部分會再出現。
SNAIL 是一種非對稱的多 JJ 迴路，提供三波混頻的非線性。JJ 陣列可以做成超電感，是 fluxonium 的核心。SFQ 是單磁通量子數位邏輯，有機會在低溫端直接產生控制訊號，減少從室溫拉下來的線。
所以可以說：整台超導量子電腦，從量子位元、耦合器到放大器，處處都是 JJ。`,
});
S({ sec: '02 JJ 元件', title: '退相干來源與對策', min: 2.5,
  async render(s) {
    s.addText(runs('退相干來源與對策'), { placeholder: 'title' });
    const q = [
      ['bug', '二能階系統（TLS）缺陷', '介面氧化物、JJ 阻障內的原子缺陷吸收量子位元能量 → T_{1} 下降、頻率漂移', '表面處理、Ta/Nb 電容板、藍寶石/高阻矽、增大電容板間距', C.accent4],
      ['fire', '準粒子（Quasiparticle）', '紅外線、宇宙射線拆散 Cooper pair；準粒子穿隧 JJ 造成能量損失', '紅外屏蔽、Eccosorb 濾波、準粒子陷阱、間隙工程', C.accent1],
      ['magnet', '磁通雜訊（1/f）', '表面自旋造成低頻磁通漂移 → 可調頻量子位元 T_{2} 下降', '停在甜蜜點、不對稱 SQUID、磁屏蔽', C.accent3],
      ['satellite', '熱光子與 Purcell 效應', '讀取腔中殘留熱光子造成失相；經讀取腔向外輻射造成 T_{1} 下降', '輸入線衰減器、Purcell 濾波器、良好接地與封裝', C.accent2],
    ];
    q.forEach(([ic, t, d, fix, col], i) => {
      const x = 0.6 + (i % 2) * 6.15, y = 1.5 + Math.floor(i / 2) * 2.65;
      card(s, x, y, 5.95, 2.45);
      iconCircle(s, ic, x + 0.25, y + 0.25, 0.6, col);
      s.addText(t, { x: x + 1.0, y: y + 0.28, w: 4.8, h: 0.5, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true, valign: 'middle' });
      para(s, [d, { t: '對策：' + fix, color: C.accent5, bold: false }], x + 0.25, y + 0.95, 5.5, 1.45, { size: 13.5, space: 5 });
    });
  },
  notes: `最後講 JJ 相關的退相干來源，這些都是目前研究的熱點。
第一是 TLS，二能階系統缺陷。在金屬和基板的介面、氧化層裡，有一些原子尺度的缺陷，它們本身像小小的二能階系統，會把量子位元的能量吸走，造成 T1 下降，還會讓頻率隨時間漂移。對策是改善表面處理、換材料，例如鉭電容板，以及把電場集中區域設計得離有損介面遠一點。
第二是準粒子。正常情況下 10 mK 幾乎沒有被拆散的電子，但紅外線、甚至宇宙射線，都可能打斷 Cooper pair 產生準粒子，它們穿隧過 JJ 時會帶走量子位元的能量。對策是紅外屏蔽、濾波器和準粒子陷阱。
第三是磁通雜訊，主要影響可調頻量子位元。對策是停在甜蜜點、用不對稱 SQUID。
第四是熱光子和 Purcell 效應，這兩個都跟讀取電路直接相關，正好帶我們進入第三部分：微波讀取。`,
});

// ===== 03 讀取 =====
S({ sec: '03 微波讀取', layout: 'SECTION_DARK', title: '03 微波讀取', min: 0.5,
  async render(s) {
    s.addText('03', { x: 0.7, y: 1.3, w: 3, h: 1.4, fontSize: 80, bold: true, color: C.accent2, margin: 0, isTextBox: true, fontFace: 'Arial' });
    s.addText(runs('如何用微波讀取量子位元'), { placeholder: 'title' });
    s.addText('電路 QED · 色散讀取 · IQ 解調 · 單發判別 · 讀取鏈 · 量子極限放大器', { placeholder: 'body' });
    await fitImage(s, IMG3('dispersive'), 7.9, 1.0, 5.1, 5.4, { crop: { left: 700, top: 120, width: 1400, height: 1250 } });
  },
  notes: `第三部分，我們來看如何用微波讀出量子位元的狀態。`,
});
S({ sec: '03 微波讀取', title: '讀取要滿足什麼條件？', min: 2,
  async render(s) {
    s.addText(runs('讀取要滿足什麼條件？'), { placeholder: 'title' });
    const rq = [
      ['tachometer', '快速', '讀取時間 ≪ T_{1}；典型 100–500 ns。量子糾錯需要每個週期都讀取', C.accent3],
      ['target', '高保真度', '單發（single-shot）就能判斷 0/1，誤判率 < 1 %', C.accent1],
      ['shield', 'QND（量子非破壞）', '量測後狀態維持在量測結果上，可重複量測、可接著做運算', C.accent5],
      ['sliders', '可擴展、低串擾', '多顆量子位元共用線路（頻率多工），讀取不干擾相鄰量子位元', C.accent2],
    ];
    rq.forEach(([ic, t, d, col], i) => {
      const y = 1.5 + i * 1.3;
      iconCircle(s, ic, 0.6, y + 0.05, 0.7, col);
      s.addText(t, { x: 1.55, y, w: 4.8, h: 0.45, fontSize: 19, bold: true, color: C.text1, margin: 0, isTextBox: true });
      para(s, [d], 1.55, y + 0.48, 5.0, 0.75, { size: 14, color: '4A5468' });
    });
    card(s, 7.0, 1.5, 5.75, 5.15, 'E8F6F8');
    s.addText('為什麼不能直接「量電壓」？', { x: 7.3, y: 1.7, w: 5.2, h: 0.5, fontSize: 18, bold: true, color: C.accent2, margin: 0, isTextBox: true });
    para(s, ['量子位元的能量只有 ~20 μeV，訊號極弱', '直接耦合量測設備 → 引入耗散、破壞相干性', '解法：讓量子位元**間接**影響一個諧振腔，再用微波「探測」諧振腔', '→ 這就是**色散讀取（dispersive readout）**，目前超導量子電腦的標準方法'], 7.3, 2.35, 5.2, 4.1, { size: 15, bullet: true, space: 10 });
  },
  notes: `在講方法之前，先定義一個好的讀取要滿足什麼。
第一，快：必須遠小於 T1，典型是一百到五百奈秒。量子糾錯每個週期都要讀取輔助量子位元，所以讀取速度直接影響糾錯效能。
第二，準：單發讀取，也就是只量一次就能判斷 0 或 1，錯誤率要低於百分之一。
第三，QND，量子非破壞：量完之後量子位元要停留在剛剛量到的狀態，而不是被打亂。
第四，可擴展：很多量子位元要能共用線路，而且讀一顆時不能干擾隔壁。
那為什麼不直接接一條線去量電壓？因為量子位元的能量只有大約 20 微電子伏特，訊號極弱；而且直接接上量測設備會引入耗散，破壞相干性。所以實際的作法是讓量子位元去「間接」影響一個諧振腔，我們再用微波去探測這個諧振腔——這就是色散讀取。`,
});
S({ sec: '03 微波讀取', title: '電路 QED：量子位元 + 讀取諧振腔', anim: 'chip', min: 3,
  async render(s) {
    s.addText(runs('電路 QED：量子位元 + 讀取諧振腔'), { placeholder: 'title' }); animPill(s, 'chip');
    await fitImage(s, IMG3('chip'), 0.6, 1.4, 7.0, 4.6, { crop: { left: 560, top: 140, width: 1720, height: 1170 }, alt: '量子晶片 3D 模型', alignX: 'left' });
    caption(s, '3D 場景 8：Xmon 量子位元、λ/4 讀取諧振腔、共用饋線', 0.6, 6.05, 7.0);
    eqBox(s, ['H_{JC} = ħω_{r} a†a + ½ħω_{q} σ_{z}', '+ ħg (a†σ_{−} + aσ_{+})'], 7.85, 1.5, 4.9, 1.45, { size: 17 });
    table(s, [['原子腔 QED', '電路 QED'], ['原子', 'Transmon（人造原子）'], ['光學共振腔', 'CPW 微波諧振腔'], ['光子（可見光）', '微波光子（~7 GHz）'], ['耦合 g ~ kHz–MHz', 'g/2π ~ 50–200 MHz']], 7.85, 3.2, 4.9, [2.2, 2.7], { size: 13, rowH: 0.43 });
    caption(s, 'λ/4 諧振腔長度約 4 mm（矽基板上）→ f_{r} ≈ 6–8 GHz', 7.85, 5.5, 4.9);
  },
  notes: `讀取的硬體架構叫電路量子電動力學，circuit QED。它的概念借自原子物理：把一顆原子放進一個光學共振腔，研究原子和光子的交互作用。在超導電路裡，原子換成 transmon 這種「人造原子」，光學腔換成一段共平面波導做成的微波諧振腔。
描述它的是 Jaynes–Cummings Hamiltonian：第一項是諧振腔，第二項是量子位元，第三項是兩者以耦合強度 g 交換能量。電路 QED 的優勢是耦合可以做得非常強，g 可以到一兩百 MHz，比原子系統大好幾個數量級。
【切換到 3D 場景 8】這是一個四量子位元的晶片模型。每個十字形就是一顆 Xmon，也就是十字形的 transmon，上端的紅色小環是 SQUID。每顆量子位元下方有一條彎來彎去的線，那是四分之一波長的讀取諧振腔，大約 4 毫米長，共振頻率大約 7 GHz。所有讀取諧振腔都耦合到最下方同一條饋線。可以按「放大 Xmon」看細節。`,
});
S({ sec: '03 微波讀取', title: '色散區域：諧振腔頻率依狀態偏移 ±χ', anim: 'dispersive', min: 3,
  async render(s) {
    s.addText(runs('色散區域：諧振腔頻率依狀態偏移 ±χ'), { placeholder: 'title' }); animPill(s, 'dispersive');
    eqBox(s, [{ t: '當 |Δ| = |ω_{q} − ω_{r}| ≫ g（色散區域）：', size: 15, cjk: true, color: '4A5468' }, 'H_{disp} ≈ ħ(ω_{r} + χσ_{z}) a†a + ½ħ(ω_{q} + χ)σ_{z}', 'χ = g²α / [Δ(Δ + α)]　（transmon）'], 0.6, 1.5, 7.2, 2.4, { size: 19 });
    // 頻譜示意
    const x0 = 0.9, x1 = 7.5, yb = 6.05;
    s.addShape(pres.shapes.LINE, { x: x0, y: yb, w: x1 - x0, h: 0, line: { color: C.text1, width: 1.5, endArrowType: 'triangle' }, objectName: oname('axis') });
    s.addText('頻率 →', { x: x1 - 0.8, y: yb + 0.08, w: 1.0, h: 0.3, fontSize: 12, color: C.accent6, margin: 0, isTextBox: true });
    const peak = (x, h, col, lab) => {
      s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: x - 0.22, y: yb - h, w: 0.44, h, fill: { color: col }, line: { color: col, width: 0 }, objectName: oname('peak') });
      s.addText(runs(lab, {}), { x: x - 1.0, y: yb + 0.1, w: 2.0, h: 0.5, fontSize: 12.5, color: col, align: 'center', margin: 0, isTextBox: true, bold: true });
    };
    peak(2.0, 1.4, C.accent6, 'ω_{q} ≈ 5 GHz\n量子位元');
    peak(5.3, 1.6, C.accent3, 'ω_{r} − χ\n|0⟩');
    peak(6.25, 1.6, C.accent4, 'ω_{r} + χ\n|1⟩');
    s.addText('Δ ≈ −2 GHz', { x: 2.6, y: yb - 1.05, w: 2.2, h: 0.35, fontSize: 13, color: C.text1, align: 'center', margin: 0, isTextBox: true });
    s.addShape(pres.shapes.LINE, { x: 2.3, y: yb - 0.7, w: 2.75, h: 0, line: { color: C.accent6, width: 1, beginArrowType: 'triangle', endArrowType: 'triangle' }, objectName: oname('dim') });
    s.addText('2χ', { x: 5.45, y: yb - 2.15, w: 0.65, h: 0.35, fontSize: 14, bold: true, color: C.accent1, align: 'center', margin: 0, isTextBox: true });
    card(s, 8.1, 1.5, 4.65, 5.2);
    s.addText('物理圖像', { x: 8.4, y: 1.65, w: 4.1, h: 0.45, fontSize: 18, bold: true, color: C.accent1, margin: 0, isTextBox: true });
    para(s, ['失諧很大 → 不交換能量，只互相「推」頻率', '諧振腔頻率成為量子位元狀態的「指示器」', '量測只碰諧振腔，量子位元狀態**不被翻轉** → **QND**', '同一項也代表：腔內每多一個光子，量子位元頻率偏移 2χ（AC Stark shift）→ 讀取光子會造成失相', '光子數需低於 n_{crit} = Δ² / 4g²'], 8.4, 2.2, 4.15, 4.4, { size: 14, bullet: true, space: 8 });
  },
  notes: `電路 QED 的讀取工作在所謂的色散區域：量子位元頻率和諧振腔頻率差得很遠，例如量子位元 5 GHz、諧振腔 7 GHz，失諧 Δ 大約負 2 GHz，遠大於耦合 g。
在這個條件下，兩者不會真正交換能量，而是互相「推」對方的頻率。數學上做一個轉換，會得到上面這條色散 Hamiltonian：諧振腔的頻率變成 ωr 加上 χ 乘 σz。σz 對 |0⟩ 和 |1⟩ 分別是負一和正一，所以諧振腔頻率是 ωr 減 χ 或 ωr 加 χ，取決於量子位元狀態。左下方的頻譜示意就是這個意思，兩個狀態相差 2χ。對 transmon，χ 由 g、Δ 和非諧性 α 一起決定。
物理圖像是：諧振腔的頻率變成量子位元狀態的指示器。我們只去探測諧振腔，量子位元本身不會被翻轉，所以是 QND 量測。
同一個式子反過來讀也很重要：腔內每多一個光子，量子位元頻率就偏移 2χ，這叫 AC Stark shift。如果讀取光子數有漲落，就會讓量子位元失相。另外光子數也不能太多，超過臨界光子數 n_crit，色散近似就失效了。`,
});
S({ sec: '03 微波讀取', title: '讀取原理：穿透訊號的振幅與相位', anim: 'dispersive', min: 3,
  async render(s) {
    s.addText(runs('讀取原理：穿透訊號的振幅與相位'), { placeholder: 'title' }); animPill(s, 'dispersive');
    await fitImage(s, IMGF('dispersive_s21'), 0.6, 1.4, 8.0, 3.0, { alignX: 'left' });
    caption(s, 'κ/2π = 2 MHz、χ/2π = 1 MHz（2χ = κ）；虛線為探測頻率', 0.6, 4.4, 8.0);
    await fitImage(s, IMG3('dispersive'), 0.6, 4.8, 4.3, 2.0, { crop: { left: 650, top: 520, width: 1500, height: 760 }, alignX: 'left' });
    para(s, ['3D 場景 9：兩條 Lorentzian 隨狀態切換', '可調 χ/κ 與探測頻率，觀察 IQ 分離'], 5.1, 5.0, 3.5, 1.7, { size: 13, color: C.accent6 });
    card(s, 8.9, 1.45, 3.85, 5.25);
    s.addText('讀取流程', { x: 9.2, y: 1.6, w: 3.3, h: 0.45, fontSize: 18, bold: true, color: C.accent2, margin: 0, isTextBox: true });
    const st = ['送入頻率在 ω_{r} 附近的微波脈衝', '穿透（或反射）後的訊號**相位**依狀態不同', '探測於兩峰中點：相位差最大、振幅相同', '2χ ≈ κ 時兩狀態在 IQ 平面分離最遠', '放大、解調 → 得到 (I, Q)'];
    st.forEach((t, i) => { numCircle(s, i + 1, 9.2, 2.2 + i * 0.88, 0.42, C.accent2); para(s, [t], 9.75, 2.17 + i * 0.88, 2.85, 0.85, { size: 13.5 }); });
  },
  notes: `實際上怎麼看出諧振腔頻率的差別？我們送一個頻率在 ωr 附近的微波脈衝穿過諧振腔，量測出來的穿透訊號。
左上圖是理論計算：藍色是量子位元在 |0⟩ 時的響應，紅色是 |1⟩。在振幅圖上，兩條 Lorentzian 曲線左右錯開；在相位圖上，兩條相位曲線也錯開。如果我們把探測頻率放在兩峰正中間——就是那條虛線——兩個狀態的振幅一樣，但相位差了 90 度。所以實務上我們主要是靠「相位」來讀取。
諧振腔的線寬 κ 和色散位移 χ 的關係很重要：當 2χ 約等於 κ 的時候，兩個狀態在複數平面上分得最開，這是讀取的最佳化條件之一。
【切換到 3D 場景 9】面板可以切換量子位元狀態，看兩條曲線切換；上方是諧振腔裡的駐波，振幅代表腔內光子數。右下角是 IQ 平面，掃頻時穿透係數畫出一個圓，兩個點是兩個狀態在探測頻率下的位置。試著把 χ/κ 調到 0.5，分離距離達到最大值 1。`,
});
S({ sec: '03 微波讀取', title: '外差解調：從微波到 (I, Q)', min: 3,
  async render(s) {
    s.addText(runs('外差解調：從微波到 (I, Q)'), { placeholder: 'title' });
    const box = (x, y, w, t, col) => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.95, rectRadius: 0.1, fill: { color: col }, line: { color: col, width: 0 }, shadow: shadow(), objectName: oname('block') });
      s.addText(runs(t, {}), { x, y, w, h: 0.95, fontSize: 13, bold: true, color: C.background1, align: 'center', valign: 'middle', margin: 2, isTextBox: true, objectName: oname('block-text') });
    };
    const arrow = (x, y, w) => s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: C.accent6, width: 1.75, endArrowType: 'triangle' }, objectName: oname('arrow') });
    const row1 = [['AWG\nIF 脈衝 (~100 MHz)', C.accent6], ['IQ 混頻器\n上變頻', C.accent3], ['冷凍機\n樣品 + 放大', C.accent2], ['IQ 混頻器\n下變頻', C.accent3], ['ADC\n~1 GS/s', C.accent6], ['FPGA\n數位解調', C.accent1]];
    const bw = 1.75, gap = 0.33;
    row1.forEach(([t, col], i) => { const x = 0.6 + i * (bw + gap); box(x, 1.55, bw, t, col); if (i < row1.length - 1) arrow(x + bw + 0.03, 2.02, gap - 0.06); });
    // LO
    s.addShape(pres.shapes.OVAL, { x: 3.55, y: 2.85, w: 1.0, h: 0.6, fill: { color: C.accent5 }, line: { color: C.accent5, width: 0 }, objectName: oname('lo') });
    s.addText('LO', { x: 3.55, y: 2.85, w: 1.0, h: 0.6, fontSize: 14, bold: true, color: C.background1, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    link(s, 3.85, 2.85, 3.55, 2.5, { color: HEX.accent5, width: 1.5, name: 'lo-line' });
    link(s, 4.55, 3.1, 7.7, 2.5, { color: HEX.accent5, width: 1.5, name: 'lo-line' });
    s.addText('同一個本地振盪源（ω_LO = ω_r − ω_IF）', { x: 4.75, y: 3.05, w: 4.4, h: 0.35, fontSize: 12, color: C.accent5, margin: 0, isTextBox: true });
    eqBox(s, ['I = ∫ s(t) w(t) cos(ω_{IF} t) dt', 'Q = ∫ s(t) w(t) sin(ω_{IF} t) dt'], 0.6, 3.85, 5.9, 1.65, { size: 19 });
    caption(s, 's(t)：數位化後的訊號；w(t)：積分權重（matched filter）', 0.6, 5.55, 5.9);
    card(s, 6.85, 3.85, 5.9, 2.85);
    para(s, [{ t: '要點', bold: true, color: C.accent1, size: 17 }, '**外差**：用 LO 把 7 GHz 降到 ~100 MHz 的中頻，便於數位化', '一條 ADC 通道可同時解調**多個 IF 頻率**（多工）', '**加權積分**（匹配濾波）考慮諧振腔充能與 T_{1} 衰減，可提升 SNR', '結果是每次量測一個複數點 (I, Q)'], 7.1, 4.0, 5.45, 2.65, { size: 14, bullet: false, space: 7 });
  },
  notes: `接下來講訊號處理。量子位元的資訊藏在微波的相位裡，我們要把它轉換成數字。
標準作法是外差解調。室溫端用 AWG 產生一個中頻約 100 MHz 的脈衝，經過 IQ 混頻器和本地振盪源 LO 上變頻到 7 GHz，送進冷凍機。從冷凍機出來、放大之後的訊號，再用同一個 LO 下變頻回中頻，由 ADC 以大約每秒十億次取樣數位化，最後在 FPGA 裡做數位解調。
解調的數學就是下面這兩條：把訊號乘上中頻的 cos 和 sin，再乘上一個權重函數積分，就得到 I 和 Q。權重函數可以設計成匹配濾波器，考慮諧振腔充能的過程和 T1 衰減，能讓訊雜比最好。
外差的好處是：一條 ADC 通道可以同時處理很多個中頻頻率，所以多顆量子位元共用一條讀取線時，只要給每個諧振腔不同的中頻就能分開解調。
最終，每一次量測會得到複數平面上的一個點 (I, Q)。下一頁我們看這些點長什麼樣子。`,
});
S({ sec: '03 微波讀取', title: '單發判別：IQ 叢集與讀取保真度', anim: 'iq', min: 3,
  async render(s) {
    s.addText(runs('單發判別：IQ 叢集與讀取保真度'), { placeholder: 'title' }); animPill(s, 'iq');
    await fitImage(s, IMGF('iq_blobs'), 0.6, 1.4, 7.7, 3.2, { alignX: 'left' });
    caption(s, '模擬：每個狀態 3000 次單發量測（含 3 % 讀取期間 T_{1} 衰減）', 0.6, 4.6, 7.7);
    eqBox(s, ['F = 1 − [P(1|0) + P(0|1)] / 2', { t: 'SNR = |μ_{1} − μ_{0}| / 2σ', size: 16 }], 0.6, 5.05, 4.5, 1.6, { size: 19 });
    await fitImage(s, IMG3('iq'), 5.3, 4.95, 3.0, 1.75, { crop: { left: 380, top: 120, width: 1800, height: 1100 } });
    card(s, 8.6, 1.45, 4.15, 5.25);
    s.addText('誤差來源', { x: 8.9, y: 1.6, w: 3.6, h: 0.45, fontSize: 18, bold: true, color: C.accent4, margin: 0, isTextBox: true });
    para(s, ['**重疊誤差**：放大器雜訊使兩團變寬 → 用量子極限放大器、加長積分', '**T_{1} 衰減**：|1⟩ 在讀取中掉到 |0⟩ → 讀取要快', '**狀態製備誤差**：殘留熱激發 → 主動重置 / 預選', '**讀取誘發躍遷**：光子數過高 → 洩漏到 |2⟩ 以上', '用閾值（垂直平分線）判別；也可用 ML 分類器'], 8.9, 2.15, 3.65, 4.5, { size: 13.5, bullet: true, space: 7 });
  },
  notes: `每次量測得到一個 (I, Q) 點。把量子位元先準備在 |0⟩ 量幾千次，點會聚成一團高斯分佈；準備在 |1⟩，聚成另一團。高斯的寬度來自放大器雜訊，中心的距離來自色散相位差。
判別方法很簡單：在兩團中心的垂直平分線畫一條閾值，落在哪一邊就判成哪個狀態。右邊的直方圖是沿判別軸的投影，用對數座標可以看到兩團之間有一條紅色拖尾，那是準備在 |1⟩ 但在讀取過程中 T1 衰減掉到 |0⟩ 的事件。
讀取保真度定義是 1 減去兩種誤判機率的平均。訊雜比是兩團中心距離除以兩倍標準差。
誤差來源有四類：兩團重疊、讀取中的 T1 衰減、一開始就沒準備好的熱激發、以及光子數太高造成的讀取誘發躍遷。
【切換到 3D 場景 10】每條細線是一次量測的積分軌跡，從上方 t=0 開始，一開始被雜訊淹沒到處亂跑，積分越久越收斂，最後落到 IQ 平面上。試著關掉「量子極限放大器」，兩團會變得很寬、互相重疊，保真度明顯下降；加長積分時間會變好，但 T1 衰減的拖尾也會增加——這就是讀取的根本權衡。`,
});
S({ sec: '03 微波讀取', title: '稀釋冷凍機中的讀取鏈', anim: 'fridge', min: 3,
  async render(s) {
    s.addText(runs('稀釋冷凍機中的讀取鏈'), { placeholder: 'title' }); animPill(s, 'fridge');
    await fitImage(s, IMG3('fridge'), 0.6, 1.35, 4.6, 5.45, { crop: { left: 760, top: 90, width: 1040, height: 1260 }, alt: '稀釋冷凍機讀取鏈 3D 模型', alignX: 'left' });
    table(s, [['溫層', '輸入線（往下）', '輸出線（往上）'],
      ['300 K', 'AWG、IQ 混頻器（≈ −50 dBm）', '室溫放大、下變頻、ADC'],
      ['50 K', '熱錨定', '熱錨定'],
      ['4 K', '衰減器 −20 dB', '**HEMT** 放大 ~40 dB'],
      ['~0.8 K（Still）', '熱錨定（可加 −10 dB）', '超導同軸線'],
      ['~100 mK', '衰減器 −20 dB', '—'],
      ['~10 mK', '衰減器 −20 dB、低通/紅外濾波', '環行器/隔離器、**TWPA/JPA** ~20 dB'],
      ['樣品', '≈ −120 dBm（腔內數個光子）', '訊號 ≈ −120 dBm 起'],
    ], 5.5, 1.45, 7.25, [1.55, 2.85, 2.85], { size: 12.5, rowH: 0.52 });
    caption(s, '3D 場景 11：脈衝沿輸入線逐級衰減、經晶片後逐級放大', 5.5, 5.75, 7.25);
    s.addText('輸入線「衰減」雜訊、輸出線「隔離 + 放大」訊號', { x: 5.5, y: 6.15, w: 7.25, h: 0.5, fontSize: 15, bold: true, color: C.accent1, margin: 0, isTextBox: true });
  },
  notes: `現在把整條讀取鏈放到稀釋冷凍機裡看。冷凍機由上而下有好幾個溫層：室溫、50 K、4 K、Still 大約 0.8 K、Cold plate 約 100 mK，最底下的混合腔約 10 mK，晶片就鎖在這裡，外面包磁屏蔽。
輸入線往下走：每經過一個溫層就放一個衰減器，總共大約負 60 dB。目的是把室溫的熱雜訊壓下去，下一頁會解釋。到晶片時，訊號只剩大約負 120 dBm，相當於腔內只有幾個光子。
輸出線往上走：訊號從晶片出來非常微弱，先經過環行器或隔離器，它們只讓訊號往上走、擋住從上面反射下來的雜訊；接著在 10 mK 就用 TWPA 或 JPA 做第一級放大，大約 20 dB；然後到 4 K 由 HEMT 放大約 40 dB；最後室溫再放大、下變頻、數位化。
【切換到 3D 場景 11】藍色的光球是讀取脈衝，往下走時每經過一個衰減器就變小；經過晶片之後變成金色，往上走經過 TWPA、HEMT 逐級變大。右下角是整條鏈的功率變化圖。可以按「放大混合腔」看底部的細節。`,
});
S({ sec: '03 微波讀取', title: '為什麼輸入線要層層衰減？', anim: 'fridge', min: 2,
  async render(s) {
    s.addText(runs('為什麼輸入線要層層衰減？'), { placeholder: 'title' }); animPill(s, 'fridge');
    await fitImage(s, IMGF('thermal_photons'), 0.6, 1.4, 6.3, 4.6, { alignX: 'left' });
    card(s, 7.2, 1.45, 5.55, 5.25);
    para(s, [{ t: '熱雜訊估算（7 GHz）', bold: true, color: C.accent1, size: 18 },
      '300 K：n_{th} ≈ **890** 個光子',
      '10 mK：n_{th} ≈ **10^{−15}**（理想）',
      '衰減器把訊號與上游雜訊一起壓低，但自身在**冷端**只貢獻該溫度的熱雜訊',
      '每級衰減讓雜訊趨近該溫層 → 總共約 −60 dB 才能讓殘留熱光子 ≲ 10^{−3}',
      '**後果**：腔內殘留熱光子 n̄ 造成失相，Γ_{φ} ≈ n̄κ(2χ)²/(κ² + 4χ²)；以及量子位元殘留熱激發',
      '衰減器本身需良好**熱錨定**，否則自己發熱變成雜訊源'], 7.5, 1.6, 5.0, 5.0, { size: 14, bullet: false, space: 8 });
  },
  notes: `為什麼輸入線要層層衰減？看這張熱光子數對溫度的圖。在 7 GHz，室溫 300 K 的同軸線裡平均有大約 890 個熱光子；降到 10 mK，理論上只剩 10 的負 15 次方個。
如果直接用一條線從室溫接到晶片，室溫的熱雜訊會一路灌進諧振腔。腔內只要有千分之幾個殘留熱光子，透過剛才說的 AC Stark shift，就會讓量子位元頻率隨機跳動，造成失相。
衰減器的作用是：它把訊號和上游的雜訊一起壓低，但它自己在低溫端，只會貢獻它所在溫度的熱雜訊。所以在 4 K、100 mK、10 mK 分別放 20 dB，就能一步一步把雜訊降到接近 10 mK 的水準。訊號也被衰減了沒關係，室溫端多給一點功率就好。
實務上要注意衰減器的熱錨定，否則它自己會發熱，變成新的雜訊源。`,
});
S({ sec: '03 微波讀取', title: '量子極限放大器：JPA 與 TWPA', min: 3,
  async render(s) {
    s.addText(runs('量子極限放大器：JPA 與 TWPA'), { placeholder: 'title' });
    eqBox(s, ['T_{sys} = T_{1} + T_{2}/G_{1} + T_{3}/(G_{1}G_{2}) + …', { t: 'Friis 公式：第一級放大器的雜訊與增益決定整條鏈', size: 14, cjk: true, color: '4A5468' }], 0.6, 1.5, 6.3, 1.5, { size: 19 });
    table(s, [['', 'HEMT（4 K）', 'JPA', 'TWPA'],
      ['原理', '半導體電晶體', 'JJ 非線性諧振腔 + 泵浦', '數千 JJ 傳輸線 + 泵浦'],
      ['增益', '~40 dB', '~20 dB', '~20 dB'],
      ['頻寬', '數 GHz', '~10–100 MHz', '數 GHz'],
      ['加入雜訊', '~10–20 光子（T_{N} 2–4 K）', '~½ 光子（量子極限）', '~½–1 光子'],
      ['多工讀取', '可', '受頻寬限制', '**適合**'],
    ], 0.6, 3.25, 6.3, [1.3, 1.65, 1.7, 1.65], { size: 12.5, rowH: 0.5 });
    card(s, 7.2, 1.5, 5.55, 5.2);
    s.addText('為什麼關鍵？', { x: 7.5, y: 1.65, w: 5.0, h: 0.45, fontSize: 18, bold: true, color: C.accent2, margin: 0, isTextBox: true });
    para(s, ['只有 HEMT 時，訊號被 ~20 倍的雜訊淹沒，需極長積分才能分辨 → 讀取慢於 T_{1}', '加上 TWPA/JPA，雜訊降至接近 ½ 光子的量子極限 → SNR 提升約 **10 dB**', '這使得 **< 200 ns、> 99 %** 的單發讀取成為可能', '**相位保留放大**最少加入 ½ 光子雜訊（量子力學限制）；**相位敏感放大**可在單一象限低於此值', 'JJ 再次登場：放大器的核心也是 JJ 的非線性'], 7.5, 2.2, 5.0, 4.4, { size: 14, bullet: true, space: 8 });
  },
  notes: `讀取鏈裡最關鍵的一環是第一級放大器。根據 Friis 公式，整條放大鏈的等效雜訊溫度，主要由第一級的雜訊決定，後面幾級的雜訊都會被前級的增益除掉。
如果第一級就是 4 K 的 HEMT，它會加入大約十到二十個光子的雜訊，而我們的訊號只有幾個光子，等於被淹沒了，需要積分很久才能分辨，久到 T1 衰減都發生了。
解法是在 10 mK 先放一個約瑟夫森參量放大器。JPA 是一個含 JJ 的非線性諧振腔，用泵浦驅動，增益約 20 dB，但頻寬窄；TWPA 是數千個 JJ 串成的傳輸線，頻寬數 GHz，適合多工讀取。它們加入的雜訊接近量子力學的下限，大約半個光子。這讓訊雜比提升約 10 dB，使得兩百奈秒以內、百分之九十九以上的單發讀取成為可能。
補充一點量子力學：同時放大兩個正交分量的「相位保留放大」，至少會加入半個光子的雜訊，這是測不準原理的結果；如果只放大一個分量，也就是相位敏感放大，可以在那個分量上低於這個限制。
大家可以注意到，JJ 在這裡又出現了——放大器的核心也是 JJ 的非線性。`,
});
S({ sec: '03 微波讀取', title: '讀取設計的權衡', min: 3,
  async render(s) {
    s.addText(runs('讀取設計的權衡'), { placeholder: 'title' });
    await fitImage(s, IMGF('readout_tradeoff'), 0.6, 1.4, 7.6, 2.9, { alignX: 'left' });
    caption(s, '左：χ 隨失諧變化；右：Purcell 效應限制的 T_{1}（g/2π = 100 MHz、κ/2π = 2 MHz）', 0.6, 4.3, 7.6);
    table(s, [['參數', '調大的好處', '調大的代價'],
      ['κ（腔線寬）', '讀取更快（響應時間 ~1/κ）', 'Purcell 衰減 κ(g/Δ)² 增加'],
      ['χ（色散位移）', '狀態分離更大', '熱光子失相、Purcell 增加'],
      ['n̄（讀取光子數）', 'SNR 提升', '超過 n_{crit} 引發躍遷/洩漏'],
    ], 0.6, 4.75, 7.6, [2.0, 2.8, 2.8], { size: 12.5, rowH: 0.47 });
    card(s, 8.5, 1.45, 4.25, 5.25);
    s.addText('設計準則', { x: 8.8, y: 1.6, w: 3.7, h: 0.45, fontSize: 18, bold: true, color: C.accent5, margin: 0, isTextBox: true });
    para(s, ['**2χ ≈ κ**：狀態分離最大（SNR 最佳）', '**n̄ ≲ n_{crit}/數倍**：n_{crit} = Δ²/4g²', '**Purcell 濾波器**：在讀取腔與饋線間加帶通濾波，讓 κ 大而量子位元不經饋線衰減', '量子位元與讀取腔失諧 |Δ| 約 1–2 GHz', '**多工**：各讀取腔間隔 > 數個 κ 以避免串擾'], 8.8, 2.15, 3.75, 4.45, { size: 14, bullet: true, space: 9 });
  },
  notes: `讀取電路的設計是一連串的權衡，這頁整理三個主要參數。
κ 是諧振腔的線寬，也就是它和饋線的耦合強度。κ 大，腔的響應快，讀取就快；但量子位元也會透過腔「漏」到饋線上，這叫 Purcell 效應，衰減率是 κ 乘以 g/Δ 的平方。右上圖紅線顯示，在一般參數下 Purcell 限制的 T1 只有幾十微秒，嚴重拖累量子位元。
χ 大，狀態分離大；但殘留熱光子造成的失相、以及 Purcell 也會變嚴重。左上圖可以看到 χ 隨失諧變化，在量子位元與腔頻率之間的跨越區有奇異點，設計時要避開。
光子數 n̄ 越多，訊號越強；但超過臨界光子數，會引發不想要的躍遷，量子位元甚至被激發到 |2⟩ 以上，這叫洩漏。
設計準則：讓 2χ 約等於 κ；光子數控制在臨界值以下；加上 Purcell 濾波器——它是一個帶通濾波器，讓讀取腔頻率的訊號通過、但擋住量子位元頻率，這樣就能同時有大的 κ 和長的 T1，右上圖綠線就是加了濾波器的效果。`,
});
S({ sec: '03 微波讀取', title: '多工讀取與進階技術', anim: 'chip', min: 2.5,
  async render(s) {
    s.addText(runs('多工讀取與進階技術'), { placeholder: 'title' }); animPill(s, 'chip');
    const items = [
      ['signal', '頻率多工', '一條饋線串接 4–10 個讀取腔（頻率間隔數十 MHz），同一脈衝內含多個頻率同時讀取'],
      ['redo', '主動重置', '讀取後依結果即時施加 π 脈衝（FPGA 回饋 < 1 μs），把量子位元快速歸零'],
      ['cogs', '中途量測（mid-circuit）', '量子糾錯中反覆讀取輔助量子位元，要求快、QND、不擾動資料量子位元'],
      ['layer', '激發態提升（shelving）', '讀取前把 |1⟩ 推到 |2⟩，拉大與 |0⟩ 的差異並降低 T1 誤差'],
      ['brain', '機器學習判別', '以神經網路處理完整時間軌跡，校正串擾與非高斯效應'],
      ['search', '讀取誘發躍遷（MIST）', '高光子數下的非線性共振會使 transmon 離開計算空間，是讀取功率的上限'],
    ];
    items.forEach(([ic, t, d], i) => {
      const col = i % 2, row = Math.floor(i / 2);
      const x = 0.6 + col * 6.15, y = 1.5 + row * 1.75;
      card(s, x, y, 5.95, 1.55);
      iconCircle(s, ic, x + 0.25, y + 0.4, 0.62, [C.accent2, C.accent1][col]);
      s.addText(t, { x: x + 1.1, y: y + 0.15, w: 4.7, h: 0.45, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true });
      para(s, [d], x + 1.1, y + 0.62, 4.7, 0.9, { size: 13.5, color: '4A5468' });
    });
  },
  notes: `最後介紹幾個讀取的進階技術。
頻率多工：剛才在 3D 場景 8 看到，一條饋線上串了四個不同頻率的讀取腔，送一個包含四個頻率的脈衝，就能同時讀四顆。實際系統一條饋線可以接六到十顆。【可切換到 3D 場景 8，按「多工讀取」，右下角是饋線穿透頻譜，四個凹陷分別對應四個讀取腔；切換某顆量子位元狀態，對應的凹陷就會移動。】
主動重置：讀到 1 的話，FPGA 在一微秒內立刻送一個 π 脈衝把它翻回 0，比等它自然衰減快得多。
中途量測：量子糾錯需要在運算中反覆讀取輔助量子位元，要求讀取快、QND、而且不能干擾旁邊的資料量子位元。
激發態提升：讀取前先把 |1⟩ 推到 |2⟩，讓兩個狀態的差別更大，也比較不怕 T1 衰減。
機器學習判別：用神經網路處理完整的時間軌跡，可以修正串擾和非高斯效應。
最後是讀取誘發躍遷，近年的研究發現，光子數太高時 transmon 會被激發離開計算空間，這設下了讀取功率的上限。`,
});
S({ sec: '03 微波讀取', title: '數值範例：設計一組讀取參數', min: 2.5,
  async render(s) {
    s.addText(runs('數值範例：設計一組讀取參數'), { placeholder: 'title' });
    table(s, [['參數', '數值', '說明'],
      ['讀取腔 ω_{r}/2π', '7.0 GHz', 'λ/4 CPW，長約 4 mm'],
      ['量子位元 ω_{q}/2π', '5.0 GHz', 'Δ/2π = −2.0 GHz'],
      ['耦合 g/2π', '100 MHz', '由爪形電容決定'],
      ['非諧性 α/2π', '−250 MHz', '≈ −E_{C}'],
      ['色散位移 χ/2π', '≈ −0.56 MHz', 'χ = g²α / [Δ(Δ+α)]'],
      ['選擇 κ/2π', '≈ 1.1 MHz', '令 κ ≈ 2|χ|'],
      ['臨界光子數 n_{crit}', '100', 'Δ² / 4g²'],
      ['Purcell T_{1} 上限', '≈ 57 μs', '1 / [κ(g/Δ)²] → 需 Purcell 濾波器'],
      ['讀取時間', '~300–600 ns', '數倍 1/κ（≈ 145 ns）'],
    ], 0.6, 1.45, 8.3, [2.6, 2.0, 3.7], { size: 13.5, rowH: 0.49 });
    card(s, 9.2, 1.45, 3.55, 5.25, 'FBF4E8');
    para(s, [{ t: '結論', bold: true, color: C.accent1, size: 18 }, '不加濾波器，讀取腔本身就把 T_{1} 限制在 ~57 μs', '想要更快讀取（κ 更大）→ Purcell 更嚴重', '→ **Purcell 濾波器 + 量子極限放大器**是現代高速高保真讀取的標準配備'], 9.45, 1.6, 3.1, 5.0, { size: 14.5, space: 10 });
  },
  notes: `我們用一組實際數字把前面的公式串起來。
讀取腔 7 GHz，量子位元 5 GHz，失諧負 2 GHz。耦合 g 100 MHz，非諧性負 250 MHz。代入 transmon 的色散位移公式，χ 大約負 0.56 MHz，兩個狀態相差 2χ 約 1.1 MHz。依照 2χ 約等於 κ 的準則，選 κ 大約 1.1 MHz。
臨界光子數是 Δ 平方除以 4g 平方，等於 100，所以讀取光子數要控制在十幾二十個以下。
再算 Purcell 效應：κ 乘以 g/Δ 的平方，換成 T1 大約只有 57 微秒。也就是說，這組參數下，就算 JJ 和材料完美無缺，量子位元的 T1 也會被讀取腔限制在 57 微秒，這對現在動輒幾百微秒的量子位元是不能接受的。
讀取時間大約是幾倍的 1/κ，也就是三百到六百奈秒。
結論：想要讀得快，κ 就要大，但 Purcell 就更嚴重。所以 Purcell 濾波器加上量子極限放大器，是現代高速高保真讀取的標準配備。`,
});

// ===== 04 總結 =====
S({ sec: '04 整合與總結', layout: 'SECTION_DARK', title: '04 整合與總結', min: 0.5,
  async render(s) {
    s.addText('04', { x: 0.7, y: 1.3, w: 3, h: 1.4, fontSize: 80, bold: true, color: C.accent5, margin: 0, isTextBox: true, fontFace: 'Arial' });
    s.addText(runs('整合與總結'), { placeholder: 'title' });
    s.addText('從 JJ 到讀出一個位元的完整旅程', { placeholder: 'body' });
    await fitImage(s, IMG3('fridge'), 8.2, 0.9, 4.6, 5.6, { crop: { left: 760, top: 90, width: 1040, height: 1260 } });
  },
  notes: `最後我們把今天的內容整合起來。`,
});
S({ sec: '04 整合與總結', title: '全流程：從 JJ 到讀出一個位元', min: 2.5,
  async render(s) {
    s.addText(runs('全流程：從 JJ 到讀出一個位元'), { placeholder: 'title' });
    chevrons(s, ['超導 Al\nCooper pair', 'JJ\n非線性電感', 'Transmon\n|0⟩、|1⟩', '耦合讀取腔\n色散 ±χ'], 0.6, 1.55, 12.15, 1.1, [C.accent3, C.accent1, C.accent1, C.accent2]);
    chevrons(s, ['微波探測\n相位差', 'TWPA + HEMT\n放大', '外差解調\n(I, Q)', '閾值判別\n0 或 1'], 0.6, 2.9, 12.15, 1.1, [C.accent2, C.accent5, C.accent5, C.accent4]);
    const cols = [
      ['JJ 提供什麼', ['無耗散非線性 → 非諧能階 → 可定址的量子位元', 'SQUID → 可調頻、可調耦合', '參量放大 → 量子極限讀取']],
      ['讀取靠什麼', ['色散位移：腔頻率隨狀態偏移', '探測相位：QND 量測', '低雜訊鏈：衰減 + 隔離 + 量子極限放大']],
      ['工程挑戰', ['JJ 製程變異 → 頻率定位', '材料缺陷、準粒子 → T_{1}/T_{2}', 'Purcell、光子數、串擾 → 讀取權衡']],
    ];
    cols.forEach(([t, b], i) => {
      const x = 0.6 + i * 4.1;
      card(s, x, 4.35, 3.9, 2.35);
      s.addText(t, { x: x + 0.25, y: 4.45, w: 3.4, h: 0.45, fontSize: 17, bold: true, color: [C.accent1, C.accent2, C.accent4][i], margin: 0, isTextBox: true });
      para(s, b, x + 0.25, 4.95, 3.45, 1.7, { size: 13.5, bullet: true, space: 5 });
    });
  },
  notes: `這頁把今天所有內容串成一條線。
從材料開始：超導鋁裡的電子配對成 Cooper pair，整塊金屬由一個相位描述。兩塊鋁中間夾一層薄氧化層就是 JJ，它是一個無耗散的非線性電感。JJ 並聯大電容就是 transmon，非線性讓我們可以只用 |0⟩ 和 |1⟩ 兩個能階。
讀取時，transmon 耦合到一個失諧很大的讀取腔，腔的頻率依量子位元狀態偏移正負 χ。我們送入微波探測，穿透訊號的相位就帶有狀態資訊；經過 TWPA 和 HEMT 放大、外差解調得到 I 和 Q，最後用閾值判斷是 0 還是 1。
下面三欄是總結：JJ 提供了非線性、可調性，以及量子極限放大；讀取靠的是色散位移、相位探測和低雜訊的讀取鏈；工程挑戰則包括 JJ 製程變異、材料缺陷，以及讀取設計中的各種權衡。`,
});
S({ sec: '04 整合與總結', title: '重點回顧', min: 2,
  async render(s) {
    s.addText(runs('重點回顧'), { placeholder: 'title' });
    const tk = [
      ['JJ = 無耗散的非線性電感', 'I = I_{c} sin φ、dφ/dt = 2eV/ħ；沒有它，超導電路只是線性振盪器'],
      ['E_{J} / E_{C} 決定量子位元性格', 'Transmon 以 E_{J}/E_{C} ≈ 50 換取對電荷雜訊免疫，非諧性 ≈ −E_{C}'],
      ['製程決定頻率', '氧化參數 → R_{n} → I_{c} → f_{01}；頻率定位與 TLS 缺陷是工程核心'],
      ['讀取 = 色散位移 + 相位探測', '腔頻率 ω_{r} ± χ；2χ ≈ κ、n̄ < n_{crit}、Purcell 濾波器'],
      ['讀取鏈決定 SNR', '輸入線衰減熱雜訊、輸出線用 TWPA/JPA 接近量子極限 → 百奈秒級 > 99 % 單發讀取'],
    ];
    tk.forEach(([t, d], i) => {
      const y = 1.5 + i * 1.05;
      numCircle(s, i + 1, 0.6, y + 0.12, 0.62, [C.accent3, C.accent1, C.accent4, C.accent2, C.accent5][i]);
      s.addText(runs(t), { x: 1.45, y, w: 11.2, h: 0.45, fontSize: 19, bold: true, color: C.text1, margin: 0, isTextBox: true });
      para(s, [d], 1.45, y + 0.47, 11.2, 0.5, { size: 14.5, color: '4A5468' });
    });
  },
  notes: `最後用五句話做回顧。
第一，JJ 是無耗散的非線性電感，這是超導量子位元存在的根本。
第二，EJ 和 EC 的比值決定量子位元的性格，transmon 用大比值換取對電荷雜訊的免疫。
第三，製程決定頻率：氧化參數決定電阻、電阻決定臨界電流、臨界電流決定頻率，頻率定位和材料缺陷是工程核心。
第四，讀取靠的是色散位移加上相位探測，設計上要記得 2χ 約等於 κ、光子數低於臨界值，並加上 Purcell 濾波器。
第五，整條讀取鏈決定訊雜比：輸入線衰減熱雜訊，輸出線用量子極限放大器，才能在百奈秒等級做到百分之九十九以上的單發讀取。`,
});
S({ sec: '04 整合與總結', title: '3D 動畫導覽（animations/index.html）', min: 1,
  async render(s) {
    s.addText(runs('3D 動畫導覽'), { placeholder: 'title' });
    const rows = [['場景', '主題', '對應投影片'],
      ['1 Bloch 球', 'Rabi、Ramsey、T1', '5–6'], ['2 Cooper pair', '超導與零電阻', '7–8'], ['3 JJ 結構', '穿隧、DC/AC Josephson', '12–13'], ['4 能階與非諧性', 'LC vs transmon、電荷色散', '10、15、19'],
      ['5 洗衣板位勢', 'RCSJ、遲滯', '16'], ['6 SQUID', '磁通調頻、甜蜜點', '17'], ['7 JJ 製程', 'Dolan bridge 五步驟', '21'], ['8 晶片與多工讀取', 'Xmon、讀取腔、饋線', '27、36'],
      ['9 色散讀取', 'S21 振幅/相位、IQ', '28–29'], ['10 IQ 判別', '單發軌跡、保真度', '31'], ['11 低溫讀取鏈', '衰減、放大、功率變化', '32–33']];
    table(s, rows, 0.6, 1.4, 7.6, [2.6, 3.3, 1.7], { size: 12.5, rowH: 0.42 });
    card(s, 8.5, 1.45, 4.25, 5.25);
    para(s, [{ t: '操作方式', bold: true, color: C.accent2, size: 18 }, '以瀏覽器開啟 animations/index.html（離線可用）', '網址加 #場景代號直接跳轉，例如 index.html#jj', '投影片右上角「▶ 3D 場景」按鈕可直接開啟', '← → 切換場景、空白鍵暫停', 'H 隱藏面板（投影時更乾淨）、F 全螢幕', '滑鼠拖曳旋轉、滾輪縮放、R 重設視角'], 8.75, 1.6, 3.8, 5.0, { size: 14, bullet: false, space: 9 });
  },
  notes: `這頁是 3D 動畫的導覽，方便大家會後自己玩。所有動畫都在 animations 資料夾裡，用瀏覽器打開 index.html 就可以，不需要網路。每個場景都可以用網址後面加井字號跳轉，投影片右上角的按鈕也是這樣連過去的。
操作上：左右方向鍵切換場景、空白鍵暫停、H 可以隱藏說明面板，投影的時候畫面比較乾淨，F 全螢幕，滑鼠可以旋轉縮放。每個場景左邊的面板都有可以調整的參數，歡迎大家會後自己調調看。`,
});
S({ sec: '04 整合與總結', title: '參考文獻與延伸閱讀', min: 0.5,
  async render(s) {
    s.addText(runs('參考文獻與延伸閱讀'), { placeholder: 'title' });
    para(s, [
      'B. D. Josephson, "Possible new effects in superconductive tunnelling," Phys. Lett. 1, 251 (1962).',
      'J. Koch et al., "Charge-insensitive qubit design derived from the Cooper pair box," Phys. Rev. A 76, 042319 (2007).',
      'A. Blais et al., "Cavity quantum electrodynamics for superconducting electrical circuits," Phys. Rev. A 69, 062320 (2004).',
      'A. Blais, A. L. Grimsmo, S. M. Girvin, A. Wallraff, "Circuit quantum electrodynamics," Rev. Mod. Phys. 93, 025005 (2021).',
      'P. Krantz et al., "A quantum engineer\'s guide to superconducting qubits," Appl. Phys. Rev. 6, 021318 (2019).',
      'M. Tinkham, Introduction to Superconductivity, 2nd ed. (Dover, 2004).',
      'V. Ambegaokar, A. Baratoff, "Tunneling between superconductors," Phys. Rev. Lett. 10, 486 (1963).',
      'G. J. Dolan, "Offset masks for lift-off photoprocessing," Appl. Phys. Lett. 31, 337 (1977).',
      'C. Macklin et al., "A near–quantum-limited Josephson traveling-wave parametric amplifier," Science 350, 307 (2015).',
      'E. A. Sete et al., "Quantum theory of a bandpass Purcell filter for qubit readout," Phys. Rev. A 92, 012325 (2015).',
      'T. Walter et al., "Rapid high-fidelity single-shot dispersive readout of superconducting qubits," Phys. Rev. Applied 7, 054020 (2017).',
    ], 0.6, 1.45, 12.15, 5.3, { size: 13.5, bullet: true, space: 6 });
  },
  notes: `這裡列出今天內容的主要參考資料。如果想入門，我最推薦 Krantz 等人寫的「A quantum engineer's guide to superconducting qubits」，以及 Blais 等人 2021 年在 Reviews of Modern Physics 的電路 QED 回顧文章，這兩篇幾乎涵蓋了今天所有內容。Koch 2007 是 transmon 的原始論文。`,
});
S({ sec: '04 整合與總結', layout: 'TITLE_DARK', title: 'Q & A', min: 10,
  async render(s) {
    s.addText(runs('Q & A'), { placeholder: 'title' });
    s.addText('謝謝大家！歡迎提問與討論', { placeholder: 'body' });
    await fitImage(s, IMG3('dispersive'), 8.0, 0.9, 5.1, 5.7, { crop: { left: 700, top: 120, width: 1400, height: 1250 } });
  },
  notes: `以上就是今天的分享，謝謝大家。接下來開放提問。
（備用問答請參考演講稿最後的「Q&A 準備」章節。）`,
});

/* ---------------- 演講稿附錄（Q&A 準備） ---------------- */
const QA = [
  ['為什麼 JJ 幾乎都用鋁？', '鋁的氧化層（AlOx）自我限制生長、厚度均勻且穩定，容易用氧化壓力×時間精確控制穿隧電阻；鋁的超導能隙夠大（~180 μeV），且製程成熟。缺點是 T_c 低（1.2 K），所以電容板等大面積結構常改用 Nb、Ta。'],
  ['Transmon 的非諧性只有 −200 MHz，會不會不小心激發到 |2⟩？', '會，這叫洩漏（leakage）。實務上使用 DRAG 等脈衝整形技術抑制 |1⟩→|2⟩ 的躍遷，並讓脈衝頻寬遠小於非諧性；讀取時也要控制光子數避免讀取誘發躍遷。'],
  ['為什麼不直接讓量子位元和讀取腔共振，讀取不是更強嗎？', '共振時兩者會交換能量（真空 Rabi 振盪），量子位元狀態會被改變，不再是 QND 量測；色散區域才能在不翻轉量子位元的情況下讀取。'],
  ['讀取一定要用穿透（S21）嗎？', '不一定。也可用反射式（S11）量測，或 notch 型（饋線旁掛諧振腔，看穿透凹陷）。多工讀取常用 notch 型，因為多個諧振腔可並聯在同一饋線上。'],
  ['TWPA 和 JPA 要怎麼選？', 'JPA 結構簡單、增益高但頻寬窄（數十 MHz），適合少數量子位元；TWPA 頻寬數 GHz，可同時放大一條饋線上所有讀取腔，是多量子位元系統的主流，但製作較複雜（數千個 JJ）。'],
  ['為什麼讀取保真度比閘保真度難提升？', '讀取需在有限時間內累積足夠 SNR，同時受 T_1 衰減、光子數上限、Purcell 效應、串擾等多重限制，且涉及整條低溫與室溫電子學鏈；任何一環的雜訊或校準誤差都會影響結果。'],
  ['室溫電阻量測真的能預測頻率嗎？', '可以達到約 1–2 % 的準確度。透過 Ambegaokar–Baratoff 關係由 R_n 推得 I_c，再加上設計的 E_C 即可估算頻率；但降溫後的 R_n 變化、老化效應都需要經驗校正。'],
  ['量子位元越多，讀取線會不會不夠？', '這是擴展的主要挑戰之一。對策包括頻率多工（一條線讀 6–10 顆）、寬頻 TWPA、低溫 CMOS 或 SFQ 控制電子學、以及更高密度的柔性同軸/扁平電纜。'],
];

/* ---------------- 產生 ---------------- */
(async () => {
  await loadIcons();
  let curSec = null;
  for (const [i, sd] of SLIDES.entries()) {
    if (sd.sec !== curSec) { pres.addSection({ title: sd.sec }); curSec = sd.sec; }
    const slide = pres.addSlide({ masterName: sd.layout || 'CONTENT', sectionTitle: sd.sec });
    await sd.render(slide);
    const cue = sd.anim ? `【3D 動畫】場景 ${SCENES[sd.anim][0]}「${SCENES[sd.anim][1]}」：animations/index.html#${sd.anim}\n` : '';
    slide.addNotes(`${cue}【建議時間】約 ${sd.min} 分鐘\n\n${sd.notes}`);
  }
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log('written', OUT, SLIDES.length, 'slides');

  // 演講稿
  const total = SLIDES.reduce((a, s) => a + s.min, 0);
  let md = `# 演講稿：超導量子電腦的核心 —— 約瑟夫森接面（JJ）與微波讀取\n\n`;
  md += `> 本稿與 \`slides/JJ_Microwave_Readout_Talk.pptx\` 的講者備註同步產生（來源：\`slides/build/build_deck.js\`）。\n`;
  md += `> 共 ${SLIDES.length} 張投影片，預估總時長約 ${Math.round(total)} 分鐘（含 Q&A 約 10 分鐘）。\n\n`;
  md += `## 使用方式\n\n- 簡報時可在 PowerPoint 的「簡報者檢視畫面」看到每頁的講者備註（與本稿相同）。\n- 標示【切換到 3D 場景 N】的段落，請點投影片右上角的藍綠色按鈕，或在瀏覽器開啟 \`animations/index.html#場景代號\`。\n- 3D 動畫操作：← → 切換場景、空白鍵暫停、H 隱藏面板、F 全螢幕、R 重設視角。\n\n`;
  md += `## 時間規劃\n\n| 段落 | 投影片 | 時間（分） |\n|---|---|---|\n`;
  const secs = {};
  SLIDES.forEach((s, i) => { (secs[s.sec] ||= { a: i + 1, b: i + 1, t: 0 }); secs[s.sec].b = i + 1; secs[s.sec].t += s.min; });
  Object.entries(secs).forEach(([k, v]) => { md += `| ${k} | ${v.a}–${v.b} | ${v.t} |\n`; });
  md += `\n### 60 分鐘精簡版建議\n\n若時間只有一小時，可略過或快速帶過以下進階頁面（內容仍保留在投影片中供會後閱讀）：第 9 頁（磁通量子化，可在 SQUID 頁一句帶過）、第 16 頁（RCSJ 洗衣板）、第 18 頁（量子位元家族）、第 20 頁（典型參數）、第 23 頁（JJ 的其他角色）、第 33 頁（輸入線衰減）、第 36 頁（多工與進階技術）、第 37 頁（數值範例）；Q&A 縮短為 5 分鐘。\n`;
  md += `\n---\n`;
  curSec = null;
  SLIDES.forEach((s, i) => {
    if (s.sec !== curSec) { md += `\n## ${s.sec}\n`; curSec = s.sec; }
    md += `\n### 第 ${i + 1} 頁：${s.title.replace(/\n/g, '').replace(/[_^]\{([^}]*)\}/g, '$1')}\n\n`;
    md += `- 建議時間：約 ${s.min} 分鐘\n`;
    if (s.anim) md += `- 3D 動畫：場景 ${SCENES[s.anim][0]}「${SCENES[s.anim][1]}」→ \`animations/index.html#${s.anim}\`\n`;
    md += `\n${s.notes.split('\n').map((l) => l.trim()).filter(Boolean).join('\n\n')}\n`;
  });
  md += `\n---\n\n## Q&A 準備\n\n`;
  QA.forEach(([q, a], i) => { md += `**Q${i + 1}. ${q}**\n\n${a}\n\n`; });
  md += `## 關鍵公式速查\n\n| 名稱 | 公式 |\n|---|---|\n`;
  [['磁通量子', 'Φ₀ = h/2e ≈ 2.068×10⁻¹⁵ Wb'], ['DC Josephson', 'I = I_c sin φ'], ['AC Josephson', 'dφ/dt = 2eV/ħ（483.6 GHz/mV）'], ['約瑟夫森電感', 'L_J = Φ₀ / (2π I_c cos φ)'],
    ['約瑟夫森能 / 充電能', 'E_J = Φ₀I_c/2π，E_C = e²/2C_Σ'], ['Transmon Hamiltonian', 'H = 4E_C(n − n_g)² − E_J cos φ'], ['Transmon 頻率 / 非諧性', 'ħω₀₁ ≈ √(8E_JE_C) − E_C，α ≈ −E_C'],
    ['Ambegaokar–Baratoff', 'I_c R_n = πΔ/2e'], ['SQUID', 'E_J(Φ) = E_JΣ|cos(πΦ/Φ₀)|√(1 + d²tan²(πΦ/Φ₀))'], ['色散位移（transmon）', 'χ = g²α / [Δ(Δ+α)]'],
    ['臨界光子數', 'n_crit = Δ²/4g²'], ['Purcell 衰減', 'γ = κ(g/Δ)²'], ['讀取保真度', 'F = 1 − [P(1|0) + P(0|1)]/2'], ['熱光子數', 'n_th = 1/(e^{hf/k_BT} − 1)'], ['Friis 公式', 'T_sys = T₁ + T₂/G₁ + …'],
  ].forEach(([a, b]) => { md += `| ${a} | \`${b}\` |\n`; });
  fs.mkdirSync(path.dirname(SPEECH), { recursive: true });
  fs.writeFileSync(SPEECH, md);
  console.log('written', SPEECH);
})().catch((e) => { console.error(e); process.exit(1); });

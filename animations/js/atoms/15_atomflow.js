/* 原子場景 15：運算與讀取總覽 — 6 顆 ⁸⁷Rb 的完整流程：裝載 + 重排 → 光泵浦 → 全域 / 定址單位元閘 → AOD 搬運 → 芮德堡 CZ → 推出 + 螢光成像
 * 量子態用 6 位元狀態向量即時計算（App.qsim）；CZ 只作用在阻斷半徑內的配對。
 * 尺度：1 單位 ≈ 7 μm；光鑷間距 1.5 單位 ≈ 10 μm；阻斷半徑 R_b ≈ 8.7 μm ≈ 1.24 單位。
 */
App.register({
  id: 'atomflow', num: 15, short: '運算與讀取總覽',
  title: '中性原子怎麼運算、怎麼讀取：一次走完',
  subtitle: '不帶電的原子用光鑷夾住；平常互不理睬，激發到芮德堡態才「打開」交互作用；讀取時推掉 |1⟩ 再拍照',
  desc: `<p><b>和離子阱、超導的根本差別</b>：同樣用<b>真的原子</b>（⁸⁷Rb），每顆一模一樣；但原子<b>不帶電</b>，電場抓不住，改用聚焦雷射<b>光鑷</b>（852 nm，深度約 1 mK）一顆一顆夾住。原子之間平常幾乎沒有交互作用——這是優點（串擾小、容易放大到數千顆），也是難處（要做兩位元閘得先「打開」交互作用）。</p>
<p><b>① 裝載 + 重排</b>：MOT 冷到約 10 μK，每支光鑷只有約 50 % 機率抓到一顆原子；拍照找空位，AOD 移動光鑷把原子補齊（場景 10）。<b>② 初始化</b>：光泵浦到 |0⟩ = |F=1, m=0⟩。</p>
<p><b>③ 單位元閘</b>：<br>• <b>全域</b>：6.835 GHz 微波或 Raman 雷射，所有原子一起轉——和超導 XY 驅動、離子的微波閘是同一套 Bloch 球物理。<br>• <b>定址</b>：AOD 打出的聚焦光束照選中的原子，用<b>光位移</b>改變它的頻率 → 局部 Z 旋轉；「全域旋轉 + 局部 Z」組合出任意單位元閘（場景 11）。這裡直接把組合後的效果畫成「定址 π/2」。</p>
<p><b>④ 搬運</b>：連接性由<b>移動</b>決定。AOD 把原子 B 抓起來搬到 A 旁邊（數百 μs）；任意兩顆都能配對，而且可以整排並行搬（場景 13）。</p>
<p><b>⑤ 芮德堡 CZ</b>：420 + 1013 nm 雷射把 |1⟩ 耦合到芮德堡態（n ≈ 70）。距離小於阻斷半徑 R<sub>b</sub>（約 8.7 μm，粉紅球）的兩顆原子最多只能有一顆被激發 → |11⟩ 累積不同的相位 → CZ（約 0.2–0.5 μs，保真度約 99.5 %，場景 12）。<b>一道全域脈衝同時對所有配對做 CZ</b>；距離太遠的原子不會糾纏。</p>
<p><b>⑥ 讀取</b>：先用和 |1⟩（F=2）共振的光把 |1⟩ 的原子<b>推出光鑷</b>，再開 780 nm 拍螢光照片：<b>有亮點 = |0⟩、沒亮點 = |1⟩</b>（和離子阱「亮 = |1⟩」剛好相反）。曝光約 1–20 ms，一次拍下整個陣列；但這是<b>破壞性</b>讀取，被推走的原子要重新裝載；原子意外遺失也會被讀成 |1⟩（場景 14）。</p>
<p><b>三平台對照</b>：雙位元閘 0.3 μs（介於超導 50 ns 與離子 100 μs 之間）；讀取 ms 級最慢；連接性靠搬運（離子靠共享振動、超導靠固定耦合器）；環境是室溫超高真空玻璃腔，不需要稀釋冷凍機。頻率基準與雷射穩頻見場景 16。</p>`,
  camera: { pos: [0.6, 3.6, 11.2], target: [0.6, 0.9, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const QC = App.QC, N = 6, SP = 1.5, Y0 = 1.2, BY = -0.25, BR = 0.32, RB = 1.24;
    const XK = (k) => (k - 2.5) * SP;
    const VTW = App.wlColor(852), V780 = App.wlColor(780), V420 = App.wlColor(420), V1013 = App.wlColor(1013), MWC = 0x38c6d9;

    /* ---------- 原子、光鑷、Bloch 球 ---------- */
    const slots = [];
    for (let k = 0; k < N; k++) {
      const home = new THREE.Vector3(XK(k), Y0, 0);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.012, 6, 20), U.glow(0x55617a, 0.6)); ring.rotation.x = Math.PI / 2; ring.position.set(home.x, Y0 - 0.12, 0); scene.add(ring);
      const tw = new THREE.Mesh(new THREE.ConeGeometry(0.16, 1.3, 16, 1, true), new THREE.MeshBasicMaterial({ color: VTW, transparent: true, opacity: 0.22, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending }));
      tw.rotation.x = Math.PI; scene.add(tw);
      const pt = App.particle(scene, QC.atom, 0.1, home.toArray());
      const lb = ctx.labelOn(pt, `${k + 1}`, [0, 0.32, 0], 'small');
      const s = new THREE.Mesh(new THREE.SphereGeometry(BR, 18, 12), new THREE.MeshBasicMaterial({ color: 0x6f8ab8, wireframe: true, transparent: true, opacity: 0.16 }));
      s.position.set(home.x, BY, 0); scene.add(s);
      const a = U.fatArrow(0xffd28a, BR, 0.022); a.position.set(home.x, BY, 0); scene.add(a);
      slots.push({ k, home, pos: home.clone(), tw, pt, lb, arrow: a, present: false, from: null, gone: 0, lbRes: ctx.label('', [home.x, BY - BR - 0.28, 0], 'small') });
    }
    ctx.label('852 nm 光鑷陣列（間距約 10 μm）', [XK(0) - 0.4, Y0 - 1.0, 0.9], 'small');
    ctx.label('|0⟩ ↑　Bloch 向量　↓ |1⟩', [XK(0) - 0.9, BY + BR + 0.25, 0], 'small');
    const blockade = new THREE.Mesh(new THREE.SphereGeometry(RB, 32, 20), new THREE.MeshBasicMaterial({ color: QC.ryd, transparent: true, opacity: 0, depthWrite: false }));
    scene.add(blockade);
    const lbBlock = ctx.label('阻斷半徑 R_b ≈ 8.7 μm', [0, 0, 0], 'small');
    const arc = U.dynLine(41, 0xff6ad5, 0.0); arc.obj.material.transparent = true; scene.add(arc.obj);
    const lbArc = ctx.label('', [0, 0, 0], 'small');

    /* ---------- 雷射、微波、成像 ---------- */
    const ryd1 = App.beam(scene, [-5.2, Y0 + 0.03, 0.1], [5.2, Y0 + 0.03, 0.1], V420, 0.09, 0.35);
    const ryd2 = App.beam(scene, [5.2, Y0 - 0.03, -0.1], [-5.2, Y0 - 0.03, -0.1], V1013, 0.09, 0.3);
    const lbRyd = ctx.label('全域芮德堡雷射 420 nm + 1013 nm', [4.2, Y0 + 0.45, 0], 'small');
    const addr = App.beam(scene, [0, 3.0, 0], [0, Y0, 0], 0xfff07a, 0.04, 0.7);
    const lbAddr = ctx.label('定址光束（AOD）→ 局部光位移', [0, 0, 0], 'small');
    const push = App.beam(scene, [-5.2, Y0 + 0.08, 0.6], [5.2, Y0 + 0.08, -0.6], V780, 0.07, 0.45);
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 4, 1, true), U.metal(0xb7a46a, { side: THREE.DoubleSide }));
    const HP = new THREE.Vector3(-4.9, -0.2, 1.8); horn.position.copy(HP); horn.lookAt(new THREE.Vector3(0, Y0, 0)); horn.rotateX(-Math.PI / 2); scene.add(horn);
    ctx.label('6.835 GHz 微波號角（全域）', [HP.x, HP.y - 0.45, HP.z], 'small');
    const obj = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.7, 0.6, 28), U.metal(0x2a2f38)); obj.position.set(0, 2.6, -0.4); scene.add(obj);
    scene.add(U.box(1.6, 0.5, 0.6, U.mat(0x1f2633, { metalness: 0.4 }), 0, 3.3, -0.4));
    ctx.label('高 NA 物鏡 → sCMOS / EMCCD 相機', [1.9, 3.3, -0.4], 'small');
    const cv = document.createElement('canvas'); cv.width = 360; cv.height = 110;
    const g2 = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv);
    const img = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 1.0), new THREE.MeshBasicMaterial({ map: tex }));
    img.position.set(4.9, 2.95, -0.9); img.rotation.y = -0.3; scene.add(img);
    ctx.label('相機影像：亮 = |0⟩、暗 = |1⟩', [4.9, 3.65, -0.9], 'gold');
    const lbStage = ctx.label('', [0, -1.25, 0.8], 'gold');
    const ph = App.photons(scene, V780, 220, { size: 0.028 });
    const phMw = App.photons(scene, MWC, 60, { size: 0.025 });

    /* ---------- 狀態 ---------- */
    const sim = App.qsim(N);
    let loaded = false, inited = false, pair = [0, 1], movedB = null;
    let psiPre = sim.copy(), measured = false, bits = null, img8 = null;
    let tab = 'time', hist = null, mark = -1, rydOn = 0;
    const queue = []; let cur = null;
    const P_PUSH_FAIL = 0.005, P_LOSS = 0.005; // 推出不完全（|1⟩ 讀成 0）、原子遺失（|0⟩ 讀成 1）
    const toScene = (b) => new THREE.Vector3(b.x, b.z, -b.y);
    const dist = () => slots[pair[0]].pos.distanceTo(slots[pair[1]].pos);
    const drawCam = () => {
      g2.fillStyle = '#05070c'; g2.fillRect(0, 0, 360, 110);
      for (let k = 0; k < N; k++) {
        const cx = 30 + k * 60, on = img8 ? img8[k] : 0;
        const grd = g2.createRadialGradient(cx, 45, 1, cx, 45, 24);
        grd.addColorStop(0, `rgba(255,120,120,${0.06 + 0.94 * on})`); grd.addColorStop(1, 'rgba(255,60,60,0)');
        g2.fillStyle = grd; g2.fillRect(cx - 28, 17, 56, 56);
        g2.fillStyle = '#9fb0c8'; g2.font = '13px sans-serif'; g2.textAlign = 'center';
        g2.fillText(`原子 ${k + 1}`, cx, 92);
        if (bits) { g2.fillStyle = bits[k] ? '#ffb0b2' : '#a9c6ff'; g2.fillText(`|${bits[k]}⟩`, cx, 107); }
      }
      tex.needsUpdate = true;
    };
    drawCam();
    const clearResult = () => { bits = null; img8 = null; measured = false; slots.forEach((s) => s.lbRes.set('')); drawCam(); };
    const needLoad = () => { if (!loaded || slots.some((s) => !s.present)) { lbStage.set('先按 ① 裝載 + 重排'); return true; } return false; };
    const gate = (name, dur, apply, onTick, m) => ({ dur, name, mark: m, start() { this.psi0 = sim.copy(); clearResult(); }, tick(k) { sim.load(this.psi0); apply(U.smooth(k)); onTick && onTick(k); }, end() { sim.load(this.psi0); apply(1); addr.on(false); } });

    const ACT = {
      load: () => ({ dur: 2.6, name: '① 裝載（約 50 %）→ 拍照 → AOD 補齊空位', start() {
          clearResult(); sim.reset(); inited = false; movedB = null;
          slots.forEach((s) => { s.pos.copy(s.home); s.gone = 0; s.present = Math.random() < 0.5; s.pt.visible = s.present; s.from = s.present ? null : new THREE.Vector3(s.home.x + (Math.random() - 0.5) * 1.2, Y0, -1.8); });
          loaded = true;
        }, tick(k) { slots.forEach((s) => { if (s.from) { const u = U.smooth(U.clamp((k - 0.35) / 0.6, 0, 1)); s.pos.copy(s.from).lerp(s.home, u); s.pt.visible = k > 0.25; } }); },
        end() { slots.forEach((s) => { s.present = true; s.from = null; s.pos.copy(s.home); s.pt.visible = true; }); mark = 0; } }),
      pump: () => ({ dur: 1.2, name: '② 光泵浦：全部送進 |0⟩', start() { if (needLoad()) { this.dur = 0; return; } clearResult(); sim.reset(); inited = true; }, tick() {}, end() { psiPre = sim.copy(); mark = 0; } }),
      mw: () => gate('③ 全域微波 π/2：六顆一起轉', 1.3, (s) => { for (let k = 0; k < N; k++) sim.ry(k, (Math.PI / 2) * s); },
        () => phMw.emit(HP, new THREE.Vector3(U.gauss() * 1.5, Y0 - HP.y, -HP.z).normalize(), 3.4, 1.5), 1),
      addrA: () => gate(`③′ 定址 π/2 → 原子 ${pair[0] + 1}（A）`, 1.3, (s) => sim.ry(pair[0], (Math.PI / 2) * s), () => { const p = slots[pair[0]].pos; addr.set([p.x, 3.0, p.z], p); addr.on(true); lbAddr.pos.set(p.x + 0.2, 2.3, p.z); }, 1),
      addrB: () => gate(`③′ 定址 π/2 → 原子 ${pair[1] + 1}（B）`, 1.3, (s) => sim.ry(pair[1], (Math.PI / 2) * s), () => { const p = slots[pair[1]].pos; addr.set([p.x, 3.0, p.z], p); addr.on(true); lbAddr.pos.set(p.x + 0.2, 2.3, p.z); }, 1),
      move: () => ({ dur: 2.4, name: `④ AOD 搬運：把原子 ${pair[1] + 1} 搬到 ${pair[0] + 1} 旁邊`, mark: 3, start() {
          clearResult(); const A = slots[pair[0]], B = slots[pair[1]];
          this.p0 = B.pos.clone(); const side = B.home.x > A.home.x ? 1 : -1;
          this.p1 = new THREE.Vector3(A.pos.x + side * 0.4, Y0, 0); this.mid = this.p0.clone().lerp(this.p1, 0.5).add(new THREE.Vector3(0, 0, 0.9)); movedB = pair[1];
        }, tick(k) { const u = U.smooth(k), B = slots[pair[1]]; const a = this.p0.clone().lerp(this.mid, u), b = this.mid.clone().lerp(this.p1, u); B.pos.copy(a.lerp(b, u)); },
        end() { slots[pair[1]].pos.copy(this.p1); } }),
      cz: () => ({ dur: 2.6, name: '⑤ 全域芮德堡脈衝：R_b 內的配對做 CZ', mark: 2, start() { this.psi0 = sim.copy(); this.ok = dist() < RB; clearResult(); },
        tick(k) { sim.load(this.psi0); if (this.ok) sim.cphase(pair[0], pair[1], Math.PI * U.smooth(k)); rydOn = Math.sin(Math.PI * k); },
        end() { sim.load(this.psi0); if (this.ok) sim.cz(pair[0], pair[1]); rydOn = 0; } }),
      read: () => ({ dur: 3.2, name: '⑥ 推出 |1⟩ → 780 nm 螢光成像', mark: 4, start() {
          psiPre = sim.copy(); clearResult();
          const idx = inited ? sim.sample() : Math.floor(Math.random() * (1 << N));
          if (inited) sim.collapse(idx);
          this.truth = []; bits = []; this.present = [];
          for (let k = 0; k < N; k++) {
            const b = (idx >> k) & 1; this.truth.push(b);
            const stays = b ? Math.random() < P_PUSH_FAIL : Math.random() > P_LOSS;
            this.present.push(stays); bits.push(stays ? 0 : 1);
          }
          measured = true;
        }, tick(k) {
          push.on(k < 0.4, 0.5);
          slots.forEach((s, i) => { if (!this.present[i]) { s.gone = U.clamp(k / 0.4, 0, 1); } });
          if (k > 0.45 && !img8) { img8 = this.present.map((p) => (p ? 1 : 0)); drawCam(); slots.forEach((s, i) => s.lbRes.set(`${this.present[i] ? '有亮點' : '沒亮點'} → <b style="color:${bits[i] ? '#ffb0b2' : '#a9c6ff'}">${bits[i]}</b>`)); }
          this.imaging = k > 0.45;
        },
        end() { push.on(false); slots.forEach((s, i) => { if (!this.present[i]) { s.present = false; s.pt.visible = false; } }); this.imaging = false; } }),
      shots: () => ({ dur: 0.2, name: '同一個線路跑 500 shots', start() {
          const keep = sim.copy(); sim.load(psiPre); const [a, b] = pair; hist = { '00': 0, '01': 0, '10': 0, '11': 0 };
          const rd = (bit) => (bit ? (Math.random() < P_PUSH_FAIL ? 0 : 1) : (Math.random() < P_LOSS ? 1 : 0));
          for (let i = 0; i < 500; i++) { const idx = sim.sample(); hist[`${rd((idx >> a) & 1)}${rd((idx >> b) & 1)}`]++; }
          const ideal = { '00': 0, '01': 0, '10': 0, '11': 0 };
          sim.probs().forEach((v, idx) => { ideal[`${(idx >> a) & 1}${(idx >> b) & 1}`] += v; });
          hist.ideal = ideal; sim.load(keep); tab = 'hist'; tabUI.set('hist');
        }, tick() {}, end() {} }),
    };
    /* CZ（qsim 只有 cphase；φ = π 即 CZ） */
    sim.cz = (a, b) => sim.cphase(a, b, Math.PI);
    const pushA = (k) => queue.push(ACT[k]());
    ui.radio([['0-1', '配對 1–2'], ['0-5', '配對 1–6（兩端）'], ['2-4', '配對 3–5']], '0-1', (v) => { if (movedB != null) return; pair = v.split('-').map(Number); hist = null; });
    const r1 = ui.row();
    ui.button('① 裝載 + 重排', () => pushA('load'), r1);
    ui.button('② 初始化 |0⟩', () => pushA('pump'), r1);
    ui.button('③ 全域 π/2', () => pushA('mw'), r1);
    const r2 = ui.row();
    ui.button('③′ 定址 π/2 → A', () => pushA('addrA'), r2);
    ui.button('③′ 定址 π/2 → B', () => pushA('addrB'), r2);
    ui.button('④ 搬運 B → A', () => pushA('move'), r2);
    const r3 = ui.row();
    ui.button('⑤ 芮德堡 CZ', () => pushA('cz'), r3);
    ui.button('⑥ 讀取', () => pushA('read'), r3);
    ui.button('跑 500 shots', () => pushA('shots'), r3);
    const r4 = ui.row();
    ui.button('▶ 示範：Bell 態', () => ['load', 'pump', 'addrA', 'addrB', 'move', 'cz', 'addrB', 'read'].forEach(pushA), r4);
    ui.button('重置', () => {
      queue.length = 0; cur = null; sim.reset(); loaded = false; inited = false; movedB = null; hist = null; mark = -1; rydOn = 0; clearResult();
      slots.forEach((s) => { s.present = false; s.pt.visible = false; s.pos.copy(s.home); s.gone = 0; }); addr.on(false); push.on(false);
    }, r4);
    const tabUI = ui.radio([['time', '插圖：時間尺度'], ['hist', '插圖：結果統計']], 'time', (v) => { tab = v; });
    const ro = ui.readout();
    addr.on(false); push.on(false); lbAddr.show(false);
    slots.forEach((s) => { s.pt.visible = false; });

    ctx.inset('', (g, W, H, P) => {
      const t = document.getElementById('inset-title');
      if (tab === 'time') {
        t.textContent = '每一步要多久：三平台比較（log 座標，代表值）';
        App.timeBars(g, W, H, P, ['初始化 / 裝載', '單位元閘', '雙位元閘', '搬運', '讀取'], [
          { name: '超導', col: '#4f8cff', vals: [1e-6, 2.5e-8, 5e-8, 0, 5e-7] },
          { name: '離子阱', col: '#ffc04a', vals: [1e-3, 1e-5, 1e-4, 1e-4, 2e-4] },
          { name: '中性原子', col: '#38d6e9', vals: [2e-1, 1e-6, 3e-7, 5e-4, 5e-3] },
        ], { lo: -8, hi: 0, every: 2, marks: mark >= 0 ? { [mark]: 2 } : null });
      } else {
        t.textContent = `原子 ${pair[0] + 1}、${pair[1] + 1} 的量測結果（虛線 = 理想機率）`;
        if (!hist) { P.text(g, '先建立量子態（例如示範 Bell 態），再按「跑 500 shots」', W / 2, H / 2, '#9fb0c8', 'center'); return; }
        App.bitHist(g, W, H, P, ['00', '01', '10', '11'], hist, { ideal: hist.ideal, col: (k) => (k === '00' ? 'rgba(79,140,255,.8)' : k === '11' ? 'rgba(255,90,95,.8)' : 'rgba(56,214,233,.75)'),
          notes: [['推出不完全 / 原子遺失造成少量錯誤', W - 230, 16, '#ffd28a']] });
      }
    });

    return {
      update(time, dt) {
        if (!cur && queue.length) { cur = queue.shift(); cur.t = 0; cur.start(); if (cur.mark != null) mark = cur.mark; }
        if (cur) {
          cur.t += dt; const k = cur.dur > 0 ? Math.min(1, cur.t / cur.dur) : 1; cur.tick(k);
          if (k >= 1) { const c = cur; cur = null; c.end(); }
        }
        const stage = cur ? cur.name : !loaded ? '光鑷是空的：按 ① 裝載 + 重排' : !inited ? '已裝載：按 ② 初始化' : measured ? '已讀取：被推出的原子要重新裝載' : '待命';
        lbStage.set(stage);
        const imaging = cur && cur.imaging;
        slots.forEach((s, i) => {
          const p = s.pos.clone(); if (s.gone > 0) p.y += s.gone * 2.2;
          s.pt.position.copy(p);
          s.tw.position.set(p.x, p.y - 0.65, p.z); s.tw.visible = s.pt.visible && s.gone < 0.5;
          s.tw.material.opacity = movedB === i && cur && cur.name.startsWith('④') ? 0.55 : 0.22;
          const b = sim.bloch(i);
          const ryd = rydOn * (1 - b.z) / 2;
          s.pt.setColor(ryd > 0.15 ? QC.ryd : QC.atom);
          s.pt.glow(imaging && s.gone === 0 && s.pt.visible ? 1 : 0.35 + ryd);
          if (imaging && s.gone === 0 && s.pt.visible) {
            const rate = 20 * dt;
            for (let j = 0; j < Math.floor(rate) + (Math.random() < rate % 1 ? 1 : 0); j++) { const up = Math.random() < 0.4; ph.emit(p, up ? [U.gauss() * 0.12, 1, U.gauss() * 0.12] : null, 2.6, up ? 0.4 : 0.45); }
          }
          s.arrow.position.set(s.home.x, BY, 0);
          if (!inited || !s.present) { s.arrow.visible = false; return; }
          const v = toScene(b).multiplyScalar(BR);
          if (v.length() < 0.02) s.arrow.visible = false; else s.arrow.setVec(v);
        });
        ph.update(dt); phMw.update(dt);
        ryd1.on(rydOn > 0.02, 0.15 + 0.4 * rydOn); ryd2.on(rydOn > 0.02, 0.12 + 0.35 * rydOn); lbRyd.show(rydOn > 0.02);
        lbAddr.show(addr.visible);
        // 阻斷球與糾纏弧線
        const A = slots[pair[0]], B = slots[pair[1]];
        blockade.position.copy(A.pos); blockade.material.opacity = rydOn > 0.02 ? 0.08 + 0.1 * rydOn : 0.04;
        blockade.visible = loaded; lbBlock.show(loaded); lbBlock.pos.set(A.pos.x, A.pos.y + RB + 0.1, 0);
        const bA = sim.bloch(pair[0]);
        const ent = inited && A.present && B.present ? U.clamp(1 - Math.hypot(bA.x, bA.y, bA.z), 0, 1) : 0;
        const pa = A.pt.position, pb = B.pt.position, hgt = 0.45;
        const ap = []; for (let s = 0; s <= 40; s++) { const u = s / 40; ap.push([pa.x + (pb.x - pa.x) * u, pa.y + 4 * hgt * u * (1 - u), pa.z + (pb.z - pa.z) * u]); }
        arc.set(ap); arc.obj.material.opacity = 0.9 * ent;
        lbArc.pos.set((pa.x + pb.x) / 2, pa.y + hgt + 0.15, 0); lbArc.show(ent > 0.3); lbArc.set(`糾纏 ${(ent * 100).toFixed(0)}%`);
        // 讀數
        const d = dist() * 7;
        const p = sim.probs(); const top = [];
        p.forEach((v, idx) => { if (v > 0.01) top.push([v, idx]); }); top.sort((x, y) => y[0] - x[0]);
        const ket = (idx) => '|' + Array.from({ length: N }, (_, k) => (idx >> k) & 1).join('') + '⟩';
        ro.innerHTML = `狀態：${stage}<br>`
          + (!inited ? '量子態：尚未初始化' : `量子態（原子 1→6）：${top.slice(0, 4).map(([v, idx]) => `${(v * 100).toFixed(0)}% ${ket(idx)}`).join('、')}${top.length > 4 ? '…' : ''}`) + '<br>'
          + (bits ? `讀到的位元串：<b>${bits.join('')}</b>（有亮點 = 0）<br>` : '')
          + `A–B 距離 ≈ <b>${d.toFixed(1)} μm</b>（R_b ≈ 8.7 μm）：${d < 8.7 ? '<b style="color:#8ef0a0">在阻斷半徑內 → 芮德堡脈衝會做 CZ</b>' : '<b style="color:#ff8a8a">太遠 → 先按 ④ 搬運，否則 CZ 不會糾纏</b>'}`;
      },
    };
  },
});

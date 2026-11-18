/* 離子阱場景 7：運算與讀取總覽 — 5 顆離子的完整流程：冷卻 → 光泵浦 → 全域微波 / Raman 定址 → MS 閘（任意配對）→ 螢光讀取
 * 量子態用 5 位元狀態向量即時計算（App.qsim）；讀取用與場景 3 相同的光子計數模型。
 */
App.register({
  id: 'ionflow', num: 7, short: '運算與讀取總覽',
  title: '離子阱怎麼運算、怎麼讀取：一次走完',
  subtitle: '真原子當量子位元：雷射 / 微波轉 Bloch 球、共享振動（聲子）做糾纏、看離子亮不亮讀結果',
  desc: `<p><b>和超導最根本的差別</b>：超導 JJ 是「人造原子」，量子能階由整個電路造出來；離子阱用<b>真的原子</b>，能階是大自然給的，阱只負責把離子固定住。所以每顆量子位元一模一樣（不必逐顆調頻率），真正難的是讓相隔數微米的兩顆離子互相作用。</p>
<p><b>① 冷卻</b>：369 nm Doppler 冷卻（約 0.5 mK）→ 邊帶冷卻，把共享振動冷到接近基態（n̄ ≈ 0）。<b>② 初始化</b>：光泵浦把每顆離子送進 |0⟩（數 μs，&gt; 99.9 %）。</p>
<p><b>③ 單位元閘</b>：<br>• <b>全域微波</b>（12.6 GHz）：物理上和超導的 XY 驅動同一套——脈衝面積 = 旋轉角度、微波相位 = 旋轉軸、Z 閘用軟體做「虛擬 Z」。但微波波長數公分，離子間距只有數微米，<b>無法只打一顆</b>。<br>• <b>Raman 定址</b>：兩道 355 nm 光的頻差 = 12.6 GHz，等效一個「虛擬微波」；光可以聚焦到約 1 μm，<b>只打選中的離子</b>，而且兩道光的動量差能推動離子的振動——這是雙位元閘的必要條件。</p>
<p><b>④ 雙位元閘（Mølmer–Sørensen）</b>：內部能階彼此不會作用，所以借<b>共享的振動模態（聲子）</b>當匯流排。雙色雷射產生自旋相依力，振動在相空間繞一圈回到原點，只留下幾何相位 → <span class="eq">exp(−iπ/4 · X⊗X)</span>，|00⟩ → (|00⟩ − i|11⟩)/√2（細節見場景 5）。整條鏈共享振動，<b>任意兩顆都能直接做</b>（全連接），不需要 SWAP。代價是慢：10–200 μs，約是超導的 1000 倍；但 T₂ 長達秒級，「相干時間內能做幾個閘」反而更多。</p>
<p><b>⑤ 讀取（狀態相依螢光，Dehmelt 的電子擱置法）</b>：369 nm 只和 |1⟩（F=1）的<b>循環躍遷</b>共振 → |1⟩ 每秒散射數百萬個光子（<b>亮</b>）；|0⟩ 差 12.6 GHz，遠大於線寬（約 20 MHz）→ <b>暗</b>。物鏡只收得到幾 % 的光，100–300 μs 內亮態約 10–30 個光子、暗態幾乎 0，設閾值判別，保真度 &gt; 99.9 %。離子不會消失，可以重新初始化再用。中途量測時散射光會干擾鄰居 → QCCD 把離子搬到偵測區（場景 6）。</p>
<p><b>超導對照</b>：XY 微波 ↔ 微波 / Raman 雷射；耦合器 / 共振腔匯流排 ↔ 聲子匯流排；最近鄰 ↔ 全連接；色散讀取（約 500 ns，JPA + HEMT 放大）↔ 螢光光子計數（約 200 μs，PMT / 相機）；10 mK 稀釋冷凍機 ↔ 超高真空 + 雷射冷卻。控制微波的頻率基準見場景 8（氫邁射）。</p>`,
  camera: { pos: [0.9, 3.4, 10.4], target: [0.9, 1.35, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const QC = App.QC, N = 5, SP = 0.9, Y0 = 1.45, BY = 0.15, BR = 0.3;
    const XK = (k) => (k - 2) * SP;
    const V369 = App.wlColor(369), V355 = App.wlColor(355), MWC = 0x38c6d9;

    /* ---------- 線性 Paul 阱 ---------- */
    [[1, 1], [-1, -1], [1, -1], [-1, 1]].forEach(([a, b], k) => {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 6.0, 14), U.metal(k < 2 ? 0xd9a441 : 0x8a93a0, { transparent: true, opacity: 0.35 }));
      m.rotation.z = Math.PI / 2; m.position.set(0, Y0 + a * 0.5, b * 0.5); scene.add(m);
    });
    [-3.1, 3.1].forEach((x) => { const r = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.05, 8, 24), U.metal(0x8a93a0, { transparent: true, opacity: 0.5 })); r.rotation.y = Math.PI / 2; r.position.set(x, Y0, 0); scene.add(r); });
    ctx.label('線性 Paul 阱：RF 電極（金）+ DC 端蓋', [-2.7, Y0 + 0.85, 0.5], 'small');

    /* ---------- 離子、彈簧（庫侖耦合）、Bloch 球 ---------- */
    const ions = [], arrows = [], lbRes = [];
    for (let k = 0; k < N; k++) {
      const p = App.particle(scene, QC.ion, 0.1, [XK(k), Y0, 0]); ions.push(p);
      ctx.labelOn(p, `${k + 1}`, [0, 0.3, 0], 'small');
      const s = new THREE.Mesh(new THREE.SphereGeometry(BR, 18, 12), new THREE.MeshBasicMaterial({ color: 0x6f8ab8, wireframe: true, transparent: true, opacity: 0.16 }));
      s.position.set(XK(k), BY, 0); scene.add(s);
      scene.add(U.line([[XK(k), BY - BR, 0], [XK(k), BY + BR, 0]], 0x9fb0c8, 0.4));
      const a = U.fatArrow(0xffd28a, BR, 0.022); a.position.set(XK(k), BY, 0); scene.add(a); arrows.push(a);
      lbRes.push(ctx.label('', [XK(k), BY - BR - 0.28, 0], 'small'));
    }
    ctx.label('|0⟩ ↑　Bloch 向量　↓ |1⟩（變短 = 和別的離子糾纏）', [0, BY + BR + 0.32, -0.6], 'small');
    const spring = U.dynLine(N, 0x9fb0c8, 0.45); scene.add(spring.obj);
    const arc = U.dynLine(41, 0xff6ad5, 0.0); arc.obj.material.transparent = true; scene.add(arc.obj);
    const lbArc = ctx.label('糾纏', [0, 0, 0], 'small');

    /* ---------- 雷射、微波、成像 ---------- */
    const b369 = App.beam(scene, [-4.2, Y0, 0.9], [4.2, Y0, -0.9], V369, 0.05, 0.45);
    ctx.label('369 nm：冷卻 / 光泵浦 / 偵測（照全部離子）', [3.2, Y0 - 0.45, -1.0], 'small');
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 4, 1, true), U.metal(0xb7a46a, { side: THREE.DoubleSide }));
    const HP = new THREE.Vector3(-3.9, 0.35, 1.6); horn.position.copy(HP); horn.lookAt(new THREE.Vector3(0, Y0, 0)); horn.rotateX(-Math.PI / 2); scene.add(horn);
    ctx.label('12.6 GHz 微波號角（全域）', [HP.x, HP.y - 0.45, HP.z], 'small');
    const raman = [0, 1, 2, 3].map(() => App.beam(scene, [0, 0, 0], [0, 1, 0], V355, 0.035, 0.7));
    const lbRaman = ctx.label('', [0, 0, 0], 'small');
    const obj = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.55, 0.55, 28), U.metal(0x2a2f38)); obj.position.set(0, 2.55, 0); scene.add(obj);
    const camBox = U.box(1.5, 0.5, 0.6, U.mat(0x1f2633, { metalness: 0.4 }), 0, 3.25, 0); scene.add(camBox);
    ctx.label('高 NA 物鏡 → EMCCD / sCMOS 相機', [1.75, 3.25, 0], 'small');
    const cv = document.createElement('canvas'); cv.width = 320; cv.height = 110;
    const g2 = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv);
    const img = new THREE.Mesh(new THREE.PlaneGeometry(2.9, 1.0), new THREE.MeshBasicMaterial({ map: tex }));
    img.position.set(4.6, 2.7, 0); img.rotation.y = -0.25; scene.add(img);
    ctx.label('相機影像：亮 = |1⟩、暗 = |0⟩', [4.6, 3.4, 0], 'gold');
    const lbStage = ctx.label('', [0, -0.75, 0.8], 'gold');
    const ph = App.photons(scene, V369, 220, { size: 0.028 });
    const phMw = App.photons(scene, MWC, 60, { size: 0.025 });

    /* ---------- 狀態 ---------- */
    const sim = App.qsim(N);
    let mixed = true, hot = 1, growK = 1, phAmp = 0, pair = [0, 4];
    let psiPre = sim.copy(), measured = false, counts = null, bits = null;
    let tab = 'time', hist = null, mark = -1;
    const queue = []; let cur = null;
    /* 讀取模型（代表值，同場景 3）：亮態收到 0.1 光子/μs、背景 0.0005/μs、偵測 200 μs；
     * 亮態漏到暗態的時間常數 10 ms、暗態漏到亮態 100 ms → 判別保真度約 99.5–99.9 % */
    const R = 0.1, BG = 0.0005, TDET = 200, TAU1 = 10000, TAU0 = 100000, THR = 1;
    const photonCount = (bright) => {
      const tp = -Math.log(1 - Math.random()) * (bright ? TAU1 : TAU0);
      const te = bright ? Math.min(TDET, tp) : Math.max(0, TDET - tp);
      return App.poisson(R * te + BG * TDET);
    };
    const toScene = (b) => new THREE.Vector3(b.x, b.z, -b.y);
    const raman2 = (k, on, i0 = 0) => {
      const P = new THREE.Vector3(XK(k), Y0, 0);
      raman[i0].set([XK(k) - 0.9, Y0 + 0.05, 1.9], P); raman[i0 + 1].set([XK(k) + 0.9, Y0 + 0.05, 1.9], P);
      raman[i0].on(on); raman[i0 + 1].on(on);
    };
    const ramanOff = () => raman.forEach((r) => r.on(false));
    const drawCam = () => {
      g2.fillStyle = '#05070c'; g2.fillRect(0, 0, 320, 110);
      for (let k = 0; k < N; k++) {
        const cx = 32 + k * 64, n = counts ? counts[k] : 0;
        const a = Math.min(1, n / 22);
        const grd = g2.createRadialGradient(cx, 45, 1, cx, 45, 26);
        grd.addColorStop(0, `rgba(200,170,255,${0.08 + 0.92 * a})`); grd.addColorStop(1, 'rgba(120,80,255,0)');
        g2.fillStyle = grd; g2.fillRect(cx - 30, 15, 60, 60);
        g2.fillStyle = '#9fb0c8'; g2.font = '13px sans-serif'; g2.textAlign = 'center';
        g2.fillText(counts ? `${n} 光子` : `離子 ${k + 1}`, cx, 92);
        if (bits) { g2.fillStyle = bits[k] ? '#ffb0b2' : '#a9c6ff'; g2.fillText(`|${bits[k]}⟩`, cx, 107); }
      }
      tex.needsUpdate = true;
    };
    drawCam();
    const clearResult = () => { counts = null; bits = null; measured = false; lbRes.forEach((l) => l.set('')); drawCam(); };
    const stepGate = (name, dur, apply, onTick) => ({ dur, name, start() { this.psi0 = sim.copy(); clearResult(); }, tick(k) { sim.load(this.psi0); apply(U.smooth(k)); onTick && onTick(k); }, end() { sim.load(this.psi0); apply(1); ramanOff(); } });

    const ACT = {
      cool: () => ({ dur: 2.2, name: '① 冷卻：Doppler + 邊帶冷卻（振動冷到 n̄ ≈ 0）', start() { b369.on(true); clearResult(); }, tick(k) { hot = Math.max(0.03, 1 - k); }, end() { hot = 0.03; b369.on(false); mark = 0; } }),
      pump: () => ({ dur: 1.3, name: '② 光泵浦：全部送進 |0⟩', start() { b369.on(true, 0.3); clearResult(); sim.reset(); mixed = false; growK = 0; }, tick(k) { growK = U.smooth(k); }, end() { growK = 1; b369.on(false); psiPre = sim.copy(); mark = 0; } }),
      mw: () => stepGate('③ 全域微波 π/2：五顆一起轉（無法只打一顆）', 1.3, (s) => { for (let k = 0; k < N; k++) sim.rx(k, (Math.PI / 2) * s); },
        () => phMw.emit(HP, new THREE.Vector3(U.gauss() * 1.2, Y0 - HP.y, -HP.z).normalize(), 3.2, 1.3)),
      raman: () => Object.assign(stepGate(`③′ Raman 定址 π/2：只轉離子 ${pair[0] + 1}`, 1.3, (s) => sim.rx(pair[0], (Math.PI / 2) * s), () => raman2(pair[0], true)), { mark: 1 }),
      ms: () => Object.assign(stepGate(`④ MS 閘：離子 ${pair[0] + 1} 與 ${pair[1] + 1} 經聲子匯流排糾纏`, 3.0, (s) => sim.xx(pair[0], pair[1], (Math.PI / 4) * s),
        (k) => { raman2(pair[0], true, 0); raman2(pair[1], true, 2); phAmp = 0.22 * Math.sin(Math.PI * k); }), { mark: 2 }),
      detect: () => ({ dur: 2.6, name: '⑤ 讀取：369 nm 照全部，數每顆離子的光子', start() {
          b369.on(true);
          psiPre = sim.copy();
          const idx = mixed ? Math.floor(Math.random() * (1 << N)) : sim.sample();
          if (!mixed) sim.collapse(idx);
          bits = []; counts = [];
          for (let k = 0; k < N; k++) { const b = (idx >> k) & 1; const n = photonCount(b === 1); counts.push(n); bits.push(n > THR ? 1 : 0); }
          measured = true; drawCam();
          for (let k = 0; k < N; k++) lbRes[k].set(`${counts[k]} 光子 → <b style="color:${bits[k] ? '#ffb0b2' : '#a9c6ff'}">${bits[k]}</b>`);
        }, tick() {}, end() { b369.on(false); mark = 3; } }),
      shots: () => ({ dur: 0.2, name: '同一個線路跑 500 shots', start() {
          const keep = sim.copy(); sim.load(psiPre); const [a, b] = pair; hist = { '00': 0, '01': 0, '10': 0, '11': 0 };
          for (let i = 0; i < 500; i++) {
            const idx = sim.sample();
            const ba = photonCount(((idx >> a) & 1) === 1) > THR ? 1 : 0, bb = photonCount(((idx >> b) & 1) === 1) > THR ? 1 : 0;
            hist[`${ba}${bb}`]++;
          }
          this.ideal = { '00': 0, '01': 0, '10': 0, '11': 0 };
          const p = sim.probs(); p.forEach((v, idx) => { this.ideal[`${(idx >> a) & 1}${(idx >> b) & 1}`] += v; });
          hist.ideal = this.ideal; sim.load(keep); tab = 'hist'; tabUI.set('hist');
        }, tick() {}, end() {} }),
    };
    const push = (k) => queue.push(ACT[k]());
    ui.radio([['0-1', '配對 1–2（相鄰）'], ['0-4', '配對 1–5（兩端）'], ['1-3', '配對 2–4']], '0-4', (v) => { pair = v.split('-').map(Number); hist = null; });
    const r1 = ui.row();
    ui.button('① 冷卻', () => push('cool'), r1);
    ui.button('② 初始化 |0⟩', () => push('pump'), r1);
    ui.button('③ 全域微波 π/2', () => push('mw'), r1);
    const r2 = ui.row();
    ui.button('③′ Raman 定址 π/2', () => push('raman'), r2);
    ui.button('④ MS 閘（配對）', () => push('ms'), r2);
    ui.button('⑤ 讀取', () => push('detect'), r2);
    const r3 = ui.row();
    ui.button('▶ 示範：Bell 態（①②④⑤）', () => { ['cool', 'pump', 'ms', 'detect'].forEach(push); }, r3);
    ui.button('跑 500 shots', () => push('shots'), r3);
    ui.button('重置', () => { queue.length = 0; cur = null; sim.reset(); mixed = true; hot = 1; growK = 1; phAmp = 0; hist = null; psiPre = sim.copy(); mark = -1; clearResult(); ramanOff(); b369.on(false); }, r3);
    const tabUI = ui.radio([['time', '插圖：時間尺度'], ['hist', '插圖：結果統計']], 'time', (v) => { tab = v; });
    const ro = ui.readout();
    b369.on(false); ramanOff();

    ctx.inset('', (g, W, H, P) => {
      const t = document.getElementById('inset-title');
      if (tab === 'time') {
        t.textContent = '每一步要多久：超導 vs 離子阱（log 座標，代表值）';
        App.timeBars(g, W, H, P, ['冷卻 / 重置', '單位元閘', '雙位元閘', '讀取'], [
          { name: '超導', col: '#4f8cff', vals: [1e-6, 2.5e-8, 5e-8, 5e-7] },
          { name: '離子阱', col: '#ffc04a', vals: [1e-3, 1e-5, 1e-4, 2e-4] },
        ], { lo: -8, hi: -2, marks: mark >= 0 ? { [mark]: 1 } : null });
      } else {
        t.textContent = `離子 ${pair[0] + 1}、${pair[1] + 1} 的量測結果（虛線 = 理想機率）`;
        if (!hist) { P.text(g, '先建立量子態（例如 ①②④），再按「跑 500 shots」', W / 2, H / 2, '#9fb0c8', 'center'); return; }
        App.bitHist(g, W, H, P, ['00', '01', '10', '11'], hist, { ideal: hist.ideal, col: (k) => (k === '00' ? 'rgba(79,140,255,.8)' : k === '11' ? 'rgba(255,90,95,.8)' : 'rgba(200,170,255,.75)'),
          notes: [['讀取誤差讓少數結果落在其他格', W - 205, 16, '#ffd28a']] });
      }
    });

    return {
      update(time, dt) {
        if (!cur && queue.length) { cur = queue.shift(); cur.t = 0; cur.start(); if (cur.mark != null) mark = cur.mark; }
        if (cur) {
          cur.t += dt; const k = Math.min(1, cur.t / cur.dur); cur.tick(k);
          if (k >= 1) { cur.end(); cur = null; phAmp = 0; }
        }
        const stage = cur ? cur.name : mixed ? (hot > 0.5 ? '熱、混合態：按 ① 冷卻、② 初始化' : '已冷卻：按 ② 初始化') : measured ? '已讀取：量子態塌縮成量測結果' : '待命';
        lbStage.set(stage);
        // 離子位置：熱抖動 + MS 期間的集體振動（質心模態，全部同向）
        const pts = [];
        for (let k = 0; k < N; k++) {
          const j = 0.1 * hot;
          const yv = j * 0.5 * Math.sin(time * 17 + k) + phAmp * Math.sin(time * 14);
          ions[k].position.set(XK(k) + j * 0.6 * Math.sin(time * 19 + k * 2), Y0 + yv, j * Math.sin(time * (23 + k * 3) + k));
          pts.push(ions[k].position.toArray());
        }
        spring.set(pts);
        // 讀取時亮的離子散射光子
        const detecting = cur && cur.name.startsWith('⑤');
        const cooling = cur && (cur.name.startsWith('①') || cur.name.startsWith('②'));
        for (let k = 0; k < N; k++) {
          const bright = detecting ? bits && bits[k] : cooling;
          ions[k].glow(bright ? 1 : 0.35);
          const rate = (bright ? (detecting ? 24 : 10) : 0) * dt;
          for (let i = 0; i < Math.floor(rate) + (Math.random() < rate % 1 ? 1 : 0); i++) {
            const up = Math.random() < 0.4;
            ph.emit(ions[k].position, up ? [U.gauss() * 0.12, 1, U.gauss() * 0.12] : null, 2.6, up ? 0.38 : 0.45);
          }
        }
        ph.update(dt); phMw.update(dt);
        // Bloch 向量
        const B = [];
        for (let k = 0; k < N; k++) {
          const b = sim.bloch(k); B.push(b);
          if (mixed) { arrows[k].visible = false; continue; }
          const v = toScene(b).multiplyScalar(BR * growK);
          if (v.length() < 0.02) arrows[k].visible = false; else arrows[k].setVec(v);
        }
        // 糾纏弧線：配對兩顆的 Bloch 向量長度變短（純態下 = 和別人糾纏）
        const [a, bb] = pair;
        const ent = mixed ? 0 : U.clamp(1 - Math.hypot(B[a].x, B[a].y, B[a].z), 0, 1);
        const pa = ions[a].position, pb = ions[bb].position, hgt = 0.35 + 0.12 * (bb - a);
        const ap = []; for (let s = 0; s <= 40; s++) { const u = s / 40; ap.push([pa.x + (pb.x - pa.x) * u, pa.y + 4 * hgt * u * (1 - u), pa.z + (pb.z - pa.z) * u]); }
        arc.set(ap); arc.obj.material.opacity = 0.9 * ent;
        lbArc.pos.set((pa.x + pb.x) / 2, pa.y + hgt + 0.15, 0); lbArc.show(ent > 0.3); lbArc.set(`糾纏 ${(ent * 100).toFixed(0)}%`);
        // Raman 標籤
        const rOn = raman[0].visible;
        lbRaman.show(rOn); if (rOn) { lbRaman.pos.set(XK(pair[0]), Y0 + 0.35, 1.9); lbRaman.set(cur && cur.name.startsWith('④') ? '雙色 Raman（兩組）→ 自旋相依力' : '兩道 355 nm，頻差 12.6 GHz'); }
        // 讀數
        const d = bb - a;
        const p = sim.probs(); const top = [];
        p.forEach((v, idx) => { if (v > 0.01) top.push([v, idx]); }); top.sort((x, y) => y[0] - x[0]);
        const ket = (idx) => '|' + Array.from({ length: N }, (_, k) => (idx >> k) & 1).join('') + '⟩';
        ro.innerHTML = `狀態：${stage}<br>`
          + (mixed ? '量子態：混合態（尚未初始化）' : `量子態（離子 1→5）：${top.slice(0, 4).map(([v, idx]) => `${(v * 100).toFixed(0)}% ${ket(idx)}`).join('、')}${top.length > 4 ? '…' : ''}`) + '<br>'
          + (bits ? `讀到的位元串：<b>${bits.join('')}</b>（> ${THR} 個光子判為 1）<br>` : '')
          + `配對 ${a + 1}–${bb + 1}：離子阱<b style="color:#8ef0a0">直接做 MS 閘</b>（共享振動 = 全連接）；超導一維鏈要先 SWAP ${Math.max(0, d - 1)} 次（每次 3 個 CZ）`;
      },
    };
  },
});

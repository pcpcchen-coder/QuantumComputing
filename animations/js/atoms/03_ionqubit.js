/* 離子阱場景 3：離子量子位元 — ¹⁷¹Yb⁺ 能階、冷卻、光泵浦初始化、微波閘、螢光偵測與光子數直方圖 */
App.register({
  id: 'ionqubit', num: 3, short: '離子量子位元',
  title: '離子量子位元：能階、初始化、閘與螢光讀取',
  subtitle: '¹⁷¹Yb⁺ 的兩個超精細能階就是 |0⟩ 和 |1⟩；用 369 nm 雷射冷卻、初始化，也用它來「看」量子位元',
  desc: `<p><b>量子位元</b>：¹⁷¹Yb⁺ 基態 ²S₁/₂ 的兩個超精細能階 <b>|0⟩ = |F=0, m=0⟩</b>、<b>|1⟩ = |F=1, m=0⟩</b>，相差 12.6 GHz。這是「時鐘躍遷」：對磁場一階不敏感，<b>T₁ 幾乎無限</b>（基態不會自發衰變），<b>T₂ 可達秒級</b>；配合動態解耦與共冷，實驗上做到超過 1 小時（代表值）。</p>
<p><b>① 冷卻</b>：369 nm 雷射略低於共振頻率，離子每吸收一個迎面光子就減速（Doppler 冷卻，約 0.5 mK）；之後再用 sideband / EIT 冷卻到運動基態。<b>935 nm</b> 把偶爾掉到 ²D₃/₂ 的離子打回來。</p>
<p><b>② 初始化</b>：369 nm 加 2.1 GHz 邊帶只激發 F=1 → F′=1，離子最後一定掉進 F=0 = |0⟩，就再也不吸光（光泵浦，約數 μs，保真度 &gt; 99.9%）。</p>
<p><b>③④ 單位元閘</b>：12.6 GHz 微波（或兩道 355 nm 光的頻差 = 12.6 GHz 的 Raman 躍遷）讓量子位元在 Bloch 球上旋轉；脈衝面積決定角度。</p>
<p><b>⑤ 偵測</b>：369 nm 只和 |1⟩（F=1 → F′=0）共振，這是<b>循環躍遷</b>，離子每秒散射上千萬個光子 → <b>亮</b>；|0⟩ 偏離 14.7 GHz → <b>暗</b>。數 PMT 的光子數，超過閾值判為 1。讀取時間約 100–300 μs，保真度 &gt; 99.9%（代表值）。</p>
<p>其他做法：<b>光學量子位元</b>（⁴⁰Ca⁺ 的 S₁/₂ ↔ D₅/₂，729 nm 窄線寬雷射直接驅動）；¹³⁷Ba⁺（可見光波段，Quantinuum Helios 採用）。</p>`,
  camera: { pos: [-0.8, 2.6, 12.6], target: [-0.8, 1.85, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const V369 = App.wlColor(369), V935 = App.wlColor(935), MWC = 0x38c6d9;
    /* ---------- 能階圖 ---------- */
    const SX = -4.4, DX = -2.2;
    const ld = App.levelDiagram(ctx, [
      { key: 's0', x: SX, y: 0.0, w: 1.4, color: App.QC.q0, label: '|0⟩　²S₁/₂ F=0', ldx: -2.3, cls: 'q0' },
      { key: 's1', x: SX, y: 0.5, w: 1.4, color: App.QC.q1, label: '|1⟩　²S₁/₂ F=1', ldx: -2.3, cls: 'q1' },
      { key: 'p0', x: SX, y: 3.0, w: 1.4, color: 0xdfe6f0, label: '²P₁/₂ F′=0', ldx: -2.15 },
      { key: 'p1', x: SX, y: 3.32, w: 1.4, color: 0xdfe6f0, label: '²P₁/₂ F′=1', ldx: -2.15 },
      { key: 'd', x: DX, y: 1.7, w: 1.0, color: 0xb0b8c8, label: '²D₃/₂', ldx: 0.45 },
      { key: 'b', x: DX, y: 4.0, w: 1.0, color: 0xb0b8c8, label: '³D[3/2]₁/₂', ldx: 0.75 },
    ]);
    const A = {
      cool: ld.arrow('s1', 'p0', V369, -0.35, '369 nm'),
      pump: ld.arrow('s1', 'p1', 0xd7b8ff, 0.25, '369 nm + 2.1 GHz'),
      decay: ld.arrow('p0', 'd', 0x8a93a0, 0.55, null),
      repump: ld.arrow('d', 'b', V935, 0.0, '935 nm'),
      back: ld.arrow('b', 's1', 0x8a93a0, -0.1, null),
      mw: ld.arrow('s0', 's1', MWC, 0.55, null),
    };
    const lbDecay = ctx.label('~0.5% 掉到 D₃/₂', [-3.3, 2.55, 0], 'small');
    const lbMw = ctx.label('12.6 GHz 微波', [-3.35, 0.22, 0], 'teal');
    Object.values(A).forEach((a) => a.show(false));
    /* ---------- 離子、雷射、物鏡、PMT、微波號角 ---------- */
    const P0 = new THREE.Vector3(1.5, 1.6, 0);
    const ion = App.particle(scene, App.QC.ion, 0.11, P0.toArray());
    const b369 = App.beam(scene, [-0.9, P0.y, 0], [2.8, P0.y, 0], V369, 0.04, 0.5);
    const b935 = App.beam(scene, [-0.9, P0.y - 0.08, 0.1], [2.8, P0.y - 0.08, 0.1], V935, 0.03, 0.45);
    ctx.label('369 / 935 nm 雷射 →', [-0.2, P0.y - 0.38, 0], 'small');
    ctx.label('Δ = 12.6 GHz', [-3.1, 0.62, 0], 'small');
    ctx.label('Δ = 2.1 GHz', [-3.15, 3.5, 0], 'small');
    const obj = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.34, 0.55, 28), U.metal(0x2a2f38)); obj.position.set(P0.x, 2.75, 0); scene.add(obj);
    const lens = new THREE.Mesh(new THREE.SphereGeometry(0.3, 24, 12), new THREE.MeshStandardMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.6 })); lens.scale.set(1, 0.25, 1); lens.position.set(P0.x, 2.45, 0); scene.add(lens);
    const pmt = U.box(0.6, 0.55, 0.6, U.mat(0x1f2633, { metalness: 0.4, emissive: 0x000000 }), P0.x, 3.4, 0); scene.add(pmt);
    ctx.label('高 NA 物鏡 → PMT（光子計數）', [P0.x + 0.6, 3.95, 0], 'small');
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.55, 4, 1, true), U.metal(0xb7a46a, { side: THREE.DoubleSide }));
    horn.position.set(P0.x, 0.25, 0.9); horn.lookAt(P0); horn.rotateX(-Math.PI / 2); scene.add(horn);
    ctx.label('微波號角', [P0.x + 0.7, 0.2, 1.0], 'small');
    const lbStage = ctx.label('', [P0.x, 0.85, 0], 'gold');
    /* ---------- Bloch 球 ---------- */
    const B0 = new THREE.Vector3(3.8, 1.6, 0), BR = 0.7;
    const sph = new THREE.Mesh(new THREE.SphereGeometry(BR, 24, 16), new THREE.MeshBasicMaterial({ color: 0x6f8ab8, wireframe: true, transparent: true, opacity: 0.18 }));
    sph.position.copy(B0); scene.add(sph);
    scene.add(U.line([[B0.x, B0.y - BR, 0], [B0.x, B0.y + BR, 0]], 0x9fb0c8, 0.6));
    scene.add(U.line([[B0.x - BR, B0.y, 0], [B0.x + BR, B0.y, 0]], 0x9fb0c8, 0.4));
    ctx.label('|0⟩', [B0.x, B0.y + BR + 0.2, 0], 'q0'); ctx.label('|1⟩', [B0.x, B0.y - BR - 0.2, 0], 'q1');
    const vec = U.fatArrow(0xffd28a, BR, 0.035); vec.position.copy(B0); scene.add(vec);
    const lbB = ctx.label('', [B0.x, B0.y - BR - 0.55, 0], 'small');
    const ph = App.photons(scene, V369, 140, { size: 0.03 });
    const phMw = App.photons(scene, MWC, 40, { size: 0.025 });

    /* ---------- 狀態 ---------- */
    let v = new THREE.Vector3(0, 0, 0); // Bloch 向量（z = |0⟩）；長度 0 = 混合態
    let hot = 1; // 運動溫度（1 = 熱、0 = 冷）
    let glow = 0.2, scatter = 0, tDet = 200;
    const queue = []; let cur = null;
    let hist0 = [], hist1 = [], thr = 1, fid = 0, lastCount = null;
    /* 偵測模型（代表值）：亮態偵測到的光子率 0.1 /μs、背景 0.0005 /μs、
     * 亮態經 F′=1 偏共振激發漏到暗態的時間常數 10 ms、暗態漏到亮態 100 ms */
    const R = 0.1, BG = 0.0005, TAU1 = 10000, TAU0 = 100000;
    const sample = (bright, t) => {
      const tp = -Math.log(1 - Math.random()) * (bright ? TAU1 : TAU0);
      const te = bright ? Math.min(t, tp) : Math.max(0, t - tp);
      return App.poisson(R * te + BG * t);
    };
    const nb = () => Math.min(90, Math.ceil(R * tDet * 1.8) + 6);
    const calib = () => {
      const M = 3000; const c0 = [], c1 = [];
      for (let i = 0; i < M; i++) { c0.push(sample(false, tDet)); c1.push(sample(true, tDet)); }
      let best = 1, bt = 0;
      for (let c = 0; c < 12; c++) {
        const e0 = c0.filter((n) => n > c).length / M, e1 = c1.filter((n) => n <= c).length / M;
        if ((e0 + e1) / 2 < best) { best = (e0 + e1) / 2; bt = c; }
      }
      thr = bt; fid = 1 - best;
    };
    const P1 = () => (1 - v.z) / 2;
    const toScene = (b) => new THREE.Vector3(b.x, b.z, -b.y);
    const rotX = (b, a) => new THREE.Vector3(b.x, b.y * Math.cos(a) - b.z * Math.sin(a), b.y * Math.sin(a) + b.z * Math.cos(a));
    const showArrows = (keys) => Object.entries(A).forEach(([k, a]) => a.show(keys.includes(k)));

    const ACT = {
      cool: () => ({ dur: 2.5, name: '① Doppler 冷卻：369 nm + 935 nm', start() { showArrows(['cool', 'decay', 'repump', 'back']); lbDecay.show(true); b369.on(true); b935.on(true); },
        tick(k) { hot = Math.max(0.05, 1 - k); scatter = 1; glow = 0.9; }, end() { scatter = 0; glow = 0.25; b369.on(false); b935.on(false); } }),
      pump: () => ({ dur: 1.6, name: '② 光泵浦：369 nm + 2.1 GHz → 掉進 |0⟩', start() { showArrows(['pump', 'decay', 'repump']); b369.on(true, 0.4); b935.on(true); this.v0 = v.clone(); },
        tick(k) { v = this.v0.clone().lerp(new THREE.Vector3(0, 0, 1), U.smooth(k)); scatter = 1 - k; glow = 0.9 * (1 - k) + 0.15; }, end() { v.set(0, 0, 1); scatter = 0; b369.on(false); b935.on(false); } }),
      half: () => ({ dur: 1.1, name: '③ 微波 π/2：繞 x 軸轉 90°', start() { showArrows(['mw']); lbMw.show(true); this.v0 = v.clone(); },
        tick(k) { v = rotX(this.v0, (Math.PI / 2) * U.smooth(k)); phMw.emit(horn.position, P0.clone().sub(horn.position), 2.2, 0.45); }, end() { v = rotX(this.v0, Math.PI / 2); } }),
      pi: () => ({ dur: 1.5, name: '④ 微波 π：|0⟩ ↔ |1⟩ 翻轉', start() { showArrows(['mw']); lbMw.show(true); this.v0 = v.clone(); },
        tick(k) { v = rotX(this.v0, Math.PI * U.smooth(k)); phMw.emit(horn.position, P0.clone().sub(horn.position), 2.2, 0.45); }, end() { v = rotX(this.v0, Math.PI); } }),
      detect: () => ({ dur: 3.0, name: '⑤ 偵測：369 nm 共振 F=1 → F′=0', start() {
          showArrows(['cool']); b369.on(true);
          const one = Math.random() < P1();
          v.set(0, 0, one ? -1 : 1); this.one = one;
          lastCount = sample(one, tDet);
          (one ? hist1 : hist0)[Math.min(nb() - 1, lastCount)] = ((one ? hist1 : hist0)[Math.min(nb() - 1, lastCount)] || 0) + 1;
        },
        tick() { scatter = this.one ? 1.6 : 0.02; glow = this.one ? 1 : 0.12; }, end() { scatter = 0; b369.on(false); } }),
      shots: () => ({ dur: 0.3, name: '一次跑 1000 shots', start() {
          const p = P1(); hist0 = new Array(nb()).fill(0); hist1 = new Array(nb()).fill(0);
          for (let i = 0; i < 1000; i++) { const one = Math.random() < p; const n = Math.min(nb() - 1, sample(one, tDet)); (one ? hist1 : hist0)[n]++; }
        }, tick() {}, end() {} }),
    };
    const push = (k) => queue.push(ACT[k]());
    const r1 = ui.row();
    ui.button('① Doppler 冷卻', () => push('cool'), r1);
    ui.button('② 光泵浦初始化 |0⟩', () => push('pump'), r1);
    const r2 = ui.row();
    ui.button('③ 微波 π/2', () => push('half'), r2);
    ui.button('④ 微波 π', () => push('pi'), r2);
    ui.button('⑤ 偵測（螢光）', () => push('detect'), r2);
    const r3 = ui.row();
    ui.button('一次跑 1000 shots', () => push('shots'), r3);
    ui.button('重置', () => { queue.length = 0; cur = null; v.set(0, 0, 0); hot = 1; glow = 0.2; scatter = 0; hist0 = []; hist1 = []; lastCount = null; showArrows([]); b369.on(false); b935.on(false); }, r3);
    ui.slider('偵測時間 (μs)', 50, 500, 10, tDet, (x) => { tDet = x; hist0 = []; hist1 = []; calib(); }, (x) => x + ' μs');
    const ro = ui.readout();
    calib();
    b369.on(false); b935.on(false); lbDecay.show(false); lbMw.show(false);

    ctx.inset('偵測光子數直方圖（藍：真值 |0⟩，紅：真值 |1⟩）', (g, W, H, P) => {
      const n = nb();
      const a0 = Array.from({ length: n }, (_, i) => hist0[i] || 0), a1 = Array.from({ length: n }, (_, i) => hist1[i] || 0);
      const step = n > 40 ? 20 : 10;
      const ticks = []; for (let i = 0; i < n; i += step) ticks.push([i + 0.5, String(i)]);
      App.hist2(g, W, H, P, a0, a1, { thr: thr + 1, xlabel: `光子數（${tDet} μs 內）`, xticks: ticks,
        notes: [[`閾值：> ${thr} 個光子判為 |1⟩`, W - 175, 18, '#ffd28a'], [`判別保真度 ≈ ${(fid * 100).toFixed(2)}%`, W - 175, 36, '#8ef0a0'], [`亮態平均 ≈ ${(R * tDet).toFixed(0)} 個`, W - 175, 54, '#ffb0b2']] });
    });

    return {
      update(time, dt) {
        if (!cur && queue.length) { cur = queue.shift(); cur.t = 0; cur.start(); }
        if (cur) {
          cur.t += dt; const k = Math.min(1, cur.t / cur.dur); cur.tick(k);
          if (k >= 1) { cur.end(); lbMw.show(false); lbDecay.show(false); cur = null; }
        }
        const stage = cur ? cur.name : (v.length() < 0.01 ? (hot > 0.5 ? '熱、混合態：先冷卻再初始化' : '已冷卻：尚未初始化') : '待命');
        lbStage.set(stage);
        // 離子：熱運動抖動 + 發光
        const j = 0.12 * hot;
        ion.position.set(P0.x + j * Math.sin(time * 23), P0.y + j * 0.6 * Math.sin(time * 17 + 1), j * 0.8 * Math.sin(time * 29 + 2));
        ion.glow(glow);
        if (!cur && glow > 0.2) glow = Math.max(0.2, glow - dt * 0.5);
        pmt.material.emissive.setHex(scatter > 0.5 ? 0x3a2a66 : 0x000000);
        // 散射光子：一部分往上進物鏡
        const rate = scatter * 60 * dt;
        for (let i = 0; i < Math.floor(rate) + (Math.random() < rate % 1 ? 1 : 0); i++) {
          const up = Math.random() < 0.35;
          ph.emit(ion.position, up ? [U.gauss() * 0.15, 1, U.gauss() * 0.15] : null, 2.6, up ? 0.42 : 0.5);
        }
        ph.update(dt); phMw.update(dt);
        // Bloch 向量
        if (v.length() < 0.01) { vec.visible = false; lbB.set('混合態（向量長度 0）'); }
        else { vec.setVec(toScene(v).multiplyScalar(BR)); lbB.set(`P(|1⟩) = ${(P1() * 100).toFixed(0)}%`); }
        ro.innerHTML = `狀態：${stage}<br>運動溫度：${hot > 0.5 ? '熱（室溫原子源）' : hot > 0.1 ? '冷卻中' : 'Doppler 極限 ~0.5 mK'}<br>`
          + (lastCount !== null ? `上一次偵測：<b>${lastCount}</b> 個光子 → 判為 <b style="color:${lastCount > thr ? '#ffb0b2' : '#a9c6ff'}">|${lastCount > thr ? 1 : 0}⟩</b>（閾值 > ${thr}）` : '按 ① → ② → ③ → ⑤ 走一次完整流程');
      },
    };
  },
});

/* 原子場景 19：三平台比較 — 超導、離子阱、中性原子：連接性、閘速度、相干時間、規模 */
App.register({
  id: 'compare', num: 18, short: '三平台比較',
  title: '三平台比較：超導 · 離子阱 · 中性原子',
  subtitle: '同樣是量子位元，載體、連接方式與時間尺度差了好幾個數量級',
  desc: `<p><b style="color:#7fb0ff">超導</b>：人造原子（電路），閘最快（約 20–100 ns）、讀取快；但相干時間短（約 0.1 ms）、只能連最近鄰、需要 10 mK 稀釋冷凍機與大量佈線。</p>
<p><b style="color:#ffd27a">離子阱</b>：天然離子，保真度最高（兩位元閘 99.9 % 以上）、相干時間長（秒級以上）、同一條鏈內<b>全連接</b>；但閘慢（約 10–200 μs），規模化需要搬運離子（QCCD）或光子互連。</p>
<p><b style="color:#8ef4ff">中性原子</b>：天然原子，<b>最容易放大</b>（已有數千顆）、可移動重排 → 任意配對、並行操作；兩位元閘約 0.3 μs，但搬運與讀取慢（數百 μs 到 ms），原子會丟失需要補充。</p>
<p>用下方按鈕切換比較項目；數值都是 2024–2026 年公開實驗的<b>代表值</b>，各家差異很大。</p>`,
  camera: { pos: [0, 6.2, 11.2], target: [0, 0.5, -0.6] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const COL = { sc: 0x4f8cff, ion: 0xffc04a, atom: 0x38d6e9 };
    const X = { sc: -5, ion: 0, atom: 5 };
    // 底座
    Object.entries(X).forEach(([k, x]) => {
      const d = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.3, 0.15, 48), U.mat(0x1a2232, { metalness: 0.3 })); d.position.set(x, -0.6, 0); scene.add(d);
      const r = new THREE.Mesh(new THREE.TorusGeometry(2.25, 0.02, 6, 64), U.glow(COL[k], 0.7)); r.rotation.x = Math.PI / 2; r.position.set(x, -0.52, 0); scene.add(r);
    });
    ctx.label('<b>超導</b>（Google、IBM…）', [X.sc, -0.9, 2.6], 'q0');
    ctx.label('<b>離子阱</b>（Quantinuum、IonQ…）', [X.ion, -0.9, 2.6], 'gold');
    ctx.label('<b>中性原子</b>（QuEra、Atom Computing…）', [X.atom, -0.9, 2.6], 'teal');

    /* 超導晶片 */
    const chip = U.box(2.6, 0.08, 2.6, U.mat(0x1d2a44, { metalness: 0.5, roughness: 0.4 }), X.sc, -0.3, 0); scene.add(chip);
    const scQ = []; const couplers = [];
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
      const x = X.sc - 0.9 + i * 0.6, z = -0.9 + j * 0.6;
      const g = new THREE.Group();
      g.add(U.box(0.28, 0.05, 0.07, U.metal(0xd8b070)), U.box(0.07, 0.05, 0.28, U.metal(0xd8b070)));
      g.position.set(x, -0.22, z); scene.add(g); scQ.push(g);
      if (i < 3) { const c = U.box(0.32, 0.02, 0.025, U.glow(COL.sc, 0.5), x + 0.3, -0.22, z); scene.add(c); couplers.push(c); }
      if (j < 3) { const c = U.box(0.025, 0.02, 0.32, U.glow(COL.sc, 0.5), x, -0.22, z + 0.3); scene.add(c); couplers.push(c); }
    }
    const fr = App.buildFridge(ctx, { pos: [X.sc - 1.75, -0.55, 0.9], scale: 0.28, canOpacity: 0.15 });
    ctx.label('10 mK 稀釋冷凍機', [X.sc - 1.9, 1.25, 1.0], 'small');

    /* 離子鏈 */
    const rods = [[0.25, 0.25], [-0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]];
    rods.forEach(([y, z]) => { const r = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 3.6, 12), U.metal(0xc98a4b)); r.rotation.z = Math.PI / 2; r.position.set(X.ion, 0.5 + y, z); scene.add(r); });
    const ions = [];
    for (let k = 0; k < 8; k++) ions.push(App.particle(scene, COL.ion, 0.08, [X.ion - 1.4 + k * 0.4, 0.5, 0]));
    const arcs = [];
    for (let a = 0; a < 8; a++) for (let b = a + 1; b < 8; b++) {
      const p1 = ions[a].position, p2 = ions[b].position; const h = 0.15 + 0.12 * (b - a);
      const pts = []; for (let s = 0; s <= 16; s++) { const u = s / 16; pts.push([p1.x + (p2.x - p1.x) * u, 0.5 + 4 * h * u * (1 - u), 0]); }
      const l = U.line(pts, COL.ion, 0.25); scene.add(l); arcs.push(l);
    }

    /* 原子陣列 */
    const atoms = [];
    for (let i = 0; i < 6; i++) for (let j = 0; j < 6; j++) {
      const m = U.sphere(0.08, U.mat(COL.atom, { emissive: COL.atom, emissiveIntensity: 0.7 }), X.atom - 1.25 + i * 0.5, -0.25, -1.25 + j * 0.5, 12);
      scene.add(m); atoms.push({ m, home: m.position.clone() });
    }
    const movers = [0, 7, 14, 21].map((k) => atoms[k]);
    const cones = movers.map(() => { const c = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.9, 12, 1, true), new THREE.MeshBasicMaterial({ color: 0xff4fd8, transparent: true, opacity: 0.4, depthWrite: false, blending: THREE.AdditiveBlending })); c.rotation.x = Math.PI; scene.add(c); return c; });

    /* 比較用的長條（3D） */
    const bars = {}, barL = {};
    Object.entries(X).forEach(([k, x]) => {
      const b = U.box(0.7, 1, 0.5, U.mat(COL[k], { emissive: COL[k], emissiveIntensity: 0.35, transparent: true, opacity: 0.85 }), x, 0, -2.5);
      scene.add(b); bars[k] = b; barL[k] = ctx.label('', [x, 0, -2.5], 'small');
    });
    const caption = ctx.label('', [0, -1.7, 3.2], 'gold');

    const DATA = {
      conn: { cap: '連接性：誰可以直接和誰做兩位元閘', val: { sc: 1.2, ion: 3.0, atom: 2.6 }, txt: { sc: '只連最近鄰（固定佈線）<br>遠距要靠 SWAP', ion: '同一條鏈內全連接<br>（共用振動模態）', atom: '搬運重排 → 任意配對<br>（R_b 內才能直接作用）' } },
      speed: { cap: '閘速度：連續做 1000 個兩位元閘要多久（動畫：1 秒 = 20 ms）', fin: { sc: 50e-6, ion: 0.1, atom: 0.3e-3 }, txt: { sc: '50 ns × 1000 = <b>50 μs</b>', ion: '100 μs × 1000 = <b>0.1 s</b>', atom: '0.3 μs × 1000 = <b>0.3 ms</b><br>（不含搬運）' } },
      coh: { cap: '相干時間內可做的閘數 ≈ T₂ / 兩位元閘時間（log₁₀）', val: { sc: Math.log10(1e-4 / 5e-8), ion: Math.log10(1 / 1e-4), atom: Math.log10(1 / 3e-7) }, txt: { sc: 'T₂ ~0.1 ms / 50 ns<br>≈ <b>2×10³</b>', ion: 'T₂ ~1 s（可更長）/ 100 μs<br>≈ <b>10⁴</b> 以上', atom: 'T₂ ~1 s / 0.3 μs ≈ 3×10⁶<br>計入搬運約 <b>10³–10⁴</b>' } },
      scale: { cap: '規模：已展示的量子位元 / 原子數（log₁₀，2024–2026 代表值）', val: { sc: Math.log10(1121), ion: Math.log10(98), atom: Math.log10(6100) }, txt: { sc: '約 100–1000+<br>（Willow 105、Condor 1121）', ion: '約 100<br>（Helios 98）', atom: '數百到數千<br>（Caltech 陣列 6100）' } },
    };
    let mode = 'conn', tMode = 0;
    const setMode = (m) => { mode = m; tMode = 0; caption.set(DATA[m].cap); Object.keys(X).forEach((k) => barL[k].set(DATA[m].txt[k])); };
    ui.radio([['conn', '連接性'], ['speed', '閘速度'], ['coh', '相干時間'], ['scale', '規模']], 'conn', setMode);
    ui.button('↻ 重播', () => { tMode = 0; });
    const ro = ui.readout();

    ctx.inset('時間尺度比較（秒，log 座標，代表值）', (g, W, H, P) => {
      const { X: Xp, Y } = P.frame(g, W, H, [-8, 1], [0, 3], { xticks: [[-8, '10 ns'], [-6, '1 μs'], [-3, '1 ms'], [0, '1 s']], m: { l: 64, b: 26 } });
      const rows = [['兩位元閘', { sc: 5e-8, ion: 1e-4, atom: 3e-7 }], ['讀取', { sc: 5e-7, ion: 2e-4, atom: 5e-3 }], ['T₂', { sc: 1e-4, ion: 1, atom: 1 }]];
      const cc = { sc: '#4f8cff', ion: '#ffc04a', atom: '#38d6e9' };
      rows.forEach(([n, v], r) => {
        const y = Y(2.5 - r);
        P.text(g, n, 58, y + 4, '#cfd8e6', 'right');
        g.strokeStyle = 'rgba(160,180,210,.2)'; g.beginPath(); g.moveTo(Xp(-8), y); g.lineTo(Xp(1), y); g.stroke();
        Object.entries(v).forEach(([k, s], q) => P.dot(g, Xp(Math.log10(s)), y + (q - 1) * 5, 5, cc[k]));
      });
      P.text(g, '● 超導', 70, 14, cc.sc); P.text(g, '● 離子阱', 140, 14, cc.ion); P.text(g, '● 中性原子', 225, 14, cc.atom);
    });

    setMode('conn');
    return {
      update(t, dt) {
        tMode += dt;
        // 連接性動畫
        const cn = mode === 'conn';
        couplers.forEach((c, i) => (c.material.opacity = cn ? 0.5 + 0.4 * Math.sin(t * 4 + i) : 0.35));
        arcs.forEach((a, i) => (a.material.opacity = cn ? 0.2 + 0.25 * (0.5 + 0.5 * Math.sin(t * 3 + i * 0.4)) : 0.12));
        ions.forEach((p, k) => { p.position.x = X.ion - 1.4 + k * 0.4 + 0.02 * Math.sin(t * 5 + k); });
        movers.forEach((a, k) => {
          const ph = (t * 0.35 + k * 0.25) % 1; const e = U.smooth(ph < 0.5 ? ph * 2 : 2 - ph * 2);
          a.m.position.copy(a.home).add(new THREE.Vector3(e * (1.0 + 0.5 * (k % 2)), 0, e * (0.5 * ((k + 1) % 2) + 0.25)));
          cones[k].position.copy(a.m.position).add(new THREE.Vector3(0, 0.5, 0));
        });
        // 長條
        Object.keys(X).forEach((k) => {
          let h;
          if (mode === 'speed') { const real = (tMode * 0.02); h = Math.min(1, real / DATA.speed.fin[k]) * 2.4; }
          else if (mode === 'conn') h = DATA.conn.val[k] * 0.8;
          else h = (DATA[mode].val[k] / 7) * 2.8 * Math.min(1, tMode * 1.5);
          h = Math.max(0.03, h);
          bars[k].scale.y = h; bars[k].position.y = -0.55 + h / 2;
          barL[k].pos.set(X[k], -0.55 + h + 0.45, -2.5);
        });
        if (mode === 'speed') {
          const real = tMode * 0.02;
          const st = (k) => (real >= DATA.speed.fin[k] ? '✓ 完成' : `${(100 * real / DATA.speed.fin[k]).toFixed(0)} %`);
          ro.innerHTML = `真實時間 ${real < 1e-3 ? (real * 1e6).toFixed(0) + ' μs' : (real * 1e3).toFixed(1) + ' ms'} · 超導 ${st('sc')} · 中性原子 ${st('atom')} · 離子阱 ${st('ion')}`;
        } else ro.innerHTML = DATA[mode].cap;
      },
    };
  },
});

/* 原子場景 9：⁸⁷Rb 原子量子位元的能階與單位元閘（全域旋轉 + 局部定址） */
App.register({
  id: 'atomqubit', num: 9, short: '原子量子位元與單位元閘',
  title: '原子量子位元：能階編碼與單位元閘',
  subtitle: '量子位元 = 原子基態的兩個超精細能階；全域微波一次轉全部，局部光束只改選中的原子',
  desc: `<p><b>⁸⁷Rb 的編碼</b>：基態 5S₁/₂ 的兩個超精細能階 <b>|0⟩ = |F=1, m=0⟩</b>、<b>|1⟩ = |F=2, m=0⟩</b>，相差 <b>6.835 GHz</b>。這兩個能階幾乎不會自發衰變（T₁ 很長），相干時間主要受雷射與磁場雜訊限制。</p>
<p>其他編碼：<b>¹³³Cs</b> 超精細（9.19 GHz）；<b>⁸⁷Sr、¹⁷¹Yb</b> 的<b>核自旋</b>（對磁場與光鑷更不敏感）；<b>基態 ↔ 芮德堡態</b>（QuEra Aquila 等類比模式）；<b>光學時鐘躍遷</b>（Sr 698 nm）。</p>
<p><b>單位元閘</b>：<br>• <b>全域</b>：6.8 GHz 微波（約 10–100 μs）或 Raman 雷射（約 1 μs），所有原子一起轉。<br>
• <b>局部定址</b>：AOD 打出的聚焦光束只照選中的原子，用<b>光位移</b>改變它的頻率 → 局部 Z 旋轉。<br>
• 「全域旋轉 + 局部 Z」可組合出任意單位元閘。例如 X(π/2) → 局部 Z(π) → X(π/2)：沒被照到的原子翻成 |1⟩，被照到的原子回到 |0⟩。</p>
<p>每顆原子上的箭頭是它的 Bloch 向量（藍 = |0⟩、紅 = |1⟩、紫 = 疊加）。</p>`,
  camera: { pos: [-0.4, 0.5, 10.5], target: [-0.6, 0.3, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const QC = App.QC;
    /* ---- 能階圖 ---- */
    // 註：自行加標籤（加上整張圖的位移）
    const OFF = [-5.2, -2.4, 0];
    const LEV = [
      { key: 'g0', y: 0, x: 0, w: 3.2, color: QC.q0, label: '5S₁/₂ F=1 → <b>|0⟩</b>', cls: 'q0' },
      { key: 'g1', y: 0.5, x: 0, w: 3.2, color: QC.q1, label: '5S₁/₂ F=2 → <b>|1⟩</b>', cls: 'q1' },
      { key: 'p5', y: 2.2, x: -0.4, w: 2.4, color: 0xdfe6f0, label: '5P₃/₂' },
      { key: 'p6', y: 3.3, x: 0.4, w: 2.4, color: 0xdfe6f0, label: '6P₃/₂（中間態）' },
      { key: 'r', y: 4.7, x: 0, w: 3.2, color: QC.ryd, label: '芮德堡態 |r⟩（n ≈ 50–70）', cls: 'small' },
    ];
    const LD = App.levelDiagram(ctx, LEV.map((L) => ({ ...L, label: null })), { pos: OFF });
    LEV.forEach((L) => ctx.label(L.label, [OFF[0] + L.x + L.w / 2 + (L.key === 'r' ? 1.25 : 0.9), OFF[1] + L.y + (L.key === 'g1' ? 0.08 : L.key === 'g0' ? -0.08 : 0), 0], L.cls || 'small'));
    const lv = LD.lv;
    const arr = (k1, k2, col, x, label) => {
      const off = new THREE.Vector3(...OFF);
      const p1 = new THREE.Vector3(x, lv[k1].y, 0).add(off), p2 = new THREE.Vector3(x, lv[k2].y, 0).add(off);
      const a = U.fatArrow(col, 1, 0.03); a.position.copy(p1); a.setVec(p2.clone().sub(p1)); scene.add(a);
      a.lbl = ctx.label(label, p1.clone().lerp(p2, 0.5).add(new THREE.Vector3(-0.05, 0, 0.3)), 'small');
      return a;
    };
    const mwArrow = arr('g0', 'g1', 0xe0a54a, -1.25, '6.835 GHz 微波 / Raman');
    mwArrow.lbl.pos.set(OFF[0] - 0.6, OFF[1] - 0.5, 0.3);
    arr('g1', 'p5', App.wlColor(780), -0.6, '780 nm<br>冷卻、成像');
    arr('g1', 'p6', App.wlColor(420), 0.55, '420 nm');
    arr('p6', 'r', App.wlColor(1013), 0.55, '1013 nm');
    ctx.label('⁸⁷Rb 能階（示意，非比例）', [OFF[0], 3.0, 0], 'gold');

    /* ---- 4×4 原子陣列 ---- */
    const atoms = [];
    for (let j = 0; j < 4; j++) for (let i = 0; i < 4; i++) {
      const P = new THREE.Vector3(0.9 + i * 1.05, 1.6 - j * 1.05, 0);
      const pt = App.particle(scene, QC.q0, 0.11, P.toArray());
      const ar = U.fatArrow(QC.q0, 0.42, 0.025); ar.position.copy(P); scene.add(ar);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.02, 8, 30), U.glow(0xff4fd8, 0.9)); ring.position.copy(P); ring.visible = false; scene.add(ring);
      const beam = App.beam(scene, [P.x, P.y, 3.5], [P.x, P.y, 0], 0xff4fd8, 0.05, 0.5); beam.visible = false;
      atoms.push({ i, j, P, pt, ar, ring, beam, s: [1, 0, 0, 0], start: null, sel: false });
    }
    ctx.label('4×4 原子陣列（每顆都是一個量子位元）', [2.48, 2.65, 0], 'teal');
    // 微波號角與波前
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 4, 1, true), U.metal(0xd4a050, { side: THREE.DoubleSide }));
    horn.position.set(5.3, 2.4, 0.6); horn.rotation.z = -Math.PI * 0.72; scene.add(horn);
    ctx.label('微波號角', [5.3, 3.0, 0.6], 'small');
    const waves = [0, 1, 2].map(() => { const w = new THREE.Mesh(new THREE.TorusGeometry(1, 0.025, 6, 48), U.glow(0xe0a54a, 0.0)); w.position.set(5.3, 2.4, 0.4); scene.add(w); return w; });

    /* ---- 狀態與閘 ---- */
    const bloch = (s) => { const [ar, ai, br, bi] = s; return [2 * (ar * br + ai * bi), 2 * (ar * bi - ai * br), ar * ar + ai * ai - br * br - bi * bi]; };
    const RX = (th, s) => { const c = Math.cos(th / 2), sn = Math.sin(th / 2); const [ar, ai, br, bi] = s; return [c * ar + sn * bi, c * ai - sn * br, c * br + sn * ai, c * bi - sn * ar]; };
    const RZ = (ph, s) => { const c = Math.cos(ph / 2), sn = Math.sin(ph / 2); const [ar, ai, br, bi] = s; return [c * ar + sn * ai, c * ai - sn * ar, c * br - sn * bi, c * bi + sn * br]; };
    const queue = []; let cur = null, log = [];
    const push = (op) => queue.push(op);
    let selMode = 'row';
    const applySel = () => atoms.forEach((a) => {
      a.sel = selMode === 'row' ? a.j === 1 : selMode === 'col' ? a.i === 2 : selMode === 'diag' ? a.i === a.j : a.i === 1 && a.j === 2;
      a.ring.visible = a.sel;
    });

    const r1 = ui.row();
    ui.button('全域微波 π/2', () => push({ type: 'RX', th: Math.PI / 2, all: true, name: 'X(π/2) 全域' }), r1);
    ui.button('全域 π', () => push({ type: 'RX', th: Math.PI, all: true, name: 'X(π) 全域' }), r1);
    const r2 = ui.row();
    ui.button('局部定址 Z(π)（選中的原子）', () => push({ type: 'RZ', th: Math.PI, all: false, name: 'Z(π) 局部' }), r2);
    const r3 = ui.row();
    ui.button('示範：只翻轉未定址的原子', () => { [{ type: 'RX', th: Math.PI / 2, all: true, name: 'X(π/2) 全域' }, { type: 'RZ', th: Math.PI, all: false, name: 'Z(π) 局部' }, { type: 'RX', th: Math.PI / 2, all: true, name: 'X(π/2) 全域' }].forEach(push); }, r3);
    ui.button('重置', () => { queue.length = 0; cur = null; log = []; atoms.forEach((a) => { a.s = [1, 0, 0, 0]; a.beam.visible = false; }); }, r3);
    ui.radio([['row', '選第 2 列'], ['col', '選第 3 欄'], ['diag', '選對角線'], ['one', '選單顆']], 'row', (v) => { selMode = v; applySel(); });
    const ro = ui.readout();
    applySel();

    ctx.inset('每顆原子的 P(|1⟩)（4×4）', (g, W, H, P) => {
      const cs = 42, x0 = 30, y0 = 18;
      atoms.forEach((a) => {
        const p1 = (1 - bloch(a.s)[2]) / 2;
        const c = new THREE.Color(QC.q0).lerp(new THREE.Color(QC.q1), p1);
        g.fillStyle = '#' + c.getHexString(); g.fillRect(x0 + a.i * cs, y0 + a.j * cs, cs - 4, cs - 4);
        if (a.sel) { g.strokeStyle = '#ff4fd8'; g.lineWidth = 2; g.strokeRect(x0 + a.i * cs, y0 + a.j * cs, cs - 4, cs - 4); }
        P.text(g, p1.toFixed(2), x0 + a.i * cs + (cs - 4) / 2, y0 + a.j * cs + cs / 2 + 2, '#fff', 'center');
      });
      P.text(g, '藍 = |0⟩', 220, 40, '#a9c6ff'); P.text(g, '紅 = |1⟩', 220, 60, '#ffb0b2'); P.text(g, '洋紅框 = 被定址', 220, 80, '#ff8ae8');
      P.text(g, '依序：', 220, 120, '#9fb0c8');
      log.slice(-4).forEach((s, k) => P.text(g, `${k + 1 + Math.max(0, log.length - 4)}. ${s}`, 220, 140 + k * 18, '#ffd28a'));
    });

    const colorOf = (z) => new THREE.Color(QC.q0).lerp(new THREE.Color(QC.q1), (1 - z) / 2);
    return {
      update(t, dt) {
        if (!cur && queue.length) {
          cur = queue.shift(); cur.u = 0; atoms.forEach((a) => (a.start = a.s.slice()));
          log.push(cur.name);
        }
        if (cur) {
          cur.u = Math.min(1, cur.u + dt / 1.4);
          atoms.forEach((a) => {
            if (cur.all || a.sel) a.s = cur.type === 'RX' ? RX(cur.th * cur.u, a.start) : RZ(cur.th * cur.u, a.start);
            a.beam.visible = !cur.all && a.sel;
            if (a.beam.visible) a.beam.material.opacity = 0.3 + 0.3 * Math.sin(t * 12);
          });
          waves.forEach((w, k) => { if (cur.all) { const ph = (t * 1.2 + k / 3) % 1; w.scale.setScalar(0.5 + ph * 4); w.material.opacity = 0.5 * (1 - ph); } else w.material.opacity = 0; });
          mwArrow.scale.setScalar(cur.all ? 1 + 0.08 * Math.sin(t * 10) : 1);
          if (cur.u >= 1) { cur = null; atoms.forEach((a) => (a.beam.visible = false)); waves.forEach((w) => (w.material.opacity = 0)); }
        }
        atoms.forEach((a) => {
          const [x, y, z] = bloch(a.s); const c = colorOf(z);
          a.pt.setColor(c.getHex()); a.ar.children.forEach((m) => { m.material.color.copy(c); m.material.emissive.copy(c); });
          a.ar.setVec(new THREE.Vector3(x, z, -y).multiplyScalar(0.42));
        });
        const sel = atoms.filter((a) => a.sel), uns = atoms.filter((a) => !a.sel);
        const avg = (arr) => arr.reduce((s, a) => s + (1 - bloch(a.s)[2]) / 2, 0) / Math.max(1, arr.length);
        ro.innerHTML = `${cur ? `<b>執行中：${cur.name}</b>` : queue.length ? '等待中…' : '就緒'}<br>被定址原子 P(|1⟩) ≈ ${avg(sel).toFixed(2)} · 其他原子 P(|1⟩) ≈ ${avg(uns).toFixed(2)}`;
      },
    };
  },
});

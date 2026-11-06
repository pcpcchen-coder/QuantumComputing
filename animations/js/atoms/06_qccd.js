/* 離子阱場景 6：QCCD 搬運架構 — 分段表面電極阱、分區、X 接面、共冷離子、搬運/分離/合併/閘/偵測 */
App.register({
  id: 'qccd', num: 6, short: 'QCCD 搬運架構',
  title: 'QCCD：把離子搬到需要的地方',
  subtitle: '一條長鏈做不大，就把晶片分成記憶區、閘區、偵測區，用 DC 電壓波形把離子搬來搬去',
  desc: `<p><b>QCCD（量子電荷耦合元件）</b>：表面電極阱晶片上有兩條 RF 軌道形成「隧道」，旁邊上百片<b>分段 DC 電極</b>。依序改變電極電壓，位能井就像輸送帶一樣把離子往前推。</p>
<p><b>基本操作</b>：<b>搬運</b>（transport）、<b>分離 / 合併</b>（split / merge 一個位能井裡的離子）、<b>接面轉向</b>（X / Y 接面）、必要時<b>交換順序</b>。每個量子位元離子旁邊配一顆<b>共冷離子</b>：搬運會加熱離子，用另一種元素冷卻（雷射不會碰到量子位元），再做下一個閘。</p>
<p><b>實例</b>：Quantinuum H2（56 位元，跑道型阱）；<b>Helios</b>（2025，98 位元，¹³⁷Ba⁺ 量子位元 + ¹⁷¹Yb⁺ 共冷，環形儲存區 + X 接面）。IonQ 收購 Oxford Ionics，走 2D 晶片阱 + 電子式量子位元控制路線。</p>
<p><b>代價</b>：搬運、分離合併與重新冷卻常佔一層線路的大部分時間（右下插圖，代表值）。</p>
<p><b>另一條擴展路線</b>：<b>光子互連</b> —— 兩個模組各讓一顆離子發出與自旋糾纏的光子，在分光鏡上做貝爾量測，兩顆遠端離子就糾纏了。</p>`,
  camera: { pos: [0.6, 7.2, 8.6], target: [-0.2, 0, 0.2] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const Y = 0.3; // 離子高度（示意；實際約 50–100 μm）
    scene.add(U.box(13.5, 0.12, 7.0, U.mat(0x2a3140, { roughness: 0.6, metalness: 0.4 }), -0.4, -0.06, 0));
    const rail = U.metal(0xd9a441, { roughness: 0.3 });
    [-0.22, 0.22].forEach((z) => { scene.add(U.box(11.6, 0.03, 0.14, rail, -0.45, 0.015, z)); });
    [-0.22, 0.22].forEach((x) => { scene.add(U.box(0.14, 0.03, 5.8, rail, 3 + x, 0.016, 0)); });
    const JX = 3;
    /* 分段 DC 電極 */
    const elecs = [];
    const emat = () => U.mat(0x8a93a0, { metalness: 0.6, roughness: 0.35, emissive: 0x000000 });
    for (let x = -6.0; x <= 5.2; x += 0.4) {
      if (Math.abs(x - JX) < 0.65) continue;
      [-0.62, 0.62].forEach((z) => { const m = U.box(0.32, 0.03, 0.42, emat(), x, 0.015, z); scene.add(m); elecs.push(m); });
    }
    for (let z = -2.8; z <= 2.8; z += 0.4) {
      if (Math.abs(z) < 0.65) continue;
      [-0.62, 0.62].forEach((dx) => { const m = U.box(0.42, 0.03, 0.32, emat(), JX + dx, 0.015, z); scene.add(m); elecs.push(m); });
    }
    /* 分區 */
    const zone = (x0, x1, z0, z1, col, name, lp) => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, z1 - z0), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.16, depthWrite: false }));
      m.rotation.x = -Math.PI / 2; m.position.set((x0 + x1) / 2, 0.035, (z0 + z1) / 2); scene.add(m);
      ctx.label(name, lp, 'small');
    };
    zone(-6.2, -4.7, -0.95, 0.95, 0x7a8699, '載入區', [-5.45, 0.2, -1.35]);
    zone(-4.5, -1.1, -0.95, 0.95, 0x4f8cff, '記憶區', [-2.8, 0.2, -1.35]);
    zone(-0.8, 1.4, -0.95, 0.95, 0x7ee05a, '閘區（雷射）', [0.3, 0.2, -1.35]);
    zone(2.05, 3.95, 1.2, 2.9, 0xb46cff, '偵測區', [4.35, 0.2, 2.1]);
    zone(2.05, 3.95, -2.9, -1.2, 0x4f8cff, '儲存區', [4.35, 0.2, -2.1]);
    ctx.label('X 接面', [JX + 0.85, 0.2, -0.75], 'small');
    ctx.label('RF 軌道（金）+ 分段 DC 電極（灰）', [-4.6, 0.2, 1.45], 'small');
    /* 離子對：量子位元 ¹³⁷Ba⁺（金）+ 共冷 ¹⁷¹Yb⁺（紫） */
    const START = { q0: -4.0, q2: -3.2, q1: -2.4, q3: -1.6 };
    const pairs = {};
    Object.entries(START).forEach(([name, x]) => {
      const q = App.particle(scene, App.QC.ion, 0.085), c = App.particle(scene, App.QC.cool, 0.075);
      const L = ctx.labelOn(q, name, [0, 0.32, 0], 'gold');
      pairs[name] = { q, c, L, p: new THREE.Vector3(x, Y, 0), path: null, moving: false, glowQ: 0.4, glowC: 0.3 };
    });
    ctx.label('<span style="color:#ffc04a">●</span> 量子位元 ¹³⁷Ba⁺　<span style="color:#9b7bff">●</span> 共冷 ¹⁷¹Yb⁺', [-2.8, 0.2, 1.85], 'small');
    const ent = U.dynLine(2, 0xffd28a); scene.add(ent.obj); ent.obj.visible = false;
    const lbEnt = ctx.label('糾纏', [0, 0, 0], 'gold'); lbEnt.show(false);
    /* 雷射 */
    const G = new THREE.Vector3(0.25, Y, 0);
    const gate1 = App.beam(scene, [-1.6, 2.2, 2.2], G, 0x7ee05a, 0.05, 0.65);
    const gate2 = App.beam(scene, [2.1, 2.2, 2.2], G, 0x7ee05a, 0.05, 0.65);
    const coolB = App.beam(scene, [-1.4, Y, 2.6], [2.0, Y, -2.6], App.wlColor(369), 0.04, 0.55);
    const detB = App.beam(scene, [1.6, Y, 2.0], [4.6, Y, 2.0], App.wlColor(493), 0.04, 0.6);
    [gate1, gate2, coolB, detB].forEach((b) => b.on(false));
    const ph = App.photons(scene, App.wlColor(493), 80, { size: 0.03 });

    /* 路徑工具 */
    const setPath = (name, pts, dur) => {
      const P = pts.map((p) => new THREE.Vector3(p[0], Y, p[1]));
      const lens = [0]; for (let i = 1; i < P.length; i++) lens.push(lens[i - 1] + P[i].distanceTo(P[i - 1]));
      pairs[name].path = { P, lens, total: lens[lens.length - 1] || 1 };
    };
    const along = (path, k) => {
      const s = U.smooth(k) * path.total;
      for (let i = 1; i < path.P.length; i++) if (s <= path.lens[i] + 1e-9) return path.P[i - 1].clone().lerp(path.P[i], (s - path.lens[i - 1]) / ((path.lens[i] - path.lens[i - 1]) || 1));
      return path.P[path.P.length - 1].clone();
    };
    const pos2 = (n) => [pairs[n].p.x, pairs[n].p.z];
    let measured = null;
    const STEPS = [
      { name: '① 分離並搬運 q1、q3 到閘區', dur: 2.5, cat: 0, start() { setPath('q1', [pos2('q1'), [0.0, 0]]); setPath('q3', [pos2('q3'), [0.5, 0]]); } },
      { name: '② 合併：兩對離子進同一個位能井', dur: 1.2, cat: 0, start() { setPath('q1', [pos2('q1'), [0.08, 0]]); setPath('q3', [pos2('q3'), [0.42, 0]]); } },
      { name: '③ 共冷：冷卻 Yb⁺，透過庫侖力帶走 Ba⁺ 的熱', dur: 1.5, cat: 1, start() { coolB.on(true); }, end() { coolB.on(false); } },
      { name: '④ 兩位元閘：閘雷射同時照兩顆量子位元離子', dur: 1.8, cat: 3, start() { gate1.on(true); gate2.on(true); }, end() { gate1.on(false); gate2.on(false); ent.obj.visible = true; lbEnt.show(true); } },
      { name: '⑤ 分離，q3 經 X 接面轉向偵測區', dur: 3.0, cat: 0, start() { setPath('q3', [pos2('q3'), [JX, 0], [JX, 2.05]]); } },
      { name: '⑥ 偵測：螢光讀出 q3（其他離子不受影響）', dur: 1.8, cat: 2, start() { detB.on(true); measured = Math.random() < 0.5 ? 1 : 0; }, end() { detB.on(false); ent.obj.visible = false; lbEnt.show(false); } },
      { name: '⑦ 搬回記憶區，準備下一層', dur: 3.0, cat: 0, start() { setPath('q3', [pos2('q3'), [JX, 0], [-1.6, 0]]); setPath('q1', [pos2('q1'), [-2.4, 0]]); } },
    ];
    let step = -1, t = 0, auto = false, active = false;
    const resetAll = () => {
      Object.entries(START).forEach(([n, x]) => { pairs[n].p.set(x, Y, 0); pairs[n].path = null; });
      [gate1, gate2, coolB, detB].forEach((b) => b.on(false)); ent.obj.visible = false; lbEnt.show(false); measured = null; step = -1; active = false;
    };
    const begin = (i) => { step = i; t = 0; active = true; Object.values(pairs).forEach((p) => (p.path = null)); STEPS[i].start(); };
    ui.button('▶ 執行一段線路', () => { resetAll(); auto = true; begin(0); });
    ui.button('單步', () => { if (active) return; auto = false; if (step >= STEPS.length - 1) resetAll(); begin(step + 1); });
    let showV = true;
    ui.toggle('顯示 DC 電極電壓', true, (on) => { showV = on; });
    const ro = ui.readout();
    const CAT = [['搬運 + 分離 / 合併', 400], ['共冷（重新冷卻）', 300], ['偵測', 150], ['兩位元閘', 50], ['單位元閘', 10]];
    ctx.inset('一層線路的時間組成（示意，代表值 μs）', (g, W, H, P) => {
      const c = active ? STEPS[step].cat : -1;
      App.bars(g, W, H, P, CAT.map(([n, v], i) => [n, v, i === c ? '#ffd28a' : '#5f7fb0']), { l: 130, max: 480, fmt: (v) => '~' + v + ' μs', footer: '搬運與冷卻常佔大部分時間' });
    });
    return {
      update(time, dt) {
        if (active) {
          const S = STEPS[step]; t += dt; const k = Math.min(1, t / S.dur);
          Object.values(pairs).forEach((p) => { if (p.path) p.p.copy(along(p.path, k)); });
          if (S.cat === 2 && measured === 1) for (let i = 0; i < 3; i++) ph.emit(pairs.q3.p, Math.random() < 0.6 ? [U.gauss() * 0.15, 1, U.gauss() * 0.15] : null, 2.5, 0.5);
          if (k >= 1) {
            S.end && S.end(); Object.values(pairs).forEach((p) => (p.path = null)); active = false;
            if (auto && step < STEPS.length - 1) begin(step + 1); else auto = false;
          }
        }
        ph.update(dt);
        const cur = active ? STEPS[step] : null;
        Object.entries(pairs).forEach(([n, pr]) => {
          const onBranch = Math.abs(pr.p.x - JX) < 0.05 && Math.abs(pr.p.z) > 0.05;
          const off = onBranch ? new THREE.Vector3(0, 0, 0.17) : new THREE.Vector3(0.17, 0, 0);
          pr.q.position.copy(pr.p).addScaledVector(off, -0.5); pr.c.position.copy(pr.p).addScaledVector(off, 0.5);
          let gq = 0.35, gc = 0.3;
          if (cur && cur.cat === 1 && (n === 'q1' || n === 'q3')) gc = 0.9 + 0.1 * Math.sin(time * 20);
          if (cur && cur.cat === 3 && (n === 'q1' || n === 'q3')) gq = 1;
          if (cur && cur.cat === 2 && n === 'q3') gq = measured ? 1 : 0.1;
          pr.q.glow(gq); pr.c.glow(gc);
          pr.moving = !!pr.path;
        });
        if (ent.obj.visible) {
          ent.set([pairs.q1.q.position.toArray(), pairs.q3.q.position.toArray()]);
          lbEnt.pos.copy(pairs.q1.q.position).lerp(pairs.q3.q.position, 0.5).add(new THREE.Vector3(0, 0.35, 0));
        }
        // DC 電極：靠近移動中離子的電極亮起（示意電壓波形形成的位能井）
        elecs.forEach((m) => {
          let s = 0;
          if (showV) Object.values(pairs).forEach((pr) => { if (!pr.moving) return; const d2 = (m.position.x - pr.p.x) ** 2 + (m.position.z - pr.p.z) ** 2; s += Math.exp(-d2 / 0.18); });
          m.material.emissive.setRGB(0.9 * Math.min(1, s), 0.45 * Math.min(1, s), 0);
        });
        ro.innerHTML = cur ? `<b>${cur.name}</b><br>步驟 ${step + 1} / ${STEPS.length}` + (cur.cat === 2 ? `<br>量測結果：q3 = <b>${measured}</b>（${measured ? '亮' : '暗'}）` : '')
          : step >= STEPS.length - 1 ? '這一層線路完成。按「▶ 執行一段線路」重播，或「單步」逐步看。' : '按「▶ 執行一段線路」或「單步」。';
      },
    };
  },
});

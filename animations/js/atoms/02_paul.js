/* 離子阱場景 2：Paul 阱原理 — 旋轉鞍形位勢、Mathieu 方程軌跡、線性阱 */
App.register({
  id: 'paul', num: 2, short: 'Paul 阱原理',
  title: 'Paul 阱：用振盪電場抓住離子',
  subtitle: '靜電場抓不住電荷（Earnshaw 定理），讓鞍形位勢快速翻轉，平均起來就變成一個碗',
  desc: `<p><b>Earnshaw 定理</b>：靜電位勢滿足 ∇²φ = 0，不可能在三個方向同時是極小值 —— 只靠固定電壓無法把離子關住。</p>
<p><b>解法</b>：在電極加上射頻（RF）電壓，位勢變成 <span class="eq">φ ∝ (x² − y²) cos Ωt</span> 的鞍形，而且每秒翻轉數千萬次。離子在某個方向剛要滑出去，位勢就翻過來把它推回。平均效果是一個指向中心的<b>擬位勢（ponderomotive pseudopotential）</b>。</p>
<p><b>Mathieu 方程</b>：<span class="eq">ẍ = −(a − 2q cos 2τ) x</span>，τ = Ωt/2。當 a = 0、<b>q &lt; 0.908</b> 時穩定。運動 = 大而慢的 <b>secular 振盪</b>（頻率 ≈ qΩ/(2√2)）+ 小而快的 <b>micromotion</b>（RF 頻率）。</p>
<p><b>實際系統</b>（代表值）：Ω/2π ≈ 20–50 MHz、RF 振幅 100–300 V、徑向 secular 頻率 2–5 MHz、軸向 0.5–2 MHz（由兩端 DC 電極決定）。<b>線性阱</b>用 4 根桿（右）；<b>表面電極阱</b>把電極「攤平」在晶片上，離子浮在表面上方約 50–100 μm，可用半導體製程大量製作。</p>
<p>拖動 q 看穩定 ↔ 不穩定；關掉 RF 看離子逃走。</p>`,
  camera: { pos: [0.3, 5.2, 9.6], target: [0.3, 0.6, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    /* ---------- 左：旋轉鞍形 ---------- */
    const L0 = new THREE.Vector3(-2.7, 0.6, 0);
    const N = 40, S = 3.2;
    const geo = new THREE.PlaneGeometry(S, S, N, N); geo.rotateX(-Math.PI / 2);
    const base = geo.attributes.position.array.slice();
    const surf = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0x3b6fd8, transparent: true, opacity: 0.55, side: THREE.DoubleSide, roughness: 0.4, metalness: 0.1 }));
    const wire = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0x8ec5ff, wireframe: true, transparent: true, opacity: 0.25 }));
    surf.position.copy(L0); wire.position.copy(L0); scene.add(surf, wire);
    const ball = App.particle(scene, App.QC.ion, 0.09);
    const trail = U.dynLine(400, 0xffd28a, 0.8); scene.add(trail.obj);
    ctx.label('旋轉鞍形位勢 φ ∝ (x² − y²) cos Ωt', [L0.x, 2.25, 0], 'gold');
    const lbStat = ctx.label('', [L0.x, -0.9, 1.4], 'teal');
    /* 四個電極（示意：雙曲面電極的截面方塊） */
    const elec = [];
    [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([sx, sz], k) => {
      const m = U.box(0.35, 0.5, 0.35, U.metal(k < 2 ? 0xd9a441 : 0x8a93a0), L0.x + sx * 2.0, L0.y, L0.z + sz * 2.0);
      scene.add(m); elec.push(m);
    });
    /* ---------- 右：線性阱 ---------- */
    const R0 = new THREE.Vector3(3.1, 0.6, 0);
    const rodR = 0.42;
    const rods = [];
    [[1, 1], [-1, -1], [1, -1], [-1, 1]].forEach(([a, b], k) => {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 3.2, 20), U.metal(k < 2 ? 0xd9a441 : 0x8a93a0));
      m.rotation.z = Math.PI / 2; m.position.set(R0.x, R0.y + a * rodR, R0.z + b * rodR); scene.add(m); rods.push(m);
    });
    [-1, 1].forEach((s) => {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.06, 10, 32), U.metal(0x5fb0ff)); ring.rotation.y = Math.PI / 2; ring.position.set(R0.x + s * 1.75, R0.y, R0.z); scene.add(ring);
    });
    const ions = [];
    for (let i = 0; i < 5; i++) ions.push(App.particle(scene, App.QC.ion, 0.06, [R0.x + (i - 2) * 0.32, R0.y, R0.z]));
    ctx.label('線性 Paul 阱', [R0.x, 1.85, 0], 'gold');
    ctx.label('RF 桿（對角一組）', [R0.x - 1.2, 1.25, 0.6], 'small');
    ctx.label('接地桿', [R0.x + 1.0, 0.0, 0.9], 'small');
    ctx.label('端蓋 DC（軸向囚禁）', [R0.x + 1.75, -0.05, 0], 'small');
    ctx.label('離子鏈', [R0.x, 0.25, 0.6], 'small');

    /* ---------- 物理：Mathieu 方程（a = 0） ---------- */
    let q = 0.4, rf = true, OmegaMHz = 30;
    const st = { x: 0.55, vx: 0, y: 0.35, vy: 0.05, tau: 0, escaped: 0 };
    const hist = [];
    const reset = () => { Object.assign(st, { x: 0.55, vx: 0, y: 0.35, vy: 0.05, tau: 0, escaped: 0 }); hist.length = 0; };
    const acc = (x, tau, sgn) => (rf ? sgn * 2 * q * Math.cos(2 * tau) * x : 0);
    const stepRK = (h) => {
      const f = (s, t) => [s[1], acc(s[0], t, 1), s[3], acc(s[2], t, -1)];
      const s0 = [st.x, st.vx, st.y, st.vy];
      const k1 = f(s0, st.tau);
      const k2 = f(s0.map((v, i) => v + (h / 2) * k1[i]), st.tau + h / 2);
      const k3 = f(s0.map((v, i) => v + (h / 2) * k2[i]), st.tau + h / 2);
      const k4 = f(s0.map((v, i) => v + h * k3[i]), st.tau + h);
      const s1 = s0.map((v, i) => v + (h / 6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
      [st.x, st.vx, st.y, st.vy] = s1; st.tau += h;
    };
    /* 插圖用：完整 x(τ) 軌跡 */
    let curve = [];
    const computeCurve = () => {
      curve = []; let x = 0.55, v = 0, t = 0; const h = 0.02;
      const a = (xx, tt) => (rf ? 2 * q * Math.cos(2 * tt) * xx : 0);
      for (let i = 0; i < 3000; i++) {
        const k1x = v, k1v = a(x, t);
        const k2x = v + (h / 2) * k1v, k2v = a(x + (h / 2) * k1x, t + h / 2);
        const k3x = v + (h / 2) * k2v, k3v = a(x + (h / 2) * k2x, t + h / 2);
        const k4x = v + h * k3v, k4v = a(x + h * k3x, t + h);
        x += (h / 6) * (k1x + 2 * k2x + 2 * k3x + k4x); v += (h / 6) * (k1v + 2 * k2v + 2 * k3v + k4v); t += h;
        if (i % 5 === 0) curve.push([t, x]);
        if (Math.abs(x) > 5) break;
      }
    };
    const stable = () => rf && q < 0.908;
    const ro = ui.readout();
    const info = () => {
      const fsec = (q * OmegaMHz) / (2 * Math.SQRT2);
      ro.innerHTML = `q = ${q.toFixed(2)}（a = 0）　RF ${rf ? '開' : '<b style="color:#ff8a8a">關</b>'}<br>`
        + (stable() ? `<b style="color:#8ef0a0">穩定</b>：secular 頻率 ≈ qΩ/(2√2) = ${fsec.toFixed(2)} MHz（Ω/2π = ${OmegaMHz} MHz）<br>micromotion 頻率 = Ω/2π = ${OmegaMHz} MHz`
          : `<b style="color:#ff8a8a">不穩定</b>：${rf ? 'q > 0.908，離子每個週期被推得更遠' : '沒有 RF，鞍形位勢消失，離子直接逃走'}`);
      lbStat.set(stable() ? '穩定：被困住' : '不穩定：逃逸');
      computeCurve();
    };
    ui.slider('q 參數', 0.1, 1.0, 0.01, q, (v) => { q = v; reset(); info(); }, (v) => v.toFixed(2));
    ui.toggle('RF 開 / 關', true, (on) => { rf = on; reset(); info(); });
    ui.slider('RF 頻率 Ω/2π (MHz)', 10, 60, 1, OmegaMHz, (v) => { OmegaMHz = v; info(); }, (v) => v + ' MHz');
    ui.button('重設離子位置', () => reset());
    info();
    ctx.inset('x(τ)：secular 大振盪 + micromotion 小抖動', (g, W, H, P) => {
      const tmax = curve.length ? curve[curve.length - 1][0] : 60;
      const { X, Y } = P.frame(g, W, H, [0, Math.min(60, tmax)], [-1.6, 1.6], { xlabel: 'τ = Ωt/2', ylabel: 'x', xticks: [[0, '0'], [20, '20'], [40, '40'], [60, '60']], yticks: [[-1, '−1'], [0, '0'], [1, '1']], m: { l: 34 } });
      g.save(); g.beginPath(); g.rect(34, 0, W - 34, H - 30); g.clip();
      P.curve(g, (t) => { let k = Math.min(curve.length - 1, Math.max(0, Math.round((t / (tmax || 1)) * (curve.length - 1)))); return curve.length ? curve[k][1] : 0; }, 0, Math.min(60, tmax), X, Y, '#ffd28a', 1.6, 600);
      g.restore();
      if (stable()) { P.text(g, '慢：secular', X(12), Y(1.35), '#8ef0ff'); P.text(g, '快：micromotion', X(34), Y(-1.35), '#c9b4ff'); }
      else P.text(g, '振幅發散 → 逃逸', X(20), Y(1.3), '#ff8a8a');
    });

    return {
      update(time, dt) {
        // 動畫時間尺度：τ 每秒前進 4（RF 週期 ≈ 0.8 s，看得見翻轉）
        const steps = 12, h = (4 * dt) / steps;
        for (let i = 0; i < steps; i++) stepRK(h);
        const amp = rf ? 0.32 * (q / 0.4) : 0;
        const c = Math.cos(2 * st.tau);
        // 更新鞍形曲面（y 方向為「位能高度」）
        const pos = geo.attributes.position.array;
        for (let i = 0; i < pos.length; i += 3) {
          const x = base[i] / (S / 2), z = base[i + 2] / (S / 2);
          pos[i + 1] = amp * (x * x - z * z) * c;
        }
        geo.attributes.position.needsUpdate = true; geo.computeVertexNormals();
        elec[0].material.emissive.setHex(c > 0 ? 0x553300 : 0x000000);
        rods[0].material.emissive.setHex(c > 0 ? 0x553300 : 0x000000);
        // 離子位置
        let x = st.x, z = st.y;
        if (Math.abs(x) > 1.55 || Math.abs(z) > 1.55) { st.escaped += dt; if (st.escaped > 1.2) reset(); }
        x = U.clamp(x, -3, 3); z = U.clamp(z, -3, 3);
        const hx = (x * 2) / S, hz = (z * 2) / S;
        ball.position.set(L0.x + x, L0.y + amp * (hx * hx - hz * hz) * c + 0.1, L0.z + z);
        ball.visible = Math.abs(x) < 2.6 && Math.abs(z) < 2.6;
        if (ball.visible && Math.abs(x) < 1.7 && Math.abs(z) < 1.7) { hist.push([ball.position.x, ball.position.y, ball.position.z]); if (hist.length > 400) hist.shift(); }
        trail.set(hist);
        // 線性阱中的離子：micromotion 小抖動
        ions.forEach((p, i) => {
          const j = rf ? 0.015 * Math.cos(2 * st.tau) : 0;
          const drift = rf ? 0 : Math.min(1.5, (time % 4) * 0.4) * (i % 2 ? 1 : -1);
          p.position.set(R0.x + (i - 2) * 0.32, R0.y + j + drift * 0.6, R0.z + j * 0.7);
          p.glow(0.6);
        });
      },
    };
  },
});

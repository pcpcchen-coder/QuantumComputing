/* 原子場景 16：螢光成像讀取 — 推出 |1⟩ → 成像 → 相機影像 → 閾值判別 */
App.register({
  id: 'imaging', num: 15, short: '螢光成像讀取',
  title: '讀取：推出 |1⟩，再拍一張螢光照片',
  subtitle: '有亮點 = |0⟩、沒亮點 = |1⟩；一次拍下整個陣列，但需要毫秒級曝光',
  desc: `<p><b>標準做法（破壞性）</b>：<br>① <b>推出（push-out）</b>：用與 |1⟩（F=2）共振的光把 |1⟩ 的原子推出光鑷，|0⟩（F=1）不受影響。<br>
② <b>成像</b>：開 780 nm 冷卻光，留下的原子不斷散射光子；高 NA 物鏡收集約 1–5 % 的光子，送到 sCMOS / EMCCD 相機。<br>
③ 每個光鑷位置的像素光子數超過閾值 → 判為「有原子」= |0⟩。</p>
<p>曝光約 1–20 ms；保真度 > 99 %（Caltech 2025：成像保真度 > 99.99 %、成像後存活率 99.99 %）。</p>
<p><b>限制</b>：量測後原子被打掉或加熱，必須補充新原子；成像時其他原子也可能被干擾。<b>原子損失</b>會被讀成「沒有亮點」→ 誤判為 |1⟩。</p>
<p><b>其他做法</b>：<b>非破壞讀取</b>（只讓 |1⟩ 在循環躍遷上發光，原子留在光鑷中）；<b>雙原子種類</b>（例如 Rb 當資料位元、Cs 當輔助位元，讀取光互不干擾）；把要量測的原子<b>搬到讀取區</b>（場景 14）。</p>`,
  camera: { pos: [1.6, 5.6, 7.8], target: [1.1, 0.6, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const QC = App.QC;
    const N = 5, sp = 0.6;
    const atoms = [];
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
      const P = new THREE.Vector3(-1.6 + (i - 2) * sp, 0, (j - 2) * sp);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.01, 6, 20), U.glow(0x55617a, 0.6)); ring.rotation.x = Math.PI / 2; ring.position.copy(P).add(new THREE.Vector3(0, -0.05, 0)); scene.add(ring);
      const pt = App.particle(scene, QC.q0, 0.09, P.toArray());
      atoms.push({ i, j, P, pt, state: 0, present: true, flyV: null, count: 0, lost: false });
    }
    ctx.label('5×5 原子陣列（光鑷）', [-1.6, -0.35, 1.9], 'teal');
    // 物鏡（上方）
    const obj = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.95, 1.0, 32), U.metal(0x2a2f38, { roughness: 0.4 })); obj.position.set(-1.6, 2.3, 0); scene.add(obj);
    ctx.label('高 NA 物鏡', [-3.0, 2.4, 0], 'small');
    const collect = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 1.5, 1.7, 32, 1, true), new THREE.MeshBasicMaterial({ color: 0xff6060, transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending }));
    collect.position.set(-1.6, 0.95, 0); scene.add(collect);
    // 成像光路 → 相機
    const path = App.beam(scene, [-1.6, 2.8, 0], [-1.6, 3.2, 0], 0xff6060, 0.05, 0.3);
    const path2 = App.beam(scene, [-1.6, 3.2, 0], [3.0, 3.2, 0], 0xff6060, 0.05, 0.3);
    const camBox = U.box(0.6, 0.5, 0.5, U.mat(0x2b3446, { metalness: 0.4 }), 3.3, 3.2, 0); scene.add(camBox);
    ctx.label('sCMOS / EMCCD 相機', [4.6, 3.2, 0], 'small');
    // 相機影像平面
    const cv = document.createElement('canvas'); cv.width = 200; cv.height = 200;
    const g2 = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv); tex.magFilter = THREE.NearestFilter; tex.minFilter = THREE.NearestFilter;
    const img = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 2.6), new THREE.MeshBasicMaterial({ map: tex }));
    img.position.set(3.4, 1.4, 0.4); img.rotation.set(-0.35, -0.15, 0); scene.add(img);
    const frame = new THREE.Mesh(new THREE.PlaneGeometry(2.75, 2.75), U.mat(0x3a4250)); frame.position.copy(img.position).add(new THREE.Vector3(0, 0, -0.02)); frame.rotation.copy(img.rotation); scene.add(frame);
    const imgL = ctx.label('相機影像（示意）', [3.4, -0.15, 0.95], 'gold');
    // 推出光束（共振光，從側面掃過）
    const push = App.beam(scene, [-4.6, 0.05, 0], [1.2, 0.05, 0], 0xff8a3d, 0.55, 0.0);
    const ph = App.photons(scene, 0xff6060, 200, { size: 0.025 });

    let expo = 10, nondes = false, phase = 'ready', tP = 0, msg = '按「準備隨機態」';
    const bright = () => 3.0 * expo, dark = () => 0.12 * expo + 0.6;
    const pois = (lam, k) => Math.exp(-lam + k * Math.log(lam) - lgam(k + 1));
    const LG = [0, 0]; for (let k = 2; k < 600; k++) LG.push(LG[k - 1] + Math.log(k - 1));
    const lgam = (n) => LG[Math.min(n, 599)];
    const cdf = (lam, k) => { let s = 0; for (let i = 0; i < k; i++) s += pois(lam, i); return s; };
    const SC = {};
    const stats = () => SC[expo] || (SC[expo] = statsCalc());
    const statsCalc = () => {
      const b = bright(), d = dark(); let best = 1, bf = 0;
      for (let th = 1; th < b + 3; th++) { const f = 1 - ((1 - cdf(d, th)) + cdf(b, th)) / 2; if (f > bf) { bf = f; best = th; } }
      return { thr: best, F: bf, b, d };
    };
    function drawImage(show) {
      g2.fillStyle = '#000'; g2.fillRect(0, 0, 200, 200);
      const im = g2.createImageData(40, 40);
      const s = stats();
      const val = new Float32Array(1600);
      for (let k = 0; k < 1600; k++) val[k] = App.poisson(0.004 * expo + 0.04);
      if (show) atoms.forEach((a) => {
        const cx = 4 + a.i * 8, cy = 4 + a.j * 8;
        const tot = a.count; // 分配到 3×3 像素（高斯權重）
        const w = [[1, 2, 1], [2, 4, 2], [1, 2, 1]];
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) val[(cy + dy) * 40 + cx + dx] += (tot * w[dy + 1][dx + 1]) / 16;
      });
      const mx = Math.max(3, s.b / 5);
      for (let k = 0; k < 1600; k++) { const v = Math.min(255, (val[k] / mx) * 255); im.data[4 * k] = v * 0.55; im.data[4 * k + 1] = v * 0.95; im.data[4 * k + 2] = v; im.data[4 * k + 3] = 255; }
      const c2 = document.createElement('canvas'); c2.width = 40; c2.height = 40; c2.getContext('2d').putImageData(im, 0, 0);
      g2.imageSmoothingEnabled = false; g2.drawImage(c2, 0, 0, 200, 200);
      if (show) atoms.forEach((a) => { const call = a.count >= s.thr; g2.strokeStyle = call ? 'rgba(94,224,138,.9)' : 'rgba(255,90,95,.6)'; g2.lineWidth = 1.5; g2.strokeRect(a.i * 40 + 3, a.j * 40 + 3, 34, 34); });
      tex.needsUpdate = true;
    }
    function reset() {
      atoms.forEach((a) => { a.present = true; a.flyV = null; a.pt.position.copy(a.P); a.pt.visible = true; a.pt.scale.setScalar(1); a.state = 0; a.count = 0; a.lost = false; a.pt.setColor(QC.q0); a.pt.glow(0.2); });
      phase = 'ready'; drawImage(false); msg = '按「準備隨機態」';
    }
    function prep() { reset(); atoms.forEach((a) => { a.state = Math.random() < 0.5 ? 1 : 0; a.pt.setColor(a.state ? QC.q1 : QC.q0); }); phase = 'prepared'; msg = '量子計算結束：每顆原子處於 |0⟩（藍）或 |1⟩（紅）'; }
    function pushOut() {
      if (phase !== 'prepared') return;
      if (nondes) { msg = '非破壞模式：不推出原子，直接成像（只有 |1⟩ 會發光）'; phase = 'pushed'; return; }
      phase = 'pushing'; tP = 0; msg = '推出光：與 |1⟩ 共振 → |1⟩ 的原子被加速飛出光鑷';
      atoms.forEach((a) => { if (a.state === 1) a.flyV = new THREE.Vector3(2.5 + Math.random(), 0.8 + Math.random(), U.gauss() * 0.4); });
    }
    function image() {
      if (!['prepared', 'pushed'].includes(phase)) return;
      if (phase === 'prepared' && !nondes) { msg = '先按「① 推出 |1⟩」'; return; }
      phase = 'imaging'; tP = 0;
      const lossP = 0.01; // 示意：成像中約 1 % 原子損失（實際可 < 0.1 %）
      atoms.forEach((a) => {
        const lit = nondes ? a.state === 1 : a.present;
        a.lost = lit && Math.random() < lossP;
        a.count = App.poisson(lit && !a.lost ? bright() : dark());
        a.lit = lit && !a.lost;
      });
      msg = nondes ? '非破壞成像：|1⟩ 在循環躍遷上發光，|0⟩ 保持暗；所有原子留在光鑷中' : '成像：剩下的原子（原本是 |0⟩）散射 780 nm 光子';
    }
    const r1 = ui.row();
    ui.button('準備隨機態', () => prep(), r1);
    ui.button('① 推出 |1⟩', () => pushOut(), r1);
    ui.button('② 成像', () => image(), r1);
    ui.button('重置', () => reset(), r1);
    ui.slider('曝光時間 (ms)', 1, 20, 1, expo, (v) => { expo = v; }, (v) => `${v} ms`);
    ui.toggle('非破壞讀取（另一種做法）', false, (on) => { nondes = on; reset(); msg = on ? '非破壞模式：|1⟩ 發光、|0⟩ 暗，原子不被推出' : '標準模式：推出 |1⟩ → 成像'; });
    const ro = ui.readout();

    ctx.inset('每個光鑷位置的光子數分佈', (g, W, H, P) => {
      const s = stats(); const nb = 40; const bw = Math.max(1, Math.ceil((s.b + 4 * Math.sqrt(s.b)) / nb));
      const A = [], B = [];
      for (let k = 0; k < nb; k++) { let a = 0, b = 0; for (let q = k * bw; q < (k + 1) * bw; q++) { a += pois(s.d, q); b += pois(s.b, q); } A.push(a); B.push(b); }
      App.hist2(g, W, H, P, A, B, { thr: s.thr / bw, xlabel: `收集到的光子數（每格 ${bw}）`, colA: 'rgba(160,170,190,.7)', colB: 'rgba(94,224,170,.75)', xticks: [[0, '0'], [nb / 2, String((nb / 2) * bw)], [nb, String(nb * bw)]],
        notes: [['無原子（暗）', 40, 22, '#cfd8e6'], ['有原子（亮）', 250, 22, '#8ef0c8'], [`閾值 ${s.thr} · 判別保真度 ${(100 * s.F).toFixed(2)} %`, 120, 44, '#ffd28a']] });
    });

    reset();
    return {
      update(t, dt) {
        tP += dt;
        if (phase === 'pushing') {
          push.material.opacity = 0.12 * Math.min(1, tP * 3) * (tP < 1.2 ? 1 : Math.max(0, 1 - (tP - 1.2) * 2));
          atoms.forEach((a) => { if (a.flyV) { a.pt.position.addScaledVector(a.flyV, dt); a.flyV.y += dt * 0.5; a.pt.scale.setScalar(Math.max(0.01, 1 - tP * 0.5)); } });
          if (tP > 1.8) { atoms.forEach((a) => { if (a.flyV) { a.present = false; a.pt.visible = false; } }); phase = 'pushed'; push.material.opacity = 0; msg = '|1⟩ 的原子已離開；剩下的都是 |0⟩ → 按「② 成像」'; }
        }
        if (phase === 'imaging') {
          collect.material.opacity = 0.05;
          atoms.forEach((a) => {
            a.pt.glow(a.lit ? 0.6 + 0.4 * Math.sin(t * 15 + a.i) : 0.05);
            if (a.lit) a.pt.setColor(0xff8080);
            if (a.lit && Math.random() < 0.25) ph.emit(a.pt.position, [U.gauss() * 0.25, 1, U.gauss() * 0.25], 3, 0.8);
          });
          path.material.opacity = path2.material.opacity = 0.3 + 0.15 * Math.sin(t * 8);
          if (tP > 1.0 && phase === 'imaging') { drawImage(true); phase = 'imaged'; }
        }
        if (phase === 'imaged') {
          atoms.forEach((a) => a.lit && a.pt.glow(0.6 + 0.3 * Math.sin(t * 15 + a.i)));
          if (Math.random() < 0.6) { const L = atoms.filter((a) => a.lit); if (L.length) ph.emit(L[Math.floor(Math.random() * L.length)].pt.position, [U.gauss() * 0.25, 1, U.gauss() * 0.25], 3, 0.8); }
          const s = stats();
          let ok = 0; atoms.forEach((a) => { const call = a.count >= s.thr; const truth = nondes ? a.state === 1 : a.state === 0; if (call === truth) ok++; });
          const lost = atoms.filter((a) => a.lost).length;
          msg = `判讀：亮 = ${nondes ? '|1⟩' : '|0⟩'}、暗 = ${nondes ? '|0⟩' : '|1⟩'} · 正確 <b>${ok} / 25</b>${lost ? ` · ${lost} 顆在成像中丟失 → 讀錯` : ''}`;
        }
        ph.update(dt);
        const s = stats();
        ro.innerHTML = `${msg}<br>曝光 ${expo} ms：亮平均 ${s.b.toFixed(0)} 光子、暗平均 ${s.d.toFixed(1)} → 閾值 ${s.thr}，判別保真度 ${(100 * s.F).toFixed(2)} %`;
      },
    };
  },
});

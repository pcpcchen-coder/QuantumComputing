/* 原子場景 12：光鑷陣列的隨機裝載、成像與重排 */
App.register({
  id: 'tweezer', num: 11, short: '光鑷裝載與重排',
  title: '光鑷陣列：隨機裝載 → 成像 → 重排成無缺陷陣列',
  subtitle: '每支光鑷只有約一半機率抓到原子；拍照找出空位，再用移動光鑷把原子搬過去',
  desc: `<p><b>光鑷（optical tweezer）</b>：把遠紅失諧的雷射聚焦成約 1 μm 的光點，原子被吸到光強最大處。陷阱深度約 1 mK，間距約 3–5 μm。SLM 一次產生上百到上千支靜態光鑷。</p>
<p><b>① 裝載</b>：MOT 原子雲（約 10–100 μK）與光鑷重疊。光鑷太小，兩顆原子會因<b>光誘發碰撞</b>一起被踢出（碰撞阻斷），所以每支光鑷最後是 0 或 1 顆，機率約 50–60 %。</p>
<p><b>② 成像</b>：拍一張螢光照片，知道哪些位置有原子。<br>
<b>③ 重排</b>：FPGA 在毫秒內算出搬運路徑，AOD 產生的<b>移動光鑷</b>（洋紅色）沿光鑷之間的「通道」把儲備區的原子搬到目標區空位。</p>
<p>不重排時，N 個位置全部填滿的機率是 p<sup>N</sup>，100 顆就只有 10⁻³⁰；重排後幾乎一定成功。Caltech 2025 年做出 <b>6100 顆</b>原子的陣列，相干時間 12.6 s。大型陣列還要<b>連續補充原子</b>來彌補真空碰撞造成的損失。</p>`,
  camera: { pos: [3.2, 2.6, 8.6], target: [0, 0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const s = 0.5;
    let T = 6, p = 0.5, G = T + 4;
    let sites = [], atoms = new Map(), group = null, cloud = null;
    let phase = 'empty', tPhase = 0, moves = [], mi = 0, mt = 0, nMoves = 0;
    const aod = new THREE.Mesh(new THREE.ConeGeometry(0.16, 1.6, 20, 1, true), new THREE.MeshBasicMaterial({ color: 0xff4fd8, transparent: true, opacity: 0.45, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
    aod.rotation.x = Math.PI / 2; aod.visible = false; scene.add(aod);
    const aodDot = U.sphere(0.07, U.glow(0xff4fd8, 0.9), 0, 0, 0, 12); aodDot.visible = false; scene.add(aodDot);
    const title = ctx.label('', [0, 0, 0], 'gold');
    const legend = ctx.label('', [0, 0, 0], 'small');
    const atomGeo = new THREE.SphereGeometry(0.085, 16, 10);

    const isTarget = (i, j) => { const o = (G - T) / 2; return i >= o && i < o + T && j >= o && j < o + T; };
    const posOf = (i, j) => new THREE.Vector3((i - (G - 1) / 2) * s, (j - (G - 1) / 2) * s, 0);

    function build() {
      if (group) { scene.remove(group); group.traverse((o) => { o.geometry && o.geometry !== atomGeo && o.geometry.dispose(); }); }
      group = new THREE.Group(); scene.add(group);
      G = T + 4; sites = []; atoms = new Map();
      const coneGeo = new THREE.ConeGeometry(0.11, 1.4, 14, 1, true);
      const ringGeo = new THREE.TorusGeometry(0.12, 0.012, 6, 24);
      for (let i = 0; i < G; i++) for (let j = 0; j < G; j++) {
        const P = posOf(i, j); const tg = isTarget(i, j);
        const cone = new THREE.Mesh(coneGeo, new THREE.MeshBasicMaterial({ color: 0xd04090, transparent: true, opacity: tg ? 0.1 : 0.06, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
        cone.rotation.x = Math.PI / 2; cone.position.set(P.x, P.y, -0.7); group.add(cone);
        const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ color: tg ? 0xe0a54a : 0x55617a, transparent: true, opacity: tg ? 0.75 : 0.45 }));
        ring.position.copy(P); group.add(ring);
        sites.push({ i, j, P, tg, ring, key: i * 100 + j });
      }
      // 目標區外框
      const o = (G - T) / 2, a = (o - (G - 1) / 2 - 0.5) * s, b = (o + T - 1 - (G - 1) / 2 + 0.5) * s;
      group.add(U.line([[a, a, 0], [b, a, 0], [b, b, 0], [a, b, 0], [a, a, 0]], 0xe0a54a, 0.8));
      // MOT 原子雲
      const N = 1800, pos = new Float32Array(N * 3), R = G * s * 0.45;
      for (let k = 0; k < N; k++) { pos[3 * k] = U.gauss() * R; pos[3 * k + 1] = U.gauss() * R; pos[3 * k + 2] = U.gauss() * 0.4; }
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      cloud = new THREE.Points(geo, new THREE.PointsMaterial({ color: 0xff6060, size: 0.035, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }));
      group.add(cloud);
      title.pos.set(0, (G / 2) * s + 0.45, 0);
      legend.pos.set(0, -(G / 2) * s - 0.45, 0);
      phase = 'empty'; moves = []; mi = 0; nMoves = 0; aod.visible = aodDot.visible = false;
      title.set(`${G}×${G} 支光鑷，金框 = ${T}×${T} 目標區`);
      legend.set('按「① 裝載」開始');
    }
    const addAtom = (key, P) => { const m = new THREE.Mesh(atomGeo, U.mat(0x38d6e9, { emissive: 0x38d6e9, emissiveIntensity: 0.2 })); m.position.copy(P); group.add(m); atoms.set(key, m); return m; };

    function load() {
      build(); phase = 'loading'; tPhase = 0;
      legend.set('MOT 原子雲與光鑷重疊 → 碰撞阻斷 → 每支光鑷 0 或 1 顆');
    }
    function image() {
      if (!['loaded', 'done'].includes(phase)) return;
      phase = phase === 'done' ? 'done' : 'imaged';
      atoms.forEach((m) => { m.material.emissiveIntensity = 1.2; });
      sites.forEach((st) => { if (st.tg && !atoms.has(st.key)) { st.ring.material.color.setHex(0xff3b3b); st.ring.material.opacity = 1; } });
      legend.set('螢光成像：亮點 = 有原子；紅圈 = 目標區的空位');
    }
    function plan() {
      const center = new THREE.Vector3();
      const empties = sites.filter((st) => st.tg && !atoms.has(st.key)).sort((a, b) => a.P.distanceTo(center) - b.P.distanceTo(center));
      const pool = sites.filter((st) => !st.tg && atoms.has(st.key));
      const out = [];
      empties.forEach((e) => {
        if (!pool.length) return;
        let bi = 0, bd = 1e9;
        pool.forEach((r, k) => { const d = Math.abs(r.i - e.i) + Math.abs(r.j - e.j); if (d < bd) { bd = d; bi = k; } });
        const r = pool.splice(bi, 1)[0];
        // 沿光鑷之間的通道走：先斜移半格到通道，再水平、垂直，最後放進目標
        const h = s / 2; const sx = e.i >= r.i ? 1 : -1, sy = e.j >= r.j ? 1 : -1;
        const P0 = r.P.clone(), P1 = r.P.clone().add(new THREE.Vector3(h * sx, h * sy, 0));
        const P2 = new THREE.Vector3(e.P.x - h * sx, P1.y, 0), P3 = new THREE.Vector3(P2.x, e.P.y - h * sy, 0);
        out.push({ from: r, to: e, path: [P0, P1, P2, P3, e.P.clone()] });
      });
      return out;
    }
    function rearrange() {
      if (phase === 'loaded') image();
      if (phase !== 'imaged') return;
      moves = plan(); mi = 0; mt = 0; nMoves = moves.length; phase = 'moving';
      legend.set(`FPGA 規劃 ${moves.length} 次搬運 → AOD 移動光鑷逐一搬運（實際約數十 μs–1 ms / 次，可多支並行）`);
    }
    const pathAt = (pts, u) => {
      const L = [0]; for (let k = 1; k < pts.length; k++) L.push(L[k - 1] + pts[k].distanceTo(pts[k - 1]));
      const d = U.clamp(u, 0, 1) * L[L.length - 1];
      for (let k = 1; k < pts.length; k++) if (d <= L[k]) return pts[k - 1].clone().lerp(pts[k], (d - L[k - 1]) / (L[k] - L[k - 1] || 1));
      return pts[pts.length - 1].clone();
    };

    const r1 = ui.row();
    ui.button('① 裝載', () => load(), r1);
    ui.button('② 成像', () => image(), r1);
    ui.button('③ 重排', () => rearrange(), r1);
    ui.button('全部重來', () => build(), r1);
    ui.slider('陣列大小（目標 T×T）', 4, 8, 1, T, (v) => { if (v !== T) { T = v; build(); } }, (v) => `${v}×${v}（光鑷 ${(v + 4)}×${(v + 4)}）`);
    ui.slider('裝載機率 p', 0.4, 0.7, 0.05, p, (v) => { p = v; }, (v) => `${Math.round(v * 100)} %`);
    const ro = ui.readout();

    // 對數階乘（二項分佈尾端機率用）
    const lf = [0]; for (let k = 1; k <= 400; k++) lf.push(lf[k - 1] + Math.log(k));
    const tail = (M, N, q) => { let sum = 0; for (let k = N; k <= M; k++) sum += Math.exp(lf[M] - lf[k] - lf[M - k] + k * Math.log(q) + (M - k) * Math.log(1 - q)); return sum; };
    ctx.inset('目標區全部填滿的機率（log₁₀）', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [1, 100], [-30, 0], { xlabel: '目標原子數 N', xticks: [[1, '1'], [25, '25'], [49, '49'], [64, '64'], [100, '100']], yticks: [[0, '1'], [-10, '10⁻¹⁰'], [-20, '10⁻²⁰'], [-30, '10⁻³⁰']], m: { l: 50 } });
      P.curve(g, (n) => Math.max(-30, n * Math.log10(p)), 1, 100, X, Y, '#ff8a8a', 2);
      P.curve(g, (n) => { const t = Math.sqrt(n); const M = Math.round((t + 4) * (t + 4)); return Math.max(-30, Math.log10(Math.max(1e-300, tail(M, Math.round(n), p)))); }, 1, 100, X, Y, '#5ee08a', 2, 99);
      const N = T * T, M = (T + 4) * (T + 4);
      P.dot(g, X(N), Y(Math.max(-30, N * Math.log10(p))), 5, '#ff8a8a');
      P.dot(g, X(N), Y(Math.max(-30, Math.log10(Math.max(1e-300, tail(M, N, p))))), 5, '#5ee08a');
      P.text(g, '不重排：p^N', X(30), Y(-19), '#ff8a8a');
      P.text(g, `重排（光鑷 (√N+4)² 支）`, X(38), Y(-3), '#5ee08a');
    });

    build();
    return {
      update(t, dt) {
        tPhase += dt;
        if (phase === 'loading') {
          cloud.material.opacity = Math.min(0.9, tPhase * 1.5) * (tPhase > 1.2 ? Math.max(0, 1 - (tPhase - 1.2) / 0.8) : 1);
          if (tPhase > 0.9 && !atoms.size) sites.forEach((st) => { if (Math.random() < p) addAtom(st.key, st.P).material.emissiveIntensity = 0.15; });
          if (tPhase > 2.0) { phase = 'loaded'; cloud.material.opacity = 0; legend.set('已裝載（還不知道哪些位置有原子）→ 按「② 成像」'); }
        }
        if (phase === 'moving') {
          if (mi >= moves.length) {
            phase = 'done'; aod.visible = aodDot.visible = false;
            const filled = sites.filter((st) => st.tg && atoms.has(st.key)).length;
            legend.set(filled === T * T ? `完成：${T}×${T} 無缺陷陣列（${nMoves} 次搬運）` : `原子不夠：目標區還缺 ${T * T - filled} 顆 → 需要更大的儲備區或重新裝載`);
          } else {
            const mv = moves[mi]; mt += dt / 0.9;
            const P = pathAt(mv.path, U.smooth(U.clamp((mt - 0.15) / 0.7, 0, 1)));
            const m = atoms.get(mv.from.key);
            aod.visible = aodDot.visible = true; aod.position.set(P.x, P.y, -0.8); aodDot.position.copy(P);
            if (m) m.position.copy(P);
            if (mt >= 1) {
              atoms.delete(mv.from.key); if (m) atoms.set(mv.to.key, m);
              mv.to.ring.material.color.setHex(0xe0a54a); mv.to.ring.material.opacity = 0.75;
              mi++; mt = 0;
            }
          }
        }
        atoms.forEach((m, k) => { if (phase !== 'loading' && phase !== 'loaded') m.material.emissiveIntensity = 0.9 + 0.3 * Math.sin(t * 4 + k); });
        const filled = sites.filter((st) => st.tg && atoms.has(st.key)).length;
        ro.innerHTML = `光鑷 ${G * G} 支 · 原子 ${atoms.size} 顆（裝載率 ${(100 * atoms.size / (G * G)).toFixed(0)} %）<br>目標區 <b>${filled} / ${T * T}</b> 已填滿 · 搬運 ${Math.min(mi, nMoves)} / ${nMoves}`;
      },
    };
  },
});

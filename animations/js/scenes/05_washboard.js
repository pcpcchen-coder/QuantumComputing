/* 場景 5：RCSJ 模型與傾斜洗衣板位勢 — 相位粒子、電漿振盪、逃逸到電壓態、遲滯 */
App.register({
  id: 'washboard', num: 5, short: '洗衣板位勢',
  title: 'RCSJ 模型：傾斜洗衣板位勢',
  subtitle: 'U(φ) = −E_J cos φ − (ħI / 2e)·φ',
  desc: `<p>把真實 JJ 視為「理想 JJ ∥ 電阻 R ∥ 電容 C」（<b>RCSJ 模型</b>），相位差 φ 的運動就像<b>一顆球在傾斜的洗衣板上滾動</b>：</p>
<p><span class="eq">C(ħ/2e)φ̈ + (ħ/2eR)φ̇ + I<sub>c</sub> sin φ = I</span></p>
<p>• 電容 ↔ 質量　• 1/R ↔ 摩擦　• 偏壓電流 ↔ 傾斜角度<br>• 球在井底振盪 ↔ <b>電漿頻率 ω_p = √(2eI<sub>c</sub>/ħC)</b><br>• 球滾下坡 ↔ dφ/dt ≠ 0 ↔ <b>出現電壓</b></p>
<p>在井中，能量是量子化的（圖中短線）。早期的<b>相位量子位元</b>就是利用這些能階；現代 transmon 則在 I = 0（不傾斜）下工作。低阻尼（Q 大）時會看到<b>遲滯</b>：電流降回 I<sub>c</sub> 以下，球仍持續滾動。</p>`,
  camera: { pos: [0, 2.0, 15], target: [0, 0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui, app } = ctx;
    const sx = 0.55, sy = 1.0, depth = 2.4;
    const PH0 = -6 * Math.PI, PH1 = 16 * Math.PI;
    let iB = 0.3, Q = 8, phi = 0, v = 0, follow = true;
    const surfGroup = new THREE.Group(); scene.add(surfGroup);
    const Uf = (p) => -Math.cos(p) - iB * p;
    const ball = U.sphere(0.28, U.mat(0xe0a54a, { emissive: 0x6a3a00, emissiveIntensity: 0.7, metalness: 0.3 }));
    scene.add(ball);
    ctx.labelOn(ball, '相位粒子 φ', [0, 0.65, 0], 'gold small');
    const levels = new THREE.Group(); scene.add(levels);
    const barrierLbl = ctx.label('', [0, 0, 0], 'teal small');

    function buildSurface() {
      while (surfGroup.children.length) { const o = surfGroup.children.pop(); o.geometry.dispose(); }
      const N = 1400, pos = [], idx = [], col = [];
      for (let i = 0; i <= N; i++) {
        const p = PH0 + ((PH1 - PH0) * i) / N, y = Uf(p) * sy;
        const c = new THREE.Color().setHSL(0.53 - 0.05 * Math.cos(p), 0.6, 0.28 + 0.1 * (1 - Math.cos(p)) / 2);
        for (let k = 0; k <= 1; k++) { pos.push(p * sx, y, -depth / 2 + depth * k); col.push(c.r, c.g, c.b); }
      }
      for (let i = 0; i < N; i++) { const a = 2 * i, b = a + 2; idx.push(a, b, a + 1, b, b + 1, a + 1); }
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
      g.setIndex(idx); g.computeVertexNormals();
      surfGroup.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, roughness: 0.5, metalness: 0.1 })));
      const edge = []; for (let i = 0; i <= N; i++) { const p = PH0 + ((PH1 - PH0) * i) / N; edge.push([p * sx, Uf(p) * sy + 0.01, depth / 2]); }
      surfGroup.add(U.line(edge, 0x8ef0ff, 0.9));
    }
    function buildLevels() {
      while (levels.children.length) { const o = levels.children.pop(); o.geometry.dispose(); }
      if (iB >= 1) { barrierLbl.show(false); return; }
      // 所在井的最小值與量子化能階（E_J / ħω_p0 = 6 的示意）
      const k = Math.round((phi - Math.asin(iB)) / (2 * Math.PI));
      const pmin = Math.asin(iB) + 2 * Math.PI * k, pmax = Math.PI - Math.asin(iB) + 2 * Math.PI * k;
      const umin = Uf(pmin), dU = Uf(pmax) - umin;
      const wp = Math.pow(1 - iB * iB, 0.25) / 6; // ħω_p / E_J
      for (let n = 0; n < 6; n++) {
        const E = umin + (n + 0.5) * wp * (1 - 0.06 * n);
        if (E > umin + dU) break;
        // 找出井內寬度
        let a = pmin, b = pmin;
        while (a > pmin - Math.PI && Uf(a) < E) a -= 0.01;
        while (b < pmax && Uf(b) < E) b += 0.01;
        levels.add(U.line([[a * sx, E * sy, depth / 2 + 0.02], [b * sx, E * sy, depth / 2 + 0.02]], n === 0 ? 0x4f8cff : n === 1 ? 0xff5a5f : 0xb9c4d4, 0.9));
      }
      barrierLbl.show(true);
      barrierLbl.pos.set(pmax * sx, Uf(pmax) * sy + 0.5, 0);
      barrierLbl.set(`位障 ΔU ≈ ${(dU).toFixed(2)} E_J`);
    }
    buildSurface();

    const sl = ui.slider('偏壓電流 I / I<sub>c</sub>（傾斜）', 0, 1.6, 0.01, iB, (x) => { iB = x; buildSurface(); }, (x) => x.toFixed(2));
    ui.slider('品質因子 Q（阻尼越小 Q 越大）', 1, 20, 0.5, Q, (x) => { Q = x; }, (x) => x.toFixed(1));
    const r = ui.row();
    ui.button('掃描：0 → 1.3 → 0（看遲滯）', () => { sweep = 0; }, r);
    ui.button('重設', () => { phi = Math.asin(Math.min(1, iB)); v = 0; sweep = -1; }, r);
    ui.toggle('相機跟隨相位粒子', true, (on) => { follow = on; if (!on) app.orbit.reset(); });
    const ro = ui.readout();
    let sweep = -1, vAvg = 0;
    const trace = [];

    ctx.inset('I–V 特性（RCSJ，低阻尼時有遲滯）', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [0, 1.7], [0, 1.7], { xlabel: '平均電壓 ⟨V⟩ / IcR', ylabel: 'I / Ic', xticks: [[0, '0'], [1, '1']], yticks: [[0, '0'], [1, '1']] });
      const ir = Math.min(1, 4 / (Math.PI * Q));
      g.strokeStyle = 'rgba(224,165,74,.5)'; g.lineWidth = 2; g.setLineDash([4, 4]);
      g.beginPath(); g.moveTo(X(0), Y(0)); g.lineTo(X(0), Y(1)); g.moveTo(X(ir), Y(ir)); g.lineTo(X(1.7), Y(1.7)); g.stroke(); g.setLineDash([]);
      g.strokeStyle = '#38c6d9'; g.lineWidth = 1.5; g.beginPath();
      trace.forEach(([x, y], i) => (i ? g.lineTo(X(x), Y(y)) : g.moveTo(X(x), Y(y)))); g.stroke();
      P.dot(g, X(Math.min(1.7, vAvg)), Y(iB), 5, '#e0a54a');
      P.text(g, `回捕電流 I_r ≈ 4Ic/πQ = ${ir.toFixed(2)} Ic`, W - 10, 22, '#9fb0c8', 'right');
    });

    const tmpT = new THREE.Vector3();
    let lvTimer = 0;
    return {
      update(time, dt) {
        if (sweep >= 0) {
          sweep += dt / 14; // 14 秒完成
          const s = sweep < 0.5 ? sweep * 2 * 1.3 : (1 - sweep) * 2 * 1.3;
          sl.set(Math.max(0, s));
          if (sweep >= 1) sweep = -1;
        }
        const n = 20, h = (dt * 7) / n;
        for (let k = 0; k < n; k++) {
          const a = iB - Math.sin(phi) - v / Q + 0.03 * U.gauss();
          v += a * h; phi += v * h;
        }
        vAvg += (v / Q - vAvg) * Math.min(1, dt * 1.5);
        if (sweep >= 0) { trace.push([Math.max(0, vAvg), iB]); if (trace.length > 2000) trace.shift(); }
        // 範圍外 → 球與相機一起平移 4π（畫面不變）
        if (phi > 6 * Math.PI || phi < -2 * Math.PI) {
          const sh = phi > 0 ? -4 * Math.PI : 4 * Math.PI;
          phi += sh;
          const d = new THREE.Vector3(sh * sx, -iB * sh * sy, 0);
          app.orbit.target.add(d); app.orbit.apply();
        }
        ball.position.set(phi * sx, Uf(phi) * sy + 0.28, 0);
        if (follow) {
          tmpT.set(ball.position.x, ball.position.y, 0);
          app.orbit.target.lerp(tmpT, Math.min(1, dt * 2)); app.orbit.apply();
        }
        lvTimer -= dt; if (lvTimer <= 0) { buildLevels(); lvTimer = 0.25; }
        const running = Math.abs(vAvg) > 0.08;
        ro.innerHTML = `${running ? '<b style="color:#ff8a8a">電壓態</b>：相位持續滾動，⟨dφ/dt⟩ ≠ 0 → V = (ħ/2e)⟨dφ/dt⟩' : '<b style="color:#8ef0ff">零電壓態</b>：相位被困在井中做電漿振盪'}<br>` +
          `ω_p(I) = ω_p0 (1 − (I/I<sub>c</sub>)²)^{1/4} = ${(Math.pow(Math.max(0, 1 - iB * iB), 0.25)).toFixed(2)} ω_p0`;
      },
    };
  },
});

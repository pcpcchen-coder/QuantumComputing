/* 場景 1：Bloch 球 — 量子位元狀態、Rabi 振盪、Ramsey 進動、T1 衰減 */
App.register({
  id: 'bloch', num: 1, short: 'Bloch 球',
  title: '量子位元與 Bloch 球',
  subtitle: '|ψ⟩ = cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩',
  desc: `<p>任何單一量子位元的純態都能畫成單位球面上的一個點：<b>北極是 |0⟩、南極是 |1⟩</b>，赤道則是等權重的疊加態。</p>
<p><b>Rabi 振盪</b>：在共振微波驅動下，狀態繞 x 軸旋轉；脈衝長度決定旋轉角（π 脈衝 = 反轉）。</p>
<p><b>Ramsey / 失相 (T2)</b>：赤道上的態因頻率失諧而繞 z 軸進動，雜訊使相位擴散、向量縮短。</p>
<p><b>能量弛豫 (T1)</b>：|1⟩ 會自發放出能量回到 |0⟩。</p>`,
  camera: { pos: [3.6, 2.4, 4.2], target: [0, 0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const R = 1.6;
    // 球體
    scene.add(new THREE.Mesh(new THREE.SphereGeometry(R, 48, 32),
      new THREE.MeshStandardMaterial({ color: 0x3a6ea5, transparent: true, opacity: 0.12, roughness: 0.2, depthWrite: false })));
    const wire = new THREE.Mesh(new THREE.SphereGeometry(R, 24, 16),
      new THREE.MeshBasicMaterial({ color: 0x6f8fbf, wireframe: true, transparent: true, opacity: 0.12 }));
    scene.add(wire);
    // 赤道與經線
    const circ = (axis) => {
      const pts = [];
      for (let i = 0; i <= 128; i++) {
        const a = (i / 128) * Math.PI * 2;
        pts.push(axis === 'eq' ? [R * Math.cos(a), 0, R * Math.sin(a)] : axis === 'xz' ? [R * Math.cos(a), R * Math.sin(a), 0] : [0, R * Math.sin(a), R * Math.cos(a)]);
      }
      return U.line(pts, 0x9fb7e0, 0.55);
    };
    scene.add(circ('eq'), circ('xz'), circ('yz'));
    // 座標軸（Bloch 座標：z 向上 → three 的 y；x → three 的 z；y → three 的 x）
    const B2T = (x, y, z) => new THREE.Vector3(y, z, x);
    [[B2T(1, 0, 0), 0xff9f43], [B2T(0, 1, 0), 0x2ecc71], [B2T(0, 0, 1), 0x8ab4ff]].forEach(([d, c]) => {
      scene.add(U.line([d.clone().multiplyScalar(-R * 1.15), d.clone().multiplyScalar(R * 1.15)], c, 0.8));
    });
    ctx.label('|0⟩', B2T(0, 0, R * 1.28), 'q0 big');
    ctx.label('|1⟩', B2T(0, 0, -R * 1.28), 'q1 big');
    ctx.label('x · |+⟩', B2T(R * 1.3, 0, 0), 'small');
    ctx.label('y · |+i⟩', B2T(0, R * 1.3, 0), 'small');

    // 狀態向量
    const arrow = U.fatArrow(0xe0a54a, R, 0.035);
    scene.add(arrow);
    const tip = U.sphere(0.07, U.glow(0xffd28a));
    scene.add(tip);
    const trail = U.dynLine(600, 0xffd28a, 0.85); scene.add(trail.obj);
    const trailPts = [];

    const stLabel = ctx.label('', [0, 0, 0], 'gold small');
    let mode = 'rabi', t0 = 0, manual = { th: 60, ph: 30 };
    let omega = 1.0, detune = 0.8, T2 = 6, T1 = 5;
    let vec = new THREE.Vector3(0, 0, 1); // Bloch (x,y,z)
    const hist = [];

    const reset = () => { trailPts.length = 0; hist.length = 0; t0 = ctx.app.time; };
    ui.radio([['rabi', 'Rabi 振盪'], ['ramsey', 'Ramsey 進動 + T2'], ['t1', 'T1 能量弛豫'], ['manual', '手動 θ / φ']], mode,
      (m) => { mode = m; reset(); });
    ui.slider('Rabi 頻率 Ω（相對單位）', 0.2, 2, 0.05, omega, (v) => { omega = v; }, (v) => v.toFixed(2));
    ui.slider('失諧 Δ（Ramsey）', 0, 2, 0.05, detune, (v) => { detune = v; }, (v) => v.toFixed(2));
    const thS = ui.slider('θ（手動）', 0, 180, 1, manual.th, (v) => { manual.th = v; }, (v) => v + '°');
    const phS = ui.slider('φ（手動）', 0, 360, 1, manual.ph, (v) => { manual.ph = v; }, (v) => v + '°');
    const ro = ui.readout();
    ui.button('π/2 脈衝 → 疊加態', () => { mode = 'manual'; thS.set(90); phS.set(270); reset(); });

    ctx.inset('激發態機率 P(|1⟩) 隨時間變化', (g, W, H, P) => {
      const tmax = 12;
      const { X, Y } = P.frame(g, W, H, [0, tmax], [0, 1], { xlabel: '時間 t（相對單位）', ylabel: 'P(|1⟩)', yticks: [[0, '0'], [0.5, '0.5'], [1, '1']], xticks: [[0, '0'], [6, '6'], [12, '12']] });
      g.strokeStyle = '#e0a54a'; g.lineWidth = 2; g.beginPath();
      hist.forEach(([t, p], i) => { const x = X(Math.min(t, tmax)); i ? g.lineTo(x, Y(p)) : g.moveTo(x, Y(p)); });
      g.stroke();
    });

    return {
      update(time) {
        let t = time - t0;
        if (t > 12) { reset(); t = 0; }
        if (mode === 'rabi') {
          const a = omega * t * 1.2; // 繞 x 軸
          vec.set(0, -Math.sin(a), Math.cos(a));
        } else if (mode === 'ramsey') {
          const a = detune * t * 1.5, r = Math.exp(-t / T2);
          vec.set(r * Math.cos(a), r * Math.sin(a), 0);
        } else if (mode === 't1') {
          const pe = Math.exp(-t / T1 * 1.0);
          vec.set(0, 0, 1 - 2 * pe);
        } else {
          const th = (manual.th * Math.PI) / 180, ph = (manual.ph * Math.PI) / 180;
          vec.set(Math.sin(th) * Math.cos(ph), Math.sin(th) * Math.sin(ph), Math.cos(th));
        }
        const v3 = B2T(vec.x, vec.y, vec.z).multiplyScalar(R);
        arrow.setVec(v3); tip.position.copy(v3);
        if (mode !== 'manual') {
          trailPts.push([v3.x, v3.y, v3.z]); if (trailPts.length > 600) trailPts.shift();
        } else { trailPts.length = 0; }
        trail.set(trailPts);
        const p1 = (1 - vec.z) / 2;
        hist.push([t, p1]);
        stLabel.pos.copy(v3.clone().multiplyScalar(1.15));
        stLabel.set(`P(1) = ${p1.toFixed(2)}`);
        const L = vec.length();
        ro.innerHTML = `Bloch 向量 (x, y, z) = (${vec.x.toFixed(2)}, ${vec.y.toFixed(2)}, ${vec.z.toFixed(2)})<br>|r| = ${L.toFixed(2)} ${L < 0.98 ? '（混態：失去相干性）' : '（純態）'}`;
      },
    };
  },
});

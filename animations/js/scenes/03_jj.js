/* 場景 3：約瑟夫森接面 SIS 三明治結構 — Cooper pair 穿隧、相位差、DC/AC Josephson 效應 */
App.register({
  id: 'jj', num: 3, short: 'JJ 結構',
  title: '約瑟夫森接面（JJ）的結構與穿隧',
  subtitle: 'Al / AlOx / Al：超導體–絕緣體–超導體（SIS）',
  desc: `<p>兩片超導鋁中間夾一層僅 <b>1–2 nm</b> 的氧化鋁（AlOx）。絕緣層夠薄，Cooper pair 可以<b>整對量子穿隧</b>。</p>
<p>兩側各有自己的巨觀相位 φ<sub>1</sub>、φ<sub>2</sub>（圖中旋轉的「相位鐘」），相位差 <b>φ = φ<sub>2</sub> − φ<sub>1</sub></b> 決定一切：</p>
<p><b>DC Josephson</b>：<span class="eq">I = I<sub>c</sub> sin φ</span>　不加電壓也能有超電流。<br>
<b>AC Josephson</b>：<span class="eq">dφ/dt = 2eV/ħ</span>　一旦有電壓 V，相位持續旋轉，電流以 483.6 GHz/mV 振盪。</p>
<p>拉動偏壓電流：I &lt; I<sub>c</sub> 時相位差固定、無電壓；I &gt; I<sub>c</sub> 時進入電壓態。</p>`,
  camera: { pos: [7.5, 5.5, 11.5], target: [0, 0.3, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    // 基板
    scene.add(U.box(12, 0.4, 5, U.mat(0x2a3140, { roughness: 0.8 }), 0, -1.0, 0));
    ctx.label('矽 / 藍寶石 基板', [-4.6, -1.0, 2.6], 'small');
    const alMat = U.metal(0xb9c4d4, { roughness: 0.32 });
    const W = 4.6, Hh = 1.2, D = 2.6, ox = 0.16;
    const left = U.box(W, Hh, D, alMat, -W / 2 - ox / 2, -0.2, 0);
    const right = U.box(W, Hh, D, alMat, W / 2 + ox / 2, -0.2, 0);
    // 為了看見內部，右側電極半透明
    right.material = U.metal(0xb9c4d4, { roughness: 0.32, transparent: true, opacity: 0.3, depthWrite: false });
    right.add(new THREE.LineSegments(new THREE.EdgesGeometry(right.geometry), new THREE.LineBasicMaterial({ color: 0xdfe8f5 })));
    const barrier = U.box(ox, Hh, D, new THREE.MeshStandardMaterial({ color: 0xff7a59, emissive: 0x5a1a00, emissiveIntensity: 0.6, transparent: true, opacity: 0.85 }), 0, -0.2, 0);
    scene.add(left, right, barrier);
    ctx.label('超導體 Al（電極 1）· 相位 φ₁', [-W / 2, 1.15, 0], 'q0');
    ctx.label('超導體 Al（電極 2）· 相位 φ₂', [W / 2, 1.15, 0], 'q1');
    ctx.label('AlOx 穿隧阻障 ~1–2 nm', [0, -1.25, D / 2 + 0.2], 'gold');

    // 相位鐘
    const clock = (x, color) => {
      const g = new THREE.Group(); g.position.set(x, 2.3, 0);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.55, 0.03, 8, 48), U.glow(color));
      const hand = U.fatArrow(color, 0.5, 0.035);
      g.add(ring, hand); scene.add(g);
      return { g, hand };
    };
    const c1 = clock(-W / 2, 0x4f8cff), c2 = clock(W / 2, 0xff5a5f);
    const dphiLbl = ctx.label('', [0, 3.2, 0], 'big gold');

    // Cooper pairs
    const NPairs = 26; const pairs = [];
    const eGeo = new THREE.SphereGeometry(0.075, 12, 8);
    const pm1 = U.glow(0x6fb4ff), pm2 = U.glow(0x9d7bff);
    for (let i = 0; i < NPairs; i++) {
      const g = new THREE.Group();
      const a = new THREE.Mesh(eGeo, pm1), b = new THREE.Mesh(eGeo, pm2);
      a.position.x = 0.13; b.position.x = -0.13; g.add(a, b);
      g.position.set(-W + Math.random() * 2 * W, -0.2 + (Math.random() - 0.5) * (Hh - 0.3), (Math.random() - 0.5) * (D - 0.3));
      g.userData = { ph: Math.random() * 6.28 };
      scene.add(g); pairs.push(g);
    }
    // 穿隧閃光
    const flashes = [];
    for (let i = 0; i < 6; i++) {
      const f = U.sphere(0.16, new THREE.MeshBasicMaterial({ color: 0xffe08a, transparent: true, opacity: 0 }));
      scene.add(f); flashes.push(f);
    }
    // 外部偏壓電路（導線示意）
    const wireMat = U.metal(0xd8a24a, { roughness: 0.4 });
    scene.add(U.tube([[-W - 0.2, -0.2, 0], [-W - 1.0, -0.2, 0], [-W - 1.0, -2.6, 0], [W + 1.0, -2.6, 0], [W + 1.0, -0.2, 0], [W + 0.2, -0.2, 0]], 0.05, wireMat));
    const src = U.box(1.2, 0.6, 0.6, U.mat(0x334155), 0, -2.6, 0); scene.add(src);
    ctx.label('偏壓電流源 I', [0, -3.15, 0], 'small');
    const vLbl = ctx.label('', [W + 1.9, -1.4, 0], 'teal');

    let iBias = 0.5; // I/Ic
    let phi = Math.asin(iBias), phi1 = 0;
    const sl = ui.slider('偏壓電流 I / I<sub>c</sub>', 0, 1.6, 0.01, iBias, (v) => { iBias = v; }, (v) => v.toFixed(2));
    ui.radio([[0.5, 'I = 0.5 Ic（超電流）'], [0.98, 'I ≈ Ic'], [1.4, 'I = 1.4 Ic（電壓態）']], 0.5, (v) => sl.set(v));
    const ro = ui.readout();

    const cpr = [];
    ctx.inset('電流–相位關係 I = Ic sin φ 與 I–V 特性', (g, Wd, H, P) => {
      const half = Wd / 2 - 4;
      const f1 = P.frame(g, half, H, [0, 2 * Math.PI], [-1.6, 1.6], { xlabel: '相位差 φ', ylabel: 'I / Ic', xticks: [[0, '0'], [Math.PI, 'π'], [2 * Math.PI, '2π']], yticks: [[-1, '-1'], [0, '0'], [1, '1']], m: { l: 38 } });
      P.curve(g, Math.sin, 0, 2 * Math.PI, f1.X, f1.Y, '#e0a54a', 2);
      const ph = ((phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
      P.dot(g, f1.X(ph), f1.Y(Math.sin(ph)), 5, '#38c6d9');
      g.save(); g.translate(half + 8, 0);
      const f2 = P.frame(g, half, H, [0, 3], [0, 1.6], { xlabel: '電壓 V（2Δ/e 單位）', ylabel: 'I / Ic', xticks: [[0, '0'], [1, '2Δ/e'], [3, '']], yticks: [[0, '0'], [1, '1']], m: { l: 38 } });
      // 簡化 I-V：V=0 超電流分支 + 準粒子分支
      g.strokeStyle = '#e0a54a'; g.lineWidth = 2; g.beginPath();
      g.moveTo(f2.X(0), f2.Y(0)); g.lineTo(f2.X(0), f2.Y(1)); g.stroke();
      P.curve(g, (v) => (v < 1 ? 0.03 * v : 0.03 + (v - 1) * 0.78), 0, 3, f2.X, f2.Y, '#9fb0c8', 1.5);
      P.dot(g, f2.X(Math.min(3, iBias <= 1 ? 0 : 1 + (iBias - 0.03) / 0.78)), f2.Y(iBias), 5, '#38c6d9');
      g.restore();
    });

    let fi = 0, fTimer = 0;
    return {
      update(time, dt) {
        const voltageState = iBias > 1;
        let flow;
        if (!voltageState) {
          phi += (Math.asin(iBias) - phi) * Math.min(1, dt * 4); // 相位差鎖定在 arcsin(I/Ic)
          flow = Math.sin(phi);
        } else {
          const Vn = Math.sqrt(iBias * iBias - 1); // RCSJ 過阻尼時平均電壓
          phi += dt * 6 * Vn;
          flow = 0.6 + 0.4 * Math.sin(phi);
        }
        phi1 += dt * 0.8; // 整體相位（不影響物理，只是示意兩側相位都在轉）
        c1.hand.rotation.z = -phi1; c2.hand.rotation.z = -(phi1 + phi);
        const dphi = (((phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI));
        dphiLbl.set(`φ = φ₂ − φ₁ = ${(dphi * 180 / Math.PI).toFixed(0)}°　I = Ic sin φ = ${Math.sin(phi).toFixed(2)} Ic`);
        vLbl.set(voltageState ? `V ≠ 0　→ 交流 Josephson 振盪<br>f = 2eV/h（483.6 GHz/mV）` : 'V = 0　（無耗散超電流）');
        // Cooper pair 流動
        const speed = 1.6 * flow;
        pairs.forEach((p) => {
          p.position.x += speed * dt;
          p.userData.ph += dt * 3; p.rotation.y = p.userData.ph; p.rotation.z = p.userData.ph * 0.4;
          if (p.position.x > W) p.position.x = -W;
          if (p.position.x < -W) p.position.x = W;
          // 穿過阻障時閃光
          const px = p.position.x;
          if (Math.abs(px) < 0.05 && Math.abs(speed) > 0.05 && fTimer <= 0) {
            const f = flashes[fi++ % flashes.length]; f.position.copy(p.position); f.material.opacity = 0.9; f.scale.setScalar(0.4); fTimer = 0.04;
          }
        });
        fTimer -= dt;
        flashes.forEach((f) => { f.material.opacity = Math.max(0, f.material.opacity - dt * 2.5); f.scale.multiplyScalar(1 + dt * 3); });
        barrier.material.emissiveIntensity = voltageState ? 0.6 + 0.5 * Math.abs(Math.sin(phi)) : 0.6;
        ro.innerHTML = voltageState
          ? `電壓態：相位差持續旋轉 → 電流以 2eV/h 振盪<br>同時出現準粒子（電阻性）電流 → 有耗散`
          : `超電流態：φ = arcsin(I/Ic) = ${(Math.asin(iBias) * 180 / Math.PI).toFixed(1)}°<br>電壓為零，能量不耗散`;
      },
    };
  },
});

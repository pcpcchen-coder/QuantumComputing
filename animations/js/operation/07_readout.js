/* 場景 7：讀取 — 量測基底、色散讀取 → IQ 點 → 閾值判別 → 位元 → 統計 → 誤差緩解 */
App.register({
  id: 'readout', num: 7, short: '讀取與統計',
  title: '讀取：從微波訊號到 0/1，再到期望值',
  subtitle: '量測基底 → 讀取脈衝 → IQ 點 → 閾值 → 位元 → 直方圖 → ⟨Z⟩',
  desc: `<p><b>硬體只會在 Z 基底量測</b>（|0⟩ 或 |1⟩）。想量 X 或 Y，就先加一個旋轉閘：量 X 前加 H，量 Y 前加 S†·H。</p>
<p>每一個 shot：送出讀取脈衝（~0.3–2 μs），讀取腔的頻率因量子位元狀態而偏移（色散位移），反射/穿透訊號經放大、ADC、積分後得到 <b>IQ 平面上的一個點</b>，再用<b>閾值</b>判成 0 或 1。</p>
<p>誤差來源：兩團雲重疊（SNR 不足）、讀取期間 |1⟩ 衰減成 |0⟩（T<sub>1</sub>）。積分時間越長 SNR 越好，但衰減越多 —— 需要折衷。</p>
<p><b>讀取誤差緩解</b>：先量好「混淆矩陣」（準備 0 量到 1 的機率、準備 1 量到 0 的機率），再把結果反推回去。</p>`,
  camera: { pos: [0.0, 4.6, 10.8], target: [0.0, 0.1, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const Bl = App.Bloch(ctx, { r: 0.95, pos: [-4.0, 1.5, 0], trailN: 2, title: '準備的狀態' });
    // 基底旋轉閘
    const gBox = U.box(0.7, 0.7, 0.4, U.mat(0x1c9db0, { emissive: 0x1c9db0, emissiveIntensity: 0.2 }), -2.3, 1.5, 0); scene.add(gBox);
    const gL = ctx.label('—', [-2.3, 1.5, 0.3], 'plain');
    ctx.label('基底旋轉', [-2.3, 2.15, 0], 'small');
    // 讀取腔、放大器、ADC
    const res = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.07, 12, 48), U.mat(0x38c6d9, { emissive: 0x38c6d9, emissiveIntensity: 0.25 }));
    res.position.set(-1.0, 1.5, 0); scene.add(res);
    ctx.label('讀取腔', [-1.0, 2.15, 0], 'small');
    const amp = new THREE.Mesh(new THREE.ConeGeometry(0.35, 0.7, 3), U.mat(0xe0a54a)); amp.rotation.z = -Math.PI / 2; amp.position.set(0.3, 1.5, 0); scene.add(amp);
    ctx.label('放大器', [0.3, 2.15, 0], 'small');
    scene.add(U.box(0.7, 0.55, 0.5, U.mat(0x4a5468), 1.5, 1.5, 0));
    ctx.label('ADC + 積分', [1.5, 2.15, 0], 'small');
    scene.add(U.tube([[-3.0, 1.5, 0], [2.3, 1.5, 0], [2.6, 1.5, 0], [2.6, -0.9, 0]], 0.03, U.metal(0xb87333)));
    const pk = U.sphere(0.1, U.glow(0xffd28a)); scene.add(pk);
    // IQ 平面
    const IX = 0.4, IY = -1.4;
    const iq = new THREE.Group(); iq.position.set(IX, IY, 0); scene.add(iq);
    const Wp = 4.2;
    iq.add(U.box(Wp, 0.03, Wp, U.mat(0x0f1828, { roughness: 0.95 }), 0, -0.02, 0));
    const grid = new THREE.GridHelper(Wp, 10, 0x2b3c58, 0x1b2840); iq.add(grid);
    iq.add(U.line([[-Wp / 2, 0.01, 0], [Wp / 2, 0.01, 0]], 0x6f8fbf), U.line([[0, 0.01, -Wp / 2], [0, 0.01, Wp / 2]], 0x6f8fbf));
    ctx.label('I', [IX + Wp / 2 + 0.25, IY, 0], 'small'); ctx.label('Q', [IX, IY, -Wp / 2 - 0.25], 'small');
    ctx.label('IQ 平面（每個點 = 一個 shot）', [IX, IY, Wp / 2 + 0.45], 'teal small');
    const thMesh = U.box(0.03, 0.9, Wp, new THREE.MeshBasicMaterial({ color: 0xff6bd5, transparent: true, opacity: 0.35, depthWrite: false }), 0, 0.45, 0); iq.add(thMesh);
    const c0L = ctx.label('|0⟩ 雲', [0, 0, 0], 'q0 small'), c1L = ctx.label('|1⟩ 雲', [0, 0, 0], 'q1 small');
    const MAXP = 3000;
    const pgeo = new THREE.BufferGeometry();
    pgeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MAXP * 3), 3));
    pgeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(MAXP * 3), 3));
    const pts = new THREE.Points(pgeo, new THREE.PointsMaterial({ size: 0.07, vertexColors: true }));
    pts.frustumCulled = false; iq.add(pts);
    let np = 0;

    let th = 70, basis = 'Z', tau = 1.0, sep = 1.0, thr = 0, auto = true, rate = 60, accum = 0, mitig = true, t1on = true;
    const T1 = 50; // μs
    let n0 = 0, n1 = 0, xs = [];
    const scale = 1.3; // IQ 平面單位
    const c0 = () => -sep * scale / 2, c1 = () => sep * scale / 2;
    const sigma = () => (0.55 * scale) / Math.sqrt(tau * 4);
    const pdec = () => (t1on ? 1 - Math.exp(-tau / T1) : 0);
    const Phi = (x) => 0.5 * (1 + erf(x / Math.SQRT2));
    function erf(x) { const s = Math.sign(x); x = Math.abs(x); const t = 1 / (1 + 0.3275911 * x); const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496735) * t + 0.254829592) * t * Math.exp(-x * x); return s * y; }
    const confusion = () => { // P(meas | prep)
      const s = sigma(), x = thr * scale;
      const p10 = 1 - Phi((x - c0()) / s);
      const pd = pdec(), frac = U.clamp((c1() - x) / (c1() - c0()), 0, 1);
      const p11 = (1 - pd) * (1 - Phi((x - c1()) / s)) + pd * frac;
      return { p10, p11, p01: 1 - p11, p00: 1 - p10 };
    };
    const blochVec = () => { const T = (th * Math.PI) / 180; return [Math.sin(T) * Math.cos(0.4), Math.sin(T) * Math.sin(0.4), Math.cos(T)]; };
    const pTrue1 = () => { const [x, y, z] = blochVec(); const c = basis === 'Z' ? z : basis === 'X' ? x : y; return (1 - c) / 2; };
    const clear = () => { n0 = n1 = 0; np = 0; xs = []; pgeo.setDrawRange(0, 0); };
    const shot = () => {
      const b = Math.random() < pTrue1() ? 1 : 0;
      let cx = b ? c1() : c0();
      if (b && Math.random() < pdec()) cx = c1() + (c0() - c1()) * Math.random();
      const x = cx + U.gauss() * sigma(), z = U.gauss() * sigma();
      const m = x > thr * scale ? 1 : 0; m ? n1++ : n0++;
      xs.push(x); if (xs.length > 6000) xs.shift();
      const i = np % MAXP; const P = pgeo.attributes.position.array, Cc = pgeo.attributes.color.array;
      P[3 * i] = U.clamp(x, -Wp / 2, Wp / 2); P[3 * i + 1] = 0.03; P[3 * i + 2] = U.clamp(z, -Wp / 2, Wp / 2);
      const col = m ? [1, 0.36, 0.38] : [0.31, 0.55, 1]; Cc[3 * i] = col[0]; Cc[3 * i + 1] = col[1]; Cc[3 * i + 2] = col[2];
      np++; pgeo.setDrawRange(0, Math.min(np, MAXP)); pgeo.attributes.position.needsUpdate = true; pgeo.attributes.color.needsUpdate = true;
    };
    ui.slider('準備狀態 θ', 0, 180, 1, th, (v) => { th = v; clear(); }, (v) => v + '°');
    ui.radio([['Z', '量 Z（直接量）'], ['X', '量 X（先 H）'], ['Y', '量 Y（先 S†H）']], basis, (b) => { basis = b; clear(); });
    ui.slider('積分時間 τ', 0.1, 4, 0.05, tau, (v) => { tau = v; clear(); }, (v) => v.toFixed(2) + ' μs');
    ui.slider('兩團雲的間距（色散位移/放大器）', 0.3, 1.6, 0.05, sep, (v) => { sep = v; clear(); }, (v) => v.toFixed(2));
    ui.slider('判別閾值位置', -1, 1, 0.02, thr, (v) => { thr = v; clear(); }, (v) => v.toFixed(2));
    const r = ui.row();
    ui.toggle('連續 shots', auto, (v) => { auto = v; });
    ui.button('清除', clear, r);
    ui.toggle('讀取期間 T₁ 衰減（T₁ = 50 μs）', t1on, (v) => { t1on = v; clear(); });
    ui.toggle('讀取誤差緩解', mitig, (v) => { mitig = v; });
    const ro = ui.readout();

    ctx.inset('IQ 點投影到 I 軸的分佈與閾值', (g, W, H, P) => {
      const lo = -Wp / 2, hi = Wp / 2, nb = 60, hb = new Array(nb).fill(0);
      xs.forEach((x) => { const k = Math.floor(((x - lo) / (hi - lo)) * nb); if (k >= 0 && k < nb) hb[k]++; });
      const mx = Math.max(1, ...hb);
      const { X, Y } = P.frame(g, W, H, [lo, hi], [0, 1.1], { xlabel: 'I（積分後）', ylabel: '次數（相對）', yticks: [] });
      hb.forEach((c, k) => { const x = lo + ((k + 0.5) / nb) * (hi - lo); g.fillStyle = x > thr * scale ? 'rgba(255,90,95,.75)' : 'rgba(79,140,255,.75)'; const bw = X(lo + (hi - lo) / nb) - X(lo); g.fillRect(X(x) - bw / 2 + 1, Y(c / mx), bw - 2, Y(0) - Y(c / mx)); });
      g.strokeStyle = '#ff6bd5'; g.lineWidth = 2; g.beginPath(); g.moveTo(X(thr * scale), Y(0)); g.lineTo(X(thr * scale), Y(1.1)); g.stroke();
      P.text(g, '閾值', X(thr * scale) + 4, Y(1.0), '#ff9be6');
    });

    return {
      update(t, dt) {
        const v = blochVec(); Bl.set(v[0], v[1], v[2], false);
        gL.set(basis === 'Z' ? '—' : basis === 'X' ? 'H' : 'S†H');
        thMesh.position.x = thr * scale;
        c0L.pos.set(IX + c0(), IY + 0.8, -1.4); c1L.pos.set(IX + c1(), IY + 0.8, -1.4);
        const ph = (t * 0.8) % 1; const px = -3.0 + ph * 7.6; pk.position.set(Math.min(2.6, px), px > 2.6 ? 1.5 - (px - 2.6) : 1.5, 0);
        res.material.emissiveIntensity = 0.25 + 0.4 * Math.max(0, Math.sin(t * 7));
        if (auto) { accum += dt * rate; while (accum >= 1) { accum--; shot(); } }
        const N = n0 + n1, raw = N ? n1 / N : 0, cf = confusion();
        const mit = U.clamp((raw - cf.p10) / Math.max(1e-6, cf.p11 - cf.p10), 0, 1);
        const est = mitig ? mit : raw;
        const pt = pTrue1();
        ro.innerHTML = `量測基底：${basis}${basis === 'Z' ? '' : `（先做 ${basis === 'X' ? 'H' : 'S†H'} 再量 Z）`}　理想 P(1) = ${pt.toFixed(3)}<br>` +
          `shots N = ${N}：0 → ${n0}，1 → ${n1}，原始 P̂(1) = ${raw.toFixed(3)}<br>` +
          `混淆矩陣：P(1|0) = ${(cf.p10 * 100).toFixed(1)}%，P(0|1) = ${(cf.p01 * 100).toFixed(1)}%，讀取保真度 F = ${((1 - (cf.p10 + cf.p01) / 2) * 100).toFixed(1)}%<br>` +
          `${mitig ? '緩解後' : '未緩解'} P̂(1) = <b>${est.toFixed(3)}</b>　→　⟨${basis}⟩ = ${(1 - 2 * est).toFixed(3)}（理想 ${(1 - 2 * pt).toFixed(3)}）`;
      },
    };
  },
});

/* 原子場景 10：芮德堡阻斷（Rydberg blockade）與 CZ 閘
 * 兩顆原子 + 共同雷射：H = Ω/2 Σ(|g⟩⟨r| + h.c.) + V(r)|rr⟩⟨rr|，V = C₆ / r⁶（數值精確演化：對角化 4×4 Hamiltonian）
 * 代表值：Ω/2π = 2 MHz，C₆/2π ≈ 858 GHz·μm⁶（⁸⁷Rb 70S 量級）→ 阻斷半徑 R_b = (C₆/Ω)^{1/6} ≈ 8.7 μm
 */
App.register({
  id: 'rydberg', num: 10, short: '芮德堡阻斷與 CZ 閘',
  title: '芮德堡阻斷：中性原子的兩位元閘',
  subtitle: '一顆原子被激發到芮德堡態後，附近的原子就無法再被激發 → 條件式相位 → CZ 閘',
  desc: `<p><b>芮德堡態</b>：把最外層電子激發到主量子數 n ≈ 50–100 的軌道，原子半徑變成約 n² 倍（數百 nm），偶極矩極大。兩顆芮德堡原子間的范德瓦耳斯交互作用 <span class="eq">V = C₆ / r⁶</span>，而 C₆ ∝ n¹¹。</p>
<p><b>阻斷（blockade）</b>：當 V ≫ ħΩ，|rr⟩ 被推離共振，兩顆原子最多只有一顆能被激發。系統只在 |gg⟩ ↔ (|gr⟩+|rg⟩)/√2 之間振盪，頻率變成 <b>√2 Ω</b>。阻斷半徑 <span class="eq">R<sub>b</sub> = (C₆/ħΩ)<sup>1/6</sup></span>，典型 5–10 μm，而光鑷間距只有 3–5 μm。</p>
<p><b>變成 CZ 閘</b>：只有 |1⟩ 被雷射耦合到 |r⟩。|11⟩ 被阻斷、|01⟩/|10⟩ 沒被阻斷，兩者經歷不同的動力學、累積不同的相位。Levine 等人（PRL 2019）用兩個脈衝 + 中間的雷射相位跳躍，讓所有態都回到原本的位置，且 φ₁₁ = 2φ₀₁ + π → 加上單位元 Z 修正就是 CZ。</p>
<p>閘時間約 0.2–0.5 μs；保真度 <b>99.5 %</b>（Evered et al., Nature 2023，60 顆原子並行），之後的實驗約 99.7 %。主要誤差：芮德堡態衰變、雷射相位雜訊、原子溫度（都卜勒失諧）。</p>
<p>拖動「原子間距」看阻斷消失：距離大時兩顆原子各自以 Ω 振盪，P(rr) 可以到 1。</p>`,
  camera: { pos: [2.4, 1.8, 11.5], target: [2.4, 0.0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const QC = App.QC;
    const TWO_PI = 2 * Math.PI;
    const Om = TWO_PI * 2; // rad/μs
    const C6 = TWO_PI * 858000; // rad/μs·μm⁶
    const Rb = Math.pow(C6 / Om, 1 / 6);
    const SC = 0.22; // 1 μm → 場景單位
    const TMAX = 1.0; // μs
    let r = 5; let tSim = 0; let running = true; let mode = 'blockade';
    const NT = 400;
    let curves = null;

    /* 精確演化：H 實對稱 → 對角化 */
    function solve() {
      const V = C6 / Math.pow(r, 6);
      const h = Om / 2;
      const H = [[0, h, h, 0], [h, 0, 0, h], [h, 0, 0, h], [0, h, h, V]];
      const { values: E, vectors: vec } = U.eigSym(H);
      const amp = (t) => { const out = [0, 1, 2, 3].map(() => [0, 0]); for (let k = 0; k < 4; k++) { const c = vec[k][0]; const ph = -E[k] * t; for (let j = 0; j < 4; j++) { out[j][0] += vec[k][j] * c * Math.cos(ph); out[j][1] += vec[k][j] * c * Math.sin(ph); } } return out.map(([a, b]) => a * a + b * b); };
      curves = { V, amp, gg: [], single: [], rr: [] };
      for (let i = 0; i <= NT; i++) { const P = amp((TMAX * i) / NT); curves.gg.push(P[0]); curves.single.push(P[1] + P[2]); curves.rr.push(P[3]); }
    }

    /* Levine 2019 協定：兩個脈衝（τ = 4.293/Ω、失諧 0.377Ω），中間雷射相位跳 ξ = 3.902 rad；用 RK4 數值演化二能階 */
    function levine() {
      const ev = (O, D, xi, tau, p) => {
        const n = 3000, dt = tau / n; let [ar, ai, br, bi] = p; const c = Math.cos(xi), s = Math.sin(xi);
        const f = (ar, ai, br, bi) => { const hr = (O / 2) * c, hi = (O / 2) * s; const Har = hr * br + hi * bi, Hai = hr * bi - hi * br; const Hbr = hr * ar - hi * ai + D * br, Hbi = hr * ai + hi * ar + D * bi; return [Hai, -Har, Hbi, -Hbr]; };
        for (let k = 0; k < n; k++) {
          const k1 = f(ar, ai, br, bi), k2 = f(ar + (dt / 2) * k1[0], ai + (dt / 2) * k1[1], br + (dt / 2) * k1[2], bi + (dt / 2) * k1[3]);
          const k3 = f(ar + (dt / 2) * k2[0], ai + (dt / 2) * k2[1], br + (dt / 2) * k2[2], bi + (dt / 2) * k2[3]), k4 = f(ar + dt * k3[0], ai + dt * k3[1], br + dt * k3[2], bi + dt * k3[3]);
          ar += (dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); ai += (dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
          br += (dt / 6) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]); bi += (dt / 6) * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]);
        }
        return [ar, ai, br, bi];
      };
      const res = {};
      [['01', 1], ['11', Math.SQRT2]].forEach(([k, f]) => { let p = ev(f, 0.377, 0, 4.293, [1, 0, 0, 0]); p = ev(f, 0.377, 3.902, 4.293, p); res[k] = { P: p[0] * p[0] + p[1] * p[1], ph: Math.atan2(p[1], p[0]) }; });
      const d = res['11'].ph - 2 * res['01'].ph; res.diff = ((d % TWO_PI) + TWO_PI) % TWO_PI;
      return res;
    }
    const LEV = levine();

    /* ---- 3D 物件 ---- */
    const A = App.particle(scene, QC.atom, 0.13), B = App.particle(scene, QC.atom, 0.13);
    const rydMat = () => new THREE.MeshStandardMaterial({ color: QC.ryd, transparent: true, opacity: 0, roughness: 0.3, emissive: QC.ryd, emissiveIntensity: 0.4, depthWrite: false });
    const rA = new THREE.Mesh(new THREE.SphereGeometry(0.5, 32, 20), rydMat()), rB = new THREE.Mesh(new THREE.SphereGeometry(0.5, 32, 20), rydMat());
    scene.add(rA, rB);
    // 電子軌道（環）示意
    const orbA = new THREE.Mesh(new THREE.TorusGeometry(0.5, 0.012, 6, 64), U.glow(QC.ryd, 0.6)), orbB = orbA.clone(); orbB.material = U.glow(QC.ryd, 0.6);
    scene.add(orbA, orbB);
    const block = new THREE.Mesh(new THREE.SphereGeometry(1, 40, 24), new THREE.MeshBasicMaterial({ color: 0x5ee08a, transparent: true, opacity: 0.08, depthWrite: false, side: THREE.DoubleSide }));
    block.scale.setScalar(Rb * SC); scene.add(block);
    const blockRing = new THREE.Mesh(new THREE.TorusGeometry(1, 0.012, 6, 96), U.glow(0x5ee08a, 0.7)); blockRing.scale.setScalar(Rb * SC); scene.add(blockRing);
    const bLbl = ctx.label('', [0, 0, 0], 'small');
    const lA = ctx.labelOn(A, '原子 A', [0, -0.45, 0], 'teal'), lB = ctx.labelOn(B, '原子 B', [0, -0.45, 0], 'teal');
    const dist = ctx.label('', [0, -1.25, 0], 'gold');
    const beamA = App.beam(scene, [-3.2, 0, 0], [4.4, 0, 0], App.wlColor(420), 0.09, 0.15);
    const beamB = App.beam(scene, [-3.2, 0.02, 0], [4.4, 0.02, 0], App.wlColor(1013), 0.06, 0.15);
    const bLabel = ctx.label('420 nm + 1013 nm 雙光子激發<br>（同時照兩顆原子）', [-2.0, 0.55, 0], 'small');
    const ruler = U.dynLine(2, 0xe0a54a); scene.add(ruler.obj);

    /* 能階圖（右側） */
    const LX = 5.6;
    const lvl = (y, w, col) => { const m = U.box(w, 0.05, 0.2, U.mat(col, { emissive: col, emissiveIntensity: 0.3 }), LX, y, 0); scene.add(m); return m; };
    lvl(-2.2, 1.6, QC.q0); lvl(-0.6, 1.6, 0xb49cff);
    const lrr0 = lvl(1.0, 1.6, 0x55617a); lrr0.material.transparent = true; lrr0.material.opacity = 0.35;
    const lrr = lvl(1.0, 1.6, QC.ryd);
    ctx.label('|gg⟩', [LX + 1.25, -2.2, 0], 'small');
    ctx.label('(|gr⟩+|rg⟩)/√2', [LX + 1.6, -0.6, 0], 'small');
    const lrrL = ctx.label('|rr⟩', [LX + 1.25, 1.0, 0], 'small');
    const a1 = U.fatArrow(0x7f5cff, 1, 0.03); a1.position.set(LX - 0.3, -2.2, 0); a1.setVec(new THREE.Vector3(0, 1.6, 0)); scene.add(a1);
    const a2 = U.fatArrow(0x7f5cff, 1, 0.03); a2.position.set(LX + 0.3, -0.6, 0); scene.add(a2);
    ctx.label('√2 Ω', [LX - 0.75, -1.4, 0], 'small');
    const a2L = ctx.label('', [LX + 0.75, 0.2, 0], 'small');
    const vL = ctx.label('', [LX, 3.6, 0], 'gold');
    ctx.label('雙原子能階', [LX, -2.9, 0], 'gold');

    function layout() {
      solve();
      const x = (r / 2) * SC;
      A.position.set(1.2 - x, 0, 0); B.position.set(1.2 + x, 0, 0);
      rA.position.copy(A.position); rB.position.copy(B.position); orbA.position.copy(A.position); orbB.position.copy(B.position);
      block.position.copy(A.position); blockRing.position.copy(A.position);
      const blocked = r < Rb;
      block.material.color.setHex(blocked ? 0x5ee08a : 0x9fb0c8); blockRing.material.color.setHex(blocked ? 0x5ee08a : 0x9fb0c8);
      bLbl.pos.set(A.position.x - Rb * SC * 0.55, Rb * SC * 0.92, 0); bLbl.set(`阻斷半徑 R_b ≈ ${Rb.toFixed(1)} μm`);
      dist.pos.set(1.2, -1.2, 0); dist.set(`間距 r = ${r.toFixed(1)} μm ${blocked ? '< R_b → <b>阻斷</b>' : '> R_b → 不阻斷'}`);
      ruler.set([[A.position.x, -0.9, 0], [B.position.x, -0.9, 0]]);
      const Vmhz = curves.V / TWO_PI;
      const shift = Math.min(2.2, Math.log10(1 + Vmhz / 2) * 1.0);
      lrr.position.y = 1.0 + shift; lrrL.pos.set(LX + 1.25, 1.0 + shift, 0);
      a2.setVec(new THREE.Vector3(0, 1.6, 0)); a2.position.set(LX + 0.3, -0.6, 0);
      a2.children.forEach((m) => m.material.color.setHex(blocked ? 0xff5a5f : 0x7f5cff));
      a2L.set(blocked ? '✗ 被推離共振' : '√2 Ω（共振）');
      vL.set(`V/h = C₆/r⁶ ≈ ${Vmhz >= 100 ? Vmhz.toFixed(0) : Vmhz.toFixed(2)} MHz（Ω/2π = 2 MHz）`);
    }

    ui.slider('原子間距 r (μm)', 2, 15, 0.5, r, (v) => { r = v; layout(); }, (v) => `${v.toFixed(1)} μm`);
    const r1 = ui.row();
    ui.button('▶ 雷射脈衝', () => { tSim = 0; running = true; mode = 'blockade'; mb.set('blockade'); }, r1);
    ui.button('⏸ 停止', () => { running = false; }, r1);
    const mb = ui.radio([['blockade', '阻斷動力學（數值演化）'], ['cz', 'CZ 協定（Levine 2019）']], 'blockade', (v) => { mode = v; });
    const ro = ui.readout();

    ctx.inset('布居數隨時間（Ω/2π = 2 MHz）', (g, W, H, P) => {
      if (mode === 'cz') {
        const { X, Y } = P.frame(g, W, H, [0, 2], [-0.2, 1.4], { xlabel: '時間（單位 τ = 4.293/Ω ≈ 0.34 μs）', xticks: [[0, '0'], [1, 'τ'], [2, '2τ']], m: { l: 20, b: 32 } });
        g.fillStyle = 'rgba(127,92,255,.55)'; g.fillRect(X(0.04), Y(0.9), X(0.96) - X(0.04), Y(0) - Y(0.9));
        g.fillStyle = 'rgba(255,106,213,.55)'; g.fillRect(X(1.04), Y(0.9), X(1.96) - X(1.04), Y(0) - Y(0.9));
        P.text(g, '脈衝 1：相位 0', X(0.5), Y(1.05), '#d6c8ff', 'center');
        P.text(g, '脈衝 2：相位 ξ = 3.902', X(1.5), Y(1.05), '#ffc6ef', 'center');
        P.text(g, '失諧 Δ = 0.377 Ω（兩個脈衝相同）', X(1), Y(1.28), '#ffd28a', 'center');
        P.text(g, '|11⟩ 每個脈衝走完一整圈（√2Ω）；|01⟩ 靠相位跳躍回到原點', X(1), Y(0.45), '#e8eef8', 'center');
        return;
      }
      const { X, Y } = P.frame(g, W, H, [0, TMAX], [0, 1], { xlabel: '時間 (μs)', xticks: [[0, '0'], [0.25, '0.25'], [0.5, '0.5'], [0.75, '0.75'], [1, '1']], yticks: [[0, '0'], [0.5, '0.5'], [1, '1']], m: { l: 34 } });
      const draw = (arr, col) => P.curve(g, (t) => arr[Math.round((t / TMAX) * NT)], 0, TMAX, X, Y, col, 2, NT);
      draw(curves.gg, '#4f8cff'); draw(curves.single, '#b49cff'); draw(curves.rr, '#ff6ad5');
      g.strokeStyle = 'rgba(255,210,138,.8)'; g.beginPath(); g.moveTo(X(tSim), Y(0)); g.lineTo(X(tSim), Y(1)); g.stroke();
      P.text(g, 'P(gg)', X(0.82), 22, '#a9c6ff'); P.text(g, 'P(單激發)', X(0.82), 38, '#d6c8ff'); P.text(g, 'P(rr)', X(0.82), 54, '#ff9fe6');
    });

    layout();
    return {
      update(t, dt) {
        if (running) { tSim += dt * 0.2; if (tSim > TMAX) tSim = 0; }
        const P = curves.amp(tSim);
        const pA = P[2] + P[3], pB = P[1] + P[3];
        rA.material.opacity = 0.05 + 0.4 * pA; rB.material.opacity = 0.05 + 0.4 * pB;
        orbA.material.opacity = 0.1 + 0.8 * pA; orbB.material.opacity = 0.1 + 0.8 * pB;
        orbA.rotation.set(t * 0.7, t * 1.1, 0); orbB.rotation.set(-t * 0.9, t * 0.6, 0);
        A.glow(0.3 + 0.7 * pA); B.glow(0.3 + 0.7 * pB);
        const on = running ? 0.12 + 0.08 * Math.sin(t * 20) : 0.04;
        beamA.material.opacity = on; beamB.material.opacity = on * 0.8;
        if (mode === 'cz') {
          ro.innerHTML = `<b>Levine 協定（RK4 數值演化）</b><br>|00⟩：不耦合 → 相位 0<br>|01⟩、|10⟩：回到原態機率 ${LEV['01'].P.toFixed(4)}，相位 φ₀₁ = ${LEV['01'].ph.toFixed(3)}<br>|11⟩：回到原態機率 ${LEV['11'].P.toFixed(4)}，相位 φ₁₁ = ${LEV['11'].ph.toFixed(3)}<br>φ₁₁ − 2φ₀₁ = <b>${LEV.diff.toFixed(3)} ≈ π</b> → 加上單位元 Z(−φ₀₁) 修正 = <b>CZ</b>`;
        } else {
          ro.innerHTML = `t = ${(tSim * 1000).toFixed(0)} ns · P(gg) = ${P[0].toFixed(2)} · P(單激發) = ${(P[1] + P[2]).toFixed(2)} · <b>P(rr) = ${P[3].toFixed(3)}</b><br>${r < Rb ? '阻斷：集體 Rabi 頻率 √2 Ω，雙激發被抑制' : '未阻斷：兩顆原子各自以 Ω 振盪，P(rr) 可達 1'}`;
        }
      },
    };
  },
});

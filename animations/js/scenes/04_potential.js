/* 場景 4：為什麼需要非線性？LC 諧振子 vs Transmon（JJ 餘弦位勢）的能階與波函數 */
App.register({
  id: 'potential', num: 4, short: '能階與非諧性',
  title: '非線性：從 LC 諧振子到 Transmon',
  subtitle: 'H = 4E_C(n − n_g)² − E_J cos φ',
  desc: `<p><b>LC 諧振子</b>的位勢是拋物線，能階<b>等間距</b>（ħω）。用頻率 ω 的微波驅動時，0→1、1→2、2→3… 全部同時共振，無法只操作兩個能階。</p>
<p>把電感換成 <b>JJ</b>，位勢變成 <b>−E_J cos φ</b>，越往上越「寬」，能階間距逐漸縮小 → <b>非諧性 α = ω₁₂ − ω₀₁ ≈ −E_C</b>。如此就能只選擇 |0⟩ 與 |1⟩ 當作量子位元。</p>
<p>調整 <b>E_J/E_C</b>：比值小（電荷量子位元）時能階對背景電荷 n_g 極敏感；比值大（transmon，約 50）時電荷色散指數級下降，但非諧性只以冪次減少。</p>`,
  camera: { pos: [0, 2.8, 12.5], target: [0, 2.6, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const EC = 0.25; // GHz
    let ratio = 50, mode = 'transmon';
    const XS = 4.6 / Math.PI; // φ → x
    const group = new THREE.Group(); scene.add(group);
    const levelColors = [0x4f8cff, 0xff5a5f, 0x2ecc71, 0xe0a54a, 0xb07cff];
    const lbls = [0, 1, 2, 3].map((k) => ctx.label('', [0, 0, 0], k === 0 ? 'q0' : k === 1 ? 'q1' : 'small'));
    const trLbls = [0, 1, 2].map(() => ctx.label('', [0, 0, 0], 'gold small'));
    const potLbl = ctx.label('', [-4.2, 6.2, 0], 'teal');
    ctx.label('相位 φ →', [5.4, -0.3, 0], 'small');
    ctx.label('−π', [-4.6, -0.4, 0], 'plain small'); ctx.label('0', [0, -0.4, 0], 'plain small'); ctx.label('π', [4.6, -0.4, 0], 'plain small');
    const ro = ui.readout();
    let bands = null;

    const hermite = (n, x) => { let h0 = 1, h1 = 2 * x; if (n === 0) return h0; for (let k = 1; k < n; k++) { const h2 = 2 * x * h1 - 2 * k * h0; h0 = h1; h1 = h2; } return h1; };

    function rebuild() {
      while (group.children.length) { const o = group.children.pop(); o.geometry && o.geometry.dispose(); }
      const EJ = ratio * EC;
      const Etop = Math.max(2 * EJ, 6 * EC);
      const ys = 5.6 / Etop; // 能量 → y
      const Upot = mode === 'lc' ? (p) => (EJ * p * p) / 2 : (p) => EJ * (1 - Math.cos(p));
      // 位勢曲面（沿 z 擠出）
      const NX = 160, NZ = 2, depth = 2.2;
      const geo = new THREE.BufferGeometry(); const pos = []; const idx = [];
      for (let i = 0; i <= NX; i++) {
        const p = -Math.PI + (2 * Math.PI * i) / NX; const y = Math.min(6.4, Upot(p) * ys);
        for (let k = 0; k <= NZ; k++) pos.push(p * XS, y, -depth + (depth * k) / NZ);
      }
      for (let i = 0; i < NX; i++) for (let k = 0; k < NZ; k++) {
        const a = i * (NZ + 1) + k, b = a + NZ + 1;
        idx.push(a, b, a + 1, b, b + 1, a + 1);
      }
      geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setIndex(idx); geo.computeVertexNormals();
      group.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: mode === 'lc' ? 0x3b6fd8 : 0x1c9db0, side: THREE.DoubleSide, transparent: true, opacity: 0.35, roughness: 0.4 })));
      const front = []; for (let i = 0; i <= NX; i++) { const p = -Math.PI + (2 * Math.PI * i) / NX; front.push([p * XS, Math.min(6.4, Upot(p) * ys), 0]); }
      group.add(U.tube(front, 0.04, U.mat(mode === 'lc' ? 0x8ab4ff : 0x38c6d9, { emissive: 0x0a3a44, emissiveIntensity: 0.6 }), false, 1));

      // 能階
      let E = [], psi = [];
      if (mode === 'lc') {
        const w = Math.sqrt(8 * EJ * EC);
        const pz = Math.pow((2 * EC) / EJ, 0.25);
        for (let n = 0; n < 5; n++) {
          E.push(w * (n + 0.5));
          psi.push((p) => hermite(n, p / pz) * Math.exp(-(p * p) / (2 * pz * pz)));
        }
      } else {
        const r = U.transmon(EJ, EC, 0, 14);
        for (let m = 0; m < 5; m++) {
          E.push(r.values[m] + EJ);
          const c = r.vectors[m];
          let dEven = 0, dOdd = 0;
          for (let n = 1; n <= 14; n++) { dEven += Math.abs(c[14 + n] - c[14 - n]); dOdd += Math.abs(c[14 + n] + c[14 - n]); }
          const even = dEven < dOdd;
          psi.push((p) => { let s = 0; c.forEach((cn, i) => { const n = i - 14; s += cn * (even ? Math.cos(n * p) : Math.sin(n * p)); }); return s; });
        }
        // 電荷色散（n_g 掃描）
        bands = [];
        for (let k = 0; k <= 60; k++) {
          const ng = -1 + (2 * k) / 60;
          const rr = U.transmon(EJ, EC, ng, 10);
          bands.push([ng, rr.values[0], rr.values[1], rr.values[2]]);
        }
      }
      const shown = E.filter((e) => e * ys < 6.3).length;
      for (let m = 0; m < Math.min(5, shown); m++) {
        const y = E[m] * ys;
        // 能階線（只畫在位勢內側）
        let pL = -Math.PI, pR = Math.PI;
        for (let i = 0; i <= 400; i++) { const p = -Math.PI + (Math.PI * i) / 400; if (Upot(p) <= E[m]) { pL = p; break; } }
        pR = -pL;
        group.add(U.line([[pL * XS, y, 0.01], [pR * XS, y, 0.01]], levelColors[m], 0.95));
        group.add(U.line([[pL * XS, y, -depth], [pR * XS, y, -depth]], levelColors[m], 0.25));
        // 波函數
        let maxA = 0; const samples = [];
        for (let i = 0; i <= 240; i++) { const p = -Math.PI + (2 * Math.PI * i) / 240; const v = psi[m](p); samples.push([p, v]); maxA = Math.max(maxA, Math.abs(v)); }
        const amp = Math.min(0.55, (E[1] - E[0]) * ys * 0.32);
        const pts = samples.map(([p, v]) => [p * XS, y + (v / maxA) * amp, 0.03]);
        group.add(U.tube(pts, 0.022, U.glow(levelColors[m]), false, 1));
      }
      for (let m = 0; m < 4; m++) {
        if (m < shown) { lbls[m].show(true); lbls[m].pos.set(-5.6, E[m] * ys, 0); lbls[m].set(`|${m}⟩`); }
        else lbls[m].show(false);
      }
      // 躍遷頻率
      const f = [E[1] - E[0], E[2] - E[1], E[3] - E[2]];
      for (let k = 0; k < 3; k++) {
        if (k + 1 < shown) {
          trLbls[k].show(true);
          trLbls[k].pos.set(5.9, ((E[k] + E[k + 1]) / 2) * ys, 0);
          trLbls[k].set(`ω${k}${k + 1}/2π = ${f[k].toFixed(2)} GHz`);
          const a = U.arrow([0, 1, 0], [4.9, E[k] * ys, 0], (E[k + 1] - E[k]) * ys, levelColors[k + 1], 0.18, 0.1);
          group.add(a);
        } else trLbls[k].show(false);
      }
      potLbl.set(mode === 'lc' ? 'LC：U = φ² E_J / 2（拋物線）' : 'JJ：U = −E_J cos φ（餘弦）');
      const alpha = (f[1] - f[0]) * 1000;
      ro.innerHTML = `E_J/E_C = ${ratio.toFixed(1)}　（E_C/h = ${(EC * 1000).toFixed(0)} MHz, E_J/h = ${EJ.toFixed(2)} GHz）<br>` +
        `ω₀₁/2π = ${f[0].toFixed(3)} GHz　ω₁₂/2π = ${f[1].toFixed(3)} GHz<br>` +
        `非諧性 α/2π = ${alpha.toFixed(0)} MHz ${mode === 'lc' ? '（等間距 → 無法單獨定址）' : `（≈ −E_C = −${(EC * 1000).toFixed(0)} MHz）`}<br>` +
        `近似公式 √(8E_JE_C) − E_C = ${(Math.sqrt(8 * EJ * EC) - EC).toFixed(3)} GHz`;
    }
    ui.radio([['lc', 'LC 諧振子（線性）'], ['transmon', 'JJ / Transmon（非線性）']], mode, (m) => { mode = m; rebuild(); });
    const rs = ui.slider('E_J / E_C（對數刻度）', 0, 2, 0.01, Math.log10(ratio), (v) => { ratio = Math.pow(10, v); rebuild(); }, (v) => Math.pow(10, v).toFixed(1));
    ui.radio([[1, 'CPB：E_J/E_C = 1'], [10, '10'], [50, 'Transmon：50']], 50, (v) => rs.set(Math.log10(v)));

    ctx.inset('電荷色散：能階隨背景電荷 n_g 的變化', (g, W, H, P) => {
      if (!bands || mode === 'lc') { P.text(g, '（切換到 Transmon 模式以顯示）', W / 2, H / 2, '#9fb0c8', 'center'); return; }
      const e01 = bands[45][2] - bands[45][1];
      const y0 = bands[30][1];
      const yr = [-0.2, 2.6];
      const { X, Y } = P.frame(g, W, H, [-1, 1], yr, { xlabel: '背景電荷 n_g', ylabel: '(E − E₀)/E₀₁', xticks: [[-1, '-1'], [0, '0'], [1, '1']], yticks: [[0, '0'], [1, '1'], [2, '2']] });
      ['#4f8cff', '#ff5a5f', '#2ecc71'].forEach((c, k) => {
        g.strokeStyle = c; g.lineWidth = 2; g.beginPath();
        bands.forEach((b, i) => { const v = (b[k + 1] - y0) / e01; const yy = Y(Math.min(yr[1], Math.max(yr[0], v))); i ? g.lineTo(X(b[0]), yy) : g.moveTo(X(b[0]), yy); });
        g.stroke();
      });
    });
    rebuild();
    return { update() {} };
  },
});

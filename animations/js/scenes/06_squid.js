/* 場景 6：DC SQUID — 兩個 JJ 並聯成環，用外加磁通調整等效 E_J 與量子位元頻率 */
App.register({
  id: 'squid', num: 6, short: 'SQUID',
  title: 'DC SQUID：可用磁通調整的 JJ',
  subtitle: 'E_J(Φ) = E_JΣ |cos(πΦ/Φ₀)| √(1 + d² tan²(πΦ/Φ₀))',
  desc: `<p>把兩個 JJ 並聯成一個超導環，穿過環的磁通 Φ 會讓兩個 JJ 的相位差產生干涉。整個 SQUID 就像<b>一個臨界電流可調的 JJ</b>。</p>
<p>由於<b>磁通量子化</b>（Φ₀ = h/2e ≈ 2.07 × 10⁻¹⁵ Wb），E_J 隨 Φ 以 Φ₀ 為週期變化。在晶片上用一條 <b>Z 控制線（flux line）</b>通入電流，就能在數百 MHz 到 GHz 範圍內<b>即時調整量子位元頻率</b>，用來做雙量子位元閘或避開缺陷。</p>
<p><b>甜蜜點（sweet spot）</b>：Φ = 0 處 df/dΦ = 0，對磁通雜訊一階不敏感。<b>非對稱 SQUID</b>（d ≠ 0）可縮小調頻範圍、降低雜訊敏感度。</p>`,
  camera: { pos: [3.5, 2.5, 10], target: [0, 0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const R = 2.6, tubeR = 0.22;
    const alMat = U.metal(0xb9c4d4);
    // 環分成上下兩段（左右兩側為 JJ）
    const gap = 0.12;
    const topM = new THREE.Mesh(new THREE.TorusGeometry(R, tubeR, 16, 64, Math.PI - 2 * gap), alMat); topM.rotation.z = gap;
    const botM = new THREE.Mesh(new THREE.TorusGeometry(R, tubeR, 16, 64, Math.PI - 2 * gap), alMat); botM.rotation.z = Math.PI + gap;
    scene.add(topM, botM);
    const jjMat = new THREE.MeshStandardMaterial({ color: 0xff7a59, emissive: 0x6a1a00, emissiveIntensity: 0.8 });
    const jj1 = U.box(0.5, 0.16, 0.5, jjMat, R, 0, 0);
    const jj2 = U.box(0.5, 0.16, 0.5, jjMat.clone(), -R, 0, 0);
    scene.add(jj1, jj2);
    ctx.label('JJ₁', [R + 0.75, 0, 0], 'gold');
    ctx.label('JJ₂', [-R - 0.75, 0, 0], 'gold');
    // 引線
    scene.add(U.tube([[0, R, 0], [0, R + 1.6, 0]], 0.16, alMat), U.tube([[0, -R, 0], [0, -R - 1.6, 0]], 0.16, alMat));
    ctx.label('接到 transmon 電容板 / 地', [0, R + 2.0, 0], 'small');
    // Z 控制線（flux line）
    const fl = U.tube([[-4.6, -R - 0.9, 0.6], [-1.2, -R - 0.9, 0.6], [-1.2, -R - 0.4, 0.6], [1.2, -R - 0.4, 0.6], [1.2, -R - 0.9, 0.6], [4.6, -R - 0.9, 0.6]], 0.08, U.metal(0xd8a24a));
    scene.add(fl);
    ctx.label('Z 控制線（磁通偏壓）', [3.6, -R - 1.4, 0.6], 'teal small');

    // 磁場箭頭陣列（沿 +z 穿過環）
    const arrows = [];
    for (let i = -2; i <= 2; i++) for (let j = -2; j <= 2; j++) {
      const x = i * 0.85, y = j * 0.85; if (x * x + y * y > (R - 0.5) ** 2) continue;
      const a = U.fatArrow(0x7fdcff, 1.8, 0.03); a.position.set(x, y, -0.9); scene.add(a); arrows.push(a);
    }
    const phiLbl = ctx.label('', [0, 0, 1.6], 'big teal');
    // 環流（屏蔽電流）粒子
    const NP = 28; const parts = [];
    for (let k = 0; k < NP; k++) { const s = U.sphere(0.07, U.glow(0xffd28a)); scene.add(s); parts.push({ s, a: (k / NP) * Math.PI * 2 }); }

    const EC = 0.25, EJS = 20;
    let flux = 0.25, d = 0.0;
    const f01 = (F, dd) => {
      const c = Math.cos(Math.PI * F), s = Math.sin(Math.PI * F);
      const EJ = EJS * Math.sqrt(c * c + dd * dd * s * s);
      return Math.sqrt(8 * EJ * EC) - EC;
    };
    ui.slider('外加磁通 Φ / Φ₀', -1, 1, 0.005, flux, (v) => { flux = v; }, (v) => v.toFixed(3));
    ui.slider('接面不對稱度 d = (E_J1 − E_J2)/(E_J1 + E_J2)', 0, 0.8, 0.01, d, (v) => { d = v; }, (v) => v.toFixed(2));
    let sweep = false;
    ui.toggle('自動掃描磁通', false, (on) => { sweep = on; });
    const ro = ui.readout();

    ctx.inset('量子位元頻率 f₀₁ 與外加磁通（E_JΣ/h = 20 GHz, E_C/h = 250 MHz）', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [-1, 1], [0, 6.5], { xlabel: 'Φ / Φ₀', ylabel: 'f₀₁ (GHz)', xticks: [[-1, '-1'], [-0.5, '-½'], [0, '0'], [0.5, '½'], [1, '1']], yticks: [[0, '0'], [2, '2'], [4, '4'], [6, '6']] });
      P.curve(g, (F) => Math.max(0, f01(F, 0)), -1, 1, X, Y, 'rgba(159,176,200,.6)', 1.5, 400);
      P.curve(g, (F) => Math.max(0, f01(F, d)), -1, 1, X, Y, '#e0a54a', 2.5, 400);
      P.dot(g, X(flux), Y(Math.max(0, f01(flux, d))), 6, '#38c6d9');
      P.text(g, '甜蜜點', X(0), Y(f01(0, d)) - 8, '#8ef0ff', 'center');
    });

    return {
      update(time, dt) {
        if (sweep) { flux = Math.sin(time * 0.35); }
        const F = flux;
        arrows.forEach((a) => { a.setVec(new THREE.Vector3(0, 0, 1.8 * F)); a.position.z = F >= 0 ? -0.9 : 0.9; a.children.forEach((m) => { m.material.opacity = Math.min(1, Math.abs(F) * 2 + 0.05); m.material.transparent = true; }); });
        // 屏蔽電流方向與大小 ∝ sin(πΦ/Φ₀)（示意）
        const J = Math.sin(Math.PI * F);
        parts.forEach((p) => {
          p.a += dt * 2.2 * J;
          p.s.position.set(R * Math.cos(p.a), R * Math.sin(p.a), 0.0);
          p.s.visible = Math.abs(J) > 0.03;
        });
        const c = Math.cos(Math.PI * F), s = Math.sin(Math.PI * F);
        const EJ = EJS * Math.sqrt(c * c + d * d * s * s);
        jj1.material.emissiveIntensity = jj2.material.emissiveIntensity = 0.3 + 0.9 * (EJ / EJS);
        phiLbl.set(`Φ = ${F.toFixed(2)} Φ₀`);
        const df = (f01(F + 1e-3, d) - f01(F - 1e-3, d)) / 2e-3;
        ro.innerHTML = `等效 E_J/h = ${EJ.toFixed(2)} GHz（E_J/E_C = ${(EJ / EC).toFixed(0)}）<br>f₀₁ ≈ √(8E_JE_C) − E_C = <b>${Math.max(0, f01(F, d)).toFixed(3)} GHz</b><br>磁通敏感度 df/dΦ = ${(df).toFixed(2)} GHz/Φ₀ ${Math.abs(df) < 0.05 ? '（甜蜜點：對磁通雜訊一階免疫）' : ''}`;
      },
    };
  },
});

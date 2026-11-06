/* 場景 9：色散讀取 — 量子位元狀態使諧振腔頻率偏移 ±χ，探測微波的振幅/相位隨之改變 */
App.register({
  id: 'dispersive', num: 9, short: '色散讀取',
  title: '色散讀取：用諧振腔頻率「看見」量子位元',
  subtitle: 'H ≈ ħ(ω_r + χσ_z) a†a + ½ħω_q σ_z ，χ = g²α / [Δ(Δ+α)]',
  desc: `<p>量子位元與諧振腔<b>失諧很大</b>（|Δ| = |ω_q − ω_r| ≫ g）時不交換能量，只互相「推」頻率：諧振腔頻率變成 <b>ω_r ± χ</b>，正負號取決於量子位元在 |0⟩ 或 |1⟩。</p>
<p>在兩個頻率中間送入一個<b>探測微波</b>，穿透出來的訊號<b>相位</b>（和振幅）就會因量子位元狀態不同而不同 → 不需直接碰觸量子位元就能讀出狀態（<b>QND 量測</b>）。</p>
<p>右下角是複數平面（IQ 平面）：掃頻時 S21 畫出一個圓；兩個狀態在探測頻率下的點分得越開，讀取越容易。當 <b>2χ ≈ κ</b> 時分離最佳。</p>`,
  camera: { pos: [0, 5, 17], target: [0, 3.4, -2] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const SX = 0.75; // 每 κ 的 x 長度
    const FR = 6; // ±6κ
    let chi = 0.5, probe = 0, state = 0, auto = true, shown = 0;
    // 座標面
    const grid = new THREE.GridHelper(12, 12, 0x2c3a52, 0x1b2638); grid.position.set(0, 0, -1.5); grid.scale.z = 0.5; scene.add(grid);
    ctx.label('探測頻率 ω − ω_r（以 κ 為單位）→', [4.2, -0.4, 0.6], 'small');
    ctx.label('振幅 |S21|', [-5.6, 3.2, 0], 'small');
    ctx.label('相位 arg S21', [-5.6, 4.9, -4], 'small');
    const amp = (f, fs) => 1 / Math.sqrt(1 + 4 * (f - fs) ** 2);
    const pha = (f, fs) => -Math.atan(2 * (f - fs));
    const mk = (n, col) => { const l = U.dynLine(n, col); scene.add(l.obj); return l; };
    const curves = { a0: mk(400, 0x4f8cff), a1: mk(400, 0xff5a5f), p0: mk(400, 0x4f8cff), p1: mk(400, 0xff5a5f) };
    // 曲線下方填色（ribbon）
    const ribbonMat0 = new THREE.MeshBasicMaterial({ color: 0x4f8cff, transparent: true, opacity: 0.18, side: THREE.DoubleSide, depthWrite: false });
    const ribbonMat1 = new THREE.MeshBasicMaterial({ color: 0xff5a5f, transparent: true, opacity: 0.18, side: THREE.DoubleSide, depthWrite: false });
    const mkRibbon = (mat) => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(401 * 2 * 3), 3)); const idx = []; for (let i = 0; i < 400; i++) { idx.push(2 * i, 2 * i + 2, 2 * i + 1, 2 * i + 1, 2 * i + 2, 2 * i + 3); } g.setIndex(idx); const m = new THREE.Mesh(g, mat); m.frustumCulled = false; scene.add(m); return g; };
    const rib0 = mkRibbon(ribbonMat0), rib1 = mkRibbon(ribbonMat1);
    const probeLine = U.dynLine(2, 0xe0a54a); scene.add(probeLine.obj);
    const pDot0 = U.sphere(0.12, U.glow(0x4f8cff)), pDot1 = U.sphere(0.12, U.glow(0xff5a5f));
    const qDot0 = U.sphere(0.12, U.glow(0x4f8cff)), qDot1 = U.sphere(0.12, U.glow(0xff5a5f));
    scene.add(pDot0, pDot1, qDot0, qDot1);
    const l0 = ctx.label('|0⟩：ω_r − χ', [0, 0, 0], 'q0'), l1 = ctx.label('|1⟩：ω_r + χ', [0, 0, 0], 'q1');
    const prL = ctx.label('探測微波', [0, 0, 0], 'gold');
    const AY = 3.0, PY = 4.9, PZ = -4;
    scene.add(U.line([[-4.6, PY, PZ], [4.6, PY, PZ]], 0x3a4a66), U.line([[-4.6, PY - 1.45, PZ], [-4.6, PY + 1.45, PZ]], 0x3a4a66));

    // 諧振腔與駐波（上方示意）
    const RY = 8.0;
    scene.add(U.tube([[-4, RY, -4], [4, RY, -4]], 0.07, U.metal(0xd6dde8)));
    const qubit = U.sphere(0.32, U.mat(0x4f8cff, { emissive: 0x4f8cff, emissiveIntensity: 0.6 }), 4.5, RY, -4); scene.add(qubit);
    const wave = U.dynLine(200, 0x8ef0ff); scene.add(wave.obj);
    const wave2 = U.dynLine(200, 0x8ef0ff, 0.35); scene.add(wave2.obj);
    ctx.label('λ/4 諧振腔內的駐波（振幅 ∝ 腔內光子數）', [-1, RY + 1.3, -4], 'teal small');
    const qL = ctx.labelOn(qubit, '量子位元', [0, 0.65, 0], 'small');

    const toX = (f) => f * SX;
    function rebuild() {
      const f0 = -chi, f1 = chi;
      const A0 = [], A1 = [], P0 = [], P1 = [];
      const r0 = rib0.attributes.position.array, r1 = rib1.attributes.position.array;
      for (let i = 0; i <= 399; i++) {
        const f = -FR + (2 * FR * i) / 399;
        A0.push([toX(f), AY * amp(f, f0), 0]); A1.push([toX(f), AY * amp(f, f1), 0.02]);
        P0.push([toX(f), PY + 0.9 * pha(f, f0), PZ]); P1.push([toX(f), PY + 0.9 * pha(f, f1), PZ + 0.02]);
        r0.set([toX(f), 0, 0, toX(f), AY * amp(f, f0), 0], 6 * i); r1.set([toX(f), 0, 0.02, toX(f), AY * amp(f, f1), 0.02], 6 * i);
      }
      curves.a0.set(A0); curves.a1.set(A1); curves.p0.set(P0); curves.p1.set(P1);
      rib0.attributes.position.needsUpdate = true; rib1.attributes.position.needsUpdate = true;
      l0.pos.set(toX(f0) - 0.8, AY + 0.45, 0); l1.pos.set(toX(f1) + 0.8, AY + 0.45, 0);
      const x = toX(probe);
      probeLine.set([[x, -0.2, 0.5], [x, PY + 1.6, PZ]]);
      prL.pos.set(x, AY + 1.25, 0);
      pDot0.position.set(x, AY * amp(probe, f0), 0); pDot1.position.set(x, AY * amp(probe, f1), 0.02);
      qDot0.position.set(x, PY + 0.9 * pha(probe, f0), PZ); qDot1.position.set(x, PY + 0.9 * pha(probe, f1), PZ);
    }
    ui.radio([[0, '量子位元 |0⟩'], [1, '量子位元 |1⟩']], 0, (v) => { state = v; auto = false; autoB.classList.remove('on'); });
    const autoB = ui.toggle('自動切換 |0⟩ ↔ |1⟩', true, (on) => { auto = on; });
    ui.slider('色散位移 χ / κ', 0.05, 2, 0.01, chi, (v) => { chi = v; rebuild(); }, (v) => v.toFixed(2));
    ui.slider('探測頻率 (ω − ω_r) / κ', -3, 3, 0.01, probe, (v) => { probe = v; rebuild(); }, (v) => v.toFixed(2));
    const ro = ui.readout();
    rebuild();

    const S = (f, fs) => { const d = 2 * (f - fs); return [1 / (1 + d * d), -d / (1 + d * d)]; }; // (κ/2)/(i(ω−ω_s)+κ/2)
    ctx.inset('IQ 平面：S21 = (κ/2) / [i(ω − ω_s) + κ/2]', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [-0.2, 1.2], [-0.62, 0.62], { xlabel: 'I = Re S21', ylabel: 'Q = Im S21', xticks: [[0, '0'], [0.5, '0.5'], [1, '1']], yticks: [[-0.5, '-0.5'], [0, '0'], [0.5, '0.5']], m: { l: 46 } });
      [[-chi, '#4f8cff'], [chi, '#ff5a5f']].forEach(([fs, c]) => {
        g.strokeStyle = c; g.globalAlpha = 0.6; g.lineWidth = 1.5; g.beginPath();
        for (let i = 0; i <= 200; i++) { const f = -8 + (16 * i) / 200; const [a, b] = S(f, fs); i ? g.lineTo(X(a), Y(b)) : g.moveTo(X(a), Y(b)); }
        g.stroke(); g.globalAlpha = 1;
      });
      const s0 = S(probe, -chi), s1 = S(probe, chi);
      g.strokeStyle = '#e0a54a'; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(X(s0[0]), Y(s0[1])); g.lineTo(X(s1[0]), Y(s1[1])); g.stroke(); g.setLineDash([]);
      P.dot(g, X(s0[0]), Y(s0[1]), state === 0 ? 8 : 5, '#4f8cff'); P.dot(g, X(s1[0]), Y(s1[1]), state === 1 ? 8 : 5, '#ff5a5f');
    });

    let tAuto = 0;
    return {
      update(time, dt) {
        if (auto) { tAuto += dt; if (tAuto > 3) { tAuto = 0; state ^= 1; } }
        shown += (state - shown) * Math.min(1, dt * 5);
        ribbonMat0.opacity = 0.05 + 0.3 * (1 - shown); ribbonMat1.opacity = 0.05 + 0.3 * shown;
        curves.a0.obj.material.opacity = 0.35 + 0.65 * (1 - shown); curves.a0.obj.material.transparent = true;
        curves.a1.obj.material.opacity = 0.35 + 0.65 * shown; curves.a1.obj.material.transparent = true;
        qubit.material.color.setHex(state ? 0xff5a5f : 0x4f8cff); qubit.material.emissive.setHex(state ? 0xff5a5f : 0x4f8cff);
        qL.set(`量子位元 |${state}⟩`);
        // 駐波：振幅 = 目前狀態下探測頻率處的響應
        const fs = state ? chi : -chi; const A = amp(probe, fs) * 1.1;
        const ph = pha(probe, fs);
        const pts = [], pts2 = [];
        for (let i = 0; i < 200; i++) {
          const x = -4 + (8 * i) / 199; const env = Math.sin(((x + 4) / 8) * (Math.PI / 2));
          pts.push([x, RY + A * env * Math.cos(time * 8 + ph), -4]); pts2.push([x, RY - A * env * Math.cos(time * 8 + ph), -4]);
        }
        wave.set(pts); wave2.set(pts2);
        const s0 = S(probe, -chi), s1 = S(probe, chi);
        const sep = Math.hypot(s0[0] - s1[0], s0[1] - s1[1]);
        const dphi = (pha(probe, chi) - pha(probe, -chi)) * 180 / Math.PI;
        ro.innerHTML = `兩狀態相位差 Δθ = ${Math.abs(dphi).toFixed(1)}°<br>IQ 分離距離 |S₀ − S₁| = ${sep.toFixed(3)}（最大值 1 出現在 2χ = κ、探測於中點）<br>目前 2χ/κ = ${(2 * chi).toFixed(2)} ${Math.abs(2 * chi - 1) < 0.08 ? '✓ 最佳' : ''}`;
      },
    };
  },
});

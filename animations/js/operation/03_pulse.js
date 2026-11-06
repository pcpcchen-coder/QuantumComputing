/* 場景 3：量子閘的物理實現 — 微波脈衝的振幅、相位、長度、失諧、DRAG 與虛擬 Z */
App.register({
  id: 'pulse', num: 3, short: '微波脈衝',
  title: '閘怎麼做出來？微波脈衝',
  subtitle: '振幅×時間 = 旋轉角；相位 = 旋轉軸；頻率要對準 f₀₁',
  desc: `<p>對 transmon 送一段頻率等於 f<sub>01</sub>（約 5 GHz）的微波脈衝，在「旋轉座標」下狀態就會繞 xy 平面上的一條軸旋轉：</p>
<p><b>脈衝面積</b>（振幅 × 時間）決定旋轉角：面積 π → X 閘；π/2 → √X。<b>脈衝相位 φ</b> 決定旋轉軸：0° → 繞 x，90° → 繞 y。</p>
<p><b>失諧</b>（頻率沒對準）會讓旋轉軸往 z 傾斜，轉不到南極 → 閘錯誤，所以要先用 Ramsey 實驗校準頻率。</p>
<p><b>脈衝形狀</b>：方波的頻譜很寬，會打到 |1⟩→|2⟩ 躍遷（f<sub>12</sub> ≈ f<sub>01</sub> − 220 MHz）造成「洩漏」；高斯脈衝較窄；<b>DRAG</b> 在 Q 通道加上導數項，在 f<sub>12</sub> 挖出零點。</p>
<p><b>虛擬 Z 閘</b>：不送任何脈衝，只把之後所有脈衝的相位平移 —— 零時間、零誤差。</p>`,
  camera: { pos: [0.6, 2.4, 11.0], target: [0.6, 0.4, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const Bl = App.Bloch(ctx, { r: 1.35, pos: [4.0, 1.0, 0], trailN: 700, title: '旋轉座標中的量子位元' });
    // 晶片與 transmon（十字形）
    const chip = new THREE.Group(); chip.position.set(1.2, -2.0, 0); scene.add(chip);
    chip.add(U.box(3.2, 0.08, 2.0, U.mat(0x8c96a8, { metalness: 0.6, roughness: 0.35 })));
    const xm = U.mat(0xd6c9a0, { metalness: 0.8, roughness: 0.25, emissive: 0xe0a54a, emissiveIntensity: 0 });
    chip.add(U.box(1.2, 0.06, 0.18, xm, 0, 0.07, 0), U.box(0.18, 0.06, 1.2, xm, 0, 0.07, 0));
    ctx.label('transmon（f₀₁ ≈ 5 GHz）', [1.2, -1.35, 1.1], 'small');
    // 驅動線（同軸）
    const lineP = [[-3.8, -1.4, 0], [-1.4, -1.4, 0], [0.0, -1.93, 0], [0.6, -1.93, 0]];
    scene.add(U.tube(lineP, 0.05, U.metal(0xb87333)));
    ctx.label('XY 驅動線', [-2.4, -1.15, 0], 'gold small');
    const blob = U.sphere(0.13, U.glow(0xffd28a)); scene.add(blob); blob.visible = false;
    // 波形（3D：x = 時間，y = I，z = Q）
    const wf = new THREE.Group(); wf.position.set(-2.2, 1.2, 0); scene.add(wf);
    wf.add(U.line([[-1.8, 0, 0], [1.8, 0, 0]], 0x6f8fbf, 0.6));
    wf.add(U.line([[-1.8, -1.2, 0], [-1.8, 1.4, 0]], 0x6f8fbf, 0.4));
    wf.add(U.line([[-1.8, 0, -1.0], [-1.8, 0, 1.0]], 0x6f8fbf, 0.4));
    ctx.label('I（同相）', [-4.0, 2.75, 0], 'gold small'); ctx.label('Q（正交）', [-4.0, 1.2, 1.25], 'teal small');
    ctx.label('時間 →', [-0.2, 0.95, 0], 'small');
    const NP = 240;
    const envL = U.dynLine(NP, 0xe0a54a), qL = U.dynLine(NP, 0x38c6d9), carL = U.dynLine(NP * 4, 0xffffff, 0.35);
    wf.add(envL.obj, qL.obj, carL.obj);
    const cursor = U.box(0.02, 2.4, 0.02, U.glow(0xff6bd5), 0, 0.1, 0); wf.add(cursor); cursor.visible = false;
    ctx.label('白線 = 實際送出的微波（包絡 × 載波，示意）', [-2.2, -0.35, 0], 'small');

    let shape = 'gauss', area = 180, phase = 0, detMHz = 0, Tg = 40, frame = 0;
    const ALPHA = -0.22; // 非諧性 GHz（f12 − f01）
    const env = (t) => { // t ∈ [0, Tg]（ns），回傳未正規化的 I
      if (shape === 'square') return 1;
      const s = Tg / 4, x = t - Tg / 2;
      return Math.exp(-(x * x) / (2 * s * s)) - Math.exp(-(Tg * Tg) / (8 * s * s));
    };
    const dEnv = (t) => (env(t + 0.01) - env(t - 0.01)) / 0.02;
    const beta = 1 / (2 * Math.PI * ALPHA); // ns，使頻譜在 f12 處為零
    let wave = []; // [{t, I, Q}]，I 單位 rad/ns
    const build = () => {
      const n = 400, dt = Tg / n; let s = 0;
      const raw = [];
      for (let i = 0; i <= n; i++) { const t = i * dt; raw.push([t, env(t), shape === 'drag' ? beta * dEnv(t) : 0]); s += env(t) * dt; }
      const k = ((area * Math.PI) / 180) / (s || 1);
      wave = raw.map(([t, I, Q]) => ({ t, I: I * k, Q: Q * k }));
      const pk = Math.max(1e-9, ...wave.map((w) => Math.abs(w.I)));
      const X = (t) => -1.8 + (3.6 * t) / Tg;
      const sc = 1.1 / Math.max(pk, (Math.PI / 20) * 1.0);
      envL.set(wave.filter((_, i) => i % 2 === 0).slice(0, NP).map((w) => [X(w.t), w.I * sc, w.Q * sc * 6]));
      qL.set(wave.filter((_, i) => i % 2 === 0).slice(0, NP).map((w) => [X(w.t), 0, w.Q * sc * 6]));
      const car = []; const Ncar = NP * 4;
      for (let i = 0; i < Ncar; i++) { const t = (i / (Ncar - 1)) * Tg; const j = Math.min(wave.length - 1, Math.round((t / Tg) * (wave.length - 1))); const w = wave[j]; const ph = 2 * Math.PI * 14 * (t / Tg) + ((phase - frame) * Math.PI) / 180; car.push([X(t), (w.I * Math.cos(ph) - w.Q * Math.sin(ph)) * sc, 0]); }
      carL.set(car);
    };
    build();
    // 頻譜（相對 f01）
    const spec = (f) => { let re = 0, im = 0; const dt = Tg / (wave.length - 1); for (const w of wave) { const a = -2 * Math.PI * f * w.t; re += (w.I * Math.cos(a) - w.Q * Math.sin(a)) * dt; im += (w.I * Math.sin(a) + w.Q * Math.cos(a)) * dt; } return Math.hypot(re, im); };

    let play = null, v = [0, 0, 1];
    const startPulse = () => { play = { k: 0, v: v.slice() }; blob.visible = true; Bl.showAxis(null); };
    ui.radio([['square', '方波'], ['gauss', '高斯'], ['drag', '高斯 + DRAG']], shape, (s) => { shape = s; build(); });
    ui.slider('脈衝面積 → 旋轉角', 0, 360, 5, area, (x) => { area = x; build(); }, (x) => x + '°' + (x === 180 ? '（π：X 閘）' : x === 90 ? '（π/2：√X）' : ''));
    ui.slider('脈衝相位 φ → 旋轉軸方向', 0, 355, 5, phase, (x) => { phase = x; build(); }, (x) => x + '°' + (x === 0 ? '（x 軸）' : x === 90 ? '（y 軸）' : ''));
    ui.slider('頻率失諧 Δ（MHz）', -20, 20, 0.5, detMHz, (x) => { detMHz = x; }, (x) => x.toFixed(1) + ' MHz');
    ui.slider('閘長度（ns）', 10, 80, 2, Tg, (x) => { Tg = x; build(); }, (x) => x + ' ns');
    const r = ui.row();
    ui.button('▶ 送出脈衝', startPulse, r);
    ui.button('虛擬 Z（90°）', () => { frame = (frame + 90) % 360; v = App.rotVec(v, [0, 0, 1], Math.PI / 2); build(); }, r);
    ui.button('重設 |0⟩', () => { v = [0, 0, 1]; frame = 0; Bl.clearTrail(); build(); }, r);
    const ro = ui.readout();

    ctx.inset('上：I/Q 包絡（ns）　下：頻譜與 f₁₂ 洩漏', (g, W, H, P) => {
      const top = P.frame(g, W, 110, [0, Tg], [-0.4, 1.1], { m: { l: 40, b: 18, t: 8 }, yticks: [[0, '0'], [1, '1']] });
      const pk = Math.max(1e-9, ...wave.map((w) => Math.abs(w.I)));
      g.lineWidth = 2; g.strokeStyle = '#e0a54a'; g.beginPath(); wave.forEach((w, i) => (i ? g.lineTo(top.X(w.t), top.Y(w.I / pk)) : g.moveTo(top.X(w.t), top.Y(w.I / pk)))); g.stroke();
      g.strokeStyle = '#38c6d9'; g.beginPath(); wave.forEach((w, i) => (i ? g.lineTo(top.X(w.t), top.Y((w.Q / pk) * 3)) : g.moveTo(top.X(w.t), top.Y((w.Q / pk) * 3)))); g.stroke();
      P.text(g, 'I', W - 20, 24, '#e0a54a'); P.text(g, 'Q×3', W - 40, 44, '#38c6d9');
      if (play) { g.strokeStyle = '#ff6bd5'; const x = top.X(play.k * Tg); g.beginPath(); g.moveTo(x, 8); g.lineTo(x, 92); g.stroke(); }
      g.save(); g.translate(0, 112);
      const fr = [-0.4, 0.2], s0 = spec(0) || 1;
      const db = (f) => Math.max(-60, 20 * Math.log10((spec(f) || 1e-9) / s0));
      const bot = P.frame(g, W, 118, fr, [-60, 0], { m: { l: 40, b: 30, t: 6 }, xlabel: '相對 f₀₁ 的頻率（GHz）', yticks: [[0, '0 dB'], [-60, '−60']], xticks: [[-0.4, '−0.4'], [-0.22, 'f₁₂'], [0, 'f₀₁'], [0.2, '+0.2']] });
      P.curve(g, db, fr[0], fr[1], bot.X, bot.Y, '#e0a54a', 1.6, 260);
      g.strokeStyle = '#ff5a5f'; g.setLineDash([3, 3]); g.beginPath(); g.moveTo(bot.X(ALPHA), bot.Y(0)); g.lineTo(bot.X(ALPHA), bot.Y(-60)); g.stroke(); g.setLineDash([]);
      P.text(g, `f₁₂ 處 ${db(ALPHA).toFixed(0)} dB`, bot.X(ALPHA) + 4, bot.Y(-50), '#ffb0b2');
      g.restore();
    });

    return {
      update(t, dt) {
        const dRad = 2 * Math.PI * detMHz * 1e-3; // rad/ns
        const ph = (phase * Math.PI) / 180;
        if (play) {
          const k1 = Math.min(1, play.k + dt / 1.6);
          const i0 = Math.floor(play.k * (wave.length - 1)), i1 = Math.floor(k1 * (wave.length - 1));
          const dts = Tg / (wave.length - 1);
          for (let i = i0; i < i1; i++) {
            const w = wave[i];
            const ox = w.I * Math.cos(ph) - w.Q * Math.sin(ph), oy = w.I * Math.sin(ph) + w.Q * Math.cos(ph);
            const om = Math.hypot(ox, oy, dRad);
            if (om > 1e-12) v = App.rotVec(v, [ox, oy, dRad], om * dts);
          }
          play.k = k1;
          const s = play.k;
          const pIdx = Math.min(lineP.length - 1, 1 + Math.floor(s * 2.999));
          blob.position.set(...lineP[0]).lerp(new THREE.Vector3(...lineP[3]), s);
          cursor.visible = true; cursor.position.x = -1.8 + 3.6 * s;
          const wi = wave[Math.min(wave.length - 1, Math.floor(s * (wave.length - 1)))];
          xm.emissiveIntensity = Math.min(1.2, Math.abs(wi.I) * 6);
          Bl.showAxis([Math.cos(ph), Math.sin(ph), dRad / Math.max(1e-6, (area * Math.PI) / 180 / Tg)]);
          if (play.k >= 1) { play = null; blob.visible = false; cursor.visible = false; xm.emissiveIntensity = 0; }
          void pIdx;
        }
        Bl.set(v[0], v[1], v[2], true);
        const p1 = (1 - v[2]) / 2;
        const ideal = App.rotVec([0, 0, 1], [Math.cos(ph), Math.sin(ph), 0], (area * Math.PI) / 180);
        ro.innerHTML = `旋轉角 θ = ${area}°，旋轉軸 φ = ${phase}°（${phase % 180 === 0 ? 'x 軸' : phase % 180 === 90 ? 'y 軸' : 'xy 平面上'}）<br>` +
          `虛擬 Z 累積的座標相位 = ${frame}°<br>` +
          `目前 P(1) = ${p1.toFixed(3)}${detMHz ? `（從 |0⟩ 出發的理想值 ${((1 - ideal[2]) / 2).toFixed(3)}，失諧造成偏差）` : ''}<br>` +
          `峰值 Rabi 頻率 ≈ ${(Math.max(...wave.map((w) => Math.abs(w.I))) / (2 * Math.PI) * 1000).toFixed(0)} MHz`;
      },
    };
  },
});

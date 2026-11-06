/* 場景 5：兩位元閘的物理實現 — 磁通調頻 CZ（|11⟩–|20⟩ 迴避交叉）與交叉共振 CR */
App.register({
  id: 'twoqubit', num: 5, short: '兩位元閘',
  title: '兩位元閘怎麼做？CZ 與交叉共振',
  subtitle: '讓兩顆量子位元「短暫對話」，產生只和兩者狀態都有關的效果',
  desc: `<p><b>CZ（Google、多數可調頻架構）</b>：用磁通脈衝把量子位元 A 的頻率往下拉，使 |11⟩ 接近 |20⟩。兩個能階因耦合互相排斥（迴避交叉），|11⟩ 的能量被推低，<b>只有 |11⟩</b> 會額外累積相位。累積到 π 時就是 CZ：|11⟩ → −|11⟩。</p>
<p>其他態 |00⟩、|01⟩、|10⟩ 的單位元相位用虛擬 Z 修正掉。脈衝太快或太靠近交叉點，會讓狀態跑到 |20⟩（<b>洩漏</b>）。</p>
<p><b>交叉共振 CR（IBM 固定頻率架構）</b>：用「目標 B 的頻率」去驅動控制 A。由於耦合，B 會繞 x 軸旋轉，但<b>方向取決於 A 是 0 還是 1</b>（ZX 交互作用）。ZX(π/2) 加上單位元閘 = CNOT。</p>
<p>典型：兩位元閘 40–300 ns，錯誤率 0.1–1%，是目前誤差的主要來源。</p>`,
  camera: { pos: [0.6, 2.4, 12.0], target: [0.6, 0.9, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    // 晶片
    const chip = new THREE.Group(); chip.position.set(-2.9, -1.2, 0); scene.add(chip);
    chip.add(U.box(4.6, 0.08, 2.4, U.mat(0x8c96a8, { metalness: 0.6, roughness: 0.35 })));
    const mA = U.mat(0xd6c9a0, { metalness: 0.8, roughness: 0.25, emissive: 0x4f8cff, emissiveIntensity: 0 });
    const mB = U.mat(0xd6c9a0, { metalness: 0.8, roughness: 0.25, emissive: 0xff5a5f, emissiveIntensity: 0 });
    const xmon = (x, m) => { chip.add(U.box(1.0, 0.06, 0.15, m, x, 0.07, 0), U.box(0.15, 0.06, 1.0, m, x, 0.07, 0)); };
    xmon(-1.3, mA); xmon(1.3, mB);
    const mC = U.mat(0x9fe0c0, { emissive: 0x2ecc71, emissiveIntensity: 0.1 });
    chip.add(U.box(1.2, 0.05, 0.12, mC, 0, 0.07, 0));
    chip.add(U.tube([[-1.3, 0.07, -0.6], [-1.3, 0.07, -1.2], [-2.3, 0.07, -1.2]], 0.03, U.metal(0x38c6d9)));
    chip.add(U.tube([[-1.9, 0.07, 0.0], [-2.3, 0.07, 0.0]], 0.03, U.metal(0xb87333)));
    ctx.label('量子位元 A', [-4.2, -0.6, 0.8], 'q0 small'); ctx.label('量子位元 B', [-1.6, -0.6, 0.8], 'q1 small');
    ctx.label('耦合器', [-2.9, -0.85, 0.4], 'small');
    const zl = ctx.label('Z 線（磁通）', [-5.0, -1.0, -1.2], 'teal small');
    const xyl = ctx.label('XY 線', [-5.4, -1.0, 0.2], 'gold small');
    const fluxBlob = U.sphere(0.1, U.glow(0x8ef0ff)); scene.add(fluxBlob); fluxBlob.visible = false;

    /* ---------- CZ：能階圖 ---------- */
    const cz = new THREE.Group(); scene.add(cz);
    const fB = 5.0, al = -0.25, gq = 0.015, fA0 = 6.0; // GHz
    const E11 = (fa) => fa + fB, E20 = (fa) => 2 * fa + al;
    const branch = (fa, s) => { const a = E11(fa), b = E20(fa), m = (a + b) / 2, d = (a - b) / 2; return m + s * Math.sqrt(d * d + 2 * gq * gq); };
    const lower11 = (fa) => (E11(fa) < E20(fa) ? branch(fa, -1) : branch(fa, -1)); // 從 fA0 出發的 |11⟩ 位於下支
    const PX = (fa) => 1.3 + (fa - 5.1) * 4.6, PY = (E) => -0.9 + (E - 10.0) * 2.4;
    const ptsU = [], ptsL = [], p11 = [], p20 = [], p10 = [];
    for (let i = 0; i <= 200; i++) {
      const fa = 5.1 + (i / 200) * 1.0;
      if (branch(fa, 1) < 11.3) ptsU.push([PX(fa), PY(branch(fa, 1)), 0]); ptsL.push([PX(fa), PY(branch(fa, -1)), 0]);
      p11.push([PX(fa), PY(E11(fa)), 0]); if (E20(fa) < 11.3) p20.push([PX(fa), PY(E20(fa)), 0]);
    }
    cz.add(U.line(ptsL, 0xe0a54a), U.line(ptsU, 0xb38cff));
    cz.add(U.line(p11, 0xe0a54a, 0.25), U.line(p20, 0xb38cff, 0.25));
    cz.add(U.line([[PX(5.1), -1.1, 0], [PX(6.1) + 0.2, -1.1, 0]], 0x6f8fbf, 0.7));
    cz.add(U.line([[PX(5.1), -1.1, 0], [PX(5.1), 2.4, 0]], 0x6f8fbf, 0.7));
    const czL = [ctx.label('|11⟩', [PX(6.1) + 0.45, PY(E11(6.1)), 0], 'gold small'), ctx.label('|20⟩', [PX(5.62) + 0.3, PY(11.3), 0], 'small'),
      ctx.label('A 的頻率 f<sub>A</sub>（磁通）→', [PX(5.45), -1.4, 0], 'small'), ctx.label('能量', [PX(5.1) - 0.4, 2.3, 0], 'small'),
      ctx.label('迴避交叉', [PX(5.25), PY(10.25) + 0.75, 0], 'teal small')];
    const dot = U.sphere(0.1, U.glow(0xffffff)); cz.add(dot);
    // 相位轉盤
    const dials = [];
    ['|00⟩', '|01⟩', '|10⟩', '|11⟩'].forEach((s, i) => {
      const gg = new THREE.Group(); gg.position.set(1.6 + i * 1.15, 3.55, 0); cz.add(gg);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.02, 8, 48), U.glow(0x6f8fbf)); gg.add(ring);
      const arr = U.fatArrow(i === 3 ? 0xe0a54a : 0x8ab4ff, 0.38, 0.025); arr.rotation.z = 0; gg.add(arr);
      dials.push({ gg, arr }); czL.push(ctx.label(s, [1.6 + i * 1.15, 2.92, 0], i === 3 ? 'gold small' : 'small'));
    });
    czL.push(ctx.label('條件相位（扣除單位元相位後）', [3.3, 4.25, 0], 'small'));

    /* ---------- CR：兩顆目標 Bloch 球 ---------- */
    const crB0 = App.Bloch(ctx, { r: 1.0, pos: [1.9, 1.0, 0], small: true, trailN: 400, title: '控制 A = |0⟩ 時的目標 B', titleCls: 'q0 small' });
    const crB1 = App.Bloch(ctx, { r: 1.0, pos: [4.9, 1.0, 0], small: true, trailN: 400, color: 0xff5a5f, trailColor: 0xffb0b2, title: '控制 A = |1⟩ 時的目標 B', titleCls: 'q1 small' });
    const crLabels = [...crB0.labels, ...crB1.labels];

    let mode = 'cz', depth = 0.95, Tp = 50, play = null, phi = 0, leak = 0, crAng = 0, crTarget = Math.PI / 2;
    const setMode = (m) => {
      mode = m; cz.visible = m === 'cz'; crB0.group.visible = crB1.group.visible = m === 'cr';
      czL.forEach((L) => L.show(m === 'cz')); crLabels.forEach((L) => L.show(m === 'cr'));
      zl.show(m === 'cz'); xyl.show(m === 'cr'); play = null; phi = 0; crAng = 0; crB0.clearTrail(); crB1.clearTrail();
    };
    // fA(t)：平頂脈衝，深度 depth（0..1 → 接近交叉點的程度）
    const fMin = () => fA0 - depth * (fA0 - 5.25 + 0.02);
    const fA = (t) => { const r = Math.min(1, t / (Tp * 0.25), (Tp - t) / (Tp * 0.25)); const s = Math.sin((Math.PI / 2) * Math.max(0, r)) ** 2; return fA0 - (fA0 - fMin()) * s; };
    const zeta = (fa) => branch(fa, -1) - E11(fa); // GHz，|11⟩ 的能量位移
    const phaseTotal = () => { let s = 0; const n = 400; for (let i = 0; i < n; i++) s += zeta(fA(((i + 0.5) / n) * Tp)) * (Tp / n); return -2 * Math.PI * s; };
    ui.radio([['cz', 'CZ（磁通調頻）'], ['cr', '交叉共振 CR']], mode, setMode);
    const dS = ui.slider('CZ：脈衝深度（接近交叉點）', 0.3, 1, 0.01, depth, (x) => { depth = x; }, (x) => `f_A 最低 ${(fA0 - x * (fA0 - 5.25 + 0.02)).toFixed(3)} GHz`);
    const tS = ui.slider('CZ：脈衝長度', 20, 120, 1, Tp, (x) => { Tp = x; }, (x) => x + ' ns');
    const r = ui.row();
    ui.button('▶ 執行', () => { play = { k: 0 }; phi = 0; crAng = 0; crB0.clearTrail(); crB1.clearTrail(); fluxBlob.visible = mode === 'cz'; }, r);
    const autoPi = () => { let best = Tp, bd = 9; for (let T = 20; T <= 120; T++) { Tp = T; const d = Math.abs(Math.abs(phaseTotal()) - Math.PI); if (d < bd) { bd = d; best = T; } } Tp = best; tS.set(best); };
    ui.button('自動找 π（調長度）', autoPi, r);
    const ro = ui.readout();
    setMode('cz'); autoPi();

    ctx.inset('上：控制脈衝　下：條件相位 / 目標旋轉角', (g, W, H, P) => {
      if (mode === 'cz') {
        const top = P.frame(g, W, 110, [0, Tp], [5.2, 6.05], { m: { l: 46, b: 18, t: 8 }, yticks: [[5.25, '5.25'], [6.0, '6.00']] });
        P.curve(g, fA, 0, Tp, top.X, top.Y, '#8ef0ff', 2);
        P.text(g, 'f_A (GHz)', W - 70, 24, '#8ef0ff');
        g.save(); g.translate(0, 112);
        const bot = P.frame(g, W, 118, [0, Tp], [0, 4], { m: { l: 46, b: 30, t: 6 }, xlabel: '時間（ns）', yticks: [[0, '0'], [Math.PI, 'π']] });
        let s = 0; g.strokeStyle = '#e0a54a'; g.lineWidth = 2; g.beginPath();
        for (let i = 0; i <= 200; i++) { const t = (i / 200) * Tp; if (i) s += -2 * Math.PI * zeta(fA(t)) * (Tp / 200); i ? g.lineTo(bot.X(t), bot.Y(s)) : g.moveTo(bot.X(t), bot.Y(0)); }
        g.stroke();
        g.strokeStyle = '#ff6bd5'; g.setLineDash([3, 3]); g.beginPath(); g.moveTo(bot.X(0), bot.Y(Math.PI)); g.lineTo(bot.X(Tp), bot.Y(Math.PI)); g.stroke(); g.setLineDash([]);
        g.restore();
      } else {
        const T = 200;
        const top = P.frame(g, W, 110, [0, T], [0, 1.1], { m: { l: 46, b: 18, t: 8 }, yticks: [[0, '0'], [1, '1']] });
        P.curve(g, (t) => Math.min(1, t / 30, (T - t) / 30), 0, T, top.X, top.Y, '#e0a54a', 2);
        P.text(g, '驅動 A，頻率 = f_B', W - 140, 24, '#e0a54a');
        g.save(); g.translate(0, 112);
        const bot = P.frame(g, W, 118, [0, T], [-2, 2], { m: { l: 46, b: 30, t: 6 }, xlabel: '時間（ns）', yticks: [[-Math.PI / 2, '−π/2'], [0, '0'], [Math.PI / 2, 'π/2']] });
        P.curve(g, (t) => (crTarget * (t / T)), 0, T, bot.X, bot.Y, '#4f8cff', 2);
        P.curve(g, (t) => -(crTarget * (t / T)), 0, T, bot.X, bot.Y, '#ff5a5f', 2);
        P.text(g, 'A=0', W - 46, bot.Y(1.2), '#a9c6ff'); P.text(g, 'A=1', W - 46, bot.Y(-1.0), '#ffb0b2');
        g.restore();
      }
    });

    return {
      update(t, dt) {
        if (mode === 'cz') {
          let fa = fA0;
          if (play) {
            play.k = Math.min(1, play.k + dt / 2.2);
            const tt = play.k * Tp; fa = fA(tt);
            const n = 30; let s = 0; for (let i = 0; i < n; i++) s += zeta(fA(((i + 0.5) / n) * tt)) * (tt / n);
            phi = -2 * Math.PI * s;
            fluxBlob.position.set(-5.2 + 1.0 * Math.min(1, play.k * 3), -1.13, -1.2 + 0.6 * Math.max(0, Math.min(1, play.k * 3 - 1)));
            mA.emissiveIntensity = 0.9 * (fA0 - fa) / (fA0 - 5.25);
            if (play.k >= 1) { play = null; fluxBlob.visible = false; mA.emissiveIntensity = 0; }
          }
          dot.position.set(PX(fa), PY(branch(fa, -1)), 0.05);
          dials.forEach((d, i) => { const a = i === 3 ? phi : 0; d.arr.setVec(new THREE.Vector3(Math.cos(a) * 0.38, Math.sin(a) * 0.38, 0)); });
          const tot = phaseTotal(), gap = (E20(fMin()) - E11(fMin())) * 1000;
          leak = gap < 40 ? Math.min(30, (40 - gap) * 0.5 + 50 / Tp) : 0.02 * 50 / Tp;
          ro.innerHTML = `完整脈衝的條件相位 = <b>${((Math.abs(tot) * 180) / Math.PI).toFixed(0)}°</b>（目標 180°）<br>` +
            `最接近時 |20⟩−|11⟩ 間距 = ${gap.toFixed(0)} MHz（耦合 √2·g = ${(Math.SQRT2 * gq * 1000).toFixed(0)} MHz）<br>` +
            `洩漏風險（示意）：${leak > 5 ? '<b style="color:#ff8080">高</b>' : leak > 1 ? '中' : '低'}　·　CZ = diag(1, 1, 1, −1)`;
        } else {
          if (play) {
            play.k = Math.min(1, play.k + dt / 2.5); crAng = play.k * crTarget;
            mA.emissiveIntensity = 0.6 * Math.sin(play.k * Math.PI); mB.emissiveIntensity = 0.3 * Math.sin(play.k * Math.PI);
            if (play.k >= 1) { play = null; mA.emissiveIntensity = mB.emissiveIntensity = 0; }
          }
          crB0.setV(App.rotVec([0, 0, 1], [1, 0, 0], crAng)); crB1.setV(App.rotVec([0, 0, 1], [1, 0, 0], -crAng));
          ro.innerHTML = `ZX 旋轉角 = ${((crAng * 180) / Math.PI).toFixed(0)}°（目標 90°）<br>A = |0⟩：B 繞 +x 轉；A = |1⟩：B 繞 −x 轉<br>ZX(π/2) + 單位元修正 = CNOT（IBM 早期的 ECR 閘即由此構成）`;
        }
      },
    };
  },
});

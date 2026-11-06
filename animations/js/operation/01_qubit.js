/* 場景 1：量子位元的狀態與測量 — Born 規則、塌縮、shots 統計 */
App.register({
  id: 'qubit', num: 1, short: '狀態與測量',
  title: '量子位元的狀態與測量',
  subtitle: '|ψ⟩ = α|0⟩ + β|1⟩　→　P(0) = |α|²，P(1) = |β|²',
  desc: `<p>量子位元的狀態是 Bloch 球上的一個點，由兩個角度決定：<b>θ</b> 決定 |0⟩、|1⟩ 的比例，<b>φ</b> 是兩者的相對相位。</p>
<p><b>測量只會得到 0 或 1</b>：得到 0 的機率是 cos²(θ/2)。測量後狀態<b>塌縮</b>到北極或南極，原本的疊加態就消失了。</p>
<p>所以「讀取」一個量子程式要<b>重複執行很多次（shots）</b>，用統計估計機率；誤差約 √(p(1−p)/N)，要精度提高 10 倍就要 100 倍的 shots。</p>
<p>注意：改變 φ 不會改變 0/1 的機率 —— 相位在 Z 測量中看不見，只有經過干涉（量子閘）才會顯現出來。</p>`,
  camera: { pos: [0.7, 1.6, 9.0], target: [0.7, 0.3, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const Bl = App.Bloch(ctx, { r: 1.6, pos: [-1.2, 0.3, 0], trailN: 2 });
    let th = 60, ph = 30;
    // 右側：統計長條
    const base = new THREE.Vector3(2.6, -1.0, 0);
    scene.add(U.box(2.6, 0.06, 1.2, U.mat(0x162238), base.x, base.y - 0.03, base.z));
    const H = 2.8;
    const mk = (x, col) => { const m = U.box(0.8, 1, 0.8, U.mat(col, { emissive: col, emissiveIntensity: 0.15 }), base.x + x, base.y, base.z); scene.add(m); return m; };
    const b0 = mk(-0.6, 0x4f8cff), b1 = mk(0.6, 0xff5a5f);
    const ideal0 = U.box(1.0, 0.035, 0.035, U.glow(0x8ef0ff), base.x - 0.6, 0, base.z + 0.45), ideal1 = U.box(1.0, 0.035, 0.035, U.glow(0x8ef0ff), base.x + 0.6, 0, base.z + 0.45);
    scene.add(ideal0, ideal1);
    ctx.label('得到 0', [base.x - 0.6, base.y - 0.35, 0.6], 'q0 small');
    ctx.label('得到 1', [base.x + 0.6, base.y - 0.35, 0.6], 'q1 small');
    ctx.label('青線 = 理論機率', [base.x, base.y + H + 0.45, 0], 'teal small');
    const c0L = ctx.label('', [0, 0, 0], 'plain small'), c1L = ctx.label('', [0, 0, 0], 'plain small');
    // 測量器（儀表盤）
    const meter = new THREE.Group(); meter.position.set(-1.2, -2.25, 0); scene.add(meter);
    meter.add(U.box(1.4, 0.5, 0.3, U.mat(0x22324c), 0, 0, 0));
    const lamp0 = U.sphere(0.11, U.mat(0x4f8cff, { emissive: 0x4f8cff, emissiveIntensity: 0.1 }), -0.35, 0, 0.2), lamp1 = U.sphere(0.11, U.mat(0xff5a5f, { emissive: 0xff5a5f, emissiveIntensity: 0.1 }), 0.35, 0, 0.2);
    meter.add(lamp0, lamp1);
    ctx.label('測量器', [-1.2, -2.75, 0], 'small');
    const flash = U.sphere(1.75, new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthWrite: false }), -1.2, 0.3, 0);
    scene.add(flash);

    let n0 = 0, n1 = 0, auto = false, rate = 20, acc = 0, collapse = null;
    const hist = [];
    const p0 = () => Math.cos((th * Math.PI) / 360) ** 2;
    const shot = (show) => {
      const b = Math.random() < p0() ? 0 : 1;
      b ? n1++ : n0++;
      const N = n0 + n1; hist.push([N, n1 / N]); if (hist.length > 4000) hist.splice(0, hist.length - 4000);
      if (show) collapse = { b, t: 0 };
      lamp0.material.emissiveIntensity = b ? 0.1 : 1.6; lamp1.material.emissiveIntensity = b ? 1.6 : 0.1;
      return b;
    };
    const clear = () => { n0 = n1 = 0; hist.length = 0; };
    const thS = ui.slider('θ（極角）', 0, 180, 1, th, (v) => { th = v; clear(); }, (v) => v + '°');
    const phS = ui.slider('φ（相位）', 0, 360, 1, ph, (v) => { ph = v; }, (v) => v + '°');
    const r = ui.row();
    ui.button('測量一次', () => { auto = false; autoB.classList.remove('on'); shot(true); }, r);
    const autoB = ui.button('連續 shots', (b) => { auto = !auto; b.classList.toggle('on', auto); }, r);
    ui.button('清除統計', clear, r);
    ui.button('一次跑 1000 shots', () => { for (let i = 0; i < 1000; i++) shot(false); });
    ui.slider('連續模式速度（shots/秒）', 2, 400, 1, rate, (v) => { rate = v; });
    const presets = ui.row();
    [['|0⟩', 0, 0], ['|1⟩', 180, 0], ['|+⟩', 90, 0], ['|+i⟩', 90, 90], ['θ=60°', 60, 30]].forEach(([t, a, b]) => ui.button(t, () => { th = a; ph = b; thS.show(a); phS.show(b); clear(); }, presets));
    const ro = ui.readout();

    ctx.inset('估計值 P̂(1) 隨 shots 數收斂（灰帶 = ±1σ）', (g, W, Hh, P) => {
      const p = 1 - p0(), Nmax = Math.max(100, n0 + n1);
      const lx = (N) => Math.log10(Math.max(1, N));
      const { X, Y } = P.frame(g, W, Hh, [0, lx(Nmax)], [0, 1], { xlabel: 'shots 數 N（對數）', ylabel: 'P̂(1)', yticks: [[0, '0'], [0.5, '0.5'], [1, '1']], xticks: [0, 1, 2, 3, 4, 5].filter((e) => e <= lx(Nmax)).map((e) => [e, '10^' + e]) });
      g.fillStyle = 'rgba(160,180,210,.18)'; g.beginPath();
      for (let k = 0; k <= 80; k++) { const x = (lx(Nmax) * k) / 80, N = 10 ** x, s = Math.sqrt(p * (1 - p) / N); g.lineTo(X(x), Y(Math.min(1, p + s))); }
      for (let k = 80; k >= 0; k--) { const x = (lx(Nmax) * k) / 80, N = 10 ** x, s = Math.sqrt(p * (1 - p) / N); g.lineTo(X(x), Y(Math.max(0, p - s))); }
      g.fill();
      g.strokeStyle = '#8ef0ff'; g.setLineDash([4, 4]); g.beginPath(); g.moveTo(X(0), Y(p)); g.lineTo(X(lx(Nmax)), Y(p)); g.stroke(); g.setLineDash([]);
      g.strokeStyle = '#e0a54a'; g.lineWidth = 2; g.beginPath();
      const step = Math.max(1, Math.floor(hist.length / 600));
      for (let i = 0; i < hist.length; i += step) { const [N, v] = hist[i]; i ? g.lineTo(X(lx(N)), Y(v)) : g.moveTo(X(lx(N)), Y(v)); }
      g.stroke();
    });

    return {
      update(t, dt) {
        const T = (th * Math.PI) / 180, F = (ph * Math.PI) / 180;
        let v = [Math.sin(T) * Math.cos(F), Math.sin(T) * Math.sin(F), Math.cos(T)];
        if (collapse) {
          collapse.t += dt;
          const z = collapse.b ? -1 : 1, k = Math.min(1, collapse.t / 0.25);
          if (collapse.t < 1.4) v = [v[0] * (1 - k), v[1] * (1 - k), v[2] + (z - v[2]) * k];
          const n = Math.hypot(...v) || 1; v = v.map((x) => x / n);
          flash.material.opacity = Math.max(0, 0.35 * (1 - collapse.t / 0.4));
          if (collapse.t > 1.6) collapse = null;
        }
        Bl.set(v[0], v[1], v[2], false);
        if (auto) { acc += dt * rate; while (acc >= 1) { acc -= 1; shot(acc < 1 && rate < 8); } }
        lamp0.material.emissiveIntensity *= 0.93; lamp1.material.emissiveIntensity *= 0.93;
        const N = n0 + n1, f0 = N ? n0 / N : 0, f1 = N ? n1 / N : 0;
        const k = 1 - Math.exp(-dt * 10);
        b0.scale.y += (Math.max(1e-3, f0 * H) - b0.scale.y) * k; b0.position.y = base.y + b0.scale.y / 2;
        b1.scale.y += (Math.max(1e-3, f1 * H) - b1.scale.y) * k; b1.position.y = base.y + b1.scale.y / 2;
        ideal0.position.y = base.y + p0() * H; ideal1.position.y = base.y + (1 - p0()) * H;
        c0L.pos.set(base.x - 0.6, base.y + b0.scale.y + 0.3, 0.45); c0L.set(String(n0));
        c1L.pos.set(base.x + 0.6, base.y + b1.scale.y + 0.3, 0.45); c1L.set(String(n1));
        const P0 = p0(), se = N ? Math.sqrt(f1 * (1 - f1) / N) : 0;
        const a = Math.cos(T / 2), b = Math.sin(T / 2);
        ro.innerHTML = `α = ${a.toFixed(3)}　β = ${b.toFixed(3)}·e<sup>i${ph}°</sup><br>理論：P(0) = ${P0.toFixed(3)}，P(1) = ${(1 - P0).toFixed(3)}<br>` +
          `shots N = ${N}：0 → ${n0} 次，1 → ${n1} 次<br>估計 P̂(1) = ${N ? f1.toFixed(3) : '—'} ± ${N ? se.toFixed(3) : '—'}（1σ）`;
      },
    };
  },
});

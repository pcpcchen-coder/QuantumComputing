/* 場景 2：單位元量子閘 = Bloch 球上的旋轉 */
App.register({
  id: 'gates', num: 2, short: '單位元閘',
  title: '單位元量子閘：Bloch 球上的旋轉',
  subtitle: '每個單位元閘 = 繞某一軸旋轉某一角度（2×2 么正矩陣）',
  desc: `<p>點下方的閘，看狀態向量怎麼轉。<b>粉紅線是旋轉軸</b>。</p>
<p><b>X</b>：繞 x 軸 180°（0↔1，量子版 NOT）。<b>Y</b>：繞 y 軸 180°。<b>Z</b>：繞 z 軸 180°（只改相位）。</p>
<p><b>H（Hadamard）</b>：繞 (x+z)/√2 軸 180°，把 |0⟩ 變成 |+⟩ = (|0⟩+|1⟩)/√2 —— 產生疊加的主力。</p>
<p><b>S、T</b>：繞 z 軸 90°、45°（相位閘）。<b>√X</b>：繞 x 軸 90°（IBM 的原生閘）。<b>Rx/Ry/Rz(θ)</b>：任意角度。</p>
<p>任何單位元操作都能寫成 Rz·Ry·Rz 的組合 —— 實際硬體只需要「繞 x/y 軸的微波脈衝」加上「虛擬 Z」。</p>`,
  camera: { pos: [3.8, 2.6, 4.6], target: [0, 0, 0] },
  build(ctx) {
    const { U, THREE, ui } = ctx;
    const { G, ROT, fmtC } = App.Q;
    const Bl = App.Bloch(ctx, { r: 1.7, trailN: 900 });
    const st = new App.Q.State(1);
    let v = [0, 0, 1], queue = [], cur = null, theta = 90, seq = [], lastM = G.I, lastName = 'I';
    const axisL = ctx.label('', [0, 0, 0], 'small');
    axisL.el.style.color = '#ff9be6';
    const push = (name, ax, ang, M, label) => queue.push({ name, ax, ang, M, label: label || name });
    const gate = (n) => { const [ax, ang] = ROT[n]; push(n, ax, ang, G[n]); };
    const rows = [['X', 'Y', 'Z', 'H'], ['S', 'Sdg', 'T', 'Tdg', 'SX']];
    rows.forEach((r) => { const row = ui.row(); r.forEach((n) => ui.button(n === 'Sdg' ? 'S†' : n === 'Tdg' ? 'T†' : n === 'SX' ? '√X' : n, () => gate(n), row)); });
    ui.slider('旋轉角 θ（給 Rx / Ry / Rz）', -180, 180, 5, theta, (x) => { theta = x; }, (x) => x + '°');
    const r2 = ui.row();
    const rad = () => (theta * Math.PI) / 180;
    ui.button('Rx(θ)', () => push('RX', [1, 0, 0], rad(), G.RX(rad()), `Rx(${theta}°)`), r2);
    ui.button('Ry(θ)', () => push('RY', [0, 1, 0], rad(), G.RY(rad()), `Ry(${theta}°)`), r2);
    ui.button('Rz(θ)', () => push('RZ', [0, 0, 1], rad(), G.RZ(rad()), `Rz(${theta}°)`), r2);
    const r3 = ui.row();
    const resetTo = (vv, re0, re1, im1 = 0) => { queue = []; cur = null; v = vv; st.re[0] = re0; st.im[0] = 0; st.re[1] = re1; st.im[1] = im1; seq = []; Bl.clearTrail(); Bl.showAxis(null); };
    ui.button('重設 |0⟩', () => resetTo([0, 0, 1], 1, 0), r3);
    ui.button('重設 |1⟩', () => resetTo([0, 0, -1], 0, 1), r3);
    ui.button('清除軌跡', () => Bl.clearTrail(), r3);
    const r4 = ui.row();
    ui.button('示範：H → Z → H = X', () => { resetTo([0, 0, 1], 1, 0); ['H', 'Z', 'H'].forEach(gate); }, r4);
    ui.button('示範：H → T → H', () => { resetTo([0, 0, 1], 1, 0); ['H', 'T', 'H'].forEach(gate); }, r4);
    const ro = ui.readout();
    let speed = 1;
    ui.slider('動畫速度', 0.3, 3, 0.1, speed, (x) => { speed = x; }, (x) => x.toFixed(1) + '×');

    ctx.inset('最後一個閘的矩陣與線路紀錄', (g, W, H, P) => {
      P.text(g, `${lastName} =`, 14, 44, '#ffd28a');
      const cell = (z, x, y) => P.text(g, fmtC(z[0], z[1]), x, y, '#e8eef8', 'center');
      g.strokeStyle = '#9fb0c8'; g.lineWidth = 1.5;
      g.beginPath(); g.moveTo(100, 18); g.lineTo(94, 18); g.lineTo(94, 76); g.lineTo(100, 76); g.stroke();
      g.beginPath(); g.moveTo(300, 18); g.lineTo(306, 18); g.lineTo(306, 76); g.lineTo(300, 76); g.stroke();
      cell(lastM[0][0], 150, 40); cell(lastM[0][1], 250, 40); cell(lastM[1][0], 150, 66); cell(lastM[1][1], 250, 66);
      // 線路
      const y = 140; g.strokeStyle = '#9fb0c8'; g.beginPath(); g.moveTo(40, y); g.lineTo(W - 12, y); g.stroke();
      P.text(g, 'q0', 12, y + 4, '#9fb0c8');
      const show = seq.slice(-7);
      show.forEach((s, i) => {
        const x = 70 + i * 44; g.fillStyle = '#1c9db0'; g.fillRect(x - 18, y - 15, 36, 30);
        P.text(g, s.length > 4 ? s.slice(0, 2) : s, x, y + 5, '#fff', 'center');
      });
      P.text(g, '|0⟩ 起始 → 由左至右依序作用；矩陣相乘順序相反', 14, 196, '#9fb0c8');
      P.text(g, `目前：${fmtC(st.re[0], st.im[0])}|0⟩ + (${fmtC(st.re[1], st.im[1])})|1⟩`, 14, 218, '#e8eef8');
    });

    return {
      update(t, dt) {
        if (!cur && queue.length) {
          cur = queue.shift(); cur.k = 0; cur.v0 = v.slice();
          Bl.showAxis(cur.ax);
          axisL.pos.copy(Bl.world(...cur.ax, 1.42)); axisL.set(`旋轉軸 · ${cur.label}`); axisL.show(true);
        }
        if (cur) {
          cur.k = Math.min(1, cur.k + (dt * speed) / (0.5 + Math.abs(cur.ang) / Math.PI * 0.8));
          v = App.rotVec(cur.v0, cur.ax, cur.ang * U.smooth(cur.k));
          if (cur.k >= 1) {
            st.apply(0, cur.M); lastM = cur.M; lastName = cur.label;
            const b = st.bloch(0); v = b; seq.push(cur.label.replace('dg', '†')); if (seq.length > 30) seq.shift();
            cur = null; if (!queue.length) { Bl.showAxis(null); axisL.show(false); }
          }
        }
        Bl.set(v[0], v[1], v[2], true);
        const p0 = st.prob(0);
        ro.innerHTML = `Bloch 向量 = (${v[0].toFixed(2)}, ${v[1].toFixed(2)}, ${v[2].toFixed(2)})<br>` +
          `|ψ⟩ = (${fmtC(st.re[0], st.im[0])})|0⟩ + (${fmtC(st.re[1], st.im[1])})|1⟩<br>測量機率：P(0) = ${p0.toFixed(3)}，P(1) = ${(1 - p0).toFixed(3)}` +
          (queue.length ? `<br>等待中的閘：${queue.map((q) => q.label).join(' → ')}` : '');
      },
    };
  },
});

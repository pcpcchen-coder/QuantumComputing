/* 場景 4：多量子位元暫存器、疊加與糾纏 — 2ⁿ 個振幅 */
App.register({
  id: 'register', num: 4, short: '多位元與糾纏',
  title: '多量子位元：2ⁿ 個振幅與糾纏',
  subtitle: 'n 個量子位元 = 2ⁿ 個複數振幅；閘一次作用在全部振幅上',
  desc: `<p>上排是每個量子位元「自己」的 Bloch 球，下方柱子是整個暫存器的 <b>2ⁿ 個基底態振幅</b>：高度 = 機率，顏色 = 相位（金 = +，藍 = −）。</p>
<p>按「均勻疊加」：每個量子位元做 H，2ⁿ 個基底態的機率全部相同。</p>
<p>按「Bell 態」：H + CNOT 得到 (|00⟩+|11⟩)/√2。注意上排的箭頭<b>縮成一點</b>：單獨看任何一個量子位元都是完全隨機的，但兩者的結果永遠相同 —— 這就是<b>糾纏</b>，資訊存在「關聯」裡，而不在任何單一量子位元裡。</p>
<p>右下插圖：在古典電腦上精確模擬 n 個量子位元，需要 2ⁿ × 16 bytes 的記憶體。</p>`,
  camera: { pos: [0.4, 3.0, 12.0], target: [0.4, 1.0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const { State, fmtC, ket } = App.Q;
    let n = 2, st, bars, blochs = [], tgt = 0, ctl = 1, objs = [];
    let measured = null;
    const clearObjs = () => {
      objs.forEach((o) => { scene.remove(o); o.traverse((c) => { c.geometry && c.geometry.dispose(); }); });
      objs = [];
      ctx.app.labels.forEach((L) => { if (L.tmp) L.el.remove(); });
      ctx.app.labels = ctx.app.labels.filter((L) => !L.tmp);
    };
    const mark = (from) => { ctx.app.labels.slice(from).forEach((L) => { L.tmp = true; }); };
    const setup = () => {
      clearObjs();
      const L0 = ctx.app.labels.length;
      st = new State(n);
      blochs = [];
      for (let q = 0; q < n; q++) {
        const x = ((n - 1) / 2 - q) * 2.3;
        const b = App.Bloch(ctx, { r: 0.75, pos: [x, 3.2, 0], small: true, trailN: 2, title: `q${q}` });
        blochs.push(b); objs.push(b.group);
      }
      const dx = n <= 2 ? 1.2 : n === 3 ? 0.85 : 0.5;
      bars = App.AmpBars(ctx, n, { pos: [0, -0.6, 0.6], dx, w: dx * 0.6, H: 1.9, labelDz: 0.45 });
      objs.push(bars.group);
      bars.set(st, true);
      mark(L0);
      measured = null;
    };
    setup();
    ui.slider('量子位元數 n', 1, 4, 1, n, (x) => { n = x; tgt = 0; ctl = Math.min(1, n - 1); setup(); }, (x) => `${x}（${1 << x} 個振幅）`);
    const tr = ui.row();
    const tsel = [];
    [0, 1, 2, 3].forEach((q) => { const b = ui.button(`目標 q${q}`, () => { tgt = q; tsel.forEach((x, k) => x.classList.toggle('on', k === q)); }, tr); tsel.push(b); });
    tsel[0].classList.add('on');
    const g1 = ui.row();
    const ap = (f) => { if (measured !== null) measured = null; f(); bars.set(st); };
    ['H', 'X', 'Z', 'S', 'T'].forEach((gname) => ui.button(gname, () => ap(() => { if (tgt < n) st.gate(gname, tgt); }), g1));
    const g2 = ui.row();
    ui.button('CNOT（控制 = 目標+1 → 目標）', () => ap(() => { const c = (tgt + 1) % n; if (n > 1 && tgt < n) st.cx(c, tgt); }), g2);
    ui.button('CZ', () => ap(() => { if (n > 1 && tgt < n) st.cz((tgt + 1) % n, tgt); }), g2);
    const pr = ui.row();
    ui.button('均勻疊加 H⊗ⁿ', () => ap(() => { st.reset(); for (let q = 0; q < n; q++) st.gate('H', q); }), pr);
    ui.button('Bell 態', () => ap(() => { st.reset(); if (n >= 2) { st.gate('H', 1); st.cx(1, 0); } }), pr);
    ui.button('GHZ 態', () => ap(() => { st.reset(); st.gate('H', n - 1); for (let q = n - 1; q > 0; q--) st.cx(q, q - 1); }), pr);
    const mr = ui.row();
    ui.button('測量全部', () => { const k = st.measureAll(); measured = k; bars.set(st); }, mr);
    ui.button('只測 q0', () => { const b = st.measure(0); measured = `q0 = ${b}`; bars.set(st); }, mr);
    ui.button('重設 |0…0⟩', () => { st.reset(); measured = null; bars.set(st); }, mr);
    const ro = ui.readout();

    ctx.inset('精確模擬 n 個量子位元所需記憶體（2ⁿ × 16 bytes）', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [0, 60], [0, 20], { xlabel: '量子位元數 n', ylabel: 'log₁₀(bytes)', xticks: [[0, '0'], [10, '10'], [20, '20'], [30, '30'], [40, '40'], [50, '50'], [60, '60']], yticks: [[3, 'KB'], [9, 'GB'], [12, 'TB'], [15, 'PB'], [18, 'EB']] });
      P.curve(g, (x) => Math.log10(16) + x * Math.log10(2), 0, 60, X, Y, '#e0a54a', 2.2);
      [[30, '16 GB（筆電）'], [40, '16 TB（大型伺服器）'], [50, '18 PB']].forEach(([q, s]) => {
        const y = Math.log10(16) + q * Math.log10(2); P.dot(g, X(q), Y(y), 4, '#38c6d9');
        P.text(g, s, X(q) - 6, Y(y) - 8, '#bff6ff', 'right');
      });
      g.strokeStyle = '#ff5a5f'; g.setLineDash([3, 3]); g.beginPath(); g.moveTo(X(0), Y(16.5)); g.lineTo(X(60), Y(16.5)); g.stroke(); g.setLineDash([]);
      P.text(g, '頂級超級電腦總記憶體 ≈ 10 PB', X(2), Y(16.5) + 14, '#ffb0b2');
    });

    return {
      update(t, dt) {
        bars.update(dt);
        for (let q = 0; q < n; q++) blochs[q].setV(st.bloch(q), false);
        const lines = [];
        for (let i = 0; i < st.N; i++) { const p = st.prob(i); if (p > 1e-6) lines.push(`${fmtC(st.re[i], st.im[i])} ${ket(i, n)}`); }
        const purity = [];
        for (let q = 0; q < n; q++) { const b = st.bloch(q); purity.push(Math.hypot(...b)); }
        const ent = n > 1 && purity.some((r) => r < 0.98);
        ro.innerHTML = `|ψ⟩ = ${lines.slice(0, 8).join(' + ')}${lines.length > 8 ? ' + …' : ''}<br>` +
          `各量子位元 Bloch 長度：${purity.map((r, q) => `q${q} ${r.toFixed(2)}`).join('，')}<br>` +
          (ent ? '<b style="color:#ff9be6">有糾纏</b>：單一量子位元的向量變短（約化態是混態）' : '無糾纏（可分離態）：每個量子位元各自是純態') +
          (measured !== null ? `<br>測量結果：${typeof measured === 'number' ? ket(measured, n) : measured}` : '');
      },
    };
  },
});

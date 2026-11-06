/* 場景 9：Grover 搜尋 — Oracle 標記 + 對平均值反射 = 振幅放大，約 (π/4)√N 次 */
App.register({
  id: 'grover', num: 9, short: 'Grover 搜尋',
  title: 'Grover 搜尋：振幅放大',
  subtitle: '在 N 個候選中找出標記的答案：古典平均 N/2 次，量子約 (π/4)√N 次',
  desc: `<p>柱子高度是<b>振幅</b>（不是機率），可以是負的。綠框是要找的答案（只有 Oracle「認得」它）。</p>
<p>① <b>均勻疊加</b>：每個答案振幅都是 1/√N。</p>
<p>② <b>Oracle</b>：把答案的振幅變號（翻到下面）。機率沒變，所以直接量測沒用。</p>
<p>③ <b>擴散（對平均值反射）</b>：每個振幅 a → 2·平均 − a。因為答案在平均值下方很遠，反射後被拉得很高，其他的則略降。</p>
<p>每一輪讓狀態在「答案 / 非答案」平面上轉 2θ（右下插圖），sin θ = 1/√N。轉太多次反而會轉過頭！</p>
<p>加速是<b>平方級</b>：N = 100 萬時，古典平均 50 萬次，Grover 約 785 次。</p>`,
  camera: { pos: [0, 4.2, 10.5], target: [0, 0.4, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    let n = 4, N, mark = 11, amp, bars, objs = [], k = 0, phase = 'init', meanPlane, frame, autoRun = false, acc = 0, measured = null;
    const HH = 3.0;
    const clear = () => { objs.forEach((o) => scene.remove(o)); objs = []; ctx.app.labels.forEach((L) => { if (L.tmp) L.el.remove(); }); ctx.app.labels = ctx.app.labels.filter((L) => !L.tmp); };
    const setup = () => {
      clear(); const L0 = ctx.app.labels.length;
      N = 1 << n; mark = Math.min(mark, N - 1);
      amp = new Float64Array(N).fill(1 / Math.sqrt(N)); k = 0; phase = 'init'; measured = null;
      const cols = N <= 16 ? N : 8, dx = N <= 4 ? 1.4 : N <= 8 ? 1.0 : N <= 16 ? 0.62 : 0.7;
      bars = App.AmpBars(ctx, n, { pos: [0, -0.6, 0], cols, dx, dz: 0.7, w: Math.min(0.5, dx * 0.6), H: HH, mode: 'amp', maxLabels: 16, labelFn: (i) => String(i) });
      objs.push(bars.group);
      const [x, , z] = bars.pos(mark);
      frame = new THREE.Mesh(new THREE.BoxGeometry(Math.min(0.5, dx * 0.6) + 0.16, 0.05, Math.min(0.5, dx * 0.6) + 0.16), U.glow(0x66ffcc));
      frame.position.set(x, -0.6, z); scene.add(frame); objs.push(frame);
      const sz = bars.group.children[0].geometry.parameters;
      meanPlane = new THREE.Mesh(new THREE.BoxGeometry(sz.width, 0.01, sz.depth), new THREE.MeshBasicMaterial({ color: 0xff6bd5, transparent: true, opacity: 0.25, depthWrite: false }));
      meanPlane.position.y = -0.6; scene.add(meanPlane); objs.push(meanPlane);
      ctx.label('答案', bars.top(mark).add(new THREE.Vector3(0, 0, 0)), 'teal small');
      ctx.app.labels[ctx.app.labels.length - 1].obj = null;
      for (let i = ctx.app.labels.length - 1; i >= L0; i--) ctx.app.labels[i].tmp = true;
      ansL = ctx.app.labels[ctx.app.labels.length - 1];
      push(true);
    };
    let ansL = null;
    const push = (instant) => { bars.setHeights(Array.from(amp), (i) => (amp[i] >= 0 ? 0xe0a54a : 0x4f8cff)); if (instant) bars.update(1, 100); };
    const mean = () => amp.reduce((a, b) => a + b, 0) / N;
    const oracle = () => { amp[mark] = -amp[mark]; phase = 'oracle'; push(); };
    const diffuse = () => { const m = mean(); for (let i = 0; i < N; i++) amp[i] = 2 * m - amp[i]; phase = 'diff'; k++; push(); };
    const theta = () => Math.asin(1 / Math.sqrt(N));
    const kOpt = () => Math.max(1, Math.round(Math.PI / (4 * theta()) - 0.5));
    ui.slider('量子位元數 n', 2, 6, 1, n, (v) => { n = v; setup(); }, (v) => `${v}（N = ${1 << v}）`);
    const mS = ui.slider('答案（標記的項目）', 0, 63, 1, mark, (v) => { mark = Math.min(v, (1 << n) - 1); setup(); }, (v) => String(v));
    void mS;
    const r1 = ui.row();
    ui.button('② Oracle', () => { if (phase !== 'oracle') oracle(); }, r1);
    ui.button('③ 擴散', () => { if (phase === 'oracle') diffuse(); }, r1);
    ui.button('完整一輪', () => { if (phase !== 'oracle') oracle(); setTimeout(() => diffuse(), 700); }, r1);
    const r2 = ui.row();
    ui.button('自動跑到最佳次數', () => { setup(); autoRun = true; acc = 0; }, r2);
    ui.button('測量', () => { const r = Math.random(); let a = 0, i = 0; for (; i < N - 1; i++) { a += amp[i] * amp[i]; if (r < a) break; } measured = i; }, r2);
    ui.button('重設', setup, r2);
    const ro = ui.readout();
    setup();

    ctx.inset('幾何圖：每輪在「答案–非答案」平面轉 2θ', (g, W, H, P) => {
      const cx = 120, cy = 128, R = 92;
      g.strokeStyle = 'rgba(160,180,210,.35)'; g.beginPath(); g.arc(cx, cy, R, -Math.PI / 2 - 0.15, 0.15); g.stroke();
      g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + R + 10, cy); g.moveTo(cx, cy); g.lineTo(cx, cy - R - 10); g.stroke();
      P.text(g, '非答案 |s′⟩', cx + R - 30, cy + 18, '#9fb0c8'); P.text(g, '答案 |w⟩', cx + 4, cy - R - 12, '#66ffcc');
      const th = theta();
      for (let j = 0; j <= Math.max(k, 0); j++) {
        const a = (2 * j + 1) * th;
        g.strokeStyle = j === k ? '#e0a54a' : 'rgba(224,165,74,.3)'; g.lineWidth = j === k ? 3 : 1.5;
        g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + R * Math.cos(a), cy - R * Math.sin(a)); g.stroke();
      }
      if (phase === 'oracle') { const a = -(2 * k + 1) * th; g.strokeStyle = '#4f8cff'; g.lineWidth = 2.5; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + R * Math.cos(a), cy - R * Math.sin(a)); g.stroke(); P.text(g, 'Oracle：對 |s′⟩ 鏡射', cx + 20, cy + 40, '#a9c6ff'); }
      // 右側：成功機率 vs 迭代次數
      const ox = 240, ow = 130;
      const km = Math.max(kOpt() * 2 + 1, 3);
      const X = (x) => ox + (x / km) * ow, Y = (y) => 200 - y * 170;
      g.strokeStyle = 'rgba(160,180,210,.35)'; g.lineWidth = 1; g.beginPath(); g.moveTo(ox, 30); g.lineTo(ox, 200); g.lineTo(ox + ow, 200); g.stroke();
      g.strokeStyle = '#e0a54a'; g.lineWidth = 2; g.beginPath();
      for (let i = 0; i <= 100; i++) { const x = (i / 100) * km; const y = Math.sin((2 * x + 1) * th) ** 2; i ? g.lineTo(X(x), Y(y)) : g.moveTo(X(x), Y(y)); } g.stroke();
      for (let j = 0; j <= km; j++) P.dot(g, X(j), Y(Math.sin((2 * j + 1) * th) ** 2), j === k ? 5 : 2.5, j === k ? '#fff' : '#e0a54a');
      P.text(g, 'P(成功) vs 輪數', ox, 22, '#9fb0c8'); P.text(g, String(km), X(km), 216, '#9fb0c8', 'center'); P.text(g, '0', X(0), 216, '#9fb0c8', 'center');
    });

    return {
      update(t, dt) {
        bars.update(dt, 6);
        const m = mean();
        meanPlane.position.y = -0.6 + m * HH; meanPlane.visible = phase === 'oracle';
        if (ansL) ansL.pos.copy(bars.top(mark)).add(new THREE.Vector3(0, 0.25, 0));
        if (autoRun) { acc += dt; if (acc > 0.8) { acc = 0; if (phase !== 'oracle') oracle(); else { diffuse(); if (k >= kOpt()) autoRun = false; } } }
        const ps = amp[mark] * amp[mark];
        ro.innerHTML = `N = ${N}，第 ${k} 輪${phase === 'oracle' ? '（已做 Oracle，粉紅面 = 平均振幅）' : ''}<br>答案的機率 P = <b>${ps.toFixed(3)}</b>　其他每個 = ${((1 - ps) / (N - 1)).toFixed(4)}<br>` +
          `最佳輪數 ≈ (π/4)√N ≈ ${kOpt()}　古典平均要查 ${(N / 2).toFixed(0)} 次` + (measured !== null ? `<br>測量結果：${measured}${measured === mark ? ' ✓ 找到了' : ' ✗'}` : '');
      },
    };
  },
});

/* 場景 6：量子線路執行器 — 一步一步看狀態向量怎麼變，最後量測得到直方圖 */
(function () {
  const PI = Math.PI;
  const H = (q) => ({ g: 'H', q }), X = (q) => ({ g: 'X', q }), Z = (q) => ({ g: 'Z', q });
  const CX = (c, t) => ({ g: 'CX', c, t }), CZ = (c, t) => ({ g: 'CZ', c, t });
  const CP = (c, t, th, label) => ({ g: 'CP', c, t, th, label });
  const RY = (q, th, label) => ({ g: 'RY', q, th, label });
  const SW = (c, t) => ({ g: 'SWAP', c, t });
  const M = (qs) => qs.map((q) => ({ g: 'M', q }));
  const all = (n, f) => [...Array(n).keys()].map(f);
  const CIRCUITS = {
    bell: { name: 'Bell 態', n: 2, meas: [0, 1], cols: [
      [[H(0)], 'H 讓 q0 進入疊加 (|0⟩+|1⟩)/√2'],
      [[CX(0, 1)], 'CNOT：q0 是 1 時翻轉 q1 → (|00⟩+|11⟩)/√2，兩個位元糾纏'],
      [M([0, 1]), '量測：只會得到 00 或 11，各 50%；兩個位元永遠相同'],
    ] },
    ghz: { name: 'GHZ 態（3 位元糾纏）', n: 3, meas: [0, 1, 2], cols: [
      [[H(0)], 'H 產生疊加'], [[CX(0, 1)], 'CNOT 把糾纏擴展到 q1'], [[CX(1, 2)], 'CNOT 再擴展到 q2 → (|000⟩+|111⟩)/√2'],
      [M([0, 1, 2]), '量測：000 或 111，各 50%'],
    ] },
    interf: { name: '干涉：H–Z–H', n: 1, meas: [0], cols: [
      [[H(0)], 'H：|0⟩ → (|0⟩+|1⟩)/√2，兩條路徑'],
      [[Z(0)], 'Z：只把 |1⟩ 路徑的振幅變號（機率不變！柱子只變色）'],
      [[H(0)], 'H 再把兩條路徑合併：|0⟩ 的兩份振幅相消、|1⟩ 的相加 → 100% 得到 1'],
      [M([0]), '量測：一定是 1。相位透過干涉變成了可觀測的結果'],
    ] },
    dj: { name: 'Deutsch–Jozsa（平衡函數）', n: 3, meas: [0, 1], cols: [
      [[X(2)], '輔助位元 q2 設為 |1⟩'],
      [all(3, H), '全部做 H：輸入是 4 種 x 的均勻疊加，q2 = |−⟩'],
      [[CX(0, 2)], 'Oracle f(x) = x₀ ⊕ x₁（第 1 步）：相位回踢，f(x)=1 的振幅變號'],
      [[CX(1, 2)], 'Oracle（第 2 步）：完成 (−1)^f(x) 的相位標記'],
      [[H(0), H(1), H(2)], '再做 H：所有路徑干涉。常數函數 → 回到 00；平衡函數 → |00⟩ 振幅完全抵消'],
      [M([0, 1]), '量測輸入位元：不是 00 → 函數是「平衡」的。只查詢 1 次（古典最壞要 2ⁿ⁻¹+1 次）'],
    ] },
    bv: { name: 'Bernstein–Vazirani（秘密字串 101）', n: 4, meas: [0, 1, 2], cols: [
      [[X(3)], '輔助位元 q3 = |1⟩'],
      [all(4, H), '全部 H：8 種輸入的均勻疊加'],
      [[CX(0, 3), CX(2, 3)], 'Oracle f(x) = s·x mod 2，s = 101：對 s 中為 1 的位元做 CNOT'],
      [all(4, H), 'H：干涉後輸入暫存器直接變成 |s⟩ = |101⟩'],
      [M([0, 1, 2]), '量測得到 101。量子：1 次查詢；古典：要 n = 3 次'],
    ] },
    grover: { name: 'Grover 搜尋（2 位元，找 |11⟩）', n: 2, meas: [0, 1], cols: [
      [[H(0), H(1)], '均勻疊加：4 個答案各 25%'],
      [[CZ(0, 1)], 'Oracle：把答案 |11⟩ 的振幅變號（藍色）'],
      [[H(0), H(1)], '擴散算子（對平均值反射）第 1 步：H'],
      [[X(0), X(1)], '擴散第 2 步：X'],
      [[CZ(0, 1)], '擴散第 3 步：CZ'],
      [[X(0), X(1)], '擴散第 4 步：X'],
      [[H(0), H(1)], '擴散第 5 步：H → |11⟩ 的機率變成 100%'],
      [M([0, 1]), '量測：一次就找到 11（N = 4 時恰好 1 次迭代）'],
    ] },
    tele: { name: '量子隱形傳態', n: 3, meas: [2], cols: [
      [[RY(0, (2 * PI) / 3, 'Ry')], '準備要傳送的狀態：q0 = cos60°|0⟩ + sin60°|1⟩（P(1) = 0.75）'],
      [[H(1)], '開始製作 q1、q2 的 Bell 對'], [[CX(1, 2)], 'q1–q2 糾纏（q2 交給遠方的 Bob）'],
      [[CX(0, 1)], 'Alice：CNOT q0 → q1'], [[H(0)], 'Alice：H q0（接著量測 q0、q1）'],
      [[CX(1, 2)], 'Bob 依 q1 的結果做 X（延遲量測：改成受控閘）'],
      [[CZ(0, 2)], 'Bob 依 q0 的結果做 Z → q2 變成原本 q0 的狀態（看左側小球）'],
      [M([2]), '量測 q2：P(1) = 0.75，和一開始的 q0 相同'],
    ] },
    qft: { name: '量子傅立葉轉換（QFT，輸入 |110⟩）', n: 3, meas: [0, 1, 2], cols: [
      [[X(1), X(2)], '準備輸入 |110⟩ = 6'],
      [[H(2)], 'H q2'], [[CP(1, 2, PI / 2, 'P(π/2)')], '受控相位 π/2'], [[CP(0, 2, PI / 4, 'P(π/4)')], '受控相位 π/4'],
      [[H(1)], 'H q1'], [[CP(0, 1, PI / 2, 'P(π/2)')], '受控相位 π/2'], [[H(0)], 'H q0'],
      [[SW(0, 2)], 'SWAP 調整位元順序 → 振幅大小相同，相位依 e^{2πi·6k/8} 變化（看顏色）'],
      [M([0, 1, 2]), '量測：8 個結果機率相同 —— 資訊都在相位裡，所以 QFT 要搭配其他步驟（如 Shor）'],
    ] },
  };

  App.register({
    id: 'circuit', num: 6, short: '量子線路',
    title: '量子線路：一步一步執行',
    subtitle: '線路 = 由左到右依序作用的量子閘；每一步都在改寫 2ⁿ 個振幅',
    desc: `<p>上方是量子線路（由上到下 q0、q1…，時間由左到右），下方柱子是當下的狀態向量（高度 = 機率，顏色 = 相位）。每條線最左邊的小球是該量子位元的約化 Bloch 向量。</p>
<p>選一個範例，按「單步」或「播放」：</p>
<p>• <b>Bell / GHZ</b>：疊加 + 糾纏。• <b>干涉</b>：相位如何變成結果。• <b>Deutsch–Jozsa、Bernstein–Vazirani</b>：一次查詢得到全域性質。• <b>Grover</b>：振幅放大。• <b>隱形傳態</b>：用糾纏 + 古典通訊傳送狀態。• <b>QFT</b>：把資訊編進相位。</p>
<p>最後的量測欄會跑 1000 shots，插圖顯示直方圖（青線 = 理想機率）；可加入雜訊比較真實硬體的結果。</p>`,
    camera: { pos: [0.6, 1.4, 13.5], target: [0.6, 0.6, 0] },
    build(ctx) {
      const { scene, U, THREE, ui } = ctx;
      const { State, fmtC, ket } = App.Q;
      let key = 'bell', C, st, bars, step = -1, objs = [], gateMeshes = [], blochs = [], playing = false, acc = 0, counts = null, ideal = null, noise = false;
      const cursor = U.box(0.9, 1, 0.9, new THREE.MeshBasicMaterial({ color: 0x38c6d9, transparent: true, opacity: 0.12, depthWrite: false }));
      scene.add(cursor);
      const colX = (k, nc) => (k - (nc - 1) / 2) * 1.05 + 0.6;
      const wy = (q) => 3.6 - q * 0.8;
      const COL = { H: 0x1c9db0, X: 0xd9534f, Z: 0x3b6fd8, RY: 0xc8862a, CP: 0x8a5cd0, M: 0x4a5468, S: 0x3b6fd8, T: 0x3b6fd8 };
      const clear = () => {
        objs.forEach((o) => scene.remove(o)); objs = [];
        ctx.app.labels.forEach((L) => { if (L.tmp) L.el.remove(); }); ctx.app.labels = ctx.app.labels.filter((L) => !L.tmp);
      };
      const tmpFrom = (k) => ctx.app.labels.slice(k).forEach((L) => { L.tmp = true; });
      const add = (o) => { scene.add(o); objs.push(o); return o; };
      const load = (k) => {
        clear(); key = k; C = CIRCUITS[k]; st = new State(C.n); step = -1; counts = null; ideal = null; playing = false; playB && playB.classList.remove('on');
        const L0 = ctx.app.labels.length;
        const nc = C.cols.length, x0 = colX(-1, nc) - 0.2, x1 = colX(nc - 1, nc) + 0.7;
        gateMeshes = C.cols.map(() => []);
        blochs = [];
        for (let q = 0; q < C.n; q++) {
          add(U.line([[x0, wy(q), 0], [x1, wy(q), 0]], 0x9fb7e0, 0.8));
          ctx.label(`q${q}`, [x0 - 1.15, wy(q), 0], 'teal small');
          const b = App.Bloch(ctx, { r: 0.3, pos: [x0 - 0.45, wy(q), 0], small: true, labels: false, trailN: 2, opacity: 0.25 }); objs.push(b.group); blochs.push(b);
        }
        C.cols.forEach(([ops], k) => {
          const x = colX(k, nc);
          ops.forEach((op) => {
            const ms = gateMeshes[k];
            if (op.g === 'CX' || op.g === 'CZ' || op.g === 'CP' || op.g === 'SWAP') {
              add(U.tube([[x, wy(op.c), 0], [x, wy(op.t), 0]], 0.025, U.mat(0xe8eef8)));
              if (op.g === 'SWAP') {
                [op.c, op.t].forEach((q) => { const m = add(U.box(0.34, 0.06, 0.06, U.mat(0xe8eef8, { emissive: 0xe0a54a, emissiveIntensity: 0 }), x, wy(q), 0)); m.rotation.z = PI / 4; const m2 = add(m.clone()); m2.rotation.z = -PI / 4; ms.push(m); });
              } else {
                const dc = add(U.sphere(0.11, U.mat(0xe8eef8, { emissive: 0xe0a54a, emissiveIntensity: 0 }), x, wy(op.c), 0)); ms.push(dc);
                if (op.g === 'CX') {
                  const ring = add(new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.03, 8, 32), U.mat(0xe8eef8, { emissive: 0xe0a54a, emissiveIntensity: 0 }))); ring.position.set(x, wy(op.t), 0); ms.push(ring);
                  add(U.box(0.03, 0.4, 0.03, U.mat(0xe8eef8), x, wy(op.t), 0)); add(U.box(0.4, 0.03, 0.03, U.mat(0xe8eef8), x, wy(op.t), 0));
                } else if (op.g === 'CZ') { const d2 = add(U.sphere(0.11, U.mat(0xe8eef8, { emissive: 0xe0a54a, emissiveIntensity: 0 }), x, wy(op.t), 0)); ms.push(d2); }
                else { const b = add(U.box(0.62, 0.44, 0.3, U.mat(COL.CP, { emissive: 0xe0a54a, emissiveIntensity: 0 }), x, wy(op.t), 0)); ms.push(b); ctx.label(op.label, [x, wy(op.t), 0.2], 'plain small'); }
              }
            } else {
              const col = COL[op.g] || 0x1c9db0;
              const b = add(U.box(0.5, 0.5, 0.3, U.mat(col, { emissive: 0xe0a54a, emissiveIntensity: 0 }), x, wy(op.q), 0)); ms.push(b);
              ctx.label(op.g === 'M' ? 'M' : op.label || op.g, [x, wy(op.q), 0.2], 'plain');
            }
          });
        });
        const dx = C.n <= 2 ? 1.3 : C.n === 3 ? 1.0 : 0.6;
        bars = App.AmpBars(ctx, C.n, { pos: [-0.6, -2.2, 1.2], dx, w: dx * 0.6, H: 1.9, labelDz: 0.5 });
        objs.push(bars.group);
        bars.set(st, true);
        tmpFrom(L0);
        cursor.scale.set(1, C.n * 0.8 + 0.2, 1);
        placeCursor();
      };
      const placeCursor = () => { const nc = C.cols.length; cursor.position.set(colX(Math.max(0, step), nc), wy((C.n - 1) / 2), 0); cursor.visible = step >= 0; };
      const sample = () => {
        const p = st.probs(), m = C.meas, K = 1 << m.length;
        ideal = new Array(K).fill(0);
        for (let i = 0; i < st.N; i++) { let k = 0; m.forEach((q, j) => { if ((i >> q) & 1) k |= 1 << j; }); ideal[k] += p[i]; }
        const gates = C.cols.reduce((a, [ops]) => a + ops.filter((o) => o.g !== 'M').length, 0);
        const pg = noise ? 1 - Math.pow(0.99, gates) : 0, pr = noise ? 0.03 : 0;
        counts = new Array(K).fill(0);
        const cdf = []; let a = 0; ideal.forEach((x) => cdf.push((a += x)));
        for (let s = 0; s < 1000; s++) {
          let k;
          if (Math.random() < pg) k = Math.floor(Math.random() * K);
          else { const r = Math.random() * a; k = 0; while (k < K - 1 && r >= cdf[k]) k++; }
          for (let j = 0; j < m.length; j++) if (Math.random() < pr) k ^= 1 << j;
          counts[k]++;
        }
      };
      const doStep = () => {
        if (step >= C.cols.length - 1) return false;
        step++;
        const [ops] = C.cols[step];
        ops.forEach((op) => {
          if (op.g === 'CX') st.cx(op.c, op.t); else if (op.g === 'CZ') st.cz(op.c, op.t);
          else if (op.g === 'CP') st.apply(op.t, App.Q.G.P(op.th), op.c); else if (op.g === 'SWAP') st.swap(op.c, op.t);
          else if (op.g === 'RY') st.gate('RY', op.q, op.th); else if (op.g !== 'M') st.gate(op.g, op.q);
        });
        if (ops.some((o) => o.g === 'M')) sample();
        bars.set(st); placeCursor();
        gateMeshes.forEach((ms, k) => ms.forEach((m) => { m.material.emissiveIntensity = k === step ? 0.8 : 0; }));
        return true;
      };
      const reset = () => { st.reset(); step = -1; counts = null; bars.set(st); placeCursor(); gateMeshes.forEach((ms) => ms.forEach((m) => { m.material.emissiveIntensity = 0; })); };

      const sel = ui.row();
      Object.entries(CIRCUITS).forEach(([k, c]) => { const b = ui.button(c.name, () => { [...sel.children].forEach((x) => x.classList.remove('on')); b.classList.add('on'); load(k); }, sel); if (k === key) b.classList.add('on'); });
      const r = ui.row();
      ui.button('⏮ 重設', reset, r);
      ui.button('單步 ▶', () => { playing = false; playB.classList.remove('on'); doStep(); }, r);
      const playB = ui.button('播放', (b) => { playing = !playing; b.classList.toggle('on', playing); if (playing && step >= C.cols.length - 1) reset(); }, r);
      ui.toggle('加入雜訊（每閘 1%、讀取 3%）', false, (v) => { noise = v; if (counts) sample(); });
      const ro = ui.readout();
      load(key);

      ctx.inset('量測 1000 shots 的結果（青線 = 理想機率）', (g, W, Hh, P) => {
        if (!counts) { P.text(g, '執行到最後的量測欄後顯示', W / 2, Hh / 2, '#9fb0c8', 'center'); return; }
        const m = C.meas, labs = counts.map((_, k) => k.toString(2).padStart(m.length, '0'));
        App.histo(g, W, Hh, P, counts, labs, { ideal, ymax: 1.05, xlabel: `量測位元（${m.slice().reverse().map((q) => 'q' + q).join(' ')}）` });
      });

      return {
        update(t, dt) {
          bars.update(dt);
          for (let q = 0; q < C.n; q++) blochs[q].setV(st.bloch(q), false);
          if (playing) { acc += dt; if (acc > 1.3) { acc = 0; if (!doStep()) { playing = false; playB.classList.remove('on'); } } }
          const lines = [];
          for (let i = 0; i < st.N; i++) if (st.prob(i) > 1e-6) lines.push(`${fmtC(st.re[i], st.im[i])}${ket(i, C.n)}`);
          const note = step < 0 ? '初始狀態：所有量子位元都是 |0⟩' : C.cols[step][1];
          const top = counts ? counts.map((c, k) => [c, k]).sort((a, b) => b[0] - a[0]).slice(0, 3).map(([c, k]) => `${k.toString(2).padStart(C.meas.length, '0')}: ${c}`).join('，') : '';
          ro.innerHTML = `<b>步驟 ${step + 1} / ${C.cols.length}</b>：${note}<br>|ψ⟩ = ${lines.slice(0, 6).join(' + ')}${lines.length > 6 ? ' + …' : ''}` + (counts ? `<br>1000 shots：${top}${noise ? '（含雜訊）' : ''}` : '');
        },
      };
    },
  });
})();

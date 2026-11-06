/* 場景 8：為什麼會比較快？(1) 振幅與干涉 — 路徑相加、相位相消 */
App.register({
  id: 'interference', num: 8, short: '干涉',
  title: '加速的關鍵：振幅會互相抵消',
  subtitle: '機率 = |所有路徑振幅的總和|²；振幅有正負（相位），所以可以抵消',
  desc: `<p>古典機率只會相加；量子<b>振幅</b>是有方向的箭頭（複數），不同路徑的箭頭要先<b>頭尾相接</b>加起來，最後才平方成機率。</p>
<p><b>單一量子位元</b>：H 把 |0⟩ 分成兩條路徑，中間在 |1⟩ 路徑加相位 φ，第二個 H 再合併。φ = 0 時通往 |1⟩ 的兩支箭頭方向相反 → 抵消，結果 100% 是 0；φ = 180° 時反過來。</p>
<p>若中途「偷看」走哪一條路（測量），干涉消失，變成 50/50。</p>
<p><b>n 位元（Deutsch–Jozsa）</b>：2ⁿ 條路徑各帶 (−1)<sup>f(x)</sup> 的符號，全部匯流到 |00…0⟩。函數是常數 → 箭頭同向，完全相長；平衡函數 → 正負各半，完全相消。<b>一次執行就看出 2ⁿ 個值的全域性質</b>。</p>
<p>量子演算法設計的本質：安排相位，讓<b>錯誤答案的振幅互相抵消、正確答案的振幅互相加強</b>。</p>`,
  camera: { pos: [1.6, -0.2, 13.0], target: [1.6, -0.8, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const S2 = Math.SQRT1_2;
    const node = (parent, x, y, label, r = 0.55) => {
      const gg = new THREE.Group(); gg.position.set(x, y, 0); parent.add(gg);
      gg.add(new THREE.Mesh(new THREE.CircleGeometry(r, 48), new THREE.MeshBasicMaterial({ color: 0x13203a, transparent: true, opacity: 0.85 })));
      gg.add(new THREE.Mesh(new THREE.TorusGeometry(r, 0.015, 6, 48), U.glow(0x6f8fbf)));
      const lb = ctx.label(label, [parent.position.x + x, parent.position.y + y - r - 0.3, 0], 'plain small');
      return { gg, lb, arrows: [] };
    };
    const arrowIn = (nd, color, rr = 0.025) => { const a = U.fatArrow(color, 0.3, rr); a.position.z = 0.02; nd.gg.add(a); nd.arrows.push(a); return a; };
    const edge = (parent, a, b, col) => { const m = U.tube([a, b], 0.018, U.mat(col, { emissive: col, emissiveIntensity: 0.25, transparent: true, opacity: 0.7 })); parent.add(m); return m; };

    /* ---------- 模式 A：單一量子位元 ---------- */
    const A = new THREE.Group(); scene.add(A);
    const L = 0.95; // 箭頭長度單位（|振幅| = 1）
    const a0 = node(A, -5, 0, '|0⟩ 起點'), m0 = node(A, -1, 1.6, '|0⟩'), m1 = node(A, -1, -1.6, '|1⟩'), f0 = node(A, 3.5, 1.6, '結果 |0⟩', 0.9), f1 = node(A, 3.5, -1.6, '結果 |1⟩', 0.9);
    const aA = arrowIn(a0, 0xe0a54a), aM0 = arrowIn(m0, 0xe0a54a), aM1 = arrowIn(m1, 0xe0a54a);
    const f0a = arrowIn(f0, 0x4f8cff, 0.02), f0b = arrowIn(f0, 0xff9f43, 0.02), f0s = arrowIn(f0, 0xffffff, 0.035);
    const f1a = arrowIn(f1, 0x4f8cff, 0.02), f1b = arrowIn(f1, 0xff9f43, 0.02), f1s = arrowIn(f1, 0xffffff, 0.035);
    edge(A, [-4.45, 0.2, 0], [-1.55, 1.5, 0], 0xe0a54a); edge(A, [-4.45, -0.2, 0], [-1.55, -1.5, 0], 0xe0a54a);
    edge(A, [-0.45, 1.6, 0], [2.6, 1.6, 0], 0x4f8cff); edge(A, [-0.45, 1.4, 0], [2.65, -1.3, 0], 0x4f8cff);
    edge(A, [-0.45, -1.4, 0], [2.65, 1.3, 0], 0xff9f43); edge(A, [-0.45, -1.6, 0], [2.6, -1.6, 0], 0xff9f43);
    const phBox = U.box(0.55, 0.55, 0.3, U.mat(0x8a5cd0, { emissive: 0x8a5cd0, emissiveIntensity: 0.3 }), 0.6, -1.6, 0); A.add(phBox);
    const labA = [a0.lb, m0.lb, m1.lb, f0.lb, f1.lb,
      ctx.label('H', [-3.0, 0, 0], 'gold big'), ctx.label('H', [1.0, 0.15, 0], 'gold big'), ctx.label('相位 φ', [0.6, -2.15, 0], 'small'),
      ctx.label('+1/√2', [-3.1, 1.15, 0], 'small'), ctx.label('+1/√2', [-3.1, -1.15, 0], 'small'),
      ctx.label('+1/√2', [1.6, 1.9, 0], 'q0 small'), ctx.label('−1/√2', [1.6, -1.9, 0], 'small'),
      ctx.label('藍 = 經由 |0⟩ 的貢獻　橙 = 經由 |1⟩ 的貢獻　白 = 總和', [0, 3.15, 0], 'small')];
    const pf0 = ctx.label('', [3.5, 2.95, 0], 'gold'), pf1 = ctx.label('', [3.5, -2.95, 0], 'gold');
    labA.push(pf0, pf1);
    const eye = U.sphere(0.25, U.mat(0xffffff, { emissive: 0xff5a5f, emissiveIntensity: 0.6 }), -1, 0, 0.3); A.add(eye);
    const eyeL = ctx.label('偵測路徑中', [-1, 0.5, 0], 'q1 small'); labA.push(eyeL);

    /* ---------- 模式 B：Deutsch–Jozsa（n = 3） ---------- */
    const B = new THREE.Group(); scene.add(B);
    const nB = 3, NB = 8;
    const bStart = node(B, -5.2, 0, '|000⟩'), bEnd = node(B, 3.6, 0, '結果 |000⟩', 1.6);
    const bMid = [];
    for (let x = 0; x < NB; x++) {
      const y = (3.5 - x) * 0.82;
      const nd = node(B, -1.2, y, '', 0.33); nd.lb.set(App.Q.ket(x, nB)); nd.lb.pos.set(-1.2 - 0.75, y, 0);
      const ar = arrowIn(nd, 0xe0a54a, 0.018); bMid.push({ nd, ar, y });
      edge(B, [-4.7, 0, 0], [-1.55, y, 0], 0x6f8fbf); edge(B, [-0.85, y, 0], [2.0, 0, 0], 0x6f8fbf);
    }
    const bChain = []; for (let x = 0; x < NB; x++) bChain.push(arrowIn(bEnd, 0xe0a54a, 0.016));
    const bSum = arrowIn(bEnd, 0xffffff, 0.035);
    const labB = [bStart.lb, bEnd.lb, ...bMid.map((m) => m.nd.lb), ctx.label('H⊗³ + Oracle (−1)^{f(x)}', [-3.3, 3.6, 0], 'gold small'), ctx.label('H⊗³', [0.6, 3.0, 0], 'gold small')];
    const pB = ctx.label('', [3.6, 2.2, 0], 'gold'); labB.push(pB);
    const FN = {
      c0: ['常數 f = 0', () => 0], c1: ['常數 f = 1', () => 1], b0: ['平衡 f = x₀', (x) => x & 1],
      bp: ['平衡 f = 奇偶', (x) => (x ^ (x >> 1) ^ (x >> 2)) & 1], rnd: ['隨機（非保證）', null],
    };
    let fkey = 'b0', rnd = [1, 0, 0, 1, 1, 1, 0, 1];
    const fval = (x) => (fkey === 'rnd' ? rnd[x] : FN[fkey][1](x));

    let mode = 'A', phi = 0, which = false, autoSweep = false;
    const setMode = (m) => { mode = m; A.visible = m === 'A'; B.visible = m === 'B'; labA.forEach((l) => l.show(m === 'A')); labB.forEach((l) => l.show(m === 'B')); };
    ui.radio([['A', '單一量子位元：兩條路徑'], ['B', '3 位元：8 條路徑（Deutsch–Jozsa）']], mode, setMode);
    const phS = ui.slider('A：相位 φ', 0, 360, 1, phi, (v) => { phi = v; }, (v) => v + '°');
    ui.toggle('A：自動掃描 φ', false, (v) => { autoSweep = v; });
    ui.toggle('A：中途偵測路徑（破壞干涉）', false, (v) => { which = v; });
    const fr = ui.radio(Object.entries(FN).map(([k, [n]]) => [k, n]), fkey, (k) => { fkey = k; if (k === 'rnd') rnd = rnd.map(() => (Math.random() < 0.5 ? 1 : 0)); });
    void fr;
    const ro = ui.readout();
    setMode('A');

    ctx.inset('', (g, W, H, P) => {
      if (mode === 'A') {
        document.getElementById('inset-title').textContent = '結果 P(0) 與 φ 的關係（干涉條紋）';
        const { X, Y } = P.frame(g, W, H, [0, 360], [0, 1], { xlabel: '相位 φ（度）', ylabel: 'P(0)', xticks: [[0, '0'], [90, '90'], [180, '180'], [270, '270'], [360, '360']], yticks: [[0, '0'], [0.5, '0.5'], [1, '1']] });
        P.curve(g, (x) => Math.cos((x * Math.PI) / 360) ** 2, 0, 360, X, Y, '#e0a54a', 2);
        g.strokeStyle = '#ff5a5f'; g.setLineDash([4, 4]); g.beginPath(); g.moveTo(X(0), Y(0.5)); g.lineTo(X(360), Y(0.5)); g.stroke(); g.setLineDash([]);
        P.text(g, '偵測路徑時：0.5', X(250), Y(0.5) - 6, '#ffb0b2');
        P.dot(g, X(phi), Y(which ? 0.5 : Math.cos((phi * Math.PI) / 360) ** 2), 5, '#fff');
      } else {
        document.getElementById('inset-title').textContent = '最後量測的機率分佈（8 種結果）';
        const st = new App.Q.State(3); for (let q = 0; q < 3; q++) st.gate('H', q); st.oracle(fval); for (let q = 0; q < 3; q++) st.gate('H', q);
        const p = st.probs(); App.histo(g, W, H, P, Array.from(p).map((x) => Math.round(x * 1000)), [...Array(8).keys()].map((k) => k.toString(2).padStart(3, '0')), { ymax: 1.05, color: (i) => (i === 0 ? '#e0a54a' : '#4f8cff') });
      }
    });

    return {
      update(t, dt) {
        if (mode === 'A') {
          if (autoSweep) { phi = (phi + dt * 40) % 360; phS.show(Math.round(phi)); }
          const p = (phi * Math.PI) / 180;
          aA.setVec(new THREE.Vector3(L, 0, 0));
          aM0.setVec(new THREE.Vector3(L * S2, 0, 0));
          aM1.setVec(new THREE.Vector3(L * S2 * Math.cos(p), L * S2 * Math.sin(p), 0));
          // 到 |0⟩：0.5 + 0.5 e^{iφ}；到 |1⟩：0.5 − 0.5 e^{iφ}
          const K = 1.6;
          const c0a = [0.5, 0], c0b = [0.5 * Math.cos(p), 0.5 * Math.sin(p)], c1a = [0.5, 0], c1b = [-0.5 * Math.cos(p), -0.5 * Math.sin(p)];
          const put = (a, b, s, ca, cb) => {
            a.position.set(0, 0, 0.02); a.setVec(new THREE.Vector3(ca[0] * K, ca[1] * K, 0));
            b.position.set(ca[0] * K, ca[1] * K, 0.03); b.setVec(new THREE.Vector3(cb[0] * K, cb[1] * K, 0));
            const sx = ca[0] + cb[0], sy = ca[1] + cb[1];
            s.visible = !which; if (!which) s.setVec(new THREE.Vector3(sx * K, sy * K, 0)); s.position.z = 0.04;
            return sx * sx + sy * sy;
          };
          let P0 = put(f0a, f0b, f0s, c0a, c0b), P1 = put(f1a, f1b, f1s, c1a, c1b);
          if (which) { P0 = 0.5; P1 = 0.5; }
          eye.visible = which; eyeL.show(which && mode === 'A');
          pf0.set(`P(0) = ${P0.toFixed(2)}`); pf1.set(`P(1) = ${P1.toFixed(2)}`);
          ro.innerHTML = `φ = ${Math.round(phi)}°<br>到 |0⟩ 的振幅 = ½ + ½e<sup>iφ</sup>　→　P(0) = cos²(φ/2) = ${P0.toFixed(3)}<br>到 |1⟩ 的振幅 = ½ − ½e<sup>iφ</sup>　→　P(1) = sin²(φ/2) = ${P1.toFixed(3)}` +
            (which ? '<br><b style="color:#ff9be6">已偵測路徑：振幅不再相加，只剩機率相加 → 50/50</b>' : '');
        } else {
          const K = 2.6 / NB; let sx = 0;
          let px = -1.3;
          for (let x = 0; x < NB; x++) {
            const s = fval(x) ? -1 : 1;
            bMid[x].ar.setVec(new THREE.Vector3(0.3 * s, 0, 0));
            bChain[x].position.set(px, (x - 3.5) * 0.13, 0.02 + x * 0.002);
            bChain[x].setVec(new THREE.Vector3(s * K, 0, 0));
            px += s * K; sx += s / NB;
          }
          bSum.position.set(-1.3, -0.45, 0.05); bSum.setVec(new THREE.Vector3(sx * 2.6, 0, 0));
          const P0 = sx * sx;
          pB.set(`P(000) = ${P0.toFixed(2)}`);
          const ones = [...Array(NB).keys()].filter((x) => fval(x)).length;
          ro.innerHTML = `函數：${FN[fkey][0]}　f(x) = 1 的有 ${ones} 個<br>|000⟩ 的振幅 = (1/8)·Σ(−1)<sup>f(x)</sup> = ${sx.toFixed(3)}　→　P(000) = ${P0.toFixed(3)}<br>` +
            (P0 > 0.99 ? '<b>常數函數：完全相長</b>' : P0 < 1e-9 ? '<b>平衡函數：完全相消</b>' : '一般函數：部分抵消') + '　（古典最壞要查 2ⁿ⁻¹+1 = 5 次）';
        }
      },
    };
  },
});

/* 離子阱場景 4：離子鏈的平衡位置與集體振動模態（軸向 / 徑向） */
App.register({
  id: 'modes', num: 4, short: '離子鏈集體振動',
  title: '離子鏈的集體振動：量子匯流排',
  subtitle: '離子之間靠庫侖力連在一起，像彈簧串起的珠子；共享的振動模態就是傳遞量子資訊的「匯流排」',
  desc: `<p><b>平衡位置</b>：軸向是諧振位勢（頻率 ω<sub>z</sub>），離子又互相排斥，於是排成一列，中間較密、兩端較疏。以長度單位 ℓ = (e²/4πε₀mω<sub>z</sub>²)<sup>1/3</sup> 無因次化後求解 <span class="eq">u<sub>i</sub> = Σ<sub>j≠i</sub> sgn(u<sub>i</sub>−u<sub>j</sub>)/(u<sub>i</sub>−u<sub>j</sub>)²</span>。</p>
<p><b>正規模態</b>：在平衡點把位能展開到二次項，對 Hessian 做特徵分解。<b>軸向</b>：最低的是 <b>COM（質心）模</b>，所有離子一起動，頻率 = ω<sub>z</sub>；第二個是<b>呼吸模</b>，頻率 = √3 ω<sub>z</sub>（與 N 無關）。<b>徑向</b>：COM 頻率最高 = ω<sub>r</sub>，其他模往下排。</p>
<p><b>為什麼重要</b>：雷射可以讓「某顆離子的自旋」推動「整條鏈的某個模態」，模態再影響另一顆離子 → 同一條鏈裡<b>任兩顆離子都能直接做兩位元閘（全連接）</b>。</p>
<p><b>擴展的代價</b>：N 變大時模態越擠越密、雷射難以單獨定址，閘也變慢；ω<sub>r</sub>/ω<sub>z</sub> 不夠大時鏈會折成鋸齒形。所以大系統把離子分成很多短鏈，靠<b>搬運（QCCD）</b>或<b>光子互連</b>連接。</p>`,
  camera: { pos: [0, 2.6, 8.8], target: [0, 0.75, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    let N = 5, axial = true, mode = 1, ratio = 5;
    // 背景：線性阱的電極（淡）
    [[1, 1], [-1, -1], [1, -1], [-1, 1]].forEach(([a, b], k) => {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 7.6, 16), U.metal(k < 2 ? 0xd9a441 : 0x8a93a0, { transparent: true, opacity: 0.35 }));
      m.rotation.z = Math.PI / 2; m.position.set(0, 0.75 + a * 0.75, b * 0.75); scene.add(m);
    });
    const axis = U.line([[-3.9, 0.75, 0], [3.9, 0.75, 0]], 0x5d6878, 0.6); scene.add(axis);
    const MAX = 12;
    const ions = [], ghosts = [], arrows = [], lbIdx = [];
    for (let i = 0; i < MAX; i++) {
      ions.push(App.particle(scene, App.QC.ion, 0.1));
      const gh = U.sphere(0.1, new THREE.MeshBasicMaterial({ color: 0x9fb0c8, wireframe: true, transparent: true, opacity: 0.35 }), 0, 0, 0, 12); scene.add(gh); ghosts.push(gh);
      const ar = U.fatArrow(0x8ef0ff, 0.5, 0.025); scene.add(ar); arrows.push(ar);
    }
    const lbMode = ctx.label('', [0, 2.35, 0], 'gold');
    const lbNote = ctx.label('', [0, -0.55, 0], 'small');

    /* ---------- 平衡位置（牛頓法）與 Hessian ---------- */
    let u = [], Ax = null, eigA = null, eigR = null, scale = 1;
    const solve = () => {
      u = Array.from({ length: N }, (_, i) => (i - (N - 1) / 2) * (2.2 / Math.pow(N, 0.44)));
      for (let it = 0; it < 200; it++) {
        const g = u.map((ui_, i) => ui_ - u.reduce((s, uj, j) => (j === i ? s : s + Math.sign(ui_ - uj) / ((ui_ - uj) ** 2)), 0));
        const Hm = hess(u);
        // 解 Hm Δ = g（小矩陣高斯消去）
        const d = gaussSolve(Hm.map((r) => r.slice()), g.slice());
        let m = 0; u = u.map((x, i) => { m = Math.max(m, Math.abs(d[i])); return x - d[i]; });
        if (m < 1e-12) break;
      }
      Ax = hess(u);
      eigA = U.eigSym(Ax); // 遞增：COM（1）、呼吸（3）…
      const Rm = Ax.map((r, i) => r.map((x, j) => (i === j ? ratio * ratio - (x - 1) / 2 : -x / 2)));
      const er = U.eigSym(Rm);
      eigR = { values: er.values.slice().reverse(), vectors: er.vectors.slice().reverse() }; // 遞減：COM 最高
      const span = u[N - 1] - u[0] || 1;
      scale = Math.min(1.25, 6.4 / span);
    };
    function hess(x) {
      const n = x.length; const Hm = Array.from({ length: n }, () => new Array(n).fill(0));
      for (let i = 0; i < n; i++) {
        let s = 1;
        for (let j = 0; j < n; j++) if (j !== i) { const c = 2 / Math.abs(x[i] - x[j]) ** 3; s += c; Hm[i][j] = -c; }
        Hm[i][i] = s;
      }
      return Hm;
    }
    function gaussSolve(M, b) {
      const n = b.length;
      for (let c = 0; c < n; c++) {
        let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
        [M[c], M[p]] = [M[p], M[c]]; [b[c], b[p]] = [b[p], b[c]];
        for (let r = c + 1; r < n; r++) { const f = M[r][c] / M[c][c]; for (let k = c; k < n; k++) M[r][k] -= f * M[c][k]; b[r] -= f * b[c]; }
      }
      const x = new Array(n).fill(0);
      for (let r = n - 1; r >= 0; r--) { let s = b[r]; for (let k = r + 1; k < n; k++) s -= M[r][k] * x[k]; x[r] = s / M[r][r]; }
      return x;
    }
    const modeName = (k) => (axial ? (k === 1 ? 'COM（質心）模' : k === 2 ? '呼吸模（breathing）' : `第 ${k} 軸向模`) : (k === 1 ? '徑向 COM 模' : k === 2 ? '徑向傾斜（rocking）模' : `第 ${k} 徑向模`));
    const ro = ui.readout();
    const info = () => {
      const k = Math.min(mode, N);
      const ev = axial ? eigA.values[k - 1] : eigR.values[k - 1];
      const zig = eigR.values[N - 1] <= 0;
      const w = ev > 0 ? Math.sqrt(ev) : NaN;
      lbMode.set(`${modeName(k)}：ω = ${isNaN(w) ? '虛數（不穩定）' : w.toFixed(3) + ' ω_z'}`);
      lbNote.set(zig ? '⚠ ω_r/ω_z 太小：最低徑向模頻率變虛數 → 鏈折成鋸齒形（zigzag）' : (axial ? '箭頭 = 各離子在此模態中的相對位移（沿軸向）' : '箭頭 = 各離子在此模態中的相對位移（垂直於軸）'));
      const lowR = eigR.values[N - 1];
      ro.innerHTML = `N = ${N}，顯示：${axial ? '軸向' : '徑向'}第 ${k} 模${mode > N ? `（模式編號超過 N，改顯示第 ${N} 模）` : ''}<br>`
        + `軸向：COM = 1.000 ω_z、呼吸 = ${eigA.values.length > 1 ? Math.sqrt(eigA.values[1]).toFixed(3) : '—'} ω_z（≈ √3）、最高 = ${Math.sqrt(eigA.values[N - 1]).toFixed(3)} ω_z<br>`
        + `徑向（ω_r = ${ratio} ω_z）：COM = ${Math.sqrt(eigR.values[0]).toFixed(3)} ω_z、最低 = ${lowR > 0 ? Math.sqrt(lowR).toFixed(3) + ' ω_z' : '不穩定'}<br>`
        + `相鄰徑向模最小間距：${minGap(eigR.values).toFixed(3)} ω_z（越小越難單獨定址）`;
    };
    const minGap = (vals) => { const w = vals.map((x) => Math.sqrt(Math.max(0, x))); let m = Infinity; for (let i = 1; i < w.length; i++) m = Math.min(m, Math.abs(w[i] - w[i - 1])); return isFinite(m) ? m : 0; };
    ui.radio([['ax', '軸向模態'], ['rad', '徑向模態']], 'ax', (v) => { axial = v === 'ax'; info(); });
    ui.slider('離子數 N', 2, 12, 1, N, (v) => { N = v; solve(); info(); }, (v) => v);
    ui.slider('模式編號', 1, 12, 1, mode, (v) => { mode = v; info(); }, (v) => v);
    ui.slider('徑向/軸向頻率比 ω_r/ω_z', 1.5, 10, 0.1, ratio, (v) => { ratio = v; solve(); info(); }, (v) => v.toFixed(1));
    solve(); info();
    ctx.inset('模態頻率譜（藍：軸向，紅：徑向）', (g, W, H, P) => {
      const top = Math.max(ratio, Math.sqrt(eigA.values[N - 1])) * 1.08;
      const { X, Y } = P.frame(g, W, H, [0, top], [0, 1], { xlabel: '頻率 ω / ω_z', xticks: [[0, '0'], [1, '1'], [Math.sqrt(3), '√3'], [Math.floor(top), String(Math.floor(top))]], m: { l: 14, b: 32 } });
      const k = Math.min(mode, N);
      eigA.values.forEach((x, i) => { const w = Math.sqrt(x); g.strokeStyle = axial && i === k - 1 ? '#ffffff' : '#4f8cff'; g.lineWidth = axial && i === k - 1 ? 3 : 2; g.beginPath(); g.moveTo(X(w), Y(0)); g.lineTo(X(w), Y(0.45)); g.stroke(); });
      eigR.values.forEach((x, i) => { if (x <= 0) return; const w = Math.sqrt(x); g.strokeStyle = !axial && i === k - 1 ? '#ffffff' : '#ff5a5f'; g.lineWidth = !axial && i === k - 1 ? 3 : 2; g.beginPath(); g.moveTo(X(w), Y(0.5)); g.lineTo(X(w), Y(0.95)); g.stroke(); });
      P.text(g, '軸向 COM', X(1) + 4, Y(0.38), '#a9c6ff');
      P.text(g, '徑向 COM', X(Math.sqrt(eigR.values[0])) - 4, Y(0.98) + 12, '#ffb0b2', 'right');
      P.text(g, '徑向模擠在 ω_r 下方', X(top * 0.55), Y(0.6), '#cfd8e6', 'center');
    });
    return {
      update(time) {
        const k = Math.min(mode, N);
        const ev = axial ? eigA.values[k - 1] : eigR.values[k - 1];
        const vecs = axial ? eigA.vectors[k - 1] : eigR.vectors[k - 1];
        const w = ev > 0 ? Math.sqrt(ev) : 0;
        const ph = Math.sin(time * 2 * Math.PI * 0.55 * (axial ? w : w / Math.max(1, ratio / 2)));
        const nrm = Math.max(...vecs.map(Math.abs)) || 1;
        for (let i = 0; i < MAX; i++) {
          const on = i < N;
          ions[i].visible = on; ghosts[i].visible = on; arrows[i].visible = on;
          if (!on) continue;
          const x0 = u[i] * scale, d = (0.32 * vecs[i]) / nrm;
          ghosts[i].position.set(x0, 0.75, 0);
          ions[i].position.set(x0 + (axial ? d * ph : 0), 0.75 + (axial ? 0 : d * ph * 1.4), 0);
          ions[i].glow(0.6);
          arrows[i].position.set(x0, axial ? 1.1 : 0.75, 0);
          arrows[i].setVec(axial ? new THREE.Vector3(d * 1.4, 0, 0) : new THREE.Vector3(0, d * 1.6, 0));
          if (Math.abs(d) < 0.01) arrows[i].visible = false;
        }
      },
    };
  },
});

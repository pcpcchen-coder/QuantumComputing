/* 場景 11：錯誤與量子錯誤更正 — 旋轉表面碼、穩定子量測、症狀、解碼、邏輯錯誤率 */
App.register({
  id: 'qec', num: 11, short: '錯誤更正',
  title: '雜訊與量子錯誤更正：表面碼',
  subtitle: '用很多實體量子位元編碼 1 個邏輯量子位元；只量「奇偶」不量資料',
  desc: `<p>白球是<b>資料量子位元</b>（d×d 個），方塊是<b>量測量子位元</b>：青色方塊檢查周圍 X 錯誤的奇偶（Z 型穩定子），紫色檢查 Z 錯誤（X 型）。量奇偶不會破壞編碼的量子資訊。</p>
<p>每一輪：① 隨機發生錯誤（紅球）→ ② 量測穩定子，奇偶改變的方塊亮橘色（<b>症狀</b>）→ ③ <b>解碼器</b>把症狀兩兩配對（或連到上下邊界），猜出最可能的錯誤鏈（綠線）→ ④ 修正。</p>
<p>如果剩下的錯誤剛好形成一條「由上貫穿到下」的鏈，就是<b>邏輯錯誤</b>。</p>
<p>關鍵：實體錯誤率低於<b>門檻</b>時，碼距 d 越大，邏輯錯誤率呈指數下降（插圖，本頁即時蒙地卡羅模擬）。Google Willow（2024）首次在硬體上看到這個趨勢：d = 3→5→7，每次邏輯錯誤率約減半。</p>
<p>（本場景只示範 X 錯誤、不含量測錯誤，解碼器為最小權重配對。）</p>`,
  camera: { pos: [0, 7.5, 7.5], target: [0, 0, 0.3] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    let d = 5, p = 0.05, objs = [], data = [], zp = [], err = [], defects = [], paths = [], phase = 0, auto = true, acc = 0, stats = { n: 0, fail: 0 }, status = '';
    const s = 1.0;
    const clear = () => { objs.forEach((o) => scene.remove(o)); objs = []; ctx.app.labels.forEach((L) => { if (L.tmp) L.el.remove(); }); ctx.app.labels = ctx.app.labels.filter((L) => !L.tmp); };
    const add = (o) => { scene.add(o); objs.push(o); return o; };
    const XP = (j) => (j - (d - 1) / 2) * s, ZP = (i) => (i - (d - 1) / 2) * s;
    const isZ = (i, j) => (i + j) % 2 === 1;
    const zValid = (i, j) => isZ(i, j) && i >= 1 && i <= d - 1 && j >= 0 && j <= d;
    const xValid = (i, j) => !isZ(i, j) && j >= 1 && j <= d - 1 && i >= 0 && i <= d;
    const dataOf = (i, j) => [[i - 1, j - 1], [i - 1, j], [i, j - 1], [i, j]].filter(([a, b]) => a >= 0 && a < d && b >= 0 && b < d);
    const setup = () => {
      clear(); const L0 = ctx.app.labels.length;
      data = []; zp = []; err = new Array(d * d).fill(0); defects = []; paths = []; phase = 0; stats = { n: 0, fail: 0 }; status = '';
      add(U.box(d * s + 1.4, 0.06, d * s + 1.4, U.mat(0x0f1828, { roughness: 0.95 }), 0, -0.12, 0));
      for (let i = 0; i <= d; i++) for (let j = 0; j <= d; j++) {
        const zv = zValid(i, j), xv = xValid(i, j);
        if (!zv && !xv) continue;
        const inner = i >= 1 && i <= d - 1 && j >= 1 && j <= d - 1;
        const w = inner ? s * 0.92 : s * 0.5;
        let cx = XP(j - 0.5), cz = ZP(i - 0.5);
        if (!inner) { if (j === 0) cx += s * 0.22; if (j === d) cx -= s * 0.22; if (i === 0) cz += s * 0.22; if (i === d) cz -= s * 0.22; }
        const ww = inner ? w : (j === 0 || j === d ? s * 0.45 : s * 0.92), dd = inner ? w : (i === 0 || i === d ? s * 0.45 : s * 0.92);
        const col = zv ? 0x1c9db0 : 0x8a5cd0;
        const m = add(U.box(ww, 0.05, dd, U.mat(col, { emissive: col, emissiveIntensity: 0.1, transparent: true, opacity: zv ? 0.75 : 0.35 }), cx, -0.06, cz));
        if (zv) {
          const pil = add(U.box(0.14, 1, 0.14, U.glow(0xff9f43), cx, 0.5, cz)); pil.visible = false;
          zp.push({ i, j, m, pil, on: false, dq: dataOf(i, j) });
        }
      }
      for (let i = 0; i < d; i++) for (let j = 0; j < d; j++) data.push(add(U.sphere(0.17, U.mat(0xe8eef8, { emissive: 0xff2020, emissiveIntensity: 0 }), XP(j), 0.12, ZP(i))));
      ctx.label('上邊界', [0, 0, ZP(-0.5) - 0.55], 'small'); ctx.label('下邊界', [0, 0, ZP(d - 0.5) + 0.55], 'small');
      ctx.label(`邏輯量子位元：d = ${d}，${d * d} 資料 + ${d * d - 1} 量測 = ${2 * d * d - 1} 實體量子位元`, [0, 0.9, ZP(-0.5) - 1.1], 'gold small');
      for (let k = ctx.app.labels.length - 1; k >= L0; k--) ctx.app.labels[k].tmp = true;
      refresh();
    };
    const syndrome = (E) => zp.map((q) => q.dq.reduce((a, [x, y]) => a ^ E[x * d + y], 0));
    /* 最小權重完美配對（症狀 ≤ 14 個時用位元遮罩 DP 求精確解，否則用貪婪法）；b = −1 表示連到邊界 */
    const matchDefects = (k, bw, dist) => {
      if (!k) return [];
      if (k > 14) {
        const edges = [];
        for (let a = 0; a < k; a++) { edges.push([bw[a] + 0.5, a, -1]); for (let b = a + 1; b < k; b++) { const w = dist(a, b); if (w <= bw[a] + bw[b]) edges.push([w, a, b]); } }
        edges.sort((x, y) => x[0] - y[0]);
        const used = new Array(k).fill(false), out = [];
        for (const [, a, b] of edges) { if (used[a]) continue; if (b < 0) { used[a] = true; out.push([a, -1]); } else if (!used[b]) { used[a] = used[b] = true; out.push([a, b]); } }
        return out;
      }
      const full = (1 << k) - 1, memo = new Float64Array(1 << k).fill(-1), choice = new Int8Array(1 << k);
      const f = (mask) => {
        if (mask === full) return 0;
        if (memo[mask] >= 0) return memo[mask];
        let i = 0; while (mask & (1 << i)) i++;
        let best = bw[i] + f(mask | (1 << i)), bc = -1;
        for (let j = i + 1; j < k; j++) if (!(mask & (1 << j))) { const c = dist(i, j) + f(mask | (1 << i) | (1 << j)); if (c < best) { best = c; bc = j; } }
        memo[mask] = best; choice[mask] = bc; return best;
      };
      f(0);
      const out = []; let mask = 0;
      while (mask !== full) { let i = 0; while (mask & (1 << i)) i++; const j = choice[mask]; out.push([i, j]); mask |= (1 << i) | (j >= 0 ? 1 << j : 0); }
      return out;
    };
    /* 解碼：回傳要翻轉的資料量子位元與路徑 */
    const decode = (E) => {
      const syn = syndrome(E), D = [];
      zp.forEach((q, k) => { if (syn[k]) D.push(q); });
      const bw = D.map((q) => Math.min(q.i, d - q.i));
      const dist = (a, b) => Math.max(Math.abs(D[a].i - D[b].i), Math.abs(D[a].j - D[b].j));
      const pairs = matchDefects(D.length, bw, dist);
      const flips = [], segs = [];
      const walk = (i, j, ti, tj, toEdge) => {
        const pts = [[i, j]];
        let guard = 0;
        while (guard++ < 4 * d) {
          if (toEdge === 'top' && i === 0) break; if (toEdge === 'bot' && i === d) break;
          if (!toEdge && i === ti && j === tj) break;
          let si, sj;
          if (toEdge) si = toEdge === 'top' ? -1 : 1; else si = ti > i ? 1 : ti < i ? -1 : i < d ? 1 : -1;
          if (toEdge) sj = pts.length % 2 ? 1 : -1; else sj = tj > j ? 1 : tj < j ? -1 : j < d ? 1 : -1;
          if (j === 0) sj = 1; else if (j === d) sj = -1;
          const a = i + (si > 0 ? 0 : -1), b = j + (sj > 0 ? 0 : -1);
          if (a >= 0 && a < d && b >= 0 && b < d) flips.push(a * d + b);
          i += si; j += sj; pts.push([i, j]);
        }
        segs.push(pts);
      };
      for (const [a, b] of pairs) {
        if (b < 0) walk(D[a].i, D[a].j, 0, 0, D[a].i <= d - D[a].i ? 'top' : 'bot');
        else walk(D[a].i, D[a].j, D[b].i, D[b].j, null);
      }
      return { flips, segs, D };
    };
    const logicalFail = (E) => { let par = 0; for (let j = 0; j < d; j++) par ^= E[j]; return par === 1; };
    const trial = (dd, pp) => { // 給蒙地卡羅用（暫時切換 d）
      const E = new Array(dd * dd); for (let k = 0; k < dd * dd; k++) E[k] = Math.random() < pp ? 1 : 0;
      const { flips } = decode(E); flips.forEach((k) => { E[k] ^= 1; }); return logicalFail(E);
    };
    const refresh = () => {
      data.forEach((m, k) => { m.material.emissiveIntensity = err[k] ? 1.4 : 0; m.material.color.set(err[k] ? 0xff6060 : 0xe8eef8); });
      const syn = syndrome(err);
      zp.forEach((q, k) => { const on = phase >= 1 && syn[k]; q.pil.visible = !!on; q.m.material.emissive.set(on ? 0xff9f43 : 0x1c9db0); q.m.material.emissiveIntensity = on ? 0.9 : 0.1; });
    };
    let pathObjs = [];
    const drawPaths = (segs) => {
      pathObjs.forEach((o) => scene.remove(o)); pathObjs = [];
      segs.forEach((pts) => { if (pts.length < 2) return; const m = U.tube(pts.map(([i, j]) => [XP(j - 0.5), 0.35, ZP(i - 0.5)]), 0.05, U.glow(0x66ffcc)); scene.add(m); pathObjs.push(m); objs.push(m); });
    };
    let dec = null;
    const stepCycle = () => {
      if (phase === 0) { for (let k = 0; k < d * d; k++) err[k] = Math.random() < p ? 1 : 0; phase = 0.5; status = '① 發生隨機錯誤（紅球）'; drawPaths([]); refresh(); return; }
      if (phase === 0.5) { phase = 1; status = '② 量測穩定子：亮起的方塊 = 症狀'; refresh(); return; }
      if (phase === 1) { dec = decode(err); drawPaths(dec.segs); phase = 2; status = `③ 解碼：配對 ${dec.D.length} 個症狀（綠線 = 推測的錯誤鏈）`; return; }
      if (phase === 2) {
        dec.flips.forEach((k) => { err[k] ^= 1; });
        const fail = logicalFail(err); stats.n++; if (fail) stats.fail++;
        status = fail ? '④ 修正後殘留一條貫穿上下的鏈 → <b style="color:#ff8080">邏輯錯誤 ✗</b>' : '④ 修正完成 → <b style="color:#66ffcc">邏輯資訊保住了 ✓</b>';
        phase = 3; refresh(); return;
      }
      err.fill(0); phase = 0; drawPaths([]); refresh(); status = '下一輪';
    };
    ui.radio([[3, 'd = 3'], [5, 'd = 5'], [7, 'd = 7']], d, (v) => { d = v; setup(); });
    ui.slider('實體錯誤率 p（每個資料量子位元）', 0.005, 0.2, 0.005, p, (v) => { p = v; stats = { n: 0, fail: 0 }; }, (v) => (v * 100).toFixed(1) + '%');
    const r = ui.row();
    ui.toggle('自動循環', auto, (v) => { auto = v; });
    ui.button('下一步', () => { auto = false; stepCycle(); }, r);
    ui.button('跑 2000 輪（只統計）', () => { for (let k = 0; k < 2000; k++) { stats.n++; if (trial(d, p)) stats.fail++; } }, r);
    const ro = ui.readout();
    setup();

    // 蒙地卡羅：邏輯錯誤率 vs 實體錯誤率（逐幀計算）
    const PS = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2];
    const DS = [3, 5, 7], TR = 1000;
    const mc = DS.map(() => PS.map(() => null));
    let mcI = 0;
    const mcStep = () => {
      if (mcI >= DS.length * PS.length) return;
      const di = Math.floor(mcI / PS.length), pi = mcI % PS.length;
      const save = d; d = DS[di]; let f = 0; for (let k = 0; k < TR; k++) if (trial(d, PS[pi])) f++; d = save;
      mc[di][pi] = Math.max(f, 0.5) / TR; mcI++;
    };
    // trial() 依賴 zp（目前 d 的穩定子），因此另建各 d 的 zp
    const zpFor = {};
    const buildZp = (dd) => { const list = []; for (let i = 0; i <= dd; i++) for (let j = 0; j <= dd; j++) if ((i + j) % 2 === 1 && i >= 1 && i <= dd - 1 && j >= 0 && j <= dd) list.push({ i, j, dq: [[i - 1, j - 1], [i - 1, j], [i, j - 1], [i, j]].filter(([a, b]) => a >= 0 && a < dd && b >= 0 && b < dd) }); return list; };
    DS.forEach((dd) => { zpFor[dd] = buildZp(dd); });
    const runMC = () => { const zSave = zp; for (let k = 0; k < 1 && mcI < DS.length * PS.length; k++) { zp = zpFor[DS[Math.floor(mcI / PS.length)]]; mcStep(); } zp = zSave; };

    ctx.inset('邏輯錯誤率 vs 實體錯誤率（即時蒙地卡羅）', (g, W, H, P) => {
      const lx = (x) => Math.log10(x), ly = (y) => Math.log10(y);
      const { X, Y } = P.frame(g, W, H, [lx(0.01), lx(0.2)], [-3.3, 0], { xlabel: '實體錯誤率 p', ylabel: '邏輯錯誤率', xticks: [[lx(0.01), '1%'], [lx(0.03), '3%'], [lx(0.1), '10%'], [lx(0.2), '20%']], yticks: [[-3, '0.1%'], [-2, '1%'], [-1, '10%'], [0, '100%']] });
      g.strokeStyle = 'rgba(255,255,255,.35)'; g.setLineDash([4, 4]); g.beginPath(); g.moveTo(X(lx(0.01)), Y(-2)); g.lineTo(X(lx(0.2)), Y(ly(0.2))); g.stroke(); g.setLineDash([]);
      P.text(g, '未編碼 = p', X(lx(0.012)), Y(-2) - 6, '#9fb0c8');
      const cols = ['#4f8cff', '#e0a54a', '#ff5a5f'];
      DS.forEach((dd, di) => {
        g.strokeStyle = cols[di]; g.lineWidth = 2; g.beginPath(); let st = false;
        PS.forEach((pp, pi) => { const v = mc[di][pi]; if (v === null) return; const x = X(lx(pp)), y = Y(Math.max(-3.3, ly(v))); st ? g.lineTo(x, y) : g.moveTo(x, y); st = true; });
        g.stroke(); P.text(g, `d=${dd}`, W - 40, 20 + di * 16, cols[di]);
      });
      g.strokeStyle = '#fff'; g.beginPath(); g.moveTo(X(lx(Math.max(0.01, p))), Y(-3.3)); g.lineTo(X(lx(Math.max(0.01, p))), Y(0)); g.stroke();
      if (mcI < DS.length * PS.length) P.text(g, `模擬中… ${Math.round((100 * mcI) / (DS.length * PS.length))}%`, X(lx(0.013)), Y(-3.0), '#9fb0c8');
    });

    return {
      update(t, dt) {
        runMC();
        if (auto) { acc += dt; if (acc > 0.9) { acc = 0; stepCycle(); } }
        ro.innerHTML = `${status}<br>統計：${stats.n} 輪中邏輯錯誤 ${stats.fail} 次 → 邏輯錯誤率 ≈ ${stats.n ? ((100 * stats.fail) / stats.n).toFixed(2) : '—'}%（實體 ${(p * 100).toFixed(1)}%）<br>` +
          `碼距 d = ${d}：最多可修正 ${Math.floor((d - 1) / 2)} 個錯誤`;
      },
    };
  },
});

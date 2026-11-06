/* 場景 10：Shor 演算法的核心 — 量子週期尋找（模指數 + QFT），以 N = 15 / 21 示範 */
App.register({
  id: 'shor', num: 10, short: 'Shor 週期尋找',
  title: 'Shor 演算法：用 QFT 找週期，進而分解質因數',
  subtitle: '分解 N ⇐ 找 f(x) = aˣ mod N 的週期 r ⇐ 量子傅立葉轉換',
  desc: `<p>分解 N 可以轉換成「找週期」：選一個 a，函數 f(x) = aˣ mod N 是週期函數，週期 r 若為偶數，gcd(a<sup>r/2</sup> ± 1, N) 通常就是 N 的因數。</p>
<p>① x 暫存器（6 個量子位元，64 個值）做 H → 均勻疊加。</p>
<p>② 量子電路計算 f(x) 存到第二個暫存器（顏色 = f(x) 的值）：<b>一次算出全部 64 個 f(x)</b>，但還讀不出來。</p>
<p>③ 量測第二個暫存器 → 只剩 f(x) 相同的那些 x：間隔正好是 r 的「梳子」。</p>
<p>④ 對 x 暫存器做 <b>QFT</b>：梳子的間隔 r 變成峰值位置 64·k/r（干涉讓其他位置抵消）。</p>
<p>⑤ 量測得到 y，用連分數從 y/64 ≈ k/r 推出 r，再用古典電腦算 gcd。</p>
<p>古典最好的演算法需要「次指數」時間；Shor 只需多項式時間 —— 這就是 RSA 會被威脅的原因。</p>`,
  camera: { pos: [0.4, 2.6, 12.5], target: [0.4, 0.5, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const Q = 64, nq = 6;
    const gcd = (a, b) => (b ? gcd(b, a % b) : a);
    const powmod = (a, e, m) => { let r = 1; a %= m; while (e > 0) { if (e & 1) r = (r * a) % m; a = (a * a) % m; e >>= 1; } return r; };
    const order = (a, N) => { for (let r = 1; r <= N; r++) if (powmod(a, r, N) === 1) return r; return 0; };
    let N = 15, a = 7, step = 0, f0 = null, yMeas = null, probs = new Float64Array(Q), autoRun = false, acc = 0;
    // 柱子
    const dx = 0.15, bars = [], g = new THREE.Group(); g.position.set(-0.4, -0.6, 0); scene.add(g);
    g.add(U.box(Q * dx + 0.3, 0.04, 0.5, U.mat(0x162238), 0, -0.03, 0));
    for (let x = 0; x < Q; x++) {
      const m = new THREE.Mesh(new THREE.BoxGeometry(dx * 0.75, 1, 0.3), new THREE.MeshStandardMaterial({ color: 0xe0a54a, roughness: 0.45 }));
      m.position.set((x - (Q - 1) / 2) * dx, 0, 0); m.scale.y = 1e-3; g.add(m);
      bars.push({ m, h: 0, th: 0, col: new THREE.Color(0xe0a54a), tcol: new THREE.Color(0xe0a54a) });
    }
    [0, 16, 32, 48, 63].forEach((x) => ctx.label(String(x), [(x - (Q - 1) / 2) * dx - 0.4, -0.9, 0.3], 'plain small'));
    ctx.label('x 暫存器的值（0–63）', [-0.4, -1.3, 0.3], 'small');
    const stepL = ctx.label('', [-0.4, 3.4, 0], 'gold');
    const peakLs = [];
    for (let i = 0; i < 8; i++) peakLs.push(ctx.label('', [0, 0, 0], 'teal small'));
    const HMAX = 3.2;
    const fcol = (v) => new THREE.Color().setHSL((v * 0.137) % 1, 0.75, 0.55);
    const setBars = (arr, col) => { const mx = Math.max(1e-12, ...arr); arr.forEach((p, x) => { bars[x].th = (p / mx) * HMAX * (step === 1 ? 0.35 : 1); bars[x].tcol.copy(col(x)); }); };
    const compute = () => {
      const f = (x) => powmod(a, x, N);
      peakLs.forEach((L) => L.show(false));
      if (step === 0) { probs.fill(0); probs[0] = 1; setBars(Array.from(probs), () => new THREE.Color(0xe0a54a)); }
      if (step === 1) { probs.fill(1 / Q); setBars(Array.from(probs), () => new THREE.Color(0xe0a54a)); }
      if (step === 2) { probs.fill(1 / Q); setBars(Array.from(probs), (x) => fcol(f(x))); }
      if (step >= 3) {
        if (f0 === null) { f0 = f(Math.floor(Math.random() * Q)); }
        const xs = []; for (let x = 0; x < Q; x++) if (f(x) === f0) xs.push(x);
        if (step === 3) { probs.fill(0); xs.forEach((x) => { probs[x] = 1 / xs.length; }); setBars(Array.from(probs), (x) => fcol(f(x))); }
        else {
          for (let y = 0; y < Q; y++) { let re = 0, im = 0; xs.forEach((x) => { const t = (2 * Math.PI * x * y) / Q; re += Math.cos(t); im += Math.sin(t); }); probs[y] = (re * re + im * im) / (xs.length * Q); }
          setBars(Array.from(probs), (y) => (yMeas === y ? new THREE.Color(0xffffff) : new THREE.Color(0x38c6d9)));
          const pk = [...Array(Q).keys()].filter((y) => probs[y] > 0.03).slice(0, 8);
          pk.forEach((y, i) => { peakLs[i].pos.set((y - (Q - 1) / 2) * dx - 0.4, -0.6 + (probs[y] / Math.max(...probs)) * HMAX + 0.3, 0); peakLs[i].set(String(y)); peakLs[i].show(true); });
        }
      }
    };
    const STEPS = ['初始：|0⟩|1⟩', '① H⊗⁶：x 暫存器均勻疊加（64 個 x 同時存在）', '② 計算 f(x) = aˣ mod N（顏色 = f(x)）：週期性藏在疊加裡', '③ 量測第二暫存器 → 只留下 f(x) 相同的 x（間隔 = r）', '④ QFT：週期 r 轉成峰值，位置 ≈ 64·k / r', '⑤ 量測 x 暫存器得到 y（白色），交給古典電腦'];
    const next = () => { if (step >= 5) return false; step++; if (step === 5) { const r = Math.random(); let c = 0; yMeas = Q - 1; for (let y = 0; y < Q; y++) { c += probs[y]; if (r < c) { yMeas = y; break; } } } compute(); return true; };
    const reset = () => { step = 0; f0 = null; yMeas = null; compute(); };
    // 連分數
    const contFrac = (y) => {
      if (y === 0) return { r: null, text: 'y = 0：沒有資訊，重新執行' };
      let h0 = 0, h1 = 1, k0 = 1, k1 = 0, num = y, den = Q; const steps = [];
      while (den) { const q = Math.floor(num / den); [h0, h1] = [h1, q * h1 + h0]; [k0, k1] = [k1, q * k1 + k0]; steps.push(`${h1}/${k1}`); [num, den] = [den, num - q * den]; if (k1 > N) break; }
      const cands = steps.map((s) => +s.split('/')[1]).filter((d) => d > 0 && d < N);
      for (const d of cands) for (let m = 1; d * m <= N; m++) if (powmod(a, d * m, N) === 1) return { r: d * m, text: `漸近分數 ${steps.slice(0, 4).join(', ')} → 試分母（及其倍數）得 r = ${d * m}` };
      return { r: null, text: `漸近分數 ${steps.slice(0, 4).join(', ')}：沒找到，重新執行` };
    };
    const aList = () => [...Array(N).keys()].filter((x) => x > 1 && gcd(x, N) === 1);
    let aRow;
    const buildA = () => {
      if (aRow) aRow.remove();
      aRow = document.createElement('div'); aRow.className = 'ctl-row';
      aList().forEach((x) => { const b = document.createElement('button'); b.textContent = `a = ${x}`; if (x === a) b.classList.add('on'); b.onclick = () => { a = x; [...aRow.children].forEach((c) => c.classList.remove('on')); b.classList.add('on'); reset(); }; aRow.appendChild(b); });
      nRow.after(aRow);
    };
    const nRadio = ui.radio([[15, 'N = 15'], [21, 'N = 21']], N, (v) => { N = v; a = N === 15 ? 7 : 2; buildA(); reset(); });
    void nRadio;
    const nRow = document.querySelector('#controls .ctl-row:last-child');
    buildA();
    const r = ui.row();
    ui.button('下一步 ▶', () => { autoRun = false; next(); }, r);
    ui.button('自動播放', () => { reset(); autoRun = true; acc = 0; }, r);
    ui.button('重設', () => { autoRun = false; reset(); }, r);
    const ro = ui.readout();
    reset();

    ctx.inset('f(x) = aˣ mod N（週期函數）', (gx, W, H, P) => {
      const { X, Y } = P.frame(gx, W, H, [0, 32], [0, N], { xlabel: 'x', ylabel: 'f(x)', xticks: [[0, '0'], [8, '8'], [16, '16'], [24, '24'], [32, '32']], yticks: [[1, '1'], [N - 1, String(N - 1)]] });
      gx.strokeStyle = 'rgba(224,165,74,.5)'; gx.beginPath();
      for (let x = 0; x <= 32; x++) { const y = powmod(a, x, N); x ? gx.lineTo(X(x), Y(y)) : gx.moveTo(X(x), Y(y)); } gx.stroke();
      for (let x = 0; x <= 32; x++) { const y = powmod(a, x, N); P.dot(gx, X(x), Y(y), f0 !== null && y === f0 && step >= 3 ? 5 : 3, f0 !== null && y === f0 && step >= 3 ? '#fff' : '#' + fcol(y).getHexString()); }
      P.text(gx, `a = ${a}，週期 r = ${order(a, N)}`, X(20), Y(N) + 12, '#ffd28a');
    });

    return {
      update(t, dt) {
        const k = 1 - Math.exp(-dt * 6);
        bars.forEach((b) => { b.h += (b.th - b.h) * k; b.col.lerp(b.tcol, k); b.m.scale.y = Math.max(1e-3, b.h); b.m.position.y = b.m.scale.y / 2; b.m.material.color.copy(b.col); });
        if (autoRun) { acc += dt; if (acc > 1.8) { acc = 0; if (!next()) autoRun = false; } }
        stepL.set(STEPS[step]);
        const rTrue = order(a, N);
        let post = '';
        if (step === 5 && yMeas !== null) {
          const cf = contFrac(yMeas);
          post = `<br>量到 y = ${yMeas}，y/64 = ${(yMeas / 64).toFixed(4)}<br>${cf.text}`;
          if (cf.r) {
            if (cf.r % 2) post += `<br>r 為奇數 → 換一個 a 重來`;
            else { const h = powmod(a, cf.r / 2, N); const p1 = gcd(h + 1, N), p2 = gcd((h - 1 + N) % N, N); post += `<br>a^{r/2} mod N = ${h}；gcd(${h}+1, ${N}) = ${p1}，gcd(${h}−1, ${N}) = ${p2}` + (p1 > 1 && p1 < N ? `<br><b style="color:#66ffcc">${N} = ${p1} × ${N / p1} ✓</b>` : p2 > 1 && p2 < N ? `<br><b style="color:#66ffcc">${N} = ${p2} × ${N / p2} ✓</b>` : '<br>得到平凡因數 → 換 a 重來'); }
          }
        }
        ro.innerHTML = `N = ${N}，a = ${a}（真正週期 r = ${rTrue}）　步驟 ${step} / 5` + (step >= 3 && f0 !== null ? `<br>第二暫存器量到 f = ${f0}` : '') + (step >= 4 ? `<br>峰值應在 64k/r：${[...Array(rTrue).keys()].map((kk) => ((64 * kk) / rTrue).toFixed(1)).join('、')}` : '') + post +
          (N === 21 ? '<br><span style="color:#9fb0c8">（教學用暫存器只有 64；正式 Shor 需 Q ≥ N²，峰值會更尖）</span>' : '');
      },
    };
  },
});

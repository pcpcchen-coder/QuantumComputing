/* 「如何操作量子電腦」場景共用：狀態向量模擬器、量子閘矩陣、Bloch 球元件、振幅長條圖元件
 * 量子位元編號沿用 Qiskit 慣例：q0 是最低位元，基底 |q(n-1) … q1 q0⟩。
 */
(function () {
  'use strict';
  const U = App.U;
  const s2 = Math.SQRT1_2;
  const C = (re, im = 0) => [re, im];

  /* ---------------- 量子閘（2×2 複數矩陣，[re, im]） ---------------- */
  const G = {
    I: [[C(1), C(0)], [C(0), C(1)]],
    X: [[C(0), C(1)], [C(1), C(0)]],
    Y: [[C(0), C(0, -1)], [C(0, 1), C(0)]],
    Z: [[C(1), C(0)], [C(0), C(-1)]],
    H: [[C(s2), C(s2)], [C(s2), C(-s2)]],
    S: [[C(1), C(0)], [C(0), C(0, 1)]],
    Sdg: [[C(1), C(0)], [C(0), C(0, -1)]],
    T: [[C(1), C(0)], [C(0), C(s2, s2)]],
    Tdg: [[C(1), C(0)], [C(0), C(s2, -s2)]],
    SX: [[C(0.5, 0.5), C(0.5, -0.5)], [C(0.5, -0.5), C(0.5, 0.5)]],
    RX(t) { const c = Math.cos(t / 2), s = Math.sin(t / 2); return [[C(c), C(0, -s)], [C(0, -s), C(c)]]; },
    RY(t) { const c = Math.cos(t / 2), s = Math.sin(t / 2); return [[C(c), C(-s)], [C(s), C(c)]]; },
    RZ(t) { const c = Math.cos(t / 2), s = Math.sin(t / 2); return [[C(c, -s), C(0)], [C(0), C(c, s)]]; },
    P(f) { return [[C(1), C(0)], [C(0), C(Math.cos(f), Math.sin(f))]]; },
  };
  /* 單位元閘在 Bloch 球上的旋轉：[軸 (x,y,z), 角度]（忽略全域相位） */
  const ROT = {
    X: [[1, 0, 0], Math.PI], Y: [[0, 1, 0], Math.PI], Z: [[0, 0, 1], Math.PI],
    H: [[s2, 0, s2], Math.PI], S: [[0, 0, 1], Math.PI / 2], Sdg: [[0, 0, 1], -Math.PI / 2],
    T: [[0, 0, 1], Math.PI / 4], Tdg: [[0, 0, 1], -Math.PI / 4], SX: [[1, 0, 0], Math.PI / 2],
  };

  /* ---------------- 狀態向量 ---------------- */
  class State {
    constructor(n) { this.n = n; this.N = 1 << n; this.re = new Float64Array(this.N); this.im = new Float64Array(this.N); this.reset(); }
    reset(k = 0) { this.re.fill(0); this.im.fill(0); this.re[k] = 1; return this; }
    copyFrom(o) { this.re.set(o.re); this.im.set(o.im); return this; }
    clone() { return new State(this.n).copyFrom(this); }
    apply(q, M, ctrl = -1) {
      const m = 1 << q, cm = ctrl >= 0 ? 1 << ctrl : 0, re = this.re, im = this.im;
      const [[a, b], [c, d]] = M;
      for (let i = 0; i < this.N; i++) {
        if (i & m) continue;
        if (cm && !(i & cm)) continue;
        const j = i | m;
        const r0 = re[i], i0 = im[i], r1 = re[j], i1 = im[j];
        re[i] = a[0] * r0 - a[1] * i0 + b[0] * r1 - b[1] * i1;
        im[i] = a[0] * i0 + a[1] * r0 + b[0] * i1 + b[1] * r1;
        re[j] = c[0] * r0 - c[1] * i0 + d[0] * r1 - d[1] * i1;
        im[j] = c[0] * i0 + c[1] * r0 + d[0] * i1 + d[1] * r1;
      }
      return this;
    }
    gate(name, q, theta) { const M = typeof G[name] === 'function' ? G[name](theta) : G[name]; return this.apply(q, M); }
    cx(c, t) { return this.apply(t, G.X, c); }
    cz(a, b) { const m = (1 << a) | (1 << b); for (let i = 0; i < this.N; i++) if ((i & m) === m) { this.re[i] = -this.re[i]; this.im[i] = -this.im[i]; } return this; }
    swap(a, b) { this.cx(a, b); this.cx(b, a); this.cx(a, b); return this; }
    ccx(c1, c2, t) { // Toffoli
      const m1 = 1 << c1, m2 = 1 << c2, mt = 1 << t;
      for (let i = 0; i < this.N; i++) if ((i & m1) && (i & m2) && !(i & mt)) {
        const j = i | mt; [this.re[i], this.re[j]] = [this.re[j], this.re[i]]; [this.im[i], this.im[j]] = [this.im[j], this.im[i]];
      }
      return this;
    }
    oracle(f) { for (let i = 0; i < this.N; i++) if (f(i)) { this.re[i] = -this.re[i]; this.im[i] = -this.im[i]; } return this; }
    prob(i) { return this.re[i] * this.re[i] + this.im[i] * this.im[i]; }
    probs() { const p = new Float64Array(this.N); for (let i = 0; i < this.N; i++) p[i] = this.prob(i); return p; }
    p1(q) { let s = 0; const m = 1 << q; for (let i = 0; i < this.N; i++) if (i & m) s += this.prob(i); return s; }
    /* 測量單一量子位元並塌縮 */
    measure(q, r = Math.random()) {
      const p1 = this.p1(q), bit = r < p1 ? 1 : 0, m = 1 << q;
      const norm = Math.sqrt(bit ? p1 : 1 - p1) || 1;
      for (let i = 0; i < this.N; i++) {
        if (((i & m) ? 1 : 0) !== bit) { this.re[i] = 0; this.im[i] = 0; } else { this.re[i] /= norm; this.im[i] /= norm; }
      }
      return bit;
    }
    sampleIndex(r = Math.random()) { let acc = 0; for (let i = 0; i < this.N; i++) { acc += this.prob(i); if (r < acc) return i; } return this.N - 1; }
    measureAll() { const k = this.sampleIndex(); this.reset(k); return k; }
    counts(shots) { const c = new Array(this.N).fill(0); const p = this.probs(); const cdf = []; let a = 0; for (const x of p) cdf.push((a += x)); for (let s = 0; s < shots; s++) { const r = Math.random() * a; let k = 0; while (k < this.N - 1 && r >= cdf[k]) k++; c[k]++; } return c; }
    /* 單一量子位元的約化 Bloch 向量（部分跡） */
    bloch(q) {
      const m = 1 << q; let p0 = 0, p1 = 0, cr = 0, ci = 0;
      for (let i = 0; i < this.N; i++) {
        if (i & m) { p1 += this.prob(i); continue; }
        p0 += this.prob(i);
        const j = i | m; // ρ01 = Σ a_i conj(a_j)
        cr += this.re[i] * this.re[j] + this.im[i] * this.im[j];
        ci += this.im[i] * this.re[j] - this.re[i] * this.im[j];
      }
      return [2 * cr, -2 * ci, p0 - p1];
    }
  }

  const ket = (i, n) => '|' + i.toString(2).padStart(n, '0') + '⟩';
  /* 相位 → 顏色：實數正 = 金色，實數負 = 藍色 */
  const phaseHue = (re, im) => ((0.1 + Math.atan2(im, re) / (2 * Math.PI)) % 1 + 1) % 1;
  const phaseColor = (re, im, target) => (target || new THREE.Color()).setHSL(phaseHue(re, im), 0.8, 0.55);
  const fmtC = (re, im, d = 2) => {
    const r = Math.abs(re) < 5e-4 ? 0 : re, i = Math.abs(im) < 5e-4 ? 0 : im;
    const R = (r < 0 ? '−' : '') + Math.abs(r).toFixed(d);
    if (!i) return R;
    if (!r) return (i < 0 ? '−' : '') + Math.abs(i).toFixed(d) + 'i';
    return `${R}${i < 0 ? '−' : '+'}${Math.abs(i).toFixed(d)}i`;
  };
  App.Q = { G, ROT, State, ket, phaseColor, phaseHue, fmtC };

  /* Bloch 座標 (x,y,z) → three.js：z 向上（three 的 y） */
  const B2T = (x, y, z) => new THREE.Vector3(y, z, x);
  App.B2T = B2T;

  /* ---------------- Bloch 球元件 ---------------- */
  App.Bloch = function (ctx, o = {}) {
    const R = o.r || 1.4, P0 = new THREE.Vector3(...(o.pos || [0, 0, 0]));
    const g = new THREE.Group(); g.position.copy(P0); ctx.scene.add(g);
    g.add(new THREE.Mesh(new THREE.SphereGeometry(R, 40, 28), new THREE.MeshStandardMaterial({ color: 0x3a6ea5, transparent: true, opacity: o.opacity ?? 0.13, roughness: 0.2, depthWrite: false })));
    const circ = (k) => {
      const pts = [];
      for (let i = 0; i <= 96; i++) {
        const a = (i / 96) * Math.PI * 2, c = R * Math.cos(a), s = R * Math.sin(a);
        pts.push(k === 0 ? [c, 0, s] : k === 1 ? [c, s, 0] : [0, s, c]);
      }
      return U.line(pts, 0x9fb7e0, 0.45);
    };
    g.add(circ(0), circ(1), circ(2));
    [[B2T(1, 0, 0), 0xff9f43], [B2T(0, 1, 0), 0x2ecc71], [B2T(0, 0, 1), 0x8ab4ff]].forEach(([d, c]) => g.add(U.line([d.clone().multiplyScalar(-R * 1.12), d.clone().multiplyScalar(R * 1.12)], c, 0.75)));
    const W = (x, y, z, k = 1.27) => B2T(x, y, z).multiplyScalar(R * k).add(P0);
    const labels = [];
    if (o.labels !== false) {
      labels.push(ctx.label('|0⟩', W(0, 0, 1), 'q0' + (o.small ? ' small' : '')));
      labels.push(ctx.label('|1⟩', W(0, 0, -1), 'q1' + (o.small ? ' small' : '')));
      if (!o.small) { labels.push(ctx.label('x', W(1, 0, 0, 1.2), 'plain small')); labels.push(ctx.label('y', W(0, 1, 0, 1.2), 'plain small')); }
    }
    if (o.title) labels.push(ctx.label(o.title, P0.clone().add(new THREE.Vector3(0, -R * (o.small ? 1.75 : 1.45), 0)), o.titleCls || 'teal small'));
    const arrow = U.fatArrow(o.color || 0xe0a54a, R, o.small ? 0.03 : 0.035); g.add(arrow);
    const tip = U.sphere(o.small ? 0.05 : 0.065, U.glow(o.tipColor || 0xffd28a)); g.add(tip);
    const trail = U.dynLine(o.trailN || 500, o.trailColor || 0xffd28a, 0.85); g.add(trail.obj);
    const tp = [];
    const axis = U.line([[0, 0, 0], [0, 0, 0]], 0xff6bd5, 0.95); g.add(axis);
    axis.visible = false;
    const vec = new THREE.Vector3(0, 0, 1);
    const W2 = {
      group: g, R, vec, labels, P0,
      set(x, y, z, keepTrail = true) {
        vec.set(x, y, z);
        const v = B2T(x, y, z).multiplyScalar(R);
        arrow.setVec(v); tip.position.copy(v);
        if (keepTrail) { tp.push([v.x, v.y, v.z]); if (tp.length > (o.trailN || 500)) tp.shift(); trail.set(tp); }
      },
      setV(v, keep) { this.set(v[0], v[1], v[2], keep); },
      clearTrail() { tp.length = 0; trail.set(tp); },
      showAxis(ax) {
        if (!ax) { axis.visible = false; return; }
        const d = B2T(...ax).normalize().multiplyScalar(R * 1.3);
        axis.geometry.setFromPoints([d.clone().negate(), d]); axis.visible = true;
      },
      world(x, y, z, k = 1) { return W(x, y, z, k); },
    };
    W2.set(0, 0, 1, false);
    return W2;
  };

  /* 以軸角旋轉 Bloch 向量（Rodrigues） */
  App.rotVec = (v, ax, ang) => {
    const [x, y, z] = v; let [a, b, c] = ax; const n = Math.hypot(a, b, c) || 1; a /= n; b /= n; c /= n;
    const co = Math.cos(ang), si = Math.sin(ang), d = a * x + b * y + c * z;
    return [x * co + (b * z - c * y) * si + a * d * (1 - co), y * co + (c * x - a * z) * si + b * d * (1 - co), z * co + (a * y - b * x) * si + c * d * (1 - co)];
  };

  /* ---------------- 振幅長條圖元件 ----------------
   * 每個基底態一根柱子：高度 = 機率（mode 'prob'）或帶正負號的實數振幅（mode 'amp'），顏色 = 相位 */
  App.AmpBars = function (ctx, n, o = {}) {
    const N = 1 << n, g = new THREE.Group(); ctx.scene.add(g);
    g.position.set(...(o.pos || [0, 0, 0]));
    const cols = o.cols || N, rows = Math.ceil(N / cols);
    const dx = o.dx || 0.6, dz = o.dz || 0.6, w = o.w || dx * 0.62, H = o.H || 2.5;
    const plate = U.box(cols * dx + 0.3, 0.04, rows * dz + 0.3, U.mat(0x162238, { roughness: 0.9 }), 0, -0.03, 0);
    g.add(plate);
    if (o.mode === 'amp') { const ref = U.box(cols * dx + 0.3, 0.005, rows * dz + 0.3, U.glow(0x6f8fbf, 0.18), 0, 0, 0); g.add(ref); }
    const bars = [], lbl = [];
    const pos = (i) => [(i % cols - (cols - 1) / 2) * dx, 0, (Math.floor(i / cols) - (rows - 1) / 2) * dz];
    for (let i = 0; i < N; i++) {
      const m = new THREE.Mesh(new THREE.BoxGeometry(w, 1, w), new THREE.MeshStandardMaterial({ color: 0xe0a54a, roughness: 0.4, metalness: 0.1, emissive: 0x000000 }));
      const [x, , z] = pos(i); m.position.set(x, 0, z); m.scale.y = 1e-3; g.add(m);
      bars.push({ m, h: 0, th: 0, col: new THREE.Color(0xe0a54a), tcol: new THREE.Color(0xe0a54a) });
      const show = o.labels !== false && (N <= (o.maxLabels || 16) || i % Math.ceil(N / 16) === 0);
      if (show) lbl.push(ctx.label(o.labelFn ? o.labelFn(i) : ket(i, n), g.position.clone().add(new THREE.Vector3(x, -0.25, z + (o.labelDz ?? 0.35))), 'plain small'));
      else lbl.push(null);
    }
    const tmp = new THREE.Color();
    const A = {
      group: g, N, bars, H, labels: lbl, pos,
      set(st, instant = false) {
        for (let i = 0; i < N; i++) {
          const re = st.re[i], im = st.im[i], p = re * re + im * im;
          const h = o.mode === 'amp' ? (Math.cos(Math.atan2(im, re)) >= -1e-9 ? 1 : -1) * Math.sqrt(p) * H : p * H;
          bars[i].th = h;
          if (p > 1e-9) phaseColor(re, im, bars[i].tcol); else bars[i].tcol.set(0x3a4658);
          if (instant) { bars[i].h = h; bars[i].col.copy(bars[i].tcol); }
        }
      },
      setHeights(arr, color) { for (let i = 0; i < N; i++) { bars[i].th = arr[i] * H; if (color) bars[i].tcol.set(color(i)); } },
      highlight(i, on, c = 0x66ffcc) { bars[i].m.material.emissive.set(on ? c : 0x000000); bars[i].m.material.emissiveIntensity = on ? 0.55 : 0; },
      update(dt, k = 8) {
        const a = 1 - Math.exp(-dt * k);
        for (const b of bars) {
          b.h += (b.th - b.h) * a; b.col.lerp(b.tcol, a);
          const hh = Math.abs(b.h) < 1e-3 ? 1e-3 : b.h;
          b.m.scale.y = Math.abs(hh); b.m.position.y = hh / 2;
          b.m.material.color.copy(b.col);
        }
      },
      top(i) { const [x, , z] = pos(i); return g.position.clone().add(new THREE.Vector3(x, Math.max(0, bars[i].h) + 0.25, z)); },
    };
    return A;
  };

  /* 相位色環圖例（畫在插圖上） */
  App.phaseLegend = (g, x, y, r) => {
    for (let k = 0; k < 64; k++) {
      const a0 = (k / 64) * 2 * Math.PI, a1 = ((k + 1) / 64) * 2 * Math.PI;
      g.fillStyle = `hsl(${((0.1 + k / 64) % 1) * 360},80%,55%)`;
      g.beginPath(); g.moveTo(x, y); g.arc(x, y, r, -a1, -a0); g.closePath(); g.fill();
    }
  };

  /* 簡易直方圖（插圖用） */
  App.histo = (g, W, Hh, P, counts, labels, o = {}) => {
    const n = counts.length, tot = counts.reduce((a, b) => a + b, 0) || 1;
    const ymax = o.ymax || Math.max(0.05, ...counts.map((c) => c / tot)) * 1.15;
    const { X, Y } = P.frame(g, W, Hh, [0, n], [0, ymax], { xlabel: o.xlabel || '量測結果', ylabel: o.ylabel || '機率', yticks: [[0, '0'], [ymax / 2, (ymax / 2).toFixed(2)], [ymax, ymax.toFixed(2)]], m: { b: n > 8 ? 40 : 30 } });
    const bw = (X(1) - X(0)) * 0.7;
    counts.forEach((c, i) => {
      const p = c / tot; g.fillStyle = o.color ? o.color(i) : '#e0a54a';
      g.fillRect(X(i + 0.5) - bw / 2, Y(p), bw, Y(0) - Y(p));
      if (o.ideal) { g.strokeStyle = '#8ef0ff'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(X(i + 0.5) - bw / 2 - 2, Y(o.ideal[i])); g.lineTo(X(i + 0.5) + bw / 2 + 2, Y(o.ideal[i])); g.stroke(); }
      if (n <= 16) {
        g.save(); g.fillStyle = '#9fb0c8'; g.font = '11px sans-serif'; g.textAlign = 'center';
        if (n > 8) { g.translate(X(i + 0.5), Hh - 26); g.rotate(-Math.PI / 4); g.fillText(labels[i], 0, 0); } else g.fillText(labels[i], X(i + 0.5), Hh - 16);
        g.restore();
      }
    });
  };
})();

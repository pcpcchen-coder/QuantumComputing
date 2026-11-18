/* 離子阱與中性原子場景的共用資料與元件：
 * 雷射光束、光子粒子、真空腔、光學桌、光學元件、能階圖、2D 直方圖、複數小型矩陣演化、波長→顏色
 * 也沿用 peripherals/common.js 的 App.Flow、App.device、App.bars。
 */
(function () {
  'use strict';
  const U = App.U;

  /* 代表性數值（文獻與廠商公開資料；實際依系統而異） */
  const AD = {
    ion: {
      species: '¹⁷¹Yb⁺', qubitGHz: 12.6428, // 超精細時鐘躍遷 |F=0,m=0⟩ ↔ |F=1,m=0⟩
      cool: 369.5, repump: 935.2, pi1: 399, raman: 355, // nm
      secularMHz: { radial: 3, axial: 1 }, rfMHz: 30,
      t1q: '1–10 μs', t2q: '25–200 μs', tread: '100–300 μs', T2: '1 s～1 小時（動態解耦 + 共冷）',
    },
    atom: {
      species: '⁸⁷Rb', qubitGHz: 6.8347, // |F=1,m=0⟩ ↔ |F=2,m=0⟩
      cool: 780, tweezer: 852, ryd1: 420, ryd2: 1013, // nm
      t1q: '0.5–100 μs', t2q: '0.2–0.5 μs', tread: '1–20 ms', T2: '~1 s（自旋回波）；Caltech 2025：12.6 s',
    },
  };
  App.AD = AD;

  /* 波長（nm）→ 顯示顏色；紅外光以洋紅色表示（肉眼不可見） */
  App.wlColor = (nm) => {
    if (nm < 380) return 0xb46cff; // 紫外
    if (nm < 440) return 0x7f5cff;
    if (nm < 490) return 0x3fa0ff;
    if (nm < 510) return 0x38d6c9;
    if (nm < 580) return 0x7ee05a;
    if (nm < 645) return 0xff8a3d;
    if (nm < 760) return 0xff4040;
    return 0xd04090; // 紅外
  };

  /* 雷射光束：發光圓柱，可開關、可改端點 */
  App.beam = function (scene, a, b, color, r = 0.03, opacity = 0.55) {
    const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity, depthWrite: false, blending: THREE.AdditiveBlending });
    const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1, 14, 1, true), mat);
    scene.add(m);
    const A = new THREE.Vector3(), B = new THREE.Vector3();
    m.set = (p, q) => {
      A.set(...(p.isVector3 ? p.toArray() : p)); B.set(...(q.isVector3 ? q.toArray() : q));
      const d = B.clone().sub(A); const L = d.length();
      m.scale.set(1, Math.max(1e-3, L), 1);
      m.position.copy(A).addScaledVector(d, 0.5);
      m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
    };
    m.on = (v, o = opacity) => { m.visible = !!v; mat.opacity = o; };
    m.set(a, b);
    return m;
  };

  /* 光子粒子池：從某點往隨機（或指定）方向射出的小亮點 */
  App.photons = function (scene, color, n = 80, o = {}) {
    const geo = new THREE.SphereGeometry(o.size || 0.03, 8, 6);
    const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.95, depthWrite: false, blending: THREE.AdditiveBlending });
    const pool = [];
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(geo, mat); m.visible = false; scene.add(m); pool.push({ m, v: new THREE.Vector3(), life: 0 }); }
    let k = 0;
    return {
      mat,
      emit(pos, dir, speed = 3, life = 1) {
        const p = pool[k++ % n];
        p.m.position.set(...(pos.isVector3 ? pos.toArray() : pos));
        let d = dir;
        if (!d) { d = new THREE.Vector3(U.gauss(), U.gauss(), U.gauss()).normalize(); }
        else if (!d.isVector3) d = new THREE.Vector3(...d).normalize();
        p.v.copy(d).multiplyScalar(speed); p.life = life; p.m.visible = true;
        return p;
      },
      update(dt) {
        pool.forEach((p) => {
          if (p.life <= 0) return;
          p.life -= dt; p.m.position.addScaledVector(p.v, dt);
          if (p.life <= 0) p.m.visible = false;
        });
      },
      clear() { pool.forEach((p) => { p.life = 0; p.m.visible = false; }); },
    };
  };

  /* 光學桌（深灰平台 + 螺絲孔格線） */
  App.opticalTable = function (ctx, o = {}) {
    const { scene } = ctx;
    const w = o.w || 12, d = o.d || 6, y = o.y ?? 0.9;
    const g = new THREE.Group();
    g.add(U.box(w, 0.25, d, U.metal(0x3a404a, { roughness: 0.55 }), 0, y - 0.125, 0));
    const grid = new THREE.GridHelper(Math.max(w, d), Math.round(Math.max(w, d) * 2.5), 0x565e6b, 0x4a515c);
    grid.scale.set(w / Math.max(w, d), 1, d / Math.max(w, d)); grid.position.y = y + 0.002; g.add(grid);
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx, sz]) => g.add(U.box(0.35, y - 0.25, 0.35, U.mat(0x2a2f38), sx * (w / 2 - 0.4), (y - 0.25) / 2, sz * (d / 2 - 0.4))));
    if (o.pos) g.position.set(...o.pos);
    scene.add(g);
    g.top = y;
    return g;
  };

  /* 小型光學元件：mirror（傾斜鏡）、lens（透鏡）、aom（聲光調變器方塊）、fiber（光纖耦合座） */
  App.optic = function (ctx, type, pos, o = {}) {
    const { scene } = ctx;
    const g = new THREE.Group();
    const post = U.box(0.05, 0.25, 0.05, U.metal(0xc0c6d0), 0, -0.12, 0); g.add(post);
    if (type === 'mirror') {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.03, 24), U.metal(0xe8ecf2, { roughness: 0.1 }));
      m.rotation.z = Math.PI / 2; m.rotation.y = o.rot ?? Math.PI / 4; g.add(m);
    } else if (type === 'lens') {
      const m = new THREE.Mesh(new THREE.SphereGeometry(0.14, 20, 12), new THREE.MeshStandardMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.55, roughness: 0.05 }));
      m.scale.set(0.3, 1, 1); m.rotation.y = o.rot ?? 0; g.add(m);
    } else if (type === 'aom') {
      g.add(U.box(0.28, 0.18, 0.2, U.mat(0x2c3a52, { metalness: 0.4 }), 0, 0, 0));
      g.add(U.box(0.06, 0.06, 0.06, U.metal(0xd4a050), 0, 0.12, 0));
    } else if (type === 'fiber') {
      g.add(U.box(0.18, 0.18, 0.18, U.metal(0x9aa4b2), 0, 0, 0));
    }
    g.position.set(...pos);
    scene.add(g);
    if (o.label) ctx.label(o.label, [pos[0], pos[1] + (o.dy ?? 0.35), pos[2]], o.cls || 'small');
    return g;
  };

  /* 超高真空腔：八角形腔體 + 視窗法蘭 + 離子泵 */
  App.chamber = function (ctx, o = {}) {
    const { scene } = ctx;
    const g = new THREE.Group();
    const r = o.r || 0.9, h = o.h || 0.7;
    const body = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, 8, 1, true), new THREE.MeshStandardMaterial({ color: 0xb8c2d0, metalness: 0.8, roughness: 0.3, transparent: true, opacity: o.opacity ?? 0.35, side: THREE.DoubleSide, depthWrite: false }));
    g.add(body);
    const capMat = new THREE.MeshStandardMaterial({ color: 0xb8c2d0, metalness: 0.8, roughness: 0.3, transparent: true, opacity: (o.opacity ?? 0.35) * 0.6, side: THREE.DoubleSide, depthWrite: false });
    [h / 2, -h / 2].forEach((y) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 0.04, 8), capMat); c.position.y = y; g.add(c); });
    for (let k = 0; k < 8; k++) {
      const a = (k / 8) * Math.PI * 2 + Math.PI / 8;
      const f = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.08, 20), U.metal(0xd0d6de));
      f.position.set(Math.cos(a) * (r * 0.95), 0, Math.sin(a) * (r * 0.95));
      f.rotation.z = Math.PI / 2; f.rotation.y = -a; g.add(f);
      const win = new THREE.Mesh(new THREE.CircleGeometry(0.11, 20), new THREE.MeshBasicMaterial({ color: 0x88c8ff, transparent: true, opacity: 0.35, side: THREE.DoubleSide }));
      win.position.set(Math.cos(a) * (r * 0.99), 0, Math.sin(a) * (r * 0.99)); win.rotation.y = Math.PI / 2 - a; g.add(win);
    }
    if (o.pump !== false) {
      const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.8, 16), U.metal(0xd0d6de));
      arm.position.set(0, -h / 2 - 0.4, 0); g.add(arm);
      const pump = U.box(0.7, 0.5, 0.5, U.mat(0x5b6474, { metalness: 0.5 }), 0, -h / 2 - 1.0, 0); g.add(pump);
      if (o.pumpLabel !== false) ctx.label(o.pumpLabel || '離子泵 + NEG（< 10⁻¹¹ mbar）', [o.pos[0] + 0.9, o.pos[1] - h / 2 - 1.0, o.pos[2]], 'small');
    }
    g.position.set(...(o.pos || [0, 0, 0]));
    scene.add(g);
    return g;
  };

  /* 能階圖（立體薄板）：levels = [{key, y, x, w, color, label}]；回傳 {lv, arrow(k1,k2,color)} */
  App.levelDiagram = function (ctx, levels, o = {}) {
    const { scene } = ctx;
    const g = new THREE.Group(); scene.add(g);
    const lv = {};
    levels.forEach((L) => {
      const m = U.box(L.w || 1.2, 0.05, 0.25, U.mat(L.color || 0xdfe6f0, { emissive: L.color || 0x333333, emissiveIntensity: 0.25 }), L.x, L.y, 0);
      g.add(m); lv[L.key] = { ...L, mesh: m };
      const P0 = o.pos || [0, 0, 0];
      if (L.label) ctx.label(L.label, [P0[0] + L.x + (L.w || 1.2) / 2 + (L.ldx ?? 0.35), P0[1] + L.y, P0[2]], L.cls || 'small');
    });
    if (o.pos) g.position.set(...o.pos);
    /* 兩能階間的躍遷箭頭（可開關、可閃爍） */
    const arrow = (k1, k2, color, dx = 0, label) => {
      const a = lv[k1], b = lv[k2];
      const off = new THREE.Vector3(...(o.pos || [0, 0, 0]));
      const p1 = new THREE.Vector3(a.x + dx, a.y, 0).add(off), p2 = new THREE.Vector3(b.x + dx, b.y, 0).add(off);
      const arr = U.fatArrow(color, 1, 0.03); arr.position.copy(p1); arr.setVec(p2.clone().sub(p1)); scene.add(arr);
      if (label) arr.lbl = ctx.label(label, p1.clone().lerp(p2, 0.5).add(new THREE.Vector3(0.18, 0, 0)), 'small');
      arr.show = (v) => { arr.visible = v; if (arr.lbl) arr.lbl.show(v); };
      return arr;
    };
    return { g, lv, arrow };
  };

  /* 2D 插圖：直方圖。bins = [{x, a, b}]（兩組計數，可選）；thr = 閾值 */
  App.hist2 = function (g, W, H, P, A, B, o = {}) {
    const n = A.length; const max = Math.max(1, ...A, ...(B || [0])) * 1.1;
    const { X, Y } = P.frame(g, W, H, [0, n], [0, max], { xlabel: o.xlabel || '', ylabel: o.ylabel || '次數', xticks: o.xticks || [], yticks: [], m: { l: 30, b: 32 } });
    const bw = X(1) - X(0);
    const bar = (arr, col) => { g.fillStyle = col; arr.forEach((v, i) => { if (v > 0) g.fillRect(X(i) + 1, Y(v), bw - 2, Y(0) - Y(v)); }); };
    bar(A, o.colA || 'rgba(79,140,255,.75)');
    if (B) bar(B, o.colB || 'rgba(255,90,95,.7)');
    if (o.thr != null) { g.strokeStyle = '#ffd28a'; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(X(o.thr), Y(0)); g.lineTo(X(o.thr), Y(max)); g.stroke(); g.setLineDash([]); }
    (o.notes || []).forEach(([s, x, y, c]) => P.text(g, s, x, y, c || '#e8eef8'));
  };

  /* Poisson 亂數（小平均值用乘法法；大平均值用常態近似） */
  App.poisson = (lam) => {
    if (lam > 40) return Math.max(0, Math.round(lam + Math.sqrt(lam) * U.gauss()));
    const L = Math.exp(-lam); let k = 0, p = 1;
    do { k++; p *= Math.random(); } while (p > L);
    return k - 1;
  };

  /* 複數小矩陣工具：狀態 ψ = [[re,im],...]；H 為實數或複數矩陣（[[ [re,im] ]]）
   * evolve(psi, Hfun, t0, dt, steps)：用 RK4 解 iħ dψ/dt = H ψ（ħ = 1） */
  const cm = {
    mulHpsi(H, psi) {
      const n = psi.length; const out = [];
      for (let i = 0; i < n; i++) {
        let re = 0, im = 0;
        for (let j = 0; j < n; j++) {
          const h = H[i][j]; const hr = Array.isArray(h) ? h[0] : h, hi = Array.isArray(h) ? h[1] : 0;
          re += hr * psi[j][0] - hi * psi[j][1]; im += hr * psi[j][1] + hi * psi[j][0];
        }
        out.push([re, im]);
      }
      return out;
    },
    // dψ/dt = -i H ψ
    deriv(H, psi) { return cm.mulHpsi(H, psi).map(([r, i]) => [i, -r]); },
    step(Hf, psi, t, dt) {
      const add = (a, b, s) => a.map((x, k) => [x[0] + s * b[k][0], x[1] + s * b[k][1]]);
      const k1 = cm.deriv(Hf(t), psi);
      const k2 = cm.deriv(Hf(t + dt / 2), add(psi, k1, dt / 2));
      const k3 = cm.deriv(Hf(t + dt / 2), add(psi, k2, dt / 2));
      const k4 = cm.deriv(Hf(t + dt), add(psi, k3, dt));
      return psi.map((x, k) => [x[0] + (dt / 6) * (k1[k][0] + 2 * k2[k][0] + 2 * k3[k][0] + k4[k][0]), x[1] + (dt / 6) * (k1[k][1] + 2 * k2[k][1] + 2 * k3[k][1] + k4[k][1])]);
    },
    prob(psi) { return psi.map(([r, i]) => r * r + i * i); },
  };
  App.cm = cm;

  /* 離子 / 原子小球（帶光暈） */
  App.particle = function (scene, color, r = 0.08, pos = [0, 0, 0]) {
    const g = new THREE.Group();
    const core = U.sphere(r, U.mat(color, { emissive: color, emissiveIntensity: 0.8, roughness: 0.3 }), 0, 0, 0, 20);
    const halo = U.sphere(r * 2.2, new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.18, depthWrite: false, blending: THREE.AdditiveBlending }), 0, 0, 0, 16);
    g.add(core, halo); g.position.set(...pos); scene.add(g);
    g.core = core; g.halo = halo;
    g.setColor = (c) => { core.material.color.setHex(c); core.material.emissive.setHex(c); halo.material.color.setHex(c); };
    g.glow = (k) => { halo.material.opacity = 0.08 + 0.5 * k; core.material.emissiveIntensity = 0.3 + 1.2 * k; };
    return g;
  };

  /* 小型 n 位元狀態向量模擬器（ψ 以 Float64Array 存實部與虛部；位元 k 對應索引的第 k 個 bit）
   * 用於「運算與讀取」總覽場景：Rx / Ry / Rz、XX(θ)（MS 閘）、CZ、Bloch 向量、取樣與塌縮 */
  App.qsim = function (n) {
    const N = 1 << n;
    const S = { n, re: new Float64Array(N), im: new Float64Array(N) };
    S.reset = () => { S.re.fill(0); S.im.fill(0); S.re[0] = 1; return S; };
    S.copy = () => ({ re: S.re.slice(), im: S.im.slice() });
    S.load = (c) => { S.re.set(c.re); S.im.set(c.im); return S; };
    /* 單位元閘 [[a,b],[c,d]]，每個元素為 [re, im] */
    S.u1 = (k, a, b, c, d) => {
      const m = 1 << k;
      for (let i = 0; i < N; i++) {
        if (i & m) continue;
        const j = i | m;
        const r0 = S.re[i], i0 = S.im[i], r1 = S.re[j], i1 = S.im[j];
        S.re[i] = a[0] * r0 - a[1] * i0 + b[0] * r1 - b[1] * i1; S.im[i] = a[0] * i0 + a[1] * r0 + b[0] * i1 + b[1] * r1;
        S.re[j] = c[0] * r0 - c[1] * i0 + d[0] * r1 - d[1] * i1; S.im[j] = c[0] * i0 + c[1] * r0 + d[0] * i1 + d[1] * r1;
      }
      return S;
    };
    S.rx = (k, t) => { const c = Math.cos(t / 2), s = Math.sin(t / 2); return S.u1(k, [c, 0], [0, -s], [0, -s], [c, 0]); };
    S.ry = (k, t) => { const c = Math.cos(t / 2), s = Math.sin(t / 2); return S.u1(k, [c, 0], [-s, 0], [s, 0], [c, 0]); };
    S.rz = (k, t) => { const c = Math.cos(t / 2), s = Math.sin(t / 2); return S.u1(k, [c, -s], [0, 0], [0, 0], [c, s]); };
    /* MS 閘：exp(−iθ X_a X_b)；θ = π/4 為最大糾纏 */
    S.xx = (a, b, t) => {
      const m = (1 << a) | (1 << b), c = Math.cos(t), s = Math.sin(t);
      const re = S.re.slice(), im = S.im.slice();
      for (let i = 0; i < N; i++) { const j = i ^ m; S.re[i] = c * re[i] + s * im[j]; S.im[i] = c * im[i] - s * re[j]; }
      return S;
    };
    /* 受控相位：|11⟩ 乘上 e^{iφ}（φ = π 即 CZ） */
    S.cphase = (a, b, phi) => {
      const m = (1 << a) | (1 << b), c = Math.cos(phi), s = Math.sin(phi);
      for (let i = 0; i < N; i++) if ((i & m) === m) { const r = S.re[i], q = S.im[i]; S.re[i] = c * r - s * q; S.im[i] = c * q + s * r; }
      return S;
    };
    S.probs = () => { const p = new Float64Array(N); for (let i = 0; i < N; i++) p[i] = S.re[i] * S.re[i] + S.im[i] * S.im[i]; return p; };
    /* 第 k 個位元的 Bloch 向量（約化密度矩陣）；z = +1 為 |0⟩ */
    S.bloch = (k) => {
      const m = 1 << k; let x = 0, y = 0, z = 0;
      for (let i = 0; i < N; i++) {
        const p = S.re[i] * S.re[i] + S.im[i] * S.im[i];
        if (i & m) { z -= p; continue; }
        z += p;
        const j = i | m; // ρ01 = Σ ψ_i ψ_j*
        const r = S.re[i] * S.re[j] + S.im[i] * S.im[j], q = S.im[i] * S.re[j] - S.re[i] * S.im[j];
        x += 2 * r; y -= 2 * q;
      }
      return { x, y, z };
    };
    S.sample = () => { const p = S.probs(); let u = Math.random(), i = 0; for (; i < N - 1; i++) { u -= p[i]; if (u <= 0) break; } return i; };
    S.collapse = (idx) => { S.re.fill(0); S.im.fill(0); S.re[idx] = 1; return S; };
    return S.reset();
  };

  /* 2D 插圖：各步驟時間的 log 座標橫條（cats = 步驟名稱；rows = [{name, col, vals: [秒...]}]） */
  App.timeBars = function (g, W, H, P, cats, rows, o = {}) {
    const lo = o.lo ?? -8, hi = o.hi ?? -1;
    const ticks = []; for (let e = lo; e <= hi; e++) { const s = { '-9': '1 ns', '-8': '10 ns', '-7': '100 ns', '-6': '1 μs', '-5': '10 μs', '-4': '100 μs', '-3': '1 ms', '-2': '10 ms', '-1': '100 ms', '0': '1 s' }[e]; if (s && (e - lo) % (o.every || 1) === 0) ticks.push([e, s]); }
    const m = { l: 74, r: 20, t: 6, b: 34 };
    const X = (e) => m.l + ((e - lo) / (hi - lo)) * (W - m.l - m.r);
    g.strokeStyle = 'rgba(160,180,210,.18)'; g.lineWidth = 1;
    ticks.forEach(([e]) => { g.beginPath(); g.moveTo(X(e), m.t); g.lineTo(X(e), H - m.b); g.stroke(); });
    g.fillStyle = '#9fb0c8'; g.font = P.font; g.textAlign = 'center';
    ticks.forEach(([e, s]) => g.fillText(s, X(e), H - m.b + 14));
    const ch = (H - m.t - m.b) / cats.length, bh = Math.min(10, (ch - 6) / rows.length);
    cats.forEach((c, i) => {
      const y0 = m.t + i * ch + (ch - bh * rows.length) / 2;
      P.text(g, c, m.l - 6, m.t + i * ch + ch / 2 + 4, '#cfd8e6', 'right');
      rows.forEach((r, k) => {
        const v = r.vals[i]; if (!v) return;
        const e = Math.log10(v);
        g.fillStyle = r.col; g.fillRect(X(lo), y0 + k * bh, Math.max(2, X(e) - X(lo)), bh - 2);
        if (o.marks && o.marks[i] === k) { g.strokeStyle = '#fff'; g.strokeRect(X(lo), y0 + k * bh, Math.max(2, X(e) - X(lo)), bh - 2); }
      });
    });
    let lx = m.l;
    rows.forEach((r) => { g.fillStyle = r.col; g.fillRect(lx, H - 12, 10, 8); P.text(g, r.name, lx + 14, H - 4, '#cfd8e6'); lx += 16 + g.measureText(r.name).width + 14; });
  };

  /* 2D 插圖：位元串長條圖（counts = {'00': n, ...}），可標示理想值 */
  App.bitHist = function (g, W, H, P, keys, counts, o = {}) {
    const tot = Math.max(1, keys.reduce((a, k) => a + (counts[k] || 0), 0));
    const { X, Y } = P.frame(g, W, H, [0, keys.length], [0, 1], { ylabel: '機率', yticks: [[0, '0'], [0.5, '0.5'], [1, '1']], xticks: keys.map((k, i) => [i + 0.5, k]), m: { l: 40, b: 30 } });
    keys.forEach((k, i) => {
      const p = (counts[k] || 0) / tot;
      g.fillStyle = o.col ? o.col(k) : 'rgba(255,192,74,.8)';
      g.fillRect(X(i) + 6, Y(p), X(1) - X(0) - 12, Y(0) - Y(p));
      if (p > 0.005) P.text(g, (p * 100).toFixed(1) + '%', X(i + 0.5), Y(p) - 4, '#e8eef8', 'center');
      if (o.ideal) { const q = o.ideal[k] || 0; g.strokeStyle = '#8ef0a0'; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(X(i) + 3, Y(q)); g.lineTo(X(i + 1) - 3, Y(q)); g.stroke(); g.setLineDash([]); }
    });
    (o.notes || []).forEach(([s, x, y, c]) => P.text(g, s, x, y, c || '#e8eef8'));
  };

  /* 頻率參考源的 Allan 偏差 σ_y(τ)（代表性經驗模型，量級正確，實際依機型而異）與科學記號格式 */
  App.FREF = {
    Q: { name: '石英 OCXO', col: '#9fb0c8', s: (t) => Math.hypot(1e-12, 1.2e-15 * t / Math.SQRT2) },
    Rb: { name: '銣鐘', col: '#ff8a3d', s: (t) => Math.hypot(1e-11 / Math.sqrt(t), 5e-13, 1.9e-17 * t / Math.SQRT2) },
    Cs: { name: '銫鐘', col: '#7ee05a', s: (t) => Math.hypot(1e-11 / Math.sqrt(t), 1e-14) },
    H: { name: '氫邁射', col: '#d8ff6a', s: (t) => Math.hypot(1.5e-13 / t, 2e-14 / Math.sqrt(t), 7e-16) },
  };
  /* Ramsey 自由演化 T 秒內，頻率 f0 的微波累積的相位誤差（rad）≈ 2π f0 σ_y(T) T */
  App.ramseyPhase = (key, f0, T) => 2 * Math.PI * f0 * App.FREF[key].s(T) * T;
  App.sciFmt = (x) => { const e = Math.floor(Math.log10(x)); return `${(x / Math.pow(10, e)).toFixed(1)}×10${String(e).replace('-', '⁻').replace(/\d/g, (d) => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d])}`; };

  /* 量子位元顏色（與其他頁一致）：|0⟩ 藍、|1⟩ 紅；離子金、原子青 */
  App.QC = { q0: 0x4f8cff, q1: 0xff5a5f, ion: 0xffc04a, atom: 0x38d6e9, cool: 0x9b7bff, ryd: 0xff6ad5 };
})();

/* 周邊系統場景的共用資料與元件：冷凍機模型、管線流動粒子、設備方塊、溫度色階 */
(function () {
  'use strict';
  const U = App.U;

  /* 典型數值（取自廠商規格與文獻的代表值，實際依機型而異） */
  const PD = {
    // 各級溫度：Krinner et al. 2019（Bluefors XLD 量測值）
    stages: [
      { key: 'rt', name: '300 K 頂板', T: 300, y: 3.3, r: 1.05 },
      { key: '50k', name: '50 K 級（~35–45 K）', T: 40, y: 2.75, r: 0.98 },
      { key: '4k', name: '4 K 級（~3 K）', T: 3, y: 2.2, r: 0.9 },
      { key: 'still', name: 'Still（~0.9 K）', T: 0.88, y: 1.7, r: 0.8 },
      { key: 'cp', name: 'Cold plate（~100 mK）', T: 0.09, y: 1.25, r: 0.72 },
      { key: 'mxc', name: 'MXC（~10 mK）', T: 0.01, y: 0.8, r: 0.64 },
    ],
    // 用電（kW）：PT415 壓縮機 CPA1110 10.7 kW（60 Hz）；Google Sycamore 約 10 kW 冷凍 + 10 kW 冷卻水 + 3 kW 電子
    power: [
      ['脈衝管壓縮機', 10.7], ['冷卻水系統', 10.0], ['控制電子機櫃', 3.0], ['氣體處理系統（泵）', 1.5], ['電腦 / 監控 / 網路', 1.0],
    ],
    // 佈線熱負載（每條不鏽鋼同軸，Krinner 2019）與各級冷卻功率（Bluefors XLD 量測）
    wiring: {
      stages: ['50 K', '4 K', 'Still', 'Cold plate', 'MXC'],
      passive: [45e-3, 1e-3, 3e-6, 0.4e-6, 0.015e-6], // W / 條
      attDiss: [0, 2e-6, 0, 2e-8, 2e-9], // 衰減器吸收的驅動功率（示意）W / 條
      hemt: 5e-3, // W / 顆（4 K）
      cool: [30, 1.5, 40e-3, 200e-6, 19e-6], // W（45 K / 4.2 K / 1.2 K / 140 mK / 20 mK）
    },
  };
  App.PD = PD;

  /* 溫度 → 顏色（對數色階：300 K 紅 → 10 mK 深藍） */
  App.tempColor = (T) => {
    const x = U.clamp((Math.log10(T) - Math.log10(0.008)) / (Math.log10(300) - Math.log10(0.008)), 0, 1);
    return new THREE.Color().setHSL(0.66 - 0.66 * x, 0.85, 0.42 + 0.12 * x);
  };

  /* 沿折線流動的粒子：用於氦氣、冷卻水、訊號、電力等連接 */
  App.Flow = function (scene, points, color, o = {}) {
    const P = points.map((p) => (p.isVector3 ? p : new THREE.Vector3(...p)));
    const lens = [0];
    for (let i = 1; i < P.length; i++) lens.push(lens[i - 1] + P[i].distanceTo(P[i - 1]));
    const total = lens[lens.length - 1];
    const at = (s) => {
      s = ((s % total) + total) % total;
      for (let i = 1; i < lens.length; i++) if (s <= lens[i]) return P[i - 1].clone().lerp(P[i], (s - lens[i - 1]) / (lens[i] - lens[i - 1] || 1));
      return P[P.length - 1].clone();
    };
    const group = new THREE.Group(); scene.add(group);
    const pipe = U.tube(P, o.radius || 0.03, new THREE.MeshStandardMaterial({ color: o.pipeColor || color, transparent: true, opacity: o.pipeOpacity ?? 0.35, roughness: 0.5 }), false, 2);
    group.add(pipe);
    const n = o.count || Math.max(4, Math.round(total * (o.density || 3)));
    const geo = new THREE.SphereGeometry(o.dot || 0.045, 10, 8);
    const mat = new THREE.MeshBasicMaterial({ color });
    const dots = [];
    for (let i = 0; i < n; i++) { const m = new THREE.Mesh(geo, mat); group.add(m); dots.push(m); }
    let off = 0;
    const F = {
      group, total, at, speed: o.speed ?? 0.8, on: true, mat,
      update(dt) {
        if (!F.on) return;
        off += dt * F.speed;
        dots.forEach((d, i) => d.position.copy(at(off + (i / n) * total)));
      },
      show(v) { group.visible = v; },
    };
    F.update(0);
    return F;
  };

  /* 設備方塊：主體 + 正面面板 + 標籤 */
  App.device = function (ctx, o) {
    const g = new THREE.Group();
    const body = U.box(o.w, o.h, o.d, U.mat(o.color || 0x2b3446, { roughness: 0.6, metalness: 0.3 }), 0, o.h / 2, 0);
    g.add(body);
    if (o.panel !== false) {
      const p = U.box(o.w * 0.86, o.h * 0.8, 0.02, U.mat(o.panelColor || 0x1a2232, { emissive: o.glow || 0x000000, emissiveIntensity: 0.25 }), 0, o.h / 2, o.d / 2 + 0.011);
      g.add(p);
      // LED
      for (let i = 0; i < (o.leds ?? 3); i++) g.add(U.sphere(0.025, U.glow(o.ledColor || 0x2ecc71), -o.w * 0.35 + i * 0.08, o.h * 0.82, o.d / 2 + 0.03, 8));
    }
    g.position.set(...o.pos);
    if (o.rotY) g.rotation.y = o.rotY;
    ctx.scene.add(g);
    if (o.label) ctx.label(o.label, [o.pos[0], o.pos[1] + o.h + (o.labelDy ?? 0.25), o.pos[2]], o.cls || '');
    g.body = body;
    return g;
  };

  /* 稀釋冷凍機（含框架、真空罩、各級板） */
  App.buildFridge = function (ctx, o = {}) {
    const { scene } = ctx;
    const g = new THREE.Group(); scene.add(g);
    const s = o.scale || 1;
    const plates = [];
    PD.stages.forEach((st, i) => {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(st.r * s, st.r * s, 0.07 * s, 48), U.metal(i === 0 ? 0x9aa4b2 : 0xc98a4b, { roughness: 0.35 }));
      m.position.y = st.y * s; g.add(m); plates.push(m);
      if (i < PD.stages.length - 1) {
        const q = PD.stages[i + 1];
        for (let k = 0; k < 3; k++) {
          const a = (k / 3) * Math.PI * 2 + 0.5, rr = (q.r - 0.12) * s;
          const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.025 * s, 0.025 * s, (st.y - q.y) * s, 8), U.metal(0xb0b8c4));
          rod.position.set(rr * Math.cos(a), ((st.y + q.y) / 2) * s, rr * Math.sin(a)); g.add(rod);
        }
      }
    });
    // 樣品盒
    const box = U.box(0.35 * s, 0.25 * s, 0.3 * s, U.metal(0xd08a3a), 0, 0.55 * s, 0); g.add(box);
    let can = null;
    if (o.can !== false) {
      can = new THREE.Mesh(new THREE.CylinderGeometry(1.15 * s, 1.15 * s, 3.0 * s, 48, 1, true), new THREE.MeshStandardMaterial({ color: 0xaab6c8, transparent: true, opacity: o.canOpacity ?? 0.12, side: THREE.DoubleSide, depthWrite: false, metalness: 0.5, roughness: 0.3 }));
      can.position.y = 1.8 * s; g.add(can);
    }
    if (o.frame !== false) {
      const fm = U.metal(0x5d6878, { roughness: 0.5 });
      const H = 4.6 * s, W = 1.6 * s;
      [[-W, -W], [W, -W], [-W, W], [W, W]].forEach(([x, z]) => g.add(U.box(0.08 * s, H, 0.08 * s, fm, x, H / 2 - 0.0, z)));
      g.add(U.box(2 * W + 0.1 * s, 0.1 * s, 2 * W + 0.1 * s, fm, 0, 3.45 * s, 0));
      // 脈衝管冷頭
      const ph = new THREE.Mesh(new THREE.CylinderGeometry(0.16 * s, 0.16 * s, 0.6 * s, 20), U.metal(0xd8dee8)); ph.position.set(0.55 * s, 3.75 * s, 0.2 * s); g.add(ph);
      g.ptHead = ph;
    }
    g.plates = plates; g.box = box; g.can = can;
    if (o.pos) g.position.set(...o.pos);
    return g;
  };

  /* 2D 插圖：長條圖 */
  App.bars = function (g, W, H, P, items, o = {}) {
    const max = o.max || Math.max(...items.map((d) => d[1])) * 1.15;
    const m = { l: o.l || 120, r: 46, t: 8, b: 22 };
    const bh = (H - m.t - m.b) / items.length;
    items.forEach(([name, v, col], i) => {
      const y = m.t + i * bh + bh * 0.18; const w = ((W - m.l - m.r) * v) / max;
      g.fillStyle = col || '#e0a54a'; g.fillRect(m.l, y, Math.max(1, w), bh * 0.64);
      P.text(g, name, m.l - 6, y + bh * 0.46, '#cfd8e6', 'right');
      P.text(g, (o.fmt || ((x) => x))(v), m.l + w + 5, y + bh * 0.46, '#ffd28a');
    });
    if (o.footer) P.text(g, o.footer, W / 2, H - 5, '#9fb0c8', 'center');
  };
})();

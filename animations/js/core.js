/* 核心框架：渲染器、相機控制、標籤、UI、插圖畫布與共用工具
 * 每個場景以 App.register({...}) 註冊，切換場景時重建 THREE.Scene。
 */
(function () {
  'use strict';
  const SCENES = [];
  const $ = (id) => document.getElementById(id);

  /* ---------------- 簡易軌道相機控制 ---------------- */
  class Orbit {
    constructor(camera, dom) {
      this.camera = camera; this.dom = dom;
      this.target = new THREE.Vector3();
      this.r = 10; this.theta = 0.6; this.phi = 1.1; // theta: 方位角, phi: 極角
      this.home = null;
      this.anim = null;
      let drag = null;
      dom.addEventListener('contextmenu', (e) => e.preventDefault());
      dom.addEventListener('pointerdown', (e) => {
        drag = { x: e.clientX, y: e.clientY, pan: e.button === 2 || e.shiftKey };
        dom.setPointerCapture(e.pointerId); this.anim = null;
      });
      dom.addEventListener('pointermove', (e) => {
        if (!drag) return;
        const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
        drag.x = e.clientX; drag.y = e.clientY;
        if (drag.pan) {
          const s = this.r * 0.0016;
          const right = new THREE.Vector3().setFromMatrixColumn(camera.matrix, 0);
          const up = new THREE.Vector3().setFromMatrixColumn(camera.matrix, 1);
          this.target.addScaledVector(right, -dx * s).addScaledVector(up, dy * s);
        } else {
          this.theta -= dx * 0.006;
          this.phi = Math.min(Math.PI - 0.05, Math.max(0.05, this.phi - dy * 0.006));
        }
        this.apply();
      });
      dom.addEventListener('pointerup', () => { drag = null; });
      dom.addEventListener('wheel', (e) => {
        e.preventDefault(); this.anim = null;
        this.r = Math.min(200, Math.max(0.5, this.r * Math.exp(e.deltaY * 0.0012)));
        this.apply();
      }, { passive: false });
    }
    set(pos, target) {
      this.target.set(...target);
      const v = new THREE.Vector3(...pos).sub(this.target);
      this.r = v.length();
      this.phi = Math.acos(v.y / this.r);
      this.theta = Math.atan2(v.x, v.z);
      this.apply();
    }
    setHome(pos, target) { this.home = { pos, target }; this.set(pos, target); }
    reset() { if (this.home) this.flyTo(this.home.pos, this.home.target); }
    flyTo(pos, target, dur = 1.2) {
      const from = { r: this.r, theta: this.theta, phi: this.phi, t: this.target.clone() };
      const tt = new THREE.Vector3(...target);
      const v = new THREE.Vector3(...pos).sub(tt);
      const r = v.length();
      let theta = Math.atan2(v.x, v.z);
      while (theta - from.theta > Math.PI) theta -= 2 * Math.PI;
      while (theta - from.theta < -Math.PI) theta += 2 * Math.PI;
      this.anim = { from, to: { r, theta, phi: Math.acos(v.y / r), t: tt }, k: 0, dur };
    }
    update(dt) {
      if (!this.anim) return;
      const a = this.anim; a.k = Math.min(1, a.k + dt / a.dur);
      const e = a.k < 0.5 ? 2 * a.k * a.k : 1 - Math.pow(-2 * a.k + 2, 2) / 2;
      this.r = a.from.r + (a.to.r - a.from.r) * e;
      this.theta = a.from.theta + (a.to.theta - a.from.theta) * e;
      this.phi = a.from.phi + (a.to.phi - a.from.phi) * e;
      this.target.lerpVectors(a.from.t, a.to.t, e);
      this.apply();
      if (a.k >= 1) this.anim = null;
    }
    apply() {
      const s = Math.sin(this.phi);
      this.camera.position.set(
        this.target.x + this.r * s * Math.sin(this.theta),
        this.target.y + this.r * Math.cos(this.phi),
        this.target.z + this.r * s * Math.cos(this.theta));
      this.camera.lookAt(this.target);
      this.camera.updateMatrixWorld();
    }
  }

  /* ---------------- 共用工具 ---------------- */
  const U = {
    clamp: (x, a, b) => Math.min(b, Math.max(a, x)),
    lerp: (a, b, t) => a + (b - a) * t,
    smooth: (t) => t * t * (3 - 2 * t),
    gauss() { // Box-Muller
      let u = 0, v = 0;
      while (u === 0) u = Math.random();
      while (v === 0) v = Math.random();
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    },
    mat(color, o = {}) {
      return new THREE.MeshStandardMaterial(Object.assign({ color, roughness: 0.45, metalness: 0.1 }, o));
    },
    metal(color, o = {}) {
      return new THREE.MeshStandardMaterial(Object.assign({ color, roughness: 0.28, metalness: 0.85 }, o));
    },
    glow(color, opacity = 1) {
      return new THREE.MeshBasicMaterial({ color, transparent: opacity < 1, opacity });
    },
    box(w, h, d, material, x = 0, y = 0, z = 0) {
      const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
      m.position.set(x, y, z); return m;
    },
    sphere(r, material, x = 0, y = 0, z = 0, seg = 24) {
      const m = new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(8, seg >> 1)), material);
      m.position.set(x, y, z); return m;
    },
    /* 由點列建立折線管 */
    tube(points, radius, material, closed = false, segPer = 6) {
      const path = new THREE.CurvePath();
      const P = points.map((p) => (p.isVector3 ? p : new THREE.Vector3(...p)));
      for (let i = 0; i < P.length - 1; i++) path.add(new THREE.LineCurve3(P[i], P[i + 1]));
      if (closed) path.add(new THREE.LineCurve3(P[P.length - 1], P[0]));
      const geo = new THREE.TubeGeometry(path, Math.max(8, P.length * segPer), radius, 8, false);
      return new THREE.Mesh(geo, material);
    },
    smoothTube(points, radius, material, closed = false, seg = 200) {
      const P = points.map((p) => (p.isVector3 ? p : new THREE.Vector3(...p)));
      const curve = new THREE.CatmullRomCurve3(P, closed);
      return new THREE.Mesh(new THREE.TubeGeometry(curve, seg, radius, 8, closed), material);
    },
    line(points, color, opacity = 1) {
      const g = new THREE.BufferGeometry().setFromPoints(points.map((p) => (p.isVector3 ? p : new THREE.Vector3(...p))));
      return new THREE.Line(g, new THREE.LineBasicMaterial({ color, transparent: opacity < 1, opacity }));
    },
    /* 可更新的動態線：回傳 {obj, set(pointsArray)} */
    dynLine(n, color, opacity = 1) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
      const obj = new THREE.Line(g, new THREE.LineBasicMaterial({ color, transparent: opacity < 1, opacity }));
      obj.frustumCulled = false;
      return {
        obj,
        set(pts) {
          const a = g.attributes.position.array;
          const m = Math.min(n, pts.length);
          for (let i = 0; i < m; i++) { a[3 * i] = pts[i][0]; a[3 * i + 1] = pts[i][1]; a[3 * i + 2] = pts[i][2]; }
          g.setDrawRange(0, m); g.attributes.position.needsUpdate = true;
        },
      };
    },
    arrow(dir, origin, len, color, head = 0.25, headW = 0.12) {
      return new THREE.ArrowHelper(new THREE.Vector3(...dir).normalize(), new THREE.Vector3(...origin), len, color, head, headW);
    },
    /* 粗箭頭（圓柱 + 圓錐），可用 setDir 更新 */
    fatArrow(color, len = 1, r = 0.04) {
      const g = new THREE.Group();
      const mat = U.mat(color, { emissive: color, emissiveIntensity: 0.35 });
      const shaft = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1, 12), mat);
      const head = new THREE.Mesh(new THREE.ConeGeometry(r * 2.6, r * 7, 16), mat);
      g.add(shaft, head);
      g.setVec = (v) => {
        const L = v.length();
        if (L < 1e-6) { g.visible = false; return; }
        g.visible = true;
        const hl = Math.min(r * 7, L * 0.5);
        shaft.scale.set(1, Math.max(1e-3, L - hl), 1); shaft.position.y = (L - hl) / 2;
        head.scale.set(1, hl / (r * 7), 1); head.position.y = L - hl / 2;
        g.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v.clone().normalize());
      };
      g.setVec(new THREE.Vector3(0, len, 0));
      return g;
    },
    /* 對稱實矩陣的 Jacobi 特徵值分解，回傳 {values, vectors}（vectors[k] 為第 k 個特徵向量），依特徵值排序 */
    eigSym(A) {
      const n = A.length;
      const a = A.map((r) => r.slice());
      const v = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => (i === j ? 1 : 0)));
      for (let sweep = 0; sweep < 60; sweep++) {
        let off = 0;
        for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += a[p][q] * a[p][q];
        if (off < 1e-18) break;
        for (let p = 0; p < n; p++) {
          for (let q = p + 1; q < n; q++) {
            if (Math.abs(a[p][q]) < 1e-14) continue;
            const th = (a[q][q] - a[p][p]) / (2 * a[p][q]);
            const t = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1));
            const c = 1 / Math.sqrt(t * t + 1), s = t * c;
            for (let k = 0; k < n; k++) {
              const akp = a[k][p], akq = a[k][q];
              a[k][p] = c * akp - s * akq; a[k][q] = s * akp + c * akq;
            }
            for (let k = 0; k < n; k++) {
              const apk = a[p][k], aqk = a[q][k];
              a[p][k] = c * apk - s * aqk; a[q][k] = s * apk + c * aqk;
            }
            for (let k = 0; k < n; k++) {
              const vkp = v[k][p], vkq = v[k][q];
              v[k][p] = c * vkp - s * vkq; v[k][q] = s * vkp + c * vkq;
            }
          }
        }
      }
      const idx = [...Array(n).keys()].sort((i, j) => a[i][i] - a[j][j]);
      return { values: idx.map((i) => a[i][i]), vectors: idx.map((i) => v.map((row) => row[i])) };
    },
    /* Transmon / CPB：電荷基底 H = 4EC(n-ng)^2 - EJ/2 (|n><n+1| + h.c.) */
    transmon(EJ, EC, ng = 0, N = 12) {
      const dim = 2 * N + 1;
      const H = Array.from({ length: dim }, () => new Array(dim).fill(0));
      for (let i = 0; i < dim; i++) {
        const n = i - N;
        H[i][i] = 4 * EC * (n - ng) * (n - ng);
        if (i + 1 < dim) { H[i][i + 1] = -EJ / 2; H[i + 1][i] = -EJ / 2; }
      }
      return U.eigSym(H);
    },
  };

  /* ---------------- 場景執行環境 ---------------- */
  const App = {
    U,
    register(def) { SCENES.push(def); },
    start() {
      SCENES.sort((a, b) => a.num - b.num);
      const canvas = $('gl');
      const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
      renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
      this.renderer = renderer;
      this.camera = new THREE.PerspectiveCamera(45, 1, 0.05, 500);
      this.orbit = new Orbit(this.camera, canvas);
      this.paused = false; this.speed = 1;
      const resize = () => {
        const w = window.innerWidth, h = window.innerHeight;
        renderer.setSize(w, h, false);
        this.camera.aspect = w / h;
        // 左側面板顯示時，把 3D 畫面中心往右移，避免被面板擋住
        const off = !document.body.classList.contains('hide-ui') && w > 820 ? 180 : 0;
        if (off) this.camera.setViewOffset(w, h, -off, 0, w, h); else this.camera.clearViewOffset();
        this.camera.updateProjectionMatrix();
      };
      this.resize = resize;
      window.addEventListener('resize', resize); resize();

      const nav = $('scene-nav');
      SCENES.forEach((s, i) => {
        const b = document.createElement('button');
        b.textContent = `${s.num}. ${s.short || s.title}`;
        b.title = s.title;
        b.onclick = () => this.show(i);
        nav.appendChild(b);
      });
      window.addEventListener('keydown', (e) => {
        if (e.target && e.target.tagName === 'INPUT') return;
        if (e.key === 'ArrowRight' || e.key === 'PageDown') this.show((this.cur + 1) % SCENES.length);
        else if (e.key === 'ArrowLeft' || e.key === 'PageUp') this.show((this.cur - 1 + SCENES.length) % SCENES.length);
        else if (e.key === ' ') { e.preventDefault(); this.paused = !this.paused; $('paused-badge').style.display = this.paused ? 'block' : 'none'; }
        else if (e.key === 'h' || e.key === 'H') { document.body.classList.toggle('hide-ui'); resize(); }
        else if (e.key === 'r' || e.key === 'R') this.orbit.reset();
        else if (e.key === 'f' || e.key === 'F') {
          if (!document.fullscreenElement) document.documentElement.requestFullscreen?.(); else document.exitFullscreen?.();
        }
      });
      window.addEventListener('hashchange', () => this.showByHash());
      const params = new URLSearchParams(location.search);
      if (params.has('noui')) { document.body.classList.add('hide-ui'); resize(); }
      if (params.has('clean')) document.body.classList.add('clean');
      this.showByHash();
      let last = performance.now();
      this.time = 0;
      const loop = (now) => {
        const dt = Math.min(0.05, (now - last) / 1000); last = now;
        this.orbit.update(dt);
        if (this.active) {
          const d = this.paused ? 0 : dt * this.speed;
          this.time += d;
          this.active.update && this.active.update(this.time, d);
        }
        renderer.render(this.scene, this.camera);
        this.updateLabels();
        if (this.insetDraw) this.drawInset();
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    },
    showByHash() {
      const id = location.hash.replace('#', '');
      const i = SCENES.findIndex((s) => s.id === id);
      this.show(i >= 0 ? i : 0, true);
    },
    show(i, fromHash) {
      if (this.cur === i && this.active) return;
      this.cur = i;
      const def = SCENES[i];
      if (!fromHash && location.hash !== '#' + def.id) history.replaceState(null, '', '#' + def.id);
      // 釋放舊場景
      if (this.scene) {
        this.active && this.active.dispose && this.active.dispose();
        this.scene.traverse((o) => {
          o.geometry && o.geometry.dispose();
          if (o.material) (Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => m.dispose());
        });
      }
      this.labels = []; $('labels').innerHTML = '';
      $('controls').innerHTML = '';
      this.insetDraw = null; $('inset-wrap').style.display = 'none';
      [...$('scene-nav').children].forEach((b, k) => b.classList.toggle('active', k === i));
      $('scene-num').textContent = `場景 ${def.num} / ${SCENES.length}`;
      $('scene-title').textContent = def.title;
      $('scene-sub').textContent = def.subtitle || '';
      $('scene-desc').innerHTML = def.desc || '';

      const scene = new THREE.Scene();
      scene.background = new THREE.Color(def.bg || 0x070c16);
      scene.add(new THREE.HemisphereLight(0xcfe0ff, 0x1a1408, 1.1));
      const d1 = new THREE.DirectionalLight(0xffffff, 2.2); d1.position.set(5, 10, 7); scene.add(d1);
      const d2 = new THREE.DirectionalLight(0x88aaff, 0.8); d2.position.set(-6, 3, -5); scene.add(d2);
      this.scene = scene;
      this.time = 0;
      const cam = def.camera || { pos: [0, 3, 10], target: [0, 0, 0] };
      this.orbit.setHome(cam.pos, cam.target);
      this.active = def.build(this.ctx(scene)) || {};
    },
    ctx(scene) {
      const app = this;
      return {
        scene, THREE, U, app,
        label(html, pos, cls = '') {
          const el = document.createElement('div');
          el.className = 'lbl ' + cls; el.innerHTML = html;
          $('labels').appendChild(el);
          const L = { el, pos: pos.isVector3 ? pos : new THREE.Vector3(...pos), obj: null, visible: true,
            set(h) { el.innerHTML = h; }, show(v) { this.visible = v; } };
          app.labels.push(L); return L;
        },
        /* 標籤跟隨物件（加上偏移） */
        labelOn(obj, html, offset = [0, 0, 0], cls = '') {
          const L = this.label(html, offset, cls); L.obj = obj; L.offset = new THREE.Vector3(...offset); return L;
        },
        ui: {
          row() { const r = document.createElement('div'); r.className = 'ctl-row'; $('controls').appendChild(r); return r; },
          button(text, onClick, row) {
            const b = document.createElement('button'); b.textContent = text;
            b.onclick = () => onClick(b);
            (row || this.row()).appendChild(b); return b;
          },
          /* 一組互斥按鈕 */
          radio(options, initial, onChange) {
            const r = this.row(); const bs = [];
            options.forEach(([val, text]) => {
              const b = this.button(text, () => { bs.forEach((x) => x.classList.remove('on')); b.classList.add('on'); onChange(val); }, r);
              if (val === initial) b.classList.add('on');
              bs.push(b);
            });
            return { set(val) { options.forEach(([v], k) => bs[k].classList.toggle('on', v === val)); } };
          },
          toggle(text, initial, onChange) {
            const b = this.button(text, () => { b.classList.toggle('on'); onChange(b.classList.contains('on')); });
            if (initial) b.classList.add('on');
            return b;
          },
          slider(text, min, max, step, value, onChange, fmt = (v) => v) {
            const w = document.createElement('label'); w.className = 'slider';
            w.innerHTML = `<span class="top"><span>${text}</span><span class="val"></span></span>`;
            const inp = document.createElement('input');
            Object.assign(inp, { type: 'range', min, max, step, value });
            const val = w.querySelector('.val');
            const upd = () => { const v = parseFloat(inp.value); val.textContent = fmt(v); onChange(v); };
            inp.oninput = upd; w.appendChild(inp); $('controls').appendChild(w);
            val.textContent = fmt(value);
            return { set(v) { inp.value = v; upd(); }, get: () => parseFloat(inp.value) };
          },
          readout() { const d = document.createElement('div'); d.className = 'readout'; $('controls').appendChild(d); return d; },
        },
        inset(title, draw) {
          $('inset-wrap').style.display = 'block'; $('inset-title').textContent = title;
          app.insetDraw = draw;
        },
      };
    },
    updateLabels() {
      const w = window.innerWidth, h = window.innerHeight;
      const v = new THREE.Vector3();
      for (const L of this.labels) {
        if (L.obj) { v.copy(L.offset); L.obj.localToWorld(v); L.pos.copy(v); }
        v.copy(L.pos).project(this.camera);
        const vis = L.visible && v.z < 1 && (!L.obj || L.obj.visible);
        L.el.style.display = vis ? 'block' : 'none';
        if (vis) { L.el.style.left = ((v.x + 1) / 2) * w + 'px'; L.el.style.top = ((1 - v.y) / 2) * h + 'px'; }
      }
    },
    drawInset() {
      const c = $('inset'); const g = c.getContext('2d');
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      if (c.width !== 380 * dpr) { c.width = 380 * dpr; c.height = 230 * dpr; }
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.clearRect(0, 0, 380, 230);
      this.insetDraw(g, 380, 230, Plot);
    },
  };

  /* ---------------- 2D 插圖小工具 ---------------- */
  const Plot = {
    font: '12px "Microsoft JhengHei","Noto Sans TC","WenQuanYi Zen Hei",sans-serif',
    /* 建立座標框，回傳 X(x)、Y(y) 映射 */
    frame(g, W, H, xr, yr, opt = {}) {
      const m = Object.assign({ l: 46, r: 12, t: 10, b: 30 }, opt.m || {});
      const X = (x) => m.l + ((x - xr[0]) / (xr[1] - xr[0])) * (W - m.l - m.r);
      const Y = (y) => H - m.b - ((y - yr[0]) / (yr[1] - yr[0])) * (H - m.t - m.b);
      g.strokeStyle = 'rgba(160,180,210,.35)'; g.lineWidth = 1;
      g.beginPath(); g.moveTo(m.l, m.t); g.lineTo(m.l, H - m.b); g.lineTo(W - m.r, H - m.b); g.stroke();
      g.fillStyle = '#9fb0c8'; g.font = Plot.font;
      if (opt.xlabel) { g.textAlign = 'center'; g.fillText(opt.xlabel, (m.l + W - m.r) / 2, H - 6); }
      if (opt.ylabel) { g.save(); g.translate(12, (m.t + H - m.b) / 2); g.rotate(-Math.PI / 2); g.textAlign = 'center'; g.fillText(opt.ylabel, 0, 0); g.restore(); }
      (opt.xticks || []).forEach(([v, s]) => { g.textAlign = 'center'; g.fillText(s, X(v), H - m.b + 14); });
      (opt.yticks || []).forEach(([v, s]) => { g.textAlign = 'right'; g.fillText(s, m.l - 5, Y(v) + 4); });
      return { X, Y, m };
    },
    curve(g, f, x0, x1, X, Y, color, lw = 2, n = 200) {
      g.strokeStyle = color; g.lineWidth = lw; g.beginPath();
      for (let i = 0; i <= n; i++) { const x = x0 + ((x1 - x0) * i) / n; const y = f(x); i ? g.lineTo(X(x), Y(y)) : g.moveTo(X(x), Y(y)); }
      g.stroke();
    },
    dot(g, x, y, r, color) { g.fillStyle = color; g.beginPath(); g.arc(x, y, r, 0, 2 * Math.PI); g.fill(); },
    text(g, s, x, y, color = '#e8eef8', align = 'left') { g.fillStyle = color; g.font = Plot.font; g.textAlign = align; g.fillText(s, x, y); },
  };
  App.Plot = Plot;
  window.App = App;
})();

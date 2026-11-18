/* 離子阱場景 9：光子互連 — 兩個模組的通訊離子各放出一顆和自己糾纏的光子，在分光鏡上做雙光子干涉，
 * 偵測器的符合計數「宣告」遠端糾纏（糾纏交換）；再用本地 MS 閘把糾纏交給記憶離子。
 * 成功率模型：每次嘗試 p = ½ · η²（η = 單顆光子從離子到被偵測的總效率；½ = 線性光學只能分辨 4 個貝爾態中的 2 個）。
 * 嘗試頻率取每秒 5×10⁵ 次（含週期性重新冷卻，代表值）。
 */
App.register({
  id: 'photonic', num: 9, short: '光子互連：遠端糾纏',
  title: '光子互連：讓兩個模組的離子遠端糾纏',
  subtitle: '每顆通訊離子放出一顆和自己糾纏的光子 → 兩顆光子在分光鏡上變得無法分辨 → 偵測器的響法「宣告」兩顆遠方離子已經糾纏',
  desc: `<p><b>為什麼需要</b>：一條離子鏈約 30–50 顆就到極限，QCCD 晶片也有上限。下一步是把很多個<b>模組</b>（各自一個阱、一個真空腔）連起來。模組之間沒有共享振動，MS 閘跨不過去，只能靠<b>光子</b>傳遞量子關聯。</p>
<p><b>① 離子–光子糾纏</b>：超快 π 脈衝把通訊離子激發到 P 態，幾奈秒內自發輻射放出<b>一顆</b>光子；掉到哪個子能階決定光子的偏振（或頻率、發射時間），所以 <span class="eq">(|↓⟩|H⟩ + |↑⟩|V⟩)/√2</span>。</p>
<p><b>② 收集</b>：高 NA 物鏡把光子耦合進單模光纖，送到中間的<b>貝爾態分析站</b>（50:50 分光鏡 + 偏振分光鏡 + 4 個單光子偵測器）。物鏡只收得到約 10 %，加上光纖耦合與偵測效率，每顆光子被偵測到的總效率 η 只有約 1–3 %。</p>
<p><b>③ 雙光子干涉 → 糾纏交換</b>：兩顆光子在分光鏡上<b>無法分辨</b>，就不可能知道哪顆來自哪顆離子。兩個偵測器以特定組合同時響（例：不同出口、偏振正交 → |Ψ⁻⟩；同一出口、偏振正交 → |Ψ⁺⟩），光子被投影到貝爾態，離子也就被投影成 <span class="eq">(|↓↑⟩ ∓ |↑↓⟩)/√2</span>。兩顆離子從未見面，卻糾纏了。</p>
<p><b>宣告式（heralded）</b>：大多數嘗試失敗（光子沒收到、遺失，或兩顆光子落在同一個偵測器而無法分辨貝爾態），但只要響法正確就<b>確定</b>成功；失敗只是重來，不引入錯誤。成功率 <span class="eq">p ≈ ½·η²</span>，乘上每秒數十萬次的嘗試 → 每秒數十到數百對（Oxford 2020：約 182 對 / 秒、保真度約 94 %，⁸⁸Sr⁺）。</p>
<p><b>④ 交給記憶離子</b>：發光的散射光會干擾同阱的量子位元，所以用<b>雙元素</b>：通訊離子（¹³⁸Ba⁺ 493 nm、⁸⁸Sr⁺ 422 nm）專門放光子，記憶離子（¹⁷¹Yb⁺、⁴³Ca⁺）存資訊。成功後用本地 MS 閘把糾纏交給記憶離子，通訊離子重設、繼續嘗試。</p>
<p><b>拿來做什麼</b>：一對遠端貝爾態 + 本地閘 + 量測 + 2 個古典位元 = <b>量子態傳送</b>或<b>量子閘傳送</b>（跨模組 CNOT），多個模組就能當一台電腦（Oxford 2025：相隔約 2 公尺的兩個模組跑 Grover）。品質不夠時用<b>糾纏純化</b>蒸餾。</p>
<p><b>和超導比</b>：離子天生會發可見光 / 近紅外光子，還能頻率轉換到 1550 nm 通訊波段走長光纖；超導量子位元是微波，要靠效率仍很低的微波→光學轉換器。打開「光子可分辨」看看：干涉失效，宣告了也只剩古典關聯（保真度 50 %）。</p>`,
  camera: { pos: [0, 5.6, 11.8], target: [0, 1.1, 1.3] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const QC = App.QC, COMM = 0x7ee05a, V493 = App.wlColor(493);
    const Y = 1.3, PH = 0x9fff6a;

    /* ---------- 兩個模組 ---------- */
    const mod = (side) => {
      const cx = side * 3.9;
      const box = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.4, 1.5), new THREE.MeshStandardMaterial({ color: 0xb8c2d0, metalness: 0.6, roughness: 0.35, transparent: true, opacity: 0.14, depthWrite: false }));
      box.position.set(cx, Y, 0); scene.add(box);
      [[1, 1], [-1, -1], [1, -1], [-1, 1]].forEach(([a, b], k) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 2.2, 10), U.metal(k < 2 ? 0xd9a441 : 0x8a93a0, { transparent: true, opacity: 0.4 })); m.rotation.z = Math.PI / 2; m.position.set(cx, Y + a * 0.25, b * 0.25); scene.add(m); });
      const comm = App.particle(scene, COMM, 0.11, [cx - side * 0.75, Y, 0]);
      const mem = [0, 0.75].map((dx) => App.particle(scene, QC.ion, 0.1, [cx + side * dx, Y, 0]));
      const lens = new THREE.Mesh(new THREE.SphereGeometry(0.28, 24, 12), new THREE.MeshStandardMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.6 }));
      lens.scale.set(1, 1, 0.3); lens.position.set(comm.position.x, Y, 0.85); scene.add(lens);
      ctx.label(side < 0 ? '模組 A' : '模組 B', [cx, Y + 1.05, 0], 'gold');
      ctx.label(side < 0 ? '通訊離子 Ba⁺ ／ 記憶離子 Yb⁺' : '記憶離子 Yb⁺ ／ 通訊離子 Ba⁺', [cx, Y - 0.95, 0.75], 'small');
      return { cx, side, comm, mem, lens };
    };
    const M = [mod(-1), mod(1)];
    ctx.label('高 NA 物鏡 → 單模光纖', [M[0].lens.position.x - 1.3, Y + 0.25, 1.1], 'small');

    /* ---------- 光纖與貝爾態分析站 ---------- */
    const BS = new THREE.Vector3(0, 0.45, 2.7);
    const fib = M.map((m) => new THREE.CatmullRomCurve3([m.lens.position.clone().add(new THREE.Vector3(0, 0, 0.12)), new THREE.Vector3(m.lens.position.x, 0.6, 1.8), new THREE.Vector3(m.side * 1.4, 0.45, 2.6), BS.clone().add(new THREE.Vector3(m.side * 0.28, 0, 0))]));
    fib.forEach((c) => scene.add(new THREE.Mesh(new THREE.TubeGeometry(c, 80, 0.025, 8, false), new THREE.MeshStandardMaterial({ color: 0xffd28a, transparent: true, opacity: 0.45 }))));
    ctx.label('光纖', [-1.9, 0.8, 2.3], 'small');
    const cube = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.42, 0.42), new THREE.MeshStandardMaterial({ color: 0xcfeaff, transparent: true, opacity: 0.35, depthWrite: false }));
    cube.position.copy(BS); scene.add(cube);
    const diag = new THREE.Mesh(new THREE.PlaneGeometry(0.58, 0.42), new THREE.MeshBasicMaterial({ color: 0x9fd8ff, transparent: true, opacity: 0.5, side: THREE.DoubleSide }));
    diag.position.copy(BS); diag.rotation.y = Math.PI / 4; scene.add(diag);
    ctx.label('50:50 分光鏡', [BS.x, BS.y + 0.45, BS.z], 'small');
    const DET = [['a', 'H', -0.95], ['a', 'V', -0.45], ['b', 'H', 0.45], ['b', 'V', 0.95]].map(([port, pol, x], i) => {
      const p = new THREE.Vector3(x, 0.45, 3.75);
      const b = U.box(0.3, 0.3, 0.3, U.mat(0x2b3446, { metalness: 0.4, emissive: 0x000000 }), p.x, p.y, p.z); scene.add(b);
      ctx.label(`D${i + 1}<br>${port}·${pol}`, [p.x, p.y - 0.42, p.z + 0.1], 'small');
      return { port, pol, p, b, flash: 0 };
    });
    [[-0.7, 3.3], [0.7, 3.3]].forEach(([x, z]) => { const c = U.box(0.25, 0.25, 0.25, new THREE.MeshStandardMaterial({ color: 0xffe0a0, transparent: true, opacity: 0.4 }), x, 0.45, z); scene.add(c); });
    ctx.label('偏振分光鏡 + 4 個單光子偵測器', [0, 1.05, 3.6], 'teal');
    const sig = M.map((m) => new THREE.CatmullRomCurve3([new THREE.Vector3(0, 0.3, 3.75), new THREE.Vector3(m.side * 2.2, 0.15, 2.4), new THREE.Vector3(m.cx, 0.2, 1.1), new THREE.Vector3(m.cx, Y - 0.7, 0.3)]));
    sig.forEach((c) => scene.add(new THREE.Mesh(new THREE.TubeGeometry(c, 60, 0.012, 6, false), new THREE.MeshBasicMaterial({ color: 0x38c6d9, transparent: true, opacity: 0.35 }))));
    ctx.label('古典「宣告」訊號', [2.6, 0.2, 2.2], 'small');
    const sigDots = M.map(() => U.sphere(0.06, U.glow(0x38c6d9), 0, 0, 0, 10)); sigDots.forEach((d) => { d.visible = false; scene.add(d); });

    /* ---------- 雷射、光子、糾纏線 ---------- */
    const exc = M.map((m) => App.beam(scene, [m.comm.position.x, Y + 1.3, -0.8], m.comm.position, App.wlColor(455), 0.04, 0.8));
    const phot = M.map(() => App.particle(scene, PH, 0.06));
    phot.forEach((p) => { p.visible = false; });
    const tether = M.map(() => { const l = U.dynLine(2, 0xff6ad5, 0.8); scene.add(l.obj); l.obj.visible = false; return l; });
    const arc = U.dynLine(61, 0xff6ad5, 0.9); arc.obj.material.transparent = true; scene.add(arc.obj);
    const lbArc = ctx.label('', [0, Y + 2.3, 0], 'big');
    const local = M.map(() => { const l = U.dynLine(21, 0xffd28a, 0.9); scene.add(l.obj); l.obj.visible = false; return l; });
    const lbStage = ctx.label('', [0, Y + 1.2, 0], 'gold');
    const lost = App.photons(scene, PH, 30, { size: 0.04 });

    /* ---------- 狀態 ---------- */
    let eta = 0.5, disting = false, auto = false, tab = 'stat';
    let phase = 'idle', t = 0, att = null;
    let ent = null; // null | 'comm' | 'mem'
    let entF = 1, entSign = '−';
    const S = { n: 0, both: 0, herald: 0, pat: { 'Ψ⁻': 0, 'Ψ⁺': 0, '無法宣告': 0 } };
    const RATE = 5e5; // 每秒嘗試次數（代表值）
    const pTheory = () => 0.5 * eta * eta;
    const sample = () => {
      const got = [Math.random() < eta, Math.random() < eta];
      let pat = null, dets = [];
      if (got[0] && got[1]) {
        const u = Math.random();
        if (u < 0.25) { pat = 'Ψ⁻'; dets = Math.random() < 0.5 ? [0, 3] : [1, 2]; }
        else if (u < 0.5) { pat = 'Ψ⁺'; dets = Math.random() < 0.5 ? [0, 1] : [2, 3]; }
        else { pat = '無法宣告'; const d = Math.floor(Math.random() * 4); dets = [d]; }
      } else if (got[0] || got[1]) dets = [Math.floor(Math.random() * 4)];
      return { got, pat, dets };
    };
    const record = (a) => { S.n++; if (a.got[0] && a.got[1]) { S.both++; S.pat[a.pat]++; if (a.pat !== '無法宣告') S.herald++; } };
    const start = () => {
      if (phase !== 'idle') return;
      if (ent) { ent = null; }
      att = sample(); phase = 'excite'; t = 0;
      M.forEach((m, i) => { phot[i].visible = false; });
    };
    const curvePt = (i, u) => fib[i].getPointAt(U.clamp(u, 0, 1));

    ui.button('▶ 單次嘗試', () => { auto = false; start(); });
    const bAuto = ui.toggle('▶ 連續嘗試（成功就停）', false, (on) => { auto = on; if (on) start(); });
    ui.button('快轉 10,000 次（只算統計）', () => { for (let k = 0; k < 10000; k++) record(sample()); tab = 'stat'; tabUI.set('stat'); });
    ui.button('④ 本地 MS：糾纏交給記憶離子', () => { if (ent === 'comm' && phase === 'idle') { phase = 'swap'; t = 0; } });
    ui.button('重置', () => { phase = 'idle'; ent = null; auto = false; bAuto.classList.remove('on'); Object.assign(S, { n: 0, both: 0, herald: 0, pat: { 'Ψ⁻': 0, 'Ψ⁺': 0, '無法宣告': 0 } }); phot.forEach((p) => { p.visible = false; }); });
    ui.slider('每顆光子被偵測到的總效率 η', 0.01, 0.8, 0.01, eta, (v) => { eta = v; }, (v) => `${(v * 100).toFixed(0)} %（實際約 1–3 %；預設調高方便觀察）`);
    ui.toggle('光子可分辨（時間錯開 → 干涉失效）', false, (on) => { disting = on; });
    const tabUI = ui.radio([['stat', '插圖：統計'], ['rate', '插圖：成功率 vs η'], ['level', '插圖：離子–光子糾纏']], 'stat', (v) => { tab = v; });
    const ro = ui.readout();
    exc.forEach((b) => b.on(false));

    ctx.inset('', (g, W, H, P) => {
      const tt = document.getElementById('inset-title');
      if (tab === 'stat') {
        tt.textContent = `嘗試 ${S.n.toLocaleString()} 次的結果（兩顆光子都到達 ${S.both.toLocaleString()} 次）`;
        App.bars(g, W, H, P, [['兩顆都到達', S.both, '#9fff6a'], ['宣告 Ψ⁻', S.pat['Ψ⁻'], '#ff6ad5'], ['宣告 Ψ⁺', S.pat['Ψ⁺'], '#c58bff'], ['同偵測器（失敗）', S.pat['無法宣告'], '#7f90a8']], { l: 112, max: Math.max(1, S.both) * 1.15, footer: S.n ? `實測 p = ${(S.herald / S.n).toExponential(2)}，理論 ½η² = ${pTheory().toExponential(2)}` : '按「單次嘗試」或「快轉 10,000 次」' });
        return;
      }
      if (tab === 'rate') {
        tt.textContent = '每秒得到幾對遠端糾纏（嘗試 5×10⁵ 次 / 秒，代表值）';
        const { X, Y: Yp } = P.frame(g, W, H, [-2.3, 0], [-2, 6], { xticks: [[-2, '1 %'], [-1, '10 %'], [0, '100 %']], yticks: [[0, '1'], [2, '100'], [4, '10⁴'], [6, '10⁶']], xlabel: '每顆光子的總效率 η', m: { l: 44, b: 32 } });
        P.curve(g, (x) => Math.log10(RATE * 0.5 * Math.pow(10, 2 * x)), -2.3, 0, X, Yp, '#ff6ad5', 2.5);
        g.strokeStyle = '#ffc04a'; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(X(-2.3), Yp(4)); g.lineTo(X(0), Yp(4)); g.stroke(); g.setLineDash([]);
        P.text(g, '本地 MS 閘（約 100 μs）≈ 10⁴ 次 / 秒', X(-2.25), Yp(4) - 5, '#ffc04a');
        g.fillStyle = 'rgba(142,240,160,.15)'; g.fillRect(X(-2), Yp(6), X(Math.log10(0.03)) - X(-2), Yp(-2) - Yp(6));
        P.text(g, '實際系統', X(-1.95), Yp(-1.3), '#8ef0a0');
        const lx = Math.log10(eta); P.dot(g, X(lx), Yp(Math.log10(RATE * pTheory())), 5, '#ffd28a');
        return;
      }
      tt.textContent = '通訊離子放出的光子和離子糾纏（示意）';
      const L = (x0, x1, y, col, s, sx) => { g.strokeStyle = col; g.lineWidth = 3; g.beginPath(); g.moveTo(x0, y); g.lineTo(x1, y); g.stroke(); g.lineWidth = 1; P.text(g, s, sx ?? x1 + 6, y + 4, col); };
      L(150, 230, 40, '#dfe6f0', 'P 激發態');
      L(70, 140, 180, '#4f8cff', '|↓⟩', 40); L(240, 310, 180, '#ff5a5f', '|↑⟩');
      g.strokeStyle = '#b46cff'; g.lineWidth = 2; g.beginPath(); g.moveTo(190, 180); g.lineTo(190, 46); g.stroke(); g.lineWidth = 1;
      P.text(g, '① 超快 π 脈衝', 150, 168, '#d7b8ff');
      const wig = (x0, y0, x1, y1, col) => { g.strokeStyle = col; g.lineWidth = 1.8; g.beginPath(); for (let i = 0; i <= 40; i++) { const u = i / 40; const x = x0 + (x1 - x0) * u + 5 * Math.sin(u * 24), y = y0 + (y1 - y0) * u; i ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); g.lineWidth = 1; };
      wig(170, 44, 110, 176, '#9fff6a'); wig(210, 44, 270, 176, '#9fff6a');
      P.text(g, '② 放出 H 光子', 30, 100, '#9fff6a'); P.text(g, '② 放出 V 光子', 280, 100, '#9fff6a');
      P.text(g, '(|↓⟩|H⟩ + |↑⟩|V⟩)/√2', W / 2, 212, '#ffd28a', 'center');
    });

    return {
      update(time, dt) {
        t += dt;
        DET.forEach((d) => { d.flash = Math.max(0, d.flash - dt * 1.5); d.b.material.emissive.setHex(d.flash > 0.05 ? 0x6aff3a : 0x000000); d.b.material.emissiveIntensity = d.flash; });
        let stage = '';
        if (phase === 'excite') {
          stage = '① 超快 π 脈衝激發兩邊的通訊離子';
          exc.forEach((b) => b.on(true, 0.9)); M.forEach((m) => m.comm.glow(1));
          if (t > 0.35) { phase = 'fly'; t = 0; exc.forEach((b) => b.on(false)); att.dir = M.map(() => new THREE.Vector3(U.gauss(), U.gauss(), -Math.abs(U.gauss())).normalize()); phot.forEach((p) => { p.visible = true; }); }
        } else if (phase === 'fly') {
          stage = '② 各放出一顆和自己糾纏的光子（洋紅細線 = 離子–光子糾纏）';
          const T1 = 1.3;
          M.forEach((m, i) => {
            const p = phot[i];
            if (att.got[i]) {
              const u = t / T1;
              if (u < 0.2) p.position.copy(m.comm.position).lerp(m.lens.position, u / 0.2); else p.position.copy(curvePt(i, (u - 0.2) / 0.8));
            } else { p.position.copy(m.comm.position).addScaledVector(att.dir[i], t * 2.4); }
            tether[i].obj.visible = true; tether[i].set([m.comm.position.toArray(), p.position.toArray()]);
          });
          if (t > T1) {
            phase = 'detect'; t = 0; record(att);
            phot.forEach((p) => { p.visible = false; }); tether.forEach((l) => { l.obj.visible = false; });
            att.dets.forEach((k) => { DET[k].flash = 1; });
            if (att.pat && att.pat !== '無法宣告') { ent = 'comm'; entF = disting ? 0.5 : 1; entSign = att.pat === 'Ψ⁻' ? '−' : '+'; phase = 'herald'; }
          }
        } else if (phase === 'detect') {
          stage = !(att.got[0] && att.got[1]) ? `③ 失敗：${att.got[0] || att.got[1] ? '只有一顆光子到達' : '兩顆光子都沒收到'} → 重新冷卻、再試一次` : '③ 兩顆光子落在同一個偵測器 → 無法分辨貝爾態，失敗';
          if (t > 0.9) { phase = 'idle'; t = 0; if (auto) start(); }
        } else if (phase === 'herald') {
          stage = `③ 宣告成功：偵測器 ${att.dets.map((k) => 'D' + (k + 1)).join(' + ')} 同時響 → |Ψ${entSign === '−' ? '⁻' : '⁺'}⟩，古典訊號通知兩邊`;
          sigDots.forEach((d, i) => { d.visible = t < 1; d.position.copy(sig[i].getPointAt(Math.min(1, t))); });
          if (t > 1.6) { phase = 'idle'; sigDots.forEach((d) => { d.visible = false; }); if (auto) { auto = false; bAuto.classList.remove('on'); } }
        } else if (phase === 'swap') {
          stage = '④ 本地 MS 閘（同一個阱內有共享振動）把糾纏交給記憶離子；通訊離子重設';
          local.forEach((l, i) => { const a = M[i].comm.position, b = M[i].mem[0].position; const pts = []; for (let s = 0; s <= 20; s++) { const u = s / 20; pts.push([a.x + (b.x - a.x) * u, a.y + 0.6 * 4 * u * (1 - u), 0]); } l.set(pts); l.obj.visible = true; });
          if (t > 1.8) { phase = 'idle'; ent = 'mem'; local.forEach((l) => { l.obj.visible = false; }); }
        } else {
          stage = ent === 'mem' ? '記憶離子保存遠端糾纏 → 可做量子態 / 量子閘傳送；通訊離子可以繼續下一輪' : ent === 'comm' ? '遠端糾纏建立！按 ④ 把它交給記憶離子' : '按「單次嘗試」或「連續嘗試」';
        }
        lbStage.set(stage);
        // 糾纏弧線
        const pair = ent === 'mem' ? [M[0].mem[0], M[1].mem[0]] : ent === 'comm' ? [M[0].comm, M[1].comm] : null;
        if (pair) {
          const a = pair[0].position, b = pair[1].position; const pts = [];
          for (let s = 0; s <= 60; s++) { const u = s / 60; pts.push([a.x + (b.x - a.x) * u, a.y + 2.2 * 4 * u * (1 - u), 0]); }
          arc.set(pts); arc.obj.material.opacity = entF === 1 ? 0.9 : 0.35; arc.obj.visible = true;
          lbArc.show(true); lbArc.set(entF === 1 ? `遠端糾纏 (|↓↑⟩ ${entSign} |↑↓⟩)/√2` : '只有古典關聯（光子可分辨，保真度 50 %）');
        } else { arc.obj.visible = false; lbArc.show(false); }
        M.forEach((m) => { if (phase !== 'excite') m.comm.glow(ent === 'comm' ? 0.8 : 0.35); m.mem[0].glow(ent === 'mem' ? 0.9 : 0.35); });
        lost.update(dt);
        const pm = S.n ? S.herald / S.n : 0;
        ro.innerHTML = `嘗試 <b>${S.n.toLocaleString()}</b> 次，宣告成功 <b>${S.herald.toLocaleString()}</b> 次（實測 p = ${S.n ? pm.toExponential(2) : '—'}；理論 ½η² = ${pTheory().toExponential(2)}）<br>`
          + `換算速率：5×10⁵ 次 / 秒 × p ≈ <b>${(RATE * pTheory()).toFixed(RATE * pTheory() < 10 ? 1 : 0)} 對 / 秒</b>（η = 2 % 時約 100 對 / 秒）<br>`
          + (disting ? '<b style="color:#ff8a8a">光子可分辨：分光鏡上不干涉，宣告後只有古典關聯</b>' : '光子無法分辨：雙光子干涉成立，宣告即糾纏');
      },
    };
  },
});

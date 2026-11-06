/* 周邊場景 5：低溫佈線 — 每顆量子位元需要哪些線、各級放什麼元件、熱負載預算 */
App.register({
  id: 'wiring', num: 5, short: '低溫佈線',
  title: '低溫佈線：從室溫接頭到量子晶片',
  subtitle: '每條線都要「讓訊號下去、讓熱與雜訊上不來」',
  desc: `<p>典型 transmon 系統每顆量子位元需要：<b>XY 驅動線</b>、<b>Z 磁通線</b>，加上每 4–8 顆共用一組<b>讀取輸入/輸出</b>，以及放大器的<b>泵浦與偏壓</b>、溫度計與加熱器的<b>直流線</b>。</p>
<p><b>輸入線</b>：各級<b>衰減器</b>把室溫雜訊壓低，<b>熱錨定</b>在每一級；MXC 端加低通與紅外（Eccosorb）濾波。<br>
<b>磁通線</b>：衰減較少（需要較大電流），以低通濾波為主。<br>
<b>輸出線</b>：環行器/隔離器 → TWPA → 超導 NbTi 同軸 → 4 K HEMT → 室溫放大。</p>
<p>線數隨量子位元增加 → <b>被動熱傳導</b>與<b>衰減器發熱</b>佔用各級冷卻功率，這是規模化的主要限制之一（右下角）。</p>`,
  camera: { pos: [3.0, 2.7, 4.8], target: [0.1, 2.05, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const st = App.PD.stages;
    const fr = App.buildFridge(ctx, { can: false, frame: false });
    st.forEach((s) => ctx.label(s.name, [-s.r - 0.95, s.y, 0], 'small'));
    const lines = [
      { key: 'xy', name: 'XY 驅動', color: 0x4f8cff, x: -0.55, comps: { '4k': ['att', '−20 dB'], cp: ['att', '−20 dB'], mxc: ['att', '−20 dB + 濾波'] } },
      { key: 'z', name: 'Z 磁通', color: 0x2ecc71, x: -0.33, comps: { '4k': ['att', '−10 dB'], mxc: ['filt', '低通 + Eccosorb'] } },
      { key: 'rin', name: '讀取輸入', color: 0x38c6d9, x: -0.11, comps: { '4k': ['att', '−20 dB'], cp: ['att', '−20 dB'], mxc: ['att', '−20 dB + 濾波'] } },
      { key: 'pump', name: 'TWPA 泵浦', color: 0xb07cff, x: 0.11, comps: { '4k': ['att', '−20 dB'], cp: ['att', '−10 dB'], mxc: ['coup', '定向耦合器'] } },
      { key: 'rout', name: '讀取輸出', color: 0xe0a54a, x: 0.33, comps: { rt: ['amp', '室溫放大'], '4k': ['hemt', 'HEMT ~40 dB'], mxc: ['circ', '隔離器 + TWPA'] } },
      { key: 'dc', name: '直流線束', color: 0x9aa4b2, x: 0.55, comps: { '4k': ['filt', 'RC 濾波'], mxc: ['filt', '溫度計/加熱器'] } },
    ];
    const yTop = st[0].y + 0.5, yBot = 0.68;
    const flows = {};
    const nameLbls = {};
    const compMeshes = [];
    lines.forEach((ln, i) => {
      const z = 0.25;
      const pts = ln.key === 'rout' ? [[ln.x, yBot, z], [ln.x, yTop, z]] : [[ln.x, yTop, z], [ln.x, yBot, z]];
      flows[ln.key] = App.Flow(scene, pts, ln.color, { speed: 0.9, radius: ln.key === 'dc' ? 0.03 : 0.018, pipeOpacity: 0.55, density: 4, dot: 0.03 });
      nameLbls[ln.key] = ctx.label(ln.name, [ln.x, yTop + 0.2 + i * 0.17, z], 'small');
      Object.entries(ln.comps).forEach(([sk, [type, txt]]) => {
        const s = sk === 'rt' ? { y: st[0].y + 0.3 } : st.find((q) => q.key === sk);
        const y = s.y + (sk === 'rt' ? 0 : -0.13);
        let m;
        if (type === 'att') m = U.box(0.09, 0.12, 0.09, U.mat(0x6c8db8));
        else if (type === 'filt') m = U.box(0.1, 0.16, 0.1, U.mat(0x3f7a5a));
        else if (type === 'circ') { m = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.06, 16), U.metal(0xb04a4a)); m.rotation.x = Math.PI / 2; }
        else if (type === 'hemt') m = U.box(0.14, 0.14, 0.12, U.mat(0x2ecc71, { emissive: 0x0a3a1a, emissiveIntensity: 0.6 }));
        else if (type === 'amp') m = U.box(0.14, 0.14, 0.12, U.mat(0x8a9bb0));
        else m = U.box(0.1, 0.1, 0.1, U.mat(0xb07cff));
        m.position.set(ln.x, y, z); scene.add(m);
        m.material.transparent = true;
        const lbl = ctx.label(txt, [ln.x + 0.14, y, z + 0.05], 'gold small'); lbl.show(false);
        lbl.el.style.transform = 'translate(0,-50%)';
        compMeshes.push({ m, ln: ln.key, txt, y, lbl, emi: m.material.emissive.clone(), ei: m.material.emissiveIntensity });
      });
    });
    // TWPA 盒
    const twpa = U.box(0.22, 0.12, 0.16, U.mat(0x38c6d9, { emissive: 0x0a3a44, emissiveIntensity: 0.7, transparent: true }), 0.33, 0.95, 0.25); scene.add(twpa);
    const genLbls = [ctx.label('TWPA', [0.75, 0.95, 0.25], 'teal small'), ctx.label('HEMT（4 K）', [0.95, st[2].y - 0.13, 0.25], 'small'), ctx.label('衰減器（熱錨定於各級）', [-1.55, st[4].y - 0.13, 0.25], 'small')];
    // 額外線束（依量子位元數）
    const bundle = new THREE.Group(); scene.add(bundle);
    const bGeo = new THREE.CylinderGeometry(0.008, 0.008, yTop - yBot, 6);
    const bMats = [new THREE.MeshBasicMaterial({ color: 0x4f8cff, transparent: true, opacity: 0.55 }), new THREE.MeshBasicMaterial({ color: 0x2ecc71, transparent: true, opacity: 0.55 }), new THREE.MeshBasicMaterial({ color: 0x38c6d9, transparent: true, opacity: 0.55 })];
    let nq = 20;
    let focus = 'all';
    const PW = App.PD.wiring;
    const counts = (n) => ({ xy: n, z: n, rin: Math.ceil(n / 6), rout: Math.ceil(n / 6), pump: Math.ceil(n / 6), dc: 4 });
    function rebuildBundle() {
      while (bundle.children.length) bundle.remove(bundle.children[0]);
      const c = counts(nq); const totalRF = c.xy + c.z + c.rin;
      const show = Math.min(totalRF, 400);
      for (let i = 0; i < show; i++) {
        const a = i * 2.399, r = 0.25 + 0.5 * Math.sqrt(i / Math.max(show, 1));
        const kind = i < c.xy * show / totalRF ? 0 : i < (c.xy + c.z) * show / totalRF ? 1 : 2;
        const m = new THREE.Mesh(bGeo, bMats[kind]); m.userData.kind = ['xy', 'z', 'rin'][kind];
        m.visible = focus === 'all' || focus === m.userData.kind;
        m.position.set(r * Math.cos(a), (yTop + yBot) / 2, -0.2 + r * Math.sin(a) * 0.6);
        bundle.add(m);
      }
    }
    rebuildBundle();
    ui.slider('量子位元數（線束示意）', 1, 200, 1, nq, (v) => { nq = v; rebuildBundle(); }, (v) => v.toFixed(0));
    // 聚焦單一線路：其他線路淡出、顯示該線各級元件說明、相機靠近
    const INFO = {
      xy: '<b>XY 驅動線</b>：送 4–8 GHz 微波脈衝做單量子位元閘。<br>數量：每顆量子位元 1 條。<br>配置：4 K −20 dB → Cold plate −20 dB → MXC −20 dB + 低通/紅外濾波；總衰減約 60 dB，使室溫熱雜訊降到 ~10⁻³ 光子。',
      z: '<b>Z 磁通線</b>：調整 SQUID 磁通（量子位元頻率）、做雙量子位元閘；直流與快速脈衝經 bias-tee 合併。<br>數量：每顆量子位元 1 條。<br>配置：4 K −10 dB；MXC ~1.3 GHz 低通 + Eccosorb。需要較大電流，所以衰減較少。',
      rin: '<b>讀取輸入線</b>：送入多工讀取脈衝（多個頻率同時）。<br>數量：每 4–8 顆量子位元共用 1 條。<br>配置與 XY 相同（共約 −60 dB）。',
      pump: '<b>TWPA 泵浦線</b>：提供參量放大器所需的泵浦微波。<br>數量：每條讀取輸出 1 條。<br>配置：衰減後經 MXC 的定向耦合器與讀取訊號合併送入 TWPA。',
      rout: '<b>讀取輸出線</b>（訊號往上走）：MXC 隔離器/環行器 → TWPA（20–30 dB）→ NbTi 超導同軸 → 4 K HEMT（~40 dB，耗電 5–10 mW）→ 室溫放大 → 下變頻 → ADC。<br>數量：每 4–8 顆量子位元共用 1 條。',
      dc: '<b>直流線束</b>：溫度計、加熱器、HEMT/TWPA 偏壓。<br>數量：數十條雙絞線（磷青銅/康銅），各級熱錨定並加 RC 濾波。',
    };
    function applyFocus(key) {
      focus = key;
      lines.forEach((ln) => {
        const f = flows[ln.key]; const on = key === 'all' || key === ln.key;
        const [pipe, ...dots] = f.group.children;
        pipe.material.opacity = key === 'all' ? 0.55 : on ? 1 : 0.06;
        pipe.material.emissive = new THREE.Color(on && key !== 'all' ? ln.color : 0x000000); pipe.material.emissiveIntensity = 0.6;
        dots.forEach((d) => { d.visible = on; d.scale.setScalar(key === ln.key ? 1.5 : 1); });
        nameLbls[ln.key].el.style.opacity = on ? 1 : 0.25;
      });
      compMeshes.forEach((c) => {
        const on = key === 'all' || key === c.ln;
        c.m.material.opacity = on ? 1 : 0.12;
        c.lbl.show(key === c.ln);
      });
      const amp = key === 'all' || key === 'rout' || key === 'pump';
      twpa.material.opacity = amp ? 1 : 0.12;
      genLbls.forEach((l) => (l.el.style.opacity = key === 'all' ? 1 : 0.25));
      bundle.children.forEach((m) => (m.visible = key === 'all' || key === m.userData.kind));
      const ln = lines.find((q) => q.key === key);
      fr.plates.forEach((pl) => { pl.material.transparent = true; pl.material.opacity = key === 'all' ? 1 : 0.35; pl.material.depthWrite = key === 'all'; pl.material.needsUpdate = true; });
      if (ln) ctx.app.orbit.flyTo([ln.x + 2.3, 2.6, 4.4], [ln.x, 1.95, 0.25], 1.0); else ctx.app.orbit.reset();
    }
    ui.radio([['all', '全部'], ...lines.map((ln) => [ln.key, ln.name])], 'all', applyFocus);
    const ro = ui.readout();
    const heat = () => {
      const c = counts(nq);
      const nCoax = c.xy + c.z + c.rin + c.rout + c.pump;
      return PW.stages.map((s, i) => {
        const passive = nCoax * PW.passive[i];
        const att = (c.xy + c.rin + c.pump) * PW.attDiss[i] + (i === 1 ? c.rout * PW.hemt : 0);
        return [s, passive + att, PW.cool[i]];
      });
    };
    const fmtW = (w) => (w >= 1 ? w.toFixed(2) + ' W' : w >= 1e-3 ? (w * 1e3).toFixed(1) + ' mW' : (w * 1e6).toFixed(1) + ' μW');
    ctx.inset('各級熱負載 / 可用冷卻功率（示意估算）', (g, W, H, P) => {
      const hs = heat();
      const items = hs.map(([s, h, cpow]) => [s, Math.min(150, (h / cpow) * 100), h / cpow > 1 ? '#ff5a5f' : h / cpow > 0.5 ? '#e0a54a' : '#2ecc71']);
      App.bars(g, W, H, P, items, { max: 150, fmt: (v) => (v >= 150 ? '>150' : v.toFixed(0)) + ' %', l: 90, footer: '100 % = 該級冷卻功率用盡（紅色）' });
    });
    return {
      update(t, dt) {
        Object.values(flows).forEach((f) => f.update(dt));
        compMeshes.forEach((cm) => {
          if (focus === cm.ln) { cm.m.material.emissive.setHex(0xffd28a); cm.m.material.emissiveIntensity = 0.35 + 0.3 * Math.sin(t * 5); }
          else { cm.m.material.emissive.copy(cm.emi); cm.m.material.emissiveIntensity = cm.ei; }
        });
        const c = counts(nq);
        const hs = heat();
        const cnt = { xy: c.xy, z: c.z, rin: c.rin, rout: c.rout, pump: c.pump, dc: '數十' };
        const lead = focus === 'all' ? '' : `${INFO[focus]}<br><span style="color:#ffd28a">目前 ${nq} 顆量子位元 → 此類線 ${cnt[focus]} 條</span><hr style="border-color:rgba(255,255,255,.12)">`;
        ro.innerHTML = lead + `${nq} 顆量子位元 → XY ${c.xy} 條、Z ${c.z} 條、讀取輸入/輸出 各 ${c.rin} 條、泵浦 ${c.pump} 條（同軸共 ${c.xy + c.z + c.rin + c.rout + c.pump} 條）<br>` +
          hs.map(([s, h, cp]) => `${s}：${fmtW(h)} / ${fmtW(cp)}`).join('<br>');
      },
    };
  },
});

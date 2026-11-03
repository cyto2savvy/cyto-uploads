/* LF02 3D shots (three.js r149). Toon + ink outlines like hf/three3d.js. Each factory returns {render(t)}; t = seconds. */
(function () {
  const INK = 0x0c1622;
  const cl = (x, a, b) => Math.max(a, Math.min(b, x));
  const sm = x => { x = cl(x, 0, 1); return x * x * (3 - 2 * x); };
  let GR = null;
  const grad = () => { if (GR) return GR; GR = new THREE.DataTexture(new Uint8Array([60, 150, 255]), 3, 1, THREE.RedFormat); GR.minFilter = GR.magFilter = THREE.NearestFilter; GR.needsUpdate = true; return GR; };
  const toon = (c, e = {}) => new THREE.MeshToonMaterial(Object.assign({ color: c, gradientMap: grad() }, e));
  const ol = (geo, mat, w = 0.04) => { const g = new THREE.Group(); const o = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide })); o.scale.setScalar(1 + w); g.add(o); const m = new THREE.Mesh(geo, mat); g.add(m); g.userData.m = m; return g; };
  const setup = (cv, fov = 40) => { const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true }); r.setPixelRatio(1); r.setSize(cv.width, cv.height, false);
    const sc = new THREE.Scene(); const cam = new THREE.PerspectiveCamera(fov, cv.width / cv.height, 0.1, 400); return { r, sc, cam }; };
  const lights = (sc, amb = 0.35) => { sc.add(new THREE.AmbientLight(0xffffff, amb)); const d = new THREE.DirectionalLight(0xffffff, 0.9); d.position.set(5, 10, 7); sc.add(d); return d; };
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const winTex = (base, lit) => { const c = document.createElement("canvas"); c.width = 64; c.height = 128; const x = c.getContext("2d"); x.fillStyle = base; x.fillRect(0, 0, 64, 128);
    for (let j = 6; j < 124; j += 14) for (let i = 6; i < 60; i += 14) { x.fillStyle = rnd() < 0.55 ? lit : "rgba(0,0,0,.25)"; x.fillRect(i, j, 8, 9); }
    const t = new THREE.CanvasTexture(c); t.magFilter = THREE.NearestFilter; return t; };
  const tower = (w, h, d, base, lit) => { const g = ol(new THREE.BoxGeometry(w, h, d), new THREE.MeshToonMaterial({ map: winTex(base, lit), gradientMap: grad() }), 0.03); g.position.y = h / 2; return g; };
  const ballTex = () => { const c = document.createElement("canvas"); c.width = 128; c.height = 64; const x = c.getContext("2d"); x.fillStyle = "#f07a1a"; x.fillRect(0, 0, 128, 64);
    x.strokeStyle = "#1a0d05"; x.lineWidth = 4; [[0, 32, 128, 32], [32, 0, 32, 64], [96, 0, 96, 64]].forEach(([a, b, c2, d]) => { x.beginPath(); x.moveTo(a, b); x.lineTo(c2, d); x.stroke(); }); return new THREE.CanvasTexture(c); };

  // ------------------------------------------------ 1. body-city fly-through into Queen's Park
  function bodycity(cv, o = {}) {
    const { r, sc, cam } = setup(cv, 45); seed = 11;
    sc.background = new THREE.Color(0x2b1640); sc.fog = new THREE.Fog(0x2b1640, 30, 120);
    lights(sc, 0.4);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), toon(0x7a2d4f)); ground.rotation.x = -Math.PI / 2; sc.add(ground);
    const road = new THREE.Mesh(new THREE.PlaneGeometry(10, 300), toon(0xc04b6a)); road.rotation.x = -Math.PI / 2; road.position.set(0, 0.02, -100); sc.add(road);
    for (let z = 5; z > -150; z -= 6) { const s = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 2.4), new THREE.MeshBasicMaterial({ color: 0xffd166 })); s.rotation.x = -Math.PI / 2; s.position.set(0, 0.04, z); sc.add(s); }
    const pal = [["#3fc1b0", "#fff3b0"], ["#7a5cc7", "#ffd166"], ["#f2c6da", "#ffe9a8"], ["#2f6f8f", "#ffd98a"], ["#ff9f5a", "#fff3b0"]];
    for (let z = 0; z > -140; z -= 7) for (const sx of [-1, 1]) { const p = pal[Math.floor(rnd() * pal.length)]; const h = 4 + rnd() * 14; const t = tower(4 + rnd() * 2, h, 4 + rnd() * 2, p[0], p[1]); t.position.x = sx * (9 + rnd() * 6); t.position.z = z - rnd() * 3; sc.add(t); }
    // heart tower (downtown) + CN-ish needle
    const needle = ol(new THREE.CylinderGeometry(0.35, 0.9, 40, 12), toon(0xd9d4c7)); needle.position.set(-26, 20, -70); sc.add(needle);
    const pod = ol(new THREE.SphereGeometry(2.2, 20, 12), toon(0xd9d4c7)); pod.scale.y = 0.6; pod.position.set(-26, 30, -70); sc.add(pod);
    const hs = new THREE.Shape(); hs.moveTo(0, -1.6); hs.bezierCurveTo(-3.2, 0.6, -1.6, 3, 0, 1.4); hs.bezierCurveTo(1.6, 3, 3.2, 0.6, 0, -1.6);
    const heart = ol(new THREE.ExtrudeGeometry(hs, { depth: 1.2, bevelEnabled: true, bevelSize: 0.4, bevelThickness: 0.4, bevelSegments: 3 }), toon(0xe63946)); heart.position.set(24, 26, -80); heart.scale.setScalar(2.4); sc.add(heart);
    // lungs = two pink trees (Don Valley)
    for (const sx of [-1, 1]) { const l = ol(new THREE.SphereGeometry(5, 18, 14), toon(0xff8fa8)); l.scale.set(0.8, 1.2, 0.8); l.position.set(sx * 40 + 34, 9, -50); sc.add(l); }
    // Queen's Park: wide block + towers + pitched roofs (generic Romanesque shape)
    const qp = new THREE.Group(); const stone = toon(0xc98f6a);
    const main = ol(new THREE.BoxGeometry(30, 9, 8), stone); main.position.y = 4.5; qp.add(main);
    const roof = ol(new THREE.ConeGeometry(17, 5, 4), toon(0x5a3a5a)); roof.rotation.y = Math.PI / 4; roof.scale.set(1, 1, 0.35); roof.position.y = 11; qp.add(roof);
    for (const x of [-8, 8]) { const t = ol(new THREE.BoxGeometry(4, 16, 4), stone); t.position.set(x, 8, 2); qp.add(t); const c = ol(new THREE.ConeGeometry(3.2, 4, 4), toon(0x5a3a5a)); c.rotation.y = Math.PI / 4; c.position.set(x, 18, 2); qp.add(c); }
    const arch = new THREE.Mesh(new THREE.PlaneGeometry(4, 5), new THREE.MeshBasicMaterial({ color: 0xffd98a })); arch.position.set(0, 2.5, 4.05); qp.add(arch);
    for (let i = -3; i <= 3; i++) if (i) { const w = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 2.2), new THREE.MeshBasicMaterial({ color: 0xffd98a })); w.position.set(i * 3.4, 5.5, 4.05); qp.add(w); }
    qp.position.set(0, 0, -150); sc.add(qp);
    // blood-cell cars
    const cells = []; for (let i = 0; i < 14; i++) { const c = ol(new THREE.TorusGeometry(0.7, 0.45, 10, 20), toon(0xe63946)); c.rotation.x = Math.PI / 2; c.position.set((i % 2 ? 2.4 : -2.4), 0.5, -i * 11); c.userData.v = i % 2 ? -9 : 7; sc.add(c); cells.push(c); }
    // snow
    const sg = new THREE.BufferGeometry(); const sp = new Float32Array(900); for (let i = 0; i < 300; i++) { sp[i * 3] = (rnd() - .5) * 80; sp[i * 3 + 1] = rnd() * 40; sp[i * 3 + 2] = -rnd() * 160; } sg.setAttribute("position", new THREE.BufferAttribute(sp, 3));
    const snow = new THREE.Points(sg, new THREE.PointsMaterial({ color: 0xffffff, size: 0.35 })); sc.add(snow);
    const dur = o.dur || 6;
    return { render(t) {
      const k = sm(t / dur);
      cam.position.set(Math.sin(k * 2.2) * 6 * (1 - k), 34 - 29 * k, 20 - 138 * k);
      cam.lookAt(0, 6 - 1 * k, cam.position.z - 30 - 10 * (1 - k));
      if (k > 0.75) cam.lookAt(0, 6, -150);
      heart.scale.setScalar(2.4 * (1 + 0.08 * Math.max(0, Math.sin(t * 7))));
      cells.forEach(c => { c.position.z = ((c.userData.v * t - c.position.x * 30) % 150) - 0; if (c.position.z > 10) c.position.z -= 150; });
      snow.position.y = -((t * 2) % 20);
      r.render(sc, cam);
    } };
  }

  // ------------------------------------------------ 2. adrenal "condos" on the kidneys, firing hormone basketballs
  function condos(cv, o = {}) {
    /* fix pass: 3 heroes only (left kidney+condos, right kidney+condos, hormone balls) + ground disc + fogged sky; eased orbit */
    const { r, sc, cam } = setup(cv, 38); seed = 21;
    sc.background = new THREE.Color(0x2b1640); sc.fog = new THREE.Fog(0x2b1640, 34, 70); lights(sc, 0.42);
    const ground = new THREE.Mesh(new THREE.CircleGeometry(30, 48), toon(0x47306b)); ground.rotation.x = -Math.PI / 2; sc.add(ground);
    const towers = [];
    for (const sx of [-1, 1]) {
      const k = ol(new THREE.SphereGeometry(4, 28, 20), toon(0xb03a6e)); k.scale.set(1.05, 0.8, 0.75); k.position.set(sx * 7, 3.4, 0); k.rotation.z = sx * 0.12; sc.add(k);
      const g = new THREE.Group(); g.position.set(sx * 7 - sx * 0.6, 5.9, 0); sc.add(g);
      [[0, 0, 2.2, 6], [1.6, 0.5, 1.4, 4], [-1.4, -0.4, 1.6, 4.8]].forEach(([x, z, w, h]) => { const t = tower(w, h, w, "#7a5cc7", "#ffd166"); t.position.x = x; t.position.z = z; g.add(t); });
      towers.push(g);
    }
    const sig = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 1, 8), new THREE.MeshBasicMaterial({ color: 0xff3b3b })); sc.add(sig);
    const bt = ballTex(); const balls = [];
    for (let i = 0; i < 10; i++) { const b = ol(new THREE.SphereGeometry(0.75, 20, 14), toon(0xffffff, { map: bt })); b.visible = false; sc.add(b); balls.push({ m: b, t0: 1.2 + i * 0.55, sx: i % 2 ? 1 : -1, vx: (i % 3 - 1) * 1.6 }); }
    const dur = o.dur || 8, tFire = o.tFire || 1.2;
    return { render(t) {
      const k = sm(t / dur); const a = 0.15 + 0.55 * k;
      cam.position.set(Math.sin(a) * (30 - 4 * k), 10 - 1.5 * k, Math.cos(a) * (30 - 4 * k)); cam.lookAt(0, 6.5, 0);
      const s = cl((t - 0.1) / 0.9, 0, 1); sig.visible = false; sig.scale.y = 40 * (1 - s) + 0.1; sig.position.set(0, 10 + 40 * (1 - s), 0);
      towers.forEach((g, i) => { const p = Math.max(0, Math.sin((t - tFire) * 9 + i)) * (t > tFire ? 0.08 : 0); g.scale.set(1 + p, 1 - p, 1 + p); });
      balls.forEach(b => { const u = t - (tFire + (b.t0 - 1.2)); if (u < 0 || u > 2.0) { b.m.visible = false; return; } b.m.visible = true;
        b.m.position.set(b.sx * 7 + b.vx * u, 13 + 10 * u - 8 * u * u, 5 * u); b.m.rotation.set(u * 6, u * 4, 0); });
      r.render(sc, cam);
    } };
  }

  // ------------------------------------------------ 3. downtown heart (calm, beating)
  function heart(cv, o = {}) {
    /* fix pass: ONE hero (the heart + its two vessels) + ground disc + fogged sky. Visible lub-dub squash & stretch
       at o.bpm (mix.py puts a heartbeat SFX on the same grid). Slow eased dolly-in. Heart sits right of frame (Cyto is left). */
    const { r, sc, cam } = setup(cv, 34); seed = 31;
    sc.background = new THREE.Color(0x1d1838); sc.fog = new THREE.Fog(0x1d1838, 26, 60); lights(sc, 0.36);
    const hs = new THREE.Shape(); hs.moveTo(0, -2.2); hs.bezierCurveTo(-4.4, 0.8, -2.2, 4.1, 0, 1.9); hs.bezierCurveTo(2.2, 4.1, 4.4, 0.8, 0, -2.2);
    const H = new THREE.Group(); sc.add(H);
    const h = ol(new THREE.ExtrudeGeometry(hs, { depth: 2.6, bevelEnabled: true, bevelSize: 0.9, bevelThickness: 1.1, bevelSegments: 5, curveSegments: 24 }), toon(0xd7263d), 0.03);
    h.position.set(0, 0, -1.3); H.add(h);
    for (const [x, c] of [[-1, 0x4a7bd1], [1.2, 0xc04b8a]]) { const v = ol(new THREE.CylinderGeometry(0.5, 0.6, 3, 14), toon(c)); v.position.set(x, 4.4, 0); v.rotation.z = x * 0.2; H.add(v); }
    H.position.set(0, 6.2, 0);
    const g = new THREE.Mesh(new THREE.CircleGeometry(22, 48), toon(0x2c2350)); g.rotation.x = -Math.PI / 2; sc.add(g);
    const per = 60 / (o.bpm || 66), dur = o.dur || 20;
    return { render(t) {
      const k = sm(t / dur);
      cam.position.set(-8.0 + 1.5 * k, 8.6, 37 - 4 * k); cam.lookAt(-7.4 + 1.2 * k, 7.6, 0);
      const ph = (t % per) / per;
      const b = Math.max(ph < 0.14 ? Math.sin(ph / 0.14 * Math.PI) : 0, ph > 0.2 && ph < 0.32 ? 0.6 * Math.sin((ph - 0.2) / 0.12 * Math.PI) : 0);
      H.scale.set(1 + 0.13 * b, 1 - 0.09 * b + 0.03 * (1 - b), 1 + 0.13 * b); H.rotation.y = 0.28 * Math.sin(t * 0.9); H.position.y = 6.2 + 0.25 * Math.sin(t * 1.3);
      r.render(sc, cam);
    } };
  }

  // ------------------------------------------------ 4. heist lasers at the nose "front door"
  function lasers(cv, o = {}) {
    const { r, sc, cam } = setup(cv, 50); seed = 41;
    sc.background = new THREE.Color(0x2a0a14); sc.fog = new THREE.Fog(0x2a0a14, 8, 46); lights(sc, 0.45);
    const tube = new THREE.Mesh(new THREE.CylinderGeometry(7, 7, 80, 32, 1, true), toon(0x8e2f5a, { side: THREE.BackSide })); tube.rotation.x = Math.PI / 2; tube.position.z = -30; sc.add(tube);
    for (let z = 4; z > -70; z -= 5) { const ring = new THREE.Mesh(new THREE.TorusGeometry(6.9, 0.18, 6, 40), new THREE.MeshBasicMaterial({ color: 0x5a1a3e })); ring.position.z = z; sc.add(ring); }
    if (false) for (let i = 0; i < 60; i++) { const hr = ol(new THREE.ConeGeometry(0.15, 1.6, 6), toon(0xe6a0aa), 0.08); const a = rnd() * Math.PI * 2; hr.position.set(Math.cos(a) * 6.3, Math.sin(a) * 6.3, -rnd() * 60); hr.lookAt(0, 0, hr.position.z); hr.rotateX(-Math.PI / 2); sc.add(hr); }
    const door = ol(new THREE.TorusGeometry(4, 0.6, 12, 40, Math.PI), toon(0xffd166)); door.position.set(0, -3, -48); sc.add(door);
    const lz = []; const lm = new THREE.MeshBasicMaterial({ color: 0xff2020 });
    for (let i = 0; i < 6; i++) { const g = new THREE.Group(); const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 14, 6), lm); beam.rotation.z = Math.PI / 2; g.add(beam);
      const glow = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 14, 8), new THREE.MeshBasicMaterial({ color: 0xff4040, transparent: true, opacity: 0.25 })); glow.rotation.z = Math.PI / 2; g.add(glow);
      g.position.z = -8 - i * 6; g.userData.ph = i * 0.9; sc.add(g); lz.push(g); }
    return { render(t) {
      const k = sm(t / (o.dur || 4)); cam.position.set(0, -0.5, 6 - 22 * k); cam.lookAt(0, -0.8, cam.position.z - 10);
      lz.forEach((g, i) => { g.rotation.z = Math.sin(t * 1.6 + g.userData.ph) * 0.9; g.position.y = Math.sin(t * 1.1 + i) * 2.4; });
      r.render(sc, cam);
    } };
  }
  window.C3D2 = { bodycity, condos, heart, lasers };
})();

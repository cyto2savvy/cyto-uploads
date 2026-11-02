/* Cyto 3D kit (three.js r149, UMD build in assets/three.min.js).
   Cel-shaded ("toon") materials + ink outlines so 3D matches the flat cutout rig.
   Every scene factory returns { render(t) } where t = seconds since the scene started.
   Drive it from the GSAP timeline (deterministic for HyperFrames seeks):
     const S = C3D.earth(canvasEl, opts);  tl.to(P,{t:dur,duration:dur,ease:"none",onUpdate:()=>S.render(P.t)}, start)
*/
(function () {
  const INK = 0x0c1622;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const ease = { out3: x => 1 - Math.pow(1 - clamp(x, 0, 1), 3), inOut: x => { x = clamp(x, 0, 1); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; },
                 back: x => { x = clamp(x, 0, 1); const c = 2.2; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); } };
  let GRAD = null;
  function grad() {
    if (GRAD) return GRAD;
    const d = new Uint8Array([28, 135, 255]);
    GRAD = new THREE.DataTexture(d, 3, 1, THREE.RedFormat); GRAD.minFilter = GRAD.magFilter = THREE.NearestFilter; GRAD.needsUpdate = true;
    return GRAD;
  }
  const toon = (color, extra = {}) => new THREE.MeshToonMaterial(Object.assign({ color, gradientMap: grad() }, extra));
  function outlined(geo, mat, w = 0.035) {           // mesh + inverted-hull ink outline
    const g = new THREE.Group(); const m = new THREE.Mesh(geo, mat);
    const o = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide }));
    o.scale.setScalar(1 + w); g.add(o); g.add(m); g.userData.mesh = m; return g;
  }
  function setup(canvas, fov = 35) {
    const r = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
    r.setPixelRatio(1); r.setSize(canvas.width, canvas.height, false);
    const sc = new THREE.Scene(); const cam = new THREE.PerspectiveCamera(fov, canvas.width / canvas.height, 0.1, 200);
    return { r, sc, cam };
  }
  function glowSprite(color = "#ffd166", size = 3) {
    const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d");
    const g = x.createRadialGradient(128, 128, 0, 128, 128, 128); g.addColorStop(0, color); g.addColorStop(.35, color + "88"); g.addColorStop(1, color + "00");
    x.fillStyle = g; x.fillRect(0, 0, 256, 256);
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthWrite: false, transparent: true })); s.scale.setScalar(size); return s;
  }
  function starfield(n = 400, R = 40, seed = 3) {
    let s = seed; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const p = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) { const th = rnd() * 6.283, ph = Math.acos(2 * rnd() - 1); p[i * 3] = R * Math.sin(ph) * Math.cos(th); p[i * 3 + 1] = R * Math.cos(ph); p[i * 3 + 2] = -Math.abs(R * Math.sin(ph) * Math.sin(th)) - 5; }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3));
    return new THREE.Points(g, new THREE.PointsMaterial({ color: 0xfaf4e8, size: 0.12, transparent: true, opacity: .8 }));
  }
  // ---- crude cartoon continents (lon, lat) for the Earth texture
  const LAND = [
    [[-168, 66], [-140, 70], [-95, 72], [-80, 62], [-62, 58], [-55, 48], [-67, 45], [-75, 38], [-81, 30], [-81, 25], [-90, 29], [-97, 26], [-105, 20], [-95, 16], [-83, 9], [-78, 8], [-85, 14], [-92, 15], [-105, 22], [-112, 30], [-117, 33], [-124, 40], [-124, 48], [-135, 58], [-150, 60], [-165, 60]],
    [[-45, 60], [-20, 70], [-20, 80], [-60, 82], [-70, 77], [-55, 65]],
    [[-78, 8], [-60, 10], [-50, 0], [-35, -6], [-40, -22], [-55, -35], [-65, -55], [-72, -50], [-73, -35], [-70, -18], [-80, -5]],
    [[-17, 21], [-5, 36], [10, 37], [32, 31], [43, 12], [51, 12], [40, -5], [40, -15], [32, -28], [20, -35], [13, -20], [9, -1], [-8, 5], [-17, 14]],
    [[-10, 36], [-9, 44], [-5, 48], [0, 51], [8, 55], [5, 62], [15, 69], [30, 71], [60, 70], [80, 73], [110, 77], [140, 72], [170, 70], [180, 66], [160, 60], [140, 52], [130, 42], [122, 30], [120, 22], [108, 20], [105, 10], [100, 13], [98, 8], [92, 22], [80, 15], [77, 8], [72, 20], [60, 25], [50, 30], [35, 30], [28, 37], [20, 40], [12, 44], [8, 44], [3, 43]],
    [[114, -22], [122, -18], [131, -12], [137, -12], [142, -11], [146, -19], [153, -27], [151, -34], [146, -39], [138, -35], [131, -31], [116, -35], [114, -26]],
    [[-74, 46], [-66, 49], [-56, 47], [-60, 44], [-66, 44], [-71, 42]]];
  function earthTexture() {
    const c = document.createElement("canvas"); c.width = 2048; c.height = 1024; const x = c.getContext("2d");
    x.fillStyle = "#2f74c4"; x.fillRect(0, 0, 2048, 1024);
    const P = ([lo, la]) => [(lo + 180) / 360 * 2048, (90 - la) / 180 * 1024];
    x.lineJoin = "round"; x.lineWidth = 10; x.strokeStyle = "#0c1622";
    LAND.forEach(poly => { x.beginPath(); poly.forEach((p, i) => { const [a, b] = P(p); i ? x.lineTo(a, b) : x.moveTo(a, b); }); x.closePath(); x.fillStyle = "#5fc27a"; x.fill(); x.stroke(); });
    x.fillStyle = "#f4f6f8"; x.fillRect(0, 0, 2048, 70); x.fillRect(0, 960, 2048, 64);
    const t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t;
  }
  const onSphere = (lon, lat, r) => { const phi = (lon + 180) / 180 * Math.PI, th = (90 - lat) / 180 * Math.PI;
    return new THREE.Vector3(-r * Math.cos(phi) * Math.sin(th), r * Math.cos(th), r * Math.sin(phi) * Math.sin(th)); };

  /* Earth in winter tilt, sun from the left; Toronto pin rotates from day into night.
     opts: {dur, rot0, rot1, label: element to pin over Toronto (screen-projected)} */
  function earth(canvas, o = {}) {
    const { r, sc, cam } = setup(canvas, 32); cam.position.set(0, 0.2, 8.2);
    sc.add(starfield());
    const tilt = new THREE.Group(); tilt.rotation.z = -0.41; sc.add(tilt);         // north pole leans away from the sun (northern winter)
    const spin = new THREE.Group(); tilt.add(spin);
    const R = 2.1;
    spin.add(outlined(new THREE.SphereGeometry(R, 96, 64), toon(0xffffff, { map: earthTexture() }), 0.025));
    const pinPos = onSphere(-79.4, 43.7, R);
    const pin = new THREE.Group(); pin.position.copy(pinPos); pin.lookAt(pinPos.clone().multiplyScalar(2)); spin.add(pin);
    const head = outlined(new THREE.SphereGeometry(0.14, 24, 16), toon(0xff7a59), 0.12); head.position.z = 0.38; pin.add(head);
    const stick = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.38, 8), new THREE.MeshBasicMaterial({ color: INK })); stick.rotation.x = Math.PI / 2; stick.position.z = 0.19; pin.add(stick);
    const sun = new THREE.DirectionalLight(0xffffff, 1.55); sc.add(sun); sc.add(new THREE.AmbientLight(0x29406b, 0.18));
    const sunBall = new THREE.Group(); const core = new THREE.Mesh(new THREE.SphereGeometry(0.55, 32, 16), new THREE.MeshBasicMaterial({ color: 0xffd166 }));
    sunBall.add(glowSprite("#ffd166", 4.2)); sunBall.add(core); sc.add(sunBall);
    const v = new THREE.Vector3();
    return { render(t) {
      const k = ease.inOut(t / (o.dur || 3));
      spin.rotation.y = (o.rot0 ?? -0.95) + ((o.rot1 ?? 0.55) - (o.rot0 ?? -0.95)) * k;
      sunBall.position.set(-4.6, 1.9 - 0.5 * k, -1.5); sun.position.set(-6, 1.2, 2.2);
      cam.position.z = 8.9 - 0.8 * k; cam.lookAt(0, 0.75, 0);
      r.render(sc, cam);
      if (o.label) { head.getWorldPosition(v); v.project(cam);
        const front = v.z < 1 && pin.getWorldPosition(new THREE.Vector3()).z > -0.2;
        o.label.style.left = ((v.x + 1) / 2 * canvas.width) + "px"; o.label.style.top = ((1 - v.y) / 2 * canvas.height) + "px"; o.label.style.opacity = front ? 1 : 0; }
    } };
  }

  /* 3D bar chart: bars = [{h, color}] (h in 0..1), grows at tGrow; labels = elements placed over each bar top. */
  function bars(canvas, o = {}) {
    const { r, sc, cam } = setup(canvas, 30);
    sc.add(new THREE.AmbientLight(0x6b84a8, 0.35)); const L = new THREE.DirectionalLight(0xffffff, 1.05); L.position.set(3, 6, 5); sc.add(L);
    const floor = outlined(new THREE.BoxGeometry(o.floorW || 5.2, 0.18, 2.4), toon(0x24425f), 0.02); floor.position.y = -0.09; sc.add(floor);
    const BS = (o.bars || []).map((b, i, a) => { const g = outlined(new THREE.BoxGeometry(1.2, 1, 1.2), toon(b.color), 0.04);
      g.position.x = (i - (a.length - 1) / 2) * 2.1; sc.add(g); return g; });
    const H = o.height || 2.5; const v = new THREE.Vector3();
    return { render(t) {
      (o.bars || []).forEach((b, i) => { const k = ease.back((t - (o.tGrow || 0) - i * 0.18) / 0.7); const h = Math.max(0.001, b.h * H * k);
        const sink = o.tSink != null ? ease.inOut((t - o.tSink) / 0.45) : 0;
        BS[i].scale.y = Math.max(0.001, h * (1 - sink)); BS[i].position.y = BS[i].scale.y / 2;
        if (o.labels && o.labels[i]) { v.set(BS[i].position.x, BS[i].scale.y + 0.15, 0.6).project(cam);
          const el = o.labels[i]; el.style.left = ((v.x + 1) / 2 * canvas.width) + "px"; el.style.top = ((1 - v.y) / 2 * canvas.height) + "px"; } });
      const a = -0.5 + 0.35 * (t / (o.dur || 4)) + (o.zoomAt != null ? 0.25 * ease.inOut((t - o.zoomAt) / 0.6) : 0);
      const d = 11 - (o.zoomAt != null ? 1.4 * ease.inOut((t - o.zoomAt) / 0.6) : 0);
      cam.position.set(Math.sin(a) * d, 2.9, Math.cos(a) * d); cam.lookAt(0, 0.95, 0);
      if (o.gap) { const top0 = BS[0].scale.y, top1 = BS[1].scale.y; v.set((BS[0].position.x + BS[1].position.x) / 2, -0.75, 1.2).project(cam);
        o.gap.style.left = ((v.x + 1) / 2 * canvas.width) + "px"; o.gap.style.top = ((1 - v.y) / 2 * canvas.height) + "px"; }
      r.render(sc, cam);
    } };
  }

  /* Vitamin D capsules rain + bounce (from tDrop), then morph out as a DNA helix rises (tDna). */
  function capsulesDna(canvas, o = {}) {
    const { r, sc, cam } = setup(canvas, 34); cam.position.set(0, 1.4, 10.5); cam.lookAt(0, 0.4, 0);
    sc.add(new THREE.AmbientLight(0x6b84a8, 0.35)); const L = new THREE.DirectionalLight(0xffffff, 1.1); L.position.set(3, 6, 5); sc.add(L);
    function capsule(c1, c2) {
      const g = new THREE.Group(), rr = 0.32, h = 0.55;
      const top = outlined(new THREE.CylinderGeometry(rr, rr, h, 32), toon(c1), 0.05); top.position.y = h / 2;
      const bot = outlined(new THREE.CylinderGeometry(rr, rr, h, 32), toon(c2), 0.05); bot.position.y = -h / 2;
      const capT = outlined(new THREE.SphereGeometry(rr, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), toon(c1), 0.05); capT.position.y = h;
      const capB = outlined(new THREE.SphereGeometry(rr, 32, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), toon(c2), 0.05); capB.position.y = -h;
      g.add(top, bot, capT, capB); return g;
    }
    const caps = [], N = 7, xs = [-2.6, -1.5, -0.5, 0.6, 1.6, 2.6, 0.1], zs = [0.2, -0.6, 0.5, -0.3, 0.4, -0.5, 1.2];
    for (let i = 0; i < N; i++) { const c = capsule(0xffb703, 0xff5a36); c.position.set(xs[i], 6, zs[i]); sc.add(c); caps.push(c); }
    const floorY = 0.32;
    // DNA
    const dna = new THREE.Group(); sc.add(dna);
    const NB = 15, rad = 0.85, rise = 0.27;
    for (let i = 0; i < NB; i++) { const a = i * 0.62, y = i * rise - NB * rise / 2;
      const p1 = new THREE.Vector3(Math.cos(a) * rad, y, Math.sin(a) * rad), p2 = new THREE.Vector3(-Math.cos(a) * rad, y, -Math.sin(a) * rad);
      const b1 = outlined(new THREE.SphereGeometry(0.17, 16, 12), toon(0x3fc1b0), 0.1); b1.position.copy(p1);
      const b2 = outlined(new THREE.SphereGeometry(0.17, 16, 12), toon(0xff7a59), 0.1); b2.position.copy(p2);
      const rung = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, rad * 2, 8), toon(i % 2 ? 0xffd166 : 0x7a5cc7));
      rung.position.set(0, y, 0); rung.lookAt(p1.x, y, p1.z); rung.rotateX(Math.PI / 2);
      dna.add(b1, b2, rung); }
    dna.position.y = 0.55;
    return { render(t) {
      const tD = o.tDrop || 0, tN = o.tDna ?? 99;
      caps.forEach((c, i) => {
        const t0 = tD + i * 0.09, s = Math.max(0, t - t0);
        // fall from y=6 with g, then damped bounces
        const g = 26, H0 = 6 - floorY, tf = Math.sqrt(2 * H0 / g);
        let y;
        if (s < tf) y = 6 - 0.5 * g * s * s;
        else { let v = g * tf * 0.45, tt = s - tf; y = floorY;
          for (let k = 0; k < 4; k++) { const tb = 2 * v / g; if (tt < tb) { y = floorY + v * tt - 0.5 * g * tt * tt; break; } tt -= tb; v *= 0.45; } }
        c.position.y = y; c.rotation.z = (i % 2 ? 1 : -1) * (0.9 + 0.5 * i) * Math.min(s, tf + 0.5) * 2.2 + (s > tf ? Math.PI / 2 : 0) * 0;
        c.rotation.x = 0.3 * i;
        const out = ease.inOut((t - tN) / 0.5); c.scale.setScalar(Math.max(0.001, 1 - out)); c.position.x = xs[i] * (1 + out * 1.5);
      });
      const din = ease.back((t - tN - 0.1) / 0.6);
      dna.scale.setScalar(Math.max(0.001, din * 0.95)); dna.rotation.y = t * 2.2; dna.rotation.z = 0.35;
      r.render(sc, cam);
    } };
  }
  window.C3D = { earth, bars, capsulesDna, toon, outlined, setup, glowSprite, starfield, ease };
})();

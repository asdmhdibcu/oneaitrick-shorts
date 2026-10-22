// Short #8 3D shots, rendered offline frame by frame (render3d.py): window.setup(name) then window.frame(t).
//   helix  DNA double helix; a Cas9-like clamp slides in and CRISPR cuts it at t = CUT
//   walk   dynein + dynactin walking along a microtubule, carrying a vesicle of cholesterol (DCTN1 makes dynactin's p150 arm)
//   jam    the p150 arm fails: the motor stalls, cholesterol can't move, and new cholesterol keeps appearing
//   pile   wide: cholesterol piled at the stalled motor, the far end of the track empty
//   fix    the arm is restored and the motor races on, cholesterol spread along the track
import * as THREE from "three";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/examples/jsm/postprocessing/OutputPass.js";

const W = 1080, H = 1920;
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
document.body.appendChild(renderer.domElement);

const AMBER = new THREE.Color("#ffb547"), TEAL = new THREE.Color("#3fc8e6"), NAVY = new THREE.Color("#05080f");
let scene, camera, composer, update;

// deterministic noise
let seed = 11;
const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const sstep = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const lerp = (a, b, t) => a + (b - a) * t;

function base(bg, fogNear, fogFar) {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(bg);
  scene.fog = new THREE.Fog(bg, fogNear, fogFar);
  camera = new THREE.PerspectiveCamera(32, W / H, 0.1, 400);
  scene.add(new THREE.HemisphereLight(0x9fd8ff, 0x0a0d18, 0.55));
  const key = new THREE.DirectionalLight(0xffe2b8, 1.6); key.position.set(6, 10, 9); scene.add(key);
  const rim = new THREE.DirectionalLight(0x4fd0ff, 1.4); rim.position.set(-8, -2, -6); scene.add(rim);
  composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  composer.addPass(new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.95, 0.55, 0.55));
  composer.addPass(new OutputPass());
}

let _dot = null;
const dot = () => { if (_dot) return _dot; const c = document.createElement("canvas"); c.width = c.height = 64; const x = c.getContext("2d");
  const g = x.createRadialGradient(32, 32, 0, 32, 32, 32); g.addColorStop(0, "rgba(255,255,255,1)"); g.addColorStop(0.4, "rgba(255,255,255,0.6)"); g.addColorStop(1, "rgba(255,255,255,0)");
  x.fillStyle = g; x.fillRect(0, 0, 64, 64); _dot = new THREE.CanvasTexture(c); return _dot; };
// floating out-of-focus specks for depth
function specks(n, spread, col) {
  const g = new THREE.BufferGeometry(); const p = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { p[i * 3] = (rnd() - 0.5) * spread; p[i * 3 + 1] = (rnd() - 0.5) * spread; p[i * 3 + 2] = (rnd() - 0.5) * spread; }
  g.setAttribute("position", new THREE.BufferAttribute(p, 3));
  const m = new THREE.PointsMaterial({ map: dot(), color: col, size: 0.16, transparent: true, opacity: 0.55, depthWrite: false });
  const pts = new THREE.Points(g, m); scene.add(pts); return pts;
}

// ------------------------------------------------------------------------------------------------ helix
function helix() {
  base("#04070d", 10, 46);
  const world = new THREE.Group(); world.rotation.z = -0.38; world.rotation.x = 0.25; scene.add(world);
  const N = 70, RISE = 0.42, TW = (Math.PI * 2) / 10, R = 1.25, CUTI = 38;
  const parts = [new THREE.Group(), new THREE.Group()]; parts.forEach((p) => world.add(p));
  const bbMat = new THREE.MeshStandardMaterial({ color: TEAL, emissive: TEAL, emissiveIntensity: 0.55, roughness: 0.35, metalness: 0.1 });
  const bbMat2 = new THREE.MeshStandardMaterial({ color: new THREE.Color("#8fe6ff"), emissive: new THREE.Color("#5fd8ff"), emissiveIntensity: 0.45, roughness: 0.35 });
  const yOf = (i) => (i - N / 2) * RISE;
  // two backbones, split into the part below and above the cut
  [[0, CUTI], [CUTI, N - 1]].forEach(([a, b], pi) => {
    [0, Math.PI * 0.78].forEach((off, si) => {
      const pts = [];
      for (let k = a * 4; k <= b * 4; k++) { const i = k / 4; const th = i * TW + off; pts.push(new THREE.Vector3(R * Math.cos(th), yOf(i), R * Math.sin(th))); }
      const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), pts.length * 2, 0.16, 10, false), si ? bbMat2 : bbMat);
      parts[pi].add(tube);
    });
  });
  // base pairs
  const pal = ["#ffb547", "#ff7a59", "#c8ff4d", "#b9a2ff"];
  const rungGeo = new THREE.CylinderGeometry(0.075, 0.075, 1, 8);
  const ballGeo = new THREE.SphereGeometry(0.17, 14, 10);
  for (let i = 0; i < N; i++) {
    const th = i * TW, y = yOf(i);
    const p1 = new THREE.Vector3(R * Math.cos(th), y, R * Math.sin(th)), p2 = new THREE.Vector3(R * Math.cos(th + Math.PI * 0.78), y, R * Math.sin(th + Math.PI * 0.78));
    const mid = p1.clone().add(p2).multiplyScalar(0.5);
    const c1 = new THREE.Color(pal[(i * 7) % 4]), c2 = new THREE.Color(pal[(i * 7 + 2) % 4]);
    [[p1, mid, c1], [mid, p2, c2]].forEach(([u, v, c]) => {
      const m = new THREE.Mesh(rungGeo, new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: 0.35, roughness: 0.4 }));
      const d = v.clone().sub(u); m.scale.y = d.length(); m.position.copy(u.clone().add(v).multiplyScalar(0.5));
      m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); parts[i < CUTI ? 0 : 1].add(m);
    });
    [p1, p2].forEach((p) => { const b = new THREE.Mesh(ballGeo, bbMat2); b.position.copy(p); parts[i < CUTI ? 0 : 1].add(b); });
  }
  // the Cas9-like clamp: a translucent amber shell with a bright core ring
  const clamp = new THREE.Group(); world.add(clamp);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(1.95, 0.09, 12, 64), new THREE.MeshBasicMaterial({ color: new THREE.Color("#ffd08a"), transparent: true }));
  const ring2 = new THREE.Mesh(new THREE.TorusGeometry(1.75, 0.05, 12, 64), new THREE.MeshBasicMaterial({ color: new THREE.Color("#ffb547"), transparent: true }));
  ring.rotation.x = Math.PI / 2; ring2.rotation.x = Math.PI / 2; clamp.add(ring, ring2);
  const shell = { scale: { setScalar() {} }, material: {} };
  // spark burst at the cut
  const NS = 160, sg = new THREE.BufferGeometry(), sp = new Float32Array(NS * 3), sv = [];
  for (let i = 0; i < NS; i++) { const u = rnd() * 2 - 1, a = rnd() * Math.PI * 2, r = Math.sqrt(1 - u * u); sv.push(new THREE.Vector3(r * Math.cos(a), u * 0.5, r * Math.sin(a)).multiplyScalar(2 + rnd() * 5)); }
  sg.setAttribute("position", new THREE.BufferAttribute(sp, 3));
  const sparks = new THREE.Points(sg, new THREE.PointsMaterial({ map: dot(), color: new THREE.Color("#ffe0a0"), size: 0.32, transparent: true, opacity: 0, depthWrite: false }));
  world.add(sparks);
  const flash = new THREE.PointLight(0xffc070, 0, 14); world.add(flash);
  const dust = specks(500, 50, 0x5fbfe0);
  const yCut = yOf(CUTI - 0.5);
  for (const k in PINS) delete PINS[k];
  PINS.cut = () => { const v = new THREE.Vector3(0, yCut, 0); world.localToWorld(v); return v; };
  const CUT = 1.47;
  update = (t) => {
    world.rotation.y = t * 0.55;
    // clamp glides up the helix and locks on the target
    const arrive = sstep(0.0, 1.15, t);
    clamp.position.set(0, lerp(yCut - 9, yCut, arrive), 0);
    clamp.rotation.y = t * 1.6;
    const lock = sstep(1.0, 1.4, t);
    shell.scale.setScalar(1 - 0.18 * lock);
    shell.material.opacity = 0.32 + 0.2 * lock - 0.4 * sstep(CUT + 0.1, CUT + 0.7, t);
    ring.scale.setScalar(1 - 0.3 * lock + 1.2 * sstep(CUT, CUT + 0.5, t)); ring.material.opacity = 1 - sstep(CUT + 0.05, CUT + 0.5, t);
    ring2.position.y = 0.35 * Math.sin(t * 7) * (1 - lock); ring2.scale.setScalar(1 - 0.35 * lock + 1.6 * sstep(CUT, CUT + 0.4, t)); ring2.material.opacity = 1 - sstep(CUT, CUT + 0.4, t);
    // the cut: the two halves drift apart and twist away
    const sep = sstep(CUT, CUT + 0.9, t);
    parts[1].position.y = 1.6 * sep; parts[1].rotation.z = 0.12 * sep; parts[1].position.x = 0.5 * sep;
    parts[0].position.y = -1.2 * sep; parts[0].rotation.z = -0.08 * sep; parts[0].position.x = -0.3 * sep;
    const st = Math.max(0, t - CUT);
    sparks.material.opacity = t < CUT ? 0 : Math.max(0, 1 - st / 0.9);
    for (let i = 0; i < NS; i++) { const v = sv[i]; const k = 1 - Math.exp(-st * 3); sp[i * 3] = v.x * k; sp[i * 3 + 1] = yCut + v.y * k - st * st * 1.2; sp[i * 3 + 2] = v.z * k; }
    sg.attributes.position.needsUpdate = true;
    flash.position.set(0, yCut, 0); flash.intensity = t < CUT ? 2 * lock : 60 * Math.exp(-st * 5) + 2;
    // camera drifts along the helix and settles on the cut
    camera.position.set(lerp(3.5, 1.2, sstep(0, 2.6, t)), lerp(-3.2, 0.4, sstep(0, 2.6, t)) + yCut * 0.6, lerp(15, 11.5, sstep(0, 2.6, t)));
    camera.lookAt(0, yCut * 0.62 - 1.3, 0);
    dust.rotation.y = t * 0.05;
  };
}

// ------------------------------------------------------------------------------------------------ motor
function motor(mode) {
  base("#04070d", 14, 70);
  const world = new THREE.Group(); scene.add(world);  // the track runs along +x, away from the camera
  const R = 1.25, PF = 13, SP = 0.5;
  // microtubule: 13 protofilaments of alternating alpha/beta tubulin
  const XMIN = -40, XMAX = 40, n = Math.floor((XMAX - XMIN) / SP);
  const tubGeo = new THREE.SphereGeometry(0.27, 12, 9);
  const tubMat = new THREE.MeshStandardMaterial({ roughness: 0.5, metalness: 0.05, emissive: new THREE.Color("#0b3a52"), emissiveIntensity: 0.6 });
  const mt = new THREE.InstancedMesh(tubGeo, tubMat, n * PF);
  const m4 = new THREE.Matrix4(), cA = new THREE.Color("#2f7fa6"), cB = new THREE.Color("#58b9dc");
  let k = 0;
  for (let p = 0; p < PF; p++) {
    const a = (p / PF) * Math.PI * 2;
    for (let i = 0; i < n; i++) {
      const x = XMIN + i * SP + (p * 3 * SP) / PF;
      m4.makeTranslation(x, R * Math.cos(a), R * Math.sin(a)); mt.setMatrixAt(k, m4); mt.setColorAt(k, i % 2 ? cA : cB); k++;
    }
  }
  world.add(mt);
  // glow along the track (the "road")
  const lane = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, XMAX - XMIN, 6), new THREE.MeshBasicMaterial({ color: new THREE.Color("#4fd0ff"), transparent: true, opacity: 0.6 }));
  lane.rotation.z = Math.PI / 2; lane.position.y = R + 0.3; world.add(lane);

  // the motor complex
  const cx = new THREE.Group(); world.add(cx);
  const headMat = new THREE.MeshStandardMaterial({ color: new THREE.Color("#d9e6f2"), roughness: 0.35, emissive: new THREE.Color("#6aa8d0"), emissiveIntensity: 0.25 });
  const stalkMat = new THREE.MeshStandardMaterial({ color: new THREE.Color("#bcd2e6"), roughness: 0.4 });
  const heads = [0, 1].map(() => {
    const g = new THREE.Group();
    for (let j = 0; j < 6; j++) { const a = (j / 6) * Math.PI * 2; const s = new THREE.Mesh(new THREE.SphereGeometry(0.34, 16, 12), headMat); s.position.set(0.56 * Math.cos(a), 0.56 * Math.sin(a), 0); g.add(s); }
    const hub = new THREE.Mesh(new THREE.SphereGeometry(0.3, 14, 10), headMat); g.add(hub);
    const stalk = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1, 6), stalkMat); g.add(stalk); g.userData.stalk = stalk;
    const foot = new THREE.Mesh(new THREE.SphereGeometry(0.14, 10, 8), stalkMat); g.add(foot); g.userData.foot = foot;
    cx.add(g); return g;
  });
  const linkMat = new THREE.MeshStandardMaterial({ color: new THREE.Color("#c5d6e6"), roughness: 0.4 });
  const links = [0, 1].map(() => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 1, 8), linkMat); cx.add(m); return m; });
  // dynactin: the Arp1 rod, the p150 arm (made from DCTN1) reaching down to the track
  const rod = new THREE.Group(); cx.add(rod);
  const rodMat = new THREE.MeshStandardMaterial({ color: new THREE.Color("#9ab8d4"), roughness: 0.45, emissive: new THREE.Color("#284a66"), emissiveIntensity: 0.4 });
  for (let j = 0; j < 9; j++) { const s = new THREE.Mesh(new THREE.SphereGeometry(0.26, 12, 9), rodMat); s.position.set(-1.2 + j * 0.3, (j % 2) * 0.16, 0); rod.add(s); }
  const armMat = new THREE.MeshStandardMaterial({ color: AMBER, emissive: AMBER, emissiveIntensity: 1.1, roughness: 0.3 });
  let arm = null; const armTip = new THREE.Mesh(new THREE.SphereGeometry(0.2, 14, 10), armMat); cx.add(armTip);
  const setArm = (pts) => { if (arm) { cx.remove(arm); arm.geometry.dispose(); } arm = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 40, 0.085, 8, false), armMat); cx.add(arm); };
  // cargo: a vesicle full of cholesterol
  const ves = new THREE.Mesh(new THREE.SphereGeometry(1.55, 40, 28), new THREE.MeshStandardMaterial({ color: new THREE.Color("#9fe0ff"), emissive: new THREE.Color("#1e6f8f"),
    emissiveIntensity: 0.5, transparent: true, opacity: 0.28, roughness: 0.15, depthWrite: false }));
  const vesRim = new THREE.Mesh(new THREE.SphereGeometry(1.58, 40, 28), new THREE.MeshBasicMaterial({ color: new THREE.Color("#7fdcff"), wireframe: true, transparent: true, opacity: 0.08 }));
  cx.add(ves, vesRim);
  const cholGeo = new THREE.IcosahedronGeometry(0.17, 1);
  const cholMat = new THREE.MeshStandardMaterial({ color: AMBER, emissive: AMBER, emissiveIntensity: 1.3, roughness: 0.3 });
  const looseMat = new THREE.MeshStandardMaterial({ color: new THREE.Color("#e89a3a"), emissive: AMBER, emissiveIntensity: 0.32, roughness: 0.35 });
  const inside = [];
  for (let j = 0; j < 26; j++) { const m = new THREE.Mesh(cholGeo, cholMat); const u = rnd() * 2 - 1, a = rnd() * 6.283, r = Math.cbrt(rnd()) * 1.15, q = Math.sqrt(1 - u * u);
    m.userData.p = new THREE.Vector3(r * q * Math.cos(a), r * u, r * q * Math.sin(a)); m.userData.ph = rnd() * 6.28; cx.add(m); inside.push(m); }
  const adaptor = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 1, 6), linkMat); cx.add(adaptor);

  // loose cholesterol out on the track (jam / pile / fix)
  const NL = 260, loose = new THREE.InstancedMesh(cholGeo, looseMat, NL); world.add(loose);
  const L = []; for (let j = 0; j < NL; j++) L.push({ x: rnd(), a: rnd() * 6.283, r: rnd(), born: rnd(), ph: rnd() * 6.28, s: 0.7 + rnd() * 0.6 });
  const warn = new THREE.PointLight(0xff4a3a, 0, 9); world.add(warn);
  const dest = new THREE.PointLight(0x4fd0ff, 0, 14); dest.position.set(16, R + 2, 0); world.add(dest);
  const glow = new THREE.PointLight(0xffb547, 2.5, 8); cx.add(glow);
  const dust = specks(700, 60, 0x5fbfe0);

  const wp = (o) => { const v = new THREE.Vector3(); o.getWorldPosition(v); return v; };
  for (const k in PINS) delete PINS[k];
  PINS.head = () => wp(heads[0]); PINS.arm = () => wp(armTip); PINS.cargo = () => wp(ves);
  PINS.heap = () => new THREE.Vector3(-6, R + 2.5, 0); PINS.dest = () => new THREE.Vector3(16, R + 1.5, 0);
  const PER = mode === "fix" ? 0.24 : 0.34, V = mode === "fix" ? 6.0 : 3.4, STEP = V * PER;
  const pose = (t, x0, moving, armOk, wobble) => {
    const hp = [0, 1].map((h) => {
      if (!moving) return { x: x0 + (h ? 0.6 : -0.6), lift: 0 };
      const ph = t / PER + h * 0.5, kk = Math.floor(ph), f = ph - kk, e = sstep(0, 0.5, f);
      return { x: x0 + STEP * (kk + e) + (h ? 0.6 : -0.6), lift: f < 0.5 ? Math.sin(Math.PI * e) * 0.75 : 0 };
    });
    const mx = (hp[0].x + hp[1].x) / 2;
    hp.forEach((p, h) => {
      const g = heads[h]; const hy = R + 2.0 + p.lift * 0.6 + (wobble ? Math.sin(t * 23 + h) * 0.08 : 0);
      g.position.set(p.x, hy, h ? -0.55 : 0.55); g.rotation.set(0.3, h ? 0.5 : -0.5, 0.15 * Math.sin(t * 6 + h));
      const st = g.userData.stalk, ft = g.userData.foot; const footY = R + 0.32 + p.lift;
      const len = hy - footY; st.scale.y = len; st.position.set(0.25, -len / 2, 0); ft.position.set(0.25, -len, 0);
      st.rotation.z = 0; // stalk points straight down in head space (approx.)
      const l = links[h]; const a = new THREE.Vector3(p.x, hy + 0.3, h ? -0.55 : 0.55), b = new THREE.Vector3(mx - 0.1, R + 3.55, 0);
      const d = b.clone().sub(a); l.scale.y = d.length(); l.position.copy(a.clone().add(b).multiplyScalar(0.5)); l.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
    });
    rod.position.set(mx - 0.2, R + 3.75, 0); rod.rotation.z = 0.05 * Math.sin(t * 3);
    // p150 arm from the rod's leading end down to the track ahead of the motor
    const okv = armOk;
    const tip = new THREE.Vector3(mx + 2.4, R + 0.45 + (1 - okv) * 1.4, 0.2 + (1 - okv) * 0.9);
    setArm([new THREE.Vector3(mx + 1.0, R + 3.8, 0), new THREE.Vector3(mx + 1.9, R + 3.3, 0.15), new THREE.Vector3(mx + 2.5, R + 2.0 + (1 - okv) * 0.8, 0.3 + (1 - okv) * 0.6), tip]);
    armTip.position.copy(tip);
    armMat.emissive.copy(AMBER).lerp(new THREE.Color("#ff3b30"), 1 - okv); armMat.color.copy(armMat.emissive); armMat.emissiveIntensity = 0.5 + 0.6 * okv + (1 - okv) * (0.6 + 0.6 * Math.max(0, Math.sin(t * 18)));
    const vy = R + 6.0;
    ves.position.set(mx - 0.4, vy, 0); vesRim.position.copy(ves.position);
    const d = new THREE.Vector3(mx - 0.4, vy - 1.5, 0).sub(new THREE.Vector3(mx - 0.2, R + 3.9, 0));
    adaptor.scale.y = d.length(); adaptor.position.set(mx - 0.3, (vy - 1.5 + R + 3.9) / 2, 0);
    inside.forEach((m) => { m.position.copy(ves.position).add(m.userData.p).add(new THREE.Vector3(0, 0.06 * Math.sin(t * 4 + m.userData.ph), 0)); m.rotation.set(t + m.userData.ph, t * 1.3, 0); });
    glow.position.set(mx - 0.4, vy, 0);
    return mx;
  };
  const setLoose = (fn) => { for (let j = 0; j < NL; j++) { const r = fn(L[j], j); if (!r) { m4.makeScale(0, 0, 0); } else { m4.compose(r.p, new THREE.Quaternion().setFromEuler(new THREE.Euler(r.rot, r.rot * 1.3, 0)), new THREE.Vector3(r.s, r.s, r.s)); } loose.setMatrixAt(j, m4); } loose.instanceMatrix.needsUpdate = true; };

  update = (t) => {
    let mx;
    if (mode === "walk" || mode === "fix") {
      mx = pose(t, -3 + (mode === "fix" ? -2 : 0), true, 1, false);
      if (mode === "fix") setLoose((c, j) => { const x = -30 + c.x * 60; if (j > 120) return null; const p = new THREE.Vector3(x, R + 0.5 + c.r * 0.4, (c.r - 0.5) * 1.6); return { p, rot: t + c.ph, s: c.s * 0.8 }; });
      else setLoose(() => null);
      // low chase camera behind the motor, looking down the track (it recedes to the top of the frame like a road)
      const back = mode === "fix" ? 27 + t * 1.2 : 26.5 - t * 1.4;
      camera.position.set(mx - back, R + 5.2, 1.4 - t * 0.2); camera.lookAt(mx + 6, R + 2.3, -0.4);
      warn.intensity = 0;
    } else if (mode === "jam") {
      const fail = sstep(0.15, 0.6, t);
      const moving = t < 0.2;
      mx = pose(t, 0, moving, 1 - fail, fail > 0.5);
      // cholesterol keeps appearing around the stalled cargo: the cell makes MORE
      setLoose((c, j) => { if (j > 170) return null; const b = 0.5 + c.born * 2.3; if (t < b) return null; const age = t - b; const grow = sstep(0, 0.25, age);
        const p = new THREE.Vector3(mx - 0.4 + (c.x - 0.5) * 6.5, R + 6.0 + (c.r - 0.5) * 5.2, Math.sin(c.a) * 2.6);
        p.y += 0.12 * Math.sin(t * 3 + c.ph); return { p, rot: t * 2 + c.ph, s: c.s * grow * 0.85 }; });
      warn.position.set(mx + 2.4, R + 1.5, 1); warn.intensity = 30 * fail * (0.6 + 0.4 * Math.sin(t * 14));
      camera.position.set(mx - 21.5 + t * 0.9, R + 6, 3.4 - t * 0.4); camera.lookAt(mx + 3, R + 2.6, -0.4);
    } else if (mode === "pile") {
      mx = pose(t, -6, false, 0, true);
      // a heap of cholesterol around the stalled motor; the track beyond is empty
      setLoose((c, j) => { const x = -6 + (c.x - 0.6) * 7 * Math.sqrt(c.r + 0.05); const p = new THREE.Vector3(x, R + 0.6 + c.r * 6.5 * (1 - Math.abs(c.x - 0.6)), Math.sin(c.a) * (1.2 + c.r * 2));
        return { p, rot: t + c.ph, s: c.s }; });
      warn.position.set(-6, R + 3, 2); warn.intensity = 22 + 8 * Math.sin(t * 9);
      // slow dolly from the empty far end back to the heap
      // from behind the heap, the track runs on, empty, to where the cholesterol was meant to go
      camera.position.set(-27 + t * 1.0, R + 7 - t * 0.3, 4.5); camera.lookAt(4, R + 1.5, -1.5);
      dest.intensity = 6 + 2 * Math.sin(t * 4);
    }
    dust.rotation.y = t * 0.04; dust.rotation.x = t * 0.02;
  };
}

window.setup = (name) => {
  seed = 11;
  if (name === "helix") helix(); else motor(name);
  return true;
};
window.frame = (t) => { update(t); composer.render(); return true; };
// screen positions (1080x1920 px) of named points, for pinning HTML labels to the 3D
const PINS = {};
const proj = (v) => { const p = v.clone().project(camera); return [Math.round((p.x + 1) * 540), Math.round((1 - p.y) * 960)]; };
window.project = (t) => { update(t); camera.updateMatrixWorld(); const o = {}; for (const k in PINS) { const v = PINS[k](); if (v) o[k] = proj(v); } return o; };

// BRIDGE — the $6 trillion bet as a viaduct over a chasm: the far cliff needs $6T a year; today's best case
// builds 30% of the span ($1.8T); the $4.2T gap waits for things that barely exist. A bubble pops (Bain doesn't
// call it one); a smartphone and a cloud fly in as new arches. At sunrise, money blows away, the tracks stay.
import { THREE, rng, clamp, prog, ease, ep, lerp, glowPlane, makePoints, textCanvas } from './core.js';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { imgTex, makeSheet, makeLoco, makeCarriage, makeSmoke, certCanvas, noiseTex } from './kit.js';
import HL from './hl.json';

export const SPAN = 4.2, NSPAN = 10, DECK = 10, FAR = -SPAN * NSPAN;
export const BEACON = new THREE.Vector3(0, DECK + 5.5, FAR - 6);

export function makeBridge(env, IMG) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x05060c); scene.fog = new THREE.FogExp2(0x0a0c16, 0.012);
  const hemi = new THREE.HemisphereLight(0xa8b4e0, 0x2a2018, 2.0); scene.add(hemi);
  const sunL = new THREE.DirectionalLight(0xffb070, 0.6); sunL.position.set(-20, 12, -80); scene.add(sunL);
  const key = new THREE.DirectionalLight(0xd0dcff, 4.2); key.position.set(26, 22, 14); scene.add(key);
  const skyU = { uWarm: { value: 0.3 } };
  const sky = new THREE.Mesh(new THREE.SphereGeometry(300, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: `varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform float uWarm; varying vec3 vP; void main(){ float h=clamp(vP.y*1.6+.08,0.,1.);
      vec3 hor=mix(vec3(.46,.32,.46),vec3(1.0,.55,.25),uWarm), top=mix(vec3(.05,.06,.14),vec3(.14,.18,.36),uWarm);
      float sun=pow(max(0.,dot(vP,normalize(vec3(-.25,.08,-1.)))),40.)*uWarm*1.6;
      gl_FragColor=vec4(mix(hor,top,pow(h,.6))+vec3(1.,.7,.4)*sun,1.); }` }));
  scene.add(sky);
  const stars = makePoints(400, 0xdfe8ff, 0.6, 0.7); { const a = stars.geometry.attributes.position.array, s = stars.geometry.attributes.aSize.array; const R = rng(2);
    for (let k = 0; k < 400; k++) { const th = R() * Math.PI * 2, ph = 0.2 + R() * 1.2; a[k * 3] = 250 * Math.cos(th) * Math.cos(ph); a[k * 3 + 1] = 250 * Math.sin(ph); a[k * 3 + 2] = 250 * Math.sin(th) * Math.cos(ph); s[k] = 0.3 + R(); } }
  scene.add(stars);
  // cliffs
  const rock = noiseTex(1024, 1024, '#6e655c', [[2600, 'rgba(15,12,10,A)', 2, 10, 0.15, 0.4], [1400, 'rgba(150,135,120,A)', 1, 6, 0.08, 0.2]], 31, [4, 4]);
  const rockM = new THREE.MeshStandardMaterial({ map: rock, color: 0x8a8076, roughness: 0.95, envMap: env, envMapIntensity: 0.12 });
  const cliff = (z0, z1) => { const g = new THREE.BoxGeometry(80, 60, Math.abs(z1 - z0), 8, 8, 4); const p = g.attributes.position; const r = rng(Math.abs(z0) + 3);
    for (let i = 0; i < p.count; i++) { if (p.getY(i) < 29) { p.setX(i, p.getX(i) + (r() - 0.5) * 1.5); p.setZ(i, p.getZ(i) + (r() - 0.5) * 1.6); } } g.computeVertexNormals();
    const m = new THREE.Mesh(g, rockM); m.position.set(0, DECK - 30.3, (z0 + z1) / 2); scene.add(m); return m; };
  cliff(0.4, 60); cliff(FAR - 0.4, FAR - 120);
  const chasmMist = []; for (let k = 0; k < 6; k++) { const m = glowPlane(40, 0x8aa0d0, 0.18); m.material.blending = THREE.NormalBlending; m.rotation.x = -Math.PI / 2; m.position.set((k % 2 - 0.5) * 10, -8 + k * 1.4, -6 - k * 6); scene.add(m); chasmMist.push(m); }
  // viaduct spans (ExtrudeGeometry along x after rotation)
  const span = new THREE.Shape(); span.moveTo(0, -40); span.lineTo(SPAN, -40); span.lineTo(SPAN, DECK); span.lineTo(0, DECK); span.lineTo(0, -40);
  const hole = new THREE.Path(); hole.moveTo(0.55, -40); hole.lineTo(SPAN - 0.55, -40); hole.lineTo(SPAN - 0.55, DECK - 3.6); hole.absarc(SPAN / 2, DECK - 3.6, SPAN / 2 - 0.55, 0, Math.PI, false); hole.lineTo(0.55, -40); span.holes.push(hole);
  const spanG = new THREE.ExtrudeGeometry(span, { depth: 2.6, bevelEnabled: false, curveSegments: 18 }); spanG.translate(0, 0, -1.3);
  const stoneM = new THREE.MeshStandardMaterial({ map: rock, color: 0xb0a090, roughness: 0.85, envMap: env, envMapIntensity: 0.2, transparent: true });
  const spans = []; const edgeCol = [0xc8ff4d, 0xc8ff4d, 0xc8ff4d, 0x7cc4ff, 0x7cc4ff];
  for (let k = 0; k < NSPAN; k++) { const g = new THREE.Group(); g.position.set(0, 0, -k * SPAN); g.rotation.y = Math.PI / 2; scene.add(g);
    const m = new THREE.Mesh(spanG, k < 3 ? stoneM : stoneM.clone()); g.add(m);
    const deck = new THREE.Mesh(new THREE.BoxGeometry(SPAN, 0.35, 3.0), new THREE.MeshStandardMaterial({ color: 0x5a524a, roughness: 0.8 })); deck.position.set(SPAN / 2, DECK + 0.17, 0); g.add(deck);
    const edge = new THREE.Mesh(new THREE.BoxGeometry(SPAN, 0.06, 3.05), new THREE.MeshBasicMaterial({ color: new THREE.Color(edgeCol[k] || 0xc8ff4d).multiplyScalar(1.15), toneMapped: false, transparent: true, opacity: 0 })); edge.position.set(SPAN / 2, DECK + 0.36, 0); g.add(edge);
    g.userData = { m, edge }; spans.push(g); }
  // ghost arches in the gap (dashed outlines) + "?" marks
  const ghostM = new THREE.LineDashedMaterial({ color: new THREE.Color(0xffb547).multiplyScalar(1.6), dashSize: 0.45, gapSize: 0.3, transparent: true, opacity: 0, toneMapped: false });
  const ghosts = []; for (let k = 3; k < NSPAN; k++) { const pts = span.getPoints(24).map((p) => new THREE.Vector3(0, Math.max(p.y, -6), -k * SPAN - p.x)); const hp = hole.getPoints(24).map((p) => new THREE.Vector3(0, Math.max(p.y, -6), -k * SPAN - p.x));
    for (const arr of [pts, hp]) { const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(arr), ghostM); l.computeLineDistances(); scene.add(l); ghosts.push(l); } }
  const q = textCanvas(256, 256); q.g.font = '900 220px InterV, Inter, sans-serif'; q.g.textAlign = 'center'; q.g.fillStyle = '#ffb547'; q.g.fillText('?', 128, 205); q.tex.needsUpdate = true;
  const qm = []; for (let k = 0; k < 4; k++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 2.2), new THREE.MeshBasicMaterial({ map: q.tex, transparent: true, opacity: 0, depthWrite: false, toneMapped: false })); m.position.set(0, DECK + 1.5 + (k % 2) * 2, -16 - k * 6.4); scene.add(m); qm.push(m); }
  // rails across near cliff + built spans; turn gold at the end
  const railM = new THREE.MeshStandardMaterial({ color: 0x8a9098, metalness: 0.9, roughness: 0.5, envMap: env, envMapIntensity: 0.35 });
  const railLen = 30 + 3 * SPAN; for (const x of [-0.36, 0.36]) { const r = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.1, railLen), railM); r.position.set(x, DECK + 0.42, 30 - railLen / 2); scene.add(r); }
  const goldRail = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xffc861).multiplyScalar(1.4), toneMapped: false, transparent: true, opacity: 0 });
  for (const x of [-0.36, 0.36]) { const r = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.12, railLen + 2 * SPAN), goldRail); r.position.set(x, DECK + 0.45, 30 - (railLen + 2 * SPAN) / 2); scene.add(r); }
  const NSL = 110; const sl = new THREE.InstancedMesh(new THREE.BoxGeometry(1.1, 0.08, 0.16), new THREE.MeshStandardMaterial({ color: 0x2e241a, roughness: 0.9 }), NSL); const M = new THREE.Matrix4();
  for (let k = 0; k < NSL; k++) { M.makeTranslation(0, DECK + 0.38, 30 - k * 0.5); sl.setMatrixAt(k, M); } sl.count = Math.floor((30 + 3 * SPAN) / 0.5); scene.add(sl);
  // far station + beacon ($6T a year needed)
  const beaconPillar = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 1.4, 40, 24, 1, true), new THREE.MeshBasicMaterial({ color: new THREE.Color(0xffc861), transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, toneMapped: false }));
  beaconPillar.position.set(BEACON.x, DECK + 20, BEACON.z); scene.add(beaconPillar);
  const beaconGlow = glowPlane(9, 0xffc861, 0); beaconGlow.position.copy(BEACON); scene.add(beaconGlow);
  const station = new THREE.Mesh(new THREE.BoxGeometry(4, 2, 2), new THREE.MeshStandardMaterial({ color: 0x3a342c, roughness: 0.8 })); station.position.set(-3.6, DECK + 1.0, FAR - 6); scene.add(station);
  const sroof = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, 4.4, 3, 1), new THREE.MeshStandardMaterial({ color: 0x2a2018, roughness: 0.7 })); sroof.rotation.z = Math.PI / 2; sroof.scale.set(1, 1, 0.55); sroof.position.set(-3.6, DECK + 2.4, FAR - 6); scene.add(sroof);
  const winM = new THREE.MeshBasicMaterial({ color: new THREE.Color(1, 0.75, 0.4).multiplyScalar(1.15), toneMapped: false });
  for (let k = 0; k < 4; k++) { const w = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.55), winM); w.position.set(-4.95 + k * 0.9, DECK + 1.1, FAR - 4.98); scene.add(w); }
  // bubble (pops on "bubble")
  const bub = new THREE.Mesh(new THREE.SphereGeometry(2.4, 48, 32), new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: 0, roughness: 0.02, transmission: 1, thickness: 0.05, iridescence: 1, iridescenceIOR: 1.3, envMap: env, envMapIntensity: 1.6, transparent: true, opacity: 0.55, depthWrite: false }));
  bub.position.set(0.5, DECK + 6, -26); scene.add(bub);
  const pop = makePoints(160, 0xe8f2ff, 0.08, 1); scene.add(pop); const R = rng(41); const pp = Array.from({ length: 160 }, () => { const v = new THREE.Vector3(R() - 0.5, R() - 0.5, R() - 0.5).normalize(); return [v, 2.2 + R() * 1.5, 0.5 + R()]; });
  // Bain page 10 (wave of innovation)
  const page = makeSheet(imgTex(IMG.bain10), 3.4, 2651 / 2048, { mc: HL.bain10_mc }, { curl: 0.03, bright: 0.98 });
  const PAGE = new THREE.Vector3(0.4, DECK + 6.3, -21); page.position.copy(PAGE); scene.add(page); page.updateMatrixWorld(true); const pMC = page.userData.local('mc').add(PAGE);
  // smartphone + cloud that become arches 4 and 5
  const phone = new THREE.Group(); scene.add(phone);
  const pb = new THREE.Mesh(new RoundedBoxGeometry(1.5, 3.0, 0.18, 4, 0.22), new THREE.MeshStandardMaterial({ color: 0x15171c, metalness: 0.8, roughness: 0.25, envMap: env, envMapIntensity: 1.2 })); phone.add(pb);
  const scr = textCanvas(300, 600); const sg = scr.g; const gr = sg.createLinearGradient(0, 0, 300, 600); gr.addColorStop(0, '#3a6bd9'); gr.addColorStop(1, '#9a4bd8'); sg.fillStyle = gr; sg.fillRect(0, 0, 300, 600);
  sg.fillStyle = 'rgba(255,255,255,0.85)'; for (let k = 0; k < 12; k++) { const x = 40 + (k % 3) * 85, y = 120 + Math.floor(k / 3) * 95; sg.beginPath(); sg.roundRect(x, y, 56, 56, 14); sg.fill(); } scr.tex.needsUpdate = true;
  const sc = new THREE.Mesh(new THREE.PlaneGeometry(1.32, 2.7), new THREE.MeshBasicMaterial({ map: scr.tex, toneMapped: false })); sc.position.z = 0.1; phone.add(sc);
  const cloud = new THREE.Group(); scene.add(cloud); const cm = new THREE.MeshStandardMaterial({ color: 0xd8e6f6, roughness: 0.7, emissive: 0x2a4a7a, emissiveIntensity: 0.25, envMap: env, envMapIntensity: 0.3 });
  for (const [x, y, r] of [[0, 0, 1.0], [-1.0, -0.3, 0.75], [1.0, -0.25, 0.8], [0.45, 0.45, 0.75], [-0.5, 0.35, 0.65], [0, -0.45, 0.8]]) { const s = new THREE.Mesh(new THREE.SphereGeometry(r, 24, 16), cm); s.position.set(x, y, 0); cloud.add(s); }
  // money blowing into the chasm
  const cert = certCanvas({ value: '£120' }); const bill = textCanvas(400, 180); bill.g.fillStyle = '#2f6b3a'; bill.g.fillRect(0, 0, 400, 180); bill.g.strokeStyle = '#a8d8a0'; bill.g.lineWidth = 6; bill.g.strokeRect(12, 12, 376, 156);
  bill.g.fillStyle = '#d8f0c8'; bill.g.font = '900 120px InterV, Inter, sans-serif'; bill.g.textAlign = 'center'; bill.g.fillText('$', 200, 132); bill.tex.needsUpdate = true;
  const NM = 40; const money = [new THREE.InstancedMesh(new THREE.PlaneGeometry(0.9, 0.6), new THREE.MeshStandardMaterial({ map: cert.tex, side: THREE.DoubleSide, roughness: 0.85 }), NM / 2),
    new THREE.InstancedMesh(new THREE.PlaneGeometry(0.9, 0.4), new THREE.MeshStandardMaterial({ map: bill.tex, side: THREE.DoubleSide, roughness: 0.8 }), NM / 2)];
  money.forEach((m) => { m.frustumCulled = false; scene.add(m); }); const ms = Array.from({ length: NM }, () => [R() * 10 - 2, R() * 4 + DECK + 1, R() * 14 - 8, R() * 6.28, 0.6 + R() * 0.8, R()]);
  // train on the kept tracks at sunrise
  const loco = makeLoco(env, { lamp: 8 }); const c1 = makeCarriage(env), c2 = makeCarriage(env, 0x2c3e2a); const TS = 0.62;
  [loco, c1, c2].forEach((o) => { o.scale.setScalar(TS); o.rotation.y = Math.PI / 2; scene.add(o); });
  const smoke = makeSmoke(120, 0xd8d2cc, 0.5); scene.add(smoke);
  const lampBeam = glowPlane(6, 0xffd090, 0); scene.add(lampBeam);
  const Q = new THREE.Quaternion(), E = new THREE.Euler(), P = new THREE.Vector3(), S = new THREE.Vector3();
  const trainZ = (t) => lerp(18, -5.5, ep(t, 80.2, 84.6, ease.out));

  function update(t) {
    // beacon on the far cliff
    const bOn = ep(t, 60.3, 61.0); beaconPillar.material.opacity = 0.09 * bOn * (0.85 + 0.15 * Math.sin(t * 3)); beaconGlow.material.opacity = 0.45 * bOn;
    // built spans 1-3 rise from the mist on "one point eight trillion"
    spans.forEach((g, k) => { let y = -60, vis = false, edge = 0;
      if (k < 3) { const r = ep(t, 63.45 + k * 0.28, 64.25 + k * 0.28, ease.out); y = lerp(-60, 0, r); vis = r > 0; edge = r * (1 - 0.6 * ep(t, 66, 67)); }
      else if (k < 5) { const tk = k === 3 ? 75.2 : 76.1; const r = ep(t, tk, tk + 0.7, ease.out); y = lerp(-14, 0, r); vis = r > 0; g.userData.m.material.opacity = r; edge = r; }
      g.position.y = y; g.visible = vis; g.userData.edge.material.opacity = edge; });
    // ghost arches + question marks in the gap
    ghostM.opacity = 0.75 * ep(t, 66.6, 67.4) * (1 - 0.5 * ep(t, 75, 76.5)); qm.forEach((m, k) => { const r = ep(t, 67.7 + k * 0.35, 68.2 + k * 0.35, ease.back); m.material.opacity = 0.9 * clamp(r) * (1 - ep(t, 70.2, 70.7)); m.scale.setScalar(Math.max(0.01, r)); m.position.y = DECK + 1.5 + (k % 2) * 2 + Math.sin(t * 2 + k) * 0.25; });
    // bubble floats in, pops on "bubble" (71.6)
    const bIn = ep(t, 69.9, 70.6, ease.out); bub.visible = t > 69.8 && t < 71.62; bub.scale.setScalar(Math.max(0.01, bIn * (1 + 0.03 * Math.sin(t * 5)))); bub.position.y = DECK + 6 + Math.sin(t * 1.5) * 0.3;
    const pa = pop.geometry.attributes.position.array, ps = pop.geometry.attributes.aSize.array; const age = t - 71.62;
    for (let k = 0; k < 160; k++) { const [v, sp, sz] = pp[k]; if (age < 0 || age > 0.9) { ps[k] = 0; continue; } const r = 2.4 + sp * age * 3; pa[k * 3] = bub.position.x + v.x * r; pa[k * 3 + 1] = bub.position.y + v.y * r - age * age * 2; pa[k * 3 + 2] = bub.position.z + v.z * r; ps[k] = sz * (1 - age / 0.9); }
    pop.geometry.attributes.position.needsUpdate = true; pop.geometry.attributes.aSize.needsUpdate = true;
    // page 10
    const pin = ep(t, 71.75, 72.4, ease.out); page.visible = t > 71.7 && t < 75.0; page.userData.u.uFade.value = pin * (1 - ep(t, 74.4, 74.9)); page.position.set(PAGE.x, PAGE.y - (1 - pin) * 3, PAGE.z + (1 - pin) * 2);
    page.rotation.set(-0.08 + (1 - pin) * 0.4, -0.05, 0.02); page.userData.setHL('mc', ep(t, 72.7, 74.2, (k) => k)); page.userData.u.uFocus.value = 0.55 * ep(t, 72.5, 73.0);
    // smartphone + cloud fly in and become arches 4 and 5
    const fly = (o, t0, z) => { const k = ep(t, t0, t0 + 0.8, ease.io); o.visible = t > t0 - 0.05 && t < t0 + 1.05; o.position.set(lerp(9, 0, k), lerp(DECK + 9, DECK - 2.5, k), lerp(4, z, k)); o.rotation.set(0.2 * (1 - k), lerp(-0.8, 0, k) + t * 0.2 * (1 - k), 0.15 * (1 - k));
      o.scale.setScalar(lerp(1.0, 1.6, k) * (1 - ep(t, t0 + 0.75, t0 + 1.05))); };
    fly(phone, 74.6, -3 * SPAN - 2.1); fly(cloud, 75.5, -4 * SPAN - 2.1);
    // sunrise, money blowing away, tracks turning gold, a train on the kept tracks
    skyU.uWarm.value = 0.3 + 0.7 * ep(t, 76.9, 82.0); sunL.intensity = 0.6 + 2.6 * ep(t, 77, 82); hemi.intensity = 0.6 + 0.4 * ep(t, 77, 82);
    goldRail.opacity = ep(t, 81.2, 82.3); spans.slice(0, 5).forEach((g) => { if (t > 81.2) g.userData.edge.material.color.set(0xffc861).multiplyScalar(1.2); });
    for (let j = 0; j < 2; j++) { const im = money[j]; for (let k = 0; k < NM / 2; k++) { const s = ms[j * NM / 2 + k]; const age2 = t - 79.2 - s[5] * 0.6;
      if (age2 < 0) { S.setScalar(0); } else { S.setScalar(1); }
      P.set(s[0] - age2 * 3.2 * s[4], s[1] - age2 * age2 * 1.6 * s[4] + Math.sin(age2 * 3 + s[3]) * 0.3, s[2] - age2 * 2.5);
      E.set(age2 * 3 * s[4] + s[3], age2 * 2 + s[3], age2 * 1.5); Q.setFromEuler(E); M.compose(P, Q, S); im.setMatrixAt(k, M); } im.instanceMatrix.needsUpdate = true; }
    const z = trainZ(t); loco.position.set(0, DECK + 0.36, z); c1.position.set(0, DECK + 0.36, z + 2.9); c2.position.set(0, DECK + 0.36, z + 4.9);
    [loco, c1, c2].forEach((o) => { o.visible = t > 79.8; o.userData.roll((18 - z) / TS); });
    lampBeam.position.set(0, DECK + 1.1, z - 1.6); lampBeam.material.opacity = t > 79.8 ? 0.6 : 0;
    smoke.userData.update(t, (i) => { const te = 79.9 + i * 0.05; if (te > t + 0.01) return null; const r = rng(i * 11 + 4); const zz = trainZ(te);
      return { t0: te, pos: new THREE.Vector3(0, DECK + 0.36 + 2.9 * TS, zz - 1.45 * TS), vel: new THREE.Vector3((r() - 0.5) * 0.4 + 0.5, 0.8 + r() * 0.4, 0.9), size0: 0.3, size1: 1.8, life: 2.6, a: 0.7 }; });
    chasmMist.forEach((m, k) => { m.position.x = (k % 2 - 0.5) * 10 + Math.sin(t * 0.2 + k) * 3; m.material.opacity = 0.14 + 0.05 * Math.sin(t * 0.3 + k); });
  }
  const T = (x, y, z) => [x, y, z];
  const cams = {
    'bridge': [[60.35, T(4, 18, 30), T(0, 10, -30), 44], [61.7, T(2.2, 13.2, 15), T(0, 10.5, -30), 42], [63.4, T(5.5, 14.5, 9), T(0, 9.5, -18), 42],
      [65.1, T(7, 15.5, 11), T(0, 9, -28), 44], [68.0, T(7.5, 16, 6), T(0, 9, -30), 44], [69.9, T(5, 17.5, -6), T(0.5, 15.5, -26), 42],
      [71.7, T(1.5, 16.9, -14), T(0.6, 16.2, -21), 40, 0, 'ease'], [72.6, T(pMC.x, pMC.y + 0.2, -15.0), T(pMC.x, pMC.y + 0.25, -21), 34, 0, 'ease'], [74.2, T(pMC.x + 0.05, pMC.y + 0.2, -15.5), T(pMC.x + 0.05, pMC.y + 0.25, -21), 34, 0, 'ease'],
      [75.0, T(7, 15, 9), T(0, 9.5, -18), 44, 0, 'ease'], [76.6, T(8, 15.5, 7), T(0, 9.5, -20), 44], [78.6, T(10, 20, 18), T(0, 9, -24), 46], [80.4, T(6, 14.5, 13), T(0, 11, -8), 44],
      [82.6, T(4.5, 13.2, 6), T(0, 10.8, -8), 42], [88.8, T(5.5, 14.5, 11), T(0, 10.2, -12), 44]],
  };
  return { scene, update, cams, pts: { beacon: new THREE.Vector3(0, DECK + 1.5, FAR - 3), best: new THREE.Vector3(0, DECK + 0.6, -3 * SPAN), gap: new THREE.Vector3(0, DECK + 1.0, -6.5 * SPAN) } };
}

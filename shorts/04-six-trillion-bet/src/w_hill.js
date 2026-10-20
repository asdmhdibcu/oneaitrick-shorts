// HILL — the share price drawn as a railway track: a train climbs from £50 to £120,
// reaches a station where fares trickle in while expectations pour, then the track breaks off a cliff (crash).
import { THREE, rng, clamp, prog, ease, ep, lerp, glowPlane, makePoints, textCanvas } from './core.js';
import { makeLoco, makeCarriage, makeSmoke, makeCoins, noiseTex, SERIF } from './kit.js';

export const priceY = (p) => (p - 20) * 0.08;   // £20 -> 0, £50 -> 2.4, £120 -> 8.0
const TRACK = [[-11, 50], [-8, 50], [-5, 54], [-2, 66], [1, 84], [4, 104], [6.5, 118], [8.2, 120], [10, 120], [12, 120], [13.6, 120]].map(([x, p]) => new THREE.Vector3(x, priceY(p) + 0.42, 0));

export function makeHill(env) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x060812); scene.fog = new THREE.FogExp2(0x070a16, 0.022);
  scene.add(new THREE.HemisphereLight(0x7f96d8, 0x141008, 0.95));
  const moon = new THREE.DirectionalLight(0xb9cdf8, 2.6); moon.position.set(-8, 14, 10); scene.add(moon);
  // sky dome + stars + moon glow
  const sky = new THREE.Mesh(new THREE.SphereGeometry(140, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false, uniforms: { uRed: { value: 0 } },
    vertexShader: `varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform float uRed; varying vec3 vP; void main(){ float h=clamp(vP.y*1.4+.15,0.,1.); vec3 a=mix(vec3(.34,.24,.40),vec3(.42,.08,.08),uRed), b=vec3(.03,.04,.10); gl_FragColor=vec4(mix(a,b,h),1.); }` }));
  scene.add(sky);
  const stars = makePoints(500, 0xdfe8ff, 0.5, 0.8); const sa = stars.geometry.attributes.position.array; const R = rng(4);
  for (let k = 0; k < 500; k++) { const th = R() * Math.PI * 2, ph = 0.15 + R() * 1.2; sa[k * 3] = 120 * Math.cos(th) * Math.cos(ph); sa[k * 3 + 1] = 120 * Math.sin(ph); sa[k * 3 + 2] = -Math.abs(120 * Math.sin(th) * Math.cos(ph)); stars.geometry.attributes.aSize.array[k] = 0.3 + R() * 0.9; }
  scene.add(stars);
  const mg = glowPlane(30, 0x9fb6ff, 0.35); mg.position.set(-30, 40, -100); scene.add(mg);
  const moonD = new THREE.Mesh(new THREE.CircleGeometry(2.6, 40), new THREE.MeshBasicMaterial({ color: new THREE.Color(0xe8eeff).multiplyScalar(1.3), toneMapped: false, fog: false })); moonD.position.set(-30, 40, -100.5); scene.add(moonD);
  // distant hill silhouettes
  for (let k = 0; k < 3; k++) { const pts = []; const r = rng(30 + k); for (let x = -70; x <= 70; x += 4) pts.push(new THREE.Vector2(x, 2 + k * 2.5 + Math.sin(x * 0.07 + k) * 3 + r() * 1.5)); pts.push(new THREE.Vector2(70, -10), new THREE.Vector2(-70, -10));
    const m = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(pts)), new THREE.MeshBasicMaterial({ color: new THREE.Color().setHSL(0.62, 0.35, 0.05 + k * 0.025) })); m.position.z = -30 - k * 18; scene.add(m); }

  // the hill: silhouette under the track, extruded; vertical cliff at x=14.2
  const curve = new THREE.CatmullRomCurve3(TRACK, false, 'catmullrom', 0.3);
  const hs = new THREE.Shape(); hs.moveTo(-16, -3); hs.lineTo(-16, TRACK[0].y - 0.45);
  for (let i = 0; i <= 80; i++) { const p = curve.getPoint(i / 80); hs.lineTo(p.x, p.y - 0.45); }
  hs.lineTo(14.2, TRACK[TRACK.length - 1].y - 0.45); hs.lineTo(14.6, 5.5); hs.lineTo(14.1, 2.5); hs.lineTo(14.7, -0.5); hs.lineTo(14.5, -3); hs.lineTo(-16, -3);
  const grass = noiseTex(1024, 1024, '#3e5634', [[3000, 'rgba(10,16,8,A)', 1, 6, 0.2, 0.5], [1200, 'rgba(70,90,50,A)', 1, 3, 0.1, 0.3]], 12, [6, 6]);
  const hillG = new THREE.ExtrudeGeometry(hs, { depth: 9, bevelEnabled: true, bevelThickness: 0.6, bevelSize: 0.5, bevelSegments: 3, steps: 1, curveSegments: 4 });
  const hill = new THREE.Mesh(hillG, new THREE.MeshStandardMaterial({ map: grass, color: 0xb8c8a8, roughness: 0.95, envMap: env, envMapIntensity: 0.25 })); hill.position.z = -6.5; scene.add(hill);
  const valley = new THREE.Mesh(new THREE.PlaneGeometry(80, 40), new THREE.MeshStandardMaterial({ color: 0x0d1410, roughness: 1 })); valley.rotation.x = -Math.PI / 2; valley.position.set(30, -0.6, -6); scene.add(valley);

  // rails + sleepers along the curve
  const railM = new THREE.MeshStandardMaterial({ color: 0x6a7078, metalness: 0.9, roughness: 0.5, envMap: env, envMapIntensity: 0.35 });
  const offsetCurve = (dz, dy = 0) => new THREE.CatmullRomCurve3(TRACK.map((p) => p.clone().add(new THREE.Vector3(0, dy, dz))), false, 'catmullrom', 0.3);
  for (const dz of [-0.36, 0.36]) scene.add(new THREE.Mesh(new THREE.TubeGeometry(offsetCurve(dz, 0.1), 300, 0.045, 6), railM));
  const NS = 120; const sl = new THREE.InstancedMesh(new THREE.BoxGeometry(0.14, 0.08, 1.05), new THREE.MeshStandardMaterial({ color: 0x3a2a1c, roughness: 0.9 }), NS); scene.add(sl);
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), S1 = new THREE.Vector3(1, 1, 1), X = new THREE.Vector3(1, 0, 0);
  for (let k = 0; k < NS; k++) { const u = k / (NS - 1); const p = curve.getPointAt(u), tg = curve.getTangentAt(u); Q.setFromUnitVectors(X, tg); M.compose(p.clone().add(new THREE.Vector3(0, 0.02, 0)), Q, S1); sl.setMatrixAt(k, M); }
  // the chart line: glowing lime trace above the track that follows the train; red plunge at the crash
  const trace = new THREE.Mesh(new THREE.TubeGeometry(offsetCurve(0.5, 1.15), 400, 0.075, 8), new THREE.MeshBasicMaterial({ color: new THREE.Color(0xc8ff4d).multiplyScalar(1.3), toneMapped: false, transparent: true, opacity: 0.9 }));
  scene.add(trace); const TI = trace.geometry.index.count;
  const plunge = new THREE.CatmullRomCurve3([new THREE.Vector3(13.6, priceY(120) + 1.57, 0.5), new THREE.Vector3(15.4, priceY(112) + 1.2, 0.5), new THREE.Vector3(16.5, priceY(64), 0.5), new THREE.Vector3(17.5, priceY(28), 0.5), new THREE.Vector3(19.6, priceY(20) + 0.4, 0.5)]);
  const pl = new THREE.Mesh(new THREE.TubeGeometry(plunge, 120, 0.07, 6), new THREE.MeshBasicMaterial({ color: new THREE.Color(0xff4a4a).multiplyScalar(2.6), toneMapped: false })); scene.add(pl); const PI = pl.geometry.index.count;
  // price gridlines + labels
  const lab = (txt, col, x, y, z, s = 1) => { const c = textCanvas(512, 160); c.g.font = `900 120px InterV, Inter, sans-serif`; c.g.fillStyle = col; c.g.textAlign = 'left'; c.g.fillText(txt, 10, 125); c.tex.needsUpdate = true;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(1.6 * s, 0.5 * s), new THREE.MeshBasicMaterial({ map: c.tex, transparent: true, depthWrite: false, toneMapped: false, opacity: 0 })); m.position.set(x, y, z); scene.add(m); return m; };
  const gridM = new THREE.LineDashedMaterial({ color: 0x8aa0c8, dashSize: 0.3, gapSize: 0.25, transparent: true, opacity: 0.35 });
  const gline = (y) => { const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-14, y, -1.2), new THREE.Vector3(22, y, -1.2)]); const l = new THREE.Line(g, gridM); l.computeLineDistances(); scene.add(l); };
  gline(priceY(50) + 0.42); gline(priceY(120) + 0.42); gline(priceY(20) + 0.42);
  const L50 = lab('£50', '#e8e0d0', -9.6, priceY(50) + 1.0, -1.1), L120 = lab('£120', '#c8ff4d', 4.2, priceY(120) + 1.25, -1.1, 1.1), L20 = lab('£20', '#ff6b6b', 17.9, priceY(20) + 1.1, 0.4, 1.1);

  // the train
  const loco = makeLoco(env, { lamp: 7 }); const car = makeCarriage(env); const car2 = makeCarriage(env, 0x2c3e2a);
  const TS = 0.42; [loco, car, car2].forEach((o) => { o.scale.setScalar(TS); scene.add(o); });
  const smoke = makeSmoke(160, 0xc9ccd6, 0.5); scene.add(smoke);
  const along = (u) => ({ p: curve.getPointAt(clamp(u, 0, 1)), tg: curve.getTangentAt(clamp(u, 0.0001, 0.9999)) });
  const LEN = curve.getLength();
  const posU = (t) => { // train front position along the curve (0..1)
    if (t < 25) return lerp(0.08, 0.78, ep(t, 15.4, 20.3, (k) => k < 0.85 ? ease.io(k / 0.85) * 0.92 : 0.92 + (k - 0.85) / 0.15 * 0.08));
    if (t < 32.4) return lerp(0.80, 0.9, ep(t, 29.9, 31.6, ease.out));
    return lerp(0.9, 0.985, ep(t, 32.35, 33.0, ease.in));
  };
  const place = (o, u, tilt = 0) => { const a = along(u); o.position.copy(a.p).add(new THREE.Vector3(0, 0.02, 0)); Q.setFromUnitVectors(X, a.tg); o.quaternion.copy(Q); if (tilt) o.rotateZ(-tilt); };

  // station + jars (fares vs expectations)
  const st = new THREE.Group(); st.position.set(11.4, priceY(120) + 0.45, -1.6); scene.add(st);
  const plat = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.3, 1.0), new THREE.MeshStandardMaterial({ color: 0x5a5048, roughness: 0.9 })); plat.position.y = 0.15; st.add(plat);
  const lampP = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.05, 2.2, 8), new THREE.MeshStandardMaterial({ color: 0x1a1a1e, metalness: 0.7, roughness: 0.4 })); lampP.position.set(-1.4, 1.4, 0); st.add(lampP);
  const lampG = glowPlane(1.3, 0xffc070, 0.9); lampG.position.set(-1.4, 2.55, 0.05); st.add(lampG); const lampL = new THREE.PointLight(0xffb060, 6, 7, 2); lampL.position.set(-1.4, 2.5, 0.4); st.add(lampL);
  const glassM = new THREE.MeshPhysicalMaterial({ color: 0xcfe3ff, metalness: 0, roughness: 0.05, transmission: 0.9, thickness: 0.2, transparent: true, opacity: 0.35, envMap: env, envMapIntensity: 1.2, side: THREE.DoubleSide, depthWrite: false });
  const jarExp = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.9, 32, 1, true), new THREE.MeshBasicMaterial({ color: new THREE.Color(0xffb547).multiplyScalar(1.4), wireframe: true, transparent: true, opacity: 0.5, toneMapped: false })); jarExp.position.set(-0.4, 1.25, 0.1); st.add(jarExp);
  const jarFare = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.9, 32, 1, true), glassM); jarFare.position.set(0.75, 1.25, 0.1); st.add(jarFare);
  const fillExp = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 1, 32), new THREE.MeshBasicMaterial({ color: new THREE.Color(0xffb547).multiplyScalar(0.9), transparent: true, opacity: 0.35, toneMapped: false })); fillExp.position.set(-0.4, 0.3, 0.1); st.add(fillExp);
  const coins = makeCoins(26, env); st.add(coins);
  const lExp = lab('EXPECTED', '#ffb547', -0.4 - 0.2, 2.45, 0.15, 0.6), lFare = lab('FARES', '#e8e0d0', 0.75 + 0.18, 2.45, 0.15, 0.6); st.add(lExp, lFare);
  // the broken bridge section beyond the cliff (falls on "CRASHED")
  const br = new THREE.Group(); br.position.set(14.2, priceY(120) + 0.45, 0); scene.add(br);
  for (const dz of [-0.36, 0.36]) { const r = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.09, 0.09), railM); r.position.set(1.7, 0.08, dz); br.add(r); }
  for (let k = 0; k < 12; k++) { const s = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.08, 1.05), sl.material); s.position.set(0.15 + k * 0.28, 0, 0); br.add(s); }
  const truss = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.35, 0.9), new THREE.MeshStandardMaterial({ color: 0x2a2018, roughness: 0.8 })); truss.position.set(1.7, -0.25, 0); br.add(truss);
  const sparks = makePoints(160, 0xffb070, 0.07, 1); scene.add(sparks); const sp = Array.from({ length: 160 }, () => [R() - 0.5, R(), R() - 0.5, 0.5 + R()]);
  const redLight = new THREE.PointLight(0xff3030, 0, 30, 1.5); redLight.position.set(15, 6, 4); scene.add(redLight);
  const CM = new THREE.Matrix4(), CQ = new THREE.Quaternion(), CE = new THREE.Euler();

  function update(t) {
    const u = posU(t); const gap = 0.042;
    const crashK = ep(t, 32.84, 33.7, ease.in); const tip = t > 32.9 ? 0.22 * ep(t, 32.9, 33.5, ease.out) : 0;
    place(loco, u, tip); place(car, u - gap * 1.25); place(car2, u - gap * 2.3);
    const dist = u * LEN; loco.userData.roll(dist / TS); car.userData.roll(dist / TS); car2.userData.roll(dist / TS);
    // smoke from the chimney, emitted along the path
    smoke.userData.update(t, (i) => { const te = (t < 25 ? 15.3 : 29.8) + i * 0.035; if (te > t + 0.01 || te < t - 2.2) return null; const ue = posU(te); const a = along(ue); const r = rng(i * 13 + 1);
      const top = new THREE.Vector3(1.45, 2.9, 0).multiplyScalar(TS); Q.setFromUnitVectors(X, a.tg); top.applyQuaternion(Q).add(a.p);
      return { t0: te, pos: top, vel: new THREE.Vector3(-0.6 - r() * 0.4, 0.7 + r() * 0.5, (r() - 0.5) * 0.3), size0: 0.25, size1: 1.4, life: 2.0, a: 0.8 }; });
    // chart trace grows with the train (price so far)
    trace.geometry.setDrawRange(0, Math.floor(TI * clamp(u + 0.01) / 3) * 3);
    trace.material.color.set(t > 32.84 ? 0xff6b6b : 0xc8ff4d).multiplyScalar(1.3);
    pl.geometry.setDrawRange(0, Math.floor(PI * ep(t, 32.84, 33.55, ease.in) / 3) * 3);
    L50.material.opacity = ep(t, 15.7, 16.3) * (t < 26 ? 1 : 0.5); L120.material.opacity = ep(t, 18.5, 19.0); L20.material.opacity = ep(t, 33.3, 33.8);
    sky.material.uniforms.uRed.value = ep(t, 32.84, 33.4);
    redLight.intensity = 60 * ep(t, 32.84, 33.2) * (0.8 + 0.2 * Math.sin(t * 20));
    // jars: expectations pour, fares trickle
    const fe = ep(t, 30.15, 31.9, ease.out); fillExp.scale.y = 0.02 + fe * 1.7; fillExp.position.y = 0.3 + fillExp.scale.y / 2;
    lExp.material.opacity = ep(t, 30.0, 30.4) * (t < 32.9 ? 1 : 0.3); lFare.material.opacity = lExp.material.opacity;
    for (let k = 0; k < 26; k++) { const tk = 30.3 + k * 0.42; const k2 = clamp((t - tk) / 0.55); const landed = k < 4 ? k * 0.05 : 0;
      CE.set(k * 1.3, 0, k * 0.7 * (1 - k2)); CQ.setFromEuler(CE);
      const y = k2 < 1 ? lerp(3.2, 0.36 + landed, ease.in(k2)) : 0.36 + landed; const vis = t > tk && k < 4 ? 1 : 0;
      CM.compose(new THREE.Vector3(0.75 + Math.sin(k * 2.1) * 0.15, y, 0.1 + Math.cos(k * 1.7) * 0.15), CQ, new THREE.Vector3(vis, vis, vis)); coins.setMatrixAt(k, CM); }
    coins.instanceMatrix.needsUpdate = true;
    // bridge breaks and falls
    br.rotation.z = -1.25 * crashK; br.position.y = priceY(120) + 0.45 - 7 * crashK * crashK;
    const sa2 = sparks.geometry.attributes.position.array, ss = sparks.geometry.attributes.aSize.array; const age = t - 32.84;
    for (let k = 0; k < 160; k++) { const s = sp[k]; if (age < 0 || age > 1.6) { ss[k] = 0; continue; } ss[k] = s[3] * (1 - age / 1.6);
      sa2[k * 3] = 14.2 + s[0] * age * 4; sa2[k * 3 + 1] = priceY(120) + 0.5 + s[1] * age * 3 - 4 * age * age; sa2[k * 3 + 2] = s[2] * age * 4; }
    sparks.geometry.attributes.position.needsUpdate = true; sparks.geometry.attributes.aSize.needsUpdate = true;
  }
  const T = (x, y, z) => [x, y, z];
  const at = (u) => curve.getPointAt(clamp(u, 0, 1));
  const follow = (tt, off, look) => { const p = at(posU(tt)); return [tt, T(p.x + off[0], p.y + off[1], p.z + off[2]), T(p.x + look[0], p.y + look[1], 0), 40]; };
  const cams = {
    'hill-a': [15.55, 16.6, 17.7, 18.8, 19.8, 20.45].map((tt) => follow(tt, [1.2, 1.4, 11.5], [1.0, 1.3])),
    'hill-b': [[30.0, T(8.0, 10.9, 10.4), T(10.2, 9.6, -0.8), 40], [31.9, T(9.2, 10.6, 10.2), T(11.2, 9.4, -0.6), 40, 0, 'ease'], [32.7, T(11.4, 10.8, 11.5), T(12.6, 10.5, 0), 42, 0, 'ease'], [33.3, T(13.8, 9.6, 13.0), T(15.0, 8.4, 0), 44, 0, 'ease'], [34.15, T(15.4, 7.0, 15.0), T(16.4, 4.8, 0), 46, 0, 'ease']],
  };
  return { scene, update, cams, curveAt: at };
}

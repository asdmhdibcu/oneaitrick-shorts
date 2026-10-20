// PAINTING — Turner's "Rain, Steam and Speed" (1844) as a 2.5D plate in the rain;
// a 3D locomotive bursts out of it on "EVERYTHING".
import { THREE, rng, clamp, prog, ease, ep, lerp, glowPlane, radialTex } from './core.js';
import { imgTex, photoPlate, makeLoco, makeSmoke } from './kit.js';

export const PAINT_W = 8, PAINT_H = 8 * 1433 / 1920;
const TRAIN = new THREE.Vector3((0.661 - 0.5) * PAINT_W, (0.262 - 0.5) * PAINT_H, 0.42);

export function makePaint(env, IMG) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x0d0b08);
  scene.add(new THREE.HemisphereLight(0xfff0d8, 0x2a2016, 0.9));
  const key = new THREE.DirectionalLight(0xffe2b8, 2.2); key.position.set(-3, 6, 8); scene.add(key);
  // depth: sky far, the viaduct diagonal (u .5->1, v .55->0) near, bottom nearer than top
  const depth = (u, v) => {
    let z = -0.9 * Math.max(0, v - 0.5) / 0.5 + 0.25 * (1 - v);
    const ax = 0.5, ay = 0.56, bx = 1.0, by = 0.0; const dx = bx - ax, dy = by - ay; const tt = clamp(((u - ax) * dx + (v - ay) * dy) / (dx * dx + dy * dy));
    const d = Math.hypot(u - (ax + dx * tt), v - (ay + dy * tt)); z += 0.55 * Math.max(0, 1 - d / 0.2) * (0.4 + 0.6 * tt);
    z += 0.12 * Math.max(0, 1 - Math.hypot((u - 0.66) / 0.05, (v - 0.27) / 0.08)); // the train itself
    return z;
  };
  const plate = photoPlate(imgTex(IMG.turner), PAINT_W, PAINT_H, depth, [120, 90]); scene.add(plate);
  const PU = plate.userData.u; PU.uVig.value = 0.2;
  const gilt = new THREE.MeshStandardMaterial({ color: 0xc89a3e, metalness: 1, roughness: 0.32, envMap: env, envMapIntensity: 1.2 });
  for (const [x, y, w, h] of [[0, PAINT_H / 2 + 0.22, PAINT_W + 0.88, 0.44], [0, -PAINT_H / 2 - 0.22, PAINT_W + 0.88, 0.44], [-PAINT_W / 2 - 0.22, 0, 0.44, PAINT_H], [PAINT_W / 2 + 0.22, 0, 0.44, PAINT_H]]) {
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.32), gilt); b.position.set(x, y, 0.05); scene.add(b); }
  const wallP = new THREE.Mesh(new THREE.PlaneGeometry(60, 40), new THREE.MeshStandardMaterial({ color: 0x241a14, roughness: 0.95 })); wallP.position.z = -0.6; scene.add(wallP);
  const pspot = new THREE.SpotLight(0xffe0b0, 160, 40, 0.5, 0.6, 1.4); pspot.position.set(0, 8, 14); pspot.target.position.set(0, 0, 0); scene.add(pspot, pspot.target);
  // rain streaks in front of the canvas
  const NR = 420; const rg = new THREE.BufferGeometry(); const rp = new Float32Array(NR * 6); rg.setAttribute('position', new THREE.BufferAttribute(rp, 3));
  const rain = new THREE.LineSegments(rg, new THREE.LineBasicMaterial({ color: 0xe8e2d4, transparent: true, opacity: 0.22, depthWrite: false })); rain.frustumCulled = false; scene.add(rain);
  const R = rng(5); const rs = Array.from({ length: NR }, () => [R() * 9 - 4.5, R() * 7, R() * 6.5 + 0.6, 0.7 + R() * 0.6]);
  // drifting mist
  const mists = []; for (let k = 0; k < 4; k++) { const m = glowPlane(5 + k, 0xf2e6cf, 0.0, radialTex('rgba(255,255,255,0.9)', 'rgba(255,255,255,0)')); m.material.blending = THREE.NormalBlending; m.position.set(-2 + k * 1.5, -1 + (k % 2) * 1.2, 0.9 + k * 0.4); scene.add(m); mists.push(m); }
  // the locomotive that comes out of the painting
  const loco = makeLoco(env, { lamp: 9, body: 0x22201c }); loco.rotation.y = -Math.PI / 2 + 0.85; scene.add(loco);
  const smoke = makeSmoke(140, 0xe6ddcf, 0.6); scene.add(smoke);
  const flare = glowPlane(3.2, 0xffb070, 0); scene.add(flare);
  const path = (t) => { // 0 = in the painting, 1 = right in front of the lens
    const k = ep(t, 7.5, 9.55, (x) => x * x * (3 - 2 * x) * 0.6 + x * x * 0.4);
    return { k, pos: new THREE.Vector3(lerp(TRAIN.x, 0.6, k), lerp(TRAIN.y - 0.08, -2.35, k), lerp(TRAIN.z, 4.6, k)), s: lerp(0.06, 0.95, k) };
  };
  function update(t) {
    const p = path(t); loco.position.copy(p.pos); loco.scale.setScalar(p.s); loco.visible = t > 7.35;
    loco.userData.roll(t * 6 * p.s + p.k * 9);
    loco.traverse((o) => { if (o.material && o.material.opacity !== undefined && o !== loco.userData.glow) { o.material.transparent = true; o.material.opacity = clamp(prog(t, 7.35, 7.9)); } });
    PU.uBright.value = lerp(0.9, 0.62, ep(t, 8.2, 9.5)); PU.uWarm.value = 0.15 + 0.2 * ep(t, 8.6, 9.6);
    // smoke: puffs from the chimney, emitted over time
    smoke.userData.update(t, (i) => { const te = 7.4 + i * 0.022; if (te > 10.4) return null; const q = path(te); const c = new THREE.Vector3(1.45, 2.9, 0).multiplyScalar(q.s).applyAxisAngle(new THREE.Vector3(0, 1, 0), loco.rotation.y).add(q.pos);
      const r = rng(i * 7 + 3); return { t0: te, pos: c, vel: new THREE.Vector3((r() - 0.5) * 0.5 - 0.25, 0.9 + r() * 0.6, (r() - 0.5) * 0.3), size0: 0.25 * q.s + 0.05, size1: 1.6 * q.s + 0.5, life: 1.4 + r() * 0.8, a: 0.9 }; });
    flare.position.copy(p.pos).add(new THREE.Vector3(0.0, 1.2 * p.s, 0.9 * p.s)); flare.material.opacity = 0.55 * ep(t, 8.6, 9.4) * (0.75 + 0.25 * Math.sin(t * 40)); flare.scale.setScalar(0.4 + p.k * 0.9);
    // rain
    for (let k = 0; k < NR; k++) { const s = rs[k]; const y = 3.5 - ((s[1] + t * 7 * s[3]) % 7); const x = s[0] + (3.5 - y) * 0.25;
      rp[k * 6] = x; rp[k * 6 + 1] = y; rp[k * 6 + 2] = s[2]; rp[k * 6 + 3] = x + 0.05; rp[k * 6 + 4] = y - 0.22; rp[k * 6 + 5] = s[2]; }
    rg.attributes.position.needsUpdate = true;
    mists.forEach((m, k) => { m.position.x = -2.5 + k * 1.5 + Math.sin(t * 0.25 + k) * 0.6 + t * 0.06; m.material.opacity = 0.12 + 0.05 * Math.sin(t * 0.4 + k * 2); });
  }
  const T = (x, y, z) => [x, y, z];
  const cams = {
    'paint': [[4.95, T(0.3, -0.45, 24), T(0.3, -0.5, 0), 40], [6.1, T(0.45, -0.6, 21), T(0.5, -0.65, 0), 40], [7.7, T(1.15, -1.25, 10.5), T(1.2, -1.35, 0), 40],
      [9.3, T(1.3, -1.1, 11.6), T(1.0, -1.25, 0), 44], [10.45, T(1.4, -1.0, 12.2), T(1.0, -1.2, 0), 46]],
  };
  return { scene, update, cams };
}

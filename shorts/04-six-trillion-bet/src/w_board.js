// BOARD — the 1845 Punch cartoon and Odlyzko's paper pinned to a board; red string from Darwin's
// and Charlotte's portraits to their names, highlighted in the paper. Share certificates rain down.
import { THREE, rng, clamp, prog, ease, ep, lerp, glowPlane } from './core.js';
import { imgTex, makeSheet, certCanvas, noiseTex } from './kit.js';
import HL from './hl.json';

export function makeBoard(env, IMG) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x0b0806); scene.fog = new THREE.FogExp2(0x0b0806, 0.03);
  scene.add(new THREE.HemisphereLight(0x9a8a78, 0x140e0a, 0.5));
  const spot = new THREE.SpotLight(0xffdcae, 45, 30, 0.8, 0.7, 1.4); spot.position.set(0.5, 6, 7); spot.target.position.set(0.3, 0.6, 0); scene.add(spot, spot.target);
  const cork = noiseTex(1024, 1024, '#5b3f26', [[2500, 'rgba(25,14,6,A)', 1, 5, 0.15, 0.35], [1500, 'rgba(190,140,90,A)', 1, 4, 0.1, 0.25]], 9, [4, 3]);
  const board = new THREE.Mesh(new THREE.PlaneGeometry(14, 10), new THREE.MeshStandardMaterial({ map: cork, color: 0x9a7a5a, roughness: 0.95, envMap: env, envMapIntensity: 0.1 })); board.position.set(0.5, 0.5, -0.02); scene.add(board);
  const frameM = new THREE.MeshStandardMaterial({ color: 0x2a1a0e, roughness: 0.55, envMap: env, envMapIntensity: 0.4 });
  for (const [x, y, w, h] of [[0.5, 5.5, 14.4, 0.4], [0.5, -4.5, 14.4, 0.4], [-6.5, 0.5, 0.4, 10.4], [7.5, 0.5, 0.4, 10.4]]) { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.25), frameM); b.position.set(x, y, 0.05); scene.add(b); }
  const pinM = new THREE.MeshStandardMaterial({ color: 0xc0262a, roughness: 0.35, metalness: 0.2, envMap: env, envMapIntensity: 0.8 });
  const pin = (x, y, z) => { const p = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 12), pinM); p.position.set(x, y, z + 0.06); scene.add(p); return p; };
  const shadow = (w, h, x, y, z, rz) => { const s = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: 0, transparent: true, opacity: 0.45, depthWrite: false })); s.position.set(x + 0.08, y - 0.1, z - 0.01); s.rotation.z = rz; scene.add(s); };
  const paper = (tex, w, h, x, y, z, rz, border = 0.08) => {
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.z = rz; scene.add(g);
    const bg = new THREE.Mesh(new THREE.PlaneGeometry(w + border * 2, h + border * 2), new THREE.MeshStandardMaterial({ color: 0xf0e8d8, roughness: 0.9 })); g.add(bg);
    const im = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.85, envMap: env, envMapIntensity: 0.15 })); im.position.z = 0.003; g.add(im);
    shadow(w + border * 2, h + border * 2, x, y, z, rz); return g; };
  // Punch cartoon (left), Darwin + Charlotte portraits (top), Odlyzko page 1 (right)
  const punch = paper(imgTex(IMG.punch), 3.7, 3.7 * 787 / 1000, -2.25, 0.85, 0.06, 0.035); pin(-2.25 - 1.7, 0.85 + 1.4, 0.06); pin(-2.25 + 1.75, 0.85 + 1.5, 0.06);
  const dar = paper(imgTex(IMG.darwin), 0.95, 0.95 * 720 / 468, 3.35, 2.35, 0.1, -0.06, 0.06); pin(3.35, 2.35 + 0.78, 0.1);
  const cha = paper(imgTex(IMG.charlotte), 0.95, 0.95 * 1144 / 800, 0.45, 2.55, 0.1, 0.05, 0.06); pin(0.45, 2.55 + 0.72, 0.1);
  const page = makeSheet(imgTex(IMG.odl1), 3.4, 2651 / 2048, { darwin: HL.odl1_darwin, bronte: HL.odl1_bronte }, { curl: 0.02, bright: 0.98 });
  page.position.set(1.95, -0.55, 0.09); page.rotation.z = -0.025; scene.add(page); shadow(3.4, 3.4 * 2651 / 2048, 1.95, -0.55, 0.09, -0.025);
  pin(1.95 - 1.5, -0.55 + 2.1, 0.09); pin(1.95 + 1.5, -0.55 + 2.12, 0.09);
  page.updateMatrixWorld(true);
  const darW = page.userData.local('darwin').applyMatrix4(page.matrixWorld), broW = page.userData.local('bronte').applyMatrix4(page.matrixWorld);
  // red string with sag, revealed progressively
  const strM = new THREE.MeshStandardMaterial({ color: 0xd8262c, roughness: 0.5, emissive: 0x3a0000 });
  const string = (a, b) => { const mid = a.clone().add(b).multiplyScalar(0.5); mid.y -= 0.35; mid.z += 0.25;
    const curve = new THREE.QuadraticBezierCurve3(a, mid, b); const g = new THREE.TubeGeometry(curve, 60, 0.014, 6); const m = new THREE.Mesh(g, strM); scene.add(m); return m; };
  const s1 = string(new THREE.Vector3(3.35, 2.35 - 0.6, 0.16), darW.clone().setZ(0.16)); s1.geometry.setDrawRange(0, 0);
  const s2 = string(new THREE.Vector3(0.45, 2.55 - 0.66, 0.16), broW.clone().setZ(0.16)); s2.geometry.setDrawRange(0, 0);
  const NI1 = s1.geometry.index.count, NI2 = s2.geometry.index.count;
  // falling share certificates (foreground)
  const cert = certCanvas({ value: '£50' });
  const N = 26; const cm = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.62, 0.41), new THREE.MeshStandardMaterial({ map: cert.tex, roughness: 0.85, side: THREE.DoubleSide, envMap: env, envMapIntensity: 0.2 }), N);
  cm.frustumCulled = false; scene.add(cm); const R = rng(21); const cs = Array.from({ length: N }, () => [R() * 9 - 4, R() * 6, 1.2 + R() * 3.2, R() * 6.28, 0.6 + R() * 0.6, R()]);
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), E = new THREE.Euler(), S = new THREE.Vector3(1, 1, 1), Pp = new THREE.Vector3();
  function update(t) {
    page.userData.setHL('darwin', ep(t, 12.45, 12.95, ease.out)); page.userData.setHL('bronte', ep(t, 14.35, 15.05, ease.out));
    page.userData.u.uFocus.value = 0.55 * ep(t, 12.2, 12.7);
    s1.geometry.setDrawRange(0, Math.floor(NI1 * ep(t, 12.55, 13.3) / 3) * 3); s2.geometry.setDrawRange(0, Math.floor(NI2 * ep(t, 14.45, 15.2) / 3) * 3);
    for (let k = 0; k < N; k++) { const c = cs[k]; const fall = ((c[1] - (t - 10) * 0.8 * c[4]) % 6 + 6) % 6 - 2.4;
      Pp.set(c[0] + Math.sin(t * 1.4 * c[4] + c[3]) * 0.4 + 0.5, fall + 0.5, c[2]); E.set(Math.sin(t * 2 * c[4] + c[3]) * 0.9, Math.cos(t * 1.7 * c[4] + c[3]) * 0.8, t * 0.6 * (c[5] - 0.5) + c[3]); Q.setFromEuler(E);
      M.compose(Pp, Q, S.setScalar(ep(t, 10.0, 10.6) * (0.85 + c[5] * 0.3))); cm.setMatrixAt(k, M); }
    cm.instanceMatrix.needsUpdate = true;
  }
  const T = (x, y, z) => [x, y, z];
  const dz = (v, dx = 0, dy = 0, d = 3.6) => T(v.x + dx, v.y + dy, v.z + d);
  const cams = {
    'board': [[10.0, T(-2.5, 0.6, 5.6), T(-2.3, 0.75, 0), 38], [11.6, T(-1.4, 0.8, 5.4), T(-1.6, 0.9, 0), 38],
      [12.25, dz(darW, 0.05, 0.1, 4.6), T(darW.x + 0.05, darW.y + 0.12, 0), 36], [13.5, dz(darW, 0.25, 0.12, 4.8), T(darW.x + 0.25, darW.y + 0.14, 0), 36],
      [14.3, dz(broW, -0.1, 0.12, 4.6), T(broW.x - 0.1, broW.y + 0.14, 0), 36], [15.85, dz(broW, -0.15, 0.14, 4.0), T(broW.x - 0.15, broW.y + 0.16, 0), 36]],
  };
  return { scene, update, cams };
}

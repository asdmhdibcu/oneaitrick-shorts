// PHOTO — 2.5D photo plates with live steam (locomotive wheel; steam train on a viaduct)
// and a desk where Odlyzko's page 25 gets highlighted ("almost all lines continued in service").
import { THREE, rng, clamp, prog, ease, ep, lerp, glowPlane, makePoints } from './core.js';
import { imgTex, photoPlate, makeSmoke, makeSheet, noiseTex } from './kit.js';
import HL from './hl.json';

export const WHEEL = new THREE.Vector3(0, 0, 0), VIA = new THREE.Vector3(60, 0, 0), DESK = new THREE.Vector3(120, 0, 0);

export function makePhoto(env, IMG) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x07070a);
  scene.add(new THREE.HemisphereLight(0xfff2e0, 0x1a140f, 0.6));
  // --- wheel plate (portrait photo 1365x2048)
  const wd = (u, v) => 0.55 * Math.max(0, 1 - Math.hypot((u - 0.44) / 0.42, (v - 0.44) / 0.3)) - 0.25 * Math.max(0, v - 0.75);
  const wheel = photoPlate(imgTex(IMG.wheel), 6, 9, wd, [60, 90]); wheel.position.copy(WHEEL); scene.add(wheel); const WU = wheel.userData.u;
  const wSteam = makeSmoke(90, 0xe9e6e2, 0.42); scene.add(wSteam);
  // --- viaduct plate (portrait photo 1365x2048)
  const vd = (u, v) => (v < 0.24 ? 0.9 * (1 - v / 0.24) : 0) - 0.9 * Math.max(0, v - 0.5) / 0.5 + 0.15 * Math.max(0, 1 - Math.abs(v - 0.42) / 0.12);
  const via = photoPlate(imgTex(IMG.viaduct), 6, 9, vd, [60, 90]); via.position.copy(VIA); scene.add(via); const VU = via.userData.u;
  const vSteam = makeSmoke(110, 0xffffff, 0.55); scene.add(vSteam);
  const PLUME = new THREE.Vector3(VIA.x + (0.705 - 0.5) * 6, VIA.y + (0.585 - 0.5) * 9, 0.25);
  const sun = glowPlane(9, 0xffc070, 0); sun.position.set(VIA.x + 2.2, VIA.y + 3.6, 0.6); scene.add(sun);
  // --- desk + page 25
  const wood = noiseTex(1024, 512, '#2a1a10', [[1600, 'rgba(10,5,2,A)', 1, 3, 0.2, 0.5], [500, 'rgba(120,80,40,A)', 1, 2, 0.1, 0.25]], 22, [3, 2]);
  const desk = new THREE.Mesh(new THREE.PlaneGeometry(18, 12), new THREE.MeshStandardMaterial({ map: wood, color: 0x8a6a50, roughness: 0.6, envMap: env, envMapIntensity: 0.3 }));
  desk.position.copy(DESK).add(new THREE.Vector3(0, 0, -0.05)); scene.add(desk);
  const lamp = new THREE.SpotLight(0xffd8a8, 90, 18, 0.7, 0.8, 1.5); lamp.position.copy(DESK).add(new THREE.Vector3(-2, 3, 6)); lamp.target.position.copy(DESK); scene.add(lamp, lamp.target);
  const page = makeSheet(imgTex(IMG.odl25), 3.4, 2651 / 2048, { service: HL.odl25_service, gained: HL.odl25_gained }, { curl: 0.025, bright: 0.97 });
  page.position.copy(DESK).add(new THREE.Vector3(0, 0, 0.04)); page.rotation.z = 0.04; scene.add(page);
  const pshadow = new THREE.Mesh(new THREE.PlaneGeometry(3.5, 4.5), new THREE.MeshBasicMaterial({ color: 0, transparent: true, opacity: 0.5, depthWrite: false })); pshadow.position.copy(DESK).add(new THREE.Vector3(0.12, -0.14, 0.0)); pshadow.rotation.z = 0.04; scene.add(pshadow);
  page.updateMatrixWorld(true); const svc = page.userData.local('service').applyMatrix4(page.matrixWorld), gnd = page.userData.local('gained', 1).applyMatrix4(page.matrixWorld);
  const dust = makePoints(120, 0xffe0b0, 0.025, 0.5); scene.add(dust); const R = rng(8); const ds = Array.from({ length: 120 }, () => [R() * 5 - 2.5, R() * 5 - 2.5, 0.3 + R() * 2, R() * 6]);

  function update(t) {
    // wheel: slow push, steam rolling across
    WU.uBright.value = 0.95; WU.uSat.value = 1.05; WU.uVig.value = 0.45;
    wSteam.userData.update(t, (i) => { const te = 27.6 + i * 0.03; const r = rng(i * 5 + 2);
      return { t0: te, pos: new THREE.Vector3(WHEEL.x - 3.2 + r() * 1.5, WHEEL.y - 3.5 + r() * 3, 0.6 + r() * 0.8), vel: new THREE.Vector3(1.0 + r() * 0.8, 0.5 + r() * 0.4, 0.1), size0: 0.6, size1: 2.6, life: 2.4, a: 0.7 }; });
    // viaduct: steam plume puffing up-left, golden grade warming up ("the tracks stayed")
    vSteam.userData.update(t, (i) => { const te = 37.4 + i * 0.035; const r = rng(i * 3 + 9);
      return { t0: te, pos: PLUME.clone().add(new THREE.Vector3((r() - 0.5) * 0.15, 0, 0)), vel: new THREE.Vector3(-0.25 - r() * 0.2, 0.55 + r() * 0.3, 0.05), size0: 0.25, size1: 1.3, life: 2.6, a: 0.85 }; });
    VU.uWarm.value = 0.25 * ep(t, 38.6, 40.4); VU.uBright.value = lerp(0.85, 1.05, ep(t, 38.4, 40.0)); VU.uVig.value = 0.4;
    sun.material.opacity = 0.35 * ep(t, 39.2, 40.6);
    // page 25 highlights
    page.userData.setHL('service', ep(t, 41.45, 42.35, ease.out)); page.userData.setHL('gained', ep(t, 43.2, 44.45, (k) => k));
    page.userData.u.uFocus.value = 0.5 * ep(t, 41.3, 41.9);
    const a = dust.geometry.attributes.position.array; for (let k = 0; k < 120; k++) { const d = ds[k]; a[k * 3] = DESK.x + d[0] + Math.sin(t * 0.3 + d[3]) * 0.2; a[k * 3 + 1] = DESK.y + ((d[1] + t * 0.04) % 5 + 5) % 5 - 2.5; a[k * 3 + 2] = d[2]; }
    dust.geometry.attributes.position.needsUpdate = true;
  }
  const T = (x, y, z) => [x, y, z]; const o = (b, x, y, z) => T(b.x + x, b.y + y, b.z + z);
  const cams = {
    'wheel': [[28.1, o(WHEEL, -0.4, -0.2, 9.0), o(WHEEL, -0.2, -0.3, 0), 44], [30.4, o(WHEEL, 0.1, -0.5, 7.4), o(WHEEL, 0.15, -0.55, 0), 44, 0.05]],
    'via': [[38.1, o(VIA, 0.5, -0.4, 8.6), o(VIA, 0.6, -0.1, 0), 44], [41.4, o(VIA, 0.85, 0.15, 7.0), o(VIA, 0.9, 0.35, 0), 44]],
    'desk': [[41.0, o(DESK, 0.3, -0.2, 7.0), o(DESK, 0.15, -0.3, 0), 36], [42.0, T(svc.x - 0.1, svc.y + 0.1, svc.z + 4.8), T(svc.x - 0.1, svc.y + 0.12, 0), 34],
      [43.4, T(gnd.x + 0.3, gnd.y + 0.12, gnd.z + 4.4), T(gnd.x + 0.3, gnd.y + 0.14, 0), 34], [45.3, T(gnd.x + 0.4, gnd.y + 0.12, gnd.z + 3.8), T(gnd.x + 0.4, gnd.y + 0.14, 0), 34]],
  };
  return { scene, update, cams };
}

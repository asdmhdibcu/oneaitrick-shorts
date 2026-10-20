// DATA CENTRE — the new tracks: glowing rails run down an aisle of server racks ($780B this year);
// the hall multiplies to the horizon ($1.5T a year by 2031); Bain's page 8 floats in ($6T a year needed).
import { THREE, rng, clamp, prog, ease, ep, lerp, glowPlane, makePoints } from './core.js';
import { imgTex, photoPlate, makeSheet } from './kit.js';
import HL from './hl.json';

export function makeDC(env, IMG) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x020409); scene.fog = new THREE.FogExp2(0x030610, 0.016);
  scene.add(new THREE.HemisphereLight(0x5a7ab0, 0x05060a, 0.5));
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 240), new THREE.MeshStandardMaterial({ color: 0x0a0d14, roughness: 0.18, metalness: 0.7, envMap: env, envMapIntensity: 0.6 }));
  floor.rotation.x = -Math.PI / 2; floor.position.z = -80; scene.add(floor);
  // floor tiles grid
  const grid = new THREE.GridHelper(240, 200, 0x1a2640, 0x101828); grid.position.set(0, 0.005, -80); grid.material.transparent = true; grid.material.opacity = 0.35; scene.add(grid);
  // the new tracks: two glowing rails + light-bar sleepers
  const railM = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xc8ff4d).multiplyScalar(1.05), toneMapped: false });
  for (const x of [-0.42, 0.42]) { const r = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.04, 200), railM); r.position.set(x, 0.03, -96); scene.add(r); }
  const NSL = 160; const sleep = new THREE.InstancedMesh(new THREE.BoxGeometry(1.2, 0.02, 0.08), new THREE.MeshBasicMaterial({ color: new THREE.Color(0x7cc4ff).multiplyScalar(0.32), toneMapped: false }), NSL);
  const M = new THREE.Matrix4(); for (let k = 0; k < NSL; k++) { M.makeTranslation(0, 0.015, 4 - k * 1.25); sleep.setMatrixAt(k, M); } scene.add(sleep);
  // racks: body + photo face with blinking LEDs. Rows: x = ±2.2 (main aisle), then extra rows revealed in 2031
  const ROWS = [-2.2, 2.2, -6.6, 6.6, -11, 11, -15.4, 15.4, -19.8, 19.8, -24.2, 24.2];
  const PER = 70, N = ROWS.length * PER;
  const body = new THREE.InstancedMesh(new THREE.BoxGeometry(1.15, 2.5, 0.92), new THREE.MeshStandardMaterial({ color: 0x151a24, metalness: 0.8, roughness: 0.35, envMap: env, envMapIntensity: 0.8 }), N);
  const faceU = { map: { value: imgTex(IMG.servers) }, uT: { value: 0 } };
  const faceG = new THREE.PlaneGeometry(1.0, 2.36); const fid = new Float32Array(N); for (let i = 0; i < N; i++) fid[i] = i; faceG.setAttribute('aId', new THREE.InstancedBufferAttribute(fid, 1));
  const face = new THREE.InstancedMesh(faceG, new THREE.ShaderMaterial({ uniforms: faceU, toneMapped: false,
    vertexShader: `attribute float aId; varying vec2 vUv; varying float vId; varying float vD; void main(){ vUv=uv; vId=aId; vec4 mv=modelViewMatrix*instanceMatrix*vec4(position,1.); vD=-mv.z; gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform sampler2D map; uniform float uT; varying vec2 vUv; varying float vId; varying float vD;
      float h(vec2 p){ return fract(sin(dot(p,vec2(41.3,289.1)))*43758.5); }
      void main(){ vec2 uv=vec2(fract(vUv.x*.5+fract(vId*.37)*.5), vUv.y*.78+.11); vec3 c=texture2D(map,uv).rgb*1.5;
        vec2 cell=floor(vUv*vec2(6.,26.)); vec2 f=fract(vUv*vec2(6.,26.))-.5; float on=step(.55,h(cell+vId*1.7+floor(uT*(2.+h(cell)*6.))));
        float led=smoothstep(.22,.0,length(f*vec2(1.,.6)))*on; vec3 lc=mix(vec3(.2,1.,.45),vec3(1.,.3,.25),step(.8,h(cell*3.1+vId)));
        c+=lc*led*2.4; float fog=exp(-vD*.03); gl_FragColor=vec4(c*fog,1.); }` }), N);
  const Q = new THREE.Quaternion(), P = new THREE.Vector3(), S = new THREE.Vector3(1, 1, 1), Yax = new THREE.Vector3(0, 1, 0);
  const rowOf = (i) => Math.floor(i / PER), zOf = (i) => 1.5 - (i % PER) * 1.2;
  const top = new THREE.InstancedMesh(new THREE.BoxGeometry(1.05, 0.05, 0.12), new THREE.MeshBasicMaterial({ color: new THREE.Color(0x7cc4ff).multiplyScalar(1.15), toneMapped: false }), N);
  body.frustumCulled = face.frustumCulled = top.frustumCulled = false; scene.add(body, face, top);
  // ceiling light strips
  const NL = 90; const strip = new THREE.InstancedMesh(new THREE.BoxGeometry(0.12, 0.04, 1.6), new THREE.MeshBasicMaterial({ color: new THREE.Color(0xd8ecff).multiplyScalar(1.1), toneMapped: false }), NL);
  for (let k = 0; k < NL; k++) { M.makeTranslation(k % 2 ? 0.9 : -0.9, 3.6, 2 - Math.floor(k / 2) * 2.6); strip.setMatrixAt(k, M); } scene.add(strip);
  // the far end: the corridor photo as a cold, glowing vanishing point
  const end = photoPlate(imgTex(IMG.corridor), 8, 8 * 1786 / 1333, () => 0, [2, 2]); end.position.set(0, 4.5, -86); end.userData.u.uCool.value = 0.8; end.userData.u.uBright.value = 0.55; scene.add(end);
  const glowEnd = glowPlane(30, 0x7cc4ff, 0.25); glowEnd.position.set(0, 3, -80); scene.add(glowEnd);
  const motes = makePoints(300, 0x9fd0ff, 0.03, 0.6); scene.add(motes); const R = rng(14); const ms = Array.from({ length: 300 }, () => [R() * 8 - 4, R() * 3.5, R() * -40, R() * 6]);
  // Bain page 8 (floats in during "the consultants at Bain did the maths")
  const page = makeSheet(imgTex(IMG.bain8), 3.4, 2651 / 2048, { b780: HL.bain8_780, b15: HL.bain8_15, b6: HL.bain8_6 }, { curl: 0.03, bright: 0.98 });
  scene.add(page); const SHEET = new THREE.Vector3(0, 13.4, 0.6);
  page.position.copy(SHEET); page.updateMatrixWorld(true);
  const pB6 = page.userData.local('b6').add(SHEET);

  function update(t) {
    faceU.uT.value = t;
    for (let i = 0; i < N; i++) { const r = rowOf(i); const x = ROWS[r]; const z = zOf(i);
      const appear = r < 2 ? 1 : ep(t, 52.3 + (r - 2) * 0.22 + (i % PER) * 0.004, 53.0 + (r - 2) * 0.22 + (i % PER) * 0.004, ease.out);
      const side = x < 0 ? 1 : -1; Q.setFromAxisAngle(Yax, side * Math.PI / 2);
      S.set(1, Math.max(0.001, appear), 1); P.set(x, 1.25 * appear, z); M.compose(P, Q, S); body.setMatrixAt(i, M);
      P.set(x + side * 0.465, 1.25 * appear, z); M.compose(P, Q, S); face.setMatrixAt(i, M);
      P.set(x + side * 0.4, 2.52 * appear, z); M.compose(P, Q, S.set(appear, appear, appear)); top.setMatrixAt(i, M); }
    body.instanceMatrix.needsUpdate = true; face.instanceMatrix.needsUpdate = true; top.instanceMatrix.needsUpdate = true;
    const a = motes.geometry.attributes.position.array; for (let k = 0; k < 300; k++) { const m = ms[k]; a[k * 3] = m[0] + Math.sin(t * 0.4 + m[3]) * 0.3; a[k * 3 + 1] = (m[1] + t * 0.08) % 3.5; a[k * 3 + 2] = m[2]; } motes.geometry.attributes.position.needsUpdate = true;
    // page: slides down into view at 55.4, highlights 780 -> 1.5T -> 6T
    const pin = ep(t, 55.35, 56.2, ease.out); page.position.set(SHEET.x, SHEET.y - (1 - pin) * 5, SHEET.z); page.rotation.set(-0.06 - (1 - pin) * 0.5, 0.04, -0.03 + (1 - pin) * 0.2);
    page.visible = t > 55.2; page.userData.u.uFade.value = pin;
    page.userData.setHL('b780', ep(t, 56.25, 56.6)); page.userData.setHL('b15', ep(t, 56.75, 57.1)); page.userData.setHL('b6', ep(t, 59.35, 60.45, (k) => k));
    page.userData.u.uFocus.value = 0.55 * ep(t, 57.4, 58.0);
  }
  const T = (x, y, z) => [x, y, z];
  const cams = {
    'dc-a': [[44.9, T(0.0, 1.3, 8.0), T(0, 1.15, -20), 46], [48.0, T(0.15, 1.35, 3.5), T(0, 1.2, -22), 46], [51.9, T(-0.1, 1.45, -3.5), T(0, 1.3, -26), 46]],
    'dc-b': [[51.85, T(-0.1, 1.5, -3.6), T(0, 1.3, -26), 46], [53.6, T(0, 9.5, 2.0), T(0, 0, -26), 50], [55.3, T(0, 14.2, 6.2), T(0, 2.0, -24), 52, 0, 'ease']],
    'dc-c': [[55.2, T(0, 14.6, 6.4), T(0, 14.4, 0.6), 46], [57.5, T(0.05, 14.5, 5.6), T(0.05, 14.45, 0.6), 40, 0, 'ease'], [59.2, T(pB6.x + 0.35, pB6.y + 0.08, 5.0), T(pB6.x + 0.35, pB6.y + 0.1, 0.6), 36, 0, 'ease'], [60.9, T(pB6.x + 0.38, pB6.y + 0.08, 4.6), T(pB6.x + 0.38, pB6.y + 0.1, 0.6), 36]],
  };
  return { scene, update, cams };
}

// WORLD 3 — "It's a pattern": 19 incident beacons across a dark terrain, and a line still being written.
import { THREE, rng, clamp, lerp, prog, ep, ease, keys, glowPlane, lightCone, makePoints } from './core.js';
import { COL } from './robot.js';

const T = (x, y, z) => [x, y, z];
function cr(p0, p1, p2, p3, u) { const u2 = u * u, u3 = u2 * u; return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u3); }
function path(keys) { return (t) => { if (t <= keys[0][0]) return keys[0]; const n = keys.length; if (t >= keys[n - 1][0]) return keys[n - 1];
  let i = 0; while (i < n - 2 && t > keys[i + 1][0]) i++; const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(n - 1, i + 2)];
  const u = (t - k1[0]) / (k2[0] - k1[0]); const f = (a) => [0, 1, 2].map(j => cr(k0[a][j], k1[a][j], k2[a][j], k3[a][j], u)); return [t, f(1), f(2), cr(k0[3], k1[3], k2[3], k3[3], u), 0]; }; }

export function makeMap(env) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x05050a); scene.fog = new THREE.FogExp2(0x07060c, 0.012);
  // terrain: displaced plane with contour-line shader
  const g = new THREE.PlaneGeometry(220, 220, 180, 180); g.rotateX(-Math.PI / 2);
  const P = g.attributes.position.array; const R = rng(91);
  const hgt = (x, z) => Math.sin(x * 0.045) * 3.2 + Math.cos(z * 0.05 + x * 0.02) * 2.6 + Math.sin((x + z) * 0.11) * 0.9;
  for (let i = 0; i < P.length; i += 3) P[i + 1] = hgt(P[i], P[i + 2]);
  g.computeVertexNormals();
  const terrU = { uT: { value: 0 }, uRed: { value: 0 } };
  const terrain = new THREE.Mesh(g, new THREE.ShaderMaterial({ uniforms: terrU, toneMapped: false,
    vertexShader: `varying vec3 vP; varying float vD; void main(){ vP=position; vec4 mv=modelViewMatrix*vec4(position,1.); vD=-mv.z; gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform float uT,uRed; varying vec3 vP; varying float vD; void main(){
      float c=abs(fract(vP.y*1.6)-.5); float line=smoothstep(.06,0.,c-.44);
      vec2 gg=abs(fract(vP.xz/8.)-.5); float grid=smoothstep(.02,0.,min(gg.x,gg.y)-.48);
      vec3 base=vec3(.02,.025,.04); vec3 lc=mix(vec3(.25,.42,.75),vec3(.9,.25,.3),uRed);
      vec3 col=base+lc*(line*.35+grid*.18); float fog=exp(-vD*.016); gl_FragColor=vec4(col*fog,1.); }` }));
  scene.add(terrain);

  // 19 beacons, in the order they "happened", joined into a path
  const N = 19, B = []; for (let k = 0; k < N; k++) { const a = k * 2.4 + R() * 0.6, r = 10 + k * 3.1 + R() * 4; const x = Math.cos(a) * r, z = -Math.sin(a) * r * 0.8 - 8; B.push(new THREE.Vector3(x, hgt(x, z), z)); }
  const pillars = [], bases = [], halos = [];
  const cores = [];
  B.forEach((p, k) => { const core = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 1, 8), new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.red).multiplyScalar(2.6), toneMapped: false })); core.geometry.translate(0, 0.5, 0); core.position.set(p.x, p.y, p.z); scene.add(core); cores.push(core);
    const pil = lightCone(26, 1.6, COL.red, 0.0); pil.rotation.x = Math.PI; pil.position.set(p.x, p.y, p.z); scene.add(pil); pillars.push(pil);
    const base = new THREE.Mesh(new THREE.RingGeometry(0.9, 1.15, 48), new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.red).multiplyScalar(2.4), transparent: true, opacity: 0, toneMapped: false, side: THREE.DoubleSide, depthWrite: false }));
    base.rotation.x = -Math.PI / 2; base.position.set(p.x, p.y + 0.08, p.z); scene.add(base); bases.push(base);
    const h = glowPlane(7, COL.red, 0); h.position.set(p.x, p.y + 1.2, p.z); scene.add(h); halos.push(h); });
  // path line through the beacons, drawn progressively, then extending into the dark
  const ext = B[N - 1].clone().add(new THREE.Vector3(-34, 0, -46)); ext.y = hgt(ext.x, ext.z);
  const pts = [...B, ext]; const curve = new THREE.CatmullRomCurve3(pts.map(p => p.clone().add(new THREE.Vector3(0, 0.25, 0))));
  const lineG = new THREE.TubeGeometry(curve, 700, 0.26, 8);
  const lineU = { uP: { value: 0 } };
  const line = new THREE.Mesh(lineG, new THREE.ShaderMaterial({ uniforms: lineU, transparent: true, depthWrite: false, toneMapped: false, blending: THREE.AdditiveBlending,
    vertexShader: `varying float vO; void main(){ vO=uv.x; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform float uP; varying float vO; void main(){ float on=step(vO,uP); float head=smoothstep(.015,0.,uP-vO); gl_FragColor=vec4(vec3(1.,.32,.36)*(1.2+head*3.5), on); }` }));
  scene.add(line);
  const head = glowPlane(9, COL.red, 0); scene.add(head);
  const dust = makePoints(600, COL.red, 0.05, 0.8); scene.add(dust); const ds = Array.from({ length: 600 }, () => [R() * 2 - 1, R(), R() * 2 - 1]);
  // arrival order mapped to the spoken "pattern" + "still being written"
  const tOn = (k) => 93.35 + k * 0.075;
  const segOf = (k) => k / N * 0.86; // fraction of the curve at beacon k (approx)

  function update(t) {
    terrU.uT.value = t; terrU.uRed.value = ep(t, 93.3, 94.5);
    B.forEach((p, k) => { const on = ep(t, tOn(k), tOn(k) + 0.35, ease.back); pillars[k].material.uniforms.o.value = 0.5 * clamp(on); cores[k].scale.set(1, Math.max(0.001, 22 * clamp(on)), 1); bases[k].material.opacity = clamp(on); bases[k].scale.setScalar(Math.max(0.001, on * (1 + 0.15 * Math.sin(t * 4 + k)))); halos[k].material.opacity = 0.55 * clamp(on); });
    const draw = t < 94.85 ? ep(t, 93.4, 94.75) * 0.86 : 0.86 + ep(t, 94.9, 96.9, ease.out) * 0.14;
    lineU.uP.value = draw; const hp = curve.getPointAt(clamp(draw, 0.001, 0.999)); head.position.copy(hp).add(new THREE.Vector3(0, 0.4, 0)); head.material.opacity = t > 93.4 ? 0.9 : 0;
    { const a = dust.geometry.attributes.position.array; for (let k = 0; k < 600; k++) { const s = ds[k]; a[k * 3] = s[0] * 70; a[k * 3 + 1] = ((s[1] * 20 + t * 0.6) % 20); a[k * 3 + 2] = s[2] * 70 - 20; } dust.geometry.attributes.position.needsUpdate = true; }
  }
  const cams = { map: path([[91.45, T(4, 32, 40), T(0, 0, -10), 46], [93.3, T(4, 36, 44), T(0, 0, -14), 50], [94.9, T(-2, 30, 32), T(-8, 0, -22), 48], [96.85, T(-16, 18, 2), T(-34, 0, -46), 44]]) };
  return { scene, update, camFor: (id) => cams[id] };
}

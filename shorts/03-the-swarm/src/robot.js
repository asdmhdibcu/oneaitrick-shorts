// Procedural robot (brand look: white glossy shell, dark visor, glowing eyes, pink ears, antenna balls).
import { THREE } from './core.js';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

export const COL = { lime: 0xc8ff4d, blue: 0x7cc4ff, amber: 0xffb547, pink: 0xff7ac6, red: 0xff6b6b, ink: 0xf5f5f2 };

// dissolve-capable standard material (discard by world-space noise, glowing burn edge)
function dissolvable(mat, edgeColor = 0xc8ff4d) {
  mat.userData.dis = { value: 0 };
  mat.userData.edge = { value: new THREE.Color(edgeColor) };
  mat.onBeforeCompile = (sh) => {
    sh.uniforms.uDis = mat.userData.dis; sh.uniforms.uEdge = mat.userData.edge;
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWp;')
      .replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvWp=(modelMatrix*vec4(transformed,1.)).xyz;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
      uniform float uDis; uniform vec3 uEdge; varying vec3 vWp;
      float dh(vec3 p){return fract(sin(dot(p,vec3(12.9898,78.233,37.719)))*43758.5453);}
      float dn(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
        return mix(mix(mix(dh(i),dh(i+vec3(1,0,0)),f.x),mix(dh(i+vec3(0,1,0)),dh(i+vec3(1,1,0)),f.x),f.y),
                   mix(mix(dh(i+vec3(0,0,1)),dh(i+vec3(1,0,1)),f.x),mix(dh(i+vec3(0,1,1)),dh(i+vec3(1,1,1)),f.x),f.y),f.z);}`)
      .replace('#include <dithering_fragment>', `#include <dithering_fragment>
      if(uDis>0.){ float k=dn(vWp*7.)*.7+dn(vWp*19.)*.3 + (vWp.y-0.)*0.0; float th=uDis*1.15-.05;
        if(k<th) discard; float e=smoothstep(th+.07,th,k); gl_FragColor.rgb+=uEdge*e*4.; }`);
  };
  return mat;
}

const G = {}; // shared geometry (hi / lo)
function geo(lo) {
  const k = lo ? 'lo' : 'hi'; if (G[k]) return G[k];
  const s = lo ? 2 : 6;
  G[k] = {
    shell: new RoundedBoxGeometry(1.0, 0.86, 0.86, s, 0.28),
    visor: new RoundedBoxGeometry(0.82, 0.46, 0.14, lo ? 2 : 4, 0.13),
    eye: lo ? new THREE.BoxGeometry(0.13, 0.24, 0.05) : new RoundedBoxGeometry(0.13, 0.25, 0.05, 3, 0.06),
    mouth: new RoundedBoxGeometry(0.3, 0.08, 0.05, 2, 0.035),
    pill: new RoundedBoxGeometry(0.42, 0.11, 0.24, lo ? 1 : 3, 0.05),
    ear: new THREE.CylinderGeometry(0.15, 0.15, 0.13, lo ? 10 : 32).rotateZ(Math.PI / 2),
    stalk: new THREE.CylinderGeometry(0.022, 0.022, 0.4, 10),
    ball: new THREE.SphereGeometry(0.085, lo ? 8 : 24, lo ? 6 : 16),
  };
  return G[k];
}

// ---------------- hero robot ----------------
export function makeRobot(env, eyeColor = COL.blue) {
  const g = geo(false), root = new THREE.Group(), body = new THREE.Group(); root.add(body);
  const shellM = dissolvable(new THREE.MeshPhysicalMaterial({ color: 0xdfe4ec, roughness: 0.26, metalness: 0, clearcoat: 0.8, clearcoatRoughness: 0.14, envMap: env, envMapIntensity: 0.42 }));
  const visorM = dissolvable(new THREE.MeshStandardMaterial({ color: 0x141826, roughness: 0.08, metalness: 0.6, envMap: env, envMapIntensity: 0.9 }));
  const pinkM = dissolvable(new THREE.MeshPhysicalMaterial({ color: 0xff5fae, roughness: 0.25, clearcoat: 1, clearcoatRoughness: 0.2, envMap: env, emissive: 0x3a0a22 }));
  const pillM = dissolvable(new THREE.MeshPhysicalMaterial({ color: 0xe8a530, roughness: 0.42, clearcoat: 0.6, envMap: env, envMapIntensity: 0.5, emissive: 0x1a0f00 }));
  const greyM = dissolvable(new THREE.MeshStandardMaterial({ color: 0x9aa3b5, roughness: 0.4, metalness: 0.6, envMap: env }));
  const eyeM = new THREE.MeshBasicMaterial({ color: new THREE.Color(eyeColor).multiplyScalar(2.6), toneMapped: false });
  const ballM = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xff4f7a).multiplyScalar(2.2), toneMapped: false });
  const mouthM = new THREE.MeshStandardMaterial({ color: 0x1a1e2b, roughness: 0.3, envMap: env });
  const add = (gm, m, x, y, z) => { const o = new THREE.Mesh(gm, m); o.position.set(x, y, z); body.add(o); return o; };
  add(g.shell, shellM, 0, 0, 0);
  add(g.visor, visorM, 0, 0.04, 0.38);
  const eL = add(g.eye, eyeM, -0.17, 0.05, 0.46), eR = add(g.eye, eyeM, 0.17, 0.05, 0.46);
  add(g.mouth, mouthM, 0, -0.27, 0.42);
  add(g.pill, pillM, 0, 0.47, 0);
  add(g.ear, pinkM, -0.55, 0, 0); add(g.ear, pinkM, 0.55, 0, 0);
  add(g.stalk, greyM, -0.55, 0.27, 0); add(g.stalk, greyM, 0.55, 0.27, 0);
  const bL = add(g.ball, ballM, -0.55, 0.5, 0), bR = add(g.ball, ballM, 0.55, 0.5, 0);
  const mats = [shellM, visorM, pinkM, pillM, greyM];
  root.userData = {
    body, eyes: [eL, eR], eyeM, ballM, mats,
    setEyes(c, k = 2.6) { eyeM.color.set(c).multiplyScalar(k); },
    setDissolve(d, edge) { mats.forEach(m => { m.userData.dis.value = d; if (edge !== undefined) m.userData.edge.value.set(edge); }); eL.visible = eR.visible = bL.visible = bR.visible = d < 0.55; },
    blink(k) { eL.scale.y = eR.scale.y = Math.max(0.08, 1 - k); },
  };
  return root;
}

// ---------------- instanced army ----------------
// bots: array of {x,y,z, ry, s} ; per-frame call update(fn) where fn(i, out) fills out {x,y,z,ry,rx,s,eye:Color,show}
export function makeArmy(env, n) {
  const g = geo(true);
  const shellM = new THREE.MeshStandardMaterial({ color: 0x6b7586, roughness: 0.42, metalness: 0.15, envMap: env, envMapIntensity: 0.3 });
  const visorM = new THREE.MeshStandardMaterial({ color: 0x0e111a, roughness: 0.12, metalness: 0.6, envMap: env, envMapIntensity: 0.5 });
  const pinkM = new THREE.MeshStandardMaterial({ color: 0x9c3a6c, roughness: 0.35, envMap: env, envMapIntensity: 0.3, emissive: 0x1a0610 });
  const pillM = new THREE.MeshStandardMaterial({ color: 0x9c7430, roughness: 0.4, envMap: env, envMapIntensity: 0.3, emissive: 0x140c00 });
  const eyeM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const mk = (gm, m, c) => { const im = new THREE.InstancedMesh(gm, m, c); im.instanceMatrix.setUsage(THREE.DynamicDrawUsage); im.frustumCulled = false; return im; };
  const shell = mk(g.shell, shellM, n), visor = mk(g.visor, visorM, n), pill = mk(g.pill, pillM, n);
  const eyes = mk(g.eye, eyeM, 2 * n), ears = mk(g.ear, pinkM, 2 * n);
  eyes.setColorAt(0, new THREE.Color(1, 1, 1));
  const grp = new THREE.Group(); [shell, visor, pill, eyes, ears].forEach(m => grp.add(m));
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), E = new THREE.Euler(), P = new THREE.Vector3(), S = new THREE.Vector3(), L = new THREE.Matrix4(), O = new THREE.Matrix4();
  const local = {
    visor: new THREE.Matrix4().makeTranslation(0, 0.04, 0.38), pill: new THREE.Matrix4().makeTranslation(0, 0.47, 0),
    eL: new THREE.Matrix4().makeTranslation(-0.17, 0.05, 0.46), eR: new THREE.Matrix4().makeTranslation(0.17, 0.05, 0.46),
    aL: new THREE.Matrix4().makeTranslation(-0.55, 0, 0), aR: new THREE.Matrix4().makeTranslation(0.55, 0, 0),
  };
  const zero = new THREE.Matrix4().makeScale(0, 0, 0);
  const o = { x: 0, y: 0, z: 0, ry: 0, rx: 0, s: 1, eye: new THREE.Color(), show: true, blink: 0 };
  const eyeScale = new THREE.Matrix4();
  grp.userData.update = (count, fn) => {
    for (let i = 0; i < n; i++) {
      if (i >= count) { shell.setMatrixAt(i, zero); visor.setMatrixAt(i, zero); pill.setMatrixAt(i, zero); eyes.setMatrixAt(2 * i, zero); eyes.setMatrixAt(2 * i + 1, zero); ears.setMatrixAt(2 * i, zero); ears.setMatrixAt(2 * i + 1, zero); continue; }
      o.show = true; o.rx = 0; o.blink = 0; fn(i, o);
      if (!o.show || o.s <= 0.001) { shell.setMatrixAt(i, zero); visor.setMatrixAt(i, zero); pill.setMatrixAt(i, zero); eyes.setMatrixAt(2 * i, zero); eyes.setMatrixAt(2 * i + 1, zero); ears.setMatrixAt(2 * i, zero); ears.setMatrixAt(2 * i + 1, zero); continue; }
      P.set(o.x, o.y, o.z); E.set(o.rx, o.ry, 0); Q.setFromEuler(E); S.setScalar(o.s); M.compose(P, Q, S);
      shell.setMatrixAt(i, M);
      visor.setMatrixAt(i, O.multiplyMatrices(M, local.visor)); pill.setMatrixAt(i, O.multiplyMatrices(M, local.pill));
      eyeScale.makeScale(1, Math.max(0.08, 1 - o.blink), 1);
      eyes.setMatrixAt(2 * i, O.multiplyMatrices(M, local.eL).multiply(eyeScale)); eyes.setMatrixAt(2 * i + 1, L.multiplyMatrices(M, local.eR).multiply(eyeScale));
      eyes.setColorAt(2 * i, o.eye); eyes.setColorAt(2 * i + 1, o.eye);
      ears.setMatrixAt(2 * i, O.multiplyMatrices(M, local.aL)); ears.setMatrixAt(2 * i + 1, L.multiplyMatrices(M, local.aR));
    }
    [shell, visor, pill, eyes, ears].forEach(m => { m.instanceMatrix.needsUpdate = true; });
    if (eyes.instanceColor) eyes.instanceColor.needsUpdate = true;
  };
  return grp;
}

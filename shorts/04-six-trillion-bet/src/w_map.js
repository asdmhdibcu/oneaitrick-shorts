// MAP — Britain at night. The 1845 network glows amber; in 1846 Parliament approves 4,538 more miles,
// which fire out in lime until the web is nearly twice the size. Routes are illustrative.
import { THREE, rng, clamp, prog, ease, ep, lerp, glowPlane, makePoints } from './core.js';
import GEO from './britain.json';

const LON0 = -3, LAT0 = 54.5, K = 2, CX = Math.cos(LAT0 * Math.PI / 180);
export const proj = (lat, lon) => new THREE.Vector3((lon - LON0) * CX * K, 0, -(lat - LAT0) * K);
const C = {
  london: [51.507, -0.128], birmingham: [52.486, -1.89], manchester: [53.48, -2.242], liverpool: [53.408, -2.991], leeds: [53.8, -1.549], york: [53.959, -1.082],
  newcastle: [54.978, -1.618], bristol: [51.455, -2.588], southampton: [50.909, -1.404], brighton: [50.822, -0.137], derby: [52.921, -1.476], darlington: [54.523, -1.552],
  carlisle: [54.892, -2.934], edinburgh: [55.953, -3.188], glasgow: [55.864, -4.252], gloucester: [51.864, -2.238], exeter: [50.718, -3.533], colchester: [51.889, 0.901],
  norwich: [52.63, 1.297], cambridge: [52.205, 0.122], hull: [53.745, -0.336], sheffield: [53.381, -1.47], nottingham: [52.954, -1.158], leicester: [52.637, -1.14],
  rugby: [52.37, -1.264], oxford: [51.752, -1.258], preston: [53.763, -2.703], lancaster: [54.047, -2.801], chester: [53.193, -2.893], holyhead: [53.309, -4.633],
  shrewsbury: [52.707, -2.754], hereford: [52.056, -2.716], cardiff: [51.481, -3.179], swansea: [51.621, -3.944], plymouth: [50.375, -4.143], salisbury: [51.069, -1.794],
  dover: [51.128, 1.313], hastings: [50.854, 0.573], portsmouth: [50.819, -1.087], weymouth: [50.614, -2.457], lincoln: [53.234, -0.538], peterborough: [52.573, -0.24],
  ipswich: [52.057, 1.148], berwick: [55.771, -2.007], aberdeen: [57.15, -2.094], perth: [56.396, -3.437], dundee: [56.462, -2.971], stirling: [56.12, -3.937],
  dumfries: [55.07, -3.605], kendal: [54.328, -2.746], scarborough: [54.283, -0.4], crewe: [53.099, -2.441], stafford: [52.806, -2.117], worcester: [52.192, -2.22],
  bath: [51.381, -2.359], reading: [51.454, -0.978], ayr: [55.458, -4.629], kilmarnock: [55.611, -4.495], thirsk: [54.232, -1.343], yarmouth: [52.608, 1.729],
  boston: [52.976, -0.026], kings_lynn: [52.754, 0.398], northampton: [52.24, -0.902], bedford: [52.136, -0.467], aylesbury: [51.816, -0.812], tunbridge: [51.132, 0.263],
  canterbury: [51.28, 1.079], dorchester: [50.715, -2.437], taunton: [51.015, -3.103], barnstaple: [51.08, -4.058], truro: [50.263, -5.051], newport: [51.588, -2.998],
  wrexham: [53.046, -2.993], bangor: [53.227, -4.129], whitehaven: [54.549, -3.587], hawick: [55.422, -2.787], montrose: [56.708, -2.467], falkirk: [56.002, -3.784],
};
const OLD = 'london-rugby rugby-birmingham birmingham-stafford stafford-crewe crewe-manchester crewe-liverpool liverpool-manchester manchester-leeds birmingham-derby rugby-leicester leicester-derby derby-sheffield sheffield-leeds leeds-york york-darlington darlington-newcastle newcastle-carlisle preston-lancaster manchester-preston crewe-chester london-reading reading-bath bath-bristol bristol-taunton taunton-exeter bristol-gloucester gloucester-birmingham london-southampton london-brighton london-tunbridge tunbridge-dover london-colchester london-cambridge cambridge-norwich norwich-yarmouth hull-leeds edinburgh-falkirk falkirk-glasgow glasgow-ayr reading-oxford derby-nottingham';
const NEW = 'lancaster-kendal kendal-carlisle carlisle-dumfries dumfries-kilmarnock kilmarnock-glasgow carlisle-hawick hawick-edinburgh newcastle-berwick berwick-edinburgh chester-wrexham wrexham-shrewsbury chester-bangor bangor-holyhead shrewsbury-hereford hereford-newport gloucester-newport newport-cardiff cardiff-swansea exeter-plymouth plymouth-truro taunton-barnstaple salisbury-southampton southampton-dorchester dorchester-weymouth london-portsmouth london-hastings tunbridge-hastings canterbury-dover london-canterbury london-bedford bedford-peterborough peterborough-boston boston-lincoln lincoln-york london-aylesbury aylesbury-oxford oxford-worcester worcester-birmingham shrewsbury-stafford northampton-peterborough rugby-northampton colchester-ipswich ipswich-norwich cambridge-kings_lynn kings_lynn-peterborough nottingham-lincoln sheffield-manchester leeds-thirsk thirsk-darlington york-scarborough hull-york stirling-perth perth-dundee dundee-montrose montrose-aberdeen falkirk-stirling edinburgh-perth whitehaven-carlisle salisbury-bath reading-salisbury';

export function makeMap(env) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x03050a); scene.fog = new THREE.Fog(0x03050a, 40, 90);
  // sea with a faint graticule
  const sea = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), new THREE.ShaderMaterial({ uniforms: { uT: { value: 0 } }, toneMapped: false,
    vertexShader: `varying vec3 vP; void main(){ vP=position; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `varying vec3 vP; void main(){ vec2 g=abs(fract(vP.xy/2.)-.5); float l=smoothstep(.015,0.,min(g.x,g.y)-.48);
      float r=length(vP.xy)/40.; vec3 c=vec3(.012,.02,.04)+vec3(.05,.09,.16)*l*(1.-r); gl_FragColor=vec4(c*(1.-r*.6),1.); }` }));
  sea.rotation.x = -Math.PI / 2; sea.position.y = -0.02; scene.add(sea);
  // land + coast
  const landM = new THREE.MeshBasicMaterial({ color: 0x172033, toneMapped: false }); const irM = new THREE.MeshBasicMaterial({ color: 0x0e1422, toneMapped: false });
  const coastM = new THREE.LineBasicMaterial({ color: new THREE.Color(0x5f86c9).multiplyScalar(1.1), transparent: true, opacity: 0.8, toneMapped: false });
  for (const [key, mat] of [['gb', landM], ['ie', irM]]) for (const ring of GEO[key]) {
    const pts = ring.map(([lo, la]) => { const v = proj(la, lo); return new THREE.Vector2(v.x, -v.z); });
    const m = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(pts)), mat); m.rotation.x = -Math.PI / 2; scene.add(m);
    const lg = new THREE.BufferGeometry().setFromPoints(pts.map((p) => new THREE.Vector3(p.x, 0.02, -p.y))); scene.add(new THREE.LineLoop(lg, coastM));
  }
  // towns
  const names = Object.keys(C); const town = makePoints(names.length, 0xffe2a8, 0.16, 0.9); const ta = town.geometry.attributes.position.array;
  names.forEach((n, i) => { const v = proj(...C[n]); ta[i * 3] = v.x; ta[i * 3 + 1] = 0.08; ta[i * 3 + 2] = v.z; }); scene.add(town);
  // routes: gentle arcs on the ground
  const R = rng(17);
  const route = (pair, color, w) => { const [a, b] = pair.split('-'); const A = proj(...C[a]), B = proj(...C[b]); const mid = A.clone().add(B).multiplyScalar(0.5);
    const n = new THREE.Vector3(-(B.z - A.z), 0, B.x - A.x).normalize().multiplyScalar((R() - 0.5) * 0.18 * A.distanceTo(B)); mid.add(n);
    const cv = new THREE.QuadraticBezierCurve3(A.clone().setY(0.06), mid.setY(0.06), B.clone().setY(0.06));
    const m = new THREE.Mesh(new THREE.TubeGeometry(cv, 40, w, 5), new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(1.35), toneMapped: false, transparent: true }));
    scene.add(m); return { m, cv, n: m.geometry.index.count, len: A.distanceTo(B) }; };
  const old = OLD.split(' ').map((p) => route(p, 0xffb547, 0.045));
  const neu = NEW.split(' ').map((p) => route(p, 0xc8ff4d, 0.04));
  // order new lines by distance from London so they "fire out"
  const L = proj(...C.london); neu.forEach((r) => { r.d = r.cv.getPoint(0).distanceTo(L); }); const order = [...neu].sort((a, b) => a.d - b.d);
  order.forEach((r, i) => { r.t0 = 22.1 + i * (2.9 / order.length); r.t1 = r.t0 + 0.55 + r.len * 0.03; });
  const heads = makePoints(neu.length, 0xf4ffd0, 0.3, 1); scene.add(heads); const ha = heads.geometry.attributes.position.array, hs = heads.geometry.attributes.aSize.array;
  const halo = glowPlane(26, 0xc8ff4d, 0); halo.rotation.x = -Math.PI / 2; halo.position.set(1, 0.03, 1); scene.add(halo);
  function update(t) {
    old.forEach((r) => { r.m.material.opacity = ep(t, 19.9, 20.6) * (1 - 0.35 * ep(t, 25.6, 26.4)); });
    order.forEach((r, i) => { const k = ep(t, r.t0, r.t1, ease.out); r.m.geometry.setDrawRange(0, Math.floor(r.n * k / 3) * 3); r.m.visible = k > 0;
      const p = r.cv.getPoint(k); ha[i * 3] = p.x; ha[i * 3 + 1] = 0.15; ha[i * 3 + 2] = p.z; hs[i] = k > 0 && k < 1 ? 1.3 : 0;
      r.m.material.color.set(0xc8ff4d).multiplyScalar(1.35 + 0.7 * ep(t, 25.7, 26.2) * (1 - ep(t, 26.4, 27.6))); });
    heads.geometry.attributes.position.needsUpdate = true; heads.geometry.attributes.aSize.needsUpdate = true;
    halo.material.opacity = 0.16 * ep(t, 25.7, 26.3) * (1 - ep(t, 27.2, 28.2));
  }
  const T = (x, y, z) => [x, y, z];
  const cams = {
    'map': [[20.0, T(0.9, 19, 7.0), T(0.6, 0, -0.2), 40], [21.8, T(0.9, 22, 7.4), T(0.6, 0, -0.6), 40], [25.3, T(0.7, 27, 8.0), T(0.5, 0, -1.2), 40], [28.5, T(0.6, 30.5, 8.4), T(0.5, 0, -1.5), 40]],
  };
  return { scene, update, cams };
}

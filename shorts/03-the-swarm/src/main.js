import { THREE, makeRenderer, makeCam, aim, clamp, prog, ease, W, H } from './core.js';
import { makeHive, TOWER, LAB } from './w_hive.js';
import { makeCore } from './w_core.js';
import { makeMap } from './w_map.js';

// ---------- camera path: centripetal-ish Catmull-Rom through timed keys ----------
// key: [t, [px,py,pz], [tx,ty,tz], fov, roll?]
function cr(p0, p1, p2, p3, u) { const u2 = u * u, u3 = u2 * u; return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u3); }
function path(keys) {
  return (t) => {
    if (t <= keys[0][0]) return keys[0]; const n = keys.length; if (t >= keys[n - 1][0]) return keys[n - 1];
    let i = 0; while (i < n - 2 && t > keys[i + 1][0]) i++;
    const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(n - 1, i + 2)];
    let u = (t - k1[0]) / (k2[0] - k1[0]);
    if (k2[5] === 'ease') { const e = ease.io(u), L = (a, b) => a + (b - a) * e; return [t, [0, 1, 2].map(j => L(k1[1][j], k2[1][j])), [0, 1, 2].map(j => L(k1[2][j], k2[2][j])), L(k1[3], k2[3]), L(k1[4] || 0, k2[4] || 0)]; }
    if (k2[5] === 'hold') u = ease.io(u);
    const f = (a) => [0, 1, 2].map(j => cr(k0[a][j], k1[a][j], k2[a][j], k3[a][j], u));
    return [t, f(1), f(2), cr(k0[3], k1[3], k2[3], k3[3], u), cr(k0[4] || 0, k1[4] || 0, k2[4] || 0, k3[4] || 0, u)];
  };
}

// ---------------- shots ----------------
const T = (x, y, z) => [x, y, z];
const SHOTS = [
  { id: 'hive-a', world: 'hive', t0: 0, t1: 47.75, cam: path([
    [0.0, T(0.35, 1.5, 8.6), T(0, 1.3, 0), 32], [2.9, T(0.12, 1.45, 7.9), T(0, 1.3, 0), 32],
    [3.9, T(0, 1.7, 12.3), T(0, 1.35, 0.4), 40], [4.6, T(-0.5, 1.65, 11.2), T(-0.5, 1.3, 0.5), 38],
    [7.3, T(-1.05, 1.6, 9.6), T(-0.75, 1.3, 0.6), 36], [8.3, T(1.0, 1.62, 9.8), T(0.75, 1.2, 0.6), 36],
    [11.0, T(1.15, 1.8, 10.2), T(0.6, 1.2, 0.5), 37], [12.3, T(0.5, 3.4, 16.5), T(0, 1.1, -3), 40],
    [13.5, T(0, 1.45, 8.4), T(0, 1.25, 0), 30], [14.3, T(0, 1.4, 10.4), T(0, 0.82, 0.8), 33],
    [18.3, T(0, 1.35, 9.4), T(0, 0.82, 0.8), 33], [19.5, T(0, 1.5, 9.6), T(0, 1.1, 0.6), 33],
    [23.6, T(0, 2.4, 12.5), T(0, 1.35, 0), 36], [26.0, T(0, 15, 30), T(0, 0, -22), 42],
    [30.4, T(9, 23, 34), T(0, 0, -40), 44], [32.3, T(4, 17, 24), T(0, 12, -150), 42],
    [34.0, T(0, 7.5, 14), T(0, 1.6, -6), 42], [35.6, T(0, 5, 16), T(0, 30, -48), 54], [37.6, T(2, 6, 14), T(0, 34, -50), 54],
    [39.3, T(0, 8, 12), T(0, 40, -52), 52], [41.8, T(0, 10, 7), T(0, 40, -52), 54],
    [42.9, T(-4.5, 2.7, 8.2), T(2.5, 1.35, -6), 44, 0, 'ease'], [44.5, T(-3, 2.9, 8), T(3, 1.6, -8), 44, 0, 'ease'], [45.3, T(-1.5, 2.4, 7.4), T(3.5, 6.5, -12), 48],
    [45.8, T(4.4, 1.75, 7.6), T(4.4, 1.3, 0), 38], [46.9, T(4.4, 1.6, 5.6), T(4.4, 0.9, 0), 42],
    [47.75, T(4.4, 1.2, 3.6), T(4.4, 0.2, 0), 50],
  ]) },
  { id: 'core-a', world: 'core', t0: 47.05, t1: 59.0, cam: null },     // filled by core world
  { id: 'hive-b', world: 'hive', t0: 58.55, t1: 66.2, cam: path([
    [58.55, T(0, 30, -18), T(0, 41, -52), 50], [59.8, T(0, 31, -22), T(0, 40.5, -52), 48], [61.0, T(0, 32, -24), T(0, 40, -52), 48],
    [62.4, T(33, 47, -36), T(0, 30, -170), 44], [63.6, T(24, 38, -82), T(0, 32, -170), 40], [64.7, T(8, 33, -114), T(0, 34, -166), 36], [66.2, T(3, 33, -132), T(0, 34, -164), 30],
  ]) },
  { id: 'hive-c', world: 'hive', t0: 65.95, t1: 75.6, cam: path([
    [65.95, T(-0.7, 1.55, TOWER.z + 22), T(-0.8, 2.25, TOWER.z + 10), 44], [67.15, T(-0.75, 1.55, TOWER.z + 20.5), T(-0.8, 2.2, TOWER.z + 10), 42],
    [67.55, T(1.4, 3.4, TOWER.z + 15.5), T(0, 1.3, TOWER.z + 55), 46], [69.6, T(2.6, 5.0, TOWER.z + 20), T(0, 1.6, TOWER.z + 60), 46],
    [70.7, T(15, 8, -140), T(0, 4, -158), 46], [73.4, T(30, 16, -124), T(0, 9, -158), 48],
    [74.6, T(52, 38, -96), T(0, 26, -160), 48], [75.6, T(56, 42, -92), T(0, 28, -158), 48],
  ]) },
  { id: 'hive-c2', world: 'hive', t0: 75.35, t1: 78.95, cam: path([
    [75.35, T(16, 46, -6), T(0, 40, -52), 52], [77.0, T(5, 39, -22), T(0, 40, -52), 44], [78.95, T(3.5, 38.5, -27), T(0, 40, -52), 40],
  ]) },
  { id: 'hive-d', world: 'hive', t0: 78.65, t1: 86.55, cam: path([
    [78.65, T(8, 4.2, -96), T(0, 1.4, -118), 42], [80.5, T(6, 3.6, -99), T(-0.5, 1.5, -116), 40],
    [81.6, T(1.6, 2.6, -101.5), T(-1.6, 1.85, -112), 36], [83.2, T(1.2, 2.7, -101.8), T(-1.6, 2.15, -112), 36],
    [85.9, T(0.9, 2.6, -102.6), T(-1.6, 2.0, -112), 36], [86.55, T(0.8, 3.0, -101.0), T(-1.6, 2.0, -110), 40],
  ]) },
  { id: 'hive-e', world: 'hive', t0: 86.3, t1: 88.75, cam: path([
    [86.3, T(16, 7, -86), T(0, 48, -172), 52], [88.75, T(14, 7.5, -90), T(0, 50, -172), 50],
  ]) },
  { id: 'hive-f', world: 'hive', t0: 88.5, t1: 91.85, cam: path([
    [88.5, T(-21, 6.2, -10), T(-46, 8.5, -64), 38], [91.85, T(-24, 6, -16), T(-46, 8.5, -64), 37],
  ]) },
  { id: 'map', world: 'map', t0: 91.45, t1: 96.85, cam: null },
  { id: 'core-b', world: 'core', t0: 96.4, t1: 110.2, cam: null },
];
// transitions at overlaps: [time, duration, mode, edgeColor]
const XF = { 'hive-a>core-a': [47.05, 0.6, 1], 'core-a>hive-b': [58.55, 0.45, 0, 0x7cc4ff], 'hive-b>hive-c': [65.95, 0.25, 0, 0xff7ac6], 'hive-c>hive-c2': [75.35, 0.25, 0, 0xffb547], 'hive-c2>hive-d': [78.65, 0.3, 0, 0xc8ff4d],
  'hive-d>hive-e': [86.3, 0.25, 0, 0xff6b6b], 'hive-e>hive-f': [88.5, 0.25, 0, 0x9aa3b5], 'hive-f>map': [91.45, 0.4, 0, 0xff6b6b], 'map>core-b': [96.4, 0.45, 0, 0xc8ff4d] };

let R, worlds = {}, cams = {}, labels = [];
function init(canvas, labelEls) {
  const lite = typeof window.__hfScriptState === 'function';
  R = makeRenderer(canvas, lite);
  worlds.hive = makeHive(R.env); worlds.core = makeCore(R.env); worlds.map = makeMap(R.env);
  SHOTS.forEach(s => { cams[s.id] = makeCam(36); if (!s.cam) s.cam = worlds[s.world].camFor(s.id); });
  labels = labelEls || [];
}
function shotAt(t) { let a = null; for (const s of SHOTS) if (t >= s.t0 && t < s.t1) { a = s; break; } return a || SHOTS[SHOTS.length - 1]; }
function setCam(s, t) { const c = cams[s.id]; const k = s.cam(t); c.fov = k[3]; c.updateProjectionMatrix(); aim(c, new THREE.Vector3(...k[1]), new THREE.Vector3(...k[2]), k[4] || 0); return c; }

const updated = new Set();
function upd(w, t) { if (updated.has(w)) return; worlds[w].update(t); updated.add(w); }
function render(t) {
  updated.clear();
  const A = shotAt(t); const ia = SHOTS.indexOf(A); const B = SHOTS[ia + 1];
  let p = 0, mode = 0, edge = 0xc8ff4d;
  const x = B && XF[A.id + '>' + B.id];
  if (x && t >= x[0]) { p = clamp((t - x[0]) / x[1]); mode = x[2]; if (x[3] !== undefined) edge = x[3]; }
  upd(A.world, t); const ca = setCam(A, t);
  R.dual.A = { scene: worlds[A.world].scene, cam: ca }; R.dual.B = null; R.dual.p = 0; R.dual.mode = mode;
  if (p > 0 && B) { upd(B.world, t); const cb = setCam(B, t); R.dual.B = { scene: worlds[B.world].scene, cam: cb }; R.dual.p = p; R.dual.mat.uniforms.edge.value.set(edge).multiplyScalar(1.4); }
  R.bloom.strength = t < 19.6 ? 0.42 : 0.72;
  R.comp.render();
  // pin HTML labels to world points
  labels.forEach((L) => {
    const el = L.el; const on = t >= L.t0 && t <= L.t1; if (!on) { el.style.opacity = 0; return; }
    const s = (p > 0.5 && B) ? B : A; if (s.world !== L.world) { el.style.opacity = 0; return; }
    const c = cams[s.id]; const v = new THREE.Vector3(...L.at).project(c);
    const sx = (v.x * 0.5 + 0.5) * W, sy = (-v.y * 0.5 + 0.5) * H;
    const vis = v.z < 1 && sx > 40 && sx < W - 40 && sy > 220 && sy < 1200;
    el.style.transform = `translate(${sx.toFixed(1)}px, ${sy.toFixed(1)}px) translate(-50%, -100%)`;
    const fade = Math.min(prog(t, L.t0, L.t0 + 0.35), 1 - prog(t, L.t1 - 0.3, L.t1));
    el.style.opacity = vis ? fade : 0;
  });
}
window.SWARM = { init, render, TOWER: TOWER.toArray(), LAB: LAB.toArray() };

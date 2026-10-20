import { THREE, makeRenderer, makeCam, aim, clamp, prog, ease, W, H } from './core.js';
import { makeGallery } from './w_gallery.js';
import { makePaint } from './w_paint.js';
import { makeBoard } from './w_board.js';
import { makeHill } from './w_hill.js';
import { makeMap } from './w_map.js';
import { makePhoto } from './w_photo.js';
import { makeDC } from './w_dc.js';
import { makeBridge } from './w_bridge.js';

// camera path: Catmull-Rom through timed keys [t, pos, target, fov, roll?, flag?]; 'ease' = straight eased segment
function cr(p0, p1, p2, p3, u) { const u2 = u * u, u3 = u2 * u; return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u3); }
function path(keys) {
  return (t) => {
    if (t <= keys[0][0]) return keys[0]; const n = keys.length; if (t >= keys[n - 1][0]) return keys[n - 1];
    let i = 0; while (i < n - 2 && t > keys[i + 1][0]) i++;
    const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(n - 1, i + 2)];
    let u = (t - k1[0]) / (k2[0] - k1[0]);
    if (k2[5] === 'ease') { const e = ease.io(u), L = (a, b) => a + (b - a) * e; return [t, [0, 1, 2].map(j => L(k1[1][j], k2[1][j])), [0, 1, 2].map(j => L(k1[2][j], k2[2][j])), L(k1[3], k2[3]), L(k1[4] || 0, k2[4] || 0)]; }
    const f = (a) => [0, 1, 2].map(j => cr(k0[a][j], k1[a][j], k2[a][j], k3[a][j], u));
    return [t, f(1), f(2), cr(k0[3], k1[3], k2[3], k3[3], u), cr(k0[4] || 0, k1[4] || 0, k2[4] || 0, k3[4] || 0, u)];
  };
}

const SHOTS = [
  { id: 'gal-a', world: 'gallery', t0: 0, t1: 5.35 },
  { id: 'paint', world: 'paint', t0: 4.95, t1: 10.45 },
  { id: 'board', world: 'board', t0: 10.05, t1: 15.85 },
  { id: 'hill-a', world: 'hill', t0: 15.55, t1: 20.45 },
  { id: 'map', world: 'map', t0: 20.05, t1: 28.5 },
  { id: 'wheel', world: 'photo', t0: 28.15, t1: 30.4 },
  { id: 'hill-b', world: 'hill', t0: 30.05, t1: 34.15 },
  { id: 'gal-b', world: 'gallery', t0: 33.85, t1: 38.5 },
  { id: 'via', world: 'photo', t0: 38.15, t1: 41.45 },
  { id: 'desk', world: 'photo', t0: 41.05, t1: 45.4 },
  { id: 'dc', world: 'dc', t0: 44.95, t1: 60.85 },
  { id: 'bridge', world: 'bridge', t0: 60.35, t1: 90 },
];
// transitions at overlaps: [time, duration, mode (0 burn / 1 zoom-through), edge colour]
const XF = {
  'gal-a>paint': [4.95, 0.4, 1], 'paint>board': [10.05, 0.38, 0, 0xffb547], 'board>hill-a': [15.55, 0.32, 0, 0xc8ff4d], 'hill-a>map': [20.05, 0.4, 1],
  'map>wheel': [28.15, 0.32, 0, 0xffb547], 'wheel>hill-b': [30.05, 0.3, 0, 0xe8e2d4], 'hill-b>gal-b': [33.85, 0.3, 0, 0xff6b6b], 'gal-b>via': [38.15, 0.38, 0, 0xffc861],
  'via>desk': [41.05, 0.35, 0, 0xffb547], 'desk>dc': [44.95, 0.45, 1], 'dc>bridge': [60.35, 0.5, 0, 0xffc861],
};
const SHAKE = [[9.3, 10.4, 0.05], [32.84, 33.9, 0.09], [36.69, 37.0, 0.025], [71.62, 71.9, 0.02]];
const BLOOM = (t) => t < 5 ? 0.5 : t < 10.5 ? 0.85 : t < 45 ? 0.6 : t < 60.4 ? 0.8 : 0.7;

let R, worlds = {}, cams = {}, paths = {}, labels = [];
function init(canvas, IMG, labelEls) {
  const lite = typeof window.__hfScriptState === 'function';
  R = makeRenderer(canvas, lite);
  worlds.gallery = makeGallery(R.env, IMG); worlds.paint = makePaint(R.env, IMG); worlds.board = makeBoard(R.env, IMG); worlds.hill = makeHill(R.env);
  worlds.map = makeMap(R.env); worlds.photo = makePhoto(R.env, IMG); worlds.dc = makeDC(R.env, IMG); worlds.bridge = makeBridge(R.env, IMG);
  const dcKeys = [...worlds.dc.cams['dc-a'], ...worlds.dc.cams['dc-b'].slice(1), ...worlds.dc.cams['dc-c'].slice(1)];
  SHOTS.forEach((s) => { cams[s.id] = makeCam(36); const ks = s.id === 'dc' ? dcKeys : worlds[s.world].cams[s.id]; paths[s.id] = path(ks); });
  labels = labelEls || [];
  window.SIXT.pts = { beacon: worlds.bridge.pts.beacon.toArray(), best: worlds.bridge.pts.best.toArray(), gap: worlds.bridge.pts.gap.toArray() };
}
function shotAt(t) { for (const s of SHOTS) if (t >= s.t0 && t < s.t1) return s; return SHOTS[SHOTS.length - 1]; }
function shake(t) { let a = 0; for (const [t0, t1, amp] of SHAKE) if (t >= t0 && t <= t1) a = Math.max(a, amp * (1 - (t - t0) / (t1 - t0))); return a; }
function setCam(s, t) {
  const c = cams[s.id]; const k = paths[s.id](t); c.fov = k[3]; c.updateProjectionMatrix();
  const a = shake(t); const pos = new THREE.Vector3(...k[1]), tg = new THREE.Vector3(...k[2]);
  if (a > 0) { const d = pos.distanceTo(tg); const j = new THREE.Vector3(Math.sin(t * 71.3), Math.sin(t * 53.9 + 1), Math.sin(t * 61.1 + 2)).multiplyScalar(a * d * 0.25); tg.add(j); pos.add(j.multiplyScalar(0.5)); }
  aim(c, pos, tg, k[4] || 0); return c;
}
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
  R.bloom.strength = BLOOM(t);
  R.comp.render();
  labels.forEach((L) => {
    const el = L.el; const on = t >= L.t0 && t <= L.t1; if (!on) { el.style.opacity = 0; return; }
    const s = (p > 0.5 && B) ? B : A; if (s.world !== L.world) { el.style.opacity = 0; return; }
    const v = new THREE.Vector3(...L.at).project(cams[s.id]);
    const sx = (v.x * 0.5 + 0.5) * W, sy = (-v.y * 0.5 + 0.5) * H;
    const vis = v.z < 1 && sx > 60 && sx < W - 60 && sy > 300 && sy < 1200;
    el.style.transform = `translate(${sx.toFixed(1)}px, ${sy.toFixed(1)}px) translate(-50%, -100%)`;
    el.style.opacity = vis ? Math.min(prog(t, L.t0, L.t0 + 0.35), 1 - prog(t, L.t1 - 0.3, L.t1)) : 0;
  });
}
window.SIXT = { init, render, setLabels: (l) => { labels = l || []; } };

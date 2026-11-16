// film19.js: Short #19 "Ten minutes", drawn in Lemo-Opuscar's Mid-century Cartoon style (toon19.js).
// Everything visual except the captions and the end card is one 1080x1920 canvas, repainted from the clock alone
// (seek-safe: no state carries between frames). Times come from the take's words (WS, WE).
const CV = document.getElementById("film"), X = CV.getContext("2d");
const W = 1080, H = 1920;
const P0 = PAL;
const C = { paper: "#F4EAD5", paperD: "#E6D8BC", paperDD: "#D4C29F", ink: "#2B2420", inkSoft: "#4A3F38", white: "#FBF6EA",
  mustard: "#E8B43A", mustardD: "#C08A1E", mustardL: "#F3D37F", teal: "#3FA7A0", tealD: "#257A74", tealL: "#8ACFC6",
  tomato: "#E0533A", tomatoD: "#B23A26", tomatoL: "#F09A86", olive: "#A7AE5B", oliveD: "#7E8538", oliveL: "#CBD08E",
  blue: "#7F9CC0", blueD: "#5B789E", blueL: "#B5C8DE", pink: "#F0B4A8", pinkD: "#D98F82", chrome: "#C9CFCB", chromeD: "#8E9894",
  kraft: "#DDB47F", kraftD: "#A2713F", graphite: "#4A4542" };
const SLAB = (px) => `${px}px "Alfa Slab One"`, SCRIPT = (px) => `700 ${px}px "Oleo Script"`, SANS = (px, wt) => `${wt || 600} ${px}px "Jost"`;
const T_ = {
  twice: w(9), pic: w(12), train: w(17), over: w(19), thousand: w(21), math: w(24), about: w(25), half: w(26),
  then: w(30), warning: w(32), off: w(36), alone: w(37), fewer: w(40), and1: w(48), skip: w(51), twice2: w(53),
  reading: w(56), no: w(58), one: w(60), after: w(65), eight: w(67), res: w(68), instant: w(75), so: w(77), balance: w(82),
  heres: w(83), weird: w(85), people: w(87), hints: w(92), did: w(93), the2: w(102), catchw: w(103), short: w(104), tests: w(105),
  and2: w(106), clue: w(112), proof: w(114), so2: w(115), hint: w(121), answer: w(125), like: w(126), hand: w(128),
  seat: w(132), lets: w(134), go: w(135), theres: w(136), never: w(143), spotted: w(147), comment: w(149), follow: w(151),
  andr: w(158), remember: w(159), was: w(163), gaveup: w(6)
};
const CH_T = [0, T_.alone, T_.res, T_.heres, T_.so2];      // chapter starts: WHEELS WOBBLE WHY HINTS TRY IT
const CH_N = ["WHEELS", "WOBBLE", "WHY", "HINTS", "TRY IT"];
const MIRROR = T_.follow + 0.4;                             // the stage resets to frame one under the end card, once it is opaque

// ---------- small helpers ----------
function track(T, K, f) { f = f || eio; if (T <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const a = K[i - 1], b = K[i]; return lerp(a[1], b[1], f(seg(T, a[0], b[0]))); }
  return K[K.length - 1][1]; }
const win = (T, a, b) => T >= a && T < b;
const pop = (T, t0, d) => back(seg(T, t0, t0 + (d || 0.3)), 2.2);       // back-ease pop-in 0..1(+overshoot)
function ik(a, b, l1, l2, bend) {                                       // 2-bone IK: elbow/knee point
  const dx = b[0] - a[0], dy = b[1] - a[1], d = Math.min(Math.hypot(dx, dy), l1 + l2 - 0.01);
  const A = Math.atan2(dy, dx), k = Math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1));
  return [a[0] + Math.cos(A + bend * k) * l1, a[1] + Math.sin(A + bend * k) * l1]; }
const circ = (cx, cy, r, n) => ellipse(cx, cy, r, r, n || 40);

// ---------- the road: one scroll position for the whole short (integrated speed, looped at the end) ----------
const SPOKE = 2 * Math.PI * 95 / 8, LOOP = 12 * SPOKE;      // wheel r 95, 8 spokes; road period: medallions 3 spokes, cranks 4
const MED = 3 * SPOKE;
const SPEED = [[0, 170], [T_.then, 170], [T_.then + 0.25, 0], [T_.off, 0], [T_.off + 0.7, 110], [T_.res, 110], [T_.res + 0.4, 160],
  [T_.weird, 160], [T_.weird + 0.12, 0], [T_.people, 0], [T_.people + 0.5, 130], [T_.so2, 130], [T_.so2 + 0.3, 100], [T_.like, 100],
  [T_.like + 0.4, 150], [T_.theres, 150], [T_.theres + 0.5, 90], [MIRROR, 90], [MIRROR + 0.4, 170], [DUR, 170]];
const POS = (() => { const dt = 1 / 240, n = Math.ceil(DUR / dt) + 2, p = new Float64Array(n); let s = 0;
  for (let i = 1; i < n; i++) { s += track((i - 0.5) * dt, SPEED, (u) => u) * dt; p[i] = s; }
  // stretch the last stretch (from the mirror) so the road ends exactly where it started, modulo one period
  const iM = Math.round(MIRROR / dt), iE = Math.round(DUR / dt), need = Math.ceil(p[iE] / LOOP) * LOOP;
  const k = (need - p[iM]) / (p[iE] - p[iM]);
  for (let i = iM + 1; i < n; i++) p[i] = p[iM] + (p[i] - p[iM]) * k;
  return { dt, p }; })();
const pos = (T) => { const i = clamp(T / POS.dt, 0, POS.p.length - 2), a = Math.floor(i); return lerp(POS.p[a], POS.p[a + 1], i - a); };
const posInv = (v) => { let lo = 0, hi = POS.p.length - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (POS.p[m] < v) lo = m; else hi = m; } return lo * POS.dt; };

// ---------- states of the stage over time ----------
const twScale = (T) => {                                     // our training wheels: 1 on, 0 off
  if (T < T_.off) return 1;
  if (T < T_.res + 0.3) return 0;
  if (T < T_.people + 0.1) return back(seg(T, T_.res + 0.3, T_.res + 0.6), 2);
  if (T < MIRROR) return 0;
  return 1; };
const wobbleA = (T) => (T >= MIRROR ? 0 : track(T, [[T_.off, 0], [T_.off + 0.4, 0.07], [T_.res, 0.07], [T_.res + 0.3, 0], [T_.weird, 0]]));
const expr = (T) => {
  if (T >= MIRROR) return "happy";
  if (T < T_.gaveup) return "happy";
  if (T < T_.pic) return "worried";
  if (T < T_.then) return "happy";
  if (T < T_.res) return "worried";
  if (T < T_.heres) return "happy";
  if (T < T_.people) return "look";
  if (T < T_.go) return "focus";
  return "happy"; };
// kitchen timer: minutes on the dial (10 at frame one; runs out as the ten minutes pass; rewinds for WHY and at the end)
const timerMin = (T) => {
  if (T < T_.then) return lerp(10, 0, ss(seg(T, 0.4, T_.then)));
  if (T < T_.res) return 0;
  if (T < T_.res + 0.45) return lerp(0, 10, eo(seg(T, T_.res, T_.res + 0.45)));
  if (T < T_.people) return lerp(10, 0, seg(T, T_.res + 0.45, T_.people));
  if (T < T_.remember + 0.05) return 0;
  return lerp(0, 10, eio(seg(T, T_.remember + 0.05, T_.remember + 0.7))); };

// ---------- camera: screen = (p - A) * s + B (rotation r about B) ----------
const CAM = { hook: [0.86, 540, 700, 540, 640], board: [1, 540, 700, 540, 700], split: [0.6, 540, 700, 540, 600],
  zoom: [1.13, 420, 900, 330, 930], crowd: [0.27, 540, 1080, 540, 720] };
function camAt(T) {
  const K = [[0, "hook"], [T_.pic - 0.05, "hook"], [T_.pic + 0.15, "zoom"], [T_.over - 0.3, "zoom"], [T_.over + 0.75, "crowd"],
    [T_.then, "crowd"], [T_.then + 0.55, "board"], [T_.alone, "board"], [T_.alone + 0.45, "split"], [T_.res - 0.25, "split"],
    [T_.res + 0.2, "board"], [T_.did + 0.4, "board"], [T_.did + 0.85, "split"], [T_.like - 0.2, "split"], [T_.like + 0.25, "board"],
    [MIRROR - 0.01, "board"], [MIRROR, "hook"], [DUR, "hook"]];
  let i = 1; while (i < K.length - 1 && T > K[i][0]) i++;
  const a = K[i - 1], b = K[i], u = (a[1] === b[1]) ? 0 : (b[1] === "zoom" || a[1] === "zoom" && b[0] - a[0] < 0.3 ? eo : eio)(seg(T, a[0], b[0]));
  const A = CAM[a[1]], B = CAM[b[1]], c = A.map((v, j) => lerp(v, B[j], u));
  // the crowd pull-back counter-rotates; the recap and the hook push a few percent
  let rot = 0; if (T > T_.over && T < T_.over + 0.75) rot = -0.12 * (1 - eio(seg(T, T_.over, T_.over + 0.75)));
  if (T > T_.theres && T < MIRROR) c[0] *= 1 + 0.03 * ss(seg(T, T_.theres, MIRROR));
  if (T > T_.off && T < T_.off + 0.22) c[0] *= 1 + 0.04 * Math.sin(Math.PI * seg(T, T_.off, T_.off + 0.22));      // punch on OFF
  if (T < T_.pic - 0.05) c[0] *= 1 + 0.025 * ss(seg(T, 0, T_.pic));
  return { s: c[0], ax: c[1], ay: c[2], bx: c[3], by: c[4], rot }; }
function applyCam(cam) { X.translate(cam.bx, cam.by); if (cam.rot) X.rotate(cam.rot); X.scale(cam.s, cam.s); X.translate(-cam.ax, -cam.ay); }

// =============================================== drawing: the rider ===============================================
const G = { y: 1000, R: [400, 905], F: [700, 905], BB: [525, 915], S: [470, 770], HD: [655, 760], HB: [632, 716], TW: [322, 962] };
function wheel(cx, cy, r, rot, o) {
  o = o || {};
  shape(X, circ(cx, cy, r, 44), { fill: null, line: o.tyre || 9, seed: o.seed || 3, breaks: 0.08 });
  ink(X, circ(cx, cy, r - 7, 40), 3, { closed: true, color: C.inkSoft, seed: (o.seed || 3) + 1, breaks: 0.2 });
  const n = o.spokes || 8;
  for (let i = 0; i < n; i++) { const a = rot + i * TAU / n;
    ink(X, [[cx + Math.cos(a) * 10, cy + Math.sin(a) * 10], [cx + Math.cos(a) * (r - 9), cy + Math.sin(a) * (r - 9)]], 2.2, { color: C.inkSoft, seed: 40 + i, taper: false, wob: 0.1 }); }
  shape(X, circ(cx, cy, 11, 16), { fill: o.hub || C.chrome, line: 3, seed: (o.seed || 3) + 2, breaks: 0 }); }
function tube(a, b, col, seed) {
  ink(X, [a, b], 17, { seed, taper: false, wob: 0.06 });
  const o = reg(seed, 0.6); ink(X, move([a, b], o[0], o[1]), 10, { seed: seed + 1, taper: false, wob: 0.04, color: col }); }
// the AI's training wheel: turquoise tyre, its hub a chat bubble with typing dots
function trainingWheel(cx, cy, r, rot, T, alpha) {
  X.save(); X.globalAlpha *= alpha;
  shape(X, circ(cx, cy, r, 32), { fill: C.tealL, line: 0, grain: 0.2 });
  shape(X, circ(cx, cy, r, 32), { fill: null, line: 7, seed: 61 });
  ink(X, circ(cx, cy, r - 5, 28), 5, { closed: true, color: C.teal, seed: 62, breaks: 0 });
  for (let i = 0; i < 4; i++) { const a = rot + i * TAU / 4;
    ink(X, [[cx + Math.cos(a) * r * 0.42, cy + Math.sin(a) * r * 0.42], [cx + Math.cos(a) * (r - 6), cy + Math.sin(a) * (r - 6)]], 2, { color: C.tealD, seed: 70 + i, taper: false }); }
  bubble(cx, cy, r * 0.5, T, C.white, 1);
  X.restore(); }
function bubble(cx, cy, r, T, fill, dots) {              // a round chat bubble with a tail and three typing dots
  const pts = [...ellipse(cx, cy, r, r * 0.8, 24, -2.4, 3.6)];
  pts.push([cx - r * 0.75, cy + r * 0.95]);
  shape(X, pts, { fill: fill || C.white, line: Math.max(2, r * 0.12), seed: 81, breaks: 0.05, grain: 0.15, regK: Math.min(1, r / 40) });
  if (dots) for (let i = 0; i < 3; i++) { const ph = Math.sin(T * 7 - i * 0.9) * 0.5 + 0.5;
    shape(X, circ(cx + (i - 1) * r * 0.42, cy - ph * r * 0.12, r * 0.13, 10), { fill: C.ink, line: 0, grain: 0, off: [0, 0] }); } }
function gloveAt(x, y, a, kind, side, k) { drawHand(X, x, y, a, kind, side, k || 1, C.white); }

function face(cx, cy, ex, T) {
  const look = ex === "look" ? [0, 2] : ex === "focus" ? [5, 1] : [3, 0];
  const blink = (T % 3.7) > 3.58 ? 0.15 : 1;
  for (const s of [-1, 1]) {
    const x = cx + s * 22, y = cy;
    shape(X, ellipse(x, y, 13, 17 * blink, 18), { fill: C.white, line: 3, seed: 90 + s, breaks: 0, regK: 0.4 });
    if (blink > 0.5) shape(X, circ(x + look[0], y + 2 + look[1], ex === "look" ? 7.5 : 6, 12), { fill: C.ink, line: 0, grain: 0, off: [0, 0] });
    if (ex === "worried") ink(X, [[x - 13, y - 22 - s * 4], [x + 13, y - 22 + s * 4]], 3.5, { seed: 95 + s });
    else ink(X, [[x - 11, y - 25], [x + 11, y - 27]], 3, { seed: 95 + s });
  }
  const my = cy + 46;
  if (ex === "happy") ink(X, spline([[cx - 20, my - 4], [cx, my + 9], [cx + 20, my - 4]], false, 8), 4, { seed: 97 });
  else if (ex === "worried") ink(X, spline([[cx - 16, my + 4], [cx - 5, my - 3], [cx + 6, my + 3], [cx + 16, my - 2]], false, 8), 3.6, { seed: 98 });
  else if (ex === "look") shape(X, ellipse(cx, my + 2, 8, 10, 16), { fill: C.tomatoD, line: 3, seed: 99, breaks: 0 });
  else ink(X, [[cx - 12, my + 1], [cx + 12, my]], 3.6, { seed: 99 }); }

// the hero: a mustard pencil (GRIT on its barrel) riding in place; o.tw training wheel scale, o.lean, o.p road pos
function rider(T, o) {
  const p = o.p, rot = p / 95, ph = p / 95;                          // wheel turn; crank follows the wheel
  const lean = 0.07 + (o.lean || 0);
  // far training wheel (behind), then far leg, wheels, frame, near leg, pencil, arms
  const tw = o.tw ?? 1, twx = o.twx || 0, twy = o.twy || 0, twr = o.twr || 0, twa = o.twa ?? 1;
  if (o.stub) { const e = [lerp(G.R[0], G.TW[0], 0.45), lerp(G.R[1], G.TW[1], 0.45)]; ink(X, [G.R, e], 7, { seed: 56 }); }
  if (tw > 0.01 && !o.stub) {
    const bx = G.R[0], by = G.R[1];
    ink(X, [[bx, by], [G.TW[0] + 20 + twx * 0.2, G.TW[1] - 8 + twy * 0.2]], 6, { seed: 55, alpha: twa });
    trainingWheel(G.TW[0] + 16 + twx, G.TW[1] - 6 + twy, 38 * tw, p / 38 + twr, T, 0.55 * twa);
  }
  const cr = [G.BB[0] + Math.cos(ph) * 38, G.BB[1] + Math.sin(ph) * 38], cr2 = [G.BB[0] - Math.cos(ph) * 38, G.BB[1] - Math.sin(ph) * 38];
  // pencil frame of reference: rotate about the seat
  const S = G.S, cx = S[0], rotP = (pt) => { const dx = pt[0] - S[0], dy = pt[1] - S[1], c = Math.cos(lean), s = Math.sin(lean); return [S[0] + dx * c - dy * s, S[1] + dx * s + dy * c]; };
  const hipF = rotP([cx - 12, 730]), hipN = rotP([cx + 14, 730]);
  const leg = (hip, ped, seed, col) => { const knee = ik(hip, ped, 112, 108, -1);
    ink(X, [hip, knee, ped], 9, { seed, taper: false, wob: 0.1, color: col }); shape(X, ellipse(ped[0] + 10, ped[1] + 4, 22, 11, 14), { fill: C.tomatoD, line: 3, seed: seed + 3, breaks: 0 }); };
  leg(hipF, cr2, 101, C.inkSoft);
  wheel(G.R[0], G.R[1], 95, rot, { seed: 11 });
  wheel(G.F[0], G.F[1], 95, rot, { seed: 13 });
  tube(G.R, G.BB, C.blue, 21); tube(G.R, G.S, C.blue, 23); tube(G.S, G.BB, C.blue, 25); tube(G.S, G.HD, C.blue, 27); tube(G.BB, G.HD, C.blue, 29); tube(G.HD, G.F, C.blue, 31);
  ink(X, [G.HD, G.HB], 10, { seed: 33 }); ink(X, [[G.HB[0] - 34, G.HB[1] - 6], [G.HB[0] + 10, G.HB[1] + 2]], 11, { seed: 34 });
  shape(X, rrect(S[0] - 40, S[1] - 6, 70, 18, 8), { fill: C.ink, line: 0, grain: 0, off: [0, 0] });
  shape(X, circ(G.BB[0], G.BB[1], 18, 18), { fill: C.chromeD, line: 3, seed: 35 });
  ink(X, [G.BB, cr], 6, { seed: 36 }); ink(X, [G.BB, cr2], 6, { seed: 37 });
  if (tw > 0.01) { const bx = G.R[0], by = G.R[1];
    if (!o.stub) ink(X, [[bx, by], [G.TW[0] + twx * 0.2, G.TW[1] + twy * 0.2]], 7, { seed: 56, alpha: twa });
    trainingWheel(G.TW[0] + twx, G.TW[1] + twy, 38 * tw, (o.stub ? 0 : p / 38) + twr, T, twa); }
  // far arm first, so the barrel covers it
  const shF = rotP([cx - 40, 606]), gripF = [G.HB[0] - 26, G.HB[1] - 8], elF = ik(shF, gripF, 88, 88, 1);
  ink(X, [shF, elF, gripF], 9, { seed: 131, taper: false, color: C.inkSoft });
  // the pencil
  X.save(); X.translate(S[0], S[1]); X.rotate(lean); X.translate(-S[0], -S[1]);
  const bx0 = cx - 58, bx1 = cx + 58, top = 452, bot = 722;
  shape(X, [[bx0, top], [bx1, top], [bx1, bot], [cx + 30, bot + 38], [cx + 10, 770], [cx - 10, 770], [cx - 30, bot + 38], [bx0, bot]], { fill: C.kraft, line: 0, seed: 111, grain: 0.3 });
  shape(X, [[cx - 12, 760], [cx + 12, 760], [cx, 782]], { fill: C.graphite, line: 3, seed: 112, breaks: 0 });
  shape(X, rect(bx0, top, 116, bot - top), { fill: C.mustard, line: 0, seed: 113, grain: 0.3,
    shade: [{ pts: rect(bx0, top, 34, bot - top), color: C.mustardL, alpha: 0.9 }, { pts: rect(bx1 - 34, top, 34, bot - top), color: C.mustardD, alpha: 0.8 }] });
  // wood cone scallops
  ink(X, spline([[bx0, bot], [cx - 38, bot + 14], [cx - 19, bot + 2], [cx, bot + 16], [cx + 19, bot + 2], [cx + 38, bot + 14], [bx1, bot]], false, 6), 3.5, { seed: 114 });
  ink(X, [[bx0, top], [bx0, bot], [cx - 30, bot + 38], [cx - 12, 762]], 4.5, { seed: 115, taper: false });
  ink(X, [[bx1, top], [bx1, bot], [cx + 30, bot + 38], [cx + 12, 762]], 4.5, { seed: 116, taper: false });
  ink(X, [[bx0 + 34, top + 6], [bx0 + 34, bot - 4]], 2.4, { seed: 117, color: C.mustardD, taper: true });
  ink(X, [[bx1 - 34, top + 6], [bx1 - 34, bot - 4]], 2.4, { seed: 118, color: C.mustardD, taper: true });
  // ferrule and eraser
  shape(X, rect(bx0 - 2, top - 30, 120, 30), { fill: C.chrome, line: 4, seed: 119, breaks: 0.05,
    shade: [{ pts: rect(bx0 - 2, top - 20, 120, 6), color: C.chromeD, alpha: 0.9 }, { pts: rect(bx0 - 2, top - 9, 120, 5), color: C.chromeD, alpha: 0.9 }] });
  shape(X, rrect(bx0 + 2, top - 84, 112, 58, 24), { fill: C.pink, line: 4.5, seed: 120, shade: [{ pts: rect(bx1 - 30, top - 84, 30, 58), color: C.pinkD, alpha: 0.7 }] });
  // GRIT on the barrel (the hidden word, never said)
  text(X, "GRIT", cx, 690, { font: SLAB(36), fill: C.ink, plate: C.mustardD, align: "center", maxW: 100, track: 2, seed: 121 });
  face(cx, 528, o.ex || "happy", T);
  X.restore();
  // arms: shoulders on the barrel, gloves on the bars (or o.arm overrides the near hand)
  const shN = rotP([cx + 44, 612]);
  const gripN = o.reach || [G.HB[0] - 4, G.HB[1] - 2];
  const elN = ik(shN, gripN, 88, 88, 1);
  gloveAt(gripF[0], gripF[1], -0.2, "grip", 1, 0.95);
  leg(hipN, cr, 103, C.ink);
  ink(X, [shN, elN, gripN], 9, { seed: 133, taper: false });
  gloveAt(gripN[0], gripN[1], o.reachA ?? -0.15, o.handKind || "grip", -1, 1.05);
  if (o.level) spiritLevel(o.level, T);
  if (o.card) o.card(); }

function spiritLevel(u, T) {           // a level on the top tube: the bubble never leaves the middle
  const x = 700, y = 676;
  X.save(); X.translate(x, y); X.scale(u * 1.15, u * 1.15);
  shape(X, rrect(-70, -22, 140, 30, 12), { fill: C.mustardL, line: 4, seed: 141 });
  shape(X, rrect(-34, -18, 68, 20, 9), { fill: C.tealL, line: 3, seed: 142, breaks: 0 });
  shape(X, ellipse(0, -8, 12, 7, 14), { fill: C.white, line: 2.5, seed: 143, breaks: 0 });
  ink(X, [[-16, -18], [-16, 2]], 2.4, { seed: 144 }); ink(X, [[16, -18], [16, 2]], 2.4, { seed: 145 });
  X.restore(); }

// =============================================== drawing: the stage ===============================================
function medallion(x, y, r, label, mark, k) {
  shape(X, circ(x, y, r, 28), { fill: C.white, line: 3.5, seed: 151 + (label.length), breaks: 0.1 });
  text(X, label, x, y + r * 0.3, { font: SLAB(Math.round(r * 0.75)), fill: C.ink, align: "center", seed: 152 });
  if (mark && k > 0) { const s = 1 + (1 - eo(k)) * 0.8;
    X.save(); X.translate(x + r * 0.55, y - r * 0.55); X.scale(s, s); X.globalAlpha *= clamp(k * 3);
    if (mark === "check") { shape(X, circ(0, 0, r * 0.55, 16), { fill: C.mustard, line: 3, seed: 153, breaks: 0 });
      ink(X, [[-r * 0.25, 0], [-r * 0.05, r * 0.2], [r * 0.3, -r * 0.25]], 4, { seed: 154 }); }
    else if (mark === "skip") { shape(X, rrect(-r * 0.75, -r * 0.32, r * 1.5, r * 0.64, 6), { fill: C.tomato, line: 3, seed: 155, breaks: 0 });
      text(X, "SKIP", 0, r * 0.17, { font: SANS(Math.round(r * 0.42), 700), fill: C.white, align: "center" }); }
    X.restore(); } }
const FRAC = ["3/4", "1/8", "2/3", "5/6", "1/2", "7/8", "3/5", "4/9"];
function medMark(i, tc) {
  if (tc < T_.off || (tc >= T_.res && tc < T_.weird) || tc >= T_.people) return "check";
  if (tc < T_.res) return ["skip", null, "check"][((i % 3) + 3) % 3];
  return null; }
function floor(T, p, x0, x1, y, rowSeed, withMeds) {
  plane(X, rect(x0, y, x1 - x0, 120), C.paperD);
  for (const ly of [26, 52, 78, 104]) ink(X, [[x0, y + ly], [x1, y + ly]], 2, { color: C.blueL, seed: rowSeed + ly, taper: false, wob: 0.05 });
  ink(X, [[x0, y], [x1, y]], 4.5, { seed: rowSeed, breaks: 0.15, taper: false });
  // ruler ticks scroll with the road (period = one spoke, so the loop is seamless)
  const ph = ((p % SPOKE) + SPOKE) % SPOKE;
  for (let x = x0 - ph + SPOKE; x < x1; x += SPOKE) ink(X, [[x, y + 2], [x, y + 16]], 3, { seed: 7, taper: false });
  if (!withMeds) return;
  const i0 = Math.floor((p + x0 - 900) / MED) - 1, i1 = Math.ceil((p + x1 - 900) / MED) + 1;
  for (let i = i0; i <= i1; i++) {
    const x = 900 + i * MED - p; if (x < x0 - 40 || x > x1 + 40) continue;
    const tc = posInv(900 + i * MED - 430), mark = (T >= tc) ? medMark(i, tc) : null;
    const k = mark ? seg(T, tc, tc + 0.25) : 0;
    const bump = withMeds === 2 ? 1 + 0.25 * Math.sin(Math.PI * seg(T, T_.math + (x - 400) / 3000, T_.math + 0.3 + (x - 400) / 3000)) : 1;
    medallion(x, y + 64, 30 * bump, FRAC[((i % 8) + 8) % 8], mark, k); } }
function timer(cx, cy, mins, T, shake) {
  X.save(); X.translate(cx, cy); X.rotate(shake ? Math.sin(T * 60) * 0.06 * shake : 0);
  shape(X, rrect(-14, -80, 28, 22, 6), { fill: C.chrome, line: 3, seed: 161 });
  shape(X, circ(0, 0, 66, 36), { fill: C.blue, line: 5, seed: 162, shade: [{ pts: ellipse(14, 12, 60, 60, 30), color: C.blueD, alpha: 0.35 }] });
  shape(X, circ(0, 0, 50, 32), { fill: C.white, line: 3, seed: 163, breaks: 0.05 });
  for (let m = 0; m < 12; m++) { const a = -Math.PI / 2 + m * TAU / 12, r0 = m % 3 === 0 ? 36 : 41;
    ink(X, [[Math.cos(a) * r0, Math.sin(a) * r0], [Math.cos(a) * 46, Math.sin(a) * 46]], m % 3 === 0 ? 3 : 2, { seed: 170 + m, taper: false }); }
  // the red "time left" wedge and the hand
  if (mins > 0.05) { X.save(); X.globalAlpha *= 0.85; X.fillStyle = C.tomatoL; X.beginPath(); X.moveTo(0, 0);
    X.arc(0, 0, 34, -Math.PI / 2, -Math.PI / 2 + mins / 60 * TAU); X.closePath(); X.fill(); X.restore(); }
  text(X, String(Math.ceil(mins - 0.02)), 0, 32, { font: SLAB(22), fill: C.ink, align: "center" });
  const a = -Math.PI / 2 + mins / 60 * TAU;
  ink(X, [[0, 0], [Math.cos(a) * 40, Math.sin(a) * 40]], 5, { seed: 181 });
  shape(X, circ(0, 0, 7, 10), { fill: C.ink, line: 0, grain: 0, off: [0, 0] });
  X.restore(); }

// the crowd: rows of tiny riders (the pull-back), half of them get training wheels on HALF
const ROWDY = 800, COLS = [-2, -1, 0, 1, 2], ROWS = [-1, 0, 1, 2];
function crowd(T, p, a) {
  if (a <= 0.01) return;
  X.save(); X.globalAlpha *= a;
  const lane = seg(T, T_.about - 0.05, T_.about + 0.3), out = seg(T, T_.then, T_.then + 0.4);
  // the two lanes (colour-block wipe, bottom-up)
  if (lane > 0 && out < 1) { X.save(); X.globalAlpha *= 1 - out;
    const top = 700 + ROWS[0] * ROWDY - 420, mid = 700 + 0.5 * ROWDY + 60, bot = 700 + 2 * ROWDY + 480;
    const yTop = lerp(bot, top, eio(lane));
    plane(X, rect(-1400, Math.max(yTop, top), 3900, Math.max(0, mid - Math.max(yTop, top))), "rgba(138,207,198,0.55)");
    plane(X, rect(-1400, Math.max(yTop, mid), 3900, Math.max(0, bot - Math.max(yTop, mid))), "rgba(203,208,142,0.6)");
    X.restore(); }
  for (const r of ROWS) floor(T, p + r * 137, -1400, 2500, 1000 + r * ROWDY, 300 + r, r === 0 ? 2 : 2);
  for (const r of ROWS) for (const c of COLS) {
    if (r === 0 && c === 0) continue;
    const dx = c * 700, dy = r * ROWDY, off = (c * 53 + r * 97) % 200;
    const topLane = r <= 0, tw = topLane ? back(seg(T, T_.half + (c + 2) * 0.06 + (r + 1) * 0.1, T_.half + 0.3 + (c + 2) * 0.06 + (r + 1) * 0.1), 2) : 0;
    X.save(); X.translate(dx, dy); rider(T, { p: p + off, tw, ex: topLane ? "happy" : "focus" }); X.restore(); }
  X.restore(); }

function tagAt(x, y, str, col, k, sc, centre) {   // a paper tag with a star bullet (detail tag)
  if (k <= 0.01) return; sc = sc || 1;
  X.font = SANS(30, 700); const tw = X.measureText(str).width + 84;
  X.save(); X.translate(centre ? x - tw * sc / 2 : x, y); X.scale(sc * k, sc * k);
  shape(X, rrect(0, -26, tw, 52, 14), { fill: col || C.white, line: 3, seed: 191, breaks: 0.1 });
  star(X, 22, 0, 12, { n: 4, inner: 0.35, fill: C.ink });
  text(X, str, 42, 11, { font: SANS(30, 700), fill: C.ink, track: 1 });
  X.restore(); }

// =============================================== the lower block (60/40 split) ===============================================
const BLK = { x: 264, y: 878, w: 556, h: 336 };
function blockVis(T) {                     // 0..1 wipe-up of the block
  const a = win(T, T_.alone, T_.res) ? Math.min(seg(T, T_.alone + 0.15, T_.alone + 0.5), 1 - seg(T, T_.res - 0.3, T_.res)) : 0;
  const b = win(T, T_.did + 0.3, T_.so2 + 0.1) ? Math.min(seg(T, T_.did + 0.45, T_.did + 0.8), 1 - seg(T, T_.so2 - 0.3, T_.so2)) : 0;
  return eio(Math.max(a, b)); }
function bar(x, base, wd, hmax, v, col, lab, numT, T, sub) {      // hmax = height of 100 %
  const h = hmax * v / 100;
  if (h > 1) shape(X, rect(x - wd / 2, base - h, wd, h), { fill: col, line: 4, seed: 201 + x % 13, breaks: 0.08 });
  const shown = Math.round(v);
  if (numT > 0) text(X, String(shown), x, base - h - 16, { font: SLAB(54), fill: C.ink, plate: col, align: "center", seed: 202 });
  text(X, lab, x, base + 32, { font: SANS(24, 700), fill: C.ink, align: "center", track: 1.5 }); }
function grid(x, y, n, col, cell, lab, cnt, T, tFill, tEach) {
  const g = 2; let k = 0;
  for (let r = 0; r < 10; r++) for (let c = 0; c < 10; c++, k++) {
    const on = k < n ? seg(T, tFill + k * tEach, tFill + k * tEach + 0.12) : 0;
    const xx = x + c * (cell + g), yy = y + r * (cell + g);
    X.fillStyle = C.white; X.fillRect(xx, yy, cell, cell);
    if (on > 0) { const s = 1 + (1 - on) * 0.6; X.save(); X.translate(xx + cell / 2, yy + cell / 2); X.scale(s, s);
      X.fillStyle = col; X.globalAlpha *= on; X.fillRect(-cell / 2 - 1, -cell / 2 - 1, cell + 2, cell + 2); X.restore(); } }
  ink(X, rect(x - 4, y - 4, 10 * (cell + g) + 6, 10 * (cell + g) + 6), 3, { closed: true, seed: 211, breaks: 0.1 });
  text(X, lab, x + 5 * (cell + g), y + 10 * (cell + g) + 30, { font: SANS(22, 700), fill: C.ink, align: "center", track: 1.5 });
  if (cnt !== null) text(X, cnt, x + 5 * (cell + g), y + 10 * (cell + g) + 76, { font: SLAB(42), fill: C.ink, plate: col, align: "center", seed: 212 }); }
function skipButton(cx, cy, press, T) {
  shape(X, rrect(cx - 92, cy + 18, 184, 64, 14), { fill: C.paperDD, line: 4, seed: 221 });
  text(X, "SKIP", cx, cy + 66, { font: SLAB(38), fill: C.ink, plate: C.tomatoL, align: "center", seed: 222 });
  const sq = press;
  shape(X, ellipse(cx, cy + 10 - 30 * (1 - sq * 0.5), 74, 46 * (1 - sq * 0.35), 30), { fill: C.tomato, line: 4.5, seed: 223,
    shade: [{ pts: ellipse(cx + 26, cy + 10 - 22 * (1 - sq * 0.5), 40, 30, 20), color: C.tomatoD, alpha: 0.5 }] });
  ink(X, [[cx - 74, cy + 10], [cx - 74, cy + 22]], 4, { seed: 224 }); ink(X, [[cx + 74, cy + 10], [cx + 74, cy + 22]], 4, { seed: 225 }); }
function book(cx, cy, k) {
  X.save(); X.translate(cx, cy); X.scale(k, k);
  shape(X, [[-90, -50], [0, -38], [0, 62], [-90, 50]], { fill: C.white, line: 4, seed: 231 });
  shape(X, [[90, -50], [0, -38], [0, 62], [90, 50]], { fill: C.white, line: 4, seed: 232 });
  for (let i = 0; i < 5; i++) { ink(X, [[-76, -26 + i * 15], [-14, -18 + i * 15]], 2.4, { seed: 233 + i, color: C.inkSoft });
    ink(X, [[14, -18 + i * 15], [76, -26 + i * 15]], 2.4, { seed: 240 + i, color: C.inkSoft }); }
  X.restore();
  text(X, "READING", cx, cy + 104, { font: SANS(24, 700), fill: C.ink, align: "center", track: 2 }); }
function block(T) {
  const v = blockVis(T); if (v <= 0.001) return;
  const { x, y, w: bw, h: bh } = BLK;
  X.save(); X.beginPath(); X.rect(x - 20, y + bh * (1 - v) - 10, bw + 40, bh * v + 30); X.clip();
  shape(X, rrect(x, y, bw, bh, 26), { fill: C.paperD, line: 4, seed: 251, breaks: 0.12 });
  const base = y + bh - 70;
  if (T < T_.res) {
    if (T < T_.and1 + 0.1) {                           // fewer solved: 74 vs 57
      const g = eo(seg(T, T_.fewer, T_.fewer + 0.9));
      bar(x + 405, base, 124, 255, 74 * g, C.olive, "NEVER HAD AI", g, T);
      bar(x + 155, base, 124, 255, 57 * g, C.mustard, "LOST THE AI", g, T);
      text(X, "SOLVED, OUT OF 100", x + bw / 2, base + 60, { font: SANS(21, 700), fill: C.inkSoft, align: "center", track: 2 });
    } else {                                           // skips: 11 vs 20, then reading: 1 vs 8
      const rd = T >= T_.reading;
      const zx = x + 74, zy = y + 118;
      if (!rd) { const press = Math.max(eo(seg(T, T_.skip - 0.02, T_.skip + 0.08)) * (1 - seg(T, T_.skip + 0.2, T_.skip + 0.45)), 0);
        X.save(); X.translate(zx, zy); X.scale(0.72, 0.72); X.translate(-zx, -zy); skipButton(zx, zy - 30, press, T); X.restore();
        const gy = lerp(-240, 0, eo(seg(T, T_.skip - 0.3, T_.skip))) - 160 * seg(T, T_.skip + 0.2, T_.skip + 0.55);
        X.save(); X.beginPath(); X.rect(x, y, bw, bh); X.clip(); gloveAt(zx + 4, zy - 72 + gy - 24 * (1 - press), Math.PI / 2, "point", 1, 1.3); X.restore();
      } else { X.save(); X.translate(zx, zy); X.scale(0.68, 0.68); X.translate(-zx, -zy); book(zx, zy - 20, pop(T, T_.reading, 0.35)); X.restore(); }
      text(X, "SKIPS", zx, y + 262, { font: SANS(22, 700), fill: C.inkSoft, align: "center", track: 2 });
      text(X, "IN 100", zx, y + 290, { font: SANS(22, 700), fill: C.inkSoft, align: "center", track: 2 });
      const cell = 17, gx1 = x + 150, gx2 = x + 356, gy0 = y + 30;
      if (!rd) {
        grid(gx1, gy0, 20, C.tomato, cell, "LOST THE AI", T > T_.skip + 0.4 ? String(Math.round(20 * seg(T, T_.skip + 0.45, T_.skip + 0.45 + 20 * 0.035))) : null, T, T_.skip + 0.45, 0.035);
        grid(gx2, gy0, 11, C.tomato, cell, "NO AI", T > T_.skip + 0.4 ? String(Math.round(11 * seg(T, T_.skip + 0.45, T_.skip + 0.45 + 11 * 0.035))) : null, T, T_.skip + 0.45, 0.035);
        const sk = seg(T, T_.twice2 - 0.04, T_.twice2 + 0.1);
        if (sk > 0) { const s2 = 1 + (1 - eo(sk)) * 0.9; X.save(); X.globalAlpha *= clamp(sk * 3); X.translate(gx1 + 164, y + 186); X.rotate(-0.14); X.scale(s2, s2);
          star(X, 0, 0, 40, { n: 12, inner: 0.76, fill: C.tomato, line: 3, seed: 213 }); text(X, "~2×", 0, 11, { font: SLAB(26), fill: C.white, align: "center" }); X.restore(); }
      } else {
        grid(gx1, gy0, 8, C.tomato, cell, "AFTER AI", T > T_.after + 0.3 ? String(Math.min(8, Math.round(8 * seg(T, T_.after + 0.35, T_.eight)))) : null, T, T_.after + 0.35, (T_.eight - T_.after - 0.4) / 7);
        grid(gx2, gy0, 1, C.tomato, cell, "NO AI", T > T_.one - 0.05 ? "1" : null, T, T_.one, 0.05);
      }
    }
    // colour-block wipes between the block's cards (side)
    for (const tw0 of [T_.and1 - 0.12, T_.reading - 0.15]) { const u = seg(T, tw0, tw0 + 0.32);
      if (u > 0 && u < 1) { const xa = x + bw * (u < 0.5 ? 0 : (u - 0.5) * 2), xb = x + bw * (u < 0.5 ? u * 2 : 1);
        plane(X, rect(xa, y, xb - xa, bh), tw0 < T_.reading - 1 ? C.tomatoL : C.blueL); } }
  } else {                                             // hints vs no AI: 76 vs 77 (and the CLUE stamp)
    const g = eo(seg(T, T_.did + 0.75, T_.did + 1.6));
    bar(x + 155, base, 124, 255, 76 * g, C.teal, "HINTS ONLY", g, T);
    bar(x + 405, base, 124, 255, 77 * g, C.olive, "NO AI", g, T);
    const ak = pop(T, T_.did + 1.7, 0.3); if (ak > 0.01) text(X, "≈", x + 280, base - 110, { font: SLAB(Math.round(70 * ak)), fill: C.ink, plate: C.mustardL, align: "center", seed: 261 });
    text(X, "SOLVED, OUT OF 100", x + bw / 2, base + 60, { font: SANS(21, 700), fill: C.inkSoft, align: "center", track: 2 });
    const ck = seg(T, T_.clue - 0.05, T_.clue + 0.12);
    if (ck > 0) { const s = 1 + (1 - eo(ck)) * 0.7; X.save(); X.translate(x + 155, base - 70); X.rotate(-0.2); X.scale(s, s); X.globalAlpha *= clamp(ck * 2.5);
      ink(X, rrect(-86, -34, 172, 68, 10), 6, { closed: true, color: C.tomato, seed: 262, breaks: 0.22 });
      text(X, "CLUE", 0, 18, { font: SLAB(50), fill: C.tomato, align: "center", seed: 263 });
      X.restore();
      const mk = pop(T, T_.clue + 0.1, 0.3); X.save(); X.translate(x + 258, base - 30); X.scale(mk, mk);
      ink(X, circ(0, 0, 26, 30), 6, { closed: true, seed: 264 }); ink(X, [[18, 18], [44, 44]], 9, { seed: 265 }); X.restore(); }
  }
  X.restore(); }

// =============================================== pins, tracker, chrome ===============================================
const PL = 22, PR = 840, PROWS = [326, 508, 690, 872], PW = 218, PH = 172;
const PINS = [
  { x: PL, y: PROWS[0], big: "1,222", lab: ["people,", "~10 min of AI"], t: T_.math + 0.1, col: C.mustardL, still: true },
  { x: PL, y: PROWS[1], big: "57 vs 74", lab: ["solved alone,", "out of 100"], t: T_.fewer + 2.2, col: C.mustardL, fs: 46 },
  { x: PL, y: PROWS[2], big: "20 vs 11", lab: ["skips", "in 100"], t: w(55), col: C.tomatoL, fs: 46 },
  { x: PL, y: PROWS[3], big: "8 vs 1", lab: ["reading skips", "in 100"], t: T_.eight + 0.3, col: C.tomatoL, fs: 54 },
  { x: PR, y: PROWS[0], big: "HINTS", lab: ["≈ no AI"], t: w(101), col: C.tealL, fs: 46 },
  { x: PR, y: PROWS[1], big: "SHORT", lab: ["tests; hints:", "a clue"], t: T_.proof, col: C.tomatoL, fs: 46 },
  { x: PR, y: PROWS[2], big: "HINT", lab: ["first, not", "the answer"], t: T_.go, col: C.mustardL, fs: 52 },
];
const RECAP = [0.1, 0.8, 1.5, 2.2, 2.6, 3.1, 3.6].map((d) => T_.theres + d);
const WORD_T = T_.comment;
function pinCard(p, T, i) {
  const k = p.still ? (T >= p.t ? 1 : 0) : pop(T, p.t, 0.4); if (k <= 0.01) return;
  const fresh = 1 - seg(T, p.t + 2.4, p.t + 2.8), lit = i < RECAP.length ? Math.min(seg(T, RECAP[i], RECAP[i] + 0.3), 1) : 0;
  const hide = seg(T, T_.short - 0.15, T_.short + 0.1) * (1 - seg(T, T_.clue - 0.1, T_.clue + 0.2));
  const gone = seg(T, MIRROR - 0.01, MIRROR);
  const a = (1 - hide) * (1 - gone);
  if (a <= 0.01) return;
  const dx = p.still ? 0 : (p.x < 540 ? 180 : -180) * (1 - eo(seg(T, p.t, p.t + 0.4)));
  X.save(); X.globalAlpha *= a; X.translate(p.x + PW / 2 + dx, p.y + PH / 2); X.scale(lerp(0.85, 1, clamp(k)), lerp(0.85, 1, clamp(k))); X.translate(-PW / 2, -PH / 2);
  const hot = Math.max(fresh, lit) > 0.5;
  shape(X, rrect(0, 0, PW, PH, 18), { fill: hot ? p.col : C.white, line: 3.5, seed: 300 + i, breaks: 0.1, off: [0, 0] });
  if (!hot) shape(X, rrect(0, 0, PW, PH, 18), { fill: null, line: 3.5, seed: 300 + i, breaks: 0.1 });
  star(X, 20, 24, 10, { n: 4, inner: 0.35, fill: C.ink });
  text(X, p.big, 36, 70, { font: SLAB(p.fs || 60), fill: C.ink, plate: p.col, seed: 310 + i, maxW: PW - 46 });
  p.lab.forEach((l, j) => text(X, l, 16, 114 + j * 32, { font: SANS(28, 600), fill: C.ink, maxW: PW - 28 }));
  if (lit > 0 && lit < 1) sparkle(X, PW - 14, 14, 24 * Math.sin(Math.PI * lit), { fill: C.mustard });
  X.restore(); }
function wordSlot(T) {
  const k = pop(T, WORD_T, 0.4) * (1 - seg(T, MIRROR - 0.01, MIRROR)); if (k <= 0.01) return;
  X.save(); X.translate(PR + PW / 2, PROWS[3] + PH / 2); X.scale(k, k); X.translate(-PW / 2, -PH / 2);
  shape(X, rrect(0, 0, PW, PH, 18), { fill: C.mustardL, line: 0, seed: 331, off: [0, 0] });
  dashed(X, [...rrect(0, 0, PW, PH, 18), [PW - 18, 0]], 4, 14, 9, T * 20, C.ink);
  text(X, "THE", PW / 2, 70, { font: SLAB(44), fill: C.ink, align: "center" });
  text(X, "WORD?", PW / 2, 126, { font: SLAB(50), fill: C.ink, plate: C.tomatoL, align: "center", seed: 333 });
  X.restore(); }
function margins(T) {
  const gone = 1 - seg(T, MIRROR - 0.01, MIRROR);
  const L = seg(T, PINS[0].t - 0.3, PINS[0].t) * gone, R = seg(T, PINS[4].t - 0.4, PINS[4].t) * gone;
  for (const [a, x0, x1, xl, dir] of [[L, 0, 252, 256, 1], [R, 828, W, 824, -1]]) {
    if (a <= 0.01) continue;
    X.save(); X.globalAlpha *= a;
    const g = X.createLinearGradient(dir > 0 ? x1 : x0, 0, dir > 0 ? x1 + 26 : x0 - 26, 0);
    g.addColorStop(0, C.paper); g.addColorStop(1, "rgba(244,234,213,0)");
    X.fillStyle = C.paper; X.fillRect(x0, 292, x1 - x0, 936);
    X.fillStyle = g; X.fillRect(dir > 0 ? x1 : x0 - 26, 292, 26, 936);
    ink(X, [[xl, 300], [xl, 1220]], 2.5, { color: C.tomatoL, seed: 541 + dir, taper: false, wob: 0.05 });
    X.restore(); } }
function chapterAt(T) { if (T >= MIRROR) return 0; let k = 0; CH_T.forEach((t, i) => { if (T >= t) k = i; }); return k; }
function tracker(T) {
  const k = chapterAt(T), x0 = 40, cw = 200, y = 258;
  for (let i = 0; i < 5; i++) {
    const x = x0 + i * cw, live = i === k, done = i < k;
    const lt = live && i > 0 ? seg(T, CH_T[i], CH_T[i] + 0.3) : 1;
    if (live) shape(X, rrect(x, y - 26, cw - 10, 52, 26), { fill: C.mustard, line: 3, seed: 341 + i, alpha: lt });
    else shape(X, rrect(x, y - 26, cw - 10, 52, 26), { fill: done ? C.white : C.paperD, line: 2.5, seed: 341 + i, alpha: done ? 1 : 0.8 });
    const s = live ? 1 + 0.15 * Math.sin(Math.PI * seg(T, CH_T[i], CH_T[i] + 0.3)) : 1;
    X.save(); X.translate(x + 26, y); X.scale(s, s);
    shape(X, circ(0, 0, 19, 20), { fill: C.ink, line: 0, grain: 0, off: [0, 0] });
    if (done) ink(X, [[-8, 0], [-2, 7], [9, -7]], 4, { color: C.white, seed: 350 + i });
    else text(X, String(i + 1), 0, 9, { font: SLAB(24), fill: C.white, align: "center" });
    X.restore();
    text(X, CH_N[i], x + 52, y + 9, { font: SANS(24, 700), fill: done || live ? C.ink : C.inkSoft, track: 1.5, maxW: cw - 70, alpha: done || live ? 1 : 0.65 }); } }
function chrome(T) {
  X.font = SANS(25, 700); X.letterSpacing = "2px"; const tw = X.measureText("AI PAPER · STORY").width; X.letterSpacing = "0px";
  shape(X, rrect(40, 150, tw + 76, 54, 27), { fill: C.white, line: 3, seed: 361, breaks: 0.08 });
  shape(X, circ(70, 177, 9, 14), { fill: "#FF7AC6", line: 2.5, seed: 362, breaks: 0 });
  text(X, "AI PAPER · STORY", 92, 186, { font: SANS(25, 700), fill: C.ink, track: 2 });
  text(X, "@ONEAITRICK", 1040, 186, { font: SANS(24, 700), fill: C.ink, align: "right", track: 2, alpha: 0.8 });
}

// =============================================== cards over the stage ===============================================
function odoDigits(x, y, str, px, offs, vel) {            // the claim card's odometer: each digit is a rolling strip
  const cw = px * 0.72, chH = px * 1.02;
  X.save(); X.beginPath(); X.rect(x - 6, y - chH * 0.74, cw * str.length + 12, chH * 0.92); X.clip();
  for (let j = 0; j < str.length; j++) {
    const d = +str[j], p = d + offs[j];                   // strip position in digits
    const blur = Math.min(0.14, Math.abs(vel) * 0.06), copies = blur > 0.01 ? 3 : 1;
    for (let c = 0; c < copies; c++) { const sh = copies > 1 ? (c - 1) * blur : 0;
      for (let n = Math.floor(p + sh) - 1; n <= Math.floor(p + sh) + 2; n++) {
        const dy = (n - (p + sh)) * chH, dd = ((n % 10) + 10) % 10;
        text(X, String(dd), x + j * cw + cw / 2, y + dy, { font: SLAB(px), fill: C.ink, plate: C.mustard, align: "center", seed: 371, alpha: copies > 1 ? (c === 1 ? 0.8 : 0.28) : 1 }); } } }
  X.restore(); }
const ODO0 = T_.andr + 0.1, ODO1 = T_.andr + 0.9;           // the end: 00 counts up to 10 in 0.8 s, then holds into the cut
function odoState(T) {                                        // [tens offset, units offset, speed]
  if (T < ODO0 - 0.5 || T >= ODO1) return [0, 0, 0];
  const u = seg(T, ODO0, ODO1), e = 1 - eo(u), v = 3 * Math.pow(1 - u, 2) / (ODO1 - ODO0);
  return [-e, -10 * e, 10 * v]; }
function claimCard(T) {
  const inA = 1 - seg(T, T_.pic - 0.2, T_.pic + 0.12), inB = T >= T_.andr - 0.1 ? 1 : 0;
  const v = T < 20 ? inA : inB; if (v <= 0.001) return;
  const x = 100, y = 922, cw = 880, ch = 286;
  X.save(); X.beginPath(); X.rect(x - 30, y - 60, cw + 60, (ch + 90) * v); X.clip();
  shape(X, rrect(x + 10, y + 12, cw, ch, 30), { fill: "rgba(120,90,60,0.25)", line: 0, grain: 0, off: [0, 0] });
  shape(X, rrect(x, y, cw, ch, 30), { fill: C.white, line: 5, seed: 381, breaks: 0.08 });
  text(X, "COLM 2026 · 1,222 PEOPLE", x + 46, y + 50, { font: SANS(23, 700), fill: C.inkSoft, track: 2 });
  const [ot, ou, vel] = odoState(T), bump = 1 + 0.08 * Math.sin(Math.PI * seg(T, 0.02, 0.32));
  X.save(); X.translate(x + 150, y + 140); X.scale(bump, bump); X.translate(-(x + 150), -(y + 140));
  odoDigits(x + 46, y + 178, "10", 142, [ot, ou], vel);
  text(X, "MIN OF AI", x + 268, y + 172, { font: SLAB(82), fill: C.ink, plate: C.mustardL, seed: 383 });
  X.restore();
  text(X, "GAVE UP ALMOST 2× AS OFTEN", x + 46, y + 252, { font: SLAB(46), fill: C.ink, plate: C.tomatoL, seed: 384, maxW: 790 });
  X.restore();
  // the ~2x stamp on TWICE (only in the hook)
  const sk = T < 20 ? seg(T, T_.twice - 0.04, T_.twice + 0.1) : 0;
  if (sk > 0 && inA > 0.01) { const s = 1 + (1 - eo(sk)) * 0.9; X.save(); X.globalAlpha *= clamp(sk * 3) * inA; X.translate(x + cw - 60, y + 4); X.rotate(-0.14); X.scale(s, s);
    star(X, 0, 0, 80, { n: 14, inner: 0.78, fill: C.tomato, line: 4, seed: 385 });
    text(X, "~2×", 0, 20, { font: SLAB(50), fill: C.white, align: "center" }); X.restore(); } }
function callout(T) {                                       // the AI = TRAINING WHEELS call-out
  const k = seg(T, T_.pic + 0.12, T_.pic + 0.45) * (1 - seg(T, T_.over - 0.35, T_.over - 0.05)); if (k <= 0.001) return;
  const cx = 196, cy = 600, r = 150 * eo(k);
  const cam = camAt(T), sp = [(G.TW[0] - cam.ax) * cam.s + cam.bx, (G.TW[1] - cam.ay) * cam.s + cam.by];
  ink(X, [sp, [cx - r * 0.7, cy + r * 0.7]], 4.5, { seed: 391, upto: eo(k), taper: false });
  shape(X, circ(sp[0], sp[1], 52 * cam.s, 30), { fill: null, line: 4, seed: 392 });
  if (r < 5) return;
  shape(X, circ(cx + 8, cy + 10, r, 48), { fill: "rgba(120,90,60,0.22)", line: 0, grain: 0, off: [0, 0] });
  shape(X, circ(cx, cy, r, 48), { fill: C.paperD, line: 5, seed: 393 });
  X.save(); path(X, circ(cx, cy, r - 4, 48)); X.clip();
  rays(X, cx, cy, 24, r, "rgba(243,211,127,0.5)", { rot: T * 0.2 });
  trainingWheel(cx, cy + 6, r * 0.62, pos(T) / 38, T, 1);
  X.restore();
  const tk = pop(T, T_.train - 0.08, 0.35); tagAt(cx, cy - 150 - 42, "AI = TRAINING WHEELS", C.tealL, tk, 0.92, true); }
function countBadge(T) {                                    // 1,222 counts up, then parks as pin 1
  const k = pop(T, T_.thousand - 0.1, 0.35), fly = eio(seg(T, T_.math - 0.25, T_.math + 0.1)); if (k <= 0.01 || fly >= 1) return;
  const n = Math.round(1222 * eo(seg(T, T_.thousand, T_.thousand + 0.8)));
  const x = lerp(540, PL + 105, fly), y = lerp(390, PROWS[0] + 80, fly), s = lerp(1, 0.5, fly) * clamp(k);
  X.save(); X.translate(x, y); X.scale(s, s);
  shape(X, rrect(-200, -76, 400, 152, 30), { fill: C.white, line: 5, seed: 401 });
  text(X, n.toLocaleString("en-US"), 0, 20, { font: SLAB(96), fill: C.ink, plate: C.mustard, align: "center", seed: 402 });
  text(X, "PEOPLE", 0, 58, { font: SANS(24, 700), fill: C.inkSoft, align: "center", track: 3 });
  X.restore(); }
function iris(T) {                                          // the wheels come off: an iris closes on them, then opens
  const close = eio(seg(T, T_.warning, T_.warning + 0.35)), open = eio(seg(T, T_.off + 0.12, T_.off + 0.55));
  const k = close * (1 - open); if (k <= 0.001) return;
  const cam = camAt(T), cx = (G.TW[0] - cam.ax) * cam.s + cam.bx, cy = (G.TW[1] - 30 - cam.ay) * cam.s + cam.by;
  const r = lerp(1300, 230, k);
  X.save(); X.beginPath(); X.rect(0, 292, W, 936); X.arc(cx, cy, r, 0, TAU, true); X.fillStyle = C.ink; X.globalAlpha = 0.93; X.fill("evenodd"); X.restore();
  ink(X, [[0, 296], [W, 296]], 6, { color: C.mustard, seed: 412, taper: false, alpha: k }); ink(X, [[0, 1224], [W, 1224]], 6, { color: C.mustard, seed: 413, taper: false, alpha: k });
  ink(X, circ(cx, cy, r, 60), 6, { closed: true, color: C.mustard, seed: 411, breaks: 0.1 }); }
function discIris(T) {                                       // chapter change: the numbered disc is the door
  for (let i = 1; i < 5; i++) { const t0 = CH_T[i], u = (T - t0) / 0.5; if (u < 0 || u > 1) continue;
    const cx = 540, cy = 700;
    X.save(); X.beginPath(); X.rect(0, 292, W, 936); X.clip();
    if (u < 0.36) { const s = back(u / 0.36, 2.4);
      shape(X, circ(cx, cy, 110 * s, 40), { fill: C.ink, line: 0, grain: 0.1, off: [0, 0] });
      text(X, String(i + 1), cx, cy + 40 * s, { font: SLAB(Math.max(1, Math.round(118 * s))), fill: C.mustard, align: "center" }); }
    else { const v = (u - 0.36) / 0.64, R = lerp(110, 1100, eo(v)), th = lerp(110, 26, eo(Math.min(1, v * 3))), al = 1 - seg(v, 0.7, 1);
      X.globalAlpha *= al;
      X.beginPath(); X.arc(cx + 7, cy + 5, R, 0, TAU); X.arc(cx + 7, cy + 5, Math.max(0, R - th), 0, TAU, true); X.fillStyle = C.mustard; X.fill("evenodd");
      X.beginPath(); X.arc(cx, cy, R, 0, TAU); X.arc(cx, cy, Math.max(0, R - th * 0.55), 0, TAU, true); X.fillStyle = C.ink; X.fill("evenodd"); }
    X.restore(); } }
function proofCard(T) {
  const pg = PAGES.p01a, img = document.getElementById("p01a"); if (!pg || !img || !img.complete) return;
  const a = eo(seg(T, T_.short - 0.15, T_.short + 0.15)), b = eio(seg(T, T_.clue - 0.14, T_.clue + 0.2));
  if (a <= 0.001 || b >= 0.999) return;
  const cw = 940, s = (cw - 40) / pg.w, ih = pg.h * s, ch = ih + 92, x = 70, y = 520;
  X.save();
  X.translate(x, y + ch / 2); X.scale(a * (1 - b), 1); X.translate(0, -ch / 2);   // page turn: in from the left edge, out the same way
  const push = 1 + 0.06 * seg(T, T_.short, T_.and2 + 0.8);
  X.translate(cw / 2, ch / 2); X.scale(push, push); X.translate(-cw / 2, -ch / 2);
  shape(X, rrect(10, 14, cw, ch, 26), { fill: "rgba(80,60,40,0.3)", line: 0, grain: 0, off: [0, 0] });
  shape(X, rrect(0, 0, cw, ch, 26), { fill: C.white, line: 5, seed: 421, breaks: 0.06 });
  { const HL = (pg.hl || []).slice().sort((p, q) => p[1] - q[1] || p[0] - q[0]), tot = HL.reduce((a, h) => a + h[2], 0) || 1;
    let acc = 0; const u = eio(seg(T, T_.tests - 0.1, T_.tests + 0.55)) * tot;
    HL.forEach((h) => { const g = clamp((u - acc) / h[2]); acc += h[2];
      if (g > 0) { X.fillStyle = C.mustardL; X.fillRect(20 + (h[0] - 4) * s, 20 + (h[1] - 2) * s, (h[2] + 8) * s * g, (h[3] + 4) * s); } }); }
  X.globalCompositeOperation = "multiply"; X.drawImage(img, 20, 20, pg.w * s, ih); X.globalCompositeOperation = "source-over";
  const dim = 0.62 * eio(seg(T, T_.tests + 0.2, T_.tests + 0.6));        // only the highlighted words stay strong
  if (dim > 0) { X.save(); X.beginPath(); X.rect(14, 14, pg.w * s + 12, ih + 12);
    (pg.hl || []).forEach((h) => X.rect(20 + (h[0] - 4) * s, 20 + (h[1] - 2) * s, (h[2] + 8) * s, (h[3] + 4) * s));
    X.fillStyle = `rgba(251,246,234,${dim})`; X.fill("evenodd"); X.restore(); }
  ink(X, [[0, ih + 36], [cw, ih + 36]], 3, { seed: 422, taper: false });
  text(X, "THE PAPER · LIMITATIONS · COLM 2026", 26, ih + 74, { font: SANS(22, 700), fill: C.inkSoft, track: 2 });
  X.restore(); }
function promptCard(T) {                                     // "Give me a hint, not the answer."
  const a = eo(seg(T, T_.so2 + 0.05, T_.so2 + 0.4)), b = eio(seg(T, T_.like - 0.2, T_.like + 0.1)); if (a <= 0.001 || b >= 0.999) return;
  const x = 264, y = 882, cw = 556, ch = 304;
  X.save(); X.beginPath(); X.rect(0, 292, W, 936); X.clip();
  X.translate(0, (1 - a) * 420 + b * 420);
  shape(X, rrect(x + 10, y + 14, cw, ch, 34), { fill: "rgba(80,60,40,0.25)", line: 0, grain: 0, off: [0, 0] });
  shape(X, rrect(x, y, cw, ch, 34), { fill: C.white, line: 5, seed: 431 });
  bubble(x + 54, y + 54, 28, T, C.tealL, 0);
  text(X, "Ask your AI", x + 98, y + 66, { font: SANS(28, 700), fill: C.inkSoft, track: 1 });
  const full = "Give me a hint, not the answer.", n = Math.round(full.length * seg(T, T_.so2 + 0.35, T_.answer - 0.3));
  const shown = full.slice(0, n), l1 = shown.slice(0, Math.min(n, 16)), l2 = shown.length > 16 ? shown.slice(16) : "";
  text(X, l1, x + 40, y + 150, { font: SANS(52, 700), fill: C.ink });
  text(X, l2, x + 40, y + 216, { font: SANS(52, 700), fill: C.ink });
  if (n < full.length && Math.floor(T * 3) % 2 === 0) { X.font = SANS(52, 700); const lw = X.measureText(l2 || l1).width;
    X.fillStyle = C.ink; X.fillRect(x + 44 + lw, y + (l2 ? 174 : 108), 5, 52); }
  const press = Math.sin(Math.PI * seg(T, T_.answer, T_.answer + 0.25));
  const bs = 1 - press * 0.15; X.save(); X.translate(x + cw - 62, y + ch - 56); X.scale(bs, bs);
  shape(X, circ(0, 0, 40, 30), { fill: C.teal, line: 4, seed: 432 });
  ink(X, [[-12, 0], [14, 0]], 6, { color: C.white, seed: 433 }); ink(X, [[2, -12], [14, 0], [2, 12]], 6, { color: C.white, seed: 434 });
  X.restore();
  X.restore(); }
function hintCard(x, y, k, T) {                              // the small HINT card the AI hands over
  if (k <= 0.01) return; X.save(); X.translate(x, y); X.scale(k, k); X.rotate(-0.08);
  shape(X, rrect(-70, -36, 140, 72, 14), { fill: C.tealL, line: 4, seed: 441 });
  text(X, "HINT", 0, 16, { font: SLAB(42), fill: C.ink, align: "center" });
  X.restore(); }
function answerCard(x, y, k) {
  if (k <= 0.01) return; X.save(); X.translate(x, y); X.scale(k, k); X.rotate(0.1);
  shape(X, rrect(-92, -32, 184, 64, 12), { fill: C.white, line: 4, seed: 451 });
  text(X, "ANSWER", -12, 12, { font: SLAB(30), fill: C.ink, align: "center" });
  ink(X, [[52, 0], [62, 10], [80, -12]], 5, { seed: 452, color: C.tealD });
  X.restore(); }

// the AI helper (HINTS on): a turquoise bubble behind the rider whose glove steadies the seat, then lets go
const HELP = [338, 600];
function helper(T) {
  const k = pop(T, T_.people + 0.1, 0.35) * (1 - seg(T, T_.go + 0.3, T_.go + 0.7)); if (k <= 0.01) return null;
  const bob = Math.sin(T * 2.2) * 6, hx = HELP[0], hy = HELP[1] + bob;
  const reach = eo(seg(T, T_.people + 0.25, T_.people + 0.55)) * (1 - eo(seg(T, T_.lets + 0.05, T_.lets + 0.5)));
  const seatBack = [G.S[0] - 46, G.S[1] + 4], el = [lerp(hx + 40, 380, 0.5), lerp(hy + 60, 700, 0.6) + 30];
  const armPts = spline([[hx + 30, hy + 36], el, seatBack], false, 10);
  if (reach > 0.01) { ink(X, subpath(armPts, reach), 12, { seed: 461, taper: false, color: C.ink });
    ink(X, move(subpath(armPts, reach), 3, 2), 6, { seed: 462, taper: false, color: C.teal });
    const tip = subpath(armPts, reach); const e = tip[tip.length - 1];
    gloveAt(e[0], e[1], 0.4, T >= T_.lets ? "open" : "grip", 1, 1.15); }
  X.save(); X.translate(hx, hy); X.scale(k, k);
  bubble(0, 0, 54, T, C.tealL, 1);
  X.restore();
  return [hx, hy]; }

// =============================================== the frame ===============================================
function paint(T) {
  setClock(T);
  X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1;
  X.fillStyle = C.paper; X.fillRect(0, 0, W, H);
  const p = pos(T), cam = camAt(T);
  // ---- the stage (camera space), clipped to the visual band
  X.save(); X.beginPath(); X.rect(0, 292, W, 936); X.clip();
  X.save(); applyCam(cam);
  const crowdA = clamp((0.45 - cam.s) / 0.12);
  // backdrop: one colour plane, the sunburst, the floor band
  shape(X, circ(520, 640, 330, 60), { fill: C.paperD, line: 0, grain: 0.2, off: [0, 0] });
  rays(X, 520, 640, 30, 600, "rgba(243,211,127,0.42)", { rot: T * (14 * TAU / 30) / DUR, r0: 60 });
  floor(T, p, -900, 2000, G.y, 501, T >= T_.math - 0.3 && T < T_.about ? 2 : 1);
  if (crowdA > 0) crowd(T, p, crowdA);
  // the timer (runs out over the ten minutes)
  const ring = T >= T_.then - 0.1 && T < T_.then + 0.6 ? 1 - seg(T, T_.then, T_.then + 0.6) : 0;
  if (crowdA < 0.3) timer(722, 440, timerMin(T), T, ring);
  // our rider
  const tws = twScale(T), detach = seg(T, T_.off, T_.off + 1.0), drop = seg(T, T_.people + 0.05, T_.people + 0.5);
  let o = { p, ex: expr(T), tw: tws };
  if (T >= T_.off && T < T_.res) {                       // OFF: up, down with one bounce, rolled away behind (the road carries it off)
    const u = detach, up = u < 0.3 ? -70 * Math.sin(Math.PI * u / 0.3) : u < 0.5 ? -22 * Math.sin(Math.PI * (u - 0.3) / 0.2) : 0;
    o.tw = detach < 1 ? 1 : 0; o.stub = true; o.twx = -40 * Math.min(1, u / 0.3) - 820 * Math.pow(Math.max(0, u - 0.25) / 0.75, 1.3); o.twy = up; o.twr = -u * 16; o.twa = 1; }
  if (T >= T_.people && T < MIRROR) { o.tw = drop < 1 ? 1 : 0; o.twy = 90 * drop * drop; o.twa = 1 - drop; }
  const wob = wobbleA(T) * Math.sin(TAU * 1.1 * T);
  if (win(T, T_.instant - 0.1, T_.so + 0.3)) {            // WHY: the answer card lands in the near glove
    const u = seg(T, T_.instant, T_.instant + 0.35), fade = 1 - seg(T, T_.so - 0.05, T_.so + 0.25);
    o.card = () => { const sx = G.TW[0], sy = G.TW[1] - 30, ex = G.HB[0] + 22, ey = G.HB[1] - 24;
      answerCard(lerp(sx, ex, eo(u)), lerp(sy, ey, eo(u)) - Math.sin(Math.PI * u) * 70, Math.min(1, u * 3) * fade); }; }
  if (win(T, T_.so, T_.heres + 0.2)) o.level = pop(T, T_.so, 0.3) * (1 - seg(T, T_.heres, T_.heres + 0.2));
  X.save(); X.translate(550, G.y); X.rotate(wob); X.translate(-550, -G.y);
  rider(T, o);
  const ob = seg(T, T_.off - 0.02, T_.off + 0.7);
  if (ob > 0 && ob < 1) { const e = [lerp(G.R[0], G.TW[0], 0.5), lerp(G.R[1], G.TW[1], 0.5)], k = back(Math.min(1, ob * 4), 2.4) * (1 - seg(ob, 0.6, 1));
    star(X, e[0], e[1], 70 * k, { n: 12, inner: 0.6, fill: C.tomato, line: 4, seed: 501 }); }
  X.restore();
  const hp = (T >= T_.people && T < MIRROR) ? helper(T) : null;
  if (hp) hintCard(hp[0] + 6, hp[1] - 110, pop(T, T_.hints - 0.05, 0.3) * (1 - seg(T, T_.short - 0.3, T_.short)), T);
  if (win(T, T_.answer, T_.like + 0.6) && hp) hintCard(hp[0] + 6, hp[1] - 110, pop(T, T_.answer + 0.15, 0.3) * (1 - seg(T, T_.like + 0.2, T_.like + 0.6)), T);
  if (win(T, T_.balance - 0.05, T_.heres + 0.15)) tagAt(548, 572, "BALANCE PRACTICE: 0", C.white, pop(T, T_.balance - 0.05, 0.3) * (1 - seg(T, T_.heres - 0.05, T_.heres + 0.15)), 0.95);
  if (win(T, T_.weird - 0.1, T_.people + 0.3)) { const sk = Math.sin(Math.PI * seg(T, T_.weird - 0.05, T_.people + 0.2));
    sparkle(X, 600, 400, 46 * sk, { fill: C.mustard, rot: T }); sparkle(X, 360, 470, 26 * sk, { fill: C.tealL, rot: -T }); }
  X.restore();
  // ---- over the stage, in screen space
  if (crowdA > 0.02) {                                          // the crowd: the ten minutes run out on a big timer; the two lanes
    X.save(); X.globalAlpha *= crowdA; X.translate(905, 400); X.scale(1.35, 1.35); timer(0, 0, timerMin(T), T, 0); X.restore();
    const lane = seg(T, T_.about - 0.05, T_.about + 0.3), out = seg(T, T_.then, T_.then + 0.4);
    if (lane > 0 && out < 1) { const k = pop(T, T_.half - 0.1, 0.35) * (1 - out);
      tagAt(268, 590, "HAD AI", C.tealL, k, 1.25); tagAt(268, 850, "NO AI", C.oliveL, k, 1.25); } }
  callout(T); countBadge(T); iris(T);
  X.restore();
  margins(T);
  block(T);
  discIris(T);
  PINS.forEach((pn, i) => pinCard(pn, T, i)); wordSlot(T);
  claimCard(T); proofCard(T); promptCard(T);
  // the catch: tomato edges and a dimmed stage
  const ce = win(T, T_.the2 - 0.1, T_.so2 + 0.2) ? Math.min(seg(T, T_.the2 - 0.1, T_.the2 + 0.2), 1 - seg(T, T_.proof + 0.3, T_.so2 + 0.1)) : 0;
  if (ce > 0) { X.save(); const g = X.createRadialGradient(540, 760, 380, 540, 760, 900); g.addColorStop(0, "rgba(224,83,58,0)"); g.addColorStop(1, `rgba(224,83,58,${0.45 * ce})`);
    X.fillStyle = g; X.fillRect(0, 280, W, 960); X.restore(); }
  tracker(T); chrome(T);
  paperFinish(X, W, H, 1);
  endIris(T); }
function endIris(T) {                                           // the end card: iris out to a dark disc behind the logo, open again for the last line
  const cl = eio(seg(T, T_.follow - 0.08, T_.follow + 0.32)), op = eio(seg(T, T_.andr - 0.06, T_.andr + 0.3)), k = cl * (1 - op);
  if (k <= 0.001) return;
  const r = lerp(1450, 472, cl) + (1450 - 472) * op, cx = 540, cy = 760;
  X.save(); X.beginPath(); X.rect(0, 0, W, H); X.arc(cx, cy, r, 0, TAU, true); X.fillStyle = "#1E1814"; X.fill("evenodd");
  X.beginPath(); X.arc(cx, cy, r, 0, TAU); X.fillStyle = `rgba(30,24,20,${0.86 * k})`; X.fill();
  X.restore();
  ink(X, circ(cx, cy, r, 80), 7, { closed: true, color: C.mustard, seed: 521, breaks: 0.1, alpha: k }); }
PAINT.push(paint);

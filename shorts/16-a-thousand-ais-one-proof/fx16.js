// Short #16: what happens on top of each shot (9:16). Inlined into index.html by make_index.py (helpers in index_template.tpl).
// Visuals sit in y 280-1220; captions own 1240-1460; the bottom ~450 px stays clear for the platform buttons.
// No generated media. The thinking orbs, the 1,000-orb field, the temple and its bricks, the boss-and-helpers diagram and
// the counters are drawn here (canvas + DOM). Canvases are repainted from the timeline's time on every frame, so seeking
// is exact. Graphics made for one shot live in that shot's overlay layer (CURP = OV(id)), so they ride its transition.
if (window.SplitText) gsap.registerPlugin(SplitText);
const STRIPS = LOGOS, LOGOSVG = __LOGOSVG__;
const LIME = "200,255,77", GRAY = "130,134,146", RED = "255,107,107", AMBER = "255,181,71", BLUE = "124,196,255";
const clamp01 = (v) => Math.max(0, Math.min(1, v));
const ramp = (t, a, b) => clamp01((t - a) / (b - a));
const ease = (k) => 1 - Math.pow(1 - k, 3);
const mixc = (c1, c2, k) => { const a = c1.split(",").map(Number), b = c2.split(",").map(Number); return a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(","); };
const shot = (id) => { CURP = OV(id); };

const typeOn = (sel, t, per) => { const n = typeof sel === "string" ? $(sel) : sel; if (!n) return;
  const parts = window.SplitText ? new SplitText(n, { type: "words,chars" }).chars : [n];
  tl.set(parts, { opacity: 0 }, 0);
  parts.forEach((c, i) => tl.set(c, { opacity: 1 }, t + i * (per || 0.028))); return parts.length; };
const bigLetters = (txt, x, y, fs, col, t0, t1, wd) => { const b = el("div", "big", `left:${x}px;top:${y}px;font-size:${fs}px;color:${col || "#fff"}` + (wd ? `;width:${wd}px;text-align:center` : ""), txt);
  tl.set(b, { opacity: 1 }, t0 - 0.01);
  const parts = window.SplitText ? new SplitText(b, { type: "chars" }).chars : [b];
  tl.set(parts, { opacity: 0 }, 0);
  tl.fromTo(parts, { opacity: 0, y: 80, scale: 1.6 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2.4)", stagger: 0.04, immediateRender: false }, t0);
  tl.to(b, { opacity: 0, duration: 0.15 }, t1); return b; };
const out = (els, t) => tl.to(els, { opacity: 0, duration: 0.15 }, t);
const stamp = (txt, x, y, rot, col, t0, t1, fs, bg) => { const s = el("div", "stamp", `left:${x}px;top:${y}px;transform:rotate(${rot}deg);color:${col};font-size:${fs || 64}px` + (bg ? `;background:${bg}` : ""), txt);
  tl.fromTo(s, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, t0); out(s, t1); return s; };
const svgEl = (x, y, wd, ht, inner, parent) => el("div", "", `position:absolute;left:${x}px;top:${y}px;width:${wd}px;height:${ht}px;opacity:0`,
  `<svg width="${wd}" height="${ht}" viewBox="0 0 ${wd} ${ht}">${inner}</svg>`, parent);
// an official logo, drawn on: the outline traces, then it fills (Simple Icons paths on a white tile)
const logoDraw = (code, x, y, wd, ht, t0, t1, fill) => { const src = LOGOSVG[code] || ""; const d = (src.match(/ d="([^"]+)"/) || [])[1] || "";
  const col = fill || (src.match(/fill="(#[0-9A-Fa-f]{6})"/) || [])[1] || "#141413";
  const tile = el("div", "logo", `left:${x}px;top:${y}px;width:${wd}px;height:${ht}px`,
    `<svg viewBox="0 0 24 24" style="width:${Math.min(wd, ht) * 0.66}px;height:${Math.min(wd, ht) * 0.66}px"><path d="${d}" pathLength="1" fill="${col}" fill-opacity="0" stroke="${col}" stroke-width="0.35" stroke-dasharray="1" stroke-dashoffset="1"/></svg>`);
  const p = tile.querySelector("path");
  tl.fromTo(tile, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(1.8)" }, t0);
  tl.to(p, { attr: { "stroke-dashoffset": 0 }, duration: 0.45, ease: "power2.inOut" }, t0 + 0.08);
  tl.to(p, { attr: { "fill-opacity": 1 }, duration: 0.25, ease: "power1.out" }, t0 + 0.42);
  out(tile, t1); return tile; };
const count = (node, from, to, t0, d, fmt, ez) => { const o = { v: from }; node.textContent = fmt(from);
  tl.fromTo(o, { v: from }, { v: to, duration: d, ease: ez || "power2.out", onUpdate() { node.textContent = fmt(o.v); }, immediateRender: false }, t0); };
const fmtInt = (v) => Math.round(v).toLocaleString("en-US");
const plate = (html, x, y, wd, fs, col, t0, t1, extra) => { const p = el("div", "big", `left:${x}px;top:${y}px;width:${wd}px;text-align:center;font-size:${fs}px;color:${col || "#fff"};` +
  `padding:16px 0 20px;border-radius:26px;background:rgba(6,8,12,0.8);text-transform:none;${extra || ""}`, html);
  tl.fromTo(p, { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(1.8)" }, t0); out(p, t1); return p; };
const scrim = (t0, t1) => { const s = el("div", "", "position:absolute;left:0;top:1150px;width:1080px;height:420px;opacity:0;background:linear-gradient(180deg,rgba(4,5,10,0),rgba(4,5,10,0.82) 30%,rgba(4,5,10,0.82) 80%,rgba(4,5,10,0))");
  tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t0); out(s, t1); };

// ---------- the painter: every canvas is redrawn from the timeline's time ----------
const PAINT = [];
const canvasEl = (x, y, wd, ht, parent) => { const c = el("canvas", "cv", `left:${x}px;top:${y}px;width:${wd}px;height:${ht}px`, undefined, parent);
  c.width = wd; c.height = ht; return c; };
const paint = (c, a, b, fn) => { PAINT.push({ c, x: c.getContext("2d"), a, b, fn });
  tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, a); out(c, b); };

// a thinking orb: a sphere of dots (my drawing, in the style of the thinking-orbs library)
const SPH = (n) => { const p = [], g = Math.PI * (3 - Math.sqrt(5)); for (let i = 0; i < n; i++) { const y = 1 - (i / (n - 1)) * 2, r = Math.sqrt(1 - y * y), th = g * i;
  p.push([Math.cos(th) * r, y, Math.sin(th) * r, i]); } return p; };
const ORB = SPH(240);
const orb = (c, X, Y, R, t, o) => { o = o || {};
  const mode = o.mode || "think", col = o.col || LIME, al = o.a === undefined ? 1 : o.a, sp = o.speed === undefined ? 0.7 : o.speed;
  const ay = (o.t0 || 0) + t * sp, ax = 0.35 + 0.12 * Math.sin(t * 0.6);
  const ca = Math.cos(ay), sa = Math.sin(ay), cb = Math.cos(ax), sb = Math.sin(ax);
  const g = c.createRadialGradient(X, Y, 0, X, Y, R * 1.7); g.addColorStop(0, `rgba(${col},${0.26 * al})`); g.addColorStop(1, `rgba(${col},0)`);
  c.fillStyle = g; c.fillRect(X - R * 1.7, Y - R * 1.7, R * 3.4, R * 3.4);
  const band = Math.sin(t * 2.6);
  for (const [px, py, pz, i] of ORB) {
    let r = 1;
    if (mode === "think") r = 1 + 0.07 * Math.sin(t * 3.2 + i * 0.7) * (o.pulse === undefined ? 1 : o.pulse);
    const x1 = px * ca + pz * sa, z1 = -px * sa + pz * ca;
    const y2 = py * cb - z1 * sb, z2 = py * sb + z1 * cb, d = (z2 + 1) / 2;
    let a = (0.12 + 0.88 * d) * al, s = (0.9 + 2.3 * d) * R / 120;
    if (mode === "search") { const k = Math.max(0, 1 - Math.abs(py - band) * 3.5); a *= 0.3 + 0.7 * k; s *= 1 + 0.9 * k; }
    c.fillStyle = `rgba(${col},${a})`; c.beginPath(); c.arc(X + x1 * R * r, Y + y2 * R * r, Math.max(0.6, s), 0, 6.2832); c.fill(); } };
// one small orb in the field: a turning ring of dots round a glowing core
const mini = (c, x, y, r, t, k, col, a) => { c.fillStyle = `rgba(${col},${a * 0.2})`; c.beginPath(); c.arc(x, y, r * 1.9, 0, 6.2832); c.fill();
  c.fillStyle = `rgba(${col},${a})`; c.beginPath(); c.arc(x, y, r * 0.42, 0, 6.2832); c.fill();
  const ph = t * 2.2 + k * 0.9;
  for (let q = 0; q < 6; q++) { const an = ph + q * 1.0472, z = Math.sin(an);
    c.fillStyle = `rgba(${col},${a * (0.45 + 0.55 * (z + 1) / 2)})`; c.beginPath(); c.arc(x + Math.cos(an) * r, y + z * r * 0.38, r * 0.2, 0, 6.2832); c.fill(); } };
// 1,000 small orbs on a 40 x 25 grid. o: {a, col, gray(x,y) -> 0..1, wave (px), wx, wy}
const field = (c, t, o) => { const cols = 40, rows = 25, W0 = c.canvas.width, H0 = c.canvas.height, dx = W0 / cols, dy = H0 / rows;
  const rr = Math.min(dx, dy) * 0.36;
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const k = j * cols + i; if (o.n !== undefined && k >= o.n) continue;
    const x = dx * (i + 0.5) + Math.sin(t * 0.9 + k) * 1.5, y = dy * (j + 0.5) + Math.cos(t * 0.8 + k * 1.3) * 1.5;
    const tw = 0.7 + 0.3 * Math.sin(t * 2.3 + k * 1.7);
    let col = o.col || LIME, a = (o.a === undefined ? 1 : o.a) * tw;
    if (o.gray) { const g = o.gray(x, y); col = mixc(LIME, GRAY, g); a *= 1 - 0.6 * g; }
    if (o.wave !== undefined) { const dist = Math.hypot(x - (o.wx === undefined ? W0 / 2 : o.wx), y - (o.wy === undefined ? H0 / 2 : o.wy)), k2 = clamp01((o.wave - dist) / 90);
      col = mixc(o.col || GRAY, LIME, k2); a = (o.a === undefined ? 1 : o.a) * tw * (1 - k2) + tw * k2; }
    mini(c, x, y, rr, t, k, col, a); } };

// a strip of a real page, centred on one highlighted phrase; soft edges where a line runs on past the frame
const strip = (name, o) => { const S = STRIPS[name]; if (!S) return null;
  const sc = o.sc || 0.72, wd = o.w || 1000, ph = S.hl[o.p || 0] || [];
  const top = ph.length ? Math.min(...ph.map((b) => b[1])) : S.h / 2 - 30, bot = ph.length ? Math.max(...ph.map((b) => b[1] + b[3])) : S.h / 2 + 30;
  const lh = ph.length ? ph[0][3] * 1.62 : 80, hh = Math.round(Math.min(S.h, Math.max((o.lines || 2) * lh, bot - top + 0.9 * lh)) * sc);
  let offY = ((top + bot) / 2) * sc - hh / 2; offY = Math.max(0, Math.min(S.h * sc - hh, offY));
  const x0 = ph.length ? Math.min(...ph.map((b) => b[0])) : 0, x1 = ph.length ? Math.max(...ph.map((b) => b[0] + b[2])) : S.w;
  let offX = ((x0 + x1) / 2) * sc - wd / 2; offX = Math.max(0, Math.min(S.w * sc - wd, offX)); const fits = S.w * sc <= wd; if (fits) offX = -(wd - S.w * sc) / 2;
  const fadeL = !fits && offX > 2, fadeR = !fits && offX < S.w * sc - wd - 2;
  const mask = `linear-gradient(90deg, ${fadeL ? "transparent 0, #000 70px" : "#000 0"}, ${fadeR ? "#000 calc(100% - 70px), transparent 100%" : "#000 100%"})`;
  const d = el("div", "strip", `left:${o.x === undefined ? 40 : o.x}px;top:${o.y}px;width:${wd}px;height:${hh + 34}px`, "");
  const win = el("div", "", `position:absolute;left:0;top:0;width:${wd}px;height:${hh}px;overflow:hidden;-webkit-mask-image:${mask};mask-image:${mask}`, "", d);
  const inner = el("div", "", `position:absolute;left:${-offX}px;top:${-offY}px;width:${S.w * sc}px;height:${S.h * sc}px`,
    `<img src="assets/img/${name}.png" alt="" style="width:${S.w * sc}px" />`, win);
  ph.forEach((b, j) => { const h = el("div", "hl", `left:${b[0] * sc - 4}px;top:${b[1] * sc - 2}px;width:${b[2] * sc + 8}px;height:${b[3] * sc + 4}px`, "", inner);
    tl.to(h, { scaleX: 1, duration: 0.35, ease: "power2.inOut" }, o.th + j * 0.3); });
  el("div", "sl", "", "● " + S.src, d);
  tl.fromTo(d, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, o.t0);
  if (!fits) tl.fromTo(inner, { x: 0 }, { x: -14, duration: o.t1 - o.t0, ease: "none" }, o.t0);
  out(d, o.t1); return d; };

// the temple: the famous building of the story (my line drawing), 840 x 600 at scale 1
const FACADE = ["M80 170 L420 40 L760 170 Z", "M60 170 H780 V215 H60 Z", ...[0, 1, 2, 3, 4, 5].map((i) => `M${115 + i * 122} 225 V505 M${165 + i * 122} 225 V505`),
  "M50 515 H790 M30 545 H810 M10 575 H830"];
const temple = (x, y, sc, o) => { o = o || {};
  const f = svgEl(x, y, Math.round(840 * sc), Math.round(600 * sc), `<g transform="scale(${sc})" fill="none" stroke="${o.col || "#c8ff4d"}" stroke-width="${6 / sc}" stroke-linejoin="round" stroke-linecap="round">` +
    FACADE.map((d) => `<path class="dr" d="${d}"/>`).join("") + `</g>`);
  f.style.filter = "drop-shadow(0 0 12px rgba(200,255,77,0.6))";
  tl.fromTo(f, { opacity: 0 }, { opacity: o.a === undefined ? 1 : o.a, duration: 0.2 }, o.t0);
  if (o.draw) f.querySelectorAll(".dr").forEach((p, i) => { const L = 2400; p.setAttribute("stroke-dasharray", L);
    tl.fromTo(p, { attr: { "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.9, ease: "power2.inOut" }, o.draw + i * 0.09); });
  if (o.t1) out(f, o.t1); return f; };

// the blueprint grid drifts on every shot that has it
SH.forEach((s) => { const g = document.getElementById("grid-" + s.id); if (g) tl.fromTo(g, { backgroundPosition: "0px 0px" }, { backgroundPosition: "-40px -150px", duration: s.t1 - s.t0 + 0.5, ease: "none" }, Math.max(0, s.t0 - HND)); });

// ---------- s01 - s02: the hook (frame one: 1,000 AIs, 30 hours) ----------
shot("s01");
tl.fromTo("#title", { opacity: 1, y: 0 }, { opacity: 1, y: 0, duration: 0.01 }, 0);
tl.fromTo("#title", { scale: 1 }, { scale: 1.04, duration: 2.0, ease: "power1.inOut", transformOrigin: "0% 0%" }, 0);
tl.to("#title", { opacity: 0, y: -20, duration: 0.2 }, w(7) - 0.12);
(function () { const c = canvasEl(60, 650, 960, 560); tl.set(c, { opacity: 1 }, 0);
  // the verdict spreads: orbs grey out left to right from "most" to "couldn't"
  PAINT.push({ c, x: c.getContext("2d"), a: 0, b: B("s01"), fn: (x, t) => field(x, t, { gray: (px) => ramp(t, w(3) + (px / 960) * (w(7) - w(3)) - 0.15, w(3) + (px / 960) * (w(7) - w(3)) + 0.25) }) });
  out(c, B("s01"));
  tl.fromTo(c, { scale: 1 }, { scale: 1.08, duration: w(7), ease: "power1.inOut" }, 0);
  tl.to(c, { y: -120, duration: 0.5, ease: "power2.inOut" }, w(7) - 0.15);
  stamp("CAN'T BE DONE", 215, 720, -6, "#ff4d4d", w(7), B("s01") - 0.02, 92, "rgba(11,12,16,0.92)");
  chip("47 OF 60 PARTS · THE AIs' OWN VERDICT", 60, 1100, "#ffb547", w(8), B("s01") - 0.06); })();
shot("s02");
(function () { const c = canvasEl(60, 530, 960, 560); tl.set(c, { opacity: 1 }, A("s02"));
  // "Then they DID it": a lime ripple runs out from the stamp
  PAINT.push({ c, x: c.getContext("2d"), a: A("s02"), b: B("s02"), fn: (x, t) => field(x, t, { a: 0.4, col: GRAY, wave: ease(ramp(t, w(12) - 0.05, w(12) + 0.6)) * 1150, wx: 480, wy: 230 }) });
  out(c, B("s02") - 0.04);
  const s = el("div", "stamp", "left:215px;top:720px;transform:rotate(-6deg);color:#ff4d4d;font-size:92px;opacity:0;background:rgba(11,12,16,0.92)", "CAN'T BE DONE");
  tl.set(s, { opacity: 1 }, A("s02")); const st = el("div", "strike", "left:180px;top:780px;width:720px;background:#c8ff4d;box-shadow:0 0 22px rgba(200,255,77,0.8)");
  tl.set(st, { rotation: -6 }, 0);
  tl.to(st, { scaleX: 1, duration: 0.22, ease: "power3.out" }, w(12) - 0.05); tl.to(s, { opacity: 0.35, duration: 0.2 }, w(12) + 0.1);
  const rg = el("div", "ring", "left:440px;top:700px;width:200px;height:200px"); tl.fromTo(rg, { opacity: 1, scale: 0.2 }, { opacity: 0, scale: 5, duration: 0.7, ease: "power2.out", immediateRender: false }, w(12));
  bigLetters("DONE ✓", 0, 320, 190, "var(--lime)", w(12), B("s02") - 0.05, 1080); punch("s02", w(12), 0.06);
  out([s, st], B("s02") - 0.05); })();

// ---------- s03 - s05: the building, brick by brick, and the inspector ----------
shot("s03");
temple(204, 600, 0.8, { t0: A("s03") + 0.05, draw: A("s03") + 0.1, t1: B("s03") - 0.06 });
chip("A FAMOUS BUILDING · ON PAPER", 60, 330, "var(--lime)", w(16), B("s03") - 0.08);
shot("s04");
(function () { const p = plate("BRICK <span id='bk'>1</span>", 330, 330, 420, 110, "#fff", w(23) - 0.05, B("s04") - 0.08, "font-family:Mono, monospace;padding:4px 0 10px");
  tl.set("#bk", { textContent: "2" }, w(25) - 0.03); [23, 25].forEach((k) => { punch("s04", w(k), 0.06); tl.fromTo(p, { scale: 1.15 }, { scale: 1, duration: 0.25, immediateRender: false }, w(k)); });
  chip("REBUILD IT, BRICK BY BRICK", 60, 1100, "#ffffff", w(21), B("s04") - 0.08); })();
shot("s05");
(function () { const cols = 6, rows = 4, bw = 132, bh = 62, gx = 12, gy = 12, X0 = 540 - (cols * (bw + gx) - gx) / 2, Y0 = 360;
  const panel = el("div", "panel", `left:${X0 - 26}px;top:${Y0 - 26}px;width:${cols * (bw + gx) - gx + 52}px;height:${rows * (bh + gy) - gy + 52}px`);
  tl.fromTo(panel, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, A("s05") + 0.05);
  const bricks = [], checks = [];
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const x = X0 + i * (bw + gx) + (j % 2 ? 20 : 0) - 10, y = Y0 + j * (bh + gy);
    bricks.push(el("div", "", `position:absolute;left:${x}px;top:${y}px;width:${bw}px;height:${bh}px;border-radius:7px;background:#b85d38;border:3px solid #e79a76;opacity:0`));
    checks.push(el("div", "", `position:absolute;left:${x + bw / 2 - 20}px;top:${y + bh / 2 - 22}px;font-weight:900;font-size:40px;color:#c8ff4d;opacity:0;text-shadow:0 0 12px rgba(0,0,0,0.9)`, "✓")); }
  tl.fromTo(bricks, { opacity: 0 }, { opacity: 1, duration: 0.2, stagger: 0.01 }, A("s05") + 0.1);
  const tA = w(28), tB = w(31);
  checks.forEach((c, n) => { const t = n < 10 ? tA + n * (tB - tA) / 10 : tB + (n - 10) * 0.03; tl.fromTo(c, { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.15, ease: "back.out(2)" }, t); });
  const mag = el("div", "", "position:absolute;left:0;top:0;width:150px;height:150px;border-radius:50%;border:8px solid #fff;opacity:0;box-shadow:0 0 30px rgba(255,255,255,0.4), inset 0 0 40px rgba(255,255,255,0.25)");
  const pos = (k) => { const i = k % cols, j = Math.floor(k / cols); return { x: X0 + i * (bw + gx) + bw / 2 - 75 + (j % 2 ? 10 : -10), y: Y0 + j * (bh + gy) + bh / 2 - 75 }; };
  tl.set(mag, Object.assign({ opacity: 1 }, pos(0)), tA - 0.1);
  for (let n = 1; n < 10; n++) tl.to(mag, Object.assign({ duration: (tB - tA) / 10, ease: "power1.inOut" }, pos(n)), tA + (n - 1) * (tB - tA) / 10);
  tl.to(mag, Object.assign({ duration: 0.5, ease: "power2.inOut" }, pos(23)), tB);
  punch("s05", tB, 0.12); flash(tB, 0.2, 0.3, "#c8ff4d");
  chip("A STRICT INSPECTOR", 60, 1010, "#ffffff", w(28), B("s05") - 0.08);
  chip("✓ EVERY SINGLE BRICK", 60, 1100, "var(--lime)", tB, B("s05") - 0.08);
  out([panel, ...bricks, ...checks, mag], B("s05") - 0.06); })();

// ---------- s06 - s09: the proof, Fermat, 358 years, paper ----------
shot("s06");
(function () { const bricks = []; const eq = el("div", "eq", "top:500px", "a<sup>n</sup> + b<sup>n</sup> = c<sup>n</sup>");
  for (let k = 0; k < 15; k++) { const i = k % 5, j = Math.floor(k / 5);
    bricks.push(el("div", "", `position:absolute;left:${215 + i * 132 + (j % 2 ? 30 : 0)}px;top:${430 + j * 74}px;width:120px;height:62px;border-radius:7px;background:#b85d38;border:3px solid #e79a76;opacity:0`)); }
  tl.fromTo(bricks, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, stagger: 0.015 }, A("s06") + 0.05);
  const tm = w(37) - 0.05;
  bricks.forEach((b, k) => tl.to(b, { x: (k % 5 - 2) * -40 + (k * 37 % 60) - 30, y: 60 - Math.floor(k / 5) * 40, scale: 0.3, rotation: (k * 47 % 90) - 45, opacity: 0, duration: 0.45, ease: "power2.in" }, tm + k * 0.012));
  tl.fromTo(eq, { opacity: 0, scale: 0.6, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "back.out(1.6)" }, tm + 0.3);
  flash(tm + 0.3, 0.15, 0.3, "#c8ff4d");
  chip("FERMAT'S LAST THEOREM", 60, 1010, "var(--lime)", w(38), B("s06") - 0.08);
  chip("NO POSITIVE WHOLE NUMBERS FIT · n > 2", 60, 1100, "#ffffff", w(39) - 0.1, B("s06") - 0.08); out(eq, B("s06") - 0.06); })();
shot("s07");
(function () { const p = el("div", "", "position:absolute;left:60px;top:300px;width:190px;height:236px;border-radius:18px;overflow:hidden;opacity:0;border:4px solid #f6f4ee;box-shadow:0 30px 60px rgba(0,0,0,0.6)",
    `<img src="assets/img/fermat.png" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%" />`);
  const pl = el("div", "tag", "left:60px;top:548px;background:#0b0c10;border:2px solid #f6f4ee", "PIERRE DE FERMAT");
  pop(p, w(40) - 0.1, w(45), 0.7); show(pl, w(40), w(45));
  scrim(A("s07"), B("s07") - 0.04);
  chip("HIS NOTE: “THIS MARGIN IS TOO SMALL” (LATIN)", 60, 1100, "#ffffff", w(46), B("s07") - 0.08);
  const yr = el("div", "off", "left:700px;top:330px;font-size:96px;padding:10px 34px;transform:rotate(-4deg)", "1637");
  pop(yr, w(49), B("s07") - 0.08, 0.3); })();
shot("s08");
(function () { const X0 = 110, X1 = 970, xOf = (yr) => X0 + (yr - 1637) / 358 * (X1 - X0);
  const svg = svgEl(0, 540, 1080, 200, `<line x1="${X0}" y1="90" x2="${X1}" y2="90" stroke="rgba(255,255,255,0.25)" stroke-width="10" stroke-linecap="round"/>
    <line class="fl" x1="${X0}" y1="90" x2="${X1}" y2="90" stroke="#c8ff4d" stroke-width="10" stroke-linecap="round" stroke-dasharray="${X1 - X0}" stroke-dashoffset="${X1 - X0}"/>
    ${[1700, 1800, 1900].map((y) => `<line x1="${xOf(y)}" y1="74" x2="${xOf(y)}" y2="106" stroke="rgba(255,255,255,0.5)" stroke-width="4"/><text x="${xOf(y)}" y="150" text-anchor="middle" font-family="Mono, monospace" font-weight="700" font-size="26" fill="#8b90a0">${y}</text>`).join("")}
    <circle cx="${X0}" cy="90" r="20" fill="#c8ff4d"/><circle class="end" cx="${X1}" cy="90" r="20" fill="#3a3f4c" stroke="#c8ff4d" stroke-width="4"/>
    <text x="${X0}" y="44" text-anchor="middle" font-family="Mono, monospace" font-weight="700" font-size="38" fill="#fff">1637</text>
    <text x="${X1}" y="44" text-anchor="middle" font-family="Mono, monospace" font-weight="700" font-size="38" fill="#fff">1995</text>`);
  tl.fromTo(svg, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, A("s08") + 0.05);
  tl.to(svg.querySelector(".fl"), { attr: { "stroke-dashoffset": 0 }, duration: w(57) - w(50), ease: "power1.inOut" }, w(50));
  tl.to(svg.querySelector(".end"), { attr: { fill: "#c8ff4d", r: 26 }, duration: 0.2 }, w(57));
  const c = el("div", "big", "left:0;width:1080px;text-align:center;top:310px;font-size:170px;color:#fff", "<span id='yrs'>0</span> <span style='font-size:90px;color:var(--lime)'>YEARS</span>");
  tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.2 }, A("s08") + 0.1); count($("#yrs"), 0, 358, w(52), w(57) - w(52), fmtInt, "power1.inOut");
  punch("s08", w(57), 0.06);
  const wc = el("div", "wcard", "left:260px;top:750px;width:560px;text-align:center", `<div class="k">1995 · THE FIRST PROOF, BY</div><div class="n">ANDREW WILES</div>`);
  tl.fromTo(wc, { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.7)" }, w(53) - 0.05);
  strip("r_wiles", { p: 0, y: 980, sc: 0.62, lines: 1.6, t0: w(55), t1: B("s08") - 0.06, th: w(57) });
  out([svg, c, wc], B("s08") - 0.06); })();
shot("s09");
(function () { const lines = [520, 600, 440, 580, 360, 540, 480];
  const pg = el("div", "", "position:absolute;left:190px;top:340px;width:700px;height:720px;border-radius:12px;background:#f3eee2;opacity:0;box-shadow:0 40px 90px rgba(0,0,0,0.6)",
    lines.map((wd, i) => `<div class="ln${i}" style="position:absolute;left:60px;top:${80 + i * 86}px;width:${wd}px;height:18px;border-radius:9px;background:${i === 4 ? "#6b6e78" : "#9a9ca6"}"></div>`).join(""));
  tl.fromTo(pg, { opacity: 0, rotation: -3, y: 40 }, { opacity: 1, rotation: -1.5, y: 0, duration: 0.35, ease: E }, A("s09") + 0.05);
  tl.to(pg.querySelector(".ln4"), { background: "#e0322b", duration: 0.15 }, w(61));
  const ring = el("div", "", "position:absolute;left:220px;top:713px;width:460px;height:90px;border-radius:50%;border:7px solid #e0322b;opacity:0;transform:rotate(-2deg)");
  tl.fromTo(ring, { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, w(61) + 0.05);
  const x = el("div", "big", "left:690px;top:670px;font-size:130px;color:#e0322b;text-shadow:none", "✗"); pop(x, w(62), B("s09") - 0.08, 0.3);
  chip("1993: A GAP WAS FOUND IN THE FIRST VERSION", 60, 1100, "#ffb547", w(62), B("s09") - 0.08); out([pg, ring], B("s09") - 0.06); })();

// ---------- s10 - s12: Lean, the machine inspector (the editor stays across s10 and s11) ----------
CURP = null;
(function () { const code = ["theorem flt_pinned (n : ℕ)", "  (hn : 3 ≤ n) (a b c : ℕ)", "  (ha : 0 < a) (hb : 0 < b)", "  (hc : 0 < c) :", "  a ^ n + b ^ n ≠ c ^ n"];
  const t = el("div", "term", "left:40px;top:470px;width:1000px",
    `<div class="tb"><i></i><i></i><i></i><span>FinalCheck.lean</span></div>` + code.map((l, i) => `<div class="tl" id="cl${i}" style="font-size:44px">${l.replace(/ /g, "&nbsp;")}<span class="g ck" style="opacity:0"> ✓</span></div>`).join("") +
    `<div class="tl d" id="cl5" style="display:none">&gt; #print axioms</div><div class="tl g" id="cl6" style="display:none;white-space:normal;font-size:36px">✓ depends on axioms: [propext, Classical.choice, Quot.sound]</div>`);
  tl.fromTo(t, { opacity: 0, scale: 0.7, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: E }, A("s10") + 0.02);
  let tt = A("s10") + 0.2; code.forEach((l, i) => { const n = $("#cl" + i); const k = n.firstChild; const sp = el("span", "", "", l.replace(/ /g, "&nbsp;")); n.replaceChild(sp, k);
    typeOn(sp, tt, 0.02); tt += l.length * 0.02 + 0.04; });
  tl.fromTo(t, { y: 0 }, { y: -20, duration: B("s10") - A("s10"), ease: "none", immediateRender: false }, A("s10"));
  CURP = OV("s10"); chip("LEAN: CODE A COMPUTER CAN CHECK", 60, 1100, "var(--lime)", w(66), B("s10") - 0.08);
  // s11: a searching orb reads every line; each gets a tick
  CURP = OV("s11");
  const c = canvasEl(420, 286, 240, 180); paint(c, A("s11"), B("s11") - 0.06, (x, t2) => orb(x, 120, 90, 72, t2, { mode: "search", speed: 1.4 }));
  chip("THE INSPECTOR = A MACHINE", 60, 1100, "var(--lime)", w(70), B("s11") - 0.08);
  CURP = null;
  const scan = el("div", "", "position:absolute;left:40px;top:560px;width:1000px;height:66px;background:linear-gradient(180deg,rgba(124,196,255,0),rgba(124,196,255,0.28),rgba(124,196,255,0));opacity:0");
  tl.set(scan, { opacity: 1 }, A("s11")); tl.fromTo(scan, { y: 0 }, { y: 300, duration: w(73) - A("s11"), ease: "none", immediateRender: false }, A("s11")); out(scan, w(73) + 0.05);
  document.querySelectorAll("#cl0 .ck, #cl1 .ck, #cl2 .ck, #cl3 .ck, #cl4 .ck").forEach((k, i) => tl.to(k, { opacity: 1, duration: 0.1 }, A("s11") + 0.1 + i * (w(73) - A("s11")) / 5));
  tl.set(["#cl5", "#cl6"], { display: "block", opacity: 0 }, w(73) - 0.01); tl.to("#cl5", { opacity: 1, duration: 0.1 }, w(73)); tl.to("#cl6", { opacity: 1, duration: 0.15 }, w(73) + 0.15);
  tl.to(t, { y: -110, duration: 0.3, ease: "power2.inOut" }, w(73));
  tl.to(t, { scale: 1.3, filter: "blur(16px)", opacity: 0, duration: 0.22, ease: "power2.in" }, B("s11") - 0.2); })();
shot("s12");
(function () { const rows = 4, cols = 6, bw = 128, bh = 60, X0 = 120, Y0 = 470, gap = 12;
  let s = ""; for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) { if (j === 1 && i === 3) continue;
    s += `<rect x="${i * (bw + gap) + (j % 2 ? 40 : 0)}" y="${j * (bh + gap)}" width="${bw}" height="${bh}" rx="7" fill="#b85d38" stroke="#c8ff4d" stroke-width="3"/>`; }
  const wall = svgEl(X0, Y0, 900, 300, s);
  tl.fromTo(wall, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, A("s12") + 0.03);
  const gx = X0 + 3 * (bw + gap) + 40, gy = Y0 + bh + gap;
  const rb = el("div", "", `position:absolute;left:${gx}px;top:${gy}px;width:${bw}px;height:${bh}px;border-radius:7px;background:#e0322b;border:3px solid #ffb0a8;opacity:0;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:40px;color:#fff`, "?");
  tl.set(rb, { x: 640, y: -260, rotation: 30 }, 0); tl.set(rb, { opacity: 1 }, w(75));
  tl.to(rb, { x: 0, y: 0, rotation: 0, duration: w(77) - w(75) - 0.05, ease: "power2.in" }, w(75));
  tl.to(rb, { x: 520, y: -360, rotation: -40, duration: 0.45, ease: "power2.out" }, w(77) - 0.05);
  for (let k = 0; k < 6; k++) tl.set(wall, { x: (k % 2 ? -1 : 1) * 12 * (1 - k / 6) }, w(77) - 0.05 + k * 0.035); tl.set(wall, { x: 0 }, w(77) + 0.2);
  stamp("REJECTED", 330, 330, -5, "#ff4d4d", w(77), B("s12") - 0.04, 84, "rgba(11,12,16,0.9)");
  chip("NOTHING GETS PAST IT", 60, 1100, "var(--lime)", w(76), B("s12") - 0.08); out([wall, rb], B("s12") - 0.06); })();

// ---------- s13 - s16: September ----------
shot("s13");
logoDraw("claude", 830, 300, 170, 140, w(81) - 0.05, B("s13") - 0.08);
chip("SEP 2026 · CLAUDE AGENTS", 60, 1060, "var(--lime)", w(80), w(86) - 0.05);
strip("r_lead", { p: 0, y: 1030, sc: 0.62, lines: 1.6, t0: w(86) - 0.1, t1: B("s13") - 0.06, th: w(87) - 0.1 });
shot("s14");
(function () { const c = el("div", "big", "left:0;width:1080px;text-align:center;top:320px;font-size:150px;color:var(--lime)", "<span id='m13'>0</span>");
  const l = el("div", "big", "left:0;width:1080px;text-align:center;top:480px;font-size:52px;color:#fff;font-family:Mono, monospace;letter-spacing:0.06em", "LINES OF LEAN CODE");
  tl.fromTo([c, l], { opacity: 0 }, { opacity: 1, duration: 0.15 }, A("s14") + 0.02);
  count($("#m13"), 0, 13000000, A("s14") + 0.05, w(90) + 0.05 - A("s14"), fmtInt, "power3.in"); punch("s14", w(90) + 0.05, 0.06);
  const cv = canvasEl(60, 570, 960, 330);
  paint(cv, A("s14") + 0.05, B("s14") - 0.06, (x, t) => { for (let i = 0; i < 26; i++) { const y = ((i * 26 - (t - A("s14")) * 900) % 676 + 676) % 676 - 13; if (y > 330) continue;
      const wd = 120 + ((i * 7919) % 600), ind = ((i * 31) % 4) * 40; x.fillStyle = `rgba(${LIME},${0.15 + 0.25 * ((i * 13) % 3) / 2})`; x.fillRect(ind, y, wd, 12); } });
  strip("r_13m", { p: 1, y: 940, sc: 0.62, lines: 1.6, t0: w(89) + 0.3, t1: B("s14") - 0.06, th: w(90) + 0.1 });
  out([c, l], B("s14") - 0.06); })();
shot("s15");
(function () { const p = el("div", "person", "left:110px;top:560px;transform:scale(1.35);transform-origin:0 0"); tl.fromTo(p, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.3, ease: E }, A("s15") + 0.03);
  const cv = canvasEl(400, 380, 660, 620);
  paint(cv, A("s15") + 0.05, B("s15") - 0.06, (x, t) => { const k = ease(ramp(t, w(94), w(95) + 0.3));
    for (let i = 0; i < 12; i++) { const cx = 110 + (i % 4) * 150 - k * 40 + Math.sin(t * 2 + i) * 6, cy = 120 + Math.floor(i / 4) * 190 + Math.cos(t * 2 + i) * 6; orb(x, cx, cy, 46, t, { speed: 1, t0: i }); } });
  const ln = svgEl(330, 520, 300, 360, `<path d="M0 180 C 100 180, 140 60, 290 50 M0 180 H 290 M0 180 C 100 180, 140 300, 290 310" fill="none" stroke="#e8e9ee" stroke-width="5" stroke-dasharray="12 10"/>`);
  tl.fromTo(ln, { opacity: 0 }, { opacity: 1, duration: 0.25 }, w(94) - 0.05);
  chip("+ A RESEARCHER GUIDING THEM", 60, 1100, "#7cc4ff", w(93), B("s15") - 0.08); out([p, ln], B("s15") - 0.06); })();
shot("s16");
(function () { const cal = el("div", "", "position:absolute;left:340px;top:360px;width:400px;height:420px;border-radius:30px;background:#f6f4ee;opacity:0;overflow:hidden;box-shadow:0 40px 90px rgba(0,0,0,0.6)",
    `<div style="height:110px;background:#e0322b;color:#fff;font-family:Mono, monospace;font-weight:700;font-size:44px;letter-spacing:0.12em;display:flex;align-items:center;justify-content:center">DAY</div>
     <div id="dayn" style="text-align:center;font-weight:900;font-size:230px;line-height:300px;color:#1b1c22">1</div>`);
  tl.fromTo(cal, { opacity: 0, rotationX: -40, y: 40 }, { opacity: 1, rotationX: 0, y: 0, duration: 0.3, ease: E }, A("s16") + 0.02);
  count($("#dayn"), 1, 11, A("s16") + 0.1, w(97) - A("s16") - 0.1, fmtInt, "power1.in");
  bigLetters("11 DAYS", 0, 830, 150, "var(--lime)", w(97) - 0.05, B("s16") - 0.05, 1080); out(cal, B("s16") - 0.06); })();

// ---------- s17 - s20: this week, 1,000 copies, one boss ----------
shot("s17");
chip("THIS WEEK · 9 NOV 2026", 60, 700, "#ffffff", A("s17") + 0.15, w(102));
chip("ANTHROPIC'S OWN REPORT · AN EARLY VERSION", 60, 700, "#ffb547", w(102) + 0.05, B("s17") - 0.08);
logoDraw("anthropic", 90, 800, 300, 140, w(100) - 0.05, B("s17") - 0.08);
logoDraw("claude", 420, 800, 140, 140, w(104) - 0.05, B("s17") - 0.08);
(function () { const n = el("div", "big", "left:600px;top:822px;font-size:86px;color:#fff;text-transform:none", "Fable 5.2"); pop(n, w(105) - 0.05, B("s17") - 0.08, 0.6); })();
shot("s18");
(function () { const cv = canvasEl(60, 330, 960, 700);
  const P = [w(107), w(108) + 0.08, w(108) + 0.22];   // 10, 100, then 1,000 on "THOUSAND"
  paint(cv, A("s18") + 0.02, B("s18") - 0.04, (x, t) => { const n = t < P[0] ? 1 : t < P[1] ? 10 : t < P[2] ? 100 : 1000;
    if (n === 1) { orb(x, 480, 350, 160, t, {}); return; }
    if (n === 1000) { field(x, t, { a: 1 }); return; }
    const cols = n === 10 ? 5 : 10, rows = n / cols, dx = 960 / cols, dy = 700 / rows;
    for (let i = 0; i < n; i++) orb(x, dx * (i % cols + 0.5), dy * (Math.floor(i / cols) + 0.5), Math.min(dx, dy) * 0.33, t, { speed: 1, t0: i }); });
  plate("×<span id='cx'>1</span>", 290, 1060, 500, 110, "var(--lime)", A("s18") + 0.03, B("s18") - 0.06);
  [[P[0], "10"], [P[1], "100"], [P[2], "1,000"]].forEach(([d, v]) => tl.set("#cx", { textContent: v }, d)); punch("s18", P[2], 0.05); })();
shot("s19");
(function () { const cv = canvasEl(60, 330, 960, 700); paint(cv, A("s19"), B("s19") - 0.04, (x, t) => field(x, t, { a: 0.3, col: LIME }));
  const p = el("div", "person", "left:440px;top:400px;transform:scale(1.3);transform-origin:0 0"); tl.fromTo(p, { opacity: 0 }, { opacity: 1, duration: 0.15 }, A("s19") + 0.02);
  const s1 = el("div", "strike", "left:400px;top:520px;width:280px"), s2 = el("div", "strike", "left:400px;top:520px;width:280px");
  tl.set(s1, { rotation: 45, scaleX: 0, transformOrigin: "50% 50%" }, 0); tl.set(s2, { rotation: -45, scaleX: 0, transformOrigin: "50% 50%" }, 0);
  tl.to([s1, s2], { scaleX: 1, duration: 0.2, stagger: 0.08 }, w(111) + 0.05); tl.to(p, { opacity: 0.25, duration: 0.3 }, w(111) + 0.2);
  bigLetters("NO RESEARCHER", 0, 800, 120, "#fff", w(110) + 0.05, B("s19") - 0.04, 1080); out([p, s1, s2], B("s19") - 0.04); })();
shot("s20");
(function () { const BX = 540, BY = 140;   // canvas coords; the canvas starts at y 280
  const cv = canvasEl(0, 280, 1080, 840);
  const helpers = []; for (let i = 0; i < 999; i++) { const a = (i * 2.39996) % 6.2832, rr = 0.22 + 0.78 * Math.sqrt(i / 999);
    helpers.push([540 + Math.cos(a) * rr * 470, 560 + Math.sin(a) * rr * 225]); }
  paint(cv, A("s20") + 0.02, B("s20") - 0.04, (x, t) => { const n = Math.floor(999 * ease(ramp(t, w(115) - 0.1, w(119))));
    x.strokeStyle = `rgba(${LIME},0.22)`; x.lineWidth = 2;
    for (let g = 0; g < 9; g++) { const a = (g + 0.5) / 9 * 6.2832, kk = ease(ramp(t, w(114) + g * 0.04, w(115) + 0.3 + g * 0.04)); if (kk <= 0) continue;
      const ex = 540 + Math.cos(a) * 470, ey = 560 + Math.sin(a) * 225; x.beginPath(); x.moveTo(BX, BY); x.lineTo(BX + (ex - BX) * kk, BY + (ey - BY) * kk); x.stroke(); }
    for (let i = 0; i < n; i++) { const [hx, hy] = helpers[i]; mini(x, hx, hy, 6, t, i, LIME, 0.75 + 0.25 * Math.sin(t * 3 + i)); }
    orb(x, BX, BY, 95, t, { speed: 1.1 }); });
  const bl = el("div", "tag", "left:470px;top:530px;font-size:28px;background:#0b0c10;border:2px solid var(--lime);color:var(--lime);width:140px;text-align:center", "1 BOSS");
  show(bl, w(113), B("s20") - 0.08);
  plate("<span id='hcn'>0</span> <span style='font-size:56px;color:#fff'>HELPERS</span>", 240, 1090, 600, 84, "var(--lime)", w(115) - 0.1, B("s20") - 0.06, "padding:8px 0 12px");
  count($("#hcn"), 0, 999, w(115) - 0.1, w(119) - w(115) + 0.1, fmtInt, "power2.out"); })();

// ---------- s21 - s26: the twist, on the building's wall of 60 bricks (the wall stays across the six shots) ----------
CURP = null;
const BOARD = (function () { const root = el("div", "", "position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0");
  const tiles = []; const TW = 136, TH = 58, PX = 148, PY = 70, X0 = 70, Y0 = 336;
  const DONE3 = [7, 22, 41], WORK = [2, 9, 15, 20, 28, 33, 38, 46, 51, 57];
  for (let k = 0; k < 60; k++) { const i = k % 6, j = Math.floor(k / 6), x = X0 + i * PX + (j % 2 ? 60 : 0), y = Y0 + j * PY;
    const t = el("div", "tile brick", `left:${x}px;top:${y}px;width:${TW}px;height:${TH}px;opacity:0`, "", root);
    tiles.push({ el: t, k, x, y, kind: DONE3.includes(k) ? "done" : WORK.includes(k) ? "work" : "red" }); }
  return { root, tiles, TW, TH }; })();
(function () { const { root, tiles } = BOARD; const T21 = A("s21"), T26 = B("s26");
  tl.set(root, { opacity: 1 }, T21); out(root, T26 - 0.06);
  // the wall's 60 empty slots wait under "THE TWIST?"; on "sixty" they light up one by one
  tiles.forEach((t) => tl.set(t.el, { transformOrigin: "0px 0px" }, 0));
  tl.fromTo(tiles.map((t) => t.el), { opacity: 0 }, { opacity: 0.35, duration: 0.3 }, T21 + 0.05);
  CURP = OV("s21");
  const tw = el("div", "big", "left:0;width:1080px;text-align:center;top:560px;font-size:150px;color:#ffb547;padding:10px 0;background:rgba(11,12,16,0.85)", "THE TWIST?");
  tl.fromTo(tw, { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, w(120) + 0.02); out(tw, w(122) + 0.1);
  plate("<span id='n60'>0</span> <span style='font-size:44px;color:#fff'>PARTS</span>", 340, 1076, 400, 70, "#fff", w(126) - 0.1, B("s21") - 0.06, "padding:4px 0 8px");
  count($("#n60"), 0, 60, w(126) - 0.1, 0.75, fmtInt, "none");
  const cv = canvasEl(60, 300, 960, 760); // three searching orbs read the parts
  paint(cv, w(123), B("s21") - 0.06, (x, t) => { for (let i = 0; i < 3; i++) orb(x, 480 + Math.sin(t * 1.3 + i * 2.1) * 360, 380 + Math.cos(t * 0.9 + i * 1.7) * 300, 46, t, { mode: "search", speed: 1.4, t0: i }); });
  CURP = null;
  tl.to(tiles.map((t) => t.el), { opacity: 1, duration: 0.15, stagger: { each: 0.012, from: "start" } }, w(126) - 0.1);
  // s22: 47 parts judged "can't be done in time"
  const reds = tiles.filter((t) => t.kind === "red"), done = tiles.filter((t) => t.kind === "done"), work = tiles.filter((t) => t.kind === "work");
  const tR = w(130) - 0.05; reds.forEach((t, n) => { const at = tR + ((n * 17) % 47) / 47 * 0.9; tl.set(t.el, { className: "tile brick red" }, at); tl.fromTo(t.el, { scale: 1.2 }, { scale: 1, duration: 0.2, immediateRender: false }, at); });
  CURP = OV("s22");
  plate("<span id='n47'>0</span> <span style='font-size:44px;color:#fff'>OF 60</span>", 340, 1076, 400, 70, "#ff6b6b", w(130) - 0.05, B("s22") - 0.06, "padding:4px 0 8px");
  count($("#n47"), 0, 47, tR, 0.95, fmtInt, "none");
  stamp("CAN'T BE DONE", 215, 600, -6, "#ff4d4d", w(131), B("s22") - 0.04, 92, "rgba(11,12,16,0.92)");
  CURP = null;
  // s23: the boss sets the 47 aside (a pallet) and puts nearly everyone on the other 10
  const tA = w(138) - 0.05;
  reds.forEach((t, n) => { const i = n % 8, j = Math.floor(n / 8);
    tl.to(t.el, { x: 70 + i * 66 - t.x, y: 790 + j * 36 - t.y, scaleX: 0.43, scaleY: 0.48, duration: 0.5, ease: "power2.inOut" }, tA + n * 0.008); });
  done.forEach((t, n) => { tl.set(t.el, { className: "tile brick ok" }, w(141)); tl.to(t.el, { x: 640 + n * 66 - t.x, y: 790 - t.y, scaleX: 0.43, scaleY: 0.48, duration: 0.5, ease: "power2.inOut" }, tA); });
  work.forEach((t, n) => { const i = n % 5, j = Math.floor(n / 5); t.wx = 70 + i * 188 + (j ? 60 : 0); t.wy = 380 + j * 110;
    tl.to(t.el, { x: t.wx - t.x, y: t.wy - t.y, scale: 1.25, duration: 0.55, ease: "power3.inOut" }, w(141) - 0.1); });
  const shelf = el("div", "tag", "left:70px;top:1010px;font-size:24px", "SET ASIDE · 47", root); show(shelf, w(139), T26 - 0.1);
  const donel = el("div", "tag", "left:640px;top:840px;font-size:22px;background:#0b0c10;border:2px solid var(--lime);color:var(--lime)", "3 ALREADY DONE", root); show(donel, w(141), w(154));
  const streams = (x, t, t0, t1, targets, n, back) => { for (let i = 0; i < n; i++) { const st = t0 + (i / n) * (t1 - t0); const k = ramp(t, st, st + 0.55); if (k <= 0 || k >= 1) continue;
      const tg = targets[i % targets.length], sx = 540 + Math.sin(i * 12.9) * 520, sy = back ? 300 : -40, e2 = ease(k);
      mini(x, sx + (tg[0] - sx) * e2, sy + (tg[1] - sy) * e2, 7, t, i, LIME, 1 - k * 0.4); } };
  CURP = OV("s23");
  paint(canvasEl(0, 280, 1080, 900), w(142), B("s23") - 0.06, (x, t) => streams(x, t, w(142), w(148), work.map((q) => [q.wx + 85, q.wy + 36 - 280]), 160));
  chip("NEARLY EVERY HELPER → THE OTHER 10", 60, 1080, "var(--lime)", w(143), B("s23") - 0.08);
  CURP = null;
  // s24: the ten are done in about 70 minutes
  work.forEach((t, n) => { const at = w(149) + n * (w(153) - w(149)) / 10; tl.set(t.el, { className: "tile brick ok" }, at); tl.set(t.el, { innerHTML: "<div style='text-align:center;font-weight:900;font-size:42px;line-height:54px;color:#0b0c10'>✓</div>" }, at);
    tl.fromTo(t.el, { scale: 1.45 }, { scale: 1.25, duration: 0.25, immediateRender: false }, at); });
  CURP = OV("s24");
  plate("<span id='clk'>0</span> <span style='font-size:60px;color:#fff'>MIN</span>", 290, 580, 500, 120, "var(--lime)", A("s24") + 0.05, B("s24") - 0.06, "padding:6px 0 10px");
  count($("#clk"), 0, 70, w(149), w(153) - w(149) + 0.2, fmtInt, "power1.inOut");
  strip("e_70min", { p: 0, y: 1062, sc: 0.8, lines: 1.3, t0: w(151), t1: B("s24") - 0.06, th: w(152) });
  CURP = null;
  // s25: the wall steps back for the boss's message
  tl.to(root, { opacity: 0, duration: 0.2 }, A("s25") - 0.1); tl.to(root, { opacity: 1, duration: 0.25 }, A("s26") - 0.1);
  // s26: back to the hard ones; most of them get laid
  CURP = OV("s26");
  paint(canvasEl(0, 280, 1080, 900), A("s26"), B("s26") - 0.06, (x, t) => streams(x, t, A("s26"), w(171), reds.map((q, n) => [70 + (n % 8) * 66 + 29, 790 + Math.floor(n / 8) * 36 + 14 - 280]), 140, true));
  chip("NO REASON TO IDLE", 60, 1080, "var(--lime)", w(165), B("s26") - 0.08);
  CURP = null;
  reds.slice(0, 41).forEach((t, n) => { const at = w(166) + ((n * 13) % 41) / 41 * (B("s26") - w(166) - 0.3); tl.set(t.el, { className: "tile brick ok" }, at); });
  tl.set(shelf, { textContent: "BACK ON THE “IMPOSSIBLE” ONES" }, A("s26")); })();
shot("s25");
(function () { const cv = canvasEl(415, 286, 250, 250); paint(cv, A("s25") + 0.02, B("s25") - 0.06, (x, t) => orb(x, 125, 125, 90, t, { mode: "think", speed: 1.3 }));
  const q = el("div", "quote", "left:60px;top:560px;width:960px;padding:36px 46px 40px", `<div class="qk">THE BOSS AI WROTE TO ITS HELPERS:</div><div id="qidle" style="font-weight:900;font-size:100px;line-height:0.98;letter-spacing:-0.03em;color:#1b1c22;text-transform:uppercase">“There is no reason to idle.”</div>`);
  tl.fromTo(q, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.5)" }, w(157) - 0.12);
  const n = window.SplitText ? new SplitText("#qidle", { type: "words" }).words : []; tl.set(n, { opacity: 0 }, 0);
  n.forEach((wd, i) => { tl.set(wd, { opacity: 1 }, w(158 + Math.min(i, 5)) - 0.02); tl.fromTo(wd, { y: 18 }, { y: 0, duration: 0.15, immediateRender: false }, w(158 + Math.min(i, 5)) - 0.02); });
  strip("e_idle", { p: 0, y: 1030, sc: 0.62, lines: 1.3, t0: w(162), t1: B("s25") - 0.06, th: w(162) + 0.2 }); out(q, B("s25") - 0.06); })();

// ---------- s27 - s28: under 30 hours; the inspector passes the whole building ----------
shot("s27");
(function () { plate("<span id='hrs'>0.0</span> <span style='font-size:70px;color:#fff'>HOURS</span>", 190, 360, 700, 150, "var(--lime)", A("s27") + 0.03, B("s27") - 0.06, "padding:6px 0 14px");
  count($("#hrs"), 0, 28.7, A("s27") + 0.05, w(176) + 0.3 - A("s27"), (v) => v.toFixed(1), "power2.out");
  chip("LESS THAN 30 HOURS · NO RESEARCHER", 60, 1100, "var(--lime)", w(174), B("s27") - 0.08); })();
shot("s28");
(function () { const f = temple(120, 330, 1.0, { t0: A("s28") + 0.02, t1: B("s28") - 0.04, a: 0.55, col: "#7cc4ff" });
  // 2,418 tasks fill the building as bricks of light, then the inspector's lens sweeps it
  const cv = canvasEl(120, 330, 840, 600);
  paint(cv, A("s28") + 0.02, B("s28") - 0.04, (x, t) => { const g = ease(ramp(t, A("s28"), w(180) + 0.1)), lit = t > w(181) - 0.05;
    for (let i = 0; i < 2418; i++) { const k = i / 2418; if (k > g) break; const col = lit ? LIME : BLUE;
      let px, py; const u = (i * 0.6180339887) % 1, v = (i * 0.7548776662) % 1;
      if (i < 380) { const yy = 45 + v * 120, half = (yy - 40) / 130 * 340; px = 420 + (u * 2 - 1) * half; py = yy; }
      else if (i < 2100) { const col6 = i % 6; px = 115 + col6 * 122 + u * 50; py = 225 + v * 280; }
      else { px = 30 + u * 780; py = 515 + v * 60; }
      x.fillStyle = `rgba(${col},${lit ? 0.95 : 0.7})`; x.fillRect(px, py, 6, 4); } });
  const mag = el("div", "", "position:absolute;left:0;top:0;width:180px;height:180px;border-radius:50%;border:9px solid #fff;opacity:0;box-shadow:0 0 30px rgba(255,255,255,0.4), inset 0 0 40px rgba(255,255,255,0.25)");
  tl.set(mag, { x: 140, y: 600, opacity: 1 }, A("s28") + 0.1); tl.to(mag, { x: 760, y: 420, duration: w(181) - A("s28") - 0.2, ease: "power1.inOut" }, A("s28") + 0.1);
  tl.to(mag, { x: 450, y: 380, scale: 1.4, opacity: 0, duration: 0.3 }, w(181) - 0.1);
  const tag = el("div", "tag", "left:330px;top:960px;font-size:26px;background:#0b0c10;border:2px solid #7cc4ff;color:#7cc4ff", "2,418 TASKS · 10 LEVELS DEEP"); show(tag, A("s28") + 0.1, w(181) + 0.02);
  const ck = el("div", "big", "left:0;width:1080px;text-align:center;top:480px;font-size:240px;color:var(--lime);text-shadow:0 0 50px rgba(200,255,77,0.8)", "✓");
  tl.fromTo(ck, { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, w(181)); out(ck, B("s28") - 0.04);
  tl.to(f, { opacity: 1, duration: 0.2 }, w(181)); tl.set(f.querySelector("g"), { attr: { stroke: "#c8ff4d" } }, w(181));
  flash(w(181) + 0.18, 0.3, 0.4, "#c8ff4d"); punch("s28", w(181) + 0.18, 0.06);
  strip("e_done", { p: 1, y: 990, sc: 0.62, lines: 1.6, t0: w(181) + 0.1, t1: B("s28") - 0.06, th: w(182) + 0.1 }); })();

// ---------- s29 - s31: the catch ----------
shot("s29");
(function () { const tc = el("div", "big", "left:0;width:1080px;text-align:center;top:420px;font-size:150px;color:#ffb547", "THE CATCH?");
  tl.fromTo(tc, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.out" }, w(185) - 0.02); punch("s29", w(185), 0.07);
  tl.to(tc, { y: -120, scale: 0.6, opacity: 0, duration: 0.3, ease: "power2.in" }, w(186) + 0.05);
  const wc = el("div", "wcard", "left:260px;top:430px;width:560px;text-align:center;border-color:#ffb547", `<div class="k">THE ROUTE: A HUMAN PROOF, 1995</div><div class="n">ANDREW WILES</div>`);
  tl.fromTo(wc, { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.7)" }, w(186) + 0.25); out(wc, B("s29") - 0.06);
  chip("HUMANS DESIGNED THE BUILDING", 60, 1100, "#ffb547", w(187), B("s29") - 0.08); })();
shot("s30");
(function () { temple(120, 330, 1.0, { t0: A("s30") + 0.05, t1: B("s30") - 0.06, a: 0.75, col: "#ffb547" });
  // 60 checkpoints on the building, then the one-line map drawn across it
  const pts = []; for (let i = 0; i < 60; i++) { let px, py; const u = ((i * 0.618) % 1);
    if (i < 12) { px = 120 + 80 + u * 680; py = 330 + 170 - (1 - Math.abs((80 + u * 680) - 420) / 340) * 120; }
    else if (i < 48) { const c6 = (i - 12) % 6, r = Math.floor((i - 12) / 6); px = 120 + 140 + c6 * 122; py = 330 + 250 + r * 45; }
    else { px = 120 + 40 + (i - 48) / 12 * 760; py = 330 + 545; } pts.push([px, py]); }
  const flags = pts.map(([px, py]) => el("div", "", `position:absolute;left:${px - 2}px;top:${py - 30}px;width:24px;height:32px;opacity:0`,
    `<svg width="24" height="32"><line x1="2" y1="0" x2="2" y2="32" stroke="#fff" stroke-width="3"/><path d="M3 2 H22 L16 8 L22 14 H3 Z" fill="#c8ff4d"/></svg>`));
  flags.forEach((fl, i) => tl.fromTo(fl, { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.15, ease: "back.out(2)" }, w(199) + (i / 60) * 0.7));
  const route = svgEl(120, 330, 840, 600, `<path d="M20 575 C 200 560, 160 420, 260 380 S 420 260, 420 60 S 620 300, 800 520" fill="none" stroke="#c8ff4d" stroke-width="9" stroke-linecap="round" stroke-dasharray="1600" stroke-dashoffset="1600" style="filter:drop-shadow(0 0 10px #c8ff4d)"/>`);
  tl.set(route, { opacity: 1 }, w(202) - 0.05); tl.to(route.querySelector("path"), { attr: { "stroke-dashoffset": 0 }, duration: 0.8, ease: "power2.inOut" }, w(202) - 0.05);
  plate("<span id='cp60'>0</span> <span style='font-size:44px;color:#fff'>CHECKPOINTS</span>", 190, 990, 700, 70, "var(--lime)", w(199) - 0.05, w(202) - 0.1, "padding:4px 0 8px");
  count($("#cp60"), 0, 60, w(199), 0.7, fmtInt, "none");
  plate("A ONE-LINE MAP", 190, 990, 700, 70, "var(--lime)", w(202), B("s30") - 0.08, "padding:4px 0 8px");
  chip("A HEAD START", 60, 330, "#ffb547", w(195), B("s30") - 0.08);
  out([...flags, route], B("s30") - 0.06); })();
shot("s31");
(function () { const pnl = el("div", "panel", "left:120px;top:330px;width:840px;height:560px");
  tl.fromTo(pnl, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, A("s31") + 0.03); out(pnl, B("s31") - 0.06);
  const n = el("div", "big", "left:150px;top:350px;font-size:120px;color:var(--lime)", "<span id='b47'>0</span>"); tl.fromTo(n, { opacity: 0 }, { opacity: 1, duration: 0.15 }, A("s31") + 0.1);
  const lb = el("div", "big", "left:390px;top:385px;font-size:46px;color:#fff;font-family:Mono, monospace;letter-spacing:0.04em", "ALREADY LAID"); tl.fromTo(lb, { opacity: 0 }, { opacity: 1, duration: 0.15 }, A("s31") + 0.1);
  const bricks = []; for (let k = 0; k < 47; k++) { const i = k % 8, j = Math.floor(k / 8);
    bricks.push(el("div", "", `position:absolute;left:${160 + i * 96 + (j % 2 ? 24 : 0)}px;top:${530 + j * 56}px;width:84px;height:44px;border-radius:6px;background:#b85d38;border:3px solid #c8ff4d;opacity:0;box-shadow:0 0 12px rgba(200,255,77,0.4)`)); }
  const t0 = w(204); bricks.forEach((b, k) => tl.fromTo(b, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }, t0 + k * 0.022));
  count($("#b47"), 0, 47, t0, 47 * 0.022 + 0.15, fmtInt, "none");
  chip("47 PIECES, PROVED BACK IN SEPTEMBER", 60, 1100, "var(--lime)", w(206), B("s31") - 0.08); out([n, lb, ...bricks], B("s31") - 0.06); })();

// ---------- s32 - s35: the lesson, the reminders, the takeaway ----------
shot("s32");
(function () { logoDraw("anthropic", 60, 300, 260, 110, A("s32") + 0.05, B("s32") - 0.08);
  const cv = canvasEl(760, 286, 230, 230);
  paint(cv, A("s32") + 0.02, B("s32") - 0.06, (x, t) => { const k = ramp(t, w(211), w(217)); orb(x, 115, 115, 80, t, { mode: "think", speed: 1.3 - 1.2 * k, a: 1 - 0.6 * k, col: mixc(LIME, GRAY, k), pulse: 1 - k }); });
  const q = el("div", "quote", "left:60px;top:540px;width:960px;padding:36px 46px 40px", `<div class="qk">ANTHROPIC'S LESSON, IN ITS OWN WORDS:</div><div id="qgive" style="font-weight:900;font-size:84px;line-height:1.0;letter-spacing:-0.03em;color:#1b1c22;text-transform:uppercase">“Agents tend to give up on hard problems.”</div>`);
  tl.fromTo(q, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.5)" }, w(209) - 0.1);
  const n = window.SplitText ? new SplitText("#qgive", { type: "words" }).words : []; tl.set(n, { opacity: 0 }, 0);
  const at = [210, 210, 210, 211, 212, 213, 214, 215]; n.forEach((wd, i) => tl.set(wd, { opacity: 1 }, w(at[Math.min(i, at.length - 1)]) - 0.02 + (i < 3 ? i * 0.08 : 0)));
  strip("e_lesson", { p: 2, y: 1030, sc: 0.62, lines: 1.3, t0: w(216), t1: B("s32") - 0.06, th: w(216) + 0.25 }); out(q, B("s32") - 0.06); })();
shot("s33");
(function () { const cv = canvasEl(390, 290, 300, 300);
  paint(cv, A("s33") + 0.02, B("s33") - 0.06, (x, t) => { const k = ramp(t, w(219), w(227) + 0.2); orb(x, 150, 150, 100, t, { mode: "think", speed: 0.1 + 1.4 * k, a: 0.4 + 0.6 * k, col: mixc(GRAY, LIME, k), pulse: k }); });
  const nb = el("div", "big", "left:740px;top:330px;font-size:150px;color:var(--lime)", "<span id='n19'>0</span>"); tl.fromTo(nb, { opacity: 0 }, { opacity: 1, duration: 0.15 }, w(218) - 0.05);
  const t0 = w(218) + 0.1, t1 = w(227) + 0.05, notes = [];
  // a stack: two blank cards behind; only the newest reminder shows its text
  const ghosts = [2, 1].map((d) => el("div", "notif", `top:${640 + d * 22}px;left:${150 + d * 24}px;width:${780 - d * 48}px;height:104px;opacity:0;background:rgba(245,245,242,${0.5 - d * 0.15})`, ""));
  ghosts.forEach((g, j) => { tl.fromTo(g, { opacity: 0 }, { opacity: 1, duration: 0.12 }, t0 + (1 + j) * (t1 - t0) / 18); });
  for (let i = 0; i < 19; i++) { const at = t0 + i * (t1 - t0) / 18;
    const nf = el("div", "notif", "top:640px", `<div class="ic">⏱</div><div class="tx">Time check: keep going<span>Automatic reminder ${i + 1} of 19</span></div>`);
    tl.fromTo(nf, { opacity: 0, y: -40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.1, ease: "back.out(2)" }, at);
    if (notes.length) tl.set(notes[notes.length - 1], { opacity: 0 }, at);
    notes.push(nf); tl.set("#n19", { textContent: String(i + 1) }, at); }
  strip("e_19", { p: 0, y: 1000, sc: 0.62, lines: 1.8, t0: w(225), t1: B("s33") - 0.06, th: w(225) + 0.3 });
  out([nb, ...notes, ...ghosts], B("s33") - 0.06); })();
shot("s34");
(function () { const cv = canvasEl(40, 330, 150, 150); paint(cv, A("s34") + 0.02, B("s34") - 0.06, (x, t) => orb(x, 75, 75, 52, t, { mode: "think", speed: t > w(240) ? 1.6 : 0.4, a: t > w(240) ? 1 : 0.55 }));
  const b1 = el("div", "bubble bot", "left:200px;top:350px;max-width:800px;font-size:56px;font-weight:800", "<span id='bb1'>That can't be done.</span>");
  tl.fromTo(b1, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2, ease: E }, w(232) - 0.1); typeOn("#bb1", w(232), 0.03);
  const b2 = el("div", "bubble me", "left:500px;top:560px;max-width:520px;font-weight:900;font-size:64px", "<span id='bb2'>Keep going.</span>");
  tl.fromTo(b2, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2, ease: E }, w(237) - 0.1); typeOn("#bb2", w(237), 0.04);
  bigLetters("KEEP GOING", 0, 820, 150, "var(--lime)", w(240), B("s34") - 0.06, 1080); punch("s34", w(240), 0.06);
  out([b1, b2], B("s34") - 0.06); })();
shot("s35");
(function () { const cv = canvasEl(60, 640, 960, 470); paint(cv, A("s35") + 0.02, B("s35") - 0.04, (x, t) => field(x, t, { a: 1 }));
  bigLetters("1 WORD", 0, 360, 170, "#fff", w(243), w(253) - 0.12, 1080);
  bigLetters("SPOTTED IT?", 0, 360, 150, "var(--lime)", w(253), B("s35") - 0.04, 1080);
  chip("COMMENT THE WORD 💬", 60, 1140, "var(--lime)", w(255), B("s35") - 0.08); })();
CURP = null;

// ---------- the painter's clock (after every canvas is registered) ----------
(function () { const clk = { t: 0 };
  tl.fromTo(clk, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate() { const t = clk.t;
    PAINT.forEach((p) => { if (t < p.a - 0.35 || t > p.b + 0.35) return; p.x.clearRect(0, 0, p.c.width, p.c.height); p.fn(p.x, t); }); } }, 0); })();

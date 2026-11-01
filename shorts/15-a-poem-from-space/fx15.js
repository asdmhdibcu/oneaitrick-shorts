// Short #15: what happens on top of each shot (9:16). Inlined into index.html by make_index.py (helpers in index_template.tpl).
// Visuals sit in y 280-1220; captions own 1240-1460; the bottom ~450 px stays clear for the platform buttons.
// No generated media: the globe (d3-geo + Natural Earth land), the satellite, the thermos and the beams are drawn here.
if (window.SplitText) gsap.registerPlugin(SplitText);

const typeOn = (sel, t, per) => { const n = $(sel); if (!n) return;
  const parts = window.SplitText ? new SplitText(n, { type: "words,chars" }).chars : [n];
  tl.set(parts, { opacity: 0 }, 0);
  parts.forEach((c, i) => tl.set(c, { opacity: 1 }, t + i * (per || 0.028))); };
const bigLetters = (txt, x, y, fs, col, t0, t1) => { const b = el("div", "big", `left:${x}px;top:${y}px;font-size:${fs}px;color:${col || "#fff"}`, txt);
  tl.set(b, { opacity: 1 }, t0 - 0.01);
  const parts = window.SplitText ? new SplitText(b, { type: "chars" }).chars : [b];
  tl.fromTo(parts, { opacity: 0, y: 80, scale: 1.6 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2.4)", stagger: 0.05 }, t0);
  tl.to(b, { opacity: 0, duration: 0.15 }, t1); return b; };
const out = (els, t) => tl.to(els, { opacity: 0, duration: 0.15 }, t);
const stamp = (txt, x, y, rot, col, t0, t1, fs) => { const s = el("div", "stamp", `left:${x}px;top:${y}px;transform:rotate(${rot}deg);color:${col};font-size:${fs || 64}px`, txt);
  tl.fromTo(s, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, t0); out(s, t1); return s; };
const logoTile = (file, x, y, wd, ht, t0, t1, parent) => { const d = el("div", "logo", `left:${x}px;top:${y}px;width:${wd}px;height:${ht}px`, `<img src="assets/logos/${file}.png" alt="" />`, parent);
  pop(d, t0, t1, 0.6); return d; };
const svgEl = (x, y, wd, ht, inner, parent) => el("div", "", `position:absolute;left:${x}px;top:${y}px;width:${wd}px;height:${ht}px;opacity:0`,
  `<svg width="${wd}" height="${ht}" viewBox="0 0 ${wd} ${ht}">${inner}</svg>`, parent);
// a small boxy satellite with two solar wings (my drawing; the real one is fridge-sized)
const SAT = (s, glow) => `<g transform="scale(${s})"><rect x="-70" y="-14" width="48" height="28" rx="3" fill="#2a6df4" stroke="#cfe0ff" stroke-width="2"/>
  <rect x="22" y="-14" width="48" height="28" rx="3" fill="#2a6df4" stroke="#cfe0ff" stroke-width="2"/>
  <path d="M-46 -14 V14 M46 -14 V14" stroke="#cfe0ff" stroke-width="1.5"/>
  <rect x="-20" y="-22" width="40" height="44" rx="6" fill="#d9dde6" stroke="#fff" stroke-width="2"/>
  <circle cx="0" cy="0" r="7" fill="${glow || "#c8ff4d"}"/></g>`;
const satEl = (x, y, s, parent) => svgEl(x - 90 * s, y - 40 * s, 180 * s, 80 * s, `<g transform="translate(${90 * s},${40 * s})">${SAT(s)}</g>`, parent);
// the poem, shown as three lines of light (the voice describes it; the words are never shown)
const poemCard = (x, y, t0, t1, lab) => { const c = el("div", "", `position:absolute;left:${x}px;top:${y}px;width:700px;height:400px;border-radius:28px;opacity:0;
    background:rgba(8,12,24,0.88);border:2px solid rgba(200,255,77,0.6);box-shadow:0 0 80px rgba(200,255,77,0.25)`,
    `<div style="position:absolute;left:44px;top:34px;font-family:Mono,monospace;font-weight:700;font-size:24px;letter-spacing:0.14em;color:var(--lime)">${lab || "THE FIRST ANSWER · A HAIKU"}</div>` +
    [0, 1, 2].map((i) => `<div class="pl" style="position:absolute;left:44px;top:${120 + i * 80}px;height:22px;width:${[420, 540, 460][i]}px;border-radius:11px;
      background:linear-gradient(90deg,#fff,#c8ff4d);box-shadow:0 0 24px rgba(200,255,77,0.8);transform-origin:0 50%;transform:scaleX(0)"></div>`).join(""));
  tl.fromTo(c, { opacity: 0, y: -60, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, t0);
  c.querySelectorAll(".pl").forEach((p, i) => tl.to(p, { scaleX: 1, duration: 0.35, ease: "power2.out" }, t0 + 0.2 + i * 0.22));
  out(c, t1); return c; };
const bubble = (txt, x, y, wd, t0, t1) => { const b = el("div", "bubble me", `left:${x}px;top:${y}px;width:${wd}px`, `<span>${txt}</span>`);
  tl.fromTo(b, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, t0); typeOn(`#${b.id = "bb" + Math.round(t0 * 100)} span`, t0 + 0.1, 0.03);
  out(b, t1); return b; };

// ---------- the globe: an orthographic Earth drawn from Natural Earth land (110m), redrawn every frame ----------
const LANDF = (window.topojson && window.LAND) ? topojson.feature(LAND, LAND.objects.land) : null;
const orbitPt = (u, inc, node) => { const lat = Math.asin(Math.sin(inc) * Math.sin(u)), lon = node + Math.atan2(Math.cos(inc) * Math.sin(u), Math.cos(u));
  return [lon * 180 / Math.PI, lat * 180 / Math.PI]; };
const globe = (x, y, size, o) => { const R = size / 2;
  const d = el("div", "", `position:absolute;left:${x}px;top:${y}px;width:${size}px;height:${size}px;opacity:0`,
    `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"><defs><radialGradient id="ocean${x}" cx="40%" cy="35%"><stop offset="0" stop-color="#2f6fb8"/><stop offset="1" stop-color="#0b2a55"/></radialGradient></defs>
     <circle cx="${R}" cy="${R}" r="${R - 2}" fill="url(#ocean${x})"/><path class="ld" fill="#5f8f4e" stroke="#9cc28a" stroke-width="0.6"/>
     <path class="nt" fill="rgba(2,4,14,0.72)"/><path class="gr" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
     <path class="ob" fill="none" stroke="#c8ff4d" stroke-width="3" stroke-dasharray="10 8"/><circle cx="${R}" cy="${R}" r="${R - 2}" fill="none" stroke="rgba(160,200,255,0.6)" stroke-width="4"/>
     <g class="st"><circle r="34" fill="rgba(200,255,77,0.18)"/>${SAT(0.42)}</g><g class="gs"><circle r="10" fill="#ff8a1f"/><circle class="pg" r="10" fill="none" stroke="#ff8a1f" stroke-width="3"/></g></svg>`);
  const proj = d3.geoOrthographic().scale(R - 2).translate([R, R]).clipAngle(90), path = d3.geoPath(proj);
  const q = (c) => d.querySelector(c), grat = d3.geoGraticule10();
  const draw = (p) => { // p: {lon, lat, sunLon, inc, node, u, ground}
    proj.rotate([-p.lon, -p.lat]);
    if (LANDF) q(".ld").setAttribute("d", path(LANDF));
    q(".gr").setAttribute("d", path(grat));
    q(".nt").setAttribute("d", p.sunLon === undefined ? "" : path(d3.geoCircle().center([p.sunLon + 180, 0]).radius(90)()));
    const ring = { type: "LineString", coordinates: d3.range(0, 361, 3).map((a) => orbitPt(a * Math.PI / 180, p.inc, p.node)) };
    q(".ob").setAttribute("d", path(ring));
    const sp = orbitPt(p.u, p.inc, p.node), vis = d3.geoDistance(sp, [p.lon, p.lat]) < Math.PI / 2, xy = proj(sp);
    q(".st").setAttribute("transform", `translate(${xy[0]},${xy[1]})`); q(".st").style.opacity = vis ? 1 : 0;
    if (p.ground) { const g = proj(p.ground), gv = d3.geoDistance(p.ground, [p.lon, p.lat]) < Math.PI / 2;
      q(".gs").setAttribute("transform", `translate(${g[0]},${g[1]})`); q(".gs").style.opacity = gv ? 1 : 0; } else q(".gs").style.opacity = 0; };
  return { d, draw, q }; };
const spin = (G, t0, t1, from, to) => { const s = { k: 0 }; const lerp = (a, b, k) => a + (b - a) * k;
  const at = (k) => { const p = {}; Object.keys(from).forEach((n) => { p[n] = typeof from[n] === "number" ? lerp(from[n], to[n] === undefined ? from[n] : to[n], k) : from[n]; }); return p; };
  G.draw(at(0));
  tl.fromTo(s, { k: 0 }, { k: 1, duration: t1 - t0, ease: "none", onUpdate() { G.draw(at(s.k)); } }, t0); };
const D2R = Math.PI / 180;

// ---------- s01 - s04: the hook ----------
tl.fromTo("#title", { opacity: 1, y: 0 }, { opacity: 1, y: 0, duration: 0.01 }, 0);
tl.to("#title", { opacity: 0, y: -20, duration: 0.2 }, B("s01") - 0.15);
(function () { const s = satEl(260, 1010, 1.4); tl.fromTo(s, { opacity: 1, x: -200, y: 40 }, { x: 640, y: -60, duration: B("s01") + 0.3, ease: "none" }, 0); out(s, B("s01") - 0.05);
  logoTile("google", 60, 860, 120, 120, 0.05, B("s01") - 0.08); })();
(function () { const s = satEl(540, 360, 1.2); tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.2 }, A("s02"));
  const bm = el("div", "", "position:absolute;left:532px;top:400px;width:16px;height:700px;opacity:0;transform-origin:50% 0;background:repeating-linear-gradient(180deg,rgba(200,255,77,0.95) 0 22px,rgba(200,255,77,0) 22px 40px);filter:drop-shadow(0 0 12px #c8ff4d)");
  tl.fromTo(bm, { opacity: 1, scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "power2.out" }, w(10));
  tl.fromTo(bm, { backgroundPositionY: 0 }, { backgroundPositionY: 200, duration: B("s02") - w(10), ease: "none" }, w(10));
  chip("FIRST WORDS FROM SPACE", 60, 1100, "#7cc4ff", w(9), w(17) - 0.1);
  poemCard(190, 520, w(17) - 0.1, B("s02") - 0.08);
  chip("…A POEM", 60, 1100, "var(--lime)", w(17), B("s02") - 0.08);
  out([s, bm], B("s02") - 0.08); })();
(function () { bubble("Write a haiku about being in space.", 230, 560, 640, w(19), B("s03") - 0.08);
  const ar = el("div", "big", "left:500px;top:420px;font-size:90px;color:#7cc4ff", "↑"); show(ar, w(23), B("s03") - 0.08);
  chip("THEY ASKED FOR ONE", 60, 1100, "#7cc4ff", w(23), B("s03") - 0.08); })();
chip("GOOGLE'S PLAN: SATELLITES WORKING AS ONE", 60, 1130, "#ffffff", w(27), w(36) - 0.12);
chip("A REALLY BIG IDEA", 60, 1130, "var(--lime)", w(36) - 0.05, B("s04") - 0.08);

// ---------- s05 - s08: the satellite and what's inside ----------
logoTile("spacex", 60, 330, 300, 120, w(42) - 0.1, B("s05") - 0.08);
chip("1 OCT 2026 · SPACEX TRANSPORTER-18", 60, 1100, "#ffffff", w(39), B("s05") - 0.08);
(function () { const s = satEl(330, 680, 2.4); const f = el("div", "", "position:absolute;left:650px;top:470px;width:250px;height:440px;border:6px dashed #fff;border-radius:22px;opacity:0",
    `<div style="position:absolute;right:16px;top:150px;width:14px;height:90px;border-radius:7px;background:#fff"></div><div style="position:absolute;left:-6px;right:-6px;top:150px;border-top:6px dashed #fff"></div>`);
  pop(s, A("s06") + 0.05, B("s06") - 0.08, 0.5); tl.fromTo(f, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.3, ease: E }, w(46)); out(f, B("s06") - 0.08);
  chip("ABOUT THE SIZE OF A FRIDGE", 60, 1010, "#ffffff", w(46) + 0.1, B("s06") - 0.08);
  logoTile("planet", 380, 330, 320, 120, w(53) - 0.1, B("s06") - 0.08);
  chip("BUILT WITH PLANET", 60, 1100, "var(--lime)", w(54), B("s06") - 0.08); })();
logoTile("google", 60, 330, 140, 140, w(58) - 0.1, B("s07") - 0.08);
chip("INSIDE: A GOOGLE AI CHIP", 60, 1100, "var(--lime)", w(58), B("s07") - 0.08);
chip("THE KIND IN ITS DATA CENTERS", 60, 1100, "#7cc4ff", w(67), B("s07b") - 0.08);
(function () { const c = svgEl(290, 380, 500, 500, `<g stroke="#9aa3b5" stroke-width="10">${[0, 1, 2, 3, 4, 5].map((i) => `<path d="M${110 + i * 56} 40 V90 M${110 + i * 56} 410 V460 M40 ${110 + i * 56} H90 M410 ${110 + i * 56} H460"/>`).join("")}</g>
    <rect x="90" y="90" width="320" height="320" rx="28" fill="#1b2230" stroke="#9aa3b5" stroke-width="6"/><rect class="core" x="150" y="150" width="200" height="200" rx="18" fill="#2b3446"/>
    <text x="250" y="262" text-anchor="middle" font-family="Mono, monospace" font-weight="700" font-size="44" fill="#e8e9ee">TPU</text>`);
  tl.fromTo(c, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, A("s08") + 0.05);
  tl.to(c.querySelector(".core"), { attr: { fill: "#c8ff4d" }, duration: 0.3 }, w(70) + 0.1);
  tl.to(c, { filter: "drop-shadow(0 0 50px rgba(200,255,77,0.8))", duration: 0.3 }, w(70) + 0.1);
  const g = el("div", "big", "left:0;width:1080px;text-align:center;top:930px;font-size:96px;color:#fff", "GEMMA <span style='color:var(--lime)'>4</span>");
  tl.fromTo(g, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, w(75) - 0.1);
  chip("GOOGLE'S OWN AI MODEL", 60, 1100, "var(--lime)", w(71), B("s08") - 0.08); out([c, g], B("s08") - 0.08); })();

// ---------- s09 - s12: the orbit, the request, the answer ----------
(function () { const G = globe(140, 330, 800); tl.fromTo(G.d, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.35, ease: E }, A("s09"));
  spin(G, A("s09"), B("s09"), { lon: 10, lat: 35, inc: 97.5 * D2R, node: -20 * D2R, u: -40 * D2R, ground: [15.4, 78.2] },
    { lon: 30, lat: 50, u: 330 * D2R });
  const pings = [w(89), w(92)]; pings.forEach((t) => tl.fromTo(G.q(".pg"), { attr: { r: 10 }, opacity: 1 }, { attr: { r: 60 }, opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, t));
  const c = el("div", "big", "left:0;width:1080px;text-align:center;top:300px;font-size:88px;color:#fff", "<span id='lap'>0</span> MIN / LAP");
  tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.2 }, w(79) - 0.1);
  const n = { v: 0 }; tl.fromTo(n, { v: 0 }, { v: 90, duration: 1.2, ease: "power1.inOut", onUpdate() { $("#lap").textContent = Math.round(n.v); } }, w(79));
  chip("ABOUT 90 MINUTES PER LAP", 60, 1060, "var(--lime)", w(81), B("s09") - 0.08);
  chip("MESSAGES SENT AS IT FLIES OVER", 60, 1140, "#ff8a1f", w(87), B("s09") - 0.08); out([G.d, c], B("s09") - 0.08); })();
(function () { const s = satEl(540, 380, 1.2); tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.2 }, A("s10"));
  const b = bubble("Write a haiku about being in space.", 230, 900, 640, w(95), B("s10") - 0.08);
  tl.to(b, { y: -380, scale: 0.4, opacity: 0, duration: 0.6, ease: "power2.in" }, w(100) + 0.2);
  chip("FIRST REQUEST: A HAIKU", 60, 1140, "var(--lime)", w(97), B("s10") - 0.08); out(s, B("s10") - 0.08); })();
// the hidden word: the pin says SVALBARD; the voice only says "the top of the world"
const pin = (sid, t0, t1) => { const p = el("div", "", "position:absolute;left:470px;top:600px;opacity:0",
    `<div style="position:absolute;left:-30px;top:-120px;width:60px;height:60px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#ff4d4d;box-shadow:0 10px 30px rgba(0,0,0,0.5)"></div>
     <div style="position:absolute;left:-14px;top:-104px;width:28px;height:28px;border-radius:50%;background:#fff"></div>
     <div class="gsign" style="opacity:1;position:absolute;left:-150px;top:-40px;width:300px;text-align:center;background:#0b0c10;border-color:#ff4d4d">SVALBARD</div>`, $("#cam-" + sid));
  tl.fromTo(p, { opacity: 0, y: -200 }, { opacity: 1, y: 0, duration: 0.4, ease: "bounce.out" }, t0); return p; };
pin("s11", w(104), B("s11"));
chip("TOP OF THE WORLD · NORWAY", 60, 1100, "#ff8a1f", w(105), B("s11") - 0.08);
(function () { const L = [0, 1, 2].map((i) => el("div", "", `position:absolute;left:${240 + i * 40}px;top:${880 + i * 60}px;width:${[520, 600, 540][i]}px;height:18px;border-radius:9px;opacity:0;
    background:linear-gradient(90deg,#fff,#c8ff4d);box-shadow:0 0 26px rgba(200,255,77,0.9);transform-origin:0 50%`));
  L.forEach((l, i) => { tl.fromTo(l, { opacity: 1, scaleX: 0, y: -200 }, { scaleX: 1, y: 0, duration: 0.4, ease: "power2.out" }, w(110 + i) - 0.05); });
  out(L, B("s12") - 0.08);
  chip("GOOGLE'S OWN POST · 30 OCT 2026", 60, 1140, "#ffffff", w(111), B("s12") - 0.08); })();

// ---------- s13 - s20: why space ----------
bigLetters("WHY?", 300, 560, 220, "#fff", w(119), B("s13") - 0.06);
bigLetters("HUNGRY", 120, 560, 200, "var(--lime)", w(128) - 0.05, B("s14") - 0.08);
chip("AI NEEDS ELECTRICITY", 60, 1100, "#ffb547", w(126), B("s14") - 0.08);
(function () { const b = el("div", "bubble bot", "left:300px;top:460px;width:480px", "Here's your answer…");
  tl.fromTo(b, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, w(131));
  tl.to(b, { x: 700, scale: 0.4, opacity: 0, duration: 0.5, ease: "power2.in" }, w(137));
  chip("EVERY ANSWER → A DATA CENTER", 60, 1100, "#7cc4ff", w(136), B("s15") - 0.08); })();
(function () { const m = el("div", "pbar", "left:90px;top:360px;width:836px",
  `<div class="lb"><span>⚡ ELECTRICITY</span><span>24/7</span></div><div class="tr"><div class="fi" id="mt" style="background:#ffb547"></div></div>`);
  tl.fromTo(m, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, A("s16") + 0.1);
  tl.fromTo("#mt", { scaleX: 0.1 }, { scaleX: 0.95, duration: B("s16") - A("s16") - 0.3, ease: "power1.in" }, A("s16") + 0.1);
  chip("ALL EATING ELECTRICITY", 60, 1100, "#ffb547", w(146), B("s16") - 0.08); out(m, B("s16") - 0.08); })();
(function () { const b = el("div", "bars", "padding:40px 44px 4px;border-radius:26px;background:rgba(8,9,14,0.86);width:900px;left:90px", `<div class="row"><div class="lbl">Japan<span>THE WHOLE COUNTRY, TODAY</span></div><div class="trk"><div class="fill" id="bj" style="width:100%;background:#7cc4ff"></div></div></div>` +
    `<div class="row"><div class="lbl">Data centers<span>THE WORLD, 2030</span></div><div class="trk"><div class="fill" id="bd" style="width:100%;background:#ffb547"></div></div></div>`);
  tl.fromTo(b, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, w(149));
  tl.fromTo("#bj", { scaleX: 0 }, { scaleX: 0.86, duration: 0.6, ease: "power2.out" }, w(157));
  tl.fromTo("#bd", { scaleX: 0 }, { scaleX: 0.9, duration: 1.2, ease: "power2.out" }, w(150));
  chip("IEA · ENERGY AND AI (2025)", 60, 1100, "#ffffff", w(155), B("s17") - 0.08); out(b, B("s17") - 0.08); })();
bigLetters("UP ↑", 300, 560, 200, "var(--lime)", w(166) - 0.05, B("s18") - 0.06);
(function () { const c = el("div", "big", "left:0;width:1080px;text-align:center;top:330px;font-size:150px;color:#fff", "×100<br/><span style='font-size:110px;color:#ffb547'>TRILLION</span>");
  tl.fromTo(c, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power4.out" }, w(172)); out(c, B("s19") - 0.08);
  chip("THE SUN vs. ALL OUR ELECTRICITY", 60, 1060, "#ffb547", w(176), B("s19") - 0.08);
  chip("GOOGLE RESEARCH, 2025", 60, 1140, "#ffffff", w(176) + 0.2, B("s19") - 0.08); })();
(function () { const m = el("div", "pbar", "left:90px;top:360px;width:836px",
  `<div class="lb"><span>☀ SOLAR POWER</span><span id="sp">100%</span></div><div class="tr"><div class="fi" id="sf" style="background:#ffd34d"></div></div>`);
  tl.fromTo(m, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, A("s20") + 0.1);
  tl.fromTo("#sf", { scaleX: 1 }, { scaleX: 1, duration: 0.01 }, A("s20") + 0.1);
  tl.to("#sf", { scaleX: 0.02, duration: 0.5, ease: "power2.in" }, w(187));
  tl.to("#sf", { scaleX: 0.55, duration: 0.3 }, w(190)); tl.to("#sf", { scaleX: 0.25, duration: 0.2, yoyo: true, repeat: 2 }, w(191));
  const pc = { v: 100 }; tl.fromTo(pc, { v: 100 }, { v: 0, duration: 0.5, ease: "power2.in", onUpdate() { $("#sp").textContent = Math.round(pc.v) + "%"; } }, w(187));
  chip("☾ STOPS AT NIGHT", 60, 1010, "#7cc4ff", w(188), B("s20") - 0.08);
  chip("☁ CLOUDS GET IN THE WAY", 60, 1100, "#c9ccd6", w(191), B("s20") - 0.08); out(m, B("s20") - 0.08); })();

// ---------- s21 - s24: the right orbit, 8x ----------
(function () { const G = globe(140, 330, 800); tl.fromTo(G.d, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.35, ease: E }, A("s21"));
  // dawn-dusk orbit: a polar orbit that rides the terminator (sun at longitude 0 -> terminator on the +-90 meridians)
  spin(G, A("s21"), B("s21"), { lon: 40, lat: 20, sunLon: 0, inc: 90 * D2R, node: 90 * D2R, u: -60 * D2R }, { lon: 70, lat: 25, u: 200 * D2R });
  chip("THE LINE WHERE DAY MEETS NIGHT", 60, 1060, "#ffb547", w(202), B("s21") - 0.08);
  chip("☀ ALMOST NEVER IN THE DARK", 60, 1140, "var(--lime)", w(209), B("s21") - 0.08); out(G.d, B("s21") - 0.08); })();
(function () { const b = el("div", "bars", "padding:40px 44px 4px;border-radius:26px;background:rgba(8,9,14,0.86);width:900px;left:90px", `<div class="row"><div class="lbl">A panel on Earth<span>SUN + NIGHT + CLOUDS</span></div><div class="trk"><div class="fill" id="p1" style="width:100%;background:#7cc4ff"></div><div class="num" style="left:24px">1×</div></div></div>` +
    `<div class="row"><div class="lbl">The same panel in the right orbit<span>GOOGLE RESEARCH</span></div><div class="trk"><div class="fill" id="p8" style="width:100%;background:var(--lime)"></div><div class="num" id="n8" style="left:24px;color:#0b0c10">1×</div></div></div>`);
  tl.fromTo(b, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, A("s22") + 0.05);
  tl.fromTo("#p1", { scaleX: 0 }, { scaleX: 1 / 8.5, duration: 0.4, ease: "power2.out" }, A("s22") + 0.2);
  tl.fromTo("#p8", { scaleX: 0 }, { scaleX: 8 / 8.5, duration: 0.9, ease: "power2.out" }, w(219));
  const n = { v: 1 }; tl.fromTo(n, { v: 1 }, { v: 8, duration: 0.9, ease: "power2.out", onUpdate() { $("#n8").textContent = "UP TO " + Math.round(n.v) + "×"; } }, w(219));
  out(b, B("s22") - 0.08); })();
chip("FREE SUNSHINE, FOREVER?", 60, 1100, "#ffd34d", w(224), B("s23") - 0.08);
flash(w(225), 0.35, 0.6, "#fff6d0");
stamp("NOT QUITE", 230, 600, -6, "#ff4d4d", w(228), B("s24") - 0.06, 96);

// ---------- s25 - s33: the heat ----------
chip("CHIPS TURN ELECTRICITY INTO HEAT", 60, 1100, "#ff8a1f", w(231), B("s25") - 0.08);
(function () { const c = el("div", "dialog", "left:150px;top:420px;width:780px",
  `<div class="q" style="font-size:40px">⚠ Temperature</div><div style="font-size:38px;line-height:1.3;color:#1b1c22;font-weight:600">Your phone needs to cool down before you can use it.</div>`);
  tl.fromTo(c, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, w(240)); out(c, B("s26") - 0.08); })();
chip("FANS", 60, 1010, "#7cc4ff", w(250), B("s27") - 0.08);
chip("+ WATER · CARRY HEAT AWAY", 60, 1100, "#7cc4ff", w(252), B("s27") - 0.08);
(function () { const h = el("div", "big", "left:0;width:1080px;text-align:center;top:360px;font-size:80px;color:#fff", "IN SPACE?");
  tl.fromTo(h, { opacity: 0 }, { opacity: 1, duration: 0.2 }, w(257)); out(h, B("s28") - 0.08);
  [["AIR", 259, 520], ["WIND", 261, 680], ["WATER", 263, 840]].forEach(([t, k, y]) => { const b = el("div", "big", `left:0;width:1080px;text-align:center;top:${y}px;font-size:120px;color:#7cc4ff`, "NO " + t);
    tl.fromTo(b, { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.out" }, w(k) - 0.05);
    const s = el("div", "strike", `left:200px;top:${y + 60}px;width:680px`); tl.to(s, { scaleX: 1, duration: 0.2 }, w(k) + 0.25);
    out([b, s], B("s28") - 0.08); }); })();
(function () { const t = svgEl(240, 330, 600, 800, `
    <rect x="120" y="120" width="360" height="620" rx="70" fill="#c9ccd6" stroke="#fff" stroke-width="6"/>
    <rect x="160" y="160" width="280" height="540" rx="50" fill="#0b0c10"/>
    <rect class="gap" x="160" y="160" width="280" height="540" rx="50" fill="none" stroke="var(--lime)" stroke-width="8" stroke-dasharray="14 10"/>
    <rect x="196" y="196" width="208" height="468" rx="34" fill="#e8e9ee"/>
    <rect x="212" y="320" width="176" height="330" rx="24" fill="#6b3b1f"/>
    <rect x="180" y="70" width="240" height="70" rx="20" fill="#9aa3b5"/>
    <g class="stm" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.8"><path d="M260 300 q-14 -30 0 -60"/><path d="M300 300 q-14 -30 0 -60"/><path d="M340 300 q-14 -30 0 -60"/></g>`);
  tl.fromTo(t, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.5)" }, A("s29") + 0.05);
  tl.fromTo(t.querySelector(".gap"), { opacity: 0 }, { opacity: 1, duration: 0.2, repeat: 3, yoyo: true }, w(270));
  const lb = el("div", "tag", "left:600px;top:560px;font-size:28px;background:#0b0c10;border:2px solid var(--lime);color:var(--lime)", "← EMPTY GAP");
  show(lb, w(270), B("s29") - 0.08);
  chip("NO AIR IN THE GAP = HEAT STAYS IN", 60, 1140, "var(--lime)", w(275), B("s29") - 0.08); out(t, B("s29") - 0.08); })();
(function () { const p = el("div", "", "position:absolute;left:0;top:520px;width:1080px;height:200px;opacity:0;background:linear-gradient(180deg,rgba(4,5,10,0),rgba(4,5,10,0.75) 25%,rgba(4,5,10,0.75) 75%,rgba(4,5,10,0))");
  tl.fromTo(p, { opacity: 0 }, { opacity: 1, duration: 0.2 }, w(281) - 0.1); out(p, B("s30") - 0.08); })();
bigLetters("ONE GIANT THERMOS", 60, 560, 96, "#fff", w(281), B("s30") - 0.08);
(function () { const wv = svgEl(140, 340, 800, 400, [0, 1, 2, 3].map((i) => `<path d="M${120 + i * 160} 380 q-40 -60 0 -120 q40 -60 0 -120 q-40 -60 0 -120" fill="none" stroke="rgba(255,200,140,0.9)" stroke-width="8" stroke-linecap="round"/>`).join(""));
  tl.fromTo(wv, { opacity: 0, y: 40 }, { opacity: 1, y: -40, duration: 1.4, ease: "none" }, w(289)); out(wv, B("s31") - 0.08);
  chip("HEAT LEAVES AS INVISIBLE LIGHT (INFRARED)", 60, 1100, "#ff8a1f", w(290), B("s31") - 0.08); })();
chip("RADIATORS: PANELS THAT GLOW HEAT AWAY", 60, 1100, "var(--lime)", w(304), B("s32") - 0.08);
(function () { const m = el("div", "pbar", "left:90px;top:400px;width:836px",
  `<div class="lb"><span id="wr">AI WORKING</span><span>LIMIT</span></div><div class="tr" style="position:relative"><div class="fi" id="tf" style="background:#ff8a1f"></div><div style="position:absolute;right:60px;top:-10px;width:6px;height:60px;background:#ff4d4d"></div></div>`);
  tl.fromTo(m, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, A("s33") + 0.05);
  const s = satEl(540, 800, 1.6); tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.2 }, A("s33") + 0.05);
  const c = [w(314), w(318), w(319) + 0.6];
  tl.fromTo("#tf", { scaleX: 0 }, { scaleX: 0.92, duration: c[1] - c[0], ease: "power1.in" }, c[0]);
  tl.set("#wr", { textContent: "REST · COOLING DOWN" }, c[1]); tl.to("#tf", { scaleX: 0.15, duration: 0.9, ease: "power2.out" }, c[1]);
  tl.to(s, { opacity: 0.35, duration: 0.2 }, c[1]);
  chip("SHORT BURSTS, THEN REST", 60, 1100, "#ff8a1f", w(316), B("s33") - 0.08); out([m, s], B("s33") - 0.08); })();

// ---------- s34 - s37: radiation ----------
(function () { const bits = "0110100101110010011011110110100101100011".split("");
  const g = el("div", "", "position:absolute;left:120px;top:520px;width:840px;opacity:0;font-family:Mono,monospace;font-weight:700;font-size:58px;letter-spacing:0.3em;line-height:1.3;color:#7cc4ff;word-break:break-all",
    bits.map((b, i) => `<span${i === 13 ? " id='fb'" : ""}>${b}</span>`).join(""));
  tl.fromTo(g, { opacity: 0 }, { opacity: 1, duration: 0.3 }, A("s34") + 0.1);
  const ps = [0, 1, 2, 3, 4, 5].map((i) => el("div", "", `position:absolute;left:-200px;top:${380 + i * 110}px;width:160px;height:6px;border-radius:3px;opacity:0;background:linear-gradient(90deg,rgba(255,138,31,0),#ffd34d)`));
  ps.forEach((p, i) => tl.fromTo(p, { opacity: 1, x: 0 }, { x: 1500, duration: 0.7, ease: "none", repeat: 2, repeatDelay: 0.3 }, w(326) + i * 0.13));
  tl.set("#fb", { textContent: "0", color: "#ff4d4d" }, w(332) + 0.1);
  tl.fromTo("#fb", { scale: 1 }, { scale: 1.8, duration: 0.15, yoyo: true, repeat: 1 }, w(332) + 0.1);
  chip("TINY, FAST PARTICLES", 60, 1010, "#ffd34d", w(327), B("s34") - 0.08);
  chip("1 → 0", 60, 1100, "#ff4d4d", w(333), B("s34") - 0.08); out([g, ...ps], B("s34") - 0.08); })();
(function () { const s = el("div", "big", "left:0;width:1080px;text-align:center;top:520px;font-size:110px;color:#fff;text-transform:none", "The sky is <span id='ty'>b</span>lue.");
  tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.2 }, A("s35") + 0.05);
  tl.set("#ty", { textContent: "g", color: "#ff4d4d" }, w(337)); tl.fromTo("#ty", { y: -40 }, { y: 0, duration: 0.25, ease: "bounce.out" }, w(337));
  chip("ONE FLIPPED BIT = A TYPO", 60, 1100, "#ff4d4d", w(338), B("s35") - 0.08); out(s, B("s35") - 0.08); })();
(function () { const c = svgEl(140, 380, 800, 500, `<rect x="440" y="130" width="240" height="240" rx="24" fill="#1b2230" stroke="#9aa3b5" stroke-width="6"/>
    <text x="560" y="265" text-anchor="middle" font-family="Mono, monospace" font-weight="700" font-size="44" fill="#c8ff4d">TPU</text>
    <path class="bm" d="M0 250 H440" stroke="#ff4d4d" stroke-width="16" stroke-linecap="round"/>`);
  tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.25 }, A("s36") + 0.05);
  tl.fromTo(c.querySelector(".bm"), { attr: { "stroke-dasharray": "0 900" } }, { attr: { "stroke-dasharray": "900 0" }, duration: 0.5, ease: "power2.in" }, w(353));
  flash(w(354), 0.3, 0.3, "#ffd0d0");
  chip("A PARTICLE BEAM, WHILE RUNNING AI", 60, 1100, "#ff4d4d", w(354), B("s36") - 0.08); out(c, B("s36") - 0.08); })();
(function () { const c = el("div", "big", "left:0;width:1080px;text-align:center;top:420px;font-size:220px;color:#fff", "<span id='yr'>1</span>");
  const l = el("div", "big", "left:0;width:1080px;text-align:center;top:660px;font-size:70px;color:var(--lime)", "YEARS IN ORBIT ✓");
  tl.fromTo([c, l], { opacity: 0 }, { opacity: 1, duration: 0.2 }, w(360));
  const n = { v: 1 }; tl.fromTo(n, { v: 1 }, { v: 5, duration: 0.9, ease: "power2.out", onUpdate() { $("#yr").textContent = (n.v >= 4.95 ? "5+" : Math.round(n.v)); } }, w(362));
  chip("SURVIVED MORE THAN 5 YEARS' WORTH", 60, 1100, "var(--lime)", w(364), B("s37") - 0.08); out([c, l], B("s37") - 0.08); })();

// ---------- s38 - s40: the big dream ----------
chip("THE BIG DREAM: A CLUSTER (GOOGLE RESEARCH)", 60, 1130, "#ffffff", w(371), w(379) - 0.12);
chip("~100–200 M APART · LINKED BY LASER", 60, 1130, "var(--lime)", w(379), B("s38") - 0.08);
(function () { const c = svgEl(90, 380, 900, 600, `<circle class="cn" cx="780" cy="300" r="26" fill="#ffd34d" stroke="#fff" stroke-width="4"/>
    <path class="lz" d="M90 300 L780 300" stroke="#ff4d4d" stroke-width="5" stroke-dasharray="0 2000"/><g class="s1" transform="translate(90,300)">${SAT(0.7)}</g>`);
  tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.25 }, A("s39") + 0.05);
  tl.to(c.querySelector(".lz"), { attr: { "stroke-dasharray": "2000 0" }, duration: 0.5 }, w(395));
  const wob = { k: 0 }; tl.fromTo(wob, { k: 0 }, { k: 1, duration: B("s39") - w(401), ease: "none", onUpdate() {
    const a = Math.sin(wob.k * 9) * 40, b = Math.cos(wob.k * 7) * 30;
    c.querySelector(".cn").setAttribute("cy", 300 + a); c.querySelector(".s1").setAttribute("transform", `translate(90,${300 + b})`);
    c.querySelector(".lz").setAttribute("d", `M90 ${300 + b} L780 ${300 + a}`); } }, w(401));
  chip("LIKE HITTING A COIN FROM MILES AWAY", 60, 1010, "#ffd34d", w(395), B("s39") - 0.08);
  chip("…WHILE BOTH ARE MOVING", 60, 1100, "#ff4d4d", w(402), B("s39") - 0.08); out(c, B("s39") - 0.08); })();
(function () { const c = svgEl(140, 420, 800, 400, `<path class="lz" d="M200 200 H600" stroke="#c8ff4d" stroke-width="6"/><g transform="translate(200,200)">${SAT(1)}</g><g transform="translate(600,200)">${SAT(1)}</g>`);
  tl.fromTo(c, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, A("s40") + 0.05);
  chip("2027 · TWO LINKED TEST SATELLITES", 60, 1100, "var(--lime)", w(406), B("s40") - 0.08); out(c, B("s40") - 0.08); })();

// ---------- s41 - s44: the catch ----------
chip("LET'S BE HONEST", 60, 1010, "#ffffff", w(413), B("s41") - 0.08);
chip("LAUNCHES MUST GET MUCH CHEAPER", 60, 1100, "#ff8a1f", w(420), B("s41") - 0.08);
(function () { const s = svgEl(240, 360, 600, 560, `<rect x="120" y="380" width="360" height="40" rx="10" fill="#9aa3b5"/><rect x="270" y="300" width="60" height="90" fill="#9aa3b5"/>
    <path d="M200 300 h200 l-30 -120 h-140 z" fill="#3a3f4c" stroke="#c9ccd6" stroke-width="4"/><text x="300" y="262" text-anchor="middle" font-weight="900" font-size="60" fill="#fff">1 kg</text>`);
  const tg = el("div", "off", "left:640px;top:420px;font-size:60px;transform:rotate(-10deg)", "&lt; $200");
  tl.fromTo(s, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, A("s42") + 0.05); pop(tg, w(427), B("s42") - 0.08, 0.3);
  chip("GOOGLE'S MATH: UNDER $200 A KILO", 60, 1100, "#ffffff", w(428), B("s42") - 0.08); out(s, B("s42") - 0.08); })();
stamp("NO REPAIRS IN ORBIT", 120, 600, -5, "#ff4d4d", w(435), B("s43") - 0.06, 72);
(function () { const q = el("div", "quote", "left:70px;top:420px;width:940px",
  `<div class="qk">PROJECT SUNCATCHER'S LEADER, TO NPR</div><div class="qt">Space data centers <span class="qh" id="qh">won't be cheaper than on Earth</span> for years.</div><div class="qa">TRAVIS BEALS, GOOGLE · NPR, 2 OCT 2026 · PARAPHRASED</div>`);
  tl.fromTo(q, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.5)" }, w(442));
  tl.to("#qh", { backgroundSize: "100% 80%", duration: 0.7, ease: "power2.inOut" }, w(448)); out(q, B("s44") - 0.08); })();

// ---------- s45 - s47: the takeaway, the hidden word ----------
poemCard(190, 480, A("s45") + 0.1, B("s45") - 0.08, "THAT LITTLE POEM");
chip("…TELLS US SOMETHING BIG", 60, 1100, "var(--lime)", w(459), B("s45") - 0.08);
chip("⚡ EVERY AI ANSWER COSTS POWER", 60, 1100, "#ffb547", w(464), B("s46") - 0.08);
bigLetters("LEFT THE PLANET", 70, 560, 104, "#fff", w(476), B("s46b") - 0.08);
pin("s47", A("s47") + 0.3, B("s47"));
chip("COMMENT THE WORD 💬", 60, 1100, "var(--lime)", w(493), B("s47") - 0.08);

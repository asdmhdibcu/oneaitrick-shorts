/* One AI Trick · long-form engine (classic script).
 * Needs gsap + plugins loaded first. Everything is deterministic and seek-safe:
 * all motion lives on one paused GSAP timeline that HyperFrames seeks frame by frame.
 *
 * Usage in a chapter (inside <script type="module">):
 *   const tl = OAT.init({ dur, words: window.WORDS, caps: window.CAPS, chapter: 2, title: "THE IMPOSSIBLE EXAM",
 *                         globalStart: 48.6, globalTotal: 726.5 });
 *   ... choreography using OAT.W("word") times ...
 *   OAT.finish();
 */
(function () {
  "use strict";
  gsap.registerPlugin(ScrambleTextPlugin, SplitText, MotionPathPlugin, DrawSVGPlugin, Physics2DPlugin, CustomEase, TextPlugin);
  const OAT = {};
  window.OAT = OAT;
  OAT.A = "assets/3d/";
  OAT.C = { bg: "#0b0c10", ink: "#f5f5f2", muted: "#9a9ca6", lime: "#c8ff4d", blue: "#7cc4ff", amber: "#ffb547", pink: "#ff7ac6", red: "#ff6b6b" };
  CustomEase.create("snap", "M0,0 C0.14,0 0.24,1.12 0.42,1.04 0.56,0.98 0.66,1 1,1");
  CustomEase.create("whip", "M0,0 C0.6,0 0.4,1 1,1");

  /* ---------- basics ---------- */
  OAT.rnd = function (seed) { let a = seed | 0; return () => { a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  OAT.$ = (s) => document.querySelector(s);
  OAT.div = function (p, c, css, html) { const d = document.createElement("div"); if (c) d.className = c; if (css) d.style.cssText = css; if (html !== undefined) d.innerHTML = html; p.appendChild(d); return d; };
  // bottom-centre anchored 3D art (characters/props stand on a floor)
  OAT.img = function (p, name, x, yb, w, css) {
    const d = OAT.div(p, "w3", `left:${x - w / 2}px;top:${yb - w}px;width:${w}px;height:${w}px;${css || ""}`);
    const i = document.createElement("img"); i.src = OAT.A + name + ".png"; d.appendChild(i); d.i = i; return d;
  };
  // centre anchored 3D art (floating objects)
  OAT.imgc = function (p, name, cx, cy, w, css) {
    const d = OAT.div(p, "w3 c", `left:${cx - w / 2}px;top:${cy - w / 2}px;width:${w}px;height:${w}px;${css || ""}`);
    const i = document.createElement("img"); i.src = OAT.A + name + ".png"; d.appendChild(i); d.i = i; return d;
  };
  OAT.shadow = (p, x, yb, w, op) => OAT.div(p, "shadow", `left:${x - w * 0.36}px;top:${yb - w * 0.05}px;width:${w * 0.72}px;height:${w * 0.11}px;opacity:${op == null ? 1 : op}`);
  OAT.chip = function (p, text, x, y, color, css) {
    const d = OAT.div(p, "chipx", `left:${x}px;top:${y}px;color:${color || OAT.C.lime};${css || ""}`, text);
    d.setAttribute("data-layout-allow-occlusion", ""); return d;
  };
  OAT.svg = function (p, w, h, inner, css) {
    const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    s.setAttribute("width", w); s.setAttribute("height", h); s.setAttribute("viewBox", `0 0 ${w} ${h}`);
    s.style.cssText = "position:absolute;overflow:visible;" + (css || ""); s.innerHTML = inner; p.appendChild(s); return s;
  };
  OAT.text = function (p, cls, x, y, html, css) { return OAT.div(p, cls, `left:${x}px;top:${y}px;${css || ""}`, html); };

  /* ---------- init / word clock ---------- */
  OAT.init = function (o) {
    OAT.o = o; OAT.DUR = o.dur; OAT.mutes = []; OAT.WORDS = o.words || []; OAT.CAPS = o.caps || [];
    OAT.tl = gsap.timeline({ paused: true });
    const norm = (s) => s.toLowerCase().replace(/[^a-z0-9']/g, "");
    OAT._w = OAT.WORDS.map((w) => ({ n: norm(w.text), s: w.start, e: w.end }));
    OAT._norm = norm;
    return OAT.tl;
  };
  // time of the k-th occurrence (1-based) of a word: W("sacrifice") start, W("days",1,"e") end
  OAT.W = function (word, k, edge) {
    const n = OAT._norm(word); let c = 0;
    for (const w of OAT._w) { if (w.n === n && ++c === (k || 1)) return edge === "e" ? w.e : w.s; }
    console.warn("OAT.W missing", word, k); return 0;
  };
  // time of a phrase: P("broke into another") start (edge "e" = end of its last word)
  OAT.P = function (phrase, k, edge) {
    const parts = phrase.split(/\s+/).map(OAT._norm); let c = 0;
    for (let i = 0; i + parts.length <= OAT._w.length; i++) {
      let ok = true; for (let j = 0; j < parts.length; j++) if (OAT._w[i + j].n !== parts[j]) { ok = false; break; }
      if (ok && ++c === (k || 1)) return edge === "e" ? OAT._w[i + parts.length - 1].e : OAT._w[i].s;
    }
    console.warn("OAT.P missing", phrase, k); return 0;
  };
  OAT.mute = function (a, b) { OAT.mutes.push([a, b]); };

  /* ---------- motion helpers ---------- */
  const T = () => OAT.tl;
  OAT.E = "power3.out";
  OAT.popIn = (t, els, st, sc) => T().fromTo(els, { opacity: 0, scale: sc || 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)", stagger: st || 0 }, t);
  OAT.popOut = (t, els, st) => T().to(els, { opacity: 0, scale: 0.4, duration: 0.3, ease: "power2.in", stagger: st || 0 }, t);
  OAT.slideIn = (t, els, from, st, d) => T().fromTo(els, Object.assign({ opacity: 0 }, from), { opacity: 1, x: 0, y: 0, rotation: 0, duration: d || 0.55, ease: OAT.E, stagger: st || 0 }, t);
  OAT.fadeIn = (t, els, d, st) => T().fromTo(els, { opacity: 0 }, { opacity: 1, duration: d || 0.4, stagger: st || 0 }, t);
  OAT.fadeOut = (t, els, d, st) => T().to(els, { opacity: 0, duration: d || 0.35, stagger: st || 0 }, t);
  OAT.bob = function (el, t0, t1, amp, per) { const n = Math.max(1, Math.floor((t1 - t0) / per) * 2 - 1); T().fromTo(el, { y: 0 }, { y: -amp, duration: per / 2, ease: "sine.inOut", yoyo: true, repeat: n }, t0); };
  OAT.sway = function (el, t0, t1, deg, per) { const n = Math.max(1, Math.floor((t1 - t0) / per) * 2 - 1); T().fromTo(el, { rotation: -deg }, { rotation: deg, duration: per / 2, ease: "sine.inOut", yoyo: true, repeat: n }, t0); };
  OAT.shake = function (el, t, dur, amp) { const k = []; for (let i = 0; i < 8; i++) k.push(((i % 2) ? -1 : 1) * amp * (1 - i / 8)); k.push(0); T().to(el, { keyframes: { x: k }, duration: dur, ease: "none" }, t); };
  OAT.pulse = (el, t, s, d) => T().to(el, { scale: s || 1.15, duration: (d || 0.36) / 2, yoyo: true, repeat: 1, ease: "sine.inOut" }, t);
  OAT.glow = (el, t, color, d) => T().to(el, { filter: `drop-shadow(0 0 18px ${color}) drop-shadow(0 0 46px ${color})`, duration: d || 0.35 }, t);
  OAT.unglow = (el, t, d) => T().to(el, { filter: "drop-shadow(0 0 0px rgba(0,0,0,0))", duration: d || 0.35 }, t);
  OAT.dim = (el, t, d) => T().to(el, { filter: "grayscale(1) brightness(0.45)", duration: d || 0.4 }, t);
  OAT.draw = function (t, els, d, ease) {
    const list = typeof els === "string" ? document.querySelectorAll(els) : (els.length ? els : [els]);
    list.forEach((p) => T().fromTo(p, { drawSVG: "0%", opacity: 1 }, { drawSVG: "100%", duration: d || 0.8, ease: ease || "power2.inOut" }, t));
  };
  OAT.fly = (el, path, t, d, opts) => T().to(el, Object.assign({ motionPath: { path, autoRotate: false }, duration: d || 1, ease: "power2.inOut" }, opts || {}), t);
  OAT.flash = function (t, op, color) { const f = OAT.$("#flash"); if (color) T().set(f, { background: color }, t); T().set(f, { opacity: op || 0.8 }, t); T().to(f, { opacity: 0, duration: 0.35, ease: "power2.out" }, t + 0.01); };
  OAT.typeOn = function (el, text, t0, t1) { const n = text.length; for (let i = 1; i <= n; i++) T().set(el, { textContent: text.slice(0, i) }, t0 + (t1 - t0) * (i / n)); };
  OAT.scramble = function (el, text, t0, d, chars) { T().fromTo(el, { scrambleText: { text: " ", chars: chars || "01#%&*<>/\\|=+" } }, { scrambleText: { text, chars: chars || "01#%&*<>/\\|=+", revealDelay: 0.1, speed: 0.6 }, duration: d || 0.9, ease: "none" }, t0); };
  OAT.countTo = function (el, from, to, t, d, fmt) { const o = { v: from }; T().fromTo(o, { v: from }, { v: to, duration: d || 1.2, ease: "power2.out", onUpdate() { el.textContent = fmt ? fmt(o.v) : Math.round(o.v).toLocaleString("en-US"); } }, t); };
  // particle burst (Physics2D, deterministic seed)
  OAT.burst = function (p, x, y, n, color, t, seed, opt) {
    const R = OAT.rnd(seed || 7); const o = opt || {}; const out = [];
    for (let i = 0; i < n; i++) {
      const s = (o.size || 8) + R() * (o.sizeVar || 12);
      const el = OAT.div(p, "pcell", `left:${x}px;top:${y}px;width:${s}px;height:${s}px;background:${color};box-shadow:0 0 14px ${color}`);
      T().set(el, { opacity: 1, x: 0, y: 0 }, t);
      T().to(el, { physics2D: { velocity: (o.v || 520) * (0.4 + R() * 0.8), angle: (o.a0 == null ? 0 : o.a0) + R() * (o.spread || 360), gravity: o.g == null ? 420 : o.g }, opacity: 0, duration: (o.d || 1.3) * (0.7 + R() * 0.5), ease: "none" }, t + 0.01);
      out.push(el);
    }
    return out;
  };
  // split-text reveal of an element's words or chars
  OAT.splitIn = function (el, t, type, st, from) {
    const sp = new SplitText(el, { type: type || "chars,words" });
    const parts = (type || "chars").indexOf("chars") >= 0 ? sp.chars : sp.words;
    T().fromTo(parts, Object.assign({ opacity: 0, y: 40, rotationX: -70 }, from || {}), { opacity: 1, y: 0, rotationX: 0, duration: 0.5, ease: "back.out(1.8)", stagger: st || 0.025 }, t);
    return sp;
  };

  /* ---------- scene transitions (per scene camera element) ---------- */
  OAT.enter = function (cam, type, t, d) {
    d = d || 0.45;
    if (type === "whipL") T().fromTo(cam, { x: 1500, filter: "blur(22px)" }, { x: 0, filter: "blur(0px)", duration: d, ease: "power3.out" }, t);
    else if (type === "whipR") T().fromTo(cam, { x: -1500, filter: "blur(22px)" }, { x: 0, filter: "blur(0px)", duration: d, ease: "power3.out" }, t);
    else if (type === "whipU") T().fromTo(cam, { y: 900, filter: "blur(22px)" }, { y: 0, filter: "blur(0px)", duration: d, ease: "power3.out" }, t);
    else if (type === "zoom") T().fromTo(cam, { scale: 2.4, opacity: 0, filter: "blur(14px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: d + 0.1, ease: "power3.out" }, t);
    else if (type === "pull") T().fromTo(cam, { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: d + 0.1, ease: "power3.out" }, t);
    else if (type === "flip") T().fromTo(cam, { rotationY: -80, opacity: 0, transformPerspective: 1600 }, { rotationY: 0, opacity: 1, duration: d + 0.15, ease: "power3.out" }, t);
    else if (type === "iris") T().fromTo(cam, { clipPath: "circle(0px at 50% 46%)" }, { clipPath: "circle(1300px at 50% 46%)", duration: d + 0.2, ease: "power3.in" }, t);
    else if (type === "wipe") T().fromTo(cam, { clipPath: "inset(0 0 0 100%)" }, { clipPath: "inset(0 0 0 0%)", duration: d, ease: "power3.inOut" }, t);
    else T().fromTo(cam, { opacity: 0 }, { opacity: 1, duration: d }, t);
  };
  OAT.exit = function (cam, type, t, d) {
    d = d || 0.35;
    if (type === "whipL") T().to(cam, { x: -1500, filter: "blur(22px)", duration: d, ease: "power3.in" }, t);
    else if (type === "whipR") T().to(cam, { x: 1500, filter: "blur(22px)", duration: d, ease: "power3.in" }, t);
    else if (type === "whipU") T().to(cam, { y: -900, filter: "blur(22px)", duration: d, ease: "power3.in" }, t);
    else if (type === "zoom") T().to(cam, { scale: 2.6, opacity: 0, filter: "blur(14px)", duration: d, ease: "power3.in" }, t);
    else if (type === "push") T().to(cam, { scale: 0.7, opacity: 0, duration: d, ease: "power3.in" }, t);
    else if (type === "flip") T().to(cam, { rotationY: 80, opacity: 0, transformPerspective: 1600, duration: d, ease: "power3.in" }, t);
    else T().to(cam, { opacity: 0, duration: d }, t);
  };
  // glitch accent across a cut (overlay bars + jitter on a camera)
  OAT.glitch = function (t, cam, d) {
    d = d || 0.32; const g = OAT.$("#glitch"); const R = OAT.rnd(Math.round(t * 100));
    for (let i = 0; i < 6; i++) {
      const tt = t + (i / 6) * d;
      T().set(g, { opacity: 1, backgroundPosition: `0 ${Math.round(R() * 1080)}px`, x: (R() - 0.5) * 60 }, tt);
      if (cam) T().set(cam, { x: (R() - 0.5) * 40, filter: `hue-rotate(${Math.round(R() * 90)}deg) saturate(1.6)` }, tt);
    }
    T().set(g, { opacity: 0, x: 0 }, t + d); if (cam) T().set(cam, { x: 0, filter: "none" }, t + d);
  };
  // light-leak sweep (lime/pink) across the frame
  OAT.leak = function (t, color, d) { const l = OAT.$("#leak"); T().set(l, { background: `radial-gradient(ellipse 40% 90% at 50% 50%, ${color || "rgba(200,255,77,0.55)"}, rgba(0,0,0,0))` }, t); T().fromTo(l, { x: -1400, opacity: 1 }, { x: 1400, opacity: 1, duration: d || 0.7, ease: "power2.inOut" }, t); T().set(l, { opacity: 0 }, t + (d || 0.7)); };

  /* ---------- quote card (mutes duplicate captions automatically) ---------- */
  // q({ text, t0, t1, style:"lime|pink|ink|amber", size, label, mode:"type|scramble", scrim:0.7, y })
  OAT.quote = function (o) {
    const ui = OAT.$("#qlayer");
    const box = OAT.div(ui, "quote " + (o.style || "ink"), `top:${o.y || 46}%;opacity:0`);
    if (o.label) OAT.div(box, "mk", "", o.label);
    const q = OAT.div(box, "q", `font-size:${o.size || 84}px`, "");
    const tIn = o.tIn == null ? o.t0 - 0.35 : o.tIn, tOut = o.t1;
    if (o.scrim !== 0) { T().to("#scrim", { opacity: o.scrim || 0.72, duration: 0.3 }, tIn); T().to("#scrim", { opacity: 0, duration: 0.4 }, tOut); }
    T().fromTo(box, { opacity: 0, y: 16, scale: 0.97 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: OAT.E }, tIn);
    if (o.mode === "scramble") OAT.scramble(q, o.text, o.t0, o.typeD || Math.max(0.6, (o.tEnd || o.t0 + 1) - o.t0));
    else OAT.typeOn(q, o.text, o.t0, o.tEnd || o.t0 + Math.max(0.5, o.text.length * 0.045));
    T().to(box, { opacity: 0, y: -10, duration: 0.35 }, tOut);
    OAT.mute(o.muteA == null ? o.t0 - 0.05 : o.muteA, o.muteB == null ? (o.tEnd || o.t0 + 1) + 0.05 : o.muteB);
    return box;
  };
  // big statement text (title-style), also mutes captions for its span
  OAT.statement = function (o) {
    const ui = OAT.$("#qlayer");
    const el = OAT.div(ui, "stmt " + (o.cls || ""), `top:${o.y || 44}%;font-size:${o.size || 150}px;opacity:0`, o.html);
    T().set(el, { opacity: 1 }, o.t0);
    OAT.splitIn(el, o.t0, o.split || "chars", o.st || 0.02);
    T().to(el, { opacity: 0, scale: 1.04, duration: 0.35 }, o.t1);
    if (o.scrim) { T().to("#scrim", { opacity: o.scrim, duration: 0.3 }, o.t0 - 0.1); T().to("#scrim", { opacity: 0, duration: 0.4 }, o.t1); }
    if (o.mute !== false) OAT.mute(o.muteA == null ? o.t0 - 0.05 : o.muteA, o.muteB == null ? o.t1 : o.muteB);
    return el;
  };

  /* ---------- finish: UI chrome, captions (minus muted words), grain, master tick ---------- */
  OAT.finish = function (tick) {
    const o = OAT.o, t = T();
    // chapter label + handle
    const lab = OAT.$("#chlabel"); if (lab) { lab.innerHTML = `<b>${String(o.chapter).padStart(2, "0")}</b><span>${o.title || ""}</span>`; t.fromTo(lab, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.6, ease: OAT.E }, 0.25); }
    t.fromTo("#handle", { opacity: 0 }, { opacity: 0.85, duration: 0.6 }, 0.25);
    // film-wide progress line
    if (o.globalTotal) { const a = (o.globalStart || 0) / o.globalTotal, b = ((o.globalStart || 0) + o.dur) / o.globalTotal; t.fromTo("#prog", { scaleX: a }, { scaleX: b, duration: o.dur, ease: "none" }, 0); }
    // captions: drop any word that is on screen elsewhere (muted spans)
    const inMute = (s) => OAT.mutes.some(([a, b]) => s >= a && s < b);
    const root = OAT.$("#caps");
    (OAT.CAPS || []).forEach((cc) => {
      const keep = cc.w.filter((w) => !inMute(w.s));
      if (!keep.length) return;
      let t0 = Math.max(cc.t0, keep[0].s - 0.06), t1 = cc.t1;
      for (const [a] of OAT.mutes) if (a > keep[0].s && a < t1) t1 = a;
      const c = OAT.div(root, "cap");
      const sp = keep.map((w) => { const s = document.createElement("span"); s.className = "cw" + (w.emph ? " emph" : ""); s.textContent = w.d; c.appendChild(s); return { s, w }; });
      t.fromTo(c, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.12 }, t0); t.set(c, { opacity: 0 }, t1);
      sp.forEach(({ s, w }, k) => { const end = k + 1 < sp.length ? sp[k + 1].w.s : t1; t.set(s, { color: OAT.C.lime, scale: w.emph ? 1.07 : 1.03 }, w.s); t.set(s, { color: w.emph ? OAT.C.lime : "#ffffff", scale: 1 }, end); });
    });
    // grain shimmer
    { const gp = { f: 0 }, gEl = OAT.$("#grain"); t.fromTo(gp, { f: 0 }, { f: o.dur * 24, duration: o.dur, ease: "none", onUpdate() { const f = Math.floor(gp.f); gEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0); }
    // master tick LAST so every state tween has applied before 3D renders
    if (tick) { const mp = { t: 0 }; t.fromTo(mp, { t: 0 }, { t: o.dur, duration: o.dur, ease: "none", onUpdate() { tick(mp.t); } }, 0); }
    window.__timelines = window.__timelines || {}; window.__timelines["main"] = t; t.seek(0); if (tick) tick(0);
  };
})();

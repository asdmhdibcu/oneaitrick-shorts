// Short #17 "Your mom's voice, for sale": one stage (the viewer's phone), a chapter tracker, pins that stay.
// Word indices are words.json positions; screens are designed at 1000 x 2140 (the phone's own pixels).
// Draft 2 (critic1.md): the board is the default view; the camera pushes in only for the two calls, the real pages
// and the chart, always to the same framing (design row 240 at frame y 300, so content starts at y 330).

const add = (p, cls, css, html) => el("div", cls, css, html, p);
const popIn = (s, t, sc, d) => fin(s, { opacity: 0, scale: sc || 0.5 }, { opacity: 1, scale: 1, duration: d || 0.38, ease: "back.out(2)" }, t);
const fadeIn = (s, t, from, d) => fin(s, Object.assign({ opacity: 0 }, from || { y: 30 }), { opacity: 1, x: 0, y: 0, duration: d || 0.35, ease: E }, t);
const out = (s, t, d) => at(s, { opacity: 0, duration: d || 0.2 }, t);
tl.set("#phone", { scale: 0.4, transformOrigin: "0px 0px", x: 0 }, 0);
const buzz = (t) => { for (let k = 0; k < 8; k++) tl.set("#phone", { x: (k % 2 ? -1 : 1) * 5 }, t + k * 0.04); tl.set("#phone", { x: 0 }, t + 0.34); };
// hits stay inside the phone: a flash on the screen only, and a small punch of the whole stage
const sflash = (t, a, d, c) => { tl.set("#sflash", { background: c || "#fff" }, t); fin("#sflash", { opacity: a }, { opacity: 0, duration: d || 0.25, ease: "power2.out" }, t); };
const punch = (t, s) => { fin("#drift", { scale: 1 }, { scale: s || 1.06, duration: 0.1, ease: "power2.out" }, t); at("#drift", { scale: 1, duration: 0.45, ease: "power2.inOut" }, t + 0.1); };
// the only two camera states: the board, or pushed into the screen (status bar and pins out of the way)
const DY = 240;
const pushIn = (t, d, ease) => { cam(PUSH(DY), t, d || 0.5, ease); at(["#sbar", "#notch"], { opacity: 0, duration: 0.25 }, t); at("#pins", { opacity: 0, duration: 0.25 }, t); };
const pullOut = (t, d) => { cam(BOARD, t, d || 0.5); at(["#sbar", "#notch"], { opacity: 1, duration: 0.3 }, t + 0.15); at("#pins", { opacity: 1, duration: 0.3 }, t + 0.1); };
const rest = (ks, t, o) => ks.forEach((k) => at(PE[k], { opacity: o, duration: 0.3 }, t));

// ---------- icons ----------
const ICON = {
  phone: '<svg viewBox="0 0 24 24"><path fill="#fff" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>',
  bank: '<svg viewBox="0 0 64 64"><path fill="#fff" d="M32 6 6 20v6h52v-6L32 6zm-20 24v20h6V30h-6zm11 0v20h6V30h-6zm12 0v20h6V30h-6zm11 0v20h6V30h-6zM6 54v6h52v-6H6z"/></svg>',
  play: '<svg viewBox="0 0 24 24"><path fill="#0b0c10" d="M8 5v14l11-7z"/></svg>',
};
const padlock = (col, n) => `<svg viewBox="0 0 300 380" style="width:100%;height:100%;overflow:visible">
  <g class="shk"><path d="M80 170 V110 a70 70 0 0 1 140 0 V170" fill="none" stroke="${col}" stroke-width="30" stroke-linecap="round"/></g>
  <rect class="bdy" x="30" y="160" width="240" height="200" rx="34" fill="rgba(200,255,77,0.10)" stroke="${col}" stroke-width="14"/>
  ${n ? `<text x="150" y="300" text-anchor="middle" font-family="InterV" font-weight="900" font-size="130" fill="${col}">${n}</text>` : `<circle cx="150" cy="245" r="26" fill="${col}"/><rect x="138" y="250" width="24" height="60" rx="8" fill="${col}"/>`}</svg>`;

// ---------- the key: a waveform whose peaks become its teeth (drawn on canvas, seek-safe) ----------
const TEETH = [0.55, 0.9, 0.4, 0.75, 1.0, 0.5, 0.85, 0.35, 0.7, 0.95, 0.45, 0.6];
const drawKey = (g, ox, oy, sc, col, dashed, m, live) => { // m: 0 = waveform bars, 1 = key; live(i) = bar level while she talks
  g.save(); g.translate(ox, oy); g.scale(sc, sc);
  g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 10; if (dashed) g.setLineDash([22, 16]);
  const kA = Math.max(0, Math.min(1, m * 1.4 - 0.2));
  if (kA > 0) { g.globalAlpha = kA;
    g.beginPath(); g.arc(150, 0, 112, 0, Math.PI * 2); g.arc(150, 0, 44, 0, Math.PI * 2, true); dashed ? g.stroke() : g.fill("evenodd");
    g.beginPath(); g.rect(250, -34, 600, 60); dashed ? g.stroke() : g.fill(); g.globalAlpha = 1; }
  for (let i = 0; i < 24; i++) { const amp = live ? live(i) : 0.25 + 0.75 * Math.abs(Math.sin(i * 1.7 + 0.6));
    const x0 = -120 + i * 42, h0 = 80 + 240 * amp, y0 = -h0 / 2;
    let x1 = x0, h1 = 0, y1 = 26, w1 = 0;
    if (i >= 12) { const j = i - 12; x1 = 440 + j * 34; h1 = 24 + 70 * TEETH[j]; y1 = 26; w1 = 30; }
    const x = x0 + (x1 - x0) * m, h = h0 + (h1 - h0) * m, y = y0 + (y1 - y0) * m, ww = 26 + (w1 - 26) * m;
    if (ww < 1 || h < 1) continue; g.beginPath(); g.rect(x, y, ww, h); dashed ? g.stroke() : g.fill(); }
  g.restore(); };
const keyCanvas = (parent, css, wd, ht, draw) => { const c = el("canvas", "", "position:absolute;" + css, undefined, parent); c.width = wd; c.height = ht; const g = c.getContext("2d");
  PAINT.push((T) => { g.clearRect(0, 0, wd, ht); draw(g, T); }); return c; };
const wave = (parent, css, wd, ht, col, fn, n) => keyCanvas(parent, css, wd, ht, (g, T) => { const N = n || 46, bw = wd / N;
  g.fillStyle = col; for (let i = 0; i < N; i++) { const a = fn(T, i, N); if (a <= 0) continue; const h = Math.max(8, a * ht * 0.92);
    g.beginPath(); g.roundRect(i * bw + bw * 0.22, (ht - h) / 2, bw * 0.56, h, bw * 0.28); g.fill(); } });
const KEYREST = (i) => 0.25 + 0.75 * Math.abs(Math.sin(i * 1.7 + 0.6));

// ---------- a call screen (the scam call, the bank call, and the mirror at the end) ----------
const callScreen = (id, name, sub, avatar) => { const s = scr(id, "radial-gradient(ellipse 90% 60% at 50% 25%, #2d3854 0%, #10131c 62%, #07080c 100%)");
  const av = add(s, "abs", "left:360px;top:300px;width:280px;height:280px;border-radius:50%;background:#59627a;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:150px;color:#fff", avatar || "M");
  const rings = [0, 1].map(() => add(s, "abs", "left:360px;top:300px;width:280px;height:280px;border-radius:50%;border:8px solid rgba(255,255,255,0.55);opacity:0"));
  const nm = add(s, "ctr", "top:640px;font-weight:700;font-size:150px;letter-spacing:-0.02em;color:#fff", name);
  const sb = add(s, "ctr", "top:830px;font-weight:500;font-size:52px;color:#a5abba", sub);
  const tm = add(s, "ctr h", "top:830px;font-family:Mono;font-weight:500;font-size:56px;color:#d6d9e2", "00:00");
  const dec = add(s, "btnc", "left:150px;top:1760px;background:#ff3b30", ICON.phone);
  dec.querySelector("svg").style.transform = "rotate(135deg)";
  const acc = add(s, "btnc", "left:650px;top:1760px;background:#34c759", ICON.phone);
  return { s, av, rings, nm, sb, tm, dec, acc }; };
const ring = (C, t) => C.rings.forEach((r, k) => fin(r, { opacity: 0.7, scale: 1 }, { opacity: 0, scale: 1.75, duration: 1.0, ease: "power1.out" }, t + k * 0.32));
const timer = (C, t0, t1) => PAINT.push((T) => { if (T < t0 || T > t1) return; const s = Math.floor(T - t0); C.tm.textContent = "00:0" + Math.min(9, s); });
// answered: the avatar steps back, the name and the timer stack at the top of the pushed frame
const answer = (C, t) => { out([C.dec, C.acc], t + 0.05, 0.25); out(C.sb, t, 0.15); fadeIn(C.tm, t + 0.05, { y: 10 });
  at(C.av, { scale: 0.5, opacity: 0, duration: 0.4, ease: IO }, t);
  at(C.nm, { y: -340, scale: 0.8, duration: 0.5, ease: IO }, t); at(C.tm, { y: -380, duration: 0.5, ease: IO }, t + 0.05); };
const RINGS = [0.15, 1.35, 2.55, 3.75, 4.95];      // the same ring rhythm on frame one and in the mirror

// =============================================================== 1 · THE CALL
// frame one: the phone at board scale ringing MOM, the claim on a solid card over its lower half
const C1 = callScreen("call", "Mom", "mobile");
swapS(null, "call", 0, "cut");
RINGS.forEach((t) => ring(C1, t)); [0.15, 1.35, 2.55, 3.75, 5.19].forEach(buzz);
const hook = el("div", "", "", `<div class="n">1 IN 3</div><div class="s">say a fake voice called them</div>`, $("#board")); hook.id = "hook";
const hyT = logoTile("hiya", hook, "left:40px;top:26px;width:150px;height:56px;border-radius:14px");
const hp = page("p01", hook, "top:250px", 860, 140);
tl.set(hook, { opacity: 1, x: 0, y: 0, scale: 1, transformOrigin: "0px 0px" }, 0);
fin(hook.querySelector(".n"), { scale: 1.1, transformOrigin: "0% 50%" }, { scale: 1, duration: 0.5, ease: E }, 0);
hp.go(0.5, 0.6);
// the card shrinks into pin 1 and the board is left: the phone ringing, the first fact parked beside it
at(hook, { x: 40 - 70, y: 352 - 780, scale: 280 / 940, duration: 0.55, ease: "power3.inOut" }, 3.2);
out(hook, 3.72, 0.12); land(0, 3.72, true);

// on "rings": push into the call
pushIn(w(15) - 0.2, 0.5);
// the call buttons belong to the board view: pushed in they would sit half off the frame's bottom edge
out([C1.dec, C1.acc], w(15) - 0.2, 0.3);
fin(C1.nm, { color: "#ffffff" }, { color: "#c8ff4d", duration: 0.2, yoyo: true, repeat: 1 }, w(18));
// she's crying: answered, the timer runs, her voice trembles
const T_ANS = w(19);
fin(C1.acc, { scale: 1 }, { scale: 0.86, duration: 0.12, yoyo: true, repeat: 1 }, T_ANS - 0.15);
answer(C1, T_ANS); timer(C1, T_ANS, w(25));
// her voice: the same 24 bars that become the key's teeth (so the cut to the key is a match cut)
const cw1 = keyCanvas(C1.s, "left:0px;top:470px;opacity:0", 1000, 360, (g, T) => { const f = Math.floor(T * 20);
  const to = Math.max(0, Math.min(1, (T - (w(25) - 0.6)) / 0.6));
  drawKey(g, 70, 180, 0.95, "#ff7a8a", false, 0, (i) => { const n = 0.2 + 0.8 * rnd(f * 3.1 + i * 7.7) * (0.5 + 0.5 * Math.abs(Math.sin(T * 6.1 + i * 0.4)));
    return n * (1 - to) + KEYREST(i) * to; }); });
fadeIn(cw1, T_ANS + 0.1, { scaleY: 0.2 });
const bub1 = add(C1.s, "bub l h", "left:100px;top:830px", 'I need money. <b style="color:#ff6b6b">NOW.</b>');
fadeIn(bub1, w(21), { y: 40 });
const send = add(C1.s, "abs h", "left:230px;top:990px;width:540px;height:150px;border-radius:40px;background:#ff3b30;display:flex;align-items:center;justify-content:center;font-weight:850;font-size:62px;color:#fff;box-shadow:0 0 60px rgba(255,59,48,0.6)", "SEND MONEY");
popIn(send, w(24), 0.4); at(send, { scale: 1.06, duration: 0.22, yoyo: true, repeat: 3, ease: "sine.inOut" }, w(24) + 0.4);
sflash(w(24), 0.25, 0.25, "#ff3b30"); punch(w(24), 1.04);

// on "Her": back to the board; her voice is a key, the key opens a door (beside pin 1)
const SK = scr("key", "radial-gradient(ellipse 80% 55% at 50% 45%, #1b2233, #07080c 70%)");
swapS("call", "key", w(25) - 0.05, "fade");
pullOut(w(25) - 0.05, 0.55);
const door = add(SK, "abs h", "left:300px;top:340px;width:420px;height:860px;border-radius:12px;background:linear-gradient(90deg,#3a2a1f,#5a4130);border:10px solid #2a1d14;box-shadow:inset 0 0 0 4px rgba(255,255,255,0.05)", "");
const light = add(SK, "abs h", "left:300px;top:340px;width:420px;height:860px;border-radius:12px;background:radial-gradient(ellipse 80% 70% at 40% 45%, #fff2cf, #ffb547 55%, #6b3d12 100%)", "");
SK.insertBefore(light, door);
add(door, "abs", "left:300px;top:420px;width:52px;height:52px;border-radius:50%;background:#c8a04a", "");
add(door, "abs", "left:312px;top:500px;width:28px;height:62px;border-radius:14px;background:#120c08", "");
tl.set(door, { transformPerspective: 2200, transformOrigin: "0% 50%" }, 0);
// the bars sit exactly where they were on the call screen, then close up into the key
const kc = keyCanvas(SK, "left:0px;top:470px", 1000, 360, (g, T) => { const m = Math.max(0, Math.min(1, (T - (w(25) + 0.25)) / 0.75));
  drawKey(g, 70, 180, 0.95, m > 0.6 ? "#d9dde6" : "#ff7a8a", false, m); });
fadeIn(door, w(27), { scale: 0.92 }, 0.5);
// into the lock: scale 0.35 about the bow, so the tip stops at the keyhole (626, 871)
tl.set(kc, { transformOrigin: "70px 180px" }, 0);
at(kc, { x: 274, y: 222, scale: 0.35, duration: 0.6, ease: IO }, w(31) - 0.1);
at(kc, { scaleY: 0.1, duration: 0.25, ease: "power2.inOut" }, w(33));
sflash(w(33) + 0.2, 0.15, 0.2);
out(kc, w(36) - 0.15, 0.15);
fin(light, { opacity: 0 }, { opacity: 1, duration: 0.3 }, w(36) - 0.2);
at(door, { rotationY: -78, duration: 0.7, ease: "power2.inOut" }, w(37) - 0.15);

// =============================================================== 2 · THE COPY
chapter(1, w(38));
const SS = scr("scan", "radial-gradient(ellipse 80% 55% at 50% 40%, #182030, #07080c 70%)");
swapS("key", "scan", w(38) - 0.02, "slide");
add(SS, "abs", "left:70px;top:420px;width:860px;height:520px;border-radius:40px;background:rgba(124,196,255,0.06);border:4px solid rgba(124,196,255,0.35);" +
  "background-image:linear-gradient(rgba(124,196,255,0.12) 2px,transparent 2px),linear-gradient(90deg,rgba(124,196,255,0.12) 2px,transparent 2px);background-size:60px 60px", "");
keyCanvas(SS, "left:0px;top:500px", 1000, 360, (g) => drawKey(g, 70, 180, 0.95, "#d9dde6", false, 1));
const scanL = add(SS, "abs", "left:70px;top:420px;width:860px;height:12px;border-radius:6px;background:#c8ff4d;box-shadow:0 0 40px 10px rgba(200,255,77,0.6);opacity:0", "");
fin(scanL, { opacity: 1, y: 0 }, { y: 508, duration: 1.3, ease: "sine.inOut" }, w(41) - 0.2);
at(scanL, { y: 0, duration: 0.6, ease: "sine.inOut" }, w(41) + 1.12); out(scanL, w(48), 0.2);
const cpy = keyCanvas(SS, "left:0px;top:1100px;opacity:0", 1000, 360, (g) => drawKey(g, 70, 180, 0.95, "#c8ff4d", true, 1));
fadeIn(cpy, w(45), { y: -120 }, 0.5);
const cpyL = add(SS, "pill h", "left:360px;top:1480px;background:#c8ff4d;color:#0b0c10;font-size:60px;padding:22px 44px", "COPY");
popIn(cpyL, w(46) + 0.1);

// the app I use for this voice: 30 seconds can be enough
pushIn(w(49) - 0.1, 0.5);
const SE = scr("el", "#0e1016");
swapS("scan", "el", w(49) + 0.05, "page");
const elT = logoTile("elevenlabs", SE, "left:250px;top:290px;width:500px;height:150px");
logoIn(elT, w(49) + 0.2);
const pe = page("p02", SE, "top:480px", 920, 520);
fadeIn(pe.c, w(50), { y: 40 });
pe.go(w(57) - 0.1, 0.6);
const n30 = add(SE, "abs h", "left:270px;top:700px;padding:6px 34px;border-radius:30px;background:#0b0c10;border:6px solid #c8ff4d;font-weight:900;font-size:160px;letter-spacing:-0.04em;line-height:1;color:#c8ff4d;box-shadow:0 20px 60px rgba(0,0,0,0.6)", "0:30");
tl.set(n30, { rotation: -4 }, 0);
popIn(n30, w(57), 0.5);
// one voice note ... and its copy: this voice
const vn = (top, col, lab, labCol) => { const b = add(SE, "abs h", `left:70px;top:${top}px;width:860px;height:190px;border-radius:60px;background:#1d2a23;border:4px solid rgba(255,255,255,0.08)`, "");
  add(b, "abs", `left:40px;top:35px;width:120px;height:120px;border-radius:50%;background:${col};display:flex;align-items:center;justify-content:center`, ICON.play.replace("<svg ", '<svg style="width:64px;height:64px" '));
  wave(b, "left:190px;top:30px", 520, 130, col, (T, i) => 0.25 + 0.75 * Math.abs(Math.sin(i * 1.3 + 0.4)) * (0.6 + 0.4 * Math.sin(i * 0.5)), 30);
  add(b, "abs mono", "left:730px;top:68px;font-size:44px;color:#d6d9e2", "0:30");
  const L = add(SE, "abs mono h", `left:80px;top:${top - 66}px;font-size:40px;color:${labCol}`, lab); return { b, L }; };
const v1 = vn(540, "#e8e9ee", "ME", "#e8e9ee"), v2 = vn(950, "#c8ff4d", "THIS VOICE · AI COPY", "#c8ff4d");
at([elT, pe.c, n30], { y: -900, opacity: 0, duration: 0.35, ease: "power3.in" }, w(62) - 0.42);
fadeIn(v1.b, w(62), { y: 200 }, 0.45); fadeIn(v1.L, w(62) + 0.2, { x: -30 });
const eq = add(SE, "ctr h", "top:755px;font-weight:900;font-size:110px;color:#fff;line-height:1", "=");
fadeIn(v2.b, w(65), { y: 200 }, 0.45); fadeIn(v2.L, w(65) + 0.25, { x: -30 }); popIn(eq, w(66));
fin([v1.b, v2.b], { borderColor: "rgba(255,255,255,0.08)" }, { borderColor: "#c8ff4d", boxShadow: "0 0 50px rgba(200,255,77,0.5)", duration: 0.25 }, w(72));

pullOut(w(72) + 0.05, 0.5);
land(1, w(72) + 0.45);

// =============================================================== 3 · THE MARKET
chapter(2, w(73));
const SM = scr("sale", "#0d0f14");
swapS("el", "sale", w(73), "up");
// real footage: a key-cutting machine (Pexels), then the FOR SALE tag drops onto it
const v01 = $("#v01"); SM.appendChild(v01);
add(SM, "abs", "left:0px;top:0px;width:1000px;height:2140px;background:linear-gradient(180deg,rgba(7,8,12,0.55) 0%,rgba(7,8,12,0.1) 35%,rgba(7,8,12,0.1) 70%,rgba(7,8,12,0.6) 100%)", "");
const tag = add(SM, "abs h", "left:190px;top:560px;width:620px;height:250px;border-radius:30px;background:#ffb547;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:120px;color:#1b1206;letter-spacing:-0.02em;box-shadow:0 40px 80px rgba(0,0,0,0.6)", "FOR SALE");
const str = add(SM, "abs h", "left:497px;top:120px;width:6px;height:440px;background:#e8e9ee", "");
tl.set(tag, { transformOrigin: "310px -440px" }, 0); tl.set(str, { transformOrigin: "3px 0px" }, 0);
fin(tag, { opacity: 0, y: -700 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.4)" }, w(76)); fin(str, { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.35, ease: E }, w(76));
[[-12, 0.35], [8, 0.35], [-4, 0.3], [0, 0.3]].forEach(([r, d], i) => at([tag, str], { rotation: r, duration: d, ease: "sine.inOut" }, w(76) + 0.4 + i * 0.33));

// a security firm watched: trade grew over SEVEN times
pushIn(w(81) - 0.1, 0.5);
const SC = scr("cc", "#0e1016");
swapS("sale", "cc", w(81) + 0.02, "page");
const nvT = logoTile("nordvpn", SC, "left:220px;top:280px;width:560px;height:140px");
logoIn(nvT, w(81) + 0.15);
const ccChip = add(SC, "chip2", "left:40px;top:460px;font-size:30px", "NORDVPN RESEARCH · AS REPORTED");
fadeIn(ccChip, w(82) + 0.2, { x: -30 });
const pc = page("p03", SC, "top:540px", 920, 560);
fadeIn(pc.c, w(83), { y: 40 }); pc.go(w(84), 0.55);
// the chart wipes over the article: bars to scale (80 px = 1×), the value and the source on screen
const ch = add(SC, "abs h", "left:0px;top:230px;width:1000px;height:930px;background:#0e1016", "");
add(ch, "abs mono", "left:110px;top:64px;font-size:34px;color:#c9ccd6", "VOICE-CLONING TRADE");
add(ch, "abs mono", "left:110px;top:118px;font-size:26px;color:#a3a8b6", "NORDVPN · AS REPORTED");
add(ch, "abs", "left:110px;top:800px;width:780px;height:6px;background:rgba(255,255,255,0.3)", "");
add(ch, "abs", "left:180px;top:720px;width:220px;height:80px;border-radius:16px 16px 0 0;background:#5b6478", "");
const bB = add(ch, "abs", "left:600px;top:208px;width:220px;height:592px;border-radius:16px 16px 0 0;background:#c8ff4d;box-shadow:0 0 50px rgba(200,255,77,0.35)", "");
tl.set(bB, { transformOrigin: "50% 100%" }, 0);
add(ch, "abs mono", "left:150px;top:830px;width:280px;text-align:center;font-size:30px;color:#c9ccd6", "JAN–JUL 2024");
add(ch, "abs mono", "left:570px;top:830px;width:280px;text-align:center;font-size:30px;color:#c9ccd6", "JAN–JUL 2026");
add(ch, "abs", "left:180px;top:630px;width:220px;text-align:center;font-weight:900;font-size:70px;color:#c9ccd6", "1×");
const n74 = add(ch, "abs", "left:560px;top:60px;width:300px;text-align:center;font-weight:900;font-size:120px;color:#c8ff4d;letter-spacing:-0.04em", "1.0×");
fin(ch, { opacity: 1, x: 1000 }, { x: 0, duration: 0.4, ease: "power3.inOut" }, w(88) - 0.2);
fin(bB, { scaleY: 1 / 7.4 }, { scaleY: 1, duration: 1.4, ease: "power2.inOut" }, w(89));
PAINT.push((T) => { const a = w(89), b = a + 1.4; const p = Math.max(0, Math.min(1, (T - a) / (b - a))); const e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
  n74.textContent = (1 + 6.4 * e).toFixed(1) + "×"; });
fin(n74, { scale: 1 }, { scale: 1.15, duration: 0.15, yoyo: true, repeat: 1 }, w(92));

pullOut(w(96) + 0.1, 0.5);
land(2, w(96) + 0.45);

// stolen accounts on real cloning apps: from about ten dollars
const SA = scr("acc", "radial-gradient(ellipse 80% 55% at 50% 40%, #1b1f2c, #07080c 70%)");
swapS("cc", "acc", w(97) - 0.05, "slide");
const lock = add(SA, "abs", "left:390px;top:200px;width:220px;height:280px", padlock("#c8ff4d"));
const card = add(SA, "abs", "left:100px;top:520px;width:800px;height:620px;border-radius:40px;background:#f3f1ea;color:#1b1c22",
  `<div style="position:absolute;left:50px;top:44px;font-weight:850;font-size:56px">Voice app</div>
   <div class="mono" style="position:absolute;left:50px;top:150px;font-size:30px;color:#6b6e78">EMAIL</div><div style="position:absolute;left:50px;top:196px;width:700px;height:90px;border-radius:20px;background:#e2dfd6;font-size:60px;padding:6px 26px;letter-spacing:6px">●●●●●●●●</div>
   <div class="mono" style="position:absolute;left:50px;top:320px;font-size:30px;color:#6b6e78">PASSWORD</div><div style="position:absolute;left:50px;top:366px;width:700px;height:90px;border-radius:20px;background:#e2dfd6;font-size:60px;padding:6px 26px;letter-spacing:6px">●●●●●●●●●●</div>
   <div style="position:absolute;left:50px;top:500px;width:700px;height:90px;border-radius:45px;background:#1b1c22;color:#fff;font-weight:800;font-size:44px;display:flex;align-items:center;justify-content:center">Log in</div>`);
fadeIn(card, w(97) + 0.1, { y: 50 });
const shk = lock.querySelector(".shk"); tl.set(shk, { transformOrigin: "220px 170px" }, 0);
at(shk, { rotation: 35, y: -40, duration: 0.3, ease: "back.out(2)" }, w(97) + 0.15);
at(lock.querySelectorAll("path,rect"), { attr: { stroke: "#ff4d4d", fill: "rgba(255,77,77,0.12)" }, duration: 0.2 }, w(97) + 0.15);
at(lock.querySelectorAll("circle"), { attr: { fill: "#ff4d4d" }, duration: 0.2 }, w(97) + 0.15);
const stl = add(SA, "pill h", "left:600px;top:470px;background:#ff3b30;color:#fff;font-size:52px", "STOLEN"); tl.set(stl, { rotation: -6 }, 0);
popIn(stl, w(98));
const ptag = add(SA, "abs h", "left:520px;top:1060px;width:400px;height:230px;border-radius:30px;background:#ffb547;color:#1b1206;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:150px;letter-spacing:-0.04em;box-shadow:0 30px 60px rgba(0,0,0,0.5)", "$0");
tl.set(ptag, { rotation: -8 }, 0);
fin(ptag, { opacity: 0, y: -300, rotation: -30 }, { opacity: 1, y: 0, rotation: -8, duration: 0.45, ease: "back.out(1.6)" }, w(103));
PAINT.push((T) => { const a = w(103) + 0.1, b = w(105) + 0.25; const p = Math.max(0, Math.min(1, (T - a) / (b - a))); ptag.textContent = "$" + Math.round(10 * p) + (p >= 1 ? "+" : ""); });
const adv = add(SA, "ctr mono h", "top:1340px;font-size:70px;color:#e8e9ee", "ADVERTISED $10–150");
fadeIn(adv, w(105) + 0.2);
land(3, w(106) + 0.2);

// =============================================================== 4 · THE BANK (chapter fires on "BANK", not before)
const ST = scr("top", "radial-gradient(ellipse 80% 55% at 50% 40%, #1b1f2c, #07080c 70%)");
swapS("acc", "top", w(107) + 0.05, "cut"); sflash(w(108), 0.3, 0.22); punch(w(108), 1.05);
const mini = add(ST, "abs", "left:150px;top:620px;width:700px;height:420px;border-radius:50px;background:#1e2230;border:3px solid rgba(255,255,255,0.1)",
  `<div style="position:absolute;left:60px;top:90px;width:240px;height:240px;border-radius:50%;background:#59627a;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:130px;color:#fff">M</div>
   <div style="position:absolute;left:340px;top:120px;font-weight:700;font-size:110px;color:#fff">Mom</div>
   <div style="position:absolute;left:345px;top:250px;font-weight:500;font-size:44px;color:#a5abba">incoming call</div>`);
fadeIn(mini, w(107) + 0.1, { scale: 0.9 });
const badge = (parent, css) => add(parent, "abs h", css + ";border-radius:50%;background:#ffb547;color:#1b1206;display:flex;align-items:center;justify-content:center;font-weight:900;letter-spacing:-0.04em;box-shadow:0 0 50px rgba(255,181,71,0.5)", "#1?");
const one = badge(ST, "left:690px;top:520px;width:220px;height:220px;font-size:90px");
popIn(one, w(109), 0.3);
// "isn't Mom": the Mom card dims and gets struck through; the badge waits for its real owner
at(mini, { opacity: 0.45, duration: 0.3 }, w(115));
const xx = add(ST, "abs h", "left:150px;top:600px;width:700px;text-align:center;font-weight:900;font-size:440px;line-height:1;color:#ff4d4d", "✗");
popIn(xx, w(116) - 0.05, 1.6, 0.3);

// it's your BANK: crash zoom into the bank's call; the #1 badge moves onto its avatar (match cut)
pushIn(w(117) - 0.02, 0.22, "power4.out"); punch(w(117), 1.06); sflash(w(117), 0.3, 0.2);
chapter(3, w(119));
const C2 = callScreen("bank", "YOUR BANK", "calling…", ICON.bank.replace("<svg ", '<svg style="width:150px;height:150px" '));
tl.set(C2.av, { background: "#2a6df4" }, 0);
tl.set([C2.dec, C2.acc], { opacity: 0 }, 0);   // only ever seen pushed in
swapS("top", "bank", w(117), "cut");
[w(117), w(119) + 0.2].forEach((t) => ring(C2, t)); buzz(w(117) + 0.05);
const one2 = badge(C2.s, "left:560px;top:240px;width:170px;height:170px;font-size:72px"); one2.textContent = "#1";
popIn(one2, w(119), 0.4);
const T_B = w(120);
answer(C2, T_B); out(one2, T_B, 0.2);
// no timer on the bank's line: FAKE takes its place under the name
tl.set(C2.tm, { display: "none" }, 0);
const fake = add(C2.s, "pill h", "left:405px;top:440px;background:#ff3b30;color:#fff;font-size:44px", "FAKE");
popIn(fake, w(121), 0.4);
const auto = add(C2.s, "ctr mono h", "top:530px;font-size:40px;color:#7cc4ff", "AUTOMATED LINE");
fadeIn(auto, T_B + 0.15, { y: 10 });
const rw = wave(C2.s, "left:70px;top:590px;opacity:0", 860, 200, "#7cc4ff", (T, i) => { if (T < T_B + 0.2 || T > w(129) + 0.5) return 0.05; const f = Math.floor(T * 12);
  return 0.2 + 0.8 * (rnd(f * 5.3 + Math.floor(i / 3) * 3.1) > 0.4 ? 1 : 0.3); }, 40);
fadeIn(rw, T_B + 0.15, { scaleY: 0.3 });
const menu = add(C2.s, "abs h", "left:70px;top:830px;width:860px;padding:36px 50px;border-radius:40px;background:#161a24;border:3px solid rgba(124,196,255,0.4);font-weight:700;font-size:56px;line-height:1.2;color:#fff",
  `Enter the code we just texted you.<div style="margin-top:22px;font-size:64px;letter-spacing:22px;color:#7cc4ff">● ● ● ● ● ●</div>`);
fadeIn(menu, w(126), { y: 40 });
const sms = add(C2.s, "abs h", "left:40px;top:280px;width:920px;height:190px;border-radius:44px;background:rgba(245,245,242,0.97);box-shadow:0 30px 60px rgba(0,0,0,0.5);color:#1b1c22",
  `<div class="mono" style="position:absolute;left:40px;top:30px;font-size:30px;color:#6b6e78">MESSAGES · NOW</div><div style="position:absolute;left:40px;top:80px;font-weight:800;font-size:66px">Your code is 482 913</div>`);
fin(sms, { opacity: 1, y: -320 }, { y: 0, duration: 0.4, ease: "back.out(1.4)" }, w(129) - 0.12);

// the code is your second lock (the FTC's own picture), read it out and they're in
const SF = scr("ftc", "#0e1016");
swapS("bank", "ftc", w(130) - 0.2, "page");
const ftcC = add(SF, "chip2", "left:40px;top:280px;font-size:30px", "FTC · AMERICA'S CONSUMER AGENCY");
fadeIn(ftcC, w(130), { x: -30 });
const pf = page("p04a", SF, "top:360px", 920, 400);
fadeIn(pf.c, w(130) + 0.05, { y: 40 }); pf.go(w(131), 0.55);
const bolt = add(SF, "abs h", "left:560px;top:600px;width:360px;height:360px",
  `<svg viewBox="0 0 360 360" style="width:100%;height:100%;overflow:visible"><circle class="pl" cx="180" cy="180" r="150" fill="#1b1f2a" stroke="#c8ff4d" stroke-width="14"/>
   <rect class="bo" x="250" y="155" width="150" height="50" rx="10" fill="#c8ff4d"/><g class="tt"><rect x="160" y="80" width="40" height="200" rx="20" fill="#e8e9ee"/></g></svg>`);
fadeIn(bolt, w(132), { scale: 0.7 });
const codeC = add(SF, "pill h", "left:70px;top:730px;background:#c8ff4d;color:#0b0c10;font-size:56px", "482 913");
fadeIn(codeC, w(133), { x: -40 });
at(codeC, { x: 520, y: 20, scale: 0.3, opacity: 0, duration: 0.5, ease: "power2.in" }, w(136));
const tt = bolt.querySelector(".tt"); tl.set(tt, { transformOrigin: "180px 180px" }, 0);
at(tt, { rotation: 90, duration: 0.3, ease: "back.out(2)" }, w(136) + 0.5);
at(bolt.querySelector(".bo"), { attr: { x: 180, fill: "#ff4d4d" }, duration: 0.3, ease: "power2.in" }, w(136) + 0.55);
at(bolt.querySelector(".pl"), { attr: { stroke: "#ff4d4d" }, duration: 0.2 }, w(136) + 0.55);
const unl = add(SF, "pill h", "left:120px;top:880px;background:#ff3b30;color:#fff;font-size:50px", "UNLOCKED");
popIn(unl, w(140)); sflash(w(140), 0.25, 0.25, "#ff3b30");

pullOut(w(141) + 0.1, 0.5);
land(4, w(141) + 0.45);

// the catch: these numbers (pins 1, 3, 4 step forward), who sells them, and what they count
const SQ = scr("count", "radial-gradient(ellipse 80% 55% at 50% 40%, #1f1a10, #07080c 70%)");
swapS("ftc", "count", w(142) - 0.05, "up");
sflash(w(143), 0.25, 0.3, "#ffb547");
add(SQ, "ctr", "top:330px;font-weight:900;font-size:110px;letter-spacing:-0.03em;color:#ffb547", "THE CATCH");
const sub2 = add(SQ, "ctr h", "top:480px;font-weight:800;font-size:64px;color:#fff", "Who's counting?");
fadeIn(sub2, w(144));
[0, 2, 3].forEach((k) => { at(PE[k], { opacity: 1, borderColor: "#ffb547", duration: 0.3 }, w(144)); });
rest([1], w(144), 0.35);
[0, 2, 3].forEach((k, i) => { const s = PE[k].querySelector(".stp"); fin(s, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, w(150) + i * 0.18); });
const who = add(SQ, "ctr h", "top:620px;font-weight:800;font-size:64px;color:#ffb547", "Companies that sell protection");
fadeIn(who, w(150), { y: 20 });
[[w(154), "Sales posts", "✓", "#c8ff4d"], [w(156), "Survey answers", "✓", "#c8ff4d"], [w(157), "Stolen money", "✗", "#ff4d4d"]].forEach(([t, txt, m, c], i) => {
  const r = add(SQ, "abs h", `left:80px;top:${780 + i * 190}px;width:840px;height:160px;border-radius:30px;background:#161922;border:3px solid ${c}55`,
    `<div style="position:absolute;left:40px;top:38px;font-weight:800;font-size:70px;color:#fff">${txt}</div><div style="position:absolute;right:40px;top:22px;font-weight:900;font-size:100px;color:${c}">${m}</div>`);
  fadeIn(r, t, { x: 60 });
  if (m === "✗") { const s = add(r, "abs", "left:30px;top:76px;width:560px;height:12px;border-radius:6px;background:#ff4d4d;transform-origin:0 50%", ""); tl.set(s, { scaleX: 0 }, 0);
    at(s, { scaleX: 1, duration: 0.35, ease: IO }, w(158)); } });
[0, 2, 3].forEach((k) => at(PE[k], { borderColor: "rgba(255,255,255,0.12)", duration: 0.3 }, w(160)));
rest([0, 1, 2, 3, 4], w(160), PIN_REST);

// =============================================================== 5 · THE LOCKS
chapter(4, w(160));
const SL = scr("locks", "radial-gradient(ellipse 80% 55% at 50% 40%, #182030, #07080c 70%)");
swapS("count", "locks", w(160) - 0.02, "slide");
const L1 = add(SL, "abs h", "left:110px;top:520px;width:330px;height:420px", padlock("#c8ff4d", "1"));
const L2 = add(SL, "abs h", "left:560px;top:520px;width:330px;height:420px", padlock("#c8ff4d", "2"));
popIn(L1, w(160) + 0.15, 0.4); popIn(L2, w(162), 0.4);
const ck = keyCanvas(SL, "left:0px;top:1300px;opacity:0", 1000, 360, (g) => drawKey(g, 70, 180, 0.95, "#c8ff4d", true, 1));
tl.set(ck, { transformOrigin: "500px 180px" }, 0);
fadeIn(ck, w(164) - 0.2, { y: 80 });
at(ck, { x: -230, y: -480, scale: 0.55, rotation: -90, duration: 0.55, ease: "power2.inOut" }, w(164) + 0.05);
at(ck, { x: -150, y: -260, rotation: -70, duration: 0.35, ease: "back.out(2)" }, w(167) - 0.15);
const nx = add(SL, "abs h", "left:150px;top:980px;width:260px;text-align:center;font-weight:900;font-size:200px;line-height:1;color:#ff4d4d", "✗");
popIn(nx, w(167) - 0.1, 1.6, 0.25);
for (let k = 0; k < 6; k++) tl.set(L1, { x: (k % 2 ? -1 : 1) * 14 * (1 - k / 6) }, w(167) - 0.1 + k * 0.04); tl.set(L1, { x: 0 }, w(167) + 0.15);

// lock 1: a family safe word (the FBI's own advice)
pushIn(w(168) - 0.1, 0.5);
const SB = scr("fbi", "#0e1016");
swapS("locks", "fbi", w(168) + 0.02, "page");
const fbiC = add(SB, "chip2", "left:40px;top:280px;font-size:30px", "FBI ALERT · DEC 2024");
fadeIn(fbiC, w(168) + 0.15, { x: -30 });
const pb = page("p05", SB, "top:360px", 920, 460);
fadeIn(pb.c, w(169), { y: 40 }); pb.go(w(170), 0.6);
const say = add(SB, "abs h", "left:70px;top:600px;width:860px;height:260px;border-radius:40px;background:#161922;border:4px solid #c8ff4d",
  `<div class="mono" style="position:absolute;left:44px;top:36px;font-size:34px;color:#c9ccd6">SAY IT IN PERSON · e.g.</div><div style="position:absolute;left:40px;top:90px;font-weight:900;font-size:130px;letter-spacing:-0.03em;color:#c8ff4d">MANGO</div>`);
fadeIn(say, w(173), { y: 40 });
pullOut(w(176) + 0.3, 0.45);
land(5, w(176) + 0.6);

// lock 2: the code never leaves your phone
const SY = scr("stay", "radial-gradient(ellipse 80% 55% at 50% 40%, #182030, #07080c 70%)");
swapS("fbi", "stay", w(177) - 0.05, "slide");
const L2b = add(SY, "abs", "left:385px;top:420px;width:230px;height:300px", padlock("#c8ff4d", "2"));
const msg = add(SY, "abs", "left:200px;top:820px;width:600px;height:220px;border-radius:50px;background:#2c2f38;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:96px;color:#fff;letter-spacing:4px", "482 913");
fadeIn(msg, w(177) + 0.1, { y: 40 });
const edge = add(SY, "abs h", "left:966px;top:200px;width:34px;height:1740px;border-radius:17px;background:#c8ff4d;box-shadow:0 0 60px 20px rgba(200,255,77,0.6)", "");
at(msg, { x: 330, duration: 0.35, ease: "power2.in" }, w(180) - 0.05);
fin(edge, { opacity: 0 }, { opacity: 1, duration: 0.08, yoyo: true, repeat: 1 }, w(180) + 0.3);
at(msg, { x: 0, duration: 0.6, ease: "elastic.out(1, 0.5)" }, w(180) + 0.32);
const shk2 = L2b.querySelector(".shk"); tl.set(shk2, { transformOrigin: "220px 170px" }, 0);
fin(shk2, { y: -60 }, { y: 0, duration: 0.25, ease: "back.out(2)" }, w(182));

// a real bank won't ask: hang up, call a number you know
pushIn(w(184) - 0.25, 0.45);
const SK2 = scr("ask", "#0e1016");
swapS("stay", "ask", w(184) - 0.2, "page");
const ftc2 = add(SK2, "chip2", "left:40px;top:280px;font-size:30px", "FTC · AMERICA'S CONSUMER AGENCY");
fadeIn(ftc2, w(184), { x: -30 });
const pa = page("p04b", SK2, "top:360px", 920, 290);
fadeIn(pa.c, w(184) + 0.05, { y: 40 }); pa.go(w(185), 0.5);
const nev = add(SK2, "stampx h", "left:110px;top:610px;font-size:56px;padding:6px 22px;border-width:10px", "REAL BANKS NEVER ASK");
tl.set(nev, { rotation: -5, transformOrigin: "50% 50%" }, 0);
fin(nev, { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, w(187)); punch(w(187) + 0.18, 1.03);
const hang = add(SK2, "btnc h", "left:390px;top:760px;width:220px;height:220px;background:#ff3b30", ICON.phone);
hang.querySelector("svg").style.transform = "rotate(135deg)";
popIn(hang, w(189) - 0.3, 0.5);
fin(hang, { scale: 1 }, { scale: 0.84, duration: 0.1, yoyo: true, repeat: 1 }, w(189));
const dial = add(SK2, "abs h", "left:70px;top:740px;width:860px;height:260px;border-radius:40px;background:#13271a;border:4px solid #34c759",
  `<div style="position:absolute;left:44px;top:50px;width:160px;height:160px;border-radius:50%;background:#34c759;display:flex;align-items:center;justify-content:center">${ICON.phone.replace("<svg ", '<svg style="width:80px;height:80px" ')}</div>
   <div style="position:absolute;left:240px;top:50px;font-weight:800;font-size:66px;color:#fff">Calling your bank</div><div class="mono" style="position:absolute;left:244px;top:150px;font-size:32px;color:#9ee6b0">THE NUMBER ON YOUR CARD</div>`);
out(hang, w(192) - 0.1, 0.15); fadeIn(dial, w(192), { y: 40 });
// on "number": back to the board, pin 7 parks before the mirror begins
pullOut(w(194) - 0.05, 0.5);
land(6, w(194) + 0.15);

// the mirror: the same phone, the same ring, the same place as frame one
const C3 = callScreen("call2", "Mom", "mobile");
swapS("ask", "call2", w(197), "fade");
const TM0 = w(197) - 0.15;
RINGS.slice(0, 2).forEach((t) => ring(C3, TM0 + t)); [TM0 + 0.15, TM0 + 1.35].forEach(buzz);
const T_M = w(201) + 0.15;
answer(C3, T_M); timer(C3, T_M, w(213));
pushIn(T_M + 0.05, 0.5);
const q = add(C3.s, "bub r h", "right:80px;top:640px;font-size:80px", "What's our word?");
fadeIn(q, w(202), { y: 40 });
const a = add(C3.s, "bub l h", "left:80px;top:840px;font-size:110px;font-weight:900;letter-spacing:-0.02em", 'MANGO <span style="color:#34c759">✓</span>');
fadeIn(a, w(206), { y: 40 });

// recap on "I never said": back to the board, the phone at rest, the attack then the locks light up
const SR = scr("lock", "radial-gradient(ellipse 80% 60% at 50% 30%, #1d2638, #07080c 72%)");
add(SR, "ctr", "top:330px;font-weight:300;font-size:250px;letter-spacing:-0.04em;color:#fff", "9:41");
add(SR, "ctr", "top:600px;font-weight:500;font-size:56px;color:#c9ccd6", "Wednesday, 11 November");
swapS("call2", "lock", w(213), "fade");
pullOut(w(213), 0.6);
const lightUp = (ks, t) => ks.forEach((k) => { const p = PE[k];
  at(p, { opacity: 1, duration: 0.3 }, t); at(p.querySelector(".bg"), { color: "#c8ff4d", duration: 0.3 }, t);
  fin(p.querySelector(".glow"), { opacity: 0 }, { opacity: 1, duration: 0.3 }, t); });
lightUp([0, 1, 2, 3], w(215)); [0, 1, 2].forEach((k) => fin(CHE[k], { scale: 1 }, { scale: 1.08, duration: 0.18, yoyo: true, repeat: 1 }, w(215)));
lightUp([4, 5, 6], w(218)); [3, 4].forEach((k) => fin(CHE[k], { scale: 1 }, { scale: 1.08, duration: 0.18, yoyo: true, repeat: 1 }, w(218)));
const hid = el("div", "pin q", "left:760px;top:1006px", `<div class="glow"></div><div class="bg" style="font-size:56px;color:#c8ff4d">THE WORD?</div><div class="lb">seen, never said · comment it</div>`, $("#pins"));
popIn(hid, w(220), 0.6);

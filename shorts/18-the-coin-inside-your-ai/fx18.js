// Short #18 "The coin inside your AI": one stage (a balance scale on the grid board, the AI as the lime thinking orb
// above its beam), a chapter tracker, pins that stay. No phone (the creator's note, 12 Nov).
// Word indices are words.json positions. Everything on the stage is painted from the time alone (seek-safe).

const add = (p, cls, css, html) => el("div", cls, css, html, p);
const popIn = (s, t, sc, d) => fin(s, { opacity: 0, scale: sc || 0.5 }, { opacity: 1, scale: 1, duration: d || 0.35, ease: "back.out(2)" }, t);
const fadeIn = (s, t, from, d) => fin(s, Object.assign({ opacity: 0 }, from || { y: 30 }), { opacity: 1, x: 0, y: 0, duration: d || 0.35, ease: E }, t);
const out = (s, t, d) => at(s, { opacity: 0, duration: d || 0.2 }, t);
const punch = (t, s) => { fin("#drift", { scale: 1 }, { scale: s || 1.05, duration: 0.1, ease: "power2.out" }, t); at("#drift", { scale: 1, duration: 0.45, ease: "power2.inOut" }, t + 0.1); };
const OVER = $("#over");
const pushIn = (t, d, ease) => { cam(PUSH, t, d || 0.5, ease); at("#pins", { opacity: 0, duration: 0.25 }, t); };
const pullOut = (t, d) => { cam(BOARD, t, d || 0.5); at("#pins", { opacity: 1, duration: 0.25 }, t + 0.3); };
const LIME = "200,255,77", AMBER = "255,181,71", BLUE = "124,196,255";

// ---------- time helpers: keyframes evaluated from T (no state, so any frame can be seeked) ----------
const EZ = { io: (u) => (u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2), out: (u) => 1 - Math.pow(1 - u, 3), in: (u) => u * u * u,
  back: (u) => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2); }, lin: (u) => u };
const kf = (T, pts) => { if (T <= pts[0][0]) return pts[0][1];
  for (let i = 1; i < pts.length; i++) { const [t1, v1, e] = pts[i], [t0, v0] = pts[i - 1];
    if (T <= t1) { const u = Math.max(0, Math.min(1, (T - t0) / (t1 - t0 || 1e-6))); return v0 + (v1 - v0) * EZ[e || "io"](u); } }
  return pts[pts.length - 1][1]; };
const lerp = (a, b, u) => a + (b - a) * u;
const clamp01 = (u) => Math.max(0, Math.min(1, u));
const on = (T, a, b) => T >= a && T < b;

// ---------- the orb (my drawing, in the style of the thinking-orbs library, as in #16) ----------
const SPH = (n) => { const p = [], g = Math.PI * (3 - Math.sqrt(5)); for (let i = 0; i < n; i++) { const y = 1 - (i / (n - 1)) * 2, r = Math.sqrt(1 - y * y), th = g * i;
  p.push([Math.cos(th) * r, y, Math.sin(th) * r, i]); } return p; };
const ORBP = SPH(240);
const orb = (c, X, Y, Rr, t, o) => { o = o || {};
  const col = o.col || LIME, al = o.a === undefined ? 1 : o.a, sp = o.speed === undefined ? 0.7 : o.speed;
  const ay = t * sp, ax = 0.35 + 0.12 * Math.sin(t * 0.6);
  const ca = Math.cos(ay), sa = Math.sin(ay), cb = Math.cos(ax), sb = Math.sin(ax);
  const g = c.createRadialGradient(X, Y, 0, X, Y, Rr * 1.8); g.addColorStop(0, `rgba(${col},${(0.26 + 0.25 * (o.glow || 0)) * al})`); g.addColorStop(1, `rgba(${col},0)`);
  c.fillStyle = g; c.fillRect(X - Rr * 1.8, Y - Rr * 1.8, Rr * 3.6, Rr * 3.6);
  for (const [px, py, pz, i] of ORBP) {
    const r = 1 + (0.07 + 0.08 * (o.glow || 0)) * Math.sin(t * 3.2 + i * 0.7);
    const x1 = px * ca + pz * sa, z1 = -px * sa + pz * ca;
    const y2 = py * cb - z1 * sb, z2 = py * sb + z1 * cb, d = (z2 + 1) / 2;
    const a = (0.12 + 0.88 * d) * al, s = (0.9 + 2.3 * d) * Rr / 120;
    c.fillStyle = `rgba(${col},${a})`; c.beginPath(); c.arc(X + x1 * Rr * r, Y + y2 * Rr * r, Math.max(0.6, s), 0, 6.2832); c.fill(); } };

// ---------- a coin: sx is its spin (cos of the turn), face = text on the front ----------
const coin = (g, x, y, r, col, sx, face, a) => { if (r <= 0.5 || a <= 0) return;
  g.save(); g.globalAlpha = a; g.translate(x, y); g.scale(Math.max(0.04, Math.abs(sx)), 1);
  const front = sx >= 0;
  const gr = g.createLinearGradient(-r, -r, r, r);
  if (col === "gold") { gr.addColorStop(0, front ? "#ffe08a" : "#e9b44c"); gr.addColorStop(0.5, front ? "#ffb547" : "#c98a2b"); gr.addColorStop(1, "#b97a1f"); }
  else { gr.addColorStop(0, "#e6ff9a"); gr.addColorStop(0.6, "#c8ff4d"); gr.addColorStop(1, "#8fbf2a"); }
  g.fillStyle = gr; g.beginPath(); g.arc(0, 0, r, 0, 6.2832); g.fill();
  g.lineWidth = Math.max(1, r * 0.08); g.strokeStyle = "rgba(60,36,6,0.55)"; g.beginPath(); g.arc(0, 0, r * 0.82, 0, 6.2832); g.stroke();
  if (front && face) { g.fillStyle = "rgba(70,40,6,0.85)"; g.font = `900 ${Math.round(r * 0.42)}px InterV`; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(face, 0, r * 0.03); }
  if (!front) { g.fillStyle = "rgba(70,40,6,0.6)"; g.beginPath(); for (let k = 0; k < 10; k++) { const an = -Math.PI / 2 + k * Math.PI / 5, rr = k % 2 ? r * 0.2 : r * 0.46;
    g.lineTo(Math.cos(an) * rr, Math.sin(an) * rr); } g.closePath(); g.fill(); }
  g.restore(); };

// ---------- the stage geometry (board pixels) ----------
const O = [540, 395], ORB_R = 62;          // the AI
const P = [540, 545], HL = 200, STR = 200;  // pivot, half beam, string
const BASE_Y = 1100;
const panAt = (a, side) => { const r = a * Math.PI / 180, ex = P[0] + side * HL * Math.cos(r), ey = P[1] + side * HL * Math.sin(r); return { ex, ey, x: ex, y: ey + STR }; };

// beam angle in degrees (positive = pan B, the right pan, goes down)
const ANG = [[0, 0], [w(36), 0], [w(36) + 0.6, 12, "back"], [20.7, 12], [21.0, 0], [w(60), 0], [w(60) + 0.4, -6, "back"], [w(65), -6], [w(65) + 0.5, 12, "back"],
  [w(67), 12], [w(67) + 0.45, 14, "back"], [31.9, 14], [32.3, 12], [w(103), 12], [w(103) + 0.16, 19, "out"], [w(109), 19], [w(109) + 0.55, 10],
  [w(129), 10], [w(132) + 0.05, 0, "back"], [52.3, 0]];
// the scale's structure dims while a card or the chat holds the eye; the orb keeps its own level
const SA = [[0, 1], [w(11), 1], [w(11) + 0.35, 0.1], [9.5, 0.1], [9.9, 1], [18.4, 1], [18.7, 0.12], [20.6, 0.12], [20.9, 1], [w(73), 1], [w(73) + 0.25, 0.16],
  [31.8, 0.16], [32.1, 1], [w(93) - 0.15, 1], [w(93) + 0.1, 0.12], [35.6, 0.12], [35.9, 1], [w(111), 1], [w(111) + 0.3, 0.3], [44.6, 0.3], [44.9, 1],
  [w(137), 1], [w(137) + 0.35, 0.35], [52.2, 0.35], [52.3, 1]];
const OA = [[0, 1], [18.55, 1], [18.75, 0.2], [20.6, 0.2], [20.9, 1], [w(93) - 0.1, 1], [w(93) + 0.1, 0.2], [35.6, 0.2], [35.9, 1], [w(137), 1], [w(137) + 0.35, 0.5],
  [52.2, 0.5], [52.3, 1]];
// how hard the orb glows: when it speaks, drops a coin or thinks about the question
const GLOW = [[0, 0], [4.7, 0], [4.9, 1], [6.6, 1], [6.9, 0], [w(35) - 0.2, 0], [w(35), 1], [w(36) + 0.3, 0], [22.8, 0], [23.0, 1], [23.5, 0], [w(125), 0],
  [w(125) + 0.15, 1.4], [44.9, 1.4], [45.3, 0.2], [52.2, 0]];

// a dropped item: falls from above its rest spot, lands at t0 with a small bounce
const drop = (T, t0, h) => { if (T < t0 - 0.28) return null; if (T < t0) return -(h || 170) * Math.pow((t0 - T) / 0.28, 2);
  const u = T - t0; return u < 0.22 ? -16 * Math.sin(Math.PI * u / 0.22) : 0; };
// a coin that leaves the orb's underside and falls into a pan, landing at t1
const fall = (T, t0, t1, pan, dx) => { const u = clamp01((T - t0) / (t1 - t0)), e = u * u;
  return [lerp(O[0], pan.x + dx, e), lerp(O[1] + ORB_R + 10, pan.y - 30, e)]; };

const block = (g, x, y, col, txt, a) => { g.save(); g.globalAlpha = a; g.fillStyle = col; g.beginPath(); g.roundRect(x - 33, y - 66, 66, 66, 12); g.fill();
  g.fillStyle = "#0b0c10"; g.font = "900 40px InterV"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(txt, x, y - 32); g.restore(); };
const token = (g, x, y, a) => { g.save(); g.globalAlpha = a; g.fillStyle = "#f5f5f2"; g.beginPath(); g.roundRect(x - 66, y - 52, 132, 52, 14); g.fill();
  g.beginPath(); g.moveTo(x - 12, y - 1); g.lineTo(x + 12, y - 1); g.lineTo(x, y + 14); g.closePath(); g.fill();
  g.fillStyle = "#0b0c10"; g.font = "700 22px Mono"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("MY PICK", x, y - 25); g.restore(); };

// ---------- the stage canvas ----------
const SCX = 1.5;
const stg = $("#stage").getContext("2d");
PAINT.push((T) => { const g = stg; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, 1620, 1950); g.setTransform(SCX, 0, 0, SCX, 0, 0);
  const a = kf(T, ANG), sa = kf(T, SA), oa = kf(T, OA);
  const A = panAt(a, -1), B = panAt(a, 1);
  g.globalAlpha = sa; g.lineCap = "round";
  // base and post
  g.fillStyle = "#171b25"; g.strokeStyle = "rgba(207,214,228,0.9)"; g.lineWidth = 4;
  g.beginPath(); g.moveTo(470, BASE_Y); g.lineTo(610, BASE_Y); g.lineTo(650, BASE_Y + 44); g.lineTo(430, BASE_Y + 44); g.closePath(); g.fill(); g.stroke();
  const pg = g.createLinearGradient(530, 0, 550, 0); pg.addColorStop(0, "#9aa3b5"); pg.addColorStop(0.5, "#e7ebf3"); pg.addColorStop(1, "#8a93a6");
  g.fillStyle = pg; g.fillRect(531, P[1], 18, BASE_Y - P[1]);
  // strings and pans
  [A, B].forEach((p) => { g.strokeStyle = "rgba(207,214,228,0.75)"; g.lineWidth = 3;
    g.beginPath(); g.moveTo(p.ex, p.ey); g.lineTo(p.x - 86, p.y); g.moveTo(p.ex, p.ey); g.lineTo(p.x + 86, p.y); g.stroke(); });
  // pan contents (drawn before the dish front, so they sit in the bowl)
  const it = (fn) => { g.save(); fn(); g.restore(); };
  const inT = (t0, t1) => on(T, t0 - 0.3, t1);
  if (inT(w(29), 52.3)) { const d = drop(T, w(29)); if (d !== null) block(g, A.x - 34, A.y + 6 + d, "#c8ff4d", "A", sa); }
  if (inT(w(30), 52.3)) { const d = drop(T, w(30)); if (d !== null) block(g, B.x + 34, B.y + 6 + d, "#7cc4ff", "B", sa); }
  // MY PICK: into pan A on "ALREADY", across to B on "switched", gone under the report
  if (on(T, w(60) - 0.3, 30.9)) { const tw0 = w(67), tw1 = w(67) + 0.32;
    let x, y; if (T < tw0) { const d = drop(T, w(60)); x = A.x; y = A.y - 88 + (d || 0); }
    else { const u = EZ.io(clamp01((T - tw0) / (tw1 - tw0))); x = lerp(A.x, B.x, u); y = lerp(A.y - 88, B.y - 88, u) - 110 * Math.sin(Math.PI * u); }
    token(g, x, y, sa); }
  // the AI's coin (amber): into B on "drops", lifted on the reset, back on "disagreed", swollen on "HEAVY"
  const amb = (() => { if (on(T, w(35), 20.7)) { const [x, y] = T < w(36) ? fall(T, w(35), w(36), B, -34) : [B.x - 34, B.y - 30]; return [x, y, 1]; }
    if (on(T, 20.7, 21.0)) { const u = (T - 20.7) / 0.3; return [B.x - 34, B.y - 30 - 160 * u, 1 - u]; }
    if (on(T, w(65) - 0.3, 52.3)) { const [x, y] = T < w(65) ? fall(T, w(65) - 0.3, w(65), B, -34) : [B.x - 34, B.y - 30]; return [x, y, 1]; }
    return null; })();
  if (amb) { const sc = kf(T, [[w(103) - 0.05, 1], [w(103) + 0.18, 2, "back"], [w(109), 2], [w(109) + 0.45, 1]]);
    coin(g, amb[0], amb[1] - 30 * (sc - 1), 30 * sc, "gold", 1, "", amb[2] * Math.max(sa, 0.12)); }
  // the second coin (lime), for the other side
  if (on(T, w(129) - 0.3, 52.3)) { const [x, y] = T < w(129) ? fall(T, w(129) - 0.3, w(129), A, 40) : [A.x + 40, A.y - 30]; coin(g, x, y, 30, "lime", 1, "", sa); }
  // dishes
  [A, B].forEach((p) => { const dg = g.createLinearGradient(p.x - 95, 0, p.x + 95, 0); dg.addColorStop(0, "#8a93a6"); dg.addColorStop(0.5, "#e7ebf3"); dg.addColorStop(1, "#8a93a6");
    g.fillStyle = dg; g.beginPath(); g.moveTo(p.x - 96, p.y); g.quadraticCurveTo(p.x, p.y + 46, p.x + 96, p.y); g.lineTo(p.x + 88, p.y + 4); g.quadraticCurveTo(p.x, p.y + 36, p.x - 88, p.y + 4); g.closePath(); g.fill();
    g.strokeStyle = "rgba(255,255,255,0.6)"; g.lineWidth = 2; g.beginPath(); g.moveTo(p.x - 96, p.y); g.lineTo(p.x + 96, p.y); g.stroke(); });
  // beam, with a glint when it is named ("Picture a scale")
  it(() => { g.translate(P[0], P[1]); g.rotate(a * Math.PI / 180);
    const bg = g.createLinearGradient(0, -9, 0, 9); bg.addColorStop(0, "#f2f4f8"); bg.addColorStop(1, "#8a93a6");
    g.fillStyle = bg; g.beginPath(); g.roundRect(-HL - 10, -8, 2 * HL + 20, 16, 8); g.fill();
    const gu = clamp01((T - w(26)) / 0.9); if (gu > 0 && gu < 1) { const gx = lerp(-HL - 60, HL + 60, gu);
      const gl = g.createLinearGradient(gx - 60, 0, gx + 60, 0); gl.addColorStop(0, "rgba(200,255,77,0)"); gl.addColorStop(0.5, "rgba(200,255,77,0.95)"); gl.addColorStop(1, "rgba(200,255,77,0)");
      g.fillStyle = gl; g.beginPath(); g.roundRect(-HL - 10, -8, 2 * HL + 20, 16, 8); g.fill(); }
    g.fillStyle = "#e7ebf3"; [-HL, HL].forEach((x) => { g.beginPath(); g.arc(x, 0, 9, 0, 6.2832); g.fill(); });
    // the pointer above the pivot tilts with the beam
    g.strokeStyle = "#e7ebf3"; g.lineWidth = 6; g.beginPath(); g.moveTo(0, 0); g.lineTo(0, -62); g.stroke(); });
  g.fillStyle = "#c8ff4d"; g.beginPath(); g.arc(P[0], P[1], 14, 0, 6.2832); g.fill();
  g.fillStyle = "#0b0c10"; g.beginPath(); g.arc(P[0], P[1], 5, 0, 6.2832); g.fill();
  // the AI
  g.globalAlpha = 1; orb(g, O[0], O[1], ORB_R, T, { a: oa, glow: kf(T, GLOW), speed: 0.8 });
});

// ---------- the TAILS coin (on top of everything on the board) ----------
const ctop = $("#coinTop").getContext("2d");
const SPIN = 9;                       // turns per second x 2 pi
const PH0 = -SPIN * w(7);             // its phase on frame one; the mirror at the end runs into the same phase
// the choice card's rows and the letter each flick lands on (B, A, B, B)
const CELLX = { A: 300, B: 372 };
const CARD = [300, 520], ROWY = [618, 690, 762, 834], LX = { A: CARD[0] + 2 + CELLX.A + 28, B: CARD[0] + 2 + CELLX.B + 28 }, PICK = ["B", "A", "B", "B"], FLICK = [w(22), w(23), w(24), w(25)];
PAINT.push((T) => { const g = ctop; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, 1620, 1950); g.setTransform(SCX, 0, 0, SCX, 0, 0);
  let x = 540, y = 650, r = 80, sx = 1, a = 1, sc = 1;
  if (T < w(7)) { sx = Math.cos(PH0 + SPIN * T); y = 650 + 6 * Math.sin(T * 5); }
  else if (T < w(11)) { sc = kf(T, [[w(7), 1.14], [w(7) + 0.28, 1, "out"]]); }
  else if (T < w(18)) { const u = EZ.io(clamp01((T - w(11)) / 0.5)); x = lerp(540, 744, u); y = lerp(650, 410, u); r = lerp(80, 34, u); }
  else if (T < 9.45) { // the secret flicks: the coin hops over the four choices
    const pts = [[w(18), 744, 410]].concat(FLICK.map((t, i) => [t, LX[PICK[i]], ROWY[i]]));
    let k = 0; while (k + 1 < pts.length && T >= pts[k + 1][0]) k++;
    if (k + 1 < pts.length) { const [t0, x0, y0] = pts[k], [t1, x1, y1] = pts[k + 1], hop = Math.min(0.24, t1 - t0), u = clamp01((T - (t1 - hop)) / hop);
      x = lerp(x0, x1, EZ.io(u)); y = lerp(y0, y1, EZ.io(u)) - 40 * Math.sin(Math.PI * u); }
    else { x = pts[k][1]; y = pts[k][2]; }
    r = 30; const lastFlick = FLICK.filter((t) => t <= T).pop(); if (lastFlick !== undefined) sx = Math.cos(2 * Math.PI * clamp01((T - lastFlick) / 0.2));
    else { sx = Math.cos(2 * Math.PI * clamp01((T - w(19)) / 0.4)); sc = kf(T, [[w(19), 1], [w(19) + 0.14, 1.45, "out"], [w(19) + 0.5, 1]]); } }
  else if (T < 9.95) { const u = EZ.in(clamp01((T - 9.45) / 0.5)); x = lerp(LX.B, O[0], u); y = lerp(ROWY[3], O[1], u); r = lerp(30, 4, u); a = 1 - u; }
  else if (T < w(137) + 0.25) { a = 0; }
  else if (T < 52.3) { a = clamp01((T - w(137) - 0.25) / 0.35); r = 90; sc = kf(T, [[w(137) + 0.25, 0.6], [w(137) + 0.6, 1, "back"]]); }
  else { sx = Math.cos(PH0 + SPIN * (T - DUR)); y = 650 + 6 * Math.sin((T - DUR) * 5); }
  coin(g, x, y, r * sc, "gold", sx, "TAILS", a);
});

// =============================================================== 1 · COIN
// frame one: the scale, the orb, the coin spinning; the claim on a solid card over the lower stage, its 50 rolling
const hook = el("div", "", "", `<svg width="0" height="0" style="position:absolute"><filter id="vblur" x="-30%" y="-10%" width="160%" height="120%"><feGaussianBlur id="vbs" stdDeviation="0 0"/></filter></svg><div class="k">ANTHROPIC STUDY · 27 OCT 2026</div><div class="l1">A COIN STEERED</div>
  <div class="l2"><span class="odo"><span class="dg"><span class="col"></span></span><span class="dg"><span class="col"></span></span></span><span>EXPERTS</span></div>`, $("#board"));
hook.id = "hook";
const hkLogo = logoTile("amark", hook, "left:48px;top:30px;width:84px;height:52px;border-radius:12px");
const DG = [...hook.querySelectorAll(".dg .col")];
DG.forEach((c) => { for (let k = 0; k < 30; k++) { const s = document.createElement("span"); s.textContent = k % 10; c.appendChild(s); } });
// the odometer: frame one rolls into 50 by 0.8 s; the last frame rolls at the same speed into frame one's start
const VBS = hook.querySelector("#vbs");
const odo = (T) => { const tgt = [5, 0]; let p, v;
  DG.forEach((c, i) => { if (T < 4) { const u = clamp01(T / 0.8); p = tgt[i] - 2.5 + 12.5 * (1 - Math.pow(1 - u, 3)); v = 46 * Math.pow(1 - u, 2); }
    else { const s = DUR - T, d = 0.49; if (s >= d) { p = tgt[i] + 10; v = 0; } else { const q = 1 - s / d; p = tgt[i] - 2.5 - 7.5 * (1 - q * q * q); v = 46 * q * q; } }
    const idx = ((p % 10) + 10) % 10 + 10; c.style.transform = `translateY(${-idx * 168}px)`; c.style.filter = v > 0.6 ? "url(#vblur)" : "none"; });
  VBS.setAttribute("stdDeviation", `0 ${Math.min(16, v * 0.35).toFixed(2)}`); };
PAINT.push((T) => { if (T < 4 || T > w(159) - 0.1) odo(T); });
gsap.set(hook, { opacity: 1, x: 0, y: 0, scale: 1, transformOrigin: "0px 0px" });
// on "knew": the card shrinks into pin 1 and the stage is left
at(hook, { x: L - 70, y: ROWS[0] - 770, scale: 210 / 940, duration: 0.5, ease: "power3.inOut" }, w(10) - 0.3);
out(hook, w(10) + 0.2, 0.1); land(0, w(10) + 0.2, true);

// "Each had an AI helper, like yours": push in on the orb; one plain chat exchange, held until the card comes in
pushIn(w(11) - 0.05, 0.5);
const aiChip = add(OVER, "chip2", "left:206px;top:446px", "AI HELPER");
fadeIn(aiChip, w(11) + 0.2, { x: -20 });
const q1 = add(OVER, "abs h", "left:420px;top:500px;padding:20px 26px;border-radius:30px;border-bottom-right-radius:10px;background:#2a6df4;color:#fff;font-weight:650;font-size:32px;white-space:nowrap",
  "A or B: which is better?");
const a1 = add(OVER, "abs h", "left:200px;top:628px;display:flex;align-items:center;gap:16px",
  `<div style="width:56px;height:56px;border-radius:50%;background:radial-gradient(circle,#c8ff4d 0 30%,rgba(200,255,77,0.25) 31% 100%)"></div><div style="padding:22px 30px;border-radius:34px;border-bottom-left-radius:10px;background:#2c2f38;color:#fff;font-weight:650;font-size:32px;white-space:nowrap">I'd pick <b style="color:#c8ff4d">B</b>.</div>`);
fin(q1, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.3, ease: E }, w(11) + 0.48);
fin(a1, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.3, ease: E }, w(15));

// "And a coin secretly picked its favorite answers": the coin flips on "coin"; a 0.2 s punch on "secretly" brings the
// card of four choices; the coin hops over them, and each cell it lands on turns amber (B, A, B, B)
punch(w(21), 1.06);
at([q1, a1, aiChip], { opacity: 0, duration: 0.25 }, w(21) - 0.15);
const cardC = add(OVER, "abs h", `left:${CARD[0]}px;top:${CARD[1]}px;width:480px;height:370px;border-radius:24px;background:#12151d;border:2px solid rgba(255,181,71,0.5);box-shadow:0 30px 70px rgba(0,0,0,0.6)`,
  `<div class="mono" style="position:absolute;left:26px;top:22px;font-size:21px;color:#ffb547">COIN FLIP → THE AI'S PICK</div>` +
  [1, 2, 3, 4].map((n, i) => `<div class="mono" style="position:absolute;left:28px;top:${70 + i * 72 + 12}px;font-size:25px;color:#e8e9ee">CHOICE ${n}</div>` +
    `<div class="cell c${i}A" style="position:absolute;left:${CELLX.A}px;top:${70 + i * 72}px;width:56px;height:52px;border-radius:12px;background:rgba(200,255,77,0.15);color:#c8ff4d;font-weight:900;font-size:30px;display:flex;align-items:center;justify-content:center">A</div>` +
    `<div class="cell c${i}B" style="position:absolute;left:${CELLX.B}px;top:${70 + i * 72}px;width:56px;height:52px;border-radius:12px;background:rgba(124,196,255,0.15);color:#7cc4ff;font-weight:900;font-size:30px;display:flex;align-items:center;justify-content:center">B</div>`).join(""));
fadeIn(cardC, w(21) - 0.05, { scale: 0.9 });
const dash = add(OVER, "abs h", "left:0;top:0;width:1080px;height:1300px",
  `<svg width="1080" height="1300" style="position:absolute;left:0;top:0;overflow:visible"><path d="M744 448 L744 520" stroke="#ffb547" stroke-width="4" stroke-dasharray="10 9" fill="none"/></svg>`);
fadeIn(dash, w(21), { y: 0 });
const rings = PICK.map((p, i) => add(cardC, "abs h", `left:${CELLX[p] - 6}px;top:${70 + i * 72 - 6}px;width:68px;height:64px;box-sizing:border-box;border-radius:16px;border:4px solid #ffb547;box-shadow:0 0 18px rgba(255,181,71,0.55);transform-origin:50% 50%`, ""));
rings.forEach((r, i) => popIn(r, FLICK[i] + 0.08, 1.5, 0.22));
PICK.forEach((p, i) => fin(cardC.querySelector(".c" + i + p), { backgroundColor: p === "A" ? "rgba(200,255,77,0.15)" : "rgba(124,196,255,0.15)", color: p === "A" ? "#c8ff4d" : "#7cc4ff" },
  { backgroundColor: "#ffb547", color: "#1b1206", duration: 0.15 }, FLICK[i] + 0.08));
at([cardC, dash], { opacity: 0, duration: 0.3 }, 9.5);

// =============================================================== 2 · SCALE
chapter(1, w(26));
pullOut(w(26) - 0.1, 0.55);
const eq = add(OVER, "abs h", "left:500px;top:690px;width:80px;text-align:center;font-weight:900;font-size:76px;line-height:1;color:#c8ff4d", "=");
popIn(eq, w(32)); out(eq, w(35) - 0.1, 0.25);

// =============================================================== 3 · FOLLOW
chapter(2, w(42));
// 60/40 split: the scale shrinks into the top; the four choices as bars below, against chance
fin("#stagewrap", { scale: 1 }, { scale: 0.62, duration: 0.45, ease: IO }, w(42) - 0.05);
at("#stagewrap", { scale: 1, duration: 0.35, ease: IO }, 18.2);
const panel = add(OVER, "glass h", "left:255px;top:880px;width:570px;height:330px", "");
const n86 = add(panel, "abs", "left:24px;top:18px;font-weight:900;font-size:100px;letter-spacing:-0.05em;line-height:1;color:#c8ff4d", "0%");
add(panel, "abs mono", "left:292px;top:34px;width:260px;font-size:22px;line-height:1.3;color:#e8e9ee", "WENT WITH<br>THE COIN");
const VAL = [92, 82, 81, 90], NAMES = ["CHOICE 1", "CHOICE 2", "CHOICE 3", "CHOICE 4"], BX = [30, 140, 250, 360], BW = 76, BASE = 290, BH = 1.4;
add(panel, "abs", `left:22px;top:${BASE}px;width:440px;height:3px;background:rgba(255,255,255,0.35)`, "");
const bars = VAL.map((v, i) => { const b = add(panel, "abs", `left:${BX[i]}px;top:${BASE - v * BH}px;width:${BW}px;height:${v * BH}px;border-radius:10px 10px 0 0;background:#c8ff4d;transform-origin:50% 100%`, "");
  add(panel, "abs mono", `left:${BX[i] - 20}px;top:${BASE + 8}px;width:${BW + 40}px;text-align:center;font-size:15px;color:#a3a8b6`, NAMES[i]);
  const lb = add(panel, "abs mono h", `left:${BX[i]}px;top:${BASE - v * BH - 30}px;width:${BW}px;text-align:center;font-size:22px;color:#e8e9ee`, v + "%");
  return { b, lb }; });
add(panel, "abs", `left:22px;top:${BASE - 50 * BH}px;width:440px;height:0;border-top:3px dashed #ffb547`, "");
add(panel, "abs mono", `left:470px;top:${BASE - 50 * BH - 13}px;font-size:17px;color:#ffb547`, "CHANCE<br>50%");
fadeIn(panel, w(42) + 0.2, { y: 60 });
gsap.set(n86, { opacity: 0 }); fin(n86, { opacity: 0 }, { opacity: 1, duration: 0.1 }, w(49) - 0.05);
bars.forEach(({ b, lb }, i) => { const t = 15.1 + i * 0.2; fin(b, { scaleY: 0 }, { scaleY: 1, duration: 0.4, ease: E }, t); fadeIn(lb, t + 0.3, { y: 10 }, 0.2); });
// 86% rolls in like an odometer on "EIGHTY-SIX" and settles in under 0.8 s
PAINT.push((T) => { const a0 = w(49), u = clamp01((T - a0) / 0.75); n86.textContent = Math.round(86 * (1 - Math.pow(1 - u, 3))) + "%"; });
fin(n86, { scale: 1 }, { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "0% 50%" }, w(49) + 0.7);
out(panel, 18.2, 0.25);

// "By chance? About half.": proof card 1 from Anthropic's own post
pushIn(18.45, 0.45);
const g1 = add(OVER, "glass h", "left:210px;top:430px;width:650px;height:330px", "");
gsap.set(g1, { transformPerspective: 2400, transformOrigin: "0% 50%" });
const lg1 = logoTile("anthropic", g1, "left:20px;top:20px;width:280px;height:70px");
const pc1 = page("p01a", g1, "left:20px;top:108px", 610, 400, true);
fin(g1, { opacity: 0, rotationY: -70 }, { opacity: 1, rotationY: 0, duration: 0.42, ease: "power2.out" }, 18.5);
logoIn(lg1, 18.6);
fin(g1, { scale: 1 }, { scale: 1.04, duration: 2.1, ease: "none" }, 18.6);
pc1.mark([w(55), w(55) + 0.35, w(57)], 0.35);
at(g1, { opacity: 0, y: -60, duration: 0.3, ease: "power2.in" }, 20.5);
pullOut(20.6, 0.5);
land(1, 20.8);

// "Some had ALREADY decided" / "When the AI disagreed... they switched": the counter under the beam
const c60w = add(OVER, "abs h", "left:400px;top:880px;width:280px;height:150px;border-radius:24px;background:rgba(10,12,18,0.94);border:3px solid #c8ff4d;" +
  "display:flex;flex-direction:column;align-items:center;justify-content:center", "");
const c60 = add(c60w, "", "font-weight:900;font-size:72px;letter-spacing:-0.04em;line-height:1;color:#c8ff4d", "0%");
add(c60w, "", "margin-top:8px;font-weight:750;font-size:27px;color:#f5f5f2", "switched sides");
popIn(c60w, w(68) - 0.05, 0.6);
PAINT.push((T) => { const u = clamp01((T - w(68)) / 0.8); c60.textContent = Math.round(60 * (1 - Math.pow(1 - u, 3))) + "%"; });
out(c60w, w(72) + 0.25, 0.25);
land(2, w(72) + 0.3);

// "Here's the weird part": record scratch, the expert's report slides up over the scale
punch(w(73), 1.05);
const rep = add(OVER, "abs h", "left:255px;top:480px;width:570px;height:440px;border-radius:20px;background:#f6f4ee;color:#1b1c22;box-shadow:0 40px 90px rgba(0,0,0,0.6);overflow:hidden", "");
add(rep, "abs mono", "left:34px;top:28px;font-size:22px;color:#6b6e78", "FINAL REPORT");
add(rep, "abs", "left:34px;top:62px;width:502px;height:3px;background:#e2dfd6", "");
const LINES = ["Choice 1: B fits best.", "Choice 2: B is safer.", "Choice 3: B covers more."];
const rl = LINES.map((s, i) => { const r = add(rep, "abs", `left:34px;top:${88 + i * 60}px;padding:5px 12px;border-radius:8px;font-weight:700;font-size:32px;white-space:nowrap`, s); return r; });
[0, 1, 2].forEach((i) => add(rep, "abs", `left:46px;top:${284 + i * 24}px;width:${[460, 410, 260][i]}px;height:12px;border-radius:6px;background:#e2dfd6`, ""));
add(rep, "abs mono", "left:34px;top:374px;font-size:22px;color:#6b6e78", "CREDIT:");
const slots = [...Array(7)].map((_, i) => add(rep, "abs", `left:${150 + i * 56}px;top:364px;width:44px;height:44px;border-radius:50%;border:3px dashed #b9b6ad;` +
  "display:flex;align-items:center;justify-content:center;font-weight:900;font-size:18px;color:#0b0c10", ""));
fin(rep, { opacity: 0, y: 500 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, w(73) + 0.05);
// threads from the orb down to the lines the expert repeated
const thr = add(OVER, "abs", "left:0;top:0;width:1080px;height:1300px;pointer-events:none",
  `<svg width="1080" height="1300" style="position:absolute;left:0;top:0;overflow:visible">${rl.map((_, i) =>
    `<path class="th" d="M${525 + i * 10} 455 C 400 466, ${266 + i * 6} 462, ${266 + i * 6} 520 L ${266 + i * 6} ${578 + i * 60} Q ${266 + i * 6} ${592 + i * 60} 286 ${592 + i * 60}" stroke="#c8ff4d" stroke-width="4" fill="none" stroke-linecap="round" stroke-dasharray="600" stroke-dashoffset="600"/>`).join("")}</svg>`);
const ths = [...thr.querySelectorAll(".th")];
[w(78) + 0.05, 28.9, 29.4].forEach((t, i) => { fin(ths[i], { attr: { "stroke-dashoffset": 600 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.35, ease: IO }, t);
  fin(rl[i], { backgroundColor: "rgba(200,255,77,0)" }, { backgroundColor: "rgba(200,255,77,0.85)", duration: 0.25 }, t + 0.25); });
// "only about one in seven gave it credit"
fin(slots, { borderColor: "#b9b6ad" }, { borderColor: "#8f8c84", duration: 0.2, stagger: 0.03 }, w(82));
fin(slots[0], { backgroundColor: "rgba(200,255,77,0)", borderStyle: "dashed" }, { backgroundColor: "#c8ff4d", borderColor: "#0b0c10", borderStyle: "solid", duration: 0.2 }, w(85));
tl.set(slots[0], { innerHTML: "AI" }, w(85));
fin(slots.slice(1), { opacity: 1 }, { opacity: 0.45, duration: 0.25, stagger: 0.04 }, w(87));
fin(rep, { scale: 1 }, { scale: 1.035, duration: 2.6, ease: "none" }, w(78) + 0.6);
at([rep, thr], { y: 520, opacity: 0, duration: 0.4, ease: "power3.in" }, 31.75);
land(3, 31.95); land(4, 32.35);

// =============================================================== 4 · CATCH
chapter(3, w(91));
fin("#amberedge", { opacity: 0 }, { opacity: 1, duration: 0.3 }, w(91)); at("#amberedge", { opacity: 0, duration: 0.5 }, 40.2);
punch(w(92), 1.05);
// "Anthropic tested its OWN AI": proof card 2, the line that the agents ran Claude
pushIn(w(93) - 0.1, 0.45);
const g2 = add(OVER, "glass h", "left:210px;top:430px;width:650px;height:372px", "");
gsap.set(g2, { transformPerspective: 2400, transformOrigin: "0% 50%" });
const lg2 = logoTile("anthropic", g2, "left:20px;top:20px;width:280px;height:70px");
const own = add(g2, "abs h mono", "left:314px;top:33px;padding:9px 14px;border-radius:12px;border:2px solid #ffb547;color:#ffb547;font-size:20px;font-weight:700;white-space:nowrap", "CLAUDE = THEIR OWN AI");
popIn(own, w(96) - 0.15, 0.6);
const pc2 = page("p01b", g2, "left:20px;top:108px", 610, 400, true);
fin(g2, { opacity: 0, rotationY: -70 }, { opacity: 1, rotationY: 0, duration: 0.42, ease: "power2.out" }, w(93) - 0.05);
logoIn(lg2, w(93) + 0.05);
fin(g2, { scale: 1 }, { scale: 1.04, duration: 2.0, ease: "none" }, w(93));
pc2.mark([w(94) - 0.05, w(94) + 0.25, w(96) - 0.1, w(96) + 0.2], 0.3);
at(g2, { opacity: 0, y: -60, duration: 0.3, ease: "power2.in" }, 35.5);
pullOut(35.6, 0.5);
// "on purpose": the strip from the post's limitations, over the scale's base
const strip = add(OVER, "glass h", "left:250px;top:1000px;width:580px;height:200px;border-radius:22px", "");
const pc3 = page("p01c", strip, "left:20px;top:16px", 540, 200, true);
const lg3 = logoTile("amark", strip, "right:18px;top:-30px;width:84px;height:52px;border-radius:12px");
fin(strip, { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 0.35, ease: E }, w(104));
pc3.mark([w(104) + 0.2, w(104) + 0.55], 0.4);
out(strip, 39.55, 0.3);
land(5, w(110) + 0.1);

// =============================================================== 5 · FIX
chapter(4, w(111));
pushIn(w(111) - 0.05, 0.5);
const fld = add(OVER, "abs h", "left:200px;top:800px;width:680px;height:150px;border-radius:40px;background:#1a1d26;border:3px solid rgba(200,255,77,0.6);" +
  "display:flex;flex-wrap:wrap;align-content:center;align-items:center;padding:0 112px 0 34px;box-sizing:border-box;font-weight:700;font-size:32px;line-height:1.3;color:#c8ff4d;overflow:hidden", "");
const ph = add(fld, "abs", "left:34px;top:52px;color:#6d7180;font-weight:500", "Message your AI");
const snd = add(fld, "abs", "right:16px;top:41px;width:66px;height:66px;border-radius:50%;background:#c8ff4d;display:flex;align-items:center;justify-content:center",
  '<svg viewBox="0 0 24 24" style="width:34px;height:34px"><path fill="#0b0c10" d="M3 20.5 21 12 3 3.5v6.6l12 1.9-12 1.9z"/></svg>');
fadeIn(fld, w(112), { y: 40 });
// the question types with the voice, word by word
const QW = ["What's", "the", "best", "case", "for", "the", "OTHER", "side?"];
const qs = QW.map((q, i) => add(fld, "", "margin-right:10px;opacity:0" + (i === 6 ? ";text-decoration:underline" : ""), q));
out(ph, w(118) - 0.05, 0.1);
qs.forEach((s, i) => fin(s, { opacity: 0 }, { opacity: 1, duration: 0.08 }, w(118 + i)));
fin(snd, { scale: 1 }, { scale: 0.82, duration: 0.1, yoyo: true, repeat: 1 }, w(125) + 0.2);
// sent: the question floats up into the orb
const sent = add(OVER, "abs h", "left:240px;top:840px;padding:20px 28px;border-radius:30px;background:#2a6df4;color:#fff;font-weight:700;font-size:28px;white-space:nowrap",
  "What's the best case for the OTHER side?");
fin(sent, { opacity: 1, x: 0, y: 0, scale: 1 }, { x: 60, y: -360, scale: 0.25, opacity: 0, duration: 0.55, ease: "power2.in" }, w(125) + 0.3);
gsap.set(sent, { transformOrigin: "50% 50%" });
out(fld, w(125) + 0.3, 0.2);
pullOut(w(126) - 0.05, 0.5);
land(6, w(132) + 0.2);
// "The choice is YOURS": a lime check on the level beam
const chk = add(OVER, "abs h", `left:${P[0] - 40}px;top:${P[1] - 112}px;width:80px;height:80px;border-radius:50%;background:#c8ff4d;box-shadow:0 0 40px rgba(200,255,77,0.6);` +
  "display:flex;align-items:center;justify-content:center;font-weight:900;font-size:50px;color:#0b0c10", "✓");
popIn(chk, w(136), 0.3); out(chk, w(137) + 0.2, 0.3);

// =============================================================== recap and the loop
const lightUp = (ks, t) => ks.forEach((k) => { const p = PE[k];
  at(p, { opacity: 1, duration: 0.3 }, t); at(p.querySelector(".bg"), { color: "#c8ff4d", duration: 0.3 }, t);
  fin(p.querySelector(".glow"), { opacity: 0 }, { opacity: 1, duration: 0.3 }, t); });
lightUp([0, 1, 2, 3, 4], w(144)); [0, 1, 2].forEach((k) => fin(CHE[k], { scale: 1 }, { scale: 1.08, duration: 0.18, yoyo: true, repeat: 1 }, w(144)));
lightUp([5, 6], w(148)); [3, 4].forEach((k) => fin(CHE[k], { scale: 1 }, { scale: 1.08, duration: 0.18, yoyo: true, repeat: 1 }, w(148)));
const hid = el("div", "pin q", `left:${R}px;top:${ROWS[2]}px`, `<div class="glow"></div><div class="bg" style="font-size:31px;top:30px;color:#c8ff4d">THE WORD?</div><div class="lb">seen, never said</div>`, $("#pins"));
popIn(hid, w(150), 0.6);

// the mirror: frame one again (the scale level and empty, the coin spinning, no pins), the end card over it
const TE = w(152) - 0.05;
at("#pins", { opacity: 0, duration: 0.3 }, 52.15);
trkReset(52.35);
fin("#end", { opacity: 0 }, { opacity: 1, duration: 0.45 }, TE);
fin("#world-clip", { opacity: 1, filter: "blur(0px)" }, { opacity: 0.8, filter: "blur(2px)", duration: 0.45 }, TE);
fin("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, TE + 0.15);
fin(["#ename", "#ehandle"], { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.45, ease: E, stagger: 0.12 }, TE + 0.4);
fin("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, TE + 0.85);
at("#fol", { scale: 1.05, duration: 0.4, yoyo: true, repeat: 1, ease: "sine.inOut" }, TE + 1.4);
at(["#bm", "#tag", "#trk"], { opacity: 0, duration: 0.3 }, TE - 0.1);
at([".botshade", ".topshade"], { opacity: 0, duration: 0.4 }, TE);
// "Think YOU'D notice? Because...": the end card clears and the claim card comes back, digits rolling, into frame one
const TB = w(159) - 0.04;
at("#end", { opacity: 0, duration: 0.15 }, TB);
at("#world-clip", { opacity: 1, filter: "blur(0px)", duration: 0.25 }, TB);
at(["#bm", "#tag", "#trk", ".botshade", ".topshade"], { opacity: 1, duration: 0.25 }, TB);
fin(hook, { opacity: 0, x: 0, y: 90, scale: 1 }, { opacity: 1, y: 0, duration: 0.35, ease: E }, TB + 0.16);

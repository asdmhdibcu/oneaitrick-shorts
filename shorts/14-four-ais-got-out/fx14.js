// Short #14: what happens on top of each shot (9:16). Inlined into index.html by make_index.py (helpers in index_template.tpl).
// Visuals sit in y 280-1220; captions own 1240-1460; the bottom ~450 px stays clear for the platform buttons.
// Every key idea is readable without sound (worldwide rule): the chips, big words and the filing's own lines say it.
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
// a stamp that slams on
const stamp = (txt, x, y, rot, col, t0, t1, fs) => { const s = el("div", "stamp", `left:${x}px;top:${y}px;transform:rotate(${rot}deg);color:${col};font-size:${fs || 64}px`, txt);
  tl.fromTo(s, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, t0); out(s, t1); return s; };
// the filing's own lines (word-exact crops of p. 48) on a card; rows light up on their words
const EXS = { inet: [1044, 160, 2], four: [975, 220, 3], abort: [1016, 160, 2], worst: [1028, 280, 4], noev: [1228, 160, 2] };
const excerpt = (name, x, y, wd, t0, t1, marks) => { const [W0, H0, n] = EXS[name]; const s = wd / W0, lh = (H0 - 40) / n;
  const c = el("div", "ex", `left:${x}px;top:${y}px;width:${wd}px`, `<div class="eh">ANTHROPIC · FORM S-1 · P. 48</div><div class="eb"><img src="assets/img/ex_${name}.png" alt="" /></div>`);
  const eb = c.querySelector(".eb");
  (marks || []).forEach(([row, t]) => { const h = el("div", "hl", `left:${22 * s}px;top:${(20 + row * lh + 4) * s}px;width:${(W0 - 44) * s}px;height:${(lh - 10) * s}px`, "", eb);
    tl.to(h, { scaleX: 1, duration: 0.45, ease: "power2.inOut" }, t); });
  tl.fromTo(c, { opacity: 0, y: 30, rotation: -1 }, { opacity: 1, y: 0, rotation: 0, duration: 0.35, ease: "back.out(1.5)" }, t0); out(c, t1); return c; };
const sw = (on) => `<div class="sw2"${on ? ' style="background:var(--lime)"' : ""}><div class="kn"${on ? ' style="left:54px"' : ""}></div></div>`;
const flip = (row, t, toOn) => { const s = row.querySelector(".sw2"), k = row.querySelector(".kn");
  tl.to(k, { left: toOn ? 54 : 6, duration: 0.18, ease: "power2.inOut" }, t);
  tl.to(s, { backgroundColor: toOn ? "#c8ff4d" : "#3a3f4c", duration: 0.18 }, t); };

// ---------- s01 - s03: the result on frame one ----------
tl.fromTo("#title", { opacity: 1, y: 0 }, { opacity: 1, y: 0, duration: 0.01 }, 0);
tl.to("#title", { opacity: 0, y: -20, duration: 0.2 }, B("s01") - 0.15);
(function () { const t = el("div", "term", "left:90px;top:760px;width:900px",
  `<div class="tb"><i></i><i></i><i></i><span>TEST LAB · NEW AI MODEL</span></div>` +
  `<div class="tl" id="t1"><span class="d">$</span> start_test --model new-ai</div><div class="tl" id="t2">internet: <b class="g">OFF ✓</b></div>`);
  tl.fromTo(t, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, 0.25);
  typeOn("#t1", 0.45, 0.03); typeOn("#t2", w(6) - 0.2, 0.04); out(t, B("s01") - 0.06); })();
(function () { const b = big("ONLINE", 175, 560, 200, "#ff5b5b", w(8) - 0.06, B("s02") - 0.04);
  [[14, -6], [-18, 4], [10, 0], [-8, -3], [0, 0]].forEach(([x, k], i) => tl.set(b, { x, skewX: k }, w(8) + 0.05 + i * 0.06));
  const s = el("div", "big", "left:300px;top:790px;font-size:70px;color:#fff", "internet: <span style='color:#ff5b5b'>ON</span>");
  tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.1 }, w(9)); out(s, B("s02") - 0.04); })();
stamp("ACCESS GRANTED", 150, 560, -6, "#ff4d4d", w(12), B("s03") - 0.08, 70);
punch("s03", w(12) + 0.17, 0.05);
chip("A REAL COMPUTER · NOT A TEST", 60, 1100, "#ff6b6b", w(15) - 0.1, B("s03") - 0.08);

// ---------- s04 - s06: the company's own paperwork ----------
(function () { const c = $("#card-s04"); if (!c) return;
  const h = el("div", "hl", "left:39.2%;top:63.2%;width:18.6%;height:9.6%", "", c);
  tl.to(h, { scaleX: 1, duration: 0.5, ease: "power2.inOut" }, w(21)); })();
chip("FORM S-1 · FILED 26 OCT 2026", 60, 1010, "#ffffff", w(18), B("s04") - 0.08);
chip("ANTHROPIC'S OWN FILING", 60, 1100, "var(--lime)", w(21), B("s04") - 0.08);
(function () { const a = el("div", "logo", "left:140px;top:450px;width:800px;height:190px", `<img src="assets/logos/anthropic.png" alt="" />`);
  const c = el("div", "logo", "left:220px;top:780px;width:640px;height:210px", `<img src="assets/logos/claude.png" alt="" />`);
  const m = el("div", "big", "left:0;width:1080px;text-align:center;top:672px;font-size:52px;color:#e8e9ee", "MAKER OF ↓");
  pop(a, w(24) - 0.05, B("s05") - 0.08, 0.6); show(m, w(26) - 0.05, B("s05") - 0.08); pop(c, w(28) - 0.08, B("s05") - 0.08, 0.6); })();
chip("FILED BEFORE ITS STOCK-MARKET DEBUT", 60, 1100, "#ffb547", w(29), B("s06") - 0.08);

// ---------- s07 - s09: the practice room ----------
chip("A NEW AI · NOT OUT YET", 60, 1100, "#7cc4ff", w(37), B("s07") - 0.08);
(function () { const L = el("div", "glass", "left:0"), R = el("div", "glass", "left:535px");
  tl.set([L, R], { opacity: 0 }, 0);
  tl.fromTo(L, { opacity: 1, x: -560 }, { x: 0, duration: 0.45, ease: "power3.in", immediateRender: false }, w(42) - 0.35);
  tl.fromTo(R, { opacity: 1, x: 560 }, { x: 0, duration: 0.45, ease: "power3.in", immediateRender: false }, w(42) - 0.35);
  flash(w(42) + 0.1, 0.25, 0.25);
  const k = el("div", "lock", "left:455px;top:520px",
    `<svg width="96" height="110" viewBox="0 0 96 110"><path d="M22 48V32a26 26 0 0 1 52 0v16" fill="none" stroke="#0b0c10" stroke-width="12"/><rect x="6" y="46" width="84" height="60" rx="12" fill="#0b0c10"/></svg>`);
  pop(k, w(42) + 0.12, B("s07b") - 0.08, 0.3);
  chip("PRACTICE ROOM · LOCKED", 60, 1100, "var(--lime)", w(46), B("s07b") - 0.08);
  out([L, R], B("s07b") - 0.08); })();
(function () { const ms = [0, 1, 2].map((i) => el("div", "mon", `left:${75 + i * 330}px;top:420px`, "<b>TEST</b>"));
  const ts = [0, 1, 2].map((i) => el("div", "tgt", `left:${105 + i * 330}px;top:760px`, "<b>FAKE</b>"));
  ms.forEach((m, i) => pop(m, w(48) + i * 0.1, B("s08") - 0.08, 0.5));
  ts.forEach((m, i) => pop(m, w(50) + i * 0.1, B("s08") - 0.08, 0.3));
  chip("FAKE COMPUTERS", 60, 1010, "#ff6b6b", w(48) + 0.1, B("s08") - 0.08);
  chip("FAKE TARGETS", 60, 1100, "#ff6b6b", w(50) + 0.1, B("s08") - 0.08); })();
(function () { const m = el("div", "map", "left:90px;top:330px;width:900px;height:780px",
  `<svg width="900" height="780" viewBox="0 0 900 780">
    <rect x="0" y="0" width="900" height="780" fill="#33452f"/>
    <g fill="#5b6b57">${[[60, 60], [560, 60], [60, 470], [560, 470]].map(([x, y]) => `<rect x="${x}" y="${y}" width="280" height="250" rx="18"/>`).join("")}</g>
    <path d="M0 390 H900 M450 0 V780" stroke="#4a4f57" stroke-width="150"/>
    <path d="M0 390 H900 M450 0 V780" stroke="#e8e2c8" stroke-width="5" stroke-dasharray="30 26"/>
    <g fill="#ff8a1f">${[[150, 330], [260, 450], [370, 330], [600, 450], [710, 330], [450, 600], [520, 170]].map(([x, y]) => `<path d="M${x} ${y - 30} l18 46 h-36 z"/>`).join("")}</g>
    <text x="450" y="760" fill="#e8e9ee" font-family="Mono, monospace" font-weight="700" font-size="30" text-anchor="middle" letter-spacing="4">FAKE TOWN · TEST COURSE</text>
    <path id="route" d="M40 420 C 200 420, 210 360, 330 390 S 470 450, 560 380 S 760 360, 860 400" fill="none" stroke="rgba(200,255,77,0.0)"/>
  </svg>
  <div id="car" style="position:absolute;left:0;top:0;width:96px;height:52px;border-radius:14px;background:#7cc4ff;box-shadow:0 8px 20px rgba(0,0,0,0.5)">
    <div style="position:absolute;left:60px;top:8px;width:26px;height:36px;border-radius:6px;background:#1b2433"></div>
    <div style="position:absolute;left:8px;top:-22px;padding:2px 8px;border-radius:6px;background:#e0322b;color:#fff;font-weight:900;font-size:22px">L</div></div>`);
  tl.fromTo(m, { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, A("s09") - 0.05);
  if (window.MotionPathPlugin) tl.fromTo("#car", { x: -8, y: 394 }, { motionPath: { path: "#route", align: "#route", autoRotate: true, alignOrigin: [0.5, 0.5] },
    duration: B("s09") - A("s09") - 0.1, ease: "none", immediateRender: true }, A("s09"));
  chip("LIKE A DRIVING TEST", 60, 1140, "#ffb547", w(54), B("s09") - 0.08);
  out(m, B("s09") - 0.08); })();

// ---------- s10 - s11: a gate left open (the hidden word, UNLOCKED, is on the gate post; never said) ----------
(function () { const g = el("div", "gsign", "left:735px;top:700px;transform:rotate(-4deg)", "UNLOCKED", $("#cam-s10"));
  tl.fromTo(g, { opacity: 0 }, { opacity: 1, duration: 0.25 }, A("s10") - 0.1);
  chip("SOMEONE LEFT A GATE OPEN", 60, 1100, "#ffb547", w(62), B("s10") - 0.08); })();
(function () { excerpt("inet", 70, 300, 940, A("s11") + 0.1, B("s11") - 0.08, [[0, w(70) - 0.3], [1, w(73)]]);
  const g = el("div", "", "position:absolute;left:740px;top:560px;width:260px;height:260px;opacity:0",
    `<svg width="260" height="260" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="rgba(124,196,255,0.18)" stroke="#7cc4ff" stroke-width="4"/>
     <ellipse cx="50" cy="50" rx="20" ry="44" fill="none" stroke="#7cc4ff" stroke-width="3"/><path d="M6 50 H94 M12 28 H88 M12 72 H88" stroke="#7cc4ff" stroke-width="3"/></svg>`);
  g.style.filter = "drop-shadow(0 0 24px rgba(124,196,255,0.9))";
  pop(g, w(70), B("s11") - 0.08, 0.4);
  chip("CONNECTED TO THE REAL INTERNET", 60, 1100, "#7cc4ff", w(72), B("s11") - 0.08); })();

// ---------- s12 - s14: four got out, for hours, into other people's computers ----------
chip("4 AI MODELS WENT THROUGH", 60, 1100, "var(--lime)", w(75) + 0.05, B("s12") - 0.08);
(function () { const c = el("div", "big", "left:0;width:1080px;text-align:center;top:250px;font-size:200px;color:#fff", "<span id='hc'>10</span>");
  const l = el("div", "big", "left:0;width:1080px;text-align:center;top:440px;font-size:58px;color:#ffb547", "HOURS OF WORK");
  tl.fromTo([c, l], { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, w(81) - 0.1);
  const n = { v: 10 }; tl.fromTo(n, { v: 10 }, { v: 34, duration: 0.8, ease: "power2.inOut", onUpdate() { $("#hc").textContent = Math.round(n.v); } }, w(83));
  tl.set("#hc", { color: "#ffb547" }, w(83) + 0.8);
  chip("10 TO 34 HOURS OF WORK", 60, 1100, "#ffb547", w(84), B("s13") - 0.08); out([c, l], B("s13") - 0.08); })();
excerpt("four", 70, 300, 940, A("s14") + 0.1, B("s14") - 0.08, [[0, w(87)], [1, w(89) + 0.1], [2, w(93)]]);
chip("REAL SYSTEMS · OTHER PEOPLE'S", 60, 1100, "#ff6b6b", w(94), B("s14") - 0.08);

// ---------- s15 - s20: the worst case ----------
(function () { excerpt("abort", 70, 290, 940, A("s15") + 0.1, B("s15") - 0.08, [[0, w(104)], [1, w(109)]]);
  const p = el("div", "pbar", "left:90px;top:520px;width:836px",
    `<div class="lb"><span>TASK: IMPOSSIBLE</span><span id="pct">0%</span></div><div class="tr"><div class="fi" id="pfi"></div></div>`);
  tl.fromTo(p, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, w(105) - 0.1);
  const q = { v: 0 }; tl.fromTo(q, { v: 0 }, { v: 99, duration: 1.4, ease: "power2.out", onUpdate() { $("#pct").textContent = Math.round(q.v) + "%"; } }, w(105));
  tl.fromTo("#pfi", { scaleX: 0 }, { scaleX: 0.99, duration: 1.4, ease: "power2.out" }, w(105));
  [0, 1, 2].forEach((i) => tl.to("#pct", { opacity: 0.2, duration: 0.15, yoyo: true, repeat: 1 }, w(109) + i * 0.4));
  const s = el("div", "stopb", "left:395px;top:760px", "STOP");
  tl.fromTo(s, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, w(110) - 0.1);
  tl.to(s, { y: 8, boxShadow: "0 2px 0 #8d1712, 0 10px 20px rgba(0,0,0,0.5)", duration: 0.08, yoyo: true, repeat: 3 }, w(112));
  stamp("✕ IT COULDN'T STOP", 240, 920, -4, "#ff4d4d", w(113) - 0.05, B("s15") - 0.08, 50);
  out([p, s], B("s15") - 0.08); })();
(function () { const n = el("div", "note2", "left:600px;top:400px;transform:rotate(5deg)", "password:<br/><b>••••••••</b>");
  tl.fromTo(n, { opacity: 0, y: -60, rotation: 20 }, { opacity: 1, y: 0, rotation: 5, duration: 0.3, ease: "back.out(1.6)" }, A("s16") + 0.05);
  out(n, B("s16") - 0.06);
  chip("PASSWORD FOUND", 60, 1100, "#ffb547", w(116), B("s16") - 0.06); })();
// the four steps: the filing's lines stay up top while each step plays below them
(function () { const c = excerpt("worst", 70, 290, 940, A("s17") + 0.05, B("s20") - 0.08, [[0, w(119)], [1, w(122)], [2, w(126) + 0.1], [3, w(132)]]);
  const t = el("div", "term", "left:90px;top:620px;width:900px",
    `<div class="tb"><i></i><i></i><i></i><span>A THIRD PARTY'S COMPUTER</span></div>` +
    `<div class="tl" id="a1"><span class="d">$</span> login --password ••••••</div><div class="tl" id="a2">role: user <span class="d">→</span> <b class="g">ADMIN</b></div>`);
  tl.fromTo(t, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, A("s17"));
  typeOn("#a1", A("s17") + 0.1, 0.025); typeOn("#a2", w(122) - 0.25, 0.035);
  const cr = el("div", "", "position:absolute;left:640px;top:665px;opacity:0",
    `<svg width="150" height="100" viewBox="0 0 150 100"><path d="M10 90 L20 20 L50 55 L75 8 L100 55 L130 20 L140 90 Z" fill="#ffd34d" stroke="#0b0c10" stroke-width="5"/></svg>`);
  tl.fromTo(cr, { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: 0.3, ease: "bounce.out" }, w(122) + 0.1);
  chip("BOSS OF THE COMPUTER", 60, 1100, "var(--lime)", w(122), B("s17") - 0.06);
  out([t, cr], B("s17") - 0.06);
  const r = el("div", "rows", "left:90px;top:620px;width:836px", `<div class="hd">PASSWORDS COLLECTED</div>` +
    [1, 2, 3, 4].map((i) => `<div class="rw"><span>account_0${i}</span><b>••••••••</b></div>`).join(""));
  tl.fromTo(r, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2, ease: E }, A("s18"));
  r.querySelectorAll(".rw").forEach((x, i) => tl.fromTo(x, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.18 }, w(126) + 0.1 + i * 0.18));
  chip("MORE PASSWORDS", 60, 1100, "#ffb547", w(127), B("s18") - 0.06); out(r, B("s18") - 0.06);
  const st = el("div", "rows", "left:90px;top:620px;width:836px", `<div class="hd">SETTINGS</div>` +
    [["Firewall", 1], ["Logging", 1], ["Remote access", 0]].map(([k, on]) => `<div class="rw" style="opacity:1"><span>${k}</span>${sw(on)}</div>`).join(""));
  tl.fromTo(st, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2, ease: E }, A("s19"));
  const rws = st.querySelectorAll(".rw"); flip(rws[0], w(129) + 0.1, false); flip(rws[1], w(129) + 0.3, false); flip(rws[2], w(130) + 0.2, true);
  chip("SETTINGS CHANGED", 60, 1100, "#ffb547", w(129) + 0.1, B("s19") - 0.06); out(st, B("s19") - 0.06);
  const pf = el("div", "prof", "left:190px;top:600px;width:620px", `<div class="av"></div>` +
    ["NAME", "ADDRESS", "PHONE"].map((k, i) => `<div class="f"><span>${k}</span><div class="x" id="x${i}" style="width:${[340, 380, 300][i]}px"></div></div>`).join(""));
  tl.fromTo(pf, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, A("s20") + 0.05);
  [0, 1, 2].forEach((i) => tl.to("#x" + i, { scaleX: 1, duration: 0.3, ease: "power2.out" }, w(133) + i * 0.25));
  stamp("PRIVATE", 560, 600, 8, "#ff4d4d", w(136), B("s20") - 0.08, 56);
  chip("ONE PERSON'S PRIVATE INFO", 60, 1100, "#ff6b6b", w(135), B("s20") - 0.08); out(pf, B("s20") - 0.08); })();

// ---------- s21 - s22: the twist ----------
bigLetters("THE TWIST", 150, 420, 130, "var(--lime)", w(140) - 0.05, B("s21") - 0.06);
(function () { chip("IT WASN'T TRYING TO ESCAPE", 60, 1100, "var(--lime)", w(142), B("s21b") - 0.08);
  const d = el("div", "tag", "left:70px;top:330px;font-size:24px;background:#2a6df4", "OPEN DOOR · IGNORED ↓");
  show(d, w(144), B("s21b") - 0.08); })();
(function () { const c = excerpt("noev", 60, 400, 960, A("s22") + 0.05, B("s22") - 0.08, [[0, w(148)], [1, w(155)]]);
  const h = el("div", "big", "left:60px;top:330px;font-size:34px;color:#e8e9ee;font-family:Mono, monospace;letter-spacing:0.08em", "ANTHROPIC'S INVESTIGATION");
  show(h, A("s22") + 0.05, B("s22") - 0.08);
  chip("✓ NO GOALS BEYOND ITS TASK", 60, 1100, "var(--lime)", w(155), B("s22") - 0.08);
  const j = el("div", "big", "left:60px;top:680px;font-size:96px;color:#fff;line-height:1.0", "JUST TRYING TO<br/><span style='color:var(--lime)'>FINISH THE JOB</span>");
  tl.fromTo(j, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, w(162)); out(j, B("s22") - 0.08); })();

// ---------- s23 - s26: the takeaway ----------
chip("REMEMBER THIS", 60, 1100, "#ffb547", w(170), w(176) - 0.1);
(function () { const b = big("EVIL AI?", 150, 520, 190, "#ff5b5b", w(177) - 0.05, B("s23") - 0.08);
  const x = el("div", "strike", "left:120px;top:610px;width:840px;height:22px;transform:rotate(-8deg) scaleX(0)");
  tl.to(x, { scaleX: 1, duration: 0.2, ease: "power3.out" }, w(178) + 0.1); out(x, B("s23") - 0.08);
  chip("✕ NOT NEEDED", 60, 1100, "#ff6b6b", w(178) + 0.1, B("s23") - 0.08); })();
bigLetters("DETERMINED", 70, 430, 140, "var(--lime)", w(181) - 0.05, B("s24") - 0.08);
chip("+ ONE OPEN DOOR", 60, 1100, "#ffb547", w(184), B("s24") - 0.08);
(function () { const d = el("div", "dialog", "left:110px;top:380px;width:860px",
  `<div class="q">An AI helper wants access to:</div>` +
  [["✉ Email", "e1"], ["📁 Files", "e2"], ["🏦 Bank account", "e3"]].map(([k, id]) => `<div class="rw" id="${id}"><span>${k}</span>${sw(0)}</div>`).join(""));
  tl.fromTo(d, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.5)" }, A("s25") + 0.1);
  flip($("#e1"), w(195), true); flip($("#e2"), w(197), true); flip($("#e3"), w(200) + 0.1, true);
  const wn = el("div", "tag", "left:110px;top:1000px;font-size:30px", "⚠ ALL OF IT?"); show(wn, w(201) + 0.1, B("s25") - 0.08);
  out(d, B("s25") - 0.08); })();
(function () { const r = el("div", "ring", "left:470px;top:820px;width:260px;height:260px", "", $("#cam-s26"));
  tl.fromTo(r, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, w(204)); out(r, B("s26") - 0.08);
  chip("ONLY THE KEYS IT NEEDS", 60, 1100, "var(--lime)", w(204), B("s26") - 0.08); })();

// ---------- s27: back at the gate (UNLOCKED readable for a beat) ----------
(function () { const g = el("div", "gsign", "left:640px;top:720px;transform:rotate(3deg)", "UNLOCKED", $("#cam-s27"));
  tl.fromTo(g, { opacity: 0 }, { opacity: 1, duration: 0.25 }, A("s27") - 0.1);
  chip("COMMENT THE WORD 💬", 60, 1100, "var(--lime)", w(222), B("s27") - 0.08); })();

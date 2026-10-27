// Short #11: what happens on top of each shot (9:16). Inlined into index.html by make_index.py (helpers in index_template.tpl).
// Visuals sit in y 280-1220; captions own 1240-1460; the bottom ~450 px stays clear for the platform buttons.

// ---------- k01: the result on frame one, the ten logos snap in on "biggest AI companies" ----------
const TEN = ["L9", "L7", "L10", "L12", "L13", "L5", "L4", "L11", "L2", "L14"];
(function () { tl.fromTo("#title", { opacity: 1, y: 0 }, { opacity: 1, y: 0, duration: 0.01 }, 0);
  tl.to("#title", { opacity: 0, y: -20, duration: 0.2 }, B("k01") - 0.15);
  TEN.forEach((c, j) => { const d = logo(c, 60 + (j % 2) * 490, 700 + Math.floor(j / 2) * 102, 470, 86);
    tl.fromTo(d, { opacity: 0, x: j % 2 ? 60 : -60, scale: 0.8 }, { opacity: 1, x: 0, scale: 1, duration: 0.28, ease: "back.out(2)" }, w(3) + j * 0.08);
    tl.to(d, { opacity: 0, duration: 0.15 }, B("k01") - 0.15); });
  punch("k01", w(14), 0.04); })();

// ---------- k02 - k04: the UK; the regulator knocks ----------
chip("THE UK", 60, 1100, "#ffffff", w(17), B("k02") - 0.1);
(function () { const d = logo("L1", 600, 320, 420, 240, "THE REGULATOR"); pop(d, w(30), B("k04") - 0.08, 0.3); punch("k04", w(31), 0.05); punch("k04", w(32) + 0.05, 0.05); })();

// ---------- k05 - k09: postcards, the sorting office ----------
chip("NOT SEALED", 60, 1100, "#ffb547", w(47), B("k06") - 0.1);
chip("ANYONE CAN READ IT", 60, 1100, "#ffb547", w(54) - 0.1, B("k07") - 0.1);
chip("SORTING OFFICE = AI TRAINING", 60, 1100, "var(--lime)", w(65), B("k08") - 0.1);
badge("k09", "L4", "META");

// ---------- k10 - k14b: the big one ----------
chip("THE BIG ONE · SENSITIVE DATA", 60, 300, "var(--lime)", w(77), B("k10") - 0.1, { y: -20 });
badge("k10", "L1", "ICO REPORT");
big("HEALTH", 60, 900, 170, "#ffffff", w(86), B("k11") - 0.02);
big("RELIGION", 60, 900, 160, "#ffffff", w(88), B("k12") - 0.02);
big("POLITICS", 60, 900, 160, "#ffffff", w(91) - 0.1, B("k13") - 0.02);
badge("k14", "L1", "ICO REPORT");
(function () { const st = el("div", "stamp", "left:110px;top:640px;font-size:104px;transform:rotate(-5deg)", "ASSUME IT HAS");
  tl.fromTo(st, { opacity: 0, scale: 2.4 }, { opacity: 0.95, scale: 1, duration: 0.2, ease: "power4.out" }, w(109)); tl.to(st, { opacity: 0, duration: 0.15 }, B("k14b") - 0.1);
  const d = logo("L1", 340, 380, 400, 220, "THE ICO'S VIEW"); pop(d, A("k14b") + 0.02, B("k14b") - 0.1, 0.5);
  tl.fromTo(cam("k14b"), { filter: "grayscale(0)" }, { filter: "grayscale(0.8) brightness(0.7)", duration: 0.4 }, A("k14b")); })();

// ---------- k15 - k16b: what they changed ----------
badge("k15", "L1", "ICO REPORT");
const GRIDW = { L9: 117, L7: 118, L10: 119, L12: 120, L13: 121, L5: 122, L4: 123, L11: 124, L2: 125, L14: 127 };
const gridAt = (id, tIn, stagger, cols) => { const out = {}; const C = cols || 2;
  TEN.forEach((c, j) => { const tw = C === 2 ? 430 : 300, th = C === 2 ? 118 : 100;
    const x = C === 2 ? 90 + (j % 2) * 470 : 60 + (j % 3) * 330, y = C === 2 ? 320 + Math.floor(j / 2) * 168 : 330 + Math.floor(j / 3) * 150;
    const d = logo(c, x, y, tw, th, null, $("#cam-" + id)); out[c] = d;
    const t = stagger ? w(GRIDW[c]) : tIn;
    tl.fromTo(d, { opacity: 0, scale: 0.5, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.28, ease: "back.out(2.2)" }, t); }); return out; };
gridAt("k16", 0, true);
(function () { const G = gridAt("k16b", A("k16b") - 0.1, false);
  TEN.forEach((c, j) => tl.fromTo(G[c].querySelector(".ok"), { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(3)" }, w(131) + j * 0.06));
  chip("MADE CHANGES · OR PROMISED TO", 60, 1160, "var(--lime)", w(131), B("k16b") - 0.1, { y: 20 }); })();

// ---------- k17 - k19: the twist ----------
(function () { tl.fromTo(cam("k17"), { filter: "grayscale(0) brightness(1)" }, { filter: "grayscale(1) brightness(0.45)", duration: 0.4, ease: "power2.out" }, A("k17"));
  const t = el("div", "big", "left:60px;top:560px;font-size:120px;color:#ffffff;white-space:normal;width:960px;text-shadow:0 0 60px rgba(0,0,0,0.9)", "The bit nobody's<br/>talking about");
  tl.fromTo(t, { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, w(137)); tl.to(t, { opacity: 0, duration: 0.15 }, B("k17") - 0.1); })();
badge("k19", "L4", "META");

// ---------- k20 - k21: one name's missing ----------
(function () { const G = gridAt("k20", A("k20") - 0.1, false, 3);
  const slot = el("div", "logo slot", "left:390px;top:780px;width:300px;height:100px;font-weight:900;font-size:64px;color:#fff;opacity:0", "?", $("#cam-k20"));
  tl.fromTo(slot, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, w(159));
  for (let k = 0; k < 4; k++) tl.to(slot, { opacity: k % 2 ? 1 : 0.35, duration: 0.12 }, w(160) + 0.15 + k * 0.14); })();
(function () { const x = logo("L16", 140, 520, 800, 240, "XAI · THE COMPANY BEHIND GROK", $("#cam-k20b"));
  tl.fromTo(x, { opacity: 0, y: -400, scale: 1.2 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "bounce.out" }, A("k20b") - 0.05); })();
(function () { const d = badge("k21", "L16", "XAI · GROK");
  const t = el("div", "tag", "", "UNDER INVESTIGATION", d); tl.set(t, { left: -40, top: 108 }, 0);
  tl.fromTo(t, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.out" }, w(177)); })();

// ---------- k22 - k23: switch it off ----------
chip("SWITCH OFF TRAINING", 580, 330, "var(--lime)", w(181), B("k22") - 0.1, { x: 30, y: 0 });
phoneCam("k22", w(183), 1.5);
steps("k23", "L3", [["CHATGPT", "Settings", w(190)], ["", "Data controls", w(191)], ["", "Improve the model for everyone", w(193)]], A("k23") + 4.75);
phoneCam("k23", A("k23") + 3.4, 1.25);

// ---------- k24 - k25: the takeaway ----------
chip("PUBLIC POSTS ARE POSTCARDS", 60, 1100, "var(--lime)", w(201), B("k24") - 0.1);

// ---------- the report's small print, set large on top of the real page (k10, k14, k21) ----------
const quoteOver = (id, kicker, html, tHl, t0) => { const q = el("div", "quote", "left:50px;top:470px;width:980px;padding:36px 40px 32px", `<div class="qk">${kicker}</div><div class="qt" style="font-size:50px">${html}</div>`);
  tl.fromTo(q, { opacity: 0, y: 50, rotation: -1.2 }, { opacity: 1, y: 0, rotation: -0.5, duration: 0.35, ease: "back.out(1.4)" }, t0 || A(id) + 0.55);
  q.querySelectorAll(".qh").forEach((h, k) => tl.to(h, { backgroundSize: "100% 80%", duration: 0.45, ease: "power2.inOut" }, tHl + k * 0.25));
  tl.to(q, { opacity: 0, duration: 0.15 }, B(id) - 0.1);
  tl.to("#card-" + id, { opacity: 0.35, duration: 0.3 }, (t0 || A(id) + 0.55)); return q; };
quoteOver("k10", "● QUOTED · ICO REPORT, P.19", 'Social media posts often contain information about a person’s <span class="qh">political opinions, religious beliefs or health.</span>', w(82));
quoteOver("k14", "● QUOTED · ICO REPORT, P.19", 'Developers are likely to be processing special category data <span class="qh">unless they can clearly demonstrate</span> the datasets they’ve used for training do not use it.', w(97), A("k14") + 0.9);
quoteOver("k21", "● QUOTED · ICO REPORT, P.25", 'Because of the announcement of this investigation, we decided to <span class="qh">suspend engagement with X.AI</span>', w(172), A("k21") + 0.7);

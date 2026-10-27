// #11 video: what happens on top of each shot. Inlined into index.html by make_index.py (helpers in index_template.tpl).
// Times come from the words (w(k) = start of word k) and the shots (A(id) = cut in, B(id) = cut out).

// ---------- v01: the claim on frame one, the ten logos snap in on "biggest AI companies" ----------
(function () { tl.fromTo("#title", { opacity: 1, y: 0 }, { opacity: 1, y: 0, duration: 0.01 }, 0);
  tl.to("#title", { opacity: 0, y: -20, duration: 0.2 }, B("v01") - 0.15);
  const TEN = ["L9", "L7", "L10", "L12", "L13", "L5", "L4", "L11", "L2", "L14"];
  TEN.forEach((c, j) => { const d = logo(c, 120 + (j % 5) * 250, 620 + Math.floor(j / 5) * 140, 220, 110);
    tl.fromTo(d, { opacity: 0, y: 40, scale: 0.6 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2)" }, w(3) + j * 0.09);
    tl.to(d, { opacity: 0, duration: 0.15 }, B("v01") - 0.15); });
  punch("v01", w(14), 0.04); })();

// ---------- v02 / v04: the UK; the regulator ----------
chip("THE UK", 120, 760, "#ffffff", w(17), B("v02") - 0.1);
(function () { const d = logo("L1", 1320, 300, 380, 220, "THE REGULATOR"); pop(d, w(30), B("v04") - 0.08, 0.3); punch("v04", w(31) + 0.1, 0.05); })();

// ---------- v05: anything YOU can do ----------
punch("v05", w(41), 0.05);

// ---------- v07 / v08: every review, post, comment, caption ----------
(function () { const W = [[54, "REVIEWS"], [60, "POSTS"], [62, "COMMENTS"], [65, "CAPTIONS"]];
  W.forEach(([k, t], j) => { const c = el("div", "big", `left:${1240 + (j % 2) * 40}px;top:${180 + j * 150}px;font-size:96px;color:${j % 2 ? "#ffffff" : "var(--lime)"}`, t);
    tl.fromTo(c, { opacity: 0, x: 60, rotation: j % 2 ? 3 : -3 }, { opacity: 1, x: 0, rotation: j % 2 ? 2 : -2, duration: 0.25, ease: "back.out(2)" }, w(k));
    tl.to(c, { opacity: 0, duration: 0.15 }, B("v08") - 0.12); }); })();

// ---------- v09 - v13: postcards, the sorting office ----------
chip("NOT SEALED", 120, 760, "#ffb547", w(80), B("v10") - 0.1);
chip("ANYONE CAN READ IT", 120, 760, "#ffb547", w(87) - 0.1, B("v11") - 0.1);
chip("THE SORTING OFFICE = AI TRAINING", 120, 760, "var(--lime)", w(98), B("v12") - 0.1);
big("BILLIONS", 120, 620, 150, "var(--lime)", w(101), B("v13") - 0.1);

// ---------- v14: the data watchdog is the ICO ----------
(function () { const d = logo("L1", 1240, 330, 520, 300); pop(d, w(116), B("v14") - 0.08, 0.3);
  chip("THE UK'S DATA WATCHDOG", 1240, 690, "#ffffff", w(116) + 0.2, B("v14") - 0.1, { y: 20 }); })();

// ---------- v15: eleven of the biggest sorting offices (ten logos and one name held back) ----------
(function () { const ELEVEN = ["L9", "L7", "L10", "L12", "L13", "L5", "L4", "L11", "L2", "L14", "?"];
  ELEVEN.forEach((c, j) => { const x = 230 + (j % 6) * 250, y = 290 + Math.floor(j / 6) * 190;
    const d = c === "?" ? el("div", "logo slot", `left:${x}px;top:${y}px;width:220px;height:110px;font-weight:900;font-size:64px;color:#fff`, "?") : logo(c, x, y, 220, 110);
    tl.fromTo(d, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, w(126) + j * 0.07);
    tl.to(d, { opacity: 0, duration: 0.15 }, B("v15") - 0.1); });
  big("11", 230, 670, 170, "var(--lime)", w(128), B("v15") - 0.1);
  chip("THE ICO'S PRIORITY LIST", 470, 720, "#ffffff", w(128) + 0.15, B("v15") - 0.1); })();

// ---------- v16: the report, 8 October ----------
badge("v16", "L1", "ICO REPORT");

// ---------- v17: a mixed bag ----------
(function () { const g = el("div", "score", "left:280px;top:250px;color:var(--lime)", '<div class="si">✓</div><div class="sl">Some real changes</div>');
  const b = el("div", "score", "left:1000px;top:250px;color:#ff6b6b", '<div class="si">✗</div><div class="sl">Some real problems</div>');
  tl.fromTo(g, { opacity: 0, x: -60, rotation: -3 }, { opacity: 1, x: 0, rotation: -2, duration: 0.3, ease: "back.out(1.8)" }, w(150));
  tl.fromTo(b, { opacity: 0, x: 60, rotation: 3 }, { opacity: 1, x: 0, rotation: 2, duration: 0.3, ease: "back.out(1.8)" }, w(151) + 0.1);
  tl.to([g, b], { opacity: 0, duration: 0.15 }, B("v17") - 0.1); })();

// ---------- v18 - v28: the three findings ----------
chip("FINDING 1 · VAGUE REASONS", 120, 110, "var(--lime)", w(153), B("v18") - 0.1);
badge("v18", "L1", "ICO REPORT");
badge("v19", "L1", "ICO REPORT");
(function () { // v19b: "benefitting humanity" is not a reason
  const q = el("div", "quote", "left:330px;top:250px;width:1260px", '<div class="qk">● THE ICO REPORT, P.14 · TOO BROAD, IT SAYS</div><div class="qt" id="humq" style="display:inline-block;font-size:92px">“benefitting humanity”</div>');
  tl.fromTo(q, { opacity: 0, y: 40, rotation: -1.5 }, { opacity: 1, y: 0, rotation: -0.6, duration: 0.35, ease: "back.out(1.4)" }, A("v19b") - 0.05);
  tl.to(q, { opacity: 0, duration: 0.15 }, B("v19b") - 0.1);
  const s = el("div", "strike", "left:-12px;right:-12px;top:50%;", undefined, q.querySelector("#humq")); tl.to(s, { scaleX: 1, duration: 0.3, ease: "power2.inOut" }, w(180));
  tl.to(s, { opacity: 0, duration: 0.15 }, B("v19b") - 0.1);
  const st = el("div", "stamp", "left:1080px;top:560px;transform:rotate(-6deg)", "NOT A REASON");
  tl.fromTo(st, { opacity: 0, scale: 2.2 }, { opacity: 0.95, scale: 1, duration: 0.18, ease: "power4.out" }, w(182)); tl.to(st, { opacity: 0, duration: 0.15 }, B("v19b") - 0.1);
  const d = logo("L1", 380, 580, 260, 150); pop(d, A("v19b") + 0.1, B("v19b") - 0.1, 0.5); })();
chip("FINDING 2 · THE SMALL PRINT", 120, 110, "var(--lime)", w(183), B("v20") - 0.1);
badge("v20", "L1", "ICO REPORT"); badge("v21", "L1", "ICO REPORT"); badge("v22", "L1", "ICO REPORT");
big("WORSE", 1300, 760, 120, "#ff6b6b", w(210), B("v22") - 0.1);
chip("FINDING 3 · SENSITIVE DATA", 120, 110, "var(--lime)", w(211), B("v23") - 0.1);
badge("v24", "L1", "ICO REPORT");
big("HEALTH", 120, 640, 170, "#ffffff", w(227), B("v25") - 0.02);
big("RELIGION", 120, 640, 170, "#ffffff", w(229), B("v26") - 0.02);
big("POLITICS", 120, 640, 170, "#ffffff", w(232), B("v27") - 0.02);
badge("v28", "L1", "ICO REPORT");

// ---------- v29 - v35: what they changed ----------
badge("v29", "L1", "ICO REPORT");
const GRID = ["L9", "L7", "L10", "L12", "L13", "L5", "L4", "L11", "L2", "L14"];
const GRIDW = { L9: 258, L7: 259, L10: 260, L12: 261, L13: 262, L5: 263, L4: 264, L11: 265, L2: 266, L14: 268 };
const gridAt = (id, tIn, stagger) => { const out = {};
  GRID.forEach((c, j) => { const x = 230 + (j % 5) * 300, y = 220 + Math.floor(j / 5) * 250;
    const d = logo(c, x, y, 260, 140, (LOGOS[c] || {}).name, $("#cam-" + id)); out[c] = d;
    const t = stagger ? w(GRIDW[c]) : tIn;
    tl.fromTo(d, { opacity: 0, scale: 0.5, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.2)" }, t); }); return out; };
(function () { const G = gridAt("v30", 0, true);
  GRID.forEach((c, j) => tl.fromTo(G[c].querySelector(".ok"), { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(3)" }, w(272) + j * 0.06));
  chip("MADE CHANGES · OR PROMISED TO", 640, 760, "var(--lime)", w(272), B("v30") - 0.1); })();
badge("v31", "L1", "ICO REPORT");
(function () { const G = gridAt("v32", A("v32") - 0.1, false);
  ["L9", "L7", "L12", "L13", "L5", "L11", "L14"].forEach((c) => tl.to(G[c], { opacity: 0.22, scale: 0.94, duration: 0.3 }, w(302)));
  ["L2", "L4", "L10"].forEach((c, j) => { tl.to(G[c], { scale: 1.12, boxShadow: "0 0 60px rgba(200,255,77,0.7)", duration: 0.3, ease: "back.out(2)" }, w(302) + j * 0.08);
    tl.to(G[c].querySelector(".ok"), { opacity: 1, duration: 0.2 }, w(302) + j * 0.08); });
  chip("GENUINELY USEFUL", 760, 760, "var(--lime)", w(302), B("v32") - 0.1); })();
badge("v33", "L2", "OPENAI HELP CENTER");
(function () { const d = logo("L3", 1500, 760, 220, 110, "CHATGPT"); pop(d, w(319), B("v33") - 0.08, 0.5); })();
badge("v34", "L4", "META");
badge("v35", "L10", "APPLE");

// ---------- v36: the record scratch ----------
(function () { tl.set(cam("v36"), Object.assign({ transformOrigin: "0px 0px" }, CAMEND["v35"] || {}), A("v36") - 0.3);
  tl.fromTo(cam("v36"), { filter: "grayscale(0) contrast(1) brightness(1)" }, { filter: "grayscale(1) contrast(1.1) brightness(0.42)", duration: 0.5, ease: "power2.out" }, A("v36"));
  const t = el("div", "big", "left:120px;top:330px;font-size:110px;color:#ffffff;white-space:normal;width:1500px;text-shadow:0 0 60px rgba(0,0,0,0.9), 0 10px 40px rgba(0,0,0,0.9)", "The bit nobody's<br/>talking about");
  tl.fromTo(t, { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, w(350)); tl.to(t, { opacity: 0, duration: 0.15 }, B("v36") - 0.1);
  tl.to("#card-v36", { opacity: 0.12, scale: 0.94, duration: 0.35, ease: "power2.out" }, w(350) - 0.1); })();

// ---------- v37 - v44 ----------
badge("v38", "L4", "META'S OWN PAGE");
badge("v39", "L1", "ICO REPORT");
chip("REBUILD THE WHOLE MODEL", 120, 760, "#ffb547", w(384), B("v40") - 0.1);
badge("v41", "L1", "ICO REPORT");
chip("→ THE UK GOVERNMENT", 120, 760, "#ffffff", w(411), B("v42") - 0.1);
(function () { // v43: one name's missing; xAI and Grok drop into the slot
  const G = gridAt("v43", A("v43") - 0.1, false);
  const slot = el("div", "logo slot", "left:830px;top:740px;width:260px;height:140px;font-weight:900;font-size:70px;color:#fff;opacity:0", "?", $("#cam-v43"));
  tl.fromTo(slot, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, w(415));
  for (let k = 0; k < 4; k++) tl.to(slot, { opacity: k % 2 ? 1 : 0.35, duration: 0.12 }, w(416) + 0.15 + k * 0.14);
  tl.to(slot, { opacity: 0, duration: 0.1 }, w(418) - 0.05);
  const x = logo("L16", 830, 740, 260, 140, "XAI · GROK", $("#cam-v43"));
  tl.fromTo(x, { opacity: 0, y: -260, scale: 1.2 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "bounce.out" }, w(418) - 0.05);
  GRID.forEach((c) => tl.to(G[c], { opacity: 0.3, duration: 0.3 }, w(418))); })();
(function () { const d = badge("v44", "L16", "XAI · GROK");
  const t = el("div", "tag", "", "UNDER INVESTIGATION", d); tl.set(t, { left: 10, top: 120 }, 0);
  tl.fromTo(t, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.out" }, w(433)); })();

// ---------- v45 - v49: AI agents ----------
badge("v45", "L1", "ICO NEWS RELEASE");
chip("REPORTEDLY · SUMMER 2026 TESTS", 120, 760, "#ffb547", w(461), B("v47") - 0.1);
badge("v48", "L1", "ICO REPORT");
(function () { // v49: the call for evidence behind, Nevinson's words in front
  const g = GEO["v49b"]; const c = el("div", "card", `left:${g.left}px;top:${g.top}px;width:${g.w}px;height:${g.h}px`, `<img src="assets/pages/p3_dates.png" style="width:${g.w}px" />`, $("#cam-v49"));
  tl.fromTo(c, { opacity: 0, rotation: -4, scale: 0.9 }, { opacity: 1, rotation: -3, scale: 0.92, duration: 0.35, ease: "back.out(1.4)" }, A("v49") - 0.05);
  tl.to(c, { opacity: 0.35, scale: 0.86, duration: 0.4 }, w(478));
  const q = el("div", "quote", "left:300px;top:230px;width:1320px",
    '<div class="qk">● QUOTED · ICO NEWS RELEASE, 8 OCT 2026</div><div class="qt">“The fact AI agents act with autonomy is <span class="qh">not an excuse for poor compliance.</span>”</div>' +
    '<div class="qa">RICHARD NEVINSON · DIRECTOR OF TECHNOLOGY REGULATION, ICO</div>');
  tl.fromTo(q, { opacity: 0, y: 60, rotation: 1.5 }, { opacity: 1, y: 0, rotation: 0.5, duration: 0.4, ease: "back.out(1.4)" }, w(478) - 0.1);
  tl.to(q.querySelector(".qh"), { backgroundSize: "100% 80%", duration: 0.6, ease: "power2.inOut" }, w(487));
  tl.to(q, { opacity: 0, duration: 0.15 }, B("v49") - 0.1);
  const d = logo("L1", 1440, 160, 230, 130); pop(d, w(475), B("v49") - 0.1, 0.5); })();

// ---------- v50 - v58: three things you can do ----------
(function () { const t = el("div", "three", "left:440px;top:300px", '<div class="n">1</div><div class="n">2</div><div class="n">3</div>');
  tl.fromTo(t, { opacity: 0 }, { opacity: 1, duration: 0.01 }, w(499) - 0.05);
  t.querySelectorAll(".n").forEach((n, j) => tl.fromTo(n, { opacity: 0, scale: 0.3, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.5)" }, w(499) + j * 0.12));
  tl.to(t, { opacity: 0, duration: 0.15 }, B("v50") - 0.1);
  big("Things you can do", 440, 560, 92, "#ffffff", w(500), B("v50") - 0.1); })();
chip("1 · SWITCH OFF TRAINING ON YOUR CHATS", 1110, 140, "var(--lime)", w(501), B("v51") - 0.1);
phoneCam("v51", w(505), 1.6);
steps("v52", "L3", [["CHATGPT", "Settings", w(511)], ["", "Data controls", w(512)], ["", "Improve the model for everyone", w(514)]], A("v52") + 4.75);
phoneCam("v52", A("v52") + 3.4, 1.3);
steps("v53", "L8", [["CLAUDE", "Settings", w(522)], ["", "Privacy", w(523)], ["", "Help improve our AI models", w(524)]], A("v53") + 4.1);
phoneCam("v53", A("v53") + 3.4, 1.3);
steps("v54", "L6", [["GEMINI", "Keep Activity", w(534)]], w(533), w(533), "TURN THIS OFF");
phoneCam("v54", w(534), 1.25);
(function () { // v55: a chatbot says something about you that's wrong, or private
  chip("2 · ASK FOR IT TO BE REMOVED", 120, 110, "var(--lime)", w(536), B("v55") - 0.1);
  const p = el("div", "panel", "left:360px;top:200px;width:1200px;height:600px");
  const me = el("div", "bubble me", "left:880px;top:250px;width:620px", "What do you know about me?");
  const bot = el("div", "bubble bot", "left:420px;top:390px;width:820px",
    '<span class="bar" style="width:92%"></span><span class="bar" style="width:70%" id="barW"><span class="tag bt" id="tagW">WRONG</span></span><span class="bar" style="width:84%"></span><span class="bar" style="width:58%" id="barP"><span class="tag bt" id="tagP" style="background:#b8860b">PRIVATE</span></span>');
  tl.fromTo(p, { opacity: 0, scale: 0.95 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, A("v55") - 0.05);
  tl.fromTo(me, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, w(537));
  tl.fromTo(bot, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, w(540));
  tl.to("#barW", { backgroundColor: "rgba(224,50,43,0.55)", duration: 0.2 }, w(545)); pop("#tagW", w(545), null, 0.5);
  tl.to("#barP", { backgroundColor: "rgba(184,134,11,0.55)", duration: 0.2 }, w(547)); pop("#tagP", w(547), null, 0.5);
  tl.to([p, me, bot], { opacity: 0, duration: 0.15 }, B("v55") - 0.1); })();
badge("v56", "L2", "OPENAI HELP CENTER");
badge("v57", "L4", "META");
chip("3 · PUBLIC POSTS ARE POSTCARDS", 120, 110, "var(--lime)", w(562), B("v58") - 0.1);

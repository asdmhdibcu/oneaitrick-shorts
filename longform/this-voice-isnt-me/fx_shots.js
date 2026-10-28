// #12 video: what happens on top of each shot. Inlined into index.html by make_index.py (helpers in index_template.tpl).
// Times come from the words (w(k) = start of word k) and the shots (A(id) = cut in, B(id) = cut out).

// ---------- helpers for this episode ----------
const dangerCard = (id, n, title) => { const d = el("div", "danger", "", `<div class="dk">● DANGER</div><div class="dn">${n}<span>/5</span></div><div class="dt">${title}</div>`);
  tl.fromTo(d, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.6)" }, A(id) + 0.05);
  tl.fromTo(d.querySelector(".dn"), { scale: 1.6, transformOrigin: "0% 100%" }, { scale: 1, duration: 0.4, ease: "power4.out" }, A(id) + 0.05);
  tl.to(d, { opacity: 0, duration: 0.15 }, B(id) - 0.12); return d; };
const words = (list, x, y0, gap, fs, tOut) => list.forEach(([k, txt, col], j) => { const c = el("div", "big", `left:${x}px;top:${y0 + j * gap}px;font-size:${fs}px;color:${col || (j % 2 ? "#ffffff" : "var(--lime)")}`, txt);
  tl.fromTo(c, { opacity: 0, x: 60, rotation: j % 2 ? 3 : -3 }, { opacity: 1, x: 0, rotation: j % 2 ? 1.5 : -1.5, duration: 0.25, ease: "back.out(2)" }, w(k));
  tl.to(c, { opacity: 0, duration: 0.15 }, tOut); });
const stamp = (txt, x, y, t, tOut, rot) => { const st = el("div", "stamp", `left:${x}px;top:${y}px;transform:rotate(${rot || -6}deg)`, txt);
  tl.fromTo(st, { opacity: 0, scale: 2.2 }, { opacity: 0.95, scale: 1, duration: 0.18, ease: "power4.out" }, t); tl.to(st, { opacity: 0, duration: 0.15 }, tOut); return st; };
const smallLogo = (code, x, y, t, tOut, label) => { const d = logo(code, x, y, 230, 115, label); pop(d, t, tOut, 0.5); return d; };

// ---------- v01 - v03: the hook ----------
(function () { tl.fromTo("#title", { opacity: 1, y: 0 }, { opacity: 1, y: 0, duration: 0.01 }, 0);
  tl.to("#title", { opacity: 0, y: -20, duration: 0.2 }, B("v01") - 0.15);
  punch("v01", w(6), 0.05); })();
badge("v02", "L1", "ELEVENLABS");
chip("MY VOICE · CLONED WITH AI", 120, 110, "var(--lime)", w(14), B("v02") - 0.1);
big("…with yours.", 120, 620, 130, "var(--lime)", w(36), B("v03") - 0.08);

// ---------- v04 - v07: five dangers in the everyday ----------
(function () { const t = el("div", "three", "left:330px;top:250px", [1, 2, 3, 4, 5].map((n) => `<div class="n" style="width:190px;height:190px;font-size:110px">${n}</div>`).join(""));
  tl.fromTo(t, { opacity: 0 }, { opacity: 1, duration: 0.01 }, w(41) - 0.05);
  t.querySelectorAll(".n").forEach((n, j) => tl.fromTo(n, { opacity: 0, scale: 0.3, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.28, ease: "back.out(2.5)" }, w(41) + j * 0.1));
  tl.to(t, { opacity: 0, duration: 0.15 }, B("v04") - 0.1);
  big("Hidden dangers", 330, 500, 110, "#ffffff", w(42), B("v04") - 0.1);
  chip("IN THE AI YOU USE EVERY DAY", 330, 650, "var(--lime)", w(45), B("v04") - 0.1); })();
chip("THE WEATHER", 120, 760, "#ffffff", w(52), B("v05") - 0.05);
chip("SETTLING AN ARGUMENT", 120, 760, "#ffffff", w(57), B("v06") - 0.05);
chip("FIXING YOUR PHOTOS", 120, 760, "#ffffff", w(63), B("v07") - 0.05);

// ---------- v08 - v11: the stranger in your phone ----------
big("A brilliant stranger", 120, 160, 104, "#ffffff", w(78), B("v08") - 0.1);
chip("WHO'S MOVED INTO YOUR PHONE", 120, 290, "var(--lime)", w(81), B("v08") - 0.1);
chip("SUPER HELPFUL", 1180, 260, "var(--lime)", w(85), B("v09") - 0.1);
chip("NEVER SLEEPS", 1180, 360, "var(--lime)", w(87), B("v09") - 0.1);
chip("KNOWS A BIT ABOUT EVERYTHING", 1180, 460, "var(--lime)", w(89), B("v09") - 0.1);
(function () { const Q = [[101, "1", "Your secrets?"], [108, "2", "Who gets a job?"], [114, "3", "Every photo?"], [123, "4", "Your mum's voice?"]];
  Q.forEach(([k, n, q], j) => { const c = el("div", "qc", `left:${190 + (j % 2) * 790}px;top:${150 + Math.floor(j / 2) * 230}px`, `<div class="qn">WOULD YOU TRUST A STRANGER WITH · ${n}</div><div class="qq">${q}</div>`);
    tl.fromTo(c, { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, w(k) - 0.25);
    tl.to(c, { opacity: 0, duration: 0.15 }, B("v10") - 0.1); });
  const s5 = el("div", "qc slot", "left:585px;top:610px", '<div class="qn">AND · 5</div><div class="qq">The quietest one…</div>');
  tl.fromTo(s5, { opacity: 0, scale: 0.9 }, { opacity: 0.85, scale: 1, duration: 0.3 }, w(123) + 0.6); tl.to(s5, { opacity: 0, duration: 0.15 }, B("v10") - 0.1); })();
chip("ONE FREE TRICK · AT THE END", 120, 760, "var(--lime)", w(136), B("v11") - 0.1);

// ---------- v12 - v25: danger 1, your secrets ----------
dangerCard("v12", "1", "Your secrets");
words([[153, "Health worries"], [155, "Money problems"], [157, "Work documents"]], 1080, 200, 150, 92, B("v13") - 0.1);
badge("v14", "L4", "SAMSUNG");
smallLogo("L3", 1500, 760, w(172), B("v14") - 0.1, "CHATGPT");
chip("A WHOLE MEETING → THE MINUTES", 120, 760, "#ffb547", w(183), B("v15") - 0.1);
badge("v16", "L4", "SAMSUNG");
stamp("BANNED", 1380, 760, w(194), B("v16") - 0.1);
chip("…FOR A WHILE", 1180, 770, "#ffffff", w(203), B("v16") - 0.1);
(function () { // v17: what happens to your chats depends on the company
  const p = el("div", "panel", "left:300px;top:150px;width:1320px;height:640px");
  const me = el("div", "bubble me", "left:960px;top:200px;width:560px", "Here's my bank statement. Can you help?");
  const bot = el("div", "bubble bot", "left:380px;top:360px;width:760px", '<span class="bar" style="width:92%"></span><span class="bar" style="width:74%"></span><span class="bar" style="width:84%"></span>');
  tl.fromTo(p, { opacity: 0, scale: 0.95 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, A("v17") - 0.05);
  tl.fromTo(me, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, A("v17") + 0.3);
  tl.fromTo(bot, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, A("v17") + 0.8);
  chip("IT DEPENDS ON THE COMPANY", 380, 620, "#ffffff", w(213), B("v17") - 0.1);
  chip("SOME: USED FOR TRAINING", 1180, 470, "#ffb547", w(222), B("v17") - 0.1);
  chip("SOME: READ BY STAFF", 1180, 560, "#ffb547", w(230), B("v17") - 0.1);
  tl.to([p, me, bot], { opacity: 0, duration: 0.15 }, B("v17") - 0.1); })();
chip("NOT PROTECTED LIKE A CHAT WITH YOUR DOCTOR", 120, 760, "#ff8a7a", w(239), B("v18") - 0.1);
badge("v19", "L3", "CHATGPT");
chip("MARCH 2023 · A BUG", 120, 110, "#ffb547", w(252), B("v19") - 0.1);
badge("v20", "L3", "CHATGPT");
badge("v21", "L2", "OPENAI");
chip("NAME · EMAIL · LAST 4 CARD DIGITS", 120, 760, "#ff8a7a", w(281), B("v21") - 0.1);
badge("v22", "L2", "OPENAI");
big("Sensitive.", 120, 620, 140, "var(--lime)", w(315), B("v23") - 0.08);
chip("THE POSTCARD RULE", 120, 110, "var(--lime)", w(320), B("v24") - 0.1);
big("Would you write it<br/>on a postcard?", 120, 560, 76, "#ffffff", w(328), B("v24") - 0.1);
chip("SWITCH OFF TRAINING", 1110, 780, "var(--lime)", w(337), B("v25") - 0.1);
steps("v25", "L3", [["CHATGPT", "Settings", w(343)], ["", "Data controls", w(346)], ["", "Improve the model for everyone", w(348)]], A("v25") + 4.75);
phoneCam("v25", A("v25") + 3.4, 1.3);

// ---------- v26 - v38: danger 2, fairness ----------
dangerCard("v26", "2", "Fairness");
chip("COMPUTERS ARE NEUTRAL…?", 120, 760, "#ffffff", w(361), B("v27") - 0.1);
big("AI learns from us.", 120, 620, 120, "var(--lime)", w(365), B("v28") - 0.1);
badge("v29", "L5", "AMAZON");
badge("v30", "L5", "AMAZON");
chip("MOST CAME FROM MEN", 120, 760, "#ffb547", w(409), B("v30") - 0.1);
chip("WHAT IT LEARNED FROM", 120, 760, "#ffffff", w(412), B("v31") - 0.1);
chip("IT TAUGHT ITSELF THIS", 120, 760, "#ff8a7a", w(425), B("v32") - 0.1);
badge("v33", "L5", "AMAZON");
badge("v34", "L5", "AMAZON");
stamp("SCRAPPED", 1160, 640, w(473), B("v34") - 0.1, -5);
chip("A PERSON: YOU CAN SEE IT", 120, 760, "#ffffff", w(497), B("v35") - 0.1);
(function () { // v36: a machine's unfairness looks like maths
  const p = el("div", "panel", "left:420px;top:180px;width:1080px;height:420px");
  const l1 = el("div", "mono", "left:500px;top:250px;font-size:44px", "candidate_score = 0.37");
  const l2 = el("div", "mono", "left:500px;top:330px;font-size:44px;color:#ff8a7a", "threshold       = 0.50");
  const l3 = el("div", "mono", "left:500px;top:430px;font-size:58px;color:#fff", "decision: <span style='color:#ff6b5b'>REJECT</span>");
  tl.fromTo(p, { opacity: 0, scale: 0.95 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, A("v36") - 0.05);
  [l1, l2, l3].forEach((l, j) => tl.fromTo(l, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: E }, A("v36") + 0.15 + j * 0.3));
  chip("ILLUSTRATION · IT LOOKS LIKE MATHS", 420, 640, "var(--lime)", w(507), B("v36") - 0.1);
  tl.to([p, l1, l2, l3], { opacity: 0, duration: 0.15 }, B("v36") - 0.1); })();
chip("HARDER TO SPOT · HARDER TO CHALLENGE", 120, 760, "#ffb547", w(516), B("v37") - 0.1);
words([[529, "Jobs"], [530, "Loans"], [532, "Healthcare"]], 260, 200, 190, 150, B("v37b") - 0.1);
badge("v38", "L10", "ICO GUIDANCE");
chip("IN THE UK · ASK FOR A HUMAN", 120, 110, "var(--lime)", w(553), B("v38") - 0.1);
big("So ask.", 1350, 740, 130, "var(--lime)", w(563), B("v38") - 0.06);

// ---------- v39 - v47: danger 3, your eyes ----------
dangerCard("v39", "3", "Your eyes");
chip("SEEING ≠ BELIEVING", 120, 760, "#ffffff", w(574), B("v40") - 0.1);
chip("MAY 2023 · \"AN EXPLOSION NEAR THE PENTAGON\"", 120, 110, "#ffb547", w(580), B("v41") - 0.1);
stamp("FAKE", 1380, 700, w(600), B("v42") - 0.08, -8);
chip("US STOCKS BRIEFLY DIPPED · AP, 22 MAY 2023", 120, 680, "#ff8a7a", w(606), B("v43") - 0.1);
chip("OFFICIALS: NO EXPLOSION", 120, 780, "var(--lime)", w(615), B("v43") - 0.1);
badge("v44", "L6", "REPUBLICAN NATIONAL COMMITTEE");
big("“Proof”", 120, 600, 170, "#ffffff", w(666), B("v45") - 0.08);
chip("WHAT'S REAL?", 120, 760, "#ffffff", w(674), B("v45b") - 0.1);
chip("ANGRY OR SCARED IN 2 SECONDS?", 120, 760, "#ff8a7a", w(688), B("v46") - 0.1);
big("Slow down.", 120, 600, 130, "var(--lime)", w(698), B("v46") - 0.08);
(function () { const R = [[700, "Who posted it first?"], [704, "Is real news reporting it?"], [711, "Check somewhere you trust"]];
  R.forEach(([k, t], j) => { const r = el("div", "row", `left:300px;top:${200 + j * 150}px`, `<span class="bx"></span>${t}`);
    tl.fromTo(r, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.28, ease: E }, w(k) - 0.1);
    tl.set(r.querySelector(".bx"), { innerHTML: "✓" }, w(k) + 0.5);
    tl.to(r, { opacity: 0, duration: 0.15 }, B("v47") - 0.1); }); })();

// ---------- v48 - v63: danger 4, a voice you trust ----------
dangerCard("v48", "4", "A voice you trust");
chip("REMEMBER MY VOICE?", 120, 760, "var(--lime)", w(727), B("v49") - 0.05);
badge("v50", "L7", "STARLING BANK");
chip("AS LITTLE AS 3 SECONDS OF AUDIO", 120, 110, "var(--lime)", w(744), B("v50") - 0.1);
chip("A BIRTHDAY VIDEO", 1180, 260, "#ffffff", w(749), B("v51") - 0.1);
chip("A VOICE NOTE", 1180, 360, "#ffffff", w(752), B("v51") - 0.1);
chip("A CLIP YOU POSTED", 1180, 460, "#ffffff", w(755), B("v51") - 0.1);
const callScreen = (id, who, tIn, tOut) => { const c = el("div", "call", "", `<div class="cl">INCOMING CALL</div><div class="cn">${who}</div><div class="cs">mobile</div>` +
    `<div class="pulse"></div><div class="av">${who[0]}</div><div class="bt no">✕</div><div class="bt yes">✆</div>`);
  tl.fromTo(c, { opacity: 0, y: 60, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, tIn);
  const pu = c.querySelector(".pulse");
  for (let k = 0; k < Math.max(1, Math.floor((tOut - tIn) / 0.9)); k++) tl.fromTo(pu, { opacity: 0.9, scale: 1 }, { opacity: 0, scale: 1.7, duration: 0.85, ease: "power1.out", immediateRender: false }, tIn + 0.2 + k * 0.9);
  tl.to(c, { opacity: 0, duration: 0.15 }, tOut); return c; };
(function () { const c = callScreen("v52", "Daughter", A("v52") + 0.1, B("v52") - 0.1);
  tl.set(c.querySelector(".cn"), { innerHTML: "Dad" }, w(768)); tl.set(c.querySelector(".av"), { innerHTML: "D" }, w(768)); })();
words([[774, "Accident"], [777, "Arrested"], [779, "Money. Now."]], 1060, 200, 160, 110, B("v53") - 0.1);
badge("v54", "L8", "US FEDERAL TRADE COMMISSION");
chip("THE FAMILY EMERGENCY SCAM", 120, 760, "#ff8a7a", w(795), B("v54") - 0.1);
badge("v55", "L7", "STARLING BANK");
big("28%", 1300, 600, 190, "var(--lime)", w(811), B("v55") - 0.08);
chip("OF UK ADULTS TARGETED IN A YEAR", 1180, 790, "#ffffff", w(814), B("v55") - 0.1);
chip("HONG KONG · 2024", 120, 760, "#ffffff", w(838), B("v56") - 0.1);
chip("A VIDEO CALL WITH HIS CFO", 120, 760, "#ffffff", w(842), B("v57") - 0.1);
stamp("ALL FAKE", 1300, 790, w(882), B("v59") - 0.06, -6);
chip("ALL DEEPFAKES", 120, 760, "#ff8a7a", w(884), B("v60") - 0.05);
badge("v61", "L9", "ARUP");
chip("FROM MY YEARS IN BANKING", 120, 760, "#ffffff", w(898), B("v62") - 0.1);
big("Someone you love.", 120, 620, 120, "var(--lime)", w(919), B("v63") - 0.08);

// ---------- v64 - v71: danger 5, your judgment ----------
dangerCard("v64", "5", "Your judgment");
(function () { const d = el("div", "def", "", '<div class="dk">THERE\'S A NAME FOR IT</div><div class="dw">Automation bias</div><div class="dd">Trusting the machine over your own judgment</div>');
  tl.fromTo(d, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.5)" }, w(947) - 0.1); tl.to(d, { opacity: 0, duration: 0.15 }, B("v65") - 0.1); })();
(function () { // v66: confident and wrong
  const p = el("div", "panel", "left:300px;top:150px;width:1320px;height:640px");
  const me = el("div", "bubble me", "left:1060px;top:200px;width:460px", "Is that definitely right?");
  const bot = el("div", "bubble bot", "left:380px;top:340px;width:820px", 'Absolutely. Here are the facts, with sources: <span class="bar" style="width:90%"></span><span class="bar" style="width:76%"></span>');
  tl.fromTo(p, { opacity: 0, scale: 0.95 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, A("v66") - 0.05);
  tl.fromTo(me, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, A("v66") + 0.25);
  tl.fromTo(bot, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, w(959));
  chip("CONFIDENT · POLISHED", 380, 620, "var(--lime)", w(960), B("v66") - 0.1);
  stamp("WRONG", 1160, 560, w(966), B("v66") - 0.08, -7);
  tl.to([p, me, bot], { opacity: 0, duration: 0.15 }, B("v66") - 0.1); })();
chip("ENGLAND'S HIGH COURT · JUNE 2025", 120, 760, "#ffffff", w(971), B("v67") - 0.1);
(function () { // v68: 45 cases cited, 18 didn't exist (Al-Haroun)
  const cs = []; const BAD = new Set([1, 4, 6, 9, 12, 15, 17, 20, 23, 25, 28, 31, 33, 36, 38, 40, 42, 44]);
  for (let j = 0; j < 45; j++) { const c = el("div", "case", `left:${300 + (j % 9) * 110}px;top:${170 + Math.floor(j / 9) * 82}px`, "CASE"); cs.push(c);
    tl.fromTo(c, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.18, ease: "back.out(2)" }, w(998) + j * 0.025); }
  cs.forEach((c, j) => { if (BAD.has(j)) { tl.set(c, { className: "case bad", innerHTML: "✕" }, w(1001) + 0.03 * j); } });
  big("45 cited", 1340, 220, 96, "#ffffff", w(998), B("v68") - 0.1);
  big("18 didn't exist", 1340, 360, 66, "#ff6b5b", w(1001) + 0.2, B("v68") - 0.1);
  tl.to(cs, { opacity: 0, duration: 0.15 }, B("v68") - 0.1); })();
(function () { // v69: the judges' words (the judgment page itself was unreachable; the words are checked against the official text)
  const q = el("div", "quote", "left:220px;top:170px;width:1480px",
    '<div class="qk">● QUOTED · HIGH COURT JUDGMENT, 6 JUNE 2025 · [2025] EWHC 1383 (Admin)</div><div class="qt" style="font-size:62px">“There are <span class="qh">serious implications for the administration of justice</span> and public confidence in the justice system…”</div>' +
    '<div class="qa">DAME VICTORIA SHARP · PRESIDENT OF THE KING\'S BENCH DIVISION</div>');
  tl.fromTo(q, { opacity: 0, y: 60, rotation: 1.2 }, { opacity: 1, y: 0, rotation: 0.4, duration: 0.4, ease: "back.out(1.4)" }, A("v69") - 0.05);
  tl.to(q.querySelector(".qh"), { backgroundSize: "100% 80%", duration: 0.7, ease: "power2.inOut" }, w(1010));
  tl.to(q, { opacity: 0, duration: 0.15 }, B("v69") - 0.1); })();
chip("TRAINED PROFESSIONALS", 120, 760, "#ffffff", w(1019), B("v70") - 0.1);
(function () { // v71: judgment makes the other four worse
  const R = [[1040, "1", "We overshare"], [1044, "2", "Accept unfair answers"], [1049, "3", "Believe the fake photo"], [1059, "4", "Trust the voice"]];
  const top = el("div", "tile on", "left:810px;top:120px", '<div class="tn">5</div><div class="tt">Stop checking</div>');
  tl.fromTo(top, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, w(1035));
  R.forEach(([k, n, t], j) => { const c = el("div", "tile", `left:${150 + j * 420}px;top:430px;width:360px`, `<div class="tn">${n}</div><div class="tt">${t}</div>`);
    tl.fromTo(c, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, w(k) - 0.15);
    tl.set(c, { className: "tile on" }, w(k) + 0.1); tl.to(c, { opacity: 0, duration: 0.15 }, B("v71") - 0.1); });
  tl.to(top, { opacity: 0, duration: 0.15 }, B("v71") - 0.1); })();

// ---------- v72 - v82: four habits ----------
(function () { const t = el("div", "three", "left:440px;top:280px", [1, 2, 3, 4].map((n) => `<div class="n">${n}</div>`).join(""));
  tl.fromTo(t, { opacity: 0 }, { opacity: 1, duration: 0.01 }, w(1076) - 0.05);
  t.querySelectorAll(".n").forEach((n, j) => tl.fromTo(n, { opacity: 0, scale: 0.3, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.5)" }, w(1076) + j * 0.12));
  tl.to(t, { opacity: 0, duration: 0.15 }, B("v72") - 0.1);
  big("Four habits", 440, 540, 104, "#ffffff", w(1077), B("v72") - 0.1);
  chip("NO NEED TO THROW YOUR PHONE IN THE SEA", 440, 110, "#ffffff", w(1066), w(1076) - 0.1); })();
chip("1 · THE POSTCARD RULE", 120, 110, "var(--lime)", w(1079), B("v73") - 0.1);
chip("2 · QUESTION IT", 1110, 780, "var(--lime)", w(1101), B("v74") - 0.1);
steps("v74", "L3", [["", "Ask for its sources", w(1108)], ["", "Open one", w(1114)], ["", "Check it yourself", w(1117)]], null, A("v74") + 3.35);
phoneCam("v74", null);
chip("3 · A FAMILY SAFE PHRASE", 120, 110, "var(--lime)", w(1135), B("v75") - 0.1);
big("Tonight.", 120, 620, 140, "var(--lime)", w(1142), B("v75") - 0.08);
(function () { // v76: the safe-phrase card. MARMALADE is the hidden word: it is never said out loud.
  const n = el("div", "note", "", '<div class="nk">OUR FAMILY SAFE PHRASE</div><div class="nw">Marmalade</div><div class="ns">An example. Pick your own and never post it.</div>');
  tl.fromTo(n, { opacity: 0, y: 50, rotation: -5 }, { opacity: 1, y: 0, rotation: -2, duration: 0.4, ease: "back.out(1.6)" }, w(1144) - 0.1);
  tl.to(n, { opacity: 0, duration: 0.15 }, B("v76") - 0.1);
  chip("✓ SAY IT FACE TO FACE", 160, 240, "var(--lime)", w(1152), B("v76") - 0.1);
  chip("✕ NEVER TEXT IT", 160, 340, "#ff8a7a", w(1157), B("v76") - 0.1);
  chip("✕ NEVER POST IT", 160, 440, "#ff8a7a", w(1160), B("v76") - 0.1); })();
(function () { // v77: Mum calls in a panic
  const c = callScreen("v77", "Mum", w(1164) - 0.2, B("v77") - 0.1);
  chip("ASK FOR THE PHRASE", 1300, 240, "var(--lime)", w(1173), B("v77") - 0.1);
  chip("NO PHRASE?", 1300, 340, "#ff8a7a", w(1177), B("v77") - 0.1);
  chip("HANG UP", 1300, 440, "#ff6b5b", w(1179), B("v77") - 0.1);
  chip("CALL BACK ON THE NUMBER YOU HAVE", 1060, 540, "var(--lime)", w(1182), B("v77") - 0.1);
  tl.to(c.querySelector(".no"), { scale: 1.3, boxShadow: "0 0 50px rgba(224,50,43,0.9)", duration: 0.2, yoyo: true, repeat: 1 }, w(1179)); })();
chip("4 · CO-PILOT, NOT AUTOPILOT", 120, 110, "var(--lime)", w(1193), B("v78") - 0.1);
chip("DRAFT", 120, 560, "#ffffff", w(1203), B("v79") - 0.1);
chip("BRAINSTORM", 120, 660, "#ffffff", w(1204), B("v79") - 0.1);
chip("EXPLAIN", 120, 760, "#ffffff", w(1205), B("v79") - 0.1);
big("The final call<br/>is yours.", 1000, 520, 96, "var(--lime)", w(1206), B("v79") - 0.08);
chip("IN YOUR OWN WORDS", 120, 760, "var(--lime)", w(1218), B("v79b") - 0.1);
chip("BRILLIANT COMPANY", 120, 760, "var(--lime)", w(1242), B("v80") - 0.1);
big("Don't hand him<br/>the keys.", 120, 520, 104, "var(--lime)", w(1245), B("v81") - 0.05);
(function () { // v82: the hidden word
  big("One word I never<br/>said out loud.", 160, 220, 96, "#ffffff", w(1250), B("v82") - 0.1);
  const cb = el("div", "row", "left:160px;top:520px;font-size:44px;font-weight:700;color:#9aa0b4", '<span class="bx" style="border-color:#9aa0b4;color:#9aa0b4">?</span>Add a comment…');
  tl.fromTo(cb, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, w(1261)); tl.to(cb, { opacity: 0, duration: 0.15 }, B("v82") - 0.1);
  big("Comment it.", 160, 680, 120, "var(--lime)", w(1263), B("v82") - 0.06); })();

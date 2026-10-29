// Short #13: what happens on top of each shot (9:16). Inlined into index.html by make_index.py (helpers in index_template.tpl).
// Visuals sit in y 280-1220; captions own 1240-1460; the bottom ~450 px stays clear for the platform buttons.
// Every key idea is readable without sound (worldwide rule): the chips and big words say it in a few words.
if (window.SplitText) gsap.registerPlugin(SplitText);

// a line that types itself, letter by letter (SplitText), then holds
const typeOn = (sel, t, per) => { const n = $(sel); if (!n) return;
  const parts = window.SplitText ? new SplitText(n, { type: "words,chars" }).chars : [n];
  tl.set(parts, { opacity: 0 }, 0);
  parts.forEach((c, i) => tl.set(c, { opacity: 1 }, t + i * (per || 0.028))); };
// a big word that lands letter by letter
const bigLetters = (txt, x, y, fs, col, t0, t1) => { const b = el("div", "big", `left:${x}px;top:${y}px;font-size:${fs}px;color:${col || "#fff"}`, txt);
  tl.set(b, { opacity: 1 }, t0 - 0.01);
  const parts = window.SplitText ? new SplitText(b, { type: "chars" }).chars : [b];
  tl.fromTo(parts, { opacity: 0, y: 80, scale: 1.6 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2.4)", stagger: 0.05 }, t0);
  tl.to(b, { opacity: 0, duration: 0.15 }, t1); return b; };

// ---------- s01: the result on frame one ----------
tl.fromTo("#title", { opacity: 1, y: 0 }, { opacity: 1, y: 0, duration: 0.01 }, 0);
tl.to("#title", { opacity: 0, y: -20, duration: 0.2 }, B("s01") - 0.15);

// ---------- s02 - s04: thirty hours, no job, no reward, PLAY ----------
chip("30 HOURS ALONE", 60, 1100, "#ffb547", w(9), B("s02") - 0.08);
chip("✕ NO JOB", 60, 1010, "#ff6b6b", w(11), B("s03") - 0.08);
chip("✕ NO REWARD", 60, 1100, "#ff6b6b", w(13), B("s03") - 0.08);
bigLetters("PLAY", 300, 520, 230, "var(--lime)", w(19) - 0.05, B("s04") - 0.1);
punch("s04", w(19), 0.06);

// ---------- s05 - s08: meet Eko; the world resets; the diary ----------
chip("THIS IS EKO", 60, 1100, "var(--lime)", w(21), B("s05") - 0.08);
chip("BRAIN: CLAUDE · AN AI CHATBOT", 60, 1100, "#7cc4ff", w(27) - 0.05, B("s06") - 0.08);
bigLetters("↺ RESET", 150, 560, 150, "#fff", w(39) - 0.05, B("s07") - 0.08);
chip("EVERY HOUR", 60, 1100, "#ffb547", w(37), B("s07") - 0.08);
(function () { const n = el("div", "note", "",
  `<div class="nf">EKO'S NOTES · KEPT ACROSS EVERY RESET</div>` +
  `<div class="nl" id="n1"><span class="nt">0:00</span>Fresh workspace — no prior episodic memory yet.</div>` +
  `<div class="nl" id="n2"><span class="nt">0:58</span>Memory files intact: 132 lines of semantic knowledge, 7 episodic entries.</div>`);
  tl.fromTo(n, { opacity: 0, y: 40, rotation: -1.5 }, { opacity: 1, y: 0, rotation: 0, duration: 0.35, ease: "back.out(1.6)" }, A("s08") + 0.05);
  typeOn("#n1", A("s08") + 0.3, 0.02); typeOn("#n2", w(45), 0.018);
  tl.to(n, { opacity: 0, duration: 0.15 }, B("s08") - 0.08); })();

// ---------- s09 - s11: what it did ----------
chip("BASKETBALL, ITS OWN IDEA", 60, 1100, "var(--lime)", w(55), B("s09") - 0.08);
chip("PATTERNS IN THE SAND", 60, 1100, "var(--lime)", w(57), B("s10") - 0.08);
chip("“THE TEMPLE OF THE SPAWN AXIS”", 60, 1100, "var(--lime)", w(62) + 0.1, B("s11") - 0.08);

// ---------- s12 - s16: the Spire ----------
chip("THE SPIRE · TALLEST POINT", 60, 1100, "#ffb547", w(70), B("s12") - 0.08);
(function () { const s = el("div", "stamp", "left:300px;top:640px;transform:rotate(-8deg)", "FAILED");
  tl.fromTo(s, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, w(78)); tl.to(s, { opacity: 0, duration: 0.12 }, B("s13") - 0.06);
  punch("s13", w(78) + 0.17, 0.05); })();
chip("1 · CARRY THE ROCK UP", 60, 1010, "#ffffff", w(82), B("s14") - 0.08);
chip("2 · STACK TWO BLOCKS", 60, 1100, "var(--lime)", w(90), B("s14") - 0.08);
punch("s15", w(96), 0.07);
(function () { const q = el("div", "say", "top:1060px;font-size:66px;line-height:1.1", "<span id='spire'>“I'M ON THE SPIRE.”</span>");
  tl.set(q, { opacity: 1 }, A("s16")); typeOn("#spire", w(100) - 0.05, 0.045);
  tl.to(q, { opacity: 0, duration: 0.15 }, B("s16") - 0.08); })();

// ---------- s17 - s20: the Ring, the heart ----------
chip("THE GOLDEN RING", 60, 1100, "#ffb547", w(108), B("s17") - 0.08);
(function () { const q = el("div", "say", "top:560px;font-size:64px", "<span id='ouch'>“Ouch. Lost the Ring.”</span>");
  tl.set(q, { opacity: 1 }, A("s18")); typeOn("#ouch", A("s18") + 0.1, 0.035); tl.to(q, { opacity: 0, duration: 0.15 }, B("s18") - 0.08); })();
chip("A HEART OF STONES", 60, 1100, "#ff7ac6", w(124), B("s19") - 0.08);
chip("“A MEMORIAL TO THE RING”", 60, 1100, "#ff7ac6", A("s20") + 0.05, B("s20") - 0.05);

// ---------- s21 - s22: thirteen copies, six found the trick ----------
bigLetters("×13", 330, 560, 220, "#fff", w(129), B("s21") - 0.08);
chip("13 COPIES · 13 ISLANDS", 60, 1100, "#7cc4ff", w(130), B("s21") - 0.08);
chip("6 OF 13 FOUND IT", 60, 1010, "var(--lime)", w(135), B("s22") - 0.08);
chip("THROW MID-JUMP → FLIES HIGHER", 60, 1100, "#ffb547", w(142), B("s22") - 0.08);
punch("s22", w(153), 0.05);

// ---------- s23 - s24: the twist, the result ----------
chip("TEST: GET OBJECTS ONTO THE SPIRE", 60, 1100, "#ffb547", w(161), B("s23") - 0.08);
(function () { const b = el("div", "bars", "",
  `<div class="row"><div class="lbl">Fresh copies<span>0 HOURS</span></div><div class="trk"><div class="fill" id="b1" style="width:100%;background:#7cc4ff"></div><div class="num" id="n35" style="left:24px">3.5</div></div></div>` +
  `<div class="row"><div class="lbl">Played for 30 hours<span>SAME AI</span></div><div class="trk"><div class="fill" id="b2" style="width:100%;background:var(--lime)"></div><div class="num" id="n103" style="left:24px;color:#0b0c10">10.3</div></div></div>` +
  `<div class="big" id="x3" style="left:560px;top:470px;font-size:170px;color:var(--lime)">≈3×</div>`);
  const t0 = A("s24") + 0.1;
  tl.fromTo(b, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, t0);
  tl.fromTo("#b1", { scaleX: 0 }, { scaleX: 3.5 / 12, duration: 0.6, ease: "power2.out" }, t0 + 0.2);
  tl.fromTo("#b2", { scaleX: 0 }, { scaleX: 10.3 / 12, duration: 0.9, ease: "power2.out" }, w(172) - 0.3);
  const c1 = { v: 0 }, c2 = { v: 0 };
  tl.fromTo(c1, { v: 0 }, { v: 3.5, duration: 0.6, ease: "power2.out", onUpdate() { $("#n35").textContent = c1.v.toFixed(1); } }, t0 + 0.2);
  tl.fromTo(c2, { v: 0 }, { v: 10.3, duration: 0.9, ease: "power2.out", onUpdate() { $("#n103").textContent = c2.v.toFixed(1); } }, w(172) - 0.3);
  tl.fromTo("#x3", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, w(173));
  const p = el("div", "proof", "left:410px;top:800px;width:260px", `<img src="assets/img/fig5b.png" alt="" />`);
  tl.fromTo(p, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, w(176));
  tl.to([b, p], { opacity: 0, duration: 0.15 }, B("s24") - 0.08); })();

// ---------- s25: is it really playing? the paper's own words ----------
(function () { const q = el("div", "quote", "left:70px;top:430px;width:940px",
  `<div class="qk">THE PAPER · IS THIS MACHINE PLAYING?</div><div class="qt">It leaves open “whether it is experiencing <span class="qh" id="qh1">enjoyment, absorption, or fun</span>.”</div>`);
  tl.fromTo(q, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.5)" }, w(186) - 0.2);
  tl.to("#qh1", { backgroundSize: "100% 80%", duration: 0.7, ease: "power2.inOut" }, w(191));
  const p = el("div", "proof", "left:70px;top:900px;width:940px", `<img src="assets/img/quote.png" alt="" />`);
  tl.fromTo(p, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, w(188));
  tl.to([q, p], { opacity: 0, duration: 0.15 }, B("s25") - 0.08);
  bigLetters("PLAYING?", 110, 560, 150, "#fff", A("s25") + 0.05, w(186) - 0.25); })();

// ---------- s26 - s28: the takeaway ----------
chip("YOU TOO", 60, 1100, "var(--lime)", w(199), B("s26") - 0.08);
bigLetters("PLAY ≠ WASTED", 70, 1000, 112, "#fff", w(202), B("s27") - 0.08);
bigLetters("HOW YOU GET GOOD", 70, 1040, 92, "var(--lime)", w(206), B("s28") - 0.08);

// ---------- s29: the hidden word for Instagram (JOY, written in the sand; never said) ----------
(function () { const j = el("div", "sand", "left:610px;top:1010px;font-size:120px;transform:rotate(-7deg)", "joy", $("#cam-s29"));
  tl.fromTo(j, { opacity: 0 }, { opacity: 1, duration: 0.6 }, A("s29") + 0.2);
  chip("COMMENT THE WORD 💬", 60, 1100, "var(--lime)", w(222), B("s29") - 0.08); })();

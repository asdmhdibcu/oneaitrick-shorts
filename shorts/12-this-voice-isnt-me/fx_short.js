// Short #12: what happens on top of each shot (9:16). Inlined by make_index.py (helpers in index_template.tpl).
// Visuals sit in y 280-1220; captions own 1240-1460; the bottom ~450 px stays clear for the platform buttons.
// Word indices are the main cut's; the Trial Reel (its first shot is t01) runs 20 words shorter at the start.
const TRIAL = SH[0].id === "t01";
const S0 = TRIAL ? -20 : 0;
const wk = (k) => w(k + S0);
const stamp = (txt, x, y, t, tOut, rot) => { const st = el("div", "stamp", `left:${x}px;top:${y}px;transform:rotate(${rot || -6}deg)`, txt);
  tl.fromTo(st, { opacity: 0, scale: 2.2 }, { opacity: 0.95, scale: 1, duration: 0.18, ease: "power4.out" }, t); tl.to(st, { opacity: 0, duration: 0.15 }, tOut); return st; };
const callScreen = (who, tIn, tOut) => { const c = el("div", "call", "", `<div class="cl">INCOMING CALL</div><div class="cn">${who}</div><div class="cs">mobile</div>` +
    `<div class="pulse"></div><div class="av">${who[0]}</div><div class="bt no">✕</div><div class="bt yes">✆</div>`);
  tl.fromTo(c, { opacity: 0, y: 60, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, tIn);
  const pu = c.querySelector(".pulse");
  for (let k = 0; k < Math.max(1, Math.floor((tOut - tIn) / 0.9)); k++) tl.fromTo(pu, { opacity: 0.9, scale: 1 }, { opacity: 0, scale: 1.7, duration: 0.85, ease: "power1.out", immediateRender: false }, tIn + 0.2 + k * 0.9);
  tl.to(c, { opacity: 0, duration: 0.15 }, tOut); return c; };

// ---------- the opening ----------
if (!TRIAL) {
  tl.fromTo("#title", { opacity: 1, y: 0 }, { opacity: 1, y: 0, duration: 0.01 }, 0);
  tl.fromTo("#tshade", { opacity: 1 }, { opacity: 1, duration: 0.01 }, 0);
  tl.to("#title", { opacity: 0, y: -20, duration: 0.2 }, B("k01") - 0.15);
  tl.to("#tshade", { opacity: 0, duration: 0.3 }, B("k01") - 0.15);
  punch("k01", w(6), 0.05);
  badge("k02", "L1", "ELEVENLABS");
  chip("MY VOICE · CLONED WITH AI", 60, 1110, "var(--lime)", w(14), B("k02") - 0.1);
  big("…and yours.", 60, 900, 120, "var(--lime)", w(37) - 0.05, B("k03") - 0.08);
} else {   // t01: "If your mum called you right now... would you know it was really her?"
  tl.set("#title", { opacity: 0 }, 0);
  const c = callScreen("Mum", 0.05, B("t01") - 0.1);
  chip("WOULD YOU KNOW IT WASN'T HER?", 60, 1110, "var(--lime)", w(11), B("t01") - 0.1);
}

// ---------- three seconds of audio ----------
badge("k04", "L7", "STARLING BANK");
big("3 seconds.", 60, 880, 170, "var(--lime)", wk(50), B("k04") - 0.08);
chip("OF AUDIO. THAT'S ALL A SCAMMER NEEDS.", 60, 1110, "#ffffff", wk(53), B("k04") - 0.1);
chip("A BIRTHDAY VIDEO", 60, 700, "#ffffff", wk(55), B("k05") - 0.1);
chip("A VOICE NOTE", 60, 800, "#ffffff", wk(58), B("k05") - 0.1);
chip("A CLIP YOU POSTED", 60, 900, "#ffffff", wk(61), B("k05") - 0.1);
(function () { const c = callScreen("Daughter", A("k06") - 0.12, B("k06") - 0.1);
  tl.set(c.querySelector(".cn"), { innerHTML: "Dad" }, wk(75) - 0.05); tl.set(c.querySelector(".av"), { innerHTML: "D" }, wk(75) - 0.05); })();
[[80, "Accident", 420], [83, "Arrested", 600], [86, "Money. Now.", 780]].forEach(([k, t, y], j) => {
  const b = el("div", "big", `left:60px;top:${y}px;font-size:130px;color:${j % 2 ? "#ffffff" : "var(--lime)"}`, t);
  tl.fromTo(b, { opacity: 0, x: 60, rotation: j % 2 ? 2 : -2 }, { opacity: 1, x: 0, rotation: j % 2 ? 1 : -1, duration: 0.25, ease: "back.out(2)" }, wk(k));
  tl.to(b, { opacity: 0, duration: 0.15 }, B("k07") - 0.1); });

// ---------- Hong Kong: every face was fake ----------
chip("HONG KONG · 2024", 60, 1110, "#ffffff", wk(99), B("k08") - 0.1);
chip("A VIDEO CALL WITH HIS CFO", 60, 1110, "#ffffff", wk(103), B("k09") - 0.1);
stamp("ALL FAKE", 560, 1060, wk(143), B("k11") - 0.06, -6);
chip("ALL DEEPFAKES", 60, 1110, "#ff8a7a", wk(145), B("k12") - 0.05);

// ---------- the fix: a family safe phrase ----------
chip("THE FIX · A FAMILY SAFE PHRASE", 60, 330, "var(--lime)", A("k13") + 0.1, B("k13") - 0.1);
big("Tonight.", 60, 900, 150, "var(--lime)", wk(154), B("k13") - 0.08);
(function () { // the safe-phrase card. MARMALADE is the hidden word: it is never said out loud.
  const n = el("div", "note", "", '<div class="nk">OUR FAMILY SAFE PHRASE</div><div class="nw">Marmalade</div><div class="ns">An example. Pick your own and never post it.</div>');
  tl.fromTo(n, { opacity: 0, y: 50, rotation: -5 }, { opacity: 1, y: 0, rotation: -2, duration: 0.4, ease: "back.out(1.6)" }, A("k14") + 0.05);
  tl.to(n, { opacity: 0, duration: 0.15 }, B("k14") - 0.1);
  chip("✓ SAY IT FACE TO FACE", 120, 860, "var(--lime)", wk(164), B("k14") - 0.1);
  chip("✕ NEVER TEXT IT", 120, 960, "#ff8a7a", wk(169), B("k14") - 0.1);
  chip("✕ NEVER POST IT", 120, 1060, "#ff8a7a", wk(172), B("k14") - 0.1); })();
(function () { // "Mum" calls in a panic
  const c = callScreen("Mum", A("k15") + 0.05, B("k15") - 0.1);
  chip("ASK FOR THE PHRASE", 60, 1110, "var(--lime)", wk(185), wk(189) - 0.22);
  chip("NO PHRASE? HANG UP.", 60, 1110, "#ff6b5b", wk(189), wk(193) - 0.22);
  chip("CALL BACK ON THE NUMBER YOU HAVE", 60, 1110, "var(--lime)", wk(193), B("k15") - 0.1);
  tl.to(c.querySelector(".no"), { scale: 1.3, boxShadow: "0 0 50px rgba(224,50,43,0.9)", duration: 0.2, yoyo: true, repeat: 1 }, wk(191)); })();

// ---------- the hidden word ----------
(function () { big("One word I never<br/>said out loud.", 60, 380, 92, "#ffffff", wk(203), B("k16") - 0.1);
  const cb = el("div", "row", "left:60px;top:700px;font-size:44px;font-weight:700;color:#9aa0b4", '<span class="bx" style="border-color:#9aa0b4;color:#9aa0b4">?</span>Add a comment…');
  tl.fromTo(cb, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, wk(214)); tl.to(cb, { opacity: 0, duration: 0.15 }, B("k16") - 0.1);
  big("Comment it.", 60, 900, 140, "var(--lime)", wk(216), B("k16") - 0.06); })();

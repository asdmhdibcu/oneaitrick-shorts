<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <script src="captions.js"></script>
    <link rel="stylesheet" href="assets/base.css" />
    <style>
      /* ---------- the board (one stage for the whole short) ---------- */
      #world { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }
      #drift { position: absolute; inset: 0; transform-origin: 540px 780px; }
      .gridbg { position: absolute; left: -400px; top: -400px; width: 1880px; height: 2720px; background-color: #0b0c10;
        background-image: linear-gradient(rgba(124,196,255,0.07) 2px, transparent 2px), linear-gradient(90deg, rgba(124,196,255,0.07) 2px, transparent 2px),
          linear-gradient(rgba(124,196,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(124,196,255,0.03) 1px, transparent 1px);
        background-size: 120px 120px, 120px 120px, 30px 30px, 30px 30px; background-position: 400px 400px; }
      .boardglow { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
        background: radial-gradient(ellipse 60% 40% at 50% 41%, rgba(124,196,255,0.10), rgba(4,5,10,0) 70%), radial-gradient(ellipse 90% 70% at 50% 45%, rgba(4,5,10,0) 50%, rgba(4,5,10,0.8) 100%); }

      /* the phone: designed at 1000 x 2140, shown at 0.4 on the board, 1.0 when the camera pushes in */
      #phone { position: absolute; left: 340px; top: 352px; width: 1000px; height: 2140px; transform-origin: 0 0; }
      #phone .frame { position: absolute; inset: -26px; border-radius: 160px; background: linear-gradient(145deg, #2a2f3b, #12141a 40%, #22262f);
        box-shadow: 0 80px 160px rgba(0,0,0,0.75), 0 0 0 3px rgba(255,255,255,0.10), inset 0 0 0 3px rgba(255,255,255,0.06); }
      #screen { position: absolute; inset: 0; border-radius: 134px; overflow: hidden; background: #07080c; }
      #notch { position: absolute; left: 380px; top: 26px; width: 240px; height: 66px; border-radius: 40px; background: #000; z-index: 60; }
      #sbar { position: absolute; left: 0; top: 0; width: 1000px; height: 120px; z-index: 59; color: #fff; }
      #sbar .tm { position: absolute; left: 110px; top: 38px; font-weight: 700; font-size: 44px; letter-spacing: -0.01em; }
      #sbar .ic { position: absolute; right: 100px; top: 46px; display: flex; gap: 14px; align-items: flex-end; }
      #sbar .sig i { display: inline-block; width: 9px; margin-right: 4px; background: #fff; border-radius: 2px; }
      #sbar .bat { width: 62px; height: 30px; border: 3px solid rgba(255,255,255,0.8); border-radius: 9px; padding: 3px; }
      #sbar .bat b { display: block; width: 70%; height: 100%; background: #fff; border-radius: 4px; }
      #phone .glare { position: absolute; inset: 0; border-radius: 134px; z-index: 58; pointer-events: none;
        background: linear-gradient(125deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0) 32%); }
      .scr { position: absolute; left: 0; top: 0; width: 1000px; height: 2140px; opacity: 0; overflow: hidden; }
      .scr .bg { position: absolute; inset: 0; }
      .h { opacity: 0; }
      .abs { position: absolute; }
      .ctr { position: absolute; left: 0; width: 1000px; text-align: center; }
      .mono { font-family: "Mono", monospace; font-weight: 700; letter-spacing: 0.08em; }
      .btnc { position: absolute; width: 200px; height: 200px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
      .btnc svg { width: 96px; height: 96px; }
      .bub { position: absolute; padding: 34px 44px; border-radius: 48px; font-size: 64px; font-weight: 650; line-height: 1.2; white-space: nowrap; }
      .bub.l { background: #2c2f38; color: #fff; border-bottom-left-radius: 14px; }
      .bub.r { background: #2a6df4; color: #fff; border-bottom-right-radius: 14px; }
      .pill { position: absolute; padding: 18px 34px; border-radius: 999px; font-family: "Mono", monospace; font-weight: 700; font-size: 40px;
        letter-spacing: 0.08em; white-space: nowrap; }
      .stampx { position: absolute; font-weight: 900; font-size: 92px; letter-spacing: 0.01em; padding: 8px 36px; border: 12px solid currentColor; border-radius: 26px;
        color: #ff4d4d; white-space: nowrap; background: rgba(10,0,0,0.25); }
      .pagecard { position: absolute; left: 40px; width: 920px; border-radius: 26px; background: #f8f6f1; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,0.55); }
      .pagecard img { position: absolute; left: 0; top: 0; }
      .pagecard .hl { position: absolute; mix-blend-mode: multiply; border-radius: 8px; transform-origin: 0 50%; background: rgba(200,255,77,0.9); }
      .pagecard .need { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px;
        background: repeating-linear-gradient(135deg, #f3efe4 0 28px, #ebe5d6 28px 56px); color: #b4532a; font-family: "Mono", monospace; font-weight: 700;
        font-size: 34px; letter-spacing: 0.08em; text-align: center; }
      .pagecard .need b { font-size: 26px; color: #6b6e78; letter-spacing: 0.04em; font-weight: 500; max-width: 760px; }
      .pagecard .sl { position: absolute; left: 0; right: 0; bottom: 0; padding: 12px 26px; font-family: "Mono", monospace; font-weight: 700; font-size: 26px;
        letter-spacing: 0.1em; color: #4a4d57; background: rgba(240,238,232,0.97); border-top: 2px solid #e2dfd6; text-transform: uppercase; }
      .logot { position: absolute; display: flex; align-items: center; justify-content: center; gap: 22px; border-radius: 30px; background: #fff;
        box-shadow: 0 24px 60px rgba(0,0,0,0.5); font-weight: 800; color: #111; }
      .logot svg, .logot img { height: 64%; width: auto; }
      .logot.need { background: rgba(10,12,18,0.85); border: 4px dashed #ff8a7a; color: #ff8a7a; font-family: "Mono", monospace; font-size: 26px; letter-spacing: 0.08em; }

      /* pins: one fact each, parked beside the phone for the rest of the short */
      .pin { position: absolute; width: 280px; height: 200px; border-radius: 22px; background: rgba(20,22,29,0.94); border: 2px solid rgba(255,255,255,0.12);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5); opacity: 0; transform-origin: 50% 50%; overflow: visible; }
      .pin .no { position: absolute; left: 18px; top: 14px; font-family: "Mono", monospace; font-weight: 700; font-size: 17px; letter-spacing: 0.1em; color: #a3a8b6; }
      .pin .bg { position: absolute; left: 18px; top: 40px; font-weight: 900; font-size: 64px; letter-spacing: -0.04em; line-height: 1; color: var(--lime); white-space: nowrap; }
      .pin .lb { position: absolute; left: 18px; right: 14px; top: 112px; font-weight: 700; font-size: 22px; line-height: 1.15; color: #e8e9ee; }
      .pin .sr { position: absolute; left: 18px; bottom: 12px; font-family: "Mono", monospace; font-weight: 700; font-size: 14px; letter-spacing: 0.09em; color: #a3a8b6; white-space: nowrap; }
      .pin .glow { position: absolute; inset: -4px; border-radius: 24px; border: 4px solid var(--lime); box-shadow: 0 0 34px rgba(200,255,77,0.55); opacity: 0; }
      .pin .stp { position: absolute; right: -12px; top: -18px; padding: 6px 12px; border: 4px solid #ffb547; border-radius: 10px; color: #ffb547; background: rgba(20,14,4,0.92);
        font-family: "Mono", monospace; font-weight: 700; font-size: 17px; letter-spacing: 0.06em; opacity: 0; white-space: nowrap; }
      .pin.q { border: 3px dashed rgba(200,255,77,0.7); }

      /* the hook card on frame one */
      #hook { position: absolute; left: 70px; top: 372px; width: 940px; height: 830px; border-radius: 34px; background: rgba(12,14,20,0.94);
        border: 2px solid rgba(255,255,255,0.14); box-shadow: 0 50px 120px rgba(0,0,0,0.7); transform-origin: 0 0; }
      #hook .k { position: absolute; left: 50px; top: 46px; font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.14em; color: #8b90a0; }
      #hook .n { position: absolute; left: 44px; top: 96px; font-weight: 900; font-size: 230px; letter-spacing: -0.06em; line-height: 0.9; color: var(--lime); white-space: nowrap; }
      #hook .s { position: absolute; left: 50px; top: 322px; font-weight: 850; font-size: 60px; letter-spacing: -0.02em; line-height: 1.05; color: #fff; }
      #hook .pagecard { left: 50px; top: 470px; width: 840px; }
      #hook .src { position: absolute; left: 50px; bottom: 34px; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.1em; color: #9a9ca6; }

      /* UI over everything */
      .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 78% at 50% 45%, rgba(4,5,10,0) 60%, rgba(4,5,10,0.5) 100%); }
      .botshade { position: absolute; left: 0; top: 1150px; width: 1080px; height: 770px;
        background: linear-gradient(180deg, rgba(4,5,10,0) 0%, rgba(4,5,10,0.7) 22%, rgba(4,5,10,0.9) 100%); }
      .topshade { position: absolute; left: 0; top: 0; width: 1080px; height: 320px; background: linear-gradient(180deg, rgba(4,5,10,0.8) 0%, rgba(4,5,10,0.55) 70%, rgba(4,5,10,0) 100%); }
      .grain { position: absolute; inset: 0; background-image: url("assets/grain.png"); opacity: 0.07; mix-blend-mode: overlay; }
      .flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
      .black { position: absolute; inset: 0; background: #000; opacity: 0; }
      .tag2 { position: absolute; left: 40px; top: 150px; display: inline-flex; align-items: center; gap: 12px; padding: 12px 22px 12px 18px;
        border: 2px solid rgba(255,255,255,0.16); border-radius: 999px; background: rgba(8,9,14,0.7); font-family: "Mono", monospace; font-weight: 700;
        font-size: 26px; letter-spacing: 0.08em; color: var(--ink); }
      .tag2 .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 14px var(--lime); }
      .brand { position: absolute; right: 40px; top: 168px; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.08em; color: rgba(245,245,242,0.78); }
      #trk { position: absolute; left: 40px; top: 232px; width: 1000px; height: 52px; display: flex; gap: 12px; }
      #trk .c { position: relative; flex: 1; border-radius: 14px; background: rgba(20,22,29,0.9); border: 2px solid rgba(255,255,255,0.12);
        font-family: "Mono", monospace; font-weight: 700; font-size: 21px; letter-spacing: 0.08em; color: #6d7180; display: flex; align-items: center; justify-content: center; gap: 8px; overflow: hidden; }
      #trk .c .f { position: absolute; inset: 0; background: var(--lime); transform-origin: 0 50%; }
      #trk .c span { position: relative; }
      #trk .c .ck { position: relative; display: none; }
      .chip2 { position: absolute; padding: 12px 20px; border-radius: 12px; background: rgba(6,8,12,0.9); border: 2px solid currentColor; color: var(--lime);
        font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.08em; white-space: nowrap; opacity: 0; }

      /* captions: karaoke */
      #caps { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .cap { position: absolute; left: 40px; width: 1000px; top: 1262px; text-align: center; opacity: 0; font-weight: 900; font-size: 84px; text-transform: uppercase;
        letter-spacing: -0.02em; line-height: 1.0; color: #fff; text-shadow: 0 6px 26px rgba(0,0,0,0.6), 0 2px 4px rgba(0,0,0,0.55); -webkit-text-stroke: 0; paint-order: stroke fill; }
      .cap .cb { display: inline-block; }
      .cw { display: inline-block; margin: 0 0.12em; }
      .cw.dim { opacity: 0.5; }

      /* end card */
      #end { position: absolute; inset: 0; opacity: 0; }
      #end .dim { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(5,6,10,0.8), rgba(5,6,10,0.96)); }
      .mark { position: absolute; left: 430px; top: 470px; width: 220px; height: 220px; border-radius: 52px; background: var(--lime);
        display: flex; align-items: flex-end; justify-content: center; gap: 8px; padding-bottom: 50px; box-shadow: 0 0 80px rgba(200,255,77,0.45); }
      .mark .one { font-weight: 900; font-size: 154px; line-height: 0.73; color: #0b0c10; letter-spacing: -0.06em; }
      .mark .cur { width: 42px; height: 16px; border-radius: 3px; background: #0b0c10; }
      .etitle { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900; letter-spacing: -0.05em; line-height: 0.95; white-space: nowrap; }
      .cta { position: absolute; display: inline-flex; align-items: center; gap: 16px; padding: 22px 36px; border-radius: 999px; background: var(--lime);
        color: #0b0c10; font-weight: 850; font-size: 42px; letter-spacing: -0.01em; white-space: nowrap; }
      .fontwarm { position: absolute; left: -9999px; top: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="1080" data-height="1920">
      <div id="base" class="clip" data-start="0" data-duration="%DUR%" style="background: #04050a; z-index: 0"></div>
      <div id="stage" class="clip" data-start="0" data-duration="%DUR%" style="z-index: 10; overflow: hidden">
        <div id="world"><div id="drift">
          <div class="gridbg"></div><div class="boardglow"></div>
          <div id="pins"></div>
          <div id="phone"><div class="frame"></div><div id="screen">
            <div id="sbar"><div class="tm">9:41</div><div class="ic"><span class="sig"><i style="height:14px"></i><i style="height:20px"></i><i style="height:26px"></i><i style="height:32px"></i></span><span class="bat"><b></b></span></div></div>
            <div id="notch"></div>
            <div id="scrs"></div>
            <div class="glare"></div>
          </div></div>
          <div id="board"></div>
        </div></div>
      </div>
      <div id="ui" class="clip" data-start="0" data-duration="%DUR%" style="z-index: 100">
        <div class="vig"></div>
        <div class="topshade"></div>
        <div class="botshade" id="botshade"></div>
        <div id="trk"></div>
        <div id="fx"></div>
        <div class="grain" id="grain"></div>
        <div class="progress" id="prog" style="background:var(--lime)"></div>
        <div class="tag2" id="tag"><span class="dot"></span>AI TREND · STORY</div>
        <div class="brand" id="bm">@ONEAITRICK</div>
        <div id="caps"></div>
        <div id="end">
          <div class="dim"></div>
          <div class="mark" id="mark"><span class="one">1</span><span class="cur"></span></div>
          <div class="etitle" id="ename" style="top:760px;font-size:110px">One <span style="color:var(--lime)">AI</span> Trick</div>
          <div class="etitle" id="ehandle" style="top:890px;font-family:Mono, monospace;font-weight:500;font-size:40px;letter-spacing:0.04em;color:var(--muted)">@oneaitrick</div>
          <div class="cta" id="fol" style="left:205px;top:990px">+ Follow for AI, explained</div>
        </div>
        <div class="flash" id="flash"></div>
        <div class="black" id="black"></div>
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span></div>
      </div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%;
      const WS = %WS%, WE = %WE%;
      const PAGES = %PAGES%, LOGOS = %LOGOS%;
      const w = (k) => WS[k], we = (k) => WE[k];
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out", IO = "power2.inOut";
      const el = (tag, cls, css, html, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css;
        if (html !== undefined) e.innerHTML = html; (parent || $("#board")).appendChild(e); return e; };
      // every tween after an element's first one must not render at build time
      const at = (sel, vars, t) => tl.to(sel, vars, t);
      const fin = (sel, from, to, t) => tl.fromTo(sel, from, Object.assign({ immediateRender: false }, to), t);
      const flash = (t, a, d, c) => { tl.set("#flash", { background: c || "#fff" }, t); fin("#flash", { opacity: a }, { opacity: 0, duration: d || 0.35, ease: "power2.out" }, t); };

      // ---------- the seek-safe painter: one clock redraws every canvas ----------
      const PAINT = [];
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate() { const T = clock.t; PAINT.forEach((f) => f(T)); } }, 0);
      const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

      // ---------- camera: the board, or pushed into the phone screen ----------
      // pushed: the phone (0.4) times the world (2.5) shows the screen at 1:1; design row dy sits at frame y 300
      const BOARD = { scale: 1, x: 0, y: 0 };
      const PUSH = (dy) => ({ scale: 2.5, x: -810, y: -580 - dy });
      const CLOSE = { scale: 1.32, x: 540 - 1.32 * 540, y: 770 - 1.32 * 780 };
      tl.set("#world", BOARD, 0);
      const cam = (state, t, d, ease) => at("#world", Object.assign({}, state, { duration: d || 0.5, ease: ease || IO }), t);
      tl.fromTo("#drift", { scale: 1 }, { scale: 1.03, duration: DUR / 2, ease: "sine.inOut" }, 0);
      at("#drift", { scale: 1, duration: DUR / 2, ease: "sine.inOut" }, DUR / 2);

      // ---------- screens inside the phone ----------
      const SCR = {};
      const scr = (id, bg) => { const s = el("div", "scr", "", `<div class="bg" style="background:${bg || "#07080c"}"></div>`, $("#scrs")); s.id = "sc-" + id; SCR[id] = s; return s; };
      const inS = (id) => SCR[id];
      const swapS = (a, b, t, kind) => { const A = SCR[a], B = SCR[b];
        if (kind === "cut" || !A) { tl.set(B, { opacity: 1, x: 0, y: 0, rotationY: 0 }, t); if (A) tl.set(A, { opacity: 0 }, t); return; }
        if (kind === "fade") { fin(B, { opacity: 0, x: 0, y: 0 }, { opacity: 1, duration: 0.25, ease: "power1.out" }, t - 0.12); tl.set(A, { opacity: 0 }, t + 0.14); return; }
        if (kind === "slide") { fin(B, { opacity: 1, x: 1000, y: 0 }, { x: 0, duration: 0.34, ease: "power3.inOut" }, t - 0.17);
          at(A, { x: -420, opacity: 0.0, duration: 0.34, ease: "power3.inOut" }, t - 0.17); tl.set(A, { opacity: 0, x: 0 }, t + 0.2); return; }
        if (kind === "up") { fin(B, { opacity: 1, y: 2140, x: 0 }, { y: 0, duration: 0.36, ease: "power3.inOut" }, t - 0.18);
          at(A, { y: -600, opacity: 0, duration: 0.36, ease: "power3.inOut" }, t - 0.18); tl.set(A, { opacity: 0, y: 0 }, t + 0.2); return; }
        if (kind === "page") { tl.set(B, { transformPerspective: 2600, transformOrigin: "0% 50%" }, 0);
          fin(B, { opacity: 1, rotationY: -88, x: 0, y: 0 }, { rotationY: 0, duration: 0.42, ease: "power2.out" }, t - 0.12);
          tl.set(A, { transformPerspective: 2600, transformOrigin: "100% 50%" }, 0);
          at(A, { rotationY: 70, opacity: 0, duration: 0.3, ease: "power2.in" }, t - 0.3); tl.set(A, { opacity: 0, rotationY: 0 }, t + 0.15); return; }
      };

      // ---------- the chapter tracker ----------
      const CH = ["CALL", "COPY", "MARKET", "BANK", "LOCKS"];
      const CHE0 = 0;
      const CHE = CH.map((n, i) => { const c = el("div", "c", "", `<div class="f"></div><span class="ck">✓</span><span>${i + 1} ${n}</span>`, $("#trk")); return c; });
      const chapter = (k, t) => { const c = CHE[k];
        fin(c.querySelector(".f"), { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: E }, t);
        at(c, { color: "#0b0c10", borderColor: "#c8ff4d", duration: 0.2 }, t + 0.05);
        fin(c, { scale: 1 }, { scale: 1.08, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, t);
        if (k > 0) { const p = CHE[k - 1];
          at(p.querySelector(".f"), { opacity: 0, duration: 0.3 }, t); at(p, { color: "#c8ff4d", borderColor: "rgba(200,255,77,0.6)", duration: 0.3 }, t);
          tl.set(p.querySelector(".ck"), { display: "inline" }, t); } };
      CHE.forEach((c) => tl.set(c.querySelector(".f"), { scaleX: 0 }, 0));

      // ---------- pins ----------
      const PINS = [
        { slot: [40, 352], big: "1 IN 3", lab: "got a fake-voice call", src: "HIYA SURVEY" },
        { slot: [40, 570], big: "30 SEC", lab: "of audio can be enough", src: "ELEVENLABS" },
        { slot: [40, 788], big: "7.4×", lab: "more cloning trade in 2 years", src: "NORDVPN · AS REPORTED" },
        { slot: [40, 1006], big: "$10", lab: "for a stolen cloning account", src: "NORDVPN · AS REPORTED" },
        { slot: [760, 352], big: "CODE", lab: "= your second lock", src: "FTC" },
        { slot: [760, 570], big: "LOCK 1", lab: "a family safe word", src: "FBI" },
        { slot: [760, 788], big: "LOCK 2", lab: "the code stays · call back", src: "FTC" },
      ];
      const PE = PINS.map((p, i) => el("div", "pin", `left:${p.slot[0]}px;top:${p.slot[1]}px`,
        `<div class="glow"></div><div class="no">0${i + 1}</div><div class="bg">${p.big}</div><div class="lb">${p.lab}</div><div class="sr">${p.src}</div><div class="stp">SELLS PROTECTION</div>`, $("#pins")));
      PE.forEach((p) => tl.set(p.querySelector(".stp"), { rotation: -9 }, 0));
      // a pin lands: big in the middle of the board, then down into its slot; it stays bright until the next one lands
      const land = (k, t, fromHook) => { const p = PE[k], [x, y] = PINS[k].slot;
        if (!fromHook) { const dx = 540 - (x + 140), dy = 760 - (y + 100);
          fin(p, { opacity: 0, x: dx, y: dy, scale: 1.9 }, { opacity: 1, duration: 0.18, ease: "power1.out" }, t);
          at(p, { x: 0, y: 0, scale: 1, duration: 0.5, ease: "power3.inOut" }, t + 0.2); }
        else { tl.set(p, { opacity: 1, x: 0, y: 0, scale: 1 }, t); }
        fin(p.querySelector(".glow"), { opacity: 0 }, { opacity: 1, duration: 0.2 }, t + (fromHook ? 0 : 0.6));
        at(p.querySelector(".glow"), { opacity: 0, duration: 0.5 }, t + 2.4); };

      // ---------- pages (real PDFs, cropped by crops.py) ----------
      // a page card: the crop scaled to width W; hl boxes are in the crop's pixels
      const page = (key, parent, css, W, H) => { const P = PAGES[key] || {};
        if (!P.have) { const c = el("div", "pagecard", css + `;width:${W}px;height:${H}px`, "", parent);
          el("div", "need", "", `PAGE NEEDED · ${key}<b>${P.name || ""}</b>`, c); return { c, hls: [], have: false }; }
        // the card is as tall as the crop (plus its label), at most H; a taller crop is framed on its first highlight
        const s = W / P.w, lab = P.label ? 52 : 0, ih = P.h * s, ch = Math.min(H, ih + lab);
        const hy = (P.hl && P.hl.length) ? P.hl[0][1] * s : 0, top = Math.max(0, Math.min(ih - (ch - lab), hy - (ch - lab) * 0.4));
        const c = el("div", "pagecard", css + `;width:${W}px;height:${ch}px`, "", parent);
        el("img", "", `width:${W}px;height:${ih}px;top:${-top}px`, undefined, c).src = P.img;
        const hls = (P.hl || []).map(([x, y, ww, hh]) => el("div", "hl", `left:${x * s - 4}px;top:${y * s - top - 2}px;width:${ww * s + 8}px;height:${hh * s + 4}px`, "", c));
        hls.forEach((h) => tl.set(h, { scaleX: 0 }, 0));
        if (P.label) el("div", "sl", "", P.label, c);
        return { c, hls, have: true }; };
      const sweep = (hls, t, d) => hls.forEach((h, i) => fin(h, { scaleX: 0 }, { scaleX: 1, duration: d || 0.45, ease: IO }, t + i * (d || 0.45) * 0.9));
      const logoTile = (code, parent, css) => { const L = LOGOS[code] || {};
        if (!L.have) return el("div", "logot need", css, `LOGO NEEDED · ${code}`, parent);
        return el("div", "logot", css + (L.bg ? `;background:${L.bg}` : ""), L.svg ? L.svg + (L.word ? `<span style="font-size:${L.fs || 56}px;letter-spacing:-0.02em">${L.word}</span>` : "") : `<img src="${L.img}" alt="" />`, parent); };
      // logos draw on: the outline traces, then the fill comes in
      const logoIn = (tile, t) => { const paths = tile.querySelectorAll("path");
        fin(tile, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, t);
        paths.forEach((p) => { const L = 400; tl.set(p, { attr: { "stroke-dasharray": L, "stroke-dashoffset": L, stroke: "currentColor", "stroke-width": 0.35, "fill-opacity": 0 } }, 0);
          fin(p, { attr: { "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power2.inOut" }, t + 0.05);
          fin(p, { attr: { "fill-opacity": 0 } }, { attr: { "fill-opacity": 1 }, duration: 0.25 }, t + 0.45); }); };

      // ===================================================== the story =====================================================
      %FXJS%

      // ---------- end card ----------
      const TE = w(222) - 0.05;
      fin("#end", { opacity: 0 }, { opacity: 1, duration: 0.5 }, TE);
      fin("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, TE + 0.15);
      fin(["#ename", "#ehandle"], { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.45, ease: E, stagger: 0.12 }, TE + 0.4);
      fin("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, TE + 0.85);
      at("#fol", { scale: 1.05, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, TE + 1.4);
      at("#mark", { boxShadow: "0 0 140px rgba(200,255,77,0.8)", duration: 0.9, yoyo: true, repeat: 1, ease: "sine.inOut" }, TE + 1.1);

      // ---------- global UI ----------
      tl.set(["#bm", "#tag", "#trk"], { opacity: 1 }, 0); at(["#bm", "#tag", "#trk"], { opacity: 0, duration: 0.4 }, TE - 0.2);
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      at([".botshade", ".topshade"], { opacity: 0, duration: 0.5 }, TE);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);
      fin("#black", { opacity: 0 }, { opacity: 1, duration: 0.4 }, DUR - 0.45);

      // ---------- captions: the spoken word lights up ----------
      const CAPS = (window.CAPS || []).map((c) => ({ t0: c.t0, t1: c.t1, w: c.w.map((x) => ({ d: x.d, s: x.s, e: x.e, em: x.emph })) }));
      const capsRoot = $("#caps");
      CAPS.forEach((ch) => {
        const c = el("div", "cap", "", undefined, capsRoot);
        const cb = el("span", "cb", "", undefined, c); const spans = ch.w.map((x) => { const s = el("span", "cw dim", "", x.d, cb); return { s, x }; });
        tl.fromTo(c, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }, ch.t0);
        tl.set(c, { opacity: 0 }, ch.t1);
        spans.forEach(({ s, x }, k) => { const end = k + 1 < spans.length ? spans[k + 1].x.s : ch.t1;
          tl.set(s, { opacity: 1, color: "#c8ff4d" }, x.s); tl.set(s, { color: x.em ? "#c8ff4d" : "#ffffff" }, end); }); });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>

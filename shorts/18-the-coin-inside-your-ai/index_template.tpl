<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <script src="captions.js"></script>
    <link rel="stylesheet" href="assets/base.css" />
    <style>
      /* ---------- the board: one stage (the balance scale) for the whole short ---------- */
      #world { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }
      #drift { position: absolute; inset: 0; transform-origin: 540px 700px; }
      .gridbg { position: absolute; left: -400px; top: -400px; width: 1880px; height: 2720px; background-color: #0b0c10;
        background-image: linear-gradient(rgba(124,196,255,0.07) 2px, transparent 2px), linear-gradient(90deg, rgba(124,196,255,0.07) 2px, transparent 2px),
          linear-gradient(rgba(124,196,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(124,196,255,0.03) 1px, transparent 1px);
        background-size: 120px 120px, 120px 120px, 30px 30px, 30px 30px; background-position: 400px 400px; }
      .boardglow { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
        background: radial-gradient(ellipse 55% 34% at 50% 36%, rgba(124,196,255,0.10), rgba(4,5,10,0) 70%), radial-gradient(ellipse 90% 70% at 50% 42%, rgba(4,5,10,0) 50%, rgba(4,5,10,0.8) 100%); }
      #stagewrap { position: absolute; left: 0; top: 0; width: 1080px; height: 1300px; transform-origin: 540px 330px; }
      #stage, #coinTop { position: absolute; left: 0; top: 0; width: 1080px; height: 1300px; }
      #over, #board, #pins { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .h { opacity: 0; }
      .abs { position: absolute; }
      .mono { font-family: "Mono", monospace; font-weight: 700; letter-spacing: 0.08em; }
      .pill { position: absolute; padding: 14px 28px; border-radius: 999px; font-family: "Mono", monospace; font-weight: 700; font-size: 30px;
        letter-spacing: 0.08em; white-space: nowrap; }
      .pagecard { position: absolute; left: 40px; width: 920px; border-radius: 22px; background: #f8f6f1; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,0.6); }
      .pagecard img { position: absolute; left: 0; top: 0; }
      .pagecard .hl { position: absolute; mix-blend-mode: multiply; border-radius: 6px; transform-origin: 0 50%; background: rgba(200,255,77,0.9); }
      .pagecard .sl { position: absolute; left: 0; right: 0; bottom: 0; padding: 9px 20px; font-family: "Mono", monospace; font-weight: 700; font-size: 19px;
        letter-spacing: 0.1em; color: #4a4d57; background: #efede7; border-top: 2px solid #e2dfd6; text-transform: uppercase; }
      .glass { position: absolute; border-radius: 30px; background: rgba(22,25,34,0.78); border: 2px solid rgba(255,255,255,0.14);
        box-shadow: 0 40px 100px rgba(0,0,0,0.6); backdrop-filter: blur(14px); }
      .logot { position: absolute; display: flex; align-items: center; justify-content: center; gap: 18px; border-radius: 22px; background: #f0eee6;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5); font-weight: 800; color: #141413; }
      .logot svg { height: 52%; width: auto; }

      /* pins: one fact each, parked beside the scale for the rest of the short */
      .pin { position: absolute; width: 210px; height: 160px; border-radius: 20px; background: rgba(20,22,29,0.94); border: 2px solid rgba(255,255,255,0.12);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5); opacity: 0; transform-origin: 50% 50%; overflow: visible; }
      .pin .bg { position: absolute; left: 16px; top: 16px; font-weight: 900; font-size: 60px; letter-spacing: -0.04em; word-spacing: 0.14em; line-height: 1; color: #f5f5f2; white-space: nowrap; }
      .pin .lb { position: absolute; left: 16px; right: 10px; top: 88px; font-weight: 750; font-size: 25px; line-height: 1.08; color: #e8e9ee; letter-spacing: -0.01em; }
      .pin .sr { position: absolute; right: 12px; top: 14px; font-family: "Mono", monospace; font-weight: 700; font-size: 15px; letter-spacing: 0.08em; color: #a3a8b6; white-space: nowrap; }
      .pin .glow { position: absolute; inset: -4px; border-radius: 22px; border: 4px solid var(--lime); box-shadow: 0 0 34px rgba(200,255,77,0.55); opacity: 0; }
      .pin.q { border: 3px dashed rgba(200,255,77,0.7); }

      /* the claim card on frame one (and again on the last frame, so the short loops) */
      #hook { position: absolute; left: 70px; top: 770px; width: 940px; height: 430px; border-radius: 34px; background: #14161d;
        border: 2px solid rgba(255,255,255,0.14); box-shadow: 0 50px 120px rgba(0,0,0,0.7); transform-origin: 0 0; }
      #hook .k { position: absolute; left: 150px; top: 44px; font-family: "Mono", monospace; font-weight: 700; font-size: 25px; letter-spacing: 0.12em; color: #a3a8b6; }
      #hook .l1 { position: absolute; left: 48px; top: 104px; font-weight: 900; font-size: 104px; letter-spacing: -0.045em; line-height: 1; color: #fff; white-space: nowrap; }
      #hook .l2 { position: absolute; left: 48px; top: 222px; height: 170px; display: flex; align-items: center; gap: 26px; font-weight: 900; font-size: 104px;
        letter-spacing: -0.045em; line-height: 1; color: #fff; white-space: nowrap; }
      .odo { display: inline-flex; color: var(--lime); font-size: 168px; }
      .odo .dg { display: inline-block; height: 168px; overflow: hidden; line-height: 168px; }
      .odo .dg .col { display: flex; flex-direction: column; }
      .odo .dg .col span { height: 168px; line-height: 168px; display: block; text-align: center; }

      /* UI over everything */
      .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 78% at 50% 45%, rgba(4,5,10,0) 60%, rgba(4,5,10,0.5) 100%); }
      .botshade { position: absolute; left: 0; top: 1150px; width: 1080px; height: 770px;
        background: linear-gradient(180deg, rgba(4,5,10,0) 0%, rgba(4,5,10,0.7) 22%, rgba(4,5,10,0.9) 100%); }
      .topshade { position: absolute; left: 0; top: 0; width: 1080px; height: 320px; background: linear-gradient(180deg, rgba(4,5,10,0.8) 0%, rgba(4,5,10,0.55) 70%, rgba(4,5,10,0) 100%); }
      .amberedge { position: absolute; inset: 0; box-shadow: inset 0 0 160px 40px rgba(255,181,71,0.42); opacity: 0; }
      .grain { position: absolute; inset: 0; background-image: url("assets/grain.png"); opacity: 0.07; mix-blend-mode: overlay; }
      .flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
      .tag2 { position: absolute; left: 40px; top: 150px; display: inline-flex; align-items: center; gap: 12px; padding: 12px 22px 12px 18px;
        border: 2px solid rgba(255,255,255,0.16); border-radius: 999px; background: rgba(8,9,14,0.7); font-family: "Mono", monospace; font-weight: 700;
        font-size: 26px; letter-spacing: 0.08em; color: var(--ink); }
      .tag2 .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--pink); box-shadow: 0 0 14px var(--pink); }
      .brand { position: absolute; right: 40px; top: 168px; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.08em; color: rgba(245,245,242,0.78); }
      #trk { position: absolute; left: 40px; top: 232px; width: 1000px; height: 52px; display: flex; gap: 12px; }
      #trk .c { position: relative; flex: 1; border-radius: 14px; background: rgba(20,22,29,0.9); border: 2px solid rgba(255,255,255,0.12);
        font-family: "Mono", monospace; font-weight: 700; font-size: 21px; letter-spacing: 0.08em; color: #6d7180; display: flex; align-items: center; justify-content: center; gap: 8px; overflow: hidden; }
      #trk .c .f { position: absolute; inset: 0; background: var(--lime); transform-origin: 0 50%; }
      #trk .c span { position: relative; }
      #trk .c .ck { position: relative; display: none; }
      .chip2 { position: absolute; padding: 10px 18px; border-radius: 12px; background: rgba(6,8,12,0.9); border: 2px solid currentColor; color: var(--lime);
        font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.08em; white-space: nowrap; opacity: 0; }

      /* captions: karaoke, with keyword pops (from #18: the word bounces 100-115-100 % on a coloured box) */
      #caps { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .cap { position: absolute; left: 40px; width: 1000px; top: 1262px; text-align: center; opacity: 0; font-weight: 900; font-size: 84px; text-transform: uppercase;
        letter-spacing: -0.02em; line-height: 1.0; color: #fff; text-shadow: 0 6px 26px rgba(0,0,0,0.6), 0 2px 4px rgba(0,0,0,0.55); paint-order: stroke fill; }
      .cap .cb { display: inline-block; }
      .cw { display: inline-block; margin: 0 0.12em; border-radius: 14px; }
      .cw.dim { opacity: 0.5; }
      .cw.pop { padding: 0 0.14em; }

      /* end card */
      #end { position: absolute; inset: 0; opacity: 0; }
      #end .dim { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(5,6,10,0.4), rgba(5,6,10,0.72)); }
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
      <div id="world-clip" class="clip" data-start="0" data-duration="%DUR%" style="z-index: 10; overflow: hidden">
        <div id="world"><div id="drift">
          <div class="gridbg"></div><div class="boardglow"></div>
          <div id="stagewrap"><canvas id="stage" width="1620" height="1950"></canvas></div>
          <div id="over"></div>
          <div id="board"></div>
          <canvas id="coinTop" width="1620" height="1950"></canvas>
          <div id="pins"></div>
        </div></div>
      </div>
      <div id="ui" class="clip" data-start="0" data-duration="%DUR%" style="z-index: 100">
        <div class="vig"></div>
        <div class="amberedge" id="amberedge"></div>
        <div class="topshade"></div>
        <div class="botshade" id="botshade"></div>
        <div id="trk"></div>
        <div class="grain" id="grain"></div>
        <div class="progress" id="prog" style="background:var(--lime)"></div>
        <div class="tag2" id="tag"><span class="dot"></span>AI PAPER · STORY</div>
        <div class="brand" id="bm">@ONEAITRICK</div>
        <div id="end">
          <div class="dim"></div>
          <div class="mark" id="mark"><span class="one">1</span><span class="cur"></span></div>
          <div class="etitle" id="ename" style="top:760px;font-size:110px">One <span style="color:var(--lime)">AI</span> Trick</div>
          <div class="etitle" id="ehandle" style="top:890px;font-family:Mono, monospace;font-weight:500;font-size:40px;letter-spacing:0.04em;color:var(--muted)">@oneaitrick</div>
          <div style="position:absolute;left:0;top:990px;width:1080px;display:flex;justify-content:center"><div class="cta" id="fol" style="position:relative;left:auto;top:auto">+ Follow for AI, explained</div></div>
        </div>
        <div id="caps"></div>
        <div class="flash" id="flash"></div>
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span></div>
      </div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%;
      const WS = %WS%, WE = %WE%;
      const PAGES = %PAGES%, LOGOS = %LOGOS%, POPS = %POPS%;
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

      // ---------- the seek-safe painter: one clock redraws every canvas from the time alone ----------
      const PAINT = [];
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate() { const T = clock.t; PAINT.forEach((f) => f(T)); } }, 0);
      const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

      // ---------- camera: the whole stage, or pushed in to one framing over the orb and the upper stage ----------
      // pushed: board x 180-900, y 360-950 fill the frame above the captions (scale 1.5)
      const BOARD = { scale: 1, x: 0, y: 0 };
      const PUSH = { scale: 1.5, x: -270, y: -240 };
      gsap.set("#world", BOARD);   // frame-one state on the DOM (a tl.set at 0 reverts when the renderer seeks back to frame 0)
      const cam = (state, t, d, ease) => at("#world", Object.assign({}, state, { duration: d || 0.5, ease: ease || IO }), t);
      tl.fromTo("#drift", { scale: 1 }, { scale: 1.03, duration: DUR / 2, ease: "sine.inOut" }, 0);
      at("#drift", { scale: 1, duration: DUR / 2, ease: "sine.inOut" }, DUR / 2);

      // ---------- the chapter tracker ----------
      const CH = ["COIN", "SCALE", "FOLLOW", "CATCH", "FIX"];
      const CHE = CH.map((n, i) => el("div", "c", "", `<div class="f"></div><span class="ck">✓</span><span>${i + 1} ${n}</span>`, $("#trk")));
      const chapter = (k, t) => { const c = CHE[k];
        fin(c.querySelector(".f"), { scaleX: 0, opacity: 1 }, { scaleX: 1, duration: 0.4, ease: E }, t);
        fin(c, { color: "#6d7180", borderColor: "rgba(255,255,255,0.12)" }, { color: "#0b0c10", borderColor: "#c8ff4d", duration: 0.2 }, t + 0.05);
        fin(c, { scale: 1 }, { scale: 1.08, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, t);
        if (k > 0) { const p = CHE[k - 1];
          at(p.querySelector(".f"), { opacity: 0, duration: 0.3 }, t); at(p, { color: "#c8ff4d", borderColor: "rgba(200,255,77,0.6)", duration: 0.3 }, t);
          tl.set(p.querySelector(".ck"), { display: "inline" }, t); } };
      // frame-one state of the tracker (also restored for the mirror at the end)
      const trkReset = (t) => { const S = t === 0 ? (x, v) => gsap.set(x, v) : (x, v) => tl.set(x, v, t);
        CHE.forEach((c, i) => { S(c.querySelector(".f"), { scaleX: i === 0 ? 1 : 0, opacity: 1 });
          S(c.querySelector(".ck"), { display: "none" });
          S(c, { color: i === 0 ? "#0b0c10" : "#6d7180", borderColor: i === 0 ? "#c8ff4d" : "rgba(255,255,255,0.12)" }); }); };
      trkReset(0);   // frame one: on the DOM, not as a tl.set at 0

      // ---------- pins ----------
      const L = 30, R = 840, ROWS = [330, 506, 682, 858, 1034];
      const PINS = [
        { slot: [L, ROWS[0]], big: "50", lab: "experts, one hidden coin" },
        { slot: [L, ROWS[1]], big: "86%", lab: "went with the coin" },
        { slot: [L, ROWS[2]], big: "60%", lab: "switched sides (38 cases)", lfs: 22 },
        { slot: [L, ROWS[3]], big: "77%", lab: "used its words" },
        { slot: [L, ROWS[4]], big: "1 IN 7", lab: "gave it credit", fs: 48 },
        { slot: [R, ROWS[0]], big: "HEAVY", lab: "on purpose, in 1 test", fs: 52 },
        { slot: [R, ROWS[1]], big: "2 SIDES", lab: "ask for both", fs: 42 },
      ];
      const PE = PINS.map((p) => el("div", "pin", `left:${p.slot[0]}px;top:${p.slot[1]}px`,
        `<div class="glow"></div><div class="bg"${p.fs ? ` style="font-size:${p.fs}px;top:${16 + (60 - p.fs) / 2}px"` : ""}>${p.big}</div><div class="lb"${p.one ? ' style="white-space:nowrap;font-size:23px"' : p.lfs ? ` style="font-size:${p.lfs}px"` : ""}>${p.lab}</div>${p.sr ? `<div class="sr" style="left:16px;right:auto;top:124px">${p.sr}</div>` : ""}`, $("#pins")));
      // a pin slides in from the scale's side along its own row, lime while it is new, then rests at 60 % with a white number
      const PIN_REST = 0.85;
      const land = (k, t, fromHook) => { const p = PE[k], [x] = PINS[k].slot, dx = x < 540 ? 220 : -220, bg = p.querySelector(".bg");
        if (!fromHook) fin(p, { opacity: 0, x: dx, scale: 0.92 }, { opacity: 1, x: 0, scale: 1, duration: 0.5, ease: "power3.out" }, t);
        else tl.set(p, { opacity: 1, x: 0, scale: 1 }, t);
        tl.set(bg, { color: "#c8ff4d" }, t);
        fin(p.querySelector(".glow"), { opacity: 0 }, { opacity: 1, duration: 0.2 }, t + (fromHook ? 0 : 0.35));
        at(p.querySelector(".glow"), { opacity: 0, duration: 0.5 }, t + 2.4);
        at(bg, { color: "#f5f5f2", duration: 0.4 }, t + 2.4); at(p, { opacity: PIN_REST, duration: 0.4 }, t + 2.4); };

      // ---------- pages (the real post, cut by crops.py) ----------
      const page = (key, parent, css, W, H, fit, zoom) => { const P = PAGES[key];
        const s0 = W / P.w, HL = P.hl || [[0, 0, P.w, P.h]];
        // fit: the whole line across the card (no panning); otherwise zoom so the longest highlight fills it
        const s = zoom ? s0 * zoom : fit ? s0 : Math.max(s0, Math.min(s0 * 2.6, (W * 0.86) / Math.max(...HL.map((h) => h[2]))));
        const iw = P.w * s, lh = Math.max(...HL.map((h) => h[3]));
        const yT = P.whole ? 0 : Math.max(0, Math.min(...HL.map((h) => h[1])) - lh * 0.55), yB = P.whole ? P.h : Math.min(P.h, Math.max(...HL.map((h) => h[1] + h[3])) + lh * 0.55);
        const lab = P.label ? 40 : 0, ch = Math.min(H, (yB - yT) * s + lab);
        const X = HL.map(([x, , ww]) => Math.max(0, Math.min(iw - W, (x + ww / 2) * s - W / 2)));
        const c = el("div", "pagecard", css + `;width:${W}px;height:${ch}px`, "", parent);
        const inner = el("div", "", `position:absolute;left:0;top:0;width:${iw}px;height:${P.h * s}px`, "", c);
        el("img", "", `width:${iw}px;height:${P.h * s}px;top:${-yT * s}px;left:0`, undefined, inner).src = P.img;
        const hls = HL.map(([x, y, ww, hh]) => el("div", "hl", `left:${x * s - 4}px;top:${(y - yT) * s - 2}px;width:${ww * s + 8}px;height:${hh * s + 4}px`, "", inner));
        gsap.set(inner, { x: -X[0] });
        if (iw > W + 2) { el("div", "", "position:absolute;left:0;top:0;bottom:0;width:50px;background:linear-gradient(90deg,#f8f6f1,rgba(248,246,241,0))", "", c);
          el("div", "", "position:absolute;right:0;top:0;bottom:0;width:50px;background:linear-gradient(270deg,#f8f6f1,rgba(248,246,241,0))", "", c); }
        // mark highlight i at time ts[i]; the strip pans to it first when it is off the card
        const mark = (ts, d) => hls.forEach((h, i) => { const ti = ts[i];
          if (i > 0 && X[i] !== X[i - 1]) at(inner, { x: -X[i], duration: 0.35, ease: IO }, ti - 0.3);
          fin(h, { scaleX: 0 }, { scaleX: 1, duration: d || 0.4, ease: IO }, ti); });
        hls.forEach((h) => gsap.set(h, { scaleX: 0 }));
        if (P.label) el("div", "sl", "", P.label, c);
        return { c, hls, mark, ch }; };
      const logoTile = (code, parent, css) => { const Lg = LOGOS[code];
        return el("div", "logot", css, Lg.svg + (Lg.word ? `<span style="font-size:${Lg.fs || 46}px;letter-spacing:-0.02em">${Lg.word}</span>` : ""), parent); };
      // logos draw on: the outline traces, then the fill comes in
      const logoIn = (tile, t) => { const paths = tile.querySelectorAll("path");
        fin(tile, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, t);
        paths.forEach((p) => { const Ln = 400; gsap.set(p, { attr: { "stroke-dasharray": Ln, "stroke-dashoffset": Ln, stroke: "currentColor", "stroke-width": 0.35, "fill-opacity": 0 } });
          fin(p, { attr: { "stroke-dashoffset": Ln } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power2.inOut" }, t + 0.05);
          fin(p, { attr: { "fill-opacity": 0 } }, { attr: { "fill-opacity": 1 }, duration: 0.25 }, t + 0.45); }); };

      // ===================================================== the story =====================================================
      %FXJS%

      // ---------- global UI ----------
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);

      // ---------- captions: the spoken word lights up; keyword pops bounce on a coloured box ----------
      const CAPS = (window.CAPS || []).map((c) => ({ t0: c.t0, t1: c.t1, w: c.w.map((x) => ({ d: x.d, s: x.s, e: x.e, em: x.emph })) }));
      const capsRoot = $("#caps");
      const popAt = (s) => POPS.find((p) => Math.abs(p.t - s) < 0.08);
      CAPS.forEach((ch) => {
        const c = el("div", "cap", "", undefined, capsRoot);
        const cb = el("span", "cb", "", undefined, c); const spans = ch.w.map((x) => { const pp = popAt(x.s); const s = el("span", "cw dim" + (pp ? " pop" : ""), "", x.d, cb); return { s, x, pp }; });
        tl.fromTo(c, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }, ch.t0);
        tl.set(c, { opacity: 0 }, ch.t1);
        spans.forEach(({ s, x, pp }, k) => { const end = k + 1 < spans.length ? spans[k + 1].x.s : ch.t1;
          if (pp) { tl.set(s, { opacity: 1, color: "#0b0c10", backgroundColor: pp.col, textShadow: "none" }, x.s);
            fin(s, { scale: 1 }, { scale: 1.15, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, x.s); return; }
          tl.set(s, { opacity: 1, color: "#c8ff4d" }, x.s); tl.set(s, { color: x.em ? "#c8ff4d" : "#ffffff" }, end); }); });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
      PAINT.forEach((f) => f(0));   // frame one is painted even if a seek to 0 fires no update
    </script>
  </body>
</html>

<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <script src="captions.js"></script>
    <link rel="stylesheet" href="assets/base.css" />
    <style>
      @font-face { font-family: "mono"; src: url("assets/fonts/mono-700.woff2") format("woff2"); font-weight: 700; }
      @font-face { font-family: "interv"; src: url("assets/fonts/inter.woff2") format("woff2"); font-weight: 100 900; }
      .shot { position: absolute; inset: 0; overflow: hidden; }
      .fx, .cam { position: absolute; inset: 0; transform-origin: 50% 45%; }
      .vid { position: absolute; object-fit: cover; }
      .still, .frz { position: absolute; }
      .frz { left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .bd { position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; background-size: cover; background-position: center;
        filter: brightness(0.4) saturate(0.9); }
      .desk { position: absolute; inset: 0; background:
        radial-gradient(ellipse 70% 45% at 50% 38%, rgba(255,255,255,0.06), rgba(0,0,0,0) 70%),
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: auto, 72px 72px, 72px 72px; }
      .card { position: absolute; overflow: hidden; border-radius: 24px; background: #fff;
        box-shadow: 0 40px 90px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08); }
      .card.dark { background: #0d1117; box-shadow: 0 40px 90px rgba(0,0,0,0.6), 0 0 0 2px rgba(121,184,255,0.25); }
      .card img { position: absolute; }
      .scroller { position: absolute; left: 0; top: 0; width: 100%; }
      .hl { position: absolute; mix-blend-mode: multiply; border-radius: 6px; transform-origin: 0 50%; transform: scaleX(0); }
      .card.dark .hl { mix-blend-mode: screen; }
      .splitline { position: absolute; left: 0; top: 954px; width: 1080px; height: 12px; background: #0b0c10; box-shadow: 0 0 30px rgba(0,0,0,0.8); }
      .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 42%, rgba(4,5,10,0) 55%, rgba(4,5,10,0.55) 100%); }
      .botshade { position: absolute; left: 0; top: 1020px; width: 1080px; height: 900px; background: linear-gradient(180deg, rgba(4,5,10,0) 0%, rgba(4,5,10,0.68) 36%, rgba(4,5,10,0.86) 100%); }
      .doctop { position: absolute; left: 0; top: 0; width: 1080px; height: 320px; pointer-events: none;
        background: linear-gradient(180deg, rgba(4,5,10,0.9) 0, rgba(4,5,10,0.84) 215px, rgba(4,5,10,0) 320px); }
      .docfade { position: absolute; left: 0; top: 1085px; width: 1080px; height: 835px; pointer-events: none;
        background: linear-gradient(180deg, rgba(4,5,10,0) 0, rgba(4,5,10,0.9) 130px, rgba(4,5,10,0.96) 175px, rgba(4,5,10,0.96) 100%); }
      .topshade { position: absolute; left: 0; top: 0; width: 1080px; height: 330px; background: linear-gradient(180deg, rgba(4,5,10,0.62) 0%, rgba(4,5,10,0) 100%); }
      .grain { position: absolute; inset: 0; background-image: url("assets/grain.png"); opacity: 0.075; mix-blend-mode: overlay; }
      .flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
      .black { position: absolute; inset: 0; background: #000; opacity: 0; }
      .tag2 { position: absolute; left: 60px; top: 150px; display: inline-flex; align-items: center; gap: 12px; padding: 12px 22px 12px 18px;
        border: 2px solid rgba(255,255,255,0.16); border-radius: 999px; background: rgba(8,9,14,0.62); font-family: "Mono", monospace; font-weight: 700;
        font-size: 26px; letter-spacing: 0.08em; color: var(--ink); }
      .tag2 .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 14px var(--lime); }
      .src { position: absolute; left: 60px; top: 232px; display: inline-flex; align-items: center; gap: 10px; font-family: "Mono", monospace; font-weight: 700;
        font-size: 21px; letter-spacing: 0.1em; padding: 9px 15px; border-radius: 10px; background: rgba(6,8,12,0.72); color: #d4d6de;
        border: 1.5px solid rgba(255,255,255,0.16); opacity: 0; white-space: nowrap; }
      .src .sd { width: 10px; height: 10px; border-radius: 50%; background: #ff5b5b; box-shadow: 0 0 10px #ff5b5b; }
      .src.gen .sd { background: #b9a2ff; box-shadow: 0 0 10px #b9a2ff; }

      /* designed captions */
      .cap { position: absolute; opacity: 0; font-weight: 900; text-transform: uppercase; letter-spacing: -0.02em; line-height: 1.0; color: #fff;
        text-shadow: 0 6px 26px rgba(0,0,0,0.6), 0 2px 4px rgba(0,0,0,0.55); }
      .cap.S, .cap.B { left: 40px; width: 1000px; bottom: 470px; text-align: center; font-size: 80px; }
      .cap.A { left: 66px; width: 960px; bottom: 470px; text-align: left; font-size: 72px; }
      .cw { display: inline-block; margin: 0 0.16em; transform-origin: 50% 70%; }
      .cap.A .cw { margin: 0 0.32em 0 0; }
      .cw.dim { opacity: 0.45; }
      .cw.hero { display: block; margin: 0.16em 0 0.22em; line-height: 0.92; letter-spacing: -0.04em; transform-origin: 0 60%; position: relative; }
      .cw.hero .bar { position: absolute; left: 0.02em; bottom: -0.1em; height: 0.07em; border-radius: 0.04em; transform-origin: 0 50%; }
      .cw.num { display: block; font-size: 2.1em; letter-spacing: -0.05em; line-height: 0.95; margin: 0.02em 0; }
      .cw.num.clock { font-family: "Mono", monospace; font-weight: 700; font-size: 1.7em; letter-spacing: 0.02em; }
      .cw.inl { font-size: 1.12em; }

      /* shot graphics */
      .stamp { position: absolute; font-weight: 900; font-size: 92px; letter-spacing: -0.01em; padding: 10px 30px; border: 9px solid currentColor; border-radius: 18px;
        color: #ff5b5b; background: rgba(12,6,8,0.5); opacity: 0; white-space: nowrap; }
      .chip { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.1em; padding: 14px 22px;
        border-radius: 14px; background: rgba(6,8,12,0.84); border: 2px solid currentColor; opacity: 0; white-space: nowrap; color: var(--lime); }
      .chip .sw { display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: currentColor; margin-right: 14px; vertical-align: 2px; box-shadow: 0 0 12px currentColor; }
      .panel { position: absolute; left: 60px; top: 330px; padding: 22px 28px 14px; border-radius: 24px; background: rgba(8,10,16,0.6); border: 1.5px solid rgba(255,255,255,0.16);
        opacity: 0; }
      .panel .ph { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.16em; color: #b9bcc6; margin-bottom: 12px; }
      .panel .pi { font-weight: 900; font-size: 46px; letter-spacing: -0.02em; line-height: 1.25; opacity: 0; color: #fff; }
      .panel .pi b { color: var(--lime); margin-right: 14px; }
      .portrait { position: absolute; width: 360px; padding: 16px 16px 20px; background: #f3efe6; border-radius: 6px; box-shadow: 0 30px 60px rgba(0,0,0,0.55); opacity: 0; }
      .portrait .pimg { width: 328px; height: 400px; background-size: cover; background-position: center top; filter: grayscale(1) contrast(1.05); }
      .portrait .pn { margin-top: 12px; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.06em; color: #1b1c22; text-align: center; }
      .portrait .py { font-family: "Mono", monospace; font-weight: 500; font-size: 20px; color: #5a5d66; text-align: center; margin-top: 4px; }
      .readout { position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; }
      .readout .rl { font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.2em; color: #c9ccd6; }
      .readout .rv { font-weight: 900; font-size: 130px; letter-spacing: -0.04em; line-height: 1; color: #fff; }
      .ring { position: absolute; border-radius: 50%; border: 6px solid var(--lime); box-shadow: 0 0 26px rgba(200,255,77,0.8), inset 0 0 20px rgba(200,255,77,0.4); opacity: 0; }
      .lens { position: absolute; border-radius: 50%; overflow: hidden; border: 8px solid #e8f6ff; box-shadow: 0 0 40px rgba(180,230,255,0.8), 0 30px 60px rgba(0,0,0,0.5); opacity: 0; background: #06121c; }
      .badge { position: absolute; font-weight: 900; font-size: 64px; padding: 10px 28px; border-radius: 999px; background: #ffd36b; color: #0b0c10; opacity: 0;
        box-shadow: 0 0 40px rgba(255,211,107,0.6); }
      .bars { position: absolute; left: 60px; width: 960px; opacity: 0; }
      .bars .row { display: flex; align-items: center; height: 120px; margin-bottom: 24px; }
      .bars .lab { width: 290px; font-family: "Mono", monospace; font-weight: 700; font-size: 32px; letter-spacing: 0.08em; color: #d4d6de; }
      .bars .bar { height: 96px; border-radius: 16px; transform-origin: 0 50%; display: flex; align-items: center; padding-left: 24px; font-weight: 900; font-size: 50px; color: #0b0c10; white-space: nowrap; }
      .codegrid { position: absolute; opacity: 0; }
      .scanline { position: absolute; height: 8px; background: #7ee787; box-shadow: 0 0 26px 8px rgba(126,231,135,0.55); opacity: 0; }
      .tk { position: absolute; font-weight: 900; font-size: 30px; color: #7ee787; opacity: 0; text-shadow: 0 0 10px rgba(126,231,135,0.8); }
      .crack { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .tracklab { position: absolute; left: 0; top: 0; opacity: 0; }
      .tracklab .tl { font-weight: 900; font-size: 54px; color: #0b0c10; background: var(--lime); padding: 8px 20px; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); white-space: nowrap; }
      .tracklab .dotp { position: absolute; left: -16px; top: 74px; width: 22px; height: 22px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 16px var(--lime); }
      .splitlab { position: absolute; left: 60px; font-weight: 900; font-size: 46px; padding: 10px 22px; border-radius: 14px; background: rgba(6,8,12,0.78); opacity: 0; white-space: nowrap; }

      /* end card */
      #end { position: absolute; inset: 0; opacity: 0; }
      #end .dim { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(5,6,10,0.72), rgba(5,6,10,0.95)); }
      .mark { position: absolute; left: 420px; top: 470px; width: 240px; height: 240px; border-radius: 56px; background: var(--lime);
        display: flex; align-items: flex-end; justify-content: center; gap: 8px; padding-bottom: 54px; box-shadow: 0 0 80px rgba(200,255,77,0.45); }
      .mark .one { font-weight: 900; font-size: 168px; line-height: 0.73; color: #0b0c10; letter-spacing: -0.06em; }
      .mark .cur { width: 46px; height: 17px; border-radius: 3px; background: #0b0c10; }
      .mtitle { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900; letter-spacing: -0.05em; line-height: 0.95; }
      .cta { position: absolute; display: inline-flex; align-items: center; gap: 16px; padding: 24px 36px; border-radius: 999px; background: var(--lime);
        color: #0b0c10; font-weight: 850; font-size: 46px; letter-spacing: -0.01em; }
      .fontwarm { position: absolute; left: -9999px; top: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="1080" data-height="1920">
      <div id="base" class="clip" data-start="0" data-duration="%DUR%" style="background: #04050a; z-index: 0"></div>
%SHOTS%
      <div id="ui" class="clip" data-start="0" data-duration="%DUR%" style="z-index: 100">
        <div class="vig"></div>
        <div class="topshade"></div>
        <div class="botshade" id="botshade"></div>

        <!-- s04 -->
        <div class="stamp" id="stUnclaimed" style="left:150px;top:720px">UNCLAIMED</div>
        <!-- s06: the authors of the rulebook -->
        <div class="portrait" id="ptNavier" style="left:80px;top:420px"><div class="pimg" style="background-image:url(assets/img/navier.jpg)"></div><div class="pn">CLAUDE-LOUIS NAVIER</div><div class="py">1785–1836</div></div>
        <div class="portrait" id="ptStokes" style="left:640px;top:480px"><div class="pimg" style="background-image:url(assets/img/stokes.jpg)"></div><div class="pn">GEORGE GABRIEL STOKES</div><div class="py">1819–1903</div></div>
        <!-- s07-s11: one rulebook, everywhere -->
        <div class="panel" id="uses"><div class="ph">ONE RULEBOOK FOR…</div>
          <div class="pi" id="u1"><b>✓</b>WATER</div><div class="pi" id="u2"><b>✓</b>AIR</div><div class="pi" id="u3"><b>✓</b>WEATHER</div><div class="pi" id="u4"><b>✓</b>PLANE WINGS</div><div class="pi" id="u5"><b>✓</b>YOUR BLOOD</div></div>
        <!-- s14: the rulebook breaks -->
        <svg class="crack" id="crack" viewBox="0 0 1080 1920">
          <g stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 10px rgba(255,90,90,0.9))">
            <path class="ck" d="M540 760 L470 640 L500 540 L410 400 L430 300" /><path class="ck" d="M540 760 L640 690 L700 560 L820 500 L900 380" />
            <path class="ck" d="M540 760 L600 880 L560 1010 L640 1150" /><path class="ck" d="M540 760 L420 830 L330 820 L200 930 L120 900" />
            <path class="ck" d="M540 760 L700 800 L820 900 L980 880" /><path class="ck" d="M470 640 L380 610 L300 650" />
          </g></svg>
        <!-- s16 / s25: speed at the core -->
        <div class="ring" id="ringCore" style="left:430px;top:850px;width:220px;height:220px"></div>
        <div class="readout" id="spd1" style="top:345px"><div class="rl">SPEED AT THE CENTRE</div><div class="rv" id="spd1v">1×</div></div>
        <div class="readout" id="spd2" style="top:345px"><div class="rl">SPEED AT THE CORE</div><div class="rv" id="spd2v">1×</div></div>
        <!-- s24 -->
        <div class="ring" id="ringFig" style="width:150px;height:150px"></div>
        <!-- s26-s28: the tap -->
        <div class="chip" id="chPress" style="left:60px;top:330px;color:#ff6b6b"><span class="sw"></span>⚠ PRESSURE RISING…</div>
        <div class="lens" id="lens" style="left:240px;top:520px;width:600px;height:600px"><canvas id="mol" width="600" height="600" style="width:600px;height:600px"></canvas></div>
        <div class="chip" id="chMol" style="left:310px;top:1150px;color:#9fe0ff"><span class="sw"></span>H₂O · REAL WATER</div>
        <!-- s30 -->
        <div class="stamp" id="stCatch" style="left:250px;top:700px;transform:rotate(-7deg)">WAIT…</div>
        <!-- s32: the push -->
        <div class="tracklab" id="push"><div class="tl">THE PUSH →</div><div class="dotp"></div></div>
        <!-- s33 / s35 -->
        <div class="chip" id="chAllowed" style="left:60px;top:1150px;color:#7ee787"><span class="sw"></span>THE PRIZE RULES: ALLOWED ✓</div>
        <div class="chip" id="chAlone" style="left:60px;top:1150px;color:#9fe0ff"><span class="sw"></span>WATER LEFT ALONE: THE BIG ONE</div>
        <!-- s34 -->
        <div class="splitlab" id="slTop" style="top:330px;color:#ffd36b">STIRRED · ALLOWED ✓</div>
        <div class="splitlab" id="slBot" style="top:990px;color:#9fe0ff">LEFT ALONE · THE REAL MYSTERY?</div>
        <!-- s38: the referee reads every step -->
        <div class="scanline" id="scan"></div>
        <div id="ticks"></div>
        <!-- s39 -->
        <div class="stamp" id="stOk" style="left:210px;top:660px;color:#7ee787;transform:rotate(-6deg)">✓ CHECKED</div>
        <!-- s41 -->
        <div class="badge" id="eqq">= ?</div>
        <!-- s42 -->
        <div class="chip" id="chHuman" style="left:60px;top:330px;color:#ffd36b"><span class="sw"></span>HUMAN CHECK · STILL GOING</div>
        <!-- s46 -->
        <div class="chip" id="chH1" style="left:60px;top:1060px;color:#ffb547"><span class="sw"></span>DIEGO CÓRDOBA</div>
        <div class="chip" id="chH2" style="left:440px;top:1060px;color:#ffb547"><span class="sw"></span>LUIS MARTÍNEZ-ZOROA</div>
        <!-- s48 -->
        <div class="bars" id="bars" style="top:620px">
          <div class="row"><div class="lab">THE PRIZE</div><div class="bar" id="b1" style="width:170px;background:#ffd36b">$1M</div></div>
          <div class="row"><div class="lab">THE COMPUTING</div><div class="bar" id="b2" style="width:640px;background:#ff8a5b">SEVERAL $ MILLION</div></div></div>
        <!-- s50-s51 -->
        <div class="chip" id="chSolved" style="left:60px;top:1150px;color:#7ee787"><span class="sw"></span>SOLVED · POINCARÉ CONJECTURE</div>
        <div class="stamp" id="stDeclined" style="left:190px;top:700px;transform:rotate(-8deg)">DECLINED</div>
        <div class="chip" id="chPerelman" style="left:60px;top:330px;color:#ff8a8a"><span class="sw"></span>GRIGORI PERELMAN · TURNED DOWN $1M, 2010</div>
        <!-- s52 -->
        <div class="chip" id="chWait" style="left:60px;top:1150px;color:#ffb547"><span class="sw"></span>⏳ RULE: WAIT AT LEAST 2 YEARS</div>

        %LABELS%

        <div class="grain" id="grain"></div>
        <div class="progress" id="prog" style="background:var(--lime)"></div>
        <div class="tag2" id="tag"><span class="dot"></span>AI EXPLAINED · TRUE STORY</div>
        <div class="brandmark" id="bm" style="right: 60px; top: 158px; padding-top: 10px">@ONEAITRICK</div>
        <div id="caps"></div>
        <div id="end">
          <div class="dim"></div>
          <div class="mark" id="mark"><span class="one">1</span><span class="cur"></span></div>
          <div class="mtitle" id="ename" style="top:760px;font-size:110px">One <span style="color:var(--lime)">AI</span> Trick</div>
          <div class="mtitle" id="ehandle" style="top:900px;font-family:Mono, monospace;font-weight:500;font-size:40px;letter-spacing:0.04em;color:var(--muted)">@oneaitrick</div>
          <div class="cta" id="fol" style="left:220px;top:1000px">+ Follow for AI, explained</div>
        </div>
        <div class="flash" id="flash"></div>
        <div class="black" id="black"></div>
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span></div>
      </div>

      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%, HND = %H%;
      const SH = %SHOTSJS%;
      const GEO = %GEO%;
      const COL = %COL%;
      const TRACK = %TRACK%;
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out";
      const fx = (id) => "#fx-" + id, cam = (id) => "#cam-" + id;
      const T0 = Object.fromEntries(SH.map((s) => [s.id, s.t0])), T1 = Object.fromEntries(SH.map((s) => [s.id, s.t1]));
      const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; };
      const el = (tag, cls, css, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css; (parent || $("#ui")).appendChild(e); return e; };

      // ---------- shots: visibility and default camera ----------
      const CUSTOM_CAM = new Set(["s13", "s17", "s18", "s19", "s21", "s22", "s23", "s24", "s31", "s33", "s35", "s36", "s37", "s38", "s43", "s44", "s45", "s46", "s48", "s49", "s50", "s52", "s30", "s57"]);
      SH.forEach((s, i) => {
        tl.set(fx(s.id), { opacity: i === 0 ? 1 : 0 }, 0);
        const a = Math.max(0, s.t0 - HND), b = s.t1 + HND;
        if (CUSTOM_CAM.has(s.id)) return;
        const card = ["PAGE", "IMG", "PDF", "PAIR"].includes(s.k);
        tl.fromTo(cam(s.id), { scale: 1 }, { scale: card ? 1.035 : 1.07, duration: b - a, ease: "none" }, a);
      });
      const flash = (t, a, d, c) => { tl.set("#flash", { background: c || "#fff" }, t); tl.fromTo("#flash", { opacity: a }, { opacity: 0, duration: d || 0.35, ease: "power2.out", immediateRender: false }, t); };
      const cardIn = (id, t) => { const c = document.querySelectorAll("#cam-" + id + " .card");
        tl.fromTo(c, { opacity: 0, scale: 0.86, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.6)", stagger: 0.12 }, t); };
      const TR = {
        whip(A, B, T) { tl.fromTo(fx(B), { opacity: 1, x: 1080, filter: "blur(22px)" }, { x: 0, filter: "blur(0px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16);
          tl.to(fx(A), { x: -760, filter: "blur(22px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16); tl.set(fx(A), { opacity: 0 }, T + 0.14); },
        slideup(A, B, T) { tl.fromTo(fx(B), { opacity: 1, y: 1920, filter: "blur(22px)" }, { y: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17);
          tl.to(fx(A), { y: -1100, filter: "blur(22px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17); tl.set(fx(A), { opacity: 0 }, T + 0.15); },
        zoom(A, B, T) { tl.to(fx(A), { scale: 1.45, filter: "blur(18px)", opacity: 0, duration: 0.26, ease: "power2.in" }, T - 0.16);
          tl.fromTo(fx(B), { opacity: 0, scale: 0.84, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: E }, T - 0.1); flash(T - 0.02, 0.25, 0.3); },
        spin(A, B, T) { tl.to(fx(A), { rotation: 30, scale: 1.5, filter: "blur(20px)", opacity: 0, duration: 0.3, ease: "power2.in" }, T - 0.18);
          tl.fromTo(fx(B), { opacity: 0, rotation: -30, scale: 1.5, filter: "blur(20px)" }, { opacity: 1, rotation: 0, scale: 1, filter: "blur(0px)", duration: 0.36, ease: E }, T - 0.08); },
        flash(A, B, T, c) { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T); flash(T, 0.6, 0.42, c); },
        dip(A, B, T) { tl.to("#black", { opacity: 1, duration: 0.14, ease: "power1.in" }, T - 0.14); tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T);
          tl.to("#black", { opacity: 0, duration: 0.28, ease: "power1.out" }, T); },
        cut(A, B, T) { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T); },
        glitch(A, B, T) { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T);
          [[0, 34, "hue-rotate(80deg) saturate(2)"], [0.033, -26, "hue-rotate(-60deg)"], [0.066, 16, "none"], [0.1, -8, "none"], [0.133, 0, "none"]].forEach(([dt, x, f]) => tl.set(fx(B), { x, filter: f }, T + dt));
          flash(T, 0.3, 0.25, "#4fd0ff"); },
        card(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out" }, T - 0.12); tl.set(fx(A), { opacity: 0 }, T + 0.12); cardIn(B, T - 0.05); },
        fade(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.inOut" }, T - 0.25); tl.set(fx(A), { opacity: 0 }, T + 0.26); },
      };
      const CUTS = [["s01", "s02", "flash", "#ffd36b"], ["s02", "s03", "whip"], ["s03", "s04", "zoom"], ["s04", "s05", "dip"], ["s05", "s06", "zoom"],
        ["s06", "s07", "whip"], ["s07", "s08", "whip"], ["s08", "s09", "slideup"], ["s09", "s10", "whip"], ["s10", "s11", "zoom"], ["s11", "s12", "dip"],
        ["s12", "s13", "card"], ["s13", "s14", "glitch"], ["s14", "s15", "spin"], ["s15", "s16", "zoom"], ["s16", "s17", "card"], ["s17", "s18", "slideup"],
        ["s18", "s19", "card"], ["s19", "s20", "flash", "#c8ff4d"], ["s20", "s21", "card"], ["s21", "s22", "slideup"], ["s22", "s23", "whip"], ["s23", "s24", "zoom"],
        ["s24", "s25", "spin"], ["s25", "s26", "flash", "#ffffff"], ["s26", "s27", "cut"], ["s27", "s28", "zoom"], ["s28", "s29", "whip"], ["s29", "s30", "cut"],
        ["s30", "s31", "card"], ["s31", "s32", "whip"], ["s32", "s33", "card"], ["s33", "s34", "slideup"], ["s34", "s35", "card"], ["s35", "s36", "zoom"],
        ["s36", "s37", "slideup"], ["s37", "s38", "whip"], ["s38", "s39", "flash", "#7ee787"], ["s39", "s40", "whip"], ["s40", "s41", "card"], ["s41", "s42", "dip"],
        ["s42", "s43", "glitch"], ["s43", "s44", "glitch"], ["s44", "s45", "slideup"], ["s45", "s46", "whip"], ["s46", "s47", "flash", "#ffd36b"], ["s47", "s48", "card"],
        ["s48", "s49", "slideup"], ["s49", "s50", "whip"], ["s50", "s51", "zoom"], ["s51", "s52", "card"], ["s52", "s53", "dip"], ["s53", "s54", "fade"],
        ["s54", "s55", "spin"], ["s55", "s56", "zoom"], ["s56", "s57", "fade"]];
      CUTS.forEach(([A, B, k, c]) => TR[k](A, B, T0[B], c));
      tl.fromTo("#flash", { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);

      // ---------- helpers ----------
      const show = (sel, t0, t1, from) => { tl.fromTo(sel, Object.assign({ opacity: 0, y: 14 }, from || {}), { opacity: 1, y: 0, x: 0, duration: 0.3, ease: E }, t0);
        tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const stamp = (sel, t0, t1, rot) => { tl.fromTo(sel, { opacity: 0, scale: 2.4, rotation: rot || -8 }, { opacity: 1, scale: 1, rotation: rot || -8, duration: 0.2, ease: "power4.out" }, t0);
        tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const punch = (id, t, s) => { tl.fromTo(fx(id), { scale: 1 }, { scale: 1 + (s || 0.06), duration: 0.12, ease: "power2.out", immediateRender: false }, t);
        tl.to(fx(id), { scale: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.12); };
      const shake = (id, t, a, n) => { for (let k = 0; k < (n || 6); k++) tl.set(fx(id), { x: (k % 2 ? -1 : 1) * a * (1 - k / (n || 6)), y: (k % 3 - 1) * a * 0.5 }, t + k * 0.04); tl.set(fx(id), { x: 0, y: 0 }, t + (n || 6) * 0.04); };
      const camTo = (id, ox, oy, s1, ease) => { const a = Math.max(0, T0[id] - HND), b = T1[id] + HND;
        tl.set(cam(id), { transformOrigin: `${ox}px ${oy}px` }, 0); tl.fromTo(cam(id), { scale: 1 }, { scale: s1, duration: b - a, ease: ease || "power1.inOut" }, a); };
      const docCam = (id) => { const g = GEO[id]; const hls = g[6] || []; const a = Math.max(0, T0[id] - HND), b = T1[id] + HND;
        const kf = (S, px, py) => { let y = 760 - S * py; const dy = 300 - (y + S * g[1]); if (dy > 0 && dy <= 160) y += dy;  // keep the card's top edge clear of the labels when a small nudge does it
        return { scale: S, x: 540 - S * px, y }; };
        tl.set(cam(id), { transformOrigin: "0px 0px" }, 0);
        if (!hls.length) { tl.fromTo(cam(id), kf(1, 540, 760), Object.assign(kf(1.06, g[0] + g[2] / 2, g[1] + g[3] / 2), { duration: b - a, ease: "none" }), a); return; }
        const zs = (w) => Math.max(1.05, Math.min(1.7, 880 / (w + 80)));
        let prevT = a;
        hls.forEach(([t, hx, hy, w], k) => { const end = Math.max(prevT + 0.35, t + 0.25); const tw = Object.assign(kf(zs(w), hx, hy), { duration: end - prevT, ease: "power2.inOut" });
          if (k === 0) tl.fromTo(cam(id), kf(1, 540, 760), tw, prevT); else tl.to(cam(id), tw, prevT); prevT = end; });
        const L = hls[hls.length - 1]; if (b > prevT + 0.05) tl.to(cam(id), Object.assign(kf(zs(L[3]) * 1.04, L[1], L[2]), { duration: b - prevT, ease: "none" }), prevT); };
      const numText = (v) => v >= 1e9 ? "∞" : (Math.round(v).toLocaleString("en-US") + "×");

      // highlights and source labels
      %HLJS%.forEach(([id, t, d]) => tl.to("#" + id, { scaleX: 1, duration: d, ease: "power2.inOut" }, t));
      %LABJS%.forEach(([sel, a, b]) => show(sel, a, b, { x: -20, y: 0 }));

      // ---------- shot moments ----------
      punch("s01", 0.16, 0.05); punch("s02", 1.34, 0.06); punch("s03", 3.47, 0.05);
      // s04: freeze on "out?"
      tl.set("#frz-s04", { opacity: 1 }, 6.54); tl.fromTo(fx("s04"), { filter: "saturate(1)" }, { filter: "saturate(0.15) brightness(0.8)", duration: 0.2, immediateRender: false }, 6.54);
      stamp("#stUnclaimed", 6.58, 7.12, -8); shake("s04", 6.58, 14);
      // s06: Navier and Stokes on "1800s"
      tl.fromTo("#ptNavier", { opacity: 0, x: -300, rotation: -14 }, { opacity: 1, x: 0, rotation: -5, duration: 0.4, ease: "back.out(1.4)" }, 10.35);
      tl.fromTo("#ptStokes", { opacity: 0, x: 300, rotation: 14 }, { opacity: 1, x: 0, rotation: 4, duration: 0.4, ease: "back.out(1.4)" }, 10.5);
      tl.to(["#ptNavier", "#ptStokes"], { opacity: 0, y: -30, duration: 0.2 }, 11.2);
      // s07-s11: the checklist grows
      tl.fromTo("#uses", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.3, ease: E }, 11.5);
      [["#u1", 12.13], ["#u2", 12.79], ["#u3", 13.67], ["#u4", 14.16], ["#u5", 15.5]].forEach(([s, t]) => tl.fromTo(s, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.2, ease: E }, t));
      tl.to("#uses", { opacity: 0, duration: 0.2 }, 16.9);
      // s14: the rulebook BREAKS
      tl.set("#crack", { opacity: 1 }, 23.62); document.querySelectorAll("#crack .ck").forEach((p, k) => { const L = p.getTotalLength(); p.style.strokeDasharray = L;
        tl.fromTo(p, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: 0.22, ease: "power3.out" }, 23.64 + k * 0.03); });
      tl.to("#crack", { opacity: 0, duration: 0.2 }, 24.4); shake("s14", 23.64, 26, 8); flash(23.64, 0.35, 0.3, "#ff5b5b");
      // s16: one tiny spot, infinitely fast
      tl.fromTo("#ringCore", { opacity: 0, scale: 2.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, 28.45);
      tl.to("#ringCore", { scale: 0.35, duration: 1.6, ease: "power2.in" }, 28.8); tl.to("#ringCore", { opacity: 0, duration: 0.2 }, 30.9);
      tl.fromTo("#spd1", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.25 }, 28.8);
      (function () { const m = { v: 0 }; tl.fromTo(m, { v: 0 }, { v: 10, duration: 1.0, ease: "power2.in", onUpdate() { $("#spd1v").textContent = m.v >= 9.9 ? "∞" : numText(Math.pow(10, m.v)); } }, 29.0); })();
      tl.to("#spd1v", { color: "#c8ff4d", scale: 1.15, duration: 0.15 }, 30.0); tl.to("#spd1", { opacity: 0, duration: 0.2 }, 30.95);
      // s18
      punch("s18", 33.39, 0.04);
      // s20
      punch("s20", 37.3, 0.04);
      // s22: YES
      punch("s22", 41.1, 0.05); flash(41.1, 0.18, 0.25, "#4fd0ff");
      // s24: OpenAI's figure, push into the core
      (function () { const g = GEO.s24; const cx = g[0] + g[2] * 0.5, cy = g[1] + g[3] * 0.52; camTo("s24", cx, cy, 1.5, "power2.in");
        const r = $("#ringFig"); r.style.left = cx - 75 + "px"; r.style.top = cy - 75 + "px"; })();
      tl.fromTo("#ringFig", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3 }, 45.28); tl.to("#ringFig", { scale: 0.4, duration: 1.2, ease: "power2.in" }, 45.6);
      tl.to("#ringFig", { opacity: 0, duration: 0.15 }, 47.5);
      // s25: the collapse
      tl.fromTo("#spd2", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.25 }, 47.8);
      (function () { const m = { v: 0 }; tl.fromTo(m, { v: 0 }, { v: 10, duration: 3.8, ease: "power3.in", onUpdate() { $("#spd2v").textContent = m.v >= 9.9 ? "∞" : numText(Math.pow(10, m.v)); } }, 47.8); })();
      tl.to("#spd2v", { color: "#ffb066", scale: 1.2, duration: 0.15 }, 51.6); flash(51.6, 0.85, 0.9, "#ffffff"); tl.to("#spd2", { opacity: 0, duration: 0.3 }, 52.7);
      // s26-s28: the tap
      tl.fromTo(fx("s26"), { rotation: 0 }, { rotation: -7, duration: 1.6, ease: "power2.in", immediateRender: false }, 53.1);
      for (let k = 0; k < 14; k++) tl.set(cam("s26"), { x: (k % 2 ? -1 : 1) * (4 + k * 1.2), y: (k % 3 - 1) * 4 }, 53.5 + k * 0.09);
      show("#chPress", 53.3, 54.8, { x: -20 });
      tl.fromTo("#lens", { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 56.35); tl.to("#lens", { opacity: 0, scale: 1.3, duration: 0.25 }, 57.4);
      show("#chMol", 56.55, 57.4);
      (function () { const cv = $("#mol"), cx = cv.getContext("2d"); let seed = 5; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
        const M = []; for (let i = 0; i < 70; i++) M.push({ x: rnd() * 600, y: rnd() * 600, a: rnd() * 6.28, ph: rnd() * 6.28, vx: (rnd() - 0.5) * 2, vy: (rnd() - 0.5) * 2 });
        const p = { t: 0 }; tl.fromTo(p, { t: 0 }, { t: 1.2, duration: 1.2, ease: "none", onUpdate() { cx.fillStyle = "#06121c"; cx.fillRect(0, 0, 600, 600);
          M.forEach((m) => { const x = (m.x + m.vx * p.t * 60 + 600) % 600, y = (m.y + m.vy * p.t * 60 + 600) % 600, a = m.a + p.t * 3 + Math.sin(p.t * 20 + m.ph) * 0.2;
            const h1 = [x + Math.cos(a) * 26, y + Math.sin(a) * 26], h2 = [x + Math.cos(a + 1.82) * 26, y + Math.sin(a + 1.82) * 26];
            cx.strokeStyle = "rgba(200,230,255,0.5)"; cx.lineWidth = 6; cx.beginPath(); cx.moveTo(h1[0], h1[1]); cx.lineTo(x, y); cx.lineTo(h2[0], h2[1]); cx.stroke();
            cx.fillStyle = "#ff6b6b"; cx.beginPath(); cx.arc(x, y, 17, 0, 6.28); cx.fill(); cx.fillStyle = "#f2f6ff";
            cx.beginPath(); cx.arc(h1[0], h1[1], 10, 0, 6.28); cx.fill(); cx.beginPath(); cx.arc(h2[0], h2[1], 10, 0, 6.28); cx.fill(); }); } }, 56.3); })();
      // s29-s30: the catch (freeze)
      punch("s29", 58.36, 0.05);
      tl.fromTo(fx("s30"), { filter: "saturate(1) brightness(1)" }, { filter: "saturate(0) brightness(0.75)", duration: 0.15, immediateRender: false }, 59.67);
      tl.fromTo(cam("s30"), { scale: 1, rotation: 0 }, { scale: 1.12, rotation: 4, duration: 1.4, ease: "power2.out" }, 59.67);
      flash(59.67, 0.45, 0.25); stamp("#stCatch", 60.32, 61.05, -7);
      // s31 / s33 / s35: the documents
      ["s13", "s17", "s18", "s19", "s21", "s22", "s23", "s31", "s33", "s35", "s37", "s43", "s44", "s45", "s46", "s48", "s49", "s50", "s52"].forEach((id) => docCam(id));
      show("#chAllowed", 69.6, 70.2, { x: -20 }); show("#chAlone", 73.3, 74.4, { x: -20 });
      // s32: the push, riding on the spoon hand
      (function () { const a = T0.s32 - HND; const p = { f: 0 }; const lab = $("#push");
        tl.fromTo("#push", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 65.8); tl.to("#push", { opacity: 0, duration: 0.2 }, 68.4);
        tl.fromTo(p, { f: 0 }, { f: TRACK.length - 1, duration: (TRACK.length - 1) / 30, ease: "none", onUpdate() { const k = Math.round(p.f), q = TRACK[Math.min(k, TRACK.length - 1)];
          lab.style.transform = `translate(${q[0] + 30}px, ${q[1] - 110}px)`; } }, a); })();
      // s34 split
      show("#slTop", 70.4, 72.1, { x: -20 }); show("#slBot", 71.7, 72.1, { x: -20 });
      // s36: scroll through the proof files
      (function () { const g = GEO.s36; tl.fromTo("#sc-s36", { y: 0 }, { y: -(g[5] - g[3]), duration: 2.6, ease: "power2.in" }, T0.s36 - 0.1); })();
      // s38: the referee reads every step
      (function () { const g = GEO.s38; tl.fromTo("#sc-s38", { y: 0 }, { y: -(g[5] - g[3]) * 0.6, duration: 4.6, ease: "power1.inOut" }, T0.s38 - 0.2);
        const sc = $("#scan"); sc.style.left = g[0] + "px"; sc.style.width = g[2] + "px";
        tl.set("#scan", { opacity: 1, y: g[1] }, 79.3); tl.to("#scan", { y: g[1] + g[3] - 10, duration: 3.6, ease: "none" }, 79.3); tl.to("#scan", { opacity: 0, duration: 0.2 }, 82.9);
        for (let k = 0; k < 16; k++) { const y = g[1] + 30 + k * (g[3] - 60) / 15; const t = el("div", "tk", `left:${g[0] + g[2] - 60}px;top:${y - 18}px`, $("#ticks")); t.textContent = "✓";
          tl.fromTo(t, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.15 }, 79.3 + (k / 15) * 3.6); }
        tl.to("#ticks", { opacity: 0, duration: 0.2 }, 83.3); })();
      // s39: whistle, checked
      stamp("#stOk", 83.91, 84.62, -6); flash(83.91, 0.25, 0.3, "#7ee787");
      // s41: same game?
      (function () { const g = GEO.s41; const b = $("#eqq"); b.style.left = "430px"; b.style.top = (g[1] + g[3] + (g[4] - g[1] - g[3]) / 2 - 50) + "px"; })();
      tl.fromTo("#eqq", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 87.21); tl.to("#eqq", { opacity: 0, duration: 0.15 }, 88.2);
      show("#chHuman", 88.6, 92.0, { x: -20 });
      // s43-s44: the pushback
      punch("s44", 95.53, 0.05);
      // s46: the real heroes
      show("#chH1", 100.84, 103.45, { x: -20 }); show("#chH2", 101.0, 103.45, { x: 20 });
      // s48: prize vs computing
      tl.to("#card-s48", { opacity: 0.18, duration: 0.25 }, 106.25);
      tl.fromTo("#bars", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3 }, 106.25);
      tl.fromTo("#b1", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: E }, 106.3); tl.fromTo("#b2", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, 106.5);
      tl.to("#bars", { opacity: 0, duration: 0.2 }, 107.35);
      // s50-s51: the other winner said no
      show("#chSolved", 111.7, 113.45, { x: -20 }); stamp("#stDeclined", 114.01, 115.6, -8); show("#chPerelman", 113.6, 115.6, { x: -20 });
      // s52: the two-year rule
      show("#chWait", 116.9, 117.65, { x: -20 });
      // s53: slowly, carefully
      punch("s53", 117.74, 0.03); punch("s53", 118.64, 0.03);
      // s54: maybe
      punch("s54", 122.89, 0.05);

      // ---------- end card ----------
      tl.fromTo("#end", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 128.53);
      tl.fromTo("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, 128.68);
      tl.fromTo(["#ename", "#ehandle"], { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: E, stagger: 0.12 }, 128.93);
      tl.fromTo("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 129.38);
      tl.to("#fol", { scale: 1.06, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, 129.95);
      tl.to("#mark", { boxShadow: "0 0 140px rgba(200,255,77,0.8)", duration: 0.9, yoyo: true, repeat: 2, ease: "sine.inOut" }, 129.7);

      // ---------- global UI ----------
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      tl.fromTo(["#tag", "#bm"], { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.4 }, 0.1);
      tl.to(["#tag", "#bm"], { opacity: 0, duration: 0.4 }, 128.3);
      tl.to([".botshade", ".topshade"], { opacity: 0, duration: 0.5 }, 128.53);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);
      tl.fromTo("#black", { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, DUR - 0.45);

      // ---------- designed captions ----------
      const CAPLAY = %CAPLAY%, COVERS = %COVERS%;
      const layoutFor = (t) => (CAPLAY.find(([a, b]) => t >= a && t < b) || [0, 0, { m: "S", c: "#c8ff4d" }])[2];
      const covered = (a, b) => COVERS.some(([c0, c1]) => a < c1 && b > c0 - 0.02);
      const capsRoot = $("#caps");
      const fmtNum = (v, target, fmt, d) => { if (fmt === "clock") { const s = Math.round(v * 3600); return String(Math.floor(s / 3600)).padStart(2, "0") + ":" + String(Math.floor((s % 3600) / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); }
        const pre = d.match(/^[^\d]*/)[0], suf = d.match(/[^\d]*$/)[0]; const n = Math.round(v); return pre + (target >= 10000 ? n.toLocaleString("en-US") : String(n)) + suf; };
      (window.CAPS || []).forEach((ch) => {
        if (covered(ch.t0, ch.t1)) return;
        const L = layoutFor(ch.t0); const col = L.c;
        const c = document.createElement("div"); c.className = "cap " + L.m; if (ch.w.some((w) => w.emph)) c.setAttribute("data-layout-allow-overlap", ""); capsRoot.appendChild(c);
        const spans = ch.w.map((w) => { const s = document.createElement("span"); let d = w.d; if (d === "1800S") { d = "1800s"; s.style.textTransform = "none"; }
          const isNum = L.m === "B" && /\d/.test(d); const hero = w.emph && L.m === "A";
          s.className = "cw dim" + (isNum ? " num" + (L.fmt === "clock" ? " clock" : "") : "") + (hero ? " hero" : "") + (w.emph && !hero ? " inl" : "");
          if (hero) { const len = d.replace(/[^A-Z0-9']/gi, "").length; const fs = Math.min(210, Math.round(930 / (len * 0.64)));
            s.style.fontSize = fs + "px"; s.style.transform = "rotate(-3deg)"; s.style.textShadow = `0 0 40px ${rgba(col, 0.55)}, 0 8px 30px rgba(0,0,0,0.5)`; }
          s.textContent = isNum && L.fmt === "clock" ? "00:00:00" : d;
          if (hero) { const bar = document.createElement("span"); bar.className = "bar"; bar.style.width = "96%"; bar.style.background = col; bar.style.boxShadow = `0 0 20px ${col}`; s.appendChild(bar); }
          c.appendChild(s); return { s, w, isNum, hero, d }; });
        tl.fromTo(c, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.14, ease: "back.out(2)" }, ch.t0);
        tl.set(c, { opacity: 0 }, ch.t1);
        spans.forEach(({ s, w, isNum, hero, d }, k) => {
          const end = k + 1 < spans.length ? spans[k + 1].w.s : ch.t1;
          const keep = w.emph || isNum || hero;
          tl.set(s, { opacity: 1, color: col, scale: hero ? 1 : 1.05 }, w.s);
          tl.set(s, { color: keep ? col : "#ffffff", scale: 1 }, end);
          if (hero) { tl.fromTo(s, { scale: 1.18 }, { scale: 1, duration: 0.22, ease: "power4.out", immediateRender: false }, w.s);
            const bar = s.querySelector(".bar"); if (bar) tl.fromTo(bar, { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, w.s + 0.05); }
          if (isNum) { const target = L.fmt === "clock" ? parseFloat(d) : parseFloat(d.replace(/[^\d.]/g, "")); const m = { v: 0 };
            tl.set(s, { textShadow: `0 0 40px ${rgba(col, 0.6)}, 0 8px 30px rgba(0,0,0,0.5)` }, w.s);
            tl.fromTo(m, { v: 0 }, { v: target, duration: Math.max(0.4, w.e - w.s + 0.2), ease: "power2.out", onUpdate() { s.firstChild.nodeValue = fmtNum(m.v, target, L.fmt, d); } }, w.s);
            if (L.fmt !== "clock") s.firstChild.nodeValue = fmtNum(0, target, "", d); }
        });
      });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>

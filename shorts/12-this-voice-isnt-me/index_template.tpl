<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <script src="captions.js"></script>
    <link rel="stylesheet" href="assets/base.css" />
    <style>
      .shot { position: absolute; inset: 0; overflow: hidden; }
      .fx, .cam { position: absolute; inset: 0; transform-origin: 50% 45%; }
      .vid { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
      .bd { position: absolute; inset: 0; background-size: cover; background-position: center; }
      .slate { position: absolute; inset: 0; background: radial-gradient(ellipse 70% 60% at 50% 45%, #1b2030, #07080d); }
      .slate .st { position: absolute; left: 0; width: 1080px; top: 700px; text-align: center; font-family: "Mono", monospace; font-weight: 700;
        font-size: 30px; letter-spacing: 0.12em; color: #ff8a7a; }
      .slate .sd { position: absolute; left: 60px; width: 960px; top: 760px; text-align: center; font-weight: 700; font-size: 44px; color: #c9ccd6; }
      .card { position: absolute; overflow: hidden; border-radius: 18px; background: #fff;
        box-shadow: 0 40px 90px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08); }
      .card img { position: absolute; left: 0; top: 0; }
      .hl { position: absolute; mix-blend-mode: multiply; border-radius: 5px; transform-origin: 0 50%; transform: scaleX(0); background: rgba(200,255,77,0.78); }
      .phone { position: absolute; overflow: hidden; border-radius: 46px; background: #000;
        box-shadow: 0 50px 110px rgba(0,0,0,0.7), 0 0 0 12px #111318, 0 0 0 14px rgba(255,255,255,0.12); }
      .phone video { position: absolute; left: 0; top: 0; }
      .gfx { position: absolute; inset: 0; }
      .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 75% at 50% 45%, rgba(4,5,10,0) 58%, rgba(4,5,10,0.5) 100%); }
      .botshade { position: absolute; left: 0; top: 1100px; width: 1080px; height: 820px;
        background: linear-gradient(180deg, rgba(4,5,10,0) 0%, rgba(4,5,10,0.66) 30%, rgba(4,5,10,0.86) 100%); }
      .topshade { position: absolute; left: 0; top: 0; width: 1080px; height: 330px; background: linear-gradient(180deg, rgba(4,5,10,0.55) 0%, rgba(4,5,10,0) 100%); }
      .grain { position: absolute; inset: 0; background-image: url("assets/grain.png"); opacity: 0.07; mix-blend-mode: overlay; }
      .flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
      .black { position: absolute; inset: 0; background: #000; opacity: 0; }
      .tag2 { position: absolute; left: 60px; top: 150px; display: inline-flex; align-items: center; gap: 12px; padding: 12px 22px 12px 18px;
        border: 2px solid rgba(255,255,255,0.16); border-radius: 999px; background: rgba(8,9,14,0.62); font-family: "Mono", monospace; font-weight: 700;
        font-size: 26px; letter-spacing: 0.08em; color: var(--ink); }
      .tag2 .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 14px var(--lime); }
      .brand { position: absolute; right: 60px; top: 168px; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.08em; color: rgba(245,245,242,0.78); }
      .src { position: absolute; left: 60px; top: 232px; display: inline-flex; align-items: center; gap: 10px; font-family: "Mono", monospace; font-weight: 700;
        font-size: 19px; letter-spacing: 0.1em; padding: 9px 15px; border-radius: 10px; background: rgba(6,8,12,0.72); color: #d4d6de;
        border: 1.5px solid rgba(255,255,255,0.16); opacity: 0; white-space: nowrap; }
      .src .sd { width: 10px; height: 10px; border-radius: 50%; background: #ff5b5b; box-shadow: 0 0 10px #ff5b5b; }
      .src.gen .sd { background: #b9a2ff; box-shadow: 0 0 10px #b9a2ff; }
      .src.q .sd { background: #7cc4ff; box-shadow: 0 0 10px #7cc4ff; }
      .src.st .sd { background: #9a9ca6; box-shadow: none; }
      .chap { position: absolute; left: 56px; top: 98px; display: inline-flex; align-items: baseline; gap: 16px; opacity: 0; white-space: nowrap;
        padding: 12px 22px 14px; border-radius: 14px; background: rgba(8,9,14,0.8); border: 2px solid rgba(200,255,77,0.55); }
      .chap .n { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; color: var(--lime); letter-spacing: 0.06em; }
      .chap .t { font-weight: 850; font-size: 34px; letter-spacing: -0.015em; color: #fff; }

      /* captions: sentence case, karaoke */
      #caps { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .cap { position: absolute; left: 40px; width: 1000px; top: 1250px; text-align: center; opacity: 0; font-weight: 900; font-size: 84px; text-transform: uppercase;
        letter-spacing: -0.02em; line-height: 1.0; color: #fff; text-shadow: 0 6px 26px rgba(0,0,0,0.6), 0 2px 4px rgba(0,0,0,0.55); }
      .cap .cb { display: inline-block; }
      .cw { display: inline-block; margin: 0 0.12em; }
      .cw.dim { opacity: 0.5; }

      /* chips, logos, cards of my own */
      .chip { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.08em; padding: 14px 22px;
        border-radius: 14px; background: rgba(6,8,12,0.86); border: 2px solid currentColor; opacity: 0; white-space: nowrap; color: var(--lime); }
      .chip .sw { display: inline-block; width: 13px; height: 13px; border-radius: 50%; background: currentColor; margin-right: 14px; vertical-align: 2px; box-shadow: 0 0 12px currentColor; }
      .big { position: absolute; font-weight: 900; letter-spacing: -0.04em; line-height: 0.95; color: #fff; opacity: 0; white-space: nowrap;
        text-shadow: 0 10px 40px rgba(0,0,0,0.7); text-transform: uppercase; }
      .logo { position: absolute; display: flex; align-items: center; justify-content: center; border-radius: 22px; background: #fff; opacity: 0;
        box-shadow: 0 24px 60px rgba(0,0,0,0.55); }
      .logo img { max-width: 82%; max-height: 72%; object-fit: contain; }
      .logo.need { background: rgba(10,12,18,0.85); border: 3px dashed #ff8a7a; color: #ff8a7a; font-family: "Mono", monospace; font-weight: 700;
        font-size: 18px; letter-spacing: 0.08em; text-align: center; line-height: 1.3; }
      .logo .ln { position: absolute; left: 0; right: 0; bottom: -40px; text-align: center; font-family: "Mono", monospace; font-weight: 700; font-size: 18px;
        letter-spacing: 0.1em; color: #e8e9ee; text-transform: uppercase; text-shadow: 0 2px 10px rgba(0,0,0,0.8); }
      .logo .ok { position: absolute; right: -16px; top: -16px; width: 48px; height: 48px; border-radius: 50%; background: var(--lime); color: #0b0c10;
        font-weight: 900; font-size: 30px; display: flex; align-items: center; justify-content: center; opacity: 0; box-shadow: 0 0 22px rgba(200,255,77,0.8); }
      .logo.slot { background: rgba(255,255,255,0.06); border: 3px dashed rgba(255,255,255,0.6); box-shadow: none; }
      .tag { position: absolute; padding: 8px 14px; border-radius: 10px; font-family: "Mono", monospace; font-weight: 700; font-size: 18px; letter-spacing: 0.1em;
        background: #e0322b; color: #fff; white-space: nowrap; opacity: 0; }
      .panel { position: absolute; border-radius: 26px; background: rgba(8,9,14,0.86); border: 2px solid rgba(255,255,255,0.12);
        box-shadow: 0 40px 90px rgba(0,0,0,0.6); opacity: 0; }
      .quote { position: absolute; padding: 44px 54px 40px; border-radius: 26px; background: rgba(250,247,240,0.98); box-shadow: 0 40px 90px rgba(0,0,0,0.6); opacity: 0; }
      .quote .qk { font-family: "Mono", monospace; font-weight: 700; font-size: 21px; letter-spacing: 0.14em; color: #b4532a; margin-bottom: 20px; }
      .quote .qt { position: relative; font-family: Georgia, serif; font-size: 58px; line-height: 1.24; color: #1b1c22; }
      .quote .qh { background-image: linear-gradient(rgba(200,255,77,0.9), rgba(200,255,77,0.9)); background-repeat: no-repeat; background-position: 0 88%; background-size: 0% 80%; }
      .quote .qa { margin-top: 26px; font-family: "Mono", monospace; font-weight: 700; font-size: 20px; letter-spacing: 0.1em; color: #6b6e78; }
      .strike { position: absolute; height: 10px; border-radius: 5px; background: #e0322b; transform-origin: 0 50%; transform: scaleX(0); box-shadow: 0 0 18px rgba(224,50,43,0.6); }
      .stamp { position: absolute; font-weight: 900; font-size: 64px; letter-spacing: 0.01em; padding: 6px 26px; border: 8px solid currentColor; border-radius: 16px;
        color: #e0322b; opacity: 0; white-space: nowrap; background: rgba(255,255,255,0.04); }
      .step { position: absolute; display: flex; align-items: center; gap: 16px; padding: 16px 24px; border-radius: 16px; background: rgba(8,9,14,0.88);
        border: 2px solid rgba(255,255,255,0.16); font-weight: 800; font-size: 36px; color: #fff; opacity: 0; white-space: nowrap; }
      .step .k { font-family: "Mono", monospace; font-weight: 700; font-size: 22px; color: #9a9ca6; letter-spacing: 0.08em; }
      .step.on { border-color: var(--lime); box-shadow: 0 0 30px rgba(200,255,77,0.25); }
      .off { position: absolute; padding: 12px 26px; border-radius: 999px; background: var(--lime); color: #0b0c10; font-weight: 900; font-size: 34px;
        letter-spacing: 0.02em; opacity: 0; white-space: nowrap; box-shadow: 0 0 40px rgba(200,255,77,0.5); }
      .ring { position: absolute; border: 6px solid var(--lime); border-radius: 999px; opacity: 0; box-shadow: 0 0 26px rgba(200,255,77,0.8); }
      .bubble { position: absolute; border-radius: 26px; padding: 26px 32px; font-size: 34px; font-weight: 600; line-height: 1.35; opacity: 0; }
      .bubble.me { background: #2a6df4; color: #fff; border-bottom-right-radius: 8px; }
      .bubble.bot { background: #f3f1ea; color: #1b1c22; border-bottom-left-radius: 8px; }
      .bar { display: block; height: 22px; border-radius: 11px; background: rgba(27,28,34,0.18); margin: 14px 0; position: relative; }
      .bar .bt { position: absolute; right: -10px; top: -14px; transform: translateX(100%); }
      .score { position: absolute; width: 640px; padding: 40px 44px; border-radius: 26px; background: rgba(8,9,14,0.88); opacity: 0;
        border: 3px solid currentColor; box-shadow: 0 40px 90px rgba(0,0,0,0.6); }
      .score .si { font-weight: 900; font-size: 96px; line-height: 1; }
      .score .sl { margin-top: 16px; font-weight: 850; font-size: 46px; color: #fff; letter-spacing: -0.02em; line-height: 1.1; }
      .three { position: absolute; display: flex; gap: 26px; opacity: 0; }
      .three .n { width: 200px; height: 200px; border-radius: 28px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 120px;
        color: #0b0c10; background: var(--lime); box-shadow: 0 0 40px rgba(200,255,77,0.45); }
      #title { position: absolute; left: 60px; top: 300px; width: 960px; }
      #title .k { font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.16em; color: var(--lime); margin-bottom: 18px; }
      #title .t { font-weight: 900; font-size: 112px; letter-spacing: -0.045em; line-height: 0.96; color: #fff; text-transform: uppercase; text-shadow: 0 10px 40px rgba(0,0,0,0.7); }
      #title .t em { font-style: normal; color: var(--lime); }
      #title .s { margin-top: 22px; font-weight: 700; font-size: 38px; color: #e8e9ee; text-shadow: 0 4px 20px rgba(0,0,0,0.7); }
      /* end card */
      #end { position: absolute; inset: 0; opacity: 0; }
      #end .dim { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(5,6,10,0.72), rgba(5,6,10,0.95)); }
      .mark { position: absolute; left: 430px; top: 470px; width: 220px; height: 220px; border-radius: 52px; background: var(--lime);
        display: flex; align-items: flex-end; justify-content: center; gap: 8px; padding-bottom: 50px; box-shadow: 0 0 80px rgba(200,255,77,0.45); }
      .mark .one { font-weight: 900; font-size: 154px; line-height: 0.73; color: #0b0c10; letter-spacing: -0.06em; }
      .mark .cur { width: 42px; height: 16px; border-radius: 3px; background: #0b0c10; }
      .etitle { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900; letter-spacing: -0.05em; line-height: 0.95; white-space: nowrap; }
      .cta { position: absolute; display: inline-flex; align-items: center; gap: 16px; padding: 22px 36px; border-radius: 999px; background: var(--lime);
        color: #0b0c10; font-weight: 850; font-size: 42px; letter-spacing: -0.01em; white-space: nowrap; }
      .fontwarm { position: absolute; left: -9999px; top: 0; }
      /* #12: the call screen, the safe-phrase card */
      .call { position: absolute; left: 280px; top: 330px; width: 520px; height: 700px; border-radius: 56px; opacity: 0;
        background: linear-gradient(180deg, #1d2333 0%, #0b0d14 100%); box-shadow: 0 50px 110px rgba(0,0,0,0.7), 0 0 0 12px #111318, 0 0 0 14px rgba(255,255,255,0.12); }
      .call .cl { position: absolute; left: 0; right: 0; top: 70px; text-align: center; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.14em; color: #9aa0b4; }
      .call .cn { position: absolute; left: 0; right: 0; top: 120px; text-align: center; font-weight: 850; font-size: 72px; letter-spacing: -0.02em; color: #fff; }
      .call .cs { position: absolute; left: 0; right: 0; top: 214px; text-align: center; font-weight: 600; font-size: 28px; color: #9aa0b4; }
      .call .av { position: absolute; left: 190px; top: 300px; width: 140px; height: 140px; border-radius: 50%; background: #3a4258; display: flex; align-items: center;
        justify-content: center; font-weight: 900; font-size: 64px; color: #e8e9ee; }
      .call .pulse { position: absolute; left: 190px; top: 300px; width: 140px; height: 140px; border-radius: 50%; border: 4px solid rgba(200,255,77,0.7); opacity: 0; }
      .call .bt { position: absolute; top: 540px; width: 110px; height: 110px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: 26px; color: #fff; }
      .call .no { left: 90px; background: #d42a23; } .call .yes { right: 90px; background: #1e9443; }
      .note { position: absolute; left: 120px; top: 380px; width: 840px; padding: 46px 52px 44px; border-radius: 20px; background: #fbf6e7; opacity: 0;
        box-shadow: 0 40px 90px rgba(0,0,0,0.6); transform: rotate(-2deg); }
      .note .nk { font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.14em; color: #b4532a; }
      .note .nw { font-family: Georgia, serif; font-style: italic; font-weight: 700; font-size: 124px; color: #1b1c22; margin: 18px 0 10px; letter-spacing: -0.01em; }
      .note .ns { font-weight: 700; font-size: 30px; color: #6b6e78; }
      .row { position: absolute; display: flex; align-items: center; gap: 22px; padding: 22px 30px; border-radius: 20px; background: rgba(8,9,14,0.86);
        border: 2px solid rgba(255,255,255,0.16); font-weight: 850; font-size: 50px; color: #fff; opacity: 0; white-space: nowrap; }
      .row .bx { width: 54px; height: 54px; border-radius: 12px; border: 4px solid var(--lime); display: flex; align-items: center; justify-content: center;
        font-size: 38px; color: var(--lime); }
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
        <div id="tshade" style="position:absolute;left:0;top:0;width:1080px;height:980px;opacity:0;background:linear-gradient(180deg,rgba(4,5,10,0.92) 0%,rgba(4,5,10,0.8) 38%,rgba(4,5,10,0) 100%)"></div>
        <div id="title"><div class="k">● LISTEN CLOSELY</div><div class="t">This voice<br />isn't <em>me</em>.</div></div>
        <div id="fx"></div>
        %LABELS%
        
        <div class="grain" id="grain"></div>
        <div class="progress" id="prog" style="background:var(--lime)"></div>
        <div class="tag2" id="tag"><span class="dot"></span>AI EXPLAINED · PROTECT YOURSELF</div>
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
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span><span style="font-family:Georgia">Aa</span></div>
      </div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%, HND = %H%;
      const SH = %SHOTSJS%;
      const GEO = %GEO%, PHONE = %PHONE%, LOGOS = %LOGOS%;
      const WS = %WS%, WE = %WE%;
      const w = (k) => WS[k], we = (k) => WE[k];
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out";
      const fx = (id) => "#fx-" + id, cam = (id) => "#cam-" + id;
      const T0 = Object.fromEntries(SH.map((s) => [s.id, s.t0])), T1 = Object.fromEntries(SH.map((s) => [s.id, s.t1]));
      const KIND = Object.fromEntries(SH.map((s) => [s.id, s.k]));
      const A = (id) => T0[id], B = (id) => T1[id];
      const FXR = $("#fx");
      const el = (tag, cls, css, html, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css;
        if (html !== undefined) e.innerHTML = html; (parent || FXR).appendChild(e); return e; };

      // ---------- shots: visibility and default camera ----------
      const CUSTOM_CAM = new Set(Object.keys(GEO).concat(Object.keys(PHONE)));
      SH.forEach((s, i) => {
        tl.set(fx(s.id), { opacity: i === 0 ? 1 : 0 }, 0);
        const a = Math.max(0, s.t0 - HND), b = s.t1 + HND;
        if (CUSTOM_CAM.has(s.id)) return;
        tl.fromTo(cam(s.id), { scale: 1 }, { scale: 1.06, duration: b - a, ease: "none" }, a);
      });
      const flash = (t, a, d, c) => { tl.set("#flash", { background: c || "#fff" }, t); tl.fromTo("#flash", { opacity: a }, { opacity: 0, duration: d || 0.35, ease: "power2.out", immediateRender: false }, t); };
      const cardIn = (id, t) => { const c = document.querySelectorAll("#cam-" + id + " .card, #cam-" + id + " .phone");
        tl.fromTo(c, { opacity: 0, scale: 0.9, y: 50 }, { opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.6)", stagger: 0.1 }, t); };
      const swap = (a, b, T) => { tl.set(fx(b), { opacity: 1 }, T); tl.set(fx(a), { opacity: 0 }, T); };
      const TR = {
        whip(a, b, T) { tl.fromTo(fx(b), { opacity: 1, x: 1080, filter: "blur(24px)" }, { x: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17);
          tl.to(fx(a), { x: -760, filter: "blur(24px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17); tl.set(fx(a), { opacity: 0 }, T + 0.15); },
        slideup(a, b, T) { tl.fromTo(fx(b), { opacity: 1, y: 1920, filter: "blur(22px)" }, { y: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17);
          tl.to(fx(a), { y: -1100, filter: "blur(22px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17); tl.set(fx(a), { opacity: 0 }, T + 0.15); },
        zoom(a, b, T) { tl.to(fx(a), { scale: 1.4, filter: "blur(18px)", opacity: 0, duration: 0.26, ease: "power2.in" }, T - 0.16);
          tl.fromTo(fx(b), { opacity: 0, scale: 0.86, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: E }, T - 0.1); flash(T - 0.02, 0.22, 0.3); },
        flash(a, b, T, c) { swap(a, b, T); flash(T, 0.6, 0.42, c); },
        cut(a, b, T) { swap(a, b, T); tl.fromTo(fx(b), { scale: 1.08 }, { scale: 1, duration: 0.35, ease: E, immediateRender: false }, T); },
        dip(a, b, T) { tl.to("#black", { opacity: 1, duration: 0.14, ease: "power1.in" }, T - 0.14); swap(a, b, T); tl.to("#black", { opacity: 0, duration: 0.28, ease: "power1.out" }, T); },
        card(a, b, T) { tl.fromTo(fx(b), { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out" }, T - 0.12); tl.set(fx(a), { opacity: 0 }, T + 0.12); cardIn(b, T - 0.05); },
        fade(a, b, T) { tl.fromTo(fx(b), { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.inOut" }, T - 0.25); tl.set(fx(a), { opacity: 0 }, T + 0.26); },
        scratch(a, b, T) { swap(a, b, T); flash(T, 0.85, 0.25, "#ffffff");
          for (let k = 0; k < 7; k++) tl.set(fx(b), { x: (k % 2 ? -1 : 1) * 26 * (1 - k / 7), y: (k % 3 - 1) * 10 }, T + k * 0.035); tl.set(fx(b), { x: 0, y: 0 }, T + 0.25); },
      };
      const CUTS = %CUTS%;
      CUTS.forEach(([a, b, k, c]) => TR[k](a, b, T0[b], c));
      tl.fromTo("#flash", { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);

      // ---------- helpers ----------
      const show = (sel, t0, t1, from) => { tl.fromTo(sel, Object.assign({ opacity: 0, y: 14 }, from || {}), { opacity: 1, y: 0, x: 0, duration: 0.3, ease: E }, t0);
        tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const pop = (sel, t0, t1, sc) => { tl.fromTo(sel, { opacity: 0, scale: sc || 0.4 }, { opacity: 1, scale: 1, duration: 0.38, ease: "back.out(2.2)" }, t0);
        if (t1) tl.to(sel, { opacity: 0, duration: 0.16 }, t1); };
      const punch = (id, t, s) => { tl.fromTo(fx(id), { scale: 1 }, { scale: 1 + (s || 0.05), duration: 0.12, ease: "power2.out", immediateRender: false }, t);
        tl.to(fx(id), { scale: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.12); };
      const chip = (txt, x, y, col, t0, t1, from) => { const c = el("div", "chip", `left:${x}px;top:${y}px;color:${col || "var(--lime)"}`, `<span class="sw"></span>${txt}`);
        show(c, t0, t1, from || { x: -24, y: 0 }); return c; };
      const big = (txt, x, y, fs, col, t0, t1) => { const b = el("div", "big", `left:${x}px;top:${y}px;font-size:${fs}px;color:${col || "#fff"}`, txt);
        tl.fromTo(b, { opacity: 0, scale: 1.35 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, t0); tl.to(b, { opacity: 0, duration: 0.14 }, t1); return b; };
      // an official logo on a white tile (a dashed "needed" tile if its file hasn't arrived)
      const logo = (code, x, y, wd, ht, label, parent) => { const L = LOGOS[code] || {};
        const d = el("div", "logo" + (L.have ? "" : " need"), `left:${x}px;top:${y}px;width:${wd}px;height:${ht}px;` + (L.bg ? `background:${L.bg}` : ""),
          L.have ? `<img src="assets/logos/${code}.png" alt="" />` : `LOGO NEEDED<br/>${code} · ${L.name || ""}`, parent);
        if (label) el("div", "ln", "", label, d);
        el("div", "ok", "", "✓", d); return d; };

      // ---------- documents: the camera finds each highlighted line on its word ----------
      const CAMEND = {};
      const docCam = (id) => { const g = GEO[id]; const a = Math.max(0, T0[id] - HND), b = T1[id] + HND;
        const CX = 540, CY = 760;
        const kf = (S, px, py) => { let x = CX - S * px, y = CY - S * py;
          x = Math.min(0, Math.max(1080 * (1 - S), x)); y = Math.min(0, Math.max(1920 * (1 - S), y)); return { scale: S, x, y }; };
        tl.set(cam(id), { transformOrigin: "0px 0px" }, 0);
        const zs = (ww) => Math.min(g.zmax || 1.5, Math.max(1.08, 960 / (ww + 60)));
        let prev = kf(1, CX, CY), tPrev = a;
        tl.set(cam(id), prev, a);
        g.hl.forEach(([t, hx, hy, ww], k) => { const S = zs(ww); const k1 = kf(S, hx, hy); const t0 = Math.max(tPrev + 0.05, t - 0.45);
          tl.to(cam(id), Object.assign({}, k1, { duration: Math.max(0.3, t + 0.2 - t0), ease: "power2.inOut" }), t0); tPrev = t + 0.2; prev = k1; });
        const last = kf(prev.scale * 1.035, (CX - prev.x) / prev.scale, (CY - prev.y) / prev.scale); CAMEND[id] = last;
        if (b > tPrev + 0.05) tl.to(cam(id), Object.assign({}, last, { duration: b - tPrev, ease: "none" }), tPrev); };
      Object.keys(GEO).forEach((id) => { const g = GEO[id];
        g.sweeps.forEach(([hid, t, d]) => tl.to("#" + hid, { scaleX: 1, duration: d, ease: "power2.inOut" }, t));
        if (KIND[id] === "PAGE") docCam(id); });
      // a badge for the page's owner: the logo tile overlapping the card's top-right corner
      const badge = (id, code, label) => { const g = GEO[id]; const wd = 220, ht = 110;
        const d = logo(code, 820, 296, 200, 100, null);
        pop(d, A(id) + 0.18, B(id) - 0.08, 0.6); return d; };

      // ---------- phones: the steps on the right, the switch going off ----------
      const steps = (id, code, items, offAt, ringAt, offTxt) => { const P = PHONE[id];
        const L = logo(code, 580, 310, 300, 130); pop(L, A(id) + 0.1, B(id) - 0.08, 0.6);
        items.forEach(([k, txt, t], j) => { const s = el("div", "step", `left:580px;top:${490 + j * 120}px;white-space:normal;max-width:460px;font-size:32px`, `<span class="k">${k}</span>${txt}`);
          tl.fromTo(s, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.28, ease: E }, t); tl.set(s, { className: "step on" }, t);
          if (j + 1 < items.length) tl.set(s, { className: "step" }, items[j + 1][2]); tl.to(s, { opacity: 0, duration: 0.15 }, B(id) - 0.1); });
        if (offAt) { const o = el("div", "off", `left:580px;top:${490 + items.length * 120 + 20}px`, offTxt || "OFF ✓"); pop(o, offAt, B(id) - 0.1, 0.5); }
        if (ringAt && P.tog) { const [x, y, rw, rh] = P.tog; const r = el("div", "ring", `left:${x - rw / 2}px;top:${y - rh / 2}px;width:${rw}px;height:${rh}px`, "", $("#cam-" + id));
          tl.fromTo(r, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, ringAt); tl.to(r, { opacity: 0, duration: 0.15 }, B(id) - 0.1); } };
      const phoneCam = (id, tz, S) => { const P = PHONE[id]; const a = Math.max(0, T0[id] - HND), b = T1[id] + HND;
        tl.set(cam(id), { transformOrigin: "0px 0px" }, 0);
        tl.fromTo(cam(id), { scale: 1, x: 0, y: 0 }, { scale: 1.02, x: -10, y: -6, duration: Math.max(0.3, (tz || b) - a - 0.4), ease: "none" }, a);
        if (tz && P.tog) { const [x, y] = P.tog; const s = S || 1.35; const tx = Math.min(0, Math.max(1080 * (1 - s), 300 - s * x)), ty = Math.min(0, Math.max(1920 * (1 - s), 760 - s * y));
          tl.to(cam(id), { scale: s, x: tx, y: ty, duration: 0.45, ease: "power2.inOut" }, tz - 0.4);
          tl.to(cam(id), { scale: s * 1.02, duration: Math.max(0.2, b - tz), ease: "none" }, tz + 0.05); } };

      // ===================================================== the shots =====================================================
      %FXJS%

      // ---------- end card ----------
      const TE = A("%ENDID%");
      tl.fromTo("#end", { opacity: 0 }, { opacity: 1, duration: 0.5 }, TE);
      tl.fromTo("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, TE + 0.15);
      tl.fromTo(["#ename", "#ehandle"], { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.45, ease: E, stagger: 0.12 }, TE + 0.4);
      tl.fromTo("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, TE + 0.85);
      tl.to("#fol", { scale: 1.05, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, TE + 1.4);
      tl.to("#mark", { boxShadow: "0 0 140px rgba(200,255,77,0.8)", duration: 0.9, yoyo: true, repeat: 1, ease: "sine.inOut" }, TE + 1.1);

      // ---------- global UI ----------
      %LABJS%.forEach(([sel, a, b]) => show(sel, a, b, { x: -20, y: 0 }));
      [].forEach(([sel, a, b]) => { tl.fromTo(sel, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, a); tl.to(sel, { opacity: 0, duration: 0.25 }, b); });
      tl.set(["#bm", "#tag"], { opacity: 1 }, 0); tl.to(["#bm", "#tag"], { opacity: 0, duration: 0.4 }, TE - 0.2);
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      tl.to([".botshade", ".topshade"], { opacity: 0, duration: 0.5 }, TE);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);
      tl.fromTo("#black", { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, DUR - 0.45);

      // ---------- captions: sentence case, the spoken word lights up ----------
      const CAPS = (window.CAPS || []).map((c) => ({ t0: c.t0, t1: c.t1, w: c.w.map((x) => ({ d: x.d, s: x.s, e: x.e, em: x.emph })) })), NOCAP = %NOCAP%;
      const capsRoot = $("#caps");
      CAPS.forEach((ch) => { if (NOCAP.some(([a, b]) => ch.t0 < b && ch.t1 > a)) return;
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

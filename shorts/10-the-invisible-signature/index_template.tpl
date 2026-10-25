<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <script src="assets/js/d3.min.js"></script>
    <script src="assets/js/land.js"></script>
    <script src="captions.js"></script>
    <link rel="stylesheet" href="assets/base.css" />
    <style>
      @font-face { font-family: "Hand"; src: url("assets/fonts/caveat-700.woff2") format("woff2"); font-weight: 700; }
      .shot { position: absolute; inset: 0; overflow: hidden; }
      .fx, .cam { position: absolute; inset: 0; transform-origin: 50% 45%; }
      .vid { position: absolute; object-fit: cover; }
      .bd { position: absolute; inset: 0; background-size: cover; background-position: center; }
      .card { position: absolute; overflow: hidden; border-radius: 24px; background: #fff;
        box-shadow: 0 40px 90px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08); }
      .card img { position: absolute; }
      .hl { position: absolute; mix-blend-mode: multiply; border-radius: 6px; transform-origin: 0 50%; transform: scaleX(0); background: rgba(200,255,77,0.75); }
      .gfx { position: absolute; inset: 0; }
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
      .src.q .sd { background: #7cc4ff; box-shadow: 0 0 10px #7cc4ff; }

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
      .cw.inl { font-size: 1.12em; }

      /* shot graphics */
      .chip { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.08em; padding: 14px 22px;
        border-radius: 14px; background: rgba(6,8,12,0.84); border: 2px solid currentColor; opacity: 0; white-space: nowrap; color: var(--lime); }
      .chip .sw { display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: currentColor; margin-right: 14px; vertical-align: 2px; box-shadow: 0 0 12px currentColor; }
      .pin { position: absolute; left: 0; top: 0; opacity: 0; color: var(--lime); }
      .pin .pl { position: absolute; left: 26px; top: -30px; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.08em; white-space: nowrap;
        padding: 10px 16px; border-radius: 12px; background: rgba(6,8,12,0.82); border: 2px solid currentColor; }
      .pin .pd { position: absolute; left: -12px; top: -12px; width: 24px; height: 24px; border-radius: 50%; background: currentColor; box-shadow: 0 0 18px currentColor; }
      .sig { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; pointer-events: none; }
      .sig path { fill: none; stroke: #c8ff4d; stroke-linecap: round; stroke-linejoin: round; }
      .sig .glow { stroke: rgba(200,255,77,0.45); filter: blur(10px); }
      .stamp { position: absolute; font-weight: 900; font-size: 96px; letter-spacing: 0.01em; padding: 8px 30px; border: 10px solid currentColor; border-radius: 18px;
        color: #e0322b; opacity: 0; white-space: nowrap; mix-blend-mode: multiply; }
      .stamp.ghost { color: rgba(255,255,255,0.9); mix-blend-mode: normal; border-style: dashed; background: rgba(6,8,12,0.35); }

      /* s01 / s29: the claim */
      #claim { position: absolute; left: 60px; top: 300px; width: 960px; }
      #claim .k { font-family: "Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.16em; color: #c8ff4d; margin-bottom: 18px; }
      #claim .t { font-weight: 900; font-size: 104px; letter-spacing: -0.045em; line-height: 0.98; color: #fff; text-transform: uppercase;
        text-shadow: 0 10px 40px rgba(0,0,0,0.7); }
      #claim .t em { font-style: normal; color: #c8ff4d; text-shadow: 0 0 40px rgba(200,255,77,0.55), 0 10px 40px rgba(0,0,0,0.7); }
      #eu { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      #euchip { position: absolute; left: 60px; top: 1080px; color: #ffd84a; }

      /* s04 / s05: the word slots */
      .slots { position: absolute; left: 70px; width: 940px; padding: 34px 40px; border-radius: 28px; background: rgba(8,9,14,0.82);
        border: 2px solid rgba(255,255,255,0.14); box-shadow: 0 40px 80px rgba(0,0,0,0.55); opacity: 0; }
      .slots .row { display: flex; align-items: center; gap: 18px; height: 112px; font-weight: 800; font-size: 58px; letter-spacing: -0.02em; color: #e8e9ee; }
      .slots .row + .row { margin-top: 14px; }
      .slot { position: relative; display: inline-flex; align-items: center; justify-content: center; min-width: 270px; height: 96px; padding: 0 26px;
        border-radius: 18px; background: #f3f1ea; color: #15161b; font-weight: 900; font-size: 60px; letter-spacing: 0.02em; box-shadow: inset 0 -6px 0 rgba(0,0,0,0.12); }
      .slot::after { content: ""; position: absolute; left: 0; right: 0; top: 50%; height: 2px; background: rgba(0,0,0,0.16); }
      .slot.lock { background: #c8ff4d; box-shadow: 0 0 34px rgba(200,255,77,0.65); }
      .slots .ok { font-size: 54px; color: #7ee787; opacity: 0; }
      .slots .coinm { width: 66px; height: 66px; border-radius: 50%; opacity: 0; flex: none;
        background: radial-gradient(circle at 35% 35%, #fff4c8, #e3b54a 45%, #8a6417 100%); box-shadow: 0 6px 18px rgba(0,0,0,0.5); }
      .slots.sm { padding: 18px 26px; }
      .slots.sm .row { height: 74px; font-size: 40px; gap: 14px; }
      .slots.sm .slot { min-width: 190px; height: 64px; font-size: 40px; border-radius: 12px; }

      /* meter */
      #meter { position: absolute; left: 70px; top: 1050px; width: 940px; opacity: 0; }
      #meter .ml { display: flex; justify-content: space-between; font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.12em; color: #c9ccd6; margin-bottom: 12px; }
      #meter .mb { position: relative; height: 34px; border-radius: 17px; background: rgba(255,255,255,0.12); border: 2px solid rgba(255,255,255,0.18); overflow: hidden; }
      #meter .mf { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; border-radius: 17px; transform-origin: 0 50%; transform: scaleX(0);
        background: linear-gradient(90deg, #7cc4ff, #c8ff4d); box-shadow: 0 0 22px rgba(200,255,77,0.7); }

      /* essay cards */
      .essay { position: absolute; border-radius: 22px; background: #f6f4ee; box-shadow: 0 40px 90px rgba(0,0,0,0.6); overflow: hidden; opacity: 0; }
      .essay .et { position: absolute; left: 44px; top: 40px; right: 44px; font-family: Georgia, serif; color: rgba(30,31,38,0.82); text-align: justify; }
      .essay .et span { border-radius: 4px; padding: 0 2px; }
      .essay .eh { font-family: "Mono", monospace; font-weight: 700; letter-spacing: 0.14em; color: #6b6e78; margin-bottom: 16px; }
      .kchip { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 34px; letter-spacing: 0.06em; padding: 14px 24px; border-radius: 16px;
        background: #15161b; color: #fff; border: 2px solid rgba(255,255,255,0.25); box-shadow: 0 16px 40px rgba(0,0,0,0.5); opacity: 0; white-space: nowrap; }
      .kchip b { color: #c8ff4d; font-weight: 700; }
      .vf { position: absolute; opacity: 0; }
      .vf i { position: absolute; width: 80px; height: 80px; border: 0 solid #fff; }

      /* quotes (Claude's help page) */
      .quote { position: absolute; left: 50px; top: 760px; width: 980px; padding: 40px 44px 36px; border-radius: 26px; background: rgba(250,247,240,0.97);
        box-shadow: 0 40px 90px rgba(0,0,0,0.6); }
      .quote .qk { font-family: "Mono", monospace; font-weight: 700; font-size: 23px; letter-spacing: 0.14em; color: #b4532a; margin-bottom: 20px; }
      .quote .qt { position: relative; z-index: 0; font-family: Georgia, serif; font-size: 56px; line-height: 1.28; color: rgba(27,28,34,0.55); }
      .quote .qt + .qt { margin-top: 22px; }
      .quote .qh { color: #1b1c22; background-image: linear-gradient(rgba(200,255,77,0.85), rgba(200,255,77,0.85)); background-repeat: no-repeat;
        background-position: 0 88%; background-size: 0% 78%; }
      .quote .qbig { font-family: "InterV", sans-serif; font-weight: 850; font-size: 72px; letter-spacing: -0.03em; line-height: 1.08; color: #1b1c22; }
      .quote .qa { margin-top: 24px; font-family: "Mono", monospace; font-weight: 700; font-size: 21px; letter-spacing: 0.1em; color: #6b6e78; }

      /* chart */
      #chart { position: absolute; left: 50px; top: 300px; width: 980px; padding: 30px 34px 26px; border-radius: 26px; background: rgba(8,10,16,0.9);
        border: 2px solid rgba(255,255,255,0.12); box-shadow: 0 40px 90px rgba(0,0,0,0.6); opacity: 0; }
      #chart .ct { font-weight: 850; font-size: 46px; letter-spacing: -0.02em; color: #fff; }
      #chart .cs { font-family: "Mono", monospace; font-weight: 700; font-size: 21px; letter-spacing: 0.1em; color: #9a9ca6; margin-top: 6px; margin-bottom: 18px; }
      #chart .cr { position: relative; height: 31px; }
      #chart .cn { position: absolute; left: 0; top: 2px; width: 190px; text-align: right; font-family: "Mono", monospace; font-weight: 700; font-size: 21px; color: #b8bcc8; }
      #chart .cb, #chart .cg { position: absolute; left: 210px; top: 5px; height: 21px; border-radius: 4px; transform-origin: 0 50%; transform: scaleX(0); }
      #chart .cb { background: #4f6f92; }
      #chart .cg { background: rgba(181,195,208,0.55); }
      #chart .cv { position: absolute; top: -4px; font-weight: 900; font-size: 34px; letter-spacing: -0.02em; opacity: 0; white-space: nowrap; }
      #chart .half { position: absolute; top: 120px; width: 0; border-left: 3px dashed rgba(255,255,255,0.55); opacity: 0; }
      #chart .halfl { position: absolute; top: 96px; font-family: "Mono", monospace; font-weight: 700; font-size: 20px; letter-spacing: 0.1em; color: #fff; opacity: 0; }

      /* globe */
      #globe { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      /* handwritten note */
      #note { position: absolute; left: 90px; top: 760px; width: 900px; height: 170px; border-radius: 10px; background: #fbf8ef; opacity: 0;
        box-shadow: 0 30px 70px rgba(0,0,0,0.55); transform: rotate(-3deg); overflow: hidden;
        background-image: repeating-linear-gradient(180deg, transparent 0, transparent 68px, rgba(80,120,200,0.25) 68px, rgba(80,120,200,0.25) 70px); }
      #note .nt { position: absolute; left: 36px; top: 34px; font-family: "Hand", cursive; font-weight: 700; font-size: 80px; color: #1d3f9e; white-space: nowrap;
        clip-path: inset(0 100% 0 0); }

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
      #inkw { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
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

        <!-- s01 + s29: the claim, the signature, Europe's stars -->
        <div id="claim"><div class="k">● NEW IN EUROPE · OCT 2026</div><div class="t">ChatGPT now <em>signs</em> its writing</div></div>
        <svg class="sig" id="sigHero" viewBox="0 0 1080 1920"></svg>
        <svg id="eu" viewBox="0 0 1080 1920"><g id="euStars"></g></svg>
        <!-- s04 / s05: tiny choices -->
        <div class="slots" id="slotsA" style="top:470px">
          <div class="row">It's a <span class="slot" id="slA1">BIG</span> day. <span class="ok" id="okA1">✓</span></div>
          <div class="row">Let's <span class="slot" id="slA2">START</span> now. <span class="ok" id="okA2">✓</span></div>
        </div>
        <div class="slots sm" id="slotsB" style="top:280px;left:110px;width:860px">
          <div class="row"><span class="coinm" id="cm1"></span>It's a <span class="slot" id="slB1">BIG</span> day.</div>
          <div class="row"><span class="coinm" id="cm2"></span>Let's <span class="slot" id="slB2">START</span> now.</div>
        </div>
        <!-- s06 -->
        <div class="chip" id="chKey" style="left:60px;top:1110px"><span class="sw"></span>THE COIN = A SECRET KEY</div>
        <svg class="sig" id="ringW" viewBox="0 0 1080 1920" style="opacity:0"><circle id="ringWc" cx="0" cy="0" r="90" fill="none" stroke="#c8ff4d" stroke-width="8"
          style="filter: drop-shadow(0 0 14px rgba(200,255,77,0.9))" /></svg>
        <!-- s07 / s08: the meter, the page of words -->
        <div class="essay" id="essayBig" style="left:90px;top:290px;width:900px;height:730px"><div class="et" id="essayBigT" style="font-size:23px;line-height:1.5"></div></div>
        <div id="meter"><div class="ml"><span>COULD BE CHANCE</span><span>SIGNATURE</span></div><div class="mb"><div class="mf" id="mfill"></div></div></div>
        <!-- s09 -->
        <svg class="sig" id="sigPen" viewBox="0 0 1080 1920"></svg>
        <!-- s11 / s12: copy, paste, screenshot -->
        <div id="copies"></div>
        <div class="kchip" id="kc1" style="left:110px;top:1080px"><b>⌘C</b> COPY</div>
        <div class="kchip" id="kc2" style="left:400px;top:1080px"><b>⌘V</b> PASTE</div>
        <div class="kchip" id="kc3" style="left:640px;top:1080px"><b>📷</b> SCREENSHOT</div>
        <div class="vf" id="vf" style="left:120px;top:330px;width:840px;height:700px"><i style="left:0;top:0;border-left-width:8px;border-top-width:8px"></i>
          <i style="right:0;top:0;border-right-width:8px;border-top-width:8px"></i><i style="left:0;bottom:0;border-left-width:8px;border-bottom-width:8px"></i>
          <i style="right:0;bottom:0;border-right-width:8px;border-bottom-width:8px"></i></div>
        <div class="essay" id="essayZ" style="left:60px;top:320px;width:960px;height:760px"><div class="et" id="essayZT" style="font-size:40px;line-height:1.55;left:54px;right:54px;top:50px"></div></div>
        <svg class="sig" id="sigZ" viewBox="0 0 1080 1920"></svg>
        <!-- s13 - s15 -->
        <div class="chip" id="chAct" style="left:60px;top:1110px;color:#ffd84a"><span class="sw"></span>EU AI ACT · ARTICLE 50</div>
        <svg class="sig" id="sigFlag" viewBox="0 0 1080 1920"></svg>
        <div class="pin" id="pinParis"><div class="pd"></div><div class="pl">PARIS · SIGNED</div></div>
        <svg class="sig" id="sigParis" viewBox="0 0 1080 1920"></svg>
        <div class="pin" id="pinLondon" style="color:#ffffff"><div class="pd"></div><div class="pl">LONDON</div></div>
        <svg class="sig" id="lineLondon" viewBox="0 0 1080 1920" style="opacity:0"><path d="M 250 1060 L 830 1060" stroke="#ffffff" stroke-width="6" stroke-dasharray="18 16" style="fill:none" /></svg>
        <!-- s17: the globe -->
        <canvas id="globe" width="1080" height="1920"></canvas>
        <div class="pin" id="pinUK"><div class="pd"></div><div class="pl">UK</div></div>
        <!-- s20: the chart -->
        <div id="chart"></div>
        <!-- s22 -->
        <svg class="sig" id="sigPhone" viewBox="0 0 1080 1920"></svg>
        <!-- s24 -->
        <div class="chip" id="chChecker" style="left:60px;top:1110px;color:#ff8a7a"><span class="sw"></span>CHATGPT'S CHECKER · RESEARCHERS ONLY</div>
        <!-- s26 / s27 -->
        <div class="stamp" id="stCheat" style="left:250px;top:930px;transform:rotate(-8deg)">CHEATED?</div>
        <div class="stamp ghost" id="stHuman" style="left:300px;top:900px;transform:rotate(6deg)">HUMAN?</div>
        <!-- s28 -->
        <div id="note"><div class="nt" id="noteT">Written with help from AI.</div></div>

        %LABELS%

        <svg id="inkw" viewBox="0 0 1080 1920"><path id="inkp" pathLength="1" d="M -200 2200 C 200 1500, 300 900, 700 600 S 1100 -100, 1300 -300"
          fill="none" stroke="#c8ff4d" stroke-width="900" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1" /></svg>
        <div class="grain" id="grain"></div>
        <div class="progress" id="prog" style="background:var(--lime)"></div>
        <div class="tag2" id="tag"><span class="dot"></span>AI EXPLAINED · REAL NEWS</div>
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
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span><span style="font-family:Georgia">Aa</span><span style="font-family:Hand;font-weight:700">Aa</span></div>
      </div>

      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%, HND = %H%;
      const SH = %SHOTSJS%;
      const GEO = %GEO%;
      const WS = %WS%, WE = %WE%;
      const CHART = %CHART%;
      %CONSTS%
      const w = (k) => WS[k], we = (k) => WE[k];
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out";
      const fx = (id) => "#fx-" + id, cam = (id) => "#cam-" + id;
      const T0 = Object.fromEntries(SH.map((s) => [s.id, s.t0])), T1 = Object.fromEntries(SH.map((s) => [s.id, s.t1]));
      const A = (id) => T0[id], B = (id) => T1[id];
      const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; };
      const el = (tag, cls, css, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css; (parent || $("#ui")).appendChild(e); return e; };
      let seed = 10; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
      const NS = "http://www.w3.org/2000/svg";

      // ---------- shots: visibility and default camera ----------
      const DOCS = ["s10", "s19", "s25"];
      const CUSTOM_CAM = new Set(DOCS.concat(["s06", "s22"]));
      SH.forEach((s, i) => {
        tl.set(fx(s.id), { opacity: i === 0 ? 1 : 0 }, 0);
        const a = Math.max(0, s.t0 - HND), b = s.t1 + HND;
        if (CUSTOM_CAM.has(s.id)) return;
        tl.fromTo(cam(s.id), { scale: 1 }, { scale: 1.07, duration: b - a, ease: "none" }, a);
      });
      const flash = (t, a, d, c) => { tl.set("#flash", { background: c || "#fff" }, t); tl.fromTo("#flash", { opacity: a }, { opacity: 0, duration: d || 0.35, ease: "power2.out", immediateRender: false }, t); };
      const cardIn = (id, t) => { const c = document.querySelectorAll("#cam-" + id + " .card");
        tl.fromTo(c, { opacity: 0, scale: 0.86, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.6)", stagger: 0.12 }, t); };
      const swap = (A, B, T) => { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T); };
      const TR = {
        whip(A, B, T) { tl.fromTo(fx(B), { opacity: 1, x: 1080, filter: "blur(22px)" }, { x: 0, filter: "blur(0px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16);
          tl.to(fx(A), { x: -760, filter: "blur(22px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16); tl.set(fx(A), { opacity: 0 }, T + 0.14); },
        slideup(A, B, T) { tl.fromTo(fx(B), { opacity: 1, y: 1920, filter: "blur(22px)" }, { y: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17);
          tl.to(fx(A), { y: -1100, filter: "blur(22px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17); tl.set(fx(A), { opacity: 0 }, T + 0.15); },
        zoom(A, B, T) { tl.to(fx(A), { scale: 1.45, filter: "blur(18px)", opacity: 0, duration: 0.26, ease: "power2.in" }, T - 0.16);
          tl.fromTo(fx(B), { opacity: 0, scale: 0.84, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: E }, T - 0.1); flash(T - 0.02, 0.25, 0.3); },
        flash(A, B, T, c) { swap(A, B, T); flash(T, 0.6, 0.42, c); },
        uv(A, B, T) { swap(A, B, T); flash(T, 0.75, 0.5, "#8a5cff"); tl.fromTo(fx(B), { scale: 1.1 }, { scale: 1, duration: 0.6, ease: E, immediateRender: false }, T); },
        light(A, B, T) { tl.to("#flash", { opacity: 1, duration: 0.14, ease: "power2.in", background: "#fffaf0" }, T - 0.14); swap(A, B, T);
          tl.to("#flash", { opacity: 0, duration: 0.6, ease: "power2.out" }, T); tl.fromTo(fx(B), { scale: 1.08 }, { scale: 1, duration: 0.7, ease: E, immediateRender: false }, T); },
        dip(A, B, T) { tl.to("#black", { opacity: 1, duration: 0.14, ease: "power1.in" }, T - 0.14); swap(A, B, T); tl.to("#black", { opacity: 0, duration: 0.28, ease: "power1.out" }, T); },
        card(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out" }, T - 0.12); tl.set(fx(A), { opacity: 0 }, T + 0.12); cardIn(B, T - 0.05); },
        fade(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.inOut" }, T - 0.25); tl.set(fx(A), { opacity: 0 }, T + 0.26); },
        // a lime ink stroke sweeps over A, B is underneath when it clears
        ink(A, B, T) { tl.set("#inkw", { opacity: 1 }, T - 0.2); tl.fromTo("#inkp", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.2, ease: "power2.in", immediateRender: false }, T - 0.2);
          swap(A, B, T); tl.to("#inkp", { strokeDashoffset: -1, duration: 0.26, ease: "power2.out" }, T + 0.02); tl.set("#inkw", { opacity: 0 }, T + 0.3);
          tl.fromTo(fx(B), { scale: 1.06 }, { scale: 1, duration: 0.5, ease: E, immediateRender: false }, T); },
      };
      const CUTS = [["s01", "s02", "zoom"], ["s02", "s03", "uv"], ["s03", "s04", "whip"], ["s04", "s05", "ink"], ["s05", "s06", "zoom"],
        ["s06", "s07", "dip"], ["s07", "s08", "card"], ["s08", "s09", "ink"], ["s09", "s10", "card"], ["s10", "s11", "slideup"],
        ["s11", "s12", "zoom"], ["s12", "s13", "whip"], ["s13", "s14", "whip"], ["s14", "s15", "slideup"], ["s15", "s16", "card"],
        ["s16", "s17", "zoom"], ["s17", "s18", "dip"], ["s18", "s19", "card"], ["s19", "s20", "slideup"], ["s20", "s21", "card"],
        ["s21", "s22", "ink"], ["s22", "s23", "card"], ["s23", "s24", "dip"], ["s24", "s25", "card"], ["s25", "s26", "whip"],
        ["s26", "s27", "flash", "#ff6b6b"], ["s27", "s28", "light"], ["s28", "s29", "ink"], ["s29", "s30", "fade"]];
      CUTS.forEach(([a, b, k, c]) => TR[k](a, b, T0[b], c));
      tl.fromTo("#flash", { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
      tl.set("#inkw", { opacity: 0 }, 0);

      // ---------- helpers ----------
      const show = (sel, t0, t1, from) => { tl.fromTo(sel, Object.assign({ opacity: 0, y: 14 }, from || {}), { opacity: 1, y: 0, x: 0, duration: 0.3, ease: E }, t0);
        tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const punch = (id, t, s) => { tl.fromTo(fx(id), { scale: 1 }, { scale: 1 + (s || 0.06), duration: 0.12, ease: "power2.out", immediateRender: false }, t);
        tl.to(fx(id), { scale: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.12); };
      const shake = (id, t, a, n) => { for (let k = 0; k < (n || 6); k++) tl.set(fx(id), { x: (k % 2 ? -1 : 1) * a * (1 - k / (n || 6)), y: (k % 3 - 1) * a * 0.5 }, t + k * 0.04); tl.set(fx(id), { x: 0, y: 0 }, t + (n || 6) * 0.04); };
      const TEXTAT = []; const textAt = (sel, steps) => TEXTAT.push([$(sel), steps]);
      tl.fromTo({ v: 0 }, { v: 0 }, { v: 1, duration: DUR, ease: "none", onUpdate() { const t = tl.time();
        TEXTAT.forEach(([e, st]) => { let txt = st[0][1]; st.forEach(([a, x]) => { if (t >= a) txt = x; }); if (e.textContent !== txt) e.textContent = txt; }); } }, 0);
      const docCam = (id) => { const g = GEO[id]; const hls = g[6] || []; const a = Math.max(0, T0[id] - HND), b = T1[id] + HND;
        const kf = (S, px, py) => { let y = 740 - S * py; const dy = 300 - (y + S * g[1]); if (dy > 0 && dy <= 160) y += dy; return { scale: S, x: 540 - S * px, y }; };
        tl.set(cam(id), { transformOrigin: "0px 0px" }, 0);
        const zs = (ww) => Math.max(1.05, Math.min(1.6, 880 / (ww + 80)));
        const [t, hx, hy, ww] = hls[0]; const end = Math.max(a + 0.35, t + 0.25);
        tl.fromTo(cam(id), kf(1, 540, 740), Object.assign(kf(zs(ww), hx, hy), { duration: end - a, ease: "power2.inOut" }), a);
        if (b > end + 0.05) tl.to(cam(id), Object.assign(kf(zs(ww) * 1.04, hx, hy), { duration: b - end, ease: "none" }), end); };
      // a quote from Claude's help page, set large; its highlight sweeps on the spoken word
      const quote = (host, kicker, html, t, tHl, foot) => { const q = el("div", "quote", "", $(host));
        q.innerHTML = `<div class="qk">${kicker}</div>${html}` + (foot ? `<div class="qa">${foot}</div>` : "");
        tl.fromTo(q, { opacity: 0, yPercent: -50, y: 50, rotation: -1.5 }, { opacity: 1, yPercent: -50, y: 0, rotation: -0.6, duration: 0.35, ease: "back.out(1.4)" }, t);
        q.querySelectorAll(".qh").forEach((h, k) => { tl.to(h, { backgroundSize: "100% 78%", color: "#000", duration: 0.45, ease: "power2.inOut" }, tHl + k * 0.2); });
        return q; };

      // ---------- signatures ----------
      // A signature of my own: a run of loops (a prolate trochoid) with a tall first loop, slanted, then an underline flourish.
      const sigD = (x0, y0, W, Hh, sd, loops) => { const L = loops || 6, P = Math.PI * 2 * L, pts = []; let s = sd || 1;
        for (let i = 0; i <= L * 36; i++) { const t = (i / (L * 36)) * P, u = t / P;
          let amp = Hh * 0.5 * (0.5 + 0.5 * Math.sin(u * Math.PI)) * (1 + 0.22 * Math.sin(1.7 * t + s)); if (t < Math.PI * 2) amp *= 1.6;
          const x = x0 + W * 0.82 * u - amp * 0.42 * Math.sin(t) + amp * 0.25 * (1 - Math.cos(t)) * 0.4;
          const y = y0 - amp * Math.cos(t) * 0.92 + Hh * 0.12 * u - amp * 0.35 * Math.sin(t) * 0.3; pts.push([x, y]); }
        const [lx, ly] = pts[pts.length - 1];
        let d = "M " + pts.map((p) => p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" L ");
        d += ` C ${(lx + W * 0.08).toFixed(1)} ${(ly + Hh * 0.5).toFixed(1)}, ${(x0 - W * 0.1).toFixed(1)} ${(y0 + Hh * 0.75).toFixed(1)}, ${(x0 + W * 0.05).toFixed(1)} ${(y0 + Hh * 0.62).toFixed(1)}`;
        d += ` S ${(x0 + W * 0.7).toFixed(1)} ${(y0 + Hh * 0.5).toFixed(1)}, ${(x0 + W * 1.02).toFixed(1)} ${(y0 + Hh * 0.42).toFixed(1)}`;
        return d; };
      const makeSig = (svgSel, x0, y0, W, Hh, sd, sw, rot) => { const svg = $(svgSel); const g = document.createElementNS(NS, "g");
        if (rot) g.setAttribute("transform", `rotate(${rot} ${x0 + W / 2} ${y0})`);
        const d = sigD(x0, y0, W, Hh, sd);
        [["glow", sw * 2.6], ["", sw]].forEach(([c, wdt]) => { const p = document.createElementNS(NS, "path"); p.setAttribute("d", d); p.setAttribute("pathLength", "1");
          p.setAttribute("stroke-width", wdt); if (c) p.setAttribute("class", c); p.style.strokeDasharray = 1; p.style.strokeDashoffset = 1; p.style.opacity = 0; g.appendChild(p); });
        svg.appendChild(g); return g.querySelectorAll("path"); };
      // round caps leave a dot before a stroke draws on: each signature starts hidden (inline style) until its stroke starts.
      // (no zero-length sets at 0 s: they revert when a renderer seeks back to 0)
      const drawSig = (paths, t, d, ease) => { tl.set(paths, { opacity: 1 }, t);
        tl.fromTo(paths, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d, ease: ease || "power1.inOut", immediateRender: false }, t); };

      // ---------- s01: the claim on frame one ----------
      const hero = makeSig("#sigHero", 200, 760, 640, 190, 1.3, 9);
      tl.set("#claim", { opacity: 1 }, 0);
      // already half-written on frame one
      tl.fromTo(hero, { strokeDashoffset: 0.55, opacity: 1 }, { strokeDashoffset: 0, duration: Math.max(0.6, w(8)), ease: "power1.inOut" }, 0);
      (function () { const g = $("#euStars"); for (let k = 0; k < 12; k++) { const a = (k / 12) * Math.PI * 2;
          const s = document.createElementNS(NS, "path"); const cx = 540 + Math.sin(a) * 300, cy = 900 - Math.cos(a) * 270; let p = "";
          for (let j = 0; j < 10; j++) { const r = j % 2 ? 11 : 26, b = (j / 10) * Math.PI * 2; p += (j ? "L" : "M") + (cx + Math.sin(b) * r).toFixed(1) + " " + (cy - Math.cos(b) * r).toFixed(1) + " "; }
          s.setAttribute("d", p + "Z"); s.setAttribute("fill", "#ffd84a"); s.style.filter = "drop-shadow(0 0 10px rgba(255,216,74,0.8))"; s.id = "st" + k; g.appendChild(s);
          tl.fromTo(s, { opacity: 0, scale: 0, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, w(8) + k * 0.03); } })();
      tl.set("#eu", { opacity: 1 }, w(8) - 0.01);
      tl.to(["#claim", "#eu"], { opacity: 0, duration: 0.15 }, B("s01") - 0.12);
      tl.to(hero, { opacity: 0, duration: 0.15 }, B("s01") - 0.12);
      tl.fromTo("#euStars", { rotation: 0, transformOrigin: "540px 900px" }, { rotation: 30, duration: B("s01") - w(8) + 0.3, ease: "none" }, w(8));

      // ---------- s02: never SEE it ----------
      punch("s02", w(13), 0.12);

      // ---------- s04 / s05: tiny choices, then the coin decides ----------
      (function () { tl.fromTo("#slotsA", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.5)" }, A("s04") + 0.02);
        tl.to("#slotsA", { opacity: 0, duration: 0.15 }, B("s04") - 0.12);
        const flip = (sel, t) => { tl.to(sel, { rotationX: 90, duration: 0.07, ease: "power2.in" }, t - 0.07); tl.to(sel, { rotationX: 0, duration: 0.1, ease: "power2.out" }, t); };
        textAt("#slA1", [[0, "BIG"], [w(24), "LARGE"], [w(28), "BIG"], [w(28) + 0.32, "LARGE"], [w(29) + 0.1, "BIG"], [w(30), "LARGE"]]);
        textAt("#slA2", [[0, "START"], [w(27), "BEGIN"], [w(28) + 0.16, "START"], [w(29), "BEGIN"], [w(29) + 0.26, "START"], [w(30) + 0.14, "BEGIN"]]);
        [w(24), w(28), w(28) + 0.32, w(29) + 0.1, w(30)].forEach((t) => flip("#slA1", t));
        [w(27), w(28) + 0.16, w(29), w(29) + 0.26, w(30) + 0.14].forEach((t) => flip("#slA2", t));
        tl.set("#slA2", { opacity: 0.35 }, A("s04")); tl.set("#slA2", { opacity: 1 }, w(25) - 0.05);
        tl.fromTo(["#okA1", "#okA2"], { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)", stagger: 0.1 }, w(30) + 0.05);
        // s05: the coin picks
        tl.fromTo("#slotsB", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, A("s05") + 0.05);
        tl.to("#slotsB", { opacity: 0, duration: 0.15 }, B("s05") - 0.12);
        textAt("#slB1", [[0, "BIG"], [A("s05") + 0.2, "LARGE"], [A("s05") + 0.36, "BIG"], [A("s05") + 0.52, "LARGE"], [w(37), "LARGE"]]);
        textAt("#slB2", [[0, "START"], [A("s05") + 0.28, "BEGIN"], [A("s05") + 0.44, "START"], [A("s05") + 0.6, "BEGIN"], [w(40), "BEGIN"]]);
        [[1, w(37)], [2, w(40)]].forEach(([k, t]) => { tl.fromTo("#cm" + k, { opacity: 0, rotationY: 0, scale: 0.4 }, { opacity: 1, rotationY: 540, scale: 1, duration: 0.4, ease: "power2.out" }, t - 0.35);
          tl.set("#slB" + k, { backgroundColor: "#c8ff4d", boxShadow: "0 0 34px rgba(200,255,77,0.65)" }, t); tl.fromTo("#slB" + k, { scale: 1.2 }, { scale: 1, duration: 0.3, ease: "back.out(2.5)", immediateRender: false }, t); });
        tl.set(["#slB1", "#slB2"], { backgroundColor: "#f3f1ea", boxShadow: "inset 0 -6px 0 rgba(0,0,0,0.12)" }, 0); })();

      // ---------- s06: only the company knows how it's loaded ----------
      (function () { const a = A("s06") - HND, b = B("s06") + HND;
        tl.fromTo(cam("s06"), { scale: 1.04 }, { scale: 1.12, duration: b - a, ease: "none" }, a);
        show("#chKey", A("s06") + 0.3, B("s06") - 0.1, { x: -20 });
        const r = { v: 0 }; tl.set("#ringW", { opacity: 0 }, 0);
        tl.fromTo("#ringW", { opacity: 0 }, { opacity: 1, duration: 0.15 }, w(48) - 0.05); tl.to("#ringW", { opacity: 0, duration: 0.15 }, B("s06") - 0.08);
        tl.fromTo("#ringWc", { attr: { r: 160 } }, { attr: { r: 84 }, duration: 0.35, ease: "back.out(2)", immediateRender: false }, w(48) - 0.05);
        tl.fromTo(r, { v: 0 }, { v: 1, duration: b - a, ease: "none", onUpdate() { const x = WEIGHT[0][0] + (WEIGHT[1][0] - WEIGHT[0][0]) * r.v, y = WEIGHT[0][1] + (WEIGHT[1][1] - WEIGHT[0][1]) * r.v;
          $("#ringWc").setAttribute("cx", x); $("#ringWc").setAttribute("cy", y); } }, a); })();

      // ---------- s07 / s08: one word proves nothing; hundreds do ----------
      const ESSAY = "Every Saturday the market wakes before the town does. Long before the first customer, the fish man is shouting at his ice, the baker is stacking warm loaves into crooked towers, and a woman with silver rings is laying out lemons as if each one were a small prize. By eight the lanes are full. People come for bread and leave with flowers, come for coffee and stay for gossip, come alone and somehow walk home with a friend. Nobody plans it this way; it simply happens, week after week, in the same narrow street. The stalls change with the seasons. Spring brings radishes and nervous lambs on the farm stand. Summer is all strawberries and arguments about tomatoes. In autumn the apples arrive in wooden crates that smell of cellars and rain, and in winter the soup van parks at the corner with its windows fogged and its queue patient in the cold. What keeps people coming back is hard to name. It is not the prices, which are rarely cheap, and it is not convenience, because the car park is a mess. It may be the small rituals: the same nod from the same cheese seller, the dog that always waits by the honey, the old man who tells every stranger which pears are ripe today. A market, in the end, is a habit that a whole town shares, and habits like that are worth more than they cost.";
      const words = ESSAY.split(" "); const PICK = words.map(() => rnd() < 0.42);
      const fillEssay = (sel, n) => { $(sel).innerHTML = words.slice(0, n).map((x, i) => `<span data-i="${i}">${x}</span>`).join(" "); };
      fillEssay("#essayBigT", words.length);
      (function () { // s07: the meter, one word
        tl.fromTo("#meter", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, A("s07") + 0.15);
        tl.to("#meter", { opacity: 0, duration: 0.15 }, B("s08") - 0.12);
        tl.fromTo("#mfill", { scaleX: 0 }, { scaleX: 0.05, duration: 0.3, ease: E }, w(50));
        for (let k = 0; k < 6; k++) tl.set("#mfill", { scaleX: 0.04 + (k % 2) * 0.025 }, w(51) + k * 0.08);
        // s08: the page of words lights up, coin pick by coin pick
        tl.fromTo("#essayBig", { opacity: 0, y: 40, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.4)" }, A("s08") - 0.05);
        tl.to("#essayBig", { opacity: 0, duration: 0.15 }, B("s08") - 0.12);
        const spans = $("#essayBigT").querySelectorAll("span"); const lit = []; spans.forEach((s, i) => { if (PICK[i]) lit.push(s); });
        const t0 = w(54), t1 = we(61) - 0.1;
        lit.forEach((s, k) => { const t = t0 + (t1 - t0) * Math.pow(k / lit.length, 0.75);
          tl.set(s, { backgroundColor: "rgba(200,255,77,0.0)", color: "rgba(30,31,38,0.82)" }, 0);
          tl.to(s, { backgroundColor: "rgba(200,255,77,0.85)", color: "#111", duration: 0.12 }, t); });
        tl.to("#mfill", { scaleX: 1, duration: t1 - t0, ease: "power1.in" }, t0);
        tl.fromTo("#meter .mb", { boxShadow: "0 0 0 rgba(200,255,77,0)" }, { boxShadow: "0 0 40px rgba(200,255,77,0.9)", duration: 0.2, yoyo: true, repeat: 1, immediateRender: false }, t1); })();

      // ---------- s09: that's a signature ----------
      (function () { const p = makeSig("#sigPen", 180, 1010, 520, 120, 2.1, 7, -4);
        drawSig(p, A("s09") + 0.05, Math.max(0.4, B("s09") - A("s09") - 0.25)); tl.to(p, { opacity: 0, duration: 0.12 }, B("s09") - 0.1); })();

      // ---------- s11: copy, paste, a screenshot; the signature rides along ----------
      (function () { const host = $("#copies"); const pos = [[90, 380, -2], [430, 560, 3], [250, 470, -1]]; const cards = [];
        pos.forEach(([x, y, r], k) => { const c = el("div", "essay", `left:${x}px;top:${y}px;width:560px;height:430px;transform:rotate(${r}deg)`, host);
          c.innerHTML = `<div class="et" style="font-size:17px;line-height:1.5;left:30px;right:30px;top:28px">${words.slice(0, 120).join(" ")}</div>`;
          const s = document.createElementNS(NS, "svg"); s.setAttribute("viewBox", "0 0 560 430"); s.setAttribute("class", "sig"); s.style.width = "560px"; s.style.height = "430px"; c.appendChild(s);
          s.id = "sigC" + k; cards.push(c); });
        const sigs = cards.map((c, k) => makeSig("#sigC" + k, 70, 300, 380, 90, 3 + k, 7));
        const t0 = A("s11"), t1 = B("s11");
        tl.fromTo(cards[0], { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, t0 - 0.05);
        tl.set(sigs[0], { strokeDashoffset: 0, opacity: 1 }, t0 - 0.05);
        // copy
        tl.fromTo(cards[1], { opacity: 0, x: -340, y: -180, scale: 0.96 }, { opacity: 1, x: 0, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.4)" }, w(68) + 0.05);
        drawSig(sigs[1], w(68) + 0.2, 0.35);
        show("#kc1", w(68) - 0.02, w(69) - 0.05, { y: 20 });
        // paste
        show("#kc2", w(69) - 0.02, w(70) - 0.05, { y: 20 });
        tl.fromTo(cards[2], { opacity: 0, y: 140, scale: 1.1 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, w(69) + 0.05);
        drawSig(sigs[2], w(69) + 0.2, 0.3);
        // screenshot
        tl.fromTo("#vf", { opacity: 0, scale: 1.15 }, { opacity: 1, scale: 1, duration: 0.18, ease: E }, w(72) - 0.25);
        tl.to("#vf", { opacity: 0, duration: 0.12 }, w(72) + 0.35); flash(w(72) + 0.05, 0.85, 0.4);
        show("#kc3", w(72) - 0.3, w(73) + 0.1, { y: 20 });
        // built to survive: every copy glows
        cards.forEach((c, k) => tl.to(c, { boxShadow: "0 0 60px rgba(200,255,77,0.55), 0 40px 90px rgba(0,0,0,0.6)", duration: 0.25 }, w(74) + k * 0.08));
        sigs.forEach((s) => tl.fromTo(s, { opacity: 1 }, { opacity: 0.3, duration: 0.1, yoyo: true, repeat: 3, immediateRender: false }, w(76)));
        tl.to(cards, { opacity: 0, duration: 0.15 }, t1 - 0.12); })();

      // ---------- s12: the signature IS the words ----------
      (function () { $("#essayZT").innerHTML = words.slice(0, 64).map((x, i) => `<span>${x}</span>`).join(" ");
        const sp = $("#essayZT").querySelectorAll("span"); const p = makeSig("#sigZ", 170, 700, 700, 230, 4.2, 10, -6);
        tl.fromTo("#essayZ", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, A("s12") - 0.1);
        tl.to("#essayZ", { opacity: 0, duration: 0.15 }, B("s12") - 0.12);
        tl.set(p, { strokeDashoffset: 0, opacity: 1 }, A("s12") - 0.1); tl.to(p, { opacity: 0, duration: 0.12 }, B("s12") - 0.12);
        tl.to(p, { opacity: 0.15, duration: 0.35 }, w(80));
        sp.forEach((s, i) => { if (!PICK[i]) return; tl.set(s, { backgroundColor: "rgba(200,255,77,0)" }, 0);
          tl.to(s, { backgroundColor: "rgba(200,255,77,0.9)", color: "#111", duration: 0.15 }, w(80) + 0.02 * (i % 12)); });
        tl.fromTo("#essayZ", { scale: 1 }, { scale: 1.08, duration: B("s12") - w(80), ease: "power1.out", immediateRender: false }, w(80)); })();

      // ---------- s13 - s15: the law; Paris signs; London not yet ----------
      show("#chAct", w(85) - 0.05, B("s13") - 0.1, { x: -20 });
      (function () { const p = makeSig("#sigFlag", 120, 930, 840, 160, 5.5, 12, -8); drawSig(p, w(91), Math.max(0.4, we(93) - w(91) + 0.1), "power2.inOut");
        tl.to(p, { opacity: 0, duration: 0.12 }, B("s13") - 0.1); })();
      (function () { tl.set("#pinParis", { left: PARIS_PIN[0], top: PARIS_PIN[1] }, 0); show("#pinParis", w(96), B("s14") - 0.1, { scale: 0.6 });
        const p = makeSig("#sigParis", 380, 1000, 560, 120, 6.1, 9, -4); drawSig(p, w(97), Math.max(0.4, we(98) - w(97))); tl.to(p, { opacity: 0, duration: 0.12 }, B("s14") - 0.1); })();
      (function () { tl.set("#pinLondon", { left: LONDON_PIN[0], top: LONDON_PIN[1] }, 0); show("#pinLondon", w(100) - 0.05, B("s15") - 0.1, { scale: 0.6 });
        tl.fromTo("#lineLondon", { opacity: 0 }, { opacity: 1, duration: 0.25 }, w(101)); tl.to("#lineLondon", { opacity: 0, duration: 0.12 }, B("s15") - 0.1);
        for (let k = 0; k < 4; k++) { const t = w(101) + 0.3 + k * 0.14; if (t + 0.12 < B("s15") - 0.12) tl.to("#lineLondon", { opacity: k % 2 ? 1 : 0.35, duration: 0.12 }, t); }
        tl.set("#lineLondon", { opacity: 0 }, B("s15") + 0.02); })();

      // ---------- s16: Claude's page: worldwide ----------
      quote("#gx-s16", "● CLAUDE HELP CENTER · HOW CLAUDE MARKS AI-GENERATED CONTENT",
        '<div class="qt"><b style="color:#1b1c22">Regions.</b> Marking applies to supported-model output <span class="qh">wherever Claude is offered worldwide.</span></div>',
        A("s16") - 0.05, w(108), "QUOTED FROM THE PAGE · 24 OCT 2026");

      // ---------- s17: the globe ----------
      (function () { const cv = $("#globe"), g = cv.getContext("2d"); const R0 = 380, CX = 540, CY = 760;
        const proj = d3.geoOrthographic().scale(R0).translate([CX, CY]).clipAngle(90); const path = d3.geoPath(proj, g);
        const grat = d3.geoGraticule10();
        const CITIES = [[-74, 40.7], [-46.6, -23.5], [-99.1, 19.4], [-79.4, 43.7], [-58.4, -34.6], [3.4, 6.5], [36.8, -1.3], [31.2, 30], [28, -26.2], [55.3, 25.2],
          [72.9, 19.1], [77.2, 28.6], [103.8, 1.35], [139.7, 35.7], [127, 37.6], [151.2, -33.9], [2.35, 48.86], [13.4, 52.5], [-3.7, 40.4], [-0.13, 51.5]];
        const st = { lam: 0, pop: 0 }; const a = A("s17"), b = B("s17");
        const sq = (x, y, s, k) => { g.beginPath(); for (let i = 0; i <= 40; i++) { const t = (i / 40) * Math.PI * 6; const px = x - 18 * s + (36 * s * i) / 40 - 6 * s * Math.sin(t), py = y - 7 * s * Math.cos(t);
            i ? g.lineTo(px, py) : g.moveTo(px, py); } g.strokeStyle = "#c8ff4d"; g.lineWidth = 3.2 * s; g.shadowColor = "rgba(200,255,77,0.9)"; g.shadowBlur = 10 * s; g.stroke(); g.shadowBlur = 0; };
        const draw = () => { g.clearRect(0, 0, 1080, 1920); proj.rotate([st.lam, -30 - 18 * Math.min(1, st.pop * 1.2), 0]);
          const grd = g.createRadialGradient(CX - 120, CY - 140, 40, CX, CY, R0); grd.addColorStop(0, "#1a2a44"); grd.addColorStop(1, "#070b14");
          g.beginPath(); path({ type: "Sphere" }); g.fillStyle = grd; g.fill(); g.lineWidth = 3; g.strokeStyle = "rgba(124,196,255,0.55)"; g.stroke();
          g.beginPath(); path(grat); g.lineWidth = 1; g.strokeStyle = "rgba(124,196,255,0.12)"; g.stroke();
          g.beginPath(); path(window.LAND); g.fillStyle = "#2c3e58"; g.fill(); g.lineWidth = 1.2; g.strokeStyle = "rgba(160,200,240,0.6)"; g.stroke();
          const n = CITIES.length; CITIES.forEach((c, k) => { const on = Math.max(0, Math.min(1, st.pop * n * 1.1 - k)); if (on <= 0) return;
            if (d3.geoDistance(c, [-proj.rotate()[0], -proj.rotate()[1]]) > Math.PI / 2 - 0.05) return; const [x, y] = proj(c); sq(x, y, (k === n - 1 ? 1.5 : 1) * (0.4 + 0.6 * on)); });
          const uk = proj([-0.13, 51.5]); $("#pinUK").style.left = uk[0] + "px"; $("#pinUK").style.top = uk[1] + "px"; };
        tl.fromTo("#globe", { opacity: 0, scale: 0.85, transformOrigin: "540px 760px" }, { opacity: 1, scale: 1, duration: 0.35, ease: E }, a - 0.1);
        tl.to("#globe", { opacity: 0, duration: 0.15 }, b - 0.12);
        tl.fromTo(st, { lam: 120, pop: 0 }, { lam: 2, pop: 1, duration: Math.max(0.8, w(113) - a + 0.2), ease: "power2.inOut", onUpdate: draw }, a - 0.1);
        tl.to(st, { lam: -2, duration: Math.max(0.2, b - w(113)), ease: "none", onUpdate: draw }, w(113) + 0.1);
        show("#pinUK", w(113), b - 0.1, { scale: 0.5 }); })();

      // ---------- s18: so does it work? ----------
      punch("s18", w(118), 0.05);

      // ---------- s20: OpenAI's own chart, redrawn; then the record scratch ----------
      (function () { const host = $("#chart"); const rows = CHART.slice().sort((p, q) => q.base - p.base); const BW = 640;
        host.innerHTML = `<div class="ct">How often the mark was caught</div><div class="cs">OPENAI'S TEST · 24 EU LANGUAGES · AT 1% FALSE ALARMS</div>` +
          rows.map((r) => `<div class="cr" data-l="${r.lang}"><div class="cn">${r.lang.toUpperCase()}</div>` +
            (r.boosted ? `<div class="cg" style="width:${(BW * r.boosted / 100).toFixed(0)}px"></div>` : "") +
            `<div class="cb" style="width:${(BW * r.base / 100).toFixed(0)}px"></div><div class="cv" style="left:${(210 + BW * r.base / 100 + 14).toFixed(0)}px"></div></div>`).join("") +
          `<div class="half" style="left:${34 + 210 + BW / 2}px;height:${rows.length * 31}px"></div><div class="halfl" style="left:${34 + 210 + BW / 2 - 30}px">HALF</div>`;
        const a = A("s20"); tl.fromTo(host, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: E }, a - 0.05);
        tl.to(host, { opacity: 0, duration: 0.15 }, B("s20") - 0.12);
        const cr = host.querySelectorAll(".cr");
        tl.to(host.querySelectorAll(".cb"), { scaleX: 1, duration: 0.55, ease: "power2.out", stagger: 0.025 }, a + 0.05);
        const row = (l) => [...cr].find((r) => r.dataset.l === l);
        const es = row("Spanish"), ro = row("Romanian");
        tl.to(es.querySelector(".cb"), { backgroundColor: "#c8ff4d", boxShadow: "0 0 18px rgba(200,255,77,0.8)", duration: 0.2 }, w(129) - 0.1);
        tl.to(es.querySelector(".cn"), { color: "#c8ff4d", duration: 0.2 }, w(129) - 0.1);
        textAt("#chart .cr[data-l='Spanish'] .cv", [[0, "69%"]]); tl.set(es.querySelector(".cv"), { color: "#c8ff4d" }, 0);
        tl.fromTo(es.querySelector(".cv"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.25, ease: "back.out(2)" }, w(129) - 0.05);
        tl.fromTo([host.querySelector(".half"), host.querySelector(".halfl")], { opacity: 0 }, { opacity: 1, duration: 0.25 }, w(134) - 0.1);
        tl.to(ro.querySelector(".cb"), { backgroundColor: "#ffb547", boxShadow: "0 0 18px rgba(255,181,71,0.8)", duration: 0.2 }, w(136) - 0.1);
        tl.to(ro.querySelector(".cn"), { color: "#ffb547", duration: 0.2 }, w(136) - 0.1);
        textAt("#chart .cr[data-l='Romanian'] .cv", [[0, "42%"]]); tl.set(ro.querySelector(".cv"), { color: "#ffb547" }, 0);
        tl.fromTo(ro.querySelector(".cv"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.25, ease: "back.out(2)" }, w(136) - 0.05);
        // the boost OpenAI gave the weaker languages, shown as it is on their chart
        tl.to(host.querySelectorAll(".cg"), { scaleX: 1, duration: 0.4, ease: "power2.out", stagger: 0.02 }, we(136) + 0.05);
        // the record scratch on "Here's the twist": freeze, jolt, the colour drains
        const T = w(137) - 0.04;
        [[0, 26, 2], [0.04, -20, -2], [0.08, 12, 1], [0.12, -6, 0], [0.16, 0, 0]].forEach(([dt, x, r]) => tl.set(fx("s20"), { x, rotation: r }, T + dt));
        tl.set(host, { filter: "grayscale(0) contrast(1)" }, 0); tl.to(host, { filter: "grayscale(1) contrast(1.15) brightness(0.8)", duration: 0.25 }, T);
        flash(T, 0.45, 0.3, "#ffffff");
        tl.fromTo(cam("s20"), { scale: 1 }, { scale: 1.08, duration: B("s20") - T, ease: "power1.out", immediateRender: false }, T); })();

      // ---------- s21: the twist: Claude signs what it only translated ----------
      quote("#gx-s21", "● CLAUDE HELP CENTER · LIMITATIONS",
        '<div class="qbig">Claude may not be the original author.</div><div class="qt" style="font-size:50px;margin-top:20px">People may use Claude to proofread, <span class="qh">translate</span>, summarize, or convert material whose original ideas, text, or data came from elsewhere.</div>',
        A("s21") - 0.05, w(146), "QUOTED FROM THE PAGE · 24 OCT 2026");
      punch("s21", w(146), 0.05); flash(w(146), 0.3, 0.4, "#c8ff4d");
      // ---------- s22: your own words, signed ----------
      (function () { const a = A("s22") - HND, b = B("s22") + HND; tl.fromTo(cam("s22"), { scale: 1 }, { scale: 1.1, duration: b - a, ease: "none" }, a);
        const p = makeSig("#sigPhone", PHONE[0], PHONE[1], PHONE[2], PHONE[3], 7.7, 8, PHONE[4]);
        drawSig(p, w(152), Math.max(0.4, we(154) - w(152))); tl.to(p, { opacity: 0, duration: 0.12 }, B("s22") - 0.1); })();
      // ---------- s23: a signal, not proof ----------
      quote("#gx-s23", "● CLAUDE HELP CENTER · LIMITATIONS",
        '<div class="qbig"><span class="qh">A detected mark is not fully conclusive</span></div><div class="qt" style="font-size:46px;margin-top:22px">A detected Claude mark signals that the content may have been processed by Claude, but it does not by itself establish the full provenance of the content.</div>',
        A("s23") - 0.05, w(163), "QUOTED FROM THE PAGE · 24 OCT 2026");
      // ---------- s24 ----------
      show("#chChecker", w(170) - 0.05, B("s24") - 0.1, { x: -20 });
      // ---------- s26 / s27: the stamps that won't stick ----------
      (function () { tl.fromTo("#stCheat", { opacity: 0, scale: 2.4 }, { opacity: 0.92, scale: 1, duration: 0.18, ease: "power4.out" }, w(184) - 0.05);
        const endC = Math.min(B("s26") - 0.3, w(184) + 0.85);
        for (let k = 0; k < 5; k++) { const t = w(184) + 0.3 + k * 0.08; if (t + 0.08 < endC) tl.to("#stCheat", { opacity: k % 2 ? 0.8 : 0.25, duration: 0.08 }, t); }
        tl.to("#stCheat", { opacity: 0, duration: 0.22 }, endC); tl.set("#stCheat", { opacity: 0 }, B("s26") + 0.02);
        tl.fromTo("#stHuman", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.out" }, w(191) - 0.05);
        const endH = Math.min(B("s27") - 0.25, w(191) + 0.8);
        for (let k = 0; k < 5; k++) { const t = w(191) + 0.3 + k * 0.08; if (t + 0.08 < endH) tl.to("#stHuman", { opacity: k % 2 ? 0.85 : 0.2, duration: 0.08 }, t); }
        tl.to("#stHuman", { opacity: 0, duration: 0.2 }, endH); tl.set("#stHuman", { opacity: 0 }, B("s27") + 0.02); })();
      // ---------- s28: just say so ----------
      (function () { tl.fromTo("#note", { opacity: 0, y: 60, rotation: -6 }, { opacity: 1, y: 0, rotation: -3, duration: 0.35, ease: "back.out(1.5)" }, w(200) - 0.35);
        tl.fromTo("#noteT", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: Math.max(0.6, B("s28") - w(200) - 0.2), ease: "power1.inOut" }, w(200) - 0.1);
        tl.to("#note", { opacity: 0, duration: 0.12 }, B("s28") - 0.1); })();
      // ---------- s29: the words might already be saying it: back to frame one ----------
      (function () { const p = makeSig("#sigHero", 200, 760, 640, 190, 1.3, 9);
        drawSig(p, A("s29") + 0.1, Math.max(0.6, we(209) - A("s29") - 0.1)); tl.to(p, { opacity: 0, duration: 0.2 }, B("s29") - 0.05); })();

      // ---------- end card ----------
      const TE = A("s30");
      tl.fromTo("#end", { opacity: 0 }, { opacity: 1, duration: 0.5 }, TE);
      tl.fromTo("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, TE + 0.15);
      tl.fromTo(["#ename", "#ehandle"], { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: E, stagger: 0.12 }, TE + 0.4);
      tl.fromTo("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, TE + 0.85);
      tl.to("#fol", { scale: 1.06, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, TE + 1.4);
      tl.to("#mark", { boxShadow: "0 0 140px rgba(200,255,77,0.8)", duration: 0.9, yoyo: true, repeat: 1, ease: "sine.inOut" }, TE + 1.1);

      // ---------- global UI ----------
      %HLJS%.forEach(([id, t, d]) => tl.to("#" + id, { scaleX: 1, duration: d, ease: "power2.inOut" }, t));
      %LABJS%.forEach(([sel, a, b]) => show(sel, a, b, { x: -20, y: 0 }));
      DOCS.forEach((id) => docCam(id));
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      tl.set(["#tag", "#bm"], { opacity: 1 }, 0);
      tl.to(["#tag", "#bm"], { opacity: 0, duration: 0.4 }, TE - 0.2);
      tl.to([".botshade", ".topshade"], { opacity: 0, duration: 0.5 }, TE);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);
      tl.fromTo("#black", { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, DUR - 0.45);

      // ---------- designed captions ----------
      const CAPLAY = %CAPLAY%, COVERS = %COVERS%;
      const layoutFor = (t) => (CAPLAY.find(([a, b]) => t >= a && t < b) || [0, 0, { m: "S", c: "#c8ff4d" }])[2];
      const covered = (a, b) => COVERS.some(([c0, c1]) => a < c1 && b > c0 - 0.02);
      const capsRoot = $("#caps");
      const fmtNum = (v, target, d) => { const pre = d.match(/^[^\d]*/)[0], suf = d.match(/[^\d]*$/)[0]; const n = Math.round(v); return pre + (target >= 1000 ? n.toLocaleString("en-US") : String(n)) + suf; };
      (window.CAPS || []).forEach((ch) => {
        if (covered(ch.t0, ch.t1)) return;
        const L = layoutFor(ch.t0); const col = L.c;
        const c = document.createElement("div"); c.className = "cap " + L.m; if (ch.w.some((x) => x.emph)) c.setAttribute("data-layout-allow-overlap", ""); capsRoot.appendChild(c);
        const spans = ch.w.map((x) => { const s = document.createElement("span"); const d = x.d;
          const isNum = L.m === "B" && /\d/.test(d); const hero = x.emph && L.m === "A";
          s.className = "cw dim" + (isNum ? " num" : "") + (hero ? " hero" : "") + (x.emph && !hero ? " inl" : "");
          if (hero) { const len = d.replace(/[^A-Z0-9']/gi, "").length; const fs = Math.min(210, Math.round(930 / (len * 0.64)));
            s.style.fontSize = fs + "px"; s.style.transform = "rotate(-3deg)"; s.style.textShadow = `0 0 40px ${rgba(col, 0.55)}, 0 8px 30px rgba(0,0,0,0.5)`; }
          s.textContent = d;
          if (hero) { const bar = document.createElement("span"); bar.className = "bar"; bar.style.width = "96%"; bar.style.background = col; bar.style.boxShadow = `0 0 20px ${col}`; s.appendChild(bar); }
          c.appendChild(s); return { s, x, isNum, hero, d }; });
        tl.fromTo(c, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.14, ease: "back.out(2)" }, ch.t0);
        tl.set(c, { opacity: 0 }, ch.t1);
        spans.forEach(({ s, x, isNum, hero, d }, k) => {
          const end = k + 1 < spans.length ? spans[k + 1].x.s : ch.t1;
          const keep = x.emph || isNum || hero;
          tl.set(s, { opacity: 1, color: col, scale: hero ? 1 : 1.05 }, x.s);
          tl.set(s, { color: keep ? col : "#ffffff", scale: 1 }, end);
          if (hero) { tl.fromTo(s, { scale: 1.18 }, { scale: 1, duration: 0.22, ease: "power4.out", immediateRender: false }, x.s);
            const bar = s.querySelector(".bar"); if (bar) tl.fromTo(bar, { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, x.s + 0.05); }
          if (isNum) { const target = parseFloat(d.replace(/[^\d.]/g, "")); const m = { v: 0 };
            tl.set(s, { textShadow: `0 0 40px ${rgba(col, 0.6)}, 0 8px 30px rgba(0,0,0,0.5)` }, x.s);
            tl.fromTo(m, { v: 0 }, { v: target, duration: Math.max(0.4, x.e - x.s + 0.2), ease: "power2.out", onUpdate() { s.firstChild.nodeValue = fmtNum(m.v, target, d); } }, x.s);
            s.firstChild.nodeValue = fmtNum(0, target, d); }
        });
      });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>

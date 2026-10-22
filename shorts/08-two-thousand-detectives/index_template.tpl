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
      .vid { position: absolute; object-fit: cover; }
      .frz { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .bd { position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; background-size: cover; background-position: center;
        filter: brightness(0.38) saturate(0.85); }
      .desk { position: absolute; inset: 0; background:
        radial-gradient(ellipse 70% 45% at 50% 38%, rgba(255,255,255,0.06), rgba(0,0,0,0) 70%),
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: auto, 72px 72px, 72px 72px; }
      .card { position: absolute; overflow: hidden; border-radius: 24px; background: #fff;
        box-shadow: 0 40px 90px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08); }
      .card img { position: absolute; }
      .scroller { position: absolute; left: 0; top: 0; width: 100%; }
      .hl { position: absolute; mix-blend-mode: multiply; border-radius: 6px; transform-origin: 0 50%; transform: scaleX(0); }
      .redact { position: absolute; background: #0b0c10; border-radius: 3px; transform-origin: 0 50%; transform: scaleX(0); }
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
        color: #ff5b5b; background: rgba(12,6,8,0.55); opacity: 0; white-space: nowrap; }
      .chip { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.08em; padding: 14px 22px;
        border-radius: 14px; background: rgba(6,8,12,0.84); border: 2px solid currentColor; opacity: 0; white-space: nowrap; color: var(--amber); }
      .chip .sw { display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: currentColor; margin-right: 14px; vertical-align: 2px; box-shadow: 0 0 12px currentColor; }
      .chip s { text-decoration-thickness: 5px; text-decoration-color: #ff5b5b; }
      .readout { position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; }
      .readout .rl { font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.2em; color: #e2e4ea; text-shadow: 0 2px 12px rgba(0,0,0,0.9); }
      .readout .rv { font-weight: 900; font-size: 130px; letter-spacing: -0.04em; line-height: 1; color: #fff; }
      .readout .rs { font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.12em; color: #c9ccd6; margin-top: 10px; }
      .ring { position: absolute; border-radius: 50%; border: 6px solid var(--amber); box-shadow: 0 0 26px rgba(255,181,71,0.8), inset 0 0 20px rgba(255,181,71,0.4); opacity: 0; }
      .pin { position: absolute; left: 0; top: 0; opacity: 0; }
      .pin .pl { position: absolute; left: 26px; top: -30px; font-family: "Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.06em; white-space: nowrap;
        padding: 10px 16px; border-radius: 12px; background: rgba(6,8,12,0.82); border: 2px solid currentColor; }
      .pin .pd { position: absolute; left: -11px; top: -11px; width: 22px; height: 22px; border-radius: 50%; background: currentColor; box-shadow: 0 0 18px currentColor; }
      .pin.left .pl { left: auto; right: 26px; }
      .gtag { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 34px; letter-spacing: 0.04em; color: #ffe2b0; padding: 8px 16px;
        border-radius: 10px; background: rgba(10,8,4,0.66); border: 2px solid rgba(255,181,71,0.75); box-shadow: 0 0 24px rgba(255,181,71,0.45); opacity: 0; white-space: nowrap; }
      .vf { position: absolute; left: 70px; top: 300px; width: 940px; height: 900px; opacity: 0; }
      .vf i { position: absolute; width: 90px; height: 90px; border: 0 solid #fff; }
      .vf .rec { position: absolute; right: 18px; top: 16px; font-family: "Mono", monospace; font-weight: 700; font-size: 28px; color: #fff; letter-spacing: 0.1em; }
      .vf .rec b { display: inline-block; width: 18px; height: 18px; border-radius: 50%; background: #ff3b30; margin-right: 10px; box-shadow: 0 0 12px #ff3b30; }
      .pop { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; opacity: 0;
        background: radial-gradient(circle, rgba(255,255,255,1) 0, rgba(255,240,220,0.7) 18%, rgba(255,255,255,0) 60%); }
      .photo { position: absolute; width: 112px; height: 84px; border: 5px solid #f3efe6; border-bottom-width: 12px; border-radius: 3px; background-size: 540px 960px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.5); opacity: 0; }
      .cal { position: absolute; left: 620px; top: 330px; width: 400px; border-radius: 22px; overflow: hidden; background: #f3efe6; box-shadow: 0 30px 60px rgba(0,0,0,0.55); opacity: 0; }
      .cal .ch { background: #c9352b; color: #fff; font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.14em; padding: 16px 0; text-align: center; }
      .cal .cn { font-weight: 900; font-size: 190px; letter-spacing: -0.05em; line-height: 1; color: #15161b; text-align: center; padding: 18px 0 0; }
      .cal .cu { font-family: "Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.14em; color: #5a5d66; text-align: center; padding: 6px 0 24px; }
      .cal .cb { height: 14px; background: #ddd6c8; } .cal .cb i { display: block; height: 100%; width: 100%; background: #c9352b; transform-origin: 0 50%; transform: scaleX(0); }
      .badge { position: absolute; left: 60px; top: 870px; width: 600px; padding: 26px 30px; border-radius: 22px; background: rgba(12,10,22,0.86); border: 2px solid rgba(185,156,255,0.7);
        box-shadow: 0 0 40px rgba(185,156,255,0.35), 0 30px 60px rgba(0,0,0,0.5); opacity: 0; }
      .badge .bk { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.18em; color: #b9a2ff; }
      .badge .bn { font-weight: 900; font-size: 66px; letter-spacing: -0.03em; color: #fff; margin-top: 8px; }
      .badge .bs { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.1em; color: #c9ccd6; margin-top: 8px; }
      .race { position: absolute; inset: 0; opacity: 0; }
      .race .rh { position: absolute; top: 330px; width: 420px; text-align: center; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.12em; color: #d4d6de; }
      .race .rn { position: absolute; top: 380px; width: 420px; text-align: center; font-weight: 900; font-size: 120px; letter-spacing: -0.04em; color: #fff; line-height: 1; }
      .race .floor { position: absolute; left: 80px; top: 1186px; width: 920px; height: 4px; background: rgba(255,255,255,0.35); }
      .x711 { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; opacity: 0; }
      .x711 span { display: inline-block; font-weight: 900; font-size: 64px; padding: 8px 26px; border-radius: 999px; background: var(--amber); color: #0b0c10; box-shadow: 0 0 40px rgba(255,181,71,0.6); }
      .judges { position: absolute; left: 0; width: 1080px; top: 1085px; display: flex; justify-content: center; gap: 26px; }
      .judges .j { width: 150px; height: 118px; border-radius: 16px; border: 3px solid rgba(255,255,255,0.25); background: rgba(8,9,14,0.75); opacity: 0;
        display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.08em; color: #c9ccd6; }
      .judges .j b { font-family: "InterV", sans-serif; font-weight: 900; font-size: 46px; color: #fff; line-height: 1.05; }
      .judges .j.team { border-color: #b99cff; box-shadow: 0 0 26px rgba(185,156,255,0.5); }
      .ev { position: absolute; left: 0; top: 0; width: 600px; height: 170px; opacity: 0; transform-origin: 50% 50%; text-align: center; padding-top: 14px; }
      .ev .et { font-family: "Mono", monospace; font-weight: 700; font-size: 118px; color: #3a1d05; letter-spacing: 0.04em; line-height: 1; }
      .ev .es { font-family: "Mono", monospace; font-weight: 700; font-size: 30px; color: #6b3a0c; letter-spacing: 0.06em; margin-top: 10px; }
      .swb { position: absolute; left: 60px; top: 300px; width: 960px; padding: 26px 30px 24px; border-radius: 26px; background: rgba(10,9,8,0.82); border: 2px solid rgba(255,181,71,0.35); }
      .swb .sh { font-family: "Mono", monospace; font-weight: 700; font-size: 25px; letter-spacing: 0.14em; color: #ffcf8a; margin-bottom: 18px; }
      .swb .grid2 { display: grid; grid-template-columns: 1fr 1fr; column-gap: 40px; row-gap: 12px; }
      .swb .row { display: flex; align-items: center; justify-content: space-between; height: 62px; padding: 0 16px; border-radius: 14px; background: rgba(255,255,255,0.04); }
      .swb .gn { font-family: "Mono", monospace; font-weight: 700; font-size: 34px; color: #9a9ca6; }
      .swb .tg { position: relative; width: 92px; height: 46px; border-radius: 23px; background: #2a2c34; }
      .swb .tg i { position: absolute; left: 5px; top: 5px; width: 36px; height: 36px; border-radius: 50%; background: #6b6e78; }
      .swb .q { margin-top: 20px; font-family: Georgia, serif; font-style: italic; font-size: 33px; line-height: 1.32; color: #f3e6d0; min-height: 132px; }
      .swb .q b { font-style: normal; font-family: "Mono", monospace; font-size: 22px; letter-spacing: 0.1em; color: #ffcf8a; display: block; margin-top: 10px; font-weight: 700; }
      .redbar { position: absolute; }
      .strings { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .quote { position: absolute; left: 60px; top: 330px; width: 960px; padding: 40px 44px 34px; border-radius: 26px; background: rgba(250,247,240,0.97);
        box-shadow: 0 40px 90px rgba(0,0,0,0.6); }
      .quote .qk { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.16em; color: #2f7a52; margin-bottom: 18px; }
      .quote .qt { position: relative; z-index: 0; font-family: Georgia, serif; font-style: italic; font-size: 54px; line-height: 1.26; color: rgba(27,28,34,0.5); }
      .quote .qt + .qt { margin-top: 22px; }
      .quote .qh { color: #1b1c22; background-image: linear-gradient(rgba(255,200,80,0.62), rgba(255,200,80,0.62)); background-repeat: no-repeat;
        background-position: 0 88%; background-size: 0% 78%; }
      .quote .qh.v { background-image: linear-gradient(rgba(185,156,255,0.55), rgba(185,156,255,0.55)); }
      .quote .qa { margin-top: 20px; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.1em; color: #5a5d66; }
      .proof { position: absolute; left: 60px; width: 960px; top: 1000px; border-radius: 14px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5); opacity: 0.92; }
      .proof img { display: block; width: 960px; }
      .race .rp { position: absolute; top: 505px; width: 420px; text-align: center; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.14em; color: #9a9ca6; }
      .race .rn span { background: rgba(6,8,12,0.82); padding: 0 22px; border-radius: 22px; }

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

        <!-- s03 / s54: stopwatch -->
        <svg id="watch" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0">
          <circle cx="540" cy="740" r="250" fill="rgba(6,8,12,0.35)" stroke="rgba(255,255,255,0.18)" stroke-width="10" />
          <g id="wticks"></g>
          <circle id="warc" cx="540" cy="740" r="250" fill="none" stroke="#ffb547" stroke-width="14" stroke-linecap="round" transform="rotate(-90 540 740)"
            style="filter: drop-shadow(0 0 14px rgba(255,181,71,0.9))" />
          <line id="whand" x1="540" y1="740" x2="540" y2="520" stroke="#fff" stroke-width="8" stroke-linecap="round" />
          <circle cx="540" cy="740" r="16" fill="#ffb547" />
        </svg>
        <!-- s07-s08 -->
        <div class="chip" id="chHouse" style="left:60px;top:1110px;color:#ffb547"><span class="sw"></span>1 HOUSE = 1 BRAIN CELL</div>
        <!-- s09: gene names on the wiring -->
        <div id="gtags"></div>
        <div class="chip" id="chWiring" style="left:60px;top:1110px;color:#ffb547"><span class="sw"></span>WIRING = GENES</div>
        <!-- s10: the cut -->
        <svg id="slash" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0">
          <path id="slashp" d="M 120 980 L 960 520" stroke="#fff" stroke-width="12" stroke-linecap="round" fill="none" style="filter: drop-shadow(0 0 18px rgba(255,90,90,0.95))" />
        </svg>
        <div class="chip" id="chOne" style="left:60px;top:1110px;color:#ff8a7a"><span class="sw"></span>1 GENE SWITCHED OFF PER CELL</div>
        <!-- s11 -->
        <div class="pin" id="pCut" style="color:#ffb547"><div class="pd"></div><div class="pl">CRISPR CUT</div></div>
        <!-- s12 -->
        
        <!-- s14: camera -->
        <div class="vf" id="vf"><i style="left:0;top:0;border-left-width:6px;border-top-width:6px"></i><i style="right:0;top:0;border-right-width:6px;border-top-width:6px"></i>
          <i style="left:0;bottom:0;border-left-width:6px;border-bottom-width:6px"></i><i style="right:0;bottom:0;border-right-width:6px;border-bottom-width:6px"></i>
          <div class="rec"><b></b>EVERY HOUSE</div></div>
        <div id="pops"></div>
        <!-- s15: lights -->
        <canvas id="lights" width="1080" height="1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0"></canvas>
        <div class="chip" id="chLight" style="left:60px;top:1110px;color:#ffd38a"><span class="sw"></span>LIGHT ON = GENE ACTIVE</div>
        <!-- s16 -->
        <div class="readout" id="rdData" style="top:300px"><div class="rl">THE REAL DATASET</div><div class="rv" style="font-size:110px">7.7 MILLION CELLS</div>
          <div class="rs">19,070 GENES MEASURED IN EACH</div></div>
        <!-- s17 -->
        <div class="cal" id="cal"><div class="ch">BY HAND</div><div class="cn" id="calN">1</div><div class="cu" id="calU">MONTH</div><div class="cb"><i id="calB"></i></div></div>
        <!-- s18 -->
        <div class="badge" id="badge"><div class="bk">● AGENT · OPENAI</div><div class="bn">GPT-Rosalind</div><div class="bs">A BIOLOGY AI</div></div>
        <!-- s19 -->
        <canvas id="copies" width="900" height="920" style="position:absolute;left:150px;top:300px;width:780px;height:797px;opacity:0"></canvas>
        <div class="readout" id="rdCopies" style="top:1118px"><div class="rv" id="cpN" style="font-size:96px">×1</div></div>
        <!-- s23 -->
        <div class="chip" id="chReports" style="left:60px;top:1110px;color:#ffd38a"><span class="sw"></span>1,946 CASE REPORTS</div>
        <!-- s24-s25: the reference race -->
        <div class="race" id="race">
          <canvas id="raceCv" width="1080" height="1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px"></canvas>
          <div class="floor"></div>
          <div class="rh" style="left:80px">ONE AI ALONE</div><div class="rn" style="left:80px"><span id="rcL">0</span></div><div class="rp" style="left:80px">PAPERS CITED</div>
          <div class="rh" style="left:580px;color:#ffcf8a">THE TEAM</div><div class="rn" style="left:580px;color:#ffb547"><span id="rcR">0</span></div><div class="rp" style="left:580px">PAPERS CITED</div>
        </div>
        <div class="x711" id="x711"><span>711× MORE</span></div>
        <!-- s26 -->
        <div class="stamp" id="stHidden" style="left:110px;top:1010px;font-size:70px;transform:rotate(-6deg)">HIDDEN FROM THE AI</div>
        <!-- s27 -->
        <div class="stamp" id="stCould" style="left:230px;top:1020px;font-size:76px;color:#7ee787;transform:rotate(-6deg)">✓ THEY COULD</div>
        <!-- s28 -->
        <div class="judges" id="judges"><div class="j team"><b>✓</b>TEAM</div><div class="j team"><b>✓</b>TEAM</div><div class="j team"><b>✓</b>TEAM</div><div class="j"><b>·</b>LONE AI</div></div>
        <!-- s29: the clue card -->
        <div class="ev" id="ev"><div class="et" id="evT">DCTN1</div><div class="es" id="evS">THE LEAD</div></div>
        <!-- s31 -->
        <div class="pin" id="pHead" style="color:#cfe3f5"><div class="pd"></div><div class="pl">MOTOR (DYNEIN)</div></div>
        <div class="pin left" id="pArm" style="color:#ffb547"><div class="pd"></div><div class="pl">ARM BUILT FROM DCTN1</div></div>
        <div class="pin" id="pCargo" style="color:#9fe0ff"><div class="pd"></div><div class="pl">CARGO</div></div>
        <!-- s33 -->
        <div class="chip" id="chCut" style="left:60px;top:1110px;color:#ff8a7a"><span class="sw"></span>WIRE CUT: DCTN1</div>
        <!-- s34: the switches -->
        <div id="swHost"></div>
        <!-- s35 -->
        <div class="stamp" id="stStop" style="left:110px;top:700px;font-size:70px;transform:rotate(-7deg)">DELIVERIES STOPPED</div>
        <!-- s39 -->
        <div class="pin left" id="pArmX" style="color:#ff5b5b"><div class="pd"></div><div class="pl">ARM FAILS ✕</div></div>
        <div class="pin" id="pStuck" style="color:#ffb547"><div class="pd"></div><div class="pl">CHOLESTEROL STUCK</div></div>
        <!-- s40 -->
        <div class="chip" id="chPerry" style="left:60px;top:1110px;color:#7fe0c8"><span class="sw"></span>DCTN1 FAULT → PERRY SYNDROME</div>
        <!-- s42 -->
        <div class="chip" id="chLittle" style="left:60px;top:1110px;color:#ffd38a"><span class="sw"></span><s id="littleS">TOO LITTLE CHOLESTEROL?</s></div>
        <!-- s43 -->
        <div class="ring" id="ringPile" style="width:300px;height:300px;border-color:#ff5b5b;box-shadow:0 0 30px rgba(255,91,91,0.8)"></div>
        <div class="pin" id="pWrong" style="color:#ff5b5b"><div class="pd"></div><div class="pl">WRONG PLACE</div></div>
        <div class="pin left" id="pDest" style="color:#4fd0ff"><div class="pd"></div><div class="pl">WHERE IT SHOULD GO</div></div>
        <!-- s44-s45 -->
        <div class="chip" id="chFix" style="left:60px;top:1110px;color:#ffb547"><span class="sw"></span>IDEA: FIX THE DELIVERIES</div>
        <div class="chip" id="chProtect" style="left:60px;top:1110px;color:#7ee787"><span class="sw"></span>PROTECTS NEURONS? NOT YET TESTED</div>
        <!-- s46 -->
        <div class="stamp" id="stLead" style="left:110px;top:560px;color:#7ee787;transform:rotate(-6deg)">✓ A LEAD</div>
        <div class="stamp" id="stCure" style="left:300px;top:820px;font-size:80px;transform:rotate(5deg)">✕ NOT A CURE</div>
        <!-- s47-s49 -->
        <div class="chip" id="chMice" style="left:60px;top:1110px;color:#ffd38a"><span class="sw"></span>MOUSE DATA, NOT PEOPLE</div>
        <div class="stamp" id="stPeer" style="left:120px;top:1040px;font-size:62px;transform:rotate(-5deg)">NOT PEER-REVIEWED YET</div>
        <div class="chip" id="chLab" style="left:60px;top:1110px;color:#7fe0c8"><span class="sw"></span>NEXT: A REAL LAB TEST</div>
        <!-- s50 -->
        <div class="readout" id="rdExp" style="top:330px;padding:30px 0 40px;background:radial-gradient(ellipse 46% 50% at 50% 50%, rgba(4,5,10,0.82), rgba(4,5,10,0) 100%)"><div class="rl">EXPERIMENTS RUN BY THE AI</div><div class="rv" style="font-size:220px">0</div></div>
        <!-- s51 -->
        <svg class="strings" id="strings" viewBox="0 0 1080 1920"><g id="strG" stroke="#ff3b30" stroke-width="5" fill="none" stroke-linecap="round" style="filter: drop-shadow(0 0 8px rgba(255,59,48,0.9))"></g><g id="strD"></g></svg>
        <!-- s55 -->
        <div class="ring" id="ringWin" style="width:220px;height:220px"></div>

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
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span><span style="font-family:Georgia;font-style:italic">Aa</span></div>
      </div>

      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%, HND = %H%;
      const SH = %SHOTSJS%;
      const GEO = %GEO%;
      const COL = %COL%;
      const GENES = %GENES%;
      const PINS = %PINS%;
      const TRACK = %TRACK%;
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out";
      const fx = (id) => "#fx-" + id, cam = (id) => "#cam-" + id;
      const T0 = Object.fromEntries(SH.map((s) => [s.id, s.t0])), T1 = Object.fromEntries(SH.map((s) => [s.id, s.t1]));
      const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; };
      const el = (tag, cls, css, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css; (parent || $("#ui")).appendChild(e); return e; };
      let seed = 7; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;

      // ---------- shots: visibility and default camera ----------
      const DOCS = ["s13", "s20", "s26", "s30", "s38", "s41"];
      const CUSTOM_CAM = new Set(DOCS.concat(["s05", "s27", "s28", "s48", "s11", "s29", "s31", "s39", "s43", "s44", "s52", "s55", "s56", "s12", "s16", "s19", "s24", "s25", "s34"]));
      SH.forEach((s, i) => {
        tl.set(fx(s.id), { opacity: i === 0 ? 1 : 0 }, 0);
        const a = Math.max(0, s.t0 - HND), b = s.t1 + HND;
        if (CUSTOM_CAM.has(s.id)) return;
        tl.fromTo(cam(s.id), { scale: 1 }, { scale: 1.07, duration: b - a, ease: "none" }, a);
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
      const CUTS = [["s01", "s02", "flash", "#ffb547"], ["s02", "s03", "whip"], ["s03", "s04", "zoom"], ["s04", "s05", "card"], ["s05", "s06", "dip"],
        ["s06", "s07", "zoom"], ["s07", "s08", "flash", "#ffb547"], ["s08", "s09", "slideup"], ["s09", "s10", "whip"], ["s10", "s11", "glitch"],
        ["s11", "s12", "zoom"], ["s12", "s13", "card"], ["s13", "s14", "dip"], ["s14", "s15", "flash", "#ffffff"], ["s15", "s16", "slideup"],
        ["s16", "s17", "whip"], ["s17", "s18", "dip"], ["s18", "s19", "zoom"], ["s19", "s20", "card"], ["s20", "s21", "zoom"], ["s21", "s22", "whip"],
        ["s22", "s23", "slideup"], ["s23", "s24", "card"], ["s24", "s25", "flash", "#ffb547"], ["s25", "s26", "card"], ["s26", "s27", "slideup"],
        ["s27", "s28", "card"], ["s28", "s29", "dip"], ["s29", "s30", "zoom"], ["s30", "s31", "glitch"], ["s31", "s32", "zoom"], ["s32", "s33", "whip"],
        ["s33", "s34", "flash", "#ffb547"], ["s34", "s35", "slideup"], ["s35", "s36", "whip"], ["s36", "s37", "zoom"], ["s37", "s38", "card"],
        ["s38", "s39", "glitch"], ["s39", "s40", "dip"], ["s40", "s41", "card"], ["s41", "s42", "fade"], ["s42", "s43", "zoom"], ["s43", "s44", "flash", "#4fd0ff"],
        ["s44", "s45", "zoom"], ["s45", "s46", "dip"], ["s46", "s47", "whip"], ["s47", "s48", "card"], ["s48", "s49", "whip"], ["s49", "s50", "slideup"],
        ["s50", "s51", "whip"], ["s51", "s52", "card"], ["s52", "s53", "flash", "#ffb547"], ["s53", "s54", "whip"], ["s54", "s55", "zoom"], ["s55", "s56", "fade"]];
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
        const kf = (S, px, py) => { let y = 740 - S * py; const dy = 300 - (y + S * g[1]); if (dy > 0 && dy <= 160) y += dy;  // keep the card's top edge clear of the labels when a small nudge does it
          return { scale: S, x: 540 - S * px, y }; };
        tl.set(cam(id), { transformOrigin: "0px 0px" }, 0);
        if (!hls.length) { tl.fromTo(cam(id), kf(1, 540, 740), Object.assign(kf(1.06, g[0] + g[2] / 2, g[1] + g[3] / 2), { duration: b - a, ease: "none" }), a); return; }
        const zs = (w) => Math.max(1.05, Math.min(1.7, 880 / (w + 80)));
        let prevT = a;
        hls.forEach(([t, hx, hy, w], k) => { const end = Math.max(prevT + 0.35, t + 0.25); const tw = Object.assign(kf(zs(w), hx, hy), { duration: end - prevT, ease: "power2.inOut" });
          if (k === 0) tl.fromTo(cam(id), kf(1, 540, 740), tw, prevT); else tl.to(cam(id), tw, prevT); prevT = end; });
        const L = hls[hls.length - 1]; if (b > prevT + 0.05) tl.to(cam(id), Object.assign(kf(zs(L[3]) * 1.04, L[1], L[2]), { duration: b - prevT, ease: "none" }), prevT); };
      // a label riding a 3D point: PINS[scene][k] = {name: [x, y]} per frame from the scene's start (out time t0 - HND)
      const pinTo = (sel, scene, key, sid, t0, t1, dx, dy) => { const P = PINS[scene]; if (!P) return; const a = T0[sid] - HND; const e = $(sel); const st = { f: 0 };
        tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t0); tl.to(sel, { opacity: 0, duration: 0.15 }, t1);
        tl.fromTo(st, { f: 0 }, { f: P.length - 1, duration: (P.length - 1) / 30, ease: "none", onUpdate() { const q = P[Math.min(P.length - 1, Math.round(st.f))][key]; if (q) e.style.transform = `translate(${q[0] + (dx || 0)}px, ${q[1] + (dy || 0)}px)`; } }, a); };

      // highlights and source labels
      %HLJS%.forEach(([id, t, d]) => tl.to("#" + id, { scaleX: 1, duration: d, ease: "power2.inOut" }, t));
      %LABJS%.forEach(([sel, a, b]) => show(sel, a, b, { x: -20, y: 0 }));
      DOCS.forEach((id) => docCam(id));

      // ---------- shot moments ----------
      // hook
      punch("s01", 0.26, 0.05); punch("s02", 3.28, 0.05);
      (function () { const g = $("#wticks"); for (let k = 0; k < 60; k++) { const a = (k / 60) * Math.PI * 2, r0 = k % 5 ? 228 : 214;
          const l = document.createElementNS("http://www.w3.org/2000/svg", "line"); l.setAttribute("x1", 540 + Math.sin(a) * r0); l.setAttribute("y1", 740 - Math.cos(a) * r0);
          l.setAttribute("x2", 540 + Math.sin(a) * 240); l.setAttribute("y2", 740 - Math.cos(a) * 240); l.setAttribute("stroke", "rgba(255,255,255,0.5)"); l.setAttribute("stroke-width", k % 5 ? 3 : 6); g.appendChild(l); }
        const C = 2 * Math.PI * 250; $("#warc").style.strokeDasharray = C;
        [[5.2, 6.75, 5.3], [114.95, 115.9, 114.89]].forEach(([a, b, s]) => { const m = { v: 0 };
          tl.fromTo("#watch", { opacity: 0, scale: 0.8, transformOrigin: "540px 740px" }, { opacity: 1, scale: 1, duration: 0.25, ease: E }, a); tl.to("#watch", { opacity: 0, duration: 0.15 }, b);
          tl.fromTo(m, { v: 0 }, { v: 1, duration: 0.95, ease: "power2.inOut", onUpdate() { $("#warc").style.strokeDashoffset = C * (1 - m.v * 32 / 60);
            $("#whand").setAttribute("transform", `rotate(${m.v * 32 * 6 * 12} 540 740)`); } }, s); }); })();
      punch("s04", 8.09, 0.06);
      // s05: what a human expert said about the AI's lead (preprint Fig. 4L), set large; the real strip underneath
      (function () { const host = $("#gx-s05"); const q = el("div", "quote", "", host);
        q.innerHTML = '<div class="qk">● A HUMAN EXPERT, REVIEWING THE AGENTS\' LEAD</div><div class="qt">“Connecting DCTN1 loss to the upregulation of SREBP/cholesterol genes to compensate makes logical sense, and a quick Google Scholar search <span class="qh">found nothing directly linking the two.</span>”</div><div class="qa">PREPRINT FIG. 4L · EXPERT COMMENT</div>';
        const pr = el("div", "proof", "", host); pr.innerHTML = '<img src="assets/img/s05_strip.png" alt="" />';
        tl.fromTo(q, { opacity: 0, y: 50, rotation: -1.5 }, { opacity: 1, y: 0, rotation: -0.6, duration: 0.35, ease: "back.out(1.4)" }, 8.4);
        tl.fromTo(pr, { opacity: 0, y: 40 }, { opacity: 0.92, y: 0, duration: 0.3, ease: E }, 8.6);
        tl.to(q.querySelector(".qh"), { backgroundSize: "100% 78%", duration: 0.5, ease: "power2.inOut" }, 9.05);
        tl.to(q.querySelector(".qh"), { color: "#000", duration: 0.2 }, 9.05);
        tl.fromTo(cam("s05"), { scale: 1 }, { scale: 1.05, duration: 2.2, ease: "none" }, 8.2); })();
      // the city
      punch("s06", 10.59, 0.04);
      show("#chHouse", 13.6, 15.12, { x: -20 });
      (function () { const names = ["Dctn1", "Grin2b", "Psmb4", "Smarcc2", "Atxn1", "Tbr1"], pos = [[150, 520], [640, 430], [90, 820], [610, 760], [300, 1010], [700, 1040]];
        names.forEach((n, k) => { const e = el("div", "gtag", `left:${pos[k][0]}px;top:${pos[k][1]}px`, $("#gtags")); e.textContent = n;
          const dx = (pos[k][0] + 80 - 540) * 0.35, dy = (pos[k][1] - 740) * 0.35;
          tl.fromTo(e, { opacity: 0, scale: 0.6, x: 0, y: 0 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 15.4 + k * 0.12);
          tl.to(e, { x: dx, y: dy, scale: 1.25, duration: 1.7 - k * 0.12, ease: "none" }, 15.4 + k * 0.12); tl.to(e, { opacity: 0, duration: 0.15 }, 16.95); }); })();
      show("#chWiring", 15.35, 17.0, { x: -20 });
      // the experiment
      (function () { const p = $("#slashp"), L = 960; p.style.strokeDasharray = L; tl.set("#slash", { opacity: 1 }, 17.62);
        tl.fromTo(p, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: 0.12, ease: "power3.out" }, 17.63); tl.to("#slash", { opacity: 0, duration: 0.35 }, 17.95); })();
      flash(17.65, 0.35, 0.3, "#ff6b6b"); shake("s10", 17.65, 16, 6); punch("s10", 17.87, 0.05);
      show("#chOne", 18.2, 19.6, { x: -20 });
      pinTo("#pCut", "helix", "cut", "s11", 20.95, 21.7, 40, 0); punch("s11", 20.91, 0.05); shake("s11", 20.91, 12, 6);
      // s12: the gene wall
      (function () { const clip = el("div", "", "position:absolute;left:0;top:290px;width:1080px;height:930px;overflow:hidden;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 60px,#000 870px,transparent 930px)", $("#gx-s12"));
        const host = el("div", "", "position:absolute;left:0;top:-290px;width:1080px;height:1920px", clip); const wall = el("div", "", "position:absolute;left:0;top:0;width:2020px;height:1960px;transform-origin:0 0", host);
        const cols = 22, cw = 92, rh = 22; let di = 0;
        GENES.forEach((g, i) => { const s = el("span", "", `position:absolute;left:${(i % cols) * cw}px;top:${Math.floor(i / cols) * rh}px;font-family:Mono,monospace;font-weight:700;font-size:16px;color:var(--c${(i * 7) % 8})`, wall);
          s.textContent = g; if (g === "Dctn1") { di = i; s.style.color = "#ffb547"; s.style.textShadow = "0 0 10px rgba(255,181,71,0.9)"; } });
        const dx = (di % cols) * cw + 30, dy = Math.floor(di / cols) * rh + 8;
        for (let k = 0; k < 8; k++) wall.style.setProperty("--c" + k, "rgba(140,205,230,0.42)");
        const S0 = 2.4, S1 = 0.49;
        tl.fromTo(wall, { scale: S0, x: 540 - S0 * dx, y: 720 - S0 * dy }, { scale: S1, x: 540 - S1 * 1010, y: 760 - S1 * 975, duration: 2.1, ease: "power2.inOut" }, 21.8);
        const st = { p: 0 }; tl.fromTo(st, { p: 0 }, { p: 1, duration: 2.6, ease: "none", onUpdate() { for (let k = 0; k < 8; k++) { const ph = st.p * 3 - k / 8; const v = Math.max(0, Math.sin(ph * Math.PI * 2)) ** 3;
          const red = st.p > 0.83 ? Math.min(1, (st.p - 0.83) / 0.08) : 0;
          wall.style.setProperty("--c" + k, `rgba(${Math.round(140 + 115 * v + 115 * red)},${Math.round(205 + 50 * v - 130 * red)},${Math.round(230 + 25 * v - 140 * red)},${(0.42 + 0.5 * v + 0.3 * red).toFixed(2)})`); } } }, 21.6); })();
      // s14-s15: photographing the houses
      tl.fromTo("#vf", { opacity: 0, scale: 1.08 }, { opacity: 1, scale: 1, duration: 0.25, ease: E }, 25.55); tl.to("#vf", { opacity: 0, duration: 0.2 }, 27.82);
      flash(25.9, 0.75, 0.35); flash(26.55, 0.45, 0.3); flash(26.85, 0.45, 0.3);
      for (let k = 0; k < 14; k++) { const e = el("div", "pop", `left:${130 + rnd() * 820}px;top:${330 + rnd() * 820}px`, $("#pops")); const t = 26.0 + k * 0.1 + rnd() * 0.08;
        tl.fromTo(e, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.06 }, t); tl.to(e, { opacity: 0, scale: 1.4, duration: 0.25 }, t + 0.07); }
      (function () { const cv = $("#lights"), cx = cv.getContext("2d"); const C = 15, R = 14, w = 64, h = 64, x0 = 60, y0 = 300; const cells = [];
        for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) cells.push({ r, c, on: rnd(), off: rnd() });
        tl.fromTo("#lights", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 27.95); tl.to("#lights", { opacity: 0, duration: 0.2 }, 30.2);
        const p = { t: 27.9 }; tl.fromTo(p, { t: 27.9 }, { t: 30.4, duration: 2.5, ease: "none", onUpdate() { cx.clearRect(0, 0, 1080, 1920);
          cx.strokeStyle = "rgba(120,200,230,0.22)"; cx.lineWidth = 2; for (let c = 0; c <= C; c++) { cx.beginPath(); cx.moveTo(x0 + c * w, y0); cx.lineTo(x0 + c * w, y0 + R * h); cx.stroke(); }
          for (let r = 0; r <= R; r++) { cx.beginPath(); cx.moveTo(x0, y0 + r * h); cx.lineTo(x0 + C * w, y0 + r * h); cx.stroke(); }
          cells.forEach((q) => { const X = x0 + q.c * w, Y = y0 + q.r * h; const onT = 28.1 + q.on * 0.5, offT = 29.35 + q.off * 0.5;
            if (q.on < 0.32 && p.t > onT) { const a = Math.min(1, (p.t - onT) / 0.12); cx.fillStyle = `rgba(255,190,90,${0.38 * a})`; cx.shadowColor = "rgba(255,181,71,0.9)"; cx.shadowBlur = 22 * a; cx.fillRect(X + 14, Y + 14, w - 28, h - 28); cx.strokeStyle = `rgba(255,200,110,${0.8 * a})`; cx.lineWidth = 3; cx.strokeRect(X + 8, Y + 8, w - 16, h - 16); cx.shadowBlur = 0; }
            else if (q.on >= 0.32 && q.off < 0.55 && p.t > offT) { const a = Math.min(1, (p.t - offT) / 0.12); cx.fillStyle = `rgba(2,3,6,${0.8 * a})`; cx.fillRect(X + 2, Y + 2, w - 4, h - 4); } }); } }, 27.9); })();
      show("#chLight", 28.2, 30.15, { x: -20 });
      // s16: a mountain of photos
      (function () { const host = $("#gx-s16"); const N = 150;
        for (let k = 0; k < N; k++) { const u = rnd(), v = rnd(); const y = 1170 - 470 * (1 - Math.sqrt(u)) * 0.98 - rnd() * 24; const half = 470 * (1170 - y) / 470; const xx = 540 + (v - 0.5) * 2 * Math.max(40, 470 - half);
          const e = el("div", "photo", `left:${xx - 56}px;top:${y - 42}px;background-image:url(assets/img/s15_last.png);background-position:${-Math.round(rnd() * 420)}px ${-Math.round(80 + rnd() * 700)}px;filter:brightness(2.3) saturate(1.3) hue-rotate(${Math.round((rnd() - 0.5) * 60)}deg)`, host);
          const t = 30.35 + (k / N) * 1.9 + rnd() * 0.12, rot = (rnd() - 0.5) * 50;
          tl.fromTo(e, { opacity: 1, y: -1200 - rnd() * 300, rotation: rot * 2 }, { y: 0, rotation: rot, duration: 0.42, ease: "power2.in" }, t); } })();
      tl.fromTo("#gx-s16", { y: -60 }, { y: 40, duration: 2.9, ease: "none" }, 30.1);
      show("#rdData", 30.5, 32.75);
      // s17: months by hand
      tl.fromTo("#cal", { opacity: 0, rotation: 6, y: 30 }, { opacity: 1, rotation: 3, y: 0, duration: 0.3, ease: "back.out(1.6)" }, 33.0); tl.to("#cal", { opacity: 0, duration: 0.2 }, 36.55);
      (function () { const m = { v: 1 }; tl.fromTo(m, { v: 1 }, { v: 12, duration: 2.1, ease: "power1.in", onUpdate() { const n = Math.round(m.v); $("#calN").textContent = n; $("#calU").textContent = n > 1 ? "MONTHS" : "MONTH"; } }, 34.3);
        tl.fromTo("#calB", { scaleX: 0 }, { scaleX: 1, duration: 3.4, ease: "none" }, 33.1); })();
      punch("s17", 35.95, 0.04);
      // the detectives
      tl.fromTo("#badge", { opacity: 0, x: -60, rotation: -4 }, { opacity: 1, x: 0, rotation: -2, duration: 0.35, ease: "back.out(1.6)" }, 37.55); tl.to("#badge", { opacity: 0, duration: 0.2 }, 38.88);
      (function () { const cv = $("#copies"), cx = cv.getContext("2d"); const img = new Image(); img.src = "assets/img/s18_tile.jpg";
        const lv = { L: 0 }, rp = { v: 0 }; const steps = [[39.0, 0], [39.41, 1], [39.63, 2], [40.22, 3], [40.63, 4.4], [41.25, 5.46]];
        const draw = () => { const L = lv.L; cx.fillStyle = "#05060a"; cx.fillRect(0, 0, 900, 920); if (!img.complete || !img.naturalWidth) return;
          let n = Math.pow(2, L); if (L >= 5.45) { // the real count: 1,946 detectives, 44 per row
            const s = 20, gap = 0.5; for (let i = 0; i < 1946; i++) { const c = i % 44, r = Math.floor(i / 44); cx.drawImage(img, 10 + c * s + gap, 10 + r * s + gap, s - 2 * gap, s - 2 * gap);
              const d = Math.hypot(c - 22, r - 22) / 31, v = Math.max(0, Math.sin((rp.v - d) * Math.PI * 2.2)); if (v > 0.02 && rp.v > d) { cx.fillStyle = `rgba(255,181,71,${(0.5 * v).toFixed(3)})`; cx.fillRect(10 + c * s, 10 + r * s, s, s); } } return; }
          const s = 900 / n, m = Math.ceil(n); const gap = Math.min(4, s * 0.04);
          for (let r = 0; r < m; r++) for (let c = 0; c < m; c++) { const x = c * s, y = r * s * (920 / 900); if (x > 900 || y > 920) continue; cx.drawImage(img, x + gap, y + gap, s - 2 * gap, s * (920 / 900) - 2 * gap); } };
        tl.fromTo("#copies", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 38.95); tl.to("#copies", { opacity: 0, duration: 0.15 }, 42.1);
        steps.forEach(([t, L], k) => { if (k) tl.to(lv, { L, duration: 0.22, ease: "power2.inOut", onUpdate: draw }, t); });
        tl.fromTo(lv, { L: 0 }, { L: 0, duration: 0.01, onUpdate: draw, immediateRender: false }, 38.96);
        tl.fromTo(rp, { v: 0 }, { v: 1.6, duration: 0.85, ease: "none", onUpdate: draw, immediateRender: false }, 41.3);
        const cn = { v: 1 }; tl.fromTo(cn, { v: 1 }, { v: 1946, duration: 2.3, ease: "power3.in", onUpdate() { $("#cpN").textContent = "×" + Math.round(cn.v).toLocaleString("en-US"); } }, 39.2);
        show("#rdCopies", 39.1, 42.05); })();
      show("#chReports", 47.4, 48.7, { x: -20 });
      // s24-s25: the reference race (same 893-gene task)
      (function () { const cv = $("#raceCv"), cx = cv.getContext("2d"); const base = 1184, LX = 290, RX = 790, SW = 300, TH = 9;
        const p = { t: 48.6 };
        const sheet = (x, y, a) => { cx.fillStyle = `rgba(243,239,230,${a})`; cx.fillRect(x - SW / 2, y - TH + 1, SW, TH - 2); cx.fillStyle = "rgba(0,0,0,0.25)"; cx.fillRect(x - SW / 2, y - 2, SW, 1); };
        tl.fromTo(p, { t: 48.6 }, { t: 55.9, duration: 7.3, ease: "none", onUpdate() { const t = p.t; cx.clearRect(0, 0, 1080, 1920);
          const ia = t < 53.2 ? Math.min(1, (t - 48.8) / 0.4) : Math.max(0, 1 - (t - 53.2) / 0.3);
          if (ia > 0) { // one agent on the left; 1,946 on the right
            cx.fillStyle = `rgba(255,181,71,${ia})`; cx.shadowColor = "rgba(255,181,71,0.9)"; cx.shadowBlur = 24; cx.beginPath(); cx.arc(LX, 800, 22, 0, 6.283); cx.fill();
            cx.shadowBlur = 0; for (let i = 0; i < 1946; i++) { const c = i % 44, r = Math.floor(i / 44); const tw = 0.55 + 0.45 * Math.sin(t * 6 + i * 0.7);
              cx.fillStyle = `rgba(255,181,71,${(ia * tw).toFixed(3)})`; cx.fillRect(RX - 154 + c * 7, 642 + r * 7, 4.5, 4.5); } }
          // one AI: 11 sheets, one at a time
          for (let i = 0; i < 11; i++) { const land = 51.15 + i * 0.085; const fy = base - i * TH; if (t >= land) sheet(LX + Math.sin(i * 2.1) * 6, fy, 1);
            else if (t > land - 0.3) { const k = 1 - (land - t) / 0.3; sheet(LX, fy - 500 * (1 - k * k), 0.9); } }
          // the team: thousands, a torrent
          if (t > 53.55) { const k = Math.min(1, (t - 53.55) / 1.7), n = Math.round(7586 * (k * k * (3 - 2 * k)));
            const hgt = Math.min(base + 400, n * 0.42 * TH); // compressed scale so the stack bursts out of the frame
            const g = cx.createLinearGradient(0, base - hgt, 0, base); g.addColorStop(0, "rgba(255,214,150,0.95)"); g.addColorStop(1, "rgba(243,239,230,1)");
            cx.save(); cx.beginPath(); cx.rect(0, 300, 1080, 1620); cx.clip();
            cx.fillStyle = g; cx.fillRect(RX - SW / 2, base - hgt, SW, hgt);
            cx.fillStyle = "rgba(0,0,0,0.22)"; for (let y = base; y > base - hgt; y -= 4) cx.fillRect(RX - SW / 2, y, SW, 1);
            for (let j = 0; j < 14; j++) { const ph = (t * 3.1 + j * 0.37) % 1; sheet(RX + Math.sin(j * 3.7) * 30, base - hgt - 40 - (1 - ph) * 700, 0.85 * (k < 1 ? 1 : 0)); }
            const fg = cx.createLinearGradient(0, 300, 0, 420); fg.addColorStop(0, "rgba(4,5,10,1)"); fg.addColorStop(1, "rgba(4,5,10,0)"); cx.fillStyle = fg; cx.fillRect(RX - SW / 2 - 40, 300, SW + 80, 120);
            cx.restore(); } } }, 48.6);
        tl.fromTo("#race", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 48.85); tl.to("#race", { opacity: 0, duration: 0.2 }, 55.55);
        const a = { v: 0 }; tl.fromTo(a, { v: 0 }, { v: 11, duration: 0.95, ease: "none", onUpdate() { $("#rcL").textContent = Math.round(a.v); } }, 51.15);
        const b = { v: 0 }; tl.fromTo(b, { v: 0 }, { v: 7586, duration: 1.7, ease: "power2.inOut", onUpdate() { $("#rcR").textContent = Math.round(b.v).toLocaleString("en-US"); } }, 53.55);
        tl.fromTo("#x711", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 54.9); tl.to("#x711", { opacity: 0, duration: 0.2 }, 55.55); })();
      shake("s25", 54.47, 10, 6);
      // s26: the scientists' paper, hidden from the AI
      (function () { const bars = document.querySelectorAll("#cam-s26 .redact"); bars.forEach((b, k) => tl.to(b, { scaleX: 1, duration: 0.16, ease: "power2.out" }, 59.25 + k * 0.025)); })();
      stamp("#stHidden", 59.75, 60.62, -6); shake("s26", 59.75, 10, 6);
      stamp("#stCould", 60.78, 61.5, -6); flash(60.78, 0.2, 0.25, "#7ee787");
      // s27: the abstract's own words
      (function () { const host = $("#gx-s27"); const q = el("div", "quote", "top:330px", host);
        q.innerHTML = '<div class="qk" style="color:#6b4fc8">● THE AGENTS\' PAPER · ABSTRACT</div><div class="qt"><span class="qh">“Without access to the source manuscript, agents recovered its conclusions”</span></div>' +
          '<div class="qt"><span class="qh v">“Blinded human experts preferred distributed-agent over single-agent interpretations”</span></div>';
        const pr = el("div", "proof", "top:1010px;height:170px", host); pr.innerHTML = '<img src="assets/img/s27_strip.png" alt="" style="margin-top:-60px" />';
        tl.fromTo(q, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.4)" }, 60.6);
        tl.fromTo(pr, { opacity: 0 }, { opacity: 0.9, duration: 0.3 }, 60.8);
        const hs = q.querySelectorAll(".qh");
        tl.to(hs[0], { backgroundSize: "100% 78%", color: "#000", duration: 0.55, ease: "power2.inOut" }, 60.85);
        tl.to(hs[1], { backgroundSize: "100% 78%", color: "#000", duration: 0.65, ease: "power2.inOut" }, 61.95);
        tl.fromTo(cam("s27"), { scale: 1 }, { scale: 1.04, duration: 3.2, ease: "none" }, 60.46); })();
      camTo("s28", 540, 740, 1.06);
      // s28: three of four
      document.querySelectorAll("#judges .j").forEach((j, k) => { const t = k < 3 ? 64.97 + k * 0.12 : 65.79;
        tl.fromTo(j, { opacity: 0, y: 30, scale: 0.8 }, { opacity: k < 3 ? 1 : 0.55, y: 0, scale: 1, duration: 0.25, ease: "back.out(2)" }, t); });
      tl.to("#judges", { opacity: 0, duration: 0.2 }, 66.3);
      // s29: the clue (the Flow card carries scribbles: the real case name goes on it)
      (function () { if (!TRACK.length) return; const a = T0.s29 - HND; const e = $("#ev"); const st = { f: 0 };
        tl.fromTo("#ev", { opacity: 0 }, { opacity: 0.92, duration: 0.25 }, 67.0); tl.to("#ev", { opacity: 0, duration: 0.12 }, 68.0);
        tl.fromTo(st, { f: 0 }, { f: TRACK.length - 1, duration: (TRACK.length - 1) / 30, ease: "none", onUpdate() { const q = TRACK[Math.min(TRACK.length - 1, Math.round(st.f))];
          e.style.transform = `translate(${q[0] - 300}px, ${q[1] - 85}px) scale(${q[2] / 600})`; } }, a); })();
      tl.set(cam("s29"), { y: -190 }, 0); punch("s29", 67.21, 0.06);
      // s31: the cargo motor
      pinTo("#pHead", "walk", "head", "s31", 70.6, 71.6, 60, 40); pinTo("#pArm", "walk", "arm", "s31", 70.7, 71.6, -40, -150); pinTo("#pCargo", "walk", "cargo", "s31", 70.85, 71.6, 120, -40);
      // s33
      show("#chCut", 73.8, 74.7, { x: -20 });
      // s34: the cholesterol-making genes switch ON (the agents' finding F001)
      (function () { const G = ["Hmgcr", "Hmgcs1", "Sqle", "Ldlr", "Insig1", "Fdps", "Msmo1", "Dhcr24", "Cyp51", "Fdft1", "Nsdhl", "Srebf2", "Fasn"];
        const host = $("#gx-s34"); const sw = el("div", "swb", "", host); el("div", "sh", "", sw).textContent = "CHOLESTEROL-MAKING GENES · WHERE DCTN1 WAS CUT";
        const grid = el("div", "grid2", "", sw);
        G.forEach((g, k) => { const r = el("div", "row", "", grid); const n = el("div", "gn", "", r); n.textContent = g; const tg = el("div", "tg", "", r); const kn = el("i", "", "", tg);
          const t = 75.97 + k * 0.03; tl.to(kn, { x: 46, background: "#ffb547", boxShadow: "0 0 16px #ffb547", duration: 0.12, ease: "power2.out" }, t);
          tl.to(tg, { background: "#6b4410", duration: 0.12 }, t); tl.to(n, { color: "#ffe2b0", textShadow: "0 0 12px rgba(255,181,71,0.8)", duration: 0.12 }, t); });
        const q = el("div", "q", "", sw); const qt = el("span", "", "", q); const qb = el("b", "", "", q); qb.textContent = "— THE AGENTS' FINDING, IN THEIR WORDS";
        const txt = "“Dctn1 knockdown induced a recurrent SREBP-like cholesterol and fatty-acid biosynthesis program…”";
        const ty = { n: 0 }; tl.fromTo(ty, { n: 0 }, { n: txt.length, duration: 1.0, ease: "none", onUpdate() { qt.textContent = txt.slice(0, Math.round(ty.n)); } }, 74.85);
        tl.fromTo(sw, { opacity: 0, y: 40, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: E }, 74.7);
        tl.to(sw, { boxShadow: "0 0 90px rgba(255,181,71,0.55)", borderColor: "rgba(255,181,71,0.9)", duration: 0.2, yoyo: true, repeat: 1 }, 76.36); })();
      flash(76.36, 0.3, 0.35, "#ffb547");
      // s35: the deliveries stop
      tl.set("#frz-s35", { opacity: 1 }, 78.21); tl.fromTo(fx("s35"), { filter: "saturate(1)" }, { filter: "saturate(0.15) brightness(0.8)", duration: 0.2, immediateRender: false }, 78.21);
      stamp("#stStop", 78.25, 78.86, -7); shake("s35", 78.25, 12);
      punch("s37", 80.27, 0.06);
      // s39: the arm fails; cholesterol piles up
      pinTo("#pArmX", "jam", "arm", "s39", 83.95, 85.95, -40, -130); pinTo("#pStuck", "jam", "cargo", "s39", 84.15, 85.95, 140, -10); punch("s39", 85.28, 0.05);
      show("#chPerry", 87.45, 88.45, { x: -20 });
      // s42
      show("#chLittle", 93.3, 95.7, { x: -20 }); tl.fromTo("#littleS", { textDecorationColor: "rgba(255,91,91,0)" }, { textDecorationColor: "rgba(255,91,91,1)", duration: 0.15 }, 94.85);
      // s43: wrong place
      (function () { const P = PINS.pile; if (!P) return; const a = T0.s43 - HND; const st = { f: 0 }; const r = $("#ringPile");
        tl.fromTo(st, { f: 0 }, { f: P.length - 1, duration: (P.length - 1) / 30, ease: "none", onUpdate() { const q = P[Math.min(P.length - 1, Math.round(st.f))].heap; if (q) r.style.transform = `translate(${q[0] - 150}px, ${q[1] - 320}px)`; } }, a);
        tl.fromTo("#ringPile", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3 }, 96.9); tl.to("#ringPile", { opacity: 0, duration: 0.15 }, 98.0); })();
      pinTo("#pWrong", "pile", "heap", "s43", 96.95, 98.0, 160, -290); pinTo("#pDest", "pile", "dest", "s43", 97.3, 98.0, 0, -170); punch("s43", 96.93, 0.05);
      tl.set(cam("s43"), { y: -170 }, 0);
      show("#chFix", 98.2, 99.35, { x: -20 }); show("#chProtect", 99.6, 101.05, { x: -20 });
      // careful
      stamp("#stLead", 102.16, 103.5, -6); stamp("#stCure", 102.93, 103.5, 5); shake("s46", 102.93, 10);
      show("#chMice", 103.65, 104.5, { x: -20 }); stamp("#stPeer", 105.41, 105.92, -5);
      // s48: the preprint's own notice
      (function () { const host = $("#gx-s48"); const q = el("div", "quote", "top:420px", host);
        q.innerHTML = '<div class="qk" style="color:#b0413a">● THE AGENTS\' PAPER · BIORXIV · 16 OCT 2026</div><div class="qt">“This version posted October 16, 2026… <span class="qh">(which was not certified by peer review)</span>”</div>';
        const pr = el("div", "proof", "top:840px", host); pr.innerHTML = '<img src="assets/img/s48_strip.png" alt="" />';
        tl.fromTo(q, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.28, ease: "back.out(1.4)" }, 104.45);
        tl.fromTo(pr, { opacity: 0 }, { opacity: 0.9, duration: 0.25 }, 104.6);
        tl.to(q.querySelector(".qh"), { backgroundSize: "100% 78%", color: "#000", duration: 0.5, ease: "power2.inOut" }, 104.85);
        tl.fromTo(cam("s48"), { scale: 1 }, { scale: 1.04, duration: 1.9, ease: "none" }, 104.33); })(); show("#chLab", 106.1, 107.6, { x: -20 });
      tl.fromTo("#rdExp", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 108.74); tl.to("#rdExp", { opacity: 0, duration: 0.2 }, 109.95);
      // s51: connecting the dots
      (function () { const D = [[180, 480], [430, 380], [760, 520], [880, 860], [560, 960], [250, 900], [470, 650]]; const E2 = [[0, 1], [1, 6], [6, 2], [2, 3], [3, 4], [4, 6], [6, 5], [5, 0]];
        const ns = "http://www.w3.org/2000/svg";
        D.forEach(([x, y], k) => { const c = document.createElementNS(ns, "circle"); c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", 14); c.setAttribute("fill", "#ffb547");
          c.style.filter = "drop-shadow(0 0 10px rgba(255,181,71,0.9))"; $("#strD").appendChild(c); tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.1 }, 110.1 + k * 0.05); });
        E2.forEach(([i, j], k) => { const l = document.createElementNS(ns, "line"); l.setAttribute("x1", D[i][0]); l.setAttribute("y1", D[i][1]); l.setAttribute("x2", D[j][0]); l.setAttribute("y2", D[j][1]);
          $("#strG").appendChild(l); const L = Math.hypot(D[j][0] - D[i][0], D[j][1] - D[i][1]); l.style.strokeDasharray = L;
          tl.fromTo(l, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: 0.16, ease: "power2.out" }, 110.25 + k * 0.13); });
        tl.fromTo("#strings", { opacity: 0 }, { opacity: 1, duration: 0.15 }, 110.08); tl.to("#strings", { opacity: 0, duration: 0.15 }, 111.45); })();
      camTo("s52", 540, 760, 1.12, "power1.inOut");
      // the bookend
      punch("s53", 113.14, 0.05);
      (function () { tl.set("#ringWin", { x: 435, y: 810 }, 0); tl.fromTo("#ringWin", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, 116.05);
        tl.to("#ringWin", { scale: 0.55, y: 840, x: 395, duration: 1.4, ease: "power1.in" }, 116.35); tl.to("#ringWin", { opacity: 0, duration: 0.2 }, 117.5); })();

      // ---------- end card ----------
      tl.fromTo("#end", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 117.77);
      tl.fromTo("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, 117.92);
      tl.fromTo(["#ename", "#ehandle"], { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: E, stagger: 0.12 }, 118.17);
      tl.fromTo("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 118.62);
      tl.to("#fol", { scale: 1.06, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, 119.2);
      tl.to("#mark", { boxShadow: "0 0 140px rgba(200,255,77,0.8)", duration: 0.9, yoyo: true, repeat: 1, ease: "sine.inOut" }, 118.9);

      // ---------- global UI ----------
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      tl.fromTo(["#tag", "#bm"], { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.4 }, 0.1);
      tl.to(["#tag", "#bm"], { opacity: 0, duration: 0.4 }, 117.55);
      tl.to([".botshade", ".topshade"], { opacity: 0, duration: 0.5 }, 117.77);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);
      tl.fromTo("#black", { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, DUR - 0.45);

      // ---------- designed captions ----------
      const CAPLAY = %CAPLAY%, COVERS = %COVERS%;
      const layoutFor = (t) => (CAPLAY.find(([a, b]) => t >= a && t < b) || [0, 0, { m: "S", c: "#c8ff4d" }])[2];
      const covered = (a, b) => COVERS.some(([c0, c1]) => a < c1 && b > c0 - 0.02);
      const capsRoot = $("#caps");
      const pad2 = (n) => String(n).padStart(2, "0");
      const fmtNum = (v, target, fmt, d) => { if (fmt === "mm") { const s = Math.round(v * 60); return "00:" + pad2(Math.floor(s / 60)) + ":" + pad2(s % 60); }
        const pre = d.match(/^[^\d]*/)[0], suf = d.match(/[^\d]*$/)[0]; const n = Math.round(v); return pre + (target >= 1000 ? n.toLocaleString("en-US") : String(n)) + suf; };
      (window.CAPS || []).forEach((ch) => {
        if (covered(ch.t0, ch.t1)) return;
        const L = layoutFor(ch.t0); const col = L.c;
        const c = document.createElement("div"); c.className = "cap " + L.m; if (ch.w.some((w) => w.emph)) c.setAttribute("data-layout-allow-overlap", ""); capsRoot.appendChild(c);
        const spans = ch.w.map((w) => { const s = document.createElement("span"); const d = w.d;
          const isNum = L.m === "B" && /\d/.test(d); const hero = w.emph && L.m === "A";
          s.className = "cw dim" + (isNum ? " num" + (L.fmt === "mm" ? " clock" : "") : "") + (hero ? " hero" : "") + (w.emph && !hero ? " inl" : "");
          if (hero) { const len = d.replace(/[^A-Z0-9']/gi, "").length; const fs = Math.min(210, Math.round(930 / (len * 0.64)));
            s.style.fontSize = fs + "px"; s.style.transform = "rotate(-3deg)"; s.style.textShadow = `0 0 40px ${rgba(col, 0.55)}, 0 8px 30px rgba(0,0,0,0.5)`; }
          s.textContent = isNum && L.fmt === "mm" ? "00:00:00" : d;
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
          if (isNum) { const target = L.fmt === "mm" ? parseFloat(d) : parseFloat(d.replace(/[^\d.]/g, "")); const m = { v: 0 };
            tl.set(s, { textShadow: `0 0 40px ${rgba(col, 0.6)}, 0 8px 30px rgba(0,0,0,0.5)` }, w.s);
            tl.fromTo(m, { v: 0 }, { v: target, duration: Math.max(0.4, w.e - w.s + 0.2), ease: "power2.out", onUpdate() { s.firstChild.nodeValue = fmtNum(m.v, target, L.fmt, d); } }, w.s);
            if (L.fmt !== "mm") s.firstChild.nodeValue = fmtNum(0, target, "", d); }
        });
      });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>

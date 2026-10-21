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
      @font-face { font-family: "SerifX"; src: url("assets/fonts/serif-bi.ttf") format("truetype"); font-weight: 700; font-style: italic; }
      .shot { position: absolute; inset: 0; overflow: hidden; }
      .fx, .cam { position: absolute; inset: 0; transform-origin: 50% 45%; }
      .vid { position: absolute; object-fit: cover; }
      .still { position: absolute; }
      .bd { position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; background-size: cover; background-position: center;
        filter: brightness(0.42) saturate(0.9); }
      .desk { position: absolute; inset: 0; background:
        radial-gradient(ellipse 70% 45% at 50% 38%, rgba(255,255,255,0.06), rgba(0,0,0,0) 70%),
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: auto, 72px 72px, 72px 72px; }
      .card { position: absolute; overflow: hidden; border-radius: 26px; background: #fff;
        box-shadow: 0 40px 90px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08); }
      .card.pagecard { background: #fbfaf3; }
      .card img { position: absolute; }
      .hl { position: absolute; mix-blend-mode: multiply; border-radius: 6px; transform-origin: 0 50%; transform: scaleX(0); }
      .dchip { position: absolute; border-radius: 8px; border: 3px solid #3d7fe0; box-shadow: 0 0 16px rgba(61,127,224,0.75); background: rgba(61,127,224,0.08); opacity: 0; }
      .scan { position: absolute; left: 0; top: 0; height: 6px; background: #4f8fe8; box-shadow: 0 0 26px 8px rgba(79,143,232,0.55); opacity: 0; }
      .bookglow { position: absolute; left: 280px; top: 620px; width: 300px; height: 300px; border-radius: 50%; opacity: 0;
        background: radial-gradient(ellipse at 50% 50%, rgba(255,200,120,0.9), rgba(255,150,60,0.45) 30%, rgba(255,140,40,0) 68%); mix-blend-mode: screen; }
      .bookglow::after { content: ""; position: absolute; left: 136px; top: 112px; width: 28px; height: 76px; border-radius: 3px; background: linear-gradient(180deg, #fff3d6, #ffc46b);
        box-shadow: 0 0 18px 6px rgba(255,200,110,0.95), 0 0 60px 20px rgba(255,160,60,0.6); }
      .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 42%, rgba(4,5,10,0) 55%, rgba(4,5,10,0.55) 100%); }
      .botshade { position: absolute; left: 0; top: 1020px; width: 1080px; height: 900px; background: linear-gradient(180deg, rgba(4,5,10,0) 0%, rgba(4,5,10,0.68) 36%, rgba(4,5,10,0.86) 100%); }
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
      .credit { position: absolute; left: 60px; top: 282px; font-family: "Mono", monospace; font-weight: 500; font-size: 22px; letter-spacing: 0.08em;
        color: rgba(230,232,240,0.75); opacity: 0; }

      /* designed captions */
      .cap { position: absolute; opacity: 0; font-weight: 900; text-transform: uppercase; letter-spacing: -0.02em; line-height: 1.0; color: #fff;
        text-shadow: 0 6px 26px rgba(0,0,0,0.6), 0 2px 4px rgba(0,0,0,0.55); }
      .cap.S, .cap.B { left: 40px; width: 1000px; bottom: 470px; text-align: center; font-size: 80px; }
      .cap.A { left: 66px; width: 960px; bottom: 470px; text-align: left; font-size: 72px; }
      .cap.C { font-size: 62px; padding: 26px 30px 30px; border-radius: 26px; background: rgba(8,10,16,0.58); border: 1.5px solid rgba(255,255,255,0.16);
        box-shadow: 0 30px 70px rgba(0,0,0,0.45); transform-origin: 0 50%; }
      .cw { display: inline-block; margin: 0 0.16em; transform-origin: 50% 70%; }
      .cap.A .cw { margin: 0 0.32em 0 0; }
      .cw.dim { opacity: 0.45; }
      .cw.hero { display: block; margin: 0.16em 0 0.22em; line-height: 0.92; letter-spacing: -0.04em; transform-origin: 0 60%; position: relative; }
      .cap.S .cw.hero, .cap.B .cw.hero { transform-origin: 50% 60%; }
      .cw.hero .bar { position: absolute; left: 0.02em; bottom: -0.1em; height: 0.07em; border-radius: 0.04em; transform-origin: 0 50%; }
      .cw.num { display: block; font-size: 2.4em; letter-spacing: -0.05em; line-height: 0.95; margin: 0.02em 0; }
      .cw.num.clock { font-family: "Mono", monospace; font-weight: 700; font-size: 1.7em; letter-spacing: 0.02em; }
      .cw.inl { font-size: 1.12em; }
      .cw.serif { font-family: "SerifX", serif; font-style: italic; font-weight: 700; text-transform: none; letter-spacing: 0; }
      .strike { position: absolute; left: -2%; top: 52%; width: 104%; height: 0.09em; background: #ff5b5b; border-radius: 0.05em; transform-origin: 0 50%;
        box-shadow: 0 0 18px rgba(255,91,91,0.7); }
      .leader { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; pointer-events: none; }

      /* shot graphics */
      .spine { position: absolute; width: 30px; font-family: "Mono", monospace; font-weight: 700; font-size: 38px; line-height: 0.98; text-align: center;
        word-break: break-all; opacity: 0.95; clip-path: inset(0 0 100% 0); }
      .fun { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900; letter-spacing: -0.04em; opacity: 0; line-height: 1; }
      .fun .lbl { display: block; margin-top: 8px; font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.18em; }
      .fun .k { position: relative; display: inline-block; }
      .fun .x { position: absolute; left: -4%; top: 46%; width: 108%; height: 10px; background: #ff5b5b; border-radius: 5px; transform-origin: 0 50%; }
      .tick { position: absolute; width: 4px; height: 26px; border-radius: 2px; background: #4fd0ff; box-shadow: 0 0 10px #4fd0ff; opacity: 0; }
      .gap { position: absolute; height: 22px; border: 3px solid #4fd0ff; border-bottom: none; border-radius: 14px 14px 0 0; opacity: 0; }
      .rowhl { position: absolute; background: rgba(79,208,255,0.32); mix-blend-mode: multiply; border-radius: 4px; transform-origin: 0 50%; transform: scaleX(0); }
      .box { position: absolute; border: 5px solid #4fd0ff; border-radius: 12px; box-shadow: 0 0 22px rgba(79,208,255,0.85); opacity: 0; }
      .flag { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.12em; padding: 10px 16px; border-radius: 10px;
        background: rgba(6,8,12,0.86); border: 2px solid currentColor; opacity: 0; white-space: nowrap; }
      .crispr { position: absolute; left: 60px; width: 960px; height: 170px; border-radius: 22px; background: rgba(8,10,16,0.82); border: 2px solid rgba(255,255,255,0.14); opacity: 0; }
      .crispr .t { position: absolute; left: 26px; top: 20px; font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.14em; color: #9da2b0; }
      .gene { position: absolute; height: 44px; background: #c9ccd3; clip-path: polygon(0 0, 82% 0, 100% 50%, 82% 100%, 0 100%); }
      .arr { position: absolute; height: 44px; border-radius: 4px; background: #cfeefc; border: 2px solid #1d2230; overflow: hidden; }
      .arr i { position: absolute; top: 0; width: 9px; height: 100%; background: #12a6e8; }
      .rnap { position: absolute; width: 64px; height: 20px; border-radius: 10px; background: #12a6e8; box-shadow: 0 0 14px rgba(79,208,255,0.9); opacity: 0; }
      .ring { position: absolute; border-radius: 50%; border: 6px solid #bfe6ff; box-shadow: 0 0 24px rgba(191,230,255,0.9), inset 0 0 18px rgba(191,230,255,0.5); opacity: 0; }

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

        <!-- s05: the hook's phage -->
        <div class="ring" id="ringHook" style="left:370px;top:831px;width:200px;height:200px"></div>
        <!-- s07: DNA printed down the book spines -->
        <div id="spines"></div>
        <!-- s13: the funnel, numbers as the caption -->
        <div class="fun" id="f1" style="left:70px;width:520px;text-align:left;top:905px;font-size:92px;color:#9a9da8"><span class="k">200,000<span class="x" id="f1x"></span></span><span class="lbl">ENZYMES PULLED</span></div>
        <div class="fun" id="f2" style="left:70px;width:520px;text-align:left;top:1062px;font-size:108px;color:#e9e9ee"><span class="k">3,500<span class="x" id="f2x"></span></span><span class="lbl" style="color:#f0a07f">KEPT</span></div>
        <div class="fun" id="f3" style="left:560px;width:460px;top:930px;font-size:300px;color:#f0a07f;text-shadow:0 0 50px rgba(240,160,127,0.55)">20</div>
        <div class="flag" id="f3l" style="left:680px;top:872px;color:#f0a07f">THEN JUST</div>
        <!-- s15 -->
        <div class="flag" id="flQuote" style="left:60px;top:900px;color:#f0a07f">THE AGENT'S OWN WORDS</div>
        <!-- s16: DNA -->
        <div class="flag" id="flRep" style="left:540px;top:1230px;color:#8cc0ff">14 REPEATS</div>
        <!-- s17 -->
        <div id="ticks"></div>
        <!-- s19 -->
        <div class="box" id="artBox"></div>
        <div class="flag" id="flArt" style="color:#4fd0ff">ART · FOUND BY CLAUDE</div>
        <div class="crispr" id="crispr"><div class="t">CRISPR · SIMPLIFIED</div>
          <div class="gene" style="left:40px;top:84px;width:150px"></div><div class="gene" style="left:196px;top:84px;width:120px"></div><div class="gene" style="left:322px;top:84px;width:170px"></div>
          <div class="arr" style="left:520px;top:84px;width:400px"><i style="left:20px"></i><i style="left:62px"></i><i style="left:104px"></i><i style="left:146px"></i><i style="left:188px"></i><i style="left:230px"></i><i style="left:272px"></i><i style="left:314px"></i><i style="left:356px"></i></div>
          <div class="flag" id="flCr" style="left:640px;top:16px;font-size:20px;padding:6px 12px;color:#4fd0ff;opacity:1">REPEAT ARRAY</div></div>
        <!-- s23: short RNAs -->
        <div class="box" id="saBox"></div>
        <div id="rnas"></div>
        <div class="flag" id="flRna" style="left:300px;top:930px;color:#4fd0ff">SHORT RNA MESSAGES</div>
        <div class="flag" id="flCr2" style="left:250px;top:1010px;color:#c8ff4d">✓ CRISPR WORKS THIS WAY TOO</div>
        <!-- s25: phages -->
        <div class="ring" id="ringPh" style="width:150px;height:150px"></div>
        <div class="flag" id="flBact" style="left:640px;top:760px;color:#bfe6ff">BACTERIUM</div>

        %LABELS%
        <div class="credit" id="crPhage" data-layout-ignore>PHOTO: GRAHAM BEARDS · CC BY-SA 3.0</div>

        <div class="grain" id="grain"></div>
        <div class="progress" id="prog" style="background:var(--lime)"></div>
        <div class="tag2" id="tag"><span class="dot"></span>AI SCIENCE · TRUE STORY</div>
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
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span><span style="font-family:SerifX;font-style:italic;font-weight:700">Aa</span></div>
      </div>

      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%, HND = %H%;
      const SH = %SHOTSJS%;
      const GEO = %GEO%;
      const FIG = %FIG%;
      const COL = %COL%;
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out";
      const fx = (id) => "#fx-" + id, cam = (id) => "#cam-" + id;
      const T0 = Object.fromEntries(SH.map((s) => [s.id, s.t0])), T1 = Object.fromEntries(SH.map((s) => [s.id, s.t1]));
      const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; };
      const el = (tag, cls, css, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css; (parent || $("#ui")).appendChild(e); return e; };

      // ---------- shots: visibility and default camera ----------
      const CUSTOM_CAM = new Set(["s05", "s09", "s10", "s13", "s15", "s24", "s25", "s26", "s29", "s20", "s35"]);
      SH.forEach((s, i) => {
        tl.set(fx(s.id), { opacity: i === 0 ? 1 : 0 }, 0);
        const a = Math.max(0, s.t0 - HND), b = s.t1 + HND;
        if (CUSTOM_CAM.has(s.id)) return;
        const card = ["PAGE", "IMG", "FIG", "DNA", "GRID"].includes(s.k);
        tl.fromTo(cam(s.id), { scale: 1 }, { scale: card ? 1.035 : 1.07, duration: b - a, ease: "none" }, a);
      });
      const flash = (t, a, d, c) => { tl.set("#flash", { background: c || "#fff" }, t); tl.fromTo("#flash", { opacity: a }, { opacity: 0, duration: d || 0.35, ease: "power2.out", immediateRender: false }, t); };
      const cardIn = (id, t) => { const c = document.querySelectorAll("#cam-" + id + " .card");
        tl.fromTo(c, { opacity: 0, scale: 0.86, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.6)", stagger: 0.1 }, t); };
      const TR = {
        whip(A, B, T) { tl.fromTo(fx(B), { opacity: 1, x: 1080, filter: "blur(22px)" }, { x: 0, filter: "blur(0px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16);
          tl.to(fx(A), { x: -760, filter: "blur(22px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16); tl.set(fx(A), { opacity: 0 }, T + 0.14); },
        slideup(A, B, T) { tl.fromTo(fx(B), { opacity: 1, y: 1920, filter: "blur(22px)" }, { y: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17);
          tl.to(fx(A), { y: -1100, filter: "blur(22px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17); tl.set(fx(A), { opacity: 0 }, T + 0.15); },
        zoom(A, B, T) { tl.to(fx(A), { scale: 1.45, filter: "blur(18px)", opacity: 0, duration: 0.26, ease: "power2.in" }, T - 0.16);
          tl.fromTo(fx(B), { opacity: 0, scale: 0.84, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: E }, T - 0.1); flash(T - 0.02, 0.25, 0.3); },
        flash(A, B, T, c) { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T); flash(T, 0.55, 0.42, c); },
        dip(A, B, T) { tl.to("#black", { opacity: 1, duration: 0.16, ease: "power1.in" }, T - 0.16); tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T);
          tl.to("#black", { opacity: 0, duration: 0.3, ease: "power1.out" }, T); },
        glitch(A, B, T) { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T);
          [[0, 34, "hue-rotate(80deg) saturate(2)"], [0.033, -26, "hue-rotate(-60deg)"], [0.066, 16, "none"], [0.1, -8, "none"], [0.133, 0, "none"]].forEach(([dt, x, f]) => tl.set(fx(B), { x, filter: f }, T + dt));
          flash(T, 0.3, 0.25, "#4fd0ff"); },
        card(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out" }, T - 0.12); tl.set(fx(A), { opacity: 0 }, T + 0.12); cardIn(B, T - 0.05); },
        fade(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.inOut" }, T - 0.25); tl.set(fx(A), { opacity: 0 }, T + 0.26); },
      };
      const CUTS = [["s01", "s02", "whip"], ["s02", "s03", "flash", "#7cc4ff"], ["s03", "s04", "card"], ["s04", "s05", "zoom"], ["s05", "s06", "dip"],
        ["s06", "s07", "slideup"], ["s07", "s08", "whip"], ["s08", "s09", "zoom"], ["s09", "s10", "card"], ["s10", "s11", "glitch"],
        ["s11", "s12a", "flash", "#ffd36b"], ["s12a", "s12b", "whip"], ["s12b", "s12c", "whip"], ["s12c", "s12d", "whip"], ["s12d", "s12e", "flash", "#c8ff4d"],
        ["s12e", "s13", "card"], ["s13", "s14", "dip"], ["s14", "s15", "card"], ["s15", "s16", "zoom"], ["s16", "s17", "slideup"],
        ["s17", "s18a", "glitch"], ["s18a", "s18b", "whip"], ["s18b", "s19", "card"], ["s19", "s20", "slideup"], ["s20", "s21a", "zoom"],
        ["s21a", "s21b", "whip"], ["s21b", "s22", "whip"], ["s22", "s23", "card"], ["s23", "s24", "slideup"], ["s24", "s25", "dip"],
        ["s25", "s26", "card"], ["s26", "s27", "slideup"], ["s27", "s28a", "flash", "#ffd36b"], ["s28a", "s28b", "whip"], ["s28b", "s29", "card"], ["s29", "s30", "zoom"],
        ["s30", "s31a", "whip"], ["s31a", "s31b", "flash", "#7cc4ff"], ["s31b", "s31c", "whip"], ["s31c", "s32", "dip"], ["s32", "s33", "whip"],
        ["s33", "s34", "zoom"], ["s34", "s35", "fade"]];
      CUTS.forEach(([A, B, k, c]) => TR[k](A, B, T0[B], c));
      tl.fromTo("#flash", { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);

      // ---------- helpers ----------
      const show = (sel, t0, t1, from) => { tl.fromTo(sel, Object.assign({ opacity: 0, y: 14 }, from || {}), { opacity: 1, y: 0, x: 0, scale: 1, duration: 0.3, ease: E }, t0);
        tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const pop = (sel, t0, t1) => { tl.fromTo(sel, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, t0); tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const punch = (id, t, s) => { tl.fromTo(fx(id), { scale: 1 }, { scale: 1 + (s || 0.06), duration: 0.12, ease: "power2.out", immediateRender: false }, t);
        tl.to(fx(id), { scale: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.12); };
      const camTo = (id, ox, oy, s1, ease) => { const a = Math.max(0, T0[id] - HND), b = T1[id] + HND;
        tl.set(cam(id), { transformOrigin: `${ox}px ${oy}px` }, 0); tl.fromTo(cam(id), { scale: 1 }, { scale: s1, duration: b - a, ease: ease || "power1.inOut" }, a); };
      const hlCenter = (id) => { const g = GEO[id]; return [g[0] + g[2] / 2, g[1] + g[3] * 0.45]; };

      // highlights on cards
      %HLJS%.forEach(([id, t, d]) => tl.to("#" + id, { scaleX: 1, duration: d, ease: "power2.inOut" }, t));
      // source labels
      %LABJS%.forEach(([sel, a, b]) => show(sel, a, b, { x: -20, y: 0 }));
      show("#crPhage", 5.95, 7.7, { y: 0 }); show("#crPhage", 55.6, 60.75, { y: 0 });

      // ---------- shot moments ----------
      // s01-s03: hook
      punch("s01", 1.43, 0.06); punch("s02", 1.99, 0.06);
      // s04: Anthropic's post on X
      // s05: phage, hook
      (function () { const img = $("#st-s05"); img.style.cssText = "left:-32px;top:-329px;width:1920px"; })();
      camTo("s05", 470, 931, 1.16, "power1.out");
      tl.fromTo("#ringHook", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }, 5.92);
      tl.to("#ringHook", { scale: 1.1, duration: 0.4, yoyo: true, repeat: 2, ease: "sine.inOut" }, 6.25); tl.to("#ringHook", { opacity: 0, duration: 0.2 }, 7.6);
      // s07: DNA printed down the spines
      (function () { const xs = [331, 452, 572, 693, 813, 934]; const B = "ATGC"; let seed = 7;
        const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
        xs.forEach((x, k) => { let s = ""; for (let i = 0; i < 16; i++) s += B[Math.floor(rnd() * 4)];
          const e = el("div", "spine", `left:${x - 15}px;top:${480 + (k % 2) * 18}px;color:${COL.s07};text-shadow:0 0 14px ${rgba(COL.s07, 0.85)}`, $("#spines")); e.textContent = s;
          tl.to(e, { clipPath: "inset(0 0 0% 0)", duration: 0.55, ease: "power1.inOut" }, 10.55 + k * 0.13);
          tl.to(e, { opacity: 0, duration: 0.2 }, 12.7); });
        tl.to(".spine", { textShadow: `0 0 26px ${rgba(COL.s07, 1)}`, duration: 0.2, yoyo: true, repeat: 1 }, 11.85); })();
      // s09: one unread book glows
      camTo("s09", 430, 770, 1.3, "power2.inOut");
      tl.fromTo("#bookglow", { opacity: 0 }, { opacity: 1, duration: 0.6 }, 14.55); tl.to("#bookglow", { opacity: 0.6, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, 15.2);
      // s10: the post's headline
      camTo("s10", 540, 420, 1.1);
      // s11: 950 agents
      (function () { const cv = $("#agents"), cx = cv.getContext("2d"); const C = 38, R = 25, P = 24, X0 = (1080 - C * P) / 2 + 4, Y0 = 330;
        const cells = []; let seed = 11; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
        for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) { const dx = c - (C - 1) / 2, dy = (r - (R - 1) / 2) * 1.2; cells.push({ x: X0 + c * P, y: Y0 + r * P, d: Math.hypot(dx, dy) + rnd() * 3, ph: rnd() * 6.28 }); }
        const dmax = Math.max(...cells.map((c) => c.d)); const g = { p: 0, t: 0 };
        const draw = () => { cx.clearRect(0, 0, 1080, 1920);
          const lit = g.p * dmax; const glow = cx.createRadialGradient(540, Y0 + R * P / 2, 10, 540, Y0 + R * P / 2, 560);
          glow.addColorStop(0, `rgba(217,119,87,${0.28 * g.p})`); glow.addColorStop(1, "rgba(217,119,87,0)"); cx.fillStyle = glow; cx.fillRect(0, 0, 1080, 1200);
          cells.forEach((c) => { const on = c.d <= lit; const tw = 0.65 + 0.35 * Math.sin(g.t * 9 + c.ph);
            cx.fillStyle = on ? `rgba(240,160,127,${tw})` : "rgba(70,74,88,0.55)"; cx.beginPath(); cx.roundRect(c.x, c.y, 16, 16, 4); cx.fill();
            if (on && tw > 0.95) { cx.fillStyle = "rgba(255,236,226,0.9)"; cx.fillRect(c.x + 5, c.y + 5, 6, 6); } }); };
        tl.fromTo(g, { p: 0 }, { p: 1, duration: 1.1, ease: "power1.in", onUpdate: draw }, 19.22);
        tl.fromTo(g, { t: 0 }, { t: 3.5, duration: 3.5, ease: "none", onUpdate: draw }, 19.15); })();
      // s12: burst punches
      punch("s12b", 23.34, 0.05); punch("s12d", 24.4, 0.05);
      // s13: the funnel on the real paragraph
      camTo("s13", 540, 560, 1.06);
      tl.fromTo("#f1", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, 26.33);
      tl.fromTo("#f1x", { scaleX: 0, rotation: -3 }, { scaleX: 1, rotation: -3, duration: 0.22, ease: "power2.out" }, 26.62); tl.to("#f1", { opacity: 0.45, duration: 0.2 }, 26.7);
      tl.fromTo("#f2", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.24, ease: "power4.out" }, 26.66);
      tl.fromTo("#f2x", { scaleX: 0, rotation: 3 }, { scaleX: 1, rotation: 3, duration: 0.22, ease: "power2.out" }, 28.3); tl.to("#f2", { opacity: 0.45, duration: 0.2 }, 28.4);
      tl.fromTo("#f3l", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.25 }, 28.3);
      tl.fromTo("#f3", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, 29.07);
      flash(29.07, 0.2, 0.3, "#f0a07f"); punch("s13", 29.07, 0.04);
      tl.to(["#f1", "#f2", "#f3", "#f3l"], { opacity: 0, duration: 0.18 }, 29.72);
      // s14: one agent notices (C caption carries the leader)
      // s15: the agent's own words
      camTo("s15", ...hlCenter("s15"), 1.12); show("#flQuote", 32.5, 34.35, { x: -20, y: 0 });
      // s16: the raw DNA, scanned
      (function () { const g = GEO.s16, h = g[3]; const t0 = 34.58, dur = 1.5;
        tl.set("#scan", { opacity: 1, y: 0 }, t0); tl.to("#scan", { y: h, duration: dur, ease: "none" }, t0); tl.to("#scan", { opacity: 0, duration: 0.15 }, t0 + dur);
        tl.to("#dnalit", { clipPath: "inset(0 0 0% 0)", duration: dur, ease: "none" }, t0);
        document.querySelectorAll(".dchip").forEach((c) => { const y = parseFloat(c.style.top) / h; const t = t0 + y * dur;
          tl.fromTo(c, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power3.out" }, t); });
        tl.to(".dchip", { boxShadow: "0 0 30px rgba(79,143,232,1)", duration: 0.25, yoyo: true, repeat: 1 }, 36.15); })();
      show("#flRep", 36.1, 36.9, { x: -20, y: 0 });
      // s17: evenly spaced, like lines on a page
      (function () { FIG.ticks.forEach(([x, y], k) => { const t = el("div", "tick", `left:${x - 2}px;top:${y - 44}px`, $("#ticks"));
          tl.fromTo(t, { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.12 }, 37.05 + k * 0.045);
          if (k) { const [px] = FIG.ticks[k - 1]; const gp = el("div", "gap", `left:${px + 3}px;top:${y - 62}px;width:${x - px - 6}px`, $("#ticks"));
            tl.fromTo(gp, { opacity: 0, scaleX: 0.3 }, { opacity: 1, scaleX: 1, duration: 0.14 }, 37.3 + k * 0.045); } });
        FIG.rows.forEach(([x, y, w, h], k) => { const r = el("div", "rowhl", `left:${x}px;top:${y}px;width:${w}px;height:${h}px`, $("#ticks"));
          tl.to(r, { scaleX: 1, duration: 0.16, ease: "power2.out" }, 38.15 + k * 0.08); });
        tl.to("#ticks", { opacity: 0, duration: 0.15 }, 39.5); })();
      // s18: headlines
      punch("s18a", 39.95, 0.04); punch("s18b", 40.45, 0.04);
      // s19: ART beside CRISPR
      (function () { const [x, y, w, h] = FIG.art; $("#artBox").style.cssText = `left:${x - 10}px;top:${y - 10}px;width:${w + 20}px;height:${h + 20}px`;
        const fl = $("#flArt"); fl.style.left = "70px"; fl.style.top = `${GEO.s19[1] + GEO.s19[3] + 26}px`;
        $("#crispr").style.top = `${GEO.s19[1] + GEO.s19[3] + 96}px`; })();
      tl.fromTo("#artBox", { opacity: 0, scale: 1.15 }, { opacity: 1, scale: 1, duration: 0.25, ease: E }, 41.6); tl.to("#artBox", { opacity: 0, duration: 0.15 }, 43.12);
      show("#flArt", 41.7, 43.12, { x: -20, y: 0 });
      tl.fromTo("#crispr", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, 42.45); tl.to("#crispr", { opacity: 0, duration: 0.15 }, 43.12);
      // s20: the Nobel
      camTo("s20", 540, 820, 1.12);
      // s23: copied into short RNAs
      (function () { const [x, y, w, h] = FIG.sa1; $("#saBox").style.cssText = `left:${x - 8}px;top:${y - 8}px;width:${w + 16}px;height:${h + 16}px`;
        FIG.rna.forEach(([rx, ry, rw], k) => { const p = el("div", "rnap", `left:${rx + rw / 2 - 32}px;top:${ry - 10}px`, $("#rnas"));
          tl.fromTo(p, { opacity: 0, x: 0, y: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.2 }, 50.3 + k * 0.22);
          tl.to(p, { x: 300 + k * 110 - (rx + rw / 2), y: 860 - ry, rotation: (k - 1) * 8, duration: 0.6, ease: "power2.inOut" }, 50.55 + k * 0.22); }); })();
      tl.fromTo("#saBox", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 50.2); tl.to("#saBox", { opacity: 0, duration: 0.2 }, 51.3);
      show("#flRna", 51.1, 53.35, { y: 10 }); show("#flCr2", 52.1, 53.35, { y: 10 }); tl.to("#rnas", { opacity: 0, duration: 0.15 }, 53.35);
      // s24: we don't yet know
      camTo("s24", ...hlCenter("s24"), 1.12);
      // s25: phages on a bacterium; music drops on "Nobody knows"
      (function () { const img = $("#st-s25"); img.style.cssText = "left:-60px;top:0;height:1920px";
        const r = $("#ringPh"); r.style.left = "179px"; r.style.top = "943px"; })();
      camTo("s25", 254, 1018, 1.18, "none");
      tl.fromTo("#ringPh", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, 58.65); tl.to("#ringPh", { opacity: 0, duration: 0.2 }, 60.75);
      show("#flBact", 59.9, 60.75, { y: 10 });
      punch("s25", 56.97, 0.05);
      // s26: Feng Zhang
      camTo("s26", ...hlCenter("s26"), 1.08);
      // s27: critics
      punch("s27", 64.3, 0.03);
      // s28-s29
      camTo("s29", ...hlCenter("s29"), 1.12);
      punch("s29", 70.0, 0.05);
      // s31: the AI
      punch("s31c", 73.96, 0.07); flash(73.97, 0.18, 0.3, "#c8ff4d");

      // ---------- end card ----------
      tl.fromTo("#end", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 81.0);
      tl.fromTo("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, 81.15);
      tl.fromTo(["#ename", "#ehandle"], { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: E, stagger: 0.12 }, 81.4);
      tl.fromTo("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 81.85);
      tl.to("#fol", { scale: 1.06, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, 82.4);
      tl.to("#mark", { boxShadow: "0 0 140px rgba(200,255,77,0.8)", duration: 0.9, yoyo: true, repeat: 2, ease: "sine.inOut" }, 82.2);

      // ---------- global UI ----------
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      tl.fromTo(["#tag", "#bm"], { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.4 }, 0.1);
      tl.to(["#tag", "#bm"], { opacity: 0, duration: 0.4 }, 80.8);
      tl.to([".botshade", ".topshade"], { opacity: 0, duration: 0.5 }, 81.0);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);
      tl.fromTo("#black", { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, DUR - 0.45);

      // ---------- designed captions ----------
      const CAPLAY = %CAPLAY%, COVERS = %COVERS%;
      const layoutFor = (t) => (CAPLAY.find(([a, b]) => t + 0.05 >= a && t + 0.05 < b) || [0, 0, { m: "S", c: "#c8ff4d" }])[2];
      const covered = (a, b) => COVERS.some(([c0, c1]) => a < c1 && b > c0 - 0.02);
      const capsRoot = $("#caps");
      const leaders = new Map();
      const fmtNum = (v, target, fmt) => { if (fmt === "clock") { const s = Math.round(v * 3600); return String(Math.floor(s / 3600)).padStart(2, "0") + ":" + String(Math.floor((s % 3600) / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); }
        const n = Math.round(v); return target >= 10000 ? n.toLocaleString("en-US") : String(n); };
      (window.CAPS || []).forEach((ch) => {
        if (covered(ch.t0, ch.t1)) return;
        const L = layoutFor(ch.t0); const col = L.c;
        const c = document.createElement("div"); c.className = "cap " + L.m; if (ch.w.some((w) => w.emph)) c.setAttribute("data-layout-allow-overlap", ""); capsRoot.appendChild(c);
        if (L.m === "C") { c.style.left = L.px + "px"; c.style.top = L.py + "px"; c.style.width = L.pw + "px"; c.style.transform = "perspective(900px) rotateY(9deg) rotateZ(-1.5deg)";
          const key = L.px + "," + L.py; if (!leaders.has(key)) { const sv = document.createElementNS("http://www.w3.org/2000/svg", "svg"); sv.setAttribute("class", "leader"); sv.setAttribute("viewBox", "0 0 1080 1920");
            const ax = L.px + L.pw * (L.tx > L.px + L.pw / 2 ? 0.75 : 0.3), ay = L.ty < L.py ? L.py : L.py + 190, mx = (ax + L.tx) / 2;
            const dpath = `M${ax} ${ay} C ${ax} ${(ay + L.ty) / 2}, ${mx} ${L.ty}, ${L.tx} ${L.ty}`; sv.innerHTML = `<path d="${dpath}" stroke="rgba(0,0,0,0.55)" stroke-width="11" fill="none" stroke-linecap="round"/><path d="${dpath}" stroke="${col}" stroke-width="6" fill="none" stroke-linecap="round"/>` +
              `<circle cx="${L.tx}" cy="${L.ty}" r="14" fill="none" stroke="${col}" stroke-width="5"/><circle cx="${L.tx}" cy="${L.ty}" r="30" fill="none" stroke="${rgba(col, 0.45)}" stroke-width="3"/>`;
            $("#ui").insertBefore(sv, capsRoot); leaders.set(key, { sv, a: ch.t0, b: ch.t1 }); } else leaders.get(key).b = ch.t1; }
        const spans = ch.w.map((w) => { const s = document.createElement("span"); let d = w.d === "AIS" ? "AIs" : w.d; if (d === "AIs") s.style.textTransform = "none";
          const isNum = L.m === "B" && /\d/.test(d); const hero = w.emph && (L.m === "A" || L.m === "C");
          s.className = "cw dim" + (isNum ? " num" + (L.fmt === "clock" ? " clock" : "") : "") + (hero ? " hero" : "") + (w.emph && !hero ? " inl" : "");
          if (hero) { const len = d.replace(/[^A-Z0-9']/gi, "").length; const fs = Math.min(L.m === "C" ? 124 : 210, Math.round((L.m === "C" ? L.pw - 60 : 930) / (len * 0.64)));
            s.style.fontSize = fs + "px"; s.style.transform = "rotate(-3deg)"; s.style.textShadow = `0 0 40px ${rgba(col, 0.55)}, 0 8px 30px rgba(0,0,0,0.5)`; }
          if (L.serif && d.replace(/[^A-Z]/g, "") === L.serif) { s.classList.add("serif"); d = "“Eureka!”"; }
          s.textContent = isNum && L.fmt === "clock" ? "00:00:00" : d;
          if (hero) { const bar = document.createElement("span"); bar.className = "bar"; bar.style.width = "96%"; bar.style.background = col; bar.style.boxShadow = `0 0 20px ${col}`; s.appendChild(bar); }
          if (s.classList.contains("serif")) { const k = document.createElement("span"); k.className = "strike"; s.appendChild(k); s.style.position = "relative"; }
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
            tl.fromTo(m, { v: 0 }, { v: target, duration: Math.max(0.35, w.e - w.s + 0.15), ease: "power2.out", onUpdate() { s.firstChild.nodeValue = fmtNum(m.v, target, L.fmt); } }, w.s);
            if (L.fmt !== "clock") s.firstChild.nodeValue = "0"; }
          const st = s.querySelector(".strike"); if (st) tl.fromTo(st, { scaleX: 0, rotation: -4 }, { scaleX: 1, rotation: -4, duration: 0.18, ease: "power2.out" }, 77.92);
        });
      });
      leaders.forEach(({ sv, a, b }) => { tl.fromTo(sv, { opacity: 0 }, { opacity: 1, duration: 0.25 }, a + 0.1); tl.set(sv, { opacity: 0 }, b); });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>

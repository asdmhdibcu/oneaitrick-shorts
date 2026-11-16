<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <script src="captions_final.js"></script>
    <link rel="stylesheet" href="assets/base.css" />
    <style>
      /* Short #19: Lemo-Opuscar's Mid-century Cartoon look (fonts: SIL Open Font Licence) */
      @font-face { font-family: "Jost"; src: url("assets/fonts/jost-latin-500-normal.woff2") format("woff2"); font-weight: 500; }
      @font-face { font-family: "Jost"; src: url("assets/fonts/jost-latin-600-normal.woff2") format("woff2"); font-weight: 600; }
      @font-face { font-family: "Jost"; src: url("assets/fonts/jost-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
      @font-face { font-family: "Oleo Script"; src: url("assets/fonts/oleo-script-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
      @font-face { font-family: "Alfa Slab One"; src: url("assets/fonts/alfa-slab-one-latin-400-normal.woff2") format("woff2"); font-weight: 400; }
      #root { background: #F4EAD5; }
      #film { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .hidden-src { position: absolute; left: -9999px; top: 0; width: 10px; height: 10px; }

      /* captions: karaoke on the style's paper caption card, keyword pops on a coloured box */
      #caps { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .cap { position: absolute; left: 30px; width: 1020px; top: 1258px; text-align: center; opacity: 0; }
      .cap .cb { display: inline-block; max-width: 1000px; padding: 10px 26px 14px; border-radius: 24px; background: #FBF6EA; border: 5px solid #2B2420;
        box-shadow: 8px 7px 0 #E6D8BC; font-family: "Jost", sans-serif; font-weight: 700; font-size: 70px; line-height: 1.08; text-transform: uppercase;
        letter-spacing: 0.01em; color: #2B2420; }
      .cw { display: inline-block; margin: 0 0.1em; border-radius: 12px; }
      .cw.dim { opacity: 0.38; }
      .cw.pop { padding: 0 0.14em; }

      /* end card (brand), over the mirrored first frame */
      #end { position: absolute; inset: 0; opacity: 0; }
      #end .dim { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(30,24,20,0.78), rgba(30,24,20,0.9)); }
      .mark { position: absolute; left: 430px; top: 470px; width: 220px; height: 220px; border-radius: 52px; background: var(--lime);
        display: flex; align-items: flex-end; justify-content: center; gap: 8px; padding-bottom: 50px; box-shadow: 0 0 80px rgba(200,255,77,0.45); }
      .mark .one { font-weight: 900; font-size: 154px; line-height: 0.73; color: #0b0c10; letter-spacing: -0.06em; }
      .mark .cur { width: 42px; height: 16px; border-radius: 3px; background: #0b0c10; }
      .etitle { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900; letter-spacing: -0.05em; line-height: 0.95; white-space: nowrap; color: #f5f5f2; }
      .cta { position: absolute; display: inline-flex; align-items: center; gap: 16px; padding: 22px 36px; border-radius: 999px; background: var(--lime);
        color: #0b0c10; font-weight: 850; font-size: 42px; letter-spacing: -0.01em; white-space: nowrap; }
      .fontwarm { position: absolute; left: -9999px; top: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="1080" data-height="1920">
      <div id="stagec" class="clip" data-start="0" data-duration="%DUR%" style="z-index: 10">
        <canvas id="film" width="1080" height="1920"></canvas>
        <img id="p01a" class="hidden-src" src="assets/pages/p01a.png" alt="" />
      </div>
      <div id="ui" class="clip" data-start="0" data-duration="%DUR%" style="z-index: 100">
        <div id="end">
          <div class="mark" id="mark"><span class="one">1</span><span class="cur"></span></div>
          <div class="etitle" id="ename" style="top:760px;font-size:110px">One <span style="color:var(--lime)">AI</span> Trick</div>
          <div class="etitle" id="ehandle" style="top:890px;font-family:Mono, monospace;font-weight:500;font-size:40px;letter-spacing:0.04em;color:#cfc7bb">@oneaitrick</div>
          <div style="position:absolute;left:0;top:990px;width:1080px;display:flex;justify-content:center"><div class="cta" id="fol" style="position:relative;left:auto;top:auto">+ Follow for AI, explained</div></div>
        </div>
        <div id="caps"></div>
        <div class="fontwarm"><span style="font-family:Jost;font-weight:700">Aa</span><span style="font-family:Jost;font-weight:600">Aa</span><span style="font-family:'Oleo Script';font-weight:700">Aa</span><span style="font-family:'Alfa Slab One'">Aa</span><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span></div>
      </div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%;
      const WS = %WS%, WE = %WE%;
      const PAGES = %PAGES%, POPS = %POPS%;
      const w = (k) => WS[k];
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const el = (tag, cls, css, html, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css;
        if (html !== undefined) e.innerHTML = html; parent.appendChild(e); return e; };
      const fin = (sel, from, to, t) => tl.fromTo(sel, from, Object.assign({ immediateRender: false }, to), t);

      // ---------- the seek-safe painter: one clock redraws the canvas from the time alone ----------
      const PAINT = [];
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate() { const T = clock.t; PAINT.forEach((f) => f(T)); } }, 0);

      // ===================================================== the picture =====================================================
      %TOONJS%
      %FILMJS%

      // ---------- end card: in over the mirrored first frame on "Follow", out for the last line ----------
      const tF = w(151), tA = w(158);
      gsap.set("#end", { opacity: 0 });
      fin("#end", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, tF - 0.05);
      fin("#mark", { scale: 0.6, rotate: -8 }, { scale: 1, rotate: 0, duration: 0.5, ease: "back.out(2.2)" }, tF);
      fin("#ename", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, tF + 0.12);
      fin("#ehandle", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, tF + 0.22);
      fin("#fol", { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }, tF + 0.32);
      tl.to("#end", { opacity: 0, duration: 0.12, ease: "power2.in" }, tA - 0.14);

      // ---------- captions: the spoken word lights up; keyword pops bounce on a coloured box ----------
      const CAPS = (window.CAPS || []).map((c) => ({ t0: c.t0, t1: c.t1, w: c.w.map((x) => ({ d: x.d, s: x.s, e: x.e, em: x.emph })) }));
      const capsRoot = $("#caps");
      const popAt = (s) => POPS.find((p) => Math.abs(p.t - s) < 0.01);
      CAPS.forEach((ch) => {
        const c = el("div", "cap", "", undefined, capsRoot);
        const cb = el("span", "cb", "", undefined, c);
        const spans = ch.w.map((x) => { const pp = popAt(x.s); const s = el("span", "cw dim" + (pp ? " pop" : ""), "", x.d, cb); return { s, x, pp }; });
        tl.fromTo(c, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }, ch.t0);
        tl.set(c, { opacity: 0 }, ch.t1);
        spans.forEach(({ s, x, pp }, k) => {
          if (pp) { tl.set(s, { opacity: 1, color: "#FBF6EA", backgroundColor: pp.col }, x.s);
            fin(s, { scale: 1 }, { scale: 1.15, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, x.s); return; }
          tl.set(s, { opacity: 1 }, x.s); }); });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
      PAINT.forEach((f) => f(0));   // frame one is painted even if a seek to 0 fires no update
      // canvas text needs the fonts: repaint the current frame once they are in
      Promise.all(["700 40px Jost", "600 40px Jost", "700 40px 'Oleo Script'", "40px 'Alfa Slab One'"].map((f) => document.fonts.load(f)))
        .then(() => document.fonts.ready).then(() => PAINT.forEach((f) => f(clock.t)));
      document.getElementById("p01a").addEventListener("load", () => PAINT.forEach((f) => f(clock.t)));
    </script>
  </body>
</html>

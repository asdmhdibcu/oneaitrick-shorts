"""Write index.html for Short #5 from the edit decision list (edl.py) and work/meta.json.
Every shot is a timed .clip holding .fx (transitions) > .cam (camera moves) > footage or an evidence card.
Usage: python3 make_index.py
"""
import json

from edl import SHOTS, H

DUR = 78.3
META = json.load(open("work/meta.json"))
CARD = {  # evidence cards: (left, top, display width) and the still blurred behind them
    "s03": (60, 420, 960, "s02_last"),
    "s08b": (40, 640, 1000, "s08_freeze"),
    "s10": (20, 470, 1040, "s09_last"),
    "s15b": (170, 290, 740, "s15_last"),
    "s20b": (40, 300, 1000, "s20_last"),
    "s21": (40, 640, 1000, None),
}
GRID_TILE = (340, 213, 16)  # tile w, h, gap for the 8 real robots


def vid(src, t0, d, css, ms=0.0):
    vidn = "v-" + src.split("/")[-1].split(".")[0]
    d = min(d, DUR - t0)
    return (f'<video id="{vidn}" class="vid" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-media-start="{ms:.3f}" style="{css}"></video>')


blocks = []
for z, (sid, t0, t1, src, sin, rate, ex) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:  # first shot: the file still starts H before the cut, so skip into it
        a, d, ms = 0.0, d + (t0 - H), H - t0
    inner = ""
    if src.startswith("C"):
        inner = vid(f"assets/clips/{sid}.mp4", a, d, "left:0;top:0;width:1080px;height:1920px", ms)
        if "freeze" in ex:
            inner += f'<img class="frz" id="frz-{sid}" src="assets/img/{sid}_freeze.png" alt="" />'
    else:
        left, top, w, bd = CARD.get(sid, (0, 0, 1080, None))
        bdcss = f"background-image:url(assets/img/{bd}.png)" if bd else "background:#0b0c10"
        inner = f'<div class="bd" style="{bdcss}"></div><div class="desk"></div>'
        if src == "PDF":
            inner += (f'<div class="card paper" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:602px">'
                      f'<img src="assets/img/paper_top.png" alt="" style="width:{w}px" />'
                      f'<div class="hl" id="hl-title" style="left:236px;top:144px;width:174px;height:36px"></div></div>')
        elif src == "PVSTILL":
            mw, mh = META[sid]
            inner += (f'<div class="card" id="card-{sid}" style="left:{left}px;top:{top}px;width:{mw}px;height:{mh}px">'
                      f'<img src="assets/img/{sid}.png" alt="" style="width:{mw}px;height:{mh}px" />'
                      f'<div class="rowbox" id="rb-dex" style="left:30px;top:292px;width:842px;height:40px"></div></div>')
        elif src == "PVGRID":
            tw, th, g = GRID_TILE
            x0 = (1080 - (2 * tw + g)) // 2
            for k in range(8):
                x, y = x0 + (k % 2) * (tw + g), 300 + (k // 2) * (th + g)
                inner += (f'<div class="card tile" id="tile-{k}" style="left:{x}px;top:{y}px;width:{tw}px;height:{th}px">'
                          + vid(f"assets/clips/{sid}_{k}.mp4", a, d, f"left:0;top:0;width:{tw}px;height:{th}px") + "</div>")
        else:  # PV footage card
            mw, mh = META[sid]
            sc = w / mw
            inner += (f'<div class="card" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{round(mh * sc)}px">'
                      + vid(f"assets/clips/{sid}.mp4", a, d, f"left:0;top:0;width:{w}px;height:{round(mh * sc)}px") + "</div>")
            if sid == "s20b":
                tw_, th_ = META["s20t"]
                inner += (f'<div class="card" id="card-s20t" style="left:732px;top:830px;width:{tw_}px;height:{th_}px">'
                          + vid("assets/clips/s20t.mp4", a, d, f"left:0;top:0;width:{tw_}px;height:{th_}px") + "</div>")
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}">'
                  f'<div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div></div></div>')

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "card": not s[3].startswith("C")} for s in SHOTS])

HTML = r"""<!doctype html>
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
      .frz { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .bd { position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; background-size: cover; background-position: center;
        filter: blur(26px) brightness(0.32) saturate(0.85); }
      .desk { position: absolute; inset: 0; background:
        radial-gradient(ellipse 70% 45% at 50% 42%, rgba(200,255,77,0.07), rgba(0,0,0,0) 70%),
        linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
        background-size: auto, 72px 72px, 72px 72px; }
      .card { position: absolute; overflow: hidden; border-radius: 22px; border: 2px solid rgba(255,255,255,0.16);
        box-shadow: 0 40px 90px rgba(0,0,0,0.65), 0 0 0 1px rgba(0,0,0,0.4); background: #0d0f15; }
      .card.paper { background: #fff; border: none; border-radius: 10px;
        -webkit-mask-image: linear-gradient(180deg, #000 78%, rgba(0,0,0,0) 100%); mask-image: linear-gradient(180deg, #000 78%, rgba(0,0,0,0) 100%); }
      .card img { position: absolute; left: 0; top: 0; }
      .card.tile { border-radius: 16px; }
      .hl { position: absolute; background: rgba(200,255,77,0.62); mix-blend-mode: multiply; border-radius: 4px; transform-origin: 0 50%; transform: scaleX(0); }
      .rowbox { position: absolute; border: 4px solid var(--lime); border-radius: 10px; box-shadow: 0 0 24px rgba(200,255,77,0.7); opacity: 0; }
      .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 42%, rgba(4,5,10,0) 52%, rgba(4,5,10,0.62) 100%); }
      .botshade { position: absolute; left: 0; top: 1150px; width: 1080px; height: 770px; background: linear-gradient(180deg, rgba(4,5,10,0) 0%, rgba(4,5,10,0.6) 34%, rgba(4,5,10,0.78) 100%); }
      .topshade { position: absolute; left: 0; top: 0; width: 1080px; height: 320px; background: linear-gradient(180deg, rgba(4,5,10,0.6) 0%, rgba(4,5,10,0) 100%); }
      .grain { position: absolute; inset: 0; background-image: url("assets/grain.png"); opacity: 0.08; mix-blend-mode: overlay; }
      .flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
      .black { position: absolute; inset: 0; background: #000; opacity: 0; }
      .tint { position: absolute; inset: 0; background: #7cc4ff; mix-blend-mode: color; opacity: 0; }
      .tag2 { position: absolute; left: 60px; top: 150px; display: inline-flex; align-items: center; gap: 12px; padding: 12px 22px 12px 18px;
        border: 2px solid rgba(255,255,255,0.16); border-radius: 999px; background: rgba(8,9,14,0.62); font-family: "Mono", monospace; font-weight: 700;
        font-size: 26px; letter-spacing: 0.08em; color: var(--ink); }
      .tag2 .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 14px var(--lime); }
      .cap { position: absolute; left: 40px; width: 1000px; top: 1262px; text-align: center; font-weight: 900; font-size: 84px; line-height: 1.02;
        letter-spacing: -0.02em; color: #fff; -webkit-text-stroke: 14px #07080c; paint-order: stroke fill; opacity: 0; }
      .cap .cw { display: inline-block; margin: 0 0.2em; transform-origin: 50% 70%; }
      .src { position: absolute; left: 60px; top: 240px; font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.1em; padding: 10px 16px;
        border-radius: 10px; background: rgba(6,8,12,0.82); color: #c9ccd6; border: 1.5px solid rgba(255,255,255,0.18); opacity: 0; white-space: nowrap; }
      .src i { font-style: normal; color: var(--lime); }
      .chipT { position: absolute; left: 60px; top: 1130px; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.1em; padding: 14px 22px;
        border-radius: 14px; background: rgba(6,8,12,0.84); border: 2px solid currentColor; opacity: 0; white-space: nowrap; color: var(--lime); }
      .chipT .sw { display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: currentColor; margin-right: 14px; vertical-align: 2px; box-shadow: 0 0 12px currentColor; }
      .count { position: absolute; left: 190px; width: 700px; top: 1000px; text-align: center; opacity: 0; padding: 18px 0 22px; border-radius: 30px;
        background: rgba(6,8,12,0.8); border: 2px solid rgba(255,255,255,0.14); }
      .count .n { font-weight: 900; font-size: 140px; letter-spacing: -0.05em; color: #fff; line-height: 0.9; }
      .count .u { margin-top: 12px; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.18em; }
      .stamp { position: absolute; font-weight: 900; font-size: 64px; letter-spacing: -0.01em; padding: 10px 26px; border: 7px solid currentColor; border-radius: 16px;
        color: var(--red); background: rgba(10,6,8,0.55); opacity: 0; white-space: nowrap; }
      .bubble { position: absolute; font-weight: 900; font-size: 56px; padding: 18px 30px; border-radius: 28px; background: #fff; color: #0b0c10; opacity: 0; white-space: nowrap;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
      .bubble::after { content: ""; position: absolute; right: -26px; top: 46px; border: 18px solid transparent; border-left: 30px solid #fff; }
      .key { position: absolute; left: 90px; top: 300px; width: 300px; height: 190px; border-radius: 30px; background: linear-gradient(180deg, #f4f5f7, #c9ccd3);
        box-shadow: 0 14px 0 #8d9099, 0 30px 50px rgba(0,0,0,0.55); color: #15171d; text-align: center; opacity: 0; }
      .key .k1 { margin-top: 28px; font-weight: 900; font-size: 84px; letter-spacing: -0.03em; line-height: 1; }
      .key .k2 { margin-top: 10px; font-family: "Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.2em; color: #555a66; }
      .xmark { position: absolute; left: 150px; top: 290px; width: 200px; height: 200px; opacity: 0; }
      #ring { position: absolute; left: 790px; top: 260px; width: 230px; height: 230px; opacity: 0; }
      #ringpct { position: absolute; left: 790px; top: 330px; width: 230px; text-align: center; font-weight: 900; font-size: 64px; letter-spacing: -0.03em; opacity: 0; }
      #ringlbl { position: absolute; left: 790px; top: 400px; width: 230px; text-align: center; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.18em; color: var(--lime); opacity: 0; }
      #fridgebox { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      /* end card */
      #end { position: absolute; inset: 0; opacity: 0; }
      #end .dim { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(5,6,10,0.78), rgba(5,6,10,0.95)); }
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
        <div class="tint" id="tint"></div>
        <div class="vig"></div>
        <div class="topshade"></div>
        <div class="botshade" id="botshade"></div>

        <div class="src" id="srcPaper">SOURCE · <i>ARXIV 2610.22471</i> · 15 OCT 2026</div>
        <div class="src" id="srcFreeze">REAL · <i>AUTHORS' PROJECT VIDEO</i></div>
        <div class="src" id="srcBoard">REAL · <i>AUTHORS' PROJECT VIDEO</i> · 12 BENCHMARKS</div>
        <div class="src" id="srcGrid">REAL ROBOTS · <i>AUTHORS' PROJECT VIDEO</i></div>
        <div class="src" id="srcFault">REAL ROBOT · <i>AUTHORS' PROJECT VIDEO</i></div>
        <div class="src" id="srcFridge">REAL TEST HOME · <i>AUTHORS' PROJECT VIDEO</i></div>
        <div class="src" id="srcVerdict" style="top:580px">THE PAPER'S VERDICT · <i>ARXIV 2610.22471</i></div>

        <div class="chipT" id="chAstra"><span class="sw"></span>GPT-6 ASTRA AT THE CONTROLS</div>
        <div class="chipT" id="chChef"><span class="sw"></span>TRAINEE CHEF = THE AI</div>
        <div class="chipT" id="chStudy"><span class="sw"></span>STUDIES THE DEMO VIDEOS</div>
        <div class="chipT" id="chPause" style="color:var(--blue)"><span class="sw"></span>⏸ CLOCK PAUSED WHILE IT THINKS</div>
        <div class="chipT" id="chReal" style="color:var(--amber)"><span class="sw"></span>THE REAL WORLD</div>

        <div class="count" id="c10"><div class="n" id="c10n">1×</div><div class="u" style="color:var(--lime)">MOVES ALLOWED</div></div>
        <div class="stamp" id="stNear" style="left:90px;top:1040px;color:var(--lime)">NEAR 100% ✓</div>
        <div class="count" id="c87" style="top:1010px"><div class="n" id="c87n">0%</div><div class="u" style="color:var(--lime)">FIDDLY HAND TASKS</div></div>
        <div class="stamp" id="stVid" style="left:70px;top:300px">✕ NO VIDEOS</div>
        <div class="stamp" id="stPause" style="left:110px;top:420px">✕ NO PAUSE</div>
        <div class="count" id="c17"><div class="n">17<span style="color:var(--muted)">/18</span> <span style="color:var(--lime)">✓</span></div><div class="u" style="color:var(--lime)">PICK-UPS · REAL ROBOTS</div></div>
        <div class="count" id="c0" style="top:1010px"><div class="n"><span style="color:var(--red)">0</span><span style="color:var(--muted)">/11</span> <span style="color:var(--red)">✕</span></div><div class="u" style="color:var(--red)">PLUG INSERTIONS</div></div>
        <svg id="ring" viewBox="0 0 230 230"><circle cx="115" cy="115" r="98" fill="rgba(6,8,12,0.8)" stroke="rgba(255,255,255,0.15)" stroke-width="14" />
          <circle id="ringarc" cx="115" cy="115" r="98" fill="none" stroke="#c8ff4d" stroke-width="14" stroke-linecap="butt" transform="rotate(-90 115 115)" stroke-dasharray="615.75" stroke-dashoffset="615.75" /></svg>
        <div id="ringpct">0%</div><div id="ringlbl">THINKING</div>
        <div class="count" id="cHour"><div class="n" id="cHourN">0:00:00</div><div class="u" style="color:var(--amber)">ONE TASK · REAL HUMANOID</div></div>
        <div class="key" id="key"><div class="k1">⌘Z</div><div class="k2">UNDO</div></div>
        <svg class="xmark" id="xk" viewBox="0 0 200 200"><path id="xk1" d="M30 30 L170 170" stroke="#ff6b6b" stroke-width="26" stroke-linecap="round" fill="none" stroke-dasharray="200" stroke-dashoffset="200" />
          <path id="xk2" d="M170 30 L30 170" stroke="#ff6b6b" stroke-width="26" stroke-linecap="round" fill="none" stroke-dasharray="200" stroke-dashoffset="200" /></svg>
        <div class="bubble" id="bub" style="left:120px;top:330px">✓ HUNG IT!</div>
        <svg id="fridgebox" viewBox="0 0 1080 1920"><rect id="fbox" x="306" y="214" width="392" height="1010" rx="26" fill="none" stroke="#ff6b6b" stroke-width="10"
          stroke-dasharray="2804" stroke-dashoffset="2804" /></svg>
        <div class="chipT" id="chOpen" style="left:330px;top:240px;color:var(--red)"><span class="sw"></span>STILL OPEN</div>

        <div class="grain" id="grain"></div>
        <div class="progress" id="prog" style="background:var(--lime)"></div>
        <div class="tag2" id="tag"><span class="dot"></span>AI PAPER · STORY</div>
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
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:InterV;font-weight:800">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span></div>
      </div>

      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%, HND = %H%;
      const SH = %SHOTSJS%;
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out";
      const fx = (id) => "#fx-" + id, cam = (id) => "#cam-" + id;

      // ---------- shots: visibility and camera ----------
      SH.forEach((s, i) => {
        tl.set(fx(s.id), { opacity: i === 0 ? 1 : 0 }, 0);
        const a = Math.max(0, s.t0 - HND), b = s.t1 + HND;
        if (s.id === "s03") return;  // has its own push-in on the title
        if (s.card) tl.fromTo(cam(s.id), { scale: 1 }, { scale: 1.035, duration: b - a, ease: "none" }, a);
        else tl.fromTo(cam(s.id), { scale: 1.0 }, { scale: 1.07, duration: b - a, ease: "none" }, a);
      });
      const flash = (t, a, d, c) => { tl.set("#flash", { background: c || "#fff" }, t); tl.fromTo("#flash", { opacity: a }, { opacity: 0, duration: d || 0.35, ease: "power2.out" }, t); };
      const cardIn = (id, t) => { const c = document.querySelectorAll("#cam-" + id + " .card");
        tl.fromTo(c, { opacity: 0, scale: 0.86, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.6)", stagger: id === "s12" ? 0.09 : 0.12 }, t); };
      const TR = {
        whip(A, B, T) { tl.fromTo(fx(B), { opacity: 1, x: 1080, filter: "blur(22px)" }, { x: 0, filter: "blur(0px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16);
          tl.to(fx(A), { x: -760, filter: "blur(22px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16); tl.set(fx(A), { opacity: 0 }, T + 0.14); },
        slideup(A, B, T) { tl.fromTo(fx(B), { opacity: 1, y: 1920, filter: "blur(22px)" }, { y: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17);
          tl.to(fx(A), { y: -1100, filter: "blur(22px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17); tl.set(fx(A), { opacity: 0 }, T + 0.15); },
        zoom(A, B, T) { tl.to(fx(A), { scale: 1.45, filter: "blur(18px)", opacity: 0, duration: 0.26, ease: "power2.in" }, T - 0.16);
          tl.fromTo(fx(B), { opacity: 0, scale: 0.84, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: E }, T - 0.1); flash(T - 0.02, 0.28, 0.3); },
        flash(A, B, T, c) { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T); flash(T, 0.6, 0.42, c); },
        dip(A, B, T) { tl.to("#black", { opacity: 1, duration: 0.14, ease: "power1.in" }, T - 0.14); tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T);
          tl.to("#black", { opacity: 0, duration: 0.26, ease: "power1.out" }, T); },
        glitch(A, B, T) { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T);
          [[0, 34, "hue-rotate(80deg) saturate(2)"], [0.033, -26, "hue-rotate(-60deg)"], [0.066, 16, "none"], [0.1, -8, "none"], [0.133, 0, "none"]].forEach(([dt, x, f]) => tl.set(fx(B), { x, filter: f }, T + dt));
          flash(T, 0.35, 0.25, "#ff6b6b"); },
        card(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out" }, T - 0.12); tl.set(fx(A), { opacity: 0 }, T + 0.12); cardIn(B, T - 0.05); },
      };
      const CUTS = [["s01", "s02", "whip"], ["s02", "s03", "card"], ["s03", "s04", "whip"], ["s04", "s05", "flash", "#c8ff4d"], ["s05", "s06", "slideup"],
        ["s06", "s07", "whip"], ["s07", "s08", "zoom"], ["s08", "s08b", "card"], ["s08b", "s09", "flash", "#ffd36b"], ["s09", "s10", "card"],
        ["s10", "s11", "dip"], ["s11", "s12", "card"], ["s12", "s13", "whip"], ["s13", "s14", "slideup"], ["s14", "s15", "whip"],
        ["s15", "s15b", "glitch"], ["s15b", "s16", "dip"], ["s16", "s17", "flash", "#ffe2a8"], ["s17", "s18", "whip"], ["s18", "s19", "zoom"],
        ["s19", "s20", "whip"], ["s20", "s20b", "card"], ["s20b", "s21", "zoom"], ["s21", "s22", "dip"], ["s22", "s23", "flash", "#c8ff4d"]];
      const T0 = Object.fromEntries(SH.map((s) => [s.id, s.t0]));
      CUTS.forEach(([A, B, k, c]) => TR[k](A, B, T0[B], c));
      flash(0, 0.0, 0.01);

      // ---------- moments inside shots ----------
      const show = (sel, t0, t1, from) => { tl.fromTo(sel, Object.assign({ opacity: 0, y: 14 }, from || {}), { opacity: 1, y: 0, x: 0, scale: 1, duration: 0.32, ease: E }, t0);
        tl.to(sel, { opacity: 0, duration: 0.2 }, t1); };
      const pop = (sel, t0, t1, rot) => { tl.fromTo(sel, { opacity: 0, scale: 2.2, rotation: rot || 0 }, { opacity: 1, scale: 1, rotation: rot || 0, duration: 0.22, ease: "power4.out" }, t0);
        tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const punch = (id, t, s) => { tl.fromTo(fx(id), { scale: 1 }, { scale: 1 + (s || 0.08), duration: 0.12, ease: "power2.out", immediateRender: false }, t);
        tl.to(fx(id), { scale: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.12); };
      const shake = (id, t, a) => { [[0, a, -a * 0.6], [0.04, -a, a * 0.5], [0.08, a * 0.7, a * 0.4], [0.12, -a * 0.5, -a * 0.3], [0.16, a * 0.3, 0], [0.2, 0, 0]].forEach(([dt, x, y]) => tl.set(fx(id), { x, y }, t + dt)); };

      // the paper: push in on the title
      tl.set(cam("s03"), { transformOrigin: "50% 30%" }, 0); tl.fromTo(cam("s03"), { scale: 1 }, { scale: 1.22, duration: 3.6, ease: "power1.inOut", immediateRender: false }, 5.3);
      // hook
      punch("s01", 1.04, 0.07); flash(1.05, 0.18, 0.3, "#ffd36b"); punch("s02", 3.89, 0.06);
      // the paper
      tl.to("#hl-title", { scaleX: 1, duration: 0.55, ease: "power2.inOut" }, 6.95);
      show("#srcPaper", 5.55, 8.55);
      show("#chAstra", 10.6, 12.05, { x: -30 });
      show("#chChef", 13.15, 15.4, { x: -30 });
      show("#chStudy", 16.75, 18.45, { x: -30 });
      // 1x -> 10x
      tl.fromTo("#c10", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 18.95);
      const m10 = { v: 1 }; tl.fromTo(m10, { v: 1 }, { v: 10, duration: 0.95, ease: "power1.in", onUpdate() { $("#c10n").textContent = Math.round(m10.v) + "×"; } }, 19.02);
      tl.to("#c10", { scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }, 19.98); tl.to("#c10", { opacity: 0, y: -24, duration: 0.25 }, 20.9);
      // freeze while it thinks
      tl.set("#frz-s08", { opacity: 1 }, 21.85); tl.fromTo(fx("s08"), { filter: "saturate(1) brightness(1)" }, { filter: "saturate(0.25) brightness(0.86)", duration: 0.25 }, 21.85);
      tl.fromTo("#tint", { opacity: 0 }, { opacity: 0.22, duration: 0.25 }, 21.85); tl.to("#tint", { opacity: 0, duration: 0.2 }, 23.1);
      punch("s08", 21.85, 0.05); show("#chPause", 22.0, 23.1, { x: -30 });
      show("#srcFreeze", 23.25, 24.7);
      // smashed
      shake("s09", 25.19, 22); flash(25.2, 0.25, 0.35, "#ffd36b"); pop("#stNear", 26.78, 28.3, -6);
      // 80% -> 87.3% dexterous hands
      show("#srcBoard", 28.45, 31.2);
      tl.fromTo("#rb-dex", { opacity: 0, scaleX: 0.6 }, { opacity: 1, scaleX: 1, duration: 0.3, ease: E }, 28.7);
      tl.to("#rb-dex", { boxShadow: "0 0 46px rgba(200,255,77,1)", duration: 0.35, yoyo: true, repeat: 3 }, 29.0);
      tl.fromTo("#c87", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 28.74);
      const m87 = { v: 0 }; tl.fromTo(m87, { v: 0 }, { v: 87.3, duration: 1.1, ease: "power2.out", onUpdate() { $("#c87n").textContent = m87.v.toFixed(1) + "%"; } }, 28.78);
      tl.to("#c87", { opacity: 0, y: -24, duration: 0.2 }, 31.15);
      // real shift
      show("#chReal", 32.45, 33.45, { x: -30 }); show("#srcGrid", 33.6, 35.45);
      // no videos, no pause
      pop("#stVid", 35.6, 39.0, -5); pop("#stPause", 36.55, 39.0, 4);
      // 17/18, 0/11
      tl.fromTo("#c17", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 40.43); tl.to("#c17", { opacity: 0, duration: 0.2 }, 42.0);
      show("#srcFault", 43.4, 45.1);
      tl.fromTo("#c0", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.out" }, 43.35); tl.to("#c0", { opacity: 0, duration: 0.2 }, 45.05);
      punch("s15b", 43.35, 0.05);
      // 90% thinking
      tl.fromTo(["#ring", "#ringpct", "#ringlbl"], { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 46.2);
      const m90 = { v: 0 }; tl.fromTo(m90, { v: 0 }, { v: 90, duration: 1.0, ease: "power2.out", onUpdate() { $("#ringpct").textContent = Math.round(m90.v) + "%";
        $("#ringarc").setAttribute("stroke-dashoffset", (615.75 * (1 - m90.v / 100)).toFixed(1)); } }, 46.6);
      tl.to(["#ring", "#ringpct", "#ringlbl"], { opacity: 0, duration: 0.2 }, 49.8);
      // over an hour
      tl.fromTo("#cHour", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 50.0);
      const mh = { v: 0 }; tl.fromTo(mh, { v: 0 }, { v: 3720, duration: 1.5, ease: "power2.in", onUpdate() { const s = Math.round(mh.v), h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
        $("#cHourN").textContent = h + ":" + String(m).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0") + (s >= 3600 ? "+" : ""); } }, 50.0);
      tl.to("#cHour", { scale: 1.1, duration: 0.15, yoyo: true, repeat: 1 }, 51.5); tl.to("#cHour", { opacity: 0, duration: 0.2 }, 52.15);
      // no undo
      tl.fromTo("#key", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: E }, 54.9);
      tl.to("#key", { y: 12, boxShadow: "0 2px 0 #8d9099, 0 10px 20px rgba(0,0,0,0.55)", duration: 0.08 }, 55.27); tl.to("#key", { y: 0, boxShadow: "0 14px 0 #8d9099, 0 30px 50px rgba(0,0,0,0.55)", duration: 0.12 }, 55.37);
      tl.set("#xk", { opacity: 1 }, 55.5); tl.to("#xk1", { strokeDashoffset: 0, duration: 0.14 }, 55.5); tl.to("#xk2", { strokeDashoffset: 0, duration: 0.14 }, 55.62);
      tl.to(["#key", "#xk"], { opacity: 0, duration: 0.2 }, 56.25);
      // the mug
      tl.fromTo("#bub", { opacity: 0, scale: 0.4, transformOrigin: "100% 60%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }, 59.3); tl.to("#bub", { opacity: 0, duration: 0.15 }, 59.95);
      // fridge callback
      tl.set("#fridgebox", { opacity: 1 }, 60.2); tl.to("#fbox", { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, 60.2); tl.to("#fridgebox", { opacity: 0, duration: 0.15 }, 61.35);
      show("#chOpen", 60.45, 61.35);
      show("#srcFridge", 61.5, 63.5);
      // verdict
      show("#srcVerdict", 63.75, 67.9);
      // the clock: ticking stops on the question
      tl.set("#frz-s22", { opacity: 1 }, 72.62); punch("s22", 72.62, 0.05);
      tl.fromTo(fx("s22"), { filter: "saturate(1)" }, { filter: "saturate(0.3)", duration: 0.2 }, 72.62);

      // ---------- end card ----------
      tl.fromTo("#end", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 73.9);
      tl.fromTo("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, 74.05);
      tl.fromTo(["#ename", "#ehandle"], { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: E, stagger: 0.12 }, 74.3);
      tl.fromTo("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 74.75);
      tl.to("#fol", { scale: 1.06, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, 75.3);
      tl.to("#mark", { boxShadow: "0 0 140px rgba(200,255,77,0.8)", duration: 0.9, yoyo: true, repeat: 2, ease: "sine.inOut" }, 75.1);

      // ---------- global UI ----------
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      tl.fromTo(["#tag", "#bm"], { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.4 }, 0.1);
      tl.to(["#tag", "#bm"], { opacity: 0, duration: 0.4 }, 73.7);
      tl.to([".botshade", ".topshade"], { opacity: 0, duration: 0.5 }, 73.9);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);
      tl.fromTo("#black", { opacity: 0 }, { opacity: 1, duration: 0.4 }, DUR - 0.45);

      // ---------- captions ----------
      const COVERS = [[73.0, 90]];
      const covered = (a, b) => COVERS.some(([c0, c1]) => a < c1 && b > c0);
      const capsRoot = $("#caps");
      (window.CAPS || []).forEach((ch) => {
        if (covered(ch.t0, ch.t1)) return;
        const c = document.createElement("div"); c.className = "cap"; capsRoot.appendChild(c);
        const spans = ch.w.map((w) => { const s = document.createElement("span"); s.className = "cw"; s.textContent = w.d; if (w.emph) s.style.color = "#c8ff4d"; c.appendChild(s); return { s, w }; });
        tl.fromTo(c, { opacity: 0, scale: 0.86, y: 10 }, { opacity: 1, scale: 1, y: 0, duration: 0.12, ease: "back.out(2)" }, ch.t0);
        tl.set(c, { opacity: 0 }, ch.t1);
        spans.forEach(({ s, w }, k) => {
          const end = k + 1 < spans.length ? spans[k + 1].w.s : ch.t1;
          tl.set(s, { color: "#c8ff4d", scale: w.emph ? 1.08 : 1.04 }, w.s);
          tl.set(s, { color: w.emph ? "#c8ff4d" : "#ffffff", scale: 1 }, end);
        });
      });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js)
       .replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
print("index.html", len(out), "bytes,", len(blocks), "shots")

/* One AI Trick motion toolkit for HyperFrames (GSAP, deterministic, seek-safe). */
(function () {
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hash(i, j) {
    let h = (i * 374761393 + j * 668265263) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }
  const $ = (s, root) => (typeof s === "string" ? (root || document).querySelector(s) : s);
  const $$ = (s, root) => (typeof s === "string" ? Array.from((root || document).querySelectorAll(s)) : [s]);

  const FX = {};

  /* Split text of each matched element into word spans (.w), keeping inline wrappers like <span class="hl">. */
  FX.splitWords = function (sel) {
    $$(sel).forEach((el) => {
      if (el.dataset.split) return;
      el.dataset.split = "1";
      const walk = (node) => {
        Array.from(node.childNodes).forEach((c) => {
          if (c.nodeType === 3) {
            const parts = c.textContent.split(/(\s+)/);
            const frag = document.createDocumentFragment();
            parts.forEach((p) => {
              if (!p) return;
              if (/^\s+$/.test(p)) frag.appendChild(document.createTextNode(" "));
              else {
                const s = document.createElement("span");
                s.className = "w";
                s.textContent = p;
                frag.appendChild(s);
              }
            });
            node.replaceChild(frag, c);
          } else if (c.nodeType === 1 && c.tagName !== "BR" && !c.classList.contains("w")) {
            walk(c);
          }
        });
      };
      walk(el);
    });
  };

  /* Words rise in with blur. */
  FX.words = function (tl, sel, t, opts) {
    opts = Object.assign({ stagger: 0.07, y: 70, dur: 0.55, blur: 14 }, opts || {});
    FX.splitWords(sel);
    const ws = $$(sel).flatMap((el) => Array.from(el.querySelectorAll(".w")));
    tl.fromTo(ws, { opacity: 0, y: opts.y, filter: `blur(${opts.blur}px)` },
      { opacity: 1, y: 0, filter: "blur(0px)", duration: opts.dur, ease: "power3.out", stagger: opts.stagger }, t);
    return ws;
  };

  /* Generic element entrance. */
  FX.in = function (tl, sel, t, opts) {
    opts = Object.assign({ y: 50, x: 0, scale: 1, dur: 0.5, blur: 10, stagger: 0.08, ease: "power3.out" }, opts || {});
    tl.fromTo(sel, { opacity: 0, y: opts.y, x: opts.x, scale: opts.scale, filter: `blur(${opts.blur}px)` },
      { opacity: 1, y: 0, x: 0, scale: 1, filter: "blur(0px)", duration: opts.dur, ease: opts.ease, stagger: opts.stagger }, t);
  };

  /* Scene exit: lift, fade, blur. */
  FX.out = function (tl, sel, t, opts) {
    opts = Object.assign({ y: -50, dur: 0.32, stagger: 0.03 }, opts || {});
    tl.to(sel, { opacity: 0, y: opts.y, filter: "blur(10px)", duration: opts.dur, ease: "power2.in", stagger: opts.stagger }, t);
  };

  /* Zoom-through exit (camera flies forward). */
  FX.zoomOut = function (tl, sel, t) {
    tl.to(sel, { scale: 2.4, opacity: 0, filter: "blur(18px)", duration: 0.42, ease: "power3.in" }, t);
  };

  /* Text decode/scramble into final text. */
  FX.scramble = function (tl, sel, t, dur, opts) {
    opts = Object.assign({ chars: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&*<>/_", fps: 30 }, opts || {});
    $$(sel).forEach((el, k) => {
      const final = el.textContent;
      const proxy = { p: 0 };
      tl.fromTo(proxy, { p: 0 }, {
        p: 1, duration: dur, ease: "none",
        onUpdate() {
          const frame = Math.floor(proxy.p * dur * opts.fps);
          let out = "";
          for (let i = 0; i < final.length; i++) {
            const ch = final[i];
            const revealAt = i / final.length;
            if (ch === " " || proxy.p >= 1 || proxy.p > revealAt + 0.25) out += ch;
            else if (proxy.p < revealAt * 0.6) out += " ";
            else out += opts.chars[Math.floor(hash(i + k * 97, frame) * opts.chars.length)];
          }
          el.textContent = out;
        },
      }, t);
      tl.set(el, { opacity: 1 }, t);
    });
  };

  /* Count a number up (or down). fmt(v) returns the string. */
  FX.counter = function (tl, sel, from, to, t, dur, fmt) {
    const el = $(sel);
    const proxy = { v: from };
    fmt = fmt || ((v) => Math.round(v).toString());
    tl.fromTo(proxy, { v: from }, { v: to, duration: dur, ease: "power2.out", onUpdate() { el.textContent = fmt(proxy.v); } }, t);
  };

  /* Draw an SVG stroke. */
  FX.draw = function (tl, sel, t, dur, ease) {
    $$(sel).forEach((p) => {
      const len = p.getTotalLength ? p.getTotalLength() : 1000;
      p.style.strokeDasharray = `${len}`;
      tl.fromTo(p, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease: ease || "power2.inOut" }, t);
    });
  };

  /* Move an element along an SVG path (path in same coordinate space as a sibling SVG at 1:1 scale). */
  FX.travel = function (tl, dotSel, pathSel, t, dur, opts) {
    opts = Object.assign({ ease: "power1.inOut", offsetX: 0, offsetY: 0 }, opts || {});
    const dot = $(dotSel), path = $(pathSel);
    const len = path.getTotalLength();
    const proxy = { p: 0 };
    tl.set(dot, { opacity: 1 }, t);
    tl.fromTo(proxy, { p: 0 }, {
      p: 1, duration: dur, ease: opts.ease,
      onUpdate() {
        const pt = path.getPointAtLength(proxy.p * len);
        dot.style.transform = `translate(${pt.x + opts.offsetX}px, ${pt.y + opts.offsetY}px)`;
      },
    }, t);
    tl.to(dot, { opacity: 0, duration: 0.15 }, t + dur);
  };

  /* Diagonal accent wipe used as a scene transition. Needs <div class="wipe"></div> inside root. */
  FX.wipe = function (tl, t, sel) {
    sel = sel || ".wipe";
    tl.fromTo(sel, { x: -1700, opacity: 1 }, { x: 1700, duration: 0.5, ease: "power3.inOut" }, t - 0.25);
    tl.set(sel, { opacity: 0 }, t + 0.26);
  };

  /* RGB-split glitch on text for a short burst. */
  FX.glitch = function (tl, sel, t, dur) {
    const steps = Math.max(4, Math.round(dur * 20));
    for (let i = 0; i < steps; i++) {
      const a = (hash(i, 7) - 0.5) * 18, b = (hash(i, 13) - 0.5) * 18;
      tl.set(sel, {
        textShadow: `${a}px 0 rgba(255,60,120,0.85), ${-b}px 0 rgba(80,220,255,0.85)`,
        x: (hash(i, 29) - 0.5) * 14,
      }, t + i * (dur / steps));
    }
    tl.set(sel, { textShadow: "0 0 0 rgba(0,0,0,0)", x: 0 }, t + dur);
  };

  /* Stamp slam. */
  FX.stamp = function (tl, sel, t, rot) {
    tl.fromTo(sel, { opacity: 0, scale: 2, rotation: (rot || -8) - 8 },
      { opacity: 1, scale: 1, rotation: rot || -8, duration: 0.26, ease: "back.out(2.2)" }, t);
  };

  /* Pop in (for chips, nodes). */
  FX.pop = function (tl, sel, t, stagger) {
    tl.fromTo(sel, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.42, ease: "back.out(2)", stagger: stagger || 0.06 }, t);
  };

  /* Top progress bar across the whole video. */
  FX.progress = function (tl, sel, dur) {
    tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: dur, ease: "none" }, 0);
  };

  /* Deterministic particle network on a <canvas>. rgb like "200,255,77". */
  FX.particles = function (tl, sel, dur, opts) {
    opts = Object.assign({ n: 70, rgb: "200,255,77", seed: 3, link: 190, speed: 0.22 }, opts || {});
    const cv = $(sel);
    const ctx = cv.getContext("2d");
    const W = cv.width, H = cv.height;
    const r = mulberry32(opts.seed);
    const pts = Array.from({ length: opts.n }, () => ({
      x: r() * W, y: r() * H, ax: 40 + r() * 90, ay: 40 + r() * 120, ph: r() * 6.28, sp: 0.4 + r() * 0.9, s: 1.5 + r() * 2.5,
    }));
    const proxy = { t: 0 };
    const draw = () => {
      ctx.clearRect(0, 0, W, H);
      const tt = proxy.t * opts.speed;
      const P = pts.map((p) => ({ x: p.x + Math.sin(tt * p.sp + p.ph) * p.ax, y: p.y + Math.cos(tt * p.sp * 0.8 + p.ph) * p.ay - proxy.t * 6, s: p.s }));
      P.forEach((p) => { p.y = ((p.y % H) + H) % H; });
      for (let i = 0; i < P.length; i++) {
        for (let j = i + 1; j < P.length; j++) {
          const dx = P[i].x - P[j].x, dy = P[i].y - P[j].y;
          const d = Math.sqrt(dx * dx + dy * dy);
          if (d < opts.link) {
            ctx.strokeStyle = `rgba(${opts.rgb},${0.16 * (1 - d / opts.link)})`;
            ctx.lineWidth = 1.2;
            ctx.beginPath(); ctx.moveTo(P[i].x, P[i].y); ctx.lineTo(P[j].x, P[j].y); ctx.stroke();
          }
        }
      }
      P.forEach((p) => {
        ctx.fillStyle = `rgba(${opts.rgb},0.55)`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.s, 0, 6.283); ctx.fill();
      });
    };
    tl.fromTo(proxy, { t: 0 }, { t: dur, duration: dur, ease: "none", onUpdate: draw }, 0);
    draw();
  };

  /* Word-by-word highlight sweep: colour words in sequence. */
  FX.highlight = function (tl, sel, t, color) {
    const ws = $$(sel).flatMap((el) => Array.from(el.querySelectorAll(".w")));
    tl.to(ws, { color: color, duration: 0.18, stagger: 0.06 }, t);
  };

  window.FX = FX;
})();

"""Write index.html for Short #9 from edl.py, work/meta.json, assets/pages/pages.json and work/photo/i1.json.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, the moving photo, a frozen frame, a page card
or a graphic on a blurred backdrop. Captions are designed into each shot (window.CAPS from make_captions.py): S standard,
A hero word, B the number is the caption (counts up). Each chunk takes the colour of the shot under it.
Usage: python3 make_index.py
"""
import json

from edl import SHOTS, H, DUR

META = json.load(open("work/meta.json"))
PAGES = json.load(open("assets/pages/pages.json"))
I1 = json.load(open("work/photo/i1.json"))
AMBER, TEAL, LIME, RED, GREEN, BLUE = "#ffb547", "#4fd0ff", "#c8ff4d", "#ff6b6b", "#7ee787", "#7cc4ff"
COL = {"s01": AMBER, "s02": AMBER, "s03": AMBER, "s04": TEAL, "s05": AMBER, "s06": TEAL, "s07": AMBER, "s08": AMBER,
       "s09": TEAL, "s10": BLUE, "s11": BLUE, "s12": AMBER, "s13": RED, "s14": RED, "s15": RED, "s16": RED, "s17": RED,
       "s18": AMBER, "s19": AMBER, "s20": AMBER, "s21": TEAL, "s22": AMBER, "s23": AMBER, "s24": RED, "s25": GREEN,
       "s26": GREEN, "s27": TEAL, "s28": AMBER, "s29": AMBER, "s30": LIME, "s31": BLUE, "s32": GREEN, "s33": GREEN,
       "s34": GREEN, "s35": LIME, "s36": LIME, "s37": LIME, "s38": AMBER}
HL_T = {"s10": 23.12, "s11": 24.08, "s15": 34.8, "s31": 63.95}   # when each page's highlight sweeps (on the spoken words)
ZMIN = {"s15": 640}   # Microsoft's figure: zoom no further than a 640 px wide window (the title stays readable)
GEOM, HL_JS = {}, []


def card(sid, sp):
    m = META[sid]
    w = sp.get("w", 1000)
    s = w / m["pw"]
    h = round(m["ph"] * s)
    left = (1080 - w) // 2
    top = max(300, round(740 - h / 2))
    if top + h > 1225:
        top = max(240, 1225 - h)
    src = "assets/pages/" + sp["name"] + ".png"
    inner = f'<img src="{src}" alt="" style="left:0;top:0;width:{w}px" />'
    boxes = m["boxes"]
    t, acc, tot = HL_T[sid], 0.0, sum(b[2] for b in boxes)
    for j, (x, y, bw, bh) in enumerate(boxes):
        hid = f"hl-{sid}-{j}"
        inner += (f'<div class="hl" id="{hid}" style="left:{x * s:.0f}px;top:{y * s:.0f}px;width:{bw * s:.0f}px;height:{bh * s:.0f}px"></div>')
        d = 0.5 * bw / max(tot, 1) + 0.08
        HL_JS.append([hid, round(t + acc, 3), round(d, 3)])
        acc += d
    x0 = min(b[0] for b in boxes); x1 = max(b[0] + b[2] for b in boxes)
    y0 = min(b[1] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
    hx = left + (x0 + x1) / 2 * s if (x1 - x0) * s < 0.6 * w else left + w / 2   # a wide highlight: frame the whole card
    hw = (x1 - x0) * s if (x1 - x0) * s < 0.6 * w else w
    GEOM[sid] = (left, top, w, h, s, h, [[t, round(hx, 1), round(top + (y0 + y1) / 2 * s, 1), round(max(hw, ZMIN.get(sid, 0)), 1)]])
    return f'<div class="card" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">{inner}</div>'


def vid(src, t0, d, css, ms=0.0, name=None):
    vidn = "v-" + (name or src.split("/")[-1].split(".")[0])
    d = min(d, DUR - t0)
    return (f'<video id="{vidn}" class="vid" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-media-start="{ms:.3f}" style="{css}"></video>')


FULL = "left:0;top:0;width:1080px;height:1920px"
blocks = []
for z, (sid, t0, t1, kind, sp) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:
        a, d, ms = 0.0, d + (t0 - H), H - t0
    bd = f'<div class="bd" style="background-image:url(assets/img/{sid}_bd.jpg)"></div><div class="desk"></div>'
    if kind in ("V", "LOOP", "MOSAIC", "SPLIT"):
        inner = vid(f"assets/clips/{sid}.mp4", a, d, FULL, ms)
        if kind == "SPLIT":
            inner += '<div class="seam" id="seam"></div>'
    elif kind == "PHOTO":
        ex, ey = I1["eye"]
        inner = (f'<img class="ph" id="phbg" src="assets/img/i1_bg.jpg" alt="" /><img class="ph" id="phfg" src="assets/img/i1_fg.png" alt="" />'
                 f'<div class="eyeglow" id="eye" style="left:{ex - 150}px;top:{ey - 60}px"></div>')
    elif kind == "STILL":
        inner = f'<img class="ph" id="still-{sid}" src="assets/img/{sid}.png" alt="" />'
    elif kind == "PAGE":
        inner = bd + card(sid, sp)
    elif kind == "GFX":
        inner = bd + f'<div class="gfx" id="gx-{sid}"></div>'
    elif kind == "END":
        inner = f'<div class="bd" style="background-image:url(assets/img/{sid}_bd.jpg);filter:blur(30px) brightness(0.45)"></div>'
    fade = '<div class="docfade"></div><div class="doctop"></div>' if kind == "PAGE" else ""
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}">'
                  f'<div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div>{fade}</div></div>')

# ---------------------------------------------------------------- captions: mode per chunk, colour of the shot under it
CAPS = json.loads(open("captions.js").read()[len("window.CAPS = "):].rstrip().rstrip(";"))
B_AT = {1.84: "", 26.11: "", 32.40: ""}     # the number is the caption: 2,200 · 14 · 2,900
CAPLAY = []
for ch in CAPS:
    t = ch["t0"]
    sid = [s[0] for s in SHOTS if s[1] - 0.02 <= t + 0.06 < s[2]][0]
    col = COL.get(sid, LIME)
    key = min(B_AT, key=lambda x: abs(x - t))
    if abs(key - t) < 0.05:
        spec = dict(m="B", c=col, fmt=B_AT[key])
    elif any(w["emph"] for w in ch["w"]):
        spec = dict(m="A", c=col)
    else:
        spec = dict(m="S", c=col)
    CAPLAY.append([round(t - 0.01, 3), round(ch["t1"], 3), spec])
COVERS = [[81.5, 999]]   # the end card says it

GEN = "AI ILLUSTRATION · GOOGLE FLOW"
LABELS = {
    GEN: ["s01", "s18", "s23", "s25", "s26", "s27", "s29", "s30", "s32", "s38"],
    "AI ILLUSTRATION": ["s07"],
    "AI ILLUSTRATION · NIGHT / DAY": ["s35"],
    "REAL · MICROSOFT: 2,250+ TENANTS TRIED": ["s02"],
    "REAL · MICROSOFT SECURITY BLOG · 21 OCT": ["s03", "s09", "s10", "s11"],
    "REAL · MICROSOFT'S 14 TARGETED SECTORS": ["s12"],
    "REAL · REUTERS · 21 OCT 2026": ["s13"],
    "REAL · MICROSOFT · PASSWORD SPRAY 10–14 OCT": ["s14", "s16", "s17"],
    "REAL · MICROSOFT · FIGURE 1": ["s15"],
    "REAL · CONNECTWISE TRUST CENTER": ["s21", "s22"],
    "REAL · MICROSOFT: \"WHAT IS ARTEX?\"": ["s31"],
    "REAL · ARTEX'S MAKER · THE HACKER NEWS": ["s34"],
}
T = {s[0]: (s[1], s[2]) for s in SHOTS}
LAB_JS, lab_html = [], []
for k, (txt, ids) in enumerate(LABELS.items()):
    gen = not txt.startswith("REAL")
    lab_html.append(f'<div class="src{" gen" if gen else ""}" id="src{k}"><span class="sd"></span>{txt}</div>')
    spans = []
    for i in sorted(ids, key=lambda q: T[q][0]):
        a, b = T[i]
        if spans and abs(spans[-1][1] - a) < 0.01:
            spans[-1][1] = b
        else:
            spans.append([a, b])
    for a, b in spans:
        LAB_JS.append([f"#src{k}", round(a + 0.12, 2), round(b - 0.08, 2)])

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%LABJS%", json.dumps(LAB_JS)).replace("%HLJS%", json.dumps(HL_JS)).replace("%GEO%", json.dumps(GEOM))
       .replace("%CAPLAY%", json.dumps(CAPLAY)).replace("%COVERS%", json.dumps(COVERS)).replace("%PAGES%", json.dumps(PAGES))
       .replace("%EYE%", json.dumps(I1["eye"])).replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(HL_JS), "highlight strips")

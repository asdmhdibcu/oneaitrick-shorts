"""Write index.html for Short #7 from edl.py, work/meta.json, work/colors.json and the located highlights.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, a still, or cards on a blurred backdrop.
Captions are designed into each shot (window.CAPS from make_captions.py): S standard, A hero word, B the number is the
caption (counts up; "clock" counts hours), C glass panel in the scene. Each chunk takes the colour of the shot under it.
Usage: python3 make_index.py
"""
import json

from edl import SHOTS, H, DUR
from locate import locate

META = json.load(open("work/meta.json"))
AUTO = json.load(open("work/colors.json"))
TEAL, LIME, CLAYG, GH, QUANTA, DECODER, SCI = "#4fd0ff", "#c8ff4d", "#6fdc7f", "#79b8ff", "#ffb547", "#5cc8ff", "#8ec5ff"
COL = {"s01": "#ffb066", "s13": CLAYG, "s16": LIME, "s17": "#ffb547", "s18": "#ffb547", "s19": TEAL, "s20": LIME, "s21": TEAL,
       "s22": TEAL, "s23": TEAL, "s24": "#ffb066", "s25": "#ffb066", "s30": "#ff6b6b", "s31": TEAL, "s33": "#ffd36b", "s34": "#ffd36b",
       "s35": "#ffd36b", "s36": GH, "s37": GH, "s38": "#7ee787", "s41": "#ffd36b", "s43": SCI, "s44": DECODER, "s45": "#ffd36b",
       "s46": QUANTA, "s48": QUANTA, "s49": TEAL, "s50": "#ffb547", "s52": "#ffb547", "s54": LIME, "s56": LIME, "s57": LIME}
for k, v in AUTO.items():
    if v and k not in COL:
        COL[k] = v

YEL = "rgba(255,214,90,0.55)"
HL = {  # shot -> [(source, phrase, near y, sweep start, colour)]
    "s13": [("page:f13", "for many decades no proof was found", None, 20.6, YEL)],
    "s17": [("page:clay_mill", "established seven Prize Problems", 1813, 31.3, YEL)],
    "s18": [("page:f18", "$1 million allocated to the solution of each", None, 33.45, YEL)],
    "s19": [("pdf:oa:5", "order of 10,000 concurrent", 470, 36.0, YEL)],
    "s21": [("pdf:oa:5", "about 88 hours after", 3048, 39.6, YEL)],
    "s22": [("pdf:oa:2", "can develop a singularity in a finite time", 2709, 41.15, YEL)],
    "s23": [("pdf:oa:3", "spirals inward", 249, 43.3, YEL),
            ("pdf:oa:3", "This central region shrinks while it speeds up", 331, 44.5, YEL)],
    "s31": [("pdf:oa:2", "The fluid has a smooth", 2709, 62.3, YEL), ("pdf:oa:2", "force applied to it", 2791, 63.25, YEL)],
    "s33": [("pdf:cl:2", "(C) Breakdown of Navier", 1686, 68.7, YEL), ("box", (1854, 1734, 210, 42), None, 69.2, YEL),
            ("box", (528, 1784, 120, 42), None, 69.35, YEL)],
    "s35": [("pdf:cl:2", "(A) Existence and smoothness", 1241, 72.4, "rgba(120,220,255,0.5)"),
            ("pdf:cl:2", "Take f (x, t) to be identically zero", 1340, 73.3, "rgba(120,220,255,0.5)")],
    "s37": [("page:f37", "Lean certificates accompanying Navier-Stokes", None, 77.5, "rgba(121,184,255,0.35)")],
    "s43": [("sciam.jpg", "isn't what you think it is", 647, 92.6, "rgba(142,197,255,0.5)")],
    "s44": [("page:f44", "doesn't understand its own", None, 95.3, YEL)],
    "s45": [("pdf:cl:1", "CHARLES L. FEFFERMAN", 817, 97.3, YEL)],
    "s46": [("page:f46", "The heroes of the story", None, 100.3, YEL), ("page:f46", "Cordoba and Martinez-Zoroa.", None, 100.9, YEL)],
    "s48": [("page:f48", "the computational cost at several million dollars", None, 105.5, YEL)],
    "s49": [("pdf:oa:7", "We do not intend to claim the Millennium Prize", 424, 108.1, YEL)],
    "s50": [("page:clay_poincare", "Poincaré Conjecture", None, 111.6, YEL), ("page:clay_poincare", "Perelman's proof", None, 113.6, YEL)],
    "s52": [("page:f52", "at least two years must have passed", None, 116.6, YEL)],
}
DARK = {"s36", "s37", "s38"}


def origin(sid, sp, kind):
    if kind == "PAGE":
        return 0, sp["y0"]
    if kind == "PDF":
        return sp["box"][0], sp["box"][1]
    if kind == "IMG":
        return sp["crop"][0], sp["crop"][1]
    return 0, 0


GEOM, HL_JS = {}, []


def card(sid, kind, sp):
    m = META[sid]
    w = sp.get("w", 1000)
    s = w / m["pw"]
    full = round(m["ph"] * s)
    h = min(full, sp.get("view", 10 ** 6))
    left = (1080 - w) // 2
    top = max(300, round(760 - h / 2))
    if top + h > 1225:
        top = max(240, 1225 - h)
    GEOM[sid] = (left, top, w, h, s, full)
    ox, oy = origin(sid, sp, kind)
    inner = f'<div class="scroller" id="sc-{sid}"><img src="assets/img/{sid}.png" alt="" style="left:0;top:0;width:{w}px" />'
    hls = []
    for k, (name, phrase, ny, t, col) in enumerate(HL.get(sid, [])):
        boxes = [phrase] if name == "box" else locate(name, phrase, ny)
        acc, tot = 0.0, sum(b[2] for b in boxes)
        if name != "box":
            x0 = min(b[0] for b in boxes); x1 = max(b[0] + b[2] for b in boxes)
            y0 = min(b[1] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
            hls.append([t, round(left + ((x0 + x1) / 2 - ox) * s, 1), round(top + ((y0 + y1) / 2 - oy) * s - (sp.get("y0", 0) if False else 0), 1), round((x1 - x0) * s, 1)])
        for j, (x, y, bw, bh) in enumerate(boxes):
            pad, hid = 6, f"hl-{sid}-{k}-{j}"
            inner += (f'<div class="hl" id="{hid}" style="left:{(x - ox) * s - pad:.0f}px;top:{(y - oy) * s - pad * 0.6:.0f}px;'
                      f'width:{bw * s + 2 * pad:.0f}px;height:{bh * s + pad * 1.2:.0f}px;background:{col}"></div>')
            d = 0.42 * bw / max(tot, 1) + 0.08
            HL_JS.append([hid, round(t + acc, 3), round(d, 3)])
            acc += d
    inner += "</div>"
    GEOM[sid] = (left, top, w, h, s, full, hls)
    dark = " dark" if sid in DARK else ""
    return f'<div class="card{dark}" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">{inner}</div>'


def vid(src, t0, d, css, ms=0.0, name=None, cls="vid"):
    vidn = "v-" + (name or src.split("/")[-1].split(".")[0])
    d = min(d, DUR - t0)
    return (f'<video id="{vidn}" class="{cls}" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-media-start="{ms:.3f}" style="{css}"></video>')


FULL = "left:0;top:0;width:1080px;height:1920px"
DOCCAM = {"s13", "s17", "s18", "s19", "s21", "s22", "s23", "s31", "s33", "s35", "s37", "s43", "s44", "s45", "s46", "s48", "s49", "s50", "s52"}
blocks = []
for z, (sid, t0, t1, kind, sp) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:
        a, d, ms = 0.0, d + (t0 - H), H - t0
    bd = f'<div class="bd" style="background-image:url(assets/img/{sid}_bd.jpg)"></div><div class="desk"></div>'
    if kind in ("V", "CUT", "SIM"):
        inner = vid(f"assets/clips/{sid}.mp4", a, d, FULL, ms)
        if "blend" in sp:
            inner += vid(f"assets/clips/{sid}_b.mp4", a, d, FULL + ";mix-blend-mode:screen;opacity:0.9", ms, name=f"{sid}_b")
        if "freeze" in sp:
            inner += f'<img class="frz" id="frz-{sid}" src="assets/img/{sid}_freeze.png" alt="" />'
    elif kind == "SPLIT":
        inner = (vid(f"assets/clips/{sid}_top.mp4", a, d, "left:0;top:0;width:1080px;height:960px", ms, name=f"{sid}_top")
                 + vid(f"assets/clips/{sid}_bot.mp4", a, d, "left:0;top:960px;width:1080px;height:960px", ms, name=f"{sid}_bot")
                 + '<div class="splitline"></div>')
    elif kind == "FREEZE":
        inner = f'<img class="still" id="st-{sid}" src="assets/img/{sid}.png" alt="" style="{FULL}" />'
    elif kind in ("PAGE", "PDF", "IMG"):
        inner = bd + card(sid, kind, sp)
    elif kind == "PAIR":
        w = sp["w"]
        ha = round(META[sid]["a"]["ph"] * w / META[sid]["a"]["pw"])
        hb = round(META[sid]["b"]["ph"] * w / META[sid]["b"]["pw"])
        inner = (bd + f'<div class="card" id="card-{sid}a" style="left:40px;top:360px;width:{w}px;height:{ha}px"><img src="assets/img/{sid}_a.png" alt="" style="left:0;top:0;width:{w}px" /></div>'
                 f'<div class="card dark" id="card-{sid}b" style="left:40px;top:{430 + ha + 150}px;width:{w}px;height:{hb}px"><img src="assets/img/{sid}_b.png" alt="" style="left:0;top:0;width:{w}px" /></div>')
        GEOM[sid] = (40, 360, w, ha, 430 + ha + 150, hb)
    elif kind == "END":
        inner = '<div class="bd" style="background-image:url(assets/img/s56_last.png);filter:blur(30px) brightness(0.45)"></div>'
    # document-camera shots zoom their card past the visual band; fade it out above the caption band and under the labels
    fade = '<div class="docfade"></div><div class="doctop"></div>' if sid in DOCCAM else ""
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}">'
                  f'<div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div>{fade}</div></div>')

# ---------------------------------------------------------------- captions: mode per chunk, colour of the shot under it
CAPS = json.loads(open("captions.js").read()[len("window.CAPS = "):].rstrip().rstrip(";"))
B_AT = {1.28: "", 3.14: "clock", 33.33: "", 36.68: "", 39.42: "clock"}
C_AT = {}
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
COVERS = [[128.45, 999]]

LABELS = {
    "REAL · CLAYMATH.ORG": ["s13", "s17", "s18", "s50", "s52"],
    "REAL · OPENAI · 8 SEP 2026": ["s19", "s21", "s22", "s23", "s24", "s31", "s49"],
    "REAL · THE OFFICIAL PROBLEM · CLAY INSTITUTE": ["s33", "s35", "s45"],
    "REAL · GITHUB · THE LEAN PROOF": ["s36", "s37", "s38"],
    "REAL · CLAY'S (C) vs THE LEAN STATEMENT": ["s41"],
    "REAL · SCIENTIFIC AMERICAN · 13 OCT": ["s43"],
    "REAL · THE DECODER · 17 OCT": ["s44"],
    "REAL · QUANTA MAGAZINE": ["s46", "s48"],
    "REAL · NASA · HURRICANE MARIA, 2017": ["s55"],
    "SIMULATION · THE REAL EQUATIONS, IN 2D": ["s16"],
    "ANIMATION · AFTER OPENAI'S VORTEX FIGURE": ["s01", "s25"],
    "ANIMATION · 10,000 LIGHTS": ["s20", "s56"],
}
T = {s[0]: (s[1], s[2]) for s in SHOTS}
LAB_JS, lab_html = [], []
for k, (txt, ids) in enumerate(LABELS.items()):
    gen = not txt.startswith("REAL")
    lab_html.append(f'<div class="src{" gen" if gen else ""}" id="src{k}"><span class="sd"></span>{txt}</div>')
    spans = []
    for i in ids:
        a, b = T[i]
        if spans and abs(spans[-1][1] - a) < 0.01:
            spans[-1][1] = b
        else:
            spans.append([a, b])
    for a, b in spans:
        LAB_JS.append([f"#src{k}", round(a + 0.12, 2), round(b - 0.08, 2)])

track = json.load(open("work/track_s32.json"))
shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%LABJS%", json.dumps(LAB_JS)).replace("%HLJS%", json.dumps(HL_JS)).replace("%GEO%", json.dumps(GEOM))
       .replace("%CAPLAY%", json.dumps(CAPLAY)).replace("%COVERS%", json.dumps(COVERS)).replace("%COL%", json.dumps(COL))
       .replace("%TRACK%", json.dumps(track)).replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(HL_JS), "highlight strips")

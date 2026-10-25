"""Write index.html for Short #10 from edl.py, words.json, work/meta.json, assets/pages/pages.json and work/chart_data.json.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, or a page card or graphics over a moving,
blurred backdrop clip. Captions are designed into each shot (window.CAPS from make_captions.py): S standard, A hero word.
Each chunk takes the colour of the shot under it.
Usage: python3 make_index.py
"""
import json

from edl import SHOTS, H, DUR, W, wt

META = json.load(open("work/meta.json"))
CHART = json.load(open("work/chart_data.json"))
LIME, BLUE, AMBER, GOLD, CORAL = "#c8ff4d", "#7cc4ff", "#ffb547", "#ffd84a", "#ff8a7a"
COL = {"s10": BLUE, "s13": GOLD, "s14": GOLD, "s15": "#ffffff", "s16": BLUE, "s17": LIME, "s19": BLUE, "s20": AMBER, "s21": BLUE,
       "s23": BLUE, "s24": CORAL, "s25": BLUE, "s26": CORAL, "s27": CORAL}
HL_T = {"s10": wt(66), "s19": wt(122), "s25": wt(175)}   # when each page's highlight sweeps (on the spoken words)
GEOM, HL_JS = {}, []
T = {s[0]: (s[1], s[2]) for s in SHOTS}


def card(sid, sp):
    m = META[sid]
    w = sp.get("w", 1000)
    s = w / m["pw"]
    h = round(m["ph"] * s)
    left = (1080 - w) // 2
    top = max(300, round(740 - h / 2))
    if top + h > 1225:
        top = max(240, 1225 - h)
    inner = f'<img src="assets/pages/{sp["name"]}.png" alt="" style="left:0;top:0;width:{w}px" />'
    boxes = m["boxes"]
    t, acc, tot = HL_T[sid], 0.0, sum(b[2] for b in boxes)
    for j, (x, y, bw, bh) in enumerate(boxes):
        hid = f"hl-{sid}-{j}"
        inner += f'<div class="hl" id="{hid}" style="left:{x * s:.0f}px;top:{y * s:.0f}px;width:{bw * s:.0f}px;height:{bh * s:.0f}px"></div>'
        d = 0.5 * bw / max(tot, 1) + 0.08
        HL_JS.append([hid, round(t + acc, 3), round(d, 3)])
        acc += d
    x0 = min(b[0] for b in boxes); x1 = max(b[0] + b[2] for b in boxes)
    y0 = min(b[1] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
    hx = left + (x0 + x1) / 2 * s if (x1 - x0) * s < 0.6 * w else left + w / 2
    hw = (x1 - x0) * s if (x1 - x0) * s < 0.6 * w else w
    GEOM[sid] = (left, top, w, h, s, h, [[t, round(hx, 1), round(top + (y0 + y1) / 2 * s, 1), round(hw, 1)]])
    return f'<div class="card" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">{inner}</div>'


def vid(src, t0, d, ms=0.0, name=None):
    vidn = "v-" + (name or src.split("/")[-1].split(".")[0])
    d = min(d, DUR - t0)
    return (f'<video id="{vidn}" class="vid" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-media-start="{ms:.3f}" style="left:0;top:0;width:1080px;height:1920px"></video>')


blocks = []
for z, (sid, t0, t1, kind, sp) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:
        a, d, ms = 0.0, d + (t0 - H), H - t0
    if kind == "V":
        inner = vid(f"assets/clips/{sid}.mp4", a, d, ms)
    elif kind == "PAGE":
        inner = vid(f"assets/clips/{sid}.mp4", a, d, ms) + card(sid, sp)
    elif kind == "GFX":
        inner = vid(f"assets/clips/{sid}.mp4", a, d, ms) + f'<div class="gfx" id="gx-{sid}"></div>'
    elif kind == "END":
        inner = f'<div class="bd" style="background-image:url(assets/img/{sid}_bd.png);filter:blur(30px) brightness(0.45)"></div>'
    fade = '<div class="docfade"></div><div class="doctop"></div>' if kind == "PAGE" else ""
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}">'
                  f'<div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div>{fade}</div></div>')

# ---------------------------------------------------------------- captions: mode per chunk, colour of the shot under it
CAPS = json.loads(open("captions.js").read()[len("window.CAPS = "):].rstrip().rstrip(";"))
CAPLAY = []
for ch in CAPS:
    t = ch["t0"]
    sid = [s[0] for s in SHOTS if s[1] - 0.02 <= t + 0.06 < s[2]][0]
    col = COL.get(sid, LIME)
    spec = dict(m="A", c=col) if any(w["emph"] for w in ch["w"]) else dict(m="S", c=col)
    CAPLAY.append([round(t - 0.01, 3), round(ch["t1"], 3), spec])
COVERS = [[0.0, T["s02"][0] - 0.02], [T["s30"][0], 999]]   # frame one carries the claim title; the end card says the rest

GEN = "AI ILLUSTRATION · GOOGLE FLOW"
LABELS = {
    GEN: ["s02", "s06", "s18", "s22", "s24", "s26", "s27", "s28"],
    "REAL · OPENAI HELP CENTER": ["s10", "s19", "s25"],
    "QUOTED · CLAUDE HELP CENTER": ["s16", "s21", "s23"],
    "DATA · OPENAI'S CHART, REDRAWN": ["s20"],
    "MAP · NATURAL EARTH": ["s17"],
}
LAB_JS, lab_html = [], []
for k, (txt, ids) in enumerate(LABELS.items()):
    cls = " gen" if txt.startswith("AI ") else (" q" if not txt.startswith("REAL") else "")
    lab_html.append(f'<div class="src{cls}" id="src{k}"><span class="sd"></span>{txt}</div>')
    spans = []
    for i in sorted(ids, key=lambda q: T[q][0]):
        a, b = T[i]
        if spans and abs(spans[-1][1] - a) < 0.01:
            spans[-1][1] = b
        else:
            spans.append([a, b])
    for a, b in spans:
        LAB_JS.append([f"#src{k}", round(a + 0.12, 2), round(b - 0.08, 2)])

# ---------------------------------------------------------------- overlay positions measured on the footage
CENTER, SC0, SC1 = (540, 864), 1.04, 1.12            # s06's camera: scale 1.04 -> 1.12 about (540, 864)
a6, b6 = T["s06"][0] - H, T["s06"][1] + H
sin6 = 1.4


def weight_at(src_t):   # the hidden weight, measured at 2.6 s (585, 1080) and 4.6 s (909, 1192) of the Flow clip
    f = (src_t - 2.6) / 2.0
    return 585 + 324 * f, 1080 + 112 * f


def cam6(p, sc):
    return round(CENTER[0] + sc * (p[0] - CENTER[0]), 1), round(CENTER[1] + sc * (p[1] - CENTER[1]), 1)


wa = cam6(weight_at(sin6 - H), SC0); wb = cam6(weight_at(sin6 - H + (b6 - a6)), SC1)
CONSTS = (f"const WEIGHT = {json.dumps([wa, wb])}, PARIS_PIN = [403, 690], LONDON_PIN = [567, 640], "
          f"PHONE = [440, 860, 300, 90, -6];")

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%LABJS%", json.dumps(LAB_JS)).replace("%HLJS%", json.dumps(HL_JS)).replace("%GEO%", json.dumps(GEOM))
       .replace("%CAPLAY%", json.dumps(CAPLAY)).replace("%COVERS%", json.dumps(COVERS))
       .replace("%WS%", json.dumps([x["start"] for x in W])).replace("%WE%", json.dumps([x["end"] for x in W]))
       .replace("%CHART%", json.dumps(CHART)).replace("%CONSTS%", CONSTS)
       .replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(HL_JS), "highlight strips; weight", wa, wb)

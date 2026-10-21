"""Write index.html for Short #6 from edl.py, work/meta.json, work/colors.json and the OCR'd highlights.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, a still, or a card on a blurred backdrop.
Captions are designed into each shot (window.CAPS from make_captions.py, laid out by CAPLAY below):
  S  centred above the platform buttons, unspoken words dim, the spoken word in the shot's colour
  A  left-aligned; emphasis words become huge tilted hero words with a glow bar
  B  a number token becomes the caption itself and counts up while it is spoken
  C  the words sit on an angled glass panel in the scene with a leader line to the subject
Usage: python3 make_index.py
"""
import json

import cv2
import numpy as np
from PIL import Image

from edl import SHOTS, H, DUR
from locate import locate

META = json.load(open("work/meta.json"))
AUTO = json.load(open("work/colors.json"))
CLAY, ICE, CYAN = "#f0a07f", "#bfe6ff", "#4fd0ff"
COL = {"s04": CLAY, "s05": ICE, "s10": CLAY, "s11": CLAY, "s13": CLAY, "s15": CLAY, "s16": "#8cc0ff", "s17": CYAN,
       "s18a": "#5ee08a", "s18b": "#ffb02e", "s19": CYAN, "s20": "#ecc56e", "s23": CYAN, "s24": CLAY, "s25": ICE,
       "s26": CLAY, "s27": "#b9a2ff", "s29": CLAY, "s35": "#c8ff4d", "s07": "#ffa45c"}
for k, v in AUTO.items():
    if v and k not in COL:
        COL[k] = v

# ---------------------------------------------------------------- cards
HDR = Image.open("work/img/page_header.png").crop((0, 25, 1240, 215))
HDR.save("assets/img/page_header_c.png")
HDR_H = HDR.size[1]
MARK = "rgba(217,119,87,0.42)"  # Anthropic clay as a highlighter on the cream page

# highlights: shot -> [(source name, phrase, near y, sweep start time, colour)]
HL = {
    "s04": [("anthropic_x.jpg", "previously unknown enzyme system", 272, 5.0, MARK)],
    "s10": [("page", "novel enzyme system with CRISPR-like repeats", 600, 17.3, MARK)],
    "s13": [("page", "over 200,000 RTs", 15209, 26.32, MARK), ("page", "3,500 new candidate systems", 15278, 26.7, MARK),
            ("page", "the 20 most compelling candidates", 15347, 28.6, MARK)],
    "s15": [("page", "The DNA next to the RT] is spectacular", 15950, 32.55, MARK),
            ("page", "tandem repeat array", 16040, 33.6, MARK)],
    "s18a": [("techcrunch.png", "already found something big", 2017, 39.7, "rgba(255,255,255,0.28)")],
    "s18b": [("aljazeera.jpg", "CRISPR-like enzyme system", 537, 40.6, "rgba(255,176,46,0.45)")],
    "s20": [("nobel.jpg", "Nobel Prize in Chemistry 2020", 834, 44.55, "rgba(236,197,110,0.55)"),
            ("nobel.jpg", "for the development of a method for genome editing", 1500, 43.4, "rgba(236,197,110,0.45)")],
    "s24": [("page", "Although we don't yet know its function", 5567, 53.6, MARK)],
    "s26": [("page", "Feng Zhang, one of the pioneers of CRISPR", 6900, 61.0, MARK),
            ("page", "genuinely intriguing and merits further investigation", 7454, 62.1, MARK)],
    "s27": [("decrypt.jpg", "It Just Doesn't Know What", 783, 64.3, "rgba(185,162,255,0.5)")],
    "s29": [("page", "Our involvement was limited to the initial prompt and the lab work", 8024, 69.4, MARK)],
}
SRC_OF = {sid: (sp.get("file") or "page") for sid, _, _, k, sp in SHOTS if k in ("PAGE", "IMG")}


def card_geom(sid, kind, sp):
    """left, top, width, scale, content offset (header) for a card shot"""
    m = META[sid]
    w = sp.get("w", 1000)
    s = w / m["pw"]
    head = round(HDR_H * w / 1240) if kind == "PAGE" else 0
    h = head + round(m["ph"] * s)
    left = (1080 - w) // 2
    top = {"s20": 300, "s10": 300}.get(sid, max(300, min(330, 1210 - h)))
    if h + top > 1225:
        top = max(250, 1225 - h)
    return left, top, w, h, s, head


GEOM = {}
HL_JS = []


def card_html(sid, kind, sp):
    left, top, w, h, s, head = card_geom(sid, kind, sp)
    GEOM[sid] = (left, top, w, h, s, head)
    inner = ""
    if kind == "PAGE":
        inner += f'<img src="assets/img/page_header_c.png?{sid}" alt="" style="left:0;top:0;width:{w}px" />'
        inner += f'<img src="assets/img/{sid}.png" alt="" style="left:0;top:{head}px;width:{w}px" />'
    else:
        inner += f'<img src="assets/img/{sid}.png" alt="" style="left:0;top:0;width:{w}px" />'
    ox, oy = (0, sp["y0"]) if kind == "PAGE" else ((sp["crop"][0], sp["crop"][1]) if kind == "IMG" else (0, 0))
    for k, (name, phrase, ny, t, col) in enumerate(HL.get(sid, [])):
        boxes = locate(name, phrase, ny)
        acc = 0.0
        tot = sum(b[2] for b in boxes)
        for j, (x, y, bw, bh) in enumerate(boxes):
            pad = 6
            hid = f"hl-{sid}-{k}-{j}"
            inner += (f'<div class="hl" id="{hid}" style="left:{(x - ox) * s - pad:.0f}px;top:{head + (y - oy) * s - pad * 0.6:.0f}px;'
                      f'width:{bw * s + 2 * pad:.0f}px;height:{bh * s + pad * 1.2:.0f}px;background:{col}"></div>')
            d = 0.42 * bw / max(tot, 1) + 0.08
            HL_JS.append([hid, round(t + acc, 3), round(d, 3)])
            acc += d
    return f'<div class="card{" pagecard" if kind == "PAGE" else ""}" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">{inner}</div>'


def vid(src, t0, d, css, ms=0.0, name=None):
    vidn = "v-" + (name or src.split("/")[-1].split(".")[0])
    d = min(d, DUR - t0)
    return (f'<video id="{vidn}" class="vid" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-media-start="{ms:.3f}" style="{css}"></video>')


# DNA chips (14 highlighted repeats in the post's figure)
lit = np.asarray(Image.open("assets/img/s16_lit.png").convert("RGB")).astype(int)
mask = (((lit[..., 2] - lit[..., 0]) > 28) & (lit[..., 2] > 120)).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((9, 15), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(mask)
CHIPS = sorted([tuple(int(v) for v in st[i][:4]) for i in range(1, n) if st[i][4] > 300], key=lambda b: (b[1], b[0]))

blocks = []
for z, (sid, t0, t1, kind, sp) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:
        a, d, ms = 0.0, d + (t0 - H), H - t0
    inner = ""
    if kind == "V":
        inner = vid(f"assets/clips/{sid}.mp4", a, d, "left:0;top:0;width:1080px;height:1920px", ms)
    elif kind == "STILL":
        if sid in ("s05", "s25"):
            inner = f'<img class="still" id="st-{sid}" src="assets/img/{sid}.jpg" alt="" />'
        else:
            inner = f'<img class="still" id="st-{sid}" src="assets/img/{sid}.png" alt="" style="left:0;top:0;width:1080px;height:1920px" />'
            inner += '<div class="bookglow" id="bookglow"></div>'
    elif kind in ("PAGE", "IMG", "FIG"):
        inner = f'<div class="bd" style="background-image:url(assets/img/{sid}_bd.jpg)"></div><div class="desk"></div>'
        inner += card_html(sid, kind, sp)
    elif kind == "DNA":
        m = META[sid]; w = 1000; s = w / m["pw"]; h = round(m["ph"] * s); left, top = 40, 300
        GEOM[sid] = (left, top, w, h, s, 0)
        chips = "".join(f'<div class="dchip" id="chip-{k}" style="left:{x * s - 4:.0f}px;top:{y * s - 4:.0f}px;width:{bw * s + 8:.0f}px;height:{bh * s + 8:.0f}px"></div>'
                        for k, (x, y, bw, bh) in enumerate(CHIPS))
        inner = (f'<div class="bd" style="background-image:url(assets/img/{sid}_bd.jpg)"></div><div class="desk"></div>'
                 f'<div class="card" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;background:#f4f1ea">'
                 f'<img src="assets/img/{sid}_dense.png" alt="" style="left:0;top:0;width:{w}px" />'
                 f'<img id="dnalit" src="assets/img/{sid}_lit.png" alt="" style="left:0;top:0;width:{w}px;clip-path:inset(0 0 100% 0)" />'
                 f'{chips}<div class="scan" id="scan" style="width:{w}px"></div></div>')
    elif kind == "GRID":
        inner = (f'<div class="bd" style="background-image:url(assets/img/{sid}_bd.jpg)"></div><div class="desk"></div>'
                 f'<canvas id="agents" width="1080" height="1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px"></canvas>')
    elif kind == "END":
        inner = '<div class="bd" style="background-image:url(assets/img/s34_last.png);filter:blur(30px) brightness(0.4)"></div>'
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}">'
                  f'<div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div></div></div>')

# figure overlays (fig coordinates are 300-dpi pixels inside the crop; the card shows 600-dpi pixels)
def figpt(sid, x, y):
    left, top, w, h, s, head = GEOM[sid]
    return left + x * 2 * s, top + y * 2 * s

TICKS = [160, 198, 233, 267, 302, 341, 380, 423, 455, 490, 522, 555, 589, 623]  # fig 1F repeat ticks (x)
F1F = {"bar_y": 125, "rows_y0": 249, "row_h": 25.5, "core_x0": 270, "core_x1": 508}

# ---------------------------------------------------------------- caption layout
# (t0, t1, spec): which design each caption chunk uses, chosen by the chunk's start time
CAPLAY = [
    (0.00, 2.36, dict(m="B", c=COL["s01"])),
    (2.36, 4.58, dict(m="B", c=COL["s03"], fmt="clock")),
    (4.58, 5.21, dict(m="S", c=CLAY)),
    (5.21, 7.79, dict(m="A", c=ICE)),
    (7.79, 10.37, dict(m="S", c=COL["s06"])),
    (10.37, 12.77, dict(m="A", c=COL["s07"])),
    (12.77, 14.22, dict(m="S", c=COL["s08"])),
    (14.22, 16.81, dict(m="C", c=COL["s09"], px=70, py=1050, pw=560, tx=430, ty=770)),
    (16.81, 19.19, dict(m="S", c=CLAY)),
    (19.19, 20.81, dict(m="B", c=CLAY)),
    (20.81, 22.41, dict(m="A", c=CLAY)),
    (22.41, 23.04, dict(m="S", c=COL["s12a"])),
    (23.04, 24.77, dict(m="B", c=COL["s12c"])),
    (24.77, 26.29, dict(m="S", c=COL["s12e"])),
    (29.83, 32.34, dict(m="C", c=COL["s14"], px=60, py=1100, pw=600, tx=600, ty=900)),
    (32.34, 34.49, dict(m="S", c=CLAY)),
    (34.49, 36.94, dict(m="S", c=COL["s16"])),
    (36.94, 39.57, dict(m="S", c=CYAN)),
    (39.57, 41.44, dict(m="A", c=COL["s18b"])),
    (41.44, 43.21, dict(m="A", c=CYAN)),
    (43.21, 45.69, dict(m="S", c=COL["s20"])),
    (45.69, 48.24, dict(m="S", c=COL["s21b"])),
    (48.24, 50.15, dict(m="S", c=COL["s22"])),
    (50.15, 53.47, dict(m="S", c=CYAN)),
    (53.47, 55.50, dict(m="S", c=CLAY)),
    (55.50, 57.72, dict(m="A", c=ICE)),
    (57.72, 60.84, dict(m="C", c=ICE, px=430, py=330, pw=600, tx=254, ty=1018)),
    (60.84, 63.49, dict(m="S", c=CLAY)),
    (63.49, 67.18, dict(m="S", c=COL["s27"])),
    (67.18, 69.18, dict(m="A", c=COL["s28a"])),
    (69.18, 71.17, dict(m="A", c=CLAY)),
    (71.17, 72.47, dict(m="S", c=COL["s30"])),
    (72.47, 74.73, dict(m="A", c=COL["s31c"])),
    (74.73, 76.04, dict(m="S", c=COL["s32"])),
    (76.04, 78.13, dict(m="A", c=COL["s33"], serif="EUREKA")),
    (78.13, 81.01, dict(m="A", c=COL["s34"])),
]
COVERS = [[26.29, 29.83], [81.0, 99]]
LABELS = {  # small source marks under the tag
    "REAL · @ANTHROPICAI ON X": ["s04"],
    "REAL · PHAGES ON A BACTERIUM · ELECTRON MICROSCOPE": ["s05", "s25"],
    "REAL · ANTHROPIC.COM · 23 SEP 2026": ["s10", "s13", "s15", "s24", "s26", "s29"],
    "REAL · THE RAW DNA CLAUDE WAS READING": ["s16"],
    "REAL · PREPRINT · YOON ET AL., ANTHROPIC, 2026": ["s17", "s19", "s23"],
    "REAL · TECHCRUNCH": ["s18a"], "REAL · AL JAZEERA": ["s18b"], "REAL · NOBELPRIZE.ORG": ["s20"], "REAL · DECRYPT": ["s27"],
    "REAL · ANTHROPIC'S LAB": ["s21a", "s21b", "s22", "s28a", "s28b", "s30", "s32", "s33"],
    "AI ILLUSTRATION · VEO 3.1": ["s01", "s12e", "s14", "s31c", "s34"],
}
T = {s[0]: (s[1], s[2]) for s in SHOTS}
LAB_JS = []
lab_html = []
for k, (txt, ids) in enumerate(LABELS.items()):
    gen = txt.startswith("AI")
    lab_html.append(f'<div class="src{" gen" if gen else ""}" id="src{k}"><span class="sd"></span>{txt}</div>')
    # merge consecutive shots into one showing
    spans = []
    for i in ids:
        a, b = T[i]
        if spans and abs(spans[-1][1] - a) < 0.01:
            spans[-1][1] = b
        else:
            spans.append([a, b])
    for a, b in spans:
        LAB_JS.append([f"#src{k}", round(a + 0.12, 2), round(b - 0.08, 2)])

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
geo_js = json.dumps({k: v for k, v in GEOM.items()})
fig_js = json.dumps({
    "ticks": [figpt("s17", x, F1F["bar_y"]) for x in TICKS],
    "rows": [[*figpt("s17", F1F["core_x0"] - 4, F1F["rows_y0"] + r * F1F["row_h"]),
              (F1F["core_x1"] - F1F["core_x0"] + 8) * 2 * GEOM["s17"][4], F1F["row_h"] * 2 * GEOM["s17"][4]] for r in range(14)],
    "art": [*figpt("s19", 366, 314), (607 - 366) * 2 * GEOM["s19"][4], (361 - 314) * 2 * GEOM["s19"][4]],
    "artrow": [*figpt("s19", 0, 314), GEOM["s19"][2], (361 - 314) * 2 * GEOM["s19"][4]],
    "sa1": [*figpt("s23", 642, 45), (1150 - 642) * 2 * GEOM["s23"][4], (82 - 45) * 2 * GEOM["s23"][4]],
    "rna": [[*figpt("s23", x0, 102), (x1 - x0) * 2 * GEOM["s23"][4]] for x0, x1 in ((700, 770), (885, 970), (1020, 1117))],
})

HTML = open("index_template.tpl").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%LABJS%", json.dumps(LAB_JS)).replace("%HLJS%", json.dumps(HL_JS)).replace("%GEO%", geo_js)
       .replace("%FIG%", fig_js).replace("%CAPLAY%", json.dumps([[a, b, s] for a, b, s in CAPLAY]))
       .replace("%COVERS%", json.dumps(COVERS)).replace("%COL%", json.dumps(COL))
       .replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(HL_JS), "highlight strips,", len(CHIPS), "DNA chips")

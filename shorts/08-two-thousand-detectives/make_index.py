"""Write index.html for Short #8 from edl.py, work/meta.json, work/colors.json, the located highlights and the 3D pins.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, a 3D render, or a card / graphic on a blurred
backdrop. Captions are designed into each shot (window.CAPS from make_captions.py): S standard, A hero word, B the number
is the caption (counts up; "mm" counts a stopwatch to the minutes). Each chunk takes the colour of the shot under it.
Usage: python3 make_index.py
"""
import csv
import json
import os

from edl import SHOTS, H, DUR
from locate import locate

META = json.load(open("work/meta.json"))
AUTO = json.load(open("work/colors.json")) if os.path.exists("work/colors.json") else {}
AMBER, TEAL, LIME, PURPLE, RED, OA = "#ffb547", "#4fd0ff", "#c8ff4d", "#b99cff", "#ff6b6b", "#7fe0c8"
COL = {"s02": TEAL, "s05": "#7ee0a8", "s11": AMBER, "s12": TEAL, "s13": AMBER, "s16": AMBER, "s19": PURPLE, "s20": PURPLE,
       "s21": TEAL, "s24": AMBER, "s25": AMBER, "s26": AMBER, "s27": PURPLE, "s28": PURPLE, "s29": AMBER, "s30": TEAL,
       "s31": AMBER, "s34": AMBER, "s38": OA, "s39": RED, "s40": TEAL, "s41": OA, "s43": RED, "s44": AMBER, "s48": AMBER,
       "s52": PURPLE, "s56": LIME}
for k, v in AUTO.items():
    if v and k not in COL:
        COL[k] = v

YEL = "rgba(255,214,90,0.55)"
HL = {  # shot -> [(source, phrase or box, near y, sweep start, colour)]
    "s13": [("pdf:at:1", "1,947 disease-associated genes", None, 24.35, YEL)],
    "s20": [("box", (40, 962, 1500, 78), None, 42.45, YEL)],
    "s26": [("pdf:at:1", "Genome-scale functional mapping of the mammalian whole brain with in vivo Perturb-seq", None, 56.05, YEL)],
    "s28": [("box", (676, 258, 128, 96), None, 65.1, "rgba(185,156,255,0.45)")],
    "s30": [("atlas_0.3.png", "Dctn1", 1192, 68.95, "rgba(79,208,255,0.35)", 820)],
    "s38": [("pdf:oa:7", "research suggesting that problems with cholesterol transport may cause cells to make more cholesterol", None, 81.9, YEL)],
    "s41": [("pdf:oa:7", "cause Perry syndrome, a neurodegenerative disease with Parkinson-like symptoms", None, 88.9, YEL)],
}
SRCNAME = {"s05": "q4l.png", "s20": "f1a.png", "s28": "f4k.png", "s30": "atlas_0.3.png", "s52": "f4a.png"}


def origin(sp, kind):
    if kind == "PDF":
        return sp["box"][0], sp["box"][1]
    return sp["crop"][0], sp["crop"][1]


GEOM, HL_JS = {}, []


def card(sid, kind, sp, extra=""):
    m = META[sid]
    w = sp.get("w", 1000)
    s = w / m["src_w"]
    h = round(m["ph"] * w / m["pw"])
    left = (1080 - w) // 2
    top = max(300, round(740 - h / 2))
    if top + h > 1225:
        top = max(240, 1225 - h)
    ox, oy = origin(sp, kind)
    inner = f'<div class="scroller" id="sc-{sid}"><img src="assets/img/{sid}.png" alt="" style="left:0;top:0;width:{w}px" />'
    hls = []
    for k, (name, phrase, ny, t, col, *zw) in enumerate(HL.get(sid, [])):
        boxes = [phrase] if name == "box" else locate(name, phrase, ny)
        acc, tot = 0.0, sum(b[2] for b in boxes)
        x0 = min(b[0] for b in boxes); x1 = max(b[0] + b[2] for b in boxes)
        y0 = min(b[1] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
        cxp = (x0 + x1) / 2 if not zw else ox + (zw[0] / 2 + 40) / s  # a zoom-width override frames the card from its left edge
        hls.append([t, round(left + (cxp - ox) * s, 1), round(top + ((y0 + y1) / 2 - oy) * s, 1), round(zw[0] if zw else (x1 - x0) * s, 1)])
        for j, (x, y, bw, bh) in enumerate(boxes):
            pad, hid = 6, f"hl-{sid}-{k}-{j}"
            inner += (f'<div class="hl" id="{hid}" style="left:{(x - ox) * s - pad:.0f}px;top:{(y - oy) * s - pad * 0.6:.0f}px;'
                      f'width:{bw * s + 2 * pad:.0f}px;height:{bh * s + pad * 1.2:.0f}px;background:{col}"></div>')
            d = 0.42 * bw / max(tot, 1) + 0.08
            HL_JS.append([hid, round(t + acc, 3), round(d, 3)])
            acc += d
    inner += extra + "</div>"
    GEOM[sid] = (left, top, w, h, s, h, hls)
    return f'<div class="card" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">{inner}</div>'


def redactions(sid, sp):
    """Black bars over every text line of a PDF card (the AI never saw this paper)."""
    words = [w for w in json.load(open(f"work/pdf/{sp['doc']}_words.json")) if w["p"] == sp["page"]]
    x, y, w, h = sp["box"]
    s = sp["w"] / w
    lines = []
    for wd in sorted(words, key=lambda q: (q["y"], q["x"])):
        if not (y <= wd["y"] and wd["y"] + wd["h"] <= y + h and x <= wd["x"] and wd["x"] + wd["w"] <= x + w):
            continue
        if lines and abs(wd["y"] - lines[-1][1]) < wd["h"] * 0.5:
            L = lines[-1]; L[0] = min(L[0], wd["x"]); L[2] = max(L[2], wd["x"] + wd["w"]); L[3] = max(L[3], wd["h"])
        else:
            lines.append([wd["x"], wd["y"], wd["x"] + wd["w"], wd["h"]])
    out = ""
    for k, (lx0, ly, lx1, lh) in enumerate(lines):
        out += (f'<div class="redact" style="left:{(lx0 - x) * s - 4:.0f}px;top:{(ly - y) * s - 3:.0f}px;width:{(lx1 - lx0) * s + 8:.0f}px;'
                f'height:{lh * s + 6:.0f}px"></div>')
    return out, len(lines)


def vid(src, t0, d, css, ms=0.0, name=None, cls="vid"):
    vidn = "v-" + (name or src.split("/")[-1].split(".")[0])
    d = min(d, DUR - t0)
    return (f'<video id="{vidn}" class="{cls}" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-media-start="{ms:.3f}" style="{css}"></video>')


FULL = "left:0;top:0;width:1080px;height:1920px"
DOCCAM = {"s13", "s20", "s26", "s30", "s38", "s41", "s52"}
blocks, NRED = [], 0
for z, (sid, t0, t1, kind, sp) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:
        a, d, ms = 0.0, d + (t0 - H), H - t0
    bd = f'<div class="bd" style="background-image:url(assets/img/{sid}_bd.jpg)"></div><div class="desk"></div>'
    if kind in ("V", "SIM", "REC"):
        inner = vid(f"assets/clips/{sid}.mp4", a, d, FULL, ms)
        if "freeze" in sp:
            inner += f'<img class="frz" id="frz-{sid}" src="assets/img/{sid}_freeze.png" alt="" />'
    elif kind in ("PDF", "IMG"):
        extra = ""
        if sid == "s26":
            extra, NRED = redactions(sid, sp)
        inner = bd + card(sid, kind, sp, extra)
    elif kind == "GFX":
        inner = bd + f'<div class="gfx" id="gx-{sid}"></div>'
    elif kind == "END":
        inner = '<div class="bd" style="background-image:url(assets/img/s55_last.png);filter:blur(30px) brightness(0.45)"></div>'
    fade = '<div class="docfade"></div><div class="doctop"></div>' if sid in DOCCAM else ""
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}">'
                  f'<div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div>{fade}</div></div>')

# ---------------------------------------------------------------- captions: mode per chunk, colour of the shot under it
CAPS = json.loads(open("captions.js").read()[len("window.CAPS = "):].rstrip().rstrip(";"))
B_AT = {0.0: "", 2.33: "", 5.01: "mm", 21.7: "", 51.54: "", 53.61: "", 113.08: "", 114.83: "mm"}
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
COVERS = [[117.7, 999]]

GEN = "AI ILLUSTRATION · GOOGLE FLOW"
LABELS = {
    "REAL · OPENAI × PERTURBAI VIDEO": ["s02", "s21", "s40"],
    "REAL · HUMAN EXPERT REVIEW · PREPRINT FIG. 4L": ["s05"],
    GEN: ["s01", "s07", "s08", "s09", "s29", "s32", "s33", "s35", "s36", "s42", "s45", "s53", "s55"],
    "ANIMATION · DNA AND A CRISPR CUT": ["s11"],
    "REAL · THE 1,946 GENES IN THE DATASET": ["s12"],
    "REAL · THE SCIENTISTS' PAPER · BIORXIV": ["s13", "s26"],
    "REAL · HUGGING FACE DATASET CARD": ["s16"],
    "REAL · THE AGENTS' PAPER · FIG. 1A": ["s20"],
    "REAL DATA · AGENTS' PAPER · SAME 893-GENE TASK": ["s24", "s25"],
    "REAL · THE AGENTS' PAPER · ABSTRACT": ["s27"],
    "REAL · BLIND EXPERT TEST · FIG. 4K": ["s28"],
    "REAL · THE AGENTS' FINDINGS SITE": ["s30"],
    "ANIMATION · DYNEIN + DYNACTIN, THE CARGO MOTOR": ["s31", "s44"],
    "REAL · THE AGENTS' FINDING · 13 GENES UP": ["s34"],
    "REAL · OPENAI · 21 OCT 2026": ["s38", "s41"],
    "ANIMATION · THE AGENTS' IDEA, NOT YET TESTED": ["s39", "s43"],
    "REAL · PREPRINT · NOT YET PEER-REVIEWED": ["s48"],
    "REAL · THE AGENTS' KNOWLEDGE GRAPH · FIG. 4A": ["s52"],
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

genes = [r["target_gene"] for r in csv.DictReader(open("work/repo_data/target_deg_burden.csv"))]
pins = {n: json.load(open(f"work/sim3d/{n}_pins.json")) for n in ("helix", "walk", "jam", "pile", "fix") if os.path.exists(f"work/sim3d/{n}_pins.json")}
track = json.load(open("work/track_s29.json")) if os.path.exists("work/track_s29.json") else []
shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%LABJS%", json.dumps(LAB_JS)).replace("%HLJS%", json.dumps(HL_JS)).replace("%GEO%", json.dumps(GEOM))
       .replace("%CAPLAY%", json.dumps(CAPLAY)).replace("%COVERS%", json.dumps(COVERS)).replace("%COL%", json.dumps(COL))
       .replace("%GENES%", json.dumps(genes)).replace("%PINS%", json.dumps(pins)).replace("%TRACK%", json.dumps(track))
       .replace("%NRED%", str(NRED)).replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(HL_JS), "highlight strips,", NRED, "redaction bars")

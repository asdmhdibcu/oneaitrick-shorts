"""Write index.html for Short #13 (9:16) from edl.py, words.json, captions.js, work/meta.json, index_template.tpl and
fx13.js.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, or a paper still / my graphics over a moving
blurred backdrop clip. Material that hasn't arrived shows as a NEEDED slate (previews only; never delivered).
Usage: python3 make_index.py
"""
import json
import os

from edl import SHOTS, H, DUR, MAT, FIGS, W, have

META = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
T = {s[0]: (s[1], s[2]) for s in SHOTS}
KIND = {s[0]: s[3] for s in SHOTS}
ORDER = [s[0] for s in SHOTS]


def vid(src, vid_id, t0, d, ms=0.0):
    d = min(d, DUR - t0)
    return (f'<video id="{vid_id}" class="vid" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-media-start="{ms:.3f}" style="left:0;top:0;width:1080px;height:1920px"></video>')


def slate(codes):
    what = " · ".join(f"{c} · {MAT[c][1]}" for c in codes)
    return f'<div class="slate"><div class="st">NEEDED</div><div class="sd">{what}</div></div>'


def figcard(sid, name, maxw=960, maxh=780, cy=740):
    from PIL import Image
    w, h = Image.open(FIGS[name][0]).size
    s = min(maxw / w, maxh / h)
    cw, ch = round(w * s), round(h * s)
    return (f'<div class="card" id="card-{sid}" style="left:{round(540 - cw / 2)}px;top:{max(300, round(cy - ch / 2))}px;'
            f'width:{cw}px;height:{ch}px"><img src="assets/img/{name}.png" alt="" style="width:{cw}px" /></div>')


blocks = []
for z, (sid, t0, t1, kind, sp) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:
        a, d, ms = 0.0, d + (t0 - H), H - t0
    need = [c for c in (sp.get("m"), sp.get("bd")) if c and not have(c)]
    ok = sid in META and not need
    clip = f"assets/clips/{sid}.mp4"
    if kind == "V":
        inner = vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)
    elif kind == "IMG":
        inner = (vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)) + figcard(sid, sp["img"])
    elif kind == "GFX":
        inner = vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)
    elif kind == "END":
        prev = ORDER[ORDER.index(sid) - 1]
        img = f"assets/img/{prev}_last.png"
        inner = f'<div class="bd" style="background-image:url({img});filter:blur(30px) brightness(0.45)"></div>' if os.path.exists(img) else ""
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}"><div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div></div></div>')

# ---------------------------------------------------------------- cuts: a transition on every cut
SPECIAL = {"s04": "flash", "s13": "scratch", "s15": "flash", "s16": "cut", "s18": "dip", "s20": "card", "s24": "zoom", "s25": "dip",
           "s09": "card", "s26": "dip", "s29": "fade", "s30": "fade"}
CUTS = []
for i in range(len(ORDER) - 1):
    a, b = ORDER[i], ORDER[i + 1]
    k = SPECIAL.get(b) or ("whip", "slideup", "zoom", "whip", "slideup")[i % 5]
    CUTS.append([a, b, k])

# ---------------------------------------------------------------- source labels
LABEL = {}
for sid, kind, sp in ((s[0], s[3], s[4]) for s in SHOTS):
    if kind == "V":
        LABEL[sid] = MAT[sp["m"]][2]
    elif kind == "IMG":
        LABEL[sid] = FIGS[sp["img"]][1]
LABEL.update({"s08": "REAL · EKO'S NOTES, AGENT 9", "s16": "REAL · AGENT 9'S TRANSCRIPT", "s24": "REAL · PAPER, FIG. 5B",
              "s25": "QUOTED · THE PAPER, P. 3"})
groups = {}
for sid in ORDER:
    if LABEL.get(sid):
        groups.setdefault(LABEL[sid], []).append(sid)
LAB_JS, lab_html = [], []
for k, (txt, ids) in enumerate(groups.items()):
    cls = " gen" if txt.startswith("AI ") else " st" if txt.startswith("STOCK") else " q" if txt.startswith("QUOTED") else ""
    lab_html.append(f'<div class="src{cls}" id="src{k}"><span class="sd"></span>{txt}</div>')
    spans = []
    for i in sorted(ids, key=lambda q: T[q][0]):
        a, b = T[i]
        if spans and abs(spans[-1][1] - a) < 0.01:
            spans[-1][1] = b
        else:
            spans.append([a, b])
    for a, b in spans:
        if a < 0.1:      # frame one carries the title
            a = T["s01"][1]
            if a >= b:
                continue
        LAB_JS.append([f"#src{k}", round(a + 0.12, 2), round(b - 0.08, 2)])

NOCAP = [[T["s30"][0] + 0.15, 999]]   # the end card says the rest

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
FX = open("fx13.js").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%CHAPS%", "").replace("%LABJS%", json.dumps(LAB_JS)).replace("%CHAPJS%", "[]")
       .replace("%GEO%", "{}").replace("%PHONE%", "{}").replace("%LOGOS%", "{}")
       .replace("%CUTS%", json.dumps(CUTS)).replace("%NOCAP%", json.dumps(NOCAP))
       .replace("%WS%", json.dumps([x["start"] for x in W])).replace("%WE%", json.dumps([x["end"] for x in W]))
       .replace("%FXJS%", FX).replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
json.dump(dict(cuts=CUTS, labels=LAB_JS), open("work/cuts.json", "w"))
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(CUTS), "cuts")

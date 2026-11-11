"""Write index.html for Short #16 (9:16) from edl.py, words.json, captions.js, work/meta.json, work/fig/crops.json,
index_template.tpl and fx16.js.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, a page card over a moving blurred backdrop,
or my graphics over a backdrop (a blurred clip, or the dark blueprint grid drawn in CSS). Page cards carry their
highlight bars; the camera finds each highlighted line on its word (docCam in the template). Strips of the other pages,
logos and graphics are placed by fx16.js. Material that hasn't arrived shows as a NEEDED slate (previews only).
Usage: python3 make_index.py
"""
import json
import os

from PIL import Image

from edl import SHOTS, H, DUR, MAT, FIGS, W, have, wt

# captions are upper case; keep the lower-case s of "AIs" (make_captions.py writes "AIS")
_c = open("captions.js").read()
# and spell the numbers the voice says in words the same way as the others ("THREE HUNDRED AND FIFTY-EIGHT", "TEN")
for a, b in [('"d": "AIS"', '"d": "AI<span style=\'text-transform:none\'>s</span>"'), ('"d": "3", ', '"d": "THREE", '),
             ('"d": "9", ', '"d": "NINE", '), ('"d": "10", ', '"d": "TEN", '), ('"d": "30", ', '"d": "THIRTY", ')]:
    _c = _c.replace(a, b)
open("captions.js", "w").write(_c)
META = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
CROPS = json.load(open("work/fig/crops.json"))
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


def asset_size(name):
    return Image.open(f"assets/img/{name}.png").size


# highlight boxes in the asset image's pixels, one list of line boxes per phrase
def phrases(name):
    if name == "arith":   # the 1670 page: Fermat's note, and its last line ("this margin is too narrow")
        return [[[112, 798, 590, 36]], [[78, 904, 338, 30]]]
    c = CROPS.get(name)
    if not c:
        return []
    aw, _ = asset_size(name)
    f = aw / c["w"]
    out, cur = [], []
    for b in c["hl"]:
        if b is None:
            out.append(cur); cur = []
        else:
            cur.append([round(v * f) for v in b])
    return out


# page cards: shot -> (image, max width, max height, centre y, highlight times per phrase, zoom limit)
CARDS = {
    "s07": ("arith", 700, 900, 760, [wt(41), wt(46)], 2.2),
    "s13": ("r_hero", 900, 760, 690, [], 1.0),
    "s17": ("l_hero", 960, 400, 520, [], 1.0),
}
GEO = {}


def figcard(sid):
    name, maxw, maxh, cy, times, zmax = CARDS[sid]
    w, h = asset_size(name)
    s = min(maxw / w, maxh / h)
    cw, ch = round(w * s), round(h * s)
    left, top = round(540 - cw / 2), max(300, round(cy - ch / 2))
    hls, sweeps, cam = [], [], []
    for p, (boxes, t) in enumerate(zip(phrases(name), times)):
        if t is None:
            continue
        for j, (x, y, bw, bh) in enumerate(boxes):
            hid = f"hl-{sid}-{p}-{j}"
            hls.append(f'<div class="hl" id="{hid}" style="left:{round(x * s) - 4}px;top:{round(y * s) - 2}px;'
                       f'width:{round(bw * s) + 8}px;height:{round(bh * s) + 4}px"></div>')
            d = 0.25 + 0.012 * bw * s / 10
            sweeps.append([hid, round(t + j * 0.28, 2), round(min(0.6, d), 2)])
        xs = [b[0] for b in boxes]; xe = [b[0] + b[2] for b in boxes]; ys = [b[1] + b[3] / 2 for b in boxes]
        cam.append([round(t, 2), round(left + s * (min(xs) + max(xe)) / 2), round(top + s * sum(ys) / len(ys)),
                    round(s * (max(xe) - min(xs)))])
    if cam:
        GEO[sid] = {"hl": cam, "sweeps": sweeps, "zmax": zmax}
    return (f'<div class="card" id="card-{sid}" style="left:{left}px;top:{top}px;width:{cw}px;height:{ch}px">'
            f'<img src="assets/img/{name}.png" alt="" style="width:{cw}px" />{"".join(hls)}</div>')


blocks = []
for z, (sid, t0, t1, kind, sp) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:
        a, d, ms = 0.0, d + (t0 - H), H - t0
    need = [c for c in (sp.get("m"), sp.get("bd")) if c and not have(c)]
    ok = sid in META and not need
    clip = f"assets/clips/{sid}.mp4"
    back = (vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)) if sp.get("bd") else f'<div class="gridbg" id="grid-{sid}"></div>'
    if kind == "V":
        inner = vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)
    elif kind == "IMG":
        inner = back + figcard(sid)
    elif kind == "GFX":
        inner = back
    elif kind == "END":
        prev = ORDER[ORDER.index(sid) - 1]
        img = f"assets/img/{prev}_last.png"
        inner = (f'<div class="bd" style="background-image:url({img});filter:blur(30px) brightness(0.45)"></div>' if os.path.exists(img)
                 else '<div class="gridbg"></div>')
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}"><div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div></div></div>')

# ---------------------------------------------------------------- cuts: a transition on every cut, chosen by meaning
SPECIAL = {"s02": "cut", "s03": "zoom", "s04": "whip", "s05": "slideup", "s06": "zoom", "s07": "card", "s08": "whip",
           "s09": "dip", "s10": "zoom", "s11": "cut", "s12": "scratch", "s13": "slideup", "s14": "zoom", "s15": "cut", "s16": "whip",
           "s17": "slideup", "s18": "zoom", "s19": "cut", "s20": "slideup", "s21": "scratch", "s22": "cut", "s23": "whip", "s24": "cut",
           "s25": "zoom", "s26": "whip", "s27": "zoom", "s28": "zoom", "s29": "whip", "s30": "slideup",
           "s31": "whip", "s32": "slideup", "s33": "cut", "s34": "slideup", "s35": "zoom", "s36": "fade"}
CUTS = []
for i in range(len(ORDER) - 1):
    a, b = ORDER[i], ORDER[i + 1]
    k = SPECIAL.get(b, "whip")
    CUTS.append([a, b, k[0], k[1]] if isinstance(k, tuple) else [a, b, k])

# ---------------------------------------------------------------- source labels
LABEL = {}
for sid, kind, sp in ((s[0], s[3], s[4]) for s in SHOTS):
    if kind == "V":
        LABEL[sid] = MAT[sp["m"]][2]
    elif kind == "IMG":
        LABEL[sid] = FIGS[CARDS[sid][0]][1]
    elif kind == "GFX":
        LABEL[sid] = "ILLUSTRATION"
PAGE_E, PAGE_R = "ILLUSTRATION + REAL PAGE · CLAUDE.DEV", "ILLUSTRATION + REAL PAGE · ANTHROPIC"
LABEL.update({"s30": PAGE_E, "s32": "QUOTED · ANTHROPIC · CLAUDE.DEV, 9 NOV 2026", "s08": PAGE_R, "s09": "ILLUSTRATION", "s10": "REAL CODE · GITHUB, ANTHROPICS/FERMATS-LAST-THEOREM",
              "s11": "REAL CODE · GITHUB, ANTHROPICS/FERMATS-LAST-THEOREM", "s14": PAGE_R, "s23": PAGE_E, "s24": PAGE_E,
              "s25": "QUOTED · THE BOSS AI · CLAUDE.DEV, 9 NOV 2026", "s28": PAGE_E, "s33": PAGE_E})
groups = {}
for sid in ORDER:
    if LABEL.get(sid):
        groups.setdefault(LABEL[sid], []).append(sid)
LAB_JS, lab_html = [], []
for k, (txt, ids) in enumerate(groups.items()):
    cls = " q" if txt.startswith(("ILLUSTRATION", "QUOTED")) else " st" if txt.startswith("STOCK") else ""
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
            continue
        LAB_JS.append([f"#src{k}", round(a + 0.12, 2), round(b - 0.08, 2)])

NOCAP = [[T["s36"][0] + 0.15, 999]]   # the end card says the rest

# strips of the real pages placed by fx16.js: asset size and highlight boxes (asset pixels)
STRIPS = {}
for name in CROPS:
    if os.path.exists(f"assets/img/{name}.png"):
        w, h = asset_size(name)
        STRIPS[name] = {"w": w, "h": h, "hl": phrases(name), "src": FIGS[name][1].replace("REAL · ", "")}

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
FX = open("fx16.js").read()
LOGOSVG = {f[:-4]: open("assets/logos/" + f).read() for f in os.listdir("assets/logos") if f.endswith(".svg")}
FX = FX.replace("__LOGOSVG__", json.dumps(LOGOSVG))
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%CHAPS%", "").replace("%LABJS%", json.dumps(LAB_JS)).replace("%CHAPJS%", "[]")
       .replace("%GEO%", json.dumps(GEO)).replace("%PHONE%", "{}").replace("%LOGOS%", json.dumps(STRIPS))
       .replace("%CUTS%", json.dumps(CUTS)).replace("%NOCAP%", json.dumps(NOCAP))
       .replace("%WS%", json.dumps([x["start"] for x in W])).replace("%WE%", json.dumps([x["end"] for x in W]))
       .replace("%FXJS%", FX).replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
json.dump(dict(cuts=CUTS, labels=LAB_JS), open("work/cuts.json", "w"))
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(CUTS), "cuts")

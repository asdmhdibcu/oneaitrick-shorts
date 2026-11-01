"""Write index.html for Short #15 (9:16) from edl.py, words.json, captions.js, work/meta.json, index_template.tpl and
fx15.js.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, or a paper still / my graphics over a moving
blurred backdrop clip. The S-1 excerpt cards and logos are placed by fx15.js. Material that hasn't arrived shows as a NEEDED slate (previews only; never delivered).
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


def figcard(sid, name, maxw=960, maxh=780, cy=640):
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
    elif kind == "STILL":
        inner = vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)
    elif kind == "CARDV":
        cw, ch = 740, round(740 * 496 / 490)
        inner = (vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)) + (
            f'<div class="card" id="card-{sid}" style="left:{540 - cw // 2}px;top:330px;width:{cw}px;height:{ch}px">'
            f'<video id="vc-{sid}" class="vid" src="assets/clips/{sid}_card.mp4" muted playsinline data-start="{a:.3f}" '
            f'data-duration="{min(d, DUR - a):.3f}" data-media-start="{ms:.3f}" style="left:0;top:0;width:{cw}px;height:{ch}px;object-fit:cover"></video></div>')
    elif kind == "GFX":
        inner = vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)
    elif kind == "END":
        prev = ORDER[ORDER.index(sid) - 1]
        img = f"assets/img/{prev}_last.png"
        inner = f'<div class="bd" style="background-image:url({img});filter:blur(30px) brightness(0.45)"></div>' if os.path.exists(img) else ""
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}"><div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div></div></div>')

# ---------------------------------------------------------------- cuts: a transition on every cut
SPECIAL = {"s02": "flash", "s03": "slideup", "s04": "card", "s05": "whip", "s06": "zoom", "s07": "zoom", "s07b": "whip",
           "s08": "flash", "s09": "zoom", "s10": "slideup", "s11": "flash", "s12": "card", "s13": "scratch", "s14": "cut",
           "s15": "whip", "s16": "cut", "s17": "slideup", "s18": "cut", "s19": "flash", "s20": "whip", "s21": "zoom", "s22": "slideup",
           "s23": "fade", "s24": "scratch", "s25": "cut", "s26": "whip", "s27": "whip", "s28": "dip", "s29": "zoom", "s30": "zoom",
           "s31": "dip", "s32": "slideup", "s33": "cut", "s34": "flash", "s35": "cut", "s36": "flash", "s37": "zoom", "s38": "card",
           "s39": "whip", "s40": "slideup", "s41": "dip", "s42": "cut", "s43": "cut", "s44": "slideup", "s45": "dip", "s46": "whip",
           "s46b": "zoom", "s47": "flash", "s48": "fade"}
CUTS = []
for i in range(len(ORDER) - 1):
    a, b = ORDER[i], ORDER[i + 1]
    k = SPECIAL.get(b) or ("whip", "slideup", "zoom", "whip", "slideup")[i % 5]
    CUTS.append([a, b, k])

# ---------------------------------------------------------------- source labels
LABEL = {}
for sid, kind, sp in ((s[0], s[3], s[4]) for s in SHOTS):
    if kind in ("V", "CARDV"):
        LABEL[sid] = MAT[sp["m"]][2]
    elif kind == "STILL":
        LABEL[sid] = FIGS[sp["img"]][1]
    elif kind == "IMG":
        LABEL[sid] = FIGS[sp["img"]][1]
LABEL.update({"s02": "ILLUSTRATION", "s03": "ILLUSTRATION", "s06": "LOGO · PLANET", "s08": "ILLUSTRATION",
              "s09": "ILLUSTRATION · MY GLOBE", "s10": "ILLUSTRATION", "s21": "ILLUSTRATION · MY GLOBE", "s22": "ILLUSTRATION",
              "s28": "ILLUSTRATION", "s29": "ILLUSTRATION", "s33": "ILLUSTRATION", "s34": "ILLUSTRATION", "s35": "ILLUSTRATION",
              "s36": "ILLUSTRATION", "s37": "ILLUSTRATION", "s39": "ILLUSTRATION", "s40": "ILLUSTRATION", "s42": "ILLUSTRATION",
              "s44": "QUOTED · NPR, 2 OCT 2026", "s45": "ILLUSTRATION"})
groups = {}
for sid in ORDER:
    if LABEL.get(sid):
        groups.setdefault(LABEL[sid], []).append(sid)
LAB_JS, lab_html = [], []
for k, (txt, ids) in enumerate(groups.items()):
    cls = " gen" if txt.startswith("AI ") else " q" if txt.startswith(("ILLUSTRATION", "LOGO")) else " st" if txt.startswith("STOCK") else " q" if txt.startswith("QUOTED") else ""
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

NOCAP = [[T["s48"][0] + 0.15, 999]]   # the end card says the rest

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
FX = open("fx15.js").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%CHAPS%", "").replace("%LABJS%", json.dumps(LAB_JS)).replace("%CHAPJS%", "[]")
       .replace("%GEO%", "{}").replace("%PHONE%", "{}").replace("%LOGOS%", "{}")
       .replace("%CUTS%", json.dumps(CUTS)).replace("%NOCAP%", json.dumps(NOCAP))
       .replace("%WS%", json.dumps([x["start"] for x in W])).replace("%WE%", json.dumps([x["end"] for x in W]))
       .replace("%FXJS%", FX).replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
json.dump(dict(cuts=CUTS, labels=LAB_JS), open("work/cuts.json", "w"))
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(CUTS), "cuts")

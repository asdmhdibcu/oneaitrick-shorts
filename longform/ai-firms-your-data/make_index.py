"""Write index.html for the #11 video (16:9) from edl.py, words.json, assets/pages/pages.json, work/meta.json, the logos,
index_template.tpl and fx_shots.js.

Every shot is .shot > .fx (transitions, punch-ins) > .cam (camera) > footage, a page card or a phone over a moving,
blurred backdrop clip. Material that hasn't arrived shows as a NEEDED slate (previews only; never delivered).
Usage: python3 make_index.py
"""
import json
import os
import re

from edl import SHOTS, H, DUR, W, MAT, HL, CHAPTERS, have, wt

PAGES = json.load(open("assets/pages/pages.json"))
META = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
LG = json.load(open("assets/logos/logos.json"))
T = {s[0]: (s[1], s[2]) for s in SHOTS}
KIND = {s[0]: s[3] for s in SHOTS}
SPEC = {s[0]: s[4] for s in SHOTS}
ORDER = [s[0] for s in SHOTS]
GEO, PHONE = {}, {}

# ---------------------------------------------------------------- page cards
ZMAX = {"r_cover": 1.15}
def card(sid, pg, maxw=1240, maxh=700, cx=880, cy=470, sweep_at=None):
    m = PAGES[pg]
    s = min(maxw / m["w"], maxh / m["h"])
    w, h = round(m["w"] * s), round(m["h"] * s)
    left, top = round(cx - w / 2), max(96, round(cy - h / 2))
    inner = f'<img src="assets/pages/{pg}.png" alt="" style="width:{w}px" />'
    sweeps, hls = [], []
    times = sweep_at if sweep_at is not None else [wt(k) for k in HL.get(sid, [])]
    for g, idxs in enumerate(m["groups"]):
        if g >= len(times):
            break
        t = times[g]; tot = sum(m["boxes"][i][2] for i in idxs); acc = 0.0
        for i in idxs:
            x, y, bw, bh = m["boxes"][i]
            hid = f"hl-{sid}-{i}"
            inner += f'<div class="hl" id="{hid}" style="left:{x * s:.0f}px;top:{y * s:.0f}px;width:{bw * s:.0f}px;height:{bh * s:.0f}px"></div>'
            d = 0.5 * bw / max(tot, 1) + 0.08
            sweeps.append([hid, round(t + acc, 3), round(d, 3)]); acc += d
        bx = [m["boxes"][i] for i in idxs]
        x0 = min(b[0] for b in bx); x1 = max(b[0] + b[2] for b in bx); y0 = min(b[1] for b in bx); y1 = max(b[1] + b[3] for b in bx)
        hls.append([round(t, 3), round(left + (x0 + x1) / 2 * s, 1), round(top + (y0 + y1) / 2 * s, 1), round((x1 - x0) * s, 1)])
    GEO[sid] = dict(left=left, top=top, w=w, h=h, s=round(s, 4), hl=hls, sweeps=sweeps, zmax=ZMAX.get(pg, 1.6))
    return f'<div class="card" id="card-{sid}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">{inner}</div>'


def vid(src, vid_id, t0, d, ms=0.0, style="left:0;top:0;width:1920px;height:1080px", cls="vid"):
    d = min(d, DUR - t0)
    return (f'<video id="{vid_id}" class="{cls}" src="{src}" muted playsinline data-start="{t0:.3f}" data-duration="{d:.3f}" '
            f'data-media-start="{ms:.3f}" style="{style}"></video>')


def slate(codes):
    what = " · ".join(f"{c} · {MAT[c][1]}" for c in codes)
    return f'<div class="slate"><div class="st">NEEDED</div><div class="sd">{what}</div></div>'


# phone toggles / targets in the conformed source clip's pixels: (x, y, ring w, ring h)
TOG = {"R1": (1130, 421, 210, 120), "R2": (1127, 985, 190, 110), "R3": (280, 1002, 370, 140)}
TOG_SHOT = {"v51": (192, 472, 240, 240)}     # the ChatGPT icon in the folder (frame one of R1)
PH_DISP = 0.82                                # a phone screen is conformed 1000 px tall and shown 880 px tall
SRCH = {"R1": 2620, "R2": 2120, "R3": 2410}

blocks = []
prev_page = None
for z, (sid, t0, t1, kind, sp) in enumerate(SHOTS):
    a, d, ms = t0 - H, (t1 - t0) + 2 * H, 0.0
    if a < 0:
        a, d, ms = 0.0, d + (t0 - H), H - t0
    need = [c for c in (sp.get("m"), sp.get("bd")) if c and not have(c)]
    ok = sid in META and not need
    clip = f"assets/clips/{sid}.mp4"
    if kind == "V":
        inner = vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)
    elif kind == "PAGE":
        inner = (vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)) + card(sid, sp["pg"])
        prev_page = (sid, sp["pg"])
    elif kind == "GFX":
        inner = vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)
    elif kind == "PHONE":
        if ok:
            pw = META[sid]["pw"]; dw, dh = round(pw * PH_DISP), round(1000 * PH_DISP)
            left, top = round(640 - dw / 2), 84
            inner = vid(clip, f"v-{sid}", a, d, ms) + (f'<div class="phone" style="left:{left}px;top:{top}px;width:{dw}px;height:{dh}px">'
                     + vid(f"assets/clips/{sid}_ph.mp4", f"p-{sid}", a, d, ms, style=f"left:0;top:0;width:{dw}px;height:{dh}px", cls="") + "</div>")
            k = PH_DISP * 1000 / SRCH[sp["m"]]
            tx, ty, rw, rh = TOG_SHOT.get(sid, TOG[sp["m"]])
            PHONE[sid] = dict(left=left, top=top, w=dw, h=dh, tog=[round(left + tx * k), round(top + ty * k), round(rw * k), round(rh * k)])
        else:
            inner = slate(need)
    elif kind == "FREEZE":   # the previous page, frozen: its backdrop's last frame and the same card, then the colour drains
        ps, pg = prev_page
        inner = f'<div class="bd" style="background-image:url(assets/img/{ps}_last.png)"></div>' + card(sid, pg, sweep_at=[0] * 4)
    elif kind == "END":
        prev = ORDER[ORDER.index(sid) - 1]
        img = f"assets/img/{prev}_last.png"
        inner = f'<div class="bd" style="background-image:url({img});filter:blur(30px) brightness(0.45)"></div>' if os.path.exists(img) else ""
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}"><div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div></div></div>')

# the call-for-evidence page behind Nevinson's quote (v49)
m3 = PAGES["p3_dates"]; s3 = 760 / m3["h"]
GEO["v49b"] = dict(left=round(1210 - m3["w"] * s3 / 2), top=150, w=round(m3["w"] * s3), h=760, s=s3, hl=[], sweeps=[])
FREEZE_GEO = {k: v for k, v in GEO.items() if KIND.get(k) == "FREEZE"}
for k in FREEZE_GEO:
    GEO[k]["sweeps"] = [[h, round(T[k][0] - 0.3, 3), 0.01] for h, _, _ in GEO[k]["sweeps"]]

# ---------------------------------------------------------------- cuts
CUTS = []
chap_first = {c[0] for c in CHAPTERS}
for i in range(len(ORDER) - 1):
    a, b = ORDER[i], ORDER[i + 1]
    kb = KIND[b]
    if kb == "END":
        k = "fade"
    elif kb == "FREEZE":
        k = "scratch"
    elif b in chap_first:
        k = "dip"
    elif kb in ("PAGE", "PHONE"):
        k = "card"
    elif kb == "GFX":
        k = "zoom"
    elif b in ("v25", "v26", "v27"):
        k = "cut"
    elif KIND[a] == "FREEZE":
        k = "flash"
    else:
        k = ("whip", "slideup", "whip", "zoom")[i % 4]
    CUTS.append([a, b, k])

# ---------------------------------------------------------------- source labels
LABEL = {}
for sid, kind, sp in ((s[0], s[3], s[4]) for s in SHOTS):
    if kind in ("V", "PHONE"):
        LABEL[sid] = MAT[sp["m"]][2]
    elif kind in ("PAGE", "FREEZE"):
        pg = sp.get("pg") or ""
        LABEL[sid] = ("REAL · ICO REPORT, 8 OCT 2026" if pg.startswith("r_") else "REAL · ICO NEWS RELEASE, 8 OCT 2026" if pg.startswith("p2") else
                      "REAL · META, HOW META USES INFORMATION FOR AI" if pg.startswith("p5") else "REAL · OPENAI HELP CENTER" if pg.startswith("p4") else
                      "REAL · ICO CALL FOR EVIDENCE" if pg.startswith("p3") else "REAL")
LABEL["v36"] = LABEL.get("v35", "")
LABEL.update({"v15": "LOGOS · THE ICO'S PRIORITY LIST", "v19b": "QUOTED · ICO REPORT, P.14", "v30": "LOGOS · NAMED BY THE ICO",
              "v32": "LOGOS · NAMED BY THE ICO", "v43": "LOGOS · NAMED BY THE ICO", "v49": "QUOTED · ICO NEWS RELEASE, 8 OCT 2026"})
groups = {}
for sid in ORDER:
    if sid in LABEL and LABEL[sid]:
        groups.setdefault(LABEL[sid], []).append(sid)
LAB_JS, lab_html = [], []
for k, (txt, ids) in enumerate(groups.items()):
    cls = " gen" if txt.startswith("AI ") else " st" if txt.startswith("STOCK") else " q" if txt.startswith(("QUOTED", "LOGOS", "DEMO", "SCREEN")) else ""
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
            a = T["v01"][1]
            if a >= b:
                continue
        LAB_JS.append([f"#src{k}", round(a + 0.12, 2), round(b - 0.08, 2)])

# chapters (as in the YouTube description)
chap_html, CHAP_JS = [], []
for j, (sid, n, title) in enumerate(CHAPTERS):
    chap_html.append(f'<div class="chap" id="ch{j}"><span class="n">{n}</span><span class="t">{title}</span></div>')
    CHAP_JS.append([f"#ch{j}", round(T[sid][0] + 0.15, 2), round(min(T[sid][0] + 2.6, T[sid][1] + 1.2), 2)])

# ---------------------------------------------------------------- captions: sentence case, karaoke chunks
EMPH = {41, 210, 377, 192, 128, 176, 177, 499}           # YOU, WORSE, OUT, maze, eleven, "benefiting humanity", Three


def disp(t):
    t = t.replace("...", "…")
    core = re.sub(r"[^A-Za-z]", "", t)
    if len(core) > 1 and core.isupper() and core not in ("AI", "UK", "ICO", "OUT"):
        t = t.lower()
    if core == "OUT":
        t = t.lower()
    return t


CAPS, cur = [], []
for i, x in enumerate(W):
    d = disp(x["text"])
    cur.append(dict(d=d, s=round(x["start"], 3), e=round(x["end"], 3), em=i in EMPH))
    nxt = W[i + 1] if i + 1 < len(W) else None
    chars = sum(len(c["d"]) + 1 for c in cur)
    end_sent = d.endswith((".", "?", "!", "…", '."', '".', "?\"", '”'))
    brk = (nxt is None or end_sent or (d.endswith(",") and len(cur) >= 3) or len(cur) >= 7
           or chars + len(disp(nxt["text"])) > 44 or (nxt["start"] - x["end"] > 0.45))
    if brk:
        CAPS.append(dict(t0=round(cur[0]["s"] - 0.05, 3), w=cur)); cur = []
for i, c in enumerate(CAPS):
    last = c["w"][-1]["e"]
    nxt = CAPS[i + 1]["t0"] if i + 1 < len(CAPS) else DUR
    c["t1"] = round(min(nxt - 0.02, last + 0.7), 3)
NOCAP = [[0.0, 0.0], [T["v60"][0] + 0.6, 999]]   # the end card says the rest

# ---------------------------------------------------------------- logos
LOGOS = {c: dict(name=LG[c]["name"], have=True, bg=LG[c]["bg"]) for c in LG}
for c, n in (("L3", "ChatGPT"), ("L4", "Meta"), ("L6", "Gemini"), ("L15", "xAI")):
    LOGOS.setdefault(c, dict(name=n, have=False, bg=None))

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
FX = open("fx_shots.js").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%CHAPS%", "\n        ".join(chap_html)).replace("%LABJS%", json.dumps(LAB_JS)).replace("%CHAPJS%", json.dumps(CHAP_JS))
       .replace("%GEO%", json.dumps(GEO)).replace("%PHONE%", json.dumps(PHONE)).replace("%LOGOS%", json.dumps(LOGOS))
       .replace("%CUTS%", json.dumps(CUTS)).replace("%CAPS%", json.dumps(CAPS)).replace("%NOCAP%", json.dumps(NOCAP))
       .replace("%WS%", json.dumps([x["start"] for x in W])).replace("%WE%", json.dumps([x["end"] for x in W]))
       .replace("%FXJS%", FX).replace("%DUR%", str(DUR)).replace("%H%", str(H)))
open("index.html", "w").write(out)
json.dump(dict(cuts=CUTS, labels=LAB_JS), open("work/cuts.json", "w"))
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(CAPS), "caption chunks,", sum(len(g["sweeps"]) for g in GEO.values()), "highlight strips")

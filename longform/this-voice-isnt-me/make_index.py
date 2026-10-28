"""Write index.html for the #12 video (16:9) from edl.py, words.json, assets/pages/pages.json, work/meta.json, the logos,
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
ORDER = [s[0] for s in SHOTS]
GEO, PHONE = {}, {}

# ---------------------------------------------------------------- page cards
ZMAX = {"ad_frame": 1.25, "e_tts": 1.35, "c_head": 1.2, "u_arup": 1.25, "r_head": 1.3, "o_title": 1.3, "t_head": 1.3}


def card(sid, pg, maxw=1240, maxh=700, cx=880, cy=470):
    m = PAGES[pg]
    s = min(maxw / m["w"], maxh / m["h"])
    w, h = round(m["w"] * s), round(m["h"] * s)
    left, top = round(cx - w / 2), max(96, round(cy - h / 2))
    inner = f'<img src="assets/pages/{pg}.png" alt="" style="width:{w}px" />'
    sweeps, hls = [], []
    times = [wt(k) for k in HL.get(sid, [])]
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


# phone targets in the conformed source clip's pixels: (x, y, ring w, ring h)
TOG = {"R2": (1130, 421, 210, 120), "R3": (600, 2060, 560, 150)}
PH_DISP = 0.82
SRCH = {"R2": 2620, "R3": 2868}

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
    elif kind == "PAGE":
        inner = (vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)) + card(sid, sp["pg"])
    elif kind == "GFX":
        inner = vid(clip, f"v-{sid}", a, d, ms) if ok else slate(need)
    elif kind == "PHONE":
        if ok:
            pw = META[sid]["pw"]; dw, dh = round(pw * PH_DISP), round(1000 * PH_DISP)
            left, top = round(640 - dw / 2), 84
            inner = vid(clip, f"v-{sid}", a, d, ms) + (f'<div class="phone" style="left:{left}px;top:{top}px;width:{dw}px;height:{dh}px">'
                     + vid(f"assets/clips/{sid}_ph.mp4", f"p-{sid}", a, d, ms, style=f"left:0;top:0;width:{dw}px;height:{dh}px", cls="") + "</div>")
            k = PH_DISP * 1000 / SRCH[sp["m"]]
            tx, ty, rw, rh = TOG[sp["m"]]
            PHONE[sid] = dict(left=left, top=top, w=dw, h=dh, tog=[round(left + tx * k), round(top + ty * k), round(rw * k), round(rh * k)])
        else:
            inner = slate(need)
    elif kind == "END":
        prev = ORDER[ORDER.index(sid) - 1]
        img = f"assets/img/{prev}_last.png"
        inner = f'<div class="bd" style="background-image:url({img});filter:blur(30px) brightness(0.45)"></div>' if os.path.exists(img) else ""
    blocks.append(f'      <div class="shot" id="sh-{sid}" style="z-index:{z + 1}"><div class="fx" id="fx-{sid}"><div class="cam" id="cam-{sid}">{inner}</div></div></div>')

# ---------------------------------------------------------------- cuts
CUTS = []
chap_first = {c[0] for c in CHAPTERS}
QUICK = {"v06", "v07", "v60", "v61"}
for i in range(len(ORDER) - 1):
    a, b = ORDER[i], ORDER[i + 1]
    kb = KIND[b]
    if kb == "END":
        k = "fade"
    elif b in chap_first:
        k = "dip"
    elif b in QUICK:
        k = "cut"
    elif kb in ("PAGE", "PHONE"):
        k = "card"
    elif kb == "GFX":
        k = "zoom"
    else:
        k = ("whip", "slideup", "whip", "zoom")[i % 4]
    CUTS.append([a, b, k])

# ---------------------------------------------------------------- source labels
PG_LABEL = {"o_": "REAL · OPENAI, 24 MAR 2023", "f_": "REAL · FORBES, 2 MAY 2023", "a_": "REAL · REUTERS, 10 OCT 2018",
            "i_": "REAL · ICO GUIDANCE", "r_": "REAL · REUTERS FACT CHECK, 22 MAY 2023", "s_": "REAL · STARLING BANK, 18 SEPT 2024",
            "t_": "REAL · FTC CONSUMER ALERT, 20 MAR 2023", "c_": "REAL · CNN, 4 FEB 2024", "u_": "REAL · CNN, 16 MAY 2024",
            "e_": "SCREEN RECORDING · ELEVENLABS", "ad": "REAL · RNC AD ON YOUTUBE, 25 APR 2023"}
LABEL = {}
for sid, kind, sp in ((s[0], s[3], s[4]) for s in SHOTS):
    if kind in ("V", "PHONE"):
        LABEL[sid] = MAT[sp["m"]][2]
    elif kind == "PAGE":
        LABEL[sid] = PG_LABEL[sp["pg"][:2]]
LABEL.update({"v69": "QUOTED · HIGH COURT JUDGMENT, 6 JUNE 2025", "v68": "THE HIGH COURT JUDGMENT, 6 JUNE 2025", "v43": "STOCK · PEXELS"})
groups = {}
for sid in ORDER:
    if sid in LABEL and LABEL[sid]:
        groups.setdefault(LABEL[sid], []).append(sid)
LAB_JS, lab_html = [], []
for k, (txt, ids) in enumerate(groups.items()):
    cls = " gen" if txt.startswith("AI ") else " st" if txt.startswith("STOCK") else " q" if txt.startswith(("QUOTED", "THE HIGH", "SCREEN")) else ""
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

# ---------------------------------------------------------------- captions: sentence case, karaoke chunks
EMPH = {10, 265, 483, 641, 781, 744, 1001}      # IS, OTHER, NEW, ENTIRELY, NOW, three (seconds), Eighteen
KEEP = {"AI", "UK", "US", "AI.", "AI,"}


def disp(t):
    t = t.replace("...", "…")
    core = re.sub(r"[^A-Za-z]", "", t)
    if len(core) > 1 and core.isupper() and core not in ("AI", "UK", "US", "CVs"):
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
END_ID = ORDER[-1]
NOCAP = [[0.0, 0.0], [T[END_ID][0] + 0.6, 999]]   # the end card says the rest

# ---------------------------------------------------------------- logos
LOGOS = {c: dict(name=LG[c]["name"], have=True, bg=LG[c]["bg"]) for c in LG}

shots_js = json.dumps([{"id": s[0], "t0": s[1], "t1": s[2], "k": s[3]} for s in SHOTS])
HTML = open("index_template.tpl").read()
FX = open("fx_shots.js").read()
out = (HTML.replace("%SHOTS%", "\n".join(blocks)).replace("%SHOTSJS%", shots_js).replace("%LABELS%", "\n        ".join(lab_html))
       .replace("%LABJS%", json.dumps(LAB_JS)).replace("%GEO%", json.dumps(GEO)).replace("%PHONE%", json.dumps(PHONE))
       .replace("%LOGOS%", json.dumps(LOGOS)).replace("%CUTS%", json.dumps(CUTS)).replace("%CAPS%", json.dumps(CAPS))
       .replace("%NOCAP%", json.dumps(NOCAP)).replace("%WS%", json.dumps([x["start"] for x in W]))
       .replace("%WE%", json.dumps([x["end"] for x in W])).replace("%FXJS%", FX).replace("%DUR%", str(DUR)).replace("%H%", str(H))
       .replace("%ENDID%", END_ID))
open("index.html", "w").write(out)
json.dump(dict(cuts=CUTS, labels=LAB_JS), open("work/cuts.json", "w"))
print("index.html", len(out), "bytes,", len(blocks), "shots,", len(CAPS), "caption chunks,", sum(len(g["sweeps"]) for g in GEO.values()), "highlight strips")

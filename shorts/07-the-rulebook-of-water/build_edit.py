"""Short #7: cut, retime, crop and conform every shot for the HyperFrames composition (edl.py).

Inputs (git-ignored): work/raw/* (Pexels clips, NASA video, the creator's phone recordings), work/img/* (screenshots,
portraits), work/pdf/*.png (PDF pages at 300 dpi), work/pages/*.png (stitch_page.py), work/sim/*.mp4 (fluid.py,
particles.py). Outputs: assets/clips/<id>.mp4 (1080x1920, 30 fps, silent), assets/img/*, work/meta.json (card sizes).

Usage: python3 build_edit.py            (all)
       python3 build_edit.py s07 s21    (only those shots)
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageFilter

from edl import SHOTS, H

Image.MAX_IMAGE_PIXELS = None
GRADE = "eq=contrast=1.04:saturation=1.06"
os.makedirs("assets/clips", exist_ok=True)
os.makedirs("assets/img", exist_ok=True)
os.makedirs("work/tmp", exist_ok=True)
T = {s[0]: (s[1], s[2]) for s in SHOTS}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)); print(r.stderr[-2500:]); sys.exit(1)
    return r


def probe(src):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src])
    w, h = r.stdout.strip().split(",")[:2]
    return int(w), int(h)


def enc(out):
    return ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", out]


def geo(src, mode, cx, W=1080, Hh=1920):
    """Filter chain from the source frame to W x Hh."""
    w, h = probe(src)
    if mode in ("native", "sim"):
        return f"scale={W}:{Hh}:flags=lanczos"
    if mode == "vert":  # vertical source: fit the width, crop the height around the centre
        return f"scale={W}:-2:flags=lanczos,crop={W}:{Hh}:0:(ih-{Hh})/2"
    if mode == "fill":
        cw = round(h * W / Hh / 2) * 2
        x = round(min(max(cx * w - cw / 2, 0), w - cw))
        return f"crop={cw}:{h}:{x}:0,scale={W}:{Hh}:flags=lanczos"
    # tall: 3:4 window at the top over its own blurred fill; the seam fades out
    cw = round(h * 3 / 4 / 2) * 2
    x = round(min(max(cx * w - cw / 2, 0), w - cw))
    fw = round(h * 9 / 16 / 2) * 2
    fx = round(min(max(cx * w - fw / 2, 0), w - fw))
    return (f"split[a][b];[a]crop={fw}:{h}:{fx}:0,scale=540:960,gblur=sigma=18,scale=1080:1920,eq=brightness=-0.06:saturation=0.9[bg];"
            f"[b]crop={cw}:{h}:{x}:0,scale=1080:1440:flags=lanczos,format=rgba[fg0];[1:v]format=gray[m];[fg0][m]alphamerge[fg];"
            f"[bg][fg]overlay=0:0,format=yuv420p")


def mask():
    p = "work/tmp/tallmask.png"
    if not os.path.exists(p):
        m = Image.new("L", (1080, 1440), 255)
        for y in range(1220, 1440):
            m.paste(int(255 * (1440 - y) / 220), (0, y, 1080, y + 1))
        m.save(p)
    return ["-loop", "1", "-i", p]


def conform(src, sin, span, out, mode="fill", cx=0.5, rate=1.0, rev=False, W=1080, Hh=1920, grade=True):
    """span seconds of output starting H before the out start (source in-point sin sits at out start)."""
    ss = max(0.0, sin - H * rate)
    timing = f"setpts=(PTS-STARTPTS)/{rate:.4f}"
    if rate < 0.97:
        timing += ",minterpolate=fps=30:mi_mode=blend"
    g = geo(src, mode, cx, W, Hh)
    chain = f"{timing},{g}" + (f",{GRADE}" if grade else "") + ",fps=30" + (",reverse" if rev else "") + ",format=yuv420p"
    extra = mask() if mode == "tall" else []
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{span * rate + 0.15:.3f}", "-i", src] + extra +
        ["-filter_complex", chain, "-t", f"{span:.3f}"] + enc(out))


def ramp(sid, sp, span):
    """Piecewise speed: [(out offset from the out start, rate), ...]; each piece conformed and joined."""
    pieces, src_t = [], sp["sin"] - H * sp["ramp"][0][1]
    bounds = [(-H, sp["ramp"][0][1])] + [(o, r) for o, r in sp["ramp"][1:]]
    for k, (o, r) in enumerate(bounds):
        o_end = bounds[k + 1][0] if k + 1 < len(bounds) else span - H
        dur = o_end - o
        p = f"work/tmp/{sid}_r{k}.mp4"
        conform(sp["src"], src_t + H * r, dur, p, sp.get("mode", "fill"), sp.get("cx", 0.5), r)
        pieces.append(p)
        src_t += dur * r
    lst = f"work/tmp/{sid}_list.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in pieces))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst] + enc(f"assets/clips/{sid}.mp4"))


def last_frame(sid):
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         "-vf", "scale=540:960", f"assets/img/{sid}_last.png"])


def still(sid, at):
    """Frame of a conformed shot at out time `at`, full size."""
    t0 = T[sid][0]
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at - (t0 - H):.3f}", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         f"assets/img/{sid}_freeze.png"])


def footage(sid, t0, t1, sp):
    span = t1 - t0 + 2 * H
    if "ramp" in sp:
        ramp(sid, sp, span)
    elif sp.get("rev"):
        # backwards: take the source window that ends at sin and reverse it
        conform(sp["src"], sp["sin"] - span * sp.get("rate", 1.0) + H, span, f"assets/clips/{sid}.mp4", sp.get("mode", "fill"),
                sp.get("cx", 0.5), sp.get("rate", 1.0), rev=True)
    else:
        conform(sp["src"], sp["sin"], span, f"assets/clips/{sid}.mp4", sp.get("mode", "fill"), sp.get("cx", 0.5), sp.get("rate", 1.0))
    if "blend" in sp:
        b = sp["blend"]
        conform(b["src"], b["sin"], span, f"assets/clips/{sid}_b.mp4", "sim", grade=False)
    if "freeze" in sp:
        still(sid, sp["freeze"])
    last_frame(sid)


def frame_of(src, at, mode, cx, out):
    g = geo(src, mode, cx)
    extra = mask() if mode == "tall" else []
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", src] + extra + ["-filter_complex", f"{g},{GRADE}", "-frames:v", "1", out])


def backdrop(sid, bd):
    out = f"assets/img/{sid}_bd.jpg"
    if bd[0] == "last":
        im = Image.open(f"assets/img/{bd[1]}_last.png")
    else:
        w, _ = probe(bd[0])
        frame_of(bd[0], bd[1], "fill", 0.5, "work/tmp/bd.png")
        im = Image.open("work/tmp/bd.png")
    im = im.convert("RGB").resize((540, 960)).filter(ImageFilter.GaussianBlur(14))
    im.save(out, quality=88)


def save_crop(sid, im):
    im.save(f"assets/img/{sid}.png", optimize=True)
    return {"pw": im.size[0], "ph": im.size[1]}


meta = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
only = set(sys.argv[1:])
for sid, t0, t1, kind, sp in SHOTS:
    if only and sid not in only:
        continue
    print(sid, kind, flush=True)
    span = t1 - t0 + 2 * H
    if kind in ("V", "CUT"):
        footage(sid, t0, t1, sp)
    elif kind == "SIM":
        conform(sp["src"], sp["sin"], span, f"assets/clips/{sid}.mp4", "sim", grade=False)
        last_frame(sid)
    elif kind == "SPLIT":
        for part in ("top", "bot"):
            p = sp[part]
            conform(p["src"], p["sin"], span, f"assets/clips/{sid}_{part}.mp4", "fill", p.get("cx", 0.5), W=1080, Hh=960)
        run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}_bot.mp4", "-frames:v", "1",
             "-vf", "scale=540:-2,pad=540:960:0:(oh-ih)/2", f"assets/img/{sid}_last.png"])
    elif kind == "FREEZE":
        of = sp["of"]
        still(of, t0)
        Image.open(f"assets/img/{of}_freeze.png").save(f"assets/img/{sid}.png")
        Image.open(f"assets/img/{sid}.png").resize((540, 960)).save(f"assets/img/{sid}_last.png")
    elif kind == "PAGE":
        pg = Image.open(f"work/pages/{sp['page']}.png")
        meta[sid] = save_crop(sid, pg.crop((sp.get("x0", 0), sp["y0"], sp.get("x1", pg.size[0]), sp["y1"])))
    elif kind == "PDF":
        x, y, w, h = sp["box"]
        pg = Image.open(f"work/pdf/{sp['doc']}-{sp['page']}.png").convert("RGB")
        meta[sid] = save_crop(sid, pg.crop((x, y, x + w, y + h)))
    elif kind == "PAIR":
        m = {}
        for part in ("a", "b"):
            src = sp[part]
            if src[0] == "pdf":
                x, y, w, h = src[3]
                im = Image.open(f"work/pdf/{src[1]}-{src[2]}.png").convert("RGB").crop((x, y, x + w, y + h))
            else:
                x, y, w, h = src[2]
                im = Image.open(f"work/pages/{src[1]}.png").convert("RGB").crop((x, y, x + w, y + h))
            im.save(f"assets/img/{sid}_{part}.png", optimize=True)
            m[part] = {"pw": im.size[0], "ph": im.size[1]}
        meta[sid] = m
    elif kind == "IMG":
        x, y, w, h = sp["crop"]
        meta[sid] = save_crop(sid, Image.open("work/img/" + sp["file"]).convert("RGB").crop((x, y, x + w, y + h)))
    if "bd" in sp:
        backdrop(sid, sp["bd"])
json.dump(meta, open("work/meta.json", "w"), indent=1)
print("done")

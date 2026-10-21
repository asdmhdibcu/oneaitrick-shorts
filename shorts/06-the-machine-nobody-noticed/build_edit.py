"""Short #6: cut, retime, crop and conform every shot for the HyperFrames composition (edl.py).

Inputs (git-ignored, supplied by the creator): work/raw/*.mp4 (Pexels, Flow, Anthropic's lab video, phone recording),
work/img/* (phone screenshots, photos), work/paper.pdf (bioRxiv 10.64898/2026.10.05.755809), plus work/page.png and
work/dna/ from stitch_page.py and stab_dna.py.
Outputs: assets/clips/<id>.mp4 (1080x1920, 30 fps, silent), assets/img/*, work/meta.json (card sizes).

Usage: python3 build_edit.py            (all)
       python3 build_edit.py s07 s21a   (only those shots)
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageFilter

from edl import SHOTS, H

Image.MAX_IMAGE_PIXELS = None
GRADE = "eq=contrast=1.04:saturation=1.05"
os.makedirs("assets/clips", exist_ok=True)
os.makedirs("assets/img", exist_ok=True)
os.makedirs("work/tmp", exist_ok=True)


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


def geo(src, mode, cx, flip):
    """Filter chain from the source frame to 1080x1920."""
    w, h = probe(src)
    fl = ",hflip" if flip else ""
    if mode == "native":
        return f"scale=1080:1920:flags=lanczos{fl}"
    if mode == "fill":
        cw = round(h * 9 / 16 / 2) * 2
        x = round(min(max(cx * w - cw / 2, 0), w - cw))
        return f"crop={cw}:{h}:{x}:0,scale=1080:1920:flags=lanczos{fl}"
    # tall: 3:4 window, 1080x1440 at the top, over a blurred 9:16 fill; the seam fades out
    cw = round(h * 3 / 4 / 2) * 2
    x = round(min(max(cx * w - cw / 2, 0), w - cw))
    fw = round(h * 9 / 16 / 2) * 2
    fx = round(min(max(cx * w - fw / 2, 0), w - fw))
    return (f"split[a][b];[a]crop={fw}:{h}:{fx}:0,scale=540:960,gblur=sigma=18,scale=1080:1920,eq=brightness=-0.06:saturation=0.9[bg];"
            f"[b]crop={cw}:{h}:{x}:0,scale=1080:1440:flags=lanczos,format=rgba[fg0];[1:v]format=gray[m];[fg0][m]alphamerge[fg];"
            f"[bg][fg]overlay=0:0,format=yuv420p{fl}")


def mask():
    """Alpha for the tall window: opaque, fading out over its last 220 px."""
    p = "work/tmp/tallmask.png"
    if not os.path.exists(p):
        m = Image.new("L", (1080, 1440), 255)
        for y in range(1220, 1440):
            m.paste(int(255 * (1440 - y) / 220), (0, y, 1080, y + 1))
        m.save(p)
    return ["-loop", "1", "-i", p]


def footage(sid, t0, t1, sp):
    src, sin = sp["src"], sp["sin"]
    span = t1 - t0 + 2 * H
    rate = sp.get("rate", 1.0)
    if "win" in sp:  # slow down just enough to stay inside the source shot
        a, b = sp["win"]
        rate = min(1.0, (b - a - 0.02) / span)
        sin = max(sin, a + H * rate + 0.01)
        sin = min(sin, b - 0.01 - (t1 - t0 + H) * rate)
    ss = sin - H * rate
    assert ss >= 0, (sid, ss)
    g = geo(src, sp.get("mode", "fill"), sp.get("cx", 0.5), sp.get("flip", False))
    timing = f"setpts=(PTS-STARTPTS)/{rate:.4f}"
    if rate < 0.97:
        timing += ",framerate=fps=30:interp_start=0:interp_end=255:scene=100"
    vf = f"{timing},{g},{GRADE},fps=30,format=yuv420p"
    extra = mask() if sp.get("mode") == "tall" else []
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{span * rate + 0.1:.3f}", "-i", src] + extra +
        ["-filter_complex", vf, "-t", f"{span:.3f}"] + enc(f"assets/clips/{sid}.mp4"))
    # first/last frames, used blurred behind the cards that follow
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         "-vf", "scale=540:960", f"assets/img/{sid}_last.png"])
    print(f"  {sid}: rate {rate:.3f}, source {ss:.2f}-{ss + span * rate:.2f}")


def frame(src, at, mode, cx, out):
    g = geo(src, mode, cx, False)
    extra = mask() if mode == "tall" else []
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", src] + extra + ["-filter_complex", f"{g},{GRADE}", "-frames:v", "1", out])


def backdrop(sid, bd):
    out = f"assets/img/{sid}_bd.jpg"
    if bd[0] == "last":
        im = Image.open(f"assets/img/{bd[1]}_last.png")
    elif bd[0] == "img":
        im = Image.open(f"work/img/{bd[1]}").convert("RGB")
    else:
        frame(bd[0], bd[1], "fill" if probe(bd[0])[0] > 2000 else "tall", 0.5, "work/tmp/bd.png")
        im = Image.open("work/tmp/bd.png")
    im = im.convert("RGB").resize((540, 960)).filter(ImageFilter.GaussianBlur(14))
    im.save(out, quality=88)


def page(sid, sp):
    pg = Image.open("work/page.png")
    crop = pg.crop((0, sp["y0"], pg.size[0], sp["y1"]))
    crop.save(f"assets/img/{sid}.png", optimize=True)
    return {"pw": crop.size[0], "ph": crop.size[1]}


def img(sid, sp):
    x, y, w, h = sp["crop"]
    im = Image.open("work/img/" + sp["file"]).convert("RGB").crop((x, y, x + w, y + h))
    im.save(f"assets/img/{sid}.png", optimize=True)
    return {"pw": w, "ph": h}


def fig(sid, sp):
    p = sp["page"]
    hi = f"work/pdf/p{p:02d}_600.png"
    if not os.path.exists(hi):
        run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", "600", "-png", "-singlefile", "work/paper.pdf", hi[:-4]])
    x, y, w, h = sp["box"]
    im = Image.open(hi).convert("RGB").crop((2 * x, 2 * y, 2 * (x + w), 2 * (y + h)))
    im.save(f"assets/img/{sid}.png", optimize=True)
    return {"pw": im.size[0], "ph": im.size[1]}


def dna(sid):
    """Dense and highlighted states of the post's DNA figure, from the steadied recording frames."""
    for name, f in (("dense", "f_0664.png"), ("lit", "f_0738.png")):
        Image.open("work/dna/" + f).convert("RGB").save(f"assets/img/{sid}_{name}.png", optimize=True)
    w, h = Image.open("work/dna/f_0664.png").size
    return {"pw": w, "ph": h}


meta = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
only = set(sys.argv[1:])
for sid, t0, t1, kind, sp in SHOTS:
    if only and sid not in only:
        continue
    print(sid, kind, flush=True)
    if kind == "V":
        footage(sid, t0, t1, sp)
    elif kind == "STILL":
        if "frame" in sp:
            src, at, mode, cx = sp["frame"]
            frame(src, at, mode, cx, f"assets/img/{sid}.png")
        else:
            Image.open(sp["img"]).convert("RGB").save(f"assets/img/{sid}.jpg", quality=92)
        im = Image.open(f"assets/img/{sid}.png" if "frame" in sp else f"assets/img/{sid}.jpg")
        im.convert("RGB").resize((540, 960)).save(f"assets/img/{sid}_last.png")
        meta[sid] = {"pw": im.size[0], "ph": im.size[1]}
    elif kind == "PAGE":
        meta[sid] = page(sid, sp)
    elif kind == "IMG":
        meta[sid] = img(sid, sp)
    elif kind == "FIG":
        meta[sid] = fig(sid, sp)
    elif kind == "DNA":
        meta[sid] = dna(sid)
    if "bd" in sp:
        backdrop(sid, sp["bd"])
json.dump(meta, open("work/meta.json", "w"), indent=1)
print("done")

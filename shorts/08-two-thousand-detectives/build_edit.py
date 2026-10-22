"""Short #8: cut, retime, crop, grade and conform every shot for the HyperFrames composition (edl.py).

Inputs (git-ignored): work/raw/* (Flow clips, Pexels clips, the creator's phone recordings), ../06-.../work/raw (library,
lab footage), work/img/* (figure images, phone frames), work/pdf/*.png (PDF pages at 300 dpi), work/sim/*.mp4 (render3d.py).
Outputs: assets/clips/<id>.mp4 (1080x1920, 30 fps, silent), assets/img/*, work/meta.json (card sizes).

One look across every source: stock footage gets a teal-shadow / amber-highlight grade to sit with the Flow clips;
upscaled sources (720p Flow clips, the phone recording) get a light unsharp after Lanczos.
Usage: python3 build_edit.py            (all)
       python3 build_edit.py s07 s21    (only those shots)
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageFilter

from edl import SHOTS, H, REC1

Image.MAX_IMAGE_PIXELS = None
NOIR = "colorbalance=rs=-0.04:bs=0.05:rm=-0.02:bm=0.03:rh=0.04:gh=0.01:bh=-0.03,eq=contrast=1.06:saturation=0.86:gamma=0.97"
LIGHT = "eq=contrast=1.03:saturation=1.04"
SHARP = "unsharp=5:5:0.55:5:5:0.0"
TM = open("work/tm.txt").read().strip()
LV = open("work/lv.txt").read().strip()
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


def geo(src, mode, cx, pre=None, W=1080, Hh=1920):
    """Filter chain from the source frame to W x Hh."""
    if mode == "rec":  # the 16:9 video band of the phone recording, full width on black, centred at y 720
        return f"crop=1320:742:0:1062,{TM},{LV},scale=1400:788:flags=lanczos,{SHARP},crop=1080:788:160:0,pad=1080:1920:0:326:black"
    if mode in ("native", "sim"):
        return f"scale={W}:{Hh}:flags=lanczos"
    w, h = probe(src)
    head = ""
    if pre:
        head = f"crop={pre[0]}:{pre[1]}:{pre[2]}:{pre[3]},"
        w, h = pre[0], pre[1]
    sharp = f",{SHARP}" if h < 1700 else ""
    if mode == "vert":  # vertical source: fit the width, crop the height around the centre
        return f"{head}scale={W}:-2:flags=lanczos,crop={W}:{Hh}:0:(ih-{Hh})/2{sharp}"
    cw = round(h * W / Hh / 2) * 2
    if cw > w:  # source narrower than 9:16: fit the width and crop the height
        ch = round(w * Hh / W / 2) * 2
        return f"{head}crop={w}:{ch}:0:{(h - ch) // 2},scale={W}:{Hh}:flags=lanczos{sharp}"
    x = round(min(max(cx * w - cw / 2, 0), w - cw))
    return f"{head}crop={cw}:{h}:{x}:0,scale={W}:{Hh}:flags=lanczos{sharp}"


def grade_for(src):
    return LIGHT if "flow_" in src or "/sim/" in src or src == REC1 else NOIR


def conform(src, sin, span, out, mode="fill", cx=0.5, rate=1.0, rev=False, pre=None, grade=True):
    """span seconds of output starting H before the out start (source in-point sin sits at out start)."""
    ss = max(0.0, sin - H * rate)
    timing = f"setpts=(PTS-STARTPTS)/{rate:.4f}"
    if rate < 0.97:
        timing += ",minterpolate=fps=30:mi_mode=blend"
    g = geo(src, mode, cx, pre)
    chain = f"{timing},{g}" + (f",{grade_for(src)}" if grade else "") + ",fps=30" + (",reverse" if rev else "") + ",format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{span * rate + 0.2:.3f}", "-i", src,
         "-filter_complex", chain, "-t", f"{span:.3f}"] + enc(out))


def ramp(sid, sp, span):
    """Piecewise speed: [(out offset from the out start, rate), ...]; each piece conformed and joined."""
    pieces, src_t = [], sp["sin"] - H * sp["ramp"][0][1]
    bounds = [(-H, sp["ramp"][0][1])] + [(o, r) for o, r in sp["ramp"][1:]]
    for k, (o, r) in enumerate(bounds):
        o_end = bounds[k + 1][0] if k + 1 < len(bounds) else span - H
        dur = o_end - o
        p = f"work/tmp/{sid}_r{k}.mp4"
        conform(sp["src"], src_t + H * r, dur, p, sp.get("mode", "fill"), sp.get("cx", 0.5), r, pre=sp.get("pre"))
        pieces.append(p)
        src_t += dur * r
    lst = f"work/tmp/{sid}_list.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in pieces))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst] + enc(f"assets/clips/{sid}.mp4"))


def last_frame(sid):
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         "-vf", "scale=540:960", f"assets/img/{sid}_last.png"])


def still(sid, at, name=None):
    """Frame of a conformed shot at out time `at`, full size."""
    t0 = T[sid][0]
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at - (t0 - H):.3f}", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         f"assets/img/{name or sid + '_freeze'}.png"])


def footage(sid, t0, t1, sp):
    span = t1 - t0 + 2 * H
    if "ramp" in sp:
        ramp(sid, sp, span)
    elif sp.get("rev"):
        # backwards: take the source window that ends at sin and reverse it
        r = sp.get("rate", 1.0)
        conform(sp["src"], max(H * r, sp["sin"] - span * r + H * r), span, f"assets/clips/{sid}.mp4", sp.get("mode", "fill"),
                sp.get("cx", 0.5), r, rev=True, pre=sp.get("pre"))
    else:
        conform(sp["src"], sp["sin"], span, f"assets/clips/{sid}.mp4", sp.get("mode", "fill"), sp.get("cx", 0.5), sp.get("rate", 1.0),
                pre=sp.get("pre"))
    if "freeze" in sp:
        still(sid, sp["freeze"])
    last_frame(sid)


def frame_of(src, at, out):
    g = geo(src, "fill", 0.5, None)
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", src, "-filter_complex", f"{g},{grade_for(src)}", "-frames:v", "1", out])


def backdrop(sid, bd):
    out = f"assets/img/{sid}_bd.jpg"
    if bd[0] == "last":
        im = Image.open(f"assets/img/{bd[1]}_last.png")
    else:
        frame_of(bd[0], bd[1], "work/tmp/bd.png")
        im = Image.open("work/tmp/bd.png")
    im = im.convert("RGB").resize((540, 960)).filter(ImageFilter.GaussianBlur(14))
    im.save(out, quality=88)


def save_crop(sid, im, maxw=2000):
    if im.size[0] > maxw:  # cards show at <= 1000 px and zoom <= 1.7x: 2000 px keeps them sharp and the page light
        im = im.resize((maxw, round(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    im.save(f"assets/img/{sid}.png", optimize=True)
    return {"pw": im.size[0], "ph": im.size[1]}


if __name__ == "__main__":
    meta = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
    only = set(sys.argv[1:])
    for sid, t0, t1, kind, sp in SHOTS:
        if only and sid not in only:
            continue
        print(sid, kind, flush=True)
        span = t1 - t0 + 2 * H
        if kind == "V":
            footage(sid, t0, t1, sp)
        elif kind == "REC":
            conform(REC1, sp["sin"], span, f"assets/clips/{sid}.mp4", "rec")
            last_frame(sid)
        elif kind == "SIM":
            conform(sp["src"], sp["sin"], span, f"assets/clips/{sid}.mp4", "sim", grade=False)
            last_frame(sid)
        elif kind == "PDF":
            x, y, w, h = sp["box"]
            pg = Image.open(f"work/pdf/{sp['doc']}-{sp['page']}.png").convert("RGB")
            meta[sid] = save_crop(sid, pg.crop((x, y, x + w, y + h)))
            meta[sid]["src_w"] = w
        elif kind == "IMG":
            x, y, w, h = sp["crop"]
            meta[sid] = save_crop(sid, Image.open("work/img/" + sp["file"]).convert("RGB").crop((x, y, x + w, y + h)))
            meta[sid]["src_w"] = w
        if "bd" in sp:
            backdrop(sid, sp["bd"])
    json.dump(meta, open("work/meta.json", "w"), indent=1)
    print("done")

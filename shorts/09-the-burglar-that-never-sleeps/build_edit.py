"""Short #9: cut, retime, crop, grade and conform every shot for the HyperFrames composition (edl.py).

Inputs (git-ignored): work/raw/* (Flow clips, Pexels clips, the robot picture), assets/pages/* (make_pages.py),
assets/img/i1_*.{jpg,png} (make_photo.py).
Outputs: assets/clips/<id>.mp4 (1080x1920, 30 fps, silent), assets/img/<id>_bd.jpg backdrops, <id>_last.png, work/meta.json.

One look: night stock gets the noir grade (teal shadows, amber highlights) to sit with the Flow clips; the two daylight
shots (the locksmith, the robot's day job) stay warm and bright on purpose. 720p Flow clips get Lanczos + light unsharp.
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
GRADES = {
    "noir": "colorbalance=rs=-0.04:bs=0.05:rm=-0.02:bm=0.03:rh=0.04:gh=0.01:bh=-0.03,eq=contrast=1.06:saturation=0.86:gamma=0.97",
    "dark": "colorbalance=rs=-0.03:bs=0.04:rh=0.05:bh=-0.03,eq=contrast=1.12:saturation=0.9:gamma=0.95",
    "day": "colorbalance=rh=0.03:gh=0.01:bh=-0.03,eq=contrast=1.04:saturation=1.02",
    "flow": "eq=contrast=1.03:saturation=0.98",
    "flowday": "colorbalance=rh=0.02:bh=-0.02,eq=contrast=1.03:saturation=1.0",
    "flowdark": "colorbalance=rs=-0.04:bs=0.06:rm=-0.02:bm=0.03:rh=0.03:bh=-0.02,eq=brightness=-0.05:contrast=1.08:saturation=0.8:gamma=0.92",
}
SHARP = "unsharp=5:5:0.55:5:5:0.0"
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


def enc(out, crf=15):
    return ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", out]


def geo(src, mode, cx, pre=None, W=1080, Hh=1920):
    """Filter chain from the source frame to W x Hh."""
    w, h = probe(src)
    head = ""
    if pre:
        head = f"crop={pre[0]}:{pre[1]}:{pre[2]}:{pre[3]},"
        w, h = pre[0], pre[1]
    sharp = f",{SHARP}" if h < 1700 or (mode == "vert" and w < 1300) else ""
    if mode == "vert":  # vertical source: fit the width, crop the height around the centre
        return f"{head}scale={W}:-2:flags=lanczos,crop={W}:{Hh}:0:(ih-{Hh})/2{sharp}"
    cw = round(h * W / Hh / 2) * 2
    if cw > w:  # source narrower than 9:16: fit the width and crop the height
        ch = round(w * Hh / W / 2) * 2
        return f"{head}crop={w}:{ch}:0:{(h - ch) // 2},scale={W}:{Hh}:flags=lanczos{sharp}"
    x = round(min(max(cx * w - cw / 2, 0), w - cw))
    return f"{head}crop={cw}:{h}:{x}:0,scale={W}:{Hh}:flags=lanczos{sharp}"


def conform(src, sin, span, out, mode="fill", cx=0.5, rate=1.0, pre=None, grade="noir", W=1080, Hh=1920):
    """span seconds of output starting H before the out start (source in-point sin sits at out start)."""
    ss = max(0.0, sin - H * rate)
    timing = f"setpts=(PTS-STARTPTS)/{rate:.4f}"
    if rate < 0.97:
        timing += ",minterpolate=fps=30:mi_mode=blend"
    if mode == "box":  # a landscape region set full width at y=ty over its own blurred, darkened fill
        bx, by, bw, bh, ty = pre
        chain = (f"{timing},crop={bw}:{bh}:{bx}:{by},split[a][b];[a]scale={W}:{Hh}:force_original_aspect_ratio=increase,crop={W}:{Hh},"
                 f"boxblur=30:2,eq=brightness=-0.12[bg];[b]scale={W}:-2:flags=lanczos,{SHARP}[fg];[bg][fg]overlay=0:{ty},{GRADES[grade]},fps=30,format=yuv420p")
    else:
        chain = f"{timing},{geo(src, mode, cx, pre, W, Hh)},{GRADES[grade]},fps=30,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{span * rate + 0.3:.3f}", "-i", src,
         "-filter_complex", chain, "-t", f"{span:.3f}"] + enc(out))


def concat(pieces, out):
    lst = "work/tmp/" + os.path.basename(out) + ".txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in pieces))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst] + enc(out))


def ramp(sid, sp, span):
    """Piecewise speed: [(out offset from the out start, rate), ...]; each piece conformed and joined."""
    pieces, src_t = [], sp["sin"] - H * sp["ramp"][0][1]
    bounds = [(-H, sp["ramp"][0][1])] + [(o, r) for o, r in sp["ramp"][1:]]
    for k, (o, r) in enumerate(bounds):
        o_end = bounds[k + 1][0] if k + 1 < len(bounds) else span - H
        dur = o_end - o
        p = f"work/tmp/{sid}_r{k}.mp4"
        conform(sp["src"], src_t + H * r, dur, p, sp.get("mode", "fill"), sp.get("cx", 0.5), r, sp.get("pre"), sp.get("grade", "noir"))
        pieces.append(p)
        src_t += dur * r
    concat(pieces, f"assets/clips/{sid}.mp4")


def pingpong(src, a, b, rate, span, out, crop_vf, grade="noir", phase=0.0, flip=False):
    """Play source a..b forwards then backwards, repeated, from `phase` seconds in, for span seconds."""
    seg = (b - a) / rate
    vf = f"setpts=(PTS-STARTPTS)/{rate:.4f},{crop_vf},{GRADES[grade]}" + (",hflip" if flip else "") + ",fps=30,format=yuv420p"
    fwd, rev = out + ".f.mp4", out + ".r.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", src, "-vf", vf, "-t", f"{seg:.3f}"] + enc(fwd, 17))
    run(["ffmpeg", "-v", "error", "-y", "-i", fwd, "-vf", "reverse"] + enc(rev, 17))
    n = int((span + phase) / (2 * seg)) + 2
    concat([fwd, rev] * n, out + ".l.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{phase:.3f}", "-i", out + ".l.mp4", "-t", f"{span:.3f}"] + enc(out))
    for f in (fwd, rev, out + ".l.mp4", out + ".l.mp4.txt"):
        os.path.exists(f) and os.remove(f)


def last_frame(sid):
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         "-vf", "scale=540:960", f"assets/img/{sid}_last.png"])


def frame_of(src, at, out):
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", src, "-filter_complex", f"{geo(src, 'fill', 0.5)},{GRADES['noir']}",
         "-frames:v", "1", out])


def backdrop(sid, bd):
    out = f"assets/img/{sid}_bd.jpg"
    if bd[0] == "last":
        im = Image.open(f"assets/img/{bd[1]}_last.png")
    else:
        frame_of(bd[0], bd[1], "work/tmp/bd.png")
        im = Image.open("work/tmp/bd.png")
    im.convert("RGB").resize((540, 960)).filter(ImageFilter.GaussianBlur(14)).save(out, quality=88)


if __name__ == "__main__":
    meta = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
    pages = json.load(open("assets/pages/pages.json"))
    only = set(sys.argv[1:])
    for sid, t0, t1, kind, sp in SHOTS:
        if only and sid not in only:
            continue
        print(sid, kind, flush=True)
        span = t1 - t0 + 2 * H
        out = f"assets/clips/{sid}.mp4"
        if kind == "V":
            if "ramp" in sp:
                ramp(sid, sp, span)
            else:
                conform(sp["src"], sp["sin"], span, out, sp.get("mode", "fill"), sp.get("cx", 0.5), sp.get("rate", 1.0), sp.get("pre"),
                        sp.get("grade", "noir"))
            last_frame(sid)
        elif kind == "LOOP":
            w, h = probe(sp["src"]); cw = round(h * 1080 / 1920 / 2) * 2; x = round(min(max(sp["cx"] * w - cw / 2, 0), w - cw))
            pingpong(sp["src"], sp["a"], sp["b"], sp["rate"], span, out, f"crop={cw}:{h}:{x}:0,scale=1080:1920:flags=lanczos")
            last_frame(sid)
        elif kind == "MOSAIC":
            # 3 x 4 tiles of 360 x 480 around the handle, each at its own phase, every other one mirrored
            tiles = []
            for k in range(12):
                p = f"work/tmp/{sid}_t{k}.mp4"
                pingpong(sp["src"], 0.05, 1.15, 1.7 + 0.15 * (k % 3), span, p, "crop=1300:1733:1193:213,scale=360:480:flags=lanczos",
                         phase=(k * 0.23) % 1.2, flip=bool(k % 2))
                tiles.append(p)
            ins = sum([["-i", p] for p in tiles], [])
            layout = "|".join(f"{(k % 3) * 360}_{(k // 3) * 480}" for k in range(12))
            run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", f"xstack=inputs=12:layout={layout},format=yuv420p"] + enc(out))
            last_frame(sid)
        elif kind == "SPLIT":
            # left half: the robot picture at night; right half: the day clip, framed on the robot
            right = f"work/tmp/{sid}_right.mp4"
            conform(sp["src"], sp["sin"], span, right, "fill", 0.5, 1.0, None, "flowday")
            run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{span:.3f}", "-i", "assets/img/i1_full.jpg", "-i", right,
                 "-filter_complex", "[0:v]crop=540:1920:270:0,fps=30,format=yuv420p[l];[1:v]crop=540:1920:200:0[r];[l][r]hstack=inputs=2,format=yuv420p",
                 "-t", f"{span:.3f}"] + enc(out))
            last_frame(sid)
        elif kind == "STILL":
            a = T[sp["of"]][0] - H
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sp['at'] - a:.3f}", "-i", f"assets/clips/{sp['of']}.mp4", "-frames:v", "1",
                 f"assets/img/{sid}.png"])
            Image.open(f"assets/img/{sid}.png").resize((540, 960)).save(f"assets/img/{sid}_last.png")
        elif kind == "PAGE":
            if sp["name"] == "r1_figure":
                im = Image.open("assets/pages/r1_figure.png"); meta[sid] = {"pw": im.width, "ph": im.height, "boxes": [[14, 316, 466, 160]]}
            else:
                pg = pages[sp["name"]]; meta[sid] = {"pw": pg["w"], "ph": pg["h"], "boxes": pg["boxes"]}
        elif kind == "PHOTO":
            Image.open("assets/img/i1_full.jpg").resize((540, 960)).save(f"assets/img/{sid}_last.png")
        if "bd" in sp:
            backdrop(sid, sp["bd"])
    json.dump(meta, open("work/meta.json", "w"), indent=1)
    print("done")

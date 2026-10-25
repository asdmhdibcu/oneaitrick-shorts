"""Short #10: cut, retime, crop, grade and conform every shot for the HyperFrames composition (edl.py).

Inputs (git-ignored): work/raw/* (Flow clips g1-g7, Pexels px_*), assets/pages/* (make_pages.py).
Outputs: assets/clips/<id>.mp4 (1080x1920, 30 fps, silent): the footage of V shots, and for PAGE and GFX shots a moving
backdrop (blurred, darkened footage); assets/img/<id>_last.png; work/meta.json (page sizes and highlight boxes).

One look: "ink" for night stock (deep navy shadows, a warm lamp kept warm), "day" for the flag and the two cities, the
Flow clips nearly untouched. 720p Flow clips get Lanczos + light unsharp.
Usage: python3 build_edit.py            (all)
       python3 build_edit.py s07 s21    (only those shots)
"""
import json
import os
import subprocess
import sys

from PIL import Image

from edl import SHOTS, H

GRADES = {
    "ink": "colorbalance=rs=-0.05:gs=-0.01:bs=0.07:rm=-0.02:bm=0.03:rh=0.03:gh=0.01:bh=-0.02,eq=contrast=1.06:saturation=0.86:gamma=0.96",
    "inkb": "colorbalance=rs=-0.04:bs=0.06:rh=0.03:bh=-0.02,eq=brightness=0.04:contrast=1.08:saturation=0.92:gamma=1.32",
    "day": "colorbalance=rh=0.02:bh=-0.02,eq=contrast=1.04:saturation=1.0",
    "flow": "eq=contrast=1.03:saturation=0.98",
    "bd": "colorbalance=rs=-0.05:bs=0.07,eq=brightness=-0.16:contrast=0.92:saturation=0.7",
}
SHARP = "unsharp=5:5:0.55:5:5:0.0"
os.makedirs("assets/clips", exist_ok=True)
os.makedirs("assets/img", exist_ok=True)
os.makedirs("work/tmp", exist_ok=True)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)); print(r.stderr[-2500:]); sys.exit(1)
    return r


def probe(src):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", src])
    j = json.loads(r.stdout)
    return int(j["streams"][0]["width"]), int(j["streams"][0]["height"]), float(j["format"]["duration"])


def enc(out, crf=15):
    return ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", out]


def geo(src, mode, cx, pre=None, W=1080, Hh=1920):
    """Filter chain from the source frame to W x Hh."""
    w, h, _ = probe(src)
    head = ""
    if pre:
        head = f"crop={pre[0]}:{pre[1]}:{pre[2]}:{pre[3]},"
        w, h = pre[0], pre[1]
    sharp = f",{SHARP}" if h < 1700 or (mode == "vert" and w < 1300) else ""
    if mode == "vert":
        return f"{head}scale={W}:-2:flags=lanczos,crop={W}:{Hh}:0:(ih-{Hh})/2{sharp}"
    cw = round(h * W / Hh / 2) * 2
    if cw > w:
        ch = round(w * Hh / W / 2) * 2
        return f"{head}crop={w}:{ch}:0:{(h - ch) // 2},scale={W}:{Hh}:flags=lanczos{sharp}"
    x = round(min(max(cx * w - cw / 2, 0), w - cw))
    return f"{head}crop={cw}:{h}:{x}:0,scale={W}:{Hh}:flags=lanczos{sharp}"


def conform(src, sin, span, out, mode="fill", cx=0.5, rate=1.0, pre=None, grade="ink", blur=False):
    """span seconds of output starting H before the shot start (source in-point sin sits at the shot start).
    A source too short for the span holds its last frame (tpad)."""
    _, _, dur = probe(src)
    ss = max(0.0, sin - H * rate)
    need = span * rate + 0.3
    hold = max(0.0, (ss + need) - dur + 0.1) / rate
    timing = f"setpts=(PTS-STARTPTS)/{rate:.4f}"
    if rate < 0.97:
        timing += ",minterpolate=fps=30:mi_mode=blend"
    if mode == "box":
        bx, by, bw, bh, ty = pre
        chain = (f"{timing},crop={bw}:{bh}:{bx}:{by},split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                 f"boxblur=30:2,eq=brightness=-0.12[bg];[b]scale=1080:-2:flags=lanczos,{SHARP}[fg];[bg][fg]overlay=0:{ty},{GRADES[grade]}")
    else:
        chain = f"{timing},{geo(src, mode, cx, pre)},{GRADES[grade]}"
    if blur:
        chain += ",scale=270:480,boxblur=6:2,scale=1080:1920:flags=bicubic," + GRADES["bd"]
    if hold > 0:
        chain += f",tpad=stop_mode=clone:stop_duration={hold + 0.5:.2f}"
    chain += ",fps=30,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{need:.3f}", "-i", src,
         "-filter_complex", chain, "-t", f"{span:.3f}"] + enc(out, 20 if blur else 15))


def last_frame(sid):
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         "-vf", "scale=540:960", f"assets/img/{sid}_last.png"])


if __name__ == "__main__":
    meta = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
    pages = json.load(open("assets/pages/pages.json"))
    only = set(sys.argv[1:])
    for sid, t0, t1, kind, sp in SHOTS:
        if only and sid not in only:
            continue
        print(sid, kind, f"{t0:.2f}-{t1:.2f}", flush=True)
        span = t1 - t0 + 2 * H
        out = f"assets/clips/{sid}.mp4"
        if kind == "V":
            conform(sp["src"], sp["sin"], span, out, sp.get("mode", "fill"), sp.get("cx", 0.5), sp.get("rate", 1.0), sp.get("pre"),
                    sp.get("grade", "ink"))
            last_frame(sid)
        elif kind in ("PAGE", "GFX"):
            src, sin, rate, cx = sp["bdv"]
            conform(src, sin, span, out, "fill", cx, rate, None, "ink", blur=True)
            if kind == "PAGE":
                pg = pages[sp["name"]]; meta[sid] = {"pw": pg["w"], "ph": pg["h"], "boxes": pg["boxes"]}
        elif kind == "END":
            prev = SHOTS[[s[0] for s in SHOTS].index(sid) - 1][0]
            Image.open(f"assets/img/{prev}_last.png").save(f"assets/img/{sid}_bd.png")
    json.dump(meta, open("work/meta.json", "w"), indent=1)
    print("done")

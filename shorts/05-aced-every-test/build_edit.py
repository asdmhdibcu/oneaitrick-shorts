"""Short #5: cut, retime, grade and conform every shot for the HyperFrames composition.

Inputs (git-ignored, supplied by the creator):
  work/raw/*.mp4            19 Veo 3.1 clips from Google Flow (720x1280, 24 fps, 8 s)
  work/raw_paper_video.mov  screen recording of the authors' project video (1320x740, HDR PQ)
  work/paper.pdf            arXiv 2610.22471
Outputs: assets/clips/*.mp4 (1080 wide, 30 fps, silent), assets/img/*.png, clips.html (markup for index.html)

Usage: python3 build_edit.py            (all)
       python3 build_edit.py s14 s19    (only those shots)
"""
import glob
import json
import os
import subprocess
import sys

RAW = "work/raw"
PV = "work/raw_paper_video.mov"
TM = ("zscale=tin=smpte2084:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=tonemap=clip:desat=0,zscale=t=bt709:m=bt709:r=tv")
GRADE = "eq=contrast=1.05:brightness=-0.008:saturation=1.04,unsharp=5:5:0.45:5:5:0"
os.makedirs("assets/clips", exist_ok=True)
os.makedirs("assets/img", exist_ok=True)

from edl import FLOW, SHOTS, GRID, TILE, H  # noqa: E402



def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)); print(r.stderr[-2000:]); sys.exit(1)


def enc(out):
    return ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", out]


def src_window(t0, t1, sin, rate):
    """Source start and length (in source seconds) covering out [t0-H, t1+H]."""
    return sin - H * rate, (t1 - t0 + 2 * H) * rate


def flow(sid, t0, t1, cid, sin, rate, ex):
    f = glob.glob(f"{RAW}/{FLOW[cid]}*.mp4")[0]
    ss, dur = src_window(t0, t1, sin, rate)
    assert ss >= 0 and ss + dur <= 8.0 + 1e-6, (sid, ss, dur)
    if "zoom_top" in ex:
        z = ex["zoom_top"]; W, Hh = round(1080 * z / 2) * 2, round(1920 * z / 2) * 2
        geo = f"scale={W}:{Hh}:flags=lanczos,crop=1080:1920:{(W - 1080) // 2}:0"
    else:
        geo = "scale=1080:1920:flags=lanczos"
    vf = f"setpts=(PTS-STARTPTS)/{rate},{geo},{GRADE},fps=30,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", f, "-vf", vf,
         "-t", f"{t1 - t0 + 2 * H:.3f}"] + enc(f"assets/clips/{sid}.mp4"))
    if "freeze" in ex:  # still frame for a freeze-frame overlay, taken from the conformed clip
        at = ex["freeze"] - (t0 - H)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
             f"assets/img/{sid}_freeze.png"])
    # last frame, used blurred behind the next evidence card
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         "-vf", "scale=540:960", f"assets/img/{sid}_last.png"])


def pv(sid, t0, t1, sin, rate, crop, w, name=None):
    x, y, cw, ch = crop
    ss, dur = src_window(t0, t1, sin, rate)
    hgt = round(ch * w / cw / 2) * 2
    vf = f"{TM},crop={cw}:{ch}:{x}:{y},setpts=(PTS-STARTPTS)/{rate},scale={w}:{hgt}:flags=lanczos,fps=30,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", PV, "-vf", vf,
         "-t", f"{t1 - t0 + 2 * H:.3f}"] + enc(f"assets/clips/{name or sid}.mp4"))
    return w, hgt


def pvstill(sid, at, crop, w):
    x, y, cw, ch = crop
    hgt = round(ch * w / cw)
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", PV, "-frames:v", "1", "-vf",
         f"{TM},crop={cw}:{ch}:{x}:{y},scale={w}:{hgt}:flags=lanczos,format=rgb24", f"assets/img/{sid}.png"])
    return w, hgt


def pvgrid(sid, t0, t1, sin):
    ss, dur = src_window(t0, t1, sin, 1.0)
    for k, (x, y) in enumerate(GRID):
        vf = f"{TM},crop={TILE[0]}:{TILE[1]}:{x}:{y},scale=360:226:flags=lanczos,fps=30,format=yuv420p"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", PV, "-vf", vf]
            + enc(f"assets/clips/{sid}_{k}.mp4"))


def pdf():
    # page 1 at 300 dpi, top band: logos, title, author line
    run(["pdftoppm", "-f", "1", "-l", "1", "-r", "300", "-png", "-singlefile", "work/paper.pdf", "work/p1_300"])
    run(["ffmpeg", "-v", "error", "-y", "-i", "work/p1_300.png", "-vf", "crop=2250:1410:75:90,scale=960:-2:flags=lanczos",
         "assets/img/paper_top.png"])


meta = {}
only = set(sys.argv[1:])
for sid, t0, t1, src, sin, rate, ex in SHOTS:
    if only and sid not in only:
        continue
    print(sid, src, flush=True)
    if src.startswith("C"):
        flow(sid, t0, t1, src, sin, rate, ex)
    elif src == "PV":
        meta[sid] = pv(sid, t0, t1, sin, rate, ex["crop"], ex["w"])
        if "also" in ex:
            n, c, w2 = ex["also"]
            meta[n] = pv(sid, t0, t1, sin, rate, c, w2, name=n)
    elif src == "PVSTILL":
        meta[sid] = pvstill(sid, sin, ex["crop"], ex["w"])
    elif src == "PVGRID":
        pvgrid(sid, t0, t1, sin)
    elif src == "PDF":
        pdf()
if meta:
    old = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
    old.update(meta)
    json.dump(old, open("work/meta.json", "w"), indent=1)
print("done")

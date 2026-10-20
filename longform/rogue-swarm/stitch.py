#!/usr/bin/env python3
"""Stitch chapter MP4s with short cross-dissolves, keeping A/V in sync.
Video: chained xfade (dissolve). Audio: chained acrossfade.
Both shorten by D at each boundary, so they stay aligned.
Usage: stitch.py OUT D SCALE CRF clip1.mp4 clip2.mp4 ...
  SCALE: 0 = keep 1920x1080; else width (e.g. 854 for a fast test)
"""
import sys, subprocess, json

def dur(f):
    out = subprocess.check_output(["ffprobe","-v","error","-show_entries",
        "format=duration","-of","default=noprint_wrappers=1:nokey=1",f]).decode().strip()
    return float(out)

out, D, SCALE, CRF = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
clips = sys.argv[5:]
n = len(clips)
durs = [dur(c) for c in clips]

cmd = ["ffmpeg","-y","-hide_banner","-loglevel","error","-stats"]
for c in clips:
    cmd += ["-i", c]

fc = []
# normalise each video stream (fps, sar, optional scale, format) and label
for i in range(n):
    vf = "settb=AVTB,fps=30,setsar=1,format=yuv420p"
    if SCALE:
        vf = f"scale={SCALE}:-2," + vf
    fc.append(f"[{i}:v]{vf}[v{i}]")
    fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo[a{i}]")

# chain xfade on video and acrossfade on audio
voff = 0.0
vprev, aprev = "v0", "a0"
for i in range(1, n):
    voff += durs[i-1] - D
    vout = f"vx{i}"; aout = f"ax{i}"
    fc.append(f"[{vprev}][v{i}]xfade=transition=fade:duration={D}:offset={voff:.3f}[{vout}]")
    fc.append(f"[{aprev}][a{i}]acrossfade=d={D}:c1=tri:c2=tri[{aout}]")
    vprev, aprev = vout, aout

filter_complex = ";".join(fc)
cmd += ["-filter_complex", filter_complex, "-map", f"[{vprev}]", "-map", f"[{aprev}]",
        "-c:v","libx264","-preset","medium" if not SCALE else "ultrafast","-crf",CRF,
        "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart", out]

total = sum(durs) - D*(n-1)
print(f"stitching {n} clips -> {out}  (expected {total:.2f}s, D={D})")
r = subprocess.run(cmd)
sys.exit(r.returncode)

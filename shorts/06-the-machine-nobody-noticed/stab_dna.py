"""Steady crop of the post's animated DNA figure, using the scroll offsets from stitch_page.py.

Usage: python3 stab_dna.py T0 T1 OUTDIR   (seconds in work/raw/rec2.mp4)
Writes OUTDIR/f_NNNN.png (figure box, full resolution) for every 30 fps frame where the whole box is in the clean band.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

T0, T1, OUT = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
os.makedirs(OUT, exist_ok=True)
W, H = 1320, 2868
d = json.load(open("work/page_off.json")); off = np.array(d["off"])
PY0, PY1, PX0, PX1 = 16300, 17260, 130, 1192  # figure box in page coords (x in source pixels)
TM = open("work/tm.txt").read().strip(); LV = open("work/lv.txt").read().strip()
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", "work/raw/rec2.mp4", "-vf", f"fps=30,{TM},{LV},format=rgb24",
                      "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
i = 0; kept = []
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3:
        break
    t = i / 30
    if T0 <= t <= T1:
        f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        y0 = PY0 - off[i]
        if 590 <= y0 and y0 + (PY1 - PY0) <= 2640:
            Image.fromarray(f[y0:y0 + PY1 - PY0, PX0:PX1]).save(f"{OUT}/f_{i:04d}.png")
            kept.append(i)
    i += 1
print(len(kept), kept[:3], kept[-3:])

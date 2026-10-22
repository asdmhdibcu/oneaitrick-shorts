"""Grab one clean phone frame showing page rows Y0..Y1 of a stitched page (avoids stitch seams). 
Usage: python3 frame_for.py PAGE SRC Y0 Y1 OUT.png"""
import json, subprocess, sys
import numpy as np
page, src, y0, y1, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
d = json.load(open(f"work/pages/{page}_off.json")); off = np.array(d["off"]); t0 = d["t0"]
band0, band1 = 200, 2560
ok = [i for i in range(len(off)) if off[i] <= y0 - band0 and off[i] >= y1 - band1]
mot = np.abs(np.diff(off, prepend=off[0])) + np.abs(np.diff(off, append=off[-1]))
best = min(ok, key=lambda i: (mot[i], abs((off[i] + 1400) - (y0 + y1) / 2)))
t = t0 + best / 30
TM = open("work/tm.txt").read().strip(); LV = open("work/lv.txt").read().strip()
fy0, fy1 = y0 - off[best], y1 - off[best]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", f"{TM},{LV},crop=1320:{fy1 - fy0}:0:{fy0}", out], check=True)
print("frame", best, "t", round(t, 2), "motion", mot[best], "rows", fy0, fy1)

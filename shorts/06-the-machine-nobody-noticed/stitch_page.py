"""Rebuild the Anthropic post as one tall, clean image from the creator's phone screen recording.

The recording scrolls by hand and has the iOS status bar, the site's sticky header, Safari's URL pill and the
AssistiveTouch button over it. This measures the scroll between frames, then pastes only the clean content band
(rows 600-2620, x 40-1280) of every frame into one canvas, keeping for each page row the frame that moved least.
The edit then pans and zooms over work/page.png with its own steady camera instead of the shaky recording.

Usage: python3 stitch_page.py work/raw/rec2.mp4 work/page.png
"""
import json
import subprocess
import sys

import numpy as np
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
W, H = 1320, 2868
Y0, Y1, X0, X1 = 600, 2620, 40, 1280
TM = open("work/tm.txt").read().strip()
LV = open("work/lv.txt").read().strip()


def frames(gray):
    fmt = "gray" if gray else "rgb24"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"fps=30,{TM},{LV},format={fmt}", "-f", "rawvideo", "-"],
                         stdout=subprocess.PIPE)
    n = W * H * (1 if gray else 3)
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        a = np.frombuffer(b, np.uint8)
        yield a.reshape(H, W) if gray else a.reshape(H, W, 3)


# pass 1: vertical shift between consecutive frames (row-profile matching on the content band)
shifts, prev = [0], None
for g in frames(True):
    prof = g[:, X0 + 20:X1 - 20].astype(np.float32).mean(1)
    if prev is not None:
        best = (1e9, 0)
        for s in range(-400, 401):
            a0, a1 = Y0 + 200, Y1 - 200
            if a0 + s < Y0 - 200 or a1 + s > Y1 + 40:
                continue
            e = np.abs(prev[a0:a1] - prof[a0 + s:a1 + s]).mean()
            if e < best[0]:
                best = (e, s)
        shifts.append(best[1])
    prev = prof
shifts = np.array(shifts)
off = -np.cumsum(shifts)  # page row = frame row + off
off -= off.min()
total = int(off.max()) + H
print("frames", len(shifts), "page height", total)

# pass 2: paste, preferring the stillest frame for each page row
canvas = np.full((total, X1 - X0, 3), 250, np.uint8)
qual = np.full(total, 1e9)
motion = np.abs(shifts).astype(float)
motion = np.maximum(motion, np.abs(np.roll(shifts, -1)))
rows = np.arange(Y0, Y1)
for i, f in enumerate(frames(False)):
    p = rows + off[i]
    # tiny preference for the middle of the band so seams land away from its edges
    q = motion[i] + np.abs(rows - (Y0 + Y1) / 2) / 4000
    m = q < qual[p]
    canvas[p[m]] = f[rows[m], X0:X1]
    qual[p[m]] = q[m]
Image.fromarray(canvas).save(OUT, optimize=True)
json.dump({"off": off.tolist(), "Y0": Y0, "X0": X0}, open(OUT.replace(".png", "_off.json"), "w"))
print("saved", OUT)

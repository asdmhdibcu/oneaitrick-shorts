"""Rebuild a web page as one tall, clean image from a phone screen recording (from Short #6, generalised).

Measures the vertical scroll between frames, then pastes only the clean content band (rows Y0..Y1) of every frame
into one canvas, keeping for each page row the frame that moved least. The AssistiveTouch button is found in every
frame (Hough circle, radius ~90 px) and its rows are never taken from that frame. With --xlock, frames that are
scrolled sideways (code views) are skipped.

Usage: python3 stitch_page.py SRC T0 T1 Y0 Y1 OUT.png [--xlock]
Writes OUT.png and OUT_off.json (page row = frame row + off[i] for frame i at 30 fps from T0).
"""
import json
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image

SRC, T0, T1, Y0, Y1, OUT = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
XLOCK = "--xlock" in sys.argv
W, H = 1320, 2868
X0, X1 = 0, W
TM = open("work/tm.txt").read().strip()
LV = open("work/lv.txt").read().strip()


def frames(gray):
    fmt = "gray" if gray else "rgb24"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{T0:.3f}", "-t", f"{T1 - T0:.3f}", "-i", SRC, "-vf",
                          f"fps=30,{TM},{LV},format={fmt}", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    n = W * H * (1 if gray else 3)
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        a = np.frombuffer(b, np.uint8)
        yield a.reshape(H, W) if gray else a.reshape(H, W, 3)


def button(g):
    strip = cv2.GaussianBlur(g[:, 1000:], (5, 5), 1.5)
    c = cv2.HoughCircles(strip, cv2.HOUGH_GRADIENT, dp=1, minDist=200, param1=60, param2=35, minRadius=80, maxRadius=96)
    return None if c is None else int(c[0][0][1])


# pass 1: vertical (and sideways) shift between consecutive frames, and where the button is
shifts, xs, btn, prev, prevc, last = [0], [0], [], None, None, None
for g in frames(True):
    prof = g[Y0:Y1, 40:W - 160].astype(np.float32).mean(1)
    prof = np.concatenate([np.zeros(Y0, np.float32), prof, np.zeros(H - Y1, np.float32)])
    colp = g[Y0 + 100:Y1 - 100, :].astype(np.float32).mean(0)
    by = button(g)
    last = by if by is not None else last
    btn.append(last)
    if prev is not None:
        best = (1e9, 0)
        for s in range(-500, 501):
            a0, a1 = Y0 + 150, Y1 - 150
            if a0 + s < Y0 or a1 + s > Y1:
                continue
            e = np.abs(prev[a0:a1] - prof[a0 + s:a1 + s]).mean()
            if e < best[0]:
                best = (e, s)
        shifts.append(best[1])
        bx = min(range(-60, 61), key=lambda s: np.abs(prevc[100:-100] - np.roll(colp, -s)[100:-100]).mean())
        xs.append(bx)
    prev, prevc = prof, colp
shifts = np.array(shifts)
xoff = np.cumsum(xs)
off = -np.cumsum(shifts)
off -= off.min()
total = int(off.max()) + H
print("frames", len(shifts), "page height", total, "sideways frames", int((np.abs(xoff) > 3).sum()), flush=True)

# pass 2: paste, preferring the stillest frame for each page row, never the button's rows
canvas = np.full((total, X1 - X0, 3), 250, np.uint8)
qual = np.full(total, 1e9)
motion = np.abs(shifts).astype(float)
motion = np.maximum(motion, np.abs(np.roll(shifts, -1)))
rows = np.arange(Y0, Y1)
for i, f in enumerate(frames(False)):
    if XLOCK and abs(xoff[i]) > 3:
        continue
    p = rows + off[i]
    q = motion[i] + np.abs(rows - (Y0 + Y1) / 2) / 4000
    if btn[i] is not None:
        q = np.where(np.abs(rows - btn[i]) < 105, q + 1e6, q)
    m = q < qual[p]
    canvas[p[m]] = f[rows[m], X0:X1]
    qual[p[m]] = q[m]
filled = qual < 1e8
ys = np.where(filled)[0]
canvas = canvas[ys.min():ys.max() + 1]
Image.fromarray(canvas).save(OUT, optimize=True)
json.dump({"off": (off - ys.min()).tolist(), "Y0": Y0, "t0": T0, "unfilled_rows": int((~filled[ys.min():ys.max() + 1]).sum()),
           "button_rows": int((qual[ys.min():ys.max() + 1] >= 1e6).sum())}, open(OUT.replace(".png", "_off.json"), "w"))
print("saved", OUT, canvas.shape, flush=True)

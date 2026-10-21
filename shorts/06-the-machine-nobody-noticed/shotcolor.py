"""Pick a caption highlight colour from a shot's own pixels (dominant saturated hue), made bright enough to read on dark.
Usage: python3 shotcolor.py  -> work/colors.json {shot id: "#rrggbb"} for footage and still shots."""
import colorsys
import json
import subprocess

import numpy as np
from PIL import Image

from edl import SHOTS, H

FALLBACK = "#c8ff4d"


def lum(rgb):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def pick(img):
    a = np.asarray(img.convert("RGB").resize((180, 320))).reshape(-1, 3) / 255.0
    mx, mn = a.max(1), a.min(1)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    keep = (s > 0.35) & (mx > 0.3)
    if keep.mean() < 0.02:
        return None
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in a[keep]])
    hist, edges = np.histogram(hsv[:, 0], bins=36, range=(0, 1), weights=hsv[:, 1] * hsv[:, 2])
    hist = hist + 0.5 * (np.roll(hist, 1) + np.roll(hist, -1))
    h = (edges[hist.argmax()] + 1 / 72) % 1
    for l in np.arange(0.62, 0.86, 0.02):  # brighten until it clears 7:1 against the dark caption shade
        rgb = tuple(int(round(v * 255)) for v in colorsys.hls_to_rgb(h, l, 0.95))
        if (lum(rgb) + 0.05) / (lum((7, 8, 12)) + 0.05) >= 7:
            break
    return "#%02x%02x%02x" % rgb


out = {}
for sid, t0, t1, kind, sp in SHOTS:
    if kind == "V":
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{H + (t1 - t0) / 2:.2f}", "-i", f"assets/clips/{sid}.mp4",
                        "-frames:v", "1", "work/tmp/col.png"], check=True)
        out[sid] = pick(Image.open("work/tmp/col.png")) or FALLBACK
    elif kind == "STILL":
        p = f"assets/img/{sid}.png" if "frame" in sp else f"assets/img/{sid}.jpg"
        out[sid] = pick(Image.open(p)) or None
json.dump(out, open("work/colors.json", "w"), indent=1)
print(out)

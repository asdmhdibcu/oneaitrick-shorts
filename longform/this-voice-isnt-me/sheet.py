"""Contact sheet from 16:9 snapshot PNGs: python3 sheet.py OUT.png COLS t1,t2,... (reads work/snap/at-<t>s.png)"""
import os
import sys

from PIL import Image, ImageDraw

out, cols, ts = sys.argv[1], int(sys.argv[2]), sys.argv[3].split(",")
W, Hh = 480, 270
tiles = []
for t in ts:
    name = "%g" % float(t)
    p = f"work/snap/at-{name}s.png"
    im = Image.open(p).convert("RGB").resize((W, Hh)) if os.path.exists(p) else Image.new("RGB", (W, Hh), "red")
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 60, 16], fill=(0, 0, 0)); d.text((3, 2), name, fill=(255, 255, 0))
    tiles.append(im)
S = Image.new("RGB", (cols * (W + 4), ((len(tiles) + cols - 1) // cols) * (Hh + 4)), "black")
for i, t in enumerate(tiles):
    S.paste(t, ((i % cols) * (W + 4), (i // cols) * (Hh + 4)))
S.save(out); print(out, S.size)

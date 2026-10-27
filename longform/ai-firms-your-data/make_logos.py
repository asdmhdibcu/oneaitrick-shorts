"""#11: the official logos the creator downloaded (work/raw/logos/*), trimmed onto transparency -> assets/logos/<code>.png.
Nothing is redrawn: white or near-white backgrounds become transparent, the mark is trimmed and scaled to 900 px max.
A logo that sits on its own colour (Stability AI's purple) keeps it, and the tile takes that colour (logos.json "bg").
Usage: python3 make_logos.py
"""
import json
import os

import numpy as np
from PIL import Image

A = "/mnt/user-data/attachments/2028a4a7-0d47-5787-9f13-5287c0bff2aa/"
# code: (file, name on screen, keep background)
LOGOS = {
    "L1": ("fc6bc6af-image.webp", "ICO", False),
    "L2": ("30005a5a-image.webp", "OpenAI", False),
    "L5": ("db910740-image.jpg", "Google", False),
    "L7": ("06dba77a-image.png", "Anthropic", False),
    "L8": ("af49be29-image.jpg", "Claude", False),
    "L8s": ("f575ed7b-image.jpg", "Claude", False),
    "L9": ("68e21feb-image.webp", "Amazon", False),
    "L10": ("ec15e626-image.png", "Apple", False),
    "L11": ("80b4bd1d-image.webp", "Microsoft", False),
    "L12": ("403e14c4-image.png", "Cohere", False),
    "L13": ("d9920922-image.webp", "DeepSeek", False),
    "L14": ("f515f095-image.png", "Stability AI", True),
    "L16": ("8989c95a-image.png", "xAI · Grok", False),
}
os.makedirs("assets/logos", exist_ok=True)
meta = {}
for code, (fn, name, keep) in LOGOS.items():
    im = Image.open(A + fn).convert("RGBA")
    a = np.asarray(im).astype(float)
    rgb, al = a[..., :3], a[..., 3]
    bg = None
    if keep:
        bg = "#%02x%02x%02x" % tuple(int(v) for v in np.median(rgb.reshape(-1, 3), axis=0))
    else:
        # near-white (or the page's very light tint) -> transparent, with a soft edge
        corner = np.median(np.concatenate([rgb[:8, :8].reshape(-1, 3), rgb[-8:, -8:].reshape(-1, 3)]), axis=0)
        if al.min() < 250 and (al[:8, :8].mean() < 10):
            pass                                  # already transparent
        elif corner.min() > 225:
            d = np.abs(rgb - corner).max(axis=2)
            al = np.minimum(al, np.clip((d - 6) * 255 / 40, 0, 255))
        a[..., 3] = al
        im = Image.fromarray(a.astype(np.uint8), "RGBA")
        bb = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
        im = im.crop(bb)
    im.thumbnail((900, 900), Image.LANCZOS)
    im.save(f"assets/logos/{code}.png", optimize=True)
    meta[code] = dict(name=name, w=im.width, h=im.height, bg=bg, src=fn)
    print(code, name, im.size, bg or "")
json.dump(meta, open("assets/logos/logos.json", "w"), indent=1)

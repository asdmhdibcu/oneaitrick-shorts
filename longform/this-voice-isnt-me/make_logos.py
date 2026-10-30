"""#12: the official logos -> assets/logos/<code>.png + logos.json. Nothing is redrawn.
SVGs (the creator's Wikimedia Commons / brand-page downloads) are rendered by Chromium onto transparency and trimmed;
PNGs lose their white background. Logos already used in #11 (OpenAI, ChatGPT, Amazon, ICO) are copied from there.
A logo drawn in white (ElevenLabs) sits on a dark tile (logos.json "bg").
Usage: python3 make_logos.py
"""
import asyncio
import json
import os
import shutil

import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

RAW = "work/raw/"
L11 = "../ai-firms-your-data/assets/logos/"
OUT = "assets/logos/"
os.makedirs(OUT, exist_ok=True)
SVG = {"L1": ("L1.svg", "ElevenLabs", "#0b0c10"), "L4": ("L4.svg", "Samsung", None), "L6": ("L6.svg", "Republican National Committee", None),
       "L7": ("L7.svg", "Starling Bank", None), "L8": ("L8.svg", "Federal Trade Commission", None)}
PNG = {"L9": ("L9.png", "Arup", None)}
FROM11 = {"L2": ("L2", "OpenAI"), "L3": ("L3", "ChatGPT"), "L5": ("L9", "Amazon"), "L10": ("L1", "ICO")}


def trim(im):
    bb = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    im = im.crop(bb)
    im.thumbnail((900, 900), Image.LANCZOS)
    return im


async def render_svgs():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1600, "height": 1600})
        for code, (fn, name, bg) in SVG.items():
            html = os.path.abspath(f"work/{code}_svg.html")
            open(html, "w").write(f'<html><body style="margin:0;background:transparent"><img id="i" src="{os.path.abspath(RAW + fn)}" '
                                  f'style="width:1400px;height:auto;display:block" /></body></html>')
            await pg.goto("file://" + html)
            await pg.wait_for_timeout(800)
            await pg.locator("#i").screenshot(path=f"work/{code}_svg.png", omit_background=True)
        await b.close()


asyncio.run(render_svgs())
meta = {}
for code, (fn, name, bg) in SVG.items():
    im = trim(Image.open(f"work/{code}_svg.png").convert("RGBA"))
    im.save(OUT + code + ".png", optimize=True); meta[code] = dict(name=name, w=im.width, h=im.height, bg=bg, src=fn)
for code, (fn, name, bg) in PNG.items():
    im = Image.open(RAW + fn).convert("RGBA")
    a = np.asarray(im).astype(float); rgb = a[..., :3]
    d = (255 - rgb).max(axis=2)                       # white -> transparent, with a soft edge
    a[..., 3] = np.minimum(a[..., 3], np.clip((d - 6) * 255 / 40, 0, 255))
    im = trim(Image.fromarray(a.astype(np.uint8), "RGBA"))
    im.save(OUT + code + ".png", optimize=True); meta[code] = dict(name=name, w=im.width, h=im.height, bg=bg, src=fn)
old = json.load(open(L11 + "logos.json"))
for code, (c11, name) in FROM11.items():
    shutil.copy(L11 + c11 + ".png", OUT + code + ".png")
    meta[code] = dict(name=name, w=old[c11]["w"], h=old[c11]["h"], bg=None, src="#11 " + c11)
json.dump(meta, open(OUT + "logos.json", "w"), indent=1)
for k, v in meta.items():
    print(k, v["name"], v["w"], v["h"], v["bg"] or "")

"""Screen positions of the labelled 3D points, per frame: work/sim3d/<name>_pins.json (same timing as render3d.py)."""
import json, os, sys
from playwright.sync_api import sync_playwright
SCENES = {"helix": 2.7, "walk": 1.8, "jam": 2.9, "pile": 2.9, "fix": 1.85}
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for name, secs in SCENES.items():
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + os.path.abspath("src3d/page.html"))
        pg.evaluate(f"window.setup('{name}')")
        out = [pg.evaluate(f"window.project({i / 30:.5f})") for i in range(int(round(secs * 30)))]
        json.dump(out, open(f"work/sim3d/{name}_pins.json", "w"))
        print(name, len(out), out[0], out[-1])
        pg.close()
    b.close()

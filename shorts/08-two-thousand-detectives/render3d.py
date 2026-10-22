"""Render the 3D shots (src3d/world.js) frame by frame to work/sim/<name>.mp4 (1080x1920, 30 fps).
Build first: npx esbuild src3d/world.js --bundle --format=iife --minify --outfile=src3d/world3d.js
Usage: python3 render3d.py NAME SECONDS [every=1]   (every>1 renders a preview of every Nth frame)
"""
import os, subprocess, sys, time, base64
from playwright.sync_api import sync_playwright

name, secs = sys.argv[1], float(sys.argv[2]); every = int(sys.argv[3]) if len(sys.argv) > 3 else 1
out = f"work/sim3d/{name}"; os.makedirs(out, exist_ok=True)
n = int(round(secs * 30))
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + os.path.abspath("src3d/page.html"))
    pg.evaluate(f"window.setup('{name}')")
    t0 = time.time()
    for i in range(0, n, every):
        pg.evaluate(f"window.frame({i / 30:.5f})")
        data = pg.evaluate("document.querySelector('canvas').toDataURL('image/png')")
        open(f"{out}/f{i:04d}.png", "wb").write(base64.b64decode(data.split(",")[1]))
        if i % 30 == 0:
            print(name, i, "/", n, f"{time.time() - t0:.0f}s", flush=True)
    b.close()
if every == 1:
    os.makedirs("work/sim", exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{out}/f%04d.png", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
                    "-pix_fmt", "yuv420p", f"work/sim/{name}.mp4"], check=True)
    print("work/sim/%s.mp4" % name)

"""#12 packaging: render the Instagram carousel (10 slides, 1080x1350), the Short's cover (1080x1920) and the video's YouTube
thumbnail (1280x720) from pack/*.html. The backgrounds are stills pulled from the video's material (git-ignored work/raw).
Writes renders/carousel/12-carousel-01.png ... -10.png, renders/short12-cover.png, renders/video12-thumbnail.jpg.
Usage: python3 make_pack.py
"""
import os
import subprocess

from playwright.sync_api import sync_playwright

from edl import R

HERE = os.path.dirname(os.path.abspath(__file__))
STILLS = {"car_voice": ("g4_voice.mp4", 0.6), "car_phone": ("s19.mp4", 0.5), "car_worry": ("s10.mp4", 0.6),
          "car_call": ("g5_call.mp4", 0.6), "car_family": ("s15.mp4", 0.3)}
os.makedirs("assets/img", exist_ok=True); os.makedirs("renders/carousel", exist_ok=True)
for name, (f, at) in STILLS.items():
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", R + f], capture_output=True, text=True).stdout)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d * at:.2f}", "-i", R + f, "-frames:v", "1", "-q:v", "2", f"assets/img/{name}.jpg"], check=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 1400}, device_scale_factor=1)
    pg.goto(f"file://{HERE}/pack/carousel.html"); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
    for i in range(1, 11):
        pg.locator(f"#c{i:02d}").screenshot(path=f"renders/carousel/12-carousel-{i:02d}.png")
    pg.goto(f"file://{HERE}/pack/cover12.html"); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    pg.locator("#cover").screenshot(path="renders/short12-cover.png")
    pg.goto(f"file://{HERE}/pack/thumb12.html"); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    pg.locator("#thumb").screenshot(path="renders/video12-thumbnail.jpg", type="jpeg", quality=92)
    b.close()
print("renders/carousel (10), renders/short12-cover.png, renders/video12-thumbnail.jpg")

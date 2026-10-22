import os, sys, json
from playwright.sync_api import sync_playwright
names = sys.argv[1].split(",")
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for n in names:
        pg = b.new_page(viewport={"width": 1080, "height": 1920}); pg.goto("file://" + os.path.abspath("src3d/page.html")); pg.evaluate(f"window.setup('{n}')")
        for t in (0, 0.9, 1.7, 2.8):
            o = pg.evaluate(f"window.project({t})"); print(n, t, {k: v for k, v in o.items() if k in ('head', 'arm', 'cargo', 'heap', 'dest', 'cut')})
        pg.close()
    b.close()

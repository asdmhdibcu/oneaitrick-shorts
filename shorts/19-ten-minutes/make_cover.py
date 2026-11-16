"""Short #19 cover: the pencil (GRIT on its barrel) wobbling as its turquoise training wheels fly off, in the same
Mid-century Cartoon drawing code as the film (toon19.js + film19.js), with the claim. Everything sits inside y 240-1680
(Instagram's grid crop). Writes cover19.html and short19-cover.png (Playwright). Usage: python3 make_cover.py
"""
import json
import os

from playwright.sync_api import sync_playwright

words = json.load(open("words.json"))
WS = [round(x["start"], 3) for x in words]
DUR = round(words[-1]["end"] + 0.1, 2)
toon = open("toon19.js").read()
film = open("film19.js").read().replace("PAINT.push(paint);", "")
html = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: "Jost"; src: url("assets/fonts/jost-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Jost"; src: url("assets/fonts/jost-latin-600-normal.woff2") format("woff2"); font-weight: 600; }
@font-face { font-family: "Oleo Script"; src: url("assets/fonts/oleo-script-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Alfa Slab One"; src: url("assets/fonts/alfa-slab-one-latin-400-normal.woff2") format("woff2"); }
html, body { margin: 0; width: 1080px; height: 1920px; background: #F4EAD5; }
</style></head><body><canvas id="film" width="1080" height="1920"></canvas>
<script>
const WS = %WS%, DUR = %DUR%, PAGES = {}, PAINT = [];
const w = (k) => WS[k];
%TOON%
%FILM%
async function cover() {
  await Promise.all(["700 40px Jost", "600 40px Jost", "700 40px 'Oleo Script'", "40px 'Alfa Slab One'"].map((f) => document.fonts.load(f)));
  const T = 20.0;
  setClock(T);
  X.fillStyle = C.paper; X.fillRect(0, 0, W, H);
  // the stage, a little bigger than in the film, centred in the grid-safe area
  X.save(); X.translate(540, 900); X.scale(1.08, 1.08); X.translate(-540, -700);
  shape(X, circ(520, 640, 360, 60), { fill: C.paperD, line: 0, grain: 0.2, off: [0, 0] });
  rays(X, 520, 640, 30, 640, "rgba(243,211,127,0.45)", { rot: 0.3, r0: 60 });
  floor(T, 0, -300, 1400, G.y, 501, 0);
  X.save(); X.translate(550, G.y); X.rotate(-0.08); X.translate(-550, -G.y);
  rider(T, { p: 40, ex: "worried", tw: 1, twx: -170, twy: -190, twr: 1.2, twa: 1 });
  for (let i = 0; i < 3; i++) ink(X, [[G.TW[0] - 120 + i * 10, G.TW[1] - 250 + i * 34], [G.TW[0] - 60 + i * 10, G.TW[1] - 232 + i * 34]], 5, { seed: 600 + i });
  X.restore();
  timer(790, 430, 0, T, 0);
  X.restore();
  // chrome inside the crop
  X.font = SANS(28, 700); X.letterSpacing = "2px"; const tw = X.measureText("AI PAPER · STORY").width; X.letterSpacing = "0px";
  shape(X, rrect(60, 262, tw + 84, 60, 30), { fill: C.white, line: 3, seed: 361, breaks: 0.08 });
  shape(X, circ(94, 292, 10, 14), { fill: "#FF7AC6", line: 2.5, seed: 362, breaks: 0 });
  text(X, "AI PAPER · STORY", 118, 302, { font: SANS(28, 700), fill: C.ink, track: 2 });
  text(X, "@ONEAITRICK", 1020, 302, { font: SANS(26, 700), fill: C.ink, align: "right", track: 2, alpha: 0.8 });
  // the claim
  text(X, "10 MINUTES OF AI...", 540, 440, { font: SLAB(86), fill: C.ink, plate: C.mustardL, align: "center", seed: 382 });
  shape(X, rrect(70, 1290, 940, 330, 34), { fill: C.white, line: 6, seed: 381, breaks: 0.08 });
  text(X, "THEN THEY GAVE UP", 540, 1400, { font: SLAB(80), fill: C.ink, plate: C.mustardL, align: "center", seed: 383, maxW: 860 });
  text(X, "ALMOST 2× AS OFTEN", 540, 1512, { font: SLAB(84), fill: C.ink, plate: C.tomatoL, align: "center", seed: 384, maxW: 860 });
  text(X, "1,222 PEOPLE · PEER-REVIEWED STUDY", 540, 1590, { font: SANS(30, 700), fill: C.inkSoft, align: "center", track: 2 });
  paperFinish(X, W, H, 1);
  document.title = "ready";
}
cover();
</script></body></html>"""
html = html.replace("%WS%", json.dumps(WS)).replace("%DUR%", str(DUR)).replace("%TOON%", toon).replace("%FILM%", film)
open("cover19.html", "w").write(html)
exe = [p for p in os.popen("ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell").read().split()][0]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=exe, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + os.path.abspath("cover19.html"))
    pg.wait_for_function("document.title === 'ready'", timeout=30000)
    pg.screenshot(path="short19-cover.png")
    b.close()
print("short19-cover.png")

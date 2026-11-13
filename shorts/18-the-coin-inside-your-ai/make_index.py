"""Short #18: index_template.tpl + fx18.js + words.json (+ crops.json, the Anthropic logo) -> index.html.
Usage: python3 make_index.py
"""
import json, re

DUR = 56.95
words = json.load(open("words.json"))
WS = [round(x["start"], 3) for x in words]
WE = [round(x["end"], 3) for x in words]
PAGES = json.load(open("crops.json"))


def svg_inner(path, col):
    s = open(path).read()
    s = re.sub(r"<title>.*?</title>", "", s)
    return s.replace("<svg ", f'<svg style="color:{col}" fill="currentColor" ', 1)


LOGOS = {"anthropic": {"svg": svg_inner("assets/logos/anthropic.svg", "#141413"), "word": "Anthropic", "fs": 44},
         "amark": {"svg": svg_inner("assets/logos/anthropic.svg", "#141413")}}

# keyword pops (MOTION.md, from #18): the word bounces 100-115-100 % on a coloured box; amber for the planted coin, lime for the fix
# (the critic's pass added the first ONE, 86, OWN and YOU'D)
POPS = [{"t": WS[7], "col": "#ffb547"}, {"t": WS[40], "col": "#ffb547"}, {"t": WS[49], "col": "#c8ff4d"}, {"t": WS[96], "col": "#ffb547"},
        {"t": WS[103], "col": "#ffb547"}, {"t": WS[124], "col": "#c8ff4d"}, {"t": WS[136], "col": "#c8ff4d"}, {"t": WS[160], "col": "#c8ff4d"}]

# caption fixes: the stressed number words show as digits
caps = json.loads(open("captions.js").read().split("=", 1)[1].rstrip().rstrip(";"))
for ch in caps:
    for x in ch["w"]:
        if x["d"] == "EIGHTY-SIX":
            x["d"] = "86"
        if x["d"] == "ONE" and abs(x["s"] - WS[85]) < 0.05:
            x["d"] = "1"
# phrase chunks that keep a number with its unit and a phrase in one piece (word index ranges -> chunk sizes)
REGROUP = [(0, 5, [3, 1, 2]),          # A COIN FLIP / STEERED / 50 EXPERTS
           (6, 10, [4, 1]),            # NOT ONE OF THEM / KNEW
           (29, 32, [2, 2]),           # BOTH OPTIONS / ARE FAIR
           (42, 53, [2, 3, 2, 2, 3]),  # THE EXPERTS / WENT WITH THE / COIN'S SIDE / 86 PERCENT / OF THE TIME
           (73, 76, [2, 2]),           # HERE'S THE / WEIRD PART
           (111, 117, [4, 3]),         # SO ASK YOUR AI / ONE MORE THING
           (152, 158, [2, 2, 1, 2])]   # FOLLOW FOR / MORE AI / EXPLAINED / LIKE THIS
flat = [x for ch in caps for x in ch["w"]]
groups, k = [], 0
for ch in caps:
    groups.append(list(range(k, k + len(ch["w"])))); k += len(ch["w"])
assert k == len(WS), (k, len(WS))
for a, b, sizes in REGROUP:
    hit = [g for g in groups if g[0] <= b and g[-1] >= a]
    assert [i for g in hit for i in g] == list(range(a, b + 1)), (a, b, hit)
    assert sum(sizes) == b - a + 1
    i0 = groups.index(hit[0])
    new, j = [], a
    for n in sizes:
        new.append(list(range(j, j + n))); j += n
    groups[i0:i0 + len(hit)] = new
caps = []
for gi, g in enumerate(groups):
    t0 = round(flat[g[0]]["s"] - 0.06, 3)
    caps.append({"t0": t0, "w": [flat[i] for i in g]})
for gi, ch in enumerate(caps):
    end = ch["w"][-1]["e"] + 0.55
    ch["t1"] = round(min(caps[gi + 1]["t0"], end) if gi + 1 < len(caps) else end, 3)
open("captions.js", "w").write("window.CAPS = " + json.dumps(caps) + ";\n")

html = open("index_template.tpl").read()
fx = open("fx18.js").read()
html = (html.replace("%FXJS%", fx).replace("%DUR%", str(DUR)).replace("%WS%", json.dumps(WS)).replace("%WE%", json.dumps(WE))
        .replace("%PAGES%", json.dumps(PAGES)).replace("%LOGOS%", json.dumps(LOGOS)).replace("%POPS%", json.dumps(POPS)))
open("index.html", "w").write(html)
print("index.html", len(html), "bytes; pages:", list(PAGES), "pops:", [round(p["t"], 2) for p in POPS])

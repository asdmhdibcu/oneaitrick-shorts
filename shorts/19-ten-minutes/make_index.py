"""Short #19: index_template.tpl + toon19.js + film19.js + words.json (+ crops.json) -> index.html.
The picture is one canvas painted from the clock (film19.js, in Lemo-Opuscar's Mid-century Cartoon style, toon19.js);
the captions and the end card are DOM. Usage: python3 make_index.py
"""
import json

words = json.load(open("words.json"))
WS = [round(x["start"], 3) for x in words]
WE = [round(x["end"], 3) for x in words]
DUR = round(WE[-1] + 0.1, 2)          # cut 0.1 s after "was", so a replay runs straight into the hook
PAGES = json.load(open("crops.json"))

TOM, TEAL, MUS = "#E0533A", "#3FA7A0", "#E8B43A"
# keyword pops: the word bounces 100-115-100 % on a coloured box (tomato for giving up, turquoise for the AI, mustard for the hero)
POPS = [{"t": WS[9], "col": TOM}, {"t": WS[17], "col": TEAL}, {"t": WS[36], "col": TOM}, {"t": WS[40], "col": TOM},
        {"t": WS[51], "col": TOM}, {"t": WS[67], "col": TOM}, {"t": WS[75], "col": MUS}, {"t": WS[92], "col": TEAL},
        {"t": WS[121], "col": TEAL}]

caps = json.loads(open("captions.js").read().split("=", 1)[1].rstrip().rstrip(";"))
# phrase chunks (word index ranges -> chunk sizes), at most 4 words
REGROUP = [(0, 3, [4]), (4, 11, [4, 4]), (25, 29, [2, 3]), (37, 47, [3, 2, 3, 3]), (48, 55, [4, 2, 2]), (56, 57, [2]),
           (58, 67, [2, 2, 3, 2, 1]), (68, 82, [2, 3, 2, 2, 3, 3]), (83, 86, [2, 2]), (87, 101, [3, 3, 4, 2, 3]),
           (102, 114, [2, 2, 4, 3, 2]), (115, 125, [4, 4, 3]), (126, 135, [3, 4, 3]), (151, 157, [4, 3]), (158, 163, [2, 4])]
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
for g in groups:
    caps.append({"t0": round(flat[g[0]]["s"] - 0.06, 3), "w": [flat[i] for i in g]})
for gi, ch in enumerate(caps):
    end = ch["w"][-1]["e"] + 0.55
    ch["t1"] = round(min(caps[gi + 1]["t0"], end) if gi + 1 < len(caps) else min(end, DUR), 3)
open("captions_final.js", "w").write("window.CAPS = " + json.dumps(caps) + ";\n")

html = open("index_template.tpl").read()
html = (html.replace("%TOONJS%", open("toon19.js").read()).replace("%FILMJS%", open("film19.js").read())
        .replace("%DUR%", str(DUR)).replace("%WS%", json.dumps(WS)).replace("%WE%", json.dumps(WE))
        .replace("%PAGES%", json.dumps(PAGES)).replace("%POPS%", json.dumps(POPS)))
open("index.html", "w").write(html)
print("index.html", len(html), "bytes; DUR", DUR, "; chunks", len(caps))

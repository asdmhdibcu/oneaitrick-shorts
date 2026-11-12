"""Short #17: index_template.tpl + fx17.js + words.json (+ crops.json, logos) -> index.html.
Usage: python3 make_index.py
"""
import json, os, re

DUR = 81.5
words = json.load(open("words.json"))
WS = [round(x["start"], 3) for x in words]
WE = [round(x["end"], 3) for x in words]

NAMES = {"p01": "Hiya, 'AI is making voice fraud worse'", "p02": "ElevenLabs help, voice samples for Instant Voice Cloning",
         "p03": "Cord Cutters News on NordVPN's study", "p04a": "FTC, 'What's a verification code…' (doorknob and deadbolt)",
         "p04b": "FTC, 'What's a verification code…' (anyone who asks)", "p05": "FBI alert I-120324-PSA"}
crops = json.load(open("crops.json")) if os.path.exists("crops.json") else {}
PAGES = {}
for k, name in NAMES.items():
    c = crops.get(k)
    PAGES[k] = dict(c, have=True, name=name) if c else {"have": False, "name": name}


def svg_inner(path, col):
    s = open(path).read()
    s = re.sub(r"<title>.*?</title>", "", s)
    return s.replace("<svg ", f'<svg style="color:{col}" ', 1)


LOGOS = {
    "elevenlabs": {"have": True, "svg": svg_inner("assets/logos/elevenlabs.svg", "#000"), "word": "ElevenLabs", "fs": 64},
    "nordvpn": {"have": True, "svg": svg_inner("assets/logos/nordvpn.svg", "#4687FF"), "word": "NordVPN", "fs": 64},
}
for ext in ("png", "svg"):
    f = f"assets/logos/hiya.{ext}"
    if os.path.exists(f):
        LOGOS["hiya"] = {"have": True, "img": f}
        if ext == "svg":
            LOGOS["hiya"] = {"have": True, "svg": svg_inner(f, "#000")}
LOGOS.setdefault("hiya", {"have": False})

# caption fixes: stressed number words (in CAPS in the script) become digits too
caps = open("captions.js").read()
for a, b in (('"ONE"', '"1"'), ('"THIRTY"', '"30"'), ('"SEVEN"', '"7"')):
    caps = caps.replace('"d": ' + a, '"d": ' + b)
open("captions.js", "w").write(caps)

html = open("index_template.tpl").read()
fx = open("fx17.js").read()
html = (html.replace("%FXJS%", fx).replace("%DUR%", str(DUR)).replace("%WS%", json.dumps(WS)).replace("%WE%", json.dumps(WE))
        .replace("%V01S%", str(round(WS[73] - 0.2, 3))).replace("%PAGES%", json.dumps(PAGES)).replace("%LOGOS%", json.dumps(LOGOS)))
open("index.html", "w").write(html)
print("index.html", len(html), "bytes; pages:", [k for k, v in PAGES.items() if v["have"]], "logos:", [k for k, v in LOGOS.items() if v["have"]])

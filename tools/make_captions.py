"""Turn aligned words (words.json from align.py) into karaoke caption chunks for the composition.

Usage: python3 make_captions.py words.json captions.js "EMPH,WORDS,IN,CAPS" [fix.json]
Writes: window.CAPS = [{t0, t1, w: [{d, s, e, emph}]}]
  d = display text (uppercase, number words -> digits), s/e = word start/end (s), emph = highlight word.
Rules: a chunk breaks after punctuation, at 3 words, or before it would pass 16 characters.
A chunk shows from its first word - 0.06 s until min(next chunk start - 0.02, last word end + 0.55).
fix.json (optional): {"WORD@approx_start": [start, end]} to correct a mis-aligned word,
  e.g. {"But@12.87": [13.58, 13.86]} when the aligner puts a word inside a laugh or breath.
"""
import json
import re
import sys

NUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
       "nine": "9", "ten": "10", "twenty": "20", "thirty": "30", "forty": "40", "fifty": "50", "hundred": "100",
       "thirty-five": "35"}

words = json.load(open(sys.argv[1]))
emph = set(x.strip().upper() for x in sys.argv[3].split(",") if x.strip()) if len(sys.argv) > 3 else set()
fix = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {}
for key, (s, e) in fix.items():
    name, at = key.split("@")
    for w in words:
        if w["text"].strip(".,?!") == name and abs(w["start"] - float(at)) < 0.3:
            w["start"], w["end"] = s, e


def display(t):
    core = re.sub(r"[^\w'-]", "", t)
    low = core.lower()
    # keep "one" as a word when it isn't a count ("one look", "one doctor" reads fine either way)
    d = NUM.get(low, core) if low != "one" else core
    q = "?" if t.rstrip().endswith("?") else ""
    return d.upper() + q


chunks, cur = [], []
for i, w in enumerate(words):
    d = display(w["text"])
    if not d.strip("?"):
        continue
    if cur and len(" ".join(x["d"] for x in cur) + " " + d) > 16:
        chunks.append(cur)
        cur = []
    cur.append({"d": d, "s": round(w["start"], 3), "e": round(w["end"], 3), "emph": d in emph})
    punct = re.search(r"[.,?!;:]$|\.\.\.$", w["text"]) is not None
    if punct or len(cur) >= 3 or i == len(words) - 1:
        chunks.append(cur)
        cur = []

out = []
for k, c in enumerate(chunks):
    t0 = max(c[0]["s"] - 0.06, 0)
    t1 = c[-1]["e"] + 0.55
    if k + 1 < len(chunks):
        t1 = min(t1, chunks[k + 1][0]["s"] - 0.02)
    out.append({"t0": round(t0, 3), "t1": round(t1, 3), "w": c})
open(sys.argv[2], "w").write("window.CAPS = " + json.dumps(out) + ";\n")
print(len(out), "chunks")

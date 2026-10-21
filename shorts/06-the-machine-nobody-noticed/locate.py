"""Find where a phrase sits in an OCR'd image, as one box per text line (source pixels).
Page words come from ocr_page.py; screenshots are OCR'd on first use and cached in work/ocr_<name>.json."""
import json
import os
import re

import pytesseract
from PIL import Image


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower().replace("’", "'"))


def words_for(name):
    if name == "page":
        return json.load(open("work/page_words.json"))
    cache = f"work/ocr_{name}.json"
    if not os.path.exists(cache):
        d = pytesseract.image_to_data(Image.open("work/img/" + name).convert("L"), output_type=pytesseract.Output.DICT)
        ws = [{"t": t, "x": d["left"][i], "y": d["top"][i], "w": d["width"][i], "h": d["height"][i]}
              for i, t in enumerate(d["text"]) if t.strip() and float(d["conf"][i]) > 30]
        json.dump(ws, open(cache, "w"))
    return json.load(open(cache))


def lines_of(ws):
    ws = sorted(ws, key=lambda w: (w["y"] + w["h"] / 2))
    lines = []
    for w in ws:
        cy = w["y"] + w["h"] / 2
        if lines and abs(cy - lines[-1]["cy"]) < max(12, w["h"] * 0.45):
            lines[-1]["ws"].append(w)
        else:
            lines.append({"cy": cy, "ws": [w]})
    out = []
    for ln in lines:
        out.extend(sorted(ln["ws"], key=lambda w: w["x"]))
    return out


def locate(name, phrase, near_y=None, y0=0, y1=10 ** 9):
    ws = [w for w in lines_of(words_for(name)) if y0 <= w["y"] <= y1]
    toks = [norm(t) for t in phrase.split() if norm(t)]
    seq = [norm(w["t"]) for w in ws]
    hits = []
    for i in range(len(seq)):
        j, k = i, 0
        while k < len(toks) and j < len(seq):
            if not seq[j]:
                j += 1; continue
            if seq[j] == toks[k] or (k in (0, len(toks) - 1) and toks[k] in seq[j]):
                j += 1; k += 1
            else:
                break
        if k == len(toks):
            hits.append(ws[i:j])
    if not hits:
        raise SystemExit(f"phrase not found: {phrase!r} in {name}")
    if near_y is not None:
        hits.sort(key=lambda h: abs(h[0]["y"] - near_y))
    hit = hits[0]
    boxes = []
    for w in hit:  # merge words on the same line
        if boxes and abs((w["y"] + w["h"] / 2) - (boxes[-1][1] + boxes[-1][3] / 2)) < w["h"] * 0.6:
            x0, y0_, x1, y1_ = boxes[-1][0], boxes[-1][1], boxes[-1][0] + boxes[-1][2], boxes[-1][1] + boxes[-1][3]
            x0, y0_ = min(x0, w["x"]), min(y0_, w["y"]); x1, y1_ = max(x1, w["x"] + w["w"]), max(y1_, w["y"] + w["h"])
            boxes[-1] = (x0, y0_, x1 - x0, y1_ - y0_)
        else:
            boxes.append((w["x"], w["y"], w["w"], w["h"]))
    return boxes


if __name__ == "__main__":
    import sys
    print(locate(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else None))

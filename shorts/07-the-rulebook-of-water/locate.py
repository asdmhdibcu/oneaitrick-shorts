"""Find where a phrase sits in a source, as one box per text line (source pixels).

Sources: "pdf:oa:5" (word boxes from pdfwords.py, page 5, 300 dpi), "page:quanta_a" (a stitched page, OCR'd once
and cached), or an image file name in work/img (OCR'd once and cached).
"""
import json
import os
import re

import pytesseract
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def norm(t):
    t = t.lower().replace("’", "'").replace("‘", "'").replace("–", "-").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9$]", "", t)


def ocr(path, cache):
    if not os.path.exists(cache):
        im = Image.open(path).convert("L")
        out, step = [], 1800
        for y0 in range(0, im.size[1], step):
            crop = im.crop((0, y0, im.size[0], min(im.size[1], y0 + step + 200)))
            d = pytesseract.image_to_data(crop, output_type=pytesseract.Output.DICT, config="--psm 3")
            for i, t in enumerate(d["text"]):
                if not t.strip() or float(d["conf"][i]) < 30:
                    continue
                if d["top"][i] >= step and y0 + step < im.size[1]:
                    continue
                out.append({"t": t, "x": d["left"][i], "y": d["top"][i] + y0, "w": d["width"][i], "h": d["height"][i]})
        json.dump(out, open(cache, "w"))
    return json.load(open(cache))


def words_for(name):
    if name.startswith("pdf:"):
        _, doc, page = name.split(":")
        return [w for w in json.load(open(f"work/pdf/{doc}_words.json")) if w["p"] == int(page)]
    if name.startswith("page:"):
        n = name.split(":")[1]
        return ocr(f"work/pages/{n}.png", f"work/pages/{n}_ocr.json")
    return ocr("work/img/" + name, f"work/tmp/ocr_{name}.json")


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
                j += 1
                continue
            if seq[j] == toks[k] or (k in (0, len(toks) - 1) and toks[k] in seq[j]):
                j += 1
                k += 1
            else:
                break
        if k == len(toks):
            hits.append(ws[i:j])
    if not hits:
        raise SystemExit(f"phrase not found: {phrase!r} in {name}")
    if near_y is not None:
        hits.sort(key=lambda h: abs(h[0]["y"] - near_y))
    boxes = []
    for w in hits[0]:
        if boxes and abs((w["y"] + w["h"] / 2) - (boxes[-1][1] + boxes[-1][3] / 2)) < w["h"] * 0.6:
            x0, yy0 = boxes[-1][0], boxes[-1][1]
            x1, yy1 = x0 + boxes[-1][2], yy0 + boxes[-1][3]
            x0, yy0 = min(x0, w["x"]), min(yy0, w["y"])
            x1, yy1 = max(x1, w["x"] + w["w"]), max(yy1, w["y"] + w["h"])
            boxes[-1] = (x0, yy0, x1 - x0, yy1 - yy0)
        else:
            boxes.append((w["x"], w["y"], w["w"], w["h"]))
    return boxes


if __name__ == "__main__":
    import sys
    print(locate(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else None))

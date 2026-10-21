"""OCR the stitched page (work/page.png) once, so highlights can be placed on exact words.
Writes work/page_words.json: [{t, x, y, w, h, line}] in page pixels."""
import json
import pytesseract
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
im = Image.open("work/page.png").convert("L")
W, Hh = im.size
out, step, lid = [], 1800, 0
for y0 in range(0, Hh, step):
    crop = im.crop((0, y0, W, min(Hh, y0 + step + 200)))
    d = pytesseract.image_to_data(crop, output_type=pytesseract.Output.DICT, config="--psm 3")
    seen = {}
    for i, t in enumerate(d["text"]):
        if not t.strip() or float(d["conf"][i]) < 30:
            continue
        y = d["top"][i] + y0
        if d["top"][i] >= step and y0 + step < Hh:  # belongs to the next chunk
            continue
        key = (d["block_num"][i], d["par_num"][i], d["line_num"][i])
        if key not in seen:
            seen[key] = lid; lid += 1
        out.append({"t": t, "x": d["left"][i], "y": y, "w": d["width"][i], "h": d["height"][i], "line": seen[key]})
json.dump(out, open("work/page_words.json", "w"))
print(len(out), "words")

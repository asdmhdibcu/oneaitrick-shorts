"""Short #17: cut the real pages into cards (assets/pages/*.png) and find the words to highlight on them.

The creator saves each page as a PDF from Safari Reader (work/pdf/, git-ignored). Each card is a slice of one page, from
the line that holds `first` to the line that holds `last`, across the text column; cuts fall halfway between lines, so
no part-line and no browser header or footer reaches the video. `hl` phrases get their line boxes in card pixels.
Writes crops.json (read by make_index.py): {key: {img, w, h, hl: [[x, y, w, h], ...], label}}.
Usage: python3 crops.py
"""
import html
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "work/pdf") + "/"
OUT = os.path.join(HERE, "assets/pages") + "/"
DPI = 440
S = DPI / 72.0

# key: (pdf, first line contains, last line contains, highlight phrases, extra pt above/below, x range in pt or None, label)
CARDS = {
    "p01": ("p01_hiya.pdf", "nearly one in three respondents", "nearly one in three respondents",
            ["nearly one in three respondents (31%)"], (8, 8), None, "HIYA SURVEY · 12,000 PEOPLE · 6 COUNTRIES"),
    "p02": ("p02_elevenlabs.pdf", "only 30 seconds", "only 30 seconds",
            ["samples of only 30 seconds and get excellent results"], (8, 8), None, "ELEVENLABS HELP CENTER"),
    "p03": ("p03_cordcutters.pdf", "grew 7.4 times", "grew 7.4 times",
            ["grew 7.4 times"], (8, 8), None, "CORD CUTTERS NEWS · 25 OCT 2026"),
    "p04a": ("p04_ftc_code.pdf", "doorknob", "doorknob",
             ["like the lock on your doorknob and a deadbolt lock."], (8, 8), None, "FTC · CONSUMER ALERT · 7 MAR 2024"),
    "p04b": ("p04_ftc_code.pdf", "Anyone who asks you for your account", "Anyone who asks you for your account",
             ["Anyone who asks you for your account verification code is a scammer."], (8, 8), None, "FTC · CONSUMER ALERT · 7 MAR 2024"),
    "p05": ("p05_fbi_psa.pdf", "Create a secret word or phrase", "Create a secret word or phrase",
            ["Create a secret word or phrase with your family to verify their identity."], (8, 8), None, "FBI · ALERT I-120324-PSA · 3 DEC 2024"),
}


def bbox_xml(pdf):
    cache = os.path.join(HERE, "work", os.path.basename(pdf) + ".bbox.html")
    if not os.path.exists(cache):
        subprocess.run(["pdftotext", "-bbox-layout", PDF + pdf, cache], check=True)
    return open(cache, encoding="utf-8").read()


def lines_of(pdf):
    """[(page, xMin, yMin, xMax, yMax, text, [(word, x0, y0, x1, y1)])] in points."""
    x = bbox_xml(pdf)
    out = []
    for p, page in enumerate(re.split(r"<page ", x)[1:], start=1):
        for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', page, re.S):
            words = [(html.unescape(w[4]), float(w[0]), float(w[1]), float(w[2]), float(w[3])) for w in
                     re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', m.group(5))]
            out.append((p, float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)),
                        " ".join(w[0] for w in words), words))
    return out


def norm(s):
    return re.sub(r"\s+", " ", s.replace("“", '"').replace("”", '"').replace("’", "'")).strip()


def find(lines, phrase, after=0):
    for i in range(after, len(lines)):
        if norm(phrase) in norm(lines[i][5]):
            return i
    raise SystemExit(f"not found: {phrase!r}")


def phrase_boxes(lines, i0, i1, phrase):
    """Line boxes (pt) that cover `phrase`, which may run across lines."""
    words = [(w, li) for li in range(i0, i1 + 1) for w in lines[li][6]]
    q = lambda s: norm(s).strip('"\'')
    toks = [q(t) for t in norm(phrase).split(" ")]
    flat = [q(w[0][0]) for w in words]
    for s in range(len(flat) - len(toks) + 1):
        if flat[s:s + len(toks)] == toks:
            sel = words[s:s + len(toks)]
            boxes = {}
            for (w, x0, y0, x1, y1), li in sel:
                b = boxes.setdefault(li, [x0, y0, x1, y1])
                b[0], b[1], b[2], b[3] = min(b[0], x0), min(b[1], y0), max(b[2], x1), max(b[3], y1)
            return [boxes[k] for k in sorted(boxes)]
    raise SystemExit(f"phrase not found on card: {phrase!r}")


def render(pdf, page, x0, y0, x1, y1, out):
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(DPI), "-png", "-singlefile",
                    "-x", str(round(x0 * S)), "-y", str(round(y0 * S)), "-W", str(round((x1 - x0) * S)), "-H", str(round((y1 - y0) * S)),
                    PDF + pdf, out[:-4]], check=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for name, (pdf, first, last, hls, (pa, pb), xr, label) in CARDS.items():
        if not os.path.exists(PDF + pdf):
            print(f"{name:5s} missing {pdf}"); continue
        L = lines_of(pdf)
        i0 = find(L, first)
        i1 = find(L, last, i0)
        page = L[i0][0]
        assert L[i1][0] == page, (name, "spans pages")
        col = [l for l in L[i0:i1 + 1]]
        x0 = (xr[0] if xr else min(l[1] for l in col)) - 14
        x1 = (xr[1] if xr else max(l[3] for l in col)) + 14
        prev = L[i0 - 1] if i0 > 0 and L[i0 - 1][0] == page else None
        nxt = L[i1 + 1] if i1 + 1 < len(L) and L[i1 + 1][0] == page else None
        y0 = L[i0][2] - pa
        if prev and L[i0][2] - prev[4] < 2 * pa + 4:
            y0 = (prev[4] + L[i0][2]) / 2
        y1 = L[i1][4] + pb
        if nxt and nxt[2] - L[i1][4] < 2 * pb + 4:
            y1 = (L[i1][4] + nxt[2]) / 2
        render(pdf, page, x0, y0, x1, y1, OUT + name + ".png")
        boxes = []
        for ph in hls:
            for b in phrase_boxes(L, i0, i1, ph):
                boxes.append([round((b[0] - x0) * S), round((b[1] - y0) * S), round((b[2] - b[0]) * S), round((b[3] - b[1]) * S)])
        meta[name] = {"img": "assets/pages/" + name + ".png", "w": round((x1 - x0) * S), "h": round((y1 - y0) * S), "hl": boxes, "label": label}
        print(f"{name:5s} p{page} {meta[name]['w']}x{meta[name]['h']}  {len(boxes)} box(es)")
    json.dump(meta, open(os.path.join(HERE, "crops.json"), "w"), indent=1)

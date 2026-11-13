"""Short #18: cut the real pages into cards (assets/pages/*.png) and find the words to highlight on them.

The creator saves each page as a PDF from Safari Reader (work/pdf/, git-ignored). Each card is a slice of one page, from
the line that holds `first` to the line that holds `last`, across the text column; cuts fall halfway between lines, so
no part-line and no browser header or footer reaches the video. `hl` phrases get their line boxes in card pixels.
REFLOW cards (from the critic's pass, 12 Nov): one complete sentence, from the word run that starts with `first` to the
run that ends with `last`, re-set as lines of word images cut from the page itself (each word keeps its own pixels;
only the line breaks change), so a short card shows the whole sentence large, with no pan and no cut word.
Writes crops.json (read by make_index.py): {key: {img, w, h, hl: [[x, y, w, h], ...], label, whole}}.
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
CARDS = {}
# key: (pdf, first words, last words, highlight phrases, line width in line-heights, label)
REFLOW = {
    "p01a": ("p01_anthropic_post.pdf", "analysts went with their agent's lean", "we'd expect about 50%.",
             ["lean 86% of the time.", "about 50%."], 12.5, "ANTHROPIC \u00b7 27 OCT 2026"),
    "p01b": ("p01_anthropic_post.pdf", "We studied one task, in one field,", "ran on Claude Opus 4.8.",
             ["with one model.", "ran on Claude Opus 4.8."], 13.5, "ANTHROPIC \u00b7 LIMITATIONS"),
    "p01c": ("p01_anthropic_post.pdf", "We deliberately strengthened", "the agents' lean.",
             ["We deliberately strengthened the agents' lean."], 11.5, "ANTHROPIC \u00b7 LIMITATIONS"),
}
OLD_CARDS = {
    "p01a": ("p01_anthropic_post.pdf", "Across the four analytical choices, analysts went", "we\'d expect about 50%",
             ["lean 86%", "of the time.", "about 50%."], (8, 8), None, "ANTHROPIC \u00b7 27 OCT 2026"),
    "p01b": ("p01_anthropic_post.pdf", "version of the VS Code editor with Claude Code", "Opus 4.8 at High",
             ["running Claude", "Opus 4.8"], (8, 8), None, "ANTHROPIC \u00b7 THE AI THEY TESTED"),
    "p01c": ("p01_anthropic_post.pdf", "We deliberately strengthened the agents", "We deliberately strengthened the agents",
             ["We deliberately strengthened the agents\' lean."], (8, 8), (94.6, 362.5), "ANTHROPIC \u00b7 LIMITATIONS"),
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


def reflow(name, pdf, first, last, hls, width_lh, label):
    from PIL import Image
    L = lines_of(pdf)
    q = lambda t: norm(t).strip('"\'')
    flat = [(w, li) for li in range(len(L)) for w in L[li][6]]
    toks = [q(w[0][0]) for w in flat]
    f, l = [q(t) for t in norm(first).split(" ")], [q(t) for t in norm(last).split(" ")]
    a = next(i for i in range(len(toks)) if toks[i:i + len(f)] == f)
    b = next(i for i in range(a, len(toks)) if toks[i:i + len(l)] == l) + len(l)
    sel = flat[a:b]
    # one rendered band per source line; every word cut from its own line's band
    bands = {}
    for (_, _, _, _, _), li in sel:
        if li in bands:
            continue
        pg, lx0, ly0, lx1, ly1 = L[li][0], L[li][1], L[li][2], L[li][3], L[li][4]
        pad = (ly1 - ly0) * 0.18
        tmp = os.path.join(HERE, "work", f"_band{li}.png")
        render(pdf, pg, lx0 - 2, ly0 - pad, lx1 + 2, ly1 + pad, tmp)
        bands[li] = (Image.open(tmp).convert("RGB"), lx0 - 2, ly0 - pad)
        os.remove(tmp)
    lh = max(im.size[1] for im, _, _ in bands.values())
    bg = list(bands.values())[0][0].getpixel((2, 2))
    gaps = [(sel[k + 1][0][1] - sel[k][0][3]) for k in range(len(sel) - 1) if sel[k + 1][1] == sel[k][1]]
    space = round(sorted(gaps)[len(gaps) // 2] * S) if gaps else round(lh * 0.25)
    maxw = round(width_lh * lh)
    lines, cur, x = [], [], 0
    for (wd, x0, y0, x1, y1), li in sel:
        im, bx, by = bands[li]
        cut = im.crop((round((x0 - bx) * S) - 2, 0, round((x1 - bx) * S) + 2, im.size[1]))
        if cur and x + space + cut.size[0] > maxw:
            lines.append(cur); cur, x = [], 0
        cur.append((wd, cut, x + (space if cur else 0))); x = cur[-1][2] + cut.size[0]
    lines.append(cur)
    mx, my = round(lh * 0.32), round(lh * 0.12)
    W = max(c[-1][2] + c[-1][1].size[0] for c in lines) + 2 * mx
    lead = round(lh * 1.12)
    H = lead * (len(lines) - 1) + lh + 2 * my
    out = Image.new("RGB", (W, H), bg)
    pos = []
    for n, ln in enumerate(lines):
        for wd, cut, xx in ln:
            out.paste(cut, (xx + mx, n * lead + my))
            pos.append((wd, xx + mx, n * lead + my, cut.size[0], lh, n))
    out.save(OUT + name + ".png")
    boxes = []
    wt = [q(p[0]) for p in pos]
    for ph in hls:
        t = [q(x) for x in norm(ph).split(" ")]
        st = next(i for i in range(len(wt)) if wt[i:i + len(t)] == t)
        run = pos[st:st + len(t)]
        for n in sorted(set(r[5] for r in run)):
            rr = [r for r in run if r[5] == n]
            x0 = min(r[1] for r in rr); x1 = max(r[1] + r[3] for r in rr)
            boxes.append([x0, rr[0][2] + round(lh * 0.1), x1 - x0, round(lh * 0.8)])
    print(f"{name:5s} reflow {W}x{H}  {len(lines)} line(s)  {len(boxes)} box(es)")
    return {"img": "assets/pages/" + name + ".png", "w": W, "h": H, "hl": boxes, "label": label, "whole": True}


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for name, args in REFLOW.items():
        meta[name] = reflow(name, *args)
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

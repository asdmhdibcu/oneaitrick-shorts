"""Short #16: cut the real pages into cards (work/fig/*.png) and find the words to highlight on them.

The creator saved the three pages as PDFs from the browser (work/pdf/, git-ignored). Each card is a slice of one page,
from the line that holds `first` to the line that holds `last`, across the text column. The browser's own header and
footer (URL, date, "Page n of 8") sit outside every slice, so no browser chrome reaches the video.
For every card, `hl` phrases get their line boxes in card pixels, written to work/fig/crops.json for the highlight sweeps.
Usage: python3 crops.py            (all cards)
"""
import html
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "work/pdf") + "/"
OUT = os.path.join(HERE, "work/fig") + "/"
DPI = 440
S = DPI / 72.0

# name: (pdf, first line contains, last line contains, highlight phrases, extra pt above/below, x range in pt or None)
CARDS = {
    # claude.dev engineering post (11 Nov 2026)
    "e_head": ("p04_engineering_post.pdf", "Safely scaling multi-agent", "with general tools, a shared database", [], (10, 8), None),
    "e_aside": ("p04_engineering_post.pdf", "announce table and got started", "between 46 and 139.",
                ["set aside the 47 statements", "reassigned nearly all of the helpers", "between 46 and 139."], (6, 6), None),
    "e_70min": ("p04_engineering_post.pdf", "All 10 statements were proved within", "All 10 statements were proved within",
                ["All 10 statements were proved within roughly 70 minutes."], (8, 8), None),
    "e_idle": ("p04_engineering_post.pdf", "With those first 10 statements done", "six hours (see the writes",
               ["there is no reason to idle,", "reassigned helpers to the harder statements"], (8, 6), None),
    "e_tree": ("p04_engineering_post.pdf", "whenever a piece proved too hard", "of helpers could work in parallel",
               ["2,418 tasks", "10 levels deep"], (6, 6), None),
    "e_done": ("p04_engineering_post.pdf", "Langlands–Tunnell was proved at hour 28.4", "checker.\"",
               ["hour 28.7.", "kernel-checked by the official"], (6, 10), None),
    "e_lesson": ("p04_engineering_post.pdf", "Human direction can also still be useful", "encouragement at such moments",
                 ["Agents tend to give up on hard", "problems and misjudge their difficulty.", "47 of the 60 statements"], (6, 6), None),
    "e_19": ("p04_engineering_post.pdf", "During the run, the harness sent the lead 19", "remained, each encouraging",
             ["19 automatic reminders"], (8, 8), None),
    "e_start": ("p04_engineering_post.pdf", "team’s actions. We gave the agents a list of 60", "on how to prove the theorem",
                ["60 statements,", "one-sentence sketch", "47 proved lemmas"], (8, 8), None),
    # Anthropic research page (4 Sep 2026)
    "r_1637": ("p02_flt_research.pdf", "Around 1637, Pierre de Fermat jotted", "Last Theorem (FLT), as the conjecture",
               ["Around 1637,", "in the margin"], (8, 8), None),
    "r_wiles": ("p02_flt_research.pdf", "to prove. The first proof, from Sir Andrew Wiles", "months of painstaking work",
                ["Sir Andrew Wiles in 1995,"], (8, 8), None),
    "r_lead": ("p02_flt_research.pdf", "We are sharing the first complete", "some thoughts about what this work",
               ["first complete computer-checked proof of Fermat's Last Theorem."], (8, 8), None),
    "r_13m": ("p02_flt_research.pdf", "Recently, Tianyi Peng, an Anthropic researcher", "Along the way, it wrote 13 million",
              ["In 11 days,", "13 million lines of Lean"], (8, 8), None),
    # Anthropic launch page (9 Nov 2026)
    "l_para": ("p03_fable52_launch.pdf", "Our first formalization of Fermat", "any more progress after 30.",
               ["took 11 days.", "guidance from a human", "a team of 1,000 Fable 5.2 agents fully formalized the theorem in just 30", "hours,"], (6, 6), None),
}
# whole regions of a page, in points: name: (pdf, page, x0, y0, x1, y1)
RECTS = {
    "l_hero": ("p03_fable52_launch.pdf", 1, 40, 70, 556, 250),       # date, title and the glow; the site menu above is left out
    "l_chart": ("p03_fable52_launch.pdf", 7, 52, 499, 548, 678),     # the completion chart, Fable 5.2 vs Opus 5.5
    "r_hero": ("p02_flt_research.pdf", 1, 60, 160, 535, 532),        # title, art, published date
}


def bbox_xml(pdf):
    cache = OUT + os.path.basename(pdf) + ".bbox.html"
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
    for name, (pdf, first, last, hls, (pa, pb), xr) in CARDS.items():
        L = lines_of(pdf)
        i0 = find(L, first)
        i1 = find(L, last, i0)
        page = L[i0][0]
        assert L[i1][0] == page, (name, "spans pages")
        col = [l for l in L[i0:i1 + 1]]
        x0 = (xr[0] if xr else min(l[1] for l in col)) - 14
        x1 = (xr[1] if xr else max(l[3] for l in col)) + 14
        # cut halfway between this card's first/last line and its neighbours, so no part-line shows
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
            boxes.append(None)  # phrase separator
        meta[name] = {"w": round((x1 - x0) * S), "h": round((y1 - y0) * S), "hl": boxes, "page": page}
        print(f"{name:9s} p{page} {meta[name]['w']}x{meta[name]['h']}  {len(hls)} highlight(s)")
    for name, (pdf, page, x0, y0, x1, y1) in RECTS.items():
        render(pdf, page, x0, y0, x1, y1, OUT + name + ".png")
        meta[name] = {"w": round((x1 - x0) * S), "h": round((y1 - y0) * S), "hl": [], "page": page}
        print(f"{name:9s} p{page} {meta[name]['w']}x{meta[name]['h']}  region")
    json.dump(meta, open(OUT + "crops.json", "w"), indent=1)

"""#11: crop the real pages around each quoted phrase, with exact highlight boxes.

Two kinds of source (all git-ignored):
  screenshots  work/raw/<id>-image.(jpg|png); tesseract finds the words:
               for f in work/raw/*image.*; do tesseract $f work/ocr/$(basename $f | cut -c1-8) --psm 3 tsv; done
  PDFs         work/pdf/<doc>.pdf (the creator's downloads / Safari prints); pdftotext -bbox finds the words,
               pdftoppm renders the page at DPI.
  python3 make_pages.py            -> assets/pages/<name>.png + assets/pages/pages.json (boxes in crop pixels)
  python3 make_pages.py --sheet    -> also work/pages_check.jpg with the boxes drawn, for review
A crop spans the page's text column (x0..x1), from `above` lines over the phrase to `below` lines under it, or a fixed
y range. Only the highlight is mine; the page is untouched (no retouching, no overlay removal).
"""
import html
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw

RAW, OCR, OUT, PDF = "work/raw", "work/ocr", "assets/pages", "work/pdf"
DPI = 200
os.makedirs(OUT, exist_ok=True)
os.makedirs(f"{PDF}/png", exist_ok=True)

# screenshot: ("img", file, x0, x1) in pixels;  pdf: ("pdf", doc, page, x0, x1) in points
SRC = {
    "p1": ("img", "72a7dd7f-image.jpg", 0, 1186),          # ICO report web page, title + "Our message to model developers"
    "p2": ("img", "52d3a89c-image.jpg", 0, 1186),          # ICO press release, "The rise of AI agents"
    "p3": ("img", "5bb2d16d-image.jpg", 0, 1320),          # ICO call for evidence on agentic AI
    "p5t": ("img", "650935be-image.jpg", 0, 1320),         # Meta: How Meta uses information for generative AI
    "p5w": ("img", "5f7b958b-image.jpg", 0, 1320),         # Meta: Where does Meta get training information?
    "p5p": ("img", "ab329cad-image.jpg", 0, 1320),         # Meta: Privacy and generative AI (the requests form)
    "p5d": ("img", "6f28534d-image.jpg", 0, 1186),         # Meta: How generative AI models work (deleted information)
    # the ICO report, "Building trust and transparency into generative AI development" (8 Oct 2026), 33 pages
    "r1": ("pdf", "p1_report", 1, 0, 595),
    "r4": ("pdf", "p1_report", 4, 60, 535),
    "r5": ("pdf", "p1_report", 5, 60, 535),
    "r10": ("pdf", "p1_report", 10, 60, 535),
    "r14": ("pdf", "p1_report", 14, 60, 535),
    "r15": ("pdf", "p1_report", 15, 60, 535),
    "r16": ("pdf", "p1_report", 16, 60, 535),
    "r19": ("pdf", "p1_report", 19, 60, 535),
    "r24": ("pdf", "p1_report", 24, 60, 535),
    "r25": ("pdf", "p1_report", 25, 60, 535),
    "r27": ("pdf", "p1_report", 27, 60, 535),
    # OpenAI Help Center: Right to be forgotten and personal data removal from ChatGPT; Data controls in ChatGPT
    "o1": ("pdf", "p4_openai", 1, 30, 565),
    "o2": ("pdf", "p4_openai", 2, 30, 565),
    "d1": ("pdf", "p7_datacontrols", 1, 30, 565),
    # Apple Support: About Applebot
    "a1": ("pdf", "p6_apple", 1, 30, 565),
}
# name: (src, highlight phrase(s), above, below, occurrence | (y0, y1) crop in source units: px or pt)
PAGES = {
    "p1_title":   ("p1", ["Building trust and transparency into generative AI development: our work to create regulatory certainty"], (150, 1520), None, 1),
    "p2_agents":  ("p2", ["capable of completing tasks, using tools and interacting with websites,"], 2, 1, 0),
    "p2_quote":   ("p2", ["robust data protection safeguards become even more critical."], (1300, 2045), None, 0),
    "p3_dates":   ("p3", ["Start date 8 October 2026"], (80, 1010), None, 0),
    "p5_title":   ("p5t", ["How Meta uses information for generative AI models and features"], (40, 1050), None, 0),
    "p5_public":  ("p5w", ["Information that is publicly available on the Internet", "such as posts or photos and their captions,"], 2, 1, 0),
    "p5_anyone":  ("p5p", ["Whether you use Meta Products or not, anyone can submit requests"], 0, 3, 0),
    "p5_form":    ("p5p", ["Learn more and submit requests here."], 3, 0, 0),
    "p5_deleted": ("p5d", ["If you delete a piece of information a model learnt from (such as a public post), the model won't change in that moment."], 2, 2, 0),
    # the report
    "r_cover":    ("r1", ["8 October 2026"], (0, 842), None, 0),
    "r_message":  ("r4", ["you must:"], 1, 5, 0),
    "r_law":      ("r4", ["interpretation and application of the law can be challenging", "We’re engaging with the government"], 0, 1, 0),
    "r_xai":      ("r4", ["We’ve opened formal investigations into X Internet Unlimited Company (XIUC) and X.AI LLC (X.AI)"], 0, 2, 0),
    "r_agents":   ("r5", ["the models bypassed protections, used unauthorised communication channels and accessed external systems"], 2, 0, 0),
    "r_decline":  ("r10", ["transparency has continued to decline."], 1, 3, 0),
    "r_notices":  ("r10", ["spread across several different privacy notices, help pages, and product interfaces,"], 1, 1, 0),
    "r_humanity": ("r14", ["“benefitting humanity”, are unlikely to meet this requirement"], 3, 1, 0),
    "r_maze":     ("r15", ["‘privacy maze’,"], 3, 2, 0),
    "r_apple":    ("r16", ["allows people to identify specific webpages that organisations shouldn’t use for training."], 3, 0, 0),
    "r_retrain":  ("r16", ["it can be difficult to erase their information from the model itself without retraining the entire model."], 2, 1, 0),
    "r_social":   ("r19", ["social media posts often contain information about a person’s political opinions, religious beliefs or health."], 2, 0, 0),
    "r_sensitive": ("r19", ["are likely to be processing special category data (whether intentionally or not", "unless they can clearly demonstrate"], 1, 1, 0),
    "r_interests": ("r25", ["firms didn’t always clearly identify specific interests"], 1, 1, 0),
    "r_suspend":  ("r25", ["initiated a formal investigation into X Internet Unlimited Company (XIUC) and X.AI LLC (X.AI).", "we decided to suspend engagement with X.AI"], 1, 1, 0),
    "r_changed":  ("r27", ["Apple, Cohere and OpenAI have made changes", "Amazon, Anthropic, DeepSeek, Google, Meta, Microsoft and Stability AI have each made changes or committed to implementing"], 1, 0, 0),
    "r_measures": ("r27", ["Non-technical summaries of the types and sources of information used to train",
                           "Improved information to enable people to exercise their data protection rights",
                           "efficacy of any technical or organisational safeguards"], 1, 2, 0),
    # OpenAI, Apple
    "p4_openai":  ("o1", ["stop certain personal information about you from appearing in ChatGPT responses."], 6, 4, 0),
    "p4_title":   ("o1", ["Right to be forgotten and personal data removal from ChatGPT"], 1, 3, 1),
    "p4_how":     ("o2", ["Select Remove personal data from ChatGPT responses"], 3, 1, 0),
    "p7_improve": ("d1", ["When Improve the model for everyone is off, your new conversations won’t be used to train"], 3, 1, 0),
    "p6_apple":   ("a1", ["Web publishers can opt out from having their content used to train generative foundation models"], 1, 1, 0),
}


def norm(t):
    t = t.lower().replace("’", "'").replace("‘", "'").replace("“", "").replace("”", "")
    t = re.sub(r"[^a-z0-9%']", "", t)
    return {"al": "ai"}.get(t, t).replace("'", "")


_cache = {}


def words_of(key):
    """Words with boxes in source pixels (screenshots) or rendered-page pixels (PDFs), and a line key."""
    if key in _cache:
        return _cache[key]
    s = SRC[key]
    ws = []
    if s[0] == "img":
        f = s[1].split("-")[0]
        for r in (r.split("\t") for r in open(f"{OCR}/{f}.tsv").read().splitlines()[1:]):
            if len(r) == 12 and r[11].strip():
                ws.append(dict(t=r[11], x=int(r[6]), y=int(r[7]), w=int(r[8]), h=int(r[9]), line=(int(r[2]), int(r[3]), int(r[4]))))
    else:
        _, doc, page = s[:3]
        out = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-bbox", f"{PDF}/{doc}.pdf", "-"], capture_output=True, text=True).stdout
        k = DPI / 72
        for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', out):
            x0, y0, x1, y1 = (float(v) for v in m.groups()[:4])
            ws.append(dict(t=html.unescape(m.group(5)), x=round(x0 * k), y=round(y0 * k), w=round((x1 - x0) * k), h=round((y1 - y0) * k), line=round(y0 * 2)))
    _cache[key] = ws
    return ws


def image_of(key):
    s = SRC[key]
    if s[0] == "img":
        return Image.open(f"{RAW}/{s[1]}").convert("RGB"), 1.0
    _, doc, page = s[:3]
    png = f"{PDF}/png/{doc}-{page}-{DPI}.png"
    if not os.path.exists(png):
        subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(page), "-l", str(page), "-singlefile", "-png", f"{PDF}/{doc}.pdf", png[:-4]], check=True)
    return Image.open(png).convert("RGB"), DPI / 72


def find(ws, phrase, occ):
    target = [norm(x) for x in phrase.split() if norm(x)]
    flat = [(i, norm(w["t"])) for i, w in enumerate(ws)]
    flat = [(i, t) for i, t in flat if t]
    hits = []
    for k in range(len(flat)):
        j, ok = k, True
        for t in target:
            if j < len(flat) and flat[j][1] == t:
                j += 1
            elif j + 1 < len(flat) and flat[j][1] + flat[j + 1][1] == t:
                j += 2
            elif j < len(flat) and flat[j][1].startswith(t) and t == target[-1]:
                j += 1
            else:
                ok = False
                break
        if ok:
            hits.append([flat[m][0] for m in range(k, j)])
    if len(hits) <= occ:
        raise SystemExit(f"not found: {phrase[:70]}")
    return hits[occ]


def lines_of(ws):
    by = {}
    for w in ws:
        by.setdefault(w["line"], []).append(w)
    ls = sorted((min(w["y"] for w in v), max(w["y"] + w["h"] for w in v)) for v in by.values())
    out = []
    for a, b in ls:
        if out and a < out[-1][1] - 6:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def boxes_for(ws, idx):
    """One box per text row of the matched words, padded like a highlighter stroke."""
    groups = []
    for i in idx:
        w = ws[i]
        a, b = w["y"], w["y"] + w["h"]
        for g in groups:
            if min(b, g[3]) - max(a, g[2]) > 0.4 * min(b - a, g[3] - g[2]):
                g[0] = min(g[0], w["x"]); g[1] = max(g[1], w["x"] + w["w"]); g[2] = min(g[2], a); g[3] = max(g[3], b)
                break
        else:
            groups.append([w["x"], w["x"] + w["w"], a, b])
    out = []
    for x0, x1, y0, y1 in sorted(groups, key=lambda g: g[2]):
        ph = max(4, round((y1 - y0) * 0.2))
        out.append([x0 - 6, y0 - ph, x1 - x0 + 12, y1 - y0 + 2 * ph])
    return out


if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    meta = json.load(open(f"{OUT}/pages.json")) if os.path.exists(f"{OUT}/pages.json") else {}
    sheet = []
    for name, (key, phrases, above, below, occ) in PAGES.items():
        if only and name not in only:
            continue
        s = SRC[key]
        im, k = image_of(key)
        cx0, cx1 = round(s[-2] * k), min(im.width, round(s[-1] * k))
        ws = words_of(key)
        allb, groups = [], []
        for p in phrases:
            bb = boxes_for(ws, find(ws, p, occ))
            groups.append(list(range(len(allb), len(allb) + len(bb))))
            allb += bb
        if isinstance(above, tuple):
            y0, y1 = round(above[0] * k), round(above[1] * k)
        else:
            ls = lines_of(ws)
            top, bot = min(b[1] for b in allb), max(b[1] + b[3] for b in allb)
            i0 = max(0, min(j for j, (a, b) in enumerate(ls) if b > top) - above)
            i1 = min(len(ls) - 1, max(j for j, (a, b) in enumerate(ls) if a < bot) + below)
            pad = round(6 * k) if s[0] == "pdf" else 34
            y0, y1 = ls[i0][0] - pad, ls[i1][1] + pad
        y0, y1 = max(0, y0), min(im.height, y1)
        crop = im.crop((cx0, y0, cx1, y1))
        crop.save(f"{OUT}/{name}.png", optimize=True)
        bx = [[x - cx0, y - y0, w, h] for x, y, w, h in allb]
        meta[name] = dict(w=crop.width, h=crop.height, boxes=bx, groups=groups, src=s[1])
        if "--sheet" in sys.argv:
            c = crop.copy(); d = ImageDraw.Draw(c, "RGBA")
            for x, y, w, h in bx:
                d.rectangle([x, y, x + w, y + h], fill=(200, 255, 77, 110), outline=(120, 160, 0, 255), width=3)
            c.thumbnail((600, 900)); sheet.append((name, c))
        print(f"{name:12s} {crop.width}x{crop.height}  {len(bx)} boxes")
    json.dump(meta, open(f"{OUT}/pages.json", "w"), indent=1)
    if sheet:
        W = 600 * 5; Hh = 920 * ((len(sheet) + 4) // 5)
        S = Image.new("RGB", (W, Hh), (40, 40, 48)); d = ImageDraw.Draw(S)
        for j, (n, c) in enumerate(sheet):
            x, y = (j % 5) * 600, (j // 5) * 920
            S.paste(c, (x, y + 20)); d.text((x + 4, y + 2), n, fill=(255, 255, 255))
        S.save("work/pages_check.jpg", quality=85)

"""#12: crop the real pages around each quoted phrase, with exact highlight boxes.

Every source is an image with a tesseract TSV (the creator's PDFs have no text layer: they are rendered at 200 DPI first;
the page recordings are frames scaled 2x so the OCR can read them):
  pdftoppm -r 200 -f N -l N -singlefile -png work/raw/P1.pdf work/pdf/png/P1-N; tesseract ... work/ocr/P1-N --psm 3 tsv
  ffmpeg -ss K -i work/raw/rec_p7.mp4 -frames:v 1 -vf scale=iw*2:ih*2:flags=lanczos work/rec/fr/p7_KK.png; tesseract ...
  python3 make_pages.py            -> assets/pages/<name>.png + assets/pages/pages.json (boxes in crop pixels)
  python3 make_pages.py --sheet    -> also work/pages_check.jpg with the boxes drawn, for review
A crop spans the page's text column (x0..x1), from `above` lines over the phrase to `below` lines under it, or a fixed
y range. Only the highlight is mine. Retouching: none, except the creator's name blurred on the ElevenLabs voice chip.
"""
import json
import os
import re
import sys

from PIL import Image, ImageDraw

OUT = "assets/pages"
os.makedirs(OUT, exist_ok=True)
P, F = "work/pdf/png/", "work/rec/fr/"
# key: (image, tsv, x0, x1) in image pixels
SRC = {
    "o1": (P + "P1-1.png", "work/ocr/P1-1.tsv", 90, 1610),      # OpenAI, "March 20 ChatGPT outage: Here's what happened"
    "o2": (P + "P1-2.png", "work/ocr/P1-2.tsv", 90, 1610),
    "f1": (P + "P2-1.png", "work/ocr/P2-1.tsv", 90, 1610),      # Forbes, Samsung bans ChatGPT (2 May 2023)
    "f2": (P + "P2-2.png", "work/ocr/P2-2.tsv", 90, 1610),
    "a1": (P + "P3-1.png", "work/ocr/P3-1.tsv", 90, 1610),      # Reuters, Amazon's recruiting tool (10 Oct 2018)
    "a2": (P + "P3-2.png", "work/ocr/P3-2.tsv", 90, 1610),
    "i1": (P + "P4-1.png", "work/ocr/P4-1.tsv", 90, 1610),      # ICO, rights related to automated decision-making
    "r5h": (F + "p5_18.png", F + "p5_18.tsv", 240, 1650),      # Reuters Fact Check, the Pentagon image (22 May 2023)
    "r5v": (F + "p5_05.png", F + "p5_05.tsv", 240, 1650),
    "s13": (F + "p7_13.png", F + "p7_13.tsv", 460, 2520),      # Starling Bank press release (18 Sept 2024)
    "s16": (F + "p7_16.png", F + "p7_16.tsv", 460, 2520),
    "s17": (F + "p7_17.png", F + "p7_17.tsv", 460, 2520),
    "t5": (F + "p8_05.png", F + "p8_05.tsv", 150, 2490),       # FTC consumer alert (20 Mar 2023)
    "t18": (F + "p8_18.png", F + "p8_18.tsv", 150, 1900),
    "c0": (F + "p9_00.png", F + "p9_00.tsv", 70, 2420),        # CNN, 4 Feb 2024
    "c7": (F + "p9_07.png", F + "p9_07.tsv", 670, 2130),
    "c14": (F + "p9_14.png", F + "p9_14.tsv", 670, 2130),
    "u1": (F + "p10_01.png", F + "p10_01.tsv", 60, 2600),      # CNN, Arup named (16 May 2024)
    "e1": ("work/rec/eleven_blur.png", "work/rec/eleven_full.tsv", 0, 1320),   # ElevenLabs Text to Speech (the creator's phone)
    "ad": ("work/raw/P6.png", None, 0, 1280),                  # the RNC's "Beat Biden" ad, a frame with its disclaimer
}
# name: (src, phrases, above, below, occurrence | (y0, y1) fixed crop); MANUAL boxes for sources without OCR
PAGES = {
    "o_title": ("o1", ["March 20 ChatGPT outage: Here’s what happened@1"], (190, 600), None, 0),
    "o_titles": ("o1", ["allowed some users to see titles from another active user’s chat history."], 1, 2, 0),
    "o_pay": ("o2", ["1.2% of the ChatGPT Plus subscribers who were active during a specific nine-hour window.",
                     "first and last name, email address, payment address, credit card type and the last four digits (only) of a credit card number,"], 1, 1, 0),
    "o_full": ("o2", ["Full credit card numbers were not exposed at any time."], 4, 2, 0),
    "f_ban": ("f1", ["Samsung Bans ChatGPT Among Employees After Sensitive Code Leak@1", "Samsung Electronics has banned the use of ChatGPT"], (620, 1260), None, 0),
    "f_code": ("f2", ["accidental leak of sensitive internal source code by an engineer who uploaded it to ChatGPT last month."], 2, 2, 0),
    "a_team": ("a1", ["building computer programs since 2014 to review job applicants’ resumes"], 2, 1, 0),
    "a_cvs": ("a2", ["resumes submitted to the company over a 10-year period.", "Most came from men,"], 2, 1, 0),
    "a_women": ("a2", ["It penalized resumes that included the word \"women's,\" as in \"women's chess club captain.\"",
                       "downgraded graduates of two all-women's colleges,"], 1, 1, 0),
    "a_never": ("a2", ["never relied solely on those rankings,", "ultimately disbanded the team"], 1, 1, 0),
    "i_human": ("i1", ["request human intervention or challenge a decision;"], 4, 2, 0),
    "r_head": ("r5h", ["Fact Check: Online posts reporting", "explosion near Pentagon on May 22,", "2023 are false"], 0, 2, 0),
    "r_false": ("r5v", ["False. There was no explosion near the Pentagon on the morning of May 22, 2023."], 3, 1, 0),
    "s_three": ("s13", ["Criminals are now able to clone a person's voice from as little as three seconds of audio"], 9, 0, 0),
    "s_quarter": ("s16", ["over a quarter (28%) of UK adults say they have been targeted by an AI voice cloning scam at least once in the past year."], 1, 3, 0),
    "s_phrase": ("s17", ["agree a ‘Safe Phrase’ with their close friends and family that no one else knows,"], 2, 2, 0),
    "t_head": ("t5", ["Scammers use AI to enhance their family emergency schemes", "March 20, 2023"], 1, 1, 0),
    "t_clip": ("t18", ["A scammer could use AI to clone the voice of your loved one. All he needs is a short audio clip of your family member’s voice"], 1, 1, 0),
    "c_head": ("c0", ["Finance worker pays out $25 million after video call with deepfake ‘chief financial officer’"], (110, 535), None, 0),
    "c_fake": ("c7", ["all of whom were in fact deepfake recreations, Hong Kong police said", "it turns out that everyone [he saw] was fake,"], 3, 1, 0),
    "c_hk": ("c14", ["remit a total of $200 million Hong Kong dollars — about $25.6 million,"], 1, 1, 0),
    "u_arup": ("u1", ["British engineering giant Arup revealed as $25 million deepfake scam victim"], 0, 2, 0),
    "e_tts": ("e1", ["[conversational]", "[warm]", "[curious]"], (470, 1420), None, 0),
    "ad_frame": ("ad", None, (0, 720), None, 0),
}
MANUAL = {"ad_frame": [[[0, 87, 182, 24]]]}   # "Built entirely with AI imagery." (white type, top left: no OCR)


def norm(t):
    t = t.lower().replace("’", "'").replace("‘", "'").replace("“", "").replace("”", "")
    t = re.sub(r"[^a-z0-9%']", "", t)
    return {"al": "ai", "ali": "ai"}.get(t, t).replace("'", "")


def words_of(key):
    img, tsv = SRC[key][:2]
    ws = []
    for r in (r.split("\t") for r in open(tsv).read().splitlines()[1:]):
        if len(r) == 12 and r[11].strip():
            ws.append(dict(t=r[11], x=int(r[6]), y=int(r[7]), w=int(r[8]), h=int(r[9]), line=(int(r[2]), int(r[3]), int(r[4]))))
    return ws


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
            elif j < len(flat) and (flat[j][1].startswith(t) or t.startswith(flat[j][1])) and len(flat[j][1]) >= 3:
                j += 1
            else:
                ok = False
                break
        if ok:
            hits.append([flat[m][0] for m in range(k, j)])
    if len(hits) <= occ:
        hits = hits or [[]]
        if len(hits) <= occ:
            raise SystemExit(f"not found: {phrase[:70]}")
    return hits[occ] if len(hits) > occ else hits[-1]


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
        img, tsv, cx0, cx1 = SRC[key]
        im = Image.open(img).convert("RGB")
        cx1 = min(cx1, im.width)
        allb, groups = [], []
        if phrases:
            ws = words_of(key)
            for p in phrases:
                po = occ
                if re.search(r"@\d+$", p):
                    p, po = p.rsplit("@", 1)[0], int(p.rsplit("@", 1)[1])
                bb = boxes_for(ws, find(ws, p, po))
                groups.append(list(range(len(allb), len(allb) + len(bb))))
                allb += bb
        for g in MANUAL.get(name, []):
            groups.append(list(range(len(allb), len(allb) + len(g)))); allb += g
        if isinstance(above, tuple):
            y0, y1 = above
        else:
            ls = lines_of(ws)
            top, bot = min(b[1] for b in allb), max(b[1] + b[3] for b in allb)
            i0 = max(0, min(j for j, (a, b) in enumerate(ls) if b > top) - above)
            i1 = min(len(ls) - 1, max(j for j, (a, b) in enumerate(ls) if a < bot) + below)
            y0, y1 = ls[i0][0] - 30, ls[i1][1] + 30
        y0, y1 = max(0, y0), min(im.height, y1)
        crop = im.crop((cx0, y0, cx1, y1))
        crop.save(f"{OUT}/{name}.png", optimize=True)
        bx = [[x - cx0, y - y0, w, h] for x, y, w, h in allb]
        meta[name] = dict(w=crop.width, h=crop.height, boxes=bx, groups=groups, src=img)
        if "--sheet" in sys.argv:
            c = crop.copy(); d = ImageDraw.Draw(c, "RGBA")
            for x, y, w, h in bx:
                d.rectangle([x, y, x + w, y + h], fill=(200, 255, 77, 110), outline=(120, 160, 0, 255), width=3)
            c.thumbnail((600, 900)); sheet.append((name, c))
        print(f"{name:10s} {crop.width}x{crop.height}  {len(bx)} boxes in {len(groups)} groups")
    json.dump(meta, open(f"{OUT}/pages.json", "w"), indent=1)
    if sheet:
        W = 600 * 6; Hh = 640 * ((len(sheet) + 5) // 6)
        S = Image.new("RGB", (W, Hh), (40, 40, 48)); d = ImageDraw.Draw(S)
        for j, (n, c) in enumerate(sheet):
            x, y = (j % 6) * 600, (j // 6) * 640
            S.paste(c, (x, y + 20)); d.text((x + 4, y + 2), n, fill=(255, 255, 255))
        S.save("work/pages_check.jpg", quality=85)

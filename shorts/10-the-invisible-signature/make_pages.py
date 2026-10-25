"""Short #10: crop the real pages around each quoted phrase, with exact highlight boxes.

Needs work/pdf/<doc>.pdf (the creator's Safari prints) and <doc>.words.json from pdfwords.py:
  for d in r1_openai r2_claude; do python3 pdfwords.py work/pdf/$d.pdf work/pdf/$d.words.json; done
  python3 make_pages.py            -> assets/pages/<name>.png + assets/pages/pages.json (boxes in crop pixels)
  python3 make_pages.py --sheet    -> also work/pages_check.jpg with the boxes drawn, for review
Pages are rendered at 300 dpi. A crop spans the text column, from MARGIN lines above the phrase to MARGIN below.
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw

PDF = 'work/pdf'
OUT = 'assets/pages'
os.makedirs(OUT, exist_ok=True)
os.makedirs('work/pdf/hi', exist_ok=True)

# name: (doc, phrase, lines of context above, below, occurrence[, end phrase])
PHRASES = {
    # R1 · OpenAI Help Center, "Provenance signals in OpenAI-generated content" (printed 24 Oct 2026)
    'r1_title':     ('r1_openai', 'Provenance signals in OpenAI-generated content', 0, 0, 1),
    'r1_eu':        ('r1_openai', 'We’re implementing text watermarking for ChatGPT users in the EU to comply with the EU AI Act', 0, 1, 0),
    'r1_hidden':    ('r1_openai', 'It does not add hidden characters, invisible spaces, or unusual punctuation.', 1, 1, 0),
    'r1_withstand': ('r1_openai', 'are designed to withstand common changes.', 1, 2, 0),
    'r1_key':       ('r1_openai', 'each favoring different choices according to a secret key.', 2, 2, 0),
    'r1_rates':     ('r1_openai', 'At 1% false-positive rate, Spanish has the highest detection rate (69.0%), while Romanian has the lowest (42.2%).', 2, 0, 0),
    'r1_student':   ('r1_openai', 'Academic integrity applications, such as checking student work for AI use', 0, 1, 0),
    # R2 · Claude Help Center, "How Claude marks AI-generated content" (the creator's copy, 24 Oct 2026)
    'r2_title':     ('r2_claude', 'How Claude marks AI-generated content', 0, 1, 0),
    'r2_worldwide': ('r2_claude', 'Marking applies to supported-model output wherever Claude is offered worldwide.', 0, 0, 0),
    'r2_translate': ('r2_claude', 'People may use Claude to proofread, translate, summarize, or convert', 1, 1, 0),
    'r2_conclusive':('r2_claude', 'A detected mark is not fully conclusive', 0, 2, 0),
    'r2_nomark':    ('r2_claude', 'No detected mark does not prove content was not AI-generated', 0, 0, 0),
}


def norm(t):
    return re.sub(r'[^a-z0-9%]', '', t.lower().replace('’', "'"))


def find(words, phrase, occ):
    target = [norm(x) for x in phrase.split() if norm(x)]
    flat = [(i, norm(w['t'])) for i, w in enumerate(words)]
    flat = [(i, t) for i, t in flat if t]
    hits = []
    for k in range(len(flat)):
        j, ok = k, True
        for t in target:
            # tolerate words split across a hyphenated line break: "multi-" + "tenant"
            if j < len(flat) and flat[j][1] == t:
                j += 1
            elif j + 1 < len(flat) and flat[j][1] + flat[j + 1][1] == t:
                j += 2
            else:
                ok = False
                break
        if ok:
            hits.append([flat[m][0] for m in range(k, j)])
    if len(hits) <= occ:
        raise SystemExit(f'not found: {phrase[:60]}')
    return hits[occ]


def lines_of(ws):
    """Group word boxes into text lines (same page, overlapping y)."""
    ls = []
    for w in sorted(ws, key=lambda w: (w['p'], w['y'], w['x'])):
        if ls and ls[-1][0]['p'] == w['p'] and abs(ls[-1][0]['y'] - w['y']) < w['h'] * 0.5:
            ls[-1].append(w)
        else:
            ls.append([w])
    return ls


def render(doc, p):
    out = f'work/pdf/hi/{doc}-{p}.png'
    if not os.path.exists(out):
        subprocess.run(['pdftoppm', '-r', '300', '-f', str(p), '-l', str(p), '-png', '-singlefile',
                        f'{PDF}/{doc}.pdf', out[:-4]], check=True)
    return out


meta, words_cache = {}, {}
for name, spec in PHRASES.items():
    doc, phrase, above, below, occ = spec[:5]
    words = words_cache.setdefault(doc, json.load(open(f'{PDF}/{doc}.words.json')))
    idx = find(words, phrase, occ)
    if len(spec) > 5:  # extend to an end phrase (a long quote)
        end = find(words, spec[5], 0)
        idx = list(range(idx[0], end[-1] + 1))
    hit = [words[i] for i in idx]
    pages = sorted({w['p'] for w in hit})
    if len(pages) > 1:  # phrase runs over a page break: keep the page holding most of it
        p = max(pages, key=lambda q: sum(w['p'] == q for w in hit))
        print(f'  {name}: spans pages {pages}, using {p}')
        hit = [w for w in hit if w['p'] == p]
    p = hit[0]['p']
    hx0 = min(w['x'] for w in hit); hx1 = max(w['x'] + w['w'] for w in hit)
    # keep to the phrase's own column (page 1 of OpenAI's print has a contents list on the right)
    page_words = [w for w in words if w['p'] == p and w['x'] >= hx0 - 250 and w['x'] + w['w'] <= hx1 + 250]
    plines = lines_of(page_words)
    hlines = lines_of(hit)
    # text column: lines of the page that overlap the phrase horizontally
    x0 = min(w['x'] for w in hit); x1 = max(w['x'] + w['w'] for w in hit)
    col = [l for l in plines if min(w['x'] for w in l) < x1 and max(w['x'] + w['w'] for w in l) > x0]
    ys = [l[0]['y'] for l in col]
    first = min(range(len(col)), key=lambda i: abs(ys[i] - hlines[0][0]['y']))
    last = min(range(len(col)), key=lambda i: abs(ys[i] - hlines[-1][0]['y']))
    a, b = max(0, first - above), min(len(col) - 1, last + below)
    span = col[a:b + 1]
    cx0 = min(min(w['x'] for w in l) for l in span) - 40
    cx1 = max(max(w['x'] + w['w'] for w in l) for l in span) + 40
    # cut halfway between lines, so no ascenders or descenders from the neighbours show
    top = min(w['y'] for w in span[0]); bot = max(w['y'] + w['h'] for w in span[-1])
    prev_bot = max(w['y'] + w['h'] for w in col[a - 1]) if a > 0 else None
    next_top = min(w['y'] for w in col[b + 1]) if b + 1 < len(col) else None
    cy0 = (prev_bot + top) // 2 if prev_bot is not None and top - prev_bot < 120 else top - 30
    cy1 = (bot + next_top) // 2 if next_top is not None and next_top - bot < 120 else bot + 30
    im = Image.open(render(doc, p)).convert('RGB')
    cx0, cy0 = max(0, cx0), max(0, cy0)
    cx1, cy1 = min(im.width, cx1), min(im.height, cy1)
    crop = im.crop((cx0, cy0, cx1, cy1))
    crop.save(f'{OUT}/{name}.png')
    boxes = [[min(w['x'] for w in l) - cx0 - 6, min(w['y'] for w in l) - cy0 - 4,
              max(w['x'] + w['w'] for w in l) - min(w['x'] for w in l) + 12,
              max(w['y'] + w['h'] for w in l) - min(w['y'] for w in l) + 8] for l in hlines]
    meta[name] = {'doc': doc, 'page': p, 'w': crop.width, 'h': crop.height, 'boxes': boxes,
                  'text': ' '.join(w['t'] for w in hit)}
    print(f'{name:12s} p{p:<3d} {crop.width}x{crop.height}  {len(boxes)} line(s)')

json.dump(meta, open(f'{OUT}/pages.json', 'w'), indent=1)

if '--sheet' in sys.argv:
    tiles = []
    for name, m in meta.items():
        im = Image.open(f'{OUT}/{name}.png').convert('RGB')
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(ov)
        for x, y, w, h in m['boxes']:
            g.rectangle([x, y, x + w, y + h], fill=(200, 255, 77, 90), outline=(120, 160, 0, 255), width=3)
        im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
        sc = 520 / im.width
        im = im.resize((520, max(1, int(im.height * sc))))
        t = Image.new('RGB', (520, im.height + 22), (30, 30, 30)); t.paste(im, (0, 22))
        ImageDraw.Draw(t).text((4, 4), f"{name} · p{m['page']}", fill=(200, 255, 77))
        tiles.append(t)
    cols = 4
    colh = [0] * cols; place = []
    for t in tiles:
        c = colh.index(min(colh)); place.append((c, colh[c])); colh[c] += t.height + 8
    sheet = Image.new('RGB', (cols * 528, max(colh)), (15, 15, 15))
    for t, (c, y) in zip(tiles, place):
        sheet.paste(t, (c * 528, y))
    sheet.save('work/pages_check.jpg', quality=82)
    print('sheet', sheet.size)

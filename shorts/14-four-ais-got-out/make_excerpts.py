"""Short #14: excerpt cards built from the real S-1 page 48 (rendered from sec.gov's HTML). Each card stacks word-exact
crops of the passage's lines, so the words on screen are the filing's own type, big enough to read on a phone.
Writes ex_<name>.png (and ex_<name>.json: the word boxes, for highlights). Reads work/fig/s1_p48.png and s1_p48_lines.json (the page rendered from the S-1's HTML).
Usage: python3 -I make_excerpts.py"""
from PIL import Image
import numpy as np, json
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work/fig'))
im = Image.open('s1_p48.png').convert('RGB'); S = 3
L = {l[0]: l[2] for l in json.load(open('s1_p48_lines.json'))}

def line(top):
    return im.crop((265, int((top - 3) * S), 2190, int((top + 12.5) * S)))

def boxes(img):
    a = np.array(img.convert('L')) < 128; col = a.any(axis=0); xs = []; inw = False; gap = 0
    for x, c in enumerate(col):
        if c:
            if not inw: start = x; inw = True
            gap = 0; end = x
        elif inw:
            gap += 1
            if gap > 14: xs.append((start, end + 1)); inw = False
    if inw: xs.append((start, end + 1))
    return xs

def excerpt(name, parts):
    rows = []
    for top, i0, i1 in parts:
        img = line(top); b = boxes(img); words = L[top].split()
        x0, x1 = b[i0][0] - 6, b[i1 - 1][1] + 6
        rows.append((img.crop((x0, 0, x1, img.height)), ' '.join(words[i0:i1])))
    W = max(r.width for r, _ in rows) + 60; lh = rows[0][0].height + 14
    out = Image.new('RGB', (W, lh * len(rows) + 40), 'white')
    for k, (r, t) in enumerate(rows):
        out.paste(r, (30, 20 + k * lh)); print(name, k, t)
    out.save(f'ex_{name}.png'); json.dump({'w': out.width, 'h': out.height, 'lh': lh}, open(f'ex_{name}.json', 'w'))

excerpt('inet', [(535, 7, 16), (550, 0, 4)])
excerpt('four', [(550, 4, 12), (550, 12, 16), (565, 0, 10)])
excerpt('abort', [(565, 10, 20), (580, 0, 1)])
excerpt('worst', [(580, 7, 15), (580, 15, 21), (595, 0, 6), (595, 6, 12)])
excerpt('noev', [(626, 5, 15), (641, 0, 6)])

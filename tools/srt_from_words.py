"""Build an SRT from aligned words (words.json): cues break at sentence ends or ~60 chars; 2 lines max.

Usage: python3 srt_from_words.py words.json OUT.srt
"""
import json
import re
import sys

NUM = {"fifty": "50", "four": "4", "thirty-five": "35", "three": "3"}
KEEP_CAPS = {"AI"}


def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def clean(w):
    core = re.sub(r"[^\w'-]", "", w)
    out = w
    if core.isupper() and len(core) > 1 and core not in KEEP_CAPS:
        out = w.replace(core, core.lower())
    low = core.lower()
    if low in NUM:
        out = out.replace(core if core in out else core.lower(), NUM[low])
    return out


words = json.load(open(sys.argv[1]))
FIX = {"But": (13.58, 13.86)}  # aligner put "But" inside the chuckle
for w in words:
    if w["text"] in FIX and abs(w["start"] - 12.87) < 0.3:
        w["start"], w["end"] = FIX[w["text"]]
cues, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    text = " ".join(clean(x["text"]) for x in cur)
    nxt = words[i + 1] if i + 1 < len(words) else None
    gap = (nxt["start"] - w["end"]) if nxt else 9
    end_sent = re.search(r"[.?!]$|\.\.\.$", w["text"]) is not None
    soft = re.search(r"[,;:]$", w["text"]) is not None
    if end_sent or (gap > 0.6 and len(text) > 24) or len(text) > 60 or (soft and len(text) > 34) or nxt is None:
        cues.append(cur)
        cur = []

merged = []
for c in cues:
    t = " ".join(clean(x["text"]) for x in c)
    if merged and len(t) < 14 and t[0].islower():
        prev = " ".join(clean(x["text"]) for x in merged[-1])
        if len(prev) + len(t) + 1 <= 84:
            merged[-1] = merged[-1] + c
            continue
    merged.append(c)
cues = merged

lines = []
for k, c in enumerate(cues):
    text = " ".join(clean(x["text"]) for x in c)
    if len(text) > 42:
        ws = text.split(" ")
        best = min(range(1, len(ws)), key=lambda j: abs(len(" ".join(ws[:j])) - len(text) / 2))
        text = " ".join(ws[:best]) + "\n" + " ".join(ws[best:])
    a = max(c[0]["start"] - 0.05, 0)
    b = c[-1]["end"] + 0.35
    if k + 1 < len(cues):
        b = min(b, cues[k + 1][0]["start"] - 0.05)
    lines.append(f"{k + 1}\n{ts(a)} --> {ts(b)}\n{text}\n")
open(sys.argv[2], "w").write("\n".join(lines))
print(len(cues), "cues")

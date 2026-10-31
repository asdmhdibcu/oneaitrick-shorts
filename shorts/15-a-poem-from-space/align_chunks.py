"""Align a long take in chunks (pocketsphinx's whole-file grammar fails on #15's 178 s take).

Cuts the audio at pauses that fall between script lines, force-aligns each chunk against its lines with the same
text cleaning as tools/align.py, and writes one words.json. A chunk only counts when the grammar reaches its end,
so a skipped or changed word shows up as a chunk that won't align.

Usage: python3 align_chunks.py work/voice16k.wav work/script_plain.txt work/words_raw.json
"""
import json
import re
import sys
import wave

import numpy as np
from pocketsphinx import Decoder

sys.argv_backup = list(sys.argv)
wav_path, script_path, out_path = sys.argv[1:4]

# Reuse the cleaning rules from tools/align.py without running it.
src = open(__file__.replace("shorts/15-a-poem-from-space/align_chunks.py", "tools/align.py")).read()
SUBS = eval(re.search(r"SUBS = (\{.*?\})", src, re.S).group(1))
WORDMAP = eval(re.search(r"WORDMAP = (\{.*?\})", src, re.S).group(1))


def clean(word):
    t = word.lower()
    for a, b in SUBS.items():
        t = t.replace(a, b)
    t = re.sub(r"[^a-z' \-]", "", t).replace("-", " ").strip("'")
    return " ".join(WORDMAP.get(x, x) for x in t.split())


lines = [l.split() for l in open(script_path).read().splitlines() if l.strip()]
with wave.open(wav_path, "rb") as wf:
    sr = wf.getframerate()
    pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
x = pcm.astype(float) / 32768
win = int(sr * 0.02)
n = len(x) // win
db = 20 * np.log10(np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
sil = db < -40
pauses = []  # (start, end) seconds of pauses >= 0.25 s
i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]:
            j += 1
        if (j - i) * 0.02 >= 0.25:
            pauses.append((i * 0.02, j * 0.02))
        i = j
    else:
        i += 1
total = len(x) / sr


def align(t0, t1, words):
    toks = [clean(w) for w in words]
    text = " ".join(t for t in toks if t)
    seg = pcm[int(t0 * sr): int(t1 * sr)].tobytes()
    d = Decoder(samprate=sr, bestpath=False)
    try:
        d.set_align_text(text)
        d.start_utt(); d.process_raw(seg, full_utt=True); d.end_utt()
        d.set_alignment()
        d.start_utt(); d.process_raw(seg, full_utt=True); d.end_utt()
    except RuntimeError:
        return None
    segs = [s for s in d.get_alignment() if s.name not in ("<s>", "</s>", "<sil>") and not s.name.startswith("+")]
    out, k = [], 0
    for disp, al in zip(words, toks):
        tk = [t for t in al.split() if t]
        if not tk:
            continue
        s = segs[k: k + len(tk)]
        k += len(tk)
        if not s:
            return None
        out.append({"text": disp, "start": round(t0 + s[0].start / 100.0, 3),
                    "end": round(t0 + (s[-1].start + s[-1].duration) / 100.0, 3)})
    return out


chars = [sum(len(w) + 1 for w in l) for l in lines]
rate = sum(chars) / total
words_out, t0, li = [], 0.0, 0
while li < len(lines):
    done = False
    for k in (1, 2, 3):  # lines in this chunk
        if li + k > len(lines):
            break
        chunk = [w for l in lines[li: li + k] for w in l]
        if li + k == len(lines):
            cands = [total]
        else:
            est = t0 + sum(chars[li: li + k]) / rate
            cands = sorted({(a + b) / 2 for a, b in pauses if a > t0 + 0.5}, key=lambda c: abs(c - est))[:6]
        for c in cands:
            res = align(t0, c, chunk)
            if res and c - res[-1]["end"] < 0.8 and res[-1]["end"] - res[-1]["start"] < 1.2:
                words_out += res
                print("lines %2d-%2d  %6.2f-%6.2f  ok  (%s ... %s)" % (li + 1, li + k, t0, c, chunk[0], chunk[-1]))
                t0, li, done = c, li + k, True
                break
        if done:
            break
    if not done:
        print("FAILED at line %d (%s), from %.2f s" % (li + 1, " ".join(lines[li][:6]), t0))
        break
json.dump(words_out, open(out_path, "w"), indent=1)
print("aligned", len(words_out), "of", sum(len(l) for l in lines), "words")

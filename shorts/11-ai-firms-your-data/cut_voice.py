"""Short #11: cut the vertical Short's voice from the long-form recording, and remap the word timings.

Parts (first word time, last word time) come from longform/ai-firms-your-data/words.json; each cut sits in the middle
of the pause around it, joins get 15 ms fades and a 0.12 s breath, and the creator's separate "Follow" take ends it.
Writes work/voice_clean.wav (48 kHz mono), words.json (Short timeline) and work/parts.json (where each part starts).
Usage: python3 cut_voice.py
"""
import json

import numpy as np
from scipy.io import wavfile

LF = "../../longform/ai-firms-your-data"
W = json.load(open(f"{LF}/words.json"))
SR, V = wavfile.read(f"{LF}/work/voice_clean.wav")
_, FOLLOW = wavfile.read(f"{LF}/work/follow_clean.wav")
V = V.astype(np.float32); FOLLOW = FOLLOW.astype(np.float32)
# (label, first word ~start, last word ~end) on the long-form timeline
# (C-H moved 2.84 s later on 27 Oct, when the corrected "First thing..." take went into the long recording)
PARTS = [("A", 0.00, 11.18), ("B", 24.21, 39.38), ("C", 80.01, 91.68), ("D", 92.04, 103.38),
         ("E", 126.27, 133.36), ("F", 147.50, 157.73), ("G", 183.72, 191.08), ("H", 208.78, 214.83)]
GAP = 0.12


def word_at(t, key):
    return min(range(len(W)), key=lambda i: abs(W[i][key] - t))


out, words, parts, cursor = [], [], [], 0.0
for lab, a, b in PARTS:
    i0, i1 = word_at(a, "start"), word_at(b, "end")
    prev_end = W[i0 - 1]["end"] if i0 > 0 else 0.0
    next_start = W[i1 + 1]["start"] if i1 + 1 < len(W) else W[i1]["end"] + 0.3
    t0 = max(0.0, (prev_end + W[i0]["start"]) / 2 if i0 > 0 else 0.0)
    t1 = (W[i1]["end"] + next_start) / 2
    t0 = max(t0, W[i0]["start"] - 0.12); t1 = min(t1, W[i1]["end"] + 0.12)
    seg = V[int(t0 * SR):int(t1 * SR)].copy()
    f = int(0.015 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    parts.append({"part": lab, "src": [round(t0, 3), round(t1, 3)], "at": round(cursor, 3), "first": W[i0]["text"], "last": W[i1]["text"]})
    for w in W[i0:i1 + 1]:
        words.append({"text": w["text"], "start": round(w["start"] - t0 + cursor, 3), "end": round(w["end"] - t0 + cursor, 3)})
    out.append(seg); cursor += len(seg) / SR
    out.append(np.zeros(int(GAP * SR), np.float32)); cursor += GAP
# the "Follow" take: trim its own silence
th = np.max(np.abs(FOLLOW)) * 0.02
nz = np.where(np.abs(FOLLOW) > th)[0]
fo = FOLLOW[max(0, nz[0] - int(0.05 * SR)):nz[-1] + int(0.2 * SR)]
parts.append({"part": "End", "src": "follow take", "at": round(cursor, 3)})
trim0 = max(0, nz[0] - int(0.05 * SR)) / SR
# work/follow_words.json: tools/align.py on the take alone (work/follow16k.wav, work/follow.txt)
for x in json.load(open("work/follow_words.json")):
    words.append({"text": x["text"], "start": round(max(x["start"] - trim0, 0.05) + cursor, 3), "end": round(x["end"] - trim0 + cursor, 3)})
out.append(fo); cursor += len(fo) / SR
wav = np.concatenate(out)
wavfile.write("work/voice_clean.wav", SR, np.clip(wav, -32768, 32767).astype(np.int16))
json.dump(words, open("words.json", "w"), indent=0)
json.dump(parts, open("work/parts.json", "w"), indent=1)
print(f"short voice {cursor:.2f} s, {len(words)} words")
for p in parts:
    print(p)

"""Short #12: cut the vertical Short's voice from the long-form recording, and remap the word timings.

Parts are word ranges of longform/this-voice-isnt-me/words.json; each cut sits in the pause around it (at most 0.12 s
from the word), joins get 15 ms fades and a 0.12 s breath. The separate take (work/take_clean.wav, aligned in
work/take_words.json) gives T1 (the hidden-word line + "Follow", words 0-21) and T2 (the Trial Reel's opening, 22-39).
Writes two cuts:
  main   A B C D + T1   -> work/voice_clean.wav, words.json, work/parts.json
  trial  T2 B C D + T1  -> work/voice_trial.wav, words_trial.json, work/parts_trial.json
Usage: python3 cut_voice.py
"""
import json

import numpy as np
from scipy.io import wavfile

LF = "../../longform/this-voice-isnt-me"
W = json.load(open(f"{LF}/words.json"))
SR, V = wavfile.read(f"{LF}/work/voice_clean.wav")
_, TK = wavfile.read("work/take_clean.wav")
TW = json.load(open("work/take_words.json"))
V = V.astype(np.float32); TK = TK.astype(np.float32)
PARTS = {"A": (0, 37), "B": (732, 781), "C": (827, 885), "D": (1135, 1190)}   # hook, three seconds, Hong Kong, the safe phrase
TAKES = {"T1": (0, 21), "T2": (22, 39)}
GAP = 0.12


def piece(src, ws, i0, i1):
    prev_end = ws[i0 - 1]["end"] if i0 > 0 else 0.0
    next_start = ws[i1 + 1]["start"] if i1 + 1 < len(ws) else ws[i1]["end"] + 0.3
    t0 = max(0.0, (prev_end + ws[i0]["start"]) / 2 if i0 > 0 else 0.0)
    t1 = (ws[i1]["end"] + next_start) / 2
    t0 = max(t0, ws[i0]["start"] - 0.12); t1 = min(t1, ws[i1]["end"] + 0.12)
    seg = src[int(t0 * SR):int(t1 * SR)].copy()
    f = int(0.015 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    return seg, t0, ws[i0:i1 + 1]


def build(order, wav_out, words_out, parts_out):
    out, words, parts, cursor = [], [], [], 0.0
    for lab in order:
        if lab in PARTS:
            seg, t0, ws = piece(V, W, *PARTS[lab])
        else:
            seg, t0, ws = piece(TK, TW, *TAKES[lab])
        parts.append({"part": lab, "src": round(t0, 3), "at": round(cursor, 3), "first": ws[0]["text"], "last": ws[-1]["text"]})
        for w in ws:
            words.append({"text": w["text"], "start": round(max(w["start"] - t0, 0.02) + cursor, 3), "end": round(w["end"] - t0 + cursor, 3)})
        out.append(seg); cursor += len(seg) / SR
        if lab != order[-1]:
            out.append(np.zeros(int(GAP * SR), np.float32)); cursor += GAP
    wav = np.concatenate(out)
    wavfile.write(wav_out, SR, np.clip(wav, -32768, 32767).astype(np.int16))
    json.dump(words, open(words_out, "w"), indent=0)
    json.dump(parts, open(parts_out, "w"), indent=1)
    print(f"{wav_out}: {cursor:.2f} s, {len(words)} words")
    for p in parts:
        print("  ", p)


build(["A", "B", "C", "D", "T1"], "work/voice_clean.wav", "words.json", "work/parts.json")
build(["T2", "B", "C", "D", "T1"], "work/voice_trial.wav", "words_trial.json", "work/parts_trial.json")

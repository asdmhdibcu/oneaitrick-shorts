"""Shorten the longer pauses between script lines so #15 ends safely under the 3:00 Shorts limit.

The take is 178.5 s. Every pause between two script lines longer than CAP is cut down to CAP from its middle (with a
10 ms crossfade); the laugh after line 1 is kept whole. Words are never touched. Writes the trimmed 48 kHz and 16 kHz
voices and words.json with every timing moved to the new timeline.

Usage: python3 trim_pauses.py   (reads work/voice_clean.wav, work/words_raw.json, work/script_plain.txt)
"""
import json

import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import resample_poly

CAP = 0.35
KEEP_AFTER_LINES = {1}  # line 1 -> 2 holds the laugh

sr, voice = wavfile.read("work/voice_clean.wav")
voice = voice.astype(np.float32) / 32768
words = json.load(open("work/words_raw.json"))
lines = [l.split() for l in open("work/script_plain.txt").read().splitlines() if l.strip()]

cuts = []  # (cut_start, cut_end) seconds in the original
idx = 0
for li, line in enumerate(lines[:-1], start=1):
    idx += len(line)
    end_prev, start_next = words[idx - 1]["end"], words[idx]["start"]
    gap = start_next - end_prev
    if li in KEEP_AFTER_LINES or gap <= CAP:
        continue
    remove = gap - CAP
    mid = (end_prev + start_next) / 2
    cuts.append((mid - remove / 2, mid + remove / 2))

fade = int(0.010 * sr)
out, pos = [], 0
for a, b in cuts:
    ia, ib = int(a * sr), int(b * sr)
    head = voice[pos:ia].copy()
    tail = voice[ib: ib + fade]
    ramp = np.linspace(0, 1, fade, dtype=np.float32)
    head[-fade:] = head[-fade:] * (1 - ramp) + tail * ramp
    out.append(head)
    pos = ib + fade
out.append(voice[pos:])
trimmed = np.concatenate(out)


def remap(t):
    shift = 0.0
    for a, b in cuts:
        if t >= b:
            shift += (b - a) + fade / sr
        elif t > a:
            return a - shift
    return t - shift


for w in words:
    w["start"] = round(remap(w["start"]), 3)
    w["end"] = round(remap(w["end"]), 3)
json.dump(words, open("words.json", "w"), indent=1)
pcm = np.clip(trimmed * 32768, -32768, 32767).astype(np.int16)
wavfile.write("work/voice_trim.wav", sr, pcm)
wavfile.write("work/voice_trim16k.wav", 16000, np.clip(resample_poly(trimmed, 1, 3) * 32768, -32768, 32767).astype(np.int16))
print("cut %d pauses, %.2f s removed; voice now %.2f s; last word ends %.2f s"
      % (len(cuts), len(voice) / sr - len(trimmed) / sr, len(trimmed) / sr, words[-1]["end"]))

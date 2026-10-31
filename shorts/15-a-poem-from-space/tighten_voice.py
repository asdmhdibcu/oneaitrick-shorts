"""Tighten the pauses in the take so the short fits under 3:00 (the take is 178.5 s).

Removes silence from the middle of every word-to-word gap longer than KEEP seconds, only where the audio is
below -38 dBFS, and shifts the word timings to match. Gaps that carry the delivery are kept as recorded: the laugh
after line 1, the [short pause]s, the "No air. No wind." beat and the whisper.
Reads work/voice_clean.wav + work/words_take.json; writes work/voice_tight.wav, work/voice16k_tight.wav, words.json.
"""
import json
import subprocess

import numpy as np
import scipy.io.wavfile as wavfile

KEEP = 0.24                                  # seconds of pause left in a tightened gap
SKIP_BEFORE = {"Okay,", "Because", "Not", "No", "Space…", "is"}  # gaps before these words are kept

sr, x = wavfile.read('work/voice_clean.wav')
words = json.load(open('work/words_take.json'))

def db(a):
    return 20 * np.log10(np.sqrt(np.mean((a.astype(float) / 32768) ** 2)) + 1e-9)

cuts = []  # (start, end) seconds to remove
for n in range(1, len(words)):
    if words[n]['text'] in SKIP_BEFORE:
        continue
    g0, g1 = words[n - 1]['end'], words[n]['start']
    extra = (g1 - g0) - KEEP
    if extra <= 0.02:
        continue
    mid = (g0 + g1) / 2
    a, b = mid - extra / 2, mid + extra / 2
    if db(x[int(a * sr):int(b * sr)]) > -38:
        print(f'gap before word {n} ({words[n]["text"]}) not silent, kept'); continue
    cuts.append((a, b))

keep, t = [], 0.0
for a, b in cuts:
    keep.append((t, a)); t = b
keep.append((t, len(x) / sr))
fade = int(0.004 * sr)
parts = []
for a, b in keep:
    seg = x[int(a * sr):int(b * sr)].astype(float)
    seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    parts.append(seg)
y = np.concatenate(parts).astype(np.int16)
wavfile.write('work/voice_tight.wav', sr, y)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/voice_tight.wav', '-ar', '16000', '-ac', '1', 'work/voice16k_tight.wav'], check=True)

def shift(t):
    return t - sum(min(b, max(a, t)) - a for a, b in cuts)

for w in words:
    w['start'], w['end'] = round(shift(w['start']), 3), round(shift(w['end']), 3)
json.dump(words, open('words.json', 'w'), indent=0)
print(f'{len(cuts)} gaps tightened, {sum(b - a for a, b in cuts):.2f} s removed; voice now {len(y) / sr:.2f} s, '
      f'last word ends {words[-1]["end"]:.2f} s')

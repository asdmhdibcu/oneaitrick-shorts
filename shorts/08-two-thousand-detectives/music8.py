"""Short #8 score: an original noir track, synthesised (deterministic, royalty-free).

Part A "the investigation" (0 - 66.4 s): D minor pulse - pad, plucked arpeggio, sub bass, ticking hats, soft kick.
The drop: everything stops on "Then... the clue." (66.44 s); a low drone holds until "One wire" (68.04 s).
Part B "the clue" (68.04 - 101.2 s): noir jazz - walking upright bass, ride and brushes, Rhodes chords.
"But careful" (101.17 s): drums out, Rhodes and bass only. Bookend (113.14 s): Part A returns and resolves to D major.
Usage: python3 music8.py OUT.wav LENGTH
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
OUT, LENGTH = sys.argv[1], float(sys.argv[2])
N = int((LENGTH + 2) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(808)
BPM = 96.0; BEAT = 60 / BPM; BAR = 4 * BEAT
DROP, CLUE, CAREFUL, BOOK, END = 66.44, 68.04, 101.17, 113.14, 117.77


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def tt(d):
    return np.arange(int(d * SR)) / SR


def add(sig, t0, pan=0.0, gain=1.0):
    i = int(max(t0, 0) * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    k = min(64, len(sig)); sig = sig.copy(); sig[:k] *= np.linspace(0, 1, k)
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def lp(x, f):
    return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)


def pad(f, d, vel=1.0):
    t = tt(d)
    s = sum(((2 * ((f * k * t + ph) % 1) - 1)) for k, ph in ((1.0, 0), (1.006, 0.3), (0.994, 0.6))) / 3
    env = np.clip(t / 0.6, 0, 1) * np.clip((d - t) / 0.8, 0, 1)
    return 0.05 * vel * lp(s, 1400) * env


def pluck(f, vel=1.0):
    t = tt(0.5)
    s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.05) + 0.2 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / 0.03)
    return 0.07 * vel * s * np.exp(-t / 0.16) * (1 - np.exp(-t / 0.002))


def sub(f, d):
    t = tt(d)
    return 0.22 * np.tanh(1.3 * np.sin(2 * np.pi * f * t)) * np.exp(-t / (d * 0.9)) * (1 - np.exp(-t / 0.01)) * np.clip((d - t) / 0.03, 0, 1)


def kick(g=1.0):
    t = tt(0.4); f = 42 + 85 * np.exp(-t / 0.028)
    return 0.55 * g * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.14)


def tick(g=1.0):
    return 0.05 * g * bp(rng.standard_normal(int(0.04 * SR)), 6000, 13000) * np.exp(-tt(0.04) / 0.008)


def upright(f, d):
    t = tt(d)
    fb = f * (1 + 0.012 * np.exp(-t / 0.03))
    ph = 2 * np.pi * np.cumsum(fb) / SR
    s = np.sin(ph) + 0.5 * np.sin(2 * ph) * np.exp(-t / 0.08) + 0.15 * np.sin(3 * ph) * np.exp(-t / 0.04)
    thump = lp(rng.standard_normal(len(t)), 400) * np.exp(-t / 0.015) * 0.6
    return 0.2 * (s + thump) * np.exp(-t / 0.45) * (1 - np.exp(-t / 0.004)) * np.clip((d - t) / 0.04, 0, 1)


def ride(g=1.0):
    t = tt(0.9)
    n = bp(rng.standard_normal(len(t)), 3500, 12000)
    bell = sum(np.sin(2 * np.pi * f * t) for f in (2950, 4170, 5310)) / 3
    return 0.035 * g * (n * np.exp(-t / 0.35) + 0.5 * bell * np.exp(-t / 0.25))


def brush(d=0.45, g=1.0):
    t = tt(d)
    return 0.04 * g * bp(rng.standard_normal(len(t)), 2000, 9000) * np.sin(np.pi * t / d) ** 2


def rhodes(f, d, vel=1.0):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.3))
    trem = 1 + 0.18 * np.sin(2 * np.pi * 4.5 * t)
    return 0.05 * vel * s * trem * np.exp(-t / 1.6) * (1 - np.exp(-t / 0.004)) * np.clip((d - t) / 0.2, 0, 1)


def riser(t0, d):
    t = tt(d)
    n = rng.standard_normal(len(t)); out = np.zeros_like(n)
    for s in range(0, len(n), 1024):
        fc = 300 + 7000 * (s / len(n)) ** 2
        out[s:s + 1024] = bp(n[s:s + 1024], fc * 0.6, min(fc * 1.6, 18000))
    add(0.12 * out * (t / d) ** 2.2, t0, 0.0)


A = [([62, 65, 69, 72, 76], 38), ([58, 62, 65, 69, 72], 34), ([55, 58, 62, 65, 69], 31), ([57, 61, 64, 67, 70], 33)]   # Dm9 Bbmaj7 Gm9 A7(b9)
B = [([62, 65, 69, 73], 38), ([55, 58, 62, 65], 31), ([52, 55, 58, 62], 28), ([57, 61, 64, 67], 33)]                   # Dm(maj7) Gm7 Em7b5 A7
WALK = [[38, 41, 45, 44], [43, 46, 50, 49], [40, 43, 46, 45], [45, 49, 52, 37]]


def energy(t):
    if t < 10.17: return 3
    if t < 25.5: return 1
    if t < 36.7: return 2
    if t < 55.7: return 3
    if t < 64.9: return 1
    return 0


t = 0.0; b = 0
while t < DROP - 0.01:
    notes, root = A[b % 4]
    e = energy(t)
    for k, n in enumerate(notes[:4]):
        add(pad(midi(n), min(BAR, DROP - t)), t, -0.4 + 0.27 * k)
    for s in range(16):
        ts = t + s * BEAT / 4
        if ts >= DROP: break
        en = energy(ts)
        if en >= 1 and (en >= 2 or s % 2 == 0):
            add(pluck(midi(notes[(s * 3) % 5] + 12), 0.75 if s % 4 else 1.0), ts, 0.3 if s % 2 else -0.3)
        if en >= 3 and s % 4 == 2:
            add(pluck(midi(notes[(s * 5) % 5] + 24), 0.45), ts, 0.5)
        add(tick(1.0 if s % 4 == 0 else 0.55), ts, 0.45)
        if s % 2 == 0 and en >= 1:
            add(sub(midi(root), BEAT / 2 * 0.95), ts)
        if en >= 2 and s in (0, 8, 10):
            add(kick(0.9 if en == 3 else 0.6), ts)
    t += BAR; b += 1
riser(DROP - 1.5, 1.5)
# the drop: a low D drone under "Then... the clue."
d = CLUE - DROP + 0.4
add(0.12 * np.sin(2 * np.pi * midi(26) * tt(d)) * np.clip(tt(d) / 0.3, 0, 1) * np.clip((d - tt(d)) / 0.4, 0, 1), DROP + 0.05)

# Part B: noir jazz, then thinner after "But careful"
t = CLUE; b = 0
while t < BOOK - 0.01:
    notes, root = B[b % 4]
    drums = t < CAREFUL
    for k, n in enumerate(notes):
        for at, ln in ((0.0, 1.4 * BEAT), (2.5 * BEAT, 1.3 * BEAT)):
            if t + at < BOOK:
                add(rhodes(midi(n), ln, 0.9 if at == 0 else 0.6), t + at + 0.01 * k, -0.3 + 0.2 * k)
    for q in range(4):
        tq = t + q * BEAT
        if tq >= BOOK: break
        add(upright(midi(WALK[b % 4][q]), BEAT * 0.95), tq, -0.1, 1.0 if drums else 0.7)
        if drums:
            add(ride(1.0 if q % 2 else 0.8), tq, 0.35)
            add(ride(0.5), tq + BEAT * 2 / 3, 0.35)
            if q % 2 == 1:
                add(brush(0.42, 1.0), tq - 0.12, -0.25)
    t += BAR; b += 1

# Bookend: Part A returns, then resolves to D major on the end card
t = BOOK; b = 0
while t < END - 0.01:
    notes, root = A[b % 4]
    for k, n in enumerate(notes[:4]):
        add(pad(midi(n), min(BAR, END - t + 0.3)), t, -0.4 + 0.27 * k)
    for s in range(16):
        ts = t + s * BEAT / 4
        if ts >= END: break
        add(pluck(midi(notes[(s * 3) % 5] + 12), 0.8 if s % 4 else 1.0), ts, 0.3 if s % 2 else -0.3)
        add(tick(1.0 if s % 4 == 0 else 0.55), ts, 0.45)
        if s % 2 == 0: add(sub(midi(root), BEAT / 2 * 0.95), ts)
        if s in (0, 8, 10): add(kick(0.9), ts)
    t += BAR; b += 1
for k, n in enumerate([50, 57, 62, 66, 69, 76]):  # Dmaj9 rings out
    add(pad(midi(n), LENGTH - END + 1, 1.3), END, -0.5 + 0.2 * k)
    add(rhodes(midi(n + 12), 3.5, 0.7), END + 0.03 * k, -0.4 + 0.16 * k)

mix = np.stack([L, R], 1)
mix = sosfilt(butter(1, 30, btype="high", fs=SR, output="sos"), mix, axis=0)
tt_ = np.arange(N) / SR
fade = np.clip(tt_ / 0.05, 0, 1) * np.clip((LENGTH - tt_) / 3.0, 0, 1)
mix = (mix * fade[:, None])[: int(LENGTH * SR)]
mix = np.tanh(mix * 1.3) / 1.3
mix /= np.max(np.abs(mix)) + 1e-9
wavfile.write(OUT, SR, (mix * 0.8 * 32767).astype(np.int16))
print("wrote", OUT, round(len(mix) / SR, 2), "s")

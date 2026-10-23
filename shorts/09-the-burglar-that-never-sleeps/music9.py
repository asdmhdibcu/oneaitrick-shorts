"""Short #9 score: an original heist track, synthesised (deterministic, royalty-free). 100 BPM, E minor.

A "the break-in" (0 - 39.18): plucked bass ostinato, the ticking clock, a safe-cracker motif up high; kick from "Picture a
  street"; busier from the password spray (31.4); half-time thuds on "jammed shut".
The one silence: the music cuts out on "So how DID it get in?" (39.18) and crashes back in on "KEY" (43.20).
B "the key" (43.2 - 62.1): driving groove, Rhodes stabs; stops dead under the record scratch on "Here's the twist" (62.1).
Drone under the ARTEX reveal (63.4 - 65.2). C "the good guys" (65.2 - 71.1): the same theme in E major, by day.
D "same robot" (71.1 - 76.4): the minor ostinato under the major chords; a riser into "wins" (75.59).
E (76.4 - 81.5): the clock alone, soft; the end card resolves on E major.
Usage: python3 music9.py OUT.wav LENGTH
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
OUT, LENGTH = sys.argv[1], float(sys.argv[2])
N = int((LENGTH + 2) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(909)
BPM = 100.0; BEAT = 60 / BPM; BAR = 4 * BEAT
STREET, SPRAY, JAM, SILENT, KEY, TWIST, ARTEX, GOOD, SAME, WINS, OUTRO, END = (8.30, 31.40, 37.40, 39.18, 43.20, 62.10,
                                                                             63.38, 65.20, 71.10, 75.59, 76.38, 81.50)


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


def pad(f, d, vel=1.0, cut=1400):
    t = tt(d)
    s = sum(((2 * ((f * k * t + ph) % 1) - 1)) for k, ph in ((1.0, 0), (1.006, 0.3), (0.994, 0.6))) / 3
    env = np.clip(t / 0.6, 0, 1) * np.clip((d - t) / 0.8, 0, 1)
    return 0.05 * vel * lp(s, cut) * env


def pluck(f, vel=1.0, dec=0.16):
    t = tt(0.5)
    s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.05) + 0.2 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / 0.03)
    return 0.07 * vel * s * np.exp(-t / dec) * (1 - np.exp(-t / 0.002))


def pizz(f, d, vel=1.0):
    """plucked bass: a short, woody note"""
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.015 * np.exp(-t / 0.02))) / SR
    s = np.sin(ph) + 0.45 * np.sin(2 * ph) * np.exp(-t / 0.05) + 0.12 * np.sin(3 * ph) * np.exp(-t / 0.03)
    thump = lp(rng.standard_normal(len(t)), 500) * np.exp(-t / 0.012) * 0.5
    return 0.21 * vel * (s + thump) * np.exp(-t / 0.22) * (1 - np.exp(-t / 0.003)) * np.clip((d - t) / 0.03, 0, 1)


def sub(f, d):
    t = tt(d)
    return 0.2 * np.tanh(1.3 * np.sin(2 * np.pi * f * t)) * np.exp(-t / (d * 0.9)) * (1 - np.exp(-t / 0.01)) * np.clip((d - t) / 0.03, 0, 1)


def kick(g=1.0):
    t = tt(0.4); f = 42 + 85 * np.exp(-t / 0.028)
    return 0.55 * g * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.14)


def snare(g=1.0):
    t = tt(0.25)
    return 0.12 * g * (bp(rng.standard_normal(len(t)), 1500, 7000) * np.exp(-t / 0.06) + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.03))


def tick(g=1.0):
    return 0.05 * g * bp(rng.standard_normal(int(0.04 * SR)), 6000, 13000) * np.exp(-tt(0.04) / 0.008)


def tock(g=1.0):
    t = tt(0.06)
    return 0.07 * g * bp(rng.standard_normal(len(t)), 900, 2600) * np.exp(-t / 0.012)


def ride(g=1.0):
    t = tt(0.9)
    n = bp(rng.standard_normal(len(t)), 3500, 12000)
    bell = sum(np.sin(2 * np.pi * f * t) for f in (2950, 4170, 5310)) / 3
    return 0.035 * g * (n * np.exp(-t / 0.35) + 0.5 * bell * np.exp(-t / 0.25))


def crash(g=1.0):
    t = tt(2.2)
    return 0.09 * g * bp(rng.standard_normal(len(t)), 3000, 14000) * np.exp(-t / 0.7) * (1 - np.exp(-t / 0.003))


def rhodes(f, d, vel=1.0):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.3))
    trem = 1 + 0.18 * np.sin(2 * np.pi * 4.5 * t)
    return 0.05 * vel * s * trem * np.exp(-t / 1.6) * (1 - np.exp(-t / 0.004)) * np.clip((d - t) / 0.2, 0, 1)


def riser(t0, d, g=0.12):
    t = tt(d)
    n = rng.standard_normal(len(t)); out = np.zeros_like(n)
    for s in range(0, len(n), 1024):
        fc = 300 + 7000 * (s / len(n)) ** 2
        out[s:s + 1024] = bp(n[s:s + 1024], fc * 0.6, min(fc * 1.6, 18000))
    add(g * out * (t / d) ** 2.2, t0, 0.0)


def drone(t0, d, n=28, g=0.1):
    x = tt(d)
    add(g * np.sin(2 * np.pi * midi(n) * x) * (1 + 0.3 * np.sin(2 * np.pi * 0.7 * x)) * np.clip(x / 0.4, 0, 1) * np.clip((d - x) / 0.5, 0, 1), t0)


MIN = [([64, 67, 71, 74, 78], 40), ([60, 64, 67, 71, 74], 36), ([57, 60, 64, 67, 71], 33), ([59, 63, 66, 69, 72], 35)]   # Em9 Cmaj7 Am9 B7(b9)
MAJ = [([64, 68, 71, 75, 78], 40), ([61, 64, 69, 73, 76], 45), ([61, 64, 68, 71, 75], 37), ([63, 66, 71, 75, 78], 35)]   # Emaj9 A(add9) C#m9 B
OST = [0, 0, 12, 0, 7, 0, 10, 7]   # the bass ostinato, in eighths over each root


def groove(t0, t1, chords, energy, ost=True, pads=True, motif=True):
    t = t0; b = 0
    while t < t1 - 0.01:
        notes, root = chords[b % 4]
        if pads:
            for k, n in enumerate(notes[:4]):
                add(pad(midi(n), min(BAR, t1 - t + 0.2)), t, -0.4 + 0.27 * k)
        for s in range(16):
            ts = t + s * BEAT / 4
            if ts >= t1:
                break
            e = energy(ts)
            add(tick(1.0 if s % 4 == 0 else 0.5), ts, 0.45)        # the clock never stops
            if s % 4 == 2:
                add(tock(0.8), ts, -0.35)
            if ost and s % 2 == 0:
                add(pizz(midi(root + OST[s // 2]), BEAT / 2 * 0.9, 1.0 if s % 8 == 0 else 0.8), ts, -0.1)
            if motif and e >= 1 and s in (3, 6, 11, 14):
                add(pluck(midi(notes[(s * 3) % 5] + 12), 0.7), ts, 0.35)
            if e >= 2 and s in (0, 8):
                add(kick(0.8), ts)
            if e >= 2 and s in (4, 12):
                add(snare(0.7 if e == 2 else 1.0), ts, 0.1)
            if e >= 3 and s in (6, 10, 14):
                add(kick(0.55), ts)
            if e >= 3 and s % 2 == 1:
                add(tick(0.7), ts, -0.45)
        t += BAR; b += 1


# A: the break-in
def eA(t):
    if t < STREET: return 1
    if t < SPRAY: return 2
    return 3
groove(0.0, JAM, MIN, eA)
for k, th in enumerate([JAM, JAM + 0.6, JAM + 1.2]):   # "jammed shut": three slow thuds, then nothing
    add(kick(1.0), th); add(sub(midi(28), 0.5), th)
add(pad(midi(52), SILENT - JAM, 0.8, 900), JAM, 0.0)
# the silence (39.18 - 43.20): nothing at all

# B: the key
add(crash(1.0), KEY); add(kick(1.2), KEY); add(sub(midi(28), 0.9), KEY)
def eB(t):
    if t < 50.82: return 2
    return 3
groove(KEY, TWIST, MIN, eB)
# the twist: dead stop (the record scratch is in sfx), a drone under ARTEX
drone(ARTEX - 0.1, GOOD - ARTEX + 0.3, 28, 0.09)
riser(GOOD - 1.2, 1.2, 0.08)
# C: the good guys, by day: the theme in E major, ride instead of the clock's tock
t = GOOD; b = 0
while t < SAME - 0.01:
    notes, root = MAJ[b % 4]
    for k, n in enumerate(notes[:4]):
        add(rhodes(midi(n), 1.4 * BEAT, 0.9), t + 0.01 * k, -0.3 + 0.2 * k)
        add(rhodes(midi(n), 1.3 * BEAT, 0.6), t + 2.5 * BEAT + 0.01 * k, -0.3 + 0.2 * k)
    for q in range(4):
        tq = t + q * BEAT
        if tq >= SAME: break
        add(pizz(midi(root + (0, 7, 12, 7)[q]), BEAT * 0.9, 0.9), tq, -0.1)
        add(ride(0.9), tq, 0.35)
    t += BAR; b += 1
# D: same robot: the minor ostinato under major pads, a riser into "wins"
t = SAME; b = 0
while t < OUTRO - 0.01:
    for k, n in enumerate(MAJ[b % 4][0][:4]):
        add(pad(midi(n), min(BAR, OUTRO - t + 0.2), 0.9), t, -0.4 + 0.27 * k)
    t += BAR; b += 1
groove(SAME, WINS, MIN, lambda x: 3 if x > 74.18 else 2, pads=False)
riser(WINS - 1.4, 1.4, 0.13)
add(crash(0.8), WINS); add(kick(1.1), WINS); add(sub(midi(28), 0.7), WINS)
# E: the clock alone, soft, then the end card resolves on E major
t = OUTRO
while t < END - 0.01:
    add(tick(0.8), t, 0.45); add(tock(0.6), t + BEAT / 2, -0.35)
    t += BEAT
add(pad(midi(52), END - OUTRO + 0.5, 0.7, 900), OUTRO, 0.0)
for k, n in enumerate([40, 52, 59, 64, 68, 71, 75]):   # Emaj9 rings out
    add(pad(midi(n), LENGTH - END + 1, 1.2), END, -0.5 + 0.17 * k)
    add(rhodes(midi(n + 12), 3.8, 0.6), END + 0.03 * k, -0.4 + 0.13 * k)

mix = np.stack([L, R], 1)
mix = sosfilt(butter(1, 30, btype="high", fs=SR, output="sos"), mix, axis=0)
tt_ = np.arange(N) / SR
fade = np.clip(tt_ / 0.05, 0, 1) * np.clip((LENGTH - tt_) / 2.5, 0, 1)
mix = (mix * fade[:, None])[: int(LENGTH * SR)]
# hard mute through the silence and the record scratch, with 20 ms edges
for a, b in ((SILENT, KEY - 0.01), (TWIST, ARTEX - 0.1)):
    g = np.ones(len(mix)); i0, i1 = int(a * SR), int(b * SR); r = int(0.02 * SR)
    g[i0:i1] = 0; g[i0 - r:i0] = np.linspace(1, 0, r); g[i1:i1 + r] = np.linspace(0, 1, r)
    mix *= g[:, None]
mix = np.tanh(mix * 1.3) / 1.3
mix /= np.max(np.abs(mix)) + 1e-9
wavfile.write(OUT, SR, (mix * 0.8 * 32767).astype(np.int16))
print("wrote", OUT, round(len(mix) / SR, 2), "s")

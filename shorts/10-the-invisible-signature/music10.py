"""Short #10 score: an original mystery cue, synthesised (deterministic, royalty-free). 92 BPM, D minor.

A "the secret" (0 - EU law): a music-box motif over a soft pulse and a pizzicato ostinato; a light shaker from "No hidden
  characters". B "the law, the test" (EU law - "Here's the twist"): kick and soft clap, pads.
The one silence: the score stops dead on "Here's the twist" and crashes back in on "TRANSLATED".
C "your own words" (TRANSLATED - "If AI helped"): the groove at full energy, thinning on "a signature doesn't prove".
D "just say so" (to the end): the motif in D major, the end card resolves on Dmaj9.
Times come from words.json via edl.py. Usage: python3 music10.py OUT.wav LENGTH
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

from edl import wt

SR = 44100
OUT, LENGTH = sys.argv[1], float(sys.argv[2])
N = int((LENGTH + 2) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1010)
BPM = 92.0; BEAT = 60 / BPM; BAR = 4 * BEAT
HIDDEN, LAW, TWIST, TRANS, SOFT, SAYSO, LOOP, END = (wt(65) - 0.05, wt(83) - 0.08, wt(137) - 0.06, wt(146) - 0.02, wt(178) - 0.1,
                                                    wt(194) - 0.1, wt(203) - 0.1, wt(210) - 0.08)


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




def mbox(f, vel=1.0, dec=1.1):
    """a music-box tine: bright partials, a quick click, a long ring"""
    t = tt(dec * 2.2)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2.01 * f * t) * np.exp(-t / 0.4) + 0.18 * np.sin(2 * np.pi * 3.98 * f * t) * np.exp(-t / 0.15)
    click = bp(rng.standard_normal(len(t)), 3000, 9000) * np.exp(-t / 0.004) * 0.3
    return 0.06 * vel * (s * np.exp(-t / dec) + click) * (1 - np.exp(-t / 0.002))


def shaker(g=1.0):
    t = tt(0.09)
    return 0.03 * g * bp(rng.standard_normal(len(t)), 5000, 12000) * np.sin(np.pi * np.clip(t / 0.09, 0, 1))


def clap(g=1.0):
    t = tt(0.22)
    n = bp(rng.standard_normal(len(t)), 900, 5000)
    env = sum(np.exp(-np.clip(t - d, 0, None) / 0.012) * (t >= d) for d in (0, 0.011, 0.022)) * 0.6 + np.exp(-t / 0.07) * 0.6
    return 0.07 * g * n * env


MIN = [([62, 65, 69, 72, 76], 38), ([58, 62, 65, 69, 72], 34), ([55, 58, 62, 65, 69], 31), ([57, 61, 64, 67, 70], 33)]   # Dm9 Bbmaj7 Gm9 A7(b9)
MAJ = [([62, 66, 69, 73, 76], 38), ([59, 62, 66, 69, 73], 35), ([55, 59, 62, 66, 69], 31), ([57, 61, 64, 69, 73], 33)]   # Dmaj9 Bm9 Gmaj9 A(add9)
OST = [0, 12, 7, 12, 0, 12, 10, 7]
MOTIF = [(0, 76), (1.5, 74), (2, 72), (3, 69), (4, 77), (5.5, 76), (6, 74), (7, 72)]   # in beats, over two bars


def motif(t0, t1, shift=0, vel=1.0):
    t = t0
    while t < t1 - 0.01:
        for b, n in MOTIF:
            tb = t + b * BEAT
            if tb < t1:
                add(mbox(midi(n + shift), vel), tb, 0.3 * np.sin(b))
        t += 2 * BAR


def groove(t0, t1, chords, energy, pads=True):
    t = t0; b = 0
    while t < t1 - 0.01:
        notes, root = chords[b % 4]
        if pads:
            for k, n in enumerate(notes[:4]):
                add(pad(midi(n), min(BAR, t1 - t + 0.2), 0.8), t, -0.4 + 0.27 * k)
        for s in range(16):
            ts = t + s * BEAT / 4
            if ts >= t1:
                break
            e = energy(ts)
            if s % 4 == 0:
                add(sub(midi(root), BEAT * 0.8) * (0.6 if e < 2 else 0.9), ts)            # the soft pulse
            if s % 2 == 0:
                add(pizz(midi(root + 12 + OST[s // 2]), BEAT / 2 * 0.9, 0.75 if s % 8 else 0.95), ts, -0.15)
            if e >= 1 and s % 2 == 1:
                add(shaker(0.8 if s % 4 == 3 else 0.5), ts, 0.4)
            if e >= 2 and s in (0, 8):
                add(kick(0.7), ts)
            if e >= 2 and s in (4, 12):
                add(clap(0.8 if e == 2 else 1.0), ts, 0.08)
            if e >= 3 and s in (6, 10):
                add(kick(0.5), ts)
            if e >= 3 and s in (2, 6, 10, 14):
                add(tick(0.6), ts, -0.4)
        t += BAR; b += 1


# A: the secret
motif(0.0, LAW, 0, 1.0)
groove(0.0, LAW, MIN, lambda x: 0 if x < HIDDEN else 1)
# B: the law and the test
groove(LAW, TWIST, MIN, lambda x: 2)
motif(LAW, TWIST, 0, 0.6)
add(crash(0.6), LAW)
# the twist: nothing at all until TRANSLATED
riser(TRANS - 1.1, 1.1, 0.06)
add(crash(1.0), TRANS); add(kick(1.2), TRANS); add(sub(midi(26), 0.9), TRANS)
# C: your own words
groove(TRANS, SAYSO, MIN, lambda x: 3 if x < SOFT else 1)
motif(TRANS, SOFT, 12, 0.5)
# D: just say so, in D major; the loop back to frame one; the end card resolves
groove(SAYSO, END, MAJ, lambda x: 1 if x < LOOP else 0)
motif(LOOP, END, 0, 0.9)
for k, n in enumerate([38, 50, 57, 62, 66, 69, 73]):
    add(pad(midi(n), LENGTH - END + 1, 1.1), END, -0.5 + 0.17 * k)
for k, n in enumerate([74, 78, 81, 85]):
    add(mbox(midi(n), 0.9, 1.6), END + 0.12 * k, -0.3 + 0.2 * k)

mix = np.stack([L, R], 1)
mix = sosfilt(butter(1, 30, btype="high", fs=SR, output="sos"), mix, axis=0)
tt_ = np.arange(N) / SR
fade = np.clip(tt_ / 0.05, 0, 1) * np.clip((LENGTH - tt_) / 2.5, 0, 1)
mix = (mix * fade[:, None])[: int(LENGTH * SR)]
g = np.ones(len(mix)); i0, i1 = int(TWIST * SR), int((TRANS - 1.1) * SR); r = int(0.02 * SR)   # the silence (the riser fades in)
g[i0:i1] = 0; g[i0 - r:i0] = np.linspace(1, 0, r); g[i1:i1 + r] = np.linspace(0, 1, r)
mix *= g[:, None]
mix = np.tanh(mix * 1.3) / 1.3
mix /= np.max(np.abs(mix)) + 1e-9
wavfile.write(OUT, SR, (mix * 0.8 * 32767).astype(np.int16))
print("wrote", OUT, round(len(mix) / SR, 2), "s; silence", round(TWIST, 2), "-", round(TRANS, 2))

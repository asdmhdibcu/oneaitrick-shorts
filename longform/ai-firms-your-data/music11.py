"""#11 score (the video and its Short): an original, synthesised cue (deterministic, royalty-free). 90 BPM, A minor,
lifting to C major for "what they changed" and the takeaway.

One plan per edit (plan_video.json, ../../shorts/11-ai-firms-your-data/plan_short.json):
  sections: [t0, t1, "MIN" | "MAJ", energy]   energy 0 pad only, 1 + music box and ticks, 2 + plucked bass,
                                               3 + kick, clap and shaker, 4 + busier kick
  silence:  [[a, b], ...]   hard mute (the twist: "here's the bit nobody's really talking about")
  hits:     [t, ...]        crash + kick + sub (part joins in the Short, the return after a silence)
  risers:   [[t, d], ...]
  end:      t               the final chord rings from here (Cmaj9)
Usage: python3 music11.py PLAN.json OUT.wav LENGTH
"""
import json
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

PLAN, OUT, LENGTH = json.load(open(sys.argv[1])), sys.argv[2], float(sys.argv[3])
SR = 44100
N = int((LENGTH + 2) * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1111)
BPM = PLAN.get("bpm", 90.0); BEAT = 60 / BPM; BAR = 4 * BEAT


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


def pad(f, d, vel=1.0, cut=1300):
    t = tt(d)
    s = sum(((2 * ((f * k * t + ph) % 1) - 1)) for k, ph in ((1.0, 0), (1.006, 0.3), (0.994, 0.6))) / 3
    return 0.05 * vel * lp(s, cut) * np.clip(t / 0.7, 0, 1) * np.clip((d - t) / 0.8, 0, 1)


def mbox(f, vel=1.0):
    t = tt(1.6)
    s = np.sin(2 * np.pi * f * t) + 0.22 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.25) + 0.1 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t / 0.05)
    return 0.045 * vel * s * np.exp(-t / 0.6) * (1 - np.exp(-t / 0.0015))


def pizz(f, d, vel=1.0):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.015 * np.exp(-t / 0.02))) / SR
    s = np.sin(ph) + 0.45 * np.sin(2 * ph) * np.exp(-t / 0.05) + 0.12 * np.sin(3 * ph) * np.exp(-t / 0.03)
    thump = lp(rng.standard_normal(len(t)), 500) * np.exp(-t / 0.012) * 0.5
    return 0.19 * vel * (s + thump) * np.exp(-t / 0.22) * (1 - np.exp(-t / 0.003)) * np.clip((d - t) / 0.03, 0, 1)


def sub(f, d):
    t = tt(d)
    return 0.2 * np.tanh(1.3 * np.sin(2 * np.pi * f * t)) * np.exp(-t / (d * 0.9)) * (1 - np.exp(-t / 0.01)) * np.clip((d - t) / 0.03, 0, 1)


def kick(g=1.0):
    t = tt(0.4); f = 44 + 80 * np.exp(-t / 0.03)
    return 0.5 * g * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.15)


def clap(g=1.0):
    t = tt(0.3); n = bp(rng.standard_normal(len(t)), 900, 6000)
    env = sum(np.exp(-np.clip(t - d, 0, None) / 0.01) * (t >= d) for d in (0, 0.012, 0.024)) / 3 + 0.6 * np.exp(-t / 0.08)
    return 0.09 * g * n * env


def tick(g=1.0):
    return 0.04 * g * bp(rng.standard_normal(int(0.04 * SR)), 6000, 13000) * np.exp(-tt(0.04) / 0.008)


def shaker(g=1.0):
    t = tt(0.09)
    return 0.028 * g * bp(rng.standard_normal(len(t)), 5000, 12000) * np.sin(np.pi * t / 0.09) ** 2


def crash(g=1.0):
    t = tt(2.2)
    return 0.08 * g * bp(rng.standard_normal(len(t)), 3000, 14000) * np.exp(-t / 0.7) * (1 - np.exp(-t / 0.003))


def riser(t0, d, g=0.09):
    t = tt(d); n = rng.standard_normal(len(t)); out = np.zeros_like(n)
    for s in range(0, len(n), 1024):
        fc = 300 + 7000 * (s / len(n)) ** 2
        out[s:s + 1024] = bp(n[s:s + 1024], fc * 0.6, min(fc * 1.6, 18000))
    add(g * out * (t / d) ** 2.2, t0)


CH = {"MIN": [([57, 60, 64, 67, 71], 45), ([53, 57, 60, 64, 67], 41), ([50, 53, 57, 60, 64], 38), ([52, 56, 59, 62, 65], 40)],   # Am9 Fmaj9 Dm9 E7(b9)
      "MAJ": [([60, 64, 67, 71, 74], 48), ([57, 60, 64, 67, 71], 45), ([53, 57, 60, 64, 67], 41), ([55, 59, 62, 67, 69], 43)]}   # Cmaj9 Am9 Fmaj9 G(add9)
OST = [0, 12, 7, 12, 0, 12, 10, 7]
MOTIF = [7, 12, 15, 14, 12, 10, 12, 7]

for t0, t1, key, e in PLAN["sections"]:
    t, b = t0, 0
    while t < t1 - 0.01:
        notes, root = CH[key][b % 4]
        d = min(BAR, t1 - t)
        for k, n in enumerate(notes[:4]):
            add(pad(midi(n), d + 0.2, 0.9 if e else 0.7), t, -0.4 + 0.27 * k)
        for s in range(16):
            ts = t + s * BEAT / 4
            if ts >= t1:
                break
            if e >= 1 and s % 2 == 0:
                add(tick(1.0 if s % 4 == 0 else 0.5), ts, 0.45)
                add(mbox(midi(root + 24 + MOTIF[(s // 2 + b) % 8]), 0.75 if s % 8 == 0 else 0.5), ts, 0.3)
            if e >= 2 and s % 2 == 0:
                add(pizz(midi(root + OST[s // 2]), BEAT / 2 * 0.9, 1.0 if s % 8 == 0 else 0.75), ts, -0.1)
            if e >= 3 and s in ((0, 8) if e == 3 else (0, 6, 8, 14)):
                add(kick(0.8), ts)
            if e >= 3 and s in (4, 12):
                add(clap(0.8), ts, 0.1)
            if e >= 3 and s % 2 == 1:
                add(shaker(0.8), ts, -0.4)
        t += BAR; b += 1
for t0, d in PLAN.get("risers", []):
    riser(t0, d)
for t in PLAN.get("hits", []):
    add(crash(0.8), t); add(kick(1.1), t); add(sub(midi(33), 0.8), t)
END = PLAN["end"]
for k, n in enumerate([36, 48, 55, 59, 62, 64, 67]):   # Cmaj9 rings out
    add(pad(midi(n), LENGTH - END + 1, 1.1), END, -0.5 + 0.17 * k)
    add(mbox(midi(n + 12), 0.7), END + 0.06 * k, -0.4 + 0.13 * k)

mix = np.stack([L, R], 1)
mix = sosfilt(butter(1, 30, btype="high", fs=SR, output="sos"), mix, axis=0)
x = np.arange(N) / SR
mix = (mix * (np.clip(x / 0.05, 0, 1) * np.clip((LENGTH - x) / 2.0, 0, 1))[:, None])[: int(LENGTH * SR)]
for a, b in PLAN.get("silence", []):
    g = np.ones(len(mix)); i0, i1 = int(a * SR), int(b * SR); r = int(0.02 * SR)
    g[i0:i1] = 0; g[i0 - r:i0] = np.linspace(1, 0, r); g[i1:i1 + r] = np.linspace(0, 1, r)
    mix *= g[:, None]
mix = np.tanh(mix * 1.3) / 1.3
mix /= np.max(np.abs(mix)) + 1e-9
wavfile.write(OUT, SR, (mix * 0.8 * 32767).astype(np.int16))
print("wrote", OUT, round(len(mix) / SR, 2), "s")

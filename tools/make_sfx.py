"""Synthesize a deterministic SFX stem from an event list.

Usage: python3 make_sfx.py EVENTS.json OUT.wav
EVENTS.json: {"length": s, "events": [{"type": ..., "t": s, ...}, ...]}
Types: whoosh, boom, pop, ding, scan, ring, rumble, tick, ticks, shimmer, glitch, zap, swell
"""
import json
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
cfg = json.load(open(sys.argv[1]))
N = int((cfg["length"] + 1) * SR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(5)


def add(sig, t0, pan=0.0, gain=1.0):
    i = int(max(t0, 0) * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def tt(d):
    return np.arange(int(d * SR)) / SR


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def whoosh(t, rise=0.45, fall=0.3, g=1.0):
    n = rng.standard_normal(int((rise + fall) * SR))
    out = np.zeros_like(n)
    ch = 480
    for s in range(0, len(n), ch):
        p = min((s / SR) / rise, 1.0)
        fc = 250 + 4500 * p ** 2 if s / SR < rise else 4750 - 3000 * ((s / SR - rise) / fall)
        out[s:s + ch] = bp(n[s:s + ch], max(fc * 0.6, 60), min(fc * 1.7, 20000))
    x = tt(rise + fall)
    env = np.where(x < rise, (x / rise) ** 2.2, np.exp(-(x - rise) / (fall / 3.5)))
    sig = 0.22 * g * out * env
    add(sig, t - rise, -0.3)
    add(sig * 0.85, t - rise + 0.012, 0.3)


def boom(t, g=1.0):
    x = tt(1.6)
    f = 38 + 70 * np.exp(-x / 0.06)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.45)
    click = hp(rng.standard_normal(len(x)), 1500) * np.exp(-x / 0.012) * 0.4
    tail = lp(rng.standard_normal(len(x)), 900) * np.exp(-x / 0.5) * 0.25
    add(0.55 * g * np.tanh(1.6 * (body + click + tail)), t, 0.0)


def pop(t, g=1.0, pitch=1.0):
    x = tt(0.12)
    s = np.sin(2 * np.pi * (700 * pitch + 900 * pitch * np.exp(-x / 0.012)) * x) * np.exp(-x / 0.03)
    add(0.16 * g * s, t, (rng.random() - 0.5) * 0.6)


def ding(t, g=1.0, base=1760):
    x = tt(2.2)
    partials = [(1, 1.0, 1.4), (2.76, 0.5, 0.6), (5.4, 0.25, 0.3), (8.93, 0.12, 0.18)]
    s = sum(a * np.sin(2 * np.pi * base * r * x) * np.exp(-x / d) for r, a, d in partials)
    add(0.11 * g * s * (1 - np.exp(-x / 0.002)), t, 0.1)


def scan(t, dur=0.9, g=1.0):
    x = tt(dur)
    f = 900 + 1400 * (x / dur)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * x))
    env = np.sin(np.pi * x / dur) ** 0.7
    add(0.05 * g * s * env, t, 0.0)


def ring(t, rings=2, g=1.0):
    for k in range(rings):
        t0 = t + k * 0.55
        x = tt(0.4)
        s = (np.sin(2 * np.pi * 1320 * x) + 0.7 * np.sin(2 * np.pi * 1660 * x)) * (np.sin(2 * np.pi * 22 * x) > 0)
        env = np.clip(x / 0.01, 0, 1) * np.clip((0.4 - x) / 0.05, 0, 1)
        add(0.05 * g * s * env, t0, 0.15)


def rumble(t, dur=2.4, g=1.0):
    x = tt(dur)
    base = lp(rng.standard_normal(len(x)), 180) * 1.5
    steps = np.zeros(len(x))
    for k in range(int(dur * 9)):
        tk = k / 9 + rng.random() * 0.05
        i = int(tk * SR)
        st = tt(0.12)
        thud = np.sin(2 * np.pi * (70 + 30 * rng.random()) * st) * np.exp(-st / 0.04)
        steps[i:i + len(st)] += thud[: len(steps) - i] * (0.6 + 0.4 * rng.random())
    env = np.clip(x / 0.5, 0, 1) * np.clip((dur - x) / 0.6, 0, 1)
    add(0.35 * g * (base + steps) * env, t, 0.0)


def tick(t, g=1.0):
    x = tt(0.03)
    s = hp(rng.standard_normal(len(x)), 3000) * np.exp(-x / 0.004)
    add(0.12 * g * s, t, (rng.random() - 0.5) * 0.4)


def shimmer(t, g=1.0):
    notes = [2093, 2637, 3136, 3951, 4186]
    for k, f in enumerate(notes):
        x = tt(0.9)
        s = np.sin(2 * np.pi * f * x) * np.exp(-x / 0.35) * (1 - np.exp(-x / 0.003))
        add(0.035 * g * s, t + k * 0.05, -0.4 + 0.2 * k)


def glitch(t, dur=0.35, g=1.0):
    x = tt(dur)
    n = rng.standard_normal(len(x))
    gate = (np.sin(2 * np.pi * 37 * x) > 0.2).astype(float)
    s = bp(n, 1500, 7000) * gate + 0.4 * np.sign(np.sin(2 * np.pi * 220 * x)) * (1 - gate)
    add(0.06 * g * s * np.exp(-x / (dur * 0.8)), t, 0.0)


def zap(t, g=1.0):
    x = tt(0.35)
    f = 2400 * np.exp(-x / 0.08) + 200
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-x / 0.1)
    add(0.05 * g * lp(s, 6000), t, 0.0)


def swell(t, dur=1.4, g=1.0):
    x = tt(dur)
    n = lp(rng.standard_normal(len(x)), 2500)
    env = (x / dur) ** 2.5
    add(0.12 * g * n * env, t, 0.0)


FUN = {"whoosh": whoosh, "boom": boom, "pop": pop, "ding": ding, "scan": scan, "ring": ring, "rumble": rumble,
       "tick": tick, "shimmer": shimmer, "glitch": glitch, "zap": zap, "swell": swell}
for ev in cfg["events"]:
    ev = dict(ev)
    kind = ev.pop("type")
    t = ev.pop("t")
    if kind == "ticks":
        n = ev.get("n", 12)
        dur = ev.get("dur", 1.0)
        for k in range(n):
            tick(t + dur * (k / n) ** 1.4, ev.get("g", 1.0))
        continue
    FUN[kind](t, **ev)

mix = np.stack([L, R], axis=1)[: int(cfg["length"] * SR)]
peak = np.max(np.abs(mix)) + 1e-9
mix = mix / peak * 0.85
wavfile.write(sys.argv[2], SR, (mix * 32767).astype(np.int16))
print("wrote", sys.argv[2], "peak was", round(peak, 3))

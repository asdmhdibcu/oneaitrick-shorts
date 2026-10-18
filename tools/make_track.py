"""Generate an original, royalty-free backing track with transition SFX (deterministic).

Usage: python3 make_track.py CONFIG.json OUT.wav
CONFIG keys:
  length (s), bpm, seed, style ("lofi" | "pulse" | "dream"),
  chords: [[midi notes...], ...] one per bar, bass: [root midi per bar],
  whooshes: [times in s]  -> filtered-noise sweeps that peak at each time,
  pops: [times in s]      -> short soft clicks for on-screen hits,
  drums_from: bar index where drums start, outro: seconds of fade-out
"""
import json
import sys
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

cfg = json.load(open(sys.argv[1]))
out_path = sys.argv[2]
SR = 44100
LENGTH = float(cfg["length"])
BPM = float(cfg["bpm"])
BEAT = 60.0 / BPM
BAR = 4 * BEAT
STYLE = cfg.get("style", "lofi")
rng = np.random.default_rng(int(cfg.get("seed", 1)))
N = int((LENGTH + 2.0) * SR)
L = np.zeros(N)
R = np.zeros(N)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def add(sig, t0, pan=0.0, gain=1.0):
    i = int(max(t0, 0) * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def keys(freq, dur=2.4, vel=1.0):
    t = np.arange(int(dur * SR)) / SR
    if STYLE == "dream":
        env = (1 - np.exp(-t / 0.25)) * np.exp(-t / 2.2)
        tone = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 1.005 * t) + 0.25 * np.sin(2 * np.pi * 2 * freq * t)
    elif STYLE == "pulse":
        env = np.exp(-t / 0.35) * (1 - np.exp(-t / 0.003))
        saw = 2 * ((freq * t) % 1.0) - 1
        tone = 0.45 * saw + np.sin(2 * np.pi * freq * t)
    else:
        env = np.exp(-t / 1.1) * (1 - np.exp(-t / 0.004))
        tone = (np.sin(2 * np.pi * freq * t)
                + 0.35 * np.sin(2 * np.pi * 2 * freq * t + 0.3) * np.exp(-t / 0.5)
                + 0.5 * np.sin(2 * np.pi * freq * 1.003 * t))
    release = np.clip((dur - t) / 0.15, 0, 1)
    return 0.10 * vel * tone * env * release


def bass(freq, dur=1.0):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t / 0.5) * (1 - np.exp(-t / 0.006))
    s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * 2 * freq * t)
    return 0.30 * np.tanh(1.4 * s) * env * np.clip((dur - t) / 0.08, 0, 1)


def kick():
    t = np.arange(int(0.35 * SR)) / SR
    f = 45 + 80 * np.exp(-t / 0.03)
    return 0.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.13)


def noise(dur, lo, hi, decay):
    n = rng.standard_normal(int(dur * SR))
    sos = butter(2, [lo, hi], btype="band", fs=SR, output="sos")
    t = np.arange(len(n)) / SR
    return sosfilt(sos, n) * np.exp(-t / decay)


def snare():
    t = np.arange(int(0.25 * SR)) / SR
    return 0.22 * noise(0.25, 1200, 6000, 0.07) + 0.15 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)


def hat(open_=False):
    return 0.07 * noise(0.12 if open_ else 0.05, 7000, 14000, 0.04 if open_ else 0.012)


def whoosh(peak_t, rise=0.55, fall=0.35):
    dur = rise + fall
    n = rng.standard_normal(int(dur * SR))
    t = np.arange(len(n)) / SR
    # Sweep a band-pass upward by processing in chunks
    out = np.zeros_like(n)
    chunk = 512
    for s in range(0, len(n), chunk):
        p = min(t[s] / rise, 1.0)
        fc = 300 + 5200 * p ** 2
        sos = butter(2, [fc * 0.6, min(fc * 1.6, 18000)], btype="band", fs=SR, output="sos")
        out[s:s + chunk] = sosfilt(sos, n[s:s + chunk])
    env = np.where(t < rise, (t / rise) ** 2, np.exp(-(t - rise) / (fall / 3)))
    sig = 0.20 * out * env
    add(sig, peak_t - rise, -0.2)
    add(sig * 0.9, peak_t - rise + 0.01, 0.2)


def pop(t0):
    t = np.arange(int(0.08 * SR)) / SR
    s = 0.12 * np.sin(2 * np.pi * (900 + 600 * np.exp(-t / 0.01)) * t) * np.exp(-t / 0.02)
    add(s, t0, 0.0)


chords = cfg["chords"]
bassline = cfg["bass"]
drums_from = int(cfg.get("drums_from", 1))
bars = int(np.ceil(LENGTH / BAR))
for b in range(bars):
    tb = b * BAR
    notes = chords[b % len(chords)]
    root = bassline[b % len(bassline)]
    for k, n in enumerate(notes):
        pan = -0.35 + 0.7 * k / max(len(notes) - 1, 1)
        if STYLE == "pulse":
            for e in range(8):  # 8th-note stabs
                add(keys(midi(n), dur=0.3, vel=0.7 if e % 2 else 1.0), tb + e * 0.5 * BEAT + 0.004 * k, pan)
        else:
            add(keys(midi(n), dur=BAR * 0.98), tb + 0.012 * k, pan)
            if STYLE == "lofi":
                add(keys(midi(n), dur=1.1, vel=0.45), tb + 2.5 * BEAT + 0.01 * k, pan)
    if STYLE != "pulse":
        add(keys(midi(notes[-1] + 12), dur=1.0, vel=0.35), tb + 1.5 * BEAT, 0.3)
    if b >= drums_from:
        add(bass(midi(root)), tb)
        add(bass(midi(root + 7), dur=0.5), tb + 2.5 * BEAT)
        add(kick(), tb)
        add(kick(), tb + 2.5 * BEAT, gain=0.8)
        if STYLE == "pulse":
            add(kick(), tb + 2 * BEAT, gain=0.9)
        add(snare(), tb + BEAT, 0.1)
        add(snare(), tb + 3 * BEAT, 0.1)
        for e in range(8):
            swing = 0.06 * BEAT if (e % 2 and STYLE == "lofi") else 0.0
            add(hat(open_=(e == 7)), tb + e * 0.5 * BEAT + swing, 0.4, gain=1.0 if e % 2 == 0 else 0.6)

for w in cfg.get("whooshes", []):
    whoosh(float(w))
for p in cfg.get("pops", []):
    pop(float(p))

mix = np.stack([L, R], axis=1)
mix = sosfilt(butter(2, 9000 if STYLE != "lofi" else 7500, btype="low", fs=SR, output="sos"), mix, axis=0)
mix = sosfilt(butter(1, 30, btype="high", fs=SR, output="sos"), mix, axis=0)
t = np.arange(N) / SR
outro = float(cfg.get("outro", 2.0))
fade = np.clip(t / 0.25, 0, 1) * np.clip((LENGTH - t) / outro, 0, 1)
mix = (mix * fade[:, None])[: int(LENGTH * SR)]
mix = np.tanh(mix * 1.2) / 1.2
mix /= np.max(np.abs(mix)) + 1e-9
wavfile.write(out_path, SR, (mix * 0.8 * 32767).astype(np.int16))
print("wrote", out_path, round(len(mix) / SR, 2), "s")

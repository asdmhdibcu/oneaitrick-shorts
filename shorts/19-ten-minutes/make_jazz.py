"""Short #19's score: an original West-Coast cool-jazz combo, synthesised in numpy (no samples):
vibraphone (bar partials 1:4:10 with motor tremolo), pizzicato walking bass, brushes, ride and finger snaps.
The arrangement follows the story (MIRROR the style's sound palette: a vibraphone chord per chapter that comes back
once per pin in the recap; half-time feel for the wobble; up a step for the payoff; the one silence before the wheels
come off; a dead stop on "weird"). Usage: python3 make_jazz.py words.json work/music_raw.wav
"""
import json
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
W = json.load(open(sys.argv[1]))
wt = lambda k: W[k]["start"]  # noqa: E731
DUR = round(W[-1]["end"] + 0.1, 2)
N = int((DUR + 3) * SR)
rng = np.random.default_rng(19)
stems = {k: np.zeros((N, 2)) for k in ("vib", "bass", "drums")}

BPM = 116.0
B = 60.0 / BPM
SW = 0.64                     # swing: the off-beat eighth sits at 64 % of the beat


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def add(stem, x, t, pan=0.0, gain=1.0):
    i = int(round(t * SR))
    if i >= N or i + len(x) <= 0:
        return
    if i < 0:
        x = x[-i:]; i = 0
    j = min(N, i + len(x))
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    stems[stem][i:j, 0] += gain * l * x[: j - i]
    stems[stem][i:j, 1] += gain * r * x[: j - i]


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def lp(x, f, o=2):
    return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)


# ---------------------------------------------------------------- instruments
def vib(m, dur, vel=0.5, trem=0.25, damp=True):
    f = hz(m)
    n = int((dur + 2.6) * SR)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t / 2.4) * (1 + trem * np.sin(2 * np.pi * 5.6 * t))
         + 0.22 * vel * np.sin(2 * np.pi * f * 4.0 * t) * np.exp(-t / 0.55)
         + 0.05 * vel * np.sin(2 * np.pi * f * 10.0 * t) * np.exp(-t / 0.16))
    x *= np.minimum(1, t / 0.002)
    if damp:                                     # the pedal lifts: damped after dur
        x *= np.where(t < dur, 1.0, np.exp(-(t - dur) / 0.12))
    click = bp(rng.standard_normal(int(0.012 * SR)), 2500, 7000) * np.linspace(1, 0, int(0.012 * SR)) * 0.08
    x[: len(click)] += click
    return x * vel


def chord(t, notes, dur, vel=0.4, pan=-0.25, gain=1.0, trem=0.25, strum=0.012):
    for i, m in enumerate(sorted(notes)):
        add("vib", vib(m, dur, vel * (0.9 + 0.1 * rng.random()), trem), t + i * strum + rng.uniform(-0.003, 0.003),
            pan + (i - 1.5) * 0.08, gain)


def bass(t, m, dur=None, vel=0.6):
    f = hz(m)
    dur = dur or 0.9 * B
    n = int((dur + 0.4) * SR)
    tt = np.arange(n) / SR
    x = np.zeros(n)
    for k in range(1, 8):
        x += np.sin(2 * np.pi * f * k * tt + rng.uniform(0, 0.3)) / k ** 1.25 * np.exp(-tt / (0.6 / (1 + 0.5 * k)))
    x *= np.minimum(1, tt / 0.004)
    thump = lp(rng.standard_normal(int(0.03 * SR)), 300) * np.exp(-np.arange(int(0.03 * SR)) / (0.006 * SR)) * 0.6
    x[: len(thump)] += thump
    x *= np.where(tt < dur, 1.0, np.exp(-(tt - dur) / 0.06))
    add("bass", lp(x, 1400) * vel, t, 0.0)


def brush_sweep(t, d=0.32, g=1.0):
    n = int(d * SR)
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5
    add("drums", bp(rng.standard_normal(n), 2600, 9000) * e * 0.05 * g, t, 0.25)


def brush_tap(t, g=1.0):
    n = int(0.09 * SR)
    add("drums", bp(rng.standard_normal(n), 900, 5200) * np.exp(-np.arange(n) / (0.018 * SR)) * 0.16 * g, t, 0.15)


RIDE_F = [3150, 4230, 5370, 6620, 7890, 9120]


def ride(t, g=1.0):
    n = int(1.0 * SR)
    tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * tt + i) for i, f in enumerate(RIDE_F)) / 6 * np.exp(-tt / 0.5)
    x += hp(rng.standard_normal(n), 6000) * np.exp(-tt / 0.06) * 0.6
    add("drums", x * 0.028 * g, t, 0.35)


def snap(t, g=1.0):
    n = int(0.05 * SR)
    tt = np.arange(n) / SR
    x = bp(rng.standard_normal(n), 1500, 3800) * np.exp(-tt / 0.008) + 0.3 * np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt / 0.01)
    add("drums", x * 0.22 * g, t, -0.35)


# ---------------------------------------------------------------- harmony (F major; up a step to G after the hints)
PROG = [("F", [57, 60, 64, 67], 41), ("Dm", [53, 57, 60, 64], 38), ("Gm", [58, 62, 65, 69], 43), ("C", [58, 64, 69, 74], 36)]
STING = {"WHEELS": [53, 57, 60, 64, 67], "WOBBLE": [50, 53, 57, 60, 64], "WHY": [58, 62, 65, 69, 76],
         "HINTS": [55, 59, 62, 66, 69], "TRYIT": [55, 59, 64, 69, 71]}

T_SIL0, T_SIL1 = wt(30) - 0.1, wt(36)            # the one silence: "Then, without warning..." until OFF
T_STOP0, T_STOP1 = wt(85), wt(87)                # the dead stop: "weird" until "People"
T_UP = wt(87)                                    # up a step from the hints
T_CATCH0, T_CATCH1 = wt(102), wt(115)            # the catch: bass and brushes only
T_RECAP, T_MIRROR = wt(136), wt(151)
WOB0, WOB1 = wt(37), wt(68)                       # half-time feel for the wobble


def section(t):
    if t < WOB0:
        return "full"
    if t < WOB1:
        return "half"
    if t < T_CATCH0:
        return "full"
    if t < T_CATCH1:
        return "thin"
    if t < T_RECAP:
        return "full"
    if t < T_MIRROR:
        return "bed"
    return "full"


def key(t):
    return 2 if T_UP <= t < T_MIRROR else 0


nbars = int(DUR / (4 * B)) + 2
for b in range(nbars):
    t0 = b * 4 * B
    name, voic, root = PROG[b % 4]
    nxt = PROG[(b + 1) % 4][2]
    sec, k = section(t0), key(t0)
    beat = lambda i, sw=False: t0 + i * B + (SW * B if sw else 0)  # noqa: E731
    # vibraphone comping (Charleston), sparse in the half feel, out in the thin and bed sections
    if sec == "full":
        chord(beat(0), [m + k for m in voic], 1.4 * B, 0.34)
        chord(beat(1, True), [m + k for m in voic], 0.5 * B, 0.26)
    elif sec == "half":
        chord(beat(0), [m + k - 12 * 0 for m in voic], 2.6 * B, 0.27, trem=0.45)
    # walking bass
    if sec in ("full", "thin", "bed"):
        walk = [root, root + 7, root + 12 if root < 40 else root + 4, nxt - 1]
        for i, m in enumerate(walk):
            bass(beat(i), m + k, vel=0.55 if sec != "bed" else 0.4)
    elif sec == "half":
        bass(beat(0), root + k, 1.8 * B, 0.55); bass(beat(2), root + 7 + k, 1.8 * B, 0.5)
    # drums
    for i in range(4):
        if sec in ("full", "thin", "bed", "half"):
            brush_sweep(beat(i) - 0.04, 0.34 if sec != "half" else 0.6, 0.9 if sec != "bed" else 0.6)
        if i in (1, 3) and sec != "half":
            brush_tap(beat(i), 1.0 if sec != "bed" else 0.6)
        if sec == "full":
            ride(beat(i), 0.8 if i % 2 == 0 else 1.0)
            if i in (1, 3):
                ride(beat(i, True), 0.6)
        if sec == "half" and i == 2:
            brush_tap(beat(i), 0.9)
    if sec == "full" and T_UP <= t0 < T_RECAP:
        snap(beat(1)); snap(beat(3))

# chapter stingers (each chapter its own chord) and the recap (one chord per pin, in story order)
CH = [(0.0, "WHEELS"), (wt(37), "WOBBLE"), (wt(68), "WHY"), (wt(87), "HINTS"), (wt(115), "TRYIT")]
for t, n in CH:
    chord(t, STING[n], 2.4, 0.5, pan=-0.1, trem=0.3, strum=0.02)
RECAP = [wt(136) + d for d in (0.1, 0.8, 1.5, 2.2, 2.6, 3.1, 3.6)]   # the pins light (film19.js RECAP)
PIN_CH = ["WHEELS", "WOBBLE", "WOBBLE", "WOBBLE", "HINTS", "HINTS", "TRYIT"]
for t, n in zip(RECAP, PIN_CH):
    chord(t, STING[n], 1.0, 0.28, pan=0.0, trem=0.3, strum=0.015)
# the WHY glissando down on "so we never learn to balance"; the payoff bell chord when the hand lets go
g0 = wt(77) - 0.05
for i, m in enumerate([86, 83, 81, 79, 76, 74, 72, 69, 67, 64]):
    add("vib", vib(m, 0.5, 0.3 - i * 0.015), g0 + i * 0.05, -0.3 + i * 0.06)
chord(wt(134), [m + 2 for m in [53, 57, 60, 64, 67, 72]], 2.6, 0.5, pan=0.0, trem=0.35, strum=0.03)
chord(T_MIRROR - 0.02, STING["WHEELS"] + [72], 2.8, 0.5, pan=0.0, trem=0.35, strum=0.03)        # end card

# ---------------------------------------------------------------- the silences, the stop, the room
mix = stems["vib"] * 0.9 + stems["bass"] * 1.1 + stems["drums"] * 1.0
ir_n = int(0.9 * SR)
ir = rng.standard_normal((ir_n, 2)) * np.exp(-np.arange(ir_n) / (0.22 * SR))[:, None]
ir /= np.sqrt((ir ** 2).sum(axis=0))
wet = np.stack([fftconvolve(mix[:, c], ir[:, c])[:N] for c in range(2)], axis=1)
mix = mix + 0.22 * wet
tt = np.arange(N) / SR
gain = np.ones(N)
gain[(tt >= T_SIL0 + 0.08) & (tt < T_SIL1 - 0.02)] = 0.0
ramp = (tt >= T_SIL0) & (tt < T_SIL0 + 0.08); gain[ramp] = 1 - (tt[ramp] - T_SIL0) / 0.08
ramp = (tt >= T_SIL1 - 0.02) & (tt < T_SIL1); gain[ramp] = (tt[ramp] - (T_SIL1 - 0.02)) / 0.02
# tape stop on "weird": the pitch and the level fall over 0.25 s, then nothing until "People"
s0 = int(T_STOP0 * SR); L = int(0.25 * SR)
src = s0 + np.cumsum(np.linspace(1.0, 0.0, L))
seg_ = np.stack([np.interp(src, np.arange(N), mix[:, c]) for c in range(2)], axis=1) * np.linspace(1, 0, L)[:, None]
mix[s0:s0 + L] = seg_
gain[(tt >= T_STOP0 + 0.25) & (tt < T_STOP1)] = 0.0
mix *= gain[:, None]
mix = mix[: int(DUR * SR)]
mix /= np.max(np.abs(mix)) / 0.89
wavfile.write(sys.argv[2], SR, (mix * 32767).astype(np.int16))
print("wrote", sys.argv[2], round(DUR, 2), "s")

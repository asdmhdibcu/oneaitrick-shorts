"""Short #19 audio: the cool-jazz score (make_jazz.py) with the one silence before the wheels come off and a dead stop
on "weird"; our synth hits (tools/make_sfx.py); the style's foley synthesised here (rubber stamps, a slide whistle,
pencil scratches, the iris "shhk", the wheels' clank and rattle, a mantel-clock tick); a sound pass from the
sound-effects skill's CC0 library; the mix with the creator's voice at -14 LUFS (tools/mix.py ... deep) -> assets/mix.wav.
The odometer ticks run to the last frame and pick up on frame one, so the loop is seamless.
Writes sfx.json and cc0.json (committed) and work/*.wav. Usage: python3 make_audio.py
"""
import json
import os
import subprocess

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

T = "../../tools/"
LIB = "../../.claude/skills/sound-effects/sfx/"
SR = 48000
W = json.load(open("words.json"))
wt = lambda k: W[k]["start"]  # noqa: E731
DUR = round(W[-1]["end"] + 0.1, 2)
rng = np.random.default_rng(1919)


def run(cmd):
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


os.makedirs("work", exist_ok=True)
SIL0, SIL1 = wt(30) - 0.1, wt(36)          # the one silence ("Then, without warning..."), voice only
STOP0, STOP1 = wt(85) + 0.25, wt(87)       # after the tape stop on "weird": room tone only

# ---------------------------------------------------------------- score
run(["python3", "make_jazz.py", "words.json", "work/music.wav"])

# ---------------------------------------------------------------- our synth hits (tools/make_sfx.py)
ev = []
E = lambda kind, t, **kw: ev.append(dict({"type": kind, "t": round(t, 3)}, **kw))  # noqa: E731
E("sub", 0.0, g=1.0)
def odo_ticks(p, t0, t1, g):                                                     # a tick each time a digit passes
    ts = np.linspace(t0, t1, 4000); ps = np.array([p(t) for t in ts]); prev = np.floor(ps[0])
    for t, v in zip(ts, ps):
        if np.floor(v) != prev:
            prev = np.floor(v); E("tick", t, g=g)
E("pop", 0.03, pitch=0.85, g=0.7)                                               # the 10 bumps on frame one
E("pop", wt(9) + 0.02, pitch=0.8, g=0.9)                                         # TWICE (keyword pop)
E("whoosh", wt(12) - 0.02, rise=0.12, fall=0.2, g=0.45)                         # crash zoom into the wheels
E("pop", wt(12) + 0.2, pitch=1.1); E("pop", wt(17) - 0.05, pitch=1.25)          # call-out, tag
E("whoosh", wt(19) - 0.05, rise=0.3, fall=0.45, g=0.4)                          # the pull-back
E("ticks", wt(21), dur=0.8, n=14, g=0.55)                                        # 1,222 counts up
E("pop", wt(24) + 0.05, pitch=0.9)                                               # pin 1 parks
for i in range(10):                                                              # half the crowd gets wheels
    E("pop", wt(26) + i * 0.06, pitch=1.0 + 0.05 * i, g=0.55)
E("clink", wt(36), g=1.0, pitch=0.7); E("boom", wt(36), g=0.3)                  # OFF: the clank
E("pop", wt(36), pitch=0.7, g=0.8)
for i in range(9):                                                               # the wheels rattle away
    E("clink", wt(36) + 0.12 + i * 0.09 * (1 + i * 0.12), g=0.45 * (1 - i / 10), pitch=1.3 + 0.1 * (i % 3))
for t in (wt(37) + 0.3, wt(40), wt(44), 20.6, 23.0, 25.3, 27.0):                 # the wobble creaks
    E("creak", t, dur=0.45, g=0.5, pitch=1.1)
E("ticks", wt(40), dur=0.9, n=12, g=0.5); E("pop", wt(40) + 0.05, pitch=0.85); E("pop", wt(40) + 0.12, pitch=1.0)   # the bars
E("pop", wt(40) + 2.25, pitch=0.9)                                               # pin 2
E("ticks", wt(51) + 0.45, dur=0.75, n=20, g=0.45)                               # the grids fill
E("pop", wt(55), pitch=0.9)                                                      # pin 3
E("pop", wt(56) + 0.02, pitch=1.15)                                              # the book
E("ding", wt(60), base=2093, g=0.35)                                             # ONE skip
for i in range(8):                                                               # EIGHT, rising
    E("ding", wt(65) + 0.35 + i * (wt(67) - wt(65) - 0.4) / 7, base=1046 * 2 ** (i / 12 * 2), g=0.22)
E("pop", wt(67) + 0.32, pitch=0.9)                                               # pin 4
E("pop", wt(68) + 0.35, pitch=1.1); E("pop", wt(68) + 0.45, pitch=1.2)           # the wheels pop back on
E("ding", wt(75), base=1568, g=0.45); E("whoosh", wt(75) + 0.05, rise=0.1, fall=0.25, g=0.35)   # INSTANT: the answer flies
E("pop", wt(77), pitch=1.0); E("pop", wt(82) - 0.05, pitch=1.2); E("tick", wt(82) + 0.1, g=0.8)   # the level, BALANCE 0
E("shimmer", wt(85), g=0.4)                                                      # "weird": the sparkle
E("pop", wt(87) + 0.1, pitch=0.95); E("whoosh", wt(87) + 0.2, rise=0.15, fall=0.25, g=0.3)   # the helper, its arm
E("clink", wt(87) + 0.1, g=0.4, pitch=1.2)                                       # the training wheels drop away
E("pop", wt(92) - 0.03, pitch=1.2); E("ding", wt(92) + 0.02, base=1318, g=0.3)   # HINT card
E("pop", wt(93) + 0.8, pitch=0.85); E("pop", wt(93) + 0.9, pitch=0.95); E("pop", wt(93) + 1.75, pitch=1.2)   # bars, the "≈"
E("pop", wt(101), pitch=0.9)                                                     # pin 5
E("boom", wt(102) - 0.02, g=0.4)                                                 # THE CATCH
E("scan", wt(105) - 0.05, dur=0.45, g=0.55); E("scan", wt(105) + 0.25, dur=0.35, g=0.5)   # highlights
E("pop", wt(112) + 0.1, pitch=1.1); E("pop", wt(114), pitch=0.9)                 # magnifier, pin 6
E("whoosh", wt(115) + 0.05, rise=0.15, fall=0.25, g=0.35)                        # the prompt card slides up
E("pop", wt(121), pitch=1.2)                                                     # HINT keyword pop
E("whoosh", wt(125) + 0.05, rise=0.08, fall=0.3, g=0.35); E("pop", wt(125) + 0.17, pitch=1.15)   # send, the HINT card comes back
E("whoosh", wt(126) - 0.1, rise=0.2, fall=0.25, g=0.3)                           # pull back
E("ding", wt(134), base=1568, g=0.45)                                            # the hand lets go: the bell
for i in range(3):
    E("pop", wt(135) + 0.2 + i * 0.35, pitch=1.0 + 0.1 * i, g=0.6)              # mustard checks
E("pop", wt(135) + 0.02, pitch=0.9)                                              # pin 7
E("pop", wt(149), pitch=1.3, g=1.1); E("tick", wt(149) + 0.05, g=1.4)            # THE WORD?
E("swell", wt(151) - 0.5, dur=0.55, g=0.3); E("shimmer", wt(151), g=0.35)        # end card
E("pop", wt(151) + 0.35, pitch=1.2)                                              # FOLLOW pill
E("whoosh", wt(158) - 0.12, rise=0.15, fall=0.2, g=0.3); E("pop", wt(158) + 0.05, pitch=1.0)   # the claim card comes back
O0, O1 = wt(158) + 0.1, wt(158) + 0.9                                       # the claim card counts 00 -> 10 in 0.8 s, then holds
odo_ticks(lambda t: 10 * (1 - (1 - (t - O0) / (O1 - O0)) ** 3), O0, O1, 0.6)
E("swell", DUR - 0.6, dur=0.6, g=0.35)                                           # sub swell into the cut
ev.sort(key=lambda e: e["t"])
json.dump({"length": DUR, "events": ev}, open("sfx.json", "w"), indent=0)
run(["python3", T + "make_sfx.py", "sfx.json", "work/sfx.wav"])

# ---------------------------------------------------------------- the style's foley, synthesised
n = int((DUR + 1) * SR)
fol = np.zeros((n, 2))


def place(x, t, pan=0.0, g=1.0):
    i = int(t * SR); j = min(n, i + len(x))
    if i >= n:
        return
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    fol[i:j, 0] += g * l * x[: j - i]; fol[i:j, 1] += g * r * x[: j - i]


def filt(x, lo, hi, kind="band"):
    return sosfilt(butter(2, [lo, hi] if kind == "band" else lo, kind, fs=SR, output="sos"), x)


def stamp(t, g=1.0):           # a damped rubber stamp: a low thud and a paper slap
    m = int(0.25 * SR); x = np.arange(m) / SR
    thud = np.sin(2 * np.pi * (90 + 60 * np.exp(-x / 0.02)) * x) * np.exp(-x / 0.05)
    slap = filt(rng.standard_normal(m), 600, 3500) * np.exp(-x / 0.018) * 0.7
    place((thud + slap) * 0.5, t, 0.0, g)


def slide_whistle(t, up=True, d=0.45, g=1.0):
    m = int(d * SR); x = np.arange(m) / SR
    f = (700 + 900 * (x / d) ** 0.8) if up else (1500 - 900 * (x / d) ** 0.8)
    f = f * (1 + 0.012 * np.sin(2 * np.pi * 6 * x))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.15 * filt(rng.standard_normal(m), 1000, 4000)
    place(s * np.sin(np.pi * x / d) ** 0.6 * 0.12, t, 0.2, g)


def shhk(t, g=1.0):            # the iris: a fast filtered-noise sweep
    m = int(0.28 * SR); x = np.arange(m) / SR
    s = rng.standard_normal(m)
    out = np.zeros(m)
    for k in range(4):
        a, b = int(k * m / 4), int((k + 1) * m / 4)
        out[a:b] = filt(s, 900 + k * 900, 2400 + k * 1800)[a:b]
    place(out * np.sin(np.pi * x / 0.28) * 0.18, t, -0.1, g)


def scratch(t, d=1.6, g=1.0, dens=60):   # pencils on paper: a granular scribble
    m = int(d * SR); s = np.zeros(m)
    k = 0.0
    while k < d - 0.05:
        L = int(rng.uniform(0.02, 0.06) * SR); i = int(k * SR)
        g0 = filt(rng.standard_normal(L), 1800, 6500) * np.hanning(L) * rng.uniform(0.4, 1.0)
        s[i:i + L] += g0[: max(0, min(L, m - i))]
        k += rng.exponential(1 / dens)
    place(s * 0.05, t, rng.uniform(-0.3, 0.3), g)


def clock_tick(t, g=1.0):
    m = int(0.05 * SR); x = np.arange(m) / SR
    s = filt(rng.standard_normal(m), 2000, 6000) * np.exp(-x / 0.004) + 0.4 * np.sin(2 * np.pi * 3100 * x) * np.exp(-x / 0.006)
    place(s * 0.06, t, 0.4, g)


for k in range(int((SIL0 - 0.4) / 1.0)):                     # the kitchen timer ticks while the ten minutes run out
    clock_tick(0.4 + k * 1.0)
stamp(wt(9) - 0.02, 0.9)                                     # the 2x stamp on TWICE
slide_whistle(wt(12) + 0.12, True)                            # the call-out opens
scratch(wt(19) + 0.1, d=2.1, g=1.0)                           # a thousand pencils at work
shhk(wt(37) - 0.02); stamp(wt(37) - 0.03, 0.8)               # chapter 2: the numbered disc
stamp(wt(51), 0.7)                                            # SKIP pressed
for i in range(20):                                           # the grids stamp in
    stamp(wt(51) + 0.45 + i * 0.035, 0.18)
stamp(wt(53) - 0.02, 0.8)                                     # 2x on TWICE
shhk(wt(68) - 0.02); stamp(wt(68) - 0.03, 0.8)               # chapter 3
slide_whistle(wt(77) - 0.05, False, d=0.6, g=0.6)             # "so we never learn to balance"
shhk(wt(83) - 0.02); stamp(wt(83) - 0.03, 0.8)               # chapter 4
stamp(wt(112) - 0.03, 1.0)                                    # CLUE
shhk(wt(115) - 0.02); stamp(wt(115) - 0.03, 0.8)             # chapter 5
for t in (wt(149), wt(158) + 0.1):
    stamp(t, 0.5)

# ---------------------------------------------------------------- the CC0 sound pass (sound-effects skill library)
CC0 = [  # (file in the library, time, gain, longest seconds)
    ("impact/kenney-sci-lowfrequency-explosion-000.ogg", 0.0, 0.33, 1.2),          # the braam under the open
    ("ambience/fs-329533-room-tone-in-an-apartment-livi.ogg", 0.0, 0.5, DUR),       # warm room tone (cut in the silence)
    ("impact/kenney-impact-impactsoft-heavy-000.ogg", wt(9), 0.35, 0.8),           # 2x stamp body
    ("transition/fs-702773-swipe-wav.ogg", wt(12) - 0.25, 0.35, 0.7),              # the claim card wipes off
    ("ui-blip/kenney-digital-pepsound1.ogg", wt(15), 0.35, 0.5),                   # "chatbot": the typing dots
    ("transition/fs-786514-swoosh-v2.ogg", wt(25) - 0.1, 0.3, 0.8),                # the lanes wipe up
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(36), 0.4, 0.9),          # OFF: the wheels hit the floor
    ("click/kenney-interface-click-001.ogg", wt(51), 0.9, 0.4),                    # the SKIP button
    ("transition/fs-702773-swipe-wav.ogg", wt(48) - 0.15, 0.3, 0.7),               # block wipe to the skips
    ("transition/fs-702773-swipe-wav.ogg", wt(56) - 0.18, 0.3, 0.7),               # block wipe to reading
    ("riser/fs-174363-rewind.ogg", wt(68) + 0.02, 0.45, 0.6),                      # WHY: the timer rewinds
    ("impact/kenney-impact-impactsoft-heavy-001.ogg", wt(102), 0.5, 1.2),          # THE CATCH
    ("transition/fs-702773-swipe-wav.ogg", wt(104) - 0.2, 0.4, 0.8),               # the proof card turns in
    ("transition/fs-850347-swipe-various.ogg", wt(106) + 0.4, 0.3, 0.6),           # and turns away
    ("typing/fs-447909-keyboard-typing.ogg", wt(115) + 0.35, 0.7, wt(125) - wt(115) - 0.6),   # typing the prompt
    ("click/kenney-interface-click-001.ogg", wt(125), 0.6, 0.4),                   # send
    ("ding/kenney-interface-confirmation-001.ogg", wt(149) + 0.1, 0.3, 1.0),       # THE WORD?
]
manifest = json.load(open(LIB + "manifest.json"))
credits = {e["file"]: e.get("attribution") or e.get("credit") for e in manifest["bundled"] + manifest["default_kit"] if "file" in e}
layer = np.zeros((n, 2)); amb = np.zeros((n, 2))
for f, t, g, mx in CC0:
    tmp = "work/cc0_tmp.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1" if "ambience" in f else "0", "-i", LIB + f, "-t", str(mx),
                    "-ar", str(SR), "-ac", "2", tmp], check=True)
    sr, x = wavfile.read(tmp)
    x = x.astype(np.float64) / 32768.0
    fade = min(len(x), int(0.05 * SR)); x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    fi = min(len(x), int(0.01 * SR)); x[:fi] *= np.linspace(0, 1, fi)[:, None]
    i = int(max(t, 0) * SR); j = min(n, i + len(x)); (amb if "ambience" in f else layer)[i:j] += g * x[: j - i]
os.remove("work/cc0_tmp.wav")
json.dump({"length": DUR, "sounds": [{"file": f, "t": round(t, 2), "gain": g, "credit": credits.get(f, "")} for f, t, g, _ in CC0]},
          open("cc0.json", "w"), indent=1)
sr, s = wavfile.read("work/sfx.wav")
s = s.astype(np.float64) / 32768.0
if s.ndim == 1:
    s = np.stack([s, s], axis=1)
m = min(len(s), n)
both = layer[:m] + s[:m] + fol[:m]
for a, b in ((SIL0, SIL1 - 0.005), (STOP0, STOP1)):              # the silence is total; after the stop only the room is left
    both[int(a * SR):int(b * SR)] = 0.0
amb[int(SIL0 * SR):int((SIL1 - 0.005) * SR)] = 0.0
both += amb[:m]
both /= max(1.0, np.max(np.abs(both)) / 0.9)
wavfile.write("work/sfx_all.wav", SR, (both * 32767).astype(np.int16))

MG = os.environ.get("MG", "0.65")
SG = os.environ.get("SG", "0.4")
run(["python3", T + "mix.py", "assets/voice_raw.wav", "work/music.wav", "work/sfx_all.wav", "assets/mix.wav", str(DUR), MG, SG, "deep"])
run(["ffmpeg", "-v", "error", "-y", "-i", "assets/mix.wav", "-af", f"apad=whole_dur={DUR + 0.1}", "-c:a", "pcm_s16le", "work/mix_pad.wav"])
os.replace("work/mix_pad.wav", "assets/mix.wav")

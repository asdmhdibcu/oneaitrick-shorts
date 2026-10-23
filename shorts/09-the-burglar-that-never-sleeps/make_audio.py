"""Short #9: write sfx.json and the score, then mix the soundtrack.
The score (music9.py) cuts to silence on "So how DID it get in?" (39.18 s) and crashes back on "KEY" (43.20 s); it stops
again under the record scratch on "Here's the twist" (62.10 s). Nothing in the SFX plays through the silence either.
Usage: python3 make_audio.py   (needs work/voice_clean.wav; writes assets/mix.wav)
"""
import json
import re
import subprocess

from edl import DUR, SHOTS

tpl = open("index_template.tpl").read()
cuts = re.findall(r'\["(s\w+)", "(s\w+)", "(\w+)"', tpl[tpl.index("const CUTS"):tpl.index("CUTS.forEach")])
T0 = {s[0]: s[1] for s in SHOTS}
SILENT = (39.0, 43.15)
ev = []
for a, b, kind in cuts:
    t = T0[b]
    if SILENT[0] <= t <= SILENT[1] or t in (62.10,):   # the silence, and the record scratch has its own sound
        continue
    if kind in ("whip", "slideup"):
        ev.append({"type": "whoosh", "t": t - 0.02, "rise": 0.18, "fall": 0.3, "g": 0.5})
    elif kind == "zoom":
        ev.append({"type": "whoosh", "t": t, "rise": 0.22, "fall": 0.3, "g": 0.5}); ev.append({"type": "pop", "t": t, "pitch": 0.9, "g": 0.22})
    elif kind == "flash":
        ev.append({"type": "shimmer", "t": t, "g": 0.25}); ev.append({"type": "pop", "t": t, "pitch": 1.1, "g": 0.25})
    elif kind == "glitch":
        ev.append({"type": "glitch", "t": t, "dur": 0.25, "g": 0.4})
    elif kind == "card":
        ev.append({"type": "whoosh", "t": t, "rise": 0.15, "fall": 0.25, "g": 0.4}); ev.append({"type": "pop", "t": t + 0.1, "pitch": 1.15, "g": 0.28})
    elif kind == "dip":
        ev.append({"type": "swell", "t": t - 0.2, "dur": 0.4, "g": 0.25})
    elif kind == "door":   # the door swings shut with a thud, then opens
        ev.append({"type": "whoosh", "t": t - 0.12, "rise": 0.16, "fall": 0.2, "g": 0.45}); ev.append({"type": "boom", "t": t, "g": 0.4})
        ev.append({"type": "tick", "t": t + 0.02, "g": 0.6})
    elif kind == "keyhole":   # a lock clicking
        ev.append({"type": "tick", "t": t - 0.04, "g": 0.8}); ev.append({"type": "tick", "t": t + 0.05, "g": 0.6})
        ev.append({"type": "whoosh", "t": t + 0.1, "rise": 0.12, "fall": 0.3, "g": 0.35})
    elif kind == "light":
        ev.append({"type": "swell", "t": t - 0.3, "dur": 0.5, "g": 0.35}); ev.append({"type": "shimmer", "t": t, "g": 0.4})


def click(t, g=0.6):
    return [{"type": "tick", "t": t, "g": g}, {"type": "pop", "t": t + 0.02, "pitch": 0.6, "g": g * 0.6}]


moments = [
    {"type": "swell", "t": 0.0, "dur": 0.6, "g": 0.3}, {"type": "boom", "t": 0.26, "g": 0.45},
    {"type": "ticks", "t": 2.4, "n": 36, "dur": 2.2, "g": 0.2},                                   # 2,250 lights come on
    {"type": "ticks", "t": 5.6, "n": 22, "dur": 1.4, "g": 0.3}, {"type": "ding", "t": 6.86, "base": 1500, "g": 0.32},
    {"type": "pop", "t": 12.1, "pitch": 1.0, "g": 0.3}, {"type": "pop", "t": 13.02, "pitch": 1.15, "g": 0.3}, {"type": "pop", "t": 14.1, "pitch": 1.3, "g": 0.3},
] + click(14.45, 0.5) + [
    {"type": "zap", "t": 17.86, "g": 0.4}, {"type": "shimmer", "t": 17.88, "g": 0.4},              # the eye lights up
    {"type": "ticks", "t": 18.75, "n": 30, "dur": 1.8, "g": 0.28}, {"type": "boom", "t": 19.39, "g": 0.4},   # every handle at once
    {"type": "pop", "t": 20.7, "pitch": 0.9, "g": 0.25}, {"type": "tick", "t": 21.22, "g": 0.7}, {"type": "tick", "t": 21.94, "g": 0.7},
    {"type": "scan", "t": 23.1, "dur": 0.5, "g": 0.2}, {"type": "scan", "t": 24.08, "dur": 0.5, "g": 0.2},
] + [{"type": "pop", "t": 25.6 + k * 0.085, "pitch": 0.9 + k * 0.04, "g": 0.18} for k in range(14)] + [
    {"type": "boom", "t": 27.78, "g": 0.45}, {"type": "boom", "t": 28.32, "g": 0.45},
    {"type": "scan", "t": 29.75, "dur": 0.5, "g": 0.2},
    {"type": "rumble", "t": 32.3, "dur": 2.4, "g": 0.4}, {"type": "ticks", "t": 32.4, "n": 60, "dur": 2.2, "g": 0.22}, {"type": "zap", "t": 32.42, "g": 0.35},
    {"type": "scan", "t": 34.8, "dur": 0.5, "g": 0.2},
    {"type": "boom", "t": 36.27, "g": 0.6}, {"type": "scan", "t": 37.6, "dur": 0.8, "g": 0.25}, {"type": "boom", "t": 38.45, "g": 0.85},
    # the silence: nothing until the key
    {"type": "boom", "t": 43.2, "g": 0.9}, {"type": "shimmer", "t": 43.22, "g": 0.4},
] + click(43.15, 0.8) + [
    {"type": "pop", "t": 44.9, "pitch": 1.0, "g": 0.25}, {"type": "scan", "t": 47.1, "dur": 0.5, "g": 0.2},
    {"type": "scan", "t": 48.5, "dur": 0.7, "g": 0.25}, {"type": "whoosh", "t": 49.55, "rise": 0.4, "fall": 0.3, "g": 0.35}, {"type": "ding", "t": 50.2, "base": 1320, "g": 0.25},
    {"type": "boom", "t": 51.42, "g": 0.45},
    {"type": "ticks", "t": 53.26, "n": 8, "dur": 0.45, "g": 0.35}, {"type": "zap", "t": 53.82, "g": 0.45}, {"type": "glitch", "t": 53.83, "dur": 0.15, "g": 0.25},
] + click(55.3, 0.7) + [
    {"type": "ding", "t": 55.45, "base": 1760, "g": 0.32}, {"type": "pop", "t": 57.9, "pitch": 1.0, "g": 0.22}, {"type": "pop", "t": 59.3, "pitch": 1.1, "g": 0.22},
    {"type": "zap", "t": 59.55, "g": 0.3}, {"type": "pop", "t": 60.4, "pitch": 1.2, "g": 0.22},
    {"type": "boom", "t": 61.17, "g": 0.55}, {"type": "ding", "t": 61.2, "base": 1980, "g": 0.32},
    # the record scratch
    {"type": "glitch", "t": 62.1, "dur": 0.32, "g": 0.6}, {"type": "zap", "t": 62.1, "g": 0.5}, {"type": "boom", "t": 62.12, "g": 0.35},
    {"type": "scan", "t": 63.95, "dur": 0.6, "g": 0.22},
    {"type": "pop", "t": 67.55, "pitch": 1.0, "g": 0.25}, {"type": "scan", "t": 69.62, "dur": 0.6, "g": 0.22}, {"type": "boom", "t": 70.45, "g": 0.45},
    {"type": "zap", "t": 71.15, "g": 0.3}, {"type": "pop", "t": 71.57, "pitch": 0.9, "g": 0.25}, {"type": "pop", "t": 72.17, "pitch": 1.2, "g": 0.25},
    {"type": "ticks", "t": 74.3, "n": 24, "dur": 1.25, "g": 0.3}, {"type": "boom", "t": 75.59, "g": 0.6},
    {"type": "pop", "t": 77.1, "pitch": 1.0, "g": 0.2}, {"type": "ring", "t": 78.89, "rings": 2, "g": 0.22},
    {"type": "pop", "t": 79.95, "pitch": 1.1, "g": 0.25},
    {"type": "swell", "t": 81.3, "dur": 0.5, "g": 0.3}, {"type": "pop", "t": 81.67, "pitch": 1.0, "g": 0.35}, {"type": "ding", "t": 82.37, "base": 1320, "g": 0.3},
]
events = sorted([e for e in ev + moments if not (SILENT[0] <= e["t"] <= SILENT[1] and e["t"] < 43.14)], key=lambda e: e["t"])
json.dump({"length": DUR, "events": events}, open("sfx.json", "w"))
json.dump({"length": DUR, "generator": "music9.py", "bpm": 100, "silence": [39.18, 43.2], "scratch": [62.1, 63.28]}, open("music.json", "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


run(["python3", "music9.py", "work/music.wav", str(DUR)])
run(["python3", "../../tools/make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", "../../tools/mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

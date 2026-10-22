"""Short #8: write sfx.json and the score, then mix the soundtrack.
The score (music8.py) stops dead on "Then... the clue." (66.44 s) and turns to noir jazz on "One wire" (68.04 s).
Usage: python3 make_audio.py   (needs work/voice_clean.wav; writes assets/mix.wav)
"""
import json
import re
import subprocess

from edl import DUR

tpl = open("index_template.tpl").read()
cuts = re.findall(r'\["(s\w+)", "(s\w+)", "(\w+)"', tpl[tpl.index("const CUTS"):tpl.index("CUTS.forEach")])
T0 = {}
for line in open("edl.py"):
    m = re.match(r'\s+\("(s\w+)", ([\d.]+), ', line)
    if m:
        T0[m.group(1)] = float(m.group(2))
ev = []
for a, b, kind in cuts:
    t = T0[b]
    if t in (66.44,):  # the drop has its own hit
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
    elif kind == "fade":
        ev.append({"type": "swell", "t": t, "dur": 0.8, "g": 0.3})


def shutter(t, g=0.5):
    return [{"type": "tick", "t": t, "g": g}, {"type": "pop", "t": t + 0.03, "pitch": 0.55, "g": g * 0.8}, {"type": "tick", "t": t + 0.07, "g": g * 0.7}]


moments = [
    {"type": "swell", "t": 0.0, "dur": 0.6, "g": 0.3}, {"type": "boom", "t": 0.26, "g": 0.45}, {"type": "boom", "t": 3.28, "g": 0.35},
    {"type": "ticks", "t": 5.3, "n": 16, "dur": 0.95, "g": 0.32}, {"type": "ding", "t": 6.26, "base": 1500, "g": 0.3},
    {"type": "ding", "t": 8.09, "base": 1100, "g": 0.3}, {"type": "pop", "t": 13.6, "pitch": 1.0, "g": 0.25},
] + [{"type": "pop", "t": 15.4 + k * 0.12, "pitch": 1.0 + k * 0.08, "g": 0.22} for k in range(6)] + [
    {"type": "zap", "t": 17.62, "g": 0.45}, {"type": "glitch", "t": 17.64, "dur": 0.2, "g": 0.35}, {"type": "pop", "t": 18.2, "pitch": 0.9, "g": 0.25},
    {"type": "swell", "t": 20.4, "dur": 0.5, "g": 0.3}, {"type": "boom", "t": 20.91, "g": 0.7}, {"type": "zap", "t": 20.91, "g": 0.35}, {"type": "shimmer", "t": 20.93, "g": 0.35},
    {"type": "whoosh", "t": 22.6, "rise": 0.7, "fall": 0.4, "g": 0.35}, {"type": "ticks", "t": 21.9, "n": 24, "dur": 1.9, "g": 0.18},
    {"type": "rumble", "t": 23.9, "dur": 0.6, "g": 0.3}, {"type": "scan", "t": 24.35, "dur": 0.5, "g": 0.22},
] + shutter(25.9, 0.6) + shutter(26.55, 0.45) + shutter(26.85, 0.45) + [
    {"type": "ticks", "t": 26.0, "n": 14, "dur": 1.4, "g": 0.2},
    {"type": "shimmer", "t": 28.16, "g": 0.3}, {"type": "glitch", "t": 29.39, "dur": 0.2, "g": 0.25}, {"type": "rumble", "t": 29.4, "dur": 0.8, "g": 0.3},
    {"type": "ticks", "t": 30.4, "n": 30, "dur": 1.9, "g": 0.28}, {"type": "boom", "t": 31.29, "g": 0.4},
    {"type": "pop", "t": 33.0, "pitch": 0.9, "g": 0.28}, {"type": "ticks", "t": 34.3, "n": 11, "dur": 2.1, "g": 0.35},
    {"type": "whoosh", "t": 37.6, "rise": 0.2, "fall": 0.25, "g": 0.4}, {"type": "pop", "t": 37.62, "pitch": 1.2, "g": 0.3},
] + [{"type": "pop", "t": t, "pitch": 0.8 + k * 0.15, "g": 0.3} for k, t in enumerate([39.41, 39.63, 40.22, 40.63])] + [
    {"type": "boom", "t": 41.25, "g": 0.5}, {"type": "shimmer", "t": 41.27, "g": 0.35},
    {"type": "scan", "t": 42.45, "dur": 0.5, "g": 0.22}, {"type": "scan", "t": 42.95, "dur": 0.5, "g": 0.22}, {"type": "pop", "t": 47.4, "pitch": 1.0, "g": 0.25},
    {"type": "ticks", "t": 51.15, "n": 11, "dur": 0.95, "g": 0.4},
    {"type": "rumble", "t": 53.55, "dur": 1.8, "g": 0.45}, {"type": "ticks", "t": 53.55, "n": 40, "dur": 1.7, "g": 0.25},
    {"type": "boom", "t": 54.47, "g": 0.6}, {"type": "ding", "t": 54.9, "base": 1320, "g": 0.32},
    {"type": "scan", "t": 56.05, "dur": 0.6, "g": 0.22}, {"type": "scan", "t": 59.25, "dur": 0.5, "g": 0.3}, {"type": "boom", "t": 59.75, "g": 0.55},
    {"type": "ding", "t": 60.78, "base": 1760, "g": 0.35}, {"type": "scan", "t": 60.85, "dur": 0.6, "g": 0.2}, {"type": "scan", "t": 62.0, "dur": 0.6, "g": 0.2},
    {"type": "pop", "t": 64.97, "pitch": 1.1, "g": 0.3}, {"type": "pop", "t": 65.09, "pitch": 1.2, "g": 0.3}, {"type": "pop", "t": 65.21, "pitch": 1.3, "g": 0.3},
    {"type": "pop", "t": 65.79, "pitch": 0.7, "g": 0.3},
    # the drop: a typewriter strike and a hit
    {"type": "boom", "t": 66.44, "g": 0.95}, {"type": "tick", "t": 66.44, "g": 1.0}, {"type": "glitch", "t": 66.45, "dur": 0.15, "g": 0.3},
    {"type": "boom", "t": 67.21, "g": 0.6}, {"type": "shimmer", "t": 67.23, "g": 0.4},
    {"type": "scan", "t": 68.95, "dur": 0.5, "g": 0.25}, {"type": "zap", "t": 73.84, "g": 0.4},
    {"type": "ticks", "t": 74.85, "n": 34, "dur": 1.0, "g": 0.25}, {"type": "ticks", "t": 75.97, "n": 13, "dur": 0.39, "g": 0.4},
    {"type": "boom", "t": 76.36, "g": 0.55}, {"type": "shimmer", "t": 76.38, "g": 0.4},
    {"type": "boom", "t": 78.21, "g": 0.6}, {"type": "glitch", "t": 78.21, "dur": 0.25, "g": 0.35}, {"type": "pop", "t": 80.27, "pitch": 1.0, "g": 0.3},
    {"type": "scan", "t": 81.9, "dur": 0.7, "g": 0.22}, {"type": "zap", "t": 83.95, "g": 0.4}, {"type": "ticks", "t": 84.2, "n": 20, "dur": 1.6, "g": 0.2},
    {"type": "boom", "t": 85.28, "g": 0.5}, {"type": "pop", "t": 87.45, "pitch": 1.0, "g": 0.25}, {"type": "scan", "t": 88.9, "dur": 0.7, "g": 0.22},
    {"type": "pop", "t": 93.3, "pitch": 1.0, "g": 0.25}, {"type": "zap", "t": 94.85, "g": 0.3},
    {"type": "boom", "t": 96.93, "g": 0.6}, {"type": "ring", "t": 96.95, "rings": 2, "g": 0.25},
    {"type": "pop", "t": 98.2, "pitch": 1.1, "g": 0.25}, {"type": "pop", "t": 99.6, "pitch": 1.2, "g": 0.25},
    {"type": "ding", "t": 102.16, "base": 1500, "g": 0.32}, {"type": "boom", "t": 102.93, "g": 0.55},
    {"type": "pop", "t": 103.65, "pitch": 1.0, "g": 0.25}, {"type": "scan", "t": 104.85, "dur": 0.6, "g": 0.22}, {"type": "boom", "t": 105.41, "g": 0.45},
    {"type": "pop", "t": 106.1, "pitch": 1.0, "g": 0.25}, {"type": "boom", "t": 108.74, "g": 0.5},
    {"type": "ticks", "t": 110.25, "n": 8, "dur": 1.05, "g": 0.35},
    {"type": "swell", "t": 112.8, "dur": 0.4, "g": 0.3}, {"type": "boom", "t": 113.14, "g": 0.5},
    {"type": "ticks", "t": 114.95, "n": 16, "dur": 0.95, "g": 0.32}, {"type": "ring", "t": 116.05, "rings": 2, "g": 0.25},
    {"type": "pop", "t": 117.92, "pitch": 1.0, "g": 0.35}, {"type": "ding", "t": 118.62, "base": 1320, "g": 0.3},
]
json.dump({"length": DUR, "events": sorted(ev + moments, key=lambda e: e["t"])}, open("sfx.json", "w"))
json.dump({"length": DUR, "generator": "music8.py", "bpm": 96, "drop": 66.44, "noir_from": 68.04}, open("music.json", "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


run(["python3", "music8.py", "work/music.wav", str(DUR)])
run(["python3", "../../tools/make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", "../../tools/mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

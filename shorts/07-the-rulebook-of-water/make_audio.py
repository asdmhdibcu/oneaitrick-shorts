"""Short #7: write music.json and sfx.json, then build the soundtrack.
The music cuts out with a record scratch on "But here's the catch" (59.6 s) and comes back on "In the AI's version" (61.15 s).
Usage: python3 make_audio.py   (needs work/voice_clean.wav; writes assets/mix.wav)
"""
import json
import re
import subprocess

from edl import DUR

music = {"length": DUR, "bpm": 92, "seed": 707, "style": "pulse",
         "chords": [[50, 57, 60, 65], [46, 53, 58, 62], [48, 55, 60, 64], [45, 52, 57, 60]],
         "bass": [38, 34, 36, 33], "drums_from": 2, "outro": 3.5, "whooshes": [], "pops": []}
json.dump(music, open("music.json", "w"))

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
moments = [
    {"type": "swell", "t": 0.0, "dur": 0.8, "g": 0.3}, {"type": "boom", "t": 0.16, "g": 0.35},
    {"type": "ticks", "t": 1.34, "n": 12, "dur": 1.0, "g": 0.28}, {"type": "ding", "t": 2.4, "base": 1320, "g": 0.32},
    {"type": "ticks", "t": 3.47, "n": 16, "dur": 1.2, "g": 0.3}, {"type": "ding", "t": 4.65, "base": 1100, "g": 0.3},
    {"type": "glitch", "t": 6.54, "dur": 0.25, "g": 0.45}, {"type": "boom", "t": 6.58, "g": 0.55},
    {"type": "pop", "t": 7.6, "pitch": 0.8, "g": 0.3},
    {"type": "whoosh", "t": 10.45, "rise": 0.15, "fall": 0.25, "g": 0.35}, {"type": "pop", "t": 10.5, "pitch": 1.0, "g": 0.25}, {"type": "pop", "t": 10.65, "pitch": 1.1, "g": 0.25},
    {"type": "pop", "t": 12.13, "pitch": 1.1, "g": 0.25}, {"type": "pop", "t": 12.79, "pitch": 1.2, "g": 0.25}, {"type": "pop", "t": 13.67, "pitch": 1.3, "g": 0.25},
    {"type": "pop", "t": 14.16, "pitch": 1.4, "g": 0.25}, {"type": "pop", "t": 15.5, "pitch": 1.5, "g": 0.25},
    {"type": "boom", "t": 18.2, "g": 0.45}, {"type": "shimmer", "t": 18.22, "g": 0.3},
    {"type": "scan", "t": 20.6, "dur": 0.6, "g": 0.22},
    {"type": "boom", "t": 23.64, "g": 0.85}, {"type": "glitch", "t": 23.64, "dur": 0.3, "g": 0.5},
    {"type": "rumble", "t": 24.5, "dur": 3.2, "g": 0.4},
    {"type": "ring", "t": 28.45, "rings": 2, "g": 0.25}, {"type": "ticks", "t": 29.0, "n": 14, "dur": 1.0, "g": 0.3}, {"type": "zap", "t": 30.0, "g": 0.35},
    {"type": "scan", "t": 31.3, "dur": 0.6, "g": 0.22}, {"type": "ding", "t": 33.39, "base": 1320, "g": 0.32}, {"type": "shimmer", "t": 33.42, "g": 0.3},
    {"type": "scan", "t": 36.0, "dur": 0.6, "g": 0.22}, {"type": "shimmer", "t": 37.3, "g": 0.35}, {"type": "ticks", "t": 36.9, "n": 14, "dur": 1.2, "g": 0.25},
    {"type": "scan", "t": 39.6, "dur": 0.6, "g": 0.22}, {"type": "boom", "t": 41.1, "g": 0.7}, {"type": "shimmer", "t": 41.12, "g": 0.35},
    {"type": "boom", "t": 42.4, "g": 0.35}, {"type": "scan", "t": 43.3, "dur": 0.5, "g": 0.2}, {"type": "scan", "t": 44.5, "dur": 0.6, "g": 0.2},
    {"type": "ring", "t": 45.3, "rings": 2, "g": 0.25},
    {"type": "rumble", "t": 47.8, "dur": 3.8, "g": 0.5}, {"type": "ticks", "t": 47.8, "n": 30, "dur": 3.8, "g": 0.25},
    {"type": "boom", "t": 51.6, "g": 0.95}, {"type": "shimmer", "t": 51.62, "g": 0.45}, {"type": "swell", "t": 51.2, "dur": 0.4, "g": 0.35},
    {"type": "rumble", "t": 53.1, "dur": 1.7, "g": 0.35}, {"type": "pop", "t": 54.9, "pitch": 0.6, "g": 0.45},
    {"type": "pop", "t": 56.35, "pitch": 1.2, "g": 0.3}, {"type": "shimmer", "t": 56.4, "g": 0.25},
    {"type": "pop", "t": 58.36, "pitch": 1.0, "g": 0.3},
    {"type": "glitch", "t": 59.62, "dur": 0.35, "g": 0.7}, {"type": "zap", "t": 59.64, "g": 0.4}, {"type": "boom", "t": 60.32, "g": 0.6},
    {"type": "scan", "t": 62.3, "dur": 0.6, "g": 0.22}, {"type": "scan", "t": 63.25, "dur": 0.5, "g": 0.2}, {"type": "pop", "t": 65.8, "pitch": 1.2, "g": 0.3},
    {"type": "scan", "t": 68.7, "dur": 0.5, "g": 0.22}, {"type": "ding", "t": 69.6, "base": 1500, "g": 0.3},
    {"type": "pop", "t": 70.4, "pitch": 1.1, "g": 0.25}, {"type": "pop", "t": 71.7, "pitch": 0.9, "g": 0.25},
    {"type": "scan", "t": 72.4, "dur": 0.6, "g": 0.22}, {"type": "pop", "t": 73.3, "pitch": 1.0, "g": 0.25},
    {"type": "ticks", "t": 74.5, "n": 22, "dur": 2.3, "g": 0.22}, {"type": "scan", "t": 77.5, "dur": 0.6, "g": 0.22},
    {"type": "ticks", "t": 79.3, "n": 16, "dur": 3.6, "g": 0.28},
    {"type": "ding", "t": 83.91, "base": 2000, "g": 0.4}, {"type": "boom", "t": 83.92, "g": 0.45},
    {"type": "pop", "t": 87.21, "pitch": 0.9, "g": 0.35}, {"type": "pop", "t": 88.6, "pitch": 1.1, "g": 0.25},
    {"type": "scan", "t": 92.6, "dur": 0.6, "g": 0.22}, {"type": "scan", "t": 95.3, "dur": 0.5, "g": 0.22}, {"type": "boom", "t": 95.53, "g": 0.5},
    {"type": "scan", "t": 97.3, "dur": 0.6, "g": 0.22}, {"type": "scan", "t": 100.3, "dur": 0.6, "g": 0.22}, {"type": "shimmer", "t": 100.84, "g": 0.35},
    {"type": "pop", "t": 100.85, "pitch": 1.1, "g": 0.25}, {"type": "pop", "t": 101.0, "pitch": 1.2, "g": 0.25},
    {"type": "scan", "t": 105.5, "dur": 0.6, "g": 0.22}, {"type": "pop", "t": 106.3, "pitch": 1.0, "g": 0.3}, {"type": "boom", "t": 106.41, "g": 0.5},
    {"type": "whoosh", "t": 106.7, "rise": 0.3, "fall": 0.3, "g": 0.35},
    {"type": "scan", "t": 108.1, "dur": 0.6, "g": 0.22}, {"type": "scan", "t": 111.6, "dur": 0.5, "g": 0.22}, {"type": "ding", "t": 111.7, "base": 1320, "g": 0.3},
    {"type": "boom", "t": 114.01, "g": 0.55}, {"type": "glitch", "t": 114.01, "dur": 0.25, "g": 0.35},
    {"type": "scan", "t": 116.6, "dur": 0.6, "g": 0.22}, {"type": "pop", "t": 116.9, "pitch": 1.0, "g": 0.25},
    {"type": "ticks", "t": 117.74, "n": 4, "dur": 1.9, "g": 0.4},
    {"type": "boom", "t": 122.89, "g": 0.4}, {"type": "swell", "t": 123.5, "dur": 0.6, "g": 0.3},
    {"type": "pop", "t": 128.68, "pitch": 1.0, "g": 0.35}, {"type": "ding", "t": 129.38, "base": 1320, "g": 0.3},
]
json.dump({"length": DUR, "events": sorted(ev + moments, key=lambda e: e["t"])}, open("sfx.json", "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


run(["python3", "../../tools/make_track.py", "music.json", "work/music_raw.wav"])
# the record scratch: music out on "But here's the catch", back on "In the AI's version"
run(["ffmpeg", "-v", "error", "-y", "-i", "work/music_raw.wav", "-af",
     "volume='if(between(t,59.6,61.13),max(0,1-(t-59.6)/0.08),1)':eval=frame", "work/music.wav"])
run(["python3", "../../tools/make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", "../../tools/mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

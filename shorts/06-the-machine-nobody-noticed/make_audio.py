"""Short #6: write music.json and sfx.json, then build the soundtrack.
The music drops out on "Nobody knows" (55.45 s) and comes back with a hit on "YET" (56.97 s).
Usage: python3 make_audio.py   (needs work/voice_clean.wav; writes assets/mix.wav)
"""
import json
import re
import subprocess

from edl import DUR

music = {"length": DUR, "bpm": 96, "seed": 606, "style": "pulse",
         "chords": [[57, 60, 64, 67], [53, 57, 60, 64], [48, 55, 60, 64], [55, 59, 62, 67]],
         "bass": [45, 41, 48, 43], "drums_from": 2, "outro": 3.5, "whooshes": [], "pops": []}
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
    {"type": "swell", "t": 0.0, "dur": 0.8, "g": 0.3},
    {"type": "ticks", "t": 0.05, "n": 10, "dur": 1.3, "g": 0.28}, {"type": "ding", "t": 1.4, "base": 1320, "g": 0.35},
    {"type": "ticks", "t": 2.6, "n": 14, "dur": 1.3, "g": 0.3}, {"type": "ding", "t": 3.9, "base": 1100, "g": 0.32},
    {"type": "scan", "t": 5.0, "dur": 0.5, "g": 0.25},
    {"type": "boom", "t": 5.9, "g": 0.6}, {"type": "ring", "t": 5.95, "rings": 2, "g": 0.3},
    {"type": "scan", "t": 10.55, "dur": 0.9, "g": 0.25}, {"type": "pop", "t": 11.86, "pitch": 1.2, "g": 0.3},
    {"type": "shimmer", "t": 14.55, "g": 0.3}, {"type": "scan", "t": 17.3, "dur": 0.6, "g": 0.22},
    {"type": "ticks", "t": 19.25, "n": 12, "dur": 1.1, "g": 0.3}, {"type": "shimmer", "t": 20.35, "g": 0.3}, {"type": "ding", "t": 21.52, "base": 1500, "g": 0.25},
    {"type": "ticks", "t": 23.34, "n": 14, "dur": 1.45, "g": 0.3}, {"type": "boom", "t": 24.83, "g": 0.45},
    {"type": "zap", "t": 26.62, "g": 0.25}, {"type": "pop", "t": 26.66, "pitch": 1.0, "g": 0.35}, {"type": "zap", "t": 28.3, "g": 0.25},
    {"type": "boom", "t": 29.07, "g": 0.7}, {"type": "shimmer", "t": 29.1, "g": 0.35},
    {"type": "rumble", "t": 30.0, "dur": 2.2, "g": 0.35}, {"type": "ding", "t": 31.6, "base": 1760, "g": 0.3},
    {"type": "scan", "t": 32.55, "dur": 0.6, "g": 0.22},
    {"type": "scan", "t": 34.58, "dur": 1.5, "g": 0.35},
    {"type": "ticks", "t": 37.05, "n": 14, "dur": 0.65, "g": 0.22}, {"type": "ticks", "t": 38.15, "n": 14, "dur": 1.1, "g": 0.2},
    {"type": "boom", "t": 40.42, "g": 0.55},
    {"type": "pop", "t": 41.6, "pitch": 1.1, "g": 0.3}, {"type": "whoosh", "t": 42.45, "rise": 0.15, "fall": 0.3, "g": 0.4}, {"type": "ding", "t": 42.5, "base": 1320, "g": 0.3},
    {"type": "shimmer", "t": 44.6, "g": 0.35},
    {"type": "pop", "t": 50.3, "pitch": 1.3, "g": 0.25}, {"type": "pop", "t": 50.52, "pitch": 1.4, "g": 0.25}, {"type": "pop", "t": 50.74, "pitch": 1.5, "g": 0.25},
    {"type": "ding", "t": 52.1, "base": 1500, "g": 0.25},
    {"type": "swell", "t": 54.9, "dur": 0.6, "g": 0.3},
    {"type": "boom", "t": 56.97, "g": 0.8}, {"type": "ring", "t": 57.0, "rings": 3, "g": 0.3},
    {"type": "pop", "t": 58.65, "pitch": 1.0, "g": 0.3}, {"type": "pop", "t": 59.9, "pitch": 1.2, "g": 0.25},
    {"type": "scan", "t": 62.1, "dur": 0.6, "g": 0.22}, {"type": "scan", "t": 64.3, "dur": 0.6, "g": 0.22},
    {"type": "swell", "t": 67.3, "dur": 0.7, "g": 0.3}, {"type": "boom", "t": 67.95, "g": 0.4},
    {"type": "ding", "t": 70.0, "base": 1320, "g": 0.38}, {"type": "scan", "t": 69.4, "dur": 0.7, "g": 0.2},
    {"type": "zap", "t": 73.96, "g": 0.35}, {"type": "boom", "t": 73.97, "g": 0.55},
    {"type": "shimmer", "t": 77.2, "g": 0.25}, {"type": "zap", "t": 77.92, "g": 0.4},
    {"type": "pop", "t": 81.15, "pitch": 1.0, "g": 0.35}, {"type": "ding", "t": 81.85, "base": 1320, "g": 0.3},
]
json.dump({"length": DUR, "events": sorted(ev + moments, key=lambda e: e["t"])}, open("sfx.json", "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


run(["python3", "../../tools/make_track.py", "music.json", "work/music_raw.wav"])
# the drop: music out on "Nobody knows", back on "YET"
run(["ffmpeg", "-v", "error", "-y", "-i", "work/music_raw.wav", "-af",
     "volume='if(between(t,55.25,56.95),max(0,1-(t-55.25)/0.2),1)':eval=frame", "work/music.wav"])
run(["python3", "../../tools/make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", "../../tools/mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

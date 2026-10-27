"""Short #11: write sfx.json and mix the soundtrack (voice + music11.py score + SFX) to -14 LUFS.
The score (plan_video.json) stops dead on "here's the bit nobody's really talking about" under the record scratch and
crashes back in on "Once a postcard's been read". Every time comes from words.json (edl.wt) or the cuts (work/cuts.json).
Usage: python3 make_audio.py   (needs work/voice_clean.wav, work/music.wav from music11.py; writes assets/mix.wav)
"""
import json
import subprocess

from edl import DUR, SHOTS, wt, we

T0 = {s[0]: s[1] for s in SHOTS}
cuts = json.load(open("work/cuts.json"))["cuts"]
SILENT = (T0["k17"] + 0.25, T0["k18"] - 0.05)
ev = []
for a, b, kind in cuts:
    t = T0[b]
    if kind in ("whip", "slideup"):
        ev.append({"type": "whoosh", "t": t - 0.02, "rise": 0.18, "fall": 0.3, "g": 0.45})
    elif kind == "zoom":
        ev.append({"type": "whoosh", "t": t, "rise": 0.22, "fall": 0.3, "g": 0.45}); ev.append({"type": "pop", "t": t, "pitch": 0.9, "g": 0.2})
    elif kind == "card":
        ev.append({"type": "whoosh", "t": t, "rise": 0.15, "fall": 0.25, "g": 0.35}); ev.append({"type": "pop", "t": t + 0.1, "pitch": 1.15, "g": 0.25})
    elif kind == "dip":
        ev.append({"type": "swell", "t": t - 0.2, "dur": 0.4, "g": 0.25})
    elif kind == "cut":
        ev.append({"type": "tick", "t": t, "g": 0.6})
    elif kind == "flash":
        ev.append({"type": "shimmer", "t": t, "g": 0.28})
    elif kind == "fade":
        ev.append({"type": "swell", "t": t - 0.3, "dur": 0.6, "g": 0.3})
    elif kind == "scratch":
        ev.append({"type": "glitch", "t": t - 0.03, "dur": 0.32, "g": 0.6}); ev.append({"type": "zap", "t": t - 0.03, "g": 0.45})


def pops(ks, pitch=1.0, g=0.2, step=0.0):
    return [{"type": "pop", "t": wt(k), "pitch": pitch + j * step, "g": g} for j, k in enumerate(ks)]


moments = [
    {"type": "swell", "t": 0.0, "dur": 0.5, "g": 0.25},
] + [{"type": "pop", "t": wt(3) + j * 0.08, "pitch": 0.9 + j * 0.03, "g": 0.14} for j in range(10)] + [
    {"type": "boom", "t": wt(30), "g": 0.3}, {"type": "ding", "t": wt(30) + 0.05, "base": 1320, "g": 0.18},
    {"type": "boom", "t": wt(31), "g": 0.4}, {"type": "tick", "t": wt(31), "g": 0.9},
    {"type": "boom", "t": wt(32) + 0.05, "g": 0.4}, {"type": "tick", "t": wt(32) + 0.05, "g": 0.9},
    {"type": "tick", "t": wt(47), "g": 0.6}, {"type": "scan", "t": wt(65), "dur": 0.6, "g": 0.18}, {"type": "scan", "t": wt(68), "dur": 0.6, "g": 0.18},
    {"type": "tick", "t": wt(86), "g": 0.8}, {"type": "tick", "t": wt(88), "g": 0.8}, {"type": "tick", "t": wt(91), "g": 0.8},
    {"type": "boom", "t": wt(109), "g": 0.45},
] + [{"type": "pop", "t": wt(k), "pitch": 0.9 + j * 0.04, "g": 0.18} for j, k in enumerate([117, 118, 119, 120, 121, 122, 123, 124, 125, 127])] + [
    {"type": "ding", "t": wt(131), "base": 1760, "g": 0.25},
    {"type": "glitch", "t": wt(159) + 0.1, "dur": 0.25, "g": 0.15}, {"type": "boom", "t": T0["k20b"], "g": 0.5},
    {"type": "zap", "t": wt(177), "g": 0.35},
    {"type": "tick", "t": wt(190), "g": 0.7}, {"type": "tick", "t": wt(191), "g": 0.7}, {"type": "tick", "t": wt(193), "g": 0.7},
    {"type": "ding", "t": T0["k23"] + 4.75, "base": 1320, "g": 0.25},
    {"type": "scan", "t": wt(208), "dur": 0.8, "g": 0.15},
    {"type": "swell", "t": T0["k26"] - 0.2, "dur": 0.5, "g": 0.3}, {"type": "pop", "t": T0["k26"] + 0.15, "pitch": 1.0, "g": 0.35},
    {"type": "ding", "t": T0["k26"] + 0.85, "base": 1320, "g": 0.3},
]
events = sorted([e for e in ev + moments if not (SILENT[0] <= e["t"] <= SILENT[1])], key=lambda e: e["t"])
json.dump({"length": DUR, "events": events}, open("sfx.json", "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


run(["python3", "../../longform/ai-firms-your-data/music11.py", "plan_short.json", "work/music.wav", str(DUR)])
run(["python3", "../../tools/make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", "../../tools/mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

"""Short #10: write sfx.json and the score, then mix the soundtrack.
The score (music10.py) stops dead on "Here's the twist" and crashes back on "TRANSLATED"; nothing in the SFX plays through
that silence except the record scratch itself. Every time comes from words.json (edl.wt) or the cuts in the template.
Usage: python3 make_audio.py   (needs work/voice_clean.wav; writes assets/mix.wav)
"""
import json
import re
import subprocess

from edl import DUR, SHOTS, wt, we

tpl = open("index_template.tpl").read()
cuts = re.findall(r'\["(s\w+)", "(s\w+)", "(\w+)"', tpl[tpl.index("const CUTS"):tpl.index("CUTS.forEach")])
T0 = {s[0]: s[1] for s in SHOTS}
SILENT = (wt(137) - 0.06, wt(146) - 0.03)
ev = []
for a, b, kind in cuts:
    t = T0[b]
    if SILENT[0] - 0.1 <= t <= SILENT[1]:
        continue
    if kind in ("whip", "slideup"):
        ev.append({"type": "whoosh", "t": t - 0.02, "rise": 0.18, "fall": 0.3, "g": 0.5})
    elif kind == "zoom":
        ev.append({"type": "whoosh", "t": t, "rise": 0.22, "fall": 0.3, "g": 0.5}); ev.append({"type": "pop", "t": t, "pitch": 0.9, "g": 0.22})
    elif kind in ("flash", "uv"):
        ev.append({"type": "shimmer", "t": t, "g": 0.28}); ev.append({"type": "pop", "t": t, "pitch": 1.1, "g": 0.25})
    elif kind == "card":
        ev.append({"type": "whoosh", "t": t, "rise": 0.15, "fall": 0.25, "g": 0.4}); ev.append({"type": "pop", "t": t + 0.1, "pitch": 1.15, "g": 0.28})
    elif kind == "dip":
        ev.append({"type": "swell", "t": t - 0.2, "dur": 0.4, "g": 0.25})
    elif kind == "ink":   # a wet brush stroke
        ev.append({"type": "whoosh", "t": t - 0.05, "rise": 0.2, "fall": 0.35, "g": 0.55}); ev.append({"type": "scan", "t": t - 0.18, "dur": 0.35, "g": 0.12})
    elif kind == "light":
        ev.append({"type": "swell", "t": t - 0.3, "dur": 0.5, "g": 0.35}); ev.append({"type": "shimmer", "t": t, "g": 0.4})
    elif kind == "fade":
        ev.append({"type": "swell", "t": t - 0.3, "dur": 0.6, "g": 0.3})


def pen(t0, dur, g=0.12):   # a nib scratching: soft ticks
    return [{"type": "ticks", "t": t0, "n": max(6, int(dur * 14)), "dur": dur, "g": g}]


moments = [
    {"type": "swell", "t": 0.0, "dur": 0.5, "g": 0.25}, {"type": "shimmer", "t": wt(8), "g": 0.35},            # Europe's stars
] + pen(0.05, 3.6, 0.1) + [
    {"type": "boom", "t": wt(13), "g": 0.45}, {"type": "zap", "t": wt(13), "g": 0.25},                       # SEE
    {"type": "pop", "t": wt(24), "pitch": 1.1, "g": 0.25}, {"type": "tick", "t": wt(24), "g": 0.6},          # the slots flip
    {"type": "pop", "t": wt(27), "pitch": 1.25, "g": 0.25}, {"type": "tick", "t": wt(27), "g": 0.6},
    {"type": "ding", "t": wt(30) + 0.05, "base": 1760, "g": 0.25},
    {"type": "pop", "t": wt(37), "pitch": 1.0, "g": 0.3}, {"type": "ding", "t": wt(37), "base": 1320, "g": 0.2},   # the coin locks
    {"type": "pop", "t": wt(40), "pitch": 1.2, "g": 0.3}, {"type": "ding", "t": wt(40), "base": 1568, "g": 0.2},
    {"type": "boom", "t": wt(48), "g": 0.4}, {"type": "zap", "t": wt(48), "g": 0.2},                         # loaded
    {"type": "tick", "t": wt(50), "g": 0.7},
    {"type": "ticks", "t": wt(54), "n": 40, "dur": we(61) - wt(54), "g": 0.18}, {"type": "ding", "t": we(61) - 0.1, "base": 1980, "g": 0.28},
] + pen(T0["s09"] + 0.05, 1.2, 0.12) + [
    {"type": "scan", "t": wt(66), "dur": 0.6, "g": 0.2},
    {"type": "pop", "t": wt(68) + 0.05, "pitch": 1.0, "g": 0.3}, {"type": "pop", "t": wt(69) + 0.05, "pitch": 1.2, "g": 0.3},
    {"type": "tick", "t": wt(72) + 0.05, "g": 0.9}, {"type": "shimmer", "t": wt(72) + 0.05, "g": 0.3},       # the screenshot shutter
    {"type": "ding", "t": wt(74), "base": 1760, "g": 0.25},
    {"type": "shimmer", "t": wt(80), "g": 0.35}, {"type": "pop", "t": wt(80), "pitch": 0.9, "g": 0.25},      # IS
    {"type": "whoosh", "t": wt(91), "rise": 0.3, "fall": 0.4, "g": 0.35},                                  # the mark across the flag
    {"type": "pop", "t": wt(96), "pitch": 1.0, "g": 0.3}, {"type": "pop", "t": wt(100), "pitch": 0.8, "g": 0.3},
    {"type": "glitch", "t": wt(101) + 0.3, "dur": 0.2, "g": 0.15},                                        # not yet
    {"type": "scan", "t": wt(108), "dur": 0.5, "g": 0.2},
    {"type": "whoosh", "t": T0["s17"], "rise": 0.4, "fall": 0.6, "g": 0.3},
] + [{"type": "pop", "t": T0["s17"] + 0.1 + k * 0.08, "pitch": 0.9 + k * 0.03, "g": 0.14} for k in range(18)] + [
    {"type": "ding", "t": wt(113), "base": 1320, "g": 0.3},                                               # the UK
    {"type": "scan", "t": wt(122), "dur": 0.6, "g": 0.2},
    {"type": "ticks", "t": T0["s20"] + 0.05, "n": 24, "dur": 0.6, "g": 0.2},                               # the bars grow
    {"type": "ding", "t": wt(129), "base": 1760, "g": 0.25}, {"type": "pop", "t": wt(136), "pitch": 0.8, "g": 0.3},
    # the record scratch, then nothing until TRANSLATED
    {"type": "glitch", "t": wt(137) - 0.04, "dur": 0.32, "g": 0.6}, {"type": "zap", "t": wt(137) - 0.04, "g": 0.5},
    {"type": "scan", "t": wt(145), "dur": 0.7, "g": 0.1},
    {"type": "boom", "t": wt(146), "g": 0.7}, {"type": "shimmer", "t": wt(146), "g": 0.35},
] + pen(wt(152), we(154) - wt(152), 0.12) + [
    {"type": "scan", "t": wt(163), "dur": 0.6, "g": 0.2},
    {"type": "pop", "t": wt(170), "pitch": 0.8, "g": 0.25},
    {"type": "scan", "t": wt(175), "dur": 0.6, "g": 0.2},
    {"type": "boom", "t": wt(184) - 0.03, "g": 0.55}, {"type": "glitch", "t": wt(184) + 0.35, "dur": 0.4, "g": 0.18},   # CHEATED? won't stick
    {"type": "boom", "t": wt(191) - 0.03, "g": 0.4}, {"type": "glitch", "t": wt(191) + 0.3, "dur": 0.4, "g": 0.15},
] + pen(wt(200) - 0.1, 1.3, 0.13) + [
    {"type": "ding", "t": wt(201), "base": 1320, "g": 0.25},
] + pen(T0["s29"] + 0.1, 1.8, 0.1) + [
    {"type": "swell", "t": T0["s30"] - 0.2, "dur": 0.5, "g": 0.3}, {"type": "pop", "t": T0["s30"] + 0.15, "pitch": 1.0, "g": 0.35},
    {"type": "ding", "t": T0["s30"] + 0.85, "base": 1320, "g": 0.3},
]
events = sorted([e for e in ev + moments if not (SILENT[0] + 0.4 <= e["t"] <= SILENT[1] - 0.05 and e["type"] != "scan")], key=lambda e: e["t"])
json.dump({"length": DUR, "events": events}, open("sfx.json", "w"))
json.dump({"length": DUR, "generator": "music10.py", "bpm": 92, "silence": [round(SILENT[0], 2), round(SILENT[1], 2)]}, open("music.json", "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


run(["python3", "music10.py", "work/music.wav", str(DUR)])
run(["python3", "../../tools/make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", "../../tools/mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

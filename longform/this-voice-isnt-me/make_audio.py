"""#12 video: write sfx.json and mix the soundtrack (voice + music12.py score + SFX) to -14 LUFS.
The score drops out on "Remember my voice at the start?" and comes back on Starling's three seconds; it thins to a
pad for "the quietest one" and lifts to a major key for the four habits. Times come from words.json (edl.wt) and the cuts.
Usage: python3 make_audio.py   (needs work/voice_clean.wav; writes work/music.wav, work/sfx.wav, assets/mix.wav)
"""
import json
import subprocess

from edl import DUR, SHOTS, wt

T0 = {s[0]: s[1] for s in SHOTS}
cuts = json.load(open("work/cuts.json"))["cuts"]
SILENT = (T0["v49"] - 0.05, T0["v50"] - 0.05)
ev = []
for a, b, kind in cuts:
    t = T0[b]
    if kind in ("whip", "slideup"):
        ev.append({"type": "whoosh", "t": t - 0.02, "rise": 0.18, "fall": 0.3, "g": 0.4})
    elif kind == "zoom":
        ev.append({"type": "whoosh", "t": t, "rise": 0.22, "fall": 0.3, "g": 0.4}); ev.append({"type": "pop", "t": t, "pitch": 0.9, "g": 0.18})
    elif kind == "card":
        ev.append({"type": "whoosh", "t": t, "rise": 0.15, "fall": 0.25, "g": 0.32}); ev.append({"type": "pop", "t": t + 0.1, "pitch": 1.15, "g": 0.22})
    elif kind == "dip":   # a danger card lands
        ev.append({"type": "boom", "t": t + 0.05, "g": 0.5}); ev.append({"type": "glitch", "t": t - 0.05, "dur": 0.25, "g": 0.25})
    elif kind == "cut":
        ev.append({"type": "tick", "t": t, "g": 0.6})
    elif kind == "fade":
        ev.append({"type": "swell", "t": t - 0.3, "dur": 0.6, "g": 0.3})


def pops(ks, pitch=1.0, g=0.2, step=0.0, dt=0.0):
    return [{"type": "pop", "t": wt(k) + dt, "pitch": pitch + j * step, "g": g} for j, k in enumerate(ks)]


def stamp(k):
    return [{"type": "boom", "t": wt(k), "g": 0.45}, {"type": "tick", "t": wt(k), "g": 0.9}]


moments = (
    [{"type": "swell", "t": 0.0, "dur": 0.6, "g": 0.25}, {"type": "shimmer", "t": wt(14), "g": 0.25}]       # a clone of my voice
    + [{"type": "pop", "t": wt(41) + j * 0.1, "pitch": 0.9 + j * 0.06, "g": 0.2} for j in range(5)]       # five
    + pops([52, 57, 63], 1.0, 0.18, 0.08) + pops([85, 87, 89], 1.0, 0.18, 0.08)
    + pops([101, 108, 114, 123], 0.9, 0.22, 0.06, -0.25) + [{"type": "ding", "t": wt(136), "base": 1320, "g": 0.2}]
    + pops([153, 155, 157], 1.0, 0.22, 0.08) + [{"type": "pop", "t": wt(172), "pitch": 1.2, "g": 0.2}] + stamp(194)
    + pops([213, 222, 230], 1.0, 0.18, 0.08) + [{"type": "glitch", "t": wt(250), "dur": 0.3, "g": 0.25}]    # things leak
    + pops([281, 283, 287], 1.1, 0.18, 0.06) + [{"type": "scan", "t": wt(320), "dur": 0.6, "g": 0.15}]
    + [{"type": "tick", "t": wt(343), "g": 0.7}, {"type": "tick", "t": wt(346), "g": 0.7}, {"type": "tick", "t": wt(348), "g": 0.7},
       {"type": "ding", "t": T0["v25"] + 4.75, "base": 1320, "g": 0.25}]
    + [{"type": "scan", "t": wt(396), "dur": 0.7, "g": 0.15}] + stamp(473)
    + pops([505, 507], 0.8, 0.2, 0.1) + [{"type": "zap", "t": wt(509), "g": 0.3}]
    + pops([529, 530, 532], 1.0, 0.25, 0.1) + [{"type": "ding", "t": wt(563), "base": 1760, "g": 0.22}]
    + stamp(600) + [{"type": "glitch", "t": wt(608), "dur": 0.3, "g": 0.2}, {"type": "glitch", "t": wt(666), "dur": 0.4, "g": 0.3}]
    + pops([700, 704, 711], 1.0, 0.2, 0.08) + [{"type": "ding", "t": wt(711) + 0.5, "base": 1320, "g": 0.2}]
    + [{"type": "boom", "t": wt(744), "g": 0.35}] + pops([749, 752, 755], 1.0, 0.18, 0.08)
    + [{"type": "ring", "t": T0["v52"] + 0.15, "rings": 4, "g": 0.6}]                                     # the phone rings
    + pops([774, 777, 779], 0.9, 0.25, 0.1) + [{"type": "boom", "t": wt(811), "g": 0.35}]
    + [{"type": "glitch", "t": wt(882), "dur": 0.35, "g": 0.35}] + stamp(882) + [{"type": "zap", "t": wt(884), "g": 0.3}]
    + [{"type": "pop", "t": wt(947), "pitch": 1.0, "g": 0.25}] + stamp(966)
    + [{"type": "pop", "t": wt(998) + j * 0.025, "pitch": 0.9 + j * 0.01, "g": 0.06} for j in range(45)]
    + [{"type": "zap", "t": wt(1001), "g": 0.35}, {"type": "scan", "t": wt(1010), "dur": 0.7, "g": 0.15}]
    + pops([1035, 1040, 1044, 1049, 1059], 0.9, 0.22, 0.05)
    + [{"type": "pop", "t": wt(1076) + 0.12 * j, "pitch": 1.0 + 0.1 * j, "g": 0.25} for j in range(4)]
    + [{"type": "tick", "t": wt(1108), "g": 0.7}, {"type": "tick", "t": wt(1114), "g": 0.7}, {"type": "tick", "t": wt(1117), "g": 0.7}]
    + [{"type": "shimmer", "t": wt(1144), "g": 0.3}] + pops([1152, 1157, 1160], 1.0, 0.2, 0.08)
    + [{"type": "ring", "t": wt(1164) - 0.2, "rings": 3, "g": 0.55}] + pops([1173, 1177], 1.0, 0.2, 0.1) + stamp(1179)
    + [{"type": "ding", "t": wt(1182), "base": 1320, "g": 0.25}]
    + pops([1203, 1204, 1205], 1.0, 0.18, 0.08) + [{"type": "ding", "t": wt(1206), "base": 1760, "g": 0.2}]
    + [{"type": "boom", "t": wt(1245), "g": 0.3}, {"type": "pop", "t": wt(1261), "pitch": 1.1, "g": 0.25},
       {"type": "ding", "t": wt(1263), "base": 1760, "g": 0.25}]
    + [{"type": "swell", "t": T0["v83"] - 0.2, "dur": 0.5, "g": 0.3}, {"type": "pop", "t": T0["v83"] + 0.15, "pitch": 1.0, "g": 0.35},
       {"type": "ding", "t": T0["v83"] + 0.85, "base": 1320, "g": 0.3}]
)
events = sorted([e for e in ev + moments if not (SILENT[0] <= e["t"] <= SILENT[1])], key=lambda e: e["t"])
json.dump({"length": DUR, "events": events}, open("sfx.json", "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


c = lambda sid: round(T0[sid], 2)
plan = {"bpm": 84, "transpose": 5,
        "sections": [[0.0, c("v04"), "MIN", 1], [c("v04"), c("v12"), "MIN", 2], [c("v12"), c("v26"), "MIN", 2], [c("v26"), c("v39"), "MIN", 2],
                     [c("v39"), c("v48"), "MIN", 3], [c("v48"), c("v49") - 0.05, "MIN", 3], [c("v50") - 0.05, c("v64"), "MIN", 3],
                     [c("v64"), c("v72"), "MIN", 1], [c("v72"), c("v83"), "MAJ", 2]],
        "silence": [[c("v49") - 0.05, c("v50") - 0.05]],
        "hits": [c("v12"), c("v26"), c("v39"), c("v48"), c("v50") - 0.05, c("v64"), c("v72")],
        "risers": [[c("v12") - 1.4, 1.4], [c("v26") - 1.4, 1.4], [c("v39") - 1.4, 1.4], [c("v48") - 1.4, 1.4], [c("v64") - 1.4, 1.4], [c("v72") - 1.4, 1.4]],
        "end": c("v83")}
json.dump(plan, open("plan_video.json", "w"))
run(["python3", "music12.py", "plan_video.json", "work/music.wav", str(DUR)])
run(["python3", "../../tools/make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", "../../tools/mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

"""#11 video: write sfx.json and mix the soundtrack (voice + music11.py score + SFX) to -14 LUFS.
The score (plan_video.json) stops dead on "here's the bit nobody's really talking about" under the record scratch and
crashes back in on "Once a postcard's been read". Every time comes from words.json (edl.wt) or the cuts (work/cuts.json).
Usage: python3 make_audio.py   (needs work/voice_clean.wav, work/music.wav from music11.py; writes assets/mix.wav)
"""
import json
import subprocess

from edl import DUR, SHOTS, wt, we

T0 = {s[0]: s[1] for s in SHOTS}
cuts = json.load(open("work/cuts.json"))["cuts"]
SILENT = (T0["v36"] + 0.25, T0["v37"] - 0.05)
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
] + [{"type": "pop", "t": wt(3) + j * 0.09, "pitch": 0.9 + j * 0.03, "g": 0.14} for j in range(10)] + [   # the ten logos
    {"type": "boom", "t": wt(30), "g": 0.3}, {"type": "ding", "t": wt(30) + 0.05, "base": 1320, "g": 0.18},   # a regulator
    {"type": "boom", "t": wt(31), "g": 0.4}, {"type": "tick", "t": wt(31), "g": 0.9},                    # knock
    {"type": "boom", "t": wt(32) + 0.05, "g": 0.4}, {"type": "tick", "t": wt(32) + 0.05, "g": 0.9},      # knock
] + pops([54, 60, 62, 65], 1.0, 0.25, 0.08) + [                                                            # reviews, posts...
    {"type": "tick", "t": wt(80), "g": 0.6}, {"type": "scan", "t": wt(98), "dur": 0.6, "g": 0.18},
    {"type": "boom", "t": wt(101), "g": 0.35}, {"type": "ding", "t": wt(116), "base": 1320, "g": 0.22},
] + [{"type": "pop", "t": wt(126) + j * 0.07, "pitch": 0.9 + j * 0.025, "g": 0.13} for j in range(11)] + [
    {"type": "ding", "t": wt(128), "base": 1760, "g": 0.22},
    {"type": "pop", "t": wt(150), "pitch": 1.2, "g": 0.25}, {"type": "pop", "t": wt(151) + 0.1, "pitch": 0.8, "g": 0.25},
    {"type": "whoosh", "t": wt(180), "rise": 0.12, "fall": 0.2, "g": 0.4}, {"type": "boom", "t": wt(182), "g": 0.45},   # NOT A REASON
    {"type": "boom", "t": wt(210), "g": 0.35},                                                                     # WORSE
    {"type": "tick", "t": wt(227), "g": 0.8}, {"type": "tick", "t": wt(229), "g": 0.8}, {"type": "tick", "t": wt(232), "g": 0.8},
] + [{"type": "pop", "t": wt(k), "pitch": 0.9 + j * 0.04, "g": 0.18} for j, k in enumerate([258, 259, 260, 261, 262, 263, 264, 265, 266, 268])] + [
    {"type": "ding", "t": wt(272), "base": 1760, "g": 0.25}, {"type": "shimmer", "t": wt(302), "g": 0.3},
    {"type": "glitch", "t": wt(415) + 0.1, "dur": 0.25, "g": 0.15}, {"type": "boom", "t": wt(418), "g": 0.5},     # xAI drops in
    {"type": "zap", "t": wt(433), "g": 0.35},
    {"type": "glitch", "t": wt(462), "dur": 0.3, "g": 0.2},                                                         # slipped past
    {"type": "scan", "t": wt(487), "dur": 0.6, "g": 0.18},
] + pops([499], 1.0, 0.3) + [{"type": "pop", "t": wt(499) + 0.12 * j, "pitch": 1.0 + 0.1 * j, "g": 0.25} for j in range(3)] + [
    {"type": "tick", "t": wt(511), "g": 0.7}, {"type": "tick", "t": wt(512), "g": 0.7}, {"type": "tick", "t": wt(514), "g": 0.7},
    {"type": "ding", "t": T0["v52"] + 4.75, "base": 1320, "g": 0.25},
    {"type": "tick", "t": wt(522), "g": 0.7}, {"type": "tick", "t": wt(523), "g": 0.7}, {"type": "tick", "t": wt(524), "g": 0.7},
    {"type": "ding", "t": T0["v53"] + 4.1, "base": 1320, "g": 0.25}, {"type": "ding", "t": wt(533), "base": 1320, "g": 0.25},
    {"type": "pop", "t": wt(537), "pitch": 1.1, "g": 0.22}, {"type": "pop", "t": wt(540), "pitch": 0.9, "g": 0.22},
    {"type": "zap", "t": wt(545), "g": 0.25}, {"type": "zap", "t": wt(547), "g": 0.25},
    {"type": "scan", "t": wt(572), "dur": 0.8, "g": 0.15},
    {"type": "swell", "t": T0["v60"] - 0.2, "dur": 0.5, "g": 0.3}, {"type": "pop", "t": T0["v60"] + 0.15, "pitch": 1.0, "g": 0.35},
    {"type": "ding", "t": T0["v60"] + 0.85, "base": 1320, "g": 0.3},
]
events = sorted([e for e in ev + moments if not (SILENT[0] <= e["t"] <= SILENT[1])], key=lambda e: e["t"])
json.dump({"length": DUR, "events": events}, open("sfx.json", "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


# the score's plan follows the cuts: minor, lifting to major on "what they changed", silent under the record scratch
c = lambda sid: round(T0[sid], 2)
plan = {"bpm": 90,
        "sections": [[0.0, c("v05"), "MIN", 2], [c("v05"), c("v14"), "MIN", 1], [c("v14"), c("v23"), "MIN", 2], [c("v23"), c("v29"), "MIN", 3],
                     [c("v29"), c("v36") - 0.08, "MAJ", 2], [c("v37"), c("v45"), "MIN", 1], [c("v45"), c("v50"), "MIN", 3],
                     [c("v50"), c("v55"), "MAJ", 1], [c("v55"), c("v60"), "MAJ", 2]],
        "silence": [[c("v36") - 0.08, c("v37")]], "hits": [c("v29"), c("v37"), c("v45")], "risers": [[c("v45") - 1.5, 1.5]], "end": c("v60")}
json.dump(plan, open("plan_video.json", "w"))
run(["python3", "music11.py", "plan_video.json", "work/music.wav", str(DUR)])
run(["python3", "../../tools/make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", "../../tools/mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

"""Short #13 audio: an original score (tools/make_track.py), sound effects on the cuts and hits (tools/make_sfx.py), and the
mix with the creator's voice at -14 LUFS (tools/mix.py) -> assets/mix.wav.
Reads edl.py, work/cuts.json (make_index.py) and words.json. Writes music.json and sfx.json (committed) and work/*.wav.
Usage: python3 make_audio.py
"""
import json
import subprocess

from edl import DUR, wt

T = "../../tools/"
music = {"length": DUR, "bpm": 100, "seed": 13, "style": "dream",
         "chords": [[48, 52, 55, 60], [43, 47, 50, 55], [45, 48, 52, 57], [41, 45, 48, 53]],
         "bass": [36, 31, 33, 29], "drums_from": 2, "outro": 2.5, "whooshes": [], "pops": []}
json.dump(music, open("music.json", "w"), indent=1)

cuts = json.load(open("work/cuts.json"))["cuts"]
T0 = {}
from edl import SHOTS  # noqa: E402
for s in SHOTS:
    T0[s[0]] = s[1]
ev = [{"type": "swell", "t": 0.0, "dur": 0.6, "g": 0.5}]
for a, b, k in cuts:
    t = T0[b]
    if k in ("whip", "slideup"):
        ev.append({"type": "whoosh", "t": round(t - 0.05, 2), "rise": 0.22, "fall": 0.25, "g": 0.55})
    elif k == "zoom":
        ev.append({"type": "whoosh", "t": round(t - 0.04, 2), "rise": 0.2, "fall": 0.2, "g": 0.5})
        ev.append({"type": "pop", "t": round(t, 2), "pitch": 0.9})
    elif k in ("flash", "scratch"):
        ev.append({"type": "zap" if k == "scratch" else "shimmer", "t": round(t, 2), "g": 0.5})
    elif k == "dip":
        ev.append({"type": "swell", "t": round(t - 0.3, 2), "dur": 0.4, "g": 0.35})
# hits on the words the pictures land on
for k, kind, extra in [(9, "pop", {"pitch": 1.1}), (11, "pop", {"pitch": 0.8}), (13, "pop", {"pitch": 0.75}), (19, "ding", {}),
                       (21, "pop", {"pitch": 1.2}), (27, "pop", {"pitch": 1.0}), (39, "glitch", {}), (55, "pop", {"pitch": 1.2}),
                       (57, "pop", {"pitch": 1.1}), (62, "pop", {"pitch": 1.0}), (70, "pop", {"pitch": 0.9}), (78, "boom", {"g": 0.6}),
                       (82, "pop", {"pitch": 1.0}), (90, "pop", {"pitch": 1.15}), (96, "boom", {"g": 0.7}), (100, "ding", {}),
                       (108, "pop", {"pitch": 1.2}), (112, "rumble", {"dur": 1.2, "g": 0.6}), (124, "shimmer", {"g": 0.4}),
                       (129, "boom", {"g": 0.5}), (135, "pop", {"pitch": 1.1}), (142, "pop", {"pitch": 1.2}), (161, "pop", {"pitch": 0.9}),
                       (172, "ding", {}), (173, "boom", {"g": 0.55}), (191, "scan", {}), (202, "pop", {"pitch": 1.1}),
                       (206, "ding", {}), (222, "pop", {"pitch": 1.25})]:
    ev.append(dict({"type": kind, "t": round(wt(k) - 0.02, 2)}, **extra))
ev.sort(key=lambda e: e["t"])
json.dump({"length": DUR, "events": ev}, open("sfx.json", "w"), indent=0)


def run(cmd):
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


run(["python3", T + "make_track.py", "music.json", "work/music.wav"])
run(["python3", T + "make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", T + "mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

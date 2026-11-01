"""Short #15 audio: an original score (tools/make_track.py), sound effects on the cuts and hits (tools/make_sfx.py), and the
mix with the creator's voice at -14 LUFS (tools/mix.py) -> assets/mix.wav.
Reads edl.py, work/cuts.json (make_index.py) and words.json. Writes music.json and sfx.json (committed) and work/*.wav.
Usage: python3 make_audio.py
"""
import json
import subprocess

from edl import DUR, wt

T = "../../tools/"
music = {"length": DUR, "bpm": 92, "seed": 15, "style": "dream",
         "chords": [[48, 52, 55, 59], [45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 54]],
         "bass": [36, 33, 29, 31], "drums_from": 2, "outro": 2.5, "whooshes": [], "pops": []}
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
for k, kind, extra in [(4, "shimmer", {"g": 0.4}), (17, "ding", {}), (23, "pop", {"pitch": 1.2}), (36, "boom", {"g": 0.5}),
                       (42, "rumble", {"dur": 1.2, "g": 0.5}), (46, "pop", {"pitch": 1.0}), (55, "pop", {"pitch": 1.1}), (58, "pop", {"pitch": 0.9}),
                       (70, "zap", {"g": 0.4}), (75, "ding", {}), (79, "ticks", {"dur": 1.2, "n": 8}), (89, "scan", {}), (92, "scan", {}),
                       (100, "whoosh", {"rise": 0.3, "fall": 0.3, "g": 0.4}), (104, "boom", {"g": 0.5}), (110, "shimmer", {"g": 0.4}),
                       (119, "glitch", {}), (128, "boom", {"g": 0.6}), (137, "whoosh", {"rise": 0.25, "fall": 0.25, "g": 0.4}),
                       (150, "pop", {"pitch": 0.9}), (157, "pop", {"pitch": 1.1}), (166, "shimmer", {"g": 0.5}), (173, "boom", {"g": 0.6}),
                       (187, "pop", {"pitch": 0.7}), (191, "pop", {"pitch": 0.8}), (209, "shimmer", {"g": 0.4}), (220, "ding", {}),
                       (228, "zap", {"g": 0.6}), (234, "pop", {"pitch": 0.9}), (240, "ding", {}), (259, "pop", {"pitch": 1.0}),
                       (261, "pop", {"pitch": 1.1}), (263, "pop", {"pitch": 1.2}), (270, "ding", {}), (281, "boom", {"g": 0.4}),
                       (305, "pop", {"pitch": 1.1}), (314, "tick", {}), (318, "pop", {"pitch": 0.8}), (326, "zap", {"g": 0.4}),
                       (332, "glitch", {}), (337, "glitch", {}), (354, "zap", {"g": 0.6}), (363, "ding", {}), (379, "pop", {"pitch": 1.1}),
                       (387, "zap", {"g": 0.4}), (397, "pop", {"pitch": 1.2}), (411, "ding", {}), (427, "pop", {"pitch": 1.0}),
                       (435, "boom", {"g": 0.5}), (448, "pop", {"pitch": 0.9}), (457, "shimmer", {"g": 0.4}), (470, "pop", {"pitch": 1.0}),
                       (477, "boom", {"g": 0.5}), (493, "pop", {"pitch": 1.25})]:
    ev.append(dict({"type": kind, "t": round(wt(k) - 0.02, 2)}, **extra))
ev.sort(key=lambda e: e["t"])
json.dump({"length": DUR, "events": ev}, open("sfx.json", "w"), indent=0)


def run(cmd):
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


run(["python3", T + "make_track.py", "music.json", "work/music.wav"])
run(["python3", T + "make_sfx.py", "sfx.json", "work/sfx.wav"])
run(["python3", T + "mix.py", "work/voice_clean.wav", "work/music.wav", "work/sfx.wav", "assets/mix.wav", str(DUR)])

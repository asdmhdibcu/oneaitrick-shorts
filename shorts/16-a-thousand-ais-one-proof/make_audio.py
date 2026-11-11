"""Short #16 audio: the robot effect on the boss's quote (tools/voice_fx.py), an original score (tools/make_track.py) with a
silence beat on "Less than thirty hours later", our synth hits (tools/make_sfx.py), a sound pass from the sound-effects
skill's CC0 library on top, and the mix with the creator's voice at -14 LUFS (tools/mix.py) -> assets/mix.wav.
Reads edl.py, work/cuts.json (make_index.py) and words.json. Writes music.json, sfx.json and cc0.json (committed) and
work/*.wav.
Usage: python3 make_audio.py
"""
import json
import os
import subprocess

import numpy as np
from scipy.io import wavfile

from edl import DUR, SHOTS, wt, we

T = "../../tools/"
LIB = "../../.claude/skills/sound-effects/sfx/"
SR = 48000
T0 = {s[0]: s[1] for s in SHOTS}


def run(cmd):
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


# ---------------------------------------------------------------- voice: the boss's words through the robot preset
ROBOT = (round(wt(158) - 0.1, 2), round(we(163) + 0.08, 2))
run(["python3", T + "voice_fx.py", "work/voice_clean.wav", "work/voice_fx.wav", f"robot@{ROBOT[0]}-{ROBOT[1]}"])

# ---------------------------------------------------------------- score
music = {"length": DUR, "bpm": 100, "seed": 16, "style": "pulse",
         "chords": [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]],
         "bass": [45, 41, 48, 43], "drums_from": 1, "outro": 2.5, "whooshes": [], "pops": []}
json.dump(music, open("music.json", "w"), indent=1)
run(["python3", T + "make_track.py", "music.json", "work/music_raw.wav"])
# the silence beat: the score drops away on "Less than thirty hours later" and comes back on the check
s0, s1 = wt(173) - 0.15, wt(181) - 0.05
run(["ffmpeg", "-v", "error", "-y", "-i", "work/music_raw.wav", "-af",
     f"volume='if(lt(t,{s0}),1,if(lt(t,{s0 + 0.25}),1-(t-{s0})/0.25*0.9,if(lt(t,{s1}),0.1,if(lt(t,{s1 + 0.1}),0.1+(t-{s1})/0.1*0.9,1))))':eval=frame",
     "work/music.wav"])

# ---------------------------------------------------------------- our synth hits: one per cut, plus the words the pictures land on
cuts = json.load(open("work/cuts.json"))["cuts"]
ev = [{"type": "swell", "t": 0.0, "dur": 0.6, "g": 0.5}]
for c in cuts:
    a, b, k = c[0], c[1], c[2]
    t = T0[b]
    if k in ("whip", "slideup"):
        ev.append({"type": "whoosh", "t": round(t - 0.05, 2), "rise": 0.22, "fall": 0.25, "g": 0.5})
    elif k == "zoom":
        ev.append({"type": "whoosh", "t": round(t - 0.04, 2), "rise": 0.2, "fall": 0.2, "g": 0.45})
        ev.append({"type": "pop", "t": round(t, 2), "pitch": 0.9})
    elif k == "flash":
        ev.append({"type": "shimmer", "t": round(t, 2), "g": 0.45})
    elif k == "dip":
        ev.append({"type": "swell", "t": round(t - 0.3, 2), "dur": 0.4, "g": 0.3})
    elif k == "card":
        ev.append({"type": "pop", "t": round(t, 2), "pitch": 1.1})
    if k in ("cut", "dip", "fade", "scratch"):
        ev.append({"type": "pop", "t": round(t - 0.01, 2), "pitch": 0.8, "g": 0.7})
    ev.append({"type": "tick", "t": round(t - 0.01, 2), "g": 1.2})   # a transient right on every cut
HITS = [(7, "boom", {"g": 0.55}), (12, "shimmer", {"g": 0.5}), (14, "scan", {"dur": 1.2, "g": 0.35}),
        (28, "ticks", {"dur": 0.95, "n": 10, "g": 0.6}), (31, "ding", {}), (37, "shimmer", {"g": 0.45}),
        (40, "pop", {"pitch": 1.0}), (46, "scan", {"dur": 0.6, "g": 0.3}), (49, "ding", {"base": 1320}),
        (52, "ticks", {"dur": 1.4, "n": 14, "g": 0.55}), (57, "boom", {"g": 0.5}), (61, "glitch", {}),
        (70, "scan", {"dur": 1.4, "g": 0.4}), (73, "ding", {}), (77, "zap", {"g": 0.5}), (81, "pop", {"pitch": 1.1}),
        (86, "ding", {}), (89, "rumble", {"dur": 1.0, "g": 0.4}), (90, "boom", {"g": 0.45}), (94, "pop", {"pitch": 1.2}),
        (96, "ticks", {"dur": 1.0, "n": 10, "g": 0.5}), (97, "boom", {"g": 0.4}), (100, "pop", {"pitch": 1.0}),
        (104, "pop", {"pitch": 1.15}), (111, "zap", {"g": 0.4}), (114, "whoosh", {"rise": 0.3, "fall": 0.3, "g": 0.4}),
        (115, "ticks", {"dur": 1.3, "n": 16, "g": 0.4}), (126, "ticks", {"dur": 0.8, "n": 12, "g": 0.4}),
        (130, "ticks", {"dur": 0.9, "n": 18, "g": 0.5}), (138, "whoosh", {"rise": 0.3, "fall": 0.35, "g": 0.45}),
        (142, "scan", {"dur": 1.6, "g": 0.35}), (149, "ticks", {"dur": 1.1, "n": 10, "g": 0.6}), (153, "ding", {}),
        (165, "scan", {"dur": 1.4, "g": 0.35}), (174, "ticks", {"dur": 1.1, "n": 8, "g": 0.35}),
        (181, "boom", {"g": 0.6}), (181, "ding", {"base": 1320}), (185, "boom", {"g": 0.5}), (186, "pop", {"pitch": 0.9}),
        (199, "pop", {"pitch": 1.0}), (202, "pop", {"pitch": 1.1}), (204, "ticks", {"dur": 1.05, "n": 20, "g": 0.45}),
        (211, "whoosh", {"rise": 0.5, "fall": 0.6, "g": 0.3}), (222, "ticks", {"dur": 2.0, "n": 19, "g": 0.55}),
        (227, "ding", {}), (232, "pop", {"pitch": 0.9}), (237, "pop", {"pitch": 1.2}), (240, "boom", {"g": 0.5}),
        (243, "pop", {"pitch": 1.0}), (253, "pop", {"pitch": 1.25}), (255, "ding", {})]
for k, kind, extra in HITS:
    ev.append(dict({"type": kind, "t": round(wt(k) - 0.02, 2)}, **extra))
ev.sort(key=lambda e: e["t"])
json.dump({"length": DUR, "events": ev}, open("sfx.json", "w"), indent=0)
run(["python3", T + "make_sfx.py", "sfx.json", "work/sfx.wav"])

# ---------------------------------------------------------------- the CC0 sound pass (sound-effects skill library)
A = lambda sid: T0[sid]  # noqa: E731
CC0 = [  # (file in the library, time, gain, longest seconds)
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(7), 0.55, 1.5),       # CAN'T BE DONE stamp
    ("ding/kenney-interface-confirmation-001.ogg", wt(12), 0.5, 1.5),           # DONE
    ("pop/kenney-interface-pluck-001.ogg", wt(23), 0.6, 0.6), ("pop/kenney-interface-pluck-001.ogg", wt(25), 0.6, 0.6),  # bricks
    ("impact/fs-222517-dramatic-hit.ogg", wt(57), 0.35, 2.5),                    # 358 YEARS
    ("glitch/kenney-sci-computernoise-001.ogg", wt(61), 0.4, 0.8),              # the hidden mistake
    ("typing/fs-447909-keyboard-typing.ogg", A("s10") + 0.25, 0.4, 1.7),        # the Lean statement types in
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(77) - 0.03, 0.5, 1.2),  # the wrong brick bounces off
    ("riser/kenney-digital-powerup2.ogg", A("s17") - 0.05, 0.35, 1.5),          # this week
    ("riser/fs-685256-riser-sound-effect-short-wav.ogg", A("s18") - 0.1, 0.35, 1.5),  # 1 -> 1,000
    ("riser/fs-174363-rewind.ogg", A("s21") - 0.05, 0.55, 0.9),                 # the twist: record scratch
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(131), 0.45, 1.2),     # CAN'T BE DONE again
    ("typing/fs-416777-digital-typing-wav.ogg", wt(158) - 0.05, 0.3, 1.5),      # the boss types its message
    ("impact/fs-222517-dramatic-hit.ogg", wt(181), 0.45, 3.0),                   # the inspector says yes
    ("impact/kenney-impact-impactsoft-heavy-000.ogg", wt(185), 0.6, 1.5),       # THE CATCH
    ("ding/fs-571513-soft-notifications-bell-ding-d.ogg", wt(227), 0.4, 1.5),   # the 19th reminder
    ("transition/fs-683096-woosh.ogg", wt(240) - 0.1, 0.45, 1.2),               # KEEP GOING
    ("ding/kenney-interface-confirmation-001.ogg", wt(255), 0.4, 1.5),          # comment it
]
CC0 = [c for c in CC0 if c[2] > 0]
manifest = json.load(open(LIB + "manifest.json"))
credits = {e["file"]: e.get("attribution") or e.get("credit") for e in manifest["bundled"] + manifest["default_kit"] if "file" in e}
n = int((DUR + 1) * SR)
layer = np.zeros((n, 2))
for f, t, g, mx in CC0:
    tmp = "work/cc0_tmp.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", LIB + f, "-t", str(mx), "-ar", str(SR), "-ac", "2", tmp], check=True)
    sr, x = wavfile.read(tmp)
    x = x.astype(np.float64) / 32768.0
    fade = min(len(x), int(0.05 * SR)); x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    i = int(max(t, 0) * SR); j = min(n, i + len(x)); layer[i:j] += g * x[: j - i]
os.remove("work/cc0_tmp.wav")
json.dump({"length": DUR, "sounds": [{"file": f, "t": round(t, 2), "gain": g, "credit": credits.get(f, "")} for f, t, g, _ in CC0]},
          open("cc0.json", "w"), indent=1)
sr, s = wavfile.read("work/sfx.wav")
s = s.astype(np.float64) / 32768.0
if s.ndim == 1:
    s = np.stack([s, s], axis=1)
if sr != SR:
    raise SystemExit(f"sfx.wav is {sr} Hz, expected {SR}")
m = min(len(s), n)
both = layer[:m] + s[:m]
both /= max(1.0, np.max(np.abs(both)) / 0.9)
wavfile.write("work/sfx_all.wav", SR, (both * 32767).astype(np.int16))

os.makedirs("assets", exist_ok=True)
run(["python3", T + "mix.py", "work/voice_fx.wav", "work/music.wav", "work/sfx_all.wav", "assets/mix.wav", str(DUR)])

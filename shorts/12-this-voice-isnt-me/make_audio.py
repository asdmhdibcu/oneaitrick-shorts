"""Short #12: write sfx.json and mix the soundtrack (voice + music12.py score + SFX) to -14 LUFS.
VARIANT=trial mixes the Trial Reel (work/voice_trial.wav -> assets/mix_trial.wav, sfx_trial.json, plan_trial.json).
The score drops out when the phone rings ("Then the phone rings") and crashes back in on "Crying"; it lifts to the major
key for the fix (the safe phrase). Times come from words.json (edl.wt with edl.K for the main cut's word numbers) and the cuts.
Usage: python3 make_audio.py   (needs work/voice_clean.wav or work/voice_trial.wav, and work/cuts*.json from make_index.py)
"""
import json
import subprocess

from edl import DUR, SHOTS, VARIANT, K, wt

MAIN = VARIANT == "main"
T0 = {s[0]: s[1] for s in SHOTS}
cuts = json.load(open("work/cuts.json" if MAIN else "work/cuts_trial.json"))["cuts"]
VOICE, MIX, SFXJ, PLANJ, SFXW, MUSW = (("work/voice_clean.wav", "assets/mix.wav", "sfx.json", "plan_short.json", "work/sfx.wav", "work/music.wav") if MAIN else
                                       ("work/voice_trial.wav", "assets/mix_trial.wav", "sfx_trial.json", "plan_trial.json", "work/sfx_trial.wav", "work/music_trial.wav"))
ev = []
for a, b, kind in cuts:
    t = T0[b]
    if kind in ("whip", "slideup"):
        ev.append({"type": "whoosh", "t": t - 0.02, "rise": 0.18, "fall": 0.3, "g": 0.42})
    elif kind == "zoom":
        ev.append({"type": "whoosh", "t": t, "rise": 0.22, "fall": 0.3, "g": 0.42}); ev.append({"type": "pop", "t": t, "pitch": 0.9, "g": 0.18})
    elif kind == "card":
        ev.append({"type": "whoosh", "t": t, "rise": 0.15, "fall": 0.25, "g": 0.32}); ev.append({"type": "pop", "t": t + 0.1, "pitch": 1.15, "g": 0.22})
    elif kind == "cut":
        ev.append({"type": "tick", "t": t, "g": 0.6})
    elif kind == "fade":
        ev.append({"type": "swell", "t": t - 0.3, "dur": 0.6, "g": 0.3})


def w(k):
    return wt(K(k))


def pops(ks, pitch=1.0, g=0.2, step=0.0):
    return [{"type": "pop", "t": w(k), "pitch": pitch + j * step, "g": g} for j, k in enumerate(ks)]


def stamp(k):
    return [{"type": "boom", "t": w(k), "g": 0.45}, {"type": "tick", "t": w(k), "g": 0.9}]


opening = ([{"type": "swell", "t": 0.0, "dur": 0.6, "g": 0.25}, {"type": "boom", "t": wt(6), "g": 0.3},
            {"type": "shimmer", "t": wt(14), "g": 0.25}, {"type": "pop", "t": wt(37), "pitch": 1.1, "g": 0.22}] if MAIN else
           [{"type": "ring", "t": 0.05, "rings": 2, "g": 0.32}, {"type": "pop", "t": wt(11), "pitch": 1.0, "g": 0.2}])
moments = opening + (
    [{"type": "ding", "t": w(50), "base": 1320, "g": 0.22}] + pops([55, 58, 61], 1.0, 0.18, 0.08)
    + [{"type": "ring", "t": T0["k06"] + 0.15, "rings": 3, "g": 0.55}]                                     # the phone rings
    + pops([80, 83], 0.9, 0.26, 0.1) + [{"type": "boom", "t": w(86), "g": 0.45}]
    + pops([99, 103], 1.0, 0.2, 0.08) + [{"type": "ding", "t": w(128), "base": 1320, "g": 0.2}]
    + [{"type": "glitch", "t": w(143) - 0.05, "dur": 0.3, "g": 0.3}] + stamp(143) + [{"type": "zap", "t": w(145), "g": 0.3}]
    + [{"type": "shimmer", "t": w(154), "g": 0.3}] + pops([164, 169, 172], 1.0, 0.2, 0.08)
    + [{"type": "ring", "t": T0["k15"] + 0.1, "rings": 2, "g": 0.4}] + pops([185], 1.0, 0.2) + stamp(191)
    + [{"type": "ding", "t": w(194), "base": 1320, "g": 0.25}]
    + [{"type": "pop", "t": w(203), "pitch": 1.0, "g": 0.22}, {"type": "tick", "t": w(214), "g": 0.7}, {"type": "ding", "t": w(216), "base": 1760, "g": 0.25}]
    + [{"type": "swell", "t": T0["k17"] - 0.2, "dur": 0.5, "g": 0.3}, {"type": "pop", "t": T0["k17"] + 0.15, "pitch": 1.0, "g": 0.35},
       {"type": "ding", "t": T0["k17"] + 0.85, "base": 1320, "g": 0.3}]
)
events = sorted(ev + moments, key=lambda e: e["t"])
json.dump({"length": DUR, "events": events}, open(SFXJ, "w"))

c = lambda sid: round(T0[sid], 2)
quiet = (c("k06") + 0.05, c("k07") - 0.05)           # the phone rings in silence
plan = {"bpm": 84, "transpose": 5,
        "sections": [[0.0, c("k04"), "MIN", 1], [c("k04"), quiet[0], "MIN", 2], [quiet[1], c("k08"), "MIN", 3], [c("k08"), c("k12"), "MIN", 3],
                     [c("k12"), c("k13"), "MIN", 2], [c("k13"), c("k16"), "MAJ", 2], [c("k16"), c("k17"), "MAJ", 1]],
        "silence": [list(quiet)],
        "hits": [c("k04"), quiet[1], c("k12"), c("k13")],
        "risers": [[c("k13") - 1.2, 1.2]],
        "end": c("k17")}
json.dump(plan, open(PLANJ, "w"))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    print(r.stdout.strip()[-200:])


run(["python3", "../../longform/this-voice-isnt-me/music12.py", PLANJ, MUSW, str(DUR)])
run(["python3", "../../tools/make_sfx.py", SFXJ, SFXW])
run(["python3", "../../tools/mix.py", VOICE, MUSW, SFXW, MIX, str(DUR)])

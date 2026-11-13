"""Short #18 audio: an original score (tools/make_track.py) with one silence before the biggest reveal (86 %),
a sub-bass hit under the first 0.5 s, our synth hits (tools/make_sfx.py: coin clinks, the beam's creak, odometer ticks),
a sound pass from the sound-effects skill's CC0 library, and the mix with the creator's voice at -14 LUFS with the
deep #18 duck (tools/mix.py ... deep) -> assets/mix.wav.
The odometer ticks and the coin's spin run to the last frame and pick up on frame one, so the loop is seamless.
Writes music.json, sfx.json and cc0.json (committed) and work/*.wav.
Usage: python3 make_audio.py
"""
import json
import os
import subprocess

import numpy as np
from scipy.io import wavfile

T = "../../tools/"
LIB = "../../.claude/skills/sound-effects/sfx/"
SR = 48000
DUR = 56.95
W = json.load(open("words.json"))
wt = lambda k: W[k]["start"]  # noqa: E731


def run(cmd):
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


os.makedirs("work", exist_ok=True)

# ---------------------------------------------------------------- score: D minor, curious, 100 bpm
music = {"length": DUR, "bpm": 100, "seed": 18, "style": "pulse",
         "chords": [[50, 53, 57, 62], [46, 50, 53, 58], [53, 57, 60, 65], [48, 52, 55, 60]],
         "bass": [38, 34, 41, 36], "drums_from": 1, "outro": 0.4, "whooshes": [], "pops": []}
json.dump(music, open("music.json", "w"), indent=1)
run(["python3", T + "make_track.py", "music.json", "work/music_raw.wav"])
# the one silence (critic 2): score and SFX drop to nothing after the last bar lands (15.9) and slam back on EIGHTY-SIX;
# only the voice ("...coin's side") is left for 0.7 s
s0, s1 = 15.90, wt(49) - 0.02
run(["ffmpeg", "-v", "error", "-y", "-i", "work/music_raw.wav", "-af",
     f"volume='if(lt(t,{s0}),1,if(lt(t,{s0 + 0.08}),1-(t-{s0})/0.08,if(lt(t,{s1}),0,if(lt(t,{s1 + 0.04}),(t-{s1})/0.04,1))))':eval=frame",
     "work/music.wav"])

# ---------------------------------------------------------------- our synth hits
ev = []
E = lambda kind, t, **kw: ev.append(dict({"type": kind, "t": round(t, 3)}, **kw))  # noqa: E731
FLICK = [wt(22), wt(23), wt(24), wt(25)]
TE, TB = wt(152) - 0.05, wt(159) - 0.04

# 0-4 s: the hook. Sub-bass hit, the 50 rolls in (odometer ticks slowing), the coin spins and lands on "ONE"
E("sub", 0.0, g=1.0)
def odo_ticks(p, t0, t1, g):                                                     # a tick each time a digit passes
    ts = np.linspace(t0, t1, 4000); ps = np.array([p(t) for t in ts]); prev = np.floor(ps[0])
    for t, v in zip(ts, ps):
        if np.floor(v) != prev:
            prev = np.floor(v); E("tick", t, g=g)
odo_ticks(lambda t: -2.5 + 12.5 * (1 - (1 - t / 0.8) ** 3), 0.0, 0.8, 0.6)       # the 50 rolls in
for k in range(10):                                                              # the spinning coin settles (Euler's disk)
    E("tick", 0.25 + 2.65 * (1 - (1 - k / 10) ** 1.6), g=0.8 + 0.06 * k)
E("clink", wt(7), g=1.0)                                                         # ONE: the coin stops
E("whoosh", wt(10) - 0.05, rise=0.25, fall=0.2, g=0.35); E("pop", wt(10) + 0.2, pitch=0.9)   # the title parks as pin 1
# 4-10 s: the AI helper, the secret picks
E("whoosh", wt(11) - 0.05, rise=0.2, fall=0.25, g=0.4)                          # push in
E("shimmer", 4.7, g=0.25)                                                        # the orb wakes
E("pop", wt(11) + 0.48, pitch=1.15); E("pop", wt(15), pitch=0.95)                       # the two chat bubbles
E("clink", wt(19), g=0.8, pitch=1.05); E("whoosh", wt(19) - 0.05, rise=0.1, fall=0.2, g=0.3)   # "And a coin": the coin flips
E("whoosh", wt(21) - 0.15, rise=0.15, fall=0.2, g=0.3)                           # the choice card
for i, t in enumerate(FLICK):                                                    # the secret flicks
    E("clink", t, g=0.55, pitch=[1.0, 1.12, 0.94, 1.06][i]); E("pop", t + 0.08, pitch=1.3, g=0.6)
E("whoosh", 9.45, rise=0.1, fall=0.4, g=0.3); E("shimmer", 9.9, g=0.6)          # the coin dives into the AI
# 10-15 s: the scale
E("whoosh", wt(26) - 0.1, rise=0.2, fall=0.25, g=0.35); E("pop", wt(26), pitch=1.2)   # chapter SCALE, pull out
E("boom", wt(29), g=0.18); E("boom", wt(30), g=0.18)                             # the two options drop on the dishes
E("pop", wt(32), pitch=1.0)                                                      # "="
E("clink", wt(36), g=0.9, pitch=0.9); E("creak", wt(36) + 0.02, dur=0.6, g=0.9)   # the AI's coin drops, the beam tips
E("pop", wt(40), pitch=0.8, g=0.7)                                              # keyword pop: ONE
# 15-21 s: 86 %
E("pop", wt(42), pitch=1.1); E("whoosh", wt(42) - 0.05, rise=0.18, fall=0.25, g=0.3)   # chapter FOLLOW, the split
for i in range(4):                                                               # the four bars (all before the silence)
    E("pop", 15.1 + i * 0.2, pitch=0.8 + 0.12 * i, g=0.7)
E("boom", wt(49), g=0.55); E("ticks", wt(49), dur=0.75, n=12, g=0.6); E("ding", wt(49) + 0.72, g=0.4)   # EIGHTY-SIX
E("whoosh", 18.2, rise=0.2, fall=0.25, g=0.3)
E("scan", wt(55), dur=0.3, g=0.5); E("scan", wt(55) + 0.35, dur=0.3, g=0.5); E("scan", wt(57), dur=0.35, g=0.6)   # highlights
E("whoosh", 20.6, rise=0.2, fall=0.25, g=0.35); E("pop", 21.1, pitch=0.9)       # pull out, pin 2
E("creak", 20.7, dur=0.35, g=0.45, pitch=1.1)                                   # the scale resets
# 21-27 s: already decided, switched
E("boom", wt(60), g=0.2); E("creak", wt(60) + 0.02, dur=0.45, g=0.6, pitch=0.95)   # MY PICK lands, the beam leans the other way
E("shimmer", 22.8, g=0.5)
E("clink", wt(65), g=0.8, pitch=0.9); E("creak", wt(65) + 0.02, dur=0.55, g=0.8)   # disagreed: the coin comes back
E("whoosh", wt(67) - 0.1, rise=0.15, fall=0.2, g=0.3); E("creak", wt(67) + 0.02, dur=0.45, g=0.6)   # switched
E("pop", wt(68) - 0.05, pitch=1.1); E("ticks", wt(68), dur=0.8, n=10, g=0.5); E("ding", wt(68) + 0.8, g=0.3)   # 60 %
E("whoosh", wt(72) + 0.3, rise=0.15, fall=0.2, g=0.3); E("pop", wt(72) + 0.6, pitch=0.9)   # pin 3
# 27-32 s: the report, the credit
E("glitch", wt(73), dur=0.25, g=0.6)
for t in (wt(78) + 0.05, 28.9, 29.4):                                            # the AI's words thread into the report
    E("zap", t, g=0.6); E("tick", t + 0.25, g=1.1)
E("tick", wt(82), g=1.0); E("pop", wt(85), pitch=1.2); E("ding", wt(85) + 0.05, base=1320, g=0.4)   # the 1 in 7: credit "AI"
for i in range(6):
    E("pop", wt(87) + i * 0.04, pitch=0.6 - 0.04 * i, g=0.35)
E("whoosh", 31.75, rise=0.15, fall=0.3, g=0.35); E("pop", 32.25, pitch=0.9); E("pop", 32.65, pitch=1.0)   # pins 4 and 5
# 32-40 s: the catch
E("boom", wt(91) - 0.02, g=0.45); E("glitch", wt(92), dur=0.2, g=0.45)           # THE CATCH
E("whoosh", wt(93) - 0.1, rise=0.2, fall=0.25, g=0.35)
E("scan", wt(96) - 0.1, dur=0.45, g=0.55); E("pop", wt(96), pitch=0.8, g=0.6)   # OWN
E("whoosh", 35.6, rise=0.2, fall=0.25, g=0.35)
E("boom", wt(103), g=0.35); E("creak", wt(103) + 0.02, dur=0.4, g=1.0, pitch=0.8); E("clink", wt(103), g=0.6, pitch=0.7)   # HEAVY
E("scan", wt(104) + 0.2, dur=0.3, g=0.5); E("scan", wt(104) + 0.55, dur=0.3, g=0.5)
E("creak", wt(109), dur=0.6, g=0.85, pitch=1.05)                                 # "push less": the beam eases
E("whoosh", 39.55, rise=0.1, fall=0.25, g=0.3)                                  # the strip goes
E("pop", wt(110) + 0.4, pitch=0.9)                                               # pin 6
# 40-48 s: the fix
E("pop", wt(111), pitch=1.2); E("whoosh", wt(111) - 0.1, rise=0.2, fall=0.25, g=0.35)
E("whoosh", wt(125) + 0.3, rise=0.12, fall=0.4, g=0.4); E("shimmer", wt(125) + 0.8, g=0.6)   # the question flies to the AI
E("whoosh", wt(126) - 0.1, rise=0.2, fall=0.25, g=0.3)
E("clink", wt(129), g=0.9, pitch=1.15); E("creak", wt(129) + 0.02, dur=0.7, g=0.7, pitch=1.05)   # the lime coin on the other side
E("ding", wt(132) + 0.05, base=1568, g=0.45)                                    # level
E("pop", wt(132) + 0.55, pitch=0.9)                                             # pin 7
E("pop", wt(136), pitch=1.3)                                                    # YOURS
# 48-57 s: the recap, the end card, the loop
E("whoosh", wt(137) + 0.1, rise=0.2, fall=0.25, g=0.3); E("clink", wt(137) + 0.55, g=0.7)   # the coin returns
E("shimmer", wt(144), g=0.35); E("shimmer", wt(148), g=0.4)
E("pop", wt(150), pitch=1.3, g=1.2); E("tick", wt(150) + 0.05, g=1.5)                   # THE WORD?
E("swell", TE - 0.5, dur=0.55, g=0.3); E("shimmer", TE, g=0.35); E("boom", TE, g=0.2)   # end card
E("pop", TE + 0.85, pitch=1.2)                                                  # FOLLOW
E("whoosh", TB - 0.15, rise=0.15, fall=0.2, g=0.3)                              # the hook comes back
E("pop", wt(160), pitch=1.2, g=0.6)                                              # YOU'D
odo_ticks(lambda t: -2.5 - 7.5 * (1 - (1 - (DUR - t) / 0.49) ** 3), DUR - 0.49, DUR - 0.005, 0.6)   # the 50 spins up into frame one
ev.sort(key=lambda e: e["t"])
json.dump({"length": DUR, "events": ev}, open("sfx.json", "w"), indent=0)
run(["python3", T + "make_sfx.py", "sfx.json", "work/sfx.wav"])

# ---------------------------------------------------------------- the CC0 sound pass (sound-effects skill library)
CC0 = [  # (file in the library, time, gain, longest seconds)
    ("impact/kenney-sci-lowfrequency-explosion-000.ogg", 0.0, 0.35, 1.2),          # the braam under the open
    ("click/kenney-interface-click-001.ogg", wt(11) + 0.2, 1.0, 0.4),              # the AI HELPER chip
    ("ui-blip/kenney-digital-twotone1.ogg", wt(11) + 0.48, 0.4, 0.5),                     # the question
    ("ui-blip/kenney-digital-pepsound1.ogg", wt(15), 0.4, 0.5),                    # the answer
    ("impact/kenney-impact-impactsoft-heavy-000.ogg", wt(21), 0.35, 1.0),          # the card of secret picks
    ("transition/fs-786514-swoosh-v2.ogg", wt(26) - 0.15, 0.3, 0.9),              # pull out to the scale
    ("pop/kenney-interface-drop-001.ogg", wt(29), 0.55, 0.6),                      # option A lands
    ("pop/kenney-interface-drop-002.ogg", wt(30), 0.55, 0.6),                      # option B lands
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(36), 0.35, 0.9),         # the coin drops
    ("transition/fs-702773-swipe-wav.ogg", wt(42) + 0.15, 0.35, 0.8),             # the chart wipes in
    ("impact/fs-222517-dramatic-hit.ogg", wt(49), 0.35, 2.0),                     # EIGHTY-SIX
    ("transition/fs-702773-swipe-wav.ogg", 18.45, 0.4, 0.8),                       # the proof card turns in
    ("click/kenney-interface-select-002.ogg", wt(60), 0.4, 0.5),                   # MY PICK
    ("impact/kenney-impact-impactsoft-heavy-001.ogg", wt(65), 0.4, 1.0),           # disagreed
    ("click/kenney-interface-toggle-002.ogg", wt(67) + 0.1, 0.5, 0.5),             # switched
    ("riser/fs-174363-rewind.ogg", wt(73) - 0.05, 0.5, 0.9),                       # record scratch: "Here's the weird part"
    ("transition/kenney-interface-maximize-005.ogg", wt(73) + 0.1, 0.35, 0.6),    # the report slides up
    ("ding/kenney-interface-glass-001.ogg", wt(85), 0.35, 0.9),                    # one in seven gave credit
    ("impact/kenney-impact-impactsoft-heavy-000.ogg", wt(91), 0.5, 1.2),           # THE CATCH
    ("transition/fs-702773-swipe-wav.ogg", wt(93) - 0.05, 0.4, 0.8),              # proof card 2
    ("impact/kenney-sci-lowfrequency-explosion-001.ogg", wt(103), 0.2, 1.4),       # HEAVY
    ("transition/kenney-interface-scroll-001.ogg", wt(104), 0.4, 0.5),             # the limitation strip
    ("typing/fs-447909-keyboard-typing.ogg", wt(118) - 0.05, 0.8, wt(125) - wt(118) + 0.5),   # typing the question
    ("click/kenney-interface-click-001.ogg", wt(125) + 0.2, 0.6, 0.4),             # send
    ("ding/kenney-interface-confirmation-001.ogg", wt(136), 0.4, 1.2),             # the choice is YOURS
    ("ding/kenney-interface-confirmation-002.ogg", wt(144), 0.35, 1.0),            # recap: the problem
    ("ding/kenney-interface-confirmation-003.ogg", wt(148), 0.35, 1.0),            # recap: the fix
    ("click/kenney-interface-tick-001.ogg", wt(150), 0.5, 0.4),                    # comment it
]
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
    fi = min(len(x), int(0.01 * SR)); x[:fi] *= np.linspace(0, 1, fi)[:, None]
    i = int(max(t, 0) * SR); j = min(n, i + len(x)); layer[i:j] += g * x[: j - i]
os.remove("work/cc0_tmp.wav")
json.dump({"length": DUR, "sounds": [{"file": f, "t": round(t, 2), "gain": g, "credit": credits.get(f, "")} for f, t, g, _ in CC0]},
          open("cc0.json", "w"), indent=1)
sr, s = wavfile.read("work/sfx.wav")
SIL = (s0, s1)   # the SFX are muted through the silence too
s = s.astype(np.float64) / 32768.0
if s.ndim == 1:
    s = np.stack([s, s], axis=1)
m = min(len(s), n)
both = layer[:m] + s[:m]
i0, i1 = int(SIL[0] * SR), int(SIL[1] * SR)
both[i0:i1] = 0.0
both /= max(1.0, np.max(np.abs(both)) / 0.9)
wavfile.write("work/sfx_all.wav", SR, (both * 32767).astype(np.int16))

MG = os.environ.get("MG", "0.65")   # score gain before the duck: it flares to this in the pauses
SG = os.environ.get("SG", "0.4")    # SFX stem gain: about 12-14 dB under the voice
run(["python3", T + "mix.py", "assets/voice_raw.wav", "work/music.wav", "work/sfx_all.wav", "assets/mix.wav", str(DUR), MG, SG, "deep"])
# loudnorm drops the last partial block: pad back to the full length so the mux never comes up short
run(["ffmpeg", "-v", "error", "-y", "-i", "assets/mix.wav", "-af", f"apad=whole_dur={DUR + 0.1}", "-c:a", "pcm_s16le", "work/mix_pad.wav"])
os.replace("work/mix_pad.wav", "assets/mix.wav")

"""Short #17 audio: an original score (tools/make_track.py) that drops out for the mirror call at the end (only the ring is
heard), our synth hits (tools/make_sfx.py, phone rings included), a sound pass from the sound-effects skill's CC0 library,
and the mix with the creator's voice at -14 LUFS (tools/mix.py) -> assets/mix.wav.
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
DUR = 81.5
W = json.load(open("words.json"))
wt = lambda k: W[k]["start"]  # noqa: E731


def run(cmd):
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


# ---------------------------------------------------------------- score: minor, tense, 92 bpm
music = {"length": DUR, "bpm": 92, "seed": 17, "style": "pulse",
         "chords": [[57, 60, 64, 71], [53, 57, 60, 64], [50, 53, 57, 60], [52, 56, 59, 62]],
         "bass": [45, 41, 38, 40], "drums_from": 1, "outro": 2.5, "whooshes": [], "pops": []}
json.dump(music, open("music.json", "w"), indent=1)
run(["python3", T + "make_track.py", "music.json", "work/music_raw.wav"])
# the one silence: the score falls away when the phone rings again ("Now your phone rings") and comes back for the recap
s0, s1 = wt(197) - 0.2, wt(213) - 0.1
run(["ffmpeg", "-v", "error", "-y", "-i", "work/music_raw.wav", "-af",
     f"volume='if(lt(t,{s0}),1,if(lt(t,{s0 + 0.3}),1-(t-{s0})/0.3*0.95,if(lt(t,{s1}),0.05,if(lt(t,{s1 + 0.15}),0.05+(t-{s1})/0.15*0.95,1))))':eval=frame",
     "work/music.wav"])

# ---------------------------------------------------------------- our synth hits
ev = [{"type": "swell", "t": 0.0, "dur": 0.6, "g": 0.4}]
E = lambda kind, t, **kw: ev.append(dict({"type": kind, "t": round(t, 2)}, **kw))  # noqa: E731
for t in (0.15, 1.35, 2.55, 3.75, 4.95):                        # Mom calling
    E("ring", t, rings=2, g=0.9)
E("whoosh", 3.2, rise=0.2, fall=0.25, g=0.4); E("pop", 3.72, pitch=0.9)          # the claim parks as pin 1
E("whoosh", wt(15) - 0.2, rise=0.22, fall=0.25, g=0.45)                         # on "rings": into the phone
E("pop", wt(19) - 0.1, pitch=0.7); E("rumble", wt(19), dur=3.0, g=0.22)          # she answers, crying
E("boom", wt(24), g=0.5)                                                         # NOW
E("shimmer", wt(25) - 0.05, g=0.3); E("whoosh", wt(25) - 0.05, rise=0.22, fall=0.3, g=0.35)   # her voice becomes a key, back to the board
E("tick", wt(33), g=1.4); E("pop", wt(33) + 0.02, pitch=0.55)                    # the key turns
E("swell", wt(37) - 0.5, dur=0.6, g=0.35); E("shimmer", wt(37), g=0.35)          # the door opens
E("pop", wt(38), pitch=1.2); E("scan", wt(41) - 0.2, dur=1.3, g=0.5)             # COPY: the scan
E("ding", wt(45), base=1320, g=0.6)                                              # the copy
E("whoosh", wt(49) - 0.1, rise=0.22, fall=0.25, g=0.4); E("pop", wt(49) + 0.25, pitch=1.1)
E("scan", wt(57) - 0.1, dur=0.6, g=0.35); E("ding", wt(57), g=0.5)              # THIRTY seconds
E("whoosh", wt(62) - 0.25, rise=0.2, fall=0.2, g=0.3); E("pop", wt(62), pitch=1.0)
E("pop", wt(65), pitch=1.2); E("pop", wt(66), pitch=1.35); E("shimmer", wt(72), g=0.4)   # the copy is MINE
E("whoosh", wt(72) + 0.05, rise=0.2, fall=0.25, g=0.35); E("pop", wt(72) + 1.0, pitch=0.9)   # pin 2
E("pop", wt(73), pitch=1.2); E("whoosh", wt(73) - 0.1, rise=0.2, fall=0.25, g=0.35)
E("boom", wt(76) + 0.3, g=0.4)                                                  # FOR SALE drops
E("whoosh", wt(81) - 0.1, rise=0.22, fall=0.25, g=0.4); E("pop", wt(81) + 0.2, pitch=1.1)
E("scan", wt(84), dur=0.6, g=0.35); E("whoosh", wt(88) - 0.25, rise=0.2, fall=0.25, g=0.4)
E("ticks", wt(89), dur=1.35, n=14, g=0.6); E("boom", wt(92), g=0.5); E("ding", wt(92) + 0.05, g=0.45)   # SEVEN times
E("whoosh", wt(96) + 0.1, rise=0.2, fall=0.25, g=0.35); E("pop", wt(96) + 0.95, pitch=0.9)              # pin 3
E("zap", wt(97) + 0.15, g=0.6); E("pop", wt(98), pitch=0.8)                      # the lock breaks, STOLEN
E("whoosh", wt(103) - 0.05, rise=0.15, fall=0.2, g=0.3); E("ticks", wt(103) + 0.1, dur=0.85, n=10, g=0.55); E("ding", wt(105) + 0.3, g=0.4)
E("pop", wt(106) + 0.4, pitch=0.9)                                               # pin 4
E("pop", wt(109), pitch=1.0)                                                     # #1?
E("whoosh", wt(115) - 0.05, rise=0.15, fall=0.25, g=0.35); E("boom", wt(116), g=0.35)   # isn't Mom
E("whoosh", wt(117) - 0.15, rise=0.12, fall=0.15, g=0.5); E("boom", wt(117), g=0.45)    # crash zoom: your BANK
E("ring", wt(117) + 0.05, rings=2, g=0.8); E("pop", wt(119), pitch=1.2); E("pop", wt(119) + 0.05, pitch=0.9)   # BANK chapter, the #1 badge
E("pop", wt(120), pitch=0.7); E("pop", wt(121), pitch=1.0); E("glitch", wt(120) + 0.2, dur=0.3, g=0.6)   # the fake line answers
E("whoosh", wt(130) - 0.3, rise=0.2, fall=0.2, g=0.35); E("scan", wt(131), dur=0.6, g=0.35)
E("pop", wt(132), pitch=0.9); E("whoosh", wt(136), rise=0.2, fall=0.3, g=0.35)   # the code flies into the deadbolt
E("boom", wt(140), g=0.5); E("zap", wt(140) + 0.05, g=0.45)                     # they're in
E("whoosh", wt(141) + 0.1, rise=0.2, fall=0.25, g=0.35); E("pop", wt(141) + 0.9, pitch=0.9)   # pin 5
E("whoosh", wt(142) - 0.2, rise=0.2, fall=0.25, g=0.35)
for k in range(3):
    E("tick", wt(150) + k * 0.18, g=1.3)
E("pop", wt(154), pitch=1.1); E("pop", wt(156), pitch=1.2); E("glitch", wt(157), dur=0.25, g=0.6); E("whoosh", wt(158), rise=0.15, fall=0.15, g=0.25)
E("pop", wt(160), pitch=1.2); E("whoosh", wt(160) - 0.15, rise=0.2, fall=0.25, g=0.35)   # LOCKS chapter
E("pop", wt(162), pitch=0.9); E("pop", wt(162) + 0.2, pitch=1.0)
E("whoosh", wt(164), rise=0.25, fall=0.3, g=0.3); E("boom", wt(167) - 0.1, g=0.35); E("glitch", wt(167) - 0.1, dur=0.25, g=0.5)
E("whoosh", wt(168) - 0.1, rise=0.22, fall=0.25, g=0.4); E("scan", wt(170), dur=0.7, g=0.35)
E("pop", wt(173), pitch=1.0); E("shimmer", wt(173) + 0.1, g=0.35)               # the safe-word card
E("whoosh", wt(176) + 0.3, rise=0.2, fall=0.25, g=0.35); E("pop", wt(176) + 0.95, pitch=0.9)   # pin 6
E("whoosh", wt(180) - 0.05, rise=0.25, fall=0.1, g=0.35); E("zap", wt(180) + 0.3, g=0.4)       # the code hits the edge
E("tick", wt(182), g=1.4)
E("whoosh", wt(184) - 0.25, rise=0.2, fall=0.25, g=0.4); E("scan", wt(185), dur=0.5, g=0.3)
E("boom", wt(187), g=0.5)                                                       # REAL BANKS NEVER ASK
E("pop", wt(189) - 0.3, pitch=0.9); E("pop", wt(189), pitch=0.6)
E("whoosh", wt(194) - 0.05, rise=0.2, fall=0.25, g=0.35); E("pop", wt(194) + 0.5, pitch=0.9)    # on "number": pin 7
for t in (wt(197) + 0.05, wt(199) + 0.35):                                       # the mirror: Mom calls again
    E("ring", t, rings=2, g=1.0)
E("pop", wt(201) + 0.15, pitch=0.7); E("whoosh", wt(201) + 0.2, rise=0.2, fall=0.25, g=0.3); E("pop", wt(202), pitch=1.1); E("pop", wt(206), pitch=1.2)
E("whoosh", wt(213) - 0.05, rise=0.25, fall=0.3, g=0.35)                       # the recap: back to the board
E("shimmer", wt(215), g=0.35); E("shimmer", wt(218), g=0.4)                   # the attack lights up, then the locks
E("pop", wt(220), pitch=1.3)
E("shimmer", wt(222) - 0.05, g=0.4); E("boom", wt(222) - 0.05, g=0.3)           # end card
ev.sort(key=lambda e: e["t"])
json.dump({"length": DUR, "events": ev}, open("sfx.json", "w"), indent=0)
run(["python3", T + "make_sfx.py", "sfx.json", "work/sfx.wav"])

# ---------------------------------------------------------------- the CC0 sound pass (sound-effects skill library)
CC0 = [  # (file in the library, time, gain, longest seconds)
    ("ambience/fs-329533-room-tone-in-an-apartment-livi.ogg", 0.0, 0.35, 10.4),          # a quiet room while Mom calls
    ("click/kenney-interface-click-001.ogg", wt(19) - 0.12, 0.6, 0.5),                  # answering
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(24), 0.45, 1.2),             # NOW
    ("click/kenney-interface-toggle-002.ogg", wt(33), 0.6, 0.5),                       # the key turns
    ("transition/fs-702773-swipe-wav.ogg", wt(49), 0.4, 0.8),                          # page in
    ("pop/kenney-interface-drop-001.ogg", wt(62), 0.5, 0.6),                           # the voice note
    ("impact/kenney-impact-impactsoft-heavy-000.ogg", wt(76) + 0.3, 0.5, 1.2),         # FOR SALE
    ("transition/fs-702773-swipe-wav.ogg", wt(81), 0.4, 0.8),                          # page in
    ("transition/fs-786514-swoosh-v2.ogg", wt(88) - 0.25, 0.35, 0.9),                  # the chart wipes in
    ("impact/fs-222517-dramatic-hit.ogg", wt(92), 0.3, 2.0),                           # SEVEN
    ("glitch/kenney-interface-glitch-002.ogg", wt(97) + 0.15, 0.4, 0.6),               # the lock breaks
    ("riser/fs-174363-rewind.ogg", wt(108) - 0.05, 0.55, 0.9),                         # the twist: record scratch
    ("ui-blip/kenney-digital-twotone1.ogg", wt(126), 0.35, 0.6),                       # the automated menu
    ("ui-blip/kenney-digital-pepsound1.ogg", wt(126) + 0.4, 0.3, 0.6),
    ("ding/fs-571513-soft-notifications-bell-ding-d.ogg", wt(129) - 0.1, 0.45, 1.4),   # the code arrives
    ("transition/fs-702773-swipe-wav.ogg", wt(130) - 0.2, 0.4, 0.8),
    ("impact/kenney-impact-impactpunch-heavy-001.ogg", wt(136) + 0.55, 0.55, 1.0),     # the deadbolt turns
    ("impact/kenney-impact-impactsoft-heavy-000.ogg", wt(143), 0.55, 1.2),             # THE CATCH
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(150), 0.35, 0.8),            # SELLS PROTECTION stamps
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(150) + 0.18, 0.3, 0.8),
    ("impact/kenney-impact-impactpunch-heavy-000.ogg", wt(150) + 0.36, 0.25, 0.8),
    ("click/kenney-interface-select-002.ogg", wt(162), 0.4, 0.5),                      # the two locks
    ("impact/kenney-impact-impactsoft-heavy-001.ogg", wt(167) - 0.1, 0.45, 1.0),       # the copy bounces off
    ("transition/fs-702773-swipe-wav.ogg", wt(168), 0.4, 0.8),
    ("click/kenney-interface-toggle-001.ogg", wt(182), 0.6, 0.5),                      # lock 2 closes
    ("transition/fs-702773-swipe-wav.ogg", wt(184) - 0.2, 0.4, 0.8),
    ("impact/kenney-impact-impactpunch-heavy-001.ogg", wt(187), 0.5, 1.0),             # REAL BANKS NEVER ASK
    ("ui-blip/kenney-digital-threetone1.ogg", wt(192), 0.35, 0.8),                     # calling your bank
    ("ambience/fs-329533-room-tone-in-an-apartment-livi.ogg", wt(197) - 0.2, 0.4, 4.8),   # the same room, the mirror
    ("ding/kenney-interface-confirmation-001.ogg", wt(206) + 0.25, 0.45, 1.2),         # MANGO ✓
    ("click/kenney-interface-tick-001.ogg", wt(220), 0.5, 0.4),                        # comment it
    ("ding/kenney-interface-confirmation-002.ogg", wt(215), 0.35, 1.0),                # recap: the attack
    ("ding/kenney-interface-confirmation-003.ogg", wt(218), 0.35, 1.0),                # recap: the locks
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
s = s.astype(np.float64) / 32768.0
if s.ndim == 1:
    s = np.stack([s, s], axis=1)
m = min(len(s), n)
both = layer[:m] + s[:m]
both /= max(1.0, np.max(np.abs(both)) / 0.9)
wavfile.write("work/sfx_all.wav", SR, (both * 32767).astype(np.int16))

os.makedirs("assets", exist_ok=True)
run(["python3", T + "mix.py", "assets/voice_raw.wav", "work/music.wav", "work/sfx_all.wav", "assets/mix.wav", str(DUR)])

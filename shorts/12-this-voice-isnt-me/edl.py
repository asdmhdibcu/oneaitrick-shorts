"""Edit decision list for Short #12 (9:16, 1080x1920), cut from the #12 video. Shared by build_edit.py, make_index.py
and make_audio.py. The material, the page crops and the logos are the video's (longform/this-voice-isnt-me).

Two cuts (cut_voice.py): the main Short (words.json, opens on "The voice you're hearing right now... isn't me") and the
Trial Reel (VARIANT=trial: words_trial.json, opens on T2, "If your mum called you right now..."). Everything after the
opening is the same; its anchors are written for the main cut and shifted for the trial.
Kinds as in the video: V, PAGE, GFX, END.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LF = os.path.normpath(os.path.join(HERE, "../../longform/this-voice-isnt-me"))
_spec = importlib.util.spec_from_file_location("long_edl", os.path.join(LF, "edl.py"))
LONG = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(LONG)   # the video's material table

MAT = LONG.MAT
H = 0.25
R = os.path.join(LF, "work/raw") + "/"
VARIANT = os.environ.get("VARIANT", "main")


def have(code):
    return os.path.exists(R + MAT[code][0])


def src(code):
    return R + MAT[code][0]


HEAD = {
    "main": [("k01", 0, "V", dict(m="G4", sin=0.3)),                         # The voice you're hearing right now... isn't me.
             ("k02", 8, "PAGE", dict(pg="e_tts", bd="G4", bdsin=5.0)),       # It IS me. It's a clone of my voice, made with AI.
             ("k03", 21, "V", dict(m="S9", sin=3.0))],                       # ...someone else can do it with yours.
    "trial": [("t01", 0, "GFX", dict(bd="S10", bdsin=4.0))],                 # If your mum called you right now... was it really her?
}
SHIFT = {"main": 0, "trial": -20}       # T2 is 18 words, the main opening 38
BODY = [
    ("k04", 38, "PAGE", dict(pg="s_three", bd="S9", bdsin=1.0)),            # Starling: three seconds of audio
    ("k05", 54, "V", dict(m="S19", sin=6.0)),                                # A birthday video. A voice note. A clip...
    ("k06", 65, "GFX", dict(bd="S9", bdsin=6.0)),                            # Then the phone rings. Your daughter. Your dad.
    ("k07", 76, "V", dict(m="S10", sin=3.0)),                                # Crying... They need money. NOW.
    ("k08", 88, "V", dict(m="S12", sin=0.5)),                                # And it's not just voices. Hong Kong, 2024.
    ("k09", 101, "V", dict(m="S11", sin=7.0)),                               # joined a video call with his CFO
    ("k10", 115, "PAGE", dict(pg="c_head", bd="S12", bdsin=0.5)),           # he sent about $25 million
    ("k11", 130, "PAGE", dict(pg="c_fake", bd="S11", bdsin=10.0)),          # everyone he saw was fake
    ("k12", 145, "V", dict(m="G5", sin=3.0)),                                # All deepfakes.
    ("k13", 147, "V", dict(m="S15", sin=2.5)),                               # Agree a safe phrase with your family. Tonight.
    ("k14", 155, "GFX", dict(bd="S15", bdsin=1.5)),                          # the safe-phrase card (the hidden word)
    ("k15", 175, "GFX", dict(bd="S10", bdsin=12.0)),                         # If "Mum" ever calls... hang up, call back
    ("k16", 203, "GFX", dict(bd="S15", bdsin=1.0)),                          # one word I never said out loud. Comment it.
    ("k17", 218, "END", dict()),                                             # Follow for more AI, explained like this.
]
PLAN = HEAD[VARIANT] + [(sid, k + SHIFT[VARIANT], kind, sp) for sid, k, kind, sp in BODY]
_HL = {"k02": [12, 17, 19], "k04": [50], "k10": [127], "k11": [135, 143]}
HL = {sid: [k + (SHIFT[VARIANT] if sid != "k02" else 0) for k in ks] for sid, ks in _HL.items()}

W = json.load(open(os.path.join(HERE, "words.json" if VARIANT == "main" else "words_trial.json")))
assert len(W) == (225 if VARIANT == "main" else 205), len(W)


def cut_at(k):
    if k == 0:
        return 0.0
    prev_end, start = W[k - 1]["end"], W[k]["start"]
    gap = start - prev_end
    t = start - (0.12 if gap > 0.3 else 0.05)
    return round(max(prev_end + 0.01, t), 2)


VOICE_END = W[-1]["end"]
DUR = round(VOICE_END + 2.4, 2)
SHOTS = []
for i, (sid, k, kind, sp) in enumerate(PLAN):
    t0 = cut_at(k)
    t1 = cut_at(PLAN[i + 1][1]) if i + 1 < len(PLAN) else DUR
    SHOTS.append((sid, t0, t1, kind, sp))


def wt(k):
    return W[k]["start"]


def we(k):
    return W[k]["end"]


def K(k):
    """A main-cut word index in this cut (for fx_short.js times after the opening)."""
    return k + SHIFT[VARIANT]


if __name__ == "__main__":
    print(f"{VARIANT}: {len(SHOTS)} shots, {DUR} s")
    for sid, t0, t1, kind, sp in SHOTS:
        need = [c for c in (sp.get("m"), sp.get("bd")) if c and not have(c)]
        print(f"{sid} {t0:6.2f}-{t1:6.2f} {t1 - t0:5.2f}s {kind:6s} {sp.get('m', sp.get('pg', ''))!s:12s}{'  NEEDED: ' + ', '.join(need) if need else ''}")

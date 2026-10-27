"""Edit decision list for Short #11 (9:16, 1080x1920), cut from the #11 video. Shared by build_edit.py, make_index.py
and make_audio.py. The material, the page crops and the logos are the video's (longform/ai-firms-your-data).

Each shot starts on a word of the Short's own voice (words.json, 220 words, cut_voice.py). Kinds as in the video:
  V      footage, full frame. spec: m, sin, rate, cx, cy (9:16 crop of a landscape source; vertical sources fill)
  PHONE  a phone screen recording as a card over its own blur. spec: m, sin | keys, pre
  PAGE   a highlighted crop of a real page over a moving blurred backdrop. spec: pg, bd, bdsin
  GFX    my graphics over a moving blurred backdrop. spec: bd, bdsin
  END    end card over the last shot, blurred
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LF = os.path.normpath(os.path.join(HERE, "../../longform/ai-firms-your-data"))
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("long_edl", os.path.join(LF, "edl.py"))
LONG = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(LONG)   # the video's material table

MAT = LONG.MAT
H = 0.25
R = os.path.join(LF, "work/raw") + "/"


def have(code):
    return os.path.exists(R + MAT[code][0])


def src(code):
    return R + MAT[code][0]


# (id, anchor word index in the Short, kind, spec)
PLAN = [
    # A: the hook, the result first
    ("k01", 0, "V", dict(m="S1", sin=0.5)),                          # Ten of the biggest AI companies... your data.
    ("k02", 16, "V", dict(m="S8", sin=1.0, cx=0.42)),               # Here, in the UK.
    ("k03", 20, "V", dict(m="G1", sin=0.0, rate=0.18)),              # didn't just wake up feeling generous
    ("k04", 29, "V", dict(m="G1", sin=0.6)),                         # A regulator came knocking.
    # B: the postcard
    ("k05", 33, "V", dict(m="G2", sin=0.6)),                         # Now imagine each one is a postcard.
    ("k06", 40, "V", dict(m="S4", sin=0.2)),                         # ...they're not sealed.
    ("k07", 49, "V", dict(m="S4", sin=3.2)),                         # Anyone who handles one can read it.
    ("k08", 56, "V", dict(m="G3", sin=0.3)),                         # a massive sorting office
    ("k09", 67, "PAGE", dict(pg="p5_public", bd="G3", bdsin=4.0)),   # reading billions of those postcards (Meta's page)
    # C: the big one
    ("k10", 77, "PAGE", dict(pg="r_social", bd="G3", bdsin=6.0)),    # Some of those postcards say really personal things.
    ("k11", 85, "V", dict(m="S5", sin=0.6, cx=0.45)),               # Your health.
    ("k12", 87, "V", dict(m="S6", sin=12.5)),                        # Your religion.
    ("k13", 89, "V", dict(m="S7", sin=0.2, cx=0.3)),                # How you vote.
    ("k14", 92, "PAGE", dict(pg="r_sensitive", bd="S10", bdsin=6.0)),    # unless a company can prove it hasn't got that kind of data...
    ("k14b", 109, "GFX", dict(bd="S10", bdsin=2.0)),                 # assume it has.
    # D: what they changed
    ("k15", 112, "PAGE", dict(pg="r_changed", bd="S1", bdsin=1.0)), # So what did they change?
    ("k16", 117, "GFX", dict(bd="S1", bdsin=2.5)),                  # ten names, ten logos
    ("k16b", 129, "GFX", dict(bd="S1", bdsin=6.0)),                 # have all made changes, or promised to.
    # E: the twist
    ("k17", 136, "GFX", dict(bd="S1", bdsin=5.0)),                  # But here's the bit nobody's really talking about.
    ("k18", 144, "V", dict(m="G4", sin=1.0, rate=1.4)),              # Once a postcard's been read and learned from...
    ("k19", 152, "PAGE", dict(pg="p5_deleted", bd="G4", bdsin=5.0)),    # you can't really un-read it.
    # F: one name's missing
    ("k20", 157, "GFX", dict(bd="S1", bdsin=4.0)),                  # Oh, and one name's missing.
    ("k20b", 162, "GFX", dict(bd="S1", bdsin=6.5)),                 # xAI, the company behind Grok.
    ("k21", 167, "PAGE", dict(pg="r_suspend", bd="S1", bdsin=6.0)), # until the ICO opened a formal investigation
    # G: one thing you can do
    ("k22", 181, "PHONE", dict(m="R1", keys=[[0.0, 0.12], [1.9, 0.62], [2.2, 0.72]])),      # Switch off training on your chats.
    ("k23", 187, "PHONE", dict(m="R1", keys=[[0.0, 9.1], [1.75, 11.0], [2.3, 12.2], [2.62, 12.6], [2.62, 13.85],
                                              [4.7, 14.8], [5.9, 16.2]])),                # In ChatGPT... "Improve the model for everyone"
    # H: the takeaway
    ("k24", 198, "V", dict(m="S4", sin=4.2)),                        # treat anything you post publicly like a postcard.
    ("k25", 206, "V", dict(m="G3", sin=6.0)),                        # Because somewhere, something might be reading it.
    ("k26", 213, "END", dict()),                                     # Follow for more AI, explained like this.
]
HL = {"k09": [68, 74], "k10": [82], "k14": [105, 97], "k15": [113, 114], "k19": [153], "k21": [178, 172]}


W = json.load(open(os.path.join(HERE, "words.json")))
assert len(W) == 220, len(W)


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


if __name__ == "__main__":
    print(f"{len(SHOTS)} shots, {DUR} s")
    for sid, t0, t1, kind, sp in SHOTS:
        need = [c for c in (sp.get("m"), sp.get("bd")) if c and not have(c)]
        print(f"{sid} {t0:6.2f}-{t1:6.2f} {t1 - t0:5.2f}s {kind:6s} {sp.get('m', sp.get('pg', ''))!s:12s}{'  NEEDED: ' + ', '.join(need) if need else ''}")

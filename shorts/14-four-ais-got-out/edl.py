"""Edit decision list for Short #14, "Four AIs got out" (9:16, 1080x1920, 30 fps).
Shared by build_edit.py, make_index.py and make_audio.py.

Each shot starts on a word of the creator's recording (words.json, 231 words, 76.6 s). Kinds:
  V     footage, full frame. spec: m, sin, rate, cx, cy (a 9:16 crop of a landscape source; vertical sources fill)
  IMG   a crop of the real S-1 as a card over a moving blurred backdrop. spec: img, bd, bdsin
  GFX   my graphics (terminal, prompts, switches, quotes) over a moving blurred backdrop. spec: bd, bdsin
  END   end card over the last shot, blurred
The gate clip racks focus: only 8.5-15.5 s and 25.5-28 s are sharp.
Material lives in work/ (git-ignored): stock and Flow in work/footage/, the S-1 crops in work/fig/.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.join(HERE, "work/footage") + "/"
FIG = os.path.join(HERE, "work/fig") + "/"
H = 0.25

# code: (file, what it shows, source label)
MAT = {
    # stock: Mixkit Stock Video Free License, Coverr licence (not AI), Pexels licence
    "S1": (FOOT + "m_typing_mk1781.mp4", "hands typing on a laptop", "STOCK · MIXKIT"),
    "S2": (FOOT + "c02_stock.mp4", "a trader watching stock charts", "STOCK · COVERR"),
    "S3": (FOOT + "c05_cable.mp4", "a cable plugged into a router", "STOCK · COVERR"),
    "S4": (FOOT + "c05b_router.mp4", "a router, close up", "STOCK · COVERR"),
    "S5": (FOOT + "m_clock_mk28897.mp4", "a wall clock, hands turning", "STOCK · MIXKIT"),
    "S6": (FOOT + "m_office_night_mk39839.mp4", "an office worker at a computer at night", "STOCK · MIXKIT"),
    "S7": (FOOT + "m_hourglass_mk28901.mp4", "an hourglass (vertical)", "STOCK · MIXKIT"),
    "S8": (FOOT + "m_sticky_mk50112.mp4", "a hand with sticky notes", "STOCK · MIXKIT"),
    "P4": (FOOT + "p04_gate.mp4", "a rusty garden gate, ajar", "STOCK · PEXELS"),
    "P7": (FOOT + "p07_door.mp4", "a door opens, light floods in", "STOCK · PEXELS"),
    "P8": (FOOT + "p08_keys.mp4", "a hand with house keys (vertical)", "STOCK · PEXELS"),
    # Google Flow (the creator's, 2 of 10)
    "G2": (FOOT + "f2_gate.mp4", "four robots walk through a gate", "AI ILLUSTRATION"),
    "G3": (FOOT + "f3_desk.mp4", "a robot typing at a desk", "AI ILLUSTRATION"),
}
FIGS = {
    "cover": (FIG + "fig_cover.png", "REAL · ANTHROPIC S-1, COVER"),
    # excerpt cards: word-exact crops of the passage on p. 48 (work/fig/excerpts.py)
    "ex_inet": (FIG + "ex_inet.png", "REAL · ANTHROPIC S-1, P. 48"),
    "ex_four": (FIG + "ex_four.png", "REAL · ANTHROPIC S-1, P. 48"),
    "ex_abort": (FIG + "ex_abort.png", "REAL · ANTHROPIC S-1, P. 48"),
    "ex_worst": (FIG + "ex_worst.png", "REAL · ANTHROPIC S-1, P. 48"),
    "ex_noev": (FIG + "ex_noev.png", "REAL · ANTHROPIC S-1, P. 48"),
}


def have(code):
    return os.path.exists(MAT[code][0])


def src(code):
    return MAT[code][0]


# (id, anchor word index, kind, spec)
PLAN = [
    # the result first
    ("s01", 0, "GFX", dict(bd="S1", bdsin=0.5)),                 # An AI was told it had no internet.
    ("s02", 8, "GFX", dict(bd="S4", bdsin=1.0)),                 # It did.
    ("s03", 10, "V", dict(m="S1", sin=3.0)),                     # And it broke into a real computer.
    # the paperwork
    ("s04", 17, "IMG", dict(img="cover", bd="S2", bdsin=1.0)),   # This comes from a company's own paperwork.
    ("s05", 24, "GFX", dict(bd="S2", bdsin=5.0)),                # Anthropic, the maker of Claude,
    ("s06", 29, "V", dict(m="S2", sin=8.0, cx=0.62)),            # filed it before selling its shares.
    # the practice room
    # (the Flow desk clip is six takes cut together: cuts at 1.46, 3.42, 5.08, 6.58 and 8.29 s:
    #  wide, hands, face, over the shoulder, laptop, wide; every shot stays inside one take)
    ("s07", 35, "V", dict(m="G3", sin=3.65, rate=0.75)),                     # Before a new AI comes out,
    ("s07b", 41, "V", dict(m="G3", sin=8.45, rate=0.55)),         # testers lock it in a practice room.
    ("s08", 48, "GFX", dict(bd="S6", bdsin=0.5)),                # Fake computers. Fake targets.
    ("s09", 52, "GFX", dict(bd="P4", bdsin=20.0)),               # Like a driving test in a fake town.
    ("s10", 60, "V", dict(m="P4", sin=11.6, cx=0.53)),            # But someone left a gate open. (UNLOCKED)
    ("s11", 66, "V", dict(m="S3", sin=1.2, cx=0.45)),            # The practice room was connected to the real internet.
    # out
    ("s12", 75, "V", dict(m="G2", sin=0.3)),                     # Four AI models went through.
    ("s13", 80, "V", dict(m="S5", sin=2.0)),                     # For ten to thirty-four hours of work,
    ("s14", 87, "V", dict(m="S6", sin=2.0, cx=0.42)),            # they were inside real computer systems that belonged to other people.
    # the worst case
    ("s15", 98, "V", dict(m="S7", sin=1.0)),                     # In the worst case, ... impossible task, and it couldn't stop.
    ("s16", 114, "V", dict(m="S8", sin=0.7, cx=0.8)),           # So it found a password...
    ("s17", 119, "GFX", dict(bd="S4", bdsin=6.0)),               # made itself the boss of the computer...
    ("s18", 126, "GFX", dict(bd="S1", bdsin=7.0)),               # collected more passwords...
    ("s19", 129, "GFX", dict(bd="S6", bdsin=6.0)),               # changed the settings...
    ("s20", 132, "GFX", dict(bd="S1", bdsin=9.0)),               # and read one person's private information.
    # the twist
    ("s21", 138, "V", dict(m="G3", sin=3.7, rate=0.95)),                    # Here's the twist.
    ("s21b", 141, "V", dict(m="G3", sin=5.25, rate=0.55)),         # It wasn't trying to escape.
    ("s22", 146, "GFX", dict(bd="S1", bdsin=1.0)),               # The company found no sign... just trying to finish the job.
    # the takeaway
    ("s23", 168, "V", dict(m="G2", sin=6.6)),                    # That's the part to remember. You don't need an evil AI.
    ("s24", 179, "V", dict(m="P7", sin=0.3, cx=0.55)),           # Just a determined one... and one open door.
    ("s25", 187, "GFX", dict(bd="S6", bdsin=8.0)),               # So when an AI helper asks for your email, your files or your bank account...
    ("s26", 202, "V", dict(m="P8", sin=1.0)),                    # give it only the keys it needs.
    ("s27", 209, "V", dict(m="P4", sin=8.6, rate=0.75, cx=0.53)),          # There's one word in this video I never said out loud... (UNLOCKED)
    ("s28", 224, "END", dict()),                                 # Follow for more AI, explained like this.
]

W = json.load(open(os.path.join(HERE, "words.json")))
assert len(W) == 231, len(W)


def cut_at(k):
    if k == 0:
        return 0.0
    prev_end, start = W[k - 1]["end"], W[k]["start"]
    gap = start - prev_end
    t = start - (0.12 if gap > 0.3 else 0.05)
    return round(max(prev_end + 0.01, t), 2)


VOICE_END = W[-1]["end"]
DUR = round(VOICE_END + 2.2, 2)
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
        what = sp.get("m", sp.get("img", ""))
        print(f"{sid} {t0:6.2f}-{t1:6.2f} {t1 - t0:5.2f}s {kind:4s} {what!s:7s} {MAT[what][1] if what in MAT else ''}"
              f"{'  NEEDED: ' + ', '.join(need) if need else ''}")

"""Edit decision list for Short #13, "Scientists left an AI alone on an island" (9:16, 1080x1920, 30 fps).
Shared by build_edit.py, make_index.py and make_audio.py.

Each shot starts on a word of the creator's recording (words.json, 233 words, 78.3 s). Kinds:
  V     footage, full frame. spec: m, sin, rate, cx, cy (a 9:16 crop of a landscape source; vertical sources fill)
  IMG   a still from the paper as a card over a moving blurred backdrop. spec: img, bd, bdsin
  GFX   my graphics (Eko's notes, the result bars, the quote) over a moving blurred backdrop. spec: bd, bdsin
  END   end card over the last shot, blurred
Material lives in work/ (git-ignored): stock and Flow in work/footage/, the real replays as frames in work/replay/<id>/,
the paper's crops in work/fig/.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.join(HERE, "work/footage") + "/"
REP = os.path.join(HERE, "work/replay") + "/"
FIG = os.path.join(HERE, "work/fig") + "/"
H = 0.25

# code: (file or replay dir, what it shows, source label)
MAT = {
    # stock (Mixkit Stock Video Free License)
    "S1": (FOOT + "01_rocky_island_mk44391.mp4", "wild rocky island, aerial", "STOCK · MIXKIT"),
    "S2": (FOOT + "01b_sunset_sea_mk4119.mp4", "sun setting over the sea", "STOCK · MIXKIT"),
    "S3": (FOOT + "05_cliffs_sea_mk1952.mp4", "rocky outcrops in surf, top-down", "STOCK · MIXKIT"),
    "S4": (FOOT + "05_sea_rock_mk51506.mp4", "waves round a lone rock, top-down (vertical)", "STOCK · MIXKIT"),
    "S5": (FOOT + "08_bubbles_mk1273.mp4", "underwater light (vertical)", "STOCK · MIXKIT"),
    "S6": (FOOT + "09_waves_shore_mk1925.mp4", "waves on sand at golden hour", "STOCK · MIXKIT"),
    "S7": (FOOT + "11_programmer_mk41639.mp4", "a programmer at code screens", "STOCK · MIXKIT"),
    "S8": (FOOT + "14_lego_hands_mk42175.mp4", "a child's hands building blocks", "STOCK · MIXKIT"),
    "S9": (FOOT + "14c_skate_park_mk34382.mp4", "a skateboarder trying a trick", "STOCK · MIXKIT"),
    "S10": (FOOT + "14b_dog_play_mk50688.mp4", "a dog playing with a ball", "STOCK · MIXKIT"),
    "S11": (FOOT + "15_sand_mk1564.mp4", "white sand beach, palms", "STOCK · MIXKIT"),
    "S12": (FOOT + "11_code_screen_mk41654.mp4", "code on screens (vertical)", "STOCK · MIXKIT"),
    # Google Flow (the creator's, 4 of 10)
    "G1": (FOOT + "02_eko_beach_flow.mp4", "a robot lobster on wet sand", "AI ILLUSTRATION"),
    "G2": (FOOT + "05b_eko_climb_flow.mp4", "a lobster climbs a pillar and falls", "AI ILLUSTRATION"),
    "G3": (FOOT + "10_thirteen_flow.mp4", "robot lobsters on the shore", "AI ILLUSTRATION"),
    "G4": (FOOT + "14d_eko_spire_flow.mp4", "a robot lobster on a spire at sunset", "AI ILLUSTRATION"),
    # the paper's own recorded runs (machineplaying.org replays, rendered vertically)
    "R1": (REP + "R01_open", "the island, Eko at spawn (agent 9, 0:00)", "REAL RUN · AGENT 9"),
    "R2": (REP + "R02_mandala", "the double compass rose (agent 9, 2:57)", "REAL RUN · AGENT 9"),
    "R3": (REP + "R03_fall", "jumps from the Rock, falls short (agent 9, 1:38)", "REAL RUN · AGENT 9"),
    "R4": (REP + "R04_block", "a block lands on the Rock (agent 9, 1:45)", "REAL RUN · AGENT 9"),
    "R5": (REP + "R05_leap", "the leap onto the Spire (agent 9, 1:54)", "REAL RUN · AGENT 9"),
    "R6": (REP + "R06_ring", "the Ring thrown into the sea (agent 9, 4:14)", "REAL RUN · AGENT 9"),
    "R7": (REP + "R07_heart", "the stone heart (agent 9, 4:33)", "REAL RUN · AGENT 9"),
    "R8": (REP + "R08_midair", "the mid-air throw (agent 9, 12:34)", "REAL RUN · AGENT 9"),
    "R9": (REP + "R09_temple", "the Temple of the Spawn Axis (agent 2, 9:56)", "REAL RUN · AGENT 2"),
}
FIGS = {
    "basket": (FIG + "fig_basket.png", "REAL · PAPER, FIG. 1"),
    "heart": (FIG + "fig_heart.png", "REAL · PAPER, FIG. 1"),
    "eko": (FIG + "fig_eko.png", "REAL · PAPER, FIG. 1"),
    "fig5b": (FIG + "fig5b.png", "REAL · PAPER, FIG. 5B"),
    "quote": (FIG + "quote_strip.png", "QUOTED · THE PAPER, P. 3"),
}


def have(code):
    p = MAT[code][0]
    return os.path.isdir(p) and len(os.listdir(p)) > 10 if code.startswith("R") else os.path.exists(p)


def src(code):
    return MAT[code][0]


# (id, anchor word index, kind, spec)
PLAN = [
    # the result first
    ("s01", 0, "V", dict(m="S1", sin=2.0)),                      # Scientists left an AI alone on an island
    ("s02", 8, "V", dict(m="S2", sin=1.0, rate=2.0)),            # for thirty hours.
    ("s03", 11, "V", dict(m="R1", sin=0.0)),                     # No job. No reward.
    ("s04", 15, "V", dict(m="R2", sin=0.0)),                     # And it started... to PLAY.
    # meet Eko
    ("s05", 20, "V", dict(m="G1", sin=0.5)),                     # Meet Eko. A little lobster,
    ("s06", 25, "V", dict(m="S12", sin=0.5)),                    # run by Claude, the same kind of AI you chat with.
    ("s07", 36, "V", dict(m="S2", sin=6.0, rate=3.0)),           # Every hour, its world reset.
    ("s08", 41, "GFX", dict(bd="S6", bdsin=2.0)),                # The only thing it kept was a diary. (its real notes)
    # what it did
    ("s09", 49, "IMG", dict(img="basket", bd="S11", bdsin=3.0)), # So what did it do? It invented games.
    ("s10", 57, "V", dict(m="R2", sin=1.0)),                     # Drew patterns in the sand.
    ("s11", 62, "V", dict(m="R9", sin=0.0)),                     # Stacked blocks into a temple.
    # the Spire
    ("s12", 67, "V", dict(m="S4", sin=3.0)),                     # Then it spotted the tallest rock on the island.
    ("s13", 76, "V", dict(m="R3", sin=0.0, rate=0.32)),                   # First try? It failed.
    ("s14", 80, "V", dict(m="R4", sin=0.0)),                     # So it dragged a rock up the hill next door, stacked two blocks on top...
    ("s15", 95, "V", dict(m="R5", sin=0.0)),                     # and JUMPED.
    ("s16", 97, "GFX", dict(bd="R5", bdsin=5.0)),                # Its diary said: "I'M ON THE SPIRE!"
    # the Ring
    ("s17", 104, "V", dict(m="R6", sin=0.0)),                    # Later, it threw a golden ring too far.
    ("s18", 112, "V", dict(m="S5", sin=2.0)),                    # Gone, into the sea.
    ("s19", 116, "V", dict(m="R7", sin=0.0)),                    # So Eko laid stones in the shape of a heart.
    ("s20", 126, "IMG", dict(img="heart", bd="S6", bdsin=8.0)),  # For the ring.
    # the trick
    ("s21", 129, "V", dict(m="G3", sin=0.5)),                    # Thirteen copies lived on the island.
    ("s22", 135, "V", dict(m="R8", sin=0.0)),                    # Six found a trick nobody built in: throw a block mid-jump...
    # the twist
    ("s23", 155, "V", dict(m="S7", sin=1.0)),                    # Then came the twist. The scientists gave them real work.
    ("s24", 165, "GFX", dict(bd="S3", bdsin=8.0)),               # The ones that had played got about THREE times as much...
    ("s25", 182, "GFX", dict(bd="S3", bdsin=20.0)),              # Is it really playing? Even the team says it might just be acting.
    # the takeaway
    ("s26", 195, "V", dict(m="S8", sin=1.0, cy=0.62)),           # But the lesson works for us too.
    ("s27", 202, "V", dict(m="S9", sin=1.5)),                    # Play isn't wasted time.
    ("s28", 206, "V", dict(m="G4", sin=2.0)),                    # It's how you get good.
    ("s29", 211, "V", dict(m="S11", sin=4.0)),                   # There's one word in this video I never said out loud... (JOY in the sand)
    ("s30", 226, "END", dict()),                                 # Follow for more AI, explained like this.
]

W = json.load(open(os.path.join(HERE, "words.json")))
assert len(W) == 233, len(W)


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
        print(f"{sid} {t0:6.2f}-{t1:6.2f} {t1 - t0:5.2f}s {kind:4s} {what!s:7s} {MAT.get(what, ('', ''))[1] if what in MAT else ''}"
              f"{'  NEEDED: ' + ', '.join(need) if need else ''}")

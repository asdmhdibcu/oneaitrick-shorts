"""Edit decision list for Short #16, "A thousand AIs, one proof" (9:16, 1080x1920, 30 fps).
Shared by build_edit.py, make_index.py and make_audio.py.

Each shot starts on a word of the creator's recording (words.json, 264 words, 95.2 s). Kinds:
  V      footage, full frame. spec: m, sin, rate, cx, cy, grade (a 9:16 crop of a landscape source; vertical sources fill)
  IMG    a real page or figure as a card over a moving blurred backdrop (bd), or over the dark grid (bd None).
         spec: img, bd, bdsin
  GFX    my graphics over a moving blurred backdrop (bd), or over the dark blueprint grid (bd None). spec: bd, bdsin
  END    end card over the last shot, blurred
No generated media (0 of 10 videos, 0 of 5 images). The thinking orbs are my own canvas drawing in the style of the
thinking-orbs library (library/thinking-orbs); the library itself is not run.
Material lives in work/ (git-ignored): work/footage/ (Pexels clips the creator downloaded), work/img/ (public-domain
scans), work/fig/ (slices of the three real pages, cut by crops.py).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.join(HERE, "work/footage") + "/"
IMGD = os.path.join(HERE, "work/img") + "/"
FIG = os.path.join(HERE, "work/fig") + "/"
H = 0.25

# code: (file, what it shows, source label)
MAT = {
    "B1": (FOOT + "v01_blueprint.mp4", "hands over a blueprint on a desk", "STOCK · PEXELS"),
    "B2": (FOOT + "v02_bricklaying.mp4", "hands laying bricks, close up", "STOCK · PEXELS"),
    "B3": (FOOT + "v03_inspector.mp4", "an inspector's gloved hands and clipboard", "STOCK · PEXELS"),
    "B4": (FOOT + "v04_timelapse.mp4", "a building site, time-lapse", "STOCK · PEXELS"),
    "B5": (FOOT + "v05_magnifier.mp4", "a desk with a blueprint and a magnifying glass", "STOCK · PEXELS"),
    "B6": (FOOT + "v06_drone.mp4", "a drone rising over a building site", "STOCK · PEXELS"),
    "B8": (FOOT + "v08_wall_vertical.mp4", "a finished brick wall on a roof (vertical)", "STOCK · PEXELS"),
}
# name: (file, source label)
FIGS = {
    "arith": (IMGD + "p01_arithmetica.jpg", "REAL · ARITHMETICA, 1670 EDITION · PUBLIC DOMAIN"),
    "fermat": (IMGD + "i01_fermat.jpg", "PIERRE DE FERMAT · PUBLIC DOMAIN"),
    "r_hero": (FIG + "r_hero.png", "REAL · ANTHROPIC RESEARCH, 4 SEP 2026"),
    "r_1637": (FIG + "r_1637.png", "REAL · ANTHROPIC RESEARCH, 4 SEP 2026"),
    "r_wiles": (FIG + "r_wiles.png", "REAL · ANTHROPIC RESEARCH, 4 SEP 2026"),
    "r_13m": (FIG + "r_13m.png", "REAL · ANTHROPIC RESEARCH, 4 SEP 2026"),
    "r_lead": (FIG + "r_lead.png", "REAL · ANTHROPIC RESEARCH, 4 SEP 2026"),
    "l_hero": (FIG + "l_hero.png", "REAL · ANTHROPIC, 9 NOV 2026"),
    "l_para": (FIG + "l_para.png", "REAL · ANTHROPIC, 9 NOV 2026"),
    "l_chart": (FIG + "l_chart.png", "REAL · ANTHROPIC, 9 NOV 2026"),
    "e_head": (FIG + "e_head.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
    "e_start": (FIG + "e_start.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
    "e_aside": (FIG + "e_aside.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
    "e_70min": (FIG + "e_70min.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
    "e_idle": (FIG + "e_idle.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
    "e_tree": (FIG + "e_tree.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
    "e_done": (FIG + "e_done.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
    "e_lesson": (FIG + "e_lesson.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
    "e_19": (FIG + "e_19.png", "REAL · CLAUDE.DEV, 9 NOV 2026"),
}


def have(code):
    return code is None or os.path.exists(MAT[code][0])


def src(code):
    return MAT[code][0]


# (id, anchor word index, kind, spec)
PLAN = [
    # the hook
    ("s01", 0, "GFX", dict(bd=None)),                               # These AIs said most of the job couldn't be done.
    ("s02", 10, "GFX", dict(bd=None)),                              # Then they DID it.
    # the everyday picture: a building, rebuilt brick by brick, with an inspector
    ("s03", 14, "V", dict(m="B1", sin=3.0, cx=0.47, cy=0.86, z=1.6)),      # Picture a famous building on paper.
    ("s04", 20, "V", dict(m="B2", sin=17.6, rate=0.8)),              # Now rebuild it brick by brick,
    ("s05", 26, "V", dict(m="B3", sin=1.0, cx=0.43, cy=0.74, z=1.4)),       # while a strict inspector checks EVERY brick.
    ("s06", 33, "GFX", dict(bd="B5", bdsin=3.0)),                   # The building is a famous math proof.
    ("s07", 40, "IMG", dict(img="arith", bd="B1", bdsin=9.0)),      # Fermat scribbled the rule in a book's margin in 1637.
    ("s08", 50, "GFX", dict(bd=None)),                              # Proving it took three hundred and fifty-eight YEARS.
    ("s09", 58, "GFX", dict(bd="B1", bdsin=13.0)),                  # But paper can hide mistakes.
    # the machine inspector
    ("s10", 63, "GFX", dict(bd=None)),                              # In a computer language called Lean,
    ("s11", 69, "GFX", dict(bd=None)),                              # the inspector is a machine,
    ("s12", 74, "GFX", dict(bd="B2", bdsin=30.0)),               # and nothing gets past it.
    # September
    ("s13", 79, "IMG", dict(img="r_hero", bd=None)),                # In September, Claude agents did it for the first time.
    ("s14", 89, "GFX", dict(bd=None)),                              # Thirteen MILLION lines,
    ("s15", 92, "GFX", dict(bd=None)),                              # a researcher guiding them,
    ("s16", 96, "GFX", dict(bd=None)),                              # eleven days.
    # this week
    ("s17", 98, "IMG", dict(img="l_hero", bd=None)),                # This week, Anthropic tried again with Claude Fable 5.2.
    ("s18", 107, "GFX", dict(bd=None)),                             # A THOUSAND copies,
    ("s19", 110, "GFX", dict(bd=None)),                             # no researcher.
    ("s20", 112, "GFX", dict(bd=None)),                             # One boss and nine hundred and ninety-nine helpers.
    # the twist
    ("s21", 120, "GFX", dict(bd=None)),                             # The twist? The helpers looked at sixty sections
    ("s22", 128, "GFX", dict(bd=None)),                             # and said forty-seven couldn't be done in time.
    ("s23", 136, "GFX", dict(bd=None)),                             # The boss set those aside and put nearly everyone on the other ten.
    ("s24", 149, "GFX", dict(bd=None)),                             # Done in about seventy minutes.
    ("s25", 154, "GFX", dict(bd=None)),                             # Then the boss wrote: "There is no reason to idle."
    ("s26", 164, "GFX", dict(bd="B4", bdsin=12.0)),                             # And sent the helpers back to the hard ones.
    ("s27", 173, "V", dict(m="B6", sin=0.3, rate=1.0)),             # Less than thirty hours later,
    ("s28", 178, "GFX", dict(bd=None)),                             # the whole proof passed the inspector.
    # the catch
    ("s29", 184, "V", dict(m="B5", sin=8.0, cx=0.62, cy=0.6, grade="warm")),  # The catch? Humans designed this building long ago,
    ("s30", 192, "GFX", dict(bd="B4", bdsin=4.0)),   # and the team had a head start: sixty checkpoints, a one-line map,
    ("s31", 204, "V", dict(m="B8", sin=6.5, cy=0.5)),               # forty-seven bricks already laid.
    # the lesson
    ("s32", 208, "GFX", dict(bd=None)),             # Anthropic's lesson? Agents give up on hard problems too early.
    ("s33", 218, "GFX", dict(bd=None)),                             # Even this boss got nineteen automatic reminders to keep going.
    ("s34", 228, "GFX", dict(bd="B2", bdsin=40.0)),                 # So when an AI says something can't be done, tell it to keep going.
    ("s35", 242, "GFX", dict(bd=None)),                             # There's one word in this video I never said out loud. Spotted it? Comment it.
    ("s36", 257, "END", dict()),                                    # Follow for more AI, explained like this.
]

W = json.load(open(os.path.join(HERE, "words.json")))
assert len(W) == 264, len(W)


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
        what = sp.get("m", sp.get("img", sp.get("bd", "")))
        print(f"{sid:5s} {t0:6.2f}-{t1:6.2f} {t1 - t0:5.2f}s {kind:5s} {what!s:12s}"
              f"{'  NEEDED: ' + ', '.join(need) if need else ''}")

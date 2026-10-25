"""Edit decision list for Short #10 "The invisible signature", shared by build_edit.py, make_index.py and make_audio.py.

Each shot starts on a word of the script (its index in work/script_plain.txt, 217 words), so the cuts follow the creator's
recording in words.json. A cut sits just before the anchor word (into the pause when there is one).
Kinds:
  V      footage. spec: src, sin (source second at the shot's start), rate, mode fill|vert|box, cx (0-1), pre crop,
         grade (build_edit.GRADES). box: pre = (x, y, w, h, top), a landscape band set full width at y=top over its own blur
  PAGE   a highlighted crop of OpenAI's help page (assets/pages, make_pages.py). spec: name, w
  GFX    my graphics over a moving, blurred backdrop clip. spec: bdv = (src, sin, rate, cx)
  END    end card over the last shot, blurred
"""
import json
import os

H = 0.25
R = "work/raw/"
# Flow (generated: 7 clips of the 10 allowed, no images)
G1 = R + "g1_uv.mp4"          # a UV torch reveals a glowing signature on a typed page
G2 = R + "g2_coin.mp4"        # a coin on an X-ray light box, a hidden weight inside
G3 = R + "g3_examiner.mp4"    # a document examiner with a magnifier under a green lamp
G4 = R + "g4_phone.mp4"       # a phone scans a handwritten card (3.3-5.5 s only: the typed screen after is nonsense text)
G5 = R + "g5_teacher.mp4"     # a teacher, a stack of essays, a laptop showing a padlock
G6 = R + "g6_stamp.mp4"       # a red stamp presses a handwritten essay and leaves no mark
G7 = R + "g7_student.mp4"     # a student types, then writes one line by pen
# Pexels (free licence)
LAPTOP = R + "px_14741625.mp4"    # hands on a laptop in the dark, the screen's glow
KEYS = R + "px_5119237.mp4"       # hands typing on a black keyboard
KEYSV = R + "px_5647324.mp4"      # fingers on white keys (vertical)
COIN = R + "px_13204789.mp4"      # a euro coin tumbling on black, slow motion
LOUPE = R + "px_6980534.mp4"      # a man reading a book through a magnifier
PEN = R + "px_7710490.mp4"        # a pen writing on paper
FLAG = R + "px_5903334.mp4"       # the EU flag against the sky
PARIS = R + "px_19538640.mp4"     # the Champs-Elysees, the Arc de Triomphe
PARIS2 = R + "px_14886910.mp4"    # a Paris boulevard
LONDON = R + "px_19787418.mp4"    # Big Ben and Westminster (vertical)
EUBLD = R + "px_14784771.mp4"     # an EU flag on a building

# (id, anchor word index, kind, spec)
PLAN = [
    # hook
    ("s01", 0, "V", dict(src=LAPTOP, sin=1.0, mode="fill", cx=0.42, grade="inkb")),              # claim title, signature
    ("s02", 9, "V", dict(src=G1, sin=0.6, mode="fill", grade="flow")),                           # UV reveal
    # the everyday picture
    ("s03", 16, "V", dict(src=KEYS, sin=2.0, mode="fill", cx=0.55, grade="ink")),
    ("s04", 22, "V", dict(src=KEYSV, sin=4.0, mode="vert", grade="ink")),                        # word slots flip
    ("s05", 31, "V", dict(src=COIN, sin=0.6, mode="box", pre=(0, 0, 1920, 1080, 440), grade="ink")),
    ("s06", 42, "V", dict(src=G2, sin=1.4, mode="fill", grade="flow")),                          # the loaded coin
    ("s07", 49, "V", dict(src=LOUPE, sin=11.0, mode="fill", cx=0.52, grade="ink")),              # one word
    ("s08", 53, "GFX", dict(bdv=(LAPTOP, 5.0, 1.0, 0.42))),                                      # hundreds of words
    ("s09", 62, "V", dict(src=PEN, sin=1.0, mode="fill", cx=0.42, grade="ink")),                 # a signature
    # evidence
    ("s10", 65, "PAGE", dict(name="r1_hidden", w=960, bdv=(KEYS, 8.0, 1.0, 0.5))),
    ("s11", 68, "GFX", dict(bdv=(KEYS, 12.0, 1.0, 0.5))),                                        # copy, paste, screenshot
    ("s12", 77, "GFX", dict(bdv=(KEYS, 15.0, 1.0, 0.5))),                                        # the signature IS the words
    ("s13", 83, "V", dict(src=FLAG, sin=1.0, mode="fill", cx=0.45, grade="day")),
    ("s14", 94, "V", dict(src=PARIS, sin=10.0, mode="fill", cx=0.26, grade="day")),
    ("s15", 99, "V", dict(src=LONDON, sin=0.5, mode="vert", grade="day")),
    ("s16", 103, "GFX", dict(bdv=(LAPTOP, 9.0, 1.0, 0.42))),                                     # Claude's page: worldwide
    ("s17", 111, "GFX", dict(bdv=(LAPTOP, 11.0, 1.0, 0.42))),                                    # the globe
    ("s18", 115, "V", dict(src=G3, sin=1.2, mode="fill", grade="flow")),                         # so does it work?
    ("s19", 119, "PAGE", dict(name="r1_rates", w=960, bdv=(LOUPE, 3.0, 1.0, 0.5))),
    ("s20", 126, "GFX", dict(bdv=(LOUPE, 6.0, 1.0, 0.5))),                                       # OpenAI's chart; the scratch
    # twist
    ("s21", 140, "GFX", dict(bdv=(LAPTOP, 3.0, 1.0, 0.42))),                                     # Claude's page: translate
    ("s22", 147, "V", dict(src=G4, sin=3.3, rate=0.6, mode="fill", grade="flow")),              # your own words
    ("s23", 155, "GFX", dict(bdv=(LAPTOP, 7.0, 1.0, 0.42))),                                     # not fully conclusive
    ("s24", 166, "V", dict(src=G5, sin=1.0, mode="fill", grade="flow")),
    ("s25", 172, "PAGE", dict(name="r1_student", w=960, bdv=(G5, 6.0, 1.0, 0.5))),
    ("s26", 178, "V", dict(src=G6, sin=0.5, mode="fill", grade="flow")),                         # CHEATED? won't stick
    ("s27", 185, "V", dict(src=G6, sin=4.8, mode="fill", grade="flow")),                         # HUMAN? won't stick
    # takeaway
    ("s28", 194, "V", dict(src=G7, sin=2.2, mode="fill", grade="flow")),                         # just say so
    ("s29", 203, "V", dict(src=LAPTOP, sin=1.0, mode="fill", cx=0.42, grade="inkb")),             # the loop to frame one
    ("s30", 210, "END", dict()),
]


def _words():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.json")
    return json.load(open(p))


W = _words()
assert len(W) == 217, len(W)


def cut_at(k):
    """Just before word k: into the pause when there is one, never into the previous word."""
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
    """Start time of script word k (for moments in the animation and the sound)."""
    return W[k]["start"]


def we(k):
    return W[k]["end"]

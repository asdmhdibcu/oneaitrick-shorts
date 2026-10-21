"""Edit decision list for Short #6, shared by build_edit.py and make_index.py.

Each shot: (id, out start, out end, kind, spec). Out times are cut on the word timings in words.json.
Kinds:
  V      footage. spec: src, sin (source second shown at out start), rate, mode fill|tall|native, cx (0-1), flip, win
         fill  = 9:16 crop of 4K/vertical footage, full bleed
         tall  = 3:4 crop of 1080p landscape footage over its own blurred 9:16 fill (sharper than a 9:16 crop)
         win   = (a, b) source shot boundaries; the rate drops just enough for the shot and its handles to fit
  STILL  a still photo or a frozen frame, camera moves in make_index.py. spec: img or (src, at, mode, cx)
  PAGE   a band of Anthropic's post, rebuilt clean from the phone recording (stitch_page.py). spec: y0, y1, w
  IMG    a phone screenshot. spec: file, crop (x, y, w, h), w
  FIG    a figure from the preprint, re-rendered from the PDF at 600 dpi. spec: page, box at 300 dpi, w
  DNA    the post's raw-DNA figure (stab_dna.py frames) with the scan rebuilt
  GRID   950 agents (animation)
  END    end card
Cards (PAGE, IMG, FIG, DNA) sit on a blurred backdrop: spec "bd" = ("last", shot id) or (src, second).
"""
H = 0.25  # handle on each side of a shot, for transitions
DUR = 85.5

RAW = "work/raw/"
LAB = RAW + "anthropic_lab_video.mp4"
GL = RAW + "px_18969594_large_library.mp4"      # grand library tilt-up, 1920x1080 60 fps
BOOKS = RAW + "px_1580502_books.mp4"            # bookshelves, 4K
HALL = RAW + "px_854417_inside_library.mp4"     # library corridor, 4K
STACKS = RAW + "px_15983292.mp4"                # compact stacks walk, vertical 1080x1920
SWITCH = RAW + "px_1085656.mp4"                 # network switch lights, 4K
RACK = RAW + "px_7140928_cpu.mp4"               # server rack, 4K
G1 = RAW + "flow_a.mp4"                         # Veo: lights swarm the library
G2 = RAW + "flow_b.mp4"                         # Veo: one light, one glowing book

SHOTS = [
    # hook
    ("s01", 0.00, 1.90, "V", dict(src=G1, sin=0.30, rate=1.0, mode="native", gen=True)),
    ("s02", 1.90, 2.50, "V", dict(src=SWITCH, sin=5.0, rate=1.0, mode="fill", cx=0.55)),
    ("s03", 2.50, 4.58, "V", dict(src=RACK, sin=1.0, rate=1.0, mode="fill", cx=0.5)),
    ("s04", 4.58, 5.82, "IMG", dict(file="anthropic_x.jpg", crop=(0, 40, 1320, 600), w=1000, bd=("last", "s03"))),
    ("s05", 5.82, 7.78, "STILL", dict(img="work/img/phage_tem.jpg")),
    # the library
    ("s06", 7.78, 10.36, "V", dict(src=GL, sin=4.0, rate=1.0, mode="tall", cx=0.5)),
    ("s07", 10.36, 12.76, "V", dict(src=BOOKS, sin=16.3, rate=1.0, mode="fill", cx=0.5)),
    ("s08", 12.76, 14.22, "V", dict(src=STACKS, sin=3.0, rate=1.0, mode="native")),
    ("s09", 14.22, 16.80, "STILL", dict(frame=(GL, 1.2, "tall", 0.5))),
    # the search party
    ("s10", 16.80, 19.15, "PAGE", dict(y0=548, y1=1680, w=860, bd=("last", "s09"))),
    ("s11", 19.15, 22.40, "GRID", dict(bd=(RACK, 6.0))),
    ("s12a", 22.40, 23.05, "V", dict(src=HALL, sin=8.0, rate=1.0, mode="fill", cx=0.62)),
    ("s12b", 23.05, 23.70, "V", dict(src=BOOKS, sin=23.0, rate=1.0, mode="fill", cx=0.5)),
    ("s12c", 23.70, 24.35, "V", dict(src=STACKS, sin=8.4, rate=1.0, mode="native")),
    ("s12d", 24.35, 25.00, "V", dict(src=BOOKS, sin=28.6, rate=1.0, mode="fill", cx=0.5)),
    ("s12e", 25.00, 26.30, "V", dict(src=G1, sin=4.4, rate=1.0, mode="native", gen=True)),
    ("s13", 26.30, 29.85, "PAGE", dict(y0=15150, y1=15610, w=1000, bd=("last", "s12e"))),
    # the find
    ("s14", 29.85, 32.35, "V", dict(src=G2, sin=3.9, rate=1.0, mode="native", gen=True)),
    ("s15", 32.35, 34.48, "PAGE", dict(y0=15680, y1=16170, w=1000, bd=("last", "s14"))),
    ("s16", 34.48, 36.95, "DNA", dict(bd=("last", "s14"))),
    ("s17", 36.95, 39.55, "FIG", dict(page=4, box=(1525, 1619, 750, 636), w=860, bd=("last", "s14"))),
    # why it matters
    ("s18a", 39.55, 40.45, "IMG", dict(file="techcrunch.png", crop=(0, 1740, 1250, 700), w=1000, bd=(LAB, 46.5))),
    ("s18b", 40.45, 41.45, "IMG", dict(file="aljazeera.jpg", crop=(0, 320, 1320, 690), w=1000, bd=(LAB, 46.5))),
    ("s19", 41.45, 43.22, "FIG", dict(page=7, box=(1313, 278, 1030, 500), w=1000, bd=(LAB, 46.5))),
    ("s20", 43.22, 45.70, "IMG", dict(file="nobel.jpg", crop=(0, 0, 1320, 1560), w=800, bd=(LAB, 46.5))),
    # the lab
    ("s21a", 45.70, 47.00, "V", dict(src=LAB, sin=16.95, mode="tall", cx=0.45, win=(16.75, 18.33))),
    ("s21b", 47.00, 48.22, "V", dict(src=LAB, sin=27.95, mode="tall", cx=0.45, win=(27.65, 30.02))),
    ("s22", 48.22, 50.15, "V", dict(src=LAB, sin=36.70, mode="tall", cx=0.45, win=(36.48, 38.65))),
    ("s23", 50.15, 53.45, "FIG", dict(page=9, box=(227, 642, 1180, 448), w=1040, bd=("last", "s22"))),
    # the mystery
    ("s24", 53.45, 55.52, "PAGE", dict(y0=5400, y1=5840, w=1000, bd=("last", "s22"))),
    ("s25", 55.52, 60.85, "STILL", dict(img="work/img/phage_tem.jpg")),
    ("s26", 60.85, 63.45, "PAGE", dict(y0=6866, y1=7730, w=1000, bd=("img", "phage_tem.jpg"))),
    ("s27", 63.45, 67.15, "IMG", dict(file="decrypt.jpg", crop=(0, 560, 1320, 720), w=1000, bd=("img", "phage_tem.jpg"))),
    # the twist
    ("s28a", 67.15, 68.00, "V", dict(src=LAB, sin=61.25, mode="tall", cx=0.4, win=(61.02, 62.15))),
    ("s28b", 68.00, 69.15, "V", dict(src=LAB, sin=57.95, mode="tall", cx=0.6, win=(57.77, 59.10))),
    ("s29", 69.15, 71.15, "PAGE", dict(y0=7866, y1=8500, w=1000, bd=("last", "s28b"))),
    ("s30", 71.15, 72.45, "V", dict(src=LAB, sin=33.70, mode="tall", cx=0.5, win=(33.52, 34.86))),
    ("s31a", 72.45, 73.05, "V", dict(src=SWITCH, sin=14.0, rate=1.0, mode="fill", cx=0.45)),
    ("s31b", 73.05, 73.55, "V", dict(src=RACK, sin=5.0, rate=1.0, mode="fill", cx=0.5)),
    ("s31c", 73.55, 74.70, "V", dict(src=G1, sin=6.3, rate=1.0, mode="native", gen=True)),
    # the ending
    ("s32", 74.70, 76.15, "V", dict(src=LAB, sin=6.35, mode="tall", cx=0.66, win=(6.10, 8.02))),
    ("s33", 76.15, 78.10, "V", dict(src=LAB, sin=67.25, mode="tall", cx=0.45, win=(67.02, 69.10))),
    ("s34", 78.10, 81.00, "V", dict(src=G1, sin=2.4, rate=1.0, mode="native", gen=True, flip=True)),
    ("s35", 81.00, DUR, "END", dict()),
]

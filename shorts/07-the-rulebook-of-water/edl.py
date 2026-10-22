"""Edit decision list for Short #7 "The rulebook of water", shared by build_edit.py and make_index.py.

Each shot: (id, out start, out end, kind, spec). Out times are cut on the word timings in words.json.
Kinds:
  V      footage. spec: src, sin (source second at out start), rate, mode fill|tall|native|vert, cx (0-1),
         win (a, b) source shot bounds, rev (play backwards), ramp [(out_offset, rate), ...] speed ramp,
         freeze (out time where the picture stops; a still is exported for the overlay)
  SIM    my own renders in work/sim (1080x1920): swirl = a real Navier-Stokes simulation, vortex, swarm
  PAGE   a band of a web page rebuilt from the creator's phone recording (stitch_page.py). spec: page, y0, y1, w
  PDF    a crop of a PDF page at 300 dpi. spec: doc (oa|cl), page, box (x, y, w, h), w
  IMG    a screenshot crop. spec: file, crop (x, y, w, h), w
  CUT    footage with a word placed behind the person (cut-out masks from rembg)
  SPLIT  two clips stacked (top/bottom)
  CARDS  graphics only, over a blurred backdrop
  END    end card
Cards sit on a blurred backdrop: spec "bd" = ("last", shot id) or (src, second).
"""
H = 0.25
DUR = 133.0

R = "work/raw/"
MONEY = R + "938d84f5-12245077-hd_1920_1080_30fps.mp4"
FAN = R + "f129e014-5466773-hd_1920_1080_25fps.mp4"
GLASS = R + "16821235_3840_2160_50fps_4.mp4"           # hourglass, red sand
DRIP = R + "beb15cb0-10811027-uhd_2560_1440_30fps.mp4"  # dripping tap close-up
TAP = R + "727adca4-2236003-hd_1920_1080_24fps.mp4"     # running outdoor tap
BOOK = R + "10419504-hd_1920_1080_25fps_4.mp4"          # old handwritten book
INK = R + "6069199-uhd_3840_2160_30fps_3.mp4"           # colour ink on black
INKV = R + "1be4622e-7565898-hd_1080_1920_25fps.mp4"    # black and orange ink, vertical
SMOKE = R + "99a4fb9c-9694227-hd_1920_1080_25fps.mp4"
STORM = R + "f9c5036f-11489658-hd_1920_1080_30fps.mp4"
WING = R + "13015509-uhd_2160_3840_30fps_4.mp4"         # vertical
BLOOD = R + "314eaaad-14920949_1920_1080_30fps.mp4"
BOARD_M = R + "47e52828-3196291-uhd_3840_2160_25fps.mp4"  # man writing equations (2560x1440)
BOARD_W = R + "5c7883aa-8197214-hd_1920_1080_25fps.mp4"   # woman at a green board
WHIRL = R + "9667989-hd_1920_1080_25fps_4.mp4"
RACK = "../06-the-machine-nobody-noticed/work/raw/px_7140928_cpu.mp4"
STIR = R + "eb73af7a-6831306-uhd_3840_2160_30fps.mp4"     # spoon stirring coffee, 4K
STIR2 = R + "bc1db3d0-946148-hd_1920_1080_30fps.mp4"      # stirring a mug by a window
REF = R + "3ebe44b0-6767263-uhd_2160_4096_25fps.mp4"      # basketball referee, vertical
NASA = R + "24605ca5-GSFC_20170920_GPM_m12723_JoseMarialarge.mp4"
SIM = "work/sim/"

SHOTS = [
    # hook
    ("s01", 0.00, 1.34, "SIM", dict(src=SIM + "vortex.mp4", sin=7.4)),
    ("s02", 1.34, 3.20, "V", dict(src=MONEY, sin=5.0, mode="fill", cx=0.5)),
    ("s03", 3.20, 4.97, "V", dict(src=GLASS, sin=1.0, mode="fill", cx=0.5, rate=2.0)),
    ("s04", 4.97, 7.22, "V", dict(src=FAN, sin=1.0, mode="fill", cx=0.5, freeze=6.54)),
    # the rulebook
    ("s05", 7.22, 8.77, "V", dict(src=DRIP, sin=2.25, mode="fill", cx=0.62)),
    ("s06", 8.77, 11.40, "V", dict(src=BOOK, sin=12.0, mode="fill", cx=0.5)),
    ("s07", 11.40, 12.57, "V", dict(src=INK, sin=8.0, mode="fill", cx=0.45)),
    ("s08", 12.57, 13.67, "V", dict(src=SMOKE, sin=5.0, mode="fill", cx=0.5)),
    ("s09", 13.67, 14.16, "V", dict(src=STORM, sin=6.0, mode="fill", cx=0.5)),
    ("s10", 14.16, 15.20, "V", dict(src=WING, sin=5.0, mode="vert")),
    ("s11", 15.20, 17.07, "V", dict(src=BLOOD, sin=2.0, mode="fill", cx=0.5)),
    ("s12", 17.07, 20.15, "CUT", dict(src=BOARD_M, sin=3.0, mode="fill", cx=0.58)),
    ("s13", 20.15, 22.50, "PAGE", dict(page="f13", y0=0, y1=1300, w=1000, bd=("last", "s12"))),
    ("s14", 22.50, 24.49, "V", dict(src=BOOK, sin=40.0, mode="fill", cx=0.5)),
    ("s15", 24.49, 27.91, "V", dict(src=WHIRL, sin=1.0, mode="fill", cx=0.5, ramp=[(0, 0.7), (2.4, 1.0), (3.0, 1.8)])),
    ("s16", 27.91, 31.08, "SIM", dict(src=SIM + "swirl.mp4", sin=3.4)),
    # the prize
    ("s17", 31.08, 33.39, "PAGE", dict(page="clay_mill", y0=1380, y1=2440, w=1000, bd=("last", "s16"))),
    ("s18", 33.39, 35.41, "PAGE", dict(page="f18", y0=0, y1=640, w=1000, bd=("last", "s16"))),
    ("s19", 35.41, 36.88, "PDF", dict(doc="oa", page=5, box=(230, 90, 2020, 610), w=1000, bd=(RACK, 2.0))),
    ("s20", 36.88, 39.48, "SIM", dict(src=SIM + "swarm.mp4", sin=0.9)),
    ("s21", 39.48, 41.10, "PDF", dict(doc="oa", page=5, box=(230, 2830, 2020, 300), w=1000, bd=("last", "s20"))),
    ("s22", 41.10, 43.16, "PDF", dict(doc="oa", page=2, box=(230, 2400, 2020, 720), w=1000, bd=("last", "s20"))),
    # the collapse
    ("s23", 43.16, 45.14, "PDF", dict(doc="oa", page=3, box=(230, 200, 2020, 780), w=1000, bd=("last", "s20"))),
    ("s24", 45.14, 47.67, "PDF", dict(doc="oa", page=3, box=(420, 1150, 1830, 1950), w=860, bd=("last", "s20"))),
    ("s25", 47.67, 53.01, "SIM", dict(src=SIM + "vortex.mp4", sin=4.3)),
    # the tap
    ("s26", 53.01, 54.88, "V", dict(src=TAP, sin=4.0, mode="fill", cx=0.42)),
    ("s27", 54.88, 55.48, "V", dict(src=DRIP, sin=13.45, mode="fill", cx=0.62)),
    ("s28", 55.48, 57.51, "V", dict(src=DRIP, sin=14.05, mode="fill", cx=0.62, rate=0.5)),
    ("s29", 57.51, 59.67, "V", dict(src=BOARD_W, sin=4.0, mode="fill", cx=0.55)),
    ("s30", 59.67, 61.15, "FREEZE", dict(of="s29")),
    # the catch
    ("s31", 61.15, 64.25, "PDF", dict(doc="oa", page=2, box=(230, 2600, 2020, 520), w=1000, bd=(STIR, 4.0))),
    ("s32", 64.25, 68.55, "V", dict(src=STIR, sin=3.0, mode="fill", cx=0.5)),
    ("s33", 68.55, 70.28, "PDF", dict(doc="cl", page=2, box=(480, 1200, 1600, 960), w=1000, bd=(STIR, 4.0))),
    ("s34", 70.28, 72.17, "SPLIT", dict(top=dict(src=STIR2, sin=3.0, cx=0.35), bot=dict(src=INK, sin=20.0, cx=0.5))),
    ("s35", 72.17, 74.50, "PDF", dict(doc="cl", page=2, box=(480, 1200, 1600, 960), w=1000, bd=(INK, 22.0))),
    # the referee
    ("s36", 74.50, 76.91, "PAGE", dict(page="gh_files", y0=1200, y1=10027, w=1000, view=900, bd=(INK, 22.0))),
    ("s37", 76.91, 79.02, "PAGE", dict(page="f37", y0=0, y1=1300, w=1000, bd=(INK, 22.0))),
    ("s38", 79.02, 83.42, "PAGE", dict(page="gh_lean68", y0=0, y1=2300, w=1000, view=1000, bd=(INK, 22.0))),
    ("s39", 83.42, 84.69, "V", dict(src=REF, sin=1.75, mode="vert")),
    ("s40", 84.69, 86.59, "V", dict(src=REF, sin=3.9, mode="vert")),
    ("s41", 86.59, 88.28, "PAIR", dict(a=("pdf", "cl", 2, (500, 1668, 1100, 84)), b=("page", "gh_lean76", (40, 1270, 960, 330)), w=1000, bd=("last", "s40"))),
    ("s42", 88.28, 92.17, "V", dict(src=BOARD_M, sin=14.0, mode="fill", cx=0.70)),
    # the pushback
    ("s43", 92.17, 94.61, "IMG", dict(file="sciam.jpg", crop=(0, 420, 1320, 600), w=1000, bd=("last", "s42"))),
    ("s44", 94.61, 96.99, "PAGE", dict(page="f44", y0=0, y1=700, w=1000, bd=("last", "s42"))),
    ("s45", 96.99, 98.97, "PDF", dict(doc="cl", page=1, box=(300, 560, 1900, 1050), w=1000, bd=("last", "s42"))),
    ("s46", 98.97, 103.58, "PAGE", dict(page="f46", y0=0, y1=520, w=1000, bd=("last", "s42"))),
    # the money
    ("s47", 103.58, 104.92, "V", dict(src=MONEY, sin=20.0, mode="fill", cx=0.5)),
    ("s48", 104.92, 107.47, "PAGE", dict(page="f48", y0=0, y1=680, w=1000, bd=("last", "s47"))),
    ("s49", 107.47, 109.98, "PDF", dict(doc="oa", page=7, box=(230, 110, 2020, 560), w=1000, bd=("last", "s47"))),
    ("s50", 109.98, 113.54, "PAGE", dict(page="clay_poincare", y0=0, y1=970, w=1000, bd=("last", "s47"))),
    ("s51", 113.54, 115.70, "V", dict(src=FAN, sin=6.6, mode="fill", cx=0.5, rev=True)),
    ("s52", 115.70, 117.74, "PAGE", dict(page="f52", y0=0, y1=1160, w=1000, bd=(GLASS, 9.0))),
    ("s53", 117.74, 119.64, "V", dict(src=GLASS, sin=9.0, mode="fill", cx=0.5, rate=0.5)),
    # the ending
    ("s54", 119.64, 123.66, "V", dict(src=BOOK, sin=60.0, mode="fill", cx=0.5, blend=dict(src=SIM + "swirl.mp4", sin=1.0))),
    ("s55", 123.66, 126.10, "V", dict(src=NASA, sin=34.0, mode="tall", cx=0.5)),
    ("s56", 126.10, 128.53, "SIM", dict(src=SIM + "swarm.mp4", sin=3.4)),
    ("s57", 128.53, DUR, "END", dict()),
]

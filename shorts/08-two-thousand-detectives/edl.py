"""Edit decision list for Short #8 "Two thousand detectives", shared by build_edit.py and make_index.py.

Each shot: (id, out start, out end, kind, spec). Out times are cut on the word timings in words.json.
Kinds:
  V      footage. spec: src, sin (source second at out start), rate, mode fill|vert|native, cx (0-1), pre (w, h, x, y) crop
         applied first (Flow clips come letterboxed), rev (play backwards), ramp [(out_offset, rate), ...], freeze (out time)
  REC    the OpenAI x PerturbAI video, cut from the creator's phone recording (HDR, 120 fps): its 16:9 band is placed
         full width on black. spec: sin
  SIM    my 3D renders in work/sim (render3d.py)
  PDF    a crop of a PDF page at 300 dpi. spec: doc (oa|ag|at), page, box (x, y, w, h), w
  IMG    a crop of an image in work/img (figure images at 600 ppi, phone frames). spec: file, crop (x, y, w, h), w
  GFX    my own animated graphics (built in the composition) over a blurred backdrop
  END    end card
Cards and graphics sit on a blurred backdrop: spec "bd" = ("last", shot id) or (src, second).
"""
H = 0.25
DUR = 122.5

R = "work/raw/"
R6 = "../06-the-machine-nobody-noticed/work/raw/"
REC1 = R + "ScreenRecording_10-22-2026_19-14-33_1.mp4"  # the OpenAI x PerturbAI video, then the OpenAI post
# Flow clips (generated: 10 used, the cap). Letterboxed ones carry their picture box in "pre".
G1 = R + "flow_19a4a162.mp4"           # lanterns rising up an avenue
G1B = R + "flow_fd3ffeca.mp4"          # lanterns from a rooftop
G2 = R + "flow_f46135a0.mp4"           # through a window into glowing wires
G3 = R + "flow_a55f7dea.mp4"           # lorries on a glowing neuron track
G4 = R + "flow_ea6b63b4.mp4"           # case-file wall, push in to a glowing card
G5 = R + "flow_35a9f324.mp4"           # lorries in the rain, a lit town
G5B = R + "flow_09d15c38.mp4"          # terraced street, chimneys smoking
G6 = R + "flow_f2f22f7a.mp4"           # golden cell body and its fibre
G7 = R + "flow_7b387745.mp4"           # one lit window, pull back to the city
G7B = R + "flow_d6c16140.mp4"          # lit windows, tilt to the skyline
P_G1B, P_G4, P_G5B, P_G6, P_G7 = (720, 1082, 0, 100), (720, 1044, 0, 118), (720, 1056, 0, 112), (720, 1262, 0, 10), (720, 1052, 0, 114)
# stock (Pexels)
CITY = R + "7068548-uhd_2160_3840_24fps.mp4"
WINDOWS = R + "9431644-hd_1920_1080_25fps.mp4"
WIRES = R + "6079420-uhd_3840_2160_24fps.mp4"
DETECTIVE = R + "7319206-uhd_2160_4096_25fps.mp4"
BOARD = R + "8369883-uhd_4096_2160_25fps.mp4"
STRINGS = R + "8369880-uhd_2160_4096_25fps.mp4"
TYPE = R + "6980931-uhd_3840_2160_25fps.mp4"
TIMELAPSE = R + "11437954-hd_1920_1080_25fps.mp4"
BREAD = R + "7405932-uhd_3840_2160_24fps.mp4"
MOUSE = R + "7235793-uhd_2160_3224_30fps.mp4"
AERIAL = R + "13398597_2160_3840_30fps.mp4"
LIBRARY = R6 + "px_854417_inside_library.mp4"
BIGLIB = R6 + "px_18969594_large_library.mp4"
PIPETTE = R6 + "px_8540611_pipette.mp4"
LAB = R6 + "px_8534547_scientists.mp4"
SIM = "work/sim/"

SHOTS = [
    # hook
    ("s01", 0.00, 2.39, "V", dict(src=G1, sin=1.0, mode="fill")),
    ("s02", 2.39, 5.07, "REC", dict(sin=1.9)),
    ("s03", 5.07, 6.88, "V", dict(src=TIMELAPSE, sin=2.0, mode="fill", cx=0.5)),
    ("s04", 6.88, 8.42, "V", dict(src=DETECTIVE, sin=9.0, mode="vert")),
    ("s05", 8.42, 10.17, "GFX", dict(bd=("last", "s04"))),  # the expert quote, set large, with the real strip under it
    # the city
    ("s06", 10.17, 12.78, "V", dict(src=CITY, sin=2.0, mode="vert")),
    ("s07", 12.78, 14.30, "V", dict(src=G7, sin=6.6, mode="fill", pre=P_G7, rate=3.0, rev=True)),
    ("s08", 14.30, 15.19, "V", dict(src=G6, sin=1.3, mode="fill", pre=P_G6)),
    ("s09", 15.19, 17.10, "V", dict(src=G2, sin=2.6, mode="fill", rate=1.6)),
    # the experiment
    ("s10", 17.10, 19.69, "V", dict(src=WIRES, sin=3.0, mode="fill", cx=0.55)),
    ("s11", 19.69, 21.76, "SIM", dict(src=SIM + "helix.mp4", sin=0.25)),
    ("s12", 21.76, 24.18, "GFX", dict(bd=("last", "s11"))),
    ("s13", 24.18, 25.50, "PDF", dict(doc="at", page=1, box=(150, 2180, 2250, 430), w=1000, bd=("last", "s11"))),
    ("s14", 25.50, 27.90, "V", dict(src=WINDOWS, sin=1.0, mode="fill", cx=0.5)),
    ("s15", 27.90, 30.31, "V", dict(src=WINDOWS, sin=5.5, mode="fill", cx=0.62)),
    ("s16", 30.31, 32.86, "GFX", dict(bd=("last", "s15"))),
    ("s17", 32.86, 36.70, "V", dict(src=BOARD, sin=1.0, mode="fill", cx=0.42)),  # keeps the threatening notes out of frame
    # the detectives
    ("s18", 36.70, 38.98, "V", dict(src=DETECTIVE, sin=15.0, mode="vert")),
    ("s19", 38.98, 42.19, "GFX", dict(bd=("last", "s18"))),
    ("s20", 42.19, 44.44, "IMG", dict(file="f1a.png", crop=(0, 0, 1560, 1070), w=1000, bd=("last", "s18"))),
    ("s21", 44.44, 46.07, "REC", dict(sin=41.6)),
    ("s22", 46.07, 47.17, "V", dict(src=LIBRARY, sin=2.0, mode="fill", cx=0.5)),
    ("s23", 47.17, 48.78, "V", dict(src=TYPE, sin=5.6, mode="fill", cx=0.5)),
    # the reference race
    ("s24", 48.78, 52.91, "GFX", dict(bd=(DETECTIVE, 12.0))),
    ("s25", 52.91, 55.71, "GFX", dict(bd=(BIGLIB, 3.0))),
    # the tests
    ("s26", 55.71, 60.71, "PDF", dict(doc="at", page=1, box=(150, 220, 2250, 980), w=1000, bd=(BIGLIB, 3.0))),
    ("s27", 60.71, 63.38, "GFX", dict(bd=(LAB, 3.0))),  # two sentences of the abstract set large, the real abstract under them
    ("s28", 63.38, 66.44, "IMG", dict(file="f4k.png", crop=(0, 0, 1080, 900), w=760, bd=(LAB, 3.0))),
    # the clue
    ("s29", 66.44, 68.04, "V", dict(src=G4, sin=3.4, mode="fill", pre=P_G4, ramp=[(0, 2.4), (1.0, 1.0)])),
    ("s30", 68.04, 70.51, "IMG", dict(file="atlas_0.3.png", crop=(0, 560, 1320, 1230), w=1000, bd=("last", "s29"))),
    ("s31", 70.51, 71.69, "SIM", dict(src=SIM + "walk.mp4", sin=0.25)),
    ("s32", 71.69, 72.91, "V", dict(src=G3, sin=1.0, mode="fill")),
    ("s33", 72.91, 74.76, "V", dict(src=G7B, sin=0.3, mode="fill")),
    ("s34", 74.76, 77.03, "GFX", dict(bd=(G6, 2.0))),
    ("s35", 77.03, 78.88, "V", dict(src=G5, sin=1.0, mode="fill", ramp=[(0, 1.0), (0.75, 0.5), (1.05, 0.15)], freeze=78.21)),
    ("s36", 78.88, 79.65, "V", dict(src=G5B, sin=3.0, mode="fill", pre=P_G5B)),
    ("s37", 79.65, 80.91, "V", dict(src=BREAD, sin=3.0, mode="fill", cx=0.5)),
    # why
    ("s38", 80.91, 83.67, "PDF", dict(doc="oa", page=7, box=(230, 820, 2100, 760), w=1000, bd=(G6, 2.0))),
    ("s39", 83.67, 86.02, "SIM", dict(src=SIM + "jam.mp4", sin=0.25)),
    ("s40", 86.02, 88.54, "REC", dict(sin=12.4)),
    ("s41", 88.54, 92.75, "PDF", dict(doc="oa", page=7, box=(230, 180, 2100, 600), w=1000, bd=("last", "s40"))),
    # the idea
    ("s42", 92.75, 95.75, "V", dict(src=G6, sin=3.4, mode="fill", pre=P_G6)),
    ("s43", 95.75, 98.13, "SIM", dict(src=SIM + "pile.mp4", sin=0.25)),
    ("s44", 98.13, 99.44, "SIM", dict(src=SIM + "fix.mp4", sin=0.25)),
    ("s45", 99.44, 101.17, "V", dict(src=G3, sin=4.6, mode="fill")),
    # careful
    ("s46", 101.17, 103.58, "V", dict(src=STRINGS, sin=4.0, mode="vert")),
    ("s47", 103.58, 104.58, "V", dict(src=MOUSE, sin=2.0, mode="fill", cx=0.42)),
    ("s48", 104.58, 105.98, "GFX", dict(bd=("last", "s47"))),  # the preprint's own notice, set large, the real header under it
    ("s49", 105.98, 107.68, "V", dict(src=PIPETTE, sin=2.0, mode="fill", cx=0.5)),
    ("s50", 107.68, 110.05, "V", dict(src=LAB, sin=2.0, mode="fill", cx=0.5)),
    ("s51", 110.05, 111.52, "V", dict(src=BOARD, sin=6.0, mode="fill", cx=0.42)),
    ("s52", 111.52, 113.14, "IMG", dict(file="f4a.png", crop=(0, 0, 2250, 1620), w=1000, bd=("last", "s51"))),
    # the bookend
    ("s53", 113.14, 114.89, "V", dict(src=G1B, sin=3.0, mode="fill", pre=P_G1B)),
    ("s54", 114.89, 116.00, "V", dict(src=AERIAL, sin=10.0, mode="vert")),
    ("s55", 116.00, 117.77, "V", dict(src=G7, sin=0.3, mode="fill", pre=P_G7)),
    ("s56", 117.77, DUR, "END", dict()),
]

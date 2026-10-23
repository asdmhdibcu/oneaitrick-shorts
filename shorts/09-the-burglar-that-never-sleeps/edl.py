"""Edit decision list for Short #9 "The burglar that never sleeps", shared by build_edit.py, make_index.py and make_audio.py.

Each shot: (id, out start, out end, kind, spec). Out times are cut on the word timings in words.json (voice 0-83.97 s).
Kinds:
  V      footage. spec: src, sin (source second at out start), rate, mode fill|vert|box, cx (0-1), pre (w, h, x, y) crop first
         (box: pre = (x, y, w, h, top) a landscape region set full width at y=top over its own blurred fill),
         ramp [(out offset, rate), ...] (first entry's offset is ignored), grade noir|day|flow|dark
  LOOP   a short source window played forwards and backwards to fill the shot (the door handle). spec: src, a, b, rate, cx
  MOSAIC the door handle in a 3 x 4 grid, every tile at its own phase (every door at once)
  PHOTO  the robot picture as a moving photo: assets/img/i1_bg.jpg under i1_fg.png (make_photo.py)
  SPLIT  left: the robot picture at night, right: a Flow clip by day. spec: src, sin
  STILL  a frame of an earlier shot, frozen (the record scratch). spec: of (shot id), at (out time)
  PAGE   a highlighted crop from the creator's PDFs (assets/pages, make_pages.py). spec: name, w
  GFX    my animated graphics over a blurred backdrop
  END    end card
Cards and graphics sit on a blurred backdrop: spec "bd" = ("last", shot id) or (src, second).
"""
H = 0.25
DUR = 86.0

R = "work/raw/"
# Flow (generated: 7 clips used of the 10 allowed, plus 1 image of 5). G1 and G3 came out as a different robot: not used.
G2 = R + "flow_30a8b499.mp4"   # aerial street, a robot at every house
G4 = R + "flow_328b367d.mp4"   # wall of keys, the robot lifts the ring
G5 = R + "flow_b9a70c75.mp4"   # key in the lock, the door opens on green light
G6 = R + "flow_8a5b2070.mp4"   # the robot walks through a home office, chest torch
G7 = R + "flow_1efc7adb.mp4"   # drops through the skylight into the boss's chair
G8 = R + "flow_11f4082f.mp4"   # daylight locksmith's workshop, robot in an apron
G9 = R + "flow_44a0a369.mp4"   # walks away down the street at dawn
# Pexels (free licence)
ROOFS = R + "px_6312208.mp4"       # aerial rooftops at night
HOUSES = R + "px_12887257.mp4"     # houses, a street lamp, clouds racing (time-lapse)
SERVERS = R + "px_1085656.mp4"     # network switches, blue light
RACK = R + "px_7140928.mp4"        # server rack
HANDLE = R + "px_6473437.mp4"      # a hand on a door handle (only 0-1.2 s: the door opens on a person after that)
PADLOCK = R + "px_10241357.mp4"    # a padlock turning on black
CHAINED = R + "px_3999371.mp4"     # a chained, padlocked door
KEYLOCK = R + "px_7646797.mp4"     # a key into a lock, close up (vertical)
KEYWALL = R + "px_6182057.mp4"     # key blanks on a red grid (vertical)
LOCKSMITH = R + "px_6182060.mp4"   # a locksmith at his machine (vertical; a flag at the top is cropped off)
CUTTER = R + "px_8321904.mp4"      # a key being cut, close up (vertical)
NOFLAG = (944, 1678, 68, 242)      # LOCKSMITH crop below the flag

SHOTS = [
    # hook: 2,250 clouds, under three hours
    ("s01", 0.00, 2.33, "V", dict(src=G2, sin=0.4, mode="fill", grade="flow")),
    ("s02", 2.33, 5.50, "GFX", dict(bd=("last", "s01"))),                       # 2,250 lights, one per tenant tried
    ("s03", 5.50, 8.30, "GFX", dict(bd=(G5, 2.0))),                              # stopwatch to 2:59, the real line
    # the street
    ("s04", 8.30, 9.65, "V", dict(src=ROOFS, sin=2.0, mode="fill", cx=0.5)),
    ("s05", 9.65, 11.80, "V", dict(src=HOUSES, sin=1.0, mode="box", pre=(760, 260, 1160, 820, 360))),
    ("s06", 11.80, 15.00, "V", dict(src=SERVERS, sin=3.0, mode="fill", cx=0.42)),
    # the burglar
    ("s07", 15.00, 18.68, "PHOTO", dict()),
    ("s08", 18.68, 20.62, "MOSAIC", dict(src=HANDLE)),
    ("s09", 20.62, 22.95, "V", dict(src=HOUSES, sin=0.3, rate=4.0, mode="fill", cx=0.4)),
    # who
    ("s10", 22.95, 24.02, "PAGE", dict(name="r1_head", w=900, bd=(ROOFS, 6.0))),
    ("s11", 24.02, 25.49, "PAGE", dict(name="r1_actor", w=960, bd=(ROOFS, 6.0))),
    ("s12", 25.49, 29.25, "GFX", dict(bd=(G2, 5.0))),                            # 14 doors, Microsoft's 14 sectors
    ("s13", 29.25, 31.40, "GFX", dict(bd=(ROOFS, 9.0))),                         # the Chinese Embassy's response
    # the password spray
    ("s14", 31.40, 34.72, "LOOP", dict(src=HANDLE, a=0.05, b=1.15, rate=2.5, cx=0.48)),
    ("s15", 34.72, 35.75, "PAGE", dict(name="r1_figure", w=1000, bd=("last", "s14"))),
    ("s16", 35.75, 37.40, "V", dict(src=PADLOCK, sin=15.6, mode="fill", cx=0.5, grade="dark")),
    ("s17", 37.40, 39.18, "V", dict(src=CHAINED, sin=0.3, mode="fill", cx=0.55)),
    # how
    ("s18", 39.18, 41.12, "V", dict(src=G5, sin=0.0, rate=0.5, mode="fill", grade="flow")),
    ("s19", 41.12, 44.00, "V", dict(src=KEYLOCK, sin=0.3, mode="vert", ramp=[(0, 0.62), (1.93, 0.3), (2.63, 2.2)])),
    ("s20", 44.00, 46.68, "V", dict(src=KEYWALL, sin=1.0, mode="vert")),
    ("s21", 46.68, 48.25, "GFX", dict(bd=("last", "s20"))),                      # ConnectWise's own advisory
    ("s22", 48.25, 50.82, "GFX", dict(bd=("last", "s20"))),                      # one key ring, every door
    ("s23", 50.82, 53.08, "V", dict(src=G4, sin=3.0, mode="fill", grade="flow")),
    ("s24", 53.08, 54.45, "GFX", dict(bd=(G5, 2.6))),                            # the password box, not needed
    ("s25", 54.45, 56.42, "V", dict(src=G5, sin=1.6, mode="fill", grade="flow", ramp=[(0, 1.0), (0.85, 0.3), (1.45, 2.4)])),
    ("s26", 56.42, 57.70, "V", dict(src=G5, sin=5.7, mode="fill", grade="flow")),
    ("s27", 57.70, 59.21, "V", dict(src=G6, sin=5.3, mode="fill", grade="flowdark")),
    ("s28", 59.21, 60.29, "V", dict(src=CUTTER, sin=6.0, mode="vert", ramp=[(0, 1.0), (0.34, 0.3), (0.79, 2.0)])),
    ("s29", 60.29, 62.10, "V", dict(src=G7, sin=0.9, mode="fill", grade="flowdark", ramp=[(0, 2.2), (0.96, 0.8)])),
    # the twist
    ("s30", 62.10, 63.38, "STILL", dict(of="s29", at=62.05)),
    ("s31", 63.38, 65.20, "PAGE", dict(name="r1_artex", w=960, bd=("last", "s29"))),
    ("s32", 65.20, 67.10, "V", dict(src=G8, sin=0.6, mode="fill", grade="flowday")),
    ("s33", 67.10, 68.80, "V", dict(src=LOCKSMITH, sin=9.2, mode="vert", pre=NOFLAG, grade="day")),
    ("s34", 68.80, 71.10, "GFX", dict(bd=("last", "s33"))),                      # the maker's own words
    ("s35", 71.10, 74.18, "SPLIT", dict(src=G8, sin=2.6)),
    ("s36", 74.18, 76.38, "GFX", dict(bd=("last", "s35"))),                      # the race
    # the takeaway
    ("s37", 76.38, 79.62, "GFX", dict(bd=(RACK, 2.0))),                          # "Allow access?"
    ("s38", 79.62, 81.50, "V", dict(src=G9, sin=0.4, mode="fill", grade="flow")),
    ("s39", 81.50, DUR, "END", dict(bd=("last", "s38"))),
]

"""Edit decision list for Short #15, "Google sent an AI to space. Its first words were a poem" (9:16, 1080x1920, 30 fps).
Shared by build_edit.py, make_index.py and make_audio.py.

Each shot starts on a word of the creator's recording (words.json, 502 words, 174.0 s). Kinds:
  V      footage, full frame. spec: m, sin, rate, cx, cy, grade (a 9:16 crop of a landscape source; vertical sources fill)
  STILL  a real photo, full frame (the camera move is CSS). spec: img, cx, cy
  IMG    a real page or figure as a card over a moving blurred backdrop. spec: img, bd, bdsin
  CARDV  a real video (Google's own animation) as a card over a moving blurred backdrop. spec: m, sin, bd, bdsin
  GFX    my graphics over a moving blurred backdrop. spec: bd, bdsin
  END    end card over the last shot, blurred
No generated media: the Flow clips in the plan became my own graphics (globe, orbit, thermos, beams) and Google's real
footage. Material lives in work/ (git-ignored): work/footage/, work/img/, work/fig/.
Google's launch video (g_launch_social) is cut together from takes; only the rocket take (4.30-8.43 s) is used: the
deploy-camera take shows other companies' satellites and logos, and the crowd takes show staff faces close up.
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
    # Google's own media (blog.google, 1 Oct 2026; Google Research, 4 Nov 2025)
    "G1": (FOOT + "g_launch_social.mp4", "the Transporter-18 launch and the deploy camera", "REAL · GOOGLE'S LAUNCH VIDEO"),
    "G2": (FOOT + "g_suncatcher_research.mp4", "the 81-satellite cluster, one orbit", "REAL · GOOGLE RESEARCH"),
    # NASA (public domain)
    "N1": (FOOT + "v03a_earth_limb.mp4", "Earth's edge from the space station", "REAL · NASA, FROM THE SPACE STATION"),
    "N2": (FOOT + "v03b_earth_clouds.mp4", "clouds from orbit", "REAL · NASA, FROM THE SPACE STATION"),
    "N3": (FOOT + "v03e_earth_snow.mp4", "snowy mountains and the horizon from orbit", "REAL · NASA, FROM THE SPACE STATION"),
    "N4": (FOOT + "v03c_earth_desert.mp4", "desert and horizon from orbit", "REAL · NASA, FROM THE SPACE STATION"),
    "N5": (FOOT + "v06_sun_sdo.mp4", "the Sun, NASA SDO (visible light only at 19-39 s)", "REAL · NASA SOLAR DYNAMICS OBSERVATORY"),
    # stock (Pexels licence; Mixkit Stock Video Free License; Coverr licence)
    "P1": (FOOT + "v20_cpu.mp4", "a chip and server boards, close up", "STOCK · PEXELS"),
    "P2": (FOOT + "v04_datacenter.mp4", "server racks", "STOCK · PEXELS"),
    "P3": (FOOT + "v05_tokyo_night.mp4", "Tokyo from the air at night (vertical)", "STOCK · PEXELS"),
    "P4": (FOOT + "v07_solar_farm.mp4", "a solar farm", "STOCK · PEXELS"),
    "P5": (FOOT + "v08_phone_typing.mp4", "typing on a phone", "STOCK · PEXELS"),
    "P6": (FOOT + "v10_fans.mp4", "computer cooling fans", "STOCK · PEXELS"),
    "M1": (FOOT + "m_phone_typing_mk4915.mp4", "hands typing on a phone", "STOCK · MIXKIT"),
    "M2": (FOOT + "m_city_night_mk49878.mp4", "a city at night from above (vertical)", "STOCK · MIXKIT"),
    "M3": (FOOT + "m_phone_texting_mk144.mp4", "a phone in a hand by a window", "STOCK · MIXKIT"),
    "M4": (FOOT + "m_fire_coal_mk3459.mp4", "glowing coals and flames", "STOCK · MIXKIT"),
    "C1": (FOOT + "c_power_tower.mp4", "a high-voltage power tower", "STOCK · COVERR"),
}
FIGS = {
    "svalbard": (IMGD + "i02_svalbard_aster.jpg", "REAL · NASA/JPL, SVALBARD FROM SPACE"),
    "radiators": (IMGD + "i01_iss_radiators.jpg", "REAL · NASA, SPACE STATION RADIATORS"),
    "google_post": (FIG + "p01_head.png", "REAL · GOOGLE, 30 OCT 2026"),
}


def have(code):
    return os.path.exists(MAT[code][0])


def src(code):
    return MAT[code][0]


# (id, anchor word index, kind, spec)
PLAN = [
    # the hook
    ("s01", 0, "V", dict(m="N1", sin=2.0)),                        # Google just launched an AI into space.
    ("s02", 7, "GFX", dict(bd="N2", bdsin=3.0)),                    # And the very first thing it said back... was a POEM.
    ("s03", 18, "GFX", dict(bd="N3", bdsin=2.0)),                   # Okay, to be fair... they asked for one.
    ("s04", 26, "CARDV", dict(m="G2", sin=0.0, bd="N1", bdsin=12.0)),  # But that little poem is the start of a really BIG idea.
    # the satellite
    ("s05", 38, "V", dict(m="G1", sin=4.45, rate=0.55, cx=0.62)),  # A month ago, a SpaceX rocket carried
    ("s06", 45, "GFX", dict(bd="N4", bdsin=1.0)),   # a fridge-sized satellite into orbit, built with a company called Planet.
    ("s07", 56, "V", dict(m="P1", sin=0.5)),                       # Inside: a Google AI chip,
    ("s07b", 61, "V", dict(m="P2", sin=4.0, cx=0.45)),             # the kind it uses in its giant data centers,
    ("s08", 70, "GFX", dict(bd="P1", bdsin=4.0)),                  # running Google's own AI model, Gemma.
    ("s09", 76, "GFX", dict(bd="N4", bdsin=4.0)),                  # It circles Earth about every hour and a half...
    ("s10", 94, "GFX", dict(bd="N2", bdsin=12.0)),                 # Their first request? A haiku about space.
    ("s11", 101, "STILL", dict(img="svalbard", cx=0.5, cy=0.5)),   # It came down over the top of the world: (SVALBARD pin)
    ("s12", 110, "IMG", dict(img="google_post", bd="N3", bdsin=10.0)),  # three short lines about looking down at Earth.
    # why space
    ("s13", 118, "V", dict(m="G1", sin=7.2, rate=0.35, cx=0.62, grade="bw")),  # But why go to all this trouble?
    ("s14", 125, "V", dict(m="C1", sin=3.0)),                      # Because AI is HUNGRY.
    ("s15", 129, "V", dict(m="M1", sin=2.0, cx=0.45)),             # Almost every AI answer you get comes from a data center:
    ("s16", 140, "V", dict(m="P2", sin=14.0, cx=0.55)),            # a building full of computers, all eating electricity.
    ("s17", 148, "V", dict(m="P3", sin=1.0)),                      # By 2030, data centers could use more electricity than... Japan
    ("s18", 163, "V", dict(m="M2", sin=2.0)),                      # So Google looked UP.
    ("s19", 167, "V", dict(m="N5", sin=24.3)),                     # The sun puts out a hundred TRILLION times more energy...
    ("s20", 183, "V", dict(m="P4", sin=2.0, cx=0.4, grade="dusk")),  # Down here, solar panels stop at night, and clouds get in the way.
    ("s21", 196, "GFX", dict(bd="N1", bdsin=18.0)),                # But in the right orbit, riding the line where day meets night...
    ("s22", 213, "GFX", dict(bd="P4", bdsin=9.0)),                 # A panel up there makes up to EIGHT times more power.
    ("s23", 224, "V", dict(m="N1", sin=22.0)),                     # Free sunshine, forever. Perfect?
    ("s24", 228, "V", dict(m="N1", sin=25.2, rate=0.3, grade="bw")),  # Not quite.
    # the heat
    ("s25", 230, "V", dict(m="P1", sin=4.0, grade="heat")),        # Chips turn electricity into heat.
    ("s26", 235, "V", dict(m="M3", sin=3.0, cx=0.35)),             # You know when your phone gets too hot and has to cool down?
    ("s27", 248, "V", dict(m="P6", sin=3.0, cx=0.4)),              # On Earth, fans and water carry that heat away.
    ("s28", 257, "GFX", dict(bd="N1", bdsin=25.0)),                # In space? No air. No wind. No water.
    ("s29", 265, "GFX", dict(bd="M4", bdsin=1.0)),                 # Think of a thermos. The empty gap between its walls keeps your coffee hot.
    ("s30", 279, "V", dict(m="N2", sin=20.0)),                     # Space... is one giant thermos.
    ("s31", 284, "V", dict(m="M4", sin=2.0, cx=0.5, grade="heat")),  # Up there, heat can only escape as invisible light, like the warmth of a fire.
    ("s32", 299, "STILL", dict(img="radiators", cx=0.5, cy=0.5)),  # So the satellite carries panels, called radiators, to glow it away.
    ("s33", 310, "GFX", dict(bd="N4", bdsin=14.0)),                # For now, the AI works in short bursts... then rests to cool down.
    # radiation
    ("s34", 323, "GFX", dict(bd="N5", bdsin=30.0)),                # Then there's radiation. Tiny, fast particles can flip a one into a zero.
    ("s35", 336, "GFX", dict(bd="P1", bdsin=6.0)),                 # A typo, right in the middle of the AI's thinking.
    ("s36", 346, "GFX", dict(bd="P1", bdsin=1.5)),                 # So Google blasted its chips with a particle beam while they ran AI.
    ("s37", 359, "GFX", dict(bd="P2", bdsin=20.0)),                # They survived more than five years' worth of radiation.
    # the big dream
    ("s38", 368, "CARDV", dict(m="G2", sin=0.0, bd="N3", bdsin=14.0)),  # The big dream? Dozens of satellites... talking by laser.
    ("s39", 388, "GFX", dict(bd="N4", bdsin=22.0)),                # Google says aiming those lasers is like hitting a coin from miles away...
    ("s40", 405, "GFX", dict(bd="N1", bdsin=6.0)),                 # Two test satellites go up in 2027.
    # the catch
    ("s41", 412, "V", dict(m="G1", sin=4.6, rate=0.6, cx=0.62)),   # But let's be honest. Google's own math says launches need to get much cheaper:
    ("s42", 426, "GFX", dict(bd="N4", bdsin=30.0)),                # under two hundred dollars a kilo.
    ("s43", 432, "V", dict(m="P2", sin=22.0, cx=0.5)),             # No one can fix a broken chip up there.
    ("s44", 441, "GFX", dict(bd="N3", bdsin=24.0)),                # And even the project's leader says it won't be cheaper than Earth for years.
    # the takeaway
    ("s45", 455, "GFX", dict(bd="N2", bdsin=28.0)),                # So that little poem tells us something big.
    ("s46", 463, "V", dict(m="P5", sin=2.0, cx=0.45)),             # Every question you ask an AI costs power...
    ("s46b", 471, "V", dict(m="N3", sin=30.0)),                    # and the search for more just left the planet.
    ("s47", 480, "STILL", dict(img="svalbard", cx=0.5, cy=0.5)),   # There's one word in this video I never said out loud... (the pin again)
    ("s48", 495, "END", dict()),                                   # Follow for more AI, explained like this.
]

W = json.load(open(os.path.join(HERE, "words.json")))
assert len(W) == 502, len(W)


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
        print(f"{sid:5s} {t0:6.2f}-{t1:6.2f} {t1 - t0:5.2f}s {kind:5s} {what!s:12s}"
              f"{'  NEEDED: ' + ', '.join(need) if need else ''}")

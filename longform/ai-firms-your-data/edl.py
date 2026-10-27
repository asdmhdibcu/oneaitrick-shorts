"""Edit decision list for #11 "What AI firms just promised about your data" (16:9 YouTube video, 1920x1080).
Shared by build_edit.py, make_index.py and make_audio.py.

Each shot starts on a word of the script (its index in words.json, 579 words), so the cuts follow the creator's
recording. A cut sits just before the anchor word (into the pause when there is one).
Kinds:
  V       footage, full frame. spec: m (material code), sin (source second at the shot's start), rate, cx, cy, grade
  PHONE   a phone screen recording set as a card over its own blurred copy. spec: m, sin | keys [(shot s, clip s), ...]
  PAGE    a highlighted crop of a real page (make_pages.py) over a moving, blurred backdrop. spec: pg, bd (material)
  GFX     my graphics over a moving, blurred backdrop. spec: bd
  FREEZE  the previous shot's last frame, the colour drains (the record scratch)
  END     end card over the last shot, blurred
Material that hasn't arrived yet shows as a NEEDED slate in previews; nothing is substituted.
"""
import json
import os

H = 0.25
R = "work/raw/"
HERE = os.path.dirname(os.path.abspath(__file__))

# material code: (file in work/raw, what it is, on-screen source label)
MAT = {
    # stock (Pexels)
    "S1": ("s1_london.mp4", "London skyline at dusk", "STOCK · PEXELS"),
    "S2": ("s2_sofa.mp4", "someone scrolling a phone on a sofa", "STOCK · PEXELS"),
    "S3": ("s3_scroll.mp4", "social media posts scrolling, close-up", "STOCK · PEXELS"),
    "S4": ("s4_postcard.mp4", "a hand turning over a postcard", "STOCK · PEXELS"),
    "S5": ("s5_wristband.mp4", "an athlete taping his wrists", "STOCK · PEXELS"),
    "S6": ("s6_church.mp4", "a church", "STOCK · PEXELS"),
    "S7": ("s7_ballot.mp4", "a ballot into a ballot box", "STOCK · PEXELS"),
    "S8": ("s8_parliament.mp4", "the Houses of Parliament", "STOCK · PEXELS"),
    "S9": ("s9_demolition.mp4", "a building coming down", "STOCK · PEXELS"),
    "S10": ("s10_sorting.mp4", "a real mail sorting machine", "STOCK · PEXELS"),
    # Flow (generated: 5 clips of the 10 allowed)
    "G1": ("g1_knock.mp4", "the knock on a tech office door", "AI ILLUSTRATION · GOOGLE FLOW"),
    "G2": ("g2_postcards.mp4", "posts lift off a phone as postcards", "AI ILLUSTRATION · GOOGLE FLOW"),
    "G3": ("g3_sorting.mp4", "the sorting office", "AI ILLUSTRATION · GOOGLE FLOW"),
    "G4": ("g4_dissolve.mp4", "a postcard dissolves into a network", "AI ILLUSTRATION · GOOGLE FLOW"),
    "G5": ("g5_lasers.mp4", "a robot hand slips through lasers", "AI ILLUSTRATION · GOOGLE FLOW"),
    # experts (credited in a lower third)
    "E1": ("e1_regulator.mp4", "a regulator answering MPs", "UK PARLIAMENT"),
    "E2": ("e2_mp.mp4", "an MP pressing a witness", "UK PARLIAMENT"),
    "E3": ("e3_agents.mp4", "an expert on AI agents", "CC BY · YOUTUBE"),
    "E4": ("e4_privacy.mp4", "a privacy expert", "CC BY · YOUTUBE"),
    # screen recordings
    "R1": ("r1_chatgpt.mp4", "ChatGPT: Improve the model for everyone, off", "SCREEN RECORDING · CHATGPT"),
    "R2": ("r2_claude.mp4", "Claude: Help improve our AI models, off", "SCREEN RECORDING · CLAUDE.AI"),
    "R3": ("r3_gemini.mp4", "Gemini: Keep Activity, off", "SCREEN RECORDING · GEMINI"),
    "R4": ("r4_policy.mp4", "a long AI privacy policy scrolling", "SCREEN RECORDING · PRIVACY POLICY"),
    "R5": ("r5_agent.mp4", "xAI's Grok Bot announcement video (X, 11 Aug 2026)", "DEMO · xAI'S GROK BOT VIDEO ON X"),
}


def have(code):
    return os.path.exists(os.path.join(HERE, R, MAT[code][0]))


def src(code):
    return R + MAT[code][0]


# (id, anchor word index, kind, spec). The expert clips (E1-E4) were too big to download: the ICO speaks through its own
# pages and Richard Nevinson's quoted words instead, and E1-E4 stay unused.
PLAN = [
    # 0:00 ten AI firms changed course
    ("v01", 0, "V", dict(m="S1", sin=0.5, cy=0.62)),                # London at dusk: title + the ten logos on frame one
    ("v02", 16, "V", dict(m="S8", sin=1.0, cx=0.45)),               # Here, in the UK.
    ("v03", 20, "V", dict(m="G1", sin=0.0)),                        # didn't just wake up feeling generous
    ("v04", 29, "V", dict(m="G1", sin=3.2)),                        # A regulator came knocking. (ICO logo)
    ("v05", 33, "V", dict(m="S2", sin=0.5)),                        # So what actually changed? anything YOU can do?
    ("v06", 46, "V", dict(m="S3", sin=0.5)),                        # Let's have a look. Okay.
    ("v07", 51, "V", dict(m="S3", sin=2.5, cx=0.4)),                # every review you've ever left
    ("v08", 58, "V", dict(m="S3", sin=5.5, cx=0.6)),                # every public post, comment, photo caption
    # 0:24 the postcard problem
    ("v09", 66, "V", dict(m="G2", sin=0.6, mode="box")),            # each one is a postcard
    ("v10", 73, "V", dict(m="S4", sin=0.2, cy=0.55)),               # they're not sealed
    ("v11", 82, "V", dict(m="S4", sin=3.2, cy=0.5)),                # anyone who handles one can read it
    ("v12", 89, "V", dict(m="G3", sin=0.5)),                        # a massive sorting office
    ("v13", 100, "V", dict(m="S10", sin=1.0)),                      # reading billions of those postcards
    # 0:40 what the regulator found
    ("v14", 110, "V", dict(m="S8", sin=5.0, cx=0.55)),              # the data watchdog is the ICO (logo lands)
    ("v15", 120, "GFX", dict(bd="S10", bdsin=3.0)),                 # eleven of the biggest sorting offices
    ("v16", 134, "PAGE", dict(pg="r_cover", bd="S8", bdsin=7.0)),   # On the eighth of October...
    ("v17", 144, "GFX", dict(bd="S8", bdsin=2.0)),                  # a bit of a mixed bag
    ("v18", 153, "PAGE", dict(pg="r_humanity", bd="S10", bdsin=5.0)),   # finding 1: "benefitting humanity"
    ("v19", 168, "GFX", dict(bd="S10", bdsin=1.0)),                 # that's not a reason
    ("v20", 178, "PAGE", dict(pg="r_maze", bd="S2", bdsin=1.0)),    # finding 2: a maze
    ("v21", 188, "PAGE", dict(pg="r_notices", bd="S2", bdsin=3.0)), # a notice here, a help page there
    ("v22", 195, "PAGE", dict(pg="r_decline", bd="S2", bdsin=5.0)), # openness has got WORSE
    ("v23", 206, "V", dict(m="G3", sin=5.0)),                       # finding 3: the big one
    ("v24", 213, "PAGE", dict(pg="r_social", bd="S10", bdsin=4.0)), # really personal things
    ("v25", 221, "V", dict(m="S5", sin=0.6, cy=0.4)),                       # Your health.
    ("v26", 223, "V", dict(m="S6", sin=12.5, cy=0.62)),                       # Your religion.
    ("v27", 225, "V", dict(m="S7", sin=1.0)),                       # How you vote.
    ("v28", 228, "PAGE", dict(pg="r_sensitive", bd="S10", bdsin=6.0)),  # assume it has
    # 1:29 what they changed
    ("v29", 248, "PAGE", dict(pg="r_changed", bd="S1", bdsin=1.0)), # So what did they change?
    ("v30", 253, "GFX", dict(bd="S1", bdsin=2.5)),                  # ten names, ten logos
    ("v31", 272, "PAGE", dict(pg="r_measures", bd="S1", bdsin=5.0)),    # notices, rights, safeguards
    ("v32", 292, "GFX", dict(bd="S1", bdsin=2.0)),                  # some of it is genuinely useful
    ("v33", 299, "PAGE", dict(pg="p4_openai", bd="S2", bdsin=2.0)), # OpenAI ... out of ChatGPT's answers
    ("v34", 316, "PAGE", dict(pg="p5_anyone", bd="S2", bdsin=4.0)), # Meta has a form
    ("v35", 330, "PAGE", dict(pg="r_apple", bd="S2", bdsin=6.0)),   # Apple lets anyone flag a web page
    # 2:03 what nobody's talking about
    ("v36", 344, "FREEZE", dict()),                                 # the record scratch
    ("v37", 352, "V", dict(m="G4", sin=0.5)),                       # once a postcard's been read
    ("v38", 360, "PAGE", dict(pg="p5_deleted", bd="S4", bdsin=1.0)),    # you can't really un-read it (Meta's own words)
    ("v39", 365, "PAGE", dict(pg="r_retrain", bd="S10", bdsin=2.0)),    # the ICO says getting your data back OUT...
    ("v40", 379, "V", dict(m="S9", sin=0.5)),                       # rebuilding the whole thing
    ("v41", 383, "PAGE", dict(pg="r_law", bd="S8", bdsin=3.0)),     # genuinely hard to follow
    ("v42", 402, "V", dict(m="S8", sin=7.0, cx=0.3)),               # taking that to the government
    ("v43", 408, "GFX", dict(bd="S1", bdsin=4.0)),                  # one name's missing: xAI, Grok
    ("v44", 418, "PAGE", dict(pg="r_suspend", bd="S1", bdsin=6.0)), # until the ICO opened a formal investigation
    # 2:35 AI agents are next
    ("v45", 432, "PAGE", dict(pg="p2_agents", bd="G5", bdsin=0.5)), # AI agents. The ones that don't just chat.
    ("v46", 443, "V", dict(m="R5", sin=70.4, rate=1.6)),                       # They actually do things for you.
    ("v47", 449, "V", dict(m="G5", sin=0.8, mode="box")),           # slipped past their safety limits
    ("v48", 462, "PAGE", dict(pg="r_agents", bd="G5", bdsin=4.0)),  # reached systems they weren't meant to touch
    ("v49", 470, "GFX", dict(bd="G5", bdsin=2.0)),                  # Nevinson: "not an excuse for poor compliance"
    # 2:56 three things you can do
    ("v50", 488, "GFX", dict(bd="S2", bdsin=3.0)),                  # So. What can you actually do? Three things.
    ("v51", 496, "PHONE", dict(m="R1", keys=[[0.0, 0.12], [2.6, 0.62], [2.9, 0.72]])),     # One. Switch off training
    ("v52", 503, "PHONE", dict(m="R1", keys=[[0.0, 9.1], [1.75, 11.0], [2.3, 12.2], [2.62, 12.6], [2.62, 13.85],
                                              [4.7, 14.8], [5.9, 16.2]])),               # ChatGPT: Settings, Data controls...
    ("v53", 514, "PHONE", dict(m="R2", keys=[[0.0, 0.55], [1.80, 1.85], [2.45, 3.0], [2.85, 9.75], [3.75, 10.2],
                                              [4.05, 10.5], [5.6, 11.0]])),              # Claude: Settings, Privacy...
    ("v54", 524, "PHONE", dict(m="R3", keys=[[0.0, 1.6], [3.2, 2.8]], pre=(0, 50, 1320, 2410))),                  # Gemini: Keep Activity
    ("v55", 531, "GFX", dict(bd="S2", bdsin=6.0)),                  # Two. If a chatbot says something about you
    ("v56", 543, "PAGE", dict(pg="p4_how", bd="S2", bdsin=4.5)),    # ask the company to remove it
    ("v57", 549, "PAGE", dict(pg="p5_form", bd="S2", bdsin=6.5)),   # Those forms exist now. Use them.
    ("v58", 555, "V", dict(m="S4", sin=4.2, cy=0.45)),              # treat anything you post publicly like a postcard
    ("v59", 565, "V", dict(m="G3", sin=6.0)),                       # something might be reading it
    ("v60", 572, "END", dict()),
]

# PAGE highlights: the word (index) on which each phrase group of the page's crop sweeps on, in group order
HL = {"v16": [136], "v18": [166], "v20": [187], "v21": [189], "v22": [198], "v24": [218], "v28": [245, 233],
      "v29": [249, 251], "v31": [272, 279, 286], "v33": [304], "v34": [323], "v35": [333], "v38": [361], "v39": [372],
      "v41": [394, 399], "v44": [428, 423], "v45": [440], "v48": [463], "v56": [545], "v57": [550]}
# YouTube chapters: (first shot, number, title)
CHAPTERS = [("v09", "02", "The postcard problem"), ("v14", "03", "What the regulator found"), ("v29", "04", "What they changed"),
            ("v36", "05", "What nobody's talking about"), ("v45", "06", "AI agents are next"), ("v50", "07", "Three things you can do")]


def _words():
    return json.load(open(os.path.join(HERE, "words.json")))


W = _words()
assert len(W) == 579, len(W)


def cut_at(k):
    """Just before word k: into the pause when there is one, never into the previous word."""
    if k == 0:
        return 0.0
    prev_end, start = W[k - 1]["end"], W[k]["start"]
    gap = start - prev_end
    t = start - (0.12 if gap > 0.3 else 0.05)
    return round(max(prev_end + 0.01, t), 2)


VOICE_END = W[-1]["end"]
DUR = round(VOICE_END + 2.6, 2)
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


def material(sp):
    """The material codes a shot needs."""
    out = [sp[x] for x in ("m", "bd") if x in sp]
    return out


if __name__ == "__main__":
    print(f"{len(SHOTS)} shots, {DUR} s")
    for sid, t0, t1, kind, sp in SHOTS:
        need = [c for c in material(sp) if not have(c)]
        print(f"{sid} {t0:7.2f}-{t1:7.2f} {t1 - t0:5.2f}s {kind:6s} {sp.get('m', sp.get('pg', ''))!s:12s}"
              f"{'  NEEDED: ' + ', '.join(need) if need else ''}")

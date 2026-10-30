"""Edit decision list for #12 "This voice isn't me" (16:9 YouTube video, 1920x1080, 7:36).
Shared by build_edit.py, make_index.py and make_audio.py.

Each shot starts on a word of the script (its index in words.json, 1272 words), so the cuts follow the creator's
recording. A cut sits just before the anchor word (into the pause when there is one).
Kinds:
  V       footage, full frame. spec: m (material code), sin (source second at the shot's start), rate, cx, cy, mode="box"
  PHONE   a phone screen recording set as a card over its own blurred copy. spec: m, keys [(shot s, clip s), ...]
  PAGE    a highlighted crop of a real page (make_pages.py) over a moving, blurred backdrop. spec: pg, bd (material)
  GFX     my graphics over a moving, blurred backdrop. spec: bd
  END     end card over the last shot, blurred
"""
import json
import os

H = 0.25
R = "work/raw/"
HERE = os.path.dirname(os.path.abspath(__file__))
ST, AI = "STOCK · PEXELS", "AI ILLUSTRATION · GOOGLE FLOW"
# material code: (file in work/raw, what it is, on-screen source label)
MAT = {
    "S1": ("s1.mp4", "a woman on the phone in her kitchen", ST),
    "S2": ("s2.mp4", "a man typing in the dark", ST),
    "S3": ("s3.mp4", "a doctor talking with a patient", ST),
    "S4": ("s4.mp4", "code on a monitor", ST),
    "S5": ("s5.mp4", "a hand filling in a form", ST),
    "S6": ("s6.mp4", "a job interview", ST),
    "S7": ("s7.mp4", "a trading screen", ST),
    "S8": ("s8.mp4", "a TV studio", ST),
    "S9": ("s9.mp4", "a phone lighting up at night", ST),
    "S10": ("s10.mp4", "a woman upset on a phone call", ST),
    "S11": ("s11.mp4", "a video call in an office", ST),
    "S12": ("s12.mp4", "Hong Kong at night", ST),
    "S13": ("s13.mp4", "a Gothic court building in London", ST),
    "S14": ("s14.mp4", "a law book", ST),
    "S15": ("s15.mp4", "a family talking at the table", ST),
    "S16": ("s16.mp4", "a cockpit", ST),
    "S17": ("s17.mp4", "house keys handed over", ST),
    "S18": ("s18.mp4", "a man texting in the street", ST),
    "S19": ("s19.mp4", "a photo edited on a phone", ST),
    "S20": ("s20.mp4", "a cheque into a bank machine", ST),
    # Flow (generated: 6 new + 2 from #11, of the 10 allowed)
    "G1": ("g1_stranger.mp4", "the stranger in the hallway, a phone in his hand", AI),
    "G2": ("g2_sorter.mp4", "a robot arm sorting job applications", AI),
    "G3": ("g3_fakeproof.mp4", "a photo of a government building shatters", AI),
    "G4": ("g4_voice.mp4", "a sound wave splits into two above a microphone", AI),
    "G5": ("g5_call.mp4", "a video call's faces turn into masks", AI),
    "G6": ("g6_autopilot.mp4", "a car driving itself in the fog", AI),
    "F2": ("f2_postcards.mp4", "posts lift off a phone as postcards (#11)", AI),
    "F3": ("f3_sorting.mp4", "the sorting office (#11)", AI),
    # screen recordings (the creator's phone; tone-mapped)
    "R2": ("r2_chatgpt.mp4", "ChatGPT: Improve the model for everyone, off (#11)", "SCREEN RECORDING · CHATGPT"),
    "R3": ("r3_sources.mp4", "ChatGPT's sources, one opened", "SCREEN RECORDING · CHATGPT"),
}


def have(code):
    return os.path.exists(os.path.join(HERE, R, MAT[code][0]))


def src(code):
    return R + MAT[code][0]


# (id, anchor word index, kind, spec)
PLAN = [
    # 0:00 the hook
    ("v01", 0, "V", dict(m="G4", sin=0.3)),                              # The voice you're hearing right now... isn't me.
    ("v02", 8, "PAGE", dict(pg="e_tts", bd="G4", bdsin=5.0)),           # It IS me. It's a clone of my voice, made with AI.
    ("v03", 21, "V", dict(m="S9", sin=3.0)),                             # ...someone else can do it with yours.
    ("v04", 38, "GFX", dict(bd="S18", bdsin=1.0)),                       # one of five dangers
    ("v05", 51, "V", dict(m="S1", sin=2.0)),                             # The weather on your phone.
    ("v06", 56, "V", dict(m="S2", sin=1.0)),                             # The chatbot that settles an argument.
    ("v07", 62, "V", dict(m="S19", sin=1.0)),                            # The app that fixes your photos.
    ("v08", 68, "V", dict(m="G1", sin=0.0)),                             # a brilliant stranger who's moved into your phone
    ("v09", 85, "V", dict(m="G1", sin=6.4)),                             # Super helpful. Never sleeps.
    ("v10", 94, "GFX", dict(bd="G1", bdsin=3.0)),                        # your secrets? a job? every photo? your mum?
    ("v11", 124, "V", dict(m="S15", sin=1.0)),                           # one free trick that protects your whole family
    # 0:46 danger 1: your secrets
    ("v12", 144, "GFX", dict(bd="S2", bdsin=2.0)),
    ("v13", 149, "V", dict(m="S2", sin=4.0)),                            # People tell chatbots everything.
    ("v14", 161, "PAGE", dict(pg="f_code", bd="S4", bdsin=1.0)),        # Samsung: source code into ChatGPT
    ("v15", 180, "V", dict(m="S11", sin=2.0)),                           # Another shared a whole meeting
    ("v16", 191, "PAGE", dict(pg="f_ban", bd="S4", bdsin=6.0)),         # Samsung's answer? It banned staff...
    ("v17", 207, "GFX", dict(bd="F3", bdsin=0.0)),                       # depends on the company: training, reviewers
    ("v18", 234, "V", dict(m="S3", sin=2.0)),                            # not protected like a chat with your doctor
    ("v19", 248, "PAGE", dict(pg="o_title", bd="S2", bdsin=6.0)),       # Plus... things leak. A bug in ChatGPT
    ("v20", 258, "PAGE", dict(pg="o_titles", bd="S2", bdsin=5.0)),      # the titles of OTHER people's chats
    ("v21", 268, "PAGE", dict(pg="o_pay", bd="S2", bdsin=3.0)),         # name, email, last four digits
    ("v22", 295, "PAGE", dict(pg="o_full", bd="S2", bdsin=5.0)),        # full card numbers never exposed
    ("v23", 309, "V", dict(m="G1", sin=7.4)),                            # how sensitive this stuff is
    ("v24", 319, "V", dict(m="F2", sin=0.6, mode="box")),               # the postcard rule
    ("v25", 336, "PHONE", dict(m="R2", keys=[[0.0, 9.1], [1.75, 11.0], [2.3, 12.2], [2.62, 12.6], [2.62, 13.85],
                                              [4.7, 14.8], [5.9, 16.2]])),   # switch off training: Data controls...
    # 1:59 danger 2: fairness
    ("v26", 353, "GFX", dict(bd="S18", bdsin=3.0)),
    ("v27", 357, "V", dict(m="S4", sin=8.0)),                            # computers are neutral
    ("v28", 364, "V", dict(m="S18", sin=3.0)),                           # But AI learns from us. From our history.
    ("v29", 378, "PAGE", dict(pg="a_team", bd="S5", bdsin=1.0)),        # Amazon built an experimental AI
    ("v30", 393, "PAGE", dict(pg="a_cvs", bd="S5", bdsin=0.0)),         # ten years of CVs; most came from men
    ("v31", 412, "V", dict(m="G2", sin=0.0)),                            # Tech has been a man's world
    ("v32", 422, "V", dict(m="G2", sin=5.0)),                            # the AI taught itself men were better
    ("v33", 433, "PAGE", dict(pg="a_women", bd="G2", bdsin=0.0)),       # "women's", two all-women's colleges
    ("v34", 458, "PAGE", dict(pg="a_never", bd="S5", bdsin=0.0)),       # never the final call; scrapped
    ("v35", 487, "V", dict(m="S6", sin=3.0)),                            # When a person is unfair, you can see it.
    ("v36", 501, "GFX", dict(bd="S4", bdsin=3.0)),                       # it looks like maths
    ("v37", 510, "V", dict(m="S20", sin=4.0)),                           # harder to spot, and to challenge
    ("v37b", 522, "GFX", dict(bd="S20", bdsin=9.0)),                     # jobs, loans, even healthcare
    ("v38", 533, "PAGE", dict(pg="i_human", bd="S6", bdsin=3.0)),       # UK: ask for a human to look at it
    # 3:14 danger 3: your eyes
    ("v39", 565, "GFX", dict(bd="S8", bdsin=1.0)),
    ("v40", 570, "V", dict(m="S8", sin=2.0)),                            # Seeing used to be believing.
    ("v41", 577, "PAGE", dict(pg="r_head", bd="S7", bdsin=1.0)),        # the Pentagon photo went viral
    ("v42", 598, "PAGE", dict(pg="r_false", bd="S7", bdsin=4.0)),       # It was fake.
    ("v43", 604, "V", dict(m="S7", sin=6.0)),                            # US stocks still dipped
    ("v44", 622, "PAGE", dict(pg="ad_frame", bd="G3", bdsin=1.0)),      # the RNC's all-AI ad
    ("v45", 652, "V", dict(m="G3", sin=0.5)),                            # "proof" of anything
    ("v45b", 669, "V", dict(m="S8", sin=5.0)),                           # If we can't agree on what's real...
    ("v46", 682, "V", dict(m="S18", sin=1.0)),                           # angry or scared in two seconds flat
    ("v47", 700, "GFX", dict(bd="S18", bdsin=2.0)),                      # Who posted it first?...
    # 4:12 danger 4: a voice you trust
    ("v48", 716, "GFX", dict(bd="G4", bdsin=2.0)),
    ("v49", 726, "V", dict(m="G4", sin=5.0)),                            # Remember my voice at the start?
    ("v50", 732, "PAGE", dict(pg="s_three", bd="S9", bdsin=1.0)),       # Starling: three seconds of audio
    ("v51", 748, "V", dict(m="S19", sin=6.0)),                           # A birthday video. A voice note.
    ("v52", 759, "GFX", dict(bd="S9", bdsin=6.0)),                       # Then the phone rings...
    ("v53", 770, "V", dict(m="S10", sin=3.0)),                           # Crying... They need money. NOW.
    ("v54", 782, "PAGE", dict(pg="t_head", bd="S10", bdsin=9.0)),       # the FTC: the family emergency scam
    ("v55", 798, "PAGE", dict(pg="s_quarter", bd="S9", bdsin=10.0)),    # more than a quarter of UK adults
    ("v56", 827, "V", dict(m="S12", sin=0.5)),                           # It's not just voices. Hong Kong.
    ("v57", 840, "V", dict(m="S11", sin=7.0)),                           # joined a video call with his CFO
    ("v58", 854, "PAGE", dict(pg="c_head", bd="S12", bdsin=0.5)),       # he sent about $25 million
    ("v59", 869, "PAGE", dict(pg="c_fake", bd="S11", bdsin=10.0)),      # everyone he saw was fake
    ("v60", 884, "V", dict(m="G5", sin=3.0)),                            # All deepfakes.
    ("v61", 886, "PAGE", dict(pg="u_arup", bd="S12", bdsin=2.0)),       # Arup. A British engineering firm.
    ("v62", 897, "V", dict(m="S20", sin=12.0)),                          # I used to work in banking.
    ("v63", 911, "V", dict(m="G4", sin=5.5)),                            # it sounds exactly like someone you love
    # 5:26 danger 5: your judgment
    ("v64", 922, "GFX", dict(bd="G6", bdsin=1.0)),
    ("v65", 931, "V", dict(m="G6", sin=0.0)),                            # automation bias
    ("v66", 957, "GFX", dict(bd="S2", bdsin=4.0)),                       # AI always sounds confident... completely wrong
    ("v67", 968, "V", dict(m="S13", sin=2.0)),                           # England's High Court
    ("v68", 987, "GFX", dict(bd="S14", bdsin=0.3)),                      # 45 cited, 18 didn't exist
    ("v69", 1006, "GFX", dict(bd="S13", bdsin=4.0)),                     # "serious implications..."
    ("v70", 1017, "V", dict(m="S14", sin=4.0)),                          # trained professionals
    ("v71", 1027, "GFX", dict(bd="G6", bdsin=0.0)),                      # it makes the other four worse
    # 6:21 four habits
    ("v72", 1060, "GFX", dict(bd="S15", bdsin=2.0)),
    ("v73", 1078, "V", dict(m="F3", sin=0.2, mode="box")),               # One. The postcard rule.
    ("v74", 1101, "PHONE", dict(m="R3", keys=[[0.0, 0.3], [3.6, 4.3], [3.9, 5.6], [5.4, 7.0], [7.6, 9.2], [9.4, 11.7]])),  # Two. Question it.
    ("v75", 1127, "V", dict(m="S15", sin=2.5)),                          # Three. A safe phrase. Tonight.
    ("v76", 1143, "GFX", dict(bd="S15", bdsin=1.5)),                     # the safe-phrase card (the hidden word)
    ("v77", 1163, "GFX", dict(bd="S10", bdsin=12.0)),                    # If "Mum" ever calls... hang up, call back
    ("v78", 1191, "V", dict(m="S16", sin=3.0)),                          # co-pilot, not autopilot
    ("v79", 1201, "V", dict(m="S2", sin=7.0)),                           # draft, brainstorm, explain; the final call is yours
    ("v79b", 1212, "V", dict(m="S5", sin=1.0)),                          # in your own words
    ("v80", 1230, "V", dict(m="G1", sin=2.0)),                           # The stranger can be brilliant company.
    ("v81", 1244, "V", dict(m="S17", sin=1.0)),                          # Just don't hand him the keys.
    ("v82", 1250, "GFX", dict(bd="S15", bdsin=1.0)),                     # one word I never said out loud
    ("v83", 1265, "END", dict()),
]
# PAGE highlights: the word (index) on which each phrase group of the page's crop sweeps on, in group order
HL = {"v02": [12, 17, 19], "v14": [167], "v16": [191, 194], "v19": [255], "v20": [263], "v21": [274, 281], "v22": [303],
      "v29": [389], "v30": [396, 405], "v33": [440, 452], "v34": [463, 473], "v38": [555], "v41": [581, 584, 588],
      "v42": [600], "v44": [641], "v50": [744], "v54": [792, 797], "v55": [809], "v58": [866], "v59": [874, 882], "v61": [892]}
# YouTube chapters: (first shot, number, title)
CHAPTERS = [("v12", "01", "Your secrets"), ("v26", "02", "Fairness"), ("v39", "03", "Your eyes"),
            ("v48", "04", "A voice you trust"), ("v64", "05", "Your judgment"), ("v72", "06", "Four habits")]


def _words():
    return json.load(open(os.path.join(HERE, "words.json")))


W = _words()
assert len(W) == 1272, len(W)


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
    return W[k]["start"]


def we(k):
    return W[k]["end"]


def material(sp):
    return [sp[x] for x in ("m", "bd") if x in sp]


if __name__ == "__main__":
    print(f"{len(SHOTS)} shots, {DUR} s")
    for sid, t0, t1, kind, sp in SHOTS:
        need = [c for c in material(sp) if not have(c)]
        print(f"{sid} {t0:7.2f}-{t1:7.2f} {t1 - t0:5.2f}s {kind:6s} {sp.get('m', sp.get('pg', ''))!s:10s}"
              f"{'  NEEDED: ' + ', '.join(need) if need else ''}")

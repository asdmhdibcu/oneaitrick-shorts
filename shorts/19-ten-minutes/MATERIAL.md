# Short #19: scene sheet and material

Hub tab: "#19 Ten minutes". Look: Lemo-Opuscar's Mid-century Cartoon (MIT licence), drawn in code.

Rebuild the alignment:

```
cp <take>.wav assets/voice_raw.wav && ffmpeg -i assets/voice_raw.wav -ac 1 -ar 16000 work/voice16k.wav
sed -E 's/\[[^]]+\] ?//g' script.txt > work/script_plain.txt
python3 whisper_chunks.py work/voice16k.wav > work/whisper_chunks.txt
python3 align_by_chunks.py work/voice16k.wav work/script_plain.txt work/whisper_chunks.txt words.json
```

## Scene sheet

Take: your ElevenLabs take, 59.36 s, word for word with script v1 (Whisper check, then 164 of 164 words aligned). The video runs about 59.3 s and cuts 0.1 s after "was", so a replay runs straight into "TEN minutes of AI". No voice effect.

One stage from the first frame to the last: the mustard pencil (GRIT on its barrel) on its bike, riding in place on a ruled worksheet line that scrolls under it, with turquoise training wheels as the AI. The camera stays on its stand: "call-out" means a round close-up on a leader line, drawn at full size rather than zoomed; "split" means the stage on the top 60% with a colour block below for the numbers; chapter changes iris through the next numbered disc. Every visual holds at least 2 s. Tracker at y ~232: WHEELS · WOBBLE · WHY · HINTS · TRY IT. Pins: left column (what happened) 1–4, right column (hints, the catch and the fix) 5–7.

| # | Time (s) | Line | What moves | Into it | Sound | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.00–4.48 | TEN minutes of AI... and people gave up almost TWICE as often. | Frame one: sunburst rays turning slowly behind the pencil, which pedals on turquoise training wheels while the line scrolls; the kitchen timer above at 10. Claim card over the lower stage: "Ten minutes of AI" in script, the slab 10 rolling like an odometer, settled by 0.8 s; chip AI PAPER · CMU · BERKELEY · OXFORD · MIT · UCLA. On "gave up" (2.54) the pencil's eyes droop; on TWICE (3.41) a tomato 2× medallion stamps onto the card (keyword pop). Tracker 1 lit. | cold open (continues the last frame) | sub-bass hit and a vibraphone chord under 0–0.5 s, clock ticks, a rubber stamp on TWICE | built |
| 2 | 4.77–7.59 | Picture your AI chatbot as TRAINING WHEELS. | The claim card wipes off; 0.2 s zoom into the wheels on "Picture" (4.77): a call-out on the back wheel, its hub a chat bubble with typing dots. On TRAINING WHEELS (6.62) a turquoise tag pops: AI = TRAINING WHEELS. | zoom-in, 0.2 s | slide whistle, pop, blip | built |
| 3 | 7.81–9.89 | Over a THOUSAND people did math. | Pull back with a slow counter-turn: the line becomes rows of tiny pencils pedalling, an atomic-age pattern; a counter rolls to 1,222 on THOUSAND (8.14); fraction medallions roll in on "math" (9.35); pin 1 parks: 1,222 PEOPLE · ~10 MIN OF AI. | pull-back | many pencil scratches, counter ticks, pin pop | built (paper) |
| 4 | 10.12–11.90 | About HALF got the wheels. | Colour-block wipe up into two lanes: on HALF (10.38) the top lane's bikes gain turquoise wheels in a ripple, labelled HAD AI; the bottom lane (olive) rides plain bikes, labelled NO AI. | colour-block wipe, bottom-up | paper swish, a ripple of pops | built (paper) |
| 5 | 12.29–15.34 | Then, without warning... the wheels came OFF. | Back to our one pencil; on "Then" the line stops scrolling and everything goes still. An iris closes on the wheels into a call-out on "warning" (13.26); on OFF (14.83) they pop off and roll out of frame, the iris opens (keyword pop OFF, tomato). | push in to the pencil, iris | the one silence: score and room tone cut at 12.2, an iris "shhk" at 13.3, then a clank and a rolling rattle on OFF | built |
| 6 | 15.62–19.39 | Alone, they solved FEWER problems than people who never had them. | Tracker 2. Split: on top the pencil wobbles on two wheels and the medallions it passes get fewer checks; below, two bars, NEVER HAD AI (olive) 74 and LOST THE AI (mustard) 57, rising on FEWER (16.75), numbers rolling, settled by 18.4; pin 2 parks: 57 vs 74 · SOLVED ALONE. | iris through disc 2 | vibraphone chord 2, wobble creaks, ticks | built (paper, Exp. 1) |
| 7 | 19.64–22.07 | And they hit SKIP almost TWICE as often. | The lower block swaps for a big tomato SKIP button; a glove presses it on SKIP (20.06, keyword pop); stamps thump onto two strips of 100 squares, NO AI 11 and LOST THE AI 20 (20.5–21.4); 2× pops on TWICE (21.01); pin 3 parks: 2× · HIT SKIP. | colour-block wipe (lower block) | button click, a fast run of stamps, pin pop | built (paper, Exp. 1) |
| 8 | 22.30–23.18 | Reading, too. | Side wipe: the worksheet under the pencil turns into an open book; the lower block becomes a page of drawn text lines. | colour-block wipe, side | page swish | built |
| 9 | 23.47–25.74 | No AI: ONE skip in a hundred. | A 10 × 10 dot grid labelled NO AI (olive); on ONE (24.51) one dot turns tomato with a pop. | continuous | one pip | built (paper, Exp. 3) |
| 10 | 26.09–27.67 | After AI: EIGHT. | A second grid beside it, AFTER AI; eight dots turn tomato in a quick run, the last on EIGHT (27.20, keyword pop); pin 4 parks: 8 vs 1 · READING SKIPS. | continuous | eight rising pips, pin pop | built (paper, Exp. 3) |
| 11 | 27.94–33.40 | Researchers think AI trains us to expect INSTANT answers... so we never learn to balance. | Tracker 3. The timer spins back and the wheels pop back on (how it happens): the chat bubble fires an answer card into the pencil's glove on INSTANT (30.30, keyword pop); from 31.7 a spirit level on the handlebars holds dead centre while the wheels do the balancing; on "balance" (32.71) its tag reads BALANCE PRACTICE: 0. | iris through disc 3 | a rewind whirr, a ding on INSTANT, a vibraphone glissando down, a gauge tick | built |
| 12 | 33.63–34.66 | Here's the weird part. | Tracker 4. The pencil freezes mid-pedal and looks at us; a 4-point sparkle. | cut on the beat | the score stops dead on "weird" (33.95), needle lift, room tone only | built |
| 13 | 34.89–39.15 | People who only asked for HINTS... did about as well as people with no AI. | A glove reaches in and steadies the seat (35.2); on HINTS (36.20) the bubble hands over a small HINT card instead of the answer (keyword pop); the wheels drop away and the pencil rides steady with only the hand. Lower block: bars HINTS 76 (turquoise) and NO AI 77 (olive) with ≈ between them (37.3–38.4); pin 5 parks: HINTS ≈ NO AI. | colour-block wipe (lower block) | the score back a step up, soft pops on the bars, pin pop | built (paper, Exp. 2) |
| 14 | 39.39–40.05 | The catch? | Tomato edges slide in; the stage dims to 70%. | cut on the beat | low hit | built |
| 15 | 40.28–41.22 | Short tests. | Proof card over the stage, 40.2–42.3: the paper's own limitation sentence ("Second, we cannot speak to the … hours (or days) later is unknown.", 28 words), re-set from the page's word images on a paper card with an off-register ink border; "tested immediately after AI removal" lights on "tests" (40.66). | page turn | page turn, highlighter scan | p01 (paper, section 6) |
| 16 | 41.39–43.83 | And the hint finding is a clue, not proof. | The card turns away; on "clue" (42.46) a tomato CLUE stamp lands on the HINTS bar, a magnifier beside it; pin 6 parks: SHORT TESTS · A CLUE. | page turn back | stamp thud, pin pop | built |
| 17 | 44.04–47.11 | So ask your AI for a HINT first... not the answer. | Tracker 5. Push into the chat bubble: a paper prompt field types itself "Give me a hint, not the answer." (44.2–46.5), keyword pop HINT (45.23); on "answer" a small HINT card comes back. | iris through disc 5, push in | typing, a send whoosh, a blip | built |
| 18 | 47.32–49.59 | Like a hand on the bike seat... that lets go. | Pull back to the whole stage: the glove holds the seat (47.5); on "lets go" (48.97) it opens and lifts away; the pencil rides on alone, steady, and the medallions behind it get mustard checks; pin 7 parks: HINT FIRST. | pull back | the chord resolves, a bell, check stamps | built |
| 19 | 49.82–52.73 | There's one word in this video I never said out loud. | Recap, the stage dead still: the left pins light one by one in story order (50.0–51.5). | continuous | one vibraphone chord per pin | built |
| 20 | 52.93–54.35 | Spotted it? Comment it. | The right pins light (52.9–53.6); the eighth slot becomes THE WORD? on "Comment" (53.71). | continuous | three chords, a chime | built |
| 21 | 54.49–56.99 | Follow for more AI, explained like this. | The stage resets to frame one's picture (wheels on, timer at 10, sunburst); the end card comes in over it. | iris-out onto the logo | end sting | built, brand logo |
| 22 | 57.20–59.31 | And remember... all it took was... | The end card clears; the timer winds back to 10 with ticks; the claim card returns, its 10 spinning up to match frame one; cut 0.1 s after "was". | mirror of frame one | clock ticks, a sub-bass swell into the cut | built |

## Material

The workspace can't reach arxiv.org (tested 15 Nov), so the paper comes from you. Nothing else to download: no photos, footage or generated media, and no company is named on screen, so no logos.

| Need | File name | What | Link |
| --- | --- | --- | --- |
| DONE | p01_paper_v6.pdf | The paper, version 6 (received 16 Nov). One sentence from its Conclusion (p. 11) is the proof card (row 15) | https://arxiv.org/pdf/2604.04721v6 |
| DONE | voice | Your take, 59.36 s, word for word (164 of 164 words aligned) | — |
| OPTIONAL | — | Nothing else. Everything on screen is drawn in code: the pencil, bike, wheels, timer, chat bubble, glove hands, bars, dot grids, SKIP button, pins and end card. Fonts are the style's own (Oleo Script, Alfa Slab One, Jost: SIL Open Font Licence) | — |

# One AI Trick: motion system

Read this in full before designing, generating or animating anything for a short. It applies to every skill in
`.claude/skills/`. Where a skill's own defaults disagree, this file, CLAUDE.md and README.md win. The full technique
tables are in the Content Hub's "Visual playbook".

## Canvas

- 1080×1920 at 30 fps.
- Main visuals sit in y 280–1220. Captions sit in the 1240–1460 band.
- Keep the bottom ~450 px free of anything that matters: the platform buttons cover it.
- Top-left: the tag `● AI CONCEPT · STORY`, coloured by category. Top-right: `@ONEAITRICK`.
- Covers: everything inside y 240–1680 (Instagram's grid crop).

## Colour

| Role | Hex | Use |
| --- | --- | --- |
| Background | #0B0C10 | Every frame |
| Card | #14161D | Panels, glass cards |
| Text | #F5F5F2 | Headlines, body |
| Lime (brand) | #C8FF4D | Logo, active caption word, the one thing that matters |
| Blue | #7CC4FF | Context, AI CONCEPT |
| Amber | #FFB547 | Limits and the catch, AI TRICK |
| Pink | #FF7AC6 | Examples, AI PAPER |
| Red | #FF6B6B | Danger, wrong, loss |

Threat vs normal (from #18): lime and blue for AI doing its job; red and amber for threats, breaches, scams and the catch.
Use them on stage elements, pin outlines and keyword boxes too, so the mood reads before the words.

Lime never goes on light paper: put lime text on a dark label instead. Footage is graded to deep blacks with lime accents.
Grades per act: cold teal for the problem, warm for the answer, film or tape for the past.

## Type

- Headlines: Inter 900, uppercase, tight tracking.
- Labels and chips: JetBrains Mono, small, uppercase.
- Karaoke captions: Inter 900, about 84 px, uppercase, 14 px dark stroke, word margin 0.2em. The active word turns lime and scales to 1.04 (emphasis words 1.08 and stay lime).
- At most two pieces of text on screen at once: the caption plus one number, label or page. No more than 3–4 words in
  any one of them; storyboard pins are the one exception (a number plus at most 4 words).
- Keyword pop (from #18, build it into the caption tool): high-impact words (CLONED, BROKE OUT, FAILED) bounce
  100 → 115 → 100 % over about 0.3 s with a coloured box behind them (lime, or red/amber for threats), with a soft pop.

## Timing and motion

- Something moves in every line. Every shot has constant drift (a slow push, pull or pan); nothing sits still.
- Change something every 2–4 s: the angle, the scale, a graphic or a colour.
- Frame one already shows the claim: the subject plus a 3–6 word title, readable at phone size.
- Seconds 4–12 are where viewers leave (the $1M math short fell from 104 % to 74 %, the brain-research short from 119 %
  to 90 %, both while giving background). Put the conflict and why it matters there, never definitions or backstory,
  and mark the turn into the conflict with a 0.2 s crash zoom or a short shake on the stressed word.
- The everyday picture arrives by 0:10. Add a twist or reset every 15–20 s.
- Big numbers in the hook roll in like an odometer and settle in under 0.8 s, then hold.
- Use eased motion (power2 or power3 out for entrances, in-out for camera moves). No linear moves except tickers and counters.
- Pace:
  - pop-ins 0.25–0.4 s;
  - camera pushes run the whole shot;
  - crash zooms 0.15–0.25 s, landing on the beat or the stressed word;
  - whips about 0.3 s, matching direction across the cut.
- One silence per short, before the biggest reveal.

## The storyboard (story spine, from #17)

Every short is built as one storyboard the viewer can follow from the first frame to the last, so nobody forgets what
was said or shown at the start. Engagement comes from following the story, not from fast cuts: a visual that flashes by
in half a second isn't seen. #17 (`shorts/17-your-moms-voice-for-sale/`, `BUILD.md`) is the reference build.
- **One stage the viewer relates to**, on screen from start to end: their phone, their inbox, their kitchen table,
  whatever the story happens on. The camera either shows the whole board or pushes into the stage, and the board is
  the default view (on screen within the first 5 s and for about half the runtime). Push in only for real pages, charts
  and moments that need reading, always to the same framing.
- **A chapter tracker** at the top (y ~232): 4–6 short chapter names. The live chapter fills lime and finished ones
  get ✓. A chapter lights when the voice reaches it, never earlier (don't give a twist away).
- **Pins:** each key fact lands as a small card beside the stage and stays there (big number 72 px, label 30 px, at
  most 4 words on two lines). A new pin slides out of the stage's edge along its own row, never across another pin; it is lime
  while new, then rests at 60 % with a white number. Pins hide while the camera is pushed in. Group them with meaning
  (in #17: left column = the attack, right column = your locks). This is the one exception to "two pieces of text".
- **Recap:** in the last ~8 s the pins light up again, by group, slow enough to read (no 0.4 s flicker).
- **Mirror ending:** the last frame mirrors the first (same stage, same position), now resolved.
- **Holds:** every visual stays on screen at least 2 s, text about 3 words a second, one new thing at a time, nothing
  under 1 s. The payoff beat holds longest.
- **Split focus for abstract parts** (from #18): when the story turns abstract (a network, a proof, a server farm), split
  the visual area 60/40: the stage on top, the animated breakdown below. Never a full-screen abstract graphic.
- **Hits stay inside the stage:** flash the stage's screen, punch the whole board slightly; no full-frame grey flashes.

## Transitions (every cut has one)

Pick by meaning, not at random:
- **Match cut:** a shape carries across the cut.
- **Zoom-through:** into a screen, eye or window and out into the next scene.
- **Whip:** for energy.
- **Glitch:** for tech moments.
- **Page turn or paper tear:** for documents and the past.
- **Feed swipe:** for phone and social.
- **Shutter or iris:** for reveals.
- **Light leak:** for a warm turn.
- **Ink spread:** for slow, thoughtful beats.
- **Split slide:** for comparisons.

Story transitions sit under the captions and labels so the words stay readable. The hyperframes-registry has about 450
ready-made blocks: use one before hand-building.

## Sound

- The voice leads. The score is ducked under it, and the mix ends at −14 LUFS with a −1.5 dBTP peak.
- Every visual hit gets a sound: a whoosh on whips, a pop on pop-ins, a tick on counters, an impact on stamps, a riser into reveals, a glitch on glitches.
- Our score and SFX tools stay. The sound-effects skill's CC0 recordings go on top.
- From #18:
  - a deep sub-bass hit or braam under the first 0.5 s, for earbud listeners;
  - tactile UI sounds: a muffled key click (`click`, `typing`) when data or code appears, a fast glitch or static
    scratch (`glitch`) on a breach or error, a soft pop or whoosh on keyword pops;
  - levels: SFX about 12–14 dB under the voice; the score ducked 18–20 dB while the voice speaks, flaring up in
    one-second pauses after a question and snapping back down (set this in `tools/mix.py` when building #18).
- Voice effects only where the story asks (a phone call, a robot speaking, a memory). Apply them to that line only, and keep the words clear.

## Proof on screen

- From #18 a real page is proof, not reading. Crop one sentence (never a full page or a full PDF), set it on a dark
  frosted-glass card with a slow 10 % push, keep it 2–3 s and highlight 2–4 words. The result itself is carried by
  motion graphics (comparison bars, a counter), not by the page. Viewers left during static preprint screenshots in
  the brain-research short.
- A sentence that matters becomes a quote card, with the real strip under it as proof.
- Source chips: `REAL · <source>`, or `AI ILLUSTRATION` on generated shots.

## End card

- A lime "1_" mark and "One AI Trick" with "AI" in lime.
- @oneaitrick, and a "+ Follow for AI, explained" pill.
- The hidden word appears on screen somewhere in the short but is never said.
- Loop (from #18): the end card sits over the mirrored first frame, not on its own black card, and the video ends
  within 0.5 s of the last word, so a replay flows straight into the hook.

## Signature visuals (from #16)

- **The AI is thinking:** the thinking orb (`library/thinking-orbs/`, skill `thinking-orbs`) in lime, driven by the timeline. Use it whenever a model works on screen: working, searching, solving, listening, composing or shaping. It becomes the channel's recurring "AI" character, with no face.
- **Logos:** every named company's logo is animated in, not just placed: a clean SVG from `pixel2motion`, drawn on or assembled in ~0.6 s.
- **How it works:** systems as `system-diagram-animation` (nodes pop, edges draw, packets travel). Maths and model internals as Manim. Physical things as `teardown`-style technical illustrations.
- **Numbers:** `data-story-charts` and `animated-chart`. Every value is exactly the source's, and the axis and source chip are on screen.
- **Big lines:** `kinetic-typography` for the hook and the twist, timed to the stressed words.
- **Analogy worlds:** `hand-drawn-cartoon` or `3d-toy-character` for the everyday picture, with invented characters only.

## Quality pass (every short, before the full render)

1. **Choreography:** for each scene, decide what moves, in what order and with how much overlap, and what stays still (`choreograph`). Nothing moves without a purpose (`animate`).
2. **Taste:** check the scenes against motionmaxxing's taste rules and run its render gates. Fix anything flat, generic or on a default ease.
3. **Review:** run `review-animations` on the composition's motion code, then fix what it flags.
4. **Critic:** an independent pass with `business-motion-film`'s critic loop on the contact sheets, before the creator sees anything.

## Before you show anything

- Snapshot every scene and ±0.1 s around every cut.
- Check them against this file.
- Fix anything cramped, overlapping, empty or off-palette, and only then show the creator.

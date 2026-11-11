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

Lime never goes on light paper: put lime text on a dark label instead. Footage is graded to deep blacks with lime accents.
Grades per act: cold teal for the problem, warm for the answer, film or tape for the past.

## Type

- Headlines: Inter 900, uppercase, tight tracking.
- Labels and chips: JetBrains Mono, small, uppercase.
- Karaoke captions: Inter 900, about 84 px, uppercase, 14 px dark stroke, word margin 0.2em. The active word turns lime and scales to 1.04 (emphasis words 1.08 and stay lime).
- At most two pieces of text on screen at once: the caption plus one number, label or page.

## Timing and motion

- Something moves in every line. Every shot has constant drift (a slow push, pull or pan); nothing sits still.
- Change something every 2–4 s: the angle, the scale, a graphic or a colour.
- Frame one already shows the claim: the subject plus a 3–6 word title, readable at phone size.
- The everyday picture arrives by 0:10. Add a twist or reset every 15–20 s.
- Use eased motion (power2 or power3 out for entrances, in-out for camera moves). No linear moves except tickers and counters.
- Pace:
  - pop-ins 0.25–0.4 s;
  - camera pushes run the whole shot;
  - crash zooms 0.15–0.25 s, landing on the beat or the stressed word;
  - whips about 0.3 s, matching direction across the cut.
- One silence per short, before the biggest reveal.

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
- Voice effects only where the story asks (a phone call, a robot speaking, a memory). Apply them to that line only, and keep the words clear.

## Proof on screen

- Real pages are set large and briefly, with the key words highlighted.
- A sentence that matters becomes a quote card, with the real strip under it as proof.
- Source chips: `REAL · <source>`, or `AI ILLUSTRATION` on generated shots.

## End card

- A lime "1_" mark and "One AI Trick" with "AI" in lime.
- @oneaitrick, and a "+ Follow for AI, explained" pill.
- The hidden word appears on screen somewhere in the short but is never said.

## Before you show anything

- Snapshot every scene and ±0.1 s around every cut.
- Check them against this file.
- Fix anything cramped, overlapping, empty or off-palette, and only then show the creator.

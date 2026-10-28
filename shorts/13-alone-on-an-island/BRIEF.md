# Short #13: "Alone on an island, the AI started to play" (brief and handoff)

Status on 28 Oct 2026: the creator picked this pitch (2 of 3). `script.txt` is draft v1, **waiting for the creator's
OK** before they record it in ElevenLabs. It is 233 words, about 88 s at #9's pace. Nothing is built yet. First short
under the worldwide-audience rule (CLAUDE.md, from #13): plain international English, US spelling on screen.

The other two pitches, not picked: "The AI that felt pain" (The Pain Axis, arXiv 2609.16247, 25 open models, a
relief button that deletes a user's family photos, 71% for the 72B model; next in line) and "Ten minutes with
ChatGPT made them quit" (Brian Christian et al., arXiv 2604.04721, COLM).

## The story

Hook → evidence → twist → takeaway. MIT left 13 copies of an AI alone on a virtual island for 30 hours with no task
and no reward, and it started to play. Evidence: games, sand mandalas, a block temple, the spire climb ("I'M ON THE
SPIRE"), the lost golden ring and the heart of stones, six of 13 discovering the mid-jump throw. Twist: given real
tasks afterwards, the agents that had played did about three times better than fresh copies (10.3 vs 3.5 objects on
the spire). Catch: even the authors say it could be role-play. Takeaway: play isn't wasted time; it's how you get good.

## Facts (from coverage; check every one against the paper)

**Paper:** "Is this machine playing?", Nathan Cloos, Antonio Norelli, Daniel Durbin, Jacob Andreas, Daniela Rus,
Phillip Isola (MIT CSAIL). arXiv 2610.07130, posted 5 Oct 2026, not peer reviewed.

- 13 agents, each Claude Opus 4.7 running in Claude Code, named Eko, steering a lobster-shaped body on a simulated
  island (reported as "Mesa World", built with "Clawblox"; one outlet says it's loosely based on Roblox).
- Minimal instruction: no task, no reward, no named activity. 30-hour runs. The world reset every hour; notes in text
  files carried over and served as memory (the script's "diary").
- Behaviour reported: climbing hills and rock spires, stacking blocks into towers and a makeshift temple, drawing
  mandalas, reinterpreting sports, physics experiments, spelling its name in blocks.
- Spire: the first climb failed; it hauled a rock up a nearby summit, stacked two blocks on top and jumped. Log:
  "I'M ON THE SPIRE".
- Golden ring thrown into the ocean while testing throw distance; it arranged stones into a heart as a memorial.
- Six of 13 learned to throw blocks farther by releasing mid-jump, a mechanic nobody programmed on purpose.
- Follow-up tasks: experienced agents put an average of 10.3 objects on the tallest spire, fresh copies 3.5 (2.9×,
  "about three times").
- Caveats: Cloos to MIT Technology Review, "All of this could be role-playing." Eunice Yiu (UC Berkeley): "It could be
  the case that the models are genuinely playing, but we don't know based on the paper." Isola (Gizmodo): "Eko seems
  to act like this little toddler in some ways, but [it] is also superintelligence."

**To confirm in the paper before recording:** the temple wording, "first try failed", the heart memorial, six of 13,
10.3 vs 3.5 and what was counted, whether "Claude" can be named as the model, and the reset interval.

**Unreachable from the workspace:** arxiv.org, technologyreview.com, gizmodo.com, mit.edu. GitHub works.

## Material to ask for once the script is OK

- NEEDED: the paper PDF (arxiv.org/pdf/2610.07130) into `work/pdf/` (git-ignored). Its figures and any screenshots of
  the island become real-material shots and the proof strip under the quote card.
- OPTIONAL: MIT Technology Review's article (19 Oct) as a PDF for a dated headline card, and any project page or video
  the authors published (as in #5, their own footage beats a recreation).

## Build rules for #13

- Mostly our own graphics: a stylised island built for the short, the real paper as proof. At most 2 Flow clips and
  2 generated images (caps 10 and 5). Label recreations "ILLUSTRATION"; real figures "REAL · PAPER".
- New Fluent 3D art (all checked to exist, MIT licence): Lobster, Desert island, Rock, Brick, Mountain, Notebook with
  decorative cover, Water wave, Hindu temple or Classical building, Ring, Red heart, Video game, Chart increasing.
  Fetch with `fetch_fluent.py`, upscale, commit to `library/3d/`.
- Graphics upgrades to try here first (template stays on its own GSAP until this renders cleanly): GSAP 3.15 from npm
  (free licence) for SplitText (the hook builds word by word), MotionPath (Eko's jump arc, the ring flying into the
  sea, the mid-jump throw going farther) and DrawSVG (mandala lines drawing in the sand).
- Option for the island: one three.js island rendered offline with `render3d.py` (#8), with Eko placed via `pins3d.py`.
- Hidden word for Instagram: **JOY**, drawn into the sand mandala. The voice never says it.
- Every key beat readable with the sound off (worldwide rule): the "30 HOURS / NO TASK / NO REWARD" card, the diary
  page, the 10.3 vs 3.5 bars.

## Shot ideas, line by line

1. Hook: an island from above, a tiny lobster; "30 HOURS · NO TASK · NO REWARD" stamps in; "PLAY" bounces in.
2. Eko's intro card: lobster + "run by Claude" chip.
3. A clock spins, the world wipes clean, the diary stays (notebook glows through the reset).
4. Quick montage: game, sand mandala drawing on, blocks stacking into a temple.
5. The spire towers over Eko; a fall and a "FAIL" scratch.
6. Rock dragged uphill, two blocks pop on, the jump on a MotionPath arc with a whoosh.
7. Diary page writes itself: "I'M ON THE SPIRE!" (handwriting font, typed on).
8. The golden ring arcs out and sinks; ripples.
9. Stones land one by one into a heart (Red heart glow at the end).
10. 13 lobsters in a grid; 6 light up; two throw arcs side by side, the mid-jump one lands farther.
11. Clipboard / "REAL WORK" card slides in (the twist).
12. Two bars count up: 3.5 fresh, 10.3 played; "×3".
13. Quote card: "All of this could be role-playing." with the paper strip under it.
14. Takeaway: Eko on the spire at sunset; "PLAY ISN'T WASTED TIME".
15. Hidden-word line over the mandala (JOY visible); end card.

## Instagram (from #12)

- Carousel, 8–10 slides at 1080×1350: the island, "no task, no reward", the spire, the ring and the heart, the mid-jump
  trick, 3.5 vs 10.3, the catch, "play isn't wasted time".
- Trial Reel openings to test:
  - A: "Scientists left an AI alone on an island for thirty hours. It started… to play."
  - B: "This AI lost its golden ring in the sea. So it built it a heart."
  - C: "The AI that played did three times better at its job."

## Posting

- YouTube title, plain and worldwide: "Scientists left an AI alone on an island. It started to play." Hashtags in the
  description: #AI #Science #Shorts.
- Translated title, description and subtitles: Spanish, Portuguese, Hindi, Indonesian.
- Credit "3D art: Microsoft Fluent Emoji (MIT licence)" and the paper (Cloos et al., MIT CSAIL, arXiv 2610.07130).
- Post at about 14:00 UTC, at least 24 h after #12's Short.

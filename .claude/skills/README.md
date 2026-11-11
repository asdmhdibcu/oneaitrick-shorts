# Skills in this repo

These skills load in any Claude Code session that has this repo open. They were installed on 11 Nov 2026, after the
account-level `hyperframes` and `motion-video-skills` plugins disappeared from the creator's account. They are technique
libraries. CLAUDE.md, README.md, `MOTION.md` and the project instructions decide the workflow. Where a skill disagrees
with them, ours win.

| Skill | From | Licence | Use it for |
| --- | --- | --- | --- |
| `hyperframes` | heygen-com/hyperframes @ 941049a (11 Nov 2026) | Apache-2.0 | Composition rules, render contract |
| `hyperframes-cli` | same | Apache-2.0 | check, snapshot, render, recovering from failures |
| `hyperframes-registry` | same | Apache-2.0 | ~450 blocks: transitions, titles, kinetic type, captions, charts, maps, 3D, camera moves |
| `media-use` | same | Apache-2.0 | Free local tools: transcripts, cut-outs, grades, mixing placed audio |
| `reverse-any-video` | same | Apache-2.0 | Rebuild a reference short's moves frame by frame to learn its technique |
| `style-sampling` | same | Apache-2.0 | Proven explainer styles (Collage, Animated Science, 3D Explainer) applied to our topic |
| `motion-effects` | charlie947/motion-graphics-skills @ 229022e | MIT | 16 premium effect recipes |
| `motion-brief-writer` | same | MIT | Turn a scene idea into a precise build brief |
| `motion-prompt-writer` | same | MIT | Claude Motion prompts for one looping graphic |
| `reference-to-motion` | same | MIT | Scene-by-scene plan from a reference reel |
| `vox-explainer` | same | MIT | Torn paper, halftone, condensed type |
| `animated-chart` | same | MIT | Exact-value animated charts |
| `milestone-reveal` | same | MIT | A big number assembling from particles |
| `title-sequence-3d` | same | MIT | Three.js title shots |
| `reel-export` | same | MIT | Safe-zone and encode checks for 9:16 uploads |
| `model-showdown` | same | MIT | Three AI models side by side |
| `brand-intake` | same | MIT | Already done: `brand.md` and `MOTION.md` at the repo root |
| `sound-effects` | Barty-Bart/motion-graphics @ 3d83d98 | MIT; `sfx/` is CC0 | Measured sound pass and 109 real CC0 sounds (Kenney, Freesound) |
| `explainer-engaging` | same | MIT | One hero element travelling through a one-take course |
| `explainer-high-energy` | same | MIT | Beat-locked kinetic promos |
| `motion-broll` | same | MIT | Motion-graphic B-roll timed to a transcript |

The full licence texts are in `_licenses/`.

## Where they clash with our rules

- **Credits:** `media-use` says to plan for the best result and not mention prices. Here, ask the creator before spending any HeyGen, vidIQ or other paid credit. Prefer the free local route.
- **Sound:** `sound-effects` bans synthesised sound. Our `tools/make_sfx.py` and `tools/make_track.py` stay, and its CC0 recordings go on top. Credit is optional, but name Kenney and Freesound in the description when they're used.
- **Grading:** `media-use` routes grades through `media-treatment`, which is newer than our pinned CLI. Our ffmpeg grades stay.
- **CLI version:** the HyperFrames skills track the latest CLI. Our shorts stay on `hyperframes@0.8.162` until one is rebuilt and checked on a newer version.
- **Labels:** some skills ban corner labels, counters and timecodes. Our source chips and number captions stay.
- **Formats:** skills that target 16:9, LinkedIn, newsletters or 8-second loops are recipes to borrow from, not formats to deliver. Every short is 1080×1920, 30 fps, 60–90 s.

## Left out on purpose

- `figma`: it clashes with the account's Figma plugin.
- `slideshow` and `remotion-to-hyperframes`: not needed.
- HeyGen's internal craft skills (`.claude/skills` inside their repo): they are tied to HeyGen's own assembler.
- `object-separation`: it runs SAM 2 on the creator's own computer.
- `explainer-default`, `apple-launch-film`, `launch-video`, `newsletter-promo` and `loop-cover`: product-launch and newsletter formats.
- Still out, from README: onetake (non-commercial licence), lemo-opuscar (it pulls new instructions on every run) and claude-youtube (paid DataForSEO).

To update a skill, copy the new version from its GitHub repo over the folder, note the commit in this table, and check its
diff for new network calls or paid steps first.

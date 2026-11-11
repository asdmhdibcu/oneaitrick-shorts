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

### Added 11 Nov 2026 for video quality

These were picked from the security-graded index zhuyansen/awesome-claude-video-skills and from the designers people
follow for motion craft (Emil Kowalski, Jakub Krehel, Jakub Antalík). Each was cloned and read before it went in.

| Skill | From | Licence | Use it for |
| --- | --- | --- | --- |
| `motionmaxxing` | Tejashmakwana/motionmaxxing (1.4k stars, graded SAFE) | Apache-2.0 (+ NOTICE: GSAP standard licence, Three.js MIT, Inter OFL) | The anti-slop director: taste rules, studies, a film template, and render gates that fail flat or generic motion before a render |
| `kinetic-typography` | PHANTOMTONYT/motion-design-skills | MIT | Words as the visuals: slam, stretch, stack, split, timed to the voice. Built on HyperFrames and GSAP |
| `system-diagram-animation` | same | MIT | How an AI system works, node by node, with data packets travelling along the edges |
| `data-story-charts` | same | MIT | A chart carries the argument: lines draw, bars grow, a counter ticks |
| `hand-drawn-cartoon` | same | MIT | Storybook cartoons with boiling ink lines, for analogy stories |
| `3d-toy-character` | same | MIT | Soft vinyl-toy 3D characters (Three.js), for analogy stories without real people |
| `animate`, `choreograph`, `review-animations`, `animation-vocabulary`, `apple-design` | emilkowalski/skills | MIT | Motion craft: whether to animate, easing and springs, order and overlap of several elements, and a strict review of motion code |
| `teardown`, `better-typography`, `better-colors`, `better-ui`, `explain-interface` | jakubkrehel/skills | MIT | Technical illustrations of how things work; type, colour (OKLCH) and surface polish; how a reference effect was built |
| `transitions-dev` | Jakubantalik/transitions-dev | MIT | 10+ production transitions (card resize, number pop-in, badges, text swap, panel reveal) for interface rebuilds |
| `thinking-orbs` | MengTo/Skills (skill) + Jakubantalik/thinking-orbs 0.3.1 (library) | MIT | The animated AI orb (working, searching, solving, listening, composing, shaping) |
| `pixel2motion` | nolangz/pixel2motion (2.6k stars) | MIT | Turn a company logo into a clean SVG and animate it, for every named company |
| `manimce-best-practices`, `manim-composer` | adithya-s-k/manim_skill (1.3k stars, graded SAFE) | MIT | 3Blue1Brown-style maths and model internals (attention, embeddings, gradients) |
| `business-motion-film` | echris6/motion-video-kit (1.4k stars, graded SAFE) | MIT | An independent critic loop and a premium quality bar for a finished cut |

The thinking-orbs library source is in `library/thinking-orbs/`. Its engine (`src/engine/`) is a set of pure functions
of time, `frame(size, t, opts)`, so a HyperFrames timeline can drive it frame-exactly. No React is needed in a
composition. The orb draws monochrome dots, so tint them with the brand lime.

The full licence texts are in `_licenses/` (the motionmaxxing licence and NOTICE sit in its own folder).

## Where they clash with our rules

- **Credits:** `media-use` says to plan for the best result and not mention prices. Here, ask the creator before spending any HeyGen, vidIQ or other paid credit. Prefer the free local route.
- **Sound:** `sound-effects` bans synthesised sound. Our `tools/make_sfx.py` and `tools/make_track.py` stay, and its CC0 recordings go on top. Credit is optional, but name Kenney and Freesound in the description when they're used.
- **Grading:** `media-use` routes grades through `media-treatment`, which is newer than our pinned CLI. Our ffmpeg grades stay.
- **CLI version:** the HyperFrames skills track the latest CLI. Our shorts stay on `hyperframes@0.8.162` until one is rebuilt and checked on a newer version.
- **Labels:** some skills ban corner labels, counters and timecodes. Our source chips and number captions stay.
- **Formats:** skills that target 16:9, LinkedIn, newsletters or 8-second loops are recipes to borrow from, not formats to deliver. Every short is 1080×1920, 30 fps, 60–90 s.
- **motionmaxxing paid steps:** it makes voice, SFX and music through ElevenLabs when a key is set, which spends the creator's credits. Ask first. The narration is always the creator's own recorded take, never one it generates. Its Codex image step isn't available here. Use its taste rules, studies and render gates freely.
- **Web UI skills (Emil Kowalski, Jakub Krehel, transitions-dev, thinking-orbs):** these are written for interactive apps. Take the motion craft and visual polish: easing, springs, choreography, type, colour, transitions. Skip the parts about keyboard, gestures, focus and component APIs, which don't apply to a rendered video.
- **Analogy characters (`3d-toy-character`, `hand-drawn-cartoon`):** invented characters only, never a real, recognisable person. No face on camera still holds.
- **Manim:** it needs `pip install --break-system-packages manim` plus system Cairo and Pango. Check that they install in the workspace before planning a short around it.

## Left out on purpose

- `figma`: it clashes with the account's Figma plugin.
- `slideshow` and `remotion-to-hyperframes`: not needed.
- HeyGen's internal craft skills (`.claude/skills` inside their repo): they are tied to HeyGen's own assembler.
- `object-separation`: it runs SAM 2 on the creator's own computer.
- `explainer-default`, `apple-launch-film`, `launch-video`, `newsletter-promo` and `loop-cover`: product-launch and newsletter formats.
- From the 11 Nov search:
  - remotion-dev/skills: a different renderer.
  - vibe-motion/skills: no licence file.
  - vox-director and wallstreet-explainer: 16:9 and Chinese-language pipelines.
  - digitalsamba/claude-code-video-toolkit: Remotion, plus paid cloud GPUs and APIs.
  - kylezantos/design-motion-principles: repeats Emil's and Jakub's own skills.
  - The rest of Emil's and Jakub Krehel's packs: app-building tools.
  - `manimgl-best-practices`: the other Manim fork.
- Still out, from README: onetake (non-commercial licence), lemo-opuscar (it pulls new instructions on every run) and claude-youtube (paid DataForSEO).

To update a skill, copy the new version from its GitHub repo over the folder, note the commit in this table, and check its
diff for new network calls or paid steps first.

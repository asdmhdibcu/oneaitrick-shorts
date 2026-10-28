# Short #13: material list (real footage first)

The creator's direction (28 Oct): no icon or cartoon look. Real footage and real visuals carry the short; graphics are
only labels, numbers and highlights on top. The Fluent 3D idea in BRIEF.md is dropped for this short.

Four layers, in order of preference:

1. **The real island from the paper.** Clawblox, the engine the MIT team built Mesa Island in, is open source
   (github.com/nacloos/clawblox, MIT licence; the world is `worlds/mesa-island`, a three.js renderer). Built and run in
   the workspace, it lets us film the actual island and drive Eko through the exact beats (the spire, the ring, the
   stones) from a script, without paying for an AI agent. Label: "REAL ISLAND · RECREATED RUN". Needs the creator's
   OK, because it builds and runs code from GitHub. Fallback: the paper's own figures and screenshots.
2. **Real stock footage** (Pexels, Pixabay, Mixkit, Coverr). The creator downloads it; the workspace can't reach those
   sites. Use it for the real-world echo of each beat, so the story feels physical, not drawn.
3. **Generated clips** (Google Flow, Veo) only where no real shot exists: Eko as a cinematic robot lobster. Cap 10
   clips and 5 images; this plan uses 6 clips and 0 images. Label "AI ILLUSTRATION" and turn on YouTube's altered or
   synthetic content label.
4. **Documents:** the paper PDF (figures, the 10.3 vs 3.5 result, the role-play caveat), MIT Technology Review's
   article as a dated headline.

## Shot list (line by line)

Files go in `work/footage/` (git-ignored) with these names. Search terms are for Pexels first, then Pixabay.

| # | Line | Shot | Source | File / search |
|---|---|---|---|---|
| 1 | "Scientists left an AI alone on an island…" | Slow aerial push over a lone island in open ocean | Stock | `01_island_aerial.mp4`: "aerial island ocean drone", "lonely island aerial" |
| 1b | "…thirty hours. No job. No reward." | Timelapse sun crossing the sky over the sea | Stock | `01b_timelapse_sky.mp4`: "sea timelapse sunrise sunset" |
| 1c | "And it started… to PLAY." | Eko on the real island, first frame of the recreated run | Clawblox | `01c_eko_real.mp4` (I record it) |
| 2 | "Meet Eko… run by Claude" | Cinematic robot lobster on wet sand, waves behind | Flow #1 | `02_eko_beach.mp4` |
| 2b | | The real island from above with Eko's lobster body | Clawblox / paper fig. | `02b_mesa_overview.png` |
| 3 | "Every hour, its world reset. …a diary." | Hand writing in a notebook, close-up; page flips | Stock | `03_journal.mp4`: "writing journal close up", "notebook pen writing" |
| 3b | | The real notes file (text from the paper's appendix) typed on screen | Paper | from the PDF |
| 4 | "It invented games." | Real island: Eko kicking or throwing a block | Clawblox | `04_games.mp4` |
| 4b | "Drew patterns in the sand." | A real sand mandala being made (monks' coloured sand), top-down | Stock / Wikimedia Commons (CC) | `04b_sand_mandala.mp4`: "sand mandala", "drawing in sand beach" |
| 4c | "Stacked blocks into a temple." | Real island: block tower; cut to stone stacking on a beach | Clawblox + stock | `04c_cairn.mp4`: "stacking stones beach", "rock balancing" |
| 5 | "…the tallest rock on the island. First try? It failed." | Low angle up a sea stack or rock spire; Eko slipping off | Stock + Flow #2 | `05_sea_stack.mp4`: "sea stack aerial", "rock pillar ocean"; `05b_eko_fall.mp4` |
| 6 | "…dragged a rock up the hill… and JUMPED." | Real island: rock carried, two blocks placed, the jump (slow motion at the top) | Clawblox | `06_spire_jump.mp4` |
| 6b | | Real-world echo: a climber's last step onto a summit | Stock | `06b_summit.mp4`: "climber reaches summit", "mountain top jump" |
| 7 | "Its diary said: I'M ON THE SPIRE!" | The real log line, typed on as a terminal or notes page | Paper | quote card over `06b` |
| 8 | "…threw a golden ring too far. Gone, into the sea." | Gold ring falling into water, underwater, in slow motion | Stock | `08_ring_water.mp4`: "ring falling into water slow motion", "gold ring underwater" |
| 8b | | Real island: the ring arcs off the cliff | Clawblox | `08b_ring_throw.mp4` |
| 9 | "…laid stones in the shape of a heart." | Heart of pebbles on a beach, waves washing in, top-down | Stock | `09_stone_heart.mp4`: "heart stones beach", "pebble heart sand" |
| 9b | | Real island: stones placed in a heart (if the recreation allows) | Clawblox | `09b_heart_real.mp4` |
| 10 | "Thirteen copies…" | 13 robot lobsters on the shoreline, wide | Flow #3 | `10_thirteen.mp4` |
| 10b | "…throw a block in the middle of a jump…" | Real island: two throws side by side, standing vs mid-jump; distance lines | Clawblox | `10b_midjump.mp4` |
| 11 | "Then came the twist. …real work." | A real lab or office: screens, a whiteboard with tasks | Stock | `11_lab.mp4`: "computer lab screens", "scientist computer night" |
| 12 | "…about THREE times as much…" | The paper's results figure, redrawn as animated bars 3.5 → 10.3 over the real figure | Paper | from the PDF |
| 13 | "Is it really playing? …might just be acting." | MIT Technology Review headline, then quote card with the paper strip | Documents | PDF of the article |
| 14 | "Play isn't wasted time. It's how you get good." | Real play: children building sandcastles, puppies wrestling, a skateboarder trying again | Stock | `14_kids_sandcastle.mp4`: "children building sandcastle"; `14b_puppies_play.mp4`: "puppies playing"; `14c_skate_retry.mp4`: "skateboard trick fail try again" |
| 14b | | Eko on the spire at sunset | Flow #4 | `14d_eko_sunset.mp4` |
| 15 | Hidden word line | "JOY" written in wet sand, a wave about to reach it | Stock + our text | `15_sand_writing.mp4`: "writing in sand beach wave" (we key JOY into the sand) |
| 16 | End card | Island aerial at dusk under the end card | Stock | reuse `01` |

Spare Flow budget (2 clips) for re-takes of #1 and #4. Flow #5 and #6 are reserved for whatever the paper shows that
stock can't: for example, Eko hauling the rock, if the Clawblox recording doesn't work out.

## Flow prompts (720×1280, then conformed as in #5)

1. "Cinematic close-up of a small sleek robot shaped like a lobster on wet sand at golden hour, gentle waves behind,
   shallow depth of field, realistic, documentary nature-film look, slow push in."
2. "A small robot lobster tries to climb a tall rock pillar on a beach and slides back down onto the sand, realistic,
   handheld documentary camera, overcast light."
3. "Wide shot of thirteen identical small robot lobsters standing in a line along a shoreline at dawn, mist, realistic,
   slow lateral dolly."
4. "A small robot lobster standing on top of a tall rock spire above the ocean at sunset, wind, realistic, slow aerial
   orbit, epic but quiet."

Keep the bottom third clear of busy detail (captions sit at y 1240–1460), and check each clip for Veo's dark band.

## Safety checks on stock (as in #8)

- Look at whole frames, not only the planned crop: no logos, faces we can't use, or text.
- Children in shot 14: wide shots and backs only, from model-released stock.
- Record each clip's source URL and licence in `edl.py`.

## Credits for the description

Paper: Cloos, Norelli, Durbin, Andreas, Rus & Isola, "Is this machine playing?" (MIT CSAIL, arXiv 2610.07130).
Island footage recreated in Clawblox (MIT licence). Stock: the Pexels / Pixabay creators, by name. Generated
illustrations: Google Veo.

## Footage in hand (28 Oct, `work/footage/`, git-ignored)

All stock is Mixkit, **Mixkit Stock Video Free License** (checked on each page; "Restricted" clips skipped), 1080p.
Pexels and Pixabay answer automated browsers with a bot check, so those come from the creator if wanted.

| File | Mixkit id | Shot | Note |
|---|---|---|---|
| `01_rocky_island_mk44391.mp4` | 44391 | Wild rocky island from the air | best opener (no buildings) |
| `01_island_aerial_mk2890/2888/5368.mp4` | 2890, 2888, 5368 | Tropical islands | 2888/2890 show resort huts and a pier, 5368 a boat: back-ups only |
| `01b_sunset_sea_mk4119.mp4` | 4119 | Sun setting over the sea | the 30 hours passing |
| `05_sea_rock_mk51506.mp4` | 51506 | Waves around a lone rock, top-down, vertical | |
| `05_cliffs_sea_mk1952.mp4`, `05_cliff_waves_mk51454.mp4` | 1952, 51454 | Rocky outcrops in surf | |
| `06b_climb_mk41045.mp4`, `06b_summit_mk43311.mp4` | 41045, 43311 | Climber on rock; sitting on a summit | 43311 has a summit cross |
| `08_bubbles_mk1273.mp4`, `08_drops_water_mk51955.mp4` | 1273, 51955 | Underwater light (vertical); a drop into water | for the ring sinking |
| `09_waves_shore_mk1925.mp4`, `09_waves_beach_mk44482.mp4` | 1925, 44482 | Waves on sand at golden hour | base for the stone heart |
| `11_programmer_mk41639.mp4`, `11_code_screen_mk41654.mp4` | 41639, 41654 | Programmer from behind; code on screens | "real work" |
| `14_lego_hands_mk42175.mp4`, `14_lego_pieces_mk42165.mp4` | 42175, 42165 | A child's hands building blocks | crop to hands (face edge in frame one) |
| `14b_dog_play_mk50688.mp4` | 50688 | Dog playing with a ball | |
| `14c_skate_park_mk34382.mp4`, `14c_skate_vert_mk1366.mp4` | 34382, 1366 | Skateboarders | trying again |
| `15_sand_mk1564.mp4` | 1564 | White sand beach, palms | for JOY in the sand |

Flow (creator, 4 of 10, all 1920×1080 landscape, 24 fps, 10 s): `02_eko_beach_flow` (dark blue lobster on wet
sand), `05b_eko_climb_flow` (red lobster climbs a pillar and falls on its back: the "first try? it failed" beat),
`10_thirteen_flow` (a line of lobsters on the shore: count them before using with "thirteen"),
`14d_eko_spire_flow` (silver robot lobster on a spire at sunset). The three Ekos look different (blue, red,
silver); cut so they never sit side by side, or ask for a re-take in one look.

The real island runs locally: Clawblox built from source, `worlds/mesa-island` served on :8280 with three.js 0.160.0
from npm, the HUD icons stubbed, and the spectator token from the server log. The paper's own recorded runs
(`data.clawblox.com/paper/replays/v1/...`) need that host allowed.

Paper: `work/pdf/paper.pdf` (arXiv 2610.07130, 6 MB). Project page: machineplaying.org (interactive replays, a
YouTube video, data on Hugging Face `nacloos/machine-playing-paper`).

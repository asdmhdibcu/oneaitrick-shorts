# Short #19: build notes

"Ten minutes". 9:16, 1080×1920, 30 fps, 59.31 s (voice 59.36 s, last word ends 59.21; the video cuts 0.1 s after "was",
so a replay runs into "TEN minutes of AI"). The first short drawn in one animated film style (hub Experiments:
"Animated film style"); the length, captions, proof card, end card, hidden word and spoken loop stay as in #18.

## The look: Lemo-Opuscar's Mid-century Cartoon

- `toon19.js` is the style's engine (Lemo-Opuscar `styles/midcentury-toon/demo/engine/toon.js` plus `drawHand` from
  `chars.js`, MIT licence, © Lemomo / LemoLab), with only the ES-module exports removed so it inlines into the page. Its
  rules: every fill printed a few px off its broken ink line and re-jittered on twos (`REG`, `setClock`), flat colour
  with dry-brush tooth, ink ribbons that breathe and break, sunbursts and 4-point sparkles, two-plate lettering,
  `paperFinish` for the paper grain and warm vignette. Nothing is built inside the library's clone (`/home/claude/ext/`).
- `film19.js` draws the whole picture on one 1080×1920 canvas, repainted from the clock alone (`PAINT`), so any frame
  can be seeked. The captions and the end card are DOM (`index_template.tpl`).
- Fonts (SIL OFL, from npm `@fontsource`): Alfa Slab One (numbers, titles), Oleo Script (kept off any line with "AI":
  in the script face it reads "Al"), Jost 500–700 (labels, captions).
- Palette: cream paper and warm ink. Mustard = the pencil, the hero; turquoise = the AI (training wheels, chat bubble,
  hint card); tomato = giving up (SKIP, the catch); olive = people who never had AI. Brand lime only on the end card.

## The story spine

- **One stage:** a mustard pencil (GRIT on its barrel, never said) riding in place on a ruled worksheet line that
  scrolls under it (`pos()`: integrated speed; it stops dead for the one silence and on "weird"; the last stretch is
  stretched so the road, the spokes, the cranks and the medallions land exactly where frame one starts). Problems pass as
  fraction medallions and get a mustard check or a tomato SKIP stamp, by chapter (`medMark`).
- **Camera** (`CAM`, `camAt`): `hook` (the claim card below), `board`, `split` (stage on the top 60%, the lower block
  y 878–1214, x 264–820, for the numbers), `zoom` (the crash zoom into the wheels at 4.77 s), `crowd` (the pull-back with
  counter-rotation to rows of pencils, 7.8–12.3 s). A 4 % punch on OFF; a 3 % push through the recap.
- **Chapter tracker** at y 258: WHEELS · WOBBLE · WHY · HINTS · TRY IT. Each chapter opens with the style's numbered disc
  that becomes a thin ink ring with an off-register mustard ring (`discIris`).
- **Pins** (`PINS`): 218×172 paper cards with a star bullet, solid fills; the colour plate while new and again in the
  recap. Left = what happened (1,222 · 57 vs 74 · 20 vs 11 · 8 vs 1), right = hints, the catch, the fix (HINTS ≈ no AI ·
  SHORT tests: a clue · HINT first, not the answer); the eighth slot becomes THE WORD? on "Comment". 1,222 counts up in a
  badge and flies into pin 1's slot.
- **Hook:** frame one shows the settled claim card (COLM 2026 · 1,222 PEOPLE / 10 MIN OF AI / GAVE UP ALMOST 2× AS OFTEN)
  with a 0.3 s bump; a "~2×" starburst stamps on TWICE. The 10's odometer runs only at the end: 00 counts up to 10
  (57.3–58.1 s) and holds into the cut, so the last frame is frame one.
- **Wheels off:** the kitchen timer runs out over the ten minutes (it reads the minutes on its face; big over the crowd);
  the one silence from "Then"; an iris closes on the training wheels; on OFF the wheel pops up, bounces once and rolls
  away behind, leaving a stub and a tomato starburst.
- **Numbers:** bars 74 vs 57 (100 % = 255 px), two 10 × 10 grids for the skips (11 vs 20, then reading 1 vs 8), bars
  76 ≈ 77 with a CLUE stamp. All values from the paper (BRIEF.md, "Facts").
- **Proof:** one sentence from the paper's limitations (p. 11), re-set from the page's own word images (`crops.py`
  REFLOW), "tested immediately after AI removal," lit and the other words dimmed, 40.1–42.6 s, pins hidden under it.
- **The fix:** the AI becomes a turquoise bubble whose gloved arm steadies the seat; the prompt "Give me a hint, not the
  answer." types itself in the lower block; on "lets go" the glove opens and the pencil rides on alone.
- **End:** an iris closes to a dark disc with a mustard edge behind the logo on "Follow" (the stage resets to frame one
  under it, 0.4 s later), and opens again for "And remember... all it took was...".

## Material

- **Voice:** the creator's ElevenLabs take (clone of their own voice), 59.36 s, v1 word for word (Whisper check, then
  `align_by_chunks.py`: 164 of 164 words). No voice effect.
- **Page:** the paper, arXiv 2604.04721 v6 (13 Oct 2026), "Published as a conference paper at COLM 2026", saved by the
  creator as a PDF (`work/pdf/`, git-ignored). The workspace can't reach arxiv.org.
- **Drawn in code:** everything else. No logos (no company is named on screen), no generated media (0 of 10 videos,
  0 of 5 images).

## Sound

- Score `make_jazz.py`: an original cool-jazz combo synthesised in numpy (vibraphone with 1:4:10 bar partials and motor
  tremolo, pizzicato walking bass, brushes, ride, finger snaps), 116 bpm swing, F major. Each chapter has its own
  vibraphone chord, and the recap brings them back one per pin. Half-time feel for the wobble, up a step for the hints,
  bass and brushes only through the catch. (The library's sample packs couldn't be fetched here, so no samples.)
- The one silence: "Then, without warning..." to OFF (12.19–14.83), voice only. A tape stop on "weird" (33.95), then
  room tone only until "People".
- Our synth hits (`sfx.json`, tools/make_sfx.py) and the style's foley synthesised in `make_audio.py`: damped rubber
  stamps, a slide whistle, pencil scratches for the crowd, the iris "shhk", the wheels' clank and rattle, a kitchen-timer
  tick while the minutes run out, odometer ticks into the loop.
- CC0 pass (`cc0.json`, 17 sounds, credits inside): the braam under the open, room tone, a stamp body, swipes for the
  wipes and the proof card, the SKIP click, the rewind for WHY, the catch impact, typing.
- Mix: `tools/mix.py … deep` (score gain 0.65, SFX 0.4). `duck_tune.py`: the score sits 14.6 dB (K-weighted) under the
  voice in words and 10.9 dB under in the pauses. Final −14.0 LUFS, −1.5 dBTP.

## Quality pass

- `npx hyperframes check`: passed. motionmaxxing `lint.mjs` (G5): passed (the end card's @oneaitrick is a WARN, brand).
- Contact sheets every 0.5 s and ±0.1 s around every cut, then an independent critic. First pass: 4 blockers, all fixed
  (frame one mid-roll and the loop's odometer jump; "2× more" overstated 20 vs 11, now "almost 2× as often" and
  "20 vs 11"; a lane label under a floor strip; pins translucent over the ground strip) plus 14 should-fix items, all
  taken (wheels-off beat, big countdown over the crowd, call-out off the timer, answer card into the glove, prompt in the
  lower block, bigger grids, bars and pins, proof card held and dimmed, iris end card instead of a dissolve, slower
  recap, level on the handlebar, caption pop on HINT only, thin disc rings, the matte's inked edge, minutes on the
  timer). Second pass: the four blockers confirmed fixed except the pins over the road; now the pin columns sit in paper
  margins with a worksheet's red margin line (`margins()`), so the road and medallions never run under a pin. Also from
  the second pass: the end count settles in 0.8 s and is clipped to its slot, the card comes back under the iris (no
  second wipe), the call-out above the back wheel with a short leader, the lower block narrowed to x 264–820, the stage
  timer moved left and hidden while the big one shows, one chart order (the AI group on the left, as in the pins), one
  highlighter sweep, a 944 px end disc, pin 6 "SHORT · tests; hints: a clue". Not taken: re-recording seconds 4–12 (the
  script is approved).
- motionmaxxing `look.py` on the MP4: gates G0, G2, G3 pass; the one silence shows as digital silence (13.86–14.15 s,
  intended); mean frame-to-frame change is low (limited animation on pale paper, as the style is).

## Rebuild

```
cp <take>.wav assets/voice_raw.wav && ffmpeg -i assets/voice_raw.wav -ac 1 -ar 16000 work/voice16k.wav
sed -E 's/\[[^]]+\] ?//g' script.txt > work/script_plain.txt
python3 whisper_chunks.py work/voice16k.wav > work/whisper_chunks.txt
python3 align_by_chunks.py work/voice16k.wav work/script_plain.txt work/whisper_chunks.txt words.json
python3 ../../tools/make_captions.py words.json captions.js "TWICE,TRAINING,WHEELS.,THOUSAND,HALF,OFF.,FEWER,SKIP,EIGHT.,INSTANT,HINTS...,HINT,COMMENT"
python3 crops.py               # the proof sentence (needs work/pdf/p01_paper_v6.pdf)
python3 make_index.py          # -> captions_final.js, index.html
python3 make_audio.py          # -> assets/mix.wav (runs make_jazz.py)
python3 ../../tools/srt_from_words.py words.json short19-captions.srt && python3 make_srt_tr.py
python3 make_cover.py          # -> short19-cover.png
HYPERFRAMES_BROWSER_PATH=<chrome-headless-shell> npx hyperframes@0.8.162 render -f 30 -q high -w 2 -o renders/short19-raw.mp4
ffmpeg -i renders/short19-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart renders/short19-ten-minutes.mp4
ffmpeg -i renders/short19-ten-minutes.mp4 -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high -level:v 4.1 -pix_fmt yuv420p -g 60 -c:a copy -movflags +faststart renders/short19-ten-minutes-phone.mp4
```

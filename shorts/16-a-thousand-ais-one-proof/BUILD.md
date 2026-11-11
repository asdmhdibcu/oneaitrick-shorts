# Short #16: build notes

"A thousand AIs, one proof". 9:16, 1080×1920, 30 fps, 97.4 s (voice 95.2 s + end card). 36 shots, a transition on
every cut, chosen by meaning (`make_index.py` SPECIAL).

## Material

- **Voice**: the creator's ElevenLabs take (clone of their own voice), word for word with `script.txt` v1. Robot preset on
  the boss's quote only ("There is no reason to idle.", 59.05–60.84 s), with `tools/voice_fx.py`.
- **Footage**: eight Pexels clips the creator downloaded (blueprint, bricklaying, inspector's clipboard, building-site
  time-lapse, desk with magnifier, drone over a site, rooftop brick wall; the engineers clip is unused). The inspector
  clip is cropped to the gloved hands and clipboard (`z=1.4`), so no face is in frame.
- **Pages**: the creator saved the three pages as PDFs from the browser. `crops.py` cuts each card or strip between two
  lines of the page and finds the highlighted phrases' boxes, so the browser's header and footer (URL, date, page number)
  never reach the video. Launch page and research page heroes are cut below the site menu.
- **Public domain**: the 1670 Arithmetica page with Fermat's note, and Fermat's portrait (Wikimedia Commons), attached
  by the creator.
- **Code**: `FinalCheck.lean` and the README from github.com/anthropics/fermats-last-theorem (Apache-2.0). The theorem is
  shown as written, re-wrapped over five lines; the `#print axioms` line shows the real output.
- **Logos**: Simple Icons (Anthropic, Claude; the Claude mark in its orange).
- **Generated media**: none (0 of 10 videos, 0 of 5 images).
- **Thinking orbs**: my own canvas drawing in the style of the thinking-orbs library (a sphere of dots that turns,
  breathes, scans or dims). The library in `library/thinking-orbs/` was not run: running its code here was refused.

## What's drawn (fx16.js)

Everything canvas is repainted from the timeline's clock (`PAINT`), so seeking to any frame is exact.
- The 1,000-orb field (40 × 25), with a lime wave on "Then they DID it".
- The building facade drawing on, the brick wall the inspector checks (magnifier, a tick on every brick, crash zoom on
  EVERY), bricks turning into aⁿ + bⁿ = cⁿ, the 1637 → 1995 timeline with the 358 counter.
- The Lean terminal, the searching orb and the ticks; the wrong brick bounced off the wall.
- 1 → 10 → 100 → 1,000 orbs; one boss orb and 999 helpers; the 60 parts as the building's wall of bricks (3 done,
  47 red, 10 to do), the 47 set aside on a pallet, the helpers streaming onto the 10, the 70-minute counter, the boss's
  quote as a big card, the helpers sent back (41 of the 47 turn lime: the run ended at 54 of 60 statements).
- The 28.7-hour counter; the finished building filling with 2,418 points of light, swept by the inspector's lens, ✓.
- The head start as the building with 60 checkpoint flags and the one-line route drawn across it.
- 47 bricks "already laid"; Anthropic's lesson as a big quote card, in its own words; the 19 reminders; the chat
  ("That can't be done." / "Keep going.").
- Logos are drawn on (outline, then fill), from the Simple Icons paths.
- Hidden word: WILES, on the 1995 card (s08, s29). Never said.

## Sound

Score `music.json` (pulse, 100 bpm) with a silence beat from "Less than thirty hours later" to the check. Our synth hits
(`sfx.json`) plus the CC0 sound pass from the `sound-effects` skill's library (`cc0.json`: 18 sounds, credits inside).
Mix: −14.0 LUFS, true peak −1.5 dBTP (`tools/mix.py`).

## Rebuild

```bash
cd shorts/16-a-thousand-ais-one-proof
mkdir -p assets/js assets/logos && cp -r ../../template/assets/{fonts,base.css,grain.png} assets/   # + gsap 3.15.1, SplitText, MotionPathPlugin (npm pack gsap@3.15)
cp ../../template/hyperframes.json . && sed 's/short05-hospital/short16-a-thousand-ais-one-proof/' ../../template/package.json > package.json
# logos: work/ext/logo_{anthropic,claude}.svg -> assets/logos/{anthropic,claude}.svg (Claude mark filled #D97757)
python3 align_by_chunks.py                       # words.json from the take (Whisper chunks + tools/align.py)
python3 ../../tools/make_captions.py words.json captions.js "DID,EVERY,YEARS,LEAN,MACHINE,MILLION,THOUSAND,TWIST,FORTY-SEVEN,TEN,IDLE,CATCH,LESSON,NINETEEN,GOING,COMMENT"
python3 ../../tools/srt_from_words.py words.json short16-captions.srt && python3 make_srt_tr.py   # + es, pt, hi, id
python3 crops.py             # page cards and strips -> work/fig (+ crops.json with highlight boxes)
python3 build_edit.py        # conform every shot -> assets/clips, assets/img
python3 make_index.py        # index_template.tpl + fx16.js -> index.html, work/cuts.json (and the "AIs" caption fix)
python3 make_audio.py        # robot FX, score, SFX, CC0 pass, mix -> assets/mix.wav (-14 LUFS)
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell HYPERFRAMES_NO_TELEMETRY=1
for r in 0,30 30,60 60,97.3; do npx --yes hyperframes@0.8.162 check --range $r --timeout 60000; done
npx --yes hyperframes@0.8.162 render -f 30 -q high -w 2 -o renders/short16-raw.mp4                      # Bash run_in_background
ffmpeg -i renders/short16-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short16-a-thousand-ais-one-proof.mp4
```

Cover: `cover16.html` (the orb field and the struck-out verdict), screenshot with Playwright to `short16-cover.png`.

## Quality pass

- Draft 1 went to an independent critic (`work/critic1.md`): "not shippable". Fixed in draft 2: the building carries
  through the middle (the wall of 60, the finished building at "passed", the head start on it); the hook moves (push,
  grey wave on the verdict, lime ripple on "DID"); the boss's quote and the lesson are big cards synced to the voice;
  every shot's graphics live in its own overlay layer (`#ov-sNN`), so whips, zooms and slides move them with the shot
  instead of reading as dissolves; washes cut down (flash 0.35, scratch 0.3, no black dip); strips fade at their edges;
  counters land on their words; captions spell the numbers the voice says.
- motionmaxxing `look.py` on draft 1: G0, G2, G3 pass; −14.0 LUFS, true peak −1.5 dBFS. Cut sync was 2 of 12, so every
  cut now gets a transient. `lint.mjs` G5 flags our brand chrome (progress bar, source chip, tag, kicker): a known clash
  (`.claude/skills/README.md`), kept.

## Notes

- `hyperframes check` passes in 30 s windows. Left: the size and sub-composition warnings (one file, as on every short),
  `#cam-s07` "escaped" (the page camera zooms on purpose), and the @ONEAITRICK handle's contrast over the light 1670 page.
- Graphics that span shots (the Lean editor s10–s11, the wall s21–s26) stay in the global layer; everything else is
  made after `shot("sNN")`, which points `el()` at that shot's overlay layer.
- Tile moves on the board are transforms only (x, y, scale from the top-left corner); left/top tweens snap to whole
  pixels under seek-by-frame capture.
- `make_captions.py` upper-cases "AIs" to "AIS"; `make_index.py` puts the lower-case s back in captions.js.

# Short #18: build notes

"The coin inside your AI". 9:16, 1080×1920, 30 fps, 56.95 s (voice 56.96 s, last word ends 56.85; the video cuts on "Because" so a
replay runs into the hook). The first short in the 45–60 s package (hub Experiments) and the first with the spoken loop.

## The story spine

- **One stage:** a balance scale on #17's grid board, with the lime thinking orb above the beam as the AI. No phone:
  the phone was #17's stage (the creator's note, 12 Nov). The stage is one canvas (`#stage`, 1620×1950 drawn at
  1080×1300) repainted from the clock (`PAINT`): beam angle, stage and orb alpha and the orb's glow are keyframe lists
  (`ANG`, `SA`, `OA`, `GLOW` in `fx18.js`), so any frame can be seeked. The TAILS coin has its own canvas (`#coinTop`).
- **Camera:** `#world` shows the whole board (`BOARD`) or pushes in (`PUSH`: scale 1.5, always the same framing) for
  the chat, the two proof cards and the question (about 13 s in all); the report stays at board scale, between the pin
  columns. Pins hide while pushed in and come back once the camera has nearly settled (`pullOut`: +0.3 s).
- **Chapter tracker** at y 232: COIN · SCALE · FOLLOW · CATCH · FIX; the live chapter fills lime, finished ones get ✓.
- **Pins:** seven fact cards in two columns (left x 30, right x 840, rows y 330–1034); each slides in along its own row
  from the scale's side, lime while new, then rests at 60%. The recap lights the left column (what the coin did) on
  "never said", the right (the catch and the fix) on "Spotted"; the eighth slot becomes THE WORD?.
- **Hook:** frame one shows the claim card (A COIN STEERED 50 EXPERTS) over the scale. Its 50 is an odometer: half a
  digit off on frame one with a vertical motion blur (SVG `feGaussianBlur` 0×16 px), settled by 0.8 s. At the end the
  card comes back reading 50 and spins up only in the last 0.49 s, reaching frame one's speed (46 digits/s) on the
  last frame, so the loop is seamless.
- **Split:** for the 86% the stage shrinks to the top 60% and the chart takes the bottom 40% (four bars against a
  dashed CHANCE 50% line, the 86% counting up).
- **Proof:** three complete sentences from the Anthropic post on frosted glass, no pan: `crops.py` (REFLOW) cuts each
  word from the page's own pixels and re-sets the line breaks so the sentence fits the card large. The Anthropic logo
  draws on (outline, then fill) on both proof cards and on the hook's chip.
- **Keyword pops** on the first ONE, ONE (side), OWN, HEAVY (amber), 86, OTHER, YOURS and YOU'D (lime): the word
  bounces on a coloured box (`POPS`). Caption chunks keep a number with its unit ("86 PERCENT", "1 IN 7") and a phrase
  in one piece (`REGROUP` in `make_index.py`).
- **Threat colours:** lime and blue for the fair options and the AI doing its job; amber for the planted coin and the
  catch (amber frame edges from "The catch?" to "push less").

## Material

- **Voice:** the creator's ElevenLabs take (clone of their own voice), 56.96 s, word for word with `script.txt` v2
  (Whisper check, then `align_by_chunks.py`: 163 of 163 words). No voice effect.
- **Page:** the Anthropic post, saved by the creator as a PDF (`work/pdf/`, git-ignored). The workspace can't reach
  anthropic.com.
- **Logo:** Anthropic from Simple Icons 16.37 (CC0).
- **Drawn:** the scale, the orb, the coins, the choice card, the chat, the chart, the report, the message field, the
  pins, the cover.
- **Generated media:** none (0 of 10 videos, 0 of 5 images).

## Sound

- Score `music.json` (pulse, 100 bpm, D minor). The one silence: once the four bars have landed (15.9 s) the score and
  every SFX drop to nothing, leaving only "...coin's side", and slam back on EIGHTY-SIX (16.6 s) with the impact.
- Our synth hits (`sfx.json`): new in `tools/make_sfx.py` for this short: `sub` (the sub-bass hit under the first
  0.5 s), `clink` (a coin on metal: the coin landing, the four flicks, each coin on a pan) and `creak` (the beam
  tilting). Odometer ticks at the start and from 54.9 s to the end, so the loop is seamless.
- CC0 pass (`cc0.json`, 29 sounds, credits inside): a low braam under the open, UI clicks and blips on the chat, drop
  thunks on the pans, the record scratch, page swipes on the proof cards, typing under the question, chimes on the
  recap.
- Mix: `tools/mix.py … deep` (new for #18, MOTION.md "Sound"; threshold 0.03, ratio 2.5, attack 20 ms, release
  800 ms, score gain 0.65), tuned over two critic passes with `duck_tune.py` (K-weighted, BS.1770): the score sits 14.3 dB
  under the voice in words and 8.0 dB under in the pauses, a 6.4 dB swing, so the bed is heard on a phone and doesn't
  pump (the first "deep" setting, ratio 20, left it 24 dB under and swelling 14 dB at every breath). SFX about 12–14 dB
  under the voice; the HEAVY thud is 6 dB down so it doesn't mask the word. Final −14.0 LUFS, true peak −1.5 dBTP.
  `make_audio.py` pads the mix 0.1 s (loudnorm drops the last block).

## Rebuild

```bash
cd shorts/18-the-coin-inside-your-ai
mkdir -p assets/js assets/logos assets/pages && cp -r ../../template/assets/{fonts,base.css,grain.png} assets/   # + gsap 3.15 (npm pack gsap@3.15)
cp ../../template/hyperframes.json . && sed 's/short05-hospital/short18-the-coin-inside-your-ai/' ../../template/package.json > package.json
# logo: Simple Icons anthropic.svg -> assets/logos/
cp <take>.wav assets/voice_raw.wav && ffmpeg -i assets/voice_raw.wav -ac 1 -ar 16000 work/voice16k.wav
python3 whisper_chunks.py work/voice16k.wav > work/whisper_chunks.txt
python3 align_by_chunks.py work/voice16k.wav work/script_plain.txt work/whisper_chunks.txt words.json
python3 ../../tools/make_captions.py words.json captions.js "50,ONE@2.93,KNEW,SECRETLY,SCALE,EIGHTY-SIX,HALF,ALREADY,SWITCHED,CREDIT,CATCH?,OWN,HEAVY,OTHER,YOURS,COMMENT"
python3 ../../tools/srt_from_words.py words.json short18-captions.srt && python3 make_srt_tr.py   # + es, pt, hi, id
python3 crops.py             # page cards -> assets/pages + crops.json (needs work/pdf/p01_anthropic_post.pdf)
python3 make_index.py        # index_template.tpl + fx18.js -> index.html (and the caption number fixes)
python3 make_audio.py        # score, SFX, CC0 pass, mix -> assets/mix.wav
npx hyperframes render -f 30 -q high -w 2 -o renders/short18-raw.mp4    # Bash run_in_background, watched
ffmpeg -i renders/short18-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short18-the-coin-inside-your-ai.mp4
ffmpeg -i renders/short18-the-coin-inside-your-ai.mp4 -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high \
  -level:v 4.1 -pix_fmt yuv420p -g 60 -c:a copy -movflags +faststart renders/short18-the-coin-inside-your-ai-phone.mp4
```

Cover: `cover18.html` (the scale tipped by the AI's coin, three pins, "A coin steered 50 experts."), screenshot with
Playwright to `short18-cover.png`.

## Quality pass

- Draft 1 (15 fps draft render, `renders/short18-draft-mix.mp4`) went to an independent critic (`work/critic1.md`):
  "one more pass". Fixed in draft 2:
  - coin chapter: the terminal panel is gone; one plain chat exchange ("A or B: which is better?" / "I'd pick B.")
    holds 2.5 s; "And a coin" gets a flip, a clink and a whoosh; the card says COIN FLIP → THE AI'S PICK with
    CHOICE 1–4 (no OUTCOME / METHOD / FARMS / WEIGHTING jargon, also on the chart and the report); its cells sit at
    fixed spots, so the rings and the coin's hops land on them, and the picked cell turns amber;
  - proof cards: complete sentences, re-set from the page's own words, no pan and no cut word; card 2 is "running
    Claude Opus 4.8" (no Claude Code jargon); the "deliberately strengthened" card is two lines, large;
  - the report stays at board scale between the pin columns (pins up 9.9–40.4 s); its threads run down its left
    margin instead of through the text; no full-frame flash on the record scratch; the report pushes in slowly;
  - MY PICK floats above its pan (it covered the A block, then the coin); the 60% counter says "switched sides";
    pins rest at 85%, "1 IN 7" gets word spacing, "38 cases" moves into pin 3's label, pin 6 reads HEAVY / on purpose,
    in 1 test; THE WORD? fits its pin;
  - the question wraps onto two lines inside its field (it ran under the send button);
  - the end card sits over the mirrored first frame (board at 55%), the Follow pill is centred (a `base.css` rule had
    pinned it at x 72, y 1240); the 50 holds after the end card and spins only in the last 0.49 s; the file is 56.95 s;
  - sound: the score is audible (gain up 7.5 dB, slower release), a real drop-out before 86%, the HEAVY thud 6 dB down,
    quiet cues raised (coin spin, threads, highlights, typing), new hits on the chat, the flip, the strip and YOU'D;
  - captions: numbers stay with their units; four more keyword pops.
- Not taken: the critic asked for 5 pins instead of 7 and no push-ins at all; the 7 pins carry the story's numbers and
  the push-ins are the #17 format (board on screen about 75% of the time).
- Draft 2 (final-quality render) went to a second, verifying critic (`work/critic2.md`): "one more pass", five blockers,
  all fixed for the final render:
  - the silence wasn't heard (the bar pops filled it and the bed was already buried): the bars now land by 15.9 s and
    music and SFX go to zero until 86; the duck above replaced the pumping one;
  - the choice rings sat off their cells: they now live inside the card, 6 px around each cell;
  - captions split "STEERED 50 / EXPERTS": now "A COIN FLIP / STEERED / 50 EXPERTS";
  - proof card 2 was a fragment ("running Claude Opus 4.8"): now the page's two complete limitation sentences ("We
    studied one task, in one field, with one model. … the agent ran on Claude Opus 4.8."), "with one model." lighting
    on "tested", "ran on Claude Opus 4.8." on "OWN", plus a chip CLAUDE = THEIR OWN AI; the "deliberately
    strengthened" card got the Anthropic mark;
  - also: the end card's mirror brighter (board at 80%), the claim card enters after the end card has gone, quiet
    cues raised (AI HELPER click, three shimmers, THE WORD?), a whoosh on pin 3.
- Frame one: the first final render showed every chapter lit on frame 0 only. GSAP reverts a zero-duration `tl.set` at
  exactly 0 when the renderer seeks back to frame 0, so frame-one states (tracker, camera, page highlights, logo
  outlines, card origins) are now set on the DOM with `gsap.set`, and the canvases are painted once at load.

- Cut check (frames ±0.1 s around 22 cuts, `work/cutsA.png`, `work/cutsB.png`), fixed before the draft:
  - frame one read as a clean wrong number ("38"): the odometer now starts half a digit off with a vertical motion blur;
  - both proof cards ran off the frame's right edge while pushed in (their slow 6% push): 650 px wide, 4% push;
  - the 86% touched its label; the report and the limitation strip overlapped the pin columns: narrowed to fit between
    them; the dimmed chat behind the choice card fades out completely;
  - pins faded back in while the camera was still pushed (half off the frame's left edge): now +0.3 s.
- `hyperframes check`: passed; the size and sub-composition warnings stay (one file, as on every short). Occlusion
  notes come from the full-frame coin canvas (transparent) and the odometer's hidden digits.
- motionmaxxing `lint.mjs` G5: brand chrome only (tracker, tag, handle, progress bar), the known clash
  (`.claude/skills/README.md`), kept.

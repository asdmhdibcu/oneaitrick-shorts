# Short #17: build notes

"Your mom's voice, for sale". 9:16, 1080×1920, 30 fps, 81.5 s (voice 78.95 s + end card). The first short in the
**story-spine** format: one stage for the whole short instead of 36 separate shots.

## The story spine

- **One stage:** the viewer's phone, in the middle of a grid board. The phone is designed at 1000 × 2140 (its own
  pixels) and sits on the board at 0.4. The camera (`#world`) either shows the whole board or pushes in to 2.5, where
  the phone screen is 1:1 and fills the frame (`PUSH(dy)` puts design row `dy` at frame y 300). `CLOSE` (1.32) is used
  once, for the mirror call.
- **Screens** (`scr(id)`) live inside the phone and swap with a transition chosen by meaning: page turn for real pages,
  slide or feed swipe ("up") for the phone moving on, cut + flash for the record scratch and the crash zoom, fade for
  the match cut (Mom's voice waveform is the same 24 bars that become the key's teeth).
- **Chapter tracker** at y 232: CALL · COPY · MARKET · BANK · LOCKS; the live chapter fills lime, finished ones get ✓.
- **Pins:** seven fact cards parked beside the phone (left column: chapters 1–3; right column: 4–5). Each lands big in
  the middle of the board and drops into its slot, and stays to the end. Pins 1, 3 and 4 (Hiya, NordVPN) get a
  SELLS PROTECTION stamp on the catch. The recap lights them in story order; the eighth slot becomes "THE WORD?".
- **Mirror:** the last call is the first call again (same screen), answered with the safe word.
- **Holds:** every shot is on screen at least 2 s; changes come one at a time.

## Material

- **Voice:** the creator's ElevenLabs take (clone of their own voice), 78.95 s, word for word with `script.txt` v1
  (Whisper check, then `align_by_chunks.py`: 229 of 229 words). No voice effect.
- **Pages:** saved by the creator from Safari Reader as PDFs (`work/pdf/`, git-ignored); `crops.py` cuts each card
  between two lines and finds the highlight boxes.
- **Logos:** ElevenLabs and NordVPN from Simple Icons (CC0), drawn on (outline, then fill); Hiya from the creator.
- **Drawn:** the call screens, the key (canvas, from the waveform), the door, the scanner, the voice notes, the chart (7.4×), the login card and price tag, the bank call,
  the deadbolt, the padlocks, the comments sheet.
- **Footage:** your Pexels clip of a key being cut (video 8322146, no faces), on the phone in shot 7 under the FOR SALE
  tag (`assets/clips/v01_key.mp4`, git-ignored).
- **Generated media:** none (0 of 10 videos, 0 of 5 images).

## Sound

Score `music.json` (pulse, 92 bpm, minor) that falls silent for the mirror call ("Now your phone rings" to the recap),
so only the ring is heard. Our synth hits (`sfx.json`: rings, whooshes on camera moves, pops on pins, ticks on
counters, booms on stamps) plus the CC0 sound pass (`cc0.json`: 31 sounds, room tone under both calls, credits inside).
Mix: −14.0 LUFS, peak −1.4 dBFS (`tools/mix.py`).

## Rebuild

```bash
cd shorts/17-your-moms-voice-for-sale
mkdir -p assets/js assets/logos assets/pages && cp -r ../../template/assets/{fonts,base.css,grain.png} assets/   # + gsap 3.15 (npm pack gsap@3.15)
cp ../../template/hyperframes.json . && sed 's/short05-hospital/short17-your-moms-voice-for-sale/' ../../template/package.json > package.json
# logos: Simple Icons elevenlabs.svg (#000) and nordvpn.svg (#4687FF) -> assets/logos/; hiya.png from the creator
cp <take>.wav assets/voice_raw.wav && ffmpeg -i assets/voice_raw.wav -ac 1 -ar 16000 work/voice16k.wav
python3 whisper_chunks.py work/voice16k.wav > work/whisper_chunks.txt
python3 align_by_chunks.py work/voice16k.wav work/script_plain.txt work/whisper_chunks.txt words.json
python3 ../../tools/make_captions.py words.json captions.js "ONE@0.39,MOM@6.42,NOW,KEY@11.51,THIRTY,MINE,SALE,SEVEN,TEN,TWIST,BANK,LOCK,CATCH,PROTECTION,SAFE,NEVER@63.48,WORD@71.09,COMMENT"
python3 ../../tools/srt_from_words.py words.json short17-captions.srt && python3 make_srt_tr.py   # + es, pt, hi, id
python3 crops.py             # page cards -> assets/pages + crops.json
python3 make_index.py        # index_template.tpl + fx17.js -> index.html (and the CAPS number fix in captions.js)
python3 make_audio.py        # score, SFX, CC0 pass, mix -> assets/mix.wav
npx hyperframes render -f 30 -q high -w 2 -o renders/short17-raw.mp4    # Bash run_in_background, watched
ffmpeg -i renders/short17-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short17-your-moms-voice-for-sale.mp4
ffmpeg -i renders/short17-your-moms-voice-for-sale.mp4 -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high \
  -level:v 4.1 -pix_fmt yuv420p -g 60 -c:a copy -movflags +faststart renders/short17-your-moms-voice-for-sale-phone.mp4
```

Cover: `cover17.html` (the phone ringing Mom, three pins and the FOR SALE tag), screenshot with Playwright to `short17-cover.png`.

Rendered 12 Nov: 81.46 s, 1080×1920, 30 fps, −14.0 LUFS, peak −1.3 dBFS (master 306 MB, phone copy 115 MB). The
render took about 35 min on 2 CPUs (capture ~15 min, encode ~20 min at `-q high`).

## Quality pass

- Draft 1 went to an independent critic (`work/critic1.md`): "not shippable", 12 findings. Fixed in draft 2:
  - the board is the default view, on screen within the first 5 s; the camera pushes in only for the two calls, the real
    pages and the chart, always to one framing (`DY` 240), with the status bar and pins hidden while pushed in;
  - frame one is the mirror frame: the phone at board scale ringing MOM, the claim on a solid card over its lower half;
  - chapter 1 is lit on frame one; chapter 4 waits for "BANK" instead of giving the twist away;
  - pins: no index or source line, 72 px numbers and 30 px labels, lime only while new, 60 % at rest; they slide out of
    the phone's edge along their own row (never across another pin); labels keep the voice's hedges ("say", "$10+");
  - the MANGO payoff holds 2 s (to "I never said"); the recap lights the left column (the attack) then the right
    (the locks); the board fades to 10 % and blurs under the end card;
  - hits flash inside the phone only (no full-frame grey); "isn't Mom" strikes the Mom card and the #1 badge moves to the
    bank's avatar; the catch points at pins 1, 3, 4 before stamping them; the key stops at the keyhole; 0:30 on THIRTY;
    the chart carries its source.
- Final check before the render: the call buttons fade as the camera pushes in (pushed in, they sat half off the frame's
  bottom edge); the cover lost the comma that touched "SALE" and its first pin keeps the hedge ("say a fake voice called
  them"). Frames pulled from the MP4 every 2.5 s and ±0.1 s around seven cuts.
- motionmaxxing `lint.mjs` G5: brand chrome only (see Notes).

## Notes

- `hyperframes check`: the size and sub-composition warnings stay (one file, as on every short). Layout notes about
  pins "overflowing" come from the camera push (the board is bigger than the frame on purpose).
- motionmaxxing `lint.mjs` G5 flags the brand chrome (progress bar, tag, tracker, chips): the known clash
  (`.claude/skills/README.md`), kept; the tracker is the creator's own ask.
- GSAP owns every transform (no CSS `transform` on animated elements): the phone's 0.4, the tracker fills, the
  highlight bars and the stamps are all set on the timeline at t = 0.
- Canvases (waveforms, key, chart counters) are repainted from one clock tween (`PAINT`), so any frame can be seeked.

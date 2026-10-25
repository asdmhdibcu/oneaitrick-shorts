# Short #10 — "The invisible signature" (build)

86.6 s, 30 shots. ChatGPT now watermarks the text it writes for users in the EU (OpenAI Help Center); Claude marks its
newer models' text worldwide, the UK included, and text it only translated can carry the mark (Claude Help Center). One
picture runs through it: a secret, loaded coin makes every small word choice ("big" or "large"), and hundreds of
choices that follow the coin are a signature. Script, checked facts and sources: `BRIEF.md`. Voice: ElevenLabs v4,
recorded 24 Oct (84.4 s), aligned word by word (all 217 words).

`assets/`, `work/` and renders are git-ignored. Rebuild:

```bash
cd shorts/10-the-invisible-signature
cp -r ../../template/assets/fonts ../../template/assets/grain.png ../../template/assets/base.css assets/
mkdir -p assets/js assets/img && cp ../../template/assets/js/gsap.min.js assets/js/
# d3 7.9.0, topojson-client 3.1.0, world-atlas 2.0.2 and @fontsource/caveat 5.0.8 from npm:
#   cp node_modules/d3/dist/d3.min.js assets/js/; land-50m -> assets/js/land.js (window.LAND = GeoJSON);
#   cp node_modules/@fontsource/caveat/files/caveat-latin-700-normal.woff2 assets/fonts/caveat-700.woff2
# the voice: ffmpeg -i ElevenLabs.wav -ar 48000 -ac 1 work/voice_clean.wav; -ar 16000 -ac 1 work/voice16k.wav
python3 ../../tools/align.py work/voice16k.wav work/script_plain.txt words.json     # script.txt without the [tags]
for d in r1_openai r2_claude; do python3 pdfwords.py work/pdf/$d.pdf work/pdf/$d.words.json; done
python3 make_pages.py --sheet          # highlighted crops of OpenAI's page -> assets/pages (+ pdfimages -f 9 -l 9: the chart)
python3 build_edit.py                  # conform every shot (edl.py) -> assets/clips, work/meta.json (~30 min, 4K sources)
python3 prep_words.py && python3 ../../tools/make_captions.py work/words_cap.json captions.js "$(cat work/emph.txt)"
python3 ../../tools/srt_from_words.py work/words_cap.json short10-captions.srt && python3 prep_words.py --srt
python3 make_audio.py                  # music10.py score + sfx.json + mix -> assets/mix.wav (-14 LUFS)
python3 make_index.py                  # index_template.tpl -> index.html
npx hyperframes render -f 30 -q high -w 2 -o renders/short10-raw.mp4
ffmpeg -i renders/short10-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short10-the-invisible-signature.mp4
```

## What's in it

- **Flow (7 clips of the 10 allowed, no images):** a UV torch revealing a glowing signature, a loaded coin on an X-ray
  light box, a document examiner, a phone scanning a handwritten card (3.3-5.5 s only: after that its screen fills with
  made-up text), a teacher and a padlocked laptop, a stamp that leaves no mark, a student who types and then writes.
- **Stock (Pexels):** hands on a laptop in the dark (frame one and the loop at the end), two keyboards, a euro coin
  tumbling, a man with a magnifier, a pen writing, the EU flag, the Champs-Élysées and the Arc de Triomphe, Big Ben.
- **Real pages:** three highlighted crops of OpenAI's help page (no hidden characters; the 69.0% / 42.2% line; student
  work out of scope). Claude's help page came as a small-type copy, so its three quotes are set large, word for word,
  labelled "QUOTED · CLAUDE HELP CENTER".
- **Data:** OpenAI's detection chart (24 EU languages, at 1% false positives), redrawn as an animated vertical bar chart
  from the published figure: bar heights read off the image and calibrated on the two stated values (Spanish 69.0,
  Romanian 42.2). The boost OpenAI gave languages under 60% is drawn as on their chart (Romanian to about 59%).
- **My graphics:** the claim title on frame one with a half-written signature; Europe's 12 stars; word slots that flip
  BIG/LARGE and START/BEGIN and then lock where the coin lands; a "could be chance → signature" meter over a page whose
  coin-picked words light up; copy / paste / screenshot copies that all keep the signature; the signature dissolving into
  the lit words; a spinning globe (Natural Earth) with signatures popping up on every continent, the UK last; stamps
  ("CHEATED?", "HUMAN?") that won't stick; a handwritten "Written with help from AI." note.

## New this time

- **A signature generator** (`sigD` in the template): a prolate trochoid with a tall first loop and an underline
  flourish, drawn on with `pathLength=1` dashes. Every signature in the short is the same hand, so it reads as one mark.
- **A chart redrawn from a published figure**, with the measurement in `work/chart_data.json`.
- **A globe** drawn per frame on a canvas with d3's orthographic projection from Natural Earth land (world-atlas).
- **One silence:** the score (an original mystery cue, `music10.py`) stops dead on "Here's the twist" under a record
  scratch that greys the chart, and crashes back in on "TRANSLATED".

## Gotchas

- Zero-length `tl.set(...)` at exactly 0 s revert when a renderer seeks back to 0: frame one lost its half-drawn
  signature. Start states that must show on frame one are a `fromTo` from 0; everything else starts hidden by inline style.
- Tweens that flicker an overlay must stop before the overlay's fade-out, then get a hard `set` to 0 after the shot:
  London's dashed line and the "CHEATED?" stamp otherwise stayed on to the end card.
- `pkill -f name` also matches the shell running it: run it on its own.
- A `.js` helper next to the short's `package.json` ("type": "module") must be `.cjs` to use `require`.

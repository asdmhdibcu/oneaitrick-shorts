# Short #14: "An AI was told it had no internet. It did." (build)

1:19, 30 shots, 1080×1920, 30 fps, −14 LUFS. The creator's ElevenLabs take (76.6 s, 231 words) aligned word by word.
Story and every number from one primary source: Anthropic, PBC, Form S-1 (SEC, filed 26 Oct 2026), Risk Factors, p. 48.
Hidden word: **UNLOCKED**, on the gate post in s10 and s27; never said.

## Material

- **The filing itself.** The S-1's HTML from sec.gov (fetched with a User-Agent naming the channel, as the SEC asks),
  rendered page by page in headless Chromium (no browser chrome, no ads). `work/fig/s1_cover.png` and `s1_p48.png`
  at 3× scale, plus each line's position (`s1_p48_lines.json`). `make_excerpts.py` cuts word-exact crops of the
  passage and stacks them into cards (`ex_inet`, `ex_four`, `ex_abort`, `ex_worst`, `ex_noev`) big enough to read on a
  phone. The cover card is cropped above the names and addresses.
- **Logos**: Anthropic wordmark and Claude logo from Wikimedia Commons (SVG, rendered to PNG for the composition).
- **Stock**: Mixkit (typing, clock, office at night, hourglass, sticky notes; Mixkit Stock Video Free License, every
  "Restricted" clip skipped), Coverr (stock-market screen, cable into router, router; Coverr licence, no AI clips),
  Pexels (gate 4169291, door 14861584, keys 7986204; from the creator).
- **Flow**: 2 of 10 (four robots through a gate; a robot at a desk). The desk clip is six takes cut together (cuts at
  1.46, 3.42, 5.08, 6.58, 8.29 s); every shot stays inside one take.
- **Missing, replaced**: no server-room or driving-school clip arrived; s03 uses the typing clip with ACCESS GRANTED,
  s09 is a drawn test town (MotionPath car through cones).
- The gate clip racks focus: only 8.5–15.5 s and 25.5–28 s are sharp, so both gate shots sit there.

## Rebuild

```bash
cd shorts/14-four-ais-got-out
mkdir -p assets/js && cp -r ../../template/assets/{fonts,base.css,grain.png} assets/   # + gsap 3.15 and its plugins (as #13)
python3 ../../tools/align.py work/voice16k.wav work/script_plain.txt words.json
python3 ../../tools/make_captions.py words.json captions.js "INTERNET@1.86,DID,REAL@5.6,FOUR,THIRTY-FOUR,IMPOSSIBLE,STOP,PASSWORD,BOSS,TWIST,ESCAPE,DETERMINED,KEYS"
python3 ../../tools/srt_from_words.py words.json short14-captions.srt && python3 make_srt_tr.py   # + es, pt, hi, id
python3 -I make_excerpts.py  # S-1 excerpt cards -> work/fig/ex_*.png
python3 build_edit.py        # conform every shot -> assets/clips, copy the S-1 cards to assets/img
python3 make_index.py        # index_template.tpl + fx14.js -> index.html, work/cuts.json
python3 make_audio.py        # score + SFX + mix -> assets/mix.wav (-14 LUFS)
npx hyperframes render -f 30 -q high -w 2 -o renders/short14-raw.mp4                       # Bash run_in_background
ffmpeg -i renders/short14-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short14-four-ais-got-out.mp4
```

Cover: `cover14.html` (a frame of the Flow gate clip as `assets/img/cover_bg.png`), screenshot at 1080×1920 with
Playwright (node; the python package isn't installed here) -> `short14-cover.png`.

## Notes

- `tools/overlay_audit.py` needs python Playwright, which this workspace lacks; the same check ran through node
  Playwright. The only long-lived overlays are the two gate signs (inside their shots, hidden with them) and the strike
  line (zero width until s23).
- `hyperframes check` in two windows (0–40, 40–78.8, `--timeout 120000`): passes. Info only: the glass doors in s07b
  start off-canvas on purpose.

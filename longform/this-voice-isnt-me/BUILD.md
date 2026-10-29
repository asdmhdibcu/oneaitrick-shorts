# #12 video: "This voice isn't me" (build)

16:9 YouTube video, 7:39, 86 shots, plus a 9:16 Short and a Trial Reel cut from it (`shorts/12-this-voice-isnt-me/`).
Five hidden dangers inside everyday AI (your secrets, fairness, your eyes, a voice you trust, your judgment) and four
habits, told through one picture: AI is a brilliant stranger who has moved into your phone. The narrator is an
ElevenLabs clone of the creator's own voice, which is the hook: "The voice you're hearing right now... isn't me."
Recorded 27 Oct (7:36, 1,272 words, all matching the script); a separate take holds T1 (the hidden-word line and
"Follow") and T2 (the Trial Reel's opening). The hidden word is **Marmalade**, on the safe-phrase card (never said).

`assets/`, `work/` and renders are git-ignored. Rebuild:

```bash
cd longform/this-voice-isnt-me
cp -r ../../template/assets/fonts ../../template/assets/grain.png assets/ && mkdir -p assets/js && cp ../../template/assets/js/gsap.min.js assets/js/
sed 's/width: 1080px; height: 1920px/width: 1920px; height: 1080px/g' ../../template/assets/base.css > assets/base.css
ffmpeg -i work/raw/voice_main.wav -ar 48000 -ac 1 work/voice_clean.wav && ffmpeg -i work/voice_clean.wav -ar 16000 work/voice16k.wav
python3 ../../tools/align.py work/voice16k.wav work/script_plain.txt words.json && python3 make_srt.py
for f in work/pdf/*.png; do tesseract $f work/ocr/$(basename $f .png) --psm 3 tsv; done   # PDFs have no text layer: 200 DPI
python3 make_pages.py                  # highlighted crops of the PDFs, screenshots and page recordings -> assets/pages
python3 make_logos.py                  # official logo files (SVG via Playwright) -> assets/logos
python3 build_edit.py                  # conform every shot (edl.py) -> assets/clips (~2 h on 2 CPUs; SKIP_EXISTING=1 resumes)
python3 make_index.py                  # index_template.tpl + fx_shots.js -> index.html, work/cuts.json
python3 make_audio.py                  # music12.py score (plan_video.json) + sfx.json + mix -> assets/mix.wav (-14 LUFS)
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell
HF_CAPTURE_PARALLEL_STREAM=true npx hyperframes render -f 30 -q high -w 2 -o renders/video12-raw.mp4   # Bash run_in_background
ffmpeg -i renders/video12-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/video12-this-voice-isnt-me.mp4
ffmpeg -i renders/video12-this-voice-isnt-me.mp4 -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high \
  -level:v 4.1 -pix_fmt yuv420p -g 60 -c:a copy -movflags +faststart renders/video12-this-voice-isnt-me-upload.mp4
```

The thumbnail, the Short's cover and the Instagram carousel come from `shorts/12-this-voice-isnt-me/make_pack.py`.

## Material

- **Real pages:** OpenAI's outage post, Forbes (Samsung), Reuters (Amazon), the ICO's automated-decisions guidance
  (PDFs, 200 DPI + tesseract); Reuters Fact Check (Pentagon image), Starling Bank, the FTC, CNN x2 (page recordings,
  2x before OCR); the RNC ad (a frame). AP's Pentagon story couldn't be opened, so it is a cited chip on the Reuters page.
  The High Court judgment site was unreachable: a quote card with the verified text and its citation.
- **Screen recordings:** ElevenLabs (the voice chip's name blurred), ChatGPT's Data controls (#11's recording),
  ChatGPT asked for sources (tone-mapped HDR). Recordings that showed private chats are never used.
- **Flow (6 new + 2 from #11):** the stranger, the CV sorter, fake proof, the voice, the call, autopilot; postcards and
  the sorting office.
- **Stock (Pexels, 20):** creators listed in `work/raw/credits.csv` and the YouTube description.

## Gotchas

- p7's first frames are Google's AI Overview, not Starling: only frames 13+ (the press release) are used.
- `"F": "flow"` in DEFAULT_GRADE: the #11 Flow clips keep their codes.
- `make_audio.py` reads work/cuts.json: run it after every `make_index.py`.
- A 7:39 render with 2 workers wants ~29 GB of frame files on disk; `HF_CAPTURE_PARALLEL_STREAM=true` streams them to the
  encoder instead (the workspace had 15 GB free).
- `hyperframes check` never finishes its runtime pass on this composition, even in 60 s windows: the review is the
  contact sheets plus `tools/overlay_audit.py`.

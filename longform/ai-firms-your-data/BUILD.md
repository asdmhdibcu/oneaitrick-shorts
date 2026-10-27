# #11 video: "What AI firms just promised about your data" (build)

16:9 YouTube video, 3:40, 61 shots, plus a 9:16 Short cut from it (`shorts/11-ai-firms-your-data/`). The ICO's 8 Oct 2026
report on the 11 biggest foundation-model developers, told through one picture: every public post is a postcard, and AI
training is a sorting office reading billions of them. Voice: ElevenLabs v4, recorded 25 Oct (3:35); the "First thing…"
lines were re-recorded 27 Oct (`splice_fix.py`) because the report gives "benefitting humanity" as an example of a
too-broad reason, not as something a firm said.

`assets/`, `work/` and renders are git-ignored. Rebuild:

```bash
cd longform/ai-firms-your-data
cp -r ../../template/assets/fonts ../../template/assets/grain.png assets/ && mkdir -p assets/js && cp ../../template/assets/js/gsap.min.js assets/js/
sed 's/width: 1080px; height: 1920px/width: 1920px; height: 1080px/g' ../../template/assets/base.css > assets/base.css
# the voice: ffmpeg -i ElevenLabs.wav -ar 48000 -ac 1 work/voice_clean_v1.wav, then the 27 Oct take as work/raw/voice_v2.wav:
python3 ../../tools/align.py work/fix16k.wav work/fix.txt work/fix_words.json && python3 splice_fix.py
python3 ../../tools/align.py work/voice16k.wav work/script_plain.txt words.json && python3 make_srt.py
for f in work/raw/*image.*; do tesseract $f work/ocr/$(basename $f | cut -c1-8) --psm 3 tsv; done
python3 make_pages.py --sheet          # highlighted crops of the screenshots and PDFs -> assets/pages
python3 make_logos.py                  # the creator's official logo files -> assets/logos
python3 build_edit.py                  # conform every shot (edl.py) -> assets/clips (4K sources: ~30 min on 2 CPUs)
python3 make_index.py                  # index_template.tpl + fx_shots.js -> index.html, work/cuts.json
python3 make_audio.py                  # music11.py score (plan from the cuts) + sfx.json + mix -> assets/mix.wav (-14 LUFS)
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell
npx hyperframes render -f 30 -q high -w 2 -o renders/video11-raw.mp4      # Bash run_in_background, ~45 min
ffmpeg -i renders/video11-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/video11-ai-firms-your-data.mp4
# the master is ~1.1 GB: deliver the upload copy (README phone-copy settings, ~0.3 GB)
ffmpeg -i renders/video11-ai-firms-your-data.mp4 -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high \
  -level:v 4.1 -pix_fmt yuv420p -g 60 -c:a copy -movflags +faststart renders/video11-ai-firms-your-data-upload.mp4
python3 shot.py thumb11.html video11-thumbnail.png 1280 720            # Playwright screenshot of the thumbnail
```

## Material

- **Real pages:** the ICO report (PDF, 33 pages; 15 highlighted crops), the ICO news release and call for evidence
  (screenshots), Meta's generative AI page (screenshots), OpenAI's removal and data-controls help pages and Apple's Applebot
  page (Safari prints). Words are found with pdftotext -bbox or tesseract; the camera finds each highlight on its word.
- **Screen recordings (creator's phone, HDR):** tone-mapped at 125 nits, cropped to the app, retimed with key pairs
  (`keys` in edl.py). Private frames (chat titles, email, profile photo) are cut or blurred.
- **Flow (5 of 10):** the knock, posts become postcards, the sorting office, a postcard dissolving, a robot hand through
  lasers. All vertical: set in the middle of the frame over their own blur (`mode="box"`).
- **Stock (Pexels, 10):** London, a sofa, a phone scrolling, a postcard, wrist tape, a church, a ballot, Parliament, a
  demolition, a parcel sorter. **Demo:** 2 s of xAI's Grok Bot video on X, credited.
- **No expert clips:** the parliamentlive/YouTube files were too big; the ICO speaks through its own pages and Nevinson's
  quote card.

## Gotchas

- A page's logo badge sits in the UI layer, not on the card: the camera zoom pushed it off the frame.
- `nohup … &` from a Bash call dies with the call (`render_cancelled_parent_exited`): render with run_in_background.
- The Short's `edl.py` imports the video's `edl.py` by path (importlib): `import edl` would import itself.

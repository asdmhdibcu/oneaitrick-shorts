# Short #11: "10 AI firms just changed how they handle your data" (build)

1:28, 29 shots, cut from the #11 video (`longform/ai-firms-your-data/`): eight parts of the long take (`cut_voice.py`) and
the creator's separate "Follow for more AI, explained like this." The result comes first: "Ten of the biggest AI companies
in the world just changed how they handle your data." Then the postcard, the sensitive-data finding, the ten logos, the
twist (a trained model can't un-read your post), the missing name (xAI, under investigation) and one thing to do (switch
off training in ChatGPT).

Everything visual comes from the video's folder: the material table (`edl.py` loads the video's `edl.py` by path), the
page crops and the logos (copied into `assets/`). `assets/`, `work/` and renders are git-ignored. Rebuild:

```bash
cd shorts/11-ai-firms-your-data
mkdir -p assets/img && for d in pages logos fonts js; do cp -r ../../longform/ai-firms-your-data/assets/$d assets/; done
cp ../../longform/ai-firms-your-data/assets/grain.png assets/
sed 's/width: 1920px; height: 1080px/width: 1080px; height: 1920px/g' ../../longform/ai-firms-your-data/assets/base.css > assets/base.css
python3 cut_voice.py                   # the Short's voice and words.json from the long take
python3 ../../tools/make_captions.py words.json captions.js "$(cat work/emph.txt)"
python3 build_edit.py                  # conform every shot (9:16) -> assets/clips
python3 make_index.py                  # index_template.tpl + fx_short.js -> index.html, work/cuts.json
python3 make_audio.py                  # music11.py (plan_short.json) + sfx.json + mix -> assets/mix.wav (-14 LUFS)
npx hyperframes render -f 30 -q high -w 2 -o renders/short11-raw.mp4                  # Bash run_in_background
ffmpeg -i renders/short11-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short11-ai-firms-your-data.mp4
ffmpeg -i renders/short11-ai-firms-your-data.mp4 -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high \
  -level:v 4.1 -pix_fmt yuv420p -g 60 -c:a copy -movflags +faststart renders/short11-ai-firms-your-data-phone.mp4
python3 ../../longform/ai-firms-your-data/shot.py cover11.html short11-cover.png 1080 1920
```

## Differences from the video

- Captions are the Shorts' uppercase karaoke chunks (`make_captions.py`) in the 1240–1460 band; visuals stay in 280–1220.
- The report's paragraphs are too small to read on a phone, so on three pages (sensitive data twice, the xAI suspension)
  the exact sentence is set large on top, labelled "QUOTED · ICO REPORT, P.n", while the real page stays dimmed behind.
- The page owner's logo is pinned top-right (820, 296), outside the zooming camera.

# Short #5 — "The robot that aced every test" (footage build)

Story: the paper "Has GPT-6-Astra Achieved Embodied Intelligence?" (SenseNova and partners, arXiv 2610.22471, 15 Oct 2026)
told as a trainee chef who aces cooking-school exams, then struggles on a real shift. Voice: the creator's ElevenLabs v4
recording (75.8 s), aligned word by word; video 78.3 s.

This is the first short made with Production workflow v2: generated footage instead of 3D. The robot-chef shots are
Veo 3.1 clips the creator made in Google Flow from `shots.json` (prompts, style line, reference images). The evidence
shots are real: page 1 of the paper and clips from the authors' project video.

## Inputs (git-ignored; the creator supplies them)

- `work/raw/*.mp4`: 19 Flow clips, 720×1280, 24 fps, 8 s. `edl.py` maps each clip number to its uploaded file.
- `work/raw_paper_video.mov`: phone screen recording of the project video on huggingface.co/papers/2610.22471.
  It is **HDR (PQ, BT.2020)**: without tone mapping it looks dim and washed out. `build_edit.py` maps it to SDR with
  `zscale` + `tonemap=clip` at 203 nits reference white.
- `work/paper.pdf`: arXiv 2610.22471.
- `work/voice_clean.wav`: `ffmpeg -i voice.wav -ar 48000 -ac 1 work/voice_clean.wav` (+ a 16 kHz copy for `align.py`).

## Rebuild

```bash
cd shorts/05-aced-every-test
mkdir -p assets/js && cp -r ../../template/assets/fonts ../../template/assets/grain.png ../../template/assets/base.css assets/
cp ../../template/assets/js/gsap.min.js assets/js/
python3 build_edit.py          # cut, retime, grade, conform every shot -> assets/clips, assets/img (about 5 min)
python3 make_index.py          # index.html from edl.py
python3 prep_words.py          # numbers to digits; its docstring has the caption and SRT commands
python3 ../../tools/make_track.py music.json work/music.wav
python3 ../../tools/make_sfx.py sfx.json work/sfx.wav
python3 ../../tools/mix.py work/voice_clean.wav work/music.wav work/sfx.wav assets/mix.wav 78.3
npx hyperframes check && npx hyperframes render -f 30 -q high -w 2 -o renders/short05-aced-every-test.mp4
```

Cover: `cover05.html` over `work/cover_bg.png` (s01 at 2.6 s) and `work/cover_inset.png` (s02 at 0.6 s), screenshot at
1080×1920 with the Playwright headless shell (`--screenshot --window-size=1080,1920`).

## How the edit is built

- `edl.py` is the shot list: out times (cut on the word timings), source clip, in-point, playback rate. Every shot is
  rendered with a 0.25 s handle on both sides so transitions can overlap.
- Flow clips: lanczos to 1080×1920, light contrast/saturation grade, unsharp, 30 fps, silent (Veo's own audio is dropped).
  `s17` is zoomed 1.3× from the top because Veo painted a flat grey band at the bottom of that clip.
- Evidence cards sit on the previous shot's last frame, blurred and darkened, with the brand grid. The robots grid
  (`s12`) is the eight tiles of the project video cropped one by one and re-laid out 2×4 for vertical.
- Each shot is `.shot > .fx (transitions, punch-ins) > .cam (slow push-in) > video`. Only the `<video>` carries
  `data-start`; a timed wrapper around a timed video makes HyperFrames extract the wrong frames, and every video needs an `id`.
- Freeze frames (`s08` "the clock stopped too", `s22` the final question) are stills from the conformed clip shown over it.

## Credits

Robot-chef footage: AI-generated with Google Veo 3.1 (Flow). Real robot, test-home and verdict clips: the authors'
project video. Paper page: arXiv 2610.22471. No Fluent Emoji art in this short.

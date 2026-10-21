# One AI Trick: Shorts production kit

This is everything used to make the Shorts, starting with Short #1, "The hospital inside your AI" (86 s, 1080×1920, 30 fps), and Short #2, "Read, don't obey" (83 s). Reuse it so every short keeps the same look, sound and quality.

## What's inside

| Folder | Contents |
| --- | --- |
| `tools/` | Python helpers: align voice to script, captions, SRT, 3D art fetch + 4× upscale, music, SFX, final mix |
| `template/` | The Short #1 HyperFrames project: `index.html` (14 scenes, global captions/UI), `base.css`, `fx.js`, GSAP, fonts, grain, `music.json`, `sfx.json`, example `captions.js` and `script.txt` |
| `brand/` | Logo, profile image, the Short #1 cover and `cover05.html` (cover template) |
| `library/3d/` | 85 upscaled 1024 px 3D illustrations ready to reuse; `library/README.md` lists them |
| `shorts/NN-slug/` | Source for each published short (script, word timings, captions, composition, SFX/music config, SRT, cover) |

Videos, WAVs and model weights stay out of git (see `.gitignore`). Deliver them as files instead.

## Setup (cloud workspace)

```bash
pip install --break-system-packages pocketsphinx torch scipy pillow numpy playwright
mkdir -p models && curl -L -o models/RealESRGAN_x4plus.pth \
  https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
export HYPERFRAMES_BROWSER_PATH=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell | head -1)
export HYPERFRAMES_NO_TELEMETRY=1
cd template && npx --yes hyperframes@0.8.162 check
```

HyperFrames can't download its own browser here. Point it at the Playwright headless shell, as above.

Network: the shell can reach PyPI, npm and GitHub (raw files and release downloads). It **can't** reach Unsplash, Pexels, Hugging Face downloads or jsdelivr. The Unsplash connector can search, but its download returns a URL the shell can't fetch. When real photos are wanted, ask the person to download and attach them. Don't route around blocks.

## Pipeline

1. **Script.** Write a 60–90 s story or analogy, with a hook in the first 2 s and one clear idea. Give the Gemini TTS settings:
   - In Google AI Studio, go to Generate media → Gemini speech generation.
   - Model: Gemini 3.8 Flash TTS. Single speaker, voice **Achird** (or Sulafat / Charon).
   - Use `<chuckle>` and `<short pause>` tags, and CAPS for emphasis words.
   - Download as WAV.
2. **Voice in.** Re-encode the upload, which fixes odd WAV headers:
   `ffmpeg -i raw.wav -ar 48000 -ac 1 voice_clean.wav` and `ffmpeg -i raw.wav -ar 16000 -ac 1 voice16k.wav`.
3. **Align.** Run `python3 tools/align.py voice16k.wav script.txt words.json`.
   - Edit `SUBS` (substring fixes, e.g. centres→centers) or `WORDMAP` (whole words, e.g. ai's→"a eyes") in `align.py` for words the dictionary lacks or says wrong.
   - Then check words near laughs, breaths and long pauses against the waveform's silences. In #1 and #2, "But" landed inside the chuckle and had to be moved. Fix timings in `words.json` itself, or in a `fix.json` that both caption tools read.
4. **Captions.**
   - On-screen captions: `python3 tools/make_captions.py words.json captions.js "EMPH,WORDS,READ@51.4" [fix.json]`. `WORD@seconds` emphasises only that occurrence.
   - Upload captions: `python3 tools/srt_from_words.py words.json shortNN-captions.srt [fix.json]`.
5. **3D art.** This is Microsoft Fluent Emoji 3D, MIT licence, so credit it in the description.
   - **Reuse `library/3d/` first.** Copy the images you need into the short's `assets/3d/`.
   - Only for new art: add entries to `ITEMS` in `fetch_fluent.py`. Folder names match `github.com/microsoft/fluentui-emoji/assets`.
   - Run `python3 tools/fetch_fluent.py raw3d name1,name2` to fetch just the new ones.
   - Then run `python3 tools/upscale.py models/RealESRGAN_x4plus.pth 23 raw3d template/assets/3d` in the background. It takes about 23 s per image on 2 CPUs.
   - **Check every PNG opens before rendering.** A half-written file renders as a blank image.
   - Commit the new 1024 px images to `library/3d/` and add them to `library/README.md`.
6. **Music + SFX.**
   - Run `python3 tools/make_track.py music.json music.wav` (styles: lofi, pulse, dream).
   - Run `python3 tools/make_sfx.py sfx.json sfx.wav` (whoosh, boom, pop, ding, scan, ring, rumble, tick(s), shimmer, glitch, zap, swell).
   - Time SFX events to the visual hits.
7. **Mix.** Run `python3 tools/mix.py voice_clean.wav music.wav sfx.wav mix.wav LENGTH`. It ducks the music under the voice and outputs −14 LUFS with a −1.5 dBTP peak.
8. **Composition.** Copy `template/` to `shorts/NN-slug/` and rewrite the scenes in `index.html`.
   - Structure: one `.clip.scene` per scene, each with an inner `.cam` for push-ins, whips and shakes. One global UI clip holds the progress bar, tag, @oneaitrick, karaoke captions, grain, vignette and the flash/black overlays. One `<audio src="assets/mix.wav">`.
   - Helpers: `img()` (bottom-anchored art), `shadow()`, `chip()`, `lobby()`, `svg()`, `popIn()`, `slideIn()`, `bob()`, `shake()`, `draw()`.
9. **Review.** Run `npx hyperframes check`, then `npx hyperframes snapshot -o DIR --at t1,t2,… --no-end --keep`, and make contact sheets.
   - Look at every scene **and** frames about ±0.1 s around every cut. Fix overlaps, empty frames and cramped captions.
10. **Render.** Run `npx hyperframes render -f 30 -q high -w 3 -o OUT.mp4`. It takes about 15 min for 86 s on 2 CPUs.
    - Keep the session active and watch it with a monitor. A background render died once when the session went idle.
11. **Verify.**
    - ffprobe should show 1080×1920, 30 fps, H.264 + AAC 48 kHz.
    - ebur128 should read about −14 LUFS.
    - Extract frames from the MP4 itself and look at them.
12. **Cover.** Copy `brand/cover05.html`, point its images at the art you need, and screenshot it at 1080×1920 with Playwright. Keep everything inside y 240–1680, the area Instagram's grid shows.

## Footage shorts (from #5)

Short #5 replaced the 3D scenes with generated and real footage: Veo 3.1 clips the creator makes in Google Flow from
prompts in the Content Hub, plus real material (paper pages, the authors' project video). `shorts/05-aced-every-test/`
is the template for this kind of build; its `BUILD.md` has the steps.

- Shot list in `edl.py`; `build_edit.py` conforms every clip (1080×1920, 30 fps, grade, handles) and `make_index.py` writes the composition.
- Only `<video>` elements carry `data-start`, each with an `id`. Never nest a timed video inside a timed `div`.
- Phone screen recordings are often HDR (PQ). Tone-map them (`zscale` + `tonemap`) or they come out dim and grey.
- Veo sometimes paints a flat dark band where a prompt says "keep the bottom third darker". Check each clip and crop or zoom past it.
- Credit the generated footage and the real sources in the description, and turn on YouTube's "altered or synthetic content" label when generated footage looks real.

## Real-material shorts (from #6)

Short #6 is mostly real material with captions designed into each shot. `shorts/06-the-machine-nobody-noticed/` is the
template; its `BUILD.md` has the steps.

- A phone recording of a web page becomes one clean tall image (`stitch_page.py`): it measures the scroll between frames
  and keeps only the content band, so the status bar, URL pill and AssistiveTouch button never appear. Pan over that
  image instead of playing the shaky recording. Tone-map first (HDR), then lift levels until the page is white again.
- `locate.py` OCRs pages and screenshots so highlights land on the exact words. Re-render paper figures from the PDF at 600 dpi.
- Captions: `CAPLAY` picks S, A (hero word), B (the number is the caption) or C (glass panel with a leader line) per chunk;
  the colour comes from the shot (`shotcolor.py`). The template's base.css already defines `.chip`, so don't reuse that class name.
- 1080p landscape footage: use `mode="tall"` (3:4 window over its own blurred fill), not a 9:16 crop.
- `-q high` renders run about 37 Mbps (H.264 level 5.0, ~400 MB). The Claude app crashes opening a file that size, so also deliver a
  phone copy: `ffmpeg -i in.mp4 -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high -level:v 4.1 -pix_fmt yuv420p -g 60 -c:a copy -movflags +faststart out-phone.mp4` (~130 MB).
  The renderer also mixes the audio about 1.7 dB quieter: swap the mix back in (`-map 0:v -map 1:a -c:v copy`) and re-check −14 LUFS.
- Render with Bash `run_in_background`, not `nohup … &`: a detached render is cancelled when its shell exits
  (`render_cancelled_parent_exited`). Don't `pgrep -f "hyperframes render"` from a monitor: it matches the monitor itself.

## Style rules (from the creator)

- Stories and examples, not information dumps. At least 60 s. Every line has something moving on screen, and every cut has a transition.
- Layout at 1080×1920:
  - Main visuals: y 280–1220.
  - Captions: band 1240–1460.
  - Bottom ~450 px: keep clear for platform buttons.
- Captions: Inter 900, about 84 px, uppercase, 14 px dark stroke.
  - The active word turns lime and scales up to 1.04 (emphasis words 1.08). Emphasis words stay lime.
  - Word margin 0.2em. Bigger scaling makes words collide.
- Brand: bg `#0b0c10`, lime `#c8ff4d`, blue `#7cc4ff`, amber `#ffb547`, pink `#ff7ac6`, red `#ff6b6b`; fonts Inter + mono.
- Tag top-left: "● AI CONCEPT · STORY". "@ONEAITRICK" top-right.
- End card: lime "1_" mark, "One AI Trick" with "AI" in lime, @oneaitrick, and a "+ Follow for AI, explained" pill.
- The first frame should already show the subject (hook), not an empty set.

## Gotchas from #1 and #2

- Fluent "Person walking" faces left, and the runners face right. Doctor/health-worker images are head-and-shoulders only.
- Grayscale + brightness filters make good "inactive" states. Lime drop-shadows make good "active" ones.
- The Fluent robot has blue eyes on a dark visor. #2's `robot()` helper overlays pink (hijacked) or lime (protected) eyes and keeps body motion separate from the entrance.
- Lime text is unreadable on cream paper. Put lime ink on a dark label instead.
- Round line caps leave a dot before a stroke draws on. `draw()` now hides the path until it starts.
- Keep scratch files (snapshots, contact sheets, WAVs) in the short's `work/` folder, which git ignores.
- AI labels:
  - YouTube doesn't need one for a generic AI narrator.
  - On TikTok, turn on "AI-generated content".
  - On Instagram, turn on "AI info".

# Short #7 — "The rulebook of water" (real-material build)

Story: OpenAI's claimed Navier–Stokes blow-up proof ([post](https://openai.com/index/navier-stokes-solution/), 8 Sep 2026;
Lean proof [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler)), told as "can the rulebook of water
break?", with the catches: the smooth push the whole time, the referee (Lean) that checks moves but not the game, the
method dispute (Scientific American 13 Oct, The Decoder 17 Oct) and the prize nobody claims.
Voice: the creator's ElevenLabs v4 recording (131.1 s), aligned word by word; video 133 s.

No generated media: 0 videos, 0 images. In place of the planned Flow clips, the edit uses three renders of my own:
a real 2D Navier–Stokes simulation (`fluid.py`), a 3D vortex after OpenAI's figure and a swarm of exactly 10,000 lights
(`particles.py`). All are labelled SIMULATION or ANIMATION on screen.

## Inputs (git-ignored; the creator supplies them)

- `work/raw/ScreenRecording_*.mp4`: phone screen recordings (HDR PQ) of the Clay pages, the GitHub repo and Lean file,
  Quanta, Scientific American and The Decoder.
- `work/img/openai_post.pdf`, `clay_navierstokes.pdf`: the OpenAI post and Fefferman's official problem as PDFs
  (the sites carried ads, so the creator printed them). `sciam.jpg`: a phone screenshot. `navier_stokes_portraits.jpg`:
  public-domain portraits of Navier and Stokes.
- `work/raw/*.mp4`: Pexels footage (money, hourglass, drip, ink, smoke, storm, wing, blood, chalkboard, whirlpool, tap,
  coffee, the basketball referee) and NASA Goddard's GPM Hurricane Maria visualisation (public domain).
  The Quanta YouTube video is deliberately not used.
- `work/voice_clean.wav`: 48 kHz mono voice (+ `voice16k.wav` for `align.py`). `work/tm.txt`, `work/lv.txt`: tone map
  and levels for the HDR recordings (same as #6).

## Rebuild

```bash
cd shorts/07-the-rulebook-of-water
mkdir -p assets/js && cp -r ../../template/assets/fonts ../../template/assets/grain.png ../../template/assets/base.css assets/
cp ../../template/assets/js/gsap.min.js assets/js/ && cp /usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-BoldItalic.ttf assets/fonts/serif-bi.ttf
bash stitch_all.sh                      # stitched pages (stitch_page.py SRC T0 T1 Y0 Y1 OUT [--xlock]) -> work/pages/
# single clean frames where a stitch seam would show: python3 frame_for.py PAGE SRC Y0 Y1 OUT.png with each shot's rows
#   from edl.py -> work/pages/f13, f17, f18, f37, f44, f46, f48, f52, clay_poincare.png; gh_lean68/76.png are the GitHub
#   recording's frames at 68 s and 76 s (tone-mapped with work/tm.txt + work/lv.txt), since that page scrolled sideways
pdftoppm -r 300 -png work/img/openai_post.pdf work/pdf/oa && pdftoppm -r 300 -png work/img/clay_navierstokes.pdf work/pdf/cl
python3 pdfwords.py work/img/openai_post.pdf work/pdf/oa_words.json        # word boxes for highlights on the PDFs
python3 pdfwords.py work/img/clay_navierstokes.pdf work/pdf/cl_words.json
python3 fluid.py swirl work/sim/swirl.mp4 10        # the 2D Navier-Stokes simulation
python3 particles.py swarm work/sim/swarm.mp4 9     # 10,000 lights
python3 particles.py vortex work/sim/vortex.mp4 10  # the 3D vortex, teal to orange
python3 build_edit.py                   # conform every shot (about 6 min)
python3 cutout.py                       # s12: equations and title behind the mathematician (rerun after build_edit)
python3 track.py s32 230 440 150        # s32: the tracked label on the spoon hand
python3 shotcolor.py                    # caption colour per footage shot
python3 prep_words.py                   # numbers to digits; its docstring has the caption + SRT commands
python3 make_index.py                   # index.html from index_template.tpl
python3 make_audio.py                   # music (cuts out on "But here's the catch"), SFX, mix to -14 LUFS
npx hyperframes check && npx hyperframes render -f 30 -q high -w 2 -o renders/short07_render.mp4
ffmpeg -i renders/short07_render.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short07-the-rulebook-of-water.mp4      # the render's own audio is ~1.7 dB quiet
```

Phone copy: the README's 12 Mbps level-4.1 command. Cover: `cover07.html` over `work/cover_bg.png` (the vortex at 6.6 s)
and `work/cover_inset.png` (OpenAI's real vortex figure), screenshot with the headless shell at 1080×1920.

## How it works

- **Own simulations instead of generated clips.** `fluid.py` solves the incompressible 2D Navier–Stokes equations
  (semi-Lagrangian advection, Fourier pressure projection, viscosity) with a Lamb–Oseen vortex whose core keeps
  shrinking, and renders dye with a flow map so it stays sharp. `particles.py` draws the 10,000-light swarm as three
  spiral arms and the 3D vortex from 300 streamlines in OpenAI's teal-to-orange colormap with a white-hot core. The speed
  readout above them climbs to ∞ on "infinity".
- **Pages without the phone.** Stitched pages (row-profile scroll matching) for long scrolls, and single clean frames
  (`frame_for.py`) wherever a stitch seam would show; the GitHub Lean file scrolled sideways, so it uses two frames.
  The PDFs give the OpenAI post and the official problem at 300 dpi with exact word boxes.
- **Document camera.** `docCam` in the template flies to each highlight as it is swept: scale
  `clamp(880/(w+80), 1.05, 1.7)`, the phrase centred at (540, 760), then a slow drift. The card is nudged down when that
  clears the labels, and every document shot fades to dark above the caption band (`.docfade`) and under the labels
  (`.doctop`), so captions never sit on page text.
- **Text behind the subject (s12).** `cutout.py` cuts the mathematician out of every frame (rembg `u2net_human_seg`)
  and puts the official equations (chalk white) and "NAVIER–STOKES" between the board and him.
- **Tracked label (s32).** OpenCV CSRT follows the spoon hand; "THE PUSH →" rides on it.
- **Record scratch.** On "But here's the catch" the frame freezes and desaturates under a "WAIT…" stamp while the music
  drops out (59.6–61.13 s).
- **Designed captions** as in #6 (modes S, A, B, C). The number counters run as a clock for "88 hours".

## Credits

Real: OpenAI's post and GitHub repo; the Clay Mathematics Institute pages, prize rules and Fefferman's official problem;
Quanta Magazine, Scientific American and The Decoder (screenshots, commentary). NASA Goddard GPM (public domain).
Portraits of Navier and Stokes (public domain). Stock: Pexels. Simulations and animations: my own renders.
No Fluent Emoji art.

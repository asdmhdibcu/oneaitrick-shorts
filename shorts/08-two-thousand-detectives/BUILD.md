# Short #8 — "Two thousand detectives" (build)

122.5 s, 56 shots. OpenAI × PerturbAI × Scripps ran 1,946 GPT-Rosalind agents over a 7.7-million-cell mouse brain
CRISPR atlas in 32 minutes; one lead (DCTN1 → cholesterol-making genes switched on) is the story. Sources: the agents
preprint (bioRxiv, 16 Oct 2026), the atlas preprint (Shi et al.), OpenAI's post (21 Oct 2026), the repo's MIT-licensed
data (`work/repo_data/`), the Hugging Face dataset card, the creator's phone recordings of the OpenAI × PerturbAI video
and the findings site.

`assets/`, `work/` and renders are git-ignored. Rebuild:

```bash
cd shorts/08-two-thousand-detectives
cp -r ../../template/assets/fonts ../../template/assets/grain.png ../../template/assets/base.css assets/
mkdir -p assets/js && cp ../../template/assets/js/gsap.min.js assets/js/
npm i three@0.170.0 esbuild@0.24.0
# 3D (three.js + bloom, rendered offline with SwiftShader, ~1 s a frame)
npx esbuild src3d/world.js --bundle --format=iife --minify --outfile=src3d/world3d.js
python3 render3d.py helix 2.7; python3 render3d.py walk 1.8; python3 render3d.py jam 2.9; python3 render3d.py pile 2.9; python3 render3d.py fix 1.85
python3 pins3d.py                      # screen positions of the labelled 3D points, per frame
# PDFs: pdftoppm -r 300 for oa/ag/at pages (work/pdf/<doc>-<page>.png), pdfwords.py for word boxes,
# pdfimages -j -f 18 -l 21 for the 600 ppi figures (work/img/fig-00N.jpg) and the crops q4l/f1a/f4k/f4a.png
python3 build_edit.py                  # conform every shot (edl.py) -> assets/clips, assets/img, work/meta.json
python3 shotcolor.py
python3 prep_words.py && python3 ../../tools/make_captions.py work/words_cap.json captions.js "$(cat work/emph.txt)"
python3 make_audio.py                  # music8.py score + sfx.json + mix -> assets/mix.wav
python3 make_index.py                  # index_template.tpl -> index.html
```

## What's in it

- **Flow clips (10, the cap):** lanterns (×2), window → wires, the neuron lorry track (×2 uses), the case wall, lorries
  in the rain, chimneys, the golden cell body (×2 uses), one window ↔ the city (reversed for the push-in, forward for
  the bookend), the lit tower. Letterboxed ones are cropped (`pre`) and upscaled with Lanczos + light unsharp.
  Labelled "AI ILLUSTRATION · GOOGLE FLOW" on screen.
- **3D (`src3d/world.js`):** a DNA helix cut by a CRISPR clamp; dynein + dynactin walking a microtubule with its
  DCTN1-built p150 arm glowing; the arm failing while cholesterol piles up; the heap in the wrong place; the motor
  restored. Labels ride the 3D points (`pins3d.py` → `work/sim3d/*_pins.json`).
- **My graphics in the composition:** stopwatch; gene tags on the wiring; the cut slash; a wall of all 1,946 real
  target genes (from the repo's `target_deg_burden.csv`) zooming out from Dctn1; viewfinder + flashes; lights on/off
  grid; a mountain of photos; the by-hand month counter; the GPT-Rosalind badge; one detective tile multiplying to
  1,946 with an amber ripple; the reference race (11 vs 7,586, the paper's 711×); redaction bars over the scientists'
  paper; the expert and abstract quotes set large over their real strips; 3-of-4 judges; the real case name tracked
  onto the Flow card (`work/track_s29.json`); the 13 real cholesterol genes switching ON (agents' finding F001);
  connecting-the-dots strings.
- **Score:** `music8.py`, original. Part A investigation pulse in D minor; it stops dead on "Then… the clue." and
  turns to noir jazz (walking bass, ride, brushes, Rhodes) on "One wire"; drums drop out on "But careful"; Part A
  returns for the bookend and resolves to D major.
- **Voice:** the creator's take with the corrected "Over SEVEN THOUSAND" sentence spliced in (`work/splice.json`).

## Gotchas

- The board footage (Pexels 8369883) has threatening notes on it ("I'll kill you…", "Don't try to find help…");
  `cx=0.42` keeps both out of the 9:16 crop. The pointing clip (8369880) shows one after ~28 s: use earlier.
- OpenAI's post says "more than 700" references; the paper and data say 7,586 (vs 11). The script uses the data.
- The phone recording is HDR PQ at 120 fps: tone-map with `work/tm.txt` + `work/lv.txt`; the video band is y 1062–1804.
- A class named `.sw` already styles the chip dots; the switch panel is `.swb`.

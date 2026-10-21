# Short #6 — "The machine nobody noticed" (real-material build)

Story: Anthropic's AI-found enzyme system, ART ([announcement](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system),
23 Sep 2026; preprint Yoon et al., bioRxiv 10.64898/2026.10.05.755809), told as a search party in the biggest library on Earth.
Voice: the creator's ElevenLabs v4 recording (83.6 s), aligned word by word; video 85.5 s.

First short in the creator's "mostly real material" style: Anthropic's post, the preprint's figures, Anthropic's lab
video, news screenshots, an electron micrograph and Pexels library footage. Only five shots are generated (two Veo 3.1
clips from Google Flow). Captions are designed into each shot in that shot's own colours.

## Inputs (git-ignored; the creator supplies them)

- `work/raw/rec2.mp4`: phone screen recording of the post (HDR PQ, 1320×2868, scrolled by hand).
- `work/raw/anthropic_lab_video.mp4`: Anthropic's lab video (AV1 1784×1080, 24 fps).
- `work/raw/px_*.mp4`: Pexels library and server footage. `work/raw/flow_a.mp4`, `flow_b.mp4`: the two Flow clips.
- `work/img/*`: phone screenshots (TechCrunch, Al Jazeera, Decrypt, Nobel press release, @AnthropicAI on X) and
  `phage_tem.jpg` (Wikimedia "Phage.jpg", Graham Beards, CC BY-SA 3.0).
- `work/paper.pdf`: the preprint. `work/voice_clean.wav`: 48 kHz mono voice (+ `voice16k.wav` for `align.py`).
- `work/tm.txt`: the HDR tone-map filter; `work/lv.txt`: levels that bring the post's cream page back to white.

## Rebuild

```bash
cd shorts/06-the-machine-nobody-noticed
mkdir -p assets/js && cp -r ../../template/assets/fonts ../../template/assets/grain.png ../../template/assets/base.css assets/
cp ../../template/assets/js/gsap.min.js assets/js/ && cp /usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-BoldItalic.ttf assets/fonts/serif-bi.ttf
python3 stitch_page.py work/raw/rec2.mp4 work/page.png   # the whole post as one clean, tall image (2 min)
python3 stab_dna.py 21.0 26.0 work/dna                   # steady frames of the post's DNA figure
python3 ocr_page.py                                      # word boxes for the highlights
python3 build_edit.py                                    # conform every shot (about 4 min)
python3 shotcolor.py                                     # caption colour per footage shot
python3 prep_words.py                                    # numbers to digits; its docstring has the caption + SRT commands
python3 make_index.py                                    # index.html from index_template.tpl
python3 make_audio.py                                    # music (drops out on "Nobody knows"), SFX, mix to -14 LUFS
npx hyperframes check && npx hyperframes render -f 30 -q high -w 2 -o renders/short06-the-machine-nobody-noticed.mp4
```

Cover: `cover06.html` over `work/cover_bg.png` (s14 at 2.45 s) and `work/cover_inset.png` (the DNA figure with its 14
repeats outlined), screenshot with the Playwright headless shell (`--no-sandbox --screenshot --window-size=1080,1920`).

## How it works

- **The post, without the phone.** The screen recording scrolls by hand under a status bar, a sticky header, Safari's
  URL pill and the AssistiveTouch button. `stitch_page.py` measures the scroll between frames (row-profile matching)
  and pastes only the clean band of every frame into one 1240×21853 image, keeping for each row the frame that moved
  least. Page cards then crop bands of it under the site header and the edit pans and zooms with its own steady camera.
- **The DNA scan.** The post's figure animates from raw DNA to 14 highlighted repeats, but the transition happened
  while the recording was scrolling. `stab_dna.py` steadies the figure; the edit shows the real "before" frame, wipes
  to the real "after" frame behind a scan line, and outlines each repeat as the scan reaches it (found by colour).
- **Highlights on real text.** `ocr_page.py`/`locate.py` OCR the page and screenshots, so each highlight sits on
  the exact words. Preprint figures are re-rendered from the PDF at 600 dpi.
- **Designed captions.** `CAPLAY` in `make_index.py` gives every caption chunk a look: S (centred, unspoken words dim),
  A (left, emphasis word huge and tilted with a glow bar), B (the number is the caption and counts up), C (glass panel in
  the scene with a leader line to the subject). Colours come from each shot (`shotcolor.py`) or its material
  (Anthropic clay on the post, the figure's cyan, the micrograph's ice blue).
- **Landscape footage.** 4K clips are cropped 9:16. 1080p landscape (the lab video, the grand library) uses a 3:4 window
  at the top over its own blurred fill (`mode="tall"`), which is far sharper than a 9:16 crop. Lab shots slow down just
  enough to fit their handles inside the source shot (`win`).

## Credits

Real: Anthropic's post and lab video; preprint figures (Yoon et al., Anthropic, CC BY 4.0); TechCrunch, Al Jazeera,
Decrypt and nobelprize.org screenshots (commentary); "Phage.jpg" by Graham Beards, CC BY-SA 3.0 (credited on screen).
Stock: Pexels. Generated: Google Veo 3.1 (Flow), marked "AI ILLUSTRATION" on screen. No Fluent Emoji art.

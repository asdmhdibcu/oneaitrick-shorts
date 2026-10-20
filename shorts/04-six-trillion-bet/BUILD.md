# Short #4 — "The $6 trillion bet" (3D + archive build)

Story: Britain's 1840s Railway Mania as "the AI of 1845" (Charlotte Brontë's shares £50 → £120 → £20; the tracks
stayed), then Bain's 2026 numbers ($780B this year, $1.5T a year by 2031, ~$6T a year needed, $1.8T best case,
$4.2T gap). Voice: creator's ElevenLabs v4 recording (85.8 s), aligned word by word; video 88.6 s.

## Rebuild

`assets/` is git-ignored. Materials the creator supplied (keep them out of git; they are third-party):
`turner.jpg` (Turner, Rain, Steam and Speed), `charlotte.jpg` (Richmond 1850, 4x Real-ESRGAN upscale of a 200 px
copy), `darwin.jpg` (Richmond 1840, cropped + upscaled), `punch.jpg` (Punch 1845 via The Victorian Web),
Unsplash `viaduct.jpg`, `corridor.jpg`, `servers.jpg`, `wheel.jpg`, and PDF pages rendered at 2048 px wide:
`page_odl-001.jpg`, `page_odl-025.jpg` (Odlyzko 2010, pp. 1 and 25), `page_bain-08.jpg`, `page_bain-10.jpg`
(Bain Technology Report 2026, PDF pages 8 and 10). `src/hl.json` holds the highlight boxes, extracted from the
PDFs' word boxes (`pdftotext -bbox`), so the marker lands exactly on the quoted words.

```bash
cd shorts/04-six-trillion-bet
cp -r ../../template/assets/fonts ../../template/assets/grain.png ../../template/assets/base.css assets/
mkdir -p assets/js && cp ../../template/assets/js/gsap.min.js assets/js/
npm i three@0.170.0 esbuild@0.24.0 world-atlas@2.0.2 topojson-client@3.1.0
npx esbuild src/main.js --bundle --format=iife --minify --loader:.json=json --outfile=assets/js/world.js
```

Audio: `ffmpeg -i voice.mp3 -ar 48000 -ac 1 work/voice_clean.wav` (+ a 16 kHz copy), `tools/align.py`
(years and "Brontë" were added to its SUBS), `make_track.py music.json`, `make_sfx.py sfx.json`,
`mix.py work/voice_clean.wav work/music.wav work/sfx.wav assets/mix.wav 88.6`.
`prep_words.py` merges spoken numbers into digits (£120, 4,500, 780, 1.5, 1.8, $4.2) for the karaoke captions
(`work/words_cap.json`) and the upload SRT (`work/words_srt.json`); its footer has the two caption commands.

## Worlds (src/)

- `w_gallery.js` portrait in a gilded oval frame, share certificate that glitches to "AI SHARE"; 1849 grey version.
- `w_paint.js` Turner's painting as a 2.5D plate in the rain; a 3D locomotive bursts out of it.
- `w_board.js` Punch cartoon + Odlyzko p.1 on a board, red string to the highlighted names, falling shares.
- `w_hill.js` the share price as a railway climbing £50 → £120; fares vs expectations; the crash off a cliff.
- `w_map.js` Britain (world-atlas outline): 1845 network amber, 1846 approvals lime (illustrative routes).
- `w_photo.js` wheel and viaduct photo plates with live steam; desk with Odlyzko p.25 highlighted.
- `w_dc.js` data-centre aisle with glowing rails, the hall multiplying, Bain p.8 highlighted.
- `w_bridge.js` viaduct over a chasm: $6T beacon, $1.8T built, $4.2T gap, bubble pops, phone + cloud arches, sunrise.
- `main.js` shot list, camera paths, burn / zoom-through transitions on every cut, pinned HTML labels.

Render with SwiftShader: `npx hyperframes render -f 30 -q high -w 2 --no-browser-gpu`. `hyperframes check` skips
the 3D layer (check mode is detected via `__hfScriptState`) and lints the HTML layer; the 3D is reviewed with
`hyperframes snapshot` contact sheets. Cover: `cover04.html` over a clean frame at 4.4 s (`work/cover_bg.png`,
snapshotted with the UI hidden).

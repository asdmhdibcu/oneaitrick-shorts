# Short #15: "Google sent an AI to space. Its first words were a poem" (build)

2:56, 50 shots, 1080×1920, 30 fps, −14 LUFS. The creator's ElevenLabs take (`ElevenLabs_2026-10-30T22_08_06`, 174.0 s,
502 words) aligned whole with `tools/align.py`: it fits under 3:00 as recorded, so no pauses were cut
(`tighten_voice.py` and the chunk scripts were for an earlier, longer take). Hidden word: **SVALBARD** on the map pin
(s11, s47) and in Google's headline card; the voice says "the top of the world".

**No generated media.** The four Flow clips in the plan became my own graphics: an orthographic globe drawn every frame
with d3-geo from Natural Earth land (orbit with a lap timer and ground-station pings; the dawn–dusk orbit riding the
day–night line), a thermos cutaway, bit flips, a proton-beam diagram, a laser-and-coin drift and two linked satellites.

## Material (all downloaded in the workspace)

- **Google**: the 30 Oct post rendered headless (no banners) for the headline card; the 1 Oct launch video
  (`g_launch_social.mp4`; only the rocket take is used: the deploy-camera take shows other companies' satellites and
  logos, and the crowd takes show staff faces close up); Google Research's 81-satellite cluster animation
  (`g_suncatcher_research.mp4`) as a card in s04 and s38.
- **NASA** (public domain, images-api.nasa.gov): "4K Earth Views, Extended Cut" from the space station (a 2 GB file:
  the moov atom is at the front, so byte ranges were fetched into a sparse file and six segments cut from it), the SDO
  4K Sun (visible light only at 19–39 s; other stretches are other wavelengths), space-station solar arrays and
  radiators (iss038e024901), Svalbard from ASTER (PIA10626).
- **Stock**: Pexels through its own download links (chip, server racks, Tokyo at night, solar farm, phone, fans),
  Mixkit (Mixkit Stock Video Free License only: phone typing, city at night, glowing coals, phone by a window), Coverr
  (power tower).
- **Logos**: Simple Icons (Google, SpaceX, Planet), rendered to PNG.
- **Not reachable**: iea.org answers 403 to the workspace, so the "more than Japan" line is shown with an IEA chip but
  was not re-read on the IEA page here (the brief cites it through three news reports).

## Rebuild

```bash
cd shorts/15-a-poem-from-space
mkdir -p assets/js && cp -r ../../template/assets/{fonts,base.css,grain.png} assets/   # + gsap 3.15, d3-array, d3-geo, topojson-client, land110.js (world-atlas)
python3 ../../tools/align.py work/voice16k.wav work/script_plain.txt words.json
python3 ../../tools/make_captions.py words.json captions.js "POEM,BIG,HUNGRY,UP,TRILLION,EIGHT,HEAT,THERMOS,RADIATORS,RADIATION,LASER,2027,PLANET,COMMENT,NEVER"
python3 ../../tools/srt_from_words.py words.json short15-captions.srt && python3 make_srt_tr.py   # + es, pt, hi, id
python3 build_edit.py        # conform every shot -> assets/clips (V, STILL, CARDV, backdrops)
python3 make_index.py        # index_template.tpl + fx15.js -> index.html, work/cuts.json
python3 make_audio.py        # score + SFX + mix -> assets/mix.wav (-14 LUFS)
npx hyperframes render -f 30 -q high -w 2 -o renders/short15-raw.mp4                       # Bash run_in_background
ffmpeg -i renders/short15-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short15-a-poem-from-space.mp4
```

Cover: `cover15.html` (a NASA Earth frame as `assets/img/cover_bg.png`), screenshot with node Playwright.

## Notes

- d3-geo needs d3-array loaded first (`t.Adder is not a constructor` otherwise).
- `hyperframes check` times out on 60 s windows here; 30 s windows pass. Contrast flags left: numbers on their own
  coloured bars in s22 and labels mid-fade.
- Overlay audit (node Playwright): the only long-lived elements are zero-width or off-screen until their shot.

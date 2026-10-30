# Short #13: "Scientists left an AI alone on an island. It started to play." (build)

1:20, 30 shots, 1080×1920, 30 fps, −14 LUFS. The creator's ElevenLabs take (78.3 s, 233 words) aligned word by word.
First short under the worldwide rule and the first built mostly from **real material**: the paper's own recorded runs,
Mixkit stock, the paper's figures, and four Flow clips. Facts checked against the paper (BRIEF.md).

## Material

- **The paper's runs** (machineplaying.org; data on data.clawblox.com). The site's replay player was loaded headless with a
  patched copy of its renderer (`v1-shared/renderer.bundle.js`, served through a Playwright route) that adds a scriptable
  camera (`globalThis.__mesaCam`), forced to a vertical 540×960 canvas and stepped frame by frame with Playwright's fake
  clock. Capture script and patch live in the session scratchpad (`replays/capture.js`, `site/shared.follow.js`).
  - Playback doesn't work for action: the replay holds positions between bursts and skips idle gaps, so Eko teleports.
    Every real-run shot is a **held moment** (`hold: true`) with a moving camera: the opener at spawn (agent 9, 0:00), the
    double compass rose (2:57), the fall from the Rock (1:38, the one playback clip, slowed without blending), a block on
    the Rock (1:45), Eko on the Spire (1:54:14), Eko with the Ring at the edge (4:13:46), the stone heart (4:33, turned 180°:
    a straight-down camera) and agent 2's Temple of the Spawn Axis (9:53).
  - Timestamps come from the agents' transcripts (data.clawblox.com/paper/replays/v1/agent-NN/transcript/).
  - ~3 s per frame in software WebGL; two browsers at once at most (four stalled the machine).
- **Paper crops** (`work/fig/`, 600 dpi): Figure 1 snapshots (basketball, the heart, the mid-air throw), Figure 5B
  (objects on the Spire, 3.5 vs 10.3), the p. 3 sentence on "enjoyment, absorption, or fun".
- **Stock**: 12 Mixkit clips under the Mixkit Stock Video Free License (MATERIAL.md lists ids); "Restricted" clips skipped.
- **Flow**: 4 of 10 (beach, thirteen on the shore, spire at sunset; the climb clip unused).

## Rebuild

```bash
cd shorts/13-alone-on-an-island
mkdir -p assets/js && cp -r ../../template/assets/{fonts,base.css,grain.png} assets/   # + gsap 3.15 and its plugins from npm (gsap@3.15.0 dist)
python3 ../../tools/align.py work/voice16k.wav work/script_plain.txt words.json
python3 ../../tools/make_captions.py words.json captions.js "PLAY,JUMPED,SPIRE,HEART,THREE,THIRTY,THIRTEEN,SIX,PLAY@67.86,GOOD"
python3 ../../tools/srt_from_words.py words.json short13-captions.srt && python3 make_srt_tr.py   # + es, pt, hi, id
python3 build_edit.py        # conform every shot -> assets/clips
python3 make_index.py        # index_template.tpl + fx13.js -> index.html, work/cuts.json
python3 make_audio.py        # score + SFX + mix -> assets/mix.wav (-14 LUFS)
npx hyperframes render -f 30 -q high -w 2 -o renders/short13-raw.mp4                       # Bash run_in_background
ffmpeg -i renders/short13-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short13-alone-on-an-island.mp4
ffmpeg -i renders/short13-alone-on-an-island.mp4 -c:v libx264 -preset slow -crf 18 -maxrate 12M -bufsize 24M -profile:v high \
  -level:v 4.1 -pix_fmt yuv420p -g 60 -c:a copy -movflags +faststart renders/short13-alone-on-an-island-phone.mp4
```

## Notes

- GSAP 3.15 (free plugins) used here first: SplitText types the notes and quotes (`words,chars`, so words never break)
  and drops the big words in letter by letter. The template still has its own GSAP.
- `hyperframes check`: lint passes (the usual two size warnings); the runtime pass times out in this workspace's
  software mode even at `--timeout=60000`, so every scene and ±0.1 s around every cut were checked from snapshots instead.
- Hidden word for Instagram: "joy", written in the sand in s29; never said.
- Verified: 1080×1920, H.264 + AAC 48 kHz, 30 fps, 80.2 s, −14.0 LUFS, −1.4 dBTP (both the master and the phone copy).

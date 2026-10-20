# Short #3 — "The swarm" (3D build)

The visuals are real-time 3D (three.js + bloom) rendered inside HyperFrames. `assets/` is git-ignored, so rebuild it:

```bash
cd shorts/03-the-swarm
cp -r ../../template/assets/fonts ../../template/assets/grain.png ../../template/assets/base.css assets/
mkdir -p assets/js && cp ../../template/assets/js/gsap.min.js assets/js/
npm i three@0.170.0 esbuild@0.24.0
npx esbuild src/main.js --bundle --format=iife --minify --outfile=assets/js/world.js
```

Audio: `python3 build_edit.py` cuts the voice from the long-form master (`longform/rogue-swarm/work/voice_master.wav`)
into `work/voice_clean.wav` + `words.json`; then `make_track.py music.json`, `make_sfx.py sfx.json` and
`mix.py work/voice_clean.wav work/music.wav work/sfx.wav assets/mix.wav 110`.

- `src/core.js` renderer, two-scene burn dissolve, bloom, camera framing (subject lands at y≈760).
- `src/robot.js` procedural robot (hero + instanced army), shader dissolve.
- `src/w_hive.js` hive of cells, exam wall, seal dome, tower, bridge, river, lab. `src/w_core.js` data core. `src/w_map.js` incident map.
- `src/main.js` shot list, camera keyframes, transitions, HTML label pinning.

Render with SwiftShader (llvmpipe stalls on init): `npx hyperframes render -f 30 -q high -w 2 --no-browser-gpu`.
`hyperframes check` can't fit real 3D in its fixed 120 s budget on software GL, so the page skips the 3D layer when
the check's `__hfScriptState` hook is present; the check then lints the HTML layer (captions, labels, contrast), and
the 3D is reviewed with `hyperframes snapshot` contact sheets.

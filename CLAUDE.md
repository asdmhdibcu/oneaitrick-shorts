# One AI Trick: Shorts studio

This repo makes the vertical Shorts for **One AI Trick** (@oneaitrick): AI explained through short stories and examples, posted on YouTube Shorts, TikTok and Instagram Reels.

Read `README.md` before building anything. It has the full pipeline, commands, style rules and known gotchas.

## Layout

- `tools/`: voice alignment, captions, SRT, 3D art fetch/upscale, music, SFX, mix
- `template/`: the HyperFrames composition every short starts from (Short #1's 14-scene build)
- `library/3d/`: upscaled 1024 px 3D art. Reuse it before fetching or upscaling anything new
- `brand/`: logo, profile image, cover template
- `shorts/NN-slug/`: one folder per short (e.g. `shorts/02-…/`) holding script, `words.json`, `captions.js`, `index.html`, `sfx.json`, `music.json`, SRT and cover

## Rules

- Story first, never an information dump. 60–90 s. Something moves on screen in every line, and every cut has a transition.
- The creator records the voice in Gemini TTS. Video timing follows their WAV, aligned word by word.
- Before rendering, check `npx hyperframes check` and snapshot contact sheets of every scene **and** ±0.1 s around every cut. Fix anything cramped, overlapping or empty.
- Render with `-f 30 -q high`. Verify the MP4: 1080×1920, 30 fps, −14 LUFS. Look at frames pulled from the file itself.
- Keep the session active while a render runs (watch it with a monitor). An idle session once killed a background render.
- Commit sources and new library art. Never commit MP4, WAV or model weights. Deliver those as files.
- Real photos: the workspace can't download from Unsplash, Pexels or Hugging Face. Ask the creator to attach them. Never work around a network block.
- Credit "3D art: Microsoft Fluent Emoji (MIT licence)" in every YouTube description that uses it.
- From Short #7: at most 10 generated videos and 5 generated images per short. Everything else is stock (Pexels, Pixabay, Unsplash, Mixkit, Coverr), public-domain or Creative Commons footage, screen recordings, screenshots and our own graphics. The Content Hub's "Visual playbook" lists the techniques.
- Scripts from #7: an expression tag on almost every line; [whispers] at most once, only when the story needs it.
- Skill packs on the account (hyperframes, motion-video-skills) are technique libraries. This file, README.md and the project instructions decide the workflow; README.md "Skill packs" lists where they clash with our rules.

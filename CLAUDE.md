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
- The creator records the voice in ElevenLabs (a clone of their own voice, so the AI labels stay on). Video timing follows their WAV, aligned word by word.
- Before rendering, check `npx hyperframes check` and snapshot contact sheets of every scene **and** ±0.1 s around every cut. Fix anything cramped, overlapping or empty.
- Render with `-f 30 -q high`. Verify the MP4: 1080×1920, 30 fps, −14 LUFS. Look at frames pulled from the file itself.
- Keep the session active while a render runs (watch it with a monitor). An idle session once killed a background render.
- Commit sources and new library art. Never commit MP4, WAV or model weights. Deliver those as files.
- Real photos: the workspace can't download from Unsplash, Pexels or Hugging Face. Ask the creator to attach them. Never work around a network block.
- Credit "3D art: Microsoft Fluent Emoji (MIT licence)" in every YouTube description that uses it.
- From Short #7: at most 10 generated videos and 5 generated images per short. Everything else is stock (Pexels, Pixabay, Unsplash, Mixkit, Coverr), public-domain or Creative Commons footage, screen recordings, screenshots and our own graphics. The Content Hub's "Visual playbook" lists the techniques.
- Scripts from #7: an expression tag on almost every line; [whispers] at most once, only when the story needs it.
- Skill packs on the account (hyperframes, motion-video-skills) are technique libraries. This file, README.md and the project instructions decide the workflow; README.md "Skill packs" lists where they clash with our rules.
- From #9: the first 1–2 seconds lead with the surprising result, never background. Every script runs Hook → evidence → twist → takeaway, 60–90 s. Story-led explainers, not how-to tutorials.
- From #12, the Instagram plan (Content Hub tab "Instagram plan"):
  - Every Reel hides one on-screen word that the voice never says. The line before "Follow for more AI, explained like this." is "There's one word in this video I never said out loud. Spotted it? Comment it."
  - Every episode also gets a carousel (8–10 slides, 1080×1350) and 2–3 opening variants for Trial Reels.
  - Instagram alone adds a third post type, "the trick": a 30–45 s demo of one AI tool. The "not how-to" rule still holds for YouTube and TikTok.
  - No face on camera for now.
- From #13, every short is made for a worldwide audience, not just the UK:
  - Pick stories that matter in any country: global tools (ChatGPT, Gemini, WhatsApp, Gmail), studies with worldwide results. A one-country story only when the mechanism happens everywhere; name the country once, as one example.
  - Plain international English that non-native viewers follow: short words, no idioms or slang, US spelling on screen (math, color). Say "phone", "mail", "mom or dad"; avoid local institutions (NHS, ICO, Parliament) unless the story needs one, then say what it is in a few words.
  - Money in US dollars, or no currency at all. Numbers rounded and said simply ("about one in eight").
  - Every key idea readable from the picture alone, so it lands even with the sound off or for a weaker English speaker.
  - Titles and hashtags in plain English with no local references. Upload translated title, description and subtitles (Spanish, Portuguese, Hindi, Indonesian) for every short.
  - Post at about 14:00 UTC (US morning, UK afternoon, India evening).

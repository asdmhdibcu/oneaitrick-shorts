# One AI Trick: Shorts studio

This repo makes the vertical Shorts for **One AI Trick** (@oneaitrick): AI explained through short stories and examples, posted on YouTube Shorts, TikTok and Instagram Reels.

Read `README.md` before building anything. It has the full pipeline, commands, style rules and known gotchas.

## Where things live

- **Content Hub** (a Claude doc): https://claude.ai/artifact/4jAqayBZERE2sH6SkepU5Q. Its Overview tab holds the posting tracker, brand, "Raising the bar" (scorecard, "Every short from #10", experiments, log) and the visual playbook. Every short has its own tab, `#NN Title`, tab order `bNN`. There is one hub: update it, never start a second.
- **This repo**: the sources. A short's hub tab and its `shorts/NN-slug/` folder mirror each other.
- **Finished files** (MP4 and phone copy, cover, SRTs) go to the creator as files, never into git.

## Every short, step by step

Before writing anything for a short (pitch, script, scene sheet), read this file, `README.md`, the hub's Overview tab and the hub tabs and repo folders of the last two shorts. Then write it the way those were written. On #16 a script was drafted without reading the hub, and the creator had to send it back.

Ask the creator before you pick a topic, treat a script as final, spend credits (vidIQ, paid Flow, HeyGen), post or publish anything, or delete files.

1. **Pitch.** Research AI news, papers and launches from the last 2–3 weeks, plus evergreen ideas. Check what is trending only when the creator asks: Google Trends' daily list, then vidIQ rising keywords and Shorts outliers (5 credits a call, so check the balance first). Pitch three ideas, each with a one-line hook, the everyday picture, the primary source and why it matters in any country. Frame each one around a mystery or what's at stake for ordinary people (money, family, privacy, safety), never the technical term: the drama-led shorts ($1M math problem, 2,250 clouds) travel furthest. Wait for the pick.
2. **Tab and folder.** Once a topic is picked, add the hub tab, a row in the posting tracker and `shorts/NN-slug/`.
3. **Script.** The hub tab, in this order:
   - the title, then the date · creator byline;
   - a bold status line (what is waiting, and for whom);
   - `## The story`: Hook, Everyday picture, Evidence, Twist, Catch, Takeaway, Hidden word, First frame;
   - `## Script vN (N words, about N s)` as a code block;
   - from #18, `## Script with pictures`: a two-column table (Spoken line | On screen and sound), one row per sentence, a new visual cue at least every 4 s, so no line is talk over a still picture;
   - `## Fact check`: a table (Script says | The source says | Source), then a "Left out on purpose" line.

   Mirror it in `BRIEF.md` (the story, the facts table, the pitches not picked) and `script.txt` (the tagged lines only). Wait for the creator's OK. A rewrite is v2, v3… and the old version stays in git history.
4. **Voice.** The creator records the approved script in ElevenLabs with their cloned voice and attaches the take. Give Gemini TTS settings only if they ask for Gemini.
5. **Scene sheet and material.** From the take's word timings, write the hub table (# | Time (s) | Line | What moves | Into it | Source), with a real page, logo, clip or graphic for every line. Then write the material table (Need | File name | What | Link), each row marked NEEDED, OPTIONAL or DONE. Mirror both in `MATERIAL.md`.
6. **Build** with README's pipeline. Put the notes and rebuild commands in `BUILD.md`.
7. **Deliver** the MP4 and phone copy, the cover, the English SRT and the es, pt, hi and id SRTs. Put the upload pack in the tab and in `UPLOAD.md`. Update the tracker row and the hub's Log row.
8. **Push** sources straight to `main`, with no pull requests. Commit message: `Short #NN 'Title': what changed`.
9. **48 hours after posting**, fill the scorecard row from the creator's analytics screenshots.

Script standards, on top of the Rules below:

- Length: 60–90 s unless the creator asks for longer (#15 ran 2:56). The best-held shorts are 84–87 s, and retention falls apart past 110 s. Never go past 3:00. #18 tests a 45–60 s package (hub Experiments): the 2-minute shorts keep only 10–25 % of viewers for their last 15 s.
- The first frame shows the claim. Seconds 4–12 carry the conflict and why it matters, never definitions or backstory (that is where the $1M math and brain-research shorts lost a quarter of their viewers). The everyday picture arrives by 0:10 and carries through the whole story. Add a twist every 15–20 s. Include the catch: what the headline leaves out. End on something the viewer can do or say.
- Read every number and quote on the primary page: the paper, the official post or the filing. A search snippet or press summary is not a source. Anything not yet read there goes in the fact-check table marked as a gap, and is settled before the creator records.
- A company that is named gets its logo on screen. Real news gets real footage or real documents, never generated stand-ins. A page is proof, not reading: one sentence on a dark card, 2–3 s, with the result carried by a chart or counter (MOTION.md, "Proof on screen").
- From #18, the visual, motion and sound techniques from YouTube's retention notes (12 Nov) are in MOTION.md: threat vs normal colours, keyword pops, a 0.2 s zoom into the conflict, odometer numbers, the 60/40 split for abstract parts, a sub-bass hit on the open, tactile UI sounds, deeper music ducking, and an end card over the mirrored first frame so the short loops.

## Layout

- `tools/`: voice alignment, captions, SRT, 3D art fetch/upscale, music, SFX, mix
- `template/`: the HyperFrames composition every short starts from (Short #1's 14-scene build)
- `library/3d/`: upscaled 1024 px 3D art. Reuse it before fetching or upscaling anything new
- `brand/`: logo, profile image, cover template
- `shorts/NN-slug/`: one folder per short (e.g. `shorts/02-…/`) holding script, `words.json`, `captions.js`, `index.html`, `sfx.json`, `music.json`, SRT and cover

## Rules

- Story first, never an information dump. 60–90 s unless the creator asks for longer (see Script standards). Something moves on screen in every line, and every cut has a transition.
- The creator records the voice in ElevenLabs (a clone of their own voice, so the AI labels stay on). Video timing follows their WAV, aligned word by word.
- Before rendering, check `npx hyperframes check` and snapshot contact sheets of every scene **and** ±0.1 s around every cut. Fix anything cramped, overlapping or empty.
- Render with `-f 30 -q high`. Verify the MP4: 1080×1920, 30 fps, −14 LUFS. Look at frames pulled from the file itself.
- Keep the session active while a render runs (watch it with a monitor). An idle session once killed a background render.
- Commit sources and new library art. Never commit MP4, WAV or model weights. Deliver those as files.
- No ads, pop-ups, cookie banners, subscribe boxes or browser chrome in any PDF, page crop or screenshot we show. Ask for pages saved from Safari Reader (or the site's print view), check every crop at full size, and crop past or recapture anything that slipped in.
- Real photos: the workspace can't download from Unsplash, Pexels or Hugging Face. Ask the creator to attach them. Never work around a network block.
- Credit "3D art: Microsoft Fluent Emoji (MIT licence)" in every YouTube description that uses it.
- From Short #7: at most 10 generated videos and 5 generated images per short. Everything else is stock (Pexels, Pixabay, Unsplash, Mixkit, Coverr), public-domain or Creative Commons footage, screen recordings, screenshots and our own graphics. The Content Hub's "Visual playbook" lists the techniques.
- Scripts from #7: an expression tag on almost every line; [whispers] at most once, only when the story needs it.
- Scripts from #18 are spoken, not written (YouTube's script notes, 12 Nov):
  - three beats: the paradox hook (0–3 s, one sentence: an anomaly or a high-stakes question); rapid escalation (the obstacle, the data and the tension, no background); the takeaway that rolls back into the hook;
  - about a 6th-grade reading level: short sentences (about 12 words, one breath), active voice, no essay words ("Furthermore", "In addition", "It is important to"), no buzzwords;
  - natural turns a narrator would say: "Here's the weird part:", "Wait, how does that work?";
  - from the source, find the single most surprising finding for an everyday person, and explain the mechanism with a physical, real-world picture (as in #1's hospital);
  - before sending the script for the creator's OK, read it at speaking speed: split any sentence that runs out of breath, and cut any sentence that only gives background.
- The skills in `.claude/skills/` (HyperFrames, motion graphics, sound effects) are technique libraries. Read `MOTION.md` before animating anything; this file, README.md and the project instructions decide the workflow. `.claude/skills/README.md` lists where they clash with our rules. Before hand-building a transition, title or chart, look for a block in `hyperframes-registry`. Every short gets a sound pass with the `sound-effects` skill's CC0 library on top of our own SFX, uses `MOTION.md`'s signature visuals, and passes its quality pass (choreography, motionmaxxing taste and render gates, `review-animations`, an independent critic) before the full render.
- From #9: the first 1–2 seconds lead with the surprising result or a high-stakes question (the brain-research short held 70.8%), never background, a greeting or a slow title card. Every script runs Hook → evidence → twist → takeaway, 60–90 s. Story-led explainers, not how-to tutorials.
- From #12, the hidden word: every short hides one on-screen word that the voice never says. The line before "Follow for more AI, explained like this." is "There's one word in this video I never said out loud. Spotted it? Comment it."
- From #17, every short is a storyboard (MOTION.md, "The storyboard"): one stage the viewer relates to on screen from start to end, a chapter tracker, key facts pinned beside the stage and kept there, a recap of the pins at the end and a last frame that mirrors the first. Engagement means the viewer can follow and remember the whole story, not fast cuts: every visual holds at least 2 s, one new thing at a time. Plan the stage, chapters and pins in the script's hub tab ("Storyboard spine") before the scene sheet.
- From #17, titles are written for the person searching: the human stakes, never the technical term. The YouTube title (main keyword in the first 40 characters) and the description's first line answer a question people search ("how to tell if it's really Mom calling"), then the hook follows. The Shorts feed still brings about 90% of views, so the first 2 seconds matter most (hub Overview, rule 9).
- From #14, one short per episode, posted as it is on YouTube, TikTok and Instagram. No carousels, no Trial Reel variants and no Instagram-only posts (the creator dropped them on 30 Oct).
- No face on camera for now.
- From #13, every short is made for a worldwide audience, not just the UK:
  - Pick stories that matter in any country: global tools (ChatGPT, Gemini, WhatsApp, Gmail), studies with worldwide results. A one-country story only when the mechanism happens everywhere; name the country once, as one example.
  - Plain international English that non-native viewers follow: short words, no idioms or slang, US spelling on screen (math, color). Say "phone", "mail", "mom or dad"; avoid local institutions (NHS, ICO, Parliament) unless the story needs one, then say what it is in a few words.
  - Money in US dollars, or no currency at all. Numbers rounded and said simply ("about one in eight").
  - Every key idea readable from the picture alone, so it lands even with the sound off or for a weaker English speaker.
  - Titles and hashtags in plain English with no local references. Upload translated title, description and subtitles (Spanish, Portuguese, Hindi, Indonesian) for every short.
  - Post at about 14:00 UTC (US morning, UK afternoon, India evening).

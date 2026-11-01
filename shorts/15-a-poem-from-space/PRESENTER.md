# Short #15: you on camera (AI presenter)

From #15 the creator appears on camera as an AI-generated version of himself, holding a mic, on 11 chosen lines
(about 51 s of the 2:56, 29%). The rest stays footage and graphics. The voice stays his ElevenLabs take.

Mirrors the "You on camera" section of the #15 tab in the Content Hub.

## How it works

1. ChatGPT (image generation) turns your reference photo into a character sheet, an expression sheet, an empty room and
   two "hero frames" (you standing in your room, holding the mic, at the exact framing the short needs).
2. Flow (Veo 3.1, Frames to Video, 9:16) starts every clip from a hero frame, so the room, the light, the shirt and the
   framing match from cut to cut. You get the face, the gestures and the mouth moving on the exact words.
3. Flow can't lip-sync to an uploaded voice: Veo invents its own voice for the line in the prompt. So Flow speaks your
   exact line, I mute it, find where each word starts in the clip, and re-time the clip word by word so the mouth lands
   on your recorded take (speed changes kept within about ±20%). I check frames around every word. A clip that still
   drifts gets regenerated, or, only with your OK, a pass through a paid lip-sync tool.

## Which lines (my call)

You take the hook, the turns, the analogies you can act out, the honest catch and the ending. Footage and graphics
carry the explanation (the rocket, the chip, the sun, the orbit, the numbers).

| Clip | In the short | Line | Face and body | Flow | Start frame |
|---|---|---|---|---|---|
| cam01 | 2.9–9.9 | "And the very first thing it said back… was a POEM. (laughs) Okay, to be fair… they asked for one." | Eyebrows up, grin on "poem"; a real laugh; shrug, palm up | 8 s | h01 medium |
| cam02 | 41.5–45.6 | "But why go to all this trouble? Because AI is HUNGRY." | Head tilt, one eyebrow up; beat; leans in, pats stomach, grin | 6 s | h01 |
| cam03 | 58.2–59.7 | "So Google looked UP." | Head back, index finger straight up, eyes follow it | 4 s | h01 |
| cam04 | 77.7–81.7 | "Free sunshine, forever. Perfect? Not quite." | Arm wide, eyes half closed, sunbathing; eyebrow up; wince, hand wobble | 6 s | h01 |
| cam05 | 84.3–86.8 | "You know when your phone gets too hot and has to cool down?" | Holds a phone by its edges as if hot, knowing pained smile | 4 s | h01 |
| cam06 | 90.1–93.6 | "In space? No air. No wind. No water." | Voice drops; counts one finger per phrase, firm head shake | 4 s | h01 |
| cam07 | 93.9–100.6 | "Think of a thermos. The empty gap between its walls keeps your coffee hot. (whispers) Space… is one giant thermos." | Lifts a steel flask, points at its side; leans in close, eyes wide, whispers; slow push-in | 8 s | h01 |
| cam08 | 135.8–142.1 | "Google says aiming those lasers is like hitting a coin from miles away… while you're both moving." | Coin at arm's length, one eye closed, aiming; sways side to side, grins | 8 s | h01 |
| cam09 | 145.3–146.6 | "But let's be honest." | Smile drops; leans in, small nod, steady eyes | 4 s | h02 close |
| cam10 | 154.8–161.2 | "And even the project's leader says it won't be cheaper than Earth for years. So that little poem tells us something big." | Skeptical head shake, palm up; softens into a warm smile | 8 s | h02 |
| cam11 | 167.0–174.2 | "There's one word in this video I never said out loud. Spotted it? Comment it. Follow for more AI, explained like this." | Finger to lips after the line; eyebrows up; points down to the comments; warm nod, two-finger salute | 8 s | h02 |
| cam12 (optional) | 10.2–13.9 | "But that little poem is the start of a really BIG idea." | Leans in; free hand spreads wide on "big" | 4 s | h01 |
| cam13 (optional) | 114.1–115.6 | "Then there's radiation." | Grimace, side glance | 4 s | h01 |
| cam14 (optional) | 129.2–129.9 | "The big dream?" | Eyes light up, looks up and off, smiles | 4 s | h01 |

In the edit I cut away inside some clips (to the poem's light lines on "poem", to the thermos cut-away on "the empty
gap", to the stamped AIR/WIND/WATER), so they play as J-cuts.

## Step 1: ChatGPT (image generation)

Attach in the same chat: 2–3 clear photos of you (front, a three-quarter angle, one smiling; even light, no sunglasses)
and `oneaitrick-logo-lime.png` (the lime square with the "1_" mark). Make the images in this order and keep the chat
going, so each one builds on the last. Check each against your photo; regenerate until it's really you.

### A. Character sheet (landscape 3:2)

```
Create a photorealistic character reference sheet of the man in the attached photos. It will be used by an AI video model to recreate him exactly in many video clips, so likeness and consistency matter more than anything else. Make it look like a real wardrobe and casting reference photographed in a studio, not an illustration.

LIKENESS: This is a real person. Keep his exact face from the photos: face shape and jawline, forehead and hairline, hairstyle and hair color, eyebrows, eye shape and eye color, nose, lips, ears, his facial hair exactly as in the photos, skin tone, natural skin texture with pores, age and build. Do not beautify, slim, smooth, de-age or change his ethnicity, hairstyle or facial hair. The same person in every panel.

OUTFIT (the One AI Trick brand): a clean white short-sleeve crew-neck T-shirt in heavy matte cotton, regular fit. On the left chest, a 7 cm lime-green (#C8FF4D) square badge with slightly rounded corners carrying the bold charcoal (#0B0C10) "1_" mark from the attached logo, printed flat and crisp. A thin lime-green (#C8FF4D) band around each sleeve hem. Dark charcoal chinos and plain dark sneakers. No other logos or text on the clothes.

PROP: a black handheld wireless microphone with a lime-green (#C8FF4D) foam windscreen and no brand name, held in his right hand with the windscreen about 10 cm below his chin, so his mouth is never covered.

LAYOUT: plain light-gray studio background (#E9E9EC), soft even studio light, landscape 3:2, small simple English labels under each panel.
Row 1, full body standing relaxed with the microphone: front, three-quarter left, left profile, three-quarter right, back.
Row 2, head and shoulders, neutral expression, sharp focus on the face: front, three-quarter left, left profile, three-quarter right.
Row 3, details: the chest badge close up on the shirt; his right hand holding the microphone correctly; his face from the front at eye level, mouth slightly open as if mid-word with teeth visible; color swatches for white #FFFFFF, lime #C8FF4D, charcoal #0B0C10, his skin tone and his hair color.

Identical clothing and proportions in every panel. Sharp, high resolution, photorealistic, no stylization.
```

### B. Expressions and gestures (landscape 3:2)

```
Using the same man (attached photos and the character sheet you just made), in the same white T-shirt with the lime-green "1_" chest badge, holding the same black microphone with the lime-green windscreen in his right hand about 10 cm below his chin: create a photorealistic expression and gesture sheet. 3 rows by 4 columns, each panel waist up, plain light-gray background, soft studio light, a short label under each panel.

1 Excited: eyebrows up, eyes wide, big open smile, mid-word.
2 Laughing: a real laugh, eyes creased, head tilted back a little, free left hand shrugging with the palm up.
3 Curious: head tilted, one eyebrow raised, slight squint.
4 Serious: calm, direct eye contact, lips mid-word.
5 Pointing up: left index finger pointing straight up, eyes looking up at it.
6 Blissful: left arm spread wide, eyes half closed, relaxed smile, face tilted up toward sunlight.
7 Skeptical: one eyebrow raised, slight frown, left palm up.
8 Counting: left hand raised showing three fingers, serious face.
9 Whisper: leaning close to the camera, eyes wide, lips near the microphone but fully visible.
10 Holding a plain brushed-steel vacuum flask (no brand) up beside his face in his left hand.
11 Holding a small silver coin between left thumb and index finger at arm's length, one eye closed as if aiming.
12 Finger to lips, playful smile.

Natural hands with five fingers. The same face, hairline, facial hair and skin tone in every panel. No other text or logos.
```

### C. The room, empty (portrait 2:3)

```
A photorealistic photo of a real, lived-in bachelor's bedroom in a small modern city apartment, taken from where a phone on a tripod would stand at chest height. Vertical portrait 2:3. No person in the frame. The middle of the frame is open floor space where a presenter will stand about 1.5 m from the camera, with the room behind him.

Behind, from left to right: a window with sheer white curtains letting in soft late-afternoon daylight; a simple wooden desk against the wall with an open laptop (dark screen, nothing readable), a second monitor with a dark screen, a desk lamp with a warm glow, over-ear headphones, a ceramic mug and a few cables; a black office chair with a gray hoodie over its back; a wall shelf with a few books (plain spines, no readable titles), a small snake plant and a small speaker, and under the shelf a thin lime-green (#C8FF4D) LED strip glowing softly; at the right edge, the corner of a single bed with a dark-gray duvet, slightly rumpled; a backpack on the floor.

Warm off-white walls, light oak floor, a small gray rug. Natural mixed light: cool daylight from the window on the left, warm lamp light at the back right. Shallow depth of field like a phone in portrait mode: background soft but recognizable. Tidy enough but lived-in, a few everyday things out of place, not staged. No posters, no flags, no religious or political items, no brand logos, no readable text anywhere.
```

### D. Hero frame, medium (portrait 2:3): save as `h01_medium.png`

```
Combine the man from the character sheet with the room photo. A photorealistic vertical frame, as if shot on a phone on a tripod at his eye level. He stands in the middle of his bedroom about 1.5 m from the camera, medium shot from the waist up, facing the camera, relaxed and friendly, mouth slightly open as if about to speak. White T-shirt with the lime-green "1_" badge on the left chest; the black microphone with the lime-green windscreen in his right hand about 10 cm below his chin; his left hand relaxed at waist height.

Framing: top of his head about 15% from the top of the frame, his eyes about 30% from the top, the microphone near the middle, his belt line near the bottom edge. Some empty wall above his head. The room behind him exactly as in the room photo, softly out of focus.

Light: soft daylight from the window on the left as the main light on his face, warm lamp glow behind him on the right, the lime LED strip faintly visible. Natural skin texture, exact likeness, no beautifying. No text or captions.
```

### E. Hero frame, close (portrait 2:3): save as `h02_close.png`

```
The same man, room, light, shirt and microphone as the last image, but closer: head and shoulders, leaning very slightly toward the camera. Top of his head about 12% from the top, his eyes about 28% from the top, the microphone windscreen just below his chin. The room behind more out of focus. Calm, direct look into the lens, mouth slightly open as if about to speak. Exact likeness. No text.
```

ChatGPT makes portrait images at 2:3; Flow trims the sides to 9:16, which is why you stay in the middle of D and E.
Send me A–E too: I use them to check likeness and the badge in every clip.

## Step 2: Flow

Settings for every clip:
- New project in Flow. Mode **Frames to Video**. Start frame: `h01_medium.png` or `h02_close.png` (the table says which).
- Model: Veo 3.1. Use Fast to test a prompt, Quality for the take you keep. Aspect ratio **9:16**. Length as in the table.
  Two outputs per prompt.
- Paste the shared block first, then the clip's lines. Download the keeper at **1080p** (upscaled) and save it with the
  clip name (`cam01.mp4`…).
- If Frames to Video drifts from your face, switch that clip to **Ingredients to Video** with three images: the
  character sheet (A), the room (C) and the hero frame (D or E), same prompt.

Before you keep a take, check: it's you; the badge is a lime square with a clean dark "1_"; the mic never covers your
lips; five fingers; it says **exactly** the words in the prompt (listen: if Veo skips or changes a word, regenerate,
because the mouth must make your words); no subtitles, no music; the room matches the hero frame.

### Shared block (paste first, every clip)

```
Vertical 9:16, photorealistic, filmed on a phone on a tripod at eye level, static locked-off camera, natural colors. The man from the start frame, in his bedroom exactly as in the start frame, wearing the white T-shirt with the lime-green "1_" badge on the left chest and holding the black microphone with the lime-green foam windscreen in his right hand about 10 cm below his chin, so his lips stay fully visible. He talks straight into the lens in a clear, warm male voice, with natural, precise lip movements on every word, an expressive face, natural blinks and small head movements. Soft daylight from the window on the left, warm lamp glow behind him. A clean frame with no on-screen text, no captions and no subtitles. Audio: only his voice in a quiet room, no music.
```

### cam01 (8 s, h01)

```
[00:00-00:04] Excited, eyebrows up and eyes wide, he leans slightly toward the camera and says, "And the very first thing it said back... was a poem." He grins on the word "poem".
[00:04-00:05] He laughs for real, eyes creasing.
[00:05-00:08] Still smiling, he shrugs with his free left hand, palm up, and says playfully, "Okay, to be fair... they asked for one."
```

### cam02 (6 s, h01)

```
[00:00-00:02] Curious, head tilted and one eyebrow raised, he asks, "But why go to all this trouble?"
[00:02-00:03] A short silent beat; he narrows his eyes knowingly.
[00:03-00:06] He leans in, pats his stomach with his free left hand and says with a grin, "Because A.I. is hungry."
```

### cam03 (4 s, h01)

```
[00:00-00:02] He says, "So Google looked up," and on the word "up" he tilts his head back and points his free left index finger straight up, his eyes following it.
[00:02-00:04] He holds the pose, looking up, with a small smile. No more words.
```

### cam04 (6 s, h01)

```
[00:00-00:02] Blissful, he spreads his free left arm wide, eyes half closed, face tilted up as if in warm sunlight, and says dreamily, "Free sunshine, forever."
[00:02-00:03] He opens his eyes and raises one eyebrow at the camera: "Perfect?"
[00:03-00:06] A short pause, then he winces and wobbles his flat left hand side to side: "Not quite."
```

### cam05 (4 s, h01)

```
[00:00-00:03] He lifts a plain dark smartphone with no logo in his free left hand, holding it gingerly by its edges as if it is hot, and asks with a knowing, slightly pained smile, "You know when your phone gets too hot and has to cool down?"
[00:03-00:04] He raises his eyebrows at the camera.
```

### cam06 (4 s, h01)

```
[00:00-00:01] Serious, his voice drops: "In space?"
[00:01-00:04] He counts on his free left hand, raising one finger for each phrase, with a small firm head shake each time: "No air. No wind. No water."
```

### cam07 (8 s, h01)

```
[00:00-00:02] Thoughtful, he lifts a plain brushed-steel vacuum flask with no brand into frame with his free left hand: "Think of a thermos."
[00:02-00:05] He turns the flask a little and points at its side with his thumb: "The empty gap between its walls keeps your coffee hot."
[00:05-00:08] He lowers the flask, leans in close to the camera with wide eyes and whispers into the microphone, "Space... is one giant thermos." In this clip only, the camera slowly pushes in toward his face.
```

### cam08 (8 s, h01)

```
[00:00-00:05] He holds a small silver coin between his left thumb and index finger at arm's length, closes one eye and squints at it as if aiming: "Google says aiming those lasers is like hitting a coin from miles away..."
[00:05-00:07] Grinning, he sways his upper body and the coin gently side to side: "...while you're both moving."
[00:07-00:08] He laughs softly.
```

### cam09 (4 s, h02)

```
[00:00-00:02] His smile fades. Serious and direct, he leans slightly toward the camera with a small nod: "But let's be honest."
[00:02-00:04] He holds steady eye contact, silent.
```

### cam10 (8 s, h02)

```
[00:00-00:04] Skeptical, one eyebrow raised, a small head shake, his free left palm up: "And even the project's leader says it won't be cheaper than Earth for years."
[00:04-00:07] His face softens into a warm smile: "So that little poem tells us something big."
[00:07-00:08] He holds the warm smile.
```

### cam11 (8 s, h02)

```
[00:00-00:03] Playful, leaning in, he says, "There's one word in this video I never said out loud," and only after the last word he briefly touches a finger of his free left hand to his lips, so his mouth is never covered while he speaks.
[00:03-00:05] He raises his eyebrows, then points down toward the bottom of the screen: "Spotted it? Comment it."
[00:05-00:08] A warm smile, a small nod and a relaxed two-finger salute: "Follow for more A.I., explained like this."
```

### Optional: cam12, cam13, cam14 (4 s each, h01)

```
cam12: [00:00-00:04] Leaning in as if sharing a secret, then spreading his free left hand wide on "big": "But that little poem is the start of a really big idea."
cam13: [00:00-00:02] He grimaces and glances to the side: "Then there's radiation." [00:02-00:04] He narrows his eyes at the camera.
cam14: [00:00-00:02] His eyes light up and he looks up and off to the side, dreaming: "The big dream?" [00:02-00:04] He smiles.
```

## Step 3: send me

The keepers `cam01.mp4` to `cam11.mp4` (and any optional ones), the hero frames `h01_medium.png` and `h02_close.png`,
and the sheets A–C. Send them with the footage from the material list if you can.

## What changes elsewhere

- Footage no longer needed: v09 (phone in sun), v16 (power lines), v17 (coin); v11 (thermos pour) becomes optional.
- The four Flow space clips (f01–f04) are dropped: I render the satellite, the cluster and the two satellites in 3D,
  so Flow is used only for you.
- Labels: a realistic AI version of a real person means YouTube's "altered or synthetic content" label goes on, along
  with TikTok's "AI-generated content" and Instagram's "AI info".

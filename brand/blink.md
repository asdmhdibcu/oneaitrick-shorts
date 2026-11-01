# Blink: the One AI Trick host (character bible)

From #15, the channel's recurring on-camera host. Blink is the "1_" logo come to life: a small desk robot whose head is
the lime square and whose mouth is the logo's underscore, the cursor. Made in Flow (Veo 3.1, Ingredients to Video) from
three reference pictures; the voice stays the creator's ElevenLabs take. Working name, easy to change.

Why this design: the scorecard found nobody subscribing because there's no recurring face, series or promise. A host
viewers recognise from one frame fixes that, and the shape is the brand itself, so every appearance is also the logo.
Small objects-are-giant comedy (a thermos taller than him, a coin as big as his head) makes every everyday analogy
literal and visual, which is what the channel does.

## Look (keep identical in every prompt)

- **Size:** about 25 cm tall. He lives on the wooden desk in a lived-in bachelor bedroom; everyday objects are huge next
  to him.
- **Head:** a rounded cube about as big as his body, soft matte lime-green (#C8FF4D) plastic. The front is a black glass
  screen with rounded corners and a thin lime rim.
- **Face (on the screen, glowing lime):** two tall rounded eyes; under them a short flat bar, the cursor, which is his
  mouth. The eyes change shape with his mood (below).
- **Body:** a small rounded bean-shaped torso in matte charcoal (#0B0C10). On the chest, a small lime square badge with
  a bold charcoal "1_".
- **Arms and legs:** short charcoal arms with small rounded white hands (a thumb and three fingers); short charcoal legs
  with chunky rounded white feet.
- **Prop:** a tiny black handheld microphone with a lime-green foam windscreen, in his right hand.
- **Finish:** soft-touch matte plastic with tiny real-world scuffs. A real handmade robot filmed in a real room, not a
  cartoon and not a toy advert.

Original design: no resemblance to existing robot characters (no white egg body, no blue eyes, no visor helmet).

## Face language

| Mood | Eyes | Mouth |
|---|---|---|
| Normal | two tall rounded pills | cursor bar |
| Happy, laughing | upside-down U arcs | wide bar |
| Surprised | big round circles | small open square |
| Skeptical | one eye a flat line, one normal | bar tilted |
| Aiming, focused | one eye closed to a line | bar |
| Love, wonder | small hearts | bar |
| Dreaming | small stars | bar |
| Whisper, secret | eyes narrowed to dots | tiny bar |
| Glitch (radiation, errors) | the screen flickers with static | — |

**The mouth is drawn in the edit, not by Flow.** I track the four corners of his screen in every frame and draw the
cursor over Veo's mouth, moving with the creator's voice: it opens on loud vowels, closes between words and, when he's
quiet, blinks on and off like a computer cursor (his signature). Sync is exact. If a frame can't be tracked (a hand in
front, a hard turn), that moment keeps Veo's own mouth, re-timed.

## Personality and movement

Curious, cheeky, a bit dramatic. Big reactions, bouncy quick movements like a small excited animal, lots of head tilts.
He uses his size: leans on things, hugs them, nearly topples. Talks straight into the lens, like a vlogger.

## The three reference pictures (make them in Flow's image tool)

### c1: Blink, full body (portrait): `c1_blink.png`

```
A photorealistic studio photo of Blink, a small handmade robot about 25 cm tall, standing on a plain light-gray tabletop against a plain light-gray background, three-quarter front view, soft even studio light, sharp focus, the whole robot in frame.
HEAD: a rounded cube about as big as his body, in soft matte lime-green (#C8FF4D) plastic. Its front is a black glass screen with rounded corners and a thin lime rim. On the screen, glowing lime-green: two tall rounded eyes, and under them a short flat bar like a computer cursor, which is his mouth.
BODY: a small rounded bean-shaped torso in matte charcoal (#0B0C10) plastic. On the chest, a small lime-green square badge with a bold charcoal "1_" mark.
ARMS AND LEGS: short charcoal arms with small rounded white hands (a thumb and three fingers); short charcoal legs with chunky rounded white feet.
PROP: in his right hand, a tiny black handheld microphone with a lime-green foam windscreen.
A friendly, curious pose, head tilted a little. Soft-touch matte materials with tiny real-world scuffs, like a real handmade robot filmed for a documentary, not a cartoon and not a toy advert. No other text or logos.
```

### c2: Blink's face, close (square): `c2_face.png`

```
A photorealistic close-up of the head of Blink, the same small robot: front view, the head filling most of the frame. A rounded cube head in soft matte lime-green (#C8FF4D) plastic; its front is a black glass screen with rounded corners and a thin lime rim. On the screen, glowing lime-green and centered: two tall rounded eyes, and under them a short flat cursor bar for a mouth. Plain light-gray background, soft studio light, a faint soft reflection on the glass, tiny real-world scuffs on the plastic. No text.
```

### c3: his desk (portrait 9:16): `c3_desk.png`

```
A photorealistic photo taken from a phone lying on a wooden desk, at tabletop height, in a real, lived-in bachelor's bedroom. Vertical 9:16. In the middle foreground, a clear empty spot on the desk where a small 25 cm robot will stand, about 40 cm from the camera. Behind, softly out of focus: an open laptop with a dark screen, a desk lamp with a warm glow, a ceramic mug, a small snake plant and a few cables; further back, a window with sheer curtains on the left letting in soft late-afternoon daylight, a wall shelf with a thin lime-green LED strip glowing under it, and the corner of a bed with a dark-gray duvet on the right. Shallow depth of field like a phone in portrait mode. Warm, natural and lived-in, not staged. No people, no posters, no brand logos, no readable text.
```

## Flow settings (every clip)

- Mode **Ingredients to Video**, the same three pictures every time: `c1_blink.png`, `c2_face.png`, `c3_desk.png`.
- Veo 3.1 (Fast to test, Quality to keep), **9:16**, length per clip, two outputs per prompt, download at **1080p**.
- Paste the shared block for the shot, then the clip's lines.
- Keep a take when: it's clearly Blink (lime cube head, black screen face, charcoal body, white hands and feet, the
  "1_" badge); his screen face is visible and not covered for most of the clip; the gestures land roughly where the
  words are; no subtitles, no music. The words don't have to be perfect any more: I draw the mouth.

### Shared block, medium (full body on the desk)

```
Vertical 9:16, photorealistic, filmed on a phone resting on the desk at the robot's eye level, about 40 cm away, static locked-off camera, shallow depth of field, natural colors. Blink, the small robot from the reference images, exactly as in them: a rounded matte lime-green cube head with a black glass screen face showing two tall glowing lime eyes and a short lime cursor-bar mouth, a small matte charcoal body with a lime "1_" badge on the chest, white hands and white feet. He stands on the wooden desk from the room image, his whole body in frame, his head about a third of the way down the frame; the laptop, the lamp's warm glow, the window light on the left and the bed corner are softly out of focus behind him. Everyday objects on the desk look huge next to him. He holds the tiny black microphone with the lime-green windscreen in his right hand. He talks straight into the lens in a clear, warm male voice; the cursor mouth on his screen moves as he talks, his eyes change shape with his feelings, and he moves with bouncy, expressive body language. A clean frame with no on-screen text, no captions and no subtitles. Audio: only his voice and small desk sounds, no music.
```

### Shared block, close (head and chest)

```
Vertical 9:16, photorealistic, filmed on a phone resting on the desk, close to the robot, at his eye level, static locked-off camera, shallow depth of field, natural colors. Blink, the small robot from the reference images, exactly as in them: a rounded matte lime-green cube head with a black glass screen face showing two tall glowing lime eyes and a short lime cursor-bar mouth, a small matte charcoal body with a lime "1_" badge on the chest. Close-up of his head and chest, his screen face large and facing the lens, the bedroom behind him well out of focus. He holds the tiny black microphone with the lime-green windscreen in his right hand, below his screen. He talks straight into the lens in a clear, warm male voice; the cursor mouth on his screen moves as he talks and his eyes change shape with his feelings. A clean frame with no on-screen text, no captions and no subtitles. Audio: only his voice, no music.
```

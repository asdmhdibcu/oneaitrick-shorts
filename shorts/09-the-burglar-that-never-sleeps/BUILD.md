# Short #9 — "The burglar that never sleeps" (build)

86 s, 39 shots. Microsoft says the China-state-aligned group Storm-0940 used ARTEX, a free, open-source AI pentesting
framework, to try more than 2,250 Microsoft 365 tenants; a 2,900-tries-a-minute password spray got nowhere, and the way
in was ConnectWise Cloud Backup's stolen app credentials, which tenants already trusted. One analogy runs through it:
companies' clouds are houses on a street, ARTEX is a robot burglar, the backup app is a spare key every house handed out.
Sources (the creator's Safari PDFs, git-ignored in `work/pdf/`): Microsoft Security blog 21 Oct 2026 (R1), ConnectWise
Trust Center advisories (R2), The Hacker News on ARTEX (R3), Reuters via Investing.com (R4).

`assets/`, `work/` and renders are git-ignored. Rebuild:

```bash
cd shorts/09-the-burglar-that-never-sleeps
cp -r ../../template/assets/fonts ../../template/assets/grain.png ../../template/assets/base.css assets/
mkdir -p assets/js assets/3d && cp ../../template/assets/js/gsap.min.js assets/js/
for f in email folder locked oldkey house door crown robot key; do cp ../../library/3d/$f.png assets/3d/; done
# the voice: ffmpeg -i ElevenLabs.wav -ar 48000 -ac 1 work/voice_clean.wav; -ar 16000 -ac 1 work/voice16k.wav
python3 ../../tools/align.py work/voice16k.wav work/script_plain.txt words.json     # script.txt without the [tags]
for d in r1_microsoft r2_connectwise r3_artex r4_reuters; do python3 pdfwords.py work/pdf/$d.pdf work/pdf/$d.words.json; done
python3 make_pages.py --sheet          # 21 highlighted crops -> assets/pages, plus Microsoft's Figure 1 (pdfimages -png -f 7 -l 7)
pip install --break-system-packages rembg onnxruntime
python3 make_photo.py                  # the robot picture as two layers (isnet-general-use cut-out over the untouched picture)
python3 build_edit.py                  # conform every shot (edl.py) -> assets/clips, backdrops, work/meta.json (~10 min)
python3 prep_words.py && python3 ../../tools/make_captions.py work/words_cap.json captions.js "$(cat work/emph.txt)"
python3 ../../tools/srt_from_words.py work/words_cap.json short09-captions.srt && python3 prep_words.py --srt
python3 make_audio.py                  # music9.py score + sfx.json + mix -> assets/mix.wav (-14 LUFS)
python3 make_index.py                  # index_template.tpl -> index.html
npx hyperframes render -f 30 -q high -w 2 -o renders/short09-raw.mp4
ffmpeg -i renders/short09-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short09-the-burglar-that-never-sleeps.mp4
```

## What's in it

- **Flow (7 clips of the 10 allowed, 1 image of 5):** the aerial street of robots, the key wall, key-in-lock and the green
  doorway (used three times: the question, the turn, inside), the home office, the boss's chair (the skylight drop is
  kept), the daylight locksmith, the dawn walk-away. G1 and G3 came out as a different robot (no beanie) and aren't used;
  the robot picture (I1) covers G1's moment as a moving photo and G5's first second covers G3's.
- **Stock (Pexels):** rooftops from above, houses and a street lamp (time-lapse, boxed over its own blurred fill), network
  switches, a hand on a door handle (only the first 1.2 s: the door opens on a person after that), a padlock on black, a
  chained door, a key into a lock, key blanks on a red grid, a key being cut, a locksmith (cropped below a flag), a server
  rack.
- **Real pages:** 21 crops from the creator's PDFs with the highlight on the exact words (`make_pages.py` finds each
  phrase in the PDF's word boxes and cuts halfway between lines). Microsoft's Figure 1 comes out of the PDF at full size.
- **My graphics:** 2,250 lights, one per tenant tried; a stopwatch stopping at 2:59; a flip calendar (3AM · SUN ·
  25 DEC, never the spoken word); Microsoft's 14 sectors as 14 doors (finance and government flash on "banks" and
  "governments"); a password-tries gauge and a failed-sign-ins counter to 151,000+; "0 successful"; a 98% lockout ring; one
  key ring threaded to 18 houses with files flying back along the threads; a password box nobody needed; a crown on
  "BOSS"; the burglar/locksmith race; an unbranded "Allow access?" screen.

## New this time

- **Speed ramps** on "KEY" (the key slows to 0.3× as it enters the lock), "TRUSTED" and "cut extra keys", then snap back.
- **Transitions that tell the story:** a front door swings shut and open (hinged, in perspective), the frame closes to a
  keyhole and opens out of it, a record scratch freezes and drains the colour on "Here's the twist", a daylight flash when
  the robot turns out to be the good guys.
- **A moving photo from one generated still:** the robot is cut out (rembg, isnet-general-use) and pushed faster than the
  street behind it, its eye strip flaring on "robot". The untouched picture sits underneath, and the cut-out only ever
  scales up about the feet, so no painted-out halo is ever seen.
- **One silence:** the score (an original heist track, `music9.py`) cuts to nothing on "So how DID it get in?" and crashes
  back in on "KEY".
- **Night and day split screen** for "the burglar and the locksmith run the same robot".

## Gotchas

- The workspace's browser moved: `/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell`
  (the old `chrome-linux/headless_shell` path no longer exists). README's setup line now tries both.
- `hyperframes check` hits its own ~2-minute deadline on this composition (22 videos) and can't finish; contact sheets of
  every shot and ±0.1 s around every cut (`sheet.py`) were the review, as on earlier footage shorts.
- Text that changes over time (the calendar, the password dots) is driven from the playhead (`textAt`), so a renderer
  seeking backwards still shows the right text.
- A stamp or chip on a quote card must not cover the highlight: the "NOW CLOSED SOURCE" stamp sits under the card.

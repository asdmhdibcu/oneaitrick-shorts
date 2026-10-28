# Short #12: "This voice isn't me" (build)

1:22, 17 shots, cut from the #12 video (`longform/this-voice-isnt-me/`): four parts of the long take (`cut_voice.py`: the
hook, Starling's three seconds and the call, Hong Kong, the safe phrase) and T1 from the separate take ("There's one word
in this video I never said out loud. Spotted it? Comment it. Follow for more AI, explained like this."). The hidden word
is **Marmalade**, on the safe-phrase card (k14), never said.

The **Trial Reel** (`VARIANT=trial`, 1:15, 15 shots) swaps the first three shots for T2, "If your mum called you right
now, crying, asking for money... would you know it was really her?" over an incoming call from "Mum" (t01). Everything
after it is the same shots; `edl.py` shifts the body's word anchors by -20 and `fx_short.js` reads `wk()`.

`assets/`, `work/` and renders are git-ignored. Rebuild:

```bash
cd shorts/12-this-voice-isnt-me
mkdir -p assets/img && for d in pages logos fonts js; do cp -r ../../longform/this-voice-isnt-me/assets/$d assets/; done
cp ../../longform/this-voice-isnt-me/assets/grain.png assets/
sed 's/width: 1920px; height: 1080px/width: 1080px; height: 1920px/g' ../../longform/this-voice-isnt-me/assets/base.css > assets/base.css
python3 cut_voice.py                   # both cuts' voices and words.json / words_trial.json
python3 ../../tools/make_captions.py words.json captions.js "ISN'T@2.08,CLONE@5.56,YOURS@11.80,3@15.93,NOW@29.89,FAKE@50.84,DEEPFAKES@52.05,TONIGHT@55.52,PHRASE@66.97,HANG@68.78,COMMENT@76.33"
python3 ../../tools/make_captions.py words_trial.json captions_trial.js "REALLY@4.89,3@9.07,NOW@23.03,FAKE@43.98,DEEPFAKES@45.19,TONIGHT@48.66,PHRASE@60.10,HANG@61.91,COMMENT@69.47"
python3 build_edit.py && VARIANT=trial python3 build_edit.py t01      # conform (9:16) -> assets/clips
python3 make_index.py && VARIANT=trial python3 make_index.py           # -> index.html; trial/index.html (its own project, git-ignored)
python3 make_audio.py && VARIANT=trial python3 make_audio.py           # -> assets/mix.wav, assets/mix_trial.wav (-14 LUFS)
npx hyperframes render -f 30 -q high -w 2 -o renders/short12-raw.mp4   # Bash run_in_background
(cd trial && npx hyperframes render -f 30 -q high -w 2 -o ../renders/short12-trial-raw.mp4)   # then mux assets/mix_trial.wav
ffmpeg -i renders/short12-raw.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -shortest -movflags +faststart renders/short12-this-voice-isnt-me.mp4
python3 make_pack.py                   # carousel (10 x 1080x1350), the Short's cover, the video's thumbnail
```

SRTs: `longform/this-voice-isnt-me/make_srt.py` writes `short12-captions.srt` and `short12-trial-captions.srt` here.

## Differences from the video

- Captions are the Shorts' uppercase karaoke chunks in the 1240–1460 band; visuals stay in 280–1220.
- The score drops out while the phone rings (k06) and crashes back in on "Crying"; it lifts to the major key for the fix.
- The carousel hides the safe phrase (a black bar: "Ours is hidden in the Reel") so it doesn't give the comment game away.

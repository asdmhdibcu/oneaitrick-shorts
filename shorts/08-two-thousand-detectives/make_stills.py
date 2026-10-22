"""Short #8: the voice splice and every hand-cut still, so a rebuild needs no guesswork.

Inputs (git-ignored, from the creator's attachments):
  work/voice_orig.wav   ElevenLabs_2026-10-22T17_34_51 (the approved take, "Over SEVEN HUNDRED")
  work/voice_fix.wav    ElevenLabs_2026-10-22T18_33_09 (full re-take; only "Given the same job ... SEVEN THOUSAND." is used)
  work/img/agents_preprint.pdf, work/raw/ScreenRecording_10-22-2026_19-23-22_1.mp4 (the findings site), work/tm.txt, work/lv.txt
  assets/clips/s18.mp4  (run build_edit.py first for the detective tile)
Outputs: work/voice_clean.wav, work/voice16k.wav, work/splice.json; work/img/{fig-00N.jpg,f1a,f4k,f4a,q4l,atlas_0.3}.png;
         assets/img/{s05_strip.png,s27_strip.png,s48_strip.png,s18_tile.jpg}
Usage: python3 make_stills.py [voice] [stills] [tile]   (default: all)
The splice reproduces words.json to within 10 ms (checked by re-aligning a window around it).
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None
parts = set(sys.argv[1:]) or {"voice", "stills", "tile"}


def run(cmd):
    subprocess.run(cmd, check=True)


if "voice" in parts:
    import numpy as np
    import soundfile as sf
    o, sr = sf.read("work/voice_orig.wav")
    f, _ = sf.read("work/voice_fix.wav")
    # cut in the silence after "case report." and in the pause before "First test"; the re-take sits 0.96 s later
    # than the original at the join, and everything after the splice moves 0.26 s later (THOUSAND is longer).
    c1, c2, OFF, SH, X = 48.15, 55.50, 0.96, 0.26, 480  # X: 10 ms crossfades

    def i(t):
        return int(round(t * sr))
    r = np.linspace(0, 1, X)
    a, b, c = o[:i(c1)], f[i(c1 + OFF):i(c2 + OFF)], o[i(c2 - SH):]
    seg1 = np.concatenate([a[:-X], a[-X:] * (1 - r) + f[i(c1 + OFF) - X:i(c1 + OFF)] * r])
    seg2 = np.concatenate([b[:-X], b[-X:] * (1 - r) + o[i(c2 - SH) - X:i(c2 - SH)] * r])
    sf.write("work/voice_spliced.wav", np.concatenate([seg1, seg2, c]), sr, subtype="PCM_16")
    run(["ffmpeg", "-v", "error", "-y", "-i", "work/voice_spliced.wav", "-ar", "48000", "-ac", "1", "work/voice_clean.wav"])
    run(["ffmpeg", "-v", "error", "-y", "-i", "work/voice_spliced.wav", "-ar", "16000", "-ac", "1", "work/voice16k.wav"])
    json.dump(dict(cut_in=c1, cut_out=c2, fix_offset=OFF, shift_after=SH, xfade_ms=10), open("work/splice.json", "w"), indent=1)
    print("voice", round(len(seg1) / sr + len(seg2) / sr + len(c) / sr, 2), "s")

if "stills" in parts:
    I = "work/img/"
    os.makedirs("work/pdf", exist_ok=True)
    os.makedirs("assets/img", exist_ok=True)
    run(["pdfimages", "-j", "-f", "18", "-l", "21", I + "agents_preprint.pdf", I + "fig"])  # Figs 1-4 at 600 ppi
    fig1, fig4 = Image.open(I + "fig-000.jpg").convert("RGB"), Image.open(I + "fig-003.jpg").convert("RGB")
    fig1.crop((1322, 328, 2882, 1398)).save(I + "f1a.png")   # Fig. 1A, the distributed agents panel
    fig4.crop((3249, 4394, 4329, 5294)).save(I + "f4k.png")  # Fig. 4K, two-choice preference (75% box at 676,258)
    kg = fig4.crop((0, 330, 2250, 1950))                     # Fig. 4A knowledge graph; white out the edge of panel B
    d = ImageDraw.Draw(kg)
    for x0, y0, x1, y1 in [(1920, 380, 2250, 530), (2005, 560, 2250, 965), (2185, 990, 2250, 1395), (2118, 1420, 2250, 1810)]:
        d.rectangle([x0, y0 - 330, x1, y1 - 330], fill=(255, 255, 255))
    kg.save(I + "f4a.png")
    fig4.crop((2380, 5380, 4367, 5592)).save(I + "q4l.png")  # Fig. 4L, the DCTN1 expert comment
    tm, lv = open("work/tm.txt").read().strip(), open("work/lv.txt").read().strip()
    run(["ffmpeg", "-v", "error", "-y", "-ss", "0.3", "-i", "work/raw/ScreenRecording_10-22-2026_19-23-22_1.mp4", "-frames:v", "1",
         "-vf", f"{tm},{lv}", I + "atlas_0.3.png"])
    run(["pdftoppm", "-r", "300", "-f", "1", "-l", "1", "-png", "-singlefile", I + "agents_preprint.pdf", "work/pdf/ag-1"])

    def strip(im, out, maxw=1920):
        if im.size[0] > maxw:
            im = im.resize((maxw, round(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
        im.save(out, optimize=True)
    ag = Image.open("work/pdf/ag-1.png").convert("RGB")
    strip(Image.open(I + "q4l.png"), "assets/img/s05_strip.png")
    strip(ag.crop((260, 1293, 2290, 1830)), "assets/img/s27_strip.png")  # abstract; its 170 px window starts between lines
    strip(ag.crop((190, 10, 2360, 175)), "assets/img/s48_strip.png")     # bioRxiv header: "not certified by peer review"
    print("stills done")

if "tile" in parts:
    run(["ffmpeg", "-v", "error", "-y", "-ss", "1.4", "-i", "assets/clips/s18.mp4", "-frames:v", "1", "work/tmp/s18_mid.png"])
    Image.open("work/tmp/s18_mid.png").convert("RGB").crop((130, 330, 1030, 1250)).save("assets/img/s18_tile.jpg", quality=90)
    print("tile done")

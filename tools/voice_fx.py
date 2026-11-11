#!/usr/bin/env python3
"""Voice effects on chosen lines of the creator's take, without changing timing.

Usage:
  python3 tools/voice_fx.py voice_clean.wav voice_fx.wav phone@12.30-15.80 robot@40.10-42.00
  python3 tools/voice_fx.py --list

Each effect is rendered over the whole take with ffmpeg, then blended in only inside its time range with 15 ms
crossfades, so there are no clicks. Every preset keeps the duration, so words.json and the captions stay valid.
Use effects only where the story asks (a phone call, a robot, a memory, a radio broadcast), and keep the words
readable: listen to every effected line before the mix.
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
from scipy.io import wavfile

PRESETS = {
    # name: (ffmpeg -af chain, what it is for)
    "phone": ("highpass=f=320,lowpass=f=3300,acompressor=threshold=-20dB:ratio=4,volume=1.4",
              "a phone call or voice note"),
    "radio": ("highpass=f=450,lowpass=f=4200,acrusher=bits=11:mix=0.25,aecho=0.8:0.4:18:0.15,volume=1.5",
              "an old broadcast or announcement"),
    "megaphone": ("highpass=f=600,lowpass=f=3000,acrusher=bits=9:mix=0.35,volume=1.8",
                  "a protest, a public warning"),
    "robot": ("afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75,volume=1.2",
              "an AI or machine speaking"),
    "memory": ("lowpass=f=5200,aecho=0.8:0.6:70|160:0.32|0.18,volume=0.95",
               "a flashback or a thought"),
    "space": ("aecho=0.8:0.88:45|90|140:0.38|0.26|0.16,volume=0.95",
              "a big empty room, space, a reveal"),
    "deep": ("asetrate=48000*0.86,aresample=48000,atempo=1.1628,volume=1.1",
             "a villain or a huge machine (pitch down, same length)"),
    "small": ("asetrate=48000*1.16,aresample=48000,atempo=0.8621",
              "a tiny voice, a chatbot bubble (pitch up, same length)"),
}

FADE_S = 0.015


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def load(path):
    rate, data = wavfile.read(path)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    else:
        data = data.astype(np.float32)
    return rate, data


def render(src, chain, tmpdir, name):
    out = os.path.join(tmpdir, f"{name}.wav")
    run(["ffmpeg", "-y", "-i", src, "-af", f"aresample=48000,{chain}", "-ar", "48000", "-ac", "1",
         "-c:a", "pcm_f32le", out])
    return load(out)[1]


def mask(n, rate, start, end):
    t = np.arange(n) / rate
    m = np.clip(np.minimum((t - start) / FADE_S + 0.5, (end - t) / FADE_S + 0.5), 0.0, 1.0)
    return m.astype(np.float32)


def main(argv):
    if len(argv) == 2 and argv[1] == "--list":
        for k, (_, what) in PRESETS.items():
            print(f"{k:10s} {what}")
        return 0
    if len(argv) < 4:
        print(__doc__)
        return 2
    src, dst, specs = argv[1], argv[2], argv[3:]
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "base.wav")
        run(["ffmpeg", "-y", "-i", src, "-ar", "48000", "-ac", "1", "-c:a", "pcm_f32le", base])
        rate, dry = load(base)
        out = dry.copy()
        wet_cache = {}
        for spec in specs:
            name, _, rng = spec.partition("@")
            if name not in PRESETS or "-" not in rng:
                print(f"bad effect '{spec}': use name@start-end, names: {', '.join(PRESETS)}")
                return 2
            a, b = (float(x) for x in rng.split("-", 1))
            if name not in wet_cache:
                wet = render(base, PRESETS[name][0], tmp, name)
                wet = np.pad(wet, (0, max(0, len(dry) - len(wet))))[:len(dry)]
                wet_cache[name] = wet
            m = mask(len(dry), rate, a, b)
            out = out * (1 - m) + wet_cache[name] * m
        peak = float(np.max(np.abs(out))) or 1.0
        if peak > 0.98:
            out *= 0.98 / peak
        wavfile.write(dst, rate, out.astype(np.float32))
    print(f"{dst}: {len(out) / rate:.3f} s (input {len(dry) / rate:.3f} s), effects: {', '.join(specs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

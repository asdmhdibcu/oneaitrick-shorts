"""Measure the ducked score against the voice (K-weighted, BS.1770) for duck settings. Usage: duck_tune.py MG THR RATIO ATT REL"""
import json, subprocess, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import os
D = os.path.dirname(os.path.abspath(__file__)) + "/"
L = 56.95
def kw(x):
    x = lfilter([1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585], x, axis=0)
    return lfilter([1.0, -2.0, 1.0], [1, -1.99004745483398, 0.99007225036621], x, axis=0)
def lufs(x): return -0.691 + 10 * np.log10(np.sum(np.mean(x ** 2, axis=0)) + 1e-15)
VCH = ("aresample=48000,aformat=channel_layouts=mono,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
       "equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=2.5,loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,aformat=channel_layouts=stereo,"
       f"apad=whole_dur={L}")
import os
if not os.path.exists("/tmp/v18.wav"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", D + "assets/voice_raw.wav", "-af", VCH, "/tmp/v18.wav"], check=True)
mg, thr, ratio, att, rel = sys.argv[1:6]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", D + "work/music.wav", "-i", "/tmp/v18.wav", "-filter_complex",
    f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume={mg}[m];[m][1:a]sidechaincompress=threshold={thr}:ratio={ratio}:attack={att}:release={rel}[md]",
    "-map", "[md]", "-t", str(L), "/tmp/md18.wav"], check=True)
_, v = wavfile.read("/tmp/v18.wav"); _, m = wavfile.read("/tmp/md18.wav")
n = min(len(v), len(m)); v = kw(v[:n].astype(float) / 32768); m = kw(m[:n].astype(float) / 32768)
W = json.load(open(D + "words.json")); SR = 48000
sp = np.zeros(n, bool); gp = np.zeros(n, bool)
for w in W: sp[int(w["start"] * SR):int(w["end"] * SR)] = True
for a, b in zip(W, W[1:]):
    if b["start"] - a["end"] >= 0.25: gp[int((a["end"] + 0.1) * SR):int(b["start"] * SR)] = True
ex = np.zeros(n, bool); ex[int(14.7 * SR):int(16.6 * SR)] = True   # the planned silence
sp &= ~ex; gp &= ~ex
lv = lufs(v[sp]); ls = lufs(m[sp]); lg = lufs(m[gp])
print(f"MG {mg} thr {thr} r {ratio} a {att} rel {rel}:  voice {lv:.1f}  music in words {ls:.1f} ({lv-ls:.1f} under)  in gaps {lg:.1f} ({lv-lg:.1f} under)  swing {lg-ls:.1f}")

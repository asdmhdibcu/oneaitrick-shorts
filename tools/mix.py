"""Mix voice + music + SFX into the final Shorts soundtrack (48 kHz stereo, -14 LUFS, -1.5 dBTP).

Usage: python3 mix.py VOICE.wav MUSIC.wav SFX.wav OUT.wav LENGTH_S [music_gain] [sfx_gain]
Voice: high-pass, gentle compression, presence EQ, normalised to -16 LUFS.
Music: ducked under the voice with a sidechain compressor.
Final: two-pass loudnorm to -14 LUFS integrated, true peak -1.5 dB.
"""
import json
import re
import subprocess
import sys

voice, music, sfx, out, length = sys.argv[1:6]
mg = float(sys.argv[6]) if len(sys.argv) > 6 else 0.32
sg = float(sys.argv[7]) if len(sys.argv) > 7 else 0.8
L = float(length)

graph = (
    "[0:a]aresample=48000,aformat=channel_layouts=mono,highpass=f=80,"
    "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
    "equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=2.5,"
    "loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,aformat=channel_layouts=stereo,"
    f"apad=whole_dur={L},asplit=2[v][vsc];"
    f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={mg}[m];"
    "[m][vsc]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=350[md];"
    f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume={sg}[s];"
    f"[v][md][s]amix=inputs=3:normalize=0:duration=longest,atrim=0:{L}"
)


def run(extra, dest):
    cmd = ["ffmpeg", "-hide_banner", "-y", "-i", voice, "-i", music, "-i", sfx,
           "-filter_complex", graph + extra, "-ar", "48000", "-ac", "2"] + dest
    return subprocess.run(cmd, capture_output=True, text=True)


# pass 1: measure
r = run(",loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", ["-f", "null", "-"])
m = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr)[-1])
# pass 2: apply measured values (linear where possible)
extra = (",loudnorm=I=-14:TP=-1.5:LRA=9:linear=true:"
         f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
         f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
r = run(extra, [out])
if r.returncode:
    sys.exit(r.stderr[-2000:])
print("wrote", out)

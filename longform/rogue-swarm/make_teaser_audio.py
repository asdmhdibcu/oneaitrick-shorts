#!/usr/bin/env python3
"""Build the highlights-teaser audio: soundbites on a rhythm + music bed, ducked."""
import subprocess, os, json

os.makedirs("work/teaser", exist_ok=True)
VM = "work/voice_master.wav"
MUS = "work/music_full.wav"
TOTAL = 34.0

# (bite source start/end, place-at time in teaser)  -- fast-cut highlights order
seq = [
    ("leash",        32.73, 34.60,  2.2),
    ("brokein",      37.56, 39.25,  4.8),
    ("mailbox",     143.30,145.85,  7.6),
    ("seventyk",    155.70,158.35, 10.7),
    ("breakthrough",226.90,228.30, 13.9),
    ("sacrifice",    22.80, 24.45, 16.6),
    ("nineteen",    554.40,556.30, 19.9),
    ("scared",      653.30,654.75, 23.3),
    ("real",         46.64, 48.30, 26.6),
]

# 1) extract each bite with short fades
bites=[]
for bid,s,e,at in seq:
    dur=round(e-s,3)
    out=f"work/teaser/b_{bid}.wav"
    fi=min(0.04,dur/4); fo=min(0.08,dur/4)
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",str(s),"-t",str(dur),
        "-i",VM,"-af",f"afade=t=in:st=0:d={fi},afade=t=out:st={max(0,dur-fo):.3f}:d={fo},"
        "aformat=sample_rates=48000:channel_layouts=stereo","-ar","48000","-ac","2",out],check=True)
    bites.append((out,at,dur))

# 2) music bed: take an energetic slice and give it a riser + duck under VO
#    use a climactic slice of the bed (break-in era ~210-250s)
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss","210","-t",str(TOTAL),
    "-i",MUS,"-af",
    f"aformat=sample_rates=48000:channel_layouts=stereo,"
    f"afade=t=in:st=0:d=0.8,afade=t=out:st={TOTAL-1.2}:d=1.2,volume=0.9",
    "-ar","48000","-ac","2","work/teaser/music.wav"],check=True)

# 3) mix: music + all bites placed with adelay, bites louder than bed
inputs=["-i","work/teaser/music.wav"]
for b,at,dur in bites: inputs+=["-i",b]
fc=[]
fc.append("[0:a]volume=0.55[mus]")   # bed sits under
labels=["[mus]"]
for i,(b,at,dur) in enumerate(bites, start=1):
    ms=int(at*1000)
    fc.append(f"[{i}:a]adelay={ms}|{ms},volume=1.35[v{i}]")
    labels.append(f"[v{i}]")
fc.append("".join(labels)+f"amix=inputs={len(labels)}:normalize=0:duration=longest[mx]")
fc.append("[mx]alimiter=limit=0.95,aformat=sample_rates=48000:channel_layouts=stereo[out]")
cmd=["ffmpeg","-y","-hide_banner","-loglevel","error"]+inputs+["-filter_complex",";".join(fc),
     "-map","[out]","-t",str(TOTAL),"work/teaser_mix.wav"]
subprocess.run(cmd,check=True)

# report bite placements for the scene timing
print(json.dumps([{"id":bid,"at":at,"dur":round(e-s,2)} for bid,s,e,at in seq],indent=0))
d=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","default=noprint_wrappers=1:nokey=1","work/teaser_mix.wav"]).decode().strip()
print("teaser_mix.wav duration:",d)

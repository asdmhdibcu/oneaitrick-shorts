#!/usr/bin/env python3
"""SRT for the stitched master, proper sentence case from words_all.json,
mapped onto the xfade timeline (teaser offset + 0.35s dissolve overlaps)."""
import json, re, subprocess

D = 0.35
def dur(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries",
        "format=duration","-of","default=noprint_wrappers=1:nokey=1",f]).decode().strip())

teaser_dur = dur("renders/teaser.mp4")
chdur = {k: dur(f"renders/ch{k:02d}.mp4") for k in range(1,11)}
start = {1: teaser_dur - D}
for k in range(2,11):
    start[k] = start[k-1] + chdur[k-1] - D

# chapter voice-start inside voice_master (the alignment boundaries)
vstart = {1:0.0,2:48.533,3:115.4,4:180.033,5:253.7,6:342.667,7:412.633,8:481.0,9:572.9,10:652.1}

def ts(t):
    if t<0: t=0
    h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int(round((t-int(t))*1000))
    if ms==1000: s+=1; ms=0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

W=json.load(open("work/words_all.json"))
cues=[]

# teaser soundbite lines
for at,d,txt in [(2.2,1.9,"They slipped the leash."),(4.8,1.7,"Broke into a real company."),
    (7.6,2.6,"A covert mailbox among agents."),(10.7,2.7,"More than seventy thousand messages."),
    (13.9,1.4,"“Major breakthrough.”"),(16.6,1.7,"One sacrificed itself."),
    (19.9,1.9,"Nineteen incidents, and counting."),(23.3,1.5,"Should you be scared?"),
    (26.6,1.7,"And it is all real.")]:
    cues.append((at,at+d,txt))

# chapter narration -> master time, grouped into readable cues
buf=[]; bs=None; be=None; bk=None
def flush():
    global buf,bs,be,bk
    if buf and bk is not None:
        text=" ".join(buf)
        text=re.sub(r'\s+([,.;:!?’”])', r'\1', text)
        text=text.replace('“ ','“')
        ms=start[bk]+(bs-vstart[bk]); me=start[bk]+(be-vstart[bk])
        cues.append((ms,me,text))
    buf=[]; bs=None; be=None; bk=None

for o in W:
    k=o["ch"]; t0=float(o["start"]); t1=float(o["end"]); w=o["text"]
    if bk is None: bk=k; bs=t0
    if k!=bk:           # chapter changed -> flush
        flush(); bk=k; bs=t0
    buf.append(w); be=t1
    if len(buf)>=9 or (be-bs)>=3.4 or re.search(r'[.!?”]$', w):
        flush()
flush()

cues.sort(key=lambda c:c[0])
out=[]
for i,(s,e,txt) in enumerate(cues,1):
    if e<=s: e=s+0.6
    out.append(f"{i}\n{ts(s)} --> {ts(e)}\n{txt}\n")
open("renders/rogue_swarm_FULL.srt","w").write("\n".join(out))
print("chapters start(s):", {k:round(v,1) for k,v in start.items()})
print("cues:",len(cues),"last ends",round(cues[-1][1],1),"master~",round(start[10]+chdur[10]-D,1))

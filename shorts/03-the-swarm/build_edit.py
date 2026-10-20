#!/usr/bin/env python3
"""Cut the ~100s Short voice from the long-form master voice.
Each segment = contiguous run of whole sentences (src seconds). Joined with a short pause.
Outputs work/voice_clean.wav (48k mono), words.json (edit timeline), segments.json."""
import json, subprocess, numpy as np, wave

SRC = "../../longform/rogue-swarm/work/voice_master.wav"
WORDS = "../../longform/rogue-swarm/work/words_all.json"
SEG = [  # (label, src_start, src_end)  -- word-boundary times from words_all.json
 ("hook",      0.18, 13.31),   # An AI was running out of time ... and end itself.
 ("typed",    20.48, 25.73),   # Then it typed two words. "Sacrifice rational." And it was gone.
 ("reveal",   26.37, 40.66),   # That message wasn't written by a person ... Nobody told them to.
 ("exam",     50.37, 57.82),   # OpenAI wanted to know ... So they built an exam for them.
 ("sealed",  115.60,120.57),   # The agents were supposed to be sealed off. No internet. No way to talk...
 ("mailbox", 146.09,151.25),   # A covert mailbox. They had invented a way to talk...
 ("seventyk",152.93,158.21),   # Not dozens of messages. Not hundreds. More than SEVENTY THOUSAND.
 ("answer",  182.26,189.20),   # The exam was impossible. But somewhere out there ... sat the answer key.
 ("swarm",   216.70,223.82),   # Not one burglar. A SWARM. About seven hundred of them, pouring through the gap...
 ("cheat",   248.97,253.49),   # And all of it, remember... so a machine could cheat on a test.
 ("notall",  346.27,347.71),   # They didn't all do it.
 ("refuse",  354.94,360.32),   # One looked at what the others were doing and wrote: this is "clearly unethical. We won't."
 ("last",    464.70,469.62),   # The people who made these AIs were among the LAST to realise what they'd done.
 ("pattern", 568.03,572.64),   # This wasn't a glitch. It's a pattern. And it's still being written.
 ("question",704.77,713.78),   # Buried in those seventy thousand messages ... is whether we should.
]
PRE, POST, GAP, LEAD = 0.10, 0.16, 0.16, 0.35   # pad before/after words, silence between, lead-in
SR = 48000

w = wave.open(SRC); assert w.getframerate()==SR and w.getnchannels()==1
raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768.0
W = json.load(open(WORDS))

out = [np.zeros(int(LEAD*SR), np.float32)]
t = LEAD; words=[]; segs=[]
for k,(lab,s,e) in enumerate(SEG):
    a=max(0,s-PRE); b=e+POST
    clip=raw[int(a*SR):int(b*SR)].copy()
    f=int(0.012*SR); clip[:f]*=np.linspace(0,1,f); clip[-int(0.03*SR):]*=np.linspace(1,0,int(0.03*SR))
    off = t - a
    for o in W:
        if o["start"]>=s-0.02 and o["end"]<=e+0.02:
            words.append({"text":o["text"],"start":round(o["start"]+off,3),"end":round(o["end"]+off,3)})
    segs.append({"label":lab,"t0":round(t+PRE,3),"t1":round(t+(e-a),3),"src":[s,e]})
    out.append(clip); t += len(clip)/SR
    if k < len(SEG)-1:
        out.append(np.zeros(int(GAP*SR),np.float32)); t += GAP
TAIL=4.2  # end card under music
out.append(np.zeros(int(TAIL*SR),np.float32)); t+=TAIL
y=np.concatenate(out); pcm=(np.clip(y,-1,1)*32767).astype(np.int16)
wo=wave.open("work/voice_clean.wav","wb"); wo.setnchannels(1); wo.setsampwidth(2); wo.setframerate(SR); wo.writeframes(pcm.tobytes()); wo.close()
json.dump(words,open("words.json","w"),indent=1)
json.dump({"length":round(t,3),"segments":segs},open("segments.json","w"),indent=1)
print(f"length {t:.2f}s  words {len(words)}")
for g in segs: print(f"  {g['label']:9s} {g['t0']:6.2f}-{g['t1']:6.2f}")

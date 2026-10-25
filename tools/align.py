"""Force-align a known script to a voice WAV with pocketsphinx; writes words.json.

Usage: python3 align.py VOICE16K.wav SCRIPT.txt OUT.json
"""
import json
import re
import sys
import wave

from pocketsphinx import Decoder

wav_path, script_path, out_path = sys.argv[1:4]
raw = open(script_path).read()
raw = re.sub(r"<[^>]+>", " ", raw)
SUBS = {"centres": "centers", "thirty-five": "thirty five", "brontë": "bronte", "maths": "math",
        "1845": "eighteen forty-five", "1846": "eighteen forty-six", "1849": "eighteen forty-nine",
        "2031": "twenty thirty-one", "gpt-6": "g p t six", "1800s": "eighteen hundreds", "2000": "two thousand",
        "gpt-rosalind": "g p t rosalind", "d-c-t-n-1": "d c t n one"}  # substring fixes (years are spoken words; digits would be dropped)
# Whole-word fixes, applied after cleaning: spoken forms the dictionary lacks or says wrong
# ("ai" is in the dictionary as one syllable, "eye"; the voice says "A-I").
WORDMAP = {"ai": "a i", "ai's": "a eyes", "ais": "a eyes", "openai": "open a i", "exploitgym": "exploit gym", "openai's": "open a eyes", "refusers": "refuse errs", "fiddly": "fiddle lee", "anthropic": "an throw pick", "crispr": "crisper", "crispr's": "crisper s", "navier": "nav yay", "connectwise": "connect wise", "artex": "art ex", "chatgpt": "chat g p t", "chatgpt's": "chat g p tees", "chatbot": "chat bot", "eu": "e u", "uk": "u k"}
display_words = raw.split()
align_words = []
for w in display_words:
    t = w.lower()
    for a, b in SUBS.items():
        t = t.replace(a, b)
    t = re.sub(r"[^a-z' \-]", "", t).replace("-", " ").strip("'")
    t = " ".join(WORDMAP.get(x, x) for x in t.split())
    align_words.append(t)

text = " ".join(x for x in align_words if x)
with wave.open(wav_path, "rb") as wf:
    assert wf.getframerate() == 16000 and wf.getnchannels() == 1
    audio = wf.readframes(wf.getnframes())

d = Decoder(samprate=16000, bestpath=False)
d.set_align_text(text)
d.start_utt()
d.process_raw(audio, full_utt=True)
d.end_utt()
d.set_alignment()
d.start_utt()
d.process_raw(audio, full_utt=True)
d.end_utt()

words = []
for seg in d.get_alignment():
    name = seg.name
    if name in ("<s>", "</s>", "<sil>") or name.startswith("+"):
        continue
    words.append({"w": name, "start": seg.start / 100.0, "end": (seg.start + seg.duration) / 100.0})

# Map aligned tokens back onto display words (a display word can expand to 2 tokens).
out = []
k = 0
for disp, al in zip(display_words, align_words):
    toks = [t for t in al.split() if t]
    if not toks:
        continue
    seg = words[k:k + len(toks)]
    k += len(toks)
    out.append({"text": disp, "start": round(seg[0]["start"], 3), "end": round(seg[-1]["end"], 3)})
json.dump(out, open(out_path, "w"), indent=1)
print("aligned", len(out), "words; tokens used", k, "of", len(words))

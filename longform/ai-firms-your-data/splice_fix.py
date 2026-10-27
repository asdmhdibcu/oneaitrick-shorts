"""#11: splice the creator's corrected take (27 Oct) over the old "benefiting humanity" lines in the long voice take.

Old (words 153-177): "First thing. Some companies justified using your data with reasons as vague as... "benefiting humanity".
                      The ICO's answer was, basically: yeah, that's not a reason."
New (30 words):      "First thing. Some companies couldn't clearly say WHY they needed your data. And the ICO's view is basically:
                      a reason as vague as... "benefiting humanity"? Yeah, that's not a reason."
(The report gives "benefitting humanity" as an example of a too-broad interest, p.13; it found firms didn't always identify
specific interests, p.25. It doesn't say a firm used the phrase.)
Needs work/voice_clean_v1.wav, words_v1.json (the 25 Oct take and its alignment), work/raw/voice_v2.wav and
work/fix_words.json (tools/align.py on the new take). Writes work/voice_clean.wav, work/voice16k.wav, words.json,
script/script.txt, work/script_plain.txt and work/remap.json (old word index -> new).
Usage: python3 splice_fix.py
"""
import json
import subprocess

OLD_A, OLD_B = 153, 177          # first and last old word replaced
GAIN_DB = -0.9                   # the new take measured 0.9 LU louder than the old segment
SR = 48000
W = json.load(open("words_v1.json"))
F = json.load(open("work/fix_words.json"))
cut_a = round((W[OLD_A - 1]["end"] + W[OLD_A]["start"]) / 2, 3)      # into the pause before "First"
cut_b = round((W[OLD_B]["end"] + W[OLD_B + 1]["start"]) / 2, 3)      # into the pause before "Second."
new_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "work/raw/voice_v2.wav"],
                               capture_output=True, text=True).stdout)
lead = 0.10                                                          # keeps the old pause before "First" (0.35 s)
seg0 = cut_a + lead
delta = seg0 + new_len - cut_b
graph = (f"[0:a]atrim=0:{cut_a},afade=t=out:st={cut_a - 0.01}:d=0.01,asetpts=PTS-STARTPTS[a];"
         f"[1:a]aresample={SR},volume={GAIN_DB}dB,afade=t=in:d=0.005,afade=t=out:st={new_len - 0.02}:d=0.02,adelay={int(lead * 1000)},asetpts=PTS-STARTPTS[b];"
         f"[0:a]atrim={cut_b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01[c];[a][b][c]concat=n=3:v=0:a=1,aformat=sample_rates={SR}:channel_layouts=mono[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work/voice_clean_v1.wav", "-i", "work/raw/voice_v2.wav", "-filter_complex", graph,
                "-map", "[o]", "-c:a", "pcm_s16le", "work/voice_clean.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work/voice_clean.wav", "-ar", "16000", "-ac", "1", "work/voice16k.wav"], check=True)

out = [dict(w) for w in W[:OLD_A]]
out += [dict(text=f["text"], start=round(f["start"] + seg0, 3), end=round(f["end"] + seg0, 3)) for f in F]
out += [dict(text=w["text"], start=round(w["start"] + delta, 3), end=round(w["end"] + delta, 3)) for w in W[OLD_B + 1:]]
json.dump(out, open("words.json", "w"), indent=1)

D = len(F) - (OLD_B - OLD_A + 1)
remap = {k: k for k in range(OLD_A)}
remap.update({k: k + D for k in range(OLD_B + 1, len(W))})
# words inside the replaced lines that the edit points at, matched by meaning
remap.update({153: 153, 166: 176, 167: 177, 168: 165, 169: 167, 173: 178, 174: 179, 175: 180, 177: 182})
json.dump({"delta_s": round(delta, 3), "cut_a": cut_a, "cut_b": cut_b, "seg0": round(seg0, 3), "D": D, "map": remap}, open("work/remap.json", "w"), indent=1)

old_line = ('[conversational] First thing. Some companies justified using your data with reasons as vague as... "benefiting humanity".\n'
            "[chuckles] The ICO's answer was, basically: yeah, that's not a reason.")
new_line = ("[conversational] First thing. Some companies couldn't clearly say WHY they needed your data.\n"
            "[chuckles] And the ICO's view is basically: a reason as vague as... \"benefiting humanity\"? Yeah, that's not a reason.")
s = open("script/script.txt").read()
assert old_line in s, "script line not found"
open("script/script.txt", "w").write(s.replace(old_line, new_line))
p = open("work/script_plain.txt").read()
p = p.replace('First thing. Some companies justified using your data with reasons as vague as... "benefiting humanity".\n'
              "The ICO's answer was, basically: yeah, that's not a reason.",
              "First thing. Some companies couldn't clearly say WHY they needed your data.\n"
              "And the ICO's view is basically: a reason as vague as... \"benefiting humanity\"? Yeah, that's not a reason.")
open("work/script_plain.txt", "w").write(p)
print(f"cut {cut_a}-{cut_b} s, new take {new_len:.2f} s at {seg0:.2f} s; later words move {delta:+.3f} s; {len(out)} words, voice ends {out[-1]['end']:.2f} s")

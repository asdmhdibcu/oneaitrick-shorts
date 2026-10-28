"""#12: upload SRTs in normal case for the video, the Short and the Trial Reel.
The script's emphasis CAPS (IS, OTHER, ENTIRELY, NEW, NOW) go back to normal case; names and acronyms stay.
Usage (from this folder): python3 make_srt.py
"""
import re
import subprocess

S12 = "../../shorts/12-this-voice-isnt-me"
JOBS = [("words.json", "this-voice-isnt-me-captions.srt"),
        (f"{S12}/words.json", f"{S12}/short12-captions.srt"),
        (f"{S12}/words_trial.json", f"{S12}/short12-trial-captions.srt")]
for src, out in JOBS:
    subprocess.run(["python3", "../../tools/srt_from_words.py", src, out], check=True)
    s = open(out).read()
    s = re.sub(r"\b([A-Z]{2,}[A-Z']*)\b", lambda m: m.group(1) if m.group(1) in {"AI", "UK", "US", "CFO"} else m.group(1).lower(), s)
    s = re.sub(r"\bchatgpt", "ChatGPT", s, flags=re.I).replace("openai", "OpenAI")
    for low, fix in (("ai", "AI"), ("uk", "UK"), ("us stocks", "US stocks"), ("cvs", "CVs")):
        s = re.sub(rf"\b{re.escape(low)}\b", fix, s, flags=re.I)
    s = s.replace("money. now.", "money. Now.")
    open(out, "w").write(s)
    print(out, s.count("-->"), "cues")

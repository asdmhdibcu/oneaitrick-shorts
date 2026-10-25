"""#11: upload SRTs in normal case for the video (longform) and the Short.
The script's emphasis CAPS go back to normal case; names and acronyms stay.
Usage (from this folder): python3 make_srt.py
"""
import re
import subprocess

KEEP = {"AI", "UK", "ICO", "ICO's", "AI,"}
JOBS = [("words.json", "ai-firms-your-data-captions.srt"),
        ("../../shorts/11-ai-firms-your-data/words.json", "../../shorts/11-ai-firms-your-data/short11-captions.srt")]
for src, out in JOBS:
    subprocess.run(["python3", "../../tools/srt_from_words.py", src, out], check=True)
    s = open(out).read()
    s = re.sub(r"\b([A-Z]{2,}[A-Z']*)\b", lambda m: m.group(1) if m.group(1) in KEEP else m.group(1).lower(), s)
    s = re.sub(r"\bchatgpt", "ChatGPT", s, flags=re.I).replace("openai", "OpenAI")
    # the SRT tool lowercases all-caps words: put the acronyms and names back
    for low, fix in (("uk", "UK"), ("ico's", "ICO's"), ("ico", "ICO"), ("ai", "AI"), ("xai", "xAI")):
        s = re.sub(rf"\b{re.escape(low)}\b", fix, s, flags=re.I)
    s = s.replace("\ntreat anything", "\nTreat anything")   # the Short's part H starts mid-sentence
    open(out, "w").write(s)
    print(out, s.count("-->"), "cues")

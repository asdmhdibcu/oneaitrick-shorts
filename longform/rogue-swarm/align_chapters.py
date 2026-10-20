"""Align the long-form voice chapter by chapter (full-length alignment runs out of memory).

Pass k aligns chapter k + chapter k+1 against a window starting at chapter k's start.
Chapter k's words come out accurate (they're followed by real text), and the first word of
chapter k+1 gives the next chapter's start. The last pass runs to the end of the audio.

Usage: python3 align_chapters.py work/voice16k.wav script work/words_all.json work/chapters.json
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

voice, script_dir, out_words, out_ch = sys.argv[1:5]
ALIGN = str(Path(__file__).resolve().parents[2] / "tools" / "align.py")
RATE = 2.5     # words per second, conservative
SLACK = 15.0   # seconds of extra audio past the estimate
WORK = Path("work/align_passes"); WORK.mkdir(parents=True, exist_ok=True)

with wave.open(voice) as wf:
    TOTAL = wf.getnframes() / wf.getframerate()

texts = [Path(script_dir, f"ch{k:02d}.txt").read_text() for k in range(1, 11)]


def count_tokens(text):
    """Display words align.py keeps (it drops words whose cleaned form is empty, e.g. a lone dash)."""
    n = 0
    for w in re.sub(r"<[^>]+>", " ", text).split():
        t = re.sub(r"[^a-z' \-]", "", w.lower()).replace("-", " ").strip("'")
        if t.strip():
            n += 1
    return n


counts = [count_tokens(t) for t in texts]
starts = [0.0]
all_words = []
for k in range(10):
    s = starts[k]
    if k < 9:
        text = texts[k] + "\n" + texts[k + 1]
        if k == 8:
            end = TOTAL
        else:
            end = min(TOTAL, s + (counts[k] + counts[k + 1]) / RATE + SLACK)
    else:
        text = texts[k]
        end = TOTAL
    seg_wav = WORK / f"p{k+1:02d}.wav"
    seg_txt = WORK / f"p{k+1:02d}.txt"
    seg_out = WORK / f"p{k+1:02d}.json"
    seg_txt.write_text(text)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-to", f"{end:.3f}", "-i", voice,
                    "-ar", "16000", "-ac", "1", str(seg_wav)], check=True)
    r = subprocess.run(["python3", ALIGN, str(seg_wav), str(seg_txt), str(seg_out)], capture_output=True, text=True)
    if r.returncode != 0:
        print("ALIGN FAILED pass", k + 1, r.stderr[-400:]); sys.exit(1)
    words = json.load(open(seg_out))
    mine = words[:counts[k]]
    for w in mine:
        all_words.append({"text": w["text"], "start": round(w["start"] + s, 3), "end": round(w["end"] + s, 3), "ch": k + 1})
    if k < 9:
        nxt = words[counts[k]]
        starts.append(round(nxt["start"] + s, 3))
    print(f"pass {k+1}: window {s:.2f}-{end:.2f}  ch{k+1} words {len(mine)}  last '{mine[-1]['text']}' ends {mine[-1]['end']+s:.2f}"
          + (f"  -> ch{k+2} starts {starts[-1]:.2f} ('{nxt['text']}')" if k < 9 else ""), flush=True)

json.dump(all_words, open(out_words, "w"), indent=1)

# Frame-exact cut points: middle of the gap between chapters, rounded to 1/30 s.
FPS = 30
cuts = [0.0]
for k in range(1, 10):
    last_prev = [w for w in all_words if w["ch"] == k][-1]["end"]
    first_next = [w for w in all_words if w["ch"] == k + 1][0]["start"]
    mid = (last_prev + first_next) / 2
    cuts.append(round(round(mid * FPS) / FPS, 4))
cuts.append(round(round(TOTAL * FPS) / FPS, 4))
chapters = [{"ch": k + 1, "start": cuts[k], "end": cuts[k + 1], "dur": round(cuts[k + 1] - cuts[k], 4),
             "frames": int(round((cuts[k + 1] - cuts[k]) * FPS))} for k in range(10)]
json.dump(chapters, open(out_ch, "w"), indent=1)
for c in chapters:
    print(f"ch{c['ch']:02d}  {c['start']:8.3f} -> {c['end']:8.3f}  ({c['dur']:6.2f}s, {c['frames']} frames)")

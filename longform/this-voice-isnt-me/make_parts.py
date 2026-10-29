"""Split index.html into two renderable halves (part_a/, part_b/) so each render fits the workspace's 2-hour limit
for a background job. Part B shifts every clip back by T and drives the timeline through a wrapper that plays
tl from T to the end. The halves are silent; the full assets/mix.wav goes on after they are joined.
Usage: python3 make_parts.py [T]   (T defaults to a cut near the middle, on a whole frame)
Then: (cd part_a && npx hyperframes render ...) and (cd part_b && ...), ffmpeg concat, mux assets/mix.wav.
"""
import os
import re
import sys

from edl import DUR, SHOTS

FPS = 30
if len(sys.argv) > 1:
    T = float(sys.argv[1])
else:   # the cut nearest the middle, snapped to a frame
    T = min((s[1] for s in SHOTS[1:]), key=lambda t: abs(t - DUR / 2))
T = round(round(T * FPS) / FPS, 4)
src = open("index.html").read()
src = re.sub(r'\s*<audio id="mix"[^>]*></audio>', "", src)


def fix_videos(html, keep):
    def sub(m):
        tag = m.group(0)
        s = float(re.search(r'data-start="([\d.]+)"', tag).group(1))
        d = float(re.search(r'data-duration="([\d.]+)"', tag).group(1))
        ms = float(re.search(r'data-media-start="([\d.]+)"', tag).group(1))
        r = keep(s, d, ms)
        if r is None:
            return ""
        s, d, ms = r
        tag = re.sub(r'data-start="[\d.]+"', f'data-start="{s:.3f}"', tag)
        tag = re.sub(r'data-duration="[\d.]+"', f'data-duration="{d:.3f}"', tag)
        return re.sub(r'data-media-start="[\d.]+"', f'data-media-start="{ms:.3f}"', tag)
    return re.sub(r'<video [^>]*></video>', sub, html)


def write(folder, html):
    os.makedirs(folder, exist_ok=True)
    open(f"{folder}/index.html", "w").write(html)
    for f in ("assets", "hyperframes.json", "package.json"):
        if not os.path.lexists(f"{folder}/{f}"):
            os.symlink(f"../{f}", f"{folder}/{f}")


durs = f'data-duration="{DUR}"'
a = fix_videos(src, lambda s, d, ms: None if s >= T else (s, min(d, T + 1 - s), ms)).replace(durs, f'data-duration="{T}"')
a = a.replace("const DUR = %s," % DUR, "const DUR = %s," % DUR)   # the timeline keeps its real length; the root stops at T
write("part_a", a)


def shift(s, d, ms):
    if s + d <= T:
        return None
    s2 = s - T
    if s2 < 0:
        return 0.0, d + s2, ms - s2
    return s2, d, ms


b = fix_videos(src, shift).replace(durs, f'data-duration="{round(DUR - T, 4)}"')
old = '''      window.__timelines["main"] = tl;
      tl.seek(0);'''
new = f'''      const PART = gsap.timeline({{ paused: true }});            // part B: play tl from {T} s to the end
      PART.add(tl.tweenFromTo({T}, DUR, {{ ease: "none" }}), 0);
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = PART;
      PART.seek(0);'''
assert b.count(old) == 1
b = b.replace(old, new)
write("part_b", b)
print(f"split at {T} s ({round(T * FPS)} frames): part_a {T} s, part_b {round(DUR - T, 4)} s")

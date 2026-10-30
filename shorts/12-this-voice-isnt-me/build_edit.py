"""Short #12: cut, retime, crop, grade and conform every shot for the 9:16 composition (edl.py), from the video's material.

Inputs (git-ignored): work/raw/<material> (edl.MAT), assets/pages/* (make_pages.py).
Outputs: assets/clips/<id>.mp4 (1920x1080, 30 fps, silent): the footage of V shots; for PHONE shots <id>_ph.mp4 (the screen,
1000 px tall) and <id>.mp4 (its blurred copy as the backdrop); for PAGE and GFX shots a moving blurred backdrop.
assets/img/<id>_last.png for the shot after it (FREEZE, END). Material that hasn't arrived is skipped (a NEEDED slate).
Usage: python3 build_edit.py            (all)
       python3 build_edit.py v07 v21    (only those shots)
"""
import json
import os
import subprocess
import sys

from edl import SHOTS, H, MAT, have, src

GRADES = {
    "ink": "colorbalance=rs=-0.05:gs=-0.01:bs=0.07:rm=-0.02:bm=0.03:rh=0.03:gh=0.01:bh=-0.02,eq=contrast=1.06:saturation=0.86:gamma=0.96",
    "day": "colorbalance=rh=0.02:bh=-0.02,eq=contrast=1.04:saturation=1.0",
    "flow": "eq=contrast=1.03:saturation=0.98",
    "clip": "eq=contrast=1.02",
    "screen": "null",
    "bd": "colorbalance=rs=-0.05:bs=0.07,eq=brightness=-0.16:contrast=0.92:saturation=0.7",
}
DEFAULT_GRADE = {"S": "ink", "G": "flow", "F": "flow", "E": "clip", "R": "screen"}
SHARP = "unsharp=5:5:0.5:5:5:0.0"
W, HH = 1080, 1920
PH = 1000                      # phone screens are set 1000 px tall
os.makedirs("assets/clips", exist_ok=True)
os.makedirs("assets/img", exist_ok=True)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)); print(r.stderr[-2500:]); sys.exit(1)
    return r


def probe(path):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", path])
    j = json.loads(r.stdout)
    return int(j["streams"][0]["width"]), int(j["streams"][0]["height"]), float(j["format"]["duration"])


def enc(out, crf=15):
    return ["-an", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", out]


def fill(w, h, cx=0.5, cy=0.5):
    """Crop to 16:9 around (cx, cy) and scale to 1920x1080."""
    if w / h > W / HH:
        cw, ch = round(h * W / HH / 2) * 2, h
    else:
        cw, ch = w, round(w * HH / W / 2) * 2
    x = round(min(max(cx * w - cw / 2, 0), w - cw)); y = round(min(max(cy * h - ch / 2, 0), h - ch))
    sharp = f",{SHARP}" if ch < 1000 else ""
    return f"crop={cw}:{ch}:{x}:{y},scale={W}:{HH}:flags=lanczos{sharp}"


def timing(sin, span, rate, dur, keys=None):
    """-ss/-t and the setpts chain. keys: [(shot_s, clip_s), ...] piecewise-linear retime measured from the shot start
    (the H handle before the shot holds the first key's frame)."""
    if keys:
        return 0.0, dur, None
    ss = max(0.0, sin - H * rate)
    need = span * rate + 0.3
    hold = max(0.0, (ss + need) - dur + 0.1) / rate
    chain = f"setpts=(PTS-STARTPTS)/{rate:.4f}"
    if rate < 0.97:
        chain += ",minterpolate=fps=30:mi_mode=blend"
    if hold > 0:
        chain += f",tpad=stop_mode=clone:stop_duration={hold + 0.5:.2f}"
    return ss, need, chain


def retime_graph(keys, span):
    """A filter graph that plays [0:v] piecewise-linearly through keys, then holds; output label [rt]."""
    pts = [(-H, keys[0][1])] + [tuple(k) for k in keys]
    if pts[-1][0] < span - H:
        pts.append((span - H, pts[-1][1]))
    parts, labels = [], []
    for i in range(len(pts) - 1):
        (a, ca), (b, cb) = pts[i], pts[i + 1]
        d = b - a
        if d <= 0:
            continue
        lab = f"r{i}"
        if cb - ca < 1 / 60:     # a hold
            parts.append(f"[0:v]trim=start={ca:.4f}:duration=0.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={d + 0.1:.3f},"
                         f"trim=duration={d:.4f},setpts=PTS-STARTPTS,fps=30[{lab}]")
        else:
            f = (cb - ca) / d
            parts.append(f"[0:v]trim=start={ca:.4f}:end={cb:.4f},setpts=(PTS-STARTPTS)/{f:.5f},fps=30,trim=duration={d:.4f}[{lab}]")
        labels.append(f"[{lab}]")
    return ";".join(parts) + f";{''.join(labels)}concat=n={len(labels)}:v=1:a=0[rt]"


def conform_v(sid, sp, span):
    path = src(sp["m"]); w, h, dur = probe(path)
    grade = GRADES[sp.get("grade", DEFAULT_GRADE[sp["m"][0]])]
    ss, need, chain = timing(sp.get("sin", 0.0), span, sp.get("rate", 1.0), dur)
    if sp.get("mode") == "box":   # a vertical source set in the middle over its own blur (720p Flow clips)
        g = (f"[0:v]{chain},split[a][b];[a]scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},boxblur=30:2,"
             f"eq=brightness=-0.14[bg];[b]scale=-2:{HH}:flags=lanczos,{SHARP}[fg];[bg][fg]overlay=(W-w)/2:0,{grade},fps=30,format=yuv420p")
    else:
        g = f"[0:v]{chain},{fill(w, h, sp.get('cx', 0.5), sp.get('cy', 0.5))},{grade},fps=30,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{need:.3f}", "-i", path, "-filter_complex", g,
         "-t", f"{span:.3f}"] + enc(f"assets/clips/{sid}.mp4"))


def conform_phone(sid, sp, span):
    path = src(sp["m"]); w, h, dur = probe(path)
    if sp.get("keys"):
        g = retime_graph(sp["keys"], span) + ";[rt]"
        ss, need = 0.0, dur
    else:
        ss, need, chain = timing(sp.get("sin", 0.0), span, sp.get("rate", 1.0), dur)
        g = f"[0:v]{chain}[rt];[rt]"
    if sp.get("pre"):
        x, y, cw, ch = sp["pre"]
        g += f"crop={cw}:{ch}:{x}:{y}[pc];[pc]"
        w, h = cw, ch
    pw = round(w * PH / h / 2) * 2
    g += (f"split[a][b];[a]scale={pw}:{PH}:flags=lanczos,fps=30,format=yuv420p[ph];"
          f"[b]scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},scale=270:480,boxblur=8:2,scale={W}:{HH}:flags=bicubic,"
          f"{GRADES['bd']},fps=30,format=yuv420p[bd]")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{need:.3f}", "-i", path, "-filter_complex", g,
         "-map", "[ph]", "-t", f"{span:.3f}"] + enc(f"assets/clips/{sid}_ph.mp4", 14) +
        ["-map", "[bd]", "-t", f"{span:.3f}"] + enc(f"assets/clips/{sid}.mp4", 22))
    return pw


def conform_bd(sid, code, span, sin=1.0):
    path = src(code); w, h, dur = probe(path)
    ss, need, chain = timing(sin, span, 1.0, dur)
    g = (f"[0:v]{chain},scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},scale=270:480,boxblur=6:2,"
         f"scale={W}:{HH}:flags=bicubic,{GRADES['bd']},fps=30,format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{need:.3f}", "-i", path, "-filter_complex", g,
         "-t", f"{span:.3f}"] + enc(f"assets/clips/{sid}.mp4", 22))


def last_frame(sid):
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         "-vf", "scale=540:960", f"assets/img/{sid}_last.png"])


if __name__ == "__main__":
    meta = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
    only = set(sys.argv[1:])
    for sid, t0, t1, kind, sp in SHOTS:
        if only and sid not in only:
            continue
        span = t1 - t0 + 2 * H
        need = [c for c in (sp.get("m"), sp.get("bd")) if c and not have(c)]
        if need:
            print(sid, kind, "skipped, needs", ", ".join(need)); meta.pop(sid, None)
            continue
        if os.environ.get("SKIP_EXISTING") and kind in ("V", "PAGE", "GFX") and os.path.exists(f"assets/clips/{sid}.mp4") and os.path.exists(f"assets/img/{sid}_last.png"):
            meta[sid] = {"ok": 1}
            continue
        print(sid, kind, f"{t0:.2f}-{t1:.2f}", flush=True)
        if kind == "V":
            conform_v(sid, sp, span); last_frame(sid); meta[sid] = {"ok": 1}
        elif kind == "PHONE":
            pw = conform_phone(sid, sp, span); meta[sid] = {"ok": 1, "pw": pw, "ph": PH}
            run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}_ph.mp4", "-frames:v", "1",
                 f"assets/img/{sid}_last.png"])
        elif kind in ("PAGE", "GFX"):
            conform_bd(sid, sp["bd"], span, sp.get("bdsin", 1.0)); last_frame(sid); meta[sid] = {"ok": 1}
    json.dump(meta, open("work/meta.json", "w"), indent=1)
    print("done")

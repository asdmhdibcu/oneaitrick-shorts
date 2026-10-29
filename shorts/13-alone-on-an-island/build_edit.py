"""Short #13: cut, retime, crop, grade and conform every shot for the 9:16 composition (edl.py).

Inputs (git-ignored): work/footage/* (stock, Flow), work/replay/<id>/f*.png (the paper's runs, 540x960 at 30 fps),
work/fig/* (the paper's crops).
Outputs: assets/clips/<id>.mp4 (1080x1920, 30 fps, silent): the footage of V shots, a moving blurred backdrop for IMG and
GFX shots; assets/img/<id>_last.png for the END card; assets/img/<fig>.png for IMG cards.
Usage: python3 build_edit.py            (all)
       python3 build_edit.py s07 s21    (only those shots)
"""
import json
import os
import shutil
import subprocess
import sys

from edl import SHOTS, H, MAT, FIGS, have, src

GRADES = {
    "stock": "colorbalance=rs=-0.03:bs=0.04:rh=0.03:bh=-0.02,eq=contrast=1.05:saturation=0.95",
    "flow": "eq=contrast=1.04:saturation=0.96",
    "real": "eq=contrast=1.03:saturation=1.05",
    "bd": "colorbalance=rs=-0.05:bs=0.07,eq=brightness=-0.16:contrast=0.92:saturation=0.7",
}
DEFAULT_GRADE = {"S": "stock", "G": "flow", "R": "real"}
SHARP = "unsharp=5:5:0.5:5:5:0.0"
W, HH = 1080, 1920
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


def inputs(code):
    """ffmpeg input args and (w, h, duration) for a file or a replay frame folder."""
    p = src(code)
    if code.startswith("R"):
        n = len([f for f in os.listdir(p) if f.startswith("f") and f.endswith(".png")])
        return ["-framerate", "30", "-i", os.path.join(p, "f%05d.png")], (540, 960, n / 30)
    return ["-i", p], probe(p)


def fill(w, h, cx=0.5, cy=0.5):
    """Crop to 9:16 around (cx, cy) and scale to 1080x1920."""
    if w / h > W / HH:
        cw, ch = round(h * W / HH / 2) * 2, h
    else:
        cw, ch = w, round(w * HH / W / 2) * 2
    x = round(min(max(cx * w - cw / 2, 0), w - cw)); y = round(min(max(cy * h - ch / 2, 0), h - ch))
    sharp = f",{SHARP}" if ch < 1500 else ""
    return f"crop={cw}:{ch}:{x}:{y},scale={W}:{HH}:flags=lanczos{sharp}"


def timing(sin, span, rate, dur, blend=True):
    ss = max(0.0, sin - H * rate)
    need = span * rate + 0.3
    hold = max(0.0, (ss + need) - dur + 0.1) / rate
    chain = f"setpts=(PTS-STARTPTS)/{rate:.4f}"
    if rate < 0.97 and blend:
        chain += ",minterpolate=fps=30:mi_mode=blend"
    if hold > 0:
        chain += f",tpad=stop_mode=clone:stop_duration={hold + 0.5:.2f}"
    return ss, need, chain


def seek(code, ss, need):
    # files seek before the input; image sequences after it (accurate either way)
    return (["-ss", f"{ss:.3f}", "-t", f"{need:.3f}"], []) if not code.startswith("R") else ([], ["-ss", f"{ss:.3f}", "-t", f"{need:.3f}"])


def conform_v(sid, sp, span):
    code = sp["m"]; inp, (w, h, dur) = inputs(code)
    grade = GRADES[sp.get("grade", DEFAULT_GRADE[code[0]])]
    ss, need, chain = timing(sp.get("sin", 0.0), span, sp.get("rate", 1.0), dur, sp.get("blend", True))
    pre, post = seek(code, ss, need)
    roll = "hflip,vflip," if sp.get("roll180") else ""   # a straight-down camera, turned so the picture reads the right way up
    g = f"[0:v]{chain},{roll}{fill(w, h, sp.get('cx', 0.5), sp.get('cy', 0.5))},{grade},fps=30,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y"] + pre + inp + post + ["-filter_complex", g, "-t", f"{span:.3f}"] + enc(f"assets/clips/{sid}.mp4"))


def conform_bd(sid, code, span, sin=1.0):
    inp, (w, h, dur) = inputs(code)
    ss, need, chain = timing(sin, span, 1.0, dur)
    pre, post = seek(code, ss, need)
    g = (f"[0:v]{chain},scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},scale=270:480,boxblur=6:2,"
         f"scale={W}:{HH}:flags=bicubic,{GRADES['bd']},fps=30,format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y"] + pre + inp + post + ["-filter_complex", g, "-t", f"{span:.3f}"] + enc(f"assets/clips/{sid}.mp4", 22))


def last_frame(sid):
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", f"assets/clips/{sid}.mp4", "-frames:v", "1",
         "-vf", "scale=960:540:force_original_aspect_ratio=increase", f"assets/img/{sid}_last.png"])


if __name__ == "__main__":
    meta = json.load(open("work/meta.json")) if os.path.exists("work/meta.json") else {}
    only = set(sys.argv[1:])
    for name, (path, _) in FIGS.items():
        if os.path.exists(path):
            shutil.copy(path, f"assets/img/{name}.png")
    for sid, t0, t1, kind, sp in SHOTS:
        if only and sid not in only:
            continue
        span = t1 - t0 + 2 * H
        need = [c for c in (sp.get("m"), sp.get("bd")) if c and not have(c)]
        if need:
            print(sid, kind, "skipped, needs", ", ".join(need)); meta.pop(sid, None)
            continue
        print(sid, kind, f"{t0:.2f}-{t1:.2f}", flush=True)
        if kind == "V":
            conform_v(sid, sp, span); last_frame(sid); meta[sid] = {"ok": 1}
        elif kind in ("IMG", "GFX"):
            conform_bd(sid, sp["bd"], span, sp.get("bdsin", 1.0)); last_frame(sid); meta[sid] = {"ok": 1}
    json.dump(meta, open("work/meta.json", "w"), indent=1)
    print("done")

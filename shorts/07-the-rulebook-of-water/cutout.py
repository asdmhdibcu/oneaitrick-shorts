"""Short #7, shot s12: put the words behind the person at the chalkboard.

Cuts the mathematician out of every frame (rembg, u2net_human_seg), then stacks: footage, the real Navier-Stokes
equations from the official Clay problem (chalk white), the title NAVIER-STOKES, and the person back on top.
Overwrites assets/clips/s12.mp4.  Usage: python3 cutout.py
"""
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from rembg import new_session, remove

from edl import SHOTS, H

sid = "s12"
t0, t1 = [(s[1], s[2]) for s in SHOTS if s[0] == sid][0]
W, Hh, FPS = 1080, 1920, 30
T_EQ, T_TITLE = 17.25, 18.20   # equations chalk on with "Mathematicians", title lands on "Navier-Stokes"

# chalk equations: the official problem's equations (1)-(2), white on transparent
eq = Image.open("work/pdf/cl-1.png").convert("L").crop((300, 1040, 2200, 1500))
a = np.clip((235 - np.asarray(eq).astype(np.float32)) / 160, 0, 1)
a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255
grain = np.random.default_rng(3).uniform(0.55, 1.0, a.shape)
eq_rgba = np.zeros(a.shape + (4,), np.float32)
eq_rgba[..., :3] = 1.0
eq_rgba[..., 3] = a * grain
EQ = Image.fromarray((eq_rgba * 255).astype(np.uint8), "RGBA")
EQ = EQ.resize((1000, round(EQ.size[1] * 1000 / EQ.size[0])), Image.LANCZOS)


def title_layer(scale):
    lay = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    f = ImageFont.truetype("assets/fonts/inter.woff2", int(176 * scale))
    try:
        f.set_variation_by_axes([900])
    except Exception:
        pass
    d = ImageDraw.Draw(lay)
    for k, (txt, y) in enumerate((("NAVIER–", 330), ("STOKES", 520))):
        bb = d.textbbox((0, 0), txt, font=f)
        x = 50 - bb[0]
        yy = 430 + (y - 430) * scale
        d.text((x, yy), txt, font=f, fill=(200, 255, 77, 255))
    glow = lay.filter(ImageFilter.GaussianBlur(22))
    return Image.alpha_composite(glow, lay)


frames = int(round((t1 - t0 + 2 * H) * FPS))
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"assets/clips/{sid}.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{Hh}", "-r", "30", "-i", "-",
                        "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        "work/tmp/s12_cut.mp4"], stdin=subprocess.PIPE)
sess = new_session("u2net_human_seg")
cache = {}
for i in range(frames):
    b = dec.stdout.read(W * Hh * 3)
    if len(b) < W * Hh * 3:
        break
    fr = Image.frombytes("RGB", (W, Hh), b)
    t = t0 - H + i / FPS
    m = remove(fr.resize((540, 960)), session=sess, only_mask=True).resize((W, Hh), Image.BILINEAR)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    out = fr.convert("RGBA")
    pe = min(1, max(0, (t - T_EQ) / 0.6))
    if pe > 0:  # chalk the equations on, left to right
        e = EQ.copy()
        al = np.asarray(e.split()[3]).astype(np.float32)
        al[:, int(e.size[0] * pe):] = 0
        e.putalpha(Image.fromarray((al * 0.85).astype(np.uint8)))
        lay = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
        lay.paste(e, (40, 980), e)
        out = Image.alpha_composite(out, lay)
    pt = min(1, max(0, (t - T_TITLE) / 0.28))
    if pt > 0:
        ease = 1 - (1 - pt) ** 3
        tl = title_layer(1.25 - 0.25 * ease)
        tl.putalpha(Image.fromarray((np.asarray(tl.split()[3]).astype(np.float32) * ease).astype(np.uint8)))
        out = Image.alpha_composite(out, tl)
    person = fr.convert("RGBA")
    person.putalpha(m)
    out = Image.alpha_composite(out, person)
    enc.stdin.write(out.convert("RGB").tobytes())
    if i % 20 == 0:
        print("frame", i, "/", frames, flush=True)
enc.stdin.close()
enc.wait()
subprocess.run(["cp", "work/tmp/s12_cut.mp4", f"assets/clips/{sid}.mp4"], check=True)
print("done")

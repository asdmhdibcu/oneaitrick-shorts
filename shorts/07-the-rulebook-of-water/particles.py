"""Short #7: particle renders on black, for screen-blending over footage.

  swarm   exactly 10,000 lights rain in from the top and get pulled into a whirlpool ("ten THOUSAND copies of its AI")
  vortex  a 3D vortex after OpenAI's figure (inward spiral + axial stretching): the core shrinks and spins faster,
          particles coloured by speed, blue (slow) to yellow (fast) to white

Usage: python3 particles.py SCENE OUT.mp4 [seconds]
"""
import subprocess
import sys

import numpy as np
from scipy.ndimage import gaussian_filter

SCENE, OUT = sys.argv[1], sys.argv[2]
SECONDS = float(sys.argv[3]) if len(sys.argv) > 3 else 6.0
W, H, FPS = 1080, 1920, 30
rng = np.random.default_rng(11)


def splat(img, x, y, rgb):
    """Add colours at sub-pixel positions (bilinear)."""
    ok = (x > 0) & (x < W - 2) & (y > 0) & (y < H - 2)
    x, y, rgb = x[ok], y[ok], rgb[ok]
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = (x - x0)[:, None], (y - y0)[:, None]
    for dy, dx, w in ((0, 0, (1 - fx) * (1 - fy)), (0, 1, fx * (1 - fy)), (1, 0, (1 - fx) * fy), (1, 1, fx * fy)):
        np.add.at(img, (y0 + dy, x0 + dx), rgb * w)


def finish(img, core=1.0, glow=0.9, sig=6, halo=10):
    g = np.stack([gaussian_filter(img[..., c], sig) for c in range(3)], -1)
    g2 = np.stack([gaussian_filter(img[..., c], sig * 4) for c in range(3)], -1)
    out = 1 - np.exp(-(img * core + g * glow * 6 + g2 * halo))
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


def colormap(s):
    """OpenAI's figure: teal = slower rotation, orange = faster; white-hot at the very end."""
    stops = np.array([[0.0, 0.05, 0.42, 0.48], [0.35, 0.18, 0.78, 0.82], [0.62, 1.0, 0.55, 0.18], [0.85, 1.0, 0.78, 0.45], [1.0, 1.0, 1.0, 1.0]])
    r = np.interp(s, stops[:, 0], stops[:, 1])
    g = np.interp(s, stops[:, 0], stops[:, 2])
    b = np.interp(s, stops[:, 0], stops[:, 3])
    return np.stack([r, g, b], -1)


ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT],
                      stdin=subprocess.PIPE)
frames = int(SECONDS * FPS)

if SCENE == "swarm":
    # kinematic: each light falls in, meets the whirlpool's rim, then orbits inward (spin ~ 1/r) until swallowed
    N = 10000
    C = np.array([540.0, 1150.0])
    TILT = 0.5
    ts = np.sort(rng.uniform(0, 3.6, N)) + rng.uniform(0, 0.05, N)
    x0 = rng.uniform(-60, W + 60, N)
    r0 = rng.uniform(430, 510, N)
    arm = rng.integers(0, 3, N)
    th0 = np.radians(np.array([200.0, 270.0, 340.0])[arm] + rng.normal(0, 5, N))   # three streams: three spiral arms
    x0 = np.array([150.0, 540.0, 930.0])[arm] + rng.normal(0, 70, N)
    ex, ey = C[0] + r0 * np.cos(th0), C[1] + TILT * r0 * np.sin(th0)
    fall = np.hypot(ex - x0, ey + 60) / rng.uniform(1100, 1600, N)
    OM, KR = 1.2, 0.26
    lime = rng.random(N) < 0.8
    base = np.where(lime[:, None], np.array([0.78, 1.0, 0.3]), np.array([0.3, 0.82, 1.0])) * rng.uniform(0.6, 1.0, (N, 1))
    GY, GX = np.mgrid[0:H, 0:W].astype(np.float32)
    RC = ((GX - C[0]) ** 2 + ((GY - C[1]) / TILT) ** 2)

    def pos(t):
        tau = t - ts
        x = np.full(N, np.nan); y = np.full(N, np.nan)
        f = (tau >= 0) & (tau < fall)
        u = tau[f] / fall[f]
        cx_, cy_ = ex[f], ey[f] - 380                          # bend: arrive moving along the rim
        x[f] = (1 - u) ** 2 * x0[f] + 2 * u * (1 - u) * cx_ + u ** 2 * ex[f]
        y[f] = (1 - u) ** 2 * -60 + 2 * u * (1 - u) * cy_ + u ** 2 * ey[f]
        o = tau >= fall
        T = tau[o] - fall[o]
        r = r0[o] * np.exp(-KR * T)
        th = th0[o] + OM / KR * (np.exp(KR * T) - 1) * (300 / r0[o]) ** 0.5
        alive = r > 34
        xo = np.where(alive, C[0] + r * np.cos(th), np.nan)
        yo = np.where(alive, C[1] + TILT * r * np.sin(th), np.nan)
        x[o], y[o] = xo, yo
        swallowed = (o.sum() - alive.sum())
        return x, y, swallowed, f

    for f in range(frames):
        t = f / FPS
        img = np.zeros((H, W, 3), np.float32)
        for k, a in enumerate((1.0, 0.55, 0.35, 0.22)):        # the light and its short trail
            x, y, sw, falling = pos(t - k / (FPS * 3))
            ok = ~np.isnan(x)
            boost = np.where(falling, 2.6, 1.0)[:, None]
            splat(img, x[ok], y[ok], (base * boost)[ok] * a)
            if k == 0:
                swallowed = sw
        img = np.stack([gaussian_filter(img[..., c], 1.0) for c in range(3)], -1) * 2.1
        core = np.exp(-RC / (2 * 16.0 ** 2)) * min(0.9, swallowed / 3000)
        img += core[..., None] * np.array([0.85, 1.0, 0.55])
        ff.stdin.write(finish(img, core=1.0, glow=0.1, sig=5, halo=1.2).tobytes())
        if f % 60 == 0:
            print(f"swarm frame {f}/{frames}", flush=True)

elif SCENE == "vortex":
    K, M = 300, 520                     # streamlines, samples per line
    th0 = rng.uniform(0, 2 * np.pi, K)
    half = np.where(np.arange(K) % 2 == 0, 1.0, -1.0)   # half the lines stretch up, half down
    jitter = rng.uniform(0.85, 1.15, K)
    s = np.linspace(0, 1, M)
    GY, GX = np.mgrid[0:H, 0:W].astype(np.float32)
    R2C = (GY - H / 2) ** 2 + (GX - W / 2) ** 2
    for f in range(frames):
        t = f / max(1, frames - 1)
        rc = 26 * (1 - 0.9 * t) + 2              # the core shrinks...
        spin = 1.0 + 7.0 * t ** 2                # ...and spins faster
        R0 = 470
        S, TH0 = np.meshgrid(s, th0)             # K x M
        rr = rc + (R0 - rc) * (1 - S) ** 1.6 * jitter[:, None]
        theta = TH0 + spin * 6.0 * np.pi * S ** 1.3 + f / FPS * spin * 2.2
        zz = half[:, None] * (50 + 640 * S ** 2.2) * (1 + 0.5 * t)       # axial stretching
        X3, Y3 = rr * np.cos(theta), rr * np.sin(theta)
        az = 0.35 + 0.25 * t
        el = 0.35
        xc = X3 * np.cos(az) - Y3 * np.sin(az)
        yc = X3 * np.sin(az) + Y3 * np.cos(az)
        yv = zz * np.cos(el) - yc * np.sin(el)
        depth = zz * np.sin(el) + yc * np.cos(el)
        persp = 1400 / (1400 + depth)
        px, py = W / 2 + xc * persp, H / 2 - yv * persp
        speed = np.clip(((spin * rr ** 0.15) / 10) * (S ** 0.7) + 0.15 * S, 0, 1)
        flow = 0.55 + 0.45 * np.sin(40 * S - f / FPS * 18 * spin)        # pulses running along each line
        rgb = colormap(speed) * (flow * (0.35 + 0.65 * S))[..., None] * persp[..., None] * 0.45
        img = np.zeros((H, W, 3), np.float32)
        splat(img, px.ravel(), py.ravel(), rgb.reshape(-1, 3))
        core = np.exp(-R2C / (2 * (8 + 30 * t ** 3) ** 2))
        img += (core * (0.2 + 3.5 * t ** 4))[..., None] * np.array([1.0, 0.95, 0.8])
        ff.stdin.write(finish(img, core=1.0, glow=0.8, sig=4).tobytes())
        if f % 60 == 0:
            print(f"vortex frame {f}/{frames}", flush=True)
ff.stdin.close()
ff.wait()
print("wrote", OUT)

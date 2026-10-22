"""Short #7: real fluid simulations for the "rulebook of water" shots, rendered to vertical video.

This is the incompressible Navier-Stokes equations themselves (2D, periodic), solved the classic way:
semi-Lagrangian advection, a smooth body force (the "push"), viscosity and the pressure projection done exactly
in Fourier space (divergence-free velocity, the "∇·u = 0" rule). Coloured ink is carried by the flow.

Usage: python3 fluid.py SCENE OUT.mp4 [seconds]
Scenes: swirl (stirred whirlpool winding tighter), drop (ink drops falling into still water),
        calm (ink left alone), tea (a spoon circling)
"""
import subprocess
import sys

import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates, zoom

SCENE, OUT = sys.argv[1], sys.argv[2]
SECONDS = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
FPS, SUB = 30, 2                       # frames per second, solver steps per frame
NY, NX = 480, 270                      # velocity grid (9:16)
DY, DX = 960, 540                      # ink grid (2x)
rng = np.random.default_rng(7)

ky = np.fft.fftfreq(NY) * 2 * np.pi
kx = np.fft.fftfreq(NX) * 2 * np.pi
KY, KX = np.meshgrid(ky, kx, indexing="ij")
K2 = KX ** 2 + KY ** 2
K2[0, 0] = 1.0
Y, X = np.mgrid[0:NY, 0:NX].astype(np.float32)
DYY, DXX = np.mgrid[0:DY, 0:DX].astype(np.float32)
cy, cx = NY / 2, NX / 2

u = np.zeros((NY, NX), np.float32)
v = np.zeros((NY, NX), np.float32)
ink = np.zeros((3, DY, DX), np.float32)   # three inks, coloured at render time
NU = {"swirl": 0.02, "drop": 0.01, "calm": 0.01, "tea": 0.02}[SCENE]
PAL = np.array([[200, 255, 77], [79, 208, 255], [245, 248, 255]], np.float32) / 255.0  # lime, cyan, white
if SCENE == "tea":
    PAL = np.array([[255, 196, 120], [255, 240, 220], [200, 255, 77]], np.float32) / 255.0


def project(u, v, dt):
    U, V = np.fft.fft2(u), np.fft.fft2(v)
    P = (KX * U + KY * V) / K2
    U, V = U - KX * P, V - KY * P
    damp = np.exp(-NU * K2 * dt)
    U, V = U * damp, V * damp
    U[0, 0] = V[0, 0] = 0
    return np.real(np.fft.ifft2(U)).astype(np.float32), np.real(np.fft.ifft2(V)).astype(np.float32)


def advect(f, u, v, dt, yy, xx, scale=1.0):
    return map_coordinates(f, [yy - v * dt * scale, xx - u * dt * scale], order=1, mode="grid-wrap")


def blob(cyp, cxp, r):
    return np.exp(-(((DYY - cyp) ** 2 + (DXX - cxp) ** 2) / (2 * r * r))).astype(np.float32)


def fractal(shape, seed, scales=(64, 24, 9, 3), amps=(1, 0.5, 0.25, 0.12)):
    r = np.random.default_rng(seed)
    n = sum(a * gaussian_filter(r.normal(0, 1, shape).astype(np.float32), s, mode="wrap") / max(1e-6, gaussian_filter(r.normal(0, 1, shape).astype(np.float32), s, mode="wrap").std())
            for s, a in zip(scales, amps))
    return (n - n.mean()) / n.std()


def lamb_oseen(rc, peak):
    r2 = (Y - cy) ** 2 + (X - cx) ** 2 + 1e-3
    r = np.sqrt(r2)
    vt = peak * 1.398 * (rc / r) * (1 - np.exp(-r2 / rc ** 2))
    return -(Y - cy) / r * vt, (X - cx) / r * vt


def forces(t, step):
    """Smooth body force for each scene, added to (u, v)."""
    fu = np.zeros_like(u)
    fv = np.zeros_like(v)
    if SCENE == "swirl":
        # a smooth stir whose core keeps shrinking and speeding up: the spiral winds tighter and tighter
        p = t / SECONDS
        rc = 80 * (1 - p) + 14 * p
        tu, tv = lamb_oseen(rc, 1.0 + 3.0 * p)
        fu += (tu - u) * 0.02
        fv += (tv - v) * 0.02
    elif SCENE == "tea":
        ang = t * 2.4
        sy, sx = cy + 70 * np.sin(ang), cx + 70 * np.cos(ang)
        g = np.exp(-((Y - sy) ** 2 + (X - sx) ** 2) / (2 * 9.0 ** 2))
        fu += -np.sin(ang) * g * 0.9
        fv += np.cos(ang) * g * 0.9
    elif SCENE == "drop":
        for k, (t0, x0) in enumerate(((0.2, 0.42), (1.6, 0.6), (3.4, 0.35))):
            if t0 <= t < t0 + 0.7:
                yy = 60 + (t - t0) * 160
                g = np.exp(-((Y - yy) ** 2 + (X - x0 * NX) ** 2) / (2 * 7.0 ** 2))
                fv += g * 0.55
    return fu, fv


def inject(t):
    if SCENE == "swirl" and t < 0.01:
        n = fractal((DY, DX), 3)
        m = fractal((DY, DX), 5, scales=(120, 40), amps=(1, 0.4))
        ink[0] += 0.55 * np.exp(-((n - 0.6) ** 2) / 0.02) * (m > -0.2)
        ink[1] += 0.55 * np.exp(-((n + 0.5) ** 2) / 0.03) * (m < 0.6)
        ink[2] += 0.35 * np.exp(-((n - 0.05) ** 2) / 0.004)
    if SCENE == "tea" and t < 0.05:
        ink[0] += 0.9 * (np.sqrt((DYY - DY / 2) ** 2 + (DXX - DX / 2) ** 2) < 230)
    if SCENE == "tea" and 1.0 < t < 1.6:
        ink[1] += 0.12 * blob(DY / 2 - 120, DX / 2 + 40, 16)  # milk poured in
    if SCENE == "drop":
        for k, (t0, x0) in enumerate(((0.2, 0.42), (1.6, 0.6), (3.4, 0.35))):
            if t0 <= t < t0 + 0.5:
                yy = (60 + (t - t0) * 160) * 2
                ink[k % 3] += 0.35 * blob(yy, x0 * DX, 10)
    if SCENE == "calm" and t < 0.05:
        for k in range(3):
            ink[k] += 1.2 * blob(DY * (0.35 + 0.15 * k), DX * (0.4 + 0.1 * k), 30)


if SCENE == "swirl":
    u, v = lamb_oseen(80, 1.0)
    u, v = u.astype(np.float32), v.astype(np.float32)
if SCENE == "calm":  # gentle leftover motion, then left alone
    u += gaussian_filter(rng.normal(0, 1.2, (NY, NX)).astype(np.float32), 18, mode="wrap")
    v += gaussian_filter(rng.normal(0, 1.2, (NY, NX)).astype(np.float32), 18, mode="wrap")
    u, v = project(u, v, 1.0)


def render(ink):
    col = np.tensordot(PAL, np.clip(ink, 0, None), axes=(0, 0))  # 3 x DY x DX
    col = 1 - np.exp(-1.3 * col)
    glow = np.stack([gaussian_filter(c, 6) for c in col])
    out = np.clip(col * 0.95 + glow * 0.3, 0, 1)
    bg = np.array([4, 5, 10], np.float32)[:, None, None] / 255
    out = bg + out * (1 - bg)
    return (np.transpose(out, (1, 2, 0)) * 255).astype(np.uint8)


FLOWMAP = SCENE in ("swirl", "calm")
if FLOWMAP:
    HY, HX = 1920, 1080
    dmy = np.zeros((DY, DX), np.float32)   # displacement to the starting position, in ink-grid cells
    dmx = np.zeros((DY, DX), np.float32)
    n = fractal((HY, HX), 3, scales=(128, 48, 18, 6), amps=(1, 0.5, 0.25, 0.12))
    m = fractal((HY, HX), 5, scales=(240, 80), amps=(1, 0.4))
    TEX = np.stack([0.9 * np.exp(-((n - 0.6) ** 2) / 0.02) * (m > -0.2),
                    0.9 * np.exp(-((n + 0.5) ** 2) / 0.03) * (m < 0.6),
                    0.6 * np.exp(-((n - 0.05) ** 2) / 0.004)]).astype(np.float32)
    if SCENE == "calm":
        TEX = np.stack([1.3 * np.exp(-(((np.mgrid[0:HY, 0:HX][0] - HY * (0.35 + 0.15 * k)) ** 2 + (np.mgrid[0:HY, 0:HX][1] - HX * (0.4 + 0.1 * k)) ** 2)) / (2 * 60.0 ** 2))
                        * (0.6 + 0.4 * np.exp(-((n - 0.2 * k) ** 2) / 0.05)) for k in range(3)]).astype(np.float32)
    HYY, HXX = np.mgrid[0:HY, 0:HX].astype(np.float32)


def flowmap_frame():
    sy, sx = HY / DY, HX / DX
    zy = zoom(dmy, (sy, sx), order=1, mode="grid-wrap") * sy
    zx = zoom(dmx, (sy, sx), order=1, mode="grid-wrap") * sx
    return np.stack([map_coordinates(c, [(HYY + zy) % HY, (HXX + zx) % HX], order=1, mode="grid-wrap") for c in TEX])


def render_hi(col):
    col = np.tensordot(PAL, np.clip(col, 0, None), axes=(0, 0))
    col = 1 - np.exp(-2.0 * col)
    glow = np.stack([gaussian_filter(c, 10) for c in col])
    out = np.clip(col + glow * 0.35, 0, 1)
    bg = np.array([4, 5, 10], np.float32)[:, None, None] / 255
    out = bg + out * (1 - bg)
    return (np.transpose(out, (1, 2, 0)) * 255).astype(np.uint8)


ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{HX}x{HY}" if FLOWMAP else f"{DX}x{DY}", "-r", str(FPS),
                       "-i", "-", "-vf", "scale=1080:1920:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "14",
                       "-preset", "medium", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
frames = int(SECONDS * FPS)
dt = 1.0
for f in range(frames):
    for s in range(SUB):
        t = (f * SUB + s) / (FPS * SUB)
        fu, fv = forces(t, f)
        u += fu * dt
        v += fv * dt
        u, v = advect(u, u, v, dt, Y, X), advect(v, u, v, dt, Y, X)
        u, v = project(u, v, dt)
        inject(t)
        U2, V2 = zoom(u, 2, order=1, mode="grid-wrap"), zoom(v, 2, order=1, mode="grid-wrap")
        if FLOWMAP:
            dmy, dmx = (advect(dmy, U2, V2, dt, DYY, DXX, scale=2.0) - V2 * 2 * dt,
                        advect(dmx, U2, V2, dt, DYY, DXX, scale=2.0) - U2 * 2 * dt)
        else:
            ink = np.stack([advect(c, U2, V2, dt, DYY, DXX, scale=2.0) for c in ink]) * 0.9995
    ff.stdin.write((render_hi(flowmap_frame()) if FLOWMAP else render(ink)).tobytes())
    if f % 60 == 0:
        print(f"{SCENE}: frame {f}/{frames}, max speed {np.hypot(u, v).max():.2f}", flush=True)
ff.stdin.close()
ff.wait()
print("wrote", OUT)

"""Snapshot times for QC: the middle of every shot, then 0.1 s either side of every cut, and the graphic moments.
Usage: VARIANT=main|trial python3 qc_times.py mids|cuts|moments   -> a comma-separated list for `hyperframes snapshot --at`
"""
import sys

from edl import SHOTS, K, wt

mode = sys.argv[1]
if mode == "mids":
    ts = [(t0 + t1) / 2 for _, t0, t1, _, _ in SHOTS]
elif mode == "cuts":
    ts = [x for _, t0, _, _, _ in SHOTS[1:] for x in (t0 - 0.1, t0 + 0.1)]
else:   # the cues in fx_short.js, a beat after each lands
    ks = [50, 61, 75, 80, 86, 103, 143, 154, 164, 172, 185, 191, 194, 203, 214, 216]
    ts = [wt(K(k)) + 0.35 for k in ks]
print(",".join(f"{round(t, 2):g}" for t in ts))

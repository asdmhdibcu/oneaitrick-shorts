"""Track a point through a conformed shot (OpenCV CSRT) for labels that ride on objects.
Usage: python3 track.py SHOT X Y SIZE  -> work/track_SHOT.json [[x, y], ...] per 30-fps frame of assets/clips/SHOT.mp4"""
import json, sys
import cv2
sid, x, y, s = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
cap = cv2.VideoCapture(f"assets/clips/{sid}.mp4")
ok, fr = cap.read()
mk = cv2.legacy.TrackerCSRT_create if hasattr(cv2, "legacy") else cv2.TrackerCSRT_create
tr = mk()
tr.init(fr, (x - s // 2, y - s // 2, s, s))
pts = [[x, y]]
while True:
    ok, fr = cap.read()
    if not ok:
        break
    ok, b = tr.update(fr)
    pts.append([round(b[0] + b[2] / 2, 1), round(b[1] + b[3] / 2, 1)] if ok else pts[-1])
json.dump(pts, open(f"work/track_{sid}.json", "w"))
print(len(pts), "points", pts[::15])

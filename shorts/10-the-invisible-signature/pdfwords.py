"""Word boxes of a PDF in 300-dpi pixels: python3 pdfwords.py IN.pdf OUT.json -> [{p, t, x, y, w, h}]"""
import json, re, subprocess, sys
xml = subprocess.run(["pdftotext", "-bbox", sys.argv[1], "-"], capture_output=True, text=True).stdout
out, page = [], 0
for line in xml.split("\n"):
    if "<page " in line:
        page += 1
    m = re.search(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*)</word>', line)
    if m:
        x0, y0, x1, y1 = (float(v) * 300 / 72 for v in m.groups()[:4])
        t = m.group(5).replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
        out.append({"p": page, "t": t, "x": round(x0), "y": round(y0), "w": round(x1 - x0), "h": round(y1 - y0)})
json.dump(out, open(sys.argv[2], "w"))
print(len(out), "words,", page, "pages")

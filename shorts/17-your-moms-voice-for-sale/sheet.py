"""Contact sheet: python3 sheet.py DIR OUT.jpg [cols] — every PNG in DIR, in time order, labelled."""
import glob, os, re, sys
from PIL import Image, ImageDraw, ImageFont
d, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 8
fs = sorted(glob.glob(d + "/*.png"), key=lambda f: float(re.findall(r"at-([\d.]+)s", f)[0]))
W, H = 270, 480
rows = (len(fs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * W, rows * (H + 30)), (20, 20, 24))
dr = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except Exception: font = None
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB").resize((W, H))
    x, y = (i % cols) * W, (i // cols) * (H + 30)
    sheet.paste(im, (x, y + 30)); dr.text((x + 8, y + 4), re.findall(r"at-([\d.]+)s", f)[0] + " s", fill=(200, 255, 77), font=font)
sheet.save(out, quality=88); print(out, sheet.size)

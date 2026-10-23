"""Short #9: the robot image (I1) as a moving photo: the picture and the robot cut out of it,
both in frame space (1080x1920), so the composition can push them at different speeds (2.5D parallax).
Needs work/raw/i1_robot.png and rembg (isnet-general-use). Writes assets/img/i1_bg.jpg, i1_fg.png, i1_full.jpg, work/photo/i1.json."""
import json
import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove

S, TOP_Y = 1.42, 330          # scale; the beanie's top lands at y 330
src = Image.open('work/raw/i1_robot.png').convert('RGB')
cut = remove(src, session=new_session('isnet-general-use'), post_process_mask=True)
a = np.array(cut)[:, :, 3]
ys, xs = np.where(a > 128)
top, bot = ys.min(), ys.max()
torso_x = np.median(xs[(ys > top + 250) & (ys < top + 550)])   # the torso, not the pointing hand
W, H = round(src.width * S), round(src.height * S)
ox = round(torso_x * S - 540)
oy = round(TOP_Y - top * S)
print('cut bbox y', top, bot, 'torso x', torso_x, 'offset', ox, oy)

# under the cut-out sits the untouched picture: the cut-out only ever scales up about the feet, so it always covers
# the robot underneath and no painted-out halo is ever seen
plate = src

def frame(im, mode):
    big = im.resize((W, H), Image.LANCZOS)
    canvas = Image.new(mode, (1080, 1920), (0, 0, 0, 0) if mode == 'RGBA' else (6, 8, 14))
    if mode == 'RGB' and oy > 0:   # extend the night sky above the picture: its own top band, flipped and blurred
        band = big.crop((0, 0, W, 6)).resize((W, oy + 40), Image.BILINEAR).filter(ImageFilter.GaussianBlur(24))
        canvas.paste(band, (-ox, 0))
    canvas.paste(big, (-ox, oy), big if mode == 'RGBA' else None)
    return canvas

bg = frame(plate, 'RGB'); fg = frame(cut, 'RGBA')
bg.save('assets/img/i1_bg.jpg', quality=92)
fg.save('assets/img/i1_fg.png', optimize=True)
full = bg.copy(); full.paste(fg, (0, 0), fg); full.save('assets/img/i1_full.jpg', quality=92)
# the eye strip, read off the picture (source pixels 439-550 x 186-212, centre 488, 200): its centre in frame space
eye = [round(488 * S - ox), round(200 * S + oy)]
json.dump({'S': S, 'ox': ox, 'oy': oy, 'eye': eye, 'feet_y': round(bot * S + oy)}, open('work/photo/i1.json', 'w'))
print('eye', eye, 'feet y', round(bot * S + oy))

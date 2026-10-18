"""4x upscale RGBA PNGs with Real-ESRGAN (RRDBNet) on CPU.

Usage: python3 upscale.py MODEL.pth NUM_BLOCKS IN_DIR OUT_DIR [names...]
RGB goes through the network after colour-bleeding transparent pixels (avoids dark halos);
alpha is Lanczos-upscaled and edge-sharpened.
"""
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from scipy import ndimage


class RDB(nn.Module):
    def __init__(self, nf=64, gc=32):
        super().__init__()
        self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1)
        self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
        self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x


class RRDB(nn.Module):
    def __init__(self, nf=64, gc=32):
        super().__init__()
        self.rdb1, self.rdb2, self.rdb3 = RDB(nf, gc), RDB(nf, gc), RDB(nf, gc)

    def forward(self, x):
        return self.rdb3(self.rdb2(self.rdb1(x))) * 0.2 + x


class RRDBNet(nn.Module):
    def __init__(self, nb=23, nf=64, gc=32):
        super().__init__()
        self.conv_first = nn.Conv2d(3, nf, 3, 1, 1)
        self.body = nn.Sequential(*[RRDB(nf, gc) for _ in range(nb)])
        self.conv_body = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        feat = self.conv_first(x)
        feat = feat + self.conv_body(self.body(feat))
        feat = self.lrelu(self.conv_up1(F.interpolate(feat, scale_factor=2, mode="nearest")))
        feat = self.lrelu(self.conv_up2(F.interpolate(feat, scale_factor=2, mode="nearest")))
        return self.conv_last(self.lrelu(self.conv_hr(feat)))


def bleed(rgb, alpha):
    """Fill transparent pixels with the colour of the nearest opaque pixel."""
    mask = alpha < 8
    if not mask.any():
        return rgb
    _, (iy, ix) = ndimage.distance_transform_edt(mask, return_indices=True)
    return rgb[iy, ix]


def main():
    model_path, nb, in_dir, out_dir = sys.argv[1], int(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    names = sys.argv[5:]
    out_dir.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(2)
    net = RRDBNet(nb=nb)
    sd = torch.load(model_path, map_location="cpu")
    sd = sd.get("params_ema", sd.get("params", sd))
    net.load_state_dict(sd, strict=True)
    net.eval()
    files = [in_dir / f"{n}.png" for n in names] if names else sorted(in_dir.glob("*.png"))
    for f in files:
        t0 = time.time()
        im = Image.open(f).convert("RGBA")
        arr = np.asarray(im).astype(np.float32)
        rgb, a = arr[..., :3], arr[..., 3]
        rgb = bleed(rgb, a)
        x = torch.from_numpy(rgb / 255.0).permute(2, 0, 1).unsqueeze(0)
        with torch.no_grad():
            y = net(x).clamp(0, 1)[0].permute(1, 2, 0).numpy()
        H, W = y.shape[:2]
        a_up = np.asarray(Image.fromarray(a.astype(np.uint8)).resize((W, H), Image.LANCZOS)).astype(np.float32) / 255.0
        a_up = np.clip((a_up - 0.5) * 1.6 + 0.5, 0, 1)  # tighten soft upscale edges
        out = np.dstack([y * 255.0, a_up * 255.0]).astype(np.uint8)
        Image.fromarray(out, "RGBA").save(out_dir / f.name, optimize=True)
        print(f.name, f"{time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()

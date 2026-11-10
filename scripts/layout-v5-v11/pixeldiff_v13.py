# V13 PIXEL-DIFF: so render V14 vs V15 cung camera -> % pixel doi + bbox vung doi.
import sys
import numpy as np
from PIL import Image

def diff(a_path, b_path, thresh=12):
    a = np.asarray(Image.open(a_path).convert('RGB')).astype(int)
    b = np.asarray(Image.open(b_path).convert('RGB')).astype(int)
    assert a.shape == b.shape, f"shape mismatch {a.shape} vs {b.shape}"
    d = np.abs(a - b).max(axis=2) > thresh
    pct = 100.0 * d.sum() / d.size
    ys, xs = np.nonzero(d)
    if len(xs):
        bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    else:
        bbox = None
    print(f"{a_path.split('/')[-1]} vs {b_path.split('/')[-1]}: changed {pct:.3f}%  bbox={bbox} (img {a.shape[1]}x{a.shape[0]})")
    return pct, bbox

if __name__ == "__main__":
    L = "/home/hatch/workspace/chua-online-work/layout/"
    for name in ["dilac", "adida", "niche", "flycam", "face_dilac", "face_adida"]:
        try:
            diff(L + f"layout_v14_{name}.png", L + f"layout_v15_{name}.png")
        except FileNotFoundError as e:
            print("skip", name, e.filename)

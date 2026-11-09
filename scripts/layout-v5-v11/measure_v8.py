"""Do V8: so V9 vs V10 tren cac render chuan (PIL).
- Xanh la trong 2 vung flycam (SW, NE) + toan anh
- B-R o mat Di Lac (dilac) — cung box voi measure_v7 + box mat chat
"""
from PIL import Image

L = "/home/hatch/workspace/chua-online-work/layout/"

def load(n):
    return Image.open(L + n).convert("RGB")

def green_share(im, box):
    px = im.crop(box)
    data = list(px.getdata())
    g = sum(1 for (r, gg, b) in data if gg > r + 8 and gg > b + 8 and gg > 55)
    return 100.0 * g / len(data)

def mean_rgb(im, box):
    px = im.crop(box)
    data = list(px.getdata())
    n = len(data)
    return tuple(round(sum(c[i] for c in data) / n, 1) for i in range(3))

print("== FLYCAM: ty le pixel xanh la (%) ==")
for tag, box in [("SW (A Di Da)", (100, 380, 500, 600)),
                 ("NE (sau chanh dien)", (750, 120, 1150, 330)),
                 ("toan anh (tru troi tren)", (0, 150, 1280, 720))]:
    v9 = green_share(load("layout_v9_flycam.png"), box)
    v10 = green_share(load("layout_v10_flycam.png"), box)
    print(f"  {tag}: V9 {v9:.1f}% -> V10 {v10:.1f}%  (delta {v10-v9:+.1f}pp)")

print("== DILAC: mau mat tuong ==")
for f in ["layout_v9_dilac.png", "layout_v10_dilac.png"]:
    im = load(f)
    for box in [(600, 80, 700, 170), (620, 100, 680, 160)]:
        m = mean_rgb(im, box)
        print(f"  {f} {box}: RGB {m}  B-R {round(m[2]-m[0], 1)}")
    # than tuong (vung giua than, tranh chuoi hat)
    m = mean_rgb(im, (450, 330, 560, 430))
    print(f"  {f} torso L: RGB {m}  B-R {round(m[2]-m[0], 1)}")
print("MEASURE V8 DONE")

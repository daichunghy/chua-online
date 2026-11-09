"""Do V7: so V8 vs V9 tren cac render chuan (PIL).
- Xanh la trong 2 vung flycam (SW quanh A Di Da, NE sau chanh dien)
- G-R o hang ngoi duoi cung (mat tien, ground)
- Pixel hong hoa giay (ground + gate, vung them)
- B-R o mat Di Lac (dilac) — vung dau tuong, lay toa do tu anh V8
"""
import sys
from PIL import Image

L = "/home/hatch/workspace/chua-online-work/layout/"

def load(n):
    return Image.open(L + n).convert("RGB")

def green_share(im, box):
    px = im.crop(box)
    w, h = px.size
    data = list(px.getdata())
    g = sum(1 for (r, gg, b) in data if gg > r + 8 and gg > b + 8 and gg > 55)
    return 100.0 * g / len(data)

def mean_rgb(im, box):
    px = im.crop(box)
    data = list(px.getdata())
    n = len(data)
    return tuple(round(sum(c[i] for c in data) / n, 1) for i in range(3))

def pink_px(im, box):
    px = im.crop(box)
    n = 0
    for (r, g, b) in px.getdata():
        if r > 140 and b > 80 and r - g > 30 and b - g > 12:
            n += 1
    return n

def band_gr(im, y0, y1, x0=100, x1=1200):
    # G-R trung binh theo hang ngang trong dai mai
    px = im.crop((x0, y0, x1, y1))
    data = list(px.getdata())
    return round(sum(g - r for (r, g, b) in data) / len(data), 1)

print("== FLYCAM: ty le pixel xanh la (%%) ==")
for tag, box in [("SW (A Di Da)", (100, 380, 500, 600)),
                 ("NE (sau chanh dien)", (750, 120, 1150, 330)),
                 ("toan anh (tru troi tren)", (0, 150, 1280, 720))]:
    v8 = green_share(load("layout_v8_flycam.png"), box)
    v9 = green_share(load("layout_v9_flycam.png"), box)
    print(f"  {tag}: V8 {v8:.1f}% -> V9 {v9:.1f}%  (delta {v9-v8:+.1f}pp)")

print("== GROUND: G-R dai mai duoi (hang ngoi sat mai hien) ==")
for (y0, y1) in [(285, 310), (310, 335)]:
    a = band_gr(load("layout_v8_ground.png"), y0, y1)
    b = band_gr(load("layout_v9_ground.png"), y0, y1)
    print(f"  y {y0}-{y1}: V8 {a} -> V9 {b} (delta {b-a:+.1f})")

print("== GROUND/GATE: pixel hong hoa giay (toan anh) ==")
for f, base in [("layout_v9_ground.png", "layout_v8_ground.png"),
                ("layout_v9_gate.png", "layout_v7_gate.png")]:
    box = (0, 0, 1280, 720)
    print(f"  {f}: {base.split('_')[1]} {pink_px(load(base), box)} -> V9 {pink_px(load(f), box)}")

print("== DILAC: mau mat tuong (vung dau, uoc luong tu anh) ==")
# dau Di Lac o giua tren anh dilac; quet cua so 60x60 quanh tam anh de tim vung trang
for f in ["layout_v7_dilac.png", "layout_v9_dilac.png"]:
    im = load(f)
    print(f"  {f}: tam anh RGB {mean_rgb(im, (590, 200, 690, 300))}")
print("MEASURE V7 DONE")

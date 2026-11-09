"""Do V9: so V10 vs V11 tren cac render chuan (PIL).
- Xanh la flycam (box giong measure_v7/v8)
- Lat trong (paving) trong hop khuon vien o flycam
- G-R dai mai duoi (ground, box giong measure_v7)
- Pixel hong hoa giay (ground + gate, toan anh)
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

def paving_share(im, box):
    # lat xam-nau: 3 kenh gan nhau, R 85..185
    px = im.crop(box)
    data = list(px.getdata())
    p = sum(1 for (r, g, b) in data
            if abs(r - g) < 20 and abs(g - b) < 20 and 85 < r < 185 and 60 < g < 165)
    return 100.0 * p / len(data)

def band_gr(im, y0, y1, x0=100, x1=1200):
    px = im.crop((x0, y0, x1, y1))
    data = list(px.getdata())
    return round(sum(g - r for (r, g, b) in data) / len(data), 1)

def pink_px(im, box):
    px = im.crop(box)
    n = 0
    for (r, g, b) in px.getdata():
        if r > 140 and b > 80 and r - g > 30 and b - g > 12:
            n += 1
    return n

print("== FLYCAM: ty le pixel xanh la (%) ==")
for tag, box in [("SW (A Di Da)", (100, 380, 500, 600)),
                 ("NE (sau chanh dien)", (750, 120, 1150, 330)),
                 ("toan anh (tru troi tren)", (0, 150, 1280, 720))]:
    a = green_share(load("layout_v10_flycam.png"), box)
    b = green_share(load("layout_v11_flycam.png"), box)
    print(f"  {tag}: V10 {a:.1f}% -> V11 {b:.1f}%  (delta {b-a:+.1f}pp)")

print("== FLYCAM: ty le lat trong trong hop khuon vien (170,150,1120,670) ==")
box = (170, 150, 1120, 670)
a = paving_share(load("layout_v10_flycam.png"), box)
b = paving_share(load("layout_v11_flycam.png"), box)
print(f"  paving: V10 {a:.1f}% -> V11 {b:.1f}%  (delta {b-a:+.1f}pp, "
      f"giam tuong doi {(a-b)/a*100:.1f}% — dich >=25%)")

print("== GROUND: G-R dai mai duoi ==")
for (y0, y1) in [(285, 310), (310, 335)]:
    a = band_gr(load("layout_v10_ground.png"), y0, y1)
    b = band_gr(load("layout_v11_ground.png"), y0, y1)
    print(f"  y {y0}-{y1}: V10 {a} -> V11 {b} (delta {b-a:+.1f})")

print("== GROUND/GATE: pixel hong hoa giay (toan anh) ==")
for f, base in [("layout_v11_ground.png", "layout_v10_ground.png"),
                ("layout_v11_gate.png", "layout_v9_gate.png")]:  # V10 khong co gate
    print(f"  {f}: {pink_px(load(base), (0, 0, 1280, 720))} -> "
          f"{pink_px(load(f), (0, 0, 1280, 720))}")
print("MEASURE V9 DONE")

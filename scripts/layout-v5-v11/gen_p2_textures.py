"""GEN TEXTURE P2 bang PIL: cum la alpha x3 tong, tau la co x2, hoa giay,
bien go 2 cong, mat thung cong duc. Chay bang python3 thuong (khong Blender)."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "/home/hatch/workspace/chua-online-work/textures/"
random.seed(20261107)

def jitter(rgb, amt=0.13):
    f = 1.0 + random.uniform(-amt, amt)
    return tuple(max(0, min(255, int(c * f))) for c in rgb)

def leaf_shape(draw, cx, cy, length, width, angle, fill):
    """La don gian: 2 cung doi nhau tao hinh thoi nhon 2 dau."""
    a = math.radians(angle)
    dx, dy = math.cos(a), math.sin(a)
    px, py = -dy, dx
    tip = (cx + dx * length / 2, cy + dy * length / 2)
    base = (cx - dx * length / 2, cy - dy * length / 2)
    left = (cx + px * width / 2, cy + py * width / 2)
    right = (cx - px * width / 2, cy - py * width / 2)
    draw.polygon([base, left, tip, right], fill=fill)

def make_leaf_cluster(path, base_rgb, n=430, size=1024):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # lop bong la (toi) o duoi
    for _ in range(n // 3):
        cx, cy = random.gauss(size/2, size*0.21), random.gauss(size/2, size*0.21)
        dark = tuple(int(c * 0.55) for c in base_rgb)
        leaf_shape(d, cx, cy, random.uniform(30, 62), random.uniform(13, 24),
                   random.uniform(0, 360), jitter(dark, 0.1) + (255,))
    # lop la chinh
    for _ in range(n):
        cx, cy = random.gauss(size/2, size*0.215), random.gauss(size/2, size*0.215)
        col = jitter(base_rgb, 0.16)
        leaf_shape(d, cx, cy, random.uniform(30, 66), random.uniform(13, 26),
                   random.uniform(0, 360), col + (255,))
        # gan la sang
        a = math.radians(random.uniform(0, 360))
    # vai canh nho
    for _ in range(14):
        x0, y0 = random.gauss(size/2, size*0.2), random.gauss(size/2, size*0.2)
        x1, y1 = x0 + random.uniform(-90, 90), y0 + random.uniform(-90, 90)
        d.line([x0, y0, x1, y1], fill=(74, 56, 38, 200), width=4)
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    img.save(path)
    print("leaf cluster ->", path)

def make_palm_frond(path, base_rgb, dry=False):
    W, H = 1024, 512
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # song la: duong cong nhe tu trai sang phai
    pts = [(x, H/2 + 46 * math.sin((x / W) * math.pi * 0.5) - x * 0.03) for x in range(10, W - 10, 8)]
    # la che: tu song ra 2 phia, dai o goc, ngan dan ve ngon
    for i, (x, y) in enumerate(pts):
        t = i / len(pts)
        ll = 205 * (1 - t * 0.72) * random.uniform(0.9, 1.05)
        for sgn in (1, -1):
            ang = math.radians(52 - t * 16) * sgn
            ex, ey = x + math.cos(ang) * ll * 0.42, y + math.sin(ang) * ll
            col = jitter(base_rgb, 0.15)
            if dry and random.random() < 0.22:
                col = jitter((150, 118, 58), 0.12)
            wdt = max(2.2, 5.2 * (1 - t * 0.5))
            d.line([x, y, ex, ey], fill=col + (255,), width=int(wdt))
            d.line([x, y, (x + ex) / 2 + 3, (y + ey) / 2], fill=col + (255,), width=int(wdt))
    d.line(pts, fill=(96, 74, 40, 255), width=9)
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    img.save(path)
    print("palm frond ->", path)

def make_bougainvillea(path, size=1024):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # nen la xanh dam
    for _ in range(300):
        cx, cy = random.gauss(size/2, size*0.23), random.gauss(size/2, size*0.23)
        leaf_shape(d, cx, cy, random.uniform(26, 48), random.uniform(12, 20),
                   random.uniform(0, 360), jitter((46, 84, 40), 0.18) + (255,))
    pinks = [(238, 127, 174), (233, 106, 158), (201, 59, 110), (245, 168, 200), (222, 84, 140)]
    # hoa theo cum
    for _ in range(46):
        gx, gy = random.gauss(size/2, size*0.22), random.gauss(size/2, size*0.22)
        for _ in range(random.randint(5, 11)):
            cx, cy = gx + random.uniform(-46, 46), gy + random.uniform(-46, 46)
            col = jitter(random.choice(pinks), 0.1)
            r = random.uniform(9, 17)
            for k in range(3):
                a = math.radians(k * 120 + random.uniform(-14, 14))
                ox, oy = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
                d.ellipse([ox - r * 0.62, oy - r * 0.5, ox + r * 0.62, oy + r * 0.5], fill=col + (255,))
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(250, 240, 210, 255))
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    img.save(path)
    print("bougainvillea ->", path)

def wood_board(w, h, base=(66, 44, 26)):
    img = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(img)
    for y in range(0, h, h // 4):
        d.line([0, y, w, y], fill=(40, 26, 14), width=3)
    for _ in range(2600):
        x, y = random.uniform(0, w), random.uniform(0, h)
        d.point((x, y), fill=jitter(base, 0.22))
    for _ in range(46):
        x, y = random.uniform(0, w), random.uniform(0, h)
        d.line([x, y, x + random.uniform(20, 90), y], fill=jitter((88, 60, 34), 0.15), width=2)
    return img

def make_sign(path, text):
    img = wood_board(1024, 256)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 1013, 245], outline=(201, 162, 39), width=5)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 118)
    d.text((512, 132), text, font=font, anchor="mm", fill=(30, 18, 6))
    d.text((510, 128), text, font=font, anchor="mm", fill=(232, 199, 102))
    img.save(path)
    print("sign ->", path, text)

def make_merit_front(path):
    img = wood_board(512, 512, base=(84, 34, 26))
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, 497, 497], outline=(201, 162, 39), width=6)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 104)
    d.text((258, 262), "CÔNG ĐỨC", font=font, anchor="mm", fill=(30, 14, 4))
    d.text((256, 258), "CÔNG ĐỨC", font=font, anchor="mm", fill=(232, 199, 102))
    img.save(path)
    print("merit front ->", path)

make_leaf_cluster(OUT + "leaf_cluster_A.png", (62, 107, 52))    # #3E6B34
make_leaf_cluster(OUT + "leaf_cluster_B.png", (76, 122, 60))    # ~#4C7A3C
make_leaf_cluster(OUT + "leaf_cluster_C.png", (92, 132, 70))    # #5C8446
make_palm_frond(OUT + "palm_frond_A.png", (63, 112, 49))
make_palm_frond(OUT + "palm_frond_B.png", (86, 128, 58), dry=True)
make_bougainvillea(OUT + "bougainvillea.png")
make_sign(OUT + "sign_phuong_tien.png", "PHƯƠNG TIỆN")
make_sign(OUT + "sign_tinh_do.png", "TỊNH ĐỘ")
make_merit_front(OUT + "cong_duc_front.png")
print("ALL TEXTURES DONE")

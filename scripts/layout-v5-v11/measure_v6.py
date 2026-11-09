# -*- coding: utf-8 -*-
"""ĐO NGHIỆM THU P1 (KE_HOACH_TOAN_DIEN_V6) trên render layout_v6_*.
Tiêu chí:
 1) nón/túi: % pixel hồng bão hòa (hue hồng/magenta, S>0.45, sen) vùng nón nhân vật ở ground
    -> phai < 2% (trừ họa tiết sen nhỏ tren non)
 2) vàng mặt tiền: mean vùng tường nắng ground (mask V5) vs đích (217,164,65) ±12/kênh
 3) trời: số tông xanh phân biệt ở dải trời flycam/ground/gate + tông ấm ở trời dilac
 4) cổng: (đo proxy) độ bão hòa TB vùng mặt cổng ở gate render tăng so với v5 + soi mắt
 5) nền đất: mean mặt nạ cỏ flycam (y 0.52..0.95H, xanh lá nhạt) vs đích (138,122,99) ±12
 6) AO compositor: kiểm chứng bằng render test (đã có) + độ tối hốc vòm ground >= V5
 7) bảng chữ: soi mắt 3 render plaque (script chỉ liệt kê file)
"""
from PIL import Image
import colorsys, os

L = os.path.expanduser('~/workspace/chua-online-work/layout/')
files = {'flycam': 'layout_v6_flycam.png', 'ground': 'layout_v6_ground.png',
         'gate': 'layout_v6_gate.png', 'dilac': 'layout_v6_dilac.png',
         'flycam5': 'layout_v5_flycam.png', 'gate5': 'layout_v5_gate.png',
         'ground5': 'layout_v5_ground.png'}

def mean(region_img):
    px = list(region_img.getdata())
    n = len(px)
    return tuple(round(sum(c[i] for c in px) / n, 1) for i in range(3)) if n else None

def wall_mask(im):
    W, H = im.size
    r, g, b = im.split()
    import PIL.ImageChops as C
    m = r.point(lambda v: 255 if v > 180 else 0)
    mg = g.point(lambda v: 255 if v > 140 else 0)
    mb = b.point(lambda v: 255 if v < 130 else 0)
    m = C.multiply(m, mg); m = C.multiply(m, mb)
    m = m.crop((0, int(0.26 * H), W, int(0.42 * H)))
    out = Image.new('RGB', (W, int(0.16 * H)))
    out.paste(im.crop((0, int(0.26 * H), W, int(0.42 * H))), (0, 0), m)
    sel = [p for p in out.getdata() if p != (0, 0, 0)]
    return (tuple(round(sum(c[i] for c in sel) / len(sel), 1) for i in range(3)), len(sel)) if sel else (None, 0)

def sky_tones(im, label):
    W, H = im.size
    bands = []
    for (y0, y1) in ((0.0, 0.08), (0.08, 0.16), (0.16, 0.30)):
        strip = im.crop((0, int(y0 * H), W, int(y1 * H)))
        blue = [p for p in strip.getdata() if p[2] > p[0] + 15 and p[2] > 90]
        if blue:
            bands.append(mean(Image.new('RGB', (len(blue), 1)) if False else _from_list(blue)))
    print(f"  sky[{label}] bands:", bands)
    return bands

def _from_list(pxs):
    im = Image.new('RGB', (len(pxs), 1))
    im.putdata(pxs)
    return im

def warm_frac(im, y0f=0.0, y1f=0.30):
    W, H = im.size
    strip = im.crop((0, int(y0f * H), W, int(y1f * H)))
    px = [p for p in strip.getdata() if p[2] > 90]
    warm = [p for p in px if p[0] > p[2] + 12]
    return round(100.0 * len(warm) / max(1, len(px)), 1)

print("=== P1 MEASURE ===")
g6 = Image.open(L + files['ground']).convert('RGB')
g5 = Image.open(L + files['ground5']).convert('RGB')
f6 = Image.open(L + files['flycam']).convert('RGB')
gt6 = Image.open(L + files['gate']).convert('RGB')
gt5 = Image.open(L + files['gate5']).convert('RGB')
d6 = Image.open(L + files['dilac']).convert('RGB')

# --- 2) vàng mặt tiền
wm6, n6 = wall_mask(g6)
wm5, n5 = wall_mask(g5)
tgt = (217, 164, 65)
print(f"[2] WALL v6={wm6} (n={n6}) v5={wm5} target={tgt} "
      f"delta={tuple(round(wm6[i]-tgt[i]) for i in range(3)) if wm6 else None} "
      f"{'DAT' if wm6 and all(abs(wm6[i]-tgt[i]) <= 12 for i in range(3)) else 'CHUA'}")

# --- 1) ám hồng vùng nhân vật (quét toàn ground: pixel hồng bão hòa là magenta render lỗi)
def pink_frac(im):
    W, H = im.size
    cnt = tot = 0
    for p in im.getdata():
        tot += 1
        r, g, b = p
        if r > 120 and b > 100 and g < min(r, b) - 40 and abs(r - b) < 110:
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s > 0.35 and (h > 0.80 or h < 0.06):
                cnt += 1
    return cnt, round(100.0 * cnt / tot, 3)
c6, pf6 = pink_frac(g6)
c5, pf5 = pink_frac(g5)
print(f"[1] PINK ground v6: {c6}px ({pf6}%) | v5: {c5}px ({pf5}%) -> "
      f"{'DAT' if pf6 < pf5 * 0.2 else 'CHUA'}")

# --- 3) trời
for lbl, im in (('flycam', f6), ('ground', g6), ('gate', gt6)):
    sky_tones(im, lbl)
print(f"[3] warm-sky dilac v6: {warm_frac(d6)}% (v5 góc này ám hoàng hôn nặng)")

# --- 4) cổng: bão hòa vùng mặt cổng (trung tâm-trên)
def sat_mean(im, box):
    W, H = im.size
    reg = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    ss = []
    for p in reg.getdata():
        h, s, v = colorsys.rgb_to_hsv(p[0] / 255, p[1] / 255, p[2] / 255)
        ss.append(s)
    return round(sum(ss) / len(ss), 3)
s6 = sat_mean(gt6, (0.30, 0.10, 0.75, 0.55))
s5 = sat_mean(gt5, (0.30, 0.10, 0.75, 0.55))
print(f"[4] GATE face saturation v6={s6} vs v5={s5} -> {'DAT (tăng)' if s6 > s5 else 'CHUA'}")

# --- 5) nền đất ngoài khuôn viên (mặt nạ cỏ V4 trên flycam)
W, H = f6.size
grass = f6.crop((0, int(0.52 * H), W, int(0.95 * H)))
gm = mean(grass)
tgtg = (138, 122, 99)
print(f"[5] GROUND flycam v6={gm} target={tgtg} "
      f"delta={tuple(round(gm[i]-tgtg[i]) for i in range(3))} "
      f"{'DAT' if all(abs(gm[i]-tgtg[i]) <= 12 for i in range(3)) else 'CHUA'}")

# --- 6) hốc vòm ground (so V5: càng tối càng tốt, AO bền)
def arch_lum(im):
    W, H = im.size
    reg = im.crop((int(0.30 * W), int(0.40 * H), int(0.72 * W), int(0.62 * H)))
    px = [p for p in reg.getdata() if p[0] > p[2]]
    return round(sum(0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2] for p in px) / len(px), 1)
print(f"[6] ARCH lum v6={arch_lum(g6)} vs v5={arch_lum(g5)} (AO compositor — v6 <= v5 là có tác dụng)")

print("=== DONE ===")

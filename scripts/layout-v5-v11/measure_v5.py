"""Nghiệm thu P0 bằng số: so render V5 với V4 (cùng camera) + đích bảng B.
Mặt nạ vùng tách từ render V4 bằng ngưỡng màu, áp nguyên sang V5."""
from PIL import Image
import colorsys
from collections import Counter

L = "/home/hatch/workspace/chua-online-work/layout/"
def load(n):
    return Image.open(L + n).convert('RGB')

def stats(img, mask):
    px = img.load()
    rs = gs = bs = n = 0
    tones = Counter()
    for y in range(img.height):
        for x in range(img.width):
            if mask(x, y):
                r, g, b = px[x, y]
                rs += r; gs += g; bs += b; n += 1
                tones[(r // 32, g // 32, b // 32)] += 1
    if n == 0:
        return None
    big = sum(1 for c in tones.values() if c >= 0.02 * n)
    return dict(n=n, mean=(rs // n, gs // n, bs // n), tones2pct=big,
                lum=(0.2126 * rs + 0.7152 * gs + 0.0722 * bs) / n)

v4f, v5f = load('layout_v4_flycam.png'), load('layout_v5_flycam.png')
v4g, v5g = load('layout_v4_ground.png'), load('layout_v5_ground.png')
p4f, p4g = v4f.load(), v4g.load()

def near(c, t, tol):
    return lambda x, y: all(abs(c[x, y][i] - t[i]) <= tol for i in range(3))

water4 = near(p4f, (112, 143, 143), 38)
w4, w5 = stats(v4f, water4), stats(v5f, water4)
print("WATER v4:", w4)
print("WATER v5:", w5)
if w5:
    r, g, b = w5['mean']
    print(f"  -> G-R = {g - r} (tieu chi: <= 20); tones>=2%: {w5['tones2pct']} (tieu chi >= 2)")

grass4 = near(p4f, (137, 149, 116), 30)
g4, g5 = stats(v4f, grass4), stats(v5f, grass4)
print("GROUND(green mask v4) v4:", g4)
print("GROUND v5 at mask:", g5, " target #8A7A63=(138,122,99)")

roof4 = near(p4f, (173, 131, 103), 34)
wall4 = lambda x, y: (p4f[x, y][0] > 175 and 120 < p4f[x, y][1] < 185 and p4f[x, y][2] < 110 and 380 < x < 880 and 230 < y < 470)
r5, wl5 = stats(v5f, roof4), stats(v5f, wall4)
r4, wl4 = stats(v4f, roof4), stats(v4f, wall4)
print("ROOF v4 lum:", None if not r4 else round(r4['lum'], 1), "-> v5:", None if not r5 else (r5['mean'], round(r5['lum'], 1)))
print("WALL v4 lum:", None if not wl4 else round(wl4['lum'], 1), "-> v5:", None if not wl5 else (wl5['mean'], round(wl5['lum'], 1)))
if r5 and wl5:
    print(f"  -> roof/wall luminance ratio v5 = {r5['lum']/wl5['lum']:.2f} (tieu chi <= 0.85)")

def is_teal(rgb):
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    return 0.42 < h < 0.58 and s > 0.15 and v > 0.25
teal_mask = lambda x, y: is_teal(p4g[x, y])
t4 = stats(v4g, teal_mask)
print("TEAL regions in v4 ground:", None if not t4 else t4['n'], "px")
if t4:
    p5 = v5g.load()
    reds = teals = n = 0
    rs = gs = bs = 0
    for y in range(v5g.height):
        for x in range(v5g.width):
            if teal_mask(x, y):
                rgb = p5[x, y]
                h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
                n += 1; rs += rgb[0]; gs += rgb[1]; bs += rgb[2]
                if h < 0.06 or h > 0.94: reds += 1
                if 0.42 < h < 0.58 and s > 0.15: teals += 1
    print(f"  V5 at same mask: mean=({rs//n},{gs//n},{bs//n}) red-hue {100*reds/n:.1f}%  teal-left {100*teals/n:.1f}% (tieu chi: teal ~0%)")

def grille4(x, y):
    r, g, b = p4g[x, y]
    return 300 < y < 590 and r > 165 and g > 115 and b < 115
gr4, gr5 = stats(v4g, grille4), stats(v5g, grille4)
print("ARCH/GRILLE v4 lum:", None if not gr4 else round(gr4['lum'], 1), "-> v5 lum:", None if not gr5 else round(gr5['lum'], 1))
if gr4 and gr5:
    print(f"  -> darkening = {100*(1 - gr5['lum']/gr4['lum']):.1f}% (tieu chi >= 20%)")

p5g = v5g.load()
skytones = Counter()
n = 0
for y in range(42):
    for x in range(v5g.width):
        skytones[p5g[x, y][0] // 24, p5g[x, y][1] // 24, p5g[x, y][2] // 24] += 1
        n += 1
big = [t for t, c in skytones.items() if c >= 0.03 * n]
print(f"SKY v5: tones >=3%: {len(big)} (tieu chi >= 3); top tones:", skytones.most_common(3))

def wallg4(x, y):
    r, g, b = p4g[x, y]
    return 190 < y < 300 and r > 180 and g > 140 and b < 130
wg4, wg5 = stats(v4g, wallg4), stats(v5g, wallg4)
print("FACADE ground v4:", None if not wg4 else wg4['mean'], "-> v5:", None if not wg5 else wg5['mean'], " target albedo #D9A441=(217,164,65)")
print("\n== (7) ART DIRECTION vs ảnh mẫu image-48 (theme chốt 04:42) ==")
import colorsys
sample = Image.open(os.path.expanduser(
    "~/workspace/user/media_library/image/image-48.png")).convert("RGB")
W, H = sample.size
strip = sample.crop((0, int(H*0.045), W, int(H*0.27))).resize((256, 128))
def hsv_stats(img):
    px = list(img.getdata())
    ss, vv = [], []
    for r, g, b in px:
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        ss.append(s); vv.append(v)
    return sum(ss)/len(ss), sum(vv)/len(vv)
s_sat, s_val = hsv_stats(strip)
print(f"ảnh mẫu (vùng cảnh): bão hòa TB={s_sat:.3f} độ sáng TB={s_val:.3f}")
if os.path.exists(G5):
    gv = Image.open(G5).convert("RGB").resize((256, 144))
    v_sat, v_val = hsv_stats(gv)
    print(f"V5 ground:           bão hòa TB={v_sat:.3f} độ sáng TB={v_val:.3f}")
    print(f"  -> chênh bão hòa {v_sat-s_sat:+.3f}, chênh sáng {v_val-s_val:+.3f} "
          f"(đối chiếu hướng, không phải tiêu chí cứng)")

print("MEASURE DONE")

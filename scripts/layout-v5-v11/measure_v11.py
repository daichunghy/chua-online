import sys
from PIL import Image

def stats(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    green = 0; tot = 0
    for y in range(0, h, 3):
        for x in range(0, w, 3):
            r, g, b = px[x, y]
            tot += 1
            if g > r + 10 and g > b + 5 and 40 < g < 180:
                green += 1
    crop = im.crop((int(w * 0.50), int(h * 0.13), int(w * 0.80), int(h * 0.42))).convert("HSV")
    cp = crop.load(); cw, ch = crop.size
    s_sum = 0; n = 0
    for y in range(0, ch, 2):
        for x in range(0, cw, 2):
            s_sum += cp[x, y][1]; n += 1
    return green / tot * 100, s_sum / n

for p in sys.argv[1:]:
    g, s = stats(p)
    print(f"{p}: green%={g:.2f}  roofSat={s:.1f}")

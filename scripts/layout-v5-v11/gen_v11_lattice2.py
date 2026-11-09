"""v11_lattice v2: đậm nét hơn (line #7A5A1E dày 5px, khung kép, medallion đậm)
để dải lattice đọc rõ ở khoảng cách cảnh. Tile 1024x512 = 2 panel 512x512."""
from PIL import Image, ImageDraw

W, H = 1024, 512
CREAM = (243, 233, 210)
DARK = (122, 90, 30)      # bronze đậm
MID = (169, 124, 40)
img = Image.new('RGB', (W, H), CREAM)
d = ImageDraw.Draw(img)

def panel(x0):
    x1 = x0 + 512
    # khung kép
    d.rectangle([x0 + 10, 10, x1 - 10, H - 10], outline=DARK, width=10)
    d.rectangle([x0 + 30, 30, x1 - 30, H - 30], outline=MID, width=4)
    # lưới trám: hai họ đường chéo, clip trong khung nội
    clip = Image.new('L', (W, H), 0)
    cd = ImageDraw.Draw(clip)
    cd.rectangle([x0 + 34, 34, x1 - 34, H - 34], fill=255)
    dia = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dia)
    step = 86
    for k in range(-H, W + H, step):
        dd.line([(x0 + k, 34), (x0 + k + H, H - 34)], fill=DARK + (255,), width=5)
        dd.line([(x0 + k + H, 34), (x0 + k, H - 34)], fill=DARK + (255,), width=5)
    img.paste(Image.alpha_composite(img.convert('RGBA'), dia).convert('RGB'),
              (0, 0), clip)
    d2 = ImageDraw.Draw(img)
    # medallion giữa panel
    cx, cy = x0 + 256, H // 2
    d2.ellipse([cx - 74, cy - 74, cx + 74, cy + 74], outline=DARK, width=9)
    d2.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], outline=MID, width=4)
    d2.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=MID)
    for a in range(0, 360, 45):
        import math
        x = cx + 61 * math.cos(math.radians(a)); y = cy + 61 * math.sin(math.radians(a))
        d2.ellipse([x - 6, y - 6, x + 6, y + 6], fill=DARK)

panel(0)
panel(512)
img.save('/home/hatch/workspace/chua-online-work/textures/v11_lattice.png')
print('saved v2')

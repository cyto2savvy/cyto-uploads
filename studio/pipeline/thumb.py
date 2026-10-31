import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw, ImageFilter
from render import font, F_BLACK, CREAM, GOLD, CORAL, INK, W, H
R.BG = R.make_bg()
f = R.BG.copy()
# goosebump skin close-up, big, tilted, top half
panel, _ = R.draw_skin(lift=1.0, pulse=0.6)
pz = panel.resize((int(panel.width * 1.12), int(panel.height * 1.12)), Image.LANCZOS).rotate(-4, expand=True, resample=Image.BICUBIC)
f.alpha_composite(pz, ((W - pz.width) // 2, 150))
# headline with glitch split
def headline(text, size, fill):
    fnt = font(F_BLACK, size)
    tw = int(fnt.getlength(text)) + 60
    im = Image.new("RGBA", (tw, int(size * 1.3)), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((30, 0), text, font=fnt, fill=fill, stroke_width=14, stroke_fill=INK)
    return im
l1 = headline("GOOSEBUMPS", 168, GOLD)
l2 = headline("ARE A GLITCH?!", 128, CREAM)
for im, y in ((l1, 930), (l2, 1120)):
    if im.width > W - 40:
        k = (W - 40) / im.width; im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    x = (W - im.width) // 2
    if im is not l1:
        a = np.array(im); r = np.zeros_like(a); b = np.zeros_like(a)
        r[..., 0] = 255; r[..., 3] = a[..., 3] // 2; b[..., 2] = 255; b[..., 1] = 220; b[..., 3] = a[..., 3] // 2
        f.alpha_composite(Image.fromarray(r), (x - 10, y)); f.alpha_composite(Image.fromarray(b), (x + 10, y))
    f.alpha_composite(im, (x, y))
# Cyto shocked, bottom
c = R.cyto(560, "open", "open", "shrug", (0, -1), None)
f.alpha_composite(c, ((W - c.width) // 2, 1300))
p = R.pill("THE BODY IS THE 6IX", 34, INK, GOLD)
f.alpha_composite(p, ((W - p.width) // 2, 90))
f.convert("RGB").save("thumbnail-ep1-1080x1920.jpg", quality=92)
f.convert("RGB").resize((360, 640)).save("thumb-small.jpg", quality=88)
print(os.path.getsize("thumbnail-ep1-1080x1920.jpg") // 1024, "KB")

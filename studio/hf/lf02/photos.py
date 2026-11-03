"""LF02 fix pass: real Toronto photo plates (Unsplash, credits in studio/episodes/lf02/photo_credits.md).
- paints out every readable brand / business text (skyline logos, the Distillery 'PURE SPIRITS' sign is cropped away)
- grades each plate toward the HQ purple (15-25% duotone) so the flat cartoon cast sits in front of it
Outputs -> /home/claude/hf/lf02/assets/ph_*.jpg (1920 wide plates + blurred/darkened backdrops)."""
import cv2, numpy as np
from PIL import Image, ImageFilter, ImageEnhance

SRC = "/home/user/cyto-uploads/audio/photo_{}.jpg"
OUT = "/home/claude/hf/lf02/assets/ph_{}.jpg"
PURPLE, MAGENTA, NIGHT = np.array([71, 48, 107]), np.array([192, 75, 138]), np.array([13, 24, 56])


def paint_out(img, boxes, pad=10):
    a = np.array(img); m = np.zeros(a.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes: m[y0 - pad:y1 + pad, x0 - pad:x1 + pad] = 255
    a = cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA)
    bl = cv2.GaussianBlur(a, (0, 0), 6)
    mm = cv2.GaussianBlur(m, (0, 0), 6)[..., None] / 255.0
    return Image.fromarray((a * (1 - mm) + bl * mm).astype(np.uint8))


def grade(img, amt=.2, lo=NIGHT, hi=None, sat=.9, contrast=1.05):
    """duotone toward (lo -> hi) by amt, keeps the photo readable."""
    img = ImageEnhance.Color(img).enhance(sat); img = ImageEnhance.Contrast(img).enhance(contrast)
    a = np.asarray(img).astype(np.float32)
    lum = (a @ np.array([.299, .587, .114]))[..., None] / 255.0
    hi = MAGENTA if hi is None else hi
    duo = lo * (1 - lum) + hi * lum
    return Image.fromarray(np.clip(a * (1 - amt) + duo * amt, 0, 255).astype(np.uint8))


def fit(img, w=1920, h=1080, cx=.5, cy=.5, zoom=1.0):
    W, H = img.size; s = max(w / W, h / H) * zoom
    img = img.resize((int(W * s + .5), int(H * s + .5)), Image.LANCZOS)
    x = int((img.width - w) * cx); y = int((img.height - h) * cy)
    return img.crop((x, y, x + w, y + h))


def save(img, name, q=88): img.convert("RGB").save(OUT.format(name), quality=q); print("wrote", OUT.format(name), img.size)


# skyline: Scotiabank 'S', 2x BMO, TRUMP, Deloitte, two small lit signs -> painted out
sky = Image.open(SRC.format("skyline_dusk")).convert("RGB")
sky = paint_out(sky, [(966, 374, 994, 414), (1178, 360, 1230, 390), (1306, 358, 1360, 390), (1134, 500, 1190, 524),
                      (960, 678, 1016, 702), (1298, 588, 1342, 618), (734, 508, 760, 534)])
plate = grade(fit(sky, 2112, 1188, .55, .5), .18, NIGHT, MAGENTA)          # 10% oversize for the Ken Burns push
save(plate.filter(ImageFilter.GaussianBlur(1.2)), "skyline")
bg = ImageEnhance.Brightness(grade(fit(sky, 2112, 1188, .6, .55), .3, NIGHT, MAGENTA)).enhance(.62).filter(ImageFilter.GaussianBlur(8))
save(bg, "skyline_bg")
save(ImageEnhance.Brightness(grade(fit(sky, 2112, 1188, .2, .8, 1.25), .22)).enhance(.85).filter(ImageFilter.GaussianBlur(2)), "skyline_block")

# Queen's Park (landmark; its own building signage is part of the landmark) - cool, slightly dusky grade
qp = Image.open(SRC.format("queens_park")).convert("RGB")
save(ImageEnhance.Brightness(grade(fit(qp, 2112, 1188, .5, .62), .3, NIGHT, np.array([255, 205, 170]), sat=.75)).enhance(.82).filter(ImageFilter.GaussianBlur(1.0)), "queens_park")

# Nathan Phillips Square: keep WIDE (distant skaters stay tiny), soft blur so no face is in focus
npq = Image.open(SRC.format("nathan_phillips")).convert("RGB")
save(ImageEnhance.Brightness(grade(fit(npq, 2112, 1188, .5, .45), .25, NIGHT, np.array([210, 225, 255]))).enhance(.88).filter(ImageFilter.GaussianBlur(2.2)), "nathan_phillips")

# Distillery: crop to the RIGHT half (arched windows + barrels) -> no 'PURE SPIRITS' sign, no person
ds = Image.open(SRC.format("distillery_bw")).convert("RGB")
ds = ds.crop((1290, 0, 2400, ds.height))
save(ImageEnhance.Contrast(fit(ds, 2112, 1188, .5, .35)).enhance(1.25).filter(ImageFilter.GaussianBlur(1.5)), "distillery_noir")
warm = grade(fit(ds, 2112, 1188, .5, .35), .45, np.array([40, 20, 30]), np.array([255, 196, 120]), sat=1.0)
save(warm.filter(ImageFilter.GaussianBlur(1.8)), "distillery_warm")

import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
from render import font, F_BLACK, GOLD, CREAM, INK, W, H
ORANGE = (255, 140, 40)
JOBS = [("ep2", "/home/claude/ep2/cyto-ep2-scared-to-death.mp4", 23.3, ["SCARED", "TO DEATH?!"]),
        ("ep3", "/home/claude/ep3/cyto-ep3-sugar-rush.mp4", 22.9, ["SUGAR RUSH", "IS FAKE"]),
        ("ep4", "/home/claude/ep4/cyto-ep4-clocks-fall-back.mp4", 15.6, ["CLOCKS FALL", "BACK SUNDAY"]),
        ("ep5", "/home/claude/ep5/cyto-ep5-cold-season.mp4", 19.6, ["WHY COLD", "= SICK"]),
        ("ep6", "/home/claude/ep6/cyto-ep6-procrastination.mp4", 21.4, ["NOT LAZY,", "JUST HUMAN"])]
for name, vid, t, lines in JOBS:
    tmp = f"/home/claude/thumbs/_{name}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", vid, "-frames:v", "1", tmp], check=True)
    im = Image.open(tmp).convert("RGBA")
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.rectangle((0, 960, W, 1250), fill=(9, 18, 32, 245))      # cover the caption with the headline
    im.alpha_composite(band)
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        size = 150
        f = font(F_BLACK, size)
        while f.getlength(ln) > W - 70: size -= 6; f = font(F_BLACK, size)
        col = GOLD if i == 0 else CREAM
        y = 1030 + i * 130
        tw = f.getlength(ln)
        # glitch split on line 2
        if i == 1:
            for dx, c in ((-8, (255, 60, 80, 170)), (8, (60, 220, 255, 170))):
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text(((W - tw) / 2 + dx, y), ln, font=f, fill=c, anchor="lm")
                im.alpha_composite(lay)
            d = ImageDraw.Draw(im)
        d.text(((W - tw) / 2, y), ln, font=f, fill=col, stroke_width=12, stroke_fill=INK, anchor="lm")
    im.convert("RGB").save(f"/home/claude/thumbs/thumb-{name}.jpg", quality=92)
    os.remove(tmp)
sheet = Image.new("RGB", (W * 5 // 4, H // 4))
for i, (name, *_ ) in enumerate(JOBS):
    sheet.paste(Image.open(f"/home/claude/thumbs/thumb-{name}.jpg").resize((W // 4, H // 4)), (i * W // 4, 0))
sheet.save("/home/claude/thumbs/sheet.jpg", quality=88)
print("ok")

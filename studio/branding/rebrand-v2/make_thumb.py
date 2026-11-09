#!/usr/bin/env python3
"""MrBeast-style Cyto thumbnail (1280x720). Usage:
  python3 make_thumb.py out.png --lines "CAN YOU|DIE FROM|FEAR?" --colors "w,w,y" --expr shock --bg "#ff3b30,#7a0fff" [--side right] [--fit none] [--arrow] [--object path.png]
Rules (THUMBNAIL_FORMAT_V2.md): <=3 words/line, <=4 words total, ONE huge face, saturated 2-colour background with light burst,
thick white sticker outline + hard shadow, headline with black stroke, one focal object or arrow, reads at 160px wide."""
import argparse, os, subprocess, tempfile, math, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); W,H=1280,720
COL={"w":(255,255,255),"y":(255,214,10),"r":(255,59,48),"g":(52,255,120),"c":(0,229,255)}
def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def cyto_png(expr,fit):
    d=tempfile.mkdtemp(); env=dict(os.environ,SEED="3",EXPR=expr)
    subprocess.run(["node",os.path.join(HERE,"cyto2d.js")],cwd=d,env=env,check=True,capture_output=True)
    f=os.path.join(d,f"cyto_{fit}{'' if expr=='chill' else '_'+expr}.svg")
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={"width":1100,"height":1100}); pg.goto("file://"+f)
        im=Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert("RGBA"); b.close()
    return im.crop(im.getbbox())
def main():
    a=argparse.ArgumentParser(); a.add_argument("out"); a.add_argument("--lines",required=True); a.add_argument("--colors",default="w,w,y")
    a.add_argument("--expr",default="shock"); a.add_argument("--bg",default="#ff3b30,#6a00ff"); a.add_argument("--side",default="right")
    a.add_argument("--fit",default="none"); a.add_argument("--arrow",action="store_true"); a.add_argument("--object"); a=a.parse_args()
    c1,c2=[hexc(x) for x in a.bg.split(",")]
    bg=Image.new("RGB",(W,H)); px=bg.load()
    for y in range(H):
        for x in range(0,W):
            t=(x/W*0.6+y/H*0.4); px[x,y]=tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))
    # light burst behind face
    fx=W*0.70 if a.side=="right" else W*0.30
    burst=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(burst)
    for k in range(24):
        a0=k*math.pi/12; a1=a0+math.pi/24; R=1400
        bd.polygon([(fx,H*0.5),(fx+R*math.cos(a0),H*0.5+R*math.sin(a0)),(fx+R*math.cos(a1),H*0.5+R*math.sin(a1))],fill=(255,255,255,38))
    bg=Image.alpha_composite(bg.convert("RGBA"),burst)
    glow=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(glow).ellipse([fx-420,H*0.5-420,fx+420,H*0.5+420],fill=(255,255,255,90)); glow=glow.filter(ImageFilter.GaussianBlur(110)); bg=Image.alpha_composite(bg,glow)
    cy=cyto_png(a.expr,a.fit); h=int(H*1.02); cy=cy.resize((int(h*cy.width/cy.height),h),Image.LANCZOS)
    cx=int(fx-cy.width/2); cyy=int(H-h+30)
    al=cy.split()[3]; st=al.filter(ImageFilter.MaxFilter(31)); st=st.filter(ImageFilter.GaussianBlur(1.2))
    sh=Image.new("RGBA",bg.size,(0,0,0,0)); sh.paste((0,0,0,170),(cx+14,cyy+18),st); sh=sh.filter(ImageFilter.GaussianBlur(10)); bg=Image.alpha_composite(bg,sh)
    wh=Image.new("RGBA",cy.size,(255,255,255,255)); bg.paste(wh,(cx,cyy),st); bg.alpha_composite(cy,(cx,cyy))
    # headline
    lines=a.lines.split("|"); cols=a.colors.split(",")
    d=ImageDraw.Draw(bg); fp="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    size=190
    while True:
        F=ImageFont.truetype(fp,size); wmax=max(d.textlength(l,font=F) for l in lines)
        if wmax<=W*0.44 or size<60: break
        size-=6
    lh=int(size*1.02); y0=int(H/2-lh*len(lines)/2+lh/2)-10; tx=(W*0.235 if a.side=="right" else W*0.765)
    for i,l in enumerate(lines):
        col=COL.get(cols[min(i,len(cols)-1)],(255,255,255)); y=y0+i*lh
        for dx,dy in [(-9,-9),(9,-9),(-9,9),(9,9),(0,-11),(0,11),(-11,0),(11,0),(0,17)]: d.text((tx+dx,y+dy),l,font=F,fill=(0,0,0),anchor="mm")
        d.text((tx,y),l,font=F,fill=col,anchor="mm")
    if a.object:
        o=Image.open(a.object).convert("RGBA"); o.thumbnail((300,300)); bg.alpha_composite(o,(int(tx-o.width/2),H-o.height-20))
    if a.arrow:
        ax=int(fx-cy.width*0.45) if a.side=="right" else int(fx+cy.width*0.45)
        d.polygon([(ax-40,H*0.78),(ax-120,H*0.70),(ax-120,H*0.74),(ax-200,H*0.74),(ax-200,H*0.82),(ax-120,H*0.82),(ax-120,H*0.86)],fill=(255,59,48),outline=(255,255,255))
    bg.convert("RGB").save(a.out); print("saved",a.out)
main()

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
    a.add_argument("--fit",default="none"); a.add_argument("--arrow",action="store_true"); a.add_argument("--object"); a.add_argument("--scene",default=""); a.add_argument("--bg2",help="2nd photo -> split-screen (left=bg-image, right=bg2)"); a.add_argument("--labels",default="",help="split corner labels L|R, e.g. \"57C|-71C\""); a.add_argument("--badge",default="",help="top-right big badge e.g. DAY 115"); a.add_argument("--blur",type=float,default=1.5); a.add_argument("--bg-image",dest="bgimg"); a=a.parse_args()
    c1,c2=[hexc(x) for x in a.bg.split(",")]
    bg=Image.new("RGB",(W,H)); px=bg.load()
    for y in range(H):
        for x in range(0,W):
            t=(x/W*0.6+y/H*0.4); px[x,y]=tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))
    bg=bg.convert('RGBA')

    # TOPIC BACKGROUND: --scene (ecg|snow|clock|toronto|stars) or --bg-image photo (cover-cropped, saturated, tinted)
    def load_cover(path,box_w):
        from PIL import ImageEnhance
        ph=Image.open(path).convert("RGB"); r=max(box_w/ph.width,H/ph.height); ph=ph.resize((int(ph.width*r)+1,int(ph.height*r)+1))
        ph=ph.crop(((ph.width-box_w)//2,(ph.height-H)//2,(ph.width-box_w)//2+box_w,(ph.height-H)//2+H))
        ph=ph.filter(ImageFilter.GaussianBlur(a.blur)); ph=ImageEnhance.Color(ph).enhance(1.55); ph=ImageEnhance.Contrast(ph).enhance(1.2); return ph.convert("RGBA")
    if a.bgimg and a.bg2:
        bg=Image.new("RGBA",(W,H)); bg.paste(load_cover(a.bgimg,W//2),(0,0)); bg.paste(load_cover(a.bg2,W-W//2),(W//2,0))
        ImageDraw.Draw(bg).polygon([(W//2-10,0),(W//2+10,0),(W//2+4,H//2),(W//2+12,H),(W//2-12,H),(W//2-4,H//2)],fill=(255,255,255,255))
    elif a.bgimg:
        ph=load_cover(a.bgimg,W); bg=Image.blend(ph,Image.new("RGBA",(W,H),c1+(255,)),0.22)
    sd=ImageDraw.Draw(bg)
    if a.scene=="ecg":
        pts=[];x=0
        while x<W:
            if x<W*0.55: pts+= [(x,H*0.5),(x+40,H*0.5),(x+55,H*0.38),(x+75,H*0.74),(x+95,H*0.22),(x+115,H*0.5),(x+170,H*0.5)]; x+=210
            else: pts+=[(x,H*0.5)]; x+=W  # flatline
        pts.append((W,H*0.5))
        for wd,al in ((34,70),(16,255)): 
            lay=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(lay).line(pts,fill=(80,255,160,al),width=wd,joint="curve"); bg=Image.alpha_composite(bg,lay.filter(ImageFilter.GaussianBlur(6 if wd>20 else 0)))
    elif a.scene=="snow":
        import random; rr=random.Random(5)
        for _ in range(160): x,y,r_=rr.random()*W,rr.random()*H,rr.choice([3,4,6,9]); sd.ellipse([x-r_,y-r_,x+r_,y+r_],fill=(255,255,255,rr.choice([150,210,255])))
    elif a.scene=="stars":
        import random; rr=random.Random(7)
        for _ in range(120): x,y,r_=rr.random()*W,rr.random()*H,rr.choice([2,3,5]); sd.ellipse([x-r_,y-r_,x+r_,y+r_],fill=(255,255,255,230))
    elif a.scene=="clock":
        cx0,cy0,R=W*0.28,H*0.52,300
        sd.ellipse([cx0-R,cy0-R,cx0+R,cy0+R],outline=(255,255,255,200),width=22,fill=(255,255,255,40))
        for k in range(12): ang=k*math.pi/6; sd.line([(cx0+(R-30)*math.sin(ang),cy0-(R-30)*math.cos(ang)),(cx0+(R-70)*math.sin(ang),cy0-(R-70)*math.cos(ang))],fill=(255,255,255,230),width=14)
        sd.line([(cx0,cy0),(cx0+150*math.sin(2.6),cy0-150*math.cos(2.6))],fill=(255,255,255,255),width=22); sd.line([(cx0,cy0),(cx0+220*math.sin(0.4),cy0-220*math.cos(0.4))],fill=(255,214,10,255),width=16)
    elif a.scene=="toronto":
        import random; rr=random.Random(11); x=0
        x=0
        while x<W:
            bw=rr.randint(50,110); bh=rr.randint(140,380); sd.rectangle([x,H-bh,x+bw,H],fill=(8,14,40,255))
            for wy in range(H-bh+14,H-10,26):
                for wx in range(x+8,x+bw-10,20):
                    if rr.random()<0.45: sd.rectangle([wx,wy,wx+8,wy+12],fill=(255,214,120,230))
            x+=bw+rr.randint(0,10)
        tx0=W*0.45; sd.rectangle([tx0-9,H*0.18,tx0+9,H],fill=(8,14,40,255)); sd.ellipse([tx0-38,H*0.40,tx0+38,H*0.46],fill=(8,14,40,255)); sd.polygon([(tx0-3,H*0.06),(tx0+3,H*0.06),(tx0+9,H*0.2),(tx0-9,H*0.2)],fill=(8,14,40,255))
    # light burst behind face
    fx=W*0.50 if a.bg2 else (W*0.70 if a.side=="right" else W*0.30)
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
    lines=[l for l in a.lines.split("|") if l]; cols=a.colors.split(",")
    d=ImageDraw.Draw(bg); fp="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    size=190
    while lines:
        F=ImageFont.truetype(fp,size); wmax=max(d.textlength(l,font=F) for l in lines)
        if wmax<=W*0.44 or size<60: break
        size-=6
    lh=int(size*1.02); y0=int(H/2-lh*len(lines)/2+lh/2)-10; tx=(W*0.235 if a.side=="right" else W*0.765)
    def big(txt,xy,sz,col,anchor):
        FB=ImageFont.truetype(fp,sz)
        for dx,dy in [(-8,-8),(8,-8),(-8,8),(8,8),(0,-10),(0,10),(-10,0),(10,0),(0,14)]: d.text((xy[0]+dx,xy[1]+dy),txt,font=FB,fill=(0,0,0),anchor=anchor)
        d.text(xy,txt,font=FB,fill=col,anchor=anchor)
    if a.labels:
        L,R=a.labels.split("|"); big(L,(30,30),120,(255,255,255),"la"); big(R,(W-30,30),120,(255,255,255),"ra")
    if a.badge: big(a.badge,(W-30,30),130,(255,255,255),"ra")
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

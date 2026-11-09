#!/usr/bin/env python3
"""Rebuild every canon PNG (profile, covers, banner, outfit sheet, transparent assets, watermark). Run after ANY change to cyto2d.js."""
import os, subprocess, tempfile, io
from playwright.sync_api import sync_playwright
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); d=tempfile.mkdtemp()
subprocess.run(["node",os.path.join(H,"cyto2d.js")],cwd=d,env=dict(os.environ,SEED="3"),check=True,capture_output=True)
job={"pfp.svg":("cyto-profile-picture-1000.png",1000,1000),"cover.svg":("cyto-facebook-cover-1640x624.png",1640,624),
     "banner.svg":("cyto-youtube-banner-2560x1440.png",2560,1440),"fits.svg":("cyto-outfit-options.png",2400,1100)}
with sync_playwright() as p:
    b=p.chromium.launch()
    for f,(out,w,h) in job.items():
        pg=b.new_page(viewport={"width":w,"height":h}); pg.goto("file://"+os.path.join(d,f)); pg.screenshot(path=os.path.join(H,out)); pg.close()
    pg=b.new_page(viewport={"width":1100,"height":1100}); A=os.path.join(H,"assets"); os.makedirs(A,exist_ok=True)
    for fit in ("none","jersey","hoodie","puffer"):
        pg.goto(f"file://{d}/cyto_{fit}.svg"); im=Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert("RGBA"); im=im.crop(im.getbbox()); im.save(f"{A}/cyto-{fit}-transparent.png")
        if fit=="none":
            w=im.copy(); w.thumbnail((150,150),Image.LANCZOS); c=Image.new("RGBA",(150,150),(0,0,0,0)); c.paste(w,((150-w.width)//2,(150-w.height)//2),w); c.save(f"{A}/video-watermark-150-canon.png")
    b.close()
print("canon PNGs rebuilt")

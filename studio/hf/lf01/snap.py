"""snap.py chK t1,t2,... [--sheet out.jpg --fps 1 --w 384]  -> frames (png) or a 1 fps contact sheet. Toggles .clip visibility by data-start/duration."""
import sys, os, threading, http.server, socketserver, argparse
from playwright.sync_api import sync_playwright
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument("ch"); ap.add_argument("times", nargs="?", default="")
ap.add_argument("--sheet"); ap.add_argument("--fps", type=float, default=1.0); ap.add_argument("--w", type=int, default=384); ap.add_argument("--out", default="/home/claude/lf01/snaps")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", 0), lambda *x, **k: Q(*x, directory="/home/claude/hf/lf01", **k)); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = """(t)=>{ const tl=window.__timelines.main; tl.seek(t,false);
 document.querySelectorAll('.clip').forEach(e=>{ if(e.id==='root')return; const s=+e.dataset.start, d=+e.dataset.duration; e.style.visibility=(t>=s-1e-3 && t<s+d-1e-3)?'':'hidden'; });
 return 1; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"http://127.0.0.1:{port}/{a.ch}/index.html"); pg.wait_for_timeout(1500)
    T = pg.evaluate("()=>+document.getElementById('root').dataset.duration")
    ts = [float(x) for x in a.times.split(",") if x] if a.times else [round(0.5 / a.fps + i / a.fps, 2) for i in range(int(T * a.fps))]
    ims = []
    for t in ts:
        pg.evaluate(JS, t); f = f"{a.out}/{a.ch}_{t:07.2f}.png"; pg.screenshot(path=f)
        if a.sheet: ims.append(Image.open(f).resize((a.w, a.w * 9 // 16))); os.remove(f)
        else: print(f)
    if a.sheet:
        cols = 6; rows = (len(ims) + cols - 1) // cols; S = Image.new("RGB", (cols * a.w, rows * a.w * 9 // 16), "white")
        for i, im in enumerate(ims): S.paste(im, ((i % cols) * a.w, (i // cols) * a.w * 9 // 16))
        S.save(a.sheet, quality=80); print(a.sheet, len(ims), "frames")
    if errs: print("PAGE ERRORS:", errs[:3])
    b.close()

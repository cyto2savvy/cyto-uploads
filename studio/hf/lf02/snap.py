"""Fast preview frames (Playwright seek, clip visibility emulated like HyperFrames).
python3 snap.py SCENE t1,t2,... out_dir [--scale 0.5]   or   python3 snap.py SCENE sheet out.jpg [--fps 1]"""
import sys, os, threading, http.server, socketserver, math
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

scene, what, out = sys.argv[1], sys.argv[2], sys.argv[3]
fps = float(sys.argv[sys.argv.index("--fps") + 1]) if "--fps" in sys.argv else 1.0
ROOT = "/home/claude/hf/lf02"
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", 0), lambda *x, **k: Q(*x, directory=ROOT, **k))
threading.Thread(target=srv.serve_forever, daemon=True).start()
SEEK = """(t)=>{ document.querySelectorAll('[data-start]').forEach(e=>{ if(e.id==='root')return; const s=+e.dataset.start,d=+e.dataset.duration;
  e.style.visibility=(t>=s-1e-3&&t<s+d-1e-3)?'':'hidden'; }); void window.__timelines.main.seek(t,false); }"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/{scene}/index.html"); pg.wait_for_timeout(1500)
    if errs: print("PAGE ERRORS:", errs[:3]); sys.exit(1)
    T = pg.evaluate("()=>+document.getElementById('root').dataset.duration")
    times = [round(i / fps + .5 / fps, 2) for i in range(int(T * fps))] if what == "sheet" else [float(x) for x in what.split(",")]
    shots = []
    for t in times:
        pg.evaluate(SEEK, t); pg.wait_for_timeout(60)
        if os.environ.get("DBG"): print(t, pg.evaluate("(ss)=>ss.map(s=>{const e=document.querySelector(s);return s+'='+(e?getComputedStyle(e).transform:'-')})", os.environ["DBG"].split(",")))
        f = f"/home/claude/lf02/snaps/snap_{scene}_{t:.2f}.png"; pg.screenshot(path=f); shots.append((t, f))
    b.close()
if errs: print("PAGE ERRORS:", errs[:3])
if what == "sheet":
    cols = 6; tw, th = 320, 180; rows = math.ceil(len(shots) / cols)
    sh = Image.new("RGB", (cols * tw, rows * th), "black"); d = ImageDraw.Draw(sh)
    for i, (t, f) in enumerate(shots):
        im = Image.open(f).convert("RGB").resize((tw, th)); sh.paste(im, ((i % cols) * tw, (i // cols) * th))
        d.text(((i % cols) * tw + 4, (i // cols) * th + 2), f"{t:.1f}", fill="yellow")
    sh.save(out, quality=80); print("sheet", out, len(shots))
else:
    os.makedirs(out, exist_ok=True)
    for t, f in shots:
        Image.open(f).convert("RGB").save(f"{out}/{scene}_{t:05.2f}.jpg", quality=85)
    print("saved", len(shots), "to", out)

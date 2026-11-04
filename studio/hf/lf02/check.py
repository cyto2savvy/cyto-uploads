"""LF02 v3 programmatic frame checks on the BUILT scenes (Playwright seek, every 2nd frame):
 d) Neutro mouth bbox vs collar (>= 6 px above) and vs any visible prop (pad/pen/ticket/desk)  -> overlap frames
 e) pupils inside the eye mask: pupil centre offset <= 25 % of the eye width, both pupils same direction
 f) closed mouth when not speaking (visible mouth shape vs the character's word times)
python3 check.py s01 s02 ...  -> /home/claude/lf02/checks/<scene>.json + summary line"""
import sys, json, os, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
sys.path.insert(0, "/home/claude/hf/lf02")
ROOT = "/home/claude/hf/lf02"; OUT = "/home/claude/lf02/checks"; os.makedirs(OUT, exist_ok=True)
TM = json.load(open("/home/claude/lf02/timing.json"))
CLOSED_CH = {"rest", "smirk", "frown", "flat", "mbp"}; CLOSED_CY = {"rest", "mbp"}
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", 0), lambda *x, **k: Q(*x, directory=ROOT, **k))
threading.Thread(target=srv.serve_forever, daemon=True).start()
SEEK = """(t)=>{ document.querySelectorAll('[data-start]').forEach(e=>{ if(e.id==='root')return; const s=+e.dataset.start,d=+e.dataset.duration;
  e.style.visibility=(t>=s-1e-3&&t<s+d-1e-3)?'':'hidden'; }); void window.__timelines.main.seek(t,false); }"""
MEASURE = """()=>{
 const vis=e=>{ if(!e) return false; let x=e; while(x&&x.nodeType===1){ const cs=getComputedStyle(x); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0) return false; if(x.getAttribute&&x.getAttribute('opacity')==='0') return false; x=x.parentNode;} return true; };
 const bb=e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom];};
 const out={chars:[]};
 const who=[['cy','CYTO','#v_',['rest','mbp','small','a','e','o','u','fv'],'cyeye','#pup'],['nt','NEUTRO','#ntm_',['rest','smirk','grin','frown','flat','small','a','e','o','mbp'],'nteye','#ntpup'],
            ['mt','MITO','#mtm_',['rest','smirk','grin','frown','flat','small','a','e','o','mbp'],'mteye','#mtpup']];
 for(const [p,name,mp,shapes,eye,pup] of who){
   const eL=document.getElementById(eye+'L'); if(!eL) continue;
   if(!vis(eL)) { out.chars.push({who:name,visible:false}); continue; }
   const c={who:name,visible:true,shape:null,eyes:[]};
   for(const s of shapes){ const g=document.querySelector(mp+s); if(g&&g.getAttribute('opacity')!=='0'&&+getComputedStyle(g).opacity>0){ c.shape=s; c.mouth=bb(g); } }
   for(const k of ['L','R']){ const E=document.getElementById(eye+k), P=document.querySelector(pup+k+' ellipse'); if(E&&P){ const a=bb(E),b=bb(P); c.eyes.push([(a[0]+a[2])/2,(a[1]+a[3])/2,a[2]-a[0],(b[0]+b[2])/2,(b[1]+b[3])/2,a[3]-a[1]]); } }
   if(p==='nt'){ const props=[]; for(const id of ['ntcollar','ntcollar2']){ const e=document.getElementById(id); if(e&&vis(e)) c[id]=bb(e); }
     for(const id of ['ntpad','ntpen','nttkt']){ const e=document.getElementById(id); if(e&&vis(e)) props.push([id,bb(e)]); } const dk=document.querySelector('#dk svg path'); if(dk&&vis(dk)) props.push(['desk',bb(dk)]); c.props=props; }
   out.chars.push(c);
 }
 return out; }"""


def speaking(who, t, pad=.06):
    for l in TM["lines"]:
        if l["who"] == who:
            for w in l["words"]:
                if w["t0"] - pad <= t <= w["t1"] + pad: return True
    return False


def check(pg, name):
    meta = json.load(open(f"{ROOT}/{name}/meta.json")); t0, t1 = meta["t0"], meta["t1"]
    pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/{name}/index.html"); pg.wait_for_timeout(1200)
    n = int(round((t1 - t0) * 30)); R = dict(scene=name, frames=0, mouth_collar=[], mouth_prop=[], pupil_out=[], pupil_split=[], open_silent=[], eye_frames=0)
    for f in range(0, n, 2):
        t = f / 30; pg.evaluate(SEEK, t); m = pg.evaluate(MEASURE); R["frames"] += 1
        for c in m["chars"]:
            if not c.get("visible"): continue
            if c["who"] == "NEUTRO" and c.get("mouth"):
                mb = c["mouth"]; sc = 1
                for cid in ("ntcollar", "ntcollar2"):
                    if cid in c and mb[3] > c[cid][1] - 6 * 0.6 and mb[0] < c[cid][2] and mb[2] > c[cid][0]: R["mouth_collar"].append((round(t, 2), cid))
                for pid, pb in c.get("props", []):
                    if mb[0] < pb[2] and mb[2] > pb[0] and mb[1] < pb[3] and mb[3] > pb[1]: R["mouth_prop"].append((round(t, 2), pid))
            if len(c["eyes"]) == 2 and min(e[2] / max(1, e[5]) for e in c["eyes"]) < .45:
                R.setdefault("edge_on_skipped", 0); R["edge_on_skipped"] += 1          # spin gag: eye seen edge-on
            elif len(c["eyes"]) == 2:
                R["eye_frames"] += 1; ds = []
                for ex, ey, ew, px, py, eh in c["eyes"]:
                    dx, dy = px - ex, py - ey; ds.append(dx)
                    if abs(dx) > .25 * ew + .6 or abs(dy) > .25 * eh + .6: R["pupil_out"].append((round(t, 2), c["who"], round(dx / ew, 3), round(dy / ew, 3)))
                if abs(ds[0] - ds[1]) > .06 * c["eyes"][0][2] + .6: R["pupil_split"].append((round(t, 2), c["who"], round(ds[0], 1), round(ds[1], 1)))
            if c.get("shape"):
                closed = CLOSED_CY if c["who"] == "CYTO" else CLOSED_CH
                if c["shape"] not in closed and not speaking(c["who"], t0 + t): R["open_silent"].append((round(t, 2), c["who"], c["shape"]))
    json.dump(R, open(f"{OUT}/{name}.json", "w"))
    print(name, "frames", R["frames"], "eye-frames", R["eye_frames"], "| mouth/collar", len(R["mouth_collar"]), "mouth/prop", len(R["mouth_prop"]),
          "| pupil out", len(R["pupil_out"]), "split", len(R["pupil_split"]), "| open-while-silent", len(R["open_silent"]), R["open_silent"][:3], R["pupil_out"][:2])


with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    for nm in sys.argv[1:]: check(pg, nm)
    b.close()

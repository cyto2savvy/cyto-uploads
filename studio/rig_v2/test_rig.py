#!/usr/bin/env python3
"""Rig v2 tests: python3 -I studio/rig_v2/test_rig.py   (needs node+playwright, numpy, pillow)
Locks in Utsha's Nov 9 feedback: cup ALWAYS held (never set down) with steam; hand on cup; Cyto's face MOVES (gaze wander, blinks,
reactions, per-syllable mouth) instead of staring one way."""
import os, sys, json, subprocess, tempfile, shutil
import numpy as np
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__)); R=[]
def check(n,ok,d=""): R.append(ok); print(("PASS " if ok else "FAIL ")+n+(f"  [{d}]" if d else ""))
def node(js): return subprocess.run(["node","-e",js],cwd=HERE,capture_output=True,text=True,check=True).stdout
tl={"fps":10,"duration":60,"fit":"none","seed":7,
 "words":[{"w":"a","start":10.0,"end":10.6},{"w":"b","start":20.0,"end":20.5}],
 "beats":[{"t":0,"emotion":"chill"},{"t":30,"emotion":"shock","gaze":[0,0]},{"t":40,"emotion":"think"},{"t":50,"emotion":"happy"}]}
js="const r=require('./cyto_rig.js');const tl="+json.dumps(tl)+";const o=[];for(let t=0;t<60;t+=0.05)o.push([t,r.state(t,tl)]);console.log(JSON.stringify(o))"
S=json.loads(node(js)); T=np.array([a for a,_ in S]); st=[b for _,b in S]
col=lambda k: np.array([ (s[k] if s[k] is not None else 0) for s in st],dtype=float)
# --- behaviour (pure state) ---
check("cup is held, never placed down (cup offset stays within +-6px, rotation +-3deg over 60 s)", abs(col("cupDy")).max()<=6 and abs(col("cupRot")).max()<=3, f"dy {abs(col('cupDy')).max():.1f} rot {abs(col('cupRot')).max():.1f}")
check("cup moves a little (sways)", col("cupDy").std()>1.5 and col("cupRot").std()>.8)
bl=col("blink")>.5; starts=T[1:][bl[1:]&~bl[:-1]]; gaps=np.diff(starts)
check("blinks every 2-4 s", len(starts)>=12 and gaps.min()>=1.8 and gaps.max()<=4.4, f"{len(starts)} blinks, gaps {gaps.min():.1f}-{gaps.max():.1f}s")
g=np.round(col("gx"),2)+1j*np.round(col("gy"),2); changes=(np.diff(g)!=0).sum()
check("gaze wanders (not staring one way)", len(set(np.round(col('gx'),1)))>=6 and abs(col('gx')).max()>.5, f"{len(set(np.round(col('gx'),1)))} distinct x gazes")
check("looks back at camera regularly", ((abs(col('gx'))<.1)&(abs(col('gy'))<.1)).mean()>.2)
words=[(10,10.6),(20,20.5)]; talk=np.array([any(a<=t<=b for a,b in words) for t in T]); m=np.array([s["mouth"] is not None for s in st])
check("mouth moves only while words play (per-syllable)", (m[talk&(T<30)].mean()>.95) and (m[~talk&(T<30)].mean()<.05))
shapes={s["mouth"] for s,tt in zip(st,talk) if tt}; check("mouth cycles several shapes", len(shapes)>=3, str(shapes))
sh=[s for s,t in zip(st,T) if 30.3<t<30.5][0]; check("shock beat: face changes + brows pop + gaze to camera", sh["expr"]=="shock" and sh["brow"]>.9 and sh["gx"]==0)
check("reaction faces vary across the video (chill/shock/think/happy)", len({s['expr'] for s in st})>=2 and len({round(s['tilt']) for s in st})>=6)
# --- rendered pixels ---
tmp=tempfile.mkdtemp(prefix="rig_"); tl2={"fps":5,"duration":3,"fit":"none","seed":7,"words":[{"w":"x","start":0.4,"end":1.4}],"beats":[{"t":0,"emotion":"chill"},{"t":2,"emotion":"shock"}]}
json.dump(tl2,open(tmp+"/tl.json","w"))
try:
    r=subprocess.run(["node",os.path.join(HERE,"render_rig.js"),tmp+"/tl.json",tmp+"/o","360"],env=dict(os.environ,SEED="3"),capture_output=True,text=True)
    fr=[np.asarray(Image.open(f"{tmp}/o/f{i:05d}.png").convert("RGBA")).astype(int) for i in range(15)]
    check("frames render with transparency", fr[0][...,3].min()==0 and (fr[0][...,3]>0).mean()>.2)
    px=lambda x,y:(int((x+550)*360/1100),int((y+550)*360/1100))
    def reg(f,x0,y0,x1,y1): a,b=px(x0,y0),px(x1,y1); return f[b[1]:b[1]+1 and a[1]:b[1], a[0]:b[0]]
    eye=lambda f: f[px(0,-120)[1]:px(0,40)[1], px(-220,0)[0]:px(220,0)[0]]
    mouth=lambda f: f[px(0,70)[1]:px(0,200)[1], px(-90,0)[0]:px(110,0)[0]]
    steam=lambda f: f[px(0,-250)[1]:px(0,-110)[1], px(-420,0)[0]:px(-300,0)[0]]
    d=lambda a,b: np.abs(a-b).sum()/max(1,a.size)
    check("face moves between frames (eyes change)", max(d(eye(fr[i]),eye(fr[0])) for i in range(1,15))>1.0, f"{max(d(eye(fr[i]),eye(fr[0])) for i in range(1,15)):.2f}")
    check("mouth shape changes while talking", max(d(mouth(fr[i]),mouth(fr[0])) for i in range(2,7))>2.0)
    check("shock reaction visibly changes the face", d(eye(fr[12]),eye(fr[0]))>3.0)
    check("steam rises/animates above the cup", max(d(steam(fr[i]),steam(fr[0])) for i in range(1,15))>.8, f"{max(d(steam(fr[i]),steam(fr[0])) for i in range(1,15)):.2f}")
    dark=lambda f: (f[...,3]>0)
    check("no frame has a stray huge jump (smooth)", max(np.abs(fr[i+1][...,3]-fr[i][...,3]).mean() for i in range(14))<25)
finally: shutil.rmtree(tmp,ignore_errors=True)
# --- props added Nov 12 (Ep 16): prostate diagram, exit timing (HARD_RULES 21), stamp plate, no ambient layers
pj=json.loads(node("const {propHtml}=require('./props.js');const b=require('./backdrops.js');const st={top:420,bottom:915};"
 "const o=propHtml({t:'organ',kind:'prostate',label:'PROSTATE',at:[540,.5],fill:.9,in:0},1,'s0',0,1,st);"
 "const a=propHtml({t:'stamp',text:'X',at:[540,.5],in:0,out:2},1.9,'s0',0,1,st),g=propHtml({t:'stamp',text:'X',at:[540,.5],in:0,out:2},2.3,'s0',0,1,st);"
 "const pl=propHtml({t:'stamp',text:'X',plate:true,at:[540,.5],in:0},1,'s0',0,1,st);"
 "console.log(JSON.stringify({org:o.visible&&o.html.includes('PROSTATE')&&!/finger/i.test(o.html),a:a.visible,g:g.visible,plate:(pl.html.match(/<rect/g)||[]).length,plain:b.bgLayers('plain').length,rings:/stroke=\"#7fe3d3\"/.test(b.bgLayers('plain').map(l=>l.s).join(''))}))"))
check("prostate organ kind renders with its label chip", pj["org"])
check("a prop with `out` is on screen before it and gone 0.25 s after (rule 21)", pj["a"] and not pj["g"])
check("stamp `plate` draws a backing plate", pj["plate"]>=3)
check("plain backdrop has no decorative rings (rule 21)", pj["plain"]==1 and not pj["rings"])

# --- prop added Nov 13 (Ep 17): brain organ kind
bj=json.loads(node("const {propHtml}=require('./props.js');const st={top:420,bottom:915};"
 "const o=propHtml({t:'organ',kind:'brain',label:'BRAIN',at:[540,.5],fill:.9,in:0},1,'s0',0,1,st);"
 "const c=propHtml({t:'organ',kind:'colon',at:[540,.5],fill:.9,in:0},1,'s0',0,1,st);"
 "console.log(JSON.stringify({org:o.visible&&o.html.includes('BRAIN')&&o.html.includes('C-140 -160')&&!/finger/i.test(o.html),other:!c.html.includes('C-140 -160')}))"))
check("brain organ kind renders with its label chip and does not leak into other kinds", bj["org"] and bj["other"])
# --- Ep 18 (Nov 14): sprint props + backdrops, loop pose (HARD_RULES 22, 25)
ej=json.loads(node("const {propHtml,PROPS}=require('./props.js');const b=require('./backdrops.js');const r=require('./cyto_rig.js');const st={top:400,bottom:915};"
 "const mk=(p,t)=>propHtml(Object.assign({at:[540,.5],fill:.8,in:0},p),t,'s0',0,1,st);"
 "const e=mk({t:'ecgLine'},1.5),bh=mk({t:'bicepHeart'},1.6),bh0=mk({t:'bicepHeart'},.3),c=PROPS.cellSlice({fill_share:.33,label:'HEART CELL'},4),c5=PROPS.cellSlice({fill_share:.5},4),f=mk({t:'fatigueMeter',labels:['HEART','BICEP'],values:[20,90]},3),fn=mk({t:'fatigueMeter',show_numbers:true},3);"
 "const gaps=n=>{const ev=PROPS[n]({in:0},0).events.filter(x=>x<=6);return Math.max(...ev.map((x,i)=>i?x-ev[i-1]:x));};"
 "const tl={fps:30,duration:20,loop:true,seed:5,words:[],beats:[{t:0,emotion:'shock',gaze:[0,0]},{t:15,emotion:'laugh'}]};const z=r.state(0,tl),l=r.state(20-1/30,tl),m=r.state(19.2,tl);"
 "console.log(JSON.stringify({vis:[e,bh,f].every(x=>x.visible),heart:bh.html.includes('#ff5a5f')&&!bh0.html.includes('#ff5a5f'),nofinger:!/finger/i.test(bh.html+e.html+f.html),"
 "share:c.share,share5:c5.share,chip:c.svg.includes('HEART CELL'),nonum:!/>\\d+</.test(f.html),num:/>\\d+</.test(fn.html),gap:Math.max(...['ecgLine','bicepHeart','cellSlice','fatigueMeter'].map(gaps)),"
 "bgs:['gym','chestcavity'].map(k=>b.bgLayers(k).length),txt:/<text/.test(b.bgLayers('gym').map(x=>x.s).join('')),kinds:b.KINDS.includes('gym')&&b.KINDS.includes('chestcavity'),"
 "loop:['gx','gy','tilt','bob','cupDy','cupRot','brow','blink'].every(k=>Math.abs(z[k]-l[k])<1e-6)&&z.expr===l.expr,mid:m.expr!=='shock',smil:Math.abs((r.smilTime(20-1/30,tl)/2.4)%1)<1e-6||Math.abs((r.smilTime(20-1/30,tl)/2.4)%1-1)<1e-6}))"))
check("Ep 18 props render (ecgLine, bicepHeart, fatigueMeter), no fingers", ej["vis"] and ej["nofinger"])
check("bicepHeart: the heart pops only after the press", ej["heart"])
check("cellSlice: mitochondria cover the declared share of the cell (0.33 -> ~1/3, 0.5 -> ~1/2) + label chip", abs(ej["share"]-.33)<.03 and abs(ej["share5"]-.5)<.04 and ej["chip"], f"{ej['share']}, {ej['share5']}")
check("fatigueMeter: no numerals unless show_numbers", ej["nonum"] and ej["num"])
check("Ep 18 props keep producing a new thing every <= 2 s", ej["gap"]<=2.0, f"max gap {ej['gap']:.2f}s")
check("gym + chestcavity backdrops: 3 parallax layers each, registered, gym has no signage text", ej["bgs"]==[3,3] and ej["kinds"] and not ej["txt"])
check("loop: the last frame's pose equals frame 0 and the steam clock is back at phase 0 (HARD_RULES 22)", ej["loop"] and ej["mid"] and ej["smil"])
print(f"\n{sum(R)}/{len(R)} passed"); sys.exit(0 if all(R) else 1)

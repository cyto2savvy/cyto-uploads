import sys; sys.path.insert(0, "/home/claude/hf/lf02")
from lib import *
import math
import sets as X

def thumbA():
    S = Scene("thA", 0, 1.0)
    S.add('<div class="fill" style="background:radial-gradient(ellipse at 40% 50%,#ff5a4a,#8e0b20 55%,#3a0510)"></div>'
          '<svg class="fill" width="1920" height="1080" style="position:absolute;opacity:.25">' + "".join(f'<path d="M760 560 L{760 + 1500 * math.cos(a / 12 * 6.283):.0f} {560 + 1500 * math.sin(a / 12 * 6.283):.0f} L{760 + 1500 * math.cos((a + .4) / 12 * 6.283):.0f} {560 + 1500 * math.sin((a + .4) / 12 * 6.283):.0f}Z" fill="#ffd166"/>' for a in range(12)) + '</svg>')
    # giant lever
    S.add('<svg class="fill" width="1920" height="1080" style="position:absolute;z-index:5"><rect x="860" y="300" width="250" height="560" rx="30" fill="#d9d4c7" stroke="#0c1622" stroke-width="14"/>'
          '<rect x="960" y="380" width="50" height="420" rx="24" fill="#555"/><g transform="rotate(35 985 790)"><rect x="960" y="380" width="50" height="420" rx="20" fill="#9aa3ab" stroke="#0c1622" stroke-width="10"/><rect x="900" y="300" width="170" height="90" rx="40" fill="#e63946" stroke="#0c1622" stroke-width="12"/></g></svg>')
    S.cyto(560, 640, 1.0, x_expr=[(0, 1, "shocked")], blinks=[], z=10, phone=True)
    S.j('tl.set("#armR",{rotation:-70},0);tl.set(["#v_rest","#v_mbp","#v_small"],{opacity:0},.4);tl.set("#v_o",{opacity:1},.4);tl.set("#cyto",{rotation:-6},0);')
    S.char("neutro", "nt", 1380, 360, .95, pose="facepalm", expr=[(0, 1, "exhausted")], blinks=[], bob=False)
    S.char("rhino", "rh", 1150, 690, .7, pose="sneak", expr=[(0, 1, "smug")], blinks=[], bob=False, z=4)
    S.over('<div style="position:absolute;left:1180px;top:50px;width:700px;text-align:center;z-index:80;font:200px/0.9 InterBlack;color:#FAF4E8;-webkit-text-stroke:9px #0c1622;paint-order:stroke fill;text-shadow:0 14px 0 rgba(0,0,0,.45)">CODE <span style="color:#FFD166">RED</span></div>')
    return S

def thumbB():
    S = Scene("thB", 0, 1.0)
    S.add('<div class="fill" style="background:radial-gradient(ellipse at 30% 55%,#3fc1b0,#1f2b4d 60%,#0c1622)"></div>')
    S.add('<div class="fill" style="z-index:2;clip-path:polygon(62% 0,100% 0,100% 100%,48% 100%);background:#222;filter:grayscale(1)"></div>')
    S.cyto(620, 720, 1.0, x_expr=[(0, 1, "shocked")], blinks=[], z=10)
    S.j('tl.set(["#v_rest","#v_mbp","#v_small"],{opacity:0},.4);tl.set("#v_o",{opacity:1},.4);tl.set("#pupL",{x:6},0);tl.set("#pupR",{x:6},0);')
    S.char("rhino", "rh", 1180, 420, 1.35, pose="sneak", expr=[(0, 1, "smug")], blinks=[], bob=False, z=6)
    S.over('<div style="position:absolute;left:60px;top:40px;width:1100px;z-index:80;font:170px/0.95 InterBlack;color:#FAF4E8;-webkit-text-stroke:8px #0c1622;paint-order:stroke fill;text-shadow:0 12px 0 rgba(0,0,0,.45)">SICK BY <span style="color:#FFD166">BREAK?</span></div>')
    return S

for f in (thumbA, thumbB): f().build()
import re as _re
for t in ("thA", "thB"):
    f = f"{P}/{t}/index.html"; h = open(f).read()
    open(f, "w").write(_re.sub(r'const MOUTH=\[[^;]*\];', 'const MOUTH=[[0,"o"]];', h))

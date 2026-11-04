"""Render Cyto (toque, cup) to transparent PNGs for the security-cam twist shot: arm down + arm up (yanking the lever)."""
import sys; sys.path.insert(0, "/home/claude/hf")
import cyto3 as R, cytohf as C
from playwright.sync_api import sync_playwright
rig = R.rig3_html("outfit_pufferhoodie", "cup_red2")
for name, rot in (("down", 0), ("up", -128)):
    html = f"""<html><head><style>{C.FONT_CSS}*{{margin:0}}body{{background:transparent;width:1200px;height:1300px}}{R.rig3_css()}
#cytoPos{{transform:none!important}}</style></head><body><div style="position:relative;width:1200px;height:1300px">{rig}</div>
<script>const a=document.querySelector('#armR'); a.setAttribute('transform','rotate({rot} {R.SH_R[0]} {R.SH_R[1]})');</script></body></html>"""
    open(f"/home/claude/hf/lf02/_cy_{name}.html", "w").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); pg = b.new_page(viewport={"width": 1200, "height": 1300})
    for name in ("down", "up"):
        pg.goto(f"file:///home/claude/hf/lf02/_cy_{name}.html"); pg.wait_for_timeout(300)
        pg.screenshot(path=f"/home/claude/hf/lf02/assets/cy_{name}.png", omit_background=True)
    b.close()
print("ok")

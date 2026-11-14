#!/usr/bin/env python3
"""Render one contact sheet of everything in LIBRARY.md: every prop, every backdrop, every transition.

    python3 studio/rig_v2/library_render.py            -> studio/rig_v2/library.png

So Utsha and the idea chat can see what already exists before anyone asks for a new visual (HARD_RULES 19).
Costs nothing: it is the same local renderer the episodes use.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "library.png")

PROPS = [
    {"t": "organ", "kind": "colon", "label": "COLON"},
    {"t": "organ", "kind": "lungs", "label": "LUNGS"},
    {"t": "organ", "kind": "brain", "label": "BRAIN"},
    {"t": "bars", "values": [80, 74], "labels": ["EXERCISE", "PAMPHLETS"]},
    {"t": "counter", "to": 1.44, "suffix": "M", "decimals": 2, "label": "ADULTS"},
    {"t": "arrowStat", "label": "-28%", "dir": "down"},
    {"t": "arrowStat", "label": "+2x", "dir": "up"},
    {"t": "icons", "glyph": "organ", "n": 13, "cols": 7, "label": "13 CANCERS", "spread": 0.1},
    {"t": "icons", "glyph": "person", "n": 7, "cols": 7, "label": "EVERYONE", "spread": 0.1},
    {"t": "icons", "glyph": "shoe", "n": 5, "cols": 5, "spread": 0.1},
    {"t": "icons", "glyph": "cell", "n": 6, "cols": 6, "spread": 0.1},
    {"t": "icons", "glyph": "check", "n": 6, "cols": 6, "spread": 0.1},
    {"t": "peopleGrid", "n": 36, "cols": 12, "hi": 9, "label": "889 PATIENTS", "spread": 0.1},
    {"t": "card", "title": "36 MONTHS", "ticks": 36, "cols": 12, "foot": "AFTER CHEMO"},
    {"t": "stamp", "text": "LINKED, NOT PROVEN"},
    {"t": "shoe"},
    {"t": "runner"},
    {"t": "stopSign", "title": "TTC", "text": "WALK IT"},
    {"t": "ecgLine"},
    {"t": "bicepHeart"},
    {"t": "cellSlice", "kind": "heartCell", "fill_share": 0.33, "label": "HEART CELL"},
    {"t": "fatigueMeter", "labels": ["HEART", "BICEP"], "values": [20, 90]},
]
BACKDROPS = ["trail", "hospital", "lab", "subway", "streetcar", "skyline", "lake", "snow", "plain", "gym", "chestcavity"]
TRANSITIONS = ["whip", "zoom", "membrane", "doors"]

JS = r"""
const path=require('path'); process.chdir(__dirname);
const {propHtml}=require('./props.js'); const {layers}=require('./backdrops.js'); const {chromium}=require('playwright');
const PROPS=JSON.parse(process.argv[2]), BGS=JSON.parse(process.argv[3]), OUT=process.argv[4];
const W=1080,H=1920, TW=360, TH=640;
const label=s=>`<div style="position:absolute;left:0;bottom:0;right:0;background:rgba(10,31,36,.86);color:#fff;font:700 34px Arial;padding:10px 14px">${s}</div>`;
(async()=>{
 const br=await chromium.launch(); const pg=await br.newPage({viewport:{width:TW*5,height:TH}});
 const tiles=[];
 // props on a neutral stage
 for(const p of PROPS){
  const spec=Object.assign({at:[540,0.5],fill:0.78,in:0},p);
  const r=propHtml(spec,2.0,'lib',0,1,{top:160,bottom:1760});
  const name=p.t+(p.kind?':'+p.kind:'')+(p.glyph?':'+p.glyph:'')+(p.dir==='up'?':up':'');
  tiles.push(`<div style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:#16254f">${r.html}${label(name)}</div>`);
 }
 for(const k of BGS){
  tiles.push(`<div style="position:relative;width:${W}px;height:${H}px;overflow:hidden">${layers(k,5).map(l=>`<div style="position:absolute;inset:0">${l.s}</div>`).join('')}${label('bg: '+k)}</div>`);
 }
 const rows=[];
 for(let i=0;i<tiles.length;i+=5){
  const row=tiles.slice(i,i+5);
  await pg.setContent(`<body style="margin:0;font-size:0;white-space:nowrap;background:#0a1f24">${row.map(t=>`<div style="display:inline-block;width:${TW}px;height:${TH}px;overflow:hidden"><div style="transform:scale(${TW/W});transform-origin:0 0">${t}</div></div>`).join('')}</body>`);
  await pg.evaluate(()=>document.querySelectorAll('svg').forEach(e=>{try{e.pauseAnimations();e.setCurrentTime(2)}catch(_){}}));
  await pg.screenshot({path:`${OUT}.row${rows.length}.png`});
  rows.push(rows.length);
 }
 console.log(JSON.stringify({rows:rows.length,cols:5,tw:TW,th:TH}));
 await br.close();
})();
"""


def main():
    js = os.path.join(HERE, "_library_render.js")
    open(js, "w").write(JS)
    env = dict(os.environ)
    env.setdefault("SEED", "3")
    stamp = os.path.join(tempfile.mkdtemp(), "lib")
    try:
        out = subprocess.run(["node", js, json.dumps(PROPS), json.dumps(BACKDROPS), stamp],
                             capture_output=True, text=True, env=env, cwd=HERE)
        if out.returncode:
            print(out.stdout, out.stderr, file=sys.stderr); sys.exit(1)
        meta = json.loads(out.stdout.strip().splitlines()[-1])
    finally:
        os.path.exists(js) and os.remove(js)
    rows = [Image.open(f"{stamp}.row{i}.png") for i in range(meta["rows"])]
    # transitions get a written strip rather than a still: a still of a cut says nothing
    cap_h = 150
    sheet = Image.new("RGB", (rows[0].width, sum(r.height for r in rows) + cap_h), "#0a1f24")
    y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    d.text((16, y + 18), "transitions (see them moving in any episode's transition_plot.png): "
                         + "  ".join(TRANSITIONS), fill="#ffc83a")
    d.text((16, y + 58), "props scale to `fill` (share of the prop stage height); `at` = [x px, y 0..1 of the stage]", fill="#ffffff")
    d.text((16, y + 98), "full parameters + copy-paste JSON: studio/rig_v2/LIBRARY.md", fill="#7fe3d3")
    sheet.save(OUT, quality=92)
    print(f"library sheet: {OUT}  ({len(PROPS)} props, {len(BACKDROPS)} backdrops, {len(TRANSITIONS)} transitions)")


if __name__ == "__main__":
    main()

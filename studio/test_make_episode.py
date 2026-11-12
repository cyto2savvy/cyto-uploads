#!/usr/bin/env python3
"""Offline tests for make_episode.validate + the layout verdicts and the scene cache key (no render):
   python3 -I studio/test_make_episode.py"""
import sys, os, copy, json, subprocess, tempfile; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import make_episode as M
G = dict(ep=1, title="Short title", health=True, fit="hoodie", publish_at="2026-11-12T23:00:00Z", pinned_comment="q? sources in description",
  script=[dict(say="Hello there fam.", scene=0, emotion="chill"), dict(say="Not medical advice.", scene=1)], scenes=[dict(bg="skyline", headline="HI", props=["heart", "bars"]), dict(bg="subway", headline="BYE", props=["arrow", "icons"])],
  thumbnails=[dict(id="A", headline=["ONE", "TWO"], hero="heart", photo="p.jpg", bg_subject="short + Sunnybrook"), dict(id="B", headline=["THREE"], hero="clock", photo="p.jpg", bg_subject="title + Princess Margaret")], stronger="A",
  sources=[dict(short="X 2020", full="X. https://pubmed.ncbi.nlm.nih.gov/1/")], description="Test. Not medical advice.", tags=["a"])
def errs(**kw):
    E = copy.deepcopy(G); E.update(kw); return M.validate(E)[0]
T = [("good passes", lambda: errs() == []), ("long title", lambda: any("title" in e for e in errs(title="x" * 61))),
 ("bad emotion", lambda: any("emotion" in e for e in errs(script=[dict(say="a b", scene=0, emotion="angry"), dict(say="c", scene=1)]))),
 ("scene order", lambda: any("in order" in e for e in errs(script=[dict(say="a", scene=1), dict(say="b", scene=0)]))),
 ("real brand", lambda: any("brand" in e for e in errs(description="Tim Hortons. Not medical advice."))),
 ("no med line", lambda: any("medical" in e for e in errs(description="Plain."))),
 ("one thumb", lambda: any("A/B" in e for e in errs(thumbnails=G["thumbnails"][:1]))),
 ("generic skyline thumb", lambda: any("skyline" in e for e in errs(thumbnails=[dict(id="A", headline=["A"], hero="heart", photo="p", bg_subject="short + CN Tower skyline"), G["thumbnails"][1]]))),
 ("no props", lambda: any("props" in e for e in errs(scenes=[dict(bg="skyline", headline="HI"), G["scenes"][1]]))),
 ("same backdrop", lambda: any("backdrop" in e for e in errs(scenes=[G["scenes"][0], dict(G["scenes"][0])]))),
 ("bad stronger", lambda: any("stronger" in e for e in errs(stronger="Z"))),
 ("missing episode.json -> rc 2", lambda: M.main(["ep9999", "--dry-run"]) == 2),
 # HARD_RULES 17/18 verdicts
 ("overlap: none recorded -> not measured", lambda: M.overlap_verdict({})[0] and "not measured" in M.overlap_verdict({})[1]),
 ("overlap: empty list passes", lambda: M.overlap_verdict({"overlaps": []})[0]),
 ("overlap: one >0.3s fails and names the pair",
  lambda: (not M.overlap_verdict({"overlaps": [dict(pair="s1:organ1 x s1:peopleGrid0", scene="s1", dur=0.4, t0=1.2)]})[0])
          and "organ1" in M.overlap_verdict({"overlaps": [dict(pair="s1:organ1 x s1:peopleGrid0", scene="s1", dur=0.4, t0=1.2)]})[1]),
 ("pose: eased blend passes", lambda: M.pose_verdict({"pose_jerk_in_cut": {"s1": 1.71, "s2": 1.66}})[0] == []),
 ("pose: a snap fails", lambda: any("s3" in b for b in M.pose_verdict({"pose_jerk_in_cut": {"s1": 1.2, "s3": 8.4}})[0])),
 # HARD_RULES 19 scene cache: the key is stable, and changing a scene reKEYs that scene AND the next one
 ("cache key stable / changes with the scene", lambda: _cache_key_test())]

def _cache_key_test():
    plan = dict(fps=30, duration=6.0, fit="hoodie", seed=7, cytoX=64, cytoY=1110, cytoSize=840, keys={}, words=[], beats=[],
                scenes=[dict(id="s0", bg="trail", start=0.0, end=2.0, headline="A", props=[]),
                        dict(id="s1", bg="lab", start=2.0, end=4.0, headline="B", props=[]),
                        dict(id="s2", bg="plain", start=4.0, end=6.0, headline="C", props=[])])
    js = ("const {segKey}=require(process.argv[2]);const p=JSON.parse(require('fs').readFileSync(process.argv[3]));"
          "console.log(JSON.stringify(p.scenes.map((s,i)=>segKey(p,i,Math.round(s.start*30),Math.round(s.end*30)))));")
    rig = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rig_v2")
    shim = os.path.join(rig, "_cachekey_shim.js")
    src = open(os.path.join(rig, "compose.js")).read()
    open(shim, "w").write(src[:src.index("(async () => {")] + "module.exports={segKey};\n")
    def keys(pl):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f: json.dump(pl, f); fn = f.name
        try: return json.loads(subprocess.run([ "node", "-e", js, "x", shim, fn], capture_output=True, text=True, cwd=rig).stdout)
        finally: os.remove(fn)
    try:
        a = keys(plan); b = keys(copy.deepcopy(plan))
        edited = copy.deepcopy(plan); edited["scenes"][1]["headline"] = "CHANGED"
        c = keys(edited)
        # same plan -> same keys; edited scene 1 -> its own key changes AND scene 2's (its cut shows scene 1), scene 0 untouched
        return a == b and len(a) == 3 and all(a) and c[0] == a[0] and c[1] != a[1] and c[2] != a[2]
    finally:
        os.path.exists(shim) and os.remove(shim)

bad = [n for n, f in T if not f()]; print(f"{len(T) - len(bad)}/{len(T)} passed", bad or ""); sys.exit(1 if bad else 0)

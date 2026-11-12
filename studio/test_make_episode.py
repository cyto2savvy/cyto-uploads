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

# ---- HARD_RULES 20 / 21 (from Ep 16)
def _g16(**kw):
    E = copy.deepcopy(G); E.update(ep=16, description="Test. Not medical advice. See a doctor.",
        script=[dict(say="Big number fam.", scene=0), dict(say="Yo, it's ya boy Cyto.", scene=1), dict(say="Not medical advice.", scene=2)],
        scenes=[dict(bg="snow", headline="HI", props=[dict(t="stamp", text="X", shows="the big number", anchor="number")]), dict(bg="lake", headline="YO", props=[]), dict(bg="snow", headline="BYE", props=[])])
    E.update(kw); return E
def _u(bgs, props=("stamp",), tr="whip", pub="2026-01-01"):
    return M.usage_of(dict(publish_at=pub, scenes=[dict(bg=b, transition=tr, props=[dict(t=p, at=[1, .5]) for p in props]) for b in bgs]))
T += [("r21: anchored prop + clean scenes pass", lambda: M.validate(_g16())[0] == []),
 ("r21: prop without shows/anchor fails", lambda: any("shows" in e for e in M.validate(_g16(scenes=[dict(bg="snow", headline="HI", props=[dict(t="stamp")]), dict(bg="lake", headline="YO", props=[]), dict(bg="snow", headline="BYE", props=[])]))[0])),
 ("r21: anchor must be a word said in the scene", lambda: any("not a word said" in e for e in M.validate(_g16(scenes=[dict(bg="snow", headline="HI", props=[dict(t="stamp", shows="x", anchor="banana")]), dict(bg="lake", headline="YO", props=[]), dict(bg="snow", headline="BYE", props=[])]))[0])),
 ("r21: catchphrase/outro props fail", lambda: sum("no props allowed" in e for e in M.validate(_g16(scenes=[dict(bg="snow", headline="HI", props=[]), dict(bg="lake", headline="YO", props=[dict(t="runner", shows="x", anchor="yo")]), dict(bg="snow", headline="BYE", props=[dict(t="shoe", shows="x", anchor="not")])]))[0]) == 2),
 ("r21 render: prop past sentence + 1.5 s fails", lambda: not M.floater_verdict(dict(scenes=[dict(id="s0", start=0, end=9, props=[dict(t="stamp", **{"in": 1.0}, sent_end=2.0)])]), dict(census=[dict(t=4.0, s="s0", ids=["s0:stamp0"])]))[0]),
 ("r21 render: prop inside its window passes", lambda: M.floater_verdict(dict(scenes=[dict(id="s0", start=0, end=9, props=[dict(t="stamp", **{"in": 1.0}, sent_end=2.0)])]), dict(census=[dict(t=3.0, s="s0", ids=["s0:stamp0"])]))[0]),
 ("r21 render: any prop in a clean scene fails", lambda: not M.floater_verdict(dict(scenes=[dict(id="s2", start=0, end=5, clean=True, props=[])]), dict(census=[dict(t=1.0, s="s2", ids=["s2:runner0"])]))[0]),
 ("r20: clone of the previous episode fails", lambda: not M.variety_verdict("ep16", dict(publish_at="2026-02-01", scenes=[dict(bg=b, transition="whip", props=[dict(t="stamp", at=[1, .5])]) for b in ("lab", "plain")]), {"ep15": _u(("lab", "plain"))})[0]),
 ("r20: fresh mix with a new item passes", lambda: M.variety_verdict("ep16", dict(publish_at="2026-02-01", scenes=[dict(bg=b, transition="zoom", props=[dict(t="card", at=[2, .4])]) for b in ("snow", "lake")]), {"ep15": _u(("lab", "plain"))})[0]),
 ("r20: no new/least-recently-used item fails", lambda: any("least-recently-used" in x for x in [M.variety_verdict("ep16", dict(publish_at="2026-02-01", scenes=[dict(bg=b, transition="zoom", props=[dict(t="stamp", at=[9, .9])]) for b in ("plain", "lab")]), {"ep15": _u(("lab", "plain"))})[1]]))]

bad = [n for n, f in T if not f()]; print(f"{len(T) - len(bad)}/{len(T)} passed", bad or ""); sys.exit(1 if bad else 0)

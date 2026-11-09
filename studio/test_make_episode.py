#!/usr/bin/env python3
"""Offline tests for make_episode.validate (no render): python3 -I studio/test_make_episode.py"""
import sys, os, copy; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import make_episode as M
G = dict(ep=1, title="Short title", health=True, fit="hoodie", publish_at="2026-11-12T23:00:00Z", pinned_comment="q? sources in description",
  script=[dict(say="Hello there fam.", scene=0, emotion="chill"), dict(say="Not medical advice.", scene=1)], scenes=[dict(bg="skyline", headline="HI"), dict(bg="skyline", headline="BYE")],
  thumbnails=[dict(id="A", headline=["ONE", "TWO"], hero="heart"), dict(id="B", headline=["THREE"], hero="clock")], stronger="A",
  sources=[dict(short="X 2020", full="X. https://pubmed.ncbi.nlm.nih.gov/1/")], description="Test. Not medical advice.", tags=["a"])
def errs(**kw):
    E = copy.deepcopy(G); E.update(kw); return M.validate(E)[0]
T = [("good passes", lambda: errs() == []), ("long title", lambda: any("title" in e for e in errs(title="x" * 61))),
 ("bad emotion", lambda: any("emotion" in e for e in errs(script=[dict(say="a b", scene=0, emotion="angry"), dict(say="c", scene=1)]))),
 ("scene order", lambda: any("in order" in e for e in errs(script=[dict(say="a", scene=1), dict(say="b", scene=0)]))),
 ("real brand", lambda: any("brand" in e for e in errs(description="Tim Hortons. Not medical advice."))),
 ("no med line", lambda: any("medical" in e for e in errs(description="Plain."))),
 ("one thumb", lambda: any("A/B" in e for e in errs(thumbnails=G["thumbnails"][:1]))),
 ("bad stronger", lambda: any("stronger" in e for e in errs(stronger="Z"))),
 ("missing episode.json -> rc 2", lambda: M.main(["ep9999", "--dry-run"]) == 2)]
bad = [n for n, f in T if not f()]; print(f"{len(T) - len(bad)}/{len(T)} passed", bad or ""); sys.exit(1 if bad else 0)

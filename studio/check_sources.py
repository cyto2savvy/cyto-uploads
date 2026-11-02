#!/usr/bin/env python3
"""Flag DOIs / PMIDs reused across episodes. Run from repo root: python3 studio/check_sources.py"""
import re,glob,collections
use=collections.defaultdict(set)
for f in glob.glob("studio/episodes/ep*/*brief.md")+glob.glob("studio/episodes/ep*/meta.json"):
    ep=re.search(r"ep(\d+)",f).group(1)
    t=open(f,encoding="utf-8").read().replace("\\/","/")
    for d in re.findall(r"10\.\d{4,9}/[^\s\"'<>)\]\\,;]+",t): use[d.rstrip('.').lower()].add(ep)
    for p in re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)",t): use["pmid:"+p].add(ep)
bad=0
for k,v in sorted(use.items()):
    if len(v)>1: bad+=1; print("REUSED",k,"in eps",sorted(v))
print("OK: no reused sources" if not bad else f"{bad} reused source(s) — fix before building")

#!/usr/bin/env python3
"""suggest_scenes.py - HARD_RULES 20 scene picker. Mixes the library instead of cloning the last episode.
   python3 studio/suggest_scenes.py --for=ep16 prostate cancer november   # 3 candidate sets per scene role, vs the 3 episodes before ep16
   python3 studio/suggest_scenes.py --usage                               # rewrite rig_v2/library_usage.json + print last-used table
Per role (hook, explain, stat, limits, payoff, clean) it prints 3 backdrop + prop sets that fit the tags, least-recently-used first,
none of them a backdrop+prop combo used in the last 3 episodes. `clean` = catchphrase/outro: backdrop only (HARD_RULES 21)."""
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import make_episode as M
def main(argv):
    U = M.write_usage(HERE); usage = json.load(open(os.path.join(HERE, "rig_v2", "library_usage.json")))
    T = json.load(open(os.path.join(HERE, "rig_v2", "library_tags.json"))); order = usage["order"]; last = usage["last_used"]
    age = lambda it: len(order) - order.index(last[it]) if it in last else 99          # 99 = never used (new)
    if "--usage" in argv:
        for kind in ("backdrops", "props", "transitions"):
            print(f"\n{kind}:"); [print(f"  {it:16s} last used: {last.get(it, 'never')}") for it in sorted(T[kind], key=lambda i: -age(i))]
        return 0
    me = next((a.split("=")[1] for a in argv if a.startswith("--for=")), None)   # --for=ep16: compare with the 3 episodes published before it
    if me in order: order = order[:order.index(me)]; last = {}; [last.__setitem__(it, k) for k in order for it in set(U[k]["backdrops"]) | set(U[k]["props"]) | set(U[k]["transitions"])]
    tags = {a.lower() for a in argv if not a.startswith("-")}; last3 = order[-3:]
    seen = {c for k in last3 for c in U[k]["combos"]}
    score = lambda it, d: 3 * len(tags & set(d["tags"])) + min(age(it), 6) * 0.5      # topic fit first, then least recently used
    print(f"tags: {sorted(tags) or '(none)'} | compared with: {', '.join(last3)}")
    for role in ("hook", "explain", "stat", "limits", "payoff", "clean"):
        B = sorted((b for b, d in T["backdrops"].items() if role in d["roles"]), key=lambda b: -score(b, T["backdrops"][b]))
        P = sorted((p for p, d in T["props"].items() if role in d["roles"]), key=lambda p: -score(p, T["props"][p]))
        print(f"\n{role}:"); n = 0
        if role == "clean":
            for b in B[:3]: print(f"  bg {b:10s} (no props)   last used {last.get(b, 'never')}")
            continue
        pairs = [p for p in itertools.combinations(P[:5], 2) if p[0].split(":")[0] != p[1].split(":")[0]] or [(p,) for p in P[:3]]
        for i in range(len(B) * len(pairs)):
            b, pair = B[i % len(B)], pairs[(i // len(B) + i) % len(pairs)]; combo = b + "|" + "+".join(sorted(pair))
            if combo in seen: continue
            print(f"  bg {b:10s} props {' + '.join(pair)}   (last used: {last.get(b, 'never')} / {' / '.join(last.get(q, 'never') for q in pair)})")
            seen.add(combo); n += 1
            if n == 3: break
    print("\nEvery prop still needs `shows` + `anchor` (the spoken word it appears on). Vary at/fill/count/colour when reusing.")
    return 0
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))

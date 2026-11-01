"""Check an episode's upload metadata against studio/PUBLISHING.md.  python3 check_meta.py epNN/meta.json
meta.json:
{ "format": "short" | "long",
  "keyword": "why do you wake up at 3am",          # primary search phrase (plain English)
  "title": "...", "description": "...", "tags": ["..."],
  "category_id": 27, "made_for_kids": false, "synthetic": true, "health": true,
  "duration_s": 29.5, "thumbnails": ["thumb-A.jpg", "thumb-B.jpg"],
  "playlist": "Wagwan with your...", "pinned_comment": "...", "related_video": "Ep N title or ID" }
Exit code 1 if any FAIL."""
import json, re, sys

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⬀-⯿]")
BRAND_HASH = {"#science", "#toronto", "#6ix"}


def check(m):
    out = []
    F = lambda msg: out.append(("FAIL", msg))
    W = lambda msg: out.append(("WARN", msg))
    fmt = m.get("format")
    if fmt not in ("short", "long"): F("format must be 'short' or 'long'"); return out
    t, d, kw = m.get("title", ""), m.get("description", ""), m.get("keyword", "").lower().strip()
    tags = [x.lower() for x in m.get("tags", [])]

    # ---- title
    n = len(t)
    if n > 70: F(f"title is {n} chars (over 70 gets cut off in search and on small screens)")
    elif fmt == "short" and n > 60: F(f"title is {n} chars (Shorts standard is ≤ 60)")
    elif fmt == "long" and n > 60: W(f"title is {n} chars (long-form sweet spot 50–60)")
    if fmt == "long" and n < 40: W(f"title is only {n} chars (long-form sweet spot 50–60)")
    if "#" in t: F("hashtag in the title — move it to the end of the description")
    if not kw: F("set 'keyword' (the plain-English phrase people search)")
    else:
        words = [w for w in re.findall(r"[a-z0-9]+", kw) if len(w) > 2]
        head = t[:40].lower()
        hit = sum(w in head for w in words)
        if words and hit < max(1, round(len(words) * .6)): F(f"keyword not in the first 40 chars of the title ('{t[:40]}')")
    if len(EMOJI.findall(t)) > 1: W("more than 1 emoji in the title")
    if t.isupper(): W("title is all caps")

    # ---- description
    first = d.strip().split("\n")[0]
    if kw and not any(w in d[:150].lower() for w in re.findall(r"[a-z0-9]{4,}", kw)): F("keyword missing from the first 150 chars of the description")
    words = len(re.findall(r"\b\w+\b", re.sub(r"#\w+|https?://\S+", "", d)))
    lo, hi = (40, 220) if fmt == "short" else (200, 600)
    if words < lo: W(f"description is {words} words (aim {lo}–{hi})")
    if words > hi: W(f"description is {words} words (aim {lo}–{hi})")
    if not re.search(r"https?://(doi\.org|pubmed\.ncbi\.nlm\.nih\.gov|www\.ncbi\.nlm\.nih\.gov)", d): F("no PubMed/DOI source link in the description")
    if m.get("health") and "not medical advice" not in d.lower(): F("health topic without 'Not medical advice.'")
    hs = re.findall(r"#\w+", d)
    if len(hs) > 15: F(f"{len(hs)} hashtags — YouTube ignores ALL of them past 15")
    if fmt == "short":
        if not BRAND_HASH <= {h.lower() for h in hs}: F(f"missing brand hashtags {sorted(BRAND_HASH - {h.lower() for h in hs})}")
        if "#shorts" not in [h.lower() for h in hs]: W("#shorts missing from description hashtags")
        if len(hs) > 8: W(f"{len(hs)} hashtags (keep ≤ 8: 1–3 topic + brand)")
        if hs and hs[0].lower() in BRAND_HASH | {"#shorts"}: W("put topic hashtags first, brand ones after")
    else:
        if not 3 <= len(hs) <= 5: W(f"{len(hs)} hashtags (long-form: 3–5)")
        ch = re.findall(r"^\s*(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$", d, re.M)
        if not ch: F("no chapters in the description (first must be 0:00)")
        else:
            secs = [sum(int(x) * 60 ** i for i, x in enumerate(reversed(c[0].split(":")))) for c in ch]
            if secs[0] != 0: F("first chapter must start at 0:00")
            if len(ch) < 3: F("need at least 3 chapters")
            if any(b - a < 10 for a, b in zip(secs, secs[1:])): F("chapters must be at least 10s apart")
            if any(re.match(r"(part|chapter|section)\s*\d", c[1], re.I) for c in ch): W("name chapters with keywords, not 'Part 1'")

    # ---- tags + settings
    if kw and (not tags or tags[0] != kw): F(f"first tag must be the exact keyword '{kw}'")
    if len(tags) > 15: W(f"{len(tags)} tags (keep 8–12 relevant ones)")
    if 0 < len(tags) < 6: W(f"only {len(tags)} tags (aim 8–12: keyword, variations, topic, context, brand, series)")
    tchars = sum(len(x) + (2 if " " in x else 0) for x in tags) + max(0, len(tags) - 1)
    if tchars > 500: F(f"tags total {tchars} chars — YouTube's limit is 500")
    if any("#" in x for x in tags): F("no '#' in tags (hashtags go in the description)")
    gen = [x for x in tags if x in {"science", "biology", "shorts", "video", "viral", "fyp", "trending", "health"}]
    if gen: W(f"single generic tags do nothing: {gen}")
    if not m.get("captions_srt"): W("captions_srt not set — run make_srt.py and upload it (auto-captions mangle slang)")
    for k in ("cyto the cell", "the body is the 6ix"):
        if k not in tags: W(f"tag '{k}' missing")
    if m.get("category_id") != 27: F("category_id must be 27 (Science & Technology)")
    if m.get("made_for_kids") is not False: F("made_for_kids must be false")
    if m.get("synthetic") is not True: F("synthetic (altered content) must be true")

    # ---- format-specific
    dur = m.get("duration_s")
    thumbs = m.get("thumbnails", [])
    if fmt == "short":
        if dur is None: W("duration_s not set")
        elif dur > 60: F(f"{dur}s — over 60s is not our Short format")
        elif dur > 35: W(f"{dur}s — target ≤ 30s")
        if len(thumbs) < 1: W("no thumbnail (still shows in search/browse)")
    else:
        if dur is not None and not 480 <= dur <= 900: W(f"{dur/60:.1f} min — 8–15 min only if retention holds")
        if len(thumbs) < 2: F("long-form needs 2–3 thumbnail options for Test & Compare")
        if not m.get("end_screen"): F("set 'end_screen' (what the last 20s points to)")
    for k, msg in (("playlist", "series playlist"), ("pinned_comment", "pinned comment (question + 'sources in description')"),
                   ("related_video", "related video (set in Studio)")):
        if not m.get(k): (F if k == "pinned_comment" else W)(f"{msg} not set")
    if m.get("pinned_comment") and "?" not in m["pinned_comment"]: W("pinned comment should ask a question")
    return out


if __name__ == "__main__":
    m = json.load(open(sys.argv[1]))
    res = check(m)
    for lvl, msg in res: print(f"{lvl:4}  {msg}")
    nf = sum(l == "FAIL" for l, _ in res)
    print(f"\n{m.get('format','?').upper()}  '{m.get('title','')}' ({len(m.get('title',''))} chars) — {nf} FAIL, {len(res) - nf} WARN" + ("  ✅ ready" if not nf else ""))
    sys.exit(1 if nf else 0)

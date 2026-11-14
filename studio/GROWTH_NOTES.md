# Growth notes — The Body is the 6ix

## Nov 14, 2026: the 1k ceiling, diagnosed (16 Shorts, YouTube Analytics API)

### The two populations
| Ep | Title | Len | Views | Avg % viewed | Avg sec held | Likes/1k | Shares | Subs |
|----|-------|-----|-------|--------------|--------------|----------|--------|------|
| 2  | Scared to death | 30s | 1486 | 56.5% | 16s | 16.8 | 2 | 4 |
| 5  | Cold season | 27s | 1356 | 62.8% | 16s | 11.1 | 0 | 1 |
| 3  | Sugar rush | 30s | 1262 | 65.2% | 19s | 21.4 | 3 | 5 |
| 9  | Vitamin D | 41s | 1258 | 41.5% | 16s | 17.5 | 1 | 1 |
| 11 | Diwali food coma | 39s | 1065 | 55.6% | 21s | 7.5 | 0 | 1 |
| 14 | Two minutes silence | 34s | 1053 | 42.2% | 14s | 11.8 | 0 | 3 |
| 13 | Neutro | 37s | 1027 | 39.7% | 14s | 11.6 | 0 | 1 |
| 17 | Quitting smoking | 36s | 943* | — | — | 10.6 | — | — |
| 8  | 3AM | 31s | 396 | 55.4% | 17s | 27.8 | 0 | 0 |
| 1  | Goosebumps | 31s | 264 | **90.9%** | **28s** | 45.6 | 3 | 3 |
| 4  | Clocks fall back | 26s | 143 | 63.8% | 16s | 49.0 | 0 | 0 |
| 6  | Procrastination | 29s | 140 | 51.5% | 14s | 85.7 | 0 | 0 |
| 12 | Movember self-checks | 42s | 86 | 31.2% | 13s | 35.7 | 0 | 0 |
| 7  | Hockey heart rate | 35s | 69 | 35.5% | 12s | 72.5 | 0 | 0 |
| 10 | Leafs vs Habs hormones | 40s | 57 | 38.1% | 15s | 53.6 | 0 | 0 |
| 15 | Exercise + cancer | 39s | 40 | — | — | 50.0 | 0 | 0 |

\* Ep 17 at ~9 hours old.

Nothing lands between 400 and 940. There are two outcomes: the Shorts feed seeds you (~1000)
or it doesn't (~50-150). Traffic source proves it:
- 6 winners: 5,667 of 6,635 views (85%) from the SHORTS feed — about 944 feed views each.
- 6 flops: 288 feed views **total across all six** — about 48 each. Their views come from the
  channel page (135) and search (23), i.e. people who already found us.

### Finding 1 — we hold ~15 seconds, full stop
Average seconds held is 12-21s on every episode except Ep 1. It does not move with length.
So percentage retention is just arithmetic on the denominator:
- Episodes ≤31s: mean 64% viewed.
- Episodes ≥34s: mean 40% viewed.
Retention did not get worse. The videos got longer while holding the same 15 seconds.
Ep 1 (31s) is the only one that held 28s / 91%, and it looped.

### Finding 2 — nothing asks for the signals that expand a Short
Per YouTube (Todd Sherman, Shorts product lead): a Short is shown to a "seed audience", and
"based on how that group responds" it either widens or levels off. YouTube publishes no
thresholds. Our seed audience watches and then does nothing:
- Shares: 0-3 per video. Nine episodes have **zero**. Shares are the strongest expansion signal.
- Comments: 0-2 per video.
- Likes: 0.7-2.1% of views on the seeded videos.
- Subs: 0.1-0.5% of views.
The outro asks for like + subscribe, the two weakest signals. No episode asks for a send.
Ep 17's pinned comment does ask ("Know someone trying to quit? Send them this") — but that
line is in a comment, not in the video.

### Finding 3 — the catchphrase sits in the most expensive 3 seconds
Measured from words_scribe: Ep 12 at 3.4s, Ep 13 at 4.5s, Ep 14 at 4.8s, Ep 15 at 8.5s,
Ep 16 at 9.8s. It costs 2-3s of the opening to say our own name to people who just swiped in.
Eps 12-14 have three of the four worst retention percentages in the catalogue.

### Finding 4 — topic decides whether you get seeded at all
Flops: local sports (hockey x2), a clock change, and two "does this health practice work"
angles that open on a caveat. Winners: "why does your body do X" and "is X real" — universal,
visceral, searchable. n=16, so a pattern, not a law.

### Finding 5 — thumbnails have been low-leverage
85% of views arrive through the feed, where the thumbnail is barely surfaced. The first frame
and the first two spoken words carry the load. Rule 3b work was worth doing once; it is not
where the next hour should go.

### Finding 6 — Ep 15 may not be classified as a Short
40 views in 36 hours and no feed push. It is also the only public vertical episode whose
YouTube thumbnail set has no `shortsAspectRatio` entry. Check the Shorts shelf in Studio.

### Watch item
Nov 3 and Nov 5 are the only days with two uploads. Eps 6, 7, 8 and the long-form all
underperformed. Weak evidence (Oct 30 had two and Ep 2 won), but don't double up.

## Nov 9, 2026 (first pass, 11 videos, 22 subs, 6.4k views)
- 85% of views come from the Shorts feed (5.4k of 6.3k in 14 days); search is 2.5%.
- Results are bimodal: hits cluster at 1.25k-1.48k, everything else is 67-392.
- Retention: hits keep ~90% of viewers through the first 20%; Ep 7 fell to 59% by 20%.
  Every video has a cliff at 15-25% (~5-7s) = right after the hook.
- Subs: ~0.35% of views convert. Ep 1 (looped, 93% avg viewed) shows the loop works.
- Duds were time-locked/niche or vague; hits were universal myth/"can you actually" questions.
- TODO each episode: Studio > Content > the Short > Reach > "Viewed vs swiped away" (not in
  the API). Under ~70% viewed = hook problem.

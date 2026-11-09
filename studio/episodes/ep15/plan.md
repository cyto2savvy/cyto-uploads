# Ep 15 plan: "Can exercise actually lower your cancer risk?" (IDEA chat, Nov 9, 2026)
Status: SCRIPTED, awaiting Utsha's OK. Nothing built, 0 credits spent. Claims and sources: `claims.md`. Build spec: `episode.json` (make_episode.py schema).

## Why this topic
- Universal "can you actually" body question, the pattern of the hits (Eps 2, 3, 5, 9). Not time-locked.
- One true, surprising number in the first 4 s (28%), from a Canadian-led NEJM randomized trial (home-team pride).
- Two NEW PubMed sources, not used in any earlier Short.
- Toronto this week: Royal Winter Fair (Nov 6-15), "Run Terry Run" doc at Hot Docs (Nov 7-14), Leafs Nov 10/12/14. The topic is evergreen, so Toronto lives in the payoff (TTC, Bloor-Yonge). Terry Fox is NOT named or drawn.
- Suggested slot: Thu Nov 12, 6 PM ET (publish_at 2026-11-12T23:00:00Z). Manager confirms.

## Hook-first test (same pattern as Ep 14)
- Frame 0: Cyto already talking (voice at ~0.02 s), huge claim on screen (COMEBACK RISK -28%), two bars (80 vs 74) half drawn, cup in hand with steam. No fade-in.
- Re-hook at 4 s ("And it's not just for patients, fam."), catchphrase AFTER the hook (6-9 s).
- New visual every ~2 s in the first 8 s. Quiet follow chip around 18-24 s. Ends on a comment question.
- Loop: the last word is "because", so the loop reads "Comment it, because in a Canadian-led trial, exercise cut...". If the TTS "because" sounds cut off, drop the spoken word and keep it in the caption only. Last visual frame = frame 1 state.
- Compare "Stayed to watch" with the 50% baseline (target >= 60%).

## Script (~94 words, ~33 s; captions keep the real spelling)
1. [0-4 HOOK, shock] In a Canadian-led trial, exercise cut colon cancer's comeback risk by about 28 percent.
2. [4-6 re-hook, skeptic] And it's not just for patients, fam.
3. [6-9 catchphrase, chill] Yo, it's ya boy Cyto, live from the 6ix... inside your body.
4. [9-18 trial figure] Colon cancer survivors did a three-year exercise plan after chemo. Five years on, 80 percent were disease-free, versus 74 percent with pamphlets.
5. [18-26 zoom out] Across 1.44 million adults, the most active had lower risk of 13 cancers. Linked, not proven, styll.
6. [26-31 Toronto payoff] So hop off the TTC early and walk. Say less.
7. [31-35 outro] Not medical advice. How much do you move a week? Comment it, because

Voice check: slang = fam, styll, say less (3). Toronto reference = TTC. No drinking/high slang, no brands, no real-person quotes. The catchphrase is intact.

## Scene plan and Toronto backgrounds (Nov 2 rule, City of Toronto only)
| Scene | Time | Visual | Toronto background |
|---|---|---|---|
| 0 hook | 0-4 | Huge "-28%" stamp + 2 bars half drawn; Cyto jogs in place with the cup | cut-out waterfront trail at dawn, skyline + CN Tower silhouette |
| 1 re-hook + catchphrase | 4-9 | "NOT JUST PATIENTS?"; push-in only | same set, no new props |
| 2 trial | 9-18 | Figure card: bars EXERCISE 80% vs PAMPHLETS 74% (colon cancer, after chemo); Cyto points | hospital row cut-out (art.univ_ave) behind the card |
| 3 zoom out | 18-26 | 1.44M ADULTS counter; 13 organ icons light up one by one; chip LINKED, NOT PROVEN; shrug on "not proven" | soft navy/teal field; small Easter egg: raccoon on a bin in the corner |
| 4 payoff | 26-31 | Cyto steps off a TTC streetcar one stop early and walks with the cup, steam trailing | streetcar stop + Bloor-Yonge platform sign (art.streetcar / art.subway_platform) |
| 5 outro | 31-35 | HOW MUCH DO YOU MOVE A WEEK?; sources card "Courneya 2025 · Moore 2016" (>= 34 px) | same waterfront trail + skyline as frame 1 (loop) |

## Look (Canon v2, non-negotiable)
- Outfit: toque + hoodie, flush with the body and clipped to the outline (`fit: hoodie`).
- Cup: generic coffee cup ALWAYS in his mitten hand, steam rising. Never set down. Cup + hand = one rigid group, no twitch.
- Style pick: Street Cyto (shoulder-bounce on the beat, point on the bars, shrug on "not proven").
- Face moves all video, pupils parallel, no fingers. Run canon 29/29, rig 15/15, layout_check 0 FAIL, 1-fps contact sheet from the real mp4 before showing Utsha.
- Safe zone x 60-940 / y 200-1480, nothing within 40 px of an edge, IG/FB top 220 / bottom 350 px clear, one big text at a time.

## Title and thumbnails
- Title (45 chars): Can Exercise Actually Lower Your Cancer Risk?
- Thumbnail A: "GYM VS / CANCER?" Reads fastest at 160 px.
- Thumbnail B (STRONGER): "CANCER'S / COMEBACK -28%". Specific number plus a curiosity gap. "Comeback" keeps it accurate to the trial.
- Both: shock face, huge Cyto, real topic background (free Unsplash runner on a city trail at dawn is the $0 route; fallback `--scene toronto`), sizes 1280x720 and 1080x1920.

## Costs (build chat asks Utsha first)
- Idea stage: $0.
- ElevenLabs voice: ~610 chars, ~700 credits per take (estimate_only first, never retry a generation).
- AI thumbnail image: ~820 credits (the free Unsplash route is recommended instead). No vidIQ credits.

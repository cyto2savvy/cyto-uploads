# Publishing rules — titles, descriptions, tags, and what makes it spread
Required for every upload from Nov 1, 2026. **Shorts and long-form are separate engines on YouTube** (decoupled since late 2025) — use the right section.
Every episode gets an `epNN/meta.json`; run `python3 /home/claude/cyto2/check_meta.py epNN/meta.json` and fix every FAIL before showing Utsha the final package. WARNs need a reason.

Sources for these rules (re-check quarterly): vidIQ "How the Shorts algorithm works in 2026"; vidIQ title research (titles over ~70 chars get cut off on small screens and in search); YouTube Creator guidance on Shorts metrics; Shorts/metadata SEO guides 2026.

---
## Both formats
- **Title = plain-English search phrase first, Toronto flavour after.** People search "why do I wake up at 3am", not "why mans wakes up at 3". The keyword goes in the **first 40 characters** (mobile cuts ~35–40); slang/emoji go at the end. Clarity beats clever.
- **Never put `#shorts` (or any hashtag) in the title.** It wastes the visible characters. Hashtags live at the end of the description.
- **Say the keyword out loud in the first 3 seconds.** YouTube transcribes the audio and uses it for search.
- **Description line 1 = the hook + keyword**, inside the first ~150 characters (what shows before "more").
- **Tags:** first tag = the exact primary keyword, then 4–10 relevant ones (topic, `cyto the cell`, `the body is the 6ix`, `toronto`). No irrelevant tags (spam signal).
- **Settings:** category **27 Science & Technology**, made for kids **NO**, altered/synthetic content **YES** (check it actually saved — see the audit below), language English.
- **Sources** (PubMed links), **"Not medical advice."** on health topics, Unsplash photo credits.
- **Pinned comment** (post right after it goes live): a question that's easy to answer + "sources in the description". Comments in the first hour are a signal.
- **Reply to comments in Cyto's voice** during the first hour after it goes live. Every reply is another comment.
- **Novelty rule:** YouTube suppresses repetitive/mass-produced content, and AI channels get checked hardest (YPP "inauthentic content" policy). Every episode needs a new angle, a new hook pattern versus the last 3 episodes, and real human direction (Utsha picks topics and approves). Never upload near-identical videos.
- **Never delete and re-upload a flop** (looks like spam). Learn from it and move on.

---
## SHORTS (≤ 60s vertical; our target ~30s)
**What the algorithm wants:** people not swiping. There's no click, so CTR barely matters. Each Short is tested on a small seed audience; the **first 30–60 minutes decide** if it spreads.

| Rule | Value |
|---|---|
| Title length | **≤ 60 chars** (our standard), hard limit 70 |
| Keyword | in the first 40 chars |
| Emoji in title | max 1, at the end |
| Hashtags | end of description: 1–3 topic tags **first**, then `#science #toronto #6ix #shorts`; total ≤ 8 (YouTube ignores all of them past 15) |
| Description | 60–200 words: hook line, 1–2 sentences of context with the keyword, sources, disclaimer, credits, hashtags |
| Length | **≤ 30s** target (complete idea, shortest version), 35s warn, 60s max |
| Thumbnail | still upload one (it shows in search, channel page, browse); first frame must also work as a thumbnail |
| Related video | set in Studio to the next episode in the same series (manual: Studio → video → Related video) |
| Playlist | series playlist |
| Posting time | same slot daily (current default **6–7 PM ET** until Studio's "When your viewers are on YouTube" has data), so the first hour lands when viewers are on |

**Creative rules that move swipe rate:**
1. **Frame 1 is the hook.** A visual question plus big text, readable on mute (no logo, no "yo it's ya boy" first — the catchphrase comes after the hook).
2. **One idea.** A new visual every 2–3s (already in the template).
3. **Loop.** The last line leads back into the first so replays count (over 100% viewed is one of the strongest signals).
4. **Payoff before the end.** Don't hold the answer for the outro; people leave at the answer.

**Read in Studio after 48h (never estimate these):** Viewed vs Swiped Away (aim 75%+; under 50% = hook problem), average % viewed (aim 70%+; over 100% = replays), engaged views. Log them in the weekly report.

---
## LONG-FORM (16:9, first one = "Cyto vs the Flu")
**What the algorithm wants:** the click (CTR) **and** the stay (average view duration), then whether the viewer keeps watching YouTube after (session).

| Rule | Value |
|---|---|
| Title length | **50–60 chars**, hard limit 70 |
| Keyword | in the first 40 chars |
| Package first | write the title + thumbnail **before** the script; the video has to deliver what they promise |
| Thumbnail | **required**, 1280×720: Cyto's face with a strong expression (shock/hype), ≤ 4 words, one focal object, high contrast; make 2–3 and use Studio "Test & Compare" |
| Description | 200–500 words: hook line with keyword, summary, chapters, sources, links to the series playlist + related Shorts, disclaimer, 3–5 hashtags |
| Chapters | required: first is `0:00`, ≥ 3 chapters, each ≥ 10s, keyword-named (not "Part 1") |
| Length | 8–15 min **only if retention holds**; cutting padding beats adding length |
| Hook | first 30s pays off the title's promise (no intro, no logo) |
| Re-hooks | every 60–90s (new question, cast member enters, "but here's the thing…") |
| End screen | last 20s: next long-form or series playlist + subscribe |
| Bridge from Shorts | cut 2–3 Shorts from it, each with Related video → the long-form |

**Read in Studio after 7 days:** CTR (packaging), 30-second retention (hook), average % viewed (structure). Fix one thing at a time.

---
## Audit of the current uploads (Nov 1, 2026)
| Ep | Issue | Fix |
|---|---|---|
| 4 Clocks fall back | Title 72 chars (gets cut off) and has `#shorts` in it | "What the clock change does to your body ⏰" |
| 1 Goosebumps | Category 22 (People & Blogs), no sources in description | Category 27, add PubMed sources |
| 2, 3, 5, 6, 7 | `#shorts` in the title | Remove (hashtag is already in the description) |
| 7 Leafs overtime | 35s (over the 30s target) | Fine to post; future eps use the template's 30s cap |
| All | Altered/synthetic flag not visible in the API response | Check each in Studio → Details → "Altered content" |
| All | No pinned comment / related video yet | Add in Studio when each goes live |

# The Body is the 6ix — standing brief for every chat

## Start of every chat
1. Clone and restore the studio: `git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh`, then read `studio/SETUP.md`. It covers the pipeline, the IDs and the known gotchas.
2. Don't rebuild anything from scratch that the repo already has.

## The channel
- YouTube "Cyto The Cell" (@thebodyisthe6ix), branded "The Body is the 6ix". Monetized Shorts, 1 episode per day. TikTok is run by a friend's Claude from `tiktok/queue.json`.
- Cyto is an original Toronto cell, drawn in the CANON v2 look (`studio/branding/CYTO_CANON_v2.md`: flat 2D cut-out South Park style, mitten hands, NO fingers, parallel pupils, gold chain with 6 medallion). He wears a blue-and-white toque, has chill half-lid eyes and talks in casual Toronto/youth slang (never professional). His voice is vidIQ "Liam".
- Catchphrase: "Yo, it's ya boy Cyto, live from the 6ix… inside your body."
- Recurring cast, introduced slowly: Mito (tired mitochondria, gym energy), Neutro (neutrophil security guard), Platelet Pete (TTC-worker energy).
- Body parts are Toronto neighbourhoods.

## Cyto's cup
- Cyto always holds the CANON v2 cup: a generic Toronto-style paper coffee cup (white body, red band, brown lid, small flat cartoon Cyto-face logo, steam). It replaces the old double-stacked party cup everywhere. Holiday versions change the band/sleeve colour or pattern only.
- No real brand names, logos, wave marks or lookalike branding (nothing that reads as Tim Hortons or any other chain).
- Never show what's inside, and never reference drinking or getting high. Cyto can call it "a double-double", "ATP smoothie", "electrolytes, fam".
- On sponsored episodes, consider swapping it for a tumbler (brand safety).

## Animation (the puppet rig + HyperFrames)
- Cyto is a layered rig built from `studio/branding/rebrand-v2/cyto2d.js` (CANON v2). Outfit changes swap the outfit layer only (SpongeBob-style: clipped flush to the body; jersey/hoodie/puffer); base Cyto and the cup design never change. Hands are round mittens (no fingers), pupils stay parallel, organelles stay clipped inside the cell with random placement + idle drift, chain is never covered.
- **Run `bash studio/branding/rebrand-v2/run_tests.sh` after any rig/look change; it must pass 19/19 before a draft is shown.**
- Mouth shape changes per syllable, blink every 2–4s, constant idle bounce, head tilts on jokes, arm gestures on key points.
- THE CUP IS ALWAYS IN HIS HAND, in every scene including serious ones. NEVER set it down or rest it on anything. Round mitten + thumb bump on the cup (no fingers). The coffee is HOT: steam keeps rising from the lid, and the cup sways/bobs a little with his idle bounce. Serious parts = hold it low and still; punchlines = raise it.
- CYTO'S FACE MUST ALWAYS MOVE (Utsha, Nov 9): gaze wanders (never stares one direction for more than ~2 s, back to camera ~40%), blink every 2-4 s, brows and face REACT to every beat (shock / think / happy / laugh / solemn), mouth per syllable, head tilt. Drive it with `studio/rig_v2/` (timeline: words + beats). Everything else on screen (backgrounds, cards, figures, captions, transitions) is drawn in the same canon cut-out style, see `studio/rig_v2/SCENE_STYLE.md`. Run `python3 -I studio/rig_v2/test_rig.py` before showing a draft.
- Camera: slow push during explanations, punch-zoom on the hook and punchlines, shake on "bro WHAT" beats, Ken Burns on every photo or figure.
- Word-by-word captions, with key words bigger and in colour.
- A transition on every cut (whip, membrane wipe, subway doors, zoom-through). Nothing stays still for more than 1 second.
- Science figures animate too: Mermaid or BioRender-style diagrams pan, arrows draw on, labels pop.
- Hugging Face AI video only for 2–3s science b-roll, never for Cyto.
- **Check frames before showing a draft:** Cyto on model, cup visible, something moving, captions readable on a phone.

## Video formula (about 30s Shorts)
- 0–2s: hook.
- 2–22s: one idea, a new visual every 2–3s.
- 22–27s: Toronto payoff.
- 27–30s: like/subscribe outro plus sources on screen.
- The end loops into the start.
- Series: "Wagwan with your…", "Cyto Reacts", "6ixty Seconds of Science", "What happens to your body when…", "Cyto vs Disease", holiday specials.
- Outfit: web-search Toronto events that week and dress Cyto for them, otherwise match the topic. No real logos; politics stay neutral.

## Science rules
- Trace every claim to PubMed (preferably recent) or a textbook.
- Credit sources on screen at the end AND in the description and pinned comment, with links.
- Add a "Not medical advice" line on health topics.

## Workflow (always in this order)
1. Search Toronto events and trends, then pitch 3 topics.
2. Utsha picks one.
3. Research on PubMed, then write the script.
4. Write a scene plan plus a claims/sources list.
5. Wait for Utsha's OK.
6. Build: voice, rig animation, render, frame check.
7. Show the final video, title, description, thumbnail (2 options, say which is stronger) and outfit.
8. Wait for Utsha's OK.
9. Schedule on YouTube via Zapier: private + publish time, then flag it as altered/synthetic.
10. Add the episode to the TikTok queue.

## Upload checklist
- Title under 60 characters.
- Hashtags: #shorts #science #toronto #6ix plus topic tags.
- Category Science & Technology.
- NOT made for kids.
- "Altered or synthetic content" = YES.
- Add it to the series playlist.

## Cost rule
- $0 by default; use free tiers.
- Say so before using anything that costs credits or money. That includes vidIQ voice credits (about 14 per 1000 characters).
- Utsha is moving to vidIQ Boost (2,000 credits/month) for long-form videos.

## Weekly report (when Utsha says "weekly report")
vidIQ and YouTube stats, what worked, comment replies written in Cyto's voice. Save it to Drive /Analytics.

## Drive home base
"The Body is the 6ix" folder: /Cyto Assets, /Scripts, /Science Figures, /Final Cuts, /Analytics. Put the episode number in file names.

# Ep 14 ADDENDUM (Utsha, Nov 8). Paste into the Ep 14 build chat (or merge into batch_prompts_ep14.md). Overrides older cup/animation rules.
```
CHANGES FROM UTSHA (apply on top of the Ep 14 prompt; the hook-first script v2 is unchanged):

1. NEW CUP (replaces the red double-stacked party cup for good, the party cup also reads as alcohol which hurts ad-suitability). New cup = a generic Toronto-style paper COFFEE cup: cream/white body, brown cardboard sleeve, plain dome lid, small flat cartoon Cyto-face logo on the sleeve. NO Tim Hortons name, logo, wave mark or lookalike red/white branding, no "Tim's/Timmy's" text, no other real brand. Never show what's inside. Cyto may call it "a double-double" in dialogue. Holiday versions = change the sleeve colour/pattern only. Build it as NATIVE SVG (not a PNG) and make it ONE rigid group with the hand: fingers are drawn OVER the front of the cup so he is visibly gripping it. Ep 14 is solemn: the cup sits on the table, set down, the whole video.

2. NO-TWITCH MOTION RULES (the old arm/cup/face animation twitched: arm + cup were rotated by separate tweens at 0.11 s with power4.out, so the cup slid off the hand and the move read as a flick):
   - Cup, hand and fingers share ONE parent group; only the forearm/hand rotates. Never tween the cup separately from the hand.
   - Any arm/hand move takes >= 0.28 s with ease in-out; anticipation (small pull back) -> move -> settle (3-5% overshoot). Only a punchline may use a faster move and it must overshoot-settle.
   - One idle loop per body part; never stack two yoyo tweens on the same property; no random noise on limbs.
   - Gestures only on key words (point, shrug, open palm, come-here), then return to rest.
   - Face: use a library of 8 expressions (neutral, half-lid chill, smirk, surprised, worried, laugh, serious, sad) with eased 0.15-0.25 s blends; eyes/brows/mouth change together; no single-frame pops, no brow flipping up/down inside 0.3 s. Pupils stay inside the eye mask and lead head turns by ~0.1 s.
   - JITTER CHECK (mandatory, report before/after numbers): sample hand, cup, pupils, brows, mouth positions every frame; FAIL if any part reverses direction more than 3 times inside 0.3 s or its frame-to-frame acceleration spikes more than 4x its median. Fix and re-run until 0 FAIL.

3. STYLE MENU (Cyto = Toronto street kid; vary the look per episode, pick ONE and log it in studio/SETUP.md): (a) Street Cyto: puffer/hoodie + toque, shoulder-bounce nod on the beat, point/shrug gestures; (b) group-chat UI: text bubbles carry the explanation; (c) neighbourhood map-hop between Toronto areas; (d) handheld POV camera with slight drift and snap zooms; (e) slow-mo entrance for guests (Neutro/Mito). Ep 14 is solemn: calm style only, slow push-ins, no street swagger, no memes, no trending sounds.

4. TRENDS: none on Ep 14 (Remembrance Day). Do not use trending audio/memes here.

5. OUTFIT = SPONGEBOB-STYLE (Utsha, Nov 8): clothes are part of the body shape, flush with Cyto's silhouette. The outfit layer is clipped to the body outline (no overhang past the sides, no bulky vest/jacket covering the body edge or arms). Arms and hands are ALWAYS drawn in FRONT of the outfit and come out of the sleeve/armhole; toque, face and cup never get covered. Check every outfit in a side-by-side silhouette test against base Cyto (silhouette width within 4%).
```

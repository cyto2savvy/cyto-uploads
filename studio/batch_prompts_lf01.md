# LF01 build prompt (long-form, ~7:15, LANDSCAPE 16:9). ONE NEW cloud session. Budget: target $30-40 of the $75; HARD STOP at $45.

```
You're building ONE long-form Cyto The Cell YouTube video: LF01 "What Happens When You Quit Smoking Weed & Tobacco". Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET: finish before then. This is NOT a Short. It is 1920x1080 landscape, about 7:15, and the quality bar is Ep 13.

SETUP
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read ONLY studio/SETUP.md sections "Ep 9 lessons", "Ep 11 lessons", "Ep 11 review", "Ep 12 lessons", "Ep 13 lessons", "Cup rule", "SOURCE RULE", "TORONTO BACKGROUND RULE", "MANDATORY AUTOMATIC CHECK", plus studio/episodes/lf01/script_v2_final_draft.md (the APPROVED script, chapters, retention design, sources; do not rewrite or swap). Don't read VOICE.md, PUBLISHING.md or BATCH.md.

AUDIO (already generated; do NOT regenerate)
3. Voice chunks (one per chapter) exist in ElevenLabs: see studio/episodes/lf01/audio_ids.md (manager fills this in before you start; if it's missing, STOP and tell Utsha). For each chunk, get the signed URL via creative_get_generations, add `name url` to audio/list.txt, push, wait for fetch-audio, read audio/status.txt. Then Scribe transcription (0 credits) -> word timing per chunk -> concatenate with 0.35s gaps -> voice.wav + timing.json. Captions use real spellings.

LANDSCAPE ADAPTATION (the rig/template are 1080x1920 vertical; this is the main risk)
4. Copy the Short template to hf/lf01/ and convert to 1920x1080: Cyto on the left third (large, on model, cup in FRONT of the hand), big content area on the right two-thirds for figures/diagrams/maps/charts. Keep the safe margin >=60px (nothing within 40px of any edge, as always). Re-run layout_check with the landscape size; if it assumes vertical, patch it (don't skip it). Do this as a SMALL test first: render 5s of the hook, view one frame, and only then build the rest.

BUILD IN CHAPTERS (this keeps cost and retries down)
5. Build each chapter as its own composition (Hook+Intro, Ch1..Ch7 per the script timestamps), render each chapter separately, then concat with ffmpeg and cross-check the audio sync. A bug then costs one chapter, not the whole video. Max TWO renders per chapter (draft + final); iterate on single frames.
6. Retention rules (these matter): something visibly changes at least every 3s (new visual, zoom, label pop, cut) and a transition on every cut; no static talking-head stretch; hook visual is a countdown clock (20 min); chapter title cards pop for 1.5s at each chapter start; a mid-video "Week four is where it flips" punch moment; arrows draw on, labels pop, charts animate; the final line loops visually back to the hook frame. Ken Burns on every figure.
7. Visuals per chapter: Ch1 lungs diagram + Neutro (neutrophil security guard, reuse studio/rig/neutro) patrolling, split card "tobacco leaf = nicotine" (flat icon only); Ch2 animated heart-rate line + CO gauge + clock; Ch3 brain with receptor-reset diagram; Ch4 calendar flipping to week 4 + cilia sweeping animation; Ch5 bar chart of years gained (25-34: ~10, 35-44: ~9, 45-54: ~6) plus a 1-year/15-year heart-risk timeline; Ch6 five tip cards (each with an icon), a text-message bubble UI (generic, no real app), a pharmacy cross icon; Ch7 Toronto-neighbourhood map tour (Lungs = Don Valley, Heart = downtown, Brain = U of T) then the sources cards.
8. Toronto backgrounds (City of Toronto only: Scarborough Bluffs, Kensington, a 501 streetcar silhouette, Don Valley, downtown skyline, U of T; NO Brampton/Mississauga). Generic shapes, no real logos or brands.
9. HARD CONTENT RULES: NEVER depict smoking, joints, blunts, grabba being used, lighters, or smoke plumes from a person. No packs or branded products. The leaf/wrap appears only as a flat abstract icon on an explainer card. No stereotyping of any community. Cyto never jokes about being high; the cup is an "ATP smoothie". Supportive, non-preachy tone. Health topics: show "Not medical advice" at the start card and the end card.
10. Audio mix: voice on top; a quiet synthesized music bed; SFX on transitions and pops (ElevenLabs sfx once each ~17 credits, max ~150 credits, or free ffmpeg synth). No copyrighted music.

EFFICIENCY
E1. Plan the full build in big chunks before running anything. E2. Contact sheets (1 fps, small) per chapter plus at most 3 full-size frames in total per chapter. E3. layout_check `--step 0.5` while iterating, `--step 0.25` once at the end; fix every FAIL and safe-zone WARN. E4. Short status lines only. E5. After two failed attempts at anything, use the SVG/GSAP or ffmpeg fallback. E6. Report running cost after each chapter in studio/costs.md; if the running total passes $30 before Ch5 is done, simplify visuals (fewer new art pieces) rather than stopping. HARD STOP at $45: commit what exists and report.

QUALITY GATE
11. layout_check = 0 FAIL on every chapter and on the concat. On-screen sources: text >=34px, max 2 per screen, include ALL sources from the script's ON-SCREEN SOURCES list across 5-6 screens at the end, each shown >=2.5s. No invented numbers; every figure comes from the script. Pupils inside eyes; Cyto on model; cup visible and in front of the hand; Lotties verified in the real mp4.

PACKAGE
12. 2 thumbnails 1280x720 (countdown clock "20 MIN -> 1 YR", Cyto + Neutro peeking; max 3 words on image; say which is stronger), meta.json (title <=60 chars, 8-12 tags with the exact keyword first, description with chapters/timestamps, ALL source DOI links, "Not medical advice", Smokers' Helpline 1-877-513-5333 / text iQuit to 123456), captions.srt, pinned_comment.txt (sources + the question "what's the hardest part, the habit or the craving?"), check_meta.py and check_sources.py = OK, Append credits to studio/costs.md.
13. Commit studio/episodes/lf01/ + final mp4 + thumbnails + hf/lf01/ and push. STOP and post: the final video, title, description, thumbnails, layout_check result, the total cost, and the 3 things you're least sure about. Do NOT upload or schedule; the manager chat does that.

Upload target: Fri Nov 20 2026 (channel one-month anniversary). Keep it private until then.
```

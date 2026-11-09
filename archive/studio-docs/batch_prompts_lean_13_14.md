# LEAN build prompts for Eps 13 and 14 (Nov 2). Same quality as Ep 12, built to cost less and finish faster. One NEW cloud session each.

## Ep 13
```
You're building ONE Cyto The Cell YouTube Short: Ep 13 ("Meet Neutro: Your Flu Season Bouncer"). Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET. Earlier builds cost $8-10 and ran long, so follow the EFFICIENCY rules; target under $6 and about 60% of Ep 11's time.

SETUP (read only what's listed, skip the other docs)
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read ONLY: studio/SETUP.md sections "Ep 9 lessons", "Ep 11 lessons", "Ep 11 review", "Ep 12 lessons", "Cup rule", "SOURCE RULE", "TORONTO BACKGROUND RULE", "MANDATORY AUTOMATIC CHECK", plus studio/episodes/ep13/EP13_brief.md. The script, sources and Toronto background plan in the brief are APPROVED; don't rewrite or swap. Don't read VOICE.md, PUBLISHING.md or BATCH.md.

AUDIO (no drag-and-drop needed)
3. The approved read already exists in ElevenLabs: flow 9FCDlyMjCyXT9Z51HIp7, historyItemId MWhXiIm9et7oPfZc5w6E ("Cyto - Toronto (A)"). Follow SETUP "Ep 12 lessons": get its signed URL via creative_get_flow / creative_get_generations, add `name url` to audio/list.txt, push, wait for the fetch-audio workflow, read audio/status.txt. Then epN/raw.mp3 -> make_segs.py (Scribe word timing, 0 credits) -> build_voice2.py -> voice.wav + timing.json. Never regenerate the voice (credits). If the ElevenLabs connector isn't attached, ask Utsha to attach the mp3 and continue.
4. Captions use real spellings (ahlie/styll/6ix); the TTS spellings are only for the voice.

BUILD (reuse, don't reinvent)
5. Copy hf/template/build.py to hf/ep13/ (v2 layout + v3 rig). Reuse existing art.py pieces and Lotties before drawing anything new; only add new art that the brief needs. Cap 60s (aim 35-50s, match audio). Pill label 6IXTY SECONDS OF SCIENCE. Outfit per the brief. Cup: double-stacked red party cup with Cyto's face logo, ALWAYS drawn IN FRONT of his hand and body (cyto3.py is already fixed; verify), nothing inside shown.
6. Backgrounds per the brief's Toronto plan, scene by scene. City of Toronto only (Scarborough, Etobicoke, North York, East York, York, old Toronto OK; NO Brampton, Mississauga or other GTA cities). Generic shapes, no real logos/brands/people.
7. Proven upgrades (do them as you build, not as a second pass): word-timed captions and mouth shapes from Scribe; head tilts, arm gestures and cup raises on stressed words (cup down for serious lines); SFX on every transition and pop (ElevenLabs sfx once each, ~17 credits each, max ~100 credits, fetched via audio/list.txt, mixed under the voice per Ep 12 lessons, or free ffmpeg synth); a quiet synthesized music bed; overshoot easing, push-ins, arrows draw on, labels pop; a transition on every cut.

EFFICIENCY (this is what cut the cost)
E1. Plan the whole build.py in one go from the brief before running anything. Write it in big chunks, not many small edits.
E2. Max TWO full-quality renders: one draft, one final. Iterate on single-frame snapshots and short clips, not full renders.
E3. Review frames as ONE 1-fps contact sheet at small size (about 216px wide, 8 across) plus at most 3 full-size frames. Don't view every frame at full resolution.
E4. layout_check: use `--step 0.5` while iterating, `--step 0.25` once at the end. Fix every FAIL and every safe-zone WARN, then re-run once.
E5. No long explanations or recaps in the chat; short status lines only. Don't re-read files you already read.
E6. If something blocks you for more than two attempts (a blank Lottie, a flaky tool), switch to the SVG/GSAP or ffmpeg fallback immediately instead of retrying.

QUALITY GATE
8. `cd /home/claude/hf && python3 layout_check.py ep13 --brief studio/episodes/ep13/EP13_brief.md` = 0 FAIL, no invented scores/numbers. Nothing within 40px of an edge; on-screen sources card text >=34px and max 2 sources; hook has at most 3 moving things; figures fill their card; verify Lotties render in the real mp4. Pupils never leave the eyes; one big text at a time; loop frame = hook frame; cup visible and in front of the hand; Cyto on model.

PACKAGE
9. 2 thumbnails (say which is stronger; thumb.py needs an ABSOLUTE out_dir), meta.json (title <=60 chars, tags/hashtags from the brief, description with PubMed DOI links + "Not medical advice"), captions.srt, `python3 cyto2/check_meta.py` = 0 FAIL, `python3 studio/check_sources.py` = OK. Append all credits used to studio/costs.md.
10. Commit studio/episodes/ep13/ + final mp4 + thumbnails + hf/ep13/ and push. STOP and post: final video, title, description, thumbnails, outfit, the layout_check result, and the 3 things you're least sure about. Do NOT upload to YouTube or schedule; the manager chat does that.

Publish target for reference: Tue Nov 10 6:00 PM ET (UTC 2026-11-10T23:00:00Z).
EP 13 EXTRA: Neutro is a NEW cast member (neutrophil security guard: high-vis vest, earpiece, arms crossed, flat-ink style like Cyto, multi-lobed nucleus). Design him once as a vector like cyto3.py, save under studio/rig/neutro/, and show me his design frame in your first update.
```

## Ep 14
```
You're building ONE Cyto The Cell YouTube Short: Ep 14 ("What Two Minutes of Silence Does to Your Body"). Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET. Earlier builds cost $8-10 and ran long, so follow the EFFICIENCY rules; target under $6 and about 60% of Ep 11's time.

SETUP (read only what's listed, skip the other docs)
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read ONLY: studio/SETUP.md sections "Ep 9 lessons", "Ep 11 lessons", "Ep 11 review", "Ep 12 lessons", "Cup rule", "SOURCE RULE", "TORONTO BACKGROUND RULE", "MANDATORY AUTOMATIC CHECK", plus studio/episodes/ep14/EP14_brief.md. The script, sources and Toronto background plan in the brief are APPROVED; don't rewrite or swap. Don't read VOICE.md, PUBLISHING.md or BATCH.md.

AUDIO (no drag-and-drop needed)
3. The approved read already exists in ElevenLabs: flow 9FCDlyMjCyXT9Z51HIp7, historyItemId 27cH5XNH2G2IPP5iqHfS ("Cyto - Toronto (A)"). Follow SETUP "Ep 12 lessons": get its signed URL via creative_get_flow / creative_get_generations, add `name url` to audio/list.txt, push, wait for the fetch-audio workflow, read audio/status.txt. Then epN/raw.mp3 -> make_segs.py (Scribe word timing, 0 credits) -> build_voice2.py -> voice.wav + timing.json. Never regenerate the voice (credits). If the ElevenLabs connector isn't attached, ask Utsha to attach the mp3 and continue.
4. Captions use real spellings (ahlie/styll/6ix); the TTS spellings are only for the voice.

BUILD (reuse, don't reinvent)
5. Copy hf/template/build.py to hf/ep14/ (v2 layout + v3 rig). Reuse existing art.py pieces and Lotties before drawing anything new; only add new art that the brief needs. Cap 60s (aim 35-50s, match audio). Pill label 6IXTY SECONDS OF SCIENCE. Outfit per the brief. Cup: double-stacked red party cup with Cyto's face logo, ALWAYS drawn IN FRONT of his hand and body (cyto3.py is already fixed; verify), nothing inside shown.
6. Backgrounds per the brief's Toronto plan, scene by scene. City of Toronto only (Scarborough, Etobicoke, North York, East York, York, old Toronto OK; NO Brampton, Mississauga or other GTA cities). Generic shapes, no real logos/brands/people.
7. Proven upgrades (do them as you build, not as a second pass): word-timed captions and mouth shapes from Scribe; head tilts, arm gestures and cup raises on stressed words (cup down for serious lines); SFX on every transition and pop (ElevenLabs sfx once each, ~17 credits each, max ~100 credits, fetched via audio/list.txt, mixed under the voice per Ep 12 lessons, or free ffmpeg synth); a quiet synthesized music bed; overshoot easing, push-ins, arrows draw on, labels pop; a transition on every cut.

EFFICIENCY (this is what cut the cost)
E1. Plan the whole build.py in one go from the brief before running anything. Write it in big chunks, not many small edits.
E2. Max TWO full-quality renders: one draft, one final. Iterate on single-frame snapshots and short clips, not full renders.
E3. Review frames as ONE 1-fps contact sheet at small size (about 216px wide, 8 across) plus at most 3 full-size frames. Don't view every frame at full resolution.
E4. layout_check: use `--step 0.5` while iterating, `--step 0.25` once at the end. Fix every FAIL and every safe-zone WARN, then re-run once.
E5. No long explanations or recaps in the chat; short status lines only. Don't re-read files you already read.
E6. If something blocks you for more than two attempts (a blank Lottie, a flaky tool), switch to the SVG/GSAP or ffmpeg fallback immediately instead of retrying.

QUALITY GATE
8. `cd /home/claude/hf && python3 layout_check.py ep14 --brief studio/episodes/ep14/EP14_brief.md` = 0 FAIL, no invented scores/numbers. Nothing within 40px of an edge; on-screen sources card text >=34px and max 2 sources; hook has at most 3 moving things; figures fill their card; verify Lotties render in the real mp4. Pupils never leave the eyes; one big text at a time; loop frame = hook frame; cup visible and in front of the hand; Cyto on model.

PACKAGE
9. 2 thumbnails (say which is stronger; thumb.py needs an ABSOLUTE out_dir), meta.json (title <=60 chars, tags/hashtags from the brief, description with PubMed DOI links + "Not medical advice"), captions.srt, `python3 cyto2/check_meta.py` = 0 FAIL, `python3 studio/check_sources.py` = OK. Append all credits used to studio/costs.md.
10. Commit studio/episodes/ep14/ + final mp4 + thumbnails + hf/ep14/ and push. STOP and post: final video, title, description, thumbnails, outfit, the layout_check result, and the 3 things you're least sure about. Do NOT upload to YouTube or schedule; the manager chat does that.

Publish target for reference: Wed Nov 11 9:00 AM ET (UTC 2026-11-11T14:00:00Z).
EP 14 EXTRA: Remembrance Day. Respectful tone: no jokes, no hype expressions, slow push-ins and cross-fades only (no whip/shake/punch-zoom), cup set down the whole episode, plain poppy shape pin (no Legion logo/text). Verify the Toronto service location before naming it on screen; otherwise keep the silhouette generic.
```

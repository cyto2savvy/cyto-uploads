# Paste-in prompts for the cloud build sessions (one NEW session per episode)
Open a NEW Claude Code cloud session on `cyto2savvy/cyto-uploads` per episode (claude.ai/code), paste the prompt, attach that episode's ElevenLabs mp3. Cloud credits expire 2:59 AM ET Nov 5.

## Ep 10
```
You're building ONE Cyto The Cell YouTube Short: Ep 10 ("Leafs vs Habs: Your Hormones Are Playing Too"). Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET, so move fast.

SETUP
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read: studio/SETUP.md (incl. "Ep 9 lessons", "SOURCE RULE", "TORONTO BACKGROUND RULE"), studio/VOICE.md, studio/PUBLISHING.md, studio/BATCH.md, studio/episodes/ep10/EP10_brief.md. The script, sources and Toronto background plan in the brief are APPROVED. Don't rewrite the script or swap sources.

AUDIO
3. Utsha attaches the approved voice mp3 ("Cyto - Toronto (A)"). Save it as epN/raw.mp3 -> silencedetect -> segs.json -> build_voice2.py -> voice.wav + timing.json. Captions use the real spellings (ahlie/styll/6ix); the TTS spellings are only for the voice.
4. ElevenLabs is available to you if the connector is attached: you MAY regenerate the read ONLY if the attached audio is missing or flawed. Use voice_id MDpsT9lfiqWEMyN3A1bk, model eleven_v4, the text in studio/episodes/ep10/tts.txt, generations_count=1, run estimate_only first (about 1 credit per character, roughly 600), never re-call a generation to retry (double charge), max 1 regeneration. Append the credits to studio/costs.md. Note: the sandbox can't download elevenlabsusercontent.com audio (403), so a regenerated mp3 must be downloaded by Utsha and dragged into this chat; tell him to do that. Never use vidIQ credits.

BUILD
5. Copy hf/template/build.py to hf/ep10/ (v2 layout + v3 rig, never the old PNG rig). Hard cap 45s. Outfit/cup per the brief (double-stacked red party cup with Cyto's face logo, nothing inside shown). Lottie via lottie/list.txt as SETUP.md says (push, read lottie/status.txt). New animated science figure per scene, word-by-word captions with key words bigger/coloured, a transition on every cut, nothing still for more than 1s.
6. Backgrounds: follow the brief's "Toronto background plan" scene by scene. Toronto-specific or topic-specific only, never random filler. Toronto proper only (no Brampton/Mississauga/GTA suburbs). Generic shapes: no real logos, store names, brands or people.

QUALITY GATE (before showing anything)
7. Pupils never leave the eyes; ONE big text element on screen at a time; nothing overlapping; snapshot EVERY second and review a contact sheet; run the safe-area sheet (C.safe_sheet); loop frame = hook frame; cup visible; Cyto on model.

PACKAGE
8. 2 thumbnails (say which is stronger), meta.json (title <=60 chars, hashtags/tags from the brief, description with PubMed DOI links + "Not medical advice"), captions.srt, `python3 cyto2/check_meta.py` = 0 FAIL, `python3 studio/check_sources.py` = OK.
9. Commit studio/episodes/ep10/ + the final mp4 + thumbnails + hf/ep10/ and push to the repo. Then STOP and post: final video, title, description, both thumbnails, outfit. Do NOT upload to YouTube or schedule anything; the manager chat does that after Utsha approves.

Publish target for reference: Sat Nov 7 4:00 PM ET (UTC 2026-11-07T21:00:00Z).
```

## Ep 11
```
You're building ONE Cyto The Cell YouTube Short: Ep 11 ("Is Your Diwali Food Coma Actually the Sweets?"). Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET, so move fast.

SETUP
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read: studio/SETUP.md (incl. "Ep 9 lessons", "SOURCE RULE", "TORONTO BACKGROUND RULE"), studio/VOICE.md, studio/PUBLISHING.md, studio/BATCH.md, studio/episodes/ep11/EP11_brief.md. The script, sources and Toronto background plan in the brief are APPROVED. Don't rewrite the script or swap sources.

AUDIO
3. Utsha attaches the approved voice mp3 ("Cyto - Toronto (A)"). Save it as epN/raw.mp3 -> silencedetect -> segs.json -> build_voice2.py -> voice.wav + timing.json. Captions use the real spellings (ahlie/styll/6ix); the TTS spellings are only for the voice.
4. ElevenLabs is available to you if the connector is attached: you MAY regenerate the read ONLY if the attached audio is missing or flawed. Use voice_id MDpsT9lfiqWEMyN3A1bk, model eleven_v4, the text in studio/episodes/ep11/tts.txt, generations_count=1, run estimate_only first (about 1 credit per character, roughly 600), never re-call a generation to retry (double charge), max 1 regeneration. Append the credits to studio/costs.md. Note: the sandbox can't download elevenlabsusercontent.com audio (403), so a regenerated mp3 must be downloaded by Utsha and dragged into this chat; tell him to do that. Never use vidIQ credits.

BUILD
5. Copy hf/template/build.py to hf/ep11/ (v2 layout + v3 rig, never the old PNG rig). Hard cap 45s. Outfit/cup per the brief (double-stacked red party cup with Cyto's face logo, nothing inside shown). Lottie via lottie/list.txt as SETUP.md says (push, read lottie/status.txt). New animated science figure per scene, word-by-word captions with key words bigger/coloured, a transition on every cut, nothing still for more than 1s.
6. Backgrounds: follow the brief's "Toronto background plan" scene by scene. Toronto-specific or topic-specific only, never random filler. Toronto proper only (no Brampton/Mississauga/GTA suburbs). Generic shapes: no real logos, store names, brands or people.

QUALITY GATE (before showing anything)
7. Pupils never leave the eyes; ONE big text element on screen at a time; nothing overlapping; snapshot EVERY second and review a contact sheet; run the safe-area sheet (C.safe_sheet); loop frame = hook frame; cup visible; Cyto on model.

PACKAGE
8. 2 thumbnails (say which is stronger), meta.json (title <=60 chars, hashtags/tags from the brief, description with PubMed DOI links + "Not medical advice"), captions.srt, `python3 cyto2/check_meta.py` = 0 FAIL, `python3 studio/check_sources.py` = OK.
9. Commit studio/episodes/ep11/ + the final mp4 + thumbnails + hf/ep11/ and push to the repo. Then STOP and post: final video, title, description, both thumbnails, outfit. Do NOT upload to YouTube or schedule anything; the manager chat does that after Utsha approves.

Publish target for reference: Sun Nov 8 3:00 PM ET (UTC 2026-11-08T20:00:00Z).
EP 11 EXTRA: SCARBOROUGH ONLY. Nothing outside Toronto, and no Gerrard India Bazaar, Brampton, Mississauga or Etobicoke places.
```

## Ep 12
```
You're building ONE Cyto The Cell YouTube Short: Ep 12 ("Movember: Does Checking Yourself Save Lives?"). Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET, so move fast.

SETUP
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read: studio/SETUP.md (incl. "Ep 9 lessons", "SOURCE RULE", "TORONTO BACKGROUND RULE"), studio/VOICE.md, studio/PUBLISHING.md, studio/BATCH.md, studio/episodes/ep12/EP12_brief.md. The script, sources and Toronto background plan in the brief are APPROVED. Don't rewrite the script or swap sources.

AUDIO
3. Utsha attaches the approved voice mp3 ("Cyto - Toronto (A)"). Save it as epN/raw.mp3 -> silencedetect -> segs.json -> build_voice2.py -> voice.wav + timing.json. Captions use the real spellings (ahlie/styll/6ix); the TTS spellings are only for the voice.
4. ElevenLabs is available to you if the connector is attached: you MAY regenerate the read ONLY if the attached audio is missing or flawed. Use voice_id MDpsT9lfiqWEMyN3A1bk, model eleven_v4, the text in studio/episodes/ep12/tts.txt, generations_count=1, run estimate_only first (about 1 credit per character, roughly 600), never re-call a generation to retry (double charge), max 1 regeneration. Append the credits to studio/costs.md. Note: the sandbox can't download elevenlabsusercontent.com audio (403), so a regenerated mp3 must be downloaded by Utsha and dragged into this chat; tell him to do that. Never use vidIQ credits.

BUILD
5. Copy hf/template/build.py to hf/ep12/ (v2 layout + v3 rig, never the old PNG rig). Hard cap 45s. Outfit/cup per the brief (double-stacked red party cup with Cyto's face logo, nothing inside shown). Lottie via lottie/list.txt as SETUP.md says (push, read lottie/status.txt). New animated science figure per scene, word-by-word captions with key words bigger/coloured, a transition on every cut, nothing still for more than 1s.
6. Backgrounds: follow the brief's "Toronto background plan" scene by scene. Toronto-specific or topic-specific only, never random filler. Toronto proper only (no Brampton/Mississauga/GTA suburbs). Generic shapes: no real logos, store names, brands or people.

QUALITY GATE (before showing anything)
7. Pupils never leave the eyes; ONE big text element on screen at a time; nothing overlapping; snapshot EVERY second and review a contact sheet; run the safe-area sheet (C.safe_sheet); loop frame = hook frame; cup visible; Cyto on model.

PACKAGE
8. 2 thumbnails (say which is stronger), meta.json (title <=60 chars, hashtags/tags from the brief, description with PubMed DOI links + "Not medical advice"), captions.srt, `python3 cyto2/check_meta.py` = 0 FAIL, `python3 studio/check_sources.py` = OK.
9. Commit studio/episodes/ep12/ + the final mp4 + thumbnails + hf/ep12/ and push to the repo. Then STOP and post: final video, title, description, both thumbnails, outfit. Do NOT upload to YouTube or schedule anything; the manager chat does that after Utsha approves.

Publish target for reference: Mon Nov 9 6:00 PM ET (UTC 2026-11-09T23:00:00Z).
```

## Ep 13
```
You're building ONE Cyto The Cell YouTube Short: Ep 13 ("Meet Neutro: Your Flu Season Bouncer"). Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET, so move fast.

SETUP
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read: studio/SETUP.md (incl. "Ep 9 lessons", "SOURCE RULE", "TORONTO BACKGROUND RULE"), studio/VOICE.md, studio/PUBLISHING.md, studio/BATCH.md, studio/episodes/ep13/EP13_brief.md. The script, sources and Toronto background plan in the brief are APPROVED. Don't rewrite the script or swap sources.

AUDIO
3. Utsha attaches the approved voice mp3 ("Cyto - Toronto (A)"). Save it as epN/raw.mp3 -> silencedetect -> segs.json -> build_voice2.py -> voice.wav + timing.json. Captions use the real spellings (ahlie/styll/6ix); the TTS spellings are only for the voice.
4. ElevenLabs is available to you if the connector is attached: you MAY regenerate the read ONLY if the attached audio is missing or flawed. Use voice_id MDpsT9lfiqWEMyN3A1bk, model eleven_v4, the text in studio/episodes/ep13/tts.txt, generations_count=1, run estimate_only first (about 1 credit per character, roughly 600), never re-call a generation to retry (double charge), max 1 regeneration. Append the credits to studio/costs.md. Note: the sandbox can't download elevenlabsusercontent.com audio (403), so a regenerated mp3 must be downloaded by Utsha and dragged into this chat; tell him to do that. Never use vidIQ credits.

BUILD
5. Copy hf/template/build.py to hf/ep13/ (v2 layout + v3 rig, never the old PNG rig). Hard cap 45s. Outfit/cup per the brief (double-stacked red party cup with Cyto's face logo, nothing inside shown). Lottie via lottie/list.txt as SETUP.md says (push, read lottie/status.txt). New animated science figure per scene, word-by-word captions with key words bigger/coloured, a transition on every cut, nothing still for more than 1s.
6. Backgrounds: follow the brief's "Toronto background plan" scene by scene. Toronto-specific or topic-specific only, never random filler. Toronto proper only (no Brampton/Mississauga/GTA suburbs). Generic shapes: no real logos, store names, brands or people.

QUALITY GATE (before showing anything)
7. Pupils never leave the eyes; ONE big text element on screen at a time; nothing overlapping; snapshot EVERY second and review a contact sheet; run the safe-area sheet (C.safe_sheet); loop frame = hook frame; cup visible; Cyto on model.

PACKAGE
8. 2 thumbnails (say which is stronger), meta.json (title <=60 chars, hashtags/tags from the brief, description with PubMed DOI links + "Not medical advice"), captions.srt, `python3 cyto2/check_meta.py` = 0 FAIL, `python3 studio/check_sources.py` = OK.
9. Commit studio/episodes/ep13/ + the final mp4 + thumbnails + hf/ep13/ and push to the repo. Then STOP and post: final video, title, description, both thumbnails, outfit. Do NOT upload to YouTube or schedule anything; the manager chat does that after Utsha approves.

Publish target for reference: Tue Nov 10 6:00 PM ET (UTC 2026-11-10T23:00:00Z).
EP 13 EXTRA: Neutro is a NEW cast member (neutrophil security guard: high-vis vest, earpiece, arms crossed, flat-ink style like Cyto, multi-lobed nucleus). Design him once as a vector like cyto3.py, save under studio/rig/neutro/, and show me his design frame in your first update.
```

## Ep 14
```
You're building ONE Cyto The Cell YouTube Short: Ep 14 ("What Two Minutes of Silence Does to Your Body"). Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET, so move fast.

SETUP
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read: studio/SETUP.md (incl. "Ep 9 lessons", "SOURCE RULE", "TORONTO BACKGROUND RULE"), studio/VOICE.md, studio/PUBLISHING.md, studio/BATCH.md, studio/episodes/ep14/EP14_brief.md. The script, sources and Toronto background plan in the brief are APPROVED. Don't rewrite the script or swap sources.

AUDIO
3. Utsha attaches the approved voice mp3 ("Cyto - Toronto (A)"). Save it as epN/raw.mp3 -> silencedetect -> segs.json -> build_voice2.py -> voice.wav + timing.json. Captions use the real spellings (ahlie/styll/6ix); the TTS spellings are only for the voice.
4. ElevenLabs is available to you if the connector is attached: you MAY regenerate the read ONLY if the attached audio is missing or flawed. Use voice_id MDpsT9lfiqWEMyN3A1bk, model eleven_v4, the text in studio/episodes/ep14/tts.txt, generations_count=1, run estimate_only first (about 1 credit per character, roughly 600), never re-call a generation to retry (double charge), max 1 regeneration. Append the credits to studio/costs.md. Note: the sandbox can't download elevenlabsusercontent.com audio (403), so a regenerated mp3 must be downloaded by Utsha and dragged into this chat; tell him to do that. Never use vidIQ credits.

BUILD
5. Copy hf/template/build.py to hf/ep14/ (v2 layout + v3 rig, never the old PNG rig). Hard cap 45s. Outfit/cup per the brief (double-stacked red party cup with Cyto's face logo, nothing inside shown). Lottie via lottie/list.txt as SETUP.md says (push, read lottie/status.txt). New animated science figure per scene, word-by-word captions with key words bigger/coloured, a transition on every cut, nothing still for more than 1s.
6. Backgrounds: follow the brief's "Toronto background plan" scene by scene. Toronto-specific or topic-specific only, never random filler. Toronto proper only (no Brampton/Mississauga/GTA suburbs). Generic shapes: no real logos, store names, brands or people.

QUALITY GATE (before showing anything)
7. Pupils never leave the eyes; ONE big text element on screen at a time; nothing overlapping; snapshot EVERY second and review a contact sheet; run the safe-area sheet (C.safe_sheet); loop frame = hook frame; cup visible; Cyto on model.

PACKAGE
8. 2 thumbnails (say which is stronger), meta.json (title <=60 chars, hashtags/tags from the brief, description with PubMed DOI links + "Not medical advice"), captions.srt, `python3 cyto2/check_meta.py` = 0 FAIL, `python3 studio/check_sources.py` = OK.
9. Commit studio/episodes/ep14/ + the final mp4 + thumbnails + hf/ep14/ and push to the repo. Then STOP and post: final video, title, description, both thumbnails, outfit. Do NOT upload to YouTube or schedule anything; the manager chat does that after Utsha approves.

Publish target for reference: Wed Nov 11 9:00 AM ET (UTC 2026-11-11T14:00:00Z).
EP 14 EXTRA: Remembrance Day. Respectful tone: no jokes, no hype expressions, slow push-ins and cross-fades only (no whip/shake/punch-zoom), cup set down the whole episode, plain poppy shape pin (no Legion logo/text). Verify the Toronto service location before naming it on screen; otherwise keep the silhouette generic.
```


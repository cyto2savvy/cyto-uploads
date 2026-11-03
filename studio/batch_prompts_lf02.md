# LF02 build prompt — "What Stress Does to Your Body (December Edition)", ~5:30, 1920x1080. ONE NEW cloud session. Target $22-28, HARD STOP $32.

```
You're building ONE long-form Cyto The Cell YouTube video: LF02 "What Stress Does to Your Body (December Edition)". Work autonomously, no questions unless truly blocked. Cloud credits expire Nov 5 2:59 AM ET: finish before then. 1920x1080 landscape, about 5:30.

THIS IS A NEW FORMAT. Utsha's friends said LF01 felt like "an AI bot explaining an infographic". LF02 must feel like a cartoon EPISODE: characters acting, banter, comedy timing, a twist. More animation than graphs. If a choice is between "clearer diagram" and "funnier acting", pick the acting.

SETUP
1. git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
2. Read ONLY: studio/SETUP.md sections "Ep 12 lessons", "Ep 13 lessons", "LF01 lessons" (or whatever the LF01 build appended), "Cup rule", "SOURCE RULE", "TORONTO BACKGROUND RULE", "MANDATORY AUTOMATIC CHECK"; studio/LF_FORMAT_V2.md; studio/episodes/lf02/script.md (APPROVED, don't rewrite lines), characters.md, voices.md, lines.json, audio_ids.md. Reuse studio/hf/lf01 (landscape template + layout_check --size landscape).

AUDIO (already generated, NEVER regenerate)
3. Four takes in ElevenLabs flow 9FCDlyMjCyXT9Z51HIp7, listed in studio/episodes/lf02/audio_ids.md (one take per character; Cyto in 2 parts). Fetch each via the fetch-audio Action (audio/list.txt) like LF01. Transcribe each with Scribe (0 credits), then CUT every line using lines.json (order + text per character) and word timings. Assemble the dialogue track in script order: 0.25s gap between lines in fast banter, 0.5-0.8s before punchlines / after "bro WHAT", and leave the silent action beats (dunk slow-mo, noir rain, Rhino heist, security-cam reveal, bird chirp) their own 1.5-3s. Captions use real spellings ("wys fam", "ahlie", "nyeahh", "6ix") even though the voice says "Waaah you sayinnn" etc.

CHARACTERS (studio/episodes/lf02/characters.md is the spec)
4. Cyto: existing v3 rig, outfit = puffer vest over hoodie; double-stacked red cup with his face logo, IN FRONT of the hand; cup down for the heart beat.
5. Neutro: update studio/rig/neutro to a Toronto-police-STYLE officer (navy shirt, peaked cap with black-and-white checkered band, blank gold badge shape, shoulder radio, notepad). NO "POLICE"/"TPS" text, NO real crest. Trench-coat overlay for the noir scene.
6. Mito: NEW vector rig like cyto3.py: bean-shaped mitochondrion with cristae "abs", red basketball jersey #6 with white/black trim, headband, high-tops; no team logo/wordmark/brand. Modes: hype and gassed (towel on head).
7. Rhino: small green spiky cold virus, sunglasses, black hoodie, never speaks.
8. FACES: build an expression set for each (smug, shocked, deadpan, hype, exhausted, determined, side-eye). Eyebrows move on every line; eye darts; squash & stretch; anticipation before big moves; 0.4-0.6s reaction holds before punchlines; listeners react while others talk (blink, nod, side-eye). Mouth shapes per syllable for whoever's talking. Show me a 4-character lineup frame in your FIRST update before building scenes.

WORLD + 3D
9. Characters stay 2D flat-ink; the WORLD gets depth (2D characters in a 3D/2.5D Toronto-body city). Use multi-plane parallax everywhere, plus up to 6-8 three.js shots (npm, pre-rendered to frames then composited): intro fly-through of the body-city into Queen's Park; the adrenal "condos" on the kidneys as 3D buildings firing hormone basketballs; a 3D-shaded beating heart (downtown) for the serious beat; Rhino's heist lasers at the nose "front door". If WebGL is flaky after two tries, fall back to parallax (E5).
10. Scenes per script: Queen's Park HQ (alarm, beanbag), incident-report cards, "MITO vs THE ALARM" streetball court with Cyto doing play-by-play at a courtside desk (scoreboard: heart rate + breathing meters), the slumped bench, the crumb + "Requesting backup", Rhino heist, "COLD CASE: 1991" film-noir (black-and-white, rain, reenactment with eye-droppers and tiny Rhinos, grainy case photos), security-cam twist (grainy, timestamp overlay), downtown heart beat (calm), cheat-code pop-ups (video-game style), skating/Distillery/side-quest montage (generic shapes, no real logos), ticket + ACHOO launch, "BREAK STARTS" outro, loop to the cold open.
11. Toronto references must stay generic shapes (Nathan Phillips Square arches, Distillery brick + lights, Line 1 train). City of Toronto only. No real logos/brands/people.

PACING RULES
12. A beat (joke, twist, reveal, sight gag) at least every 20-30s; something visibly moves every 2-3s; transitions on every cut; snap zoom + SFX on punchlines; a silent beat before "Bro, WHAT". Diagrams max ~1 per minute, under 4s, always with a character reacting. SFX library: siren, whoosh, crowd, backboard shatter, sax sting, rain, camera click, bird chirp, ACHOO (ElevenLabs sfx once each, max ~200 credits total, or free ffmpeg synth). Quiet synthesized music bed that changes per scene (noir sax, streetball beat, calm downtown).

BUILD IN SCENES (cost control)
13. Render each scene separately (max 2 renders per scene), then concat with ffmpeg. Contact sheets (1 fps, small) per scene + max 3 full frames per scene. layout_check --size landscape --step 0.5 while iterating, 0.25 once at the end. Log running cost in studio/costs.md after every 2 scenes. If the total passes $24 before the twist scene is done, simplify (drop 3D shots to parallax first). HARD STOP at $32: commit and report.

QUALITY GATE
14. layout_check = 0 FAIL. Sources end card: text >=34px, max 2 per screen, include every source in script.md's CLAIMS list (5-6 screens, >=2.5s each). "Not medical advice" on the intro card and end card. Cyto + cast on model, cup in front of the hand, faces expressive (check 3 random mid-line frames: is someone reacting?).

PACKAGE
15. 2 thumbnails 1280x720 (idea in script.md; say which is stronger), meta.json (title from script.md, 8-12 tags, keyword "what stress does to your body" first, description with chapters + all DOI links + "Not medical advice"), captions.srt, pinned_comment.txt ("What's stressing you out the most this December? 👇" + sources), check_meta.py + check_sources.py OK. Append credits to studio/costs.md and add "LF02 lessons" to studio/SETUP.md.
16. Commit studio/episodes/lf02/ + lf02/ mp4 + thumbnails + hf/lf02/ + rig changes, push. STOP and post: final video, title, description, thumbnails, layout_check result, total cost, 3 things you're least sure about. Do NOT upload or schedule.

Publish target: Sun Dec 6 2026, 6:00 PM ET (manager chat schedules it).
```

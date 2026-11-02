# Ep 10 build brief — Leafs vs Habs: your heart (publish 2026-11-07 16:00 ET)
Status: SCRIPTED, waiting for Utsha's OK (workflow steps 4-5). Do NOT build until approved.
Series: 6ix Seconds of Science · Length target 38-45s (hard cap 45s) · ~101 words ≈ 36s at 2.8 w/s · Template: `hf/template/build.py` (v2 layout + v3 rig) · follow SETUP.md "Ep 9 lessons".
Title (≤60): Leafs vs Habs: Your Heart Is Working Out (40 chars) · Tags: #hockey #leafs #habs #science #toronto #6ix #shorts · NOT made for kids · Altered/synthetic = YES · Category Science & Technology · Playlist: 6ix Seconds of Science

## Why this one / timing
Leafs vs Canadiens, Sat Nov 7, 7:00 PM puck drop at Scotiabank Arena (ticket listing; re-check the morning of). Publish 4 PM ET so it lands pre-game. Neutral on teams, no logos.

## Script (101 words; captions keep real spelling)
[HOOK 0-3s, shock] Leafs and Habs tonight? Bro, your heart's about to hit the gym… from the couch.
[3-6s, catchphrase, cup raise] Yo, it's ya boy Cyto, live from the 6ix… inside your body.
[6-14s, skeptic] Scientists put heart monitors on Habs fans. I know, allow it. Resting? About sixty beats a minute.
[14-24s, figure: heart-rate line 60 -> 114] During the game? A hundred and fourteen. That's a ninety-two percent jump, styll.
[24-32s, bar: live 110% vs TV 75%] Live at the arena hit harder than watching on TV. And the biggest spikes? Overtime and scoring chances.
[32-40s, Toronto payoff, cup down on serious] So if the Leafs go to overtime tonight, that's cardio with a hot dog, fam. Breathe. Not medical advice.
[40-44s outro, sources, loops] Like, subscribe, see you at puck drop.

## TTS text (send exactly this to ElevenLabs voice "Cyto - Toronto (A)", `eleven_v4`, 1 take; spelled for the ear)
Leafs and Habs tonight? Bro, your heart's about to hit the gym… from the couch. Yo, it's ya boy Cyto, live from the six… inside your body. Scientists put heart monitors on Habs fans. I know, allow it. Resting? About sixty beats a minute. During the game? A hundred and fourteen. That's a ninety-two percent jump, stiiill. Live at the arena hit harder than watching on TV. And the biggest spikes? Overtime and scoring chances. So if the Leafs go to overtime tonight, that's cardio with a hot dog, fam. Breathe. Not medical advice. Like, subscribe, see you at puck drop.
Chars: 568 · est ~645 credits/take (Ep 9 read: ~560 chars = 636 cr; run `estimate_only` first).

## Claims / sources (every claim traced; links go on screen, in description and pinned comment)
1. Khairy et al., Can J Cardiol 2017: 20 healthy adults (35% women, age 46±10) wore Holter monitors; median heart rate rose 92%, 60 -> 114 bpm (P<0.001). https://doi.org/10.1016/j.cjca.2017.08.002
2. Live game +110% vs televised +75% (same paper).
3. Peak heart rates most often in overtime (40%) and scoring opportunities for (25%) / against (15%). Fan passion score did NOT predict response (same paper, don't say passion matters).
4. Caveats (put in pinned comment): small study (n=20), MONTREAL fans, authors call live game 'vigorous' physical-stress-equivalent heart rate response, not proof of harm. Do not say 'Leafs fans were studied'.
Attribution line for description: "Sources via PubMed." + the DOI links above. Add "Not medical advice" line.

## Scene plan
Hook: arena silhouette (Scotiabank Arena shape, no logos) + shake on 'gym'. Figure: animated heart-rate line climbing 60 -> 114 with big counter. Bar chart live 110 vs TV 75. Overtime clock beat on 'overtime'. Payoff: couch + hot dog + breathing bubble.
Outfit: Leafs-blue jersey/toque colours only (NO logos), red cup. Game night = team-colour cup is allowed.
Lottie search terms (LottieFiles MCP -> `lottie/list.txt`): hockey puck, heart beat/pulse, stadium crowd, goal light, hot dog
Quality gate: eyes centred, one big text at a time, 1-fps frame check, safe-area sheet, loop frame = hook frame.

# Ep 13 build brief — Neutro vs the flu (publish 2026-11-10 18:00 ET)
Status: SCRIPTED, waiting for Utsha's OK (workflow steps 4-5). Do NOT build until approved.
Series: Cyto vs Disease · Length target 38-45s (hard cap 45s) · ~103 words ≈ 37s at 2.8 w/s · Template: `hf/template/build.py` (v2 layout + v3 rig) · follow SETUP.md "Ep 9 lessons".
Title (≤60): Meet Neutro: Your Flu Season Bouncer (36 chars) · Tags: #flu #immunesystem #neutrophil #science #toronto #6ix #shorts · NOT made for kids · Altered/synthetic = YES · Category Science & Technology · Playlist: Cyto vs Disease

## Why this one / timing
Flu season ramping (Canadian surveillance page unfilled when checked, so DON'T claim H1N1 or case numbers). Evergreen immune cast intro. Calendar had 'H1N1 + Neutro'; script avoids any current-case claims.

## Script (103 words; captions keep real spelling)
[HOOK 0-3s, shock] Flu's coming for the 6ix. Who pulls up first? Neutro.
[3-6s, catchphrase, cup raise] Yo, it's ya boy Cyto, live from the 6ix… inside your body.
[6-14s, Neutro enters, hype] When flu hits your airways, neutrophils are the first immune cells on the scene. Bouncer energy, dun know.
[14-24s, figure: 3 moves pop] They eat germs, release toxic chemicals, even throw out sticky nets.
[24-33s, skeptic -> sad] But McMaster researchers say it's a thin line between helpful and harmful. In severe flu, the same moves can hurt your lungs.
[33-40s, Toronto payoff] Neutro's the bouncer who's amazing till he swings too hard. Your best defence is still the yearly flu shot, fam. Not medical advice.
[40-44s outro, sources, loops] Like, subscribe, tell Neutro we said wagwan.

## TTS text (send exactly this to ElevenLabs voice "Cyto - Toronto (A)", `eleven_v4`, 1 take; spelled for the ear)
Flu's coming for the six. Who pulls up first? Neutro. Yo, it's ya boy Cyto, live from the six… inside your body. When flu hits your airways, neutrophils are the first immune cells on the scene. Bouncer energy, dun know. They eat germs, release toxic chemicals, even throw out sticky nets. But McMaster researchers say it's a thin line between helpful and harmful. In severe flu, the same moves can hurt your lungs. Neutro's the bouncer who's amazing till he swings too hard. Your best defence is still the yearly flu shot, fam. Not medical advice. Like, subscribe, tell Neutro we said wagwan.
Chars: 592 · est ~672 credits/take (Ep 9 read: ~560 chars = 636 cr; run `estimate_only` first).

## Claims / sources (every claim traced; links go on screen, in description and pinned comment)
1. George et al. (McMaster), Vaccines 2021 review 'Neutrophils and Influenza: A Thin Line between Helpful and Harmful': neutrophils are the first innate cells recruited to the infection site; effector functions = phagocytosis, degranulation, ROS, NETs; can promote resolution OR contribute to severe-disease pathology; threshold not well understood; yearly vaccination = most effective means of combating influenza. https://doi.org/10.3390/vaccines9060597
2. Supporting: Lamichhane & Samarasinghe, J Immunol Res 2019 (innate leukocytes balance immunoprotection vs immunopathology). https://doi.org/10.1155/2019/8028725
3. Supporting (optional): Buttignol et al., Respir Res 2017: autopsy lungs from H1N1pdm09 severe injury had more neutrophils and macrophages than controls. https://doi.org/10.1186/s12931-017-0630-x
4. Caveats: mostly mechanistic/animal-heavy field; the review warns human vs mouse neutrophils differ. 'Toxic chemicals' = ROS/degranulation; 'nets' = NETs.
Attribution line for description: "Sources via PubMed." + the DOI links above. Add "Not medical advice" line.

## Scene plan
Neutro intro (needs new rig asset: draw once as vector in cyto3 style, 1 pose set: idle, flex, crossed arms). Three move icons pop (eat / spray / net). Slider 'helpful <-> harmful' animates. Vaccine Lottie at payoff.
Outfit: toque + hoodie (cold-weather match), red cup. Introduces NEUTRO (neutrophil security guard): blue-and-white-toque-free design, high-vis vest, earpiece, arms crossed, same flat-ink style, NOT Cyto-shaped (multi-lobed nucleus visible). New cast member: design once, store in `studio/rig/neutro/`.
Lottie search terms (LottieFiles MCP -> `lottie/list.txt`): shield, virus particle, security guard, sneeze, syringe/vaccine
Quality gate: eyes centred, one big text at a time, 1-fps frame check, safe-area sheet, loop frame = hook frame.

## Toronto background plan (Nov 2 rule: no generic backgrounds)
- Hook: Union Station Great Hall / front doors as the 'airway entrance' (Neutro stands at the door like security).
- Flu spreading: packed Line 1 train at rush hour, sneeze cloud passing from rider to rider, a raccoon on a TTC bench.
- 'Thin line' scene: slider drawn over a snowy Queen streetcar track; GO train in the background.
- Payoff: pharmacy window with flu-shot sign (generic, no brand), Nathan Phillips Square rink in the background. Neutro design: high-vis vest + earpiece, TTC-inspector energy.

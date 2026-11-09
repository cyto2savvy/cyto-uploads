# HARD RULES (Utsha, Nov 9, 2026, after Ep 15). These override every older note in the repo. make_episode.py enforces what it can; a FAIL blocks the draft.

## Thumbnails
1. The background shows THE TOPIC, in Toronto where it can. A Toronto skyline/CN Tower is NOT allowed unless the topic is the city. Cancer/oncology = Sunnybrook Odette Cancer Centre, Princess Margaret, a hospital row on University Ave; heart = a Toronto cardiac/hospital or ECG scene; sleep = bedroom/night streetcar; etc. If no real photo exists, use a drawn canon scene of the topic, never a generic city.
2. Each `thumbnails[]` entry needs `photo` (or a drawn scene) AND `bg_subject` = "<topic word> + <Toronto place>" (e.g. "cancer + Sunnybrook Odette Cancer Centre"). Validation fails without it and fails if the subject names no topic word from the title.
3. One giant Cyto face, <= 4 words, 1 hero object, A/B with the stronger one named, 160 px readable test (THUMBNAIL_FORMAT_V2.md still applies for the rest).

## Video body (every scene, not just the hook)
4. EVERY scene is canon cut-out style (SCENE_STYLE.md): drawn props, parallax, pop-in with overshoot. Plain text on a backdrop is not a scene.
5. Each scene declares `props` (>= 2 drawn objects: organ, bars/chart, counter, arrow that draws on, map card, icon row) and moves a new thing in every 2 s. Text per scene <= 8 words (headline + card). No half-empty screen: the middle of the frame is always a visual, never a gap.
6. No two consecutive scenes share the same backdrop. Backdrops come from the topic (hospital row, trail, TTC, lab-bench cut-out), not always the skyline.
7. Photos are for thumbnails only.

## Transitions
8. Every cut has a transition 0.35-0.5 s that moves continuously: no frozen frames inside it, no single-frame pop, no hard cut. Check = frame-diff series around every cut (make_episode `transitions smooth`).
9. Same-backdrop cuts are banned (rule 6), so the transition always changes something visible. Cyto's pose/expression blends across the cut, never jumps.

## Cyto and the cup
10. Cyto is fully on screen, the WHOLE cup inside the frame (>= 40 px margin, nothing clipped at an edge), cup in his mitten with the hand wrapped around it, handled with a natural hold: cup rests at chest height beside the body, sways slightly, steam rises. Never floating, never half off-screen, never placed down.
11. Cyto is large enough to read on a phone (>= 55% frame width) and centred-low, with the visual above him.

## Process
12. Plan.md scene table must list each scene's props; the build is rejected if the render does not show them (check reads `props_rendered` in video.layout.json).
13. Before showing a draft: contact sheet at 2 fps, transition frame-diff plot, thumbnail at 160 px, all clean. Show Utsha only a draft that passes.
14. Repo hygiene: current docs only at the top level of studio/. Anything superseded goes to `archive/` (repo root) the same day. studio/INDEX.md lists what to read.

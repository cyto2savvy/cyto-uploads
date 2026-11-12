# HARD RULES (Utsha, Nov 9, 2026, after Ep 15). These override every older note in the repo. make_episode.py enforces what it can; a FAIL blocks the draft.

## Thumbnails
1. The background shows THE TOPIC, in Toronto where it can. A Toronto skyline/CN Tower is NOT allowed unless the topic is the city. Cancer/oncology = Sunnybrook Odette Cancer Centre, Princess Margaret, a hospital row on University Ave; heart = a Toronto cardiac/hospital or ECG scene; sleep = bedroom/night streetcar; etc. If no real photo exists, use a drawn canon scene of the topic, never a generic city.
2. Each `thumbnails[]` entry needs `photo` (or a drawn scene) AND `bg_subject` = "<topic word> + <Toronto place>" (e.g. "cancer + Sunnybrook Odette Cancer Centre"). Validation fails without it and fails if the subject names no topic word from the title.
3. One big Cyto face, <= 4 words, 1 hero object, A/B with the stronger one named, 160 px readable test (THUMBNAIL_FORMAT_V2.md still applies for the rest).
3b. Big is not cropped (Utsha, Nov 11, Ep 14 "too big"): the whole Cyto (toque, pom, face) and the whole cup sit inside the frame with >= 40 px margin, Cyto <= ~75% of frame width, and the headline never overlaps his face. Shorts thumbnails are the VERTICAL 1080x1920 file (safe zone x 60-940, y 200-1480); 16:9 is only for long-form. `thumbs.js` has `cscale`/`cx`/`cy` to size and place him.

## Video body (every scene, not just the hook)
4. EVERY scene is canon cut-out style (SCENE_STYLE.md): drawn props, parallax, pop-in with overshoot. Plain text on a backdrop is not a scene.
5. Each scene declares `props` (>= 2 drawn objects: organ, bars/chart, counter, arrow that draws on, map card, icon row) and moves a new thing in every 2 s. Text per scene <= 8 words (headline + card). No half-empty screen: the middle of the frame is always a visual, never a gap.
6. No two consecutive scenes share the same backdrop. Backdrops come from the topic (hospital row, trail, TTC, lab-bench cut-out), not always the skyline.
7. Photos are for thumbnails only.

## Transitions
8. Every cut has a transition 0.35-0.5 s that moves continuously: no frozen frames inside it, no single-frame pop, no hard cut. Check = frame-diff series around every cut (make_episode `transitions smooth`).
9. Same-backdrop cuts are banned (rule 6), so the transition always changes something visible. Cyto's pose/expression blends across the cut, never jumps.

## Cyto and the cup
**Cup (canon v2):**
- Cyto always holds the canon v2 paper COFFEE cup: white body, red band, brown lid, small flat Cyto-face logo, steam rising. Never the old double-stacked party cup.
- No real brand names or logos. Never show what's inside, never reference drinking or getting high.
- Whole cup always in frame, mitten wrapped around it, held at chest height.
- On sponsored episodes, consider swapping it for a tumbler.

10. THE CUP = the canon v2 paper COFFEE cup (white body, red band, brown lid, small flat Cyto-face logo, STEAM rising). Never the old double-stacked party cup (Utsha confirmed Nov 11). No real brand, never show contents, no drinking/getting-high references. Cyto is fully on screen, the WHOLE cup inside the frame (>= 40 px margin, nothing clipped at an edge), cup in his mitten with the hand wrapped around it, handled with a natural hold: cup rests at chest height beside the body, sways slightly, steam rises. Never floating, never half off-screen, never placed down.
11. Cyto is large enough to read on a phone (>= 55% frame width) and centred-low, with the visual above him.

## Process
12. Plan.md scene table must list each scene's props; the build is rejected if the render does not show them (check reads `props_rendered` in video.layout.json).
13. Before showing a draft: contact sheet at 2 fps, transition frame-diff plot, thumbnail at 160 px, all clean. Show Utsha only a draft that passes.
14. Pipeline buffer: always >= 3 episodes built or scheduled ahead of today. The manager chat flags a gap as soon as fewer than 3 are queued and tells the idea chat to pitch.
15. Social queue: every episode that is scheduled also gets a row in the Sheet "Cyto IG+FB Post Queue" (episode, post_date, video_url, caption, posted blank, thumbnail_url = the vertical thumbnail raw URL). The daily scheduled task posts it to Instagram and Facebook; the Meta "AI info" label is turned on by hand.
16. Repo hygiene: current docs only at the top level of studio/. Anything superseded goes to `archive/` (repo root) the same day. studio/INDEX.md lists what to read.
17. No overlaps (Utsha, Nov 11, Ep 15 v2): props, headline, card, captions and Cyto may not cover each other. make_episode checks bounding boxes every frame (prop vs prop, prop vs headline/card/captions, anything vs Cyto's face or cup); an overlap longer than 0.3 s = FAIL.
18. The first cut (hook -> intro) is checked like every other transition: continuous, no pop, no stall, Cyto's pose blends.
19. Reuse before you build (a Short must take ~15 min of build time, not an hour): pick backdrops, props, transitions and scene templates from studio/rig_v2/LIBRARY.md by id in episode.json. Only a genuinely new visual may be drawn, and it is added to the library the same day (id, params, thumbnail) so the next episode can reuse it. Unchanged scenes are cached (render keyed by a hash of the scene JSON + rig version) so a re-render only redoes what changed.
20. Mix, don't clone (Utsha, Nov 12): every episode must look somewhat unique. The library (rig_v2/LIBRARY.md) is a pool built from ALL past episodes; each new episode picks from it by topic tags and recency, it never copies the last episode's backdrops and animations wholesale. make_episode check "variety vs last 3 episodes": FAIL if more than half of the scenes use a backdrop+prop combination already used in any of the last 3 episodes, or if two episodes in a row share the same backdrop order. Every episode must use at least one least-recently-used or brand-new item, and reused items must vary their params (position, colour, scale, count, timing). Usage is logged per episode in rig_v2/library_usage.json.


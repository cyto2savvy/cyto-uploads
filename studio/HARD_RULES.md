# HARD RULES (Utsha, Nov 9, 2026, after Ep 15). These override every older note in the repo. make_episode.py enforces what it can; a FAIL blocks the draft.

## Thumbnails
1. The background shows THE TOPIC, in Toronto where it can. A Toronto skyline/CN Tower is NOT allowed unless the topic is the city. Cancer/oncology = Sunnybrook Odette Cancer Centre, Princess Margaret, a hospital row on University Ave; heart = a Toronto cardiac/hospital or ECG scene; sleep = bedroom/night streetcar; etc. If no real photo exists, use a drawn canon scene of the topic, never a generic city.
2. Each `thumbnails[]` entry needs `photo` (or a drawn scene) AND `bg_subject` = "<topic word> + <Toronto place>" (e.g. "cancer + Sunnybrook Odette Cancer Centre"). Validation fails without it and fails if the subject names no topic word from the title.
3. One big Cyto face, <= 4 words, 1 hero object, A/B with the stronger one named, 160 px readable test (THUMBNAIL_FORMAT_V2.md still applies for the rest).
3b. Big is not cropped (Utsha, Nov 11, Ep 14 "too big"): the whole Cyto (toque, pom, face) and the whole cup sit inside the frame with >= 40 px margin, Cyto <= ~75% of frame width, and the headline never overlaps his face. Shorts thumbnails are the VERTICAL 1080x1920 file (safe zone x 60-940, y 200-1480); 16:9 is only for long-form. `thumbs.js` has `cscale`/`cx`/`cy` to size and place him.

## Video body (every scene, not just the hook)
4. EVERY scene is canon cut-out style (SCENE_STYLE.md): drawn props, parallax, pop-in with overshoot. Plain text on a backdrop is not a scene.
5. Each explaining scene declares `props` (usually 2+ drawn objects, only ones that SHOW what is being said: organ, bars/chart, counter, arrow that draws on, map card, icon row) and moves a new thing in every 2 s. Text per scene <= 8 words (headline + card). No half-empty screen: the middle of the frame is always a visual, never a gap.
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
21. Nothing floats for no reason (Utsha, Nov 12, Ep 15): every element on screen must show something the narrator is saying at that moment. Banned: decorative or ambient floaters (stray circles, bubbles, tabs/boxes, dot rows, a jogger or shoe that illustrates nothing), props carried over from a template or the previous scene, and props that stay after their sentence ends. Each prop in episode.json needs `shows` (what it illustrates, e.g. "28% drop in comeback risk") and an anchor to the spoken words (`at` = word/beat); it appears when the word is said and leaves within 1.5 s of the sentence ending. The catchphrase and outro scenes are clean: Cyto, headline/captions, backdrop only, no props. Zero props is fine when the line has nothing to show; padding a scene to hit a prop count is not. make_episode check "no floaters": FAIL if a prop lacks `shows`/anchor, is on screen > 1.5 s past its anchor, or has no matching word in the scene's script.

## Views (Utsha, Nov 14, after the 16-Short analytics pull — see studio/GROWTH_NOTES.md)
The data: 85% of views come from the Shorts feed. Every episode holds ~15 seconds no matter how
long it is, so longer videos just score a worse retention percentage. Seeded episodes stop at
~1,000 views because shares and comments are ~zero. Rules 22-26 exist to fix those three things.

22. **Answer the hook, then worry about length** (rewritten Nov 14 after Ep 18 — the first
    version of this rule produced a 62-word episode whose hook asked "why does flexing your
    bicep burn?" and which never answered it. Short and empty is worse than long.)
    - The hook's question MUST be answered in the body, with a mechanism, in plain words.
      make_episode FAIL: the hook is a question and no later line answers it.
    - **Minimum 3 explaining lines** between the hook and the payoff. One line of mechanism is
      not an episode. This floor beats the ceiling: if the idea needs 4 beats, take the seconds.
    - Narration 24-32 s. Over 34 s = FAIL. Budget it as: hook <= 2 s, 3-4 explaining beats,
      Toronto payoff, then the outro — and the outro's seconds are NOT part of the body budget.
    - Still cut a beat rather than speeding the read, and still make the last frame match the
      first so the loop is seamless (Ep 1 looped and held 28 s / 91%).
    - Why we are not Kurzgesagt-length yet: their Shorts run 71-79 s and hold it. We hold
      ~15-17 s. Earning second 15 is the goal; a short runtime is a stopgap, not a principle.
      Revisit the ceiling once avg seconds held clears ~20 s.
23. **A different intro every episode.** The first 2 spoken words are the question or the claim,
    never setup ("In a Canadian-led trial…" opened Ep 15: 40 views). Scene 0 carries the whole
    hook on screen at frame 1 (`instant`). Pick an opening pattern that none of the last 3
    episodes used, and log it in `library_usage.json` as `intro:<pattern>`:
    cold-open question on a full-frame visual · stat stamp slams in first · Cyto mid-sip
    reacting · POV push-in through the skin · a wrong answer crossed out · 1-frame before/after
    tease · Cyto already mid-sentence. New patterns are welcome and get added to LIBRARY.md.
    **The catchphrase never appears in the first 6 seconds**, and it gets its OWN beat — a
    1.5-2 s scene with a visual, placed after the payoff. It is never a stinger tacked onto the
    end of another line (Ep 18 did that and it read as a blurt: "Not medical advice. Send this
    to the one who does the bicep heart. Yo, it's ya boy Cyto!" — three jobs in one breath).
    If there is no room for its own beat, cut it from that episode; it is not mandatory on
    Shorts. (Measured: it sat at 3.4 s in Ep 12, 4.5 s in Ep 13, 4.8 s in Ep 14. Those three
    have the worst retention in the catalogue, which is why it moved back.)
23b. **One line, one job.** No spoken line may carry more than one of: the disclaimer, the ask,
    the catchphrase. The "not medical advice" line is ON-SCREEN TEXT and is not spoken unless
    the topic needs it said. make_episode FAIL if any line contains two of the three.
24. **One ask, and it's a send.** Shares are the strongest expansion signal and we have had 0-3
    per episode, zero on nine of them. Every episode ends on exactly one ask, spoken AND on
    screen, and it is a send to a specific person: "send this to the one who always…".
    Like/subscribe may ride along in the outro art but is never the ask. The closing question
    goes ON SCREEN, not only in the pinned comment, and the pinned comment is posted the hour
    the episode goes public.
25. **Library expansion sprint, Eps 18-25.** The library is too small (9 backdrops, ~14 props),
    which is why recent episodes look alike. For these 8 episodes each build ships ~75% new
    visual material: at least 75% of scenes contain an element making its first appearance, and
    at least **2 brand-new backdrops + 2 brand-new props per episode**, all added to
    backdrops.js/props.js, LIBRARY.md and library.png the same day. New means a different
    silhouette, not a recolour. That takes the library to roughly 25 backdrops and 30 props.
    Build time will go back up during the sprint; that is the trade and it is $0 (render only).
    From Ep 26 the quota drops to >= 1 new item per episode and rule 20 becomes the main test.
26. **Topic gate.** A topic has to be phrasable as "why does your body do X", "is X real", or
    "what happens to your body when X" — universal, visceral, searchable. Five of our six
    non-seeded episodes were local sports, a clock change, or "does this health practice work"
    opening on a caveat. Toronto is the flavour, never the reason to watch: a local hook is
    allowed only when the body fact leads and the city follows.

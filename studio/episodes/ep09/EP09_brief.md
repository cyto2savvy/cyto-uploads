# Ep 9 build brief — "Dark at 5" / vitamin D myth (publish Fri Nov 6, 6 PM ET)
Status: SCRIPTED, waiting for Utsha's OK (steps 4-5 of the workflow). Do NOT build until approved.
Series: 6ix Seconds of Science · Length target 38-45s (hard cap 45s, `C.MAX_T_V2`) · Template: `hf/template/build.py` (v2 layout + v3 rig)

## Why this one / trend fit
- First full week after the clocks fell back: sun is gone just before 5 PM in Toronto. Peak "why am I tired/sad at 5pm" feeling (VERIFY exact sunset for Nov 6 on timeanddate before locking an on-screen time; script says "before five").
- Myth-buster format = our proven winner (sugar rush 1,186 views, scared-to-death 1,448 vs 89-232 for generic ones).
- Toronto-specific twist: our audience is heavily South Asian/diverse; the Health Canada study shows low vitamin D is more common in South Asian Canadians year-round. Tell it as a fact about the data, not a stereotype; supplements mattered most.
- Nov 6 Toronto event search returned nothing usable. Don't invent one. Anchor = the clock change + early dark (same week trend). Re-check Leafs/TTC/weather the morning of the build for the outfit.

## The idea (one idea only)
Myth: "winter crashes your vitamin D." Truth: in Canadian studies the summer-vs-winter swing was small; supplements and ancestry mattered more. But the dark CAN hit mood (seasonal affective disorder), and bright white light is what the evidence supports.

## Script (~108 words ≈ 38-40s at ~2.8 w/s; recount after edits). Slang: ahlie, styll, bare, dun know, say less. Toronto refs: TTC, 4:50-ish dark.
[HOOK 0-3s, shock face] Bro. It's dark before five. Is winter actually killing your vitamin D?
[3-6s, catchphrase, cup raise] Yo, it's ya boy Cyto, live from the 6ix… inside your body.
[6-12s, skeptic] Sun clocks out, so your D crashes, ahlie?
[12-22s, figure: bar chart, the twist] Nah. Canadian studies found the winter dip was small. What mattered way more? Supplements, and ancestry. South Asian Canadians ran low all year, styll.
[22-32s, sad then hype] But the dark can still hit your mood. For some people it's real seasonal depression. And a 2025 review of seventeen trials? Bright white light came out on top.
[32-40s, Toronto payoff, cup down on "serious"] So before you blame the TTC for your vibe… check your D, get some light, say less. Not medical advice.
[40-45s outro, sources on screen, loops to hook] Like, subscribe, see you at five. (cut back to "Bro. It's dark before five.")

Trim rule: if over 45s, drop the 'ahlie' myth line first; never cut the hook or payoff.

## Claims / sources (every claim traced; link in description + pinned comment + on-screen)
1. Summer-to-winter vitamin D swing was small in Canadian studies.
   - Li et al., Can J Public Health 2011 (pregnant women, Vancouver 49°N): mean 25OHD 67 nmol/L; ~12 nmol/L higher in summer than winter; season effect "not large". https://doi.org/10.1007/BF03404056
   - Nagasaka et al., PLoS One 2018 (Health Canada, Ottawa): spring vs fall differences small, significant only in European ancestry (2.9 nmol/L). https://doi.org/10.1371/journal.pone.0207429
2. Supplements and ancestry = biggest differences; low 25OHD more common in South Asian vs European Canadians (Nagasaka 2018). Same DOI. Paper says skin colour was NOT a major factor: do not say "skin".
3. Toddlers (Vancouver) DID show a winter jump in low status (43% vs 13%), so winter matters more in young kids: Wiedeman et al., J Nutr 2026. https://doi.org/10.1016/j.tjnut.2026.101382 . Not in the script (adult myth). Put in the pinned comment as nuance.
4. Bright white light best of visible light colours for SAD: Wan et al., Medicine 2025, network meta-analysis, 17 RCTs, 773 patients; authors say larger studies still needed. https://doi.org/10.1097/MD.0000000000043107
5. (Textbook, optional on-screen mechanic) Light entrains the circadian clock via the suprachiasmatic nucleus. Verify against a textbook page before using; leave out if not verified.
Caveats to keep honest: studies are pregnant women / mixed adults, not "everyone"; single-study ancestry finding. Description: "Not medical advice. Low mood lasting 2+ weeks or low vitamin D worries: talk to a doctor or pharmacist."

## Scene plan (v2 layout, big Cyto lower-left, cards right; all inside C.SAFE)
| t | Scene | Visual | Motion / acting |
|---|---|---|---|
| 0-3 | Hook | Toronto skyline at dusk (art.skyline) + moon, clock "4:5x"? only if verified, else sun dipping | punch-zoom, `shock`, shake on "dark before five" |
| 3-6 | Catchphrase | Cyto centre, puffer vest, red cup | cup raise, hype |
| 6-12 | Myth | big "SUN GONE = D GONE?" card, sun Lottie setting | `skeptic`, whip transition |
| 12-22 | Twist | animated bar chart: Summer 67 vs Winter 55 (Vancouver, approx +12), then pill/capsule beat | arrows draw on, numbers pop, slow push; supplement bottle drops in on "Supplements" |
| 22-32 | Mood | dark window -> lamp turns on (white light) | `sad` then `hype` on "came out on top"; Lottie lamp/sunrise |
| 32-40 | Payoff | TTC streetcar stop at 4:5x PM, snow, subway-doors transition | cup set down for "Not medical advice" |
| 40-45 | Outro | sources on screen + like/sub | loop frame = hook frame (same pose/eyes) |
Outfit: toque + puffer vest (red cup). Cup rules unchanged, nothing inside shown.

## Lottie (LottieFiles MCP, add `name url` to `lottie/list.txt`, push, check `lottie/status.txt`)
Search terms: "sunset", "sun rays", "moon stars", "snowfall", "pill capsule", "light bulb on", "desk lamp", "clock". Prefer navy/yellow/teal to match the brand. One per science scene; drive with `C.lottie_js`. Offset frames if they start blank (see Ep 8 Zzz).

## Voice — ElevenLabs (connected) vs Utsha-disguised
Current standing plan: Utsha records, `cyto_voice.py` disguises ($0). ElevenLabs gives a second option to A/B:
- Library pick if we just want a fast test: "jimmy - Energetic & Chill" (voice_id 6Wfy7ZKe234uNpJqQZIz, young US male, made for Shorts). Not Toronto, but chill.
- Better: `creative_design_voice` (eleven_ttv_v3) from a description: "young adult male, Toronto accent, laid-back, slightly raspy, quick and casual, urban slang", previewing on the approved Ep 9 script. Costs credits: Utsha OKs first; run `estimate_only` first; never retry a generation (double charge).
- Performance: `eleven_v4` takes inline tags ([laughs softly], [whispering], [excited]); use them for the story-time cadence in VOICE.md. Spell for the ear ("six", "five").
- Open risk: audio may not download into the sandbox (like vidIQ S3). If so, Utsha drags the file in chat.
- Pipeline after audio is the same: silencedetect -> segs.json -> build_voice2.py -> timing.json.

## Make it better than Ep 8 (checklist)
- [ ] One new visual every 2-3s, a transition on every cut, nothing still >1s.
- [ ] Bar chart animates (bars grow, numbers pop); Lottie per science scene; Ken Burns on any photo.
- [ ] 2+ expressions beyond neutral; `looks` at the chart; sip on a pause, cup raised on the punchline.
- [ ] Captions word-by-word, key words big + coloured, slang in brand colour.
- [ ] Frame check: Cyto on model, cup visible, safe-zone sheet (`C.safe_sheet`), captions readable on a phone.
- [ ] Loop: last frame == first frame.
- [ ] Two thumbnails (series pill, <=4-word headline, hero = pill bottle vs sun, huge reacting Cyto); say which is stronger.
- [ ] meta.json + `check_meta.py` 0 FAIL before upload. Title <=60, keyword in first 40.

## Title / metadata candidates (pick after OK)
- "Is Winter Really Killing Your Vitamin D?" (40 chars) <- recommended (myth question)
- "Why It's Dark at 5PM Hits Different 🌑"
- Keyword: "winter vitamin d" (not volume-checked; vidIQ credits ~1 left, so don't spend)
- Hashtags: #vitamind #winter #science #toronto #6ix #shorts. Series playlist: 6ix Seconds of Science. Related video: Ep 8 (3AM).
- Pinned comment: "Do you take a D supplement in winter? Be honest 👇 Toddlers swing more in winter (Wiedeman 2026), link in description."

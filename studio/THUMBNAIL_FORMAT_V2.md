# Thumbnail format v2 — MrBeast style (Utsha, Nov 9, 2026). Replaces the old thumb.py structure.
Tool: `python3 studio/branding/rebrand-v2/make_thumb.py out.png --lines "A|B|C" --colors "w,w,y" --expr shock --bg "#ff3b30,#6a00ff" --scene ecg [--arrow] [--object x.png] [--side left|right]`
Output 1280x720 using the CANON v2 Cyto (never the old rig PNGs).
1. ONE giant face: Cyto fills ~100% of the height on one side, cropped by the frame, thick white sticker outline + hard drop shadow.
2. Expression sells the curiosity: `shock` (default, mouth open, wide eyes), `solemn` (serious/Remembrance), `chill` (canon default). Never a neutral face on a normal episode.
3. Text: <= 4 words total, <= 3 lines, giant, white + ONE colour word (yellow/red), black stroke. A question or a shocking claim, not the title.
4. BACKGROUND = THE TOPIC (never a generic gradient): pick a scene that shows the subject, then 2 saturated colours + light burst. Built-in `--scene`: ecg (heart/silence/stress), clock (sleep/time/DST), snow (cold/winter/immune), toronto (city/sports/events), stars (night/quiet). Anything else: `--bg-image photo.jpg` (Unsplash free photo of the topic, auto cover-crop + saturation + colour tint; try the Unsplash tool's download_asset, or add a new scene function in make_thumb.py: e.g. a sugar cube, brain, bone, sun for vitamin D). High contrast, no clutter, no tiny details.
5. One focal object or an arrow/circle pointing at the "thing" (optional). Max 3 elements: face, text, object.
6. Test: shrink to 160px wide, it must still read. Make 2 options, say which is stronger. Use Studio "Test & Compare".
7. Tone exceptions: Remembrance Day / grief / serious topics use `solemn` + navy palette; no shock face, no arrows.
8. No real brands/logos, no politics. The cup stays generic.
Note: Shorts viewed in the feed ignore thumbnails (the first frame matters); thumbnails drive search, channel page, browse and Shorts-shelf clicks.

## Photo backgrounds (MrBeast = real scenes of the topic; procedural --scene is only a fallback)
- Looks to copy: full real-world scene of the topic behind a huge face; SPLIT-SCREEN contrast (`--bg-image A --bg2 B --labels "57C|-71C"`); a corner BADGE ("DAY 115", "100 COPS": `--badge`); 0-3 words of text.
- Source A (Utsha chose this Nov 9): AI-generate ONE photoreal 16:9 scene per episode with ElevenLabs `creative_generate_image` (model bytedance-seedream-5-pro, generations_count=1, ~818 credits ~ $0.16; say the cost first, estimate_only first). Prompt: "photorealistic cinematic wide shot of <topic scene>, rich saturated colours, shallow depth of field, large empty space on the left third, no people, no text, no logos". The sandbox cannot download from ElevenLabs/Unsplash: bring the file in via a fetch GitHub Action list (like audio/list.txt) or have Utsha download it from the flow link and attach it.
- Source B ($0): free Unsplash photos through `photos/list.txt` + the fetch-photos GitHub Action (already in the repo, files land in `photos/`), then `--bg-image photos/<name>.jpg`.
- Split-screen is the strongest format for myth/vs/before-after topics (loud vs quiet, hot vs cold): 2 images.

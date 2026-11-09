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

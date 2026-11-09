# Ep 14 v3 checks (Nov 9 2026)
- Canon tests (`bash studio/branding/rebrand-v2/run_tests.sh`): 29/29 PASS (19 original + 10 new rig checks: ids/layers, runtime drift, no id collisions, 4 talking mouths, mouth isolation, blink, cup+hand rigid group, rig idle no-jitter, outfit silhouette within 4%).
- JITTER CHECK (`jitter.py`, every frame, 30 fps, full video): BEFORE (v2 PNG rig) 8 FAIL / 8 parts (spike ratios 470-6442x median, up to 5 reversals/0.3s). AFTER (canon rig) 0 FAIL / 8 (max 1 reversal/0.3s, spike ratio <= 2.1x; cup + hand static: 0.0).
- layout_check: 0 FAIL (5 WARN = the gold "6" medallion/toque badge inside Cyto's own drawing).
- Voice onset 0.022 s; claim + heart trace on frame 1; catchphrase 5.8 s; re-hook 4.1 s.
- First 8 s static-run: longest still run 0 frames. New visual every <=2 s (0.0 claim/trace, 2.0 silence zone, 3.2 heart icon, 4.1 re-hook title + BP/breathing ? lines, 5.7 skyline, 7.4 LIVE FROM THE 6IX, 9.0 inside chip).
- Mouth: 255 silent frames -> 0 not closed; 111 loud frames -> 72 open.
- Loop frame vs hook frame: mean abs diff 2.05/255 (only the first caption differs).
- Duration 33.55 s; mp4 19.3 MB.

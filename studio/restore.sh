#!/usr/bin/env bash
# Rebuild the Cyto studio workspace in a fresh Claude session.
# Usage:  git clone https://github.com/cyto2savvy/cyto-uploads && bash cyto-uploads/studio/restore.sh
set -e
S="$(cd "$(dirname "$0")" && pwd)"
H=/home/claude
mkdir -p $H/cyto2 $H/hf $H/thumbs
cp $S/pipeline/*.py $H/cyto2/
cp -r $S/rig $H/cyto2/rig
mkdir -p $H/cyto2/photos && cp $S/photos/* $H/cyto2/photos/
cp $S/branding/* $H/cyto2/
cp $S/thumbs/* $H/thumbs/
# episodes: ep01 lives in cyto2/, the rest in /home/claude/epN
cp $S/episodes/ep01/* $H/cyto2/ 2>/dev/null || true
for d in $S/episodes/ep[0-9]*; do
  n=$(basename $d | sed 's/ep0*//'); [ "$n" = "1" ] && continue
  mkdir -p $H/ep$n && cp -r $d/* $H/ep$n/
done
# finished episode videos (ep07/build.py reads its audio mix from the mp4)
for d in $S/../ep[0-9][0-9]; do n=$(basename $d | sed "s/ep0*//"); if ls $d/*.mp4 >/dev/null 2>&1; then mkdir -p $H/ep$n && cp $d/*.mp4 $H/ep$n/; fi; done
# hyperframes projects
cp $S/hf/cytohf.py $S/hf/cyto3.py $S/hf/art.py $S/hf/package.json $H/hf/
cp -r $S/hf/thumbs $S/hf/outfits $H/hf/
cp -r $S/hf/ep07 $S/hf/rigtest $S/hf/v2 $S/hf/v2test $S/hf/v3test $S/hf/template $H/hf/
for d in $S/hf/ep[0-9][0-9]; do if [ -d "$d" ]; then cp -r "$d" $H/hf/; fi; done
# v2: Lottie JSON (fetched by the fetch-lottie workflow) + Mermaid renderer config
mkdir -p $H/lottie && cp $S/../lottie/*.json $H/lottie/ 2>/dev/null || true
CH=$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | head -1)
echo "{\"executablePath\":\"$CH\",\"args\":[\"--no-sandbox\"]}" > $H/hf/v2/pup.json
cd $H/hf && npm i hyperframes@0.8.222 gsap@3.13.0 lottie-web@5 @mermaid-js/mermaid-cli >/dev/null 2>&1
for d in $H/hf/*/; do if [ -f "$d/build.py" ]; then ln -sfn ../node_modules "$d/node_modules"; fi; done
pip install --break-system-packages -q pillow numpy >/dev/null 2>&1 || true
# rebuild voice.wav + timing from raw.mp3 + segs.json
for n in 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do [ -f $H/ep$n/segs.json ] && (cd $H/cyto2 && python3 build_voice2.py $H/ep$n >/dev/null) || true; done
echo "Restored. Before rendering with HyperFrames run:"
echo '  export HYPERFRAMES_BROWSER_PATH=$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell | head -1)'

pip install --break-system-packages -q pyworld pedalboard 2>/dev/null; cp studio/pipeline/cyto_voice.py /home/claude/cyto2/ 2>/dev/null

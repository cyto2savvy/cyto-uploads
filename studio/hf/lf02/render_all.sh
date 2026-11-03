#!/bin/bash
export HYPERFRAMES_BROWSER_PATH=$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell | head -1)
mkdir -p /home/claude/lf02/renders
for s in "$@"; do
  cd /home/claude/hf/lf02/$s && npx hyperframes render --output /home/claude/lf02/renders/$s.mp4 --fps 30 --workers 4 > /home/claude/lf02/renders/$s.log 2>&1
  echo "$s $(ffprobe -v error -show_entries format=duration -of csv=p=0 /home/claude/lf02/renders/$s.mp4 2>/dev/null)" >> /home/claude/lf02/renders/done.txt
done

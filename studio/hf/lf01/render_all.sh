#!/bin/bash
export HYPERFRAMES_BROWSER_PATH=$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell | head -1)
mkdir -p /home/claude/lf01/renders
for k in "$@"; do
  s=$(date +%s)
  (cd /home/claude/hf/lf01/ch$k && npx hyperframes render . -o /home/claude/lf01/renders/ch$k.mp4 --quiet > /home/claude/lf01/renders/ch$k.log 2>&1)
  echo "ch$k done rc=$? $(( $(date +%s) - s ))s" >> /home/claude/lf01/renders/progress.txt
done

#!/bin/bash
# run layout_check on every scene, 4 at a time
STEP=${1:-0.5}
cd /home/claude/hf
ls -d lf02/s[0-9][0-9] | xargs -n1 basename | xargs -P 4 -I{} sh -c "timeout 1500 python3 layout_check.py {} --root /home/claude/hf/lf02 --size landscape --step $STEP --brief /home/user/cyto-uploads/studio/episodes/lf02/script.md > /tmp/claude-0/lc_{}.txt 2>&1"
for f in /tmp/claude-0/lc_s*.txt; do echo "== $f"; grep -E "FAIL|WARN|ERROR" $f | head -12; done

#!/bin/bash
# concat the scene renders, mux the episode mix -> lf02/cyto-lf02-stress-december.mp4
set -e
R=/home/claude/lf02/renders
: > $R/list.txt
for s in s01 s02 s03 s04 s05 s06 s07 s08 s09 s10 s11 s12 s13 s14 s15 s16 s17; do
  N=$(python3 -c "import json;m=json.load(open('/home/claude/hf/lf02/$s/meta.json'));print(round(m['t1']*30)-round(m['t0']*30))")
  ffmpeg -v error -y -i $R/$s.mp4 -an -frames:v $N -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p $R/${s}_t.mp4
  echo "file '$R/${s}_t.mp4'" >> $R/list.txt
done
ffmpeg -v error -y -f concat -safe 0 -i $R/list.txt -an -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p $R/video.mp4
mkdir -p /home/user/cyto-uploads/lf02
ffmpeg -v error -y -i $R/video.mp4 -i /home/claude/lf02/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart /home/user/cyto-uploads/lf02/cyto-lf02-stress-december.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 /home/user/cyto-uploads/lf02/cyto-lf02-stress-december.mp4

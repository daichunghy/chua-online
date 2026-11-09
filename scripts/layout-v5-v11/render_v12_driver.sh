#!/bin/bash
# V12 verification renders: cho khe (ffmpeg=0, khong blender la, load<7) roi render.
BL=~/workspace/vinh-trang-3d/tools/blender5/blender
F=~/workspace/chua-online-work/layout_v14_v12.blend
L=~/workspace/chua-online-work/layout
S=$L/scripts/render_v12.py
while true; do
  NF=$(pgrep -c ffmpeg || true)
  NB=$(pgrep -c -f "tools/blender5/blender" || true)
  LD=$(awk '{print $1}' /proc/loadavg)
  OK=$(awk -v l="$LD" 'BEGIN{print (l<7.0)?1:0}')
  if [ "${NF:-99}" -eq 0 ] && [ "${NB:-99}" -eq 0 ] && [ "$OK" = "1" ]; then
    echo "GAP OPEN $(date +%H:%M:%S) load=$LD"; break
  fi
  echo "wait: ffmpeg=$NF blender=$NB load=$LD $(date +%H:%M:%S)"; sleep 30
done
$BL -b "$F" --factory-startup -noaudio --python "$S" -- "$F" "$L" >> $L/render_v12.log 2>&1
echo "DRIVER DONE exit=$? $(date +%H:%M:%S)"

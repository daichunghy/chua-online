#!/bin/bash
# V11 verification renders: chờ máy trống (ffmpeg=0, không blender lạ) rồi render tuần tự.
BL=~/workspace/vinh-trang-3d/tools/blender5/blender
F=~/workspace/chua-online-work/layout_v13_v11.blend
L=~/workspace/chua-online-work/layout
S=$L/scripts/render_one.py
wait_gap() {
  while true; do
    NF=$(pgrep -c ffmpeg || true)
    NB=$(pgrep -c -f "tools/blender5/blender" || true)
    LD=$(awk '{print $1}' /proc/loadavg)
    OK=$(awk -v l="$LD" 'BEGIN{print (l<7.0)?1:0}')
    if [ "${NF:-99}" -eq 0 ] && [ "${NB:-99}" -eq 0 ] && [ "$OK" = "1" ]; then
      echo "GAP OPEN $(date +%H:%M:%S) load=$LD"; return 0
    fi
    echo "wait: ffmpeg=$NF blender=$NB load=$LD $(date +%H:%M:%S)"; sleep 30
  done
}
for pair in "Cam_Flycam:$L/layout_v13_flycam.png" "Cam_Ground:$L/layout_v13_ground.png" "Cam_Gate:$L/layout_v13_gate.png" "Cam_V11_Facade:$L/layout_v13_facade.png" "Cam_V11_DiLac:$L/layout_v13_dilac.png"; do
  CAM="${pair%%:*}"; OUT="${pair#*:}"
  if [ -s "$OUT" ]; then echo "SKIP done $OUT"; continue; fi
  wait_gap
  echo "RENDER $CAM -> $OUT $(date +%H:%M:%S)"
  $BL -b "$F" --factory-startup -noaudio --python "$S" -- "$CAM" "$OUT" >> $L/render_v11.log 2>&1
  echo "DONE $CAM exit=$? $(date +%H:%M:%S)"
done
echo "ALL V11 RENDERS DONE"

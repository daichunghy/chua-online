#!/bin/bash
# V13 RENDER DRIVER — cho khe CPU that roi moi render (luat CPU du an).
# Ghi log vao layout/ (ben, song VM restart) thay vi /tmp.
BL=~/workspace/vinh-trang-3d/tools/blender5/blender
L=~/workspace/chua-online-work/layout
LOG=$L/render_v13_driver.log
echo "DRIVER START $(date +%H:%M:%S)" | tee -a $LOG
[ -f ~/workspace/chua-online-work/layout_v15_v13.blend ] || { echo "THIEU layout_v15_v13.blend — STOP" | tee -a $LOG; exit 1; }
count_blender() { local n=0; for p in /proc/[0-9]*; do [ "$(readlink $p/exe 2>/dev/null)" = "$HOME/workspace/vinh-trang-3d/tools/blender5/blender" ] && n=$((n+1)); done; echo $n; }
while true; do
  NF=$(pgrep -c ffmpeg || true)
  NB=$(count_blender)
  LD=$(awk '{print $1}' /proc/loadavg)
  AV=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
  OK=$(awk -v l="$LD" -v a="$AV" 'BEGIN{print (l<7.0 && a>=2200)?1:0}')
  if [ "${NF:-99}" -eq 0 ] && [ "$NB" -eq 0 ] && [ "$OK" = "1" ]; then
    echo "GAP OPEN $(date +%H:%M:%S) load=$LD availMB=$AV" | tee -a $LOG; break
  fi
  echo "wait: ffmpeg=$NF blender=$NB load=$LD availMB=$AV $(date +%H:%M:%S)" >> $LOG; sleep 60
done
echo "== RENDER FACEBASE (v14) ==" | tee -a $LOG
$BL -b --factory-startup -noaudio --python $L/scripts/render_v13.py -- ~/workspace/chua-online-work/layout_v14_v12.blend $L facebase > $L/render_v13_facebase.log 2>&1; echo "facebase exit=$?" | tee -a $LOG
echo "== RENDER FULL (v15) ==" | tee -a $LOG
$BL -b --factory-startup -noaudio --python $L/scripts/render_v13.py -- ~/workspace/chua-online-work/layout_v15_v13.blend $L full > $L/render_v13_full.log 2>&1; echo "render exit=$?" | tee -a $LOG
echo "== PIXELDIFF ==" | tee -a $LOG
python3 $L/pixeldiff_v13.py > $L/pixeldiff_v13_run.log 2>&1; cat $L/pixeldiff_v13_run.log | tee -a $LOG
ls -la $L/layout_v15_*.png $L/layout_v14_face_*.png 2>&1 | tee -a $LOG
echo "RENDER DRIVER DONE $(date +%H:%M:%S)" | tee -a $LOG

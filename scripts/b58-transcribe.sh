#!/bin/bash
# b58 短优先转录：w01–w36，与下载并行
cd /Users/chenzhiheng/Projects/video-notes
LOCKDIR=_work/b58-logs/whisper-locks
mkdir -p "$LOCKDIR" _work/b58-logs
LOG=_work/b58-logs/transcribe.log

while true; do
  next=""; next_dur=999999
  for n in $(seq 1 36); do
    k=$(printf 'w%02d' "$n")
    [ -f "$k.m4a" ] || continue
    [ -f "$k.json" ] && continue
    [ -f "$LOCKDIR/$k.lock" ] && continue
    dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
    [ -n "$dur" ] || continue
    dur=${dur:-0}
    [ "$dur" -lt 1 ] && continue
    if [ "$dur" -lt "$next_dur" ]; then next=$k; next_dur=$dur; fi
  done

  if [ -z "$next" ]; then
    done_count=$(ls w[0-9][0-9].json 2>/dev/null | wc -l | tr -d ' ')
    dl_count=$(ls w[0-9][0-9].source.mp4 2>/dev/null | wc -l | tr -d ' ')
    echo "=== 暂无可转：转录 $done_count/36，已下载 $dl_count/36 ===" | tee -a "$LOG"
    if ! pgrep -f 'b58-download.sh' >/dev/null 2>&1; then
      pending=0
      for n in $(seq 1 36); do
        k=$(printf 'w%02d' "$n")
        if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then pending=$((pending+1)); fi
      done
      if [ "$pending" -eq 0 ] && [ "$dl_count" -ge 36 ]; then
        echo "=== b58 转录结束（$done_count）===" | tee -a "$LOG"
        break
      fi
    fi
    sleep 20
    continue
  fi

  echo "=== 转录 $next (${next_dur}s) [短优先] ===" | tee -a "$LOG"
  touch "$LOCKDIR/$next.lock"
  python3 -m whisper "$next.m4a" --model medium --language Chinese --output_dir . >>"$LOG" 2>&1
  rc=$?
  rm -f "$LOCKDIR/$next.lock"
  if [ -f "$next.json" ]; then
    echo "=== $next 转录完成 ===" | tee -a "$LOG"
  else
    echo "=== $next 转录失败 rc=$rc ===" | tee -a "$LOG"
  fi
done

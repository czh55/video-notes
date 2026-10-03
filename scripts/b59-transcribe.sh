#!/bin/bash
# b59 短优先转录：x01–x71，与下载并行
# Apple Silicon 优先 MPS；遇 NaN/失败自动回退 CPU（openai-whisper + medium）
cd /Users/chenzhiheng/Projects/video-notes
LOCKDIR=_work/b59-logs/whisper-locks
FAILDIR=_work/b59-logs/whisper-fails
mkdir -p "$LOCKDIR" "$FAILDIR" _work/b59-logs
LOG=_work/b59-logs/transcribe.log
MAX_FAIL=3
TOTAL=71

run_whisper() {
  local audio=$1 device=$2
  python3 -m whisper "$audio" --model medium --language Chinese \
    --device "$device" --fp16 False --output_dir .
}

while true; do
  next=""; next_dur=999999
  for n in $(seq 1 "$TOTAL"); do
    k=$(printf 'x%02d' "$n")
    [ -f "$k.m4a" ] || continue
    [ -f "$k.json" ] && continue
    [ -f "$LOCKDIR/$k.lock" ] && continue
    fails=0
    [ -f "$FAILDIR/$k.count" ] && fails=$(cat "$FAILDIR/$k.count")
    [ "$fails" -ge "$MAX_FAIL" ] && continue
    dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
    [ -n "$dur" ] || continue
    dur=${dur:-0}
    [ "$dur" -lt 1 ] && continue
    if [ "$dur" -lt "$next_dur" ]; then next=$k; next_dur=$dur; fi
  done

  if [ -z "$next" ]; then
    done_count=$(ls x[0-9][0-9].json 2>/dev/null | wc -l | tr -d ' ')
    dl_count=$(ls x[0-9][0-9].source.mp4 2>/dev/null | wc -l | tr -d ' ')
    echo "=== 暂无可转：转录 $done_count/$TOTAL，已下载 $dl_count/$TOTAL ===" | tee -a "$LOG"
    pending=0
    for n in $(seq 1 "$TOTAL"); do
      k=$(printf 'x%02d' "$n")
      if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then
        fails=0
        [ -f "$FAILDIR/$k.count" ] && fails=$(cat "$FAILDIR/$k.count")
        [ "$fails" -lt "$MAX_FAIL" ] && pending=$((pending+1))
      fi
    done
    if [ "$pending" -eq 0 ] && [ "$dl_count" -ge "$TOTAL" ]; then
      echo "=== b59 转录结束（$done_count）===" | tee -a "$LOG"
      break
    fi
    # 下载还在跑或暂无音频：等待
    if ! pgrep -f 'b59-download.sh' >/dev/null 2>&1 && [ "$pending" -eq 0 ]; then
      echo "=== b59 转录结束（下载已停，pending=0，$done_count）===" | tee -a "$LOG"
      break
    fi
    sleep 20
    continue
  fi

  echo "=== 转录 $next (${next_dur}s) [短优先] ===" | tee -a "$LOG"
  touch "$LOCKDIR/$next.lock"
  rm -f "$next.json" "$next.tsv" "$next.vtt" "$next.srt" "$next.txt"

  ok=0
  if python3 -c 'import torch; raise SystemExit(0 if torch.backends.mps.is_available() else 1)' 2>/dev/null; then
    echo "  try device=mps" | tee -a "$LOG"
    run_whisper "$next.m4a" mps >>"$LOG" 2>&1 || true
    [ -f "$next.json" ] && ok=1
  fi
  if [ "$ok" -eq 0 ]; then
    echo "  fallback device=cpu" | tee -a "$LOG"
    run_whisper "$next.m4a" cpu >>"$LOG" 2>&1 || true
    [ -f "$next.json" ] && ok=1
  fi

  rm -f "$LOCKDIR/$next.lock"
  if [ "$ok" -eq 1 ]; then
    rm -f "$FAILDIR/$next.count"
    echo "=== $next 转录完成 ===" | tee -a "$LOG"
  else
    fails=0
    [ -f "$FAILDIR/$next.count" ] && fails=$(cat "$FAILDIR/$next.count")
    fails=$((fails+1))
    echo "$fails" > "$FAILDIR/$next.count"
    echo "=== $next 转录失败 ($fails/$MAX_FAIL) ===" | tee -a "$LOG"
  fi
done

#!/bin/bash
# b63 短优先转录：与下载并行；MPS 失败立即回退 CPU
cd /Users/chenzhiheng/Projects/video-notes
LOCKDIR=_work/b63-logs/whisper-locks
FAILDIR=_work/b63-logs/whisper-fails
mkdir -p "$LOCKDIR" "$FAILDIR" _work/b63-logs
LOG=_work/b63-logs/transcribe.log
MAX_FAIL=2
KEYS=(b63a b63b b63c b63d b63e b63f b63g b63h b63i b63j b63k b63l b63m b63n b63o b63p b63q b63r b63s b63t b63u b63v b63w b63x b63y b63z b63aa b63ab b63ac b63ad)
TOTAL=${#KEYS[@]}

run_whisper() {
  local audio=$1 device=$2
  python3 -m whisper "$audio" --model medium --language Chinese \
    --device "$device" --fp16 False --output_dir .
}

while true; do
  next=""; next_dur=999999
  for k in "${KEYS[@]}"; do
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
    done_count=0; dl_count=0
    for k in "${KEYS[@]}"; do
      [ -f "$k.json" ] && done_count=$((done_count+1))
      [ -f "$k.source.mp4" ] && dl_count=$((dl_count+1))
    done
    echo "=== 暂无可转：转录 $done_count/$TOTAL，已下载 $dl_count/$TOTAL ===" | tee -a "$LOG"
    pending=0
    for k in "${KEYS[@]}"; do
      if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then
        fails=0
        [ -f "$FAILDIR/$k.count" ] && fails=$(cat "$FAILDIR/$k.count")
        [ "$fails" -lt "$MAX_FAIL" ] && pending=$((pending+1))
      fi
    done
    if [ "$pending" -eq 0 ] && [ "$dl_count" -ge "$TOTAL" ]; then
      echo "=== b63 转录结束（$done_count）===" | tee -a "$LOG"
      break
    fi
    if ! pgrep -f 'xhs-fetch-b63.sh' >/dev/null 2>&1 && [ "$pending" -eq 0 ]; then
      echo "=== b63 转录结束（下载已停，pending=0，$done_count）===" | tee -a "$LOG"
      break
    fi
    sleep 20
    continue
  fi

  touch "$LOCKDIR/$next.lock"
  echo "=== 开始转录 $next (dur≈${next_dur}s) ===" | tee -a "$LOG"
  ok=0
  # 上次批次 MPS 常 NaN；短于 90s 直接 CPU，其余先 MPS
  device=mps
  [ "$next_dur" -lt 90 ] && device=cpu
  if run_whisper "$next.m4a" "$device" >>"$LOG" 2>&1 && [ -f "$next.json" ]; then
    ok=1
  fi
  if [ "$ok" -eq 0 ] && [ "$device" = "mps" ]; then
    echo "=== $next MPS 失败，回退 CPU ===" | tee -a "$LOG"
    rm -f "$next.json" "$next.txt" "$next.vtt" "$next.srt" "$next.tsv"
    if run_whisper "$next.m4a" cpu >>"$LOG" 2>&1 && [ -f "$next.json" ]; then
      ok=1
    fi
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

#!/bin/bash
# b64：短优先 Whisper；MPS(+fp16 False) 失败回退 CPU；可与下载并行续跑
cd /Users/chenzhiheng/Projects/video-notes
LOCKDIR=_work/b64/whisper-locks
FAILDIR=_work/b64/whisper-fails
mkdir -p "$LOCKDIR" "$FAILDIR" _work/b64
LOG=_work/b64/transcribe.log
MAX_FAIL=3
KEYS=(
  b64a b64b b64c b64d b64e b64f b64g b64h b64i b64j
  b64k b64l b64m b64n b64o b64p b64q b64r b64s b64t
  b64u b64v b64w b64x b64y b64z b64aa b64ab b64ac b64ad
  b64ae b64af b64ag b64ah b64ai b64aj
)

run_whisper() {
  local audio=$1 device=$2
  python3 -m whisper "$audio" --model medium --language Chinese \
    --device "$device" --fp16 False --output_dir .
}

echo "=== b64 转录队列启动 $(date '+%F %T') ===" | tee -a "$LOG"

# 纯图文占位
for k in "${KEYS[@]}"; do
  [ -f "$k.json" ] && continue
  [ -f "$k.meta.json" ] || continue
  kind=$(python3 -c "import json;print(json.load(open('$k.meta.json')).get('kind',''))" 2>/dev/null || true)
  if [ "$kind" = "image" ]; then
    echo '{"text":"","segments":[],"kind":"image"}' > "$k.json"
    echo "$(date '+%H:%M:%S') $k 纯图文占位" | tee -a "$LOG"
  fi
done

while true; do
  next=""; next_dur=999999
  for k in "${KEYS[@]}"; do
    [ -f "$k.m4a" ] || continue
    [ -f "$k.json" ] && continue
    [ -f "$LOCKDIR/$k.lock" ] && continue
    fails=0
    [ -f "$FAILDIR/$k.count" ] && fails=$(cat "$FAILDIR/$k.count")
    [ "$fails" -ge "$MAX_FAIL" ] && continue
    dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
    dur=${dur:-0}
    [ "$dur" -lt 1 ] && continue
    if [ "$dur" -lt "$next_dur" ]; then next=$k; next_dur=$dur; fi
  done

  if [ -z "$next" ]; then
    done_count=0; dl_count=0; pending=0
    for k in "${KEYS[@]}"; do
      [ -f "$k.json" ] && done_count=$((done_count+1))
      { [ -f "$k.m4a" ] || [ -d "$k.images" ]; } && dl_count=$((dl_count+1))
      if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then
        fails=0; [ -f "$FAILDIR/$k.count" ] && fails=$(cat "$FAILDIR/$k.count")
        [ "$fails" -lt "$MAX_FAIL" ] && pending=$((pending+1))
      fi
    done
    echo "=== 暂无可转：转录 $done_count/36，素材 $dl_count/36，pending=$pending ===" | tee -a "$LOG"
    if [ "$pending" -eq 0 ] && [ "$dl_count" -ge 36 ]; then
      echo "=== b64 转录结束 ($done_count) ===" | tee -a "$LOG"; break
    fi
    if ! pgrep -f 'xhs-fetch-b64.sh' >/dev/null 2>&1 && [ "$pending" -eq 0 ]; then
      echo "=== b64 转录结束（下载已停，$done_count）===" | tee -a "$LOG"; break
    fi
    sleep 20
    continue
  fi

  touch "$LOCKDIR/$next.lock"
  echo "=== 开始转录 $next (dur≈${next_dur}s) $(date '+%H:%M:%S') ===" | tee -a "$LOG"
  ok=0
  if run_whisper "$next.m4a" mps >>"$LOG" 2>&1; then
    [ -f "$next.json" ] && ok=1
  fi
  if [ "$ok" -eq 0 ]; then
    echo "=== $next MPS 失败，回退 CPU ===" | tee -a "$LOG"
    rm -f "$next.json" "$next.txt" "$next.vtt" "$next.srt" "$next.tsv"
    if run_whisper "$next.m4a" cpu >>"$LOG" 2>&1 && [ -f "$next.json" ]; then ok=1; fi
  fi
  rm -f "$LOCKDIR/$next.lock"
  if [ "$ok" -eq 1 ]; then
    rm -f "$FAILDIR/$next.count"
    echo "=== $next 转录完成 $(date '+%H:%M:%S') ===" | tee -a "$LOG"
  else
    fails=0; [ -f "$FAILDIR/$next.count" ] && fails=$(cat "$FAILDIR/$next.count")
    fails=$((fails+1)); echo "$fails" > "$FAILDIR/$next.count"
    echo "=== $next 转录失败 ($fails/$MAX_FAIL) ===" | tee -a "$LOG"
  fi
done

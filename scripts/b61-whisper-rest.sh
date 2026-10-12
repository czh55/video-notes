#!/bin/bash
cd "$(dirname "$0")/.."
LOG=_work/b61/whisper-rest.log
for item in \
  "future-three-valuable-jobs:Chinese" \
  "wangziru-iphone18-pro:Chinese" \
  "top10-british-drama-21c:Chinese" \
  "tesla-fsd-thirteen-years:Chinese" \
  "silicon-valley-gossip:Chinese"
do
  slug="${item%%:*}"; lang="${item##*:}"
  if [[ -f "$slug.json" ]]; then echo "skip $slug" | tee -a "$LOG"; continue; fi
  audio=""
  for e in m4a webm mp3 opus; do [[ -f "$slug.$e" ]] && audio="$slug.$e" && break; done
  [[ -n "$audio" ]] || { echo "no audio $slug" | tee -a "$LOG"; continue; }
  echo "start $slug $(date)" | tee -a "$LOG"
  python3 -m whisper "$audio" --model medium --language "$lang" --output_format all --output_dir . --device cpu >>"$LOG" 2>&1
  echo "done $slug ok=$([[ -f $slug.json ]] && echo 1 || echo 0) $(date)" | tee -a "$LOG"
done
echo ALL_WHISPER_DONE | tee -a "$LOG"

#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG=_work/b61/transcribe.log
# slug lang pairs, short first
while read -r slug lang; do
  [[ -z "$slug" ]] && continue
  if [[ -f "${slug}.json" ]]; then
    echo "skip $slug" | tee -a "$LOG"
    continue
  fi
  # wait for audio up to 2h
  for i in $(seq 1 240); do
    audio=""
    for ext in m4a webm mp3 opus; do
      [[ -f "${slug}.${ext}" ]] && audio="${slug}.${ext}" && break
    done
    [[ -n "$audio" ]] && break
    sleep 30
  done
  if [[ -z "${audio:-}" ]]; then
    echo "timeout no audio $slug" | tee -a "$LOG"
    continue
  fi
  bash scripts/b61-transcribe-one.sh "$slug" "$lang"
done <<'QUEUE'
english-doc-binge-learning	English
huberman-health-guide	Chinese
hasselblad-x2d-review	Chinese
future-three-valuable-jobs	Chinese
wangziru-iphone18-pro	Chinese
top10-british-drama-21c	Chinese
tesla-fsd-thirteen-years	Chinese
silicon-valley-gossip	Chinese
QUEUE
echo "全部转录流程结束" | tee -a "$LOG"

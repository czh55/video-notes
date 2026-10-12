#!/usr/bin/env bash
set -euo pipefail
slug="$1"
lang="${2:-Chinese}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG="_work/b61/transcribe.log"
mkdir -p _work/b61
if [[ -f "${slug}.json" ]]; then echo "skip $slug" | tee -a "$LOG"; exit 0; fi
audio=""
for ext in m4a webm mp3 opus; do
  [[ -f "${slug}.${ext}" ]] && audio="${slug}.${ext}" && break
done
[[ -n "$audio" ]] || { echo "no audio $slug" | tee -a "$LOG"; exit 1; }
echo "=== 转录 $slug lang=$lang device=cpu ===" | tee -a "$LOG"
python3 -m whisper "$audio" --model medium --language "$lang" \
  --output_format all --output_dir . --device cpu >>"$LOG" 2>&1
if [[ -f "${slug}.json" ]]; then
  echo "=== 完成转录 $slug ===" | tee -a "$LOG"
else
  echo "=== ✗ $slug ===" | tee -a "$LOG"
  exit 1
fi

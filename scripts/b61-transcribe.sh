#!/usr/bin/env bash
# b61：短片优先 Whisper medium（MPS→CPU）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG="_work/b61/transcribe.log"
mkdir -p _work/b61

# duration ascending from meta
python3 -c "
import json
from pathlib import Path
rows=sorted(json.loads(Path('_work/b61/meta.json').read_text()), key=lambda r: r.get('duration_sec') or 0)
for r in rows:
  print(r['slug'])
" | while read -r slug; do
  if [[ -f "${slug}.json" ]]; then
    echo "=== skip $slug (json exists) ===" | tee -a "$LOG"
    continue
  fi
  audio=""
  for ext in m4a webm mp3 opus; do
    if [[ -f "${slug}.${ext}" ]]; then audio="${slug}.${ext}"; break; fi
  done
  if [[ -z "$audio" ]]; then
    echo "=== wait $slug (no audio yet) ===" | tee -a "$LOG"
    continue
  fi
  echo "=== 转录 $slug ($audio) ===" | tee -a "$LOG"
  if python3 -c "import torch; assert torch.backends.mps.is_available()" 2>/dev/null; then
    DEVICE=mps
  else
    DEVICE=cpu
  fi
  # try MPS first; on failure CPU
  set +e
  whisper "$audio" --model medium --language Chinese --output_format all \
    --output_dir . --device "$DEVICE" >>"$LOG" 2>&1
  rc=$?
  set -e
  if [[ $rc -ne 0 && "$DEVICE" == mps ]]; then
    echo "  MPS fail → CPU" | tee -a "$LOG"
    whisper "$audio" --model medium --language Chinese --output_format all \
      --output_dir . --device cpu >>"$LOG" 2>&1 || echo "  ✗ $slug fail" | tee -a "$LOG"
  fi
  if [[ -f "${slug}.json" ]]; then
    echo "=== 完成转录 $slug ===" | tee -a "$LOG"
  else
    echo "=== ✗ 无 json $slug ===" | tee -a "$LOG"
  fi
done
echo "全部转录流程结束" | tee -a "$LOG"

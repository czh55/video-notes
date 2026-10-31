#!/usr/bin/env bash
# b66 视频 Whisper 队列：短优先
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG=_work/b66/whisper-queue.log
mkdir -p _work/b66

# 收集视频：duration 升序
python3 - <<'PY' > _work/b66/whisper-queue.txt
import json
from pathlib import Path
items=[]
for line in Path('_work/b66/manifest.tsv').read_text().splitlines()[1:]:
    if not line.strip(): continue
    key,slug,*_=line.split('\t')
    meta=Path(f'_work/b66/{key}/{slug}.meta.json')
    if not meta.exists():
        continue
    m=json.loads(meta.read_text())
    if m.get('kind')!='video':
        continue
    audio=Path(f'_work/b66/{key}/{slug}.m4a')
    out=Path(f'_work/b66/{key}/{slug}.json')
    if out.exists() and out.stat().st_size>100:
        continue
    # duration from ffprobe if meta duration_ms looks wrong (<1000 often means seconds mislabeled as ms)
    dur=m.get('duration_ms') or 0
    if dur and dur < 5000:
        # likely seconds stored as ms field
        dur=dur
    else:
        dur=dur/1000 if dur>5000 else dur
    items.append((dur or 9999, key, slug, str(audio)))
for dur,key,slug,audio in sorted(items):
    print(f'{dur}\t{key}\t{slug}\t{audio}')
PY

echo "=== whisper queue start $(date) ===" | tee "$LOG"
while IFS=$'\t' read -r dur key slug audio; do
  outdir="_work/b66/$key"
  out="$outdir/$slug.json"
  lock="$outdir/$slug.whisper.lock"
  if [[ -f "$out" && $(wc -c <"$out") -gt 100 ]]; then
    echo "=== skip $key ===" | tee -a "$LOG"
    continue
  fi
  mkdir -p "$outdir"
  echo "=== whisper $key dur~${dur}s ===" | tee -a "$LOG"
  date > "$lock"
  if python3 -m whisper "$audio" --model medium --language Chinese \
      --output_dir "$outdir" --output_format json 2>&1 | tee -a "$LOG"; then
    echo "=== ok $key ===" | tee -a "$LOG"
  else
    echo "=== retry CPU $key ===" | tee -a "$LOG"
    python3 -m whisper "$audio" --model medium --language Chinese --fp16 False \
      --device cpu --output_dir "$outdir" --output_format json 2>&1 | tee -a "$LOG" || echo "=== FAIL $key ===" | tee -a "$LOG"
  fi
  rm -f "$lock"
done < _work/b66/whisper-queue.txt
echo "=== whisper 全部结束 $(date) ===" | tee -a "$LOG"

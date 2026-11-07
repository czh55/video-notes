#!/usr/bin/env bash
# b67 Whisper 队列：短优先
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG=_work/b67/whisper-queue.log
mkdir -p _work/b67

python3 - <<'PY' > _work/b67/whisper-queue.txt
import json, subprocess
from pathlib import Path
items=[]
for line in Path('_work/b67/manifest.tsv').read_text().splitlines()[1:]:
    if not line.strip(): continue
    key,slug,*_=line.split('\t')
    meta=Path(f'_work/b67/{key}/{slug}.meta.json')
    if not meta.exists():
        continue
    m=json.loads(meta.read_text())
    if m.get('kind')!='video':
        continue
    out=Path(f'_work/b67/{key}/{slug}.json')
    if out.exists() and out.stat().st_size>100:
        continue
    audio=Path(f'_work/b67/{key}/{slug}.m4a')
    if not audio.exists():
        continue
    try:
        dur=float(subprocess.check_output(
            ['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)],
            text=True).strip())
    except Exception:
        dur=float(m.get('duration_ms') or 999)
        if dur>5000: dur/=1000
    items.append((dur,key,slug,str(audio)))
for t in sorted(items):
    print(f'{t[0]:.0f}\t{t[1]}\t{t[2]}\t{t[3]}')
print('count', len(items), file=__import__('sys').stderr)
PY

echo "=== whisper queue start $(date) ===" | tee "$LOG"
while IFS=$'\t' read -r dur key slug audio; do
  outdir="_work/b67/$key"
  out="$outdir/$slug.json"
  if [[ -f "$out" && $(wc -c <"$out") -gt 100 ]]; then
    echo "=== skip $key ===" | tee -a "$LOG"
    continue
  fi
  echo "=== whisper $key dur~${dur}s ===" | tee -a "$LOG"
  if python3 -m whisper "$audio" --model medium --language Chinese \
      --output_dir "$outdir" --output_format json 2>&1 | tee -a "$LOG"; then
    echo "=== ok $key ===" | tee -a "$LOG"
  else
    echo "=== retry CPU $key ===" | tee -a "$LOG"
    python3 -m whisper "$audio" --model medium --language Chinese --fp16 False \
      --device cpu --output_dir "$outdir" --output_format json 2>&1 | tee -a "$LOG" \
      || echo "=== FAIL $key ===" | tee -a "$LOG"
  fi
done < _work/b67/whisper-queue.txt
echo "=== whisper 全部结束 $(date) ===" | tee -a "$LOG"

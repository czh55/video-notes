#!/usr/bin/env bash
# b61：下载剩余 B 站条目（短片优先，已存在跳过）
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG="_work/b61/download.log"
mkdir -p _work/b61
echo "=== 续跑 $(date) ===" >> "$LOG"

python3 -c "
import json
from pathlib import Path
rows=sorted(json.loads(Path('_work/b61/meta.json').read_text()), key=lambda r: r.get('duration_sec') or 0)
for row in rows:
  print(row['slug'] + '\t' + row['url'])
" > _work/b61/queue.tsv

while IFS=$'\t' read -r slug url; do
  echo "=== 开始 $slug ===" | tee -a "$LOG"
  has_audio=0
  for ext in m4a webm mp3 opus; do
    if [[ -f "${slug}.${ext}" ]]; then has_audio=1; break; fi
  done
  if [[ $has_audio -eq 1 ]]; then
    echo "  音频已存在，跳过" | tee -a "$LOG"
  else
    if yt-dlp --no-update -f "bestaudio[ext=m4a]/bestaudio/best" --no-playlist -o "${slug}.%(ext)s" "$url" >>"$LOG" 2>&1; then
      echo "  ✓ 音频" | tee -a "$LOG"
    else
      echo "  ✗ 音频失败" | tee -a "$LOG"
    fi
  fi
  has_video=0
  for f in "${slug}".source.*; do
    if [[ -f "$f" && "$f" != *.part ]]; then has_video=1; break; fi
  done
  if [[ $has_video -eq 1 ]]; then
    echo "  视频已存在，跳过" | tee -a "$LOG"
  else
    if yt-dlp --no-update -f "bestvideo[height<=1080][ext=mp4]/bestvideo[height<=1080]/best[height<=1080]" --no-playlist -o "${slug}.source.%(ext)s" "$url" >>"$LOG" 2>&1; then
      echo "  ✓ 视频" | tee -a "$LOG"
    else
      echo "  ✗ 视频失败" | tee -a "$LOG"
    fi
  fi
  python3 - "$slug" "$url" <<'PY'
import json, sys
from pathlib import Path
slug, url = sys.argv[1], sys.argv[2]
meta = json.loads(Path('_work/b61/meta.json').read_text())
row = next(x for x in meta if x['slug'] == slug)
Path(f'{slug}.meta.json').write_text(json.dumps({
  'id': row.get('id'),
  'title': row.get('title'),
  'duration_sec': row.get('duration_sec'),
  'url': url,
  'webpage_url': row.get('webpage_url'),
  'platform': 'bilibili',
}, ensure_ascii=False, indent=2), encoding='utf-8')
PY
  echo "=== 完成 $slug ===" | tee -a "$LOG"
done < _work/b61/queue.tsv

echo "全部下载流程结束" | tee -a "$LOG"

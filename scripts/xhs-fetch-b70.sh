#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MANIFEST="_work/b70/manifest.tsv"
LOG="_work/b70/xhs-fetch.log"
SITE="/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/lib/python3.14/site-packages"
mkdir -p _work/b70
TMPDIR_NODE="$(node -e 'console.log(require("os").tmpdir())')"
rm -f "$TMPDIR_NODE"/video-notes-xhs-last-request* 2>/dev/null || true

echo "=== b70 xhs fetch start $(date) ===" | tee "$LOG"
tail -n +2 "$MANIFEST" | while IFS=$'\t' read -r key slug title url platform; do
  [[ "$platform" == "xiaohongshu" ]] || continue
  out="_work/b70/$key/$slug"
  mkdir -p "_work/b70/$key"
  if [[ -f "${out}.meta.json" ]]; then
    echo "=== skip existing $key $slug ===" | tee -a "$LOG"
    continue
  fi
  echo "=== fetch $key $slug ===" | tee -a "$LOG"
  if PYTHONPATH="$SITE" /opt/homebrew/bin/python3 scripts/xhs-fetch.py "$url" "$out" 2>&1 | tee -a "$LOG"; then
    echo "=== 完成 $key ===" | tee -a "$LOG"
  else
    echo "=== FAIL $key ===" | tee -a "$LOG"
  fi
done
echo "=== 全部下载流程结束 $(date) ===" | tee -a "$LOG"

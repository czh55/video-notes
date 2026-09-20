#!/bin/bash
# b58：36（前缀 w01-w36，避免与旧 k* 冲突） 条小红书视频串行下载（xhs-fetch 内置 60s 限流）
# 注意：必须用独立 fd 读列表，避免 xhs-fetch 内部 ffmpeg 吞掉 while-read 的 stdin。
cd /Users/chenzhiheng/Projects/video-notes
mkdir -p _work/b58-logs
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
[ -x "$PY" ] || PY=python3

python3 << 'PY'
import json
from pathlib import Path
mp=json.loads(Path('scripts/b58-slug-map.json').read_text())
keys=sorted(mp.keys(), key=lambda k:int(k[1:]))
Path('/tmp/b58-download.list').write_text('\n'.join(f"{k}\t{mp[k]['url']}" for k in keys)+'\n')
print('queued', len(keys))
PY

LOG=_work/b58-logs/download.log
: > "$LOG"
while IFS=$'\t' read -r k u <&3; do
  [ -z "$k" ] && continue
  if [ -f "$k.source.mp4" ] && [ -s "$k.source.mp4" ] && [ -f "$k.meta.json" ]; then
    echo "=== $k 已存在，跳过 ===" | tee -a "$LOG"
    continue
  fi
  echo "=== 开始 $k $u ===" | tee -a "$LOG"
  "$PY" scripts/xhs-fetch.py "$u" "$k" </dev/null >>"$LOG" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "=== $k 失败 (rc=$rc)，继续下一个 ===" | tee -a "$LOG"
  else
    echo "=== $k 完成 ===" | tee -a "$LOG"
  fi
done 3< /tmp/b58-download.list
echo "=== 全部下载流程结束 ===" | tee -a "$LOG"

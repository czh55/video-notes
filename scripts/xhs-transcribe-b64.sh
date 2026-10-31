#!/bin/bash
# b64: 轮询已下载的 m4a，串行 Whisper medium 中文转录（可续跑）
cd /Users/chenzhiheng/Projects/video-notes
PY=python3
LOG=_work/b64/transcribe.log
mkdir -p _work/b64

KEYS=(
  b64a b64b b64c b64d b64e b64f b64g b64h b64i b64j
  b64k b64l b64m b64n b64o b64p b64q b64r b64s b64t
  b64u b64v b64w b64x b64y b64z b64aa b64ab b64ac b64ad
  b64ae b64af b64ag b64ah b64ai b64aj
)

echo "=== 转录监视启动 $(date '+%F %T') ===" | tee -a "$LOG"

# 最多等下载 3 小时；每 30 秒扫一轮
deadline=$((SECONDS + 10800))
while (( SECONDS < deadline )); do
  pending=0
  done_n=0
  missing=0
  for k in "${KEYS[@]}"; do
    if [ -f "$k.json" ]; then
      done_n=$((done_n+1))
      continue
    fi
    if [ -f "$k.meta.json" ]; then
      kind=$(python3 -c "import json;print(json.load(open('$k.meta.json')).get('kind',''))" 2>/dev/null || echo "")
      if [ "$kind" = "image" ]; then
        # 纯图文：写空占位，跳过 whisper
        echo '{"segments":[],"text":"","kind":"image"}' > "$k.json"
        echo "$(date '+%H:%M:%S') $k 纯图文，跳过转录" | tee -a "$LOG"
        done_n=$((done_n+1))
        continue
      fi
    fi
    if [ -f "$k.m4a" ] && [ -s "$k.m4a" ]; then
      pending=$((pending+1))
      echo "$(date '+%H:%M:%S') 开始转录 $k" | tee -a "$LOG"
      if $PY -m whisper "$k.m4a" --model medium --language Chinese --output_dir . >>"_work/b64/whisper-$k.log" 2>&1; then
        echo "$(date '+%H:%M:%S') 完成转录 $k" | tee -a "$LOG"
      else
        echo "$(date '+%H:%M:%S') FAILED 转录 $k" | tee -a "$LOG"
      fi
    else
      missing=$((missing+1))
    fi
  done
  echo "$(date '+%H:%M:%S') 进度: 已转录=$done_n 本轮待转已消化 仍缺媒体≈$missing" | tee -a "$LOG"
  if [ "$done_n" -ge 36 ]; then
    echo "=== 全部转录结束 $(date '+%F %T') ===" | tee -a "$LOG"
    exit 0
  fi
  # 若下载进程还在或仍缺文件，继续等
  if ! kill -0 "$(cat _work/b64/fetch.pid 2>/dev/null)" 2>/dev/null && [ "$missing" -eq 0 ] && [ "$pending" -eq 0 ]; then
    # 下载已结束且没有可转的
    left=0
    for k in "${KEYS[@]}"; do
      [ -f "$k.json" ] || left=$((left+1))
    done
    if [ "$left" -eq 0 ]; then
      echo "=== 全部转录结束 $(date '+%F %T') ===" | tee -a "$LOG"
      exit 0
    fi
    echo "$(date '+%H:%M:%S') 下载已停且还有 $left 未转录（可能失败），继续等待/重试..." | tee -a "$LOG"
  fi
  sleep 30
done
echo "=== 转录监视超时退出 $(date '+%F %T') ===" | tee -a "$LOG"
exit 1

#!/bin/bash
# b64: 36 条小红书笔记（跳过主页口令 KclvK8FG7O）
# 串行下载；xhs-fetch.py 内置 ≥60s 限流；已下载跳过
cd /Users/chenzhiheng/Projects/video-notes
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
mkdir -p _work/b64
LOG=_work/b64/fetch.log

KEYS=(
  b64a b64b b64c b64d b64e b64f b64g b64h b64i b64j
  b64k b64l b64m b64n b64o b64p b64q b64r b64s b64t
  b64u b64v b64w b64x b64y b64z b64aa b64ab b64ac b64ad
  b64ae b64af b64ag b64ah b64ai b64aj
)
URLS=(
  "https://xhslink.cn/o/4tMqSctgKmt"
  "https://xhslink.cn/o/1ngmMeddK1M"
  "https://xhslink.cn/o/A7lDzmntKaD"
  "https://xhslink.cn/o/1FnZTYTSaUG"
  "https://xhslink.cn/o/48CRkDUg849"
  "https://xhslink.cn/o/1X2T1UKqqEb"
  "https://xhslink.cn/o/AD8TBAgdvP8"
  "https://xhslink.cn/o/5SeFEOHj4qE"
  "https://xhslink.cn/o/sK5aFXRe3m"
  "https://xhslink.cn/o/9DZLKSaOEkU"
  "https://xhslink.cn/o/5PXdltZoVZJ"
  "https://xhslink.cn/o/8L4ra1jfEhb"
  "https://xhslink.cn/o/5zJTLtIbqH7"
  "https://xhslink.cn/o/2XLD0JgXrAd"
  "https://xhslink.cn/o/48z0TItS9wU"
  "https://xhslink.cn/o/2f6uX6Xctsl"
  "https://xhslink.cn/o/6LdGjmMTIU0"
  "https://xhslink.cn/o/6FSoHuDuWno"
  "https://xhslink.cn/o/6U6T6V4PbWo"
  "https://xhslink.cn/o/X4LRot2mTw"
  "https://xhslink.cn/o/3wPb54D9oDv"
  "https://xhslink.cn/o/2ZkBNL6O1Pa"
  "https://xhslink.cn/o/9hOkRPt9YiM"
  "https://xhslink.cn/o/Fwv2YVukF2"
  "https://xhslink.cn/o/6XWbCSDrhlf"
  "https://xhslink.cn/o/2GYRWcyrpnL"
  "https://xhslink.cn/o/3gZ3qFDN7Db"
  "https://xhslink.cn/o/4lAB5TCaBRN"
  "https://xhslink.cn/o/6meYgtVDtie"
  "https://xhslink.cn/o/4PIRD7SqXoE"
  "https://xhslink.cn/o/39NlChj46LH"
  "https://xhslink.cn/o/A9Pv8Tfw7ss"
  "https://xhslink.cn/o/29WcZDwiL1u"
  "https://xhslink.cn/o/2dQtePzZVtk"
  "https://xhslink.cn/o/3Py5TYjEBWQ"
  "https://xhslink.cn/o/sRfGFdqPur"
)

for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"
  u="${URLS[$i]}"
  if { [ -f "$k.source.mp4" ] && [ -s "$k.source.mp4" ]; } || { [ -f "$k.meta.json" ] && [ -d "$k.images" ]; }; then
    echo "=== $k 已存在，跳过 ===" | tee -a "$LOG"
    continue
  fi
  echo "=== 下载 $k ($(date '+%H:%M:%S')): $u ===" | tee -a "$LOG"
  if "$PY" scripts/xhs-fetch.py "$u" "$k" >>"$LOG" 2>&1; then
    echo "=== 完成 $k ($(date '+%H:%M:%S')) ===" | tee -a "$LOG"
  else
    echo "=== FAILED $k ($(date '+%H:%M:%S')) ===" | tee -a "$LOG"
  fi
done
echo "全部下载流程结束 $(date '+%F %T')" | tee -a "$LOG"

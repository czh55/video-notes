#!/bin/bash
# b63: 30 条小红书（调色/摄影/达芬奇/咖啡/交通/色彩理论）
# 串行下载；xhs-fetch.py 内置 ≥60s 限流
# 跳过无效占位 ${shortLink}（HDR 美图那条没有真实短链）
cd /Users/chenzhiheng/Projects/video-notes
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
KEYS=(b63a b63b b63c b63d b63e b63f b63g b63h b63i b63j b63k b63l b63m b63n b63o b63p b63q b63r b63s b63t b63u b63v b63w b63x b63y b63z b63aa b63ab b63ac b63ad)
URLS=(
  "https://xhslink.cn/o/4iDuuR7qpky"
  "https://xhslink.cn/o/3YrcDPLbxuV"
  "https://xhslink.cn/o/70j1EK4SRam"
  "https://xhslink.cn/o/3NwL5fkSLdy"
  "https://xhslink.cn/o/1QgaN67DeYr"
  "https://xhslink.cn/o/7yOqZxZLceu"
  "https://xhslink.cn/o/4YPSI90okhB"
  "https://xhslink.cn/o/5m4QIfHp8Tv"
  "https://xhslink.cn/o/8vxnZyVNm0x"
  "https://xhslink.cn/o/1hNULWifpqJ"
  "https://xhslink.cn/o/6tVAgiVjlMw"
  "https://xhslink.cn/o/Am1z2LwXreI"
  "https://xhslink.cn/o/6XOwp1kWqk3"
  "https://xhslink.cn/o/1axLmWPV9SD"
  "https://xhslink.cn/o/2NZLPLALcGO"
  "https://xhslink.cn/o/8suSjGp4VYS"
  "https://xhslink.cn/o/1AzF6rt6KhS"
  "https://xhslink.cn/o/1zRoaWoT9fL"
  "https://xhslink.cn/o/1zcCCkVKYIC"
  "https://xhslink.cn/o/24DgBwrAEkw"
  "https://xhslink.cn/o/1RB1oFws9GA"
  "https://xhslink.cn/o/3u4zeIyI0lZ"
  "https://xhslink.cn/o/90O6lV5bFoE"
  "https://xhslink.cn/o/9Qzw5phJtQ8"
  "https://xhslink.cn/o/8Fly8YgeIqT"
  "https://xhslink.cn/o/8zaimOs6of3"
  "https://xhslink.cn/o/3Zwy0y18ASR"
  "https://xhslink.cn/o/8gS4Epeyfk2"
  "https://xhslink.cn/o/6EowgCrjfdz"
  "https://xhslink.cn/o/9JUKYkdxjhF"
)
for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"
  u="${URLS[$i]}"
  if [ -f "$k.source.mp4" ] && [ -s "$k.source.mp4" ]; then
    echo "=== $k 已存在，跳过 ==="
    continue
  fi
  echo "=== 下载 $k: $u ==="
  "$PY" scripts/xhs-fetch.py "$u" "$k" || echo "FAILED: $k"
  echo "=== 完成 $k ==="
done
echo "全部下载流程结束"

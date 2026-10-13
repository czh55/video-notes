#!/bin/bash
# b62: 20 条小红书（汽车/手机/英语/咖啡经营/表达/摄影/地图/舞蹈）
# 串行下载；xhs-fetch.py 内置 ≥60s 限流
cd /Users/chenzhiheng/Projects/video-notes
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
KEYS=(b62a b62b b62c b62d b62e b62f b62g b62h b62i b62j b62k b62l b62m b62n b62o b62p b62q b62r b62s b62t)
URLS=(
  "https://xhslink.cn/o/9EMVTLEXPcN"
  "https://xhslink.cn/o/6GrB9slekhu"
  "https://xhslink.cn/o/1zY9O3Ur17C"
  "https://xhslink.cn/o/2ZHWNtP6QqN"
  "https://xhslink.cn/o/3ncye3zBuDz"
  "https://xhslink.cn/o/5PtNH1qUAEN"
  "https://xhslink.cn/o/3sv78FfB0sR"
  "https://xhslink.cn/o/Axsh7cqF0dz"
  "https://xhslink.cn/o/3KvyJWICIkc"
  "https://xhslink.cn/o/72V75eiXrkN"
  "https://xhslink.cn/o/67nH0AbT7Xd"
  "https://xhslink.cn/o/5kT10zg9OBj"
  "https://xhslink.cn/o/8oHA2m5BWWP"
  "https://xhslink.cn/o/3ia9NIz5I2O"
  "https://xhslink.cn/o/53Yg0UDxRtr"
  "https://xhslink.cn/o/8hOsu422nrh"
  "https://xhslink.cn/o/8itigYhyWET"
  "https://xhslink.cn/o/4IB76GeYLwk"
  "https://xhslink.cn/o/2Ii0OJvl8V7"
  "https://xhslink.cn/o/4MYY2B7sKqa"
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

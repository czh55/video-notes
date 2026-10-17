#!/usr/bin/env python3
"""小红书笔记抓取：短链 → 展开 → 抓页面 → 按笔记类型下载。

绕过 yt-dlp XiaoHongShu 提取器失效问题（小红书改版后 __INITIAL_STATE__ 顶层结构
从 note.noteDetailMap 变为 noteData.data.noteData，yt-dlp 2026.07.04 未适配）。

用法：
  python3 scripts/xhs-fetch.py {short_url} {out_prefix} [--no-rate-limit]
  例如：python3 scripts/xhs-fetch.py http://xhslink.cn/o/8bnTzqVAMvT white-balance

视频笔记输出：
  {out_prefix}.source.mp4   (≤1080p 视频)
  {out_prefix}.m4a          (抽取的音频)
  {out_prefix}.meta.json    (kind=video)

纯图文笔记（type=normal，或没有视频直链但有 imageList）输出：
  {out_prefix}.images/01.jpg …   (按笔记顺序的全部原图，不抽选)
  {out_prefix}.images/manifest.json
  {out_prefix}.meta.json    (kind=image)

限流：默认在请求前执行仓库根的 xhs-rate-limit.mjs（两次小红书请求开始时间间隔 ≥60 秒）。
图片文件在 CDN，下载本身不额外占页面限流额度。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATE_LIMIT = ROOT / "xhs-rate-limit.mjs"

UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
      "Mobile/15E148 Safari/604.1")


def pick_image_url(item: dict) -> str:
    """优先清晰图 WB_DFT，其次原图，再次预览图。"""
    info = item.get("infoList") or []
    by_scene = {row.get("imageScene"): row.get("url") for row in info if isinstance(row, dict)}
    for scene in ("WB_DFT", "WB_ORG", "WB_PRV"):
        url = by_scene.get(scene) or ""
        if url:
            return url
    return item.get("urlDefault") or item.get("url") or item.get("urlPre") or ""


def curl_to(url: str, dest: Path, timeout: int) -> None:
    dl = subprocess.run(
        ["curl", "-fsSL", "-A", UA, "-H", "Referer: https://www.xiaohongshu.com/",
         "-o", str(dest), url],
        capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)
    if dl.returncode != 0 or not dest.exists() or dest.stat().st_size < 500:
        err = dl.stderr.decode("utf-8", errors="replace")[:200]
        raise SystemExit(f"下载失败 {dest.name} rc={dl.returncode} {err}")


def to_jpeg(src: Path, dest: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-frames:v", "1", "-q:v", "3", str(dest)],
        check=True, stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def download_image_note(note: dict, prefix: Path, display_id: str, final_url: str) -> None:
    images = [item for item in (note.get("imageList") or []) if isinstance(item, dict)]
    if not images:
        raise SystemExit("纯图文笔记没有 imageList")
    img_dir = prefix.with_name(prefix.name + ".images")
    img_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for i, item in enumerate(images, start=1):
        url = pick_image_url(item)
        if not url:
            raise SystemExit(f"第 {i} 张图没有可用 URL")
        raw = img_dir / f"{i:02d}.bin"
        jpg = img_dir / f"{i:02d}.jpg"
        curl_to(url, raw, timeout=120)
        to_jpeg(raw, jpg)
        raw.unlink(missing_ok=True)
        manifest.append({
            "index": i,
            "file": jpg.name,
            "width": item.get("width"),
            "height": item.get("height"),
            "url": url,
        })
        print(f"图片 {i}/{len(images)}: {jpg.name} {jpg.stat().st_size/1e3:.0f} KB")
    (img_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    user = note.get("user", {})
    meta = {
        "kind": "image",
        "id": display_id,
        "title": note.get("title", ""),
        "desc": note.get("desc", "")[:500],
        "image_count": len(manifest),
        "images_dir": img_dir.name,
        "uploader": user.get("nickName", "") or user.get("nickname", ""),
        "uploader_id": user.get("userId", ""),
        "url": final_url,
    }
    prefix.with_name(prefix.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"图文笔记: {meta['title'][:60]} | {meta['image_count']} 张 | 作者 {meta['uploader']}")


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        raise SystemExit(__doc__)
    no_rate_limit = "--no-rate-limit" in args
    args = [a for a in args if a != "--no-rate-limit"]
    no_audio = "--no-audio" in args
    args = [a for a in args if a != "--no-audio"]
    short_url, prefix_str = args[0], args[1]
    prefix = Path(prefix_str)

    if not no_rate_limit:
        subprocess.run(["node", str(RATE_LIMIT)], check=True, stdin=subprocess.DEVNULL)

    # 1. 展开短链（跟随跳转直接拿页面，一次请求）
    out = subprocess.run(
        ["curl", "-s", "-L", "-A", UA, "-H", "Referer: https://www.xiaohongshu.com/",
         "-w", "\n__FINAL_URL__%{url_effective}",
         short_url], capture_output=True, timeout=90,
        stdin=subprocess.DEVNULL)
    body = out.stdout.decode("utf-8", errors="replace")
    if "__FINAL_URL__" in body:
        html, _, tail = body.rpartition("__FINAL_URL__")
        final_url = tail.strip()
    else:
        html, final_url = body, short_url
    print(f"展开: {final_url[:120]}")

    display_id = "unknown"
    note_id = re.search(r"/item/([0-9a-f]{20,40})", final_url)
    if note_id:
        display_id = note_id.group(1)

    m = re.search(r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\});?\s*</script>", html, re.S)
    if not m:
        raise SystemExit("页面中未找到 __INITIAL_STATE__")
    raw = m.group(1)
    try:
        state = json.loads(raw)
    except json.JSONDecodeError:
        import yt_dlp.utils as u
        state = json.loads(u.js_to_json(raw))

    note = state.get("noteData", {}).get("data", {}).get("noteData", {})
    if not note:
        for k, v in state.get("note", {}).get("noteDetailMap", {}).items():
            if isinstance(v, dict) and "note" in v:
                note = v["note"]
                display_id = k
                break
    if not note:
        raise SystemExit(f"未找到笔记数据。state 顶层 keys={list(state.keys())}")
    display_id = note.get("noteId") or note.get("id") or display_id

    video = note.get("video") or {}
    stream = video.get("media", {}).get("stream", {}) or video.get("stream", {}) or {}
    streams = stream.get("h264", []) or stream.get("h265", []) or []
    master_url = next((s["masterUrl"] for s in streams if isinstance(s, dict) and s.get("masterUrl")), None)
    note_type = note.get("type") or ""
    image_list = note.get("imageList") or []
    # type=normal，或没有视频直链但带图：整本笔记都是图片，全部下载。
    if note_type == "normal" or (not master_url and image_list):
        download_image_note(note, prefix, display_id, final_url)
        return
    if not master_url:
        raise SystemExit(f"未找到 masterUrl，也没有 imageList。stream keys={list(stream.keys())}")

    capa = video.get("capa", {}) or video.get("media", {}).get("capa", {})
    user = note.get("user", {})
    meta = {
        "kind": "video",
        "id": display_id,
        "title": note.get("title", ""),
        "desc": note.get("desc", "")[:200],
        "duration_ms": capa.get("duration"),
        "uploader": user.get("nickName", "") or user.get("nickname", ""),
        "uploader_id": user.get("userId", ""),
        "master_url": master_url,
        "url": final_url,
    }
    prefix.with_name(prefix.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"笔记: {meta['title'][:60]} | 时长 {meta['duration_ms']}ms | 作者 {meta['uploader']}")

    # 2. 下载视频（curl，带 Referer）
    src = prefix.with_name(prefix.name + ".source.mp4")
    dl = subprocess.run(
        ["curl", "-s", "-A", UA, "-H", "Referer: https://www.xiaohongshu.com/",
         "-o", str(src), master_url], capture_output=True, timeout=300,
        stdin=subprocess.DEVNULL)
    if dl.returncode != 0 or not src.exists() or src.stat().st_size < 1000:
        raise SystemExit(f"视频下载失败 rc={dl.returncode}")
    print(f"视频: {src.name} {src.stat().st_size/1e6:.1f} MB")

    # 3. 抽音频（--no-audio 时跳过，便于外部脚本手动处理）
    m4a = prefix.with_name(prefix.name + ".m4a")
    if not no_audio:
        subprocess.run(["ffmpeg", "-y", "-i", str(src), "-vn", "-acodec", "aac",
                        "-b:a", "128k", str(m4a)], check=True,
                       stdin=subprocess.DEVNULL,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"音频: {m4a.name} 完成")


if __name__ == "__main__":
    main()

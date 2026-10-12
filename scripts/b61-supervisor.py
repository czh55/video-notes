#!/usr/bin/env python3
"""b61：短片优先，每条 audio→video→whisper(CPU)，可续跑。"""
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "_work/b61/supervisor.log"
LOG.parent.mkdir(parents=True, exist_ok=True)

def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def has_audio(slug: str):
    for ext in ("m4a", "webm", "mp3", "opus"):
        p = ROOT / f"{slug}.{ext}"
        if p.exists() and p.stat().st_size > 1000:
            return p
    return None

def has_video(slug: str) -> bool:
    for p in ROOT.glob(f"{slug}.source.*"):
        if not str(p).endswith(".part") and p.stat().st_size > 1000:
            return True
    return False

def ytdlp(args):
    return subprocess.run(["yt-dlp", "--no-update", *args], cwd=ROOT).returncode

def lang_for(slug, title):
    if slug in ("language-shapes-thinking", "english-doc-binge-learning"):
        return "English"
    if "全英" in (title or "") or "英文纪录片" in (title or ""):
        return "English"
    return "Chinese"

def process(row):
    slug, url = row["slug"], row["url"]
    title = row.get("title") or ""
    log(f"=== item {slug} ({row.get('duration_sec',0)}s) ===")
    if not has_audio(slug):
        log(f"DL audio {slug}")
        log(f"audio rc={ytdlp(['-f','bestaudio[ext=m4a]/bestaudio/best','--no-playlist','-o',f'{slug}.%(ext)s',url])} {slug}")
    else:
        log(f"audio skip {slug}")
    if not has_video(slug):
        log(f"DL video {slug}")
        log(f"video rc={ytdlp(['-f','bestvideo[height<=1080][ext=mp4]/bestvideo[height<=1080]/best[height<=1080]','--no-playlist','-o',f'{slug}.source.%(ext)s',url])} {slug}")
    else:
        log(f"video skip {slug}")
    (ROOT / f"{slug}.meta.json").write_text(json.dumps({
        "id": row.get("id"), "title": title, "duration_sec": row.get("duration_sec"),
        "url": url, "webpage_url": row.get("webpage_url"), "platform": "bilibili",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    if (ROOT / f"{slug}.json").exists():
        log(f"whisper skip {slug}"); return
    audio = has_audio(slug)
    if not audio:
        log(f"whisper no-audio {slug}"); return
    lang = lang_for(slug, title)
    log(f"whisper start {slug} {lang}")
    r = subprocess.run([sys.executable, "-m", "whisper", str(audio),
        "--model", "medium", "--language", lang, "--output_format", "all",
        "--output_dir", str(ROOT), "--device", "cpu"], cwd=ROOT)
    log(f"whisper done {slug} rc={r.returncode} ok={(ROOT/f'{slug}.json').exists()}")

def main():
    rows = sorted(json.loads((ROOT/"_work/b61/meta.json").read_text()), key=lambda r: r.get("duration_sec") or 0)
    log(f"supervisor start n={len(rows)}")
    for row in rows:
        try:
            process(row)
        except Exception as e:
            log(f"ERROR {row.get('slug')}: {e}")
    log("全部监督流程结束")

if __name__ == "__main__":
    main()

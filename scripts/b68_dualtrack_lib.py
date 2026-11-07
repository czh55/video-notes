#!/usr/bin/env python3
"""b68 双轨公共脚手架：SVG build / translations / index-entry / enhance / caption audio。"""
from __future__ import annotations

import asyncio
import hashlib
import json
import subprocess
from pathlib import Path
import html as html_mod

ROOT = Path(__file__).resolve().parents[1]

SVG_CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
p,li{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul{padding-left:24px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px;background:#dbeafe;color:#1e40af}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin:20px 0;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.card{background:#fff;border-radius:16px;padding:28px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #3b82f6}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card .action{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
.card .bound{background:#f0fdf4;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#166534;border-left:4px solid #22c55e}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2)}
.conclusion p,.conclusion li{color:rgba(255,255,255,.92)}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}"""

HTML_CSS = """*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
.container{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}
header h1{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}
.meta-row{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.meta-tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}
.tag-platform{background:#ff2442;color:#fff}.tag-duration{background:#f1f5f9;color:#64748b}.tag-topic{background:#dbeafe;color:#1e40af}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none}
.toc{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.toc h3{font-size:16px;color:#1e40af;margin:0 0 12px}.toc a{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}
.story-section{margin:48px 0}
.story-section h2{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.story-section p{margin:0 0 14px;color:#44403c}
.time-marker{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}
img{display:block;max-width:100%;height:auto}
figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}
figcaption{padding:14px 18px;color:#57534e;font-size:14px}
.summary-row{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}
.summary-row .time-marker{flex-shrink:0;margin-top:2px}
.summary-row strong{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}
.summary-row p{color:#57534e;margin:0;font-size:15px}
.takeaway-box{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}
.takeaway-box strong{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}
.takeaway-box p{color:#3b82f6;margin:0;font-size:15px}
.warn{background:#fff7ed;border-left:4px solid #f59e0b;padding:12px 16px;border-radius:8px;margin:16px 0;font-size:14px;color:#9a3412}
.bound{background:#f0fdf4;border-left:4px solid #22c55e;padding:12px 16px;border-radius:8px;margin:16px 0;font-size:14px;color:#166534}
.pitfall{background:#fef2f2;border-left:4px solid #ef4444;padding:12px 16px;border-radius:8px;margin:16px 0;font-size:14px;color:#991b1b}
.steps{background:#fff;border-radius:12px;padding:16px 20px;margin:16px 0;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.steps ol{margin:8px 0 0;padding-left:22px;color:#44403c}
.steps li{margin-bottom:8px}
.param{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#f1f5f9;padding:1px 6px;border-radius:4px;font-size:13px}
.transcript-section{margin-top:48px}
.transcript-note{font-size:14px;color:#78716c;margin-bottom:24px}
.transcript-list{list-style:none;padding:0;margin:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}.transcript-row p{margin:0}
.transcript-collapsible{border:none;margin:0;padding:0}
.transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}
.transcript-collapsible summary::before{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}
.transcript-collapsible[open] summary::before{transform:rotate(90deg)}
.transcript-collapsible[open] summary{margin-bottom:16px}
@media(max-width:640px){.container{padding:28px 18px 56px}header h1{font-size:24px}.transcript-row{grid-template-columns:56px 1fr;gap:10px}}"""


def build_svg(slug: str, body: str, key_tag: str) -> int:
    script = ROOT / "_work" / "b68" / f"build-{key_tag}-{slug}-svg.mjs"
    out_path = ROOT / "docs" / f"{slug}-理性分析.svg"
    script.write_text(
        "\nimport { writeFileSync } from 'fs';\n"
        "import { buildSvg } from '../../svg-auto-height.mjs';\n"
        f"const css = {json.dumps(SVG_CSS)}\n"
        f"const body = {json.dumps(body)}\n"
        "const { svg, height } = await buildSvg({ css, body, width: 1320 });\n"
        f"writeFileSync({json.dumps(str(out_path))}, svg);\n"
        "console.log('svg_height', height);\n",
        encoding="utf-8",
    )
    out = subprocess.check_output(["node", str(script)], cwd=str(ROOT), text=True)
    print(out.strip())
    return int(out.strip().split()[-1])


def merge_translations(slug: str, part: dict[str, str]) -> None:
    part_dir = ROOT / "_work" / "b68" / "translations-partial"
    part_dir.mkdir(parents=True, exist_ok=True)
    (part_dir / f"{slug}.json").write_text(
        json.dumps(part, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    tr_path = ROOT / "translations.json"
    tr = json.loads(tr_path.read_text(encoding="utf-8"))
    tr.update(part)
    tr_path.write_text(json.dumps(tr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_index_entry(entry: dict) -> None:
    slug = entry["slug"]
    ent_dir = ROOT / "_work" / "b68" / "index-entries"
    ent_dir.mkdir(parents=True, exist_ok=True)
    (ent_dir / f"{slug}.json").write_text(
        json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def enhance(slug: str) -> None:
    subprocess.check_call(
        ["python3", str(ROOT / "scripts" / "enhance-captions-html.py"), slug],
        cwd=str(ROOT),
    )


async def _tts_one(zh: str, en: str) -> None:
    try:
        import edge_tts
    except ImportError:
        print("no edge_tts")
        return
    if not en or not en.strip():
        return
    audio_dir = ROOT / "docs" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    h = hashlib.md5(zh.encode("utf-8")).hexdigest()[:12]
    path = audio_dir / f"{h}.mp3"
    if path.exists() and path.stat().st_size > 0:
        print("ok", h, path.stat().st_size)
        return
    try:
        communicate = edge_tts.Communicate(en, "en-US-JennyNeural")
        await communicate.save(str(path))
        print("ok", h, path.stat().st_size)
    except Exception as e:
        print("fail", h, type(e).__name__, e)


def gen_caption_audio(part: dict[str, str]) -> None:
    import re

    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for zh, en in part.items():
        m = re.match(r"\[(\d{1,2}:\d{2}(?::\d{2})?|\d+/\d+)\]\s*(.*)", zh)
        key = m.group(2) if m else zh
        if key in seen:
            continue
        seen.add(key)
        pairs.append((key, en))

    async def main() -> None:
        for zh, en in pairs:
            await _tts_one(zh, en)
            await asyncio.sleep(0.3)

    asyncio.run(main())


def finalize(slug: str, part: dict[str, str]) -> None:
    # WORKFLOW: gen-caption-audio before enhance
    gen_caption_audio(part)
    enhance(slug)


def fmt_duration(seconds: float) -> str:
    s = int(round(seconds))
    if s < 60:
        return f"{s}秒"
    m, sec = divmod(s, 60)
    if m < 60:
        return f"{m}分{sec:02d}秒" if sec else f"{m}分钟"
    h, m = divmod(m, 60)
    return f"{h}小时{m:02d}分"


def extract_frames(mp4: Path, slug: str, n: int | None = None) -> int:
    assets = ROOT / "docs" / "assets" / slug
    assets.mkdir(parents=True, exist_ok=True)
    dur = float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(mp4),
            ],
            text=True,
        )
    )
    if n is None:
        n = 10 if dur > 600 else 8
    existing = list(assets.glob("shot-*.jpg"))
    if len(existing) >= n:
        return n
    for i in range(1, n + 1):
        t = (i - 0.5) / n * dur
        out = assets / f"shot-{i:02d}.jpg"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{t:.2f}",
                "-i",
                str(mp4),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(out),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    return n


def copy_images(images_dir: Path, slug: str) -> int:
    import shutil

    assets = ROOT / "docs" / "assets" / slug
    assets.mkdir(parents=True, exist_ok=True)
    imgs = sorted(
        [
            p
            for p in images_dir.iterdir()
            if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        ]
    )
    for i, src in enumerate(imgs, 1):
        dst = assets / f"shot-{i:02d}.jpg"
        if src.suffix.lower() in {".jpg", ".jpeg"}:
            shutil.copy2(src, dst)
        else:
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(src), "-q:v", "2", str(dst)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
    return len(imgs)

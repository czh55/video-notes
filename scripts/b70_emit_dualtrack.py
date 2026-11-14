#!/usr/bin/env python3
"""从结构化 content dict 生成 b70 双轨（html/svg/translations/index/enhance/tts）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from b70_dualtrack_lib import (  # noqa: E402
    HTML_CSS,
    build_svg,
    finalize,
    fmt_duration,
    merge_translations,
    write_index_entry,
)
import html as html_mod
import re


def _esc(s: str) -> str:
    return html_mod.escape(s or "", quote=True)


def _clean_summary(s: str, limit: int = 120) -> str:
    t = re.sub(r"[…\.．]{2,}|\.\.\.", "，", (s or "").strip())
    t = re.sub(r"\s+", " ", t)
    if len(t) <= limit:
        return t
    cut = t[:limit]
    # avoid trailing orphan punctuation from hard cut
    return cut.rstrip("，,、；; ")


def emit(spec: dict) -> None:
    slug = spec["slug"]
    key = spec["key"]
    url = spec["url"]
    title = spec["title"]
    duration = spec.get("duration") or fmt_duration(float(spec["duration_s"]))
    tags = spec.get("tags") or ["达芬奇"]
    topic = " · ".join(tags[:4])
    summary = _clean_summary(spec["summary"])
    takeaway = spec["takeaway"]
    bound = spec.get("bound") or ""
    pitfall = spec.get("pitfall") or ""
    steps = spec.get("steps") or []
    chapters = spec["chapters"]  # [{id,time,title,body,shots:[(i,t,zh,en),...]}]
    transcript = spec.get("transcript") or []  # [(t,text)]
    primary = spec.get("primary") or "video"
    date = spec.get("date") or "2026-11-14"
    uploader = spec.get("uploader") or "小红书作者"

    toc = "\n".join(
        f'<a href="#{c["id"]}">{_esc(c["title"])}</a>' for c in chapters
    ) + '\n<a href="#transcript">口述/画面要点</a>'

    rows = ""
    for c in chapters:
        rows += (
            f'<div class="summary-row"><span class="time-marker">[{_esc(c["time"])}]</span>'
            f'<div><strong>{_esc(c["title"])}</strong><p>{_esc(c.get("blurb",""))}</p></div></div>\n'
        )

    sections = []
    part: dict[str, str] = {}
    shot_count = 0
    for c in chapters:
        figs = []
        for i, t, zh, en in c["shots"]:
            shot_count = max(shot_count, i)
            figs.append(
                f'<figure><img src="assets/{slug}/shot-{i:02d}.jpg" alt="{_esc(zh)}" loading="lazy">'
                f"<figcaption>[{_esc(t)}] {_esc(zh)}</figcaption></figure>"
            )
            part[zh] = en
            part[f"[{t}] {zh}"] = en
        steps_html = ""
        if c.get("steps"):
            lis = "".join(f"<li>{_esc(x)}</li>" for x in c["steps"])
            steps_html = f'<div class="steps"><strong>步骤</strong><ol>{lis}</ol></div>'
        sections.append(
            f'<section class="story-section" id="{c["id"]}">'
            f'<h2><span class="time-marker">{_esc(c["time"])}</span>{_esc(c["title"])}</h2>'
            f'<p>{_esc(c["body"])}</p>{steps_html}{"".join(figs)}</section>'
        )

    if not transcript:
        transcript = [(t, zh) for c in chapters for _, t, zh, _ in c["shots"]]
    tr_rows = "".join(
        f'<div class="transcript-row"><time>{_esc(t)}</time><p>{_esc(text)}</p></div>\n'
        for t, text in transcript
    )

    bound_html = f'<div class="bound"><strong>适用边界</strong>：{_esc(bound)}</div>' if bound else ""
    pit_html = f'<div class="pitfall"><strong>踩坑</strong>：{_esc(pitfall)}</div>' if pitfall else ""
    global_steps = ""
    if steps:
        global_steps = (
            '<div class="steps"><strong>总步骤</strong><ol>'
            + "".join(f"<li>{_esc(x)}</li>" for x in steps)
            + "</ol></div>"
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{_esc(summary)}">
<title>{_esc(title)}｜图文实录</title>
<style>{HTML_CSS}</style>
</head>
<body><main class="container">
<header>
  <h1>{_esc(title)}</h1>
  <div class="meta-row">
    <span class="meta-tag tag-platform">小红书</span>
    <span class="meta-tag tag-duration">{_esc(duration)}</span>
    <span class="meta-tag tag-topic">{_esc(topic)}</span>
  </div>
  <a class="source-link" href="{_esc(url)}" target="_blank" rel="noopener">→ 原视频链接</a>
</header>
<nav class="toc"><h3>内容导航</h3>
{toc}
</nav>
<article>
<div class="content-points">
  <h2>内容要点</h2>
  <p>{_esc(summary)}</p>
  <h3>知识结构</h3>
  {rows}
  {global_steps}
  <div class="takeaway-box"><strong>总结</strong><p>{_esc(takeaway)}</p></div>
  {bound_html}{pit_html}
</div>
{"".join(sections)}
<section class="transcript-section" id="transcript">
<details class="transcript-collapsible"><summary>口述/画面要点（{len(transcript)}段）</summary>
<div class="transcript-body">
<p class="transcript-note">结合 Whisper medium 与画面大字整理；专有名词已校对。</p>
<div class="transcript-list">{tr_rows}</div>
</div></details></section>
</article></main>
<script>(function(){{var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){{d.setAttribute("open","")}}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){{a.addEventListener("click",open)}});if(location.hash==="#transcript")open()}})();</script>
</body></html>
"""
    Path(f"docs/{slug}-图文实录.html").write_text(html, encoding="utf-8")

    # SVG cards from chapters — escape text so bare < in ASR won't break XML
    cards = []
    for c in chapters:
        blurb = c.get("blurb") or c["body"][:120]
        cards.append(
            f'<div class="card"><h3>{_esc(c["title"])}</h3><p>{_esc(blurb)}</p></div>'
        )
    action = "<br>".join(_esc(x) for x in steps[:6]) if steps else _esc(takeaway)
    svg_title = _esc(spec.get("svg_title") or title)
    svg_body = f"""
<div class="container">
  <h1>{svg_title}</h1>
  <div>{"".join(f'<span class="tag">{_esc(t)}</span>' for t in tags[:5])}</div>
  <p class="summary-line">{_esc(takeaway)}</p>
  {"".join(cards)}
  <div class="card"><h3>行动清单</h3><div class="action">{action}</div>
  {"<div class='pitfall'>" + _esc(pitfall) + "</div>" if pitfall else ""}
  {"<div class='bound'>" + _esc(bound) + "</div>" if bound else ""}
  </div>
  <div class="conclusion"><h2>结论</h2><p>{_esc(takeaway)}</p></div>
  <p class="footer">来源：小红书 · {_esc(uploader)} · {_esc(date)}</p>
</div>"""
    h = build_svg(slug, svg_body, key)
    merge_translations(slug, part)
    write_index_entry(
        {
            "date": date,
            "title": title,
            "summary": summary,
            "primary": primary,
            "skills": [],
            "tags": tags,
            "platform": "xiaohongshu",
            "url": url,
            "duration": duration,
            "outputs": {"html": f"{slug}-图文实录.html", "svg": f"{slug}-理性分析.svg"},
            "screenshot_count": shot_count,
            "transcript_segments": len(transcript),
            "svg_height": h,
            "slug": slug,
        }
    )
    finalize(slug, part)
    print(f"OK {key} {slug} svg_h={h} shots={shot_count}")


if __name__ == "__main__":
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    emit(spec)

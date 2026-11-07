#!/usr/bin/env python3
"""从结构化 content dict 生成 b68 双轨（html/svg/translations/index/enhance/tts）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from b68_dualtrack_lib import (  # noqa: E402
    HTML_CSS,
    build_svg,
    finalize,
    fmt_duration,
    merge_translations,
    write_index_entry,
)


def emit(spec: dict) -> None:
    slug = spec["slug"]
    key = spec["key"]
    url = spec["url"]
    title = spec["title"]
    duration = spec.get("duration") or fmt_duration(float(spec["duration_s"]))
    tags = spec.get("tags") or ["达芬奇"]
    topic = " · ".join(tags[:4])
    summary = spec["summary"]
    takeaway = spec["takeaway"]
    bound = spec.get("bound") or ""
    pitfall = spec.get("pitfall") or ""
    steps = spec.get("steps") or []
    chapters = spec["chapters"]  # [{id,time,title,body,shots:[(i,t,zh,en),...]}]
    transcript = spec.get("transcript") or []  # [(t,text)]
    primary = spec.get("primary") or "video"
    date = spec.get("date") or "2026-11-07"
    uploader = spec.get("uploader") or "小红书作者"

    toc = "\n".join(
        f'<a href="#{c["id"]}">{c["title"]}</a>' for c in chapters
    ) + '\n<a href="#transcript">口述/画面要点</a>'

    rows = ""
    for c in chapters:
        rows += f'<div class="summary-row"><span class="time-marker">[{c["time"]}]</span><div><strong>{c["title"]}</strong><p>{c.get("blurb","")}</p></div></div>\n'

    sections = []
    part: dict[str, str] = {}
    shot_count = 0
    for c in chapters:
        figs = []
        for i, t, zh, en in c["shots"]:
            shot_count = max(shot_count, i)
            figs.append(
                f'<figure><img src="assets/{slug}/shot-{i:02d}.jpg" alt="{zh}" loading="lazy">'
                f"<figcaption>[{t}] {zh}</figcaption></figure>"
            )
            part[zh] = en
            part[f"[{t}] {zh}"] = en
        steps_html = ""
        if c.get("steps"):
            lis = "".join(f"<li>{x}</li>" for x in c["steps"])
            steps_html = f'<div class="steps"><strong>步骤</strong><ol>{lis}</ol></div>'
        sections.append(
            f'<section class="story-section" id="{c["id"]}">'
            f'<h2><span class="time-marker">{c["time"]}</span>{c["title"]}</h2>'
            f'<p>{c["body"]}</p>{steps_html}{"".join(figs)}</section>'
        )

    if not transcript:
        transcript = [(t, zh) for c in chapters for _, t, zh, _ in c["shots"]]
    tr_rows = "".join(
        f'<div class="transcript-row"><time>{t}</time><p>{text}</p></div>\n'
        for t, text in transcript
    )

    bound_html = f'<div class="bound"><strong>适用边界</strong>：{bound}</div>' if bound else ""
    pit_html = f'<div class="pitfall"><strong>踩坑</strong>：{pitfall}</div>' if pitfall else ""
    global_steps = ""
    if steps:
        global_steps = (
            '<div class="steps"><strong>总步骤</strong><ol>'
            + "".join(f"<li>{x}</li>" for x in steps)
            + "</ol></div>"
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{summary}">
<title>{title}｜图文实录</title>
<style>{HTML_CSS}</style>
</head>
<body><main class="container">
<header>
  <h1>{title}</h1>
  <div class="meta-row">
    <span class="meta-tag tag-platform">小红书</span>
    <span class="meta-tag tag-duration">{duration}</span>
    <span class="meta-tag tag-topic">{topic}</span>
  </div>
  <a class="source-link" href="{url}" target="_blank" rel="noopener">→ 原视频链接</a>
</header>
<nav class="toc"><h3>内容导航</h3>
{toc}
</nav>
<article>
<div class="content-points">
  <h2>内容要点</h2>
  <p>{summary}</p>
  <h3>知识结构</h3>
  {rows}
  {global_steps}
  <div class="takeaway-box"><strong>总结</strong><p>{takeaway}</p></div>
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

    # SVG cards from chapters
    cards = []
    for c in chapters:
        cards.append(
            f'<div class="card"><h3>{c["title"]}</h3><p>{c.get("blurb") or c["body"][:120]}</p></div>'
        )
    action = "<br>".join(steps[:6]) if steps else takeaway
    svg_body = f"""
<div class="container">
  <h1>{spec.get("svg_title") or title}</h1>
  <div>{"".join(f'<span class="tag">{t}</span>' for t in tags[:5])}</div>
  <p class="summary-line">{takeaway}</p>
  {"".join(cards)}
  <div class="card"><h3>行动清单</h3><div class="action">{action}</div>
  {"<div class='pitfall'>" + pitfall + "</div>" if pitfall else ""}
  {"<div class='bound'>" + bound + "</div>" if bound else ""}
  </div>
  <div class="conclusion"><h2>结论</h2><p>{takeaway}</p></div>
  <p class="footer">来源：小红书 · {uploader} · {date}</p>
</div>"""
    h = build_svg(slug, svg_body, key)
    merge_translations(slug, part)
    write_index_entry(
        {
            "date": date,
            "title": title,
            "summary": summary[:120],
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

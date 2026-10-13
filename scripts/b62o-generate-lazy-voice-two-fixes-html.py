#!/usr/bin/env python3
"""b62o：生成 lazy-voice-two-fixes 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "lazy-voice-two-fixes"
KEY = "b62o"


def fmt(t: float) -> str:
    t = max(0, int(t))
    return f"{t // 60:02d}:{t % 60:02d}"


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_transcript() -> tuple[str, int]:
    whisper = json.loads((ROOT / f"{KEY}.json").read_text(encoding="utf-8"))
    rows = []
    n = 0
    for seg in whisper.get("segments", []):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        n += 1
        rows.append(
            f'<li class="transcript-row" id="transcript-{n}">'
            f'<time datetime="PT{int(seg["start"])}S">{fmt(seg["start"])}</time>'
            f"<p>{esc(text)}</p></li>"
        )
    return "\n".join(rows), n


def main() -> None:
    shots = json.loads((ROOT / f"shots-{SLUG}.json").read_text(encoding="utf-8"))["shots"]
    by_num = {int(s["file"].replace("shot-", "").replace(".jpg", "")): s for s in shots}
    transcript, n_seg = build_transcript()

    title = "说话声音懒散，没精神，两件事帮助改善"
    url = "https://xhslink.cn/o/53Yg0UDxRtr"
    duration = "1分13秒"
    intro = (
        "「小柯语音与演讲」约1分13秒竖屏口播：若说话声音懒洋洋、没有精气神，"
        "可以从「咬字」和「声音」两个维度提升——"
        "先把双唇与舌头的力度加起来，咬清每个字的边缘；"
        "再把声音往远处送，像抛物线把珠子扔出口腔。"
        "片尾收束为：送远感带来优雅感，精气神与形象感也会跟着改善。"
        "下列实录按时间线展开；观点属作者教学建议。"
    )
    summary_rows = [
        (
            "00:00→00:10",
            "问题与框架",
            "声音懒洋洋、没精气神时，别空练嗓，先拆成咬字与声音两个维度。",
        ),
        (
            "00:10→00:31",
            "咬字加力",
            "力度加强，避免松松垮垮；双唇舌头有力量感，咬字略带斩钉截铁。",
        ),
        (
            "00:31→01:13",
            "声音送远",
            "别让声音一说就落地结束；可带一点拖音，像抛物线扔珠子，送远后才有优雅感与精气神。",
        ),
    ]
    takeaway = (
        "两件事：咬字加力咬清边缘，声音按抛物线送远；"
        "作者认为精气神与形象感会因此改善——属可练习的表达习惯，非嗓音医学结论。"
    )

    def figs(*nums: int) -> str:
        out = []
        for num in nums:
            m = by_num[num]
            cap = m.get("caption") or m.get("scene") or ""
            alt = m.get("alt") or cap
            out.append(
                f'<figure><img src="assets/{SLUG}/{m["file"]}" alt="{esc(alt)}" loading="lazy">'
                f"<figcaption>[{m['time']}] {esc(cap)}</figcaption></figure>"
            )
        return "\n".join(out)

    summary_html = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{esc(label)}</strong><p>{esc(txt)}</p></div></div>"
        for tr, label, txt in summary_rows
    )

    chapters_html = f"""
<section class="story-section" id="ch-hook">
  <h2><span class="time-marker">00:00–00:10</span>懒洋洋没精气神：先定两个维度</h2>
  <p>视频开场直接点题：如果你也觉得自己说话时声音懒洋洋、没有精气神，作者给出的入口不是「练嗓条件」，而是「两个维度」——一个是咬字，一个是声音。顶栏黄字标题也同步写着「说话声音懒散 没有精气神 两件事能改善」，把整条短片的结构提前钉死。</p>
  <p class="quote">「那你可以从两个维度去提升——一个是你的咬字，一个是你的声音。」</p>
  {figs(1, 2)}
</section>

<section class="story-section" id="ch-articulation">
  <h2><span class="time-marker">00:10–00:31</span>第一件事：咬字加力，把字的边缘咬清楚</h2>
  <p>维度一落在咬字力度。作者要求把咬字「力度加强一点」，过程中不要松松垮垮；否则每个字其实都没真正咬清楚，字的边缘也不清晰。操作落点很具体：双唇和舌头的力量感要加强，让咬字带一点「斩钉截铁」的感觉。</p>
  <p>这一段的关键不是「说大声」，而是口腔动作有边界——字咬实了，听感才不会散、不会懒。</p>
  {figs(3)}
</section>

<section class="story-section" id="ch-project">
  <h2><span class="time-marker">00:31–01:13</span>第二件事：声音送远，像抛物线扔珠子</h2>
  <p>维度二转向声音的运行方式：讲话时要把声音「送远」。反面示范是声音一出口马上结束、缺少送出去的感觉。作者给了一个朴素理解——可以有一点点拖音，让声音稍微往远处「打远」一些。</p>
  <p>隐喻更直观：声音似乎像抛物线；把自己的声音当成一颗颗珠子，从口腔扔出去、往远处送。当声音有了送远感，而不是一下一下掉到地面上，听感会多出「优雅感」；讲话时整个人的精气神和形象感，也会因此得到一定改善。</p>
  <p class="quote">「把自己的声音当做一个一个的珠子，从自己的口腔扔出去，往远处送出去的感觉。」</p>
  {figs(4)}
</section>
"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{esc(intro[:140])}">
<title>{esc(title)}｜图文实录</title>
<style>*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}}
.container{{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}}header{{margin-bottom:40px}}
header h1{{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}}
.meta-row{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}}
.meta-tag{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}}
.tag-platform{{background:#ff2442;color:#fff}}.tag-duration{{background:#f1f5f9;color:#64748b}}.tag-topic{{background:#dbeafe;color:#1e40af}}
.source-link{{color:#3b82f6;font-size:14px;text-decoration:none}}.source-link:hover{{text-decoration:underline}}
.toc{{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}}
.toc h3{{font-size:16px;color:#1e40af;margin:0 0 12px}}.toc a{{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}}.toc a:hover{{color:#3b82f6}}
.documentary{{font-size:17px}}.story-section{{margin:48px 0}}
.story-section h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.story-section p{{margin:0 0 14px;color:#44403c}}
.quote{{background:#f8fafc;border-left:4px solid #cbd5e1;padding:10px 14px;border-radius:8px;margin:12px 0;font-size:15px;color:#57534e;font-style:italic}}
.time-marker{{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}}
img{{display:block;max-width:100%;height:auto}}figure{{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}}
figcaption{{padding:14px 18px;color:#57534e;font-size:14px}}
.transcript-section{{margin-top:48px}}
.transcript-note{{font-size:14px;color:#78716c;margin-bottom:24px}}
.transcript-list{{list-style:none;padding:0;margin:0}}
.transcript-row{{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}}
.transcript-row time{{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}}.transcript-row p{{margin:0}}
@media(max-width:640px){{.container{{padding:28px 18px 56px}}header h1{{font-size:24px}}.transcript-row{{grid-template-columns:56px 1fr;gap:10px}}}}
.transcript-collapsible{{border:none;margin:0;padding:0}}.transcript-collapsible summary{{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{{display:none}}
.transcript-collapsible summary::before{{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}}
.transcript-collapsible[open] summary::before{{transform:rotate(90deg)}}.transcript-collapsible[open] summary{{margin-bottom:16px}}
.summary-row{{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}}
.summary-row .time-marker{{flex-shrink:0;margin-top:2px}}
.summary-row strong{{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}}
.summary-row p{{color:#57534e;margin:0;font-size:15px}}
.takeaway-box{{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}}
.takeaway-box strong{{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}}
.takeaway-box p{{color:#3b82f6;margin:0;font-size:15px}}
.content-points h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.content-points h3{{font-size:20px;font-weight:700;color:#1c1917;margin:22px 0 14px}}
.warn{{background:#fff7ed;border-left:4px solid #f59e0b;padding:12px 16px;border-radius:8px;margin:16px 0;font-size:14px;color:#9a3412}}
</style>
</head>
<body><main class="container">
<header>
  <h1>{esc(title)}</h1>
  <div class="meta-row">
    <span class="meta-tag tag-platform">小红书</span>
    <span class="meta-tag tag-duration">{esc(duration)}</span>
    <span class="meta-tag tag-topic">职场表达 · 语音演讲</span>
  </div>
  <a class="source-link" href="{esc(url)}" target="_blank" rel="noopener">→ 原视频链接</a>
</header>
<nav class="toc"><h3>内容导航</h3>
<a href="#ch-hook">懒洋洋没精气神：先定两个维度</a>
<a href="#ch-articulation">第一件事：咬字加力</a>
<a href="#ch-project">第二件事：声音送远</a>
<a href="#transcript">完整转录</a>
</nav>
<article class="documentary">
<div class="content-points">
  <h2>内容要点</h2>
  <p>{esc(intro)}</p>
  <h3>知识结构</h3>
  {summary_html}
  <div class="takeaway-box"><strong>总结</strong><p>{esc(takeaway)}</p></div>
  <div class="warn">初始 Whisper 稿几乎只认出开场半句；本篇以 medium 重转录 34 段为准，并与片内字幕交叉核对。「松松垮垮」由「松松卡卡」据语境校正。</div>
</div>
{chapters_html}
<section class="transcript-section" id="transcript">
<details class="transcript-collapsible">
<summary>完整转录（{n_seg}段）</summary>
<div class="transcript-body">
<p class="transcript-note">以下文本由 Whisper medium 模型自动转录，已做简体转换与少量术语校正，可能仍有识别误差。</p>
<ol class="transcript-list">
{transcript}
</ol>
</div>
</details>
</section>
</article>
</main>
<script>(function(){{var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){{d.setAttribute("open","")}}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){{a.addEventListener("click",open)}});if(location.hash==="#transcript")open()}})();</script>
</body></html>
"""
    out = DOCS / f"{SLUG}-图文实录.html"
    out.write_text(html, encoding="utf-8")
    print(f"Generated: {out} segments: {n_seg}")


if __name__ == "__main__":
    main()

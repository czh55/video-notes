#!/usr/bin/env python3
"""b62c：生成 english-rhythm-melody-rules 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "english-rhythm-melody-rules"
KEY = "b62c"


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
    for i, seg in enumerate(whisper.get("segments", []), 1):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        rows.append(
            f'<li class="transcript-row" id="transcript-{i}">'
            f'<time datetime="PT{int(seg["start"])}S">{fmt(seg["start"])}</time>'
            f"<p>{esc(text)}</p></li>"
        )
    return "\n".join(rows), len(rows)


def main() -> None:
    shots = json.loads((ROOT / f"shots-{SLUG}.json").read_text(encoding="utf-8"))["shots"]
    by_num = {int(s["file"].replace("shot-", "").replace(".jpg", "")): s for s in shots}
    transcript, n_seg = build_transcript()

    title = "说英语必须掌握节奏和旋律规律"
    url = "https://xhslink.cn/o/1zY9O3Ur17C"
    duration = "1分09秒"
    intro = (
        "小红书 UP 主 Roger说美音（画面账号 imrogerchow）用约一分钟口播，把口语语调压成一条可跟练的节奏型："
        "英语像音乐，先往上造张力、再往下释放；短语或从句结束后上扬，信息结束时下落。"
        "片中用介词短语与 if 从句链当场示范。下列实录按时间线展开；Whisper 为繁体且有误识，正文以画面英中字幕与笔记文案校正。"
    )
    summary_rows = [
        ("00:00→00:09", "命题定调", "English is music：每句话都有上扬与下落，先建立「说话像唱歌」的听感。"),
        ("00:09→00:28", "张力规则", "往上制造张力 → 往下释放；关键是知道该在哪里上扬——短语/从句说完后。"),
        ("00:28→00:42", "介词短语", "on the table / under the light 等介词短语示范边界上扬，再落到 there is a book。"),
        ("00:42→01:02", "从句链", "clause=带动词的短语；if… / if… 上扬，we can eat together 收束下落；更有音乐性也更易懂。"),
        ("01:02→01:09", "互动收束", "点赞关注留言；想学英语可私聊（平台 CTA）。"),
    ]
    takeaway = (
        "先记住「上-上-下」：未说完的信息块上扬吊住听者，说完再下落释放；"
        "跟练时优先练短语边界与 if 从句链，而不是逐词平推。"
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

    toc = "".join(
        [
            '<a href="#ch-music">英语就是音乐</a>',
            '<a href="#ch-rule">往上张力、往下释放</a>',
            '<a href="#ch-phrase">介词短语示例</a>',
            '<a href="#ch-clause">从句链示例</a>',
            '<a href="#transcript">完整转录</a>',
        ]
    )

    chapters_html = f"""
<section class="story-section" id="ch-music">
  <h2><span class="time-marker">00:00–00:09</span>开场：英语就是音乐</h2>
  <p>视频在户外露台开拍。作者先用「Dada dada dada / 哒哒哒哒哒哒」做节奏口型，随即打出全片命题大字：<strong>English is music / 英语就是音乐</strong>。口播强调：每一句话都有上扬与下落，语调本身就像旋律线。Whisper 把「大致规则」误识成「法律」，画面字幕写的是 “And the general rule is like this / 大致的规则是这样的”，下文按画面校正。</p>
  {figs(1)}
</section>

<section class="story-section" id="ch-rule">
  <h2><span class="time-marker">00:09–00:28</span>规则：往上造张力，往下释放</h2>
  <p>规则被拆成两个动作。先是「往上」：字幕写 You go up and build up the tension——往上走、逐渐制造张力；作者举手示意音高抬升。接着「往下」：go down to release it——往下走把张力释放掉，手势同步下压。作者说真正的方法不是记住术语表，而是<strong>知道该在哪里上扬</strong>。</p>
  <p>操作落点写得很具体：基本上可以在说完一个 <strong>phrase（短语）</strong> 或 <strong>clause（从句）</strong> 之后往上扬。也就是说，信息还没说完时用上扬吊住听者，而不是每个词都平着念完。</p>
  <div class="quote">画面字幕：You can basically go up after you finish saying a phrase or a clause / 基本上你可以在说完一个短语或一个从句后往上扬</div>
  {figs(2, 3, 4)}
</section>

<section class="story-section" id="ch-phrase">
  <h2><span class="time-marker">00:28–00:42</span>示例一：介词短语怎么「上扬」</h2>
  <p>第一个可跟练模板是介词短语。字幕点名 a prepositional phrase，示范 <strong>on the table / 在桌子上</strong>，并补充 under the light / 在灯光下。作者用意是：短语作为一个信息块说完后可以上扬，再接到后续信息；当落到 there is a book / 有一本书 这类收束信息时，再考虑下落释放。</p>
  <p>这一段几乎全是短句示范，适合暂停跟读：先找短语边界，再决定音高走向上还是下。</p>
  {figs(5)}
</section>

<section class="story-section" id="ch-clause">
  <h2><span class="time-marker">00:42–01:09</span>示例二：从句链「上-上-下」</h2>
  <p>作者给从句一个极简定义（字幕）：a clause is a phrase with a verb——带有动词的短语就是从句。Whisper 把 clause 识成「Claus」，正文已校正。示范句是条件链：if I have time tomorrow（上扬）→ if I also have time（继续上扬）→ we can eat together（信息结束，下落释放）。笔记文案里的「往上，往上，往下」正是这条链的节奏型。</p>
  <p>收束主张：把这套节奏用到口语里，听起来会更有音乐性、也更有逻辑，别人更容易理解你在说什么。最后 7 秒是平台互动——点赞、关注、留言，并邀请想学英语的人聊聊；不含新知识点。</p>
  {figs(6)}
</section>
"""

    summary_html = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{esc(label)}</strong><p>{esc(txt)}</p></div></div>"
        for tr, label, txt in summary_rows
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{esc(intro[:140])}">
<title>{esc(title)}｜图文实录</title>
<style>
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}}
.container{{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}}
header h1{{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}}
.meta-row{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}}
.meta-tag{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}}
.tag-platform{{background:#ff2442;color:#fff}}.tag-duration{{background:#f1f5f9;color:#64748b}}.tag-topic{{background:#dbeafe;color:#1e40af}}
.source-link{{color:#3b82f6;font-size:14px;text-decoration:none}}.source-link:hover{{text-decoration:underline}}
.toc{{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}}
.toc h3{{font-size:16px;color:#1e40af;margin:0 0 12px}}
.toc a{{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}}
.toc a:hover{{color:#3b82f6}}
.documentary{{font-size:17px}}.story-section{{margin:48px 0}}
.story-section h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.story-section p{{margin:0 0 14px;color:#44403c}}
.time-marker{{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}}
img{{display:block;max-width:100%;height:auto}}
figure{{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}}
figcaption{{padding:14px 18px;color:#57534e;font-size:14px}}
.transcript-section{{margin-top:48px}}
.transcript-note{{font-size:14px;color:#78716c;margin-bottom:24px}}
.transcript-list{{list-style:none;padding:0;margin:0}}
.transcript-row{{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}}
.transcript-row time{{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}}
.transcript-row p{{margin:0}}
.transcript-collapsible{{border:none;margin:0;padding:0}}
.transcript-collapsible summary{{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{{display:none}}
.transcript-collapsible summary::before{{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}}
.transcript-collapsible[open] summary::before{{transform:rotate(90deg)}}
.transcript-collapsible[open] summary{{margin-bottom:16px}}
.summary-row{{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}}
.summary-row .time-marker{{flex-shrink:0;margin-top:2px}}
.summary-row strong{{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}}
.summary-row p{{color:#57534e;margin:0;font-size:15px}}
.takeaway-box{{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}}
.takeaway-box strong{{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}}
.takeaway-box p{{color:#3b82f6;margin:0;font-size:15px}}
.content-points h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.content-points h3{{font-size:20px;font-weight:700;color:#1c1917;margin:22px 0 14px}}
.quote{{background:#f8fafc;border-left:4px solid #cbd5e1;padding:10px 14px;border-radius:8px;margin:12px 0;font-size:15px;color:#57534e;font-style:italic}}
@media(max-width:640px){{.container{{padding:28px 18px 56px}}header h1{{font-size:24px}}.transcript-row{{grid-template-columns:56px 1fr;gap:10px}}}}
</style>
</head>
<body>
<main class="container">
<header>
  <h1>{esc(title)}</h1>
  <div class="meta-row">
    <span class="meta-tag tag-platform">小红书</span>
    <span class="meta-tag tag-duration">{duration}</span>
    <span class="meta-tag tag-topic">美音语调 · 口语节奏</span>
  </div>
  <p style="color:#57534e;font-size:14px;margin:0 0 12px">作者 Roger说美音 · 2026-10-13</p>
  <a class="source-link" href="{url}" target="_blank" rel="noopener">→ 原视频链接</a>
</header>
<nav class="toc"><h3>内容导航</h3>{toc}</nav>
<article class="documentary">
  <div class="content-points">
    <h2>内容要点</h2>
    <p>{esc(intro)}</p>
    <h3>知识结构</h3>
    {summary_html}
    <div class="takeaway-box"><strong>总结</strong><p>{esc(takeaway)}</p></div>
  </div>
  {chapters_html}
  <section class="transcript-section" id="transcript">
    <details class="transcript-collapsible">
      <summary>详细文字转录（{n_seg}段）</summary>
      <div class="transcript-body">
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现（多为繁体，含误识如「法律」「Claus」）；正文已按画面英中字幕与笔记文案校正，转录区保持原样以便核对。</p>
        <ol class="transcript-list">
{transcript}
        </ol>
      </div>
    </details>
  </section>
</article>
</main>
<script>(function(){{var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){{d.setAttribute("open","")}}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){{a.addEventListener("click",open)}});if(location.hash==="#transcript")open()}})();</script>
</body>
</html>
"""
    out = DOCS / f"{SLUG}-图文实录.html"
    out.write_text(html, encoding="utf-8")
    print(f"Generated: {out} segments={n_seg}")


if __name__ == "__main__":
    main()

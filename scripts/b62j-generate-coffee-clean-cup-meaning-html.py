#!/usr/bin/env python3
"""b62j：生成 coffee-clean-cup-meaning 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "coffee-clean-cup-meaning"
KEY = "b62j"


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

    title = "咖啡的干净指的是什么？"
    url = "https://xhslink.cn/o/72V75eiXrkN"
    duration = "3分59秒"
    intro = (
        "小红书账号「甄茶笔记&大喜」用一杯水洗咖啡常被夸「干净」当切口："
        "行业说的干净通常不是卫生，更不是「用水洗过所以更干净」。"
        "视频先用画面拆开水洗处理的阶段与日晒对照，说明关键在于更早减少完整果肉参与后续干燥；"
        "再划清水洗不是干净认证、风格不等于等级；最后给出杯中判断线索，"
        "并把干净收束为「风味轮廓清楚、杂味较少」。下列实录按时间线展开；"
        "中段口播稀疏，叙述以画面标题与硬字幕重建为主，观点均标注为作者科普。"
    )
    summary_rows = [
        ("00:00→00:40", "概念纠偏", "干净≠卫生、≠洗衣服；更接近味道容易分开、杂味不拖尾的感受。"),
        ("00:40→01:15", "水洗机制", "豆是种子；去皮→处理果胶/发酵清洗→羊皮干燥。关键不是碰了很多水。"),
        ("01:15→02:10", "日晒对照", "水洗更早去掉果实组织，整果长期发酵影响通常更小；但仍会发酵，不是认证。"),
        ("02:10→03:10", "风格边界", "水洗常见清晰酸质；同一豆不同处理是表达差异；优秀日晒也可干净。"),
        ("03:10→03:59", "杯中定义", "看味道是否分开、余味有无杂味；干净来自减弱果肉长期影响，不是洗得更干净。"),
    ]
    takeaway = (
        "水洗咖啡被说「干净」，指的是杯中风味轮廓清楚、杂味较少，"
        "而不是洗得更卫生。机制上它通常更早去掉完整果肉对干燥的长期参与；"
        "品鉴时别只盯酸，试着分辨味道是否分开、喝完有没有奇怪杂味拖着不走。"
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

    chapters_html = f"""
<section class="story-section" id="ch1">
  <h2><span class="time-marker">00:00–00:40</span>开场：行业「干净」不是卫生，也不是洗衣服</h2>
  <p>视频以系列课口吻开场（画面标 SP011）。标题直接问：水洗咖啡的「干净」到底是什么？旁边两枚标签抢答——杂味更少、风味更清楚；并写明关键在处理方式：去掉果肉和黏液，让豆子本身更容易被喝懂。</p>
  <p>口播只留下一句很短的引子（Whisper：「为什么很多人一喝水洗咖啡就会说」），随后几乎全靠画面推进。作者用「咖啡又不是洗衣服」做反差，把咖啡杯和洗衣机并置，字幕追问：难道水洗咖啡真因为拿水洗过，所以喝起来更干净？紧接着给出行业口径：说一杯咖啡「干净」，通常不是说它卫生；它更接近一种感受——同样有柑橘、花香、酸甜感时，各种味道比较容易一个个分开。</p>
  {figs(1, 2)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:40–01:15</span>水洗在做什么：四阶段与「关键不是很多水」</h2>
  <p>为了解释「为什么这种形容常落在水洗身上」，画面先回到果实结构：咖啡豆是果实里的种子；外面有果皮、果肉，还有一层非常黏的果胶。随后进入「水洗处理的四个阶段」：去皮后，再通过发酵、机械去胶等方式处理剩余果胶，清洗，再把带羊皮层的咖啡种子干燥。</p>
  <p>作者把 SCA 概括的核心动作压成两步视觉：去掉果肉时果胶往往还在，再靠发酵与清洗去掉黏性的 mucilage（黏液）。真正重要的，画面用一条橙线划掉水滴——关键不是碰了很多水；并点明这和日晒差别非常大。本段 Whisper 几乎空白，以上句子均来自硬字幕与标题重建。</p>
  {figs(3, 4)}
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">01:15–02:10</span>对照日晒：更早去掉果实组织，但不是干净认证</h2>
  <p>日晒侧的关键画面是：相当长一段时间里，种子还待在完整果实里面。水洗侧则强调更早去掉果实组织，于是后续由完整果实长期干燥和发酵带来的影响通常会小一些；作者据此说它特别适合突出单一产地本身的风味特征（画面词：干净·一致·产地特征）。</p>
  <p>纠偏立刻跟上：水洗一样会发酵，一样可以产生杂味或缺陷。所以不要把「水洗」理解成一张干净认证——印章被划掉的画面把这句钉死。Whisper 在此附近只抓到孤零零的「发酵」，与画面标题「水洗一样会发酵」相互印证。</p>
  {figs(5, 6)}
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">02:10–03:10</span>研究线索与风格边界：表达不同，不等于等级高低</h2>
  <p>作者引用「2026 年一项直接比较发酵」相关研究的叙述：那组水洗咖啡反而具有最高的有机酸浓度；并过渡到水洗常见的清晰风味——例如清晰酸质；当强烈果肉发酵特征不那么突出时，轮廓往往更清楚。注意：视频未给出论文名与样本细节，此处按作者观点呈现，未作外部核实。</p>
  <p>同一支埃塞豆的对照最直观：水洗像柠檬花茶，另一种处理更偏浆果果酱。结论不是「谁更正宗」，而是处理方式改变了最后进入杯子里的风味表达。平台上反复出现的水洗/日晒/蜜处理之争，背后常混淆「风格≠等级」：优秀水洗可以干净且复杂；优秀日晒也可以干净，水果感强未必就不干净。</p>
  {figs(7)}
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">03:10–03:59</span>杯中怎么判：线索收束到「轮廓清楚、杂味较少」</h2>
  <p>机制句再次收紧：水洗只是减弱果肉长期影响，让咖啡本身的轮廓更容易被喝出来。品鉴时先别只看酸，可以找更有意思的东西——画面标题写作「用五个线索判断干净度」。口播在尾段重新变密（也是 Whisper 主要抓到的部分）：这杯里面的味道是不是很容易被你一个一个分开？柑橘是柑橘，花香是花香，甜感是甜感；喝完以后嘴里有没有奇怪的杂味拖着不走。这才更接近咖啡师说的：「这杯很干净。」</p>
  <p>最后记住：水洗咖啡的干净，不是因为它用水洗得比较干净，而是处理方式通常减少了完整果肉长期参与后续干燥的影响，最后更容易得到风味轮廓清楚、杂味较少的杯中表现。最终定义卡把这两点并排高亮。</p>
  {figs(8)}
</section>
"""

    summary_html = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{esc(label)}</strong><p>{esc(txt)}</p></div></div>"
        for tr, label, txt in summary_rows
    )

    toc = "".join(
        f'<a href="#{cid}">{t}</a>'
        for cid, t in [
            ("ch1", "干净≠卫生/洗衣服"),
            ("ch2", "水洗四阶段与关键机制"),
            ("ch3", "日晒对照与非认证"),
            ("ch4", "风格≠等级"),
            ("ch5", "杯中线索与最终定义"),
            ("transcript", "完整转录"),
        ]
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
    <span class="meta-tag tag-topic">水洗咖啡 · 干净杯 · 处理法</span>
  </div>
  <p style="color:#57534e;font-size:14px;margin:0 0 12px">作者 甄茶笔记&amp;大喜 · 2026-10-13</p>
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
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差与繁体字形；正文已按画面硬字幕与语境校正为简体，并补全中段空白处的画面信息。约 00:03–03:10 口播极稀疏，请以章节叙述与图注为准。</p>
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

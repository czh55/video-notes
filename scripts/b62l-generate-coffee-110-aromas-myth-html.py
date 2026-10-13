#!/usr/bin/env python3
"""b62l：生成 coffee-110-aromas-myth 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "coffee-110-aromas-myth"
KEY = "b62l"


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

    title = "咖啡真的有 110 种香气吗？"
    url = "https://xhslink.cn/o/5kT10zg9OBj"
    duration = "4分05秒"
    intro = (
        "小红书账号「甄茶笔记&大喜」拆开一句常见口号："
        "咖啡是不是真有「110 种香气」？"
        "视频先给答案——110 指的是世界咖啡研究组织（WCR）感官词典第一版里的 110 个感官属性，"
        "不只香气，也含酸苦与口感质地，而且是会更新的活词典，不是天花板。"
        "接着说明风味轮是把这套语言画成地图，用法应从中间往外；"
        "新手只喝到酸苦很正常，具体风味多半靠鼻后嗅觉与感官记忆；"
        "包装上的「草莓」是相似描述，不是配料表。"
        "下列实录按时间线展开；观点均标注为作者口播与画面。"
    )
    summary_rows = [
        ("00:00→00:12", "开场误区", "包装写草莓茉莉，却只喝到酸苦；弄不清时风味轮会让人更怀疑自己。"),
        ("00:12→00:49", "110 是什么", "110=WCR 词典感官属性数，不是香气总数；105 样品整理的活词典，非上限。"),
        ("00:49→01:14", "尺子非评分", "也收录霉味泥土味甚至石油气味；只描述出现了什么与强度，不自动打分。"),
        ("01:14→01:46", "风味轮用法", "地图不是答案库；从中心大类往外走到子类与具体水果，可停在任一层。"),
        ("01:46→02:46", "味觉与嗅觉", "酸苦靠舌头；具体香气多靠鼻后通路；风味词是「更像什么」不是完全相同。"),
        ("02:46→03:15", "记忆与包装词", "咖啡师差在感官记忆与参考物校准；草莓是交流用相似描述，加味豆另判。"),
        ("03:15→04:05", "怎么练与收束", "厨房参考物先练闻；110 非天花板，风味轮非标准答案——先问自己感受到了什么。"),
    ]
    takeaway = (
        "别把「110」当成香气排行榜或上限；别拿风味轮从外圈对答案。"
        "先描述大类，再细化；包装风味词是沟通语言。"
        "想练就从橙子柠檬杏仁黑巧这类厨房参考物开始建立气味记忆。"
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
  <h2><span class="time-marker">00:00–00:12</span>开场：包装很香，嘴里却只剩酸和苦</h2>
  <p>标题直接抛出问题：咖啡真的有 110 种香气吗？画面用风味轮和一杯黑咖啡把「香气语言」摆上台面，随即落到日常挫败感——包装上写着草莓、茉莉花，喝起来却只感到酸和苦。</p>
  <p>作者把观众的自我怀疑压成二选一：到底是豆子在吹牛，还是你的味觉不够好？并提醒：如果这件事没弄明白，风味轮不但帮不了你，反而会让你越喝越怀疑自己。（转录里「钟伟伦」按全片语境校正为「风味轮」。）</p>
  {figs(1)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:12–00:49</span>先说答案：110 不是香气总数，也不是上限</h2>
  <p>答案来得很早：咖啡并不是「只有 110 种香气」。所谓 110，指的是世界咖啡研究组织（WCR）建立的咖啡感官词典第一版里的 110 个感官属性——里面不只有香气，还包括酸、苦等味觉，以及和口感、质地有关的描述。</p>
  <p>作者继续拆第二层误解：这 110 也不是咖啡风味的上限。研究人员当时花了超过 100 个小时，评估来自 13 个国家的 105 个阿拉比卡样品，才整理出这套词典；WCR 自己也明确说，它是一份会继续更新的活词典——因为 105 支咖啡不可能代表全世界所有咖啡。</p>
  {figs(2)}
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">00:49–01:14</span>好闻不好闻都要能写：尺子，不是排行榜</h2>
  <p>更反常识的一点是：词典里不只有蓝莓、茉莉花、巧克力和焦糖，还有霉味、泥土味，甚至石油气味。画面用「记录出现了什么，不等于推荐」点明立场。</p>
  <p>为什么研究品质还要写这些不讨喜的味道？因为感官词典的任务，不是告诉你哪种风味更高级、哪种豆子更值钱；它首先只回答一件事——这杯咖啡里出现了什么感觉，强度大概有多少。它是一把用来描述和测量的尺子，不是一张自动评分表。</p>
  {figs(3)}
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">01:14–01:46</span>风味轮是地图：从中间往外走</h2>
  <p>那常见的咖啡风味轮又是什么？作者把它理解成：把这套专业语言整理成一张更容易使用的地图。它以 WCR 感官词典为重要基础，但正确用法不是拿着包装从最外圈开始找「草莓在哪里」。</p>
  <p>正确方法恰恰是从中间往外：先喝一口，只判断大方向——像水果，还是像坚果、可可；如果像水果，再判断是莓果、核果还是柑橘；确定像柑橘以后，再分辨更像葡萄柚、橙子、柠檬还是青柠。你可以停在任何一层，不必每次都猜到最具体的水果。</p>
  {figs(4)}
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">01:46–02:46</span>新手只喝到酸苦很正常；风味多半是「闻到的」</h2>
  <p>所以新手只喝到酸和苦非常正常：酸和苦是舌头能直接感觉到的基础味觉；而草莓、茉莉花、巧克力这类具体风味，往往还需要鼻子一起参与。咖啡进入口腔以后，香气会从口腔后方向上进入鼻腔——你以为自己在尝草莓，其实很大一部分信息是闻到的。</p>
  <p>作者用「苦」做类比：黄连是苦的，黑巧克力也是苦的，但入口绝不会让人觉得是同一种苦，因为最终感受还混合了香气、强度、口感和余味。风味词也是同样道理：它描述的是一整组感觉更像什么，不是说两样东西的味道完全相同。</p>
  {figs(5)}
</section>

<section class="story-section" id="ch6">
  <h2><span class="time-marker">02:46–03:15</span>咖啡师差在记忆库；包装「草莓」不是配料表</h2>
  <p>为什么咖啡师能说出蓝莓、红茶、茉莉花，你却只能说「挺酸、还挺香」？作者认为不一定是舌头更灵，更多时候是感官记忆不同——他们反复闻、反复比较，还会用标准参考物去校准「大家说的蓝莓大概指怎样一种感觉」。训练的目的，是把「这个味道很熟」变成「它更接近什么」。</p>
  <p>包装上写草莓，通常也不是说豆子里真的加了草莓，更不是喝起来和草莓汁一模一样。对普通没有额外加味的咖啡，更准确的理解是：先感受到莓果这一大类特征，再往下判断它在香气、酸甜感或整体组合上更接近草莓。所以「草莓」是帮助交流的相似描述，不是配料表，也不是要求你必须喝出一个标准答案；明确加味或使用外源共发酵的咖啡，则要另外判断。</p>
  {figs(6)}
</section>

<section class="story-section" id="ch7">
  <h2><span class="time-marker">03:15–04:05</span>厨房参考物怎么练；真正会用风味轮问什么</h2>
  <p>普通人怎么练？不用先买一整套专业工具。准备橙子、柠檬和葡萄柚，再放一点杏仁、花生、黑巧克力和红糖；先分辨闻，再闭上眼睛重新闻，慢慢给这些气味建立记忆。下次喝咖啡时，也别逼自己立刻说出水蜜桃——先判断是水果类还是坚果可可类，再从水果走到柑橘，从柑橘走到橙子。</p>
  <p>收束句很清楚：110 不是咖啡香气的天花板，风味轮也不是标准答案；它更像一本词典，帮助你把「我感觉有点香」一步步说成「像水果、像柑橘，最后有点像橙子」。真正会用风味轮，不是拼命寻找包装上的答案，而是先问自己：我现在到底感受到了什么？片尾留下互动：你喝咖啡时，最容易认出来的是水果、花香，还是坚果巧克力？</p>
</section>
"""

    summary_html = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{esc(label)}</strong><p>{esc(txt)}</p></div></div>"
        for tr, label, txt in summary_rows
    )

    toc = "".join(
        f'<a href="#{cid}">{title}</a>'
        for cid, title in [
            ("ch1", "包装香 vs 嘴里酸苦"),
            ("ch2", "110=感官属性，非上限"),
            ("ch3", "尺子不是评分表"),
            ("ch4", "风味轮从内往外"),
            ("ch5", "酸苦正常与鼻后嗅觉"),
            ("ch6", "记忆库与包装词"),
            ("ch7", "厨房练习与收束"),
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
    <span class="meta-tag tag-topic">咖啡 · 感官词典 · 风味轮</span>
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
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差；正文已按画面与语境校正（如风味轮、霉味、核果、黄连、没有额外加味），转录区保持原样以便核对。</p>
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

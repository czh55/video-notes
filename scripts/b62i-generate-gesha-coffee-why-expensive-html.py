#!/usr/bin/env python3
"""b62i：生成 gesha-coffee-why-expensive 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "gesha-coffee-why-expensive"
KEY = "b62i"


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

    title = "瑰夏咖啡，为什么能卖这么贵？"
    url = "https://xhslink.cn/o/3KvyJWICIkc"
    duration = "3分17秒"
    intro = (
        "小红书账号「甄茶笔记&大喜」用一个尖锐对照开场："
        "同样叫瑰夏，普通咖啡馆的一杯和冠军拍卖批次，价格可以差到天上。"
        "视频先用画面抛出极端拍卖数字，再把「贵」拆成品种潜力、具体（微）批次与市场竞价三层，"
        "并强调同名不等于同源、拍卖价不能倒推普通成本。"
        "结尾落到买豆清单与口味匹配。下列实录按时间线展开；数字与历史细节均标注为视频画面/作者口播，未独立核验。"
    )
    summary_rows = [
        ("00:00→00:30", "价差锚点", "冠军小批次可拍到约每公斤 3 万美元量级；产量低只说对一部分，真正拉开差距的是潜力、批次与竞价。"),
        ("00:30→00:54", "品种潜力", "WCR 口径：高海拔品质潜力极高、产量潜力低；花香/茉莉/桃子/茶感带来辨识度，是进入高价市场的门票。"),
        ("00:54→01:28", "名字≠顶级", "多个遗传背景曾共用 Geisha/Gesha 名；T2722 也需海拔、成熟采摘与管理；2004 翡翠庄园分区独立批次改写玩法。"),
        ("01:28→02:29", "稀缺与竞价", "筛选越细量越少；售价≠成本；极端拍卖价是成交结果，不能倒推普通生产成本。"),
        ("02:29→03:17", "怎么买", "别贴智商税标签，也别只看「瑰夏」二字；问清国家/庄园/地块/处理/批次，并先确认口味偏好。"),
    ]
    takeaway = (
        "真正贵的往往不是「瑰夏」这两个字，"
        "而是把品质潜力做出来、信息清楚、数量又很少的具体批次。"
        "买之前先问批次信息，再问自己更想为花香茶感买单，还是更看重稳定厚重与性价比。"
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
  <h2><span class="time-marker">00:00–00:30</span>开场：同名瑰夏，为什么不是同一个价格</h2>
  <p>封面把咖啡果、瑰夏包装、一杯咖啡、生豆麻袋和拍卖槌摆在同一张桌上，标题直接问：「瑰夏为什么这么贵？」约前 30 秒口播几乎被 Whisper 漏掉，信息主要靠画面推进。</p>
  <p>作者先抛出一个极端锚点：在 2025 年 Best of Panama，一支约 20 公斤的冠军批次被标到每公斤约 30,204 美元（画面数字）。紧接着把「普通瑰夏批次」和「冠军小批次」并置，点破常见误解——很多人以为贵只因树难种、产量低；画面写「只说对一部分」。真正拉开差距的，是品种潜力、具体（微）批次，还有市场竞价。</p>
  {figs(1, 2, 3)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:30–00:54</span>第一层：品种潜力给了入场门票</h2>
  <p>口播接上：这里主要说的是著名的 Panama Geisha。世界咖啡研究（WCR）把它在高海拔的品质潜力评为极高，产量潜力却是低——它不是靠结很多果实取胜，而是在管理得当的高海拔环境里，有机会表现出细致的花香、茉莉、桃子和茶感。</p>
  <p>作者把这种辨识度定位为「进入高价市场的基础」。话锋一转抛出观众疑问：既然品种这么厉害，随便找个地方种瑰夏，不就能卖高价了吗？</p>
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">00:54–01:28</span>名字本身不等于顶级瑰夏</h2>
  <p>答案很干脆：还真不行。瑰夏这个名字本身不等于顶级瑰夏。WCR 提醒过，世界上有多个遗传背景不同的咖啡都曾被叫做 Geisha/Gesha——画面用 DNA 示意写「同名，不一定同源」。</p>
  <p>真正让巴拿马瑰夏出名的 T2722 后代，也要在合适海拔、成熟采摘和良好管理下，才可能发挥品质潜力。即使是同一个庄园，不同地块、采收时间和处理批次，结果也可能完全不同。</p>
  <p>历史节点落到 2004 年：翡翠庄园第一次把不同区域采收的咖啡分成独立批次；来自高海拔 Jaramillo 的一批 100% Geisha 单独杯测后香气突出，并与后续比赛、拍卖纪录叙事衔接（具体名次与金额以画面为准，未独立核验）。</p>
  {figs(4)}
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">01:28–02:29</span>稀缺与竞价：售价很高，不等于成本就这么高</h2>
  <p>这一段 Whisper 出现长空洞与乱码，内容以画面字幕为准。作者先讲筛选：越细筛，最终能留下的量往往越少——冠军小批次是「剩下来」的稀缺结果。</p>
  <p>接着纠偏成本直觉：售价很高，不等于生产成本就这么高。画面给出冠军批次约 20 公斤、总成交约 604,080 美元等数字，并强调它面对的不是普通农产品批发市场，而是全球买家争夺极少量冠军批次的拍卖场。</p>
  <p>关键句写在画面上：「拍卖价是成交结果，不能倒推普通成本。」同名瑰夏可能分别来自普通商用批次、高海拔微批次、获奖批次与年度冠军——价格谈的是层级，不是两个字本身。</p>
  {figs(5)}
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">02:29–03:17</span>买之前先问批次，也先问自己的口味</h2>
  <p>消费决策段把情绪标签先拿掉：先别急着说它是智商税，也别只看到「瑰夏」两个字就认定它值。你真正应该问的是——哪个国家、哪个庄园、哪个地块、什么处理，有没有明确批次信息？</p>
  <p>最后还要看它是不是符合你的口味。喜欢深烘、坚果、巧克力和厚重低酸的人，未必会喜欢一只花香明显、口感像茶的浅烘瑰夏。</p>
  <p>收束逻辑很清楚：品种潜力给了高端市场门票；精细生产与微批次筛选减少了数量；比赛、稀缺和竞价又把最顶尖的一小部分继续推高。真正贵的不是「瑰夏」这两个字，而是那些把品质潜力发挥出来、信息清楚而且数量很少的具体批次。片尾留下选择题：同样预算，你更愿意为鲜明花香和茶感买单，还是更看重稳定、厚重和性价比？</p>
  {figs(6)}
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
            ("ch1", "同名瑰夏为何不是同价"),
            ("ch2", "品种潜力是入场门票"),
            ("ch3", "名字≠顶级：同源与分区"),
            ("ch4", "稀缺竞价与成本纠偏"),
            ("ch5", "批次清单与口味匹配"),
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
    <span class="meta-tag tag-topic">咖啡 · 瑰夏 · 批次与拍卖</span>
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
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差；正文已按画面与语境校正（如瑰夏、结很多果实、微批次、Jaramillo），转录区保持原样以便核对。约 00:00–00:30 与 01:28–02:29 口播/字幕漏识别较多，信息见画面文案与章节叙述。</p>
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

#!/usr/bin/env python3
"""b62d：生成 coffee-bean-surface-oil 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "coffee-bean-surface-oil"
KEY = "b62d"


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

    title = "咖啡豆出油，是更香还是放坏了？"
    url = "https://xhslink.cn/o/2ZHWNtP6QqN"
    duration = "2分04秒"
    intro = (
        "小红书账号「甄茶笔记&大喜」用一整豆表面的油光当切口："
        "油亮既不能证明更香，也不能单独证明放坏了。"
        "视频先用示意动画讲清油脂本就存在、烘焙与存放会让油迁到表面，"
        "再把「油光」和「挥发香气」拆开，最后给出一套看烘焙深度、日期、开袋与储存的判断清单，"
        "并划清霉变属于安全边界、不要试喝。下列实录按时间线展开；观点均标注为作者口播与画面。"
    )
    summary_rows = [
        ("00:00→00:30", "二元误区", "油亮≠更香，也≠放坏；豆子本就有油脂，深烘更易出油。"),
        ("00:30→00:54", "存放出油", "存放后小油滴是原有油脂迁移；不能只按放了多少天判断。"),
        ("00:54→01:19", "油≠香", "看见的是油，闻到的是挥发物；油光变多≠香气变多，还可能哈喇。"),
        ("01:19→01:46", "判断清单", "看深烘/日期/开袋/密封/温度；香气变弱查储存；霉变勿试喝。"),
        ("01:46→02:04", "行动结论", "别冲油光买，也别只因出油就扔；密封避高温，盯香气味道。"),
    ]
    takeaway = (
        "油亮只能说明油到了表面。"
        "买豆别冲着油光买，扔豆也别只因为出油；开袋后密封、避高温，用实际香气与味道做主判断，霉变豆子直接放弃试喝。"
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
  <h2><span class="time-marker">00:00–00:30</span>开场：油亮既不能证明更香，也不能证明放坏了</h2>
  <p>视频一上来就把观众常有的直觉压成二选一：「咖啡豆油亮亮的，是更香还是放坏了？」画面用三颗反光明显的深烘豆特写把「油亮」钉在视觉上，随后立刻用大字纠偏——既不能证明更香，也不能证明放坏了。</p>
  <p>约 00:04 到 00:30 口播几乎空白，信息主要靠画面文案推进：咖啡豆本来就有油脂；普通原味豆表面看到的油，通常来自豆子内部；烘焙时豆子会膨胀，油脂更容易往表面移动；一般来说烘得越深越容易出油，有些深烘豆在烘焙时就能看到油光。这一段把「油」从神秘卖点还原成物理迁移。</p>
  {figs(1, 2)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:30–00:54</span>浅烘干爽≠无油；存放后的小油滴是迁移</h2>
  <p>口播接上：浅烘豆看着干爽，也不等于里面没有油。那为什么有些豆子刚开始不怎么亮，放着放着却出油了？作者引用烘焙研究拍到的变化（画面标注 Schenker·2000 Fig.65，并注明「变化示意，非研究原图」）：深烘样本刚烘完时表面比较光滑，存放之后出现了许多小油滴。</p>
  <p>关键句是：「这不是存放让豆子凭空多了油，而是原有的油脂继续移到了表面。」烘焙方式也会影响这个变化，因此不能只按放了多少天判断。</p>
  {figs(3)}
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">00:54–01:19</span>油到了外面，香气不一定更足</h2>
  <p>观众下一问很自然：油到了外面，香气是不是也更足了？作者直接答「不一定」。你看到的是油；闻到的咖啡香来自许多能挥发的香气物质。油光变多不等于香气也变多。</p>
  <p>存放过程中香气会散失，也会发生化学变化，油脂还可能氧化。有的豆子看着仍然油亮，香气却已经弱了，甚至出现哈喇味。反过来，表面没什么油的豆子，也不能靠这个证明自己新鲜——干爽与新鲜度之间没有单向箭头。</p>
  {figs(4)}
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">01:19–01:46</span>拿到油亮豆怎么看：清单 + 霉变边界</h2>
  <p>实用段给出检查顺序：先看是不是深烘；再看烘焙日期、开袋多久、有没有密封、有没有放在热的地方。如果是烘焙日期很近的深烘豆，不能一见油就认定它坏了。</p>
  <p>若同一包豆、冲法没变，香气却明显变弱或出现陈旧味，就要留意储存和新鲜度，别把它解释成「油更多所以更香」。作者同时划清边界：风味比较不是安全检测；已经有明显霉变的豆子，就不要再试喝了——画面给出带白色霉斑的豆子示例。</p>
  {figs(5, 6)}
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">01:46–02:04</span>记住：油亮只说明油到了表面</h2>
  <p>收束很干脆：油亮只能说明油到了表面。买豆别冲着油光买；扔豆也别只因为它出油。开袋后密封好、避开高温，关注实际的香气和味道变化，比盯着它亮不亮更有用。</p>
  <p>片尾留下互动题：「你那包豆，是刚开袋就油亮，还是放着放着才出油？」——把观察从单一外观指标，拉回「何时出油」与储存史。</p>
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
            ("ch1", "二元误区：油亮≠更香/放坏"),
            ("ch2", "存放出油是迁移"),
            ("ch3", "油光≠香气"),
            ("ch4", "判断清单与霉变边界"),
            ("ch5", "行动结论"),
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
    <span class="meta-tag tag-topic">咖啡豆 · 表面出油 · 储存</span>
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
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差；正文已按画面与语境校正（如开袋、哈喇味、霉变），转录区保持原样以便核对。约 00:04–00:30 口播空白，信息见画面文案与章节叙述。</p>
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
